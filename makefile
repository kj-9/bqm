.PHONY: install
install:
	python -m pip install '.[test]'

.PHONY: install-e
install-e:
	python -m pip install -e '.[test]'

.PHONY: pre-commit-update
pre-commit-update:
	python -m pre_commit autoupdate

.PHONY: readme
readme:
	python -m cogapp -r README.md

.PHONY:
check:
	python -m pre_commit run --all-files --show-diff-on-failure && python -m cogapp --check README.md

.PHONY: test
test:
	python -m pytest
