# Stages: build waves, run stages, gates, exit points

Build waves are aligned with run stages. After each wave, the matching stage can run, so stopping after any wave leaves a working, reportable state.

## 1. Build waves

`∥` means the modules in the wave are built in parallel by separate builders. **TW** means an independent test writer: a different agent from the implementer, who writes the tests from the TEST_PLAN.

| Wave | Enables | Modules (∥) | Tier: implementer / tests | Depends on (public API) |
|---|---|---|---|---|
| **W0** | S0 | `contracts`, then the package skeleton, `tools/`, and `experiment` (CLI skeleton only: `status`, `stage` dispatch) | A or B under review / **TW** for contracts | — |
| **W1** | S1 | `world` ∥ `topology` ∥ `process` ∥ `executors` | B / **TW** for world and topology; B for process; B for executors | contracts. `process` uses the world fixtures in `contracts.testing` until `world` is accepted |
| **W2** | S2 | `dataset` ∥ `oracle` ∥ `prediction` (baselines and metrics part) ∥ `analysis` (reference spaces, discriminability table, σ calibration) | B / **TW** for oracle and analysis | contracts, world, process, topology |
| **W3** | S3 | `learner` ∥ `activations` | B / B | contracts, dataset (loader API) |
| **W4** | S4–S6 | `analysis` (F1 rule, Δgeom, R0–R3, Gaussian floor, layer sweep, dynamics, checkpoint-order null) ∥ `experiment` (runner, gates, run plan, report, preregistration writer) ∥ `prediction` (learning gate) | A reviews `analysis` closely / **TW** for the F1 rule | everything above |
| **W5** | S7 | `prediction` (ridge probes) ∥ `topology` (circular coordinates) ∥ `analysis` (sensitivity) | B / B | W4 |
| **WX** | X1–X3 | world-family plugins, center strategies, homology over GF(p) beyond 2, H₂ and H₃ pipelines | B / **TW** | E2 reached |

A wave completes when every module in it is `accepted` and `tests/integration/test_<stage>.py` passes.

## 2. Run stages

Command form:

```bash
topo-pilot stage <id> --config configs/stages.yaml [--executor local|bundle|ssh]
```

| Stage | Reads | Writes | Gate (automatic) | Est. active hours |
|---|---|---|---|---|
| **S0** | — | store initialised; env lock; contracts tests green | contracts suite passes; `tools/check_imports.py` is clean | 3–4 |
| **S1** | configs | 2 WorldSpec, 2 TransitionSpec, EmissionSpec for O/P/N at the 3 σ candidates; PH calibration report | **G-A:** see below | 5–6 |
| **S2** | S1 | datasets, OracleOutputs, n-gram baselines, σ choice, discriminability table, `PREREGISTRATION.md` draft | **G-B, G-C, G-D:** see below | 7–8 + **H1** |
| **S3** | S2 | smoke run (cylinder, O, seed 1729); throughput and memory report | **G-E:** captured ≥ 0.8 on the smoke run, and the projected S4/S5 compute fits §5 | 5–6 + **H2** |
| **S4** | S3 | 6 O runs + 1 N run; activations at all checkpoints for panel 1, and at checkpoints 0 and 5000 for all panels; F1, H2, R0–R3, Gaussian floor; README at level E2 | **G-F:** every model passes the learning gate (or is marked), and the H0 checks pass | 6–8 |
| **S5** | S4 | 6 P runs; same analysis | **G-F** for P | 2–3 |
| **S6** | S4/S5 | S and regret over 12 checkpoints; checkpoint-order null; layer sweep | — | 3–4 |
| **S7** | S6 | 2 U runs + 2 extra N runs; probes; sensitivity; circular coordinates | **G-G:** all runs documented, failures included | 6–8 |
| **S8** | all | final README, `make reproduce-figures`, clean rerun of one run from scratch | rerun artifact IDs match | 3–4 |

**Gate details:**

- **G-A:** all three of the following hold:
  - β is correct for both worlds;
  - Vietoris–Rips on $d_M$ gives a long H₁ bar for the cylinder only;
  - synthetic circle and disk clouds embedded in $\mathbb{R}^{128}$ with noise, at $M=512$, are classified correctly in ≥ 19/20 draws.
