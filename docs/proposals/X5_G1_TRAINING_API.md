# X5 G1 training-study implementation — API contract (x5g1-train-v3; job 0009)

This is the contract for the builder and for the **independent test writers**. It covers [protocol v3](X5_G1_TRAINING_PROTOCOL_V3.md).

* All randomness comes from `SeedTree`.
* Errors are the named exceptions below, or `StageFailure`.
* "Grid" means a strictly increasing integer tuple; the study grid is `GRID`.

## 1. `topo_pilot.analysis.x5_endpoint` (pure: no I/O, no torch)

### Constants

```python
GRID: tuple[int, ...]     # (0, 100, 200, ..., 1000, 1250, 1500, ..., 5000), 27 points
THRESHOLD = 0.05; DELAY = 250
```

### `pass_sequence(ratios, threshold=THRESHOLD) -> NDArray[bool]`

* Returns `ratios <= threshold`, element-wise.
* `ValueError` if any ratio is NaN.

### `@dataclass(frozen=True) GridEvent`

| Field | Observed | Censored |
|---|---|---|
| `tau: int \| None` | t_j | `None` |
| `lower: float` | t_j | `grid[-3]` |
| `upper: float` | t_j | `inf` |
| `censored: bool` | `False` | `True` |
| `lower_strict: bool` | `False` | `True` |
| `trailing_pass: tuple[int, ...]` | `()` | grid steps among the last two positions whose PASS is `True` (unconfirmed, descriptive) |

### `grid_event(passes, grid=GRID) -> GridEvent`

* Finds the smallest `j <= len(grid) - 3` such that `passes[j]`, `passes[j+1]` and `passes[j+2]` are all true.
* `ValueError` if:
  - `len(passes) != len(grid)`;
  - `len(grid) < 3`;
  - the grid is not strictly increasing;
  - any element is not a bool or `np.bool_`. `None` is rejected: an incomplete curve is a failed model, not an event.

### `@dataclass(frozen=True) DiffBounds` and `difference_bounds(curved, flat) -> DiffBounds`

`DiffBounds` has fields `low`, `high`, `low_strict` and `high_strict`.

* `low = curved.lower - flat.upper` and `high = curved.upper - flat.lower`. Lowers are always finite, so the result is never NaN.
* `low_strict = curved.censored and not flat.censored`.
* `high_strict = flat.censored and not curved.censored`.
* Both censored gives `(-inf, +inf)`.

### `ratio_curve(regret, gc) -> NDArray`

* `regret[R, K]` gives `regret.mean(axis=0) / gc`.
* `ValueError` unless `gc` is finite and > 0, and `R >= 1`.

### `quantile_inverted_cdf(values, q) -> float`

* Returns the k-th smallest value with `k = max(1, ceil(q·n − 1e-9))`, for q in [0, 1].
* It equals `np.quantile(values, q, method="inverted_cdf")` on finite data and also works with ±inf.
* `ValueError` if `values` is empty, contains NaN, or q is outside [0, 1].

### `@dataclass(frozen=True) BootstrapResult`

| Field | Content |
|---|---|
| `d_low` | `NDArray[n_draws]` |
| `d_high` | `NDArray[n_draws]` |
| `censored_curved` | bool array `[n_draws]` |
| `censored_flat` | bool array `[n_draws]` |
| `q025_low` | `quantile_inverted_cdf(d_low, 0.025)` |
| `q975_high` | `quantile_inverted_cdf(d_high, 0.975)` |
| `censored_curved_frac`, `censored_flat_frac` | fractions of censored draws |

### `paired_bootstrap_endpoint(reg_curved, reg_flat, gc_curved, gc_flat, rng, n_draws=2000, batch=500, grid=GRID, threshold=THRESHOLD, guard=None) -> BootstrapResult`

