import click
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.dialects import registry
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import Selectable
from sqlalchemy.sql import select as sgla_select
from sqlalchemy.sql.expression import text


class Runner:
    def __init__(self) -> None:
        registry.register("bigquery", "sqlalchemy_bigquery", "BigQueryDialect")
        self.engine = create_engine(
            "bigquery://",
        )
        self.metadata = MetaData()

    def get_table(self, project_name: str, dataset_name: str, table_name: str) -> Table:
        table = Table(
            f"{project_name}.{dataset_name}.{table_name}",
            self.metadata,
            autoload_with=self.engine,
        )
        return table

    def select(self, stmt: Selectable, params=None) -> list[dict]:
        with Session(self.engine) as session:
            results: list[Row] = session.execute(stmt, params).fetchall()
            return [r._asdict() for r in results]


@click.group()
@click.version_option()
def cli():
    "Bigquery meta data table utility"


@cli.command("tables")
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
def tables(  # noqa: PLR0913
    project: str,
    dataset: str,
    select: str,
    orderby: list[str],
    dryrun: bool,
    format: str,
    timezone: str,
):
    "bigquery meta data table utility"
    runner = Runner()

    table = runner.get_table(project, dataset, "__TABLES__")
    stmt = sgla_select(
        table.c,
        text(
            "FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', TIMESTAMP_MILLIS(creation_time), :timezone) as creation_time_tz"
        ),
        text(
            "TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), TIMESTAMP_MILLIS(creation_time), DAY) as days_since_creation"
        ),
        text(
            "FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', TIMESTAMP_MILLIS(last_modified_time), :timezone) as last_modified_time_tz"
        ),
        text(
            "TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), TIMESTAMP_MILLIS(last_modified_time), DAY) as days_since_last_modification"
        ),
        text("size_bytes / 1024 / 1024 / 1024 as size_gb"),
        text(
            "CASE type WHEN 1 THEN 'table' WHEN 2 THEN 'view' ELSE '' END AS table_type"
        ),
    )
    # select columns
    if select:
        selects = select.split(",")
        stmt = stmt.with_only_columns(*[table.c[c] for c in selects])

    if orderby:
        for c in orderby:
            # get if last 4 char is 'desc' with case not sensitive
            if c[-4:].lower() == "desc":
                stmt = stmt.order_by(table.c[c[:-4].strip()].desc())
            else:
                stmt = stmt.order_by(table.c[c])

    if dryrun:
        print(stmt)

    else:
        res = runner.select(stmt, {"timezone": timezone})

        # print as json
        if format == "json":
            import json

            print(json.dumps(res, indent=2))
        elif format == "csv":
            import csv
            import sys

            writer = csv.DictWriter(sys.stdout, fieldnames=res[0].keys())
            writer.writeheader()
            writer.writerows(res)
        else:
            print(res)
