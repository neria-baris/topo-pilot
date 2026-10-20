# `tests/x2a_stage0/test_x2a_stage0_ph.py`

- Source: [tests/x2a_stage0/test_x2a_stage0_ph.py](../../../../../tests/x2a_stage0/test_x2a_stage0_ph.py)
- Kind: python
- Lines: 296

## Module docstring

> Independent tests of tools/x2a_stage0 (job 0025), part 2: credits, the additive score,
> statistics, decision labels, verdict logic and the PH readings on hand-made inputs.

## Imports

### Internal (repo files)

- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 18, via package root)
- `from topo_pilot.world import WORLD_REGISTRY` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 19, via package root)
- `import x2a_mc` -> [tools/x2a_stage0/x2a_mc.py](../../tools/x2a_stage0/x2a_mc.py.md) (line 29, via sys.path edit)
- `import x2a_ph` -> [tools/x2a_stage0/x2a_ph.py](../../tools/x2a_stage0/x2a_ph.py.md) (line 30, via sys.path edit)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 8)
- `json` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 13)
- `sys` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `str(REPO_ROOT.joinpath(*_parts))` -> `tests/oracle_profile`, `tools/x2a_stage0`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `GATES`
- `INF`
- `REPO_ROOT`

## Classes and functions

- **function `rows`** [L36-37]: `def rows(*bars) -> np.ndarray`
- **function `blockdiag`** [L38-41]: `def blockdiag(a: np.ndarray, b: np.ndarray) -> np.ndarray`
- **function `ref_loglik`** [L42-46]: `def ref_loglik(T, E, pi, w) -> float`
- **function `approx2`** [L47-48]: `def approx2(pair, expected) -> bool`
- **test `test_decision_tie_rule`** [L51-57]: `def test_decision_tie_rule()`
- **test `test_lemma_C_credits`** [L58-75]: `def test_lemma_C_credits()`
- **test `test_additive_score_iid_toy_equals_full_llr`** [L78-90]: `def test_additive_score_iid_toy_equals_full_llr()`
- **test `test_additive_score_uses_disjoint_stationary_blocks`** [L91-104]: `def test_additive_score_uses_disjoint_stationary_blocks()`
- **test `test_entropy_mass_logit_and_expit`** [L107-118]: `def test_entropy_mass_logit_and_expit()`
- **test `test_stratified_se_interval_and_hoeffding`** [L119-129]: `def test_stratified_se_interval_and_hoeffding()`
- **test `test_p3_p4_a3_labels`** [L132-148]: `def test_p3_p4_a3_labels()`
- **test `test_scientific_outcome`** [L149-155]: `def test_scientific_outcome()`
- **function `_st`** [L156-161]: `def _st(bad: str | None = None, status: str = 'FAIL', after: str = 'NOT_RUN') -> dict`
- **test `test_validity_rule`** [L162-170]: `def test_validity_rule()`
- **test `test_released_and_withheld_labels`** [L171-180]: `def test_released_and_withheld_labels()`
- **test `test_q1_and_q2_outcomes`** [L181-195]: `def test_q1_and_q2_outcomes()`
- **test `test_band_select_plateau_intersection`** [L198-206]: `def test_band_select_plateau_intersection()`
- **test `test_band_select_longest_tie_width_and_beta0`** [L207-231]: `def test_band_select_longest_tie_width_and_beta0()`
- **test `test_betti_at_beta1_band_and_k2`** [L232-243]: `def test_betti_at_beta1_band_and_k2()`
- **test `test_clusters_count_original_points_through_dedup_map`** [L244-262]: `def test_clusters_count_original_points_through_dedup_map()`
- **test `test_split_check`** [L263-273]: `def test_split_check()`
- **test `test_h0_star`** [L274-285]: `def test_h0_star()`
- **test `test_run_with_failed_preflight_is_invalid`** [L288-296]: `def test_run_with_failed_preflight_is_invalid(tmp_path)`

