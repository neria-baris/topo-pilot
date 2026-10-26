# `tools/hws/hws_dry.py`

- Source: [tools/hws/hws_dry.py](../../../../../tools/hws/hws_dry.py)
- Kind: python
- Lines: 329

## Module docstring

> HWS synthetic dry run: the decision, records and meter cases DR9-DR13, the R-0118-1 design
> check and run_dry with the DRY_REPORT writer (protocol §13, TEST_PLAN §4). Split from hws_driver
> by size (erratum E16); hws_driver.run_dry delegates here. Planted decision fixtures are labelled
> "fixture": true and never enter hist/; running the dry run is a separate metered job.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](hws_worlds.py.md) (line 13, via same directory)
- `import hws_driver` -> [tools/hws/hws_driver.py](hws_driver.py.md) (line 14, via same directory)
- `import hws_exact` -> [tools/hws/hws_exact.py](hws_exact.py.md) (line 15, via same directory)
- `import hws_known` -> [tools/hws/hws_known.py](hws_known.py.md) (line 16, via same directory)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](hws_oracle.py.md) (line 17, via same directory)
- `import hws_records` -> [tools/hws/hws_records.py](hws_records.py.md) (line 18, via same directory)
- `import hws_select` -> [tools/hws/hws_select.py](hws_select.py.md) (line 19, via same directory)
- `import hws_stats` -> [tools/hws/hws_stats.py](hws_stats.py.md) (line 20, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 22, via unique basename)
- `from hws_known import TINY, KNOWN, _dry` -> [tools/hws/hws_known.py](hws_known.py.md) (line 23, via same directory)
- `from topo_pilot.dataset.sampler import HMMSampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 24, via package root)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../x4_oracle_profile/controls.py.md) (line 169, via unique basename) (inside a function)
- `import hws_meter_bind` -> [tools/hws/hws_meter_bind.py](hws_meter_bind.py.md) (line 170, via same directory) (inside a function)
- `import k4b_meter_bind` -> [tools/k4b/k4b_meter_bind.py](../k4b/k4b_meter_bind.py.md) (line 171, via unique basename) (inside a function)
- `import meter` -> [tools/x4_oracle_profile/meter.py](../x4_oracle_profile/meter.py.md) (line 172, via unique basename) (inside a function)
- `import winjob` -> [tools/x4_oracle_profile/winjob.py](../x4_oracle_profile/winjob.py.md) (line 173, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 10)
- `math` (lines 9)
- `pathlib` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hws/hws_driver.py](hws_driver.py.md) (line 204, import)

## Top-level constants

- `CASES`
- `FIX`

## Classes and functions

- **function `_b`** [L27-29]: `def _b(mean, se=0.001) -> dict`
- **function `_fx`** [L32-42]: `def _fx(W, q, s, p, d4=0.05, gc=0.3, g4=0.05, g4a=0.05, elig='ELIGIBLE', se=0.001) -> dict` - A planted decision fixture (labelled), classified by hws_select under FIX floors.
- **function `_oc`** [L48-58]: `def _oc(recs, ordinary=(), fallback=(), quals=(), below=(), complete=True, fail=None) -> str`
- **function `dr9`** [L61-110]: `def dr9(out)`
- **function `dr10`** [L113-131]: `def dr10(out)`
- **function `_ref_m`** [L134-148]: `def _ref_m(T, E, pi, tok, K, c, trap=None) -> np.ndarray` - Independent suffix filter (restart from pi, emit first) and its five alignment traps.
- **function `dr11`** [L151-165]: `def dr11(out)`
- **function `dr12`** [L168-240]: `def dr12(out)`
- **function `dr13`** [L243-264]: `def dr13(out)`
- **function `design_checks`** [L267-279]: `def design_checks() -> dict` - R-0118-1: the exact p-weighted SD of H(r_w) under the rebuilt w0 spec (a note).
- **function `run_dry`** [L305-329]: `def run_dry(out=hw.DRY_STORE) -> dict` - §13 synthetic dry run with the real records, selection and report code (J1 AUTH).

