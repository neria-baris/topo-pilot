# `tests/experiment/test_x5g1t_usage.py`

- Source: [tests/experiment/test_x5g1t_usage.py](../../../../../tests/experiment/test_x5g1t_usage.py)
- Kind: python
- Lines: 400

## Module docstring

> Independent contract tests for ``topo_pilot.experiment.x5g1t_usage`` (worker self-hold latch).

## Imports

### Internal (repo files)

- `from topo_pilot.experiment import x5g1t_usage` -> [src/topo_pilot/experiment/x5g1t_usage.py](../../src/topo_pilot/experiment/x5g1t_usage.py.md) (line 17, via package root)

### External (third-party)

- `pytest` (lines 15)

### Standard library

- `__future__` (lines 9)
- `datetime` (lines 13)
- `json` (lines 11)
- `math` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- `LATER`
- `SCHEMA`
- `T0`
- `UNAVAILABLE`
- `UTC`

## Classes and functions

- **function `ps`** [L26-28]: `def ps(t: datetime) -> str` - PowerShell ``"o"`` format: 7 fractional digits and a Z suffix.
- **function `lim`** [L31-33]: `def lim(kind, pct, *, relevant=True, warning=None, reset=None) -> dict`
- **function `multi`** [L36-39]: `def multi(session=40, weekly=86, model=90) -> list[dict]` - Realistic multi-limit snapshot; the per-model allowance is irrelevant.
- **function `usage`** [L42-46]: `def usage(limits, *, at=T0 - timedelta(minutes=1), obs='OBSERVED', source='owner report')`
- **function `latch`** [L53-55]: `def latch(kinds=('weekly_all_models',), at=T0) -> dict`
- **function `fresh_clear`** [L58-59]: `def fresh_clear(minutes=30, **kw) -> dict`
- **function `kinds_of`** [L62-63]: `def kinds_of(items) -> set[str]`
- **test `test_constants`** [L68-72]: `def test_constants() -> None`
- **test `test_parse_utc_offsets`** [L84-87]: `def test_parse_utc_offsets(text, expected) -> None` decorators: @pytest.mark.parametrize('text, expected', [('2026-10-14T03:15:34Z', datetime(2026, 10, 14, 3, 15, 34, tzinfo=UTC)), ('2026-10-14T03:15:34+00:00', datetime(2026, 10, 14, 3, 15, 34, tzinfo=UTC)), ('2026-10-14T06:15:34+03:00', datetime(2026, 10, 14, 3, 15, 34, tzinfo=UTC)), ('2026-10-14T00:15:34-03:00', datetime(2026, 10, 14, 3, 15, 34, tzinfo=UTC)), ('2026-10-14T03:15:34.5Z', datetime(2026, 10, 14, 3, 15, 34, 500000, tzinfo=UTC)), ('2026-10-14T03:15:34.123456+00:00', datetime(2026, 10, 14, 3, 15, 34, 123456, tzinfo=UTC))])
- **test `test_parse_utc_powershell_seven_digits`** [L92-96]: `def test_parse_utc_powershell_seven_digits(text) -> None` decorators: @pytest.mark.parametrize('text', ['2026-10-14T03:15:34.0014496Z', '2026-10-14T06:15:34.0014496+03:00'])
- **test `test_parse_utc_rejects`** [L103-105]: `def test_parse_utc_rejects(bad) -> None` decorators: @pytest.mark.parametrize('bad', ['2026-10-14T03:15:34', '2026-10-14T03:15:34.0014496', '2026-10-14', 'yesterday', '', '2026-13-40T99:00:00Z', None, 1760411734, 1.5, ['2026-10-14T03:15:34Z'], datetime(2026, 10, 14, tzinfo=UTC)])
- **test `test_realistic_multi_limit_only_relevant_high_one_blocks`** [L110-113]: `def test_realistic_multi_limit_only_relevant_high_one_blocks() -> None`
- **test `test_threshold_boundary`** [L118-120]: `def test_threshold_boundary(pct, blocks) -> None` decorators: @pytest.mark.parametrize('pct, blocks', [(85, True), (85.0, True), (100, True), (84.99, False), (0, False), (None, False)])
- **test `test_custom_threshold`** [L123-125]: `def test_custom_threshold() -> None`
- **test `test_relevant_warning_blocks_with_null_percent`** [L129-132]: `def test_relevant_warning_blocks_with_null_percent(obs) -> None` decorators: @pytest.mark.parametrize('obs', ['OBSERVED', 'UNAVAILABLE'])
- **test `test_irrelevant_warning_does_not_block`** [L135-136]: `def test_irrelevant_warning_does_not_block() -> None`
- **test `test_unavailable_never_blocks_by_itself`** [L139-143]: `def test_unavailable_never_blocks_by_itself() -> None`
- **test `test_observed_empty_limits_is_not_blocking`** [L146-147]: `def test_observed_empty_limits_is_not_blocking() -> None`
- **function `_mut`** [L150-151]: `def _mut(**limit_overrides) -> dict`
- **function `_drop`** [L154-157]: `def _drop(key) -> dict`
- **test `test_blocking_limits_malformed`** [L176-178]: `def test_blocking_limits_malformed(bad) -> None` decorators: @pytest.mark.parametrize('bad', [None, [], 'OBSERVED', {**usage(multi()), 'observability': 'observed'}, {**usage(multi()), 'observability': None}, {k: v for (k, v) in usage(multi()).items() if k != 'observability'}, {k: v for (k, v) in usage(multi()).items() if k != 'limits'}, {**usage(multi()), 'limits': None}, {**usage(multi()), 'limits': {'session': 40}}, usage(['session']), usage([None]), usage([[40]]), _mut(kind=None), _mut(kind=3), _drop('kind'), _mut(relevant='true'), _mut(relevant=1), _mut(relevant=None), _drop('relevant'), _mut(used_percent=True), _mut(used_percent=False), _mut(used_percent='86'), _mut(used_percent=math.nan), _mut(used_percent=math.inf), _mut(used_percent=-math.inf), _mut(used_percent=-0.5), _mut(used_percent=100.01), _mut(used_percent=[86]), _mut(warning=5), _mut(warning=True), _mut(warning=['limit'])])
- **test `test_make_latch_shape`** [L183-190]: `def test_make_latch_shape() -> None`
- **test `test_fresh_full_clearance_clears`** [L195-197]: `def test_fresh_full_clearance_clears() -> None`
- **function `_not_cleared`** [L200-204]: `def _not_cleared(lt, us) -> str`
- **test `test_older_or_equal_evidence_is_stale`** [L208-209]: `def test_older_or_equal_evidence_is_stale(at) -> None` decorators: @pytest.mark.parametrize('at', [T0 - timedelta(minutes=1), T0])
- **test `test_offset_comparison_is_by_instant_not_text`** [L212-218]: `def test_offset_comparison_is_by_instant_not_text() -> None`
- **test `test_unavailable_never_clears`** [L221-224]: `def test_unavailable_never_clears() -> None`
- **test `test_bad_source_never_clears`** [L228-229]: `def test_bad_source_never_clears(source) -> None` decorators: @pytest.mark.parametrize('source', ['unavailable', None, 7])
- **test `test_missing_source_never_clears`** [L232-239]: `def test_missing_source_never_clears() -> None`
- **test `test_every_latched_kind_must_be_present_relevant_numeric_low`** [L246-248]: `def test_every_latched_kind_must_be_present_relevant_numeric_low(weekly) -> None` decorators: @pytest.mark.parametrize('weekly', [None, lim('weekly_all_models', None), lim('weekly_all_models', 20, relevant=False), lim('weekly_all_models', 85), lim('weekly_all_models', 20, warning='approaching')])
- **test `test_one_of_two_latched_kinds_missing`** [L251-254]: `def test_one_of_two_latched_kinds_missing() -> None`
- **test `test_latched_kind_just_below_threshold_clears`** [L257-259]: `def test_latched_kind_just_below_threshold_clears() -> None`
- **test `test_other_relevant_limit_blocking_prevents_clear`** [L262-264]: `def test_other_relevant_limit_blocking_prevents_clear() -> None`
- **test `test_garbage_evidence_time_never_clears`** [L267-273]: `def test_garbage_evidence_time_never_clears() -> None`
- **function `_bad_latches`** [L276-286]: `def _bad_latches() -> list`
- **test `test_malformed_latch`** [L290-294]: `def test_malformed_latch(bad) -> None` decorators: @pytest.mark.parametrize('bad', _bad_latches())
- **function `_hold`** [L301-305]: `def _hold(d) -> None`
- **test `test_no_latch_blocking_sets_latch`** [L308-313]: `def test_no_latch_blocking_sets_latch() -> None`
- **test `test_no_latch_warning_sets_latch_even_unavailable`** [L316-321]: `def test_no_latch_warning_sets_latch_even_unavailable() -> None`
- **test `test_no_latch_not_blocking_continues`** [L325-328]: `def test_no_latch_not_blocking_continues(us) -> None` decorators: @pytest.mark.parametrize('us', [None, UNAVAILABLE, usage(multi(40, 60, 99)), usage([])])
- **test `test_latch_without_fresh_full_clearance_holds`** [L339-340]: `def test_latch_without_fresh_full_clearance_holds(us) -> None` decorators: @pytest.mark.parametrize('us', [None, UNAVAILABLE, {**UNAVAILABLE, 'observed_at_utc': ps(LATER)}, usage(multi(12, 20, 99), at=T0 - timedelta(minutes=5)), usage(multi(12, 20, 99), at=T0), usage([lim('session', 3)], at=LATER), usage([lim('session', 3), lim('weekly_all_models', None)], at=LATER), fresh_clear(source='unavailable')])
- **test `test_fresh_full_clearance_continues_and_clears`** [L343-346]: `def test_fresh_full_clearance_continues_and_clears() -> None`
- **test `test_cleared_kind_but_new_relevant_limit_blocks`** [L349-354]: `def test_cleared_kind_but_new_relevant_limit_blocks() -> None`
- **test `test_elapsed_time_and_reset_times_never_clear`** [L359-363]: `def test_elapsed_time_and_reset_times_never_clear(now) -> None` decorators: @pytest.mark.parametrize('now', [datetime(2099, 1, 1, tzinfo=UTC), T0 + timedelta(days=30)])
- **test `test_decision_with_malformed_usage_raises`** [L368-370]: `def test_decision_with_malformed_usage_raises(bad) -> None` decorators: @pytest.mark.parametrize('bad', [{**usage(multi()), 'observability': 'MAYBE'}, usage([lim('session', '86%')])])
- **test `test_none_latch_is_absence_sentinel_in_decision_but_malformed_for_latch_clears`** [L373-377]: `def test_none_latch_is_absence_sentinel_in_decision_but_malformed_for_latch_clears() -> None`
- **test `test_decision_naive_or_nonstring_evidence_time_never_releases`** [L380-387]: `def test_decision_naive_or_nonstring_evidence_time_never_releases() -> None`
- **test `test_session_and_weekly_both_latched_then_partial_clear_holds`** [L390-400]: `def test_session_and_weekly_both_latched_then_partial_clear_holds() -> None`

