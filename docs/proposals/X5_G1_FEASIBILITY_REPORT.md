# X5 G1 — exact-process and calibration feasibility report

**Run.** 14 October 2026, handoff job 0006.

**Protocol.** [x5g1-feas-v2](X5_G1_FEASIBILITY_PROTOCOL_V2.md), frozen by D-065 (sha256 E5B0DCEB…9E45 unchanged).

**Code and outputs.**

| Item | Value |
|---|---|
| Branch | `x5-g1-gates` |
| Producer commit | 6448262 (clean tree) |
| Tables | [X5_G1_FEASIBILITY_OUTPUTS/](X5_G1_FEASIBILITY_OUTPUTS/) |
| Independent store | `topo-pilot/x5g1-research-store/` |
| MetricRecords | `e978af31f4625fbb` |

**What did not run.** No training, checkpoint, activation, PH or fresh test.

## Verdict: **FEASIBLE** — both kernels are valid and G_C PASSES in both arms

FEASIBLE authorises **only** proposing a six-model training protocol in a new, separately reviewed task. It is not a training authorisation, and it is not a curvature result.

| | a0 (flat, `e4dafc7b9785c172`) | a020 (conductance, `08a22a03727d2295`) |
|---|---|---|
| Kernel validity (§3.1) | ok: row sum error 2.2e-16, symmetric (0), min diagonal 0.2, support ok, stationarity 8.7e-19, connected, min p_w 0.0268 | ok: same checks pass; min diagonal 0.2, stationarity 1.7e-18 |
| **G_C** (nats; repository definition KL(q_C ‖ q_last) at p32) | **0.2713**, 95% CI [0.2674, 0.2750] → **PASS** | **0.2939**, 95% CI [0.2900, 0.2980] → **PASS** |
| G_C against the stationary marginal (descriptive) | 1.376 | 1.425 |
| Two-symbol comparator regret KL(q_C ‖ q_2) | 0.0860 | 0.1032 |
| H(W\|Z) / H(W) (identical by construction) | 1.754 / 3.583 | 1.754 / 3.583 |
| Bayes entropy H(q_t) at t = 0 / 1 / 8 / 32 | 3.583 / 2.478 / 2.209 / 2.207 | 3.583 / 2.459 / 2.159 / 2.158 |
| O2 numerical rank (relative 1e-10) | 138 | 143 |

* **Paired G_C difference** (a020 − a0, descriptive, stream "gc_bootstrap_paired"): 95% CI [0.0183, 0.0266] nats.
* **Sanity check.** The a0 calibration G_C (0.271) agrees with the stored E3 ProcessDiagnostics G_C of the same process (0.265, test panels).

## Kernels and exact process diagnostics (descriptive)

* **a020 metadata:**
  - l_h(y) runs from 1.200 at y = 0 and 11 down to 0.808 at y = 5 and 6;
  - C_max = 5.0627;
  - 144 horizontal edges (including 12 wraps) and 132 vertical.
* **a0 equivalence:** the conductance builder at a = 0 equals the stored flat T exactly (maximum difference 0).

| | a0 | a020 | rate-matched flat (α = 0.8035, valid; **diagnostic only**) |
|---|---|---|---|
| Movement rate r | 0.7667 | 0.6160 | 0.6160 (matched) |
| Spectral gap 1 − λ₂ (= γ*) | 0.01363 | 0.01077 | 0.01095 |
| t_rel = 1/γ* | 73.4 | 92.9 | 91.3 |
| Mixing upper bound ⌈t_rel · log(1/(¼·1/144))⌉ | 467 steps | 591 steps | 581 steps |
| λ_min | −0.586 | −0.521 | — |
| τ_int cos x / sin x | 36.3 / 36.3 | 46.8 / 46.8 | 45.4 / 45.4 |
| τ_int centred y | 144.0 | 182.5 | 179.5 |
| τ_int of g_w = E[:, w], mean [min, max] | 35.2 [23.6, 43.0] | 45.6 [26.9, 59.0] | 44.1 [29.7, 53.7] |

