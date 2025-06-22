# BigQuery INFORMATION_SCHEMA Documentation

Source: https://cloud.google.com/bigquery/docs/information-schema-intro
Generated automatically using pure Python

# Introduction to INFORMATION_SCHEMA

The BigQuery INFORMATION_SCHEMA views are read-only, system-defined views that provide metadata information about your BigQuery objects. The following table lists all INFORMATION_SCHEMA views that you can query to retrieve metadata information:

† For *BY_PROJECT views, the BY_PROJECT suffix is optional. For example, querying INFORMATION_SCHEMA.JOBS_BY_PROJECT and INFORMATION_SCHEMA.JOBS return the same results.

For projects that use on-demand pricing, queries against INFORMATION_SCHEMA views incur a minimum of 10 MB of data processing charges, even if the bytes processed by the query are less than 10 MB. 10 MB is the minimum billing amount for on-demand queries. For more information, see On-demand pricing.

For projects that use capacity-based pricing, queries against INFORMATION_SCHEMA views and tables consume your purchased BigQuery slots. For more information, see capacity-based pricing.

Because INFORMATION_SCHEMA queries are not cached, you are charged each time that you run an INFORMATION_SCHEMA query, even if the query text is the same each time you run it.

You are not charged storage fees for the INFORMATION_SCHEMA views.

An INFORMATION_SCHEMA view needs to be qualified with a dataset or region.


## Overview Tables

### Table 1

| Resource type | INFORMATION_SCHEMA View |
| --- | --- |
| Access control | OBJECT_PRIVILEGESscience |
| BI Engine | BI_CAPACITIES BI_CAPACITY_CHANGES |
| Configurations | EFFECTIVE_PROJECT_OPTIONS ORGANIZATION_OPTIONS ORGANIZATION_OPTIONS_CHANGESscience PROJECT_OPTIONS PROJECT_OPTIONS_CHANGESscience |
| Datasets | SCHEMATA SCHEMATA_LINKS SCHEMATA_OPTIONS SHARED_DATASET_USAGE SCHEMATA_REPLICASscience SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATIONscience |
| Jobs | JOBS_BY_PROJECT† JOBS_BY_USER JOBS_BY_FOLDER JOBS_BY_ORGANIZATION |
| Jobs by timeslice | JOBS_TIMELINE_BY_PROJECT† JOBS_TIMELINE_BY_USER JOBS_TIMELINE_BY_FOLDER JOBS_TIMELINE_BY_ORGANIZATION |
| Recommendations and insights | INSIGHTSscience RECOMMENDATIONSscience RECOMMENDATIONS_BY_ORGANIZATIONscience |
| Reservations | ASSIGNMENTS_BY_PROJECT† ASSIGNMENT_CHANGES_BY_PROJECT† CAPACITY_COMMITMENTS_BY_PROJECT† CAPACITY_COMMITMENT_CHANGES_BY_PROJECT† RESERVATIONS_BY_PROJECT† RESERVATION_CHANGES_BY_PROJECT† RESERVATIONS_TIMELINE_BY_PROJECT† |
| Routines | PARAMETERS ROUTINES ROUTINE_OPTIONS |
| Search indexes | SEARCH_INDEXES SEARCH_INDEX_COLUMNS SEARCH_INDEX_COLUMN_OPTIONSscience SEARCH_INDEX_OPTIONS |
| Sessions | SESSIONS_BY_PROJECT† SESSIONS_BY_USER |
| Streaming | STREAMING_TIMELINE_BY_PROJECT† STREAMING_TIMELINE_BY_FOLDER STREAMING_TIMELINE_BY_ORGANIZATION |
| Tables | COLUMNS COLUMN_FIELD_PATHS CONSTRAINT_COLUMN_USAGE KEY_COLUMN_USAGE PARTITIONSscience TABLES TABLE_OPTIONS TABLE_CONSTRAINTS TABLE_SNAPSHOTS TABLE_STORAGE_BY_PROJECT† TABLE_STORAGE_BY_FOLDER TABLE_STORAGE_BY_ORGANIZATION TABLE_STORAGE_USAGE_TIMELINEscience TABLE_STORAGE_USAGE_TIMELINE_BY_FOLDERscience TABLE_STORAGE_USAGE_TIMELINE_BY_ORGANIZATIONscience |
| Vector indexes | VECTOR_INDEXES VECTOR_INDEX_COLUMNS VECTOR_INDEX_OPTIONS |
| Views | VIEWS MATERIALIZED_VIEWSscience |
| Write API | WRITE_API_TIMELINE_BY_PROJECT† WRITE_API_TIMELINE_BY_FOLDER WRITE_API_TIMELINE_BY_ORGANIZATION |


## Table Definitions

### ASSIGNMENTS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-assignments

**Description:** The INFORMATION_SCHEMA.ASSIGNMENTS view contains a near real-time list of all current assignments within the administration project. Each row represents a single, current assignment. A current assignment is either pending or active and has not been deleted. For more information about reservation, see Introduction to Reservations.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| ddl | STRING | The DDL statement used to create this assignment. |
| project_id | STRING | ID of the administration project. |
| project_number | INTEGER | Number of the administration project. |
| assignment_id | STRING | ID that uniquely identifies the assignment. |
| reservation_name | STRING | Name of the reservation that the assignment uses. |
| job_type | STRING | The type of job that can use the reservation. Can be PIPELINE, QUERY, CONTINUOUS, ML_EXTERNAL, or BACKGROUND. |
| assignee_id | STRING | ID that uniquely identifies the assignee resource. |
| assignee_number | INTEGER | Number that uniquely identifies the assignee resource. |
| assignee_type | STRING | Type of assignee resource. Can be organization, folder or project. |

---

### ASSIGNMENTS_CHANGES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-assignments-changes

**Description:** The INFORMATION_SCHEMA.ASSIGNMENT_CHANGES view contains a near real-time list of all changes to assignments within the administration project. Each row represents a single change to a single assignment. For more information about reservation, see Introduction to Reservations.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| change_timestamp | TIMESTAMP | Time when the change occurred. |
| project_id | STRING | ID of the administration project. |
| project_number | INTEGER | Number of the administration project. |
| assignment_id | STRING | ID that uniquely identifies the assignment. |
| reservation_name | STRING | Name of the reservation that the assignment uses. |
| job_type | STRING | The type of job that can use the reservation. Can be PIPELINE or QUERY. |
| assignee_id | STRING | ID that uniquely identifies the assignee resource. |
| assignee_number | INTEGER | Number that uniquely identifies the assignee resource. |
| assignee_type | STRING | Type of assignee resource. Can be organization, folder or project. |
| action | STRING | Type of event that occurred with the assignment. Can be CREATE, UPDATE, or DELETE. |

---

### BI_CAPACITIES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-bi-capacities

**Description:** The INFORMATION_SCHEMA.BI_CAPACITIES view contains metadata about the current state of BI Engine capacity. If you want to view the history of changes to BI Engine reservation, see the INFORMATION_SCHEMA.BI_CAPACITY_CHANGES view.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| project_id | STRING | The project ID of the project that contains BI Engine capacity. |
| project_number | INTEGER | The project number of the project that contains BI Engine capacity. |
| bi_capacity_name | STRING | The name of the object. Currently there can only be one capacity per project, hence the name is always set to default. |
| size | INTEGER | BI Engine RAM in bytes |
| preferred_tables | REPEATED STRING | Set of preferred tables this BI Engine capacity must be used for. If set to null, BI Engine capacity is used for all queries in the current project |

---

### BI_CAPACITY_CHANGES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-bi-capacity-changes

**Description:** The INFORMATION_SCHEMA.BI_CAPACITY_CHANGES view contains history of changes to the BI Engine capacity. If you want to view the current state of BI Engine reservation, see the INFORMATION_SCHEMA.BI_CAPACITIES view.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| change_timestamp | TIMESTAMP | Timestamp when the current update to BI Engine capacity was made. |
| project_id | STRING | The project ID of the project that contains BI Engine capacity. |
| project_number | INTEGER | The project number of the project that contains BI Engine capacity. |
| bi_capacity_name | STRING | The name of the object. Currently there can only be one capacity per project, hence the name is always default. |
| size | INTEGER | BI Engine RAM in bytes. |
| user_email | STRING | Email address of the user or subject of the workforce identity federation that made the change. google for changes made by Google. NULL if the email address is unknown. |
| preferred_tables | REPEATED STRING | The set of preferred tables this BI Engine capacity must be used for. If set to null, BI Engine capacity is used for all queries in the current project. |

---

### CAPACITY_COMMITMENTS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-capacity-commitments

**Description:** The INFORMATION_SCHEMA.CAPACITY_COMMITMENTS view contains a near real-time list of all current capacity commitments within the administration project. Each row represents a single, current capacity commitment. A current capacity commitment is either pending or active and has not been deleted. For more information about reservation, see Commitments.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| ddl | STRING | The DDL statement used to create this capacity commitment. |
| project_id | STRING | ID of the administration project. |
| project_number | INTEGER | Number of the administration project. |
| capacity_commitment_id | STRING | ID that uniquely identifies the capacity commitment. |
| commitment_plan | STRING | Commitment plan of the capacity commitment. |
| state | STRING | State the capacity commitment is in. Can be PENDING or ACTIVE. |
| slot_count | INTEGER | Slot count associated with the capacity commitment. |
| edition | STRING | The edition associated with this reservation. For more information about editions, see Introduction to BigQuery editions. |
| is_flat_rate | BOOL | Whether the commitment is associated with the legacy flat-rate capacity model or an edition. If FALSE, the current commitment is associated with an edition. If TRUE, the commitment is the legacy flat-rate capacity model. |
| renewal_plan | STRING | New commitment plan after the end of current commitment plan. You can change the renewal plan for a commitment at any time until it expires. |

---

### CAPACITY_COMMITMENT_CHANGES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-capacity-commitment-changes

**Description:** The INFORMATION_SCHEMA.CAPACITY_COMMITMENT_CHANGES view contains a near real-time list of all changes to capacity commitments within the administration project. Each row represents a single change to a single capacity commitment. For more information about reservation, see Commitments.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| change_timestamp | TIMESTAMP | Time when the change occurred. |
| project_id | STRING | ID of the administration project. |
| project_number | INTEGER | Number of the administration project. |
| capacity_commitment_id | STRING | ID that uniquely identifies the capacity commitment. |
| commitment_plan | STRING | Commitment plan of the capacity commitment. |
| state | STRING | State the capacity commitment is in. Can be PENDING or ACTIVE. |
| slot_count | INTEGER | Slot count associated with the capacity commitment. |
| action | STRING | Type of event that occurred with the capacity commitment. Can be CREATE, UPDATE, or DELETE. |
| commitment_end_time | TIMESTAMP | The end of the current commitment period. Only applicable for ACTIVE capacity commitments, otherwise this is NULL. |
| failure_status | RECORD | For a FAILED commitment plan, provides the failure reason, otherwise this is NULL. RECORD consists of code and message. |
| renewal_plan | STRING | The plan this capacity commitment is converted to after commitment_end_time passes. After the plan is changed, the committed period is extended according to the commitment plan. Only applicable for ANNUAL and TRIAL commitments, otherwise this is NULL. |
| edition | STRING | The edition associated with this reservation. For more information about editions, see Introduction to BigQuery editions. |
| is_flat_rate | BOOL | Whether the commitment is associated with the legacy flat-rate capacity model or an edition. If FALSE, the current commitment is associated with an edition. If TRUE, the commitment is the legacy flat-rate capacity model. |

---

### COLUMNS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-columns

**Description:** The INFORMATION_SCHEMA.COLUMNS view contains one row for each column (field) in a table.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| TABLE_CATALOG | STRING | The project ID of the project that contains the dataset |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the table also referred to as the datasetId |
| TABLE_NAME | STRING | The name of the table or view also referred to as the tableId |
| COLUMN_NAME | STRING | The name of the column |
| ORDINAL_POSITION | INT64 | The 1-indexed offset of the column within the table; if it's a pseudo column such as _PARTITIONTIME or _PARTITIONDATE, the value is NULL |
| IS_NULLABLE | STRING | YES or NO depending on whether the column's mode allows NULL values |
| DATA_TYPE | STRING | The column's GoogleSQL data type |
| IS_GENERATED | STRING | The value is always NEVER |
| GENERATION_EXPRESSION | STRING | The value is always NULL |
| IS_STORED | STRING | The value is always NULL |
| IS_HIDDEN | STRING | YES or NO depending on whether the column is a pseudo column such as _PARTITIONTIME or _PARTITIONDATE |
| IS_UPDATABLE | STRING | The value is always NULL |
| IS_SYSTEM_DEFINED | STRING | YES or NO depending on whether the column is a pseudo column such as _PARTITIONTIME or _PARTITIONDATE |
| IS_PARTITIONING_COLUMN | STRING | YES or NO depending on whether the column is a partitioning column |
| CLUSTERING_ORDINAL_POSITION | INT64 | The 1-indexed offset of the column within the table's clustering columns; the value is NULL if the table is not a clustered table |
| COLLATION_NAME | STRING | The name of the collation specification if it exists; otherwise, NULL If a STRING or ARRAY<STRING> is passed in, the collation specification is returned if it exists; otherwise NULL is returned |
| COLUMN_DEFAULT | STRING | The default value of the column if it exists; otherwise, the value is NULL |
| ROUNDING_MODE | STRING | The mode of rounding that's used for values written to the field if its type is a parameterized NUMERIC or BIGNUMERIC; otherwise, the value is NULL |

---

### COLUMN_FIELD_PATHS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-column-field-paths

