# `tools/x4_circle_history/runner.py`

- Source: [tools/x4_circle_history/runner.py](../../../../../tools/x4_circle_history/runner.py)
- Kind: python
- Lines: 344

## Module docstring

> Future feasibility stage driver (job 0016 builds it; it never runs a scientific stage here).

## Imports

### Internal (repo files)

- `import stage_records` -> [tools/x4_circle_history/stage_records.py](stage_records.py.md) (line 29, via same directory)
- `from errors import AccessDenied, Invalid, JoinError, Unresolved` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 30, via same directory)
- `from stage_records import gates_so_far, record_gate` -> [tools/x4_circle_history/stage_records.py](stage_records.py.md) (line 31, via same directory)
- `from adapter import RestrictedE4Adapter` -> [tools/x4_circle_history/adapter.py](adapter.py.md) (line 51, via same directory) (inside a function)
- `from scores import canonical_from_named` -> [tools/x4_circle_history/scores.py](scores.py.md) (line 52, via same directory) (inside a function)
- `from adapter import RestrictedE4Adapter, cross_model_join` -> [tools/x4_circle_history/adapter.py](adapter.py.md) (line 65, via same directory) (inside a function)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](error_bound.py.md) (line 86, via same directory) (inside a function)
- `from reference_cache import row_record` -> [tools/x4_circle_history/reference_cache.py](reference_cache.py.md) (line 87, via same directory) (inside a function)
- `from scores import oracle_moments` -> [tools/x4_circle_history/scores.py](scores.py.md) (line 88, via same directory) (inside a function)
- `import process_law` -> [tools/x4_circle_history/process_law.py](process_law.py.md) (line 115, via same directory) (inside a function)
- `import reference_cache` -> [tools/x4_circle_history/reference_cache.py](reference_cache.py.md) (line 116, via same directory) (inside a function)
- `import reference_cache` -> [tools/x4_circle_history/reference_cache.py](reference_cache.py.md) (line 151, via same directory) (inside a function)
- `from reference_cache import verify_rows` -> [tools/x4_circle_history/reference_cache.py](reference_cache.py.md) (line 171, via same directory) (inside a function)
- `import chart` -> [tools/x4_circle_history/chart.py](chart.py.md) (line 185, via same directory) (inside a function)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](error_bound.py.md) (line 186, via same directory) (inside a function)
- `from scores import scores, unit_vectors` -> [tools/x4_circle_history/scores.py](scores.py.md) (line 187, via same directory) (inside a function)
- `import precision_stage` -> [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 283, via same directory) (inside a function)
- `import precision_stage` -> [tools/x4_circle_history/precision_stage.py](precision_stage.py.md) (line 292, via same directory) (inside a function)
- `import release` -> [tools/x4_circle_history/release.py](release.py.md) (line 313, via same directory) (inside a function)
- `import live_context` -> [tools/x4_circle_history/live_context.py](live_context.py.md) (line 327, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 13)
- `argparse` (lines 311)
- `dataclasses` (lines 17)
- `json` (lines 15)
- `pathlib` (lines 18)
- `sys` (lines 16)
- `typing` (lines 19)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `str(extra)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tests/circle_history/test_builder_e2e.py](../../tests/circle_history/test_builder_e2e.py.md) (line 25, import)
- [tests/circle_history/test_builder_runtime.py](../../tests/circle_history/test_builder_runtime.py.md) (line 166, import)
- [tests/circle_history/test_builder_v24_stages.py](../../tests/circle_history/test_builder_v24_stages.py.md) (line 19, import)
- [tools/x4_circle_history/live_context.py](live_context.py.md) (line 97, import)

## Top-level constants

- `HERE`
- `REPO`
- `SPLITS`
- `STAGES`
- `STAGE_ORDER`

## Classes and functions

- **class `Context`** [L38-47] decorators: @dataclass
- **function `_panel_rows`** [L50-57]: `def _panel_rows(ctx: Context, model: int) -> dict`
- **function `_ptuple`** [L60-61]: `def _ptuple(p)`
- **function `stage_identity`** [L64-82]: `def stage_identity(ctx: Context) -> dict`
- **function `_oracle_split`** [L85-111]: `def _oracle_split(ctx, model, split, panel, d, cache)`
- **function `stage_oracle`** [L114-146]: `def stage_oracle(ctx: Context) -> dict`
- **function `_load_reference`** [L149-161]: `def _load_reference(ctx: Context) -> tuple[dict, dict]` - Verified (cache file object, cache) of the oracle stage; no recomputation (item 9).
- **function `_load_npz`** [L164-166]: `def _load_npz(path: Path) -> dict`
- **function `_check_alignment`** [L169-181]: `def _check_alignment(model, data, orc, ref_obj) -> None` - Saved oracle IDs must equal the reloaded rows EXACTLY (Invalid -> FAIL_TECHNICAL).
- **function `_chart_model`** [L184-256]: `def _chart_model(ctx, model, cfg, ref_obj, ref_cache, budget) -> dict`
- **function `stage_charts`** [L259-279]: `def stage_charts(ctx: Context) -> dict`
- **function `stage_precision`** [L282-288]: `def stage_precision(ctx: Context) -> dict`
- **function `stage_export`** [L291-298]: `def stage_export(ctx: Context) -> dict`
- **function `main`** [L310-340]: `def main(argv=None) -> int`

