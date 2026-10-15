STATUS: REVIEW_CHANGES_APPLIED (not frozen)

# C1-MERGED-v2: crossed counterfactual state forcing at the final readout of the E4 cylinder-O models

**Document identity.** `C1-MERGED-v2`. This is the merged protocol for planning request `coord-c1-freeze-readiness-20261014`. It is `C1-MERGED-v1` (sha256 72C86FFC…45D7) with every required change of the independent review `planning/responses/coord-c1-merged-review-20261015.codex.md` (sha256 2894E604…AB17; verdict APPROVE_WITH_REQUIRED_CHANGES) applied. §22 lists each change, the sections touched and the flags.

**Authority.** The owner's message `archive/owner-overnight-transfer-20261014/OWNER_MESSAGE.md` (sha 13160D21…), part B3 item C, with resources from B4 and limits from B5/B6. The binding coordinator decisions are in `planning/responses/coord-c1-freeze-readiness-20261014.MERGE.md`. The adopted design is `…MERGE_ANALYSIS.md` §6, items 1–22. **Erratum to MERGE ruling 4 (review required change 2):** the clause "so an oracle-perfect readout gives θ = 1" is superseded by the oracle-perfect anchor of §1.3. An oracle-perfect primary readout gives θ_T = 1; the control-adjusted endpoint θ equals 1 only when E[Ā_C] = 0. This document does not edit MERGE.md; the coordinator records the erratum there (§22, flag F1).

**Sources.**
- Track L: `…claude.md`.
- Track X: `…codex.md`.
- Independent review of v1: `coord-c1-merged-review-20261015.codex.md`.

**Code verified against.** `topo-pilot` main @ 4f219d6, read-only. §18 lists every reused function together with its verified signature and semantics. §21 lists every correction made to the source plans. The code facts cited by the review were re-verified for v2 (§22).

**What this document is.** A planning document, not a freeze. v1 received the result-blind independent review (Codex first, per owner part D). This v2 applies the review's required changes and returns to that reviewer for confirmation. **Freeze is additionally blocked until the numerical certificate of §15.3 (status NOT_READY) is attached and independently reviewed.** After freeze come independent test authors and implementation. No C1 data stage may start before K4's chart outcome is known (§14).

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

`percentile_interval` uses `inverted_cdf`. The gate requires `lower > 0.01` (nat), subject to the signed numerical guard of §15.3. Use seed 520506, with the same call, on the fresh eligible rows. Calibration Ḡ is reported only.

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

**Inference.** Joint whole-row bootstrap with 5000 draws, PCG64 seed 520504 (fresh: 520507). Each draw makes one `rng.integers(0, n, size=n)` call, shared by all models and arrays. The lower bound per model is the 0.05/3 `inverted_cdf` quantile of the resampled mean of Z_full.

**Gate.** All three lower bounds > 0, subject to the signed numerical guard of §15.3. Otherwise INCONCLUSIVE/MODEL_HEADROOM. V3 did not establish that the model exceeds the prespecified 0.30 normalized discrimination threshold with the required lower bound. This can reflect insufficient discrimination, uncertainty, or a numerical/technical problem. It does not establish zero discrimination. The phase assay stops as specified.

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
2. **Numerical certificate** (§15.3; NOT_READY until its proof is attached and reviewed). If for any model j |L_j| or |U_j| ≤ max(B_num,j, 1e-9), the outcome is INCONCLUSIVE/NUMERICAL.
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
See §3.4: 4 rows per split, three histories each, 60-digit posteriors in an 80-digit trapping context. All-row Decimal enclosures (X) are not used. They are out of proportion to a 0.10 relative margin and would cost tens of CPU-hours. These reference-row comparisons are implementation checks, not universal error bounds (§15.3).

### 15.3 Numerical certificate

**Numerical certification: NOT_READY until the following proof is attached and independently reviewed before freeze.**

Recorded float64 logits remain the operational model output. The certificate must bound post-logit evaluation, oracle predictive errors, construction of A/G/Y/Z, and bootstrap-mean arithmetic for every eligible fresh row. Reference-row comparisons are implementation checks, not universal error bounds.

Oracle uncertainty must be established analytically for the permitted filtering computation or by validated per-row enclosures. Componentwise or relative bounds should be used where an absolute L1 bound becomes uninformative for tiny probabilities. All assumptions about elementary functions, BLAS reductions, underflow, and normalization must be stated.

Neither η = `1e-12` nor the log-softmax constant `2^-44` is accepted solely because it passes sampled reference checks. Their retention requires a source-specific derivation. Certificate evaluation must round bounds outward.

