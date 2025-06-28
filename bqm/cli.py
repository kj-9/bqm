from __future__ import annotations

import asyncio
import datetime
import itertools
import warnings
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from zoneinfo import ZoneInfo

import click
from google.cloud.bigquery import Client
from google.cloud.bigquery.schema import SchemaField
from google.cloud.bigquery.table import RowIterator
from trogon import tui

from bqm.schema import BIGQUERY_REGIONS

# Suppress the specific warning
warnings.filterwarnings(
    "ignore",
    message="Cannot create BigQuery Storage client, the dependency google-cloud-bigquery-storage is not installed.",
    category=UserWarning,
    module="google.cloud.bigquery.client",
)


class Runner:
    """Runner class to execute queries"""

    def __init__(self) -> None:
        self.client = Client()

    def execute_sync(self, query: str) -> RowIterator:
        """Execute a query synchronously and return the result."""
        query_job = self.client.query(query)  # Make an API request.

        # Wait for the job to complete.
        result = query_job.result()

        return result


def validate_tz(tz: str) -> str:
    try:
        ZoneInfo(tz)
    except Exception as e:
        raise click.BadParameter(f"{tz} is not a valid timezone") from e

    return tz


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


TABLES_DEFAULT_COLUMNS = ",".join(
    [
        "_region",
        "table_schema",
        "table_name",
        "table_type",
        "total_rows",
        "total_logical_bytes",
        "creation_time",
        "last_modified_time",
    ]
)

DATASETS_DEFAULT_COLUMNS = ",".join(
    [
        "_region",
        "schema_name",
        "location",
        "creation_time",
        "last_modified_time",
        "default_collation_name",
    ]
)


