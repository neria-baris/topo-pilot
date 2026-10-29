# `tools/k4b/k4b_driver.py`

- Source: [tools/k4b/k4b_driver.py](../../../../../tools/k4b/k4b_driver.py)
- Kind: python
- Lines: 395

## Module docstring

> K4b release-A driver: G0 -> P1 (API.md §9; protocol §6 gate table, §11.8 stage records).

## Imports

### Internal (repo files)

- `import k4b_config` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 15, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](k4b_cert.py.md) (line 16, via same directory)
- `import k4b_charts` -> [tools/k4b/k4b_charts.py](k4b_charts.py.md) (line 17, via same directory)
- `import k4b_data` -> [tools/k4b/k4b_data.py](k4b_data.py.md) (line 18, via same directory)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](k4b_registry.py.md) (line 19, via same directory)
- `import k4b_release` -> [tools/k4b/k4b_release.py](k4b_release.py.md) (line 20, via same directory)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](k4b_scores.py.md) (line 21, via same directory)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](k4b_stats.py.md) (line 22, via same directory)
- `import op_guard` -> [tools/x4_circle_history/op_guard.py](../x4_circle_history/op_guard.py.md) (line 24, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 25, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 26, via unique basename)
- `from c1_records import C1GateFailure, classify_exception` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 27, via unique basename)
- `from k4b_config import MODELS, SEEDS, check_checkpoint_meta, expected_meta` -> [tools/k4b/k4b_config.py](k4b_config.py.md) (line 28, via same directory)
- `from topo_pilot.contracts import ArtifactStore, Checkpoint` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 138, via package root) (inside a function)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 139, via package root) (inside a function)
- `import c1_cert` -> [tools/c1prime/c1_cert.py](../c1prime/c1_cert.py.md) (line 169, via unique basename) (inside a function)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 170, via unique basename) (inside a function)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 171, via unique basename) (inside a function)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 274, via unique basename) (inside a function)
- `import k4b_decoder` -> [tools/k4b/k4b_decoder.py](k4b_decoder.py.md) (line 283, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 23)
- `torch` (lines 172)

### Standard library

- `__future__` (lines 7)
- `argparse` (lines 9)
- `hashlib` (lines 10)
- `json` (lines 11)
- `pathlib` (lines 13)
- `time` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_b_binding.py](../../tests/hwsc/test_b_binding.py.md) (line 171, import)
- [tests/hwsc/test_b_records.py](../../tests/hwsc/test_b_records.py.md) (line 35, import)
- [tests/k4b/test_b_flow.py](../../tests/k4b/test_b_flow.py.md) (line 25, import)
- [tests/k4b/test_b_h1_meta.py](../../tests/k4b/test_b_h1_meta.py.md) (line 30, import)
- [tests/k4b/test_b_rerun.py](../../tests/k4b/test_b_rerun.py.md) (line 24, import)
- [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 17, import)
- [tools/hwsc/hwsc_driver.py](../hwsc/hwsc_driver.py.md) (line 19, import)
- [tools/hwsc/hwsc_dry.py](../hwsc/hwsc_dry.py.md) (line 27, import)
- [tools/hwsc/hwsc_gates.py](../hwsc/hwsc_gates.py.md) (line 20, import)
- [tools/hwsc/hwsc_jobs.py](../hwsc/hwsc_jobs.py.md) (line 19, import)
- [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 23, import)
- [tools/k4b/k4b_fresh.py](k4b_fresh.py.md) (line 20, import)

## Top-level constants

- `ARTIFACTS`
- `AUTHORITY_FILES`
- `GATE_ORDER`
- `IDENTITY`
- `K4_FREEZE`
- `OWNER_DIR`

## Classes and functions

- **function `_sha`** [L41-42]: `def _sha(path) -> str`
- **function `_utc`** [L45-46]: `def _utc() -> str`
- **function `run_gates`** [L49-67]: `def run_gates(out, steps) -> list`
- **function `begin_stage`** [L70-74]: `def begin_stage(out, stage) -> None`
- **function `complete_stage`** [L77-84]: `def complete_stage(out, stage, files) -> dict`
- **function `classify_seed_hits`** [L87-91]: `def classify_seed_hits(hits) -> dict` - RC5: PASS iff every hit is this lineage's declaration; anything else fails closed.
- **function `_stage_dir`** [L94-97]: `def _stage_dir(out, stage) -> Path`
- **function `g0`** [L100-134]: `def g0(out, release, mailbox) -> dict`
- **function `load_checkpoint`** [L137-142]: `def load_checkpoint(artifact_id)`
- **function `checkpoint_meta`** [L145-153]: `def checkpoint_meta(artifact_root, artifact_id) -> dict` - API.md §14.1: reads only <root>/Checkpoint/<id>/meta.json.
- **function `check_checkpoints`** [L156-165]: `def check_checkpoints(artifact_root=ARTIFACTS) -> dict` - All six meta checks before any checkpoint load; the first non-PASS raises.
- **function `h1`** [L168-198]: `def h1(out, ctx) -> dict`
- **function `reg1`** [L201-212]: `def reg1(out, ctx) -> dict`
- **function `h2`** [L215-240]: `def h2(out, ctx) -> dict`
- **function `oracle_val`** [L243-258]: `def oracle_val(out, ctx) -> dict`
- **function `b4_val`** [L261-270]: `def b4_val(out, ctx) -> dict`
- **function `_acts`** [L273-279]: `def _acts(ctx, split) -> dict`
- **function `c0_cal_stage`** [L282-308]: `def c0_cal_stage(out, ctx) -> dict`
- **function `c0_val_stage`** [L311-321]: `def c0_val_stage(out, ctx) -> dict`
- **function `cert_val`** [L324-343]: `def cert_val(out, ctx) -> dict`
- **function `p1`** [L346-371]: `def p1(out, ctx) -> dict`
- **function `main`** [L374-391]: `def main(argv=None) -> int`

