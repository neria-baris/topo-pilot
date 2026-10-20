# `tests/k4b/test_b_charts.py`

- Source: [tests/k4b/test_b_charts.py](../../../../../tests/k4b/test_b_charts.py)
- Kind: python
- Lines: 398

## Module docstring

> Author B, K4b TEST_PLAN B4-B8, B12: K4b cfg reaches c1_chart; ledgers (6 trained, 3 step-0,
> 'direct' refused on step-0); INIT_UNAVAILABLE non-gating, shared-code FAIL_TECHNICAL stops;
> freeze before validation, no gauge/refit on validation; GIANT 487/486, support 507/506;
> bitwise determinism. Kernels monkeypatched (fit_chart_lcc, chart.extend); no PH, no checkpoint.

## Imports

### Internal (repo files)

- `import c1_chart` -> [tools/c1prime/c1_chart.py](../../tools/c1prime/c1_chart.py.md) (line 21, via sys.path edit)
- `import c1_config` -> [tools/c1prime/c1_config.py](../../tools/c1prime/c1_config.py.md) (line 22, via sys.path edit)
- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 23, via sys.path edit)
- `import errors` -> [tools/x4_circle_history/errors.py](../../tools/x4_circle_history/errors.py.md) (line 24, via sys.path edit)
- `import k4b_charts` -> [tools/k4b/k4b_charts.py](../../tools/k4b/k4b_charts.py.md) (line 25, via sys.path edit)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../../tools/k4b/k4b_config.py.md) (line 26, via sys.path edit)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../tools/c1prime/c1_records.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 18)
- `pytest` (lines 19)

### Standard library

- `__future__` (lines 6)
- `copy` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 16: `str(REPO / _sub)` -> `tools/c1prime`, `tools/c1prime_registry`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `GIANT_FAIL`
- `LABELS`
- `M32`
- `MODELS`
- `N`
- `REPO`
- `UNAVAILABLE`

## Classes and functions

- **function `outcome`** [L35-40]: `def outcome(fn, *args, **kwargs)`
- **function `grid_phi`** [L43-44]: `def grid_phi(n=N)`
- **function `fake_chart`** [L47-55]: `def fake_chart(n=N, d=4, seed=0)`
- **class `Kernel`** [L61-74] - Fake fit_chart_lcc: records each call and the ledger claims present at call time.
- **method `Kernel.__init__`** [L64-65]: `def __init__(self, out, plan=())`
- **method `Kernel.__call__`** [L67-74]: `def __call__(self, X, ids, cfg, guard=None, timed=None, persist=None)`
- **function `patch`** [L77-80]: `def patch(monkeypatch, name, fn, module=c1_chart)`
- **function `inputs`** [L83-87]: `def inputs(seed=1)`
- **function `ledger_claims`** [L90-91]: `def ledger_claims(out, name)`
- **test `test_chart_cfg_equals_c1prime_cfg`** [L96-102]: `def test_chart_cfg_equals_c1prime_cfg()`
- **test `test_check_chart_equality_default_is_equal`** [L105-108]: `def test_check_chart_equality_default_is_equal()`
- **test `test_check_chart_equality_detects_each_difference`** [L111-121]: `def test_check_chart_equality_detects_each_difference()`
- **test `test_build_chart_claims_first_and_passes_k4b_cfg`** [L124-138]: `def test_build_chart_claims_first_and_passes_k4b_cfg(tmp_path, monkeypatch)`
- **test `test_failed_construction_keeps_its_claim_and_is_never_retried`** [L141-152]: `def test_failed_construction_keeps_its_claim_and_is_never_retried(tmp_path, monkeypatch)`
- **test `test_open_ledgers_two_files`** [L157-163]: `def test_open_ledgers_two_files(tmp_path)`
- **test `test_trained_ledger_holds_six`** [L166-174]: `def test_trained_ledger_holds_six(tmp_path)`
- **test `test_init_ledger_refuses_any_role_but_production`** [L178-185]: `def test_init_ledger_refuses_any_role_but_production(tmp_path, role)` decorators: @pytest.mark.parametrize('role', ['direct', 'validation_only'])
- **test `test_init_ledger_three_production_claims`** [L188-196]: `def test_init_ledger_three_production_claims(tmp_path)`
- **test `test_init_unavailable_is_non_gating`** [L201-211]: `def test_init_unavailable_is_non_gating(tmp_path, monkeypatch)`
- **test `test_init_shared_code_fail_technical_stops_immediately`** [L218-225]: `def test_init_shared_code_fail_technical_stops_immediately(tmp_path, monkeypatch, plan, n_calls)` decorators: @pytest.mark.parametrize('plan,n_calls', [([errors.Invalid('exact duplicate landmarks carry conflicting phases')], 1), ([None, errors.Invalid('queries must be finite')], 2)])
- **test `test_init_gauge_integrity_defect_stops`** [L228-235]: `def test_init_gauge_integrity_defect_stops(tmp_path, monkeypatch)`
- **function `fake_extend`** [L240-245]: `def fake_extend(n_sup)`
- **function `frozen_store`** [L248-259]: `def frozen_store(out, monkeypatch, kernel)`
- **test `test_require_frozen_refuses_without_record`** [L262-265]: `def test_require_frozen_refuses_without_record(tmp_path)`
- **test `test_c0_val_gate_refused_before_freeze_spends_no_construction`** [L268-278]: `def test_c0_val_gate_refused_before_freeze_spends_no_construction(tmp_path, monkeypatch)`
- **test `test_tampered_frozen_artefact_refused`** [L281-292]: `def test_tampered_frozen_artefact_refused(tmp_path, monkeypatch)`
- **function `run_val_gate`** [L295-320]: `def run_val_gate(out, monkeypatch, n_sup, direct_plan=())`
- **test `test_c0_val_support_507_passes_without_gauge_or_refit`** [L323-334]: `def test_c0_val_support_507_passes_without_gauge_or_refit(tmp_path, monkeypatch)`
- **test `test_c0_val_support_506_is_chart_unavailable`** [L337-338]: `def test_c0_val_support_506_is_chart_unavailable(tmp_path, monkeypatch)`
- **test `test_c0_val_direct_giant_failure_is_chart_unavailable`** [L341-342]: `def test_c0_val_direct_giant_failure_is_chart_unavailable(tmp_path, monkeypatch)`
- **test `test_giant_487_passes_486_fails`** [L347-350]: `def test_giant_487_passes_486_fails()`
- **test `test_c0_val_support_threshold_with_k4b_cfg`** [L354-361]: `def test_c0_val_support_threshold_with_k4b_cfg(monkeypatch, n_sup, ok)` decorators: @pytest.mark.parametrize('n_sup,ok', [(507, True), (506, False)])
- **function `activations`** [L369-371]: `def activations()`
- **test `test_determinism_identical_passes`** [L374-378]: `def test_determinism_identical_passes()`
- **test `test_determinism_any_bitwise_difference_fails`** [L382-398]: `def test_determinism_any_bitwise_difference_fails(change)` decorators: @pytest.mark.parametrize('change', ['bit', 'dtype', 'shape', 'negzero'])

