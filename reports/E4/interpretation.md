# E4: interpretation, limitations and exploratory notes (NOT pre-registered)

Written by the conductor on 2026-10-13, after `summary.md` was generated and read for the first time. Nothing here changes a verdict, threshold, rule or metric. Each item reads numbers that are already in `summary.md` or in the stored S7/S8 records. Anything that would need a new analysis is named as a follow-up; a follow-up needs its own preregistration before it counts as evidence.

## 1. What is decided, and by what

| layer | items | status after E4 |
|---|---|---|
| Primary (PREREGISTRATION.md) | F1 under O, H2, H3 (F1 rule under P), H4 | **unchanged** since E2/E3: F1 SUPPORTED, H2 sign-consistent (48/48), H3 REJECTED and uninformative by design, H4 REJECTED |
| Approved decision rule (D-037) | H3′ under P | **unchanged**: SUPPORTED |
| Secondary (PREREGISTRATION_X4.md) | X4-a…d under O and P | unchanged |
| S7, fixed blind (D-047) | U/N controls, probes, circular coordinates | descriptive |
| S7, fixed blind (D-047) | sensitivity | robustness checks of the primary verdicts; they cannot replace a verdict |
| S8 (D-047, D-048, D-049) | clean rerun, integrity, report reproduction, tests | G-H **fail** on `rerun_ok` only (§6) |
| This file | readings and post hoc observations | exploratory |

## 2. Sensitivity: the primary verdicts do not depend on the analysis choices tested

One factor at a time (chord metric, PCA-32 fitted on dev, M = 256, √JSD for beliefs):

- **F1 under O** stays SUPPORTED in every variant, with every replicate's median D above its recomputed envelope (chord 0.279–0.300 vs u_r 0.132–0.161; PCA-32 essentially identical to raw, 0.158–0.177; M = 256 0.163–0.173 vs 0.066–0.090).
- **The F1 rule under P** stays REJECTED in every variant (median D 0.009–0.041, below u_r in every replicate). The one-sided reading of PREREGISTRATION §3 still applies, so this remains uninformative and is not evidence against learning under P.
- **H3′ under P** stays SUPPORTED in every variant, including √JSD on the belief side.
- **Δgeom sign** is positive in every O run-panel under every variant. Under P (H2 is registered for O only, so this is descriptive) the fraction drops from 1.00 to 0.90 (chord) and 0.71 (√JSD).

Scope: this is robustness to four registered single-factor changes, not to every analysis choice. Hook, checkpoint, filtration, coefficient field, σ and the world size were not varied in S7. The layer sweep (S6) covers hooks descriptively.

## 3. Circular coordinates: under O, the trained cylinder's H₁ class is the latent x circle

The circular coordinate of the most persistent H₁ class of the raw `resid_post_3` cloud agrees with the latent angle 2πx(z₃₂)/12:

| | O cylinder, step 5000 | O cylinder, step 0 | y angle (control), O cylinder 5000 | O square, step 5000 | exact belief b³² (ceiling) |
|---|---|---|---|---|---|
| median agreement | 0.884–0.892 (3 runs) | 0.058–0.120 | 0.097 | 0.209–0.298 | 0.915 |
| panels above the permutation-null q95 | 24/24 | 15/24 | – | 24/24 | – |

Reading:

- Under O, training turns the dominant H₁ class of the cylinder models into a coordinate on the world's periodic axis, at about 97% of the agreement that the exact posterior itself reaches. This is the most direct evidence in the project that the detected H₁ signal is the cylinder's circle and not some other loop. It identifies **which** loop F1 detects; F1 itself was already supported.
- **The permutation null is weak on its own.** Even at initialisation, 15/24 cylinder panels exceed its q95, and the trained square models exceed it in 24/24 panels with agreement around 0.25. The null only says that φ is not independent of θ. The informative comparisons are the predeclared ones: initialisation, the non-periodic axis, the square runs and the oracle ceiling. All of them place the O cylinder far apart.
- **Under P** the trained cylinder models stay at the floor (0.049–0.054). This is consistent with the F1 rule failing under P, and it carries the same one-sided caveat: under P, the exact belief's circular mean still tracks x (0.819), but the PH of b³² does not separate the worlds (E1), so the leading H₁ class need not be the x circle even for an ideal tracker.
- **U** (state visible, one replicate): the trained U-cylinder reaches 0.601 (U-square 0.338). The model learns the visible-state dynamics almost completely (captured_U 0.9985). There, no multi-step inference is needed, because the last symbol reveals the state, and a circle aligned with x still appears in the activations. So symbol-level transition statistics can suffice to produce such a circle.

