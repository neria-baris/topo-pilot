# `tests/circle_history/test_builder_v25.py`

- Source: [tests/circle_history/test_builder_v25.py](../../../../../tests/circle_history/test_builder_v25.py)
- Kind: python
- Lines: 280

## Module docstring

> BUILDER tests (not independent) for spec v2.5 (job 0017): release issuer binding for the
> designated Claude coordinator, measure-only CPU policy under the owner override, and the
> [0, 2pi) phase interval (F4). Synthetic temporary mailboxes and stores only.

## Imports

### Internal (repo files)

- `import chart` -> [tools/x4_circle_history/chart.py](../../tools/x4_circle_history/chart.py.md) (line 22, via sys.path edit)
- `import meter_bind` -> [tools/x4_circle_history/meter_bind.py](../../tools/x4_circle_history/meter_bind.py.md) (line 23, via sys.path edit)
- `import release` -> [tools/x4_circle_history/release.py](../../tools/x4_circle_history/release.py.md) (line 24, via sys.path edit)

### External (third-party)

- `numpy` (lines 13)
- `pytest` (lines 14)

### Standard library

- `__future__` (lines 5)
- `copy` (lines 7)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 11)
- `sys` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(extra)` -> `tests/oracle_profile`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- none

## Top-level constants

- `REPO`
- `SESSION`
- `TOOL`

## Classes and functions

- **function `_mailbox`** [L29-64]: `def _mailbox(tmp_path, mode='ACTIVE_CLAUDE_COORDINATOR', issuer='claude-coordinator')`
- **function `_verify`** [L67-70]: `def _verify(box, out, rel)`
- **test `test_claude_release_verifies`** [L73-75]: `def test_claude_release_verifies(tmp_path)`
- **function `_mutations`** [L78-99]: `def _mutations(box, rel, tmp_path)`
- **test `test_claude_release_refuses_bad_binding`** [L114-122]: `def test_claude_release_refuses_bad_binding(tmp_path, case)` decorators: @pytest.mark.parametrize('case', ['wrong session', 'wrong sha', 'wrong schema', 'outside archive', 'missing session', 'missing ref', 'unknown issuer'])
- **test `test_claude_release_refused_when_runtime_not_claude_active`** [L125-128]: `def test_claude_release_refused_when_runtime_not_claude_active(tmp_path)`
- **test `test_codex_release_verifies_only_while_not_relinquished`** [L131-140]: `def test_codex_release_verifies_only_while_not_relinquished(tmp_path)`
- **test `test_codex_release_with_claude_fields_refused`** [L143-149]: `def test_codex_release_with_claude_fields_refused(tmp_path)`
- **test `test_missing_runtime_file_fails_closed`** [L152-156]: `def test_missing_runtime_file_fails_closed(tmp_path)`
- **function `measured`** [L160-171]: `def measured(tmp_path, monkeypatch)` decorators: @pytest.fixture() - The real v2.5 CONTRACT (measure-only policy) bound to a temporary store.
- **function `_ledger`** [L174-183]: `def _ledger(out, entries, policy=None)`
- **test `test_measure_only_never_stops_on_cpu`** [L186-194]: `def test_measure_only_never_stops_on_cpu(measured)`
- **test `test_measure_only_unreleased_stage_still_refused`** [L197-201]: `def test_measure_only_unreleased_stage_still_refused(measured)`
- **test `test_measure_only_limiter_has_no_cpu_reason_but_keeps_other_guards`** [L204-213]: `def test_measure_only_limiter_has_no_cpu_reason_but_keeps_other_guards(tmp_path)`
- **test `test_ledger_policy_sync_preserves_entries`** [L216-225]: `def test_ledger_policy_sync_preserves_entries(measured)`
- **test `test_wrap_maps_two_pi_to_zero`** [L228-234]: `def test_wrap_maps_two_pi_to_zero()`
- **test `test_apply_gauge_never_returns_two_pi`** [L237-240]: `def test_apply_gauge_never_returns_two_pi()`
- **function `_equidistant_chart`** [L243-262]: `def _equidistant_chart(phases)`
- **test `test_extend_never_returns_two_pi`** [L265-280]: `def test_extend_never_returns_two_pi()` - A query equidistant from 8 landmarks whose mean angle is a tiny negative number.

