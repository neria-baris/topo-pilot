# `tests/c2_readout/test_a_gls.py`

- Source: [tests/c2_readout/test_a_gls.py](../../../../../tests/c2_readout/test_a_gls.py)
- Kind: python
- Lines: 347

## Module docstring

> Independent tests, author A (job 0101; v2 update): T-GLS part 2, the G1 scale-invariance
> fixture of D-0104-2 and the GLS-REF fixtures 1-6 of NEW-1 (C2-FROZEN-v2 2.5, 9.2, 13.3). T-GLS
> part 1 (Lemmas G1-G3, the whitened-design fixtures) is in test_a_readout.py; T-LADDER moved to
> test_a_oracle.py (the 400-line limit).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](../../tools/c2_readout/c2_config.py.md) (line 29, via sys.path edit)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../../tools/c2_readout/c2_code.py.md) (line 30, via sys.path edit)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../../tools/c2_readout/c2_stats.py.md) (line 31, via sys.path edit)

### External (third-party)

- `numpy` (lines 22)
- `pytest` (lines 23)

### Standard library

- `__future__` (lines 14)
- `decimal` (lines 16, 18)
- `fractions` (lines 19)
- `pathlib` (lines 20)
- `sys` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 27: `str(REPO / 'tools' / 'c2_readout')` -> `tools/c2_readout`

## Imported by

- none

## Top-level constants

- `DEG`
- `REPO`

## Classes and functions

- **function `_F`** [L38-39]: `def _F(M)`
- **function `_mm`** [L42-44]: `def _mm(A, B)`
- **function `_tr`** [L47-48]: `def _tr(A)`
- **function `_sub`** [L51-52]: `def _sub(A, B)`
- **function `_f2`** [L55-56]: `def _f2(A)`
- **function `_solve`** [L59-70]: `def _solve(A, B)`
- **function `_dsqrt`** [L73-75]: `def _dsqrt(fr)`
- **function `_fd`** [L78-79]: `def _fd(s)`
- **function `_exact_proj`** [L82-87]: `def _exact_proj(A, Gamma, B)`
- **function `_problem`** [L90-95]: `def _problem(p=12, K=1, seed=0, spread=1.0)`
- **function `_whit_asym`** [L99-102]: `def _whit_asym(P, Sigma)`
- **function `_planted`** [L105-111]: `def _planted(g, Gamma, B, V)` - An oblique projector in the metric V: every G1 identity except self-adjointness holds.
- **test `test_g1_check_is_scale_invariant_and_rejects_a_non_self_adjoint_projector`** [L114-137]: `def test_g1_check_is_scale_invariant_and_rejects_a_non_self_adjoint_projector()`
- **function `_embedded`** [L141-147]: `def _embedded(delta=DELTA)`
- **function `_patch_dsolve`** [L150-164]: `def _patch_dsolve(monkeypatch, p, m, first=None, second=None)` - Replace the first solve Y* = A^-1 X_n (A is p x p) by `first`, or add `second` to the
- **test `test_fixture1_first_solve_error_propagation_independent_exact`** [L167-184]: `def test_fixture1_first_solve_error_propagation_independent_exact()`
- **test `test_fixture1_module_bound_covers_the_true_error_and_is_not_accepted`** [L187-197]: `def test_fixture1_module_bound_covers_the_true_error_and_is_not_accepted(monkeypatch)`
- **test `test_fixture2_perturbed_operator_residual_r_g`** [L200-208]: `def test_fixture2_perturbed_operator_residual_r_g(monkeypatch)`
- **function `_up`** [L211-212]: `def _up(fr2)`
- **test `test_fixture2_independent_r_c_and_r_g_perturbations_lemma_gr`** [L215-234]: `def test_fixture2_independent_r_c_and_r_g_perturbations_lemma_gr()`
- **test `test_fixture3_lemma_inv_bound_and_non_acceptance`** [L237-255]: `def test_fixture3_lemma_inv_bound_and_non_acceptance(monkeypatch)`
- **test `test_fixture4_euclidean_case_conditioning_differs_from_whitened`** [L258-275]: `def test_fixture4_euclidean_case_conditioning_differs_from_whitened()`
- **test `test_fixture5_reduced_precision_enclosure_and_trap`** [L278-299]: `def test_fixture5_reduced_precision_enclosure_and_trap()`
- **test `test_fixture6_eps_p_enters_delta_p_and_the_gate`** [L302-312]: `def test_fixture6_eps_p_enters_delta_p_and_the_gate(monkeypatch)`
- **test `test_accepted_reference_bounds_the_exact_projector_distance`** [L315-327]: `def test_accepted_reference_bounds_the_exact_projector_distance()`
- **test `test_dctx_dsolve_dinverse_against_exact_rationals`** [L330-347]: `def test_dctx_dsolve_dinverse_against_exact_rationals()`