**Description:** The INFORMATION_SCHEMA.COLUMN_FIELD_PATHS view contains one row for each column nested within a RECORD (or STRUCT) column.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| TABLE_CATALOG | STRING | The project ID of the project that contains the dataset |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the table also referred to as the datasetId |
| TABLE_NAME | STRING | The name of the table or view also referred to as the tableId |
| COLUMN_NAME | STRING | The name of the column |
| FIELD_PATH | STRING | The path to a column nested within a `RECORD` or `STRUCT` column |
| DATA_TYPE | STRING | The column's GoogleSQL data type |
| DESCRIPTION | STRING | The column's description |
| COLLATION_NAME | STRING | The name of the collation specification if it exists; otherwise, NULL If a STRING, ARRAY<STRING>, or STRING field in a STRUCT is passed in, the collation specification is returned if it exists; otherwise, NULL is returned |
| ROUNDING_MODE | STRING | The mode of rounding that's used when applying precision and scale to parameterized NUMERIC or BIGNUMERIC values; otherwise, the value is NULL |

---

### CONSTRAINT_COLUMN_USAGE

**Source:** https://cloud.google.com/bigquery/docs/information-schema-constraint-column-usage

**Description:** The CONSTRAINT_COLUMN_USAGE view contains all columns used by constraints. For PRIMARY KEY constraints, these are the columns from the KEY_COLUMN_USAGE view. For FOREIGN KEY constraints, these are the columns of the referenced tables.

**Schema:**

| Column Name | Data type | Value |
| --- | --- | --- |
| TABLE_CATALOG | STRING | The name of the project that contains the dataset. |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the table. Also referred to as the datasetId. |
| TABLE_NAME | STRING | The name of the table. Also referred to as the tableId. |
| COLUMN_NAME | STRING | The column name. |
| CONSTRAINT_CATALOG | STRING | The constraint project name. |
| CONSTRAINT_SCHEMA | STRING | The constraint dataset name. |
| CONSTRAINT_NAME | STRING | The constraint name. It can be the name of the primary key if the column is used by the primary key or the name of foreign key if the column is used by a foreign key. |

---

### DATASETS_SCHEMATA

**Source:** https://cloud.google.com/bigquery/docs/information-schema-datasets-schemata

**Description:** The INFORMATION_SCHEMA.SCHEMATA view provides information about the datasets in a project or region. The view returns one row for each dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| CATALOG_NAME | STRING | The name of the project that contains the dataset |
| SCHEMA_NAME | STRING | The dataset's name also referred to as the datasetId |
| SCHEMA_OWNER | STRING | The value is always NULL |
| CREATION_TIME | TIMESTAMP | The dataset's creation time |
| LAST_MODIFIED_TIME | TIMESTAMP | The dataset's last modified time |
| LOCATION | STRING | The dataset's geographic location |
| DDL | STRING | The CREATE SCHEMA DDL statement that can be used to create the dataset |
| DEFAULT_COLLATION_NAME | STRING | The name of the default collation specification if it exists; otherwise, NULL. |

---

### DATASETS_SCHEMATA_LINKS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-datasets-schemata-links

**Description:** The INFORMATION_SCHEMA.SCHEMATA_LINKS view contains one row for each linked dataset. A linked dataset links to a shared dataset in a project to which the current user has access.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| CATALOG_NAME | STRING | The name of the project that contains the source dataset. |
| SCHEMA_NAME | STRING | The name of the source dataset. The dataset name is also referred to as the datasetId. |
| LINKED_SCHEMA_CATALOG_NUMBER | STRING | The project number of the project that contains the linked dataset. |
| LINKED_SCHEMA_CATALOG_NAME | STRING | The project name of the project that contains the linked dataset. |
| LINKED_SCHEMA_NAME | STRING | The name of the linked dataset. The dataset name is also referred to as the datasetId. |
| LINKED_SCHEMA_CREATION_TIME | TIMESTAMP | The time when the linked dataset was created. |
| LINKED_SCHEMA_ORG_DISPLAY_NAME | STRING | The display name of the organization in which the linked dataset is created. |

---

### DATASETS_SCHEMATA_OPTIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-datasets-schemata-options

**Description:** The INFORMATION_SCHEMA.SCHEMATA_OPTIONS view contains one row for each option that is set in each dataset in a project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| CATALOG_NAME | STRING | The name of the project that contains the dataset |
| SCHEMA_NAME | STRING | The name of the dataset, also referred to as the datasetId |
| OPTION_NAME | STRING | The name of the option. For a list of supported options, see the schema options list. The storage_billing_model option is only displayed for datasets that have been updated after December 1, 2022. For datasets that were last updated before that date, the storage billing model is LOGICAL. |
| OPTION_TYPE | STRING | The data type of the option |
| OPTION_VALUE | STRING | The value of the option |

---

### EFFECTIVE_PROJECT_OPTIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-effective-project-options

**Description:** You can query the INFORMATION_SCHEMA.EFFECTIVE_PROJECT_OPTIONS view to retrieve real-time metadata about BigQuery effective project options. This view contains default settings at the organization or project levels.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| OPTION_NAME | STRING | Option ID for the specified configuration setting. |
| OPTION_DESCRIPTION | STRING | The option description. |
| OPTION_TYPE | STRING | The data type of the OPTION_VALUE. |
| OPTION_SET_LEVEL | STRING | The level in the hierarchy at which the setting is defined, with possible values of DEFAULT, ORGANIZATION, or PROJECTS. |
| OPTION_SET_ON_ID | STRING | Set value based on value of OPTION_SET_LEVEL: If DEFAULT, set to null. If ORGANIZATION, set to "". If PROJECT, set to ID. |

---

### INDEXES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-indexes

**Description:** The INFORMATION_SCHEMA.SEARCH_INDEXES view contains one row for each search index in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| index_catalog | STRING | The name of the project that contains the dataset. |
| index_schema | STRING | The name of the dataset that contains the index. |
| table_name | STRING | The name of the base table that the index is created on. |
| index_name | STRING | The name of the index. |
| index_status | STRING | The status of the index: ACTIVE, PENDING DISABLEMENT, TEMPORARILY DISABLED, or PERMANENTLY DISABLED. ACTIVE means that the index is usable or being created. Refer to the coverage_percentage to see the progress of index creation. PENDING DISABLEMENT means that the total size of indexed base tables exceeds your organization's limit; the index is queued for deletion. While in this state, the index is usable in search queries and you are charged for the search index storage. TEMPORARILY DISABLED means that either the total size of indexed base tables exceeds your organization's limit, or the base indexed table is smaller than 10GB. While in this state, the index is not used in search queries and you are not charged for the search index storage. PERMANENTLY DISABLED means that there is an incompatible schema change on the base table, such as changing the type of an indexed column from STRING to INT64. |
| creation_time | TIMESTAMP | The time the index was created. |
| last_modification_time | TIMESTAMP | The last time the index configuration was modified. For example, deleting an indexed column. |
| last_refresh_time | TIMESTAMP | The last time the table data was indexed. A NULL value means the index is not yet available. |
| disable_time | TIMESTAMP | The time the status of the index was set to DISABLED. The value is NULL if the index status is not DISABLED. |
| disable_reason | STRING | The reason the index was disabled. NULL if the index status is not DISABLED. |
| DDL | STRING | The DDL statement used to create the index. |
| coverage_percentage | INTEGER | The approximate percentage of table data that has been indexed. 0% means the index is not usable in a SEARCH query, even if some data has already been indexed. |
| unindexed_row_count | INTEGER | The number of rows in the base table that have not been indexed. |
| total_logical_bytes | INTEGER | The number of billable logical bytes for the index. |
| total_storage_bytes | INTEGER | The number of billable storage bytes for the index. |
| analyzer | STRING | The text analyzer to use to generate tokens for the search index. |

---

### INDEXES#SCOPE_AND_SYNTAX

**Source:** https://cloud.google.com/bigquery/docs/information-schema-indexes#scope_and_syntax

**Description:** The INFORMATION_SCHEMA.SEARCH_INDEXES view contains one row for each search index in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| index_catalog | STRING | The name of the project that contains the dataset. |
| index_schema | STRING | The name of the dataset that contains the index. |
| table_name | STRING | The name of the base table that the index is created on. |
| index_name | STRING | The name of the index. |
| index_status | STRING | The status of the index: ACTIVE, PENDING DISABLEMENT, TEMPORARILY DISABLED, or PERMANENTLY DISABLED. ACTIVE means that the index is usable or being created. Refer to the coverage_percentage to see the progress of index creation. PENDING DISABLEMENT means that the total size of indexed base tables exceeds your organization's limit; the index is queued for deletion. While in this state, the index is usable in search queries and you are charged for the search index storage. TEMPORARILY DISABLED means that either the total size of indexed base tables exceeds your organization's limit, or the base indexed table is smaller than 10GB. While in this state, the index is not used in search queries and you are not charged for the search index storage. PERMANENTLY DISABLED means that there is an incompatible schema change on the base table, such as changing the type of an indexed column from STRING to INT64. |
| creation_time | TIMESTAMP | The time the index was created. |
| last_modification_time | TIMESTAMP | The last time the index configuration was modified. For example, deleting an indexed column. |
| last_refresh_time | TIMESTAMP | The last time the table data was indexed. A NULL value means the index is not yet available. |
| disable_time | TIMESTAMP | The time the status of the index was set to DISABLED. The value is NULL if the index status is not DISABLED. |
| disable_reason | STRING | The reason the index was disabled. NULL if the index status is not DISABLED. |
| DDL | STRING | The DDL statement used to create the index. |
| coverage_percentage | INTEGER | The approximate percentage of table data that has been indexed. 0% means the index is not usable in a SEARCH query, even if some data has already been indexed. |
| unindexed_row_count | INTEGER | The number of rows in the base table that have not been indexed. |
| total_logical_bytes | INTEGER | The number of billable logical bytes for the index. |
| total_storage_bytes | INTEGER | The number of billable storage bytes for the index. |
| analyzer | STRING | The text analyzer to use to generate tokens for the search index. |

---

### INDEX_COLUMNS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-index-columns

**Description:** The INFORMATION_SCHEMA.SEARCH_INDEX_COLUMNS view contains one row for each search-indexed column on each table in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| index_catalog | STRING | The name of the project that contains the dataset. |
| index_schema | STRING | The name of the dataset that contains the index. |
| table_name | STRING | The name of the base table that the index is created on. |
| index_name | STRING | The name of the index. |
| index_field_path | STRING | The full path of the expanded indexed field, starting with the column name. Fields are separated by a period. |

---

### INDEX_COLUMN_OPTIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-index-column-options

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| index_catalog | STRING | The name of the project that contains the dataset. |
| index_schema | STRING | The name of the dataset that contains the index. |
| table_name | STRING | The name of the base table that the index is created on. |
| index_name | STRING | The name of the index. |
| column_name | STRING | The name of the indexed column that the option is set on. |
| option_name | STRING | The name of the option specified on the column. |
| option_type | STRING | The type of the option. |
| option_value | STRING | The value of the option. |

---

### INDEX_OPTIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-index-options

**Description:** The INFORMATION_SCHEMA.SEARCH_INDEX_OPTIONS view contains one row for each search index option in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| index_catalog | STRING | The name of the project that contains the dataset. |
| index_schema | STRING | The name of the dataset that contains the index. |
| table_name | STRING | The name of the base table that the index is created on. |
| index_name | STRING | The name of the index. |
| option_name | STRING | The name of the option, which can be one of the following: analyzer, analyzer_options, data_types, or default_index_column_granularity. |
| option_type | STRING | The type of the option. |
| option_value | STRING | The value of the option. |

---

### INSIGHTS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-insights

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| insight_id | STRING | Base64 encoded ID that contains the insight type and insight ID |
| insight_type | STRING | The type of the Insight. For example, google.bigquery.materializedview.Insight. |
| subtype | STRING | The subtype of the insight. |
| project_id | STRING | The ID of the project. |
| project_number | STRING | The number of the project. |
| description | STRING | The description about the recommendation. |
| last_updated_time | TIMESTAMP | This field represents the time when the insight was last refreshed. |
| category | STRING | The optimization category of the impact. |
| target_resources | STRING | Fully qualified resource names this insight is targeting. |
| state | STRING | The state of the insight. For a list of possible values, see Value. |
| severity | STRING | The severity of the Insight. For a list of possible values, see Severity. |
| associated_recommendation_ids | STRING | Full recommendation names this insight is associated with. Recommendation name is the Base64 encoded representation of recommender type and the recommendations ID. |
| additional_details | RECORD | Additional details about the insight. content: Insight content in JSON format. state_metadata: Metadata about the state of the Insight. Contains key-value pairs. observation_period_seconds: Observation Period for generating the insight. |

---

### INTRO

**Source:** https://cloud.google.com/bigquery/docs/information-schema-intro

**Description:** The BigQuery INFORMATION_SCHEMA views are read-only, system-defined views that provide metadata information about your BigQuery objects. The following table lists all INFORMATION_SCHEMA views that you can query to retrieve metadata information:

---

### JOBS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-jobs

