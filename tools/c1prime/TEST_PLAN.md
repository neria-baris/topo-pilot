# C1′ test plan (job 0026; S1 independent tests, synthetic fixtures only)

**Authority.** The tests are derived from `PROTOCOL_C1PRIME_v1.md` (sha256 0B1F107E…F33A; the protocol wins), `API.md`, `CONTRACT.json` and `CERTIFICATE.md`.

**Authors.** Two independent clean-context authors, A and B. Each writes tests from the protocol and these four documents, plus the production and reference code the tests call (§18 field 1).
- They never read, list or search `tools/c1prime/*.py`. `materialise_protocol.py` is the only exception: it is not module code, and the authors may ignore it.
- They execute nothing.
- Each records an AUTHORSHIP file: `tests/c1prime/AUTHORSHIP_A.md` and `AUTHORSHIP_B.md`.
- The builder runs the tests under the meter.

**Author split.** The dispatching task divides the work as below. Every item of protocol §17 ("S1 test lists") and §15.3.16 is assigned to exactly one author, so the union covers both lists.

**Files.**
- Author A: `tests/c1prime/test_a_*.py`.
- Author B: `tests/c1prime/test_b_*.py`.

Each file is at most 400 lines, ruff line length 100, Python 3.10. Synthetic fixtures only: no artifact store, no checkpoint, no mailbox access, no network. Store-writing tests use pytest's `tmp_path`.

**Runtime.** The whole suite runs in at most about 10 minutes on one thread. Fixtures are small; the 512-landmark chart fixtures are the largest.

## Author A: the chart, the oracle checks, eligibility, support, and the gate table

**A-1 Chart wrapper `fit_chart_lcc` (§14; protocol §17 Author B list as reassigned).**
1. On a connected fixture, `fit_chart_lcc` equals `chart.fit_chart` bitwise in every array and scalar field. Only `info` differs, by the added keys.
2. Component selection is deterministic: the largest component, with ties to the component containing the smallest index. The cocycle restriction and re-indexing keep ids ascending and edges lexicographic.
3. GIANT: 487/512 passes and 486/512 fails. The failure is INCONCLUSIVE/CHART_UNAVAILABLE with reason GIANT_BELOW_0.95. The pre-raise record (b, d, r, k, ℓ_max, the component count and sorted sizes, the excluded ids, m and the outcome) is persisted before the failure, and also when GIANT passes.
4. A trivial restricted class stops: Unresolved, giving INCONCLUSIVE/CHART_UNAVAILABLE.
5. Excluded landmarks are extension-only. They get their phase from `extend_phase`, are never neighbours or gauge points, and remain rows.
6. A 512-row fixture with an isolated point and nonconstant neighbour distances: d8, σ and support_radius computed on C* differ from those computed on all 512 rows. The wrapper uses exactly `chart._neighbor_scale(D[np.ix_(C*, C*)])`.
7. The six-construction limit and immutability (`ConstructionLedger`): no second claim of the same (model, role), and no seventh construction.
8. C0-val (`c0_val`):
   - support 507/512 passes and 506/512 fails;
   - fidelity uses the complete direct retained component, unmasked by support;
   - bins and resultant use all 512 queries;
   - `chart_gates` is not called.
9. The persistence order of step 10 (lift kind, then g, then smoothing residual), and record preservation on failure.

**A-2 Chart exception mapping (§14; c1prime-v1-rulings 1, 2, 6), exercised through `run_c1_gate(..., chart=True)`.**
- The filtration-boundary cocycle error → INCONCLUSIVE/CHART_UNAVAILABLE.
- Smoothing with finite f and a finite residual > 1e-8 → INCONCLUSIVE/CHART_UNAVAILABLE.
- Non-finite f, a NaN or infinite residual, or unavailable diagnostics → FAIL_TECHNICAL.
- Input, lineage, hash, integer-certificate and other integrity defects → FAIL_TECHNICAL.

**A-3 Donors and oracle checks (§3; protocol §17 Author A).**
- The donor transform τ_k with w32 kept.
- The symmetry checks on a tiny periodic HMM.
- The closed-form donor posterior (`closed_form_b32`, index convention of API.md §4).
- The v4 comparison rules:
  - t + t² with r_E and ε_sym; the t ≤ 3/2 switch to the enclosure branch;
  - exact T/π invariance and its failure → FAIL_TECHNICAL/ORACLE;
  - the named/canonical 4·10⁻¹² rule and its off-fast-path interval rule;
  - the §3.4 interval rule at its boundaries: D_high = a passes; D_low just above a fails; the case in between is INCONCLUSIVE/NUMERICAL;
  - zero operational posterior entries do not fail P4.
- The synthetic enclosure-branch fixture of §3.2 (corrupted float closed form → FAIL_TECHNICAL/ORACLE).
- Named/canonical joins and the cross-model G identity (the permuted canonical arrays).

**A-4 Eligibility, κ_ν (§4).**
- s_max at an inverted_cdf boundary.
- The eligibility rule (both donors ≤ s_max, finite evidence).
- The H4 fractions.
- κ_ν with population covariance, and the 0.01 trigger.

**A-5 Support (§9).**
- D_M with the source's or the donor's own z̃.
- q99 by inverted_cdf.
- The four M3 requirements at their boundaries.

