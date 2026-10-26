STATUS: MERGED v2, design freeze candidate (pending confirmation)

# X6ZC-MERGED-v2 (supersedes v1; see "Change log v1 → v2" at the end): why do commutative controls respond to the designed order contrasts of X6 stage 1? (no training)

**Round:** `coord-x6zc-placebo-20261026`. **Writer:** merge writer for coordinator Claude 243a611b, 2026-10-26.
**Base text:** track L (`coord-x6zc-placebo-20261026.claude.md`), with track X imports, the comparison's MD-1..MD-9 and the binding coordinator rulings R-X6ZC-1..6 (`….MERGE.md`) applied. Where this file and an input disagree, this file follows the rulings.
**Code base for every citation:** topo-pilot main at **b67f332** (contains the merge 1dc9749 of branch `x6s1-0069`). `git diff 213d1e2 b67f332` over the X6S1 import closure is empty, so every `tools/x6_stage1` line number below is also the line number at the executed commit H‴ = 213d1e2.

Citation key: `pairs` = `tools/x6_stage1/x6s1_pairs.py`, `eval` = `x6s1_eval.py`, `decide` = `x6s1_decide.py`, `data` = `x6s1_data.py`, `stats` = `x6s1_stats.py`, `run` = `x6s1_run.py`, `pre` = `x6s1_stage_pre.py`, `ingest` = `x6s1_ingest.py`, `reg` = `x6s1_registry.py` (all in `tools/x6_stage1/`); `model` = `tools/x6_stage0/x6_model.py`, `exact` = `tools/x6_stage0/x6_exact.py`; `tad` = `tests/x6_stage1/test_a_designed.py`; `lm` = `src/topo_pilot/learner/model.py`. Store paths are relative to `X:/Downloads/projects/topo-pilot/x6-stage1-store/` unless absolute.

---

## Summary

**Question.** X6 stage 1 closed INCONCLUSIVE (rule 9) only because the commutative control ZC-s1 gave β_W2 = 0.209 on the designed W2 contrast (ordD(s1) UNRESOLVED). The stored values show this is not a lone anomaly: on the designed W1 contrast, which has the same order coupling, ZC-s3 gives β_W1 = −0.133 and ZC-s4 −0.218. The study asks why commutative controls respond to the designed order contrasts (W1 and W2), with ZC-s1/W2 as the motivating case, and whether the designed-placebo machinery is fit for reuse.

**Leading mechanistic hypothesis (exact algebra, verified in Stage A).** On W2 and W1, the NA oracle's x-first answer equals the ZC oracle's answer, and the NA oracle's y-first answer equals the ZC answer with one crossing missed. Any order-dependent Z₃ counting error of a Z₃-trained model therefore lies along the NA contrast, although β is exactly 0 for an exactly commutative predictor. The architecture permits such errors: the learner reads ordered tokens with learned positions and nothing enforces commutativity.

**Design.** No training. About 2.8 CPU-h central at the base Stage-C size.
- **A (blind, exact):** record, code and stored-array audits; exact oracle geometry for W1, W2 and their loop-sign variants; known cases; synthetic mechanisms.
- **B (descriptive, opened D):** bit-exact reproduction of all 16 stored designed results, with known cases first; then decompositions, bootstraps and summaries.
- **C (registered, run once):** four loop-sign variants of W2 and of W1 on never-used prefix rows. The NA contrast is the same in every variant, while Z₃ counting errors change sign.

**Outcomes.** STOP_REPLAN, INVALID, DEFECT_FOUND, ESTIMATOR_ARTIFACT/NON_INVARIANT, ZC_NOT_COMMUTATIVE/{ZC_COORDINATE, NA_DIRECTION, NOT_REPLICATED, NOT_NA_DIRECTION (W1)} or UNEXPLAINED/{…}. A Stage-B descriptive tier is reported beside them, and the placebo-reuse verdict has two axes. **None changes X6 stage 1:** INCONCLUSIVE (rule 9), ordD(s1) UNRESOLVED.

---

## 1. Question and scope

**Primary.**
- X6 stage 1 closed INCONCLUSIVE (rule 9) only because ordD(s1) was UNRESOLVED (`jobs/0099/review.md`).
- ordD(s1) was UNRESOLVED because the designed placebo |β_W2(ZC-s1)| ≤ 0.10 failed: β_W2 = 0.20930750050575797 (`decide.ord_d`, lines 107–128; the placebo test is at 116–120, with the bars `sd.PLACEBO` = 1/10 and `sd.RHO_MAX` = 1/4 at `data:97`).
- **Widened by R-X6ZC-2:** why do commutative controls respond to the designed order contrasts W1 and W2? ZC-s1/W2 is the motivating case, and ZC-s3/W1 and ZC-s4/W1 are the other stored responses above the 0.10 bar.
- Which mechanism produced these values?
  - (a) a computation or pairing defect;
  - (b) a trained control that is not commutative in practice;
  - (c) a finite-sample or estimator effect;
  - (d) a property of the designed sets;
  - or another cause found in the code (§3.2).

**Derived.**
- (i) What the stage-1 result means descriptively, within its licence.
- (ii) Whether the designed-placebo machinery (β and ρ bars on init/AB/ZC controls) is fit for reuse, before the owner chooses between "does any order sensitivity exist?" and "is order used at a meaningful size?" (owner addendum 25 item 3). That choice is not asked here.

**Fixed.**
- The registered X6S1 outcome stands: INCONCLUSIVE (rule 9) with CONTROL_LIMITED(designed, s1), CONTROLS_LEARNED, LADDER(parity), DESIGNED_UNRESOLVED(1) and LENGTH_PROFILE. ordD(s1) stays UNRESOLVED. No post-hoc reclassification is possible.
- This study adds a diagnostic finding with its own licence.
- No training. Existing models, data and code only.
- Working rule 2 (learning pilot) does not apply: no training.

## 2. What the opened records already show (descriptive; motivates, decides nothing)

**Source:** the stored `stages/E3w*/<predictor>/designed.json` (written by `eval.designed_stats`, lines 274–304) and `stages/E3z/report.json` (sha256 90be2081…).

| Predictor | β_W2 | ρ_W2 | cos = β/√ρ | per-cue β_W2,y (y = 0, 1, 2) | **β_W1** | R_W2 | natural β_ord |
|---|---|---|---|---|---|---|---|
| **ZC-s1** | **+0.2093** | **0.04594** | **0.977** | 0.205, 0.202, 0.221 | −0.0126 | **0.0766** | 0.0014 |
| ZC-s2 | +0.0011 | 1.6e-4 | 0.08 | 0.008, 0.002, −0.007 | −0.0064 | 0.0939 | 0.001–0.008 (ZC) |
| ZC-s3 | +0.0011 | 2.4e-5 | 0.22 | 0.001, 0.003, −0.001 | **−0.1325** | 0.0905 | ″ |
| ZC-s4 | −0.0054 | 1.7e-4 | −0.41 | −0.001, −0.006, −0.009 | **−0.2184** | 0.0945 | ″ |
| AB-s1 | +0.0028 | 1.1e-3 | 0.08 | 0.023, −0.016, 0.002 | −0.0013 | 0.2042 | 0.001–0.004 (AB) |
| AB-s2 | −0.0001 | 3.9e-5 | −0.02 | 0.004, −0.004, 0.000 | −0.0007 | 0.1980 | ″ |
| AB-s3 | +0.0009 | 7.0e-5 | 0.11 | −0.002, 0.005, −0.001 | −0.0114 | 0.1987 | ″ |
| AB-s4 | −0.0023 | 2.0e-3 | −0.05 | 0.023, −0.029, 0.000 | +0.0004 | 0.2107 | ″ |
| NA-s1 | 0.0883 | 0.02186 | 0.60 | 0.251, 0.013, 0.001 | 0.1031 | 0.0797 | 0.047 |
| NA-s2 | 0.0179 | 0.00113 | 0.53 | 0.031, 0.013, 0.010 | 0.2697 | 0.0874 | 0.090 |
| NA-s3 | 0.0743 | 0.01993 | 0.53 | 0.180, −0.071, 0.113 | 0.2963 | 0.0859 | 0.072 |
| NA-s4 | 0.0197 | 0.00093 | 0.65 | 0.041, −0.003, 0.021 | 0.0753 | 0.0853 | 0.049 |
| init-s1..s4 | ≈ −1e-5 | ≤ 1e-5 | — | ≈ 0 | ≈ +1e-5 | 1.19–1.26 | ≈ 0 |

**Observations.**
- **The cosine.** Over the same 3,090 pairs, β_W2 = Σ⟨Δp̂_c, Δq*_c⟩ / Σ‖Δq*_c‖² and ρ_W2 = mean‖Δp̂_c‖² / mean‖Δq*_c‖² (`eval:281–294`). By Cauchy–Schwarz |β| ≤ √ρ, so β/√ρ is an aggregate cosine. Equivalently, β²/ρ is an alignment-energy share (ZC-s1: 0.954).
- **ZC-s1 on W2.** It has the largest W2 order response of all 16 predictors (√ρ_W2 = 0.214). It is more closely aligned with the NA contrast than any NA model, and nearly uniform across cues. ρ_C(ZC-s1) = 0.0078 is also the highest of the 16 (NA-s1 0.0058).
- **W1 (added by R-X6ZC-2).**
  - Three of the four ZC seeds exceed |β| = 0.10 on one of the two order contrasts: s1 on W2 (+), s3 and s4 on W1 (−).
  - The sign varies by seed and by geometry.
  - AB seeds give |β_W1| ≤ 0.012. NA seeds give 0.075–0.296.
- **Against a pure NA-leak reading.** An NA leak, p = (1−w)·q*_ZC + w·q*_NA, predicts β = w on every NA contrast, so β_W1 = β_W2 for each model. ZC-s1 (−0.013 vs +0.209), ZC-s3 (−0.133 vs +0.001) and ZC-s4 (−0.218 vs −0.005) all contradict it, descriptively.
- **AB per-cue pattern.** AB-s1 and AB-s4 show per-cue β_W2 of roughly (+, −, 0) with a pooled value near 0. This is the cancellation pattern predicted in §3.1.
- **Natural pairs.** ZC-s1 is ordinary there:
  - natural β_ord = 0.0014;
  - own-process within-Parikh-class spread ratio 0.073 (ZC seeds 0.072–0.077, spread 0.062–0.066; AB ratio 0.019–0.036; `E3z/report.json` `abelian_spread`);
  - LOSS-ECHO max |Δ| ≤ 4.8e-7;
  - LEARN-TEST PASS.
  Every AB/ZC model therefore already shows non-zero within-class spread: no trained control is exactly commutative.
- **The bars are on different scales.** For perfectly aligned errors β = √ρ, so the β bar 0.10 acts as a ρ bar of 0.01, against RHO_MAX = 0.25 (`data:97`, `decide:118–119`). ZC-s1 failed β with ρ_W2 = 0.046, which passes the ρ bar.

## 3. Geometry and competing explanations

### 3.1 The geometry from the frozen code (exact; verified in Stage A as K0)

**Established premise (track X, verified).** AB and ZC are commutative data-generating processes, but their learners are not constrained to be commutative:
- the model reads BOS plus the raw ordered tokens (`eval:57–60`);
- it uses learned positional embeddings (`lm:70`; `pos_emb` at `lm:90`; `x = tok_emb + pos_emb` at `lm:116`);
- one `MODEL_CFG` serves every arm (`data:83`).
Oracle commutativity therefore does not imply learned commutativity. The question is why the learned errors align with the NA contrast.

**Labels and holonomy.**
- `model:57–58` sets S3_A = (1,0,2) = a, S3_B = (0,2,1) = b and S3_C = (1,2,0) = c; c² = (2,0,1).
- `compose(g, h)[x] = g[h[x]]` (`model:62–63`).
- `_SEAM` (`model:99–100`) gives NA = (a, b), AB = (a, a) and ZC = (c, c) for the (x, y) seams. `seam_labels` (`model:103–107`) gives x± and y± their labels, with the inverse for the minus direction. Since a = a⁻¹ and b = b⁻¹, NA and AB ignore the sign of a crossing, while ZC maps x−, y− to c⁻¹ = c².
- `seam_letter` (`model:88–94`): an x crossing is the step between x = 3 and x = 0 on a fixed y ("x+" from x = 3), and a y crossing likewise.
- `holonomy` (`model:186–190`) left-composes each crossing label in path order.
- ANCHOR = 10, and its neighbours are {6, 9, 11, 14}.

**The readout.**
- `closed_form` (`model:261–284`) gives cue law (1−λ_{n+1})/3 + λ_{n+1}·δ_{ρ(y)}, with one η step after the n path steps (`model:273–277`) and λ_m = (49/50)^m (`model:242–247`).
- W2 readout: t = L + 18, n = 17, λ₁₈ = 0.6951353.
- W1 readout: t = L + 8, n = 7, λ₈ = 0.8507630.

**The two designed order families.**
- **W2** (`pairs:200–202`, `pairs:216–219`): prefix + cue(y) + path (9, 5) + loop₁ + loop₂ + `_S7` (`pairs:36`). The loops are A⁺ = (9, 13, 1, 5) and B⁺ = (6, 7, 4, 5) (`exact:89`). A⁺ crosses x+ (13→1) and B⁺ crosses y+ (7→4). Member a = A⁺B⁺ (`W2_LETTERS[0]`, `pairs:33`) and member b = B⁺A⁺. Bag-, bigram-, κ- and last-8-matched (`tad:122–144`).
- **W1** (`exact:98–99`, `pairs:205–207`, `pairs:220–222`): path (14, 15, 3 | 12, 0, 4, 5, 6). Member a = U crosses x+ (15→3) and then y+ (3→0). Member b = D crosses y+ (15→12) and then x+ (12→0). Matched on length, n, end, prefix, cue, Parikh, H1, counts and parity (`exact._EQUAL_ROWS`). **Not bag-matched:** the members visit 3 vs 12 (`exact:282` `_BAGGED["W1"] = False`; last 4 tokens shared, `exact:281`).

