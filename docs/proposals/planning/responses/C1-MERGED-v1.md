STATUS: REVIEW_READY (not frozen)

# C1-MERGED-v1: crossed counterfactual state forcing at the final readout of the E4 cylinder-O models

**Document identity.** `C1-MERGED-v1`. This is the merged protocol for planning request `coord-c1-freeze-readiness-20261014`.

**Authority.** The owner's message `archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md` (sha 13160D21…), part B3 item C, with resources from B4 and limits from B5/B6. The binding coordinator decisions are in `planning/responses/coord-c1-freeze-readiness-20261014.MERGE.md`. The adopted design is `…MERGE_ANALYSIS.md` §6, items 1–22.

**Sources.**
- Track L: `…claude.md`.
- Track X: `…codex.md`.

**Code verified against.** `topo-pilot` main @ 4f219d6, read-only. §18 lists every reused function together with its verified signature and semantics. §21 lists every correction made to the source plans.

**What this document is.** A planning document, not a freeze. It needs the result-blind independent review first (Codex first, per owner part D). After that come a freeze, independent test authors and implementation. No C1 data stage may start before K4's chart outcome is known (§14).

**How to read the rules.** Every number in this document is fixed. Every inequality is meant exactly as written: strict or non-strict, with no added tolerance. Nothing is selected on validation or test data, with one exception: the pre-declared ladder rule (§12.4), which uses validation precision and the oracle-only validation eligible fraction.

---

## 1. Question, competing explanations, and licences

### 1.1 Question
The models are the three original E4 cylinder-O models (seeds 1729, 2718 and 3141, step 5000). The site is `resid_post_3`, input index 32.

The question: at this site, does the final readout of each model functionally use the learned circular (PH-chart) phase for next-symbol prediction, in the direction that an exact counterfactual oracle prescribes? The alternative is that the phase is only decodable there; m32 is already known to be decodable at R² ≈ 0.997.

At index 32 the only computation downstream of the site is `ln_final` followed by `unembed`. So C1 tests use **by the trained readout at the final site**. It says nothing about how earlier blocks compute the phase.

The test is not trivial:
- after the softmax shift is removed, the readout of the 128-dimensional residual into 36 symbols has rank ≤ 35;
- so at least 93 directions are invisible to the readout;
- a perfectly decodable circle could therefore lie entirely in directions the readout ignores.

The study tests **causal efficacy**: setting the variable moves the output in the right direction. It does not test necessity, because nothing is removed.

### 1.2 Competing explanations

| | Explanation | Prediction for A_T | Prediction for the controls | How C1 separates it |
|---|---|---|---|---|
| E1 | Directional use: the readout maps chart-phase changes to predictive changes aligned with the oracle | A_T ≫ 0 | mean A_C ≈ 0 | Endpoint (§12) |
| E0 | Decodable only: the phase lies in directions the readout ignores | A_T ≈ 0 | ≈ 0 | Endpoint, made interpretable by the positive control V3 (§11) |
| E2 | Generic displacement or damage: flattening, LayerNorm scale, off-support distortion, nuisance damage | Arm-common **additive** log-p effects cancel exactly in A. Multiplicative (temperature-like) effects scale A toward 0, which is conservative. Arm-asymmetric residuals are estimated by the matched family | same | Crossed contrast (§12.1), matched family (§6), damage gate M2 (§8), support gate M3 (§9) |
| E3 | Nuisance channel: the move also shifts decoded y-nuisance in the counterfactual direction, and the readout uses that | bounded | — | Leakage gate inside M2 (§8.3) |
| E4 | Short-context channel: within-symbol phase mostly carries w31 information | **not separated** | — | A stated limit, not a gate |

### 1.3 Estimand
For model j, over naturally sampled, oracle-eligible rows (§4):

θ_j = E[Y_j] / E[G]

Y and G are defined in §12 and §3. θ_j = 1 means that the phase-only move reproduces, beyond the matched controls, as much counterfactual discrimination as the oracle itself has.

The estimand is conditional on the frozen chart (§14), the calibration fits (§5, §7) and the 32 frozen frames (§6).

**Specificity statement (MERGE ruling 1; part of every claim).** The comparison measures specificity relative to equal-norm, equal-spectrum displacements in random within-class directions. The random family is a near-placebo:
- by Haar symmetry its expected crossed contrast is ≈ 0 to first order;
- it subtracts only second-order generic effects;
- so "beyond the controls" adds little discrimination beyond "A_T exceeds 0.10·G".

This near-zero expected effect is the null being tested against. It is not a defect.

### 1.4 What each outcome licenses
The decision rule is in §13.

**PASS** (all three models have L_j > 0, where L_j is the lower bound of Z = Y − 0.10·G) licenses exactly this claim. In each of the three E4 cylinder-O models at `resid_post_3`/index 32:
- forcing the learned PH-chart phase toward the phase the model assigns to a ±2-cell x-translated prefix (w32 kept) moves the next-symbol distribution in the oracle's counterfactual direction;
- it does so by more than 10% of the oracle's own discrimination (θ_j > 0.10);
- it does so beyond matched random-frame moves, that is, relative to equal-norm, equal-spectrum displacements in random within-class directions.

So the final readout functionally uses this phase component in an oracle-consistent way, for this counterfactual family, on the prespecified eligible population, conditional on the declared gates.

**FAIL** (all three models have U_j < 0) licenses this: at this site and with this operationalisation, phase-only moves along the fitted map reach less than 10% of the oracle-aligned discrimination beyond the matched controls, in each of the three models. Because V3 passed, the models themselves do discriminate the counterfactual prefixes (θ_full > 0.30). A FAIL is therefore a scoped lack of *practical* support for use of this phase component. It does not show that the circle is epiphenomenal: other sites, harmonics or nonlinear operationalisations remain open.

**MIXED** (any other combination of valid per-model results) licenses only two things:
1. the all-three claim is not supported;
2. the per-model statuses PASS_j / FAIL_j / INC_j are reported as computed, each at one-sided level 0.05/3.

No model is selected as "the" one that uses the phase, and no post-hoc explanation is attached.

**Validity outcomes** (any gate not PASS, FAIL_TECHNICAL, or INCONCLUSIVE/NUMERICAL) license only "assay infeasible as specified", with the exact gate and values preserved.

**No outcome licenses any of the following (union of L and X):**
1. H1 or topological necessity, or any claim about square worlds;
2. that the circle is the only carrier of the information, or that it is necessary;
3. the upstream mechanism (how earlier blocks compute the phase);
4. long memory, or separation from w31 or short-context information (E4 explanation);
5. predictive repair or improvement over the unpatched prediction: p_S does not enter A, and repair R is secondary;
6. complete erasure, absence of causal use, or universal sufficiency;
7. generalisation to other counterfactual families, sites, checkpoints, horizons or natural-language models;
8. a literal internal circular variable;
9. that the matching controls every nuisance: matching is empirical, within the stated tolerances;
10. selective confidence coverage conditional on passing the fresh validity gates. The bootstrap bounds are reported as the prespecified unconditional procedure.
11. any change to frozen verdicts: X4-F stays INCONCLUSIVE/FAMILY_UNMATCHED (causal endpoint NOT_RUN), and E4 G-H FAIL, B2/D-055 NO-GO, K8 FAIL and H5 REJECTED keep their recorded scopes. C1 is a new protocol, not a rescue of X4-F.

If a C1 result appeared to change a published E4 claim, the coordinator stops and waits for the owner (B6).

---

## 2. Models, site, identities, splits, seeds, exposure registry

### 2.1 Fixed objects (no training, no site search)
All IDs come from K4 `tools/x4_circle_history/CONTRACT.json` and are re-verified at gate M0.

| Seed | Checkpoint (step 5000) | EmissionSpec |
|---|---|---|
| 1729 | c3358e3cb9c352fb | 3633ac27dab50cf4 |
| 2718 | 98b0e703a337d513 | 97838b9e13a26f74 |
| 3141 | 036b670743ffbbaf | 8c29c329c197c79e |

- Shared objects: WorldSpec 21feee1d8ee5422e (12×12 cylinder, axis 0 periodic) and TransitionSpec e4dafc7b9785c172 (max-degree lazy walk, p_stay 0.2, uniform π).
- Emission: overlap mode, σ = 1.25, 36 symbols.
- Artifact root (read-only): `X:/Downloads/projects/topo-pilot/topo-pilot/artifacts`.
- The original E4 ObservationSet, HistoryIndex and ActivationSet IDs in the K4 CONTRACT are **exposed assets**. They are used only in the exposure registry, never as C1 data.

**Site.** Model input `[BOS, named w1..w32]` (BOS = 36, length 33). The hook is `resid_post_3`, the output of the last of the 4 blocks, at index 32, which holds w32. `logits[:, 32]` predicts w33.

**Symbol conventions** (K4 CONTRACT `symbols`):
- E_canon = E_named[:, perm];
- named = perm[canonical];
- canonical = argsort(perm)[named];
- the canonical history digest is the sha256 of the canonical w1..w32 as uint8 (`scores.history_digests`);
- canonical symbol j = 6a + b, with x-centre index a, y-centre index b, and centre (0.5 + 2a, 0.5 + 2b) (`process/centers.py`).

### 2.2 Histories and splits (all new)
One canonical history set is sampled per block with `dataset.sampler.HMMSampler(T, E_canon, π, SequenceLayout())`:
- `.sample(4096, rng)`, one call per block;
- named tokens per model are perm[canonical];
- the sampler necessarily returns 33 tokens and the latent states, so column 33 (w33) and the states are **dropped in memory immediately** and never stored or read;
- no EvalSidecar is created or read.

