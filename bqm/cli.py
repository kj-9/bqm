from __future__ import annotations

import warnings
from functools import wraps
from zoneinfo import ZoneInfo

import click
from sqlalchemy import Column, MetaData, String, Table, create_engine
from sqlalchemy.dialects import registry
from sqlalchemy.engine import Engine
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import Selectable
from sqlalchemy.sql import select as sa_select
from sqlalchemy.sql.expression import literal_column

# Suppress the specific warning
warnings.filterwarnings(
    "ignore",
    message="Cannot create BigQuery Storage client, the dependency google-cloud-bigquery-storage is not installed.",
    category=UserWarning,
    module="google.cloud.bigquery.client",
)


class Runner:
    engine: None | Engine

    def __init__(self) -> None:
        registry.register("bigquery", "sqlalchemy_bigquery", "BigQueryDialect")
        self.engine = None
        self.metadata = MetaData()

    def get_table(
        self,
        project_name: str,
        dataset_name: str,
        table_name: str,
    ) -> Table:
        # we don't do auto_load here because:
        # 1. INFORMATION_SCHEMA.XYZ views raise error when auto_load due to current implementation of sqlalchemy-bigquery
        # 2. It requires interaction to BigQuery to get metadata which makes tests harder
        table = Table(
            f"{project_name}.{dataset_name}.{table_name}",
            self.metadata,
        )
        return table

    def execute(self, stmt: Selectable, params=None) -> list[dict]:
        if not self.engine:
            # creating engine requires authentication to GCP
            # so, create engine only when it's needed
            self.engine = create_engine(
                "bigquery://",
            )

        with Session(self.engine) as session:
            results: list[Row] = session.execute(stmt, params).fetchall()  # type: ignore[call-overload]
            return [r._asdict() for r in results]


def validate_tz(tz: str) -> str:
    try:
        ZoneInfo(tz)
    except Exception as e:
        raise click.BadParameter(f"{tz} is not a valid timezone") from e

    return tz


@click.group()
@click.version_option()
def cli():
    "Bigquery meta data table utility"


def query_options(f):
    @click.option(
        "-p",
        "--project",
        type=str,
        help="project name",
    )
    @click.option(
        "-d",
        "--dataset",
        type=str,
        help="dataset name",
    )
    @click.option(
        "-s",
        "--select",
        type=str,
        help="commna separated column names",
    )
    @click.option(
        # order by column
        "-o",
        "--orderby",
        type=str,
        multiple=True,
        help="order by columns, if 'column_name desc' to sort descending",
    )
    @click.option(
        "--dryrun",
        is_flag=True,
        help="dry run mode, only show the rendered command",
    )
    @click.option(
        "--format",
        type=click.Choice(["json", "csv"]),
        help="output format",
        default="json",
    )
    @click.option(
        "--timezone",
        type=str,
        help="timezone",
        default="Asia/Tokyo",
    )
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


def output_result(res, format):
    if not res:
        click.echo("No data returned.", err=True)
        return

    if format == "json":
        import json

        click.echo(json.dumps(res, indent=2))
    elif format == "csv":
        import csv
        import sys

        writer = csv.DictWriter(sys.stdout, fieldnames=res[0].keys())
        writer.writeheader()
        writer.writerows(res)


def add_selects(stmt, selects):
    if selects:
        stmt = stmt.with_only_columns(
            *[stmt.selected_columns[align_column_case(c)] for c in selects],
            maintain_column_froms=True,  # this keeps derived columns in sa_select using literal_column
        )
    return stmt


def add_orderby(stmt, stmt_all, orderbys):
    for c in orderbys:
        _c = align_column_case(c)
        # get if last 4 char is 'desc' with case not sensitive
        if c[-5:].lower() == " desc":
            stmt = stmt.order_by(stmt_all.selected_columns[_c[:-4].strip()].desc())

        elif c[-4:].lower() == " asc":
            stmt = stmt.order_by(stmt_all.selected_columns[_c[:-3].strip()])
        else:
            stmt = stmt.order_by(stmt_all.selected_columns[_c])
    return stmt


