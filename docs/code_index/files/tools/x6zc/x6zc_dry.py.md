# `tools/x6zc/x6zc_dry.py`

- Source: [tools/x6zc/x6zc_dry.py](../../../../../tools/x6zc/x6zc_dry.py)
- Kind: python
- Lines: 278

## Module docstring

> X6ZC stage 0: the synthetic dry run of every CONTRACT fixture through the pipeline
> (X6ZC-DESIGN-v1 §12; API.md §15, §20 C-52). Synthetic data only.

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](x6zc_core.py.md) (line 13, via same directory)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../x6_stage1/x6s1_eval.py.md) (line 17, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../x6_stage1/x6s1_pairs.py.md) (line 18, via unique basename)
- `import x6zc_census` -> [tools/x6zc/x6zc_census.py](x6zc_census.py.md) (line 19, via same directory)
- `from x6zc_pipeline import predict_variants, stage_c_statistics, decide_report` -> [tools/x6zc/x6zc_pipeline.py](x6zc_pipeline.py.md) (line 22, via same directory)
- `from x6zc_store import _utc, _sha, _norm, _cj, xwrite, ledger_cpu, pause_check` -> [tools/x6zc/x6zc_store.py](x6zc_store.py.md) (line 25, via same directory)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 53, via unique basename) (inside a function)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../x6_stage0/x6_model.py.md) (line 62, via unique basename) (inside a function)
- `import x6s1_cloud` -> [tools/x6_stage1/x6s1_cloud.py](../x6_stage1/x6s1_cloud.py.md) (line 80, via unique basename) (inside a function)
- `import x6s1_data` -> [tools/x6_stage1/x6s1_data.py](../x6_stage1/x6s1_data.py.md) (line 81, via unique basename) (inside a function)
- `from topo_pilot.learner import TransformerLM` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 83, via package root) (inside a function)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../x6_stage1/x6s1_stats.py.md) (line 253, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 16)
- `torch` (lines 79)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 10)
- `io` (lines 7)
- `math` (lines 8)
- `pathlib` (lines 11)
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

- [tools/x6zc/x6zc_run.py](x6zc_run.py.md) (line 30, import)

## Top-level constants

- none

## Classes and functions

- **class `Planted`** [L33-51] - p = Z + sum_k f_k(prefix) (P_k - Z), Z = q*_ZC, P_k a SyntheticPredictor selected by
- **method `Planted.__init__`** [L37-38]: `def __init__(self, name, comps, paths)`
- **method `Planted.__call__`** [L39-48]: `def __call__(self, tokens, t)`
- **method `Planted._info`** [L49-51]: `def _info(self, row, t)`
- **function `sd_parse`** [L52-54]: `def sd_parse(row) -> dict`
- **function `_jitter`** [L55-60]: `def _jitter(prefixes, fid) -> dict`
- **function `_pool`** [L61-69]: `def _pool(gen, rows=4096) -> np.ndarray`
- **function `_ev`** [L70-76]: `def _ev(**kw) -> dict`
- **function `dry`** [L77-277]: `def dry(scratch=zc.DRY_STORE, fixtures=None, faults=None) -> dict` - Stage 0: every CONTRACT dry-run fixture through the pipeline on synthetic data only.
- **function `se_qstar`** [L278-278]: `def se_qstar(tok, t)`

