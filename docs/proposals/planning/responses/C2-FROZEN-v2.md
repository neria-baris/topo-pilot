STATUS: C2-FROZEN-v2, FROZEN 2026-10-22 (Codex CONFIRM_AFTER_MINOR_FIXES; NEW-10..NEW-13 applied verbatim). Pre-data revision of C2-FROZEN-v1, sha256 4d97d8e258cfab906ccfe1d99564d4dd74202edd96dd63eb836abd64c277a3d8). It is C2-FROZEN-v1 with exactly the changes listed in §21: D-0104-1 (the y-placebo donor H^R is replaced by the one-symbol-row y-translation donor H^Y; H4 f_y ≥ 0.85, owner addendum 23), D-0104-2 (the scale-invariant F1 G1 identity check), R-0104-1 (the 14-module footprint) and the carried coordinator addenda 1–2. No C2 data existed when it was made (S3; §21). It authorises nothing by itself. No run of any kind may start before the re-freeze and an owner AUTH addendum naming the re-frozen sha256 and the forecast. The owner-level readings of §18 are confirmed by owner addendum 21. (v1 status line, historical: MERGED DRAFT v3, writer revision round 3, frozen as C2-FROZEN-v1.)

# C2-FROZEN-v2 (candidate; frozen v1 = C2-MERGED-v3): does the learned circle matter for prediction? Exact readout attribution of natural counterfactual responses to a registered circle-code interchange (C2-R), with an upstream interchange family (C2-M), an oracle-phase secondary (C2-S*) and a report-only rotation arm

