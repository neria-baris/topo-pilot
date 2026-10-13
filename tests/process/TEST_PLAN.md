# TEST_PLAN: process

Marker: `pytest.mark.process`. Uses `contracts.testing.tiny_world_spec` until `world` is accepted. Budget: under 20 s.

| ID | Test | Kind |
|---|---|---|
| P01 | Square, n = 3: T at the corner, edge, and centre equals hand values (stay 0.6 / 0.4 / 0.2; each neighbour 0.2) | known answer |
| P02 | Cylinder: no corner states; edge rows (y = 0) have stay 0.4; wrap neighbours have 0.2 | known answer |
| P03 | T symmetric, rows sum to 1, π uniform, π T = π, support ⊆ edges ∪ diagonal | contract |
| P04 | O: rows sum to 1; hand check of E for one state with σ = 1.25 against a direct formula in the test | known answer |
| P05 | O on core worlds: `factorizes` is True (outer-product reconstruction error < 1e-12) | property |
| P06 | P: the row multiset equals O's; `p_w` and H(W\|Z) are equal; factorisation is preserved | property |
| P07 | P: the x- and y-permutations depend on the world seed, not the replicate seed | contract |
| P08 | N: all rows equal 1/V. U: E is a permutation matrix | known answer |
| P09 | Symbol-name permutation changes `E` by a column permutation only, and the diagnostics are invariant | property |
| P10 | σ = 0 raises `INVALID_SIGMA`; a dead symbol (constructed) raises `INVALID_SIGMA` | error path |
| P11 | The emission builder signature does not accept T (inspect), and the transition builder does not accept E | contract |
| P12 | `FPSCenters` (extension readiness): on tiny_world_spec, centers are distinct and greedy maxmin by hand | known answer |
| P13 | `is_x_periodic` reads the wrap edges of the complex: core worlds known answer; a renamed family keeps its periodicity; crossed (flipped) wrap edges are not periodic; partial wrap edges, or 'x periodic' declared without wrap edges, raise `INVALID_GLUE` | known answer / error path |
| P20 | X5 G1 `test_conductance.py` (independent): warp profile, a = 0 equivalence, a = 0.2 validity, closed-form C_max, edge classes, metadata, ProcessStage save | known answer + contract |
