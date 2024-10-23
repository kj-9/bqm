import click

from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.dialects import registry
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import Selectable, select
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

    def select(self, stmt: Selectable) -> list[dict]:
        with Session(self.engine) as session:
            results: list[Row] = session.execute(stmt).fetchall()
            return [r._asdict() for r in results]


@click.command()
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
    type=str,
    help="output format",
    default="json",
)
def main(project: str, dataset: str, orderby: list[str], dryrun: bool, format: str):
    "bigquery meta data table utility"
    runner = Runner()

    table = runner.get_table(project, dataset, "__TABLES__")
    derived_column = text("last_modified_time AS derived_column")
    stmt = (
        select(
            # all column astarisk
            # table.c.
            table.c,
            derived_column,
        )
        # .filter(
        #    table.c.categoryID == 1,
        # )
    )
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
        res = runner.select(stmt)

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


if __name__ == "__main__":
    main()