Rows are paired across models by sequence_id (`adapter.cross_model_join`). Canonical digests must be identical across models; any mismatch → FAIL_TECHNICAL.

| Split | Sampled rows | Blocks (4096 each) | Panels | Use |
|---|---|---|---|---|
| Calibration | 8192 | cal b0, b1 | 8 × 1024 | All fitting: s_max, κ_ν, FWL map, Σ_W, decoders, q99, and (chart branch C) the landmarks. Early-stop gates M2/M3. **No logit is read on calibration**, except the identity/zero-patch check of M0. |
| Validation | 4096 | val b0 | 4 × 1024 | All feasibility gates, positive control V3, precision P1. Endpoint means are written to a sealed file. |
| Fresh test | k × 4096, k ∈ {1, …, 5} by the ladder (§12.4) | test b0..b(k−1) of b0..b4 | — | The single endpoint. Sampled only after the coordinator ACCEPTs the validation gate report. |

- **Panel assignment:** panel = 4·block + ⌊rank_in_block / 1024⌋, where the rank is by ascending sequence_id.
- **Population used in each fit:**
  - fits that need only natural rows (s_max, FWL, Σ_W, decoders, q99) use **all** 8192 calibration rows;
  - every gate statistic and the endpoint use **eligible** rows only (§4).
- **Fixed streams:** blocks are fixed 4096-row streams, because `HMMSampler.sample` draws `rng.random(n)` per step, so a sample of size n is not a prefix of one of size 2n. The ladder never changes which rows a block contains, and there is no replenishment.
- **Storage:** C1 histories are stored as C1 history tables, not as ObservationSets (correction C-9). Each table is an immutable NPZ via `stage_records.save_npz` and holds:
  - canonical uint8 [n, 32];
  - sequence_id int64;
  - panel;
  - per-row digests of H, H⁺ and H⁻.

### 2.3 Sequence IDs and seed map
Use `contracts.SeedTree` (PCG64; `generator(name, *scope)` accepts str or int scopes; every issued seed is recorded in `.issued` and saved with each artifact). Bootstrap streams are direct `numpy.random.Generator(numpy.random.PCG64(seed))`.

| Purpose | Stream or seed |
|---|---|
| Histories | `SeedTree(0).generator("data", "c1-sf-v1", split, block, "cylinder", "overlap", "1.25")`, split ∈ {cal, val, test}; cal blocks 0–1, val block 0, test blocks 0–4 (only 0..k−1 sampled) |
| Sequence IDs | `make_sequence_ids(process_code("cylinder", "overlap", "1.25", f"c1-sf-v1/{split}/b{block}"), "test", 4096)`. `SPLIT_CODES` has only train/dev/test; the C1 split is carried by the distinct process code |
| Control frames | `SeedTree(0).generator("c1-sf-v1", "frame", model_seed, r)`, r = 0..31; one call `rng.standard_normal((128, 2))` per frame |
| RFF bandwidth subsample | `SeedTree(0).generator("c1-sf-v1", "rbf_bandwidth", model_seed, target)` |
| RFF map | `SeedTree(0).generator("c1-sf-v1", "rbf", model_seed, target)`, target ∈ {"w32", "ymarg", "m32"} |
| Bootstrap (PCG64) | 520501 val SD; 520502 val centred (same seed for every ladder N); 520503 fresh endpoint; 520504 val V3; 520505 val headroom; 520506 fresh headroom; 520507 fresh V3 |

The seed scope tag `c1-sf-v1` is part of the frozen contract. Any change to a seed or scope requires a new tag and a new review.

### 2.4 Exposure registry (sources and donors)
The registry is a set of canonical 32-symbol digests, built with identity-only access (digests only, no scored diagnostics) from:
- **(R1)** w1..w32 of every row of every ObservationSet in the main artifact store (E4 train/dev/test for all three models), each canonicalised with its own EmissionSpec perm;
- **(R2)** every history stored in the X4, X4-B2, job-0014, K4 (0015/0016) and X4-F stores, plus every constructed donor or counterfactual prefix recorded there;
- **(R3)** every planning-feasibility history recorded under `agent-handoff`;
- **(R4)**, for the fresh stage only, every C1 calibration and validation H, H⁺ and H⁻.

The registry manifest lists every store scanned, with its listing hash. The coordinator certifies completeness in the release. An incomplete registry blocks the release (INCONCLUSIVE/REGISTRY_INCOMPLETE).

Freeze points:
- version 1 (R1–R3) is frozen before S3 sampling;
- version 2 (R1–R4) is frozen before fresh sampling.

Both are bound by sha256 in the release that authorises sampling.

**Requirement.** Every C1 source H **and** donor H⁺ and H⁻, in every split, must be absent from the registry, and C1 splits must be pairwise disjoint on all three kinds of history.

Under correct seeding, a collision between 32-symbol histories has negligible probability. So any collision is a seed or lineage defect (FAIL_TECHNICAL/LINEAGE), not a statistical event. This is why the check is every-row (§16 note).

---

## 3. Donors H±, oracle quantities q±, G, and their checks

### 3.1 Donor transform
For k ∈ {+1, −1}: τ_k(6a + b) = 6·((a + k) mod 6) + b.

H^k = (τ_k(w1), …, τ_k(w31), w32): positions 1–31 are shifted one symbol column (2 cells) and **w32 is kept**.

The donors are a pure deterministic function of the source tokens. They are converted to named tokens per model and their digests are recorded.

### 3.2 Exact symmetry (gate H3)
Let ρ_k(x, y) = ((x + 2k) mod 12, y) act on the 144 states (coordinates from the WorldSpec). The checks:
- T[ρz, ρz′] = T[z, z′];
- E_canon[ρz, τ_k(j)] = E_canon[z, j];
- π is uniform.

Each holds with max absolute deviation ≤ 1e-14. The tolerance allows for `logsumexp` summation order in the emission rows; see correction C-16.

Consequences:
- b_t(τH_{1:t}) = ρ b_t(H_{1:t}) for t ≤ 31;
- p(τ w1..w31) = p(w1..w31);
- because w32 is kept, the **closed form** is b32(H^k) ∝ (ρ_k b31(H) · T) ⊙ E_canon[:, w32]. This is **not** a rotation of b32(H).

The donor posterior is computed directly with `BayesFilter` on H^k and must agree with the closed form to max abs ≤ 1e-12.

### 3.3 Oracle (operational)
`oracle.BayesFilter(T, E_canon, π).run(tokens[R, 32])`. The verified semantics:
- a₁ = π, so it emits first and transitions only between emissions, matching `HMMSampler`;
- `b[:, 31]` = b32;
- `q[:, 32]` = b32·T·E_canon;
- `ce[:, 31]` = −log q_31(w32);
- `log_evidence` = log p(w1..w32);
- zero likelihood raises IMPOSSIBLE_HISTORY.

The oracle is the **operational** one: the normalised likelihood calculation with the stored float weights. As in K4, no claim is made that the PRNG realises ideal independent uniforms.

| Symbol | Definition (canonical order) |
|---|---|
| q⁰_i | b32(H_i)·T·E_canon (secondary use only) |
| q^±_i | b32(H^±_i)·T·E_canon |
| G_i | ½ Σ_v (q⁺_i − q⁻_i)(v)·(log q⁺_i − log q⁻_i)(v) = ½[KL(q⁺‖q⁻) + KL(q⁻‖q⁺)] ≥ 0 |
| ν(b) | y-marginal of b (12-vector) |
| z(b) | nuisance covariates (ȳ, Var y, ‖m32‖), where m32 = Σ_z b(z)·c(z) and c(z) = (cos 2πx/12, sin 2πx/12) from `oracle_profile.circle_features` |

- Exactly one transition and then one emission follow the posterior.
- Every entry is strictly positive (softmax emissions); nothing is floored or clipped.
- No w33 and no sidecar enter any calculation.

**Named order and cross-model identity.**
- q_named[perm[j]] = q_canon[j]. This is cross-checked against direct named-space filtering (`BayesFilter(T, E_named, π)` on named tokens) to max abs ≤ 1e-12.
- G is permutation-invariant. It is computed per model in named order and must agree across the three models to ≤ 1e-12 (X: verify, do not assume).

### 3.4 Decimal reference (gate H3)
**Rows.** The 4 lowest-sequence_id eligible rows per split (cal, val, test), each for H, H⁺ and H⁻.

**Method.** Inside `decimal.localcontext(error_bound.trapping_context(80))`:
- posteriors b31 and b32 from `independent_reference.decimal_suffix_posterior(T, E_canon, π, suffix, digits=60)`, with suffix = w1..w31 and w1..w32 respectively;
- the predictive Σ_z b(z) Σ_z′ T(z, z′) E(z′, v), and Decimal `ln` for surprisals and G. This is a small new helper; the existing reference returns posteriors only.

**Tolerances.**
- posterior max abs ≤ 1e-12;
- predictive max abs ≤ 1e-12;
- surprisal ≤ 1e-10;
- G ≤ 1e-10.

Any trap or mismatch → FAIL_TECHNICAL/ORACLE.

### 3.5 Oracle headroom (gate H5; fresh pre-scoring)
Call `oracle_profile.bootstrap_profile(norm={1: G}, sq={1: G}, Ks=(1,), rng=PCG64(520505), draws=5000)` over the validation eligible rows. The lower bound is `percentile_interval(B[:, 0], [0.05])`, which uses inverted_cdf.

The gate requires lower bound **> 0.01 nat**. Use seed 520506 on the fresh rows. Calibration Ḡ is reported only.

---

## 4. Eligibility (oracle-only, fixed before calibration)

