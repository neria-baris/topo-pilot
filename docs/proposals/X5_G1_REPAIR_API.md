# X5 G1 audit repairs — API specification (job 0007)

**Purpose.** These repairs implement the coordinator's job-0006 review items without changing any numerical scientific rule:

* full-hash payload verification before **and** after computation;
* STOP and budget guards around exports;
* an atomic, preserving ledger with the termination cause;
* immutable output versions.

**Location.** `src/topo_pilot/experiment/x5g1_safety.py`, with changes to `x5g1_controls.RunControls`.

**Conventions.** Errors are `StageFailure` from contracts or the named exception classes below.

## 1. `x5g1_controls.RunControls` (changed behaviour)

* **Atomic ledger write.** The JSON is written to `ledger_path.with_suffix(".json.tmp")` and then moved over the ledger with `os.replace`.
* **Never lose history.** All existing entries are preserved, and `cumulative_cpu_s` is the previous value plus this run's CPU.
* **Unreadable ledger.** If the existing ledger cannot be parsed, `__init__` raises `LedgerCorrupt(RuntimeError)`, and the file is **not** overwritten.
* **Termination cause.** Each entry gains a `"cause"` field: `None` for a normal exit, otherwise `"<ExceptionName>: <message>"`.
* **Existing statuses kept:** `ok`, `stopped`, `budget`, `error:<Name>`.
* **Documented limitation.** `try/finally` cannot record CPU used by a process that is killed abruptly (task kill, power loss). Such costs are absent from the ledger and must be reported as unknown.

## 2. `x5g1_safety.py`

```python
class OutputExists(FileExistsError): ...
class SourceTampered(RuntimeError): ...
```

```python
def verify_sources_full(store: ArtifactStore, expected: dict[str, tuple[type, str]],
                        consumer: str = "experiment") -> list[str]
```

* `expected` maps artifact_id to (artifact class, full 64-hex payload_sha256).
* For each artifact:
  1. `store.meta(aid).payload_sha256` must **equal** the expected full hash. Prefix matching is not allowed.
  2. `store.load(cls, aid, consumer=consumer)` must succeed. This re-hashes the stored payload, so an in-place payload change that left the metadata intact is detected.
* Returns failure strings. It never raises: any exception becomes a failure string.

```python
def checked_computation(store: ArtifactStore, expected: dict[str, tuple[type, str]],
                        fn: Callable[[], T]) -> T
```

* Calls `verify_sources_full` before `fn()`. Any failure raises `SourceTampered("before: …")` without calling `fn`.
* Runs `fn()`, then calls `verify_sources_full` again. Any failure raises `SourceTampered("after: …")`, and **the result is discarded**: it is not returned.
* Otherwise returns `fn()`'s result.

```python
def ensure_new_output_dir(path: Path) -> Path
```

* If `path` exists and contains any entry, raises `OutputExists` (nothing is deleted or modified).
* Otherwise creates it (with parents) and returns it.
* An existing empty directory is accepted.

```python
def guarded_export(ctl: RunControls, steps: list[tuple[str, Callable[[], None]]],
                   status_path: Path) -> None
```

* For each (name, fn) in order: `ctl.guard(f"export {name}")`, then `fn()`, then `ctl.guard(f"export {name} done")`.
* If `StopRequested` or `BudgetExceeded` is raised at any point:
  1. write a small JSON at `status_path`: {"status": "STOPPED_DURING_EXPORT" or "BUDGET_DURING_EXPORT", "completed_steps": [...], "cause": "<Name>: <msg>"};
  2. **skip all remaining steps**;
  3. re-raise the same exception, so that the ledger records `stopped` or `budget` with the cause.
* Other exceptions propagate unchanged, without writing a status file.

## 3. Required independent regressions

* **Source tampering after computation:** in a MemoryBackend store, mutate a saved payload (or meta hash) inside `fn` → `SourceTampered("after…")`, and the result is not returned.
* **Prefix-only hashes are rejected:** a correct 16-hex prefix → failure.
* **Missing artifact or broken backend:** reported as a failure string, never raised.
* **Cancellation during export:** create the STOP file inside step 1 → step 2 does not run; the status file has STOPPED_DURING_EXPORT; the ledger entry has status `stopped` and a non-null cause.
* **Budget during export:** BudgetExceeded during export → BUDGET_DURING_EXPORT.
* **Atomic ledger preservation:**
  - two prior entries survive a new run that raises;
  - cumulative = previous + this run;
  - no `.tmp` file remains;
  - a corrupt ledger raises LedgerCorrupt and keeps its bytes unchanged.
* **Immutable outputs:** a non-empty directory → OutputExists, with its content unchanged; a new or empty directory is accepted.

## 4. Job 0008 additions (export integration and ledger validation)

### 4.1 `x5g1_main._export(repo, main_root, out_root, tables, res, ctl)`

This is the real gate-driver export path. Inputs:

* `res` holds:
  - "provenance": a list of {"artifact_id": …};
  - "T_a020_id";
  - "arms": {arm: {"obs_id", "GC", "GC_stationary", "two_token_regret", "context"}} for arms a0 and a020;
  - "verdict", "reason", "global_failed" and "global_inconclusive".
* `ctl` is an entered `RunControls`.

Behaviour:

* The parents of the MetricRecords are every ID in provenance, plus T_a020_id and the obs_ids. They must exist in the main store (a `LocalFSBackend` at `main_root`).
* **The only scientific store save** (one MetricRecords into `out_root/store`) is the **first guarded export step**, named "metric_records". It runs only if IDs exist and `global_failed` is empty. The table writes follow (verdict.json, result.json, run.json), then the manifest, all via `guarded_export` with status file `tables/EXPORT_STATUS.json`.
* **STOP present before `_export`:** StopRequested propagates, **no `ArtifactStore.save` call happens**, no MetricRecords directory is created, and the status file shows completed_steps [].
* **STOP created during the save step:** that save completes, the remaining steps are skipped, and the status file shows completed_steps ["metric_records"].
* **Normal run:** exactly one save; run.json contains "metric_records_id"; MANIFEST.json lists the written files.
* **`global_failed` non-empty:** no save, and the tables are still written.

### 4.2 `RunControls` ledger validation

* LedgerCorrupt is raised at construction, with the file left byte-identical, when:
  - `cumulative_cpu_s` is not a finite, non-negative number (NaN, ±inf, negative, a bool or a string);
  - `entries` is not a list (for example a string or a dict);
  - any entry is not an object.
* A valid ledger whose run raises inside the `with` block keeps all prior entries, and its cumulative CPU is ≥ the prior value.