**The answers (x-first member a, y-first member b).**

| Arm | Member a (x then y) | Member b (y then x) |
|---|---|---|
| NA | b∘a = c² → answer c²·y | a∘b = c → answer c·y |
| ZC | c∘c = c² → c²·y (= NA's a-answer) | c²·y; **one crossing missed: c·y (= NA's b-answer)** |
| AB | a∘a = e → y (neither NA answer) | y |

The same table holds for W1 and W2.

**The coupling.**
- In the cue-difference plane, Δq*_NA,c = λ(δ_{c²y} − δ_{cy}) on every pair, and den_i = ‖Δq*_c‖² = 2λ² (W2: 0.966427; W1: 1.447595). β is therefore a mean of pair terms, with no ratio-estimator bias.
- For a ZC-trained predictor, an error that moves mass between "ZC answer" and "one crossing missed" lies exactly along the NA contrast. A pure change of confidence in the ZC answer has cosine √3/2 = 0.866 with it.
- **Why AB cancels.** An AB "missed crossing" moves mass to a·y. That is NA's b-answer for y = 0, NA's a-answer for y = 1 and neither for y = 2, so per-cue values have opposite signs and cancel in the pool (per-cue projections (−½, +½, 0)·(π_a − π_b), since a·2 = 2; the h_last pattern (½, −1, ½) is a different known case; `exact:285–287`, `tad:170–189`).

**The loop-sign variants (new histories; checked by K0).** In each variant, member a is the x-first ordering.

| Variant | W2 member a / b | W1 member a / b (path after the cue) | NA answer a / b | ZC answer | ZC, one crossing missed | Coupling to the NA contrast |
|---|---|---|---|---|---|---|
| PP | A⁺B⁺ / B⁺A⁺ (= W2) | (14,15,3,0,4,5,6) / (14,15,12,0,4,5,6) (= W1) | c²y / cy | c²y (= NA a) | cy | ZC answer on the a side |
| MM | A⁻B⁻ / B⁻A⁻ | (6,5,4,0,12,15,14) / (6,5,4,0,3,15,14) | c²y / cy | cy (= NA b) | c²y | **mirror of PP:** ZC errors flip sign |
| PM | A⁺B⁻ / B⁻A⁺ | (14,13,12,0,3,7,6) / (14,13,12,15,3,7,6) | c²y / cy | y | first loop missed: c²y in a, cy in b | ZC answer uncoupled; missed-crossing errors coupled |
| MP | A⁻B⁺ / B⁺A⁻ | (6,7,3,15,12,13,14) / (6,7,3,0,12,13,14) | c²y / cy | y | first loop missed: cy in a, c²y in b | opposite of PM |

- **W2 variants.** A⁻ = (1, 13, 9, 5) crosses x− (1→13), and B⁻ = (4, 7, 6, 5) crosses y− (4→7) (`exact:89`). Each loop is a closed cycle from vertex 5, so swapping loops preserves the token bag, the directed bigrams, κ, t and the last 8 symbols (5, 1, 2, 3, 7, 11, 15, 14).
- **W1 variants.**
  - MM is the reversal of the W1 paths. PM uses the corner (3,0)→{(0,0) | (3,3)}→(0,3), and MP is its reversal.
  - Every W1 variant starts and ends at an anchor neighbour (6 or 14) with n = 7.
  - Within each pair, the variants are matched like W1: the `exact._EQUAL_ROWS` set, with bags differing by one visited vertex.
  - These paths are the writer's construction (OPEN-5, closed: the paths stand; the result-blind reviewer verified all eight). K0 verifies them exactly before any model runs.
  - The W1 variants differ from W1 in where the crossings and the differing vertex sit: tails 4/2/3/3 tokens and crossing steps 3–4/5–6/4–5/4–5 (PP/MM/PM/MP); no n = 7 adjacent-corner MM path keeps a 4-token tail. On W1 only a sign reversal is diagnostic; ratio sizes are not interpreted.
- **The NA contrast is identical** in all four variants of a family (a = a⁻¹, b = b⁻¹), with the same λ.

**Closed-form predictions (exact; checked in K3).** All are cue-normalised, with s_v = +1 for PP, −1 for MM and 0 for PM and MP. λ = λ₁₈ for W2 and λ₈ for W1.
- **M0, NA leak** (p = (1−w)·q*_ZC + w·q*_NA): β_v = w for every v and both families, so r_v := β_v/β_PP = 1, and β_W1 = β_W2.
- **M1, confidence asymmetry.** With κ the point-law excess (p_c = (1−κ)/3 + κ·δ_z on the ZC answer z, with κ_a ≠ κ_b): β_v = s_v·(κ_a − κ_b)/(2λ). That is 0.7193·s_v·(κ_a − κ_b) on W2 and 0.5877 on W1. So r_MM = −1 and r_PM = r_MP = 0.
  - *Reading κ instead as "ZC-answer mass κ, rest uniform"* changes the coefficient to 0.75/λ (1.0789 on W2, 0.8816 on W1). The r_v values are unchanged.
- **M2, order-asymmetric missed crossing** (rate π_a vs π_b, the same for ± loops):
  - β_PP = π_b − π_a and β_MM = −β_PP;
  - if the first loop is missed, β_PM = (π_a + π_b)/2 = −β_MP; if the second, the signs swap.
- **The key fact.** Every sign-symmetric Z₃ counting error gives r_MM = −1 and opposite-signed r_PM and r_MP. An NA-direction response gives r_v = 1 for every v.

### 3.2 The explanations and how each is told apart

| # | Explanation | Discriminating observation (where) |
|---|---|---|
| (a1) | **Pairing or orientation defect**: a/b swapped or mismatched between p̂ and q*, wrong prefix, y or family (X: E1) | A2 code audit: `designed_set` builds a = `W2_LETTERS[0]` = A⁺B⁺ (`pairs:216–219`); `designed_stats` uses the same a/b for p̂ and q* (`eval:281–282`). A-audit: pairs rebuilt from stored-array content. K2: q*_NA → β = 1. K5: independent recomputation and joint swap invariance. |
| (a2) | **Wrong oracle for controls** (q*_arm instead of q*_NA) | A2: `eval_chunk` passes `qstar("NA", …)` for every predictor (`eval:455`). With q*_ZC the denominator would be 0 and β NaN, but the stored β is finite. |
| (a3) | **Readout-index, BOS, padding or cue-normalisation defect** (X: E2) | A2: `ModelPredictor._run` (`eval:105–114`), `model_inputs` (`eval:57–60`), `cue_normalise` (`eval:205–211`). K5: padding, batch, two-load, scalar-vs-vector t, permutation, independent BOS/readout extraction, readout-index cue mass. |
| (a4) | **Wrong checkpoint or wrong D evaluated** (X: E9 part) | A1: the admitted lock `cloud/ADMITTED/ZC-s1.json` (final file 9f498d48…, weights 96307d7c…) is what `ModelPredictor` verifies (`eval:70–78`); D's `designed_sha256` b4eeff59… equals the E0 record's. K4: bit-exact reproduction. |
| (a5) | **Non-determinism or environment** | K4 in the recorded environment (`chunk.json` `env_local`: torch 2.14.1+cpu, numpy 2.2.6, threads 2/1, batch 1,024, commit 213d1e2). |
| (b1) | **ZC-s1 trained on order-bearing data** (wrong pool, NA tokens; X: E9) | A1: DATA-ID PASS; LOSS-ECHO ≤ 4.8e-7 on its own ZC pool; LEARN-TEST PASS; natural β_ord 0.0014. M0 predicts β_W1 = β_W2 (already contradicted, §2) and r_v = 1 in Stage C. |
| (b2) | **A learned order-dependent Z₃ counting error** (for example, a crossing missed more often in one order). This is the **leading candidate**, and it is consistent with seed- and geometry-specific signs (§3.3). | B4: ZC-coordinate profile and per-member own-arm regret. Stage C: r_MM ≈ −1, with opposite signs on PM and MP. |
| (b3) | **Seed-shared inductive bias**: ZC-s1, NA-s1, AB-s1 and init-s1 share init and batch order (`run_key` → (`"x6s1"`, s), `data:168–177`) | B6: cosine of ZC-s1's per-pair Δp̂ with NA-s1's against NA-s2..s4. Evidence against already: AB-s1 shares the seed and does not respond, and ZC-s3/s4 respond on W1 without sharing seed 1. |
| (b4) | **Cloud or session artefact**: ZC-s1 was the only control in wave C1 (bundle C1-97a8b8950072, with NA-s1 and NA-s2); the other controls are in C2-7a03d762d0a8 | A1: manifests, devices, sessions, CLOUD-PROV PASS. Recorded only; this cannot by itself create NA alignment. |
| (b5) | **Token-identity effect on W1** (new): the W1 members differ in one visited vertex, so an order-free, bag-dependent error can respond | Applies to W1 only (W2 is bag- and bigram-matched). It cannot explain ZC-s1/W2. Stage C on W1 cannot separate it from (b2); the W1 licences say so. |
| (c1) | **Finite prefix sample**: 1,030 prefixes, a census with no interval in X6S1 (X: E6) | B5 prefix-cluster bootstrap; D3 summaries; Stage C replication on unused prefixes. Note (X): for an exactly invariant predictor u_i = 0 on every pair, so sampling alone cannot create β ≠ 0. |
| (c2) | **Single geometry**: one loop configuration repeated over 3,090 pairs | Stage C sign variants (new geometries). |
| (c3) | **Ratio-estimator bias** | None: den_i = 2λ² on every pair (K0). |
| (d1) | **Non-invariance of the estimator for exactly commutative predictors** | K1: exact zero for every exactly commutative predictor. |
| (d2) | **Anisotropic coupling** (§3.1): the NA contrast lies in the span of Z₃ counting errors; AB errors cancel over y | K0 coupling table (exact); K3 synthetic mechanisms; B3 decomposition. |
| (d3) | **Designed construction fails its matching claims** (X: E4) | K0 on the constructions; A-audit on the stored arrays. |
| (e1) | **The β and ρ bars on different scales** (§2) | Reported in the reuse verdict. Not a cause; it explains why ρ passed while β failed. |
| (e2) | **R_W2 for controls measured against q*_NA**: ZC-s1's 0.0766 is the lowest of the 16 because of the answer coincidence | B4: per-member own-arm regret against q*_ZC. A consequence, not a cause. |
| (e3) | **Readout amplification by cue normalisation** (X: E5) | D2 decomposition and β_fixed, READOUT_AMPLIFIED qualifier. Equal predictions stay invariant regardless. |

Several explanations can coexist. The report separates the **proximate explanation** of β (what in the predictions produces it) from the **origin** of the learned function (why training produced it). The origin stays unresolved without training (ORIGIN_UNRESOLVED; §11).

### 3.3 What the W1/W2 sign and seed pattern already says (descriptive)
- **M0 (NA leak)** predicts the same sign and size on W1 and W2 for each model. It is contradicted for s1, s3 and s4.
- **Z₃ counting errors (b2)** allow any sign and size per geometry. W1 and W2 differ in crossing adjacency (adjacent corner crossings vs crossings separated by loops) and in readout age (n = 7 vs 17). This is consistent with the observed pattern.
- **Token-identity effects (b5)** are consistent with W1-only responses (s3, s4). They cannot produce ZC-s1/W2.
- **A pipeline defect (a1–a3)** would be expected to act on every predictor, or on the q* references. K2 and K5 test this directly.

These are descriptive readings of opened data. They motivate the registered Stage-C cells (§8) and settle nothing.

## 4. Data status, exposure and inputs

### 4.1 Already opened (used by a model evaluation or a decision in X6S1)
- test_NA, test_AB and test_ZC with partners (E3);
- val_NA and val_ZC;
- the 12 dev pools, the gate pools and the train pools;
- the six stage-0 prefixes and the first 1,024 yielding rows of the `prefix` pool;
- the whole designed set D (W2, C1–C4, W1, W3, W3′; `tables/designed.npz`) and every stored E3 output.

**What opened data allow.** Reproduction, known-case checks whose answers are exact identities (they hold on any history), and descriptive exploration. **No confirmatory claim.**

### 4.2 Unused, reserved for the registered check (track X's "no unused reserve" claim is dropped, MD-3)
- **The prefix rows after r\*.**
  - The `prefix` pool is ObservationSet 54371c403e588227 (4,096 rows, token sha256 2b7a6e60…, stream (`"x6s1"`, `"prefix"`), `data:180–197`).
  - r\* is the row that produced the 1,024th natural prefix.
  - The only model-facing consumer is `designed_set → natural_prefixes` (`pairs:186–193`, `pairs:210–213`, called at `pre:220`). It draws one L_max per row from (`"x6s1"`, `"prefix_len"`) under DATA_MASTER and keeps the first 1,024 yields only.
  - The pool is excluded from every cloud bundle (`ingest:38` `_FORBID` contains "prefix"), so no training saw it.