Let \(b^Z_{j,i}\) be the proved row bound and \(r^{\rm mean}_j\) the proved bootstrap-mean arithmetic bound. Define
\[
B_{{\rm num},j}=\max_i b^Z_{j,i}+r^{\rm mean}_j.
\]
The endpoint rule uses `max(B_num,j, 1e-9)` for model j. Corresponding signed numerical guards apply to the headroom and V3 thresholds. The `1e-9` floor is an additional conservative guard, not a proof of accuracy.

**Guidance for checking a proposed proof (from the review; not itself a certificate).** Under a genuinely established per-arm L1 bound η, a valid **input-perturbation portion** of the A bound is:
\[
\tfrac12\left[
(\|\widehat q^+-\widehat q^-\|_1+2\eta)(\epsilon_++\epsilon_-)
+2\eta\|\widehat\ell_+-\widehat\ell_-\|_\infty
\right].
\]
Arithmetic-rounding terms must still be added. For oracle logarithms, an absolute-error approach requires \(m_\pm=\min\widehat q^\pm>\eta\), and uses \(-\log(1-\eta/m_\pm)\), plus logarithm-evaluation error—not simply `η/m±`.

**Do not freeze with this item unresolved.** This does not require all-row Decimal posterior calculations; a proved analytic envelope or validated enclosure is sufficient.

The v1 certificate (ε = 2⁻⁴⁴·(1 + 2·max_v|logit_v|), declared η = 1e-12 verified on the reference rows, and the A/G/Z bounds built from them) is withdrawn: four reference rows cannot establish an all-row bound, a maximum-absolute-error check does not imply an L1 bound, 2⁻⁴⁴ lacked a derivation, rounding and some product-error terms were omitted, and the G bound used η/min(q) without ensuring the required lower bound on the true probabilities. The rule is applied in §13 step 2.

---

## 16. Gate table (exact evaluation order; the first non-PASS stops)

**Conventions.**
- "≥", "≤", ">" and "<" are meant exactly as written.
- Gate records use `stage_records.record_gate`/`run_gate`: `errors.Invalid`/`JoinError` → FAIL_TECHNICAL; `Unresolved` → INCONCLUSIVE.
- The C1 boundary adapts `StageFailure`, `ProfileError`, and reference-input/Decimal exceptions into recorded C1 failures. `stage_records.run_gate` does not catch those exception classes unchanged. Every failure receives a gate or resource-stop record before termination.
- **Every-row checks** appear only for algebraic or numerical identities and lineage, whose failure is treated as a defect or, for lineage, as an alarm (§2.4). **Statistical gates are fraction-based.**
- Eligible rows are used unless stated otherwise.

