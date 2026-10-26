# `tools/c2_readout/c2_code.py`

- Source: [tools/c2_readout/c2_code.py](../../../../../tools/c2_readout/c2_code.py)
- Kind: python
- Lines: 307

## Module docstring

> C2 code: the K = 1, 2, 3 FWL fit, Ledoit-Wolf, the whitened-design checks, the QR-route GLS
> operator and its Euclidean variant, the Lemma G1 identities, the interchange, the code phase,
> the R1 wrapper with the zero-modulus overrides, the N2 radial support screen, the Haar frames and
> the masked S* features (API.md §8, §19.3; C2-FROZEN-v2 §2.4, §2.5, §2.8, §2.10, §2.11, §6.6).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 14, via same directory)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](../c1prime/c1_fit.py.md) (line 17, via unique basename)
- `import c1_gates` -> [tools/c1prime/c1_gates.py](../c1prime/c1_gates.py.md) (line 18, via unique basename)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](c2_oracle.py.md) (line 19, via same directory)
- `from topo_pilot.analysis import x4f_scores` -> [src/topo_pilot/analysis/x4f_scores.py](../../src/topo_pilot/analysis/x4f_scores.py.md) (line 23, via package root)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 24, via package root)

### External (third-party)

- `numpy` (lines 20)
- `scipy` (lines 21)

### Standard library

- `__future__` (lines 10)
- `fractions` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_readout/test_a_gls.py](../../tests/c2_readout/test_a_gls.py.md) (line 30, import)
- [tests/c2_readout/test_a_oracle.py](../../tests/c2_readout/test_a_oracle.py.md) (line 34, import)
- [tests/c2_readout/test_a_partition.py](../../tests/c2_readout/test_a_partition.py.md) (line 34, import)
- [tests/c2_readout/test_a_readout.py](../../tests/c2_readout/test_a_readout.py.md) (line 29, import)
- [tests/c2_readout/test_a_scope.py](../../tests/c2_readout/test_a_scope.py.md) (line 37, import)
- [tests/c2_readout/test_b_fwl_l1.py](../../tests/c2_readout/test_b_fwl_l1.py.md) (line 22, import)
- [tests/c2_readout/test_b_policy.py](../../tests/c2_readout/test_b_policy.py.md) (line 24, import)
- [tests/c2_readout/test_b_screens.py](../../tests/c2_readout/test_b_screens.py.md) (line 22, import)
- [tools/c2_readout/c2_attrib.py](c2_attrib.py.md) (line 21, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 21, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 20, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 15, import)
- [tools/c2_readout/c2_stats.py](c2_stats.py.md) (line 24, import)

## Top-level constants

- `DEG`
- `N_CLASS`

## Classes and functions

- **function `_le`** [L31-33]: `def _le(x, limit) -> bool` - x <= the exact CONTRACT value `limit` (a non-finite x fails).
- **function `harmonics`** [L37-43]: `def harmonics(phi, K) -> np.ndarray` - (cos phi, sin phi, cos 2 phi, sin 2 phi, ..., cos K phi, sin K phi).
- **function `standardise`** [L46-47]: `def standardise(z_fit) -> tuple`
- **function `fwl`** [L50-68]: `def fwl(Y, w32, zt, f) -> dict` - OLS of Y on [onehot(w32), zt, f] (36 + 5 + 2K columns) by numpy.linalg.lstsq.
- **function `f1_fwl`** [L71-80]: `def f1_fwl(fit) -> str` - Design rank 41 + 2K, cond <= 1e8, sigma_max(B) > 0, sigma ratio >= 1e-6 (F1).
- **function `ledoit_wolf`** [L83-84]: `def ledoit_wolf(resid) -> np.ndarray`
- **function `lw_ok`** [L87-89]: `def lw_ok(S) -> bool`
- **function `partial_r2`** [L92-100]: `def partial_r2(Y, w32, zt, f) -> float` - Within-class partial R^2 of f (reported): 1 - RSS(full) / RSS(base).
- **function `gls`** [L104-128]: `def gls(Gamma, B, Sigma=None) -> dict` - L = R_x^-1 Q_x' R_Sigma^-T with Sigma = Lc Lc' and X~ = Lc^-1 X_n = Q_x R_x (GLS), or the
- **function `_mx`** [L131-133]: `def _mx(x) -> float`
- **function `gls_identities`** [L136-161]: `def gls_identities(g, Gamma, B, Sigma=None) -> dict` - Lemma G1 in the scale-invariant form of v2 §2.5 (D-0104-2) on the production L and
- **function `interchange`** [L164-168]: `def interchange(y1, y2, P_S) -> tuple` - (y_S^{2<-1}, y_S^{1<-2}): arm 2 receives arm 1's code, and the reverse (Lemma G2).
- **function `code_pair`** [L171-173]: `def code_pair(Y, alpha, w32, L_B) -> np.ndarray`
- **function `code_phase`** [L176-179]: `def code_phase(Y, alpha, w32, L_B) -> tuple` - Phase and modulus of the centred first-harmonic code pair (first two coordinates).
- **function `zero_code_threshold`** [L182-185]: `def zero_code_threshold(mod_fit) -> float` - 1e-12 x the inverted_cdf median of the FIT modulus (per model and family; NEW-3).
- **function `r1`** [L189-214]: `def r1(phi_c_p, phi_c_m, mod_p, mod_m, m32_p, m32_m, thr_code) -> dict` - The zero overrides on c1_gates.v1's inputs (before its median and agreement), then v1
- **function `n2_fit`** [L218-235]: `def n2_fit(a2_fit, w32_fit) -> dict` - FIT class means, Sigma_2w = Ledoit-Wolf of the class-centred states, W = Sigma^-1/2,
- **function `dm`** [L238-240]: `def dm(h, w32, fit) -> np.ndarray`
- **function `n2_gate`** [L243-260]: `def n2_gate(fit, w32, D2, S, C) -> dict` - F = fraction of (row, arm) states beyond q99; PASS iff F_S and F_C <= max(1/20, F_D +
- **function `_roots`** [L264-266]: `def _roots(Sigma) -> tuple`
- **function `haar_frames`** [L269-277]: `def haar_frames(j, count, p, Sigma) -> list` - P_R = Sigma^1/2 Q Q' Sigma^-1/2, Q = qr_pos of the frame stream's p x 6 normal draw.
- **function `fstar`** [L280-283]: `def fstar(m32, K) -> tuple` - Masked oracle-phase harmonics f*_K = m_valid (cos k phi*, sin k phi*) (NEW-3).
- **function `problem`** [L287-307]: `def problem(Y, w32, zt, f, euclidean=False, fit=None) -> dict` - FWL (or the given fit), Ledoit-Wolf Sigma_eps, GLS (or the Euclidean variant), the G1

