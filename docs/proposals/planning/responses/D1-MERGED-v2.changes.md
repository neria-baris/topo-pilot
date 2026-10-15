# D1-MERGED-v2: review changes applied (v1→v2)

| Field | Value |
|---|---|
| Base document | `D1-MERGED-v1.md`, sha256 `A1E0779F06EB59B6193B0C26E2F32648B28A5C54E0260D4523FA9B237453C083` (verified) |
| Review | `coord-d1-merged-review-20261015.codex.md`, VERDICT: APPROVE_WITH_REQUIRED_CHANGES (8 required changes, 2 optional suggestions) |
| Output | `D1-MERGED-v2.md`, first line `STATUS: REVIEW_CHANGES_APPLIED (not frozen)`; sha256 at writing `2E4CDE3D2BE11E13D5D99BEA56D955B57A5A69C289A0D896AD383AA08070C50C` (LF line endings, as in v1) |
| Code checked | topo-pilot main @ `4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c` (= HEAD), read-only |
| Method | Each required change was applied with the reviewer's replacement text verbatim where the review gives one. Each instruction was checked against the code and by hand. No Python was run, no data was opened, and no git writes were made. |

## Change table

| change # | applied? | location (v2) | note |
|---|---|---|---|
| 1 | Yes, verbatim | §5.2 G0.3 (symmetric-difference sentence); §5.2 G0.6 (replaced); consistency edits in §6.1 field 4 ("one shared E object" → `vstack((E, E))`, bitwise, no identity) and the §5.2 G6 L1 cell (now refers to the G0.6 block-equality criterion) | Correct against the code. `world/lattice.py::_wrap` maps the flipped corner (4,y) to (0, 2−y), so the M seam is (3,0)–(0,2), (3,1)–(0,1), (3,2)–(0,0). The worlds share one seam edge and differ in 4. v1's "3 + 3" criterion would have rejected a correct build. |
| 2 | Yes, verbatim | §2.6 "Flat bounds" (the three bullets replaced; the glide bullet kept); §8.1 row; §8.2 C4 | Correct against `world/metrics.py`: glide (x+4, 2−y); copies `itertools.product((-1,0,1))`; `check_flat_bounds` tests `dist ≥ dist_graph/√2 − 1e-9`. Diameters rechecked by hand: C = 4, M = 3. |
| 3 | Yes, verbatim (heading/status sentence, G2.11, S4) | §3.6 (heading; status sentence; "Conjecture F." → "Theorem F (statement)." with F1–F3 unchanged; proof inserted; "Consequences (if adopted)" → "Consequences"; "Status and check" and the reviewer outline replaced by the proof and a "Check" paragraph); §5.1; §5.2 G2.11 (replaces CONJ); §5.2 G3 (F3 bullet added); §5.3; §6.2 module item 5; R11, R12, R14; §7.2 S3, S4; Summary (f); header Arithmetic row; §8.1; §8.2 C13; open question 3 | The proof is the review's "Decision-phase gap formula" re-derivation, rewritten in document notation. The editor re-derived it independently: F1, F2 and F3 all hold. G2.11 says "verify F3 … in G3", so G3 gets an explicit F3 bullet. All CONFIRMED/REFUTED and "reported, not gating" language is removed. |
| 4 | Yes, verbatim except for a notation substitution (flag N1) | §3.6 Consequences (dwell bullet); §3.7 item 2 (lazy stay, last bullet); §4 derivation (winding-count bullet) | Mathematics correct. For general a, K's boundary rows give (ρK)(0) − (ρK)(2) = (1−3a)δ with row sum 1−2a, which is 2/3 at a = 1/5. For t ≤ 8 there are at most 7 x-moves, so displacement ±12 is impossible. |
| 5 | Yes, verbatim | §5.2 G5 (comparison rule appended, plus a pointer to the trap); §6.2 test list (trap replaced; the blanket "~1e-17" claim deleted, with the reason given); R9 | Correct against `process/transition.py` and `tests/oracle_profile/independent_reference.py`. By hand: (1.0−0.2) rounds to float 0.8, so r = 0.8/4 = float(0.2). 3·0.8 rounds up at a tie, so d = 1 − 2.4000000000000004/4 = 3602879701896396·2⁻⁵³ and 2r = 3602879701896397·2⁻⁵³, giving d − 2r = −2⁻⁵³. The mixture-entry error at (A,A) is ½·3·2⁻⁵³/(4·1.6) ≈ 2.6e−17 > 1e−19. `_as_decimal` keeps Decimal inputs and otherwise uses `Decimal(float(x))`. |
| 6 | Yes, verbatim | §5.3 (PASS, FAIL and a new Controls bullet; INVALID kept); §5.1 (first-failure stop, NOT_RUN, mandatory §6 checks); §5.2 G6 (L1 and L2 cells, plus a harness note); §5.4 report (NOT_RUN status); §7.2 S3, S5 | Consistency edits beyond the verbatim text: §5.1 wording, S5 adopting NOT_RUN, and the report JSON listing NOT_RUN. |
| 7 | Yes, verbatim | §1.3 (the "L's caveat stands" paragraph replaced by the architecture caveat); §7.3 item 3 (the recurrent "must carry π" claim removed); R13 | Checked: Lemma D plus the differing two-step laws of h_A and h_B force S(h_A) ≠ S(h_B), and nothing more. |
| 8 | Yes, verbatim | New §5.5 "Freeze bindings"; header row; §5.4 store; §6.2 module and test file; §7.2 S0; open questions 5–6 closed | Request sha256 recomputed: `45b0e801…ceb7528`, a match. `git rev-parse HEAD` = `4f219d6…454c`, a match. As of 2026-10-15, `tools/d1_seam/`, `tests/d1_seam/` and `X:/Downloads/projects/topo-pilot/d1-seam-oracle-store/` do not exist. |
| O1 (optional) | Yes, flagged | §5.2 G5; §5.4 (651 → 650); §5.5; open question 6 | Needed for consistency: change 8's G5 set is 646 + {h_A, h_B, h_edge, h_max} = 650 distinct histories, because h* (t = 3) is already in the 646. v1's "651" counted h* twice. |
| O2 (optional) | No | — | Not needed for consistency. G0O.2 already requires a dual cycle with ∏ω = −1 for M. Left to the coordinator (decision 7). |

