.ONESHELL:
SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

VENV ?= .venv
PY   := $(VENV)/bin/python
PIP  := $(VENV)/bin/pip

.PHONY: venv test clean

venv:
	test -x "$(PY)" || python3 -m venv "$(VENV)"
	"$(PIP)" install -U pip
	"$(PIP)" install -e .

test: venv
	"$(PY)" -m unittest discover -s tests/unit -p "test_*.py" -v

clean:
	rm -rf "$(VENV)" .pytest_cache .coverage
	find . -type d -name "__pycache__" -print0 | xargs -0r rm -rf
