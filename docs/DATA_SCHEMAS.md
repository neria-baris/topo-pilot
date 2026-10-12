# Data schemas

Every artifact class is defined in `topo_pilot.contracts.schemas` as a frozen dataclass with a `validate()` method. This file is the human-readable mirror. When they disagree, the code in `contracts` wins and this file must be updated in the same commit.

**Notation:**

| Symbol | Meaning |
|---|---|
| N | number of states |
| V | number of symbols |
| R | number of trajectories |
| L = 33 | observed symbols per trajectory |
| C = 32 | context length (model positions are 0..32) |
| M | histories in a panel (512) |
| K | number of hooks |
| d = 128 | model width |

Ids are dense 0-based integers. Symbol ids and state ids carry **no** geometric meaning.

## 1. Envelope (every artifact)

`meta.json`:

| Field | Type | Meaning |
|---|---|---|
| `artifact_type` | str | class name, e.g. `WorldSpec` |
| `artifact_id` | str[16] | `sha256(canonical_json(type, config, sorted(parent_ids), schema_version))[:16]` |
| `schema_version` | semver str | if the major version is unknown, loading fails with `SCHEMA_VERSION_MISMATCH` |
| `parent_ids` | list[str] | the artifacts it was derived from |
| `config` | dict | the full generating config after defaults |
| `seed_map` | dict[str,int] | every derived seed used |
| `producer_version` | str | git SHA plus a dirty flag |
| `created_utc` | str | **not** part of the identity |
| `shapes`, `dtypes` | dict | for each payload array |
| `payload_sha256` | str | checksum of the payload file(s) |
| `status` | `complete` \| `incomplete` | `incomplete` artifacts are never valid inputs |

On disk: `artifacts/<artifact_type>/<artifact_id>/{meta.json, payload.npz | state.pt}`.

## 2. World and process

**WorldSpec**
- `family: str`: a registry key (`square`, `cylinder`, …).
- `dims: tuple[int,...]`: for example `(12, 12)`.
- `coords: [N, D] float64`: chart coordinates. Used **only** by the generator and the analysis.
- `cells: dict[k, int32[n_k, 2**k]]`: the k-cubes as ordered vertex tuples, for k ≤ `max_dim`.
- `edges: int32[E, 2]`: the 1-skeleton, canonical with the lower id first.
- `dist: [N, N] float64`: the primary metric $d_M$.
- `dist_graph: [N, N] float64`: graph geodesic distance.
- `betti_expected: dict[p, tuple]` and `betti_computed: dict[p, tuple]`: over GF(p), with p ∈ {2, 3}.
- `identifications: list[str]`: a human-readable description of the gluing.
- **Invariants:**
  - ∂∂ = 0;
  - computed β equals expected β;
  - `dist` is a metric;
  - the graph is connected, except for declared disjoint-union families.

**TransitionSpec**
- `T: [N, N] float64`, where `T[i, j] = P(z_{t+1} = j | z_t = i)`.
- `pi: [N]`.
- `p_stay`, `d_max`.
- `event_order = "emit_then_transition"`.
- **Invariants:** rows sum to 1 ± 1e-12; π T = π; support only on edges and self-loops; T is symmetric.

**EmissionSpec**
- `E: [N, V] float64`, where `E[z, w] = P(w_t = w | z_t = z)`.
- `mode` ∈ {`overlap`, `axis_permuted`, `full_permuted`, `identical`, `unique`}.
- `sigma`; `centers: [V, D] float64 | null`; `center_strategy`.
- `state_perm: int32[N] | null`; `symbol_perm: int32[V]`.
- `diagnostics`: `H_W_given_Z`, `H_W`, `p_w[V]`, `coverage_radius`, `row_entropy_quantiles`, `factorizes: bool`.
- **Invariants:**
  - rows sum to 1;
  - every `p_w ≥ 1e-4`;
  - a permuted mode has the same row multiset as its source;
  - `identical` has equal rows;
  - `unique` is a permutation matrix.

## 3. Data

**ObservationSet** (public)
- `split` ∈ {train, dev, test}.
- `sequence_id: int64[R]`, globally unique.
- `tokens: uint8[R, 33]` (`uint16` if V > 255).
- `V`, `layout_version`.

**EvalSidecar** (privileged; dev and test only)
- `sequence_id: int64[R]`.
- `z: int16[R, 33]`, where `z[:, t]` is the state that emitted `tokens[:, t]`.

**HistoryIndex**
- `history_id: str[M]`, defined as `sha1(dataset_id, sequence_id, end, tokens_hash)[:16]`.
- `sequence_id`, `end = 32`, `panel ∈ 1..8`, `tokens_hash`.
- **Invariants:** panels are disjoint, and each panel holds 512 histories from 512 distinct trajectories.

### Alignment (single source: `contracts.SequenceLayout`)

| Model position p | Input token | History | Target | Oracle quantity | Latent label |
|---|---|---|---|---|---|
| 0 | BOS (= V) | ∅ | w₁ | q₀ = πE | z₁ |
| p ≥ 1 | w_p | w₁..w_p | w_{p+1} | b_p, q_p = b_p T E | z_p (current), z_{p+1} (emits target) |
| 32 (analysis) | w₃₂ | w₁..w₃₂ | w₃₃ | b₃₂, b^(1) = r_{w₃₂} | z₃₂ |