- **Natural surprisal:** s_i = −log q_31(H_i)[w32] = `ce[:, 31]` on H_i.
- **Donor surprisal:** s^±_i = −log q_31(H^±_i)[w32] = `ce[:, 31]` on H^±_i.
- **Threshold:** s_max = `np.quantile(s_cal, 0.999, method="inverted_cdf")` over all 8192 calibration rows. It is computed at S3 and frozen.
- **Rule:** row i is eligible iff s⁺_i ≤ s_max, s⁻_i ≤ s_max, and every one of H, H⁺, H⁻ has positive likelihood (finite `log_evidence`).

Why this measures donor plausibility exactly: under the symmetry, p(τ w1..w31) = p(w1..w31). The only implausible step in H^± is therefore the last one, and the donor's last-symbol surprisal measures its plausibility exactly.

The same rule is applied identically to every split. It uses no model output, chart value, patch or regret. No row is ever removed after the model stage, and model-side support is gated only as fractions (§9).

**Gate H4.** The eligible fraction must be ≥ 0.90 on calibration **and** on validation.

**Leakage trigger.** κ_ν = mean_i ‖ν⁺_i − ν⁻_i‖² / tr Cov_cal(ν).
- Cov_cal(ν) is the population covariance of the natural ν(b32) over all calibration rows.
- The mean is over calibration eligible rows.
- κ_ν is computed at S3 and frozen. It fixes, before any model work, whether the leakage gate (§8.3) is active: active iff κ_ν ≥ 0.01.

---

## 5. Forced state: FWL phase map and covariates

### 5.1 Model evaluation (float64; MERGE ruling 5)
**Building the model.** `learner.stage.load_model(checkpoint)` returns an eval-mode CPU model. Then:
- `model64 = model.to(torch.float64)`;
- every parameter cast back to float32 must equal the original bitwise;
- `torch.set_num_threads(1)`;
- all passes run under `torch.no_grad()`.

**Natural and donor activations.** `model64(inputs, return_hooks=("resid_post_3",)).hooks["resid_post_3"][:, 32, :]` (float64, [R, 128]).

`ActivationExtractor` is **not** used. It returns float32 and needs ObservationSet/HistoryIndex inputs (correction C-2).

On calibration, the logits the forward pass returns are discarded unread.

**Notation, per model and row:**
- a_i: natural activation;
- a^±_i: the model's activation on H^±_i;
- φ^S_i = φ(a_i) and φ^±_i = φ(a^±_i): gauged phases from `chart.extend` (§14);
- f(φ) = (cos φ, sin φ).

### 5.2 FWL regression (calibration, all 8192 natural rows, OLS via `numpy.linalg.lstsq`)
a_i = Σ_w α_w·1[w32(i) = w] + Γ z̃_i + B f(φ^S_i) + ε_i

- The design has 41 columns: 36 symbol indicators (no global intercept), 3 nuisance covariates z̃, and 2 phase columns.
- z̃ = z(b32(H_i)), standardised with the calibration mean and population SD.
- Gate F1 requires all of:
  - full column rank 41;
  - 2-norm condition number of the design ≤ 1e8;
  - σ_min(B)/σ_max(B) ≥ 1e-6.

  Otherwise INCONCLUSIVE/PATCH_MODEL_DEGENERATE.
- **Reported, not gated:** the within-class partial R² of f(φ), and the partial R² against a per-x-column slope model (misspecification diagnostic).

**Why this regression.** By Frisch–Waugh–Lovell, B is identified only from **within-symbol**, nuisance-adjusted covariation of a with the chart phase. That is exactly the variation the w32-preserving donors change. The 6 x-centre columns give distinct tangent directions in R², so B is identified.

Including ‖m32‖ among the covariates keeps the circle radius out of B.

X's alternative is not used. It binned the symbol residual by absolute phase into a 12-bin centroid curve, and that aliases: the gauged centres sit at 15° + 60°·a, inside the bins.

### 5.3 Primary forced states
- Δ^±_i = B[f(φ^±_i) − f(φ^S_i)];
- a^±_{T,i} = a_i + Δ^±_i.

Every other position, every weight and every buffer is unchanged. The move depends nonlinearly on the activation, through the chart. It is state forcing, not erasure.

### 5.4 Patched pass
**Reference path.** `learner.forward_with_patch(model64, inputs, "resid_post_3", 32, a_forced)`, reading `.logits[:, 32]`. Verified semantics:
- it replaces x[:, 32] after block 3;
- it then applies `ln_final` and `unembed`;
- it casts the replacement to x.dtype;
- the model must be in eval mode.

The reference path is used for S, D± and T± on validation and test.

**Tail path, for the control frames only.** `model64.unembed(model64.ln_final(a))`. It is mathematically identical, because no block follows `resid_post_3` and LayerNorm acts per position.

Before the tail path is used, the log-softmax from the tail path must equal that from `forward_with_patch` within max abs 1e-12 for T±, on every validation and test eligible row. This is a numerical identity; failure is FAIL_TECHNICAL.

### 5.5 Within-class covariance and whitening
- **Residual:** r_i = a_i − α̂_{w32(i)} − Γ̂ z̃_i. This keeps the phase term and ε.
- **Covariance:** (r̄, Σ_W) = `x4f_scores.ledoit_wolf(r_cal)`, which returns the mean and the LW-shrunk population covariance.
- **Whitening:** W = Σ_W^{−1/2}, the symmetric inverse square root via `numpy.linalg.eigh`. If λ_min ≤ 1e-12·λ_max: INCONCLUSIVE/SUPPORT_DEGENERATE.

---

## 6. Controls: Haar whitened 2-frames

**Construction (per model).**
- Q̃ = an orthonormal basis of span(W B), from the QR decomposition of the 128×2 matrix W B.
- Primary whitened coordinates: c^±_i = Q̃ᵀ W Δ^±_i ∈ R². This is exact, since W Δ ∈ span(W B).
- For r = 0..31:
  - draw G_r = `rng_r.standard_normal((128, 2))` (§2.3);
  - take the QR decomposition G_r = U_r R_r;
  - set Q_r = U_r·diag(sign(diag R_r)), a Haar 2-frame.
- No draw is rejected, regenerated or selected.
- Control displacement: Δ^±_{r,i} = W^{−1} Q_r c^±_i. Control state: a^±_{C_r,i} = a_i + Δ^±_{r,i}.
- **The same frame Q_r maps both arms of a row.**

**Identities (gate M1, relative error ≤ 1e-10):**
1. Per-row whitened norm: ‖W Δ^±_{r,i}‖ = ‖c^±_i‖ = ‖W Δ^±_i‖.
2. Spectrum: the whitened second-moment matrix Q_r S Q_rᵀ (S = Σ_{i,±} c cᵀ, both uncentred and centred versions) has the same eigenvalues as Q̃ S Q̃ᵀ. So trace and spectrum match exactly.
3. Frame orthonormality: ‖Q_rᵀ Q_r − I‖_max ≤ 1e-12.

Information damage and support are not identities. They are measured and gated on calibration **before any endpoint logit exists** (§8, §9), and again on validation and test.

**Metric.** "Norm" means the within-class Mahalanobis norm. This makes the norm requirement coincide with support, and it is invariant to the anisotropic scale of the residual stream. Matching raw L2 norm in random directions would push controls off-support along low-variance directions, the mirror image of the X4-F mismatch.

The raw-norm ratio mean‖Δ_C‖ / mean‖Δ_T‖ is reported per frame and not gated. Under the crossed contrast it affects variance, not bias.

**Overlap with the primary.** The expected squared overlap of a Haar frame vector with span(W B) is 2/128. X's sign-field family is not used: it has two destinations per row, about half of the fields reproduce the primary, and the family mean is ½·reflection.

**Owner B3-C.** The family is matched in advance in norm and variance (exactly, by construction) and in information damage (gate M2), with a matching gate that stops early on calibration (MERGE ruling 1).

---

## 7. Probes and decoders (fixed in advance)

**Class.** 2048-feature Gaussian random Fourier features followed by affine ridge, one decoder per target. The reused functions and their verified semantics:
- `x4f_scores.standardizer(X)` returns the fit-row mean and population SD; columns with SD ≤ 1e-12 get scale 1;
- `rbf_bandwidth(X_std_cal, rng, 1024)` returns the median pairwise distance among 1024 rows drawn without replacement, or (None, "RBF_DEGENERATE") if ≤ 1e-12;
- `rbf_map(128, 2048, ℓ, rng)` draws Ω ~ N(0,1)/ℓ first, then β ~ U[0, 2π);
- `rbf_features(X_std, Ω, β)` = sqrt(2/2048)·cos(X_std Ω + β).

**Pipeline per model and target.**
1. Standardise activations: (μ_a, s_a) = `standardizer(a_cal)` over all 8192 calibration natural activations. Then ã = (a − μ_a)/s_a.
2. ℓ from `rbf_bandwidth(ã_cal, rng_bw, 1024)`. ℓ = None → INCONCLUSIVE/RBF_DEGENERATE.
3. (Ω, β) = `rbf_map(128, 2048, ℓ, rng_rbf)`. Features F = `rbf_features(ã, Ω, β)`.
4. λ selection: `x4f_probe.nested_ridge(F_cal, Y_cal, panel_cal, F_cal, Y_cal, grid=(1e-3, 1e-2, 1e-1, 1.0, 10.0))`.
   - This is leave-one-panel-out over the 8 calibration panels; ties go to the larger λ.
   - It standardises the features internally and refits on all calibration rows.
   - It returns λ*, fold MSEs and the refit's predictions on its 4th argument. That argument is the calibration features themselves, so no validation row is touched.
