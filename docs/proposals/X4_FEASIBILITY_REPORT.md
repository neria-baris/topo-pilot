# X4 Phase B — feasibility audit report

13 October 2026. Protocol [x4b-v1](X4_FEASIBILITY_PROTOCOL.md), frozen before computation (D-051, commit fbd12bf). Branch `x4-phase-b` from `f8afc2a`. Code: commit 5b2f384. Outputs: [X4_FEASIBILITY_OUTPUTS/](X4_FEASIBILITY_OUTPUTS/), plus an independent store at `topo-pilot/x4b-research-store/` (MetricRecords `be4fbf6252097544`, four npz exports; checksums in `run.json`). Exploratory feasibility only: the test pool was already unblinded. **Stopped after Phase B.**

## Verdict

| Question | Verdict | Basis |
|---|---|---|
| (i) Ambient algebra | **ALLOWS_STABLE** — Q2 distinguishes beliefs that Q1 does not | Identical at all three tolerances. Rank certificate holds analytically. |
| (ii) Practical reachable gap | **INCONCLUSIVE** — insufficient near-neighbour coverage | All four pools UNDERCOVERED: 49–66 eligible anchors, below the frozen 128 |
| (iii) Strict sufficiency of Q1 on the reachable set | **UNRESOLVED** | No exact reachable witness. Numerical near-equality is not evidence of one. |
| (iv) Overall | **INCONCLUSIVE** | Practical screen inconclusive. Every validity, precision and permutation check passed. |

Under X4_NEXT_EXPERIMENT this outcome means: stop and report the limitation. Do not propose Phase C. Do not enlarge the pool or fit decoders automatically.

## What was computed

### Inputs and validity

All 27 input artifacts were resolved through the existing resolver and matched the frozen table (`inputs.json`: IDs, parents, producer commits, checksums). The three dev pools are ancestors of the S7 dev-extraction, probe and sensitivity records. No checkpoint, ActivationSet or EvalSidecar was loaded.

The three replicates' canonical emission matrices `E[:, symbol_perm]` are identical (max |diff| 0). π is stationary to 9e-19.

### Future maps (float64)

The two maps were built by three routes: `observability_matrices(2)`, `F2` on the identity beliefs, and the explicit formula.

| Check | Result |
|---|---|
| Route A vs route B | equal (0) |
| Explicit lexicographic formula | differs by ≤ 3e-17 |
| O1 = G1ᵀ and O2[:36] = O1 | exactly |
| Row sums of G1/G2 | within 4e-16 |
| Σ_j Q2 = G1 | ≤ 2e-16 |
| Σ_i Q2 = T²E | ≤ 2e-16 (differs from G1 by 0.056, so the joint is not the second-step marginal) |
| Stored ProcessDiagnostics spectra (k = 1, 2) | reproduced exactly |
| Each replicate's maps | equal the canonical ones under its symbol permutation (0) |

### Ambient algebra (`ambient.json`)

Helmert basis residuals: max |BᵀB − I| = 4e-16; max |1ᵀB| = 3e-15.

| τ | rank BᵀG1 | dim ker | ‖U0ᵀH‖₂ | rank BᵀG2 | ρ = σmax(D)/σmax(BᵀG2) | cond (s1/s35) | gap s35/s36 | amplification |
|---|---|---|---|---|---|---|---|---|
| 1e-8 | 35 | 108 | 5.6e-16 | 137 | 0.176 | 57.0 | 1.1e14 | 1.05 |
| 1e-10 | 35 | 108 | 5.6e-16 | 137 | 0.176 | 57.0 | 1.1e14 | 1.05 |
| 1e-12 | 35 | 108 | 5.6e-16 | 137 | 0.176 | 57.0 | 1.1e14 | 1.05 |

* **Rank of BᵀG1 is exactly 35:**
  - s35/s1 = 1.8e-2 and s36/s1 = 1.6e-16;
  - this is also the analytic upper bound, because the rows of G1 sum to 1.
* **D has 102 singular values above 1e-6 of σmax(BᵀG2).** So G2 acts with rank about 102 on the 108-dimensional tangent kernel of G1.
* **Certificate:** σ36(BᵀG2)/σ1 = 0.127 ≥ 1e-6. Therefore rank(BᵀG2) > 35 ≥ rank(BᵀG1), and Q2 cannot factor through Q1 on the full simplex. This holds independently of τ.
* **Descriptive:** six tangent directions (143 − 137) are invisible to both horizons.
* **Permutation invariance:** every replicate vocabulary gives the same verdict and spectra.

### Reachable audit (`pools.json`, `anchors_*.csv`)

Setup: 512 anchors per pool, selected by sha256 of canonical trajectory IDs; 5 same-last-symbol nearest Q1 neighbours each (2,560 anchor–partner slots per pool). The last-symbol groups held 88–147 candidates. No anchor had fewer than 5 candidates, and no identical-history duplicates occurred.

| Pool | eligible anchors (d1 ≤ 0.01) | witnesses (d2 ≥ 0.05) | status | max d2 over admissible pairs | median nearest d1 | anchors with nearest d1 ≤ 0.02 |
|---|---|---|---|---|---|---|
| test | 66 | 0 | UNDERCOVERED | 0.0133 | 0.028 | 168 |
| dev1729 | 54 | 0 | UNDERCOVERED | 0.0122 | 0.030 | 169 |
| dev2718 | 49 | 0 | UNDERCOVERED | 0.0123 | 0.029 | 156 |
| dev3141 | 62 | 0 | UNDERCOVERED | 0.0137 | 0.029 | 163 |

