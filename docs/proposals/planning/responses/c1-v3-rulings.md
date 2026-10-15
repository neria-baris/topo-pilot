# Coordinator rulings on the C1-MERGED-v3 open items (§23.6)
1. **Review.** §15.3 goes to your review now; that is this pass.
2. **E_canon.** Bitwise identity across the three models is required at H1. If it does not hold, the result is FAIL_TECHNICAL: no shared oracle, consistent with the K4 identity/JoinError taxonomy. Decisions 4 and 9 stand.
3. **H5** goes through the C1 tree-mean wrapper, with the index stream unchanged. Accepted in place of a direct `bootstrap_profile` call.
4. **Guard-band hits** at H5 and V3 are labelled INCONCLUSIVE/NUMERICAL.
5. **Closed-form and named=canonical H3 checks** are aligned to the proved componentwise bounds, the same as decision 5, in place of an absolute 1e-12.
6. **A reference row that fails the underflow precondition** is checked against its route-F 60-digit Decimal enclosure, using the enclosure's own proved width.
7. **Smaller items** (P2/P4 limits, operational-only scope, replicating `_reference_posterior`, the route-F volume alarm, self-test vectors): the editor's defaults stand unless you require otherwise.
