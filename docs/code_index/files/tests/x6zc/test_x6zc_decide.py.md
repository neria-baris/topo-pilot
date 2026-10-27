# `tests/x6zc/test_x6zc_decide.py`

- Source: [tests/x6zc/test_x6zc_decide.py](../../../../../tests/x6zc/test_x6zc_decide.py)
- Kind: python
- Lines: 391

## Module docstring

> Author A (job 0120): X6ZC decision rules (§9.1, every branch and its precedence, G-R0 first),
> licences, qualifiers, reuse verdict, report schema, K4 tiers, the 0.10 band, the §13 pause points
> and the stage-1 store guards (TEST_PLAN.md §3). Written from the protocol copy, API.md,
> CONTRACT.json, TEST_PLAN.md and the 0117 review only (tools/x6zc/*.py never read). Evidence
> records are synthetic dicts built here; stores are tmp_path directories (never a project store).

## Imports

### Internal (repo files)

- `import x6zc_core` -> [tools/x6zc/x6zc_core.py](../../tools/x6zc/x6zc_core.py.md) (line 16, via sys.path edit)
- `import x6zc_census` -> [tools/x6zc/x6zc_census.py](../../tools/x6zc/x6zc_census.py.md) (line 17, via sys.path edit)
- `import x6zc_run` -> [tools/x6zc/x6zc_run.py](../../tools/x6zc/x6zc_run.py.md) (line 18, via sys.path edit)

### External (third-party)

- `pytest` (lines 12)

### Standard library

- `__future__` (lines 6)
- `json` (lines 8)
- `pathlib` (lines 10)
- `sys` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 15: `str(REPO / 'tools' / 'x6zc')` -> `tools/x6zc`

## Imported by

- none

## Top-level constants

- `CONTRACT`
- `GENERIC`
- `LV`
- `PHRASES`
- `PRIME`
- `REPO`
- `STORED`
- `TOP`

## Classes and functions

- **function `cell`** [L35-43]: `def cell(c='P', b=0.2, lo=0.15, hi=0.25, und=0.0, mm=BAND, pm=BAND, mp=BAND, label=None)` - Cell statistics in the API §8 cell_statistics layout; b is already σ·β_PP.
- **function `ev`** [L45-52]: `def ev(**kw) -> dict`
- **function `ruling`** [L54-56]: `def ruling(check, ident=True, aff=True, rid='D1') -> dict`
- **function `failed`** [L58-61]: `def failed(check, status='FAIL', **kw) -> dict`
- **function `with_cell`** [L63-66]: `def with_cell(c='P', **kw) -> dict`
- **function `outs`** [L68-69]: `def outs(d) -> dict`
- **function `ro`** [L71-73]: `def ro(e, c='P') -> tuple`
- **test `test_global_precedence_g_r0_first`** [L75-81]: `def test_global_precedence_g_r0_first()`
- **test `test_g_r1_invalid`** [L83-87]: `def test_g_r1_invalid()`
- **test `test_g_r2_defect_found`** [L90-95]: `def test_g_r2_defect_found(chk)` decorators: @pytest.mark.parametrize('chk', ['K4', 'A1', 'A2', 'A_audit', 'K2', 'K5'])
- **test `test_g_r2_prime_irreproducible`** [L97-100]: `def test_g_r2_prime_irreproducible()`
- **test `test_defect_elsewhere_does_not_preempt`** [L102-108]: `def test_defect_elsewhere_does_not_preempt()`
- **test `test_missing_ruling_raises`** [L112-116]: `def test_missing_ruling_raises(chk, status)` decorators: @pytest.mark.parametrize('chk,status', [('K2', 'DEFECT_CANDIDATE'), ('K2', 'FAIL'), ('K4', 'DEFECT_CANDIDATE')])
- **test `test_g_r3_non_invariant`** [L118-123]: `def test_g_r3_non_invariant()`
- **test `test_r4a_not_enough_data`** [L125-134]: `def test_r4a_not_enough_data()`
- **test `test_r4b_underpowered`** [L136-146]: `def test_r4b_underpowered()`
- **test `test_r5_fresh_set_unstable`** [L148-152]: `def test_r5_fresh_set_unstable()`
- **test `test_r6_not_replicated`** [L154-158]: `def test_r6_not_replicated()`
- **test `test_r7_weak_replication_cases`** [L160-170]: `def test_r7_weak_replication_cases()`
- **test `test_r7b_unstable_ratio`** [L172-176]: `def test_r7b_unstable_ratio()`
- **test `test_r8_zc_coordinate_and_w1`** [L178-186]: `def test_r8_zc_coordinate_and_w1()`
- **test `test_r8b_not_na_invariant`** [L188-192]: `def test_r8b_not_na_invariant()`
- **test `test_r9_na_direction`** [L194-199]: `def test_r9_na_direction()`
- **test `test_r9_prime_not_discriminable`** [L201-210]: `def test_r9_prime_not_discriminable()`
- **test `test_r10_partial`** [L212-214]: `def test_r10_partial()`
- **test `test_licences_filled`** [L225-243]: `def test_licences_filled()`
- **function `_q_case`** [L245-249]: `def _q_case() -> tuple`
- **test `test_qualifiers`** [L251-259]: `def test_qualifiers()`
- **test `test_qualifiers_census`** [L261-271]: `def test_qualifiers_census()`
- **test `test_reuse_verdict`** [L273-293]: `def test_reuse_verdict()`
- **function `_report`** [L300-319]: `def _report(outcome=NA_DIR, licence='L', rule='R9', g_rule=None) -> dict`
- **test `test_report_schema`** [L321-333]: `def test_report_schema()`
- **test `test_k4_tiers_and_crosses`** [L340-351]: `def test_k4_tiers_and_crosses()`
- **test `test_pause_check`** [L353-365]: `def test_pause_check()`
- **test `test_inventory_and_guards`** [L367-391]: `def test_inventory_and_guards(tmp_path)`

