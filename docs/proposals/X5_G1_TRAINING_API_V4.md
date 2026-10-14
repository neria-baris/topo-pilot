# X5 G1 training-study implementation — API contract v4 (x5g1-train-v4; job 0010)

This contract is for the builder and the independent test writers. It covers [protocol v4](X5_G1_TRAINING_PROTOCOL_V4.md).

* [API v3](X5_G1_TRAINING_API.md) is preserved. Its §1 (endpoint), §2 (lineage), §3 (oracle), §4 (score), §6 (train composition) and §9 (clarifications) remain in force, except where this document changes them.
* v4 changes the runtime controls (§2 here), and adds a usage latch (§1), a config validator (§3), complete exports (§4), integrity and identity checks (§5) and the stage integration (§6).
* Errors are the named classes below, or the existing `StopRequested`, `BudgetExceeded` and `LedgerCorrupt` (`x5g1_controls`), `OutputExists` (`x5g1_safety`), and `RunLocked` and `ResourceExceeded` (`x5g1t_runtime`).

## 1. `topo_pilot.experiment.x5g1t_usage` (worker self-hold latch; pure decision + file apply)

### Constants

```python
THRESHOLD_PERCENT = 85
LATCH_NAME = "usage_hold_latch.json"; LATCH_SCHEMA = "usage-hold-latch-v1"
```

### `UsageMalformed(ValueError)`

Raised for a malformed usage file or latch. Callers treat it as **STOP** (fail closed).

### `parse_utc(text) -> datetime`

* Parses an ISO 8601 timestamp **with** a `Z` or `±hh:mm` offset, with 0–7 fractional digits (PowerShell `"o"` format), into an aware UTC datetime.
* A naive timestamp, a non-string or an unparseable value raises `UsageMalformed`.

### `blocking_limits(usage, threshold=THRESHOLD_PERCENT) -> list[dict]`

**Validation.** `usage` is the parsed `claude_usage.json`. It must be a dict with:

* `observability` in {"OBSERVED", "UNAVAILABLE"};
* `limits` a list of dicts, each with:
  - `kind`: a str;
  - `relevant`: a bool;
  - `used_percent`: `None` or a finite non-bool number in [0, 100];
  - `warning`: `None` or a str.

Anything else raises `UsageMalformed`.

**Returns** the relevant limits that block:

* any relevant limit with a non-null `warning`, whatever the observability;
* if `observability == "OBSERVED"`, also any relevant limit with `used_percent >= threshold`.

`UNAVAILABLE` with no warnings returns `[]`. UNAVAILABLE is never a hold by itself.

### `make_latch(blocking, source, now) -> dict`

Returns `{"schema": LATCH_SCHEMA, "set_at_utc": now.isoformat(), "source": source, "blocking": [{"kind", "used_percent", "warning"}...]}`.

### `latch_clears(latch, usage, threshold=THRESHOLD_PERCENT) -> tuple[bool, str]`

**Validation.** The latch must have the schema, a parseable `set_at_utc` and a non-empty `blocking` list of dicts with a str `kind`. Otherwise `UsageMalformed`.

**The latch clears (True) only if all of these hold:**

* `usage["observability"] == "OBSERVED"`;
* `usage["source"]` is a str other than `"unavailable"`;
* `parse_utc(usage["observed_at_utc"]) > parse_utc(latch["set_at_utc"])`, i.e. **new** evidence;
* for **every** latched kind, a limit of that kind exists in `usage["limits"]` with `relevant is True`, a numeric `used_percent < threshold` and `warning is None`;
* `blocking_limits(usage)` is empty.

Otherwise it returns `(False, reason)`. Elapsed time, reset times and the runtime mode are never consulted.

### `UsageDecision(action, reasons, set_latch, clear_latch)`

A NamedTuple; `action` is `"CONTINUE"` or `"HOLD"`.

### `usage_decision(usage, latch, now, threshold=THRESHOLD_PERCENT) -> UsageDecision`

`usage` and `latch` may each be `None` (file missing).

| Case | Result |
|---|---|
| latch present and `latch_clears` | CONTINUE, `clear_latch=True`, unless the current usage blocks: then HOLD with a new latch, `set_latch` |
| latch present and not cleared | HOLD |
| no latch and `blocking_limits(usage)` non-empty | HOLD, `set_latch=make_latch(...)` |
| otherwise | CONTINUE |

A missing usage file with a latch present means HOLD.

### `apply_usage(mailbox, now=None) -> tuple[str, tuple[str, ...]]`