**A-6 The gate table and stage machinery (§16; protocol §17 Author B items reassigned).**
- Gate order and the computation-order rule:
  - no logit is read on calibration except M0;
  - donor logits are first retained at V3, and primary and control logits at P1;
  - fresh primary/control A, Y and Z are never evaluated before T-PRE passes, so never when row 20 fails;
  - A_full and Z_full are evaluated inside T-PRE.
- The `stage_records` PREREQUISITE rebinding and the C1 PASS-gate-set checks: `begin_stage` refuses a missing PASS, a recorded non-PASS, a retry, and changed evidence.
- The exception mapping of §16 conventions: one fixture per exception class and per exceptional `StageFailure` code, including `PH_RESOURCE_LIMIT` and `GATE_FAILED`.
- The release schema checks (`c1_release.verify` on synthetic mailboxes in tmp_path).
- The meter-binding rebindings (WORKER_SESSION, caps, OUTPUT_CAP, MEMORY_CAP, the disk safe-STOP helper), checked in memory without launching a meter.

## Author B: the endpoint, inference and precision, controls and Haar frames, certificate, registry and freshness

**B-1 The A identities (§1.2, §12.1; v4 review fix 4), on normalised and non-stochastic (δ_m ≠ 0) fixtures, in exact rationals where stated.**
- A = G − ½δ_m·log(m₊/m₋) at p = q/m, and A = G when m₊ = m₋.
- A symbol-constant arm difference contributes ½kδ_m.
- Arm-common additive log-p perturbations cancel exactly.
- A_β = βA − ½δ_m(log Z_β⁺ − log Z_β⁻).
- A = 0 for equal arms. The zero patch gives A = 0 bitwise.
- The logit-difference form equals the log-softmax form when Σd = 0.

**B-2 Inference (§12, §13, §3.5, §11).**
- The ratio-to-mean reduction θ > c ⇔ E[Y − cG] > 0.
- The decision boundaries: equality gives INC.
- The bootstrap index order, shared across models: one `rng.integers(0, n, size=n)` per draw.
- tree_mean against exact rationals, with cancellation and subnormal inputs.
- The H5 wrapper's index stream equals `bootstrap_profile`'s. On integer-valued fixtures their means are bitwise equal.
- Ranks 250, 84 and 4917; the rank check rejects a wrong value; inverted_cdf returns an input element.
- The ladder logic, including the k formula and the fresh-fraction rule.
- `precision.py` called as specified.

**B-3 Controls and Haar frames (§5–§8, §10; protocol §17 Author B).**
- FWL recovers a known B in a noiseless synthetic case. A trap fixture shows that sequential residualisation is wrong.
- F1 degeneracy.
- Haar and primary-QR sign conventions (positive diagonal).
- Isometry and isospectral identities, with the §6 zero-norm and zero-spectrum rules. The same frame maps both arms.
- D_w, D_y and leakage; M2 at its boundaries, including the dispersion rule (≥ 28/32).
- V1/V2: wrap at ±π, sign(0), and median ties.
- M4 boundaries.
- RidgeProbe/`nested_ridge` equivalence.

**B-4 Numerical certificate (§15.3.16 items 1–14; CERTIFICATE.md).**
1. Theorem 1 on tiny positive HMMs (N 4–12, sparse and dense support, L ≤ 33), against an exact Fraction filter. ρ̄_ref(32, 144, 5) = 729·u′ and ρ̄_ref(32, 144, 144) = 9486·u′.
2. Theorem 1′ with injected perturbations. r_h > 1/2 → FAIL_TECHNICAL/ORACLE.
3. Underflow and route F: emissions near 10⁻³⁰⁰ fail P1; ρ_F bounds the exact error; x > 1/2 → FAIL_TECHNICAL/ORACLE.
4. Theorems 2 and 3 against exact rationals, with q entries of 10⁻²⁵⁰ and non-stochastic rows (ω_TE required and sufficient).
5. The logit form (also B-1).
6. M-ln: an injected log error enlarges b^G; Decimal traps and flags → FAIL_TECHNICAL/NUMERICAL.
7. L4, quantiles and ranks (also B-2).
8. Theorem 5 and the H5 wrapper (also B-2).
9. L5:
   - OUT(evaluated) ≥ the exact value on random nonnegative expressions within the premises, subnormal leaves included;
   - the node, monomial and degree counts of the implemented b^G, b^A, b^Y, b^Z and b^Zf, recomputed with `c1_bounds.Sym`, do not exceed the table.
10. Guards at their boundaries: Γ = ±g exactly, the floor binding, and exact rational comparisons for (E), (H) and (V).
11. Constants: δ₁ and δ₃ are exact, and up(c) ≥ c.
12. P0, P2 and the A1 self-test: non-identical E_canon, or non-finite or out-of-range values, → the declared FAIL_TECHNICAL statuses.
13. Kernels: no certified kernel calls BLAS or a numpy reduction. This is checked by source inspection through `inspect.getsource` of the named API functions only, which is allowed at run time; the author still never reads the source. Skipping zero T entries is bitwise neutral.
14. Coverage and order: every eligible row, model and pair has its bounds. The sealed validation bounds are not opened.

**B-5 Registry and freshness (§2.2–§2.4).**
- Sequence-id and panel rules.
- The lowest-n selection.
- History-table digests for H, H⁺ and H⁻.
- Separation over every role combination (collision → FAIL_TECHNICAL/LINEAGE).
- The registry manifest binds content hashes; an unreadable source → INCONCLUSIVE/REGISTRY_INCOMPLETE.
- `first_token_ok`.
