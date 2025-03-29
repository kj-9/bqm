from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import TIMESTAMP, Column, MetaData, String, Table


@dataclass
class PreDefinedTable:
    """
    # we don't do auto_load here because:
    # 1. INFORMATION_SCHEMA.XYZ views raise error when auto_load due to current implementation of sqlalchemy-bigquery
        - full table name which contains 3 parts (dots) like `project.dataset.INFORMATION_SCHEMA.VIEWS` is not supported.
    # 2. It requires interaction to BigQuery to get metadata which makes tests harder
    """

    # project_name: str
    # dataset_name: str
    table_name: str
    columns: list[Column]

    def get_table(
        self,
        metadata: MetaData,
        project: str,
        region: str | None = None,
        dataset: str | None = None,
    ) -> Table:
        if region and dataset:
            raise ValueError("region and dataset cannot be both set")

        if not region and not dataset:
            raise ValueError("region or dataset must be set")

        table_name = self.table_name

        if region:
            table_name = f"{project}.region-{region}.{self.table_name}"
        else:
            table_name = f"{project}.{dataset}.{self.table_name}"
        t = Table(table_name, metadata)

        for c in self.columns:
            t.append_column(c)

        return t


TABLES = PreDefinedTable(
    table_name="INFORMATION_SCHEMA.TABLES",
    columns=[
        Column("table_catalog", String),
        Column("table_schema", String),
        Column("table_name", String),
        Column("table_type", String),
        Column("is_insertable_into", String),
        Column("is_typed", String),
        Column("is_change_history_enabled", String),
        Column("creation_time", TIMESTAMP),
        Column("base_table_catalog", String),
        Column("base_table_schema", String),
        Column("base_table_name", String),
        Column("snapshot_time_ms", TIMESTAMP),
        Column("replica_source_catalog", String),
        Column("replica_source_schema", String),
        Column("replica_source_name", String),
        Column("replication_status", String),
        Column("replication_error", String),
        Column("ddl", String),
        Column("default_collation_name", String),
        Column("upsert_stream_apply_watermark", TIMESTAMP),
    ],
)

TABLES_LEGACY = PreDefinedTable(
    table_name="__TABLES__",
    columns=[
        Column("project_id", String),
        Column("dataset_id", String),
        Column("table_id", String),
        Column("creation_time", String),
        Column("last_modified_time", String),
        Column("row_count", String),
        Column("size_bytes", String),
        Column("type", String),
    ],
)


VIEWS = PreDefinedTable(
    table_name="INFORMATION_SCHEMA.VIEWS",
    columns=[
        Column("table_catalog", String),
        Column("table_schema", String),
        Column("table_name", String),
        Column("view_definition", String),
        Column("check_option", String),
        Column("use_standard_sql", String),
    ],
)