**Description:** The INFORMATION_SCHEMA.JOBS view contains near real-time metadata about all BigQuery jobs in the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| bi_engine_statistics | RECORD | If the project is configured to use the BI Engine, then this field contains BiEngineStatistics. Otherwise NULL. |
| cache_hit | BOOLEAN | Whether the query results of this job were from a cache. If you have a multi-query statement job, cache_hit for your parent query is NULL. |
| creation_time | TIMESTAMP | (Partitioning column) Creation time of this job. Partitioning is based on the UTC time of this timestamp. |
| destination_table | RECORD | Destination table for results, if any. |
| end_time | TIMESTAMP | The end time of this job, in milliseconds since the epoch. This field represents the time when the job enters the DONE state. |
| error_result | RECORD | Details of any errors as ErrorProto objects. |
| job_creation_reason.code | STRING | Specifies the high level reason why a job was created. Possible values are: REQUESTED: job creation was requested. LONG_RUNNING: the query request ran beyond a system defined timeout specified by the timeoutMs field in the QueryRequest. As a result it was considered a long running operation for which a job was created. LARGE_RESULTS: the results from the query cannot fit in the in-line response. OTHER: the system has determined that the query needs to be executed as a job. |
| job_id | STRING | The ID of the job if a job was created. Otherwise, the query ID of a query using optional job creation mode. For example, bquxjob_1234. |
| job_stages | RECORD | Query stages of the job. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| job_type | STRING | The type of the job. Can be QUERY, LOAD, EXTRACT, COPY, or NULL. A NULL value indicates an internal job, such as a script job statement evaluation. |
| labels | RECORD | Array of labels applied to the job as key-value pairs. |
| parent_job_id | STRING | ID of the parent job, if any. |
| priority | STRING | The priority of this job. Valid values include INTERACTIVE and BATCH. |
| project_id | STRING | (Clustering column) The ID of the project. |
| project_number | INTEGER | The number of the project. |
| query | STRING | SQL query text. Only the JOBS_BY_PROJECT view has the query column. |
| referenced_tables | RECORD | Array of tables referenced by the job. Only populated for query jobs that are not cache hits. |
| reservation_id | STRING | Name of the primary reservation assigned to this job, in the format RESERVATION_ADMIN_PROJECT:RESERVATION_LOCATION.RESERVATION_NAME. In this output: RESERVATION_ADMIN_PROJECT: the name of the Google Cloud project that administers the reservation RESERVATION_LOCATION: the location of the reservation RESERVATION_NAME: the name of the reservation |
| edition | STRING | The edition associated with the reservation assigned to this job. For more information about editions, see Introduction to BigQuery editions. |
| session_info | RECORD | Details about the session in which this job ran, if any. |
| start_time | TIMESTAMP | The start time of this job, in milliseconds since the epoch. This field represents the time when the job transitions from the PENDING state to either RUNNING or DONE. |
| state | STRING | Running state of the job. Valid states include PENDING, RUNNING, and DONE. |
| statement_type | STRING | The type of query statement. For example, DELETE, INSERT, SCRIPT, SELECT, or UPDATE. See QueryStatementType for list of valid values. |
| timeline | RECORD | Query timeline of the job. Contains snapshots of query execution. |
| total_bytes_billed | INTEGER | If the project is configured to use on-demand pricing, then this field contains the total bytes billed for the job. If the project is configured to use flat-rate pricing, then you are not billed for bytes and this field is informational only. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| total_bytes_processed | INTEGER | Total bytes processed by the job. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| total_modified_partitions | INTEGER | The total number of partitions the job modified. This field is populated for LOAD and QUERY jobs. |
| total_slot_ms | INTEGER | Slot milliseconds for the job over its entire duration in the RUNNING state, including retries. |
| transaction_id | STRING | ID of the transaction in which this job ran, if any. (Preview) |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the job. |
| query_info.resource_warning | STRING | The warning message that appears if the resource usage during query processing is above the internal threshold of the system. A successful query job can have the resource_warning field populated. With resource_warning, you get additional data points to optimize your queries and to set up monitoring for performance trends of an equivalent set of queries by using query_hashes. |
| query_info.query_hashes.normalized_literals | STRING | Contains the hashes of the query. normalized_literals is a hexadecimal STRING hash that ignores comments, parameter values, UDFs, and literals. The hash value will differ when underlying views change, or if the query implicitly references columns, such as SELECT *, and the table schema changes. This field appears for successful GoogleSQL queries that are not cache hits. |
| query_info.performance_insights | RECORD | Performance insights for the job. |
| query_info.optimization_details | STRUCT | The history-based optimizations for the job. |
| transferred_bytes | INTEGER | Total bytes transferred for cross-cloud queries, such as BigQuery Omni cross-cloud transfer jobs. |
| materialized_view_statistics | RECORD | Statistics of materialized views considered in a query job. (Preview) |
| metadata_cache_statistics | RECORD | Statistics for metadata column index usage for tables referenced in a query job. |
| search_statistics | RECORD | Statistics for a search query. |
| query_dialect | STRING | This field will be available sometime in May, 2025. The query dialect used for the job. Valid values include: GOOGLE_SQL: Job was requested to use GoogleSQL. LEGACY_SQL: Job was requested to use LegacySQL. DEFAULT_LEGACY_SQL: No query dialect was specified in the job request. BigQuery used the default value of LegacySQL. DEFAULT_GOOGLE_SQL: No query dialect was specified in the job request. BigQuery used the default value of GoogleSQL. This field is only populated for query jobs. The default selection of query dialect can be controlled by the configuration settings. |
| continuous | BOOLEAN | Whether the job is a continuous query. |
| continuous_query_info.output_watermark | TIMESTAMP | Represents the point up to which the continuous query has successfully processed data. |
| vector_search_statistics | RECORD | Statistics for a vector search query. |

---

### JOBS_BY_FOLDER

**Source:** https://cloud.google.com/bigquery/docs/information-schema-jobs-by-folder

**Description:** The INFORMATION_SCHEMA.JOBS_BY_FOLDER view contains near real-time metadata about all jobs submitted in the parent folder of the current project, including the jobs in subfolders under it.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| bi_engine_statistics | RECORD | If the project is configured to use the BI Engine, then this field contains BiEngineStatistics. Otherwise NULL. |
| cache_hit | BOOLEAN | Whether the query results of this job were from a cache. If you have a multi-query statement job, cache_hit for your parent query is NULL. |
| creation_time | TIMESTAMP | (Partitioning column) Creation time of this job. Partitioning is based on the UTC time of this timestamp. |
| destination_table | RECORD | Destination table for results, if any. |
| end_time | TIMESTAMP | The end time of this job, in milliseconds since the epoch. This field represents the time when the job enters the DONE state. |
| error_result | RECORD | Details of any errors as ErrorProto objects. |
| folder_numbers | REPEATED INTEGER | Number IDs of folders that contain the project, starting with the folder that immediately contains the project, followed by the folder that contains the child folder, and so forth. For example, if folder_numbers is [1, 2, 3], then folder 1 immediately contains the project, folder 2 contains 1, and folder 3 contains 2. This column is only populated in JOBS_BY_FOLDER. |
| job_creation_reason.code | STRING | Specifies the high level reason why a job was created. Possible values are: REQUESTED: job creation was requested. LONG_RUNNING: the query request ran beyond a system defined timeout specified by the timeoutMs field in the QueryRequest. As a result it was considered a long running operation for which a job was created. LARGE_RESULTS: the results from the query cannot fit in the in-line response. OTHER: the system has determined that the query needs to be executed as a job. |
| job_id | STRING | The ID of the job if a job was created. Otherwise, the query ID of a query using optional job creation mode. For example, bquxjob_1234. |
| job_stages | RECORD | Query stages of the job. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| job_type | STRING | The type of the job. Can be QUERY, LOAD, EXTRACT, COPY, or NULL. A NULL value indicates an internal job, such as a script job statement evaluation. |
| labels | RECORD | Array of labels applied to the job as key-value pairs. |
| parent_job_id | STRING | ID of the parent job, if any. |
| priority | STRING | The priority of this job. Valid values include INTERACTIVE and BATCH. |
| project_id | STRING | (Clustering column) The ID of the project. |
| project_number | INTEGER | The number of the project. |
| query | STRING | SQL query text. Only the JOBS_BY_PROJECT view has the query column. |
| referenced_tables | RECORD | Array of tables referenced by the job. Only populated for query jobs that are not cache hits. |
| reservation_id | STRING | Name of the primary reservation assigned to this job, in the format RESERVATION_ADMIN_PROJECT:RESERVATION_LOCATION.RESERVATION_NAME. In this output: RESERVATION_ADMIN_PROJECT: the name of the Google Cloud project that administers the reservation RESERVATION_LOCATION: the location of the reservation RESERVATION_NAME: the name of the reservation |
| edition | STRING | The edition associated with the reservation assigned to this job. For more information about editions, see Introduction to BigQuery editions. |
| session_info | RECORD | Details about the session in which this job ran, if any. |
| start_time | TIMESTAMP | The start time of this job, in milliseconds since the epoch. This field represents the time when the job transitions from the PENDING state to either RUNNING or DONE. |
| state | STRING | Running state of the job. Valid states include PENDING, RUNNING, and DONE. |
| statement_type | STRING | The type of query statement. For example, DELETE, INSERT, SCRIPT, SELECT, or UPDATE. See QueryStatementType for list of valid values. |
| timeline | RECORD | Query timeline of the job. Contains snapshots of query execution. |
| total_bytes_billed | INTEGER | If the project is configured to use on-demand pricing, then this field contains the total bytes billed for the job. If the project is configured to use flat-rate pricing, then you are not billed for bytes and this field is informational only. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| total_bytes_processed | INTEGER | Total bytes processed by the job. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| total_modified_partitions | INTEGER | The total number of partitions the job modified. This field is populated for LOAD and QUERY jobs. |
| total_slot_ms | INTEGER | Slot milliseconds for the job over its entire duration in the RUNNING state, including retries. |
| transaction_id | STRING | ID of the transaction in which this job ran, if any. (Preview) |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the job. |
| query_info.resource_warning | STRING | The warning message that appears if the resource usage during query processing is above the internal threshold of the system. A successful query job can have the resource_warning field populated. With resource_warning, you get additional data points to optimize your queries and to set up monitoring for performance trends of an equivalent set of queries by using query_hashes. |
| query_info.query_hashes.normalized_literals | STRING | Contains the hashes of the query. normalized_literals is a hexadecimal STRING hash that ignores comments, parameter values, UDFs, and literals. The hash value will differ when underlying views change, or if the query implicitly references columns, such as SELECT *, and the table schema changes. This field appears for successful GoogleSQL queries that are not cache hits. |
| query_info.performance_insights | RECORD | Performance insights for the job. |
| query_info.optimization_details | STRUCT | The history-based optimizations for the job. |
| transferred_bytes | INTEGER | Total bytes transferred for cross-cloud queries, such as BigQuery Omni cross-cloud transfer jobs. |
| materialized_view_statistics | RECORD | Statistics of materialized views considered in a query job. (Preview) |
| metadata_cache_statistics | RECORD | Statistics for metadata column index usage for tables referenced in a query job. |
| search_statistics | RECORD | Statistics for a search query. |
| query_dialect | STRING | This field will be available sometime in May, 2025. The query dialect used for the job. Valid values include: GOOGLE_SQL: Job was requested to use GoogleSQL. LEGACY_SQL: Job was requested to use LegacySQL. DEFAULT_LEGACY_SQL: No query dialect was specified in the job request. BigQuery used the default value of LegacySQL. DEFAULT_GOOGLE_SQL: No query dialect was specified in the job request. BigQuery used the default value of GoogleSQL. This field is only populated for query jobs. The default selection of query dialect can be controlled by the configuration settings. |
| continuous | BOOLEAN | Whether the job is a continuous query. |
| continuous_query_info.output_watermark | TIMESTAMP | Represents the point up to which the continuous query has successfully processed data. |
| vector_search_statistics | RECORD | Statistics for a vector search query. |

---

### JOBS_BY_ORGANIZATION

**Source:** https://cloud.google.com/bigquery/docs/information-schema-jobs-by-organization