## Flags

- **N1 (reviewer text adapted, change 4).** The review writes the y-belief as μ_f (μ_f K/c, μ_M = R^par μ_C). In this protocol, μ is the start law (§0), and G4 already uses μ_f for the per-world start law δ_{(1,0)}. v2 therefore writes ρ_f, the §0 symbol for the y-marginal, as ρ′_f = ρ_f K/c and ρ_M = R^{par} ρ_C. The mathematics is unchanged.
- **H (consistency, change 3).** v1 labelled h_max "not a PASS witness", but G2.8 gates its values and G2.11 relies on it. It is relabelled "an enumeration probe, not a Theorem E witness".
- **G3 (change 3).** An F3 bullet is added to G3, as G2.11's text requires.
- **No reviewer instruction found wrong.** Changes 1, 2, 4, 5 and 8 were checked against code or recomputed. Changes 3, 4 and 7 were checked mathematically.
- **Residual, not changed.** "𝓗_I⁺" in §7.3 item 2 is not defined anywhere. It is inherited from v1 and outside the review's scope.
- **Not a flag.** G5's sentence that float inputs "would test the binary model instead" is kept. It is true, and it is not the deleted "~1e−17" magnitude claim.

## Decisions left for the coordinator

1. **Ratify the §5.5 bindings.** The review binds them as "existing proposed choices", but v1 reserved binding for the coordinator (AN C6; v1 open question 5). Ratify each binding explicitly:
   - enumeration depth K = 8;
   - module `tools/d1_seam/d1_seam.py`;
   - independent test file `tests/d1_seam/test_d1_seam.py`;
   - output store `X:/Downloads/projects/topo-pilot/d1-seam-oracle-store/`, which is outside the repo and does not yet exist, so it must be created before the run;
   - base commit `4f219d6ce4c73a2ef654f21ce1ef5ec6f220454c`;
   - request SHA256 `45B0E80152E324D2A0833DC5BC3B75853E1E9FD18B27C152887E41346CEB7528`;
   - G5 set: all reachable histories of length 1–5 plus h*, h_A, h_B, h_edge and h_max (650 distinct).
2. **Protocol hash.** At freeze:
   - compute the SHA256 of the exact text being frozen (v2 as written is `2E4CDE3D…070C50C`; any further edit changes it);
   - record it in the freeze record, optionally with a `D1-MERGED-v2.sha256` sidecar as for v1;
   - change the STATUS line, which itself changes the hash, so hash after the final edit.
3. **Freeze route.** Decide whether v2 freezes directly or returns to the reviewer for a confirmation pass on the applied text (owner policy part D).
4. **MERGE §2 adoption condition.** Confirm that the review satisfies "independent reviewer re-derives it" for Theorem F. The review was Codex, which also wrote track X. The formula is the analyst's. The review request called the review independent.
5. **Notation flag N1.** Accept ρ_f in place of the reviewer's μ_f in the dwell text.
6. **Test-file author.** Name the author of `tests/d1_seam/test_d1_seam.py`. The author must differ from the module's author and write the tests from the frozen protocol before the module exists (§6.2, X§9). The review did not bind this.
7. **Optional suggestion O2.** Decide whether the report must carry an explicit negative orientation-cycle witness for M (the list of dual-cycle squares with ∏ω = −1) alongside the ranks and boundary-component counts.
8. **Unspecified by the review (minor).**
   - When the mandatory §6.1–§6.2 checks (regression, new tests, registry hygiene, geometry guards, Decimal trap, file size) run relative to G0–G6.
   - Whether a failure of an existing regression test counts as FAIL, or as INVALID (environment). v2 states only that these checks are required for PASS and that an inability to evaluate invokes INVALID.
9. **Optional cleanup.** Define or remove "𝓗_I⁺" in §7.3 item 2.
10. **Owner questions 1–2 (not blocking).** The meaning of "topological distinction" (D-1 delivers orientability), and whether to run a downstream trained-model study.
