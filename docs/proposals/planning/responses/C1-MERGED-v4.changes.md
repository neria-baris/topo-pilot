# C1-MERGED-v4: review-fix change record

- **Input:** `C1-MERGED-v3.md`, sha256 A163929CBC31CA3D0966E5ACD5EEE8C6E8846B7711E07D29E933EFCD58A132EA (unchanged).
- **Review:** `coord-c1-merged-review-20261015.v3confirm.codex.md`, sha256 EDC9196F86F220A754E9CFAACE5A6EE045FCC97D7AEA6AAC80EB21667F6B5D7A, verdict NOT_CONFIRMED, fixes 1–7.
- **Rulings:** `c1-v3-rulings.md`, sha256 2EB4A22C8F33CF0F8FE8746F831B795282EF817479BD1DF878635BC367338A9A. Rulings 5 and 6 are superseded by fixes 2 and 3. Rulings 2, 3, 4 and 7 are written into the protocol text.
- **Output:** `C1-MERGED-v4.md`, sha256 C2D64A79DA076ABF5651229A60E33A934102B4161C79C2F4A16195BA3C27EA89, LF line endings. First line `STATUS: REVIEW_FIXES_APPLIED (not frozen)`. The full record is in its §24.
- **Method:** document editing only. No code was run, no data was accessed, and nothing was written to git.

## Fixes

| Fix | Main sections | Change | Flags |
|---|---|---|---|
| 1 L5 / lemma U | §15.3.3 P2, §15.3.5, §15.3.11 Thm 5, §15.3.16 item 9, §20 item 14, §23.4 items 19–20 | L5 premises and proof replaced verbatim: leaves ≤ 2²³, degree ≤ 7, ≤ 2¹⁶ monomials, ≤ 2¹⁷ nodes, allowance 2⁻⁸⁰⁵. Expression-count table added. "Fewer than 7,000 leaves" withdrawn. U uses operands ≤ 2⁶⁴, giving 2⁻⁸⁷³. P2 checks 2²³ on every bound leaf. L5 test fixtures restricted to the premises. | V4-F5 |
| 2 two-evaluation H3 checks | §3.2, §3.3, §15.3.12, §16 row 3, §15.3.16 item 15 | Named = canonical: componentwise relative 4·10⁻¹² on the normal fast path. Closed form: exact T/π invariance, r_E, ε_sym, 62ε_sym, t + t², enclosures otherwise. No absolute 1e-12 rule remains for these two checks. | V4-F1, F3, F4, F7, F8 |
| 3 P1-failing reference rows | §3.4, §15.3.3 P4, §15.3.7, §16 row 3 | Interval I_v, a = 2·10⁻¹², D_low/D_high, three-way PASS / FAIL_TECHNICAL/ORACLE / INCONCLUSIVE/NUMERICAL. P4 concerns predictives only. | V4-F4 |
| 4 mass of the literal target | header erratum, §1.2, §1.3, §3.3, §12.1, §12.5, §15.3.16 item 5, §17 | Verbatim m_±/δ_m qualification. ½kδ_m; A_β = βA − ½δ_m(log Z_β⁺ − log Z_β⁻); A_oracle = G* − ½δ_m log(m₊/m₋). Unconditional identities made conditional. KL and regret are literal sums. Tests updated. | V4-F2 |
| 5 exception statuses | §16 conventions, §18 field 2, §22.3 F6 | The reviewer's mapping inserted verbatim; F6 resolved. | — |
| 6 consistency | §11, §2.2, §16 row 20, §15.3.16 item 14, §17, §18 field 5 | V3 three-way rule; fresh primary/control A, Y, Z after T-PRE, with A_full and Z_full inside T-PRE for V3; production-fit invariant. | V4-F6 |
| 7 INCONCLUSIVE/NUMERICAL projection | §15.3.13 | Paragraph replaced verbatim (illustrative, conditional; ≈ 5·10⁻⁵). | — |

**Expression counts (fix 1).** All are within the reviewer's limits, so no allowance needed recomputing:

| Bound | Nodes | Monomials | Degree |
|---|---|---|---|
| b^G | 1,117 | 1,081 | 6 |
| b^A | 474 | 254 | 6 |
| b^Y | 15,711 | 8,416 | 7 |
| b^Z | 16,837 | 9,501 | 7 |
| b^Zf | 1,600 | 1,339 | 7 |

**Formula checks.** Every reviewer formula was re-derived (§24.4), and none was found to be wrong. Two supplements were needed:
- V4-F1: the reviewer's ε_E collides with P0's ε_E = min E_canon, so it is renamed ε_sym.
- V4-F2: Z_β^± = Σ_v p^±(v)^β is defined. A raw-logit normaliser would make the A_β formula incomplete.

The 4·10⁻¹² tolerance rests on the proved bound (≈ 2.11·10⁻¹²), not on 2δ/(1−δ), which is fractionally above 4·10⁻¹².

## Open items

1. Reviewer confirmation of v4 (freeze blocker).
2. **V4-F4:** confirm or replace the editor's concretizations of the branches the fixes left without a criterion: the closed-form enclosure branch, and named = canonical off the normal fast path. Both have an expected count of 0.
3. **V4-F3:** confirm the definition of the "normal fast path" (P1 applied to the evaluated posteriors), and FAIL_TECHNICAL/ORACLE for inexact T/π invariance.
4. **Coordinator:** update the MERGE addendum's erratum to the mass-qualified anchor (fix 4). This is outside this edit's write scope.
5. **Result-blind pre-freeze confirmations from stored arrays:** E_canon bitwise identity across the models (ruling 2), and exact ρ_k-invariance of T and π (V4-F8).
6. **Freeze task:** fix the A1 self-test vectors in API.md (ruling 7).
