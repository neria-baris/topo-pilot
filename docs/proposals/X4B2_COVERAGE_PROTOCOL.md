# X4 Phase B2 — frozen coverage-extension protocol (x4b2-v1)

14 October 2026. Branch `x4-phase-b2`, continuing from `x4-phase-b` at d7dcf5d. **Frozen before any B2 sampling.** No B2 trajectory, belief or distance existed when this was written. Seeds and sequence-ID codes below are deterministic hashes, not draws.

## 1. What B2 is, and what it is not

B2 is a new, separately approved check, motivated by Phase B ([report](X4_FEASIBILITY_REPORT.md), D-052). Phase B's verdict stays INCONCLUSIVE. Its protocol x4b-v1, report, outputs, D-051 and D-052 are unchanged, and this is not a retroactive repair of B.

B2 asks the same practical question with denser pools. Does joint Q2 separate beliefs that are near-equal under Q1, among beliefs reached by the original process at p32?

* **Not a new world or model.** The four pools are sampling repetitions from one process, not independent worlds or models.
* **No fitting.** No checkpoint is loaded, no activations are extracted, nothing intervenes and nothing is trained. The pools are not train or dev splits.
* **Scope of a NO-GO.** If B2 returns NO-GO, it is scoped to this process, horizon 2, p32 and this sampling screen. It is not a proof that Q1 is sufficient on all reachable beliefs.

## 2. Process identity (verified before sampling)

The process is the same as in x4b-v1 §2:

* WorldSpec 21feee1d8ee5422e;
* TransitionSpec e4dafc7b9785c172 (T, and π as the initial law);
* overlap EmissionSpecs 3633ac27dab50cf4 / 97838b9e13a26f74 / 8c29c329c197c79e at σ 1.25.

They are resolved through `resolve_inputs` exactly as in Phase B, and any mismatch stops the run. Sampling uses the canonical emission `E_canon = E[:, symbol_perm]`, which must be identical across the three EmissionSpecs (as verified in B). This is the convention DatasetStage uses (D-019). Tokens are kept in the canonical vocabulary.

## 3. Pools, streams and sequence-ID namespaces (frozen)

| Role | Size | Stream: `SeedTree(0).generator("x4b2-v1", "pool", "cylinder", "overlap", "1.25", role)` | Derived seed | Process code (namespace `x4b2-v1:role`) | Sequence-ID range |
|---|---|---|---|---|---|
| reference | 16,384 | role = `reference` | 4472965773301758267 | 2076810545 | 8919833372105113600 – …129983 |
| repetition1 | 16,384 | role = `repetition1` | 9041520877900685805 | 662554568 | 2845650202717585408 – …601791 |
| repetition2 | 16,384 | role = `repetition2` | 1190608976536703855 | 31366180 | 134716718642626560 – …642943 |
| repetition3 | 16,384 | role = `repetition3` | 264034718665583389 | 2024988825 | 8697260779482644480 – …660863 |

* **Sampler:** `dataset.HMMSampler(T, E_canon, π, SequenceLayout())`, which draws 33 symbols per trajectory (emit, then transition). It also returns latent states. They are used only for its range check and are discarded immediately; states are never persisted or passed on.
* **Sequence IDs:** `(process_code << 32) | (5 << 28) | index`, where `process_code` follows the documented dataset rule (the first 31 bits of `sha256(canonical_json([family, mode, sigma, replicate]))`, with `replicate = "x4b2-v1:<role>"`). Namespace code 5 is not used by DatasetStage, which uses 1/2/3.
* **History and identity:**
  - history = the first 32 symbols; the belief is taken after w32 (p32);
  - canonical trajectory ID: `"x4b2-<role>|<sequence_id>|<tokens_hash(w1..w32)>"`.
* **Order:** pools are processed one at a time, in the order reference, repetition1, repetition2, repetition3. Beliefs are computed in chunks of 4,096.

**Separation checks (failure stops the run, except where descriptive):**

* Sequence IDs are disjoint between B2 pools.
* Sequence IDs are disjoint from every ObservationSet in the main store (all splits, all worlds and conditions).
* The four process codes are distinct.
* First-token frequencies match πE: a χ² p-value below 1e-4 is a sampler-bias failure, as in DatasetStage.
* **Descriptive only:** identical 32-symbol windows between B2 pools, and between B2 and the old cylinder-O test/dev/train data, compared in the canonical vocabulary. Chance repeats are not an error; this is the dataset convention.