**Description:** The INFORMATION_SCHEMA.JOBS_BY_ORGANIZATION view contains near real-time metadata about all jobs submitted in the organization that is associated with the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| bi_engine_statistics | RECORD | If the project is configured to use the BI Engine, then this field contains BiEngineStatistics. Otherwise NULL. |
| cache_hit | BOOLEAN | Whether the query results of this job were from a cache. If you have a multi-query statement job, cache_hit for your parent query is NULL. |
| creation_time | TIMESTAMP | (Partitioning column) Creation time of this job. Partitioning is based on the UTC time of this timestamp. |
| destination_table | RECORD | Destination table for results, if any. |
| end_time | TIMESTAMP | The end time of this job, in milliseconds since the epoch. This field represents the time when the job enters the DONE state. |
| error_result | RECORD | Details of any errors as ErrorProto objects. |
| folder_numbers | REPEATED INTEGER | Number IDs of folders that contain the project, starting with the folder that immediately contains the project, followed by the folder that contains the child folder, and so forth. For example, if folder_numbers is [1, 2, 3], then folder 1 immediately contains the project, folder 2 contains 1, and folder 3 contains 2. This column is only populated in JOBS_BY_FOLDER. |
| job_creation_reason.code | STRING | Specifies the high level reason why a job was created. Possible values are: REQUESTED: job creation was requested. LONG_RUNNING: the query request ran beyond a system defined timeout specified by the timeoutMs field in the QueryRequest. As a result it was considered a long running operation for which a job was created. LARGE_RESULTS: the results from the query cannot fit in the in-line response. OTHER: the system has determined that the query needs to be executed as a job. |
| job_id | STRING | The ID of the job if a job was created. Otherwise, the query ID of a query using optional job creation mode. For example, bquxjob_1234. |
| job_stages | RECORD | Query stages of the job. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| job_type | STRING | The type of the job. Can be QUERY, LOAD, EXTRACT, COPY, or NULL. A NULL value indicates an internal job, such as a script job statement evaluation. |
| labels | RECORD | Array of labels applied to the job as key-value pairs. |
| parent_job_id | STRING | ID of the parent job, if any. |
| priority | STRING | The priority of this job. Valid values include INTERACTIVE and BATCH. |
| project_id | STRING | (Clustering column) The ID of the project. |
| project_number | INTEGER | The number of the project. |
| query | STRING | SQL query text. Only the JOBS_BY_PROJECT view has the query column. |
| referenced_tables | RECORD | Array of tables referenced by the job. Only populated for query jobs that are not cache hits. |
| reservation_id | STRING | Name of the primary reservation assigned to this job, in the format RESERVATION_ADMIN_PROJECT:RESERVATION_LOCATION.RESERVATION_NAME. In this output: RESERVATION_ADMIN_PROJECT: the name of the Google Cloud project that administers the reservation RESERVATION_LOCATION: the location of the reservation RESERVATION_NAME: the name of the reservation |
| edition | STRING | The edition associated with the reservation assigned to this job. For more information about editions, see Introduction to BigQuery editions. |
| session_info | RECORD | Details about the session in which this job ran, if any. |
| start_time | TIMESTAMP | The start time of this job, in milliseconds since the epoch. This field represents the time when the job transitions from the PENDING state to either RUNNING or DONE. |
| state | STRING | Running state of the job. Valid states include PENDING, RUNNING, and DONE. |
| statement_type | STRING | The type of query statement. For example, DELETE, INSERT, SCRIPT, SELECT, or UPDATE. See QueryStatementType for list of valid values. |
| timeline | RECORD | Query timeline of the job. Contains snapshots of query execution. |
| total_bytes_billed | INTEGER | If the project is configured to use on-demand pricing, then this field contains the total bytes billed for the job. If the project is configured to use flat-rate pricing, then you are not billed for bytes and this field is informational only. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| total_bytes_processed | INTEGER | Total bytes processed by the job. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| total_modified_partitions | INTEGER | The total number of partitions the job modified. This field is populated for LOAD and QUERY jobs. |
| total_slot_ms | INTEGER | Slot milliseconds for the job over its entire duration in the RUNNING state, including retries. |
| transaction_id | STRING | ID of the transaction in which this job ran, if any. (Preview) |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the job. |
| query_info.resource_warning | STRING | The warning message that appears if the resource usage during query processing is above the internal threshold of the system. A successful query job can have the resource_warning field populated. With resource_warning, you get additional data points to optimize your queries and to set up monitoring for performance trends of an equivalent set of queries by using query_hashes. |
| query_info.query_hashes.normalized_literals | STRING | Contains the hashes of the query. normalized_literals is a hexadecimal STRING hash that ignores comments, parameter values, UDFs, and literals. The hash value will differ when underlying views change, or if the query implicitly references columns, such as SELECT *, and the table schema changes. This field appears for successful GoogleSQL queries that are not cache hits. |
| query_info.performance_insights | RECORD | Performance insights for the job. |
| query_info.optimization_details | STRUCT | The history-based optimizations for the job. |
| transferred_bytes | INTEGER | Total bytes transferred for cross-cloud queries, such as BigQuery Omni cross-cloud transfer jobs. |
| materialized_view_statistics | RECORD | Statistics of materialized views considered in a query job. (Preview) |
| metadata_cache_statistics | RECORD | Statistics for metadata column index usage for tables referenced in a query job. |
| search_statistics | RECORD | Statistics for a search query. |
| query_dialect | STRING | This field will be available sometime in May, 2025. The query dialect used for the job. Valid values include: GOOGLE_SQL: Job was requested to use GoogleSQL. LEGACY_SQL: Job was requested to use LegacySQL. DEFAULT_LEGACY_SQL: No query dialect was specified in the job request. BigQuery used the default value of LegacySQL. DEFAULT_GOOGLE_SQL: No query dialect was specified in the job request. BigQuery used the default value of GoogleSQL. This field is only populated for query jobs. The default selection of query dialect can be controlled by the configuration settings. |
| continuous | BOOLEAN | Whether the job is a continuous query. |
| continuous_query_info.output_watermark | TIMESTAMP | Represents the point up to which the continuous query has successfully processed data. |
| vector_search_statistics | RECORD | Statistics for a vector search query. |

---

### JOBS_BY_USER

**Source:** https://cloud.google.com/bigquery/docs/information-schema-jobs-by-user

**Description:** The INFORMATION_SCHEMA.JOBS_BY_USER view contains near real-time metadata about the BigQuery jobs submitted by the current user in the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| bi_engine_statistics | RECORD | If the project is configured to use the BI Engine, then this field contains BiEngineStatistics. Otherwise NULL. |
| cache_hit | BOOLEAN | Whether the query results of this job were from a cache. If you have a multi-query statement job, cache_hit for your parent query is NULL. |
| creation_time | TIMESTAMP | (Partitioning column) Creation time of this job. Partitioning is based on the UTC time of this timestamp. |
| destination_table | RECORD | Destination table for results, if any. |
| dml_statistics | RECORD | If the job is a query with a DML statement, the value is a record with the following fields: inserted_row_count: The number of rows that were inserted. deleted_row_count: The number of rows that were deleted. updated_row_count: The number of rows that were updated. For all other jobs, the value is NULL. This column is present in the INFORMATION_SCHEMA.JOBS_BY_USER and INFORMATION_SCHEMA.JOBS_BY_PROJECT views. |
| end_time | TIMESTAMP | The end time of this job, in milliseconds since the epoch. This field represents the time when the job enters the DONE state. |
| error_result | RECORD | Details of any errors as ErrorProto objects. |
| job_creation_reason.code | STRING | Specifies the high level reason why a job was created. Possible values are: REQUESTED: job creation was requested. LONG_RUNNING: the query request ran beyond a system defined timeout specified by the timeoutMs field in the QueryRequest. As a result it was considered a long running operation for which a job was created. LARGE_RESULTS: the results from the query cannot fit in the in-line response. OTHER: the system has determined that the query needs to be executed as a job. |
| job_id | STRING | The ID of the job if a job was created. Otherwise, the query ID of a query using optional job creation mode. For example, bquxjob_1234. |
| job_stages | RECORD | Query stages of the job. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| job_type | STRING | The type of the job. Can be QUERY, LOAD, EXTRACT, COPY, or NULL. A NULL value indicates an internal job, such as a script job statement evaluation. |
| labels | RECORD | Array of labels applied to the job as key-value pairs. |
| parent_job_id | STRING | ID of the parent job, if any. |
| priority | STRING | The priority of this job. Valid values include INTERACTIVE and BATCH. |
| project_id | STRING | (Clustering column) The ID of the project. |
| project_number | INTEGER | The number of the project. |
| query | STRING | SQL query text. Only the JOBS_BY_PROJECT view has the query column. |
| referenced_tables | RECORD | Array of tables referenced by the job. Only populated for query jobs that are not cache hits. |
| reservation_id | STRING | Name of the primary reservation assigned to this job, in the format RESERVATION_ADMIN_PROJECT:RESERVATION_LOCATION.RESERVATION_NAME. In this output: RESERVATION_ADMIN_PROJECT: the name of the Google Cloud project that administers the reservation RESERVATION_LOCATION: the location of the reservation RESERVATION_NAME: the name of the reservation |
| edition | STRING | The edition associated with the reservation assigned to this job. For more information about editions, see Introduction to BigQuery editions. |
| session_info | RECORD | Details about the session in which this job ran, if any. |
| start_time | TIMESTAMP | The start time of this job, in milliseconds since the epoch. This field represents the time when the job transitions from the PENDING state to either RUNNING or DONE. |
| state | STRING | Running state of the job. Valid states include PENDING, RUNNING, and DONE. |
| statement_type | STRING | The type of query statement. For example, DELETE, INSERT, SCRIPT, SELECT, or UPDATE. See QueryStatementType for list of valid values. |
| timeline | RECORD | Query timeline of the job. Contains snapshots of query execution. |
| total_bytes_billed | INTEGER | If the project is configured to use on-demand pricing, then this field contains the total bytes billed for the job. If the project is configured to use flat-rate pricing, then you are not billed for bytes and this field is informational only. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| total_bytes_processed | INTEGER | Total bytes processed by the job. Note: This column's values are empty for queries that read from tables with row-level access policies. For more information, see best practices for row-level security in BigQuery. |
| total_modified_partitions | INTEGER | The total number of partitions the job modified. This field is populated for LOAD and QUERY jobs. |
| total_slot_ms | INTEGER | Slot milliseconds for the job over its entire duration in the RUNNING state, including retries. |
| transaction_id | STRING | ID of the transaction in which this job ran, if any. (Preview) |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the job. |
| query_info.resource_warning | STRING | The warning message that appears if the resource usage during query processing is above the internal threshold of the system. A successful query job can have the resource_warning field populated. With resource_warning, you get additional data points to optimize your queries and to set up monitoring for performance trends of an equivalent set of queries by using query_hashes. |
| query_info.query_hashes.normalized_literals | STRING | Contains the hashes of the query. normalized_literals is a hexadecimal STRING hash that ignores comments, parameter values, UDFs, and literals. The hash value will differ when underlying views change, or if the query implicitly references columns, such as SELECT *, and the table schema changes. This field appears for successful GoogleSQL queries that are not cache hits. |
| query_info.performance_insights | RECORD | Performance insights for the job. |
| query_info.optimization_details | STRUCT | The history-based optimizations for the job. |
| transferred_bytes | INTEGER | Total bytes transferred for cross-cloud queries, such as BigQuery Omni cross-cloud transfer jobs. |
| materialized_view_statistics | RECORD | Statistics of materialized views considered in a query job. (Preview) |
| metadata_cache_statistics | RECORD | Statistics for metadata column index usage for tables referenced in a query job. |
| search_statistics | RECORD | Statistics for a search query. |
| query_dialect | STRING | This field will be available sometime in May, 2025. The query dialect used for the job. Valid values include: GOOGLE_SQL: Job was requested to use GoogleSQL. LEGACY_SQL: Job was requested to use LegacySQL. DEFAULT_LEGACY_SQL: No query dialect was specified in the job request. BigQuery used the default value of LegacySQL. DEFAULT_GOOGLE_SQL: No query dialect was specified in the job request. BigQuery used the default value of GoogleSQL. This field is only populated for query jobs. The default selection of query dialect can be controlled by the configuration settings. |
| continuous | BOOLEAN | Whether the job is a continuous query. |
| continuous_query_info.output_watermark | TIMESTAMP | Represents the point up to which the continuous query has successfully processed data. |
| vector_search_statistics | RECORD | Statistics for a vector search query. |

---

### JOBS_TIMELINE

**Source:** https://cloud.google.com/bigquery/docs/information-schema-jobs-timeline

**Description:** The INFORMATION_SCHEMA.JOBS_TIMELINE view contains near real-time BigQuery metadata by timeslice for all jobs submitted in the current project. This view contains currently running and completed jobs.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| period_start | TIMESTAMP | Start time of this period. |
| period_slot_ms | INTEGER | Slot milliseconds consumed in this period. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the job. |
| job_id | STRING | ID of the job. For example, bquxjob_1234. |
| job_type | STRING | The type of the job. Can be QUERY, LOAD, EXTRACT, COPY, or null. Job type null indicates an internal job, such as script job statement evaluation or materialized view refresh. |
| statement_type | STRING | The type of query statement, if valid. For example, SELECT, INSERT, UPDATE, or DELETE. |
| priority | STRING | The priority of this job. Valid values include INTERACTIVE and BATCH. |
| parent_job_id | STRING | ID of the parent job, if any. |
| job_creation_time | TIMESTAMP | (Partitioning column) Creation time of this job. Partitioning is based on the UTC time of this timestamp. |
| job_start_time | TIMESTAMP | Start time of this job. |
| job_end_time | TIMESTAMP | End time of this job. |
| state | STRING | Running state of the job at the end of this period. Valid states include PENDING, RUNNING, and DONE. |
| reservation_id | STRING | Name of the primary reservation assigned to this job at the end of this period, if applicable. |
| edition | STRING | The edition associated with the reservation assigned to this job. For more information about editions, see Introduction to BigQuery editions. |
| total_bytes_billed | INTEGER | If the project is configured to use on-demand pricing, then this field contains the total bytes billed for the job. If the project is configured to use flat-rate pricing, then you are not billed for bytes and this field is informational only. |
| total_bytes_processed | INTEGER | Total bytes processed by the job. |
| error_result | RECORD | Details of error (if any) as an ErrorProto. |
| cache_hit | BOOLEAN | Whether the query results of this job were from a cache. |
| period_shuffle_ram_usage_ratio | FLOAT | Shuffle usage ratio in the selected time period. |
| period_estimated_runnable_units | INTEGER | Units of work that can be scheduled immediately in this period. Additional slots for these units of work accelerate your query, provided no other query in the reservation needs additional slots. |
| transaction_id | STRING | ID of the transaction in which this job ran, if any. (Preview) |

---

### JOBS_TIMELINE_BY_FOLDER

**Source:** https://cloud.google.com/bigquery/docs/information-schema-jobs-timeline-by-folder

