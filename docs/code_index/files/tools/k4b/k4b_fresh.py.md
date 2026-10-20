# `tools/k4b/k4b_fresh.py`

- Source: [tools/k4b/k4b_fresh.py](../../../../../tools/k4b/k4b_fresh.py)
- Kind: python
- Lines: 389

## Module docstring

> K4b release-B stages: K-REG2, H2-FRESH, T-PRE, ENDPOINT, export (API.md §10).

## Imports

### Internal (repo files)

- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 15, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](k4b_cert.py.md) (line 16, via same directory)
- `import k4b_charts` -> [tools/k4b/k4b_charts.py](k4b_charts.py.md) (line 17, via same directory)
- `import k4b_data` -> [tools/k4b/k4b_data.py](k4b_data.py.md) (line 18, via same directory)
- `import k4b_decoder` -> [tools/k4b/k4b_decoder.py](k4b_decoder.py.md) (line 19, via same directory)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](k4b_driver.py.md) (line 20, via same directory)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](k4b_registry.py.md) (line 21, via same directory)
- `import k4b_release` -> [tools/k4b/k4b_release.py](k4b_release.py.md) (line 22, via same directory)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](k4b_scores.py.md) (line 23, via same directory)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](k4b_stats.py.md) (line 24, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 25, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 27, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 28, via unique basename)
- `from k4b_cert import control_bounds_all` -> [tools/k4b/k4b_cert.py](k4b_cert.py.md) (line 29, via same directory)
- `from k4b_config import MODELS, SEEDS` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 30, via same directory)
- `from k4b_decoder import decoder_agreement` -> [tools/k4b/k4b_decoder.py](k4b_decoder.py.md) (line 31, via same directory)
- `from k4b_scores import control_arrays, support_entries` -> [tools/k4b/k4b_scores.py](k4b_scores.py.md) (line 32, via same directory)
- `from k4b_stats import ratios` -> [tools/k4b/k4b_stats.py](k4b_stats.py.md) (line 33, via same directory)
- `import chart` -> [tools/x4_circle_history/chart.py](../x4_circle_history/chart.py.md) (line 321, via unique basename) (inside a function)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 347, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 26)

### Standard library

- `__future__` (lines 7)
- `argparse` (lines 9)
- `fractions` (lines 12)
- `hashlib` (lines 10)
- `json` (lines 11)
- `pathlib` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/k4b/test_b_endpoint.py](../../tests/k4b/test_b_endpoint.py.md) (line 29, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 26, import)

## Top-level constants

- `ACTS_FILE`
- `AUTHORITY`
- `CONTROL_NAMES`
- `FRESH_ORDER`
- `STEPS`
- `TWO_SIDED`

## Classes and functions

- **function `kreg2_step`** [L44-50]: `def kreg2_step(out, release_b_draft, tables) -> dict` - Identity-only K-REG2 inside the W2 reservation (extra: K4b's cal b0 and val b0 tables).
- **function `require_release_b`** [L53-67]: `def require_release_b(out, release_path, session) -> dict`
- **function `sample_test`** [L70-89]: `def sample_test(out, proc, release, reservation_path) -> dict`
- **function `h2_fresh`** [L92-111]: `def h2_fresh(out, ctx) -> dict`
- **function `t_pre`** [L114-157]: `def t_pre(out, ctx) -> dict` - Oracle + references on every test row; determinism; extension; certificate; fresh B4.
- **function `_plain`** [L160-168]: `def _plain(x)` - JSON-ready copy: Fraction -> str, numpy scalars -> Python; containers recursively.
- **function `_fr`** [L171-174]: `def _fr(x) -> Fraction`
- **function `_keys`** [L177-178]: `def _keys(entries) -> list`
- **function `bootstrap_inputs`** [L181-196]: `def bootstrap_inputs(arrays, controls) -> dict` - The one ordered dict of the single 610103 bootstrap (API.md §14.2).
- **function `_tm`** [L199-200]: `def _tm(x) -> float`
- **function `control_summary`** [L203-230]: `def control_summary(draws, controls, bounds_all) -> dict` - Per entry: point, central 95%, alpha / 1-alpha bounds, max B, certified; no status (R22).
- **function `init_qualifier`** [L233-237]: `def init_qualifier(init_entry, L_init, F_init)` - §9.3, R21: L-_init - F_init > 1/100, strict and exact.
- **function `endpoint`** [L240-285]: `def endpoint(arrays, controls, bounds_all, fresh_b4, Z_bound, decoders, ext, canon32, m, R) -> dict` - API.md §14.3: one joint bootstrap (610103); the RESULT dict with the §11 keys only.
- **function `export`** [L288-298]: `def export(out, result) -> Path`
- **function `_npz`** [L301-303]: `def _npz(path) -> dict`
- **function `load_recorded`** [L306-316]: `def load_recorded(out, stage, name) -> dict` - Arrays of stages/<stage>/<name>, re-hashed against its STAGE_COMPLETE record.
- **function `load_frozen`** [L319-334]: `def load_frozen(out) -> dict` - API.md §14.3: the frozen production charts, step-0 charts and decoders; no refit.
- **function `endpoint_gate`** [L337-343]: `def endpoint_gate(ctx) -> dict`
- **function `main`** [L346-385]: `def main(argv=None) -> int`

