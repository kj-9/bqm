# 🚀 Enhancement Ideas

This document outlines potential enhancements for `bqm`, categorized by area of improvement.

## New Commands & Features

*   **`bqm datasets`**: List all datasets within a project, showing metadata such as `creation_time`, `last_modified_time`, `location`, and `default_collation_name`. This can be implemented by querying `INFORMATION_SCHEMA.SCHEMATA`.
*   **`bqm views`**:  List all standard and materialized views. For standard views, show the view definition (`VIEW_DEFINITION` from `INFORMATION_SCHEMA.VIEWS`). For materialized views, include `last_refresh_time` and `refresh_watermark` from `INFORMATION_SCHEMA.MATERIALIZED_VIEWS`.
*   **`bqm routines`**:  List User-Defined Functions (UDFs) and Stored Procedures. Display `routine_type`, `routine_body`, `routine_definition`, and `external_language` from `INFORMATION_SCHEMA.ROUTINES`.
*   **`bqm jobs`**:  Provide insights into job history and performance. Query `INFORMATION_SCHEMA.JOBS_BY_PROJECT` to show `job_type`, `statement_type`, `total_bytes_billed`, `total_slot_ms`, and `error_result`.
*   **`bqm schema`**:  Export table schemas.  The `ddl` column from `INFORMATION_SCHEMA.TABLES` can be used to get the SQL DDL.  The schema can also be formatted as JSON by querying `INFORMATION_SCHEMA.COLUMNS`.
*   **`bqm costs`**: Analyze storage and query costs.
    *   Storage: Use `INFORMATION_SCHEMA.TABLE_STORAGE` to calculate costs based on `total_logical_bytes`, `active_logical_bytes`, and `long_term_logical_bytes`.
    *   Query: Aggregate `total_bytes_billed` from `INFORMATION_SCHEMA.JOBS_BY_PROJECT` to estimate query spending.

## Enhanced Functionality

*   **Configuration File**: Support a configuration file (e.g., `~/.bqm.yaml`) to store default projects, regions, and output formats, reducing the need for command-line flags.
*   **Caching**: Implement a local caching mechanism for `INFORMATION_SCHEMA` query results to speed up repeated commands.
*   **Query Templates**: Introduce a system for users to define and use their own query templates for common metadata analysis tasks.
*   **Expanded Export Formats**: In addition to the existing formats, add support for exporting to Parquet and directly to a BigQuery table.
*   **Interactive TUI**: Enhance the existing Textual TUI to be more interactive, allowing for sorting, filtering, and drilling down into results.

## Developer Experience

*   **Auto-completion**: Implement shell auto-completion for commands, options, and potentially for project/dataset/table names.
*   **Verbose Mode (`--verbose`)**: The current implementation of `--verbose` is good. We can enhance it to show the exact SQL query being executed.
*   **Progress Indicators**: For long-running, multi-region queries, display a progress bar to improve user feedback.
*   **Improved Error Handling**: Provide more specific and actionable error messages. For example, if a query fails due to permissions, suggest checking IAM roles.

## Performance & Scalability

*   **Async BigQuery Client**: The current implementation uses a `ThreadPoolExecutor` to run queries in parallel. This could be replaced with a fully asynchronous approach using `google-cloud-bigquery-storage-async` and `aiohttp` for better performance.
*   **Query Optimization**: Analyze and optimize the `INFORMATION_SCHEMA` queries for better performance, especially for projects with a large number of tables.
*   **Streaming Results**: For commands that can return a large number of rows, stream the results to avoid high memory usage.
*   **Connection Pooling**: Implement connection pooling to reuse BigQuery client connections, reducing overhead.

## Integration & Automation

*   **CI/CD Integration**:  Enable `bqm` to be used in CI/CD pipelines to generate reports on data infrastructure changes, such as schema drift or new table additions.
*   **Webhook Support**:  Allow `bqm` to trigger webhooks based on metadata changes (e.g., when a new table is created), enabling integration with other systems.
*   **Plugin Architecture**:  Develop a plugin system that allows users to create and share their own custom commands and output formatters.
*   **API Mode**:  Expose `bqm`'s functionality via an HTTP server, allowing for programmatic access from other applications.

## Quality of Life

*   **Fuzzy Search**: Implement fuzzy searching for table and dataset names to make it easier to find resources.
*   **Bookmarks**: Allow users to save and name frequently used queries or table locations.
*   **Command History**:  Implement a command history feature with the ability to search and replay previous commands.
*   **Metadata Diff**: Create a `diff` command to compare the metadata of two tables or datasets, highlighting differences in schema, options, or other properties.
