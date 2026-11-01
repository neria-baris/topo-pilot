# `tests/hwsu/test_a_of_gates.py`

- Source: [tests/hwsu/test_a_of_gates.py](../../../../../tests/hwsu/test_a_of_gates.py)
- Kind: python
- Lines: 382

## Module docstring

> Author A (job 0198): the OF gates OF-2 ... OF-5, the outcome rule and the tails report
> (protocol §4.2, §4.3, S3 §4.1; DRO4, DRO5, DRO8) on hand-built gate contexts (API §4).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../../tools/hwsu/hwsu_config.py.md) (line 14, via sys.path edit)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](../../tools/hwsu/hwsu_pairs.py.md) (line 15, via sys.path edit)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](../../tools/hwsu/hwsu_oracle.py.md) (line 16, via sys.path edit)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../../tools/hwsu/hwsu_of.py.md) (line 17, via sys.path edit)
- `import hwsu_driver_of` -> [tools/hwsu/hwsu_driver_of.py](../../tools/hwsu/hwsu_driver_of.py.md) (line 18, via sys.path edit)
- `import hwsu_dry` -> [tools/hwsu/hwsu_dry.py](../../tools/hwsu/hwsu_dry.py.md) (line 19, via sys.path edit)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../tools/c1prime/c1_means.py.md) (line 20, via unique basename)
- `import c1_records` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 21, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../tools/c2_readout/c2_attrib.py.md) (line 22, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../tools/c2_readout/c2_decide.py.md) (line 23, via unique basename)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../../tools/c2_readout/c2_stats.py.md) (line 24, via unique basename)
- `import precision` -> [tools/x4_circle_history/precision.py](../../tools/x4_circle_history/precision.py.md) (line 26, via unique basename)
- `from topo_pilot.dataset import sampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 25)
- `pytest` (lines 27)

### Standard library

- `__future__` (lines 4)
- `fractions` (lines 8)
- `math` (lines 6)
- `pathlib` (lines 9)
- `sys` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 12: `str(REPO / 'tools' / 'hwsu')` -> `tools/hwsu`

## Imported by

- none

## Top-level constants

- `FEAS`
- `GATES`
- `LADDER`
- `REPO`
- `SEEDS`

## Classes and functions

- **function `make_ctx`** [L34-39]: `def make_ctx(tmp_path, **kw)`
- **function `status`** [L42-48]: `def status(fn, ctx)` - A gate returns details with "status" or raises C1GateFailure (API §4); both count.
- **function `fr`** [L51-52]: `def fr(x)`
- **function `_of2_with_bound`** [L56-82]: `def _of2_with_bound(tmp_path, monkeypatch, L, rank=250)` - Plants stream_bounds and, consistently (API E-4), the stored bootstrap-mean draws: half
- **test `test_of_2_boundary_is_exact`** [L85-93]: `def test_of_2_boundary_is_exact(tmp_path, monkeypatch)`
- **test `test_of_2_rank_is_checked`** [L96-98]: `def test_of_2_rank_is_checked(tmp_path, monkeypatch)`
- **test `test_of_2_real_bounds`** [L101-107]: `def test_of_2_real_bounds(tmp_path)`
- **function `_of3_ctx`** [L111-121]: `def _of3_ctx(tmp_path, c, rng)`
- **function `_plant`** [L124-146]: `def _plant(monkeypatch, A_S, A_full, bad=())` - Seams: c2_stats.f1_problem (the fit status per (K, euclidean)) and c2_attrib.partition
- **function `_flat`** [L149-157]: `def _flat(x)`
- **test `test_of_3_share_ceiling`** [L161-181]: `def test_of_3_share_ceiling(tmp_path, monkeypatch, c, want)` decorators: @pytest.mark.parametrize('c,want', [(0.5, 'PASS'), (0.1, 'SHARE_DROPPED')])
- **test `test_of_3_degenerate_primary_fit`** [L184-187]: `def test_of_3_degenerate_primary_fit(tmp_path, monkeypatch)`
- **function `_of4`** [L194-233]: `def _of4(tmp_path, monkeypatch, passes, results, n=300, shift=0.0)`
- **test `test_of_4_calls_and_alternatives`** [L236-249]: `def test_of_4_calls_and_alternatives(tmp_path, monkeypatch)`
- **test `test_of_4_family_rules`** [L260-274]: `def test_of_4_family_rules(tmp_path, monkeypatch, passes, prior, want, nr, ns)` decorators: @pytest.mark.parametrize('passes,prior,want,nr,ns', [({'ZR010': 4096, 'ZR030': 4096, 'Z010': None, 'Z050': 4096}, 'PASS', 'SHARE_DROPPED', 4096, None), ({'ZR010': None, 'ZR030': 4096, 'Z010': 4096, 'Z050': 4096}, 'PASS', FEAS, None, 4096), ({'ZR010': 32768, 'ZR030': 4096, 'Z010': 4096, 'Z050': 4096}, 'SHARE_DROPPED', 'SHARE_DROPPED', 32768, 4096), ({'ZR010': 8192, 'ZR030': None, 'Z010': 4096, 'Z050': 4096}, 'SHARE_DROPPED', FEAS, None, 4096)])
- **function `tiny`** [L279-282]: `def tiny()` decorators: @pytest.fixture(scope='module')
- **function `_pi_sampler`** [L285-296]: `def _pi_sampler(T, E, pi, a1, rng)` - Planted defect: z_28 ~ π instead of the bridge (β dropped); otherwise API §2.2.
- **function `_lemma_ctx`** [L299-303]: `def _lemma_ctx(tmp_path, w, a1, a2)`
- **function `_my_lemma`** [L306-324]: `def _my_lemma(ctx)`
- **test `test_of_5_real_sampler_passes`** [L327-333]: `def test_of_5_real_sampler_passes(tmp_path, tiny)`
- **test `test_of_5_planted_pi_sampler_fails`** [L336-342]: `def test_of_5_planted_pi_sampler_fails(tmp_path, tiny)`
- **function `recs`** [L350-351]: `def recs(**over)`
- **test `test_of_outcome`** [L354-365]: `def test_of_outcome()`
- **test `test_tails`** [L368-382]: `def test_tails()`