**Description:** The INFORMATION_SCHEMA.JOBS_TIMELINE_BY_FOLDER view contains near real-time BigQuery metadata by timeslice for all jobs submitted in the parent folder of the current project, including the jobs in subfolders under it. This view contains both running and completed jobs.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| period_start | TIMESTAMP | Start time of this period. |
| period_slot_ms | INTEGER | Slot milliseconds consumed in this period. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| folder_numbers | REPEATED INTEGER | Number IDs of the folders that contain the project, starting with the folder that immediately contains the project, followed by the folder that contains the child folder, and so forth. For example, if `folder_numbers` is `[1, 2, 3]`, then folder `1` immediately contains the project, folder `2` contains `1`, and folder `3` contains `2`. |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the job. |
| job_id | STRING | ID of the job. For example, bquxjob_1234. |
| job_type | STRING | The type of the job. Can be QUERY, LOAD, EXTRACT, COPY, or null. Job type null indicates an internal job, such as script job statement evaluation or materialized view refresh. |
| statement_type | STRING | The type of query statement, if valid. For example, SELECT, INSERT, UPDATE, or DELETE. |
| priority | STRING | The priority of this job. Valid values include INTERACTIVE and BATCH. |
| parent_job_id | STRING | ID of the parent job, if any. |
| job_creation_time | TIMESTAMP | (Partitioning column) Creation time of this job. Partitioning is based on the UTC time of this timestamp. |
| job_start_time | TIMESTAMP | Start time of this job. |
| job_end_time | TIMESTAMP | End time of this job. |
| state | STRING | Running state of the job at the end of this period. Valid states include PENDING, RUNNING, and DONE. |
| reservation_id | STRING | Name of the primary reservation assigned to this job at the end of this period, if applicable. |
| edition | STRING | The edition associated with the reservation assigned to this job. For more information about editions, see Introduction to BigQuery editions. |
| total_bytes_billed | INTEGER | If the project is configured to use on-demand pricing, then this field contains the total bytes billed for the job. If the project is configured to use flat-rate pricing, then you are not billed for bytes and this field is informational only. |
| total_bytes_processed | INTEGER | Total bytes processed by the job. |
| error_result | RECORD | Details of error (if any) as an ErrorProto. |
| cache_hit | BOOLEAN | Whether the query results of this job were from a cache. |
| period_shuffle_ram_usage_ratio | FLOAT | Shuffle usage ratio in the selected time period. |
| period_estimated_runnable_units | INTEGER | Units of work that can be scheduled immediately in this period. Additional slots for these units of work accelerate your query, provided no other query in the reservation needs additional slots. |
| transaction_id | STRING | ID of the transaction in which this job ran, if any. (Preview) |

---

### JOBS_TIMELINE_BY_ORGANIZATION

**Source:** https://cloud.google.com/bigquery/docs/information-schema-jobs-timeline-by-organization

**Description:** The INFORMATION_SCHEMA.JOBS_TIMELINE_BY_ORGANIZATION view contains near real-time BigQuery metadata by timeslice for all jobs submitted in the organization associated with the current project. This view contains currently running and completed jobs.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| period_start | TIMESTAMP | Start time of this period. |
| period_slot_ms | INTEGER | Slot milliseconds consumed in this period. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| folder_numbers | REPEATED INTEGER | Number IDs of the folders that contain the project, starting with the folder that immediately contains the project, followed by the folder that contains the child folder, and so forth. For example, if `folder_numbers` is `[1, 2, 3]`, then folder `1` immediately contains the project, folder `2` contains `1`, and folder `3` contains `2`. |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the job. |
| job_id | STRING | ID of the job. For example, bquxjob_1234. |
| job_type | STRING | The type of the job. Can be QUERY, LOAD, EXTRACT, COPY, or null. Job type null indicates an internal job, such as script job statement evaluation or materialized view refresh. |
| statement_type | STRING | The type of query statement, if valid. For example, SELECT, INSERT, UPDATE, or DELETE. |
| priority | STRING | The priority of this job. Valid values include INTERACTIVE and BATCH. |
| parent_job_id | STRING | ID of the parent job, if any. |
| job_creation_time | TIMESTAMP | (Partitioning column) Creation time of this job. Partitioning is based on the UTC time of this timestamp. |
| job_start_time | TIMESTAMP | Start time of this job. |
| job_end_time | TIMESTAMP | End time of this job. |
| state | STRING | Running state of the job at the end of this period. Valid states include PENDING, RUNNING, and DONE. |
| reservation_id | STRING | Name of the primary reservation assigned to this job at the end of this period, if applicable. |
| edition | STRING | The edition associated with the reservation assigned to this job. For more information about editions, see Introduction to BigQuery editions. |
| total_bytes_billed | INTEGER | If the project is configured to use on-demand pricing, then this field contains the total bytes billed for the job. If the project is configured to use flat-rate pricing, then you are not billed for bytes. This field is not configurable. |
| total_bytes_processed | INTEGER | Total bytes processed by the job. |
| error_result | RECORD | Details of error (if any) as an ErrorProto. |
| cache_hit | BOOLEAN | Whether the query results of this job were from a cache. |
| period_shuffle_ram_usage_ratio | FLOAT | Shuffle usage ratio in the selected time period. |
| period_estimated_runnable_units | INTEGER | Units of work that can be scheduled immediately in this period. Additional slots for these units of work accelerate your query, provided no other query in the reservation needs additional slots. |

---

### JOBS_TIMELINE_BY_USER

**Source:** https://cloud.google.com/bigquery/docs/information-schema-jobs-timeline-by-user

**Description:** The INFORMATION_SCHEMA.JOBS_TIMELINE_BY_USER view contains near real-time BigQuery metadata by timeslice of the jobs submitted by the current user in the current project. This view contains currently running and completed jobs.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| period_start | TIMESTAMP | Start time of this period. |
| period_slot_ms | INTEGER | Slot milliseconds consumed in this period. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the job. |
| job_id | STRING | ID of the job. For example, bquxjob_1234. |
| job_type | STRING | The type of the job. Can be QUERY, LOAD, EXTRACT, COPY, or null. Job type null indicates an internal job, such as script job statement evaluation or materialized view refresh. |
| statement_type | STRING | The type of query statement, if valid. For example, SELECT, INSERT, UPDATE, or DELETE. |
| priority | STRING | The priority of this job. Valid values include INTERACTIVE and BATCH. |
| parent_job_id | STRING | ID of the parent job, if any. |
| job_creation_time | TIMESTAMP | (Partitioning column) Creation time of this job. Partitioning is based on the UTC time of this timestamp. |
| job_start_time | TIMESTAMP | Start time of this job. |
| job_end_time | TIMESTAMP | End time of this job. |
| state | STRING | Running state of the job at the end of this period. Valid states include PENDING, RUNNING, and DONE. |
| reservation_id | STRING | Name of the primary reservation assigned to this job at the end of this period, if applicable. |
| edition | STRING | The edition associated with the reservation assigned to this job. For more information about editions, see Introduction to BigQuery editions. |
| total_bytes_billed | INTEGER | If the project is configured to use on-demand pricing, then this field contains the total bytes billed for the job. If the project is configured to use flat-rate pricing, then you are not billed for bytes and this field is informational only. |
| total_bytes_processed | INTEGER | Total bytes processed by the job. |
| error_result | RECORD | Details of error (if any) as an ErrorProto. |
| cache_hit | BOOLEAN | Whether the query results of this job were from a cache. |
| period_shuffle_ram_usage_ratio | FLOAT | Shuffle usage ratio in the selected time period. |
| period_estimated_runnable_units | INTEGER | Units of work that can be scheduled immediately in this period. Additional slots for these units of work accelerate your query, provided no other query in the reservation needs additional slots. |
| transaction_id | STRING | ID of the transaction in which this job ran, if any. (Preview) |

---

### KEY_COLUMN_USAGE

**Source:** https://cloud.google.com/bigquery/docs/information-schema-key-column-usage

**Description:** The KEY_COLUMN_USAGE view contains columns of the tables from TABLE_CONSTRAINTS that are constrained as keys by PRIMARY KEY and FOREIGN KEY constraints.

**Schema:**

| Column Name | Data Type | Value |
| --- | --- | --- |
| CONSTRAINT_CATALOG | STRING | The constraint project name. |
| CONSTRAINT_SCHEMA | STRING | The constraint dataset name. |
| CONSTRAINT_NAME | STRING | The constraint name. |
| TABLE_CATALOG | STRING | The project name of the constrained table. |
| TABLE_SCHEMA | STRING | The name of the constrained table dataset. |
| TABLE_NAME | STRING | The name of the constrained table. |
| COLUMN_NAME | STRING | The name of the constrained column. |
| ORDINAL_POSITION | INT64 | The ordinal position of the column within the constraint key (starting at 1). |
| POSITION_IN_UNIQUE_CONSTRAINT | INT64 | For foreign keys, the ordinal position of the column within the primary key constraint (starting at 1). This value is NULL for primary key constraints. |

---

### MATERIALIZED_VIEWS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-materialized-views

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| TABLE_CATALOG | STRING | The name of the project that contains the dataset. Also referred to as the projectId. |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the materialized view. Also referred to as the datasetId. |
| TABLE_NAME | STRING | The name of the materialized view. Also referred to as the tableId. |
| LAST_REFRESH_TIME | TIMESTAMP | The time when this materialized view was last refreshed. |
| REFRESH_WATERMARK | TIMESTAMP | The refresh watermark of the materialized view. The data contained in materialized view base tables up to this time are included in the materialized view cache. |
| LAST_REFRESH_STATUS | RECORD | Error result of the last automatic refresh job as an ErrorProto object. If present, indicates that the last automatic refresh was unsuccessful. |

---

### OBJECT_PRIVILEGES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-object-privileges

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| OBJECT_CATALOG | STRING | The project ID of the project that contains the resource. |
| OBJECT_SCHEMA | STRING | The name of the dataset that contains the resource. This is NULL if the resource itself is a dataset. |
| OBJECT_NAME | STRING | The name of the table, view, or dataset the policy applies to. |
| OBJECT_TYPE | STRING | The resource type, such as SCHEMA (dataset), TABLE, VIEW, and EXTERNAL. |
| PRIVILEGE_TYPE | STRING | The role ID, such as roles/bigquery.dataEditor. |
| GRANTEE | STRING | The user type and user that the role is granted to. |

---

### ORGANIZATION_OPTIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-organization-options

**Description:** You can query the INFORMATION_SCHEMA.ORGANIZATION_OPTIONS view to retrieve real-time metadata about BigQuery organization options. This view contains information about configuration options in a project that differ from the default values at the organization level.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| OPTION_NAME | STRING | One of the name values in the options table. |
| OPTION_DESCRIPTION | STRING | The option description. |
| OPTION_TYPE | STRING | The data type of the OPTION_VALUE. |
| OPTION_VALUE | STRING | The current value of the option. |

---

### ORGANIZATION_OPTIONS_CHANGES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-organization-options-changes

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| update_time | TIMESTAMP | The time the configuration change occurred. |
| username | STRING | For first-party users, it's their user email. For third-party users, it's the name that users set in the third-party identity provider. |
| updated_options | JSON | A JSON object of the configuration options users updated in the change, containing the previous and the new values of updated fields. |
| project_id | STRING | The project ID. This field is empty for organization-level configuration changes. |
| project_number | INTEGER | The project number. This field is empty for the organization-level configuration changes. |

---

### PARAMETERS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-parameters

**Description:** The INFORMATION_SCHEMA.PARAMETERS view contains one row for each parameter of each routine in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| SPECIFIC_CATALOG | STRING | The name of the project that contains the dataset in which the routine containing the parameter is defined |
| SPECIFIC_SCHEMA | STRING | The name of the dataset that contains the routine in which the parameter is defined |
| SPECIFIC_NAME | STRING | The name of the routine in which the parameter is defined |
| ORDINAL_POSITION | STRING | The 1-based position of the parameter, or 0 for the return value |
| PARAMETER_MODE | STRING | The mode of the parameter, either IN, OUT, INOUT, or NULL |
| IS_RESULT | STRING | Whether the parameter is the result of the function, either YES or NO |
| PARAMETER_NAME | STRING | The name of the parameter |
| DATA_TYPE | STRING | The type of the parameter, will be ANY TYPE if defined as an any type |
| PARAMETER_DEFAULT | STRING | The default value of the parameter as a SQL literal value, always NULL |
| IS_AGGREGATE | STRING | Whether this is an aggregate parameter, always NULL |

---

### PARTITIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-partitions

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| TABLE_CATALOG | STRING | The project ID of the project that contains the table |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the table, also referred to as the datasetId |
| TABLE_NAME | STRING | The name of the table, also referred to as the tableId |
| PARTITION_ID | STRING | A single partition's ID. For unpartitioned tables, the value is NULL. For partitioned tables that contain rows with NULL values in the partitioning column, the value is __NULL__. |
| TOTAL_ROWS | INTEGER | The total number of rows in the partition |
| TOTAL_LOGICAL_BYTES | INTEGER | The total number of logical bytes in the partition |
| LAST_MODIFIED_TIME | TIMESTAMP | The most recent time that data was written to the partition. It is used to calculate a partition's eligibility for long-term storage. After 90 days, the partition automatically transitions from active storage to long-term storage. For more information, see BigQuery storage pricing. This field is updated when data is inserted, loaded, streamed, or modified within the partition. Modifications that involve record deletions might not be reflected. |
| STORAGE_TIER | STRING | The partition's storage tier: ACTIVE: the partition is billed as active storage LONG_TERM: the partition is billed as long-term storage |

---

### PARTITIONS#SCOPE_AND_SYNTAX

**Source:** https://cloud.google.com/bigquery/docs/information-schema-partitions#scope_and_syntax

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| TABLE_CATALOG | STRING | The project ID of the project that contains the table |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the table, also referred to as the datasetId |
| TABLE_NAME | STRING | The name of the table, also referred to as the tableId |
| PARTITION_ID | STRING | A single partition's ID. For unpartitioned tables, the value is NULL. For partitioned tables that contain rows with NULL values in the partitioning column, the value is __NULL__. |
| TOTAL_ROWS | INTEGER | The total number of rows in the partition |
| TOTAL_LOGICAL_BYTES | INTEGER | The total number of logical bytes in the partition |
| LAST_MODIFIED_TIME | TIMESTAMP | The most recent time that data was written to the partition. It is used to calculate a partition's eligibility for long-term storage. After 90 days, the partition automatically transitions from active storage to long-term storage. For more information, see BigQuery storage pricing. This field is updated when data is inserted, loaded, streamed, or modified within the partition. Modifications that involve record deletions might not be reflected. |
| STORAGE_TIER | STRING | The partition's storage tier: ACTIVE: the partition is billed as active storage LONG_TERM: the partition is billed as long-term storage |

