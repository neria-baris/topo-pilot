# `tools/hwsb/hwsb_driver.py`

- Source: [tools/hwsb/hwsb_driver.py](../../../../../tools/hwsb/hwsb_driver.py)
- Kind: python
- Lines: 328

## Module docstring

> HWSB driver: preflight, the KB/TRAIN/EVAL stages, pauses, the study ledger, inventories,
> FREEZE and the CLI (API.md §8, §12, §13; protocol §5, §6.4, §8.2).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 9, via same directory)
- `import hws_records` -> [tools/hws/hws_records.py](../hws/hws_records.py.md) (line 16, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 17, via same directory)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](hwsb_gates.py.md) (line 18, via same directory)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 19, via same directory)
- `import hwsb_stages` -> [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 20, via same directory)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](hwsb_train.py.md) (line 21, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 22, via unique basename)
- `from hwsb_records import freeze, implementation_files, inventory_diff, inventory_snapshot, ledger_append, ledger_read, verify_freeze` -> [tools/hwsb/hwsb_records.py](hwsb_records.py.md) (line 23, via same directory)
- `from hwsb_stages import train_core` -> [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 32, via same directory)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 34, via package root)
- `import hws_worlds` -> [tools/hws/hws_worlds.py](../hws/hws_worlds.py.md) (line 62, via unique basename) (inside a function)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 63, via unique basename) (inside a function)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 64, via unique basename) (inside a function)
- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 66, via package root) (inside a function)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 310, via same directory) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `argparse` (lines 10)
- `fractions` (lines 13)
- `json` (lines 11)
- `pathlib` (lines 14)
- `time` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- `import errors` (line 61): `src/topo_pilot/contracts/errors.py`, `tools/x4_circle_history/errors.py`

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsb/test_b_records.py](../../tests/hwsb/test_b_records.py.md) (line 27, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 21, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 16, import)
- [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 107, import)
- [tools/hwsb/hwsb_known.py](hwsb_known.py.md) (line 282, import)
- [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 77, import)
- [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 304, import)

## Top-level constants

- `C`
- `FREEZE`
- `REFUSE`

## Classes and functions

- **class `Paused(RuntimeError)`** [L41-42] - A 3x trigger fired at an item boundary; nothing new is started (exit 4).
- **function `utc`** [L45-46]: `def utc() -> str`
- **function `_gate`** [L49-50]: `def _gate(out, gate, status, **details) -> str`
- **function `_json`** [L53-56]: `def _json(x)`
- **function `status_of`** [L59-82]: `def status_of(exc) -> str` - Choice 20 exception map.
- **function `auth_ok`** [L88-93]: `def auth_ok(auth, stage) -> dict`
- **function `sched_ok`** [L96-111]: `def sched_ok(sched, stage) -> dict`
- **function `preflight`** [L114-127]: `def preflight(out, stage, auth, sched, repo=hc.REPO) -> dict`
- **function `pause_check`** [L133-145]: `def pause_check(stage, stage_cpu, cum_cpu) -> dict`
- **function `running_cpu`** [L148-152]: `def running_cpu(stage, ledger_path=hc.STUDY_LEDGER, t0=0.0) -> tuple`
- **function `pause_or_raise`** [L155-163]: `def pause_or_raise(out, stage, t0, ledger_path=hc.STUDY_LEDGER, cont=None) -> None` - Both 3x triggers at an item boundary; a continued stage is exempt.
- **function `_store`** [L169-170]: `def _store(out) -> ArtifactStore`
- **function `run_train`** [L173-209]: `def run_train(out, auth, sched, master, kb_accept, cont=None, threads=1) -> dict`
- **function `run_eval`** [L215-246]: `def run_eval(out, auth, sched, cont=None) -> dict`
- **function `run_close`** [L249-258]: `def run_close(out, reason) -> dict`
- **function `main`** [L261-324]: `def main(argv=None) -> int`