## 4. Ambient algebra: inherited, verified

The ambient verdict is not re-decided. B2 recomputes the canonical G1/G2 with `future_maps` (all x4b-v1 §3 checks) and runs `tangent_audit`. The recomputation must reproduce Phase B's `ambient.json`:

* the same verdict;
* H and BᵀG2 spectra, and ρ per τ, within 1e-12 absolute.

Only then is ALLOWS_STABLE carried over. A mismatch is a failure.

## 5. Reachable screen: unchanged x4b-v1 rules

Unchanged from x4b-v1:

* 512 anchors per pool: the smallest `sha256("x4b-v1|anchor|" + canonical ID)`.
* Five nearest Hellinger-Q1 neighbours with the same last symbol.
* Excluded: the anchor's own row and any identical 32-symbol window (self-pairs or identical histories).
* Admissible partner: H(Q1) ≤ 0.01. Eligible anchor: at least one admissible partner. Witness: an admissible partner with H(Q2) ≥ 0.05.
* Coverage: at least 128 eligible anchors per pool. Pool status: WITNESS if witnesses/eligible ≥ 0.05, else NO_MATERIAL_GAP; UNDERCOVERED below the coverage floor.
* Unrestricted neighbours: secondary and descriptive.

The x4b-v1 code is reused unchanged, with **reference in the role of test** and **repetition1–3 in the role of the dev pools**:

* **GAP:** reference is WITNESS, and at least 2 of the 3 repetitions are WITNESS.
* **NO_GAP:** reference is NO_MATERIAL_GAP, at least 2 repetitions are NO_MATERIAL_GAP, and no pool is WITNESS.
* **Otherwise INCONCLUSIVE:** under-coverage or inconsistency.

Everything recorded in x4b-v1 §6 is recorded again.

**Validity and agreement (failure gives INCONCLUSIVE):**

* Pool checks as in x4b-v1 §5.
* **Permutation:** the reference pool is recomputed in replicate 1729's vocabulary (`tokens = symbol_perm[canonical]`, filter with `E_1729`). The screen must give identical partners and flags.
* **Precision sensitivity:** the Q2 distances are recomputed from float32-cast Q2 for every pool. No pool status may change.

## 6. Decision and stop

The decision function is x4b-v1's `overall_verdict`:

| Ambient | Practical | Checks | Overall | Then |
|---|---|---|---|---|
| ALLOWS_STABLE | GAP | all pass | **GO** | Propose Phase C only. Do not run it. |
| any | NO_GAP | all pass | **NO-GO** | Recommend closing the practical Q2-gap hypothesis at p32 (scoped as in §1). |
| any other combination, or any failed check | | | **INCONCLUSIVE** | Stop. Do not propose a third extension automatically. |

No further pool enlargement, re-sampling or threshold change follows any result. **STOP for owner review.**

## 7. Code, budget and outputs

* **Code:**
  - reuses `HMMSampler`, `BayesFilter`, `FutureOperator` and the x4b analysis/audit code;
  - adds one small lineage adapter, `experiment/x4b2.py`, with known-answer tests;
  - the producer commit is recorded;
  - inherited and recorded: the zero-map guard in `tangent_audit` (inert here, x4b-v1 report note 1) and the corrected memory query (741333c).
* **Budget:** at most 1 CPU hour, measured as process time, checked after every pool. An 8 GB RAM target, measured as the Windows peak working set. Exceeding the cap means stop and INCONCLUSIVE.
* **Main store:** read-only. Its file-listing hash must be equal before and after the run.
* **Outputs:**
  - an independent store `topo-pilot/x4b2-research-store/` holding one MetricRecords plus npz exports of each pool's canonical tokens and sequence IDs (never states), with checksums;
  - tables in `docs/proposals/X4B2_OUTPUTS/`;
  - the report `docs/proposals/X4B2_COVERAGE_REPORT.md`.
* **Prohibited:**
  - no fitting, checkpoint loading or extraction;
  - no intervention or training;
  - no Phase C, X5 or X6;
  - no edit to Phase B outputs, D-051/D-052, reports, preregistrations or historical artifacts;
  - no merge, push or tag change.
