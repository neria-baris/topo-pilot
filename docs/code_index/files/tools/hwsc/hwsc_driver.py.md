# `tools/hwsc/hwsc_driver.py`

- Source: [tools/hwsc/hwsc_driver.py](../../../../../tools/hwsc/hwsc_driver.py)
- Kind: python
- Lines: 256

## Module docstring

> HWSC driver: the jobs KC, TRAIN, E1, REG2, E2, close and the CLI (API.md §7.3, §11; protocol
> §5, §8). Records, gate runner, budget and export live in hwsc_records (split by size) and are
> re-exported here under their API names. Every stage function runs inside bound_stage_c().

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 7, via same directory)
- `import hwsb_registry` -> [tools/hwsb/hwsb_registry.py](../hwsb/hwsb_registry.py.md) (line 12, via unique basename)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../hwsb/hwsb_train.py.md) (line 13, via unique basename)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](hwsc_bind.py.md) (line 14, via same directory)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](hwsc_data.py.md) (line 15, via same directory)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](hwsc_gates.py.md) (line 16, via same directory)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 17, via same directory)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 18, via same directory)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 19, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 20, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 21, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 22, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 23, via unique basename)
- `from hwsc_records import auth_ok, central, export_c, freeze_c, implementation_files, ledger_append, ledger_read, lineage_c, pause_check_c, pause_or_raise_c, preflight, run_gates_c, s0, sched_ok, status_of, utc, verify_freeze_c` -> [tools/hwsc/hwsc_records.py](hwsc_records.py.md) (line 24, via same directory)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 29, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 30, via package root)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 177, via unique basename) (inside a function)
- `from hwsc_jobs import e2_context, main, run_close, run_e2` -> [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 253, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 5)
- `json` (lines 8)
- `pathlib` (lines 10)
- `time` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_b_records.py](../../tests/hwsc/test_b_records.py.md) (line 29, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 27, import)
- [tests/hwsc/test_r_0181_kc_records_rehearsal.py](../../tests/hwsc/test_r_0181_kc_records_rehearsal.py.md) (line 17, import)
- [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 99, import)
- [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 148, import)
- [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 84, import)
- [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 250, import)

## Top-level constants

- `E1_GATES`
- `REFUSE`

## Classes and functions

- **function `_store`** [L37-38]: `def _store(out) -> ArtifactStore`
- **function `_files_under`** [L41-43]: `def _files_under(d) -> set`
- **function `_audit_gate`** [L46-52]: `def _audit_gate(out) -> None`
- **function `run_kc`** [L56-70]: `def run_kc(out, auth, sched, job) -> dict`
- **function `run_train`** [L74-136]: `def run_train(out, auth, sched, master, kc_accept, cont=None, plan=None) -> dict`
- **function `obs_inventory`** [L139-149]: `def obs_inventory(out) -> dict`
- **function `_reg`** [L153-161]: `def _reg(out, version, handoff, extra=None) -> dict`
- **function `e1_steps`** [L164-201]: `def e1_steps(out, ctx, handoff, auth, sched) -> list`
- **function `run_e1`** [L204-221]: `def run_e1(out, auth, sched, release_path, session, task_sha256, cont=None, dry_continue=False) -> dict`
- **function `run_reg2`** [L225-250]: `def run_reg2(out, auth, sched, accept) -> dict`

