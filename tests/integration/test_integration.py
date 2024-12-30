import pytest
from click.testing import CliRunner
from google.cloud import bigquery

from bqm.cli import cli


@pytest.fixture(scope="module")
def bigquery_client(project):
    client = bigquery.Client(project=project)
    yield client


@pytest.fixture(scope="module")
def dataset(bigquery_client):
    dataset_id = f"{bigquery_client.project}.bqm_test_dataset"
    dataset = bigquery.Dataset(dataset_id)
    dataset = bigquery_client.create_dataset(dataset, exists_ok=True)
    yield dataset
    bigquery_client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)


@pytest.fixture(scope="module")
def table(bigquery_client, dataset):
    table_id = f"{bigquery_client.project}.{dataset.dataset_id}.bqm_test_table"
    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("age", "INTEGER"),
    ]
    table = bigquery.Table(table_id, schema=schema)

    # Delete the table if it exists
    bigquery_client.delete_table(table_id, not_found_ok=True)

    table = bigquery_client.create_table(table)

    # NOTE:  BigQuery: Streaming insert is not allowed in the free tier
    # rows_to_insert = [
    #    {"name": "Alice", "age": 30},
    #    {"name": "Bob", "age": 25},
    # ]
    # errors = bigquery_client.insert_rows_json(table, rows_to_insert)

    yield table
    bigquery_client.delete_table(table_id, not_found_ok=True)


def test_integration(bigquery_client, table, snapshot):
    runner = CliRunner()
    result_json = runner.invoke(
        cli,
        [
            "tables",
            "--project",
            bigquery_client.project,
            "--dataset",
            table.dataset_id,
            "--format",
            "json",
        ],
    )
    assert result_json.exit_code == 0

    # parse json
    import json

    result = json.loads(result_json.output)

    assert list(result[0].keys()) == snapshot


def test_tables_dryrun(project, table, snapshot):
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                "tables",
                "--project",
                project,
                "--dataset",
                table.dataset_id,
                "--select",
                "creation_time_tz",
                "--orderby",
                "days_since_creation desc",
                "-o",
                "size_bytes asc",
                "--dryrun",
            ],
        )

        assert result.exit_code == 0  # need to mock the bq request when using auto_load
        assert result.output == snapshot
