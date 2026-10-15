STATUS: CERTIFICATE_MERGED (not frozen)

# C1-MERGED-v3: crossed counterfactual state forcing at the final readout of the E4 cylinder-O models

**Document identity.** `C1-MERGED-v3`. This is the merged protocol for planning request `coord-c1-freeze-readiness-20261014`. It is `C1-MERGED-v2` (sha256 F9F679DC…12F6) with the numerical certificate of §15.3 merged from the two certificate tracks of request `coord-c1-numcert-20261015`, under the binding coordinator decisions `planning/responses/coord-c1-numcert-20261015.MERGE.md` (sha256 6215A4B9…3DCA), together with every consequential edit. §23 records the merge: what came from each track, every proof step checked, and the errors found and fixed. v2 was itself `C1-MERGED-v1` (sha256 72C86FFC…45D7) with every required change of the independent review `planning/responses/coord-c1-merged-review-20261015.codex.md` (sha256 2894E604…AB17; verdict APPROVE_WITH_REQUIRED_CHANGES) applied; §22 lists those changes, the sections touched and the flags.

**Authority.** The owner's message `archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md` (sha 13160D21…), part B3 item C, with resources from B4 and limits from B5/B6. The binding coordinator decisions are in `planning/responses/coord-c1-freeze-readiness-20261014.MERGE.md`. The adopted design is `…MERGE_ANALYSIS.md` §6, items 1–22. **Erratum to MERGE ruling 4 (review required change 2):** the clause "so an oracle-perfect readout gives θ = 1" is superseded by the oracle-perfect anchor of §1.3. An oracle-perfect primary readout gives θ_T = 1; the control-adjusted endpoint θ equals 1 only when E[Ā_C] = 0. This document does not edit MERGE.md; the coordinator records the erratum there (§22, flag F1).

**Sources.**
- Track L: `…claude.md`.
- Track X: `…codex.md`.
- Independent review of v1: `coord-c1-merged-review-20261015.codex.md`.
- Certificate track X: `coord-c1-numcert-20261015.codex.md` (sha256 6D330509…7714).
- Certificate track L: `coord-c1-numcert-20261015.claude.md` (sha256 AF2CA4CF…E313).
- Certificate merge decisions: `coord-c1-numcert-20261015.MERGE.md` (decisions 1–9).

**Code verified against.** `topo-pilot` main @ 4f219d6, read-only. §18 lists every reused function together with its verified signature and semantics. §21 lists every correction made to the source plans. The code facts cited by the review were re-verified for v2 (§22). For v3, the certificate's code facts were re-read: `oracle/_filter.py` and `_common.py` (`BayesFilter.run`, `normalise_rows`), `tools/x4_circle_history/error_bound.py` (`trapping_context`, `u_digits`, `gamma_digits`, `posterior_envelope`, `_reference_posterior`), `tests/oracle_profile/independent_reference.py` (`decimal_suffix_posterior`), `oracle_profile.bootstrap_profile`/`percentile_interval`, and the pinned numpy 2.2.6 (`requirements.lock`) `quantile` path for `inverted_cdf` and `_methods._mean` (§23.4).

**What this document is.** A planning document, not a freeze. v1 received the result-blind independent review (Codex first, per owner part D). v2 applied the review's required changes and returns to that reviewer for confirmation. v3 attaches the numerical certificate of §15.3 (proof complete; status PROOF_ATTACHED). **Freeze additionally requires the independent review of §15.3 and confirmation of the open items listed in §23.6.** After freeze come independent test authors and implementation. No C1 data stage may start before K4's chart outcome is known (§14).

**How to read the rules.** Every number in this document is fixed. Every inequality is meant exactly as written: strict or non-strict, with no added tolerance. Nothing is selected on validation or test data, with one exception: the pre-declared ladder rule (§12.4), which uses validation precision and the oracle-only validation eligible fraction.

---

## 1. Question, competing explanations, and licences

### 1.1 Question
The models are the three original E4 cylinder-O models (seeds 1729, 2718 and 3141, step 5000). The site is `resid_post_3`, input index 32.

The question: at this site, does the final readout of each model functionally use the learned circular (PH-chart) phase for next-symbol prediction, in the direction that an exact counterfactual oracle prescribes? The alternative is that the phase is only decodable there; m32 is already known to be decodable at R² ≈ 0.997.

At index 32 the only computation downstream of the site is `ln_final` followed by `unembed`. So C1 tests use **by the trained readout at the final site**. It says nothing about how earlier blocks compute the phase.

The test is not trivial. After removing the softmax shift, the unembedding has rank at most 35. The Jacobian of the complete residual-to-distribution map therefore has a kernel of dimension at least 93 at each activation. LayerNorm makes this map nonlinear, so these local null directions are not automatically globally invisible finite displacements.

The study tests **causal efficacy**: setting the variable moves the output in the right direction. It does not test necessity, because nothing is removed.

### 1.2 Competing explanations

| | Explanation | Prediction for A_T | Prediction for the controls | How C1 separates it |
|---|---|---|---|---|
| E1 | Directional use: the readout maps chart-phase changes to predictive changes aligned with the oracle | A_T ≫ 0 | mean A_C ≈ 0 | Endpoint (§12) |
| E0 | Decodable only: the phase lies in directions the readout ignores | A_T ≈ 0 | ≈ 0 | Endpoint, made interpretable by the positive control V3 (§11) |
| E2 | Generic displacement or damage: flattening, LayerNorm scale, off-support distortion, nuisance damage | Exact cancellation in A only of arm-common additive log-p perturbations and symbol-constant terms; a common inverse-temperature β scales A by β. No general conservatism and no unbiased subtraction by the family (note below the table) | same | Crossed contrast (§12.1), matched family (§6), damage gate M2 (§8), support gate M3 (§9) |
| E3 | Nuisance channel: the move also shifts decoded y-nuisance in the counterfactual direction, and the readout uses that | Decoded y-alignment is constrained by the leakage gate. The gate does not bound the fraction of the predictive endpoint attributable to y or exclude every nuisance-mediated explanation. | — | Leakage gate inside M2 (§8.3) |
| E4 | Short-context channel: within-symbol phase mostly carries w31 information | **not separated** | — | A stated limit, not a gate |

**Note on E2 (what the crossed contrast and the controls establish).** In exact arithmetic, arm-common additive log-probability perturbations cancel, and terms constant across symbols cancel. A common inverse-temperature multiplier β scales A by β. This is attenuation only for \(0<β<1\); it does not establish general conservatism for Y when primary and control effects differ.

Averaging over Haar frames eliminates the linear Taylor term of the control contrast. Higher-order terms and the finite, frozen 32-frame mean need not be zero. Matching whitened displacement norms and covariance spectra, together with the damage gates, does not establish equality of orientation-dependent nonlinear effects. The family provides an operational random-direction comparison, not an unbiased subtraction of every generic or nuisance effect.

### 1.3 Estimand
For model j, over naturally sampled, oracle-eligible rows (§4):

θ_j = E[Y_j] / E[G]

Y and G are defined in §12 and §3. Write Ā_C = (1/32) Σ_r A(C_r), so that Y = A_T − Ā_C (§12.1).

