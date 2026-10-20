# `tools/x6_stage0/x6_store.py`

- Source: [tools/x6_stage0/x6_store.py](../../../../../tools/x6_stage0/x6_store.py)
- Kind: python
- Lines: 250

## Module docstring

> X6 stage 0: labels and outcome (D), S0, store lineage, archive and compare, canonical JSON,
> per-gate records and the preflight record (X6-FROZEN-v1 sections 8.1, 8.3-8.5, 10.5, 10.8;
> API.md 6.2-6.5, 7 choice 21). Moved unchanged in behaviour from x6_run.py (coordinator
> addendum 1, ruling X5); x6_run re-exports every moved name.

## Imports

### Internal (repo files)

- `import x6_model` -> [tools/x6_stage0/x6_model.py](x6_model.py.md) (line 20, via same directory)
- `import x6_dp` -> [tools/x6_stage0/x6_dp.py](x6_dp.py.md) (line 21, via same directory)
- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](x6_exact.py.md) (line 22, via same directory)
- `from x6_model import G_MIN` -> [tools/x6_stage0/x6_model.py](x6_model.py.md) (line 23, via same directory)

### External (third-party)

- `numpy` (lines 18)

### Standard library

- `__future__` (lines 6)
- `decimal` (lines 14)
- `fractions` (lines 15)
- `hashlib` (lines 8)
- `json` (lines 9)
- `os` (lines 10)
- `pathlib` (lines 16)
- `re` (lines 11)
- `shutil` (lines 12)
- `subprocess` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/x6_stage1/test_b_chain_ops.py](../../tests/x6_stage1/test_b_chain_ops.py.md) (line 29, import)
- [tools/x6_stage0/x6_run.py](x6_run.py.md) (line 28, import)
- [tools/x6_stage1/x6s1_run.py](../x6_stage1/x6s1_run.py.md) (line 29, import)

## Top-level constants

- `ALLOWLIST`
- `ATTEMPT_RE`
- `G7_DP_ITEMS`
- `G7_ITEMS`
- `GATES`
- `KERNEL_DIFF_EXPECTED`
- `MAILBOX`
- `METER_FILES`
- `ORDER`
- `OUTCOMES`
- `PF_SUITES`
- `PROTECTED_PATHS`
- `S8_NOT_RUN`
- `VOLATILE_KEYS`

## Classes and functions

- **function `decide`** [L56-76]: `def decide(statuses, o1, o2, s8=None) -> dict`
- **function `label_cert`** [L78-79]: `def label_cert(cert: str, yes: str, no: str) -> str`
- **function `labels`** [L80-91]: `def labels(g3, g4, poe_values) -> dict`
- **function `_git`** [L94-96]: `def _git(wt, *args) -> list`
- **function `allowlist_ok`** [L97-97]: `def allowlist_ok(lines) -> bool`
- **function `kernel_diff_ok`** [L98-99]: `def kernel_diff_ok(lines) -> bool`
- **function `_norm`** [L100-100]: `def _norm(p) -> str`
- **function `s0_check`** [L101-118]: `def s0_check(worktree, head, store, dispatch) -> dict`
- **function `sha256_file`** [L121-121]: `def sha256_file(path) -> str`
- **function `write_manifest`** [L122-127]: `def write_manifest(attempt_dir) -> Path`
- **function `read_manifest`** [L128-130]: `def read_manifest(path) -> dict`
- **function `_lineage`** [L131-158]: `def _lineage(store, s0: bool) -> dict`
- **function `lineage_precheck`** [L159-159]: `def lineage_precheck(store) -> dict`
- **function `s0_lineage`** [L160-160]: `def s0_lineage(store) -> dict`
- **function `archive_attempt`** [L162-176]: `def archive_attempt(store, job: str, ledger_entries=(), logs=()) -> Path`
- **function `compare_attempt`** [L177-187]: `def compare_attempt(attempt_dir, run_dir, affected=()) -> dict`
- **function `_key`** [L189-189]: `def _key(k) -> str`
- **function `jsonable`** [L190-198]: `def jsonable(obj)`
- **function `canonical_json`** [L199-201]: `def canonical_json(obj) -> bytes`
- **function `_volatile`** [L202-203]: `def _volatile(k) -> bool`
- **function `strip_volatile`** [L204-207]: `def strip_volatile(obj)`
- **function `reports_equal`** [L208-208]: `def reports_equal(a, b) -> bool`
- **function `write_marker`** [L209-213]: `def write_marker(run_dir, gate: str) -> None`
- **function `write_gate`** [L214-225]: `def write_gate(run_dir, gate: str, status: str, values) -> dict`
- **function `_load`** [L228-228]: `def _load(path) -> dict`
- **function `scratch_ok`** [L229-230]: `def scratch_ok(path, job) -> bool`
- **function `write_preflight`** [L231-243]: `def write_preflight(store, record: dict) -> dict`
- **function `_typed`** [L244-250]: `def _typed(obj)`