- **G-B:** the oracle matches brute-force enumeration, and the U and N controls behave as specified.
- **G-C:** σ selected by the rule.
- **G-D:** no latent field in the public data, and the leakage tests pass.

**Run priority inside a stage** is seed-major and paired by world, so that a partial stop still leaves matched pairs:

```text
S4: cyl-O-1729 (from S3) → sq-O-1729 → N-1729 → cyl-O-2718 → sq-O-2718 → cyl-O-3141 → sq-O-3141
S5: cyl-P-1729 → sq-P-1729 → … same pairing
S7: U-cyl → U-sq → N-2718 → N-3141
```

## 3. Exit points (definition of done)

| Exit | After | Deliverable | Allowed claim |
|---|---|---|---|
| **E0** | S1 | complex figures, PH of the world, graph-vs-surface table, calibration report | "The PH pipeline recovers the known topology; graph cycles ≠ surface holes" |
| **E1** | S2 | σ table, discriminability table of the unlearned spaces, committed preregistration | "These topological differences exist in principle, with no model involved" |
| **E2** | S4 | prediction-vs-oracle table; $D_{r,i}$ with the four $S$ values and $u_r$; $\Delta_\text{geom}$ (including same-last-symbol pairs); R0–R3; Gaussian floor; H0 checks; README | an F1 verdict (supported, rejected, or inconclusive with reason) and the H2 result |
| **E3** | S5 + S6 | F1 rule under P; S and regret curves; checkpoint-order null; layer sweep | H3, H4 |
| **E4** | S7 + S8 | controls, probes, sensitivity, circular coordinates, clean rerun | strengthened interpretation |

At **every** exit:

- the README is in English and states exactly one finding sentence at that level;
- unrun stages are listed as "not run";
- `make reproduce-figures` regenerates every figure from MetricRecords;
- the git tag `E<k>` is set.

## 4. Pre-registered cut paths

Cuts are decided on time or resources, never on results, and every cut is logged.

| Trigger | Action |
|---|---|
| S3 projects S4 compute over budget | 3000 steps instead of 5000, uniformly for all runs; or switch to the bundle executor (H2) |
| Time runs out after S4 | stop at E2; H3 and H4 are reported as "not run" |
| G-E fails | fallback ladder: 10k steps → 6 blocks with d=256 → the next σ in the calibration order (requires a new preregistration). If the whole ladder fails, stop at E1 |
| S2 shows no world difference in any unlearned space | stop at E1 with the finding "no expected signature"; no training |

## 5. Budgets (assumptions, measured in S3)

| Resource | Budget |
|---|---|
| Training | 17 runs × ~21M target tokens (E4). **No GPU assumed.** Estimated 15–45 min per run on a multi-core CPU: E2 ≈ 2–5 h, E4 ≈ 4–13 h. A GPU takes minutes per run. Device choice follows the rule in `EXECUTION.md` §5: local CPU if the projection is ≤ 8 h per stage, otherwise bundles to a free or rented GPU. **Cap:** 12 GPU-hours or 24 CPU-hours |
| PH | about 700 Ripser calls of 512 points in H₀ and H₁; **cap 4 CPU-hours, 8 GB RAM**; no H₂ in the core pilot |
| Storage | activations ≈ 0.4 GB; checkpoints ≈ 2 GB (12 per run, with optimizer state for the last only); total **< 4 GB** |
| Active work | 41–52 hours to E4; 27–33 hours to E2 |

## 6. Extension stages (after E2)

| Stage | Content | Spec |
|---|---|---|
| X1 | orientability: Möbius vs cylinder; Klein and RP² vs torus and S², via PH over $\mathbb{F}_2$ vs $\mathbb{F}_3$ | `EXTENSIONS.md` §2 |
| X2 | T²⊔T² (belief over *which* world) and T²#T² (genus 2) | `EXTENSIONS.md` §3 |
| X3 | S², T³, S³ (H₂ and H₃) | `EXTENSIONS.md` §4 |
