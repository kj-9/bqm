# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BQM is a BigQuery metadata table utility that provides CLI tools to query and display BigQuery table metadata across different regions and projects. The tool is built in Python using Click for CLI functionality and includes a TUI interface via Trogon.

## Core Architecture

- **bqm/cli.py**: Main CLI module containing command definitions, query execution logic, and output formatting
- **bqm/schema.py**: Contains BigQuery regions configuration
- **bqm/__main__.py**: Entry point for `python -m bqm` execution
- **tests/**: Unit and integration tests with snapshot testing using syrupy

The tool uses Google Cloud BigQuery client library to execute queries against INFORMATION_SCHEMA tables across multiple regions in parallel using asyncio and ThreadPoolExecutor.

## Development Commands

This project uses `uv` for dependency management and `just` as a task runner.

### Setup
```bash
just init  # Sets up virtual environment and installs dependencies
```

### Testing
```bash
just test-unit                    # Run unit tests only
just test-unit -vv               # Run unit tests with verbose output
just test <project_id>           # Run all tests including integration tests
just test --snapshot-update      # Update snapshots
just update-snapshot             # Update unit test snapshots only
```

### Code Quality
```bash
just fmt                         # Run cog + pre-commit on all files
just lint                        # Check cog + run pre-commit without fixing
just cog                         # Update README.md help text using cog
```

### Integration Tests
Integration tests require a GCP project ID and are configured via pytest options:
- Use `--integration` flag to run integration tests
- Use `--project <project_id>` to specify GCP project
- Configure `.vscode/settings.json` with your project for IDE debugging

## Key Implementation Details

- Queries are executed in parallel across multiple BigQuery regions using asyncio
- Results are merged and sorted in Python since cross-region UNION ALL queries are not supported
- Output supports table (Rich), JSON, and CSV formats
- Schema information is preserved from BigQuery results for proper column formatting
- The tool handles timezone conversion and numeric formatting for table output
- Error handling includes graceful degradation when individual region queries fail
