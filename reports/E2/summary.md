# E2: F1 under condition O (S4)

**F1 verdict: SUPPORTED**

Missing replicates (not run): none

## Prediction vs oracle (p = 32, test panels)

| run | captured | regret (nats) | G_C (nats) | dev CE, final | learning gate | wall (min) |
|---|---|---|---|---|---|---|
| any-N-1729 | n/a | 0.0000 | 0.0000 | 3.5835 | n/a | 15.1 |
| cylinder-O-1729 | 0.986 | 0.0036 | 0.2649 | 2.2676 | pass | 16.0 |
| cylinder-O-2718 | 0.985 | 0.0039 | 0.2649 | 2.2699 | pass | 15.4 |
| cylinder-O-3141 | 0.986 | 0.0038 | 0.2649 | 2.2598 | pass | 14.4 |
| square-O-1729 | 0.992 | 0.0019 | 0.2360 | 2.0807 | pass | 15.5 |
| square-O-2718 | 0.992 | 0.0019 | 0.2360 | 2.0786 | pass | 13.6 |
| square-O-3141 | 0.992 | 0.0018 | 0.2360 | 2.0768 | pass | 15.5 |

## F1 contrasts (median S over 8 panels; RESEARCH_SUMMARY §7.4)

| replicate | S cyl init | S cyl final | S sq init | S sq final | panels D > 0 | median D | u_r | median D > u_r |
|---|---|---|---|---|---|---|---|---|
| 1729 | 0.058 | 0.307 | 0.062 | 0.129 | 8/8 | 0.1582 | 0.0966 | yes |
| 2718 | 0.057 | 0.321 | 0.058 | 0.137 | 8/8 | 0.1762 | 0.0839 | yes |
| 3141 | 0.058 | 0.304 | 0.059 | 0.126 | 8/8 | 0.1726 | 0.0842 | yes |

![D per panel](fig_f1_contrasts.png)

## Representation baselines (D-028: baseline in place of the final checkpoint)

| replicate | model median D | R1: median D (panels > 0, ratio) | R2: median D (panels > 0, ratio) | R3: median D (panels > 0, ratio) |
|---|---|---|---|---|
| 1729 | 0.1582 | 0.1402 (8, 0.89) | 0.0277 (7, 0.17) | 0.0033 (4, 0.02) |
| 2718 | 0.1762 | 0.0828 (8, 0.47) | 0.0346 (8, 0.20) | 0.0171 (6, 0.10) |
| 3141 | 0.1726 | 0.0935 (8, 0.54) | 0.0325 (8, 0.19) | 0.0130 (7, 0.08) |

## H2: Δgeom = ρ(d_A, d_B32) − ρ(d_A, d_B1) (D-031 for same-w₃₂ pairs)

| replicate | world | median Δgeom, all pairs | panels > 0 | median Δgeom, same w₃₂ | panels > 0 (of ok) |
|---|---|---|---|---|---|
| 1729 | cylinder | 0.124 | 8/8 | 0.939 | 8/8 |
| 1729 | square | 0.089 | 8/8 | 0.979 | 8/8 |
| 2718 | cylinder | 0.127 | 8/8 | 0.938 | 8/8 |
| 2718 | square | 0.087 | 8/8 | 0.977 | 8/8 |
| 3141 | cylinder | 0.124 | 8/8 | 0.935 | 8/8 |
| 3141 | square | 0.090 | 8/8 | 0.977 | 8/8 |

## Gaussian floor (reported, never a threshold; D-005)

| replicate | world | S final, panel 1 | iso floor mean / q95 | cov floor mean / q95 |
|---|---|---|---|---|
| 1729 | cylinder | 0.256 | 0.057 / 0.072 | 0.087 / 0.115 |
| 1729 | square | 0.127 | 0.057 / 0.064 | 0.081 / 0.101 |
| 2718 | cylinder | 0.273 | 0.058 / 0.063 | 0.080 / 0.100 |
| 2718 | square | 0.152 | 0.057 / 0.068 | 0.086 / 0.103 |
| 3141 | cylinder | 0.233 | 0.055 / 0.059 | 0.087 / 0.109 |
| 3141 | square | 0.135 | 0.059 / 0.065 | 0.084 / 0.102 |

## H0 (N model; D-029)

Test NLL at p = 32: 3.5835; H(W) = 3.5835; bootstrap 95% half-width 0.0002.

Gate G-F: **pass**
- learning_gate_replicate_0: True (threshold True) -> pass
- learning_gate_replicate_1: True (threshold True) -> pass
- learning_gate_replicate_2: True (threshold True) -> pass
- H0_N_model_nll_not_below_H_W: 3.58355 (threshold 3.58336) -> pass