* **Mixing bound.** It is an upper bound for irreducible, π-reversible, lazy chains, not an estimate.
* **τ_int.** These are conditional-state diagnostics, not autocorrelations of the observed token sequence.

**Confound, stated plainly.** The C_max normalisation lowers the curved arm's movement rate by about 20%. A flat kernel slowed by the same factor (α = 0.80) reproduces most of a020's mixing summaries: gap 0.0110 vs 0.0108, t_rel 91 vs 93, and τ_int within about 3–5%. Its emission-function τ_int range differs more (min 29.7 vs 26.9, max 53.7 vs 59.0).

* So any later learning-time difference between a0 and a020 would be **heavily confounded with movement speed**.
* Matching these summaries would still leave anisotropy, entropy and context gain, and the full correlation structure, as alternatives. In particular, a020's G_C and two-symbol regret are higher than a0's.
* **No curvature attribution** is licensed by this gate, and none would follow from a G1 training result without a speed-matched comparison.

## Lineage, pairing and checks

* **Pools.** One per arm, 16,384 trajectories each, drawn by **two separately initialised** generators from `SeedTree(0).generator("x5g1-v1", "calibration", "cylinder", "overlap", "1.25")` with one sampler call per arm.
  - The first symbol is identical in every paired trajectory (verified).
  - Canonical draws were remapped as **named = perm[canon]** to the stored E vocabulary, and every oracle call used the named tokens with the stored E.
  - Latent states were discarded; no EvalSidecar was written.
* **Persistence.** Calibration ObservationSets with `split="dev"` and config role "calibration": a0 `eb3170a226f03bd0` and a020 `e574367fd00ccf02`, with parents being the arm's T and E `3633ac27dab50cf4`. ID namespace code 8.
* **Disjointness.** Sequence IDs are disjoint from all stored ObservationSets and from the B2 namespaces (0 clashes), and between arms (0).
  - 127 identical 32-symbol windows occur **between the two arms**, which is expected under common randomness; this is descriptive.
* **Integrity.**
  - Parent payload checksums matched the frozen prefixes: world b6f0746e…, T f94340a6…, E f5b6197c….
  - The main-store listing (2,568 files) was identical before and after.
  - Old dirty-tree producer versions of the parents (`84152ab27e91+dirty`) are recorded as found and not repaired.
* **Tests.**
  - 89 independent tests (written by a separate test-writer agent from the frozen contract and API before reading the implementation), plus 2 builder smoke tests.
  - On first contact, 98 of 99 new X5 tests passed. The one failure was a real defect: `verify_parents` let a non-StageFailure exception escape, against the spec's "never raises". It was fixed before data.
  - process + analysis + experiment: 492 passed; ruff, import and file-size checks clean.

## Cost

* **Scientific CPU:** 8.9 CPU s, including export, single-threaded BLAS. Peak working set 0.70 GB.
* **X5 cumulative ledger:** 8.9 s of 21,600; the gate cap was 3,600. The ledger lives in the store.
* **Technical fixture tests:** about 30 CPU s, reported separately.
* **Storage added:** 1.5 MB.

## Deviations

1. **Identical windows against old data not computed.** Protocol §4 lists "identical windows with old data" as a reported (descriptive) item. Only the between-arm count was computed. ID disjointness against the old data, which is the gate check, was done.
2. **Verdict function renamed.** It is exported as `x5_overall_verdict` because `overall_verdict` already names the X4 Phase B function. Same semantics; the API doc was corrected before tests were written against it.
3. **Ledger outcome field.** Ledger entries also record an `outcome` field (the verdict), beyond the API's minimum fields.

## What this licenses

**Licensed.** Both specified processes are lawful, and both carry ample history-dependent next-symbol information at p32 (G_C ≈ 0.27–0.29 nats). A later learning-time comparison is therefore not blocked by weak context.

**Not licensed.**

* Any claim about learning speed.
* Curvature specificity: the movement-speed confound is large, as shown above.
* Topology.

**Next step.** A separately reviewed training protocol has to resolve the open outline items (evaluation grid count, the ≥ 250 tie rule, censoring, the pairing key, dataset lineage collisions) before any of the six models is trained.