**Limitation (R1 again).** The design has no last-symbol baseline for the circular statistic. Under O the activations decode r_w = b¹ almost perfectly (probe R² 0.965–0.985), and b¹ already varies smoothly with position. So the circular agreement does not show that the circle comes from multi-step history integration rather than from a geometry of the last symbol learned from the dynamics; the U result shows the latter route exists. Follow-up (needs preregistration): the same statistic on R1 (`embed`), on b¹ and on R2/R3.

## 4. Probes: belief is linearly decodable, but no better than from the next-symbol distribution

| test R², median over 6 runs | O | P |
|---|---|---|
| activations, step 5000 → b³² | 0.829 | 0.378 |
| exact next-symbol distribution F₁ → b³² | 0.838 | 0.382 |
| activations, step 0 → b³² | 0.483 | 0.167 |
| one-hot w₃₂ → b³² | 0.421 | 0.144 |
| activations, step 5000 → r_w | 0.974 | 0.825 |
| activations, step 5000 → shuffled b³² | −0.010 | −0.027 |

- Training raises linear belief decodability well above initialisation and above every last-symbol decoder. The shuffled-label control is at zero, so the probe protocol does not manufacture fit.
- **The predeclared descriptive pattern largely fails:** the activations beat all three rivals in only 1/6 runs per condition, because they do not beat F₁. Linearly, the final residual stream carries about as much information about b³² as the exact next-symbol distribution does, and no more. On this evidence the representation is consistent with "what next-token prediction needs" and gives no linear evidence of belief content beyond it. Ridge probes are linear and pooled over 144 coordinates, so non-linear or low-variance belief components are not excluded.
- Under O the selected λ is the smallest grid value (1e-3) in every run, so the grid did not bracket the optimum. Since the probe is linear on 3072 fit rows with 128 features, the effect is likely small, but R² under O may be slightly underestimated. The grid was fixed in D-047 and is not changed after the fact.
- Under P, b³² is much harder to decode from anything (F₁ → b³² 0.38). This matches E1: under P the belief geometry is less tied to observable structure.

This does not contradict H2 or H3′, which are about distance geometry (rank correlation of pairwise distances), not about linear decodability. It does qualify them: matching the belief geometry is compatible with encoding what the next-token objective requires.

## 5. Controls

- **N (3 seeds incl. S4):** NLL at p = 32 equals H(W) = ln 36 to within 2e-5, inside the bootstrap half-width (≈ 2e-4): H0 holds; no leakage. The N models' activation S stays at noise level (median 0.002–0.077 at step 5000).
- **U (seed 1729):** captured_U = 0.9985 in both worlds (regret 0.005 nats against a unigram gain of 3.4 nats): the architecture learns the dynamics when the state is visible. Learning gate: n/a by construction (G_C = 0). PH, one replicate: median S 0.215 (cylinder) vs 0.147 (square), D > 0 in 8/8 panels (median D 0.054). This is descriptive; the U belief cloud is the simplex vertices and U is not a PH positive control.

## 6. Reproducibility (S8)

**Gate G-H: FAIL**, on one check (`rerun_ok`). The other five checks pass. The verdict is kept as recorded (D-049).

- **Clean rerun** (fresh clone of HEAD d2f060b, empty store, same interpreter and locked environment, same Windows machine; S0 0.2 min, S1 0.5 min, S2 4.9 min, S3 14.9 min). 307 of the rerun's 308 non-gate artifacts exist in the main store with identical ids **and identical payload checksums**. They include all 12 checkpoints and 12 activation sets of the retrained run cylinder-O-1729, every dataset, oracle, baseline and spec, and the S1/S2/S3 metric records (S3 compared without its measured timing rows, D-048). All 6 gate verdicts match. CPU training is bitwise deterministic here.
- **The failing item** is the one artifact present only in the rerun: the `run_timing` record of cylinder-O-1729 (`d5f25f7e2968a602`). The code that writes it was added in D-032, after the original S3 run, so the main store never contained it. Its non-timing rows (dev cross-entropy per checkpoint) also appear in the S3 stage record, which matched. This is a provenance gap created by code evolution, not a numerical difference. The predeclared check still fails, and E4 must not claim exact store-level reproducibility.
- **Store integrity:** 785/785 artifacts complete, with parents present and payload checksums verified on load.
- **Reports:** E0, E2 and E3 regenerated from MetricRecords alone, 9/9 generated files byte-identical (the hand-written `exploratory.md` notes excluded).
- **Tests:** module suites 511 passed (7 deselected: slow/integration); slow tests 3 passed (G-A calibration T10/T11, circular coordinates T12); integration 4 passed (I01 S1, I02 S2 mini, I04 leakage end to end, I06 mini rerun identity).

