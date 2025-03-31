# bqm

[![PyPI](https://img.shields.io/pypi/v/bqm.svg)](https://pypi.org/project/bqm/)
[![Changelog](https://img.shields.io/github/v/release/kj-9/bqm?include_prereleases&label=changelog)](https://github.com/kj-9/bqm/releases)
[![Tests](https://github.com/kj-9/bqm/actions/workflows/ci.yml/badge.svg)](https://github.com/kj-9/bqm/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/kj-9/bqm/blob/master/LICENSE)

Bigquery meta data table utility

## Installation

[uv](https://github.com/astral-sh/uv) is recommended to install this tool:
```bash
uv tool install git+https://github.com/kj-9/bqm
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
  regions  Show all supported regions
  tables   query INFORMATION_SCHEMA.TABLES
  tui      Open Textual TUI.

```
<!-- [[[end]]] -->

You can also use:
```bash
python -m bqm --help
```

## Development

This project uses:
- [uv](https://github.com/astral-sh/uv) to manage the python virtual environment
- [just](https://github.com/casey/just) as task runner

To develop this tool, first checkout the code. Then create a new virtual environment:
```bash
cd bqm
just init
```

this installs `bqm` in editable mode:
```bash
bqm --help
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

add `--snapshot-update` to update the snapshots:
```bash
just test --snapshot-update
```

To run cog and pre-commit to format:
```bash
just fmt
```
This runs [cog](https://cog.readthedocs.io/en/latest/) on README.md and updates the help message inside it.

### Debug in VSCode

To debug in VSCode,
- install the recommended extensions
- set the python interpreter to the virtual environment created by `uv` (`.venv/bin/python`)

For integration tests, update the project name in `.vscode/settings.json`:
```bash

```diff
index 7e19242..1ba076c 100644
--- a/.vscode/settings.json
+++ b/.vscode/settings.json
@@ -1,6 +1,6 @@
 {
     "python.testing.pytestArgs": [
-        "tests", "--integration", "--project=<YOUR_PROJECT_NAME_HERE>"
+        "tests", "--integration", "--project=my-gcp-project"
     ],
     "python.testing.unittestEnabled": false,
     "python.testing.pytestEnabled": true
```
