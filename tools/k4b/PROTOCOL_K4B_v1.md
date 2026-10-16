STATUS: FROZEN (K4B-FROZEN-v1, 2026-10-16; coordinator 75dcd488; Codex review coord-k4b-review-20261016 + v2 and v3 confirmations; v3 = K4B-MERGED-v3 sha256 BE734BF4…EA0C)

# K4B-MERGED-v3: does the learned circle carry first-harmonic belief information beyond the last four symbols? (E4 cylinder-O models, fresh histories, no training)

| Field | Value |
|---|---|
| Protocol id | K4B-MERGED-v3. Seed and data scope tag `k4b-sf-v1` |
| Role | Protocol writer (W) for the merged protocol; v2 was the fix round, v3 the final fix round after the v2 confirmation (`coord-k4b-review-20261016.v2confirm.codex.md`, items 1–4; §18.5). Planning only: no Python run, no test run, no repository code run, no scientific data or store payload opened, no git write. Two files written: this one and `K4B-MERGED-v3.sha256`. v1 and v2 are left untouched |
| Date | 2026-10-16 |
| Review applied (v1→v2) | `planning/responses/coord-k4b-review-20261016.codex.md`, Codex result-blind review of K4B-MERGED-v1 (sha256 63120E93187E74EFD41F7193DD811637C47CCC73DFFDCB7DEDE1A15F41E56C96, re-checked by W against `K4B-MERGED-v1.sha256`): VERDICT APPROVE_WITH_REQUIRED_CHANGES, RC1–RC15 (cited **RC n**). Coordinator rulings `…/coord-k4b-review-20261016.rulings.md` (cited **RU**): every RC adopted as written; F1–F19 ruled as the reviewer recommends; three optional suggestions adopted (deterministic worst-case F_plan; a width-preserving exclusion-power diagnostic, report only; extra independent-test cases). The mapping of every change to its location is in §18; the one place where a reviewer text was adapted is §18.3 |
| Authority | Owner addendum 3, `archive/owner-decisions-20261015/OWNER_DECISIONS.addendum-3.md`, sha256 `222578FE865C7FFFAD5B4CF6919F734A5B1A7E7B296C1D706F0D5EC4138B38A4` (re-hashed by W): K4b is approved as a new study; K4 stays closed INCONCLUSIVE, with no rescue. Owner addendum 10, `…/OWNER_DECISIONS.addendum-10.md`, sha256 `E28BDE0C1B2FE989FFF945AF282AA62F378FB4EF93987C7C1C2E3874993722A2` (hashed by W): C1′ is closed; the next track is this writer. Chart rule: owner A2 in `…/OWNER_DECISIONS.v1-a73c869.md`, sha256 `5BD1FDB0D66BCE5299644659B3E09436CA94B762A62D24D02E1AB064FDE537CD` (re-hashed by W). The convenience view `OWNER_DECISIONS.md` is never bound |
| Binding decisions | `planning/responses/coord-k4b-20261015.MERGE.md` (sha256 66B0E33C…5570), decisions 1–15 (cited **MD n**). They are followed exactly, except where an update since the merge (U1–U6 below) supersedes a fact a decision assumed. Each such place carries the mark **⚑** and is listed in §17, where every flag now carries its ruling (RU) |
| Analyst | `…/coord-k4b-20261015.MERGE_ANALYSIS.md` (sha256 9F5E6AB7…3035), D1–D14 (cited **AN §n** or **AN Dn**) |
| Request | `planning/requests/coord-k4b-20261015.md` (cited **RQ n**). W re-hashed it: `ECDFA7C447FADA80E0A8ADAE95A0B85EA8BAF8963D563911AE7B290816BFA162`, equal to `requests/coord-k4b-20261015.sha256` |
| Tracks | Track L `…/coord-k4b-20261015.claude.md` (sha256 D84AFFF3…2DD3), the base design (MD 1; cited **L§n**). Track X `…/coord-k4b-20261015.codex.md` (sha256 464B335D…A83A), the grafts (cited **X§n**) |
| Other inputs | `PROTOCOL_C1PRIME_v1.md` on c1p-0035 (sha256 0B1F107E…F33A, identical at main; cited **C1′ §n**), especially §2.4, §14, §15.3.11, §19. `C1PRIME-DELTA-FROZEN-v1.md` (sha256 4556EB91…9A58). `D2A-FROZEN-v1.md` §11.3 (the allowlisted-diff commit rule, cited **D5 rule**). `X6-MERGED-v1.md` (style). K4: `docs/proposals/CIRCULAR_HISTORY_K4_PROTOCOL_DRAFT.md` (sha256 42FB2E9F…E0FA) and `tools/x4_circle_history/ERROR_BOUND.md` (sha256 CCBF55C8…6705; cited **EB §n**). Job records: jobs/0014, 0018, 0023, 0027, 0033, 0039, 0042, 0044 (cited **job n**) |
| Code read for reuse claims | topo-pilot **main @ `c460e249785a0b0c66633aefb31ace400edd05bb`** (the recommended reviewed reference, §11.5) and **c1p-0035 @ `93350d7e9016ad9c88108ecb50d0ec2f9c233d44`** (the C1′ execution commit). W ran, read-only: `git diff --name-status c460e24 93350d7 -- tools/c1prime tests/c1prime tools/c1prime_registry tools/x4_circle_history tools/x4_oracle_profile tests/oracle_profile src` and `git show <commit>:<file> | sha256sum` for every reused file at both commits (§11.3). Every function named in §11.3 was read at c460e24; its signature is quoted there. v2: W additionally verified at c460e24 (identical at 93350d7) `tools/x4_circle_history/op_guard.py` (sha256 90fb20e3…0590a1; `timed_factory`, `overdue`, `archive_stale`), the job-0014 `meter.py` module names rebound in §11.7 (`OUT`, `LEDGER`, `EMERGENCY`, `LOCK`, `ACTIVE`, `LOG_DIR`, `WORKER_SESSION`, `CAP_S`, `STOP_NEW_S`, `OUTPUT_CAP` = 128 MiB default, `--max-cpu` default 600, `--max-wall` default 3600, `limit_reason`), `controls.JOB_ID`/`TASK_SHA256`, `winjob.MEMORY_CAP` (8 GiB default), and `c1_registry_sources.history_index_ids(store=None, root=ART)`, `coverage(seqs_a, hist_ids, root=ROOT)` and the `ValueError → EMPTY` branch of `handoff_sources` |
| Reads outside code (disclosure) | W listed store directory names (no content) of `c1prime-store`, `d2a-store` and the project root. W read the `meta.json` (metadata, not payload) of the six checkpoints of §2.2 to verify run_key, step, status and `seed_map`. W hashed `c1prime-store/FREEZE.json` (a code-freeze record, not a payload) and read its file-hash list. W read job reports and reviews 0014, 0018, 0027, 0033, 0039, 0041 (CPU lines only), 0042 and 0044. No `*.npz`, `*.pt`, `HIST_*`, `ORACLE_*`, `CERT_*` or `CHART_*` file was opened or hashed |
| Arithmetic | Every hand value was recomputed by W with a desk calculator (awk floating point, written to the scratchpad; no Python, no repository code, no data). Values that appear in no input are marked **[W]**. Inherited measurements and forecasts are marked **[H]**. **No [W] or [H] value is a gate**: every gated quantity is computed by the run |
| Next step | The independent result-blind review (planning protocol rule 4) is done (RC1–RC15, applied here). The Codex confirmation of v2 (CONFIRM_WITH_REQUIRED_CHANGES, items 1–4) is applied in v3 (§18.5). Next: the freeze. Execution only after coordinator dispatch |

**Updates since the merge (2026-10-15 ~10:00Z) that this protocol reflects.**

| # | Fact | Source | Effect here |
|---|---|---|---|
| U1 | **C1′ is terminal.** It ended INCONCLUSIVE/FAMILY_UNMATCHED at S4 gate M2-cal (all three models), and the owner closed it. Its chart did **not** fail: C0-cal PASSED in all three models (\|C*\| = 512/512, one component, no excluded landmark, lift `centered_exact`, g = 1, smoothing residual 2.10e-12 to 2.72e-12, gauge alignment 0.894 to 0.899). C0-val was never reached | addendum 10; jobs/0044/review.md (sha256 19C3E623…E220); jobs/0044/report.md; jobs/0042/report.md | MD 11's two branches (CHART_UNAVAILABLE; FAIL_TECHNICAL in shared chart code) did not occur ⚑. What K4b inherits instead is in §4.5 |
| U2 | **D-2a is terminal**: NOT_LEARNED at stage 1 (stop rule S4), jobs 0028–0033, merged to main at 4bc0b16. Its histories are in `d2a-store` | jobs/0033/review.md (sha256 4AD2691D…2969); main commit 4bc0b16 | MD 10's sequencing precondition is met for both studies; D-2a histories enter the K4b registry (§3.4) ⚑ |
| U3 | **C1′ code location.** The C1′ code K4b reuses was executed on c1p-0035 @ 93350d7, frozen as `c1prime-store/FREEZE.json` (sha256 EA063628…C9E65C, W verified). Main @ c460e24 has the older C1′ merge 7c8da1f and **already contains job 0027** (4ac46de is an ancestor of c460e24). Main lacks R10, R11 and R13 | git (W) | MD 12's "main after job 0027" is already satisfied. W verified that **every reused file is byte-identical at c460e24 and 93350d7**; the fixes touch only files K4b does not reuse. Recommendation in §11.5 ⚑ |
| U4 | `docs/proposals/GAP_CLOSING_EXPERIMENTS_HE.md` is committed on main at 89b9bab | git (W) | Bound in §2.1 (MD 14 done) ⚑ |
| U5 | C1′ M2-cal lesson: the chart-phase-directed intervention moved the decoded w32 readout on 29–39% of rows, while matched random-whitened controls moved it on < 0.1% | jobs/0044/review.md | K4b has no intervention, forcing or decoder-damage gate, so the lesson does not apply (§9.8) |
| U6 | C1′ job 0039 lesson: an aborted stage left HIST files that blocked the rerun's G0, and no lineage rule existed in advance | jobs/0039/review.md (R12) | The rerun and lineage rule is fixed in advance (§11.8) |

**Merge decisions as applied.**

| MD | Decision | Where | Status |
|---|---|---|---|
| 1 | L's design is the base, with X's grafts | throughout | applied |
| 2 | Own charts by the C1′ LCC ≥ 95% rule; `fit_chart_lcc`, `c0_val`, the construction ledger and the exception mapping reused unchanged and hash-bound; fresh landmarks under `k4b-sf-v1`; C1′ histories and charts enter only as registry digests | §4, §3.4, §11.3 | applied |
| 3 | Calibration and validation 3,072 rows each | §3.1 | applied |
| 4 | C1′ tree mean, B_num and rank checks | §5.4 | applied |
| 5 | F = certified numerical bound + Z_bound; claims about the documented law | §5.5, §8 | applied (Theorem B′ restated) |
| 6 | Two-sided exclusion; SUPPORT in all three models | §8.1 | applied |
| 7 | Test size from the ladder by `precision.mde` on upper validation SDs, plus X's joint power check; validation means sealed | §7 | applied; L's power claim corrected (§7.4) |
| 8 | m4-phase null, SHA-of-suffix null; three step-0 charts (nine constructions in total), reported and never subtracted; step-0 IDs verified at the identity gate; descriptive suffix decoder with a fully specified target; Δ1, Δ2 descriptive | §9, §6 (H1) | applied |
| 9 | Fresh-test B4 reported only; the validation B4 is the gate (`guard_H5`, unchanged) | §6 (B4-VAL, T-PRE) | applied |
| 10 | Nothing sampled until C1′ is terminal; queue C1′ → D-2a → K4b; registry includes every C1′ and D-2a history and every store present at the freeze; refresh rule | §3.4, §3.5 | applied; ⚑ both preconditions now met (U1, U2) |
| 11 | If C1′'s chart fails: proceed with a qualifier (CHART_UNAVAILABLE) or stop for review (FAIL_TECHNICAL in shared chart code) | §4.5 | ⚑ neither branch occurred (U1); replaced by the disclosure of §4.5 |
| 12 | Base commit: main after job 0027; execution commit pinned at dispatch under the allowlisted-diff S0 rule | §11.5 | ⚑ job 0027 is already in main; R_ref = c460e24 (F1 ruled by RU: adopted; housekeeping wording corrected by RC4) |
| 13 | Measure-only CPU; TEMP on X:; 12 GiB RAM; forecast 1–3 CPU-h | §11.7, §12 | applied (forecast revised in §12) |
| 14 | `GAP_CLOSING_EXPERIMENTS_HE.md` committed before freeze, its hash bound | §2.1 | ⚑ done at 89b9bab (U4) |
| 15 | Licences: no memory horizon, no causal use, no mechanism, no generalisation, no change to any verdict | §8.4 | applied (union with X) |

## Summary (≤ 300 words)

**Question.** In the three E4 cylinder-O models (seeds 1729/2718/3141, step 5000, `resid_post_3`, position 32), does a circular coordinate, built by the LCC ≥ 95% chart rule on fresh calibration histories, covary with the part of the first-harmonic belief that the last four observations do not determine?

**Target.** Δ4 = E[u·r4] with r4 = m32 − m4, over the full natural population. Under the documented law, Δ4 = 0 for every suffix-only coordinate (tower property, Proposition 1).

**Unsupported rows.** Every row is kept. Supported rows score u·r4; unsupported rows contribute [−‖r4‖, +‖r4‖]. [E X−, E X+] is exactly the identified set of Δ4 over all completions (Theorem A).

**Chart.** K4b builds its own charts with the unchanged C1′ code on its own fresh landmarks (3 production + 3 direct comparators, plus 3 step-0 control charts; at most 9 constructions).

**Numerics.** K4's per-row Decimal certificate on every validation and test row (cap 1e-4), an exact-integer norm bracket, and C1′'s tree-mean bound B_num. The decision margin is F = max(B_num, 1e-9) + Z_bound, so the claims concern the documented law (Theorem B′).

**Gates.** Authority and window, identity, registry, separation, oracle, validation B4 > 0.01 (certified), C0-cal, C0-val, certificate, precision. The test size N ∈ {3,072, 6,144, 12,288} is chosen once from validation SDs plus a projected per-model and joint power check. Validation means stay sealed.

**Decision.** Per model: SUPPORT iff L(E X−) − F > 0.01; EXCLUDE iff U(E X+) + F < 0.01 and L(E X−) − F > −0.01 (one-sided bounds at 0.05/3; a false definite claim ≤ 2α per model, §8.3). SUPPORT or EXCLUSION overall requires all three models; otherwise MIXED or INCONCLUSIVE.

**Controls.** m4-phase and SHA-of-suffix nulls, step-0 charts, a descriptive suffix decoder, Δ1 and Δ2. Nothing is ever subtracted.

**Cost.** About 0.9–3.3 CPU-h of execution [W from H], measure-only.

---

## 0. Notation and conventions

| Symbol | Meaning |
|---|---|
| j ∈ {1729, 2718, 3141} | Model seed. Model maps are keyed by **int** seeds everywhere (the job-0039 R11 lesson) |
| h = (w1, …, w32) | A canonical 32-symbol history; S4 = (w29, …, w32) |
| c(z) | (cos 2πx/12, sin 2πx/12), x = coords[z, 0] |
| m_K(h) | Posterior mean of c(z32) given the last K observations, computed by the job-0014 kernel `oracle_profile.posterior_means` (restart at π, emit first, transitions between emissions) |
| r_K | m32 − m_K; r4 is the primary residual |
| B_K | E‖r_K‖ (oracle headroom); V_K = E‖r_K‖² |
| φ_j(h), u_j(h) | Gauged extension phase of model j's frozen production chart, and u_j = (cos φ_j, sin φ_j) |
| A_j(h) ∈ {0, 1} | Operational support flag of `extend` on the production chart (resultant ≥ 0.2 and 8th-NN distance ≤ R) |
| X−_j, X+_j | Bounded row scores (§1.4) |
| P*, P_op, Q | Documented generating law; the stored float arrays read as exact reals; the sampler law (EB §1, §6) |
| Z_bound | 2(ρ_κ − 1) + 4·TV(Q, P*), from `process_law.process_law_bound` (EB §6, §9) |
| B_num | C1′ Theorem 5 bound for a tree-mean bootstrap statistic (§5.4) |
| F | max(B_num, 1e-9) + Z_bound, per model and side (§5.5) |
| α | 0.05/3 per one-sided bound |
| L−_j, U+_j | Rank-84 order statistic of the 5,000 bootstrap tree means of X−_j; rank-4,917 order statistic of those of X+_j |
| K-REG1, K-REG2 | K4b exposure registry versions 1 and 2 (§3.4). Not to be confused with releases |
| Release A, release B | Coordinator releases for the calibration/validation stages and for the fresh test |
| R_ref, H_exec | Reviewed reference commit and pinned execution commit (§11.5) |

All statuses are `PASS`, `INCONCLUSIVE/<reason>` or `FAIL_TECHNICAL/<reason>`. The first non-PASS gate ends the cohort (§13).

---

## 1. Question, target, identities and the bounded estimand

### 1.1 Question (RQ title, RQ 1)

K4b asks whether a circular coordinate learned by the three E4 cylinder-O models carries first-harmonic information about the hidden x-position that the last four observations do not determine. It is a new study (addendum 3). It is not K4, not a rescue of K4 and not part of C1′; K4 stays INCONCLUSIVE at chart_calibration (job 0018). K4b results are never pooled with, or reported as, K4, C1′ or E4 results.

### 1.2 Target and the suffix-only zero identity

For model j, conditional on its frozen calibration chart and gauge,

  Δ4,j = E[ũ_j(h)·r4(h)],

over the full natural population of stationary 32-observation histories, where ũ_j = u_j on the supported set S_j; §1.4 makes the target well defined without assuming anything off S_j. There is no eligibility filter, prefix matching, residual cutoff, phase-bin selection or support conditioning. Landmark membership never defines the scored population.

**Proposition 1 (suffix-only zero; L§1 = X§2, AN §1.1).** Let P* be the documented stationary law (π* T* = π*, z1 ~ π*), with m4 and m32 computed under P*. For every bounded measurable g of S4 with values in ℝ², E_{P*}[g(S4)·r4] = 0.

*Proof.* (1) By stationarity z29 ~ π*, and conditional on z29 the variables (z29..32, w29..32) follow the HMM; so the filter restarted at π* at position 29 returns P*(z32 | S4) and m4 = E*[c(z32) | S4]. (2) m32 = E*[c(z32) | w1..32] and σ(S4) ⊂ σ(w1..32), so the tower property gives E*[m32 | S4] = m4 and E*[r4 | S4] = 0 a.s. (3) E*[g·r4] = E*[g·E*[r4 | S4]] = 0; integrability holds because ‖r4‖ ≤ 2 and g is bounded. ∎

**Consequences.**
- The identity is gauge-invariant: a rotation or reflection of a suffix-only field is suffix-only. The gauge cannot manufacture Δ4.
- It holds conditional on any independent calibration data: a chart, a gauge or a decoder fitted on calibration and then frozen is a fixed function on the test population.
- The m4-phase control, the SHA-of-suffix control and the frozen suffix decoder (§9) are suffix-only on the test population, so each has Δ4 = 0 under P*.
- |Δ4| ≤ B4 = E‖r4‖ ≤ 2 (Cauchy–Schwarz).

**Conditioning on support breaks the identity (L§1; AN §1.3).** Take S = {e1·r4 > 0} and the constant, suffix-only g ≡ e1. Then E[e1·r4 | S] > 0 and also E[1_S·e1·r4] > 0 whenever P(S) > 0. The support indicator depends on activations, hence on the whole history, so this is a real risk. K4b therefore never conditions on support. A supported-row mean, and the full-denominator supported contribution E[A·u·r4], appear only as labelled diagnostics that are **not null-protected** (§10).

