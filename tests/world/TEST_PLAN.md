# TEST_PLAN: world

Marker: `pytest.mark.world`. Budget: under 30 s.

| ID | Test | Kind |
|---|---|---|
| W01 | For square and cylinder with n ∈ {3, 4, 12}, ∂₁∂₂ = 0 over ℤ | contract |
| W02 | β over GF(2) and GF(3): square (1,0,0), cylinder (1,1,0) | known answer |
| W03 | Cell counts for n = 12: square V/E/F = 144/264/121; cylinder 144/276/132; χ = 1 and 0 | known answer |
| W04 | Graph cycle rank (E − V + 1) of the square is 121 while β₁ = 0, documenting that graph ≠ surface | known answer |
| W05 | Flat metric on the cylinder: d((11,y),(0,y)) = 1; d((0,0),(6,0)) = 6; metric axioms on the full matrix | known answer + property |
| W06 | `dist ≤ dist_graph + 1e-9` and `dist ≥ dist_graph / √2` | property |
| W07 | Relabelling vertices by a permutation leaves β unchanged (complex built from permuted ids) | property |
| W08 | A hand-built invalid complex (a face repeating a vertex) raises `INVALID_GLUE` | error path |
| W09 | Wrong `expected_betti` raises `BETTI_MISMATCH` | error path |
| W10 | `build_world` dispatches through the registry; an unknown family raises `INVALID_CONFIG` | contract |
| W11 | Extension readiness: an *in-test* builder (torus, both axes periodic, n = 4) registers and gives β (1,2,1) over GF(2) and GF(3) | contract |
| W12 | Extension readiness: an in-test Klein builder (flipped gluing, n = 4) gives (1,2,1) over GF(2) and (1,1,0) over GF(3) | known answer |
| W13 | `WorldStage.run` saves a `WorldSpec` that validates, and re-running gives the same id | contract |
