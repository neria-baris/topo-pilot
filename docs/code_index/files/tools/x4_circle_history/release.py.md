# `tools/x4_circle_history/release.py`

- Source: [tools/x4_circle_history/release.py](../../../../../tools/x4_circle_history/release.py)
- Kind: python
- Lines: 203

## Module docstring

> Coordinator release verification (standard library only; no subprocess). No release exists in
> job 0016.

## Imports

### Internal (repo files)

- `from errors import ScoringAuthority` -> [tools/x4_circle_history/errors.py](errors.py.md) (line 28, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 22)
- `hashlib` (lines 24)
- `json` (lines 25)
- `pathlib` (lines 26)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/circle_history/test_builder_guards.py](../../tests/circle_history/test_builder_guards.py.md) (line 25, import)
- [tests/circle_history/test_builder_runtime.py](../../tests/circle_history/test_builder_runtime.py.md) (line 22, import)
- [tests/circle_history/test_builder_v25.py](../../tests/circle_history/test_builder_v25.py.md) (line 24, import)
- [tools/x4_circle_history/meter_bind.py](meter_bind.py.md) (line 50, import)
- [tools/x4_circle_history/runner.py](runner.py.md) (line 313, import)

## Top-level constants

- `ASSUMPTION_SCHEMA`
- `CLAUDE_ACTIVE_MODE`
- `CLAUDE_FIELDS`
- `HERE`
- `ISSUERS`
- `MAILBOX`
- `REPO`
- `SCHEMA`
- `STAGES`

## Classes and functions

- **class `ReleaseError(RuntimeError)`** [L41-42] - Missing, malformed or mismatching coordinator release.
- **function `_sha`** [L45-46]: `def _sha(path: Path) -> str`
- **function `_git_dir`** [L49-60]: `def _git_dir(repo: Path) -> tuple[Path, Path]`
- **function `_head`** [L63-79]: `def _head(repo: Path = REPO) -> str` - HEAD commit id read from the git files (worktree aware; loose or packed refs).
- **function `verify`** [L82-134]: `def verify(path: Path, mailbox: Path = MAILBOX, out: Path | None = None) -> dict` - Return the release dict if every binding holds; ReleaseError otherwise.
- **function `_runtime_mode`** [L137-142]: `def _runtime_mode(mailbox: Path)`
- **function `_verify_issuer`** [L145-178]: `def _verify_issuer(rel: dict, mailbox: Path) -> None` - Bind the issuer: Claude by its assumption record; Codex only while not relinquished.
- **function `_owner_record`** [L181-190]: `def _owner_record(rel: dict) -> dict`
- **function `scoring_authority`** [L193-203]: `def scoring_authority(rel: dict) -> ScoringAuthority` - The ONLY issuer of ScoringAuthority: a verified release with an owner scoring record.

