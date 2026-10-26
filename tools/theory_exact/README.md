# theory_exact

Process-only computations for `docs/proposals/THEORY_TRACK_HE.md` (owner go-ahead 2026-10-26). No models and no project data: matrices come from the project builders, and histories are sampled here with fixed seeds.

Run from this folder with the project venv:

- `python sym_check.py`: symmetry groups from the plan's formulas (Theorem 1.1).
- `python theory_exact.py 1000` and `python theory_exact.py 3000`: symmetry groups on the project matrices; certificate numbers for belief, prediction and window-k clouds (Theorem 1.4, sections 5.1–5.3). Writes `theory_exact_results.json`.
- `python theory_exact2.py`: harmonic structure of the optimal centred log-predictions (section 5.5) and the winding rank for torus, cylinder and square (section 5.4).
- `python null_kappa.py`: null calibration of kappa (section 5.6).
- `python theory_exact3.py 1000 <seed>` (seeds 1, 2, 3): searched circle maps on the square cloud, hybrid worlds for the axis-permuted prediction loop, and ripser H1 barcodes (sections 5.6–5.7). Writes `theory_exact3_results_n1000_s<seed>.json`.
- `python kappa_ceiling.py 500,1000,2000`: the ceiling of Corollary 2.2 (largest death/birth ratio over H1 bars) next to the fixed-map kappa, by sample size and seed (Conjecture 1.5, section 5.6).

Outputs used in the document are in `docs/proposals/THEORY_OUTPUTS/`. The null-calibration numbers are quoted in section 5.6 from the console output.
