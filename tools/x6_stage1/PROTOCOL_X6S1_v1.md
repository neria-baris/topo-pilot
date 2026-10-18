STATUS: FROZEN (X6S1-FROZEN-v1, 2026-10-18; coordinator 75dcd488; dual-track X+L, merge analysis, MERGE MD 1-18, Codex review coord-x6s1-review-20261018 + v2 confirmation CONFIRM_FOR_FREEZE; v2 = X6S1-MERGED-v2 sha256 EFE57F10…AAAC)

# X6S1-MERGED-v2: X6 stage 1 — do small causal transformers trained on natural NA histories use order-dependent (non-commutative) history information? (training on the Colab free-tier GPU, every outcome-bearing evaluation local on CPU in float64)

| Field | Value |
|---|---|
| Protocol id | X6S1-MERGED-v2. Seed and data scope tag `x6s1` |
| Role | Protocol writer (W) for the merged protocol of the dual-track round `coord-x6-stage1-20261018` (PLANNING_PROTOCOL.md); v2 is the fix round after the Codex result-blind review of v1 (§19). Planning only: no training, no sampling, no test run, no repository code run, no payload opened (`*.npz`, `*.pt`, store payloads), no git write. Committed code read with `git -C X:/Downloads/projects/topo-pilot/topo-pilot show 727af56:<path>` only; the main working tree's uncommitted edits (including `docs/proposals/D2A_RUNTIME_MAINTENANCE_V1.md` and `tools/d2a/process_tree.py`) were **not** read and nothing here depends on their text. Two files written: this one and `X6S1-MERGED-v2.sha256`. v1 is left untouched |
| Date | 2026-10-18 |
| Review applied (v1→v2) | `planning/responses/coord-x6s1-review-20261018.codex.md` (sha256 `05EB068F39D46FDC056352966C99A008019A83C5E32810F2F0F3B15C7A5A4D6A`), the Codex result-blind review of X6S1-MERGED-v1 (sha256 `BBB3387AF7BEFAEDE3A0B18FA947E0475C1C0FB2B5517BB97D40322D4F5EA03A`): VERDICT APPROVE_WITH_REQUIRED_CHANGES; required changes RC1–RC14 (cited **RC n**); open-item recommendations; four optional suggestions (cited **OS n**). Rulings `…/coord-x6s1-review-20261018.rulings.md` (sha256 `21C19693DD83687EB0F9174A916B844EFB1213D40C6B076CBE3924D7F3AA588B`; cited **RU**): every RC adopted as written; O-0…O-16 resolved; all four OS adopted. The empirical-Bernstein theorem and its constants were verified (RU O-10). Mapping in §19 |
| Dispatch | Coordinator Claude 75dcd488. The owner's writer hold (addendum 14) was released by **owner addendum 16** (sha256 `C87DCFCBDF2DA341B17D36DFB1C74C6E46648B7A9A05ECABD6CBE75E40F2779B`): "start the exact protocol and everything required for the cloud run". Training itself remains unauthorised until the owner authorises the frozen protocol's sha256 and budget (§8 AUTH) |
| Authority | Owner addendum 12 (stage-1 planning approved; no training authorised), **addendum 13** (30,000 updates × 2²⁰ histories per model; NA, AB, ZC × 4 seeds = 12 models; empirical Bernstein at N = 2²¹ per arm for the log-loss claims), **addendum 14** (training on Google's free cloud GPU, Colab free tier; evaluation local, float64, from hashed weights). OWNER_DECISIONS.v1-a73c869 and addenda 3, 5, 9, 10, 11. sha256: addendum 12 `23EBF7D3…0542`, 13 `7922ADC7…7220`, 14 `E7B98D81…49BA` |
| Binding decisions | `planning/responses/coord-x6-stage1-20261018.MERGE.md` (sha256 `E49D44BF…F451`), decisions MD 1–18, followed exactly (map below) |
| Analysis | `…/coord-x6-stage1-20261018.MERGE_ANALYSIS.md` (sha256 `6E7AB992…B629`), conflicts D1–D16 and corrections X-E1…X-E6, L-E1…L-E6 (cited **AN §n**, **D n**) |
| Tracks | Base design: track L `…claude.md` (sha256 `4A105428…B6B5`, cited **L§n**). Grafts: track X `…codex.md` (sha256 `8EFE0521…AF7`, cited **X§n**) |
| Request | `planning/requests/coord-x6-stage1-20261018.md`, sha256 `1D567D297F0AAB8946A2D98708043F189C508E00283473100C67A065ACB8E401` (re-hashed by W; equals its `.sha256` record) |
| Stage-0 references | `X6-FROZEN-v1.md` sha256 `61DDA37BF5B23648894440B4016F80191C56B6626F04CD2D5A4178D46EF2B572` (cited **S0§n**), its coordinator addendum 1 (sha256 `7352828C…9C30`; rulings X5, X5′), `jobs/0066/review.md` (sha256 `8DB32AD0…DAF9`; GO_X6_NATURAL) and `jobs/0066/report.md` (G6 table, stage-0 artifact hashes) |
| Style references | `K4B-FROZEN-v1.md` (sha256 `957F0D5E…B485`): §5.6 tolerance table, §11.4 test authors, §11.8 rerun rule; `X6-FROZEN-v1.md` §8.7, §10.8 |
| Code read at 727af56 | `src/topo_pilot/learner/{trainer.py, config.py, stage.py, __init__.py}`; `src/topo_pilot/dataset/{public.py, checks.py}`; `src/topo_pilot/contracts/{_schemas_data.py, ids.py}`; `tools/x6_stage0/API.md` (function list); `tools/d2a/d2a_train.py` (`Limits`, `Supervisor`, `admit`, `bind_meter`, `_set_threads`, `wave_main`, `_launch`); `tools/k4b/k4b_registry.py` (`inventory`, `validate_handoff_json`, `load`), `tools/k4b/k4b_registry_k.py` (`source_k`), `tools/c1prime_registry/c1_registry_sources.py` (`handoff_sources`); `src/topo_pilot/analysis/x5_context.py::percentile_interval`; `tools/x4_oracle_profile/winjob.py` (`MEMORY_CAP = 8 GiB`). Local venv library versions read from directory names only: Python 3.10, numpy 2.2.6, torch 2.14.1+cpu |
| Arithmetic | Hand values are marked **[W]** (awk desk calculation in W's scratchpad; floating point); forecasts are marked **[H]**. **No [W] or [H] value is a gate**: every gated quantity is computed by the run. Inherited values carry their source (S0, L, X, AN) |
| Next step | Codex confirmation (resume of the review thread); freeze; owner authorisation addendum (frozen sha256, local and cloud forecast, smoke and preflight work, transfers, owner sessions, account access and free-tier use; §8 AUTH, §17 O-3) before any E0 execution or training, including the cloud smoke |

**MD → section map (MERGE.md decisions, followed exactly).**

| MD | Decision (short) | Where |
|---|---|---|
| 1 | L's architecture and module split as base, X's additions | §2, §4, §14 |
| 2 | C-ORD (β_ord across seeds) primary; SHARP a per-seed claim and qualifier; X's 0.75·G_safe secondary target with GAIN_BELOW_REGISTERED_TARGET; n ≥ 8 restriction stated (J_8 = 3.72e-5, 1.4 %) | §2.3, §2.4, §3, §11 |
| 3 | L's gate UB_0.975(Δ_nat) < G_8 on NA, sealed; X's HEADROOM pre-check and γ sealed descriptive; no CONTROL_NOT_LEARNED stop; corrected pass wording | §4.7, §2.8, §3 row 2 |
| 4 | 30,000 updates on 2²⁰ histories; NA/AB/ZC × 4, identical init and batch order per seed; pilot NA-s1, NA-s2 (gate) + ZC-s1 (descriptive); order-blind learning-curve record | §4.1–§4.5 |
| 5 | Controls are placebos, subtracted as max(init, mean AB, mean ZC) inside the resampling; placebo failure → CONTROL_LIMITED or INCONCLUSIVE, never PIPELINE_INVALID; abelian learnedness a qualifier; per-seed matched C_s reported | §2.7, §7.9, §11 |
| 6 | X's quantised, ε-smoothed readout is the registered predictor of every log-loss statistic, from a float64 forward; raw values descriptive | §2.2 |
| 7 | Log-loss claims by empirical Bernstein at N = 2²¹ per arm, exact bound and constants derived here; C-ORD by bootstrap with a registered tail diagnostic; fixed family, Bonferroni before data | §7.2–§7.5 |
| 8 | X6-scoped registry: stage-0 regenerated identity-only, handoff JSON, K-REG2 and reader k as foreign alarm, collision → FAIL_TECHNICAL with no replacement, **no sealed-D-2a predicate** (stated departure), ID-reuse and cross-process diagnostics reported, G_safe = G0⁻ | §6.4–§6.6, §7.1 |
| 9 | L's natural prefixes + the 6 stage-0 prefixes, readout t = L + 18; W2 rule β_W2 ≥ 0.25 ∧ R_W2 ≤ 0.75·Δ_W2 ∧ per-cue β ≥ 0.25; both ρ_spur checks | §2.5, §6.3 |
| 10 | L's ORDER_* taxonomy + X's GAIN_BELOW_REGISTERED_TARGET, CONTROL_LIMITED, READOUT_LIMITED as qualifiers; union of never-licensed lists | §3, §11 |
| 11 | 6 threads; 3 GiB per process (shown to fit); CPU measure-only; L's guard and alarm are owner questions; 12 h wall or chunked evaluation; output cap scaled | §13, §17 |
| 12 | Exact compute forecast; authorisation is the owner's | §13 |
| 13 | L's split, 2,600–3,200 planned lines, two pre-allowlisted overflow modules (registry; stats), ≤ 400 lines each, test authors A/B | §14 |
| 14 | X's outward bounds and certified constants for the Bernstein claim; L's 1e-9 band for designed comparisons | §7.4, §7.8, §10.2 |
| 15 | L's sealing (gate Δ values sealed; only PASS/FAIL/UNRESOLVED released) | §4.7, §8 |
| 16 | X's AUTH/RUNTIME binding + L's RUNTIME-ACCT smoke wave in PF; D-2a launcher repair committed, frozen, bound by hash before execution | §4.6, §8, §15 |
| 17 | Tolerance table; oracle-scale check; rerun/lineage rule; scratch outside root; post-data change needs the owner | §10, §12, §13 |
| 18 | Errors X-E*, L-E* corrected as the analysis states | §18 |
| Add. 14 | Cloud training execution (Colab free tier) | **§5** (dedicated), §8, §9, §11, §12, §14 |
| Review | RC1–RC14, O-0…O-16, OS 1–4 (v1→v2) | **§19** |

---

## Summary (≤ 300 words)

**Question.** Do small causal transformers trained only by next-symbol prediction on X6's natural NA histories (S₃ local system, 3-cycle flux, η = 1/50) make predictions that depend on the **order** of seam crossings, beyond the registered R_Parikh statistic of directed seam-crossing counts and its coarsenings?

**Design.** The pilot TransformerLM (4 × 128, 802,304 parameters), the default recipe (AdamW 1e-3, warmup 200, cosine, batch 128), 30,000 updates on 2²⁰ fresh histories per model. NA, AB and ZC × 4 seeds (12 models), identical initialisation and batch order per seed.

**Execution.** Training runs on the Colab free-tier GPU in resumable 1,000-update chunks (model, optimiser and RNG state); the batch sequence is seeded, device-independent and verified chunk by chunk. Weights are hashed and transferred; four integrity gates (WEIGHTS-HASH, CLOUD-PROV, DATA-ID, TRAIN-COMPLETE) run locally. Every outcome-bearing evaluation runs locally on CPU in float64.

**Primary estimand.** The within-Parikh-class order slope β_ord at t = 32: each test history is paired with an exact uniform draw from its own class (same prefix, cue, age, end vertex and directed crossing counts). Every Parikh function scores exactly 0, every function of the last 8 symbols 0 in expectation, the oracle 1. Control-adjusted by step-0 and abelian models; C-ORD across seeds.

**Log-loss claims.** SHARP (excess log-loss below G_Parikh(32) = 2.636e-3) and a secondary 25 %-recovery target, by a fully derived empirical-Bernstein bound on the bounded readout at 2²¹ rows. Designed W2 (bag- and bigram-matched) alignment and regret.

**Gate.** Before any outcome: an NA model must beat the exact window-8 Bayes gap G_8 = 8.855e-3; otherwise NOT_LEARNED and stop.

**Cost.** Local ≈ 43 CPU-h (range 23–70) measure-only; cloud ≈ 1–4 GPU-h.

**Prerequisites.** Committed D-2a launcher repair bound by hash; review; freeze; owner authorisation.

---

## 0. Notation and conventions

Everything from S0§0 is kept: vertices i = 4x + y, anchor a★ = 10, N(a★) = {6, 9, 11, 14}, tokens 0..14 (vertices) and 15 + x (cue), V = 18, λ_m = (49/50)^m, μ_m(z) = λ_m δ_z + (1 − λ_m) u, q*_t, seam letters, κ (Parikh vector), R_S keys (`x6_exact.rs_key`), emit-then-transition, stationary start.

| Symbol | Meaning |
|---|---|
| m | A predictor: a model checkpoint evaluated as in §2.2, or an oracle reference (q*, q_S, q_8, heuristics) |
| p̂_t(h) | **Raw predictor**: float64 softmax of the logits at position p = t (input [BOS, w_1..w_32]), the law of w_{t+1} |
| p^Q_t(h) | **Quantised readout** of p̂_t(h) (§2.2); the registered predictor of every log-loss statistic |
| q_c | Cue-normalised law (entries 15..17 renormalised) |
| R_ord(t) | Rows with a cue in w_{1:t}, age n = t − s ≥ 8, v_t ∈ N(a★) |
| h′ | Class partner of h (§2.3) |
| Δq̂, Δq* | p̂_c(h) − p̂_c(h′) and q*_c(h) − q*_c(h′); Δp_{m,c} (§2.3, RC2) is Δq̂ for predictor m |
| X_i(m) | KL(q*_32(H_i) ‖ p^Q_32(H_i)), the per-row excess log-loss of m's quantised readout |
| Δ_nat(m) | E X(m): natural excess log-loss at t = 32 (full vocabulary) |
| NA-s, AB-s, ZC-s, init(s) | Arm-a model of seed s ∈ {1,2,3,4}; init(s) is the shared step-0 state |
| G0⁻ | Lower endpoint of the certified stage-0 enclosure of G_Parikh(32) (0.0026358964806790516…); G_8.lo likewise for G_8(32) |
| U_δ(m) | Empirical-Bernstein upper confidence bound of Δ_nat(m) at level 1 − δ (§7.3–§7.4) |
| UB_γ, LB_γ | One-sided bootstrap bounds at level γ |
| K | Cloud checkpoint interval, 1,000 updates |
| H, R, P | Execution commit, reviewed reference commit, D-2a repair commit (§14.5, §15) |

---

## 1. Question, competing explanations, scope

### 1.1 Question
Stage 0 proved that order information is predictively available in this process; it did not establish learnability by the registered neural recipe: G_Parikh(32) = 2.6359e-3 nats (certified), M_32(0.01) = 0.0468, designed witnesses W1/W2/W3 (cue-normalised TVs 0.851, 0.695, 0.524), exact zeros in AB and ZC (jobs/0066). Stage 1 asks whether trained next-symbol models **use** it: whether their predictions vary with the composition order of seam crossings, in the oracle's direction, on fresh histories. This is a behavioural claim, not a mechanistic or representational one.

### 1.2 Competing explanations and the observations that separate them (L§1.2, X§2)

| Explanation for an apparent order effect, or for its absence | Discriminating observation |
|---|---|
| E-artifact: pipeline or positional artifact | Abelian-trained and step-0 placebos on the same NA pairs and designed sets (§2.7); oracle positive controls (β(q*) = 1, β(q_Parikh) = 0, Δ(q*) ≤ readout floor) |
| E-short: the last ≤ 8 symbols | Restriction to n ≥ 8 with Lemma P2 (§2.3); the gate requires Δ_nat < G_8 |
| E-comm: a function of the Parikh vector (or parity, counts, H1) | Partners share the R_Parikh key, so the pair term is exactly 0 (Lemma P1); SHARP (Δ_nat < G_Parikh) |
| E-bag: the segment's token or bigram bag | **Not** excluded on natural pairs. Excluded on designed W2 (bag- and bigram-matched, S0 Theorem 5) |
| E-heuristic: first or last crossing letter | W2 pooled β = 0 for both (S0§4.9); natural reference β reported |
| E-reverse: reversed composition | W2 β = −1 |
| E-noise: spurious order sensitivity | ρ_spur on commuting control sets C1–C4 (NA model) and on W2 (abelian models); natural spurious ratio |
| E-coset: parity quotient S₃/A₃ only | Pairs share parity, so β = 0; ladder rung reported |
| E-block: order-blind aggregate of 8-block evidence | Ladder rung against D_blk(32) = 1.30972e-3. **The literal PoE comparator is not used** (TRIV ≈ 19 se above 0 at stage 0) |
| A-not-learned: the recipe does not learn long-range transport | Learnability gate (§4.7), decided before any order statistic exists |
| A-transfer: a cloud/transfer artifact (wrong weights, wrong data, broken chain) | Integrity gates WEIGHTS-HASH, CLOUD-PROV, DATA-ID, TRAIN-COMPLETE (§5.8), all before any evaluation of the model |

### 1.3 Scope
- One frozen process (S0§2, NA at η = 1/50); AB and ZC only as controls; TRIV not trained.
- One architecture and one recipe, no search, no tuning.
- Behaviour only: no probes, activations, interventions or PH.
- No frozen result is reopened (X6 stage 0, D-2a, K4b, C1′).
- Causal use (charter priority 2) is **not** addressed.
- **Training reproducibility is not claimed** (GPU non-determinism is accepted for training only, addendum 14). What is reproducible is the training data, the batch sequence, the initial state, and every evaluation from the hashed weights.

---

## 2. Estimands, registered predictors, success criteria

### 2.1 Oracle anchors (stage 0; certified enclosures of width ≈ 2e-60 unless marked)

| Quantity at t = 32 (NA) | Value | Role |
|---|---|---|
| G_8(32) | 8.85531e-3 | Learnability threshold; identical in NA, AB, ZC (S0 T11′) |
| G_∅ / G_parity / G_H1 / G_counts | 1.05935e-2 / 7.7918e-3 / 2.9868e-3 / 2.7360e-3 | Ladder rungs (descriptive) |
| **G_Parikh(32)** (G0⁻ = its lo) | **2.6358965e-3** | SHARP threshold; G_safe = G0⁻ (MD 8, §7.1) |
| (3/4)·G0⁻ | ≈ 1.9769223605e-3 [W] (exact rational product of the full endpoint) | TARGET threshold (secondary, MD 2) |
| D_blk(32) | 1.30972e-3 | Ladder rung (descriptive) |
| J_8(32) | 3.7201925132837e-5 (1.41 % of G_Parikh) | Mass excluded by the n ≥ 8 restriction (MD 2) |
| G_Parikh(32) on n ≥ 8 | ≈ 2.59869456e-3 [W, L App. A; AN D1; RC review] | Share kept 98.6 % |
| Δ_challenge = Δ_W3 (W3, 24 orderings) | ≈ 0.0378320848 (lo: Δ_W3^lo) | Designed qualifier |
| W2 set gap Δ_W2 | ≈ 0.0611193713 (lo: Δ_W2^lo) | W2 regret bar (3/4)·Δ_W2^lo ≈ 0.0458395285 [W] |
| λ_18, λ_32 | 0.6951353, 0.5238831 | Oracle TVs; 2λ_18² = 0.96643 [W] |

Displayed decimals are explanatory approximations and are never binding comparison inputs. `API.md` freezes a constant map giving each authoritative stage-0 JSON path and its complete Decimal string or enclosure. S0 verifies the stage-0 report hash and exact equality with those strings. Rebuilt constants are checked using T6. Derived thresholds use exact rational multiplication of the full certified endpoints, without intermediate rounding.

Define Δ_W2^lo and Δ_W3^lo as certified lower endpoints of the stage-0 W2 set gap and W3 challenge gap. G0-ORC reconstructs their enclosures from the unchanged exact laws and Decimal method. Their central values are approximately:

  Δ_W2 = 0.061119371341896547955524807971231695289846551087376421303896009064819738013445345,

  Δ_W3 = 0.037832084794304540254080229574490474113844007878061695581602399097047383150353710.

Desk values for the natural pairing (L App. A [W], t = 32): P(R_ord) = 0.095207; P(Δq* ≠ 0) = 0.022797; E‖Δq*‖² = 0.0194791 per row; E‖Δq*‖⁴ = 0.0177479 per row.

### 2.2 Registered predictors (MD 6; D6)

**Model evaluation (every outcome-bearing evaluation; addendum 14).**
- The step-30,000 weights of each model are the float32 tensors of its verified final cloud checkpoint (§5.5), identified by their canonical weights digest. They are loaded locally on CPU (`learner.stage.load_model` on an in-memory `Checkpoint` built from the verified file), **cast to float64** (`model.double()`), and run in eval mode under `torch.no_grad()` with 2 intra-op threads, 1 inter-op thread and batch size 1,024 rows (fixed and recorded; MKL/OpenBLAS results may depend on thread count, so neither may change).
- **Local evaluation environment record (OS 3).** Every local job that evaluates a model records, in its stage record: the Python, numpy and torch versions; the BLAS/LAPACK backend and version (`numpy.show_config()`, `torch.__config__.show()`); the CPU model and core count; the intra-op and inter-op thread settings and the thread environment variables; the batch size; the worktree commit H. "Reproducible evaluation" means bit-reproducible **within this recorded environment**; DET (E3.1) checks it, and any environment change between E3 jobs is a recorded event that requires bit-identical regeneration of an overlapping chunk before continuation (§12 item 6).
- Histories shorter than 33 tokens are padded after t; causality makes positions ≤ t independent of the padding (T-EVAL tests it).
- p̂_t(h) is the float64 softmax at position t.

**Raw predictor p̂ (MD 6, L§2.7).** Used for every alignment statistic (β_ord, β_W1/W2/W3, ρ_spur, cue mass). Raw log-loss values are reported descriptively.

**Quantised readout p^Q (X§3; MD 6).** Used for every log-loss statistic (Δ_nat, SHARP, TARGET, the gate, LEARN-TEST, R_W2, Δ_W3, the ladder).
1. Input: the 18-way float64 vector s = p̂_t(h). Precondition: |Σ_j s_j − 1| ≤ 1e-12 and s_j ≥ 0 (else QUANT_INVALID, a PIPELINE_INVALID cause; T25).
2. r_j = Q·s_j with **Q = 2²⁰**; f_j = ⌊r_j⌋; R = Q − Σ_j f_j, required 0 ≤ R ≤ 18 (else QUANT_INVALID).
3. k_j = f_j + 1 for the R indices with the largest fractional parts r_j − f_j, ties broken by the lower token index; k_j = f_j otherwise. Σ_j k_j = Q exactly.
4. p^Q_j = (1 − ε)·k_j/Q + ε/18 with **ε = 10⁻⁶**, an exact rational.

Properties (exact):
- p^Q_j ≥ ε/18 for every j, so for every history 0 ≤ X = KL(q*‖p^Q) ≤ Σ_j q*_j ln(1/p^Q_j) ≤ ln(18/ε) = 16.705882 [W] < **B = 17**.
- An entry with s_j = 0 has fractional part 0 and never receives the +1 when R ≥ 1 (the R units go to entries with positive fractional part, of which there are more than R because Σ frac = R and each frac < 1), so k_j = 0.
- **Oracle-readout floor** (X§11, verified): passing q* (float64) through the same map gives, per row, KL(q*‖p^Q) ≤ −ln(1 − ε) + KL(q*‖k/Q) ≤ −ln(1 − ε) + χ²(q*‖k/Q) ≤ −ln(1 − ε) + 18/(Q²(1/750 − 1/Q)) = **1.012287e-6** [W] (1/750 is the smallest positive q* entry; p^Q ≥ (1 − ε)k/Q entrywise gives the first step; KL ≤ ln(1 + χ²) ≤ χ² the second; |k_j/Q − q*_j| < 1/Q and k_j/Q > q*_j − 1/Q the third). This is 3.8 × 10⁻⁴ of G0⁻.

The quantisation uses model outputs alone: no support masking, no oracle correction, no calibration; every arm uses the same map.

### 2.3 Natural primary: within-Parikh-class order alignment β_ord (L§2.2; MD 2)

**Partner draw (exact; genuinely new code).**
- Counts c_m(u, κ′) = Σ_g of `x6_dp.classes(layer_m, "Parikh")` from the unchanged `x6_dp.segment_dp("NA", 31)`; Python ints; label-free.
- Backward sampling for m = n…1 from v_m: predecessor u ∈ NEIGHBOURS[v_m] (the graph is symmetric and includes the stay), u ≠ a★ if m − 1 ≥ 1 and u = a★ if m − 1 = 0; κ_{m−1} = κ_m − e(seam_letter(u, v_m)); weight c_{m−1}(u, κ_{m−1}). The weights sum to c_m(v_m, κ_m) by the DP recursion.
- Each step draws `randrange(c_m(v_m, κ_m))` from `random.Random(SeedTree(DATA).seed("x6s1", "partner", pool, t, row))` and selects by cumulative weights (exact big integers). The product of step probabilities is 1/c_n(v_t, κ): **the draw is uniform over the class**.
- h′ = w_{1:s} (prefix and cue unchanged) + tok(v′_{s+1}..v′_t).
- Layer zero is the singleton anchor state (c_0(a★, 0) = 1); absent predecessor states and states with a negative count component have weight zero.
- By S0 Theorem 7 and Theorem 1, every anchor-avoiding segment of length n after a given w_{1:s} has the same probability P(w_{1:s})·5⁻ⁿ (the segment emits no cue). Hence, given the class, h is uniform and h′ is an independent uniform draw: (h, h′) is exchangeable and **h′ has the natural marginal law on the registered eligibility domain R_ord** (the partner transformation is defined only there).

**Population estimand.** For a fixed predictor m, let A_m = 1_{R_ord}⟨Δp_{m,c}, Δq*_c⟩ and D = 1_{R_ord}‖Δq*_c‖², under a natural history and its independently sampled uniform class partner. Define β_ord(m) = E[A_m]/E[D]. The displayed ratio of sample sums estimates this population ratio. Population control adjustment applies the registered maximum to the population slopes; each bootstrap draw applies the same maximum to the resampled slopes. Models and seeds are fixed, and only history rows are resampled.

**Statistic.** For predictor m and test rows i ∈ R_ord(32):

  β_ord(m) = Σ_i ⟨Δq̂_i, Δq*_i⟩ / Σ_i ‖Δq*_i‖².

It is `x6_exact.beta` with each pair as a set (within-pair centring halves numerator and denominator alike); the run computes it vectorised and cross-checks it against `beta` (E3.5, T7). Rows with Δq*_i = 0 contribute zero to both sums.

**Lemma P1 (exact zero for commutative predictors).** If m is a function of R_Parikh = (no-cue flag, prefix, n, y, v_t, κ), every pair term is exactly 0, because h and h′ share the key. ∎

**Lemma P2 (zero in expectation for segment-only predictors; reworded per L-E5).** Restrict to R_ord(32) (n ≥ 8). Let f depend on h only through the tokens of the segment v_{s+1..t} (in particular any function of the last 8 symbols, which lie inside the segment when n ≥ 8). By S0 Theorem 7 each (y, γ) has natural mass (1/48)·5⁻ⁿ, so under the natural law **marginally** y is uniform on {0,1,2} and independent of the segment γ; the partner γ′ is drawn given (n, v_t, κ(γ)) only, so y ⊥ (γ, γ′). Δq*_c = λ_{n+1}(δ_{ρ(γ)[y]} − δ_{ρ(γ′)[y]}) and Δf does not depend on y, hence E[⟨Δf, Δq*⟩ | γ, γ′] = (λ_{n+1}/3)⟨Δf, Σ_y(δ_{ρ[y]} − δ_{ρ′[y]})⟩ = (λ_{n+1}/3)⟨Δf, (1,1,1) − (1,1,1)⟩ = 0. ∎ The independence holds only marginally: y is **not** uniform given the prefix's earlier cues, so the lemma does **not** cover predictors that combine the window with prefix cue tokens. The exact window-8 Bayes predictor has Δq_8 = 0 on every R_ord row (S0 Theorem 4(a): no cue in the window, fibre uniform, q_8 a function of v_t).

**Normalisation.** β_ord(q*) = 1 exactly (identical numerator and denominator arrays).

**n ≥ 8 restriction (MD 2).** It removes the n ≤ 7 part of the gap, J_8(32) = 3.72019e-5 (1.41 % of G_Parikh), and makes every short-window mechanism score zero in expectation.

**Control adjustment (MD 5).** For seed s:

  ctrl(s) = max{ β_ord(init(s)), ¼Σ_{s′=1..4} β_ord(AB-s′), ¼Σ_{s′=1..4} β_ord(ZC-s′) },  β̃(s) = β_ord(NA-s) − ctrl(s),

every term on the **same NA test pairs**, the max taken inside each bootstrap draw (§7.5).

**C-ORD (primary order claim).** Supported iff mean_s β̃(s) ≥ 0.25 **and** LB_0.975(mean_s β̃(s)) > 0.05 **and** β̃(s) > 0 in ≥ 3 of the 4 seeds (§7.2).

**Per-seed matched contrast (MD 5, descriptive).** C_s = β_ord(NA-s) − max{β_ord(init(s)), β_ord(AB-s), β_ord(ZC-s)}, with a per-seed bootstrap interval.

### 2.4 Natural log-loss claims (MD 2, MD 7)

- **Pythagorean bound.** Every function of R_Parikh (or of any coarser statistic) has Δ_nat ≥ G_Parikh(32) ≥ G0⁻ (S0§5.1). If the model's softmax were a function of R_Parikh, so would its quantised readout be.
- **SHARP(s):** U_{δ_s}(NA-s) < G0⁻, δ_s = 0.025/4 = 0.00625. Licence: model NA-s's predictor is not a function of the Parikh statistic or of any coarser one (parity, counts, H1, S₃/A₃).
- **TARGET(s) (registered secondary accuracy level, X§4):** U_{δ_s}(NA-s) < (3/4)·G0⁻, computed as the exact rational product of the full certified endpoint (≈ 1.9769223605e-3 [W]; never a displayed decimal), i.e. at least 25 % of the commutative-oracle gap recovered. It uses the **same** bound U_{δ_s} as SHARP, so both claims hold on the single event {Δ_nat ≤ U} and no extra multiplicity is needed (§7.2).
- **Per-seed natural status:** TARGET_MET (TARGET holds); GAIN_BELOW_TARGET (SHARP holds, TARGET does not); NOT_CERTIFIED (SHARP fails). GAIN_BELOW_TARGET states that the target was **not certified**; it makes no claim that the true regret exceeds the target (no lower bound is computed).
- **Limit.** SHARP does not exclude bag-of-tokens mechanisms on the natural distribution.

### 2.5 Designed criteria (exact, deterministic per model; MD 9)

**Registered designed set D** (L§2.4; token hashes frozen in E0):
- *Prefixes:* the six stage-0 prefixes Π0, Π1, Π3 and Π6 with y₀ ∈ {0,1,2}, plus 1,024 natural prefixes from pool `prefix` (§6.1). For row i of the prefix pool, draw L_max ∈ {1..14} uniformly (stream ("x6s1", "prefix_len")) and take the largest L ≤ L_max with v_L ∈ N(a★) ∪ {a★}; rows with none are skipped, in row order; the first 1,024 yielding rows are used. The transition into a★ is then legal. Lexicographic prefixes are **not** used (X-E1).
- 1,030 prefixes × 3 cue values y.
- *W2:* AB versus BA (S0§4.3), readout at t = L + 18 ≤ 32: **3,090 pairs (6,180 histories)**. q* is prefix-invariant exactly (S0 Theorem 1).
- *Commuting controls C1–C4* (L§2.4): C1 = {A⁺A⁻, A⁻A⁺}, C2 = {A⁺F, FA⁺}, C3 = {B⁺B⁻, B⁻B⁺}, C4 = {B⁺F, FB⁺}, with F = (4, 8, 9, 5) the flat face loop at p = 5 (edges interior and avoiding a★; AN D9 re-checked). Within each set the token and directed-bigram multisets, κ, the tail and q* are identical. 4 × 3,090 = 12,360 control pairs.
- *W3:* the 72 canonical histories at t = 32 (16/4/4). *W3′* and *W1:* with the stage-0 prefixes (W1 also with the 1,024 natural prefixes, readout t = L + 8). Descriptive.

**Statistics (per predictor):**
- β_W2(m): `beta` over the 3,090 W2 pairs, cue-normalised raw p̂, pooled over y with equal weights; β_W2,y(m) per cue value (1,030 pairs each). Oracle reference values (exact, S0§4.9): q* 1; every matched or set-constant competitor 0; last- and first-crossing pooled 0; reversed −1.
- R_W2(m): mean over the 6,180 W2 histories of KL(q* ‖ p^Q) (full vocabulary; quantised readout). Every predictor constant on each (prefix, y) set has mean ≥ Δ_W2 = 0.061119, equality for the mixture.
- Δ_W3(m): mean over the 72 W3 histories of KL(q* ‖ p^Q). Every function of the bag, bigram bag, H1 or counts (with cue and scaffolding) has ≥ Δ_challenge = 0.0378321; reversed composition 0.05095 [W, L].
- ρ_spur^C(m) (NA models, L): mean_{C1–C4 pairs}‖Δq̂‖² / mean_{W2 pairs}‖Δq*‖² (denominator 2λ_18² = 0.96643 [W]; oracle 0).
- ρ_spur^{W2}(c) (abelian models, X§5): mean_{W2 pairs}‖Δp̂_c(c)‖² / mean_{W2 pairs}‖Δq*_NA‖² (same denominator; their own oracle within-set variance is exactly 0).

**Per-seed designed flag ordD(s).**
- *Defined* iff the NA-s designed cue mass passes (§2.6), ρ_spur^C(NA-s) ≤ 0.25, and the seed's designed placebos are valid: |β_W2(c)| ≤ 0.10 for c ∈ {init(s), AB-s, ZC-s}, and ρ_spur^{W2}(AB-s) ≤ 0.25 and ρ_spur^{W2}(ZC-s) ≤ 0.25.
- *PASS* iff β_W2(NA-s) ≥ 0.25 + 1e-9 **and** the ordD regret PASS condition R_W2(NA-s) ≤ (3/4)Δ_W2^lo − 10⁻⁹ holds **and** min_y β_W2,y(NA-s) ≥ 0.25 + 1e-9.
- *FAIL* iff β_W2 < 0.25 − 1e-9 **or** the ordD regret FAIL condition R_W2 > (3/4)Δ_W2^lo + 10⁻⁹ holds **or** min_y β_W2,y < 0.25 − 1e-9.
- Otherwise NUMERICALLY_UNRESOLVED. An undefined flag is UNRESOLVED, never FAIL; an undefined flag caused by a placebo carries CONTROL_LIMITED(designed, s).
- Every designed-result summary reports the PASS, FAIL and UNRESOLVED counts explicitly (OS 2); an unresolved designed flag is never described as a demonstrated failure.

**Designed qualifiers.** W2_GAP_BEATEN: R_W2 < Δ_W2^lo − 10⁻⁹. CHALLENGE_BEATEN: Δ_W3(m) < Δ_W3^lo − 10⁻⁹. The 1e-9 band is L's (MD 14); these are census statistics, not samples, and carry no sampling interval (X§5).

### 2.6 Readout validity (READOUT_LIMITED; L§2.5, X§5)
For each predictor: the median total raw cue mass Σ_x p̂(15 + x) over R_ord(32) test rows, and separately over the designed readouts, must be ≥ 0.10 (half the oracle's 1/5). Otherwise that predictor's order statistics on that domain are UNRESOLVED and the qualifier READOUT_LIMITED(m, domain) is attached. The check is vacuous against a uniform predictor (3/18 = 0.167; AN §6); its purpose is to catch cue suppression.

Any zero/non-finite cue normaliser or non-finite required alignment value makes that predictor's affected order contrast UNRESOLVED, even if its median cue mass passes. Rows are never dropped to restore definability.

### 2.7 Controls and placebos (MD 5)
- **Natural placebos (E3.4):** |β_ord(c)| ≤ 0.10 (point) for each of the 12 control predictors c ∈ {init(1..4), AB-1..4, ZC-1..4} on the NA test pairs. A failure attaches CONTROL_LIMITED(natural, c) and routes the natural order claim to INCONCLUSIVE (§7.9 rule 6′); it is a scientific specificity finding, never PIPELINE_INVALID (L-E3).
- **Designed placebos:** as in ordD(s) (§2.5).
- **Abelian learnedness (qualifier):** learned(AB-s), learned(ZC-s) on their own arm's test pool (E3.2), reported as CONTROLS_LEARNED(AB a/4, ZC b/4). Never a stop, never a conjunct (no CONTROL_NOT_LEARNED, MD 3).
- **Oracle positive controls (G0-POS):** β_ord(q*) = 1, β_ord(q_Parikh) = 0 exactly, Δ_nat(q* through the quantiser) ≤ the readout floor, the ladder Δ_nat(q_S) against G_S.

### 2.8 Descriptive estimands (no decision effect)
- **Ladder per seed:** U_{0.025}(Δ_nat) < G_S(32) for S ∈ {∅, parity, H1, counts, Parikh} and against D_blk (not totally ordered).
- **Length profile:** β_ord and Δ_nat at t ∈ {16, 24} on the first 2¹⁷ NA test rows (partners drawn at each t; Δ_nat(t) against stage-0 G_Parikh(t)); β_ord by age bin n ∈ 8–15, 16–23, 24–31.
- **References on the natural pairs:** β_ord of the rev, last and first heuristics (`competitor_holonomy`).
- **Natural spurious ratio:** E[‖Δq̂‖² | Δq* = 0, R_ord] / E[‖Δq*‖² | Δq* ≠ 0].
- **Abelian controls on their own processes:** within-Parikh-class spread on own-process pairs (oracle spread exactly 0).
- **Matched excess:** Δ_nat(NA-s) − Δ_own(ZC-s) beside G_Parikh (caveat: ZC needs signed counts mod 3).
- **Paired gain A_s** (X§4) = E[KL(q*‖q_Parikh) − KL(q*‖p^Q_s)] on the NA test pool; M_32-stratified results.
- **Raw values:** raw full-vocabulary β; raw log-loss; float32-versus-float64 difference.
- **Emergence:** β_ord and Δ_nat at checkpoints 1,000, 3,000, 10,000 and 20,000 on the first 2¹⁴ NA test rows (NA models).
- **γ_m (X§9, MD 3; sealed until E3):** γ_m = (β_m − β_8)/(1 − β_8), β_m = Σ⟨p̂_m − q_Parikh, d⟩/Σ‖d‖² with d = q* − q_Parikh on val(NA), β_8 the same with the exact window-8 predictor. Computed at E3 for the four NA models; never a gate (X-E3).
- **HEADROOM-D (MD 3; sealed until E3):** β_8 and mean ‖d‖² on val(NA), computed in E0 (oracle only). X's energy fraction is **not computed**: its definition and its claimed bound (≈ 0.57) were never derived (X-E4), so the claim is dropped (§18).
- **Learning-curve record** (§4.5) and **LOSS-ECHO** (§5.7).
- β_W1, β_W3 (equal weights and holonomy-balanced), β_W3′.

---

## 3. Licensed claims and non-claims

**Fixed scope of every licence:** the frozen X6 NA process (4×4 torus, S₃ local system flat on 15 faces with a 3-cycle flux, η = 1/50, base observed exactly, fibre only through anchor cues); the pilot TransformerLM (4 × 128, n_ctx 33) trained by next-symbol cross-entropy for 30,000 AdamW updates on 2²⁰ natural histories per model, on Colab GPUs (types recorded per chunk); the 4 registered NA models and 8 abelian control models; readout t = 32 inside the context. Every statement is behavioural and conditional on these registered models (their hashed weights); seed-level robustness (≥ 3 of 4) is descriptive, not a population-of-seeds inference.

| # | Outcome | Licensed sentence (brackets filled from the run) |
|---|---|---|
| 1 | INVALID / CONSTRUCTION_FAIL / FEASIBILITY_NO_GO / FAIL_TECHNICAL/LINEAGE / INCONCLUSIVE/REGISTRY_INCOMPLETE / INCOMPLETE | No statement about models. CONSTRUCTION_FAIL: the stage-1 oracle or scoring pipeline disagrees with stage 0. FEASIBILITY_NO_GO: this design cannot resolve the estimand. INCOMPLETE: the registered models could not all be trained and verified. None is a negative result |
| 2 | NOT_LEARNED | "Neither registered NA validation model's natural excess log-loss at t = 32 was credibly below the exact 8-symbol-window Bayes gap G_8(32) = 8.855e-3 nats on fresh validation histories, so neither was shown to be better than every function of the last 8 symbols (and hence not transport-blind). This recipe failed the registered learnability gate." A scoped feasibility result; not evidence that order information, or S₃ transport, is unlearnable. (The pass wording is the exact implication: "not a function of R_∅, and better than every function of the last 8 symbols", MD 3; L-E6) |
| 2b | LEARNING_UNRESOLVED | "Learnability could not be decided because a required statistic was undefined." Descriptive only |
| 3 | PIPELINE_INVALID | No conclusion from the affected analysis until a documented technical correction (no threshold change) |
| 4 | LEARNING_NOT_ROBUST | "Fewer than three of the four registered NA models met the learnability criterion on the fresh test pool; order statistics are reported per model, descriptively." |
| 5 | ORDER_USE_NATURAL_AND_DESIGNED | Natural: "On fresh natural histories, the models' next-symbol predictions at t = 32 varied between histories with identical prefix, last cue, cue age, end vertex and directed seam-crossing counts, in the direction of the exact oracle's order-dependent variation: mean control-adjusted alignment [β̄] (nominal one-sided 97.5% bootstrap lower bound [ ]; oracle 1; every function of the Parikh vector exactly 0; every function of the cue-free segment, including every function of the last 8 symbols, 0 in expectation). These models' predictors are therefore not functions of the Parikh vector or of any coarser commutative statistic of the crossing word." Designed: "On the registered AB-versus-BA family, whose members share token and directed-bigram multisets, crossing counts, H1 class and their last 8 symbols, [k ≥ 3] of the 4 models ([k] PASS, [f] FAIL, [u] UNRESOLVED) shifted their cue predictions in the oracle direction (pooled and per-cue alignment ≥ 0.25) and had full-vocabulary regret ≤ 75 % of the best set-constant predictor's. Every function of the matched statistics, first- and last-crossing rules (pooled 0) and reversed-order composition (−1) cannot do this." |
| 6 | ORDER_USE_NATURAL | The natural sentence of 5, plus: "The designed criterion had [k] PASS, [f] FAIL and [u] UNRESOLVED models and was not established in three models. A natural-distribution mechanism using segment token bags or a last-crossing rule remains possible." An unresolved designed flag must not be described as a demonstrated failure |
| 7 | ORDER_USE_DESIGNED_ONLY | The designed sentence of 5 (with its PASS/FAIL/UNRESOLVED counts), plus: "The registered natural-distribution order criterion was not met." Designed results are never presented as natural |
| 8 | ORDER_NOT_DETECTED | "The models passed the transport learnability gate, but their control-adjusted within-Parikh-class order alignment was below 0.10 in at least three of four seeds, and the registered order criteria were not met." Non-attainment by this recipe; it does not show that the models carry no order information, nor that transformers cannot learn S₃ composition |
| 9 | INCONCLUSIVE | Split seeds, an UNRESOLVED confirmatory contrast, a natural placebo failure (CONTROL_LIMITED), a failed tail diagnostic, precision failure or mixed patterns. Descriptive only |

**Qualifiers** (outcomes 4–9; never change the outcome):
- **SHARP_NATURAL(k/4):** "Model NA-s's natural excess log-loss at t = 32 was below G_Parikh(32) = 2.636e-3 nats (one-sided, distribution-free empirical-Bernstein bound at level 0.025/4, on 2²¹ fresh histories), so its predictor is not a function of the Parikh statistic or of any coarser one."
- **NATURAL_TARGET(k/4)** and **GAIN_BELOW_REGISTERED_TARGET(j/4)** (X; MD 2, MD 10): TARGET met, or SHARP met without the 25 % target being certified ("positive natural advantage established; the registered 25 % recovery target was not certified").
- **W2_GAP_BEATEN(k/4)**; **CHALLENGE_BEATEN(k/4):** "On the 24-ordering commutator family at t = 32 with orderings equally likely, model NA-s's expected excess was below 0.0378 nats, the minimum for every predictor that is a function of the token bag, bigram bag, H1 class or crossing counts."
- **CONTROL_LIMITED(domain, list)** (X; MD 5): a placebo or abelian spurious-order check failed; the corresponding matched-control interpretation is withheld.
- **READOUT_LIMITED(list)** (X; MD 10): a cue-mass check failed.
- **CONTROLS_LEARNED(AB a/4, ZC b/4)**; **LADDER(s)**; **PRECISION_LIMITED**; **DESIGNED_UNRESOLVED(k)**; **LENGTH_PROFILE**; **MIXED_DEVICE(model list)** (provenance only: a model's chunks ran on more than one GPU type); **MIXED_ENV(model list)** (provenance only: a model's sessions ran under more than one Python/numpy/torch/CUDA/cuDNN version, §5.4).

**Never licensed** (union of L§3 and X§13, MD 10, plus the cloud items):
- that a model composes S₃ internally, implements an automaton or an explicit S₃ multiplication algorithm, or represents the holonomy, the cover, the puncture, a learned sheaf or obstruction, or any representation with the topology of the torus, punctured complex or cover;
- any causal or mechanistic statement, including causal necessity of an activation coordinate (no intervention is run);
- generalisation to other η, worlds, architectures, sizes, training recipes, budgets, devices, noise rates or a population of seeds;
- exclusion of bag-of-tokens mechanisms on the natural distribution; any natural bag gap or natural lower bound for arbitrary token-bag or bigram-bag predictors;
- a reading of designed results as natural;
- absence of order information following a failed criterion;
- anything about the pilot square/cylinder question, D-2a, C1′, K4b, E4 or other frozen findings, or their revision;
- confirmation or refutation of Zhang & Li beyond "consistent with" (abstract-level source);
- any reading of the AB or ZC models as evidence about abelian learnability in general;
- the PoE comparator as an order signal;
- that training is bitwise reproducible, or that a retrained model would give the same weights (GPU non-determinism; only data, batch sequence, initial state and every evaluation are reproducible).

---

## 4. Models and training

### 4.1 Arms, runs and pairing (MD 4; addendum 13)

| Arm | Process (`x6_model.model(arm)`) | Seeds s | Models |
|---|---|---|---|
| NA | NA labels, η = 1/50, standard E | 1, 2, 3, 4 | 4 |
| AB | AB labels (a on both seams) | 1, 2, 3, 4 | 4 |
| ZC | ZC labels (c / c²) | 1, 2, 3, 4 | 4 |
| **Total** | | | **12 trained models**, plus the step-0 states init(1..4) |

"Trained identically" means: the same `ModelConfig`, the same recipe, the same data volume; for seed s every arm loads the **same initial state** init(s) and uses the **same batch-index sequence** (`SeedTree(MODEL).generator("batch_order", "x6s1", s)` over training sets of identical size 2²⁰; verified in `trainer.py` at 727af56, AN §0); arms differ only in the process generating their own training data.

### 4.2 Fixed configuration (no production change)

| Item | Value |
|---|---|
| Model | `ModelConfig(vocab_in=19, vocab_out=18)`, otherwise defaults: 4 layers, d_model 128, 4 heads, d_mlp 512, GELU, dropout 0, untied, n_ctx 33. 802,304 parameters [W, L; AN] |
| Recipe | `TrainConfig(steps=30000)` defaults: batch 128, lr 1e-3, warmup 200, cosine to 0 (`WarmupCosine`), AdamW (betas 0.9/0.999, eps 1e-8), weight decay 0.1 on `nn.Linear` weight matrices only (both embeddings, biases and LayerNorm excluded), global-norm clipping 1.0 |
| Loss | Unchanged `lm_loss`: next-symbol cross-entropy over all 33 positions. No auxiliary heads, oracle targets, curriculum, witness augmentation or cue reweighting |
| Data | train(arm, s): 2²⁰ fresh natural histories (33 symbols) from `HMMSampler(Tf, Ef, pif, SequenceLayout())`, through `ObservationSet` and `PublicTokenDataset` only; 3.84M draws with replacement = 3.66 passes [W, L]. Latent states are discarded and never stored |
| Precision on GPU | float32 throughout; no AMP; `torch.backends.cuda.matmul.allow_tf32 = False`, `torch.backends.cudnn.allow_tf32 = False`, `torch.set_float32_matmul_precision("highest")`; `torch.use_deterministic_algorithms(True, warn_only=True)` (as `Trainer.fit`) with `CUBLAS_WORKSPACE_CONFIG=:4096:8`. GPU determinism is best effort and is **not** relied on |
| Checkpoints | Every K = 1,000 updates, steps 0, 1,000, …, 30,000 (31 per model), each holding model, optimiser, scheduler and RNG state (§5.5) |
| Scientific checkpoint | 30,000 only. No early stopping, no best-checkpoint selection, no retuning. Earlier checkpoints are descriptive |

Why 30,000 updates (L§4.2; owner addendum 13): D-2a's 10,000-update recipe ended NOT_LEARNED with dev CE flat from step 1,000 (jobs/0033); here the order incentive is small (mean_t G_Parikh(t) = 1.06e-3 nats per position). It is a registered owner choice, not a tuned value.

### 4.3 The chunked trainer (Trainer-equivalent; new code, forced by addendum 14)

The unchanged `learner.Trainer` cannot resume (it always starts from its own initialisation and has no start step), so the agreed "default Trainer path" (AN §2 item 3) cannot run in chunks. `tools/x6_stage1/x6s1_cloud.py` therefore implements `train_chunked`, which reproduces `Trainer._fit` exactly and adds checkpoint/resume. This is a binding departure recorded for a coordinator ruling (§17 O-5); it changes no scientific choice.

**Equivalence by construction (each item tested, §4.6 TRAIN-EQUIV):**
1. *Initial state:* init(s) is computed **locally** in E0 exactly as `Trainer._fit` does: inside `torch.random.fork_rng(devices=[])`, `torch.manual_seed(SeedTree(MODEL).seed("init", "x6s1", s))`, then `TransformerLM(ModelConfig(19, 18))` on CPU (local torch 2.14.1). It is saved as `init_s<s>.pt` with its canonical weights digest (§5.5) and uploaded; the cloud trainer only loads it. Init therefore never depends on Colab's torch version.
2. *Data tensors:* `PublicTokenDataset(ObservationSet("train", 18, ids, tokens), SequenceLayout())` materialised with the unchanged `learner.trainer._materialise` (an imported private helper at H, protected by S0), then moved to the device.
3. *Optimiser:* AdamW with the `Trainer._optimizer` grouping rule (re-implemented; tested to produce the identical groups and order). *Scheduler:* `LambdaLR(opt, WarmupCosine(200, 30000))` (public class).
4. *Batches:* for step k, `idx = rng.integers(0, 2**20, size=128)` with `rng = SeedTree(MODEL).generator("batch_order", "x6s1", s)`, **one call per step** exactly as `Trainer`; `torch.from_numpy(idx).to(device)`.
5. *Step:* `out = model(x[idx])`; `loss = lm_loss(out.logits, y[idx])`; finiteness check (`NONFINITE_LOSS`); `opt.zero_grad(set_to_none=True)`; `loss.backward()`; `clip_grad_norm_(…, 1.0)`; `opt.step()`; `sched.step()` — the identical sequence.
6. *Not done in the cloud:* `dev_ce`. It does not change parameters, optimiser or RNG (no_grad, eval/train toggles with dropout 0), so omitting it preserves equivalence; dev CE is recomputed locally in float64 (§4.5).
7. *Resume:* model, optimiser and scheduler `state_dict`s and the PCG64 `bit_generator.state` are restored; the optimiser state is loaded after the scheduler is constructed, so the restored per-group `lr` is the saved one.

### 4.4 Waves (MD 4)
- **C0 (smoke, non-scientific):** §5.9.
- **C1 (pilot):** NA-s1, NA-s2, ZC-s1. ZC-s1 is descriptive at the gate and never gates.
- **C2 (after LEARN = GO only):** NA-s3, NA-s4, AB-s1, AB-s2, AB-s3, AB-s4, ZC-s2, ZC-s3, ZC-s4. The C2 bundle hash is released to the owner only after GO; under NOT_LEARNED it is never released.

### 4.5 Learning-curve record (order-blind; MD 4; descriptive, sealed)
- For every model, local float64 dev cross-entropy (`lm_loss` on dev(arm, s), 2¹² rows, mean over all 33 positions, raw p̂) at the fixed checkpoints **0, 1,000, 2,000, 3,000, 5,000, 7,000, 10,000, 15,000, 20,000, 25,000, 30,000**.
- It is a function of dev tokens only and contains no order statistic, no oracle quantity and no validation or test row.
- It is computed in E1 (C1 models) and E2 (C2 models), stored in `sealed/learning_curve.json` (sha256 recorded), and released at E3 or at a stop. It never selects, stops or changes anything.

### 4.6 PF trainability and runtime pre-checks (MD 16; L§4.4)

**TRAIN-EQUIV (PF; local CPU).** On the smoke pool (§6.1), with the §4.2 `ModelConfig` and `TrainConfig(steps=60, warmup=10, checkpoint_steps=(0, 20, 40, 60))`:
1. run the unchanged `Trainer.fit` once (CPU, 2 threads);
2. run `train_chunked` with K = 20 on CPU, killing the process after the step-20 and step-40 checkpoints are written and resuming each time from disk;
3. PASS requires bitwise equality of the final model state, every optimizer tensor and scalar, the complete scheduler state and current learning rates, the PCG64 state, initialisation and all batch-index arrays. The reference run exposes its generator through a test-only delegating SeedTree wrapper without modifying production Trainer code. Fresh-process resumes must also restore the registered train mode, configuration and step numbering. This establishes equivalence on the frozen local CPU environment; it does not establish bitwise equivalence between CPU and Colab GPU trajectories.

**RUNTIME-ACCT (PF; the jobs/0033 defect; metered, with the repaired supervisor in the clean worktree).** Two children run `train_chunked` on CPU for 50 updates on the smoke pool (§4.2 `ModelConfig`, `TrainConfig(steps=50, warmup=10)`); a third child has an artificial per-process CPU limit of 5 CPU-s. PASS iff:
1. both normal children complete with finite loss;
2. each normal child's supervisor-recorded CPU is ≥ 10 CPU-s (forecast ≈ 39 CPU-s [W: 50 × 0.784]; the D-2a defect read 0.0 and 0.016 s);
3. each child's recorded peak memory is ≥ 200 MB (an interpreter with torch loaded [H]);
4. Σ child CPU ≤ the meter's job CPU + 1 s;
5. the third child ends INCOMPLETE:MODEL_CPU and its **training interpreter** (not only the venv launcher) has exited within 2 polling intervals + 10 s of the limit being crossed.

The local evaluation waves (E3.A) use the same supervisor, so RUNTIME-ACCT certifies their accounting. Failure of either check is INVALID (S1). Smoke results never enter a scientific statistic.

### 4.7 The learnability gate (pre-registered; decided before any order statistic exists; MD 3, MD 15)
- **Statistic:** Δ_nat(m) on val(NA) (2¹⁵ fresh rows, t = 32), per-row exact full-vocabulary KL(q* ‖ p^Q) against the closed-form oracle (validated against `BayesFilter`, G0-ORC). Percentile bootstrap, B = 2,000 over rows (stream ("x6s1", "boot", "learn", model)), levels by the registered `np.quantile` wrapper (L-E1).
- **learned_val(m):** defined PASS iff UB_0.975(Δ_nat(m)) < G_8.lo; defined FAIL iff the bound is finite and ≥ G_8.lo; UNRESOLVED if any required value is non-finite or undefined. A model that is INVALID:NONFINITE is a defined FAIL (D-2a convention). A model still in HOLD (§5.8) keeps LEARN from running.
- **Why G_8 (AN D2):** it is the exact beyond-8-symbol information, identical in NA, AB and ZC; Bayes 0, the best commutative predictor 0.30·G_8, a parity-level predictor 0.88·G_8 all pass; a transport-blind predictor (G_∅ = 1.196·G_8) fails; it is not an order statistic. The statistical margin is 2.4–6.1 % of G_8 [W, AN].
- **Pass wording (MD 3; L-E6):** a pass means "not a function of R_∅, and better than every function of the last 8 symbols" (UB < G_8 < G_∅, and G_8 is the minimum excess of every function of the last 8 symbols by the Pythagorean identity). It does **not** mean "holonomy use at parity level or better".
- **Stage decision:** GO iff NA-s1 or NA-s2 has a defined PASS; NOT_LEARNED iff both are defined FAIL; otherwise LEARNING_UNRESOLVED. ZC-s1's value on val(ZC) is computed, sealed and never gates.
- **Sealing (MD 15):** the E1 record releases only PASS/FAIL/UNRESOLVED per NA pilot and the GO/NOT_LEARNED/LEARNING_UNRESOLVED decision. Δ values, bounds, ZC-s1's value and the learning-curve record go to `sealed/` (sha256 recorded) until E3 or a stop.
- **On failure (S4):** the study stops; C2 is never released or trained; test pools stay sealed and are never opened; E3 is NOT_RUN; the sealed values and learning curves are reported descriptively; no retuning, extra training, new seed or relaxed threshold inside this protocol. Any successor is a new protocol (dual-track planning, owner decision, fresh pools).
- At E3, learned(m) is recomputed for all 12 models on their own arm's test pool by the empirical-Bernstein bound (E3.2) and enters rule 4 (§7.9).

---

## 5. Cloud training execution (Colab free tier) (owner addendum 14)

### 5.1 Division of work

| Where | What | Determinism |
|---|---|---|
| **Local (this machine, CPU)** | Pool generation and registry; init states; expected digests; the cloud bundles; ingest and the four integrity gates; the gate; the learning-curve record; every evaluation (float64) | Deterministic and bit-reproducible (fixed threads and batching) |
| **Colab (owner's browser session, GPU)** | Training only: `train_chunked` over registered train pools, from registered init states, in 1,000-update chunks | The **inputs** (data bytes, init state, batch-index sequence, recipe) are verified exactly; the **floating-point trajectory** is not reproducible (GPU non-determinism accepted for training only) |
| **Owner** | Uploads a bundle to Drive, runs the notebook, relays one hash, downloads the output folder | Every transfer is checked by sha256 |

The coordinator cannot run Colab headless; the owner runs the notebook (§5.10). Nothing outcome-bearing is computed in the cloud.

### 5.2 Data handling: **upload** (decision and justification)
The training histories are generated **locally** by the frozen sampler in E0 and **uploaded**; Colab never samples.
1. The train pools must exist locally anyway: REG2 must contain them before the test draw (§6.4), and DATA-ID needs their local digests. Generating them a second time in Colab would add a second execution path for the same bytes.
2. A Colab regeneration depends on Colab's Python, numpy and sampler behaviour; numpy's `Generator` distribution methods are not guaranteed stream-stable across versions. A mismatch could only end in a DATA-ID failure after GPU time was spent. Uploaded bytes are identical by construction and verified by sha256 before the first update.
3. The volume is small: tokens only (uint8 [2²⁰, 33] = 34.6 MB per model [W]); wave C1 ≈ 104 MB, C2 ≈ 311 MB. Sequence ids are not uploaded: Colab rebuilds them with the unchanged `make_sequence_ids(process_code("x6s1", arm, "train", s), "train", 2**20)` (no RNG).
4. Colab then runs no sampler, no oracle and no latent-state code, and receives no validation, test, gate, prefix, dev or sealed data (§5.12).

### 5.3 The cloud bundle and ticket (built in E0, gate CLOUD-PREP)
A bundle is a folder `<bundle-id>/` built under `X:/Downloads/topo-scratch/<job>/cloud_bundle/` and uploaded by the owner into a new immutable directory `My Drive/X6S1/<bundle-id>/` (RC8, below):

| File | Content |
|---|---|
| `code.tar` | `git archive H -- src tools/x6_stage1 pyproject.toml` (its pax header carries the commit id H; `git get-tar-commit-id`) |
| `X6S1_colab.ipynb` | The thin notebook (§5.11), outputs stripped |
| `data/train_<arm>_s<s>.npy` | uint8 [2²⁰, 33] tokens of each model of the wave (C0: `data/smoke.npy`, 2¹²) |
| `init/init_s<s>.pt` | `torch.save({"model": state_dict})` of init(s), CPU float32 |
| `ticket_<wave>.json` | Wave id; protocol id and sha256; H; the model list with arm, seed, run_key ("x6s1", s), data file and sha256, init file and canonical digest, steps 30,000, K 1,000; the **expected digests** for every chunk (batch digest and PCG64-state digest after the chunk, §5.5); the registered notebook cell templates' sha256 |
| `SHA256SUMS` | sha256 of every file above except the notebook (Colab may rewrite the notebook file when it saves) |

- **BUNDLE_SHA256** = sha256 of `SHA256SUMS`; the coordinator gives it to the owner (one 64-hex string) when releasing the wave.
- **Ticket and schema contents (RC7).** Tickets include DATA and MODEL masters, all derived model seeds, complete model/train configuration, and the wave's actual `steps` and `K`. Chain requirements are parameterised by those ticket values, including C0's 200 steps and K=100. The record schema specifies step-0 null values for chunk-only fields and stores the PCG64 state needed for resume. Checkpoint-internal step, scheduler phase, optimizer structure and PCG64 state must agree with the corresponding record and expected ticket state.
- **Immutable namespace (RC8).** Each released bundle is uploaded into a new immutable directory `My Drive/X6S1/<bundle-id>/`. The owner uses the notebook inside that directory and pastes its BUNDLE_SHA256. The bundle identifies its wave and output lineage. Never merge or overwrite different waves' notebooks, tickets or SHA256SUMS. Only one notebook session may write a given model lineage at a time. The bundle id is `<wave>-<first 12 hex digits of BUNDLE_SHA256>` (a retrain bundle, §12 item 9, therefore has a new id); cell 2 locates `ROOT` as the unique directory `My Drive/X6S1/*-<those 12 digits>` and stops if there is not exactly one. Every path below is relative to `ROOT`.
- **Allowed classes only (S9):** the builder refuses any file that is not code, the notebook, a train or smoke pool of the wave's models, an init state, the ticket or `SHA256SUMS`; it asserts that no validation, test, gate, prefix, dev, sealed or registry file and no latent array is present (T-BUNDLE).
- C0, C1 and C2 bundles are built in E0 (all pools exist then); only their hashes are recorded. C2 is released after GO.

### 5.4 Chunked, resumable training: the exact resume protocol
`run_wave(ROOT, env)` processes the ticket's models in ticket order. For each model it performs:

0. **Terminal markers first (RC6).** Before quarantine or resume, discover and validate all terminal NONFINITE markers in the active model lineage. A valid marker is permanently terminal, is included in provenance and transfer inventories, is never quarantined away, and prevents further updates or retraining. An unreadable or ambiguous terminal marker stops recovery for coordinator review. (The marker is `rec/NONFINITE.json`.)
1. **Discover.** List `out/<model>/` under ROOT. Valid chain elements are pairs (`ckpt/<step:06d>.pt`, `rec/<step:06d>.json`). Read every record; a record is valid iff it parses, its own `record_sha256` field equals the sha256 of its canonical JSON without that field, and the checkpoint file it names exists with the recorded `file_sha256`.
2. **Validate the chain from step 0.** Records must exist for steps 0, K, 2K, … consecutively (K and `steps` from the ticket), each `prev_record_sha256` equal to the previous record's `record_sha256` (step 0: equal to the sha256 of the model's ticket entry), with the checkpoint's canonical weights digest equal to the record's. The step-0 record is created from the uploaded init state (weights digest equal to the ticket's).
3. **Quarantine (RC6).** Quarantine applies only to nonterminal artifacts outside the validated chain. Read failures or incomplete Drive listings produce HOLD and a stable re-read; they are not evidence of corruption. Before relocating an artifact, create and re-hash a preservation copy and record its original path. A broken interior link remains FAIL_TECHNICAL/CHAIN. (Nonterminal artifacts outside the chain are `.part` files, a checkpoint without a record, a record without a checkpoint, a truncated record, anything after the chain's last valid element; they are relocated to `orphans/<utc>-<model>/` and listed in the session record. Nothing is deleted. A broken interior link prints `STOP: CHAIN BROKEN`, §5.8.)
4. **Last state.** If step 0 found a valid terminal marker, the model is INVALID:NONFINITE and is skipped. Otherwise let k* be the last valid step; if k* = `steps` (30,000; C0: 200) the model is DONE.
5. **Restore.** Load `ckpt/k*.pt` with `map_location=device`; build the model and load its state; build AdamW (registered groups), then `LambdaLR`, then load the optimiser and scheduler states; restore the numpy `Generator` from the recorded PCG64 state; check the restored PCG64-state digest against the record and the ticket's expected digest for step k* (`STOP: RNG STATE MISMATCH` otherwise).
6. **Pre-check the next chunk.** On a deep copy of the generator, draw the K index arrays of steps k*+1..k*+K (one 128-element call per step), compute their batch digest (sha256 of the concatenated little-endian int64 arrays) and compare it with the ticket's expected digest for that chunk; on mismatch `STOP: BATCH-ID MISMATCH` (DATA-ID failure, before any GPU work). The pre-drawn arrays are the ones used for training; the original generator is then advanced by the identical draws, so the stored state equals the expected one.
7. **Train the chunk** exactly as §4.3. A non-finite loss writes `rec/NONFINITE.json` (exclusive create: step, chunk, session id, loss bit pattern) and stops that model; no retry (S5).
8. **Write the checkpoint.** The snapshot is {model, optimiser, scheduler, PCG64 state, torch CPU and CUDA RNG states (recorded, not consumed: dropout is 0 and no torch randomness is used after init), step}. Serialize one checkpoint snapshot once to an in-memory byte buffer, hash those exact bytes, write those same bytes to `.part`, flush and fsync, re-read and verify, then publish the checkpoint. Do not compare separate `torch.save` serializations to different filename/buffer destinations. Publication refuses an existing target. A completed record is published only after its referenced checkpoint verifies. (`.part` is `ckpt/<step>.pt.part`; publication renames it to `ckpt/<step>.pt`; an existing target prints `STOP: DUPLICATE STEP`.)
9. **Write the record** (§5.5) to `rec/<step>.json.part`, fsync, re-read and verify, rename. Only now is the chunk complete. Because interrupted moves through mounted Drive can lose data, the protocol promises verified recovery (steps 0–3 at every resume and the ingest gates), not POSIX durability from `fsync` alone (RC8).
10. **Print** one progress line (§5.10) and continue with step 6 until `steps`.

**Why a resumed run is bit-identical in its batch sequence.** The index sequence is a pure function of (MODEL master, "batch_order", "x6s1", s, number of draws): it uses no device, no torch RNG and no floating-point state. Each chunk starts from the recorded PCG64 state, which is checked against the locally computed expected state, and each chunk's index digest is checked against the locally computed expected digest before training it. A disconnect inside a chunk loses only that chunk's unsaved work; the chunk is recomputed from the same checkpoint with the same indices. Its floating-point result may differ from the lost attempt (GPU non-determinism), which is harmless because the lost attempt was never saved.

**Interruption accounting.** Colab disconnects, idle timeouts, usage limits and GPU unavailability are **not** failures: they leave a valid chain prefix (HOLD:CLOUD_INCOMPLETE) and the owner resumes (§5.10). They do not count against any correction limit.

**Device policy (RU O-7).** A CUDA device is required (the notebook refuses a CPU runtime). The GPU type may differ between chunks of one model (Colab assigns it); every chunk records its device, and a model with more than one type carries the provenance qualifier MIXED_DEVICE. It changes the training trajectory, not the frozen evaluation procedure.

**Software versions (RU O-14).** Every session records all versions (§5.6). A stable torch/numpy environment within a model is preferred. At each session start, `precheck` compares Python, numpy, torch, CUDA and cuDNN versions with the model lineage's previous session; a change is detected and recorded **before continuation** (`ENV CHANGED <field>: <old> → <new>` and a session-record entry; provenance qualifier MIXED_ENV), and continuation still requires the next chunk's batch-ID pre-check. The batch checks establish stream identity, not framework-semantic equivalence. The notebook never installs or upgrades packages; no unreviewed installation is introduced automatically.

### 5.5 Checkpoint, record and chain formats
- **Checkpoint file** `ckpt/<step:06d>.pt`: `torch.save` dict {"model": state_dict (CPU float32 tensors), "optimizer", "scheduler", "rng": {"pcg64": bit_generator.state, "torch_cpu": tensor, "torch_cuda": list}, "step": int}. Size ≈ 9.63 MB [W] (weights 3.21 MB + AdamW moments 6.42 MB); 31 per model, ≈ 298 MB per model and ≈ 3.58 GB for 12 models [W].
- **Canonical weights digest:** sha256 over, for each `state_dict` key in sorted order: the UTF-8 key, a zero byte, the dtype name, the shape as little-endian int64, and the contiguous little-endian tensor bytes. Independent of pickling; computed by the same `x6s1_cloud.weights_digest` in Colab and locally.
- **Record** `rec/<step:06d>.json` (canonical JSON, sorted keys): `model`, `step`, `file`, `file_sha256`, `weights_sha256`, `batch_sha256` (steps step−K+1..step), `pcg64_state` (the full `bit_generator.state` after `step`, needed for resume) and `pcg64_state_sha256`, `prev_record_sha256`, `record_sha256`, `session_id`, `device_name`, `cuda_capability`, `train_loss_first` and `train_loss_last` (losses of the chunk's first and last step, descriptive), `loss_finite`, `wall_s`, `utc`. **Step-0 values (RC7):** the chunk-only fields `batch_sha256`, `train_loss_first`, `train_loss_last`, `loss_finite` and `wall_s` are `null` at step 0; `pcg64_state` at step 0 is the fresh generator's state; `device_name` and `cuda_capability` are those of the session that created the record. The checkpoint's internal `step`, scheduler phase (`last_epoch` = step), optimizer structure (two groups, registered order) and PCG64 state must agree with the record and with the ticket's expected state for that step.
- **Terminal marker** `rec/NONFINITE.json` (exclusive create): model, step, chunk, session id, loss bit pattern, `prev_record_sha256` of the last valid record, its own sha256.
- **The chain** of a model is its records for steps 0, K, 2K, …, `steps` (ticket values: 30,000 and 1,000 for C1/C2; 200 and 100 for C0) linked by `prev_record_sha256`: strictly increasing steps, exactly one record per step, no gap (**monotone checkpoint chain**).

### 5.6 Environment record, session records and the manifest
- **Session-start record** `sessions/<utc>-<session_id>.start.json` (under ROOT), written at each start of cell 5: Python, numpy and torch versions; `torch.version.cuda`; cuDNN version; GPU name, driver and memory (`nvidia-smi`); determinism and TF32 flags; `CUBLAS_WORKSPACE_CONFIG`; the code commit read from the `code.tar` pax header; sha256 of `code.tar`, of the ticket and of `SHA256SUMS`; the version comparison with the lineage's previous session (§5.4); models attempted and resume steps; orphans and preservation copies; STOP messages.
- **Executed-cell recording (RC7).** A session-start record captures executed sources through cell 5. Cell 6 writes a session-finalisation record capturing its own executed source and referencing the start record. Interrupted sessions legitimately have no cell-6 record. CLOUD-PROV validates every available execution record against the permitted cell templates and permitted repetitions; unexplained additional user-executed code fails provenance. (Sources are read from the IPython input history; the pasted 64-hex value is normalised to the template placeholder. The finalisation record is `sessions/<utc>-<session_id>.final.json`.)
- **Manifest** `exports/<utc>/MANIFEST.json` (under ROOT), written by cell 6: protocol id and sha256; code commit (H) and `code.tar` sha256; BUNDLE_SHA256; ticket sha256; per model: arm, seed, run_key, MODEL and DATA master seeds and stream names, data file sha256, init digest, the full chain (every record verbatim), final checkpoint sha256 and **final weights sha256**, status (DONE, INVALID:NONFINITE, INCOMPLETE), device list; the orphan and preservation-copy list; and the output inventory:
- **Output inventory (RC7).** `MANIFEST.json` contains a canonical path-to-SHA256 inventory of immutable checkpoint, record, terminal-marker and session-record files in the exported snapshot. The inventory excludes `MANIFEST.json`, transient `.part` files and any inventory file itself. MANIFEST_SHA256 authenticates the manifest separately. Ingest verifies exact inventory coverage with these explicit exclusions. Re-finalisation creates a new immutable export snapshot and preserves earlier snapshots.
- **MANIFEST_SHA256** = sha256 of `MANIFEST.json`, printed by cell 6; the owner relays it to the coordinator (an out-of-band anchor). The coordinator ingests the snapshot named by the relayed hash.

### 5.7 Transfer and local ingest
- **Transfer.** The owner downloads the bundle directory `My Drive/X6S1/<bundle-id>/` (Drive web "Download", possibly split zips, or Google Drive for desktop) into `X:/Downloads/topo-scratch/<job>/cloud_in/<bundle-id>/` and tells the coordinator, quoting MANIFEST_SHA256. The medium is irrelevant: every byte is verified.
- **Ingest** (`x6s1_ingest.py`, metered local job E0b/E1/E2) runs the four integrity gates (§5.8) per model, in the order WEIGHTS-HASH → CLOUD-PROV → DATA-ID → TRAIN-COMPLETE, then copies the verified files by exclusive create into `x6-stage1-store/cloud/<wave>/<model>/` with a store manifest. Evaluation only ever loads from the store, re-verifying the final checkpoint's sha256 and weights digest at load (E3.0).
- **Admission lock (RC9).** Immediately after a model first passes all four integrity gates, record its admitted final checkpoint and weights digests by exclusive create, before LOSS-ECHO, learning curves, validation or test evaluation. This first verified final chain is immutable and is the model's only admissible chain. (The lock is `x6-stage1-store/cloud/ADMITTED/<model>.json`, holding the bundle id, MANIFEST_SHA256, the final checkpoint sha256, the final weights digest and every chain record sha256.)
- **LOSS-ECHO (descriptive; after admission):** for every chunk, the training loss of its first step is recomputed locally (float32 and float64) from the previous checkpoint's weights and the known batch indices, and reported beside the cloud's `train_loss_first` of that record (maximum absolute difference per model). It is a consistency diagnostic, not proof of the entire training trajectory, and never a gate. (Likewise CLOUD-PROV and TRAIN-COMPLETE audit the trusted notebook execution; they are not cryptographic proof that every reported optimiser update occurred.)

### 5.8 Integrity gates and statuses (each per model, before any local evaluation of that model)

| Gate | Checks (all exact) | Failure → status | Route |
|---|---|---|---|
| **WEIGHTS-HASH** | (a) sha256 of the received `MANIFEST.json` equals the owner-relayed MANIFEST_SHA256; (b) the received snapshot covers the manifest's output inventory exactly, with the explicit exclusions of §5.6, every listed file matches its inventory sha256, and the inventory's checkpoint entries match the chain records' `file_sha256`s; (c) every checkpoint, loaded locally with `torch.load(weights_only=True)`, has the recorded canonical weights digest; the final weights digest equals the manifest's | (a)–(b) local copy differs but a fresh download matches → **TRANSFER_RETRY** (environment; ≤ 3 downloads); persists, or the Drive copy itself differs from the manifest, or (c) fails → **FAIL_TECHNICAL/WEIGHTS_HASH** | Retrain route (§12 item 9) |
| **CLOUD-PROV** | Every manifest and session field of §5.6 present and well-typed; code commit = H; protocol sha256 = the frozen one; BUNDLE_SHA256 = the released one; ticket sha256 equal and its seeds, configuration, `steps` and K equal the frozen values; every available execution record (start and finalisation) validates against the permitted cell templates and permitted repetitions, with no unexplained user-executed code (§5.6); every session's versions recorded; device CUDA in every chunk; TF32 off and deterministic flag on in every session | **FAIL_TECHNICAL/CLOUD_PROV** (includes owner deviations: edited cells, a wrong bundle, manual edits on Drive) | Retrain route; if a code defect, technical correction (§12 item 3) |
| **DATA-ID** | Data file sha256 = the local pool's (and the raw token digest equals the registered pool digest); step-0 weights digest = local init(s) digest; every chunk's `batch_sha256` and `pcg64_state_sha256` = the locally computed expected values; each checkpoint's internal step, scheduler phase, optimiser structure and PCG64 state agree with its record (§5.5) | **FAIL_TECHNICAL/DATA_ID** (a systematic mismatch, e.g. a numpy stream change, stops the wave: S11) | Retrain route after the cause is corrected |
| **TRAIN-COMPLETE** | Records for steps 0, K, …, `steps` (ticket values), exactly one each, linked; final status DONE; no terminal NONFINITE marker in the lineage (§5.4 step 0) | Valid prefix ending before `steps` → **HOLD:CLOUD_INCOMPLETE** (not a failure; resume in Colab). Gap, duplicate, bad link or out-of-order step → **FAIL_TECHNICAL/CHAIN**. Valid terminal marker → **INVALID:NONFINITE** (terminal; no retry or retraining; the model counts as failing every per-seed condition and is a defined FAIL at the gate). Unreadable or ambiguous marker → HOLD for coordinator review | HOLD: resume. CHAIN: retrain route. NONFINITE: none |

A model enters evaluation only with all four PASS and its admission lock written (§5.7). A wave's gates run once per downloaded export snapshot; a HOLD model is re-ingested from a new snapshot after the owner resumes it. Retrain routes apply only under §12 item 9 (never after admission or any local evaluation).

### 5.9 CLOUD-SMOKE (wave C0; after owner authorisation, before C1)
- In Colab: `train_chunked` on the smoke pool (NA, 2¹², non-scientific) with the §4.2 `ModelConfig`, `TrainConfig(steps=200, warmup=10)` and K = 100; after the step-100 checkpoint the notebook's smoke mode discards every in-memory object and resumes from Drive (exercising steps 1–9 of §5.4), then finishes.
- Locally (job E0b): the four integrity gates; the step-200 weights evaluated in float64 on CPU on 1,024 smoke rows (finite, valid softmax); TRAIN-COMPLETE of a 3-record chain; the session record's fields; and the owner's experience of the runbook (time, prompts, problems) recorded.
- Descriptive: from the GPU step-100 checkpoint, 100 local CPU updates are run and compared with the GPU step-200 weights (maximum absolute difference reported; no gate, since devices differ).
- Any failure is INVALID (S1): no scientific wave runs until a corrected smoke passes.

### 5.10 Owner-facing runbook
**Before the first run (once).** A Google account with Drive space ≥ 6 GB free (forecast ≈ 4.3 GB [W]); a desktop browser. No installation.

**Per wave.**
1. The coordinator sends: the wave name (C0, C1 or C2), the local folder to upload, and **BUNDLE_SHA256** (64 hex characters).
2. Create `My Drive/X6S1/` once if it does not exist. Upload the bundle folder `<bundle-id>` (drag and drop) so that it becomes `My Drive/X6S1/<bundle-id>/`. Each released bundle is uploaded into a new immutable directory `My Drive/X6S1/<bundle-id>/`. The owner uses the notebook inside that directory and pastes its BUNDLE_SHA256. The bundle identifies its wave and output lineage. Never merge or overwrite different waves' notebooks, tickets or SHA256SUMS. Only one notebook session may write a given model lineage at a time (do not open the same bundle's notebook in two tabs).
3. In Drive, double-click `X6S1/<bundle-id>/X6S1_colab.ipynb` and choose "Open with Google Colaboratory".
4. Menu **Runtime → Change runtime type → T4 GPU** (any GPU offered is acceptable) → Save.
5. Run the six cells in order (Shift+Enter each, or **Runtime → Run all**).

| Cell | What it does (registered source in `API.md` §cloud) | Expected output | If not |
|---|---|---|---|
| 1 GPU | `nvidia-smi` query; asserts CUDA | `Tesla T4, <driver>, 15360 MiB` and `GPU OK: Tesla T4` (name may differ) | `NO GPU`: set the runtime (step 4); if Colab says it cannot connect to a GPU (usage limit), stop and retry hours later or next day. Never use a CPU runtime |
| 2 Drive | `drive.mount("/content/drive")`; the line `BUNDLE_SHA256 = "…"` where the owner pastes the hash; `ROOT` = the unique directory `/content/drive/MyDrive/X6S1/*-<BUNDLE_SHA256[:12]>` | A Google sign-in prompt, then `Mounted at /content/drive` and `ROOT X6S1/<bundle-id>` | Re-run; accept the permission prompt. `STOP: BUNDLE DIRECTORY` (none or several matches): check the upload and the pasted hash |
| 3 Verify | Inline hashlib check of `SHA256SUMS` against BUNDLE_SHA256, then of `code.tar`; unpack to `/content/x6s1`; import `x6s1_cloud`; `verify_bundle` | `BUNDLE OK 1A2B3C4D… wave C1, 3 models, code <H prefix>` | `STOP: BUNDLE HASH MISMATCH`: check the pasted hash and that the upload finished; otherwise send the message to the coordinator |
| 4 Environment | `environment()`, `precheck()`: versions, flags, batch-ID pre-check of the first pending chunk of every model | `ENV OK torch 2.x cuda 12.x Tesla T4` and `PRECHECK OK 3/3` | Any `STOP:` line → send it verbatim to the coordinator; do not continue |
| 5 Train | `run_wave(ROOT, env)`: resumes automatically | One line per chunk, e.g. `[NA-s1] step 07000/30000 ok ckpt 3fa2c1d0 12.3 s`; per model `MODEL DONE NA-s1 weights 7b1e…`; finally `WAVE DONE 3/3` | Disconnect: see below. `STOP:` → send it |
| 6 Finalise | `finalise(ROOT)` (revalidates every chain from Drive, writes the finalisation record and a new export snapshot); `drive.flush_and_unmount()` | `WAVE DONE 3/3` and `MANIFEST_SHA256 = <64 hex>` | If finalisation fails, reconnect and run cells 1–4 and then cell 6 using the same bundle. `finalise` independently revalidates the chain from Drive and refuses a WAVE DONE result unless every required model is DONE or terminal INVALID:NONFINITE. If training remains incomplete, run cell 5 before finalising again. |

6. Send the coordinator the `MANIFEST_SHA256` line and say the wave is done.
7. In Drive, right-click `X6S1/<bundle-id>` → **Download**; put the zip(s) in the folder the coordinator names (`X:/Downloads/topo-scratch/<job>/cloud_in/`); do not unzip or edit.

**On disconnect, idle timeout, a closed tab or "runtime disconnected".** Reconnect (or reopen the notebook from Drive), and run cells 1–5 again with the **same** BUNDLE_SHA256. Training resumes from the last saved checkpoint; at most one chunk (≈ 10–40 s of GPU work [H]) is repeated. Nothing needs to be deleted. Free-tier GPU availability, idle timeouts and runtime lifetimes vary. A free notebook may run for at most 12 hours and can terminate earlier. Resume from verified checkpoints; do not rely on a fixed idle interval. Waves are expected to take ≈ 20–60 min (C1) and ≈ 1–3 h (C2) of GPU time [H], possibly over several sessions.

**Never:** edit a cell (other than pasting the hash in cell 2); run any additional code in the notebook; run a cell from a different copy of the notebook; delete, rename or move files inside `X6S1/<bundle-id>`; merge two bundles; change the runtime to CPU; upload files the coordinator did not send.

### 5.11 The notebook in the footprint
- `tools/x6_stage1/X6S1_colab.ipynb`: nbformat 4, **six code cells** (plus short markdown cells repeating the runbook lines), at most 60 code lines in total, outputs and execution counts stripped. All logic is in `x6s1_cloud.py`; the cells only call it (cell 3 holds a ≤ 12-line inline hashlib bootstrap, because the module can be imported only after `code.tar` is verified).
- The registered cell sources are reproduced verbatim in `API.md` §cloud; the cell-2 hash line is a placeholder template.
- It is frozen with the code (its sha256 recorded at the code freeze and in FREEZE.json), reviewed with the modules, and tested by author B (T-NB): the JSON parses; exactly six code cells; each source equals the registered template; no outputs; the inline bootstrap's hash check refuses a modified `SHA256SUMS` or `code.tar` (run locally against a temporary bundle).
- `x6s1_cloud.py` imports only the standard library, numpy, torch and `topo_pilot.{learner, contracts, dataset}`; it runs both in Colab and locally (TRAIN-EQUIV, RUNTIME-ACCT, smoke replay). `tools/check_imports.py` and T-SIZE cover it.

### 5.12 What never leaves the local machine (S9)
Validation, test, gate, prefix and dev pools; sealed files; the registry; latent states; oracle laws and tables; any evaluation output. The cloud receives only code at H, the notebook, the wave's train (or smoke) pools, init states and the ticket. The test pools are drawn in E0 for the oracle-only preparation of §12 item 11; no model prediction on test histories is made before E3, and test data never reach the cloud.

---

## 6. Evaluation sets, witnesses, seeds and registry

### 6.1 Pools (natural, fresh, drawn once from registered streams; never extended, filtered or redrawn)

| Pool | Arm | Rows (33 symbols) | Use | Access before E3 |
|---|---|---|---|---|
| train(arm, s) | NA, AB, ZC × s = 1..4 | 2²⁰ each (12 pools) | Cloud training (uploaded) | learner only |
| dev(arm, s) | as train | 2¹² each | Local learning-curve record | E1/E2 (sealed output) |
| smoke | NA | 2¹² | TRAIN-EQUIV, RUNTIME-ACCT, CLOUD-SMOKE | PF and C0 only |
| gate | NA 2¹⁶; AB, ZC 2¹⁴ | | G0-ORC, G0-POS (oracle only) | yes |
| prefix | NA | 2¹² (→ 1,024 prefixes) | Designed set D | yes (E0) |
| val | NA, AB, ZC | 2¹⁵ each | Gate; FEAS-POWER (oracle only); HEADROOM-D; γ at E3 | yes (gate sealed) |
| **test** | NA, AB, ZC | **2²¹ each** (addendum 13; retained, RU O-4) | E3 only | only the oracle-only preparation of §12 item 11 (S9) |

Total 19,128,320 rows, ≈ 631 MB of tokens [W]. ObservationSet splits: train → "train"; dev, val, gate, smoke, prefix → "dev"; test → "test". Sequence ids: `make_sequence_ids(process_code("x6s1", arm, pool, s), split, n)` with the codes fixed in `API.md`; `check_disjoint` over every pool.

### 6.2 Seeds and streams
- **Masters (both tracks):** DATA = 2026101861 and MODEL = 2026101862. S0 refuses them if either appears in any recorded seed map or config of any store (D-2a §2.6 freshness rule); a collision requires a documented replacement before any data.
- **Data:** `SeedTree(DATA).generator("x6s1", pool, arm[, s])`; partners `.seed("x6s1", "partner", pool, t, row)`; prefixes ("x6s1", "prefix") and ("x6s1", "prefix_len"); bootstraps ("x6s1", "boot", statistic_id[, model]); FEAS synthetic ("x6s1", "feas").
- **Model:** init `SeedTree(MODEL).seed("init", "x6s1", s)`; batches `SeedTree(MODEL).generator("batch_order", "x6s1", s)` (the `Trainer` names with run_key ("x6s1", s)).
- Stage 1 uses new seeds throughout (S0§8.4). The full scope map is committed in `API.md` before implementation.

### 6.3 Designed set D
As §2.5. D's token arrays and their sha256 are frozen in E0. Designed histories are constructed, never uploaded and never inserted into training; their natural occurrences as exact prefixes of training rows are counted and reported (D-2a §2.6 rule 4).

### 6.4 X6-scoped exposure registry (MD 8; K4b manner, X6-scoped)
Digest: sha256 of the uint8 row w_1..w_32 (the K4/K4b digest space; w_33 is a label only). Membership uses a sorted array of the first 8 digest bytes (uint64) with full-digest confirmation of candidate matches, built with bounded-memory ingestion and external/streamed ordering where necessary (§13.4).

**X6-REG1 (built before any stage-1 draw):**
- **(a) X6 stage-0 Monte Carlo rows,** regenerated identity-only with the unchanged `x6_run.sample` and `SeedTree(420700)` for every MC arm (NA 2¹⁸; AB, ZC, TRIV, ETA1 2¹⁶; NOCUE 2¹⁴; 540,672 rows [W]) — the stage-0 store holds no token arrays (AN §0). The NA regeneration must reproduce the token- and table-derived counts of stage-0's `report.json`: E_cue hits **200,306** and E_amb,Parikh ∧ E_nb hits **13,402**; a mismatch is FAIL_TECHNICAL/LINEAGE. The other arms are accepted by determinism of the unchanged code at H (coordinator ruling under MD 8; L Q6). The stage-0 constructed histories (W1, W2 with Π0/Π1/Π3/Π6, W3, W3′, the Decimal reference set) are included.
- **(b) Handoff JSON:** 32- and 33-element integer lists that are X6-valid (`x6_model.parse` succeeds), read through the unchanged `c1_registry_sources.handoff_sources` after `k4b_registry.validate_handoff_json` of every JSON file; a parse failure is INCONCLUSIVE/REGISTRY_INCOMPLETE.
- **(c) Foreign alarm:** the frozen K4b K-REG2 (6,024,521 digests, per the review) and k4b-store's later stage tables via the unchanged `k4b_registry_k.source_k`. Verify the unchanged K-REG2 manifest and digest-file hashes, but ingest its digest and sequence-id arrays through a bounded-memory identity reader inside `x6s1_registry.py`. Validate the stored dtype, shape, ordering, counts and canonical union hashes while streaming. Do not materialise the full Unicode digest array, Python digest set or joined digest string. On small synthetic fixtures, author B checks exact equivalence with `k4b_registry.load`. This is an explicit memory-motivated implementation departure; frozen K4b files and semantics remain unchanged.
- **(d) Completeness:** Inventory covers the project root and the explicitly named X6 scratch roots, including `.npz`, `.npy`, ObservationSet roots and registered history-bearing JSON formats. The reused inventory alone is insufficient because it scans `.npz` under the project root. Every X6 history-bearing source is covered, recognised as a hash-identical registered copy, or causes REGISTRY_INCOMPLETE. Foreign classification includes a recorded reason. (The unchanged `k4b_registry.inventory(ROOT)` is run as one component; `x6s1_registry.py` extends the scan to the named X6 scratch roots `X:/Downloads/topo-scratch/<job>/` of every X6S1 job, including `cloud_bundle/` and `cloud_in/`, and to `.npy` files.)

**X6-REG2** = REG1 ∪ every non-test stage-1 pool (train × 12, dev × 12, val × 3, gate, smoke, prefix), built after those pools are drawn and **before** the test draw. A **reservation window** runs from the start of the REG2 build to the end of the test draw: no other X6-process history generation (coordinator attestation, K4b W2/W3).

**Reported diagnostics (MD 8, X§7):** sequence-id reuse between stage-1 pools and every ObservationSet in other stores (diagnostic only; within stage 1, id disjointness is required); cross-process digest coincidences by source.

### 6.5 Separation (checked on every row)
- test(arm) ∩ REG2 = ∅ for every arm, and test pools pairwise disjoint;
- val ∩ (REG1 ∪ train ∪ dev ∪ gate ∪ smoke ∪ prefix) = ∅;
- gate, prefix and smoke disjoint from train and dev;
- sequence ids disjoint across all stage-1 pools;
- within-split duplicates counted and kept (iid draws, not removed).

Any collision is **FAIL_TECHNICAL/LINEAGE, with no replacement sampling**; an unreadable source is INCONCLUSIVE/REGISTRY_INCOMPLETE. Expected collisions: every 32-symbol history has probability ≤ (1/16)·5⁻³¹ = 1.342e-23 [W], so with ≈ 2 × 10⁷ X6 rows and ≤ 10⁸ registered rows the expected count is ≤ 2.7 × 10⁻⁸ [W]: a collision is a lineage alarm, not a sampling event.

### 6.6 Stated departures from K4b (MD 8)
1. The registry is X6-scoped. Other processes' histories are not exposures of X6 models: no X6 model trained on them and no X6 decision read them.
2. **The sealed-D-2a alphabet predicate is not applied**; D-2a's sealed pools are never opened. (Under K4b's rule a predicate hit is INCONCLUSIVE; at X's test scale it would very likely stop the study, AN D8.)
3. The foreign component (c) is kept as a conservative alarm.
4. No rejection sampling: with no exclusion, G_safe = G0⁻. Separation failures suppress claims and do not define a conditioned sampling law (§7.1, RC1).
5. K-REG2 is ingested by a bounded-memory identity reader instead of `k4b_registry.load` (§6.4 (c); RC10).

---

## 7. Statistics and inference

### 7.1 Units, conditioning and independence
- **Rows.** One t = 32 readout per test history. Test pools are drawn in E0 from their own streams, before training, sealed, and never uploaded, so the models (functions of train pools, init states and GPU noise) are independent of the test rows.
- **Sampling and separation.** Each test pool is one original iid draw from its arm's natural law, with no rejection, replacement, filtering or deduplication. Statistical coverage is assessed over this original draw, conditional on fixed potential model checkpoints whose training inputs and training randomness are independent of the test draw. Registry, separation and oracle-feasibility failures suppress claims; they do not define a conditioned sampling distribution. Consequently a reported erroneous empirical-Bernstein claim is a subset of the corresponding erroneous claim on the original iid draw. The guarantee is not asserted conditional on SEP or feasibility passing.
- **Collision mass (descriptive lineage diagnostic).** ρ̄ := |S|·(1/16)·5⁻³¹ for the REG2 digest set S is computed exactly and reported (≤ 1.342e-15 for |S| ≤ 10⁸ [W]); it enters no bound. With no rejection, G_safe = G0⁻ (MD 8).
- **Inference is conditional on the registered models** (D-2a §10.3; X§10), with no population-of-seeds claim.
- **Designed statistics** are deterministic censuses with no sampling interval.

### 7.2 Registered confirmatory family: nominal level 0.05; finite-sample log-loss subfamily guarantee 0.025

| Claim | Statistic | Method | Level | Supported iff |
|---|---|---|---|---|
| **C-ORD** | mean_{s=1..4} β̃(s) | Paired bootstrap with tail diagnostic (§7.5) | α = 0.025 | mean ≥ 0.25 **and** LB_0.975 > 0.05 **and** β̃(s) > 0 in ≥ 3 of 4 **and** TAIL PASS |
| **SHARP(s)**, s = 1..4 | Δ_nat(NA-s) | Empirical Bernstein (§7.3–§7.4), N = 2²¹ | δ = 0.00625 each | U_{0.00625}(NA-s) < G0⁻ |
| **TARGET(s)**, s = 1..4 (secondary) | Δ_nat(NA-s) | the **same** U as SHARP(s) | (shared) | U_{0.00625}(NA-s) < (3/4)·G0⁻ |

- The allocation is 0.025 + 4(0.00625) = 0.05. The four empirical-Bernstein bounds provide a finite-sample simultaneous guarantee of at least 0.975 for all SHARP/TARGET statements together. TARGET shares its seed's coverage event with SHARP and requires no additional allocation. C-ORD uses a nominal one-sided 97.5% percentile-bootstrap bound. Its tail diagnostics do not prove coverage, so the combined family has nominal, rather than established distribution-free, FWER 0.05.
- **Resolution:** C-ORD is UNRESOLVED if any NA model or control term is missing, INVALID, readout-undefined (§2.6) or TAIL fails. No averaging over fewer seeds; no control term dropped.
- **Not in the family:** the gate (a pre-outcome decision), LEARN-TEST (a robustness branch, δ = 0.025 per model), per-seed flags, designed flags, ladder, length profiles (descriptive or exact).

### 7.3 The empirical-Bernstein bound: theorem and full proof
**Setting.** X_1, …, X_n iid, 0 ≤ X_i ≤ B, mean μ, variance σ²; n = 2m even. Here X_i = KL(q*(H_i) ‖ p^Q(H_i)) under the original natural law P (§7.1), B = 17 (§2.2), n = 2²¹, m = 2²⁰. Define

  X̄ = (1/n)Σ_i X_i,  Z_k = (X_{2k−1} − X_{2k})²/2 (k = 1..m),  Z̄ = (1/m)Σ_k Z_k,

with the pairs fixed by test-pool row order before data.

**Theorem EB.** For δ₁, δ₂ ∈ (0, 1), let L₁ = ln(1/δ₁), L₂ = ln(1/δ₂),

  a = B·√(L₂/m),  b = B²·L₂/(12m),  σ_up = (a + √(a² + 4(Z̄ + b)))/2,

  U = X̄ + σ_up·√(2L₁/n) + B·L₁/(3n).

Then P(μ ≤ U) ≥ 1 − δ₁ − δ₂. **Registered choice:** δ₁ = δ₂ = δ/2.

**Lemma B1 (one-sided Bernstein moment bound).** Let Y ≤ b with b > 0, E Y = 0, E Y² = v. For 0 ≤ λ < 3/b: ln E e^{λY} ≤ vλ²/(2(1 − λb/3)).

*Proof.* Taylor's theorem with integral remainder gives e^x − 1 − x = x²·g(x) with g(x) = ∫₀¹ (1 − s)e^{sx} ds, and g is increasing on ℝ (its derivative ∫₀¹ (1 − s)s e^{sx} ds is positive). For λ ≥ 0 we have λY ≤ λb, hence e^{λY} = 1 + λY + λ²Y²g(λY) ≤ 1 + λY + λ²Y²g(λb). Taking expectations, E e^{λY} ≤ 1 + λ²v·g(λb) ≤ exp(λ²v·g(λb)). For 0 ≤ u < 3, g(u) = Σ_{k≥2} u^{k−2}/k! ≤ Σ_{k≥2} u^{k−2}/(2·3^{k−2}) = 1/(2(1 − u/3)), because k! ≥ 2·3^{k−2} for k ≥ 2 (equality at k = 2, 3; then k! = k·(k − 1)! ≥ 3·2·3^{k−3}). With u = λb the claim follows. ∎

**Lemma B2 (sub-gamma tail).** Let S = Σ_{i=1}^{r} Y_i with independent Y_i satisfying Lemma B1's hypotheses with common b and Σ_i E Y_i² ≤ V. Then for every L > 0, P(S ≥ √(2VL) + bL/3) ≤ e^{−L}.

*Proof.* If V = 0, every Y_i is 0 almost surely, so S = 0 < bL/3 almost surely and the claim holds; assume V > 0. By independence and Lemma B1, ln E e^{λS} ≤ Vλ²/(2(1 − cλ)) with c = b/3, for 0 ≤ λ < 1/c. Markov's inequality gives P(S ≥ t) ≤ exp(−λt + Vλ²/(2(1 − cλ))). Put t = √(2VL) + cL and choose λ = α/(1 + cα) with α = √(2L/V); then cλ < 1 and 1 − cλ = 1/(1 + cα). Now Vλ²/(2(1 − cλ)) = Vα²/(2(1 + cα)) = L/(1 + cα), since Vα² = 2L; and √(2VL) = Vα, so λt = α(Vα + cL)/(1 + cα) = (2L + cαL)/(1 + cα). Hence λt − Vλ²/(2(1 − cλ)) = (2L + cαL − L)/(1 + cα) = L, and P(S ≥ t) ≤ e^{−L}. ∎

**Step 1 (mean).** Y_i = μ − X_i satisfies E Y_i = 0, E Y_i² = σ², and Y_i ≤ μ ≤ B (X_i ≥ 0, μ ≤ B). Lemma B2 with r = n, b = B, V = nσ², L = L₁: with probability ≥ 1 − δ₁, n(μ − X̄) < √(2nσ²L₁) + BL₁/3, i.e.

  μ < X̄ + σ√(2L₁/n) + BL₁/(3n).  (E1)

**Step 2 (variance).** The Z_k are iid (disjoint pairs), E Z_k = E(X_{2k−1} − X_{2k})²/2 = σ², 0 ≤ Z_k ≤ B²/2. Let W_k = σ² − Z_k: E W_k = 0; W_k ≤ σ² ≤ B²/4 (Popoviciu: a variable in [0, B] has variance ≤ B²/4), so b = B²/4 is admissible; E W_k² = Var Z_k ≤ E Z_k² ≤ (B²/2)·E Z_k = (B²/2)σ². Lemma B2 with r = m, b = B²/4, V = m(B²/2)σ², L = L₂: with probability ≥ 1 − δ₂, m(σ² − Z̄) < √(2·m(B²/2)σ²·L₂) + (B²/4)L₂/3 = Bσ√(mL₂) + B²L₂/12, i.e.

  σ² < Z̄ + aσ + b,  a = B√(L₂/m),  b = B²L₂/(12m).  (E2)

The quadratic σ² − aσ − (Z̄ + b) is negative only strictly between its roots, whose larger root is σ_up and whose smaller root is ≤ 0 ≤ σ; so (E2) implies σ < σ_up.

**Step 3 (union).** On the intersection of the events of Steps 1 and 2 (probability ≥ 1 − δ₁ − δ₂ by the union bound; independence of the two events is not needed), μ < X̄ + σ_up√(2L₁/n) + BL₁/(3n) = U. ∎

**Remarks.**
- U is increasing in X̄ and in Z̄; §7.4 uses this to bound numerical error outward.
- The variance step uses a paired U-statistic instead of Maurer & Pontil's self-bounding concentration of the sample variance; it is elementary (Lemmas B1–B2 only) at a small cost in the constant (a = B√(L₂/m) = B√(2L₂/n) against Maurer & Pontil's B√(2L/(n − 1))).
- The theorem holds for every n = 2m ≥ 2; no asymptotics are used.
- The theorem's b (an additive variance correction) is not the generic upper-bound parameter b of Lemma B1.
- The widths of §7.7 are **scenario forecasts**, not distribution-free width guarantees; even at zero observed paired variance the width is ≈ 1.163e-4 at δ = 0.00625 (review value; [W] re-checked: σ_up = (a + √(a² + 4b))/2 = 0.042957), well below SHARP and TARGET for an oracle-quality predictor.

**Registered constants at N = 2²¹, B = 17 [W; the run recomputes them in Decimal]:**

| Use | δ | L₁ = L₂ = ln(2/δ) | a | b | B·L₁/(3n) | √(2L₁/n) |
|---|---|---|---|---|---|---|
| SHARP(s), TARGET(s) | 0.00625 | ln 320 = 5.768321 | 3.98725e-2 | 1.32485e-4 | 1.55865e-5 | 2.34544e-3 |
| LEARN-TEST(m), ladder | 0.025 | ln 80 = 4.382027 | 3.47525e-2 | 1.00645e-4 | 1.18406e-5 | 2.04427e-3 |

### 7.4 Certified computation of U (MD 14; X§11)
1. **Exact per-row target.** X_i = Σ_{j: q*_j > 0} q*_j ln q*_j − Σ_j q*_j ln p^Q_j, with q* the exact closed-form law (S0 Theorem 1; a finite set of rational entries: 1/5, (1/5)(λ_m + (1 − λ_m)/3), (1/5)(1 − λ_m)/3 for m = 1..32, 1/15) and p^Q rational.
2. **Certified tables** (gate SCORE): ln p^Q(k) for k = 0..Q (p^Q(k) = (1 − ε)k/Q + ε/18) and q ln q for every q* entry value, each evaluated as an exact rational converted by 90-digit (130-digit) rational division and `Decimal.ln` at 80 and 120 digits (the S0§5.6 enclosure method), with |v₈₀ − v₁₂₀| ≤ 10⁻⁶⁰ asserted; the stored float64 value is the float64 value nearest to v₈₀ (not a separately proved correctly rounded transcendental value; the row budget does not need that). The enclosure rests on the known rounding errors of rational division, `Decimal.ln` and float conversion (S0§5.6 item 3); the 80/120-digit agreement is a diagnostic, not the proof. At these precisions the analytic rounding allowance (≲ 10⁻⁷⁸ per entry before float conversion, ≤ ½ ulp after) is far smaller than e_row. Tables are stored with sha256 (8.4 MB [W]).
3. **Float scoring.** x̂_i = Σ_j (T_qlnq[q*_j] − fl(q*_j)·T_lnp[k_j]) in float64. Per-row error bound |x̂_i − X_i| ≤ e_row := **1e-12** (T15: ≤ (18 + 3)·u·19.6 ≈ 4.6e-14 [W], u = 2⁻⁵³, Σ|terms| ≤ ln 18 + ln(18/ε) ≈ 19.6). SCORE also recomputes X_i in 80-digit Decimal for the first 2¹⁴ gate rows passed through the quantiser with a synthetic reference predictor (q_∅) and asserts |x̂_i − X_i| ≤ 1e-13.
4. **Outward inputs** (exact rational arithmetic on the float64 values, Python `Fraction`): X̄⁺ = (Σ_i x̂_i)/n + e_row; Z̄⁺ = (1/m)Σ_k (|x̂_{2k−1} − x̂_{2k}| + 2e_row)²/2. Then X̄ ≤ X̄⁺ and Z_k ≤ (|x̂_{2k−1} − x̂_{2k}| + 2e_row)²/2 for every k, so Z̄ ≤ Z̄⁺.
5. **Outward formula.** U⁺ is computed from X̄⁺ and Z̄⁺ in a 60-digit `Decimal` context with rounding toward +∞ (ROUND_CEILING) for every operation; L = ln(2/δ) is the 60-digit `Decimal.ln` plus 10⁻⁵⁵; each square root is the correctly rounded 60-digit root plus 10⁻⁵⁵.
6. **Reported bound.** U_report = U⁺. No separation correction is required under §7.1's unconditional reporting guarantee. The registered collision-mass calculation remains a descriptive lineage diagnostic.
7. **Comparison.** SHARP(s) iff U_report < G0⁻ and TARGET(s) iff U_report < (3/4)·G0⁻ (exact rational product), as exact comparisons of the Decimal against the stage-0 enclosure's lo (a Decimal string). Equality counts as not supported. There is no unresolved band: every numerical error is inside U_report.

The same computation gives U for LEARN-TEST (δ = 0.025; threshold G_8.lo) and the ladder (δ = 0.025; descriptive).

### 7.5 Bootstrap for C-ORD and the registered tail diagnostic (MD 7; L§6.1; L-E1)
- **Draws.** B = 20,000 draws (stream ("x6s1", "boot", "cord")). Each draw resamples the NA test rows with replacement (N = 2²¹) and recomputes every predictor's numerator and denominator on the **same** resampled rows (pairs move with their rows), so controls are paired and ctrl(s) is evaluated inside each draw.
- **Exact reduction.** Rows with Δq* = 0 contribute zero to every numerator and denominator, so a draw is generated exactly in distribution as M ~ Binomial(N, n_inf/N), then M indices uniform with replacement among the n_inf informative rows (≈ 47,809 [W]); counts per row by `bincount`; sums by matrix product with the per-row [16, n_inf] numerator array and the denominator vector. This is the full-row multinomial bootstrap, not an approximation (T-STAT tests the equivalence exactly on small cases).
- **Levels.** One-sided percentile bounds by a thin `np.quantile` wrapper in `x6s1_stats.py` with the registered levels (L-E1: the existing `analysis.percentile_interval` is hard-coded to [0.025, 0.975]); "linear" interpolation, fixed.
- **TAIL diagnostic (registered; failure → C-ORD UNRESOLVED and PRECISION_LIMITED):**
  - D1 (bounded-influence sanity check; OS 1): for every predictor m in C-ORD, max_i |num_i(m)| ≤ 0.01·Σ_i den_i (num_i, den_i on the observed test rows). It is not evidence that the bootstrap has correct tails. It is effectively redundant after G0-FEAS: an informative NA pair has denominator ≥ 2λ_32² ≈ 0.549 [W] and |num_i| ≤ 2, so with ≥ 24,000 informative pairs the margin is deterministic and large (0.01 × 24,000 × 0.549 ≈ 132 ≫ 2 [W]).
  - D2 checks a gross percentile-versus-normal discrepancy; it does not validate coverage, especially around ties in the maximum over controls.
  - D2 (shape): |LB_perc − LB_norm| ≤ 0.02, where LB_norm = mean β̃ − 1.959964·sd_boot(mean β̃). Forecast difference ≪ 0.01 for ≈ 47,800 bounded pairs [H].
- **Per-model descriptive intervals:** B = 2,000.
- **Gate bootstrap** (§4.7) uses the same wrapper; it has no tail diagnostic (it is a gate, MD 3).

### 7.6 Per-seed flags and precision (L§6.3; descriptive, used in ≥ 3-of-4 rules)
- **orderN(s):** β̃(s) ≥ 0.25 and per-model LB_0.975(β̃(s)) > 0.05.
- **lowN(s):** point β̃(s) < 0.10.
- **precision_ok(s):** 95 % bootstrap half-width of β_ord(NA-s) ≤ 0.10 **and** U_{0.025}(NA-s) − X̄(NA-s) ≤ 0.25·G_Parikh = 6.5897e-4 [W].

### 7.7 Test sizes and power [W; forecasts, no gate uses them]
**C-ORD at N = 2²¹** (47,809 informative pairs; L's noise model, se scaled by √(2¹⁷/2²¹) = 1/4 from L's table): se(β) ≈ 0.0007 (s = 0.1, τ = 0) to 0.0042 (s = 0.5, τ = 0.5). The listed standard errors are forecasts under L's stated noise model. There is no general "at most double the variance" guarantee for the control-adjusted maximum, because predictor statistics share rows and can be correlated. The bootstrap estimates the registered contrast's sampling variation. The LB>0.05 requirement is expected to be less restrictive than the point threshold near 0.25. At a true adjusted mean exactly 0.25, the point-threshold requirement generally gives approximately 50% passage under a regular symmetric sampling approximation, not approximately 100%. Power approaches one only with a positive margin above 0.25.

**SHARP and TARGET (empirical Bernstein, δ = 0.00625).** Width W = U − X̄ for a per-row SD σ (stage 0: q_Parikh SD ≈ 0.016, q_8 ≈ 0.028, q_∅ ≈ 0.036; trained models taken as 0.016–0.06 [H]):

| σ | σ_up | W | W / G0⁻ | 80 % power for SHARP if Δ_nat ≤ | 80 % power for TARGET if Δ_nat ≤ |
|---|---|---|---|---|---|
| 0.016 | 0.0480 | 1.281e-4 | 0.049 | 2.4985e-3 (0.948 G) | 1.8395e-3 (0.698 G) |
| 0.025 | 0.0539 | 1.421e-4 | 0.054 | 2.4793e-3 (0.941 G) | 1.8203e-3 (0.691 G) |
| 0.040 | 0.0661 | 1.706e-4 | 0.065 | 2.4421e-3 (0.926 G) | 1.7831e-3 (0.676 G) |
| 0.060 | 0.0842 | 2.131e-4 | 0.081 | 2.3880e-3 (0.906 G) | 1.7290e-3 (0.656 G) |

(80 % power: Δ_nat ≤ G − W − 0.8416·σ/√n, taking Z̄ ≈ σ².) This corrects L's "SHARP attainable for Δ ≤ 0.89·G" (L-E6): at this size and method SHARP has ≥ 80 % power for Δ_nat ≤ 0.91–0.95·G0⁻ and TARGET for Δ_nat ≤ 0.66–0.70·G0⁻.

**LEARN-TEST (δ = 0.025):** W = 0.998e-4 to 1.767e-4 (1.1–2.0 % of G_8) [W].

**Gate (val 2¹⁵, bootstrap):** margin 2.4–6.1 % of G_8 at SD 0.02–0.05 [W, AN]; 3.4 % at the stage-0 window SD 0.028.

**Designed:** exact censuses (3,090 W2 pairs, 12,360 control pairs); the band is 1e-9.

### 7.8 Certification summary (MD 14)
- Stage-0 constants: certified enclosures; every "below" test uses lo.
- Log-loss claims: outward empirical-Bernstein bounds with certified log tables (§7.4); no unresolved band.
- Deterministic designed comparisons: fixed absolute band 1e-9 (NUMERICALLY_UNRESOLVED inside), a decision rule like S0 T15.
- Float64 model evaluation: deterministic at fixed threads and batching (DET); float32-versus-float64 difference reported.

### 7.9 Ordered decision rules (the first match applies)
1. S0, PF or SMOKE-INGEST failure → INVALID. G0-ORC, SCORE or G0-POS → CONSTRUCTION_FAIL. G0-FEAS → FEASIBILITY_NO_GO. Registry or separation → FAIL_TECHNICAL/LINEAGE or INCONCLUSIVE/REGISTRY_INCOMPLETE. A registered model that can never be verified (owner abandons HOLD, S12) → INCOMPLETE.
2. LEARN not GO → NOT_LEARNED or LEARNING_UNRESOLVED (§4.7).
3. Natural-pipeline validity failure (E3.1 DET, E3.5 XCHECK, QUANT_INVALID) → PIPELINE_INVALID.
4. From LEARN-TEST of the four NA models: fewer than 3 defined PASS with PASS + UNRESOLVED < 3 → **LEARNING_NOT_ROBUST**; an UNRESOLVED count that leaves the branch undetermined → LEARNING_UNRESOLVED; otherwise continue.
5. C-ORD supported, no natural placebo failure, and ordD(s) defined PASS in ≥ 3 of 4 → **ORDER_USE_NATURAL_AND_DESIGNED**.
6. C-ORD supported and no natural placebo failure → **ORDER_USE_NATURAL**.
6′. C-ORD supported but a natural placebo failed → **INCONCLUSIVE** with CONTROL_LIMITED(natural) (MD 5; L-E3).
7. C-ORD resolved and not supported, and ordD PASS in ≥ 3 of 4 → **ORDER_USE_DESIGNED_ONLY**.
8. C-ORD is resolved and unsupported; lowN holds in at least three seeds; all four ordD flags are resolved, with at most one PASS; precision_ok holds for every NA model; and every required validity and placebo check passed → **ORDER_NOT_DETECTED**.
9. Otherwise → **INCONCLUSIVE**.

Then: the qualifiers of §3 are appended (SHARP_NATURAL, NATURAL_TARGET, GAIN_BELOW_REGISTERED_TARGET, W2_GAP_BEATEN, CHALLENGE_BEATEN, CONTROL_LIMITED, READOUT_LIMITED, CONTROLS_LEARNED, LADDER, PRECISION_LIMITED, DESIGNED_UNRESOLVED, LENGTH_PROFILE, MIXED_DEVICE, MIXED_ENV); comparisons are strict exactly as written; a missing or INVALID model fails every per-seed condition; a designed placebo failure of seed s makes only ordD(s) UNRESOLVED.

---

## 8. Gates in exact order

Execution is by separate coordinator-dispatched jobs, each reviewed before the next. Local jobs are metered (measure-only), run in the clean execution worktree at H (§14.4), with TEMP/TMP/TMPDIR and pytest basetemp under `X:/Downloads/topo-scratch/<job>/`. Every gate records PASS, FAIL, INVALID, HOLD, UNRESOLVED or NOT_RUN; the run stops at the first non-PASS validity gate and later gates are NOT_RUN. Cloud waves are owner sessions (§5.10).

**AUTH is an admission prerequisite**, before E0 execution, CLOUD-SMOKE, scientific training, and the training portions of TRAIN-EQUIV/RUNTIME-ACCT. The owner addendum names the frozen protocol hash, local budget, cloud use and smoke/preflight work. Planning, implementation and static review may precede AUTH. Move the AUTH admission check before E0; its later numbered row is a verification of the existing authorisation, not its first acquisition. (Row 0b below is the admission check; row 10 is the verification. Per RU O-3/O-16 the addendum also covers the transfers, the owner sessions, and the owner's confirmation of Google account access and free-tier use.)

**Pool-construction order.** After admission and S0, build REG1 before drawing any registered stage-1 pool. Draw the non-test pools, including smoke and gate pools, then run PF and the oracle/scoring checks. Build REG2 before drawing the test pools. Draw test once, run SEP, and perform only the explicitly permitted oracle-only preparation below. This dependency order controls the numbered presentation of gates. (Executed order in E0: AUTH-ADMIT → S0 → REG1 → non-test pools → PF → G0-ORC → SCORE → G0-POS → REG2 → test → SEP → G0-FEAS → HEADROOM-D → CLOUD-PREP. The permitted test preparation is §12 item 11.)

| # | Where / job | Gate | Content | Threshold / tolerance | On failure |
|---|---|---|---|---|---|
| 0 | IMPL | IMPL | `API.md` first (incl. §cloud cell templates); tests A/B written before the modules; modules ≤ 400 lines; notebook; coordinator full suite (detached); code freeze H with notebook sha256 | §14 | S7 |
| 0b | owner → E0 | AUTH-ADMIT | Owner authorisation addendum present before any E0 execution (content as above); recorded as `AUTH.json` in the store at E0 start | exact | do not run (S10) |
| 1 | E0 | S0 | (i) protocol frozen, sha256 match, byte copy `tools/x6_stage1/PROTOCOL_X6S1_v1.md`; (ii) request sha256 `1D567D29…E401`; (iii) R→H diff over the protected paths only allowlisted `A` entries (§14.5); (iv) **AUTH/RUNTIME:** the repair commit P is an ancestor of R, the repair files' blob sha256 equal FREEZE.json, and `tools/d2a` is byte-identical P→H; (v) stage-0 binding: `x6-stage0-oracle-store/run/report.json` sha256 `e7846911…3aca`, `GATES.jsonl` `c871f5e4…2462`, `model.npz` `e1b9a753…230b`, outcome GO_X6_NATURAL, and exact equality of every authoritative stage-0 JSON value with the complete Decimal string or enclosure frozen in the `API.md` constant map (§2.1, T24); (vi) fresh seed masters; (vii) dispatch identities, meter-binding sha256 and import directory (ruling X5′ pattern); (viii) store lineage (§12 item 8); (ix) notebook sha256 at H equals FREEZE.json | exact | INVALID (S0) |
| 2 | E0 | PF | Unchanged suites `tests/{learner (incl. test_trainer_golden), dataset, contracts, oracle, oracle_profile, world, process, x6_stage0, d2a (incl. the repair's tests), k4b, c1prime_registry}`; `tests/x6_stage1`; `tools/check_file_sizes.py`, `tools/check_imports.py`; **NB-STATIC** (T-NB); **TRAIN-EQUIV** (§4.6); **RUNTIME-ACCT** (§4.6); TEMP and basetemp recorded | all pass; T9, T22 | INVALID (S1) |
| 3 | E0 | G0-ORC | (a) NA/AB/ZC model arrays equal stage-0's `model_sha256`; (b) closed-form q_t vs `BayesFilter` for all t ≤ 32 on gate rows; (c) **rebuilt NA class tables** (`segment_dp` + `classes`) persisted canonically with sha256, their G_Parikh(32) equal to the stage-0 enclosure; (d) partner sampler: exhaustive uniformity for n ≤ 6 (Fraction products = 1/\|class\|), c_n totals = `avoid_counts`, every gate-row partner valid with equal `rs_key("Parikh")` and P(h′) = P(h) (`closed_form`); (e) β_ord(q*) = 1, β_ord(q_Parikh) = 0, \|Δq_8\| on n ≥ 8 rows; (f) D: `fraction_filter` = `closed_form`, prefix invariance, W2 TV = λ_18, control-set spread 0, the W2 β table; (g) G_8(32) from `avoid_counts`; the enclosures of Δ_W3 (Δ_challenge) and Δ_W2 (W2 set gap) reconstructed from the unchanged exact laws and Decimal method, giving Δ_W3^lo and Δ_W2^lo | (b) T1; (c), (g) T6; (d) T2; (e) T3–T5; else exact | CONSTRUCTION_FAIL (S2) |
| 4 | E0 | SCORE | Quantiser (conservation, zero rule, ties, R range, positivity) on synthetic and gate laws; certified log and qlnq tables (§7.4 item 2); per-row scoring error check (§7.4 item 3); oracle-readout floor: max over gate(NA) rows of KL(q*‖quant(q*)) ≤ 1.012287e-6 + 1e-12; EB arithmetic self-test against an independent Decimal evaluation | T13–T17 | CONSTRUCTION_FAIL (S2; "SCORING_INVALID") |
| 5 | E0 | G0-POS | Full evaluation pipeline with oracle predictors on gate(NA) 2¹⁶: (a) per row KL(q*‖quant(q*)) ≤ floor; (b) raw path: Δ_nat(q_S) against G_S(32) for S ∈ {∅, parity, counts, H1, Parikh} and Δ_nat(q_8) against G_8 (6 comparisons, as stage-0 G6); (c) quantised path: for each of the 6 predictors, Δ^Q − Δ^raw on the same rows lies within the exact per-row quantisation bounds averaged over the rows (T18) | (a) T17; (b) 4·SE + 2e-12; (c) exact bounds + 2e-12 | CONSTRUCTION_FAIL (S2) |
| 6 | E0 | REG | REG1 → pools (§6.1, all but test) → REG2 → test draw → SEP, inside the reservation window; ρ̄ computed | exact | FAIL_TECHNICAL/LINEAGE or INCONCLUSIVE/REGISTRY_INCOMPLETE (S3R) |
| 7 | E0 | G0-FEAS | Oracle-only: (a) informative NA test pairs (Δq* ≠ 0, n ≥ 8, t = 32) ≥ 24,000 (forecast 47,809 ± 219 [W]); (b) Σ‖Δq*‖² > 0 on test and val; (c) FEAS-POWER on val(NA): bootstrap se of β_ord for a synthetic predictor that is q* or q_Parikh per row by a fair registered coin (expected β = ½) ≤ 0.04 (forecast 0.019 [W, L]); (d) D complete (1,030 prefixes; 3,090 W2 pairs; 12,360 control pairs; 72 W3 histories) | as stated | FEASIBILITY_NO_GO (S3) |
| 8 | E0 | HEADROOM-D | β_8 and mean ‖d‖² on val(NA) (oracle only) → `sealed/headroom.json` | record only | — |
| 9 | E0 | CLOUD-PREP | init(1..4) and digests; expected batch and PCG64 digests for every chunk of every model (and the smoke); bundles C0, C1, C2 with allowed-class check (T-BUNDLE) and BUNDLE_SHA256 each | exact | INVALID |
| 10 | coordinator | AUTH-VERIFY | Verification of the existing authorisation (row 0b) before releasing the C0 bundle hash: same frozen sha256, budget and cloud use; no new acquisition | exact | do not run (S10) |
| 11 | Colab | C0 | Smoke wave (§5.9) | — | — |
| 12 | E0b | SMOKE-INGEST | The four integrity gates on the smoke; float64 local forward finite; resume exercised; session record complete | exact | INVALID (S1) |
| 13 | Colab | C1 | Train NA-s1, NA-s2, ZC-s1 (bundle C1) | — | HOLD on disconnect |
| 14 | E1 | INGEST-C1 | Per model: WEIGHTS-HASH → CLOUD-PROV → DATA-ID → TRAIN-COMPLETE (§5.8), then the **admission lock** (§5.7) before any evaluation | exact | §5.8 statuses (S11) |
| 15 | E1 | LEARN | §4.7 on val; sealed | UB_0.975 < G_8.lo | NOT_LEARNED or LEARNING_UNRESOLVED (S4) |
| 16 | E1 | LC-1 | Learning-curve record for C1 models (sealed) | record only | — |
| 17 | Colab | C2 | Train the 9 remaining models (bundle C2 released after GO) | — | HOLD on disconnect |
| 18 | E2 | INGEST-C2 | As 14 (incl. the admission lock), for the 9 models | exact | §5.8 statuses (S11) |
| 19 | E2 | LC-2 | Learning-curve record for C2 models (sealed) | record only | — |
| 20 | E3 | E3.0 BIND | Bindings; all 12 models ingested with four PASS and an admission lock (or terminal INVALID:NONFINITE); every final checkpoint's sha256 and weights digest equal its admission lock; store hashes of every pool; local evaluation environment record (§2.2, OS 3) | exact | INVALID (byte-identical transport recovery allowed, §12 item 10) |
| 21 | E3 | E3.1 DET | One registered model evaluated twice on 1,024 NA test rows (same threads and batching) | \|Δ\| ≤ 1e-12 on probabilities and identical quantised counts (T8) | PIPELINE_INVALID |
| 22 | E3 | E3.A EVAL | Per-predictor evaluation chunks (12 models + 4 init; §13.3): own-arm test pass, NA pairs, designed set, emergence, length profile, val γ; outputs persisted by exclusive create with sha256 | per chunk | environment rerun (S8) |
| 23 | E3 | E3.2 LEARN-TEST | learned(m) for all 12 models: U_{0.025}(m) on own-arm test < G_8.lo | §7.3 | → rule 4; CONTROLS_LEARNED |
| 24 | E3 | E3.3 READOUT | Cue mass (§2.6) for all 16 predictors, natural and designed | median ≥ 0.10 | order statistics UNRESOLVED; READOUT_LIMITED |
| 25 | E3 | E3.4 PLACEBO | Natural: \|β_ord(c)\| ≤ 0.10 for the 12 controls; designed: \|β_W2(c)\| ≤ 0.10 for init(s), AB-s, ZC-s and ρ_spur^{W2}(AB-s), ρ_spur^{W2}(ZC-s) ≤ 0.25 | 0.10 / 0.25 | natural: CONTROL_LIMITED → rule 6′; designed: ordD(s) UNRESOLVED |
| 26 | E3 | E3.5 XCHECK | Vectorised β against `x6_exact.beta` on the full row set, every predictor. Omit zero-oracle-difference pairs before invoking `x6_exact.beta`; this preserves the exact result and avoids constructing millions of irrelevant Fraction records | absolute 1e-9 (T7) | PIPELINE_INVALID |
| 27 | E3 | E3.6 STATS | §2.3–§2.8 for every predictor; ρ_spur^C per NA model | — | — |
| 28 | E3 | E3.7 PREC | precision_ok | §7.6 | PRECISION_LIMITED |
| 29 | E3 | E3.8 CONFIRM | C-ORD (bootstrap + TAIL); SHARP(1..4) and TARGET(1..4) (EB) | §7.2 | — |
| 30 | E3 | E3.9 RULES | §7.9, qualifiers, licence text, report; unseal | — | — |

E3 may span several metered jobs (each ≤ 12 h wall, MD 11): E3-a (gates 20–22 for the first chunk wave), further E3.A waves, and E3-z (gates 23–30). Model predictions on test histories are first computed in E3-a (§12 item 11).

---

## 9. Stop rules

| Rule | Trigger | Action |
|---|---|---|
| S0 | Any S0 item fails | INVALID; do not run |
| S1 | PF (incl. NB-STATIC, TRAIN-EQUIV, RUNTIME-ACCT) or SMOKE-INGEST fails | INVALID; nothing scientific runs; no scientific cloud wave is released |
| S2 | G0-ORC, SCORE or G0-POS fails | CONSTRUCTION_FAIL; preserve the discrepancy; escalate; no edit of theorems, values or tolerances after data |
| S3 | G0-FEAS fails | FEASIBILITY_NO_GO. No pool growth, no threshold change, no other process or readout |
| S3R | Registry collision or incompleteness | FAIL_TECHNICAL/LINEAGE (technical-correction route, §12) or INCONCLUSIVE/REGISTRY_INCOMPLETE |
| S4 | LEARN does not GO | NOT_LEARNED or LEARNING_UNRESOLVED; stop; C2 never released (§4.7) |
| S5 | NONFINITE_LOSS (cloud) | That model INVALID:NONFINITE, no retry, counts as failing |
| S6 | A local process > 3 GiB (supervisor), job > 12 GiB (Job Object) | That child INCOMPLETE; escalate as a technical event; no configuration change without the §12 route |
| S7 | A production change, an unlisted module or a `.py` file over 400 lines is needed (notebook over its §5.11 limits) | Stop before writing; escalate |
| S8 | Owner STOP, usage limit, disk floor (C: < 2 GB, X: < 30 GB), a `--max-wall` kill of a local job | INVALID (interrupted). Environment rerun under the same specification reproducing identical values (§12 item 6); the rerun may raise `--max-wall` |
| S9 | Leakage: test tokens, predictions or statistics before E3 beyond the oracle-only preparation of §12 item 11; Any **model-dependent** order statistic before E3 is leakage. The explicit exceptions are the registered oracle/reference identities in G0-ORC and G0-POS, oracle-only feasibility preparation, the synthetic FEAS-POWER calibration on validation rows, and sealed HEADROOM-D. These exceptions cannot select or alter data, models, thresholds or partners; opening `sealed/` before E3 or a stop; training on anything but `PublicTokenDataset` of the registered train pool; storing or using latent states; **uploading** any file outside the allowed bundle classes (§5.3, §5.12) | INVALID (leakage) |
| S10 | No owner authorisation addendum (AUTH-ADMIT, §8) | No E0 execution, CLOUD-SMOKE, scientific training, or training portion of TRAIN-EQUIV/RUNTIME-ACCT runs. Planning, implementation and static review may precede AUTH |
| S11 | A cloud integrity gate fails (§5.8) | The §5.8 status. FAIL_TECHNICAL/* → retrain route (§12 item 9) only for a model that has never had an admitted final chain and has had no local evaluation of any candidate checkpoint; otherwise transport recovery of byte-identical admitted artifacts only, or the model is INVALID. A systematic DATA-ID or CLOUD-PROV failure stops the wave until a technical correction |
| S12 | A wave cannot be completed in Colab within 14 calendar days of its release (GPU unavailable, repeated usage limits) | HOLD:CLOUD_UNAVAILABLE; the owner decides: keep waiting; an owner-authorised local-CPU fallback with the same `train_chunked` (≈ 6.5 CPU-h per model [L]; a protocol departure needing its own addendum); or abandon → INCOMPLETE |
| S13 | Owner-run deviation detected (edited cells, a wrong bundle, manual changes on Drive) | FAIL_TECHNICAL/CLOUD_PROV for the affected models → S11 route |

No scientific early stopping, extra seed, extra model, longer training, checkpoint choice, threshold change, readout change, pool change or partner redraw is allowed after any result. **Any post-data change of a threshold or tolerance needs the owner** (MD 17; addendum 10).

---

## 10. Threshold register, tolerance attainability and oracle-scale check (MD 17; fixed before any data)

### 10.1 Threshold register

| Item | Value |
|---|---|
| Process | NA/AB/ZC of S0§2; η = 1/50; t* = 32 |
| Model and recipe | §4.2; 30,000 updates; 2²⁰ train histories; K = 1,000 |
| Readout | Q = 2²⁰; ε = 10⁻⁶; B = 17 |
| Gate | UB_0.975(Δ_nat) < G_8.lo; val 2¹⁵; bootstrap B = 2,000 |
| C-ORD | mean β̃ ≥ 0.25; LB_0.975 > 0.05; β̃ > 0 in ≥ 3/4; TAIL D1 ≤ 0.01·Σden, D2 ≤ 0.02; B = 20,000 |
| SHARP / TARGET | U_{0.00625} < G0⁻ / < (3/4)·G0⁻ (exact rational product); N = 2²¹; δ₁ = δ₂ = δ/2 |
| LEARN-TEST | U_{0.025} < G_8.lo on own-arm test, N = 2²¹ |
| ordD | β_W2 ≥ 0.25; regret PASS R_W2 ≤ (3/4)Δ_W2^lo − 10⁻⁹, FAIL R_W2 > (3/4)Δ_W2^lo + 10⁻⁹ ((3/4)Δ_W2 ≈ 0.0458395285 [W]); min_y β_W2,y ≥ 0.25; band 1e-9 |
| Validity | cue mass ≥ 0.10; ρ_spur^C ≤ 0.25; ρ_spur^{W2} ≤ 0.25; placebo \|β\| ≤ 0.10 |
| Qualifiers | W2_GAP_BEATEN: R_W2 < Δ_W2^lo − 10⁻⁹; CHALLENGE_BEATEN: Δ_W3(m) < Δ_W3^lo − 10⁻⁹ |
| Unchanged in v2 (OS 4) | Every scientific threshold of v1 is preserved; v2 repairs specifications and implementation only and adds no more permissive criterion |
| Flags | lowN < 0.10; precision 0.10 (β) and 6.5897e-4 (Δ) |
| Feasibility | informative pairs ≥ 24,000; FEAS-POWER se ≤ 0.04; D complete |
| Runtime | RUNTIME-ACCT ≥ 10 CPU-s, ≥ 200 MB, kill ≤ 2 polls + 10 s |
| Resources (environment) | §13.4 |

### 10.2 Tolerance attainability (the R13 lesson; K4b §5.6 and S0§8.7 pattern)
No stage-1 gate compares two linear solvers or solves a linear system. Every float comparison is between a production kernel and exact rationals or Decimal, between two runs of the same deterministic code, or a bitwise identity. Error bounds are hand bounds [W] (u = 2⁻⁵³ ≈ 1.11e-16), not gates.

| # | Identity or comparison | Tolerance | Conditioning and error bound | Why attainable |
|---|---|---|---|---|
| T1 | Closed-form q_t vs `BayesFilter` (t ≤ 32, gate rows) | 1e-12 | S0 T16 bound 1.8e-13; measured 3.3e-16 (jobs/0066 G5) | margin ≥ 5 |
| T2 | Partner exactness, key equality, P(h′) = P(h), uniformity n ≤ 6 | exact | Python ints and Fractions | no rounding |
| T3 | β_ord(q*) = 1 | 1e-12 | identical numerator and denominator arrays | by construction |
| T4 | β_ord(q_Parikh) = 0 | exact | identical class lookups; Δ = 0.0 exactly | by construction |
| T5 | \|Δq_8\| on n ≥ 8 rows | 1e-12 | `suffix_posterior` uniform fibre; stage-0 window error ≤ 1.1e-16 | margin > 10³ |
| T6 | Rebuilt-table G_Parikh(32), G_8, Δ_challenge, W2 set gap vs stage 0 | 1e-40 | the same Decimal code paths as stage-0 G3/G4 (enclosure width 2e-60) | margin > 10²⁹ |
| T7 | Vectorised β vs `x6_exact.beta` | absolute 1e-9 | `beta` computes exactly in Fractions from the same float64 inputs (only the ≈ 47,809 informative rows contribute), so the difference is the vectorised side's float error: with `math.fsum` for both sums (registered) ≲ 1e-14; even naive summation gives ≤ n_inf·u·Σ\|num_i\|/den ≲ 4.8e4 × 1.1e-16 × 2 ≈ 1.1e-11 [W] (\|num_i\|/den_i ≤ 1/λ_32 < 2 per row) | margin ≥ 90 |
| T8 | DET re-evaluation | 1e-12 and identical counts | fixed threads and batches: expected bitwise | margin > 10³ |
| T9 | TRAIN-EQUIV (CPU) | bitwise (model, every optimiser tensor and scalar, scheduler state and current learning rates, PCG64 state, init, all batch arrays; §4.6) | identical operations, identical states restored, CPU kernels deterministic at fixed threads; a genuine precondition to verify, not a consequence of prose; establishes local CPU equivalence only, not CPU-versus-GPU trajectories | verified before any data |
| T10 | init(s) digest = Trainer's initialisation; step-0 record digest = init digest | exact | same torch, same seed, same code (local) | by construction |
| T11 | Batch digests and PCG64-state digests (cloud vs local) | exact | integer stream independent of device; one call per step | by construction; a numpy change is detected before GPU work |
| T12 | File sha256 and canonical weights digests | exact | bytes | — |
| T13 | Quantiser: Σk = Q, 0 ≤ R ≤ 18, zero rule | exact | integer arithmetic on floats ≤ Q; \|Σs − 1\| ≤ 1e-12 gives \|Σr − Q\| ≤ 1.05e-6 | by construction |
| T14 | Log tables: \|v₈₀ − v₁₂₀\| ≤ 10⁻⁶⁰ (diagnostic); float = nearest float64 to v₈₀ | 1e-60 | S0§5.6 method; the analytic rounding bound of rational division, `Decimal.ln` and float conversion (single-term logs, ≲ 10⁻⁷⁸ before conversion) is the enclosure argument (§7.4 item 2) | margin > 10¹⁷ |
| T15 | Per-row scoring error e_row | 1e-12 (empirical check 1e-13) | ≤ 21·u·19.6 ≈ 4.6e-14 | margin > 20 (> 2 for the check) |
| T16 | EB arithmetic | outward (ROUND_CEILING, +10⁻⁵⁵ per ln and sqrt) | 60-digit Decimal; inputs exact rationals | rigorous by construction; no tolerance |
| T17 | Oracle-readout floor | ≤ 1.012287e-6 + 1e-12 per row | exact bound of §2.2 on float(q*) (relative perturbation ≤ u) | bound proven; slack from 1/Q terms |
| T18 | G0-POS (b) raw path; (c) quantised path | (b) 4·SE + 2e-12; (c) within [−A⁻, A⁺] + 2e-12 | (b) stage-0 G6 z ≤ 0.8 on the same quantities; union false-FAIL ≈ 6 × 6.3e-5 = 3.8e-4 [W]. (c) For a law q with positive entries ≥ 1/750 and p^Q its readout, \|k_j/Q − q_j\| < 1/Q gives per row −Σ_j q*_j(1/Q + ε/18)/q_j ≤ KL(q*‖p^Q) − KL(q*‖q) ≤ Σ_j q*_j[−ln(1 − ε) − ln(1 − 1/(Q q_j))]; A⁻, A⁺ are the row means of the two bounds, computed exactly by the run (worst case per row ≈ 7.2e-4 at q_j = 1/750; typical ≪ 1e-5 [W]) | (b) asymptotic diagnostic; (c) a deterministic inequality, no sampling |
| T19 | Designed numerical band | 1e-9 | float64 β over ≤ 6,180 rows; error ≲ 1e-13 | a decision rule; values inside are NUMERICALLY_UNRESOLVED |
| T20 | Softmax precondition \|Σs − 1\| ≤ 1e-12 | 1e-12 | float64 softmax of 18 entries: ≤ ~20u ≈ 2.2e-15 | margin > 400 |
| T21 | Bootstrap Monte-Carlo error of percentiles | B = 20,000 | 2.5 % tail ≈ 0.019·σ_boot [W, L] | negligible |
| T22 | RUNTIME-ACCT | ≥ 10 CPU-s, ≥ 200 MB, ≤ 2 polls + 10 s | forecast ≈ 39 CPU-s; interpreter ≥ 300 MB [H]; poll 2 s | margin ≈ 4 |
| T23 | Registry and binding hashes | exact | — | — |
| T24 | Stage-0 constants (S0 item v) | exact | Displayed decimals are explanatory approximations and are never binding comparison inputs. `API.md` freezes a constant map giving each authoritative stage-0 JSON path and its complete Decimal string or enclosure. S0 verifies the stage-0 report hash and exact equality with those strings. Rebuilt constants are checked using T6. Derived thresholds use exact rational multiplication of the full certified endpoints, without intermediate rounding. | string equality; no rounding |
| T25 | QUANT_INVALID condition | (precondition) | T20 | never expected |
| T26 | Stage-0 regeneration counts | exact | unchanged deterministic code at H | by construction |
| T27 | TAIL D1 (bounded-influence sanity check), D2 | 0.01·Σden; 0.02 | D1: \|num_i\| ≤ 2 against ≥ 0.01 × 24,000 × 2λ_32² ≈ 132 after G0-FEAS (deterministic [W]); D2 ≪ 0.01 [H] | margins ≥ 66 and ≥ 2 |

**Rule (fixed now).** No threshold or tolerance changes after any stage-1 gate value (G0-ORC onward) exists. An unattainable tolerance keeps its gate status, and any change needs an **owner** decision (addendum 10; S0§8.7), never a coordinator ruling alone.

### 10.3 Oracle-scale check (the K4b lesson: Δ4^orc < margin; AN §6)
Every threshold is checked against what the oracle and the natural competitors attain. Oracle scale: G_Parikh(32) = 2.6359e-3, G_8 = 8.8553e-3, G_∅ = 1.05935e-2, W2 set gap 0.061119, Δ_challenge 0.0378321.

| Threshold | Oracle value | Competitor values | Attainable? | Note |
|---|---|---|---|---|
| Gate UB < G_8 | 0 | commutative 0.30·G_8; parity 0.88·G_8; transport-blind 1.196·G_8 (fails) | Yes | margin 2.4–6.1 % of G_8; discriminates transport from no transport |
| SHARP U < G0⁻ | ≤ 1.0123e-6 (readout floor) | every Parikh function ≥ G0⁻ (fails by definition) | Yes | W = 4.9–8.1 % of G; 80 % power at Δ ≤ 0.91–0.95·G |
| TARGET U < (3/4)·G0⁻ (≈ 1.97692236e-3) | ≤ 1.0123e-6 | Parikh functions fail | Yes, demanding | 80 % power at Δ ≤ 0.66–0.70·G |
| LEARN-TEST U < G_8 | ≤ 1.0123e-6 | as the gate | Yes | W = 1.1–2.0 % of G_8 |
| C-ORD mean ≥ 0.25, LB > 0.05 | 1 | every Parikh function 0 (exact); window functions 0 in expectation | Yes | se 0.0007–0.0042 per model (forecast); ≈ 50 % passage at a true adjusted mean of exactly 0.25, approaching 1 only with a positive margin above 0.25 (§7.7) |
| ordD β_W2 ≥ 0.25 (pooled and per cue) | 1 | set-constant 0; last/first pooled 0 (per cue ½, −1, ½); rev −1 | Yes | per-cue rule excludes the last/first heuristics on at least one cue |
| R_W2 ≤ (3/4)Δ_W2^lo − 10⁻⁹ (≈ 0.0458395285) | ≈ 1e-6 | every set-constant predictor ≥ Δ_W2 ≈ 0.0611193713 | Yes | a β = 0.5 interpolation scores ≈ 0.017 [AN] |
| Placebo \|β\| ≤ 0.10 | 0 | — | Yes | null se ≲ 0.003 at 2²¹ [W] |
| ρ_spur ≤ 0.25 | 0 | — | Yes | — |
| Cue mass ≥ 0.10 | 0.2 | uniform 0.167 | Yes | vacuous against uniform by design |
| Precision 0.10 / 6.59e-4 | — | forecast 0.0014–0.0082 / 1.0e-4–2.1e-4 | Yes | margin ≥ 3 |
| FEAS ≥ 24,000 pairs | forecast 47,809 ± 219 | — | Yes | ≥ 100 SD |
| FEAS-POWER ≤ 0.04 | forecast 0.019 | — | Yes | margin 2 |
| W2_GAP: R_W2 < Δ_W2^lo − 10⁻⁹ | ≈ 1e-6 | set-constant = Δ_W2 | Yes | qualifier |
| CHALLENGE: Δ_W3(m) < Δ_W3^lo − 10⁻⁹ | ≈ 1e-6 | bag/bigram/H1/counts ≥ Δ_W3 ≈ 0.0378320848; rev 0.05095 | Yes | qualifier |

**No threshold exceeds the oracle's own scale.** No 0.01-nat margin is used (it would exceed G_Parikh and repeat K4b's failure). X's near-vacuous regret condition 4·G0⁻ (X-E3) and the vacuous mean‖d‖² ≥ 1e-8 guard are not gates here.

---

## 11. Outcome taxonomy

**Study outcomes (exactly one; §7.9):**

| Outcome | Origin |
|---|---|
| INVALID | S0, PF, SMOKE-INGEST, S8 interruption without rerun, S9 leakage |
| CONSTRUCTION_FAIL | G0-ORC, SCORE, G0-POS |
| FEASIBILITY_NO_GO | G0-FEAS |
| FAIL_TECHNICAL/LINEAGE · INCONCLUSIVE/REGISTRY_INCOMPLETE | Registry, separation, lineage |
| INCOMPLETE | A registered model never verified (abandoned HOLD, S12) |
| NOT_LEARNED · LEARNING_UNRESOLVED | LEARN |
| PIPELINE_INVALID | DET, XCHECK, QUANT_INVALID |
| LEARNING_NOT_ROBUST | LEARN-TEST rule 4 |
| ORDER_USE_NATURAL_AND_DESIGNED · ORDER_USE_NATURAL · ORDER_USE_DESIGNED_ONLY · ORDER_NOT_DETECTED · INCONCLUSIVE | Rules 5–9 |

**Per-model statuses:** DONE (four integrity PASS); HOLD:CLOUD_INCOMPLETE; HOLD:CLOUD_UNAVAILABLE; TRANSFER_RETRY; FAIL_TECHNICAL/{WEIGHTS_HASH, CLOUD_PROV, DATA_ID, CHAIN}; INVALID:NONFINITE; INVALID (after evaluation, unrecoverable).

**Per-gate statuses:** PASS, FAIL, INVALID, HOLD, UNRESOLVED, NUMERICALLY_UNRESOLVED (designed band), NOT_RUN.

**Qualifiers (MD 10):** SHARP_NATURAL(k/4), NATURAL_TARGET(k/4), GAIN_BELOW_REGISTERED_TARGET(j/4), W2_GAP_BEATEN(k/4), CHALLENGE_BEATEN(k/4), CONTROL_LIMITED(domain, list), READOUT_LIMITED(list), CONTROLS_LEARNED(AB a/4, ZC b/4), LADDER(s), PRECISION_LIMITED, DESIGNED_UNRESOLVED(k), LENGTH_PROFILE, MIXED_DEVICE(list), MIXED_ENV(list).

---

## 12. Rerun and lineage rule (fixed in advance; S0§10.8 and K4b §11.8 patterns, adapted to cloud training and chunked evaluation)

1. **Store** `X:/Downloads/projects/topo-pilot/x6-stage1-store/` (new; verified absent or holding only this lineage): `FREEZE.json`, `AUTH.json`, `registry/`, `pools/` (ArtifactStore), `tables/`, `cloud/<wave>/<model>/` (verified cloud files), `stages/<stage>/` (exclusive-create payloads), `GATES.jsonl`, `STAGES.jsonl`, `sealed/`, `waves/`, `superseded/<job>-a<k>/`, `logs/`, `cpu_ledger.json` (pre-created, schema `x4-oracle-profile-ledger-v1`), `x6s1_meter_bind.py`. No `tmp/`; bundles and downloads live in scratch.
2. **Final outcomes** are never rerun to obtain another outcome: a PASS gate, LEARN's decision, a verified model's weights, every E3 value and the E3 outcome.
3. **Technical correction.** Only for a documented implementation or environment defect, by coordinator ruling naming the defect, the correction commit (inside the allowlist), the affected stages and artifacts, and evidence of independence from the outcome. **At most two correction jobs per defect.** A failure that shows a protocol statement to be wrong is not a defect: it stops stage 1 and returns to planning (owner).
4. **Supersede, append-only.** The affected attempt moves to `superseded/<job>-a<k>/` under `SHA256SUMS`, unique per attempt; nothing is deleted. Unaffected artifacts must regenerate **bit-identically**, compared with the archived hashes; a mismatch is FAIL_TECHNICAL/LINEAGE.
5. **Owner escalation** is required if a correction would change an already computed outcome-bearing quantity, or if the failed attempt computed one at or after its failure point. Outcome-bearing: gate values, learned values, β_ord, Δ_nat and every bound, every designed statistic, the controls, C-ORD, SHARP, TARGET. No owner escalation is needed solely because an unchanged outcome-bearing quantity was computed before that point.
6. **Environment reruns** (S8) of local jobs reproduce identical values and do not count against item 3. An interrupted E3.A chunk is archived and recomputed bit-identically from the stored checkpoints and pools, with the same partner draws and bootstrap streams; persisted per-row outputs let E3-z statistics be recomputed without re-running models.
7. **Cloud interruptions** (disconnects, idle timeouts, usage limits, GPU unavailability) are resumed under §5.4 and are neither failures nor corrections.
8. **The store recognises lineage.** Before a job writes, every existing store file must be recognised: meter bookkeeping, a `SHA256SUMS` manifest of a recorded superseded attempt, an archived file listed in such a manifest, or a recorded output of an earlier accepted job of this lineage with its sha256. Anything else is INVALID/LINEAGE (S0 item viii).
9. **Cloud retrain route.** A model with FAIL_TECHNICAL/{WEIGHTS_HASH, CLOUD_PROV, DATA_ID, CHAIN} may be retrained **from step 0** with the same seeds, data, init and recipe, under a coordinator technical-correction ruling, subject to the eligibility rule below. At most two retrains per model per defect. The failed lineage stays in its own immutable bundle directory on Drive and is archived locally; the retrain uses a re-issued bundle with a new bundle id (§5.3) and a fresh chain. Because GPU training is not reproducible, a retrained model has new weights; this is admissible only because nothing has been evaluated. INVALID:NONFINITE is terminal and never retrained.

   **Admission lock and eligibility (RC9).** Immediately after a model first passes all four integrity gates, record its admitted final checkpoint and weights digests by exclusive create, before LOSS-ECHO, learning curves, validation or test evaluation. This first verified final chain is immutable and is the model's only admissible chain.

   Retraining is available only for a model that has never had an admitted final chain and has had no local evaluation of any candidate checkpoint. "Local evaluation" includes LOSS-ECHO, dev curves, validation, test, emergence and other descriptive evaluations. A later integrity problem cannot reopen an admitted model for retraining.
10. **Restoration versus replacement (RC9).** Re-downloading or restoring byte-identical admitted artifacts is transport recovery and remains allowed after evaluation. Substituting different weights or a different chain is forbidden.
11. **Test access.** E0 may generate and hash test pools, check separation, draw and persist partners, classify rows by oracle-only eligibility/informativeness, and evaluate the registered oracle-only feasibility counts and denominators. Before E3 these operations release only their prescribed PASS/FAIL statuses and sealed artifacts. No model prediction on test histories is permitted before E3. E3 and its authorised environment reruns use the identical stored histories and partners.

---

## 13. Compute forecast and resource limits (this machine: i7-10750H, 6 cores, 31.9 GB RAM; Colab free tier)

### 13.1 Local CPU forecast [W arithmetic on H rates; MD 12]
Forward FLOP per sequence ≈ 5.52e7 [W] (2 × 802,304 × 33 plus attention). Float64 throughput 8–25 GFLOP per CPU-s [H] (central 13: about half of D-2a's measured float32 training rate of 26 GFLOP per CPU-s [AN]).

| Part | Basis | Forecast (CPU-h) |
|---|---|---|
| PF (+ TRAIN-EQUIV, RUNTIME-ACCT) | jobs/0066 PF ≈ 3 min; tests/d2a, k4b, learner golden, new tests; 2 × 60 + 3 × 50 CPU updates | 0.5–1.5 |
| E0: pools | 19.1M rows by `HMMSampler` [H] | 0.2–0.6 |
| E0: DP, class tables, partner counts, Decimal checks (G_Parikh, G_8, gaps) | stage-0 G4 took most of 3,316 CPU-s (incl. all ladders and K-blk) | 0.3–1.0 |
| E0: SCORE tables (2 × 2²⁰ Decimal logs), registry (19.7M digests + K4b readers), G0, FEAS, HEADROOM, CLOUD-PREP | [H] | 0.3–1.0 |
| E0b smoke ingest | hashing, one forward batch | < 0.1 |
| E1: ingest 3 models, gate (3 × 2¹⁵ forwards), LC-1 (11 × 3 × 2¹² forwards) | [W] 0.28 at 13 GFLOP/s | 0.2–0.6 |
| E2: ingest 9 models, LC-2 (11 × 9 × 2¹²) | [W] 0.48 at 13 | 0.3–0.9 |
| **E3.A forwards** | 32.55M forwards [W]: own-arm test 12 × 2²¹ = 25.17M; NA pairs for 8 abelian (2 × 199,664 each) 3.19M and 4 init 1.60M; NA partners for 4 NA models 0.80M; designed 16 × ≈ 37.2k = 0.60M; emergence 0.31M; length profile 0.25M; DET | **20.0–62.4 (central 38.4)** |
| E3: oracle laws (closed form; BayesFilter checks), quantisation, scoring, partner draws | 6.7M rows × 2e5 FLOP [W]; Python partner draws | 0.5–1.5 |
| E3: bootstrap (20,000 × 47.8k × 16), EB, decisions, report | [W] | 0.1–0.5 |
| **Total local** | | **≈ 23–70 CPU-h, central ≈ 43 CPU-h** |

The per-model own-arm pass is ≈ 2.5 CPU-h at 13 GFLOP/s [W]. The abelian own-arm passes are 51.5 % of the forwards [W]; evaluating them on the first 2¹⁹ rows instead would save ≈ 15 CPU-h, but **2²¹ abelian own-arm rows are retained** per owner addendum 13 (RU O-4); a 2¹⁹ reduction would need an owner amendment.

### 13.2 Cloud forecast [H]
Training FLOP per update 2.03e10, per model 6.1e14 [W]. On a T4 (small matrices, launch-bound) 8–40 ms per update [H] → 4–20 min per model, plus ≈ 31 checkpoint writes of 9.6 MB. **Total ≈ 0.8–4 GPU-h for 12 models** (+ ≈ 3 min smoke). Owner wall: C0 ≈ 20 min; C1 ≈ 20–60 min; C2 ≈ 1–3 h, possibly over several sessions. Drive ≈ 0.42 GB uploaded data + 3.58 GB checkpoints + ≈ 0.3 GB code/bundle copies ≈ 4.3 GB [W]. Downloads ≈ 0.9 GB (C1) and ≈ 2.7 GB (C2).

### 13.3 Wall and chunking (X-E2 correction; MD 11)
- E0: one job ≤ 12 h (forecast 1–3 h).
- E3.A: one chunk per predictor (12 models + 4 init), run in supervisor waves of ≤ 3 children × 2 threads (forecast 1.2–2 h wall per model chunk; init chunks ≈ 15 min). Waves are grouped into metered jobs of ≤ 12 h wall (forecast 2 jobs). Each chunk persists its outputs by exclusive create with sha256; an interrupted chunk is rerun bit-identically (§12 item 6).
- Total local wall ≈ 15–25 h over 6–8 jobs [H].

### 13.4 Resource limits (operational, not scientific; MD 11)
- **CPU:** measure-only (job-0014 meter with `--max-cpu inf`, the default 600 s overridden). The supervisor's per-process CPU limit is ∞; no per-child CPU stop (L's 20 CPU-h guard and the 8 CPU-h child-stop analogue are not adopted). **A 90 CPU-h notification alarm is adopted as notification only** (RU O-1): when the cumulative X6S1 ledger passes 90 CPU-h the coordinator notifies the owner; it never stops, pauses or changes anything.
- **Wall:** `--max-wall 43200` (12 h) per local job; a kill is S8.
- **Threads:** ≤ 6 (≤ 3 children × 2 intra-op + 1 inter-op); single-process stages 2 threads; fixed and recorded (they also fix float64 results).
- **Memory (MD 11; the memory question):** per process **3 GiB** (supervisor; precedent addendum 5, D-2a) and job **12 GiB** (`winjob.MEMORY_CAP` rebound as D-2a's `bind_meter`). Forecasts [H/W]: E3.A child ≤ 1.2 GB (float64 model 6.4 MB; batch 1,024 activations ≤ 0.2 GB; tokens 69 MB; per-row outputs ≈ 0.2 GB; oracle laws in chunks of 2¹⁶ rows); DP and tables ≤ 1.4 GB (stage-0's whole job peaked at 1.33 GiB); pool generation ≤ 0.5 GB per pool (2²¹ × 33 × 3 B with states). **Registry (RC10):** Keep the 3 GiB process and 12 GiB job limits. Registry construction uses bounded-memory ingestion and external/streamed ordering where necessary. Forecasts include foreign sources and sorting temporaries; no universal 1.9× margin is claimed without that accounting. Resource exhaustion follows S6 and does not permit an automatic limit increase. Accounting [W]: X6 rows 19,668,992 plus K-REG2's 6,024,521 digests = 25,693,513 identities before handoff JSON and reader-k tables; uint64 keys ≈ 206 MB and full digests ≈ 822 MB if held at once, so the registry streams the digests in sorted runs (run size registered in `API.md`, ≤ 2²² identities ≈ 134 MB of digests per run) and keeps only the merged uint64 key array (≈ 206 MB) and the confirmation runs on disk under the store's `registry/`. No raise is requested (RU O-2). Training memory is not local any more (L's 2.0–2.4 GB forecast and L-E2 are moot). Colab: training ≈ 1–1.5 GB RAM and ≈ 1 GB GPU memory [H] (int64 tensors 2 × 277 MB, `_materialise` list overhead), far below the free tier's ≈ 12 GB RAM / 15 GB GPU [H].
- **Disk:** C: ≥ 2 GB and X: ≥ 30 GB (meter floors, S8); ≥ 60 GB free on X: at E0 launch. Store forecast ≈ 8 GB [W] (checkpoints 3.58 GB; E3 per-row outputs 2.42 GB; pools 0.78 GB; registry 0.8 GB; tables 0.1 GB); scratch bundles and downloads ≈ 5 GB.
- **Output cap:** `meter.OUTPUT_CAP` = **16 GiB** (scaled to N = 2²¹ with archive allowance).
- **Scratch:** TEMP, TMP, TMPDIR and pytest `--basetemp` under `X:/Downloads/topo-scratch/<job>/` (outside the project root); bundles in `…/cloud_bundle/`, downloads in `…/cloud_in/`. Nothing temporary goes into the store or the repository.

---

## 14. Implementation footprint, reuse, binding and test authors (MD 13)

### 14.1 Files (new tools directory; no change to `src/` or to any existing file)

| File | Contents | Budget |
|---|---|---|
| `tools/x6_stage1/API.md` | Contract, committed first: names, signatures, shapes, dtypes, streams, sequence-id codes, report keys, volatile fields, static output manifest, the bound repair API names, **§cloud: the six notebook cell templates verbatim, ticket/record/manifest schemas** | — |
| `tools/x6_stage1/PROTOCOL_X6S1_v1.md` | Byte copy of the frozen protocol | — |
| `x6s1_data.py` | Constants and seed map; pool table; sampling via `HMMSampler`; ObservationSet storage; digests; stage-0 regeneration; init states | ≤ 400 (≈ 330) |
| `x6s1_pairs.py` | Class tables (rebuild, persist, validate); exact backward partner sampler; exhaustive n ≤ 6 check; designed set D (W1, W2, C1–C4, W3, W3′, natural prefixes); oracle cue laws for the references | ≤ 400 (≈ 330) |
| `x6s1_cloud.py` | Runs in Colab and locally: bundle verification, environment and session records, `train_chunked` (Trainer-equivalent), atomic checkpoint/record I/O, chain validation and quarantine, `run_wave`, `finalise`, `weights_digest`. Imports: stdlib, numpy, torch, `topo_pilot.{learner, contracts, dataset}` only | ≤ 400 (≈ 380) |
| `x6s1_ingest.py` | Local: CLOUD-PREP (bundles with the allowed-class guard; expected batch and PCG64 digests; tickets), ingest and the four integrity gates, store import, learning-curve record, LOSS-ECHO | ≤ 400 (≈ 330) |
| `x6s1_eval.py` | Predictor interface (float64 model wrapper via `load_model`; oracle wrappers q*, q_S, q_8, heuristics); forward at positions with padding; quantiser; per-row scoring; cue mass; designed statistics; E3.A chunk outputs | ≤ 400 (≈ 370) |
| `x6s1_decide.py` | learned; C-ORD; SHARP/TARGET; flags; precision; placebos; ordered rules; qualifiers; licence fill; report | ≤ 400 (≈ 380) |
| `x6s1_run.py` | S0 (allowlist, repair ancestry and blob hashes, stage-0 binding, seed freshness, owner authorisation, notebook hash); PF record; stage drivers and CLI; sealing; lineage (reusing the `x6_store` generics); local evaluation waves with the **repaired** supervisor; RUNTIME-ACCT | ≤ 400 (≈ 380) |
| `x6s1_registry.py` (**pre-allowlisted overflow 1; now planned in use**) | REG1/REG2, sources, separation, diagnostics, the extended inventory scan (§6.4 (d)) and the **bounded-memory K-REG2 identity reader** (§6.4 (c); RC10), with streamed sorted runs. If it cannot fit in 400 lines, S7 applies before implementation expands the footprint (K4b's registry took ≈ 510 lines in 2 files) | ≤ 400 |
| `x6s1_stats.py` (**pre-allowlisted overflow 2**) | Empirical-Bernstein bound and its outward evaluation, certified log tables, the `np.quantile` wrapper, the two-stage bootstrap, TAIL, moved out of `x6s1_decide.py`/`x6s1_eval.py` if they overflow | ≤ 400 |
| `tools/x6_stage1/X6S1_colab.ipynb` | Thin notebook (§5.11): six code cells, ≤ 60 code lines, stripped | — |
| `tests/x6_stage1/test_a_*.py` (≤ 5), `test_b_*.py` (≤ 5), `AUTHORSHIP_A.md`, `AUTHORSHIP_B.md` | Independent tests | ≤ 400 each |
| Store-local `x6-stage1-store/x6s1_meter_bind.py` | Rebinds module names only (meter paths, `CAP_S = STOP_NEW_S = inf`, `OUTPUT_CAP` 16 GiB, `winjob.MEMORY_CAP` 12 GiB); reads `JOB_ID`, `TASK_SHA256` and `WORKER_SESSION` at launch from the dispatch record; fail-closed sha256 and import-directory check (ruling X5′ pattern) | outside the repository |

Planned: 7 modules ≈ 2,500 lines, realistically **2,600–3,200 lines** with whichever overflow module is used (MD 13; AN D13 precedents: D-2a 1,958 lines in 5 modules, x6_stage0 1,815 in 5, K4b ≈ 3,700 in 14). Ceiling 9 × 400 = 3,600. A tenth module, or any module over 400 lines, is S7. Tests ≈ 2,000–3,000 lines [H].

### 14.2 Six-field reuse assessment

| Field | Assessment |
|---|---|
| **1. Reused unchanged** | **x6_stage0:** `model`, `edge_labels`, `NEIGHBOURS`, `tok`, `vertex`, `seam_letter`, `parse`, `closed_form`, `cue_normalised`, `point_law`, `lam`, `holonomy`, `parikh`, `statistic`; `segment_dp`, `classes`, `weights`, `avoid_counts`, `to_decimal`, `kl_decimal`, `enclosure`; `fraction_filter`, `LOOPS`, `ORDERINGS`, `witness_path`, `witness_tokens`, `prefix_tokens`, `family_values`, `rs_key`, `beta`, `competitor_holonomy`, `challenge_values`, `set_gap`; `x6_run.sample`; the `x6_store` generics. **src:** `HMMSampler`, `SequenceLayout`, `ObservationSet`, `PublicTokenDataset`, `make_sequence_ids`, `process_code`, `check_disjoint`, `SeedTree`, `ArtifactStore`, `Checkpoint`, `BayesFilter`, `ModelConfig`, `TrainConfig`, `TransformerLM`, `WarmupCosine`, `lm_loss`, `learner.trainer._materialise`, `Trainer` (TRAIN-EQUIV reference; `test_trainer_golden`), `load_model`. **Oracle profile:** `suffix_posterior`. **D-2a:** `Limits`, `Supervisor`, `admit`, `boundary`, `disk_reason`, `jsonable`, `write_json`, `verify_identity`, `bind_meter`, `bound_controls`, `_set_threads`, and the **repaired** process-tree accounting once committed. **K4b:** `k4b_registry.inventory` (one component of the extended scan), `validate_handoff_json`; `k4b_registry.load` only as the equivalence reference of author B's synthetic-fixture test (K-REG2 itself is ingested by the bounded-memory reader, RC10); `k4b_registry_k.source_k`; `c1_registry_sources.handoff_sources`. **Meter:** job-0014 meter, controls, winjob through the store-local binding |
| **2. Genuinely missing** | The exact uniform Parikh-class partner sampler; the pair statistic and its bootstrap; designed set D with natural prefixes and commuting controls; the quantised readout and certified scoring; the empirical-Bernstein bound; the float64 predictor interface; the X6-scoped registry wrapper; **the chunked, resumable Trainer-equivalent cloud trainer, the bundle, the chain, the manifest, the ingest gates and the notebook**; an X6 evaluation wave loop (D-2a's `wave_main` and `_launch` hard-code D-2a runs, AN §4 X item 8); the stage-1 rules and report; the `np.quantile` wrapper (L-E1) |
| **3. Smallest change** | One new tools directory and one new test directory; production learner, oracle, dataset and contracts unchanged (`test_trainer_golden` runs in PF) |
| **4. Stable interfaces and invariants** | The learner sees only `PublicTokenDataset` of a registered train pool; latent states never stored; position p = t predicts w_{t+1}; 16-versus-48 indexing via `x6_model`; partners share prefix, cue and R_Parikh key; test sealed until E3 and never uploaded; exclusive-create records locally and atomic writes in Drive; fixed threads; canonical weights digest |
| **5. Regression checks** | The PF list (§8 gate 2); `check_file_sizes`; `check_imports`; NB-STATIC; TRAIN-EQUIV |
| **6. Next plausible extension (not built)** | A causal interchange protocol on these checkpoints if order use is found; X6-II (in-context flux inference). Promote the partner sampler or the chunked trainer into `src/` only with a second consumer |

### 14.3 Test-author split (independent; D-1/X2a/K4b pattern; binding)
**Rules:** authors write from the frozen protocol and `API.md` only, after the freeze and before any module exists; they may read the reused production and reference code and the committed D-2a repair; they never read, list or search `tools/x6_stage1/*.py` or the notebook's implementation module, and execute nothing (the worker runs the tests in PF); corrections only by the file's author; **no formatter is ever run over `tests/x6_stage1`** (the implementer formats module files by name only). `AUTHORSHIP_A.md` and `AUTHORSHIP_B.md` record what was read, not read and executed.

**Author A (science and numerics):**
- *T-PAIR:* exhaustive n ≤ 6 uniformity with an independent enumerator; key and probability equality; validity.
- *T-BETA:* num/den against hand values and `beta`; Lemma P1 exact zero; Lemma P2 zero in expectation on a synthetic segment-only predictor (exact expectation over y), and a counterexample predictor that uses a prefix cue (non-zero), documenting the L-E5 scope.
- *T-DESIGN:* W2 and C1–C4 matched statistics; control oracle spread 0; prefix invariance; the β table; per-cue β for last/first heuristics (½, −1, ½).
- *T-EVAL:* position index (logits[:, t] predicts w_{t+1}); padding independence; float64 determinism; KL with zeros in q*; cue mass.
- *T-QUANT:* conservation Σk = Q; zero rule; ties by lower index; 0 ≤ R ≤ 18; positivity ε/18; the readout floor on hand laws; QUANT_INVALID.
- *T-LOGTAB:* table entries against an independent Decimal evaluation; enclosure consistency; correctly rounded floats; the e_row check.
- *T-EB:* U against an independent Decimal implementation of §7.3; monotonicity in X̄ and Z̄; **exact coverage** P(μ ≤ U) ≥ 1 − δ for two-point laws X ∈ {0, B} (n = 2m, m ∈ {2, 4, 8, 16}, p on a grid, δ ∈ {0.1, 0.00625}) by exact trinomial enumeration over (mixed pairs, both-B pairs); the outward inputs X̄⁺, Z̄⁺; U_report = U⁺ with no separation term (RC1).
- *T-STAT:* the two-stage bootstrap equals the full-row multinomial bootstrap in distribution (exact on n ≤ 6); common indices across predictors; max over controls inside each draw; the `np.quantile` levels; TAIL D1/D2; the gate's PASS/FAIL/UNRESOLVED.
- *T-RULES:* every §7.9 branch (incl. 6′ and the RC12 rule 8 requiring all four ordD flags resolved), missing-model convention, UNRESOLVED routing (cue mass, zero/non-finite cue normaliser, non-finite alignment, ρ_spur, placebos), precedence, qualifiers, the SHARP/TARGET/GAIN_BELOW statuses, PASS/FAIL/UNRESOLVED counts in every designed summary, and the exact-rational thresholds (3/4)·G0⁻ and (3/4)Δ_W2^lo.

**Author B (operations and cloud):**
- *T-SEED:* fresh masters; disjoint streams; the scope map.
- *T-POOL:* sizes; splits; ids; no states stored.
- *T-REG:* a collision gives FAIL_TECHNICAL/LINEAGE; regenerated stage-0 count mismatch; malformed handoff JSON gives INCOMPLETE; an unclassified X6 directory gives INCOMPLETE; an X6 `.npy` or ObservationSet root under a named X6 scratch root that is neither registered nor a hash-identical registered copy gives INCOMPLETE; no sealed-D-2a predicate; **the bounded-memory K-REG2 reader equals `k4b_registry.load` exactly on small synthetic fixtures** (dtype, shape, ordering, counts, canonical union hashes) and refuses a hash mismatch (RC10).
- *T-TRAIN-EQUIV:* chunked trainer = `Trainer.fit` bitwise on CPU with two fresh-process forced resumes, under the full §4.6 PASS condition (model state, every optimiser tensor and scalar, complete scheduler state and current learning rates, PCG64 state, initialisation, all batch-index arrays; restored train mode, configuration and step numbering), with the reference generator exposed through a test-only delegating SeedTree wrapper (RC11); identical init and batch order across arms for one seed.
- *T-CHAIN:* single-serialisation checkpoint write (one byte buffer hashed, written to `.part`, fsync, re-read, publish; refusal of an existing target); records published only after their checkpoint verifies; quarantine only of nonterminal artifacts, each with a re-hashed preservation copy and recorded original path; read failures and incomplete listings → HOLD and stable re-read; refusal of a duplicate step; a broken inner link → CHAIN BROKEN; **a terminal NONFINITE marker survives interruption and quarantine and blocks further updates and retraining; an unreadable marker stops recovery** (RC6); resume restores model, optimiser, scheduler and PCG64 state and checks checkpoint-internal step, scheduler phase, optimiser structure and PCG64 state against the record; the batch-ID pre-check refuses a wrong stream; chains parameterised by ticket `steps` and K (C0: 200, 100).
- *T-INGEST:* every §5.8 failure row gives its status (one-byte corruption; wrong relayed manifest hash; an inventory with a missing or extra file, honouring the explicit exclusions; missing field; wrong code commit; an execution record with an edited cell source or unexplained extra code; a session without a cell-6 record accepted; wrong init; wrong batch digest; gap; terminal marker; HOLD prefix); the admission lock is written before any evaluation and blocks a later retrain; byte-identical re-download after evaluation is accepted and different weights are refused (RC9); re-finalisation produces a new snapshot and preserves the earlier one (RC7).
- *T-BUNDLE:* only allowed classes; refusal of val/test/gate/prefix/dev/sealed/registry files; BUNDLE_SHA256.
- *T-NB:* notebook static checks (§5.11); the inline bootstrap refuses a modified bundle.
- *T-ENV:* session-record fields and the executed-cell hash normalisation.
- *T-RESOURCE:* process-tree CPU and memory read the interpreter, not the venv launcher; a kill reaches the interpreter; S6 limits; disk floors; STOP/HOLD propagation; no real mailbox writes.
- *T-S0:* the allowlist; repair ancestry and blob hashes; stage-0 hash binding; owner-authorisation record; notebook hash.
- *T-LINEAGE:* supersede and manifest; bit-identical regeneration; volatile fields; the cloud retrain route's precondition (refused after admission or any local evaluation); one immutable bundle directory per bundle id.
- *T-ENV-LOCAL:* the local evaluation environment record of §2.2 (OS 3) is complete in every evaluating stage record.
- *T-METER:* binding sha256 and import-directory refusal; OUTPUT_CAP and MEMORY_CAP values.
- *T-SIZE:* the module set (7 + the two allowlisted), the 400-line limit, the notebook limits.

### 14.4 Execution worktree
A new worktree `X:/Downloads/projects/topo-pilot/topo-pilot-x6s1` on branch `x6s1-<job>` from R; PF and every local stage run there at H with an empty `git status --porcelain --untracked-files=all` recorded; `PYTHONPATH=<worktree>/src` and the venv interpreter with `-s` (the editable install would otherwise import main's `src`, C1′ R9); the meter imported from `<worktree>/tools/x4_oracle_profile`. The main worktree's uncommitted edits can never reach X6. `code.tar` is `git archive` of H, so Colab runs exactly H.

### 14.5 Commit binding (D2A D5 rule)
- **R:** the main commit, recorded at the freeze, that contains the accepted D-2a repair commit P (§15 D1). This draft was reviewed against 727af56; the freeze round re-checks the 727af56→R diff over the protected paths (S0§8.1 review-base pattern).
- **Protected paths:** `src`, `pyproject.toml`, `tools/{x4_oracle_profile, x6_stage0, d2a, k4b, c1prime, c1prime_registry, x4_circle_history}`, `tools/check_file_sizes.py`, `tools/check_imports.py`, `tools/x6_stage1`, `tests/{learner, dataset, contracts, oracle, oracle_profile, world, process, x6_stage0, d2a, k4b, c1prime_registry, x6_stage1}`.
- **Allowlist:** `A` entries for the §14.1 repository files only (the two overflow modules included).
- **Mechanical check:** `git diff --no-renames --name-status R H -- <protected>` lists only allowlisted `A` entries.

---

## 15. Dependencies and prerequisites (must hold before freeze or dispatch)

| # | Dependency | Needed by | Check |
|---|---|---|---|
| **D1** | **The D-2a launcher/accounting repair** (jobs/0033 §7.1; owner addendum 12 item 4; `tools/d2a/process_tree.py` and its tests), **committed** to main as its own commit, accepted by coordinator review, and **frozen**. X6S1 binds its committed API in `API.md` and its files by blob sha256 in FREEZE.json; its uncommitted text is not used. It still matters: local evaluation waves (E3.A) and RUNTIME-ACCT run under the repaired supervisor | Freeze (API binding); S0 item iv; PF RUNTIME-ACCT | P and blob hashes in FREEZE.json; RUNTIME-ACCT PASS |
| D2 | **Owner authorisation** naming the frozen protocol hash, the local budget (central ≈ 43 CPU-h, range 23–70), the cloud use (≈ 1–4 GPU-h, Drive ≈ 4.3 GB), the smoke/preflight work, the transfers and the owner sessions, with the owner's confirmation of account access and free-tier use (X6-FROZEN-v1 §8.4; addenda 12–14, 16; RU O-3/O-16). **AUTH is an admission prerequisite**, before E0 execution, CLOUD-SMOKE, scientific training, and the training portions of TRAIN-EQUIV/RUNTIME-ACCT; planning, implementation and static review may precede it (RC5) | E0 and every later execution (AUTH-ADMIT, S10) | Addendum in the store (`AUTH.json`) |
| D3 | The planning protocol: this writer round, a Codex result-blind review verifying §7.3–§7.4, confirmation, freeze | Everything | Freeze record |
| D4 | Stage-0 artifacts unchanged: `report.json` e7846911…, `GATES.jsonl` c871f5e4…, `model.npz` e1b9a753… | S0 (v); REG1 (a) | sha256 |
| D5 | K4b registry artifacts unchanged (K-REG2 manifest and digest file; k4b-store stage tables) | REG1 (c) | `k4b_registry.load` re-hash |
| D6 | A clean worktree at H, the venv, the `PYTHONPATH` setting | PF | §14.4 |
| D7 | Disk: C: ≥ 2 GB, X: ≥ 30 GB before each job; ≥ 60 GB at E0 | All jobs | `disk_reason` |
| D8 | One scientific job at a time; no other X6-process generation during the reservation window | E0 | Coordinator attestation |
| D9 | No conflict with another session's uncommitted edits in main | Implementation | Isolated worktree |
| D10 | Owner access to Colab and Drive (≥ 6 GB free) | C0–C2 | CLOUD-SMOKE |
| D11 | Colab's preinstalled torch can load and save the bundle formats and run `x6s1_cloud.py` (Python ≥ 3.10) | C0 | CLOUD-SMOKE |
| D12 | Owner addendum 14's writer hold released (O-0) | This document | **Resolved:** owner addendum 16 (sha256 `C87DCFCB…779B`) |

---

## 16. Risks

| # | Risk | Handling |
|---|---|---|
| R1 | NOT_LEARNED again (D-2a precedent; a weak, sparse order signal; S₃ composition over ≤ 31 steps) | Pre-registered non-order gate; scoped NOT_LEARNED; ZC-s1 descriptive; 3× D-2a's updates; no rescue |
| R2 | Gate too strict (G_8 needs beyond-window transport) | Disclosed; gated identically across arms; exact pass wording |
| R3 | Learned transport, order alignment below threshold | ORDER_NOT_DETECTED is legitimate; ladder and length profiles descriptive |
| R4 | Bag or heuristic mechanism misread as composition | Natural licence limits; W2 regret and per-cue β; heuristic reference β |
| R5 | Spurious within-class sensitivity | ρ_spur (both kinds), placebos, natural spurious ratio |
| R6 | Readout fragility of cue-normalised laws | Cue-mass check; W2 full-vocabulary regret; raw β reported |
| R7 | Supervisor defect recurs (venv launcher) in local evaluation | D1 plus RUNTIME-ACCT with a kill test |
| R8 | **Colab unavailability** (no GPU, usage limits) | Chunked resume; no deadline inside 14 days; S12 owner options |
| R9 | **Disconnect mid-write; Drive FUSE lag** | Atomic `.part`/fsync/re-read/rename; records written after checkpoints; quarantine; full chain re-validation at each resume |
| R10 | **numpy or torch version drift on Colab** | Uploaded data and init; batch-ID pre-check before GPU work; DATA-ID; canonical weights digest independent of pickling |
| R11 | **Owner error** (wrong bundle, edited cell, deleted files) | Pasted BUNDLE_SHA256; executed-cell hashes; never-delete rule; S13 |
| R12 | **NONFINITE on GPU** (possibly hardware-related) | No retry (precedent); the model counts as failing; disclosed |
| R13 | Bitwise TRAIN-EQUIV fails on CPU (e.g. optimiser state restoration order) | Found in PF before any data; technical correction |
| R14 | Evaluation cost overrun (float64 rate) | Chunked E3.A; measure-only; forecast range shown; O-4 option |
| R15 | Footprint overrun | Two pre-allowlisted overflow modules; thin notebook |
| R16 | Test leakage via the cloud | The cloud receives only train/smoke pools, init, code and ticket (T-BUNDLE, S9) |
| R17 | Overclaiming (mechanism, topology, causal use, PoE, reproducible training) | §3 never-licensed list |

---

## 17. Open items: resolutions (RU, 2026-10-18)

All v1 open items are closed by the coordinator's rulings (`coord-x6s1-review-20261018.rulings.md`); the only remaining owner action is the authorisation (O-3), which must precede any execution.

| # | Item | Resolution | Where |
|---|---|---|---|
| O-0 | Writer hold (addendum 14) | **Resolved by owner addendum 16** (hold released for writing the exact protocol and everything the cloud run needs; training still unauthorised) | Header; §15 D12 |
| O-1 | L's runaway guard and alarm | CPU stays measure-only. **The 90 CPU-h notification alarm is adopted as notification only**; it never stops anything. No 8 CPU-h child stop and no 20 CPU-h guard | §13.4 |
| O-2 | Memory | 3 GiB per process and 12 GiB per job; bounded-memory registry ingestion; the blanket 1.9× margin claim is withdrawn | §6.4, §13.4 |
| O-3, O-16 | Owner authorisation | Before execution it covers the frozen hash, the local and cloud forecast, the smoke and preflight work, the transfers and the owner sessions, plus confirmation of account access and free-tier use | §8 AUTH, S10, §15 D2 |
| O-4 | Abelian own-arm test size | **2²¹ retained** per owner addendum 13; a 2¹⁹ reduction would need an owner amendment | §6.1, §13.1 |
| O-5 | Chunked trainer | Adopted, with the completed TRAIN-EQUIV (RC11) | §4.3, §4.6 |
| O-6 | Data handling | Upload of the locally generated training data adopted | §5.2 |
| O-7 | GPU mixing | Permitted and recorded (MIXED_DEVICE) | §5.4 |
| O-8 | Colab unavailable | Default: wait; CPU fallback is an owner decision (with its own amendment) | S12 |
| O-9 | D-2a repair | **Prerequisite:** P committed, accepted and frozen, and bound by exact blob | §15 D1, §8 S0 (iv) |
| O-10 | Bernstein proof | Theorem and constants verified by the review; application corrected (RC1) | §7.1, §7.3–§7.4 |
| O-11 | Energy fraction | Dropped (undefined) | §2.8 |
| O-12 | Natural placebo routing | INCONCLUSIVE + CONTROL_LIMITED for an otherwise supported natural claim with failed placebos | §7.9 rule 6′ |
| O-13 | Bundle hash anchor | The pasted BUNDLE_SHA256 is tied to an immutable per-bundle directory | §5.3, §5.10 |
| O-14 | Colab versions | Record every version; a version change is detected before continuation; no unreviewed auto-install | §5.4, §5.6 |
| O-15 | Length profile | Stays descriptive | §2.8 |

---

## 18. Corrections applied and writer's decisions

**Analysis corrections (MD 18):**

| Id | Correction | Where |
|---|---|---|
| X-E1 | Lexicographic fresh prefixes dropped; L's natural prefixes from a registered stream | §2.5, §6.3 |
| X-E2 | Evaluation chunked per predictor, resumable, hashed outputs; 12 h jobs | §13.3, §12 item 6 |
| X-E3 | X's regret + γ gate replaced by L's G_8 gate; γ sealed descriptive | §4.7, §2.8 |
| X-E4 | Energy-fraction claim dropped; not computed | §2.8, O-11 |
| X-E5 | Stage-0 histories regenerated identity-only with count checks | §6.4 (a) |
| X-E6 | NOT_LEARNED wording fits the G_8 gate | §3 row 2 |
| L-E1 | `np.quantile` wrapper with registered levels, listed as new code | §7.5, §14.2 |
| L-E2 | 3 GiB per process kept; registry fitted by bounded-memory ingestion (v2, RC10; no blanket margin claim) | §13.4 |
| L-E3 | Placebo failure → CONTROL_LIMITED / INCONCLUSIVE, never PIPELINE_INVALID | §2.7, §7.9 |
| L-E4 | Footprint 2,600–3,200 lines with two pre-allowlisted overflow modules | §14.1 |
| L-E5 | Lemma P2 reworded: marginal independence; scope excludes predictors using prefix cue tokens | §2.3 |
| L-E6 | Gate pass wording exact; SHARP power restated for EB at 2²¹ | §4.7, §7.7 |

**Writer's decisions (W; for review, none changes an MD):**
- W1. The registered predictor is split by statistic type: raw float64 softmax for alignment statistics, quantised readout for log-loss statistics (MD 6 names the readout for log-loss statistics only).
- W2. TARGET uses SHARP's bound, so no separate α share; GAIN_BELOW_TARGET claims non-certification only (no lower bound).
- W3. The empirical-Bernstein variance step is a paired U-statistic bound derived from Lemmas B1–B2, not Maurer–Pontil's Theorem 10, so the whole proof is self-contained (§7.3).
- W4. (v2, RC1) Coverage is asserted unconditionally over the original iid test draw; separation failures only suppress claims; the threshold stays G0⁻ (MD 8) and ρ̄ is a descriptive diagnostic. v1's ρ̄B correction is withdrawn.
- W5. LEARN-TEST and the ladder use the EB bound at δ = 0.025 (distribution-free; outside the family); the gate keeps L's bootstrap (EB at 2¹⁵ rows would be ≈ ½·G_8 wide [W]).
- W6. The pilot gate's γ is computed only at E3 (no model-dependent order statistic before E3, S9), which satisfies "sealed descriptive" (MD 3).
- W7. Dev pools stay local; the learning-curve record is local float64 and sealed until E3 or a stop.
- W8. Informative-pair feasibility floor scaled to N = 2²¹ (≥ 24,000, about half the forecast, as L's 1,500 at 2¹⁷).
- W9. The cloud retrain route is limited to models never admitted and never locally evaluated (v2, RC9 admission lock), so GPU non-determinism can never select an outcome.

---

## 19. v1→v2 changes (Codex review coord-x6s1-review-20261018, VERDICT APPROVE_WITH_REQUIRED_CHANGES; rulings: every RC adopted as written, O-0…O-16 resolved, all four OS adopted)

### 19.1 Required changes (reviewer's exact texts at the stated locations)

| RC | Change | Location in v2 |
|---|---|---|
| 1 | Independence and conditioning: "Sampling and separation" paragraph; §7.3 "under the original natural law P"; §7.4 item 6 "Reported bound. U_report = U⁺"; P′ claims removed | §7.1; §7.3 setting; §7.4 item 6; conformed: §6.6 item 4, T-EB, §18 W4, App. A collision line |
| 2 | Population estimand inserted before the sample statistic; §7.2 heading and first bullet; "nominal one-sided 97.5% bootstrap lower bound" in the licensed sentence | §2.3; §7.2; §3 outcome 5; notation (Δp_{m,c}) |
| 3 | Full stage-0 constants: §2.1 paragraph replaced; Δ_W2^lo, Δ_W3^lo defined with central values; ordD regret PASS/FAIL, W2_GAP_BEATEN, CHALLENGE_BEATEN replaced; TARGET as (3/4)G0⁻ | §2.1 (table and paragraph); §2.4; §2.5; §7.2; §7.4 item 7; §8 S0 (v) and G0-ORC (g); §10.1; T24; §10.3; App. A |
| 4 | Pool-construction order (controlling schedule); §12 item 11 "Test access"; S9 model-dependent clause | §8 (paragraph before the table); §12 item 11; S9; conformed: §5.12, §6.1 test row, §8 E3 note |
| 5 | AUTH as an admission prerequisite | §8 (paragraph and rows 0b AUTH-ADMIT, 10 AUTH-VERIFY); S10; §15 D2; header next step |
| 6 | Terminal NONFINITE markers first; conservative quarantine; single-serialisation checkpoint write; tests | §5.4 steps 0, 3, 4, 8; §5.5 terminal marker; §5.8 TRAIN-COMPLETE row; T-CHAIN, T-INGEST |
| 7 | Output inventory without circularity; executed-cell start/finalisation records; ticket and record schemas | §5.6 (inventory, execution records, manifest path); §5.3 (ticket contents); §5.5 (step-0 values, `pcg64_state`, internal consistency); §5.8 WEIGHTS-HASH (b), CLOUD-PROV, DATA-ID; §5.4 steps 2, 4, 10 |
| 8 | Immutable per-bundle namespace; cell-6 retry; variable idle/lifetime statement | §5.3; §5.10 steps 2, 3, 7, cell 2 and cell 6 rows, disconnect paragraph, "Never" list; §5.7 transfer; §5.4 step 9 (verified recovery, not fsync durability) |
| 9 | Admission lock before any evaluation; retrain eligibility; restoration versus replacement | §5.7; §12 items 9–10; §5.8 closing paragraph; S11; §8 rows 14, 18, 20; T-INGEST, T-LINEAGE |
| 10 | Bounded-memory K-REG2 reader; extended inventory; memory statement; XCHECK Fraction note | §6.4 (c), (d) and digest paragraph; §6.6 item 5; §13.4 memory; §14.1 `x6s1_registry.py`; §14.2 field 1; T-REG; §8 row 26 |
| 11 | TRAIN-EQUIV acceptance condition | §4.6 item 3; T9; T-TRAIN-EQUIV |
| 12 | Rule 8 requires all four ordD flags resolved; §2.6 non-finite/zero normaliser rule | §7.9 rule 8; §2.6; T-RULES |
| 13 | C-ORD power statement | §7.7 first paragraph; §10.3 C-ORD row |
| 14 | Narrowed licence language | Summary question; §1.1; §3 outcome 6 (and outcome 7 counts) |

### 19.2 Open items (RU)
All closed as in §17: O-0 (addendum 16), O-1 (90 CPU-h notification alarm only; §13.4), O-2 (§6.4, §13.4), O-3/O-16 (§8 AUTH, §15 D2), O-4 (2²¹ retained; §6.1, §13.1), O-5 (§4.3, §4.6), O-6 (§5.2), O-7 (§5.4), O-8 (S12), O-9 (§15 D1), O-10 (verified; §7.1 corrected), O-11 (§2.8), O-12 (§7.9 rule 6′), O-13 (§5.3, §5.10), O-14 (§5.4 software versions, §5.6, MIXED_ENV qualifier), O-15 (§2.8).

### 19.3 Optional suggestions (all adopted)

| OS | Change | Location |
|---|---|---|
| 1 | D1 labelled a bounded-influence sanity check, with its deterministic margin; D2's limits stated | §7.5; T27 |
| 2 | PASS/FAIL/UNRESOLVED counts in every designed summary | §2.5; §3 outcomes 5–7; T-RULES |
| 3 | Explicit local evaluation environment record (Python, numpy, torch, BLAS, CPU, threads, batching) | §2.2; §8 row 20; T-ENV-LOCAL |
| 4 | Scientific thresholds preserved | §10.1 (row "Unchanged in v2") |

### 19.4 Writer's conforming edits from the review's findings (not RCs; no scientific change)
- Lemma B2: the V = 0 case handled explicitly; the theorem's b distinguished from Lemma B1's b; widths labelled scenario forecasts with the zero-variance width 1.163e-4 [W] (§7.3 remarks).
- Partner sampler: layer zero singleton, zero weight for absent/negative states, and the natural marginal stated **on the registered eligibility domain** (§2.3).
- Log tables: the enclosure rests on analytic rounding bounds; the 80/120-digit agreement is a diagnostic; "nearest float64" replaces "correctly rounded" (§7.4 item 2; T14).
- LOSS-ECHO, CLOUD-PROV and TRAIN-COMPLETE described as consistency/audit checks, not proofs of the trajectory (§5.7).
- MIXED_ENV provenance qualifier introduced for O-14 (§3, §7.9, §11).
- New arithmetic is marked [W] (§2.1, §10.1, §13.4, App. A).

### 19.5 Typographic deviation from the reviewer's texts
The reviewer's texts are inserted verbatim except that LaTeX markup is rendered in this document's Unicode notation (for example \(\Delta_{W2}^{\mathrm{lo}}\) → Δ_W2^lo, \(G0^-\) → G0⁻, display equations as indented lines); the wording is unchanged. Where a replacement text gives a rule without concrete paths, a parenthetical after it supplies the paths and names (marker file, bundle id, record file names) without altering the reviewer's sentences.

---

## Appendix A. Hand arithmetic [W] (awk in W's scratchpad; not gates)

- **Readout:** ln(18/ε) = 16.705882 < 17; oracle-readout floor −ln(1 − 1e-6) + 18/(2⁴⁰(1/750 − 2⁻²⁰)) = 1.000000e-6 + 1.229e-8 = 1.012287e-6.
- **EB constants (N = 2²¹, m = 2²⁰, B = 17):** δ = 0.00625: ln 320 = 5.768321, a = 3.987252e-2, b = 1.324848e-4, BL/(3n) = 1.558645e-5, √(2L/n) = 2.345442e-3. δ = 0.025: ln 80 = 4.382027, a = 3.475253e-2, b = 1.006449e-4, BL/(3n) = 1.184057e-5, √(2L/n) = 2.044267e-3. Widths W(σ) at δ = 0.00625: σ = 0.016 → 1.2810e-4; 0.025 → 1.4205e-4; 0.0282 → 1.4773e-4; 0.0358 → 1.6217e-4; 0.040 → 1.7059e-4; 0.060 → 2.1307e-4. At δ = 0.025: 0.9982e-4, 1.1289e-4, 1.1811e-4, 1.3126e-4, 1.3884e-4, 1.7669e-4.
- **Thresholds (v2, exact products of the full central values; the run uses the certified lo endpoints):** (3/4)·G0⁻ = (3/4) × 0.0026358964806790516544… = 0.0019769223605092887408…; (3/4)·Δ_W2 = (3/4) × 0.0611193713418965479555… = 0.0458395285064224109666…; 0.25·G_Parikh = 6.5897e-4. (v1's 0.0458392 used the rounded 0.061119 and was 3.3e-7 too low; corrected by RC3.)
- **v2 additions:** zero-variance EB width at δ = 0.00625: σ_up = (a + √(a² + 4b))/2 = 0.042957, width 1.163e-4; 2λ_32² = 0.548906; D1 deterministic margin 0.01 × 24,000 × 0.549 ≈ 132 against |num_i| ≤ 2; registry identities 19,668,992 + 6,024,521 (K-REG2) = 25,693,513, uint64 keys ≈ 206 MB, full digests ≈ 822 MB, runs of 2²² identities ≈ 134 MB.
- **Pairs at 2²¹:** R_ord rows 199,664; informative pairs 47,809 (SD 219). First 2¹⁷ rows: R_ord(24) 9,672; R_ord(16) 5,681.
- **Stage-0 per-row SDs** (se × 512 at 2¹⁸): q_Parikh 0.0159; q_8 0.0282; q_∅ 0.0358.
- **Forwards:** 5.5182e7 FLOP each; 3.2550e7 forwards; 1.796e15 FLOP; 62.4 / 38.4 / 20.0 CPU-h at 8 / 13 / 25 GFLOP per CPU-s; abelian own-arm share 0.515; 2¹⁹ option saves 14.8 CPU-h; per-model own-arm pass 2.47 CPU-h.
- **GPU:** 2.033e10 FLOP per update; 6.1e14 per model; 8/12/20/40 ms per update → 4/6/10/20 min per model, 0.8/1.2/2.0/4.0 h for 12.
- **Sizes:** checkpoint 9.63 MB (weights 3.21 MB); chain 298.5 MB per model, 3.58 GB for 12; train pool tokens 34.6 MB; C1 ≈ 104 MB, C2 ≈ 311 MB of tokens; local pools 19,128,320 rows, 631 MB tokens, 153 MB ids; stage-0 regeneration 540,672 rows; registry 19,668,992 X6 rows, 629 MB digests; E3 per-row outputs 201 MB per model, 2.42 GB total.
- **Collisions and exclusion:** max P(h) = (1/16)·5⁻³¹ = 1.3422e-23; ρ̄ ≤ 1.342e-15 for 10⁸ registered rows (v2: a descriptive lineage diagnostic only, RC1); expected collisions ≤ 2.7e-9 (X6 pairs) and ≤ 2.7e-8 (X6 × 10⁸ foreign).
- **Scoring error:** e_row bound (18 + 3) × 1.11e-16 × 19.6 ≈ 4.6e-14.
- Inherited and re-used (L App. A, AN): 802,304 parameters; P(R_ord) 0.095207; P(Δq* ≠ 0) 0.022797; E‖Δq*‖² 0.0194791; E‖Δq*‖⁴ 0.0177479; G_Parikh on n ≥ 8 2.5987e-3; 2λ_18² = 0.96643; W3 reversed 0.05095; D-2a 0.78394 CPU-s per update; FEAS-POWER 0.019.

## Freeze record (coordinator)
- **Source:** X6S1-MERGED-v2.md (sha256 EFE57F1063354EE88C5B66DF69A24B71D68AE62DEB3CCF825B144B393033AAAC). Only the STATUS line and this record differ.
- **History:**
  - **Planning:** request coord-x6-stage1-20261018; track X (Codex) and track L (Claude), worked independently; a clean-context merge analysis (D1–D16); the coordinator MERGE decisions MD 1–18.
  - **v1** (BBB3387A).
  - **Codex result-blind review:** APPROVE_WITH_REQUIRED_CHANGES, RC1–RC14. **The empirical-Bernstein theorem and constants are verified.**
  - **Rulings:** coord-x6s1-review-20261018.rulings.md.
  - **v2** (EFE57F10).
  - **Codex v2 confirmation:** CONFIRM_FOR_FREEZE.
- **Authority:**
  - OWNER_DECISIONS.v1-a73c869.md;
  - addenda 12 (the track);
  - 13 (30k × 2²⁰; NA, AB and ZC × 4 seeds; empirical Bernstein at 2²¹);
  - 14 (Google free cloud GPU);
  - 16 (writer hold released).
- **Code reference:** main at the time of planning, 727af56. Main has since advanced to 1121df8 with additions only (the c1p-0035 merge and the reorg translations). The implementation job pins H and its S0 diff as the protocol specifies.
- **Prerequisites before any execution:**
  - **(i)** the D-2a launcher repair P, currently uncommitted work by another owner session, committed, accepted, frozen and bound by exact blob (O-9);
  - **(ii)** the implementation (contract, independent tests A and B, modules, notebook) frozen;
  - **(iii)** **the owner's authorisation**, naming this freeze's sha256, the local and cloud budget, the smoke and preflight work, the transfers and the owner's Colab sessions, and confirming account access and free-tier use (O-3, O-16).
- **No training or test sampling is authorised by this freeze.**
