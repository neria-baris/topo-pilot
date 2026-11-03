# `tools/hwsg/hwsg_train.py`

- Source: [tools/hwsg/hwsg_train.py](../../../../../tools/hwsg/hwsg_train.py)
- Kind: python
- Lines: 289

## Module docstring

> HWSG parallel training children (API.md §5; protocol §9; G7, DRG12, DRG13, KG4).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 5, via same directory)
- `import hwsg_bind` -> [tools/hwsg/hwsg_bind.py](hwsg_bind.py.md) (line 6, via same directory)
- `import hwsb_registry` -> [tools/hwsb/hwsb_registry.py](../hwsb/hwsb_registry.py.md) (line 15, via unique basename)
- `import hwsb_train` -> [tools/hwsb/hwsb_train.py](../hwsb/hwsb_train.py.md) (line 16, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 17, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 18, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 19, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 20, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 21, via unique basename)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 78, via unique basename) (inside a function)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 79, via unique basename) (inside a function)
- `import hwsg_oracle` -> [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 80, via same directory) (inside a function)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 109, via same directory) (inside a function)
- `import hwsg_handoff` -> [tools/hwsg/hwsg_handoff.py](hwsg_handoff.py.md) (line 134, via same directory) (inside a function)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 135, via same directory) (inside a function)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 202, via same directory) (inside a function)
- `import hwsg_oracle` -> [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 222, via same directory) (inside a function)
- `from topo_pilot.contracts import ArtifactStore, SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 223, via package root) (inside a function)
- `from topo_pilot.contracts.backends import MemoryBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 224, via package root) (inside a function)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 226, via unique basename) (inside a function)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../hwsb/hwsb_data.py.md) (line 227, via unique basename) (inside a function)
- `from topo_pilot.contracts import ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 240, via package root) (inside a function)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 241, via package root) (inside a function)

### External (third-party)

- `psutil` (lines 48, 57)

### Standard library

- `__future__` (lines 3)
- `argparse` (lines 7)
- `dataclasses` (lines 248)
- `json` (lines 8)
- `os` (lines 9)
- `pathlib` (lines 13)
- `subprocess` (lines 10)
- `sys` (lines 11)
- `time` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsg/test_impl_review.py](../../tests/hwsg/test_impl_review.py.md) (line 17, import)
- [tools/hwsg/hwsg_dry2.py](hwsg_dry2.py.md) (line 11, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 237, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 166, import)

## Top-level constants

- `RES`

## Classes and functions

- **function `_tools_path`** [L27-28]: `def _tools_path() -> str`
- **function `child_env`** [L31-37]: `def child_env(job, out, master=0) -> dict`
- **function `child_argv`** [L40-43]: `def child_argv(w, master, out, job, attempt, sub='child') -> list`
- **function `ram_ok`** [L46-52]: `def ram_ok(n_children=3, free_bytes=None) -> dict`
- **function `_peak_rss`** [L55-62]: `def _peak_rss()`
- **function `_files_under`** [L65-67]: `def _files_under(d) -> set`
- **function `child`** [L70-126]: `def child(world_key, master, out, job, attempt) -> dict`
- **function `_next_attempt`** [L129-130]: `def _next_attempt(wd, master) -> int`
- **function `run_train`** [L133-198]: `def run_train(out, w, auth, sched, kc_accept, job, launcher=None) -> dict`
- **function `aggregate`** [L201-217]: `def aggregate(world_dir, job, ledger_path) -> dict`
- **function `kg4_child`** [L220-259]: `def kg4_child(master, out, steps=100, persist=True) -> dict` - One one-thread 100-step training on dry data of a dry master (KG4); writes the checksums.
- **function `_launch_kill`** [L262-269]: `def _launch_kill(out) -> bool` - Start a dry child and kill it at once (DRG12): it must leave no record.
- **function `main`** [L272-285]: `def main(argv=None) -> int`