## 4. Oracle and baselines

**OracleOutputs**
- `history_id[M]`.
- `b32: [M, N] f64`, `b1: [M, N] f64`.
- `q: [M, V] f64`, `q_last: [M, V] f64`.
- `F2: [M, V, V] f32`: panels only. Flattening index is `i*V + j`, ordered as (next1, next2).
- `belief_entropy: [M]`, `log_evidence: [M]`.
- `ce_oracle_all_positions: [R_test, 33] f32`.

**ProcessDiagnostics**
- `G_C`, `mean_H_b1`.
- `O_singular_values: list[[r_k]]` for k ≤ 3.
- `sigma_table`: one row per candidate.

**BaselineOutputs**
- `ngram_order`, `smoothing`.
- `probs: [M, V] f64`, aligned to `history_id`.

## 5. Model and activations

**Checkpoint**
- `run_id`, `step`, `model_config`, `train_config`, `observation_id`.
- `state.pt`: model weights. Optimizer and RNG state are included **only** for the last step.
- `layout_version`.

**ActivationSet**
- `checkpoint_id`, `history_id[M]`.
- `hooks: list[str]` (K entries).
- `A: [M, K, d] float32`, `logits: [M, V] float32`.
- `source` ∈ {`model`, `baseline:R0..R3`}.
- **Invariant:** row order equals `HistoryIndex` order, and every row is tied to an exact token history.

## 6. Topology and results

**DistanceArtifact**
- `point_ids[M']`: after deduplication.
- `D: [M', M'] f64`.
- `metric_id`, `scale_s`, `dedup_map`, `pca_ref | null`.

**Diagrams**
- `rows: [n, 4] f64`, with columns (dim, birth, death, censored).
- `coeff_p`, `maxdim`, `threshold`, `library_version`.

**MetricRecords** (long table; one row per value)
- Columns: `run_id, replicate, world, condition, checkpoint, hook, panel, space, metric_id, value|null, units, status, uncertainty_kind, parent_ids`.
- `null` means undefined or missing, never 0.
- `status` ∈ {`ok`, `collapsed`, `censored`, `nonseparable`, `inconclusive`, `not_run`}.

**GateReport**
- `stage`, `gate_id`.
- `checks: list[{name, passed, value, threshold}]`.
- `verdict` ∈ {`pass`, `fail`, `waived`}; `waiver_reason`.

**RunManifest**
- The DAG of artifact ids.
- Config and seed bundle.
- `stage_status`.
- Hardware, wall time, peak memory.
- The executor used.
- All failures.

## 7. Access policy (enforced by `ArtifactStore.load`)

| Artifact | Allowed consumers |
|---|---|
| EvalSidecar | `analysis`, `prediction` (secondary analyses only), `experiment` (bundling) |
| WorldSpec, TransitionSpec, EmissionSpec | `process`, `dataset`, `oracle`, `analysis`, `experiment` |
| ObservationSet | all except `world` |
| Checkpoint | `learner`, `activations`, `experiment` |
| everything else | all |

`learner` and `activations` requesting any privileged artifact raises `LEAKAGE`.

## 8. Contracts 1.0.0: concrete field additions (code in `topo_pilot.contracts` wins)

These were fixed when `contracts` was frozen (D-008 to D-011). They are additive refinements of the tables above.

- **Storage:** non-array fields are stored in `extra.json` next to `payload.npz`. `payload_sha256` is a canonical *content* checksum (array names, dtypes, shapes, bytes, plus `canonical_json(extra)`), not a hash of the zip file. `meta.json` also records `consumer`, the module that wrote the artifact.
- **WorldSpec:** `metric` (the name of `dist`) and `disjoint` (exempts declared disjoint unions from connectivity). `cells` is stored as arrays `cells__<k>`.
- **EmissionSpec:** `diagnostics["p_w"]` is a length-V list. `validate()` also rejects an all-zero column (`dead_symbol`).
- **ObservationSet:** tokens hold `w_1..w_33` without BOS. **EvalSidecar** adds `split` and `N`.
- **HistoryIndex:** adds `dataset_id`, `panel_size`, and `n_panels`. `end`, `panel`, and `tokens_hash` are per-row arrays. `tokens_hash = sha1(int64 LE bytes of w_1..w_end)[:16]`, and `history_id = sha1("dataset_id|sequence_id|end|tokens_hash")[:16]` (`contracts.tokens_hash`, `contracts.make_history_id`).
- **ProcessDiagnostics:** adds `sigma` and `world_family`. **BaselineOutputs** adds `extra_info`.
- **Checkpoint:** adds `has_optimizer_state`; `state` holds the `state.pt` bytes.
- **ActivationSet:** `logits` and `checkpoint_id` may be `None` for representation baselines R2 and R3.
- **DistanceArtifact** and **Diagrams** carry a `status` (a `Status` value).
- **MetricRecords:** `rows` is a tuple of `MetricRow`. Every column of §6 is present; `value` is `None` when undefined.
- **GateReport:** `checks` is a tuple of `GateCheck(name, passed, value, threshold)`.
- **RunManifest:** fields `run_key, executor, config_hash, config, dag, seed_bundle, stage_status, hardware, wall_time_s, peak_mem_mb, failures, waivers`.
- **SequenceLayout:** `model_inputs(tokens, V)` takes `V` explicitly.
