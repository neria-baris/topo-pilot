# `tools/hwsd/hwsd_known2.py`

- Source: [tools/hwsd/hwsd_known2.py](../../../../../tools/hwsd/hwsd_known2.py)
- Kind: python
- Lines: 252

## Module docstring

> HWSD known cases KD2 (binding mirrors) and KD3 (stage-C reproduction) with their helpers
> (API.md §9; split from hwsd_known by size, API erratum; hwsd_known re-exports every name).

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 6, via same directory)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](../hwsc/hwsc_bind.py.md) (line 14, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 15, via unique basename)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../hwsc/hwsc_known.py.md) (line 16, via unique basename)
- `import hwsd_bind` -> [tools/hwsd/hwsd_bind.py](hwsd_bind.py.md) (line 17, via same directory)
- `import hwsd_data` -> [tools/hwsd/hwsd_data.py](hwsd_data.py.md) (line 18, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 19, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 20, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 21, via unique basename)
- `import k4b_decoder` -> [tools/k4b/k4b_decoder.py](../k4b/k4b_decoder.py.md) (line 22, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 23, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 24, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 25, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 27, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 28, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)
- `from topo_pilot.contracts.backends import MemoryBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 31, via package root)
- `import hwsd_dry` -> [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 50, via same directory) (inside a function)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](hwsd_score.py.md) (line 51, via same directory) (inside a function)
- `import c1_chart` -> [tools/c1prime/c1_chart.py](../c1prime/c1_chart.py.md) (line 72, via unique basename) (inside a function)
- `import hwsd_score` -> [tools/hwsd/hwsd_score.py](hwsd_score.py.md) (line 182, via same directory) (inside a function)
- `import c1_chart` -> [tools/c1prime/c1_chart.py](../c1prime/c1_chart.py.md) (line 199, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 26)

### Standard library

- `__future__` (lines 4)
- `contextlib` (lines 7)
- `fractions` (lines 11)
- `importlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 12)
- `tempfile` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 96: `dynamic: r['module']`
- `import_module` line 107: `dynamic: m`

### sys.path additions

- none

## Imported by

- [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 37, import)

## Top-level constants

- `KNOWN`

## Classes and functions

- **function `_canon`** [L37-46]: `def _canon(x)`
- **function `_fixture_calls`** [L49-84]: `def _fixture_calls(tmp) -> dict`
- **function `kd2`** [L87-110]: `def kd2() -> dict`
- **function `c0_val_line`** [L114-126]: `def c0_val_line(gates_path) -> dict`
- **function `_write_guard`** [L130-158]: `def _write_guard(hwsc)` decorators: @contextlib.contextmanager - Decision 13: refuse any write under hwsc while KD3 runs.
- **function `_npz`** [L161-163]: `def _npz(path) -> dict`
- **function `_same`** [L166-169]: `def _same(a, b) -> bool`
- **function `_val`** [L172-173]: `def _val(x)`
- **function `_load_table`** [L176-178]: `def _load_table(hwsc, stage, name, split) -> dict`
- **function `repro_c`** [L181-250]: `def repro_c(out, hwsc=dc.HWSC_STORE) -> dict`