def align_column_case(column_str) -> str:
    """Align column case to lower case

    Columns are case sensitive in sqlalchemy but bq's columns are.
    Use lowercase to algin bigquery's column names in their document
    """
    return column_str.lower()


@cli.command("tables")
@query_options
def tables(  # noqa: PLR0913
    project: str,
    dataset: str,
    select: str,
    orderby: list[str],
    dryrun: bool,
    format: str,
    timezone: str,
):
    """query __TABLES__"""
    runner = Runner()

    # sanitize timezone
    timezone = validate_tz(timezone)

    table = runner.get_table(project, dataset, "__TABLES__")

    columns = [
        Column("project_id", String),
        Column("dataset_id", String),
        Column("table_id", String),
        Column("creation_time", String),
        Column("last_modified_time", String),
        Column("row_count", String),
        Column("size_bytes", String),
        Column("type", String),
    ]

    for c in columns:
        table.append_column(c)

    stmt_all = sa_select(  # type: ignore[call-overload]
        table.c,
        literal_column(
            f"FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', TIMESTAMP_MILLIS(creation_time), '{timezone}')"
        ).label("creation_time_tz"),
        literal_column(
            "TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), TIMESTAMP_MILLIS(creation_time), DAY)"
        ).label("days_since_creation"),
        literal_column(
            f"FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', TIMESTAMP_MILLIS(last_modified_time), '{timezone}')"
        ).label("last_modified_time_tz"),
        literal_column(
            "TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), TIMESTAMP_MILLIS(last_modified_time), DAY)"
        ).label("days_since_last_modification"),
        literal_column("size_bytes / 1024 / 1024 / 1024").label("size_gb"),
        literal_column(
            "CASE type WHEN 1 THEN 'table' WHEN 2 THEN 'view' ELSE '' END"
        ).label("table_type"),
    )

    # select columns
    selects = select.split(",") if select else None
    stmt = add_selects(stmt_all, selects)
    # order by columns
    stmt = add_orderby(stmt, stmt_all, orderby)

    if dryrun:
        click.echo(stmt)

    else:
        res = runner.execute(stmt)

        output_result(res, format)


@cli.command("views")
@query_options
def views(  # noqa: PLR0913
    project: str,
    dataset: str,
    select: str,
    orderby: list[str],
    dryrun: bool,
    format: str,
    timezone: str,
):
    """query INFORMATION_SCHEMA.VIEWS"""

    runner = Runner()

    # auto_load=False to avoid error
    # sqlalchemy-bigquery does not allow to auto_load full table name which contains 3 parts (dots)
    # like `project.dataset.INFORMATION_SCHEMA.VIEWS`
    table = runner.get_table(project, dataset, "INFORMATION_SCHEMA.VIEWS")

    """INFORMATION_SCHEMA.VIEWS
    ref: https://cloud.google.com/bigquery/docs/information-schema-views#schema

    columns:
    TABLE_CATALOG	STRING	The name of the project that contains the dataset
    TABLE_SCHEMA	STRING	The name of the dataset that contains the view also referred to as the dataset id
    TABLE_NAME	STRING	The name of the view also referred to as the table id
    VIEW_DEFINITION	STRING	The SQL query that defines the view
    CHECK_OPTION	STRING	The value returned is always NULL
    USE_STANDARD_SQL	STRING	YES if the view was created by using a GoogleSQL query; NO if useLegacySql is set to true
    """

    columns = [
        Column("table_catalog", String),
        Column("table_schema", String),
        Column("table_name", String),
        Column("view_definition", String),
        Column("check_option", String),
        Column("use_standard_sql", String),
    ]

    for c in columns:
        table.append_column(c)

    stmt_all = sa_select(table.c)  # type: ignore[call-overload]

    # need to align upper case that is defined above
    selects = select.split(",") if select else None
    stmt = add_selects(stmt_all, selects)
    orderby = [c.upper() for c in orderby]
    stmt = add_orderby(stmt, stmt_all, orderby)

    if dryrun:
        click.echo(stmt)

    else:
        res = runner.execute(stmt)

        output_result(res, format)