- **Prior code reads, recorded as exposure entry `E0-PREFIX-READ`** (the first line of `x6zc-store/EXPOSURE.jsonl`):
  - at E0, G0-ORC scanned all 4,096 rows to draw L_max and kept the first 1,024 yields (`pre:220`);
  - REG hashed row digests for the separation check (`reg:437–460`, `gsp_train_dev`);
  - the pool build recorded the token sha256.
  - No model was evaluated on any row, and no decision used rows after r\*. A1 item 5 confirms this by code search and by the `EVALUATIONS.jsonl` kinds.
- **The variant histories.** MM, PM and MP on fresh prefixes, for both families, are new token strings that no model or person has evaluated.
- **Correction to track L.** Short prefixes repeat by value, so some fresh prefix token strings will equal prefixes in D, and PP histories on those prefixes coincide with opened W2/W1 histories.
  - This does not compromise the registered check: the fresh rows are draws from the registered stream, independent of every X6S1 result, and every rule is frozen before any fresh-set model output exists.
  - **Policy, fixed now.** The number of fresh prefixes whose token string occurs among D's 1,030 prefixes is counted and reported. A sensitivity line recomputes the Stage-C decision without them. The registered decision uses all fresh prefixes.
- **Expected N_avail** (blind count in A3) is roughly 2,000–2,400. It depends on the yield rate of the prefix rule, about 0.75–0.85 per row.

### 4.3 Separation of exploration from the registered check
- **Stage A is blind.** It uses records, code, stored designed arrays, and oracle/analytic/synthetic predictors only. It is the only stage that touches the fresh variant set, and only through oracles.
- **Stage B is descriptive:** models on the opened D only.
- **No model is evaluated on any fresh history before Stage C.** No model is evaluated on any variant history built on one of D's 1,030 prefix rows, ever (fresh rows equal by value to a D prefix: §4.2).
- **Stage C is registered and runs once.** All its rules, including the W1 cells, are frozen in this plan before Stage B runs (R-X6ZC-2).
- **Only frozen-rule sizing crosses from B to C:** G1 uses the bootstrap variance of the focal cells on opened D, a blind quantity under addendum 26 item 3.

### 4.4 Input artefacts (R-X6ZC-4)
**None of these lies under `sealed/`. None is a payload opened or hashed at planning time.**
- At planning time only JSON reports and metadata were read: the 16 `designed.json`, `E3z/report.json`, `E3w5/ZC-s1/chunk.json`, `cloud/ADMITTED/*.json`, `pools/POOLS.json`, `stages/E0/record.json`, `EVALUATIONS.jsonl` and `STAGES.jsonl` (see §19).
- "Payload" below means a file whose content is read only during the authorised run, as the study's own data use, and logged in `x6zc-store/EXPOSURE.jsonl`.

| # | Artefact | Path (store-relative) | Identity (sha256 prefix; full value in the cited record) | Kind | Used in |
|---|---|---|---|---|---|
| 1 | Designed set D | `tables/designed.npz` | file 04cde023…; `designed_sha256` b4eeff59… (`stages/E0/record.json` `designed`) | payload | A-audit, K0–K2, B |
| 2 | Log/score tables | `tables/log_tables.npz` | file 19616eaa… (`stages/E0/record.json` SCORE `tables.file_sha256`) | payload | B1 (R_W2, Δ_W3), B4 |
| 3 | Prefix pool | `pools/ObservationSet/54371c403e588227/` (`payload.npz`, `meta.json`, `extra.json`) via `pre.load_obs(store, "prefix")` (`pre:67–72`, digest re-checked) | token 2b7a6e60… (`pools/POOLS.json`) | payload | A3, K0, Stage C |
| 4 | Train pools (exposure check A4 only) | `pools/npy/train_{NA_s1, NA_s2, NA_s3, NA_s4, ZC_s1, ZC_s3, ZC_s4}.npy` | files cfa6cb0e…, a8718eb5…, b60c5d5b…, 8fec6f24…, 3859c861…, e6db371f…, 0529a3f5… (`POOLS.json`) | payload | A4 |
| 5 | Admitted final checkpoints (12) | `cloud/C1/{NA-s1, NA-s2, ZC-s1}/ckpt/030000.pt`; `cloud/C2/{NA-s3, NA-s4, AB-s1..s4, ZC-s2..s4}/ckpt/030000.pt` | final file/weights per `cloud/ADMITTED/<model>.json` (e.g. ZC-s1 9f498d48…/96307d7c…; ZC-s3 8e5fbb27…/040426c9…; ZC-s4 6a1cbb19…/9c578ea8…). A1 confirms each path against the lock. | payload | B1–B10, C |
| 6 | Init states (4) | `stages/E0/init/init_s{1..4}.pt` | digests in `stages/E0/record.json` (CLOUD-PREP `inits`) | payload | B1, C |
| 7 | ZC-s1 chain (B8 only, optional) | `cloud/C1/ZC-s1/ckpt/{001000, 003000, 010000, 020000}.pt` with `cloud/C1/ZC-s1/rec/*.json` | `chain_record_sha256` in `cloud/ADMITTED/ZC-s1.json` | payload | B8 |
| 8 | Admission locks | `cloud/ADMITTED/*.json` | — | JSON (opened) | A1, B1 |
| 9 | Stored designed results (16) | `stages/E3w1/init-s{1,2,3}/`, `stages/E3w2/{init-s4, NA-s1, NA-s2}/`, `stages/E3w3/{AB-s1, NA-s3, NA-s4}/`, `stages/E3w4/AB-s{2,3,4}/`, `stages/E3w5/ZC-s{1,2,3}/`, `stages/E3w6/ZC-s4/` (`designed.json`, `chunk.json`, `float32.json`). The init-s1 copies under `stages/E3r2/` and `stages/E3r5/` hold identical designed values; A1 names the one E3z consumed. | file sha in `chunk.json` `files` | JSON (opened) | A1, B1 |
| 10 | Outcome report | `stages/E3z/report.json` | 90be2081… (`jobs/0099/review.md`) | JSON (opened) | A1 |
| 11 | Store records | `FREEZE.json`, `AUTH.json`, `GATES.jsonl`, `STAGES.jsonl`, `EVALUATIONS.jsonl`, `pools/POOLS.json`, `stages/E0/record.json`, `stages/E3w2/record.json`, `stages/E3w5/record.json` | — | JSON (opened) | A1 |
| 12 | Code | topo-pilot ≥ 1dc9749; `tools/x6_stage1` ≡ 213d1e2 | git | code | all |

- **Not used:** anything under `sealed/` (it holds `headroom.json`, `learn.json`, `learning_curve.json`, `learning_curve_C2.json` and `zc_s1.json`, whose names alone were seen by directory listing). Also unused: `registry/`, `superseded/`, the test, val, dev and gate pools, the partner files, and `tables/class_tables_NA.json` (q_stat rebuilds class tables in memory, `data:272–280`).
- **Exposure check A4, restricted (MD-7).** It uses the train pools of the registered-cell models (ZC-s1, ZC-s3, ZC-s4) plus the four NA pools for the positive control: 7 pools, not 12. The AB and ZC-s2 models enter only K6 and descriptive lines, so their pools are not read.

## 5. Common rules

**Environment.**
- The recorded E3 environment: CPU, float64 cast, 2 intra-op and 1 inter-op threads (`eval.set_threads`, `eval:42–47`), batch 1,024 (`data:106`), at most 3 children (`MAX_CHILDREN`).
- Every stage records `run.env_local()` (`run:231–242`) and diffs it against the E3w5 ZC-s1 `chunk.json` with `run.env_changed` (`run:243–245`). A commit-only difference is expected and is not ENV_DRIFT.

**Streams and bootstrap.**
- X6ZC_MASTER = 2026102670 (OPEN-3 ruling; freshness checked before freeze). Its freshness is checked against every store's seed maps with `run._seed_maps` (`run:127–138`), applying the `seed_fresh` test (`run:118–126`) to this value.
- Streams: `SeedTree(X6ZC_MASTER).generator("x6zc", "boot", "B")` for Stage B and `("x6zc", "boot", "C")` for Stage C.
- 5,000 resamples per bootstrap (GAP_CLOSING §2 rule 4).
- **Paired prefix-cluster bootstrap.** The cluster is a prefix: all its cues, members, families (W1 and W2) and variants are resampled together. Draws use `gen.integers(0, P, size=P)`, the `stats.boot_beta` rule (`stats:151–157`). The same indices are used for every predictor, family and variant in a draw. Intervals come from `stats.quantile` (`stats:140–141`, linear).

**Numerical rules** (track X's table merged with L's tiers; MD-5). Tolerances are never relaxed after a discrepancy is seen.

| Check | Requirement |
|---|---|
| Token, key, manifest, checkpoint and table identities | Exact equality |
| Rational known cases (K0, K3, Fractions) | Exact |
| Float β of an exactly commutative predictor (K1) | `== 0.0` exactly, and `beta_exact == 0` |
| Float β of an exact reference vs its exact target (K2, K3 float path) | ≤ 1e-12 absolute |
| Independent recomputation vs production (K5a) | ≤ 1e-12 absolute; (1e-12, 1e-9] → NUMERIC_DRIFT flag; > 1e-9 → DEFECT_CANDIDATE |
| Same-environment repeated float64 predictions (two loads, batch) | ≤ 1e-12 max-abs; padding ≤ 1e-13 |
| Reproduction of stored designed values (K4) | Bit-exact → PASS; ≤ 1e-9 relative → ENV_DRIFT (flag, record the env diff, proceed with the new values as the Stage-B basis); > 1e-9 relative → DEFECT_CANDIDATE (investigate); IRREPRODUCIBLE only if no cause is found |
| Paired non-invariance (descriptive tier) | Cue-normalised pair difference > 1e-9 on at least one verified pair |
| Placebo boundary for descriptive qualifiers | 0.10, with a 1e-9 band: "crosses 0.10" means the two values lie on opposite sides outside [0.10 − 1e-9, 0.10 + 1e-9] |
| Descriptive material change | |Δβ| ≥ 0.05 |
| Registered Stage-C comparisons (§9) | Strict as written, on float64 statistics |

## 6. Stage A: blind (records, code, stored arrays, exact oracles, analytic and synthetic predictors)

No model output on any history in this stage.

**A1, records audit** (zero CPU). Every item must hold.
1. `E3z/report.json` placebo.designed for ZC-s1 equals its `designed.json`, key by key; likewise for ZC-s3 and ZC-s4 (β_W1).
2. `decide.ord_d` (`decide:107–128`) on the stored designed dicts returns UNRESOLVED with control_limited and reason "designed placebo ZC" for s = 1, and FAIL for s = 2–4.
3. **Provenance of ZC-s1, ZC-s3 and ZC-s4:**
   - the admitted locks;
   - WEIGHTS-HASH, CLOUD-PROV, DATA-ID and TRAIN-COMPLETE PASS in `GATES.jsonl`;
   - each ticket's data stream (`"x6s1"`, `"train"`, `"ZC"`, s), with data and token sha equal to `POOLS.json` `train_ZC_s<s>`;
   - LOSS-ECHO max_abs_32 ≤ 5e-7; LEARN-TEST PASS;
   - devices and sessions listed.
4. Each focal checkpoint path resolves to the admitted final file and weights sha (the `ModelPredictor` checks, `eval:70–78`; `ingest.verify_admitted`, `ingest:441–452`). D's `designed_sha256` equals the E0 record's.
5. No X6S1 code path or `EVALUATIONS.jsonl` entry uses prefix-pool rows beyond the 1,024 yields. The E0 reads of §4.2 are recorded as `E0-PREFIX-READ`.
6. **Code base (R-X6ZC-1).** `git diff 213d1e2 <X6ZC commit> -- src tools/x6_stage1 tools/x6_stage0 tools/d2a tools/x4_oracle_profile tools/k4b tools/c1prime_registry tests/oracle_profile` is empty. This is the import closure of `eval` (`sys.path` additions `eval:22`, plus `src`). It holds at b67f332; the X6ZC branch starts at 1dc9749 or later.

Any failure → DEFECT_CANDIDATE (§9, rule G-R2 or G-R2′).

