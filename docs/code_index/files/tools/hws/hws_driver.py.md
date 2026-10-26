# `tools/hws/hws_driver.py`

- Source: [tools/hws/hws_driver.py](../../../../../tools/hws/hws_driver.py)
- Kind: python
- Lines: 361

## Module docstring

> HWS driver: G0, stages S0, S1, X1, S2, S3, the null re-check, pauses, resume and the CLI
> (API.md §6.2, §10, §11; erratum E8-E10, E14). Records, report and SELECTION writers live in
> hws_records (R-0118-6) and are re-exported here under their API names. The synthetic dry run
> (DR1-DR13) and stage S0 live in hws_known/hws_dry (erratum E16); running them is metered work.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](hws_worlds.py.md) (line 15, via same directory)
- `import hws_exact` -> [tools/hws/hws_exact.py](hws_exact.py.md) (line 16, via same directory)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](hws_oracle.py.md) (line 17, via same directory)
- `import hws_records` -> [tools/hws/hws_records.py](hws_records.py.md) (line 18, via same directory)
- `import hws_select` -> [tools/hws/hws_select.py](hws_select.py.md) (line 19, via same directory)
- `import hws_stats` -> [tools/hws/hws_stats.py](hws_stats.py.md) (line 20, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 21, via unique basename)
- `from hws_records import append_stage_event, archive_partial, freeze, save_hist` -> [tools/hws/hws_records.py](hws_records.py.md) (line 22, via same directory)
- `from hws_records import look_record, tree_sha` -> [tools/hws/hws_records.py](hws_records.py.md) (line 23, via same directory)
- `from topo_pilot.contracts import SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 24, via package root)
- `import hws_known` -> [tools/hws/hws_known.py](hws_known.py.md) (line 189, via same directory) (inside a function)
- `import hws_dry` -> [tools/hws/hws_dry.py](hws_dry.py.md) (line 196, via same directory) (inside a function)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 322, via unique basename) (inside a function)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 323, via unique basename) (inside a function)
- `from topo_pilot.contracts import StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 324, via package root) (inside a function)

### External (third-party)

- none

### Standard library

- `__future__` (lines 7)
- `argparse` (lines 9)
- `json` (lines 10)
- `os` (lines 11)
- `pathlib` (lines 13)
- `time` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- `import errors` (line 321): `src/topo_pilot/contracts/errors.py`, `tools/x4_circle_history/errors.py`

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hws/test_b_kc1.py](../../tests/hws/test_b_kc1.py.md) (line 35, import)
- [tests/hws/test_b_records.py](../../tests/hws/test_b_records.py.md) (line 31, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 14, import)
- [tools/hws/hws_known.py](hws_known.py.md) (line 16, import)

## Top-level constants

- `SKIP_DIRS`
- `SWEEP`
- `TEXT_SUFFIXES`
- `TINY`

## Classes and functions

- **class `Paused(RuntimeError)`** [L35-36] - A 3x trigger fired at a world or stage boundary (§9.3); exit 4.
- **function `_rel`** [L39-40]: `def _rel(out, path) -> str`
- **function `_gate`** [L43-44]: `def _gate(out, gate, status, **details) -> str`
- **function `_skip_dir`** [L50-53]: `def _skip_dir(parent: Path, name: str) -> bool`
- **function `seed_search`** [L56-70]: `def seed_search(root, needles) -> list` - §6.6 G0 discovery search; excluded folders are pruned before any listing or open.
- **function `classify_seed_hits`** [L73-82]: `def classify_seed_hits(hits) -> dict`
- **function `g0`** [L85-93]: `def g0(out, root=hw.ROOT, stage='S0') -> dict`
- **function `_json`** [L99-100]: `def _json(path)`
- **function `_preflight`** [L103-116]: `def _preflight(out, stages, auth)` - FREEZE (missing: refusal; mismatch: FAIL_TECHNICAL/FREEZE) and AUTH, before sampling.
- **function `_ledger_cpu`** [L119-121]: `def _ledger_cpu(out) -> float`
- **function `_pause`** [L124-133]: `def _pause(ctx, stage, stage_cpu, stage_fc) -> None` - §9.3 both triggers at a world or stage boundary; a continued stage is exempt.
- **function `_spot`** [L139-148]: `def _spot(proc, tok) -> dict` - §8 S3 spot checks (E6) and the tier-0 report-only law bound.
- **function `null_recheck`** [L151-162]: `def null_recheck(out, proc, stage, look, n, Ks) -> dict` - §5.3 item 5: one fresh NULLCHK look; halt only if the same null exceeds again.
- **function `world_record`** [L165-184]: `def world_record(out, proc, exact, stage, n, Ks, floors, seed=None, known=False, origin=None)` - One world-look: sample once, keep the tokens, aggregate, null rule, write the record.
- **function `run_s0`** [L187-191]: `def run_s0(out, auth) -> dict` - §3 stage S0 (KC1-KC14); implemented in hws_known (erratum E16).
- **function `run_dry`** [L194-198]: `def run_dry(out=hw.DRY_STORE) -> dict` - §13 synthetic dry run DR1-DR13; implemented in hws_known (erratum E16).
- **function `_stage`** [L204-250]: `def _stage(ctx, stage, worlds, kinds=None) -> list` - One stage over its worklist with resume at world boundaries (RC-5, choice 40).
- **function `_accept`** [L253-260]: `def _accept(out, s0_accept)`
- **function `_world_of`** [L263-264]: `def _world_of(r)`
- **function `run_sweep`** [L267-313]: `def run_sweep(out, auth, s0_accept, cont=None) -> dict` - S1 -> (X1) -> (S2) -> S3 under the frozen rules (§6), then the outcome and report.
- **function `status_of`** [L319-330]: `def status_of(exc) -> str` - Choice 43 exception map.
- **function `main`** [L333-357]: `def main(argv=None) -> int` - Exit codes: 0 complete, 2 refused (nothing sampled), 3 STOP, 4 PAUSE.

