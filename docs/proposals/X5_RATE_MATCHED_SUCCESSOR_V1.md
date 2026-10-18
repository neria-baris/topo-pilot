# X5 rate-matched successor v1 — planning only

Date: 17 October 2026. Status: reviewable proposal, not frozen or executed.
X5 G1 remains REJECTED. This proposal does not re-score its dev analysis or access its test.
No new history generation while the active K4b reservation is open.

## Question and reuse

Does the conductance kernel change learning behaviour after matching mean movement rate?
This removes one measured confound; it does not isolate curvature from every other
property of the transition kernel. Spectral structure and state-dependent holding times
can still differ and must be reported as alternative explanations.

Reuse the original world, emissions, learner, exact oracle, paired-seed machinery,
`movement_rate`, `rate_matched_kernel`, `spectrum_report` and
`integrated_autocorrelation` from the analysis API. Add a new configuration/driver only;
do not duplicate kernel construction or filtering. Reuse the repaired runtime controls.

## Arms and process gate, before any model training

| Arm | Kernel | Role |
| --- | --- | --- |
| A | Original flat T0 | Historical-design reference |
| B | Original conductance T020 | Treatment |
| C | I + alpha (T0 - I) | Mean-rate-matched flat comparison |

Compute alpha = movement_rate(T020, pi) / movement_rate(T0, pi) from exact frozen matrices,
not rounded rates in a report. Use `rate_matched_kernel(T0, alpha)` unchanged. If the
result violates nonnegativity or the 0.2 diagonal floor, stop INFEASIBLE_RATE_MATCH; do
not clip it or change the target rate after seeing results.

Freeze T, E, pi and state ordering by hashes. Require stochasticity, stationarity,
common support on off-diagonal edges, common emissions and positive exact context gain.
Require |movement_rate(C)-movement_rate(B)| <= 1e-12. Report distributions of diagonal
probabilities, spectral gaps and autocorrelation of emission-probability state functions
for all three arms. No threshold on those differences is inferred after computation.
If the next-symbol task is already solved by a last-symbol predictor to the registered
resolution, stop before training; its oracle gate and minimum effect must be defined in
the final preregistration before drawing calibration histories.

## Training and primary measurement

Propose six paired model seeds, one model in each arm per seed: 18 models, original
architecture and fixed 5,000-update schedule, with checkpoints every 250 updates including
0. Fresh train/dev/test pools per arm; the same paired initialisation and batch-index
streams are used where possible. Stream collision checks and hashes precede sampling.
Choose and freeze final master seeds only through the existing registry.

For each seed and arm compute the trapezoidal area of normalised oracle regret
regret/G_C over updates 0..5,000, divided by 5,000. G_C is arm-specific, fixed from the
calibration oracle and strictly positive. Negative regret estimates, if any, are reported
with numerical diagnostics rather than clipped to improve an outcome.

Primary contrast: paired AUC(B)-AUC(C). Secondary contrasts: AUC(B)-AUC(A) and
AUC(C)-AUC(A), labelled descriptive unless a multiplicity plan is frozen. This measures
the fixed training trajectory and avoids selecting an event-time threshold after data.
Report every seed, the paired mean and a seed-level interval. Episode resampling may
quantify each model's evaluation uncertainty, but does not substitute for model seeds.

No numeric success/equivalence threshold is invented from the old 250-step result.
Before freezing, specify the smallest scientifically relevant AUC difference, choose
the interval/test and perform power analysis with model-seed variation. Six seeds is a
proposal, not a claim of adequate power. If that design is underpowered within the
available resource ceiling, close UNDERPOWERED or submit a new pre-data plan.

## Resource and inference requirements

Benchmark training and scoring without study payloads. Bind an explicit cumulative CPU,
RAM, output and wall-time allocation covering all 18 runs and final analysis before
release. No GPU purchase or external execution is implied. A full arm/seed failure is
reported; it is not silently replaced. Define incomplete-grid handling in the freeze.

Freeze the analysis implementation and one fresh test before training. Dev is used only
for the registered learning gate and diagnostics, never to choose a favourable checkpoint,
arm, matching alpha or endpoint. The test is scored once after all required models and
validity gates complete. A positive result licenses a difference between these kernels
at matched mean rate. It does not license an isolated causal claim about curvature.
