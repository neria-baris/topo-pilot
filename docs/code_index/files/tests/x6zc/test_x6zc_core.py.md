# `tests/x6zc/test_x6zc_core.py`

- Source: [tests/x6zc/test_x6zc_core.py](../../../../../tests/x6zc/test_x6zc_core.py)
- Kind: python
- Lines: 400

## Module docstring

> Author A (job 0120): X6ZC core tests (TEST_PLAN.md §2) from the protocol copy, API.md, CONTRACT,
> TEST_PLAN and the 0117 review only (tools/x6zc/*.py never read). Expected values: protocol closed
> forms or exact Fractions via reused X6S1 / stage-0 code (on sys.path via zc, API §1); synthetic.

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](../../tools/x6zc/x6zc_core.py.md) (line 19, via sys.path edit)
- `import x6zc_census` -> [tools/x6zc/x6zc_census.py](../../tools/x6zc/x6zc_census.py.md) (line 20, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../../tools/x6_stage0/x6_model.py.md) (line 21, via unique basename)
- `import x6s1_eval` -> [tools/x6_stage1/x6s1_eval.py](../../tools/x6_stage1/x6s1_eval.py.md) (line 22, via unique basename)
- `import x6s1_pairs` -> [tools/x6_stage1/x6s1_pairs.py](../../tools/x6_stage1/x6s1_pairs.py.md) (line 23, via unique basename)
- `import x6s1_stats` -> [tools/x6_stage1/x6s1_stats.py](../../tools/x6_stage1/x6s1_stats.py.md) (line 24, via unique basename)
- `from topo_pilot.contracts import SeedTree, canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 25, via package root)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 4)
- `collections` (lines 10)
- `fractions` (lines 11)
- `hashlib` (lines 6)
- `json` (lines 7)
- `math` (lines 8)
- `pathlib` (lines 12)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 18: `str(REPO / 'tools' / 'x6zc')` -> `tools/x6zc`

## Imported by

- none

## Top-level constants

- `CONTRACT`
- `REPO`
- `W1`

## Classes and functions

- **function `expected_beta`** [L44-56]: `def expected_beta(kind, p, lam) -> tuple`
- **function `pool`** [L61-68]: `def pool()` decorators: @pytest.fixture(scope='module')
- **test `test_pp_equals_x6s1_construction`** [L72-77]: `def test_pp_equals_x6s1_construction()`
- **test `test_variant_arrays_layout`** [L79-89]: `def test_variant_arrays_layout(fam)`
- **test `test_w2_variant_matching`** [L91-102]: `def test_w2_variant_matching()`
- **function `w1_stats`** [L104-108]: `def w1_stats(h) -> tuple`
- **test `test_w1_variant_matching`** [L110-126]: `def test_w1_variant_matching()`
- **test `test_k0_on_pi0_exact`** [L128-146]: `def test_k0_on_pi0_exact(fam)`
- **test `test_k0_answer_table`** [L148-159]: `def test_k0_answer_table()`
- **test `test_k0_detects_violation`** [L161-168]: `def test_k0_detects_violation()`
- **test `test_missed_law`** [L170-177]: `def test_missed_law()`
- **test `test_coupling_table`** [L179-189]: `def test_coupling_table()`
- **test `test_k3_exact_values`** [L191-201]: `def test_k3_exact_values(fam)`
- **test `test_f1_passes`** [L203-205]: `def test_f1_passes(fam)`
- **test `test_partial_composite`** [L207-210]: `def test_partial_composite(fam)`
- **test `test_k3_float_path`** [L212-219]: `def test_k3_float_path(fam)`
- **function `mk_key`** [L221-225]: `def mk_key(h) -> int`
- **test `test_k1_exact_zero`** [L227-247]: `def test_k1_exact_zero(fam)`
- **function `skew_a`** [L249-255]: `def skew_a(tokens, t)`
- **test `test_k1_detects_noninvariance`** [L257-259]: `def test_k1_detects_noninvariance(fam)`
- **test `test_k2_references`** [L261-277]: `def test_k2_references(fam)`
- **test `test_fresh_prefix_continuation`** [L279-299]: `def test_fresh_prefix_continuation(pool, dset)`
- **test `test_qstar_cache_bitwise`** [L301-316]: `def test_qstar_cache_bitwise(tmp_path)`
- **test `test_paired_boot_equals_boot_beta`** [L318-328]: `def test_paired_boot_equals_boot_beta()`
- **test `test_cluster_sums_and_ratio_interval`** [L330-344]: `def test_cluster_sums_and_ratio_interval()`
- **test `test_halfwidth_and_choose_n`** [L346-365]: `def test_halfwidth_and_choose_n()`
- **function `rand_pred`** [L367-372]: `def rand_pred(tokens, t, rng=np.random.default_rng(13))`
- **test `test_d2_identity`** [L376-386]: `def test_d2_identity()`
- **test `test_audit_pairs`** [L388-400]: `def test_audit_pairs(dset)`

