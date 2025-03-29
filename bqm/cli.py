from __future__ import annotations

import warnings
from functools import wraps
from zoneinfo import ZoneInfo

import click
from sqlalchemy import Column, MetaData, create_engine
from sqlalchemy.dialects import registry
from sqlalchemy.engine import Engine
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select, Selectable
from sqlalchemy.sql import select as sa_select
from sqlalchemy.sql.expression import literal_column
from trogon import tui

from bqm.schema import BIGQUERY_REGIONS, TABLES

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

    def execute(
        self, stmt: Selectable, params=None
    ) -> tuple[list[Column[str]], list[Row]]:
        """Execute query and return tuple of column descriptions and rows"""
        if not self.engine:
            # creating engine requires authentication to GCP
            # so, create engine only when it's needed
            self.engine = create_engine(
                "bigquery://",
            )

        with Session(self.engine) as session:
            res = session.execute(stmt, params)

        return res.cursor.description, res.fetchall()


def validate_tz(tz: str) -> str:
    try:
        ZoneInfo(tz)
    except Exception as e:
        raise click.BadParameter(f"{tz} is not a valid timezone") from e

    return tz


def query_options(
    select_default: str | None = None, orderby_default: tuple[str, ...] = ()
):
    def decorator(f):
        @click.option(
            "-p",
            "--project",
            type=str,
            help="project name",
            required=True,
        )
        @click.option(
            "-r",
            "--region",
            type=str,
            help="comma separated region names. if not set, query all regions.",
            default=None,
        )
        @click.option(
            "-d",
            "--dataset",
            type=str,
            help="dataset name",
            default=None,
        )
        @click.option(
            "-s",
            "--select",
            type=str,
            help="commna separated column names. set --select '' to select all columns."
            + " default columns are limited to particularly useful ones to avoid redundancy."
            if select_default
            else None,
            default=select_default,
        )
        @click.option(
            # order by column
            "-o",
            "--orderby",
            type=str,
            multiple=True,
            help="order by columns, if 'column_name desc' to sort descending"
            + f"default is '{orderby_default}'"
            if orderby_default
            else None,
            default=orderby_default,
        )
        @click.option(
            "--dryrun",
            is_flag=True,
            help="dry run mode, only show the rendered command",
        )
        @click.option(
            "--format",
            type=click.Choice(["table", "json", "csv"]),
            help="output format",
            default="table",
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

    return decorator


def output_result(columns, rows, fmt) -> None:
    if not rows:
        click.echo("No data returned.", err=True)
        return

    if fmt == "table":
        from rich.console import Console
        from rich.table import Table as RichTable

        table = RichTable()

        for c in columns:
            match c.type_code:
                case "INTEGER":
                    table.add_column(c.name, justify="right")
                case _:
                    table.add_column(c.name)

        for row in rows:
            # if numeric (int or float), format with comma
            import datetime

            parsed_row = []
            for el in row:
                match el:
                    case int() | float():
                        parsed_row.append(f"{el:,}")
                    case datetime.datetime():
                        parsed_row.append(el.isoformat())
                    case _:
                        parsed_row.append(el)

            table.add_row(*parsed_row)

        console = Console()
        console.print(table)

    if fmt == "json":
        from rich import print_json

        print_json(data=[r._asdict() for r in rows])

    elif fmt == "csv":
        import csv
        import sys

        writer = csv.DictWriter(sys.stdout, fieldnames=rows[0]._fields)
        writer.writeheader()
        writer.writerows([r._asdict() for r in rows])


def add_selects(stmt: Select, selects: list[str]) -> Select:
    if selects:
        stmt = stmt.with_only_columns(
            *[stmt.selected_columns[align_column_case(c)] for c in selects],
            maintain_column_froms=True,  # this keeps derived columns in sa_select using literal_column
        )
    return stmt


def add_orderby(stmt: Select, stmt_all: Select, orderbys) -> Select:
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


def build_stmt(stmt: Select, select: str | None, orderby: list[str] | None) -> Select:
    import copy

    # copy stmt to keep original
    stmt_all = copy.deepcopy(stmt)

    if select:
        selects = select.split(",")
        stmt = add_selects(stmt_all, selects)

    if orderby:
        orderby = [c.upper() for c in orderby]
        stmt = add_orderby(stmt, stmt_all, orderby)

    return stmt


@tui()
@click.group()
@click.version_option()
def cli():
    "Bigquery meta data table utility"


@cli.command("tables_legacy")
@query_options(
    select_default="project_id,dataset_id,table_id,row_count,size_gb,creation_time_tz,last_modified_time_tz",
    orderby_default=("project_id", "dataset_id", "table_id"),
)
def tables_legacy(  # noqa: PLR0913
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

    from bqm.schema import TABLES_LEGACY

    table = TABLES_LEGACY.get_table(runner.metadata, project, dataset=dataset)

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
        literal_column("cast(size_bytes / 1024 / 1024 / 1024 as integer)").label(
            "size_gb"
        ),
        literal_column(
            "CASE type WHEN 1 THEN 'table' WHEN 2 THEN 'view' ELSE '' END"
        ).label("table_type"),
    )

    stmt = build_stmt(stmt_all, select, orderby)

    if dryrun:
        click.echo(stmt)

    else:
        columns, rows = runner.execute(stmt)

        output_result(columns, rows, format)


def ensure_regions(region: str | None) -> set[str]:
    """Ensure regions are valid"""

    if not region:
        return BIGQUERY_REGIONS

    regions = set(region.split(","))

    invalid_regions = regions - BIGQUERY_REGIONS

    if invalid_regions:
        raise click.BadParameter(
            f"Invalid regions: {', '.join(invalid_regions)}. "
            f"Valid regions are: {', '.join(BIGQUERY_REGIONS)}"
        )

    return regions


@cli.command("tables")
@query_options()
def tables(  # noqa: PLR0913
    project: str,
    region: str | None,
    dataset: str | None,
    select: str,
    orderby: list[str],
    dryrun: bool,
    format: str,
    timezone: str,
):
    """query INFORMATION_SCHEMA.TABLES"""

    runner = Runner()

    stmts = []
    if region:
        print(region)
        regions = ensure_regions(region)
        print(regions)
        for r in regions:
            tables = TABLES.get_table(runner.metadata, project, region=r)

            stmts.append(
                build_stmt(sa_select(tables.c), select, orderby)  # type: ignore[call-overload]
            )

    else:
        tables = TABLES.get_table(runner.metadata, project, dataset=dataset)

        stmts.append(
            build_stmt(sa_select(tables.c), select, orderby)  # type: ignore[call-overload]
        )

    if dryrun:
        click.echo(stmts)
        return

    # assume stmts are cross regional so we cannot use UNION ALL in one query in BQ.
    # so, we need to run each query separately and merge the result in python

    # use asyncio and threading to run queries in parallel
    # bigquery-sqlalchemy does not support async: see: https://github.com/googleapis/python-bigquery-sqlalchemy/issues/1071
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    def run_query(stmt):
        return runner.execute(stmt)

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, run_query, stmt) for stmt in stmts]
        results = loop.run_until_complete(asyncio.gather(*tasks))

    columns = results[0][0]  # just use first one
    rows = []

    for result in results:
        rows.extend(result[1])

    output_result(columns, rows, format)


# @cli.command("views")
# @query_options()
# def views(  # noqa: PLR0913
#     project: str,
#     dataset: str,
#     select: str,
#     orderby: list[str],
#     dryrun: bool,
#     format: str,
#     timezone: str,
# ):
#     """query INFORMATION_SCHEMA.VIEWS"""

#     from bqm.schema import VIEWS

#     runner = Runner()

#     views = VIEWS.get_table(project, dataset, runner.metadata)

#     stmt = build_stmt(sa_select(views.c), select, orderby)  # type: ignore[call-overload]

#     if dryrun:
#         click.echo(stmt)
#     else:
#         columns, rows = runner.execute(stmt)