---

### PROJECT_OPTIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-project-options

**Description:** You can query the INFORMATION_SCHEMA.PROJECT_OPTIONS view to retrieve real-time metadata about BigQuery project options. This view contains information about configuration options in a project that differ from the default values.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| OPTION_NAME | STRING | Option ID for the specified configuration setting. |
| OPTION_DESCRIPTION | STRING | The option description. |
| OPTION_TYPE | STRING | The data type of the OPTION_VALUE. |
| OPTION_VALUE | STRING | The current value of the option. |

---

### PROJECT_OPTIONS_CHANGES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-project-options-changes

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| update_time | TIMESTAMP | The time the configuration change occurred. |
| username | STRING | For first-party users, it's their user email. For third-party users, it's the name that users set in the third-party identity provider. |
| updated_options | JSON | A JSON object of the configuration options users updated in the change, containing the previous and the new values of updated fields. |
| project_id | STRING | The project ID. This field is empty for organization-level configuration changes. |
| project_number | INTEGER | The project number. This field is empty for the organization-level configuration changes. |

---

### RECOMMENDATIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-recommendations

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| recommendation_id | STRING | Base64 encoded ID that contains the RecommendationID and recommender. |
| recommender | STRING | The type of recommendation. For example, google.bigquery.table.PartitionClusterRecommender for partitioning and clustering recommendations. |
| subtype | STRING | The subtype of the recommendation. |
| project_id | STRING | The ID of the project. |
| project_number | STRING | The number of the project. |
| description | STRING | The description about the recommendation. |
| last_updated_time | TIMESTAMP | This field represents the time when the recommendation was last created. |
| target_resources | STRING | Fully qualified resource names this recommendation is targeting. |
| state | STRING | The state of the recommendation. For a list of possible values, see State. |
| primary_impact | RECORD | The impact this recommendation can have when trying to optimize the primary category. Contains the following fields: category: The category this recommendation is trying to optimize. For a list of possible values, see Category. cost_projection: This value may be populated if the recommendation can project the cost savings from this recommendation. Only present when the category is COST. security_projection: Might be present when the category is SECURITY. |
| priority | STRING | The priority of the recommendation. For a list of possible values, see Priority. |
| associated_insight_ids | STRING | Full Insight names associated with the recommendation.Insight name is the Base64 encoded representation of Insight type name & the Insight ID. This can be used to query Insights view. |
| additional_details | RECORD | Additional Details about the recommendation. overview: Overview of the recommendation in JSON format. The content of this field might change based on the recommender. state_metadata: Metadata about the state of the recommendation in key-value pairs. operations: List of operations the user can perform on the target resources. This contains the following fields: action: The type of action the user must perform. This can be a free-text set by the system while generating the recommendation. Will always be populated. resource_type: The cloud resource type. resource: Fully qualified resource name. path: Path of the target field relative to the resource. value: Value of the path field. |

---

### RECOMMENDATIONS_BY_ORG

**Source:** https://cloud.google.com/bigquery/docs/information-schema-recommendations-by-org

**Description:** Preview

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| recommendation_id | STRING | Base64 encoded ID that contains the RecommendationID and recommender. |
| recommender | STRING | The type of recommendation. For example, google.bigquery.table.PartitionClusterRecommender for partitioning and clustering recommendations. |
| subtype | STRING | The subtype of the recommendation. |
| project_id | STRING | The ID of the project. |
| project_number | STRING | The number of the project. |
| description | STRING | The description about the recommendation. |
| last_updated_time | TIMESTAMP | This field represents the time when the recommendation was last created. |
| target_resources | STRING | Fully qualified resource names this recommendation is targeting. |
| state | STRING | The state of the recommendation. For a list of possible values, see State. |
| primary_impact | RECORD | The impact this recommendation can have when trying to optimize the primary category. Contains the following fields: category: The category this recommendation is trying to optimize. For a list of possible values, see Category. cost_projection: This value may be populated if the recommendation can project the cost savings from this recommendation. Only present when the category is COST. security_projection: Might be present when the category is SECURITY. |
| priority | STRING | The priority of the recommendation. For a list of possible values, see Priority. |
| associated_insight_ids | STRING | Full Insight names associated with the recommendation.Insight name is the Base64 encoded representation of Insight type name & the Insight ID. This can be used to query Insights view. |
| additional_details | RECORD | Additional Details about the recommendation. overview: Overview of the recommendation in JSON format. The content of this field might change based on the recommender. state_metadata: Metadata about the state of the recommendation in key-value pairs. operations: List of operations the user can perform on the target resources. This contains the following fields: action: The type of action the user must perform. This can be a free-text set by the system while generating the recommendation. Will always be populated. resource_type: The cloud resource type. resource: Fully qualified resource name. path: Path of the target field relative to the resource. value: Value of the path field. |

---

### RESERVATIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-reservations

**Description:** The INFORMATION_SCHEMA.RESERVATIONS view contains a near real-time list of all current reservations within the administration project. Each row represents a single, current reservation. A current reservation is a reservation that has not been deleted. For more information about reservation, see Introduction to reservations.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| ddl | STRING | The DDL statement used to create this reservation. |
| project_id | STRING | ID of the administration project. |
| project_number | INTEGER | Number of the administration project. |
| reservation_name | STRING | User provided reservation name. |
| ignore_idle_slots | BOOL | If false, any query using this reservation can use unused idle slots from other capacity commitments. |
| slot_capacity | INTEGER | Baseline of the reservation. |
| target_job_concurrency | INTEGER | The target number of queries that can execute simultaneously, which is limited by available resources. If zero, then this value is computed automatically based on available resources. |
| autoscale | STRUCT | Information about the autoscale capacity of the reservation. Fields include the following: current_slots: the number of slots added to the reservation by autoscaling. Note: After users reduce max_slots, it may take a while before it can be propagated, so current_slots may stay in the original value and could be larger than max_slots for that brief period (less than one minute). max_slots: the maximum number of slots that could be added to the reservation by autoscaling. |
| edition | STRING | The edition associated with this reservation. For more information about editions, see Introduction to BigQuery editions. |
| primaryLocation | STRING | The current location of the reservation's primary replica. This field is only set for reservations using the managed disaster recovery feature. |
| secondaryLocation | STRING | The current location of the reservation's secondary replica. This field is only set for reservations using the managed disaster recovery feature. |
| originalPrimaryLocation | STRING | The location where the reservation was originally created. |
| labels | RECORD | Array of labels associated with the reservation. |
| max_slots | INTEGER | The maximum number of slots that this reservation can use, which includes baseline slots (slot_capacity), idle slots (if ignore_idle_slots is false), and autoscale slots. This field is specified by users for using the reservation predictability feature. |
| scaling_mode | STRING | The scaling mode for the reservation, which determines how the reservation scales from baseline to max_slots. This field is specified by users for using the reservation predictability feature. |

---

### RESERVATION_CHANGES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-reservation-changes

**Description:** The INFORMATION_SCHEMA.RESERVATION_CHANGES view contains a near real-time list of all changes to reservations within the administration project. Each row represents a change to a single reservation. For more information, see Introduction to reservations.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| change_timestamp | TIMESTAMP | Time when the change occurred. |
| project_id | STRING | ID of the administration project. |
| project_number | INTEGER | Number of the administration project. |
| reservation_name | STRING | User provided reservation name. |
| ignore_idle_slots | BOOL | If false, any query using this reservation can use unused idle slots from other capacity commitments. |
| action | STRING | Type of event that occurred with the reservation. Can be CREATE, UPDATE, or DELETE. |
| slot_capacity | INTEGER | Baseline of the reservation. |
| user_email | STRING | Email address of the user or subject of the workforce identity federation that made the change. google for changes made by Google. NULL if the email address is unknown. |
| target_job_concurrency | INTEGER | The target number of queries that can execute simultaneously, which is limited by available resources. If zero, then this value is computed automatically based on available resources. |
| autoscale | STRUCT | Information about the autoscale capacity of the reservation. Fields include the following: current_slots: the number of slots added to the reservation by autoscaling. Note: After users reduce max_slots, it may take a while before it can be propagated, so current_slots may stay in the original value and could be larger than max_slots for that brief period (less than one minute). max_slots: the maximum number of slots that could be added to the reservation by autoscaling. |
| edition | STRING | The edition associated with this reservation. For more information about editions, see Introduction to BigQuery editions. |
| primaryLocation | STRING | The current location of the reservation's primary replica. This field is only set for reservations using the managed disaster recovery feature. |
| secondaryLocation | STRING | The current location of the reservation's secondary replica. This field is only set for reservations using the managed disaster recovery feature. |
| originalPrimaryLocation | STRING | The location where the reservation was originally created. |
| labels | RECORD | Array of labels associated with the reservation. |
| max_slots | INTEGER | The maximum number of slots that this reservation can use, which includes baseline slots (slot_capacity), idle slots (if ignore_idle_slots is false), and autoscale slots. This field is specified by users for using the reservation predictability feature. |
| scaling_mode | STRING | The scaling mode for the reservation, which determines how the reservation scales from baseline to max_slots. This field is specified by users for using the reservation predictability feature. |

---

### RESERVATION_TIMELINE

**Source:** https://cloud.google.com/bigquery/docs/information-schema-reservation-timeline

**Description:** The INFORMATION_SCHEMA.RESERVATIONS_TIMELINE view shows near real-time time slices of reservation metadata for each reservation administration project for every minute.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| autoscale | STRUCT | Information about the autoscale capacity of the reservation. Fields include the following: current_slots: the number of slots added to the reservation by autoscaling. Note: After users reduce max_slots, it may take a while before it can be propagated, so current_slots may stay in the original value and could be larger than max_slots for that brief period (less than one minute). max_slots: the maximum number of slots that could be added to the reservation by autoscaling. |
| edition | STRING | The edition associated with this reservation. For more information about editions, see Introduction to BigQuery editions. |
| ignore_idle_slots | BOOL | False if slot sharing is enabled, otherwise true. |
| labels | RECORD | Array of labels associated with the reservation. |
| period_start | TIMESTAMP | Start time of this one-minute period. |
| project_id | STRING | ID of the reservation admin project. |
| project_number | INTEGER | Number of the project. |
| reservation_id | STRING | For joining with the jobs_timeline table. This is of the form project_id:location.reservation_name. |
| reservation_name | STRING | The name of the reservation. |
| slots_assigned | INTEGER | The number of slots assigned to this reservation. |
| slots_max_assigned | INTEGER | The maximum slot capacity for this reservation, including slot sharing. If ignore_idle_slots is true, this is the same as slots_assigned, otherwise this is the total number of slots in all capacity commitments in the admin project. |
| max_slots | INTEGER | The maximum number of slots that this reservation can use, which includes baseline slots (slot_capacity), idle slots (if ignore_idle_slots is false), and autoscale slots. This field is specified by users for using the reservation predictability feature. |
| scaling_mode | STRING | The scaling mode for the reservation, which determines how the reservation scales from baseline to max_slots. This field is specified by users for using the reservation predictability feature. |

---

### ROUTINES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-routines

**Description:** The INFORMATION_SCHEMA.ROUTINES view contains one row for each routine in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| SPECIFIC_CATALOG | STRING | The name of the project that contains the dataset where the routine is defined |
| SPECIFIC_SCHEMA | STRING | The name of the dataset that contains the routine |
| SPECIFIC_NAME | STRING | The name of the routine |
| ROUTINE_CATALOG | STRING | The name of the project that contains the dataset where the routine is defined |
| ROUTINE_SCHEMA | STRING | The name of the dataset that contains the routine |
| ROUTINE_NAME | STRING | The name of the routine |
| ROUTINE_TYPE | STRING | The routine type: FUNCTION: A BigQuery persistent user-defined function PROCEDURE: A BigQuery stored procedure TABLE FUNCTION: A BigQuery table function. |
| DATA_TYPE | STRING | The data type that the routine returns. NULL if the routine is a stored procedure |
| ROUTINE_BODY | STRING | How the body of the routine is defined, either SQL or EXTERNAL if the routine is a JavaScript user-defined function |
| ROUTINE_DEFINITION | STRING | The definition of the routine |
| EXTERNAL_LANGUAGE | STRING | JAVASCRIPT if the routine is a JavaScript user-defined function or NULL if the routine was defined with SQL |
| IS_DETERMINISTIC | STRING | YES if the routine is known to be deterministic, NO if it is not, or NULL if unknown |
| SECURITY_TYPE | STRING | Security type of the routine, always NULL |
| CREATED | TIMESTAMP | The routine's creation time |
| LAST_ALTERED | TIMESTAMP | The routine's last modification time |
| DDL | STRING | The DDL statement that can be used to create the routine, such as CREATE FUNCTION or CREATE PROCEDURE |
| CONNECTION | STRING | The connection name, if the routine has one. Otherwise NULL |

---

### ROUTINE_OPTIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-routine-options

