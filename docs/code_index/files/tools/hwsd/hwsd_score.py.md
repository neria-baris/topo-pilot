# `tools/hwsd/hwsd_score.py`

- Source: [tools/hwsd/hwsd_score.py](../../../../../tools/hwsd/hwsd_score.py)
- Kind: python
- Lines: 393

## Module docstring

> HWSD per-checkpoint scorer (API.md section 6 and section 16): learning, chart_one, arrays_one,
> controls_one, statuses, determinism, acceptance. Reused functions are called through their module
> attributes at call time, so the binding applies.

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 7, via same directory)
- `import c1_chart` -> [tools/c1prime/c1_chart.py](../c1prime/c1_chart.py.md) (line 12, via unique basename)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 13, via unique basename)
- `import c1_records` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 14, via unique basename)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../hwsb/hwsb_eval.py.md) (line 15, via unique basename)
- `import hwsd_records` -> [tools/hwsd/hwsd_records.py](hwsd_records.py.md) (line 16, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 17, via unique basename)
- `import k4b_charts` -> [tools/k4b/k4b_charts.py](../k4b/k4b_charts.py.md) (line 18, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 19, via unique basename)
- `import k4b_decoder` -> [tools/k4b/k4b_decoder.py](../k4b/k4b_decoder.py.md) (line 20, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 21, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 22, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 24, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 25, via unique basename)

### External (third-party)

- `numpy` (lines 23)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 9)
- `pathlib` (lines 10)
- `re` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_a_learning.py](../../tests/hwsd/test_a_learning.py.md) (line 26, import)
- [tests/hwsd/test_a_scorer.py](../../tests/hwsd/test_a_scorer.py.md) (line 28, import)
- [tests/hwsd/test_b_records_meter.py](../../tests/hwsd/test_b_records_meter.py.md) (line 18, import)
- [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 39, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 30, import)
- [tools/hwsd/hwsd_dry3.py](hwsd_dry3.py.md) (line 40, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 20, import)
- [tools/hwsd/hwsd_known2.py](hwsd_known2.py.md) (line 51, import)
- [tools/hwsd/hwsd_known2.py](hwsd_known2.py.md) (line 182, import)
- [tools/hwsd/hwsd_summary.py](hwsd_summary.py.md) (line 14, import)

## Top-level constants

- `NUMERICAL`
- `STATUSES`

## Classes and functions

- **function `_jsonable`** [L31-40]: `def _jsonable(x)`
- **function `checkpoint_dir`** [L43-44]: `def checkpoint_dir(out, j, step) -> Path`
- **function `ledger_for`** [L47-50]: `def ledger_for(out, j, step)`
- **function `load_checkpoint_d`** [L53-57]: `def load_checkpoint_d(j, step) -> tuple`
- **function `acts_fn`** [L60-62]: `def acts_fn(model64, perm)`
- **function `learning_one`** [L65-75]: `def learning_one(ckpt, canon32, perm, q, z=dc.Z, z_s=dc.Z_S) -> dict`
- **function `_is_wall`** [L78-80]: `def _is_wall(status, reason) -> bool`
- **function `_text`** [L83-87]: `def _text(status, reason) -> str`
- **function `map_build`** [L90-98]: `def map_build(res, where)`
- **function `_exc_status`** [L101-106]: `def _exc_status(exc) -> tuple`
- **function `_sha`** [L109-110]: `def _sha(path) -> str`
- **function `chart_one`** [L113-165]: `def chart_one(j, acts, tables, m32_cal, ledger, cfg, out_dir, timed=None, skip_direct=False)`
- **function `arrays_one`** [L168-187]: `def arrays_one(prod, acts_test, m, refs, eps, cfg, planted=False) -> dict`
- **function `controls_one`** [L190-203]: `def controls_one(m, canon32, ext, decoder) -> dict`
- **function `status_of_checkpoint`** [L206-224]: `def status_of_checkpoint(ch, cert) -> tuple`
- **function `archived_wall`** [L227-251]: `def archived_wall(out, j, step)`
- **function `_write_json`** [L254-255]: `def _write_json(path, obj) -> None`
- **function `score_checkpoint`** [L258-351]: `def score_checkpoint(ctx, j, step, ckpt=None, model64=None, perm=None, acts=None, learn=None)`
- **function `run_checkpoints`** [L354-363]: `def run_checkpoints(ctx, j, pause=None) -> list`
- **function `determinism_d`** [L366-378]: `def determinism_d(ctx, j, records) -> dict`
- **function `acceptance`** [L381-393]: `def acceptance(out, j, job, attempt, records, cpu_s, freeze_sha256) -> dict`

