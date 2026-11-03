STATUS: HWSU-DESIGN-v1: design freeze candidate (HWSU-v2 + F-1..F-7, J9, S-1..S-3); J10; D-1..D-3

# HWSU-DESIGN-v1: track U. Does the readout of the three stage-C models use the beyond-four information that their circle carries?

**Revision v2.** v1 is `ah/planning/responses/coord-hws-use-20261101.claude.md` (sha256 7ca3bb77…62ca), unchanged. v2 applies the following inputs, each verified with `sha256sum` before reading:
- the result-blind review `coord-hws-use-20261101.claude-reviewer.md` (sha256 20b010d2…dc4d46; VERDICT: CONFIRM_AFTER_MINOR_FIXES): RC-1..RC-12 with the reviewer's replacement or insertion text verbatim;
- the coordinator's rulings `coord-hws-use-20261101.rulings.md` (sha256 1d074b4d…0c7c1f): RC-1..RC-12 accepted; S1–S8 as ruled;
- the joint rulings for tracks U and D, `coord-hws-ud-20261101.joint-rulings.md` (sha256 641502e8…f9546f): J1–J7;
- the mailbox records `ah/records/HWSC_W2_END.json` (sha256 2390e29d58add4a65025559785f0e67c49291625847c0511d8b6321a9c03c6cb) and `ah/records/HWS_UD_NAMESPACE.json` (sha256 b4c6d6ff21ad6282c530a2c9e992c4973836ed0750c6cca06db4704ddd427b5e). The track-D reserved tokens they name are treated as declared needles.

Every change is listed in the final section, "Change log v1 → v2". No other text was changed.

**Design freeze candidate.** HWSU-DESIGN-v1 = HWSU-v2 (sha256 c51efe50…a750, unchanged on disk) with the following applied:
- F-1..F-7 of the confirmation read `coord-hws-use-20261101.v2confirm.claude-reviewer.md` (sha256 3b7cd637…81d9; VERDICT: CONFIRM_AFTER_MINOR_FIXES), with the reviewer's exact text;
- joint ruling J9 (`coord-hws-ud-20261101.joint-rulings-addendum-2.md`, sha256 6644433a…d9b5);
- suggestions S-1..S-3, as ruled in `coord-hws-use-20261101.v2confirm.rulings.md` (sha256 5e734dcf…47e8);
- joint ruling J10 (`coord-hws-ud-20261101.joint-rulings-addendum-3.md`, sha256 127d08fe…c092).

Each input was verified with `sha256sum` before reading. The rows are in "Change log HWSU-v2 → HWSU-DESIGN-v1" at the end.

**Round:** `coord-hws-use-20261101`. **Request:** `ah/planning/requests/coord-hws-use-20261101.md`, sha256 `2822c5c5916a97067f43bfde99639e2a71221405dc55d243cdf839ee58c07c9c`, verified by the writer with `sha256sum` before reading [V]. **Track:** L only (Codex frozen, addendum 28; PLANNING_PROTOCOL rule 5). **Writer:** a clean-context Claude subagent of coordinator d9a66698, 2026-11-01. The parallel round `coord-hws-dyn-20261101` (track D) and any `HWSD-*` file were not opened.
**Authority:** owner addendum 37 item 1 approves planning, result-blind review, a design freeze candidate, implementation with independent tests and a synthetic dry run, up to an execution freeze. **No real-scope run is approved:** no draw of protected histories and no scoring of real models (addendum 37 item 2). Addenda 25 (working rules) and 26 (adaptive budget) apply.
**Base code:** topo-pilot main `8f89462`. `.venv/Scripts/python.exe tools/build_code_index.py --check` printed "code index is current" (exit 0) [V].
**Planning only.** The writer ran no sampling, training, tests, drivers or oracle computation, and wrote no file except this one. No `payload.npz`, `state.pt`, `sealed/` file, `hist/**` array, `HIST_*.npz`, chart or activation `.npz`, or checkpoint payload was opened or hashed. The writer hashed only JSON records (§14).

**Labels.** **[V]**: checked by the writer against code or a record (file:line or JSON key). **[H]**: an inherited record value. **[W]**: the writer's desk arithmetic or design reasoning. **No [W] or [H] value is a gate threshold.** Every gate threshold below is a registered constant: C2's owner-approved lines, or exact multiples of them that this plan fixes now. Every gated quantity is computed by the run.

**Paths.** `tp/` = `X:/Downloads/projects/topo-pilot/topo-pilot` (main 8f89462). `ah/` = `X:/Downloads/projects/topo-pilot/agent-handoff`. `root/` = `X:/Downloads/projects/topo-pilot`. `scratch/` = `X:/Downloads/topo-scratch`. **Protocols:** C2 = `ah/planning/responses/C2-FROZEN-v2.md`; C2ND = `C2ND-FROZEN-v1.md`; K4B = `K4B-FROZEN-v1.md`; HWSC = `HWSC-DESIGN-v1.md` (the stage-C freeze, sha256 f0f2396c…a100a9, equal to RESULT.json `protocol_sha256` [V]).

---

## Summary (≤ 300 words)

**Question.** Stage C showed that the gauged chart phase of the three stage-C models (masters 620301–620303, step 5000, `resid_post_3`, position 32) **carries** beyond-four information. Track U asks whether the model's **prediction uses** it. When only the history before the last four symbols changes, does the next-symbol prediction move the way the oracle's moves (θ)? And what share of that oracle-aligned move runs through the circle code (ψ)?

**Design.** Natural suffix-matched pairs: arm 1 is a process draw; arm 2 keeps arm 1's last four symbols and redraws the prefix exactly from its conditional law given those symbols. Both arms are process-distributed. Any function of the last four symbols is identical across a pair (Lemma P1), so every response measured on the pairs is beyond-four by construction. On pairs, the code interchange moves exactly the code's beyond-four component (Lemma P3). Attribution is C2's exact linear readout after the final LayerNorm (Lemma R). The code is C2's registered recipe (FWL harmonics 1–3 of the frozen **stage-C** chart phase, 5 nuisance covariates, GLS), refitted on fresh histories.

**Oracle feasibility first.** Stage OF is oracle-only: its own metered job and owner approval, run before the model part is implemented. It checks the following:
- the oracle's own response E[G], with E[G] ≥ G4 (Lemma J);
- the share of the oracle's response carried by an oracle-phase code (ψ_orc), required ≥ 2 × 0.10;
- exact oracle known cases, the pair sampler, and a hygiene gate on the oracle-only rows.

OF has its own execution freeze, `FREEZE_OF.json`. A failed share ceiling stops only the share part; the response part may still go to the owner (S3).