| Field | Value |
|---|---|
| Protocol id | C2-MERGED-v3 (supersedes C2-MERGED-v2, sha256 `07912b3310e41c497d0effda102fbd1fe3d242ea7271feb759430ce666d5496d`, which superseded C2-MERGED-v1, sha256 `d8043b88ff6bd108a7bbdcafbdd8534bd788bf10adaa8558d9b017aaad0d93db`). Seed and data scope tag `c2-v1` (the lineage tag is unchanged). New package `tools/c2_readout/`; new store `X:/Downloads/projects/topo-pilot/c2-readout-store/` |
| Revision (v2 candidate) | Pre-data revision of C2-FROZEN-v1 (sha256 `4d97d8e258cfab906ccfe1d99564d4dd74202edd96dd63eb836abd64c277a3d8`) by the protocol writer, launched by coordinator dcecc9ff, 2026-10-22. Binding inputs: owner addendum 23 (`archive/owner-decisions-20261015/OWNER_DECISIONS.addendum-23.md`, sha256 `21c941a14aacf35a2eacd88d1c8310ddc62037136715aef327973fa7c2b135ab`; option A verbatim: "A: הזזה טהורה, סף 0.85 (מומלץ)"); the job 0104 interim review (`jobs/0104/review.md`, sha256 `e832173ae90807e1c59383c8976038786c7225f4b145534e4b2f5abd30a79b8a`; D-0104-1, D-0104-2, R-0104-1); coordinator addenda 1–3 to v1. Planning only: no model run, no sampling into the `c2-v1` namespace, no store payload, no git write. Read-only: v1, the addenda, the job 0104 report and scratch summaries and scripts (`fy_check.txt`, `fy_alt.txt`, `fy_check.py`, `fy_alt.py`, `fy_alt2.py`; no payloads), `tools/c1prime/c1_oracle.py`; one synthetic check of the whitening identity (random matrices, no data). Change log: §21 |
| Role | Protocol writer (W), revision round 3, launched by coordinator dcecc9ff. Planning only: no model run, sampling, test run or repository code run; no store payload opened (`*.npz`, `*.pt`); no git write. Read-only commands: `sha256sum` on documents, `git show HEAD:<path>` of committed code, one line (line 8, the M0 gate record) of `c1prime-store/GATES.jsonl`, and scalar desk arithmetic (Python as a calculator, no data). Round 3 added read-only `sed` reads of `tools/c1prime/c1_oracle.py` 130–201 and `c1_gates.py` 76–107 in the main worktree at 967605c |
| Date | 2026-10-21 |
| Review (binding through the rulings) | `planning/responses/coord-c2-review-20261021.codex.md`, sha256 `7980a0215aced4476d591aad7c3ef993cbb8efe9482b0261f2d93014354ce6db` (verdict NOT_READY; RC-1..RC-16; cited **RC-n**). Codex thread 01a15e5c-12c0-70b3-b6ab-c11d214ea42f |
| Confirmation review (round 3; binding through the rulings) | `planning/responses/coord-c2-review-20261021.v2confirm.codex.md`, sha256 `2b76cf4d31ccc1bc7b80dbc73afa995bee4518eb42fb325abd74bb597af9830e` (verdict NOT_READY; NEW-1..NEW-8; RC-1, RC-10, RC-13, RC-14 PARTIAL; every other RC APPLIED; cited **NEW-n**) |
| Coordinator rulings (round 3) | `planning/responses/coord-c2-review-20261021.v2confirm.rulings.md`, sha256 `24f9888fd1b8cdec7321bd48d46a7caba1182ca959150988497d4e6c69e85cb1`: NEW-1..NEW-8 accepted with the reviewer's exact fixes, the PARTIAL RCs completed as specified, no reopening of the accepted scope or of addendum 21; disposition in §20 |
| Coordinator rulings | `planning/responses/coord-c2-review-20261021.rulings.md`, sha256 `70c2c93994fb1d6d2fce7640ccfdc5f8a33cf5549b325af8bc4ad35bb4676501`: every RC accepted with the reviewer's exact fix; disposition in §19 |
| Binding decisions | `planning/responses/coord-c2-causal-20261021.MERGE.md`, sha256 `305b74f7f118955e96e2de59211311c606bc0bdfb0194764576e1a8654abfd51`, MD 1–11 (map below) |
| Owner decisions | `archive/owner-decisions-20261015/OWNER_DECISIONS.addendum-20.md`, sha256 `d8cc0f1875535674ba7e8b8d018b9b5908fb5e800abae5f298bd104c4e75d8c8` (Q1–Q4, verbatim, binding; thresholds unchanged in v2). Also addendum 10 (`e28bde0c1b2fe989fff945af282aa62f378fb4ef93987c7c1c2e3874993722a2`: C1′ closed; post-data tolerance changes need the owner) and addendum 18 (`faf611dbdc983bd9800fd251113e90583f401876ee9cb98633729d3120ebccd2`: measure-only CPU, read by MD 10 as applying here); addendum 21 (`1e6e88382cc32dbef5ae2b6a3cc3ebf80901c76924064170b7b777400df4380f`: the §18 readings confirmed: claim scope, restricted ROUTED_AROUND, NOT_RUN exclusions, O-2 with the qualifier only, O-3, a measure-only budget with the revised forecast presented at AUTH) |
| Tracks | Primary design: track L `coord-c2-causal-20261021.claude.md`, sha256 `2ffd8ce5da722239533b990530e5ece5c43295fc4f41d37984e61caa8d89cd4a` (cited **L§n**). Grafts: track X `topo-pilot/docs/proposals/C2_CONSTRAINED_CIRCULAR_INTERVENTION_HE.md` at 967605c, sha256 `e9465164fb0ee96e53eb2fdb6536ec8c5e24b06ed0749f6146971125cd3e01bd` (cited **X§n**) |
| Comparison | `coord-c2-causal-20261021.compare.md`, sha256 `a8fddd4ed3c89872924b258eaf7c5b4863dbad77573871b457a402ed6e7dadc0` (cited **CMP §n**; its defects X1–X8 and L1–L7 are fixed as mapped in §17) |
| Request | `planning/requests/coord-c2-causal-20261021.md`, sha256 `1c2d12147608859be846f7f6a59e65248cad3749f3eecf0fc1c97edf5e94cc66` |
| Format model | `X6S1-FROZEN-v1.md`, sha256 `2a909ace38231fbc6647e8ffdb5e6b5f22669a7c92182ae84240f32cd36efb9e` |
| Base commit | topo-pilot main `967605c256bcb554f43d4681326d32efc95bfcc9` (re-checked by W at revision). `tools/c1prime` at 967605c is identical to the C1′ execution commit 93350d7 |
| Records read | `jobs/0041/report.md` (C1′ S3), `jobs/0044/report.md` and `review.md` (C1′ S4, M2-cal), C1-FROZEN-v1 §3; `c1prime-store/GATES.jsonl` line 8 (M0 gate record, 2026-10-16T08:01:43Z; the full `sha_f32` strings, §4) |
| Code read at 967605c | `src/topo_pilot/learner/model.py` (blob `ee1c124c…e039`), `learner/patch.py` (`64d742e8…0ad4`), `learner/config.py` (defaults d_model 128, d_mlp 512, 4 layers, 4 heads); `src/topo_pilot/experiment/x4f_probe.py` (`nested_ridge`, `_ridge_path`), `src/topo_pilot/prediction/ridge.py` (`RidgeProbe`), `src/topo_pilot/analysis/x4f_scores.py` (`standardizer`); `tools/c1prime/{c1_oracle (named_from_canonical, canonical_from_named_cols, G_named), c1_fit (fit_decoder recipe, equivalence_tolerance), c1_means, c1_model (model_inputs, natural_logits), c1_gates, c1_endpoint, c1_data, c1_config, c1_records}.py`, `CONTRACT.json` (chart block); `tools/x4_circle_history/{chart, precision}.py`; `tools/c1prime_registry/c1_registry_sources.py` |
| Arithmetic | **[W]** = worked from recorded numbers or exact algebra (desk arithmetic); **[H]** = heuristic or assumption that a gate or the run measures before anything is decided. No [W] or [H] value is a gate; every gated quantity is computed by the run |
| Next step (MD 11; owner addendum 23) | History: confirmation of v3 → freeze as C2-FROZEN-v1 → owner AUTH (addendum 22, naming v1's sha256). Now: Codex confirmation of this v2 candidate → re-freeze as C2-FROZEN-v2 → owner AUTH addendum naming the v2 sha256 and the forecast → implementation (14 modules, R-0104-1) with the independent authors' updates (T-ORACLE, T-GLS, T-SIZE) → staged jobs |

**MD → section map (MERGE decisions, followed exactly).**

| MD | Decision (short) | Where |
|---|---|---|
| 1 | L's C2-R at `ln_final_out`/32; natural ±2-cell donors, w32 kept; 6-d code (harmonics 1–3 of the C1′ chart phase); GLS nuisance-excluding projector; ψ = E[A_S]/E[A_full] | §2.1–§2.6, §5 |
| 2 | C2-M at `resid_post_2` with a support screen (N2, a radial support screen; RC-6), a context-matched ratio and a licensed ROUTED_AROUND (restricted licence, RC-5); X's rotation arm report-only with the corrected oracle | §2.10, §2.11, §3.2, §3.4 |
| 3 | USED iff LB(ψ) > 0.50; NOT_USED iff UB(ψ) < 0.10 **and** a total-logit-change energy bound (writer sets it; a gate); PARTIAL between; MIXED/INCONCLUSIVE otherwise; V3 at 0.30·G and the code moving with the counterfactual as gates | §2.9, §3.1, §6.4, §7 |
| 4 | Claim breadth 2 of 3 models; all three receive the preregistered validity assessment and are reported (RC-13); the error control of the 2-of-3 rule stated exactly: an exact event-counting argument conditional on valid bounds, with a nominal implemented FWER (RC-9) | §6.3 (Lemma FW), §6.5 |
| 5 | The 3-harmonic code primary; C1's first-harmonic plane reported; the C1′ chart phase (production charts by sha256) primary; the oracle x-phase a pre-registered secondary with its own licence | §2.4, §2.11, §3.3, §5.6 |
| 6 | Euclidean-complement projector and K = 1, 2 are pre-registered qualifiers, not decision inputs | §2.5, §6.6 |
| 7 | X's adversarial fixtures (leakage; circle in the head kernel) and the per-reason coverage tally | §5.5, §13.3 |
| 8 | "Computationally inert" restricted to "not used by the position-32 readout beyond the bound", further restricted to the registered code and interchange (RC-2) | §3.1, §3.5 |
| 9 | Last symbol fixed by design; separating w31 from longer history is the named next extension | §1.5, §13.2 field 6 |
| 10 | 1e-9 guard band and Decimal reference rows instead of the full certificate; no new training; `tools/c2_readout/`; measure-only; MERGE forecast ≈ 1.5–2.5 CPU-h, recounted in v2 to a provisional central ≈ 2.0 CPU-h, range ≈ 0.9–4.5 (RC-15), and in v3 to central ≈ 2.1, range ≈ 0.9–4.8 (the revised GLS-REF machinery, NEW-1; the C2-M descriptive stream, NEW-5) | §9, §12, §13 |
| 11 | Writer → Codex review → revision → confirmation review → revision round 3 (this document) → confirmation → freeze; owner AUTH before any run | Header, §7 row 0, §14, §18, §20 |
| Owner Q1–Q4 | Addendum 20 | Q1 §2.6/§2.11; Q2 §2.9; Q3 §2.10; Q4 §6.3, §6.5 (reading confirmed by owner addendum 21, §18) |

---

## Summary (≤ 300 words)

**Question.** In the three trained cylinder-O models (1729, 2718, 3141; step 5000), does the next-symbol prediction depend on history *through* the learned circle code at the final position?

**Key fact.** After the final LayerNorm the head is exactly linear (`unembed` has no bias). Setting coordinates of the normalised state at position 32 changes the logits by a closed form from natural activations; gate X1 measures its agreement with the network's own `forward_with_patch` path.

**Design (C2-R, primary).** Exact-symmetry donors H± (positions 1–31 shifted ±2 cells, w32 kept) give natural counterfactual pairs. The circle code is the 6-d span of the within-symbol regression of the readout coordinates on harmonics 1–3 of the reused C1′ chart phase, made nuisance-excluding by a GLS projector. ψ = E[A_S]/E[A_full] is the share of the model's signed oracle-aligned response carried by the registered code interchange.

**Outcomes.** USED (LB > 0.50); NOT_USED (UB < 0.10 **and** energy share below min(0.10, (127/60)× the exact random-6-plane energy): a low signed share, opposition included, with a bounded mean-square effect); LOW_ALIGNED_SHARE; PARTIAL; CIRCLE_NOT_HISTORY_SENSITIVE; MIXED; INCONCLUSIVE. *"These outcomes concern the frozen, nuisance-excluding linear code defined by this fit and projector. They do not exclude predictive use of phase information in excluded directions, higher harmonics, interactions, or other encodings."* Claims need 2 of 3 models; all three are assessed and reported; failed validity gates can leave endpoints NOT_RUN. Lemma FW is an exact event count (≤ 12α = 0.05 given valid bounds); the implemented error rate is nominal.

**Controls.** V3 (θ_full > 0.30), a one-row y-translation placebo (a linear inequality), exact random references, readout-null and operator decompositions, projector and harmonic qualifiers.

**Secondaries.** C2-M at `resid_post_2`/32 (restricted ROUTED_AROUND); C2-S*; a report-only rotation arm.

**Cost.** No training. Provisional central ≈ 2.1 CPU-h (k = 2), range ≈ 0.9–4.8, measure-only.

---

## 0. Notation and conventions

| Symbol | Meaning |
|---|---|
| j | Model seed, j ∈ J = {1729, 2718, 3141} (cylinder-O, step 5000; checkpoint IDs `c3358e3cb9c352fb`, `98b0e703a337d513`, `036b670743ffbbaf`; EmissionSpecs `3633ac27dab50cf4`, `97838b9e13a26f74`, `8c29c329c197c79e`; WorldSpec `21feee1d8ee5422e`, TransitionSpec `e4dafc7b9785c172`; C1′ CONTRACT `artifacts.per_model`; float32 `state_sha` §4) |
| H = (w1..w32) | A history (canonical symbols c = 6a + b, a = x-column, b = y-row); model input [BOS = 36, named(w1..w32)] (`c1_model.model_inputs`); position 32 predicts w33 |
| perm | The model's symbol map: canonical symbol c ↔ named symbol perm[c] (§2.3) |
| τ_k, H^k | x-donor: τ_k(6a + b) = 6((a + k) mod 6) + b, H^k = (τ_k(w1..w31), w32), k = ±1; arms H⁺ = H^{+1}, H⁻ = H^{−1} (`c1_oracle.donors`) |
| υ_k, k_Y, H^Y, Y_def | y-donor (§2.2): υ_k(6a + b) = 6a + (b + k), k = ±1, defined iff 0 ≤ b + k ≤ 5; k_Y(H) = +1 if ȳ(b31(H)) < 5.5, else −1; H^Y = (υ_{k_Y(H)}(w1..w31), w32), defined iff Y_def(H) = 1 (no shifted prefix symbol leaves rows 0..5; never clamped or wrapped) |
| b31, b32, q | Oracle filtering posteriors after 31 and 32 symbols and the predictive of w33 (`BayesFilter.run`: `b[:,30]`, `b[:,31]`, `q[:,32]`) |
| q̄ | q/Σ_v q(v) (normalised; §2.3) |
| d, G | d = q̄¹ − q̄² (canonical; d_named in the model's order, §2.3); G = ½ Σ_v d_v (log q̄¹_v − log q̄²_v) ≥ 0, for an arm pair (1, 2); x pair (H⁺, H⁻), y pair (H, H^Y) |
| a, a₂ | Float64 `resid_post_3`[:, 32] and `resid_post_2`[:, 32] |
| u, γ, β, W_U | `ln_final_out`[:, 32]; ln_final weight and bias; `unembed.weight` (36 × 128) |
| Q₀, y, M | Readout basis (128 × 127), readout coordinates y = Q₀ᵀ(u − β) ∈ ℝ¹²⁷, M = W_U Q₀ (36 × 127, named output order) (§2.1) |
| C | Centring matrix I₃₆ − 11ᵀ/36 |
| J | Euclidean orthogonal projector onto ker(CM) ⊂ ℝ¹²⁷ (readout-null coordinates; §2.12) |
| φ | Gauged C1′ chart phase of a (§2.4); f(φ) = (cos kφ, sin kφ)_{k=1..K} |
| φ*, m_valid, f*_K | Oracle x-phase arg m32; its validity mask m_valid(H) = 1[‖m32(H)‖ > 1e-12]; the masked harmonics f*_K = m_valid·(cos kφ*, sin kφ*)_{k=1..K} (§2.11; NEW-3) |
| B, Γ, α_w, Σ_ε | FWL coefficients (127 × 2K, 127 × 5, class means) and Ledoit–Wolf residual covariance (§2.4) |
| X_n, X̃ | [Γ, B] ∈ ℝ^{127×(5+2K)} and its whitened form R_Σ^{−ᵀ}X_n, Σ̂_ε = R_ΣᵀR_Σ (§2.5) |
| L, L_B, L_Γ, P_S, P_Γ | GLS operator and projectors (§2.5) |
| A_full, A_S, A_Γ, A_rest | Readout decomposition (§2.6); A_S = A_S^vis + A_S^null (operator decomposition, §2.12) |
| e_full, e_S, r | Logit-change energies and the exact random-6-plane energy reference (§2.8–§2.9) |
| D0, D_code, D_lin; SSE_0, SSE_code, SSE_lin | L1 decoders and their FEAS sums of squared errors (§6.6) |
| e_Y, e_L, ρ_ref, ε*_P, δ_P | GLS-REF composed residual bounds on the first solve and on the operator (Lemma GR), the accepted relative bound e_L/‖L*‖_F, the projector reference uncertainty and the projector guard input (§2.5, §9.2; NEW-1) |
| E_x, E_y | Oracle eligibility of a row for the x pair and the y pair (§5.4); 1_E its indicator |
| FIT, FEAS, VAL, TEST | The four splits (§5.1) |
| L(·), U(·) | One-sided lower and upper percentile-bootstrap bounds of a mean (§6.2) |
| Q-CODE | The mandatory scope clause of every family licence (§3, RC-2) |
| u_m | Unit roundoff 2⁻⁵³ ≈ 1.11e-16 |

Conventions: every inequality is strict exactly as written; equality fails a criterion; `inverted_cdf` quantiles with run-time rank checks (`c1_means.quantile_with_rank`); exact rationals for thresholds that are fractions; float64 everywhere, single thread.

---

## 1. Question, competing explanations, scope

### 1.1 Question
For each model j and for natural counterfactual histories that differ in the x-history with the last symbol kept, what fraction of the model's own signed oracle-aligned change in next-symbol prediction is carried by an interchange of the model's registered circular code at the final position? Is it large, low with a bounded effect in every direction, or intermediate? Secondary: does an interchange of the registered layer-2 code at the final position change the output after the remaining computation (C2-M)?

**Operational scope (RC-2).** The endpoint measures the effect of one frozen projector: the frozen, nuisance-excluding linear code defined by the FIT regression and the GLS projector. A representation can contain excellent first-harmonic phase information in that code while the head reads higher harmonics, phase–shape interactions, class-dependent phase encodings, or phase-associated information assigned to the excluded nuisance directions. C2 therefore answers the question for the registered code interchange, not for "every encoding of circular information"; every licence carries the Q-CODE clause (§3). This scope is confirmed by owner addendum 21 (§18 item 1).

### 1.2 What C1′ showed and what changes (L§1; CMP §3.1)
- **C1′ outcome** (jobs/0044, owner addendum 10): INCONCLUSIVE/FAMILY_UNMATCHED at M2-cal in all three models. The forced state T = a + B[f(φ±) − f(φ)] flipped the decoded w32 on 29–39% of arms (D_w(T) = 0.3111, 0.3891, 0.2861) and moved the decoded y-marginal by 2.5–3.2 × tr Cov(ν). The equal-whitened-norm Haar controls left ŵ unchanged (D_w(C̄) ≤ 0.00075) but still exceeded the D_y ceiling (0.0808–0.1009). The M1 identities were exact, so the gap is a property of the fitted B-plane's *direction*.
- **Two structural lessons.** (i) Controls matched in the instrument but not in the variable cannot match in damage; controls must hold the instrument fixed and vary the variable. (ii) A decoder's response is not the information.
- **The change.** At `resid_post_3`/32 the only downstream operations are `ln_final` and the bias-free `unembed` (model.py 92–93, 123–126). After LayerNorm the map to the logits is exactly linear. Attribution of a natural response to any set of normalised coordinates is therefore exact, needs no synthetic state evaluated through a nonlinearity, and needs no decoder gates. This removes C1′'s damage/control failure at its root instead of loosening thresholds. It does not make the registered code the unique carrier of circle information (§1.1).

### 1.3 Competing explanations and the observations that separate them

| Explanation | Discriminating observation | What it cannot separate (RC-2, RC-4–RC-8) |
|---|---|---|
| E-read: the registered code interchange carries the readout's aligned response | ψ > 0.5 (USED); Y1's linear inequality holds | other carriers of the same information (redundancy is not tested) |
| E-epi: the registered code is readout-epiphenomenal (in readout-null directions, or read orthogonally to the oracle difference) | ψ < 0.10 and energy share below the bound (NOT_USED); ν_S and the operator decomposition descriptive; R1 passes (the code does move) | predictive use of phase in excluded directions, higher harmonics, interactions or other encodings (Q-CODE) |
| E-orth/E-cancel: the code moves the logits strongly, but orthogonally to d or with opposite-sign per-row effects | ψ small but energy share large → LOW_ALIGNED_SHARE, never NOT_USED (§2.9); E\|A_S\| reported | — |
| E-oppose: the code opposes the aligned response with a small mean-square effect | NOT_USED is still declared (the rule includes negative contributions); NEGATIVE_ALIGNED_CONTRIBUTION qualifier when certified (§2.9, RC-4) | its magnitude relative to the response (ψ may be −1 with an energy share ≈ 1e-4) |
| E-share: the code carries part, other directions the rest | 0.10 < ψ < 0.50 (PARTIAL); ψ_Γ, ψ_rest reported | — |
| E-nuis: the code also carries readout-relevant y-information | Y1 fails (the registered linear inequality fails) → model excluded | a passing Y1 does not establish general nuisance exclusion, small placebo magnitude, or absence of a subspace illusion (RC-7) |
| E-proj/E-harm: the share is an artefact of the complement metric or of the harmonic content | PROJECTOR_DEPENDENT and HARMONIC_DEPENDENT qualifiers (Euclidean complement; K = 1, 2) | — |
| E-reg: the registered first-harmonic code phase does not register the prefix change | R1 fails after L1 passes → CIRCLE_NOT_HISTORY_SENSITIVE (an assay-registration finding, RC-8) | absence of history in the representation |
| E-sym: the circle's role is the last symbol's | Closed by design: w32 identical in both arms; the analysis is within symbol class | — |
| E-image / E-code: the circle is only the shape of the prediction, or an upstream representation used downstream | C2-M: UPSTREAM_USED means the layer-2 code interchange changes the final output after the remaining computation, including the residual skip | active block-3 processing versus bypass through the skip; ROUTED_AROUND licenses no inference to E-image (RC-5, RC-6) |
| E-short: the within-symbol phase mostly reflects w31 | **Not separated** (w31 changes in both donor pairs); stated limit, next extension (MD 9) | — |
| E-artifact: a pipeline, index, symbol-order or LayerNorm-coordinate defect | M0, SYMBOL-ORDER at H1/H2/H3/M0 (RC-1, NEW-2), X1 (measured identity on the stated rows), GLS-REF, H3 | — |

### 1.4 Prior expectation (stated in advance; CMP §4 "both missed")
x and y nearly decouple in this process (E factorises exactly, §2.2; P(x ± 1) = 0.2 for every state), so the x-pair response is essentially an x-belief response, and the circle code is by construction the x-phase covariation. **USED at the final site is the expected outcome [H].** The informative results are: a NOT_USED surprise; the y placebo; the split ψ_S/ψ_Γ/ψ_rest and the operator decomposition; and C2-M, which tests whether a layer-2 code interchange transmits to the output (without separating block-3 processing from the residual skip). A USED result is reported as confirming the expectation, not as a discovery.

### 1.5 Scope
- Three frozen models; no training, no site search, no checkpoint choice.
- Sites fixed in advance: the circle variable at `resid_post_3`/32; attribution at `ln_final_out`/32 (C2-R, C2-S*, rotation arm); the upstream interchange at `resid_post_2`/32 (C2-M).
- Population: natural cylinder-O histories (overlap emission, σ = 1.25), conditional on oracle eligibility; the last symbol held fixed by design (MD 9). Separating w31 from longer history is not in C2.
- Object: the frozen, nuisance-excluding linear code defined by the FIT fit and the projector (Q-CODE).
- No frozen result is reopened (C1′, X4-F, E4, K4, K4b, X6). C2 is a new protocol, not a rescue of C1′.

---

## 2. Estimands and exact derivations

### 2.1 Readout coordinates and the exact readout (Lemma R)
**Code facts at 967605c.** `TransformerLM.forward`: `normed = ln_final(x)`, `logits = unembed(normed)`, `unembed = nn.Linear(128, 36, bias=False)`, `ln_final = nn.LayerNorm(128)` (ε = 1e-5, affine γ, β); embedding tying is rejected by `_validate`. `forward_with_patch(site="ln_final_out")` runs the full forward, replaces `normed[:, index]` and applies `unembed` with no second LayerNorm (patch.py 111–117). The affine LayerNorm bias contributes the fixed term W_Uβ.

**Construction.** N₁ ∈ ℝ^{128×127} is the Helmert orthonormal basis of 1^⊥ (column k ∝ (1, …, 1, −k, 0, …, 0)/√(k(k+1)), k = 1..127). Q₀ = qr_pos(diag(γ)N₁) (`c1_fit.qr_pos`, positive-diagonal R). y = Q₀ᵀ(u − β); M = W_U Q₀ (rows in the model's named output order).

**Lemma R (exact readout).** If diag(γ)N₁ has full column rank 127, then for every LayerNorm output u: (i) u − β ∈ U₀ := col(Q₀) = {γ ⊙ v : v ⊥ 1}; (ii) u = β + Q₀y; (iii) the logits are z = W_Uβ + M y; (iv) for any ŷ ∈ ℝ¹²⁷, `forward_with_patch(model, inputs, "ln_final_out", 32, β + Q₀ŷ)` returns z(ŷ) = W_Uβ + Mŷ at position 32, independently of `inputs`.

*Proof.* u = γ ⊙ x̂ + β with x̂ = (a − ā1)/√(var(a) + ε), and Σ_k x̂_k = 0, so u − β = γ ⊙ x̂ ∈ U₀; dim U₀ = rank(diag(γ)N₁) = 127, and col(Q₀) = col(diag(γ)N₁) = U₀. Since Q₀ has orthonormal columns spanning U₀, Q₀Q₀ᵀ(u − β) = u − β, which is (ii). (iii) is unembed applied to (ii). (iv): the patched call sets normed[:, 32] = β + Q₀ŷ and applies the same bias-free linear map. ∎

Remarks. (a) Rank 127 holds iff at most one γ_k is 0 (two zeros put e_k − e_l in the kernel); gate M0 checks the computed rank directly. (b) y-coordinates are used instead of u because u − β lies in a 127-dimensional subspace, so a covariance of u is structurally singular. Using 127 coordinates removes that structural singularity only; it does not by itself guarantee a nonsingular empirical covariance, which the F1 Ledoit–Wolf eigen-ratio and rank gates check (RC-16). (c) **LayerNorm and scale (corrected, RC-16).** LayerNorm subtracts the mean along 1 exactly. With ε = 1e-5 > 0 it does **not** remove scale exactly: for a centred vector v, scaling by c gives cv/√(c²Var(v) + ε), which still depends on c. Neither fact changes the ambient space: x̂ ⊥ 1 for every input whatever ε is, so u − β ∈ U₀ and the 127-dimensional linear readout space of Lemma R is exact. (d) **Wording (CMP L4).** C2-R evaluates no synthetic state through any nonlinearity. A patched normalised vector β + Q₀ŷ need not lie on the LayerNorm image (its norm can differ from that of any γ ⊙ x̂ + β); this is harmless because only the linear head reads it. The per-row ratio ‖ŷ‖/‖y‖ is reported.

### 2.2 Counterfactual pairs and exactly what they preserve
**Process facts** (L§4.1; C1 §3): WorldSpec 12 × 12 cylinder, x periodic, y non-periodic; max-degree lazy walk with p_stay 0.2, uniform π; overlap emission E[z, j] = softmax_j(−d(z, c_j)²/2σ²), σ = 1.25, centres c_{ab} = (0.5 + 2a, 0.5 + 2b), periodic dx. Because d² = dx² + dy², E(z, (a, b)) = E_x(x, a)·E_y(y, b) exactly.

**y-translation donor (D-0104-1; owner addendum 23).** The y-row b of a canonical symbol c = 6a + b indexes the emission centre 0.5 + 2b, so one symbol row is 2 cells. For k ∈ {+1, −1}, υ_k(6a + b) := 6a + (b + k), defined iff 0 ≤ b + k ≤ 5; the x-column a is kept. The shift points toward the interior: k_Y(H) := +1 if ȳ(b31(H)) < 5.5 and −1 otherwise, where ȳ(b) := Σ_z b(z)·y(z) is the posterior mean of the cell row y(z) ∈ {0, …, 11} under the natural history's oracle filter after 31 symbols. The donor is H^Y := (υ_{k_Y(H)}(w1..w31), w32), with w32 kept.

**Ineligibility (no clamp, no wrap).** H^Y is defined iff every shifted prefix symbol stays in rows 0..5: Y_def(H) := 1[0 ≤ b(w_t) + k_Y(H) ≤ 5 for every t ≤ 31]. A row with Y_def(H) = 0 is ineligible for the y placebo (reason OFF_GRID_Y, §5.5). It stays in its split, is counted in the coverage tally and in the denominator of f_y, and no H^Y token array, digest, oracle run or forward is formed for it. A shifted symbol is never clamped to row 0 or 5 and never wrapped. The construction is exactly that of the job 0104 feasibility check (`topo-scratch/0104/fy_alt.py`, sha256 `0e1113ede9939f87895ffa80b51c37c29bc7b4ca9e3dbf35b5b95583327763aa`: b = w mod 6 and a = w div 6 on w1..w31, the sign from ȳ(b31(H)) < 5.5, w32 kept, rows with an off-grid shifted symbol counted as ineligible).

**No closed-form symmetry.** τ is an exact symmetry of the cylinder in x. A y-translation is not a symmetry of the process: y is non-periodic, the boundary rows keep their own self-transition mass, and the emission softmax over the six rows is normalised differently near the boundary. So the y pair has no index map, no closed form for b31(H^Y) or b32(H^Y), and no ε_sym bound. Its oracle quantities are the exact oracle forward (`BayesFilter.run` on the H^Y tokens). Gate H3 checks them against the Decimal reference rows (§7 row 6).

| Quantity | x pair (H⁺, H⁻) | y pair (H, H^Y) |
|---|---|---|
| Last symbol w32 | identical (exact) | identical (exact) |
| Prefix likelihood p(w1..w31) | identical in exact symmetry; stored-weight deviation ≤ 31ε_sym (C1 §4) | not preserved: H^Y is not the image of H under a symmetry; no ε_sym bound applies; finite log-evidence is required (§5.4) |
| y-evidence (b indices) of w1..w31 | identical | shifted by k_Y(H) symbol rows (2 cells) toward the interior (the placebo's variable) |
| x-evidence (a indices) of w1..w31 | rotated by ±1 column (H⁺ and H⁻ are 2 columns = 4 cells apart) | identical |
| b31 | ρ_{±1} b31(H) | no closed form: the exact oracle forward on the H^Y tokens; its mean y moves toward the interior (mean 2.13 cells on Y_def rows [W, job 0104 in-memory check]) |
| b32 | (ρ_k b31 T) ⊙ E[:, w32], not a rotation of b32 | no closed form: the exact oracle forward on the H^Y tokens |
| y-marginal of b32 | changes only through the one-move-per-step coupling; κ_ν = 0.009319 in C1′ [W, 0041] | changes |
| x-belief of b32 (m32) | changes (the variable) | changes only through the coupling and the boundary (the measured x leakage, a known property, below); κ_m measured at S1 |
| w31 | changes | changes |
| Naturalness | each arm is a real history; eligibility bounds the w32 surprisal (§5.4); f_val 0.98584 in C1′ [W, 0041] | each defined arm is a real token sequence; the same surprisal rule, plus Y_def (§5.4); f_y = 0.89270 for this construction [W, job 0104 in-memory check] |

**Not preserved, stated:** the x-history (the variable), w31 (E-short), and the prefix–w32 consistency, which changes the shape of the x-belief (concentration, bimodality). The shape part is a measured nuisance: entropy and second-harmonic modulus enter Γ, so it goes to A_Γ, not to A_S (§2.4). Any phase-associated predictive contribution assigned to Γ is thereby excluded from A_S (Q-CODE).

**Known property of the y pair: x leakage (measured before any C2 data; reported descriptively).** The job 0104 in-memory check used the real process from the `src` builders and 8,192 rows on scratch seed 999002, outside the `c2-v1` namespace, with nothing persisted (`fy_alt.txt`, sha256 `a56ced392970625f8fb733e98e51c27ab030d37585a02abcd5ce5d448585930a`). On the Y_def rows, the mean ‖m32(b31(H^Y)) − m32(b31(H))‖ was 0.0035, against 1.5915 for the x pair's mean ‖m32(b31(H⁺)) − m32(b31(H⁻))‖. That is **about 0.2% of the x contrast** [W]. At b32 the y pair's mean was 0.0161. The leakage comes from the one-move-per-step coupling of x and y and from the boundary. It is a known property of the placebo, not a gate. It is reported descriptively (§2.12), and κ_m (§2.3) remains the registered activity condition of Y1, Y1* and Y2.

### 2.3 Oracle quantities and symbol order
- `BayesFilter(T, E_canon, π).run` is the operational oracle (C1 §3.3; `c1_oracle.run_oracle`). One canonical oracle per row, shared by the three models (gate H1: E_canon bitwise identical across models).
- **Normalised predictive.** q̄ = q/Σ_v q(v). Then Σ_v d_v = 0 up to rounding, so the logit-difference and log-softmax forms of every A agree (Lemma D2). The difference between C1's unnormalised G and this G is below 1e-14 nat [W, C1 §1.2 bound].
- d and G for both pairs, the y-marginal ν (`y_marginal`), m32 (`m32`), the nuisance covariates (§2.4), κ_ν (`kappa_nu`), surprisals and eligibility (`s_max`, `eligible`) come from `c1_oracle` unchanged.
- **Symbol order (RC-1; one convention).** The oracle works in canonical order; the model's input tokens and output logits are in its named order, canonical symbol c ↔ named symbol perm[c]. `c1_oracle.named_from_canonical` scatters canonical column c into named column perm[c]; `c1_oracle.canonical_from_named_cols` gathers named columns back into canonical order (the opposite conversion; code at 967605c, `c1_oracle.py` 146–155). **M stays in the model's named output order, and**

  `d_named = c1_oracle.named_from_canonical(d_canonical, perm)`,

  likewise d^Y_named and d_rot,named; every A in §2.6–§2.11 is ½ d_namedᵀ(·). `canonical_from_named_cols` is used only in two SYMBOL-ORDER checks: the contrast round trip (c) at H3 and the independent route of the M0 two-route comparison (named logits gathered into canonical order and dotted with canonical d) (§7; NEW-2). An involutive permutation would conceal a direction error, so the independent fixture uses a non-involutive permutation (§13.3 T-ORDER).
- **κ_m** = mean_{E_y, FIT} ‖m32(H) − m32(H^Y)‖² / tr Cov_FIT(m32) (population covariance over all FIT rows). Frozen at S1. **Y1, Y1* and Y2 are active iff κ_m < 0.01** (and V3y, §6.6). Otherwise they are report-only and every USED/PARTIAL licence carries SPECIFICITY_NOT_ESTABLISHED. This is decided from oracle quantities before any model work.

### 2.4 The circle variable and the circle code
**Circle variable (MD 5).** φ(H) = `c1_chart.extend_phase(prod_j, gauge_j, a(H), cfg).phase`, the gauged phase from the three **C1′ production charts reused by sha256**:

| Chart | sha256 (jobs/0044 report, R14 table) |
|---|---|
| CHART_1729_production.npz | `6154af0ee1a5ad01d378b507272365d1f0e797b4a843835d7dc09525d5c9cc71` |
| CHART_2718_production.npz | `6a5d8c1cbe4aea9909b85aff258a31d2dfdfb8d12c1f93f33a79b245d69370da` |
| CHART_3141_production.npz | `ce0c0192d243ff9e8fa4ddc6b07750db31a637ff059a4e8cc55535b8dd21cf2d` |

Each NPZ carries its serialised gauge (`chart.chart_from_arrays` returns (Chart, Gauge)). The charts passed the C1′ rule (|C*| = 512, one component, `centered_exact` lift, primitive g = 1, smoothing residual ≤ 2.72e-12, gauge alignment 0.89425/0.89908/0.89728; jobs/0044). C0-val was never run in C1′, so C2 runs it (gate C0v). Reusing a deterministic artifact is not a rescue of C1′: no C1′ endpoint was computed. The 512 landmarks are C1′ cal-b0 rows (in `HIST_cal_b0.npz`, sha256 `d80ad5f42e333b4dc910667c0465cf03adc66518a22e961dec50a8eca2d5ba5e`, jobs/0041); they enter the registry and never become C2 data. Chart kernel parameters are the C1′ CONTRACT's (`extension_k` 8, `support_min_resultant` 0.2, `fidelity_min_agreement` 0.8, `phase_bins` 12, `phase_bin_min_rows` 8, `overall_resultant_max` 0.3), bound by `c1_config.chart_cfg` at CONTRACT sha256 `f8df2e43bc24a3e992ce4323a8577ec4a7e2657a4e00bdf3ff0323b909a7a379`.

**FWL fit (FIT only, all 8192 natural rows H, OLS by `numpy.linalg.lstsq`).**

  y_i = α_{w32(i)} + Γ z̃_i + B f(φ_i) + ε_i.

- **Harmonics, K = 3 (primary):** f(φ) = (cos φ, sin φ, cos 2φ, sin 2φ, cos 3φ, sin 3φ), B ∈ ℝ^{127×6}. Within a class, harmonic k varies as k·δφ·(−sin kφ_w, cos kφ_w); with K = 3 the six coefficient columns let each of the 6 x-columns have its own within-class circle tangent. K = 1 (C1's single rigid plane, the construction C1′ found crossing class boundaries) and K = 2 are pre-registered qualifier variants with their own fits.
- **Nuisance covariates z̃ (5),** oracle-computed from b32 of the row's own history and standardised by `c1_fit.standardise_nuisance` (FIT mean and population SD; scale 1 for a constant column): ȳ, Var y, ‖m32‖ (`c1_oracle.nuisance`); Shannon entropy H(b32); the second x-harmonic modulus |Σ_z b32(z) exp(2i·2πx(z)/12)|.
- **Design (RC-12):** 36 class indicators + 5 covariates + 2K harmonic columns = **36 + 5 + 2K columns: 43, 45 and 47 for K = 1, 2, 3.** F1 requires the `lstsq` rank to equal 36 + 5 + 2K for each fitted K. **No column is ever dropped for rank** (X§5 "rank truncation is not a licence to drop a constraint"): a deficient rank → INCONCLUSIVE/PATCH_MODEL_DEGENERATE for that fit. Separately, the GLS operator needs the nuisance-plus-code block [Γ, B] at full column rank **5 + 2K** (7, 9, 11), checked on the whitened design X̃ (§2.5).
- **Σ_ε** = `x4f_scores.ledoit_wolf`(ε̂_FIT) (127 × 127).
- Reported: within-class partial R² of f(φ), per K.

### 2.5 The GLS projector and its nuisance exclusion (Lemmas G1–G3)
Let X_n = [Γ, B] ∈ ℝ^{127×(5+2K)} (11 columns at K = 3), W = Σ_ε⁻¹, 𝒢 = X_nᵀ W X_n, L = 𝒢⁻¹X_nᵀW ∈ ℝ^{(5+2K)×127}; L_Γ = rows 1–5, L_B = rows 6–(5+2K). P = X_n L, **P_S = B L_B**, **P_Γ = Γ L_Γ**, P_rest = I − P_S − P_Γ.

**Whitened design (RC-10, RC-12).** With the Cholesky factor Σ̂_ε = R_ΣᵀR_Σ, X̃ := R_Σ^{−ᵀ}X_n, so 𝒢 = X̃ᵀX̃ and κ(𝒢) = cond₂(X̃)². F1 requires (i) numerical rank(X̃) = 5 + 2K (SVD, `numpy.linalg.matrix_rank` default tolerance σ_max·max(127, 5 + 2K)·eps), and (ii) cond₂(X̃) ≤ 1e8 (the same degeneracy limit as the FWL design). Failure → EXCLUDED_j/PATCH_MODEL_DEGENERATE (primary projector) or the qualifier NOT_COMPUTED (variant). The conditioning of the FWL design and the rank of B do not bound the conditioning of [Γ, B]; this check does.

**Lemma G1 (identities).** L X_n = I_{5+2K}; hence L_B B = I_{2K}, L_B Γ = 0, L_Γ Γ = I₅, L_Γ B = 0; P_S² = P_S, P_Γ² = P_Γ, P_S P_Γ = P_Γ P_S = 0, P_S + P_Γ = P, P² = P; P_S Γ = 0, P_Γ B = 0; P is W-self-adjoint (WP = PᵀW), equivalently the whitened P̃ := R_Σ^{−ᵀ}PR_Σᵀ is symmetric.
*Proof.* L X_n = 𝒢⁻¹𝒢 = I. The block identities are its blocks. P_S² = B(L_B B)L_B = P_S; P_S P_Γ = B(L_B Γ)L_Γ = 0; P_Γ P_S = Γ(L_Γ B)L_B = 0; P_SΓ = B(L_BΓ) = 0. WP = W X_n𝒢⁻¹X_nᵀW is symmetric. With Σ̂_ε = R_ΣᵀR_Σ, W = R_Σ⁻¹R_Σ^{−ᵀ} and X̃ = R_Σ^{−ᵀ}X_n: P̃ = R_Σ^{−ᵀ}X_n𝒢⁻¹X_nᵀR_Σ⁻¹R_Σ^{−ᵀ}R_Σᵀ = X̃𝒢⁻¹X̃ᵀ, the Euclidean orthogonal projector onto col(X̃), and WP − PᵀW = R_Σ⁻¹(P̃ − P̃ᵀ)R_Σ^{−ᵀ}. ∎

**G1 identity check (F1; scale-invariant form; D-0104-2).** F1 checks Lemma G1 on the production (QR-based) L̂ and P̂ of **every** projector problem: the primary R, M and S* problems, and the R variants (Euclidean: R_Σ := I; K = 1, 2). ‖·‖_max is the largest absolute entry.
- *Dimensionless identities, absolute 1e-10:* ‖L̂X_n − I_{5+2K}‖_max (its blocks are L_B B = I_{2K}, L_B Γ = 0, L_Γ Γ = I₅ and L_Γ B = 0), and ‖P̂_S² − P̂_S‖_max, ‖P̂_Γ² − P̂_Γ‖_max, ‖P̂_SP̂_Γ‖_max, ‖P̂_ΓP̂_S‖_max, ‖P̂_S + P̂_Γ − P̂‖_max and ‖P̂² − P̂‖_max, each ≤ 1e-10.
- *Relative bounds for the two products that carry the units of Γ and B:* ‖P̂_SΓ‖_max ≤ 1e-10·‖Γ‖_max and ‖P̂_ΓB‖_max ≤ 1e-10·‖B‖_max.
- *Self-adjointness, whitened:* ‖P̃ − P̃ᵀ‖_max ≤ 1e-10, with P̃ = R_Σ^{−ᵀ}P̂R_Σᵀ formed from the production P̂: a triangular solve with R_Σᵀ and a product with R_Σᵀ, never recomputed from X̃. With Ω := R_Σ^{−ᵀ}, the whitening map (ΩΣ̂_εΩᵀ = I), this is P̃ = ΩP̂Ω⁻¹. For the Euclidean variant the check is ‖P̂ − P̂ᵀ‖_max ≤ 1e-10.

Every checked quantity is unchanged under a common positive rescaling of the readout coordinates: y → cy gives Σ̂_ε → c²Σ̂_ε, R_Σ → cR_Σ, X_n → cX_n and L̂ → L̂/c, while P̂ is unchanged. The previous absolute check of WP − PᵀW was scale-dependent. In spectral norm, ‖WP − PᵀW‖₂ ≤ λ_min(Σ̂_ε)⁻¹‖P̃ − P̃ᵀ‖₂, so a small covariance scale can amplify rounding residuals and cause an otherwise equivalent problem to fail that absolute check. There is no universal λ_min threshold implying unattainability. The job 0104 synthetic dry run observed a residual of 2e-9 at the M problem, motivating the whitened criterion. Failure of the revised check remains EXCLUDED_j/NUMERICAL for a primary projector or NOT_COMPUTED for a variant.

**Lemma G2 (nuisance exclusion and what the swap holds).** For any Δ ∈ ℝ¹²⁷ and any t ∈ ℝ⁵, P_S(Δ + Γt) = P_SΔ: displacements along the measured nuisance directions never enter the circle code. For the interchange y_S := y² + P_S(y¹ − y²): (i) L_B y_S = L_B y¹ (the code takes arm 1's value); (ii) (I − P_S) y_S = (I − P_S) y² (everything else, including the five nuisance coordinates L_Γ y and the complement P_rest y, keeps arm 2's value).
*Proof.* P_SΓ = 0 gives the first claim. (i) L_B y_S = L_B y² + (L_B B)L_B(y¹ − y²) = L_B y¹. (ii) (I − P_S)P_S = 0. Also L_Γ y_S = L_Γ y² + (L_Γ B)L_B Δ = L_Γ y². ∎
The operator preserves the stated GLS coordinates; it does not preserve arbitrary nuisance information (RC-2, review "verified foundations").

**Lemma G3 (within-state covariance under the within-class Gaussian model).** If y | (w, z̃, φ) ~ N(α_w + Γz̃ + Bf(φ), Σ_ε), then Cov(L y, P_rest y | w, z̃, φ) = 0, so the 5 + 2K GLS coordinates L y are independent of the complement P_rest y given (w, z̃, φ).
*Proof.* Cov(Lε, (I − P)ε) = LΣ_ε(I − P)ᵀ = 𝒢⁻¹X_nᵀ(I − Pᵀ) = 𝒢⁻¹(X_n − PX_n)ᵀ = 0 since PX_n = X_n. ∎

**What G3 does and does not say (CMP L2; RC-6).** **G3 concerns conditional within-state residual covariance. It provides no distribution-preservation guarantee for the paired interchange.** The two arms are deterministic paired transformations of one history, not independent draws, so an interchanged state (code from arm 1, nuisance coordinates and complement from arm 2) need not follow the natural law of any state. Counterexample (independent fixture, §13.3 T-N2): with s, t independent standard normals, source state (s, t) and donor state (t, s), both natural states have independent coordinates, but swapping the first coordinate gives (t, t), whose joint law differs. Also Cov(L_B ε, L_Γ ε) = [𝒢⁻¹]_{BΓ} ≠ 0 in general, and f(φ) and z̃ need not be independent. In C2-R this affects only interpretation, because the head is linear and Lemma D1 holds for any state. In C2-M, where block 3 evaluates the patched state, N2 is an operational **radial support screen** (§2.10), not a naturalness certificate.

**Variants (MD 6; qualifiers only).** (a) **Euclidean complement:** L^E = (X_nᵀX_n)⁻¹X_nᵀ, P^E_S = B L^E_B (Γ still excluded exactly; only the metric of the complement changes). Its F1 rank and conditioning checks apply to X_n itself (the whitened design for the identity metric); its Gram system X_nᵀX_n has condition number cond₂(X_n)², not κ(X̃)² (NEW-1). (b) **K = 1, 2:** the same GLS construction on the K-harmonic fits (designs of 43 and 45 columns; [Γ, B] of rank 7 and 9). C1's first-harmonic plane is the K = 1 variant (MD 5).

**GLS-REF (numerical reference; CMP L7; RC-10; composed residual bound, NEW-1).** At F1, per model and per projector problem (the primary R, M and S* fits and the three R variants; each problem yields both P_S and P_Γ), the reference targets are the exact projectors of the float64 inputs. *Local notation (this paragraph and §9.2 only):* A := Σ̂_ε (Euclidean variant: A := I), and X_n = [Γ̂, B̂]; both are exactly representable as `Decimal` (exact `Decimal(float)` conversion). The exact targets are Y = A⁻¹X_n, 𝒢 = X_nᵀY, L = 𝒢⁻¹Yᵀ, P_S = B̂L_B and P_Γ = Γ̂L_Γ. The reference is computed in `Decimal` at **p = 80 significant digits** (raised from v2's 50; see attainability below). The context uses ROUND_HALF_EVEN and traps Overflow, Underflow, Subnormal, DivisionByZero and InvalidOperation (a trap → reference not accepted):
1. Y* by Gaussian elimination with partial pivoting (Euclidean: Y* := X_n exactly);
2. 𝒢* = X_nᵀY*;
3. L* = 𝒢*⁻¹Y*ᵀ by elimination; P*_S = B̂L*_B, P*_Γ = Γ̂L*_Γ.

This compares the production result with a high-precision reference of the same problem, not two float solvers (the R13 lesson).

**v2's ε_ref = 16(κ_Σρ_Σ + κ_X̃²ρ_G) is withdrawn.** It does not bound the composed computation:
- 16 < 2√127 ≈ 22.54;
- an error in Y* perturbs both the Gram matrix and the right-hand side of the second solve;
- the rounding in forming 𝒢* was omitted;
- the Euclidean Gram system X_nᵀX_n is not conditioned as κ(X̃)²;
- the review's example shows that enlarging the constant does not repair it.

The replacement:
- **Residuals against the exact inputs:** R_A := AY* − X_n, R_C := 𝒢* − X_nᵀY*, R_G := 𝒢*L* − Y*ᵀ (Euclidean: R_A = 0).
- **Lemma GR (composed residual bound).** Suppose ω_A ≥ ‖A⁻¹‖₂ and ω_G ≥ ‖𝒢⁻¹‖₂ = ‖(X_nᵀA⁻¹X_n)⁻¹‖₂ (the review's a and h). Then

  ‖Y* − Y‖_F ≤ e_Y := ω_A‖R_A‖_F,  ‖L* − L‖_F ≤ e_L := ω_G[‖R_G‖_F + ‖R_C‖_F‖L*‖_F + e_Y(1 + ‖X_n‖_F‖L*‖_F)].

  *Proof.* Y* − Y = A⁻¹(AY* − X_n) = A⁻¹R_A, so ‖Y* − Y‖_F ≤ ‖A⁻¹‖₂‖R_A‖_F ≤ e_Y. Next, 𝒢 − 𝒢* = X_nᵀ(Y − Y*) − R_C, and 𝒢L = Yᵀ, so 𝒢(L* − L) = (𝒢 − 𝒢*)L* + 𝒢*L* − Yᵀ = −X_nᵀ(Y* − Y)L* − R_CL* + R_G + (Y* − Y)ᵀ. Multiply by 𝒢⁻¹ and use ‖UV‖_F ≤ ‖U‖₂‖V‖_F, ‖UVW‖_F ≤ ‖U‖_F‖V‖_F‖W‖_F and ‖·‖₂ ≤ ‖·‖_F. This gives ‖L* − L‖_F ≤ ‖𝒢⁻¹‖₂(‖X_n‖_F e_Y‖L*‖_F + ‖R_C‖_F‖L*‖_F + ‖R_G‖_F + e_Y) ≤ e_L. ∎ The bound is a posteriori and exact (nothing is truncated at first order). It holds for any Y*, 𝒢*, L*, however they were computed.
- **Lemma INV (verified inverse-norm bound).** Let 𝔐 be a square matrix and V any matrix of the same size. If θ ≥ ‖I − V𝔐‖₂ and θ < 1, then 𝔐 is nonsingular and ‖𝔐⁻¹‖₂ ≤ ‖V‖₂/(1 − θ). *Proof.* V𝔐 = I − E with ‖E‖₂ ≤ θ < 1, so V𝔐 is invertible (Neumann series) and ‖(V𝔐)⁻¹‖₂ ≤ 1/(1 − θ). Since 𝔐 is square, it is invertible and 𝔐⁻¹ = (V𝔐)⁻¹V. ∎
- **Verified ω_A and ω_G.**
  - *ω_A:* V_A := the float64 inverse of A (`numpy.linalg.inv`; exact in `Decimal`), and θ̄_A := a verified upper bound on ‖I − V_A A‖_F, which must be < 1. Then ω_A := ‖V_A‖_F/(1 − θ̄_A). (Euclidean: ω_A = 1, unused because R_A = 0.)
  - *ω_G:* V_G := the `Decimal` elimination inverse of 𝒢*. From the identity above, e_G := ‖X_n‖_F e_Y + ‖R_C‖_F ≥ ‖𝒢 − 𝒢*‖_F, so θ̄_G := ‖I − V_G𝒢*‖_F + ‖V_G‖_F e_G ≥ ‖I − V_G𝒢‖₂, which must be < 1. Then ω_G := ‖V_G‖_F/(1 − θ̄_G).
  - Uninflated float64 condition estimates are never used for ω_A or ω_G.
- **Arithmetic uncertainty: every norm entering a bound is a verified upper bound.** Python's `decimal` rounds every +, −, ×, ÷ and square root correctly at the context precision. Under the traps above, each operation therefore obeys fl(x ∘ y) = (x ∘ y)(1 + δ) with |δ| ≤ u_D := ½·10^{1−p} = 5·10⁻⁸⁰. Write ϑ_k := k·u_D/(1 − k·u_D).
  - (i) *Residual enclosures.* Take a residual of the form (fixed matrix) − (product with inner dimension q), computed as R̃. Entrywise, |R̃ − R| ≤ ϑ_{q+1}(|fixed| + |left factor|·|right factor|), by the standard dot-product error bound for any summation order. Hence ‖R‖_F ≤ ‖R̃‖_F + ϑ_{q+1}‖|fixed| + |left|·|right|‖_F. This applies to R_A (q = n), R_C (q = n), R_G (q = 5 + 2K), I − V_A A (q = n) and I − V_G𝒢* (q = 5 + 2K). A product without a fixed term (P*_S, P*_Γ) has the enclosure ϑ_q|left|·|right|.
  - (ii) *Inflation and deflation.* Every computed nonnegative quantity used as an upper bound is multiplied by (1 + 10⁻⁷⁰): each Frobenius norm, each enclosure term, each product or quotient of such quantities, and ‖P̂_S − P*_S‖_F. Every quantity used as a lower bound is multiplied by (1 − 10⁻⁷⁰): 1 − θ̄_A, 1 − θ̄_G, ‖L*‖_F in ρ_ref, and ‖P*_S‖_F, ‖P*_Γ‖_F in the gate. Each such quantity is formed from nonnegative terms, or by single rounded subtractions, through fewer than 10⁶ successive roundings, so its relative rounding error is below ϑ_{10⁶} < 10⁻⁷³.
- **Acceptance (fail-closed).** The reference is accepted iff:
  - no trap occurred;
  - θ̄_A < 1 (GLS problems) and θ̄_G < 1;
  - **ρ_ref := e_L/‖L*‖_F ≤ 1e-20**.

  Otherwise the result is EXCLUDED_j/NUMERICAL (primary projector) or NOT_COMPUTED (variant). A condition that cannot be verified counts as non-acceptance, never as a pass.
- **Projector reference uncertainty.** For P_S, ε*_P := ‖B̂‖_F·e_L + ϑ_{2K}‖|B̂|·|L*_B|‖_F; for P_Γ, ε*_{P_Γ} := ‖Γ̂‖_F·e_L + ϑ_5‖|Γ̂|·|L*_Γ|‖_F; both are inflated per (ii). They bound ‖P*_S − P_S‖_F and ‖P*_Γ − P_Γ‖_F. The first term holds because L*_B − L_B is a block of rows of L* − L, so ‖B̂(L*_B − L_B)‖_F ≤ ‖B̂‖_F e_L; the second term encloses the rounding of the product.
- **Gate.** ‖P̂_S − P*_S‖_F + ε*_P ≤ 1e-8·‖P*_S‖_F, with verified upper bounds on the left and the verified lower bound on the right; the same for P_Γ. By the triangle inequality, δ_P := ‖P̂_S − P*_S‖_F + ε*_P ≥ ‖P̂_S − P_S‖_F, the distance of the production projector from the exact projector of the float64 inputs. δ_P enters the NUM guard (§9.2).
- **Precision and attainability [H].** Write κ_Σ := λ_max/λ_min(Σ̂_ε) (the F1 Ledoit–Wolf ratio) and κ_X̃ := cond₂(X̃). The floor of ρ_ref is set by the residual enclosures:
  - e_Y ≈ ω_Aϑ_{n+1}‖|A||Y*| + |X_n|‖_F, with ω_A‖A‖₂ ≈ κ_Σ;
  - ω_G‖X_n‖‖Y*‖ ≲ κ_Σ^{1/2}κ_X̃²;
  - hence ρ_ref ≲ (n + 1)·u_D·c_dim·κ_Σ^{3/2}·κ_X̃², with c_dim ≤ 1e4 for the Frobenius and dimension factors.

  At the F1 admissibility limits (κ_Σ < 1e12, κ_X̃ ≤ 1e8), the heuristic expression above evaluates to approximately 6e-40 at p = 80, compared with approximately 6e-10 at p = 50. This motivates using 80 digits and suggests substantial precision headroom for the 1e-20 criterion. It does not guarantee reference acceptance for every F1-admissible design: the inverse-residual checks and the composed residual bound must still pass. Actual acceptance is determined solely by the fail-closed conditions above. At the conditioning expected in these fits, smaller reference uncertainties are anticipated [H; measured by the run]. For the Euclidean variant, the corresponding heuristic uses cond₂(X_n), whose admissibility limit is 1e8.

### 2.6 The ψ decomposition (Lemmas D1–D3)
For a pair (1, 2) of arms with natural readout coordinates y¹, y² and Δy = y¹ − y² (d = d_named throughout, §2.3):

  A_full = ½ dᵀ(z¹ − z²) = ½ dᵀMΔy,
  A_S = ½ dᵀM P_S Δy,  A_Γ = ½ dᵀM P_Γ Δy,  A_rest := A_full − A_S − A_Γ = ½ dᵀM P_rest Δy.

**Lemma D1 (partition and interventional meaning).** (i) A_S + A_Γ + A_rest = A_full exactly. (ii) A_S = ½ dᵀ(z(y_S^{2←1}) − z(y²)) = ½ dᵀ(z(y¹) − z(y_S^{1←2})), where y_S^{2←1} = y² + P_SΔy sets arm 2's circle code to arm 1's value with every other coordinate held fixed (Lemma G2), and y_S^{1←2} = y¹ − P_SΔy does the reverse. So A_S is the interventional effect of the registered code interchange, projected on the oracle direction. (iii) Neither the source history H nor α_w enters (w32 is shared, so α_w cancels in Δy).
*Proof.* (i) P_S + P_Γ + P_rest = I and linearity. (ii) Lemma R(iii): z(y² + P_SΔy) − z(y²) = MP_SΔy. ∎

**Lemma D2 (softmax invariance).** With Σ_v d_v = 0, ½dᵀ(log p¹ − log p²) = ½dᵀ(z¹ − z²), where p = softmax(z). Proof: log p = z − logsumexp(z)·1 and dᵀ1 = 0. ∎ Hence A_full is C1's crossed contrast (½⟨q̄⁺ − q̄⁻, log p⁺ − log p⁻⟩), equal to G for the oracle predictor itself.

**Lemma D3 (ratio reduction).** If E[A_full·1_E] > 0, then ψ := E[A_S 1_E]/E[A_full 1_E] > c ⇔ E[(A_S − cA_full)1_E] > 0, and the same holds conditional on E (divide by P(E) > 0). ∎

**Sign and magnitude (RC-4).** ψ is unrestricted in sign and magnitude: ψ < 0 means the code interchange opposes the model's aligned response; ψ > 1 means it overshoots it.

**Estimands (per model; population = natural histories conditional on E_x; conditional on the frozen chart, gauge and FIT fit):**
- **ψ_S,j = E[A_S | E_x]/E[A_full | E_x]** (primary);
- θ_full,j = E[A_full | E_x]/E[G | E_x] (positive control, V3);
- ψ_Γ, ψ_rest, θ_S = E[A_S]/E[G] (reported);
- y pair: the placebo inequality E[A^Y_S | E_y] < 0.10·E[A^Y_full | E_y] (Y1; a registered linear inequality, no population ratio claim, RC-7), with A^Y built from (H, H^Y) on the rows where H^Y is defined, d^Y = q̄(H) − q̄(H^Y) in named order.

### 2.7 The closed form and the network's patch path (gate X1; Lemma X)
**Lemma X (exact arithmetic).** For every row and arm, let z_net = natural logits at position 32 from `TransformerLM.forward` and z_fwp(ŷ) = logits at position 32 from `forward_with_patch(model64, inputs, "ln_final_out", 32, β + Q₀ŷ)`. In exact arithmetic z_net = W_Uβ + My and z_fwp(ŷ) = W_Uβ + Mŷ (Lemma R).

**Head-arithmetic estimate (partial; RC-10).** For a *given* placed vector u (natural, or β + Q₀ŷ), the float64 error of the head arithmetic alone is bounded per entry v by 4·128·u_m·S_v + O(u_m²), S_v := Σ_k |W_U,vk|·(|u_k| + |β_k|) + Σ_l (|W_U||Q₀|)_vl·|ŷ_l| [W, standard dot-product bounds: the `unembed` dot products, forming β + Q₀ŷ, the closed form W_Uβ, and M = W_UQ₀ with Mŷ]. This expression does **not** include the errors in constructing Q₀, in reconstructing the natural coordinates y = Q₀ᵀ(u − β), or in forming the interchange coordinates ŷ (projector products), so it does not bound the complete computation. It is used only to judge the attainability of τ_X1.

**Gate X1 (a directly measured implementation identity; VAL and TEST).** On every eligible row, for the natural arms and the primary interchange arms y_S^{2←1}, y_S^{1←2} of the x pair and the y pair: ‖z − ẑ_closed‖_∞ ≤ τ_X1 := 1e-9·max(1, ‖z‖_∞), fail-closed (any row over the tolerance → FAIL_TECHNICAL, study). For the S*, qualifier-variant and rotation arms, X1 runs on the 1024 lowest-sequence-id eligible rows per split. X1 is an *ephemeral integrity operation* (§5.7, RC-13): it may form the prescribed replacements and compare logits, retains only identity diagnostics (per-arm maximum deviations, the count and ids of rows over tolerance), and may not form, retain or release scientific endpoint arrays or summaries before the relevant admission gates pass.
**Preliminary attainability check (M0 on FIT, before any VAL data).** κ_X1 := max_{i,v} S_{iv}/max(1, ‖z_i‖_∞) over the 1024 lowest-id FIT rows (natural u, ŷ = y); require 4·128·u_m·κ_X1 ≤ 1e-10 (κ_X1 ≤ 1.76e3). Expected κ_X1 ≈ 10–100 [H]. This is a preliminary check on natural states, **not an all-interchange guarantee**: interchange states can be amplified (‖ŷ‖/‖y‖ is reported). A failure is INCONCLUSIVE/NUMERICAL at M0, and any tolerance change needs the owner (addendum 10).
**What X1 detects.** A defect in the replacement vector, site, index, β or Q₀ that moves the logits by more than τ_X1 (such defects give errors of order 1). At this site the patched logits do not depend on the context (Lemma R(iv)); that is the exact-linearity fact, not a weakness of the check. X1 does **not** check the output order of d (d does not enter the logits); that is the SYMBOL-ORDER checks (H1 (b), H2 (a), H3 (c) and the M0 two-route comparison) and the T-ORDER fixture (RC-1, NEW-2).

### 2.8 Random-subspace references (Lemmas RS1–RS2)
Let w = Σ_ε^{−1/2}Δy (whitened displacement), Π a uniformly (Haar) random orthogonal projector of rank k = 6 in ℝⁿ, n = 127, and P_R = Σ_ε^{1/2} Π Σ_ε^{−1/2} the corresponding Σ_ε-orthogonal random projector in y-coordinates.

**Lemma RS1 (aligned share).** E_Π[½dᵀMP_RΔy] = (k/n)·A_full for every row; hence E_Π[ψ_R] = 6/127 = 0.047244 exactly, conditional on the data. (Centring the logits does not reduce the sampling dimension to 126 or 35; the Haar projector lives in the 127-dimensional readout-coordinate space.)
*Proof.* ½dᵀMP_RΔy = ½ r̃ᵀΠw with r̃ = Σ_ε^{1/2}Mᵀd. E[Π] commutes with every orthogonal matrix, so E[Π] = cI, and tr E[Π] = k gives c = k/n. Then E[½r̃ᵀΠw] = (k/n)·½r̃ᵀw = (k/n)·½dᵀMΔy. The denominator of ψ_R does not depend on Π. ∎

**Lemma RS2 (energy).** With K = CMΣ_ε^{1/2} (36 × 127), e_R := ‖CMP_RΔy‖² = ‖KΠw‖², and

  E_Π[e_R] = a·‖Kw‖² + b·‖w‖²·‖K‖_F²,  a = k(n(k+1) − 2)/(n(n+2)(n−1)),  b = k(n − k)/(n(n+2)(n−1)).

For k = 6, n = 127: **a = 887/344043 = 0.0025782**, **b = 121/344043 = 0.00035170**, and a + nb = 6/127.
*Proof.* For symmetric S, Φ(S) := E[ΠSΠ] commutes with conjugation by every orthogonal matrix, so by Schur's lemma on Sym = span(I) ⊕ Sym₀ (both O(n)-irreducible), Φ(S) = aS + b·tr(S)·I. Trace: tr Φ(S) = tr(E[Π]S) = (k/n)tr S, so a + nb = k/n. With S = e₁e₁ᵀ: Φ(S)₁₁ = E[Π₁₁²] = a + b, and Π₁₁ = ‖Πe₁‖² ~ Beta(k/2, (n−k)/2), so E[Π₁₁²] = k(k+2)/(n(n+2)). Solving gives a and b as stated. Finally E‖KΠw‖² = tr(KᵀK·Φ(wwᵀ)) = a‖Kw‖² + b‖w‖²tr(KᵀK). ∎

Here ‖Kw‖² = ‖CMΔy‖² = e_full (the natural response's centred logit-change energy) and ‖K‖_F² = tr(CMΣ_εMᵀC) (no matrix square root is computed). **Per-row exact random-6-plane energy reference:**

  r_i := a·e_full,i + b·τ_K·w_iᵀw_i,  τ_K = tr(CMΣ_εMᵀC),  w_iᵀw_i = Δy_iᵀΣ_ε⁻¹Δy_i.

The random energy share η̄_R = E[r]/E[e_full] = a + b·n/g, where g := E‖Kw‖²/(E‖w‖²·‖K‖_F²/n) measures how strongly the natural displacement aligns with readout gain (g = 1 isotropic → 6/127; g = 3.63 [H, all of Δw in the 35-dimensional readout rowspace with flat gain] → 0.0149; g = 0.5 → 0.0919) [W].

**Caveat (CMP L6).** P_S is Γ-oblique as well as Σ_ε-orthogonal to its complement, so RS1–RS2 are exact references for a random Σ_ε-orthogonal 6-plane, not exact nulls for S. They calibrate the thresholds; they are not hypothesis tests. Empirical Haar frames (32 per model, `SeedTree(0).generator("c2-v1", "frame", j, r)`) are reported on TEST.

### 2.9 The energy-share bound for NOT_USED (MD 3; owner Q2)
**Definitions (per row, x pair).** e_full = ‖C(z⁺ − z⁻)‖² = ‖CMΔy‖²; e_S = ‖CMP_SΔy‖² = ‖C(z(y_S^{−←+}) − z(y⁻))‖², the total centred logit change, in every direction, that setting arm H⁻'s circle code to arm H⁺'s value causes (equal for the reverse swap). Centring removes the softmax-invariant common shift. η_S := E[e_S | E_x]/E[e_full | E_x].

**The bound (registered; owner-approved; unchanged).** NOT_USED_j requires, in addition to the aligned-share condition,

  (E-abs)  η_S < 0.10,  i.e. U(E[(e_S − 0.10·e_full)1_E]) < 0;
  (E-rand) E[e_S | E_x] < (127/60)·E[r | E_x],  i.e. U(E[(e_S − (127/60)·r)1_E]) < 0.

Together: **η_S < η₀ := min(0.10, (127/60)·η̄_R).**

**What NOT_USED means (RC-4).** The owner-approved inequalities are kept. The outcome is described throughout as: **"Low signed oracle-aligned share and bounded mean-square centred-logit effect for the registered interchange."** Negative contributions, which oppose the model's response, are included by this rule. A per-model qualifier **NEGATIVE_ALIGNED_CONTRIBUTION(j)** is reported whenever the signed contribution is certified negative: U(E[A_S·1_E]) < −g_s in the family stream at the family level α_F (§6.4). The rule contains no lower-bound condition on ψ. The qualifier-only treatment, with no lower-bound condition, is confirmed by owner addendum 21 (item 2; §18 item 4).

**Justification.**
1. *Same calibration as the ψ threshold.* The ψ threshold 0.10 is (127/60) = 2.1167 times the exact random share 6/127 (Lemma RS1). (E-rand) applies the same multiple to the exact random energy (Lemma RS2), row by row, so "the code moves the logits no more than 2.12 times what an arbitrary 6-dimensional Σ_ε-whitened subspace moves them, in expectation, on the same rows". Under isotropy (g = 1) the two conjuncts coincide at 0.10.
2. *Why both conjuncts.* The random energy share depends on the data (η̄_R = a + bn/g). If the natural displacement concentrates in readout-gain directions (g > 1), η̄_R ≪ 6/127 and 0.10 alone would let the code carry many times a random subspace's energy and still be called "not used"; (E-rand) blocks that. If g < 1, (127/60)η̄_R exceeds 0.10 and (E-abs) caps the share at the owner's "little in any direction" level. The conjunction is never more permissive than either.
3. *Scale (an RMS statement).* η_S < 0.10 means the RMS centred logit change caused by the code interchange is below √0.10 = 0.316 of the RMS natural response. It limits total RMS movement relative to the full logit change; it does not make the signed-share condition an equivalence test around zero.
4. *Cauchy–Schwarz (descriptive).* Because dᵀC = dᵀ, A_S = ½dᵀCMP_SΔy and **E|A_S| ≤ ½·(E‖d‖²)^{1/2}·(E e_S)^{1/2}**; E|A_S| and the bound are reported. The bound limits the mean absolute aligned effect in nat by the energy; it does **not** bound |ψ|. Example (RC-4): in orthonormal centred-logit coordinates, natural change ∝ (1, 100), code effect (−1, 0), oracle contrast along the first coordinate: ψ = −1 while the energy share is ≈ 1e-4, and both energy conjuncts can pass. No wording in this protocol says that the aligned-effect magnitude itself is below 10%.
5. *Cost in error control.* The energy conjuncts add no allocation in Lemma FW (§6.3): they can only be falsely passed in the truth region where the aligned-share statements contribute one event. The NEGATIVE_ALIGNED_CONTRIBUTION qualifier is outside the Lemma FW allocation (§6.3 remark 8).

If the aligned share is certified below 0.10 but an energy conjunct is not, the per-model status is **LOW_ALIGNED_j**, licensed only for the oracle direction and never called NOT_USED (owner Q2). The Fisher-weighted energy e^F_S = vᵀ(diag(p̄) − p̄p̄ᵀ)v, v = CMP_SΔy, p̄ = ½(p̂(H⁺) + p̂(H⁻)) (model predictives), is reported as a descriptive variant only (the owner's wording is "logits"). This bound (O-2) is confirmed by owner addendum 21 (§18 item 4).

### 2.10 C2-M: the upstream interchange at `resid_post_2`/32 (MD 2; owner Q3)
**Fit (FIT).** a₂ = `resid_post_2`[:, 32] (raw 128-d; LayerNorm is inside block 3). FWL of a₂ on 36 indicators, the 5 covariates and harmonics 1–3 of the **final** chart phase φ (the circle variable is unchanged): B₂ (128 × 6), Γ₂, Σ_ε2 (Ledoit–Wolf), GLS operator L₂ and P₂ = B₂L_{B₂} exactly as §2.5 (Lemmas G1–G3 hold verbatim with n = 128). Gates F1-2 (design rank 36 + 5 + 6 = 47; whitened [Γ₂, B₂] rank 11 and cond₂ ≤ 1e8; identities; GLS-REF), L1-2, R1-2 (§6.6).

**Interventions** (VAL and TEST eligible rows; inputs = source tokens H; `forward_with_patch(model64, inputs(H), "resid_post_2", 32, r)`):
- F (full): r± = a₂(H±);
- S (circle code): r± = a₂(H) + P₂(a₂(H±) − a₂(H));
- C (complement): r± = a₂(H) + (I − P₂)(a₂(H±) − a₂(H)).

**Wording (CMP L4; RC-6).** Block 3's attention at position 32 reads the keys and values of positions 0–31 computed from H's own unpatched prefix (common to both arms) **and** its own patched key and value at position 32. Block 3's MLP, the residual skip from the patched state, `ln_final` and `unembed` follow. So A_M,S includes both the skip path and the path through block 3, and no C2-M outcome distinguishes active block-3 processing from bypass through the skip.

**Per-row quantities** (logits at position 32; d = d_named): A_M,X = ½dᵀ(z_X⁺ − z_X⁻), X ∈ {F, S, C}; e_M,X = ‖C(z_X⁺ − z_X⁻)‖²; I_M = A_M,F − A_M,S − A_M,C (interaction, reported); A_M,ctx = A_full − A_M,F (context effect, reported).

**Context-matched ratio (CMP L5).** All of A_M,F, A_M,S, A_M,C are evaluated in the *same* context H, whereas the natural A_full has contexts H⁺ and H⁻. Dividing A_M,S by A_full would mix "which state sits at position 32" with "which history the context holds". The registered estimands are therefore:
- **τ_M = E[A_M,F | E_x]/E[A_full | E_x]**: the signed oracle-aligned effect of the full layer-2 final-position interchange in the fixed source context, as a share of the natural contrast; τ_M is unrestricted in sign and magnitude (it can be negative or exceed one; RC-5);
- **ψ_M = E[A_M,S | E_x]/E[A_M,F | E_x]** (primary M share; numerator and denominator in the same context);
- η_M = E[e_M,S]/E[e_M,F]; ψ_M,C = E[A_M,C]/E[A_M,F] (reported).
Lemma D3 applies to ψ_M once E[A_M,F 1_E] > 0, which the declared statement "τ_M > 0.10" establishes on the complement of its coverage failure.

**ROUTED_AROUND (restricted; RC-5).** ROUTED_AROUND_j iff U(Z_τ) < 0, Z_τ = (A_M,F − 0.10·A_full)1_E, i.e. τ_M < 0.10. 0.10 is the study's single negligibility threshold. The enum is kept (MD 2), with this licence only: *the signed oracle-aligned effect of the full layer-2 final-position interchange, in the fixed source context, is below 10% of the natural contrast. This does not distinguish weak transfer, opposition, cancellation, interaction, context incompatibility, or compensation, and does not establish routing around the circle.* No share of the response is attributed or denied to the layer-2 code from this outcome, and no inference to E-image is drawn. A small τ_M can coexist with large circle and complement effects that cancel or interact: E[A_full] = 1, E[A_M,F] = 0, E[A_M,S] = 1, E[A_M,C] = −1 is ROUTED_AROUND although the circle interchange has a substantial effect (independent fixture, §13.3 T-CMODE). **After the M outcome is recorded**, the circle, complement, interaction and energy quantities (E[A_M,S]/E[A_full], E[A_M,C]/E[A_full], E[I_M]/E[A_full], E[e_M,S]/E[e_full], E[e_M,C]/E[e_full], E[e_M,F]/E[e_full]) are reported descriptively for every M-ok model, including ROUTED_j models, with descriptive intervals outside the family. **The descriptive intervals are specified as follows (NEW-5):**
- **When and how many.** After the M outcome is recorded, 5,000 shared whole-row bootstrap draws (`c1_means.bootstrap_means`, PCG64(620518)) give two-sided 95% percentile intervals for the ratios of the resampled indicator-form means. The ranks come from `quantile_with_rank` at the exact levels 1/40 and 39/40: 125 and 4,875 [W].
- **Shared indices.** One index stream is shared across models and quantities.
- **Arrays.** Per model, the stream holds six numerator arrays (A_M,S, A_M,C, I_M, e_M,S, e_M,C, e_M,F, each ·1_{E_x}) and two shared denominator arrays (A_full·1_{E_x}, e_full·1_{E_x}): **24 arrays** for the three models.
- **Undefined intervals.** If an original or resampled denominator is zero, or a required quantity is nonfinite, that interval is reported as UNDEFINED. No replicate is discarded or redrawn.

This restricted licence is confirmed by owner addendum 21 (§18 item 2).

**N2 radial support screen (FEAS, then T-PRE on TEST; RC-6).** Class-mean Mahalanobis at layer 2 (X§8 rule, C1 §9 cap): μ_w = FIT class mean of a₂; Σ_2w = `ledoit_wolf`(a₂ − μ_w) over FIT; DM(h; w) = ‖Σ_2w^{−1/2}(h − μ_w)‖ with w = w32 of the row (shared by all arms); q99 = `c1_gates.q99` over FIT natural rows; F(·) = `c1_gates.frac_beyond` over (row, arm) pairs of eligible rows. Natural donor states D₂ = {a₂(H±)}. **PASS iff F(S-patched) ≤ max(0.05, F(D₂) + 0.02) and F(C-patched) ≤ max(0.05, F(D₂) + 0.02)** (thresholds unchanged; C1 §9 rule 1). F(D₂) ≈ 0.01 by construction of q99 on natural states [H]. N2 is an operational screen on the radial (Mahalanobis-norm) support of the patched states only: it is not a naturalness certificate, it does not assess the joint law of the interchanged state, and it does not assess compatibility with the source prefix's keys and values. In the paired-Gaussian counterexample (§2.5) the screen passes: the patched squared norm is 2t², whose probability of exceeding the natural two-dimensional Gaussian q99 (χ²₂ q99 = 9.2103) is 0.0319 [W], below the 5% cap. The F-patched states are natural donor states (in a foreign context), so they are the reference, not a gated family. Failure → EXCLUDED_j/RADIAL_SUPPORT (M only).

**Y2 placebo (M; active iff κ_m < 0.01 and the y-transmission check below passes).** Arms (H, H^Y) with source H, on the rows where H^Y is defined: arm H is natural; arm H^Y is patched in context H. A^Y_M,S = ½d^{Yᵀ}(z_nat(H) − z_S(H^Y in H)), A^Y_M,F likewise with the full state a₂(H^Y). Y2 statement (a registered linear inequality only, RC-7): E[(A^Y_M,S − 0.10·A^Y_M,F)1_{E_y}] < 0. Activity check (VAL): L(E[(A^Y_M,F − 0.10·A^Y_full)1_{E_y}]) > 0.

**Report-only (VAL, 1024 lowest-id eligible rows):** 8 Σ_ε2-whitened Haar 6-frames in place of P₂ (ψ_M,R); the per-row block-3 LayerNorm scale ratio. A direct-versus-through-block-3 split is **not** built (it needs new forward code); it is a next extension.

### 2.11 Secondary families (MD 2, MD 5; owner Q1)
**C2-S\* (oracle x-phase code; pre-registered secondary with its own licence).** φ*(H) = arg m32(b32(H)), m32 = Σ_z b32(z)(cos 2πx/12, sin 2πx/12) (oracle-computed; no chart). The whole C2-R pipeline (FWL, GLS, L1* with its D0, R1*, V3 shared, Y1*, endpoint, energy) is rerun with the masked features f*_3 in place of f(φ) (L1* target f*_1; NEW-3). It is computed regardless of C0v and is never a substitute for C2-R: its licence speaks of "the oracle x-phase code", never of "the PH circle", and carries the Q-CODE clause (RC-2).
- **Zero or unresolved modulus (deterministic; RC-14; masked features, NEW-3).**
  - *Masked features.* |m32| ≤ 1 always (a convex combination of unit vectors). Define m_valid(H) := 1[‖m32(H)‖ > 1e-12] and f*_K(H) := m_valid(H)·(cos kφ*, sin kφ*)_{k=1..K}. A row with m_valid(H) = 0 is ZERO_MOD. Its stored phase φ* = 0 is only a placeholder and never regenerates unmasked harmonic targets: an unmasked φ* = 0 would give the pairs (1, 0).
  - *Where the masked features are used.* **The S\* FWL regressors are f*_3, and every L1\* decoder (D0, D_code, D_lin) uses the target f*_1 ∈ ℝ²,** which is zero on invalid rows.
  - **Zero oracle modulus (R1\* and R1).** An arm with |m32| ≤ 1e-12 gives δ* := 0, so |δ*| = 0 and, if the row is selected, sign 0 counts as disagreement.
  - *ZERO_CODE.* The code phase φ_c of a row gives δ_c := 0 (disagreement) when its centred first-harmonic code pair has modulus ≤ 1e-12·m̃. The code pair is the first two coordinates of L_B(y − α̂_{w32}). m̃ is the `inverted_cdf` median of that modulus over the 8,192 FIT natural rows, computed at F1 **separately for each model and applicable family** (R: L_B and y; M: L_{B₂} and a₂ with its class means; S*: L_{B*} and y).
  - *Order of the overrides.* **The zero overrides are applied before the median selection and the agreement calculation** of R1, R1-2 and R1*. For an overridden δ*, the wrapper replaces the m32 inputs of both arms of that row by (1, 0); for an overridden δ_c, it replaces both phase inputs by 0. `c1_gates.v1` (unchanged) forms δ* from atan2 of m32 and δ_c by `wrap`, so it obtains δ* = 0 and δ_c = 0 exactly (atan2(0, 1) = 0; `wrap`(0) = 0) before it takes the `inverted_cdf` median of |δ*| and counts agreement [verified against `c1_gates.py` 76–95 at 967605c].
  - *Counting.* No row is deleted or replaced. The counts are reported in the coverage tally (ZERO_MOD_H/PLUS/MINUS, ZERO_CODE_PLUS/MINUS; §5.5) for every split. Expected count ≈ 0 under overlap emission [H].

**Rotation arm (report-only; owner Q1 secondary, corrected oracle).**
- *Intervention (closed form at `ln_final_out`/32; X§5 dose, CMP D7):* with f̂ := L_B(y − α̂_w) (= L_B(y − α̂_w − Γz̃) because L_BΓ = 0) and R_K(θ) the block-diagonal rotation turning harmonic k by kθ,
  y_rot(±θ) = y + B(R_K(±θ) − I)f̂.
  By Lemma G2 the code becomes R_K(±θ)f̂ (all three harmonics rotate, CMP X7) and every other coordinate is held.
- *Frozen orientation (RC-14).* Block k of R_K(θ) is [[cos kθ, −sin kθ], [sin kθ, cos kθ]] acting on the column (cos kφ, sin kφ)ᵀ, so R_K(θ)f(φ) = f(φ + θ): positive θ increases the code phase. The chart phase is oriented with +x by `fit_gauge` against m32, and +θ is paired with the oracle roll ρ^{(m)}_+ (x ↦ x + m). An exact synthetic sign fixture (§13.3 T-ROT) fixes this pairing.
- *Corrected oracle (owner Q1; CMP X1):* roll the belief **before** the last symbol and re-apply it: b_rot32^± ∝ (ρ^{(m)}_{±} b31(H)·T) ⊙ E[:, w32], with ρ^{(m)}_±(x, y) = ((x ± m) mod 12, y), computed by `c1_oracle.closed_form_b32` with that index map; q_rot^± = normalise(b_rot32^± T E). This holds w32 exactly as the intervention does.
- *What the dose means (RC-14).* **The dose names a latent pre-observation rotation. The code-coordinate rotation is a descriptive proxy whose posterior phase and shape need not match that oracle counterfactual.** Fixing the final observation generally prevents the posterior phase from rotating by exactly mπ/6, and chart alignment does not establish exact equivariance under latent translations, so rotating all registered harmonic pairs does not exactly match the oracle's post-observation phase or full belief transformation.
- *Doses:* θ = π/6 (m = 1, X's one cell) and θ = π/3 (m = 2). At m = 2, b_rot32^± equals the closed form of b32(H^±) (C1 §3.2): the oracle side agrees with the natural-donor closed form; the code side remains the descriptive proxy above.
- *Report:* A_rot = ½d_rotᵀM(y_rot(+θ) − y_rot(−θ)) (d_rot = q̄_rot⁺ − q̄_rot⁻ in named order), G_rot = ½Σd_rot(log q̄_rot⁺ − log q̄_rot⁻), θ_rot = E[A_rot | E_x]/E[G_rot | E_x], with a two-sided 95% percentile interval (5000 draws, seed 620517) on TEST. **Scalar sign-agreement statistic (RC-14):** s_rot := (1/|E_x|)·Σ_{i∈E_x} 1[A_rot,i > 0], per model and dose (A_rot,i = 0 counts as disagreement); since A_rot is already projected on d_rot, A_rot,i > 0 is agreement of the code-rotation logit change with the oracle's rotated-belief contrast. Attainable θ_rot can be < 1 even for a perfect circle user, because the rotation moves only the code while the rotated belief also changes shape. No claim is ever made from this arm.

### 2.12 Descriptive estimands (no decision effect)
ψ_Γ, ψ_rest, θ_S; E|A_S| and the Cauchy–Schwarz bound; ν_S = E‖J P_SΔy‖²/E‖P_SΔy‖² (J the Euclidean projector onto ker(CM): the share of the code displacement no readout can see; Makelov et al.'s "disconnected" component); **the operator decomposition (interpretability addition, review "interpretability controls"):**

  CMP_SΔy = CMP_S(I − J)Δy + CMP_SJΔy,  A_S = A_S^vis + A_S^null,  A_S^vis := ½dᵀMP_S(I − J)Δy,  A_S^null := ½dᵀMP_SJΔy,

with e_S^vis = ‖CMP_S(I − J)Δy‖², e_S^null = ‖CMP_SJΔy‖² and the shares E[A_S^null]/E[A_full], E[e_S^null]/E[e_full] (the same for P_Γ; the decomposition is a readout-site construction and is not computed at layer 2). Since CMJΔy = 0, a nonzero A_S^null or e_S^null shows readout-null source variation being converted by the patching operator into a readout-active patch, the mechanism of Makelov, Lange and Nanda (arXiv 2311.17030); reporting ‖JP_SΔy‖² (ν_S) alone does not answer that question. The decomposition is descriptive only: no projector is selected and no outcome changes from it. Also: ψ_max (the largest share of any Euclidean 6-plane, from the top-6 eigenvectors of sym(E[Δy·(Mᵀd)ᵀ]); output-optimised and illusion-prone, an upper reference only); the change in affine w32 and y-marginal readouts under P_SΔy as full score vectors (X§8, CMP D3); η̄_R and g; per-K partial R²; the L1 complete-decoder scores R²_code, R²_lin (RC-3); 32 empirical Haar shares; the Fisher-weighted energy; the y-pair partition; ‖y_S‖/‖y‖; the C2-M descriptive quantities of §2.10; the sealed validation endpoint values after the fresh outcome is recorded. The y-translation placebo tests one nuisance transformation; it cannot certify absence of other misattribution. Also reported (oracle-only, per split): the y pair's x leakage λ_x := mean_{E_y}‖m32(b31(H^Y)) − m32(b31(H))‖ / mean_{E_x}‖m32(b31(H⁺)) − m32(b31(H⁻))‖, and the same ratio at b32 (§2.2; about 0.2% at b31 before any C2 data).

---

## 3. Licensed claims and non-claims (the outcome lattice)

**Fixed scope of every licence:** the three E4 cylinder-O models (1729, 2718, 3141; step 5000; frozen weights in exact float64 casts); the natural cylinder-O process with overlap emission σ = 1.25 at 32 symbols, conditional on oracle eligibility; position 32; the ±2-cell x-history donors with the last symbol kept (and, for the placebo, the one-symbol-row y-translation donors toward the interior, w32 kept, on the rows where they are defined); the circle defined by the three reused C1′ production charts and their gauges (C2-S*: by the oracle x-phase); the frozen FIT fits. Every claim needs **2 of the 3 models** (owner Q4). **All three models receive the preregistered validity assessment and are reported. Failed validity gates can leave scientific endpoints NOT_RUN. Two valid, resolved models can support a two-of-three claim; no claim is made about the excluded model** (RC-13; confirmed by owner addendum 21, §18 item 3). Family-wise error is nominal 0.05 per family, separately, with R uniquely primary; the study-wide nominal union bound is 0.15 and is displayed wherever combined study conclusions are discussed (O-3; Lemma FW, §6.3). Bracketed values are filled from the run.

**Q-CODE (mandatory clause of every family licence and of the summary; RC-2, verbatim):** *"These outcomes concern the frozen, nuisance-excluding linear code defined by this fit and projector. They do not exclude predictive use of phase information in excluded directions, higher harmonics, interactions, or other encodings."* (C2-M: "…defined by the layer-2 fit and projector…"; C2-S*: "…defined by the oracle x-phase fit and projector…".)

### 3.1 C2-R (primary family)

| # | Overall outcome (rule §10) | Licensed sentence (each followed by Q-CODE) |
|---|---|---|
| R0 | FAIL_TECHNICAL/<class> | "No statement about the models: an identity, lineage, oracle, model or numerical-integrity defect was found at gate [g] ([values])." Not a negative result |
| R0′ | INCONCLUSIVE/<reason> (a study-level validity gate, or fewer than 2 models left after a per-model validity gate) | "The assay was infeasible as specified at gate [g] ([values]; per model [statuses]; endpoints NOT_RUN for [models])." Not evidence for or against use of the circle |
| R1 | CIRCLE_NOT_HISTORY_SENSITIVE (≥ 2 models with L1 PASS and R1 FAIL at FEAS) | "In models [list], the registered first-harmonic phase coordinate failed the specified directional registration criterion on FEAS (sign agreement [ ] < 0.75 on the larger half of the oracle phase changes; L1 passed: R²_code\|0 [ ], incremental ratio [ ]); this is an assay-registration finding, not evidence that the representation carries no history." Not licensed (RC-8): absence of history sensitivity (a code can move consistently in the opposite orientation, move in unmeasured coordinates, or keep substantial sensitivity below the threshold); anything about the circle's use for the last symbol or other counterfactuals |
| R2 | **USED** (≥ 2 USED_j) | "In [k] of the 3 models ([list]; the other: [status]), the registered code interchange carries more than half of the signed oracle-aligned response: setting the six circle-code coordinates of the final LayerNorm output at position 32 to their values under the counterfactual history, with every other coordinate held fixed, gives ψ̂ = [ ] (one-sided lower bounds [ ]) of the model's signed oracle-aligned response to a ±2-cell rotation of the x-history with the last symbol kept. The models respond to this counterfactual (θ_full > 0.30). [If Y1 active:] The mean signed placebo contribution is below 0.10 times the mean full placebo contrast." Not licensed: that the readout's history-dependent prediction runs mainly through "the circle" in general; necessity; uniqueness of the carrier |
| R3 | **NOT_USED** (≥ 2 NOT_USED_j) | "In [k] of the 3 models, the registered interchange has a low signed oracle-aligned share and a bounded mean-square centred-logit effect: the circle code moves with the counterfactual on FEAS (registration [ ]) and the model responds (θ_full > 0.30), yet setting the code to its counterfactual value gives a signed oracle-aligned contribution below 0.10 of the model's signed oracle-aligned response (the contribution may be negative, i.e. opposing; [NEGATIVE_ALIGNED_CONTRIBUTION in models …]), and its total effect on the centred logits has less than 10% of the mean-square energy of the full natural response and less than 127/60 times the energy that a Σ_ε-whitened random six-dimensional subspace carries in expectation on the same rows. **The position-32 readout does not use this registered code interchange beyond this bound.**" (MD 8: never "computationally inert" without the bound, the site and Q-CODE.) Not licensed: that the aligned-effect magnitude is below 10%; that the readout reads the x-history through other directions (ψ̂_Γ [ ], ψ̂_rest [ ], ν_S [ ] and the operator decomposition are descriptive) |
| R4 | LOW_ALIGNED_SHARE (≥ 2 models in {NOT_USED_j, LOW_ALIGNED_j}, fewer than 2 NOT_USED_j) | "In [k] models the signed oracle-aligned contribution of the registered code interchange is below 10% of the model's signed oracle-aligned response, but its total logit-change energy was not shown to be below the bound, so movement of the logits in other directions, or per-row cancellation, is not excluded. **This is not a NOT_USED result.**" |
| R5 | PARTIAL (≥ 2 PARTIAL_j) | "In [k] models the registered code interchange carries more than 10% and less than 50% of the signed oracle-aligned response (ψ̂ [ ], bounds [ ]); ψ̂_Γ, ψ̂_rest are reported descriptively." Not licensed: a majority, a null, or a mechanism ("one channel among others") |
| R6 | MIXED (no category in ≥ 2 models; ≥ 2 models with a resolved category) | "Per-model statuses [..]; no 2-of-3 claim is supported." Not licensed: selecting a model after the fact; population heterogeneity (RC-8) |
| R7 | INCONCLUSIVE/PRECISION (no category in ≥ 2 models; at most one model resolved) | "The fresh test could not resolve ψ against 0.10 and 0.50 in two models ([intervals])." No claim; not evidence of lack of use (RC-8) |

**Per-model statuses (always reported):** USED_j, NOT_USED_j, LOW_ALIGNED_j, PARTIAL_j, INC_j (an interval straddles a threshold, or a NUM guard hit), CNHS_j (R1 failed after L1 passed; the RC-8 licence), EXCLUDED_j/<gate> (a per-model validity gate failed: CHART_UNAVAILABLE, PATCH_MODEL_DEGENERATE, NUMERICAL, LINK, MODEL_HEADROOM, NUISANCE_IN_S, TEST_GATE, UNDERPOWERED).

**Endpoint status (RC-13; NEW-6):**
- **NOT_RUN/<gate>.** A model excluded from family F at a gate before ACCEPT (S2–S4), at T-PRE or at RESP/SPEC has its F endpoint **NOT_RUN/<gate>**. No F endpoint array is formed for it, and its permitted gate and integrity data are retained and reported. *If T-PRE fails before scientific endpoint formation, record the endpoint as NOT_RUN/<gate>.*
- **SEALED_UNSCORED.** *SEALED_UNSCORED applies only to arrays already lawfully formed. No endpoint is computed merely to fulfil a promise to report a sealed array.*
- **Descriptive values.** For a model excluded at T-PRE or at RESP/SPEC, descriptive values are produced only by the separate post-outcome operation POST-DESC (§5.7), labelled "unlicensed (gate [g])". Its endpoint status stays NOT_RUN/<gate>.

Only the declared per-model categories are inferential statements under Lemma FW; CNHS_j, EXCLUDED_j, INC_j and NOT_RUN are operational results (RC-8).

**Coarse statements (reported with every R outcome; same family, no extra allocation, §6.3; RC-8 prerequisites):** for each model j whose RESP_j and SPEC_j (or Y1 inactive) are declared, as for the categories: "ψ > 0.10 in at least two [in all three] models" iff L(Z^{0.10}) > 0 in ≥ 2 [3] such models; "ψ < 0.50 in at least two [in all three]" iff U(Z^{0.50}) < 0 in ≥ 2 [3] such models. A model without the prerequisites does not count toward a coarse statement.

**Qualifiers (never change the outcome):**
- SPECIFICITY_NOT_ESTABLISHED: Y1 inactive (κ_m ≥ 0.01, or V3y failed at VAL). When Y1 is active it licenses only the registered linear inequality (RC-7).
- NEGATIVE_ALIGNED_CONTRIBUTION(j): U(E[A_S·1_E]) < −g_s in the family stream at α_F for a model with RESP_j declared (RC-4; outside the Lemma FW allocation, nominal per-statement level α_F).
- PROJECTOR_DEPENDENT(j): the Euclidean-complement variant's category for model j differs from the primary category.
- HARMONIC_DEPENDENT(j, K): the K-variant's category differs (K = 1 is C1's first-harmonic plane, MD 5; its category is always reported).
- PRECISION_LIMITED(j): model j failed P1 at the chosen N.
- DISSENT(j: status): the model not counted in a 2-of-3 claim.

### 3.2 C2-M (secondary family; owner Q3)

| Outcome (≥ 2 models unless stated) | Licensed sentence (each followed by Q-CODE for the layer-2 code) |
|---|---|
| ROUTED_AROUND | "In [k] models, the signed oracle-aligned effect of the full layer-2 final-position interchange, in the fixed source context, is below 10% of the natural contrast (τ̂_M [ ]). This does not distinguish weak transfer, opposition, cancellation, interaction, context incompatibility, or compensation, and does not establish routing around the circle." (RC-5, verbatim.) Reported descriptively after the outcome is recorded: the circle, complement, interaction and energy quantities of §2.10. Not licensed: any share attributed or denied to the layer-2 code; E-image; that layer 2 carries no history; anything about other positions |
| UPSTREAM_USED | "In [k] models, the full layer-2 final-position interchange carries more than 10% of the natural contrast (τ̂_M [ ]), and the registered layer-2 code interchange, in the source context, carries more than half of the signed oracle-aligned effect of the full interchange (ψ̂_M [ ]). The layer-2 code intervention changes the final output after the remaining computation, including the residual skip." (RC-6.) Not licensed: that block 3's attention or MLP reads the code; any distinction between active block-3 processing and bypass through the skip; that the interchanged state is natural |
| UPSTREAM_NOT_USED | "…the full interchange carries more than 10% (τ̂_M [ ]), but the registered layer-2 code interchange has a low signed oracle-aligned share (below 0.10 of the full interchange's, possibly negative) and a bounded mean-square centred-logit effect (below 10% of the full interchange's energy)." Not licensed: that the layer-2 state carries the history through other directions |
| UPSTREAM_LOW_ALIGNED | As R4, at layer 2 |
| UPSTREAM_PARTIAL | The registered layer-2 code interchange carries between 10% and 50% of the full interchange's signed oracle-aligned effect |
| CNHS-2 | As R1, at layer 2 (L1-2 PASS, R1-2 FAIL): "the registered layer-2 first-harmonic phase coordinate failed the specified directional registration criterion on FEAS; this is an assay-registration finding, not evidence that the representation carries no history." |
| MIXED / INCONCLUSIVE/<reason> | As R6, R7, R0′ (including RADIAL_SUPPORT from N2) |

Caveats stated in every C2-M licence: a patched final-position state combined with a context from H is never produced naturally (it is the intended interchange counterfactual); N2 is a radial support screen, which assesses neither the joint law of the interchanged state nor its compatibility with the source prefix's keys and values; the residual skip is part of every M effect; only position 32 is tested; self-repair can lower τ_M; Q-CODE.

### 3.3 C2-S* (secondary family; MD 5)
Outcomes X_PHASE_USED, X_PHASE_NOT_USED, X_PHASE_LOW_ALIGNED, X_PHASE_PARTIAL, X_PHASE_NOT_HISTORY_SENSITIVE, MIXED, INCONCLUSIVE, with the R sentences in which "the circle code" is replaced by **"the six-dimensional code of the oracle x-phase (harmonics 1–3 of arg m32 of the exact belief)"**, every RC-2/RC-4/RC-7/RC-8 restriction applied: the USED and NOT_USED sentences speak of the registered oracle-phase code interchange; X_PHASE_NOT_HISTORY_SENSITIVE uses "the registered first-harmonic oracle-phase coordinate failed the specified directional registration criterion on FEAS; this is an assay-registration finding, not evidence that the representation carries no history"; each sentence carries Q-CODE ("…defined by the oracle x-phase fit and projector…"); ZERO_MOD counts are stated. It licenses a statement about the oracle phase variable, never about the PH circle, and never substitutes for a C2-R outcome.

### 3.4 Rotation arm (report-only)
"Rotating the six-dimensional circle code within its own coordinates by ±θ (harmonic k by kθ, frozen orientation §2.11), with every other coordinate held fixed, moved the model's prediction in the direction of the prediction of the belief obtained by rotating the pre-last-symbol belief by ±[m] cells and re-applying the last symbol, by θ̂_rot = [ ] of that belief contrast (95% interval [ ], descriptive; sign agreement s_rot = [ ]). The dose names a latent pre-observation rotation. The code-coordinate rotation is a descriptive proxy whose posterior phase and shape need not match that oracle counterfactual." No claim, no gate, no family.

### 3.5 Never licensed (union of L§10.4, X§2/§10, CMP and the review; MD 8)
- topological necessity; any claim about the square or the P/U/N models;
- that the circle is the only carrier, or that it is necessary (C2 is an interchange, a sufficiency-type test; redundancy is not tested);
- that the registered code contains all predictively relevant circle information; any outcome read as excluding predictive use of phase in excluded directions, higher harmonics, interactions or other encodings (Q-CODE, RC-2);
- "computationally inert" or "useless in the network" without the stated bound, site and Q-CODE (MD 8); any upstream mechanism from C2-R alone;
- that NOT_USED bounds the magnitude of the aligned effect by 10%, or excludes opposition (RC-4);
- routing around the circle, E-image, or any cause of a small τ_M from ROUTED_AROUND (RC-5);
- that block 3's attention or MLP reads the layer-2 code, or any split between block-3 processing and the residual skip (RC-6);
- that an interchanged state follows a natural law, or that N2 certifies naturalness (RC-6);
- that Y1, Y1* or Y2 establish general nuisance exclusion, a small placebo-effect magnitude, a population placebo ratio, or the absence of a subspace illusion; that the y-translation certifies absence of other misattribution, or leaves the x-belief exactly unchanged (its x leakage is a measured, reported property, §2.2) (RC-7);
- that CNHS shows the representation carries no history; that MIXED shows population heterogeneity; that INCONCLUSIVE shows lack of use (RC-8);
- an exact or finite-sample 0.05 coverage (the implemented FWER is nominal, RC-9);
- that the code rotation matches the oracle's post-observation phase or full belief transformation (RC-14);
- separation of w31 from longer history (E-short); long memory; horizons beyond w33;
- other sites, positions, counterfactual families, checkpoints, architectures or language models;
- a literal internal variable, a unique natural computational variable, or a learned belief algorithm;
- selective coverage (rows are conditional on oracle eligibility only);
- that the rotation arm or any Haar frame is evidence for or against use;
- that C2-S* speaks about the PH circle; any claim about an excluded model;
- any claim combining families, or selecting the favourable family as "the answer";
- any change to the C1′, X4-F, E4, K4, K4b, B2, K8, H5 or X6 verdicts, or a reading of C2 as a rescue of C1′.

---

## 4. Models, sites, and why no training

| Models | Use | Reason |
|---|---|---|
| cylinder-O 1729, 2718, 3141 (step 5000) | all of C2 | They carry the circle: E4 agreement 0.884–0.892 against 0.915 for the exact belief (request; L§3); C1′ gauge alignment 0.894–0.899 [W, 0044] |
| square-O × 3 | not used | No periodic coordinate, no τ symmetry, no x-donors |
| cylinder-P, square-P × 6 | not used | The belief geometry itself has no circle under P (agreement 0.05; L§3) |
| U × 2 | not used | The last symbol reveals the state: within-class G = 0 (no headroom) |
| N × 3 | not used | No information |

**Frozen float32 `state_sha` (RC-16; O-7 resolved).** Copied from the C1′ M0 gate record (`c1prime-store/GATES.jsonl` line 8, gate M0, PASS, 2026-10-16T08:01:43Z, field `values.models.<j>.sha_f32`) into the frozen contract. These are the production `state_sha` values recorded by M0 (`c1_model.state_sha`), **not** checkpoint-file SHA256 values:

| Model | `state_sha` (float32, M0) |
|---|---|
| 1729 | `062d0a0aa71c41ad5afd9d3f76e58cf38a81419d629defcf2e3ac6316ffaf8f8` |
| 2718 | `501d9c9ad80d4ffe272d7e03003cdee24b7fe3b25bed40e044f2111afd69aa5c` |
| 3141 | `197cccd6cf5491143171fe8ccd6ce79f71cb2f16995aa99af4e9dffe4bec94c8` |

- **No new training.** The question is whether *these* trained models use their circle code. Every C2 quantity is a functional of their frozen weights and of new oracle-sampled histories. Training would be needed only for a counterfactual about learning ("would a model without a circle predict as well?"), which C2 does not ask.
- **Sites (fixed; no search).** Circle variable: `resid_post_3`/32 (the PH site, through the C1′ chart). Attribution: `ln_final_out`/32 (C2-R, C2-S*, rotation arm). Upstream interchange: `resid_post_2`/32, the last site with a nontrivial downstream block; the E3 layer sweep shows the H1 contrast there (median D 0.172–0.186) at least as strong as at `resid_post_3` [W, L§3].

---

## 5. Data discipline

### 5.1 Splits (all new; scope `c2-v1`)

| Split | Rows | Allowed use | Logits read |
|---|---|---|---|
| **FIT** (fitting) | 8192 (blocks b0, b1) | s_max, κ_ν, κ_m; FWL (all K), Σ_ε, GLS projectors (R, M, S*, variants); L1 decoders (D0, D_code, D_lin); N2 class means, Σ_2w, q99; chart support | Only on the 1024 lowest-sequence-id rows, for the M0 identity checks (including the M0 two-route SYMBOL-ORDER comparison). Never otherwise |
| **FEAS** (feasibility) | 4096 (b0) | Activation-only validity: C0v (its 512 lowest-id rows are the direct comparator's landmarks), L1, R1, N2, chart support, coverage tally | **None** (forwards run; logits are discarded unread) |
| **VAL** (validation) | 4096 (b0) | X1 (ephemeral), V3x, V3y, Y1, Y1*, Y2 (activity checks and gates), P1 precision (SDs only) | Yes; every endpoint-bearing mean is sealed (§5.7) |
| **TEST** (fresh) | k × 4096, k ∈ {1, 2, 4} (N_test ∈ {4096, 8192, 16384}) | T-PRE gates (X1 ephemeral inside T-PRE), then the single confirmatory endpoint of each family | Endpoint arrays only after the relevant admission gates |

The separate FEAS split (X§3) decides the instrument's validity (does the code decode the circle beyond the baseline; does it move with the counterfactual; do patched layer-2 states pass the radial support screen) on rows on which no logit is ever read. VAL then measures the model's response and the precision on different rows. FEAS findings are operational assay findings, outside Lemma FW (RC-8).

### 5.2 Sampling, seeds and identifiers
- **Histories:** `HMMSampler(T, E_canon, π, SequenceLayout()).sample(4096, rng)` once per block, rng = `SeedTree(0).generator("data", "c2-v1", split, block, "cylinder", "overlap", "1.25")`, split ∈ {"fit", "feas", "val", "test"}. w33 and the latent states are dropped in memory immediately (as in `c1_data.sample_block`, which cannot be reused because it hard-codes `c1-sf-v1`). Model input tokens are perm[w] of the canonical symbols (the map of §2.3). TEST blocks are sampled only after the coordinator's ACCEPT of the validation report.
- **Sequence ids:** `make_sequence_ids(process_code("cylinder", "overlap", "1.25", f"c2-v1/{split}/b{block}"), "test", 4096)` (the role argument as in `c1_data.sequence_ids`). Panels: `c1_data.panels` (8 panels on FIT).
- **Donors:** H⁺, H⁻ by `c1_oracle.donors`; H^Y by the υ map with the sign rule k_Y and the off-grid rule of §2.2 (never clamped or wrapped; no H^Y on an OFF_GRID_Y row).
- **Haar frames:** `SeedTree(0).generator("c2-v1", "frame", j, r)`, r = 0..31 (R, report) and r = 0..7 (M, report); `c1_fit.qr_pos` of a 127 × 6 (M: 128 × 6) standard-normal draw, mapped by Σ_ε^{1/2}.
- **Bootstrap seeds (PCG64):**

| Seed | Use |
|---|---|
| 620501 / 620502 | VAL P1 for R: `sd_b4_draws` / `centered_draws` |
| 620503 | TEST: the whole R family (V3x, Y1, Z^{0.10}, Z^{0.50}, V^{abs}, V^{rand}), the NEGATIVE_ALIGNED_CONTRIBUTION array, and the R qualifier variants; one shared index stream |
| 620504 | VAL V3x |
| 620505 / 620506 | H5 on VAL / on TEST (G_x and G_y; two calls with the same seed) |
| 620507 / 620511 | VAL P1 for M: centred / SD |
| 620508 | VAL V3y |
| 620509 | VAL Y1 |
| 620510 | VAL Y2 and the Y2 activity check |
| 620512 / 620514 | VAL P1 for S*: SD / centred |
| 620513 | TEST: the whole M family (V3x, transmission, Z_M^{0.10}, Z_M^{0.50}, V_M, Y2) and its NEGATIVE array |
| 620515 | VAL Y1* |
| 620516 | TEST: the whole S* family and its NEGATIVE array |
| 620517 | TEST: rotation arm (descriptive) |
| 620518 | TEST, after the M outcome is recorded: 5,000 shared whole-row draws; two-sided 95% percentile intervals of the six C2-M descriptive ratios per model (24 arrays; UNDEFINED on a zero or nonfinite denominator, no redraw; §2.10, NEW-5) |

  Reuse of an integer seed across independently named PCG64 streams (e.g. 620505/620506 for H5) is not itself scientific leakage; the specified joint streams must remain reproducible (O-9).
- **Namespace admission (gate G0; RC-11, verbatim rule):** *No unrelated or superseded scientific lineage may have used `c2-v1`. Permit the current pinned code/configuration and explicitly recognised records of this authorised lineage. Before first sampling, require no prior scientific data for that lineage; on continuation, require exact recognised manifests and hashes.* Operationally: (i) a scan of every CONTRACT, FREEZE, STAGES and GATES record and every store directory under `X:/Downloads/projects/topo-pilot/` for the tag `c2-v1`; every hit must be either the pinned code/configuration at H (`tools/c2_readout/`, `CONTRACT.json`, the protocol byte copy) or a record listed in the lineage manifest (`c2-readout-store/FREEZE.json`, `AUTH.json` and the accepted job outputs with their sha256); any other hit → FAIL_TECHNICAL/LINEAGE; (ii) at S1 before first sampling, the store holds no `hist/`, `oracle/`, `fits/`, `stages/` or `sealed/` payload; (iii) at every later job, every existing store file matches the recognised manifests and hashes exactly (§11 item 7). The three cases are tested separately (§13.3 T-NAMESPACE).

### 5.3 Registry and leakage rules (C1 §2.4 pattern; version `c2-reg-v1`)
- **R (prior exposures),** built before FIT is sampled, by the frozen `c1_data.build_registry` with readers:
  - (a)–(c) the C1′ registry v1 sources (every ObservationSet under `artifacts/`; the X4, X4-B2, job-0014, K4, X4-F, d1-seam, chart-diag and K4b stores; planning-feasibility histories under `agent-handoff`), via `tools/c1prime_registry/c1_registry_sources.py` unchanged;
  - (d) every C1′ history and donor: `c1prime-store/HIST_cal_b0.npz` (`d80ad5f4…5ba5e`; it holds the 512 chart landmarks), `HIST_cal_b1.npz` (`7b33b372…284a`), `HIST_val_b0.npz` (`97db9467…6616`) (jobs/0041), roles H, H⁺, H⁻;
  - (e) an inventory of every other `*-store*` directory under the project root (including `k4b-store`, `x6-stage0-oracle-store`, `x6-stage1-store`, `x2a-stage0-oracle-store`, `d2a-store`, the `x4*` and `x5g1*` stores and `circular-audit-store`). Each is either read by an existing reader (K4b registry readers; X6S1 registry readers) or carried by an explicit exclusion record stating that it holds no history tokens. An unreadable source, or a history-bearing directory with neither, is INCONCLUSIVE/REGISTRY_INCOMPLETE. **The complete source and exclusion inventory is still to freeze in `API.md` before sampling (O-7, outstanding).**
- **Digests:** `scores.history_digests` of the canonical 32-symbol arrays, for every role of every row (H, H⁺, H⁻, and H^Y wherever it is defined).
- **Separation (gate H2):** U_FIT, U_FEAS, U_VAL pairwise disjoint and each disjoint from R; `check_disjoint`; `c1_data.first_token_ok` per block. **TEST:** R′ = R ∪ U_FIT ∪ U_FEAS ∪ U_VAL is rebuilt after ACCEPT, before TEST is sampled; U_TEST ∩ R′ = ∅. A collision is FAIL_TECHNICAL/LINEAGE. Rows are never rejected or replaced, so every split is an unconditioned iid draw from the natural law (a collision suppresses claims; it does not condition the sampling distribution).
- **Leakage rules.** (L1) No TEST token exists before ACCEPT. (L2) No logit on FIT except the M0 rows; none on FEAS. (L3) Every threshold, tolerance, seed, grid, K, covariate set, projector, site, donor step and chart is fixed at the freeze and never changed after any C2 data exist (stop rule S3). (L4) Nothing is selected on any model output: all fits use activations and oracle quantities only; decoders and subspaces never see logits. (L5) Validation endpoint-bearing statistics are sealed (§5.7). (L6) Pytest base temporaries and every scratch directory live outside the project root (`X:/Downloads/topo-scratch/<job>/`; the K4b registry trap). (L7) The chart landmarks are exposures in R and never C2 data.

### 5.4 Eligibility (oracle-only, fixed before any model work; C1 §4 kept)
- s_max = `c1_oracle.s_max`: the FIT q0.999 (`inverted_cdf`) of the natural surprisal −log q_31(H)[w32]; frozen at S1.
- **E_x:** s⁺ ≤ s_max, s⁻ ≤ s_max, and H, H⁺, H⁻ all have finite log-evidence (`c1_oracle.eligible`).
- **E_y:** Y_def(H) = 1 (§2.2), s^Y ≤ s_max, and H, H^Y have finite log-evidence.
- **H4:** f_x ≥ 0.90 and f_y ≥ 0.85 on FIT, FEAS and VAL (C1′ recorded f = 0.98401 and 0.98584 for the identical x construction [W, 0041]). f_y = |E_y|/N over all rows of the split, so OFF_GRID_Y rows count as ineligible. The 0.85 threshold is owner addendum 23. The job 0104 in-memory check of this construction gave f_y = 7,313/8,192 = 0.89270 (OFF_GRID_Y on 831 rows; 0.99348 within Y_def) [W, scratch seed 999002]. v1's 0.90 for the reflection donor is withdrawn, because that donor gave f_y = 3,641/8,192 = 0.44446 [W, job 0104, scratch seed 999001].
- No row is removed after the model stage; ineligible rows are stored with their reasons.

### 5.5 Per-reason coverage tally (MD 7; X§3)
For every split, every row is counted under every applicable reason (a row can carry several): S_PLUS, S_MINUS, S_Y (surprisal above s_max); LIK_H, LIK_PLUS, LIK_MINUS, LIK_Y (non-finite log-evidence); OFF_GRID_Y (a shifted prefix symbol of H^Y would leave rows 0..5: no H^Y is formed, S_Y and LIK_Y are not evaluated on that row, and the row counts as ineligible for the y pair in f_y; §2.2); ZERO_MOD_H, ZERO_MOD_PLUS, ZERO_MOD_MINUS (|m32| ≤ 1e-12; §2.11); and, per model and family, UNSUPPORTED_H/PLUS/MINUS (chart extension not supported: the row is kept and phased; support is gated as a fraction), ZERO_CODE_PLUS/MINUS (centred code-pair modulus ≤ 1e-12·its FIT median, per model and family; §2.11), R1_ZERO (sign 0 in δ_c or δ*), R1_UNSELECTED (|δ*| below the median). The tally is a report table and an input to H4 and C0; it never removes a row.

### 5.6 Use of the C1′ charts by sha256 (MD 5)
Gate C0c loads each NPZ with `chart.chart_from_arrays` only after its file sha256 equals the §2.4 value. The K4 kernel files are bound by the K4 FREEZE (`x4-circle-history-feas-store-0015/FREEZE.json`, sha256 `e3049feedf0fadfb004c9422effe560af031addb846a7b8d1c1bffd52ce3c94a`), with blobs `chart.py` `938821a0…9ccb`, `cochain.py` `e53f6725…3075` and `errors.py` `8aa309c4…b99f` at 967605c (full sha256 `8aa309c42350cad93f24ad73baf09a70e10c1d552a0b5d70514eeb541c7eb99f`; v1's abbreviation "…f99f" was a typo, corrected by E-0102-1, coordinator addendum 2). No chart is refitted. The only new chart constructions are the three C0v direct comparators on FEAS (a new C2 `ConstructionLedger`, limit 3). There is no fallback chart; C2-S* is a separate family, not a fallback.

### 5.7 Sealing and the computation-order rule (C1 §2.2 adapted; a C2 `LogitPolicy`)
- FIT: logits only on the M0 rows. FEAS: none.
- **X1 is an ephemeral integrity operation (RC-13).** At VAL and inside T-PRE on TEST, X1 may form the prescribed replacements and compare logits. It retains only identity diagnostics (per-arm maximum deviations, the count and ids of rows over tolerance) and may not form, retain or release scientific endpoint arrays or summaries (no A_S, A_Γ, A_rest, e_S, r or any mean of them) before the relevant admission gates pass. The `LogitPolicy` enforces this: the X1 code path has no write access to endpoint arrays, and its patched logits are discarded after the comparison. This resolves the v1 order ambiguity between "no endpoint array before T-PRE" and "X1 within T-PRE".
- VAL: after X1, A_full and A^Y_full (V3), A^Y_S (Y1), A^Y_M,* (Y2 and its activity check) are released as gate statistics. **Sealed until the fresh outcome is recorded:** the x-pair A_S, A_Γ, A_rest, e_S, r, V^{abs}, V^{rand}; A_M,F, A_M,S, A_M,C and e_M,* (hence τ_M and ψ_M); the S* equivalents; the variants; the operator decomposition; the rotation arm; and every statistic from which any of their means can be reconstructed. P1 releases SDs, MDEs and power only (outcome-blind precision calculations on VAL are acceptable).
- TEST: no endpoint array is computed before T-PRE passes (X1 inside T-PRE is ephemeral, above). V3x and Y1 are computed first, with the same seed and index stream as the endpoint (§6.2); then the endpoint arrays of the admitted models only (an excluded model's F endpoint is NOT_RUN/<gate>, §3.1).
- **Endpoint status at a TEST failure (NEW-6, reviewer's rule).** *If T-PRE fails before scientific endpoint formation, record the endpoint as NOT_RUN/<gate>. Retain permitted gate and integrity data. SEALED_UNSCORED applies only to arrays already lawfully formed. No endpoint is computed merely to fulfil a promise to report a sealed array.*
- **Post-outcome descriptive operation (POST-DESC; NEW-6).**
  - *Scope.* It covers a family or model whose endpoint is NOT_RUN at T-PRE (INCONCLUSIVE/TEST_GATE or EXCLUDED_j/TEST_GATE) or at RESP/SPEC.
  - *What it computes.* Descriptive point values of that family's estimands: eligible-row ratios, with no bound, category or qualifier.
  - *When.* It is a separate operation in the REPORT stage and starts only after every family outcome is recorded. Its arrays did not exist before admission and are formed only then.
  - *Effect.* None: the endpoint status stays NOT_RUN/<gate>, the values are labelled "unlicensed (gate [g]); computed after the outcome", and nothing in it changes an outcome, a status or a qualifier.
  - *When it is not run.* After a FAIL_TECHNICAL, after an INVALID, or for an exclusion before ACCEPT.

---

## 6. Statistics and inference

### 6.1 Units, conditioning and independence
- **Rows.** One history H per row; its arms (H⁺, H⁻ and, where Y_def(H) = 1, H^Y) are deterministic functions of H. TEST rows are an iid draw from the natural law, sampled after every fit, gate and threshold is frozen, from streams never used before (registry R′, §5.3). The models, charts and FIT fits are independent of the TEST rows.
- **Indicator form.** Every TEST per-row statistic s is used as s·1_E over **all** N_test rows (E = E_x for x-pair statistics, E_y for y-pair statistics). Because P(E) > 0, sign E[s·1_E] = sign E[s | E], so every registered decision about a conditional mean is a decision about an unconditional mean of an iid per-row variable, and all statistics of a family share one row set and one bootstrap index stream. Point estimates (ψ̂ etc.) are reported as eligible-row ratios. On a row with Y_def(H) = 0 (OFF_GRID_Y) no y-pair statistic is computed, and its indicator-form value s·1_{E_y} is 0 by definition.
- **Conditioning.** Inference is conditional on the three registered models and on the frozen chart, gauge and FIT fits (as C1 §1.3); no population-of-seeds claim. Shared TEST rows, shared bootstrap indices and a VAL-selected common TEST size are acceptable because all selection precedes TEST and the inference is conditional on the frozen choices.

### 6.2 Bounds
- **TEST (family bounds).** `c1_means.bootstrap_means(arrays, seed, draws=20000)`: one `rng.integers(0, n, size=n)` per draw, shared by every array of the family (all models, all statistics), tree means. L = `quantile_with_rank(means, α)`, U = `quantile_with_rank(means, 1 − α)` with α an exact `Fraction`:

| Family | α per bound | Ranks (of 20,000) | z_{1−α} |
|---|---|---|---|
| R, S* | 1/240 = 0.05/12 | 84 and 19,917 | 2.6383 |
| M | 1/360 = 0.05/18 | 56 and 19,945 | 2.7729 |

  V3x and Y1 are computed first at T-PRE; running `bootstrap_means` later with the same seed and n reproduces the identical index stream for the endpoint arrays.
- **VAL (gate bounds; C1 precedent, not in any family).** 5,000 draws, one-sided level 0.05/3 (ranks 84 and 4,917); H5 at level 0.05 (rank 250).
- **What the bounds deliver (RC-9).** The ranks are correct for the requested `inverted_cdf` quantiles; the run-time rank checks verify the implementation, not statistical coverage. Asymptotic percentile coverage and finite-bootstrap Monte Carlo error are separate approximations: even in an ideal continuous-percentile setting, rank 84 of 20,000 corresponds to an expected tail probability of 84/20,001 = 0.0041998, slightly above 1/240 = 0.0041667 (M: 56/20,001 = 0.0027999 against 1/360 = 0.0027778) [W], and the tail Monte Carlo relative errors are ≈ 11% (R, S*) and ≈ 13% (M). **20,000 draws do not certify 0.05 coverage.** The error control of §6.3 is **an exact event-counting argument conditional on valid individual bounds; the implemented percentile-bootstrap family error rate is nominal and includes sampling and bootstrap Monte Carlo approximation.** No conservative Monte Carlo rank treatment is adopted; the ranks above are frozen now, and no rank treatment may be selected after results are observed.

### 6.3 The 2-of-3 rule and its error control (Lemma FW; owner Q4; MD 4)
**Registered statements of the R family, per model j** (each a sign statement about a TEST mean, declared only if its bound condition holds):

| Statement | Declared iff | False iff (truth) |
|---|---|---|
| RESP_j: θ_full > 0.30 | L(Z^{V3}) > 0, Z^{V3} = (A_full − 0.30·G)1_E | μ_{V3} ≤ 0 |
| SPEC_j (if Y1 active): E[A^Y_S] < 0.10·E[A^Y_full] (a linear inequality) | U(Z^{Y1}) < 0, Z^{Y1} = (A^Y_S − 0.10·A^Y_full)1_{E_y} | μ_{Y1} ≥ 0 |
| USED_j: ψ > 0.50 | L(Z^{0.50}) > 0 and L(Z^{0.10}) > 0 | ψ ≤ 0.50 |
| PARTIAL_j: 0.10 < ψ < 0.50 | L(Z^{0.10}) > 0 and U(Z^{0.50}) < 0 | ψ ≤ 0.10 or ψ ≥ 0.50 |
| LOW_ALIGNED_j: ψ < 0.10 | U(Z^{0.10}) < 0 and U(Z^{0.50}) < 0, energy not both certified | ψ ≥ 0.10 |
| NOT_USED_j: ψ < 0.10 and η_S < η₀ | U(Z^{0.10}) < 0, U(Z^{0.50}) < 0, U(V^{abs}) < 0, U(V^{rand}) < 0 | ψ ≥ 0.10, or η_S ≥ 0.10, or E[e_S] ≥ (127/60)E[r] |
| Coarse ψ > 0.10 / ψ < 0.50 (per model, toward §3.1) | L(Z^{0.10}) > 0 / U(Z^{0.50}) < 0 | ψ ≤ 0.10 / ψ ≥ 0.50 |

with Z^c = (A_S − c·A_full)1_E, V^{abs} = (e_S − 0.10·e_full)1_E, V^{rand} = (e_S − (127/60)·r)1_E. **Category statements and coarse statements alike are declared only if RESP_j and (SPEC_j or Y1 inactive) are declared** (RC-8), and only for a model that passed every family-validity gate. The four categories are mutually exclusive (L ≤ U for the same draws; NOT_USED and LOW_ALIGNED are complementary on the energy conditions).

Coverage-failure events: F^L_{s,j} = {L(s_j) > μ_{s,j}} and F^U_{s,j} = {U(s_j) < μ_{s,j}}, each of probability ≤ α under valid individual bounds (nominal, §6.2).

**Lemma FW (scope restricted; RC-8, RC-9).** *Scope:* the explicitly registered TEST sign statements of the table (RESP_j, SPEC_j), the category propositions (USED_j, PARTIAL_j, LOW_ALIGNED_j, NOT_USED_j), the eligible coarse statements, and the overall 2-of-3 category claims built from them. Operational validity statuses (C0v, LINK, CNHS, support, N2, EXCLUDED, NUMERICAL, INC, NOT_RUN), FEAS findings, the MIXED and INCONCLUSIVE outcomes and the qualifiers are **outside** this inferential guarantee. *Statement:* for every truth state, the event "some declared R statement in scope is false" is contained in a union of at most **4 coverage-failure events per model**: at most 2 for the category and coarse statements, 1 for RESP_j, 1 for SPEC_j. Hence, conditional on valid individual bounds,

  P(any declared in-scope R statement false) ≤ 3 × 4 × α = 12α = **0.05** at α = 1/240,

and the implemented percentile-bootstrap family error rate is nominal (§6.2). A false overall 2-of-3 category claim, or a false eligible coarse statement, requires at least one false declared per-model statement, so it is covered by the same bound. No independence between models is needed (a union bound), which matters because the models share histories and bootstrap indices.

*Proof.* RESP_j is false-and-declared only on F^L_{V3,j}; SPEC_j only on F^U_{Y1,j}. On the complement of F^L_{V3,j}, any declared category or coarse statement comes with μ_{V3} > 0, hence E[A_full 1_E] > 0.30·E[G 1_E] ≥ 0, so Lemma D3 gives ψ > c ⇔ μ_{Z^c} > 0. Also E[e_full 1_E] > 0 then (A_full ≠ 0 on a set of positive probability forces e_full > 0 there, since A_full = ½dᵀC·CMΔy), so the energy statements are statements about η_S. Cases on ψ = ψ_{S,j}:
- ψ < 0.10. USED_j, PARTIAL_j and the coarse "ψ > 0.10" all need L(Z^{0.10}) > 0 > μ_{0.10}: event F^L_{Z.10}. NOT_USED_j is false only if an energy conjunct is false; fix one false conjunct s ∈ {V^{abs}, V^{rand}} (μ_s ≥ 0); declaring needs U(s) < 0 ≤ μ_s: event F^U_s. LOW_ALIGNED_j and the coarse "ψ < 0.50" are true. ≤ 2 events.
- ψ = 0.10. USED_j, PARTIAL_j, coarse "ψ > 0.10" need L(Z^{0.10}) > 0 = μ: F^L_{Z.10}. NOT_USED_j, LOW_ALIGNED_j need U(Z^{0.10}) < 0 = μ: F^U_{Z.10}. ≤ 2.
- 0.10 < ψ < 0.50. USED_j needs L(Z^{0.50}) > 0 > μ_{0.50}: F^L_{Z.50}. NOT_USED_j, LOW_ALIGNED_j need U(Z^{0.10}) < 0 < μ_{0.10}: F^U_{Z.10}. PARTIAL_j and both coarse statements are true. ≤ 2.
- ψ = 0.50. USED_j: F^L_{Z.50}. PARTIAL_j, LOW_ALIGNED_j, NOT_USED_j and coarse "ψ < 0.50" need U(Z^{0.50}) < 0 = μ: F^U_{Z.50}. ≤ 2.
- ψ > 0.50. PARTIAL_j, LOW_ALIGNED_j, NOT_USED_j and coarse "ψ < 0.50" need U(Z^{0.50}) < 0 < μ: F^U_{Z.50}. ≤ 1.
Summing over the 3 models with the union bound gives ≤ 3·(2 + 1 + 1)α. A false 2-of-3 claim "category C holds in ≥ 2 models" needs ≥ 2 declared C_j while fewer than 2 are true, so at least one declared C_j is false. ∎

**Remarks.**
1. *Relation to the comparison's 0.05/6* (CMP §3.9): that allocation counts the two ψ tails in three models. Lemma FW adds the response and specificity statements that every licence uses. The energy conjuncts cost nothing: they can only be falsely passed in the region where the ψ statements contribute one event.
2. If Y1 is inactive, the bound is 9α = 0.0375 < 0.05 (conservative; α is not re-allocated).
3. **SPEC_j licenses only the registered linear inequality (RC-7):** "the mean signed placebo contribution is below 0.10 times the mean full placebo contrast." It is one-sided: a large negative placebo contribution passes, and cancellation and orthogonal output changes are untested. No population placebo-ratio claim is made, because the positivity of the placebo denominator is established only by the nominal VAL gate V3y, which is not one of the controlled TEST statements. Stronger specificity (positivity, two-sided or energy-based placebo conditions) would need preregistration and a recount of the error events; none is added.
4. **C2-M (Lemma FW-M).** Per model: the transmission statements "τ_M > 0.10" (declared iff L(Z_τ) > 0, Z_τ = (A_M,F − 0.10·A_full)1_E; the precondition of every M category) and "τ_M < 0.10" (ROUTED_AROUND; U(Z_τ) < 0) contribute ≤ 2 events (both only at τ_M = 0.10 exactly); the categories (as R with Z_M^c = (A_M,S − c·A_M,F)1_E and the single energy conjunct V_M = (e_M,S − 0.10·e_M,F)1_E) ≤ 2; Y2 1; RESP_j (shared V3x, recomputed in the M stream) 1. Total ≤ 6 per model, 18α = 0.05 at α = 1/360, conditional on valid bounds. The same proof applies, with Lemma D3 for ψ_M on the event that "τ_M > 0.10" is true. ROUTED_AROUND is in scope only as the restricted signed-effect statement τ_M < 0.10 (RC-5).
5. **C2-S\*** is structured exactly as R: 12α = 0.05 at α = 1/240.
6. **Families are controlled separately (O-3, adopted).** Each family has its own nominal 0.05: R is uniquely primary, M and S* are explicitly secondary. The study-wide nominal union bound over the three families is 0.15, and it is displayed wherever combined study conclusions are discussed. No claim combines families, and the favourable family is never selected as "the answer" (stop rule S10). The rotation arm, the variants, the Haar frames, the operator decomposition and every descriptive interval are outside all families. O-3 is confirmed by owner addendum 21 (§18 item 4).
7. **TEST validity rechecks (review, data discipline).** Rechecking validity on TEST (T-PRE) can suppress declarations without invalidating the unconditional union-bound containment argument above. It does not provide coverage *conditional* on having passed those TEST gates.
8. **NEGATIVE_ALIGNED_CONTRIBUTION** (U(E[A_S 1_E]) < −g_s at α_F) is a reported qualifier outside the Lemma FW allocation; its nominal per-statement level is α_F, and it never changes a category.

### 6.4 Per-model rules
**R (and S\*), for each model j that is R-ok after VAL and T-PRE:**
1. If RESP_j is not declared → EXCLUDED_j/MODEL_HEADROOM (TEST_GATE).
2. If Y1 is active and SPEC_j is not declared → EXCLUDED_j/NUISANCE_IN_S (TEST_GATE).
3. A bound inside its NUM guard (§9.2) counts as neither > 0 nor < 0.
4. The category of the §6.3 table that is declared (USED_j, PARTIAL_j, NOT_USED_j, LOW_ALIGNED_j); else INC_j, recorded as INC_j/NUMERICAL if a guard hit is what left it undeclared.
5. Qualifier NEGATIVE_ALIGNED_CONTRIBUTION(j) if U(E[A_S 1_E]) < −g_s (after rule 1 passes), whatever the category.
A model that is not R-ok (excluded before ACCEPT) has its R endpoint NOT_RUN (§3.1).

**M, for each model j that is M-ok:**
1. RESP_j as R (in the M stream); 2. Y2 as SPEC_j; 3. NUM guard;
4. ROUTED_j if U(Z_τ) < 0;
5. else, if L(Z_τ) > 0: UPSTREAM_USED_j iff L(Z_M^{0.50}) > 0 and L(Z_M^{0.10}) > 0; UPSTREAM_PARTIAL_j iff L(Z_M^{0.10}) > 0 and U(Z_M^{0.50}) < 0; UPSTREAM_NOT_USED_j iff U(Z_M^{0.10}) < 0, U(Z_M^{0.50}) < 0 and U(V_M) < 0; UPSTREAM_LOW_ALIGNED_j iff the first two hold and the third does not; else INC_j;
6. else INC_j;
7. NEGATIVE_ALIGNED_CONTRIBUTION(j) if U(E[A_M,S 1_E]) < −g_s;
8. after the M outcome is recorded, the descriptive circle, complement, interaction and energy quantities of §2.10 for every M-ok model, ROUTED_j included (seed 620518).

### 6.5 Overall rules (2 of 3; owner Q4; RC-13)
**Reading of Q4 (confirmed by owner addendum 21, §18 item 3):** all three models receive the preregistered validity assessment and are reported. Failed validity gates can leave scientific endpoints NOT_RUN. Two valid, resolved models can support a two-of-three claim; no claim is made about the excluded model.

For R (and S*, M with their category names):
1. A study-level validity failure → FAIL_TECHNICAL/<class> or INCONCLUSIVE/<reason>.
2. Fewer than 2 models left after a per-model validity gate → INCONCLUSIVE/<that gate's reason> (with CIRCLE_NOT_HISTORY_SENSITIVE if ≥ 2 models are CNHS_j).
3. ≥ 2 USED_j → USED. ≥ 2 NOT_USED_j → NOT_USED. ≥ 2 PARTIAL_j → PARTIAL. ≥ 2 in {NOT_USED_j, LOW_ALIGNED_j} (and < 2 NOT_USED_j) → LOW_ALIGNED_SHARE. (M: ≥ 2 ROUTED_j → ROUTED_AROUND, checked first.) These are mutually exclusive because the per-model categories are, and 2 + 2 > 3.
4. Else, ≥ 2 models with a non-INC category → MIXED; else INCONCLUSIVE/PRECISION.
5. Qualifiers (§3.1) appended; every per-model status and endpoint status (including NOT_RUN) listed.

### 6.6 Validation and feasibility gate statistics
- **C0v (FEAS, per model; C1′ rule unchanged).** `c1_chart.c0_val(prod_j, gauge_j, X_FEAS512, direct_j, cfg)` with direct_j = `fit_chart_lcc` on the natural `resid_post_3`/32 activations of the 512 lowest-sequence-id FEAS rows (landmark ids as the C1′ CONTRACT rule). PASS iff support ≥ 507/512 (`100·n_sup ≥ 99·512`), fidelity ≥ 0.80, every one of 12 bins ≥ 8 rows, overall resultant ≤ 0.30; and Sup(FEAS) ≥ 0.99 over all FEAS natural rows. Else EXCLUDED_j/CHART_UNAVAILABLE (R and M).
- **L1 link (FEAS, per model; incremental over a baseline decoder; RC-3).** Three frozen decoders of the target f₁(φ) = (cos φ, sin φ), identical except for the features:
  - **D0** on [onehot(w32), z̃] (36 + 5 = 41 features; the baseline);
  - **D_code** on [onehot(w32), z̃, L_B y] (36 + 5 + 6);
  - **D_lin** on [onehot(w32), z̃, y] (36 + 5 + 127).
  - *FIT procedure and standardisation (explicit; the C1′ `c1_fit.fit_decoder` recipe without the RFF map).* For each decoder, F = its FIT feature matrix (8192 rows). (1) λ* from `x4f_probe.nested_ridge(F, Y, panel_FIT, F, Y, grid=(1e-3, 1e-2, 1e-1, 1.0, 10.0))`: leave-one-panel-out over the 8 FIT panels, ties to the larger λ. **`nested_ridge` standardises its features internally** (`x4f_scores.standardizer` on the fold's fit rows: mean and population SD, scale 1 for SD ≤ 1e-12), centres them and solves by Cholesky. (2) **`RidgeProbe` does not standardise**, so the frozen decoder is built on explicitly standardised features: (μ_F, s_F) = `x4f_scores.standardizer(F)` over all FIT rows, F̃ = (F − μ_F)/s_F, `RidgeProbe([λ*]).fit(F̃, Y, F̃, Y)` (a singleton grid, so the validation arguments select nothing). (3) Its FIT predictions must equal `nested_ridge`'s `pred_val` within `c1_fit.equivalence_tolerance` (max(1e-10, 64·eps·κ·‖pred‖_∞), the R13 rule); failure → EXCLUDED_j/NUMERICAL. (4) FEAS (and TEST) rows are standardised with the FIT (μ_F, s_F) and predicted by the frozen probe. z̃ is the FIT-standardised nuisance (§2.4) before this column standardisation.
  - *Scores (FEAS natural rows).* SSE_X = Σ_i‖f₁(φ_i) − D_X(i)‖², X ∈ {0, code, lin}, and

    R²_code|0 = 1 − SSE_code/SSE_0,  ρ_inc = (SSE_0 − SSE_code)/(SSE_0 − SSE_lin).

  - **PASS iff SSE_0 > 0, SSE_0 − SSE_lin > 0, R²_code|0 ≥ 0.50 and ρ_inc ≥ 0.90** (the provisional 0.50/0.90 thresholds, frozen before data, O-1). An undefined or nonpositive denominator (SSE_0 ≤ 0 or SSE_0 − SSE_lin ≤ 0) is a LINK failure. Failure → EXCLUDED_j/LINK.
  - *Why incremental.* D_code and D_lin both receive the symbol indicators and the oracle nuisance covariates, and those covariates can predict the phase. A high complete-decoder score therefore does not show that the moved coordinates supply the information: sufficiently predictive nuisance covariates can make both complete decoders pass even when the code adds little (independent fixture, §13.3 T-L1). R²_code|0 measures the code's reduction of the baseline error; ρ_inc measures the fraction of the best linear decoder's improvement over the baseline that the code achieves.
  - *Why both sides are fitted decoders (kept from v1).* Comparing a raw GLS estimate f̂₁ = L_B y with a shrinkage decoder fails a valid code: in a scalar Gaussian model with noise-to-signal ratio ρ, R²(f̂) = 1 − ρ while R²_lin = 1/(1 + ρ), so their ratio is 1 − ρ², below 0.90 for ρ > 0.316 even when the code holds all of the circle's linear information. With every side fitted by the same procedure, pure noise creates no gap.
  - *What the ratio measures.* Under the within-class Gaussian linear model with col(B) Σ_ε-orthogonal to col(Γ), [w, z̃, L_B y] is linearly sufficient for f (the best linear predictor depends on y only through BᵀΣ_ε⁻¹(y − α_w − Γz̃), by the Woodbury identity), so SSE_code = SSE_lin and ρ_inc = 1 in population. ρ_inc < 0.90 means more than 10% of the linearly decodable improvement over the baseline lies outside the moved code. **These remain operational decoder comparisons, not guarantees that every predictive phase encoding was captured** (Q-CODE).
  - *The 0.50 floor:* a code that removes less than half of the baseline decoder's error on the circle coordinate is not called the circle's code.
  - Reported descriptively: the v1 complete-decoder scores R²_X = 1 − SSE_X/Σ_i‖f₁(φ_i) − f̄₁,w(i)‖² (f̄₁,w: FIT class means) for X ∈ {0, code, lin} and the ratio R²_code/R²_lin; an RFF decoder of f₁ from P_rest y (X4-F: linear erasure left RBF recoverability at 0.998; nonlinear residues cannot affect the linear head except through linear functionals, which A_rest counts exactly).
- **R1 registration (FEAS, E_x rows, per model).** φ_c(y) = atan2 of the first-harmonic pair of f̂ = L_B(y − α̂_{w32}) (L_BΓ = 0, so z̃ does not enter; both arms use their shared class mean). `c1_gates.v1(phi_p = φ_c(y⁺), phi_m = φ_c(y⁻), m32_p = m32(H⁺), m32_m = m32(H⁻))`: δ_c = wrap(φ_c(y⁺) − φ_c(y⁻)), δ* = wrap(arg m32(H⁺) − arg m32(H⁻)); zero and unresolved moduli handled deterministically, with the overrides applied to v1's inputs before its median selection and agreement calculation (§2.11, NEW-3); among rows with |δ*| ≥ med* (`inverted_cdf` median), the fraction with sign δ_c = sign δ* ≠ 0; **PASS iff ≥ 0.75** (C1 §10.1 V1 kept: 0.5 is chance; 0.75 is a strong majority on the informative half). This is the requirement that the circle code moves with the counterfactual (MD 3). Failure after L1 PASS → CNHS_j, with the RC-8 licence: an assay-registration finding; failing to reach 75% does not establish absence of history sensitivity. Reported: the chart-phase V1 of C1 (φ(a⁺) against φ(a⁻)) and κ_reg = Σδ_c·sign δ*/Σ|δ*|.
- **N2 (FEAS; M).** The radial support screen of §2.10. Failure → EXCLUDED_j/RADIAL_SUPPORT (M only).
- **L1-2, R1-2 (FEAS; M), L1*, R1* (FEAS; S\*).** The same statistics at layer 2 (D0 on [onehot, z̃]; D_code on [onehot, z̃, L_{B₂}a₂]; D_lin on [onehot, z̃, a₂], 36 + 5 + 128) and with φ* in place of φ (D_code on [onehot, z̃, L_{B*}y]; every L1* decoder uses the masked target f*_1 ∈ ℝ², §2.11, NEW-3).
- **V3x (VAL).** Z = A_full − 0.30·G (`c1_endpoint.Zfull_hat`, with d in named order, §2.3) on VAL E_x rows; `bootstrap_means` seed 620504, 5000 draws; PASS iff L_{0.05/3} > g (§9.2). Failure → EXCLUDED_j/MODEL_HEADROOM (all families). *Why 0.30* (C1 V3 kept): ψ is a share of the model's response; below 0.30 of the oracle's own discrimination the "response" is too weak for a share to mean much. E2's recorded capture 0.985–0.986 suggests θ_full ≈ 0.9 [H, E2 summary via L§11].
- **V3y (VAL).** The same on E_y rows with y-pair quantities, seed 620508. Failure makes Y1, Y1* and Y2 inactive (qualifier SPECIFICITY_NOT_ESTABLISHED); it excludes no model.
- **Y1 (VAL; R; active iff κ_m < 0.01 and V3y PASS).** Z = A^Y_S − 0.10·A^Y_full on VAL E_y rows; seed 620509; PASS iff U_{0.05/3} < −g. Failure → EXCLUDED_j/NUISANCE_IN_S (R only). *What it licenses (RC-7):* only the registered linear inequality "the mean signed placebo contribution is below 0.10 times the mean full placebo contrast"; 0.10 is the study's single negligibility threshold. It does not establish general nuisance exclusion, a small placebo-effect magnitude, or the absence of a subspace illusion. Y1* (S*, seed 620515) likewise.
- **Y2 (VAL; M).** Activity: κ_m < 0.01, V3y PASS, and L_{0.05/3}(E[(A^Y_M,F − 0.10·A^Y_full)1_{E_y}]) > g (seed 620510). If active: PASS iff U_{0.05/3}(E[(A^Y_M,S − 0.10·A^Y_M,F)1_{E_y}]) < −g (seed 620510); the same RC-7 restriction. Failure → EXCLUDED_j/NUISANCE_IN_S (M only).

### 6.7 Precision ladder P1 (VAL; outcome-blind; C1 §12.4 pattern)
**What P1 powers (RC-15).** P1 powers the specified R/S* threshold contrasts (Z^{0.10}, Z^{0.50}) and the M transmission contrast (Z_τ) only. It does not power the primary M classification ψ_M (whose arrays need the sealed mean of A_M,F for an alternative), the energy conjuncts (V^{abs}, V^{rand}, V_M) or the NEGATIVE qualifier. The M-share MDEs (Z_M^{0.10}, Z_M^{0.50}) and the energy MDEs are reported at VAL and not gated, and those outcomes **may remain unresolved at the maximum sample size N = 16,384**. No assumption is made that patched-forward variance is no greater than natural-pair variance.

For each family F and each F-ok model, indicator-form VAL arrays over all 4096 VAL rows: R and S*: Z^{0.10}, Z^{0.50}; M: Z_τ only. `precision.sd_b4_draws(X = {j: arr_j}, r4n = {j: (A_full·1_E)_j}, models, seed_SD, draws 5000, size 4096)`; for N ∈ (4096, 8192, 16384): `precision.centered_draws(X, models, seed_centred, 5000, size N)` and `precision.precision_summary(sd, e, models, cfg)` with cfg = {alpha: α_F, power: 0.80, delta: 0, alternative: 0.10·min_j mean_VAL(A_full·1_E)_j, projected_N: N}. Every array of a model must PASS for the model to pass at N. The alternative is "ψ (or τ_M) lies 0.10 beyond the threshold": E[Z^c 1_E] = (ψ − c)E[A_full 1_E]. mean(A_full 1_E) is a V3 gate quantity, not an endpoint, so using it leaks nothing about ψ.
- N_F = the smallest N at which every F-ok model passes; else the smallest N at which ≥ 2 F-ok models pass (the others PRECISION_LIMITED(j)); else F → INCONCLUSIVE/UNDERPOWERED (F stops).
- **N_test = max of N_F over the families still alive; k = N_test/4096 ∈ {1, 2, 4}.** One fresh sample serves every family.

### 6.8 Power and precision [H, with W sources]
**Recorded inputs [W, jobs/0041, identical donor construction and process]:** Ḡ_val = 1.12874 nat (range 0.0712–3.6965; 0.05 lower bound 1.12464); f_val = 0.98584 (4,038/4,096); κ_ν = 0.0093195; s_max = 7.878. C2 draws new histories from the same law, so the same magnitudes are expected. [H] θ_full ≈ 0.9 (E2 capture 0.985), so E[A_full·1_E] ≈ 0.985 × 0.9 × 1.13 ≈ 1.0 nat.

**Half-width of a one-sided bound, in ψ units, at α = 1/240** (hw = 2.6383·SD(Z)/√N ÷ E[A_full 1_E]; SD(Z) ≲ SD(A_S) + c·SD(A_full) ≲ 1 nat [H, L§11]):

| N_test | SD 0.5 | SD 1.0 | SD 1.5 | P(INC_j) under a flat prior on ψ ∈ [0, 1] at SD 1.0 (≈ 4·hw) |
|---|---|---|---|---|
| 4,096 | 0.021 | 0.041 | 0.062 | ≈ 0.165 |
| 8,192 | 0.015 | 0.029 | 0.044 | ≈ 0.117 |
| 16,384 | 0.010 | 0.021 | 0.031 | ≈ 0.082 |

**P1 pass condition [W given SD]:** mde = (z_{1−α} + z_{0.80})·SD/√N must be ≤ 0.10 nat; at α = 1/240, z + z = 3.4799, so N = 4,096 passes for SD ≤ 1.84 nat, 8,192 for SD ≤ 2.60, 16,384 for SD ≤ 3.68 (M transmission, α = 1/360: 1.77, 2.50, 3.54). k = 1 or 2 is expected [H].

**Energy.** SD(V^{abs}), SD(V^{rand}) are unknown [H]; their MDEs are reported at VAL (not gated). If they are large, NOT_USED may be unreachable and a small-ψ result is reported as LOW_ALIGNED_SHARE: this is the conservative direction.

**C2-M [H].** The variance of the patched-forward contrasts is unknown and is not assumed to be no larger than the natural-pair variance; τ_M is unknown, and a small τ_M lowers the precision of ψ_M (INC_j more likely). The M-share outcome may remain unresolved at N = 16,384.

---

## 7. Gates in exact order

Conventions (C1 §16 kept): `c1_records.run_c1_gate` and `classify_exception` taxonomy; FAIL_TECHNICAL for identity, lineage and integrity defects; INCONCLUSIVE/<reason> for unmet valid criteria; inequalities exactly as written. **Scope** says what a failure stops: *study* (every family stops; values kept), *model* (the model is excluded from the named families' claims, its endpoint in those families has the status of §3.1 (NOT_RUN/<gate>; SEALED_UNSCORED only for arrays already lawfully formed), and it keeps its reported status; a family continues while ≥ 2 of its models remain, otherwise it stops with that gate's status), *family*. Execution is by separate coordinator-dispatched jobs, each reviewed before the next; every local job is metered (measure-only), runs in the clean execution worktree at H (§13.4), with TEMP/TMP/TMPDIR and pytest basetemp under `X:/Downloads/topo-scratch/<job>/`.

| # | Stage / job | Gate | Content | Threshold / tolerance | On failure | Scope |
|---|---|---|---|---|---|---|
| 0 | IMPL | IMPL | `API.md` committed first (including the frozen registry source and exclusion inventory, O-7); tests A/B written before the modules (§13.3); modules ≤ 400 lines; full suite run detached by the coordinator; code freeze H | §13 | S14 | study |
| 0b | owner → S1 | AUTH-ADMIT | Owner addendum naming the frozen protocol sha256 and the budget, present before any S1 execution; recorded as `AUTH.json` | exact | do not run (S1) | study |
| 1 | S1 | G0 AUTHORITY | (i) frozen protocol sha256 and byte copy `tools/c2_readout/PROTOCOL_C2_v2.md`; (ii) `tools/c2_readout/CONTRACT.json` sha256 (it carries the §4 `state_sha` strings); (iii) every reused file's blob sha256 at H equals §13.1; (iv) K4 FREEZE `e3049fee…c94a` and the kernel blobs; C1′ CONTRACT `f8df2e43…a379`; (v) the three chart NPZ sha256 (§2.4); (vi) namespace admission for `c2-v1` (§5.2, RC-11: unrelated or superseded lineage absent; pinned code/configuration and recognised lineage records permitted; no prior scientific data before first sampling; exact manifests and hashes on continuation); (vii) store absent or lineage-recognised (§11 item 7); (viii) dispatch identities, release, meter binding sha256 and import directory | exact | FAIL_TECHNICAL | study |
| 2 | S1 | PF | Unchanged suites `tests/{learner, dataset, contracts, oracle, process, world, analysis, prediction, experiment, circle_history, c1prime, c1prime_registry}` and the new `tests/c2_readout`; `tools/check_file_sizes.py` (passes iff no report line names a file under `tools/c2_readout/` or `tests/c2_readout/`; lines naming other files are recorded as pre-existing, with their line counts; E-0102-2, coordinator addendum 2); `tools/check_imports.py`; TEMP and basetemp outside the root recorded | all pass | FAIL_TECHNICAL | study |
| 3 | S1 | H1 IDENTITY | C1 H1 unchanged: artifact IDs equal the CONTRACT; `validate_process`; perms are permutations; round trip; E_canon bitwise identical across the three models. **SYMBOL-ORDER (RC-1; static part, NEW-2):** per model, (b) `named_from_canonical(e_c, perm) = e_{perm[c]}` for every canonical c (bitwise). Check (a) runs at H2 and check (c) at H3, after their data exist (NEW-2) | exact | FAIL_TECHNICAL/IDENTITY | study |
| 4 | S1 | REG | Registry R (§5.3 a–e) complete, digests and union sha256 recorded | complete | INCONCLUSIVE/REGISTRY_INCOMPLETE | study |
| 5 | S1 | H2 SEPARATION | Sample FIT (2 blocks), FEAS, VAL (only after REG passes); `check_disjoint`; U_FIT, U_FEAS, U_VAL pairwise disjoint and disjoint from R over the roles H, H⁺, H⁻ and H^Y (where defined); `first_token_ok` per block. **Then SYMBOL-ORDER (a) (RC-1, NEW-2):** per model, the named input tokens are perm[w] of the canonical symbols on every FIT row | 0 collisions; (a) exact | FAIL_TECHNICAL/LINEAGE; (a): FAIL_TECHNICAL/IDENTITY | study |
| 6 | S1 | H3 ORACLE | τ: C1′ H3 unchanged (`symmetry_report` ≤ 1e-14 and exact T/π invariance; closed form within t + t²; named = canonical ≤ 4e-12; cross-model G ≤ 1e-12). H^Y (no symmetry, §2.2): no symmetry report, closed form or ε_sym bound applies. The H^Y oracle quantities are the exact oracle forward (`BayesFilter`) on the H^Y tokens, checked by the Decimal reference rows below; named = canonical and cross-model G apply to G_y as to G_x. Decimal reference (`decimal_reference`, `h3_compare`) on the 4 lowest-id eligible rows of FIT, FEAS and VAL for H, H⁺, H⁻ and H^Y (for H^Y, the 4 lowest-id E_y rows): posterior and predictive 2e-12 relative (interval rule off the fast path), surprisal 1e-10, \|Ĝ − G̃\| ≤ 2e-11·(1 + max_v\|λ̂_v\|). \|Σ_v q_v − 1\| ≤ 1e-12 on every row. **Then SYMBOL-ORDER (c) (RC-1, NEW-2):** after the FIT oracle contrasts are constructed, `canonical_from_named_cols(named_from_canonical(x, perm), perm) = x` bitwise on the FIT d arrays | T1–T8; (c) bitwise | FAIL_TECHNICAL/ORACLE (INCONCLUSIVE/NUMERICAL if undetermined); (c): FAIL_TECHNICAL/IDENTITY | study |
| 7 | S1 | H4 ELIGIBILITY | f_x ≥ 0.90 and f_y ≥ 0.85 on FIT, FEAS, VAL (OFF_GRID_Y rows count as ineligible for f_y; owner addendum 23); coverage tally (§5.5) | 0.90 (f_x); 0.85 (f_y) | INCONCLUSIVE/ELIGIBILITY | study |
| 8 | S1 | H5 HEADROOM | VAL: lower 0.05 bound (seed 620505, 5000 draws, rank 250) of mean G_x over E_x > 0.01 nat **and** of mean G_y over E_y > 0.01 nat; freeze s_max, κ_ν, κ_m (`ORACLE_FROZEN.json`) | 0.01 nat | INCONCLUSIVE/HEADROOM | study |
| 9 | S2 | M0 MODEL | Per model: checkpoint IDs and EmissionSpecs equal the CONTRACT; float32 `state_sha` equals the §4 value (full 64-hex strings from the C1′ M0 record; RC-16); float64 round trip bitwise; identity patch bitwise at `ln_final_out`, `resid_post_2` and `resid_post_3` on the 1024 lowest-id FIT rows; rank(diag(γ)N₁) = 127 (min\|R_ii\| > 1e-8·max\|R_ii\|); readout identity ‖z − (W_Uβ + My)‖_∞ ≤ τ_X1 on those rows; SYMBOL-ORDER two-route check on those rows (NEW-7): with s_named = ½d_namedᵀz, s_canonical = ½d_canonicalᵀz_canonical and z_canonical = `canonical_from_named_cols`(z, perm), per row \|s_named − s_canonical\| ≤ 1e-12·max(1, Σ_v\|d_canonical,v z_canonical,v\|) (summation order only; T18); preliminary X1 attainability κ_X1 ≤ 1.76e3 | T9, T10, T18 | FAIL_TECHNICAL/MODEL; INCONCLUSIVE/NUMERICAL (attainability) | study |
| 10 | S2 | C0c CHART | NPZ sha256 equal §2.4 (else FAIL_TECHNICAL, study); `chart_from_arrays`; Sup(FIT) ≥ 0.99 (`extend.supported` over all FIT natural rows) | 0.99 | EXCLUDED_j/CHART_UNAVAILABLE | model (R, M) |
| 11 | S2 | F1 FIT | Per model and projector (P_S; P₂; P_S*; Euclidean; K = 1, 2): FWL design rank = 36 + 5 + 2K (43, 45, 47; RC-12); cond(design) ≤ 1e8; σ_max(B) > 0 and σ_min(B)/σ_max(B) ≥ 1e-6; Ledoit–Wolf λ_min > 1e-12·λ_max; **whitened nuisance-plus-code design X̃ (Euclidean variant: X_n itself, NEW-1): numerical rank = 5 + 2K (7, 9, 11) and cond₂(X̃) ≤ 1e8** (RC-10, RC-12); the GLS identities (Lemma G1) in the scale-invariant form of §2.5, on every problem (dimensionless identities ≤ 1e-10 absolute; ‖P_SΓ‖_max ≤ 1e-10·‖Γ‖_max and ‖P_ΓB‖_max ≤ 1e-10·‖B‖_max; whitened symmetry ‖P̃ − P̃ᵀ‖_max ≤ 1e-10; D-0104-2); GLS-REF reference accepted (80-digit `Decimal`; no trap, verified θ̄_A < 1, θ̄_G < 1 and ρ_ref = e_L/‖L*‖_F ≤ 1e-20 by Lemma GR; NEW-1) and ‖P̂ − P*‖_F + ε*_P ≤ 1e-8·‖P*‖_F (§2.5); L1 decoder equivalence (RidgeProbe vs `nested_ridge`, `equivalence_tolerance`) | T11–T14, T17 | Primary (P_S, P₂, P_S*): EXCLUDED_j/PATCH_MODEL_DEGENERATE (ranks, conds, σ) or EXCLUDED_j/NUMERICAL (identities, GLS-REF, decoder equivalence). Variant: that qualifier NOT_COMPUTED | model (family of the projector) |
| 12 | S3 | C0v CHART | §6.6 on FEAS (3 direct constructions, ledger limit 3) | 507/512, 0.80, 8, 0.30, 0.99 | EXCLUDED_j/CHART_UNAVAILABLE | model (R, M) |
| 13 | S3 | L1 LINK | §6.6 (R: L1; M: L1-2; S*: L1*): D0, D_code, D_lin on FEAS; incremental scores | SSE_0 > 0, SSE_0 − SSE_lin > 0, R²_code\|0 ≥ 0.50, ρ_inc ≥ 0.90 | EXCLUDED_j/LINK | model (that family) |
| 14 | S3 | R1 REGISTRATION | §6.6 (R1, R1-2, R1*) on FEAS E_x rows; zero-modulus rule §2.11 | 0.75 | CNHS_j (licensed as an assay-registration finding) | model (that family) |
| 15 | S3 | N2 RADIAL SUPPORT | §2.10 (M only; a radial support screen) | max(0.05, F(D₂) + 0.02) | EXCLUDED_j/RADIAL_SUPPORT | model (M) |
| 16 | S3 | SURVIVAL | Each family needs ≥ 2 ok models; ≥ 2 CNHS_j → CIRCLE_NOT_HISTORY_SENSITIVE (CNHS-2, X_PHASE_NOT_HISTORY_SENSITIVE) | 2 of 3 | family stops | family |
| 17 | S4 | X1 READOUT IDENTITY (ephemeral, §5.7) | Every VAL eligible row: natural arms and the R interchange arms y_S^{2←1}, y_S^{1←2} for the x and y pairs; S*, the three qualifier projectors (x and y pairs) and rotation arms on the 1024 lowest-id eligible rows (Lemma X). Only identity diagnostics retained | τ_X1 | FAIL_TECHNICAL | study |
| 18 | S4 | V3x, V3y | §6.6 | L > g | V3x: EXCLUDED_j/MODEL_HEADROOM (all families). V3y: Y1/Y1*/Y2 inactive, SPECIFICITY_NOT_ESTABLISHED | model |
| 19 | S4 | Y1, Y1*, Y2 | §6.6 (if active) | U < −g | EXCLUDED_j/NUISANCE_IN_S | model (that family) |
| 20 | S4 | P1 PRECISION | §6.7 → N_F per family, N_test, k | §6.7 | INCONCLUSIVE/UNDERPOWERED (family) or PRECISION_LIMITED(j) | family |
| 21 | — | ACCEPT | Coordinator's independent review of the S1–S4 gate report with the sealed means unopened; release R5 names N_test and k | — | stop | study |
| 22 | S5 | REG′ / H2′ | R′ = R ∪ U_FIT ∪ U_FEAS ∪ U_VAL; sample k TEST blocks once; U_TEST ∩ R′ = ∅; `first_token_ok`; then SYMBOL-ORDER (a) on every TEST row (NEW-2) | 0 collisions; (a) exact | FAIL_TECHNICAL/LINEAGE; (a): FAIL_TECHNICAL/IDENTITY | study |
| 23 | S5 | T-PRE (study) | In this order: H1 (static checks with SYMBOL-ORDER (b)); the TEST oracle, then H3 on the 4 lowest-id eligible TEST rows with SYMBOL-ORDER (c) on the TEST d arrays (NEW-2); \|f_x,TEST − f_x,VAL\| ≤ 0.02 and \|f_y,TEST − f_y,VAL\| ≤ 0.02; H5 on TEST (seed 620506); M0 identity patch bitwise on the 1024 lowest-id TEST rows; **X1 on every TEST eligible row as an ephemeral integrity operation inside T-PRE** (RC-13: it forms the prescribed replacements and compares logits, retains only identity diagnostics, and forms, retains or releases no endpoint array or summary) | as above | INCONCLUSIVE/TEST_GATE (endpoints NOT_RUN/T-PRE; gate and integrity data retained; NEW-6); FAIL_TECHNICAL for identity, lineage or X1 | study |
| 24 | S5 | T-PRE (model) | Sup(TEST) ≥ 0.99; L1, R1 (and L1-2, R1-2, L1*, R1*) with the frozen FIT decoders; N2 (M) on TEST rows | as at FEAS | EXCLUDED_j/TEST_GATE (endpoint NOT_RUN/T-PRE; NEW-6) | model |
| 25 | S5 | RESP / SPEC | First part of each family stream (seeds 620503, 620513, 620516): RESP_j (V3x at α_F), SPEC_j (Y1, Y2, Y1* if active) | §6.3 | EXCLUDED_j/MODEL_HEADROOM or NUISANCE_IN_S (endpoint NOT_RUN/<gate>: the model's endpoint arrays are not formed; NEW-6) | model |
| 26 | S5 | NUM | Every bound used in a decision clears the guard g_s (§9.2) | §9.2 | INC_j/NUMERICAL for the affected statement | model |
| 27 | S5 | ENDPOINT | §6.3–§6.5 for R, M, S* on the admitted models; qualifiers (variants on the R stream; NEGATIVE_ALIGNED_CONTRIBUTION); rotation arm (seed 620517, report) | §6 | outcome | family |
| 28 | S5 | REPORT | Licence fill (§3, with Q-CODE); unseal the VAL endpoint values (reported as secondary); every per-model status and endpoint status (NOT_RUN included); coverage tally; descriptives (§2.12; C2-M descriptives after the M outcome, seed 620518, §2.10); POST-DESC for NOT_RUN models or families, after every family outcome is recorded (§5.7, NEW-6); the 0.15 study-wide union bound beside any combined discussion | — | — | — |

**Computation order inside the stages** follows §5.7. **Gate order is enforced (NEW-2):** no check uses FIT tokens before they are sampled at H2, and none uses oracle contrasts before they are constructed at H3. No FIT sampling moves ahead of REG. The driver refuses a gate run out of order (§13.3 T-POLICY). A family stopped at gate 16 or 20 is not scored at S5 (its endpoints NOT_RUN), but its gate values and per-model statuses are reported; the fresh stage runs if any family is alive.

**Y-donor preparation.** Within H2 and H2′, after REG or REG′ has passed and the natural histories have been sampled, run the pinned natural-history oracle sufficiently to obtain b31(H). Cache that result for H3. Use b31(H) only to determine k_Y(H), identify Y_def, and construct the defined H^Y donors. Complete separation over all defined donor roles before proceeding. Donor contrasts and scientific statistics are constructed at H3; no fitting or model-output evaluation is permitted during this preparation. H3 validates the cached natural-history oracle results as well as the donor results. Add an ordering fixture covering this dependency.

---

## 8. Stop rules

| Rule | Trigger | Action |
|---|---|---|
| S1 | No owner AUTH addendum (gate 0b) | Nothing executes. Planning, implementation and static review may precede AUTH |
| S2 | G0 or PF fails | FAIL_TECHNICAL; nothing runs |
| S3 | Any change to a threshold, tolerance, seed, grid, K, covariate set, projector, site, donor step, chart, split size or family structure after any C2 data exist | Forbidden. Reviewer changes happen only before S1. A post-data change needs an **owner** decision (addendum 10; the R13 precedent), never a coordinator ruling alone |
| S4 | A study-scope gate fails | Every family stops at that gate; all values kept (B5) |
| S5 | A model-scope gate fails | The model is excluded from that family's claims; its endpoint in that family is NOT_RUN/<gate> (SEALED_UNSCORED only for arrays already lawfully formed; NEW-6); its status and values are kept and reported; the family continues iff ≥ 2 of its models remain, otherwise it stops with that gate's status |
| S6 | Any refit, redraw or substitution (chart, frame, donor, projector, covariate, site, rows) | Forbidden; frames are never redrawn; no fallback chart |
| S7 | A technical defect | Correction route of §11 (at most 2 correction jobs per defect) |
| S8 | TEST shortfall or a T-PRE failure | No replenishment of fresh rows. An endpoint not yet formed is NOT_RUN/<gate> and is never computed to fill a sealed array. Arrays already lawfully formed are SEALED_UNSCORED. Descriptive values come only from POST-DESC, after every family outcome is recorded (§5.7, NEW-6) |
| S9 | Identity, lineage or numerical-integrity mismatch | Stop before any classification |
| S10 | Cross-family influence | C2-R, C2-M and C2-S* never change each other's outcomes; all are frozen before S1 and scored in the same fresh stage; no claim combines families; no family is selected as "the answer" |
| S11 | Owner STOP, a usage limit, a disk floor (C: < 2 GB, X: < 30 GB), a latch | INVALID (interrupted); an environment rerun under the same specification must reproduce identical values (§11 item 5) |
| S12 | Leakage: a TEST token before ACCEPT; a FEAS logit; a FIT logit outside the M0 rows; any opening of sealed values before the fresh outcome; X1 retaining an endpoint array or summary; latent states stored | INVALID (leakage) |
| S13 | A result would change a published claim, or a protocol statement is shown wrong | Stop and wait for the owner (B6) |
| S14 | A production change, an unlisted module, or a `.py` file over 400 lines is needed | Stop before writing; escalate |

---

## 9. Threshold register, tolerance attainability and numerics

### 9.1 Threshold register (all fixed before any C2 data; owner-approved thresholds unchanged)

| Item | Value | Justification |
|---|---|---|
| ψ thresholds | 0.10 (NOT_USED, LOW_ALIGNED), 0.50 (USED) | 0.10 = (127/60) × 6/127 (Lemma RS1); 0.50 = majority (10.58 × random); owner Q2 |
| Energy bound η₀ | min(0.10, (127/60)·η̄_R), as two conjuncts | §2.9 (O-2, confirmed by owner addendum 21) |
| NEGATIVE_ALIGNED_CONTRIBUTION | U(E[A_S 1_E]) < −g_s at α_F | §2.9 (qualifier) |
| V3 | 0.30·G | C1 V3 kept (§6.6) |
| Y1, Y1*, Y2 | 0.10 (linear inequalities) | the negligibility threshold (§6.6) |
| κ_m trigger | 0.01 | mirrors C1's κ_ν trigger |
| τ_M (ROUTED_AROUND) | 0.10 | §2.10 (restricted licence) |
| H4 / H5 | f_x ≥ 0.90, f_y ≥ 0.85 / 0.01 nat | C1 kept; f_y: owner addendum 23 (the y-translation donor, §2.2) |
| s_max | FIT q0.999 | C1 kept |
| L1 | SSE_0 > 0; SSE_0 − SSE_lin > 0; R²_code\|0 ≥ 0.50; ρ_inc ≥ 0.90 (D0 baseline; fitted decoders; RC-3) | §6.6 (O-1, provisional, frozen before data) |
| L1 decoder equivalence | `c1_fit.equivalence_tolerance` (max(1e-10, 64·eps·κ·‖pred‖_∞)) | C1′ R13 rule |
| R1 | ≥ 0.75 sign agreement on \|δ*\| ≥ median; zero modulus ≤ 1e-12 (m32; masked features f*_K) or ≤ 1e-12·FIT median of the centred code-pair modulus (per model and family); overrides before the median selection (NEW-3) | C1 V1 kept; §2.11 |
| N2 | q99; max(0.05, F(D₂) + 0.02) | C1 §9 rule 1 kept |
| C0v | 507/512, 0.80, 8 per bin, 0.30; Sup ≥ 0.99 | C1′ rule unchanged |
| F1 | FWL rank 36 + 5 + 2K (43/45/47); cond ≤ 1e8; σ ratio ≥ 1e-6; LW ratio > 1e-12; whitened X̃ rank 5 + 2K and cond₂ ≤ 1e8; Lemma G1 identities in the scale-invariant form of §2.5 (1e-10: absolute for the dimensionless identities and ‖P̃ − P̃ᵀ‖_max, relative to ‖Γ‖_max and ‖B‖_max for P_SΓ and P_ΓB) | C1 kept; RC-10, RC-12; D-0104-2 |
| GLS-REF | 80-digit `Decimal`; θ̄_A < 1, θ̄_G < 1, ρ_ref = e_L/‖L*‖_F ≤ 1e-20 (Lemma GR with verified bounds); ‖P̂ − P*‖_F + ε*_P ≤ 1e-8·‖P*‖_F | §2.5 (RC-10, NEW-1) |
| Ridge | grid {1e-3, 1e-2, 1e-1, 1, 10}; LOPO 8 panels; ties to the larger λ | C1 kept |
| Family levels | α_R = α_S* = 1/240; α_M = 1/360 (one-sided per bound); nominal FWER 0.05 per family; study-wide nominal union 0.15 displayed | Lemma FW; O-3 |
| Bootstrap | TEST 20,000 draws (ranks 84/19,917; 56/19,945); VAL 5,000 at 0.05/3 (84/4,917); H5 rank 250; C2-M descriptive intervals (620518) 5,000 draws, two-sided 95%, ranks 125/4,875 (NEW-5); no conservative rank treatment | §6.2, §2.10 |
| Ladder | N_test ∈ {4096, 8192, 16384}; power 0.80; alternative 0.10·min mean(A_full 1_E); powers R/S* threshold contrasts and M transmission only | §6.7 |
| Rotation doses | θ ∈ {π/6, π/3}; frozen orientation (§2.11) | §2.11 |
| Splits | FIT 8192, FEAS 4096, VAL 4096, TEST k × 4096 | §5.1 |
| Seeds | §5.2 (620501–620518) | — |

### 9.2 The numerical guard (MD 10)
For a per-row statistic s entering a decision bound b:

  g_s := 1e-9·max(1, mean_i|s_i|) + β_s,

where β_s = max_i b_proj,i is the projector-induced error bound from GLS-REF: b_proj,i = ½‖Mᵀd_i‖₂·δ_P·‖Δy_i‖₂ for A_S-type terms (scaled by the coefficient of A_S in s) and b_proj,i = (2‖CMP̂_SΔy_i‖₂ + ‖CM‖₂δ_P‖Δy_i‖₂)·‖CM‖₂δ_P‖Δy_i‖₂ for e_S-type terms, with **δ_P = ‖P̂_S − P*_S‖_F + ε*_P** (the measured deviation plus the reference uncertainty of Lemma GR, RC-10, NEW-1; δ_P ≥ ‖P̂_S − P_S‖_F). "b > 0" requires b > g_s and "b < 0" requires b < −g_s; otherwise the bound is NUMERICALLY_UNRESOLVED and every statement that needs it is not declared (INC_j/NUMERICAL).

**Why a guard band, not C1's certificate (MD 10) [W/H].** The per-row A is a 36-term dot product of |d_v| ≤ 1 with |Δz_v| ≲ 50, so its float error is ≤ 36·u_m·Σ_v|d_v||Δz_v| ≲ 36 × 1.1e-16 × 100 ≈ 4e-13 nat (L§12). Tree means add ≤ ⌈log₂ n⌉·u_m·max|s| ≈ 1.6e-15·max|s| at n = 16384. The projector term is ≲ 1e-11 relative [H] and is bounded at run time by GLS-REF (with its reference uncertainty). The smallest decision-relevant margin is about 0.01 in ψ, ≈ 0.01 nat at E[A_full 1_E] ≈ 1 nat. The guard therefore sits ≥ 10³ above the expected error and ≈ 10⁷ below the margins [H for the expected error]. C1's full §15.3 certificate was built for a hypothesised Ḡ of 1e-2–1e-1 nat and a 0.1·Ḡ margin; at the recorded Ḡ ≈ 1.13 nat it is disproportionate. Kept: the Decimal reference rows (H3), the exact-rational symmetry checks, X1 on every scored row, GLS-REF.

### 9.3 Tolerance attainability (the R13 lesson)
No gate compares two float linear solvers, except the L1 decoder equivalence, which uses the C1′ R13 conditioning-dependent tolerance. Every other float comparison is with exact rationals or a Decimal reference, between two runs of the same deterministic code, or a bitwise identity.

| # | Comparison | Tolerance | Bound / evidence | Margin |
|---|---|---|---|---|
| T1 | τ symmetry (T, E, π) | 1e-14 | C1′ measured 1.11e-16 (jobs/0041) | ≈ 90 |
| T2 | (withdrawn: v1's ρ_R symmetry; D-0104-1) | — | H^Y has no symmetry; its oracle quantities are checked against the Decimal reference rows (T4–T6) | — |
| T3 | Closed form b32 vs BayesFilter (x pair only) | t + t², t = 2δ/(1−δ) + 62ε_sym (δ = 2e-12) | C1 §3.2 proof | by proof |
| T4 | Decimal posterior/predictive | 2e-12 relative (interval rule off the fast path) | proved bound 1.06e-12 (C1 §15.3.12) | ≥ 1.9 |
| T5 | Decimal surprisal | 1e-10 | ≤ 1.1e-12 from T4 | ≥ 90 |
| T6 | Decimal G | 2e-11·(1 + max_v\|λ̂_v\|) | \|δG\| ≤ ½Σ_v(\|δd_v\|\|λ_v\| + \|d_v\|\|δλ_v\|) ≤ 2.12e-12·max\|λ\| + 4.24e-12 [W from T4] | ≥ 4.7 |
| T7 | Named = canonical | 4e-12 relative | C1 v4 bound 2.11e-12 | ≥ 1.9 |
| T8 | Cross-model G | 1e-12 | summation order only: ≈ 3.9e-15·Σ\|dλ\| (C1 §3.3); fails only if Σ\|dλ\| > 250 | by bound |
| T9 | Identity patch; SYMBOL-ORDER (a)–(c) | bitwise | C1′ M0 PASS (0042, 0044) at `resid_post_3`; same code path at the other sites; index maps are exact | — |
| T10 | Readout identity, X1 | 1e-9·max(1, ‖z‖_∞) | Directly measured identity on the stated rows (RC-10). The head-arithmetic estimate (Lemma X) covers only part of the computation; the M0 attainability check (κ_X1 ≤ 1.76e3) is preliminary and on natural states only; expected κ_X1 ≈ 10–100 [H] | [H]; fail-closed |
| T11 | GLS identities (scale-invariant form, §2.5; D-0104-2) | 1e-10: absolute for the dimensionless identities and the whitened symmetry ‖P̃ − P̃ᵀ‖_max; relative to ‖Γ‖_max, ‖B‖_max for P_SΓ, P_ΓB | QR-based solve (§13.2 c2_code): error ≈ κ(R_x)·u_m ≈ 1e-13 for κ ≤ 1e3 [H]; forming P̃ from P̂ adds rounding that grows with cond₂(R_Σ) = κ_Σ^{1/2} [H]; every checked quantity is invariant under a common rescaling of y, unlike v1's absolute WP − PᵀW, which grows like 1/λ_min(Σ̂_ε) (2e-9 at the M problem in the job 0104 synthetic dry run); measured directly by GLS-REF | [H]; failure is INCONCLUSIVE, not a defect |
| T12 | GLS-REF | ρ_ref ≤ 1e-20 (with θ̄_A, θ̄_G < 1); ‖P̂ − P*‖_F + ε*_P ≤ 1e-8·‖P*‖_F | Lemma GR (a proved composed residual bound) with verified inverse-norm bounds (Lemma INV) and arithmetic enclosures (§2.5). Attainability [H]: ρ_ref ≲ 6e-40 at p = 80 even at the F1 admissibility limits (κ_Σ < 1e12, κ_X̃ ≤ 1e8). The float error of the production solve grows with κ_X̃ and κ_Σ^{1/2} [H] and is measured by the gate | ≈ 1e20 at the limits [H]; fail-closed |
| T13 | LW eigen-ratio | > 1e-12 | shrinkage bounds λ_min below [H] | — |
| T14 | FWL cond; whitened X̃ cond | ≤ 1e8 each | C1′ recorded 24.9 for the 41-column design (jobs/0044); 43/45/47 columns and X̃ not yet measured [H] | ≈ 4e6 (41 columns) [H] |
| T15 | NUM guard | §9.2 | per-row ≲ 4e-13 | ≥ 10³ [H] |
| T16 | Bootstrap tail Monte Carlo | 20,000 draws | relative SE ≈ 0.11 (R), 0.13 (M) of α [W]; does not certify 0.05 coverage (RC-9) | nominal |
| T17 | L1 decoder equivalence | `equivalence_tolerance` | C1′ R13 rule (job 0042), PASS in C1′ S4 | conditioning-scaled |
| T18 | M0 two-route SYMBOL-ORDER (NEW-7) | \|s_named − s_canonical\| ≤ 1e-12·max(1, Σ_v\|d_canonical,v z_canonical,v\|) per row | Both routes have the same exact value (the gather and the factor ½ are exact), so \|s_named − s_canonical\| ≤ (36u_m/(1 − 36u_m))·Σ_v\|d_v z_v\| = 4.0e-15·Σ_v\|d_v z_v\| [W; standard dot-product bound, any summation order]. The max(1, ·) form never fails at zero or under cancellation | ≥ 250 |

**Rule (fixed now).** No threshold or tolerance changes after any C2 gate value exists. An unattainable tolerance keeps its gate status; any change needs an owner decision (addendum 10).

### 9.4 Oracle-scale check (every threshold against what the oracle attains)
- V3: the oracle predictor has θ_full = 1 exactly (A_full = G for p = q̄; Lemma D2); recorded model capture 0.985 [W, E2 via L] → attainable.
- H5: recorded LB 1.12464 nat ≫ 0.01 [W, 0041].
- ψ and η thresholds are shares (dimensionless); 6/127 = 0.047 < 0.10 < 0.50 < 1: every category is attainable by some state of the world. ψ itself is unrestricted in sign and magnitude.
- ROUTED_AROUND/τ_M: τ_M is unrestricted in sign and magnitude (it can be negative or exceed one; v1's asserted range is withdrawn, RC-5); 0.10 is attainable in both directions.
- L1: R²_code|0 and ρ_inc are attainable by construction under the Gaussian linear model (§6.6); no attainability claim is made from current records (O-1).
- No 0.01-nat margin is applied to a share (the K4b lesson).

---

## 10. Outcome taxonomy

**Per family (exactly one; ordered rules §6.5):**

| Family | Outcomes |
|---|---|
| C2-R | FAIL_TECHNICAL/<class> · INCONCLUSIVE/<reason> (REGISTRY_INCOMPLETE, ELIGIBILITY, HEADROOM, NUMERICAL, CHART_UNAVAILABLE, PATCH_MODEL_DEGENERATE, LINK, MODEL_HEADROOM, NUISANCE_IN_S, UNDERPOWERED, TEST_GATE, PRECISION) · CIRCLE_NOT_HISTORY_SENSITIVE · USED · NOT_USED · LOW_ALIGNED_SHARE · PARTIAL · MIXED |
| C2-M | as R with RADIAL_SUPPORT added, ROUTED_AROUND · UPSTREAM_USED · UPSTREAM_NOT_USED · UPSTREAM_LOW_ALIGNED · UPSTREAM_PARTIAL · CNHS-2 · MIXED |
| C2-S* | as R with the X_PHASE_* names |
| Rotation arm | report-only (no outcome) |
| Study | INVALID (S11 interruption without rerun; S12 leakage); otherwise the three family outcomes side by side, with the 0.15 study-wide nominal union bound displayed |

**Per-model statuses:** USED_j, NOT_USED_j, LOW_ALIGNED_j, PARTIAL_j, INC_j, INC_j/NUMERICAL, CNHS_j, EXCLUDED_j/<gate>; M: ROUTED_j, UPSTREAM_*_j. Only the declared categories are in the scope of Lemma FW.
**Per-model endpoint statuses (RC-13):** SCORED, NOT_RUN/<gate> (excluded before ACCEPT, or family stopped), SEALED_UNSCORED/<gate> (T-PRE, RESP or SPEC), reported in every outcome.
**Per-gate statuses:** PASS, FAIL, INVALID, NOT_RUN, NUMERICALLY_UNRESOLVED.
**Qualifiers:** SPECIFICITY_NOT_ESTABLISHED, NEGATIVE_ALIGNED_CONTRIBUTION(j), PROJECTOR_DEPENDENT(j), HARMONIC_DEPENDENT(j, K), PRECISION_LIMITED(j), DISSENT(j: status).

---

## 11. Rerun and lineage rule (X6S1 §12 pattern)
1. **Store** `X:/Downloads/projects/topo-pilot/c2-readout-store/` (new; verified absent or holding only this lineage): `FREEZE.json`, `AUTH.json`, `registry/`, `hist/` (canonical arrays, digests, coverage tally), `oracle/`, `fits/`, `stages/<stage>/` (exclusive-create payloads with sha256), `GATES.jsonl`, `STAGES.jsonl`, `sealed/`, `superseded/<job>-a<k>/`, `logs/`, `cpu_ledger.json` (pre-created; schema `x4-oracle-profile-ledger-v1`), `c2_meter_bind.py`.
2. **Final outcomes are never rerun** to obtain another outcome: a PASS gate, a per-model status, a family outcome, every TEST value.
3. **Technical correction** only for a documented implementation or environment defect, by coordinator ruling naming the defect, the correction commit (inside the allowlist), the affected stages and artifacts, and evidence of independence from the outcome. **At most two correction jobs per defect.** A failure that shows a protocol statement wrong is not a defect: it stops C2 and returns to planning (owner).
4. **Supersede, append-only.** An affected attempt moves to `superseded/<job>-a<k>/` under `SHA256SUMS`; nothing is deleted. Unaffected artifacts must regenerate bit-identically against the archived hashes (else FAIL_TECHNICAL/LINEAGE). A superseded attempt is a recognised record of this lineage for namespace admission (§5.2), never an unrelated lineage.
5. **Environment reruns** (S11) reproduce identical values and do not count against item 3.
6. **Owner escalation** if a correction would change an already computed outcome-bearing quantity (every gate value, every bound, ψ, τ_M, η, every category).
7. **The store recognises lineage**: before a job writes, every existing store file is meter bookkeeping, a recorded superseded attempt's manifest or file, or a recorded output of an earlier accepted job of this lineage with its sha256 (the "exact recognised manifests and hashes" of the namespace rule, §5.2); anything else is INVALID/LINEAGE.
8. **Test access.** Before ACCEPT no TEST token exists. After ACCEPT, the TEST stage generates, hashes and separation-checks the TEST rows, then runs T-PRE (with X1 ephemeral) before any endpoint array (§5.7).

---

## 12. Cost forecast and resources (measure-only; MD 10, addendum 18; recounted, RC-15)

**Status.** Every count below is recounted from §5–§7 [W counts]; every rate and overhead is a heuristic [H]. The result is a **provisional** forecast, to be presented to the owner at AUTH (O-10; owner addendum 21 item 4 confirmed the measure-only budget). It is not validated and not a cap (CPU is measure-only).

**Rate basis [W/H].** C1′ S4 (jobs/0044) metered 696.81 CPU s for 73,728 float64 row-forwards at `resid_post_3` (8192 rows × 3 histories × 3 models) **plus** 3 chart constructions, 9 RFF decoder fits and the control decodes: ≤ 9.45 ms per row-forward including all of that overhead. With the `ModelConfig` defaults (d_model 128, d_mlp 512, 4 layers, 33 positions) a row-forward is ≈ 2·33·4·(4·128² + 2·128·512) ≈ 52 MFLOP [H: defaults assumed for the checkpoints], i.e. 17 / 8.7 / 5.5 GFLOP/s single-thread float64 at the 3 / 6 / 9.45 ms rates used below. C1′ S3 (jobs/0041) metered 160.09 CPU s for 36,864 history-oracles including the certificate and Decimal rows: ≤ 4.34 ms per history-oracle. Because overheads are now listed separately, the 9.45 ms upper rate (which already contains overhead) is conservative.

**(a) Row-forwards (one full or patched forward of one 33-token row through one model), all three models.**

| Stage | Content (per model; × 3 models) | Row-forwards [W] | CPU-h at 3 / 6 / 9.45 ms |
|---|---|---|---|
| S2 FIT | 8,192 natural rows with 3 hooks in one pass; M0 identity patch on 1,024 rows × 3 sites | 33,792 | 0.028 / 0.056 / 0.089 |
| S3 FEAS | 4,096 rows × 3 histories (H, H⁺, H⁻). No FEAS gate reads H^Y in a forward, so v1's fourth history is dropped | 36,864 | 0.031 / 0.061 / 0.097 |
| S4 VAL | Natural 4,096 × 4 histories = 49,152; X1 primary 4 interchange arms (x and y pairs) × 4,038 eligible = 48,456; C2-M 8 patched forwards (F, S, C for H⁺ and H⁻; S and F for H^Y) × 4,038 = 96,912; M Haar 8 frames × 2 arms × 1,024 = 49,152; **X1 low-id 20 arms × 1,024 = 61,440** (S* 4; **the three qualifier projectors 3 × 4 = 12, i.e. the 36,864 row-forwards per evaluated split that v1 omitted**; rotation 2 doses × 2 signs = 4) | 305,112 | 0.254 / 0.509 / 0.801 |
| S5 TEST, per 4,096-row block | Natural 49,152; X1 primary 48,456; C2-M 96,912 | 194,520 per block | 0.162 / 0.324 / 0.511 per block |
| S5 TEST, once per split | X1 low-id 61,440 (as VAL, including the 36,864 qualifier-projector forwards); M0 identity patch 1,024 × 3 sites = 9,216 | 70,656 | 0.059 / 0.118 / 0.185 |
| **S5 total** | k = 1 / **2** / 4 | 265,176 / **459,696** / 848,736 | k = 2: 0.383 / 0.766 / 1.207 |
| **All forwards** | k = 1 / **2** / 4 | 640,944 / **835,464** / 1,224,504 | k = 1: 0.534 / 1.068 / 1.682; **k = 2: 0.696 / 1.392 / 2.193**; k = 4: 1.020 / 2.041 / 3.214 |

X1 for the C2-R interchange arms is the only reason those arms are forwarded at all (the endpoint itself is the closed form); C2-M has no closed form, so its 8 patched forwards per row are endpoint computations. The R Haar frames, the operator decomposition and the rotation arm's endpoint values are closed forms (no forwards).

**(b) Overheads, listed separately (k = 2; k = 1 and k = 4 scale the two TEST-dependent rows).**

| Overhead | Count or basis | CPU-h low / central / high [H] |
|---|---|---|
| Oracle histories | S1 ≤ 65,536 (16,384 rows × 4 histories; H^Y only where defined) + TEST 16,384 per block, at 2 / 3.5 / 4.34 ms per history-oracle (C1′ S3 all-in ≤ 4.34) | 0.055 / 0.096 / 0.119 (k = 1: 0.046 / 0.080 / 0.099; k = 4: 0.073 / 0.127 / 0.158) |
| Registry (R before FIT; R′ after ACCEPT) | readers and digests over every source store and the inventory (§5.3); two builds | 0.03 / 0.08 / 0.25 |
| TEST family bootstraps | `bootstrap_means` loops over every statistic in every draw (one tree mean per (draw, array)): 20,000 draws × 99 arrays (R 57 = 3 × (6 primary + 12 variant + 1 NEGATIVE); M 21; S* 21) + 5,000 draws × 38 arrays (rotation 12, H5 2, C2-M descriptives 24 = 3 × (6 numerators + 2 shared denominators); NEW-5) = 2.17 million tree means at n = 8,192, at 50 / 110 / 250 µs each; not representable by a row-forward rate | 0.030 / 0.066 / 0.151 (k = 1: × 0.6; k = 4: × 1.8) |
| VAL gate bootstraps, P1 and MDE reports | gates 20 arrays × 5,000; P1 15 arrays and MDE reports 21 arrays (energy, M share), `sd_b4_draws` at 4,096 and `centered_draws` at N ∈ {4,096, 8,192, 16,384}, 5,000 draws: ≈ 1.54 million tree means in 4,096-row units at 30 / 70 / 150 µs | 0.013 / 0.030 / 0.064 |
| GLS-REF (80-digit Decimal; NEW-1) | 18 references (6 projector problems × 3 models). Per GLS problem ≈ 5.8 million Decimal multiply-adds: the two eliminations ≈ 0.88 M, the residuals R_A, R_C, R_G with their enclosures ≈ 0.43 M, the projector products with enclosures ≈ 0.39 M, the inverse residual I − V_A A with its enclosure ≈ 4.1 M. Per Euclidean problem ≈ 0.48 M. ≈ 88 million in all, at 1.5 / 4 / 12 µs | 0.037 / 0.098 / 0.295 |
| Decoders and fits | 27 L1 decoders (D0, D_code, D_lin × R, M, S* × 3 models; `nested_ridge` 8 folds + refit, `RidgeProbe` refit, equivalence) and 21 FWL/GLS fits | 0.005 / 0.01 / 0.03 |
| Charts | 3 direct C0v constructions; extension of every phased row (FIT 8,192; FEAS 12,288; VAL 12,288; TEST 12,288·k) | 0.01 / 0.03 / 0.06 |
| Closed-form attribution, descriptives, records | A partition, energies, r, ν_S, operator decomposition, 32 R Haar frames, ψ_max, records and I/O | 0.01 / 0.03 / 0.08 |
| PF and test suites | existing suites (the C1′ full suite alone took ≈ 12 min, run detached) and `tests/c2_readout` | 0.20 / 0.25 / 0.35 |
| **Overhead total** | k = 1 / **2** / 4 | 0.369 / 0.648 / 1.318; **0.390 / 0.690 / 1.399**; 0.432 / 0.774 / 1.558 |

**(c) Totals (forwards + overheads).**

| k | Low | Central | High |
|---|---|---|---|
| 1 | 0.90 | 1.72 | 3.00 |
| **2** | **1.09** | **2.08** | **3.59** |
| 4 | 1.45 | 2.82 | 4.77 |

**Revised provisional forecast (v3): central ≈ 2.1 CPU-h (k = 2), range ≈ 0.9–4.8 CPU-h** over k ∈ {1, 2, 4} and the rate and overhead bounds [W counts × H rates].
- **v3 against v2.** v2's central ≈ 2.0 CPU-h (range ≈ 0.9–4.5) changes only through:
  - the revised GLS-REF machinery (80 digits, residual enclosures and the verified inverse-norm check; NEW-1): +0.03 / +0.08 / +0.24 CPU-h, low / central / high;
  - the two shared denominator arrays per model in the C2-M descriptive stream (NEW-5): ≤ +0.002 CPU-h.

  The row-forward counts are unchanged; the review confirmed them.
- **v2 candidate against v3 (FROZEN-v1) (D-0104-1, R-0104-1; [W] from the job 0104 fractions).** H^Y exists only on Y_def rows (7,361/8,192 = 0.899), and E_y ≈ 0.893 replaces the ≈ 0.986 eligibility of the x pair for the y-pair arms. The y-pair counts in (a) and the H^Y oracle histories in (b) are therefore upper bounds. In (a) these are the H^Y natural forwards at 4,096 rows, and the two y-pair X1 arms and the two y-pair C2-M arms at 4,038 rows. The difference is about 5,800 row-forwards per 4,096-row split, ≈ 2% of all row-forwards (k = 2: ≤ 0.05 CPU-h). The ρ_R symmetry report and closed form are dropped (negligible); the H^Y Decimal reference rows keep v1's count; the stage-module split adds no computation. **The forecast is kept unchanged, as a conservative bound: central ≈ 2.1 CPU-h (k = 2), range ≈ 0.9–4.8.**
- **v2 against v1.** v1's 2.1 CPU-h (range 1.0–4.2) was superseded in v2. The recount added the qualifier-projector X1 forwards and the bootstrap, GLS-REF, decoder and registry overheads, and removed the unneeded FEAS H^R history (the y donor of that version; now H^Y, §21) and v1's per-block repetition of the low-id X1 rows.
- **Not included:** correction jobs (§11 item 3, at most two per defect), environment reruns (S11) and the coordinator's review work.
- **Against MD 10.** The range is consistent with MD 10's 1.5–2.5 CPU-h at its centre and exceeds it at the top.
- **Status.** The budget is measure-only (owner addendum 21 item 4). The revised forecast is presented to the owner at AUTH.

**Resources.** Single thread (`load_model64` sets `torch.set_num_threads(1)`); RAM < 4 GiB (the largest arrays are TEST activations: 16,384 rows × 4 histories × 3 hooks × 128 × 8 B ≈ 201 MB per model [W]); outputs < 1 GiB in `c2-readout-store/`; C: ≥ 2 GB and X: ≥ 30 GB before each job (the meter kills at C: < 2 GB); meter binding modelled on `c1_meter_bind` with `--max-cpu inf` and a pre-created `cpu_ledger.json`; jobs longer than the 600 s tool limit run detached. **Ordering in small steps:** S1, S2, S3+S4, S5 are separate jobs (releases R1–R5), each reviewed before the next.

---

## 13. Implementation footprint, reuse and test authors (charter six-field assessment)

### 13.1 Reused unchanged (blob sha256 at 967605c; G0 item iii)

| File | Functions used | sha256 |
|---|---|---|
| `src/topo_pilot/learner/model.py` | `TransformerLM.forward(return_hooks)` | `ee1c124ce83da147ccc2a4b4c0be167de902d61ecd00ead5748b8566f62ae039` |
| `src/topo_pilot/learner/patch.py` | `forward_with_patch` (sites `ln_final_out`, `resid_post_2`, `resid_post_3`) | `64d742e85ddba3d121a5c72af0abaef910c9b986a03a7b87caa26c4c20dd0ad4` |
| `tools/c1prime/c1_oracle.py` | `tau, donors, rho_index, symmetry_report, closed_form_b32, closed_form_tolerance, rel_agree, interval_rule, run_oracle, G_hat, named_from_canonical` (d, d^Y, d_rot into named order; RC-1), `canonical_from_named_cols` (only the SYMBOL-ORDER round trip (c) at H3 and the M0 two-route check; NEW-2), `G_named, y_marginal, m32, nuisance, s_max, eligible, eligible_fraction, kappa_nu, decimal_reference, decimal_G, h3_compare` | `077ea1489262d15075624fd6116900c74a6e5b0eb2fe02e5d4f6127cbc0323b3` |
| `tools/c1prime/c1_chart.py` | `extend_phase, c0_val, fit_chart_lcc, ConstructionLedger, landmark_ids` | `45b6aa0d8c8db28ce291eca320b1f322baddc9c70cee6588843f10935f4418df` |
| `tools/c1prime/c1_fit.py` | `standardise_nuisance, unit, fwl_design, qr_pos, partial_r2, equivalence_tolerance` | `13962c7a46541b9abbd53b2e9e69d6ce7c2f58de042499ba6f48c062228edf61` |
| `tools/c1prime/c1_gates.py` | `wrap, v1` (R1, with the zero overrides applied to its inputs, §2.11), `q99, frac_beyond` | `017499e0c434321ceae95c78ad584c15e93e82efd0ce768137f452d5668db485` |
| `tools/c1prime/c1_endpoint.py` | `A_hat, Zfull_hat` | `bdb283efbed04119cf23a5875835d08e1c21b4935d5f9cff334e3e88525d6e46` |
| `tools/c1prime/c1_means.py` | `tree_mean, bootstrap_means, c1_bootstrap_means, rank_for, rank_check, quantile_with_rank` | `e0630816942224933d3380897eb90b374522ca0ac4c4c8f3f6b62edcead2d00c` |
| `tools/c1prime/c1_model.py` | `state_sha, load_model64, model_inputs, natural_logits, identity_patch_ok` (the last only at `resid_post_3`) | `37665037dd4d6b29a45b5981016c3a965d98f9ee47d474e21c74c616f2324d0a` |
| `tools/c1prime/c1_data.py` | `panels, lowest, registry_digests, build_registry, first_token_ok` | `262418b2f0272e8425a038c53bb120c8f40402a4100b8a71e257f71b560106e9` |
| `tools/c1prime/c1_records.py` | `C1GateFailure, run_c1_gate, classify_exception` | `d0299ff4621c699a9439184b72e125a2dea34f304e50772c0c190fb9f628fdb5` |
| `tools/c1prime/c1_config.py`, `CONTRACT.json` | `chart_cfg`, `MODELS`, the chart block | `8e170b5144b732527d41aeeb2ab71e41da2bfcd5b33b2d580527711b3ea6e207`, `f8df2e43bc24a3e992ce4323a8577ec4a7e2657a4e00bdf3ff0323b909a7a379` |
| `tools/x4_circle_history/chart.py`, `cochain.py`, `errors.py` | `chart_from_arrays, extend, agreement, phase_bin_counts, overall_resultant` (K4-frozen) | `938821a0…9ccb`, `e53f6725…3075`, `8aa309c4…b99f` (full value of `errors.py` §5.6; E-0102-1) |
| `tools/x4_circle_history/precision.py` | `sd_b4_draws, centered_draws, precision_summary, mde` | `5ae1e632eee0ac5767a9b536c6f7aebbc2d7328a9a664db828f37afc643329c8` |
| `tools/x4_circle_history/scores.py` | `history_digests` | `8cf9a5f810ad41a412379bfe2786e9ce7fafe4efbd31122ea66a7d7c70f989a6` |
| `tools/c1prime_registry/c1_registry_sources.py` | sources (a)–(c), `store_sources`, `handoff_sources`, readers | `4f40840d8eb88d515556aeb7058640761d4b44a7a6ee8045fb3bce9987a5a253` |
| `src/topo_pilot/analysis/x4f_scores.py` | `ledoit_wolf`, `standardizer` (decoder standardisation, §6.6) | `03e2d736a734cf8d45d158112d1955b4faba267b235777064814dee3bafc563b` |
| other `src` | `dataset.HMMSampler, make_sequence_ids, process_code, check_disjoint, check_first_token`; `contracts.SeedTree, SequenceLayout`; `oracle.BayesFilter`; `learner.stage.load_model`; `experiment.x4f_probe.nested_ridge` (standardises internally); `prediction.ridge.RidgeProbe` (does not standardise) | bound by the R→H protected-path diff (§13.5) |
| runtime | job-0014 meter, controls, winjob, op_guard; a store-local `c2_meter_bind.py` modelled on `c1_meter_bind.py` (`3c1439fc…58d`) | — |

### 13.2 Six-field assessment and the new package

| Field | Assessment |
|---|---|
| **1. Reused unchanged** | §13.1. Nothing in `src/` changes; no frozen file is edited |
| **2. Not reusable unchanged (verified)** | `c1_data.history_generator`, `sequence_ids`, `sample_block` hard-code scope `c1-sf-v1` (frozen; never retrofit) → thin C2 equivalents. `c1_model.activations` and `patched_logits` hard-code `resid_post_3` → a C2 three-hook pass and site-parameterised patch wrappers (`natural_logits` is reused: it reads index 32). `c1_fit.fit_fwl`/`f1_check` hard-code 41 columns and K = 1; `c1_fit.fit_decoder` adds an RFF map; `c1_fit.haar_frames` uses scope `c1-sf-v1` and 2-frames → C2 equivalents (same `lstsq`, same `qr_pos`, the same nested_ridge → standardizer → RidgeProbe recipe without the RFF map). `c1_endpoint.endpoint_bounds`, `ladder`, `per_model_status`, `overall`, `v3` hard-code 0.05/3, 5,000 draws, C1 seeds and C1 semantics → C2 bounds and rules on `c1_means`. `c1_records.LogitPolicy` encodes the C1 gate order → a C2 policy. `c1_driver*`, `c1_release`, `c1_config.CONTRACT` are bound to the C1′ contract. Not used: `c1_gates.{D_w, D_y, leakage, m2, m3, v2, m4}`, the fixed decoders, `c1_bounds`, `c1_cert` |
| **3. Missing capability** | (1) the y-translation donor υ_k with the sign rule k_Y and the off-grid ineligibility (OFF_GRID_Y; no clamp, no wrap; ≈ 20 lines, mirroring `tau`/`donors`; no symmetry report or closed form, §2.2); (2) readout coordinates Q₀, M, the SYMBOL-ORDER checks and the X1 identity (ephemeral); (3) the K ∈ {1, 2, 3} FWL (36 + 5 + 2K), the whitened-design rank/conditioning check, the QR-based GLS operator (Cholesky Σ_ε = R_ΣᵀR_Σ, X̃ = R_Σ^{−ᵀ}X_n = Q_xR_x, L = R_x⁻¹Q_xᵀR_Σ^{−ᵀ}), the Euclidean variant, the identities and the 80-digit Decimal GLS-REF with the composed residual bound (Lemmas GR and INV; NEW-1); (4) the A partition, the energies, the exact random reference r, ν_S, the operator decomposition, ψ_max, E\|A_S\|; (5) the incremental L1 with D0 (S*: the masked target f*_1), the R1 wrapper with the zero-modulus overrides applied to the `c1_gates.v1` inputs, N2; (6) the C2-M patch construction and its descriptives; (7) the S* parameterisation with the masked features f*_K (NEW-3); (8) the rotation arm, its corrected oracle, the frozen orientation and s_rot; (9) family bounds, Lemma FW rules, 2-of-3, endpoint statuses, qualifiers (NEGATIVE included), Q-CODE licence fill, ladder; (10) the registry `c2-reg-v1`; (11) the driver, policy, sealing, namespace admission, records, release, meter binding and contract |
| **4. Smallest change** | One new package `tools/c2_readout/` outside `tools/c1prime` (the C1′ pin check) and one test directory `tests/c2_readout/` |
| **5. Invariants** | Frozen weights in exact float64 casts; bitwise identity patches; donors keep w32; one symbol-order convention (d_named by `named_from_canonical`); no w33 and no latent states stored; every fit on FIT; charts reused by hash, never refitted; gates in the §7 order; no row trimmed; no stage retried except §11; X1 ephemeral; sealed VAL endpoint values |
| **6. Regression and next extension** | Regression: the PF suites unchanged, the S1′ fixtures, X1 and SYMBOL-ORDER on real data. **Next extension (MD 9; not built):** a w31-kept donor (shift w1..w30) to separate E-short; a horizon-2 readout target; a direct-versus-through-block-3 split for C2-M; other positions; encodings outside the registered code (higher harmonics, interactions) as their own preregistered families |

**Files** (`tools/c2_readout/`; every `.py` ≤ 400 lines; `tools/check_file_sizes.py` enforces it). The pre-allowlisted overflow module `c2_stats.py` is now planned from the start, so unrelated responsibilities are not forced into `c2_code.py` or the driver (RC-15):

| File | Contents | Budget |
|---|---|---|
| `API.md` | Contract committed first: names, signatures, shapes, dtypes, streams, sequence-id codes, report keys, the frozen registry source and exclusion inventory (O-7), the lineage manifest schema, the static output manifest | — |
| `PROTOCOL_C2_v2.md`, `CONTRACT.json`, `TEST_PLAN.md` | Byte copy of the frozen protocol; machine-readable thresholds, seeds, hashes (the §4 `state_sha` strings included); the test plan | — |
| `c2_config.py` | CONTRACT loading, constants, exact `Fraction` levels and ranks, seeds, paths | ≤ 400 (≈ 150) |
| `c2_data.py` | Sampling (scope `c2-v1`), ids, panels, the y-translation donor H^Y (sign rule, off-grid rule; §2.2), history tables with the H^Y digest (where defined), coverage tally, namespace admission | ≤ 400 (≈ 340) |
| `c2_registry.py` | R and R′ sources (reusing `c1_registry_sources` and the K4b/X6S1 readers), inventory scan, exclusion records, separation | ≤ 400 (≈ 300) |
| `c2_oracle.py` | Oracle for the four histories, q̄, d (named order), G (x, y, rotation), κ_m, eligibility, zero-modulus flags, the exact oracle forward and Decimal reference rows for H^Y, the x-leakage descriptive, the rotation oracle | ≤ 400 (≈ 310) |
| `c2_model.py` | Three-hook pass, Q₀/M, M0 checks, SYMBOL-ORDER, X1 (ephemeral) and its attainability, patch wrappers | ≤ 400 (≈ 320) |
| `c2_code.py` | FWL (K = 1, 2, 3), whitened-design checks, GLS (QR), Euclidean variant, identities, R1 (zero-modulus rule), N2, Haar frames, S* | ≤ 400 (≈ 340) |
| `c2_stats.py` (pre-allowlisted overflow, planned) | GLS-REF 80-digit Decimal elimination, residuals with enclosures, verified inverse-norm bounds ω_A and ω_G, e_Y, e_L, ρ_ref and ε*_P (Lemmas GR, INV); the L1 decoders D0/D_code/D_lin with the standardisation recipe and equivalence; P1 ladder wrappers and the MDE reports | ≤ 400 (≈ 380) |
| `c2_attrib.py` | A partition, energies, r, ν_S, operator decomposition, ψ_max, E\|A_S\|, rotation arm and s_rot, C2-M quantities and descriptives (the NEW-5 interval stream), the POST-DESC values (NEW-6) | ≤ 400 (≈ 340) |
| `c2_decide.py` | Bounds, NUM guard, Lemma FW per-model rules, coarse prerequisites, 2-of-3, endpoint statuses, qualifiers, Q-CODE licence fill | ≤ 400 (≈ 390) |
| `c2_driver.py` | Infrastructure: the C2 `LogitPolicy` (X1 ephemeral), sealing, records, lineage, release binding, `auth_ok`, G0, the meter check, the lazy stage dispatch `run_stage` and the CLI. The gate bodies live in the four stage modules (R-0103-1, superseded in footprint by R-0104-1) | ≤ 400 (≈ 400) |
| `c2_stage_base.py` (R-0104-1) | Shared stage helpers: store loaders and the per-stage `ctx` caches, and the split-level checks that several stages and T-PRE reuse | ≤ 400 |
| `c2_stage_pre.py` (R-0104-1) | The step functions of the first stages of §7, in §7 order | ≤ 400 |
| `c2_stage_val.py` (R-0104-1) | The step functions of the later stages up to and including VAL (S4), in §7 order | ≤ 400 |
| `c2_stage_post.py` (R-0104-1) | The S5 step functions (ACCEPT through REPORT, POST-DESC inside REPORT), in §7 order | ≤ 400 |
| Store-local `c2_meter_bind.py` | Rebinds module names only (measure-only, `CAP = inf`), fail-closed sha256 and import-directory check | outside the repository |

Planned: the ten modules from `c2_config.py` to `c2_driver.py` ≈ 3,270 lines (realistically 2,800–3,600), plus the four stage modules (the job 0104 scratch drafts of the S1–S5 stage bodies total 1,084 lines [W]): **14 modules, ceiling 14 × 400 = 5,600 lines (R-0104-1; it supersedes coordinator addendum 3's 12 modules and 4,800 lines)**. The exact assignment of §7 rows to `c2_stage_pre`, `c2_stage_val` and `c2_stage_post` is fixed in an `API.md` erratum before the stage code is written, following §7's stage column (the R-0103-1 procedure); no gate, order or scope changes with it. Precedents: `tools/c1prime` 3,597 lines in 22 files; X6S1 2,600–3,200 planned. L's 600–900-line estimate (L§14) is replaced.

### 13.3 Test-author split (independent; D-1/X2a/K4b/X6S1 pattern; binding)
**Rules:** authors write from the frozen protocol and `API.md` only, after the freeze and before any module exists; they may read the reused production code of §13.1; they never read, list or search `tools/c2_readout/*.py`; they execute nothing (the worker runs the tests in PF); corrections only by the file's author; **no formatter is ever run over `tests/c2_readout`** (the implementer formats module files by name only); synthetic fixtures only, no payload. `AUTHORSHIP_A.md` and `AUTHORSHIP_B.md` record what was read, not read and executed. Files `tests/c2_readout/test_a_*.py` (≤ 6) and `test_b_*.py` (≤ 6), ≤ 400 lines each (one more file per author than v1, for the review fixtures).

**Author A (algebra, statistics, oracle):**
- *T-READOUT:* Helmert N₁, Q₀ = qr_pos(diag(γ)N₁) on a random LayerNorm; Lemma R (u = β + Q₀y; z = W_Uβ + My); the rank rule (one zero γ_k keeps rank 127, two zeros do not); **LayerNorm ε fixture (RC-16):** with ε = 1e-5, scaling a centred input by c changes the output (scale is not removed) while u − β ∈ U₀ still holds exactly.
- ***T-ORDER (RC-1):*** an independently checked **non-involutive** permutation (perm∘perm ≠ id, e.g. a 36-cycle composed with a transposition); for canonical d and canonical logits z_c with named logits z_n = `named_from_canonical`(z_c, perm): dᵀz_c = `named_from_canonical`(d, perm)ᵀz_n, and the wrong conversion `canonical_from_named_cols`(d, perm)ᵀz_n differs (the fixture is constructed so that it does); an involutive permutation is shown to hide the error; the SYMBOL-ORDER checks (b) at H1, (a) at H2 and (c) at H3, and the M0 two-route check, accept the correct map and reject the inverse map; **cancellation/zero-result fixture (NEW-7):** rows where ½dᵀz is exactly 0, or cancels to below 1e-15 while Σ_v\|d_v z_v\| ≈ 1, pass the per-row rule (a purely relative 1e-12 rule fails them on summation-order error alone) and still reject the inverse map.
- *T-GLS:* Lemma G1 identities; P_SΓ = 0; Lemma G2 (code from arm 1, complement and nuisance coordinates from arm 2); Lemma G3 by Monte Carlo on a Gaussian fixture (Cov(Ly, P_rest y) ≈ 0, with an explicit tolerance from the fixture's n); the Euclidean variant still excludes Γ; GLS-REF against an independent Decimal implementation; **whitened-design fixtures (RC-10, RC-12):** [Γ, B] of rank < 5 + 2K → PATCH_MODEL_DEGENERATE; cond₂(X̃) > 1e8 with a well-conditioned FWL design → PATCH_MODEL_DEGENERATE; **Lemma GR fixtures (NEW-1):**
  1. *First-solve error propagation* (the review's example): Σ = I₃, X = [e₁, εe₂], Y* = [e₁, εe₂ + δe₃] with ε = 1e-3, δ = 1e-19, 𝒢* = XᵀY* and an exact second solve (R_C = R_G = 0). The exact error ‖L* − L‖_F = δ/ε² = 1e-13 (computed in `Fraction`) is ≤ e_L ≈ 1.0e-10. The withdrawn v2 expression (≈ 9.2e-16 absolute) is shown to lie below the true error. The reference is not accepted (ρ_ref ≈ 1e-13 > 1e-20).
  2. Separate perturbations of 𝒢* (R_C ≠ 0) and of L* (R_G ≠ 0), each with e_L ≥ the exact error.
  3. Lemma INV: θ̄ < 1 gives a valid upper bound on the inverse norm (checked against the exact inverse); θ̄ ≥ 1 → not accepted.
  4. The Euclidean case (A = I, Y* = X, R_A = 0, ω_G bounding ‖(X_nᵀX_n)⁻¹‖₂) on a fixture where cond₂(X_n) and cond₂(X̃) differ by orders of magnitude, so a κ(X̃)²-based tolerance would be wrong.
  5. Arithmetic uncertainty: a residual computed at a deliberately reduced precision has a computed norm plus enclosure ≥ its exact (`Fraction`) norm; a `Decimal` trap → not accepted.
  6. ε*_P enters the gate and δ_P.

  Further T-GLS fixtures: **fixture "B in the nuisance span"** (col(B) ⊂ col(Γ)) → F1 INCONCLUSIVE/PATCH_MODEL_DEGENERATE (X§11 item 3); **scale-invariance fixture (D-0104-2):** one GLS problem with Σ_ε scaled by c ∈ {1e-8, 1, 1e8} and [Γ, B] by √c. The scale-invariant G1 check of §2.5 gives the same values up to rounding at every c and passes, while v1's absolute ‖WP − PᵀW‖_max exceeds 1e-10 at small c. A planted non-self-adjoint P fails the whitened check at every c, and the Euclidean variant reduces to ‖P − Pᵀ‖_max.
- *T-PARTITION:* A_S + A_Γ + A_rest = A_full exactly; interventional identity (Lemma D1 ii); source independence; Lemma D2 (logit vs log-softmax with Σd = 0); **operator decomposition:** A_S^vis + A_S^null = A_S exactly, and a fixture where CMJΔy = 0 but CMP_SJΔy ≠ 0 (a readout-null source displacement converted into a readout-active patch) gives A_S^null ≠ 0.
- *T-RANDOM:* Lemma RS1 (E[ψ_R] = k/n) and Lemma RS2 (a, b; E[e_R] = a‖Kw‖² + b‖w‖²‖K‖_F²) by Monte Carlo with explicit tolerances, and exactly for a = 887/344043, b = 121/344043 at (k, n) = (6, 127) by `Fraction`.
- *T-ENERGY:* both conjuncts; isotropic case gives the 0.10 bound for both; **cancellation fixture** (E[A_S] ≈ 0, large \|A_S\|) → energy blocks NOT_USED → LOW_ALIGNED; **orthogonal-movement fixture** (P_SΔy moves the logits orthogonally to d) → ψ = 0, LOW_ALIGNED; the Cauchy–Schwarz bound; **opposition fixture (RC-4):** natural change ∝ (1, 100), code effect (−1, 0), oracle contrast along the first coordinate → ψ = −1, energy share 1/10001, both conjuncts pass → NOT_USED_j with NEGATIVE_ALIGNED_CONTRIBUTION, and the filled licence contains "possibly negative"/"opposing" and no "below 10% in magnitude" wording.
- *T-HEADKERNEL (X§11 item 5):* the circle code in ker(CM) → A_S = 0 and e_S = 0 exactly, R1 PASS, the model responds → per-model NOT_USED (a valid zero, never an invalid one).
- ***T-SCOPE (RC-2; run with the R and the S\* parameterisation):***
  - (i) **out-of-code fixtures** (the representation carries the phase in the registered first three harmonics; L1 and R1 pass):
    - (i-a) the synthetic head reads only a fourth harmonic of φ;
    - (i-b) *the interaction fixture uses cos φ [h − E(h)], with the centred nuisance independent of phase and with a balanced synthetic design making the interaction orthogonal to the registered additive regressors* (h = entropy; NEW-4, verbatim). An uncentred cos φ × entropy head is not used: through the mean entropy it has a first-harmonic component.

    In both, ψ ≈ 0 and energy ≈ 0 → per-model NOT_USED, and the filled licence carries Q-CODE and no unrestricted "the circle is not used" sentence.
  - (ii) **excluded-direction fixture:** a phase-associated predictive contribution is placed along a Γ column. That nuisance covariate's correlation with the phase is **imperfect**, so the FWL design stays full rank and the code can still pass the incremental L1 (NEW-4). Expected: A_Γ carries the response and ψ is small → NOT_USED or LOW_ALIGNED with Q-CODE, with ψ_Γ reported large.
  - **Validity prerequisites first (NEW-4).** In every T-SCOPE fixture, F1, L1, R1 and RESP_j are asserted to pass before the NOT_USED (or LOW_ALIGNED) outcome is asserted.

  Both expected results demonstrate the restricted interpretation; neither certifies a universal circle null.
- *T-LEAK (X§11 item 3; RC-7):* a planted y-direction inside col(B) → Y1 fails → EXCLUDED/NUISANCE_IN_S; **a large negative placebo contribution passes Y1**, and the filled licence states only the linear inequality.
- *T-PROJ:* a fixture where the Γ-oblique and Euclidean complements give different categories → PROJECTOR_DEPENDENT set; harmonic analogue → HARMONIC_DEPENDENT.
- *T-ORACLE:* **the y-translation donor H^Y (D-0104-1)** on synthetic canonical token arrays (36 symbols, c = 6a + b), with these checks:
  - the sign rule: k_Y = +1 iff ȳ(b31(H)) < 5.5, and ȳ = 5.5 exactly gives −1;
  - the shift b → b + k on w1..w31, with the x-column a and w32 kept;
  - the off-grid rule: a prefix symbol in row 5 under k = +1, or in row 0 under k = −1, makes the row OFF_GRID_Y. Such a row is ineligible and counted; it is never clamped or wrapped, and no H^Y is formed for it;
  - E_y and f_y, with OFF_GRID_Y rows counted as ineligible;
  - the H^Y oracle quantities from `BayesFilter` against an independent Decimal filter on a small synthetic HMM with 36 symbols. No closed form or symmetry report is used for H^Y;
  - the x-leakage descriptive λ_x.

  Kept from v1: the rotation oracle (roll b31, re-apply w32) and its m = 2 equality with the donor closed form; normalised q̄.
- ***T-ROT (RC-14):*** the frozen orientation: R_K(θ)f(φ) = f(φ + θ) for φ = 0.3, θ ∈ {π/6, π/3}, every k, within 1e-15; an exact synthetic sign fixture where a toy head reads the code phase and the +θ rotation moves the prediction toward the ρ^{(m)}_+ rolled belief (s_rot = 1), and the sign-flipped orientation gives s_rot = 0; A_rot,i = 0 counts as disagreement.
- *T-FAMILY (Lemma FW):* exhaustive grid over truth states (ψ ∈ {−1, 0.05, 0.10, 0.3, 0.50, 0.7}, energy true/false per conjunct, θ_full above/below 0.30, Y1 true/false) × all sign patterns of the registered bounds: every false in-scope declaration lies in the listed failure events, and never more than 4 per model (M: 6); coarse statements are never declared without RESP_j and (SPEC_j or Y1 inactive) (RC-8); the mutual exclusivity of the categories; equality → not declared; NEGATIVE_ALIGNED_CONTRIBUTION is outside the count.
- *T-RULES:* §6.4–§6.5 branches, 2-of-3 with every split (3–0, 2–1, 1–1–1, with exclusions), endpoint statuses (SCORED, NOT_RUN, SEALED_UNSCORED; RC-13; **NEW-6:** a T-PRE or RESP/SPEC failure records NOT_RUN/<gate> and forms no endpoint array; SEALED_UNSCORED only for arrays formed before a later stop; POST-DESC runs only after every family outcome is recorded, never after FAIL_TECHNICAL, INVALID or a pre-ACCEPT exclusion, and never changes an endpoint status), MIXED vs INCONCLUSIVE/PRECISION, DISSENT, coarse statements, the C2-M ROUTED precedence, the CNHS licence text (RC-8).
- *T-BOOT:* the shared index stream (V3 first then the endpoint, identical indices); Fraction ranks (84/19,917; 56/19,945; 84/4,917; 250; 125/4,875 for the two-sided 95% descriptive intervals); **the C2-M descriptive stream (NEW-5):** 24 arrays with indices shared across models and quantities, intervals of ratios of resampled means, and UNDEFINED on a zero (original or resampled) or nonfinite denominator, with no replicate discarded or redrawn; the indicator form (sign of E[s·1_E] = sign of E[s | E]).
- *T-LADDER:* precision kernels called with the registered cfg; N_F and N_test rules; PRECISION_LIMITED; only Z^{0.10}, Z^{0.50} (R, S*) and Z_τ (M) are gated, the M-share and energy MDEs reported only (RC-15).

**Author B (model, gates, operations):**
- *T-PATCH:* on a tiny `TransformerLM`: `forward_with_patch` identity (bitwise) at the three sites; linearity at `ln_final_out` and independence from the inputs at position 32; at `resid_post_2` positions < 32 unchanged and position 32 attending to its own patched key/value.
- *T-X1:* the closed form vs the patch path within τ_X1; an injected index, β or Q₀ defect fails by ≥ 1e6·τ_X1; the attainability statistic κ_X1; X1 fail-closed.
- *T-FWL (RC-12):* recovery of a known B with K = 3 on synthetic data; the design ranks 43/45/47 for K = 1/2/3 and the whitened ranks 7/9/11; rank and conditioning failures; no column dropping.
- *T-L1 (RC-3):* the three decoders through `nested_ridge`/`RidgeProbe` with the explicit standardisation recipe and the equivalence check; the SNR fixture where raw-GLS-vs-shrinkage would fail and the registered comparator passes; a code missing half the circle information fails; **nuisance-predictive fixture:** z̃ predicts the phase so well that both complete-decoder scores pass (R²_code ≥ 0.50, R²_code ≥ 0.90·R²_lin) while the code adds nothing → R²_code|0 < 0.50 → LINK fail; **denominator fixtures:** SSE_0 − SSE_lin ≤ 0 or SSE_0 = 0 → LINK fail.
- *T-R1 (RC-14):* wrap at ±π, sign(0) as disagreement, median ties (`inverted_cdf`), CNHS routing; **zero-modulus fixtures:** |m32| ≤ 1e-12 on an arm → δ* = 0, kept and counted (ZERO_MOD), no row deleted; a centred code pair below 1e-12 × its FIT median (per model and family) → sign δ_c = 0 (ZERO_CODE); **the overrides come before the median selection and the agreement** (an overridden row's |δ*| = 0 enters the median; the input substitution makes `c1_gates.v1` reproduce δ* = δ_c = 0 exactly, and on rows without overrides the wrapper returns `c1_gates.v1`'s values bitwise); **masked features (NEW-3):** on an invalid row f*_3 = 0 ∈ ℝ⁶ in the S* regressors and f*_1 = 0 ∈ ℝ² as every L1* target, never the unmasked (1, 0) pairs of the placeholder φ* = 0; the S* fit is deterministic.
- *T-N2 (RC-6):* class-mean Mahalanobis, q99, fraction rule, the max(0.05, F + 0.02) cap; **paired-Gaussian counterexample:** s, t iid N(0, 1), source (s, t), donor (t, s), first-coordinate swap → (t, t): the radial screen passes (exceedance ≈ 0.032 < 0.05) while the joint law differs (coordinate correlation 1), and the status/licence wording is "radial support screen", never "natural".
- *T-CMODE (RC-5, RC-6):* C2-M F/S/C constructions; context-matched ratio; ROUTED_AROUND precedence; Y2 activity; **cancellation fixture** E[A_full] = 1, E[A_M,F] = 0, E[A_M,S] = 1, E[A_M,C] = −1 → ROUTED_AROUND with the restricted licence text and the descriptive circle/complement/interaction quantities reported after the outcome; the UPSTREAM_USED licence mentions the residual skip and makes no block-3 claim.
- *T-POLICY (RC-13):* the computation-order rule: no FIT logit outside M0 rows, no FEAS logit, VAL sealed arrays refused before the outcome, TEST endpoint refused before T-PRE; **X1 ephemeral:** the X1 path retains only identity diagnostics, and an attempt to write an endpoint array or summary from it is refused (INVALID/leakage); **gate-order fixture (NEW-2):** the driver refuses SYMBOL-ORDER (a) before H2's sampling and separation are complete, (c) before H3 has constructed the FIT oracle contrasts, the two-route check before M0, and any FIT sampling before REG passes; the recorded gate sequence equals §7.
- *T-REG:* a collision gives FAIL_TECHNICAL/LINEAGE; an unreadable source or an unclassified history-bearing store gives INCONCLUSIVE/REGISTRY_INCOMPLETE; the C1′ landmarks are in R; R′ includes FIT/FEAS/VAL; pytest basetemp outside the root.
- *T-SEED:* scope `c2-v1`, disjoint streams, the seed map (620501–620518).
- ***T-NAMESPACE (RC-11; three separate tests):*** (1) **initial admission:** the only `c2-v1` hits are the pinned code/configuration and the recognised FREEZE/AUTH records, and the store has no scientific payload → PASS; the same with a pre-existing `hist/` payload → FAIL; (2) **legitimate continuation:** a store holding the recognised manifests and hashes of earlier accepted jobs (and a recorded superseded attempt) → PASS; one altered hash → FAIL; (3) **unrelated collision:** a foreign record or store referencing `c2-v1` outside the lineage manifest → FAIL_TECHNICAL/LINEAGE.
- *T-G0 (RC-16):* blob hashes (§13.1), chart hashes, K4 FREEZE, protocol hash, the three full `state_sha` strings of §4; refusal on any mismatch.
- *T-LINEAGE:* supersede and manifest; bit-identical regeneration; exclusive create.
- *T-METER:* the binding sha256 and import-directory refusal; measure-only caps.
- *T-SIZE:* the module set (14 modules: the ten v1 modules with `c2_stats.py`, plus `c2_stage_base.py`, `c2_stage_pre.py`, `c2_stage_val.py` and `c2_stage_post.py`; R-0104-1) and the 400-line limit.

### 13.4 Execution worktree
A new worktree `X:/Downloads/projects/topo-pilot/topo-pilot-c2` on branch `c2-<job>` from R. Every job runs there at H with an empty `git status --porcelain --untracked-files=all` recorded; `PYTHONPATH=<worktree>/src` and the venv interpreter with `-s` (the editable install would otherwise import main's `src`); the meter imported from `<worktree>/tools/x4_oracle_profile`.

### 13.5 Commit binding (D2A D5 rule)
- **R:** the main commit recorded at the freeze; this draft was written against 967605c, and the freeze round re-checks the 967605c→R diff over the protected paths. **Bound by coordinator addendum 1 and carried into v2:** R = `d44548b073523d402cc31fbfc5440c0d6df37a23`; the protected-path diff 967605c→R is empty; execution worktree `topo-pilot-c2`, branch `c2-0100` from R.
- **Protected paths:** `src`, `pyproject.toml`, `tools/{c1prime, c1prime_registry, x4_circle_history, x4_oracle_profile, k4b, x6_stage1, c2_readout}`, `tools/check_file_sizes.py`, `tools/check_imports.py`, `tests/{learner, dataset, contracts, oracle, process, world, analysis, prediction, experiment, circle_history, c1prime, c1prime_registry, c2_readout}`.
- **Allowlist:** `A` entries for the §13.2 repository files and the §13.3 test files only (the overflow module included).
- **Mechanical check:** `git diff --no-renames --name-status R H -- <protected>` lists only allowlisted `A` entries.

---

## 14. Dependencies and prerequisites

| # | Dependency | Needed by | Check |
|---|---|---|---|
| D1 | Codex result-blind review (done: NOT_READY, RC-1..RC-16), revision v2, confirmation review (done: NOT_READY, NEW-1..NEW-8), revision v3, confirmation, freeze as C2-FROZEN-v1; then this pre-data revision (v2 candidate; owner addendum 23), its Codex confirmation and the re-freeze as C2-FROZEN-v2 | everything | freeze record |
| D2 | **Owner AUTH addendum** naming the frozen sha256 (that of the re-frozen C2-FROZEN-v2; owner addendum 22 named v1's) and the revised forecast (provisional central ≈ 2.1 CPU-h, range ≈ 0.9–4.8, measure-only) | S1 and every later execution | `AUTH.json` (gate 0b) |
| D3 | The three C1′ chart NPZs unchanged (sha256 §2.4) | C0c | sha256 |
| D4 | C1′ `HIST_*.npz` unchanged (registry source d) | REG | sha256 (§5.3) |
| D5 | K4 FREEZE and kernel blobs unchanged | G0 | sha256 |
| D6 | The full float32 `state_sha` of the three models copied into `CONTRACT.json` — **resolved:** strings in §4 from the C1′ M0 gate record (RC-16) | M0 | string equality |
| D7 | Registry readers for every history-bearing store, or exclusion records, frozen in `API.md` — **outstanding** (O-7) | REG | completeness |
| D8 | Clean worktree, venv, `PYTHONPATH` | PF | §13.4 |
| D9 | Disk: C: ≥ 2 GB, X: ≥ 30 GB before each job | all jobs | meter |
| D10 | One scientific job at a time; no other session writing into the worktree | all jobs | coordinator attestation |
| D11 | The owner confirmations of §18 (scope, ROUTED_AROUND licence, NOT_RUN reading of Q4, O-2, O-3, O-10 measure-only). **Resolved:** owner addendum 21 | freeze | addendum 21 sha256 (§18) |

---

## 15. Risks

| # | Risk | Likelihood [H] | Consequence | Handling |
|---|---|---|---|---|
| K1 | C0v fails for a reused chart (C0-val never ran; gauge alignment 0.89) | low–moderate | per-model CHART_UNAVAILABLE for R and M (endpoints NOT_RUN) | 2-of-3 survival; C2-S* unaffected; no fallback chart |
| K2 | L1 fails (the code adds too little over the D0 baseline) | moderate (raised by the incremental rule) | per-model LINK exclusion | K = 1, 2 reported; complete-decoder scores reported descriptively; no threshold change after data |
| K3 | ψ in an indecision band | 0.08–0.17 per model | INC_j, possibly MIXED | ladder; 2-of-3 |
| K4 | Energy SDs large | unknown | NOT_USED unreachable → LOW_ALIGNED_SHARE | conservative by design; MDEs reported; not powered (RC-15) |
| K5 | Y1 fails (S carries readout-relevant y-information) | low | NUISANCE_IN_S exclusion | five covariates excluded exactly; y-pair partition reported |
| K6 | κ_m ≥ 0.01 | low | specificity report-only | pre-declared qualifier |
| K7 | N2 fails at layer 2 | moderate | C2-M per-model exclusion | a radial support screen only; no distribution guarantee is claimed either way (RC-6) |
| K8 | ROUTED_AROUND | plausible | no circle-specific M answer | licensed only as the restricted signed-effect statement; descriptives reported (RC-5) |
| K9 | GLS-REF or identities fail (ill-conditioned Σ_ε or X̃) | low | per-model NUMERICAL or PATCH_MODEL_DEGENERATE | QR solve; LW shrinkage; whitened-design check; the scale-invariant G1 identity check (D-0104-2) |
| K10 | X1 attainability fails at M0, or X1 fails on amplified interchange states | very low | INCONCLUSIVE/NUMERICAL before VAL, or FAIL_TECHNICAL | owner decision needed to change τ_X1 |
| K11 | Registry incomplete | known traps | release blocked | temporaries outside the root; exclusion records; inventory frozen in `API.md` |
| K12 | Torch float64 nondeterminism | very low | M0/X1 fail | single thread; bitwise identity checks |
| K13 | USED read as a discovery although expected | — | overclaiming | §1.4 stated in advance |
| K14 | "Only linear algebra" reading of C2-R | — | perceived triviality | §1.2: the answer is exact because the question at this site is exact; C2-M supplies the nonlinear, context-dependent test |
| K15 | Post-hoc model selection under 2-of-3 | — | inflated claims | rules fixed; Lemma FW covers every model; DISSENT reported |
| K16 | Footprint overrun | moderate | S14 | overflow module planned; stage bodies in four stage modules; ceiling 5,600 lines (14 modules, R-0104-1) |
| K17 | Editable-install or venv-launcher traps | known | wrong code imported | `PYTHONPATH=<worktree>/src`, `-s` |
| K18 | Scope misreading: NOT_USED read as "the circle is not used" | — | overclaiming | Q-CODE in every licence; T-SCOPE fixtures (RC-2) |
| K19 | Nominal FWER read as exact coverage | — | overclaiming | §6.2 wording; never-licensed list (RC-9) |
| K20 | Symbol-order defect in d | low | every attribution wrong | one convention; SYMBOL-ORDER at H1/H2/H3/M0 (NEW-2); non-involutive T-ORDER fixture (RC-1) |
| K21 | Budget above the central estimate (k = 4, slow overheads) | moderate | up to ≈ 4.8 CPU-h | measure-only (addendum 21); the forecast is presented at AUTH |
| K22 | H4 fails at f_y ≥ 0.85 (about 10% of rows are OFF_GRID_Y; pre-data f_y = 0.893, a margin of ≈ 0.04 [W, job 0104]) | low | INCONCLUSIVE/ELIGIBILITY at S1 (study) | threshold fixed by owner addendum 23; no clamp or wrap; no change after data (S3) |
| K23 | The y placebo is not exactly x-neutral (x leakage about 0.2% of the x contrast at b31 [W, job 0104]) | known | a small x component in the y-pair contrasts | reported descriptively (§2.12); κ_m gates Y1/Y1*/Y2 activity; Y1 licenses only the registered linear inequality (RC-7); never licensed as x-neutral (§3.5) |

---

## 16. Open items (status after the reviews, the rulings and owner addendum 21)

| # | Item | Status in v3 | For |
|---|---|---|---|
| O-1 | L1 thresholds | **Adopted per the review:** 0.50/0.90 provisionally, applied to the incremental comparison (R²_code\|0, ρ_inc) of RC-3; frozen before data; no attainability claim from current records | — |
| O-2 | The NOT_USED energy bound η₀ = min(0.10, (127/60)·η̄_R) on centred Euclidean logits; Fisher-weighted version descriptive | Reviewer: adopt as a conservative operational energy criterion, keeping its RMS interpretation and the signed-share limitations of RC-2/RC-4. **Confirmed by owner addendum 21** (§18 item 4) | — |
| O-3 | Three separately controlled families | **Adopted (ruling):** separate nominal 0.05 per family, R uniquely primary, M and S* secondary, the study-wide nominal union bound 0.15 displayed wherever combined conclusions are discussed; no selecting the favourable family. **Confirmed by owner addendum 21** (§18 item 4) | — |
| O-4 | Excluded models under 2-of-3 | Replaced by the RC-13 reading (assessment vs NOT_RUN). **Confirmed by owner addendum 21** (§18 item 3) | — |
| O-5 | A separate FEAS split | **Adopted per the review**; FEAS failures remain operational findings | — |
| O-6 | C2-M context-matched ψ_M | **Adopted per the review**; the routing interpretation is not adopted (RC-5, RC-6) | — |
| O-7 | Hashes and registry | **Hashes resolved** (§4, RC-16). **Registry reader/exclusion inventory still to freeze in `API.md`** before sampling | coordinator (at implementation) |
| O-8 | Rotation-arm doses {π/6, π/3} | **Adopted per the review**, report-only, with the RC-14 qualification | — |
| O-9 | Scope tag `c2-v1`, seeds 620501–620518, store and worktree names | **Adopted per the review** after the namespace fix (RC-11); integer-seed reuse across named PCG64 streams is not leakage | — |
| O-10 | Budget | Recounted (§12; v3): provisional central ≈ 2.1 CPU-h, range ≈ 0.9–4.8, measure-only. **Measure-only confirmed by owner addendum 21** (§18 item 4); the revised forecast is presented at AUTH | owner (AUTH) |

---

## 17. Corrections applied and writer's decisions

### 17.1 The comparison's defects (CMP §5), each fixed

| Defect | Fix | Where |
|---|---|---|
| X1 (oracle/intervention mismatch) | The rotation oracle rolls b31 and re-applies w32, exactly as held by the intervention; the code rotation is a descriptive proxy (RC-14) | §2.11 |
| X2 (filter directions, arbitrary metric) | X's sphere-constrained decoder-row move is dropped; the code moves natural values along pattern (encoding) directions | §2.4–§2.6 |
| X3 (no positive control; constraints may absorb the readout) | V3 positive control; every NOT_USED needs RESP_j; no constraint set | §6.3, §6.6 |
| X4 (copied D_w/D_y ceilings known to fail) | No decoder-damage gate (no synthetic state is consumed nonlinearly at the endpoint) | §1.2 |
| X5 (frame-level randomness in control means) | No frame-averaged control enters a decision; random references are exact (RS1–RS2); Haar frames report-only | §2.8 |
| X6 (power unsupported) | Power and precision from recorded inputs, marked; P1's scope stated (RC-15) | §6.7, §6.8 |
| X7 (rotated harmonic content) | The rotation turns harmonic k by kθ, with a frozen orientation | §2.11 |
| X8 (15° measurement gate possibly unreachable) | Dropped; L1 with fitted decoders, incremental over D0 | §6.6 |
| L1 (NOT_USED overclaims "inert") | Energy gate with a justified bound; MD 8 wording; LOW_ALIGNED_SHARE; Q-CODE; RC-4 description | §2.9, §3.1 |
| L2 (attribution depends on the complement) | Euclidean-complement qualifier (MD 6); what the swap preserves is stated, and that G3 gives no distribution guarantee (RC-6) | §2.5 |
| L3 (multiplicity proof incomplete) | Lemma FW with explicit event counting, scope restricted (RC-8) and nominal (RC-9) | §6.3 |
| L4 (two wording errors) | "No synthetic state evaluated through a nonlinearity"; block 3 also reads its own patched key/value | §2.1, §2.10 |
| L5 (C2-M ratio mixes contexts; 0.30 unjustified; self-repair) | Context-matched ψ_M; τ_M at 0.10 with the restricted ROUTED_AROUND licence (RC-5) | §2.10, §3.2 |
| L6 (6/127 only approximate for S) | Stated as references, not nulls | §2.8 |
| L7 (no GLS error bound) | GLS-REF (an 80-digit Decimal reference accepted by the proved composed residual bound, with verified inverse-norm bounds and arithmetic enclosures; RC-10, NEW-1) and the NUM guard term β_s | §2.5, §9.2 |
| Both missed: prior predictability | Stated in advance | §1.4 |
| Both missed: cancellation | E\|A_S\| reported; the energy bound limits RMS movement; the signed rule includes opposition (RC-4) | §2.9 |

### 17.2 Writer's corrections to track L beyond the comparison (v1, kept)
1. **L1 comparator.** L compared the raw GLS coordinate with a shrinkage decoder, which fails a valid code whenever the noise-to-signal ratio exceeds 0.316. Both sides are fitted decoders on nested feature sets, now incremental over D0 (§6.6).
2. **R1 covariates.** "Each donor's own z̃±" is moot: L_BΓ = 0, so z̃ never enters the code (§6.6).
3. **Multiplicity statement.** L's "each declared category is wrong with ≤ 0.05/3; union ≤ 0.05" is replaced by Lemma FW (§6.3).
4. **Stopping under 2-of-3.** L's "the first non-PASS stops the family" is adapted to the owner's 2-of-3 rule with explicit study/model/family scopes (§7, S4–S5).
5. **X1 and Decimal tolerances.** X1 is set at 1e-9·max(1, ‖z‖_∞) with a preliminary attainability check at M0; the Decimal G tolerance is derived (T6).
6. **TEST identity patches.** M0's bitwise identity patch on TEST runs on the 1,024 lowest-id rows; X1 remains on every scored row.
7. **Footprint.** 600–900 lines → 2,800–3,600 lines (§13.2).
8. **Data split.** A separate FEAS split (X§3) carries the activation-only validity gates.

### 17.3 What C2 keeps, changes or drops from C1/C1′ (L§17, updated)

| Item | Decision | Why |
|---|---|---|
| Models, checkpoints, float64 cast, identity patch | Keep | M0 PASS in 0042 and 0044 |
| τ± donors with w32 kept; q0.999 eligibility; H1–H5; κ_ν | Keep | the part that worked: exact symmetry, natural histories, Ḡ ≈ 1.13 nat, κ_ν < 0.01, f ≈ 0.98 |
| Canonical oracle, G, Decimal rows | Keep, with normalised q̄ and one explicit symbol-order convention | removes the δ_m term; RC-1 |
| C1′ chart rule and the three production charts | Keep by hash; C0-val run now | bit-reproducible; no new constructions beyond 3 comparators |
| Crossed contrast A (logit-difference form), V3 at 0.30·G | Keep | arm-common effects cancel; ψ must be a share of a real response |
| Bootstrap discipline, ladder, sealing, registry, stop rules | Keep (levels per Lemma FW; 2-of-3 replaces intersection–union, owner Q4) | proven discipline |
| Decisive site | Change: `ln_final_out`/32, variable still at `resid_post_3` | exact linear head |
| Intervention | Change: synthetic forced state → natural-value interchange of GLS code coordinates | no synthetic state through a nonlinearity |
| Phase map | Change: K = 1 Euclidean plane → K = 3, GLS nuisance-excluding projector, 5 covariates | targets the cause of M2-cal's ŵ flips |
| Endpoint | Change: θ vs Haar controls → ψ share with energy-gated NOT_USED | a well-defined, scope-restricted "not used" |
| Controls | Change: matched Haar family → y placebo, exact random references, V3, ν_S, operator decomposition | vary the variable, not the instrument |
| M2 damage/matching gates, fixed RFF decoders, leakage gate, V2 | Drop | no synthetic state consumed nonlinearly; replaced by L1, R1, Y1, X1 |
| M3 support | Drop for R; keep as N2 (a radial support screen) for M | needed only where the network evaluates patched states |
| §15.3 numerical certificate | Drop (guard band, Decimal rows, GLS-REF kept) | margins ≈ 10⁷ × the error (MD 10) |

### 17.4 Revision round 2 (Codex review RC-1..RC-16; coordinator rulings)
Every RC is applied with the reviewer's exact fix (rulings: all ACCEPTED). The RC-by-RC disposition is §19. Additions beyond a literal RC: the interpretability operator decomposition (§2.12, review "interpretability controls"); the TEST-recheck conditional-coverage remark (§6.3 remark 7, review "data discipline"); seed 620518 for the C2-M descriptive intervals that RC-5 requires; renaming the N2 failure status from UNNATURAL_PATCH to RADIAL_SUPPORT (consistent with RC-6); the M0 two-route SYMBOL-ORDER check (a runtime counterpart of the RC-1 fixture).

### 17.5 Revision round 3 (Codex confirmation review NEW-1..NEW-8; coordinator rulings)
Every NEW item is applied with the reviewer's exact fix, and RC-1, RC-10, RC-13 and RC-14 are completed (rulings: all ACCEPTED). Everything the review confirmed as APPLIED is unchanged. The disposition is in §20.

Writer's decisions within the fixes:
- **NEW-1.** The reviewer's composed residual bound is adopted with its proof (Lemma GR, §2.5), together with verified inverse-norm bounds (Lemma INV) and explicit arithmetic enclosures. The bound is proved, so the measured-only fallback the rulings allow is not needed.
- **NEW-1, precision.** The Decimal precision is raised from 50 to 80 digits, so that the 1e-20 acceptance is attainable over the whole F1-admissible conditioning range.
- **NEW-1, Euclidean variant.** The variant's F1 conditioning check applies to X_n.
- **NEW-3.** `c1_gates.v1` is reused unchanged: the zero overrides are applied to its inputs.
- **NEW-6.** The descriptive reporting of NOT_RUN models is specified as the separate post-outcome operation POST-DESC.
- **NEW-7.** The attainability row T18 is added.

---

## Appendix A. Desk arithmetic [W] (Python as a calculator; no data)
- Ranks: `ceil(B·α)` and `ceil(B·(1−α))`: B = 20,000, α = 1/240 → 84, 19,917; α = 1/360 → 56, 19,945; B = 5,000, α = 1/60 → 84, 4,917.
- Expected tail of rank k of B under an ideal continuous percentile (RC-9): 84/20,001 = 0.0041998 vs 1/240 = 0.0041667; 56/20,001 = 0.0027999 vs 1/360 = 0.0027778.
- z-values: z_{1−1/240} = 2.638257, z_{1−1/360} = 2.772921, z_{1−1/60} = 2.128045, z_{0.80} = 0.841621.
- Lemma RS2 constants at (k, n) = (6, 127): n(n+2)(n−1) = 2,064,258; a = 5,322/2,064,258 = 887/344,043 = 0.00257817; b = 726/2,064,258 = 121/344,043 = 0.00035170; a + 127b = 6/127 = 0.0472441. 0.10/(6/127) = 127/60 = 2.11667; 0.50/(6/127) = 10.5833.
- η̄_R = a + 127b/g: g = 0.5 → 0.0919; 1 → 0.0472; 2 → 0.0249; 3.63 → 0.0149; 5 → 0.0115.
- RC-4 example: ψ = ½(−1)/(½·1) = −1; energy share 1/(1 + 100²) = 1/10,001 ≈ 1.0e-4.
- RC-6 counterexample: χ²₂ q99 = −2 ln 0.01 = 9.21034; P(2t² > 9.21034) = 2(1 − Φ(2.14597)) = 0.031876.
- P1: (z_{1−α} + z_{0.80})/√N at α = 1/240: N = 4,096 → 0.05437; 8,192 → 0.03845; 16,384 → 0.02719 (SD ceilings for a 0.10-nat alternative: 1.84, 2.60, 3.68).
- Half-widths at α = 1/240 (SD 1.0): N = 4,038 → 0.0415; 8,076 → 0.0294; 16,152 → 0.0208.
- Forward recount (§12): S2 8,192·3 + 3·1,024·3 = 33,792; S3 4,096·3·3 = 36,864; S4 49,152 + 4·4,038·3 + 8·4,038·3 + 8·2·1,024·3 + 20·1,024·3 = 49,152 + 48,456 + 96,912 + 49,152 + 61,440 = 305,112; S5 per block 49,152 + 48,456 + 96,912 = 194,520; per split 61,440 + 9,216 = 70,656; totals 640,944 / 835,464 / 1,224,504 (k = 1, 2, 4). Qualifier-projector X1 forwards per split: 4 × 1,024 × 3 × 3 = 36,864 (the RC-15 count).
- FLOPs per row-forward (defaults): 2·33·4·(4·128² + 2·128·512) = 51.9 M; at 3 / 6 / 9.45 ms: 17.3 / 8.65 / 5.49 GFLOP/s.
- Cost: 0044 rate 696.81/73,728 = 9.451 ms per row-forward; 0041 rate 160.09/36,864 = 4.343 ms per history-oracle; TEST bootstrap 20,000·99 + 5,000·38 = 2,170,000 tree means (v3, NEW-5; v2: 5,000·32, 2,140,000); totals as §12 (v3, k = 2: 1.086 / 2.082 / 3.592 CPU-h; v2: 1.055 / 2.003 / 3.355). Overheads (v3), k = 1 / 2 / 4: 0.369 / 0.648 / 1.318; 0.390 / 0.690 / 1.399; 0.432 / 0.774 / 1.558 CPU-h.
- GLS-REF (v3, NEW-1):
  - Count per GLS problem (n = 127, m = 11): n³/3 + n²m (Y*) + 2n²m (R_A) + 3m²n (𝒢*, R_C) + m³/3 + m²n (L*) + 2m²n (R_G) + 3m³ (V_G) + 2n²·6 + 2n²·5 + 2n² (projectors, difference) + 2n³ (I − V_A A) ≈ 5.80 M Decimal multiply-adds. Euclidean ≈ 0.48 M.
  - Total and cost: 3 × (5 × 5.80 + 0.48) ≈ 88.4 M; at 1.5 / 4 / 12 µs this is 0.037 / 0.098 / 0.295 CPU-h.
  - Attainability heuristic (u_D = 5e-80 at p = 80): (n + 1)·u_D·1e4·κ_Σ^{3/2}κ_X̃² at κ_Σ = 1e12, κ_X̃ = 1e8 gives 6.4e-40 (6.4e-10 at p = 50).
- NEW-1 example (ε = 1e-3, δ = 1e-19):
  - true ‖L* − L‖_F = δ/ε² = 1e-13 (relative ≈ 1.0e-16);
  - e_L ≈ ω_G·e_Y·(1 + ‖X‖_F‖L*‖_F) = 1e6·1e-19·1,001 ≈ 1.0e-10;
  - v2's ε_ref = 16·δ/(√3·√(1 + ε²)) ≈ 9.2e-19 relative (≈ 9.2e-16 absolute), below the true error.
- NEW-7: 36u_m/(1 − 36u_m) = 3.9968e-15; 1e-12/3.9968e-15 = 250.2.
- NEW-5 ranks: ⌈5,000·1/40⌉ = 125, ⌈5,000·39/40⌉ = 4,875.
- Rotation: one x-cell = 2π/12 = π/6.

---

## 18. Owner confirmations (resolved: owner addendum 21)

**Resolved on 2026-10-21.** The owner confirmed all four items below in `archive/owner-decisions-20261015/OWNER_DECISIONS.addendum-21.md` (sha256 1e6e88382cc32dbef5ae2b6a3cc3ebf80901c76924064170b7b777400df4380f):
- item 1: the claim scope is the fitted code and intervention;
- item 2: the restricted ROUTED_AROUND licence;
- item 3: validity exclusions with NOT_RUN endpoints under the 2-of-3 rule;
- item 4: O-2 with NEGATIVE_ALIGNED_CONTRIBUTION as a qualifier only, with no lower bound; O-3 as separate nominal 0.05 families; O-10 as a measure-only budget.

**Still required (separate from these confirmations):** a future execution AUTH addendum naming the frozen sha256 and the forecast (gate 0b, §14 D2; now central ≈ 2.1 CPU-h, range ≈ 0.9–4.8, §12).

**Historical text (NEW-8).** The rest of this section records, unchanged in substance, the questions as they were put to the owner with v2. They are no longer pending.

The thresholds approved in addendum 20 are unchanged. The following readings were introduced or made explicit by the review and the rulings and needed the owner's explicit confirmation before the freeze (they were sent to the owner at the same time as v2):

1. **Claim scope = the fitted code and intervention.** USED and NOT_USED (and every family outcome) concern the frozen, nuisance-excluding linear code defined by the FIT fit and the GLS projector, and its registered interchange, not every encoding of circular information (Q-CODE, §1.1, §3; RC-2). *Does the owner accept this scope?*
2. **The restricted ROUTED_AROUND licence.** ROUTED_AROUND is licensed only as "the signed oracle-aligned effect of the full layer-2 final-position interchange, in the fixed source context, is below 10% of the natural contrast", with no inference about routing around the circle, E-image or active block-3 processing; the circle, complement, interaction and energy quantities are reported descriptively (§2.10, §3.2; RC-5, RC-6). *Does the owner accept this licence?*
3. **Validity exclusions with NOT_RUN endpoints under the 2-of-3 rule.** The reading of addendum 20 Q4 ("2 מתוך 3 אבל כמובן שלבדוק על כולם ולדווח על כך"): all three models receive the preregistered validity assessment and are reported; failed validity gates can leave scientific endpoints NOT_RUN; two valid, resolved models can support a two-of-three claim; no claim is made about the excluded model (§3, §6.5; RC-13, O-4). *Does Q4 permit this?*
4. **O-2, O-3 and O-10.**
   - **O-2 (the energy bound):** η₀ = min(0.10, (127/60)·η̄_R) on centred Euclidean logits, as two conjuncts, read as an RMS criterion; NOT_USED is "a low signed oracle-aligned share and bounded mean-square centred-logit effect for the registered interchange" and includes negative (opposing) contributions, flagged by NEGATIVE_ALIGNED_CONTRIBUTION (§2.9; RC-4). If the owner intends NOT_USED also to exclude substantial opposition, that needs an additional lower-bound condition and a revised multiplicity proof before freeze; v2 adds none.
   - **O-3 (separate 0.05 families):** nominal 0.05 per family, R uniquely primary, M and S* secondary, the study-wide nominal union bound 0.15 displayed wherever combined conclusions are discussed (§6.3 remark 6).
   - **O-10 (the revised budget):** provisional central ≈ 2.0 CPU-h (k = 2), range ≈ 0.9–4.5 CPU-h, measure-only, excluding correction jobs and environment reruns (§12).

---

## 19. RC-by-RC disposition (Codex review; all ACCEPTED by the coordinator's rulings)

*This is the round-2 record, kept as written except for the bracketed round-3 notes.*
- *RC-1, RC-10, RC-13 and RC-14 were PARTIAL in the confirmation review. Round 3 completes them (§20), and §20 supersedes the corresponding cells.*
- *The owner questions referred to here were confirmed by owner addendum 21 (§18).*

| RC | Severity | What changed | Where |
|---|---|---|---|
| RC-1 | BLOCKER | One convention: M stays in named output order and `d_named = c1_oracle.named_from_canonical(d_canonical, perm)` (also d^R, d_rot; [v2 candidate: d^Y, §21]); v1's `canonical_from_named_cols` on d removed (kept only for the independent check route); `named_from_canonical` added to the reuse table; H1 SYMBOL-ORDER checks and an M0 two-route check; independent **non-involutive permutation fixture** T-ORDER; X1 no longer claimed to catch symbol-order defects. [Round 3: SYMBOL-ORDER (a) moved to H2 and (c) to H3; per-row M0 rule; NEW-2, NEW-7, §20.] | §2.3, §2.7, §7 rows 3, 9, 23, §13.1, §13.3 T-ORDER, §15 K20 |
| RC-2 | BLOCKER | The Q-CODE clause (verbatim) added to every family licence (R, M, S*) and the summary; "the readout's history-dependent prediction runs mainly through the circle" replaced by "the registered code interchange carries more than half of the signed oracle-aligned response"; operational scope stated; never-licensed list extended; **out-of-code and excluded-direction synthetic fixtures** (T-SCOPE, run for R and S*) with restricted-interpretation expectations | Summary, §1.1, §1.3, §1.5, §2.2, §3 (Q-CODE), §3.1–§3.3, §3.5, §13.3 T-SCOPE |
| RC-3 | MAJOR | **Baseline decoder D0** on [onehot(w32), z̃]; FEAS SSE_0, SSE_code, SSE_lin; R²_code\|0 = 1 − SSE_code/SSE_0 and ρ_inc = (SSE_0 − SSE_code)/(SSE_0 − SSE_lin) with the 0.50/0.90 thresholds; undefined or nonpositive denominator → LINK failure; complete-decoder scores kept descriptively; "operational decoder comparisons" statement; FIT standardisation explicit (`nested_ridge` standardises internally; `RidgeProbe` does not; the standardizer → RidgeProbe recipe and equivalence check); nuisance-predictive and denominator fixtures | §6.6 L1, §3.1 R1, §7 rows 11, 13, §9.1, §12, §13.3 T-L1, §16 O-1 |
| RC-4 | MAJOR | Owner inequalities kept; NOT_USED described as "low signed oracle-aligned share and bounded mean-square centred-logit effect for the registered interchange"; negative contributions stated as included; **NEGATIVE_ALIGNED_CONTRIBUTION** qualifier (outside the FW allocation); magnitude-below-10% wording removed; Cauchy–Schwarz item recast as descriptive with the (1, 100)/(−1, 0) example and fixture; no lower bound (owner question; confirmed by addendum 21) | §1.3, §2.6, §2.9, §3.1 R3, qualifiers, §6.3 remark 8, §6.4, §9.1, §13.3 T-ENERGY, §18 item 4 |
| RC-5 | BLOCKER | ROUTED_AROUND keeps the enum with the reviewer's restricted licence (verbatim); "so no share … can be attributed to its circle code", the τ_M range claim and the inference to E-image deleted; τ_M stated as unrestricted in sign and magnitude; circle, complement, interaction and energy quantities reported descriptively after the outcome (seed 620518); cancellation fixture | §1.3, §2.10, §3.2, §6.3 remark 4, §6.4 M rule 8, §9.4, §13.3 T-CMODE, §15 K8, §18 item 2 |
| RC-6 | MAJOR | G3 reworded ("conditional within-state residual covariance … no distribution-preservation guarantee for the paired interchange"); N2 renamed a **radial support screen** (status RADIAL_SUPPORT), with the keys/values caveat; UPSTREAM_USED rewritten to include the residual skip, block-3 claims removed; **paired-Gaussian counterexample fixture** (exceedance 0.0319 < 0.05) | §2.5, §2.10, §3.2, §3.5, §6.6 N2, §7 row 15, §10, §13.3 T-N2, T-CMODE, §15 K7 |
| RC-7 | MAJOR | Y1/Y1*/Y2 license only the registered linear inequality ("the mean signed placebo contribution is below 0.10 times the mean full placebo contrast"); general nuisance-exclusion, small-magnitude and subspace-illusion readings removed; no population placebo-ratio claim (denominator positivity is a nominal VAL gate); negative-placebo fixture | §1.3, §2.6, §2.10 Y2, §3.1 R2, qualifiers, §3.5, §6.3 remark 3, §6.6 Y1/Y2, §13.3 T-LEAK |
| RC-8 | MAJOR | Lemma FW scope restricted to the registered TEST sign statements, category propositions and eligible coarse statements; operational validity statuses and FEAS findings stated as outside; coarse statements require RESP_j and (SPEC_j or Y1 inactive) and family validity; CNHS licence replaced (verbatim) for R, M (CNHS-2) and S*; MIXED/INCONCLUSIVE non-claims; 2-of-3 aggregation kept | §3.1 R1, R6, R7, coarse, statuses, §3.2 CNHS-2, §3.3, §3.5, §6.3 (table, Lemma FW, proof), §6.6 R1, §10, §13.3 T-FAMILY, T-RULES |
| RC-9 | MINOR | "Exact error control" replaced by "an exact event-counting argument conditional on valid individual bounds; the implemented percentile-bootstrap family error rate is nominal and includes sampling and bootstrap Monte Carlo approximation"; 84/20,001 and Monte Carlo error stated; 20,000 draws do not certify 0.05; no conservative rank treatment adopted, ranks frozen | MD map row 4, Summary, §6.2, §6.3, §9.3 T16, §3.5, Appendix A |
| RC-10 | MAJOR | Whitened GLS design X̃ gated (rank 5 + 2K, cond₂ ≤ 1e8); Decimal reference accepted by ε_ref = 16(κ_Σρ_Σ + κ_X̃²ρ_G) ≤ 1e-20 from conditioning and residuals; reference uncertainty ε*_P in the GLS-REF gate and in δ_P of the NUM guard; X1 described as a measured identity, the head-arithmetic expression declared partial (no complete-computation bound); M0 attainability stated as preliminary, not an all-interchange guarantee. [Round 3: ε_ref withdrawn and replaced by the composed residual bound, Lemmas GR/INV, §2.5; NEW-1, §20.] | §2.5, §2.7, §7 row 11, §9.1, §9.2, §9.3 T10, T12, T14, §13.3 T-GLS |
| RC-11 | MAJOR | Namespace admission replaced by the reviewer's rule (verbatim) with its operational form; G0 (vi) updated; superseded attempts recognised; **three separate tests**: initial admission, legitimate continuation, unrelated collision | §5.2, §7 row 1, §11 items 4, 7, §13.3 T-NAMESPACE, §16 O-9 |
| RC-12 | MINOR | Every universal "rank 47" replaced by 36 + 5 + 2K (43/45/47 for K = 1/2/3); explicit full-rank check of the whitened nuisance-plus-code design at 5 + 2K (7/9/11); no-column-dropping rule kept | §2.4, §2.5, §2.10, §7 row 11, §9.1, §9.3 T14, §13.3 T-FWL |
| RC-13 | MAJOR | The assessment-versus-NOT_RUN wording (verbatim) in the scope, summary and overall rules; endpoint statuses SCORED/NOT_RUN/SEALED_UNSCORED; X1 defined as an ephemeral integrity operation permitted within T-PRE (and at VAL) that retains only identity diagnostics; owner acceptance requested (Q3; confirmed by addendum 21). [Round 3: endpoint status at TEST failures and POST-DESC; NEW-6, §20.] | MD map row 4, Summary, §3, §3.1 statuses, §5.1, §5.7, §6.5, §7 rows 17, 23, §8 S5, S12, §10, §13.3 T-POLICY, T-RULES, §18 item 3 |
| RC-14 | MINOR | Doses {π/6, π/3} and the corrected oracle kept; exact-matching language replaced by the reviewer's sentence (latent pre-observation rotation; descriptive proxy); frozen rotation-matrix orientation and pairing with ρ^{(m)}_+; exact synthetic sign fixture; scalar sign-agreement statistic s_rot defined; deterministic zero/unresolved-modulus handling for C2-S* (and R1), no row deletion, counts reported. [Round 3: masked features f*_K, per-family ZERO_CODE median, overrides before the median selection; NEW-3, §20.] | §2.11, §3.4, §3.5, §5.5, §6.6 R1, §9.1, §13.3 T-ROT, T-R1, §16 O-8 |
| RC-15 | MAJOR | Every forward recounted, including the qualifier-projector X1 forwards (36,864 per split); bootstrap, GLS-REF, decoder, registry, chart and suite overheads listed separately; revised provisional forecast central ≈ 2.0 CPU-h (k = 2), range ≈ 0.9–4.5; P1 stated to power the R/S* threshold contrasts and the M transmission contrast only; M-share and energy MDEs reported, possibly unresolved at N = 16,384; no assumption on patched-forward variance; the overflow module `c2_stats.py` planned from the start. [Round 3: forecast now central ≈ 2.1 CPU-h, range ≈ 0.9–4.8, from the GLS-REF and descriptive-stream recounts; NEW-1, NEW-5, §12, §20.] | §6.7, §6.8, §12, §13.2, §14 D2, §16 O-10, Appendix A, §18 item 4 |
| RC-16 | MINOR | LayerNorm-ε remark corrected (scale is not removed exactly; the 127-dimensional ambient space is unaffected); the 127-coordinate remark no longer claims a nonsingular empirical covariance (rank/covariance gates kept); the three full M0 `state_sha` strings frozen (from `c1prime-store/GATES.jsonl` line 8), labelled as production `state_sha` values, not checkpoint-file SHA256 | §2.1 remarks (b), (c), §4, §7 row 9, §13.3 T-READOUT, T-G0, §14 D6, §16 O-7 |
| Interpretability addition | — | Descriptive operator decomposition CMP_SΔy = CMP_S(I − J)Δy + CMP_SJΔy (A_S^vis, A_S^null, energies), no projector selection, no outcome change; the y-reflection's limit stated [v2 candidate: the y-translation's, §21] | §0, §2.12, §5.7 (sealed), §13.3 T-PARTITION |
| Open items | — | O-1, O-5, O-6, O-8, O-9 adopted per the review; O-3 adopted (separate nominal 0.05, R uniquely primary, 0.15 displayed); O-7 resolved for the hashes, registry inventory outstanding; O-2, O-3, O-10 and Q4/O-4 for the owner (confirmed by addendum 21) | §16, §18 |

---

## 20. NEW-by-NEW and PARTIAL disposition (Codex confirmation review; all ACCEPTED by the coordinator's round-3 rulings)

**Sources:**
- Review: `coord-c2-review-20261021.v2confirm.codex.md` (sha256 `2b76cf4d…830e`).
- Rulings: `coord-c2-review-20261021.v2confirm.rulings.md` (sha256 `24f9888f…85cb1`).

**Scope of round 3.** Every RC the review confirmed as APPLIED is kept unchanged: RC-2 to RC-9, RC-11, RC-12, RC-15 and RC-16. RC-15's text changed only where NEW-5 and NEW-1 required it: the bootstrap count and the GLS-REF overhead. Nothing in the accepted scientific scope, or in owner addendum 21, is reopened.

| Item | Severity | What changed | Where |
|---|---|---|---|
| **NEW-1** | MAJOR | **The withdrawal.** v2's ε_ref = 16(κ_Σρ_Σ + κ_X̃²ρ_G) is withdrawn, and its four defects are stated. **The replacement.** The reviewer's composed residual bound is adopted and proved as **Lemma GR**: e_Y = ω_A‖R_A‖_F and e_L = ω_G[‖R_G‖_F + ‖R_C‖_F‖L*‖_F + e_Y(1 + ‖X_n‖_F‖L*‖_F)], with the residuals R_A, R_C, R_G taken against the exact float64 inputs. The bound is a posteriori and exact. ω_A and ω_G are the review's a and h, renamed to avoid clashing with existing symbols. **Verified inverse-norm bounds (Lemma INV):** ω_A comes from the float64 inverse V_A and a verified θ̄_A = ‖I − V_A A‖_F < 1. ω_G comes from the Decimal inverse V_G of 𝒢*, with e_G = ‖X_n‖_F e_Y + ‖R_C‖_F ≥ ‖𝒢 − 𝒢*‖_F and θ̄_G < 1. Uninflated float64 condition estimates are never used. **Arithmetic uncertainty:** correctly rounded `Decimal` with traps; ϑ_{q+1} dot-product enclosures on every residual and on the two inverse residuals; 1 ± 1e-70 inflation and deflation of every computed bound. **Acceptance:** ρ_ref = e_L/‖L*‖_F ≤ 1e-20. **Projector uncertainty:** ε*_P = ‖B̂‖_F e_L plus the projector-product enclosure, with the Γ analogue; δ_P ≥ ‖P̂_S − P_S‖_F by the triangle inequality, and it enters the NUM guard. **Euclidean variant:** A = I, Y* = X_n and the X_nᵀX_n system, with F1 conditioning on X_n. **Fixtures:** the review's first-solve error-propagation example, separate R_C and R_G perturbations, Lemma INV, the Euclidean conditioning case and the arithmetic-enclosure case. **Writer's decision:** precision raised from 50 to 80 digits, because at 50 digits the bound is not attainable at the F1 admissibility limits (heuristic ≈ 6e-10 against ≈ 6e-40 at 80 digits). **Cost:** the GLS-REF overhead is recounted (0.037 / 0.098 / 0.295 CPU-h), and the forecast becomes central ≈ 2.1 CPU-h, range ≈ 0.9–4.8, for AUTH. **Fallback not used:** the bound is proved, so the measured-only fallback the rulings allow is not needed | §0; §2.5 (GLS-REF, variants); §7 row 11; §9.1 GLS-REF; §9.2 δ_P; §9.3 T12; §12 (b), (c) and forecast; §13.2 fields 3, files; §13.3 T-GLS; §14 D2; §15 K21; §16 O-10; §17.1 L7; §17.5; §19 RC-10 note; Summary; MD map row 10; Appendix A |
| **NEW-2** | MAJOR | **The order now enforced:** H1 keeps the static artifact and permutation checks and SYMBOL-ORDER (b). The token-map check (a) moves to H2, after sampling and separation; at TEST it runs at H2′. The contrast round trip (c) moves to H3, after the FIT oracle contrasts are constructed; at TEST it runs inside T-PRE, after the TEST oracle, in a stated order. The M0 two-route comparison stays at M0. FIT, FEAS and VAL are sampled only after REG. An explicit gate-order statement is added, plus a T-POLICY gate-order fixture that refuses out-of-order checks and FIT sampling before REG. Every reference to "H1 SYMBOL-ORDER (a)–(c)" is updated | §1.3; §2.3; §2.7; §5.1 FIT row; §7 rows 3, 5, 6, 22, 23 and the order note; §13.1 `c1_oracle` row; §13.3 T-ORDER, T-POLICY; §15 K20 |
| **NEW-3** | MINOR | **Masked features:** m_valid(H) = 1[‖m32(H)‖ > 1e-12] and f*_K = m_valid·(cos kφ*, sin kφ*)_{k=1..K} are defined. The S* FWL uses f*_3, and every L1* decoder uses the target f*_1 ∈ ℝ². φ* = 0 on invalid rows is only a placeholder and never regenerates unmasked (1, 0) targets. **ZERO_CODE:** the threshold is the FIT `inverted_cdf` median modulus of the centred code pair L_B(y − α̂_w), per model and applicable family (R, M, S*). **Order:** the zero overrides are applied before median selection and agreement, by substituting the inputs of the unchanged `c1_gates.v1` (δ* = δ_c = 0 exactly). This was checked against `c1_gates.py` 76–95, where v1 forms δ* itself from atan2(m32) | §0; §2.11 (S* pipeline and the zero rule); §5.5; §6.6 R1, L1*; §9.1 R1; §13.1 `c1_gates` row; §13.2 field 3; §13.3 T-R1 |
| **NEW-4** | MINOR | **Interaction fixture:** it uses cos φ[h − E(h)] with the reviewer's sentence (verbatim), and the fourth-harmonic option is kept beside it. **Excluded-direction fixture:** the nuisance–phase correlation is made imperfect, so the FWL design stays full rank and the code can pass the incremental L1. **Prerequisites:** F1, L1, R1 and RESP_j are asserted before any NOT_USED or LOW_ALIGNED assertion | §13.3 T-SCOPE |
| **NEW-5** | MINOR | **Intervals:** the reviewer's specification is adopted: 5,000 shared whole-row draws, PCG64(620518), two-sided 95% percentile intervals of ratios of resampled indicator-form means, indices shared across models and quantities, and UNDEFINED on a zero or nonfinite denominator, with no discard or redraw. Ranks are 125/4,875 [W]. **Arrays:** 6 numerators + 2 shared denominators per model = 24 arrays. **Count:** 2.17 million TEST tree means, with the bootstrap overhead updated | §2.10; §5.2 seed 620518; §9.1 Bootstrap; §12 (b) bootstrap row, overhead total, (c); §13.3 T-BOOT; Appendix A |
| **NEW-6** | MINOR | **The rule:** the reviewer's endpoint-status rule is adopted (verbatim): NOT_RUN/<gate> if T-PRE fails before endpoint formation; permitted gate and integrity data retained; SEALED_UNSCORED only for arrays already lawfully formed; nothing computed to fulfil a sealing promise. RESP/SPEC exclusions are also NOT_RUN/<gate>, since their arrays are not formed. **Descriptive reporting:** v2's intended descriptive reporting of excluded models is now a separate post-outcome operation, **POST-DESC**. It runs after every family outcome is recorded, gives point values only, is labelled unlicensed, leaves the endpoint status unchanged, and is not run after FAIL_TECHNICAL, INVALID or a pre-ACCEPT exclusion | §3.1 endpoint status; §5.7; §7 scope note and rows 23, 24, 25, 28; §8 S5, S8; §10 endpoint statuses; §13.2 files (`c2_attrib`); §13.3 T-RULES |
| **NEW-7** | MINOR | **The rule:** the M0 two-route rule is now per row: \|s_named − s_canonical\| ≤ 1e-12·max(1, Σ_v\|d_canonical,v z_canonical,v\|), with s the prescribed half-dot-products. **Attainability:** row T18 states the bound 4.0e-15·Σ\|dz\| and a margin ≥ 250 [W]. **Fixture:** a cancellation/zero-result fixture is added to T-ORDER | §7 row 9; §9.3 T18; §13.3 T-ORDER; Appendix A |
| **NEW-8** | MINOR | **Replaced wording:** pending-confirmation wording now reads "confirmed by owner addendum 21" for the claim scope, the restricted ROUTED_AROUND licence, the NOT_RUN exclusions, O-2 and O-3. For O-10, the measure-only budget is confirmed, and the revised forecast is presented at AUTH. **Kept:** the requirement for a future execution AUTH naming the frozen sha256 and the forecast. **Historical text:** the §18 questions are kept and explicitly marked historical, and the §19 cells are annotated | Header (status, review/rulings/owner rows, next step); MD map rows 11 and Q1–Q4; §1.1; §2.9 (two places); §2.10; §3 scope; §6.3 remark 6; §6.5; §9.1 energy row; §12 status and forecast; §14 D1, D11; §15 K21; §16 O-2, O-3, O-4, O-10; §18; §19 |
| **RC-1** (PARTIAL → completed) | BLOCKER | **Completed by NEW-2 and NEW-7.** SYMBOL-ORDER checks run only once their data exist, and the M0 comparison is robust to cancellation. The permutation direction, the reuse list and the non-involutive fixture are unchanged, as confirmed | as NEW-2, NEW-7 |
| **RC-10** (PARTIAL → completed) | MAJOR | **Completed by NEW-1.** The whitened-design rank and conditioning gates and the measured-X1 wording are unchanged, as confirmed. The Decimal-reference acceptance is now the proved composed bound of Lemma GR | as NEW-1 |
| **RC-13** (PARTIAL → completed) | MAJOR | **Completed by NEW-6.** No text promises to seal an endpoint array that cannot yet exist. Owner-approved assessment/NOT_RUN wording and ephemeral X1 are unchanged | as NEW-6 |
| **RC-14** (PARTIAL → completed) | MINOR | **Completed by NEW-3.** The zero-modulus override is an explicit masked-feature definition, with the target dimension fixed (f*_3 for S* regressors, f*_1 for L1* targets). Oracle qualification, orientation and s_rot are unchanged, as confirmed | as NEW-3 |

**Applied with an addition beyond the reviewer's literal text.** Each addition is a writer's decision inside the fix, needed for consistency, and none changes a threshold:
- **NEW-1:** the 50 → 80-digit precision, so that the reviewer's 1e-20 acceptance is attainable; F1's Euclidean conditioning on X_n, implied by the reviewer's defect 4; and the renaming a, h → ω_A, ω_G.
- **NEW-3:** the input-substitution mechanism that keeps `c1_gates.v1` unchanged.
- **NEW-6:** POST-DESC, the reviewer's "separate post-outcome operation", restricted to point values so that no new seed is needed.

**Not applied:** none.

---

## 21. Change log: C2-FROZEN-v1 → C2-FROZEN-v2 (candidate; pre-data protocol change)

**Base.** C2-FROZEN-v1, sha256 `4d97d8e258cfab906ccfe1d99564d4dd74202edd96dd63eb836abd64c277a3d8`. Everything not listed below is v1 byte for byte. The table lists every change.

**Sources:**
- **Owner addendum 23** (binding): `archive/owner-decisions-20261015/OWNER_DECISIONS.addendum-23.md`, sha256 `21c941a14aacf35a2eacd88d1c8310ddc62037136715aef327973fa7c2b135ab`. Option A, verbatim: "A: הזזה טהורה, סף 0.85 (מומלץ)".
- **Job 0104 interim review:** `jobs/0104/review.md`, sha256 `e832173ae90807e1c59383c8976038786c7225f4b145534e4b2f5abd30a79b8a`. It carries D-0104-1, D-0104-2 and R-0104-1.
- **Job 0104 report:** `jobs/0104/report.md`, sha256 `1bb9f3073309d187aaa808e9158ec73407ce40d0d9e9750d9673b794501f0d0d`.
- **Coordinator addenda 1–3 to v1:** sha256 `2db09007…11a8`, `fb6b52e4…21e5` and `5cdfca2f…129e`.
- **Feasibility evidence** (summary files and scripts in `X:/Downloads/topo-scratch/0104/`; no payloads):

| File | sha256 |
|---|---|
| `fy_check.txt` | `ec599fd34cdb33f101ee9ab61846c64d953b07f46c109b1ecaa560aafb0c1168` |
| `fy_alt.txt` | `a56ced392970625f8fb733e98e51c27ab030d37585a02abcd5ce5d448585930a` |
| `fy_check.py` | `95800a89639f07363f2d9e7e84ab0a083c63d1e0f30bd49a1549e9e8b0feb907` |
| `fy_alt.py` | `0e1113ede9939f87895ffa80b51c37c29bc7b4ca9e3dbf35b5b95583327763aa` |
| `fy_alt2.py` | `213f98067cad87cc97bd488384fd395fef1404b65d47a18b8b8675ff28140236` |

**Registered-data status and revision authority.** S1 has not run, and no registered C2 FIT, FEAS, VAL or TEST data or corresponding model endpoints have been generated. Real-process oracle-only feasibility measurements on scratch seeds 999001 and 999002 were nevertheless observed and informed the donor and coverage-threshold choices; their summaries and scripts are recorded above. These measurements are exploratory evidence, not confirmatory C2 results. Owner addendum 23 explicitly authorises this protocol revision and requires independent review and re-freezing. The revision therefore does not rely merely on a namespace distinction or on the absence of persisted history arrays to satisfy S3. Subsequent registered execution requires a new AUTH naming the re-frozen v2 hash.

| # | Change | Reason | Sections touched |
|---|---|---|---|
| C-1 | **The y-placebo donor.** H^R (w1..w31 reflected about y = 5.5, w32 kept) is replaced by the **pure one-symbol-row y-translation donor H^Y**: b → b + k on w1..w31 with k = +1 if ȳ(b31(H)) < 5.5 and −1 otherwise, w32 kept, exactly as in `fy_alt.py`. Symbols: σ, H^R, ρ_R, d^R and A^R become υ_k, k_Y, H^Y, Y_def, d^Y and A^Y | D-0104-1: H^R gives f_y = 0.444, so H4 would fail at S1. Owner addendum 23, option A | §0; Summary; §2.2 (donor, table, no-symmetry paragraph); §2.3 (d^Y; κ_m); §2.6; §2.10 Y2; §2.12; §3 scope; §3.5; §5.2 donors; §5.3 digests; §5.7; §6.1; §6.3 SPEC; §6.6 Y1, Y2; §7 rows 5, 6; §13.1 `c1_oracle` row; §13.2 field 3 and the `c2_data`, `c2_oracle` rows; §13.3 T-ORACLE; §19 two historical cells annotated |
| C-2 | **Ineligibility, no clamp or wrap.** A row whose shifted prefix would leave rows 0..5 is ineligible for the y placebo (OFF_GRID_Y). It is counted in the coverage tally and in f_y's denominator, no H^Y is formed for it, and its indicator-form y-pair value is 0. Coverage reasons S_REFL and LIK_REFL become S_Y and LIK_Y | D-0104-1; owner addendum 23 (coordinator reading: "counted in coverage") | §0; §2.2; §5.2; §5.4 E_y; §5.5; §6.1 indicator form |
| C-3 | **H4 threshold.** f_y ≥ 0.85 (was 0.90); f_x ≥ 0.90 unchanged | Owner addendum 23 | §5.4; §7 row 7; §9.1 |
| C-4 | **The H3 y check.** H^Y has no closed-form symmetry. So the ρ_R symmetry report, the closed form b32(H^R) and the ε_sym^R bound are removed. The H^Y oracle quantities are the exact oracle forward (`BayesFilter`), checked by the Decimal reference rows (the 4 lowest-id E_y rows per split), and no ε_sym bound applies. T2 is withdrawn, keeping the row numbering; T3 is x pair only | D-0104-1 | §2.2; §7 row 6; §9.3 T2, T3 |
| C-5 | **The x leakage of the y pair, a known property.** Pre-data, it is about 0.2% of the x contrast at b31 (0.0035 against 1.5915; 0.0161 at b32). It is stated, and reported descriptively as λ_x per split. Two new risks (K22 H4 margin, K23 leakage) | D-0104-1 (coordinator instruction) | §2.2; §2.12; §3.5; §15 K22, K23 |
| C-6 | **The F1 G1 identity check in a whitened, scale-invariant form**, on every problem (R, M and S*, and the R variants). The dimensionless identities stay at absolute 1e-10. P_SΓ and P_ΓB get relative bounds (≤ 1e-10·‖Γ‖_max and ≤ 1e-10·‖B‖_max). W-self-adjointness becomes ‖P̃ − P̃ᵀ‖_max ≤ 1e-10 for P̃ = R_Σ^{−ᵀ}P̂R_Σᵀ. A scale-invariance fixture is added | D-0104-2: v1's absolute check of WP − PᵀW scales with 1/λ_min(Σ_ε) and was unattainable at the M problem (2e-9 in the synthetic dry run) | §2.5 (Lemma G1, its proof, the new check paragraph); §7 row 11; §9.1 F1; §9.3 T11; §13.3 T-GLS; §15 K9 |
| C-7 | **Footprint: 14 modules**, the ten v1 modules plus `c2_stage_base`, `c2_stage_pre`, `c2_stage_val` and `c2_stage_post`. Each is ≤ 400 lines, with a ceiling of 5,600. The driver becomes infrastructure plus the lazy dispatch. The row-to-module assignment is fixed by an `API.md` erratum | R-0104-1 (supersedes coordinator addendum 3: 12 modules, 4,800) | §13.2 files table and planned-lines sentence; §13.3 T-SIZE; §15 K16 |
| C-8 | **Cost.** The y-pair forward and oracle counts are now upper bounds, about 2% of row-forwards fewer at k = 2. The forecast is unchanged: central ≈ 2.1 CPU-h (k = 2), range ≈ 0.9–4.8 | Consequence of C-1, C-2 and C-7 | §12 (FEAS and S4 rows, oracle row, a new v2-candidate bullet, a historical note) |
| C-9 | **Carried coordinator addenda.** Addendum 1: R = d44548b. Addendum 2: E-0102-1, the `errors.py` abbreviation reads `8aa309c4…b99f` and the full sha256 binds; E-0102-2, the PF file-size scope. Addendum 3 is superseded by C-7 | The addenda carry into v2 (coordinator instruction) | §5.6; §7 row 2; §13.1; §13.5 |
| C-10 | **Metadata and process.** The status line, the title, a header row for this revision and the next-step row. §14 D1 adds the v2 confirmation and re-freeze; §14 D2 now requires an AUTH naming the re-frozen sha256 | Owner addendum 23 ("C2-FROZEN-v2 needs a Codex review before it is frozen again"); gate 0b names the frozen sha256 | Header; §14 D1, D2 |

**Unchanged.**
- Every threshold except H4's f_y, and every tolerance except the form of F1's G1 identity check.
- Every seed, split size, site, K, covariate set, projector, chart and family structure.
- Every outcome rule, every multiplicity argument, and the licence wording, except the donor's name and the added "not x-neutral" non-claim (§3.5).
- The data scope tag `c2-v1`.

**Writer's decisions inside the changes:**
- **Whitening convention.** The check "P̃ = R_ΣPR_Σ⁻¹ symmetric" is written in this protocol's factor convention Σ̂_ε = R_ΣᵀR_Σ (§2.5), in which the symmetric whitened matrix is P̃ = R_Σ^{−ᵀ}PR_Σᵀ = ΩPΩ⁻¹, with Ω = R_Σ^{−ᵀ} the whitening map. In that convention, R_ΣPR_Σ⁻¹ itself is not symmetric (a synthetic check with random matrices, no data, showed an asymmetry of order 10).
- **Normalisation of the relative bounds:** ‖Γ‖_max and ‖B‖_max, the units those two products carry.
- **An OFF_GRID_Y row forms no H^Y at all:** no tokens, digest, oracle or forward.
- **Renaming:** ^R → ^Y and S_REFL → S_Y, to avoid any reading of a reflection. T2 is withdrawn rather than renumbered.
- **Cost:** the forecast is kept as a conservative bound instead of being recounted downward.
- **Additions:** the §3.5 non-claim, and the two risks K22 and K23.

**For the coordinator (outside the protocol text):**
1. **AUTH.** Gate 0b needs an owner AUTH naming the re-frozen v2 sha256; owner addendum 22 named v1's.
2. **G0 byte copy.** The sole active repository byte copy at H is `tools/c2_readout/PROTOCOL_C2_v2.md`, byte-identical to the re-frozen v2 document. Remove `tools/c2_readout/PROTOCOL_C2_v1.md` from the execution branch’s final tree before H. Update implementation bindings, CONTRACT metadata and integrity tests to the v2 path and hash. Historical v1 records remain archived.
3. **The independent authors' updates:** T-ORACLE, the T-GLS scale-invariance fixture and T-SIZE. Also the coverage reason names S_Y, LIK_Y and OFF_GRID_Y.
4. **The `API.md` erratum** for the stage split (R-0104-1).
