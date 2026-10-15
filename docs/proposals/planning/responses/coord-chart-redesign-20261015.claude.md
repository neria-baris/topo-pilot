STATUS: PROPOSAL

# coord-chart-redesign-20261015: Claude planning track (L)

Planning only. No Python, tests or data were run, and no store file was opened except `jobs/0018/report.md`. I read: the request; job 0018 report and review; `docs/proposals/CIRCULAR_HISTORY_K4_PROTOCOL_DRAFT.md`; `tools/x4_circle_history/chart.py`, `cochain.py`, `adapter.py` and `CONTRACT.json` (chart section); `src/topo_pilot/topology/circular.py`, `src/topo_pilot/analysis/circular.py`, `src/topo_pilot/experiment/s7_circular.py` and `report_e4_s7.py`; `docs/proposals/CIRCULAR_BASELINE_AUDIT_REPORT.md`; `C1-FROZEN-v1.md` §1, §2, §9 to §19; the owner charter; and the owner message, parts B3 to B6. All of this is at main @c2046fc.

---

## Summary (≤ 300 words)

**Diagnosis.** The K4 graph at scale r is connected exactly when r ≥ ℓ_max, the longest minimum-spanning-tree edge (the largest finite H0 death). The bar's midpoint fell below ℓ_max.

E4 S7 ran the same construction on the same 512 vectors: same ripser call, F47, bar, midpoint and edge rule. So E4's 1729 panel-1 coordinate (agreement 0.892) came from this same disconnected graph. E4's least-squares step silently gives each off-giant component a constant phase. Since E4 still reached 0.892, against 0.921 for the exact-belief angle, the giant component very probably holds ≳93% of points and carries the circle. That makes "wrong or short bar" implausible and favours "a few outliers isolated at r". This is an inference, not a measurement.

**Recommendation.** Before any new computation, freeze one redesign: **chart v2 = the largest connected component at the unchanged scale, gated at ≥ 95% of landmarks.** Everything else stays frozen; v2 is bitwise v1 when the graph is connected. Then run a label-free geometry diagnostic (about one CPU-minute) on panels 1–2 of all three models.
- If every case keeps ≥ 95% in the giant component: implement v2. C1 builds its chart once on **its own fresh calibration histories** and validates it on fresh validation histories.
- Otherwise: stop the chart route.

**K4 stays closed** (owner rule B3-A, no rescue). For priority 1 its value would only be exploratory, on exposed data.

**Worth it?**
- **Priority 2:** yes, at this small cost. C1 is the only designed causal test, blocked by a defect in the instrument. Rough chance of a C1 scientific verdict: 15–25%.
- **Priority 1:** not by rescuing K4. A later fresh-history protocol, reusing v2 and C1's oracle, is the better route.

---

## 1. Diagnosis without data

### 1.1 Exact facts from the code

1. **Connectivity criterion (exact).** `edge_list(D, r)` keeps every pair with D ≤ r. So G_r is the 1-skeleton of VR_r.
   - G_r is connected **iff r ≥ ℓ_max**. Here ℓ_max is the longest edge of a Euclidean minimum spanning tree, which is the largest finite death in ripser's H0 diagram `dgms[0]`.
   - The number of components is 1 + #{finite H0 deaths > r}.
   - A landmark is isolated iff its nearest-neighbour distance d1_i > r.

   `fit_chart` computed `dgms[0]` and then discarded it. The quantity that decides the failure was therefore available, and it was not persisted.
2. **The class lives in one component.** b ≤ r < d, so the selected class is alive at r. Any representing cycle is connected, so it lies inside a single component. Other components can only receive an arbitrary constant phase.
3. **Lift and failure point.** The lift succeeded on the whole disconnected complex. Triangles never cross components, so restricting it to any component is still an exact, closed integer cochain. `primitive_class` failed only because its BFS from vertex 0 (the lowest history ID) did not reach every vertex. This tells us nothing about where vertex 0 lies.
   - The 0.031 s lift is consistent with the `centered_exact` branch, which makes no solver call.
   - However, `lift_info["kind"]` was not persisted.