### 1.3 Documented law, operational law and the sampler (X§2, MD 5)

The identity is exact only under P*. The run computes moments from the stored binary64 arrays (P_op) and samples with the actual sampler (law Q). EB §6 and §9 give, for the stored E4 arrays, κ < 1, ‖P_op − P_{P*}‖₁ ≤ ρ_κ − 1 with ρ_κ = ((1+κ)/(1−κ))^(2L+1), L = 32, and TV(Q, P*) bounded under the **idealised** sampler law (independent uniform 53-bit draws; deterministic PCG64 bias and correlation are not bounded). `process_law_bound` returns Z_bound = up(2(ρ_κ − 1) + 4·TV) on the 10⁻⁴⁰ grid. Job 0018 recorded Z_bound = 2.12e-12 for these arrays [H].

**Lemma T (transport; AN §1.1).** Let f(h, r) be any score that, for fixed h, is 1-Lipschitz in r ∈ ℝ² and satisfies |f(h, r)| ≤ ‖r‖. Let r_op and r_* be r4 computed under P_op and P*. Then |E_Q[f(h, r_op(h))] − E_{P*}[f(h, r_*(h))]| ≤ Z_bound.

*Proof.* |f(h, r_op) − f(h, r_*)| ≤ ‖r_op − r_*‖ ≤ ‖m32,op − m32,*‖ + ‖m4,op − m4,*‖. Each posterior-mean difference is at most ‖P_op − P*‖₁·max_s‖c_s‖ ≤ ρ − 1, because ‖c_s‖ = 1. For K = 4 the positive-path argument of EB §3(a)/§6 has 2·4 factors, so its bound ρ_4 − 1 ≤ ρ_32 − 1 (AN §1.1). This gives ≤ 2(ρ_κ − 1). Next, |E_Q f_* − E_{P*} f_*| ≤ 2·sup|f_*|·TV(Q, P*) ≤ 4·TV, because |f_*| ≤ ‖r_*‖ ≤ 2 and f depends on (z, w) only through w1..w32, whose TV is at most the path TV. Summing gives Z_bound. ∎

Every K4b row score is of this form, with u, the support flag and every chart quantity fixed functions of h after calibration: u·r for a unit vector u; −‖r‖ and +‖r‖ (reverse triangle inequality); and ‖r‖ for B4. So Lemma T applies to X−, X+, the controls and B4.

### 1.4 Rows without support: the bounded estimand (RQ 3; L§3; X§5)

For model j and row i:
- if A_j = 1: X−_j = X+_j = u_j·r4;
- if A_j = 0: X−_j = −‖r4‖ and X+_j = +‖r4‖.

The bounded estimand is [E X−_j, E X+_j]. Every sampled row is kept. No phase is assigned to an unsupported row in the primary analysis. A non-finite extension, a phase outside [0, 2π) or a conflicting exact duplicate is a defect (FAIL_TECHNICAL by the frozen taxonomy), never "unsupported".

**Theorem A (identification; L§3.2, verified AN §1.2).** Let S ⊆ Ω be the supported set, measurable and fixed once the chart is frozen, and u : S → S¹ the chart field. A **completion** is any random field ũ with ‖ũ‖ ≤ 1 and ũ = u on S. It may depend on h, on the hidden path or on auxiliary randomness ω′, in any measurable way. Let Δ4(ũ) = E[ũ·r4]. Then:
1. **Bound:** E X− ≤ Δ4(ũ) ≤ E X+ for every completion.
2. **Sharpness:** ũ = −r4/‖r4‖ on S^c ∩ {r4 ≠ 0} attains E X−, and ũ = +r4/‖r4‖ attains E X+ (the value on {r4 = 0} is arbitrary).
3. **No gaps:** every value in [E X−, E X+] is attained by a unit-valued completion.

So [E X−, E X+] is exactly the identified set of Δ4 when nothing is assumed off S.

*Proof.* (1) On S, ũ·r4 = u·r4 = X− = X+. On S^c, Cauchy–Schwarz gives |ũ·r4| ≤ ‖ũ‖‖r4‖ ≤ ‖r4‖, so X− ≤ ũ·r4 ≤ X+ pointwise for every ω′. All terms are bounded by 2; for randomised completions take the conditional expectation given h (Fubini), then the expectation; monotonicity and linearity give the bound. (2) Equality holds pointwise for the stated completions, which are measurable because r4 and {r4 ≠ 0} are. (3) Let R_θ be the rotation by θ and ũ_θ = R_θ(−r4/‖r4‖) on S^c ∩ {r4 ≠ 0}. Then ũ_θ·r4 = −cos θ·‖r4‖, so E[ũ_θ·r4] = E[X−·1_S] − cos θ·E[‖r4‖·1_{S^c}], which is continuous on [0, π] and runs from E X− to E X+. ∎

**Corollary A1 (no spurious rejection of the suffix null).** If u coincides on S with a unit-valued suffix-only field g(S4), then g is itself a completion, so E X− ≤ Δ4(g) ≤ E X+, and Δ4(g) = 0 under P* (Proposition 1). Hence, with Lemma T, E_{P*} X− > 0.01 implies that u is not equal on S (a.s.) to any unit-valued suffix-only field; more strongly, every completion has Δ4 > 0.01. This holds whatever the dependence of S on the prefix.

**Corollary A2 (uniform coverage).** The bracket X− ≤ ũ·r4 ≤ X+ is rowwise, so it holds for the sample mean of every completion and within every bootstrap draw. A lower confidence bound L for E X− satisfies P(L ≤ Δ4(ũ) for all ũ) ≥ P(L ≤ E X−). The SUPPORT claim concerns only the lower end of the identified set, so a one-sided test of H0: E X− ≤ 0.01 is the right test, with no Imbens–Manski adjustment. The two-sided EXCLUDE is an intersection–union of two one-sided tests (§8.3).

**Width.** E X+ − E X− = 2·E[(1 − A)‖r4‖]. Support fraction alone does not determine identification precision; the missing residual mass does. The width is reported (§10) and never gated (F5, ruled by RU: no width gate; RC14).

---

## 2. Authority, provenance, fixed objects and site

### 2.1 Authority and provenance bindings (MD 14 ⚑)

| Object | Binding |
|---|---|
| Addendum 3 (approval) | sha256 222578FE…38A4 |
| Addendum 10 (C1′ closed; this writer) | sha256 E28BDE0C…22A2 |
| Owner A2 (chart rule), v1 record | sha256 5BD1FDB0…37CD |
| Design proposal `docs/proposals/GAP_CLOSING_EXPERIMENTS_HE.md` §4 "H" | **Committed on main at 89b9bab5ef20f369a6104909bf24fb8f05531eba.** Blob sha256 `8b5c7049817696bb92221471cc26f0be437b6787caddb439a776d9f5a957f091` (git blob id 62268af62baf1b3e619ade30587d2299a3e8dd15). W verified it is unchanged at c460e24 and equal to the working-tree hash L recorded |
| K4 draft `docs/proposals/CIRCULAR_HISTORY_K4_PROTOCOL_DRAFT.md` | sha256 42FB2E9F…E0FA (at c460e24) |
| C1′ protocol `tools/c1prime/PROTOCOL_C1PRIME_v1.md` | sha256 0B1F107E…F33A (identical at c460e24 and 93350d7) |
| Request | sha256 ECDFA7C4…A162 |
| This protocol | sha256 in `K4B-MERGED-v1.sha256`; the frozen version's hash is bound in the freeze record |

**Scope of the C1′ sentence.** C1′ §14 says "A K4b would re-run the frozen K4 protocol with this chart rule". That sentence is descriptive. Its normative parts are kept: a separate opt-in, protocol, seed scope, review and freeze; C1′ never loads a K4b object; C1′ histories are never K4b inputs.

### 2.2 Fixed objects (no training, no site search)

| Model seed | Checkpoint, step 5000 | Checkpoint, step 0 (initialisation control) | EmissionSpec |
|---|---|---|---|
| 1729 | c3358e3cb9c352fb | bd8813115bbd970b | 3633ac27dab50cf4 |
| 2718 | 98b0e703a337d513 | 5e6e6b7c446907f9 | 97838b9e13a26f74 |
| 3141 | 036b670743ffbbaf | 995f11b1120ccb36 | 8c29c329c197c79e |

Shared: WorldSpec 21feee1d8ee5422e (12×12 cylinder, axis 0 periodic), TransitionSpec e4dafc7b9785c172 (lazy max-degree walk, uniform π), overlap emissions with σ = 1.25 and 36 symbols.

W read the six `meta.json` files (metadata only): each step-5000 and step-0 pair has the same run_key [cylinder, O, seed], steps 5000 and 0, status complete, and the same `seed_map["init/cylinder/O/<seed>"]` (1729: 1959191081547677733; 2718: 1650155370212577495; 3141: 7028749409156379047). H1 re-verifies these at run time, together with the payload hashes (§6).

**Site.** Input `[BOS = 36, named w1..w32]`, hook `resid_post_3`, index 32, dimension 128. Evaluation uses `c1_model.load_model64` and `c1_model.activations`, unchanged: the exact float64 cast of the frozen float32 weights, verified by round trip. The float32 state sha256 is recorded before and after every stage. Logits are discarded unread. w33 is never stored or read; no latent-state sidecar is created.

**Symbols.** E_canon = `oracle_profile.canonical_emission(E_named_j, perm_j)`; named = perm_j[canonical]. The canonical digest is the sha256 of the uint8 w1..w32 (`scores.history_digests`). All oracle work is canonical and shared across models, which is permitted only if the three E_canon arrays are bitwise identical (H1; C1′ H1 passed this check).

---

## 3. Histories, splits, seeds, exposure registry and window

### 3.1 Splits and fixed blocks (MD 3)

Each block is drawn by one call `HMMSampler(T, E_canon, π, SequenceLayout()).sample(3072, rng)` with rng = `SeedTree(0).generator("data", "k4b-sf-v1", split, block, "cylinder", "overlap", "1.25")`. Column w33 and the latent states are dropped in memory at once. Sequence IDs: `make_sequence_ids(process_code("cylinder", "overlap", "1.25", f"k4b-sf-v1/{split}/b{block}"), "test", 3072)`. Rows are ordered by ascending sequence_id; landmark IDs are 20-digit zero-padded sequence_id strings (`c1_chart.landmark_ids`).

Blocks are fixed 3,072-row streams, because a sample of size n is not a prefix of a sample of size 2n. The ladder changes only how many test blocks are drawn, never the content of a block.

| Split | Blocks | Rows | Use |
|---|---|---|---|
| Calibration | cal b0 | 3,072 | Production landmarks = the 512 lowest sequence_ids. Gauge on m32 of the charted landmarks. Step-0 control charts on the same 512 landmarks. The descriptive suffix decoder on the 2,560 non-landmark rows (§9.4). Four lowest-ID rows get Decimal references. No certified decision |
| Validation | val b0 | 3,072 | Direct comparator = the 512 lowest sequence_ids, with the C0-val criteria on them. B4 gate, row certificate and precision on all 3,072 rows. Endpoint-bearing means sealed (§7.5) |
| Fresh test | test b0 … b(k−1), k ∈ {1, 2, 4} | 3,072·k | The single endpoint. Sampled only under release B |

**Population.** Every sampled row is in the population. No eligibility filter, trimming, replacement or complete-case analysis. Rows are independent stationary trajectories. Within-split duplicate histories are legitimate independent draws: they are kept and counted. The bootstrap resamples whole rows with one index stream shared by all models and arrays.

### 3.2 Seeds

| Seed | Use |
|---|---|
| `SeedTree(0)` scope `("data", "k4b-sf-v1", split, block, "cylinder", "overlap", "1.25")` | History blocks |
| PCG64 610101 | Validation SD draws (`precision.sd_b4_draws`, the same seed for X− and X+, so one index stream) |
| PCG64 610102 | Validation B4 tree-mean draws |
| PCG64 610103 | Fresh endpoint: one joint stream for X±, controls, step-0 arrays, decoder, Δ1, Δ2, Δ4^orc |
| PCG64 610104 | Fresh B4 (report only, MD 9) |
| PCG64 610105 | Validation centred projection (`precision.centered_draws`), the same seed for every candidate N (C1-FROZEN-v1 precedent; [W] addition, F10) |
| `SeedTree(0).generator("k4b-sf-v1", "suffix_rbf_bw", j)` and `("k4b-sf-v1", "suffix_rbf", j)` | Decoder bandwidth subsample and random-feature map (§9.4) |

Scope `k4b-sf-v1` and seeds 610101–610105 are frozen. G0 verifies that they have no prior scientific issuance, by the classification rule of §6 row 0 (RC5); K4b's own specifications, constants, synthetic tests and authorised regeneration in this lineage are expected declarations, not prior use.

### 3.3 Exposure: histories, not weights (L§0.4)

The three models have been analysed by E4, the circular audit, X4-F, K4, the chart diagnostic and C1′; the E4 finding motivated K4b. Freshness here is a property of histories. All K4b inference is conditional on the three fixed weight sets, the frozen charts and the gauges.

### 3.4 Exposure registry (MD 2, MD 10 ⚑)

The registry is a set of canonical 32-symbol digests, built with identity-only access through the unchanged `c1_data.build_registry` (token arrays → digests) plus, for sources that already store digests, a direct union of the stored digest columns. K4b reads token arrays and identity columns only; no scored diagnostic, activation, chart, oracle array or endpoint of any other study is read.

**Sources of K-REG1** (frozen before any K4b sampling):
- **(a) E4.** Every ObservationSet in `topo-pilot/artifacts`, canonicalised with its own EmissionSpec perm: `c1_registry_sources.observation_set_sources()`, unchanged.
- **(b) Earlier stores.** `c1_registry_sources.store_sources()`, unchanged: the X4-B2 pools, `x4-history-feas-store` calibration/validation, the K4 job-0015 oracle tables and its K = 32 reference cache, and the recorded empty-with-reason entries (x4b, job 0014, X4-F, D-1, chart diagnostic, X2a).
- **(c) Handoff.** `c1_registry_sources.handoff_sources()`, unchanged: every JSON under `agent-handoff` scanned for 32/33-element integer lists.
- **(d) C1′ (MD 2).** (d1) the digest list of `c1prime-store/registry/registry_v1.json` (job 0027; sha256 ebcebe18…7d9e per its review); (d2) the `digest_H`, `digest_Hp` and `digest_Hm` columns of every `HIST_*.npz` in `c1prime-store`, including `superseded/`. These are identity columns. C1′ never sampled its fresh test (U1), so these are all C1′ histories and donors.
- **(e) D-2a.** Cover all 19 pools. Read token identities only from pools whose frozen access rules permit that access. Do not open test or testN tokens under this protocol.

  The sealed pools are covered conservatively by the predicate \(H\in\{0,1,2,3,4\}^{32}\), using D-2a’s bound five-symbol identity alphabet. Before any K4b activation or endpoint calculation, every K4b history must fail that predicate. A history satisfying it yields INCONCLUSIVE/REGISTRY_INCOMPLETE, with reason “potential overlap with sealed D-2a histories”; it is neither removed nor replaced. This proves disjointness from every sealed D-2a history whenever the check passes.

  Bind the pool metadata and permitted integrity records. Derive sealed-pool sequence-ID ranges from the frozen pool configuration and sequence-ID rule without reading token arrays. Any unresolved alphabet, pool inventory or sequence-ID identity stops registry completion.

  These restrictions apply to every generic store reader as well as the D-2a-specific reader. Reading sealed tokens instead requires an explicit owner-authorised exception bound before access. (RC6; MD 10 ⚑; F3 ruled by RU.) The permitted D-2a pools are read as raw `tokens[:, :32]` uint8 (identity alphabet, no canonicalisation). The predicate check runs in H2 (cal, val) and H2-FRESH (test), on every row, before any activation of those rows. W checked read-only that the derivation is possible: `tools/d2a/API.md` (at c460e24) fixes `sequence_id = SEQ_CODE[pool]·2³² + arange(n)` with SEQ_CODE 1..19 in POOLS order (test = 17, testN = 19), and `pools.json` records each pool's n, so the sealed ranges follow from metadata alone.
- **(f) Every other directory under `X:/Downloads/projects/topo-pilot` present at the freeze.** Each is either scanned (any ObservationSet store with a raw-token reader, plus the canonicalised digest when an EmissionSpec perm resolves; this covers the X5 stores that C1′ v1 listed as not scanned) or listed as NOT_SCANNED with a recorded reason backed by the recursive inventory below (no history-bearing file, identity reference or ObservationSet root found; or synthetic test fixtures only). A directory's being a worktree, a temporary directory or "not an ObservationSet" is not by itself evidence of absence (RC7). The manifest classifies every directory (F4, ruled by RU: RC7).

Readers that are not in `c1_registry_sources` (d2, e, f) are new K4b code (`k4b_registry.py`, §11.1). The manifest binds every scanned file by content hash, with canonicalisation metadata, as C1′ §2.4 requires; a filename listing alone is insufficient. An unreadable source makes the registry INCONCLUSIVE/REGISTRY_INCOMPLETE. The coordinator certifies completeness in release A.

**Fail-closed completeness (RC7).**

Registry completion requires a recursive inventory of history-bearing files, identity references and ObservationSet roots within every classified project directory, including worktrees, superseded attempts and temporary directories containing scientific histories. “Worktree”, “temporary” or “not an ObservationSet” is not sufficient evidence of absence.

Before invoking an unchanged handoff reader, independently validate its JSON input. A parse failure is INCONCLUSIVE/REGISTRY_INCOMPLETE; it must not become an empty contribution.

Revalidate every empty-with-reason identity source against scanned histories. Reuse c1_registry_sources.history_index_ids(store=None, root=ART) and coverage(seqs_a, hist_ids, root=ROOT), supplemented where necessary for the expanded inventory. Every referenced history or sequence ID must resolve to a covered source. Missing references fail registry completion.

When observation_set_sources is used for a non-default artifact root, pass an ArtifactStore backed by that same root explicitly; changing root alone does not change its default store. Sources lacking resolvable EmissionSpec metadata require a documented appropriate identity reader.

Freeze the complete digest union, conservative membership predicates, sequence-ID union, source hashes, canonicalisation records and coverage results. Unknown or unreadable history-bearing sources are incomplete, not NOT_SCANNED.

