# `tools/hws/hws_records.py`

- Source: [tools/hws/hws_records.py](../../../../../tools/hws/hws_records.py)
- Kind: python
- Lines: 370

## Module docstring

> HWS records: STAGES events, histories, look records, tree hashes, resume archive,
> FREEZE.json, the REPORT and SELECTION writers (API.md §6.1, §6.3-§6.5; erratum E8-E10, E14;
> ruling R-0118-6). Writes only inside the store `out`, by exclusive create (append-only:
> STAGES.jsonl). Reads no payload; G0 never opens excluded paths.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](hws_worlds.py.md) (line 20, via same directory)
- `import hws_select` -> [tools/hws/hws_select.py](hws_select.py.md) (line 21, via same directory)
- `import hws_stats` -> [tools/hws/hws_stats.py](hws_stats.py.md) (line 22, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 25, via unique basename)
- `from topo_pilot.contracts import canonical_json` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 26, via package root)
- `from topo_pilot.process import EmissionConfig, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 27, via package root)
- `from topo_pilot.world import WorldConfig` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 23)
- `scipy` (lines 24)

### Standard library

- `__future__` (lines 7)
- `dataclasses` (lines 16)
- `fractions` (lines 17)
- `hashlib` (lines 9)
- `json` (lines 10)
- `math` (lines 11)
- `pathlib` (lines 18)
- `platform` (lines 12)
- `shutil` (lines 13)
- `subprocess` (lines 14)
- `time` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hws/hws_driver.py](hws_driver.py.md) (line 19, import)
- [tools/hws/hws_driver.py](hws_driver.py.md) (line 23, import)
- [tools/hws/hws_driver.py](hws_driver.py.md) (line 24, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 18, import)
- [tools/hws/hws_known.py](hws_known.py.md) (line 19, import)

## Top-level constants

- `EFFECT_KS`
- `FREEZE`
- `IDENT`

## Classes and functions

- **function `utc`** [L35-36]: `def utc() -> str`
- **function `sha_bytes`** [L39-40]: `def sha_bytes(data: bytes) -> str`
- **function `append_stage_event`** [L43-47]: `def append_stage_event(out, event: dict) -> None`
- **function `stage_events`** [L50-53]: `def stage_events(out) -> list`
- **function `save_hist`** [L56-61]: `def save_hist(out, stage, key, tok, origin=None) -> Path`
- **function `_files`** [L64-71]: `def _files(out, prefixes) -> dict`
- **function `tree_sha`** [L74-75]: `def tree_sha(out, prefixes) -> str`
- **function `archive_partial`** [L78-98]: `def archive_partial(out, stage)` - RC-5 resume (choice 40): unlisted files of the interrupted stage go to superseded/.
- **function `num`** [L104-116]: `def num(x)` - JSON-safe copy: numpy scalars to Python, Fractions to strings, keys to str.
- **function `_ediff`** [L119-122]: `def _ediff(kl, h4, hl) -> dict`
- **function `_all_finite`** [L125-130]: `def _all_finite(rows) -> bool`
- **function `boot_arrays`** [L133-141]: `def boot_arrays(rows) -> dict` - Choice 21: D_K, B_K, V_K, G_K at the effect Ks present, G0, G4A, IZ4, IX4, Hq[L].
- **function `_ident`** [L144-147]: `def _ident(proc, exact, stage, n) -> dict`
- **function `_report`** [L150-159]: `def _report(rows, exact, lh, g4_mean) -> dict`
- **function `look_record`** [L162-205]: `def look_record(proc, exact, look, stage, n, floors=None, seed=None) -> dict` - §6.4 per-world-look aggregate. A bootstrap seed (S3: 620103, S0: 620101) adds the
- **function `write_look`** [L208-213]: `def write_look(out, rec, origin=None) -> Path`
- **function `exact_record`** [L216-220]: `def exact_record(proc, exact, stage) -> dict` - Record of a world excluded by E1-E4 before sampling (never sampled; no bounds).
- **function `_git`** [L226-227]: `def _git(repo, *args) -> bytes`
- **function `implementation_files`** [L230-234]: `def implementation_files(repo, h_exec) -> dict`
- **function `_hashes`** [L237-248]: `def _hashes(repo) -> dict`
- **function `freeze`** [L251-266]: `def freeze(out, repo, h_exec, dry_report) -> dict` - §6.5 FREEZE.json by exclusive create, bound to h_exec and the dry-run report.
- **function `verify_freeze`** [L269-281]: `def verify_freeze(out, repo) -> dict` - Every stage job checks FREEZE.json against the working tree before any sampling.
- **function `report_record`** [L287-308]: `def report_record(state, oc, extra) -> dict` - §6.4 REPORT.json from the outcome state and run extras (x1, s2, cpu, nulls, hashes).
- **function `write_report`** [L311-315]: `def write_report(out, report) -> Path`
- **function `_arr_sha`** [L318-319]: `def _arr_sha(a) -> str`
- **function `selection_record`** [L322-346]: `def selection_record(proc, rec_s3, oc, extra) -> dict` - §10.1 hand-off package (written only for HWS_SELECTED, choice 32).
- **function `write_selection`** [L349-352]: `def write_selection(out, sel) -> Path`
- **function `write_world_summaries`** [L355-370]: `def write_world_summaries(out, history) -> list` - worlds/<key>.json once per evaluated world: every look path and sha256, latest class.

