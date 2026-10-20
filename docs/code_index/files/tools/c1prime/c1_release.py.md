# `tools/c1prime/c1_release.py`

- Source: [tools/c1prime/c1_release.py](../../../../../tools/c1prime/c1_release.py)
- Kind: python
- Lines: 157

## Module docstring

> C1' coordinator release (API.md §13; protocol §17, §18 field 2). Same checks as K4's
> release.py (provenance: tools/x4_circle_history/release.py, Claude-issuer branch), separately
> versioned: schema c1prime-release-v1, C1 stages, issuer "claude-coordinator" only, plus the
> stage-specific bindings of R1 (authority, registry v1) and R3 (N_test, k, registry v2).

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 12, via same directory)

### External (third-party)

- none

### Standard library

- `__future__` (lines 6)
- `hashlib` (lines 8)
- `json` (lines 9)
- `pathlib` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_release_meter.py](../../tests/c1prime/test_a_release_meter.py.md) (line 35, import)
- [tests/c1prime/test_c_release_worker.py](../../tests/c1prime/test_c_release_worker.py.md) (line 19, import)
- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 17, import)
- [tools/c1prime/c1_meter_bind.py](c1_meter_bind.py.md) (line 110, import)

## Top-level constants

- `ASSUMPTION_SCHEMA`
- `CLAUDE_ACTIVE_MODE`
- `ISSUER`
- `MAILBOX`
- `REQUIRED`
- `SCHEMA`
- `STAGES`

## Classes and functions

- **class `ReleaseError(RuntimeError)`** [L25-26] - Missing, malformed or mismatching C1 release.
- **function `_sha`** [L29-30]: `def _sha(path) -> str`
- **function `_json`** [L33-37]: `def _json(path)`
- **function `_git_dirs`** [L40-51]: `def _git_dirs(repo: Path) -> tuple`
- **function `git_head`** [L54-68]: `def git_head(repo=c1_config.REPO) -> str`
- **function `_bound_file`** [L71-75]: `def _bound_file(ref, what) -> None`
- **function `_verify_issuer`** [L78-94]: `def _verify_issuer(rel: dict, mailbox: Path) -> None`
- **function `_stage_fields`** [L97-111]: `def _stage_fields(rel: dict) -> None`
- **function `authorized_worker`** [L114-124]: `def authorized_worker(rel: dict, path) -> str` - The executing worker session (protocol §18: "the authorized executing worker session").
- **function `verify`** [L127-157]: `def verify(path, mailbox=MAILBOX, out=None, head=None, contract_path=c1_config.CONTRACT_PATH) -> dict`

