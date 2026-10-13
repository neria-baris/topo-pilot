# X5 G1 — implementation plan v2 (for x5g1-feas-v2)

14 October 2026. Handoff job 0005. **Plan only.** Nothing is implemented, sampled or trained.

This plan supersedes [plan 1](X5_G1_IMPLEMENTATION_PLAN.md) for the gate implementation (§1–§5). Plan 1 is kept byte-identical. Its training outline, plan 1 §6, is carried forward by reference, still **NOT FROZEN** (§6 below).

## 1. Finalised adapters (accepted in the job 0004 review; no schema change)

| Where | Addition |
|---|---|
| process `conductance.py` (exported) | `ConductanceConfig(a=0.20, move=0.8)`; `warp_profile(dims, a) -> (f, l_h)`; `conductance_kernel(world, cfg) -> (TransitionSpec, metadata)` |
| process `ProcessStage` | `run_conductance_transition(world_id, cfg, store) -> id`. Config holds kind "metric_conductance", a, move, f_y, l_h, C_max and the edge counts; the parent is the WorldSpec. |
| analysis `x5_kernel.py` | `movement_rate`, `spectrum_report` (λ, gap, γ*, t_rel, ⌈mixing bound⌉, near-unit status), `integrated_autocorrelation` (constant and reducible statuses), `rate_matched_kernel` (status), `is_connected` |
| analysis `x5_context.py` | `context_status(gc_low, gc_high, valid) -> PASS / FAIL / NEAR_THRESHOLD / INVALID_PREDICTIVE`; `overall_verdict(arms, global_failures)` with precedence FAILED > INCONCLUSIVE > WEAK_CONTEXT > FEASIBLE; `percentile_interval(values)` (linear, 2.5/97.5) |
| experiment `x5g1_lineage.py` | `paired_generators()` returns **two separately initialised** generators from SeedTree(0) stream ("x5g1-v1", "calibration", "cylinder", "overlap", "1.25"). `sample_named(T, E, perm, pi, rng, n=16384)` returns (named = perm[canon], seq), with states discarded and one call. Also `sequence_ids(arm)` (code 8), and `calibration_obs(named, seq, arm)` → ObservationSet(split "dev") plus config {role: "calibration", …}. |
| experiment `x5g1_run.py` | integrity; kernels; diagnostics; pools; oracle quantities in 4,096-row batches; bootstrap in 4 × 500 batches; verdict; exports. STOP and budget polled before and after each operation; ledger in `try/finally`, including failure and export cost. |
| contracts, world, dataset, oracle, learner | no change |

**Resolver rule.** X5 code finds its calibration ObservationSets by (role, protocol, arm) in config. It never uses `child_of(…, split="dev")`, which would also see the original S2 dev split through a read-through store. The independent X5 store is never mounted for legacy resolvers.

## 2. Pure-function definitions targeted by the tests

These carry over from plan 1 §2, with the following additions and changes.

* `spectrum_report`:
  - mixing bound = `ceil(t_rel * log(1/(eps * pi_min)))`, with ε = 1/4;
  - `NEAR_UNIT_GAP` when γ* ≤ 1e-12 and the graph is connected.
* `integrated_autocorrelation(T, pi, g)`:
  - `UNDEFINED_CONSTANT` if Var_π(g) ≤ 1e-12;
  - `REDUCIBLE` if λ_k ≥ 1 − 1e-12 for some k ≥ 2.
  - The docstring states that g is a **state function** (g_w = E[:, w] is the conditional emission probability). This is not an autocorrelation of observed tokens.
* `context_status`:
  - INVALID_PREDICTIVE if the input is flagged invalid or not finite;
  - PASS iff low ≥ 0.03;
  - FAIL iff high < 0.03;
  - else NEAR_THRESHOLD.
  - There is no G_C floor: a valid G_C of 0 is FAIL.
* `overall_verdict`: precedence exactly as protocol §8. The α diagnostic is never an input.

## 3. Independent tests

A separate test-writer agent writes these from protocol v2 and §1–§2 before reading the implementation. Fixtures are synthetic.

| Module | Required cases (new in v2 marked ★) |
|---|---|
| process | a = 0 equals `TransitionBuilder` within 1e-15 on the 12×12 cylinder; a = 0.2 validity; closed-form C_max; edge classification including wraps; \|a\| ≥ 1 error; metadata equals `warp_profile` |
| analysis `x5_kernel` | 2-state τ_int hand value; constant and reducible statuses; ★ near-unit-gap status; ★ ceil in the mixing bound (a hand case where t_rel·log is non-integer); gap and t_rel hand values; rate-matched validity boundary |
| analysis `x5_context` | ★ G_C exactly 0 (valid) → FAIL; ★ lower = 0.03 exactly → PASS; ★ upper = 0.03 exactly → NEAR_THRESHOLD; ★ non-finite or invalid → INVALID_PREDICTIVE; ★ precedence: FAILED beats everything, an INVALID_KERNEL arm plus a weak arm gives INCONCLUSIVE (not WEAK_CONTEXT), a NEAR_THRESHOLD arm plus a FAIL arm gives INCONCLUSIVE, the α status never changes the verdict |
| experiment lineage | ★ non-identity permutation: an oracle on named tokens with the stored E equals an oracle on canonical tokens with E[:, perm] (beliefs identical; predictive laws equal after perm reindexing) and the named → canonical round trip is exact; ★ paired generators: two arms with different T share z1 and the first canonical symbol for every trajectory, and reusing one advanced generator for the second arm would fail the test; ★ w33 isolation: changing the 33rd token leaves every gate quantity unchanged; states never returned; frozen seeds and namespace code 8; the ObservationSet has split "dev" and config role "calibration" |
| experiment run (builder smoke + independent) | ★ ledger written when an exception, STOP or budget stop occurs mid-run, including the export step; ★ an integrity mismatch (tampered parent checksum or a changed listing) gives FAILED and no scientific verdict; STOP raised inside the bootstrap batch loop |

## 4. Execution sequence (a later job, after ACCEPT)

1. Freeze (DECISIONS: protocol sha256) and commit the code and tests (clean producer commit).
2. Integrity check: parents, checksums, state and edge order, the listing hash. Failure → FAILED; stop.
3. Kernels, a0 equivalence, validity checks and exact diagnostics.
4. Pools: two separately initialised generators, one sampling call per arm, named tokens, ObservationSets persisted to the independent store, disjointness checks.
5. Oracle quantities on named tokens with the stored E (4,096-row batches), the G_C bootstrap (4 × 500) and the descriptive paired difference.
6. Verdict by precedence; exports; ledger (`finally`); STOP for review.

## 5. Cost (unchanged)

* Compute: ≤ 0.1 CPU h expected (gate cap 1 CPU h; X5 6 CPU h).
* Storage: ≤ 50 MB (two ObservationSets and the exports).
* Engineering: about 1.5 days, including the independent tests.

## 6. Training outline — carried forward unchanged, NOT FROZEN

Plan 1 §6 stays the outline. It was not refined using any data. Two open items are added for later resolution:

* **Grid count.** "Every 100 steps to 1,000, then every 250 to 5,000" gives 26 points from step 100 onward (27 including step 0). Plan 1's "29 points" figure must be recounted, and the exact grid (including step 0 and any final confirmation evaluations) fixed in the training protocol.
* **The ≥ 250 equality.** Whether a difference of exactly 250 steps satisfies "≥ 250" is ambiguous. Plan 1 §6.3 item 3 says ties do not count, which conflicts with "≥". This must be resolved, together with the interval rule, in the training protocol.

Training cannot start on the gate contract. It needs a separately reviewed training protocol and a distinct task.