**Oracle-perfect anchor (review required change 2; supersedes MERGE ruling 4's θ = 1 clause).** If the primary arms reproduce \(q^+\) and \(q^-\), then \(A_T=G\) pointwise. Consequently,
\[
\theta=1-\frac{E[\overline A_C]}{E[G]}.
\]
The primary oracle-perfect anchor is \(\theta_T=E[A_T]/E[G]=1\). The control-adjusted endpoint equals 1 only when \(E[\overline A_C]=0\). An oracle-perfect full-donor readout gives \(\theta_{\rm full}=1\). These ratios are discrimination indices, not proportions constrained to \([0,1]\).

The estimand is conditional on the frozen chart and its gauge (§14), the calibration fits (§5, §7), the primary QR basis and the 32 frozen frames (§6).

**Specificity statement (MERGE ruling 1; part of every claim).** The comparison measures specificity relative to equal-norm, equal-spectrum displacements in random within-class directions. The random family is a near-placebo:
- by Haar symmetry its expected crossed contrast is ≈ 0 to first order;
- Its leading nonzero frame-averaged Taylor contribution is second order; higher-order contributions remain possible.
- so "beyond the controls" adds little discrimination beyond "A_T exceeds 0.10·G".

This near-zero expected effect is the null being tested against. It is not a defect.

Averaging over Haar frames eliminates the linear Taylor term of the control contrast. Higher-order terms and the finite, frozen 32-frame mean need not be zero. Matching whitened displacement norms and covariance spectra, together with the damage gates, does not establish equality of orientation-dependent nonlinear effects. The family provides an operational random-direction comparison, not an unbiased subtraction of every generic or nuisance effect.

### 1.4 What each outcome licenses
The decision rule is in §13.

**PASS** (all three models have L_j > 0, where L_j is the lower bound of Z = Y − 0.10·G) licenses exactly this claim. In each of the three E4 cylinder-O models at `resid_post_3`/index 32:
- a chart-phase-directed move along the fitted B map, toward the phase the model assigns to a ±2-cell x-translated prefix (w32 kept), moves the next-symbol distribution in the oracle's counterfactual direction;
- it does so by more than 10% of the oracle's own discrimination (θ_j > 0.10);
- it does so beyond matched random-frame moves, that is, relative to equal-norm, equal-spectrum displacements in random within-class directions.

PASS supports causal efficacy of the prespecified chart-phase-directed state changes at the trained final readout, relative to the frozen random-direction family. It does not uniquely attribute the predictive change to phase independently of every collateral feature. This holds for this counterfactual family, on the prespecified eligible population, conditional on the declared gates.

**FAIL** (all three models have U_j < 0) licenses this: at this site and with this operationalisation, chart-phase-directed moves along the fitted B map reach less than 10% of the oracle-aligned discrimination beyond the matched controls, in each of the three models. Because V3 passed, each model's discrimination of the counterfactual prefixes exceeded the 0.30 normalized threshold at the prespecified nominal level (lower bound of mean Z_full > 0, §11). A FAIL is therefore a scoped lack of *practical* support for use of this phase component. It does not show that the circle is epiphenomenal: other sites, harmonics or nonlinear operationalisations remain open.

**MIXED** (any other combination of valid per-model results) licenses only two things:
1. the all-three claim is not supported;
2. the per-model statuses PASS_j / FAIL_j / INC_j are reported as computed, each at nominal one-sided level 0.05/3 (§13).

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
9. that the matching controls every nuisance, or that the random-direction family subtracts every generic or nuisance effect: matching is empirical, within the stated tolerances (§1.2, note on E2);
10. selective confidence coverage conditional on passing the fresh validity gates. The bootstrap bounds are reported as the prespecified unconditional procedure; their tail levels and coverage are nominal approximations (§13).
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
| Calibration | 8192 | cal b0, b1 | 8 × 1024 | All fitting: s_max, κ_ν, FWL map, Σ_W, decoders, q99, and (chart branch C) the landmarks. Early-stop gates M2/M3. Logits follow the computation-order rule below: on calibration no logit is read except for the declared M0 identity/zero-patch checks. |
| Validation | 4096 | val b0 | 4 × 1024 | All feasibility gates, positive control V3, precision P1. Endpoint means are written to a sealed file. |
| Fresh test | k × 4096, k ∈ {1, …, 5} by the ladder (§12.4) | test b0..b(k−1) of b0..b4 | — | The single endpoint. Sampled only after the coordinator ACCEPTs the validation gate report. |

**Computation-order rule (logits; review required change 12).** Required activation forwards and model-construction checks may generate logits internally. Those logits are discarded unread, except for declared identity/zero-patch checks. Donor logits are first retained for scientific use at V3; primary and control logits are first retained for endpoint/precision use at P1. Fresh A/Y/Z are not evaluated before T-PRE passes, apart from the declared target-free identity checks.

- **Panel assignment:** panel = 4·block + ⌊rank_in_block / 1024⌋, where the rank is by ascending sequence_id.
- **Population used in each fit:**
  - fits that need only natural rows (s_max, FWL, Σ_W, decoders, q99) use **all** 8192 calibration rows;
  - every gate statistic and the endpoint use **eligible** rows only (§4), with the explicit exceptions stated next.
  - All production fits use calibration. The direct validation chart is a fixed-rule fidelity comparator only and is never used to construct interventions. Explicit exceptions to eligible-only evaluation include the declared all-row fits, M0 calibration panel, registry checks, sampler diagnostics, and branch-C chart panels.
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
- **(a)** w1..w32 of every row of every ObservationSet in the main artifact store (E4 train/dev/test for all three models), each canonicalised with its own EmissionSpec perm;
- **(b)** every history stored in the X4, X4-B2, job-0014, K4 (0015/0016) and X4-F stores, plus every constructed donor or counterfactual prefix recorded there;
- **(c)** every planning-feasibility history recorded under `agent-handoff`;
- **(d)**, for the fresh stage only, every C1 calibration and validation H, H⁺ and H⁻.

(Source classes are labelled (a)–(d) in v2. The review's \(R_1\), \(R_2\) below denote registry versions 1 and 2; they are unrelated to the releases R1–R3 of §17.)

Registry manifests bind scanned inputs by content hashes, including canonicalization metadata and identity material. A filename listing alone is insufficient. The coordinator certifies completeness in the release. An incomplete registry blocks the release (INCONCLUSIVE/REGISTRY_INCOMPLETE).

Freeze points:
- version 1 (sources a–c) is frozen before S3 sampling;
- version 2 (sources a–d) is frozen before fresh sampling.

Both are bound by sha256 in the release that authorises sampling.

**Requirement.** Define \(U_s=\bigcup_i\{H_i,H_i^+,H_i^-\}\) for split s. Calibration and validation require \(U_{\rm cal}\cap R_1=\varnothing\), \(U_{\rm val}\cap R_1=\varnothing\), and \(U_{\rm cal}\cap U_{\rm val}=\varnothing\), where \(R_1\) is registry version 1. Fresh requires \(U_{\rm test}\cap R_2=\varnothing\), where registry version 2 contains version 1 and both complete C1 earlier split unions. Cross-split disjointness includes every source/donor role combination.

Under correct seeding, a collision between 32-symbol histories has negligible probability. Collision detection stops as a lineage alarm (FAIL_TECHNICAL/LINEAGE); it does not logically prove that a seed defect caused the collision. The check is every-row for this reason (§16 note).

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
- G is permutation-invariant. It is computed per model in named order and must agree across the three models to ≤ 1e-12 (X: verify, do not assume). **v3:** the named-order value is computed from the canonical q̂ and ℓ̂ arrays permuted into named order (permuted, not recomputed), with the G kernel of §15.3.2 C3 applied in named order. It then differs from the canonical Ĝ_i only in summation order, so for a correct join |Ĝ_named − Ĝ_i| ≤ γ_35·Σ_v|fl(d̂_v λ̂_v)| (two ordered 36-term sums of the same 36 float products, ½ applied exactly), about 3.9·10⁻¹⁵·Σ_v|d̂_v λ̂_v|; two models' values differ by at most twice that. The 1e-12 tolerance therefore detects join and permutation defects, and rounding alone cannot trip it unless Σ_v|d̂_v λ̂_v| exceeds 125 (its plausible size is of order 2Ḡ ≈ 10⁻¹).

**Operational G (v3; MERGE numcert decision 4).** Ĝ_i is computed once per row, in canonical order, by §15.3.2 C3. It is the single value used by H5, V3, Z, Z_full and θ̂ for all three models, and by the certificate. The per-model named-order values serve only the cross-model identity check above.

**One canonical oracle (v3).** The oracle, Ĝ and their certificate are computed once per row, on the two donor histories, not once per model (MERGE numcert decision 9). This requires the canonical process to be one object: gate H1 checks that the three models' E_canon arrays are bitwise identical (equal sha256 of dtype, shape and C-order bytes, as in K4's `process_digest`), with T and π shared by construction. Approximate equality, or the 1e-12 cross-model checks, is insufficient for sharing (K4 CONTRACT: "canonical references shared across models only after exact process and history equality").

### 3.4 Decimal reference (gate H3)
**Rows.** The 4 lowest-sequence_id eligible rows per split (cal, val, test), each for H, H⁺ and H⁻.

**Method.** Inside `decimal.localcontext(error_bound.trapping_context(80))`:
- posteriors b31 and b32 from `independent_reference.decimal_suffix_posterior(T, E_canon, π, suffix, digits=60)`, with suffix = w1..w31 and w1..w32 respectively;
- the predictive Σ_z b(z) Σ_z′ T(z, z′) E(z′, v), and Decimal `ln` for surprisals and G. This is a small new helper; the existing reference returns posteriors only. The same predictive helper is step 2 of route F (§15.3.7); it runs at a context precision of at least 60 digits, and its envelope β_q uses γ^(60), which is valid for any precision ≥ 60.

**Tolerances (v3: aligned with the proved bounds of §15.3; MERGE numcert decision 5).**
- posterior and predictive: componentwise |x̂/x̃ − 1| ≤ 2·10⁻¹², compared in exact rationals. For a reference row whose donor or source history fails precondition P1 of §15.3.3, the absolute criterion max|x̂ − x̃| ≤ 2·10⁻¹² is used instead (an implementation check only; §15.3.12);
- surprisal ≤ 1e-10;
- G: |Ĝ_i − G̃_i| ≤ b^G_i + 10⁻³⁰, with Ĝ_i the canonical value (§3.3) and b^G_i from §15.3.8, compared in exact rationals. On calibration, where no certified decision is made, the certificate inputs of b^G_i (§15.3.6) are computed for these 4 reference rows only. The allowance 10⁻³⁰ covers the Decimal value's own error, which is below 10⁻⁴⁵ (β_q ≈ 10⁻⁵⁵, 60-digit `ln`, |λ| ≤ 1500).

Why these values (§15.3.12): 2·10⁻¹² exceeds 1.06·10⁻¹², the proved componentwise bound for **any** evaluation of `BayesFilter`'s expressions by IEEE binary64 operations in any summation order (Theorem 1 with dense support, d = N). A correct operational pipeline therefore cannot fail them unless it is not such an evaluation, which is itself a defect. The v2 absolute 1e-12 sat marginally below that bound for entries near 1.

Any trap or mismatch → FAIL_TECHNICAL/ORACLE.

### 3.5 Oracle headroom (gate H5; fresh pre-scoring)
`bootstrap_profile` returns a dictionary, and its `rng` argument requires a `Generator`, not a bare `PCG64`. Over the validation eligible rows, with G the vector of G_i:

```python
seed = 520505  # validation; 520506 for fresh
result = oracle_profile.bootstrap_profile(
    norm={1: G},
    sq={1: G},
    Ks=(1,),
    rng=np.random.Generator(np.random.PCG64(seed)),
    draws=5000,
)
lower = float(
    oracle_profile.percentile_interval(result["B"][:, 0], [0.05])[0]
)
```

`percentile_interval` uses `inverted_cdf`. The gate requires `lower > 0.01` (nat), subject to the signed numerical guard of §15.3.11 (H). Use seed 520506, with the same call, on the fresh eligible rows. Calibration Ḡ is reported only.

**Certified mean arithmetic (v3; §15.3.2 C7).** The code block above fixes the RNG, seed, draw count, index semantics, returned schema and percentile helper. For the gate value, the mean arithmetic inside the index loop is replaced by the certified balanced-tree mean kernel, because `bootstrap_profile` takes no mean-kernel argument and its `np.mean` is not on the certified path. C1's thin wrapper `c1_bootstrap_means(x, rng, draws)` makes, for each draw in order, exactly the one call `idx = rng.integers(0, n, size=n)` that `bootstrap_profile` makes (never batched across draws), and stores `tree_mean(x[idx])`. Then `lower = float(oracle_profile.percentile_interval(means, [0.05])[0])`, with G = the canonical Ĝ vector over the split's eligible rows. NumPy is not monkeypatched, and frozen K4/job-0014 files are not edited. An S1 test shows that the wrapper's index stream is identical to `bootstrap_profile`'s (on integer-valued fixtures, whose sums are exact, the two return bitwise-equal means).

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

Logits returned by these forwards follow the computation-order rule (§2.2): they are discarded unread, except for the declared identity/zero-patch checks.

**Notation, per model and row:**
- a_i: natural activation;
- a^±_i: the model's activation on H^±_i;
- φ^S_i = φ(a_i) and φ^±_i = φ(a^±_i): gauged phases from `chart.extend` (§14);
- f(φ) = (cos φ, sin φ).

### 5.2 FWL regression (calibration, all 8192 natural rows, OLS via `numpy.linalg.lstsq`)
a_i = Σ_w α_w·1[w32(i) = w] + Γ z̃_i + B f(φ^S_i) + ε_i

- The design has 41 columns: 36 symbol indicators (no global intercept), 3 nuisance covariates z̃, and 2 phase columns.
- z̃ = z(b32(H_i)), standardised with the calibration mean and population SD. Constant nuisance columns use scale 1 and are handled by the rank gate.
- Gate F1 requires all of:
  - full column rank 41;
  - 2-norm condition number of the design ≤ 1e8;
  - σ_max(B) > 0, evaluated before the ratio;
  - σ_min(B)/σ_max(B) ≥ 1e-6.

  Otherwise INCONCLUSIVE/PATCH_MODEL_DEGENERATE.
- **Reported, not gated:** the within-class partial R² of f(φ), and the partial R² against a per-x-column slope model (misspecification diagnostic).

**Why this regression.** By Frisch–Waugh–Lovell, B is estimated only from **within-symbol**, nuisance-adjusted covariation of a with the chart phase. That is exactly the variation the w32-preserving donors change.

Let C contain the 36 symbol indicators and three standardized nuisance columns, F contain the two phase columns, and A contain the activation rows. With \(M_C=I-CC^+\),
\[
\widehat B^{\,T}=(F^TM_CF)^{-1}F^TM_CA.
\]
F1 establishes identification through full rank of \([C,F]\). Distinct symbol-column tangent directions alone do not guarantee identification after nuisance adjustment. Constant nuisance columns use scale 1 and are handled by the rank gate. F1 additionally requires \(\sigma_{\max}(B)>0\) before evaluating the singular-value ratio.

Including ‖m32‖ adjusts the fitted phase coefficient for its linear association with the oracle radius. It does not guarantee radius preservation by the intervention.

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
- Q̃ = an orthonormal basis of span(W B), from the QR decomposition W B = Ũ R̃ of the 128×2 matrix W B, with the positive-diagonal sign convention: Q̃ = Ũ·diag(sign(diag R̃)), matching the control convention below.
- A rank-deficient QR input causes the appropriate degeneracy failure; it is never redrawn. For W B, rank deficiency is already excluded by F1 (INCONCLUSIVE/PATCH_MODEL_DEGENERATE). For a frame draw G_r, a zero diagonal entry of R_r gives a frame that fails the M1 orthonormality identity (FAIL_TECHNICAL).
- Primary whitened coordinates: c^±_i = Q̃ᵀ W Δ^±_i ∈ R². This is exact, since W Δ ∈ span(W B).
- For r = 0..31:
  - draw G_r = `rng_r.standard_normal((128, 2))` (§2.3);
  - take the QR decomposition G_r = U_r R_r;
  - set Q_r = U_r·diag(sign(diag R_r)), a Haar 2-frame.
- No draw is rejected, regenerated or selected.
- Control displacement: Δ^±_{r,i} = W^{−1} Q_r c^±_i. Control state: a^±_{C_r,i} = a_i + Δ^±_{r,i}.
- **The same frame Q_r maps both arms of a row.**

**Identities (gate M1, relative error ≤ 1e-10 as defined in the comparison definitions below):**
1. Per-row whitened norm: ‖W Δ^±_{r,i}‖ = ‖c^±_i‖ = ‖W Δ^±_i‖.
2. Spectrum: the whitened second-moment matrix Q_r S Q_rᵀ has the same eigenvalues as Q̃ S Q̃ᵀ, for both the uncentred and the centred S defined below. So trace and spectrum match exactly in exact arithmetic.
3. Frame orthonormality: ‖Q_rᵀ Q_r − I‖_max ≤ 1e-12.

**M1 comparison definitions (review required change 7).** For each norm identity, divide absolute error by the primary norm when it is positive. If the primary norm is zero, require the primary coordinates and control displacement to be exactly zero.

For the uncentered second moment, \(S=\sum cc^T\). For the centered version, \(S=\sum(c-\bar c)(c-\bar c)^T\), with the mean taken over the pooled eligible rows and both arms.

Compare sorted spectra using their maximum absolute difference divided by the primary spectrum’s maximum absolute eigenvalue. If that denominator is zero, require both moment matrices to be zero. Retain the `1e-10` relative threshold and `1e-12` frame-orthonormality threshold.

These identities concern displacement covariance in whitened coordinates. They do not assert equality of the covariance of complete patched activations.

(Componentwise relative comparisons would encounter the 126 zero eigenvalues of these rank-two matrices.)

Information damage and support are not identities. They are measured and gated on calibration **before any logit is retained for scientific use** (computation-order rule, §2.2; §8, §9), and again on validation and test.

**Metric.** "Norm" means the within-class Mahalanobis norm. This makes the norm requirement coincide with support, and it is invariant to the anisotropic scale of the residual stream. Matching raw L2 norm in random directions would push controls off-support along low-variance directions, the mirror image of the X4-F mismatch.

The raw-norm ratio mean‖Δ_C‖ / mean‖Δ_T‖ is reported per frame and not gated. Raw-norm ratios are reported because raw-scale differences can affect both the mean contrast and its variance.

**Overlap with the primary.** The expected squared overlap of a Haar frame vector with span(W B) is 2/128. X's sign-field family is not used: it has two destinations per row, about half of the fields reproduce the primary, and the family mean is ½·reflection.

**Owner B3-C.** The family is matched in advance in norm and variance (exactly, by construction) and in information damage (gate M2), with a matching gate that stops early on calibration (MERGE ruling 1). The independent review accepts ruling 1 under this explicit operational interpretation: displacement norm and variance are matched in the declared whitened metric, and information damage is matched through the declared decoder metrics. A near-placebo family does not itself violate B3-C. The matching does not establish equality of orientation-dependent nonlinear effects (§1.2, note on E2).

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

**Why decoders are fixed rather than refitted.** Fixed decoders measure changes in the responses of prespecified readers. Refit recoverability answers a different question. Because the displacement depends on the activation through the chart, invertibility of the intervention is not assumed. X's refit-recoverability numbers may be reported descriptively; they are never gated.

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

The counterfactual itself changes the y-nuisance by ν⁺ − ν⁻. A chart-phase-directed move along the fitted B map cannot and should not reproduce that part. Donor nuisance changes can affect the achievable discrimination of this intervention. They impose no general mathematical upper bound on θ. κ_ν is reported.

**Leakage:**

L(X) = Σ_i ⟨ŷ(a⁺_{X,i}) − ŷ(a⁻_{X,i}), ν⁺_i − ν⁻_i⟩ / Σ_i ‖ν⁺_i − ν⁻_i‖²

If κ_ν ≥ 0.01 (frozen at S3), M2 also requires L(T) ≤ 0.25 on calibration, validation and fresh. Otherwise INCONCLUSIVE/NUISANCE_CONFOUNDED, because the primary could succeed through a y-channel. If κ_ν < 0.01, L is reported only.

Decoded y-alignment is constrained by the leakage gate. The gate does not bound the fraction of the predictive endpoint attributable to y or exclude every nuisance-mediated explanation.

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
- **Computation (v3).** A_full is computed in the logit-difference form of §15.3.2 C4, with the recorded donor logits, and Z_full by C6 with the canonical Ĝ (§3.3).

**Inference.** Joint whole-row bootstrap with 5000 draws, PCG64 seed 520504 (fresh: 520507). Each draw makes one `rng.integers(0, n, size=n)` call, shared by all models and arrays. The resampled means use the certified balanced-tree mean kernel (§15.3.2 C7). The lower bound per model is the 0.05/3 `inverted_cdf` quantile of the resampled mean of Z_full (one-based rank 84 of 5000, §15.3.2 C7).

**Gate.** All three lower bounds > 0, subject to the signed numerical guard of §15.3.11 (V). Otherwise INCONCLUSIVE/MODEL_HEADROOM. V3 did not establish that the model exceeds the prespecified 0.30 normalized discrimination threshold with the required lower bound. This can reflect insufficient discrimination, uncertainty, or a numerical/technical problem. It does not establish zero discrimination. The phase assay stops as specified.

θ_full = E[A_full]/E[G] is reported. Its validation point estimate goes to the sealed file.

---

## 12. Endpoint, inference and precision

### 12.1 Per-row statistic (crossed regret contrast)
For an intervention pair X = (X⁺, X⁻), with log p in canonical order the log-softmax of the recorded float64 patched logits (read as exact reals; this is the certified target, §15.3.1):

A_i(X) = ½ Σ_v (q⁺_i − q⁻_i)(v)·[log p_{X⁺,i}(v) − log p_{X⁻,i}(v)]
       = ½[KL(q⁺‖p_{X⁻}) + KL(q⁻‖p_{X⁺})] − ½[KL(q⁺‖p_{X⁺}) + KL(q⁻‖p_{X⁻})]

That is, mismatched regret minus matched regret against the exact oracle.

**Computation (v3; §15.3.2 C4; MERGE numcert decision 3).** The recorded float64 logits of both arms are gathered into canonical order (the gather is exact), and Â = 0.5·Σ_v (q̂⁺ − q̂⁻)(v)·(z_{X⁺}(v) − z_{X⁻}(v)), with the ordered sum of §15.3.2. In exact arithmetic this equals the log-softmax definition above up to the term −½(lse(z_{X⁺}) − lse(z_{X⁻}))·Σ_v (q⁺ − q⁻)(v). That term vanishes for exactly normalised q and is bounded in §15.3.9 for the stored weights. The definition is unchanged: the log-softmax form remains the target. The float64 log-softmax is computed only for secondary quantities and for the §5.4 tail-path check.

**Properties** (each is checked by the independent tests):
- if p_{X^±} = q^±, then A = G;
- if p_{X⁺} = p_{X⁻}, then A = 0 (so the zero patch gives A = 0 exactly);
- terms constant in v cancel, because Σ(q⁺ − q⁻) = 0;
- additive log-p perturbations common to both arms cancel exactly;
- a common multiplicative temperature β scales A by β.

Arm-asymmetric effects do **not** cancel. The arms do differ, because |d⁺| ≠ |d⁻| when w32 is kept. What the contrast and the controls establish (correction C-1, as amended by review required change 3):

In exact arithmetic, arm-common additive log-probability perturbations cancel, and terms constant across symbols cancel. A common inverse-temperature multiplier β scales A by β. This is attenuation only for \(0<β<1\); it does not establish general conservatism for Y when primary and control effects differ.

Averaging over Haar frames eliminates the linear Taylor term of the control contrast. Higher-order terms and the finite, frozen 32-frame mean need not be zero. Matching whitened displacement norms and covariance spectra, together with the damage gates, does not establish equality of orientation-dependent nonlinear effects. The family provides an operational random-direction comparison, not an unbiased subtraction of every generic or nuisance effect.

**Endpoint quantities, per model j and eligible row i:**
- Y_i = A_i(T) − (1/32) Σ_r A_i(C_r) = A_i(T) − Ā_{C,i};
- θ_j = E[Y]/E[G]. Oracle-perfect anchor (§1.3): if the primary arms reproduce q⁺ and q⁻, then A_T = G pointwise and θ = 1 − E[Ā_C]/E[G]; θ_T = E[A_T]/E[G] = 1, and θ = 1 only when E[Ā_C] = 0. θ is a discrimination index, not a proportion constrained to [0, 1];
- Z_i = Y_i − c·G_i, with c = 0.10.

The unpatched prediction p_S does not enter. So θ > 0 does not mean improvement over the unpatched prediction.

### 12.2 Ratio-to-mean reduction
For the eligible population, when \(E[G]>0\),
\[
\theta>c\iff E[Y-cG]>0,
\]
and likewise for `<`. This algebraic reduction avoids a delta-method ratio decision. C1 uses a percentile-bootstrap test of the resulting mean. It is not the classical Fieller confidence-set construction. H5 supplies empirical evidence of denominator headroom, not a deterministic guarantee about the population expectation.

### 12.3 Fresh-test inference
- 5000 draws, PCG64 seed 520503.
- Per draw, one call `idx = rng.integers(0, n_test, size=n_test)`, shared by every model and every array (rows in ascending sequence_id).
- Per model, the resampled mean Z̄*_j, computed with the certified balanced-tree mean kernel (§15.3.2 C7).
- L_j = `quantile(Z̄*_j, 0.05/3, inverted_cdf)` and U_j = `quantile(Z̄*_j, 1 − 0.05/3, inverted_cdf)`. These are the order statistics of one-based ranks 84 and 4917 of the 5000 draws; the rank of each returned value is verified at run time (§15.3.2 C7).
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

Every validation endpoint-bearing secondary statistic is sealed until the fresh outcome is recorded, including primary/control contrast means, per-frame contrast means, repair, phase share, and summaries from which the primary endpoint mean can be reconstructed. Validation gate records and centered precision summaries remain available as declared.

**Secondary quantities** (reported, never part of the decision; their validation values are sealed where endpoint-bearing, as above):
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
2. **Numerical certificate** (§15.3; proof attached, subject to its independent review before freeze). For each model j, B_num,j = OUT(max_i b^Z_{j,i}) + r^mean_j is computed as in §15.3.11, and F_j = max(B_num,j, 10⁻⁹). If, for any j, |L_j| ≤ F_j or |U_j| ≤ F_j, compared in exact rational arithmetic, the outcome is INCONCLUSIVE/NUMERICAL. Otherwise, by §15.3 Theorem 6, every per-model status of step 3, and hence the overall outcome of step 4, equals the outcome that exact evaluation of the declared formulas would give on the same rows, recorded logits, stored process weights and bootstrap draws; equivalently, the certified signed bounds L_j − F_j and U_j + F_j have the signs of L_j and U_j. A certificate precondition or integrity defect (§15.3.3: P0, P2, P3, an operational-reference discrepancy above 1/2, a route-F failure, a rank-check failure) is FAIL_TECHNICAL and is decided before this step.
3. **Per model:** PASS_j ⇔ L_j > 0; FAIL_j ⇔ U_j < 0; otherwise INC_j. Equality at 0 is INC_j.
4. **Overall (MERGE ruling 2):**
   - **PASS** iff PASS_j for all three models. This is an intersection–union test at nominal one-sided level 0.05/3 per model, so conservative.
   - **FAIL** iff FAIL_j for all three.
   - **MIXED** otherwise. Per-model statuses are reported, with the sentence "the all-three claim is not supported".
5. Licences are as in §1.4. The bootstrap bounds are an unconditional prespecified procedure; no selective-coverage claim is made conditional on passing the fresh gates.

**Nominal inference (review required change 11).** Bootstrap tail levels and coverage are nominal approximations, conditional on the frozen calibration objects and family. The joint resampling preserves cross-model dependence but does not make percentile-bootstrap coverage exact.

At α = 0.05/3 per tail, the union bound is 0.05 separately for erroneous above-margin declarations and erroneous below-margin declarations across models. It is not a simultaneous 0.05 guarantee covering both directions together.

---

## 14. Chart dependency on K4 (MERGE ruling 7)

**Method (identical to K4 apart from the explicit owner resource override below, from the CONTRACT `chart` section):**
- `chart.fit_chart(X, landmark_ids, cfg, guard, timed)` on raw 128-D float64 activations with Euclidean distances;
- ripser field 47;
- the largest strictly positive finite H1 bar, with ties by birth, death, index;
- midpoint scale;
- the certified integer lift with bounds [1, 2, 4, 8, 16];
- `fit_gauge(chart, m32)`, a reflection and rotation aligning the phase to arg m32 on the landmarks;
- `extend(chart, gauge, Q, cfg)`: 8-NN Gaussian weights with σ = median d8, support resultant ≥ 0.2 and 8th-NN ≤ 2·q0.99(d8);
- the phase it returns is gauged, in [0, 2π).

**Owner resource override (review required change 9).** `cochain.integer_lift` independently enforces `cfg["lift_cpu_cap_s"]`, currently 30 seconds in the K4 CONTRACT; rebinding the meter does not remove it. C1 retains K4’s scientific chart choices and exact lift checks, with the owner’s resource override applied explicitly. In the C1 contract, `lift_cpu_cap_s` is JSON `null`, decoded to positive infinity; `native_operation_wall_s` is 600. The external operation guard remains 600 seconds. The finite lift bounds, node limit, rounding tolerance, and construction-count limit remain unchanged. Frozen K4 files are not edited. (Code note: `integer_lift` evaluates `float(cfg["lift_cpu_cap_s"])` at entry, so the C1 configuration loader decodes `null` to `float("inf")` before the cfg reaches `cochain`; each solver call's time limit is then min(+∞, 600) = 600 s.)

A rotation or reflection is absorbed into B for the primary displacement in exact arithmetic. The complete frozen-family endpoint remains conditional on the gauge and QR basis: changing that basis can change the controls generated by fixed frame draws. No gauge or basis is selected using intervention outcomes. The gauge is used by V1. No oracle-angle decoder may substitute for the chart.

### 14.1 Branches
The branch is decided at gate G0, before any C1 data, from K4's final recorded chart-stage gates (chart_calibration, gauge, validation_direct_chart, extension_support, fidelity_A, phase_bins, overall_resultant). K4's final status is taken after any correction jobs the coordinator authorises inside K4 under B5.

- **Branch A (reuse).** All K4 chart-stage gates are PASS for all three models.
  - C1 binds, per model, the chart NPZ sha256 (`chart_to_arrays` output), plus the K4 CONTRACT sha256, the producer commit, the GATES.jsonl records and the coordinator acceptance record.
  - C1 loads with `chart_from_arrays` and never refits.
  - K4 does not have to pass its own B4 or precision endpoint for the chart to be reusable.
  - The K4 landmarks are the 512 exposed E4 test panel-1 rows, float32-derived. They serve only as the coordinate system, never as C1 data.
  - C1 queries are float64 activations; extension distances are computed in float64.
- **Branch B (stop).** Any K4 chart-stage gate for any model is FAIL_TECHNICAL or INCONCLUSIVE. Then C1 stops: INCONCLUSIVE/CHART_UNAVAILABLE. The same method at the same site has already failed, and there is no refit until it passes.
  - If K4 attempted charts but lacks a complete, accepted PASS record for all required chart gates and models, C1 stops as INCONCLUSIVE/CHART_UNAVAILABLE. Branch C applies only when K4 never attempted chart construction.
- **Branch C (construct once).** K4 terminated before its chart stage, for example at its oracle headroom gate, and so never attempted chart construction. Then C1 builds the chart once per model with the identical frozen `chart.py`/`cochain.py` and the K4 CONTRACT `chart` configuration, identical apart from the explicit owner resource override (above):
  - **Landmarks:** the 512 lowest-sequence_id rows of cal block 0, all sampled rows, natural activations. landmark_ids are 20-digit zero-padded decimal strings of sequence_id, because `fit_chart` requires strictly ascending string ids (correction C-15).
  - **Gauge:** fitted on the landmarks' oracle m32.
  - **Validation chart gates (K4's, on a 512-row panel only; correction C-4):**
    - the direct chart is `fit_chart` on the 512 lowest-sequence_id rows of val block 0, giving direct_phi. It is a fixed-rule fidelity comparator only and is never used to construct interventions (§2.2);
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
See §3.4: 4 rows per split, three histories each, 60-digit posteriors in an 80-digit trapping context. All-row Decimal enclosures (X) are not used for all rows; route F of §15.3.7 applies the 60-digit Decimal enclosure only to donor histories failing precondition P1. Dense all-row Decimal filtering is out of proportion to a 0.10 relative margin and would cost tens of CPU-hours. The ordinary all-row certificate uses the ordered float64 reference oracle of §15.3.2 (C0). These reference-row comparisons are implementation checks, not universal error bounds (§15.3).

### 15.3 Numerical certificate

**Status: PROOF_ATTACHED (v3).** Merged from certificate tracks X and L of request `coord-c1-numcert-20261015` under the binding coordinator decisions 1–9 of `coord-c1-numcert-20261015.MERGE.md` (§23 records the sources, every proof step checked and the errors fixed). **Before freeze it must pass the independent review the protocol requires.**

This section replaces the v2 placeholder written from review required change 6 (RC6). The v1 certificate stays withdrawn: its ε = 2⁻⁴⁴·(1 + 2·max_v|logit_v|), its η = 1e-12 "verified" on four reference rows, and the A/G/Z bounds built on them. Four reference rows cannot establish an all-row bound, a maximum-absolute-error check does not imply an L1 bound, 2⁻⁴⁴ lacked a derivation, rounding and some product-error terms were omitted, and the G bound used η/min(q) without a lower bound on the true probabilities. Neither η nor 2⁻⁴⁴ is used below (§15.3.12). The reference-row comparisons of §3.4 remain implementation checks, not universal error bounds.

**The design in one paragraph.** Every oracle quantity is strictly positive, so oracle errors are tracked componentwise as log-ratios, in the Hilbert projective (oscillation) metric (L). A certificate-only **ordered float64 reference oracle**, whose every summation order is fixed in C1 source and which calls no BLAS (X), is analysed exactly. Its proved componentwise bound grows linearly in the 32 filter steps and has no 1/min q penalty. The operational `BayesFilter` predictive is compared with that reference on every certified history; its bound is the proved reference bound plus the **measured discrepancy**, evaluated in exact rationals (X). No accuracy assumption is made about BLAS, `np.log`, or any library reduction. A history that fails the underflow precondition P1 is certified instead by K4's 60-digit Decimal enclosure (route F; L). A is evaluated in logit-difference form, so no exponential and no log-softmax enters the certified path (L). The 72 oracle logarithms per row are measured against correctly rounded 40-digit Decimal `ln` (L). Ĝ, Â, Ŷ and Ẑ are computed by prescribed ordered kernels whose forward error is proved (L), and bootstrap means by a prescribed balanced-tree kernel (X). Every bound is rounded outward, and every guard is compared in exact rationals.

#### 15.3.1 What is certified, and against what

**Certified decisions.**
- **(E)** The per-model endpoint statuses PASS_j, FAIL_j and INC_j, through L_j and U_j (§12.3, §13), and hence the overall PASS / FAIL / MIXED.
- **(H)** The headroom gate H5 on validation and on fresh rows (§3.5).
- **(V)** The positive-control gate V3 on validation and on fresh rows (§11).

**Exact-arithmetic counterpart.** For each certified decision, D* is the decision obtained by evaluating the declared formulas in exact real arithmetic on exactly the same inputs:
- the stored float64 arrays T, E_canon and π, read as exact reals. This is the operational oracle of §3.3. The stored rows need not be exactly stochastic: b*_t is exactly normalised, whereas the literal predictive b*_32 T E may carry a small mass defect. The certificate covers that literal predictive, with no renormalisation, clipping or flooring;
- the recorded float64 logits, read as exact reals. They are the operational model output (§15.1); no exact-real Transformer pass is approximated;
- the operationally eligible rows (§4);
- the same bootstrap index draws;
- the same order-statistic ranks.

The exact quantities, per donor history h ∈ {H⁺_i, H⁻_i}, are:
- g_1 = π ⊙ E[:, w_1] and g_{t+1} = (b*_t T) ⊙ E[:, w_{t+1}], with b*_t = g_t / Σ g_t;
- q* = b*_32 T E;
- G* = ½ Σ_v (q*⁺ − q*⁻)(v)·(log q*⁺(v) − log q*⁻(v));
- for each arm X, ℓ*_X = z_X − lse(z_X), the exact log-softmax of the recorded logits, and A*(X) = ½ Σ_v (q*⁺ − q*⁻)(v)·(ℓ*_{X⁺}(v) − ℓ*_{X⁻}(v));
- Y* = A*(T) − (1/32) Σ_r A*(C_r), Z* = Y* − (1/10)·G* and Z*_full = A*_full − (3/10)·G*;
- for each draw d, the exact means m*_{j,d} of Z*_j over the drawn rows (likewise for G* and Z*_full), and the order statistics L*_j, U*_j, lower* and L*^V3_j of those exact means at the same ranks.

The coefficients 1/2, 1/32, 1/10 and 3/10 are exact in the target; their float64 representations are accounted for in the bounds.

**Coverage.** Every eligible row of each certified split (validation; fresh); both donor histories of each row; the primary pair, all 32 control pairs and the full-donor pair; all three models; every row statistic and every bootstrap mean that enters a guard. No row is ever removed to obtain a certificate. A history that fails a fast-path precondition takes route F (§15.3.7).

**Sharing.** The oracle and its certificate are computed once per row, on H⁺ and H⁻, not once per model (MERGE numcert decision 9). This is permitted because H1 verifies that the canonical process arrays are bitwise identical across the three models (§3.3, P0). Sharing on approximate equality is not permitted.

**Operational, not certified.** The following are deterministic rules applied to computed float64 values, recorded as computed:
- eligibility and s_max;
- κ_ν;
- every fit (FWL, Σ_W, decoders, chart);
- the M, F, V1 and V2 gates;
- the P1 ladder, including `precision.py`'s SDs, centred draws, normal quantiles and power;
- θ̂, the calibration Ḡ and every secondary quantity.

They define the population, the frozen objects or the test size. A numerical perturbation of them changes *which* valid quantity is assessed; it cannot make a certified decision about that quantity wrong. The statistical meaning of L*, U* (nominal levels, §13) is unchanged: this section concerns arithmetic only.

#### 15.3.2 Permitted computation (prescribed; the implementation uses exactly these expressions)

**Kernels.** An *ordered sum* osum(x_1, …, x_n) means: acc = x_1, then acc = fl(acc + x_k) for k = 2, …, n, in the stated index order. Certified kernels are vectorised only across independent rows (or draws), using numpy elementwise `+`, `−`, `*` and `/` on float64 arrays. No certified kernel calls BLAS, `matmul`, `@`, `dot`, `einsum`, `np.sum` or `np.mean`. Multiplication and addition are separate operations.

- **C0 Reference oracle (certificate only; X).** Per history, vectorised over rows:
  1. û_1(s) = fl(π(s)·E(s, w_1)) for s = 0, …, N−1;
  2. D̂_t = osum over s = 0, …, N−1 of û_t(s), and b̂_t(s) = fl(û_t(s) / D̂_t);
  3. for t < 32: â_{t+1}(z) = osum over z′ ∈ S_col(z), ascending, of fl(b̂_t(z′)·T(z′, z)); then û_{t+1}(z) = fl(â_{t+1}(z)·E(z, w_{t+1})), and step 2 again;
  4. once: TE^ref(z, v) = osum over z′ ∈ S_row(z), ascending, of fl(T(z, z′)·E(z′, v));
  5. q^ref(v) = osum over z = 0, …, N−1 of fl(b̂_32(z)·TE^ref(z, v)).

  Here S_col(z) = {z′ : T(z′, z) > 0} and S_row(z) = {z′ : T(z, z′) > 0} are read from the stored T. Skipping zero entries is bitwise identical to including them, because 0·x = 0 and acc + 0 = acc exactly. Let d = max over z of max(|S_col(z)|, |S_row(z)|), read from the stored T at P0. The documented lazy walk has d = 5; dense support (d = N) is also covered by the proof.
- **C1 Operational oracle.** `oracle.BayesFilter(T, E_canon, π).run(tokens)`, unchanged, on the canonical H⁺ and H⁻; q̂^± = `q[:, 32]`. Its arithmetic (BLAS matrix products, numpy reductions) is not assumed. It enters the certificate only through the measured discrepancy (§15.3.6).
- **C2 Logs.** ℓ̂^± = `np.log(q̂^±)`, stored. They are measured by M-ln (§15.3.6); no property of `np.log` is assumed.
- **C3 G.** d̂ = fl(q̂⁺ − q̂⁻), λ̂ = fl(ℓ̂⁺ − ℓ̂⁻) and Ĝ = 0.5·osum_v fl(d̂_v·λ̂_v) in canonical order, computed **once per row** (§3.3). The per-model named-order values (§3.3) use the same kernel on the permuted arrays.
- **C4 A (logit-difference form; MERGE numcert decision 3).** For a pair X = (X⁺, X⁻), the recorded float64 logits are gathered into canonical order (the gather is exact). Then Δ̂ = fl(z_{X⁺} − z_{X⁻}) and Â = 0.5·osum_v fl(d̂_v·Δ̂_v), with d̂ the C3 array. A_full uses the same form with the donor logits.
- **C5 Y.** m̂_C = fl(osum_{r=0..31} Â_{C_r} · 2⁻⁵) (multiplication by 2⁻⁵ = 1/32), then Ŷ = fl(Â_T − m̂_C).
- **C6 Z.** Ẑ = fl(Ŷ − fl(0.1·Ĝ)) and Ẑ_full = fl(Â_full − fl(0.3·Ĝ)), with the float64 literals 0.1 and 0.3.
- **C7 Means and quantiles.**
  - Every certified bootstrap mean (the §12.3 endpoint, the §11 V3 and the §3.5 H5) is tree_mean(x[idx]), with idx from exactly one `rng.integers(0, n, size=n)` call per draw, in draw order, never batched across draws. tree_mean gathers the values, then adds adjacent pairs level by level (y_k = fl(x_{2k} + x_{2k+1}); an unmatched last entry is carried unchanged) until one value remains, and divides it once by n, which is exactly representable.
  - Quantiles come from `np.quantile(..., method="inverted_cdf")`, directly or through `oracle_profile.percentile_interval`. At numpy 2.2.6 this computes the index from (n, p) alone and returns an input element (`partition` then `take`), with no interpolation (§23.4). For 5000 draws the one-based ranks are ⌈5000·p⌉: **250** for p = 0.05 (H5), **84** for p = 0.05/3, and **4917** for p = 1 − 0.05/3.
  - **Rank check.** For each returned value v and its rank k, the driver verifies #{draws with m̂ < v} < k ≤ #{draws with m̂ ≤ v}, which proves that v is the k-th order statistic. Failure → FAIL_TECHNICAL/NUMERICAL.

The float64 log-softmax is **not** on the certified path. It is computed only for secondary quantities and for the tail-path identity check of §5.4.

#### 15.3.3 Assumptions and checked preconditions

**Assumptions (not checkable from within the run; stated in full).**
- **A1 (IEEE elementwise arithmetic).** Every float64 `+`, `−`, `×` and `/` of the prescribed kernels (C0, C3–C7) and of the bound evaluation (L5) is an IEEE 754 binary64 operation with round-to-nearest, possibly fused with an adjacent operation into a single rounding, and executed without extended precision.
  - **Normal range.** If every operand and the exact result are 0 or of magnitude ≥ 2⁻¹⁰²², then fl(x∘y) = (x∘y)(1+δ) with |δ| ≤ u = 2⁻⁵³. Multiplication by 0.5 or 2⁻⁵ is then exact.
  - **Below the normal range.** If an operand or the exact result is below 2⁻¹⁰²² in magnitude, the absolute error is at most 2⁻¹⁰⁰⁰·max(1, |other operand|). This covers gradual underflow, flush-to-zero and denormals-are-zero; nothing is assumed about which mode is active.

  At H1 a run-time self-test exercises known IEEE cases of these kernels (a round-half-to-even tie in addition, a correctly rounded quotient, a subnormal product) and records the outcome with the environment. It supports A1; it does not prove it.
- **A3 (Decimal).** libmpdec rounds +, −, × and ÷ correctly at the context precision; `Decimal.ln` is correctly rounded under ROUND_HALF_EVEN, as the Python documentation states; and the enabled traps are raised. `Decimal(float)` is an exact conversion. The Python and libmpdec versions are pinned and recorded. This is K4's trust base (ERROR_BOUND.md §5), extended to `ln`; only "error ≤ half a unit in the last digit" is used.
- **A4 (exact helpers).** Python `int` and `Fraction` arithmetic is exact; `float(Fraction)` rounds correctly to nearest; `math.nextafter` is exact.

The label A2 is retired. L's assumption that BLAS and numpy reductions evaluate binary trees of A1 operations is **not used** (MERGE numcert decision 2): no certified kernel calls them, and the operational filter is covered by measurement.

**Not assumed:**
- the accuracy, summation order, blocking, threading or FMA use of BLAS, `np.matmul`, `np.sum` or `np.mean`;
- the accuracy of `np.log`, `np.exp`, libm, SVML, torch or any log-softmax;
- the floating-point underflow mode;
- that the stored rows of T and E sum to exactly 1;
- any property of the model forward pass, since the logits are the recorded operational output.

**Preconditions (checked; each failure has a fixed status).**
- **P0 (structural; once, at H1, in exact rationals on the stored arrays).** All of the following:
  - E_canon > 0 entrywise, π > 0, and T ≥ 0 with a strictly positive diagonal;
  - N = 144 and V = 36 are read from the arrays, and d from C0;
  - with ε_E = min E_canon, π_min = min π and τ⁺ the smallest positive entry of T: π_min·ε_E ≥ 2⁻¹⁰⁰⁰ and τ⁺·ε_E ≥ 2⁻¹⁰⁰⁰;
  - the three models' E_canon arrays are bitwise identical (§3.3).

  ω_TE (§15.3.4) is computed alongside. Failure → FAIL_TECHNICAL/IDENTITY.
- **P1 (per history h, on the reference C0).** Every b̂_t(z), t = 1, …, 32, is finite, and ν_min(h) := min_{t,z} b̂_t(z) ≥ ν₀ := 2⁻¹⁰⁰⁰ / (τ⁺·ε_E), compared in exact rationals. With τ⁺ = 0.2 and ε_E ≈ 2·10⁻²⁰, ν₀ ≈ 2·10⁻²⁸¹; the exact value comes from P0. Failure is **not** an error: h is certified by route F (§15.3.7).
- **P2 (per certified row and model).** Every logit used is finite with |z| ≤ 2¹⁹; q̂ is finite and > 0; ℓ̂ is finite; Â, Ĝ, Ŷ, Ẑ and Ẑ_full are finite with magnitude ≤ 2²¹; the measured ē_ℓ (§15.3.6) is ≤ 2²¹. Failure → FAIL_TECHNICAL/NUMERICAL. For these models, logits are expected well below 10² nats.
- **P3 (Decimal).** Any trap, or any watched flag (Underflow, Subnormal, Overflow) raised in a certificate Decimal computation → FAIL_TECHNICAL/NUMERICAL. This is K4's policy.
- **P4 (operational agreement; per history).** The measured discrepancy r_h of §15.3.6, or x of route F (§15.3.7), is ≤ 1/2. Failure → FAIL_TECHNICAL/ORACLE: the operational oracle then disagrees with a validated reference by more than 50% in some component, which is a defect.

#### 15.3.4 Notation and constants

| Symbol | Definition | Value / bound |
|---|---|---|
| u, u′ | 2⁻⁵³; u/(1−u) | 1.1102·10⁻¹⁶ |
| γ_n | nu/(1−nu), an exact rational | γ_13 ≈ 1.443·10⁻¹⁵; γ_16 ≈ 1.776·10⁻¹⁵; γ_31 ≈ 3.442·10⁻¹⁵; γ_35 ≈ 3.886·10⁻¹⁵; γ_36 ≈ 3.997·10⁻¹⁵ |
| w_u | log((1+u)/(1−u)), the width of one rounding factor | ≤ 2u′ |
| m_u | −log(1−u), the magnitude of one rounding factor; log(1+u) ≤ m_u | ≤ u′ |
| θ(x̂:x) | componentwise log(x̂/x), for positive vectors | — |
| osc(x̂:x), mag(x̂:x) | max θ − min θ, and max \|θ\| | — |
| d | maximum number of nonzero entries in any row or column of T (P0) | 5 for the documented walk |
| ρ_ref | [(L−1)(d+2) + 1]·w_u + (2N + d)·m_u, with L = 32, N = 144 | — |
| ρ̄_ref | [2(L−1)(d+2) + 2 + 2N + d]·u′ ≥ ρ_ref, an exact rational | d = 5: 729·u′ ≈ 8.094·10⁻¹⁴; d = N: 9486·u′ ≈ 1.0532·10⁻¹² |
| ν₀ | 2⁻¹⁰⁰⁰ / (τ⁺·ε_E) | ≈ 2·10⁻²⁸¹ |
| ω_TE | max_z r(z) − min_z r(z), with r(z) = Σ_{z′} T(z,z′)·Σ_v E_canon(z′,v), in exact rationals | a few 10⁻¹⁶ |
| ĉ₁, δ₁ | fl(0.1); \|ĉ₁ − 1/10\| = 1/(5·2⁵⁵) | 5.551·10⁻¹⁸ |
| ĉ₃, δ₃ | fl(0.3); \|ĉ₃ − 3/10\| = 1/(5·2⁵⁴) | 1.110·10⁻¹⁷ |
| d_n | ⌈log₂ n⌉, the depth of the mean tree | 12 for n ≤ 4096; 15 for n ≤ 20,480 |
| ζ | underflow allowance | 2⁻⁸⁰⁰ ≈ 1.5·10⁻²⁴¹ |
| up(c) | `math.nextafter(float(c), +inf)` for a rational c; up(c) ≥ c | — |
| OUT(x) | (1 + 2⁻³⁰)·Fraction(x) + ζ, evaluated exactly | — |

#### 15.3.5 Lemmas

**L1 (nonnegative ordered dot).** Let x, y ≥ 0 be float vectors, and let m be the number of indices with x_k·y_k ≠ 0. Assume every nonzero product and every nonzero partial result lies in the normal range. Then the ordered dot of C0 equals Σ_k x_k y_k (1+θ_k) with (1−u)^m ≤ 1+θ_k ≤ (1+u)^m for every nonzero term. Hence every term's log-factor lies in [m·log(1−u), m·log(1+u)], an interval of width m·w_u inside [−m·m_u, m·m_u]. For an ordered sum of n nonnegative terms without products, the same holds with n − 1 in place of m.

*Proof.* A nonzero term undergoes its own product rounding, then the rounded additions on its way to the result. An addition in which the accumulator is still 0, or the added term is 0, is exact. A nonzero term therefore meets at most m − 1 rounded additions. The first nonzero term meets one for each later nonzero term, at most m − 1. Any other nonzero term meets the addition at which it enters plus one for each later nonzero term; since at least one nonzero term precedes it, that is again at most m − 1. Each rounding contributes a factor in [1−u, 1+u] (A1, normal range); a fused operation contributes one factor instead of two. Finally (1+u)^m ≤ e^{m·m_u} and (1−u)^m = e^{−m·m_u}. ∎

**L2 (positive linear maps do not increase oscillation).** Let x, x̂ > 0 and M ≥ 0 with xM > 0, and let θ = θ(x̂:x). Then every component of θ(x̂M : xM) lies in [min θ, max θ].

*Proof.* (x̂M)_j = Σ_k x_k M_kj e^{θ_k} is a nonnegative combination of the terms of (xM)_j, each scaled by a factor in [e^{min θ}, e^{max θ}]. (X states the same fact as: an exact nonnegative transition maps each output ratio to a weighted average of the input ratios.) ∎

**L3 (normalisation).** Let ĝ and g > 0 have length N, and let θ(ĝ:g) have range [a, a+w]. Let b = g/Σg and b̂ = fl(ĝ / D̂), with D̂ the ordered sum of ĝ, all in the normal range. Then osc(b̂:b) ≤ w + w_u and mag(b̂:b) ≤ w + N·m_u.

*Proof.*
- Write s = Σg. By L1 (n = N terms, N − 1 additions), D̂ = Σ_k ĝ_k(1+θ′_k) with log(1+θ′_k) ∈ [(N−1)·log(1−u), (N−1)·log(1+u)].
- So log(D̂/s) = log Σ_k (g_k/s)·e^{θ_k}(1+θ′_k) lies in [a − (N−1)·m_u, a + w + (N−1)·m_u].
- Then log(b̂_k/b_k) = θ_k + log(1+δ_k) − log(D̂/s), with log(1+δ_k) ∈ [log(1−u), log(1+u)]. Its smallest value is ≥ −w − N·m_u and its largest ≤ w + N·m_u, which is the magnitude bound.
- The term log(D̂/s) is common to every k, so the oscillation grows only by the width of the division factor, w_u. ∎

**L4 (order statistics).** If x, y ∈ ℝ^D satisfy |x_d − y_d| ≤ B for all d, then |x_(k) − y_(k)| ≤ B for every k.

*Proof.* At least k entries of y are ≤ y_(k). Their partners in x are ≤ y_(k) + B, so x_(k) ≤ y_(k) + B. The other direction is symmetric. ∎

**L5 (outward evaluation of bounds).** Let E be an expression tree with nonnegative float leaves, each ≤ 2²¹ (data magnitudes from P2, the per-history ρ^± and ρ̄^± ≤ 4, and constants up(c) ≤ 2); internal nodes + and × only; at most 6 multiplications on any root-to-leaf path; and at most 2¹⁶ leaves. Let Ê be its float64 evaluation, with sums in any order. Under A1, the exact value with exact constants c satisfies E ≤ OUT(Ê).

*Proof.*
- All leaves and nodes are nonnegative and the operations are monotone, so replacing each constant c by up(c) ≥ c can only increase the exact value.
- Every term of the expanded expression passes through at most K = 2¹⁶ + 6 relative roundings, so in the normal range the exact value is at most (1−u)^{−K}·Ê ≤ (1 + 2⁻³⁶)·Ê.
- An operation below the normal range has absolute error at most 2⁻¹⁰⁰⁰·2²¹ = 2⁻⁹⁷⁹ (A1). It is then multiplied by at most five later factors, each ≤ 2²¹, and there are at most 2¹⁷ operations. The total is ≤ 2¹⁷·2⁻⁹⁷⁹·2¹⁰⁵ = 2⁻⁸⁵⁷ < ζ. ∎

Every row bound of §15.3.8–15.3.10, fully expanded, meets these limits: at most 6 multiplications on any path (the deepest monomial is (1/32)·½·(1/(1−u))·(ρ·ρ)·q̂·|Δ̂|, from the control term of b^Y with ρ̄ evaluated as ρ + ρ·ρ; the deepest in (3/10)·b^G, (3/10)·½·(ρ·ρ)·q̂·ρ, has 5), fewer than 7,000 leaves per row and model, and leaves ≤ 2²¹ by P2. The implementation evaluates each bound as displayed, in float64, with the constants replaced by up(·). OUT is monotone, so OUT(max_i b̂_i) ≥ max_i b_i.

**L6 (one rounded difference).** In the normal range, |fl(a − b) − (a − b)| ≤ u·|a − b| ≤ u′·|fl(a − b)|, because |a − b| ≤ |fl(a − b)|/(1 − u). A difference below the normal range has absolute error ≤ 2⁻¹⁰⁰⁰·max(1, |other operand|) (A1), which the "+ζ" of each bound absorbs (lemma U).

**U (underflow allowance).** In every displayed bound, the final "+ζ" covers all below-normal-range events of the computation the bound concerns. Each event has absolute error ≤ 2⁻⁹⁷⁹ (A1 with operands ≤ 2²¹ by P2). It is propagated through at most two later multiplications by quantities ≤ 2²¹ (for example |λ̂| or |Δ̂|), through coefficients ≤ 1 (½, 2⁻⁵, 0.1, 0.3, 1/n), and through relative factors ≤ 2. There are at most 2¹⁶ such events per row bound and model, or per bootstrap mean. The total is ≤ 2¹⁶·2⁻⁹⁷⁹·2⁴³ = 2⁻⁹²⁰ < ζ.

#### 15.3.6 Oracle bound: reference (Theorem 1), operational (Theorem 1′) and measured logarithms

**Theorem 1 (reference oracle, componentwise).** Assume A1, P0, and P1 for history h. Then, for the C0 reference with L = 32 observations,

  mag(b̂_32 : b*_32) ≤ M_b := [(L−1)(d+2) + 1]·w_u + N·m_u,
  mag(q^ref : q*) ≤ ρ_ref = M_b + (N + d)·m_u ≤ ρ̄_ref.

This holds for every symbol v, independently of the history and of the size of q*(v). For d = 5: ρ̄_ref = (436 + 293)·u′ = 729·u′ ≈ 8.094·10⁻¹⁴. For dense support, d = N = 144, the formula gives 9486·u′, which reproduces track L's ρ_q for the BLAS-evaluated filter exactly.

*Proof.*

*Step 0: P1 keeps the whole reference in the normal range.*
- At t = 1, the products π(s)·E(s, w_1) are ≥ π_min·ε_E ≥ 2⁻¹⁰⁰⁰ by P0.
- A transition product b̂_t(z′)·T(z′, z) with T(z′, z) > 0 is ≥ ν₀·τ⁺ = 2⁻¹⁰⁰⁰/ε_E ≥ 2⁻¹⁰⁰⁰.
- Rounding is monotone and every term is nonnegative, so an ordered accumulator never decreases. Hence â_{t+1}(z) ≥ fl(b̂_t(z)·T(z, z)) ≥ (1−u)·ν₀·τ⁺, using the positive diagonal. The exact emission product then satisfies â_{t+1}(z)·E(z, w) ≥ (1−u)·ν₀·τ⁺·ε_E = (1−u)·2⁻¹⁰⁰⁰.
- Every partial sum of nonnegative normal terms is ≥ its first nonzero term, hence normal; in particular D̂_t is normal.
- Every stored quotient b̂_t(z) is ≥ ν₀ ≥ 2⁻¹⁰⁰⁰ (P1). If the exact quotient were below 2⁻¹⁰²², its rounding would be ≤ 2⁻¹⁰²² < ν₀; so every exact quotient is normal.
- The products in TE^ref are ≥ τ⁺·ε_E ≥ 2⁻¹⁰⁰⁰ (P0). TE^ref(z, v) ≥ fl(T(z, z)·E(z, v)) ≥ (1−u)·τ⁺·ε_E, so the products b̂_32(z)·TE^ref(z, v) are ≥ (1−u)·2⁻¹⁰⁰⁰.
- Every posterior entry is ≤ 1 (the ordered accumulator D̂_t is ≥ each of its terms), and every other value is a sum of at most N terms each ≤ N·(1+u)^N, hence below 2¹⁶, so nothing overflows.

Hence A1's normal-range model holds for every operation of C0, and FTZ/DAZ cannot act. All exact quantities are strictly positive (E > 0, π > 0, positive T diagonal), so every log-ratio below is defined.

*Step 1 (t = 1).* û_1 against g_1 has every log-ratio in [log(1−u), log(1+u)], so osc ≤ w_u. By L3, osc(b̂_1 : b*_1) ≤ 2·w_u.

*Step 2 (t → t+1, t ≤ 31).* Let θ_t = θ(b̂_t : b*_t).
- â_{t+1} against a_{t+1} = b*_t T: by L2 for the exact part and L1 for the rounding (m = |S_col(z)| ≤ d), every log-ratio lies in [min θ_t + d·log(1−u), max θ_t + d·log(1+u)], so osc ≤ osc_t + d·w_u.
- The emission multiplication adds w_u.
- The normalisation (L3) adds w_u.

So osc_{t+1} ≤ osc_t + (d+2)·w_u, and therefore osc(b̂_t : b*_t) ≤ [2 + (t−1)(d+2)]·w_u.

*Step 3 (t = L = 32).* osc(û_32 : g_32) ≤ osc_31 + (d+1)·w_u = [2 + 30(d+2) + d + 1]·w_u = [(L−1)(d+2) + 1]·w_u. L3 then gives mag(b̂_32 : b*_32) ≤ M_b.

*Step 4 (T·E prediction).*
- By L1, TE^ref(z, v) = (TE)(z, v)·e^{φ_zv} with |φ_zv| ≤ d·m_u, since row z of T has at most d nonzero entries.
- q^ref(v) = Σ_z b̂_32(z)·TE^ref(z, v)·(1 + θ″_zv) = Σ_z b*_32(z)(TE)(z, v)·e^{θ_z + φ_zv}·(1 + θ″_zv), with |θ_z| ≤ M_b and |log(1 + θ″_zv)| ≤ N·m_u (L1, N positive terms).
- So mag(q^ref : q*) ≤ M_b + d·m_u + N·m_u = ρ_ref.
- Finally, w_u ≤ 2u′ and m_u ≤ u′ give ρ_ref ≤ ρ̄_ref. For d = 5: 2·218 + 293 = 729. ∎

For general L ≥ 1 and support d, ρ̄_ref(L, N, d) = [2(L−1)(d+2) + 2 + 2N + d]·u′; the S1 tests use this form on small HMMs.

**Theorem 1′ (operational predictive; measured discrepancy, X).** For a history h that passes P1, let

  r_h := max_v |Fraction(q̂(v)) − Fraction(q^ref(v))| / Fraction(q^ref(v)),

computed exactly. If r_h ≤ 1/2 (P4), then mag(q̂ : q*) ≤ ρ_h := ρ̄_ref + r_h/(1 − r_h).

*Proof.* q̂(v)/q*(v) = [q̂(v)/q^ref(v)]·[q^ref(v)/q*(v)]. The first factor lies in [1 − r_h, 1 + r_h], whose logarithm lies in [log(1 − r_h), log(1 + r_h)] ⊂ [−r_h/(1 − r_h), r_h]. The second factor's logarithm has magnitude ≤ ρ_ref ≤ ρ̄_ref (Theorem 1). ∎

ρ_h is computed as an exact rational and stored as up(ρ_h). No property of the operational BLAS, of numpy's reductions or of the underflow mode enters: whatever the operational filter did is inside r_h.

**Notation for the rest of §15.3.** ρ^± denotes the oracle bound for H^±_i: ρ_h under P1, or ρ_F(h) from route F. Both are < 3/2 by P4.

**Consequence.** |q̂(v) − q*(v)| ≤ ρ̄^±·q̂(v), with ρ̄ := e^ρ − 1. Indeed q*(v)/q̂(v) ∈ [e^{−ρ}, e^{ρ}], so |1 − q*/q̂| ≤ max(1 − e^{−ρ}, e^{ρ} − 1) = e^{ρ} − 1. For 0 ≤ ρ ≤ 3/2, e^ρ − 1 ≤ ρ + ρ², because Σ_{k≥2} ρ^{k−2}/k! ≤ (e^{3/2} − 5/2)/(9/4) < 0.89; ρ̄ is evaluated as ρ + ρ·ρ. (By P4, ρ ≤ ρ̄_ref + 1 < 3/2 on the main route and ρ_F ≤ 1 on route F.)

**Measured logarithms (M-ln; MERGE numcert decision 6).** For every certified row i, sign ± and symbol v:
- inside `decimal.localcontext(error_bound.trapping_context(40))`, compute 𝓛 = `Decimal(q̂(v)).ln()`; the conversion is exact;
- set e = |Fraction(ℓ̂(v)) − Fraction(𝓛)| + 10⁻³⁸·|Fraction(𝓛)|;
- set ē_ℓ,i = up(max of e over the 72 values of the row);
- a trap or watched flag triggers P3.

By A3, |𝓛 − log q̂(v)| ≤ u_40·|log q̂(v)| = 5·10⁻⁴⁰·|log q̂(v)| ≤ 10⁻³⁸·|𝓛|, since |log q̂(v)| ≤ |𝓛|/(1 − 5·10⁻⁴⁰). Hence |ℓ̂^±(v) − log q̂^±(v)| ≤ ē_ℓ,i. No property of `np.log` is assumed. (X's alternative, validated scalar logarithms of interval endpoints, needs at least as many Decimal logarithms and is not cheaper; decision 6 allows either, and M-ln is used.)

**Corollary 1.** |ℓ̂^±(v) − log q*^±(v)| ≤ ρ^± + ē_ℓ,i for every v. No lower bound on q* is required. This answers RC6's tiny-probability point: an absolute L1 bound divided by min q (about 10⁻²¹ here) would be about 10⁹ and would force INCONCLUSIVE, while the componentwise bound is about 10⁻¹³ to 10⁻¹².

#### 15.3.7 Route F: validated enclosure for a history that fails P1 (K4 machinery; L)

For a donor history h with ν_min(h) < ν₀, the reference may have left the normal range, so Theorem 1 is not used for h. Instead:

1. **Decimal posterior.** b̃ = `independent_reference.decimal_suffix_posterior(T, E_canon, π, h, digits=60)`, with the suffix equal to all 32 tokens, which is exactly the restart-at-π full filter. It runs inside `decimal.localcontext(error_bound.trapping_context(60))`, with K4's flag inspection: C1 replicates, with provenance, the 8-line wrapper `error_bound._reference_posterior` rather than importing a private name (§18). β = `error_bound.posterior_envelope(32, N)` (≈ 10⁻⁵⁵) gives |b̃ − b*_32| ≤ β·b*_32 componentwise (K4 ERROR_BOUND.md §3(a)).
2. **Decimal predictive.** q̃(v) = Σ_z b̃(z)·Σ_{z′} T(z, z′)·E_canon(z′, v), in a 60-digit trapping context. This is the §3.4 helper. Each positive path has at most 2N + 2 roundings: inner product and N additions from 0, outer product and N additions from 0. Set β_q = (1+β)(1+γ^(60)_{2N+2}) − 1, with γ^(60) from `error_bound.gamma_digits(2N+2, 60)`. Then q̃/q* ∈ [1 − β_q, 1 + β_q], because (1−β)(1−γ) ≥ 1 − β − γ ≥ 1 − β_q.
3. **Measured discrepancy.** r = max_v |Fraction(q̂(v)) − Fraction(q̃(v))| / Fraction(q̃(v)), computed exactly.
4. **Row bound.** x = (1 + r)(1 + β_q) − 1. If x > 1/2 → FAIL_TECHNICAL/ORACLE (P4). Otherwise ρ_F(h) = x/(1 − x) ≥ mag(q̂ : q*), because q̂/q* ∈ [(1−r)(1−β_q), (1+r)(1+β_q)] ⊂ [1 − x, 1 + x], log(1 + x) ≤ x, and −log(1 − x) ≤ x/(1 − x).

ρ_F(h) then replaces ρ_h for that history; everything else is unchanged. Route F makes no assumption about float64 arithmetic, BLAS or the underflow mode; this is K4's assumption profile. Cost: 0.5–2 s per history, metered and uncapped. The expected count is 0, because the projected ν_min for this process is about 10⁻¹⁵⁰ or larger, far above ν₀ ≈ 10⁻²⁸¹. The count is reported.

#### 15.3.8 G bound (Theorem 2)

Define, per row i and symbol v (d̂ and λ̂ from C3):
- ε^d_v := u′·|d̂_v| + ρ̄⁺·q̂⁺_v + ρ̄⁻·q̂⁻_v;
- ε^λ_v := u′·|λ̂_v| + 2·ē_ℓ,i + ρ⁺ + ρ⁻;
- b^G_i := ½ Σ_v [ ε^d_v·|λ̂_v| + (|d̂_v| + ε^d_v)·ε^λ_v + γ_V·|d̂_v|·|λ̂_v| ] + ζ.

**Theorem 2.** |Ĝ_i − G*_i| ≤ b^G_i.

*Proof.*
- **Bound on d.** By L6, Theorem 1′ (or route F) and the Consequence, |d̂_v − d*_v| ≤ u′|d̂_v| + |q̂⁺_v − q*⁺_v| + |q̂⁻_v − q*⁻_v| ≤ ε^d_v.
- **Bound on λ.** By L6 and Corollary 1, |λ̂_v − λ*_v| ≤ u′|λ̂_v| + (ρ⁺ + ē_ℓ,i) + (ρ⁻ + ē_ℓ,i) = ε^λ_v.
- **Product.** |d̂λ̂ − d*λ*| ≤ |d̂ − d*|·|λ̂| + |d*|·|λ̂ − λ*| ≤ ε^d|λ̂| + (|d̂| + ε^d)·ε^λ.
- **Reduction.** Each term of the ordered 36-term dot meets one product rounding and at most V − 1 = 35 rounded additions, so the reduction error is ≤ γ_V·Σ_v|d̂_v||λ̂_v| (Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., Lemma 3.1 and (3.5)). Multiplication by 0.5 is exact; below-normal events are inside ζ (U).
- Summing these terms gives b^G_i. ∎

#### 15.3.9 A bound, post-logit evaluation (Theorem 3)

For a pair X with recorded logits z^± in canonical order, write Δ_v = z⁺(v) − z⁻(v) (exact) and Δ̂_v for the computed difference. Define

  b^A_{X,i} := ½ [ (γ_V + u′)·Σ_v |d̂_v||Δ̂_v| + (1/(1−u))·( Σ_v ε^d_v|Δ̂_v| + ω_TE·max_v|Δ̂_v| ) ] + ζ.

**Theorem 3.** |Â_i(X) − A*_i(X)| ≤ b^A_{X,i}.

*Proof.*
1. **lse cancellation.** Since ℓ*_X = z_X − lse(z_X), A* = ½ Σ_v d*_v Δ_v − ½·Δlse·Σ_v d*_v, with Δlse = lse(z⁺) − lse(z⁻).
2. **Residual.** lse is 1-Lipschitz in the ∞-norm, so |Δlse| ≤ max_v|Δ_v| ≤ max_v|Δ̂_v|/(1−u). Moreover Σ_v q*^±(v) = Σ_z b*^±(z)·r(z) with Σ_z b*^±(z) = 1 exactly, so both sums lie in [min r, max r] and |Σ_v d*_v| ≤ ω_TE. The residual is therefore ≤ ½·ω_TE·max_v|Δ̂_v|/(1−u).
3. **Main part.** |Δ̂_v − Δ_v| ≤ u′|Δ̂_v| (L6) and |d̂_v − d*_v| ≤ ε^d_v (proof of Theorem 2), so |d̂Δ̂ − d*Δ| ≤ ε^d|Δ̂| + (|d̂| + ε^d)·u′|Δ̂|. The ordered dot and the factor ½ contribute ½γ_V Σ|d̂||Δ̂| (as in Theorem 2).
4. **Collecting.** ½[γ_V Σ|d̂||Δ̂| + u′Σ|d̂||Δ̂| + (1 + u′)Σ ε^d|Δ̂| + ω_TE max|Δ̂|/(1−u)], and 1 + u′ = 1/(1−u), gives b^A_{X,i}; below-normal events are inside ζ. ∎

**Relation to RC6's guidance.** With no transcendental post-logit evaluation certified (ε± = 0) and the L1 η replaced by the componentwise ρ̄^±q̂^±: the review's term 2η‖ℓ̂₊ − ℓ̂₋‖∞ becomes Σ_v(ρ̄⁺q̂⁺_v + ρ̄⁻q̂⁻_v)|Δ̂_v|, a weighted mean of |Δ̂| that is never larger; the log-softmax normaliser contributes only ω_TE·‖Δ‖∞; and the arithmetic-rounding terms the review required are explicit (γ_V, u′ and ζ).

**Zero patch.** Bitwise-equal arm logits give Δ̂ = 0, so Â = 0 exactly (§15.1 check).

#### 15.3.10 Y, Z and Z_full (Theorem 4)

Per model j and row i, with T the primary pair and C_r the 32 control pairs:

  b^Y := u′|Ŷ| + b^A_T + (1/32)·Σ_r b^A_{C_r} + (γ_31/32)·Σ_r |Â_{C_r}| + ζ,
  b^Z_{j,i} := u′|Ẑ| + b^Y + (u′ĉ₁ + δ₁)·|Ĝ| + (1/10)·b^G_i + ζ,
  b^Zf_{j,i} := u′|Ẑ_full| + b^A_full + (u′ĉ₃ + δ₃)·|Ĝ| + (3/10)·b^G_i + ζ.

**Theorem 4.** |Ŷ − Y*| ≤ b^Y, |Ẑ − Z*| ≤ b^Z_{j,i} and |Ẑ_full − Z*_full| ≤ b^Zf_{j,i}.

*Proof.*
- **Frame mean.** The ordered 32-term sum has error ≤ γ_31·Σ_r|Â_{C_r}| (each term meets at most 31 rounded additions, and each rounding multiplies the exact partial sum by (1+δ), which distributes over its inputs also for signed terms; Higham (3.4)); multiplication by 2⁻⁵ is exact (below-normal events inside ζ). With Theorem 3, |m̂_C − (1/32)Σ_r A*_{C_r}| ≤ (γ_31/32)Σ_r|Â_{C_r}| + (1/32)Σ_r b^A_{C_r}.
- **Y.** Ŷ = fl(Â_T − m̂_C) adds u′|Ŷ| (L6); add b^A_T (Theorem 3).
- **Z.** fl(ĉ₁Ĝ) differs from ĉ₁Ĝ by ≤ u′ĉ₁|Ĝ|; |ĉ₁ − 1/10|·|Ĝ| = δ₁|Ĝ|; (1/10)|Ĝ − G*| ≤ (1/10)·b^G_i (Theorem 2); the final subtraction costs u′|Ẑ|.
- **Z_full.** The same argument with ĉ₃, δ₃ and A_full. ∎

#### 15.3.11 Bootstrap means, B_num, guards and the decision theorem

**Theorem 5 (balanced-tree mean; X's kernel, proof checked and completed).** For model j, any draw d and its index multiset I_d of size n, let m̂_{j,d} = tree_mean(Ẑ_j[I_d]) (C7) and m*_{j,d} = (1/n)·Σ_{k∈I_d} Z*_{j,k}. Then

  |m̂_{j,d} − m*_{j,d}| ≤ max_i b^Z_{j,i} + r^mean_j,  with r^mean_j := γ_{d_n+1}·max_i|Ẑ_{j,i}| + ζ.

*Proof.*
- **Depth.** After level ℓ of the tree every entry is a rounded sum of at most 2^ℓ inputs, and each input has met at most ℓ rounded additions (a carried entry meets none at that level). So one entry remains after d_n = ⌈log₂ n⌉ levels, and each input has met at most d_n additions.
- **Arithmetic part.** In the normal range each addition multiplies the exact partial sum by (1+δ), |δ| ≤ u, which distributes over its inputs; so the computed sum is Ŝ = Σ_a x_a(1+θ_a) with |θ_a| ≤ γ_{d_n} (Higham Lemma 3.1), even with signed terms, and |Ŝ − Σ_a x_a| ≤ γ_{d_n}Σ_a|x_a|. The division by n adds |m̂ − Ŝ/n| ≤ u|Ŝ/n| ≤ u(1 + γ_{d_n})Σ_a|x_a|/n. Together, |m̂ − (1/n)Σ_a x_a| ≤ (γ_{d_n} + u + uγ_{d_n})·max|Ẑ| ≤ γ_{d_n+1}·max|Ẑ|, because (1+u)(1+γ_k) = (1+u)/(1−ku) ≤ 1/(1−(k+1)u) = 1 + γ_{k+1}. Below-normal events: at most n − 1 additions and one division, each ≤ 2⁻⁹⁷⁹ (A1, P2), propagated by factors ≤ 2 and divided by n; the total is far below ζ (U).
- **Input part.** |(1/n)Σ_{k∈I_d}(Ẑ_{j,k} − Z*_{j,k})| ≤ max_i b^Z_{j,i} (Theorem 4). ∎

The same theorem holds for Ĝ with b^G and for Ẑ_full with b^Zf.

*Why this kernel (MERGE numcert decision 7).* L's alternative, r^mean = γ_n·max|Ẑ| for `np.mean`, needs an assumption about numpy's reduction (its own A2), which decision 2 removes from the certified path. The tree kernel is fully specified in C1 source, needs only A1, and is about 10³ times tighter: γ_16 ≈ 1.8·10⁻¹⁵ against γ_20480 ≈ 2.3·10⁻¹².

**Certified constants (exact rationals; n is the eligible-row count of the split being gated, and i runs over its eligible rows).**
- B_num,j := OUT(max_i b̂^Z_{j,i}) + γ_{d_n+1}·Fraction(max_i|Ẑ_{j,i}|) + ζ.
- B^H := OUT(max_i b̂^G_i) + γ_{d_n+1}·Fraction(max_i|Ĝ_i|) + ζ.
- B^V3_j := OUT(max_i b̂^Zf_{j,i}) + γ_{d_n+1}·Fraction(max_i|Ẑ_full,j,i|) + ζ.

By L5 and Theorem 5 these dominate the exact quantities. B_num,j is the review's B_num,j = max_i b^Z_{j,i} + r^mean_j (MERGE numcert decision 8), rounded outward.

**Signed guards (MERGE numcert decision 8).** All comparisons are in exact rationals. The floor 10⁻⁹ is retained as an additional conservative guard; it is not a proof of accuracy.
- **(E) Endpoint, §13 step 2.** F_j := max(B_num,j, 10⁻⁹). If, for any j, |L̂_j| ≤ F_j or |Û_j| ≤ F_j → INCONCLUSIVE/NUMERICAL. Otherwise the certified signed bounds L̂_j − F_j and Û_j + F_j have the signs of L̂_j and Û_j, and §13 step 3 applies.
- **(H) H5.** Let Γ = Fraction(lower̂) − 1/100 and g = max(B^H, 10⁻⁹).
  - PASS iff Γ > g;
  - INCONCLUSIVE/HEADROOM iff Γ ≤ −g;
  - otherwise INCONCLUSIVE/NUMERICAL.

  Validation uses seed 520505 and fresh uses 520506.
- **(V) V3.** Let Γ_j = Fraction(L̂^V3_j) and g_j = max(B^V3_j, 10⁻⁹).
  - PASS iff Γ_j > g_j for every j;
  - INCONCLUSIVE/MODEL_HEADROOM iff Γ_j ≤ −g_j for some j;
  - otherwise INCONCLUSIVE/NUMERICAL.

  Validation uses seed 520504 and fresh uses 520507.

**Theorem 6 (decisions).** Assume A1, A3, A4, P0, P2, P3, P4, and P1 or route F for every certified history, and that the rank checks of C7 pass. Then:
- if the endpoint guard (E) is not triggered, every PASS_j / FAIL_j / INC_j, and hence the overall PASS / FAIL / MIXED, equals its exact-arithmetic counterpart;
- a PASS of (H) or (V) implies that the exact gate passes;
- an INCONCLUSIVE/HEADROOM or INCONCLUSIVE/MODEL_HEADROOM implies that the exact gate fails.

*Proof.*
1. By Theorem 5 and L5, |m̂_{j,d} − m*_{j,d}| ≤ B_num,j for every draw d.
2. The computed and the exact quantiles are order statistics of the same rank k of their 5000-vectors (C7: the rank depends only on (n, p), and the rank check verifies it for the computed vector). L4 then gives |L̂_j − L*_j| ≤ B_num,j ≤ F_j and |Û_j − U*_j| ≤ F_j.
3. If |L̂_j| > F_j, then L*_j ≠ 0 and sign L*_j = sign L̂_j; likewise for U. So PASS_j (L̂_j > 0), FAIL_j (Û_j < 0) and INC_j coincide with their exact counterparts, and the overall rule of §13 step 4 is a function of these statuses.
4. For (H): lower* ≥ lower̂ − B^H > 1/100 + g − B^H ≥ 1/100 when Γ > g; lower* ≤ lower̂ + B^H ≤ 1/100 − g + B^H ≤ 1/100 when Γ ≤ −g. For (V) the same argument with B^V3_j against 0. ∎

#### 15.3.12 η = 1e-12 and 2⁻⁴⁴ (RC6); H3 alignment

Neither constant is retained.
- **η = 1e-12** is replaced by the derived componentwise bounds ρ^±. For comparison, its L1 consequence ‖q̂ − q*‖₁ ≤ ρ̄·Σ_v q̂(v) is ≈ 1.053·10⁻¹² for a dense evaluation of `BayesFilter`'s expressions in any IEEE summation order (Theorem 1 with d = N), slightly **larger** than 1e-12. So 1e-12 could not have been kept as a worst-case L1 bound for the operational filter.
- **2⁻⁴⁴** has no role: no log-softmax and no exponential is evaluated on the certified path (C4).

**H3 alignment (MERGE numcert decision 5; before any data).** The H3 Decimal checks of §3.4 become componentwise |x̂/x̃ − 1| ≤ 2·10⁻¹² for posteriors and predictives, and |Ĝ − G̃| ≤ b^G_i + 10⁻³⁰ for G. These remain implementation checks of the **operational** pipeline; the certificate does not rely on them. The value 2·10⁻¹² is chosen above the bound e^{ρ̄_ref(32,144,144)} − 1 ≈ 1.0532·10⁻¹² that the proof of Theorem 1 gives for any IEEE evaluation of the same expressions, in any binary-tree summation order (a leaf of a tree with n leaves has at most n − 1 addition ancestors), whenever the evaluated posteriors satisfy P1. A correct operational pipeline therefore cannot trip it unless it is not such an evaluation, which is itself a defect (FAIL_TECHNICAL/ORACLE). For a reference row whose history fails P1, no such proof exists, and the absolute criterion max|x̂ − x̃| ≤ 2·10⁻¹² is used as a plain implementation check. The closed-form (§3.2) and named = canonical (§3.3) checks keep their v2 absolute 1e-12; see §23.6.

#### 15.3.13 Expected magnitudes against the 0.10·G margin

These are projections from the bounds, not data. Ḡ is taken to be 10⁻² to 10⁻¹ nat, so 0.10·Ḡ is 10⁻³ to 10⁻².

| Quantity | Typical row | Plausible worst | Ratio to 0.10·Ḡ |
|---|---|---|---|
| ρ̄_ref (log q^ref, every v; d = 5) | 8.09·10⁻¹⁴ (fixed) | same | — |
| r_h (measured operational discrepancy) | ≲ 10⁻¹⁵ | ≈ 1.1·10⁻¹² (an IEEE-order evaluation at its proved dense bound) | — |
| ρ^± = ρ̄_ref + r_h/(1−r_h) | ≈ 10⁻¹³ | ≈ 1.2·10⁻¹² | — |
| ē_ℓ (measured `np.log` error) | ≲ 10⁻¹⁴ (≤ 1 ulp of \|log q\| ≤ 47) | — | — |
| b^G | ≈ 10⁻¹³ to 10⁻¹² | ≤ 5·10⁻¹¹ (\|λ\| ≤ 47) | ≤ 5·10⁻⁸ |
| b^A per pair | ≈ 10⁻¹⁴ to 10⁻¹² | ≤ 10⁻¹¹ (‖Δz‖∞ ≤ 10 nats) | ≤ 10⁻⁸ |
| b^Y, b^Z, b^Zf | ≈ 10⁻¹² | ≤ 3·10⁻¹¹ | ≤ 3·10⁻⁸ |
| r^mean (tree, n ≤ 20,480) | 1.8·10⁻¹⁵·max\|Ẑ\| | ≤ 2·10⁻¹⁴ (max\|Ẑ\| ≤ 10) | ≤ 2·10⁻¹¹ |
| B_num,j, B^H, B^V3_j | ≈ 10⁻¹² to 10⁻¹¹ | ≤ 10⁻¹⁰ | ≤ 10⁻⁷ |
| Binding guard | the 10⁻⁹ floor | the 10⁻⁹ floor | 10⁻⁷ to 10⁻⁶ |

**Risk of INCONCLUSIVE/NUMERICAL (heuristic projection, L).** P1's design implies a bootstrap standard error of the mean Z of about 0.10·Ḡ/3, so SE ≥ 10⁻⁴ for the smallest plausible Ḡ. If the bootstrap bound has a density no larger than that of a normal with this SE, the chance that one of the 6 endpoint bounds lands in a ±10⁻⁹ band is at most about 6 × 2·10⁻⁹ / (√(2π)·10⁻⁴) ≈ 5·10⁻⁵. Numerical inconclusiveness is therefore practically excluded, not near-certain. For contrast, the withdrawn v1 G bound (η/min q, with min q ≈ 10⁻²¹) would have been about 10⁹, making INCONCLUSIVE certain.

#### 15.3.14 Cost (single thread; MERGE numcert decision 9)

The oracle is canonical and model-independent: it runs on 2 donor histories per row, not 2 × 3. The three models enter only the cheap A/Y/Z float arithmetic. Certified rows: validation eligible (≈ 3,700) plus fresh eligible (≤ 5 × 4096); H3 adds 4 calibration rows. That is ≤ about 24.6k rows, ≈ 50k histories.

| Item | Cost |
|---|---|
| Operational filter (already in §17) | ≈ 1 MFLOP per history: minutes |
| C0 reference oracle (d = 5) | ≈ 7·10⁴ elementwise operations per history, vectorised over rows; ≈ 4·10⁹ in all: minutes |
| P0 exact constants (ω_TE, ε_E, τ⁺, π_min, d) and the E_canon identity | ≈ 3·10⁴ Fraction operations, once: < 1 s |
| P1 | one minimum per history: negligible |
| Measured discrepancies r_h | 36 exact Fraction quotients per history, ≈ 1.8·10⁶: about 1 min |
| M-ln | ≤ 1.8·10⁶ Decimal `ln` at 40 digits, plus Fractions: ≤ about 3 min |
| Row bounds b^G, b^A (34 pairs), b^Y, b^Z, b^Zf | vectorised numpy, about 10⁸ flops: seconds |
| Tree means | five certified bootstraps (H5 and V3 on validation and on fresh, and the fresh endpoint) × 5000 draws × ≤ 3 arrays × ≤ 20,480 additions ≈ 1.5·10⁹ elementwise: about a minute |
| OUT, B constants, rank checks, guards | negligible |
| Route F | 0.5–2 s per failing history (metered); expected 0; worst case, all ≈ 50k histories, about 7–28 CPU-h, uncapped and reported |
| **Expected total** | **< 0.1 CPU-h** |

**Alternatives considered.**
- *X's validated exponential and interval log-softmax.* Not needed once A is evaluated in logit-difference form (MERGE numcert decision 3); it would add about 2·10⁸ validated exponentials and 10⁷ scalar Decimal logarithms.
- *A validated interval filter.* Because every quantity is positive, it reduces to the projective bound of Theorem 1 applied to the C0 reference.
- *All-row Decimal (K4's pattern).* About 50k histories at roughly 1 s each, so 14 CPU-h or more. It is retained only as route F.

#### 15.3.15 Placement and records

**Placement.**
- **P0 and the A1 self-test:** at H1 (S3).
- **H3 (S3):** the C0 reference, P1, route F where needed, r_h, M-ln and b^G for the 4 Decimal reference rows of each split.
- **Validation eligible rows at S3, before H5 (gate N0, §16 row 4a):** C0, P1, route F, r_h, P4, M-ln, P2 for q̂, ℓ̂ and Ĝ, b^G and B^H.
- **At V3 (S5):** b^A_full, b^Zf and B^V3_j.
- **On fresh rows inside T-PRE (row 20):** N0, B^H and B^V3_j.
- **At NUM (row 21):** b^A for the primary and control pairs, b^Y, b^Z and B_num,j.
- **Calibration:** no certified decision; Ḡ_cal is reported only.

**Records.** Saved immutably (`save_npz` / `write_new`):
- per history: ν_min, the route flag, r_h or (r, x), ρ;
- per row: ē_ℓ, b^G, b^A_T, the mean b^A_C, b^A_full, b^Y, b^Z and b^Zf;
- per gate and model, as exact rational strings: the P0 constants (ε_E, π_min, τ⁺, d, ν₀, ω_TE), ρ̄_ref, B_num,j, B^H, B^V3_j, the ranks and rank-check counts, and the guard outcome;
- the E_canon digests, the A1 self-test record, and the numpy, Python and libmpdec versions.

#### 15.3.16 Tests (S1, Author A, synthetic fixtures only)

1. **Theorem 1 on tiny positive HMMs** (N between 4 and 12, lazy walks with sparse and dense support, all L ≤ 33). Compare the C0 reference against an exact `Fraction` filter and assert mag(q^ref : q*) ≤ ρ̄_ref(L, N, d). Verify ρ̄_ref(32, 144, 5) = 729·u′ and ρ̄_ref(32, 144, 144) = 9486·u′ exactly.
2. **Theorem 1′.** Inject perturbations into a synthetic "operational" predictive and confirm that ρ_h contains the exact error; r_h > 1/2 gives FAIL_TECHNICAL/ORACLE.
3. **Underflow and route F.** With crafted emissions near 10⁻³⁰⁰, P1 fails, route F is taken, and ρ_F bounds the exact error; x > 1/2 gives FAIL_TECHNICAL/ORACLE.
4. **Theorems 2 and 3 against exact rationals,** including q with entries of 10⁻²⁵⁰ (G must not blow up) and stored rows that are not exactly stochastic (the ω_TE term must be required and sufficient).
5. **Logit form.** The logit-difference form equals the log-softmax form exactly in rationals when Σd = 0. Equal logits give Â = 0 bitwise.
6. **M-ln.** An injected log error enlarges b^G accordingly. Decimal traps and flags give FAIL_TECHNICAL/NUMERICAL.
7. **L4, quantiles and ranks.** L4 holds; `inverted_cdf` returns an input element bitwise; at 5000 draws the ranks for 0.05, 0.05/3 and 1 − 0.05/3 are 250, 84 and 4917; the run-time rank check rejects a wrong value.
8. **Theorem 5 and the H5 wrapper.** tree_mean against exact rationals, with cancellation and subnormal inputs. The wrapper's index stream equals `bootstrap_profile`'s, and on integer-valued fixtures the means are bitwise equal.
9. **L5.** OUT(evaluated) ≥ the exact rational value on random nonnegative trees, including subnormal leaves.
10. **Guards at their boundaries.** Γ = ±g exactly, the floor binding, and exact rational comparisons for (E), (H) and (V).
11. **Constants.** δ₁ and δ₃ are exact, and up(c) ≥ c for every constant.
12. **P0, P2 and the A1 self-test.** Non-identical E_canon, non-finite or out-of-range values give the declared FAIL_TECHNICAL statuses.
13. **Kernels.** No certified kernel calls BLAS or a numpy reduction (source inspection, recorded in the S1 test report); skipping zero T entries is bitwise neutral.
14. **Coverage and order.** Every eligible row, model and pair has its bounds; fresh A/Y/Z bounds are not computed before T-PRE passes; validation endpoint-bearing bounds are sealed (§12.5).

---

## 16. Gate table (exact evaluation order; the first non-PASS stops)

**Conventions.**
- "≥", "≤", ">" and "<" are meant exactly as written.
- Gate records use `stage_records.record_gate`/`run_gate`: `errors.Invalid`/`JoinError` → FAIL_TECHNICAL; `Unresolved` → INCONCLUSIVE.
- The C1 boundary adapts `StageFailure`, `ProfileError`, and reference-input/Decimal exceptions into recorded C1 failures. `stage_records.run_gate` does not catch those exception classes unchanged. Every failure receives a gate or resource-stop record before termination.
- **Every-row checks** appear only for algebraic or numerical identities and lineage, whose failure is treated as a defect or, for lineage, as an alarm (§2.4). **Statistical gates are fraction-based.**
- Eligible rows are used unless stated otherwise.
- **Numerical certificate (v3).** Certified quantities (Ĝ, Â, Ŷ, Ẑ, Ẑ_full and their bootstrap means) are computed only by the prescribed expressions of §15.3.2, including the ordered reference oracle (C0), the ordered sums and the balanced-tree mean kernel. Certificate bounds are evaluated as §15.3.5 L5 prescribes, and every certificate comparison is made in exact rationals. Coverage is every-row: a fast-path precondition failure (P1) invokes route F and never removes a row. A valid finite certificate that fails to separate a threshold is INCONCLUSIVE; a precondition, integrity or implementation defect of the certificate (P0, P2, P3, P4, a rank-check failure) is FAIL_TECHNICAL.

| # | Stage | Gate | Criterion | Status on failure |
|---|---|---|---|---|
| 0 | pre-data | G0 CHART_BRANCH | §14: branch A or C proceeds (C only if K4 never attempted chart construction) | B, including charts attempted without a complete, accepted PASS record → INCONCLUSIVE/CHART_UNAVAILABLE; K4 not final → WAIT |
| 1 | S3 | H1 IDENTITY | World/Transition/Emission/checkpoint IDs equal the CONTRACT; `validate_process(T, E, π, 1e-12)`; perms are permutations; `canonical_emission` round trip; the three models' E_canon arrays bitwise identical (§3.3); P0 of §15.3.3 in exact rationals (ω_TE, d, ν₀ recorded); the A1 arithmetic self-test (§15.3.3) | FAIL_TECHNICAL/IDENTITY |
| 2 | S3 | H2 SEPARATION | `check_disjoint` over all C1 sequence IDs and stored ones; U_cal ∩ R_1 = ∅, U_val ∩ R_1 = ∅ and U_cal ∩ U_val = ∅ over every source/donor role combination, with registry version 1 bound by content hashes (§2.4); `check_first_token(first, πE, split)` does not raise (p ≥ 1e-4) per block | FAIL_TECHNICAL/LINEAGE |
| 3 | S3 | H3 ORACLE | symmetry ≤ 1e-14; closed form ≤ 1e-12; named = canonical ≤ 1e-12; G cross-model ≤ 1e-12 (named-order G from the permuted canonical arrays, §3.3); Decimal (§3.4; v3 aligned with §15.3): posterior and predictive componentwise \|x̂/x̃ − 1\| ≤ 2·10⁻¹² (a reference row whose history fails P1: max\|x̂ − x̃\| ≤ 2·10⁻¹²), surprisal ≤ 1e-10, \|Ĝ − G̃\| ≤ b^G_i + 10⁻³⁰ (b^G_i from §15.3.8; exact rationals) | FAIL_TECHNICAL/ORACLE (FAIL_TECHNICAL/NUMERICAL for a Decimal trap or flag, P3) |
| 4 | S3 | H4 ELIGIBILITY | f_cal ≥ 0.90 and f_val ≥ 0.90 | INCONCLUSIVE/ELIGIBILITY |
| 4a | S3 | N0 NUMERIC PRECONDITIONS (validation eligible rows; v3) | §15.3.3 and §15.3.6: the C0 reference oracle and P1 for every donor history (route F, §15.3.7, where P1 fails; this is not a failure); measured discrepancy r_h and P4; M-ln; P2 for q̂, ℓ̂ and Ĝ; b^G_i and B^H computed | FAIL_TECHNICAL/NUMERICAL (P2, P3); FAIL_TECHNICAL/ORACLE (P4: r_h > 1/2 or route-F x > 1/2) |
| 5 | S3 | H5 HEADROOM | one-sided 0.05 LB of Ḡ_val > 0.01 nat: index stream and quantile as `bootstrap_profile(..., rng=np.random.Generator(np.random.PCG64(520505)), draws=5000)` and `percentile_interval(result["B"][:, 0], [0.05])[0]` (§3.5), with the certified tree-mean wrapper (§3.5, §15.3.2 C7) and the rank check (rank 250). Signed guard §15.3.11 (H): PASS iff lower − 1/100 > max(B^H, 10⁻⁹), in exact rationals | lower − 1/100 ≤ −max(B^H, 10⁻⁹) → INCONCLUSIVE/HEADROOM; otherwise INCONCLUSIVE/NUMERICAL |
| 6 | S4 | M0 MODEL | checkpoint IDs; float32 sha; float64 round trip bitwise; identity patch bitwise and zero patch, both on 1024 cal rows | FAIL_TECHNICAL/MODEL |
| 7 | S4 | C0-cal CHART | A: NPZ sha equals the K4 record and loads. C: `fit_chart` + `fit_gauge` resolve within the construction budget | A: FAIL_TECHNICAL; C: INCONCLUSIVE/CHART_UNAVAILABLE |
| 8 | S4 | F1 FIT | FWL rank 41, cond ≤ 1e8, σ_max(B) > 0 then σ ratio ≥ 1e-6; Σ_W λ_min > 1e-12·λ_max; ℓ not None | INCONCLUSIVE/PATCH_MODEL_DEGENERATE, SUPPORT_DEGENERATE, RBF_DEGENERATE |
| 9 | S4 | M1 IDENTITIES | §6 identities ≤ 1e-10 relative, with the §6 comparison definitions (division by the positive primary norm, else exact zeros; uncentred and pooled-centred S; sorted spectra by max abs difference over the primary's max abs eigenvalue, else both matrices zero); frame orthonormality ≤ 1e-12; same frame on both arms; RidgeProbe vs `nested_ridge` ≤ 1e-10 | FAIL_TECHNICAL |
| 10 | S4 | M2-cal | §8.2, plus leakage if κ_ν ≥ 0.01 — activations and fixed decoders only; no logit read (computation-order rule, §2.2) | INCONCLUSIVE/FAMILY_UNMATCHED or NUISANCE_CONFOUNDED |
| 11 | S4 | M3-cal | §9, all four requirements | INCONCLUSIVE/SUPPORT |
| 12 | S5 | C0-val CHART | C: K4 chart_gates on the 512-row val panel (support all 512, fidelity ≥ 0.80, bins ≥ 8 each, resultant ≤ 0.30). A: no additional gate | INCONCLUSIVE/CHART_UNAVAILABLE |
| 13 | S5 | M4 ADEQUACY | accuracy ≥ 0.95; r2_pooled ≥ 0.50 | INCONCLUSIVE/DECODER_INADEQUATE |
| 14 | S5 | M2-val | as row 10 | as row 10 |
| 15 | S5 | M3-val | as row 11 | INCONCLUSIVE/SUPPORT |
| 16 | S5 | V1 | sign agreement ≥ 0.75 on rows with \|δ*\| ≥ med* | INCONCLUSIVE/CHART_NOT_REGISTERING |
| 17 | S5 | V2 | 0.5 ≤ κ ≤ 1.5 and sign agreement ≥ 0.80 on \|d\| ≥ med | INCONCLUSIVE/MANIPULATION_FAILED |
| 18 | S5 | V3 | all three LB(Z_full) at 0.05/3 (seed 520504; tree-mean kernel; rank 84), with Z_full computed by §15.3.2 C4/C6 and b^Zf_{j,i}, B^V3_j by §15.3.10–11; P2 on the donor logits and Ẑ_full. Signed guard §15.3.11 (V): PASS iff L^V3_j > max(B^V3_j, 10⁻⁹) for every j, in exact rationals. Donor logits are first retained for scientific use here (§2.2) | some L^V3_j ≤ −max(B^V3_j, 10⁻⁹) → INCONCLUSIVE/MODEL_HEADROOM; otherwise INCONCLUSIVE/NUMERICAL (FAIL_TECHNICAL/NUMERICAL for P2, P3 or a rank-check failure) |
| 19 | S5 | P1 | ladder (§12.4): some N PASS; primary and control logits are first retained for endpoint/precision use here (§2.2); tail-path identity ≤ 1e-12; identity patch bitwise. The ladder is operational, not certified (§15.3.1): `precision.py`'s arithmetic is used as computed, and a numerical perturbation can change only the test size | INCONCLUSIVE/UNDERPOWERED (FAIL_TECHNICAL for identity) |
| — | S6 | ACCEPT | coordinator's independent review of the gate report (sealed means unopened); release R3 names N_test and k | not accepted → stop |
| 20 | S7 | T-PRE | all computed before any fresh A/Y/Z, apart from the declared target-free identity checks (§2.2): H1, H2 (U_test ∩ R_2 = ∅ over every source/donor role combination, registry version 2, §2.4), H3 on test rows; N0 (row 4a) on test eligible rows; \|f_test − f_val\| ≤ 0.02 and f_test ≥ f_val − 0.02 (so n_test ≥ N_test); H5 on test with seed 520506 and the §15.3.11 (H) guard; M0 (identity patch on every eligible row), M1, M2 (with leakage), M3, M4, V1, V2, V3 with seed 520507 and the §15.3.11 (V) guard, tail-path identity — same tolerances. Fresh primary/control A/Y/Z and their bounds are not evaluated before T-PRE passes | INCONCLUSIVE/TEST_GATE: endpoint not scored, arrays sealed and kept (FAIL_TECHNICAL for identity or lineage; INCONCLUSIVE/NUMERICAL for an H5 or V3 guard-band hit; FAIL_TECHNICAL/NUMERICAL or /ORACLE for P2, P3, P4 or a rank-check failure) |
| 21 | S7 | NUM | §15.3 (proof attached; independent review before freeze): P2 on all certified arrays; b^A, b^Y and b^Z_{j,i} for every test eligible row; B_num,j = OUT(max_i b̂^Z_{j,i}) + γ_{d_n+1}·max_i\|Ẑ_{j,i}\| + ζ (§15.3.11); rank checks (ranks 84 and 4917); per model \|L_j\| > max(B_num,j, 10⁻⁹) and \|U_j\| > max(B_num,j, 10⁻⁹), in exact rationals | INCONCLUSIVE/NUMERICAL (FAIL_TECHNICAL/NUMERICAL for P2, P3 or a rank-check failure) |
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
- Chart lift (branch C): the inherited K4 lift CPU cap is removed by the explicit owner resource override of §14 (`lift_cpu_cap_s` JSON `null` → +∞; `native_operation_wall_s` 600; external operation guard 600 s). Rebinding the meter alone would not remove it.

**Cost basis.**
- About 54 MFLOP per full forward row.
- Batches of 1024 rows; peak RAM < 4 GiB.
- About 7,400 eligible calibration rows × 64 control states per model are decoded on calibration, and about 3,700 × 64 on validation.

| Stage | Content | CPU forecast |
|---|---|---|
| S0 Written contract | This document → result-blind independent review (Codex first) → corrections (v2) → reviewer confirmation; the §15.3 certificate merged with its proof (v3) → independent review of §15.3 and resolution of the §23.6 open items → freeze with C1 `PROTOCOL.md`, `CONTRACT.json` (uncapped CPU and `lift_cpu_cap_s` written as JSON `null`; `native_operation_wall_s` 600), `API.md`, `TEST_PLAN.md`; freeze sha recorded in the decision log | documents only |
| S1 Independent tests | Two authors work from API.md before any implementation, on synthetic fixtures only (see the list below) | ≤ 0.25 h |
| S2 Implementation | Separate builder, new worktree from the accepted head; reuse and bindings per §18 (including `meter.WORKER_SESSION`/RUN.lock identity, the extracted disk/limiter helpers with provenance and regression checks, the `env_identity` import order, the C1 PREREQUISITE and PASS-gate-set checks, and exception adaptation at the C1 boundary); ≤ 2 correction jobs per defect; the full existing suite and the K4 chart/precision tests must pass unchanged | ≤ 0.25 h of tests |
| — | **Wait for K4's chart outcome (G0)** | — |
| S3 Oracle only (release R1) | Registry v1; sample cal and val (12,288 rows); H1–H5 with N0 (row 4a: C0 reference oracle, P1, route F where needed, measured discrepancies, M-ln, b^G, B^H); s_max; κ_ν | 0.05–0.25 h |
| S4 Calibration (R2) | Forward passes for S and D± (8192 × 3 × 3 models, activations only); chart (A: load; C: construct ≤ 0.5 h); FWL; Σ_W; decoders (LOPO, 3 targets × 3 models); frames; M0–M3 | 0.4–1.0 h (+ ≤ 0.5 h for branch C) |
| S5 Validation (R2 continued) | Rows 12–19 in order: full passes for S, D±, T± (4096 × 5 × 3); tail path for 64 control states per row; chart extension and decoding of about 240k states per model; bootstraps (tree-mean kernel; V3 certificate b^Zf, B^V3); P1; gate report; sealed means | 0.3–1.0 h |
| S6 Coordinator ACCEPT | Independent review; registry v2; release R3 (N_test, k) | — |
| S7 Fresh test (R3) | Sample k blocks; row 20 (including N0 and the H5/V3 certificates on test rows); endpoint; certificate (row 21); decision; immutable exports | 0.3–1.7 h (k = 2 → 5) |
| S8 Report | Report, review, decision record, morning report (Hebrew) | ≤ 0.1 h |

**S1 test lists.**
- **Author A:**
  - donor transform and symmetry on a tiny periodic HMM;
  - closed-form donor posterior;
  - eligibility with an `inverted_cdf` boundary;
  - the A identities (A = G at p = q; exact cancellation of arm-common additive terms; A scales by β under a common temperature; A = 0 for equal arms);
  - the ratio-to-mean reduction θ > c ⇔ E[Y − cG] > 0 (§12.2) and the decision boundaries (equality → INC);
  - bootstrap index order, shared across models;
  - ladder logic, including the k formula;
  - the numerical certificate (§15.3.16 items 1–14, synthetic fixtures only);
  - named/canonical joins.
- **Author B:**
  - FWL recovery of a known B in a noiseless synthetic case, plus a trap showing that sequential residualisation is wrong;
  - Haar and primary-QR sign conventions (positive diagonal), isometry and isospectral identities with the §6 zero-norm and zero-spectrum rules, pair mapping;
  - D_w, D_y, leakage and D_M with q99 `inverted_cdf`;
  - V1/V2 wrap at ±π, sign(0) and median ties;
  - gate order (computation-order rule, §2.2: no logit read before M2/M3 pass on calibration apart from the declared identity/zero-patch checks; donor logits first retained at V3, primary and control logits at P1; fresh A/Y/Z never evaluated when row 20 fails);
  - RidgeProbe/`nested_ridge` equivalence;
  - `stage_records` prerequisite rebinding.

**Total forecast.** Expected 2–6 CPU-h including overhead, tests and the branch-C fallback (MERGE ruling 8). This is a forecast, not a cap. The coordinator may refine it from metered stage timings, but may not change sample counts, methods or stop rules. The numerical certificate (§15.3.14) adds an expected < 0.1 CPU-h inside this forecast; route F, if ever taken, is uncapped, metered and reported separately.

---

## 18. Six-field reuse assessment (charter; every reused function verified at 4f219d6)

| Field | C1 |
|---|---|
| **1. Existing functions reused unchanged** | See the grouped list below the table. |
| **2. Not reused, or not reusable unchanged (verified)** | See the second list below the table. |
| **3. Missing capability** | (1) Donor transform with w32 kept, the symmetry and closed-form checks, eligibility, κ_ν, G. (2) The FWL map and forced states. (3) Haar frames and the control family. (4) Kernels for damage, leakage, D_M support, V1–V3. (5) The crossed contrast (logit-difference form), Z, the bootstrap decision, the ladder k rule, and the certificate of §15.3: the ordered float64 reference oracle (C0), P0–P4, the exact measured discrepancies, route F (a provenance-recorded replica of the 8-line `error_bound._reference_posterior` wrapper plus the Decimal predictive), M-ln, the ordered sums and row bounds, OUT, the balanced-tree mean kernel and the H5 index-loop wrapper `c1_bootstrap_means`, the rank checks and the signed guards. (6) The exposure registry builder and C1 history tables. (7) The Decimal predictive/log helper (also step 2 of route F). (8) The C1 stage driver and bindings: `c1_meter_bind` (including the `meter.WORKER_SESSION` binding and the extracted disk/limiter helpers), C1 release, `stage_records` PREREQUISITE rebinding with the C1 PASS-gate-set checks, `env_identity` imports rebinding, exception adaptation at the C1 boundary, and one ledger initialisation in the existing schema `x4-oracle-profile-ledger-v1` (the meter requires the ledger to exist). |
| **4. Smallest change** | One new package, `tools/c1_state_forcing/`. It contains pure kernels (arrays, configuration and an injected guard/timer in; no hidden I/O or randomness) plus thin bindings and a driver, roughly 900–1,200 lines plus tests. Frozen K4 and job-0014 files are never edited. Nothing new goes into `src/`. |
| **5. Stable interfaces and invariants** | See the third list below the table. |
| **6. Regression checks and next extension** | **Regression:** the existing learner, analysis and oracle-profile suites and the K4 chart/precision tests pass unchanged; the S1 independent tests come first; on real data, the tail path vs `forward_with_patch` and RidgeProbe vs `nested_ridge` equivalences are checked; guard fault tests cover every rebinding (STOP, disk, uncapped ledger, 12 GiB job object, WORKER_SESSION/RUN.lock identity, uncapped lift); the certificate tests of §15.3.16 pass, including the exact-rational small-HMM checks of the reference oracle and the injected-discrepancy checks. **Next extension:** the same kernels can serve one separately reviewed follow-up without new abstractions, for example a w31-retaining donor (shifting w1..w30) to separate short from long history, or an earlier site if a certified chart exists there. No generic causal or topology framework. |

**Field 1, existing functions reused unchanged (signature → use):**
- **Process and data:**
  - `dataset.sampler.HMMSampler(T, E, π, layout).sample(n, rng)` → (tokens [n, 33], states), emitting first; w33 and the states are dropped;
  - `dataset.checks.process_code(family, mode, sigma, replicate)`, `make_sequence_ids(code, split ∈ {train, dev, test}, n)`, `check_disjoint(**splits)`, `check_first_token(first, p_w, split)`;
  - `contracts.SeedTree(master).generator(name, *scope)` with `.issued`.
- **Oracle:**
  - `oracle.BayesFilter(T, E, π).run(tokens)` → b, q, log_evidence, ce (§3.3);
  - `tools/x4_oracle_profile/oracle_profile.py`: `validate_process(T, E, π, tol)`, `canonical_emission(E_named, perm)`, `circle_features(coords)`, `posterior_means`/`suffix_posterior` (K = 32 equals the full-prefix filter for 32-token histories), `bootstrap_profile(norm, sq, Ks, rng, draws)` (returns a dict {"B", "V"}; `rng` must be a `numpy.random.Generator`, §3.5), `percentile_interval(samples, probs)` (inverted_cdf; at numpy 2.2.6 an input element at a rank depending only on (n, p), §15.3.2 C7). For the certified H5 the index semantics of `bootstrap_profile` are kept and its `np.mean` is replaced by the tree-mean kernel through a C1 wrapper (§3.5);
  - `tests/oracle_profile/independent_reference.decimal_suffix_posterior(T, E, π, suffix, digits ≥ 60)` (§3.4, and route F of §15.3.7);
  - `tools/x4_circle_history/error_bound.trapping_context(prec)` (H3, M-ln at 40 digits, route F at 60 digits), `u_digits(n)`, `gamma_digits(k, n)` and `posterior_envelope(L, S)` (route F: β = `posterior_envelope(32, 144)`, γ^(60)_{2N+2}). Importing `error_bound` inserts `tests/oracle_profile` into sys.path, imports K4's `errors` and verifies its Taylor constants exactly; these effects are recorded.
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
  - it passes `--max-cpu inf --max-wall inf` and installs a limiter with the owner disk safe-STOP and the op-marker deadline, using the disk/limiter helpers extracted into the C1 binding (below);
  - the native-operation deadline is 600 s wall per marked operation (one 1024-row batch, one solve, one chart construction);
  - `c1_meter_bind` additionally binds `meter.WORKER_SESSION` to the authorized executing worker session. The same identity must own RUN.lock; `--lock-owner` alone does not override the run-mode identity check.
  - C1 does not import `meter_bind` as an allegedly side-effect-free helper module. That import reads the K4 CONTRACT, changes import paths, imports the K4 release module, and captures `_LEGACY_LIMIT`. The small disk/limiter helpers are extracted into the C1 binding, with provenance and regression checks, while frozen K4 files remain unchanged.
- `cochain.integer_lift`: it independently enforces `cfg["lift_cpu_cap_s"]` (30 s in the K4 CONTRACT); rebinding the meter does not remove it. **Fix:** the explicit owner resource override of §14 (`lift_cpu_cap_s` JSON `null`, decoded to +∞; `native_operation_wall_s` 600); `cochain.py` itself is reused unchanged.
- `release.verify`: its schema, issuer `"codex-coordinator"`, K4 STAGES and K4 CONTRACT are all K4-specific. **Fix:** a separately versioned C1 release module with the same checks and the current coordinator as issuer.
- `stage_records.PREREQUISITE`: it is K4's chain. **Fix:** Use `stage_records.PREREQUISITE = {"oracle": None, "calibration": "oracle", "validation": "calibration", "fresh": "validation"}`. The C1 driver separately verifies the expected PASS-gate set for each prerequisite stage: the reused helper checks evidence and absence of recorded failures, but does not know C1’s required gate names. `begin()` then enforces no retry, no non-PASS gate earlier, and unchanged evidence from the prior stage. Its K4-named branches are inert for C1 names (the K4 `"oracle"` branch of `_check_prerequisite` is never reached, because C1's `"oracle"` has prerequisite `None`). The C1 driver adds the release and ACCEPT checks.
- `stage_records.run_gate` exception coverage: it catches only `Invalid`/`JoinError` and `Unresolved`. **Fix:** The C1 boundary adapts `StageFailure`, `ProfileError`, and reference-input/Decimal exceptions into recorded C1 failures. `stage_records.run_gate` does not catch those exception classes unchanged. Every failure receives a gate or resource-stop record before termination.
- `env_identity.SCIENTIFIC_IMPORTS`: it lacks torch and the C1 modules. **Fix:** Rebind `env_identity.SCIENTIFIC_IMPORTS`, call `env_identity.import_scientific()`, then call `record()`. `record()` itself does not consult SCIENTIFIC_IMPORTS.
- X4-F's `random_family`, `x4f_damage`, `x4f_gates` and orchestration: they carry dormant defects (X4-F addendum §3).
- **Certificate (v3).**
  - `error_bound._reference_posterior` is a private name. **Fix:** C1 replicates its 8-line wrapper (60-digit trapping context, `decimal_suffix_posterior`, watched-flag check) with provenance, rather than importing it (§23.6).
  - `error_bound.certify_rows`, `reference_moments`, `row_bound` and the cos/sin Taylor machinery certify K4's circular moments M_32 − M_4, a different target. Not reused.
  - `process_law.py`: C1's oracle is operational (§3.3), so the documented-law deviation is not part of any C1 claim and is not added to B_num.
  - `bootstrap_profile`'s `np.mean` and `BayesFilter`'s BLAS products are not on the certified path: their accuracy is not assumed. The operational filter enters only through the measured discrepancy against the ordered reference (§15.3.6), and the certified means use the tree kernel (§3.5, §15.3.2 C7).
  - K4 deliberately made no float64 error model. C1 differs on purpose: a proved float64 model (A1, elementwise IEEE operations only) of a reference whose every summation order C1 specifies makes an all-row certificate proportionate (< 0.1 CPU-h instead of 14 CPU-h or more). Route F keeps K4's assumption-free profile for any history the reference does not cover.

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
9. Validation means, and every validation endpoint-bearing secondary statistic (§12.5), stay sealed until the fresh result is recorded. After fresh exposure, a repair cannot change the method or bring in replacement data.

---

## 20. Parameters for the reviewer to scrutinise (all fixed; changes only before any C1 data)

1. The margin c = 0.10, the planning alternative 0.20, the positive-control threshold 0.30, power 0.80, and α = 0.05/3 per tail (MERGE ruling 3).
2. The donor step of ±1 column (2 cells) with w32 kept; eligibility at the calibration q0.999 of the natural surprisal, with coverage ≥ 0.90.
3. The FWL covariates (ȳ, Var y, ‖m32‖) and the degeneracy bounds (cond ≤ 1e8, σ_max(B) > 0, σ ratio ≥ 1e-6, which the analyst judged nearly vacuous: L-8).
4. Whitened (within-class LW, phase term retained) versus raw metric for the isometry.
5. Whether a near-placebo Haar family satisfies owner B3-C. The coordinator ruled yes (ruling 1). The independent review accepted ruling 1 under the explicit operational interpretation stated in §6 (review required change 3).
6. 32 frames and the ≥ 28/32 dispersion rule.
7. Damage tolerances 0.02 / 0.05 / 0.01 / 0.02; leakage 0.25 with the κ_ν trigger 0.01; leakage applied on calibration as well.
8. Support: q99, max(0.05, F(D) + 0.02), 0.02, and K4 support fractions 0.99 / 0.98.
9. V1 0.75 on rows at or above the median |δ*|; V2 κ ∈ [0.5, 1.5] and 0.80.
10. Decoder adequacy 0.95 / 0.50; the λ grid (1e-3 … 10); 2048 features; median bandwidth.
11. Headroom: Ḡ lower bound > 0.01 nat.
12. The ladder grid {4096, 8192, 16384} on eligible rows, the k formula with the 0.02 slack, and the use of all eligible rows in the k blocks.
13. The FAIL-all versus FAIL-any asymmetry (MERGE ruling 2).
14. Symmetry tolerance 1e-14 (changed from L's 1e-15). The numerical certificate (§15.3; proof attached in v3, independent review before freeze):
    - **Oracle.** An ordered float64 reference oracle with every summation order fixed in C1 source and no BLAS, with a proved componentwise bound ρ̄_ref = [2(L−1)(d+2) + 2 + 2N + d]·u′ (log-ratio, every symbol; 729·u′ ≈ 8.09·10⁻¹⁴ for d = 5), under the per-history precondition P1 (no reference posterior entry below ν₀ ≈ 10⁻²⁸¹). The operational `BayesFilter` predictive is compared with it on every certified history: ρ = ρ̄_ref + r/(1−r), with r the exact measured relative discrepancy (r ≤ 1/2 required). A history failing P1 is certified by K4's 60-digit Decimal enclosure (route F).
    - **Logs and A.** `np.log` errors are measured against correctly rounded 40-digit Decimal `ln`. A is evaluated in logit-difference form, with the proved normaliser residual ω_TE·‖Δz‖∞, so no log-softmax or exponential enters the certified path.
    - **Bounds.** Per-row b^A, b^G, b^Y, b^Z and b^Zf from ordered kernels. r^mean_j = γ_{d_n+1}·max|Ẑ| + ζ for the prescribed balanced-tree mean kernel, and B_num,j = OUT(max_i b^Z_{j,i}) + r^mean_j, with outward inflation OUT(x) = (1 + 2⁻³⁰)·x + 2⁻⁸⁰⁰.
    - **Guards.** Signed guards for the endpoint, H5 and V3, compared in exact rationals.
    - **Constants.** η = 1e-12 and 2⁻⁴⁴ are withdrawn, not retained. The H3 Decimal tolerances are aligned with the proved bounds (componentwise 2·10⁻¹²; per-row b^G). The P2 limits 2¹⁹ and 2²¹ and the P4 limit 1/2 are fixed.
    - **Floor.** The numerical floor 1e-9 is retained as an additional conservative guard, not a proof of accuracy. It is the binding guard: the projected B_num,j is ≤ 10⁻¹⁰.
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
| 12 | L (A, Y, Z, Fieller (v2: ratio-to-mean reduction, §12.2), `precision.py`) + A (ruling 4 wording; its θ = 1 clause superseded in v2, §1.3) + W (verified `precision_summary` semantics; k rule) | C-1, C-5 |
| 13 | L + X (validity precedence; "all-three not supported" sentence) | — |
| 14 | L (three-way rule) + A (ruling 7) + W (landmark id strings; 512-panel gates) | C-4, C-15 |
| 15 | L (float64, bitwise identity, Decimal on 4 rows) + X (logits as operational output) + W (certificate constants). **v3:** §15.3 merged from certificate tracks X (ordered reference, measured discrepancy, tree-mean kernel, coverage) and L (projective proof, route F, logit-difference A, canonical Ĝ, M-ln, row bounds, OUT, guards) under MERGE numcert decisions 1–9 | C-19 |
| 16–17 | L (gate order, stages) + X (output envelope, JSON null, one thread) + A (ruling 8 CPU) | C-23, C-25, C-26, C-27 |
| 18 | L + X lists, corrected by W against the code | C-2, C-3, C-9 to C-13 |
| 19 | L ∪ X | — |
| 20 | L§15 + A§6 list + W additions | — |
| all | v2: independent review `coord-c1-merged-review-20261015.codex.md`, required changes 1–13 | §22 |
| 3, 11–13, 15–18, 20 | v3: certificate merge `coord-c1-numcert-20261015` (tracks X and L; MERGE decisions 1–9): §3.3 canonical Ĝ and shared process, §3.4 aligned tolerances, §3.5 tree-mean wrapper, §11 and §12.1 logit-difference A, §12.3 tree means and ranks, §13 step 2, §15.2, §15.3, §16 conventions and rows 1, 3, 4a, 5, 18–21, §17, §18, §20 item 14, C-19 | §23 |

**Corrections:**
- **C-1 (L-1).** "Cancels exactly every target-independent effect" was replaced by: arm-common additive log-p terms and v-constant terms cancel exactly; multiplicative effects scale A; arm-asymmetric residuals are estimated by the controls. **v2 (review RC3):** the last clause is withdrawn. A common inverse-temperature β scales A by β (attenuation only for 0 < β < 1, no general conservatism for Y), and the Haar family is an operational random-direction comparison, not an unbiased subtraction of every generic or nuisance effect (§1.2 note on E2, §12.1).
- **C-2 (L-3).** `ActivationExtractor` (float32; needs ObservationSet/HistoryIndex) was replaced by float64 `TransformerLM.forward(..., return_hooks=("resid_post_3",))`.
- **C-3 (L-4).** `support_report` (linear quantile, own LW) was replaced by an explicit D_M with `inverted_cdf`.
- **C-4 (L-5).** K4's every-row chart support applies only to the 512-row branch-C validation panel. The C1 cohort uses fractions.
- **C-5 (L-6).** The ladder counts eligible rows. The fresh block count k is derived from f_val with a 0.02 slack, and the fresh fraction gate guarantees n_test ≥ N_test.
- **C-6 (L-7).** V1 is described as the substantive gate and V2 as weak.
- **C-7 (L-8).** The degeneracy bound is kept; the partial R² is reported and listed for review.
- **C-8 (L-9).** Donor freshness is checked via X's exposure registry (sources and donors).
- **C-9 (W).** L's binding of C1 ObservationSet/HistoryIndex IDs is incompatible with dropping w33, because the ObservationSet schema requires 33 tokens. C1 history tables replace them.
- **C-10 (W).** `meter_bind.py` cannot be reused unchanged: it reads the K4 CONTRACT, applies the 3600/3480 caps and K4 stage caps, and on top of that the meter defaults to `--max-cpu 600`/`--max-wall 3600` and `winjob` to 8 GiB. A new `c1_meter_bind` replaces it. **v2 (review RC8):** `c1_meter_bind` also binds `meter.WORKER_SESSION` (same identity owns RUN.lock); `meter_bind` is not imported as a helper module (its import has side effects), and its small disk/limiter helpers are extracted with provenance and regression checks (§18).
- **C-11 (W).** `release.verify` is K4-specific (schema, issuer `codex-coordinator`, stages, CONTRACT). A C1 release module replaces it.
- **C-12 (W).** `stage_records.begin` keys on the K4 PREREQUISITE. The global is rebound. **v2 (review RC8):** to `{"oracle": None, "calibration": "oracle", "validation": "calibration", "fresh": "validation"}`; the C1 driver separately verifies each prerequisite stage's expected PASS-gate set; the C1 boundary adapts `StageFailure`, `ProfileError` and reference-input/Decimal exceptions into recorded failures (§16 conventions, §18).
- **C-13 (W).** `env_identity.SCIENTIFIC_IMPORTS` lacks torch. It is rebound. **v2 (review RC8):** rebind, call `env_identity.import_scientific()`, then `record()`; `record()` does not consult SCIENTIFIC_IMPORTS.
- **C-14 (W).** `nested_ridge` returns no weights and standardises features internally, while `RidgeProbe` neither standardises nor runs without validation arguments. The exact refit recipe is specified, and the 1e-10 equivalence is moved to calibration predictions, so decoders freeze at S4 without validation data.
- **C-15 (W).** `fit_chart` requires strictly ascending **string** landmark ids. Zero-padded sequence IDs are used.
- **C-16 (W).** Symmetry tolerance 1e-15 → 1e-14, because emission rows are `logsumexp`-normalised in a different summation order after the shift.
- **C-17 (W).** "No logits on calibration" is made precise: the forward pass returns logits by construction, and they are discarded unread. The only calibration logit comparison is the M0 identity/zero-patch check, which involves no oracle target. **v2 (review RC12):** all "no logits exist/computed" claims are replaced by the computation-order rule of §2.2 (logits may be generated internally and are discarded unread; donor logits first retained at V3, primary and control logits at P1; fresh A/Y/Z not evaluated before T-PRE passes).
- **C-18 (W).** The existing Decimal reference yields posteriors only. A small Decimal predictive/log helper runs inside `error_bound.trapping_context`.
- **C-19 (X + W).** The certificate is defined relative to the recorded float64 logits, with explicit constants. **v2 (review RC6):** the v1 certificate and its constants are withdrawn as unsupported; §15.3 is NOT_READY until a proof is attached and independently reviewed before freeze; the endpoint rule uses per-model max(B_num,j, 1e-9). **v3 (certificate merge; proof attached, §15.3, §23):**
  - an ordered float64 reference oracle (X) analysed in the projective (log-ratio oscillation) metric (L), giving the componentwise ρ̄_ref ≈ 8.09·10⁻¹⁴ for d = 5; the operational oracle certified by exact measured discrepancy against it (X), so no BLAS or library-reduction assumption is made;
  - precondition P1, with route F (K4 Decimal enclosure) where it fails;
  - measured logarithms (40-digit Decimal `ln`);
  - A in logit-difference form with the ω_TE residual; a single canonical Ĝ;
  - explicit per-row b^A, b^G, b^Y, b^Z and b^Zf from ordered kernels; r^mean = γ_{d_n+1}·max|Ẑ| + ζ for the balanced-tree mean kernel (X); B_num,j = OUT(max_i b^Z_{j,i}) + r^mean_j;
  - the order-statistic lemma with a run-time rank check; signed guards for the endpoint, H5 and V3; exact rational comparisons.

  The certificate is relative to the recorded float64 logits and the stored process weights. It certifies the decisions (E), (H) and (V), not the operational definitions listed in §15.3.1. Neither η nor 2⁻⁴⁴ is retained. Not adopted: L's BLAS/reduction tree assumption (A2) and γ_n mean bound; X's validated exponential and interval log-softmax, and X's interval-difference row bounds for A/G/Y/Z (superseded by the logit-difference form and L's forward bounds; MERGE numcert decisions 2, 3 and 7).
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

---

## 22. Review changes applied (v1→v2)

**Review.** `planning/responses/coord-c1-merged-review-20261015.codex.md` (sha256 2894E60410FD3C808059ABC7ABF71DA0A0DA3774D58FDF7971226BC144E6AB17), verdict APPROVE_WITH_REQUIRED_CHANGES, against `C1-MERGED-v1.md` (sha256 72C86FFC0C76386EBD1FF6D991D0AB2DE62684FB2334831628A9D3DCCB0745D7). All 13 required changes are applied. The reviewer's replacement text and values are used verbatim, including its LaTeX notation; only the review's Markdown block-quote markers were dropped. None of the optional suggestions is applied (flag F10).

### 22.1 Required changes

| RC | Sections touched | What changed |
|---|---|---|
| 1 | §3.5; §16 rows 5, 20; §18 field 1 | The H5 call now uses `rng=np.random.Generator(np.random.PCG64(seed))`. It takes `lower = float(oracle_profile.percentile_interval(result["B"][:, 0], [0.05])[0])` from the returned dictionary (verbatim code block). Seed 520505 is used for validation and 520506 for fresh; `lower > 0.01` is retained. |
| 2 | Header (Authority: erratum to MERGE ruling 4); §1.3 (new "Oracle-perfect anchor"); §8.3; §12.1; §21 row 12 | "θ_j = 1 means that the phase-only move reproduces …" is replaced by the reviewer's anchor text. If the primary arms reproduce q±, A_T = G pointwise and θ = 1 − E[Ā_C]/E[G]. θ_T = 1, and θ = 1 only when E[Ā_C] = 0. An oracle-perfect full-donor readout gives θ_full = 1. The ratios are discrimination indices, not proportions in [0, 1]. "it caps θ below 1" (§8.3) is replaced verbatim. MERGE.md is not edited (flag F1). |
| 3 | §1.2 (E2 cell and a new note on E2); §1.3 specificity statement; §6 raw-norm and Owner B3-C paragraphs; §12.1; §21 C-1 | Three v1 claims are removed: "residual estimated by the controls", "conservative" and "subtracts only second-order generic effects". In their place come the reviewer's three paragraphs and the second-order sentence. The paragraphs say that cancellation is exact only in exact arithmetic, that Haar averaging removes only the linear Taylor term, and that raw-norm ratios affect both mean and variance. The reviewer's operational interpretation of B3-C is added to §6 (and to §20 item 5). |
| 4 | §1.1; §1.2 E3; §1.4 PASS and FAIL; §5.2; §7; §8.3 | "Phase-only move(s)" becomes "chart-phase-directed move(s) along the fitted B map" (§1.4 FAIL, §8.3; RC2 removed the §1.3 instance). Five passages are replaced verbatim: the PASS conclusion, the E3 characterisation, the ‖m32‖ sentence, the §7 invertibility rationale and the §1.1 null-direction argument. The E3 text is also added under the leakage rule in §8.3. |
| 5 | §5.2 (z̃ bullet, F1 bullets, identifiability paragraph); §6 (primary QR); §14 (gauge paragraph); §16 row 8; §20 item 3 | The identifiability paragraph is inserted verbatim: M_C, B̂ᵀ = (FᵀM_CF)⁻¹FᵀM_CA, and identification through full rank of [C, F]. Constant nuisance columns use scale 1. F1 requires σ_max(B) > 0 before the ratio. The gauge sentence is replaced verbatim. The primary QR uses the positive-diagonal convention, and a rank-deficient input is never redrawn (flag F3). |
| 6 | §15.3 (replaced); §13 step 2; §15.2; §16 row 21; §20 item 14; §21 C-19; header; §3.5 and §11 (guards) | §15.3 is replaced verbatim. Its status is NOT_READY. It sets the proof requirements and refuses η = 1e-12 and 2^-44 without a derivation. Bounds are rounded outward, and B_num,j = max_i b^Z_{j,i} + r^mean_j. The endpoint rule uses `max(B_num,j, 1e-9)` per model, with signed guards for headroom and V3. The reviewer's input-perturbation bound and log-error requirement are included as guidance, together with "Do not freeze with this item unresolved." The v1 certificate is withdrawn (flag F2). |
| 7 | §6 (M1 identities and new comparison definitions); §16 row 9; §17 Author B | The reviewer's definitions are inserted verbatim. A zero primary norm requires exact zeros. S is uncentred (Σccᵀ) or centred about the pooled mean over eligible rows and both arms. Sorted spectra are compared by the max abs difference over the primary's max abs eigenvalue; if that is zero, both matrices must be zero. The 1e-10 and 1e-12 thresholds are retained, and so is the scope sentence on whitened displacement covariance. |
| 8 | §16 conventions; §17 S2; §18 fields 2, 3 and 6; §21 C-10, C-12, C-13 | The binding text is added verbatim. `meter.WORKER_SESSION` is bound to the authorised session, which must own RUN.lock. `meter_bind` is not imported; its helpers are extracted with provenance. The order is rebind → `import_scientific()` → `record()`. The exact C1 `PREREQUISITE` dict is used, with separate PASS-gate-set checks. `StageFailure`, `ProfileError` and reference-input/Decimal exceptions are adapted. The v1 clause "`meter_bind.disk_reason` and `make_stage_limiter` may be imported as pure helpers" is removed. |
| 9 | §14 (method heading, new resource-override paragraph, Branches A, B and C); §16 row 0; §17 resources and S0; §18 field 2 | The resource override is added verbatim. `lift_cpu_cap_s` is JSON `null` (→ +∞), `native_operation_wall_s` is 600 and the external guard is 600 s. All other lift and construction limits are unchanged, and K4 files are not edited. Branch B now covers charts that were attempted without a complete, accepted PASS record. Branch C applies only if K4 never attempted chart construction. Branch A binds the coordinator acceptance record. The configuration is described as "identical apart from the explicit owner resource override". |
| 10 | §2.4; §16 rows 2 and 20 | The requirement is replaced verbatim by the U_s definitions. U_cal ∩ R_1, U_val ∩ R_1 and U_cal ∩ U_val must be empty, and so must U_test ∩ R_2, over all role combinations. Manifests bind content hashes, not filename listings. A collision is a lineage alarm and does not prove a seed defect. The source classes are relabelled (a)–(d) (flag F4). |
| 11 | §12.2 (replaced, retitled); §13 (step 4 wording, new "Nominal inference" paragraphs); §1.4 (MIXED, item 10); §17 Author A; §21 row 12 | The ratio-to-mean reduction θ > c ⇔ E[Y − cG] > 0 is stated as exact algebra. The bootstrap is a percentile test, not Fieller's construction, and H5 is empirical evidence, not a guarantee. Nominal levels, conditional coverage and the per-direction union bound are added verbatim. The all-PASS/all-FAIL/MIXED rule is retained. |
| 12 | §2.2 (calibration cell, new computation-order rule, eligible-only exceptions); §5.1; §6; §12.5; §14 Branch C; §16 rows 10, 18, 19, 20; §17 Author B; §19 item 9; §21 C-17 | Every "no logits exist/computed" or "computed here for the first time" claim is replaced by the verbatim computation-order rule. The sealing of every validation endpoint-bearing secondary statistic is added verbatim (§12.5). §2.2 also gains, verbatim: all production fits use calibration; the direct validation chart is a comparator only; and the explicit exceptions to eligible-only evaluation. |
| 13 | §11 | "the model itself does not discriminate the two counterfactuals, so no phase test can be read" is replaced verbatim by the reviewer's text, ending "The phase assay stops as specified." |

### 22.2 Consistency edits beyond the reviewer's listed locations (flagged; each follows from the RC named)

- §1.3: the estimand is also conditional on the gauge and the primary QR basis (RC5).
- §1.4:
  - PASS bullet 1 reads "a chart-phase-directed move along the fitted B map" instead of "forcing the learned PH-chart phase" (RC4).
  - The FAIL sentence on V3 becomes a nominal-level lower-bound statement instead of "the models do discriminate (θ_full > 0.30)" (RC11, RC13).
  - No-licence items 9 and 10 add the family's non-subtraction and the nominal coverage (RC3, RC11).
- §5.2: "B is identified only from within-symbol … covariation" now reads "estimated only from", because identification rests on F1's rank condition (RC5).
- §6 and §20 item 5: the reviewer's B3-C acceptance under the operational interpretation is recorded (RC3).
- §8.3: the E3 sentence is repeated under the leakage rule (RC4).
- §12.1: the anchor is restated next to θ_j, with Y = A_T − Ā_C (RC2).
- §12.2: the heading changes from "Fieller equivalence" to "Ratio-to-mean reduction"; the §17 Author A test item and the §21 row 12 note follow (RC11).
- §12.5 and §19 item 9: the secondary list and the stop rule refer to the extended sealing (RC12). §14 Branch C: the direct chart is marked as a comparator only (RC12).
- §15.2: the reference rows are labelled implementation checks (RC6). §3.5 and §11 cite the signed numerical guards of §15.3 (RC6).
- §16 conventions: an every-row lineage failure is "a defect or, for lineage, an alarm" (RC10).
- Restatements of RC1 and RC5–RC12 wherever v1 repeated the old claim:
  - §16 rows 0, 2, 5, 8, 9, 10, 18, 19, 20 and 21;
  - §17 resources, S0, S2 and the Author B items;
  - §18 fields 1, 3 and 6;
  - §20 items 3 and 14;
  - §21 annotations on C-1, C-10, C-12, C-13, C-17 and C-19, plus a new changelog row.
- Header: status, identity, sources, the MERGE ruling 4 erratum and the freeze blocker (RC2, RC6).

### 22.3 Flags

- **F1 (RC2, MERGE ruling 4).** The reviewer requires the correction to "also appear in the merge ruling and associated explanatory text". MERGE.md is outside this edit's write scope and is unchanged, so two passages there still carry the old claim:
  - ruling 4: "so an oracle-perfect readout gives θ = 1";
  - lesson 4: "crossed ± donors that anchor θ = 1".

  v2 records the erratum in its header and §1.3. **The coordinator must add the erratum to MERGE.md (or an addendum) before freeze.**
- **F2 (RC6, freeze blocker).** RC6 is applied as text, but the certificate itself does not yet exist. §15.3 is NOT_READY. **Reviewer confirmation of v2 is not enough for freeze: the certificate proof must first be attached and independently reviewed** (review: "Do not freeze with this item unresolved"). **v3:** the proof is attached (§15.3; merge record §23). Its independent review is still required before freeze.
- **F3 (RC5, degeneracy mapping).** The reviewer writes "the appropriate degeneracy failure" without naming it. The editor specified the following mapping for the reviewer to confirm:
  - **W B:** rank deficiency is already excluded by F1 (INCONCLUSIVE/PATCH_MODEL_DEGENERATE), because W is invertible after the Σ_W check.
  - **Frame draw G_r:** a zero diagonal entry of R_r makes `sign` return 0, and the frame then fails the M1 orthonormality identity (FAIL_TECHNICAL).

  Code-level note: Householder QR (`numpy.linalg.qr`) returns an orthonormal U even for a nearly rank-deficient input. Only an exactly zero diagonal entry breaks the frame.
- **F4 (RC10, notation).** The review uses \(R_1\), \(R_2\) for registry versions. That collided with v1's source labels (R1)–(R4) and with releases R1–R3. The source classes are relabelled (a)–(d), the releases keep R1–R3, and §2.4 gains a one-line notation note.
- **F5 (RC9, code note, not a reviewer error).** `cochain.integer_lift` evaluates `float(cfg["lift_cpu_cap_s"])` at entry, and `float(None)` raises. The C1 loader must therefore decode JSON `null` to `float("inf")` before the cfg reaches `cochain`, as the review's "decoded to positive infinity" already says. Each solver call's limit is then min(+∞ − elapsed, 600) = 600 s. The 600 s is a C1-contract value: the K4 CONTRACT sets `native_operation_wall_s` to 180, and `cochain`'s fallback default is also 180.
- **F6 (RC8, open point).** The review requires `StageFailure`, `ProfileError` and reference-input/Decimal exceptions to be adapted into recorded C1 failures, but it does not name their statuses (FAIL_TECHNICAL or INCONCLUSIVE). v2 does not invent a mapping. It must be fixed in API.md at freeze or confirmed by the reviewer.
- **F7 (RC4, retained scope).** v1's scope sentence follows the verbatim PASS conclusion as "This holds for this counterfactual family, on the prespecified eligible population, conditional on the declared gates." It narrows the claim and adds no new content.
- **F8 (RC3, placement).** The E2 replacement is several paragraphs long, so it sits as a note directly below the §1.2 table, and the E2 cell carries a one-line summary that points to it. The same verbatim paragraphs also replace the §12.1 assertion. In §1.3, bullet 2 is replaced verbatim and the Haar paragraph follows the bullets.
- **F9.** No reviewer instruction was found to be wrong against the code (§22.4).
- **F10 (optional suggestions not applied).** The following are unchanged:
  - the §20 values;
  - the RidgeProbe/`nested_ridge` tolerance of 1e-10;
  - the pooling of Sup(T), Sup(C̄) and Sup(D±), which is not redefined;
  - the 1e-9 floor, which the required RC6 text also keeps;
  - the §16 note "binomial SD ≈ 0.004".

### 22.4 Code facts cited by the review, re-verified at main 4f219d6 (read-only)

| Review claim | Verified at |
|---|---|
| `bootstrap_profile(..., rng: np.random.Generator, ...)` returns `{"B": B, "V": V}` and uses `rng.integers`, which a bare `PCG64` lacks; `percentile_interval` uses `inverted_cdf` | `tools/x4_oracle_profile/oracle_profile.py` 194–224 |
| The unembedding is `nn.Linear(d_model, vocab_out, bias=False)` after `ln_final` (128 → 36, so rank ≤ 35 after the softmax shift) | `src/topo_pilot/learner/model.py` 92–93, 123–126 |
| `meter.WORKER_SESSION` exists; run mode requires owner == WORKER_SESSION even with `--lock-owner`; the defaults are `--max-cpu 600` and `--max-wall 3600`; `CAP_S, STOP_NEW_S = 3600, 3480` | `tools/x4_oracle_profile/meter.py` 55–56, 243–245, 259–261 |
| Importing `meter_bind` inserts sys.path entries, imports `release`, reads the K4 CONTRACT and captures `_LEGACY_LIMIT = meter.limit_reason`; `bind()` does not set WORKER_SESSION | `tools/x4_circle_history/meter_bind.py` 38–66 |
| `import_scientific()` iterates SCIENTIFIC_IMPORTS at call time; `record()` uses `loaded_distributions` over `sys.modules` and never reads SCIENTIFIC_IMPORTS | `tools/x4_circle_history/env_identity.py` 89–92, 116–126, 162 |
| `PREREQUISITE` is K4's dict; `run_gate` catches only `(Invalid, JoinError)` and `Unresolved`; `begin`/`_check_prerequisite` check evidence and recorded non-PASS gates, and their gate-name checks are K4-specific | `tools/x4_circle_history/stage_records.py` 20, 70–79, 96–136 |
| `StageFailure` and `ProfileError` exist and fall outside `run_gate`'s handlers | `src/topo_pilot/contracts/errors.py` 54; `oracle_profile.py` 24 |
| `integer_lift` enforces `float(cfg["lift_cpu_cap_s"])`. The K4 CONTRACT has `lift_cpu_cap_s` 30, `lift_node_limit` 128, `lift_rounding_tol` 1e-7, `lift_bounds` [1, 2, 4, 8, 16], `max_chart_constructions` 6 and `native_operation_wall_s` 180. `chart.py`/`cochain.py` have no other time cap | `tools/x4_circle_history/cochain.py` 140–200; `CONTRACT.json` 123–138, 237 |

---

## 23. Certificate merge (v2→v3)

### 23.1 Inputs and procedure

| Input | sha256 |
|---|---|
| `C1-MERGED-v2.md` (base) | F9F679DC0DFF74D7765B7A3E2AB0B5CB98ADE6DC73707EE367D0BC01257E12F6 |
| `coord-c1-numcert-20261015.MERGE.md` (binding decisions 1–9) | 6215A4B9FB30E4B95AD1551CBBF3F4E26BDDD530A5A6C2447DACA1C1E3723DCA |
| `coord-c1-numcert-20261015.codex.md` (track X) | 6D3305093CFA53FCE4F39FC2CB941FB2C5074B28F64F970731C20E5EBBEB7714 |
| `coord-c1-numcert-20261015.claude.md` (track L) | AF2CA4CF38E4D7BE6470F8E44A90CA775CE8F60EEBD01FF5948A1CF9CEC4E313 |
| `coord-c1-merged-review-20261015.codex.md` (RC6 defines the target) | 2894E60410FD3C808059ABC7ABF71DA0A0DA3774D58FDF7971226BC144E6AB17 |

The track hashes equal those in `coord-c1-numcert-20261015.tracks.sha256`. Code was read at main @4f219d6 (read-only), with the pinned numpy 2.2.6 from the repository's `.venv`. No code was run, no test executed, and no data or payload opened. Every proof step was re-derived by the editor (§23.4) rather than copied; where a track was wrong or loose, the merged text uses the corrected form (§23.5).

### 23.2 What came from X and what from L

| Component of §15.3 | Source | Notes |
|---|---|---|
| Projective (log-ratio oscillation) analysis: L1–L3, Theorem 1 steps 0–4, the P1 normal-range argument with ν₀ | **L** | Applied in v3 to the ordered reference instead of the BLAS-evaluated filter (decision 2). |
| Sparse transition count d (nonzeros per row/column of T) | **X** | Tighter than L's dense N: ρ̄_ref = 729·u′ for d = 5 against L's 9486·u′. The per-term rounding count is L's (m), not X's γ_{2m} (§23.5 X-a). |
| Weighted-average statement of L2 | **X** | Same fact as L's L2; quoted as the cleaner wording. |
| Final normalisation (L3) | **L** | X's weighted-average-of-M argument is valid but looser by one w_u. |
| Ordered float64 reference oracle with prescribed summation order, computed alongside the oracle (C0) | **X** | Decision 2. Specification tightened: ordered sums start from the first term, zero T entries skipped (bitwise neutral). |
| Operational predictive certified by proved reference bound plus exact measured discrepancy (Theorem 1′, P4) | **X** | Decision 2. v3 states it componentwise in log-ratio form, ρ_h = ρ̄_ref + r_h/(1 − r_h), so that L's downstream theorems apply unchanged. |
| Route F (K4 60-digit Decimal enclosure for P1 failures) | **L** (X had the same fallback) | Decision 2. Uses `posterior_envelope`, `gamma_digits`, `decimal_suffix_posterior`. |
| A in logit-difference form, ω_TE residual (Theorem 3) | **L** | Decision 3. X's validated exponential and interval log-softmax are not used. |
| Single canonical Ĝ everywhere | **L** | Decision 4 (§3.3). |
| H3 tolerances aligned (componentwise 2·10⁻¹²; b^G_i + 10⁻³⁰) | **L** | Decision 5 (§3.4, §16 row 3). |
| M-ln: 40-digit correctly rounded Decimal `ln` | **L** | Decision 6. X's validated scalar logarithms are not cheaper here (§15.3.6). |
| Bootstrap-mean bound: balanced-tree kernel, r^mean = γ_{d_n+1}·max\|Ẑ\| + ζ | **X** (kernel and bound); proof completed in v3 | Decision 7. L's γ_n bound for `np.mean` needs L's A2, which decision 2 removes. |
| Order-statistic lemma L4 | **L** (X stated the same) | Decision 7. v3 adds X's exact rational ranks and a run-time rank check. |
| Theorems 2, 4 (b^G, b^Y, b^Z, b^Zf), constants δ₁, δ₃ | **L** | Re-derived; ρ̄ tightened to e^ρ − 1 (§23.5 L-d). |
| Outward evaluation L5 and OUT; ζ | **L** | Underflow arithmetic corrected (§23.5 L-b). |
| B_num,j = OUT(max_i b^Z) + r^mean; B^H; B^V3_j; 1e-9 floor | **L** (form) + **X** (r^mean) | Decision 8. |
| Signed guards (E), (H), (V) and Theorem 6 | **L** (three-way labels) + **X** (signed-bound statement) | Decision 8; band labels flagged (§23.6). |
| Coverage list, sharing only on exact identity, every-row rule, sealing | **X** | v3 adds the E_canon identity check at H1. |
| Mode-agnostic underflow model (A1) | **L** | Replaces X's gradual-underflow assumption (§23.5 X-c). |
| Operational-not-certified scope | **L** | X's §16 row 19 certification note is not adopted (§23.5 X-f). |
| §13 step 3 | v2 text kept | X proposed PASS_j iff L̂_j − F_j > 0 and FAIL_j iff Û_j + F_j < 0. Once step 2 has passed (|L̂_j|, |Û_j| > F_j), this is equivalent to v2's L_j > 0 and U_j < 0; step 2 now states the equivalence. |
| Cost structure: 2 histories per row, < 0.1 CPU-h | **L** | Decision 9. |
| Tests 1–14 (§15.3.16) | **L** items 1–10, **X** items on injected discrepancies, ranks, coverage; v3 adds kernel, wrapper and E_canon tests | — |

**MERGE decisions, as implemented.**

| Decision | Implemented in |
|---|---|
| 1 Analytic core (L; X where tighter/cleaner, stated) | §15.3.5–15.3.6; this table |
| 2 BLAS assumption removed (ordered reference + measured discrepancy); route F fallback | §15.3.2 C0–C1, §15.3.3 (A2 retired; P1, P4), §15.3.6 Theorem 1′, §15.3.7 |
| 3 Logit-difference A with ω_TE·‖Δz‖∞ | §15.3.2 C4, §15.3.9, §11, §12.1 |
| 4 Canonical Ĝ everywhere | §3.3, §15.3.2 C3 |
| 5 H3 tolerances aligned | §3.4, §15.3.12, §16 row 3 |
| 6 Logs vs 40-digit Decimal `ln` | §15.3.6 M-ln |
| 7 Proved bootstrap-mean bound for the implemented kernel; L4 kept | §15.3.2 C7, §15.3.11 Theorem 5, §3.5 wrapper, §12.3 |
| 8 η and 2⁻⁴⁴ withdrawn; 1e-9 floor kept as extra guard; B_num,j = OUT(max_i b^Z) + r^mean | §15.3.11, §15.3.12, §13 step 2, §16 row 21, §20 item 14 |
| 9 Cost; oracle twice per row | §3.3 (one canonical oracle), §15.3.14, §17 |

**RC6 requirements, as met.**

| RC6 requirement | Where met |
|---|---|
| Four reference rows cannot give an all-row bound | Every-row coverage (§15.3.1); reference rows remain implementation checks (§3.4, §15.2) |
| Max-abs checks do not imply L1 ≤ 1e-12 | No L1 bound is used; componentwise bounds (§15.3.6) |
| 2⁻⁴⁴ lacks a derivation | No log-softmax or exp on the certified path (C4, §15.3.12) |
| Missing rounding and product-error terms | Explicit u′, γ_V, γ_31, γ_{d_n+1}, product cross-terms and ζ in Theorems 2–5 |
| η/min q without a lower bound on true q | Componentwise log-ratio bounds need no lower bound on q* (Corollary 1) |
| Tiny probabilities must not force INCONCLUSIVE | Componentwise ρ ≈ 10⁻¹³ irrespective of q (§15.3.13) |
| Bound post-logit evaluation, oracle, A/G/Y/Z construction, bootstrap means for every eligible row | Theorems 1–5 |
| State all assumptions (elementary functions, BLAS, underflow, normalisation) | §15.3.3: A1, A3, A4 and the "not assumed" list; stored rows not assumed stochastic (ω_TE) |
| Round outward | L5, OUT, up(·), exact rational comparisons |
| B_num,j = max_i b^Z + r^mean; max(B_num,j, 1e-9); signed guards for headroom and V3 | §15.3.11 |
| Absolute log approach would need m± > η and −log(1 − η/m±) | Not used; the componentwise approach avoids it |

### 23.3 What v3 changed outside §15.3

See the changelog row "v3" in §21 and `C1-MERGED-v3.changes.md`. In short: header; §3.3 (canonical Ĝ, one canonical oracle with bitwise E_canon identity, named-order G from permuted arrays); §3.4 (aligned tolerances); §3.5 (tree-mean wrapper); §11 and §12.1 (logit-difference computation); §12.3 (tree means, ranks, rank check); §13 step 2; §15.2; §16 conventions and rows 1, 3, 4a (new), 5, 18, 19, 20, 21; §17 S0, S1 Author A, S3, S5, S7 and the forecast note; §18 fields 1, 2, 3 and 6; §20 item 14; §21 (row 15, new v3 row, C-19); §22.3 F2 (v3 note).

### 23.4 Proof steps checked

Each item was re-derived; "✓" means the step holds as stated in §15.3.

1. **L1 rounding count.** In an ordered sum starting from the first term, a nonzero term meets its product rounding and at most m − 1 rounded additions (additions with a zero operand are exact). ✓ This is tighter than X's γ_{2m} and equal to L's count for dense support.
2. **w_u ≤ 2u′ and m_u ≤ u′.** log((1+u)/(1−u)) = log(1 + 2u/(1−u)) ≤ 2u′; −log(1−u) = log(1 + u′) ≤ u′; log(1+u) ≤ u ≤ m_u. ✓
3. **L2.** Positive combination argument. ✓
4. **L3.** log(D̂/s) ∈ [a − (N−1)m_u, a + w + (N−1)m_u]; adding the division factor gives mag ≤ w + N·m_u and osc ≤ w + w_u. ✓ (X's alternative gives w + w_u + N·m_u.)
5. **Theorem 1, Step 0 (normal range).** Each bullet checked: π_min ε_E ≥ 2⁻¹⁰⁰⁰; transition products ≥ ν₀τ⁺ = 2⁻¹⁰⁰⁰/ε_E; monotone accumulation gives â(z) ≥ fl(b̂(z)T(z,z)); emission products ≥ (1−u)·2⁻¹⁰⁰⁰; P1 on computed quotients implies normal exact quotients (rounding is monotone and 2⁻¹⁰²² is representable); TE^ref and final products ≥ (1−u)·2⁻¹⁰⁰⁰; no overflow. ✓
6. **Theorem 1, Steps 1–3.** osc(b̂_1) ≤ 2w_u; recurrence osc_{t+1} ≤ osc_t + (d+2)w_u; osc(û_32) ≤ [2 + 30(d+2) + d + 1]w_u = [31(d+2) + 1]w_u. ✓
7. **Theorem 1, Step 4 and the constant.** ρ_ref = M_b + (d + N)m_u; ρ̄_ref = [2·31(d+2) + 2 + 2·144 + d]u′. d = 5: 434 + 2 + 288 + 5 = 729. d = 144: 9052 + 2 + 288 + 144 = 9486, which equals L's 2·4527 + 3·144. 729·u′ = 8.094·10⁻¹⁴; 9486·u′ = 1.0532·10⁻¹². ✓
8. **Theorem 1′.** [log(1−r), log(1+r)] ⊂ [−r/(1−r), r] for 0 ≤ r < 1; composition with the reference bound. ✓
9. **Consequence.** |1 − q*/q̂| ≤ e^ρ − 1; e^ρ − 1 ≤ ρ + ρ² for 0 ≤ ρ ≤ 3/2, since (e^{3/2} − 5/2)/(9/4) = 0.8807 < 1. ✓ P4 keeps ρ < 3/2 (main route: ρ̄_ref + 1; route F: ≤ 1).
10. **M-ln.** Correct rounding at 40 digits: relative error ≤ u_40 = 5·10⁻⁴⁰; 5·10⁻⁴⁰·|log q̂| ≤ 10⁻³⁸·|𝓛|. ✓ `Decimal.ln` is documented as correctly rounded under ROUND_HALF_EVEN. ✓ The 40-digit context has Emin −999999, so `ln` of a value ≥ 2⁻¹⁰⁷⁴ cannot underflow. ✓
11. **Corollary 1.** Triangle inequality. ✓
12. **Route F.** β from K4's `posterior_envelope(32, 144)`: the code computes n_ops = 1 + (L−1)(2S+2) and returns max(1 − ℓ, q − 1), a componentwise relative bound (ERROR_BOUND.md §3(a)). ✓ `decimal_suffix_posterior` copies the current context and sets prec = digits, so it inherits the trapping context's traps. ✓ Predictive path count 2N + 2 (two products, 2N additions from Decimal(0)). ✓ (1−β)(1−γ) ≥ 1 − β_q and (1+β)(1+γ) = 1 + β_q. ✓ x = r + β_q + rβ_q; [(1−r)(1−β_q), (1+r)(1+β_q)] ⊂ [1 − x, 1 + x]; −log(1−x) ≤ x/(1−x). ✓
13. **Theorem 2.** L6 for the two subtractions; product cross-term |d̂λ̂ − d*λ*| ≤ |d̂ − d*||λ̂| + |d*||λ̂ − λ*| with |d*| ≤ |d̂| + ε^d; ordered 36-term dot error ≤ γ_36·Σ|d̂||λ̂|. ✓
14. **Theorem 3.** ℓ*_{X⁺} − ℓ*_{X⁻} = Δ − Δlse; lse is 1-Lipschitz in ∞-norm; Σ_v q*^±(v) = Σ_z b*^±(z) r(z) with Σ_z b* = 1, so |Σ_v d*_v| ≤ ω_TE; |Δ| ≤ |Δ̂|/(1−u); collecting gives exactly L's b^A because 1 + u′ = 1/(1−u). ✓
15. **Theorem 4.** 32-term ordered sum error γ_31·Σ|Â|; 2⁻⁵ exact; |fl(0.1·Ĝ) − Ĝ/10| ≤ (u′ĉ₁ + δ₁)|Ĝ|. δ₁: fl(0.1) = 3602879701896397/2⁵⁵, so δ₁ = 0.2/2⁵⁵ = 1/(5·2⁵⁵). δ₃: fl(0.3) = 5404319552844595/2⁵⁴, so δ₃ = 0.2/2⁵⁴ = 1/(5·2⁵⁴). ✓
16. **Theorem 5.** Depth ⌈log₂ n⌉ with carried entries; relative factors distribute over signed inputs; (1+u)(1+γ_k) = (1+u)/(1−ku) ≤ 1/(1−(k+1)u), since (1+u)(1−(k+1)u) = 1 − ku − (k+1)u² ≤ 1 − ku. ✓
17. **L4.** Counting argument in both directions. ✓
18. **Ranks.** numpy 2.2.6 `_inverted_cdf`: virtual index n·p − 1, floor, previous index if the fractional part is 0 else next, integer index, then `take` after `partition` (no `_lerp`). One-based rank = ⌈n·p⌉ as evaluated in float. Float check for p = 0.05: fl(0.05) − 1/20 ≈ 2.776·10⁻¹⁸, so the exact product 5000·fl(0.05) is 250 + 1.3878·10⁻¹⁴, which rounds to 250.0 because the excess is below half an ulp at 250 (2⁻⁴⁶ ≈ 1.4211·10⁻¹⁴); rank 250. p = 0.05/3: 5000·p ≈ 83.33, rank 84. p = 1 − 0.05/3: ≈ 4916.67, rank 4917. ✓ The rank-250 case is close to a rounding boundary, which is why v3 verifies the rank at run time.
19. **L5.** K = 2¹⁶ + 6 roundings: (1−u)^{−K} ≤ 1 + 2⁻³⁶ (Ku ≈ 7.3·10⁻¹²); underflow ≤ 2¹⁷·2⁻⁹⁷⁹·2¹⁰⁵ = 2⁻⁸⁵⁷ < 2⁻⁸⁰⁰. The deepest product in the expanded bounds has 6 multiplications (b^Y's (1/32)·b^A with (1/(1−u))·(ρ·ρ)·q̂·|Δ̂|·½). Leaves ≤ 2²¹: data by P2, ρ̄ ≤ 3.75, constants ≤ 1 + 2⁻⁵². ✓
20. **Lemma U.** ≤ 2¹⁶ events per bound, each ≤ 2⁻⁹⁷⁹, amplified by ≤ 2⁴³: 2⁻⁹²⁰ < ζ. ✓
21. **Theorem 6.** Order statistics of equal rank, L4, sign preservation for |L̂| > F; the H5/V3 inequalities in both directions. ✓
22. **Cross-model G (§3.3).** Two ordered sums of the same 36 float products differ by ≤ 2·γ_35·Σ|p|·½; the 1e-12 tolerance is safe while Σ|p| ≤ 125. ✓ This requires the named-order arrays to be permuted, not recomputed (§23.5 B-b).
23. **H3 alignment.** Componentwise posterior bound for a dense IEEE-tree evaluation M_b = 9198·u′ ≈ 1.021·10⁻¹², predictive 1.0532·10⁻¹², relative-to-ratio conversion e^ρ − 1 < 1.06·10⁻¹² < 2·10⁻¹². ✓ The Decimal G error is below 10⁻⁴⁵ ≪ 10⁻³⁰. ✓
24. **Code facts.** `BayesFilter.run` computes `prior * E[:, w].T`, `normalise_rows` (np.sum then division), `post @ TE` and `post @ T`, with `TE = T @ E` precomputed; `q[:, t+1]` is b_t·TE, so `q[:, 32]` is b_32·T·E. ✓ numpy `_methods._mean` is `umr_sum` then `true_divide`. ✓ `bootstrap_profile` makes one `rng.integers(0, n, size=n)` per draw and calls `np.mean`. ✓ `percentile_interval` is `np.quantile(..., axis=0, method="inverted_cdf")`. ✓ `trapping_context` traps Underflow, Subnormal, Overflow, Clamped, InvalidOperation and DivisionByZero, with Emin −999999. ✓

### 23.5 Errors found in the tracks, and how they were fixed

**Track L.**
- **L-a (presentation error in Theorem 1, Step 2).** L wrote that every log-ratio lies in [min θ_t − N·m_u, max θ_t + N·m_u] and concluded osc ≤ osc_t + N·w_u. That interval has width osc_t + 2N·m_u, so the conclusion does not follow from it. The correct interval is [min θ_t + N·log(1−u), max θ_t + N·log(1+u)], which gives the stated conclusion. Fixed in v3 (with d in place of N).
- **L-b (arithmetic slip in L5).** L's own A1 bounds a below-normal error by 2⁻¹⁰⁰⁰·max(1, |other operand|), but its L5 proof used 2⁻¹⁰⁰⁰. With operands ≤ 2²¹ the per-operation error is 2⁻⁹⁷⁹ and the total is 2⁻⁸⁵⁷, not 2⁻⁸⁷⁸. The conclusion (< ζ) still holds. Fixed.
- **L-c (assumption removed).** Theorem 1 for the BLAS-evaluated filter, r^mean = γ_n·max|Ẑ| for `np.mean`, and the `np.sum` reductions of C3/C4 all rested on L's A2 (BLAS and numpy reductions as binary trees of IEEE operations). L itself flagged A2 as unverifiable from source (its open question 5). Not an error given A2, but A2 is removed by decision 2. Fixed: Theorem 1 is applied to the ordered reference; the operational filter enters by measured discrepancy; C3–C6 use ordered sums; means use the tree kernel.
- **L-d (loose constant).** L used ρ̄ = (e^ρ − 1)·e^ρ, from |q̂ − q*| ≤ (e^ρ − 1)q* ≤ (e^ρ − 1)e^ρ·q̂. Valid, but |q̂ − q*| ≤ (e^ρ − 1)·q̂ holds directly. Tightened; this also shortens the deepest product in L5.
- **L-e (unsupported remark).** L's §15.3.12 stated ‖q̂ − q*‖₁ ≤ (e^ρ − 1)(1 + ω_TE). That presumes min_z r(z) ≤ 1, which the stored rows do not guarantee. Replaced by ρ̄·Σ_v q̂(v), which needs no assumption. The remark is illustrative only.
- **L-f (context precision).** L ran route F's 60-digit computations "inside trapping_context(80)". The posterior function overrides the precision to 60 internally, so the posterior was right; the predictive step must run at ≥ 60 digits for γ^(60) to apply. v3 uses a 60-digit trapping context, as K4's `_reference_posterior` does, and states that γ^(60) is valid for any precision ≥ 60.
- **L-g (H3 for P1-failing rows).** L wrote that a reference row failing P1 "is checked by route F" without saying which tolerance applies. v3 uses the absolute criterion max|x̂ − x̃| ≤ 2·10⁻¹² as a plain implementation check and flags it (§23.6).
- **L-h (placement).** L's row-3 edit attached P0 to H3 with status IDENTITY, while its placement text puts P0 at H1. v3 places P0 at H1 (row 1).
- **L-i (scope of Theorem 6).** L's decision theorem relied on numpy returning the order statistic of the expected rank, without a run-time check. The numpy code supports it (§23.4 item 18), but in the rank-250 case the float product n·p lies only 3.3·10⁻¹⁶ inside a rounding boundary. v3 adds the run-time rank check.
- **L-j (heuristic labelled).** L's P(INCONCLUSIVE/NUMERICAL) ≲ 5·10⁻⁵ assumes a normal-like density for the bootstrap bound. Retained, labelled as a heuristic projection.

**Track X.**
- **X-a (conservative count).** X counted g_m = γ_{2m} per nonnegative dot (two roundings per term). For an ordered sum starting from the first term, the count is m per nonzero term (§23.4 item 1). Not wrong; tightened, and L's per-term count is used.
- **X-b (looser normalisation).** X's weighted-average bound on the final posterior is valid but exceeds L3 by w_u. L3 is used.
- **X-c (underflow mode).** X's mean-kernel term ((n−1)/n·(1+u)^{d_n} + 1)·2⁻¹⁰⁷⁴ and its "a = 2⁻¹⁰⁷⁴ per operation" assume gradual underflow; under flush-to-zero an addition can lose up to 2⁻¹⁰²². X relied on a run-time check of subnormal prerequisites. v3 uses L's mode-agnostic A1 and ζ, so the bound holds in every mode.
- **X-d (unproved range condition).** X's "an output at least twice the smallest normal value is sufficient to rule out a borderline normal/subnormal ambiguity" was not tied to a precondition that covers every intermediate operation. Replaced by L's P1/ν₀ argument, which is proved for every operation of the reference (Theorem 1, Step 0).
- **X-e (bootstrap-mean wrapper).** X's kernel and bound are adopted. The proof sketch did not state that the relative factors distribute over signed inputs, or that (1+u)(1+γ_{d_n}) ≤ 1 + γ_{d_n+1}; both are proved in Theorem 5.
- **X-f (scope).** X's §16 row 19 edit said that P1's row construction and centred-draw mean arithmetic are certified. `precision.py` uses `np.mean`, and under the merged scope the ladder is operational. Not adopted; row 19 now states that P1 is operational.
- **X-g (labels).** X kept the existing scientific statuses for a guard-band hit at H5/V3 (HEADROOM, MODEL_HEADROOM), whereas L used INCONCLUSIVE/NUMERICAL. v3 adopts L's three-way rule and flags the labels (§23.6).
- **X-h (not adopted; checked anyway).** X's exponential reference: the Taylor remainder τ = 2/(8¹³·13!) holds because e^{1/8} < 2; the squaring envelope L_{e,k}, U_{e,k} is correct; k ≤ 10 for |x| ≤ 128. No error found. It is unused because decision 3 removes the exponential from the certified path.

**Both tracks.**
- **B-a (sharing).** Neither track checked that a single canonical oracle across the three models requires the models' E_canon arrays to be bitwise identical. X stated the rule generically ("sharing only on exactly identical arrays"); L assumed it. v3 adds the check at H1 (P0, §3.3) and flags it for pre-freeze confirmation (§23.6).
- **B-b (cross-model G).** Both tracks kept "G cross-model ≤ 1e-12" without justification. v3 proves it safe when the named-order G is computed from the permuted canonical arrays, and prescribes that the arrays be permuted rather than recomputed. Recomputing `np.log` on a permuted array need not reproduce bitwise values, because numpy's vectorised and scalar-tail paths may differ.
- **B-c (readiness claims).** Both tracks declared FREEZE_READY, and X stated that "no mathematical question remains open". Each still needed the corrections above and the independent review. v3 is CERTIFICATE_MERGED, not frozen.

### 23.6 Open items for the coordinator or reviewer

1. **Independent review of §15.3** (the RC6 condition). Freeze stays blocked until it is recorded.
2. **E_canon identity (B-a).** H1 now requires the three models' E_canon arrays to be bitwise identical. This is result-blind and can be confirmed before freeze from the stored EmissionSpecs. If they are not identical, decisions 4 and 9 need a ruling: one oracle per distinct process, and which Ĝ enters Z_j.
3. **H5 kernel.** The certified H5 uses a C1 wrapper that keeps `bootstrap_profile`'s index semantics but replaces `np.mean` by the tree kernel. This departs from calling `bootstrap_profile` directly as RC1 wrote it. The alternative, keeping `np.mean` with L's γ_n bound, would reintroduce a numpy-reduction assumption.
4. **Band labels at H5/V3** (L open question 4; X-g): INCONCLUSIVE/NUMERICAL (adopted) or the gate's own HEADROOM/MODEL_HEADROOM. Both stop the study.
5. **Closed-form and named = canonical checks** (L open question 3, second half; not ruled by decision 5). They remain absolute 1e-12. Two operational evaluations, each within ≈ 1.05·10⁻¹² of the exact value under an IEEE-tree model, could in principle differ by up to ≈ 2.1·10⁻¹² for entries near 1. L suggested componentwise 4·10⁻¹².
6. **H3 for P1-failing reference rows** (L-g): absolute 2·10⁻¹², an implementation check without a proof. Expected count 0.
7. **P2 and P4 limits** (L open question 7): |z| ≤ 2¹⁹, magnitudes ≤ 2²¹, discrepancy ≤ 1/2, with FAIL_TECHNICAL statuses.
8. **Scope** (L open question 9): the eligibility, κ_ν, fits, M/F/V1/V2 gates and the P1 ladder are operational, not certified.
9. **`error_bound._reference_posterior`** (L open question 10): replicated with provenance (adopted) or imported.
10. **Route-F volume alarm** (L open question 6): not adopted; the count is reported.
11. **A1 self-test content**: the exact test vectors are to be fixed in API.md at freeze.
12. **Carried from v2:** reviewer confirmation of the v2 required changes; F1 (MERGE.md erratum); F6 (statuses of adapted exceptions).
