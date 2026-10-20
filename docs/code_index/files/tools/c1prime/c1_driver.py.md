# `tools/c1prime/c1_driver.py`

- Source: [tools/c1prime/c1_driver.py](../../../../../tools/c1prime/c1_driver.py)
- Kind: python
- Lines: 324

## Module docstring

> C1' stage driver, part 1: context, gate runner, G0 and the oracle stage S3 (API.md §15;
> protocol §16 rows 0-5, §2-§4, §15.3). Implemented in job 0026; never run on data in job 0026.
> Usage (venv, through c1_meter_bind.py --release R): python c1_driver.py <stage> <release.json>

## Imports

### Internal (repo files)

- `import c1_cert` -> [tools/c1prime/c1_cert.py](c1_cert.py.md) (line 13, via same directory)
- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 14, via same directory)
- `import c1_data` -> [tools/c1prime/c1_data.py](c1_data.py.md) (line 15, via same directory)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](c1_oracle.py.md) (line 16, via same directory)
- `import c1_release` -> [tools/c1prime/c1_release.py](c1_release.py.md) (line 17, via same directory)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../x4_circle_history/error_bound.py.md) (line 18, via unique basename)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 20, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 21, via unique basename)
- `from c1_records import C1Stop, LogitPolicy, begin_stage, run_c1_gate` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 22, via same directory)
- `import controls` -> [tools/x4_oracle_profile/controls.py](../x4_oracle_profile/controls.py.md) (line 40, via unique basename) (inside a function)
- `import c1_freeze` -> [tools/c1prime/c1_freeze.py](c1_freeze.py.md) (line 53, via same directory) (inside a function)
- `import inputs` -> [tools/x4_oracle_profile/inputs.py](../x4_oracle_profile/inputs.py.md) (line 105, via unique basename) (inside a function)
- `from oracle_profile import canonical_emission` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 106, via unique basename) (inside a function)
- `from topo_pilot.dataset.checks import check_disjoint` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 149, via package root) (inside a function)
- `from c1_bounds import row_certificate` -> [tools/c1prime/c1_bounds.py](c1_bounds.py.md) (line 229, via same directory) (inside a function)
- `from c1_bounds import row_certificate` -> [tools/c1prime/c1_bounds.py](c1_bounds.py.md) (line 263, via same directory) (inside a function)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](c1_endpoint.py.md) (line 278, via same directory) (inside a function)
- `import c1_driver_late` -> [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 314, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 19)

### Standard library

- `__future__` (lines 5)
- `dataclasses` (lines 9)
- `fractions` (lines 10)
- `json` (lines 7)
- `pathlib` (lines 11)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_c_process_keys.py](../../tests/c1prime/test_c_process_keys.py.md) (line 22, import)
- [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 11, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 13, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 13, import)

## Top-level constants

- `MODELS`
- `ROOT`

## Classes and functions

- **class `Ctx`** [L29-36] decorators: @dataclass
- **function `_guard`** [L39-49]: `def _guard(rel, out)`
- **function `make_context`** [L52-61]: `def make_context(release_path) -> Ctx`
- **function `gate`** [L64-69]: `def gate(ctx, name, fn, chart=False)`
- **function `_sha`** [L72-73]: `def _sha(path) -> str`
- **function `g0`** [L77-100]: `def g0(ctx) -> dict`
- **function `_process`** [L104-119]: `def _process(ctx) -> dict`
- **function `h1`** [L122-136]: `def h1(ctx) -> dict`
- **function `sample_s3`** [L139-145]: `def sample_s3(ctx) -> None`
- **function `h2`** [L148-164]: `def h2(ctx) -> dict`
- **function `oracle_split`** [L167-179]: `def oracle_split(ctx, split) -> dict`
- **function `eligibility`** [L182-189]: `def eligibility(ctx) -> None`
- **function `_rel_rows`** [L192-193]: `def _rel_rows(xh, xr, tol_) -> bool`
- **function `h3`** [L196-224]: `def h3(ctx, splits=('cal', 'val')) -> dict`
- **function `_h3_decimal`** [L227-251]: `def _h3_decimal(ctx, r, split, prior) -> str`
- **function `h4`** [L254-259]: `def h4(ctx) -> dict`
- **function `n0`** [L262-274]: `def n0(ctx) -> dict`
- **function `h5`** [L277-281]: `def h5(ctx) -> dict`
- **function `run_oracle_stage`** [L284-304]: `def run_oracle_stage(ctx) -> None`
- **function `main`** [L307-320]: `def main() -> int`

