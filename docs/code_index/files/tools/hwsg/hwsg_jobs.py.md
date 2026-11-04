# `tools/hwsg/hwsg_jobs.py`

- Source: [tools/hwsg/hwsg_jobs.py](../../../../../tools/hwsg/hwsg_jobs.py)
- Kind: python
- Lines: 276

## Module docstring

> HWSG jobs: REG1, E1-w, REG2, E2-w and the CLI (API.md §11.4-§11.7). Every world stage runs
> inside hwsg_bind.world(w); the stage-C gate functions are reused unchanged.

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 6, via same directory)
- `import hwsg_bind` -> [tools/hwsg/hwsg_bind.py](hwsg_bind.py.md) (line 7, via same directory)
- `import hwsg_handoff` -> [tools/hwsg/hwsg_handoff.py](hwsg_handoff.py.md) (line 8, via same directory)
- `import hwsg_known` -> [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 9, via same directory)
- `import hwsg_ratio` -> [tools/hwsg/hwsg_ratio.py](hwsg_ratio.py.md) (line 10, via same directory)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 11, via same directory)
- `import hwsg_registry` -> [tools/hwsg/hwsg_registry.py](hwsg_registry.py.md) (line 12, via same directory)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 17, via unique basename)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 18, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 19, via unique basename)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](../hwsc/hwsc_gates.py.md) (line 20, via unique basename)
- `import hwsc_jobs` -> [tools/hwsc/hwsc_jobs.py](../hwsc/hwsc_jobs.py.md) (line 21, via unique basename)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../hwsc/hwsc_known.py.md) (line 22, via unique basename)
- `import hwsc_outcome` -> [tools/hwsc/hwsc_outcome.py](../hwsc/hwsc_outcome.py.md) (line 23, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 24, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 25, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 26, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 27, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 28, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 30, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 31, via unique basename)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 33, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 34, via package root)
- `import hwsg_cross` -> [tools/hwsg/hwsg_cross.py](hwsg_cross.py.md) (line 240, via same directory) (inside a function)
- `import hwsg_oracle` -> [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 241, via same directory) (inside a function)
- `import hwsg_train` -> [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 242, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 29)

### Standard library

- `__future__` (lines 4)
- `argparse` (lines 13)
- `json` (lines 14)
- `pathlib` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `CACHE`

## Classes and functions

- **function `_store`** [L39-40]: `def _store(wd) -> ArtifactStore`
- **function `_files_under`** [L43-45]: `def _files_under(d) -> set`
- **function `_audit_gate`** [L48-53]: `def _audit_gate(out, tag) -> None`
- **function `_registry_job`** [L57-74]: `def _registry_job(out, auth, sched, stage, version, extra=None, worlds=gc.TAGS) -> dict`
- **function `run_reg1`** [L77-78]: `def run_reg1(out, auth, sched, job=None) -> dict`
- **function `_tables`** [L81-88]: `def _tables(out, tag, blocks=('lgate', 'cal', 'val')) -> dict`
- **function `run_reg2`** [L91-98]: `def run_reg2(out, auth, sched, job=None) -> dict`
- **function `_g0g`** [L102-117]: `def _g0g(wd, out, auth, sched, rel)`
- **function `e1_steps`** [L120-149]: `def e1_steps(out, wd, tag, ctx, handoff, auth, sched) -> list`
- **function `run_e1`** [L152-176]: `def run_e1(out, w, auth, sched, release_path=None, session=None, task_sha256=None, dry_continue=False) -> dict`
- **function `run_e2`** [L180-235]: `def run_e2(out, w, auth, sched, release_path=None, session=None, dry_continue=False) -> dict`
- **function `main`** [L239-272]: `def main(argv=None) -> int`

