# TEST_PLAN: executors

Marker: `pytest.mark.executors`. Uses a stub stage registered at test time. Budget: under 20 s.

| ID | Test | Kind |
|---|---|---|
| E01 | `LocalExecutor` runs a stub job in a subprocess and imports its output artifact | contract |
| E02 | Bundle round trip: export → unpack in a temp dir → `run_bundle.py` → pack outputs → `fetch` gives the same artifact ids as a local run of the same stub | contract |
| E03 | A tampered output tarball raises `CHECKSUM_MISMATCH`; an unexpected output type is rejected | error path |
| E04 | The exporter refuses to include `configs/local.yaml` or files matching `*token*` | error path |
| E05 | `BundleExecutor.status` returns `awaiting_user` after submit, and `done` after a successful fetch | contract |
| E06 | `NotebookExporter` produces valid nbformat JSON with exactly 3 code cells and no Drive mount calls | contract |
| E07 | Static: no imports of science modules | contract |