* Reads `mailbox/"claude_usage.json"` and `mailbox/LATCH_NAME` (utf-8-sig) and calls `usage_decision`.
* It then atomically writes the latch, or archives it on clearing to `mailbox/f"usage_hold_latch.cleared-{stamp}.json"`, together with the clearing evidence.
* Returns `(action, reasons)`.
* `UsageMalformed`, including unparseable JSON, propagates.

## 2. `x5g1t_runtime.read_controls(mailbox, now=None) -> ControlState` (v4 revision)

The v3 rules hold, plus the following. Precedence is **STOP > HOLD > CONTINUE**.

**`runtime_state.json` mode allow-list.**

| Mode | Effect |
|---|---|
| `WORKING`, `WAITING`, `USAGE_READY` | no-op |
| `WAIT_USAGE_RESET`, `RUNTIME_BLOCKED`, `NEEDS_USAGE_INFO` | HOLD |
| anything else: a missing `mode`, a non-string, an unknown string | STOP (fail closed) |
| a missing file | no-op |

**Usage evidence.** `apply_usage(mailbox, now)` runs on every call. HOLD adds its reasons. `UsageMalformed` gives STOP with the reason `usage_malformed:...`.

**Precedence of sources.**

* A coordinator `WAIT_USAGE_RESET` holds whatever the usage evidence says.
* An actual blocking usage reading holds even when `worker_control` says `CONTINUE`.
* STOP from any source wins over everything.

`hold_while_needed`, `StudyControls` (including `sleep` and `poll_s`), `RunLock`, the outcomes, `BudgetPlanner`, `EST`, `interval_estimate`, `evaluation_reserve`, `check_resources` and `dir_size` are unchanged.

## 3. `topo_pilot.experiment.x5g1t_config`

### `ConfigInvalid(RuntimeError)`

### `StudyConfig`

A frozen dataclass with **exactly** these keys. An unknown key, a missing key, a wrong type or malformed JSON raises `ConfigInvalid`.

| Key | Type |
|---|---|
| `mode` | "production" or "synthetic-fixture" |
| `protocol` | str |
| `protocol_doc` | str, relative to the repo |
| `protocol_doc_sha256` | 64-hex string |
| `read_roots` | list[str] |
| `study_root` | str |
| `ledger_path` | str |
| `mailbox` | str |
| `sources` | `{"world": [id, sha], "T": {"a0": [id, sha], "a020": [id, sha]}, "E": [id, sha]}` |
| `source_producers` | `{id: producer_version}` for the world, T and E IDs |
| `stored_checkpoint` | `[id, sha]` or null |
| `masters` | list |
| `sizes` | `{"train", "dev", "test"}` ints |
| `model_config` | dict |
| `steps` | int |
| `grid` | list[int] |
| `gc` | `{"a0", "a020"}` floats |
| `threads` | int |
| `bootstrap_draws` | int |
| `cap_s` | float |
| `cumulative_cap_s` | float |
| `check_stored_ids` | bool |
| `env` | `{name: str}` |

It also exposes `.root` = `Path(study_root)`.

### `load_config(path) -> StudyConfig`

Loads the JSON. `ConfigInvalid` as above.

### `ProductionSpec` and `PRODUCTION`

`ProductionSpec` is a frozen dataclass; `PRODUCTION` holds the frozen protocol-v4 values:

| Field | Value |
|---|---|
| protocol | `"x5g1-train-v4"` |
| protocol document | its path and sha256 |
| world | `21feee1d8ee5422e` WorldSpec b6f0746e…f77f |
| T a0 | `e4dafc7b9785c172` TransitionSpec f94340a6…68dd |
| T a020 | `08a22a03727d2295` TransitionSpec 663d0011…6b7b |
| E | `3633ac27dab50cf4` EmissionSpec f5b6197c…b1fb |
| source producers | as stored |
| stored checkpoint | `c3358e3cb9c352fb`, bcd024ef…f8596b; its stored model and train configs |
| masters | (310001, 310002, 310003) |
| sizes | 131072 / 4096 / 4096 |
| steps | 5000 |
| grid | `X5_GRID` |
| G_C | 0.27133797235249024 / 0.2939268960103646 |
| bootstrap draws | 2000 |
| threads | 1 |
| caps | 21600 / 21600 |
| stored-ID check | `check_stored_ids` True |
| env | `{"OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "OMP_NUM_THREADS": "1"}` |
| roots | the three read roots, the study root, the ledger and the mailbox (absolute) |
| lineage | `NAMESPACE`, `CODES` and the stream tail ("cylinder", "overlap", "1.25") |

### `ProductionSpec` fields (exact)