5. Frozen predictor (correction C-14):
   - (μ_F, s_F) = `standardizer(F_cal)`;
   - `RidgeProbe([λ*]).fit(F̃_cal, Y_cal, F̃_cal, Y_cal)`. RidgeProbe does not standardise and requires validation arguments; with a singleton grid there is nothing to select.
   - Its predictions on F_cal must equal `nested_ridge`'s `pred_val` within max abs 1e-10 (cho_solve versus lstsq). This is part of gate M1.

**Fit split.** All 8192 calibration natural source activations. No donors, no patched states, no validation rows.

**Targets:**

| Decoder | Target | Use |
|---|---|---|
| (i) | w32 one-hot (36 columns, canonical order) | ŵ = argmax, ties to the lowest index; the damage metric D_w |
| (ii) | ν(b32), the 12-state y-marginal | ŷ; the damage metric D_y and leakage |
| (iii) | m32 (2 columns) | diagnostic only; never in a gate |

**Gate M4 (adequacy, unpatched eligible rows; validation, then fresh).**
- Accuracy of ŵ ≥ 0.95;
- `r2_pooled(ŷ, ν, mean_cal)` ≥ 0.50, with SST around the calibration mean (`r2_pooled` returns None if SST is degenerate, which also fails).

Otherwise INCONCLUSIVE/DECODER_INADEQUATE.

**Why decoders are fixed rather than refitted.** The forced state is an additive, nearly invertible shift, so refit-recoverability damage is ≈ 0 for every condition and measures nothing (X-4). What matters for a frozen downstream readout is how **fixed** decoders read the forced state. X's refit-recoverability numbers may be reported descriptively; they are never gated.

---

## 8. Damage and leakage gates (M2)

### 8.1 Metrics
For an intervention X ∈ {T, C_0, …, C_31} on n eligible rows of a split:
- D_w(X) = (1/2n) Σ_{i,±} 1[ŵ(a^±_{X,i}) ≠ ŵ(a_i)];
- D_y(X) = (1/2n) Σ_{i,±} ‖ŷ(a^±_{X,i}) − ŷ(a_i)‖² / tr Cov_cal(ν);
- D(C̄) = mean over r of D(C_r).

### 8.2 Gate M2 (calibration first, as the early stop; then validation; then fresh)
All of the following, per model:

| Requirement | Bound |
|---|---|
| Primary ceilings | D_w(T) ≤ 0.02 and D_y(T) ≤ 0.05 |
| Family ceilings | D_w(C̄) ≤ 0.02 and D_y(C̄) ≤ 0.05 |
| Matching | \|D_w(T) − D_w(C̄)\| ≤ 0.01 and \|D_y(T) − D_y(C̄)\| ≤ 0.02 |
| Dispersion | at least 28 of 32 frames have both D_w(C_r) ≤ 0.02 and D_y(C_r) ≤ 0.05. No frame is dropped; this only checks that outliers do not dominate the family |

Failure → INCONCLUSIVE/FAMILY_UNMATCHED. No redraw and no retuning.

### 8.3 Intended changes versus damage; leakage

| Change | Classification |
|---|---|
| Chart phase; m32 direction; circle radius ‖m32‖; 2nd and 3rd x-harmonics | Intended or allowed: they are part of the circular variable. Radius and harmonic fidelity are reported, not gated |
| Decoded w32 | No change intended (the donor keeps w32), so any change is damage (D_w) |
| Decoded y-marginal | No change intended by the intervention, so any shift is damage (D_y). This is conservative |

The counterfactual itself changes the y-nuisance by ν⁺ − ν⁻. A phase-only intervention cannot and should not reproduce that part, and it caps θ below 1. κ_ν is reported.

**Leakage:**

L(X) = Σ_i ⟨ŷ(a⁺_{X,i}) − ŷ(a⁻_{X,i}), ν⁺_i − ν⁻_i⟩ / Σ_i ‖ν⁺_i − ν⁻_i‖²

If κ_ν ≥ 0.01 (frozen at S3), M2 also requires L(T) ≤ 0.25 on calibration, validation and fresh. Otherwise INCONCLUSIVE/NUISANCE_CONFOUNDED, because the primary could succeed through a y-channel. If κ_ν < 0.01, L is reported only.

---

## 9. Support (gate M3; calibration early stop, then validation, then fresh)

**Within-class Mahalanobis distance** (implemented explicitly; `x4f_scores.support_report` is **not** used, because it uses the linear quantile and its own LW fit, correction C-3):

D_M(a; w, z̃) = ‖W(a − α̂_w − Γ̂ z̃ − r̄)‖

- For S, T and C states, use the source row's w32 and z̃.
- For donor states D±, use w32 and the donor's own z̃ = z(b32(H^±)).
- q99 = `np.quantile(D_M over all 8192 calibration natural rows, 0.99, method="inverted_cdf")`.

**Fractions beyond q99** (eligible rows):
- F(S);
- F(D), pooled over ±;
- F(T), pooled over ±;
- F(C̄), the mean over frames of the pooled fraction.

