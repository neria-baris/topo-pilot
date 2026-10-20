# `tools/c1prime/c1_fit.py`

- Source: [tools/c1prime/c1_fit.py](../../../../../tools/c1prime/c1_fit.py)
- Kind: python
- Lines: 224

## Module docstring

> C1' FWL phase map, forced states, within-class whitening, Haar control frames, M1 identities
> and fixed decoders (API.md §9; protocol §5.2-§5.5, §6, §7). Calibration fits only.

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 8, via same directory)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 10, via same directory)
- `from topo_pilot.analysis import x4f_scores` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 12, via package root)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 13, via package root)
- `from topo_pilot.experiment.x4f_probe import nested_ridge` -> [src/topo_pilot/experiment/x4f_probe.py](../../src/topo_pilot/experiment/x4f_probe.py.md) (line 14, via package root)
- `from topo_pilot.prediction.ridge import RidgeProbe` -> [src/topo_pilot/prediction/ridge.py](../../src/topo_pilot/prediction/ridge.py.md) (line 15, via package root)

### External (third-party)

- `numpy` (lines 9)

### Standard library

- `__future__` (lines 4)
- `dataclasses` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c1prime/test_a_eligibility_support.py](../../tests/c1prime/test_a_eligibility_support.py.md) (line 25, import)
- [tests/c1prime/test_b_decoder.py](../../tests/c1prime/test_b_decoder.py.md) (line 32, import)
- [tests/c1prime/test_b_frames.py](../../tests/c1prime/test_b_frames.py.md) (line 28, import)
- [tests/c1prime/test_b_fwl.py](../../tests/c1prime/test_b_fwl.py.md) (line 27, import)
- [tests/c1prime/test_b_gates.py](../../tests/c1prime/test_b_gates.py.md) (line 24, import)
- [tests/c1prime/test_c_ridge_tolerance.py](../../tests/c1prime/test_c_ridge_tolerance.py.md) (line 18, import)
- [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 13, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 17, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 16, import)

## Top-level constants

- `EQ_C`
- `GRID`

## Classes and functions

- **function `standardise_nuisance`** [L21-24]: `def standardise_nuisance(z_cal) -> tuple`
- **function `unit`** [L27-29]: `def unit(phi) -> np.ndarray`
- **function `fwl_design`** [L32-35]: `def fwl_design(w32, zt, f) -> np.ndarray`
- **function `fit_fwl`** [L38-45]: `def fit_fwl(a, w32, zt, phi) -> dict`
- **function `f1_check`** [L48-51]: `def f1_check(fit) -> str`
- **function `partial_r2`** [L54-61]: `def partial_r2(a, w32, zt, phi) -> float` - Within-class partial R^2 of f(phi) (reported, not gated).
- **function `forced`** [L64-65]: `def forced(a, B, phi_s, phi_d) -> np.ndarray`
- **function `residual`** [L68-70]: `def residual(a, w32, zt, fit) -> np.ndarray`
- **function `whitening`** [L73-81]: `def whitening(r_cal) -> dict`
- **function `qr_pos`** [L84-86]: `def qr_pos(M) -> np.ndarray`
- **function `primary_coords`** [L89-91]: `def primary_coords(W, B, Delta) -> tuple`
- **function `haar_frames`** [L94-97]: `def haar_frames(model_seed, count=32) -> list`
- **function `control_delta`** [L100-101]: `def control_delta(W_inv, Q_r, c) -> np.ndarray`
- **function `_rel_norm`** [L104-107]: `def _rel_norm(primary, other) -> float`
- **function `_spectrum_dev`** [L110-115]: `def _spectrum_dev(S_p, S_r) -> float`
- **function `m1_report`** [L118-143]: `def m1_report(W, Delta_pm, Qt, frames, c_pm, W_inv=None) -> dict`
- **class `Decoder`** [L147-165] decorators: @dataclass
- **method `Decoder.features`** [L160-162]: `def features(self, a) -> np.ndarray`
- **method `Decoder.predict`** [L164-165]: `def predict(self, a) -> np.ndarray`
- **function `equivalence_tolerance`** [L171-181]: `def equivalence_tolerance(Ft, lam, pred) -> tuple` - R13: the M1 cho_solve-vs-lstsq tolerance. Both solvers are backward stable on the same
- **function `fit_decoder`** [L184-203]: `def fit_decoder(a_cal, Y_cal, panel_cal, model_seed, target) -> Decoder`
- **function `w_hat`** [L206-207]: `def w_hat(dec_w, a) -> np.ndarray`
- **function `decoder_arrays`** [L210-214]: `def decoder_arrays(dec) -> dict`
- **function `decoder_from_arrays`** [L217-224]: `def decoder_from_arrays(a) -> Decoder` - Rebuild the frozen decoder (no refit): RidgeProbe with its stored W and bias.