| Field | Type |
|---|---|
| `protocol` | str |
| `protocol_doc` | str |
| `protocol_doc_sha256` | str |
| `read_roots` | tuple[str, ...] |
| `study_root` | str |
| `ledger_path` | str |
| `mailbox` | str |
| `sources` | dict, shaped like the config |
| `source_producers` | dict |
| `stored_checkpoint` | tuple[str, str] |
| `stored_model_config` | dict |
| `stored_train_config` | dict, the stored E3 dict |
| `masters` | tuple |
| `sizes` | dict |
| `steps` | int |
| `grid` | tuple[int, ...] |
| `gc` | dict |
| `threads` | int |
| `bootstrap_draws` | int |
| `cap_s` | float |
| `cumulative_cap_s` | float |
| `check_stored_ids` | bool |
| `env` | dict |
| `lineage` | dict: `{"namespace": str, "codes": dict, "stream_tail": tuple}` |

**Tests can build a synthetic spec** with `dataclasses.replace(PRODUCTION, ...)`, pointing it at temporary stores and a temporary repo that holds a protocol document.

The validator reads the stored checkpoint's `meta.config["model_config"]` and `meta.config["train_config"]`. Any Checkpoint artifact saved with such a config can serve as the stored checkpoint in a test.

### `validate_config(cfg, repo, spec=PRODUCTION) -> dict`

* **Read-only.** No file or directory is created.
* Returns a report: resolved roots, the mode, and the checked hashes.
* Raises `ConfigInvalid` **before any sampler, model or output computation**.

**`mode == "production"`.** Every field must equal `spec`:

* Paths are compared after `Path.resolve()` and `os.path.normcase`.
* The repo protocol document's sha256 must equal both `cfg` and `spec`.
* `os.environ` must contain `cfg.env`, which must equal `spec.env`.
* Each source's `meta.artifact_type`, `payload_sha256` and `producer_version` must match, with a full re-hash through `verify_sources_full`.
* The stored checkpoint's metadata must match: type Checkpoint, the payload sha, `model_config == cfg.model_config`, and `dataclasses.asdict(study_train_config(steps, grid))` equal to the stored `train_config` with only `checkpoint_steps` replaced by the grid and `device` by `"cpu"`.
* The lineage constants must match.
* **Write-root safety.** The study root must not equal or lie inside any read root, the repo, or the main repository (the parent of the main artifacts root). The ledger must not lie inside the study root.

**`mode == "synthetic-fixture"`.**

* `protocol` must contain "SYNTHETIC".
* No read root, study root, ledger or mailbox may equal or lie inside any `spec` production root. No source ID may equal a production source ID.
* Structure: positive sizes; a strictly increasing grid with ≥ 3 points, `grid[0] == 0` and `grid[-1] == steps`; positive finite G_C values; masters a non-empty list of ints; `threads >= 1`.
* Sources are verified with full hashes.

**Any other mode** raises `ConfigInvalid`.

## 4. `topo_pilot.experiment.x5g1t_exports`

### `study_export(sc, out, files, arrays=None, reserve=0.0) -> None`

**Steps, in order:**

1. each JSON file in `files`;
2. each npz in `arrays`;
3. `MANIFEST.json`, holding the sha256 of every file written so far;
4. `EXPORT_STATUS.json` = `{"status": "COMPLETE", "completed_steps": [...]}`.

**Per step:** `sc.boundary(f"export {name}", ...)` → write → `sc.boundary(f"export {name} done", ...)`.

**On `StopRequested`, `BudgetExceeded` or `ResourceExceeded`:**

* write `EXPORT_STATUS.json` = `{"status": "STOPPED_DURING_EXPORT" | "BUDGET_DURING_EXPORT" | "RESOURCE_DURING_EXPORT", "completed_steps": [...], "cause": "..."}`;
* write no further file;
* re-raise.

### `verify_export_complete(out) -> dict`

* `StudyFailed`-compatible: it raises `ExportIncomplete(RuntimeError)` unless all of these hold:
  - `EXPORT_STATUS.json` has status `"COMPLETE"`;
  - `MANIFEST.json` exists and every hash matches;
  - the directory holds exactly the manifest files plus the two status files.
* Returns the manifest.

## 5. `topo_pilot.experiment.x5g1t_checks`

### `IntegrityFailed(RuntimeError)`

### `verify_full(store, expected, when) -> None`

* `expected` maps id → (cls, sha).
* Raises `IntegrityFailed` on any `verify_sources_full` failure (metadata hash, re-hash on load, missing).

### `validate_checkpoints(store, outcome, cfg, arm, master, train_pool_id, dev_pool_id) -> dict`