def query_options(
    select_default: tuple[str, ...] | str | None = None,
    orderby_default: tuple[str, ...] = (),
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
            "--verbose",
            is_flag=True,
            help="Show the rendered command",
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


def output_result(
    rows: list[dict], schema_fields: list[SchemaField], fmt: str, timezone: str
):
    if fmt == "table":
        from rich.console import Console
        from rich.table import Table as RichTable

        table = RichTable()

        for f in schema_fields:
            match f.field_type:
                case "INTEGER":
                    table.add_column(f.name, justify="right")
                case _:
                    table.add_column(f.name)

        for row in rows:
            parsed_row = []
            for el in row.values():
                match el:
                    # if numeric (int or float), format with comma
                    case int() | float():
                        parsed_row.append(f"{el:,}")
                    case datetime.datetime():
                        parsed_row.append(el.isoformat())
                    case _:
                        parsed_row.append(el)

            table.add_row(*parsed_row)

        console = Console()
        console.print(table)

    elif fmt == "json":
        from rich import print_json

        print_json(data=[dict(row) for row in rows], default=str)

    elif fmt == "csv":
        import csv
        import sys

        writer = csv.DictWriter(sys.stdout, fieldnames=[f.name for f in schema_fields])
        writer.writeheader()
        writer.writerows([dict(row) for row in rows])

    else:
        raise click.BadParameter(f"Unsupported format: {fmt}")


def validate_select(select: str) -> list[str]:
    if not select:
        return []
    columns = [c.strip() for c in select.split(",")]

    return columns


def validate_orderby(orderbys: list[str]) -> dict[str, str]:
    orderby = {}

    for c in orderbys:
        _c = align_case(c)
        # get if last 4 char is 'desc' with case not sensitive
        if c[-5:].lower() == " desc":
            orderby[_c[:-5].strip()] = "desc"

        elif c[-4:].lower() == " asc":
            orderby[_c[:-4].strip()] = "asc"
        else:
            orderby[_c.strip()] = "asc"

    return orderby


def align_case(column_str) -> str:
    return column_str.lower()


def get_query(project, region=None, dataset=None, columns: list[str] | None = None):
    if region and dataset:
        raise click.BadParameter("region and dataset are mutually exclusive")

    if columns:
        if dataset:
            # When querying a specific dataset, don't add _region prefix
            # Filter out _region column if it's in the list since it won't exist
            filtered_columns = [col for col in columns if col != "_region"]
            select_cols = ", ".join(filtered_columns) if filtered_columns else "*"
            select_clause = f"SELECT {select_cols}"
        else:
            # When querying by region, add _region prefix and filter it from columns
            filtered_columns = [col for col in columns if col != "_region"]
            if filtered_columns:
                select_cols = ", ".join(filtered_columns)
                select_clause = f"SELECT '{region}' AS _region, {select_cols}"
            else:
                select_clause = f"SELECT '{region}' AS _region"
    else:
        select_cols = "*"
        select_clause = (
            f"SELECT {select_cols}"
            if dataset
            else f"SELECT '{region}' AS _region, {select_cols}"
        )

    middle_part = dataset if dataset else f"region-{region}"

    return f"""
{select_clause}
FROM `{project}.{middle_part}.INFORMATION_SCHEMA.TABLES`
LEFT JOIN `{project}.{middle_part}.INFORMATION_SCHEMA.TABLE_STORAGE`
  USING(table_catalog, table_schema, table_name, creation_time, table_type)
"""


def get_datasets_query(
    project, region=None, dataset=None, columns: list[str] | None = None
):
    if region and dataset:
        raise click.BadParameter("region and dataset are mutually exclusive")

    if columns:
        if dataset:
            # When querying a specific dataset, don't add _region prefix
            # Filter out _region column if it's in the list since it won't exist
            filtered_columns = [col for col in columns if col != "_region"]
            select_cols = ", ".join(filtered_columns) if filtered_columns else "*"
            select_clause = f"SELECT {select_cols}"
        else:
            # When querying by region, add _region prefix and filter it from columns
            filtered_columns = [col for col in columns if col != "_region"]
            if filtered_columns:
                select_cols = ", ".join(filtered_columns)
                select_clause = f"SELECT '{region}' AS _region, {select_cols}"
            else:
                select_clause = f"SELECT '{region}' AS _region"
    else:
        select_cols = "*"
        select_clause = (
            f"SELECT {select_cols}"
            if dataset
            else f"SELECT '{region}' AS _region, {select_cols}"
        )

    middle_part = dataset if dataset else f"region-{region}"

    return f"""
{select_clause}
FROM `{project}.{middle_part}.INFORMATION_SCHEMA.SCHEMATA`
"""


@tui()
@click.group()
@click.version_option()
def cli():
    "Bigquery meta data table utility"


@cli.command("regions")
def regions():
    """Show all supported regions"""
    from rich.console import Console

    console = Console()
    console.print(sorted(BIGQUERY_REGIONS))


@cli.command("tables")
@query_options(select_default=TABLES_DEFAULT_COLUMNS)
def tables(  # noqa: PLR0913
    project: str,
    region: str | None,
    dataset: str | None,
    select: str,
    orderby: list[str],
    dryrun: bool,
    verbose: bool,
    format: str,
    timezone: str,
):
    """Show all tables in the project and their metadata."""

    selects = validate_select(select)

    queries = []

    if dataset:
        # if dataset is set, region is ignored
        queries.append(get_query(project, dataset=dataset, columns=selects))

    else:
        regions = ensure_regions(region)
        for r in regions:
            queries.append(get_query(project, region=r, columns=selects))

    if dryrun:
        click.echo(queries)
        return

    if verbose:
        click.echo(queries)

    # we cannot use UNION ALL to concat cross-region queries into one query.
    # so we need to run each query separately and merge the result in python
    # use asyncio and threading to run queries in parallel
    runner = Runner()

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()

        def execute_query(query):
            try:
                return runner.execute_sync(query)

            except Exception as e:
                click.echo(f"Error executing query: {query}", err=True)
                click.echo(f"Error: {e}", err=True)
                return []

        # run queries in parallel
        tasks = [
            loop.run_in_executor(executor, execute_query, query) for query in queries
        ]
        row_iters = loop.run_until_complete(asyncio.gather(*tasks))

    rows = []

    for row in itertools.chain(*row_iters):
        rows.append(dict(row))

    if not rows:
        click.echo("No data returned.", err=True)
        return

    orderbys = validate_orderby(orderby)

    for col, order in reversed(orderbys.items()):
        rows.sort(
            key=lambda r: r[col],
            reverse=(order == "desc"),
        )

    # select columns
    selects = validate_select(select)
    if selects:
        rows = [{col: row[col] for col in selects if col in row.keys()} for row in rows]

    schema_fields = row_iters[0].schema
    output_result(rows, schema_fields, format, timezone)


@cli.command("datasets")
@query_options(select_default=DATASETS_DEFAULT_COLUMNS)
def datasets(  # noqa: PLR0913
    project: str,
    region: str | None,
    dataset: str | None,
    select: str,
    orderby: list[str],
    dryrun: bool,
    verbose: bool,
    format: str,
    timezone: str,
):
    """Show all datasets in the project and their metadata."""

    selects = validate_select(select)

    queries = []

    if dataset:
        # if dataset is set, region is ignored
        queries.append(get_datasets_query(project, dataset=dataset, columns=selects))

    else:
        regions = ensure_regions(region)
        for r in regions:
            queries.append(get_datasets_query(project, region=r, columns=selects))

    if dryrun:
        click.echo(queries)
        return

    if verbose:
        click.echo(queries)

    # we cannot use UNION ALL to concat cross-region queries into one query.
    # so we need to run each query separately and merge the result in python
    # use asyncio and threading to run queries in parallel
    runner = Runner()

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()

        def execute_query(query):
            try:
                return runner.execute_sync(query)

            except Exception as e:
                click.echo(f"Error executing query: {query}", err=True)
                click.echo(f"Error: {e}", err=True)
                return []

        # run queries in parallel
        tasks = [
            loop.run_in_executor(executor, execute_query, query) for query in queries
        ]
        row_iters = loop.run_until_complete(asyncio.gather(*tasks))

    rows = []

    for row in itertools.chain(*row_iters):
        rows.append(dict(row))

    if not rows:
        click.echo("No data returned.", err=True)
        return

    orderbys = validate_orderby(orderby)

    for col, order in reversed(orderbys.items()):
        rows.sort(
            key=lambda r: r[col],
            reverse=(order == "desc"),
        )

    # select columns
    selects = validate_select(select)
    if selects:
        rows = [{col: row[col] for col in selects if col in row.keys()} for row in rows]

    schema_fields = row_iters[0].schema
    output_result(rows, schema_fields, format, timezone)