| # | Stage | Gate | Criterion | Status on failure |
|---|---|---|---|---|
| 0 | pre-data | G0 CHART_BRANCH | §14: branch A or C proceeds (C only if K4 never attempted chart construction) | B, including charts attempted without a complete, accepted PASS record → INCONCLUSIVE/CHART_UNAVAILABLE; K4 not final → WAIT |
| 1 | S3 | H1 IDENTITY | World/Transition/Emission/checkpoint IDs equal the CONTRACT; `validate_process(T, E, π, 1e-12)`; perms are permutations; `canonical_emission` round trip | FAIL_TECHNICAL/IDENTITY |
| 2 | S3 | H2 SEPARATION | `check_disjoint` over all C1 sequence IDs and stored ones; U_cal ∩ R_1 = ∅, U_val ∩ R_1 = ∅ and U_cal ∩ U_val = ∅ over every source/donor role combination, with registry version 1 bound by content hashes (§2.4); `check_first_token(first, πE, split)` does not raise (p ≥ 1e-4) per block | FAIL_TECHNICAL/LINEAGE |
| 3 | S3 | H3 ORACLE | symmetry ≤ 1e-14; closed form ≤ 1e-12; named = canonical ≤ 1e-12; G cross-model ≤ 1e-12; Decimal: posterior ≤ 1e-12, predictive ≤ 1e-12, surprisal ≤ 1e-10, G ≤ 1e-10 | FAIL_TECHNICAL/ORACLE |
| 4 | S3 | H4 ELIGIBILITY | f_cal ≥ 0.90 and f_val ≥ 0.90 | INCONCLUSIVE/ELIGIBILITY |
| 5 | S3 | H5 HEADROOM | one-sided 0.05 LB of Ḡ_val > 0.01 nat: `lower` from `bootstrap_profile(..., rng=np.random.Generator(np.random.PCG64(520505)), draws=5000)` and `percentile_interval(result["B"][:, 0], [0.05])[0]` (§3.5) | INCONCLUSIVE/HEADROOM |
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
| 18 | S5 | V3 | all three LB(Z_full) > 0 at 0.05/3 (seed 520504), with the signed numerical guard of §15.3; donor logits are first retained for scientific use here (§2.2) | INCONCLUSIVE/MODEL_HEADROOM |
| 19 | S5 | P1 | ladder (§12.4): some N PASS; primary and control logits are first retained for endpoint/precision use here (§2.2); tail-path identity ≤ 1e-12; identity patch bitwise | INCONCLUSIVE/UNDERPOWERED (FAIL_TECHNICAL for identity) |
| — | S6 | ACCEPT | coordinator's independent review of the gate report (sealed means unopened); release R3 names N_test and k | not accepted → stop |
| 20 | S7 | T-PRE | all computed before any fresh A/Y/Z, apart from the declared target-free identity checks (§2.2): H1, H2 (U_test ∩ R_2 = ∅ over every source/donor role combination, registry version 2, §2.4), H3 on test rows; \|f_test − f_val\| ≤ 0.02 and f_test ≥ f_val − 0.02 (so n_test ≥ N_test); LB Ḡ_test > 0.01 (seed 520506, same call as §3.5); M0 (identity patch on every eligible row), M1, M2 (with leakage), M3, M4, V1, V2, V3 (seed 520507), tail-path identity — same tolerances | INCONCLUSIVE/TEST_GATE: endpoint not scored, arrays sealed and kept (FAIL_TECHNICAL for identity or lineage) |
| 21 | S7 | NUM | §15.3 certificate, per model: \|L_j\| and \|U_j\| > max(B_num,j, 1e-9) (proof NOT_READY; must be attached and reviewed before freeze) | INCONCLUSIVE/NUMERICAL |
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
| S0 Written contract | This document → result-blind independent review (Codex first) → corrections (this v2) → reviewer confirmation, and the §15.3 certificate proof attached and independently reviewed → freeze with C1 `PROTOCOL.md`, `CONTRACT.json` (uncapped CPU and `lift_cpu_cap_s` written as JSON `null`; `native_operation_wall_s` 600), `API.md`, `TEST_PLAN.md`; freeze sha recorded in the decision log | documents only |
| S1 Independent tests | Two authors work from API.md before any implementation, on synthetic fixtures only (see the list below) | ≤ 0.25 h |
| S2 Implementation | Separate builder, new worktree from the accepted head; reuse and bindings per §18 (including `meter.WORKER_SESSION`/RUN.lock identity, the extracted disk/limiter helpers with provenance and regression checks, the `env_identity` import order, the C1 PREREQUISITE and PASS-gate-set checks, and exception adaptation at the C1 boundary); ≤ 2 correction jobs per defect; the full existing suite and the K4 chart/precision tests must pass unchanged | ≤ 0.25 h of tests |
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
  - the ratio-to-mean reduction θ > c ⇔ E[Y − cG] > 0 (§12.2) and the decision boundaries (equality → INC);
  - bootstrap index order, shared across models;
  - ladder logic, including the k formula;
  - the numerical certificate;
  - named/canonical joins.
- **Author B:**
  - FWL recovery of a known B in a noiseless synthetic case, plus a trap showing that sequential residualisation is wrong;
  - Haar and primary-QR sign conventions (positive diagonal), isometry and isospectral identities with the §6 zero-norm and zero-spectrum rules, pair mapping;
  - D_w, D_y, leakage and D_M with q99 `inverted_cdf`;
  - V1/V2 wrap at ±π, sign(0) and median ties;
  - gate order (computation-order rule, §2.2: no logit read before M2/M3 pass on calibration apart from the declared identity/zero-patch checks; donor logits first retained at V3, primary and control logits at P1; fresh A/Y/Z never evaluated when row 20 fails);
  - RidgeProbe/`nested_ridge` equivalence;
  - `stage_records` prerequisite rebinding.

**Total forecast.** Expected 2–6 CPU-h including overhead, tests and the branch-C fallback (MERGE ruling 8). This is a forecast, not a cap. The coordinator may refine it from metered stage timings, but may not change sample counts, methods or stop rules.

---

## 18. Six-field reuse assessment (charter; every reused function verified at 4f219d6)

