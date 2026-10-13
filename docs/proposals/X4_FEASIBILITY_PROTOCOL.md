# X4 Phase B — frozen feasibility protocol (x4b-v1)

13 October 2026. Branch `x4-phase-b`, based on `f8afc2a5e43309aa4bf2d402f2be4e38470df180`. **Frozen before any Phase B quantity was computed.** Only the input artifacts' metadata and lineage were inspected while it was written: IDs, parents, producer commits, shapes and dtypes. No rank, spectrum, belief, distance or neighbour has been calculated. Governing documents: [X4_NEXT_EXPERIMENT.md](X4_NEXT_EXPERIMENT.md) (Phase B only), [X4_CAUSAL.md](X4_CAUSAL.md), [RESEARCH_HARNESS_ARCHITECTURE.md](RESEARCH_HARNESS_ARCHITECTURE.md) (M1–M3/M7), [REVISION_AFTER_E4.md](REVISION_AFTER_E4.md), [RESEARCH_ROADMAP.md](RESEARCH_ROADMAP.md).

The owner approved the screening thresholds for this task only. They are not universal constants and are not additions to the J rule, 0.01 nat or 250 steps. Nothing below is changed after results. Any deviation would be reported as a deviation, never silently applied.

## 1. Question and scope

Does the joint two-symbol future Q2 contain meaningful distinctions that Q1 does not, among beliefs that the process actually produces? Three questions are answered separately:

1. **Ambient algebra:** can Q2 distinguish beliefs on the full belief simplex that Q1 does not?
2. **Practical reachable gap:** do near-equal Q1 / distinct Q2 pairs occur among beliefs from existing histories?
3. **Strict sufficiency:** is Q1 provably insufficient on the reachable set?

Near-equality of Q1 is not equality and is never relabelled as such.

The old test pool is already unblinded, so this is an exploratory feasibility check, not a confirmatory experiment. Dev pools are repeated evidence for the same process, not independent worlds. Nearest-neighbour pairs are dependent: no pair-count p-value is computed, and pairs are never treated as units.

## 2. Frozen inputs (cylinder O, 12×12, σ = 1.25, original T/E)

| Role | ID(s) | Notes |
|---|---|---|
| WorldSpec (cylinder) | 21feee1d8ee5422e | parent of T and every E |
| TransitionSpec T, π | e4dafc7b9785c172 | shared by all three runs; π is the initial law used by the filter |
| EmissionSpec 1729 / 2718 / 3141 | 3633ac27dab50cf4 / 97838b9e13a26f74 / 8c29c329c197c79e | mode overlap, σ 1.25; replicate-specific `symbol_perm` |
| test ObservationSet | 2a67b2c947e293ba / 95c4d118517ecd92 / 2e2cf22bb4820155 | shared test trajectories up to relabelling (D-019) |
| test HistoryIndex | afb6e7120c9477b1 / 908cb61ffbd956c6 / 7e7d27bd143ebeb5 | 4096 rows, end 32 |
| OracleOutputs (b32, q, F2 float32) | efebc05165d4f7bc / d9c6defcc7a9d803 / 1731629d61077e96 | stored test targets |
| ProcessDiagnostics | 2cd84acf8e3897b2 / c904849c3b3ba6d7 / 07a9775b7c0eae63 | stored observability spectra |
| dev ObservationSet | 096f9b6dbe8536cd / d6d3eeb32dfa40ac / 6da65c49fac77b30 | one dev pool per replicate |
| dev HistoryIndex | d9fe461a56797514 / 880c3e8ec8347b72 / d5e64c5398ef4c25 | 4096 rows, end 32 |
| S7 lineage | dev extraction 13be28a051ce15b1, probes 63ebd7ec1ba5f38a, sensitivity baff2c7a1e5294c9, circular a7a60592e32b26fb | dev indexes and dev ObservationSets are ancestors of these records (verified) |

The inputs are resolved through the existing `find_run_inputs` resolver and checked against this table; a mismatch, a missing parent or a second candidate stops the run (`MISSING_PARENT`). Nothing is taken as "latest". No checkpoint, ActivationSet or EvalSidecar is loaded. No RunManifest payload exists in the store, so provenance uses artifact metadata (parents, producer version, payload checksum).

## 3. Future maps (M2, float64)

