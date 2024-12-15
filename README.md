# bqm

[![PyPI](https://img.shields.io/pypi/v/bqm.svg)](https://pypi.org/project/bqm/)
[![Changelog](https://img.shields.io/github/v/release/kj-9/bqm?include_prereleases&label=changelog)](https://github.com/kj-9/bqm/releases)
[![Tests](https://github.com/kj-9/bqm/actions/workflows/ci.yml/badge.svg)](https://github.com/kj-9/bqm/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/kj-9/bqm/blob/master/LICENSE)

Bigquery meta data table utility

## Installation

Install this tool using `pip`:
```bash
pip install bqm
```
## Usage

For help, run:
<!-- [[[cog
import cog
from bqm import cli
from click.testing import CliRunner
runner = CliRunner()
result = runner.invoke(cli.cli, ["--help"])
help = result.output.replace("Usage: cli", "Usage: bqm")
cog.out(
    f"```bash\n{help}\n```"
)
]]] -->
```bash
Usage: bqm [OPTIONS] COMMAND [ARGS]...

  Bigquery meta data table utility

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  tables  query __TABLES__
  views   query INFORMATION_SCHEMA.VIEWS

```
<!-- [[[end]]] -->

You can also use:
```bash
python -m bqm --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd bqm
python -m venv venv
source venv/bin/activate
```

As a task runner, this project uses [`just`](https://github.com/casey/just?tab=readme-ov-file).
To install `just` in brew:
```bash
brew install just
```
for other installation methods, refer to the just documentation.


To install the dependencies:
```bash
just init
```
To run the unit tests:
```bash
just test-unit
```

You can pass additional arguments to `pytest`:
```bash
just test-unit -vv
```

Integration tests are skipped by default. To run all tests:
```bash
just test <project_id>
```
where `<project_id>` is the GCP project id where the tests will be run.


To run cog and pre-commit to format:
```bash
just format
```
This runs [cog](https://cog.readthedocs.io/en/latest/) on README.md and updates the help message inside it.