**Outcomes.** Response: RESPONDS / WEAK_RESPONSE / LOW_RESPONSE, plus a "positive but below margin" statement. Share: USED / PARTIAL / NOT_USED / LOW_ALIGNED_SHARE, plus a "positive but below margin" statement. Both use 2-of-3 claims with every model reported, at family error 15α = 0.05 (α = 1/300). Technical and INCONCLUSIVE outcomes are registered. Known cases on real activations (a planted code reader, C2ND's null-head decoy, a decoy code) and on the oracle are checked before the endpoint.

**Cost (central).** About 1,800 CPU-s for phase OF. About 10,050–14,950 CPU-s for the model phase at test sizes from 4,096 to 32,768 pairs, including the expected test, dry-run, KC and registry repeats. Overall about 3.3–4.7 CPU-h, no training, with 3× pauses.

---

## 1. The question

### 1.1 Where things stand
- **Stage C** (HWSC; outcome `ah/jobs/0196/review.md`) [V] tested three new models in w\* = W12-q1-s1.75-p0.2 (masters 620301–620303, step 5000, `resid_post_3`, position 32). The registered outcome was **SUPPORT** in 3/3: per-model lower bounds of E[u·r4] after F of 0.0406 / 0.0395 / 0.0402, against M = 0.01. The oracle comparator Δ4_orc was 0.0473, and E X⁻/Δ4_orc was 0.925 / 0.894 / 0.918 [H, `hwsc-store/stages/S8/RESULT.json` keys `per_model.*.L`, `controls.delta4_orc`, `ratios`].
  - The suffix-only controls were near zero: m4-phase lower bound −0.0017; SHA-of-suffix lower bound −0.0039; suffix decoder lower bound about −0.003 [H, same file, `controls`]. Support was 3,072/3,072 per model [H].
  - The licence: the chart phase is not a function of the last four observations; it depends on earlier ones, aligned with the oracle belief residual.
  - **What stage C does not show:** whether the model's prediction depends on that information.
- **C2** (E4 models in w0, ±2-cell x-history rotations with w32 kept) found **USED**: ψ̂ ≈ 0.85 of the model's signed oracle-aligned response ran through the registered 6-d circle code at `ln_final_out`/32 (`ah/jobs/0115/review.md`) [V].
  - **C2ND** found the complement CODE_DOMINANT (1 − ψ ≈ 0.15). The null-head decoy returned DECOY_NOT_USED (ψ̂′ 0.020–0.028) (`ah/jobs/0167/review.md`) [V].
  - C2's counterfactual changed w31 and the whole prefix. It did not separate beyond-four history from the recent symbols (C2 §1.3 "E-short: not separated") [V].

### 1.2 The registered question (two parts, one error family)
For each stage-C model j, take natural pairs (H¹, H²) of process-drawn histories that share w29..w32 (§2.1):
- **U-RESP (does the prediction move with beyond-four history, in the oracle's direction?).** The registered response is θ_j = E[A_full]/E[G], with A_full = ½dᵀ(z¹ − z²), d = q̄¹ − q̄² (the oracle's next-symbol predictive) and G = ½Σ_v d_v(log q̄¹_v − log q̄²_v) (the oracle's own response) (§2.5). θ is the model's signed oracle-aligned response as a fraction of the oracle's.
- **U-SHARE (how much of that response is carried by the circle code?).** The registered share is ψ_j = E[A_S]/E[A_full], with A_S = ½dᵀM P_S(y¹ − y²). This is the response of the registered circle-code interchange at `ln_final_out`/32 (C2 Lemma D1). On suffix-matched pairs it is exactly the interchange of the code's beyond-four component (Lemma P3). It is assessed only in models whose response is declared above 0.30 (RESPONDS).

Track U is a new study. It is not C2, not a rescue of C2, and not part of stage C. Its results are never pooled with C2, C2ND, K4b, E4 or stage-C results. It changes no earlier verdict.

### 1.3 Competing explanations [W]
| Explanation | What discriminates it |
|---|---|
| E-suf: the prediction depends only on the last four symbols (the circle's beyond-four content is carried but not read) | A_full ≡ 0 on every pair for any such predictor (Lemma P1); LOW_RESPONSE certifies θ < 0.10 |
| E-use: the beyond-four response runs mainly through the circle code | ψ > 0.50 (USED) with RESPONDS |
| E-share: the circle code carries part of it, other directions the rest | 0.10 < ψ < 0.50 (PARTIAL); ψ_Γ, ψ_rest reported |
| E-bypass: the model responds through non-code directions (y-belief, concentration, other encodings) | ψ < 0.10 and bounded energy (NOT_USED); descriptive ψ_Γ, ψ_rest, S\* share |
| E-orth / E-cancel: the code moves the logits orthogonally to d, or with cancelling signs | LOW_ALIGNED_SHARE, never NOT_USED (energy conjuncts, C2 §2.9) |
| E-method: the recipe manufactures a share from any fitted 6-d subspace, or from an unread code | known cases KU2 (code present, readout null) and KU3 (decoy code) at VAL (§5) |
| E-ceiling: the circle can carry only part of the oracle's beyond-four response (the rest is y- or shape-information) | the oracle-ideal share ψ_orc (§4); reported beside every share outcome |
| E-power: an unresolved result is a lack of precision | the P1 ladder (blind), the OF precision proxy, and INCONCLUSIVE/PRECISION (never read as non-use) |
| E-artifact: a pipeline, sampler, symbol-order or index defect | exact sampler known cases, Lemma P cross-check, M0, X1, SYMBOL-ORDER, GLS-REF, H3-U |

### 1.4 Prior expectation (stated now; the writer has read the stage-C outcome)
The stage-C circle carries about 0.9 of the oracle comparator's beyond-four phase covariance [H]. If the models read their circle at the end, as the E4 models did in C2, U-RESP should be RESPONDS and U-SHARE USED or PARTIAL.

The oracle-ideal share is unknown before OF. Stage A recorded G4^A/G4 ≈ 0.018/0.031 ≈ 0.59 (lower bounds, `ah/jobs/0136/review.md:5`) [H]: the circular-label part of the beyond-four predictive gain is about 59 % of the total [W]. **Even an ideal circle reader may therefore sit near the 0.50 line.** PARTIAL is a likely and informative outcome, not a failure (§4.3).

A NOT_USED or LOW_RESPONSE result would be the surprise.

### 1.5 Scope
- **Models:** the three stage-C models, unchanged (step 5000; masters 620301–620303). No training.
- **Sites:**
  - circle variable at `resid_post_3`/32 through the **frozen stage-C production charts** (by sha256);
  - attribution at `ln_final_out`/32.
- **Position:** 32 only.
- **Counterfactual:** the natural suffix-matched pair family of §2.1 only.
- **Not in scope:**
  - the layer-2 interchange (C2-M), a deferred extension;
  - other positions or horizons;
  - track D's questions;
  - other worlds (addendum 37 item 3).

---

## 2. The design

### 2.1 The counterfactual family: natural suffix-matched pairs
**Process facts.**
- The sampler draws z₁ ~ π; for t = 1..33 it emits w_t ~ E[z_t, ·] and then draws z_{t+1} ~ T[z_t, ·] (`tp/src/topo_pilot/dataset/sampler.py:1, 69-80`) [V].
- The model input is [BOS = 36, perm_j(w1..w32)]. Position 32 predicts w33.
- w\* is the 12 × 12 cylinder, stay 0.2, overlap emission σ = 7/4, alphabet 36 (HWSC §2.2–§2.3) [V].

**Pair construction (per split block of n pairs).**
1. **Arm 1.** `HMMSampler(T, E_canon, π, SequenceLayout()).sample(n, rng₁)`, once per block. rng₁ = `SeedTree(0).generator("data", SCOPE, split, block, "cylinder", "overlap", "1.75")`. This is the K4b/HWSC block pattern (`tp/tools/hwsc/hwsc_data.py:98-117`) [V]. w33 and the states are dropped at once.
2. **Arm 2 (the exact conditional prefix sampler, new: `hwsu_pairs.sample_prefix`).** For each row, with suffix s = (w29, w30, w31, w32) of arm 1:
   - **(a) backward messages:** β₃₂ ≡ 1; β_t(z) = Σ_{z′} T[z, z′]·E[z′, w_{t+1}]·β_{t+1}(z′) for t = 31, 30, 29, 28. This gives β₂₈(z) = P(w29..w32 | z₂₈ = z).
   - **(b) the bridge state:** draw z₂₈ from P(z₂₈ = z | s) ∝ π₂₈(z)·β₂₈(z), with π₂₈ = π (stationarity, gated: ‖πT − π‖∞ ≤ 1e-12).
   - **(c) the past, backwards:** for t = 28 down to 1, draw w_t ~ E[z_t, ·], then (t > 1) z_{t−1} ~ T̃[z_t, ·]. The time reversal is T̃[z, z′] = π(z′)T[z′, z]/π(z), computed in general and never assumed equal to T.
   - **(d) the arm:** arm 2 = (w′1..w′28, w29..w32), with the suffix copied bitwise.
   - The draws come from rng₂ = `SeedTree(0).generator("data", SCOPE, split + "/cf", block, *PROC)`, in a frozen order: n uniforms for z₂₈, then per t an emission uniform and a transition uniform. Inverse CDF uses `_cumulative_rows`/`_draw` semantics (`sampler.py:12-30`) [V], so a zero-probability column is never drawn.
   - **Row order and pairing (S2).** Arm-2 draws and `a2` sequence ids are produced in arm 1's sorted (sequence-id) row order. The pairing is by row index; arm 2's ids are never sorted.

**Lemma P0 (naturalness and exchangeability) [W, standard].** Under the stationary HMM, (z₁..z₂₇, w₁..w₂₈) ⊥ (w₂₉..w₃₂) | z₂₈, and the reversed chain of a stationary chain has kernel T̃. So steps (a)–(c) draw arm 2's prefix exactly from P(w₁..w₂₈ | w₂₉..w₃₂). Consequences:
- (i) arm 2 is distributed as the process (P(s)·P(prefix | s) = P(H));
- (ii) H¹ and H² are conditionally iid given s, so the pair is exchangeable;
- (iii) the support is every positive-probability history. Under overlap emission every symbol has positive probability from every state [W], so every prefix has positive probability given every suffix;
- (iv) no eligibility screen is needed: both arms are natural draws.

A finite log-evidence check on every arm stays a gate (H3-U). A failure there is a sampler defect, never an exclusion.

**Why pairs, and not single rows with the exact suffix predictive [W].** By Lemma P2, the pair estimand equals the single-row form E[ρ4ᵀz], with ρ4 = q̄32 − q̄4. In the single-row form, the large suffix-determined part of the logits, g(s), adds variance through ρ4ᵀg(s). The pair difference removes g(s) exactly. The single-row form is computed as a descriptive cross-check (§2.6).

**Rejected alternatives [W].**
- **Matching independent draws on their last four symbols:** 36⁴ ≈ 1.7 M suffixes make exact matches rare.
- **More than two prefixes per suffix:** a later efficiency extension.
- **Shifted or rotated prefixes (C2's donors):** not natural, and they change w31.

### 2.2 What a pair preserves (exact lemmas)
- **Lemma P1 (suffix invariance).** Any function g of (w29..w32) satisfies g(H¹) = g(H²) bitwise. In particular:
  - the suffix-only belief and moments m4, q4 are identical across the arms;
  - d = q̄32¹ − q̄32² = ρ4¹ − ρ4²;
  - for any predictor whose logits depend on the last four symbols only, A_full ≡ 0 on every pair. The same holds for any code that depends on the last four symbols only: Δc ≡ 0 and A_S ≡ 0. *Proof:* identical inputs give identical outputs. ∎
- **Lemma P2 (pair covariance identity).** For conditionally iid arms and any square-integrable a, b: ½E[(a¹ − a²)ᵀ(b¹ − b²)] = E[Cov(a, b | S4)] = E[(a − E[a|S4])ᵀ(b − E[b|S4])]. With b = q̄32 and E[q̄32 | S4] = q̄4 (tower property; stationarity makes the suffix-only predictive the conditional expectation), **E[A_full] = E[zᵀρ4]**. With b = m32 and a = u (the chart unit vector), the pair statistic ½(Δu)·(Δm32) has mean **E[u·r4]**, stage C's estimand. *Proof:* expand; the cross terms factor by conditional independence. ∎ It is checked numerically in OF-5 and reported in U.
- **Lemma P3 (the code interchange moves exactly the beyond-four component).** Write the code coordinates as c = L_B(y − α_{w32}), and split them any way as c = h(S4) + c_b. Then Δc = Δc_b on every pair, exactly. So P_SΔy and A_S (Lemma D1) are the interchange of the beyond-four component of the code; **the circle code's share and its beyond-four component's share are the same quantity on these pairs**. *Proof:* Lemma P1 applied to h; α_{w32} is shared. ∎
- **Lemma J (the oracle's own response).** E[G] = E[KL(q32 ‖ q4)] + E[KL(q4 ‖ q32)] = G4 + G4^rev ≥ G4. *Proof:* by exchangeability, E[G] = E[q̄·log q̄] − E[q̄¹·log q̄²]. Given S4, E[q̄¹·log q̄² | S4] = q̄4·E[log q̄ | S4], and E[q̄·log q̄4] = E[q̄4·log q̄4]. ∎ Stage A recorded L3(G4) = 0.03093 nats at w\* (`ah/jobs/0136/review.md:5`) [H]. So E[G] ≥ 0.031 [W from H], and to second order E[G] ≈ 2·G4 ≈ 0.062 nats [W].

### 2.3 Oracle quantities per arm and pair
For each arm, `c2_oracle.oracle_role(T, E, π, tokens32, coords)` gives b31, b32, q, q̄, surprisal, log-evidence and m32 (`tp/tools/c2_readout/c2_oracle.py:87-101`) [V]. This is the operational oracle `c1_oracle.run_oracle` (`tp/tools/c1prime/c1_oracle.py:126`) [V], with w\*'s T, E_canon and π passed explicitly.

New, in `hwsu_oracle`:
- **q4 (the suffix-only predictive):** filter w29..w32 from π, then predict;
- **m4:** checked against `oracle_profile.posterior_means(…, K = 4, …)`, as used by K4b (`tp/tools/k4b/k4b_scores.py:20-24`; `tp/tools/x4_oracle_profile/oracle_profile.py:155`) [V];
- **d and G:** via `c1_oracle.G_hat` (`c1_oracle.py:139`) [V];
- **the named order:** d_named = `c1_oracle.named_from_canonical(d, perm_j)` per model (`c1_oracle.py:146`) [V];
- **the 5 nuisance covariates** of each arm: `c2_oracle.nuisance5` (`c2_oracle.py:137-145`) [V].

### 2.4 Sites, position, chart, and the circle code (and its beyond-four component)
- **Circle variable.** φ_j(H) = the gauged phase of the **stage-C production chart** of model j, extended to the row's `resid_post_3`/32 float64 activation by `k4b_charts.extend(prod, gauge, Q, cfg)` (`tp/tools/k4b/k4b_charts.py:168-174`) [V]. The configuration is `k4b_config.chart_cfg()`, unchanged.
  - Charts are bound by `hwsc-store/stages/S4a/PRODUCTION_FROZEN.json` (sha256 17da0ee8…ba36 [V]), whose `files` give CHART_620301/2/3.npz = 808f4bf3…45e8, b4458c20…d2d8, f8fcd886…b043, and whose `gauges` give the stored gauges [V].
  - The run checks each file's sha256 before loading. No chart is refitted and no new chart is constructed: the stage-C C0-cal and C0-val passed on these charts [H, `ah/jobs/0191/review.md`]. Support on new rows is gated (SUP, §6).
- **Readout coordinates (C2 Lemma R).** y = Q₀ᵀ(u − β) ∈ ℝ¹²⁷, M = W_U Q₀, z = W_Uβ + My, built from `c2_model.readout_basis` (`tp/tools/c2_readout/c2_model.py:114-136`) [V].
  - The stage-C architecture equals E4's: 4 layers, d_model 128, LayerNorm, bias-free unembed (HWSC §2.3) [V]. So Lemma R transfers verbatim. Gate BASIS checks rank 127 per model.
- **The registered circle code (C2-R recipe, refitted).** FWL on FIT singles: y = α_{w32} + Γz̃ + B f(φ) + ε, with:
  - K = 3 harmonics (47 design columns);
  - z̃ = the 5 standardised nuisance covariates;
  - Ledoit–Wolf Σ_ε, GLS L = 𝒢⁻¹X_nᵀW, and P_S = B L_B.
  - This is `c2_code.problem` (`tp/tools/c2_readout/c2_code.py:287-307`) with `harmonics`, `fwl`, `gls` and `gls_identities` (:37, :50, :104, :136), and GLS-REF `c2_stats.gls_ref` with δ_P (`c2_stats.py:185, 205`) [V], all unchanged.
- **Its beyond-four component.** The per-row code value is c(H) = L_B(y − α̂_{w32}) (`c2_code.code_pair`, :171) [V]. The per-pair beyond-four component is Δc = c(H¹) − c(H²) = Δc_b, exactly by Lemma P3; it is computed as the difference of the two arms' code values. No separate projection is needed or used.
  - Reported (descriptive): the beyond-four fraction of code variance, ½E‖Δc‖²/tr Cov(c); and the same fraction for the chart unit vector u.

### 2.5 Estimands and attribution
For each pair and model, with y¹, y² the natural readout coordinates and Δy = y¹ − y²:
- A_full = ½dᵀMΔy, the network's own logit difference (gate X1);
- A_S = ½dᵀMP_SΔy, A_Γ = ½dᵀMP_ΓΔy and A_rest = A_full − A_S − A_Γ (`c2_attrib.partition`, `pair`, `tp/tools/c2_readout/c2_attrib.py:62, 87-92`) [V];
- the energies e_full = ‖CMΔy‖² and e_S = ‖CMP_SΔy‖², and the exact random-6-plane energy reference r (Lemma RS2, n = 127, k = 6; `c2_attrib.random_ref`, :77-84) [V].

A_S is the interventional effect of setting the code of one arm to the other's, with every other GLS coordinate held (C2 Lemmas D1, G2) [V]. On these pairs that is exactly the beyond-four component of the code (Lemma P3).

**Per-model estimands.**
- θ_j = E[A_full]/E[G] (response). For a suffix-only predictor θ = 0 exactly (Lemma P1). For the oracle θ = 1 exactly (C2 Lemma D2).
- ψ_j = E[A_S]/E[A_full] (share; defined when E[A_full] > 0).
- θ_S,j = E[A_S]/E[G], and ψ_Γ, ψ_rest (reported).

**Indicator form.** Every pair is eligible (Lemma P0), so E ≡ 1. The C2 array kernels apply with E = all rows.

### 2.6 Controls and descriptive quantities
| Control | Construction | Role |
|---|---|---|
| Oracle comparator ψ_orc (problem O) | C2-S\*'s recipe applied to the **oracle as a model**. The readout coordinates are the Helmert coordinates of log q̄ (35-d), with M = N₃₆. The code uses harmonics 1–3 of the masked oracle phase φ\* = arg m32 (`c2_code.fstar`, :280) [V], with the same 36 classes and 5 covariates, refitted on FIT. A°_full = G exactly (Lemma D2); ψ_orc = E[A°_S]/E[G] | OF gate (§4) and the comparator printed beside every share outcome, as Δ4_orc was in stage C |
| Projector and harmonic variants | R_E (Euclidean complement), R_K1, R_K2 on FIT (C2 §2.5) | qualifiers PROJECTOR_DEPENDENT(j) and HARMONIC_DEPENDENT(j, K) via `c2_decide.variant_category` (:164) [V] |
| Oracle-phase code S\* on the model readout | C2-S\* recipe (φ\* in place of φ) | descriptive ψ\*_j; never a substitute for ψ_j |
| Decoy code (KU3) | the same recipe with φ replaced by the SHA-of-suffix phase `k4b_scores.sha_phase` (:49-51) [V], a variable that is a hash of w29..w32 (no circle, no beyond-four content) | known case: must not return USED (§5) |
| Null-head decoy (KU2) | C2ND D-NULL head edit W′_U = g·W_U(I − Q₀P_S^K Q₀ᵀ) with **g = 1**, built from the KFIT projector P_S^K (`tp/tools/c2_nd/nd_decoy.py:63-76`, called with g explicit) [V] | known case: code carried bitwise, read exactly zero |
| Planted code reader (KU1) | head edit W′_U = K L_B^K Q₀ᵀ. K (36 × 6) is the OLS fit on KFIT pairs of the oracle's centred Δlog q̄ (named order) on Δc^K. It uses activations and oracle quantities only, never model logits | known case: the readout uses only the code's beyond-four component, ψ′ = 1 under construction |
| Oracle dose cases (KO1–KO3) | logits log q̄32 (θ = 1), log q̄4 (θ = 0), and log q̄4 + λ(log q̄32 − log q̄4) with λ = 1/5 (θ = 1/5 exactly) | exact known cases for the response rules (§5) |

**Rejected control: the m4-phase code [W].** A code fitted on harmonics of arg m4 spans x-phase directions of the readout, much like the chart code. It would therefore legitimately capture the response. The m4-phase *variable* is constant within a pair, but the fitted *subspace* is not a null, so it is not used as a decoy. The SHA-of-suffix phase has no phase geometry and is used instead.

**Descriptive (reported, never decision-bearing):**
- the sign-agreement fraction P(A_full > 0);
- E|A_S| and its Cauchy–Schwarz bound;
- the operator decomposition A_S^vis/A_S^null (`c2_attrib.decomposition`, :104) [V];
- ψ_max;
- the single-row cross-check E[zᵀρ4] versus the pair estimate (Lemma P2);
- the chart-phase pair statistic ½Δu·Δm32 on fresh pairs (Lemma P2: a fresh-data replication of stage C's quantity, descriptive);
- 32 empirical Haar 6-frames (drawn by `hwsu_gates.haar_frames_u`, §11.2);
- ψ_comp = 1 − ψ, which is an identity (C2ND Lemma N1), not a necessity test;
- the radial/tangential split of the first-harmonic code change: the share of A_S carried by the change of the code pair's modulus versus its phase (`c2_code.code_phase`, per arm), descriptive (RC-9);
- **the axial share (S1; descriptive, a stand-in for the missing y-placebo).** The oracle change d is split into the part that changes the circular-label marginal and the part that changes the axial-label marginal, using the same label map as G4^A: with v = 6a + b, d_ax,v := Δm_ax(b)·q̃(v | b). Here m_ax(b) = Σ_a q̄(6a + b) is the axial-label marginal, Δm_ax = m_ax¹ − m_ax², and q̃(v | b) is the pair-averaged conditional of v given its axial label; d_circ is defined in the same way from the circular label. The reported quantity is the code's axial contribution ½d_axᵀMP_SΔy as a fraction of ½d_axᵀMΔy, and the same for d_circ. **(S-1)** d_ax and d_circ are formed in canonical order, where v = 6a + b holds (`tools/hws/hws_worlds.py:59, 139-141, 171-180`, per the confirmation read). They are mapped by `named_from_canonical(·, perm_j)` per model before ½d_axᵀMP_SΔy is taken. A large axial fraction sharpens SPECIFICITY_NOT_ESTABLISHED;
- **the chart check on fresh rows (S6; descriptive, not a gate).** A C0v-style fidelity check on the 512 lowest-id FEAS rows: a direct chart per model against the production chart, with C2's C0v thresholds (support ≥ 507/512, fidelity ≥ 0.80, 12 bins ≥ 8 rows, resultant ≤ 0.30). It is reported only; no exclusion follows from it.
  - Forecast cost ≈ 300 CPU-s for three direct chart constructions [W from H: stage C's E1, 1,578.2 CPU-s, contained K-REG1 (291 s) and all of its chart constructions].
  - That is below 5 % of the model-phase central (≥ 10,050 CPU-s, so ≥ 502 CPU-s), so S6 is adopted as ruled.
  - It is booked inside E1, whose itemisation (REG1 ≈ 290, oracle ≈ 250, fits ≈ 300, feas ≈ 200, val and KC-U ≈ 500, the G0U needle search ≈ 490 (§4.4), H1 ≈ 50, and this check ≈ 300) sums to ≈ 2,380 [W]. E1's registered central stays 2,000 (inside its range 1,200–4,500) and is re-set from KC's measured G0 and KC5's registry cost before the model-phase approval (§10.2 'Re-setting'). The S6 adoption test is unaffected.

### 2.7 What transfers from C2 / C2ND, and what does not
| Item | C2 / C2ND | Track U | Transfers? |
|---|---|---|---|
| World | w0 (σ = 5/4); E4 process loaded by `c2_oracle.load_process` from E4 payloads (`c2_oracle.py:31-58`) [V] | w\* (σ = 7/4); process built in memory by the `hwsb_data.build_process` pattern and identity-checked against `hws-store/SELECTION.json` and the stage-C artifact `meta.json` values | **No:** `load_process` is never called |
| Models | E4 1729/2718/3141, via `c2_model.load_models` from main `artifacts` (`c2_model.py:35-48`; `c2_config.py:54, 99`) [V] | stage-C 620301–3 step 5000, from `hwsc-store/artifacts` by the TRAIN_RECORD ids | **No:** `load_models` is never called; new `hwsu_model.load_stage_c` |
| Site and position | circle at `resid_post_3`/32; attribution at `ln_final_out`/32 | the same | **Yes** (same architecture; gate BASIS) |
| Chart | C1′ production charts by sha256 | stage-C production charts by sha256 | the mechanism transfers; the objects are new |
| Code definition | FWL K = 3, 5 covariates, GLS, on C2 FIT (E4 activations) | the same recipe on fresh w\* FIT rows of the stage-C models | **Recipe yes; fitted projectors no** (they belong to other models) |
| Counterfactual | ±2-cell x-rotation donors; y-translation placebo; eligibility screen | natural suffix-matched pairs; no donors; no eligibility screen | **No** (new family) |
| Y1 placebo | y-translation donor | none: there is no natural y-only beyond-four pair | **No:** every share licence carries SPECIFICITY_NOT_ESTABLISHED (registered now); the decoy code KU3 and ψ_Γ are the substitutes |
| Decision rules | `c2_decide._category`, `r_model`, `stream_bounds`, `guard`, `beta_A`, `beta_E` (`c2_decide.py:38-145`) [V] | the same functions on U arrays, α = 1/300 | **Yes** |
| P1 | `c2_stats.p1`/`_summaries` (C2 seeds and ladder read from `c2_config` at call time, `c2_stats.py:305-330`) [V] | the `precision.sd_b4_draws`, `centered_draws` and `precision_summary` kernels (`tp/tools/x4_circle_history/precision.py:22-105`) [V], with U seeds and ladder | kernels yes; `p1` and `_summaries` no |
| Decoys | `nd_decoy.head_edit`, `make_head_decoy`, `decoy_sha64`, `dx` | KU2 by `head_edit("DNULL", …, g=1)`; KU1 is a new head of the same type | **Yes** (explicit g) |
| Thresholds | 0.30 (response gate), 0.10 / 0.50 (share), energy conjuncts, (127/60)× random energy | the same values, owner-approved for C2 (addendum 21) | **Yes, unchanged** (owner Q2) |

### 2.8 Splits, sizes, streams, seeds, scope (all new)
KEY = `"W12-q1-s1.75-p0.2"`, PROC = `("cylinder", "overlap", "1.75")`. Scopes: `hwsu-of-v1` (phase OF), `hwsu-v1` (model phase), `hwsu-dry-v1` (dry runs only). Store: `root/hwsu-store`.

| Split (scope) | Unit | Size | Use | Model logits read |
|---|---|---|---|---|
| of-fit (`hwsu-of-v1`) | singles | 8,192 (b0, b1) | oracle-ideal code fit (problem O) | — (no model) |
| of-eval (`hwsu-of-v1`) | pairs | 8,192 (b0, b1) | OF-1 … OF-5 | — |
| fit (`hwsu-v1`) | singles | 8,192 (b0, b1) | the code (R and its variants, S\*, decoy code, O); decoders; Sup | no |
| kfit | pairs | 4,096 (b0) | KU1/KU2 construction: code refit on both arms pooled (8,192 histories); K on pairs | no |
| feas | pairs | 4,096 (b0) | activation-only validity: Sup, L1 link (both arms as rows), R1-U | no |
| val | pairs | 4,096 (b0) | M0, X1 (ephemeral), H5-U, KO/KU known cases, P1 (SDs and oracle means only); sealed endpoint values | yes (sealed) |
| test | pairs | 4,096·k, k ∈ {1, 2, 4, 8} | T-PRE, then the single endpoint | yes |
| DRY (`hwsu-dry-v1`) | small | — | `scratch/hwsu-dry*/` only; masters never real | — |

- **Sequence ids:** `make_sequence_ids(process_code(*PROC, f"{scope}/{split}/b{block}/{arm}"), "test", n)`, with arm ∈ {s, a1, a2}. Rows are ordered by the sequence id of arm 1.
- **Seeds (PCG64; whole-token unused under `tp/tools`, `tp/src`, `tp/tests` on 2026-11-01 [V by search]; G0 repeats the search over the whole tree).**
  - **OF:** 640101 (headroom, rank 250), 640102 (ψ_orc and identity bounds), 640103 / 640104 (proxy P1 SD / centred), 640105 (Lemma P cross-check SE).
  - **Model phase:**
    - 640111: the TEST family stream U, 20,000 draws;
    - 640112: KO/KU at VAL;
    - 640113: H5-U at VAL;
    - 640114 / 640115: P1 SD / centred;
    - 640116: R1-U at FEAS;
    - 640117: descriptive intervals at TEST;
    - 640118: KO/KU report at TEST;
    - 640119: H5-U at TEST;
    - 640120: Haar frames.
  - **DRY:** 649901–649920.
  - No master is issued (no training).

**Registry-risk check.** All evaluation and OF rows are counted: 24,576 + 32,768 + 8,192·k histories (≤ 122,880 at k = 8). The run computes p_D2a(w\*) with `hws_exact.p_d2a` and requires agreement with HANDOFF `p_D2a` within 1e-12 relative (the HWSC rule, `hwsc_data.p_d2a_check` unchanged; the row sum by `hwsu_records.registry_risk_u`, because `hwsc_data.registry_risk` adds stage C's own rows, `hwsc_data.py:242-246`) [V], and then rows·p_D2a ≤ 1/100 in exact rationals. Desk value: 122,880 × 5.4163e-15 ≈ 6.7e-10 [W].

### 2.9 Statistics, error control and decision rules
**TEST family stream U** (seed 640111; `c2_decide.stream_bounds(arrays, seed, alpha, 20000)`, :38-46 [V]; one shared index stream over all models and arrays). Per model j, with all arrays over all N pairs:
- **Response:** ZR010 = A_full − 0.10·G; ZR030 = A_full − 0.30·G; AF = A_full.
- **Share:** Z010 = A_S − 0.10·A_full; Z050 = A_S − 0.50·A_full; Vabs = e_S − 0.10·e_full; Vrand = e_S − (127/60)·r; NEG = A_S.
- **Report-only variants:** v:Z010, v:Z050 for v ∈ {R_E, R_K1, R_K2}, outside the error count.

**α = 1/300 per one-sided bound** (ranks 67 and 19,934 of 20,000, `inverted_cdf`, run-time rank checks) [W, as C2ND §4.1].

**Per-model statements, declared only if their bound conditions hold** (a bound inside its NUM guard g_s counts as neither sign; `c2_decide.guard`, `beta_A`, `beta_E` with δ_P from GLS-REF, :49-72) [V]:

| Statement | Declared iff | Truth claimed |
|---|---|---|
| RESPONDS_j | L(ZR030) > 0 and L(ZR010) > 0 | θ > 0.30 |
| WEAK_RESPONSE_j | L(ZR010) > 0 and U(ZR030) < 0 | 0.10 < θ < 0.30 |
| LOW_RESPONSE_j | U(ZR010) < 0 and U(ZR030) < 0 | θ < 0.10 (signed; may be negative) |
| RESP_POSITIVE_BELOW_MARGIN_j (rule 6) | L(AF) > 0 and U(ZR030) < 0 | 0 < θ < 0.30 |
| *only if RESPONDS_j:* USED_j / PARTIAL_j / NOT_USED_j / LOW_ALIGNED_j | `c2_decide._category(b, "Z010", "Z050", ("Vabs", "Vrand"))` (:107-115) [V] | ψ > 0.5 / 0.1 < ψ < 0.5 / ψ < 0.1 and η_S < η₀ / ψ < 0.1 |
| *only if RESPONDS_j:* SHARE_POSITIVE_BELOW_MARGIN_j (rule 6) | L(NEG) > 0, U(Z010) < 0, U(Z050) < 0 | 0 < ψ < 0.10 |
| coarse: "θ > 0.10", "θ < 0.30"; "ψ > 0.10", "ψ < 0.50" | the single bound | as stated |

The response categories reuse `_category(b, "ZR010", "ZR030", ())`, with USED/PARTIAL/NOT_USED mapped to RESPONDS/WEAK_RESPONSE/LOW_RESPONSE. An empty energy tuple makes the third branch LOW_RESPONSE [V, `c2_decide.py:107-115`].

**Lemma FW-U (event count; the C2 Lemma FW argument, C2 §6.3) [W].** For every truth state, the event "some declared statement of model j is false" lies in a union of at most 5 coverage-failure events:
- **Response statements: ≤ 2.**
  - θ ≤ 0: F^L(ZR010) and F^L(AF).
  - 0 < θ ≤ 0.10: F^L(ZR010), plus F^U(ZR010) at θ = 0.10.
  - 0.10 < θ < 0.30: F^L(ZR030) and F^U(ZR010).
  - θ = 0.30: F^L(ZR030) and F^U(ZR030). LOW_RESPONSE needs U(ZR030) < 0, so it is contained in F^U(ZR030).
  - θ > 0.30: F^U(ZR030).
- **Share statements: ≤ 3.** These are declared only with RESPONDS_j. On the complement of RESPONDS_j's own failure events, θ > 0.30 and so E[A_full] > 0, and C2 Lemma D3 applies. C2's count is ≤ 2; the rule-6 statement adds F^L(NEG) in the region ψ ≤ 0.

So the bound is 3 × 5 × α = 15α = **0.05 at α = 1/300**, conditional on valid individual bounds. The implemented percentile-bootstrap rate is nominal (C2 §6.2). The qualifier NEGATIVE_ALIGNED_CONTRIBUTION(j) (U(NEG) < −g) and every variant or descriptive quantity are outside the count.

**Overall rules (2 of 3, C2 §6.5; owner Q3).**
- **Response:** RESPONDS if ≥ 2 RESPONDS_j; else WEAK_RESPONSE if ≥ 2 WEAK_RESPONSE_j; else LOW_RESPONSE if ≥ 2 LOW_RESPONSE_j; else MIXED if ≥ 2 models are resolved; else INCONCLUSIVE/PRECISION.
- **Share:** evaluated over the models with RESPONDS_j declared.
  - Fewer than 2 such models → **INCONCLUSIVE/NOT_RESPONSIVE**. The share is not assessed; the response outcome stands.
  - Otherwise: USED, PARTIAL, NOT_USED, LOW_ALIGNED_SHARE (≥ 2 in {NOT_USED, LOW_ALIGNED} with < 2 NOT_USED), else MIXED or INCONCLUSIVE/PRECISION.
- **Rule-6 statements** aggregate the same way ("in k models" iff ≥ 2 declare it). "In all three" is stated when all three declare.
- Every per-model status, every endpoint status (including NOT_RUN/<gate>) and every qualifier is reported. No model is selected after the fact.

**P1 precision ladder (VAL; outcome-blind; owner Q5).**
- **Ladder:** N ∈ {4,096, 8,192, 16,384, 32,768} pairs. The top value is twice C2's top, because the effect is small; see §4.4 [W].
- **Arrays:** per model, on the 4,096 VAL pairs, the SDs of ZR010, ZR030, Z010 and Z050, by `precision.sd_b4_draws` (seed 640114, the `r4n` argument is the oracle G array, so no model mean enters), `centered_draws` (seed 640115) and `precision_summary` (power 0.80, δ = 0) [V, `precision.py:22-105`].
- **Alternatives, from oracle means only:**
  - response arrays: 0.10·min_j mean_VAL(G);
  - share arrays: 0.03·min_j mean_VAL(G), which is 0.10 × the 0.30 response line × G. This is a lower bound on 0.10·E[A_full] whenever RESPONDS is true (the C2ND §4.5 pattern) [V].
- **N_RESP** is the smallest N at which every model passes the response arrays. Else it is the smallest N at which ≥ 2 pass (the others PRECISION_LIMITED(j)). Else **INCONCLUSIVE/UNDERPOWERED** before any TEST draw.
- **N_SHARE** is the same rule on the share arrays. If none passes, N_SHARE = 32,768 and the share family carries the qualifier SHARE_PRECISION_LIMITED: an unresolved share is then explicitly not evidence of non-use.
- **N = max(N_RESP, N_SHARE)**, k = N/4,096. No model mean of A_full or A_S at VAL enters P1. If the share family was dropped at OF (OF_PASS_RESPONSE_ONLY), N = N_RESP.

**A null is distinguished from a lack of power:**
- NOT_USED needs certified upper bounds on the signed share *and* on two energy conjuncts.
- LOW_RESPONSE needs a certified θ < 0.10.
- INC and INCONCLUSIVE/PRECISION are never read as non-use (licences, §7).
- P1 guarantees power against a stated blind alternative, or records that it could not.
- OF-4 shows beforehand that even the oracle-as-model can be powered within the ladder.

### 2.10 Sealing plan
| Object | Sealed by | Opened | Who may open |
|---|---|---|---|
| VAL means and every reconstructing statistic: A_full, A_S, A_Γ, e_S, r, the Z and V arrays, θ̂, ψ̂, variants, S\*, decoy-code share, KU1–KU3 values, the operator decomposition | `hwsu_records.write_sealed` (exclusive create, the `k4b_stats.write_sealed` pattern, `k4b_stats.py:185-204`) [V] into `hwsu-store/SEALED_VALIDATION.json` at P1; the validation report is checked by a `check_unsealed` mirror | after the TEST outcome is recorded, inside the ENDPOINT STAGE_COMPLETE (the stage-C D6 fix: `SEALED_OPENED.json` is written and hashed there) | ENDPOINT stage code; then the coordinator and the owner |
| KU1–KU3 at VAL | released as PASS/FAIL per case and model only (the C2ND `require_release` rule, `tp/tools/c2_nd/API.md:218`) [V] | REPORT | as above |
| VAL oracle quantities (G, ψ_orc, KO1–KO3), SDs, MDEs, support, chart and fit diagnostics | not sealed (they are not endpoints) | validation report | coordinator |
| OF report | not sealed (oracle-only) | OF stage | coordinator; the owner in plain language; later roles through the frozen plan only |

A computation-order policy (the C2 `LogitPolicy` pattern, `tp/tools/c2_readout/c2_driver.py:49-50`: the section comment is at line 49 and the class at line 50, by `grep -n` and a byte-level line count; S7) [V] makes the following refusals in code:
- no FIT, KFIT or FEAS logit, except the BASIS and M0 identity rows;
- X1 is ephemeral (identity diagnostics only);
- no TEST token before release B;
- no endpoint array before T-PRE passes.

---

## 3. Binding to stage C, and the exposure statement

### 3.1 Identity table (read and compared exactly by the run; G0U/H1-U)
| Item | Value (the writer's check) | Use |
|---|---|---|
| Stage-C FREEZE | `hwsc-store/FREEZE.json` sha256 **17c5b574…279800** (equal to `ah/jobs/0194/review.md`) [V] | binding: stage C was run under this freeze |
| Stage-C protocol | HWSC-DESIGN-v1 sha256 f0f2396c…a100a9 (RESULT.json `protocol_sha256`) [V] | binding |
| Stage-C completion | the `STAGES.jsonl` STAGE_COMPLETE record of stage S8 lists `RESULT.json` with sha256 f2b8a678…7048 [V] | presence and hash only. **RESULT.json is never opened by the run** |
| TRAIN records | `stages/TRAIN/{620301,620302,620303}/TRAIN_RECORD.json` sha256 3e60208a…5335, 023a332b…2d9, 9bf6417b…efd6 [V]. The run checks them against their STAGE_COMPLETE records | the loader reads only the keys `checkpoint_ids`, `checksums`, `run_key`, `status` (key whitelist; `dev_ce` is never read) |
| Checkpoints (step 5000) | a4cb0279bee92f52, 71b118ba2c5e12cc, 69c86a578ae8c1bc [V] | `meta.json` checks by the unchanged `hwsc_gates.expected_meta_c(j, 5000, record)` (`tp/tools/hwsc/hwsc_gates.py:52-58`) [V]: run key `("hwsc-v1", KEY, j)`, step, status, init seed, payload sha256. Then `c1_model.load_model64`, exact round trip; float32 `state_sha` recorded |
| Pilot exclusions | HANDOFF `stage_c_exclusions` (24 ids) | any of them → FAIL_TECHNICAL/IDENTITY (the HWSC rule) |
| Charts and gauges | PRODUCTION_FROZEN.json sha256 17da0ee8…ba36; chart file sha256 as in §2.4 [V] | file sha256 checked before loading; the gauges must equal the record exactly |
| Process | WorldSpec 21feee1d8ee5422e, TransitionSpec e4dafc7b9785c172; E_canon, T, π, coords sha256 equal to `hws-store/SELECTION.json` (243f7324…f087, HWSC §3.1 row 11) [H]; per-master EmissionSpec ids from `hwsc-store` `meta.json` | in-memory build and `hwsc_data.process_identity` (:37) [V]; E_canon bitwise identical across masters; per-model perm_j from its EmissionSpec |
| Stage-C store unchanged | `hwsc_records.lineage_c(hwsc-store)` PASS (:99) [V] at every U job | read-only; HWSU never writes `hwsc-store` |

**Preconditions found by the writer (G0U checks them; `hwsc-store` is never written).**
- (a) **`hwsc-store/REGISTRY_OBLIGATION.json` does not exist** [V]. HWSC §9.3 registered it, but no stage-C code writes it (`hwsc_registry_build.obligation` has no call site). Writing it now would hash ObservationSet payloads and HIST tables and write into a closed store, so **it is not written**. The coordinator records the gap in a mailbox note (stage-C record gap; no stage-C verdict affected). HWSU's U2 reader takes its expected inventory from records that already bind every file by sha256 (§8.3 U2).
  - (J1) The gap is recorded in the joint rulings `coord-hws-ud-20261101.joint-rulings.md` (sha256 641502e8…f9546f), item J1, and in the stage-C round. It is not an outcome defect.
- (b) `hwsc-store/RES-HWSC-W2` (`RESERVATION_W2.json`) is still `ACTIVE` with `end_utc` null [V]. The namespace reservation table (§8.2) records stage C's history-generation window as ended at its S8 STAGE_COMPLETE (2026-10-30T00:30:48Z, `STAGES.jsonl`), and G0 checks that statement. `hwsc-store` is not edited. `RUN.lock` (job 0196) and `OPERATION_ACTIVE.json` (idle) are lineage-exempt meter files (`k4b_release.py:27-30`) and are left as they are.
  - (J2) The statement is the mailbox record `ah/records/HWSC_W2_END.json` (sha256 2390e29d…c6cb). It binds the reservation file (28c74163…dbe5), `RUN.lock` (5d6b0e3d…a4f) and `OPERATION_ACTIVE.json` (ccfd90c3…e01e), with "ended with S8 STAGE_COMPLETE 2026-10-30T00:30:48Z", the S8 RESULT sha256 and the job-0196 review sha256 [V, record read].
  - The HWSU CONTRACT binds this record. G0U re-hashes it and checks that the three bound files still have the recorded sha256. A reservation named there counts as ended for HWSU's W2 attestation.

### 3.2 Exposure statement (stage-C data that were opened)
- **What was opened, and by whom:**
  - The stage-C calibration rows built the charts; their 512 lowest-id rows are the landmarks.
  - The validation rows gave the validation report.
  - The test rows gave the SUPPORT outcome.
  - The L1 learning-gate values were computed on the lgate rows.
  - Those values, and the stage-C outcome, are known to the coordinator and to this writer: the writer read `stages/S8/RESULT.json`, as permitted by the request.
- **What this does not affect:**
  - **Data.** Every HWSU history is fresh (new scopes) and registry-disjoint from all stage-C rows, training sets included (§8.3). So no HWSU endpoint statistic reuses an opened row.
  - **Objects.** The charts are frozen artifacts reused by sha256; nothing in them is tuned on HWSU data.
  - **Settings.** HWSU's thresholds are C2's owner-approved lines, the site and position are stage C's, and the code recipe is C2's. None was chosen from stage-C values.
  - **Different quantity.** No stage-C quantity measured the models' *prediction* response to beyond-four history. The L1 values bound overall predictive quality only, and were not read by this writer.
- **What it does affect, disclosed in every report:**
  - The prior expectation (§1.4) and the decision to plan track U were formed knowing stage C's SUPPORT.
  - The stage-C charts' validity is inherited from stage C's C0 gates, not re-established; SUP covers the new rows.
  - A stage-C chart that fits stage-C calibration rows unusually well cannot bias a covariance on fresh pairs, but it does define which phase the code tracks.

### 3.3 No tuning on stage-C data; changes from stage C, each justified
- **Unchanged:** the chart configuration, the charts themselves, the site `resid_post_3`, position 32, the models, the world.
- **Added:** the attribution site `ln_final_out`/32. It is not a change of stage C's site: it is C2's registered readout site, where the head is exactly linear (Lemma R). That exactness is what lets a share of the prediction response be attributed without evaluating synthetic states through a nonlinearity [W].
- **New:** the code is refitted on fresh FIT rows (C2's recipe). A code fitted on stage-C rows would reuse opened data.

---

## 4. Oracle feasibility (stage OF; addendum 25 rule 1)

### 4.1 Proposal (owner Q1)
OF runs as **its own metered stage, with its own owner approval, right after the design freeze and before the model part is implemented.** It needs only the phase-1 code: `hwsu_config`, `hwsu_pairs`, `hwsu_oracle`, `hwsu_of`, records, meter binding, their tests and an OF dry run. OF draws fresh oracle-only histories in scope `hwsu-of-v1` into `hwsu-store/stages/OF/`. It loads no model and opens no checkpoint, chart, activation or `sealed/` file.

**Failure scope (S3, registered now, before any OF value is seen).**
- **Study level.** A failure of OF-2, or of OF-4 on its response arrays, stops the round with INCONCLUSIVE/ORACLE_FEASIBILITY, and no model code is written. A failure of OF-B, OF-0, OF-H, OF-1 or OF-5 is technical or authority (their rows).
- **Share level.** A failure of OF-3 (the share ceiling), or of OF-4 on its share arrays only, **stops only the share part**. The share family is dropped: the share outcome is INCONCLUSIVE/ORACLE_FEASIBILITY, the share arrays are not formed, and KU1–KU3 and the share P1 arrays are not run. The response family may go to the owner for a model-phase approval, with the forecast re-stated.
- No response-only or other redesign may be proposed after OF values are seen. The response-only variant is this registered one, and Lemma FW-U's count for it is ≤ 2 events per model, which is conservative at the unchanged α = 1/300.
- OF-4's share-array clause is the writer's extension of S3 to the same question; it is flagged for the confirmation read.

OF rows are not checked against earlier stores' digests. No model reads them and every OF quantity is a fixed function of the history, so a repeat of an earlier history cannot bias it. They enter K-REG1 (U6), so no model-phase row repeats them, and `REGISTRY_OBLIGATION_OF.json` lets track D cover them.

Phase 1 has its own execution freeze, `FREEZE_OF.json`. It binds the phase-1 `H_exec`, the accepted J-OF test records, the accepted DRO report and the CONTRACT (`CONTRACT_OF.json`, F-2), and the plain-language OF forecast is given to the owner after it. Phase-2 code does not change any phase-1 file; it adds new files only. A change to a phase-1 file needs a versioned binding, a re-run of KC6 and a bitwise DRO re-run. Phase 1's documents are `CONTRACT_OF.json`, `API_OF.md` and `TEST_PLAN_OF.md`. Phase 2's `CONTRACT.json`, `API.md` and `TEST_PLAN.md` bind `CONTRACT_OF.json` by sha256 and add the phase-2 allowlist, tables and resources. The CONTRACT loader in `hwsu_config` (phase 1) loads `CONTRACT_OF.json` and, when present, `CONTRACT.json`. `CONTRACT.json` must carry `contract_of_sha256` equal to the sha256 of `CONTRACT_OF.json` (else FAIL_TECHNICAL/BINDING). The loader returns their union: phase-2 keys are added and never override a phase-1 key (an override → FAIL_TECHNICAL/BINDING). `hwsu_bind`, `hwsu_records` and `hwsu_meter_bind` read every setting through this loader, so phase 2 needs no phase-1 edit. OF runs with `CONTRACT.json` absent.

**Order (J6).**
- Whichever track the owner approves first draws first.
- OF is its own metered stage with its own freeze and its own owner approval, and it may come before both model phases.
- Its rows enter track D's registry through `hwsu-store/REGISTRY_OBLIGATION_OF.json`. At the end of OF, HWSU writes that obligation and then ends its own OF reservation with `hwsu_records.end_reservation`, which writes `hwsu-store/reservations/<reservation_id>.END.json` (J2, J3, J8; §8.2 item 3).
- **(J10)** `REGISTRY_OBLIGATION_OF.json` lists every array file then in `hwsu-store` (the OF history tables as K4b history tables; OF's oracle, fit, bootstrap and precision arrays as NON_HISTORY under the frozen name rule of `CONTRACT_OF.json`), with relpath and sha256 (§8.2 4(b)).
- If an OF attempt stops, it still writes `REGISTRY_OBLIGATION_OF-a<k>.json` before exit; this is the `<job>-a<k>` form of J10 item 2, with the job named OF.
- If it stopped before its first row, that no-history obligation ends `RES-HWSU-OF` and a rerun uses `RES-HWSU-OF-a<k+1>` (§8.2 item 3).

### 4.2 Gates of OF (computation, data, pass reading, tolerance, failure action)
| # | Gate | Computation | Data | Pass reading | Tolerance | On failure |
|---|---|---|---|---|---|---|
| OF-B | BINDING | `FREEZE_OF.json` present; the diff from R_ref to the phase-1 H_exec touches only the allowlisted phase-1 files; reused-file blob sha256 = the CONTRACT table; call-allowlist audit | git, files | all hold | exact | INVALID: do not run |
| OF-0 | G0-OF | authority: addenda 25, 26, 28, 37 and the owner's OF approval by sha256; the HWSU design-freeze file; namespace needles `hwsu-of-v1`, `hwsu-v1`, `hwsu-dry-v1`, `hwsu-store`, 640101–640120, 649901–649920, searched by `hwsu_seed.seed_search_u`. It is a line-for-line mirror of `hwsc_known.seed_search_c` (`hwsc_known.py:44-67`, whole-token rule) whose skip predicate is `hwsu_config.blinded` (§8.1), not `hwsc_config.blinded`, so track-D files, `hwsd-store` and the blinded stage-C files are never opened. Hits are classified by `hwsb_known.classify_hits` with the CONTRACT's `g0_declaration_fragments` and `g0_job_scratch`, frozen at the design freeze. The fragments follow HWSC's frozen list (`tools/hwsc/CONTRACT.json` `g0_declaration_fragments`) with HWSU's names: `/tools/hwsu/`, `/tests/hwsu/`, `/agent-handoff/` (this plan, its request, reviews and rulings, the namespace and W2 records, job, ledger and state files; track-D round files stay blinded and unsearched), `/hwsu-store/`, `/coord-scratch/`, `/docs/code_index/`, `/topo-scratch/hwsu-dry`, `/topo-scratch/test_hwsu-`. They also include the other track's declaration sites, which name HWSU's tokens as declared needles and as a READER_IF_PRESENT root (J3): `/tools/hwsd/`, `/tests/hwsd/`, `/topo-scratch/hwsd-dry`, `/topo-scratch/test_hwsd-`, and `/hwsd-store/` (only its obligation files are searched; its reports stay blinded). **(J9)** Under `/hwsd-store/`, only its `REGISTRY_OBLIGATION*.json` and `reservations/*.END.json` files and its reservation files are searched; everything else there is pruned unsearched as blinded. Disjointness from track D rests on the shared reservation table, not on reading track-D files. Any unclassified hit → FAIL_TECHNICAL/SEED_SCOPE.<br>**J3/J5 merge.** The classification runs through `hwsu_seed.classify_hits_u`, a mirror of `hwsc_known.classify_hits_c` (`hwsc_known.py:69-74`), which applies `hwsb_known.classify_hits` with the frozen fragments. Track D's reserved tokens (`hwsd-v1`, `hwsd-dry-v1`, `hwsd-store`, `hwsd-dry*`, `test_hwsd-*`, 620400–620499, 629950–629999, from `ah/records/HWS_UD_NAMESPACE.json`) are declared needles: G0-OF checks exactly, from the record, that no HWSU token equals or overlaps a track-D token (overlap → FAIL_TECHNICAL/SEED_SCOPE). Their hits are classified with the same fragment list; a hit anywhere else is unclassified → FAIL_TECHNICAL/SEED_SCOPE. Both records `HWS_UD_NAMESPACE.json` and `HWSC_W2_END.json` are bound by sha256; the reservation (§8.2) is the HWSU entry of `HWS_UD_NAMESPACE.json`; `hwsu-store` is absent or holds only this lineage's files | records, tree | all hold | exact | FAIL_TECHNICAL/SEED_SCOPE or INCONCLUSIVE/AUTHORITY |
| OF-P | PROCESS | in-memory w\* build; identity as §3.1; ‖πT − π‖∞ ≤ 1e-12; `validate_process(…, 1e-12)` | builders | all hold | 1e-12 | FAIL_TECHNICAL/IDENTITY |
| OF-S | SAMPLE | of-fit singles 8,192; of-eval pairs 8,192 (§2.1); history tables in the K4b format (canon32, seq_ids, digest), written as `stages/OF/HIST_OF_{fit,eval_a1,eval_a2}_b{0,1}.npz` | — | — | — | — |
| OF-H | HYGIENE | (i) `k4b_data.predicate_check(canon32, ("sealed_d2a",))` on every of-fit row and on both arms of every of-eval pair; (ii) `hwsc_data.p_d2a_check` against HANDOFF `p_D2a` (≤ 1e-12 relative) and 24,576·p_D2a ≤ 1/100 in exact rationals (`hwsu_records.registry_risk_u`); (iii) duplicate digests within OF reported | of-fit, of-eval | (i), (ii) hold | exact | (i) → INCONCLUSIVE/REGISTRY_INCOMPLETE, no OF value computed; (ii) → FAIL_TECHNICAL/SAMPLER |
| OF-1 | IDENTITIES and SAMPLER | (i) suffix of arm 2 = suffix of arm 1, bitwise, on every pair; (ii) q4 and m4 bitwise equal across arms; (iii) finite log-evidence on every arm; (iv) KO1: per pair, \|A°_full − G\| ≤ 1e-12·max(1, \|G\|) with z = log q̄32 (Lemma D2); KO2: \|A\| ≤ 1e-12 with z = log q̄4; KO3: \|A − G/5\| ≤ 1e-12·max(1, \|G\|) with λ = 1/5; (v) Decimal references on the 4 lowest-id pairs: q32 of both arms and q4 by `c1_oracle.decimal_reference` / `decimal_posterior60` with `h3_compare` and `decimal_G` (`c1_oracle.py:215-274`) [V] | of-eval | all hold | as stated; Decimal ≤ 1e-10 relative | FAIL_TECHNICAL/ORACLE or /SAMPLER |
| OF-2 | HEADROOM (response) | lower bound (rank 250 of 5,000, seed 640101) of mean G over the of-eval pairs | of-eval | **> 0.02 nat** (2 × C2's H5 floor of 0.01 nat) | exact comparison | INCONCLUSIVE/ORACLE_FEASIBILITY |
| OF-3 | CODE-SHARE CEILING | problem O fitted on of-fit (FWL design rank 47; LW ratio; whitened rank 11, cond ≤ 1e8; G1 identities; GLS-REF ρ_ref ≤ 1e-20; C2 F1 rules, `c2_stats.f1_problem`, :370) [V]; on of-eval, Z°020 = A°_S − 0.20·G; lower bound (rank 84 of 5,000, seed 640102) | of-fit, of-eval | **L(Z°020) > 0**, i.e. ψ_orc > 0.20 = 2 × the 0.10 share line | guard g_s | share family dropped: share outcome INCONCLUSIVE/ORACLE_FEASIBILITY (S3, §4.1); a degenerate fit → FAIL_TECHNICAL/NUMERICAL |
| OF-4 | PRECISION PROXY | the oracle-as-model arrays (z = log q̄32 with problem O): Z°010 = A°_S − 0.10·G and Z°050; ZR°030 = (1 − 0.30)·G. Run the P1 rule of §2.9 (seeds 640103/640104), with the share alternative 0.03·mean(G) and the response alternative 0.10·mean(G) | of-eval | some ladder N ≤ 32,768 passes every proxy array | rule exact | response arrays: INCONCLUSIVE/ORACLE_FEASIBILITY (study); share arrays only: share family dropped (S3, §4.1) |
| OF-5 | LEMMA P CROSS-CHECK | the pair estimate ½(Δu°)·(Δm32) against the single-row estimate u°·r4 on the arm-1 rows (u° the oracle unit phase); also ½dᵀΔlog q̄ (= mean G) against the single-row E[ρ4ᵀ log q̄32] | of-eval | \|difference\| ≤ 5·SE_diff (SE by 5,000 joint draws, seed 640105) for both | 5 SE | FAIL_TECHNICAL/SAMPLER (coordinator review; no tolerance change) |

**OF report** (`stages/OF/OF_REPORT.json`, hashed in STAGE_COMPLETE) contains:
- E[G] with its bound;
- ψ_orc with its bound (point estimate and two-sided 95 % interval), and against 0.50 (descriptive, §4.3);
- the K = 1 and Euclidean variants of ψ_orc;
- the oracle's circular-label share (the pair version of G4^A/G4);
- the proxy MDEs per N, and next to them the share of ΣG carried by the top 1 % of pairs and the per-pair kurtosis of G (S4; report only; percentile bounds at α = 1/300 are only nominal under heavy tails);
- the measured CPU.

**Pass:** OF-B, OF-0, OF-H and OF-1 … OF-5 all PASS → OF_PASS. If only OF-3, or only OF-4's share arrays, fail → OF_PASS_RESPONSE_ONLY (S3, §4.1). The coordinator ACCEPTs and tells the owner in plain language. Only then does phase 2 (model-part implementation) start. OF's measured SDs and CPU may re-set the CPU centrals of §10 (cost only, addendum 26 item 2). They never change a threshold, margin or ladder value.

### 4.3 The margin-to-oracle ratios required, and what is not required
- **Response:**
  - Oracle θ = 1 against the 0.30 line: ratio 3.3, exact by Lemma D2 (OF-1 KO1).
  - Oracle response in nats against C2's H5 floor: OF-2 requires a lower bound ≥ 2×.
  - Desk: E[G] ≥ G4 ≥ 0.031 nats [W from H, Lemma J]. Second order: ≈ 0.062, about 3× the 0.02 requirement [W].
- **Share:** ψ_orc ≥ 2 × 0.10 (OF-3).
  - Desk guess: ψ_orc ≈ the circular-label fraction ≈ 0.5–0.6 [W from H: G4^A/G4 ≈ 0.59]. Some circular information (concentration) goes to the nuisance block Γ, which lowers it. So the expected ratio to 0.10 is ≈ 4–6 [W].
- **Not required, and stated now: ψ_orc against the 0.50 line.** A rule-1 ratio of 2 against 0.50 would need ψ_orc ≥ 1, which is impossible. The USED/PARTIAL boundary is therefore **not oracle-feasible at 2×**, and this is registered.
  - USED stays a category: a model whose beyond-four response is more circle-concentrated than the oracle's (for example, one that learned the circular part but not the axial part) can have ψ > ψ_orc.
  - A PARTIAL outcome with ψ near ψ_orc reads "as circle-concentrated as an ideal predictor". It is not a weak result. ψ_orc is printed beside every share outcome as the comparator (§7.2).
  - **No threshold moves after OF** (owner Q2).

### 4.4 OF scope and cost
- **Rows:** 8,192 singles + 8,192 pairs = 24,576 histories.
- **Work:** oracle filtering; the q4 filter; problem O (a 47-column FWL; 35-d GLS-REF at 80 digits); 5,000-draw bootstraps.
- **G0:** the needle search over the tree, ≈ 490 CPU-s [W from H: the J-C1 with seed pre-check took 1,048.2 s against 560.3 s without it, `ah/jobs/0190`, `0194`].
- **Central:** ≈ 700 CPU-s, range 400–1,500 [W].
- **Phase OF in all:** J-OF tests (2 runs × 450) + OF dry run (2 × 100) + OF ≈ 1,800 CPU-s; 3× line 5,400 (§10).

---

## 5. Known-case checks (addendum 25 rule 5)

### 5.1 Synthetic known cases (tests and the dry run; synthetic data only)
- **KS-PAIR (sampler, exact).** On a tiny HMM with a **non-reversible** chain (T ≠ T̃, so a transposition defect cannot hide, as with C2's non-involutive permutation), with L = 8 and a 4-symbol suffix:
  - the sampler's implied distribution of the prefix, given each suffix (the product of its own kernels, in Fractions), equals the brute-force Bayes conditional exactly;
  - 10⁵ draws match within 4 SE per cell;
  - arm 2's marginal equals the process law exactly.
  - A planted "use T instead of T̃" or "drop the β message" sampler fails.
- **KS-P (Lemmas P1–P3, J) by exact enumeration on the tiny world:** pair moments equal the conditional-covariance forms; E[G] = Jeffreys(q32, q4); a suffix-only predictor gives A ≡ 0.
- **KS-USE / KS-IGNORE / KS-DECOY on a tiny `TransformerLM`-shaped readout with planted structure:**
  - a readout reading only a planted beyond-four code → USED;
  - a readout reading only suffix-determined directions while the code carries beyond-four variation → LOW_RESPONSE (A ≡ 0);
  - the D-NULL head edit → NOT_USED;
  - a decoy code from a hash phase → NOT_USED or LOW_ALIGNED; a planted decoy whose fitted plane overlaps the planted reader → DECOY_PARTIAL;
  - a dose head (ρ = 0.92, the C2ND construction) → PARTIAL;
  - the C2ND T-COPY lesson: a copied code is absorbed into col(B̂) → USED.
- **KS-RULES:** the decision table of §2.9 and its rule-6 statements at every boundary (a mean exactly at a threshold is never declared; a bound inside the guard is neither sign); the Lemma FW-U event grid (exhaustive over truth regions, the C2ND T-FAMILY-ND pattern); the 2-of-3 aggregation; INCONCLUSIVE/NOT_RESPONSIVE.
- **KS-P1:** the ladder and max() rule with N_RESP and N_SHARE in every combination; SHARE_PRECISION_LIMITED; P1 reads no model mean (a seed-sensitive fixture, and a fixture where changing mean(A_full) changes nothing).

### 5.2 Oracle known cases on real-scope rows (OF-1; repeated at VAL and on TEST; exact)
- **KO1:** the oracle itself → θ = 1 exactly, RESPONDS.
- **KO2:** the suffix-only predictive → A ≡ 0, LOW_RESPONSE ("carries nothing beyond four").
- **KO3:** the dose λ = 1/5 → θ = 1/5 exactly → WEAK_RESPONSE and RESP_POSITIVE_BELOW_MARGIN. Both are deterministic, since G ≥ 0 on every row.

**Pass:** per-row identities and the declared categories as stated. **Failure:** FAIL_TECHNICAL/KNOWN_CASE (study).

### 5.3 Model known cases on real activations (gate KC-U at VAL; decision-bearing for the share family)
The constructions use the **KFIT** projector P_S^K. The method under test is the registered **FIT** projector P̂_S, so the known answers hold by margin under refit, not by tautology (C2ND §2.8, MD-5) [V].
| Case | "The request's" role | Known answer | PASS | CONTRADICTED | UNRESOLVED |
|---|---|---|---|---|---|
| KU1 D-USE (planted reader of the code's beyond-four component, §2.6) | uses the beyond-four code | ψ′ = 1 under construction; USED | USED declared | NOT_USED, LOW_ALIGNED or PARTIAL | its prerequisite L(A′_full) > 0 fails, or INC |
| KU2 D-NULL, g = 1 (the code bitwise in the activations, read exactly zero; C2ND Lemma DC2) | carries it but ignores it | ψ′ = 0; NOT_USED or LOW_ALIGNED | NOT_USED or LOW_ALIGNED | USED or PARTIAL | L(A′_full) > 0 fails (the model reads beyond-four almost only through the code), or INC |
| KU3 decoy code (SHA-of-suffix phase, same recipe, base readout) | a decoy | not USED (expected ψ ≈ 6/127 = 0.047 [W, C2 Lemma RS1, approximate for a fitted plane]) | NOT_USED or LOW_ALIGNED (U(Z010_dec) < −g) | USED | otherwise (incl. L(A_full) > 0 failing or INC) |
| KO1–KO3 | the oracle itself | §5.2 | §5.2 | — | — |

**KU3 at PARTIAL.** If the decoy code declares PARTIAL at VAL, the result is not a contradiction. It is the qualifier **DECOY_PARTIAL(j)**. Every share statement for j that is not NOT_USED or LOW_ALIGNED then carries: 'a hash-of-suffix decoy plane fitted by the same recipe also carried more than 10 % of the response on the validation pairs; this share is not distinguished from a fitted decoy plane'. The decoy's TEST share ψ̂_dec (seed 640118) and the 5th/50th/95th percentiles and the maximum of the 32 Haar-frame shares are printed beside every USED or PARTIAL licence for j.

(Merge: a KU3 PARTIAL takes DECOY_PARTIAL(j), not DECOY_UNRESOLVED(j). Other KU3 results in the UNRESOLVED column take DECOY_UNRESOLVED(j), as below.)

- **Prerequisite.** Each case needs its own positivity prerequisite, L(E[A′_full]) > 0 (VAL bounds, 5,000 draws, α = 1/60, seed 640112), in place of the 0.30 response line. The share decisions of a head-edit family do not depend on the gain (C2ND Lemma DG) [V]. So the 0.30 line carries no information about the method for a constructed case, while a positive denominator is required by Lemma D3 [W]. The gain is therefore fixed at 1, and no gain is chosen from data.
- **Release:** PASS/FAIL per case and model only (§2.10). The KU MDEs at VAL (SD-based, outcome-blind: ψ-share arrays of each case at the P1 alternative) are reported next to the release (S8, report only). If ψ is high, KU2's residual response (1 − ψ)·A_full is small and DECOY_UNRESOLVED is likely; Lemma DG means a gain would not help.
- **Consequences, per model j:**
  - A KU2 or KU3 contradiction → **KNOWN_CASE_CONTRADICTED(j, case)**: the method manufactures a share on this model. The share endpoint of j is NOT_RUN/KNOWN_CASE; the coordinator reports to the owner before ACCEPT (the C2ND S13 pattern).
  - A KU1 contradiction or unresolved → **EXCLUDED_j/KNOWN_CASE** for the share family: without a working positive control, NOT_USED is not trustworthy.
  - KU2 or KU3 unresolved → the qualifier **DECOY_UNRESOLVED(j)** on every share licence for j.
  - The response family is unaffected by KU1–KU3. It depends only on KO1–KO3.

### 5.4 Coverage
Each control meets a case with a known answer:
- every response category and the response rule-6 statement (KO1–KO3);
- USED (KU1), NOT_USED/LOW_ALIGNED (KU2), and "not USED" for a fitted decoy plane (KU3);
- PARTIAL, the share rule-6 statement and the energy conjuncts: synthetic only (§5.1);
- X1, BASIS, M0, GLS-REF and the sampler: known identities.

---

## 6. Gates, frozen before any draw (model phase; the OF gates are in §4.2)

**Convention.** Exact Fractions; strict inequalities as written; the first non-PASS **study-scope** gate ends the study and later gates are NOT_RUN. A **model-scope** gate excludes that model from the named family, and the family continues while ≥ 2 models remain (C2 §7). One metered stage per job. Every gate value computed is reported. VAL bounds are 5,000 draws at α = 1/60 (ranks 84 / 4,917), except the headroom bounds H5-U and OF-2 at level 0.05 (rank 250), as C2's H5.

| # | Job | Gate | Computation | Data | Pass reading | Tolerance | On failure (scope) |
|---|---|---|---|---|---|---|---|
| S0 | dispatch | BINDING | protocol sha256 = freeze record; R_ref → H_exec diff touches only the allowlisted `tools/hwsu/*`, `tests/hwsu/*`, `docs/code_index/*`; every reused file's blob sha256 = the CONTRACT `reuse_sha256` table; the call allowlist audit (§11.2) | git, files | all hold | exact | INVALID: do not run |
| PF | J-U1 | PREFLIGHT | unchanged suites `tests/{c2_readout, c2_nd, hwsc, hwsb, k4b, c1prime, oracle, oracle_profile, circle_history, dataset, world, process, learner, contracts}` + `tests/hwsu`; `check_file_sizes` (≤ 400 lines); the call-allowlist audit; tempdir and basetemps under `scratch/test_hwsu-<job>/` | code | all pass | — | INVALID |
| KC | KC | KC0–KC6 | KC0 = G0U authority and namespace (OF-0 rules (the same `seed_search_u` and fragment list) plus OF_ACCEPT, with OF_PASS or OF_PASS_RESPONSE_ONLY, and the model-phase run approval); KC1 = process identity (OF-P); KC2 = checkpoint `meta.json` identity without loading (§3.1); KC3 = the synthetic known cases KS-PAIR, KS-P, KS-RULES re-run in the job; KC4 = the call-allowlist audit; KC5 = **registry rehearsal** of R-sources against the real root into `hwsu-store/registry/rehearsal/` (CPU, peak memory and store size recorded); KC6 = OF reproduction: the OF report's E[G] point recomputed bitwise from the stored OF tables | records, synthetic | all PASS | exact | FAIL_TECHNICAL/KNOWN_CASE (study) |
| 0 | E1 | G0U | KC0 repeated; release A present (W3 attestation, K-REG1 reservation, seed-hit classification). The attestation applies the J8 rule (§8.2 item 3): a reservation counts as ended iff it is `RES-HWSC-W2` with `HWSC_W2_END.json` bound and matching (J2), or a `<store>/reservations/<reservation_id>.END.json` record of schema "hws-reservation-end-v1" matches the current reservation and obligation sha256. This covers the OF reservation and any track-D reservation. Any other ACTIVE reservation → INCONCLUSIVE/AUTHORITY (serial generation, J3) | records | all hold | exact | INCONCLUSIVE/AUTHORITY; FAIL_TECHNICAL on hash or seed defects |
| 1 | E1 | H1-U | §3.1 table: FREEZE, TRAIN records, checkpoint meta and load round trip, `state_sha`, pilot exclusions, chart and gauge identity, process identity, `lineage_c(hwsc-store)`, one torch thread | checkpoints, charts | all hold | exact | FAIL_TECHNICAL/IDENTITY (study) |
| 2 | E1 | REG1 | K-REG1 built (§8.3), every directory classified; coordinator completeness certificate in release A | §8.3 | complete | exact | INCONCLUSIVE/REGISTRY_INCOMPLETE (study) |
| — | E1 | sampling S3 | reservation verified; fit, kfit, feas, val drawn (§2.8) | — | — | — | breach before the first row: cancel release A; after: lineage review |
| 3 | E1 | H2-U | every digest of every arm ∉ K-REG1 (`Registry.contains`, the `c2_registry.separation` pattern) [V]; the splits pairwise disjoint; sequence ids disjoint from the frozen union; sealed-D-2a predicate false on every arm (`k4b_data.predicate_check`, :186) [V]; registry risk (§2.8) | all U rows | 0 collisions, 0 hits | exact | FAIL_TECHNICAL/LINEAGE; predicate → INCONCLUSIVE/REGISTRY_INCOMPLETE |
| 4 | E1 | H3-U | OF-1 (i)–(v) on fit, kfit, feas and val (Decimal: 4 lowest-id rows or pairs per split); Σq = 1 within C2's `T_QSUM` | all U rows | all hold | as OF-1 | FAIL_TECHNICAL/ORACLE or /SAMPLER (study) |
| 5 | E1 | H5-U | VAL lower bound (rank 250, seed 640113) of mean G > 0.01 nat, and the OF-2 re-check > 0.02 nat | val | both | exact | INCONCLUSIVE/HEADROOM (study) |
| 6 | E1 | BASIS | per model: rank(diag(γ)N₁) = 127 (`readout_basis` `rank_ok`) [V]; κ_X1 attainability on 1,024 lowest-id FIT rows (`c2_model.kappa_x1`, `x1_attainable`, :180-190) [V] | weights, fit | PASS | C2 T9 | FAIL_TECHNICAL/MODEL (study) |
| 7 | E1 | SUP | per model, `k4b_charts.extend` support fraction ≥ 0.99 on fit, kfit and feas arms; support on val computed and reported (it is support_VAL for T-PRE, S7) | fit, kfit, feas, val | ≥ 0.99 | exact | EXCLUDED_j/CHART_UNAVAILABLE (model) |
| 8 | E1 | F1 | problems R (primary), R_E, R_K1, R_K2, S\*, SHA (decoy code), O (oracle comparator) on fit; problem K (construction) on kfit; C2 F1 rules (design rank 47; LW eigen-ratio; whitened rank 11, cond ≤ 1e8; G1 identities 1e-10; GLS-REF ρ_ref ≤ 1e-20 and the projector gate) [V, C2 §2.5] | fit, kfit | PASS | C2 | R or K: EXCLUDED_j/PATCH_MODEL_DEGENERATE or /NUMERICAL (model); variants: NOT_COMPUTED; O: FAIL_TECHNICAL/NUMERICAL (study) |
| 9 | E1 | L1 | C2 link decoders on feas (both arms as rows): R²_code\|0 ≥ 0.50 and ρ_inc ≥ 0.90 (`c2_stats.fit_decoder`, `l1`, :234, :275) [V] | fit → feas | PASS | C2 | EXCLUDED_j/LINK (share) |
| 10 | E1 | R1-U | beyond-four registration of the code: the lower bound (α = 1/60, seed 640116) of mean ½(Δû_c)·(Δm32) over feas pairs, with û_c the unit vector of the code's first-harmonic pair (`c2_code.code_phase`, :176) [V]; C2's sign-agreement R1 on the larger half of \|Δ arg m32\| reported, not gated | feas | L > 0 | guard | CNHS-U_j: the code does not register beyond-four change (share NOT_RUN for j; model) |
| 11 | E1 | M0 | `hwsu_model.m0_u` on the 1,024 lowest-id VAL pairs: the `c2_model.m0` sequence (`c2_model.py:228-257`) with its identity step replaced by H1-U's stage-C identity (checkpoint id, `meta.json`, float32 `state_sha`). It calls unchanged `identity_patch`, `readout_identity`, `two_route`, `kappa_x1`, `x1_attainable` and `symbol_order_b/c`. `c2_model.m0` itself is never called, because it reads `PROTOCOL_IDS` and `CONTRACT["models"]` (`:27-31, :233-234`) | val | PASS | C2 T9, T10, T18 | FAIL_TECHNICAL/MODEL (study) |
| 12 | E1 | X1 | closed form against the network: natural arms on every VAL pair; interchange arms y_S^{2←1}, y_S^{1←2} on the 4,096 lowest-id pairs per split; KU heads on the 1,024 lowest-id pairs; ephemeral | val | ‖z − ẑ‖∞ ≤ 1e-9·max(1, ‖z‖∞) | as stated | natural arms: FAIL_TECHNICAL/X1 (study); interchange arms y_S^{2←1}, y_S^{1←2}: FAIL_TECHNICAL/X1 for the share family; KU heads: FAIL_TECHNICAL/DECOY for the share family |
| 13 | E1 | DX | construction exactness: KU2 \|A′_S\| ≤ 1e-9·max(1, \|A′_full\|) under P_S^K; KU1 \|A′_full − A′_S\| ≤ 1e-9 under P_S^K; head identity and `decoy_sha64` (`nd_decoy.dx`, `decoy_sha64`, :341, :167) [V] | val | all rows | as stated | FAIL_TECHNICAL/DECOY (share family) |
| 14 | E1 | KC-U | §5.2–§5.3 at VAL bounds | val | §5.3 | — | §5.3 |
| 15 | E1 | P1 | §2.9; `SEALED_VALIDATION.json` written and hashed | val | N_RESP exists | ranks checked | INCONCLUSIVE/UNDERPOWERED (before any TEST draw) |
| 16 | release | ACCEPT, REG2, release B | coordinator ACCEPT of the validation report (no endpoint-reconstructing value); K-REG2 rebuilt from scratch with the U rows (its own job, booked to E2, as stage C after D-0192-1); release B binds N, k, the K-REG2 sha256, the reservation and the worker session | — | all present | exact | no release, no fresh data |
| — | E2 | sampling S7 | test b0…b(k−1) pairs under release B | — | — | — | — |
| 17 | E2 | H2-FRESH-U | test digests ∉ K-REG2; ids disjoint; predicate false | test | 0 | exact | as row 3 |
| 18 | E2 | T-PRE | H1-U re-check; H3-U and H5-U on test (seed 640119); SUP ≥ 0.99; L1 and R1-U with the frozen decoders and code; M0 and X1 on the lowest-id test pairs (ephemeral); \|support − support_VAL\| reported | test | all hold | as above | study gates: INCONCLUSIVE/TEST_GATE (endpoints NOT_RUN/T-PRE); model gates: EXCLUDED_j/TEST_GATE |
| 19 | E2 | NUM | every decision bound clears its guard g_s | test | — | §2.9 | INC_j/NUMERICAL |
| 20 | E2 | ENDPOINT | family stream U (§2.9), per-model statuses, overall outcomes, rule-6 statements, qualifiers; KO/KU report on test (seed 640118); descriptives (§2.6; seed 640117); `SEALED_OPENED.json` hashed inside STAGE_COMPLETE | test | — | ranks checked | rank-check failure → FAIL_TECHNICAL/NUMERICAL |

**Obligations of model-phase jobs (J10).**
- Every job of this table that writes into `hwsu-store` (KC, E1, REG2, E2) ends by writing its obligation (§8.2 4(b)), including a stopped attempt: `REGISTRY_OBLIGATION_<job>-a<k>.json`, or `REGISTRY_OBLIGATION.json` for the E2 job that completes the study.
- A drawing job (E1 at sampling S3; E2 at sampling S7) that stops after its reservation starts and before its first row writes a no-history obligation, ends `RES-HWSU-U` with it, and a rerun takes `RES-HWSU-U-a<k+1>` (§8.2 item 3).
- The job's STAGE_COMPLETE (or stop record) lists the obligation's sha256.

**Under OF_PASS_RESPONSE_ONLY** the share-family gates are NOT_RUN/SHARE_DROPPED and cannot end the study: SUP, F1 (all problems), L1, R1-U, the interchange-arm and KU-head parts of X1, DX and the KU part of KC-U. BASIS, M0, natural-arm X1, H1–H5, KO1–KO3 and the response part of P1 run unchanged.

**Stop rules and corrections.** These follow the K4B §11.8 technical-correction rule unchanged:
- at most two correction jobs per documented defect;
- PASS stages immutable;
- superseded attempts archived with SHA256SUMS;
- bit-identical regeneration;
- an owner decision if a correction would change an already-computed outcome-bearing quantity: OF values, fits, KU results, SDs, N, endpoint means.

No threshold, tolerance, seed, rank, ladder value, chart, site or construction constant changes after any HWSU data exist.

---

## 7. Outcomes and licences (registered now)

### 7.1 Outcomes, in order of precedence
| # | Outcome | Condition |
|---|---|---|
| 1 | **FAIL_TECHNICAL/<class>** | IDENTITY, LINEAGE, ORACLE, SAMPLER, MODEL, NUMERICAL, X1, DECOY, BINDING, SEALING, BLINDNESS, KNOWN_CASE, SEED_SCOPE, not resolved under §6's correction rule. S0/PF failures are "do not run", not outcomes |
| 2 | **INCONCLUSIVE/RESOURCE_OR_AUTHORITY** | a 3× pause the owner does not continue; lost process; disk or memory safe-STOP; missing authority; window precondition not met |
| 3 | **INCONCLUSIVE/ORACLE_FEASIBILITY** | study level: OF-2, or OF-4 on its response arrays, failed (phase OF; no model part is built). Share level: OF-3, or OF-4 on its share arrays only, failed. Then only the share outcome is INCONCLUSIVE/ORACLE_FEASIBILITY and the response family may proceed after an owner approval (S3, §4.1) |
| 4 | **INCONCLUSIVE/<study gate>** | REGISTRY_INCOMPLETE, HEADROOM, UNDERPOWERED, TEST_GATE; or fewer than 2 models left after per-model gates |
| 5 | **Response outcome** | RESPONDS / WEAK_RESPONSE / LOW_RESPONSE / MIXED / INCONCLUSIVE/PRECISION (§2.9) |
| 6 | **Share outcome** | USED / PARTIAL / NOT_USED / LOW_ALIGNED_SHARE / MIXED / INCONCLUSIVE/PRECISION / INCONCLUSIVE/NOT_RESPONSIVE (fewer than 2 RESPONDS_j) / INCONCLUSIVE/<per-model gate> (CHART_UNAVAILABLE, LINK, CNHS-U, KNOWN_CASE) |

**Qualifiers (never change an outcome):**
- SPECIFICITY_NOT_ESTABLISHED (on every share licence; registered);
- DECOY_UNRESOLVED(j);
- KNOWN_CASE_CONTRADICTED(j, case);
- NEGATIVE_ALIGNED_CONTRIBUTION(j);
- PROJECTOR_DEPENDENT(j), HARMONIC_DEPENDENT(j, K);
- PRECISION_LIMITED(j), SHARE_PRECISION_LIMITED;
- DECOY_PARTIAL(j) (§5.3);
- DISSENT(j: status).

**Rule-6 statements (addendum 25 rule 6):** RESP_POSITIVE_BELOW_MARGIN and SHARE_POSITIVE_BELOW_MARGIN, per model and in k models.

**What happens if a model fails a gate.** The model is reported with its EXCLUDED_j/<gate> status, and its endpoints in that family are NOT_RUN/<gate>; the family continues with ≥ 2 models. There is no replacement model, no world change, no recipe change, no new chart, no other code recipe and no larger gain without a new owner decision. A rerun with other choices would be a new versioned protocol with its own review and registry. The coordinator reports in plain language and asks the owner (default: stop).

### 7.2 Licences (filled at run time; nominal percentile-bootstrap statements, conditional on the three stage-C models, their frozen charts and the FIT fits)
**Scope clause carried by every licence (Q-CODE-U).** *"Pairs are natural histories of world w\* that share their last four symbols; each arm is a draw from the process. Any predictor or code that depends only on the last four symbols has zero effect on these pairs, so every effect stated here depends on the history before the last four symbols. The share outcomes concern the frozen, nuisance-excluding linear code defined by the FIT fit and projector of the stage-C chart phase. They do not exclude predictive use of beyond-four information in excluded directions, higher harmonics, interactions or other encodings."*

- **RESPONDS.** "In k of the 3 stage-C models (masters …), when only the history before the last four symbols changes, the next-symbol prediction at position 32 moves in the direction of the oracle's change by more than 0.30 of the oracle's own discrimination: θ̂ = …, one-sided (1 − 1/300) lower bounds …. A predictor reading only the last four symbols would show θ = 0 on these pairs. The prediction therefore depends on earlier history, aligned with the belief." [+ Q-CODE-U]
- **WEAK_RESPONSE / RESP_POSITIVE_BELOW_MARGIN.** "… the prediction moves in the oracle's direction (lower bound above 0) but by less than 0.30 of the oracle's discrimination [WEAK: and by more than 0.10]. This is a positive finding below the response margin; it is neither RESPONDS nor evidence of a negligible response."
- **LOW_RESPONSE.** "… the signed oracle-aligned response is certified below 0.10 of the oracle's (it may be negative). The circle carries beyond-four information (stage C), but these predictions move little with it in the oracle's direction." Not licensed: that the prediction is a function of the last four symbols only (orthogonal or cancelling movement is not excluded).
- **USED.** "In k models that respond, setting the six circle-code coordinates of the final LayerNorm output to their values under the other history of the pair, with every other GLS coordinate held, carries more than half of the model's signed oracle-aligned response: ψ̂ = …, bounds …. On these pairs this moves exactly the part of the code that the last four symbols do not determine (magnitude and phase changes alike; §7.3 item 11). The oracle-ideal share on the same pairs is ψ_orc = …." [+ Q-CODE-U; + SPECIFICITY_NOT_ESTABLISHED: the share is not shown to exclude y-belief information carried in the code beyond the five nuisance covariates.]
- **PARTIAL.** "… carries more than 10 % and less than 50 % … (ψ̂ …; oracle-ideal ψ_orc …)". If ψ̂'s interval contains ψ_orc, the report adds: "about as circle-concentrated as an ideal predictor's". [If DECOY_PARTIAL(j):] the registered qualifier sentence (§5.3).
- **NOT_USED.** "… the circle-code interchange has a signed share below 0.10 of the model's beyond-four response (possibly opposing), and its total centred-logit effect is below 10 % of the response's mean-square energy and below 127/60 times that of a random 6-dimensional subspace. The position-32 readout does not use this registered code's beyond-four component beyond this bound." It is never called "computationally inert" without the bound, the site and Q-CODE-U.
- **LOW_ALIGNED_SHARE.** "… signed share below 0.10, but the energy was not shown to be small. This is not a NOT_USED result."
- **SHARE_POSITIVE_BELOW_MARGIN.** "… the code's share is certified positive and below 0.10."
- **MIXED / INCONCLUSIVE.** Only the per-model results, and the statement "not evidence for or against use". INCONCLUSIVE/NOT_RESPONSIVE: "the share was not assessed because fewer than two models were certified to respond".

**Disclosure carried by every report.** "Track U follows stage C (SUPPORT in 3/3: the chart phase carries beyond-four information) and C2/C2ND (circle code used at the readout in the E4 models of world w0). Track U's histories, code fits and decisions are its own. Its thresholds are C2's owner-approved lines, unchanged; the charts, site and models are stage C's, unchanged. No threshold, margin or construction constant was set from any track-U or stage-C value. The oracle feasibility stage changed only cost forecasts."

### 7.3 Registered "does not establish" list
1. **Necessity or uniqueness of the carrier.** ψ_comp = 1 − ψ is an identity at the readout (C2ND Lemma N1); redundancy is not tested.
2. **Which upstream computation produces the code's beyond-four variation** (attention to early positions, or belief formation): the interchange is at the readout only.
3. **Specificity against y-information** inside the code beyond the five nuisance covariates (SPECIFICITY_NOT_ESTABLISHED; no natural placebo exists here).
4. **Use of the circle for the last-four part of the prediction.** On pairs that part is invisible by design.
5. **Other positions, horizons beyond w33, other counterfactual families, other sites, other worlds, other architectures, other training seeds** (three draws of the training process, not a population).
6. **That the stage-C chart is "the" circle**, or that the code contains all circle information (Q-CODE-U).
7. **That LOW_RESPONSE means suffix-only prediction**, or that INCONCLUSIVE means non-use.
8. **Any change to earlier verdicts:** stage C's SUPPORT, K4b's EXCLUSION, C2's USED, C2ND's results, and anything about the E4 models or the stage-B pilots.
9. **That the oracle-ideal share is a bound on a model's share.** It is a comparator only (§4.3).
10. **That the interchanged state is a natural state.** Harmless here because the head is linear (C2 Lemma R remark d), but stated.
11. **That the code's beyond-four component is a change of circle phase.** Δc includes any beyond-four change of code magnitude, e.g. LayerNorm-scale or confidence modulation of suffix-determined code content.

---

## 8. Blindness, hygiene, registry and track-D disjointness

### 8.1 Blindness
- **Roles.** The implementer and the two test authors read this plan (once frozen), `API.md`, `CONTRACT.json`, `TEST_PLAN.md` and the reused code.
  - **They never read** the public research-summary paths; stage-B `REPORT.json`, `stages/EVAL/`, `GATES.jsonl`, `CHART_CONSTRUCTIONS_*.json`, `ah/jobs/0175/` (the HWSC list); `hwsc-store/stages/S8/RESULT.json`, `SEALED_*.json`, `stages/S5/VALIDATION_REPORT.json`, `stages/E1/L1.json`, or TRAIN_RECORD `dev_ce`; any track-D planning file, `HWSD-*`, or `hwsd-store` report; any `sealed/` file.
  - The reviewer of this plan is result-blind to track D and to any HWSU data (none exist).
- **Code.** `hwsu_config.blinded` extends `hwsc_config.blinded`/`guard` (`tp/tools/hwsc/hwsc_config.py:171-203`) [V]. The added paths are `hwsc-store/{stages/S8, stages/S5, stages/E1/L1.json, SEALED_VALIDATION.json, SEALED_OPENED.json}`, `ah/planning/**/*hws-dyn*`, `ah/planning/**/HWSD-*` and `hwsd-store/**`. The only `hwsd-store` exceptions are the files the frozen registry reader opens (§8.3). An attempt raises FAIL_TECHNICAL/BLINDNESS (tested in DRY).
  - The needle search `hwsu_seed.seed_search_u` prunes with this list before any open (RC-3, J5). Track D's round files are on it.
- **Stage-C values quoted in this plan (S7).** §1.1 and §1.4 quote stage C's outcome values, which come from the request and from `RESULT.json`. Implementers and test authors who read this plan therefore see them. This is harmless: stage C's outcome is not HWSU data, and no HWSU threshold, construction or computation depends on it. They still never open `RESULT.json` itself.
- **Planner disclosure:** §14.

### 8.2 Namespace reservation and the two-track rule (whichever runs first)
1. **Now (before either design freeze).** The coordinator records a namespace reservation table in the mailbox (one commit, sha256 bound by both tracks' G0). **(J3)** This table is `ah/records/HWS_UD_NAMESPACE.json` (sha256 b4c6d6ff…7b427b5e) [V, record read]. HWSU reserves:
   - the scopes `hwsu-of-v1`, `hwsu-v1`, `hwsu-dry-v1`;
   - the store `root/hwsu-store`; the dry stores `scratch/hwsu-dry*`; the test roots `scratch/test_hwsu-*`;
   - the seeds 640101–640120 and 649901–649920.

   Track D's reservation in the same record: scopes `hwsd-v1`, `hwsd-dry-v1`; store `root/hwsd-store`; `scratch/hwsd-dry*`, `scratch/test_hwsd-*`; seeds 620400–620499 and 629950–629999.

   Track D's reservation must not contain any HWSU token, and HWSU's G0 fails closed if it does. Track D's tokens are declared needles in HWSU's search (OF-0). Whole-token needle search (OF-0, KC0) classifies any other hit; unclassified → FAIL_TECHNICAL/SEED_SCOPE.

   The reservation table also fixes, for both tracks, that every fresh history file is written either as a K4b history table (`canon32`, `seq_ids`, a `digest` column re-derivable from `canon32`) or as an ObservationSet, and is listed with its sha256 and reader in the track's `REGISTRY_OBLIGATION*.json` at the end of each drawing stage.

   G0-OF, KC0 and G0U bind the sha256 of `HWS_UD_NAMESPACE.json` and of `HWSC_W2_END.json` (J3).
   - **(J10)** They also bind the joint rulings addenda 1–3: `coord-hws-ud-20261101.joint-rulings-addendum-1.md` (241040fb…c22b), `-addendum-2.md` (6644433a…d9b5) and `-addendum-3.md` (127d08fe…c092).
   - Where J10 and rule 3 of `HWS_UD_NAMESPACE.json` differ, J10 governs (§8.2 item 4).
2. **Streams.** Different scope strings give different `SeedTree` streams. Exact digest disjointness is nevertheless enforced by the registry, not assumed.
3. **Windows (K4B §3.5 W2/W3).** The coordinator never lets two studies hold overlapping history-generation reservations. A study's reservation runs from its first draw to its last draw. HWSU holds one reservation for OF, and another from REG1 through the last test block, renewed per job.
   - **(J2, J3) Serial generation.** At most one live history-generation reservation exists across all studies.
   - **(J8) One reservation-end form for both tracks** (joint rulings addendum 1, `coord-hws-ud-20261101.joint-rulings-addendum-1.md`, sha256 241040fb…c22b).
   - **No edits.** A reservation file is never edited after creation.
   - **The end record.** `hwsu_records.end_reservation(store, reservation_id, utc, obligation_path)` writes, by exclusive create, `<store>/reservations/<reservation_id>.END.json`. It is written only after the obligation file exists, and it is called right after that obligation record is written: `REGISTRY_OBLIGATION_OF.json` after OF; `REGISTRY_OBLIGATION.json` at study end. Its fields:
     - `schema` "hws-reservation-end-v1";
     - `reservation_id`;
     - `reservation_file` and `reservation_sha256`;
     - `end_utc`;
     - `obligation_file` and `obligation_sha256`;
     - `written_by`.
   - **Refusals.** It refuses when the reservation is not ACTIVE, the obligation is absent, or the end record exists.
   - **W2 attestation.** A history-generation reservation counts as ended if and only if one of these holds:
     - The attestation inspects every `<root>/*/RESERVATION*.json` and `<root>/*/reservations/*.json` (end records excluded); a reservation is ACTIVE iff its top-level `state` is `"ACTIVE"`. On 2026-11-01 only `RES-HWSC-W2` qualifies; `c2nd-store/RESERVATION_S{1,5}.json` carry no `state`.
     - (a) it is `RES-HWSC-W2` and `records/HWSC_W2_END.json` (sha256 2390e29d…) is bound and matches (§3.1 (b));
     - (b) an end record of the schema above exists whose `reservation_sha256` equals the current reservation file's sha256 and whose `obligation_sha256` equals the current obligation file's sha256.

     Any other ACTIVE reservation is live, so the attestation is INCONCLUSIVE/AUTHORITY. The same rule recognises track D's end records (`hwsd_data.end_reservation`, same schema).
   - **HWSU's own reservation files (S-3).**
     - **OF:** `hwsu-store/RESERVATION_OF.json`, id `RES-HWSU-OF`.
     - **Model phase:** `hwsu-store/RESERVATION_U.json`, id `RES-HWSU-U`, held from REG1 through the last test block.
     - **Reruns (J10 item 3):** a new id in a new file: `RESERVATION_OF-a<k>.json` / `RES-HWSU-OF-a<k>`, and `RESERVATION_U-a<k>.json` / `RES-HWSU-U-a<k>`.
     - These names, `reservations/*.END.json` and the `REGISTRY_OBLIGATION*.json` names of item 4(b) are on `hwsu-store`'s record allowlist (the `lineage_c`-style check of `hwsu_records`).
   - **Stopped drawing job (J10 item 3).** Suppose a drawing job (OF, E1, E2) stops after its reservation starts and before its first row. It writes `REGISTRY_OBLIGATION_<job>-a<k>.json` (no history file) and calls `end_reservation` with that obligation before it exits. A rerun starts a new reservation id in a new file, as above. If the stop comes after the first row, it is a lineage stop under §6's rules, and the obligation is still written before exit. The J8 end record binds the obligation of the job that drew.
   - **Tests (author B).**
     - `end_reservation` ends an ACTIVE reservation.
     - It refuses one that is not ACTIVE, one without its obligation, and a second call.
     - The attestation treats a reservation without a valid end record as live, and a reservation whose file changed after its end record as live.
     - The attestation accepts the other track's end record in this schema (fixture).
4. **The later registry covers the earlier store.**
   - **(a)** If `hwsd-store` exists when HWSU builds the KC5 rehearsal or REG1, HWSU requires `hwsd-store/REGISTRY_OBLIGATION.json`, naming each history file with its sha256 and its reader. The reader must be one of the two frozen generic readers:
     - the K4b history-table reader: `canon32`, `seq_ids` and a `digest` column re-derived from `canon32` (the `hwsc_registry.source_own` pattern, `:282-303`) [V];
     - `hwsb_registry.registry_digests` for ObservationSets.

     With exact inventory match, this is READER. Anything else (another format, an unlisted file, an unreadable file) is **REGISTRY_INCOMPLETE**, and nothing is drawn. The coordinator may add a reader only by a reviewed CONTRACT erratum before the HWSU execution freeze.
     - (J3) In the root table, `hwsd-store` is READER_IF_PRESENT with exactly these closed reader classes. A store present without an obligation, a sha256 mismatch, an unlisted array file or an unknown class → REGISTRY_INCOMPLETE.
     - (J4) The same holds for every `scratch/hwsd-dry*` store: it must carry its own `REGISTRY_OBLIGATION.json` in the closed format, else REGISTRY_INCOMPLETE. No exception is made.
     - **(J10, superseding the "history files only" form above where they differ.)**
       - HWSU reads every `REGISTRY_OBLIGATION*.json` present in `hwsd-store`, and in each `hwsd-dry*` store.
       - The newest one by `written_utc` must list every array file then in the store, each with its relpath, its sha256 and exactly one class:
         - **ObservationSet**, or **K4b history table**, each read by its reader above;
         - **NON_HISTORY**, with one closed basis:
           - (i) WorldSpec, TransitionSpec, EmissionSpec or Checkpoint, classed by its sibling `meta.json`. A Checkpoint `state.pt` or `payload.npz` is classed by `meta.json` only and is never opened or hashed by HWSU;
           - (ii) a file under `registry/**`;
           - (iii) a chart, decoder, activation, oracle-moment, score, bootstrap or certificate array, matched by the owning track's frozen name rule, which the obligation copies.
       - NON_HISTORY files are checked by sha256 only. HWSU does not hash a `state.pt` or `payload.npz` (basis (i)); its listed sha256 is not re-computed.
       - Any of the following → REGISTRY_INCOMPLETE: a store present without an obligation, a sha mismatch, an unlisted array file, or an unknown class or basis.
       - A track-D dry store that aborted before writing its obligation stays REGISTRY_INCOMPLETE until a recorded coordinator step writes one listing every array file present (J10 item 4).
   - **(b)** HWSU writes `hwsu-store/REGISTRY_OBLIGATION_OF.json` at the end of OF, and `REGISTRY_OBLIGATION.json` at the end of the study. Each gives every history file, its sha256 and its reader, in the same generic formats, so track D can cover HWSU whichever runs second.
     - (J4) Every HWSU dry run (`scratch/hwsu-dry*`) writes its own `REGISTRY_OBLIGATION.json` in the same closed format at its end. A HWSU dry store without one is REGISTRY_INCOMPLETE for track D.
     - **(J10) One obligation per writing job.** Every job that writes into `hwsu-store` ends by writing an obligation, including a stopped attempt. It is written by exclusive create and lists every array file then in the store, with the classes and closed bases of 4(a). Names:
       - `REGISTRY_OBLIGATION_OF.json` for the OF stage;
       - `REGISTRY_OBLIGATION.json` at study end (the E2 job that completes the study);
       - `REGISTRY_OBLIGATION_<job>-a<k>.json` for every other job and attempt: J-OF/J-U store writes if any, KC, E1, REG2, an E2 that does not complete, and every stopped attempt, OF's included.
     - **HWSU's NON_HISTORY name rule (basis (iii)), frozen in `CONTRACT_OF.json` (phase-1 arrays) and `CONTRACT.json` (phase-2 arrays) and copied into each obligation.** It covers `stages/**` files named:
       - `ACTS_*`, `Y_*` (activations and readout coordinates);
       - `ORACLE_*`, `MOMENTS_*` (oracle moments, q4, G);
       - `FIT_*`, `DECODER_*`, `DECOY_*` (fits, projectors and decoders: linear decoders and readouts of activations; KU head constructions);
       - `BOOT_*`, `SCORES_*`, `PAIR_*`, `ENDPOINT_*`, `CERT_*`, `PREC_*` (bootstrap arrays; score and per-pair statistic arrays, including the endpoint arrays; certificate and precision arrays); `FRAMES_*` (Haar and other projector frames, basis (iii) as a decoder/projector under the coordinator's reading). `hwsu_records` refuses to write an array file under `hwsu-store` whose name matches neither this rule nor `HIST_*` (FAIL_TECHNICAL/LINEAGE at write time), so the list is closed by construction.

       Charts are not written by HWSU (the stage-C charts are read in place). History tables are K4b history tables (`HIST_*`); dry stores use their DRY names under the same classes.
     - **Dry stores (J10 item 4).** HWSU dry stores follow the same rules. A HWSU dry run that aborts before writing its obligation is recovered by a recorded coordinator step: an obligation listing every array file present, written before any other track's registry build. Until then the dry store is REGISTRY_INCOMPLETE for both tracks.
   - **(c)** The R8 root inventory treats any top-level directory not in the frozen table, holding any history file, identity reference or ObservationSet root, as REGISTRY_INCOMPLETE (K4B lines 252–262; HWSC R8) [V].

### 8.3 The HWSU exposure registry (K-REG1; K-REG2 adds the U rows)
`hwsu_registry.build` is a mirror of `hwsc_registry_build.build` (`tp/tools/hwsc/hwsc_registry_build.py:60-153`) [V]. The mirror is needed because `build` hard-codes the hwsc versions, the `hwsc-reg-v1` label, the protocol sha256 and the hwsc own-source. The dry run checks that, with stage-C's source map, the mirror equals `hwsc_registry_build.build` on a synthetic root (DRU-REG). Its sources are:

| # | Source | Reader | Basis |
|---|---|---|---|
| U1 | everything stage C's K-REG2 covered: C2/C2ND readers, the X6 base, hws, x6zc, c2nd, hwsb (HANDOFF `store_inventory`), the stage-A/B/C dry stores, the scratch table | the unchanged `hwsc_registry_build._default_sources` callables (:34-52) [V] | the newest frozen registry: stage C's K-REG2 PASS, 8,348,018 digests (`hwsc-store/registry/K-REG2.json` `n_digests`) [V] |
| U2 | `hwsc-store`: ObservationSets (train and dev × 3 masters, superseded included), `stages/S3/HIST_{lgate,cal,val}_b0.npz`, `stages/S7/HIST_test_b0.npz`, `superseded/**/HIST_*.npz` | (i) ObservationSets and superseded HIST tables: `hwsc_registry.source_own(hwsc-store, expected=OBS_INVENTORY)` unchanged (`hwsc_registry.py:282-303`), where `stages/TRAIN/OBS_INVENTORY.json` must re-hash to its TRAIN_INVENTORY STAGE_COMPLETE entry. (ii) `stages/S3/HIST_{lgate,cal,val}_b0.npz` and `stages/S7/HIST_test_b0.npz`: the K4b history-table reader, each file re-hashed against its S3/S7 STAGE_COMPLETE entry. (iii) Classed without opening: `artifacts/{WorldSpec, TransitionSpec, EmissionSpec, Checkpoint}/**` and `superseded/*/artifacts/**` by the artifact type in `meta.json`; `registry/**`; `stages/S4/ORACLE_*`; `stages/S4a/{ACTS,CHART,DECODER,INIT_CHART}_*`; `logs/**`; `tmp/**`. `sealed`-type files are never opened. (iv) Any other array file, or any STAGE_COMPLETE-listed history file that is missing or does not re-hash → REGISTRY_INCOMPLETE.<br>(J1 merge) This is the joint layout reader: `source_own` reads ObservationSets through `hwsb_registry.registry_digests(expected=OBS_INVENTORY)` and `superseded/**` file by file with the same two readers. **Superset check (J1):** after K-REG1 is built, every digest of stage C's `hwsc-store/registry/K-REG2_digests.npz` (bound by `K-REG2.json` `digest_file_sha256` 07215343…2654 [V]) must be in HWSU's K-REG1 digest set, else REGISTRY_INCOMPLETE. The check compares the two stored sorted digest arrays chunk by chunk (no second in-memory set). Its peak memory is recorded at the KC5 rehearsal, which runs the same check against stage C's K-REG2. The run opens this registry digest file; it is not a history payload.<br>**(S-2)** Stage C's K-REG2 digest set is also a **union source** of K-REG1 (U8 below). The superset check is then run on the reader-built union, before U8 is added, and kept as a **diagnostic**: the missing digests are counted and listed. A miss is covered by U8 instead of stopping the study, for example a scratch file deleted since 2026-10-29. This supersedes "else REGISTRY_INCOMPLETE" above; J1's check stays, as a diagnostic | `STAGES.jsonl` STAGE_COMPLETE records (sha256 bound in G0U) and `OBS_INVENTORY.json` |
| U2′ | `hwsu-store/` dry and test stores of HWSU itself: `scratch/hwsu-dry*`, `scratch/test_hwsu-*` | each dry store by its own `REGISTRY_OBLIGATION.json` with the closed reader classes (J4; contents and newest-governs rule per J10, §8.2 4(a)); test roots: EXCLUSION by the frozen fixture rule of the HWSU scratch table (synthetic DRY-scope rows only; any `HIST_*`-named file, ObservationSet root or file holding a registered-scope sequence id → REGISTRY_INCOMPLETE) | J3, J4, J10 |
| U3 | stage-C dry and test stores: `scratch/hwsc-dry*`, `scratch/test_hwsc-*` | the HWSC R5 token reader and the stage-C dry-type rule (`hwsc_drystore.dry_class`, :75) [V] | REGISTRY_OBLIGATION `dry_stores` |
| U4 | every other new scratch directory since stage C's frozen scratch table (2026-10-29) | a frozen **HWSU scratch table** (one row per top-level directory: READER or EXCLUSION with reason), built at implementation by a read-only header scan (`hwsc_scratch.scratch_scan` semantics, :44) [V] and reviewed before the freeze; re-scanned at KC5, REG1 and REG2. (J3) The scratch check recognises `hwsu-*` and `hwsd-*` directories by the reserved globs of `HWS_UD_NAMESPACE.json` (`hwsu-dry*`, `test_hwsu-*`, `hwsd-dry*`, `test_hwsd-*`); they are routed to U2′ and U5 rather than to the scratch table | HWSC R6 |
| U5 | `hwsd-store` and `scratch/hwsd-dry*` (READER_IF_PRESENT, J3; dry stores J4) | §8.2 4(a): every `REGISTRY_OBLIGATION*.json` present is read; the newest by `written_utc` must list every array file with class ObservationSet, K4b history table or NON_HISTORY with a closed basis (J10) | track D; J10 |
| U6 | HWSU own lineage: OF tables (`stages/OF/HIST_OF_*`), then the E1 tables (K-REG2) | K4b history-table reader against the STAGE_COMPLETE file lists | own rows are never reused |
| U7 | the root inventory (R8) | `k4b_registry.inventory`/`classify` against a frozen table extending stage C's by `hwsc-store` (READER U2), `hwsu-store` (OWN), `hwsd-store` (READER_IF_PRESENT U5, J3), with deep-scan exclusions for them; both tracks' dry and test globs listed (J3) | fail closed |
| U8 (S-2) | stage C's K-REG2 digest set: `hwsc-store/registry/K-REG2_digests.npz`, with the file sha256 equal to `K-REG2.json` `digest_file_sha256` 07215343…2654 | a union source of digests, read as a stored digest array. A sha256 mismatch → REGISTRY_INCOMPLETE. The U2 superset check runs before this source is added and is a diagnostic | stage C's K-REG2 PASS record |

**Requirements (K4B line 268, unchanged).** U_fit, U_kfit, U_feas and U_val (every arm) are disjoint from K-REG1 and from each other. U_test is disjoint from K-REG2. K-REG1 ⊇ stage C's K-REG2 digest set (J1, U2; it holds by U8, and the reader-built superset check is a diagnostic, S-2). Sequence ids are disjoint from every frozen union. Every row fails the sealed-D-2a predicate. A collision is FAIL_TECHNICAL/LINEAGE; there is no replacement sampling.

### 8.4 Hygiene
- Dry stores never use `HIST_*` names, and dry runs never use the registered scopes (C2 coordinator addendum 4 lesson) [V].
- Pytest basetemps and meter temp folders are under `scratch/test_hwsu-<job>/` (the K4b registry trap).
- Repeated dry runs set aside the old `hist/` (R-0157-1, HWSC §9.3) [V].
- After each implementation or dry job, a read-only header inventory of `root/` must show no new history file, identity reference or ObservationSet root.

---

## 9. Synthetic dry run (addendum 25 rule 4; before each freeze)

**Phase OF dry run (DRO; scope `hwsu-dry-v1`, `scratch/hwsu-dry-of/`).**
- DRO1: the whole OF driver on a tiny synthetic world (W = 6, H = 2, L = 32), with every gate returning a value. The loader refuses a `CONTRACT.json` with a wrong `contract_of_sha256` or one that overrides a phase-1 key.
- DRO2: KS-PAIR exact on a non-reversible tiny chain, with planted sampler defects caught.
- DRO3: OF-1 identities with planted defects (q4 from the wrong window; λ ≠ 1/5) caught.
- DRO4: OF-3 and OF-4 on a planted oracle with a known ψ_orc (pass and fail fixtures).
- DRO5: OF-5 with a planted biased sampler → FAIL.
- DRO6: blindness guard; records; exclusive create; ledger. A planted needle in a file named `coord-hws-dyn-x.md` and in `hwsd-store/x.json` is not found, and an access hook records zero opens of either; a planted needle in an undeclared file → FAIL_TECHNICAL/SEED_SCOPE. Hits of HWSU tokens in a fixture `hwsu-store/FREEZE_OF.json`, a `docs/code_index/files/tools/hwsu/*.md` page and a `tools/hwsd/CONTRACT.json`, and hits of track-D tokens in `tools/hwsu/CONTRACT.json`, are classified as declarations; the same tokens in `topo-pilot/src/x.py` are unclassified. (J9) Under a fixture `hwsd-store/`, a token in `REGISTRY_OBLIGATION.json`, in `reservations/x.END.json` or in a reservation file is searched and declared; the same token in `hwsd-store/x.json` is pruned unsearched (an access hook records zero opens).
- DRO9 (J10 item 5; fixtures in track D's form, in a synthetic root):
  - a store whose newest obligation lists NON_HISTORY artifact payloads (classed by `meta.json`, never opened), `registry/**` files and named arrays → PASS;
  - the same store with one unlisted chart array → INCOMPLETE;
  - a store holding only known-case records and their obligation → PASS;
  - an older obligation that lists everything, but a newer one that omits a file → INCOMPLETE (the newest governs);
  - an OF drawing job stopped before its first row writes a no-history obligation and ends `RES-HWSU-OF`, and the rerun opens `RES-HWSU-OF-a2`;
  - an aborted dry store without an obligation is INCOMPLETE until the recorded coordinator obligation exists;
  - an attempt to write `hwsu-store/stages/X/OTHER_1.npz` is refused at write time.
- DRO7 (RC-5, RC-10, J2–J4, J8): OF-H with a planted sealed-D-2a row → INCONCLUSIVE/REGISTRY_INCOMPLETE before any OF value; OF-B refuses a phase-1 file changed after `FREEZE_OF.json`; a planted track-D token overlapping an HWSU token → FAIL_TECHNICAL/SEED_SCOPE; the J8 `end_reservation` and W2-attestation tests of §8.2 item 3, including a fixture end record in track D's form; the dry store writes its own `REGISTRY_OBLIGATION.json` (J4).
- DRO8 (S3): a planted OF-3 failure gives OF_PASS_RESPONSE_ONLY, the share family is dropped, and no share array is formed downstream.

**Pass:** every expected result exactly. **Cost:** ≈ 100 CPU-s per run [W].

**Model-phase dry run (DRU; `scratch/hwsu-dry/`; the DRY scope only; tiny or random-initialised models; no real checkpoint opened).**
| # | Case | Expected |
|---|---|---|
| DRU1 | full pipeline on the tiny world: three tiny trained models (1 layer, d_model 16, 200 steps; the HWSC DRC1 pattern), synthetic charts, every gate through REPORT on a synthetic root | every record complete; every gate returns a value |
| DRU2 | real architecture (4 layers, d128), random initialisation, 2,048 in-memory w\* DRY pairs: readout basis, M0, X1, head-edit decoys, the closed form | identities hold; nothing persisted |
| DRU3 | planted-truth readouts: KS-USE → USED; KS-IGNORE → LOW_RESPONSE; D-NULL → NOT_USED; decoy code → NOT_USED or LOW_ALIGNED; the DECOY_PARTIAL fixture → qualifier carried on the PARTIAL licence; dose → PARTIAL | exact categories |
| DRU4 | decision rules at every boundary; Lemma FW-U grid; 2-of-3 aggregation; INCONCLUSIVE/NOT_RESPONSIVE; rule-6 statements; qualifiers | exact |
| DRU5 | P1: the max rule, SHARE_PRECISION_LIMITED; P1 reads no model mean (a fixture where only mean(A_full) differs gives an identical N) | exact |
| DRU6 | sealing: a validation report that would reconstruct θ̂ or ψ̂ is refused; KU releases carry PASS/FAIL only; `SEALED_OPENED.json` inside the ENDPOINT STAGE_COMPLETE | as stated |
| DRU7 | the call-allowlist audit: a planted call to `c2_model.load_models`, `c2_oracle.load_process`, `c2_stats.p1` or a C2-seed default is caught; a planted call to `c2_model.m0` on a stage-C fixture is caught by the audit; a function reading an unlisted `c2_config` name fails closed | as stated |
| DRU-REG | registry mirror against `hwsc_registry_build.build` on a synthetic root (bitwise manifest digests); U2 reader with planted missing, renamed and unreadable files; a planted unlisted `hwsd-store` → INCOMPLETE; a conforming `hwsd-store` obligation → READER; `sealed/` never opened (an access hook records zero opens); U2 with a planted Checkpoint `payload.npz` (classed by type, never opened: an access hook records zero opens) and a planted S3 table whose sha256 differs from STAGES.jsonl → INCOMPLETE; (J1, S-2) a planted K-REG2 digest file with one digest missing from the reader-built union → the diagnostic counts and lists it, K-REG1 contains it through U8, status PASS; a K-REG2 digest file whose sha256 differs from `K-REG2.json` `digest_file_sha256` → INCOMPLETE; (J3, J4) a `hwsd-dry*` store without an obligation → INCOMPLETE; (J10) the DRO9 obligation fixtures repeated against `hwsu_registry`'s U5 reader, plus an E1 attempt stopped before S3 (a no-history obligation, `RES-HWSU-U` ended, the rerun on `RES-HWSU-U-a2`) and a KC job's `REGISTRY_OBLIGATION_<job>-a1.json` accepted by a track-D-form reader fixture | as stated |
| DRU8 | stage-C binding: H1-U on fixture records (a planted checkpoint id from `stage_c_exclusions` refused; a chart sha256 off by one byte refused; `dev_ce` never read: a key-access hook) | as stated |
| DRU9 | budget: per-stage and cumulative 3× triggers; ledger labels unique per attempt; meter output cap read from the CONTRACT | as stated |

**Pass:** every expected result exactly. The report is committed, bound to the implementation hash and accepted before the execution freeze. **Cost:** ≈ 300 CPU-s per run [W]: HWSC DRY 121–142 s measured over 9 runs (`ah/HWSC_CPU_LEDGER.json`) [V], plus the oracle, fits and bootstraps here.

---

## 10. Adaptive budget (addendum 26; addendum 37 item 7)

### 10.1 Measured basis [H unless marked]
- **C2:** S0 66.0 (S7, from the review), S1 724.5, S2 192.1, S3 327.4, S4 761.7 and S5 1,042.3 CPU-s; total 3,114.4 (`ah/jobs/0111`–`0115/review.md`) [V; S0 [H]].
- **C2ND:** S1 1,675.7; cumulative through S4 2,759.5; total 3,868 (`ah/jobs/0163/review-a2.md`, `0166/ACCEPT_REVIEW.md`, `0167/review.md`) [V].
- **Stage C, from the study ledger `ah/HWSC_CPU_LEDGER.json`, summed by the writer [V]:**

  | Stage | Runs | CPU-s | Central (3× line) |
  |---|---|---|---|
  | J-C1 | 11 | 6,603.7 | 1,200 (3,600) |
  | DRY | 9 | 1,139.4 | 600 (1,800) |
  | KC | 4 | 2,219.4 | — |
  | TRAIN | 3 | 5,563.5 | — |
  | E1 | 1 | 1,578.2 | — |
  | E2 | 3 (REG2 killed, REG2, E2) | 1,482.5 | — |
  | Total | | 18,586.6 | |

  - **J-C1 overran its 3× line by 1.8×**, through pre-freeze iterations and post-freeze corrections (D-0187-1…3, D-0192-1, the 0193 test leak).
  - Registry builds: 281.75 / 290.97 / 286.88 CPU-s (REHEARSAL, K-REG1, K-REG2 JSON `cpu_s`) [V]; each digest file ≈ 0.38–0.40 GB [V, listing].

### 10.2 Stage forecast and 3× lines [W] (single thread; measure-only, never a cap)
Repeats are budgeted from stage C's record: about 5 J-U runs and 4 dry runs, against 11 and 9 in stage C, because track U adds no training path and no new chart path.

| Stage (one job each attempt) | Content | Central CPU-s | Range | Stage 3× | Cumulative central | Cumulative 3× |
|---|---|---|---|---|---|---|
| J-OF ×2 | phase-1 tests + PF subset | 900 (2 × 450) | 600–1,800 | 2,700 | 900 | 2,700 |
| DRO ×2 | OF dry run | 200 (2 × 100) | 100–600 | 600 | 1,100 | 3,300 |
| **OF** (own approval) | §4 | 700 | 400–1,500 | 2,100 | 1,800 | 5,400 |
| J-U1 ×5 | full tests + PF suites | 3,250 (5 × 650) | 1,800–6,500 | 9,750 | 5,050 | 15,150 |
| DRU ×4 | §9 | 1,200 (4 × 300) | 500–2,400 | 3,600 | 6,250 | 18,750 |
| KC ×2 | KC0–KC6 (G0 ≈ 490; rehearsal ≈ 290); one repeat budgeted (stage C: 4 KC runs) | 2,000 (2 × 1,000) | 1,200–5,000 | 6,000 | 8,250 | 24,750 |
| E1 (release A) | G0U … P1: REG1 ≈ 290; oracle on 32,768 histories; 8 FIT problems × 3 + GLS-REF; feas (incl. the S6 descriptive chart check ≈ 300); val, X1, KC-U | 2,000 | 1,200–4,500 | 6,000 | 10,250 | 30,750 |
| REG2 ×2 | K-REG2 (booked to E2); one repeat budgeted (stage C: REG2 killed and rerun) | 600 (2 × 300) | 500–1,800 | 1,800 | 10,850 | 32,550 |
| E2 (release B) | 300 + 700·k: T-PRE, forwards, X1, and 20,000-draw bootstraps of ≈ 40 arrays per block | k = 1: 1,000; 2: 1,700; 4: 3,100; 8: 5,900 | ×0.6–×2 | 3× its central at the released k | 11,850 / 12,550 / 13,950 / 16,750 | 35,550 / 37,650 / 41,850 / 50,250 |
| **Total** | | **≈ 11,850 (3.3 CPU-h) at k = 1; 13,950 (3.9 h) at k = 4; 16,750 (4.7 h) at k = 8** | | | | |

- **Model phase alone** (J-U1 through E2): 10,050 / 10,750 / 12,150 / 14,950 CPU-s at k = 1 / 2 / 4 / 8 [W, the table minus phase OF's 1,800].
- **If OF ends OF_PASS_RESPONSE_ONLY (S3):** the KU and share computations are not run; the model-phase forecast is re-stated before that approval.
- **J-U central (S5).** The 650 CPU-s J-U central is set, before the OF approval, from the last measured runs of the suites in the PF list. Stage C's J-C1 runs averaged ≈ 600 CPU-s without `tests/c2_readout`, `tests/c2_nd` and `tests/hwsc`; the coordinator reads those suites' last measured metered runs and writes the re-set central into the CONTRACT (cost only).

- **Likely k [W].** P1's blind share alternative (0.03·E[G] ≈ 0.0019 nat at E[G] ≈ 0.062), with a per-pair SD of 0.05–0.08 nat, needs 9,000–23,000 pairs (mde = 3.555·SD/√N). So k = 4–8 is likely, and the planning central is **≈ 16,750 CPU-s (4.7 h) at k = 8**. OF-4 replaces this desk SD with a measured proxy before the model-phase approval.
- **E2's central is fixed** by the formula at release B from the released k, before any test row.
- **Re-setting.** After OF and after KC5 (rehearsal registry CPU), the J-U, E1 and E2 centrals are re-set from measured cost (cost, not data) and written into the CONTRACT. The owner forecast is restated if the total moves by more than 20 %.

### 10.3 Pauses, caps and extension rules (frozen)
- **Meter settings:** `--max-cpu inf --max-wall inf` (the meter kills at 600 s by default, so measure-only is explicit).
- **Disk floors:** C: ≥ 2 GB, X: ≥ 30 GB.
- **Memory caps:** 12 GiB for KC, E1, REG2 and E2 (an ≈ 8.4 M-digest registry in memory); 8 GiB for J-OF, J-U and the dry runs.
- **Native-operation wall:** 600 s.
- **Meter output cap (a CONTRACT resource `resources.output_cap_bytes`, read by `hwsu_meter_bind`, never hard-coded).**
  - It is compared with the whole out directory, which for store jobs is all of `hwsu-store` (the D-0192-1 lesson) [V, `ah/jobs/0192/review.md`].
  - Forecast store size [W from V]: stage C's store measures 5.4 GB, of which `registry/` is 4.0 GB (per version a ≈ 0.39 GB digest file plus a ≈ 0.99 GB X6 run directory). HWSU holds three registries (≈ 4.2 GB), plus history tables, activations and readout coordinates for 3 models (≤ 0.15 M histories × 3 × 2 × 128 × 8 B ≈ 0.9 GB), plus fits and records: **≈ 5.5 GB**.
  - The cap is set at **16 GiB** (stage C's corrected value), about 3× headroom. KC5 records the measured store size and requires the projected end-of-study size ≤ cap/2; otherwise the coordinator raises the cap by a reviewed resource erratum before E1 (a resource, never a scientific parameter).
- **Pause triggers.**
  - *Per stage:* the running stage CPU exceeds 3× its central.
  - *Cumulative:* the running total exceeds 3× the cumulative central through the current stage.
  - Both are checked at every item boundary (each gate, each model, each known case).
  - On a trigger no new item starts, and the coordinator reports CPU, item and projection only, with no gate value. Continuing needs the owner. Not continued → INCONCLUSIVE/RESOURCE_OR_AUTHORITY.
- **Ledger:** `ah/HWSU_CPU_LEDGER.json`, with a unique label per attempt (the HWSB ledger-label lesson). Test and dry-run repeats are counted and reported (addendum 37 item 7).
- **Extension rules.**
  - **X-1.** No stage grows on a scientific reading.
  - **X-2.** The only growth is N, chosen once at P1 from blind quantities (VAL SDs, centred draws, oracle means), on the frozen ladder.
  - **X-3.** Technical corrections follow K4B §11.8 (at most 2 per defect). Each correction's J-U and DRU repeats are booked to their stage lines and reported.
  - **X-4.** OF can only stop the study or re-set cost centrals. It never changes a threshold, margin, ladder value or construction.

### 10.4 Plain-language forecast for the owner (to be said when asking for each run approval)
"This study trains nothing. It takes the three small models from the last test and asks a simple question. When we change only the older part of a history, and keep the last four symbols the same, does the model's guess about the next symbol shift the way the ideal predictor's guess shifts? And how much of that shift passes through the model's internal circle?

First comes a short check that uses only the ideal predictor and no model: is there enough of this older-history effect to measure, and could a circle carry a meaningful part of it at all? That check needs about half an hour of processor time, including its tests, and its own yes from you. If it shows there is too little of the effect to measure, we stop there. If it shows only that a circle could not carry a meaningful part of it, we drop the circle question. I would then ask you whether to go on with the first question alone.

If it passes, the main part follows: building and testing the code, a rehearsal on made-up data, and then the measurement on fresh histories. The main part is about three to four hours of processor time, depending on how many fresh histories the precision rule asks for. The effect is small, so the larger size is likely. Altogether that is about three and a quarter to four and three quarter hours. These are estimates, not limits. If any part runs past three times its estimate, I stop and ask you.

At the end I will tell you, for each model:
- whether its prediction follows the older history in the right direction;
- whether most, part or almost none of that runs through the circle;
- or whether the test could not decide."

---

## 11. Reuse and footprint

### 11.1 New code: `tools/hwsu/` (one new module; each `.py` ≤ 400 lines; no existing file edited)
The code is developed on branch `hwsu-impl` in an existing, inventory-listed worktree (a new top-level worktree would be an unlisted directory; the HWSC §10.1 lesson). It uses `PYTHONPATH=<worktree>/src` and the venv interpreter with `-s`. No `.npz`/`.npy` file is committed.

| File | Contents | Lines [W] | Phase |
|---|---|---|---|
| `PROTOCOL_HWSU_v1.md` (byte copy of the frozen plan), `CONTRACT_OF.json` (phase-1 call allowlist, seeds, OF resources, the phase-1 NON_HISTORY name rule, declaration fragments), `API_OF.md`, `TEST_PLAN_OF.md` | committed first | — | 1 |
| `API.md`, `CONTRACT.json` (binds `CONTRACT_OF.json` by sha256; adds the phase-2 allowlist, scratch and root tables, the phase-2 name rule and resources), `TEST_PLAN.md` | committed first in phase 2 | — | 2 |
| `hwsu_config.py` | constants, scopes, seeds, paths, CONTRACT loader (`CONTRACT_OF.json` + optional bound `CONTRACT.json`, §4.1), blindness guard | ≈ 170 | 1 |
| `hwsu_pairs.py` | `sample_prefix` (§2.1), pair tables, sequence ids, suffix checks | ≈ 200 | 1 |
| `hwsu_oracle.py` | per-arm oracle, q4/m4, d, G, KO1–KO3, Decimal rows, Lemma P cross-checks, problem O | ≈ 280 | 1 |
| `hwsu_of.py` | the OF stage (§4) | ≈ 260 | 1 |
| `hwsu_records.py` | records, freeze (`FREEZE_OF.json`, the execution freeze), sealing, ledger, pauses, lineage (HWSC patterns); `registry_risk_u`; `end_reservation` and the W2 attestation rule (J2, J8); the per-job obligation writer (J10) | ≈ 390 | 1 |
| `hwsu_meter_bind.py` | thin main over `k4b_meter_bind` (the `hwsc_meter_bind` pattern; output cap from CONTRACT) | ≈ 120 | 1 |
| `hwsu_bind.py` | call allowlist and constant-read audit (§11.2) | ≈ 200 | **1** (OF-B runs the audit; RC-10) |
| `hwsu_model.py` | stage-C loading (§3.1), activations, readout coordinates, chart extension, X1 wrapper, `m0_u` | ≈ 320 | 2 |
| `hwsu_seed.py` | `seed_search_u`, `classify_hits_u` (RC-3, J5, J9) | ≈ 100 | 1 |
| `hwsu_known.py` | G0U, KC0–KC6, KU1–KU3 constructions, DX | ≈ 280 | 2 |
| `hwsu_registry.py` | the build mirror, U2 (layout reader, J1), U2′/U5 (obligation readers, J3/J4/J10), U6 readers, U8 union source and the superset diagnostic (S-2), the scratch and root tables | ≈ 395 | 2 |
| `hwsu_gates.py` | H1-U … P1, the decision table, outcomes, licences, `haar_frames_u` | ≈ 390 | 2 |
| `hwsu_driver_of.py` | job OF; CLI | ≈ 150 | 1 |
| `hwsu_driver.py` | jobs KC, E1, REG2, E2; CLI | ≈ 300 | 2 |
| `hwsu_dry.py` | DRO | ≈ 330 | 1 |
| `hwsu_dry2.py` | DRU | ≈ 330 | 2 |

About 4.1k lines [W]. Phase 1 files are frozen by `FREEZE_OF.json` (§4.1). Every file has exactly one phase (F-2). Phase-1 tests live in `tests/hwsu/test_*_of_*.py` and are not edited in phase 2.
- **Tests** (≈ 2k lines, `tests/hwsu/`) are written by **two independent authors**, neither the implementer, who never read `tools/hwsu/*.py`:
  - **A:** sampler exactness (KS-PAIR), Lemmas P/J by enumeration, oracle identities, the decision table, Lemma FW-U grid, rule-6, aggregation, P1 blindness;
  - **B:** stage-C binding and identity, the call allowlist, the registry readers with planted defects, blindness guard, sealing, records, meter binding, basetemps outside the root, the KU constructions and DX.
- `AUTHORSHIP_A.md`, `AUTHORSHIP_B.md`. No formatter is run over `tests/`.
- After each accepted code commit: `.venv/Scripts/python.exe tools/build_code_index.py` and a separate `docs(index): …` commit (CLAUDE.md rule).

### 11.2 Reuse without editing: the call allowlist (replacing a monkeypatch binding)
Track U calls only reused functions that take every study-specific object as an argument. The CONTRACT lists each allowlisted function and the module names it reads at call time, established by an AST audit at implementation.

**Permitted call-time reads** are the shape constants and the owner-approved C2/C2ND thresholds and tolerances that the allowlisted functions use. The CONTRACT enumerates each one, per function and with its value, from the AST audit. At 8f89462 they include `c2_config.{SITES, INDEX, V, N_NUIS, RS_A, RS_B, RS_K, RANK_R, GUARD_REL, T_QSUM, TAU_X1, X1_ATTAIN, UNIT_ROUNDOFF, T18, COND_MAX, SV_RATIO, LW_RATIO, T_GLS_ID, ZERO_MOD, ZERO_CODE, R1, GLSREF_PREC, GLSREF_PROJ, GLSREF_RHO, GLSREF_INFLATE, RIDGE_GRID, L1_R2, L1_RHO, DESC_ALPHA}` with the Decimal tolerances, `nd_config.{DX_A, DX_E}` and `k4b_config.chart_cfg()`. n = 127 and k = 6 hold for the stage-C architecture.

**Forbidden** reads are identities, seeds, scopes, stores, sizes and ladders: `MODELS`, `PROTOCOL_IDS`, `SCOPE`, `PROCESS`, `CONTRACT[…]` other than the HWSC `world` block, `seed()`, `N_LADDER`, `BLOCK`, `VAL_DRAWS`, `DESC_DRAWS`, `LGATE_N`, `STORE`, `ARTIFACT_ROOT`.

A function that reads a forbidden name is never called, and HWSU uses a named mirror instead:
- `c2_model.m0` → `hwsu_model.m0_u`;
- `hwsc_data.registry_risk` → `hwsu_records.registry_risk_u` (HWSU rows, the same exact-rational ≤ 1/100 rule, after `hwsc_data.p_d2a_check`);
- `c2_code.haar_frames` → `hwsu_gates.haar_frames_u` (stream `SeedTree(640120)`, else identical);
- `c2_attrib.desc_intervals` → `c2_attrib.ratio_intervals(…, seed=640117, draws=5000)`.

An unlisted read of any kind fails closed (FAIL_TECHNICAL/BINDING).

The audit (in PF, the dry run and every job) fails closed (FAIL_TECHNICAL/BINDING) on two things:
- any allowlisted function that reads a C2-, C2ND-, K4b- or HWSC-only name (`MODELS`, `SCOPE`, `PROCESS`, `CONTRACT["models"]`, seeds, `STORE`, `ARTIFACT_ROOT`);
- any call to a never-called function: `c2_model.load_models`, `c2_oracle.load_process`, `c2_oracle.h3`, `decimal_rows`, `c2_stats.p1`, `_summaries`, the C2/C2ND stage and driver modules, `nd_decoy.head_edit` without an explicit `g`, `k4b_driver.*`, `c2_model.m0`, `hwsc_data.registry_risk`, `c2_code.haar_frames`, `c2_attrib.desc_intervals`.

`hwsc_gates.expected_meta_c` is called unchanged: its hwsc constants are the correct identities for these checkpoints.

### 11.3 Six-field reuse assessment
| Part | 1 Existing (unchanged) | 2 Missing | 3 Smallest change | 4 Invariants | 5 Regression checks | 6 Next extension (not built) |
|---|---|---|---|---|---|---|
| Attribution (C2) | `c2_model.{readout_basis, readout_coords, closed_logits, placed, x1, kappa_x1}`, `c2_attrib.{partition, energies, random_ref, pair, decomposition}`, `c2_code.{harmonics, fwl, gls, gls_identities, problem, code_pair, code_phase, fstar}`, `c2_stats.{gls_ref, delta_p, fit_decoder, l1, f1_problem}`, `c2_decide.{stream_bounds, guard, beta_A, beta_E, _category, variant_category}` | stage-C models; pair family; response family; P1 seeds and ladder | wrappers in `hwsu_gates`/`hwsu_model`; call allowlist; `m0_u`, `registry_risk_u`, `haar_frames_u` mirrors | Lemma R exactness; first non-PASS stops; no FIT/FEAS logits | `tests/c2_readout` unchanged; DRU2–DRU4, DRU7 | layer-2 interchange (C2-M) on pairs |
| Decoys (C2ND) | `nd_decoy.{head_edit, make_head_decoy, decoy_sha64, dx}` | the KU1 planted reader | one head formula in `hwsu_known` | only `unembed.weight` changes | `tests/c2_nd`; DRU3, DX | coordinate decoys (D-NULL-R) |
| Charts (K4b) | `k4b_charts.extend`, `k4b_config.chart_cfg`, `k4b_scores.sha_phase`, `oracle_moments` | — | none | frozen charts by sha256 | `tests/k4b`; SUP | — |
| Stage-C identity and data (HWSC) | `hwsc_gates.expected_meta_c`, `hwsc_data.{process_identity, p_d2a_check}`, `hwsc_records.lineage_c`, `hwsc_config.blinded`, `hwsc_registry.source_own` | key-whitelisted record loader | `hwsu_model.load_stage_c`; `m0_u`, `registry_risk_u`, `haar_frames_u` mirrors | never write `hwsc-store` | `tests/hwsc`; DRU8 | — |
| Registry | `hwsc_registry_build._default_sources`, `hwsc_registry.{source_own pattern, scratch_check, inventory_c}`, `hwsb_registry.registry_digests`, `c2_registry.Registry`, `k4b_registry.{inventory, classify}`, `k4b_data.{predicate_check, sealed_d2a_predicate}` | U2 reader (hwsc-store), U5 (hwsd), U6 (own), the new tables | `hwsu_registry` mirror (DRU-REG equality) | fail closed; never `sealed/`, never `state.pt` | DRU-REG; KC5 | a generic registry library (a separate reviewed protocol) |
| Oracle | `c2_oracle.{oracle_role, nuisance5}`, `c1_oracle.{run_oracle, G_hat, named_from_canonical, m32, decimal_reference, decimal_posterior60, decimal_G, h3_compare}`, `oracle_profile.posterior_means` | q4; the conditional sampler; problem O | `hwsu_oracle`, `hwsu_pairs` | float64; exact sampler (KS-PAIR) | `tests/oracle`, `tests/oracle_profile`; DRO2–DRO5 | R > 2 prefixes per suffix |
| Precision | `precision.{sd_b4_draws, centered_draws, precision_summary}`, `c1_means.{bootstrap_means, quantile_with_rank}` | U ladder and seeds | 15-line wrapper | blind P1 | `tests/circle_history`; DRU5 | — |
| Meter | `k4b_meter_bind`, the job-0014 meter, `op_guard` | the HWSU store and cap | `hwsu_meter_bind` | measure-only CPU; cap from CONTRACT | DRU9 | — |

---

## 12. Risks
| Risk | Effect | Mitigation |
|---|---|---|
| The oracle-ideal share ψ_orc is near or below 0.50 | USED is out of reach even for an ideal reader; PARTIAL is likely | registered now (§4.3): ψ_orc is printed as the comparator, the PARTIAL licence states "as circle-concentrated as an ideal predictor" when it holds, and no threshold moves (owner Q2) |
| The beyond-four effect is small (E[G] ≈ 0.06 nat) | UNDERPOWERED, or the share unresolved | OF-2/OF-4 fail fast; ladder up to 32,768 pairs; SHARE_PRECISION_LIMITED; INC never read as non-use |
| Conditional-sampler defect (e.g. T used for T̃) | non-natural arms; biased estimands | KS-PAIR exact on a non-reversible chain; OF-1 suffix and q4 bitwise checks; OF-5 Lemma P cross-check; H3-U on every split |
| `hwsd-store` appears in an unknown format | REGISTRY_INCOMPLETE; a stop | the reservation and window rule (§8.2); the generic-reader obligation; a pre-freeze erratum route |
| Stage-C records incomplete (no obligation file; reservation left ACTIVE) | registry or lineage failure | U2 reads STAGES.jsonl-bound inventories; the reservation table records stage C's window as ended (§3.1) |
| The decoy plane comes out PARTIAL (RC-4) | a PARTIAL claim not distinguished from a fitted decoy plane | DECOY_PARTIAL(j) qualifier sentence; decoy and Haar shares printed beside every USED/PARTIAL licence |
| The other track's store or dry store appears without a conforming obligation (J3, J4) | REGISTRY_INCOMPLETE; a stop | the closed history format fixed now in `HWS_UD_NAMESPACE.json`; serial generation |
| The model reads beyond-four almost only through the code | KU2 unresolved (no residual response) | registered qualifier DECOY_UNRESOLVED; KU3 still runs |
| The KU1 planted reader has no positive response | the positive control is unavailable | KU1 fitted on KFIT pairs to the oracle's beyond-four change; if unresolved → EXCLUDED_j/KNOWN_CASE for the share (fail closed) |
| y-information in the code | a share that is partly not circle | five nuisance covariates in Γ; SPECIFICITY_NOT_ESTABLISHED registered; ψ_Γ and S\* reported |
| Leakage through known-case or P1 releases | loss of sealing | PASS/FAIL-only releases; P1 uses oracle means only (DRU5, DRU6) |
| Post-freeze correction loops (stage C: 11 J-C1 runs) | budget overrun | repeats budgeted (§10.2); 3× pauses; correction rule X-3 |
| Partial reuse of C2/HWSC functions bound to other studies' constants | silent wrong seeds or models | call allowlist and audit (§11.2); DRU7 |
| Chart support lower on fresh rows | exclusions | SUP ≥ 0.99 per model; 2-of-3 rule |
| Overreading RESPONDS as "the model computes the belief", or NOT_USED as "the circle is useless" | overclaiming | §7.2 wording; §7.3 list |
| Track D and track U both reading `hwsc-store` | interference | both read-only; `lineage_c` at every U job |
| Worktree imports main's `src`; basetemps under the root | wrong code; registry INCOMPLETE elsewhere | `PYTHONPATH`, `-s`; `scratch/test_hwsu-<job>/` |

---

## 13. Owner questions (science and risk only; each with a registered default)
1. **Oracle feasibility first, as its own run.** Run the oracle-only check (§4) as a separate metered stage, with its own approval, before the model part is built? **Default: yes.**
2. **Thresholds.** Keep C2's owner-approved lines unchanged: response 0.30 (with the 0.10 line for LOW/WEAK), share 0.10 and 0.50, and the energy conjuncts. The 0.50 line may lie at or above what an ideal circle reader reaches; OF reports it, and nothing is re-set after OF. **Default: keep, no re-setting.** Alternative: express the share relative to ψ_orc (a new, untested rule).
3. **How many models must agree.** **Default: 2 of 3** for every claim, with all three reported and "all three" stated when it holds (C2 precedent, addendum 21). Alternative: all three, as in stage C.
4. **"Positive but below margin" statements** for both the response (0 < θ < 0.30) and the share (0 < ψ < 0.10). **Default: yes**, never a RESPONDS or USED.
5. **Largest test size.** Allow up to 32,768 pairs (twice C2's largest), chosen only by the blind precision rule. **Default: yes.**
6. **Runs.** None is approved by this plan. Two separate approvals: OF after the design freeze (about 0.5 CPU-h with its tests), then the model part after the execution freeze (about 2.8–4.2 CPU-h more, re-stated from OF and the registry rehearsal). **Default: no run until the owner says so.**
7. **A failing model.** Stop with that outcome and ask; no replacement model, world, recipe, chart or code recipe. **Default: yes.**
8. **(Reviewer's question 1; S3.) The oracle-only check finds that an ideal circle reader would carry less than 20 % of the older-history response.** Stop the whole study, or stop only the "how much runs through the circle" part, while the "does the prediction follow older history" part may still come to you for a run approval? **Default: stop only the circle part** (registered, §4.1).
9. **(Reviewer's question 2; J1.) Stage C's missing final registry record.** It was registered but never written. It is recorded in the mailbox, not written into the finished stage-C store; the new study reads the same files through stage C's existing per-file records. No stage-C verdict is affected. **Decided by the coordinator; reported to the owner for information.**
10. **(Reviewer's question 3; RC-4.) A decoy built from a meaningless hash of the last four symbols also shows a "part" share.** Report a "part" result for the real circle as a finding with the qualifier, or withhold it? **Default: report it with the qualifier sentence** (§5.3).

**(J7)** These defaults stand as registered, with the reviewer's comments applied. The coordinator asks the owner at each run approval, in plain language. The procedural items (J1–J6) are decided by the coordinator under the owner's standing "keep running" instruction.

**Decided by the coordinator (procedural, registered here):**
- the scope names and the seed blocks 6401xx/6499xx;
- the namespace reservation and the window scheduling with track D;
- the mailbox note on stage C's missing obligation and the reservation-table entry that ends stage C's window (§3.1); `hwsc-store` is never written;
- the worktree, branch and ledger file;
- the repeat budget;
- the cap check.

---

## 14. Provenance

| Input | Identity / what was read |
|---|---|
| Request | `ah/planning/requests/coord-hws-use-20261101.md`, sha256 2822c5c5…c9c (verified with `sha256sum` before reading), read in full |
| Rules | `ah/planning/PLANNING_PROTOCOL.md` (full); `tp/CLAUDE.md` (session context) |
| Owner addenda | 25, 26, 28, 34, 35, 36, 37 (full) in `ah/archive/owner-decisions-20261015/` |
| Model-of-depth | `ah/planning/requests/coord-hws-stage-c-20261029.md` was listed but not opened; `ah/planning/responses/HWSC-DESIGN-v1.md` (full) |
| C2 | `C2-FROZEN-v2.md` lines 1–744 (summary, §0–§7 head; §8–§21 not read), `C2-FROZEN-v2.coordinator-addendum-4.md`; outcome `ah/jobs/0115/review.md` |
| C2ND | `C2ND-FROZEN-v1.md` lines 22–436 (summary, §1–§5) and the §-heading list; outcome `ah/jobs/0167/review.md`; CPU lines of `ah/jobs/0163/review-a1.md`, `review-a2.md`, `0166/ACCEPT_REVIEW.md` |
| C2 CPU | `ah/jobs/0107`, `0109`, `0111`–`0114/review.md` (CPU lines only) |
| Stage A | `ah/jobs/0136/review.md` (head); `HWS-FROZEN-v1.md` (grep lines 118–186, 304–306, 549–565, 640–771 for G_K definitions only) |
| Stage C execution | `ah/jobs/0186`–`0196/review.md` (all); `ah/HWSC_CPU_LEDGER.json` (summed); `hwsc-store/stages/S4a/PRODUCTION_FROZEN.json` (full); `stages/S8/RESULT.json` (structure and values printed to depth 2); `registry/{K-REG1, K-REG2, rehearsal/REHEARSAL}.json` (keys `version, status, n_digests, cpu_s, peak_memory_bytes, known_gaps, digest_file_sha256` only); `stages/TRAIN/*/TRAIN_RECORD.json` (key names, `run_key`, `status`, `checkpoint_ids` for steps 0 and 5000 only; `dev_ce` values not read); `OPERATION_ACTIVE.json`, `RUN.lock`, the head of `cpu_ledger.json` (first entry). Hashed (JSON only): FREEZE.json, the three TRAIN_RECORDs, PRODUCTION_FROZEN.json, RESULT.json, VALIDATION_REPORT.json (hashed, not opened), `hwsb-store/HANDOFF.json` (hashed, not opened) |
| Code (main 8f89462) | `tools/c2_readout/{c2_config.py:1-120 and grep lines, c2_model.py:28-160, c2_oracle.py:28-160, 259-343, c2_decide.py:30-160, c2_attrib.py:77-95, c2_code.py:287-307, c2_stats.py:305-330}`, plus `def` lists of c2_attrib, c2_code, c2_model, c2_oracle, c2_stats, c2_decide; `tools/c2_nd/{nd_decoy.py:51-90, nd_decide.py:132-146}`, the `def` lists of nd_decoy, nd_attrib, nd_decide, and `nd_config.py` grep lines; `tools/k4b/{k4b_scores.py:1-80, k4b_charts.py:168-176}` and `def` lists; `tools/x4_circle_history/precision.py:22-105`; `tools/hwsc/{hwsc_registry_build.py:1-171, hwsc_registry.py:282-303, hwsc_gates.py:52-60, hwsc_config.py grep lines}`, the API.md heading list, CONTRACT.json keys `resources`, `seeds`, `masters`, `dry_masters`, and the `def` lists of every hwsc module; `src/topo_pilot/dataset/sampler.py:1-95`; `c1prime/c1_oracle.py` `def` list |
| Code index | `--check`: current at 8f89462. The `files/tools/c2_readout/*.md` pages were consulted (their output was truncated); direct source reads at the cited lines are the authority |
| Searches | whole-token search for 6401xx, 6499xx, 6204xx, 6206xx, `hwsu`, `hwsd` under `tp/tools`, `tp/src`, `tp/tests`: no hits |
| Directory listings (names only) | `root/`, `hwsc-store/`, `hwsc-store/{stages/*, registry, logs}` |
| Arithmetic | desk only (no repository code, no data): ranks, Lemma FW-U count, CPU sums, registry-risk product, store size, P1 sizes |
| **v2 inputs** | review `coord-hws-use-20261101.claude-reviewer.md` (20b010d2…dc4d46), rulings `coord-hws-use-20261101.rulings.md` (1d074b4d…0c7c1f), joint rulings `coord-hws-ud-20261101.joint-rulings.md` (641502e8…f9546f), `ah/records/HWSC_W2_END.json` (2390e29d…c6cb), `ah/records/HWS_UD_NAMESPACE.json` (b4c6d6ff…427b5e). Each was verified with `sha256sum` and read in full. For v2 the writer additionally checked `tp/tools/c2_readout/c2_driver.py:45-52` (`LogitPolicy`: comment at line 49, class at line 50) by `grep -n` and a byte-level line split. No other file was opened for v2. The track-D review and plan, which hold the HWSD review RC-2 text that J2 refers to, were not opened (§ change log, J2) |

**Not read:**
- the public research-summary paths;
- `coord-hws-dyn-20261101*` and any `HWSD-*` file;
- any `payload.npz`, `state.pt`, `sealed/` file, `hist/**` or `HIST_*.npz` array, chart, activation or decoder `.npz`, or checkpoint payload;
- stage-B `REPORT.json`;
- `hwsc-store/stages/S5/VALIDATION_REPORT.json` content;
- `stages/E1/L1.json`;
- any TRAIN_RECORD `dev_ce` value.

**What the writer saw of results.** The stage-C outcome, per-model bounds, control bounds and ratios (RESULT.json, and the request), and the C2 and C2ND outcomes. These shaped the prior expectation (§1.4) and the motivation. No threshold, margin, ladder value, construction constant or seed was set from them; the thresholds are C2's owner-approved values.

**Findings of this plan not in the inputs:**
1. Exact natural suffix-matched pairs through a backward-message conditional prefix sampler (Lemma P0), and the pair identities P1–P3: every pair response is beyond-four by construction, and the code interchange is exactly the interchange of its beyond-four component.
2. Lemma J (E[G] = Jeffreys(q32, q4) ≥ G4), which ties oracle feasibility to stage A's recorded G4.
3. The oracle-ideal share ψ_orc, and the registered statement that the 0.50 line cannot meet rule 1 at 2×.
4. The m4-phase code is not a valid decoy on pairs.
5. Stage C's `REGISTRY_OBLIGATION.json` is missing. (v2, RC-1: the material stale record is `RESERVATION_W2.json`, still ACTIVE; `RUN.lock` and `OPERATION_ACTIVE.json` are lineage-exempt.)
6. Stage C's J-C1 overran its 3× line (6,604 CPU-s over 11 runs); this plan budgets repeats.
7. `c2_stats.p1`/`_summaries`, `c2_model.load_models` and `c2_oracle.load_process` read C2-only constants at call time and must not be called.

---

## Change log v1 → v2

**Base.** v1 `coord-hws-use-20261101.claude.md` (sha256 7ca3bb77…62ca), unchanged. RC texts are the reviewer's replacement or insertion text, applied verbatim (all accepted by the rulings). The J items are applied as the joint rulings state them. The S items are applied as ruled.
- **"Merge"** marks a place where two changes met.
- **"Conforming"** marks a wording change made only to keep the document consistent with an applied item.

| Item | Where applied | Merge / conforming / note |
|---|---|---|
| Header | STATUS line; title HWSU-v2; "Revision v2" paragraph with the input hashes | — |
| RC-1 (MAJOR) | §3.1 preconditions (a) and (b) replaced verbatim; §8.3 U2 Reader and Basis cells replaced verbatim; §12 row replaced verbatim; §13 coordinator bullet replaced verbatim; DRU-REG insertion appended verbatim | **Merge J1/J2:** sub-bullets after (a) and (b) cite the joint ruling and `HWSC_W2_END.json` (its bound hashes, read by the writer) and add the CONTRACT binding and the G0U re-hash; a "(J1 merge)" paragraph in U2 adds the K-REG2 superset check. **Conforming:** the §3.1 precondition header now reads "G0U checks them; `hwsc-store` is never written"; §14 finding 5 annotated |
| RC-2 (MAJOR) | §6 row 11 (M0) replaced verbatim; §11.2 permitted-reads paragraph replaced verbatim (laid out as paragraphs and a list, text unchanged); §2.8 registry-risk parenthesis replaced verbatim; §11.3: `m0` deleted from Attribution column 1 and `registry_risk` from the HWSC row's column 1, mirrors added to column 3 of both rows; never-called list extended verbatim; DRU7 appended verbatim | **Merge J1:** the HWSC row's column 1 also lists `hwsc_data.p_d2a_check` (which §2.8 calls unchanged) and `hwsc_registry.source_own` (used by U2). **Conforming:** §2.6 Haar-frame bullet names `haar_frames_u`; §11.1 rows `hwsu_model` (`m0_u`), `hwsu_records` (`registry_risk_u`), `hwsu_gates` (`haar_frames_u`) |
| RC-3 (MAJOR) | §4.2 OF-0 replaced verbatim; §6 KC0 "OF-0 rules" replaced verbatim; DRO6 appended verbatim | **Merge J3/J5:** a "J3/J5 merge" paragraph in the OF-0 cell: `classify_hits_u` mirrors `hwsc_known.classify_hits_c` (J5 names that function; RC-3 names `hwsb_known.classify_hits`, which the mirror applies); track-D tokens from `HWS_UD_NAMESPACE.json` as declared needles with an exact overlap check; both records bound. §8.1 "Code" gets one sentence (the search prunes with this list; track-D round files are on it). **Conforming:** KC0 also accepts OF_PASS_RESPONSE_ONLY (S3) |
| RC-4 (MAJOR) | §5.3 KU3 PASS / CONTRADICTED / UNRESOLVED cells replaced verbatim; the "KU3 at PARTIAL" paragraph inserted after the table verbatim; DECOY_PARTIAL(j) added to §7.1; §7.2 PARTIAL licence appended verbatim; §5.1 and DRU3 replacements verbatim | **Merge:** one sentence after the inserted paragraph states that a KU3 PARTIAL takes DECOY_PARTIAL, not DECOY_UNRESOLVED (the new UNRESOLVED cell "otherwise" would include PARTIAL). §12 gets a risk row (conforming) |
| RC-5 (MAJOR) | OF-H row inserted after OF-S verbatim; §4.1 paragraph appended verbatim | **Conforming:** the "Pass" line lists OF-H; DRO7 adds a planted-predicate case |
| RC-6 (MINOR) | §10.3 store-size and cap sub-bullets replaced verbatim | — |
| RC-7 (MINOR) | §10.2 rows KC and REG2, the E1 and E2 cumulative columns, Total and "Likely k" replaced verbatim; Summary cost sentence replaced verbatim; §10.4 two phrases replaced verbatim; §13 Q6 replaced verbatim | **Conforming:** the E1 content cell names the S6 check booked inside E1; a "model phase alone" bullet (10,050–14,950, consistent with the Summary); the S3 and S5 notes after the table. Summary, table and §10.4 now agree: 11,850–16,750 CPU-s total, 3.3–4.7 h overall, the model phase 10,050–14,950 (≈ 2.8–4.2 h), OF ≈ 1,800 (≈ 0.5 h) |
| RC-8 (MINOR) | §6 row 12 "On failure" cell replaced verbatim | — |
| RC-9 (MINOR) | §7.3 item 11 added verbatim; §2.6 descriptive bullet added verbatim; §7.2 USED licence sentence appended verbatim | — |
| RC-10 (MINOR) | §4.1 paragraph appended verbatim; OF-B row inserted before OF-0 verbatim; §11.1 Phase column | **Conforming:** `hwsu_bind` moved to phase 1 (OF-B runs the audit); `hwsu_known` split: phase 1 for `seed_search_u`/`classify_hits_u`, phase 2 for the rest; `hwsu_records` lists `FREEZE_OF.json`; "Phase 1 files are frozen by `FREEZE_OF.json`" after the table; DRO7 |
| RC-11 (MINOR) | §8.2 item 1 appended verbatim | **Merge J3:** item 1 now names the record `HWS_UD_NAMESPACE.json` and track D's reserved tokens, and binds both records in G0-OF, KC0 and G0U |
| RC-12 (MINOR) | §6 "Convention" sentence replaced verbatim | — |
| J1 | §3.1 (a) sub-bullet; §8.3 U2 (layout reader, superset check); §8.3 requirements (K-REG1 ⊇ stage C's K-REG2); DRU-REG | The track-D blindness exception for `OBS_INVENTORY.json` concerns track D; for HWSU, `OBS_INVENTORY.json` is read by the U2 reader as RC-1 states |
| J2 | §3.1 (b) sub-bullets (record, CONTRACT binding); §8.2 item 3 (serial generation; `hwsu_records.end_reservation` and its tests); §6 row 0 (W3 attestation); §4.1 order paragraph; DRO7 | **Not verbatim:** J2 says "HWSD review RC-2 text applies to both tracks". That text is in the track-D round, which this writer may not open. J2 was applied from the joint ruling's own description: the record binding, "a reservation named there counts as ended", and each track ending its own reservation with new `end_reservation` code. The tests registered for `end_reservation` are the writer's (§8.2 item 3); the confirmation read should compare them with HWSD RC-2 |
| J3 | §8.2 item 1 (record, track-D tokens, format); §8.2 4(a) (READER_IF_PRESENT, closed classes); §8.3 U4 (scratch globs), U5, U7; OF-0 (declared needles, overlap check, both records bound) | — |
| J4 | §8.2 4(a) (hwsd-dry obligations) and 4(b) (each HWSU dry run writes its obligation); §8.3 new row U2′ (HWSU's own dry and test stores); DRO7; DRU-REG | — |
| J5 | OF-0 merge paragraph; §8.1 "Code" sentence; §11.1 `hwsu_known` row | — |
| J6 | §4.1 "Order (J6)" paragraph (the first-approved track draws first; OF is its own stage with its own freeze and approval; its rows reach track D through `REGISTRY_OBLIGATION_OF.json`) | — |
| J7 | §13 closing paragraph | — |
| J8 (joint rulings addendum 1, sha256 241040fb…c22b; applied after v2's commit 974def7e) | §8.2 item 3 (no edits; the end record at `<store>/reservations/<reservation_id>.END.json` with the listed schema fields; refusals; the W2 attestation rule (a)/(b); the item-5 tests, which replace the v2 test list); §6 row 0 (attestation rule); §4.1 order paragraph (end-record path); DRO7; §11.1 `hwsu_records` row | Items 1–5 are applied as written, laid out as bullets. Three things are mine: (i) the item-5 tests are assigned to author B, because the ruling says "author-A or author-B set" and B owns records; (ii) one sentence says the same rule recognises track D's end records; (iii) J8 item 6 concerns track D's plan only and is not applied here |
| S1 (adopted, descriptive) | §2.6 axial-share bullet with an explicit definition of d_ax and d_circ | The definition of the axial and circular parts of d is the writer's (the review named the split, not a formula) |
| S2 (adopted) | §2.1 "Row order and pairing" sub-bullet | — |
| S3 (adopted) | §4.1 "Failure scope" paragraph; OF-3 and OF-4 failure cells; the "Pass" line (OF_PASS_RESPONSE_ONLY); §7.1 outcome 3; Summary sentence; §10.2 note; §10.4 paragraph 2; §13 Q8; DRO8 | **Writer's extension:** an OF-4 failure on share arrays only is treated like an OF-3 failure (share family dropped), because it asks the same question. Flagged for the confirmation read. §10.4: "If it fails, we stop there" became the two-case wording (conforming) |
| S4 (adopted, report only) | §4.2 OF report bullet (top-1 % share of ΣG, per-pair kurtosis) | — |
| S5 (adopted) | §10.2 "J-U central (S5)" note | — |
| S6 (adopted: cost ≤ 5 %) | §2.6 descriptive bullet; §10.2 E1 content cell | Forecast ≈ 300 CPU-s [W from H] < 5 % of the model-phase central (≥ 502 CPU-s). Booked inside E1's existing central of 2,000 (itemised ≈ 1,990), so RC-7's verbatim figures stand unchanged |
| S7 (adopted) | §8.1 bullet on stage-C values quoted in the plan; §6 row 7: val added to the data, support_VAL computed; §2.10 `LogitPolicy` cite; §10.1 C2 line: S0 66.0 added | **Not verbatim:** the review gives `c2_driver.py:49`. The writer re-checked: line 49 is the section comment and line 50 is `class LogitPolicy:` (`grep -n` and a byte-level line split agree). The cite reads `:49-50` with that note |
| S8 (adopted, report only) | §5.3 "Release" bullet: KU MDEs reported next to the release | — |
| Owner questions | §13 Q8–Q10 added with the ruled defaults; Q6 per RC-7 | — |
| Provenance | §14 "v2 inputs" row | — |

No other text changed. The estimands, lemmas, thresholds, α, ranks, ladder, seeds and decision rules of v1 are unchanged, except where an item above changes them: the KU3 pass rule (RC-4), the OF failure scope (S3), the OF-H and OF-B gates (RC-5, RC-10), the M0 implementation (RC-2) and the X1 failure scopes (RC-8).

---

## Change log HWSU-v2 → HWSU-DESIGN-v1

**Base.** HWSU-v2 (sha256 c51efe50…a750), left unchanged on disk. F texts are the confirmation reader's exact replacement or insertion text (all accepted by `coord-hws-use-20261101.v2confirm.rulings.md`). J9 and J10 are applied as the joint rulings addenda 2 and 3 state them. S-1..S-3 are applied as ruled.

| Item | Where applied | Merge / conforming / note |
|---|---|---|
| Header | STATUS line; title; "Design freeze candidate" paragraph with input hashes | — |
| F-1 (MAJOR) | §4.2 OF-0: "The fragments cover …" replaced verbatim; the merge sentence "Their hits in non-blinded files …" replaced verbatim; DRO6 appended verbatim | **Merge J9:** one sentence after the fragment list: under `/hwsd-store/` only obligation files, `reservations/*.END.json` and reservation files are searched; everything else there is pruned unsearched. F-1 says "only its obligation files are searched"; J9 adds the end records and reservation files. DRO6 also gains the J9 `hwsd-store` fixture |
| F-2 (MAJOR) | §4.1 phase-1 sentence replaced verbatim; §11.1 rows split so each file has one phase (`hwsu_seed.py`, `hwsu_known.py`, `hwsu_driver_of.py`, `hwsu_driver.py`, `hwsu_dry.py`, `hwsu_dry2.py`, the phase-1 and phase-2 document rows); the phase-1 test-location sentence after the table; OF-0 and §8.1 references renamed to `hwsu_seed.seed_search_u` / `hwsu_seed.classify_hits_u` | The line counts of the split files are my estimates (F-2 gives ≈ 100, 280, 150, 300; the dry modules ≈ 330 each). **Conforming:** §4.1 freeze paragraph "the CONTRACT (`CONTRACT_OF.json`, F-2)"; `hwsu_records` gains the J10 obligation writer (≈ 390). The v2 change-log rows that name `hwsu_known.seed_search_u` (RC-3, RC-10, J5) are historical and were left as written |
| F-3 (MINOR) | §2.9 P1 bullet appended verbatim; the "Under OF_PASS_RESPONSE_ONLY" paragraph inserted after the §6 table verbatim | — |
| F-4 (MINOR) | §8.3 U2 superset-check sentence appended verbatim | **Merge S-2:** see S-2 |
| F-5 (MINOR) | §8.3 U2′ test-root clause replaced verbatim | **Merge J10:** the dry-store clause of the same cell cites J10's contents rule |
| F-6 (MINOR) | §2.6 S6 booking sentence replaced verbatim | — |
| F-7 (MINOR) | §8.2 item 3 "W2 attestation": the inspected-files sentence inserted before "(a)" verbatim | — |
| J9 | OF-0 (the J9 sentence on `/hwsd-store/`); DRO6 fixtures; `hwsu_seed.py` row | J9's fragment lists for track U equal F-1's text |
| S-1 | §2.6 axial-share bullet: canonical order, mapped per model by `named_from_canonical` | — |
| S-2 | §8.3 U2 "(S-2)" paragraph; new row U8 (stage C's K-REG2 digest set as a union source); requirements sentence; `hwsu_registry` row | **Not verbatim (a choice the ruling left open):** with U8 a union source, the J1 superset check runs on the reader-built union before U8 is added and becomes a diagnostic. This supersedes J1/RC-1's "else REGISTRY_INCOMPLETE" for that check. A sha256 mismatch of the K-REG2 digest file is still REGISTRY_INCOMPLETE |
| S-3 | §8.2 item 3: `RESERVATION_OF.json` / `RES-HWSU-OF`, `RESERVATION_U.json` / `RES-HWSU-U`, rerun names; the record allowlist | The rerun names follow J10 item 3 |
| J10 | §8.2 item 1 (G0s bind addenda 1–3; J10 governs over the namespace record's rule 3); §8.2 item 3 ("Stopped drawing job"); §8.2 4(a) (the J10 reader: every obligation read, the newest governs, the three classes and closed bases, sha256-only for NON_HISTORY, the INCOMPLETE conditions, aborted dry stores); §8.2 4(b) (one obligation per writing job with J10's names; HWSU's NON_HISTORY name rule; dry stores); §8.3 U2′ and U5; §4.1 order paragraph (OF obligation contents, stopped OF attempt); §6 "Obligations of model-phase jobs"; DRO9; DRU-REG; `hwsu_records` row | **Points of mine, beyond J10's text:** (i) HWSU's NON_HISTORY name rule (prefixes `ACTS_`, `Y_`, `ORACLE_`, `MOMENTS_`, `FIT_`, `DECODER_`, `DECOY_`, `BOOT_`, `SCORES_`, `CERT_`, `PREC_`). HWSU's FWL/GLS fit and projector arrays and the KU head constructions are classed under J10's basis (iii) "decoder" (linear decoders and readouts of activations); J10's closed list does not name fits or projectors explicitly, so this reading is flagged for the coordinator. (ii) A stopped OF attempt's obligation is named `REGISTRY_OBLIGATION_OF-a<k>.json` (J10's `<job>-a<k>` form with the job named OF). (iii) The DRO9 case "an older full obligation and a newer one that omits a file → INCOMPLETE". J10 item 5's own four tests are all included (DRO9; DRU-REG for the E1 stop) |

No other text changed. The estimands, lemmas, thresholds, α, ranks, ladder, seeds and decision rules are those of HWSU-v2, apart from the following:
- N under OF_PASS_RESPONSE_ONLY (F-3);
- the U8 union source and the superset diagnostic (S-2);
- the registry and obligation rules (J9, J10).

### Design-check fixes (D-1..D-3)
Source: `coord-hws-use-20261101.design-check.claude-reviewer.md` (sha256 7e3d73fc…49d3; VERDICT: FIX_REQUIRED). All three fixes were accepted by the coordinator with the reviewer's exact text, and are applied in place. Nothing else changed.

| Item | Where applied | Note |
|---|---|---|
| D-1 (MINOR) | §9 DRU-REG cell: the clause "(J1) the superset check … → INCOMPLETE" replaced verbatim | — |
| D-2 (MINOR) | §4.1: the loader paragraph inserted verbatim after "…add the phase-2 allowlist, tables and resources."; §11.1 `hwsu_config.py` row: "CONTRACT loader" replaced verbatim; DRO1: the loader test added | In DRO1 the reviewer's text is appended to the existing DRO1 bullet as a second sentence, with an initial capital |
| D-3 (MINOR) | §8.2 4(b) name-rule sub-bullet replaced verbatim; DRO9: the write-refusal case added | In DRO9 the case is added as a final list item; the preceding item's full stop became a semicolon to keep the list form |
