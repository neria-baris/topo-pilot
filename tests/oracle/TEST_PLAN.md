# TEST_PLAN: oracle

Marker: `pytest.mark.oracle`. Written by an **independent** test writer. Budget: under 20 s.

| ID | Test | Kind |
|---|---|---|
| O01 | Brute force: for `tiny_hmm` (N = 4) and every token sequence of length 4 (V = 3 → 81 sequences), enumerate all 4⁴ state paths in the test; posterior marginals, predictive q, and evidence match to 1e-10 | known answer |
| O02 | q₀ = πE for every row | known answer |
| O03 | U-like process (E = I): b_t = δ_{w_t} and q_t = row w_t of T E | known answer |
| O04 | N-like process (E uniform): b_t = π for all t, and q is uniform | known answer |
| O05 | Sum over j of F2 gives F1; F1 = q; F2 matches brute force on `tiny_hmm` for 2-step futures | known answer |
| O06 | `LastSymbolPosterior.r` equals the filter belief after a single symbol with prior π | known answer |
| O07 | `context_gain` ≥ 0 (property over random beliefs); equals 0 when q_C = q_last | property |
| O08 | An impossible history (a token with E[:,w] = 0 on the support) raises `IMPOSSIBLE_HISTORY` | error path |
| O09 | Long sequence (33) of a near-deterministic HMM: no underflow (log-evidence finite, beliefs normalised) | property |
| O10 | Observability singular values: E = I gives full rank N at k = 1; uniform E gives rank 1 | known answer |
| O11 | `OracleStage` refuses (via policy) to load an `EvalSidecar` | error path |
