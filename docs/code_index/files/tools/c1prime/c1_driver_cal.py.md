# `tools/c1prime/c1_driver_cal.py`

- Source: [tools/c1prime/c1_driver_cal.py](../../../../../tools/c1prime/c1_driver_cal.py)
- Kind: python
- Lines: 258

## Module docstring

> C1' stage driver, part 2: per-split model work (activations, phases, forced and control
> states, decodes, M2/M3 statistics) and the calibration stage S4 (protocol §16 rows 6-11, §5-§9).
> Implemented in job 0026; never run on data in job 0026.

## Imports

### Internal (repo files)

- `import c1_chart` -> [tools/c1prime/c1_chart.py](c1_chart.py.md) (line 9, via same directory)
- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 10, via same directory)
- `import c1_driver` -> [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 11, via same directory)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](c1_endpoint.py.md) (line 12, via same directory)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](c1_fit.py.md) (line 13, via same directory)
- `import c1_gates` -> [tools/c1prime/c1_gates.py](c1_gates.py.md) (line 14, via same directory)
- `import c1_model` -> [tools/c1prime/c1_model.py](c1_model.py.md) (line 15, via same directory)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](c1_oracle.py.md) (line 16, via same directory)
- `import chart` -> [tools/x4_circle_history/chart.py](../x4_circle_history/chart.py.md) (line 17, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 19, via unique basename)
- `from c1_records import C1GateFailure, begin_stage` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 20, via same directory)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 28, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 18)

### Standard library

- `__future__` (lines 5)
- `json` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 14, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 14, import)

## Top-level constants

- `CFG`
- `MODELS`

## Classes and functions

- **function `load_checkpoint`** [L26-33]: `def load_checkpoint(ctx, model)`
- **function `reload_oracle`** [L36-42]: `def reload_oracle(ctx, split) -> dict`
- **function `model_rows`** [L45-50]: `def model_rows(ctx, model64, perm, r) -> dict` - Natural and donor activations (named tokens), logits discarded unread.
- **function `phases`** [L53-55]: `def phases(prod, gauge, A, timed=None)`
- **function `split_states`** [L58-68]: `def split_states(ctx, m, fit, white, prod, gauge, rows, r, elig, frames) -> dict` - phi, forced and control states, decodes and support for one model on one split.
- **function `damage_support`** [L71-98]: `def damage_support(ctx, st, dec, fit, white, zt, zt_p, zt_m, w32, nu_p, nu_m, q99_, trcov, prod, gauge, active) -> dict` - M2 and M3 statistics on the eligible rows of one split (activations only, no logits).
- **function `decoder_targets`** [L101-104]: `def decoder_targets(r, coords) -> dict`
- **function `run_calibration`** [L107-226]: `def run_calibration(ctx) -> None`
- **function `_per_model`** [L229-232]: `def _per_model(stats, key) -> dict`
- **function `save_fit`** [L235-241]: `def save_fit(ctx, m, mm, q99_, mean, scale, trcov) -> None`
- **function `load_fit`** [L244-258]: `def load_fit(ctx, m) -> dict`

