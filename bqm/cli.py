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
        "total_physical_bytes",
        "active_logical_bytes",
        "long_term_logical_bytes",
        "current_physical_bytes",
        "creation_time",
        "storage_last_modified_time",
    ]
)

TABLES_DATASET_DEFAULT_COLUMNS = ",".join(
    [
        "table_schema",
        "table_name",
        "table_type",
        "creation_time",
        "ddl",
        "default_collation_name",
    ]
)

DATASETS_DEFAULT_COLUMNS = ",".join(
    [
        "_region",
        "catalog_name",
        "schema_name",
        "location",
        "table_count",
        "creation_time",
        "last_modified_time",
        "days_old",
        "days_since_modified",
        "default_collation_name",
        "ddl",
        "schema_owner",
        "options",
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
            help="comma separated column names. set --select '' to select all columns."
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
            help="order by columns, use 'column_name desc' to sort descending. "
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


def extract_rows_parallel(row_iters: list[RowIterator]) -> list[dict]:
    """Extract rows from iterators in parallel to speed up processing"""

    def extract_rows(row_iter):
        return [dict(row) for row in row_iter]

    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        extract_tasks = [
            loop.run_in_executor(executor, extract_rows, row_iter)
            for row_iter in row_iters
            if row_iter  # Skip empty results
        ]
        row_lists = loop.run_until_complete(asyncio.gather(*extract_tasks))

    return list(itertools.chain(*row_lists))


def extract_region_from_query(query: str) -> str:
    """Extract region name from query for better error context"""
    region_match = query.find("region-")
    if region_match != -1:
        region_start = region_match + 7  # len("region-")
        region_end = query.find(".", region_start)
        return query[region_start:region_end] if region_end != -1 else "unknown"
    return "unknown"


def execute_queries_with_progress(
    queries: list[str], runner: Runner, verbose: bool = False
) -> tuple[list[RowIterator], list[dict[str, str | None]]]:
    """Execute queries in parallel with progress bar and error collection"""
    show_progress = len(queries) > 1 and not verbose
    errors = []

    if show_progress:
        from rich.progress import (
            BarColumn,
            MofNCompleteColumn,
            Progress,
            SpinnerColumn,
            TextColumn,
        )

        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,  # Hide progress bar when done
        )

        with progress:
            task = progress.add_task(
                f"Querying {len(queries)} regions...", total=len(queries)
            )

            with ThreadPoolExecutor() as executor:
                loop = asyncio.get_event_loop()

                def execute_query_with_progress(query):
                    try:
                        result = runner.execute_sync(query)
                        progress.advance(task)
                        return result
                    except Exception as e:
                        progress.advance(task)
                        region = extract_region_from_query(query)
                        error_msg = f"Error querying region '{region}': {e}"
                        errors.append(
                            {
                                "message": error_msg,
                                "query": query if verbose else None,
                            }
                        )
                        return []

                tasks = [
                    loop.run_in_executor(executor, execute_query_with_progress, query)
                    for query in queries
                ]
                row_iters = loop.run_until_complete(asyncio.gather(*tasks))
    else:
        # No progress bar for single query or verbose mode
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()

            def execute_query(query):
                try:
                    return runner.execute_sync(query)
                except Exception as e:
                    region = extract_region_from_query(query)
                    error_msg = f"Error querying region '{region}': {e}"
                    errors.append(
                        {
                            "message": error_msg,
                            "query": query if verbose else None,
                        }
                    )
                    return []

            tasks = [
                loop.run_in_executor(executor, execute_query, query)
                for query in queries
            ]
            row_iters = loop.run_until_complete(asyncio.gather(*tasks))

    return row_iters, errors


def execute_metadata_query(
    queries: list[str],
    runner: Runner,
    orderby: list[str],
    select: str,
    verbose: bool = False,
) -> tuple[list[dict], list[SchemaField]]:
    """Execute metadata queries and process results"""

    if verbose:
        click.echo(f"Executing {len(queries)} queries across regions...")
        for i, query in enumerate(queries, 1):
            click.echo(f"Query {i}/{len(queries)}:")
            click.echo(query.strip())
            click.echo()

    # Execute queries with progress tracking
    row_iters, errors = execute_queries_with_progress(queries, runner, verbose)

    # Display errors
    for error_info in errors:
        click.echo(error_info["message"], err=True)
        if error_info.get("query"):
            click.echo(f"Failed query: {error_info['query']}", err=True)

    # Extract rows in parallel
    rows = extract_rows_parallel(row_iters)

    if not rows:
        return [], []

    # Apply ordering
    orderbys = validate_orderby(orderby)
    for col, order in reversed(orderbys.items()):
        rows.sort(
            key=lambda r: r[col],
            reverse=(order == "desc"),
        )

    # Apply column selection
    selects = validate_select(select)
    if selects:
        rows = [{col: row[col] for col in selects if col in row.keys()} for row in rows]

    # Get schema from first successful result
    schema_fields: list[SchemaField] = next((ri.schema for ri in row_iters if ri), [])

    return rows, schema_fields


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

    if dataset:
        from_clause = f"`{project}.{dataset}.INFORMATION_SCHEMA.TABLES`"
        return f"""
{select_clause}
FROM {from_clause}
"""
    else:
        from_clause = f"`{project}.region-{region}.INFORMATION_SCHEMA.TABLES`"
        join_clause = f"`{project}.region-{region}.INFORMATION_SCHEMA.TABLE_STORAGE`"
        return f"""
{select_clause}
FROM {from_clause}
LEFT JOIN {join_clause}
  USING(table_catalog, table_schema, table_name, creation_time, table_type)
"""


def _build_dataset_select_clause(  # noqa: PLR0912
    columns, region, dataset, computed_columns, base_columns
):
    """Build the SELECT clause for dataset queries."""
    if columns:
        if dataset:
            # When querying a specific dataset, don't add _region prefix
            filtered_columns = [col for col in columns if col != "_region"]
            select_items = []
            for col in filtered_columns:
                if col in computed_columns:
                    select_items.append(computed_columns[col])
                elif col in base_columns:
                    select_items.append(f"{base_columns[col]} AS {col}")
                else:
                    select_items.append(f"s.{col}")
            return f"SELECT {', '.join(select_items)}" if select_items else "SELECT *"
        else:
            # When querying by region, add _region prefix
            filtered_columns = [col for col in columns if col != "_region"]
            select_items = [f"'{region}' AS _region"]
            for col in filtered_columns:
                if col in computed_columns:
                    select_items.append(computed_columns[col])
                elif col in base_columns:
                    select_items.append(f"{base_columns[col]} AS {col}")
                else:
                    select_items.append(f"s.{col}")
            return (
                f"SELECT {', '.join(select_items)}"
                if len(select_items) > 1
                else f"SELECT '{region}' AS _region"
            )
    else:
        # Select all columns with computed ones
        all_select_items = []
        if not dataset:
            all_select_items.append(f"'{region}' AS _region")

        # Add base columns
        for col, mapping in base_columns.items():
            all_select_items.append(f"{mapping} AS {col}")

        # Add computed columns
        for _col, mapping in computed_columns.items():
            all_select_items.append(mapping)

        return f"SELECT {', '.join(all_select_items)}"


def get_datasets_query(
    project, region=None, dataset=None, columns: list[str] | None = None
):
    # Note: dataset parameter is kept for compatibility but not used in query construction
    # Filtering by dataset is done after query execution

    # Define computed columns
    computed_columns = {
        "table_count": "COALESCE(tc.table_count, 0) AS table_count",
        "days_old": "DATE_DIFF(CURRENT_DATE(), DATE(s.creation_time), DAY) AS days_old",
        "days_since_modified": "DATE_DIFF(CURRENT_DATE(), DATE(s.last_modified_time), DAY) AS days_since_modified",
        "options": "opt.options AS options",
    }

    # Define column mappings (with table alias)
    base_columns = {
        "catalog_name": "s.catalog_name",
        "schema_name": "s.schema_name",
        "location": "s.location",
        "creation_time": "s.creation_time",
        "last_modified_time": "s.last_modified_time",
        "default_collation_name": "s.default_collation_name",
        "ddl": "s.ddl",
        "schema_owner": "s.schema_owner",
    }

    select_clause = _build_dataset_select_clause(
        columns,
        region,
        False,
        computed_columns,
        base_columns,  # Always pass False for dataset
    )

    # Base table and join for table counts (always use region-based query)
    schemata_table = f"`{project}.region-{region}.INFORMATION_SCHEMA.SCHEMATA`"
    tables_table = f"`{project}.region-{region}.INFORMATION_SCHEMA.TABLES`"
    options_table = f"`{project}.region-{region}.INFORMATION_SCHEMA.SCHEMATA_OPTIONS`"

    return f"""
{select_clause}
FROM {schemata_table} s
LEFT JOIN (
  SELECT
    table_schema,
    COUNT(*) as table_count
  FROM {tables_table}
  GROUP BY table_schema
) tc ON s.schema_name = tc.table_schema
LEFT JOIN (
    SELECT
        schema_name,
        TO_JSON_STRING(ARRAY_AGG(STRUCT(option_name, option_type, option_value))) AS options
    FROM {options_table}
    GROUP BY schema_name
) opt ON s.schema_name = opt.schema_name
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

    # Use different default columns when querying by dataset
    if dataset and select == TABLES_DEFAULT_COLUMNS:
        select = TABLES_DATASET_DEFAULT_COLUMNS

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
        if verbose:
            click.echo(f"Generated {len(queries)} queries:")
            for i, query in enumerate(queries, 1):
                click.echo(f"Query {i}/{len(queries)}:")
                click.echo(query.strip())
                click.echo()
        else:
            click.echo(queries)
        return

    runner = Runner()
    rows, schema_fields = execute_metadata_query(
        queries, runner, orderby, select, verbose
    )

    if not rows:
        click.echo("No data returned.", err=True)
        return

    output_result(rows, schema_fields, format, timezone)


@cli.command("datasets")
@query_options(select_default=DATASETS_DEFAULT_COLUMNS)
def datasets(  # noqa: PLR0913, PLR0912
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

    # Regular dataset query
    if dataset:
        # When querying a specific dataset, search across all regions
        regions = ensure_regions(None)  # Get all regions
        for r in regions:
            queries.append(get_datasets_query(project, region=r, columns=selects))
    else:
        regions = ensure_regions(region)
        for r in regions:
            queries.append(get_datasets_query(project, region=r, columns=selects))

    if dryrun:
        if verbose:
            click.echo(f"Generated {len(queries)} queries:")
            for i, query in enumerate(queries, 1):
                click.echo(f"Query {i}/{len(queries)}:")
                click.echo(query.strip())
                click.echo()
        else:
            click.echo(queries)
        return

    runner = Runner()
    rows, schema_fields = execute_metadata_query(
        queries, runner, orderby, select, verbose
    )

    # Filter results if a specific dataset was requested
    if dataset and rows:
        rows = [row for row in rows if row.get("schema_name") == dataset]

    if not rows:
        if dataset:
            click.echo(
                f"No datasets found in project '{project}' matching dataset '{dataset}'. Verify the dataset name and your permissions.",
                err=True,
            )
        else:
            click.echo(
                f"No datasets found in project '{project}' across {len(queries)} regions. Verify the project name and your permissions.",
                err=True,
            )
        return

    output_result(rows, schema_fields, format, timezone)
