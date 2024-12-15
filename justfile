
# Run tests and pre-commit
default: format test-unit

# Setup project
init:
  python -m pip install -e '.[test]'

# Run unit tests with supplied options
test-unit *options:
  python -m pytest {{options}}

# Update snapshot of unit tests
update-snapshot:
	python -m pytest --snapshot-update

# Run all tests including integration tests
test PROJECT *options:
  python -m pytest --integration --project {{PROJECT}} {{options}}

# Rebuild docs with cog
cog:
  python -m cogapp -r README.md

# Apply pre-commit checks
format: cog
	python -m pre_commit run --all-files --show-diff-on-failure

lint:
  python -m cogapp --check README.md
  python -m pre_commit run --all-files --show-diff-on-failure