* `reg_*` are `[R, K]` arrays; `R` and `K` must be equal across arms (`ValueError` otherwise), and `K == len(grid)`.
* **Per draw j, in order:** exactly **one** call `idx = rng.integers(0, R, size=R)`, shared by both arms and applied to whole rows. Then ratio curve → PASS → `grid_event` → `difference_bounds`.
* Censored draws are kept.
* `guard(f"bootstrap {start}")` is called before and `guard(f"bootstrap {start} done")` after each batch.

### `@dataclass(frozen=True) PairEvidence`

Fields: `point: DiffBounds`, `q025_low: float`, `q975_high: float`, and `events: tuple[GridEvent, GridEvent]` (curved, flat).

### `pair_evidence(reg_curved, reg_flat, gc_curved, gc_flat, rng, **kw) -> PairEvidence`

* The point events come from the full-sample ratio curves.
* The quantiles come from `paired_bootstrap_endpoint`.

### `pair_flags(ev) -> tuple[bool, bool]`

* `supported = ev.point.low >= DELAY and ev.q025_low > 0`
* `rejected = ev.q975_high < DELAY`

### `cohort_verdict(pairs, failures=(), n_required=3) -> tuple[str, str]`

`pairs` is a sequence of `PairEvidence | None`.

| Verdict | Condition |
|---|---|
| `"INCONCLUSIVE"` | `failures` is non-empty, or `len(pairs) != n_required`, or any entry is `None` |
| `"INCONCLUSIVE"` (contradiction) | all pairs are supported **and** some pair is rejected |
| `"SUPPORTED"` | all pairs are supported (and none rejected) |
| `"REJECTED"` | some pair is rejected (and not all supported) |
| `"INCONCLUSIVE"` | anything else |

The second element is a non-empty reason string.

### `dev_auc(ratios, grid=GRID) -> float`

The trapezoid rule over the actual step values.

## 2. `topo_pilot.experiment.x5g1t_lineage`

### Constants

* `NAMESPACE = "x5g1-train-v1"`, `PROTOCOL = "x5g1-train-v3"`
* `MASTERS = (310001, 310002, 310003)`, `ARMS = ("a0", "a020")`
* `CODES = {"train": 9, "dev": 10, "test": 11}`
* `SIZES = {"train": 131072, "dev": 4096, "test": 4096}`
* `TEST_MASTER = "shared"`

### Functions

| Function | Behaviour |
|---|---|
| `stream(split)` | `(NAMESPACE, split, "cylinder", "overlap", "1.25")`. `StageFailure(INVALID_CONFIG)` for an unknown split. |
| `paired_generators(split, master)` | Two **separately created** generators, `SeedTree(seed_master).generator(*stream(split))`, where `seed_master = 0` for test (`master` must be `"shared"`) and `master` (an int) otherwise. Otherwise `INVALID_CONFIG`. |
| `sequence_ids(split, arm, master, n)` | `(process_code("cylinder", "overlap", "1.25", f"{NAMESPACE}:{split}:{arm}:{master}") << 32) \| (CODES[split] << 28) \| arange(n)`, as int64. `INVALID_CONFIG` for a bad split or arm, or `n` outside `1..2**28`. |
| `draw_pair(kernels, E, perm, pi, split, master, n)` | `{arm: named [n, 33]}`. One `x5g1_lineage.sample_named(T_arm, E, perm, pi, rng_arm, n)` per arm, with the paired generators in `ARMS` order. |
| `pool_observation(split, named, ids, V)` | A validated public `ObservationSet` (split = `split`) |
| `pool_config(split, arm, master)` | `{"role": f"x5g1t-{split}", "protocol": PROTOCOL, "arm": arm, "master": master, "stream": "/".join(stream(split)), "namespace_code": CODES[split]}` |
| `collisions(new, stored)` | `new` is `dict[str, ids]`. Returns `{name: count of ids in stored}`, plus `"internal"`: the number of duplicates across all new IDs. |

## 3. `topo_pilot.experiment.x5g1t_oracle`

### `oracle_q32(T, E, pi, tokens, guard=None, batch=4096) -> NDArray[R, V]`

