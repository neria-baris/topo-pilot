# `tools/c2_readout/c2_attrib.py`

- Source: [tools/c2_readout/c2_attrib.py](../../../../../tools/c2_readout/c2_attrib.py)
- Kind: python
- Lines: 369

## Module docstring

> C2 attribution (closed forms at ln_final_out/32; d = d_named, dy = y1 - y2): the A partition,
> the energies, the exact random-6-plane reference r, nu_S, the operator decomposition, psi_max,
> E|A_S| and its Cauchy-Schwarz bound, the rotation arm and s_rot, the C2-M quantities, the
> descriptive ratio intervals (seed 620518), the other §2.12 descriptives and the POST-DESC values
> (API.md §10, §19.3; C2-FROZEN-v2 §2.6, §2.8-§2.12, §5.7, §6.1).

## Imports

### Internal (repo files)

- `import c2_config` -> [tools/c2_readout/c2_config.py](c2_config.py.md) (line 16, via same directory)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](../c1prime/c1_endpoint.py.md) (line 19, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 20, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](c2_code.py.md) (line 21, via same directory)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 23, via unique basename)

### External (third-party)

- `numpy` (lines 22)
- `scipy` (lines 24)

### Standard library

- `__future__` (lines 12)
- `fractions` (lines 14)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_a_decoy_maths.py](../../tests/c2_nd/test_a_decoy_maths.py.md) (line 22, import)
- [tests/c2_nd/test_a_inference.py](../../tests/c2_nd/test_a_inference.py.md) (line 24, import)
- [tests/c2_nd/test_a_known.py](../../tests/c2_nd/test_a_known.py.md) (line 23, import)
- [tests/c2_nd/test_b_decoy_model.py](../../tests/c2_nd/test_b_decoy_model.py.md) (line 24, import)
- [tests/c2_nd/test_b_layer2.py](../../tests/c2_nd/test_b_layer2.py.md) (line 24, import)
- [tests/c2_readout/test_a_inference.py](../../tests/c2_readout/test_a_inference.py.md) (line 33, import)
- [tests/c2_readout/test_a_oracle.py](../../tests/c2_readout/test_a_oracle.py.md) (line 33, import)
- [tests/c2_readout/test_a_partition.py](../../tests/c2_readout/test_a_partition.py.md) (line 33, import)
- [tests/c2_readout/test_a_scope.py](../../tests/c2_readout/test_a_scope.py.md) (line 36, import)
- [tests/c2_readout/test_b_screens.py](../../tests/c2_readout/test_b_screens.py.md) (line 21, import)
- [tools/c2_nd/nd_attrib.py](../c2_nd/nd_attrib.py.md) (line 20, import)
- [tools/c2_readout/c2_stage_base.py](c2_stage_base.py.md) (line 20, import)
- [tools/c2_readout/c2_stage_post.py](c2_stage_post.py.md) (line 14, import)
- [tools/c2_readout/c2_stage_pre.py](c2_stage_pre.py.md) (line 19, import)
- [tools/c2_readout/c2_stage_val.py](c2_stage_val.py.md) (line 14, import)

## Top-level constants

- `C`
- `LABEL`
- `UNDEFINED`

## Classes and functions

