# `tests/experiment/test_x5g1t_usage_files.py`

- Source: [tests/experiment/test_x5g1t_usage_files.py](../../../../../tests/experiment/test_x5g1t_usage_files.py)
- Kind: python
- Lines: 251

## Module docstring

> Independent contract tests for ``topo_pilot.experiment.x5g1t_usage`` (worker self-hold latch).

## Imports

### Internal (repo files)

- `from topo_pilot.experiment import x5g1t_usage` -> [src/topo_pilot/experiment/x5g1t_usage.py](../../src/topo_pilot/experiment/x5g1t_usage.py.md) (line 18, via package root)
- `from topo_pilot.experiment import x5g1t_runtime` -> [src/topo_pilot/experiment/x5g1t_runtime.py](../../src/topo_pilot/experiment/x5g1t_runtime.py.md) (line 69, via package root)

### External (third-party)

- `pytest` (lines 16)

### Standard library

- `__future__` (lines 10)
- `datetime` (lines 13)
- `json` (lines 12)
- `pathlib` (lines 14)

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

- `NOW`
- `SCHEMA`
- `T0`
- `UNAVAILABLE`
- `UTC`

## Classes and functions

- **function `ps`** [L27-29]: `def ps(t: datetime) -> str` - PowerShell ``"o"`` format: 7 fractional digits and a Z suffix.
- **function `lim`** [L32-34]: `def lim(kind, pct, *, relevant=True, warning=None, reset=None) -> dict`
- **function `multi`** [L37-40]: `def multi(session=40, weekly=86, model=90) -> list[dict]` - Realistic multi-limit snapshot; the per-model allowance is irrelevant.
- **function `usage`** [L43-47]: `def usage(limits, *, at=T0 - timedelta(minutes=1), obs='OBSERVED', source='owner report')`
- **function `latch`** [L54-56]: `def latch(kinds=('weekly_all_models',), at=T0) -> dict`
- **function `fresh_clear`** [L59-60]: `def fresh_clear(minutes=30, **kw) -> dict`
- **function `kinds_of`** [L63-64]: `def kinds_of(items) -> set[str]`
- **function `put`** [L74-76]: `def put(box: Path, name: str, content) -> None`
- **function `box`** [L80-84]: `def box(tmp_path: Path) -> Path` decorators: @pytest.fixture
- **function `cleared_files`** [L87-88]: `def cleared_files(b: Path) -> list[Path]`
- **test `test_apply_usage_missing_files_no_hold`** [L91-94]: `def test_apply_usage_missing_files_no_hold(tmp_path: Path) -> None`
- **test `test_apply_usage_blocking_writes_latch_and_reads_utf8_sig`** [L97-103]: `def test_apply_usage_blocking_writes_latch_and_reads_utf8_sig(tmp_path: Path) -> None`
- **test `test_apply_usage_hold_persists_without_usage_file`** [L106-109]: `def test_apply_usage_hold_persists_without_usage_file(tmp_path: Path) -> None`
- **test `test_apply_usage_clears_and_archives`** [L112-120]: `def test_apply_usage_clears_and_archives(tmp_path: Path) -> None`
- **test `test_apply_usage_existing_malformed_usage_file_raises`** [L124-127]: `def test_apply_usage_existing_malformed_usage_file_raises(tmp_path: Path, content) -> None` decorators: @pytest.mark.parametrize('content', ['null', '[]', '"x"', '42', '{bad', ''])
- **test `test_apply_usage_existing_malformed_latch_file_raises`** [L131-135]: `def test_apply_usage_existing_malformed_latch_file_raises(tmp_path: Path, content) -> None` decorators: @pytest.mark.parametrize('content', ['null', '[]', '"x"', '42', '{bad', ''])
- **test `test_read_controls_existing_malformed_file_is_stop`** [L140-144]: `def test_read_controls_existing_malformed_file_is_stop(box: Path, name, content) -> None` decorators: @pytest.mark.parametrize('content', ['null', '[]', '"x"', '{bad']) @pytest.mark.parametrize('name', ['claude_usage.json', u.LATCH_NAME])
- **test `test_read_controls_missing_usage_files_continue`** [L147-148]: `def test_read_controls_missing_usage_files_continue(box: Path) -> None`
- **test `test_read_controls_multi_limit_hold_and_latch`** [L154-158]: `def test_read_controls_multi_limit_hold_and_latch(box: Path) -> None`
- **test `test_read_controls_warning_hold`** [L161-164]: `def test_read_controls_warning_hold(box: Path) -> None`
- **test `test_read_controls_unavailable_alone_continues`** [L167-170]: `def test_read_controls_unavailable_alone_continues(box: Path) -> None`
- **test `test_read_controls_unknown_values_stop`** [L173-177]: `def test_read_controls_unknown_values_stop(box: Path) -> None`
- **test `test_read_controls_stale_evidence_holds`** [L180-185]: `def test_read_controls_stale_evidence_holds(box: Path) -> None`
- **test `test_read_controls_naive_or_nonstring_time_not_release`** [L188-192]: `def test_read_controls_naive_or_nonstring_time_not_release(box: Path) -> None`
- **test `test_read_controls_mode_edited_to_working_does_not_release`** [L195-200]: `def test_read_controls_mode_edited_to_working_does_not_release(box: Path) -> None`
- **test `test_read_controls_fresh_clearance_plus_continue_releases_and_archives`** [L203-210]: `def test_read_controls_fresh_clearance_plus_continue_releases_and_archives(box: Path) -> None`
- **test `test_read_controls_coordinator_wait_holds_despite_clearance`** [L213-217]: `def test_read_controls_coordinator_wait_holds_despite_clearance(box: Path) -> None`
- **test `test_blocking_usage_holds_despite_worker_continue`** [L220-223]: `def test_blocking_usage_holds_despite_worker_continue(box: Path) -> None`
- **test `test_stop_beats_everything`** [L227-237]: `def test_stop_beats_everything(box: Path, stop_src: str) -> None` decorators: @pytest.mark.parametrize('stop_src', ['file', 'request', 'worker'])
- **test `test_hold_modes_hold`** [L241-244]: `def test_hold_modes_hold(box: Path, mode: str) -> None` decorators: @pytest.mark.parametrize('mode', ['RUNTIME_BLOCKED', 'NEEDS_USAGE_INFO', 'WAIT_USAGE_RESET'])
- **test `test_unknown_or_missing_mode_is_stop`** [L249-251]: `def test_unknown_or_missing_mode_is_stop(box: Path, state) -> None` decorators: @pytest.mark.parametrize('state', [{'mode': 'BOGUS'}, {'mode': 3}, {'mode': None}, {}, {'state': 'WORKING'}])