* Computes `BayesFilter(T, E, pi).run(tokens[:, :32]).q[:, 32]`: the predictive for w33 from the **public history w1..w32 only**.
* Column 33, if present, is never read.
* Tokens are **named**, so `E` is the stored (named) emission matrix.
* `guard` is called before and after each batch.

## 4. `topo_pilot.experiment.x5g1t_score` (exists)

* `p32_log_probs(model, inputs, batch=512)` gives `[R, V]` float64 `log_softmax` at index 32. The training flag is restored. `inputs` must be `[R, 33]`.
* `kl_from_log_probs(q, logp)` gives per-row KL with 0·log 0 = 0. `NUMERICAL_FAILURE` on invalid q or a non-finite result.
* `regret_rows(model, inputs, q, batch=512)` composes the two.

## 5. `topo_pilot.experiment.x5g1t_runtime`

### Controls

**`ControlState(action, reasons)`** is a NamedTuple; `action` is `"CONTINUE"`, `"HOLD"` or `"STOP"`.

**`read_controls(mailbox: Path) -> ControlState`**, in precedence order **STOP > HOLD > CONTINUE**:

| Source | STOP | HOLD | Missing |
|---|---|---|---|
| `mailbox/STOP` exists | reason `"owner_stop_file"` | — | — |
| `request.json` | its command is `"STOP"`; **missing, unparseable, or a command other than `RUN_NEXT`/`STOP`** also gives STOP (fail closed) | — | STOP |
| `worker_control.json` | `"STOP"`, or a malformed file or unknown command | `"WAIT_USAGE_RESET"` (`"CONTINUE"` is no-op) | allowed (no-op) |
| `runtime_state.json` (the worker's own) | malformed | mode `"WAIT_USAGE_RESET"`; any other mode is a no-op | allowed (no-op) |

* `claude_usage.json` is **not** read. Observability `UNAVAILABLE` never creates a hold.

**`hold_while_needed(mailbox, audit_path, audit, sleep=time.sleep, poll_s=45.0) -> int`**

The loop:

1. Read the controls.
2. STOP → raise `StopRequested`.
3. CONTINUE → return the number of held polls.
4. HOLD → atomically write `audit_path` as JSON `{"kind": "AUDIT_ONLY_NOT_A_RESUME_CHECKPOINT", "pid": os.getpid(), "reasons": [...], "polls": n, "utc": ..., **audit()}`, then `sleep(poll_s)` and repeat.

Rules:

* `ValueError` if `poll_s > 45` or `poll_s <= 0`.
* Wall-clock time is never used to decide a resume.

### Run lock and outcomes

**`RunLocked(RuntimeError)`.**

**`RunLock(path, identity: dict)`** is a context manager.

* `__enter__` creates `path` **exclusively** (`O_CREAT | O_EXCL`) with `{"pid", "identity", "utc"}`. If the file exists → `RunLocked`.
* `__exit__` removes the file and never suppresses exceptions.

**Outcome records.**

| Function | Behaviour |
|---|---|
| `outcome_path(root, arm, master)` | `root/"outcomes"/f"{arm}_{master}.json"` |
| `read_outcome(root, arm, master)` | `dict` or `None` |
| `record_outcome(root, arm, master, outcome)` | atomic write; `OutputExists` (from `x5g1_safety`) if one already exists |
| `assert_can_start(root, arm, master, lock_path)` | `RunLocked` if the lock exists or an outcome exists (no retry) |

### Budget

**`BudgetPlanner(cap_s=21600.0, factor=1.5)`**

* `.check(cumulative_now, next_estimate, reserve, what)` raises `BudgetExceeded` iff `cumulative_now + factor·next_estimate + reserve > cap_s`.

**Estimates.**

```python
EST = {"update": 0.383, "dev_ce": 3.92, "score": 3.906, "save": 1.0, "bootstrap": 120.0, "exports": 60.0}
```

* `interval_estimate(updates, est=EST) = updates·update + dev_ce + save`
* `evaluation_reserve(unscored_checkpoints, unscored_final, est=EST, factor=1.5) = factor·(unscored_checkpoints·score + 60 + unscored_final·score + 60 + bootstrap + exports)`

### Resources

**`ResourceExceeded(RuntimeError)`.**

**`check_resources(peak_bytes, storage_bytes, ram_cap=8·2**30, storage_cap=2·2**30)`** raises if:

* `peak_bytes` is `None` (fail closed);
* `peak_bytes > ram_cap`;
* `storage_bytes > storage_cap`.

**`dir_size(path)`** is the total file bytes under `path` (0 if it is missing).

### `StudyControls(ctl, mailbox, planner, out_root, audit_path)`

**`.boundary(what, next_estimate, reserve, audit=lambda: {})`**, in order:

1. `ctl.guard(what)`: STOP file and per-run or cumulative cap.
2. `read_controls`: STOP → `StopRequested`; HOLD → `hold_while_needed`, after which the controls are re-read via step 2.
3. `planner.check(ctl.prior + ctl.cpu(), next_estimate, reserve, what)`.
4. `check_resources(peak_memory_bytes(), dir_size(out_root))`.

## 6. `topo_pilot.experiment.x5g1t_train`

| Function | Behaviour |
|---|---|
| `study_train_config(steps=5000, grid=GRID)` | `TrainConfig(steps=steps, checkpoint_steps=tuple(grid), device="cpu")`, other fields at their defaults (= the stored values) |
| `study_run_key(master)` | `("x5g1", "cylinder", master)`, the same for both arms |
| `checkpoint_callback(store, obs_train_id, obs_dev_id, model_cfg, train_cfg, seeds, run_key, before, after, record)` | the `on_checkpoint` callback (details below) |
| `train_one(store, obs_train_id, obs_dev_id, model_cfg, train_cfg, master, arm, root, controls)` | trains one model (details below) |

**The checkpoint callback.**

* `before(step)` is called **before** the write, so STOP or hold happens before any artifact.
* It saves a `Checkpoint` **exactly as `LearnerStage` does**:
  - `run_id = "-".join(map(str, run_key))`;
  - `state = serialise_state(model, info)`;
  - config `{"run_key": list(run_key), "step", "model_config", "train_config"}` (the dataclass dicts);
  - parents `[obs_train_id, obs_dev_id]`;
  - `seed_map = dict(seeds.issued)`;
  - consumer `"experiment"`.
* It appends `{"step", "checkpoint_id", "payload_sha256"}` to `record`, then calls `after(step)`.

**`train_one`.**

1. `assert_can_start`, then `RunLock(root/"RUN.lock", {...})`.
2. Load both ObservationSets with consumer `"learner"` and wrap them in `PublicTokenDataset`.
3. `Trainer(model_cfg, train_cfg, SeedTree(master), study_run_key(master)).fit(...)`, with the callback's before/after wired to `controls.boundary`.
4. **Always** record an outcome: `{"status": "COMPLETE" | "INCOMPLETE", "arm", "master", "checkpoints": record, "cause": None | "<Name>: msg"}`.
5. Re-raise any exception after recording.

## 7. `x5g1t_stages` / `x5g1t_main` (CLI)

**`StudyConfig`** is loaded from JSON.

| Field | Content |
|---|---|
| `protocol` | protocol name |
| `read_roots` | read-only roots |
| `study_root` | writable: `store/`, `runs/`, `outcomes/`, `tables/` |
| `ledger_path` | scientific ledger |
| `mailbox` | mailbox directory |
| `sources` | `{"T": {arm: [id, sha]}, "E": [id, sha]}` |
| `masters`, `sizes` | as in §2 |
| `model_config`, `steps`, `grid` | as in §6 |
| `gc` | `{arm: float}` |
| `threads` | intra-op thread count |
| `bootstrap_draws` | 2,000 for the study |
| `cap_s`, `cumulative_cap_s` | run and cumulative CPU caps |
| `check_stored_ids` | bool |

**Sub-commands:**

* `pools`
* `train --arm A --master M`
* `dev-analysis`
* `final-test --authorized-final` (refused without the flag, and refused before `dev-analysis` has written `tables/dev_analysis/verdict.json`)

**Every stage:**

* runs inside `RunControls` on `ledger_path`;
* verifies the sources with full hashes before and after (`checked_computation`);
* writes a new immutable `tables/<stage>[/<arm>_<master>]` directory through `guarded_export`, including `MANIFEST.json`.

**Fresh test.** The fresh-test pool is generated **only** by `final-test`.

## 8. Required independent fixtures

All fixtures use tiny models, N4/V3 processes and temporary stores.

* **Endpoint:**
  - every hand example: non-monotone, τ = 0, the 4,500 edge observed, first PASS at 4,750 censored, PASS only at 5,000, never;
  - D_low equality at 250;
  - all four censoring combinations, including both censored → (−inf, inf) with no NaN;
  - `quantile_inverted_cdf` versus numpy, and with ±inf;
  - the cohort truth table: supported, rejected, contradiction, a `None` pair, failures, wrong length;
  - the bootstrap uses one shared whole-row index draw per replicate (reproduce with the same rng), keeps censored draws, and calls the guard.
* **Lineage and oracle:**
  - frozen constants and IDs;
  - identical first symbols across arms;
  - test-stream rules;
  - disjointness;
  - the oracle ignores column 33 and equals the canonical-vocabulary computation under a non-identity perm.
* **Training composition:**
  - the same run_key gives identical step-0 weights and batch order across arms, with distinct checkpoint IDs through the parents;
  - public `serialise_state` gives bytes and IDs identical to `LearnerStage`;
  - STOP before the write → no artifact;
  - INCOMPLETE recorded and the exception re-raised;
  - a second start is refused (lock or outcome).
* **Runtime:**
  - the control precedence table, with fail-closed malformed files;
  - hold → live resume only on release (an injected `sleep`), and STOP while held;
  - `poll_s` bounds;
  - audit-only wording;
  - budget arithmetic, including the prior ledger of 17.016;
  - malformed-ledger preservation (existing `LedgerCorrupt`);
  - resource caps, with `None` failing closed;
  - manifest hashes.

## 9. Clarifications after implementation (additive, job 0009)

These were raised by the independent test writers. None of them changed a frozen rule.

### Endpoint

* **Guard label.** `{start}` in the guard string is the 0-based index of the batch's first draw. A partial last batch is allowed.
* **`quantile_inverted_cdf`.** It applies a 1e-9 tolerance. It can differ from numpy only when q·n lies within 1e-9 above an integer. The study values (n = 2000, q = 0.025 and 0.975) are exact.
* **`collisions` "internal" count.** It is total minus unique.

### Runtime

* **`StudyControls` keyword arguments.** It also takes `sleep=None` and `poll_s=45.0`, passed to `hold_while_needed`.
* **`hold_while_needed` sleep.** `sleep=None` resolves to `time.sleep` at call time.
* **Malformed controls.** A JSON file that is not an object, or that has a missing or null `command` or `mode`, is malformed and fails closed (STOP). Commands are case-sensitive.

### Training composition

* **`train_one` keyword arguments.** It also takes `reserve_s=0.0` (the study evaluation reserve) and `est=EST`.
* **Boundary calls.** `controls.boundary` is called once before the model starts, then before and after every checkpoint write.
* **An outcome is recorded once the lock is taken.** A STOP or budget stop at the start boundary therefore records an INCOMPLETE outcome. That model's single attempt is consumed, with no retry. A start refused by `RunLocked`, before the lock is taken, records nothing.
* **Directories.** `record_outcome` creates the parent directories.

### Stages

* **Pool parents.** Pool ObservationSets have parents [T_arm, E].
* **Dev-analysis requirements.** Dev-analysis treats a pair as failed (`None`) unless both models are COMPLETE and their recorded checkpoint steps equal the grid.