**K4 chart extension support** (`chart.extend(...).supported` = resultant ≥ 0.2 **and** 8th-NN distance ≤ the chart's support_radius) is reported as the supported fraction, Sup(·).

**Requirements (all must hold):**
1. F(T) ≤ max(0.05, F(D) + 0.02);
2. F(C̄) ≤ max(0.05, F(D) + 0.02);
3. |F(T) − F(C̄)| ≤ 0.02;
4. Sup(S) ≥ 0.99, Sup(D±) ≥ 0.98, Sup(T) ≥ 0.98, Sup(C̄) ≥ 0.98.

Failure → INCONCLUSIVE/SUPPORT.

No row is removed for lack of support. An unsupported row keeps its phase arg z and stays in the endpoint. The every-row K4 support rule applies only inside the 512-row chart panel of branch C (§14), not to the C1 cohort (correction C-4).

X's rule (every state within 1.25 × the calibration max Mahalanobis) is not used. It is a maximum over 10⁴ to 10⁵ objects and fails regardless of the science.

---

## 10. Manipulation and registration (validation, then fresh)

### 10.1 Gate V1: the chart registers the counterfactual (the substantive gate)
- wrap(x) maps an angle to (−π, π].
- δ_i = wrap(φ⁺_i − φ⁻_i), from the chart on the model's own donor activations, in the gauge orientation.
- δ*_i = wrap(arg m32(H⁺_i) − arg m32(H⁻_i)), from the oracle.
- Let med* = `np.quantile(|δ*|, 0.5, method="inverted_cdf")` over eligible rows.
- Among rows with |δ*_i| ≥ med*, the fraction with sign(δ_i) = sign(δ*_i) must be ≥ 0.75. sign(0) counts as disagreement.

Otherwise INCONCLUSIVE/CHART_NOT_REGISTERING. An insensitive chart cannot pass as a negative result.

### 10.2 Gate V2: manipulation
- d^±_i = wrap(φ^±_i − φ^S_i) and e^±_i = wrap(φ(a^±_{T,i}) − φ^S_i).
- κ = Σ_{i,±} e^±_i·sign(d^±_i) / Σ_{i,±} |d^±_i|. Require 0.5 ≤ κ ≤ 1.5.
- Let med = the inverted_cdf median of |d|. Among arms with |d| ≥ med, the fraction with sign(e) = sign(d) must be ≥ 0.80.
- κ for the controls is reported; it is expected to be ≈ 0.

Otherwise INCONCLUSIVE/MANIPULATION_FAILED.

V2 is partly guaranteed by construction, because B is fitted from φ itself. It is a weak check. V1 is the substantive one (correction C-6). Absolute angle thresholds such as π/12 are not used, because within-symbol shifts are small.

---

## 11. Positive control (gate V3; validation, then fresh)

- p^{D±} = the model's own unpatched prediction on H^±. At this final site, that equals full donor-state replacement.
- A_full,i = ½⟨q⁺_i − q⁻_i, log p^{D+}_i − log p^{D−}_i⟩.
- Z_full,i = A_full,i − 0.30·G_i.

**Inference.** Joint whole-row bootstrap with 5000 draws, PCG64 seed 520504 (fresh: 520507). Each draw makes one `rng.integers(0, n, size=n)` call, shared by all models and arrays. The lower bound per model is the 0.05/3 `inverted_cdf` quantile of the resampled mean of Z_full.

**Gate.** All three lower bounds > 0. Otherwise INCONCLUSIVE/MODEL_HEADROOM: the model itself does not discriminate the two counterfactuals, so no phase test can be read.

θ_full = E[A_full]/E[G] is reported. Its validation point estimate goes to the sealed file.

---

## 12. Endpoint, inference and precision

### 12.1 Per-row statistic (crossed regret contrast)
For an intervention pair X = (X⁺, X⁻), with p in canonical order from the float64 log-softmax of the patched logits:

A_i(X) = ½ Σ_v (q⁺_i − q⁻_i)(v)·[log p_{X⁺,i}(v) − log p_{X⁻,i}(v)]
       = ½[KL(q⁺‖p_{X⁻}) + KL(q⁻‖p_{X⁺})] − ½[KL(q⁺‖p_{X⁺}) + KL(q⁻‖p_{X⁻})]

That is, mismatched regret minus matched regret against the exact oracle.

**Properties** (each is checked by the independent tests):
- if p_{X^±} = q^±, then A = G;
- if p_{X⁺} = p_{X⁻}, then A = 0 (so the zero patch gives A = 0 exactly);
- terms constant in v cancel, because Σ(q⁺ − q⁻) = 0;
- additive log-p perturbations common to both arms cancel exactly;
- a common multiplicative temperature β scales A by β.

Arm-asymmetric effects do **not** cancel. The arms do differ, because |d⁺| ≠ |d⁻| when w32 is kept. The cancellation is therefore approximate, and the residual is estimated by the controls (correction C-1).

**Endpoint quantities, per model j and eligible row i:**
- Y_i = A_i(T) − (1/32) Σ_r A_i(C_r);
- θ_j = E[Y]/E[G];
- Z_i = Y_i − c·G_i, with c = 0.10.

The unpatched prediction p_S does not enter. So θ > 0 does not mean improvement over the unpatched prediction.

### 12.2 Fieller equivalence
H5 guarantees E[G] > 0. Therefore θ_j > c ⇔ E[Z_j] > 0, and θ_j < c ⇔ E[Z_j] < 0. The decision is made on a mean, and inverting this test at the margin is exactly Fieller's test. No delta method is needed.

### 12.3 Fresh-test inference
- 5000 draws, PCG64 seed 520503.
- Per draw, one call `idx = rng.integers(0, n_test, size=n_test)`, shared by every model and every array (rows in ascending sequence_id).
- Per model, the resampled mean Z̄*_j.
- L_j = `quantile(Z̄*_j, 0.05/3, inverted_cdf)` and U_j = `quantile(Z̄*_j, 1 − 0.05/3, inverted_cdf)`.
- θ̂_j = Ȳ_j/Ḡ, with descriptive ratio-of-resampled-means intervals from the same draws.
- Chart, fits, decoders and frames are held fixed: inference is conditional on them.

### 12.4 Validation precision (gate P1) and the test-size ladder
`tools/x4_circle_history/precision.py` is used **unchanged**. It is imported with `tools/x4_circle_history` on sys.path, because it does `from errors import Invalid`. The calls, with Z_val and G_val over the n_val validation eligible rows:
- `sd, _ = sd_b4_draws(X={j: Z_val_j}, r4n={j: G_val}, models=[1729, 2718, 3141], seed=520501, draws=5000, size=n_val)`;
- for each N in (4096, 8192, 16384):
  - `e = centered_draws(X={j: Z_val_j}, models, seed=520502, draws=5000, size=N)`;
  - `s = precision_summary(sd, e, models, cfg)`, with cfg = {alpha: 0.05/3, power: 0.80, delta: 0.0, alternative: (0.20 − 0.10)·Ḡ_val, projected_N: N}.

Verified semantics of `precision_summary`:
- mde = delta + (z_{1−α} + z_power)·sd/√projected_N;
- power = mean(alternative + e + q_α > delta);
- PASS requires, for **every** model, mde_upper ≤ alternative **and** power ≥ 0.80.

For Z = Y − 0.10·G, θ = 0.20 corresponds to E[Z] = 0.10·E[G], hence this alternative.

**Ladder rule (pre-declared; counts eligible rows; correction C-5).**
- N_test = the smallest N in (4096, 8192, 16384) with status PASS. If none passes: INCONCLUSIVE/UNDERPOWERED, and the study stops.
- What drives the choice: only validation SDs, centred errors and the oracle mean Ḡ_val. The validation endpoint mean is never used.
- Fresh blocks to sample: k = ⌈N_test / ((f_val − 0.02)·4096)⌉, where f_val is the validation eligible fraction (oracle-only). Since f_val ≥ 0.90, k ≤ 5.
- The endpoint uses **all** eligible rows of the k blocks, n_test.
- The fresh gate (§16, row 20) requires f_test ≥ f_val − 0.02, which guarantees n_test ≥ N_test.

### 12.5 Sealed validation means and secondary quantities
**Sealed.** The validation point estimates Z̄, θ̂ and θ̂_full are written to a sealed file. It is opened only after the fresh result is recorded. The gate report contains `precision_summary` outputs, which hold no means.

**Secondary quantities** (reported, never part of the decision):
- θ_full;
- the phase share ψ = θ/θ_full;
- repair R = ½ Σ_± [KL(q^±‖p_S) − KL(q^±‖p_{T^±})];
- the per-frame A_C;
- κ_ν and L;
- radius and harmonic fidelity;
- the raw-norm ratio;
- Y against |d| (descriptive);
- the float32-vs-float64 logit discrepancy on validation (expected ≤ 1e-4).

---

## 13. Decision rule and precedence

1. **Validity first.** If any gate in §16 is not PASS, the outcome is that gate's status. INCONCLUSIVE/<reason> applies when a valid criterion is not met (including resource exhaustion); FAIL_TECHNICAL applies to an integrity, identity, implementation or numerical defect. A validity failure can never become a scientific FAIL, and the endpoint is not scored after a pre-scoring failure.
2. **Numerical certificate** (§15.3). If for any model |L_j| or |U_j| ≤ max(B_num, 1e-9), the outcome is INCONCLUSIVE/NUMERICAL.
3. **Per model:** PASS_j ⇔ L_j > 0; FAIL_j ⇔ U_j < 0; otherwise INC_j. Equality at 0 is INC_j.
4. **Overall (MERGE ruling 2):**
   - **PASS** iff PASS_j for all three models. This is an intersection–union test, valid at one-sided 0.05/3 per model, so conservative.
   - **FAIL** iff FAIL_j for all three.
   - **MIXED** otherwise. Per-model statuses are reported, with the sentence "the all-three claim is not supported".
5. Licences are as in §1.4. The bootstrap bounds are an unconditional prespecified procedure; no selective-coverage claim is made conditional on passing the fresh gates.

---

## 14. Chart dependency on K4 (MERGE ruling 7)

**Method (identical to K4, from the CONTRACT `chart` section):**
- `chart.fit_chart(X, landmark_ids, cfg, guard, timed)` on raw 128-D float64 activations with Euclidean distances;
- ripser field 47;
- the largest strictly positive finite H1 bar, with ties by birth, death, index;
- midpoint scale;
- the certified integer lift with bounds [1, 2, 4, 8, 16];
- `fit_gauge(chart, m32)`, a reflection and rotation aligning the phase to arg m32 on the landmarks;
- `extend(chart, gauge, Q, cfg)`: 8-NN Gaussian weights with σ = median d8, support resultant ≥ 0.2 and 8th-NN ≤ 2·q0.99(d8);
- the phase it returns is gauged, in [0, 2π).

The gauge does not enter the endpoint, because any rotation or reflection is absorbed into B. It is used by V1. No oracle-angle decoder may substitute for the chart.

### 14.1 Branches
The branch is decided at gate G0, before any C1 data, from K4's final recorded chart-stage gates (chart_calibration, gauge, validation_direct_chart, extension_support, fidelity_A, phase_bins, overall_resultant). K4's final status is taken after any correction jobs the coordinator authorises inside K4 under B5.

- **Branch A (reuse).** All K4 chart-stage gates are PASS for all three models.
  - C1 binds, per model, the chart NPZ sha256 (`chart_to_arrays` output), plus the K4 CONTRACT sha256, the producer commit and the GATES.jsonl records.
  - C1 loads with `chart_from_arrays` and never refits.
  - K4 does not have to pass its own B4 or precision endpoint for the chart to be reusable.
  - The K4 landmarks are the 512 exposed E4 test panel-1 rows, float32-derived. They serve only as the coordinate system, never as C1 data.
  - C1 queries are float64 activations; extension distances are computed in float64.
- **Branch B (stop).** Any K4 chart-stage gate for any model is FAIL_TECHNICAL or INCONCLUSIVE. Then C1 stops: INCONCLUSIVE/CHART_UNAVAILABLE. The same method at the same site has already failed, and there is no refit until it passes.
- **Branch C (construct once).** K4 terminated before its chart stage, for example at its oracle headroom gate, and so never reached charts. Then C1 builds the chart once per model with the identical frozen `chart.py`/`cochain.py` and the K4 CONTRACT `chart` configuration:
  - **Landmarks:** the 512 lowest-sequence_id rows of cal block 0, all sampled rows, natural activations. landmark_ids are 20-digit zero-padded decimal strings of sequence_id, because `fit_chart` requires strictly ascending string ids (correction C-15).
  - **Gauge:** fitted on the landmarks' oracle m32.
  - **Validation chart gates (K4's, on a 512-row panel only; correction C-4):**
    - the direct chart is `fit_chart` on the 512 lowest-sequence_id rows of val block 0, giving direct_phi;
    - `chart_gates(extend(...) of those 512 rows, direct_phi, cfg)` requires support on all 512 rows, fidelity `agreement` ≥ 0.80, every one of the 12 phase bins ≥ 8 rows, and overall resultant ≤ 0.30.
  - **Construction budget:** at most 6 constructions (3 production + 3 direct, K4's `max_chart_constructions`).
  - Any failure → INCONCLUSIVE/CHART_UNAVAILABLE. No other chart family, field, scale, site or landmark set is permitted.
- **K4 not yet final.** C1 waits. This status is not a gate outcome.

**Consequence.** C1 implementation (S0–S2) can proceed now. C1 data stages (S3 onward) wait for K4's chart outcome.

---

## 15. Numerics

### 15.1 Precision
- All C1 forward passes use the exact float64 cast of the frozen float32 weights (§5.1). The float32 state-dict sha256 is recorded before and after every stage and must be unchanged.
- **Identity patch:** `forward_with_patch` with the natural a_i must reproduce the unpatched `logits[:, 32]` **bitwise**. It is run on the 1024 lowest-sequence_id calibration rows at M0, and on every validation and test eligible row.
- **Zero patch:** Δ = 0 for both arms must give A = 0 exactly.
- All oracle, endpoint and statistical arithmetic is float64.

### 15.2 Decimal reference
See §3.4: 4 rows per split, three histories each, 60-digit posteriors in an 80-digit trapping context. All-row Decimal enclosures (X) are not used. They are out of proportion to a 0.10 relative margin and would cost tens of CPU-hours.

### 15.3 Per-row certificate
The recorded float64 logits are treated as the operational model output (X). Bounds cover the post-logit arithmetic and the oracle:
- **Log-softmax error per arm:** ε = 2⁻⁴⁴·(1 + 2·max_v|logit_v|).
- **Oracle vector error:** η = 1e-12 in L1. This is the declared bound, verified on the reference rows.
- **A bound:** b^A_i(X) = ½[‖q⁺ − q⁻‖₁(ε_{X⁺} + ε_{X⁻}) + 2η·‖log p_{X⁺} − log p_{X⁻}‖_∞].
- **G bound:** b^G_i = ½[2η·‖log q⁺ − log q⁻‖_∞ + ‖q⁺ − q⁻‖₁·η·(1/min q⁺ + 1/min q⁻)].
- **Z bound:** b^Z_i = b^A_i(T) + (1/32)Σ_r b^A_i(C_r) + 0.10·b^G_i.
- **Overall:** B_num = max_i b^Z_i, which bounds the error of every resampled mean.

The rule is applied in §13 step 2. Limitation: η is declared and verified on sampled rows, not enclosed per row.

---

## 16. Gate table (exact evaluation order; the first non-PASS stops)

**Conventions.**
- "≥", "≤", ">" and "<" are meant exactly as written.
- Gate records use `stage_records.record_gate`/`run_gate`: `errors.Invalid`/`JoinError` → FAIL_TECHNICAL; `Unresolved` → INCONCLUSIVE.
- **Every-row checks** appear only for algebraic or numerical identities and lineage, whose failure is a defect. **Statistical gates are fraction-based.**
- Eligible rows are used unless stated otherwise.

| # | Stage | Gate | Criterion | Status on failure |
|---|---|---|---|---|
| 0 | pre-data | G0 CHART_BRANCH | §14: branch A or C proceeds | B → INCONCLUSIVE/CHART_UNAVAILABLE; K4 not final → WAIT |
| 1 | S3 | H1 IDENTITY | World/Transition/Emission/checkpoint IDs equal the CONTRACT; `validate_process(T, E, π, 1e-12)`; perms are permutations; `canonical_emission` round trip | FAIL_TECHNICAL/IDENTITY |
| 2 | S3 | H2 SEPARATION | `check_disjoint` over all C1 sequence IDs and stored ones; 0 registry collisions for H, H⁺, H⁻; 0 cross-split collisions; `check_first_token(first, πE, split)` does not raise (p ≥ 1e-4) per block | FAIL_TECHNICAL/LINEAGE |
| 3 | S3 | H3 ORACLE | symmetry ≤ 1e-14; closed form ≤ 1e-12; named = canonical ≤ 1e-12; G cross-model ≤ 1e-12; Decimal: posterior ≤ 1e-12, predictive ≤ 1e-12, surprisal ≤ 1e-10, G ≤ 1e-10 | FAIL_TECHNICAL/ORACLE |
| 4 | S3 | H4 ELIGIBILITY | f_cal ≥ 0.90 and f_val ≥ 0.90 | INCONCLUSIVE/ELIGIBILITY |
| 5 | S3 | H5 HEADROOM | one-sided 0.05 LB of Ḡ_val > 0.01 nat (seed 520505) | INCONCLUSIVE/HEADROOM |
| 6 | S4 | M0 MODEL | checkpoint IDs; float32 sha; float64 round trip bitwise; identity patch bitwise and zero patch, both on 1024 cal rows | FAIL_TECHNICAL/MODEL |
| 7 | S4 | C0-cal CHART | A: NPZ sha equals the K4 record and loads. C: `fit_chart` + `fit_gauge` resolve within the construction budget | A: FAIL_TECHNICAL; C: INCONCLUSIVE/CHART_UNAVAILABLE |
| 8 | S4 | F1 FIT | FWL rank 41, cond ≤ 1e8, σ ratio ≥ 1e-6; Σ_W λ_min > 1e-12·λ_max; ℓ not None | INCONCLUSIVE/PATCH_MODEL_DEGENERATE, SUPPORT_DEGENERATE, RBF_DEGENERATE |
| 9 | S4 | M1 IDENTITIES | §6 identities ≤ 1e-10 relative; frame orthonormality ≤ 1e-12; same frame on both arms; RidgeProbe vs `nested_ridge` ≤ 1e-10 | FAIL_TECHNICAL |
| 10 | S4 | M2-cal | §8.2, plus leakage if κ_ν ≥ 0.01 — **no logits** | INCONCLUSIVE/FAMILY_UNMATCHED or NUISANCE_CONFOUNDED |
| 11 | S4 | M3-cal | §9, all four requirements | INCONCLUSIVE/SUPPORT |
| 12 | S5 | C0-val CHART | C: K4 chart_gates on the 512-row val panel (support all 512, fidelity ≥ 0.80, bins ≥ 8 each, resultant ≤ 0.30). A: no additional gate | INCONCLUSIVE/CHART_UNAVAILABLE |
| 13 | S5 | M4 ADEQUACY | accuracy ≥ 0.95; r2_pooled ≥ 0.50 | INCONCLUSIVE/DECODER_INADEQUATE |
| 14 | S5 | M2-val | as row 10 | as row 10 |
| 15 | S5 | M3-val | as row 11 | INCONCLUSIVE/SUPPORT |
| 16 | S5 | V1 | sign agreement ≥ 0.75 on rows with \|δ*\| ≥ med* | INCONCLUSIVE/CHART_NOT_REGISTERING |
| 17 | S5 | V2 | 0.5 ≤ κ ≤ 1.5 and sign agreement ≥ 0.80 on \|d\| ≥ med | INCONCLUSIVE/MANIPULATION_FAILED |
| 18 | S5 | V3 | all three LB(Z_full) > 0 at 0.05/3 (seed 520504); donor logits are computed here for the first time | INCONCLUSIVE/MODEL_HEADROOM |
| 19 | S5 | P1 | ladder (§12.4): some N PASS; primary and control logits are computed here for the first time; tail-path identity ≤ 1e-12; identity patch bitwise | INCONCLUSIVE/UNDERPOWERED (FAIL_TECHNICAL for identity) |
| — | S6 | ACCEPT | coordinator's independent review of the gate report (sealed means unopened); release R3 names N_test and k | not accepted → stop |
| 20 | S7 | T-PRE | all computed before Z: H1, H2 (registry v2), H3 on test rows; \|f_test − f_val\| ≤ 0.02 and f_test ≥ f_val − 0.02 (so n_test ≥ N_test); LB Ḡ_test > 0.01 (seed 520506); M0 (identity patch on every eligible row), M1, M2 (with leakage), M3, M4, V1, V2, V3 (seed 520507), tail-path identity — same tolerances | INCONCLUSIVE/TEST_GATE: endpoint not scored, arrays sealed and kept (FAIL_TECHNICAL for identity or lineage) |
| 21 | S7 | NUM | §15.3 certificate | INCONCLUSIVE/NUMERICAL |
| 22 | S7 | ENDPOINT | §13 | PASS / FAIL / MIXED |

**Note on row 20.** The fraction condition has two parts:
- |f_test − f_val| ≤ 0.02 is the integrity check of the sampler and the oracle;
- f_test ≥ f_val − 0.02 is the binding part for the ladder.

Under correct sampling the binomial SD of the difference is ≈ 0.004, so the gate is attainable.

---

## 17. Staged plan and CPU forecast

**Resources (owner B4).**
- No CPU-time cap; usage is measured and recorded in one C1 ledger.
- Threads fixed at 1 (BLAS and torch). This is within the ≤ 4 limit.
- ≤ 12 GiB RAM.
- One scientific job at a time.
- Outputs on X: only, in `X:/Downloads/projects/topo-pilot/c1-state-forcing-store/`, under a 16 GiB output envelope. Reaching the envelope stops the job at a safe boundary.
- Safe STOP when C: < 2 GB or X: < 30 GB free.
- Real usage limits, STOP and existing latches always win.
- The main store's listing hash must be unchanged before and after.

**Cost basis.**
- About 54 MFLOP per full forward row.
- Batches of 1024 rows; peak RAM < 4 GiB.
- About 7,400 eligible calibration rows × 64 control states per model are decoded on calibration, and about 3,700 × 64 on validation.

| Stage | Content | CPU forecast |
|---|---|---|
| S0 Written contract | This document → result-blind independent review (Codex first) → corrections → freeze with C1 `PROTOCOL.md`, `CONTRACT.json` (uncapped CPU written as JSON `null`), `API.md`, `TEST_PLAN.md`; freeze sha recorded in the decision log | documents only |
| S1 Independent tests | Two authors work from API.md before any implementation, on synthetic fixtures only (see the list below) | ≤ 0.25 h |
| S2 Implementation | Separate builder, new worktree from the accepted head; reuse per §18; ≤ 2 correction jobs per defect; the full existing suite and the K4 chart/precision tests must pass unchanged | ≤ 0.25 h of tests |
| — | **Wait for K4's chart outcome (G0)** | — |
| S3 Oracle only (release R1) | Registry v1; sample cal and val (12,288 rows); H1–H5; s_max; κ_ν | 0.05–0.25 h |
| S4 Calibration (R2) | Forward passes for S and D± (8192 × 3 × 3 models, activations only); chart (A: load; C: construct ≤ 0.5 h); FWL; Σ_W; decoders (LOPO, 3 targets × 3 models); frames; M0–M3 | 0.4–1.0 h (+ ≤ 0.5 h for branch C) |
| S5 Validation (R2 continued) | Rows 12–19 in order: full passes for S, D±, T± (4096 × 5 × 3); tail path for 64 control states per row; chart extension and decoding of about 240k states per model; bootstraps; P1; gate report; sealed means | 0.3–1.0 h |
| S6 Coordinator ACCEPT | Independent review; registry v2; release R3 (N_test, k) | — |
| S7 Fresh test (R3) | Sample k blocks; row 20; endpoint; certificate; decision; immutable exports | 0.3–1.7 h (k = 2 → 5) |
| S8 Report | Report, review, decision record, morning report (Hebrew) | ≤ 0.1 h |

**S1 test lists.**
- **Author A:**
  - donor transform and symmetry on a tiny periodic HMM;
  - closed-form donor posterior;
  - eligibility with an `inverted_cdf` boundary;
  - the A identities (A = G at p = q; exact cancellation of arm-common additive terms; A scales by β under a common temperature; A = 0 for equal arms);
  - Fieller equivalence and the decision boundaries (equality → INC);
  - bootstrap index order, shared across models;
  - ladder logic, including the k formula;
  - the numerical certificate;
  - named/canonical joins.
- **Author B:**
  - FWL recovery of a known B in a noiseless synthetic case, plus a trap showing that sequential residualisation is wrong;
  - Haar sign convention, isometry and isospectral identities, pair mapping;
  - D_w, D_y, leakage and D_M with q99 `inverted_cdf`;
  - V1/V2 wrap at ±π, sign(0) and median ties;
  - gate order (no logits before M2/M3 pass on calibration; fresh Z never computed when row 20 fails);
  - RidgeProbe/`nested_ridge` equivalence;
  - `stage_records` prerequisite rebinding.

**Total forecast.** Expected 2–6 CPU-h including overhead, tests and the branch-C fallback (MERGE ruling 8). This is a forecast, not a cap. The coordinator may refine it from metered stage timings, but may not change sample counts, methods or stop rules.

---

## 18. Six-field reuse assessment (charter; every reused function verified at 4f219d6)

| Field | C1 |
|---|---|
| **1. Existing functions reused unchanged** | See the grouped list below the table. |
| **2. Not reused, or not reusable unchanged (verified)** | See the second list below the table. |
| **3. Missing capability** | (1) Donor transform with w32 kept, the symmetry and closed-form checks, eligibility, κ_ν, G. (2) The FWL map and forced states. (3) Haar frames and the control family. (4) Kernels for damage, leakage, D_M support, V1–V3. (5) The crossed contrast, Z, the bootstrap decision, the certificate, the ladder k rule. (6) The exposure registry builder and C1 history tables. (7) The Decimal predictive/log helper. (8) The C1 stage driver and bindings: `c1_meter_bind`, C1 release, `stage_records` PREREQUISITE rebinding, `env_identity` imports rebinding, and one ledger initialisation in the existing schema `x4-oracle-profile-ledger-v1` (the meter requires the ledger to exist). |
| **4. Smallest change** | One new package, `tools/c1_state_forcing/`. It contains pure kernels (arrays, configuration and an injected guard/timer in; no hidden I/O or randomness) plus thin bindings and a driver, roughly 900–1,200 lines plus tests. Frozen K4 and job-0014 files are never edited. Nothing new goes into `src/`. |
| **5. Stable interfaces and invariants** | See the third list below the table. |
| **6. Regression checks and next extension** | **Regression:** the existing learner, analysis and oracle-profile suites and the K4 chart/precision tests pass unchanged; the S1 independent tests come first; on real data, the tail path vs `forward_with_patch` and RidgeProbe vs `nested_ridge` equivalences are checked; guard fault tests cover every rebinding (STOP, disk, uncapped ledger, 12 GiB job object). **Next extension:** the same kernels can serve one separately reviewed follow-up without new abstractions, for example a w31-retaining donor (shifting w1..w30) to separate short from long history, or an earlier site if a certified chart exists there. No generic causal or topology framework. |

**Field 1, existing functions reused unchanged (signature → use):**
- **Process and data:**
  - `dataset.sampler.HMMSampler(T, E, π, layout).sample(n, rng)` → (tokens [n, 33], states), emitting first; w33 and the states are dropped;
  - `dataset.checks.process_code(family, mode, sigma, replicate)`, `make_sequence_ids(code, split ∈ {train, dev, test}, n)`, `check_disjoint(**splits)`, `check_first_token(first, p_w, split)`;
  - `contracts.SeedTree(master).generator(name, *scope)` with `.issued`.
- **Oracle:**
  - `oracle.BayesFilter(T, E, π).run(tokens)` → b, q, log_evidence, ce (§3.3);
  - `tools/x4_oracle_profile/oracle_profile.py`: `validate_process(T, E, π, tol)`, `canonical_emission(E_named, perm)`, `circle_features(coords)`, `posterior_means`/`suffix_posterior` (K = 32 equals the full-prefix filter for 32-token histories), `bootstrap_profile(norm, sq, Ks, rng, draws)`, `percentile_interval(samples, probs)` (inverted_cdf);
  - `tests/oracle_profile/independent_reference.decimal_suffix_posterior(T, E, π, suffix, digits ≥ 60)`;
  - `tools/x4_circle_history/error_bound.trapping_context(prec)`.
- **Model:**
  - `learner.stage.load_model(checkpoint)`;
  - `TransformerLM.forward(inputs, return_hooks=...)` (no internal `no_grad`; the caller wraps it);
  - `learner.forward_with_patch(model, inputs, site, index, replacement, return_hooks=())`.
- **Chart:** `chart.chart_from_arrays`, `extend`, `chart_gates`, `agreement`, `phase_bin_counts`, `overall_resultant`, and `fit_chart`/`fit_gauge` with `cochain.py` for branch C only.
- **Statistics:**
  - `precision.sd_b4_draws`, `centered_draws`, `precision_summary` (§12.4);
  - `analysis.x4f_scores.standardizer`, `r2_pooled`, `rbf_bandwidth`, `rbf_map`, `rbf_features`, `ledoit_wolf`;
  - `experiment.x4f_probe.nested_ridge`;
  - `prediction.ridge.RidgeProbe`.
- **K4 helpers:**
  - `scores.canonical_from_named`, `history_digests`;
  - `adapter.cross_model_join(per_model)`;
  - `stage_records.record_gate`, `run_gate`, `refuse`, `write_new`, `save_npz`, `complete`, `begin` (the last with the PREREQUISITE rebinding below);
  - `op_guard.timed_factory(out, wall_s)`, compatible with the `timed=` argument of `fit_chart`/`extend`.
- **Runtime:** `tools/x4_oracle_profile/{meter, controls, winjob}.py`, with module-level names rebound by the C1 binding.

**Field 2, not reused, or not reusable unchanged (verified):**
- `activations.ActivationExtractor`: it returns float32 and needs an ObservationSet and HistoryIndex.
- `x4f_scores.support_report`: it uses the linear quantile and its own LW fit.
- ObservationSet/HistoryIndex for C1 histories: the ObservationSet schema requires 33 tokens, which would store w33.
- `meter_bind.py`:
  - at import it reads the K4 CONTRACT, then applies the 3600/3480 s caps, K4 stage caps and the K4 `release.verify`;
  - the meter's own defaults (`--max-cpu 600`, `--max-wall 3600`) and `winjob.MEMORY_CAP = 8 GiB` also apply;
  - **fix:** `c1_meter_bind.py` reuses meter/controls/winjob/op_guard unchanged and rebinds `controls.JOB_ID/TASK_SHA256`, the `meter.OUT/LEDGER/EMERGENCY/LOCK/ACTIVE/LOG_DIR` paths, `meter.CAP_S = meter.STOP_NEW_S = inf` in memory (JSON `null` in the contract), `meter.OUTPUT_CAP` = 16 GiB, and `winjob.MEMORY_CAP` = 12 GiB;
  - it passes `--max-cpu inf --max-wall inf` and installs a limiter with the owner disk safe-STOP and the op-marker deadline; `meter_bind.disk_reason` and `make_stage_limiter` may be imported as pure helpers;
  - the native-operation deadline is 600 s wall per marked operation (one 1024-row batch, one solve, one chart construction).
- `release.verify`: its schema, issuer `"codex-coordinator"`, K4 STAGES and K4 CONTRACT are all K4-specific. **Fix:** a separately versioned C1 release module with the same checks and the current coordinator as issuer.
- `stage_records.PREREQUISITE`: it is K4's chain. **Fix:** rebind the module global to the C1 chain (oracle → calibration → validation → fresh). `begin()` then enforces no retry, no non-PASS gate earlier, and unchanged evidence from the prior stage. Its K4-named branches are inert for C1 names. The C1 driver adds the release and ACCEPT checks.
- `env_identity.SCIENTIFIC_IMPORTS`: it lacks torch and the C1 modules. **Fix:** rebind before `record()`; verify at S2 that the global is read at call time.
- X4-F's `random_family`, `x4f_damage`, `x4f_gates` and orchestration: they carry dormant defects (X4-F addendum §3).

**Field 5, stable interfaces and invariants:**
- one site, one model set, one next-symbol endpoint;
- donors keep w32;
- every fit and the gauge use calibration only;
- canonical/named joins are exact, and rows are paired by sequence_id;
- no w33 and no sidecar;
- weights frozen; the identity patch is bitwise;
- maps, frames, seeds and artifacts are immutable (`write_new`/`save_npz` use exclusive create);
- gates run in the fixed order, and the first failure stops;
- no row is trimmed;
- no stage is retried.

---

## 19. Stop rules

1. The first non-PASS gate ends the cohort. Outputs, exact values and negative findings are kept (B5: nothing deleted).
2. Frames are never redrawn, regenerated or selected. Decoders, FWL and chart are never refitted after a gate result. No other chart, site, harmonic count, metric or donor step is substituted.
3. No threshold, tolerance, seed or ladder grid changes after any C1 data exist. Reviewer-driven changes happen only before S3.
4. At most 2 correction jobs per technical defect (B5). After that, reformulate or stop and move to queue item D.
5. No fresh rows are added after fresh sampling, and there is no replenishment of any block. A fresh pre-scoring failure seals the arrays unscored.
6. Any identity, lineage or numerical-integrity mismatch stops before classification (FAIL_TECHNICAL).
7. Usage limits, STOP, the disk thresholds, the output envelope and latches always win.
8. B6: if a result would change a published E4 claim, or a frozen criterion would need to change, stop and wait for the owner.
9. Validation means stay sealed until the fresh result is recorded. After fresh exposure, a repair cannot change the method or bring in replacement data.

---

## 20. Parameters for the reviewer to scrutinise (all fixed; changes only before any C1 data)

1. The margin c = 0.10, the planning alternative 0.20, the positive-control threshold 0.30, power 0.80, and α = 0.05/3 per tail (MERGE ruling 3).
2. The donor step of ±1 column (2 cells) with w32 kept; eligibility at the calibration q0.999 of the natural surprisal, with coverage ≥ 0.90.
3. The FWL covariates (ȳ, Var y, ‖m32‖) and the degeneracy bounds (cond ≤ 1e8, σ ratio ≥ 1e-6, which the analyst judged nearly vacuous: L-8).
4. Whitened (within-class LW, phase term retained) versus raw metric for the isometry.
5. Whether a near-placebo Haar family satisfies owner B3-C. The coordinator ruled yes (ruling 1); the reviewer may challenge this.
6. 32 frames and the ≥ 28/32 dispersion rule.
7. Damage tolerances 0.02 / 0.05 / 0.01 / 0.02; leakage 0.25 with the κ_ν trigger 0.01; leakage applied on calibration as well.
8. Support: q99, max(0.05, F(D) + 0.02), 0.02, and K4 support fractions 0.99 / 0.98.
9. V1 0.75 on rows at or above the median |δ*|; V2 κ ∈ [0.5, 1.5] and 0.80.
10. Decoder adequacy 0.95 / 0.50; the λ grid (1e-3 … 10); 2048 features; median bandwidth.
11. Headroom: Ḡ lower bound > 0.01 nat.
12. The ladder grid {4096, 8192, 16384} on eligible rows, the k formula with the 0.02 slack, and the use of all eligible rows in the k blocks.
13. The FAIL-all versus FAIL-any asymmetry (MERGE ruling 2).
14. Symmetry tolerance 1e-14 (changed from L's 1e-15); certificate constants 2⁻⁴⁴ and η = 1e-12; numerical floor 1e-9.
15. Threads fixed at 1, the native-operation deadline of 600 s, and the 16 GiB output envelope.
16. Branch C landmarks (cal b0, 512 lowest IDs) and the 512-row validation chart panel.

---

## 21. Changelog (source per section; corrections applied)

Sources: **L** = track L, **X** = track X, **A** = analyst (MERGE_ANALYSIS) or coordinator (MERGE.md), **W** = this writer's code verification.

| § | Source | Notes |
|---|---|---|
| 1 | L (question, E0–E4, estimand, licences) ∪ X (licence wording, "neither" items, no selective coverage) + A (specificity sentence, ruling 1; FAIL-all/MIXED, ruling 2) | C-1 applied to E2 |
| 2 | L (objects, splits, seed map, fixed streams) + X (exposure registry with sources and donors, exposed-asset table, ruling 6) + A (eligible-row ladder) + W | C-9, C-5 |
| 3 | L (crossed donors, symmetry, closed form, G) + X (operational oracle, cross-model G identity) + W (Decimal helper, trapping context) | C-16, C-18, C-22 |
| 4 | L (single surprisal rule) + A (drop X's TV, \|δ_O\| and y-TV rules) | κ_ν frozen at S3 (W) |
| 5 | L (FWL, forced state, patch paths) + A (ruling 5, float64 `return_hooks`) + W | C-2, C-17, C-7 |
| 6 | L (Haar frames) + A (ruling 1; placebo documented, L-2) | — |
| 7 | L (RFF, LOPO λ) + W (exact refit recipe) | C-14 |
| 8 | L (fixed-decoder damage, leakage) + A (calibration early stop) | C-20 |
| 9 | L (fraction support) + A/W (explicit D_M with inverted_cdf; K4 all-row rule only on the 512 panel) | C-3, C-4 |
| 10 | L (V1, V2) + A (V1 substantive, V2 weak) | C-6 |
| 11 | L (V3) | C-21 |
| 12 | L (A, Y, Z, Fieller, `precision.py`) + A (ruling 4 wording) + W (verified `precision_summary` semantics; k rule) | C-1, C-5 |
| 13 | L + X (validity precedence; "all-three not supported" sentence) | — |
| 14 | L (three-way rule) + A (ruling 7) + W (landmark id strings; 512-panel gates) | C-4, C-15 |
| 15 | L (float64, bitwise identity, Decimal on 4 rows) + X (logits as operational output) + W (certificate constants) | C-19 |
| 16–17 | L (gate order, stages) + X (output envelope, JSON null, one thread) + A (ruling 8 CPU) | C-23, C-25, C-26, C-27 |
| 18 | L + X lists, corrected by W against the code | C-2, C-3, C-9 to C-13 |
| 19 | L ∪ X | — |
| 20 | L§15 + A§6 list + W additions | — |

**Corrections:**
- **C-1 (L-1).** "Cancels exactly every target-independent effect" was replaced by: arm-common additive log-p terms and v-constant terms cancel exactly; multiplicative effects scale A; arm-asymmetric residuals are estimated by the controls.
- **C-2 (L-3).** `ActivationExtractor` (float32; needs ObservationSet/HistoryIndex) was replaced by float64 `TransformerLM.forward(..., return_hooks=("resid_post_3",))`.
- **C-3 (L-4).** `support_report` (linear quantile, own LW) was replaced by an explicit D_M with `inverted_cdf`.
- **C-4 (L-5).** K4's every-row chart support applies only to the 512-row branch-C validation panel. The C1 cohort uses fractions.
- **C-5 (L-6).** The ladder counts eligible rows. The fresh block count k is derived from f_val with a 0.02 slack, and the fresh fraction gate guarantees n_test ≥ N_test.
- **C-6 (L-7).** V1 is described as the substantive gate and V2 as weak.
- **C-7 (L-8).** The degeneracy bound is kept; the partial R² is reported and listed for review.
- **C-8 (L-9).** Donor freshness is checked via X's exposure registry (sources and donors).
- **C-9 (W).** L's binding of C1 ObservationSet/HistoryIndex IDs is incompatible with dropping w33, because the ObservationSet schema requires 33 tokens. C1 history tables replace them.
- **C-10 (W).** `meter_bind.py` cannot be reused unchanged: it reads the K4 CONTRACT, applies the 3600/3480 caps and K4 stage caps, and on top of that the meter defaults to `--max-cpu 600`/`--max-wall 3600` and `winjob` to 8 GiB. A new `c1_meter_bind` replaces it.
- **C-11 (W).** `release.verify` is K4-specific (schema, issuer `codex-coordinator`, stages, CONTRACT). A C1 release module replaces it.
- **C-12 (W).** `stage_records.begin` keys on the K4 PREREQUISITE. The global is rebound.
- **C-13 (W).** `env_identity.SCIENTIFIC_IMPORTS` lacks torch. It is rebound.
- **C-14 (W).** `nested_ridge` returns no weights and standardises features internally, while `RidgeProbe` neither standardises nor runs without validation arguments. The exact refit recipe is specified, and the 1e-10 equivalence is moved to calibration predictions, so decoders freeze at S4 without validation data.
- **C-15 (W).** `fit_chart` requires strictly ascending **string** landmark ids. Zero-padded sequence IDs are used.
- **C-16 (W).** Symmetry tolerance 1e-15 → 1e-14, because emission rows are `logsumexp`-normalised in a different summation order after the shift.
- **C-17 (W).** "No logits on calibration" is made precise: the forward pass returns logits by construction, and they are discarded unread. The only calibration logit comparison is the M0 identity/zero-patch check, which involves no oracle target.
- **C-18 (W).** The existing Decimal reference yields posteriors only. A small Decimal predictive/log helper runs inside `error_bound.trapping_context`.
- **C-19 (X + W).** The certificate is defined relative to the recorded float64 logits, with explicit constants.
- **C-20 (A/W).** The leakage gate also runs on calibration (early stop) and on fresh.
- **C-21 (W).** V3 is repeated on fresh with a new seed (520507).
- **C-22 (X).** The cross-model identity of G is checked to 1e-12.
- **C-23 (L).** Fresh headroom is checked with seed 520506.
- **C-24 (A).** X's sealed retention of w33 was not adopted; w33 and the states are discarded in memory.
- **C-25 (X).** Threads are fixed at 1.
- **C-26 (X).** 16 GiB output envelope; JSON `null` for uncapped CPU.
- **C-27 (W).** The fresh eligible-fraction gate is stated as two-sided integrity plus a one-sided ladder guarantee.

**Rejected from X** (per A §3–§4):
- the sign-field family (X-1);
- the absolute-phase centroid curve (X-2);
- raw-norm rescaling and dual norm matching (X-3);
- refit-recoverability damage as a gate (X-4);
- every-row Mahalanobis/support/angle gates (X-5);
- the nine-rule eligibility (X-6);
- KL(q_D‖q_S) normalisation (X-7);
- no positive control (X-8);
- construct-if-absent charts (X-9);
- the Clopper–Pearson power bound (X-10);
- all-row 80-digit Decimal;
- α = 0.05/6.