## X4 (SECONDARY; PREREGISTRATION_X4.md): representation vs readout geometry

Secondary analyses; they never replace the F1 verdict above.

Blinding: Blind to owner and to the planning conductor; a prior conductor session that ended before this plan may have seen S4 console output; no repo changes after the S4 analysis (last commit a4f7844, 11:50).

Missing runs (not run): none

Views: V0 = resid_post_3, raw (primary metric); V1 = LN-gauge-free u; V2 = ln_final_out; V3 = readout-visible P_A u; V4 = readout-null u − P_A u; V5 = softmax(logits), Hellinger.

### F1 rule under each view (median S over 8 panels)

| view | replicate | S cyl init | S cyl final | S sq init | S sq final | panels D > 0 | median D | u_r | F1-rule under view |
|---|---|---|---|---|---|---|---|---|---|
| V0 | 1729 | 0.058 | 0.307 | 0.062 | 0.129 | 8/8 | 0.1582 | 0.0966 | SUPPORTED |
| V0 | 2718 | 0.057 | 0.321 | 0.058 | 0.137 | 8/8 | 0.1762 | 0.0839 | SUPPORTED |
| V0 | 3141 | 0.058 | 0.304 | 0.059 | 0.126 | 8/8 | 0.1726 | 0.0842 | SUPPORTED |
| V1 | 1729 | 0.070 | 0.457 | 0.065 | 0.141 | 8/8 | 0.2916 | 0.1607 | SUPPORTED |
| V1 | 2718 | 0.074 | 0.451 | 0.069 | 0.137 | 8/8 | 0.2980 | 0.1565 | SUPPORTED |
| V1 | 3141 | 0.068 | 0.434 | 0.059 | 0.143 | 8/8 | 0.2776 | 0.1317 | SUPPORTED |
| V2 | 1729 | 0.070 | 0.445 | 0.065 | 0.140 | 8/8 | 0.2832 | 0.1582 | SUPPORTED |
| V2 | 2718 | 0.074 | 0.441 | 0.069 | 0.136 | 8/8 | 0.2897 | 0.1525 | SUPPORTED |
| V2 | 3141 | 0.068 | 0.426 | 0.059 | 0.140 | 8/8 | 0.2725 | 0.1306 | SUPPORTED |
| V3 | 1729 | 0.072 | 0.454 | 0.076 | 0.142 | 8/8 | 0.3062 | 0.1600 | SUPPORTED |
| V3 | 2718 | 0.085 | 0.450 | 0.081 | 0.137 | 8/8 | 0.2865 | 0.1540 | SUPPORTED |
| V3 | 3141 | 0.089 | 0.434 | 0.064 | 0.145 | 8/8 | 0.2646 | 0.1326 | SUPPORTED |
| V4 | 1729 | 0.083 | 0.339 | 0.069 | 0.176 | 8/8 | 0.1203 | 0.0760 | SUPPORTED |
| V4 | 2718 | 0.060 | 0.321 | 0.073 | 0.168 | 8/8 | 0.1601 | 0.0877 | SUPPORTED |
| V4 | 3141 | 0.062 | 0.301 | 0.065 | 0.168 | 8/8 | 0.1404 | 0.0829 | SUPPORTED |
| V5 | 1729 | 0.079 | 0.516 | 0.072 | 0.192 | 8/8 | 0.2987 | 0.1172 | SUPPORTED |
| V5 | 2718 | 0.085 | 0.529 | 0.075 | 0.193 | 8/8 | 0.3149 | 0.1347 | SUPPORTED |
| V5 | 3141 | 0.085 | 0.530 | 0.072 | 0.184 | 8/8 | 0.3152 | 0.1337 | SUPPORTED |

### Δgeom per view (checkpoint final)

| view | median Δgeom, all pairs | panels > 0 | median Δgeom, same w₃₂ | panels > 0 (of ok) |
|---|---|---|---|---|
| V0 | 0.106 | 48/48 | 0.958 | 48/48 |
| V1 | 0.103 | 48/48 | 0.973 | 48/48 |
| V2 | 0.101 | 48/48 | 0.974 | 48/48 |
| V3 | 0.103 | 48/48 | 0.973 | 48/48 |
| V4 | 0.059 | 48/48 | 0.842 | 48/48 |
| V5 | 0.094 | 48/48 | 0.989 | 48/48 |

Pipeline checks (max over runs and checkpoints): ln_reconstruction_max_abs = 0.0000013; logits_from_U_max_abs = 0.0000049; logits_from_visible_max_abs = 0.0000049.