| Field | C1 |
|---|---|
| **1. Existing functions reused unchanged** | See the grouped list below the table. |
| **2. Not reused, or not reusable unchanged (verified)** | See the second list below the table. |
| **3. Missing capability** | (1) Donor transform with w32 kept, the symmetry and closed-form checks, eligibility, κ_ν, G. (2) The FWL map and forced states. (3) Haar frames and the control family. (4) Kernels for damage, leakage, D_M support, V1–V3. (5) The crossed contrast, Z, the bootstrap decision, the certificate, the ladder k rule. (6) The exposure registry builder and C1 history tables. (7) The Decimal predictive/log helper. (8) The C1 stage driver and bindings: `c1_meter_bind` (including the `meter.WORKER_SESSION` binding and the extracted disk/limiter helpers), C1 release, `stage_records` PREREQUISITE rebinding with the C1 PASS-gate-set checks, `env_identity` imports rebinding, exception adaptation at the C1 boundary, and one ledger initialisation in the existing schema `x4-oracle-profile-ledger-v1` (the meter requires the ledger to exist). |
| **4. Smallest change** | One new package, `tools/c1_state_forcing/`. It contains pure kernels (arrays, configuration and an injected guard/timer in; no hidden I/O or randomness) plus thin bindings and a driver, roughly 900–1,200 lines plus tests. Frozen K4 and job-0014 files are never edited. Nothing new goes into `src/`. |
| **5. Stable interfaces and invariants** | See the third list below the table. |
| **6. Regression checks and next extension** | **Regression:** the existing learner, analysis and oracle-profile suites and the K4 chart/precision tests pass unchanged; the S1 independent tests come first; on real data, the tail path vs `forward_with_patch` and RidgeProbe vs `nested_ridge` equivalences are checked; guard fault tests cover every rebinding (STOP, disk, uncapped ledger, 12 GiB job object, WORKER_SESSION/RUN.lock identity, uncapped lift). **Next extension:** the same kernels can serve one separately reviewed follow-up without new abstractions, for example a w31-retaining donor (shifting w1..w30) to separate short from long history, or an earlier site if a certified chart exists there. No generic causal or topology framework. |

**Field 1, existing functions reused unchanged (signature → use):**
- **Process and data:**
  - `dataset.sampler.HMMSampler(T, E, π, layout).sample(n, rng)` → (tokens [n, 33], states), emitting first; w33 and the states are dropped;
  - `dataset.checks.process_code(family, mode, sigma, replicate)`, `make_sequence_ids(code, split ∈ {train, dev, test}, n)`, `check_disjoint(**splits)`, `check_first_token(first, p_w, split)`;
  - `contracts.SeedTree(master).generator(name, *scope)` with `.issued`.
- **Oracle:**
  - `oracle.BayesFilter(T, E, π).run(tokens)` → b, q, log_evidence, ce (§3.3);
  - `tools/x4_oracle_profile/oracle_profile.py`: `validate_process(T, E, π, tol)`, `canonical_emission(E_named, perm)`, `circle_features(coords)`, `posterior_means`/`suffix_posterior` (K = 32 equals the full-prefix filter for 32-token histories), `bootstrap_profile(norm, sq, Ks, rng, draws)` (returns a dict {"B", "V"}; `rng` must be a `numpy.random.Generator`, §3.5), `percentile_interval(samples, probs)` (inverted_cdf);
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
14. Symmetry tolerance 1e-14 (changed from L's 1e-15); the numerical certificate (§15.3: NOT_READY until its proof is attached and independently reviewed; η = 1e-12 and 2⁻⁴⁴ are not accepted without a source-specific derivation; per-model B_num,j); numerical floor 1e-9 (an additional conservative guard, not a proof of accuracy).
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
| 15 | L (float64, bitwise identity, Decimal on 4 rows) + X (logits as operational output) + W (certificate constants) | C-19 |
| 16–17 | L (gate order, stages) + X (output envelope, JSON null, one thread) + A (ruling 8 CPU) | C-23, C-25, C-26, C-27 |
| 18 | L + X lists, corrected by W against the code | C-2, C-3, C-9 to C-13 |
| 19 | L ∪ X | — |
| 20 | L§15 + A§6 list + W additions | — |
| all | v2: independent review `coord-c1-merged-review-20261015.codex.md`, required changes 1–13 | §22 |

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
- **C-19 (X + W).** The certificate is defined relative to the recorded float64 logits, with explicit constants. **v2 (review RC6):** the v1 certificate and its constants are withdrawn as unsupported; §15.3 is NOT_READY until a proof is attached and independently reviewed before freeze; the endpoint rule uses per-model max(B_num,j, 1e-9).
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
- **F2 (RC6, freeze blocker).** RC6 is applied as text, but the certificate itself does not yet exist. §15.3 is NOT_READY. **Reviewer confirmation of v2 is not enough for freeze: the certificate proof must first be attached and independently reviewed** (review: "Do not freeze with this item unresolved").
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
