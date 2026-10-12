# Repository tasks. make is not installed on Windows; use .\tasks.ps1 there instead.
PY ?= .venv/Scripts/python.exe
BIN ?= .venv/Scripts

.PHONY: test affected checks reproduce-figures lock

test:
ifndef m
	$(error usage: make test m=<module>)
endif
	$(PY) -m pytest tests/$(m) -q

affected:
	$(PY) tools/affected_tests.py --changed $(shell git diff --name-only HEAD)

checks:
	$(PY) tools/check_imports.py
	$(PY) tools/check_file_sizes.py
	$(PY) tools/check_state_files.py

reproduce-figures:
	$(BIN)/topo-pilot report

lock:
	$(PY) -m pip freeze --exclude-editable > requirements.lock
