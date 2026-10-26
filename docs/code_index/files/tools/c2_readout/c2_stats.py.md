# `tools/c2_readout/c2_stats.py`

- Source: [tools/c2_readout/c2_stats.py](../../../../../tools/c2_readout/c2_stats.py)
- Kind: python
- Lines: 395

## Module docstring

> C2 statistics (the pre-allowlisted overflow module): GLS-REF, the 80-digit Decimal reference of
> every projector problem accepted by the composed residual bound with verified inverse-norm
> bounds (Lemmas GR, INV), the L1 decoders D0/D_code/D_lin with the explicit standardisation recipe
> and the R13 equivalence check, the P1 ladder and the MDE reports (API.md §9; C2-FROZEN-v1 §2.5,
> §6.6, §6.7, §9.2, §9.3 T12, T17).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 20, via same directory)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../c1prime/c1_fit.py.md) (line 23, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](c2_code.py.md) (line 24, via same directory)
- `import precision` -> [tools/x4_circle_history/precision.py](../x4_circle_history/precision.py.md) (line 26, via unique basename)
- `from topo_pilot.analysis import x4f_scores` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 28, via package root)
- `from topo_pilot.experiment.x4f_probe import nested_ridge` -> [src/topo_pilot/experiment/x4f_probe.py](../../src/topo_pilot/experiment/x4f_probe.py.md) (line 29, via package root)
- `from topo_pilot.prediction.ridge import RidgeProbe` -> [src/topo_pilot/prediction/ridge.py](../../src/topo_pilot/prediction/ridge.py.md) (line 30, via package root)

### External (third-party)

- `numpy` (lines 25)

### Standard library

- `__future__` (lines 12)
- `dataclasses` (lines 16)
- `decimal` (lines 14, 17)
- `fractions` (lines 18)
- `operator` (lines 15)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_readout/test_a_gls.py](../../tests/c2_readout/test_a_gls.py.md) (line 31, import)
- [tests/c2_readout/test_a_oracle.py](../../tests/c2_readout/test_a_oracle.py.md) (line 37, import)
- [tests/c2_readout/test_a_scope.py](../../tests/c2_readout/test_a_scope.py.md) (line 39, import)
- [tests/c2_readout/test_b_fwl_l1.py](../../tests/c2_readout/test_b_fwl_l1.py.md) (line 23, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 28, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 26, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 21, import)

## Top-level constants

- `FIELDS`
- `KEYS`
- `KINDS`
- `P1_ARRAYS`
- `P1_SEEDS`
- `TRAPS`
- `ZERO`

## Classes and functions

- **function `dctx`** [L42-43]: `def dctx(prec=80) -> decimal.Context`
- **function `D`** [L46-48]: `def D(M) -> list` - Exact Decimal(float) entries of a 2-d array.
- **function `dmatmul`** [L51-53]: `def dmatmul(A, B) -> list`
- **function `dsub`** [L56-57]: `def dsub(A, B) -> list`
- **function `dabs`** [L60-61]: `def dabs(A) -> list`
- **function `deye`** [L64-65]: `def deye(n) -> list`
- **function `dT`** [L68-69]: `def dT(A) -> list`
- **function `frob`** [L72-73]: `def frob(A) -> Decimal`
- **function `inflate`** [L76-77]: `def inflate(x) -> Decimal`
- **function `deflate`** [L80-81]: `def deflate(x) -> Decimal`
- **function `theta`** [L84-88]: `def theta(q) -> Decimal` - theta_q = q u_D / (1 - q u_D), u_D = 1/2 10^(1 - p) at the active precision p.
- **function `dsolve`** [L91-106]: `def dsolve(A, Bm) -> list` - A^-1 Bm by Gauss-Jordan elimination with partial pivoting (largest |entry|, ties to the
- **function `dinverse`** [L109-110]: `def dinverse(A) -> list`
- **function `enclosure`** [L113-121]: `def enclosure(R_tilde, fixed, left, right, q) -> Decimal` - Verified upper bound on ||R||_F of R = fixed - left right (inner dimension q), from the
- **function `_ref`** [L125-178]: `def _ref(o, A, Gamma, B, PS_hat, PG_hat, euclidean) -> None` - The §2.5 steps in order; fills `o` (Decimal values as str).
- **function `gls_ref`** [L185-202]: `def gls_ref(A, Gamma, B, P_S_hat, P_G_hat, euclidean=False, prec=80) -> dict` - GLS-REF of one projector problem (A = Sigma_eps; Euclidean: A = I, Y* = X_n). Accepted
- **function `delta_p`** [L205-208]: `def delta_p(ref, tag='S') -> float` - delta_P as a float upper bound for the NUM guard (inf if not available).
- **class `Decoder`** [L213-228] decorators: @dataclass
- **method `Decoder.predict`** [L223-224]: `def predict(self, F) -> np.ndarray`
- **method `Decoder.ok`** [L227-228]: `def ok(self) -> bool` decorators: @property
- **function `fit_decoder`** [L234-247]: `def fit_decoder(F_fit, Y_fit, panel_fit) -> Decoder` - lambda* by nested_ridge (LOPO over the FIT panels; standardises internally), then
- **function `decoder_features`** [L250-257]: `def decoder_features(kind, w32, zt, code=None, full=None) -> np.ndarray`
- **function `decoder_arrays`** [L260-261]: `def decoder_arrays(dec) -> dict`
- **function `decoder_from_arrays`** [L264-268]: `def decoder_from_arrays(d) -> Decoder`
- **function `_sse`** [L271-272]: `def _sse(Y, pred) -> float`
- **function `l1`** [L275-292]: `def l1(Y, pred0, pred_code, pred_lin) -> dict` - PASS iff SSE_0 > 0, SSE_0 - SSE_lin > 0, R2_code|0 >= 1/2 and rho_inc >= 9/10 (exact
- **function `l1_complete_scores`** [L295-301]: `def l1_complete_scores(Y, preds, w32, class_means_fit) -> dict` - Descriptive R^2_X = 1 - SSE_X / sum ||f1 - f1-bar_w||^2 and R^2_code / R^2_lin.
- **function `_cfg`** [L305-307]: `def _cfg(alpha, alternative, N) -> dict`
- **function `_summaries`** [L310-323]: `def _summaries(arrays, afull, models, seeds, alpha, alternative) -> dict` - One sd_b4_draws call per array (4,096 VAL rows) and one centered_draws +
- **function `p1`** [L326-349]: `def p1(family, arrays, afull, models, alpha) -> dict` - N_F = the smallest N at which every model passes every gated array; else the smallest N
- **function `mde_report`** [L352-361]: `def mde_report(arrays, models, seed_sd, seed_c, alpha) -> dict` - The same kernels for the arrays that are reported only (energy, M share); seeds by
- **function `n_test`** [L364-366]: `def n_test(N_by_family) -> tuple`
- **function `f1_problem`** [L370-379]: `def f1_problem(Y, w32, zt, f, euclidean=False, fit=None) -> dict` - c2_code.problem plus GLS-REF (only when the float part passed): F1 of one problem.
- **function `fit_decoders`** [L385-389]: `def fit_decoders(w32, zt, code, full, target, panel) -> dict`
- **function `l1_split`** [L392-395]: `def l1_split(decs, w32, zt, code, full, target) -> dict` - The frozen FIT decoders scored on another split's natural rows (FEAS, TEST).

