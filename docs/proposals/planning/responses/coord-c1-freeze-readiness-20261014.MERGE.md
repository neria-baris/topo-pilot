# C1 merge: coordinator decisions and lessons (round 1)

**Coordinator:** Claude c351b245. **Date:** 2026-10-15, ~00:00 local (21:50Z).
**Inputs (sha256):**

| Input | File | sha256 |
|---|---|---|
| Request | requests/coord-c1-freeze-readiness-20261014.md | 8761AAF0… |
| Track X (Codex gpt-6.1-sol, high, read-only) | .codex.md | 28121896…A016 |
| Track L (Claude, clean context) | .claude.md | A30E2A38…087B |
| Comparison (clean-context analyst) | .MERGE_ANALYSIS.md | — |

## Decision

Adopt **MERGE_ANALYSIS §6 items 1–22 as the merged C1 design**, with the explicit rulings below.

The merged protocol document is `C1-MERGED-v1`, written from these decisions. It requires the result-blind independent review (Codex first, per the owner's message, part D) before any freeze.

**Rulings on open points:**
1. **Random-control family (L-2, owner B3-C).** Use Haar whitened 2-frames applied to the primary's whitened displacement coordinates, with the same frame for both ± arms. Norm and spectrum match exactly, and damage is gated on calibration before any logits are computed. **This satisfies B3-C.** The control's near-zero expected effect is the null being tested against. It is not a defect. The claim text must say that the comparison is specificity relative to equal-norm, equal-spectrum displacements in random within-class directions.
2. **Decision asymmetry.** PASS requires all three models to have a lower bound > 0. FAIL requires all three to have an upper bound < 0. Anything else is MIXED. **Kept** (conservative; per-model statuses are reported).
3. **Thresholds.** These planning values are adopted as they stand and must not be tuned after any data:
   - margin c = 0.10, planning alternative 0.20;
   - positive control 0.30;
   - α = 0.05/3 per tail, power 0.80;
   - eligibility at calibration q0.999 of natural surprisal, with coverage ≥ 0.90.

   The reviewer may challenge them. Any change must happen before any C1 data exists.
4. **Normalisation.** Use θ = E[Y]/E[G], with G = ½·Jeffreys(q⁺, q⁻), so an oracle-perfect readout gives θ = 1. Correct L's wording: only arm-common **additive** effects cancel exactly.
5. **Numerics.** float64 forward passes of the frozen weights through `return_hooks`. Do not use `ActivationExtractor`, which works in float32 and needs stored observation sets.
6. **Freshness.** Use an exposure registry covering sources **and** donors (from X). Fresh test histories are sampled only after validation acceptance.
7. **Chart.**
   - If K4 (queue A) produces an accepted chart, reuse it and bind its NPZ sha.
   - If K4's chart gate FAILS or is INCONCLUSIVE, C1 **stops** at the chart gate. There is no refit of a method that already failed.
   - If K4 never reaches the chart stage, construct the chart once, with identical frozen code.

   **So C1 implementation can be planned now, but C1 data stages wait for K4's chart outcome.**
8. **CPU.** Expected 2–6 CPU-h. This is a forecast, not a cap (owner override).

## D decision (queue item D)

Pursue **L's D-1 first**: cylinder versus Möbius, with a seam band where emissions reveal x exactly and nothing about y. It needs three fixes:
- emission rows identical outside the band in both worlds;
- one process with a hidden world bit;
- the result scoped to a reachable decision phase (X's sufficiency lemma).

Keep X's D2 in reserve, for the case where the owner means a continuous circular family. The next step is a dual-track planning round, `coord-d1-oracle-proof-*`, documents only.

**Prerequisite found by the analyst:** the current emission code (`process/_geometry.py::point_distances`) handles only x-periodic gluing. For a Möbius world it would use unwrapped x-distances. D-1's oracle check therefore needs either the emission rows supplied directly (identical by construction) or a reviewed generalisation. The coordinator already flagged the same gap independently (2026-10-14).

## Lessons from round 1

1. **Both tracks self-labelled FREEZE_READY, and both had real defects.** A self-assessment is not a review. The third, result-blind review is necessary.
2. **Codex (X) was strongest on binding discipline:** exposure registries, ID and seed scopes, licence wording, CPU and thread bindings, and a clean sufficiency lemma for D.
3. **Codex's weakness was the statistical construction.** Its sign-field controls collapse onto the primary. Its absolute-phase binning aliases against symbol centres at 15°+60°a. Its refit-recoverability damage metric is nearly blind for additive shifts. Its every-row gates make INCONCLUSIVE nearly certain whatever the science.
4. **Claude (L) was strongest on identification:** crossed ± donors that anchor θ = 1, an FWL within-symbol tangent, and a positive control that makes FAIL interpretable.
5. **Claude's weakness was overclaims and code-reuse mismatches:** the float32 extractor, the quantile convention, a test ladder counted on sampled rather than eligible rows, and no donor freshness check.
6. **Process rule going forward:**
   - ask both tracks explicitly for a positive control, an attainability check for every gate (fraction rather than every-row), and a code-reuse verification against the actual function signatures;
   - use the analyst comparison, then a decision record, then the merged document, then an independent review by the other model family.

## Erratum and addendum (2026-10-15 ~22:40Z, after Codex review coord-c1-merged-review-20261015)
- **Ruling 4 and lesson 4 are corrected.** If the primary arms reproduce q±, then A_T = G pointwise, so the primary anchor is θ_T = E[A_T]/E[G] = 1. The control-adjusted θ = 1 − E[Ā_C]/E[G] equals 1 only when E[Ā_C] = 0. An oracle-perfect full-donor readout gives θ_full = 1. These ratios are discrimination indices, not proportions in [0,1]. "Anchor θ = 1" in lesson 4 should read "anchor θ_T = 1".
- **Coordinator decisions on the v2 editor flags:**
  - (a) Adapted `StageFailure`, `ProfileError` and reference-input/Decimal exceptions record **FAIL_TECHNICAL**. This matches the K4 taxonomy: integrity, implementation and numerical defects are FAIL_TECHNICAL; scientific criteria not met are INCONCLUSIVE.
  - (b) The degeneracy failure for change 5 is **accepted as the editor specified**: rank-deficient W·B goes to F1 (INCONCLUSIVE / PATCH_MODEL_DEGENERATE); a zero QR diagonal goes to M1 (FAIL_TECHNICAL). The reviewer confirms this at verification.
  - (c) The source-label rename to (a)–(d) is accepted.
  - (d) The C1 loader maps JSON null to +inf before `cochain.integer_lift`. The 600 s native-operation wall is a C1-contract value.
- **Remaining blocker:** the review's change 6, the numerical certificate (§15.3). It goes to planning round `coord-c1-numcert-20261015`, dual-track.

## Erratum 2 (~23:55Z, after Codex v3 verification, fix 4)
Every exact identity above holds when the two oracle predictives have equal mass. For the literal stored-weight target, m± = Σ_v q*±(v) and δ_m = m₊ − m₋, with |δ_m| ≤ ω_TE.
- A symbol-constant arm difference k contributes ½kδ_m.
- An oracle-perfect probability readout gives A_oracle = G* − ½δ_m·log(m₊/m₋), so the exact unit anchor θ_T = 1 holds only when m₊ = m₋.
- Arm-common additive log-probability perturbations still cancel exactly.

C1-MERGED-v4 §1.2–§1.3 carries the normative text.

## Coordinator rulings on the v4 open items
- **V4-F3:** the "normal fast path" is P1 applied to the evaluated posteriors. Accepted. Inexact ρ_k-invariance of T or π is FAIL_TECHNICAL/ORACLE.
- **V4-F4:** the editor's rules for the two unspecified branches are accepted provisionally, subject to the reviewer's confirmation in the v4 pass. Both branches are expected to be empty.
- **V4-F8:** these become hard result-blind preflight requirements: bitwise E_canon identity across the three models, and exact T/π invariance. They are checked from stored process arrays before any C1 data stage.
- **Ruling 7:** the A1 self-test vectors are fixed in API.md at implementation freeze.