(W verified at c460e24: `handoff_sources`' reader returns `EMPTY` on `ValueError`; `observation_set_sources(store=None, root=ART)` builds its default store from the module constant `ART` whatever `root` is passed; `coverage` reads the x4b, X4-F, chart-diagnostic, x4-history-feas and job-0014 identity files under its `root`. These are the hazards the paragraphs above close; the reused functions are not edited.)

**K-REG2** is rebuilt from scratch, by an identity-only step after the coordinator ACCEPTs the validation report, inside the W2 reservation, and before release B. It includes every source existing then, plus K4b's own cal b0 and val b0 histories. Release B binds its sha256, its source inventory and the reservation (§3.5).

**Requirements.** U_s is the set of natural histories of split s; K4b constructs no donors. Calibration and validation require U_cal ∩ K-REG1 = ∅, U_val ∩ K-REG1 = ∅ and U_cal ∩ U_val = ∅ (`c1_data.separation`, unchanged). The fresh test requires U_test ∩ K-REG2 = ∅. K4b sequence IDs must be disjoint across all K4b blocks and from the sequence-id union frozen with the registry, including the derived sealed D-2a ranges (`dataset.checks.check_disjoint`). A collision is FAIL_TECHNICAL/LINEAGE, with no replacement sampling. Every K4b history must also fail every frozen conservative membership predicate (today: the sealed-D-2a predicate H ∈ {0,…,4}³² of source (e)); a history satisfying one is INCONCLUSIVE/REGISTRY_INCOMPLETE (RC6), never removed or replaced. Collisions between independently seeded 32-symbol histories are improbable, so a collision is a lineage alarm; it does not prove a seed defect (C1′ §2.4).

### 3.5 The registry window (MD 10 ⚑; AN D5; X's refresh rule)

- **W1, precondition (G0).** K4b samples nothing until C1′ and D-2a are terminal. **Both are met as of this writing** (U1, U2). G0 records the evidence: addendum 10, jobs/0044/review.md, jobs/0033/review.md and main commit 4bc0b16, each by hash. The queue order of MD 10 (C1′ data stages, then D-2a, then K4b) is thereby satisfied.
- **W2, registry-to-draw exclusion.** Rebuild K-REG2 from scratch before release B. The coordinator reserves an exclusive scientific-history-generation window from the start of the final registry rebuild through completion of every released test block. Release B binds the registry, its source inventory, the reservation and N. Immediately before sampling, verify that the reservation remains valid and no other scientific history generation occurred.

  If external generation occurs before the first test row, cancel the release, rebuild and re-freeze K-REG2, and issue a new release before sampling. If it occurs after test sampling has begun, stop for lineage review; do not rebuild around a partly exposed test or draw replacement data.

  Apply the same registry-to-draw protection to K-REG1 through completion of cal b0 and val b0. Retain within-split duplicates. (RC8; X's refresh rule.)
- **W3, no blind spot in another study.** K4b samples nothing while another study holds a frozen registry, awaiting a fresh draw, that would not include K4b's stores. Release A and release B record the coordinator's attestation. Known candidates today: X6 stage 0 (oracle-only Monte Carlo on its own process; not frozen) and the R1 replication of E4 (queued after K4b). Whichever of them generates histories before a K4b registry freeze enters that registry through (f); any later study's registry must include `k4b-store`.

  The coordinator’s exclusion also covers activation of another study’s incompatible frozen-registry window while K4b’s reservation is live. Record the reservation’s start, end, relevant job states and any interruption. Attestations without this enforced scheduling constraint do not establish completeness of the window. (RC8; F16 ruled by RU.)

---

## 4. The chart (MD 2; RQ 2)

### 4.1 K4b builds its own charts

1. **The frozen text forbids reuse.** C1′ §14: "C1′ never loads a K4b chart, and C1′ histories are never K4b inputs". The C1′ production chart is made of C1′ calibration activations, and its gauge is fitted to their m32; loading it would make C1′ histories K4b inputs. C1′ §19 rule 10 forbids pooling.
2. **Independence.** With its own chart, K4b's validity rests only on K4b's gates on K4b's histories. Neither study's estimand is conditional on the other's instrument.
3. **Owner wording.** Addendum 3: the C1′ chart rule "on fresh histories". K4b's own histories are the fresh ones.
4. **Cost.** Six 512-point PH runs took about 2.5 CPU s (job 0023 [H]); one lift took 0.03 s (job 0018 [H]).

| Shared with C1′, unchanged and hash-bound | Never shared |
|---|---|
| The rule (C1′ §14) and its code: `c1_chart`, `c1_model`, `c1_means`, `c1_bounds`, `c1_cert`, `c1_records`, `c1_data` (registry functions only), `c1_config`, `c1_oracle` (transitive import), and the K4 kernels they call | Any C1′ chart, gauge, decoder, activation, oracle array, gate value, seed or history. C1′ digests enter only the K4b registry. No K4b object enters C1′ |

### 4.2 Construction (C1′ §14 steps 1–10, through the unchanged code)

`c1_chart.fit_chart_lcc(X, ids, cfg, guard, timed, persist)` with cfg = `c1_config.chart_cfg(K4B_CONTRACT)`:
- PH over F47 on all 512 landmarks; the largest strictly positive finite H1 bar (ties by birth, death, index); r = (b + d)/2; edges D ≤ r;
- connected components; C* the largest (ties to the smallest landmark index); GIANT passes iff 100·m ≥ 95·512 in integers (m ≥ 487; 0.95·512 = 486.4 [W]); the pre-raise record is persisted before any failure;
- restriction to C* without recomputing persistence or changing r; the exact integer lift (bounds [1, 2, 4, 8, 16], node limit 128, rounding tolerance 1e-7, two local passes over ≤ 128 vertices), primitive class (g ≠ 0, 47 ∤ g, BFS root = lowest ID in C*), smoothing (residual ≤ 1e-8); d8, σ = median d8 and R = 2·q0.99(d8) (`inverted_cdf`) over D[np.ix_(C*, C*)];
- the gauge `fit_production_gauge(ch, m32[C*])` (= `chart.fit_gauge`): reflection then rotation to arg m32, sign +1 on a tie, alignment finite and > 0;
- extension `chart.extend`: 8 nearest charted landmarks, Gaussian weights with σ, stable ordering, exact-duplicate rule with 1e-8 conflict tolerance, support iff resultant ≥ 0.2 and 8th-NN distance ≤ R;
- `lift_cpu_cap_s` = null (decoded to +inf; owner resource override); `native_operation_wall_s` = 600.

**Contract equality (correction C2 of §16.2).** The K4b CONTRACT chart section must make `c1_config.chart_cfg(K4B_CONTRACT)` equal, key for key and value for value, to `c1_config.chart_cfg(C1PRIME_CONTRACT)`, and its `giant` and `val_support` entries must equal C1′'s. These are the parameters that reach the kernels and the gates. The descriptive C1′ keys (`landmarks`, `construction_plan`, `support_rule`, `max_chart_constructions` = 6) are rewritten for K4b. L's "equal key for key" is not literally satisfiable, because K4b has nine constructions and its own landmark source. W verified that the C1′ CONTRACT chart section is identical at c460e24 and 93350d7 (the files differ only in `resources.worker_session`).

**Inputs per model.** Production landmarks: the 512 lowest sequence_ids of cal b0. Direct comparator: the 512 lowest sequence_ids of val b0 (ungauged; serialised with `c1_chart.IDENTITY_CARRIER`; role "validation_only"; used for fidelity only). Activations are float64 from `c1_model`.

**Order (no peeking).** Calibration activations, then C0-cal for every model. The production chart, gauge, membership, decoder and artifact hashes are serialised (`c1_chart.serialise`) and frozen before any validation activation is computed. Then validation activations, the direct charts and C0-val.

**C0-val** = `c1_chart.c0_val(prod, gauge, val_X, direct, cfg)`, unchanged: support 100·n_sup ≥ 99·512 (≥ 507; 0.99·512 = 506.88 [W]); fidelity ≥ 0.80 on the direct chart's C*_val rows, unmasked; every one of 12 bins ≥ 8 over all 512 rows; overall resultant ≤ 0.30 over all 512 rows. `chart_gates` is not called.

### 4.3 Construction ledgers (MD 8)

- **Trained ledger** `k4b-store/CHART_CONSTRUCTIONS_trained.json`: `c1_chart.ConstructionLedger`, unchanged, MAX 6 (3 production, 3 direct).
- **Step-0 ledger** `k4b-store/CHART_CONSTRUCTIONS_init.json`: the same class on a second file. The K4b wrapper refuses role "direct" on it, so it holds at most three claims, one production per model (the class forbids a repeated (model, role) pair).
- Total at most **nine** constructions. Each is attempted once and never retried. No substitution of component, bar, scale, landmark set, field, chart family or site, and no refit. No test persistence and no test chart.

### 4.4 Failure taxonomy (C1′ §14, unchanged)

An unmet criterion or unresolved construction is INCONCLUSIVE/CHART_UNAVAILABLE. This includes GIANT, the four C0-val criteria, Unresolved from the kernels, and the two chart-specific Invalid cases mapped by `c1_records.adapt_chart_exception`: (1) Invalid("not a cocycle mod p") from `integer_lift` (float32/float64 filtration boundary); (2) Invalid from `smooth_phase` with finite f and a finite residual > 1e-8. Non-finite f or residual, unavailable diagnostics, conflicting duplicates, invalid inputs, hash, lineage and certificate defects are FAIL_TECHNICAL (`c1_records.classify_exception`). Diagnostics come from the original invocation; a failed construction is never rerun.

### 4.5 What K4b inherits from C1′'s chart (MD 11 ⚑; U1)

MD 11 planned for C1′'s chart failing. It did not. What K4b inherits is limited to this:
- The LCC rule, through the same code, **passed C0-cal on C1′'s own unexposed calibration histories** in all three models (\|C*\| = 512/512, one component, no excluded landmark, `centered_exact` lift, g = 1, residuals 2.1e-12 to 2.7e-12, gauge alignment 0.894 to 0.899; jobs 0042 and 0044 [H]). The shared chart code raised no exception there.
- C1′ never reached C0-val. Nothing is known about support, fidelity, bins or resultant on unexposed validation data.
- No claim beyond this is inherited. In particular, C1′'s pass is not evidence that K4b's charts will pass, and K4b's gates are evaluated on K4b's histories alone.

**Consequences.** MD 11's licence qualifier ("the same rule failed its C1′ gates on other fresh histories") is not triggered. MD 11's stop branch (FAIL_TECHNICAL in shared chart code) did not occur. Every K4b report and the freeze record carry a disclosure instead: "C1′ ended INCONCLUSIVE/FAMILY_UNMATCHED at S4 M2-cal; its LCC charts passed C0-cal in all three models; C0-val was not reached. No K4b parameter was changed in response." Any K4b change in response to a C1′ outcome would be a new protocol version with its own review.

**Evidence status of the rule.** The LCC rule was fixed after K4's chart failure; its feasibility was checked on exposed E4 geometry (job 0023: no phases, labels or fitting) and its calibration step on C1′'s calibration histories. K4b's C0-cal and C0-val are an independent test of the rule on K4b's own unexposed histories, and the first validation-stage test of it.

---

## 5. Numerics (MD 4, MD 5; RQ 4)

### 5.1 Exact-arithmetic counterpart

For each certified quantity, the target is the same formula evaluated in exact real arithmetic on the same inputs: T, E_canon and π read as exact reals (P_op, EB §1); the float64 phases φ̂ read as exact reals (the saved phase defines the coordinate); the operational support flags; the same bootstrap index draws and the same order-statistic ranks.

### 5.2 Row level (K4 machinery, unchanged)

Per validation or test row:
1. Decimal reference moments M̃_K for K ∈ {1, 2, 4, 32} by `error_bound.reference_moments(T, E, pi, coords, canonical32, Ks, cache, cache_only)` (60-digit posterior, 80-digit features, trapping context, flags checked). Cache key: process digest, K and the history bytes.
2. **Moment check:** |m̂_K − M̃_K| ≤ 1e-10 for every K and row, compared exactly with Fractions against `error_bound.MOMENT_TOL_EXACT`. K4b implements this comparison itself in three lines over the public `reference_moments`. It does not call `reference_check_rows` or `certify_rows`, whose test ("scoring") path requires K4's own ScoringAuthority (L's catch, confirmed by W at c460e24).
3. **Phase-defined score** x̂ = `scores.scores(scores.unit_vectors(φ̂), m̂32, m̂K)`: B = `error_bound.row_bound(x̂, φ̂, M̃_K, M̃32, ε_K, ε32)["B"]`, with ε_K = `moment_envelope(posterior_envelope(K, 144), 144)`. This is K4's proved B = Δ + E_ref (EB §2–3), compared exactly. `row_bound` is generic in the suffix length, because EB §3(e) uses only the two envelopes.

### 5.3 Lemma N, the norm bracket (X's integer bracket with L's constant; AN §1.4)

Let r̃ = M̃32 − M̃4 ∈ ℚ² exactly, s = r̃x² + r̃y² = a/b ∈ ℚ exactly, D = 10⁸⁰ and k = isqrt(⌊a·D²/b⌋). Let n̂ be the float ‖r4‖ (`scores.r4_norms`) read exactly. Define

  B_N := max(|n̂ − k/D|, |n̂ − (k+1)/D|) + (3/2)(ε4 + ε32).

**Lemma N.** |n̂ − ‖r*‖| ≤ B_N, where r* = M*32 − M*4 under P_op in exact arithmetic.

*Proof.* k² ≤ ⌊aD²/b⌋ ≤ aD²/b, so (k/D)² ≤ s; (k+1)² > ⌊aD²/b⌋ implies (k+1)² ≥ ⌊aD²/b⌋ + 1 > aD²/b, so ((k+1)/D)² > s. Hence ‖r̃‖ = √s ∈ [k/D, (k+1)/D] and |n̂ − ‖r̃‖| ≤ max(|n̂ − k/D|, |n̂ − (k+1)/D|). By the reverse triangle inequality, |‖r̃‖ − ‖r*‖| ≤ ‖r̃ − r*‖₂ ≤ √2·max_coord |r̃ − r*| ≤ √2(ε32 + ε4) (EB §3(c), (e)), and √2 ≈ 1.414214 < 3/2 [W]. ∎

s = 0 gives k = 0 and the bracket [0, 10⁻⁸⁰]. Everything is integer or Fraction arithmetic; no square root is trusted.

**Row bound per array.** For X−_j and X+_j: B_{j,i} = row_bound's B on supported rows and B_N on unsupported rows (X∓ = ∓n̂ is exact in float). For B4: B_N on every row. For a control or descriptive phase score: row_bound's B. **Cap:** every primary B ≤ 1e-4, compared exactly; every row is certified, not a sample (the proved all-row bound, RQ 4). **P2 analogue:** every X̂ finite with |X̂| ≤ 4, else FAIL_TECHNICAL/NUMERICAL.

### 5.4 Mean level (C1′ machinery, unchanged; MD 4)

- Every certified mean is `c1_means.tree_mean`; the bootstrap is `c1_means.bootstrap_means(arrays, seed, draws=5000)`: one `rng.integers(0, n, size=n)` per draw, shared by every array.
- **C1′ Theorem 5** (balanced-tree mean; general in n, with d_n = ⌈log₂ n⌉ levels; AN §1.5) and **Lemma L4** (same-rank order statistics are 1-Lipschitz in the sup norm) give, for every draw and every rank, |m̂ − m*| ≤ B_num and |q̂ − q*| ≤ B_num, with
  B_num = `c1_bounds.B_constant(max_i B_i, max_i |X̂_i|, n)` = OUT(max_i B_i) + γ_{d_n+1}·max|X̂| + ζ, OUT(x) = (1 + 2⁻³⁰)x + 2⁻⁸⁰⁰, ζ = 2⁻⁸⁰⁰, max_i B_i passed as an exact rational.
- Ranks for 5,000 draws by `c1_means.quantile_with_rank`, with its run-time rank check: 84 for α = 0.05/3 (`P_THIRD` = 5/300; 5000·5/300 = 83.33 → 84 [W]); 4,917 for 1 − α (5000·295/300 = 4916.67 → 4917 [W]); 250 for 0.05; 125 and 4,875 for the central 95%.

### 5.5 Decision margin and Theorem B′ (MD 5)

Per model j and side s ∈ {−, +}:

  F_{j,s} = max(B_num,j,s, 10⁻⁹) + Z_bound,

in exact rationals, with Z_bound the exact upper value returned by `process_law_bound` at H1.

**Theorem B′ (decision soundness, with transport).** Assume A1 (IEEE elementwise arithmetic; `c1_cert.a1_selftest` passes), A3 (libmpdec correctly rounded, traps enabled), A4 (exact Fraction and int arithmetic), the idealised sampler law of EB §9 item 7, and that the moment checks, the cap, the P2 analogue and the rank checks pass. Let L*−_j be the rank-84 order statistic of the exact-arithmetic (P_op) bootstrap means of X−_j over the same draws, and U*+_j the rank-4,917 one of X+_j. Let μ_{P*}(X) = E_{P*}[X computed with r_*]. Then:
1. |L̂−_j − L*−_j| ≤ B_num,j,− and |Û+_j − U*+_j| ≤ B_num,j,+.
2. On the event {L*−_j ≤ E_Q[X*−_j]}, L̂−_j − F_{j,−} ≤ μ_{P*}(X−_j); on {U*+_j ≥ E_Q[X*+_j]}, Û+_j + F_{j,+} ≥ μ_{P*}(X+_j). The transported bounds therefore have coverage at least as large as the actual coverage of the corresponding exact-arithmetic bootstrap bounds for their sampler-law expectations. Those actual coverages are approximated nominally by the percentile-bootstrap procedure; numerical certification does not prove nominal statistical coverage.
3. Hence: (i) L̂−_j − F > 0.01 implies L*−_j − Z_bound > 0.01; (ii) Û+_j + F < 0.01 implies U*+_j + Z_bound < 0.01; (iii) L̂−_j − F > −0.01 implies L*−_j − Z_bound > −0.01. Thus every reported SUPPORT_j or EXCLUDE_j is supported by the corresponding exact-arithmetic, transport-adjusted inequalities. The converse need not hold: the numerical allowance may turn an exact-arithmetic definite result into UNRESOLVED.
4. The B4 guard `c1_bounds.guard_H5(lower, B^H + Z_bound)`, unchanged, PASSes only if the exact lower bound minus Z_bound exceeds 0.01, and returns HEADROOM only if the exact lower bound plus Z_bound is ≤ 0.01. HEADROOM establishes failure of the registered lower-bound gate; it does not establish that the population B4 is at most 0.01.

*Proof.* (1) C1′ Theorem 5 bounds each draw's mean error by B_num, and L4 transfers this to the same-rank order statistic; the rank check verifies that the computed order statistic has the registered rank. (2) By Lemma T, μ_{P*}(X) ≥ E_Q[X*] − Z_bound, and by (1) and F ≥ B_num + Z_bound, L̂ − F ≤ L* − Z_bound ≤ E_Q[X*] − Z_bound ≤ μ_{P*}(X) on the stated event; the upper side is symmetric. (3) The strict inequalities transfer with margin. (4) This is C1′ Theorem 6(H) with B^H replaced by B^H + Z_bound, which dominates the arithmetic error plus the transport term; `guard_H5` takes max(B, 10⁻⁹) internally. ∎

**Mutual exclusivity.** X− ≤ X+ rowwise; float addition is monotone, so every draw's tree mean satisfies m̂(X−) ≤ m̂(X+), and the rank-84 statistic of X− is ≤ the rank-84 statistic of X+ ≤ its rank-4,917 statistic. So L̂−_j ≤ Û+_j. SUPPORT_j needs L̂− > 0.01 and EXCLUDE_j needs Û+ < 0.01, so they cannot both hold (AN §1.5).

**Certified, and not certified.**
- **Certified:** the stated error enclosures for the fixed operational coordinate and support rule, the means and same-rank quantiles, and the conservative arithmetic implications used by SUPPORT, EXCLUDE and the B4 guard. Lemma T transports expectations to P* under the stated idealised sampler assumption. Neither exact statistical coverage nor equivalence with an unguarded exact-arithmetic decision is certified.
- **Operational, not certified:** activations and forward passes; the chart (PH, lift, smoothing, gauge, extension); the support flags; the precision ladder; the suffix decoder; PCG64's deviation from the idealised law. An operational perturbation changes which valid quantity is assessed, never the validity of a certified decision about it.
- **Statistical:** the bootstrap percentile bounds are nominal approximations, conditional on the weights, the charts and the gauges. Numerical certification does not make their coverage exact.
- **Expected magnitudes [H].** Float discrepancies of 1e-16 to 1e-15 and E_ref about 1e-54 give B_num about 1e-15, so the 1e-9 floor binds; with Z_bound ≈ 2e-12, F ≈ 1.002e-9. The 1e-4 cap is a cap, not an expected value.

### 5.6 Tolerance attainability, fixed before data (the R13 lesson)

C1′'s M1 tolerance of 1e-10 for a cho_solve versus lstsq comparison was not attainable at κ ≈ 1e9 (job 0042), and the change after data needed retroactive owner ratification (addendum 10). Every K4b numerical identity and its tolerance is listed here, with the reason it is attainable. **No K4b gate compares two linear solvers.**

| Identity | Tolerance | Why attainable | Evidence [H] |
|---|---|---|---|
| Moment check m̂_K vs M̃_K | 1e-10, exact comparison | A forward recursion over a 144-state posterior with positive entries; normalised at each step; expected 1e-16 to 1e-15 | job 0018: gaps ≤ 8e-16 (1,024 histories × 3 K); job 0014: 4.4e-16 |
| Float64 round trip of each checkpoint | bitwise | float32 → float64 → float32 is exact | C1′ M0 PASS |
| E_canon equal across models | bitwise | the same array permuted by the model's perm | C1′ H1 PASS |
| Landmark-activation determinism (T-PRE) | bitwise | the identical call: the same 3,072 cal b0 inputs in the same order, `activations(model64, inputs, batch=1024)`, one thread, same environment | C1′ R14: three production charts regenerated bit-identically across separate runs (jobs 0042 → 0044) |
| Row certificate | B ≤ 1e-4 | expected B ≈ 1e-15 | K4 EB; job 0018 |
| Lemma N, rank checks, guards, decisions | exact | integer or Fraction arithmetic | — |
| Chart smoothing residual | ≤ 1e-8 (inherited gate) | — | C1′: 2.1e-12 to 2.7e-12 |
| Suffix decoder: RidgeProbe vs `nested_ridge` predictions | max(1e-10, 64·ε·κ₂(Xc′Xc + λ*I)·‖pred‖∞) (the R13 formula, fixed now) | **Descriptive only; never a gate.** A failure makes the decoder "UNAVAILABLE (equivalence)" | job 0044: κ up to 2.8e9, tolerances ≥ 4.85e-8 |

No threshold or tolerance changes after any K4b data exist. If a frozen technical tolerance proves unattainable, the gate's status stands (FAIL_TECHNICAL), and any change needs an owner decision (C1′ §19.3, §19.8; addendum 10), never a coordinator ruling alone (F13, adopted by RU).

---

## 6. Gates, in exact evaluation order (RQ 4)

The first non-PASS ends the cohort; later gates are NOT_RUN. Exceptions map through `c1_records.classify_exception` (and `adapt_chart_exception` inside chart gates), unchanged; `dataset.checks` SPLIT_OVERLAP maps to FAIL_TECHNICAL/LINEAGE. Resource exhaustion is INCONCLUSIVE/RESOURCE: CPU is measure-only and never stops the run, but the 600 s native-operation wall, the memory limit and the disk safe-STOP do.

| # | Stage | Gate | Criterion (numeric) | Status on failure |
|---|---|---|---|---|
| S0 | dispatch | BINDING | Protocol frozen, its sha256 = the freeze record; request sha256 = ECDFA7C4…A162; R_ref → H_exec diff over the protected paths contains only allowlisted `A` entries (§11.5); every reused file's sha256 = §11.3 table; C1′ CONTRACT chart section at H_exec = at R_ref; the GAP doc blob at H_exec = 8b5c7049…f091 | INVALID: do not run |
| PF | dispatch | PREFLIGHT | The unchanged regression suites and the new `tests/k4b` pass; `tools/check_file_sizes.py` (every .py ≤ 400 lines); `tempfile.gettempdir()` inside a metered child is on X: (§11.7) | INVALID |
| 0 | release A | G0 AUTHORITY AND WINDOW | Addendum 3, addendum 10, the A2 v1 record bound by hash; window W1 evidence recorded (C1′ and D-2a terminal); W3 attestation and the K-REG1 reservation (§3.5) present in release A; scope and seeds (RC5): No prior scientific issuance of the registered K4b data streams or seeds is present in another cohort’s seed maps, generation manifests or execution records. Searches cover the execution tree, planning records and historical cohort records. Current K4b specifications, implementation constants, independent synthetic tests and authorised deterministic regeneration in this lineage are expected declarations and are not prior scientific issuance. Text search is a discovery aid, not by itself the pass/fail definition. Record every hit and its classification; unresolved prior-use evidence fails closed. `k4b-store` absent before creation, or containing only this lineage's recorded files; K4 FREEZE (e3049fee…c94a) hashes of `chart.py`, `cochain.py`, `errors.py` match; chart cfg equality (§4.2) | Missing authority, evidence or attestation → INCONCLUSIVE/AUTHORITY; hash, scope or seed defect → FAIL_TECHNICAL |
| 1 | release A | H1 IDENTITY | All six checkpoints load through `c1_model.load_model64` (round trip exact), with run_key, step, status, payload sha and the step-0 `seed_map` init seed equal to the step-5000 one (§2.2); the job-0014 `inputs.load_process` identities (WorldSpec, TransitionSpec, EmissionSpecs); maps re-keyed to int; perms are permutations with an exact round trip; E_canon bitwise identical across models; `oracle_profile.validate_process(T, E_canon, π)` returns; `process_law_bound` status BOUNDED, Z_bound recorded (with job 0018's 2.12e-12 beside it, report only); `c1_cert.a1_selftest()` ok; environment identity (distribution hashes as in C1′'s FREEZE) and one thread recorded | FAIL_TECHNICAL/IDENTITY |
| 2 | release A | REG1 | K-REG1 complete and frozen (§3.4); manifest classifies every project directory; coordinator completeness certificate in release A | INCONCLUSIVE/REGISTRY_INCOMPLETE |
| — | S3 | sampling | Immediately before sampling, the K-REG1 reservation is verified valid with no other scientific history generation since the K-REG1 rebuild began (§3.5 W2); cal b0 and val b0 drawn (§3.1); history tables written | Reservation breach before the first row: cancel release A, rebuild K-REG1, new release; after sampling began: stop for lineage review |
| 3 | S3 | H2 SEPARATION | U_cal ∩ K-REG1 = ∅, U_val ∩ K-REG1 = ∅, U_cal ∩ U_val = ∅ (every row); sequence IDs disjoint from the frozen sequence-ID union (§3.4); every row fails the sealed-D-2a predicate (RC6); within-split duplicates counted | Collision → FAIL_TECHNICAL/LINEAGE; predicate satisfied → INCONCLUSIVE/REGISTRY_INCOMPLETE |
| 4 | S3 | ORACLE-VAL | m1, m2, m4, m32 on cal and val; Decimal references (K = 1, 2, 4, 32) on all 3,072 validation rows and the 4 lowest-ID calibration rows; moment check ≤ 1e-10 on each | FAIL_TECHNICAL/ORACLE |
| 5 | S3 | B4-VAL | B^H = B_constant(max B_N, max n̂, 3072); lower = rank-250 order statistic of 5,000 tree means of n̂ (seed 610102); `guard_H5(lower, B^H + Z_bound)` = PASS, i.e. the certified one-sided 95% lower bound of B4 exceeds 0.01 (MD 9) | INCONCLUSIVE/HEADROOM, or INCONCLUSIVE/NUMERICAL in the guard band |
| 6 | S4a | C0-CAL | Per model: `fit_chart_lcc` on the cal landmarks (GIANT, lift, primitive, smoothing), then the gauge (alignment finite, > 0). Trained ledger claims 3. Then, non-gating for valid unavailability: the three step-0 production charts (§9.3; a shared-code FAIL_TECHNICAL stops immediately, RC10) and the suffix decoder (§9.4). Production artifacts and the decoder are serialised, hashed and frozen | C1′ §14 taxonomy: INCONCLUSIVE/CHART_UNAVAILABLE or FAIL_TECHNICAL |
| 7 | S4b | C0-VAL | Validation activations (trained models); direct chart per model with its own GIANT (≥ 487); `c0_val`: support ≥ 507/512, fidelity ≥ 0.80, all 12 bins ≥ 8, resultant ≤ 0.30 | As row 6 |
| 8 | S5 | CERT-VAL | Production extension on all 3,072 validation rows; for every row and every primary array (X−_j, X+_j for three models; n̂): B ≤ 1e-4, P2 analogue. Control and step-0 arrays are certified and reported, non-gating | B above the cap → INCONCLUSIVE/NUMERICAL; trap, flag, phase-range, non-finite or P2 defect → FAIL_TECHNICAL/NUMERICAL |
| 9 | S5 | P1 PRECISION | The test-size rule (§7.1–7.2, with the deterministic F_plan); the §7.6 diagnostic reported (never gated); `SEALED_VALIDATION.json` written and hashed (§7.5) | INCONCLUSIVE/UNDERPOWERED (before any fresh sampling) |
| 10 | release | ACCEPT, K-REG2, release B | Coordinator ACCEPT of the validation report; exclusive generation reservation started (§3.5 W2); K-REG2 rebuilt and frozen (§3.4); release B binds k, N, the K-REG2 sha256 and its source inventory, the reservation, the worker session and the W3 record | No release, no fresh data |
| — | S7 | sampling | Immediately before sampling, the K-REG2 reservation is verified valid with no other scientific history generation (§3.5 W2); test b0 … b(k−1) | Breach before the first test row: cancel release B, rebuild and re-freeze K-REG2, new release; after test sampling began: stop for lineage review, no rebuild around a partly exposed test, no replacement data |
| 11 | S7 | H2-FRESH | Reservation still valid (§3.5 W2); U_test ∩ K-REG2 = ∅ (every row); test sequence IDs disjoint from the frozen union and all others; every row fails the sealed-D-2a predicate (RC6) | Collision → FAIL_TECHNICAL/LINEAGE; predicate satisfied → INCONCLUSIVE/REGISTRY_INCOMPLETE; reservation breach → stop for lineage review (W2) |
| 12 | S7 | T-PRE | Oracle and Decimal references on every test row with the moment check; landmark determinism (§5.6: all 3,072 cal b0 activations recomputed with the identical call, bitwise equal to the stored ones, for the three trained and three step-0 models); extension by the frozen production charts; row certificate ≤ 1e-4 for every primary array; fresh B4 computed and **reported only** (seed 610104; MD 9) | FAIL_TECHNICAL/ORACLE, /DETERMINISM or /NUMERICAL; INCONCLUSIVE/NUMERICAL (cap) |
| 13 | S8 | ENDPOINT | Joint bootstrap (seed 610103, 5,000 draws); ranks and rank checks; B_num and F per model and side; per-model status; overall outcome (§8) | Rank-check failure → FAIL_TECHNICAL/NUMERICAL |

**Notes.**
- B4-VAL is oracle-only and model-independent; it precedes any chart construction, so a headroom failure spends no construction.
- The step-0 charts and the decoder are fixed before any validation activation. A step-0 construction’s valid INCONCLUSIVE/CHART_UNAVAILABLE outcome is non-gating and is recorded as INIT_UNAVAILABLE. A FAIL_TECHNICAL in shared chart code or shared integrity machinery stops the cohort immediately for review. No subsequent gate is evaluated until the defect is resolved under §11.8 or an owner decision. The initialisation control’s descriptive role does not waive shared-code integrity requirements. (RC10; F15 ruled by RU. A decoder failure of §9.4 is non-gating, "unavailable".)
- "First non-PASS stops" means an immediate stop throughout, with only the documented technical-correction exception of §11.8 (RC9).
- Fresh B4 is reported with the flag FRESH_B4_LOW if its certified lower bound is ≤ 0.01. It never changes the outcome (MD 9).

---

## 7. Test size, power and sealing (MD 7; RQ 5)

### 7.1 Inputs (validation, after CERT-VAL)

- **SD upper bounds.** For s ∈ {−, +}: `precision.sd_b4_draws(X_s, r4n, models, seed=610101, draws=5000, size=3072)`, unchanged. The same seed gives the same index stream for both arrays and all models. SD^U_{j,s} = the `inverted_cdf` quantile at 1 − α (rank 4,917) of the 5,000 SDs.
- **Planning allowance (RU optional suggestion 1; closes F6).** F_plan = max{B_constant(1e-4, 4, 12288), 10⁻⁹} + Z_bound, in exact rationals, with B_constant = `c1_bounds.B_constant` unchanged, the cap 1e-4 passed as the exact rational 1/10⁴, and Z_bound the H1 value. It is the same for every model, side and candidate N.
  - **Value [W].** d_n = bit_length(12288 − 1) = 14 (2¹³ = 8192 ≤ 12287 < 16384), so the factor is γ₁₅ = 15u/(1 − 15u) with u = 2⁻⁵³: γ₁₅ ≈ 1.6653345e-15. OUT(1e-4) = (1 + 2⁻³⁰)·1e-4 + 2⁻⁸⁰⁰ = 1e-4 + 9.313226e-14 + 2⁻⁸⁰⁰. γ₁₅·Fraction(4.0) ≈ 6.661338e-15. ζ = 2⁻⁸⁰⁰ ≈ 1.5e-241 (twice in total, negligible). Hence B_constant(1e-4, 4, 12288) ≈ 1e-4 + 9.979360e-14 = 1.0000000009979e-4 > 10⁻⁹. With job 0018's Z_bound = 2.12e-12 [H], F_plan ≈ 1e-4 + 2.219794e-12 ≈ 1.0000000222e-4. The run computes F_plan exactly with its own Z_bound.
  - **Why it bounds the future allowance.** OUT, γ_k and therefore B_constant are nondecreasing in max_b, in max_abs and (through d_n = ⌈log₂ n⌉) in n. Whenever the fresh cap (every primary row B ≤ 1e-4) and P2 (|X̂| ≤ 4) checks pass at any n ≤ 12,288, every fresh B_num,j,s ≤ B_constant(1e-4, 4, 12288), so every fresh F_{j,s} ≤ F_plan (the same H1 Z_bound enters both).
  - F_plan is used only in planning. The fresh decision always uses the actual F_{j,s} of §5.5. This is part of the planning approximation and does not alter the fresh numerical guard. (Adapted RC14 text; see §18.3.)
- **Reused-call contract (RC13).** For each side, X_s is an int-seed-keyed dictionary. Pass r4n as {j: norm_array for j in models}, not as a single ndarray: sd_b4_draws requires dictionaries for both arguments. Its return is (sd_draws, b4_draws), each with columns in models order. Use only sd_draws for the ladder; the B4 decision uses its separately registered certified tree-mean stream.

### 7.2 The rule

For N in the order 3,072, 6,144, 12,288, N qualifies iff both hold.

1. **MDE (L's rule, `precision.mde` unchanged).** With cfg = {delta: 0.01 + F_plan, alpha: 0.05/3, power: 0.80, projected_N: N}: mde(SD^U_{j,s}, cfg) ≤ 0.02 for every j and both s. Equivalently (z_{1−α} + z_{0.80})·SD^U/√N ≤ 0.01 − F_plan, with z_{1−α} = 2.128045, z_{0.80} = 0.841621 and z-sum 2.969666 [W].
2. **Projected power, per model and joint (X's check, MD 7).** e = `precision.centered_draws(X_dict, keys, seed=610105, draws=5000, size=N)`, unchanged, where X_dict holds the six validation arrays keyed (j, s), so one index vector per draw is shared by every model and side. Let q_α(e_{j,−}) be the rank-84 and q_{1−α}(e_{j,+}) the rank-4,917 value of the column. For draw b:
   - **SUPPORT scenario (E X−_j = 0.02):** succ_{j,b} = [0.02 + e_{b,j,−} + q_α(e_{j,−}) − F_plan > 0.01];
   - **EXCLUSION scenario (E X−_j = E X+_j = 0):** succ_{j,b} = [e_{b,j,+} + q_{1−α}(e_{j,+}) + F_plan < 0.01] ∧ [e_{b,j,−} + q_α(e_{j,−}) − F_plan > −0.01].

   In each scenario, every per-model count Σ_b succ_{j,b} and the joint count Σ_b Π_j succ_{j,b} must be ≥ 4,000 of 5,000 (projected probability ≥ 0.80, compared in integers).

N is the smallest qualifying candidate. If none qualifies, the result is **INCONCLUSIVE/UNDERPOWERED**, recorded before any fresh sampling, and the cohort ends. N is chosen once and never revised; k = N/3072 test blocks are released.

The projection uses centred draws, so it is invariant to the validation means, which stay sealed (§7.5). It is a planning approximation: power at E X− = 0.02 is not power at Δ4 = 0.02 (X§8), and the bootstrap spread at size N is approximated by resamples of the 3,072 validation rows.

The exclusion projection separately recentres the endpoint columns to zero. With positive missing residual mass, those shifted columns do not represent a feasible zero-width completion model for this frozen chart. This is a hypothetical zero-width precision benchmark, not an estimate or guarantee of actual EXCLUSION power for the observed support rule. Passing its 4,000/5,000 threshold remains a registered planning requirement. No width gate is added. (RC14; F5 ruled by RU. The width-preserving diagnostic of §7.6 is reported beside it, never gated.)

### 7.3 What the rule implies (desk arithmetic, not gates)

- Since |X±| ≤ ‖r4‖, SD(X±) ≤ √E‖r4‖² = √V4. Job 0014 measured V4 = 0.0072 (calibration) and 0.0089 (validation; 95% upper 0.0121) on other histories [H], so SD ≲ 0.085–0.110 [W from H].
- **MDE rule:** it passes at N iff SD^U ≤ (0.01 − F_plan)·√N/2.9697. With F_plan ≈ 1.0000000222e-4 [W]: 0.18477 (N = 3,072), 0.26131 (6,144), 0.36955 (12,288) [W] (v1, ignoring F_plan: 0.1866, 0.2640, 0.3733).
- **Joint power, sufficient conditions (union bound, normal approximation):** exclusion over 6 one-sided events holds with joint power ≥ 0.80 if each fails with probability ≤ 0.2/6, i.e. SD ≤ (0.01 − F_plan)·√N/(2.1280 + 1.8339): 0.13850, 0.19586, 0.27699 [W]. Support over 3 events: SD ≤ (0.01 − F_plan)·√N/(2.1280 + 1.5011): 0.15120, 0.21382, 0.30239 [W]. These are sufficient, not necessary; the run decides by the projection.
- At SD = 0.11 and N = 3,072 [W]: se = 0.001985; (0.01 − F_plan)/se − 2.1280 = 2.8603, so each one-sided failure probability ≈ 2.1e-3 and the six-event union ≈ 0.013. So **N = 3,072 is expected** [W from H], unless the validation SDs are far above the oracle bound.

### 7.4 Correction of L's power claim (MD "Verified"; AN §1.6)

L§5 said the single MDE inequality "gives 80% planned power for each side of EXCLUDE at Δ = 0". That is wrong as stated.
1. **The planning point is E X+ = E X− = 0**, not Δ4 = 0. When the width 2E[(1 − A)‖r4‖] is positive, Δ4 = 0 does not place either endpoint at 0, and the two are different planning points.
2. **Per-model power of the two-sided rule** at that point is ≥ 60%, not 80%. The MDE rule bounds each one-sided failure by 20%. The two failures lie in opposite tails: the upper fails iff the mean exceeds 0.01 − z_{1−α}·se, the lower iff it is below −0.01 + z_{1−α}·se, and both need z_{1−α}·se > 0.01, which the rule excludes (z_{1−α}·se ≤ 0.01·2.128/2.970 < 0.01). So the failures are disjoint, and power ≥ 1 − 0.2 − 0.2 = 0.6.
3. **Joint power across the three models was not planned.** The models share histories and r4, so it is neither 0.6³ nor 0.6. MD 7 adds the projected joint check of §7.2(2), which is now part of the rule.

The ≥60% statement is a normal-planning lower bound at the zero-width reference point, using the MDE inequality. It is not a finite-sample coverage or power theorem for the percentile bootstrap. Likewise, 4,000 successes among 5,000 projection draws is an empirical planning threshold, not a confidence lower bound of 0.80 on true power. (RC14)

### 7.5 Sealing (L; MD 7)

Validation means of X±, controls, step-0 arrays, decoder scores, Δ1, Δ2 and Δ4^orc are written only by the sealing writer to SEALED_VALIDATION.json. This also seals every reported quantity that directly reconstructs those means, including the supported contribution mean(A·u·r4), the conditional supported-row score mean and endpoint-derived ratios.

The sealing writer may compute these quantities internally. precision.centered_draws may compute internal centring means, which are neither exported nor logged. SEALED_VALIDATION.json is written once at P1, hashed, and opened only after the fresh result is recorded.

The validation report may contain chart diagnostics, support counts, missing residual mass and width, residual-norm summaries, B4, reference discrepancies, SD bounds, projection summaries and certificate bounds. It contains no supported contribution or conditional supported-row score mean.

(RC3. Reason: with C = mean(A·u·r4) and D = mean((1 − A)‖r4‖), the endpoint means are X̄± = C ± D, so reporting C beside the width would unseal them. The width-preserving diagnostic of §7.6 uses D and centred draws only, never C.)

### 7.6 Width-preserving exclusion-power diagnostic (RU optional suggestion 2; report only)

This diagnostic is a width-preserving translated-endpoint benchmark. It retains the measured missing residual mass and recentres the common endpoint location using centred draws. It does not construct a new unit-valued coordinate or establish a feasible generating model for the frozen support rule.

- D̄_j = mean((1 − A_j)‖r4‖) over the 3,072 validation rows (a reported quantity, §7.5).
- Hypothetical translated endpoints have means −D̄_j and +D̄_j. In exact algebra, translating both validation arrays by −C̄_j gives those empirical means and leaves their centred draws unchanged. Implement the diagnostic from D̄_j and the existing centred draws; do not materialise translated arrays or compute C̄_j outside the sealing writer. The computation remains an operational resampling approximation.
- For each candidate N and draw b: succ^w_{j,b} = [D̄_j + e_{b,j,+} + q_{1−α}(e_{j,+}) + F_plan < 0.01] ∧ [−D̄_j + e_{b,j,−} + q_α(e_{j,−}) − F_plan > −0.01].
- Reported: the per-model counts and the joint count out of 5,000, for every candidate N, beside the registered zero-width projection.
- **Never gated.** It does not change N, the ladder, any gate or any outcome. It is a resampling planning approximation, not a power theorem. For population endpoints C−D and C+D, exclusion requires D<0.01 and |C|<0.01−D. Thus population D≥0.01 makes the population exclusion claim false. A finite-sample EXCLUDE decision can nevertheless occur through statistical error, and an observed D̄≥0.01 is not a certificate that population D≥0.01.

---

## 8. Decision rule, levels and licences (MD 6, MD 15; RQ 6)

### 8.1 Per-model status (exact rationals)

Fresh endpoint: one joint stream (seed 610103, 5,000 draws) over every array of §9 and X±_j. L−_j = rank-84 order statistic of the X−_j tree means; U+_j = rank-4,917 order statistic of the X+_j tree means; both rank-checked. F_{j,−}, F_{j,+} as in §5.5. Central 95% intervals (ranks 125, 4,875) and point means are reported.

- **SUPPORT_j** iff L−_j − F_{j,−} > 0.01.
- **EXCLUDE_j** iff U+_j + F_{j,+} < 0.01 **and** L−_j − F_{j,−} > −0.01 (two-sided; MD 6).
- **UNRESOLVED_j** otherwise. Labels: **UNRESOLVED/NUMERICAL** if the status would differ with F replaced by 0; **NEGATIVE_ALIGNMENT** if U+_j + F_{j,+} < −0.01 (reported; history information of the opposite sign, not its absence).

All inequalities are strict; equality is unresolved.

### 8.2 Overall outcome

| Outcome | Rule |
|---|---|
| **SUPPORT** | SUPPORT_j in all three models |
| **EXCLUSION** | EXCLUDE_j in all three models |
| **MIXED** | At least one definite status (SUPPORT_j or EXCLUDE_j), and not all three the same definite status |
| **INCONCLUSIVE** | No model has a definite status (labelled INCONCLUSIVE/NUMERICAL if any is UNRESOLVED/NUMERICAL), or an earlier gate ended the cohort (with that gate's reason) |
| **FAIL_TECHNICAL** | Integrity, implementation or numerical defect |

A stopped gate is never converted into a scientific exclusion. All per-model results are always published; no model is selected post hoc as representative.

### 8.3 Levels

Each one-sided bound uses α = 0.05/3. Subject to the nominal accuracy of the percentile bootstrap, a false SUPPORT_j has probability at most α, and a false EXCLUDE_j has probability at most α; EXCLUDE_j is an intersection-union test.

These are separate claim-specific guarantees. Because the procedure can report either SUPPORT_j or EXCLUDE_j, their combined per-model false-claim probability is bounded by 2α, not α. Across the three published per-model results, Bonferroni therefore gives a bound of 6α = 0.10 for any false definite claim. The SUPPORT family separately and the EXCLUDE family separately each have a 0.05 bound.

For the two all-three study-level verdicts, a false overall SUPPORT requires an erroneous lower bound in at least one fixed null model; a false overall EXCLUSION requires an erroneous relevant bound in at least one fixed model violating exclusion. Each verdict separately is bounded by α, and the union of the two erroneous overall verdicts is bounded by 2α.

These bounds are nominal bootstrap approximations, conditional on the weights, charts and gauges. They exclude training-seed variability and do not constitute a simultaneous six-bound 95% confidence statement.

(RC1. This replaces v1's claim that the per-model error is ≤ α and the family error ≤ 0.05; that claim was wrong because, at E X− = E X+ = 0.01, either direction can produce a false claim through opposite tail errors. The three checkpoints are fixed objects, not a sample of training runs.)

### 8.4 Licences (L's templates ∪ X's list; MD 15)

These are nominal percentile-bootstrap statements conditional on the three fixed models and frozen charts/gauges. Documented-law transport assumes independent uniform 53-bit sampler draws. The certified allowance does not bound deterministic PCG64 bias or dependence. (RC15; F18 ruled by RU.)

**SUPPORT (numbers filled at run time).** "In each of the three E4 cylinder-O models (seeds 1729/2718/3141, step 5000, resid_post_3, position 32), the gauged phase of a chart built by the LCC ≥ 95% rule on fresh calibration histories covaries with the first-harmonic oracle residual r4 = m32 − m4 on fresh stationary test histories. For every assignment of unit coordinates to the unsupported rows (a/N, b/N, c/N of N), the one-sided (1 − 0.05/3) lower bound of E[u·r4] under the documented generating law exceeds 0.01 after the certified numerical and transport margin F (values …; B4 = …). Every function of the last four observations has zero population covariance with r4 under that law, so on its supported rows this coordinate does not coincide with any unit-valued function of the last four observations: it depends on observations before the last four, in a direction aligned with the oracle belief residual." Qualifiers are appended when triggered: the step-0 qualifier (§9.3), "initialisation control unavailable (reason)", and the C1′ disclosure of §4.5 in every report.

These are nominal percentile-bootstrap statements conditional on the three fixed models and frozen charts/gauges. Documented-law transport assumes independent uniform 53-bit sampler draws. The certified allowance does not bound deterministic PCG64 bias or dependence. (RC15.)

**EXCLUSION.** "For this chart rule, site and process, in each model the covariance of the chart phase with r4 lies within (−0.01, 0.01) for every completion of unsupported rows, under the documented law, at the stated nominal levels (bounds …; B4 = …). Covariance of either sign at or beyond the 0.01 margin is excluded." There is no post-test reflection that turns a negative alignment positive (X§10).

**MIXED / INCONCLUSIVE.** Only the recorded per-model results and the identified limitations.

**What a positive result does not establish.**
1. **Memory horizon.** Nothing beyond "earlier than the last four observations". Historical job 0014 reported B8 ≈ 0.0093 on other histories. That observation motivates the selected margin and context length. Neither that historical point estimate nor K4b establishes an eight-observation memory horizon, short-context sufficiency, or absence of dependence beyond any particular position. (RC15)
2. **Use.** No causal use, predictive use, benefit or necessity for prediction (C1′'s question, separate and closed INCONCLUSIVE). Not that the output uses the beyond-four component.
3. **Mechanism.** No topological necessity, no literal internal circle, no mechanism in earlier layers, not that the circle is how the model computes, no nonadditive integration of history.
4. **Tracking quality.** Δ4 is a covariance with a residual, bounded by B4. It is not fidelity, recovery of the hidden state, decodability of m32 or belief-tracking accuracy.
5. **Unsupported rows.** Nothing about the coordinate's value on unsupported rows; the claim holds for all completions, which is weaker than knowing them.
6. **Learning.** No training-induced gain over initialisation; even a null step-0 control does not establish a causal effect of training.
7. **Population.** No generalisation to other training seeds, sizes, architectures, sites, layers, checkpoints, harmonics, the y-coordinate, processes or worlds. Three fixed models of one process are not three independent worlds.
8. **Uniqueness.** Not that this coordinate is the unique carrier.
9. **Other studies.** It is not a K4 result and changes no verdict: K4 INCONCLUSIVE, E4 G-H FAIL, X4-F INCONCLUSIVE, B2 NO-GO, K8 FAIL, H5 REJECTED, C1′ INCONCLUSIVE/FAMILY_UNMATCHED and D-2a NOT_LEARNED all stand. It does not validate the LCC rule beyond K4b's own gates.
10. **Exact zero for the saved data.** The suffix-only zero holds for P*; Z_bound covers the stored parameters and the idealised sampler law only.

**What EXCLUSION does not establish.** Short-context sufficiency; suffix-only dependence of the coordinate; absence of history information in other coordinates, harmonics or nonlinear readouts. Δ4 ≈ 0 is compatible with prefix dependence orthogonal to r4.

### 8.5 Competing explanations and what discriminates them (L§6)

| Explanation | Discriminating observation |
|---|---|
| E1, symbol or short-context statistics | Predicts E X− ≤ 0 (Corollary A1) |
| E2, belief formation over history | Predicts Δ4 > 0; the ideal phase-only coordinate scores 0 ≤ Δ_ideal^orc ≤ B4 (§9.6) |
| E3, a chart or architecture artifact | Step-0 control; the two population-zero controls |
| E4, selection through support | Ruled out by Theorem A |
| E5, numerics or the stored law | Arithmetic discrepancies are bounded for the fixed operational coordinate by the row and aggregation certificates; expectation transport is bounded under Lemma T’s sampler assumptions. These do not rule out statistical error, PRNG departures or a scientifically uninformative operational chart. (RC15) |
| E6, reuse or leakage | Fresh histories, K-REG1 and K-REG2, every-row separation |
| E7, a gauge tuned to the outcome | Gauge fitted on calibration m32 only; gauge invariance of the zero |

---

## 9. Controls and descriptive analyses (MD 8; RQ 7). Reported, never gated, never subtracted

All use the fresh rows and the joint stream (seed 610103). Each reports the point value, the central 95% interval, the α and 1 − α bounds and its own certified B (an array whose B exceeds the cap is labelled "uncertified"). Every coordinate is a float phase φ ∈ [0, 2π) with u = (cos φ, sin φ), so `row_bound` certifies it unchanged. A phase equal to 2π after rounding is mapped to 0. **No control mean is ever subtracted from X±, used to centre the endpoint, or used to change a threshold or a null.**

1. **m4-phase null.** φ = atan2(m̂4,y, m̂4,x) mod 2π, exact (0, 0) → 0. Suffix-only, so Δ4 = 0 under P*. Score u·r4 on every row (no support set). `scores.angular_instability` counts are reported. This departs from K4's `_unit` vectors so that a phase exists to certify; it remains suffix-only.
2. **SHA-of-suffix null.** φ = `scores.sha256_phase(canonical w29..w32)` (first 8 digest bytes, big-endian). Suffix-only, Δ4 = 0 under P*. Score on every row.
3. **Step-0 (initialisation) control.** The step-0 checkpoints of the same runs (§2.2), the same rule on the same 512 cal landmarks, production role only (step-0 ledger, ≤ 3), gauge on m32[C*_init]. Extension, support, X±_init and the identified set exactly as for the trained models; step-0 validation diagnostics (support on the 512 val panel, bins, resultant) reported; no direct comparator and no fidelity gate (AN D10). It has no population-zero identity: an untrained network is a fixed function of the whole history (X§11), so it is a reference, not a zero null. **Pre-registered reading:** if L−_init,j − F_init,j > 0.01 in model j, that model's SUPPORT sentence carries "a chart built by the same rule on the untrained network of the same run also shows this". If a step-0 chart or gauge fails validly, the control is "unavailable (reason)", and the licence notes it. A step-0 construction’s valid INCONCLUSIVE/CHART_UNAVAILABLE outcome is non-gating and is recorded as INIT_UNAVAILABLE. A FAIL_TECHNICAL in shared chart code or shared integrity machinery stops the cohort immediately for review. No subsequent gate is evaluated until the defect is resolved under §11.8 or an owner decision. The initialisation control’s descriptive role does not waive shared-code integrity requirements. (RC10)
4. **Fixed suffix decoder (descriptive; target fully specified, MD 8).**
   - **Rows:** the 2,560 non-landmark rows of cal b0, supported or not.
   - **Input:** one-hot of canonical w29..w32 (4 × 36 = 144 columns).
   - **Target:** (cos φ_j, sin φ_j), the production extension phase of model j on those rows (computed after C0-cal, before any validation activation).
   - **Fit (x4f family, reused unchanged; c1_fit pattern, not `c1_fit.fit_decoder`, which hard-codes the `c1-sf-v1` scope):** `x4f_scores.standardizer`; ℓ from `rbf_bandwidth(·, generator("k4b-sf-v1", "suffix_rbf_bw", j), 1024)`; `rbf_map(144, 2048, ℓ, generator("k4b-sf-v1", "suffix_rbf", j))`; `rbf_features`; `x4f_probe.nested_ridge` with grid (1e-3, 1e-2, 1e-1, 1, 10), ties to the larger λ, over 5 panels of 512 rows (rank among the 2,560 rows by ascending sequence_id, integer-divided by 512) [W specification, F8]; then `RidgeProbe([λ*]).fit(Ft, Y, Ft, Y)` on the standardised features. The equivalence self-check of §5.6 is reported.
   - **Call contract (RC13).** Let F be the raw random-feature matrix after the saved one-hot-input standardisation and random-feature map. Call nested_ridge(F, Y, panels, F, Y, grid): the outer arrays here are the same calibration rows, and its outer score is not a validation result or a selection criterion. nested_ridge performs feature standardisation internally on each fit set.

     For the final RidgeProbe, compute and save mean_F, scale_F = standardizer(F), set Ft = (F - mean_F)/scale_F, and call RidgeProbe([λ*]).fit(Ft, Y, Ft, Y). Apply those saved transformations to every future suffix. Compare its calibration predictions with nested_ridge.pred_val using §5.6’s descriptive tolerance. Unpack and check rbf_bandwidth’s (ell, status) return before constructing the map. (F8 ruled by RU: fixed descriptive family, no fallback.)
   - **Output:** ψ_j = atan2 of the prediction mod 2π (exact zero → 0), frozen before validation.
   - **Reported:** (a) its score u_ψ·r4 on every test row (a fixed suffix function, so Δ4 = 0 under P*); (b) the agreement |mean exp(i(φ_j − ψ_j))| on supported test rows, which describes how much of the learned phase one suffix function reproduces; it is not a ceiling over all suffix functions.
   - A degenerate bandwidth or a failed equivalence check makes the decoder "unavailable", non-gating. No fallback family (X's KRR is not adopted; F8, ruled by RU).
5. **Secondary context lengths Δ1, Δ2 (descriptive).** r_K = m32 − m_K with the same S and u; X±_K; certified by `row_bound` at K and by Lemma N with ε_K. No inference or multiplicity claim. K = 8 and 16 are not analysed (the historical B8 ≈ 0.0093 of job 0014 [H] motivates this choice; it is not a horizon claim, §8.4 item 1).
6. **Phase-only oracle scale.** For the ideal documented-law coordinate \(v_*=m_{32,*}/\|m_{32,*}\|\), with a fixed unit fallback at exact zero, define \(\Delta_{\mathrm{ideal}}^{orc}=E_*[v_*\cdot r_{4,*}]\). Then
   \[
   0\le\Delta_{\mathrm{ideal}}^{orc}\le B_4.
   \]
   Indeed, \(v_*\cdot m_{32,*}=\|m_{32,*}\|\), \(v_*\cdot m_{4,*}\le\|m_{4,*}\|\), and conditional Jensen gives \(E\|m_{4,*}\|\le E\|m_{32,*}\|\).

   The reported operational comparator uses the saved float phase obtained from the computed m32, with exact zero mapped to phase 0. Its score is certified for that fixed phase. The ideal-coordinate nonnegativity proof is not a certificate of the normalised phase computation, and a finite-sample estimate need not be nonnegative. Neither comparator is an upper bound on other coordinates’ covariance. Endpoint ratios with a nonpositive or undefined comparator denominator are reported as undefined. (RC15; the operational comparator is the array called Δ4^orc elsewhere in this protocol.)
7. **Also reported:** the naive completion (the extension phase used on unsupported rows; one member of the identified set, never decision-bearing); E X−/B4 and E X−/Δ4^orc (undefined when the denominator is nonpositive or undefined); Z_bound; the chart diagnostics (b, d, r, ℓ_max, components, excluded IDs, lift kind, g, residual, alignment, fidelity, bins, resultant).
8. **Intervention lesson (U5).** K4b has no intervention, patching, forcing or decoder-damage gate; it is purely observational, so the C1′ M2-cal feasibility lesson does not apply.

---

## 10. Support reporting (RQ 4)

Per model and per split (the 512-row chart panel, all validation rows, all test rows, and each test block):
- denominator, supported count and fraction;
- C* size and excluded landmark IDs;
- counts of unsupported rows by reason (resultant < 0.2; 8th-NN distance > R; both), and duplicate-query counts;
- resultant and 8th-NN distance summaries;
- the missing residual mass mean((1 − A)‖r4‖) and the width 2·mean((1 − A)‖r4‖);
- mean ‖r4‖ on supported and on unsupported rows (whether unsupported rows are atypical);
- **diagnostic, not null-protected (AN §1.3):** the full-denominator supported contribution mean(A·u·r4) and the conditional supported-row mean;
- numerical maxima and certificate counts.

The 507/512 validation chart gate is the only support gate. There is no fresh-test support gate: low fresh support widens the registered interval; it never removes rows or triggers replacement data.

For validation, the supported contribution and conditional supported-row score mean are sealed under §7.5. The reporting requirements in this section do not override sealing. (RC3)

---

## 11. Implementation, reuse, binding and execution (RQ 8)

### 11.1 Files (each ≤ 400 lines; no edit to any existing file)

| File | Contents | Budget [H/W] |
|---|---|---|
| `tools/k4b/API.md` | Written contract, committed before any module code: every function, input, output, report key, seed and path; the S0 allowlist. The protocol wins on conflict | — |
| `tools/k4b/CONTRACT.json` | Constants, seeds, thresholds, checkpoint IDs, the chart section (§4.2), resources, worker session default | — |
| `tools/k4b/TEST_PLAN.md`, `CERTIFICATE.md` | Test plan; Lemma N, Lemma T, Theorem B′ with references to EB and C1′ §15.3.11 | — |
| `k4b_config.py` | Contract load; constants; chart-cfg equality with C1′ | ≈ 100 |
| `k4b_data.py` | Process assembly (int-keyed), sampling, IDs, history tables, separation, duplicates | ≈ 220 |
| `k4b_registry.py` | Registry sources (§3.4): reuse of `c1_registry_sources` readers; C1′ digest sources; permitted D-2a pools and other-store readers; recursive inventory; handoff-JSON pre-validation; coverage revalidation; sealed-D-2a predicate and derived sequence-ID ranges; NOT_SCANNED table; manifest (RC6, RC7) | ≈ 320 |
| `k4b_scores.py` | Oracle moments (K = 1, 2, 4, 32); X± assembly; control and descriptive phases | ≈ 220 |
| `k4b_decoder.py` | The suffix decoder (§9.4), equivalence self-check | ≈ 120 |
| `k4b_charts.py` | Ledgers (6 + 3), construction and extension wrappers, persist hooks, C0-cal/C0-val, step-0 non-gating handling, determinism recheck | ≈ 220 |
| `k4b_cert.py` | References, moment checks, row bounds, Lemma N, B_num, F, guards | ≈ 250 |
| `k4b_stats.py` | Joint bootstrap, ranks, the ladder (§7), statuses, outcome, sealed file | ≈ 260 |
| `k4b_driver.py` | G0 → P1 (release A stages), gate records, stage directories | ≈ 380 |
| `k4b_fresh.py` | K-REG2 step, H2-FRESH, T-PRE, endpoint, export | ≈ 330 |
| `k4b_release.py` | Release verification, freeze, pin check; reservation records (RC8) | ≈ 220 |
| `k4b_meter_bind.py` | The meter binding of §11.7 (RC11): controls, meter and winjob rebinding; worker session from the release (R10 pattern); the supervisor limiter wrapper with op_guard and disk safe-STOP | ≈ 140 |

About 2.4–2.9k lines of Python [W], plus about 1.5–2.5k lines of tests [H]. L planned 8 files; W separated the registry (widened by MD 10) and the decoder.

The implementation table specifies eleven configuration/orchestration/scientific modules plus the meter binding: twelve Python files in total. Each is at most 400 lines. An additional Python module requires a documented footprint/reuse reassessment before implementation; it is not prohibited by the erroneous “twelfth module” rule. (RC12; F11 ruled by RU.) A file over 400 lines stops implementation for escalation.

### 11.2 Contract first

`API.md`, `CONTRACT.json`, `TEST_PLAN.md` and `CERTIFICATE.md` are committed before any module code and change no scientific choice.

### 11.3 Six-field reuse assessment (every reused function verified at c460e24; every file below is byte-identical at 93350d7; 31 files in v2, with op_guard added by RC11)

**Reused files and their sha256** (W, `git show c460e24:<f> | sha256sum`, equal at 93350d7):

| File | sha256 (first 16) | File | sha256 (first 16) |
|---|---|---|---|
| tools/c1prime/c1_chart.py | 45b6aa0d8c8db28c | tools/x4_circle_history/chart.py | 938821a0fd6651ce |
| tools/c1prime/c1_model.py | 37665037dd4d6b29 | tools/x4_circle_history/cochain.py | e53f6725d6596000 |
| tools/c1prime/c1_means.py | e063081694222493 | tools/x4_circle_history/errors.py | 8aa309c42350cad9 |
| tools/c1prime/c1_bounds.py | e6a2c1fc9594aa37 | tools/x4_circle_history/error_bound.py | b44fcda14ba11271 |
| tools/c1prime/c1_cert.py | b0cb037a52071e80 | tools/x4_circle_history/precision.py | 5ae1e632eee0ac57 |
| tools/c1prime/c1_records.py | d0299ff4621c699a | tools/x4_circle_history/scores.py | 8cf9a5f810ad41a4 |
| tools/c1prime/c1_data.py | 262418b2f0272e84 | tools/x4_circle_history/stage_records.py | 997a425dd16f7256 |
| tools/c1prime/c1_config.py | 8e170b5144b73252 | tools/x4_circle_history/process_law.py | a0ae95894147bd76 |
| tools/c1prime/c1_oracle.py | 077ea1489262d150 | tools/x4_oracle_profile/oracle_profile.py | fbda1c0382cb5985 |
| tools/c1prime_registry/c1_registry_sources.py | 4f40840d8eb88d51 | tools/x4_oracle_profile/inputs.py | 2ce1492e4388499e |
| tests/oracle_profile/independent_reference.py | e08d02ad03ca8400 | tools/x4_oracle_profile/config.json | 624b3a90def9924e |
| src/topo_pilot/analysis/x4f_scores.py | 03e2d736a734cf8d | tools/x4_oracle_profile/meter.py | 738ea68accc7a02c |
| src/topo_pilot/experiment/x4f_probe.py | d6315bc94869dc8f | tools/x4_oracle_profile/winjob.py | 3b29e863ab6ae97c |
| src/topo_pilot/prediction/ridge.py | e63de356d0aa258d | tools/x4_oracle_profile/controls.py | c4fac9946c0fed21 |
| src/topo_pilot/dataset/sampler.py | a94ffd3e7310e45d | src/topo_pilot/learner/stage.py | b6170ca6037c8f95 |
| tools/x4_circle_history/op_guard.py (v2, RC11) | 90fb20e3686c19b2 | | |

**Reuse binding added in v2 (RC11; W verified the sha256 at c460e24 and 93350d7):** tools/x4_circle_history/op_guard.py, SHA-256 90fb20e3686c19b28c561259634ef97b6516037a9165a8eba9d81640a0c590a1. Public interfaces reused: timed_factory(out, wall_s, clock=time.monotonic, wall_clock=time.time), overdue(marker_path, now_epoch), archive_stale(out). Protect this file under S0.

Every file of this table that `c1prime-store/FREEZE.json` lists (the nine `c1_*` files, the eight K4 files other than `process_law.py`, including `op_guard.py`, and the four job-0014 files other than `inputs.py` and `config.json`) has exactly the hash recorded there (W compared them). The full 64-hex values are bound in the K4b freeze record.

| Field | Assessment |
|---|---|
| **1. Existing functions and artifacts, reused unchanged** | **C1′ chart** (`c1_chart`): `MAX_CONSTRUCTIONS = 6`, `ROLES = ("production", "direct")`, `IDENTITY_CARRIER`; `landmark_ids(seq_ids) -> ndarray`; `ConstructionLedger(path)` with `.claims() -> list` and `.claim(model, role) -> None`; `giant_pass(m, n=512) -> bool`; `fit_chart_lcc(X, ids, cfg, guard=None, timed=None, persist=None) -> chart.Chart`; `fit_production_gauge(ch, m32_cstar) -> chart.Gauge`; `serialise(ch, gauge, role) -> dict`; `extend_phase(prod, gauge, Q, cfg, timed=None)`; `c0_val(prod, gauge, val_X, direct, cfg) -> dict`. **Model:** `c1_model.load_model64(checkpoint) -> (model64, sha)`, `model_inputs(named32) -> Tensor`, `activations(model64, inputs, batch=1024) -> ndarray`, `state_sha(model) -> str`. **Means:** `c1_means.tree_mean(X)`, `bootstrap_means(arrays, seed, draws=5000) -> dict`, `rank_for(p, draws=5000) -> int`, `P_THIRD = Fraction(5, 300)`, `rank_check(values, v, k) -> bool`, `quantile_with_rank(values, p) -> (v, k)`. **Bounds:** `c1_bounds.FLOOR = Fraction(1, 10**9)`, `B_constant(max_b, max_abs, n) -> Fraction`, `guard_H5(lower, B_H) -> str`. **Certificate:** `c1_cert.gamma(n)`, `OUT(x)`, `ZETA`, `a1_selftest() -> dict`, `p0(T, E_list, pi) -> dict` (its `identical` and `E_digests` fields). **Records:** `c1_records.C1GateFailure(status, reason)`, `classify_exception(exc) -> (status, reason)`, `adapt_chart_exception(exc) -> (status, reason) or None`. **Registry:** `c1_data.registry_digests(canon32) -> set`, `separation(U_cal, U_val, R1) -> dict`, `build_registry(sources) -> dict`, `lowest(seq_ids, n)`; `c1_registry_sources.observation_set_sources(store=None, root=ART) -> (sources, seqs)`, `store_sources(root=ROOT) -> list`, `handoff_sources(root=…) -> list` (its reader returns `EMPTY` on `ValueError`, so K4b validates the JSON first, RC7), `canonical32(named, perm)`, `reference_cache_reader(path)`, `history_index_ids(store=None, root=ART) -> dict`, `coverage(seqs_a, hist_ids, root=ROOT) -> dict` (RC7; W verified at c460e24); `observation_set_sources` is always passed an explicit `store` backed by the same root when the root is not the default (RC7). **Config:** `c1_config.chart_cfg(contract=None) -> dict`, `load_contract(path)`, `CHART_KERNEL_KEYS` (import loads C1′'s CONTRACT.json and sets the K4/0014 sys.path). **K4:** `chart.Chart`, `Gauge(sign, shift, alignment)`, `Extension(phase, resultant, eighth_distance, supported, duplicate)`, `extend(chart, gauge, Q, cfg, timed=None) -> Extension`, `fit_gauge(chart, m32) -> Gauge`, `agreement(phi_a, phi_b) -> float`, `phase_bin_counts(phi, bins=12)`, `overall_resultant(phi)`, `chart_to_arrays(chart, gauge)`, `chart_from_arrays(d)`; `error_bound.reference_moments(T, E, pi, coords, canonical32, Ks=(4, 32), cache=None, cache_only=False) -> list[dict]`, `row_bound(x_hat, phi, M4, M32, eps_M4, eps_M32) -> dict`, `posterior_envelope(L, S)`, `moment_envelope(beta, S)`, `process_digest(T, E, pi, coords)`, `MOMENT_TOL_EXACT`; `process_law.process_law_bound(T, E, pi, coords) -> dict` (key `Z_bound`); `precision.sd_b4_draws(X, r4n, models, seed, draws, size)`, `centered_draws(X, models, seed, draws, size)`, `mde(sd, cfg) -> float`; `scores.history_digests(canonical32)`, `canonical_from_named(named, symbol_perm)`, `unit_vectors(phi)`, `scores(u, m32, m4)`, `r4_norms(m32, m4)`, `sha256_phase(last4_row)`, `angular_instability(m, bound)`; `stage_records.write_new(path, obj)`, `save_npz(path, **arrays)`, `record_gate(out, gate, status, **details)`, `sha256(path)`; `errors.Invalid`, `Unresolved`, `JoinError`; `op_guard.timed_factory(out, wall_s, clock=time.monotonic, wall_clock=time.time)`, `overdue(marker_path, now_epoch)`, `archive_stale(out)` (RC11). **Job 0014:** `oracle_profile.circle_features(coords)`, `canonical_emission(E_named, symbol_perm)`, `validate_process(T, E, pi, tol=1e-12)`, `posterior_means(T, E, pi, tokens, Ks, features) -> {K: [n, 2]}`; `inputs.load_config()`, `load_process(cfg) -> dict`; `meter.py` (module names `OUT`, `LEDGER`, `EMERGENCY`, `LOCK`, `ACTIVE`, `LOG_DIR`, `WORKER_SESSION`, `CAP_S`, `STOP_NEW_S`, `OUTPUT_CAP`; hook `limit_reason(ledger, child, args, active_wall, polls, mailboxes)`; flags `--max-cpu`, `--max-wall`), `controls.py` (`JOB_ID`, `TASK_SHA256`), `winjob.py` (`MEMORY_CAP`), all through the binding of §11.7 (RC11); `independent_reference` (called by `error_bound`). **src:** `SeedTree(master).generator(name, *scope)`; `HMMSampler(T, E, pi, layout).sample(n, rng) -> (tokens uint8 [n, 33], states int16 [n, 33])`; `SequenceLayout()`; `make_sequence_ids(code, split, n)`; `process_code(family, mode, sigma, replicate)`; `check_disjoint(**splits)`; `x4f_scores.standardizer(X_fit)`, `rbf_bandwidth(X_std_cal, rng, n_sub=1024)`, `rbf_map(d, n_features, ell, rng)`, `rbf_features(X_std, Omega, b)`; `x4f_probe.nested_ridge(X_cal, Y_cal, panel_cal, X_val, Y_val, grid) -> NestedResult(lam, r2, r2_status, pred_val, fold_mse)`; `RidgeProbe(lambdas).fit(X_fit, Y_fit, X_val, Y_val, splits=…)`, `.predict(X)`; `ArtifactStore`, `LocalFSBackend`, `ObservationSet`, `EmissionSpec` (registry readers). **Not reused:** `c1_data.history_generator/sequence_ids/sample_block/panels/history_table` (hard-coded `c1-sf-v1`, BLOCK 4096, donors); `c1_registry_sources.build` (writes C1′-named files and C1′'s protocol hash); `c1_driver._process` (the R11 str/int defect on main); `c1_fit` (the R13 change; C1′-scoped seeds); `c1_meter_bind`, `c1_release` (C1′ store and mailbox); `error_bound.reference_check_rows` and `certify_rows` (ScoringAuthority) |
| **2. Genuinely missing** | K4b sampling wrapper (own scope, 3,072-row blocks); the registry readers for C1′ digest columns, permitted D-2a pools and other stores; the recursive inventory, handoff-JSON pre-validation, coverage revalidation and the sealed-D-2a alphabet predicate (RC6, RC7); the reservation records and pre-sampling checks (RC8); X± assembly with support; Lemma N; F and the decision rule; the ladder's projection logic; step-0 orchestration; the suffix decoder; releases, freeze, meter binding with the release worker session; the rerun/lineage machinery (§11.8) |
| **3. Smallest change** | A new `tools/k4b/` importing the frozen K4, C1′, job-0014 and src modules unchanged under sha256 binding. No existing file is edited. Private names of reused modules are not imported (the moment check is three lines over the public `reference_moments`; the R10 worker-session check is re-implemented in `k4b_release`, because `c1_release.authorized_worker` exists only at 93350d7) |
| **4. Stable interfaces and invariants** | Int-keyed model maps; ordered sequence_id joins; w33 never stored or read; restart-at-π suffix convention; each chart built once per (model, role, ledger), never refit; gauge on calibration C* m32 only; every row kept; X− ≤ X+ rowwise; one bootstrap index stream for all arrays; every validation and test row certified; every-row registry separation; first non-PASS stops; validation means sealed; exclusive-create writes in stage directories |
| **5. Relevant regression checks** | S0 hash checks. PF suites, unchanged: `tests/circle_history`, `tests/c1prime`, `tests/c1prime_registry`, `tests/oracle_profile`, `tests/oracle`, `tests/dataset`, `tests/contracts`, `tests/prediction`, `tests/analysis`, `tests/experiment`, `tests/learner`; the new `tests/k4b`; `tools/check_file_sizes.py`. The C1′ suite takes about 12 minutes [H] and is run detached |
| **6. Next plausible extension (not built now)** | The same saved-chart interface for an owner-approved confirmation on new histories, or a pre-registered K = 1/2 inferential study. No generic framework |

### 11.4 Test-author independence (L§8.3; X§14)

Two clean-context authors, A and B, work only from the frozen protocol, `API.md`, `CONTRACT.json`, `TEST_PLAN.md` and the reused frozen code. They never read, list or search `tools/k4b/*.py` and execute nothing. Their tests are committed before the module enters the worktree; corrections are made only by each file's own author. **No formatter is ever run over `tests/k4b`** (the module author formats module files by name only). `AUTHORSHIP.md` records what each author read and did not read.

- **Author A (mathematics and certificate):** Proposition 1 by exact Fraction enumeration on a tiny asymmetric stationary HMM (L = 6, K = 2): E[g(S_K)·r_K] = 0 for random suffix tables g, and ≠ 0 for a prefix-dependent g. Theorem A on that HMM with a support set correlated with the prefix and with the residual sign: every completion on a grid and the extremal ones lie in [E X−, E X+]; sharpness; the continuity path; conditioning on S gives a spurious non-zero value while the bounds stay valid. Lemma N against exact rationals, including s = 0, tiny values and adversarial n̂. Lemma T on a toy perturbation with a known κ. `row_bound` at K = 1 and 2. B_num and the decision boundaries: L − F exactly 0.01 is not SUPPORT; U + F exactly 0.01 is not EXCLUDE; the lower side exactly at −0.01; NEGATIVE_ALIGNMENT; UNRESOLVED/NUMERICAL; SUPPORT and EXCLUDE exclusive. Ranks 84, 125, 250, 4,875, 4,917. The cap: 1e-4 passes and the next value above fails. The ladder's projection on synthetic arrays: invariance to mean shifts; the joint count threshold 4,000 of 5,000; UNDERPOWERED.
- **Author B (data, chart reuse, registry and flow):** seed streams and fixed 3,072-row blocks (block content invariant to k); IDs; int-keyed maps; the registry with C1′-style digest columns, a D-2a-style raw-token store and a NOT_SCANNED entry; every collision → FAIL_TECHNICAL/LINEAGE; within-split duplicates kept; `c1_chart` called with the K4b cfg; two ledgers (6 trained, 3 step-0; "direct" refused on the step-0 ledger); valid step-0 INCONCLUSIVE/CHART_UNAVAILABLE is non-gating and recorded as INIT_UNAVAILABLE; FAIL_TECHNICAL in shared chart code or shared integrity machinery stops immediately; production chart and decoder frozen before any validation activation; no gauge or refit on validation or test; GIANT 487 passes and 486 fails, support 507 passes and 506 fails; the sealed file; gate order and first-non-PASS stop; no fresh access without release B; the determinism recheck; the rerun rule of §11.8 (superseded moves, hash restore, refusal on unrecorded prior files).
- **Added in v2 (RU optional suggestion 3; assignment by W).**
  - Author A: the directional error-rate counterexample of RC1, as an analytically specified tail construction, not a simulation-enforced bound (a zero-width setting with E X− = E X+ = 0.01 and an exactly specified, enumerable law of the two one-sided bounds, under which the false-SUPPORT event {L−_j − F > 0.01} and the false-EXCLUDE event {U+_j + F < 0.01 and L−_j − F > −0.01} are disjoint opposite-tail events with closed-form probabilities; the test checks in exact arithmetic that the combined per-model false-claim probability is their sum, exceeds each, and is at most 2α when each is at most α; the nominal bootstrap approximation is not treated as a universal finite-sample bound to be enforced through simulation); the deterministic F_plan (B_constant(1e-4, 4, 12288) against exact rationals, and F_test ≤ F_plan whenever the cap and |X̂| ≤ 4 hold for n ≤ 12,288); the width-preserving diagnostic of §7.6 on synthetic arrays (invariance to C̄; the D̄ shift).
  - Author B: reconstruction of sealed means (a validation report that would allow X̄± = C ± D to be recomputed is refused; no supported contribution or conditional supported mean appears in it); malformed handoff JSON (a parse failure gives INCONCLUSIVE/REGISTRY_INCOMPLETE, never an empty contribution); non-default registry roots (`observation_set_sources` with a non-default root and a matching explicit store reads that root, not main's artifacts); the sealed-D-2a predicate (a history in {0,…,4}³² gives INCONCLUSIVE/REGISTRY_INCOMPLETE, and no sealed token array is opened); interrupted-stage replay (an interrupted stage without a terminal gate record; archive and byte restore; bit-identical regeneration of unaffected artifacts; owner escalation when a correction changes an already computed outcome-bearing quantity or such a quantity was computed at or after the declared failure point; no automatic owner escalation solely because an unchanged outcome-bearing quantity was computed before that point); the actual meter bindings (controls, meter and winjob values after binding; `--max-cpu inf --max-wall inf`; op_guard deadline per operation, not per stage; child TEMP/TMP/TMPDIR on X:; worker session and RUN.lock identity from the release). Test simultaneous overdue-operation/disk conditions with STOP and INVALID: the control reason and state retain precedence. Test HOLD both without a resource failure and with one; preserve latch processing and the returned HOLD state. Test ordinary overdue-operation and disk failures, including unreadable free-space information; the G0 seed-classification rule of RC5 (K4b's own declarations are not prior use; an unclassified hit fails closed).

### 11.5 Commit binding (MD 12 ⚑; the D5 rule)

**Facts (W, read-only git).**
- `git diff --name-status c460e24 93350d7` over the reused paths lists: `M tools/c1prime/{API.md, CONTRACT.json, c1_driver.py, c1_driver_cal.py, c1_fit.py, c1_meter_bind.py, c1_release.py}`; `A tests/c1prime/{test_c_process_keys.py, test_c_release_worker.py, test_c_ridge_tolerance.py}`; and, in `src`, D-2a's `learner/trainer.py` (M) and `learner/multihorizon.py` (present on main only).
- These are the R10 (worker session: `c1_meter_bind`, `c1_release`, CONTRACT `worker_session`, API.md), R11 (`c1_driver._process` int keys) and R13 (`c1_fit`, `c1_driver_cal` tolerance) fixes. **None is in a function K4b reuses.** The C1′ CONTRACT differs only in `resources.worker_session`; its chart section is identical.
- `trainer.py` is imported by `topo_pilot.learner.__init__` but is used only for training; `load_model` (`learner/stage.py`) is identical at both commits.
- Every reused file is byte-identical at both commits (§11.3).
- Main already contains job 0027 (4ac46de) and the committed GAP doc (89b9bab).

**Ruling (F1, RU: adopted).** The reviewed reference is **R_ref = main @ c460e249785a0b0c66633aefb31ace400edd05bb**. It is the minimal correct choice: it already satisfies MD 12, holds the bound GAP doc in tree, and carries every reused function in exactly the bytes C1′ executed at 93350d7. Basing K4b on 93350d7 instead would fork from a side branch that lacks the D-2a merge and the GAP doc, for no change in any reused byte. The lessons of R10, R11 and R13 are applied in K4b's own code (release-bound worker session, int keys, attainable tolerances), not imported. R_ref remains c460e249785a0b0c66633aefb31ace400edd05bb. A housekeeping merge of c1p-0035 can add files inside the protected tests/c1prime directory and therefore need not satisfy the current S0 additions-only allowlist. Keep K4b’s execution lineage based on R_ref with only the registered additions. Any execution lineage containing additional protected-path changes needs a newly reviewed reference or an explicitly reviewed allowlist amendment before data. (RC4; F1 ruled by RU. v1's claim that such a merge could not affect the binding was wrong: the three tests R10, R11 and R13 added under `tests/c1prime` are inside a protected PF test directory.)

**Rule.** At dispatch the exact execution commit H_exec is pinned and recorded. Across the protected paths, the R_ref → H_exec diff may contain only the allowlisted additions. Unrelated main changes outside the protected paths do not invalidate the binding. In this rule R_ref and H_exec name commits.
- **Protected paths:** `src`; the reused files of §11.3 by name, including `tools/x4_circle_history/op_guard.py` (RC11); `tools/x4_circle_history/ERROR_BOUND.md`; `tools/check_file_sizes.py`; `tools/k4b`; the PF test directories of §11.3 field 5; `tests/k4b`.
- **Not protected, checked by content instead:** `tools/c1prime/CONTRACT.json`, whose chart section at H_exec must equal its chart section at R_ref.
- **Allowlist:** new `tools/k4b/*` and new `tests/k4b/*` (including `AUTHORSHIP.md`).
- **Mechanical check:** `git diff --no-renames --name-status R_ref H_exec -- <protected paths>` lists only `A` entries for allowlisted files. Any `M`, `D` or other entry fails S0.

### 11.6 Worktree

A new worktree `topo-pilot-k4b` on branch `k4b-<job>` from R_ref. In it, `PYTHONPATH=<worktree>/src` is set and the venv interpreter runs with `-s` (the editable install otherwise imports main's `src`; C1′ R9).

### 11.7 Store, meter, TEMP and resources (MD 13)

- **Store:** `X:/Downloads/projects/topo-pilot/k4b-store/`, new and verified absent before creation (or holding only this lineage's recorded files, §11.8). Layout: `FREEZE.json`; `registry/`; `stages/<stage>/` (every payload of a stage); `GATES.jsonl`, `STAGES.jsonl`; the two ledgers; `SEALED_VALIDATION.json`; `superseded/`; `logs/`; `cpu_ledger.json`.
- **Meter (RC11).** Reuse the unchanged job-0014 meter, controls and winjob modules through k4b_meter_bind.py. Rebind controls.JOB_ID and controls.TASK_SHA256 to the verified dispatch; rebind meter.OUT, LEDGER, EMERGENCY, LOCK, ACTIVE and LOG_DIR to the K4b store; set meter.CAP_S = meter.STOP_NEW_S = inf, meter.OUTPUT_CAP = 4*1024**3, and winjob.MEMORY_CAP = 12*1024**3. Set meter.WORKER_SESSION from the verified release and require the matching task and RUN.lock identity.

  Force --max-cpu inf and --max-wall inf. Enforce the separate 600-second native-operation deadline and disk safe-STOP through the supervisor limiter, while preserving STOP, INVALID and usage-latch precedence. Reuse op_guard.timed_factory, overdue and archive_stale unchanged; do not apply a 600-second wall to an entire multi-hour oracle stage. Resource stops receive the registered INCONCLUSIVE/RESOURCE classification; control stops retain their control semantics.

  Set the registered single-thread environment and X:-based TEMP/TMP/TMPDIR for every child. PF verifies the actual bindings and child environment before scientific work.

  Capture the original meter.limit_reason before installing the wrapper. Invoke it exactly once at the beginning of every supervisor poll. If it returns a kill reason, return its reason and control state unchanged. Otherwise evaluate the operation deadline and disk safe-STOP, returning any resource reason with the original control state. Never substitute literal CONTINUE for STOP, INVALID or HOLD. HOLD alone does not kill; a registered resource stop may still terminate while HOLD is active. The early-return ordering of c1_meter_bind.make_limiter is not copied.

  (W verified the defaults these rebindings override at c460e24: `controls.JOB_ID = "0014"` and its task hash; `meter.OUT` = the job-0014 store; `CAP_S, STOP_NEW_S = 3600.0, 3480.0`; `OUTPUT_CAP = 128 MiB`; `winjob.MEMORY_CAP = 8 GiB`; `--max-cpu` default 600; `--max-wall` default 3600; the supervisor hook is `meter.limit_reason(ledger, child, args, active_wall, polls, mailboxes)`, which the binding wraps, as C1′'s binding did, without editing `meter.py`. The disk safe-STOP and op-marker limiter are re-implemented in `k4b_meter_bind.py` with provenance from `c1_meter_bind.disk_reason`/`make_limiter` (themselves extracted from K4 `meter_bind`); `c1_meter_bind` is not imported, because importing it loads C1′'s CONTRACT and its file differs between c460e24 and 93350d7.)
- **TEMP on X: (MD 13).** `TEMP`, `TMP` and `TMPDIR` are set for every metered process to `X:/Downloads/projects/topo-pilot/k4b-store/tmp-<job>`; pytest gets `--basetemp` there. PF records `tempfile.gettempdir()` from inside a metered child. No output or cache is written to C:.
- **Limits:** RAM 12 GiB (`winjob.MEMORY_CAP`, owner policy); output ceiling 4 GiB (`meter.OUTPUT_CAP`; F12 ruled by RU); native-operation wall 600 s per operation (op_guard); disk safe-STOP at C: < 2 GB or X: < 30 GB. CPU and total wall time are measure-only and never a stop.

### 11.8 Rerun and lineage rule (fixed in advance; U6)

1. **Stage directories.** Each stage writes its payloads by exclusive create (`write_new`, `save_npz`) inside `stages/<stage>/`. The driver writes an operation marker before the stage and a STAGE_COMPLETE record with the sha256 of every file after it.
2. PASS gates and valid INCONCLUSIVE gate outcomes are final. A valid non-PASS scientific or feasibility criterion ends the cohort and is never rerun. FAIL_TECHNICAL and incomplete interrupted attempts remain stopped unless the narrow technical-correction rule below applies.

3. A coordinator may authorise a technical correction only for a documented K4b implementation or environment defect. The ruling names the defect, correction commit, affected stage, exact artifacts to supersede and evidence that the correction is independent of the scientific outcome. At most two correction jobs are allowed per defect. This rule includes an interrupted stage without a terminal gate record when the interruption is attributable to the documented defect.

4. Earlier PASS stages remain immutable. Archive the complete failed attempt and its appended record suffixes under superseded/<job>/ with hashes, restore the active record files to their verified pre-attempt bytes, and restart only the affected stage with the frozen seeds. Completed artifacts unaffected by the correction must regenerate bit-identically. Any mismatch is FAIL_TECHNICAL/LINEAGE.

5. If the correction would change an already computed outcome-bearing quantity, or the failed attempt computed such a quantity at or after its declared failure point, a coordinator ruling is insufficient: an owner decision is required. This includes B4 bounds, chart-validation criteria, SD bounds, N and endpoint/control/descriptive means. No threshold or tolerance may change under this rule.

6. A valid failed chart construction is never re-attempted. Previously completed constructions may only be regenerated bit-identically under the original claim and construction limit. After release B, no repair changes the method or introduces replacement data; any permitted replay reproduces the frozen data and all unaffected completed artifacts.

(Items 2–6 are RC9's text; F14 ruled by RU. "First non-PASS stops" means an immediate stop throughout, with only this documented technical-correction exception. The superseded archive carries a `SHA256SUMS` manifest; the ledger claims of a superseded attempt move with it, as in C1′ R14.)

7. **G0 recognises lineage.** G0's "scope unused" and "no prior K4b store" checks accept exactly the files listed in this lineage's superseded manifests, and nothing else.
8. A technical tolerance is never changed under this rule (§5.6; F13).

---

## 12. Staged plan and CPU forecast (MD 13; forecasts, not caps)

| Job | Content | Gates | Forecast |
|---|---|---|---|
| I (implementation) | Contract; independent tests A and B; modules; PF; freeze (`FREEZE.json` with every bound hash). No data | S0 (at the freeze commit), PF | 15–25 CPU-min of suites [H: C1′ suite ≈ 12 min] |
| E1 (release A) | G0, H1, REG1, S3 sampling, H2, ORACLE-VAL, B4-VAL, C0-cal (+ step-0 charts, decoder), C0-val, CERT-VAL, P1; validation report | rows 0–9 | see below |
| — | Coordinator review and ACCEPT; K-REG2 identity-only step; release B | row 10 | ≤ 5 min [H: job 0027] |
| E2 (release B) | Test sampling, H2-FRESH, T-PRE, ENDPOINT; report | rows 11–13 | see below |

**Execution forecast (E1 + E2 + K-REG2; single thread).**

| Item | N = 3,072 | N = 12,288 | Basis |
|---|---|---|---|
| Decimal references, K = 1, 2, 4, 32, on 3,072 validation + N test + 4 calibration rows, at 0.3–0.5 CPU s per history | 0.51–0.85 h [W] (6,148 histories) | 1.28–2.13 h [W] (15,364 histories) | Rate [H]: job 0018 took 300.5 s for 1,024 histories × 3 Ks (0.29 s each [W]); X's record 0.094 + 0.328 s for K4 + K32 |
| Forward passes, 6 checkpoints × (6,144 + N) histories | 5–20 min | 10–30 min | [H] L |
| Sampling, registries, process law, float oracle | 5–10 min | 10–15 min | [H] jobs 0016, 0027 |
| Charts (≤ 9) and extensions | ≤ 5 min | ≤ 5 min | [H] jobs 0018, 0023, 0044 |
| Taylor certificates (about 15–20 phases per row) | 2–5 min | 5–15 min | [H] |
| Bootstraps and projections | 2–5 min | 5–10 min | [H] |
| **Total** | **≈ 0.9–1.6 CPU-h** [W] | **≈ 1.9–3.3 CPU-h** [W] | N = 6,144: ≈ 1.2–2.2 CPU-h [W] |

The upper end at N = 12,288 slightly exceeds MD 13's 1–3 CPU-h; the expected N is 3,072 (§7.3). RAM is expected below 2 GB and the store below 300 MB [H]. CPU is measured and reported per stage; an overrun is reported, never a stop.

---

## 13. Stop rules

1. The first non-PASS gate ends the cohort immediately; the only exception is the documented technical-correction rule of §11.8 (RC9). Outputs, exact values and negative findings are kept; nothing is deleted. A FAIL_TECHNICAL in shared chart code or shared integrity machinery, including during a step-0 construction, stops the cohort immediately (RC10).
2. No retry, refit, re-sampling, replacement, threshold or tolerance change, other K, site, layer, checkpoint, harmonic or chart family. At most nine constructions (6 trained, 3 step-0), each once. The production charts, gauges and decoder are frozen before any validation activation and never change.
3. UNDERPOWERED, HEADROOM, CHART_UNAVAILABLE, NUMERICAL, REGISTRY_INCOMPLETE, AUTHORITY and RESOURCE are INCONCLUSIVE outcomes with recorded reasons; none is an effect-zero finding.
4. Fresh data are sampled only under release B, after the coordinator's ACCEPT and the K-REG2 freeze, inside the enforced W2 reservation and with the W3 record (RC8). After fresh exposure no repair may change the method or bring in replacement data; integrity defects are FAIL_TECHNICAL.
5. Validation means, and every reported quantity that directly reconstructs them, stay sealed until the fresh result is recorded (§7.5, RC3).
6. No K4b sampling while the window conditions of §3.5 fail. No K4b change follows a C1′ or D-2a outcome without a new version and review.
7. A defect in, or a change to, any reused frozen file stops the run for review. K4b never edits a frozen file.
8. No threshold or tolerance changes after any K4b data exist; a frozen criterion that would need to change stops the run and waits for the owner (C1′ §19.3, §19.8; addendum 10; F13 ruled by RU).
9. Technical corrections are permitted only under §11.8, at most two correction jobs per defect. An owner decision is required if the correction would change an already computed outcome-bearing quantity, or an outcome-bearing quantity was computed at or after the declared failure point. An unchanged quantity computed before that point does not by itself require an owner decision. Earlier PASS stages remain immutable.
10. Usage limits, STOP and INVALID channels, the disk safe-STOP, the output ceiling and the operation wall always win. No silent restart.
11. K4b results are never pooled with K4, C1′ or E4 results.
12. Sealed D-2a test and testN tokens are never opened under this protocol (RC6).

---

## 14. Risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | The chart fails on fresh validation data (C1′ never tested C0-val) | INCONCLUSIVE/CHART_UNAVAILABLE is a legitimate outcome; GIANT is likely to pass (job 0023 minimum giant fraction 0.998; C1′ 512/512 [H]) |
| 2 | A true but small Δ4: a noisy phase attenuates it relative to Δ_ideal^orc ≤ B4 ≈ 0.067 [H] | UNRESOLVED or MIXED are legitimate results |
| 3 | A wide identified set (low support or atypical unsupported rows) | Reported at validation; not gated (F5) |
| 4 | Negative alignment | Not EXCLUDE (two-sided); NEGATIVE_ALIGNMENT flag |
| 5 | Step-0 control positive or unavailable | Pre-registered qualifier; nothing subtracted |
| 6 | Code drift in reused files | S0 hash binding; stop and review |
| 7 | Another study generating histories inside K4b's window | §3.5 enforced W2 reservations (K-REG1 and K-REG2) and the W3 record (RC8); K-REG2 rebuilt from scratch |
| 8 | Heavy tails of ‖r4‖ (up to 1.14 seen in job 0014 [H]) | SD upper bound; projection; nominal bootstrap levels stated |
| 9 | Overclaiming "long memory" or "use" | Licences tie the claim to "earlier than the last four observations"; the historical B8 is cited only as motivation, never as a horizon (RC15) |
| 10 | Float64 versus float32 activations (job 0023 used float32) | The inherited §14 mapping classifies filtration-boundary cases |
| 11 | Decimal-reference cost at N = 12,288 | Measure-only; reported |
| 12 | Unattainable technical tolerance (the R13 pattern) | §5.6 table fixed now; no solver-equivalence gate |
| 13 | Partial files blocking reruns (the job-0039 pattern) | §11.8 |
| 14 | Editable-install trap and TEMP on C: | §11.6, §11.7; PF records `gettempdir` |
| 15 | Forecasts or [W] values treated as findings | Labelled; never gates |

---

## 15. Parameters for the reviewer to scrutinise (all fixed; changes only before any K4b data)

1. Margin 0.01; planning alternative 0.02 for SUPPORT and E X± = 0 for EXCLUSION; power 0.80 per model and jointly; α = 0.05/3 per one-sided bound; 5,000 draws; ranks 84, 4,917, 250, 125, 4,875.
2. Two-sided EXCLUDE (MD 6) and the NEGATIVE_ALIGNMENT label.
3. F = max(B_num, 1e-9) + Z_bound (MD 5); the deterministic F_plan = max{B_constant(1e-4, 4, 12288), 1e-9} + Z_bound in the ladder (§7.1; F6 closed by RU); B^H + Z_bound in `guard_H5` (F7).
4. Calibration and validation at 3,072 rows; 512-row chart panels; the ladder {3,072, 6,144, 12,288} in fixed blocks.
5. The C1′ chart thresholds: GIANT ≥ 487/512, support ≥ 507/512, fidelity ≥ 0.80, 12 bins ≥ 8, resultant ≤ 0.30, extension support at resultant ≥ 0.2 and 8th-NN ≤ R; nine constructions.
6. The certificate: cap 1e-4; moment tolerance 1e-10; Lemma N with D = 10⁸⁰ and (3/2)(ε4 + ε32).
7. The validation B4 gate (lower 95% bound > 0.01); fresh B4 report-only.
8. The registry sources (a)–(f), with sealed D-2a pools covered by the alphabet predicate (RC6) and the fail-closed recursive inventory (RC7); the window rules W1–W3 with enforced reservations (RC8).
9. The decoder specification and call contract (§9.4, RC13) and the absence of a fallback (F8).
10. No width gate (F5); the zero-width projection's qualification and the width-preserving diagnostic (§7.2, §7.6).
11. The technical-correction rule (§11.8, RC9) and the tolerance-governance rule (F13).
12. Seeds 610101–610105 and scope `k4b-sf-v1`, with the G0 classification rule (RC5).
13. The error-rate statement of §8.3 (RC1: 2α per model, 6α = 0.10 for any false definite claim, 0.05 per directional family).
14. The meter bindings (§11.7, RC11).

---

## 16. Changelog, corrections and arithmetic re-checks

### 16.1 Section sources

| Section | Source |
|---|---|
| Header, U1–U6 | MD; AN; the coordinator's brief to W; jobs 0033, 0039, 0042, 0044; addendum 10; git (W) |
| §1 | L§1, §3; X§2, §5; AN §1.1–1.3; Lemma T from AN §1.1 and EB §6 (W statement and proof) |
| §2 | L§0.1–0.2; X§1; MD 14; W's metadata check |
| §3 | L§0.3–0.4, §2.3; X§3; MD 2, 3, 10; AN D5, D12; C1′ §2.4; `c1_registry_sources` |
| §4 | L§2; X§4; MD 2, 8, 11; C1′ §14; jobs 0042, 0044 |
| §5 | L§4.2; X§6; AN §1.4–1.5; MD 4, 5; C1′ §15.3.11; EB; R13 (job 0042) |
| §6 | L§4.1; X§17; MD 9; C1′ §16 pattern |
| §7 | L§5; X§8; MD 7; AN §1.6, D9 |
| §8 | L§6; X§9–10; MD 6, 15 |
| §9 | L§7; X§11; MD 8; AN D10, D11; U5 |
| §10 | L§4.4; X§12; AN §1.3 |
| §11 | L§8; X§13–16; MD 12, 13; D2A §11.3; X6-MERGED-v1 §10.5; C1′ §18; U3, U6 |
| §12 | L§8.4; X§16; AN §2 (cost row); MD 13 |
| §13 | L§9.1; X§17; C1′ §19 |

### 16.2 Corrections and W decisions

| # | Item | Resolution |
|---|---|---|
| C1 | L§5 "80% planned power for each side of EXCLUDE at Δ = 0" | **Error** (MD; AN §1.6). Planning point E X± = 0; per-model two-sided power ≥ 60%; joint not planned. Corrected in §7.4; joint projection added (MD 7). v2: accepted by the review with RC14's normal-planning and zero-width qualifications (§7.2, §7.4) |
| C2 | L§2.1 "K4b CONTRACT chart section equals the C1′ one key for key" | Not satisfiable (nine constructions; own landmark source; C1′ descriptive keys mention M3). Replaced by equality of `chart_cfg()` output and of `giant`/`val_support` (§4.2; F9, ruled) |
| C3 | L's base commit (df06d5f or main) and "`tools/c1prime_registry/` untracked" | Stale (AN). Job 0027 is in main; R_ref = c460e24 (§11.5; F1, ruled), subject to RC4's housekeeping/S0 correction |
| C4 | L's fresh B4 gate in T-PRE | Removed (MD 9); reported with FRESH_B4_LOW |
| C5 | L's F = max(B_num, 1e-9) without Z_bound | Replaced by MD 5; Theorem B′ restated with Lemma T. v2: its conclusions are one-way implications and coverage-event inclusions, not decision equivalence (RC2) |
| C6 | X's 512/512 calibration and validation | Replaced by 3,072/3,072 (MD 3) |
| C7 | X's ε₀ = 1e-4 allowance and exact dyadic means | Replaced by the C1′ tree mean and B_num (MD 4) plus F (MD 5) |
| C8 | X's reporting of E[A·u·r4] without a caveat | Labelled diagnostic, not null-protected (§10; AN §1.3). v2: its validation versions are sealed (§7.5, RC3) |
| C9 | X's 12 constructions | Nine (MD 8) |
| C10 | X's KRR decoder; L's decoder target ("supported calibration rows", 3 panels of 1,024, variable sizes) | Target per AN: all 2,560 non-landmark cal rows, including unsupported rows; 5 panels of 512 (W); no KRR fallback (F8, ruled); full call contract (§9.4, RC13) |
| C11 | L's "owner's queue order" (C1′ → D-2a → K4b) | Overstated per AN (addendum 3 ordered C1′ before D-2a only); MD 10 fixed the order; both preconditions now met (U1, U2) |
| C12 | MD 11 branches | Did not occur (U1); disclosure in §4.5 (F2, ruled) |
| C13 | MD 12 "main after job 0027" | Already true at c460e24 (U3); verified by the review |
| C14 | MD 14 | Done at 89b9bab (U4); GAP hash verified by the review |
| C15 | L's 8 files | v1 said "10 module files plus the meter binding", which miscounted its own table. v2: eleven configuration/orchestration/scientific modules plus the meter binding, twelve Python files (§11.1; RC12; F11, ruled) |
| C16 | L's CPU forecast 0.5–1.6 CPU-h | Low per AN; revised to 0.9–3.3 CPU-h (§12); a forecast, never a cap |
| C17 | L's single-ledger wording | Two ledger files; "direct" refused on the step-0 ledger (§4.3) |
| C18 | L's seeds; X's 5406xx | L's 610101–610104 kept; 610105 added for the projection (F10, ruled); G0's non-use check is the classification rule of RC5 |
| C19 | The determinism recheck | Specified as the identical call, so bitwise equality is attainable (§5.6) |
| C20 | Lemma N | X's integer bracket with L's (3/2) constant (AN §1.4); verified by the review |
| C21 | X's "no open questions" | Superseded; every v1 open item is now ruled and closed in §17; residual items in §18.4 |
| C22 | X's sequencing ("does not reorder the queue") | Superseded by MD 10 and §3.5, strengthened by RC8's enforced reservations |
| C23 | X's `INITIALISATION_CHART_UNAVAILABLE` naming | Valid step-0 unavailability is recorded as INIT_UNAVAILABLE (non-gating); a shared-code technical defect stops immediately (RC10) |

### 16.3 Arithmetic re-checks [W]

- z_{1−0.05/3} = 2.128045, z_{0.80} = 0.841621, z-sum 2.969666 (L's 2.9696 confirmed); z_{1−0.2/6} = 1.83391; z_{1−0.2/3} = 1.50109.
- Ranks: 5000·5/300 = 83.33 → 84; 5000·295/300 = 4916.67 → 4917; 250, 125, 4,875 (AN and the review confirmed).
- √N: 55.4256, 78.3837, 110.8513. v1 limits (ignoring F_plan): MDE SD 0.18664, 0.26395, 0.37328; union-bound joint, exclusion 0.13989, 0.19784, 0.27979; support 0.15272, 0.21598, 0.30545.
- **v2, deterministic F_plan.** u = 2⁻⁵³ = 1.1102230e-16; d_n for n = 12,288 is bit_length(12287) = 14; γ₁₅ = 15u/(1 − 15u) = 1.6653345e-15; γ₁₅·4 = 6.661338e-15; 1e-4·2⁻³⁰ = 9.313226e-14; ζ = 2⁻⁸⁰⁰ ≈ 1.5e-241. B_constant(1e-4, 4, 12288) = 1e-4 + 9.979360e-14 + 2ζ ≈ 1.0000000009979e-4. With Z_bound = 2.12e-12 [H]: F_plan ≈ 1.0000000222e-4.
- **v2 limits with F_plan:** MDE SD 0.18477, 0.26131, 0.36955; union-bound joint, exclusion 0.13850, 0.19586, 0.27699; support 0.15120, 0.21382, 0.30239.
- SD = 0.11, N = 3,072: se = 0.0019846; v2 threshold (0.01 − F_plan)/se − 2.1280 = 2.8603, one-sided failure ≈ 2.1e-3, six-event union ≈ 0.013 (v1: 1.8e-3, 0.011). mde(0.11, 3,072) = 0.01589 with delta 0.01.
- √V4 [from H]: √0.007213 = 0.0849, √0.008913 = 0.0944, √0.012058 = 0.1098.
- 0.95·512 = 486.4 → 487; 0.99·512 = 506.88 → 507. √2 = 1.414214 < 1.5.
- Job 0018 reference rate: 300.52/1024 = 0.2935 s per history (3 Ks). Reference histories: 6,148 / 9,220 / 15,364; at 0.3–0.5 s: 0.51–0.85 h, 0.77–1.28 h, 1.28–2.13 h. Execution totals 0.86–1.55 h, 1.20–2.20 h, 1.86–3.30 h.
- RC1 error-rate bounds: 2α = 0.0333 per model; 6α = 0.10 over three models for any false definite claim; 3α = 0.05 per directional family.

---

## 17. Flags: all ruled (RU, 2026-10-16) and closed

No item remains open. Every flag below points to its ruling and to where v2 implements it. Items still worth a look in the confirmation round are listed in §18.4.

| # | Item | Ruling (RU) | Implemented in |
|---|---|---|---|
| F1 | MD 12 ⚑ base commit | **R_ref = main c460e24, adopted** (RC4). The housekeeping-merge claim is corrected: a c1p-0035 merge adds protected `tests/c1prime` files, so any such lineage needs a newly reviewed reference or a reviewed allowlist amendment before data | §11.5; MD table row 12 |
| F2 | MD 11 ⚑ did not trigger | **Disclosure only**; no failed-chart qualifier | §4.5 |
| F3 | MD 10 ⚑ D-2a test pools | **Do not open sealed test or testN tokens.** Coverage by the {0,…,4}³² alphabet predicate (RC6). A terminal status is not authority to unseal | §3.4 (e), §3.4 requirements, §6 rows 3 and 11, §13 item 12 |
| F4 | "Every store present" | **Expanded recursive inventory, fail-closed** (RC7) | §3.4 (f) and "Fail-closed completeness"; §11.3 |
| F5 | Width-aware planning | **No width gate** (RC14); the zero-width projection is qualified; the width-preserving diagnostic is report-only | §7.2, §7.6 |
| F6 | F_plan | **Closed by the deterministic worst-case F_plan** = max{B_constant(1e-4, 4, 12288), 1e-9} + Z_bound (RU optional suggestion 1) | §7.1, §7.3, §16.3 |
| F7 | B4 guard with transport | **guard_H5(lower, B^H + Z_bound), adopted** | §5.5 clause 4; §6 row 5 |
| F8 | Decoder family | **Fixed descriptive family, no fallback**, with the full call contract (RC13) | §9.4 |
| F9 | Contract equality | **Kernel-config and gate-rule equality, adopted** | §4.2 |
| F10 | Projection seed | **Seed 610105, adopted**; non-use checked by RC5's classification rule | §3.2, §6 row 0 |
| F11 | File count | **Twelve Python files** (RC12) | §11.1 |
| F12 | Output ceiling | **4 GiB via `meter.OUTPUT_CAP`, adopted** | §11.7 (RC11) |
| F13 | Tolerance governance | **Adopted:** any post-data change of a threshold or tolerance needs the owner (consistent with addendum 10) | §5.6, §11.8 item 8, §13 item 8 |
| F14 | Rerun and lineage rule | **RC9's technical-correction rule** | §11.8 items 2–6 |
| F15 | Shared-code FAIL_TECHNICAL during a step-0 construction | **Immediate stop** (RC10) | §6 notes and row 6, §9.3, §13 item 1 |
| F16 | Window attestations | **Attestations plus the enforced registry-to-draw reservations** (RC8) | §3.5 W2, W3; §6 sampling rows, rows 10–11 |
| F17 | C1′ HIST digest columns | **Identity columns only, including superseded histories, adopted** | §3.4 (d2) |
| F18 | Idealised sampler law | **Accepted conditionally; the idealisation is stated in every licence** (RC15) | §5.5, §8.4 (before each template) |
| F19 | Independent review | **The Codex review satisfies rule 4; a confirmation round follows** | Header "Next step" |

---

## 18. v1→v2 changes

### 18.1 Required changes (all adopted as written, RU)

| RC | Change | Location in v2 |
|---|---|---|
| RC1 | Error rates: α per claim type, 2α per model, 6α = 0.10 over three models for any false definite claim, 0.05 per directional family, α per overall verdict, 2α for their union | §8.3 replaced (verbatim, plus a closing parenthetical) |
| RC2 | Theorem B′: one-way soundness, not decision equivalence | §5.5 clause 2 last sentence; clause 3 last sentence; clause 4 appended sentence (HEADROOM); "Certified" bullet replaced |
| RC3 | Sealing covers reconstructing quantities | §7.5 replaced; §10 final paragraph appended; §13 item 5 conformed |
| RC4 | Housekeeping merge and S0 | §11.5 housekeeping sentence replaced; "Ruling (F1)" heading; MD table row 12; F1 |
| RC5 | G0 seed and stream non-use as a classification rule | §6 row 0 (criterion replaced); §3.2 conformed; F10; §11.4 Author B test |
| RC6 | Sealed D-2a pools by the alphabet predicate | §3.4 (e) replaced; §3.4 requirements paragraph; §6 rows 3 and 11 (criterion and status); §11.1 registry row; §11.3 field 2; §13 item 12; F3 |
| RC7 | Fail-closed registry completeness | §3.4 (f) wording; "Fail-closed completeness" paragraphs after the manifest paragraph; §11.3 field 1 (`handoff_sources`, `history_index_ids`, `coverage`, explicit `store`) and field 2; §11.1 registry row; F4 |
| RC8 | Registry-to-draw reservation | §3.5 W2 replaced, W3 paragraph appended; §3.4 K-REG2 paragraph; §6 row 0, S3 and S7 sampling rows, rows 10 and 11; §11.1 release row; §13 item 4; §14 risk 7; F16 |
| RC9 | Technical-replay rule | §11.8 items 2–6 replaced (verbatim, plus a parenthetical keeping the SHA256SUMS manifest and ledger move); §6 notes ("first non-PASS stops" read as an immediate stop); §13 items 1 and 9; F14 |
| RC10 | Immediate stop on a shared-code technical defect | §6 notes (verbatim) and row 6; §9.3 (verbatim); §13 item 1; F15 |
| RC11 | Meter and op_guard bindings | §11.7 meter bullet replaced (verbatim, plus W's verification of the defaults and the limiter provenance), Limits bullet; §11.3 hash-table row, binding paragraph and field 1; §11.5 protected paths; §11.1 meter-binding row; header code-read row; F12 |
| RC12 | Twelve Python files | §11.1 (table split into `k4b_release.py` and `k4b_meter_bind.py` rows; RC text verbatim); C15; F11 |
| RC13 | Reused-call contracts | §7.1 "Reused-call contract" bullet (verbatim); §9.4 "Call contract" sub-bullet (verbatim); F8 |
| RC14 | Power and planning qualifications | §7.1 planning-allowance bullet (adapted, §18.3); §7.2 appended paragraph (verbatim); §7.4 appended paragraph (verbatim); F5, F6 |
| RC15 | Narrowed licences | §8.4: idealisation text inserted before the SUPPORT and the EXCLUSION templates, item 1 replaced; §8.5 E5 replaced (E2 conformed); §9 item 6 ("§9.6") replaced; §9.5, §14 risks 2 and 9 conformed; F18 |

### 18.2 Optional suggestions adopted (RU)

| Suggestion | Location in v2 |
|---|---|
| Deterministic worst-case F_plan = max{B_constant(1e-4, 4, 12288), 1e-9} + Z_bound | §7.1 (definition, [W] value and monotonicity argument), §7.2 (used in both rules), §7.3 (limits recomputed), §6 row 9, §15 item 3, §16.3; closes F6 |
| Width-preserving exclusion-power diagnostic, report only | New §7.6; referenced from §7.2, §7.5 and §6 row 9 |
| Extra independent-test cases (directional error-rate counterexample; sealed-mean reconstruction; malformed handoff JSON; non-default registry roots; interrupted-stage replay; actual meter bindings) | §11.4 "Added in v2" (W also added tests for the F_plan bound, the §7.6 diagnostic, the D-2a predicate and the RC5 classification rule) |
| Keep the existing narrow licences | §8.4 unchanged apart from RC15 |

Other v2 edits: title and header (protocol id, review row, code-read verification, next step); §16.2 rows C1, C2, C3, C5, C8, C10, C12–C16, C18, C20–C23 conformed; §16.3 v2 arithmetic; §15 items 3 and 8–14; §1.4 cross-reference to §8.3.

### 18.3 Where v2 departs from a reviewer replacement text

1. **RC14, the §7.1 append.** The reviewer's first two sentences read: "F_plan is a validation-based planning allowance, not a certified upper bound on the future test allowance. B_num can change with n and with the future maximum row certificate." They describe v1's validation-based F_plan. The coordinator then adopted the reviewer's own optional suggestion of a deterministic worst-case F_plan, which **is** an upper bound on every fresh F whenever the registered cap and |X̂| ≤ 4 checks pass at any n ≤ 12,288. Keeping those two sentences would make §7.1 false. v2 replaces them with the statement of when the bound holds and why (monotonicity of OUT, γ_k and B_constant), and keeps the reviewer's third sentence verbatim: "This is part of the planning approximation and does not alter the fresh numerical guard." No other RC text was changed. Some RC texts carry short appended parentheticals (RC1, RC3, RC9, RC11, RC15) or were placed inside a table cell (RC5), without changing their wording.

### 18.4 Residual items (all resolved in the v2 confirmation)

| # | Item | Recommendation | Resolution (`coord-k4b-review-20261016.v2confirm.codex.md`; coordinator adoption) |
|---|---|---|---|
| R1 | The adapted RC14 §7.1 sentence (§18.3) | Accept; it follows from the adopted deterministic F_plan | **Resolved: accepted.** The reviewer re-derived B_max = B_constant(1e-4, 4, 12288) ≈ 1.000000000997936e-4 and F_plan ≈ 1.000000022197936e-4 (with the illustrative Z = 2.12e-12), and confirmed F_{j,s} ≤ F_plan whenever the cap and \|X̂\| ≤ 4 checks pass |
| R2 | The sealed-D-2a sequence-ID ranges are derived from `tools/d2a/API.md` (SEQ_CODE·2³² + arange(n)) and the n recorded in `pools.json`; W checked the rule read-only but not the pool sizes | The implementation job records the derivation in the registry manifest; an underivable range is REGISTRY_INCOMPLETE (RC6), so no protocol change is needed | **Resolved: accepted.** The reviewer checked the sizes: test n = 65,536, range 73,014,444,032–73,014,509,567; testN n = 16,384, range 81,604,378,624–81,604,395,007. Codes come from the frozen API/source POOLS order, not JSON key order; the metadata is bound and revalidated at registry construction |
| R3 | The supervisor limiter is re-implemented in `k4b_meter_bind.py` with provenance from `c1_meter_bind`, not imported | Accept; record the provenance in API.md and test it under the actual-binding test of §11.4 | **Resolved: accepted subject to confirmation change 3,** now applied: the precedence contract appended to §11.7 and its tests appended to §11.4 |

### 18.5 v2→v3 changes (the Codex v2 confirmation, VERDICT CONFIRM_WITH_REQUIRED_CHANGES, items 1–4, adopted as written by the coordinator)

| Item | Change | Location in v3 |
|---|---|---|
| 1 (RC9 conformance) | §13 item 9 replaced with the reviewer's text; the §11.4 "interrupted-stage replay" test item replaced with the reviewer's text | §13 item 9; §11.4 "Added in v2", Author B |
| 2 (RC10 conformance) | "step-0 failure non-gating" in Author B's original test list replaced with the reviewer's text | §11.4, Author B |
| 3 (limiter precedence) | The reviewer's precedence contract appended to §11.7's meter specification; its three test sentences appended to the §11.4 actual-meter-binding tests | §11.7 meter bullet (last paragraph); §11.4 "Added in v2", Author B |
| 4 (§7.6 interpretation) | Opening paragraph, "Hypothetical" bullet and "Never gated" bullet replaced with the reviewer's texts; the formula and report-only status are unchanged | §7.6 |
| Note under the RC table | The directional error-rate counterexample test now specifies an analytically defined tail construction, not a simulation-enforced bound | §11.4 "Added in v2", Author A |
| R1–R3 | Marked resolved with the reviewer's acceptance | §18.4 |
| Identity | Title, protocol id, role row (files written) and next-step row updated to v3 | Header |

No other text changed. No reviewer text was adapted in v3.

## Freeze record (coordinator)
- **Source:** K4B-MERGED-v3.md (sha256 BE734BF45AFCC3984C2AC52D25E42EAA6ADDAF9CB8BB87BF599747E3B5E4EA0C). Only the STATUS line and this record differ from it.
- **History:**
  - **v1** (63120E93…6C96): writer, from MERGE decisions MD 1–15.
  - **Codex review** (`coord-k4b-review-20261016.codex.md`): APPROVE_WITH_REQUIRED_CHANGES, RC1–RC15.
  - **Coordinator rulings** (`coord-k4b-review-20261016.rulings.md`): every RC adopted; F1–F19 as recommended; three optional suggestions adopted.
  - **v2** (3DEA3723…AB52).
  - **Codex v2 confirmation:** CONFIRM_WITH_REQUIRED_CHANGES (items 1–4; R1–R3 accepted).
  - **v3:** items 1–4 verbatim. The coordinator checked that the v2→v3 diff has only the 13 listed hunks (`K4B-MERGED-v2-v3.diff`).
  - **Codex v3 confirmation:** CONFIRM_FOR_FREEZE.
- **Authority:**
  - OWNER_DECISIONS.v1-a73c869.md (5BD1FDB0…37CD);
  - addendum 3 (222578FE…38A4; queue order);
  - addendum 9;
  - addendum 10 (e28bde0c…22a2; C1′ closed, next track K4b).
- **Code reference:** R_ref = main c460e249785a0b0c66633aefb31ace400edd05bb. The reused files are byte-identical at c1p-0035 93350d7 (checked by the writer and by Codex).
- **Planning precondition MD 10 is satisfied:** C1′ is terminal (job 0044) and D-2a is terminal (job 0033). Registry windows W2/W3 apply from the first K4b registry build.
- **Execution:**
  - **Implementation job first:** the twelve Python files of §11.1, each at most 400 lines, with an independent test author per §11.4. A coordinator full suite at the tip, then review, then a code freeze.
  - **Then stage jobs, one stage per job,** under releases A and B, measure-only (`--max-cpu inf`), on one thread, with TEMP on X:.
- **Post-data changes:** any change to a threshold or tolerance after K4b data exist needs the owner (F13; owner addendum 10).
