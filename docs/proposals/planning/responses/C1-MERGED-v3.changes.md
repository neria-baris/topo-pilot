# C1-MERGED-v3: certificate-merge change record

- **Input:** `C1-MERGED-v2.md`, sha256 F9F679DC0DFF74D7765B7A3E2AB0B5CB98ADE6DC73707EE367D0BC01257E12F6 (unchanged).
- **Decisions:** `coord-c1-numcert-20261015.MERGE.md` (decisions 1–9), sha256 6215A4B9FB30E4B95AD1551CBBF3F4E26BDDD530A5A6C2447DACA1C1E3723DCA.
- **Tracks:** X `coord-c1-numcert-20261015.codex.md` (6D330509…7714); L `coord-c1-numcert-20261015.claude.md` (AF2CA4CF…E313). Both match `.tracks.sha256`.
- **Output:** `C1-MERGED-v3.md`, sha256 A163929CBC31CA3D0966E5ACD5EEE8C6E8846B7711E07D29E933EFCD58A132EA. First line `STATUS: CERTIFICATE_MERGED (not frozen)`. Full record in its §23.
- **Code checked:** `topo-pilot` main @4f219d6 and the pinned numpy 2.2.6, read-only. Nothing was run.

## Sections changed

| Section | Change | Source |
|---|---|---|
| Header | Status, identity, sources, code facts; freeze now needs the §15.3 review and the §23.6 items | — |
| §3.3 | Single canonical Ĝ (decision 4). One canonical oracle, which requires bitwise-identical E_canon across models (checked at H1). Named-order G is computed from permuted canonical arrays, which proves the 1e-12 cross-model check safe | L + X (sharing rule) + editor |
| §3.4 | H3 Decimal tolerances aligned: componentwise 2·10⁻¹², G ≤ b^G_i + 10⁻³⁰ (decision 5) | L |
| §3.5 | H5 keeps `bootstrap_profile`'s index semantics through a C1 wrapper using the tree-mean kernel; guard reference | X |
| §11 | A_full in logit-difference form; tree means; rank 84; guard reference | L + X |
| §12.1 | Target restated as the exact log-softmax of recorded logits; computation note (logit-difference form) | L |
| §12.3 | Tree-mean kernel; ranks 84 and 4917; run-time rank check | X |
| §13 step 2 | Certified guard, F_j = max(B_num,j, 10⁻⁹), Theorem 6 equivalence, FAIL_TECHNICAL defects | L + X |
| §15.2 | Route F replaces "no all-row Decimal"; ordered reference named | L + X |
| **§15.3** | **Replaced: merged certificate with complete proofs** (C0 ordered reference, Theorem 1 projective bound with sparse d, Theorem 1′ measured discrepancy, route F, M-ln, Theorems 2–6, L1–L6, U, OUT, signed guards, magnitudes, cost, placement, 14 tests) | X + L, decisions 1–9 |
| §16 | Convention bullet; rows 1 (P0, E_canon identity, A1 self-test), 3 (aligned), **4a N0 (new)**, 5, 18, 19 (operational note), 20, 21 | L + X |
| §17 | S0 path, S1 Author A item, S3/S5/S7 content, forecast note (< 0.1 CPU-h) | L |
| §18 | Fields 1, 2, 3, 6: error_bound helpers, route F, wrapper, replicated `_reference_posterior`, not-reused list | L + X |
| §20 item 14 | Replaced (merged constants and guards) | L + X |
| §21 | Row 15, new v3 row, C-19 v3 annotation | — |
| §22.3 F2 | v3 note: proof attached, review pending | — |
| §23 (new) | Merge record: inputs, X/L provenance, decision and RC6 mapping, 24 checked proof steps, errors found, open items | — |

## Errors found and fixed (detail in v3 §23.5)

- **L:** a Step-2 interval that does not yield its stated conclusion (fixed); an L5 underflow slip, 2⁻¹⁰⁰⁰ instead of 2⁻⁹⁷⁹ (fixed; still < ζ); reliance on the BLAS/reduction assumption A2 (removed per decision 2); a loose ρ̄ (tightened); an unsupported L1 remark (replaced); 80-digit context for a 60-digit envelope (clarified); P0 placement (moved to H1); no run-time rank check (added).
- **X:** conservative γ_{2m} rounding counts (tightened: 729·u′ instead of ≈ 1190·u); final normalisation looser than L3; underflow term valid only under gradual underflow (replaced by a mode-agnostic ζ); an unproved "twice the smallest normal" range rule (replaced by P1/ν₀); a P1-ladder certification claim (not adopted).
- **Both:** no check that the shared oracle's E_canon is identical across models (added at H1); the cross-model G 1e-12 check was unjustified (now proved, given permuted arrays); FREEZE_READY claims were premature.

## Left open for the coordinator or reviewer

1. Independent review of §15.3 (freeze blocker, RC6).
2. Confirm before freeze that the three models' E_canon arrays are bitwise identical. If they are not, decisions 4 and 9 need a ruling.
3. H5 uses a C1 tree-mean wrapper instead of calling `bootstrap_profile` directly, as RC1 wrote it. The index semantics are unchanged.
4. Band-hit labels at H5/V3: INCONCLUSIVE/NUMERICAL (adopted, from L) or HEADROOM/MODEL_HEADROOM (X).
5. The closed-form and named = canonical H3 checks remain absolute 1e-12, which a correct pipeline could trip in principle. Componentwise 4·10⁻¹² was suggested by L and is not ruled.
6. The H3 check for a reference row whose history fails P1 (absolute 2·10⁻¹²) has no proof.
7. P2/P4 limits (2¹⁹, 2²¹, 1/2) and their FAIL_TECHNICAL statuses.
8. Scope: eligibility, fits, M/F/V1/V2 and the P1 ladder are operational, not certified.
9. `_reference_posterior`: replicate it with provenance (adopted) or import it.
10. Route-F volume alarm: not adopted; the count is reported.
11. The A1 self-test vectors are to be fixed in API.md.
12. Carried from v2: reviewer confirmation of RC1–13, F1 (MERGE.md erratum), F6 (adapted-exception statuses).