- **function `_f`** [L30-31]: `def _f(x) -> np.ndarray`
- **function `ind`** [L34-39]: `def ind(s, E) -> np.ndarray` - Indicator form s 1_E; a non-finite s on an eligible row is FAIL_TECHNICAL/NUMERICAL.
- **function `half_dot`** [L43-46]: `def half_dot(d, v) -> np.ndarray` - 1/2 sum_v d_v v_v with the ordered C4 kernel of c1_endpoint.A_hat.
- **function `centre`** [L49-51]: `def centre(v) -> np.ndarray`
- **function `energy`** [L54-55]: `def energy(v) -> np.ndarray`
- **function `_through`** [L58-59]: `def _through(dy, P, M) -> np.ndarray`
- **function `partition`** [L62-65]: `def partition(d, M, dy, P_S, P_G) -> dict`
- **function `energies`** [L68-69]: `def energies(M, dy, P_S) -> dict`
- **function `_CM`** [L72-74]: `def _CM(M) -> np.ndarray`
- **function `random_ref`** [L77-84]: `def random_ref(M, Sigma, dy, e_full) -> dict` - r = a e_full + b tau_K w'w (Lemma RS2), tau_K = tr(C M Sigma M' C), w'w = dy' Sigma^-1 dy.
- **function `pair`** [L87-92]: `def pair(d, M, y1, y2, P_S, P_G, Sigma) -> dict` - The partition, energies and r of one arm pair under one projector problem.
- **function `null_projector`** [L96-101]: `def null_projector(M) -> np.ndarray` - J = I - V_r V_r', V_r the right singular vectors of C M at its matrix_rank (C-28).
- **function `decomposition`** [L104-112]: `def decomposition(d, M, dy, P, J) -> dict`
- **function `nu_S`** [L115-117]: `def nu_S(J, P_S, dy) -> float`
- **function `psi_max`** [L120-127]: `def psi_max(d, M, dy, E) -> float` - 1/2 (sum of the 6 largest eigenvalues of sym E[ind(dy (M'd)')]) / E[ind(A_full)].
- **function `cs_bound`** [L130-133]: `def cs_bound(d, e_S, E) -> float`
- **function `abs_mean`** [L136-137]: `def abs_mean(A_S, E) -> float`
- **function `_softmax`** [L140-143]: `def _softmax(z) -> np.ndarray`
- **function `fisher_energy`** [L146-149]: `def fisher_energy(M, dy, P_S, z_p, z_m) -> np.ndarray` - v' (diag(p) - p p') v, v = C M P_S dy, p = (softmax(z+) + softmax(z-)) / 2 (reported).
- **function `affine_readouts`** [L152-158]: `def affine_readouts(Y_fit, w32_fit, nu_fit) -> dict` - OLS affine maps on FIT natural rows from y to onehot(w32) and to nu (C-26); slopes.
- **function `readout_change`** [L161-163]: `def readout_change(R, dy, P_S, E) -> np.ndarray`
- **function `rotation_block`** [L167-173]: `def rotation_block(K, theta) -> np.ndarray` - Block k = [[cos k theta, -sin k theta], [sin k theta, cos k theta]] (frozen orientation).
- **function `y_rot`** [L176-180]: `def y_rot(Y, alpha, w32, B, L_B, theta) -> np.ndarray` - y + B (R_K(theta) - I) f-hat, f-hat = L_B (y - alpha_w): the code rotates, the rest holds.
- **function `rotation_arm`** [L183-187]: `def rotation_arm(d_rot, M, y_p, y_m, G_rot, E) -> dict`
- **function `cm_replacements`** [L191-194]: `def cm_replacements(a2_H, a2_D, P2) -> dict`
- **function `cm_quantities`** [L197-205]: `def cm_quantities(d, z, A_full) -> dict` - A_M,X and e_M,X for X in F, S, C from z[X] = (z_X+, z_X-); I_M and A_M,ctx (reported).
- **function `cm_placebo`** [L208-212]: `def cm_placebo(dR, z_nat_H, z_S_R, z_F_R) -> dict`
- **function `ln_scale_ratio`** [L215-217]: `def ln_scale_ratio(rep, a2_H, eps) -> np.ndarray` - sqrt(Var(rep) + eps) / sqrt(Var(a2(H)) + eps) per row (C-30).
- **function `ratio_intervals`** [L221-237]: `def ratio_intervals(nums, dens, pairs, seed, draws) -> dict` - One shared bootstrap_means stream over every array; per (num, den) the two-sided 95 %
- **function `desc_intervals`** [L240-242]: `def desc_intervals(nums, dens, pairs) -> dict` - The C2-M descriptive stream: PCG64(620518), 5,000 draws, 24 arrays (NEW-5).
- **function `post_desc`** [L245-252]: `def post_desc(arrays) -> dict` - Eligible-row point ratios only, labelled unlicensed (NEW-6); no bound, no category.
- **function `threshold_arrays`** [L260-264]: `def threshold_arrays(q, E, prefix='') -> dict` - Z010, Z050, Vabs, Vrand of one pair() result (x pair, E_x).
- **function `r_arrays`** [L267-275]: `def r_arrays(qx, qy, G_x, E_x, E_y, variants=None, y_name='Y1') -> dict` - The R (or S*, y_name "Y1*") stream of one model: V3x, Y1, Z010, Z050, Vabs, Vrand, NEG
- **function `m_arrays`** [L278-288]: `def m_arrays(cm, cmR, A_full, AR_full, G_x, E_x, E_y) -> dict` - The M stream of one model: V3x, Ztau, ZM010, ZM050, VM, Y2, NEG (and Y2's activity).
- **function `point_ratios`** [L291-315]: `def point_ratios(family, q, E) -> dict` - Eligible-row point estimates of a family (report.json `point`, API.md §15.2).
- **function `_ratio`** [L319-321]: `def _ratio(a, b, E) -> float`
- **function `shares`** [L324-328]: `def shares(q, E) -> dict` - psi_S, psi_Gamma, psi_rest and eta_S of one pair() result on its eligible rows.
- **function `descriptives`** [L331-369]: `def descriptives(q, d, M, P_S, P_G, J, E, frames=(), aff=None, z_pm=None, ys=None) -> dict` - nu_S, psi_max, E|A_S| and its CS bound, the operator decompositions of P_S and P_G, the