4. **E4 used the same graph.** `topology/circular.py` (E4 S7) makes these calls:
   - `ripser(D, maxdim=1, thresh=D.max(), coeff=47, distance_matrix=True, do_cocycles=True)`;
   - argmax lifetime;
   - r = b + 0.5(d − b);
   - edges D ≤ r;
   - the same centred cocycle representative, with the same orientation convention.

   Its inputs are `act.A[rows, hook, :]` in float64. These are the same vectors as K4's landmarks, in a different row order. Ripser only compares distances, so the diagram is the same, and so is the bar (barring an exact lifetime tie).

   **E4's 1729 panel-1 coordinate was therefore computed on this same disconnected G_r.** E4 did not fail, because `lstsq` of the dense Laplacian returns the minimum-norm solution. That solution gives each component its own offset: phase 0 for every isolated point and for every component with no cocycle support.

### 1.2 Bound from E4 (inference; assumptions stated)

E4 coordinates are functions of the history, so their agreement with the latent angle θ has a population ceiling E|E[e^{iθ}|h]|. That is the "b32-angle" agreement, 0.921 on 1729 panel 1, against the model's 0.892. In-sample the ceiling can be exceeded by about 0.02 of sampling noise.

Suppose the off-giant points (fraction ε) received constant phases whose latent angles are not concentrated. Then A ≈ (1 − ε)·A_giant. That gives **ε ≲ 1 − 0.892/(0.921 + 0.02) ≈ 5%**: at most about 25 of 512 points.
- **Caveat:** if the off-giant points share similar x, their constant phase could add coherently, and the bound would weaken.
- 2718 and 3141 give similar values (0.893 and 0.883 on panel 1). E4 never checked connectivity in any of its 48 run-panels.

### 1.3 Candidates and what separates them