**Description:** The INFORMATION_SCHEMA.ROUTINE_OPTIONS view contains one row for each option of each routine in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| SPECIFIC_CATALOG | STRING | The name of the project that contains the routine where the option is defined |
| SPECIFIC_SCHEMA | STRING | The name of the dataset that contains the routine where the option is defined |
| SPECIFIC_NAME | STRING | The name of the routine |
| OPTION_NAME | STRING | One of the name values in the options table |
| OPTION_TYPE | STRING | One of the data type values in the options table |
| OPTION_VALUE | STRING | One of the value options in the options table |

---

### SCHEMATA_REPLICAS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-schemata-replicas

**Description:** Preview

---

### SCHEMATA_REPLICAS_BY_FAILOVER_RESERVATION

**Source:** https://cloud.google.com/bigquery/docs/information-schema-schemata-replicas-by-failover-reservation

**Description:** Preview

---

### SESSIONS_BY_PROJECT

**Source:** https://cloud.google.com/bigquery/docs/information-schema-sessions-by-project

**Description:** The INFORMATION_SCHEMA.SESSIONS_BY_PROJECT view contains real-time metadata about all BigQuery sessions in the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| creation_time | TIMESTAMP | (Partitioning column) Creation time of this session. Partitioning is based on the UTC time of this timestamp. |
| expiration_time | TIMESTAMP | (Partitioning column) Expiration time of this session. Partitioning is based on the UTC time of this timestamp. |
| is_active | BOOL | Is the session is still active? TRUE if yes, otherwise FALSE. |
| last_modified_time | TIMESTAMP | (Partitioning column) Time when the session was last modified. Partitioning is based on the UTC time of this timestamp. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| session_id | STRING | ID of the session. For example, bquxsession_1234. |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the session. |

---

### SESSIONS_BY_USER

**Source:** https://cloud.google.com/bigquery/docs/information-schema-sessions-by-user

**Description:** The INFORMATION_SCHEMA.SESSIONS_BY_USER view contains real-time metadata about BigQuery sessions created by the current user in the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| creation_time | TIMESTAMP | (Partitioning column) Creation time of this session. Partitioning is based on the UTC time of this timestamp. |
| expiration_time | TIMESTAMP | (Partitioning column) Expiration time of this session. Partitioning is based on the UTC time of this timestamp. |
| is_active | BOOL | Is the session is still active? TRUE if yes, otherwise FALSE. |
| last_modified_time | TIMESTAMP | (Partitioning column) Time when the session was last modified. Partitioning is based on the UTC time of this timestamp. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| session_id | STRING | ID of the session. For example, bquxsession_1234. |
| user_email | STRING | (Clustering column) Email address or service account of the user who ran the session. |

---

### SHARED_DATASET_USAGE

**Source:** https://cloud.google.com/bigquery/docs/information-schema-shared-dataset-usage

**Description:** The INFORMATION_SCHEMA.SHARED_DATASET_USAGE view contains the near real-time metadata about consumption of your shared dataset tables. To get started with sharing your data across organizations, see BigQuery sharing (formerly Analytics Hub).

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| project_id | STRING | (Clustering column) The ID of the project that contains the shared dataset. |
| dataset_id | STRING | (Clustering column) The ID of the shared dataset. |
| table_id | STRING | The ID of the accessed table. |
| data_exchange_id | STRING | The resource path of the data exchange. |
| listing_id | STRING | The resource path of the listing. |
| job_start_time | TIMESTAMP | (Partitioning column) The start time of this job. |
| job_end_time | TIMESTAMP | The end time of this job. |
| job_id | STRING | The job ID. For example, bquxjob_1234. |
| job_project_number | INTEGER | The number of the project this job belongs to. |
| job_location | STRING | The location of the job. |
| linked_project_number | INTEGER | The project number of the subscriber's project. |
| linked_dataset_id | STRING | The linked dataset ID of the subscriber's dataset. |
| subscriber_org_number | INTEGER | The organization number in which the job ran. This is the organization number of the subscriber. This field is empty for projects that don't have an organization. |
| subscriber_org_display_name | STRING | A human-readable string that refers to the organization in which the job ran. This is the organization number of the subscriber. This field is empty for projects that don't have an organization. |
| job_principal_subject | STRING | The principal identifier (user email ID, service account, group email ID, domain) of users who execute jobs and queries against linked datasets. |
| num_rows_processed | INTEGER | The number of rows processed from this table by the job. |
| total_bytes_processed | INTEGER | The total bytes processed from this table by the job. |

---

### SNAPSHOTS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-snapshots

**Description:** The INFORMATION_SCHEMA.TABLE_SNAPSHOTS view contains metadata about your table snapshots. For more information, see Introduction to table snapshots.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| table_catalog | STRING | The name of the project that contains the table snapshot |
| table_schema | STRING | The name of the dataset that contains the table snapshot |
| table_name | STRING | The name of the table snapshot |
| base_table_catalog | STRING | The name of the project that contains the base table |
| base_table_schema | STRING | The name of the dataset that contains the base table |

---

### STREAMING

**Source:** https://cloud.google.com/bigquery/docs/information-schema-streaming

**Description:** The INFORMATION_SCHEMA.STREAMING_TIMELINE view contains per minute aggregated streaming statistics for the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| start_timestamp | TIMESTAMP | (Partitioning column) Start timestamp of the 1 minute interval for the aggregated statistics. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| dataset_id | STRING | (Clustering column) ID of the dataset. |
| table_id | STRING | (Clustering column) ID of the table. |
| error_code | STRING | Error code returned for the requests specified by this row. NULL for successful requests. |
| total_requests | INTEGER | Total number of requests within the 1 minute interval. |
| total_rows | INTEGER | Total number of rows from all requests within the 1 minute interval. |
| total_input_bytes | INTEGER | Total number of bytes from all rows within the 1 minute interval. |

---

### STREAMING_BY_FOLDER

**Source:** https://cloud.google.com/bigquery/docs/information-schema-streaming-by-folder

**Description:** The INFORMATION_SCHEMA.STREAMING_TIMELINE_BY_FOLDER view contains per minute aggregated streaming statistics for the parent folder of the current project, including its subfolders.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| start_timestamp | TIMESTAMP | (Partitioning column) Start timestamp of the 1 minute interval for the aggregated statistics. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| dataset_id | STRING | (Clustering column) ID of the dataset. |
| table_id | STRING | (Clustering column) ID of the table. |
| error_code | STRING | Error code returned for the requests specified by this row. NULL for successful requests. |
| total_requests | INTEGER | Total number of requests within the 1 minute interval. |
| total_rows | INTEGER | Total number of rows from all requests within the 1 minute interval. |
| total_input_bytes | INTEGER | Total number of bytes from all rows within the 1 minute interval. |

---

### STREAMING_BY_ORGANIZATION

**Source:** https://cloud.google.com/bigquery/docs/information-schema-streaming-by-organization

**Description:** The INFORMATION_SCHEMA.STREAMING_TIMELINE_BY_ORGANIZATION view contains per minute aggregated streaming statistics for the whole organization associated with the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| start_timestamp | TIMESTAMP | (Partitioning column) Start timestamp of the 1 minute interval for the aggregated statistics. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| dataset_id | STRING | (Clustering column) ID of the dataset. |
| table_id | STRING | (Clustering column) ID of the table. |
| error_code | STRING | Error code returned for the requests specified by this row. NULL for successful requests. |
| total_requests | INTEGER | Total number of requests within the 1 minute interval. |
| total_rows | INTEGER | Total number of rows from all requests within the 1 minute interval. |
| total_input_bytes | INTEGER | Total number of bytes from all rows within the 1 minute interval. |

---

### TABLES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-tables

**Description:** The INFORMATION_SCHEMA.TABLES view contains one row for each table or view in a dataset. The TABLES and TABLE_OPTIONS views also contain high-level information about views. For detailed information, query the INFORMATION_SCHEMA.VIEWS view.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| table_catalog | STRING | The project ID of the project that contains the dataset. |
| table_schema | STRING | The name of the dataset that contains the table or view. Also referred to as the datasetId. |
| table_name | STRING | The name of the table or view. Also referred to as the tableId. |
| table_type | STRING | The table type; one of the following: BASE TABLE: A standard table CLONE: A table clone SNAPSHOT: A table snapshot VIEW: A view MATERIALIZED VIEW: A materialized view or materialized view replica EXTERNAL: A table that references an external data source |
| is_insertable_into | STRING | YES or NO depending on whether the table supports DML INSERT statements |
| is_typed | STRING | The value is always NO |
| is_change_history_enabled | STRING | YES or NO depending on whether change history is enabled |
| creation_time | TIMESTAMP | The table's creation time |
| base_table_catalog | STRING | For table clones and table snapshots, the base table's project. Applicable only to tables with table_type set to CLONE or SNAPSHOT. |
| base_table_schema | STRING | For table clones and table snapshots, the base table's dataset. Applicable only to tables with table_type set to CLONE or SNAPSHOT. |
| base_table_name | STRING | For table clones and table snapshots, the base table's name. Applicable only to tables with table_type set to CLONE or SNAPSHOT. |
| snapshot_time_ms | TIMESTAMP | For table clones and table snapshots, the time when the clone or snapshot operation was run on the base table to create this table. If time travel was used, then this field contains the time travel timestamp. Otherwise, the snapshot_time_ms field is the same as the creation_time field. Applicable only to tables with table_type set to CLONE or SNAPSHOT. |
| replica_source_catalog | STRING | For materialized view replicas, the base materialized view's project. |
| replica_source_schema | STRING | For materialized view replicas, the base materialized view's dataset. |
| replica_source_name | STRING | For materialized view replicas, the base materialized view's name. |
| replication_status | STRING | For materialized view replicas, the status of the replication from the base materialized view to the materialized view replica; one of the following: REPLICATION_STATUS_UNSPECIFIED ACTIVE: Replication is active with no errors SOURCE_DELETED: The source materialized view has been deleted PERMISSION_DENIED: The source materialized view hasn't been authorized on the dataset that contains the source Amazon S3 BigLake tables used in the query that created the materialized view. UNSUPPORTED_CONFIGURATION: There is an issue with the replica's prerequisites other than source materialized view authorization. |
| replication_error | STRING | If replication_status indicates a replication issue for a materialized view replica, replication_error provides further details about the issue. |
| ddl | STRING | The DDL statement that can be used to recreate the table, such as CREATE TABLE or CREATE VIEW |
| default_collation_name | STRING | The name of the default collation specification if it exists; otherwise, NULL. |
| upsert_stream_apply_watermark | TIMESTAMP | For tables that use change data capture (CDC), the time when row modifications were last applied. For more information, see Monitor table upsert operation progress. |

---

### TABLE_CONSTRAINTS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-table-constraints

**Description:** The TABLE_CONSTRAINTS view contains the primary and foreign key relations in a BigQuery dataset.

---

### TABLE_OPTIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-table-options

**Description:** The INFORMATION_SCHEMA.TABLE_OPTIONS view contains one row for each option, for each table or view in a dataset. The TABLES and TABLE_OPTIONS views also contain high-level information about views. For detailed information, query the INFORMATION_SCHEMA.VIEWS view.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| TABLE_CATALOG | STRING | The project ID of the project that contains the dataset |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the table or view also referred to as the datasetId |
| TABLE_NAME | STRING | The name of the table or view also referred to as the tableId |
| OPTION_NAME | STRING | One of the name values in the options table |
| OPTION_TYPE | STRING | One of the data type values in the options table |
| OPTION_VALUE | STRING | One of the value options in the options table |

---

### TABLE_STORAGE

**Source:** https://cloud.google.com/bigquery/docs/information-schema-table-storage

**Description:** The INFORMATION_SCHEMA.TABLE_STORAGE view provides a current snapshot of storage usage for tables and materialized views. When you query the INFORMATION_SCHEMA.TABLE_STORAGE view, the query results contain one row for each table or materialized view for the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| PROJECT_ID | STRING | The project ID of the project that contains the dataset. |
| PROJECT_NUMBER | INT64 | The project number of the project that contains the dataset. |
| TABLE_CATALOG | STRING | The project ID of the project that contains the dataset. |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the table or materialized view, also referred to as the datasetId. |
| TABLE_NAME | STRING | The name of the table or materialized view, also referred to as the tableId. |
| CREATION_TIME | TIMESTAMP | The creation time of the table. |
| TOTAL_ROWS | INT64 | The total number of rows in the table or materialized view. |
| TOTAL_PARTITIONS | INT64 | The number of partitions present in the table or materialized view. Unpartitioned tables return 0. |
| TOTAL_LOGICAL_BYTES | INT64 | Total number of logical (uncompressed) bytes in the table or materialized view. |
| ACTIVE_LOGICAL_BYTES | INT64 | Number of logical (uncompressed) bytes that are younger than 90 days. |
| LONG_TERM_LOGICAL_BYTES | INT64 | Number of logical (uncompressed) bytes that are older than 90 days. |
| CURRENT_PHYSICAL_BYTES | INT64 | Total number of physical bytes for the current storage of the table across all partitions. |
| TOTAL_PHYSICAL_BYTES | INT64 | Total number of physical (compressed) bytes used for storage, including active, long-term, and time travel (deleted or changed data) bytes. Fail-safe (deleted or changed data retained after the time-travel window) bytes aren't included. |
| ACTIVE_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes younger than 90 days, including time travel (deleted or changed data) bytes. |
| LONG_TERM_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes older than 90 days. |
| TIME_TRAVEL_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes used by time travel storage (deleted or changed data). |
| STORAGE_LAST_MODIFIED_TIME | TIMESTAMP | The most recent time that data was written to the table. |
| DELETED | BOOLEAN | Indicates whether or not the table is deleted. |
| TABLE_TYPE | STRING | The type of table. For example, BASE TABLE. |
| FAIL_SAFE_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes used by the fail-safe storage (deleted or changed data). |
| LAST_METADATA_INDEX_REFRESH_TIME | TIMESTAMP | The last metadata index refresh time of the table. |