Returns `{checkpoint_id: (Checkpoint, sha)}` and raises `IntegrityFailed` unless:

* the outcome steps equal `list(cfg.grid)`, in order;
* every checkpoint is type Checkpoint, with `meta.payload_sha256` equal to the recorded sha;
* `meta.config == {"run_key": list(study_run_key(master)), "step": step, "model_config": cfg.model_config, "train_config": asdict(study_train_config(cfg.steps, cfg.grid))}`, with the model config compared as `asdict(ModelConfig(**cfg.model_config))`;
* `meta.parent_ids == tuple(sorted({train_pool_id, dev_pool_id}))`;
* the loaded `Checkpoint.observation_id == train_pool_id` and `run_id == "-".join(map(str, study_run_key(master)))`;
* the outcome's `arm` and `master` match.

## 6. `x5g1t_stages` and `x5g1t_main` (v4 integration)

**Every stage** calls `validate_config` first. It runs before `ensure_new_output_dir`, any store open for writing, any sampler and any model.

**Exports** go through `study_export`. `guarded_export` is no longer used by the study drivers.

**Prerequisites** use `verify_export_complete`:

| Stage | Requires complete |
|---|---|
| `train` | `tables/pools` |
| `dev-analysis` | `tables/pools`, plus `tables/train/<arm>_<m>` for each COMPLETE model used |
| `final-test` | `tables/dev_analysis`, plus the pools |

**Integrity.**

* `verify_full` runs on world, T and E plus every **used** pool and checkpoint, before use and again before the result export.
* A failure raises `IntegrityFailed`, and no scientific export happens.
* `validate_checkpoints` runs before any checkpoint is scored.

**Guards.** `sc.boundary` is called:

* before and after each `draw_pair` call (pools and final-test);
* before and after each scientific save;
* before and after **each 512-row scoring batch**: `regret_rows(..., guard=...)` / `p32_log_probs(..., guard=...)`, called with `guard(f"score batch {i}")` and `guard(f"score batch {i} done")`;
* before and after **each oracle batch**: `oracle_q32(..., guard=...)`.

**Fresh test.** Its IDs are collision-checked against all ObservationSet IDs in the read roots **and** the study store's train and dev pools **before** the fresh `draw_pair`. A collision, or a STOP before the draw, means `draw_pair` is never called.

**CLI** `x5g1t_main --config C [--repo R] <stage>`:

* stages: `validate` (read-only report to stdout), `pools`, `train --arm --master`, `dev-analysis`, `final-test --authorized-final`, `fixture --root`;
* exit codes:
  - 0 ok;
  - 2 STOP, budget, resource or hold-stop;
  - 3 refusal: `ConfigInvalid`, `StudyFailed`, `ExportIncomplete`, `IntegrityFailed`, `RunLocked`, `OutputExists`, `LedgerCorrupt` or `UsageMalformed`.

**Synthetic fixture** `x5g1t_fixture.build_fixture(root, sizes=None, steps=6, bootstrap_draws=40, cap_s=21600.0) -> Path`:

* writes a `mode = "synthetic-fixture"` config under `root`;
* its protocol contains "SYNTHETIC";
* its mailbox holds `request.json` = RUN_NEXT.

## 7. Required independent regressions (actual stages and CLI, tiny fixtures)

* **Export STOP (root probe):** a `worker_control` STOP raised during `pools` must not leave `pools.json`, or any scientific file, after the boundary that saw the STOP. `EXPORT_STATUS` is STOPPED_DURING_EXPORT, the ledger records stopped, and a later `train` refuses (exit 3, incomplete prerequisite).
* **The same for a `request.json` STOP**, and for a HOLD released through an injected sleep, after which the run proceeds.
* **STOP before the fresh draw:** `draw_pair` is never called (spy). A collision of the fresh IDs also gives no draw.
* **Guard counts:** the per-batch scoring and oracle guards are actually called in `dev-analysis`.
* **Tampered prerequisites:** an interrupted, tampered or extra-file export cannot advance.
* **Tampered checkpoints:** a reordered list, a wrong parent, a wrong config, or a same-metadata mutated payload gives `IntegrityFailed` and no result export.
* **Config tampering:** each production field (source, G_C, cap, grid, masters, model or train config, env, roots, protocol hash) and an unknown or malformed key are rejected **before** any sampler or model. A synthetic config pointing at production roots is rejected.
* **Usage latch:** a realistic multi-limit or warning hold; unknown values and timestamps; stale evidence; a worker mode edited without fresh clearance; fresh clearance plus coordinator release; STOP priority; `RUNTIME_BLOCKED` holding; UNAVAILABLE alone not holding.