* Canonical emission: `E_canon = E_run[:, symbol_perm_run]`; the three canonical matrices must agree exactly (max |diff| = 0), else stop.
* `G1 = T E` (144×36). `Q1(b) = b G1`.
* `Q2(b)[i, j] = b T diag(E[:, i]) T E[:, j]`, flattened lexicographically at `i·36 + j`; `G2` is 144×1296. Q2 is the joint law, not `b T² E`.
* Route A: `FutureOperator(T, E).observability_matrices(2)` returns `[O1, O2]`; `O1 = G1ᵀ` (36×144), `O2` is 1332×144 with the horizon-one rows first; `G2 = O2[36:]ᵀ`. Route B: `FutureOperator.F2` evaluated on the 144 identity beliefs. Horizon 3 is not built.
* Checks (all in float64; failure stops the run):
  - Route A equals route B: max |diff| ≤ 1e-12.
  - `O1 = G1ᵀ` exactly and `O2[:36] = O1`.
  - Explicit lexicographic formula per first symbol i equals `G2[:, i·36:(i+1)·36]`: max |diff| ≤ 1e-12.
  - Rows of G1 and G2 sum to 1 within 1e-10; min entry ≥ −1e-14.
  - Marginalization: Σ_j Q2 = G1 within 1e-12. The second-symbol marginal Σ_i Q2 equals `T² E` within 1e-12; it is reported to show it differs from G1.
  - Stored ProcessDiagnostics spectra for k = 1, 2 equal the recomputed singular values of O1, O2 within a relative 1e-10.
* The same checks run on each replicate's own `E_run`. Results are reported for the canonical vocabulary, and permutation invariance is checked against the runs.

## 4. Ambient algebra (M3)

* `B`: the 144×143 Helmert basis of the sum-zero tangent, defined analytically. Report max |BᵀB − I| and max |1ᵀB|.
* `H = BᵀG1` (143×36); full SVD `H = U S Vᵀ` with U 143×143, so the null directions are included.
* For each relative tolerance τ ∈ {1e-8, 1e-10, 1e-12}:
  - `r_τ` = number of singular values of H with `s_i > τ·s_1`;
  - `U0_τ = U[:, r_τ:]` spans the numerical ker(Hᵀ) (the left null space, row-vector convention `v G1 = 0`);
  - `D_τ = U0_τᵀ BᵀG2`.
  - Report: the spectra of H and BᵀG2; `r_τ` and `dim U0_τ`; ‖U0_τᵀH‖₂; the singular values of `D_τ`; `ρ_τ = σ_max(D_τ)/σ_max(BᵀG2)`; numerical rank of BᵀG2 at τ; conditioning `s_1/s_{r_τ}`; and the spectral gap `s_{r_τ}/s_{r_τ+1}`, where it exists.
  - Amplification `A_τ = ‖H⁺_τ BᵀG2‖₂`, using the τ-truncated pseudo-inverse.
* **Dimension certificate (analytic):** `G1 1 = 1` implies `BᵀG1 1 = 0`, so rank(H) ≤ 35 exactly and dim ker ≥ 108. Factorization of Q2 through Q1 on the simplex would force rank(BᵀG2) ≤ rank(H) ≤ 35. The certificate holds if `σ_36(BᵀG2)/σ_1(BᵀG2) ≥ 1e-6`. That margin exceeds float64 rounding of a matrix of this size by many orders (Weyl). If the certificate holds, the exact ambient distinction is proven independently of τ.
* **Verdict (i):**
  - `ALLOWS_STABLE` if `ρ_τ ≥ 1e-6` at all three τ.
  - `FACTORIZES` if `ρ_τ ≤ 1e-10` at all three τ. That is "practically conditioned" if additionally `A_τ ≤ 1e3` at all τ, and "ill-conditioned" otherwise.
  - Anything else is `TOLERANCE_DEPENDENT`.

## 5. Reachable pools and precision (M2)

* Pools: `test` (4096 shared test histories), `dev1729`, `dev2718` and `dev3141` (4096 dev histories each). History = first 32 symbols; belief after w32.
* Canonical tokens: `c = argsort(symbol_perm)[w]`. Canonical trajectory ID: `"{split}|{sequence_id}|{tokens_hash(c[:32])}"`. For the test pool the three runs must give the same IDs and canonical tokens (D-019), else stop. Each canonical ID is mapped to every run's own `history_id`. Runs are never joined on token-derived IDs alone.
* Beliefs: `BayesFilter(T, E_canon, π)` on canonical tokens gives b32 (float64). Then `Q1 = b32 G1`, `Q2 = b32 G2` (float64).
* Checks: Q1/Q2 rows sum to 1 within 1e-10; min ≥ −1e-14; Σ_j Q2 = Q1 within 1e-12.
* Precision reconciliation, test pool only (this is not a new sample):
  - The run-vocabulary filter on run tokens gives the same b32 within 1e-12.
  - Stored float64 b32 and q match the recomputation within 1e-12.
  - Stored float32 F2 vs float64 Q2 in the run vocabulary: the max |diff| is reported, and the schema tolerance 1e-4 must hold.
  - Stored targets are never rounded.
* Hellinger: `H(p, q) = ‖√p − √q‖₂ / √2`. Entries in [−1e-14, 0) are set to 0 before the square root and counted.

## 6. Reachable-history audit (frozen screening settings)