---

### TABLE_STORAGE_BY_FOLDER

**Source:** https://cloud.google.com/bigquery/docs/information-schema-table-storage-by-folder

**Description:** The INFORMATION_SCHEMA.TABLE_STORAGE_BY_FOLDER view contains one row for each table or materialized view in the parent folder of the current project, including its subfolders.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| FOLDER_NUMBERS | REPEATED INTEGER | Number IDs of folders that contain the project, starting with the folder that immediately contains the project, followed by the folder that contains the child folder, and so forth. For example, if FOLDER_NUMBERS is [1, 2, 3], then folder 1 immediately contains the project, folder 2 contains 1, and folder 3 contains 2. This column is only populated in TABLE_STORAGE_BY_FOLDER. |
| PROJECT_ID | STRING | The project ID of the project that contains the dataset. |
| PROJECT_NUMBER | INT64 | The project number of the project that contains the dataset. |
| TABLE_CATALOG | STRING | The project ID of the project that contains the dataset. |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the table or materialized view, also referred to as the datasetId. |
| TABLE_NAME | STRING | The name of the table or materialized view, also referred to as the tableId. |
| CREATION_TIME | TIMESTAMP | The creation time of the table. |
| TOTAL_ROWS | INT64 | The total number of rows in the table or materialized view. |
| TOTAL_PARTITIONS | INT64 | The number of partitions present in the table or materialized view. Unpartitioned tables return 0. |
| TOTAL_LOGICAL_BYTES | INT64 | Total number of logical (uncompressed) bytes in the table or materialized view. |
| ACTIVE_LOGICAL_BYTES | INT64 | Number of logical (uncompressed) bytes that are younger than 90 days. |
| LONG_TERM_LOGICAL_BYTES | INT64 | Number of logical (uncompressed) bytes that are older than 90 days. |
| CURRENT_PHYSICAL_BYTES | INT64 | Total number of physical bytes for the current storage of the table across all partitions. |
| TOTAL_PHYSICAL_BYTES | INT64 | Total number of physical (compressed) bytes used for storage, including active, long-term, and time travel (deleted or changed data) bytes. Fail-safe (deleted or changed data retained after the time-travel window) bytes aren't included. |
| ACTIVE_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes younger than 90 days, including time travel (deleted or changed data) bytes. |
| LONG_TERM_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes older than 90 days. |
| TIME_TRAVEL_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes used by time travel storage (deleted or changed data). |
| STORAGE_LAST_MODIFIED_TIME | TIMESTAMP | The most recent time that data was written to the table. |
| DELETED | BOOLEAN | Indicates whether or not the table is deleted. |
| TABLE_TYPE | STRING | The type of table. For example, BASE TABLE. |
| FAIL_SAFE_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes used by the fail-safe storage (deleted or changed data). |
| LAST_METADATA_INDEX_REFRESH_TIME | TIMESTAMP | The last metadata index refresh time of the table. |

---

### TABLE_STORAGE_BY_ORGANIZATION

**Source:** https://cloud.google.com/bigquery/docs/information-schema-table-storage-by-organization

**Description:** The INFORMATION_SCHEMA.TABLE_STORAGE_BY_ORGANIZATION view contain one row for each table or materialized view for the whole organization associated with the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| PROJECT_ID | STRING | The project ID of the project that contains the dataset. |
| PROJECT_NUMBER | INT64 | The project number of the project that contains the dataset. |
| TABLE_CATALOG | STRING | The project ID of the project that contains the dataset. |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the table or materialized view, also referred to as the datasetId. |
| TABLE_NAME | STRING | The name of the table or materialized view, also referred to as the tableId. |
| CREATION_TIME | TIMESTAMP | The creation time of the table. |
| TOTAL_ROWS | INT64 | The total number of rows in the table or materialized view. |
| TOTAL_PARTITIONS | INT64 | The number of partitions present in the table or materialized view. Unpartitioned tables return 0. |
| TOTAL_LOGICAL_BYTES | INT64 | Total number of logical (uncompressed) bytes in the table or materialized view. |
| ACTIVE_LOGICAL_BYTES | INT64 | Number of logical (uncompressed) bytes that are younger than 90 days. |
| LONG_TERM_LOGICAL_BYTES | INT64 | Number of logical (uncompressed) bytes that are older than 90 days. |
| CURRENT_PHYSICAL_BYTES | INT64 | Total number of physical bytes for the current storage of the table across all partitions. |
| TOTAL_PHYSICAL_BYTES | INT64 | Total number of physical (compressed) bytes used for storage, including active, long-term, and time travel (deleted or changed data) bytes. Fail-safe (deleted or changed data retained after the time-travel window) bytes aren't included. |
| ACTIVE_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes younger than 90 days, including time travel (deleted or changed data) bytes. |
| LONG_TERM_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes older than 90 days. |
| TIME_TRAVEL_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes used by time travel storage (deleted or changed data). |
| STORAGE_LAST_MODIFIED_TIME | TIMESTAMP | The most recent time that data was written to the table. |
| DELETED | BOOLEAN | Indicates whether or not the table is deleted. |
| TABLE_TYPE | STRING | The type of table. For example, BASE TABLE. |
| FAIL_SAFE_PHYSICAL_BYTES | INT64 | Number of physical (compressed) bytes used by the fail-safe storage (deleted or changed data). |
| LAST_METADATA_INDEX_REFRESH_TIME | TIMESTAMP | The last metadata index refresh time of the table. |

---

### TABLE_STORAGE_USAGE

**Source:** https://cloud.google.com/bigquery/docs/information-schema-table-storage-usage

**Description:** Preview

---

### TABLE_STORAGE_USAGE_BY_FOLDER

**Source:** https://cloud.google.com/bigquery/docs/information-schema-table-storage-usage-by-folder

**Description:** Preview

---

### TABLE_STORAGE_USAGE_BY_ORGANIZATION

**Source:** https://cloud.google.com/bigquery/docs/information-schema-table-storage-usage-by-organization

**Description:** Preview

---

### VECTOR_INDEXES

**Source:** https://cloud.google.com/bigquery/docs/information-schema-vector-indexes

**Description:** The INFORMATION_SCHEMA.VECTOR_INDEXES view contains one row for each vector index in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| index_catalog | STRING | The name of the project that contains the dataset. |
| index_schema | STRING | The name of the dataset that contains the index. |
| table_name | STRING | The name of the table that the index is created on. |
| index_name | STRING | The name of the vector index. |
| index_status | STRING | The status of the index: ACTIVE, PENDING DISABLEMENT, TEMPORARILY DISABLED, or PERMANENTLY DISABLED. ACTIVE means that the index is usable or being created. Refer to the coverage_percentage to see the progress of index creation. PENDING DISABLEMENT means that the total size of indexed tables exceeds your organization's limit; the index is queued for deletion. While in this state, the index is usable in vector search queries and you are charged for the vector index storage. TEMPORARILY DISABLED means that either the total size of indexed tables exceeds your organization's limit, or the indexed table is smaller than 10 MB. While in this state, the index isn't used in vector search queries and you aren't charged for the vector index storage. PERMANENTLY DISABLED means that there is an incompatible schema change on the indexed table. |
| creation_time | TIMESTAMP | The time the index was created. |
| last_modification_time | TIMESTAMP | The last time the index configuration was modified. For example, deleting an indexed column. |
| last_refresh_time | TIMESTAMP | The last time the table data was indexed. A NULL value means the index is not yet available. |
| disable_time | TIMESTAMP | The time the status of the index was set to DISABLED. The value is NULL if the index status is not DISABLED. |
| disable_reason | STRING | The reason the index was disabled. NULL if the index status is not DISABLED. |
| DDL | STRING | The data definition language (DDL) statement used to create the index. |
| coverage_percentage | INTEGER | The approximate percentage of table data that has been indexed. 0% means the index is not usable in a VECTOR_SEARCH query, even if some data has already been indexed. |
| unindexed_row_count | INTEGER | The number of rows in the table that have not been indexed. |
| total_logical_bytes | INTEGER | The number of billable logical bytes for the index. |
| total_storage_bytes | INTEGER | The number of billable storage bytes for the index. |

---

### VECTOR_INDEX_COLUMNS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-vector-index-columns

**Description:** The INFORMATION_SCHEMA.VECTOR_INDEX_COLUMNS view contains one row for each vector-indexed column on each table in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| index_catalog | STRING | The name of the project that contains the dataset. |
| index_schema | STRING | The name of the dataset that contains the vector index. |
| table_name | STRING | The name of the table that the vector index is created on. |
| index_name | STRING | The name of the vector index. |
| index_column_name | STRING | The name of the indexed column. |
| index_field_path | STRING | The full path of the expanded indexed field, starting with the column name. Fields are separated by a period. |

---

### VECTOR_INDEX_OPTIONS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-vector-index-options

**Description:** The INFORMATION_SCHEMA.VECTOR_INDEX_OPTIONS view contains one row for each vector index option in a dataset.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| index_catalog | STRING | The name of the project that contains the dataset. |
| index_schema | STRING | The name of the dataset that contains the vector index. |
| table_name | STRING | The name of the table that the vector index is created on. |
| index_name | STRING | The name of the vector index. |
| option_name | STRING | The name of the option used in the data definition language statement (DDL) to create the vector index. |
| option_type | STRING | The option data type. |
| option_value | STRING | The option value. |

---

### VIEWS

**Source:** https://cloud.google.com/bigquery/docs/information-schema-views

**Description:** The INFORMATION_SCHEMA.VIEWS view contains metadata about views.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| TABLE_CATALOG | STRING | The name of the project that contains the dataset |
| TABLE_SCHEMA | STRING | The name of the dataset that contains the view also referred to as the dataset id |
| TABLE_NAME | STRING | The name of the view also referred to as the table id |
| VIEW_DEFINITION | STRING | The SQL query that defines the view |
| CHECK_OPTION | STRING | The value returned is always NULL |
| USE_STANDARD_SQL | STRING | YES if the view was created by using a GoogleSQL query; NO if useLegacySql is set to true |

---

### WRITE_API

**Source:** https://cloud.google.com/bigquery/docs/information-schema-write-api

**Description:** The INFORMATION_SCHEMA.WRITE_API_TIMELINE view contains per minute aggregated BigQuery Storage Write API ingestion statistics for the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| start_timestamp | TIMESTAMP | (Partitioning column) Start timestamp of the 1 minute interval for the aggregated statistics. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| dataset_id | STRING | (Clustering column) ID of the dataset. |
| table_id | STRING | (Clustering column) ID of the table. |
| stream_type | STRING | The stream type used for the data ingestion with BigQuery Storage Write API. It is supposed to be one of "DEFAULT", "COMMITTED", "BUFFERED", or "PENDING". |
| error_code | STRING | Error code returned for the requests specified by this row. "OK" for successful requests. |
| total_requests | INTEGER | Total number of requests within the 1 minute interval. |
| total_rows | INTEGER | Total number of rows from all requests within the 1 minute interval. |
| total_input_bytes | INTEGER | Total number of bytes from all rows within the 1 minute interval. |

---

### WRITE_API_BY_FOLDER

**Source:** https://cloud.google.com/bigquery/docs/information-schema-write-api-by-folder

**Description:** The INFORMATION_SCHEMA.WRITE_API_TIMELINE_BY_FOLDER view contains per minute aggregated BigQuery Storage Write API ingestion statistics for the parent folder of the current project, including its subfolders.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| start_timestamp | TIMESTAMP | (Partitioning column) Start timestamp of the 1 minute interval for the aggregated statistics. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| dataset_id | STRING | (Clustering column) ID of the dataset. |
| table_id | STRING | (Clustering column) ID of the table. |
| stream_type | STRING | The stream type used for the data ingestion with BigQuery Storage Write API. It is supposed to be one of "DEFAULT", "COMMITTED", "BUFFERED", or "PENDING". |
| error_code | STRING | Error code returned for the requests specified by this row. "OK" for successful requests. |
| total_requests | INTEGER | Total number of requests within the 1 minute interval. |
| total_rows | INTEGER | Total number of rows from all requests within the 1 minute interval. |
| total_input_bytes | INTEGER | Total number of bytes from all rows within the 1 minute interval. |

---

### WRITE_API_BY_ORGANIZATION

**Source:** https://cloud.google.com/bigquery/docs/information-schema-write-api-by-organization

**Description:** The INFORMATION_SCHEMA.STREAMING_TIMELINE_BY_ORGANIZATION view contains per minute aggregated streaming statistics for the whole organization associated with the current project.

**Schema:**

| Column name | Data type | Value |
| --- | --- | --- |
| start_timestamp | TIMESTAMP | (Partitioning column) Start timestamp of the 1 minute interval for the aggregated statistics. |
| project_id | STRING | (Clustering column) ID of the project. |
| project_number | INTEGER | Number of the project. |
| dataset_id | STRING | (Clustering column) ID of the dataset. |
| table_id | STRING | (Clustering column) ID of the table. |
| stream_type | STRING | The stream type used for the data ingestion with BigQuery Storage Write API. It is supposed to be one of "DEFAULT", "COMMITTED", "BUFFERED", or "PENDING". |
| error_code | STRING | Error code returned for the requests specified by this row. "OK" for successful requests. |
| total_requests | INTEGER | Total number of requests within the 1 minute interval. |
| total_rows | INTEGER | Total number of rows from all requests within the 1 minute interval. |
| total_input_bytes | INTEGER | Total number of bytes from all rows within the 1 minute interval. |

---