### X4-a (gauge robustness)

X4-a (gauge robustness): the verdict under V1 equals the verdict under V0. If V0 is supported but V1 is not, the primary signal lives in readout-invisible gauge directions: report it as a caveat on F1, not as a refutation.

Result: V0 SUPPORTED, V1 SUPPORTED; equal: yes; caveat case (V0 supported, V1 not): no.

### X4-b (functional geometry)

X4-b (functional geometry): under O, the verdict under V5 is SUPPORTED (expected because oracle future1 separates the worlds 8/8 and the models pass the learning gate). Positive control: median over panels of ρ_s(d_V5, d_future1) ≥ 0.9 in every replicate; if the control fails, X4-b is INCONCLUSIVE (pipeline or model issue).

Positive control, median over panels of ρ_s(d_V5, d_future1) per run: cylinder-1729: 0.999, cylinder-2718: 0.999, cylinder-3141: 0.999, square-1729: 0.999, square-2718: 0.999, square-3141: 0.999; passed: yes.

Result: X4-b SUPPORTED.

### X4-c (where the structure lives)

X4-c (where the structure lives): two-sided, descriptive. Report median_i D under V3 and under V4, and their ratio, per replicate. Interpretation fixed in advance:

median_i D per replicate: 1729: V3 0.3062, V4 0.1203, ratio 2.54; 2718: V3 0.2865, V4 0.1601, ratio 1.79; 3141: V3 0.2646, V4 0.1404, ratio 1.89.

Category: both. Pre-registered interpretation: both / neither → reported as such.

### X4-d (same-last-symbol H2 baseline)

X4-d (same-last-symbol H2 baseline): within pairs with equal w32, compare ρ_s(d_A, d_B32) for the model (V0 and V1) against R2 and R3 (R1 is constant on these pairs and excluded). Supported iff the model value exceeds max(R2, R3) in all 3 replicates and ≥ 7/8 panels.

- A = V0: panels passing per run cylinder-1729: 8, cylinder-2718: 8, cylinder-3141: 8, square-1729: 8, square-2718: 8, square-3141: 8; X4-d SUPPORTED
- A = V1: panels passing per run cylinder-1729: 8, cylinder-2718: 8, cylinder-3141: 8, square-1729: 8, square-2718: 8, square-3141: 8; X4-d SUPPORTED

### H3′ (approved at H3, D-037; decided under P only)

H3′ (requires owner approval at checkpoint H3; until approved, report only as descriptive): under P, at checkpoint 5000, ρ_s(d_A, d_B32) on all pairs (A = V0 and, separately, V1) exceeds both its checkpoint-0 value and max(R2, R3) in all 3 replicates and ≥ 7/8 panels. Under O the same measure is reported for comparison. H3 as registered stays one-sided.

Condition O: comparison only (descriptive); the decision needs S5 (P).
- A = V0: panels passing per run cylinder-1729: 8, cylinder-2718: 8, cylinder-3141: 8, square-1729: 8, square-2718: 8, square-3141: 8; rule outcome SUPPORTED
- A = V1: panels passing per run cylinder-1729: 8, cylinder-2718: 8, cylinder-3141: 8, square-1729: 8, square-2718: 8, square-3141: 8; rule outcome SUPPORTED

### Interpretation caveats (addendum D-040, fixed before results)

The analyses, thresholds and verdict rules above are unchanged. These caveats qualify how the pre-registered interpretations are read; any new analysis they suggest is a separately labelled follow-up, not part of X4.
1. LayerNorm gauge (V1): `ln_gauge_free` is exactly invariant to per-history shifts along the all-ones vector; with eps = 1e-5 it is not exactly invariant to positive rescaling (exact identity: U_eps(αz) = U_{eps/α²}(z)). The V1 definition is unchanged.
2. Readout split (X4-c): V3 is the logit-readout-visible subspace, not necessarily the functionally necessary subspace. Softmax is also invariant to constant logit shifts, so up to one further direction inside range(A) does not affect the predictive distribution. V4 is logit-readout-null. H1 structure in V3 is not evidence of causal predictive use; that needs interventions.
3. Functional geometry (X4-b): the oracle's future1 separating the worlds does not mathematically guarantee that the trained model's predictive cloud has the same topology (passing the learning gate bounds an average KL, not H1 persistence). X4-b is a falsifiable empirical hypothesis; "expected" above is a prediction, not a theorem.
4. Gauge robustness (X4-a): a verdict difference between V0 and V1 establishes sensitivity to normalisation (per-history centring and rescaling), not that the whole signal lies in the mean-shift gauge direction.