These rows are descriptive and carry no verdict:

* **d2/d1 ratio across all 10,240 primary slots:** between 1.15 and 1.48. The median is about 1.17 in every pool. A witness would need a ratio ≥ 5 near d1 ≈ 0.01.
* **Largest d2 among pairs with d1 ≤ 0.02:** 0.025 in every pool.
* **Hellinger monotonicity:** d2 ≥ d1 held in every pair, with 0 violations.
* **Exact Q1 ties:** none (0 pairs with max |ΔQ1| ≤ 1e-15).
* **Partner reuse:** at most 2.
* **Posterior shape:** anchor entropy was 1.75–2.7 nats and max b32 was 0.16–0.39. Eligible and non-eligible anchors overlap in both.
* **Unrestricted neighbours (secondary):** 84–96 eligible per pool, 0 witnesses, max admissible d2 = 0.0142, ratio ≤ 1.71.

### Precision and permutation agreement (`test_agreement.json`)

For each replicate, the run-vocabulary filter on the run's own tokens, the stored float64 b32 and the stored q all equal the canonical recomputation exactly (0).

The stored float32 F2 differs from the float64 joint by at most 7.4e-9: 6e-8 relative, well inside the schema tolerance of 1e-4. Recomputing d2 from float32 changes distances by ≤ 6.4e-9, flips no anchor and leaves every pool status unchanged.

The audit repeated in each replicate's vocabulary selects identical partners and flags; distances differ by ≤ 1.1e-16. Pool checks: Q1/Q2 rows sum to 1 within 8e-16; Σ_j Q2 = Q1 within 3.4e-16; all entries are nonnegative.

### Tests and cost

* **Validation fixtures (§8), all passing:**
  - `tests/analysis/test_horizon.py`: 17 tests (constant emissions, four-state path, constructed factorization, permutation, joint order against bT²E and transposed order, float and gate logic);
  - `tests/experiment/test_x4b.py`: 7 tests;
  - analysis + experiment suites: 221 passed;
  - ruff, import and file-size checks clean.
* **Scientific run:** 19.7 CPU-s and 14.9 s wall, against a cap of 3,600 CPU-s.
* **Main store:** its file-listing hash (2,568 files) was identical before and after the run.
* **Peak memory:** not captured by the first run. The Windows query truncated the 64-bit process handle and recorded 0; fixed in 741333c. A measurement-only rerun from that commit reproduced every table byte for byte, with the same MetricRecords ID. It measured 17.3 CPU-s and a **1.51 GB** peak working set, against the 8 GB target. Its outputs stayed in a scratch directory.
* **Output size:** about 26 MB in the external store; about 1.1 MB of committed tables.

## Deviations and implementation notes

1. **Zero-map guard** (added before the real run, after a validation fixture failed). With constant emissions, BᵀG1 and BᵀG2 are exactly zero. A relative rank tolerance then ranks rounding noise, and the fixture came out "ALLOWS". `tangent_audit` therefore treats a tangent map whose largest singular value is ≤ 1e-12 × its ambient norm as exactly zero. This is not in the frozen protocol text. It cannot act on this process: s1(BᵀG1) = 1.86 and σ1(BᵀG2) is of the same order.
2. **Peak-memory instrumentation bug** (note above). The run's verdict outputs are unaffected; this is shown by the byte-identical rerun.
3. **Commit message:** fbd12bf says "progress: running", but the PROGRESS file was committed separately in e5bfe90.
4. **Producer versions:** 21 of the 27 input artifacts were written from dirty working trees (`+dirty`) when they were produced. This is historical, pre-existing provenance; it is recorded, not altered.
5. **Pool sizes:** the dev pools are each replicate's full dev split (4,096 histories); the test pool is the shared test split (4,096). No new history, extraction, fit, checkpoint load or stage-config change occurred.

## What this licenses — and what it does not

**Can be stated:**

* On the full belief simplex, the joint two-symbol future strictly refines the next-symbol law. A 108-dimensional tangent kernel of Q1 is about 102-dimensionally visible to Q2. This is exact and tolerance-independent (the rank certificate).
* In the beliefs these four existing pools actually produce, sampled near-Q1 pairs show Q2 distances only about 1.15–1.5 times their Q1 distances. No admissible pair approaches the 0.05 witness distance.

**Cannot be stated:**

* That the practical gap is absent. Coverage failed the frozen rule in every pool, and the descriptive pattern is not a NO-GO.
* That Q1 is sufficient or insufficient for Q2 on the reachable set.
* Anything about model representations, decoding, causality or topology. No model was loaded.
* Generality beyond cylinder O, 12×12, σ 1.25, horizon 2 and p32.

The pools are repeated samples of one process. Pairs are dependent and were not tested.

**Evidence that would change the decision:**

* Pools dense enough to give ≥ 128 eligible anchors under the unchanged thresholds:
  - a witness fraction ≥ 5% in test and in 2 of 3 dev pools would give GO;
  - no material gap in adequately covered pools would give NO-GO.
* Alternatively, an analytic exact reachable witness, which would resolve (iii).

Either route needs owner approval. Fresh histories, even oracle-only ones, are outside this task.

## Recommendation (one)

Do not propose Phase C. If the owner wants the horizon-gap question resolved rather than left inconclusive, the one next step is a separately approved, oracle-only coverage extension of Phase B. It would use larger fresh pools from the same frozen process, with no model, no fitting, and every x4b-v1 threshold and rule unchanged. Its pool size and lineage would be frozen before sampling. Otherwise, close this branch as INCONCLUSIVE.

**STOP: review with the owner before any Phase C.**
