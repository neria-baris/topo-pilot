# C1-MERGED-v2: required-change application record

- **Input:** `C1-MERGED-v1.md`, sha256 72C86FFC0C76386EBD1FF6D991D0AB2DE62684FB2334831628A9D3DCCB0745D7 (unchanged).
- **Review:** `coord-c1-merged-review-20261015.codex.md`, sha256 2894E60410FD3C808059ABC7ABF71DA0A0DA3774D58FDF7971226BC144E6AB17, verdict APPROVE_WITH_REQUIRED_CHANGES.
- **Output:** `C1-MERGED-v2.md`, sha256 F9F679DC0DFF74D7765B7A3E2AB0B5CB98ADE6DC73707EE367D0BC01257E12F6. Its first line is `STATUS: REVIEW_CHANGES_APPLIED (not frozen)`, and its §22 records the full detail.
- **Code checked:** `topo-pilot` main @4f219d6, read-only.

| RC | Applied? | Location in v2 | Note |
|---|---|---|---|
| 1 | Yes, verbatim | §3.5; §16 rows 5, 20; §18 field 1 | The `Generator(PCG64(seed))` call and the `result["B"][:, 0]` extraction match the code (`oracle_profile.py` 194–224). |
| 2 | Yes, verbatim | Header erratum; §1.3 anchor; §8.3; §12.1; §21 | The θ = 1 claim is removed everywhere in v2. MERGE.md is **not** edited (F1). |
| 3 | Yes, verbatim | §1.2 E2 cell and note; §1.3; §6 (raw-norm, B3-C); §12.1; §21 C-1; §20 item 5 | The E2 text sits as a note under the table (F8). |
| 4 | Yes, verbatim | §1.1; §1.2 E3; §1.4; §5.2; §7; §8.3 | "Phase-only" is gone everywhere. The PASS conclusion keeps v1's scope sentence (F7). |
| 5 | Yes, verbatim, plus one specification | §5.2; §6; §14; §16 row 8; §20 item 3 | The "appropriate degeneracy failure" mapping is specified by the editor (F3). |
| 6 | Yes, verbatim | §15.3 (replaced); §13 step 2; §15.2; §16 row 21; §20 item 14; §21 C-19; header | The certificate is **NOT_READY**: freeze stays blocked until the proof is attached and reviewed (F2). |
| 7 | Yes, verbatim | §6 M1 definitions; §16 row 9; §17 Author B | The 1e-10 and 1e-12 thresholds are retained. |
| 8 | Yes, verbatim | §16 conventions; §17 S2; §18 fields 2, 3, 6; §21 C-10, C-12, C-13 | All cited code facts are confirmed. The statuses of the adapted exceptions are unspecified by the review (F6). |
| 9 | Yes, verbatim | §14 (override, Branches A, B, C); §16 row 0; §17 resources and S0; §18 field 2 | The lift cap of 30 s is confirmed (`cochain.py` 147; CONTRACT 131). JSON null must be decoded before `float()` (F5). |
| 10 | Yes, verbatim | §2.4; §16 rows 2, 20 | The source labels are renamed (a)–(d) to avoid a clash with the review's R_1/R_2 (F4). |
| 11 | Yes, verbatim | §12.2 (retitled "Ratio-to-mean reduction"); §13; §1.4; §17 Author A; §21 | The all-PASS/all-FAIL/MIXED rule is retained. |
| 12 | Yes, verbatim | §2.2; §5.1; §6; §12.5; §14 Branch C; §16 rows 10, 18–20; §17 Author B; §19 item 9; §21 C-17 | No "no logits computed" claim remains. |
| 13 | Yes, verbatim | §11 | — |

## Flags

- **F1.** The reviewer requires the RC2 correction in the MERGE ruling as well. MERGE.md is outside this edit's scope and still contains "so an oracle-perfect readout gives θ = 1" (ruling 4) and "crossed ± donors that anchor θ = 1" (lesson 4). **The coordinator must record the erratum there.**
- **F2. Freeze blocker.** The §15.3 certificate is NOT_READY. Reviewer confirmation of v2 alone does not permit freeze.
- **F3.** RC5's degeneracy mapping was specified by the editor, for the reviewer to confirm. For W B, F1 already returns PATCH_MODEL_DEGENERATE. For a frame G_r, a zero diag(R_r) entry fails M1 orthonormality (FAIL_TECHNICAL). Note that Householder QR stays orthonormal for nearly rank-deficient input.
- **F4.** The v1 registry source labels (R1)–(R4) were renamed (a)–(d). Releases R1–R3 are unchanged.
- **F5.** This is a code note, not a reviewer error. `integer_lift` calls `float(cfg["lift_cpu_cap_s"])`, so `null` must reach it as `inf`. K4's `native_operation_wall_s` is 180; C1's 600 is a C1-contract value.
- **F6. Open point.** The review does not give the statuses (FAIL_TECHNICAL or INCONCLUSIVE) for adapted `StageFailure`/`ProfileError`/Decimal exceptions. v2 does not invent them.
- **F7.** v1's scope qualifiers are retained after the verbatim PASS conclusion. They narrow the claim and add nothing.
- **F8.** The multi-paragraph E2 replacement is placed as a note under the §1.2 table and repeated in §12.1.
- **F9. No reviewer instruction was found to be wrong against the code.** All cited facts were verified (v2 §22.4).
- **F10.** No optional suggestion was applied. In particular, §20 values, the RidgeProbe 1e-10 tolerance, the Sup(·) definitions and the "binomial SD ≈ 0.004" note are unchanged.
- **Consistency edits** beyond the reviewer's listed locations are itemised in v2 §22.2. Each one follows from a required change. Examples are the §1.4 PASS bullet 1 and the V3 sentence under FAIL, §5.2 "identified" → "estimated", the §12.2 heading, and the §16, §17, §18, §19 and §20 restatements.