* **Anchors:** in each pool, the 512 histories with the smallest `sha256("x4b-v1|anchor|" + canonical trajectory ID)` (hex order).
* **Partners:** for each anchor, its 5 nearest neighbours by H(Q1, Q1′), taken from the same pool, with the same canonical last symbol (w32). Excluded: the anchor's own row and any history with an identical canonical 32-symbol window (a self-pair: same oracle history); the number excluded is reported. Ties break by canonical ID. If fewer than 5 candidates exist, all are used; this is reported.
* **Admissible partner:** H(Q1, Q1′) ≤ 0.01. **Eligible anchor:** at least one admissible partner. **Witness anchor:** an admissible partner with H(Q2, Q2′) ≥ 0.05.
* **Pool status:**
  - `UNDERCOVERED` if eligible < 128.
  - Otherwise `WITNESS` if witnesses/eligible ≥ 0.05, else `NO_MATERIAL_GAP`.
* **Verdict (ii):**
  - `GAP` if test is `WITNESS` and at least 2 of 3 dev pools are `WITNESS`.
  - `NO_GAP` if test and at least 2 dev pools are `NO_MATERIAL_GAP` and no pool is `WITNESS`.
  - Otherwise `INCONCLUSIVE`, with the reason: coverage or inconsistency.
* **Recorded, never a verdict:**
  - all partner distances d1/d2 and the ratio d2/d1;
  - last-symbol group sizes;
  - anchor posterior entropy and max b32;
  - partner reuse counts;
  - discarded anchors with their reason (group < 1, nearest d1 > 0.01);
  - the invariant d2 ≥ d1 (Hellinger is monotone under marginalization), with violations > 1e-12 reported.
* **Secondary, descriptive:** the same audit without the last-symbol restriction.
* **Agreement checks:**
  - The test-pool audit is repeated in each replicate's own vocabulary from the stored b32. Anchors, partners and flags must be identical (permutation invariance).
  - The test-pool d2 is recomputed from the stored float32 F2 for the same pairs. Anchor flag flips and status changes are reported. A pool-status change is a precision instability.

## 7. Strict sufficiency, overall decision and stop

* **Verdict (iii):**
  - `SUFFICIENT_AMBIENT` only if (i) is `FACTORIZES`.
  - `INSUFFICIENT_PROVEN` only for an analytically exact reachable witness. None is attempted: floating-point equality is not proof.
  - Otherwise `UNRESOLVED`. Pairs with numerically equal Q1 (max |ΔQ1| ≤ 1e-15) among the partner pairs are counted descriptively.
* **Overall (iv):**
  - `INCONCLUSIVE` if any check in §2, §3 or §5 fails, if the budget is exceeded, or if the permutation or precision agreement fails.
  - Otherwise `NO-GO` if (i) is `FACTORIZES` (practically conditioned), or if (ii) is `NO_GAP`.
  - `GO` if (i) is `ALLOWS_STABLE` and (ii) is `GAP`. Subtype: practical near-Q1 / distinct-Q2 accessibility, not strict insufficiency.
  - Otherwise `INCONCLUSIVE`, with the specific limitation.
* GO justifies proposing Phase C only; it authorizes nothing. NO-GO stops the horizon-gap branch for this process, horizon and resolution, scoped to the sample. **After Phase B: STOP and review with the owner.**

## 8. Validation before the real run (known-answer fixtures)

1. Constant emissions: no gap, and (i) = `FACTORIZES`.
2. Four-state path (neighbour probability .4; A at states 0/1/2, B at 3): Q1(δ0) = Q1(δ1) = A, Q2(δ0)[AA] = 1, Q2(δ1)[AB] = .16; (i) = `ALLOWS_STABLE`. This shows ambient possibility only.
3. Constructed `G2 = G1 L`: detected as `FACTORIZES`.
4. Symbol permutations leave spectra, distances, anchors, partners and gates unchanged.
5. Joint order and marginalization: a fixture that fails for `b T² E` or for transposed (j, i) order.
6. float32/float64 reconciliation flags an exceedance above 1e-4.
7. Gate logic: coverage, witness fraction, 2-of-3 rule, self/duplicate exclusion and deterministic anchors.

## 9. Budget, outputs and prohibitions

* Scientific run: at most 1 CPU hour (process time) and an 8 GB RAM target, both measured and reported. If the cap is reached: stop and record `INCONCLUSIVE`, with no automatic extension.
* Outputs:
  - an independent store at `topo-pilot/x4b-research-store/` (outside git) holding one MetricRecords and checksummed npz arrays; its read-through backend never writes to the main store;
  - committed tables in `docs/proposals/X4_FEASIBILITY_OUTPUTS/` with IDs, parents, checksums and precision details;
  - the report at `docs/proposals/X4_FEASIBILITY_REPORT.md`.
* The main store's file listing (path, size, mtime) is hashed before and after the run and must be unchanged.
* Prohibited:
  - no fitting of any kind;
  - no new histories, extraction, intervention or training;
  - no Phase C/D, X5 or X6;
  - no edits to reports, preregistrations, historical artifacts, frozen contracts or G-H;
  - no merge, push or tag change.