Remaining reproducibility limitations: the rerun used the same machine, OS and Python environment, so it does not test cross-platform or GPU determinism (bundle round trip I05 was never built). Only one of the 17 training runs was retrained. Measured wall times are not reproducible by nature. Integration test I03 (mini S1→S4 pipeline) was never built.

## 7. Negative and inconclusive findings, collected

1. **H3 (F1 rule under P):** rejected; uninformative by design. Still rejected under every sensitivity variant.
2. **H4 timing rule:** rejected. The raw H₁ score rises at step 50 in both worlds, before history use (regret < G_C at step 100). The early rise is not cylinder-specific.
3. **Probes:** activations do not decode b³² better than the exact next-symbol distribution (pattern in 1/6 runs per condition).
4. **Circular coordinates under P:** at the floor (0.05).
5. **λ at the grid edge under O** (probe), and the permutation null exceeded at initialisation in 15/24 panels (circular): two places where the predeclared protocol is weaker than intended.
6. **Gate G-H failed** (`rerun_ok`): the clean rerun reproduced every shared artifact bitwise, but produced one record the main store lacks (§6, D-049).
7. **Integration tests I03 and I05** (mini pipeline, bundle round trip) were never built in W4. I04 (leakage end to end) and I06 (mini rerun identity) were built in S8.

## 8. Limitations (mathematical and methodological)

1. **No causal claims.** Everything here is representational: PH of activation clouds, rank correlations, linear probes, circular coordinates. No intervention tested whether the circle or the belief geometry is used for prediction (X4-causal was not run).
2. **The R1 limitation stands.** Under O the last-symbol embedding carries 0.47–0.89 of the F1 contrast (E2), the activations decode r_w with R² ≈ 0.97, and the circular statistic has no last-symbol baseline. History integration versus learned symbol-level transition statistics remains undecided.
3. **P is one-sided.** Under P the exact belief does not separate the worlds by PH, so a failed rule under P says nothing about learning.
4. **One toy setting.** 12 × 12 lattice, two topologies, one σ, a 4-layer d = 128 transformer trained from scratch on synthetic HMM sequences. Nothing here is evidence about natural-language LLMs or larger models.
5. **Statistics.** Three replicates per cell; panels are sample splits within a run, not replicates. The F1 rule is sign consistency plus an envelope, not a significance test. Pair correlations are descriptive.
6. **PH choices.** Vietoris–Rips over F₂ (F₄₇ for cocycles), S = longest finite H₁ bar / q95 scale, M = 512. The Gaussian floor is context, not a threshold. Sensitivity covered four single-factor changes only.
7. **Circular coordinates** use one cocycle at mid-lifetime; the agreement statistic is invariant to rotation and reflection but not to non-linear reparametrisation of the circle, so it underestimates correspondence for a distorted but faithful circle.
8. **U and extra N** are single replicates where noted (U: one seed per world).
9. **Reproducibility scope:** see §6. The rerun is a fresh clone on the same machine with the same environment, not an independent machine.

## 9. Exploratory observations (post hoc)

- The trained square models' circular coordinates also align with x at about 0.25 (and with y at 0.27). Square activation clouds have a weaker leading H₁ class (E2: S ≈ 0.13). One possible reading is a loop that runs along the boundary of the square rather than around a hole, which would correlate with both coordinates. Not tested.
- Under O, PCA-32 (fitted on dev) reproduces the raw-Euclidean S and D almost exactly (median D within 0.001). The cylinder structure lives in a low-dimensional subspace of the 128-d stream. Consistent with the factorisation argument (RESEARCH_PLAN §3.3); not tested.
- Under P, Δgeom stays positive under PCA-32 and M = 256 but drops under √JSD (0.71). The belief metric matters more under P, where beliefs are flatter. Not tested.

Candidate follow-ups (each needs its own preregistration): circular statistic on R1/b¹/R2/R3; non-linear probes against the F₁ baseline; interventions along the circular coordinate (X4-causal); a contrast-based dynamics rule on a denser early grid (E3 §9).