**A2, code audit** (zero CPU, a written table).
- For every item in (a1)–(a3) of §3.2, plus `_fam` (`eval:238–246`), `pair_terms` (`eval:214–217`), `beta_fsum` (`eval:220–222`) and `cue_mass` (`eval:201–202`): cite file and lines and state the expected behaviour.
- **Input-path audit (X's D4; establishes the premise E8):**
  - ordered raw tokens with BOS (`eval:57–60`);
  - learned positions (`lm:90`, `lm:116`);
  - the next-token objective over all positions;
  - no commutativity constraint or augmentation in the training recipe;
  - no oracle or latent labels in the learner input;
  - arm and seed identities agreeing with the admission records.
- A discrepancy between code and protocol §2.5 → DEFECT_CANDIDATE.

**A-audit, per-pair audit of the stored arrays** (X §7 Stage A; reads `tables/designed.npz`).
- For every W2 and W1 pair (3,090 each) and every control pair, identities are reconstructed from **history content**, never from row position.
- **Both families:** both histories legal (`model.parse`); stored t equals the unpadded length; same prefix before the cue; same cue and cue position; same n, end vertex and directed seam-crossing counts; the a member crosses x first.
- **W2 only:** the same token bag, directed-bigram bag and last 8 tokens.
- **W1 only:** the last 4 tokens are equal, and the bags differ in exactly one vertex (3 vs 12).
- All three cues are present for each prefix entry. Counts and multiplicities equal the frozen construction: 1,030 prefixes (`pre:341`).
- **Failure** → DEFECT_CANDIDATE, keeping the smallest counterexample.

**A3, fresh prefixes** (blind; reads the prefix pool).
1. Rebuild the yield list with the `natural_prefixes` rule over all 4,096 rows, drawing one `integers(1, 15)` per row from a fresh (`"x6s1"`, `"prefix_len"`) generator under DATA_MASTER and recording row indices.
2. **Check:** the first 1,024 yields equal `sp.natural_prefixes(prefix_tokens, rnd)` and D's natural prefixes exactly.
3. r\* is the row of the 1,024th yield. The fresh prefixes are the yields of rows r\* + 1 … 4095, in order. N_avail is their number.
4. Count the fresh prefixes whose token string occurs among D's 1,030 prefixes (§4.2).
5. **The 512 floor (R-X6ZC-4).** If N_avail < 512, record NOT_ENOUGH_DATA now. Default (owner Q3): Stage C later runs on all N_avail prefixes, descriptively; **no new sampling**.

**K0, exact oracle geometry** (blind; exact Fractions through `sp.q_exact`, `pairs:277–278`).
- **Scope:**
  - every W2, W1 and control pair of D;
  - every fresh-variant pair of both families on all N_avail fresh prefixes;
  - arms NA, ZC and AB.
- **Required, exactly:**
  1. q*_ZC(a) == q*_ZC(b) and q*_AB(a) == q*_AB(b) on every W1, W2 and variant pair.
  2. Cue-normalised Δq*_NA,c = λ(δ_{c²y} − δ_{cy}) on every pair of every variant of each family (λ₁₈ for W2, λ₈ for W1), with den_i = 2λ².
  3. The answer table and missed-crossing classes of §3.1 hold on every pair. The missed-crossing laws are point_law(n + 1, g[y]), with g the ZC holonomy of the segment after the named crossing's label is replaced by e (`model:186–190`, `242–247`). No new history is built.
  4. **Variant matching.**
     - W2 variants: token bag, directed-bigram bag, κ, (n, v_t, y) and the last 8 symbols (the checks of `tad:122–144`).
     - W1 variants: the `exact._EQUAL_ROWS` set (`exact:283`); the start vertex is an anchor neighbour; adjacency is legal; the crossing letters are as designed; the end vertex is an anchor neighbour with q* cue mass 1/5. Bag difference and tail length are recorded; the shared tail and crossing steps must equal those values (tails 4/2/3/3 tokens and crossing steps 3–4/5–6/4–5/4–5 for PP/MM/PM/MP).
  5. q*_NA is prefix-invariant on the fresh prefixes.
- **Output.** The coupling table: for every family, variant and y, the cosines of e_z = δ_z − ⅓·1 and of the missed-crossing directions with Δq*_NA.
- **Failure:** any mismatch with §3.1 → **STOP_REPLAN** (rule G-R0). No model has run yet; the hypotheses are re-derived before anything else.

**K1, exact invariance for exactly commutative predictors** (D's W2 and W1 through `eval.designed_stats` (`eval:274–304`) or its `pair_terms` path; every fresh variant through the new per-pair path).
- **Predictors:**
  - OraclePredictor("ZC", "qstar") and ("AB", "qstar") (`eval:129–139`);
  - q_empty, q_parity, q_counts, q_H1 and q_Parikh (`pairs:288–296`);
  - the set-constant ⅓ cue law;
  - **X's matched-key analytic predictor**: an integer K is formed from (prefix tokens, cue, n, end vertex, Parikh vector), and the predictor returns cue law (K+1, K+2, K+3)/(3K+6) with a K-dependent cue mass, the rest spread over non-cue tokens, identically for both members. This tests non-constant class dependence and varying cue mass.
  - q_8 (`pairs:299–307`) on W2 and its variants only (last 8 identical). It is not used on W1, which shares only the last 4.
  - sym(m), p(h) := ½(p̂_m(a) + p̂_m(b)) for both members, for m ∈ {ZC-s1, ZC-s3, ZC-s4}. It is built from Stage-B readouts, so this check runs at the start of Stage B.
- **Required:** `beta == 0.0` and `rho == 0.0` as floats, every pair numerator exactly 0, and `eval.beta_exact(num, den) == 0` (`eval:225–234`).
- **Failure** while the code is otherwise verified → ESTIMATOR_ARTIFACT/NON_INVARIANT.

**K2, exact references** (D's W2 and W1, and the fresh PP of both families).
- q*_NA: |β − 1| ≤ 1e-12, pooled and per cue, on every family and variant.
- h_last: per cue (½, −1, ½), pooled |β| ≤ 1e-12.
- h_first: per cue (−½, 1, −½).
- h_rev: −1 within 1e-12.
- These hold on W2 and W1 (`pairs:310–322`; `exact:285–287`; `exact.beta_table`, `exact:196–216`).
- The heuristics' values on MM, PM and MP are computed exactly and recorded. They are known cases, not gates, because last/first depend on letters.
- **Failure** → DEFECT_CANDIDATE.

**K3, synthetic mechanisms** (discrimination feasibility; working rule 1).
- **Mechanisms**, built from q*_ZC and q*_NA laws on both families with parameters (w, κ, π) ∈ {0.05, 0.2} combinations, and with both signs:
  - M0, M1, M2a (first loop missed) and M2b (second loop missed);
  - M4 (one seam's crossing missed, in one order only);
  - M6 (both crossings missed, order-asymmetric).
- **Recorded known cases only, not gated:** a W1 token-identity mechanism (a law depending on whether vertex 3 or 12, or 0 or 15, was visited).
- **Exact values.** β_v for the four variants, in Fractions on prefix Π0 (exact because q* is prefix-invariant).
- **Float path.** The same predictors through the float pipeline on the fresh variants agree within 1e-12.
- **Feasibility gate F1** (per family):
  - M0 gives r_v = 1 for all v;
  - every sign-symmetric Z₃ mechanism (M1, M2a, M2b, M4, M6) has at least one r_v with |r_v − 1| ≥ 1, so it lies outside [0.5, 1.5] by at least 0.5.
  - every sign-symmetric Z₃ mechanism (M1, M2a, M2b, M4, M6) gives r_MM = −1 exactly (the R8 route); a failure is recorded before Stage B as UNEXPLAINED/NOT_DISCRIMINABLE(<mechanism>) for ZC_COORDINATE and NOT_NA_DIRECTION.
- **If F1 fails** for a listed mechanism, the NA_DIRECTION outcome is replaced by UNEXPLAINED/NOT_DISCRIMINABLE(<mechanism>) for that family, recorded before Stage B.
- **Known limit, recorded now.** A Z₃ error whose rates depend on loop sign in a tuned way can mimic NA invariance. The NA_DIRECTION licence therefore says only "not explained by sign-symmetric Z₃ counting errors".

**A4, exposure check** of the fresh variant histories against the 7 train pools of §4.4.
- Each fresh w_{1:t} is compared byte for byte with w_{1:t} of every pool row, bucketed by t.
- **Policy, fixed now.** Matches are kept, counted and reported. If any exist, the Stage-C decision is recomputed without them as a sensitivity line; the registered decision uses all histories.
- Expected counts: about 0 for W2 (one designed path has probability about 5⁻¹⁷). For W1 with short prefixes a few matches are possible (probability about 5⁻⁸ per pool row per history).

## 7. Stage B: descriptive, models on the opened D only

**Order (known cases first, request requirement 2).** Stage-A exact references, then init-s1..s4, AB-s1..s4, ZC-s2, NA-s1..s4, and the focal models ZC-s3, ZC-s4 and ZC-s1 last. Each earlier group must reproduce (B1) before the next is interpreted. Inits and trained controls are empirical comparison cases. Their "known answer" is their stored value; they are not forced to zero.

**B1, K4 bit-exact reproduction (gate).**
- **What runs:**
  - for the 12 admitted step-30,000 models: `eval.ModelPredictor` (`eval:67–114`, which verifies the file sha and weights digest against the lock);
  - for the 4 inits: the state spec of the E3w chunk (`eval._predictor`, `eval:408–411`, `{"state"}` from `stages/E0/init/init_s<s>.pt`, checked against the CLOUD-PREP weights digest);
  - then `eval.designed_stats` on `tables/designed.npz` (sha-verified), with `tables/log_tables.npz` and a cached q*_NA function. The cache returns arrays identical to `eval.qstar("NA", …)` (`eval:147–154`) and is computed once in K0; its equality with uncached `qstar` is a test.
- **Required:** every stored key (β_W2, β_W2_y, R_W2, Δ_W3, ρ_C, ρ_W2, cue_mass_median, β_W1, β_W3, β_W3_bal, β_W3p, nonfinite) equal as a float.
- **Otherwise:** the K4 tiers of §5.

**B2, K5 independent checks** (ZC-s1, ZC-s3, ZC-s4, NA-s1 and init-s1; for W2 and W1).
- (a) An independent re-implementation: pairs by explicit content identity; p̂ and q* converted to exact Fractions; independent cue normalisation and pair terms; independent aggregation. It must match `designed_stats` (§5 tiers). Also cross-checked with `exact.beta` on actual pair membership with within-pair centring.
- (b) Swapping a and b jointly in p̂ and q* leaves num exactly unchanged. Swapping on the predictor side only flips the sign.
- (c) **Padding invariance:** re-pad after t with token 5 instead of 0; p̂ at t within 1e-13 max-abs.
- (d) **Batch invariance:** one-at-a-time vs batches of 1,024, ≤ 1e-12.
- (e) **Readout index.** On W2 the median p̂ cue mass is in [0.15, 0.25] at t and ≤ 0.01 at t − 1. The q* cue mass at t − 1 is exactly 0 (vertex 15 has no anchor neighbour). The same holds on W1 at t − 1 (vertex 5).
- (f) The K1 check of sym(m).
- (g) **Two independent model loads** give identical outputs.
- (h) **Scalar vs vector readout positions** agree.
- (i) **Joint row permutation and restoration** preserves every statistic.
- (j) **Independent BOS and readout extraction** (BOS = 18, logits at position t, `eval:35`, `eval:111–113`) agrees within 1e-12.
- Items (g)–(j) run on a fixed structural subset: the first pair in each observed (readout length, cue) cell, chosen from metadata only.
- **Any failure** → DEFECT_CANDIDATE.

**B3, alignment decomposition** (all 16 predictors, per pair, W2 and W1).
- Basis of the cue-difference plane: e₁ = (δ_{n_a} − δ_{n_b})/√2 (the NA direction) and e₂ = (2δ_w − δ_{n_a} − δ_{n_b})/√6, with w the third cue.
- **Report:**
  - cos_agg (which reproduces β/√ρ) and β²/ρ;
  - φ₁ = Σ(Δp̂·e₁)²/Σ‖Δp̂‖²;
  - the means and SDs of the e₁ and e₂ components;
  - the fraction of pairs with ⟨Δp̂, Δq*⟩ > 0;
  - the distribution of paired full-vocabulary and cue-normalised differences;
  - prefix- and cue-level numerators.
- **Descriptive expectations:** missed-crossing errors put φ₁ near 1; pure confidence asymmetry gives φ₁ = 0.75 and cos = 0.866.

**B4, ZC-coordinate profile.**
- For each member and each k ∈ {0, 1, 2}: the mean p̂ cue share on c^k·y.
- For each member: the own-arm regret, mean KL(q*_ZC ‖ p^Q), through `eval.quantise` (`eval:161–176`), `eval.score` (`eval:187–191`) and the ZC codes of `eval.qstar("ZC", …)`.
- Run for ZC-s1..s4, AB-s1..s4 (in their own coordinate a·y) and the NA models, on W2 and W1.

**B5, prefix-cluster bootstrap.** For every predictor, a 5,000-draw paired bootstrap of β_W2, ρ_W2, β_W1, ρ_W1 and the per-cue values: report the SD and the 95 % interval.

**D2, cue-normalisation decomposition** (X; W2 and W1; all predictors).
- For each pair, with cue masses m_a, m_b and m̄ = (m_a + m_b)/2:
  c_a − c_b = (p_{a,c} − p_{b,c})/m̄ − (m_a − m_b)/(2m̄)·(c_a + c_b).
  This is an algebraic identity. The two terms are projected onto d_i, and their contributions must sum to the original numerator within 1e-12.
- β_fixed = Σ⟨5(p_{a,c} − p_{b,c}), d_i⟩ / Σ‖d_i‖², using the oracle cue mass 1/5.
- Report the per-family cue-mass minimum, median, 1st/5th/10th percentiles and the fraction below 0.10. No row is deleted from the primary census.
- **READOUT_AMPLIFIED** (qualifier): |β − β_fixed| ≥ 0.05 **and** the two values cross 0.10 (§5).

**D3, prefix and weighting summaries** (X and L).
- Summaries:
  - the six named prefixes vs the 1,024 natural ones;
  - each prefix length, and the bins L ∈ {1–4, 5–9, 10–14};
  - four consecutive blocks of natural prefixes;
  - equal weight per distinct token prefix (all three cues kept);
  - equal weight per prefix length;
  - leave-one-distinct-prefix-out β;
  - the share of Σ|num| from the top 5 % of prefixes and from the top 10 % of distinct-prefix groups.
- Identical token prefixes are grouped, and their multiplicities reported.
- **MULTIPLICITY_SENSITIVE / LENGTH_WEIGHT_SENSITIVE** (qualifiers): the relevant alternative weighting changes β by ≥ 0.05 **and** crosses 0.10. These alternatives never replace the registered estimand. Concentration alone does not establish a sampling accident.

**B6, cross-model similarity.** A 16 × 16 matrix of cosines between stacked per-pair Δp̂ vectors on W2 and on W1. Of interest: ZC-s1 with NA-s1 (shared seed) vs NA-s2..s4, AB-s1 and ZC-s2..s4; ZC-s3 with ZC-s4 on W1.

**B7, control families.** Per-family ρ (C1–C4 separately), per-cue β_W1,y and ρ_W1 (not stored in X6S1), β_W3 and β_W3′ for every predictor.

**B8, emergence (optional; G3).** β_W2, ρ_W2 and β_W1 of ZC-s1 at steps 1,000, 3,000, 10,000, 20,000 and 30,000 from its stored chain (§4.4 item 7, sha-checked against the chain records), on D's W2 and W1 only.

**B10, float32 replay (descriptive; cheap).**
- A float32 copy of each focal model (`ModelPredictor.float32`, `eval:97–102`) on its focal family.
- **PRECISION_SENSITIVE:** |β₃₂ − β₆₄| > 1e-5. This never invalidates the float64 estimand. (`float32.json` already records max_abs 6.8e-7 for ZC-s1 on natural rows.)

**Descriptive tier (MD-6; track X's ZC_NOT_COMMUTATIVE on the census).** For each trained control m and family F ∈ {W2, W1}, CENSUS_NON_INVARIANT(m, F) is assigned when:
- B1 gives PASS or ENV_DRIFT;
- K1 and K5 pass;
- the maximum paired cue-normalised difference exceeds 1e-9 on at least one verified pair.

Attached qualifiers:
- READOUT_AMPLIFIED, MULTIPLICITY_SENSITIVE, LENGTH_WEIGHT_SENSITIVE and PRECISION_SENSITIVE where they fire;
- ORIGIN_UNRESOLVED always;
- BAG_UNMATCHED on W1;
- FAMILY_PATTERN(β_W1, β_W2), which replaces X's W2_SPECIFIC_ON_TESTED_FAMILIES because W1 also shows control responses.

This tier is reported beside the registered tier and never changes it.

**B9, G1 sizing** (frozen rule; blind with respect to Stage C).
- **Inputs.** SE_D(cell) is the SD of the 5,000 B5 draws of the cell's β on D: β_W2(ZC-s1) for cell P, β_W1(ZC-s3) for S3 and β_W1(ZC-s4) for S4. β_D(cell) is the stored value.
- **Predicted half-width of each r_v at n fresh prefixes:**
  h(n) = z·√2·SE_D·√(1030/n) / max(|β_D| − 2·SE_D, 0.05).
  - z = 2.394 for cell P: two-sided 98.33 %, Bonferroni over 3 ratios.
  - z = 2.638 for cells S3 and S4: two-sided 99.17 %, Bonferroni over 2 cells × 3 ratios.
- **Variance assumptions behind the rule (R-X6ZC-4; MD-5 fix 2):**
  - (V1) **Exchangeability.** Fresh prefixes are later draws from the same registered stream as D's natural prefixes, so a cell's prefix-level SD carries over, and SE scales as √(1030/n). D's 6 named prefixes are ignored in this approximation.
  - (V2) **Equal or smaller variance in the variants.** For each v ∈ {MM, PM, MP}, the prefix-level SD of β_v^fresh is at most that of β_PP^fresh. The variants are matched copies of the same geometry and readout age.
  - (V3) **Non-negative correlation** between β_v and β_PP across paired resamples when the true r_v ≥ 0 (shared prefixes).
  - Under V1–V3, the half-width of r_v at r ∈ [0, 1] is at most h(n), because Var(β_v − rβ_PP) ≤ (1 + r²)σ². At r = 1 this is the binding case: NA_DIRECTION needs the interval inside (0.5, 1.5).
  - For r < 0 (the Z₃ hypotheses), the Cauchy–Schwarz bound is 2σ instead of √2σ. The distance to the band is then 1.5, so this case is not binding.
- **These assumptions affect power only, never validity.** Every Stage-C decision uses the realised bootstrap intervals. The report gives realised against predicted half-widths and the realised SD ratios.
- **Choice.** n is the smallest of {1,024; 2,048; N_avail} ∩ [512, N_avail] with h_P(n) ≤ 0.25. Each hypothesis is ≥ 0.5 = 2 × 0.25 away from the 0.5 threshold (working rules 1 and 3).
  - If 512 ≤ N_avail < 1,024, the only candidate is N_avail.
  - If no candidate qualifies, record UNDERPOWERED for cell P before Stage C. Ruling (OPEN-1, closed): if no sample size meets the precision target, the registered check runs at the largest available size, labelled underpowered and descriptive.
- **Replication feasibility (rule 1), from stored values:** |β_D|/0.10 = 2.09 (P), 1.33 (S3), 2.18 (S4). S3's outcome carries the qualifier LOW_FEASIBILITY(S3).
- **Secondary cells.** If h_S(n) > 0.25 at the chosen n, that cell is UNDERPOWERED (descriptive). The secondary cells never change n.

**Stage B gate.** Stage C runs only if no global rule G-R0..G-R3 (§9) fired, apart from a defect recorded as DEFECT_ELSEWHERE (§10).

## 8. Stage C: registered, run once on the fresh set

**Cells (frozen now from stored, opened values).** The selection rule is: a commutative-trained control with |β_D| > 0.10 on W1 or W2.

| Cell | Model × family | β_D | Sign σ | Role |
|---|---|---|---|---|
| **P** | ZC-s1 × W2 | +0.2093 | +1 | **Primary:** gives the headline X6ZC outcome |
| S3 | ZC-s3 × W1 | −0.1325 | −1 | Secondary registered finding |
| S4 | ZC-s4 × W1 | −0.2184 | −1 | Secondary registered finding |

**What runs.**
- The 16 predictors, the q*_NA float reference and the K3 synthetic predictors, on PP, MM, PM and MP of **both** families.
- For the first n fresh prefixes × 3 cues × 2 members: 48n histories per predictor (49,152 at n = 1,024).
- No model is evaluated on any other fresh history.

**Per family, variant and predictor:** β_v = Σnum/Σden pooled over prefixes and cues (equal counts per cue), plus ρ_v, the per-cue β_v,y and the B3/B4 summaries.

**Registered statistics, per cell**, with σ the cell sign:
- **b = σ·β_PP^fresh**, with its paired prefix-cluster interval: 95 % for P (quantiles 0.025 and 0.975), 97.5 % for S3 and S4 (0.0125 and 0.9875).
- **r_v = β_v/β_PP** for v ∈ {MM, PM, MP}, computed inside each draw. Intervals: (1/120, 119/120) for P; (1/240, 239/240) for S3 and S4.
- **Undefined draws.** A draw with σ·β_PP\* ≤ 0 is undefined and excluded from the ratio quantiles. If more than 1 % of draws are undefined → UNSTABLE_RATIO for that cell.
- **β_sb = ½(β_PP + β_MM)** per cell, with a 95 % interval. It is reported for the reuse amendment (§9.4) and is not a decision statistic.
- **Cell-P qualifier (registered; never changes the outcome):** r_W1|P = β_W1,PP^fresh(ZC-s1) / β_W2,PP^fresh(ZC-s1), with a 95 % interval. M0 predicts 1.
  - W2_ONLY if the upper bound is < 0.5;
  - NA_BOTH_FAMILIES if the interval lies inside (0.5, 1.5);
  - none otherwise.

**K6, fresh-set stability (validity, per family).**
- W2: at least 10 of the 11 other controls (init-s1..s4, AB-s1..s4, ZC-s2..s4) have |β_W2,PP^fresh| ≤ 0.10.
- W1: at least 9 of the 10 controls outside cells S3 and S4 (init-s1..s4, AB-s1..s4, ZC-s1, ZC-s2) have |β_W1,PP^fresh| ≤ 0.10.
- Failure → FRESH_SET_UNSTABLE for the cells of that family.

**Descriptive only:**
- every other predictor's β_v and r_v, including the four NA models as an empirical positive control for sign invariance (owner Q2);
- the B4 profile on the variants;
- the exposure and D-coincident-prefix sensitivity lines (§4.2, A4).

## 9. Outcomes, decision rules and licences

### 9.1 Rules, applied in order (first match wins)

**Global rules (whole study):**

| Rule | Condition | Outcome |
|---|---|---|
| **G-R0** | K0 mismatch (evaluated as soon as K0 runs, before any model) | **STOP_REPLAN**: no outcome; re-plan |
| G-R1 | A stage did not complete (crash, NaN or QuantInvalid in a required value, meter stop) after its one unchanged technical rerun (G2) | INVALID (technical; no statement) |
| G-R2 | A1, A2, A-audit, K2, K4 (> 1e-9 relative) or K5 fails, and a code or data cause is identified that affects β_W1 or β_W2 | **DEFECT_FOUND** (Stage C does not run; §10) |
| G-R2′ | One of those fails and no cause is identified | UNEXPLAINED/IRREPRODUCIBLE |
| G-R3 | K1 fails while A2 and K5 pass | **ESTIMATOR_ARTIFACT/NON_INVARIANT** |

A cause that is a setup error of this study (A1 item 6 non-empty diff, wrong worktree, an environment difference beyond the commit) is not a defect. The stage stops before any further payload is opened, the setup is corrected, and the stage restarts under G2. It is never DEFECT_FOUND or DEFECT_ELSEWHERE. If the recorded environment cannot be restored, the outcome is INVALID (technical).

**Per-cell rules** (cell P gives the headline; S3 and S4 their own findings):

| Rule | Condition | Outcome (cell P, W2) | Outcome (cells S3, S4, W1) |
|---|---|---|---|
| R4a | NOT_ENOUGH_DATA at A3 (N_avail < 512) | UNEXPLAINED/NOT_ENOUGH_DATA (Stage C descriptive) | same |
| R4b | UNDERPOWERED at B9 for the cell | UNEXPLAINED/UNDERPOWERED (descriptive) | same |
| R5 | K6 fails for the cell's family | UNEXPLAINED/FRESH_SET_UNSTABLE | same |
| R6 | hi(b) < 0.10 and lo(b) ≤ 0 | **ZC_NOT_COMMUTATIVE/NOT_REPLICATED** | same |
| R7 | Not R6, and (b < 0.10 or lo(b) ≤ 0.05) | UNEXPLAINED/WEAK_REPLICATION: the **"positive but below margin" licence** when lo(b) > 0 and b < 0.10; otherwise "replication ambiguous" | same |
| R7b | > 1 % undefined ratio draws | UNEXPLAINED/UNSTABLE_RATIO | same |
| R8 | hi(r_MM) < 0 (the r_MM interval lies entirely below 0) | **ZC_NOT_COMMUTATIVE/ZC_COORDINATE** | ZC_NOT_COMMUTATIVE/NOT_NA_DIRECTION |
| R8b | Not R8, and for at least one v the r_v interval lies entirely outside [0.5, 1.5] | UNEXPLAINED/NOT_NA_INVARIANT | same |
| R9 | F1 passed for the family, and all three r_v intervals lie inside (0.5, 1.5) | **ZC_NOT_COMMUTATIVE/NA_DIRECTION** | ZC_NOT_COMMUTATIVE/NA_DIRECTION (W1) |
| R9′ | The R9 interval pattern while F1 failed | UNEXPLAINED/NOT_DISCRIMINABLE(<mechanism>) | same |
| R10 | Otherwise | UNEXPLAINED/PARTIAL | same |

- **Comparisons** are strict as written. lo and hi are the cell's registered interval bounds.
- **Precedence.** Global rules pre-empt every cell. A DEFECT_ELSEWHERE qualifier (§10) does not pre-empt.
- **R8, R8b and F1.** Unlike track L, R8 and R8b do not require F1. An out-of-band ratio excludes M0 whatever F1 says; F1 governs only NA_DIRECTION. Only the r_MM sign reversal (R8), which every sign-symmetric Z₃ mechanism predicts, earns the Z₃ licence; an out-of-band ratio without it (R8b) is NOT_NA_INVARIANT.

### 9.2 What every outcome says about X6 stage 1 (L's sentence, carried by every licence)
- The registered outcome stays INCONCLUSIVE (rule 9), with CONTROL_LIMITED(designed, s1) and DESIGNED_UNRESOLVED(1).
- ordD(s1) stays UNRESOLVED, and no seed is relabelled FAIL.
- Nothing here turns rule 9 into rule 8. ZC-s1's control result is not removed or replaced.
- A description may say, as already recorded facts, that NA-s1's own designed numbers lie on the FAIL side of both registered bars (β_W2 = 0.088 < 0.25; R_W2 = 0.0797 > 0.0458). Each such sentence must say that the flag remains UNRESOLVED. No sentence may state or imply what ordD(s1), rule 8 or the stage-1 outcome would have been without the ZC-s1 placebo failure.
- No claim about topology, internal representation or causal necessity.

### 9.3 Licences

| Outcome | Licensed sentence (brackets filled) | Not licensed |
|---|---|---|
| **DEFECT_FOUND** | "The value [β_F(m)] was produced by [defect: file, line, effect]; a versioned corrected computation gives [v] (descriptive)." | Any change to the X6S1 outcome. Whether X6S1's technical-correction path applies (protocol §3 row 3, §12 item 3) is the owner's decision (§10). |
| **ESTIMATOR_ARTIFACT/NON_INVARIANT** | "The registered designed β estimator is not invariant for [exactly commutative predictor]; the designed placebo cannot certify specificity in its current form." | Any statement about the trained controls' behaviour |
| **ZC_NOT_COMMUTATIVE/NOT_REPLICATED** | "ZC-s1's predictions differ between the two orderings of the registered W2 census (β = 0.209, reproduced through a verified pipeline): a real response of this model on the registered prefixes. It did not replicate on [n] unused prefixes (β_PP = [ ], 95 % interval [ ], below the 0.10 margin and not above 0)." | "Estimator artefact", "chance", or that ZC-s1 is commutative on designed inputs in general |
| **UNEXPLAINED/WEAK_REPLICATION**, positive-below-margin case (addendum 25 rule 6) | "On [n] unused prefixes ZC-s1's W2 order response is positive but below the 0.10 placebo margin: β_PP = [ ] (interval [lo, hi]; lo > 0). It is not exact commutativity and not absence of order sensitivity." | Any mechanism; "the placebo failure was noise" |
| UNEXPLAINED/WEAK_REPLICATION, ambiguous case | The numbers only: "replication ambiguous (β_PP = [ ], interval [ ])." | Any explanation |
| **ZC_NOT_COMMUTATIVE/ZC_COORDINATE** (cell P) | "ZC-s1's next-cue predictions differ between the two orderings of the registered W2 family and of its loop-sign variants on [n] unused prefixes, unlike [k] of the other seven commutative controls on W2 (|β_W2,PP^fresh| ≤ 0.10; any exception named). When the loop directions are reversed, the response reverses sign (r_MM = [ ], interval below 0) relative to the NA oracle's contrast (r_PM = [ ], r_MP = [ ], intervals [ ]), which the NA contrast itself does not do. This is the pattern of an order-dependent Z₃ counting error. On W2 such an error is projected onto the NA contrast, because NA's x-first answer equals ZC's answer and NA's y-first answer equals ZC's answer with one crossing missed. The stage-1 placebo failure is therefore read as a control-specific order error made visible by the W2 geometry, not as NA-direction order use by ZC-s1 and not as a pipeline artefact." | How ZC-s1 computes (no mechanism, probe or intervention); that the NA models' designed statistics are free of other artefacts; anything about retrained models; any change to rule 9 |
| **ZC_NOT_COMMUTATIVE/NOT_NA_DIRECTION** (W1 cells) | "[ZC-s3/ZC-s4]'s W1 response replicated on [n] unused prefixes and reverses sign when both crossings are reversed (r_MM = [ ], interval below 0), so it is not an NA-direction response. W1's members differ in one visited vertex, so this pattern fits an order-dependent Z₃ counting error or an order-free token-identity effect; W1 cannot separate the two. The four NA models' W1 r_v values are printed beside the cell." | "Order use" by the control; a Z₃ mechanism specifically |
| **UNEXPLAINED/NOT_NA_INVARIANT** | "[Model]'s response replicated (β_PP = [ ]) and is not invariant to loop-sign reversal (r_v = [ ], intervals [ ]), but it does not reverse sign when both loops are reversed; it matches neither the NA oracle nor a sign-symmetric Z₃ counting error." | Any mechanism; "NA-direction"; "Z₃ error" |
| **ZC_NOT_COMMUTATIVE/NA_DIRECTION** | "[Model] shows an order response on [family] aligned with the NA oracle's composition and invariant to loop-sign reversal on [n] unused prefixes (r_v intervals inside (0.5, 1.5)); it is not explained by sign-symmetric Z₃ counting errors. Its source is unidentified." Plus the r_W1\|P qualifier for cell P. For the W1 cells S3 and S4 the sentence adds: "The four NA models' W1 r_v values are printed beside the cell." This triggers a provenance audit (a token-content check of the model's training batches beyond LOSS-ECHO's first-batch losses), which needs its own go-ahead. | "Leak", "NA knowledge" or "learned S₃ composition"; any statement about the NA models |
| **UNEXPLAINED/PARTIAL** | "[Model]'s response replicated (β_PP = [ ]), but its loop-sign ratios were neither clearly NA-invariant nor clearly Z₃-covariant ([intervals]); a sign-invariant component of up to [upper r × β_PP] cannot be excluded." | Any explanation |
| **UNEXPLAINED/** (NOT_ENOUGH_DATA, UNDERPOWERED, FRESH_SET_UNSTABLE, IRREPRODUCIBLE, UNSTABLE_RATIO, NOT_DISCRIMINABLE; NOT_NA_INVARIANT has its own row above) | The numbers only, labelled descriptive where Stage C ran descriptively | Any explanation |
| STOP_REPLAN, INVALID | No statement | — |

**Qualifiers carried by every ZC_NOT_COMMUTATIVE outcome:**
- ORIGIN_UNRESOLVED;
- the Stage-B qualifiers that fired;
- for cell P, r_W1|P (W2_ONLY / NA_BOTH_FAMILIES);
- the A4 and D-coincident-prefix sensitivity lines, where they differ.

### 9.4 Placebo-reuse verdict (two axes; MD-6)

**Axis 1, computational validity** (from A1, A2, A-audit, K0–K2, K4, K5):

| Value | Condition |
|---|---|
| VALID | All of these pass; K4 is PASS or ENV_DRIFT |
| NOT_FIT | DEFECT_FOUND (until a versioned fix passes K1–K5 again) or NON_INVARIANT |
| UNDETERMINED | IRREPRODUCIBLE, INVALID or STOP_REPLAN |

**Axis 2, scientific specificity** (from the K0 coupling algebra, the W1 data and Stage C). Assessed only if axis 1 is VALID.

| Value | Condition | Amendments (proposals for a future protocol version; each needs its own known-case checks and freeze; nothing is retroactive) |
|---|---|---|
| **FIT_WITH_AMENDMENT** | K0 confirms the coupling for W1 and W2. This is expected from the algebra, independently of Stage C. | 1. A Z₃ control is not a clean placebo for an NA contrast with this coupling. Drop it as a designed placebo, or gate it on β_sb = ½(β_PP + β_MM), which is 1 for q*_NA and 0 for sign-symmetric Z₃ errors (validated by K3 and the Stage-C control values). This is supported by K0 and the W1 data whatever Stage C gives. 2. Put the β and ρ bars on one scale (|β| ≤ √ρ), or gate on ρ relative to the NA models. 3. Give the designed placebo a prefix-cluster interval and a per-control known-case check (working rule 5); use larger or fresh prefix sets. 4. The sign-variant discriminator works for Z₃-type controls only: AB is sign-invariant like NA (a = a⁻¹), so AB-type errors could mimic NA_DIRECTION. On bag-unmatched families (W1), it cannot separate counting from token-identity effects. |
| UNDETERMINED | Cell P is NA_DIRECTION: the placebo did its job and the anomaly sits in the control | Amendments 2 and 3 still apply |
| (axis 1 not VALID) | — | Not assessed |

- If cell P is NA_DIRECTION, axis 2 is UNDETERMINED; this takes precedence over FIT_WITH_AMENDMENT. The amendments listed are the union over cells P, S3 and S4.
- **Which amendments a verdict lists:** ZC_COORDINATE or NOT_NA_DIRECTION lists 1–4. NOT_NA_INVARIANT lists 1–3. NOT_REPLICATED or WEAK_REPLICATION lists 1–3. PARTIAL or another UNEXPLAINED lists 1–3, with amendment 1 marked "supported by algebra and W1 data; Stage C inconclusive".
- **Reuse statement (all VALID cases, from X):** the W2/W1 pipeline may be reused as a behavioural contrast with explicit empirical controls. It must not be described as automatically excluding every predictor trained on a commutative process.

## 10. Defect path (R-X6ZC-6)

- **Report.** On any DEFECT_CANDIDATE with an identified cause, the coordinator writes `agent-handoff/jobs/<id>/DEFECT.md` with:
  - the file, line and effect;
  - a minimal reproduction;
  - expected vs observed behaviour;
  - the implicated source version;
  - the affected X6S1 statistics;
  - whether it is a **code** defect or a **specification** defect. X6S1 §12 item 3: a failure that shows a protocol statement to be wrong is not a defect.
- **Never fixed in place.** `tools/x6_stage1` is not edited. A correction is a new versioned function in `tools/x6zc` (or, if the owner rules for an X6S1 correction, a separate erratum: coordinator addendum 6, API §13 item 42). It comes with an independent regression fixture and a review. Original and corrected values are shown side by side, the corrected ones labelled descriptive.
- **Who decides.** Whether X6S1's documented-technical-correction path (protocol §3 row 3; §12 items 3 and 5) applies is the **owner's decision**, after the written report. Until then the stage-1 result stays as registered.
- **Effect on this study.**
  - A defect that affects β_W1 or β_W2 gives DEFECT_FOUND and stops before Stage C (OPEN-2, closed): a defect affecting the designed β values stops the registered check and goes to the owner as a defect report.
  - A defect elsewhere (for example in a record unrelated to the designed statistics) is reported as qualifier DEFECT_ELSEWHERE(<id>), and the study continues.

## 11. What cannot be answered without training

- How often designed-placebo failures occur among Z₃ control seeds (3 of 4 seeds exceed 0.10 on W1 or W2; this is a description, not a rate).
- Whether a retrained model would show the same response. Training is not bit-reproducible (X6S1 §1.3).
- Which training feature caused the learned function (ORIGIN_UNRESOLVED).
- These need new seeds (GPU training, plus about 0.1 CPU-h of designed-only evaluation per seed) or an intervention on training.

This study answers *why these models' values arose* and *whether the instrument is sound*. Neither needs training.

## 12. Synthetic dry run (working rule 4; before freeze; needs owner go-ahead (a))

**Setup.**
- **Where.** A scratch store `X:/Downloads/topo-scratch/x6zc-dry/`. No project store data, no admitted weights, no world sampling.
- **Synthetic prefix pool.** 4,096 rows of random legal walks on the torus from a numpy generator with a scratch seed (adjacency only, cue tokens at anchor visits drawn uniformly), so the `natural_prefixes` rule yields a test set with a known r\*. A second pool is truncated so that N_avail < 512.
- **Synthetic models.** Two tiny random-init `TransformerLM(MODEL_CFG)` states saved as fake checkpoints with fake admission locks. They exercise the `ModelPredictor` sha checks, the stage runner, the meter path and the ledger.
- **Dry-run sizes.** The two random-init models are evaluated on the first 64 prefixes of the synthetic D and on n = 128 fresh synthetic prefixes; analytic and planted predictors use full sizes.

**Planted predictors** (each through the whole pipeline: input manifest → construction validation → predictor adapter → raw outputs → production statistics → independent reference → decision → report):

| Fixture | Expected |
|---|---|
| r_PM interval above 1.5 with r_MM ≈ 1 | UNEXPLAINED/NOT_NA_INVARIANT |
| M0, w = 0.2 (both families) | ZC_NOT_COMMUTATIVE/NA_DIRECTION |
| M2a, π = (0.05, 0.25), on W2 | ZC_COORDINATE |
| M2a with π_a > π_b, on W1 (negative cell sign) | NOT_NA_DIRECTION |
| M1 | ZC_COORDINATE |
| Order response keyed to D-prefix ids only, absent on fresh | NOT_REPLICATED |
| Response β_PP = 0.05 with a tight interval | WEAK_REPLICATION, positive-below-margin licence |
| M0 (w = 0.15) + M2a (π_a = 0, π_b = 0.05) on W2: exact r_MM = 0.5, r_PM = 0.875, r_MP = 0.625 | PARTIAL |
| Response with σβ_PP\* ≤ 0 in > 1 % of draws (planted as a bimodal draw distribution: a few prefixes with large opposite-sign numerators) | UNSTABLE_RATIO |
| Two controls responding on fresh W2 | FRESH_SET_UNSTABLE |
| N_avail < 512 pool | NOT_ENOUGH_DATA, Stage C descriptive |
| SE large enough that no candidate n qualifies | UNDERPOWERED |
| Deliberately a/b-swapped pipeline fixture | DEFECT_FOUND (caught by K2 and K5) |
| Float-path fixture that breaks exact commutativity | NON_INVARIANT |
| A K0-violating variant path | STOP_REPLAN |
| Planted mixtures (1−δ)·q_Parikh + δ·q*, δ ∈ {0, 0.05, 0.10, 0.20, 0.25, 1} | β = δ exactly (X) |
| Joint member swap / predictor-only swap / joint permutation and duplication | unchanged / sign flip / unchanged |
| Mismatched joins, wrong readout positions | rejected |
| Zero cue mass, non-finite output, zero denominator | INVALID or undefined, never 0 |
| D2 identity on duplicate-prefix fixtures | holds within 1e-12 |
| Boundary fixtures inside and outside the 1e-9 band | the expected qualifier side |
| A simulated ledger above a 3× threshold | a pause record |

- **Pass.** Every expected outcome is reproduced exactly and the report schema validates. After any correction the full synthetic path is rerun before freeze.
- **Calibration (blind).** The measured CPU per history may update the §13 forecast **before freeze only**, and only if it lies outside [0.5×, 2×] of the anchor; the change is recorded. After freeze the thresholds never change.
- The result-blind review sees this evidence before freeze (PLANNING_PROTOCOL rule 4).

## 13. Adaptive budget (addendum 26)

**Cost anchor.**
- Job 0098 measured 64,767 CPU-s for 4 ZC chunks (`jobs/0098/report.md`). That is about 6.4 ms per history evaluation (model forward + exact q* + scoring), an upper anchor. The q* cache lowers it.
- Stage B evaluates 16 × 37,224 = 595,584 histories.
- Stage C evaluates 16 × 48n histories (786,432 at n = 1,024).

| Stage | Work | Central CPU-h (CPU-s) | Upper CPU-h |
|---|---|---|---|
| 0 | Independent tests (affected only) + synthetic dry run | 0.20 (720) | 0.40 |
| A | A1–A3, A-audit, K0 (3 arms × D pairs + 48 × N_avail fresh histories), K1–K3 references (W1, W2, variants), A4 (7 pools, hashing) | 0.85 (3,060) | 1.5 |
| B | B1 (595,584 histories), K5, B3–B7, D2, D3, B10, bootstraps; B8 optional (+0.05, 180 s) | 0.80 (2,880) | 1.2 |
| C | 48n fresh histories × 16 predictors, bootstraps | 0.90·n/1,024 (3,240·n/1,024) | 1.4·n/1,024 |
| **Total, n = 1,024** | | **2.75 (9,900)** | 4.5 |
| Total, n = 2,048 | | 3.65 (13,140) | 5.9 |

**Wall time.** About 3 h with ≤ 3 children.

**Measurement.**
- The project meter in measure-only mode (`--max-cpu inf`), the C: disk floor, and one new cumulative ledger `x6zc-store/cpu_ledger.json`. The ledger includes tests, the dry run, failed attempts, reruns and child processes.
- One child per model chunk, 2 intra-op and 1 inter-op threads, and the existing 3 GiB per-process limit.

**Frozen growth rules (blind quantities only):**
- **G1.** The Stage-C size n, from B9.
- **G2.** One unchanged technical rerun per stage after a technical failure. In Stage C no decision statistic, interval or summary is computed or displayed until every chunk has completed. The G2 rerun is allowed only while no Stage-C statistic exists; after that, a failure gives INVALID.
- **G3.** B8 runs only if Stage-B CPU to date ≤ its central forecast (2,880 CPU-s).
- **No other growth:**
  - no more models, families or variants;
  - no more prefixes after Stage C, and no rerun of Stage C after any statistic is seen;
  - no expansion because a value is near a margin;
  - batch size or streaming may change only to meet memory limits, after a synthetic equivalence check.

**3× pause points, in CPU-s (frozen; never reset by revising the estimate).** If measured CPU exceeds either threshold, the coordinator pauses at the next stage boundary and reports to the owner in plain language.

| Boundary | Cumulative threshold (3 × cumulative central) | Per-stage safeguard (3 × stage central) |
|---|---|---|
| After Stage 0 | 2,160 | 2,160 |
| After A | 11,340 | 9,180 |
| After B | 19,980 | 8,640 |
| After C, n = 1,024 | 29,700 | 9,720 |
| After C, n = 2,048 | 39,420 | 19,440 |
| After C, n = N_avail (any other n, including NOT_ENOUGH_DATA or UNDERPOWERED runs) | 19,980 + 9.4921875·n | 9.4921875·n |

## 14. Reuse and footprint

**Reused unchanged** (at ≥ 1dc9749; identical to 213d1e2):

| Module | Functions (lines) |
|---|---|
| `x6s1_pairs` | `natural_prefixes` 186–193, `_loops` 196–197, `designed_history` 200–202, `_w1_history` 205–207, `designed_set` 210–225, `designed_arrays` 235–246, `designed_sha256` 249–255, `q_exact` 277–278, `q_stat` 288–296, `q_window` 299–307, `q_heuristic` 310–322; `CONTROL_SETS`, `W2_LETTERS`, `_S7`, `PAIR_FAMILIES` 31–37 |
| `x6s1_eval` | `set_threads` 42–47, `model_inputs` 57–60, `ModelPredictor` 67–114 (incl. `float32` 97–102), `_law` 117–126, `OraclePredictor` 129–139, `qstar` 147–154, `quantise` 161–176, `score` 187–191, `kl_rows` 194–198, `cue_mass` 201–202, `cue_normalise` 205–211, `pair_terms` 214–217, `beta_fsum` 220–222, `beta_exact` 225–234, `_fam` 238–246, `designed_stats` 274–304, `_predictor` 408–411 |
| `x6s1_stats` | `log_tables` 110–127 (cross-check only), `quantile` 140–141, `boot_beta` 151–157 (single-variant cross-check) |
| `x6s1_data` | `MODEL_CFG` 83, constants 90–106, `run_key` 168–169, `init_state` 252–260, `holonomy_classes` 272–280 |
| `x6s1_stage_pre` | `ostore` 64–65, `pools_index` 66, `load_obs` 67–72 |
| `x6s1_ingest` | `admitted` 416–418, `verify_admitted` 441–452 |
| `x6s1_decide` | `ord_d` 107–128 (A1) |
| `x6s1_run` | `seed_fresh` 118–126 and `_seed_maps` 127–138 (pattern, for X6ZC_MASTER), `env_local` 231–242, `env_changed` 243–245, the `write_gate`/`write_stage` pattern 282–296 (pointed at the new store), `limits` 299–302, `launch` 303–309, `supervise` 310–343. `meter_bind_check` 147–151 is followed as a pattern only: it binds `sd.WORKTREE` (`<root>/topo-pilot-x6s1`), so X6ZC binds its own worktree. |
| Stage 0 | `x6_model`: `compose`/`inverse` 62–65, `seam_letter` 88–94, `seam_labels` 103–107, `edge_labels` 118–119, `holonomy` 186–190, `parikh` 227–231, `lam`/`point_law` 242–247, `parse` 248–260, `closed_form` 261–284. `x6_exact`: `LOOPS` 89, `members`/`witness_path` 95–104, `matched` 138–158, `competitor_holonomy` 169–180, `beta` 181–195, `beta_table` 196–216 |

Do not invoke `run_stage` (`run:497–534`), `eval_chunk` (`eval:438–479`) or the full E3 schedule.

**New code** (genuinely missing: loop-sign variants of W2 and W1, fresh-prefix continuation, per-pair geometry and audit, the matched-key predictor, paired cluster bootstrap with ratios, decompositions, the X6ZC decision):
- `tools/x6zc/x6zc_core.py` (≤ 400 lines):
  - constants and bindings: X6S1 store paths and hashes, H‴, X6ZC_MASTER, `VARIANTS` (W2 letters, W1 paths), `CELLS`;
  - `prefix_yields`, `fresh_prefixes`, `variant_arrays`;
  - `oracle_geometry` (K0), `audit_pairs` (A-audit), `synthetic_predictor` (M0–M6, matched-key, sym);
  - `pair_arrays`, `decompose` (B3, D2), `zc_profile` (B4), `weighting_summaries` (D3);
  - `paired_cluster_boot`, `ratio_intervals`, `decide_x6zc` (§9).
  - If it would exceed 400 lines, the descriptive functions move to `tools/x6zc/x6zc_census.py` (OPEN-4, closed: coordinator ruling).
- `tools/x6zc/x6zc_run.py` (≤ 400 lines): stages A, B and C, the gates, the store writer (exclusive create), the report, the CLI, `EXPOSURE.jsonl`, the meter binding, and the stage-1 store no-write check.
- **Stage-1 store no-write check (correction to track L).** Before and after each stage, a **metadata inventory** of `x6-stage1-store` (relative path, size, mtime_ns) must be identical. No content hashing: L's `run.store_lineage` (`run:154–162`) hashes accepted files and superseded payloads, which would be payload access including `sealed/`.
- `tools/x6zc/API.md`: a short written contract. It goes to the independent test author first.
- **Protocol (MD-8):** `agent-handoff/planning/responses/X6ZC-FROZEN-v1.md`, with its byte copy `tools/x6zc/PROTOCOL_X6ZC_v1.md`.
- **Tests (independent, result-blind authors):** `tests/x6zc/test_x6zc_core.py`, `test_x6zc_decide.py`, `test_x6zc_dryrun.py` (each ≤ 400 lines).
  - Authors work from `API.md` and fixtures only, with no store access, and are not the implementer.
  - Coverage:
    - variant matching for W1 and W2;
    - K0 on Π0;
    - exact M0–M6 values;
    - the paired bootstrap equal to `stats.boot_beta` per variant;
    - every decision branch and its precedence (G-R0 first);
    - fresh-prefix continuation equal to `natural_prefixes`;
    - cached vs uncached q* bit-identical;
    - the D2 identity;
    - the report schema.
  - Implementers never run a formatter over the tests directory (format their own files by name only).
- `docs/code_index/` regenerated with `tools/build_code_index.py` and committed separately (`docs(index): …`).
- **New store** `X:/Downloads/projects/topo-pilot/x6zc-store/`: `FREEZE.json`, `AUTH.json`, `cpu_ledger.json`, `stages/{A, B, C}/`, `report.json`, `EXPOSURE.jsonl` (first entry `E0-PREFIX-READ`), `EVALUATIONS.jsonl`, `logs/`. Mailbox job files as usual.

**Must not change:** `tools/x6_stage1/*`, `tools/x6_stage0/*`, `src/*`, anything in `x6-stage1-store` (read-only), or any frozen protocol.

**Execution worktree.** On a branch from 1dc9749 or later, with `PYTHONPATH=<worktree>/src` (the editable install points at main's `src`). Pytest basetemps under `X:/Downloads/topo-scratch/<job>/`. Affected tests only, run detached: the full suite exceeds the 600 s tool limit.

## 15. Authorisation steps (R-X6ZC-5; MD-9)

1. **Done:** planning go-ahead (owner addendum 27). It authorises planning only.
2. This merged plan → result-blind review (a clean-context Claude reviewer under PLANNING_PROTOCOL rule 5 while Codex is frozen, addendum 28) → coordinator acceptance as **design freeze candidate** (not the execution freeze).
3. **Owner go-ahead (a):** implementation, independent tests and the synthetic dry run (§12; about 0.2 CPU-h; no project data). The coordinator asks for it together with the other two rounds of addendum 27.
4. Plan + dry-run evidence → result-blind review → **freeze**: `X6ZC-FROZEN-v1.md`, `x6zc-store/FREEZE.json` with protocol sha256, code commit, X6ZC_MASTER and the §13 thresholds, the implementation commit hash and the sha256 of the dry-run report and its stage records.
5. **Owner AUTH (b), asked again after the freeze:** the real check under the staged adaptive budget with the frozen pause thresholds → `x6zc-store/AUTH.json`.
6. Stages A → B → C, each with a stage record and a coordinator review. Pauses as in §13. A plain-language report to the owner at the end, and at any pause or DEFECT_FOUND.

## 16. Risks

1. **Wrong code base.** Gated by A1 item 6 (R-X6ZC-1).
2. **Environment drift since 21 October.** Handled by the K4 tiers and the X6S1 environment rule (§12 item 6). A commit-only difference is expected.
3. **Forking paths.** Every rule, including the W1 cells, is frozen before Stage B. No model sees a fresh history before Stage C, and Stage C runs once.
4. **Fresh PP histories that coincide with opened ones** (repeated short prefixes). Counted, with a sensitivity line (§4.2). Independence of the sample is unaffected.
5. **Mechanism mimicry by sign-specific Z₃ errors.** F1 covers it; the NA_DIRECTION licence is narrow.
6. **W1 is bag-unmatched.** W1 cells can say only NOT_NA_DIRECTION, not ZC_COORDINATE.
7. **Overclaiming a mechanism** ("ZC-s1 misses crossings"). Licences say "the pattern of", never "the model does".
8. **Ratio instability** when β_PP^fresh is small. Handled by R6, R7 and R7b.
9. **Too few fresh prefixes.** The 512 floor, the B9 ladder and owner Q3.
10. **Meter and runtime traps.**
    - The default 600 CPU-s kill: use `--max-cpu inf`.
    - The `.venv` launcher (per-process CPU reads about 0): account by process tree.
    - The full suite longer than the tool limit.
    - The C: free-space floor.
11. **Payload access during execution is real access.** Every load of checkpoints and pools is logged in `EXPOSURE.jsonl`. Nothing under `sealed/` is read or hashed. The stage-1 store is checked by metadata only.
12. **A misread geometry in this plan** (including the writer's W1 variant paths). K0 checks it exactly before any model runs (STOP_REPLAN).
13. **Overstating causation.** Proximate explanation and origin are kept apart (ORIGIN_UNRESOLVED).
14. **Mistaking alignment for invariance.** A low β can coexist with substantial non-commutative spread; the descriptive tier reports both.

## 17. Open items (all closed by coordinator rulings, 2026-10-26)

- **OPEN-1, UNDERPOWERED handling. CLOSED.** If no sample size meets the precision target, the registered check runs at the largest available size, labelled underpowered and descriptive (B9; rule R4b).
- **OPEN-2, Stage C after a β-affecting DEFECT_FOUND. CLOSED.** A defect affecting the designed β values stops the registered check and goes to the owner as a defect report (R-X6ZC-6; §10). A corrected Stage C would be a new frozen plan.
- **OPEN-3, X6ZC_MASTER. CLOSED.** Seed master 2026102670, checked for freshness before freeze (§5); replaced by a documented value only if it collides.
- **OPEN-4, module split. CLOSED.** If `x6zc_core.py` would exceed 400 lines, the descriptive functions (A-audit, B3–B7, D2, D3) move to `tools/x6zc/x6zc_census.py`, with no scientific change.
- **OPEN-5, W1 loop-sign variant paths (§3.1 table). CLOSED.** The writer's paths stand; the result-blind reviewer verified all eight. K0 still verifies them exactly before any model runs.

## 18. Owner questions (plain language; defaults)

1. **Go-ahead in two steps.**
   - (a) Build the check now and run its rehearsal on made-up data. It uses no project data and about 0.2 CPU-hours.
   - (b) After the plan is frozen and reviewed, run the real check under the adaptive budget: about 2.8 CPU-hours at the base size, about 3.7 if the larger sample is needed. The coordinator pauses and reports if use passes three times the estimate (about 8 to 11 CPU-hours). No training, no cloud.
   - *Default: yes to both; (b) asked again after the freeze.*
2. **Positive control.** Also run the four models trained on the order-sensitive world on the new mirrored histories, as a check that the new test recognises real order use. *Default: yes; descriptive; it cannot change the stage-1 result.*
3. **Too few unused starting segments (fewer than 512; unlikely, about 2,000 or more expected).** *Default: run on what there is and report "not enough data". Do not draw new ones from the world simulator.*
4. **A bug in the frozen stage-1 code.** *Default: the owner decides whether the stage-1 correction rule applies, after a written report; until then the stage-1 result stays as registered.*

The choice between "does any order sensitivity exist?" and "is order used at a meaningful size?" is not asked now. It comes back after this finding (addendum 25 item 3).

## 19. Provenance

**Inputs (sha256 prefix):**
- request 0edfac06…;
- track L 36ff66cd… (STATUS FREEZE_READY);
- track X 7e5f04b2… (STATUS DRAFT);
- comparison 2317743e…;
- MERGE 7fcc59c8…;
- X6S1-FROZEN-v1 2a909ace…, with coordinator addenda 1–5 (footprint and bindings; no scientific change);
- jobs 0093–0099 (reports and reviews of 0097–0099 read);
- owner addenda 25–27.

**Code.** Read with Read/Grep/shell text tools at b67f332. The code index (`docs/code_index/files/tools/x6_stage1/*.md`) was used for line numbers, and every cited line was checked in the source. `git diff 213d1e2 b67f332` over the import closure is empty, and 213d1e2 is an ancestor of b67f332.

**Store, read at planning time (JSON and metadata only):**
- the 16 `designed.json`, `stages/E3z/report.json`, `stages/E3w5/ZC-s1/chunk.json`, `cloud/ADMITTED/*.json`;
- `pools/POOLS.json` (prefix, train entries), `stages/E0/record.json` (designed, SCORE tables and init digests), `STAGES.jsonl` and `EVALUATIONS.jsonl` (kinds);
- directory listings of the store (names only, including the names of the five files under `sealed/`);
- sha256 of four JSON files (`E3z/report.json`, `POOLS.json`, `FREEZE.json`, `AUTH.json`).

**Not opened or hashed:** any payload (`*.npz`, `*.npy`, `*.pt`, ObservationSets), any file under `sealed/`, and the public research summary.

**Disclosures.**
- Track L ran one `python -c` JSON parse, and the comparison analyst ran `python -c "print(1)"` (recorded in MERGE).
- **This writer inadvertently invoked `.venv/Scripts/python.exe --version` once,** inside a shell line meant for text tools. It printed only the interpreter version, with no script, project code, data or store access, and the output was discarded. No other Python, test, sampling or model run. No git writes. The only file written is this one.

## 20. Changes from track L

1. **Code base (R-X6ZC-1, MD-2):** branch from 1dc9749 or later instead of 213d1e2. The A1 item-6 empty-diff gate is kept, with the full import-closure path list. Citations are at b67f332.
2. **W1 added throughout (R-X6ZC-2):**
   - the question (§1); stored β_W1 for all 16 and the M0 contradiction (§2);
   - W1 geometry and variants (§3.1); the pattern account (§3.3); explanation (b5);
   - K0–K3 on W1; Stage-B per-cue β_W1 and ρ_W1;
   - registered cells S3 and S4 with the NOT_NA_DIRECTION label; the cell-P cross-family qualifier;
   - K6 for W1; W1 in the reuse verdict.
3. **Corrected citations (R-X6ZC-3):**
   - `_SEAM` 99–100 (`seam_labels` 103–107); S3 constants 57–58;
   - `eval` +1 shift (`ModelPredictor` 67–114, `_run` 105–114, `OraclePredictor` 129–139, `qstar` 147–154, `cue_normalise` 205–211, `pair_terms` 214–217, `designed_stats` 274–304, cosine lines 281–294);
   - `eval_chunk` 438–479 with the oracle call at 455;
   - `witness_path` W1 at `exact:98–99`.
4. **M1 coefficient:** κ stated as the point-law excess (0.7193 on W2); 1.079 noted for the "ZC-answer mass" reading.
5. "Unlike the other seven commutative controls" is now restricted to W2.
6. **Ladder order:** G-R0 (K0 → STOP_REPLAN) first.
7. **PREFIX_SPECIFIC renamed** ZC_NOT_COMMUTATIVE/NOT_REPLICATED, with X's licence. ESTIMATOR_ARTIFACT is kept only as NON_INVARIANT.
8. **R6/R7 restructured** so that R7 carries the addendum-25 rule-6 "positive but below margin" licence. PARTIAL has its own wording. R7b (unstable ratio) is placed explicitly. R8 no longer requires F1.
9. **B1/K4 tiers fixed:** ≤ 1e-9 → ENV_DRIFT; > 1e-9 → DEFECT_CANDIDATE; IRREPRODUCIBLE only without a cause.
10. **G1 (R-X6ZC-4):** variance assumptions V1–V3 stated; power-only role made explicit; secondary-cell z; 512 floor with NOT_ENOUGH_DATA and no new sampling (L's owner option (a), new sampling, removed); UNDERPOWERED handling (OPEN-1).
11. **Budget:** forecasts updated for W1 (central 2.75 CPU-h at n = 1,024, up from 1.85). 3× pause points given in CPU-s, cumulative and per stage, for both G1 branches and any n. The pre-freeze calibration rule is stated.
12. **A4** restricted to 7 train pools (MD-7).
13. **Input-artefact list** with paths and identities; `sealed/` confirmation (R-X6ZC-4).
14. **Stage-1 store no-write check** by metadata inventory instead of `store_lineage`, which hashes payloads.
15. L's "new token strings" claim for fresh PP histories corrected (repeated short prefixes), with a sensitivity line.
16. **Track X imports:**
    - the E8 architecture premise;
    - the per-pair stored-array audit (content-based identity);
    - the matched-key analytic predictor;
    - K5 items (g)–(j) and the Fraction reference;
    - D2 (identity, β_fixed, READOUT_AMPLIFIED) and D3 (weighting summaries, sensitivity qualifiers);
    - B10 float32 (PRECISION_SENSITIVE);
    - the numerical-rules table;
    - ORIGIN_UNRESOLVED and the proximate/origin split;
    - the Stage-B descriptive tier;
    - the two-axis reuse verdict;
    - X's dry-run fixtures.
17. **Known-cases-first order** in Stage B (inits, AB, other ZC, NA, then the focal models).
18. **Authorisation (R-X6ZC-5)** in two owner steps; the dry run is no longer treated as covered by planning.
19. **Defect path (R-X6ZC-6):** the owner decides on X6S1's correction route; a β-affecting defect stops Stage C (OPEN-2); other defects become a qualifier.
20. **Footprint (MD-8):** `X6ZC-FROZEN-v1.md` plus `tools/x6zc/PROTOCOL_X6ZC_v1.md`; optional census module (OPEN-4); worktree meter binding noted.
21. Owner questions updated (§18), and the deviation disclosures recorded (§19).

## Change log v1 → v2

All RC-1..RC-12 accepted by the coordinator (rulings file) and applied with the reviewer's text verbatim; OPEN-1..5 folded in and closed. Nothing else changed except the status line and the title line (header: "MERGED v2, design freeze candidate (pending confirmation)"; title renamed v2).

**RC-1 (MAJOR).**
- §9.1 per-cell table: R8 replaced by "hi(r_MM) < 0 (the r_MM interval lies entirely below 0)" with outcomes ZC_NOT_COMMUTATIVE/ZC_COORDINATE (P) and ZC_NOT_COMMUTATIVE/NOT_NA_DIRECTION (S3, S4). New row R8b: "Not R8, and for at least one v the r_v interval lies entirely outside [0.5, 1.5]" → UNEXPLAINED/NOT_NA_INVARIANT, same for both columns. The bullet "R8 and F1" renamed "R8, R8b and F1" with an added sentence that only the r_MM sign reversal earns the Z₃ licence.
- §9.3: ZC_COORDINATE licence "changes [sign/size] relative to the NA oracle's contrast (r_MM = [ ], r_PM = [ ], r_MP = [ ], intervals [ ])" replaced by "reverses sign (r_MM = [ ], interval below 0) relative to the NA oracle's contrast (r_PM = [ ], r_MP = [ ], intervals [ ])". New licence row UNEXPLAINED/NOT_NA_INVARIANT with the reviewer's sentence and not-licensed list. The generic UNEXPLAINED/ row notes that NOT_NA_INVARIANT has its own row.
- §9.4: "NOT_NA_INVARIANT lists 1–3" added.
- §12: fixture "r_PM interval above 1.5 with r_MM ≈ 1 → UNEXPLAINED/NOT_NA_INVARIANT" added.

**RC-2 (MAJOR).**
- §3.1 W1 variants: bullet inserted after the OPEN-5 bullet ("The W1 variants differ from W1 in where the crossings and the differing vertex sit: tails 4/2/3/3 tokens and crossing steps 3–4/5–6/4–5/4–5 (PP/MM/PM/MP); no n = 7 adjacent-corner MM path keeps a 4-token tail. On W1 only a sign reversal is diagnostic; ratio sizes are not interpreted.").
- K0 item 4 (W1): "the shared tail and crossing steps must equal those values (tails 4/2/3/3 … for PP/MM/PM/MP)" appended.
- §9.3 NOT_NA_DIRECTION licence: "changes [sign/size] under loop-sign reversal (r_v [ ])" replaced by "reverses sign when both crossings are reversed (r_MM = [ ], interval below 0)". "The four NA models' W1 r_v values are printed beside the cell." added to it and to the NA_DIRECTION licence (stated for the W1 cells S3 and S4).

**RC-3.** §15 step 2 replaced by the reviewer's text (clean-context Claude reviewer, rule 5, addendum 28; design freeze candidate, not the execution freeze). Step 4 appended with "the implementation commit hash and the sha256 of the dry-run report and its stage records".

**RC-4.** §9.1, paragraph added below the global-rule table (after G-R3, the row following G-R2′): the reviewer's setup-error text, verbatim.

**RC-5.** §13 G2 extended with the reviewer's two sentences (no Stage-C statistic displayed until every chunk completes; rerun only while none exists, else INVALID).

**RC-6.** §9.4 two sentences added after the axis-2 table: NA_DIRECTION at cell P gives UNDETERMINED and takes precedence over FIT_WITH_AMENDMENT; amendments are the union over cells P, S3, S4.

**RC-7.** §9.3 ZC_COORDINATE licence: "unlike the other seven commutative controls on W2" replaced by "unlike [k] of the other seven commutative controls on W2 (|β_W2,PP^fresh| ≤ 0.10; any exception named)".

**RC-8.** §9.2 fourth bullet appended: "No sentence may state or imply what ordD(s1), rule 8 or the stage-1 outcome would have been without the ZC-s1 placebo failure."

**RC-9.** B9 (§7), new bullet after the Choice block: replication feasibility |β_D|/0.10 = 2.09 (P), 1.33 (S3), 2.18 (S4), S3 carries LOW_FEASIBILITY(S3). §1 Fixed: "Working rule 2 (learning pilot) does not apply: no training."

**RC-10.** §12 Setup: bullet "Dry-run sizes" (64 prefixes of synthetic D, n = 128 fresh synthetic prefixes; analytic and planted predictors full size). UNSTABLE_RATIO fixture appended with the bimodal-draw plant.

**RC-11.** K0 item 3: the missed-crossing sentence replaced by "The missed-crossing laws are point_law(n + 1, g[y]), with g the ZC holonomy of the segment after the named crossing's label is replaced by e (`model:186–190`, `242–247`). No new history is built."

**RC-12.** (a) §5: "X6ZC_MASTER = 2026102670 (OPEN-3 ruling; freshness checked before freeze)." (b) §4.3: "…built on one of D's 1,030 prefix rows, ever (fresh rows equal by value to a D prefix: §4.2)". (c) §3.1 "Why AB cancels": parenthesis replaced by "per-cue projections (−½, +½, 0)·(π_a − π_b), since a·2 = 2; the h_last pattern (½, −1, ½) is a different known case".

**OPEN-1.** §7 B9 Choice bullet ("Default (OPEN-1)…" replaced by the ruling text) and §17 (closed). **OPEN-2.** §10 Effect bullet and §17. **OPEN-3.** §5 and §17. **OPEN-4.** §14 New-code bullet ("closed: coordinator ruling") and §17. **OPEN-5.** §3.1 bullet ("closed: the paths stand; the result-blind reviewer verified all eight") and §17. §17 heading changed to "Open items (all closed by coordinator rulings, 2026-10-26)"; each item rewritten as a closed ruling.

**Codex references.** The only named Codex reviewer for later steps was §15 step 2 (see RC-3). No other Codex mention existed in v1.

## Confirmation and design freeze candidate (coordinator 243a611b, 2026-10-26)

- Claude result-blind confirmation of v2 (`coord-x6zc-review-20261026.v2confirm.claude-reviewer.md`; Codex frozen, addendum 28): **CONFIRM_AFTER_MINOR_FIXES**; RC-1..RC-12 applied; writer placements accepted.
- N-1 (F1 list, R8 route) and N-2 (mixed-response dry-run fixture) applied verbatim by the coordinator. No other change from v2.
- This document is the **X6ZC design freeze candidate (X6ZC-DESIGN-v1)**. The final execution freeze binds the implementation hash and the accepted dry-run report, after a separate owner AUTH for implementation, tests and synthetic-only dry runs. The real stages need a later owner AUTH.
