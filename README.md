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
  tables  bigquery meta data table utility

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
Now install the dependencies and test dependencies:
```bash
make install-e
```
To run the unit tests:
```bash
make test
```

Integration tests are skipped by default. To run all tests:
```bash
make test-all project=<project_id>
```
where `<project_id>` is the GCP project id where the tests will be run.


To run pre-commit to lint and format:
```bash
make check
```

`make check` detects if cli help message in `README.md` is outdated and updates it.

To update cli help message `README.md`:
```bash
make readme
```

this runs [cog](https://cog.readthedocs.io/en/latest/) on README.md and updates the help message inside it.
