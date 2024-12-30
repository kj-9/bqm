uv_run := "uv run"

# Run tests and pre-commit
default: fmt test-unit

# Setup project
init:
  uv sync --extra test

# Run unit tests with supplied options
test-unit *options:
  {{uv_run}} pytest {{options}}

# Update snapshot of unit tests
update-snapshot:
	{{uv_run}} pytest --snapshot-update

# Run all tests including integration tests
test PROJECT *options:
  {{uv_run}} pytest --integration --project {{PROJECT}} {{options}}

# Rebuild docs with cog
cog:
  {{uv_run}} cog -r README.md

# Apply pre-commit checks
fmt: cog
	{{uv_run}} pre-commit run --all-files --show-diff-on-failure

lint:
  {{uv_run}} cogapp --check README.md
  {{uv_run}} pre-commit run --all-files --show-diff-on-failure