| Candidate | Mechanism | Prior (given §1.1–1.2) | Diagnostic signature (label-free) |
|---|---|---|---|
| H-OUT: isolated outliers / heavy tail | A few points have d1 > r: rare histories, or a high-variance direction in raw 128-d resid_post_3 (no normalisation). Breakdown point of the frozen rule: 1 point. | **Most likely** | Few components; the non-giant ones are singletons or of size ≤ 5; giant fraction g ≥ 0.95; excluded points rank top in d1 and in ‖x − mean‖; ℓ_max ≫ r. |
| H-CLUS: clustered cloud | Separate clusters (e.g. by last symbol or y) do not link at r. | Unlikely (E4's 0.89 needs a large giant) | A non-giant component of size ≥ 10 (about 2%); g < 0.95; excluded points not extreme in norm. |
| H-BAR: short or wrong bar | A noise bar is selected, so r is small and most points are isolated. | **Very unlikely**: E4 used the same bar and got 0.89. | r ≲ median(d1); g small; top lifetime not dominant over the second. |
| H-DEATH: connectivity only after death | ℓ_max ≥ d, so no scale inside the bar's lifetime connects the graph. This does not cause the failure by itself, but it decides whether option (b) can work. | Unknown | ℓ_max vs d. |
| H-DIM: concentration of distances | d1 ≈ d8 ≈ typical distance in 128-d, so r sits inside the d1 distribution. | Possible, overlaps H-OUT | Fraction with d1 > r; r / median(d1). |
| Implementation defect | — | Very unlikely | The BFS, edge rule and lift are consistent with the frozen tests. The diagnostic's integrity check (1729 panel 1 must show ≥ 2 components) settles it. |

**Discriminating diagnostic.** A single label-free computation per model and panel decides between these: (b, d, r), ℓ_max, component sizes, giant fraction, d1/d8 quantiles, and the norm rank of the excluded points. No fitting, phases, lift, m32, tokens or latent values are used. §4 gives the full specification. It adds almost no new exposure, because E4 S7 already ran the identical PH on these panels.

---

## 2. Redesign options

Notation: n = 512 landmarks, r = the frozen midpoint, C* = a component of G_r.

### (a) Largest connected component with an exclusion gate (chart v2): recommended

**Exact rule.** Steps 1–4 are unchanged: D, ripser F47, `select_h1_bar`, r = (b + d)/2, `edge_list(D, r)`.
5. Components of G_r (deterministic). C* is the largest; ties go to the component with the smallest landmark index.
6. Gate GIANT: |C*| ≥ ⌈0.95·n⌉, which is 487 for n = 512. Otherwise `Unresolved("giant component below 0.95")`, i.e. INCONCLUSIVE.
7. Restrict the cocycle, edges and triangles to C*. Re-index while preserving ascending ID order. Then run `triangle_system`, `integer_lift`, `primitive_class` and `smooth_phase` **unchanged**; the BFS root is the lowest ID in C*. If the class is trivial on C*, the existing g = 0 check raises Unresolved.
8. Chart landmarks, IDs and φ cover C* only. σ, R and d8 come from the **frozen** `_neighbor_scale` on the full n×n D, which is literally the current code path. Extension therefore uses only charted landmarks.
9. **Persist before anything can raise:** b, d, r, ℓ_max, number of components, component sizes, excluded IDs, lift kind and g. This closes the 0018 persistence gap.
10. **Fidelity with a direct chart:** agreement is computed on the rows that the direct chart charts (its own C*). Support, bins and resultant still use all 512 extended rows.

**Identifiability.**
- The chart is a deterministic function of the calibration cloud.
- The gauge is unchanged.
- K4's zero benchmark (a suffix-only u has Δ4 = 0) and C1's estimand are both conditional on a fixed calibration-only chart. Excluding *calibration landmarks* does not touch either. *Scored rows* are never excluded; any unsupported row still triggers the frozen rules.
- **Breakdown:** up to 25 arbitrary outliers leave φ unchanged. Only R (the 99th percentile) responds once outliers exceed 1%.

**Comparability.**
- **With v1:** if G_r is connected, v2 is bitwise v1, so connected models are unaffected.
- **With E4:** on C*, φ_v2 = φ_E4 + const whenever the lift is centred-exact and g = 1. Both are the harmonic representative of the same cochain on the same connected graph, and the integer q of `primitive_class` vanishes mod 2π. So v2 is "E4's construction on the giant component, with K4's certificate".
- **Old K4 results:** the identity and oracle PASS records stand; no chart result exists.

**Risk of fitting to the failure: low to moderate.**
- There is one new number, 0.95. It reuses C1 §9's existing 5% off-support allowance. It is fixed before the diagnostic and is independent of the diagnostic's values.
- The disclosure must still say that the rule was designed after v1 failed, and that my ε estimate in §1.2 used exposed E4 results.

**Residual risk.** v2 tightens support for outlier *queries*, because their outlier landmark neighbours no longer carry phases. K4's every-row validation support can then fail. The diagnostic predicts the distance half of this (§4, item 9).

**Changes.** K4 gets a new chart module (`chart_v2.py`, reusing `chart.py`/`cochain.py` unchanged), a new CONTRACT chart version, and new tests. C1 changes §14 (§3.2). Everything else stays frozen.

### (b) A scale rule that guarantees connectivity

**Rule b1:** r′ = max(r, ℓ_max). It is valid only if ℓ_max < d; otherwise INCONCLUSIVE. Using r′ ≥ d would kill the class: every period would be 0, so g = 0. **Rule b2:** r′ = d − ε.

**Identifiability.** The class is the same for any r′ ∈ [b, d), but the harmonic representative depends on r′. b1 is backward-compatible when the graph is connected.

**Problems.**
- **Breakdown point 1/n.** The single farthest point sets the scale for the whole chart, which makes the calibration chart and the direct chart behave differently. That is a fidelity risk.
- **Near-death charts are poorly conditioned.**
- **Cost.** Edges at r′ near d may reach 10⁴–10⁵, and triangles 10⁶ or more. `triangle_system` is a pure-Python triple loop, and the MILP has one variable per edge. Exhausting resources is likely; K4's 30 s lift cap and 180 s wall would bind. C1 lifts the CPU cap, but the 600 s wall remains.
- **b2's ε is an arbitrary knob.**

**Changes.** The scale line of the K4 CONTRACT and C1 §14. When ℓ_max > r it is not comparable with E4. **Fitting risk: moderate. Not recommended.**

### (c) Maxmin landmarks plus extension

Greedy maxmin selects outliers *first*, because they maximise the min-distance. So it does not cure outlier-driven disconnection, and it adds a landmark-count knob L. It changes the landmark set, the PH and the bar, which makes comparability with v1 and E4 poor. Perea-style sparse circular coordinates still need every point covered by the landmark balls, so outliers break them too. **Not recommended.**

### (d) Reuse E4's `CircularCoordinates` as the chart

The exact differences from K4's `fit_chart`:

| Step | E4 `circular.py` | K4 `chart.py`/`cochain.py` |
|---|---|---|
| PH | ripser F47, thresh = D.max() | ripser F47, thresh = ∞ (same diagram) |
| Bar | argmax lifetime (first index on ties) | largest finite strictly positive; ties by birth, death, index |
| Scale / graph | b + 0.5(d − b); D ≤ r | (b + d)/2; D ≤ r (same up to float rounding) |
| Cochain | centred F47 representative, used as a **real** cochain; no closure check | exact **integer** lift (MILP correction), closure and congruence certified |
| Normalisation | none (the winding number can be g ≠ 1) | primitive class β = periods / g, with g coprime to 47 |
| Smoothing | dense min-norm `lstsq` on the Laplacian; **disconnection tolerated silently**; isolated points get phase 0 | `lsqr` with f[root] = 0 after BFS; **disconnection is Unresolved** |
| Output | transductive phases only | fixed chart + calibration gauge (m32) + 8-NN extension, support and fidelity gates |
| Agreement target | latent x(z32) (privileged) | gauge to m32 on calibration; fidelity extension vs direct chart |

As a K4/C1 chart, (d) would drop the certificate and give excluded landmarks arbitrary phases that then leak into the extension. It also has no out-of-sample map. The one useful part of E4 is that it does not fail on disconnection, and (a) already takes exactly that. **(d) is dominated by (a).**

### (e) Denoising or kNN-graph chart

- **Density filtering** (keep the densest x% by k-NN distance, then run PH) is the classical robust alternative. It changes the bar and the PH, and adds two knobs (k and x). The filtered cloud can still be disconnected at its own midpoint.
- **DTM or weighted-Rips filtrations** are principled, but they are new code and a new chart family.
- **A kNN graph in place of G_r** has edges outside VR_r on which the cocycle is undefined, so it would need a different complex.

Fitting risk is high; there is no comparability with v1 or E4; and the cost is a new family with new tests. **Not now.**

### (f) Stop K4 and C1 and redirect

- **K4:** it is already closed INCONCLUSIVE, and the owner's B3-A rules out a rescue. This is the default.
- **C1:** stopping leaves priority 2 without any designed test.
- **Redirect options:**
  - (i) Re-protocol C1 with a supervised phase, arg of a decoded m32. C1 §14 forbids this now, it would change the question to "use of the belief angle direction", and it needs a full re-review.
  - (ii) Move to queue D (priority 3, oracle-only), which is already running as job 0019.
- **Stop is the right outcome** if the diagnostic shows giant fraction < 0.95 anywhere. In that case the PH chart at this site is not robust, and each further redesign would be fitted to the failure.

### Summary table

| Option | Changes in K4 | Changes in C1 | Stays frozen | Comparable to v1 / E4 | Fitting risk | Cost |
|---|---|---|---|---|---|---|
| (a) LCC ≥ 0.95 | chart v2 module, CONTRACT chart version | §14 branch C′ (fresh) | PH, bar, scale, lift, gauge, extension, σ/R, gates, scoring | v1: identical if connected; E4: identical on C* (centred-exact, g = 1) | low–moderate | ~100 lines + ~12 tests; seconds of CPU |
| (b) max(r, ℓ_max) | scale rule | §14 | all else | v1: identical if connected; E4: no | moderate | small code, possibly prohibitive CPU |
| (c) maxmin | landmarks, PH | §14 | gauge, extension | no | moderate–high | moderate |
| (d) E4 chart | drops certificate, needs an extension | §14 | — | E4: yes; v1: no | low, but invalid | moderate |
| (e) denoise / kNN | new family | §14 | gauge | no | high | high |
| (f) stop | none | stays INCONCLUSIVE/CHART_UNAVAILABLE | everything | — | none | none |

---

## 3. Recommendation: one design plus a mechanical decision tree

### 3.1 Pre-registration discipline (everything fixed before any new computation, the diagnostic included)

Freeze one document, `CHART-V2-FROZEN`, with its sha256 recorded in DECISIONS **before the diagnostic runs**, after a result-blind Codex review. It contains:
1. the v2 rule (§2(a), steps 1–10), with 0.95 and the tie rule;
2. the diagnostic specification and its reading rule (§4);
3. the C1 §14 delta text (§3.2);
4. the K4 decision (§3.3).

After the diagnostic, only the pre-declared branch is applied. No threshold, rule or scope may change. Any later design after a STOP needs a new owner decision and is labelled exploratory.

### 3.2 What changes in C1 (delta to §14 and §16 row 0)

**New branch C′ (construct once with chart v2):**
- **Trigger:** K4 attempted charts and ended INCONCLUSIVE at chart_calibration *because the graph was disconnected*, and the diagnostic reading is GO.
- **Construction:** identical to branch C (512 lowest-sequence_id fresh rows of cal block 0; gauge on their oracle m32; direct chart on the 512 lowest-sequence_id rows of val block 0; at most 6 constructions), but with `fit_chart_v2`.
- **C1 never loads a chart built on exposed data.**

**Validation support in branch C′.** Use ≥ ⌈0.99·512⌉ = 507 supported rows, in place of every-row. **This is an anticipatory change that the owner must decide** (Q4).
- **Reason:** consistency with C1's own M3 rule (Sup(S) ≥ 0.99). Under C1 §9, unsupported rows keep their phase and stay in the endpoint, so C1 never needs every-row support.
- **Disclosure:** it is motivated by the outlier hypothesis, and it is fixed before any diagnostic value exists.

**Everything else in C1-FROZEN-v1 is unchanged.** That covers seeds, scope tag `c1-sf-v1`, gates, thresholds, the ladder, the certificate and the stop rules. The delta is versioned C1-FROZEN-v1.1, with a review of the delta only.

### 3.3 K4

K4 stays closed INCONCLUSIVE. **No K4b by default** (B3-A: no rescue).

If the owner nevertheless wants the exploratory K=4 point for priority 1, a K4b would run as follows:
- **Rules:** the frozen K4 protocol with chart v2 only, every-row support kept, and the identity/oracle stages re-run or sha-bound (Q5).
- **Gate:** run only if the diagnostic predicts full distance-support for all three models (§4, item 9). Otherwise it would certainly fail.
- **Status:** exploratory, as before.

### 3.4 Handling the exposed data

1. The diagnostic touches only the geometry of panels 1–2. E4 S7 already ran the identical PH on all 8 panels, and K4's scoring panels 3–8 stay untouched.
2. **The redesigned rule is first tested on fresh data**, through C1 branch C′ (C0-cal and C0-val on new histories). This is the honest test of a rule designed after the failure.
3. A K4b result could never become fresh. Reports state that v2 was designed after the v1 failure.
4. **Possible next extension (not proposed now):** a fresh-history K-profile of the v2 coordinate (Δ1, Δ2, Δ4) for priority 1. It would reuse C1's oracle and sampling with a new seed scope.

### 3.5 Decision tree for the owner

```
Owner morning decision
├─ A3 STOP → K4 closed, C1 INCONCLUSIVE/CHART_UNAVAILABLE; continue queue D.
├─ A2 Diagnostics only, no v2 commitment → run §4; any later design is
│      fitted to the diagnostic → acceptable only with C1 fresh validation.
└─ A1 (recommended) Freeze CHART-V2 + diagnostic + reading + C1 delta (Codex review),
       then run the §4 diagnostic:
       ├─ INTEGRITY fails (1729 p1 shows 1 component, or the bar mismatches 0018 context)
       │      → FAIL_TECHNICAL; investigate the environment; stop.
       ├─ GO   (every one of the 6 model×panel cases: g ≥ 0.95)
       │      → independent tests → implement chart_v2 → C1-v1.1 runs branch C′ on fresh data.
       │        K4b only if the owner opts in AND item 9 = 100% for all 3 models.
       └─ STOP (any case g < 0.95)
              → chart route closed; report the descriptive pattern (H-CLUS/H-BAR/H-DEATH);
                no (b)/(e) without a new owner decision.
```

### 3.6 Cost

| Item | Compute | Effort |
|---|---|---|
| Freeze document + Codex review | — | 1 planning round |
| Diagnostic job | < 60 CPU s (six ripser runs at ~0.1 s, plus three artifact loads at ~3–8 s) | ~100 lines + 3 synthetic tests |
| chart_v2 | — | ~100 lines wrapping the frozen functions; ~12 independent tests; full suite re-run |
| C1 | as frozen: 2–6 CPU-h (+ ≤ 0.5 h for the branch-C′ chart) | unchanged |
| K4b (optional) | ≤ 1200 CPU s as before | new CONTRACT version and release |

### 3.7 Honest worth estimate

- **Priority 1:** redesigning in order to rescue K4 is **not worth it**. It would be exploratory on exposed data and would not resolve the audit's open question cleanly. Oracle B4 is about 0.07 against a 0.01 margin. It would also cut against the owner's no-rescue rule. Better route: a fresh-history profile later.
- **Priority 2: worth it, conditionally.** C1 is a fully specified causal test, blocked by an instrument problem that E4 suggests is minor. The incremental cost is small: one diagnostic plus about 100 lines, with no new science machinery.
- **Rough, subjective probabilities:**
  - P(GO) ≈ 0.65;
  - P(v2 passes C1's fresh C0-cal/C0-val | GO) ≈ 0.6; fidelity ≥ 0.80 between two independently fitted charts is the next likely failure;
  - P(C1 then reaches a scientific PASS/FAIL/MIXED, through M2, M3, V1, V3 and P1) ≈ 0.4–0.6;
  - **overall ≈ 0.15–0.25.**

  If the owner judges that too low for C1's 2–6 CPU-h plus supervision, **stop** is defensible. The diagnostic alone is still worth running, because it costs about a minute and settles whether the PH chart at this site is usable at all.

---

## 4. Minimal diagnostic job (if the owner approves diagnostics only)

**Name:** DIAG-chart-geometry (exploratory; owner-authorised; single scientific job; existing mailbox, release and meter; new output store `X:/…/x4-chart-diag-store-00NN`).

**Inputs.**
- The K4 CONTRACT identities for 1729, 2718 and 3141.
- `adapter.E4Adapter.panels(model, (1, 2))`, which refuses other panels. Use the `activation` arrays only, in ascending history_id order: exactly K4's landmark matrices.
- **Not read:** tokens (`named32`), oracle quantities, m32, sidecar or latent values.

**Computation per (model, panel), 6 cases.** This reuses the frozen functions read-only, without editing them.
1. `D = cdist(X, X)`, then `ripser(D, maxdim=1, coeff=47, distance_matrix=True, do_cocycles=True)`, as in `fit_chart`.
2. `k = chart.select_h1_bar(dgm1)`; record b, d, r = (b + d)/2, and the top 5 H1 bars (b, d).
3. **H0:** ℓ_max = the largest finite death; n_comp_H0 = 1 + #{finite deaths > r}.
4. `cochain.edge_list(D, r)`, then components with `scipy.sparse.csgraph.connected_components`.
   - Record the sorted sizes, the giant fraction g, and the C* tie rule as in v2.
   - **Consistency check:** n_comp must equal n_comp_H0.
5. `chart.cocycle_to_edges(cocycles[1][k], edges, 47)`: the number of nonzero entries inside C* and outside it (descriptive).
6. **Per point:**
   - d1 and d8, with quantiles 0.5, 0.9, 0.99 and max;
   - the number isolated (d1 > r);
   - for excluded points: d1, d8 and the percentile rank of ‖x − mean(X)‖;
   - r / median(d1).
7. R_all = 2·quantile(d8 over all 512, 0.99, inverted_cdf), which is the frozen formula.
8. For option (b), descriptive only:
   - whether ℓ_max < d;
   - edge counts at r and at max(r, ℓ_max);
   - triangle counts as trace(A³)/6 with the dense 0/1 adjacency.
9. **Support prediction (geometry only; no phase):** for each model, the fraction of panel-2 rows whose 8th-nearest distance to panel-1 C* landmarks is ≤ R_all(panel 1).
10. **Identity material:** excluded history IDs, and the cross-model overlap counts of the excluded sets. If the same histories are excluded across models, the cause is the histories; if not, it is the models.

**Outputs.** One JSON per case plus a summary, with sha256 of each. Not saved: activations, phases, cocycles or tokens. Wherever a reused function allows it, persist the values before any step that can raise.

**Pre-declared reading** (mechanical; the labels are descriptive, and only GO/STOP drives decisions):
- **INTEGRITY:** 1729 panel 1 must show n_comp ≥ 2, and n_comp must equal n_comp_H0 in every case. Otherwise FAIL_TECHNICAL, and stop.
- **GO** iff g ≥ 0.95 in all 6 cases. Otherwise **STOP**.
- **K4b-eligible** (relevant only if the owner opts in) iff item 9 = 1.0 for all 3 models.
- **Pattern label per case:**
  - OUT: g ≥ 0.95 and the largest non-giant component ≤ 5;
  - CLUS: some non-giant component ≥ 10;
  - BAR: r < median(d1);
  - DEATH: ℓ_max ≥ d (may co-occur);
  - MIXED: otherwise.

**Tests (synthetic only, written first).**
- A noisy circle plus 3 far outliers gives n_comp = 4, g = (n − 3)/n, and ℓ_max = the outlier gap.
- Two disjoint circles give CLUS.
- A point at exactly distance r is connected (≤).
- The n_comp_H0 identity holds.
- The adapter refuses panel 3.

**Limit.** 300 CPU s measured, 1 thread. If it is exceeded, stop safely.

**What it cannot do:**
- it does not estimate fidelity, phases or any endpoint;
- it does not change K4's verdict;
- it does not test v2 itself; C1's fresh gates do that.

---

## Questions for the owner

1. **Route.** Do you choose A1 (freeze v2, the diagnostic and the C1 delta, then the diagnostic), A2 (diagnostics only, any design afterwards treated as fitted) or A3 (stop)? I recommend A1.
2. **Single redesign.** Do you approve chart v2 (largest component at the unchanged midpoint, gate ≥ 95%, everything else frozen, bitwise v1 when connected) as the *only* candidate, with STOP as the pre-declared alternative?
3. **C1 branch C′.** After K4's connectivity INCONCLUSIVE, should C1 build its v2 chart once on its own fresh calibration and validation histories, and never reuse a chart built on exposed data? (This is the C1-FROZEN-v1.1 delta, reviewed by Codex.)
4. **C1 validation support.** In branch C′, replace every-row support on the 512-row validation panel with ≥ 507/512, matching C1's M3 level of 0.99? This is anticipatory, fixed before the diagnostic, and disclosed as such. Or keep every-row and accept the risk?
5. **K4b.** Keep K4 closed (my recommendation; your B3-A no-rescue rule), or allow an exploratory K4b with v2, run only if the diagnostic predicts full support? If K4b runs, should it re-run the identity and oracle stages, or bind the 0018 PASS artefacts by sha?
6. **Threshold.** Is 0.95 acceptable? It reuses C1's 5% off-support allowance. 0.90 is the lenient alternative, and either must be fixed before the diagnostic.
7. **E4 disclosure.** Add a documentation-only note that E4 S7's construction silently tolerated disconnected graphs, giving off-giant points a constant phase? This changes no E4 claim; if anything, it means the reported agreements are slightly diluted.
