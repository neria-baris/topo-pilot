# `tools/hwsu/hwsu_driver_of.py`

- Source: [tools/hwsu/hwsu_driver_of.py](../../../../../tools/hwsu/hwsu_driver_of.py)
- Kind: python
- Lines: 160

## Module docstring

> HWSU job OF: gate context, run_of and the CLI (API.md §9; protocol §4.2, §5).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 5, via same directory)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](hwsu_of.py.md) (line 6, via same directory)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](hwsu_records.py.md) (line 7, via same directory)
- `import hwsu_seed` -> [tools/hwsu/hwsu_seed.py](hwsu_seed.py.md) (line 8, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 14, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 15, via unique basename)
- `import hwsu_bind` -> [tools/hwsu/hwsu_bind.py](hwsu_bind.py.md) (line 143, via same directory) (inside a function)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 151, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 3)
- `json` (lines 9)
- `pathlib` (lines 12)
- `sys` (lines 10)
- `time` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_a_of_gates.py](../../tests/hwsu/test_a_of_gates.py.md) (line 18, import)
- [tests/hwsu/test_a_of_ladder.py](../../tests/hwsu/test_a_of_ladder.py.md) (line 14, import)
- [tests/hwsu/test_a_of_oracle.py](../../tests/hwsu/test_a_of_oracle.py.md) (line 17, import)
- [tests/hwsu/test_b_of_driver.py](../../tests/hwsu/test_b_of_driver.py.md) (line 20, import)
- [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 8, import)
- [tools/hwsu/u2/hwsu_driver.py](u2/hwsu_driver.py.md) (line 10, import)

## Top-level constants

- `ORDER`
- `PASS_OUTCOMES`

## Classes and functions

- **function `build_ctx`** [L21-26]: `def build_ctx(out, job, attempt, reservation_id, root=uc.ROOT, mailbox=uc.MAILBOX, hwsc_store=uc.HWSC_STORE, scope=uc.SCOPE_OF, seeds=uc.SEEDS_OF, dry=False) -> dict`
- **function `_exit_code`** [L29-38]: `def _exit_code(outcome, gate, rows_drawn) -> int`
- **function `run_of`** [L41-99]: `def run_of(out, job, attempt=1, reservation_id='RES-HWSU-OF', repo=uc.REPO, ledger_path=None, cont=None, ctx=None, dry_continue=False) -> dict`
- **function `_parse`** [L102-111]: `def _parse(argv) -> tuple`
- **function `main`** [L114-156]: `def main(argv=None) -> int`

