# X4-F gates: public API specification for builder and independent test writer

**Authority.** This spec implements the frozen [x4f-exec-v2](X4F_EXECUTION_PROTOCOL_V2.md) (D-061) and [addendum v2](X4F_IMPLEMENTATION_PLAN_ADDENDUM_V2.md). Where they differ, the protocol governs. This document adds signatures only, never numbers.

**Conventions.**

* All analysis kernels use numpy float64 and contain no I/O.
* Errors are `topo_pilot.contracts.StageFailure` with a `topo_pilot.contracts.ErrorCode`.
* "Status" strings are returned values, not exceptions.
* Rows are histories and columns are features.
* Population covariance (1/n) is used throughout.
* A column-action map M acts on a batch as `X' = (X − μ) @ M.T + μ`.

## 1. learner (file `src/topo_pilot/learner/patch.py`, exported from `topo_pilot.learner`)

```python
@dataclass(frozen=True)
class PatchedOutput:
    logits: torch.Tensor                 # [R, L, vocab_out], float32, ALL positions
    hooks: dict[str, torch.Tensor]       # requested hooks [R, L, d_model], values AFTER the patch

def forward_with_patch(model: TransformerLM, inputs: torch.Tensor, site: str, index: int,
                       replacement: torch.Tensor, *, return_hooks: Sequence[str] = ()) -> PatchedOutput
```

**Semantics.** The same computation as `TransformerLM.forward`, except:

* **`site == f"resid_post_{k}"`, 0 ≤ k < n_layers:**
  1. x = tok_emb(inputs) + pos_emb(arange(L)).
  2. x = blocks[j](x) for j = 0..k.
  3. x[:, index, :] = replacement, on a copy.
  4. x = blocks[j](x) for j = k+1..n_layers−1.
  5. normed = ln_final(x); logits = unembed(normed).
* **`site == "ln_final_out"`:** normal forward to normed = ln_final(x); then normed[:, index, :] = replacement (on a copy); logits = unembed(normed). LayerNorm is **not** applied again.
* **Hooks.** A hook value at the patched site shows the replaced vector at `index`.
* **No side effects.** It runs under `torch.no_grad()`, never changes parameters or buffers, and never calls `.train()` or `.eval()`.

**Errors.**

| Condition | Error |
|---|---|
| `model.training` is True | `INVALID_CONFIG` |
| `inputs` is not a 2-D integer tensor; L > n_ctx; a token is outside 0..vocab_in−1 | `ALIGNMENT_ERROR` |
| `site` is not one of the two forms above (e.g. `"embed"`, `"resid_post_9"`, `"foo"`); a `return_hooks` name is unknown | `UNKNOWN_HOOK` |
| `index` is outside 0..L−1 | `ALIGNMENT_ERROR` |
| `replacement` shape ≠ [R, d_model] | `ALIGNMENT_ERROR` |
| `replacement` has non-finite entries | `NUMERICAL_FAILURE` |

**Required behaviour** (test with a tiny model: `ModelConfig(vocab_in=4, vocab_out=3, n_layers=2, d_model=16, n_heads=2, d_mlp=32)`, put in eval mode):

* **Identity:** replacement equal to the unpatched site value at `index` (from `model(inputs, return_hooks=[site])`) reproduces `model(inputs).logits` at every position within 1e-6.
* **Causality:** a non-identity replacement leaves the logits at positions < index unchanged within 1e-6, and changes the logits at `index`.
* **Final site:** at `ln_final_out`, logits equal `replacement @ unembed.weight.T` at `index`, with no second LayerNorm, using non-trivial γ ≠ 1 and β ≠ 0 set on `ln_final`.
* **Parameters:** the parameter tensors are bitwise identical before and after the call.
* **Imports:** the learner module still imports no world, process, oracle, analysis or prediction code (AST check of `patch.py`).

## 2. analysis part (g): `src/topo_pilot/analysis/x4f_*.py`, exported from `topo_pilot.analysis`

### 2.1 Targets (`x4f_targets.py`)

```python
def circle_expectation(b, x, period) -> ndarray[n, 2]
```

* Computes m = b @ [cos(2πx/period), sin(2πx/period)].
* Errors: `ALIGNMENT_ERROR` if b.shape[1] ≠ len(x); `INVALID_CONFIG` if period ≤ 0.

```python
@dataclass(frozen=True, eq=False)
class PCMap:
    mean: ndarray      # [q]
    components: ndarray  # [q, c]

def leading_components(Z_cal, n_components) -> PCMap
```

* The components are eigenvectors of the population covariance of Z_cal, in descending eigenvalue order.
* Sign convention: the entry of largest absolute value in each component is positive.
* Errors: `ALIGNMENT_ERROR` if n_components > q or n_components < 1.

```python
def pc_scores(Z, pc) -> ndarray[n, c]
```

* Computes (Z − pc.mean) @ pc.components.

### 2.2 Whitening and erasure (`x4f_erasure.py`)

**Status constants** (module-level strings): `OK = "ok"`, `FEATURES_DEGENERATE`, `TARGET_ZERO_VARIANCE`, `TARGET_UNCORRELATED`, `ERASER_INVALID`, `ZERO_DISPLACEMENT`, `RANK_EXCEEDS_RETAINED`, `FAMILY_UNMATCHED`.

```python
@dataclass(frozen=True, eq=False)
class Whitening:
    mu, U_keep, lam_keep, W, W_pinv  # [d], [d,k], [k], [k,d], [d,k]
    k: int
    status: str

def whiten(X, floor=1e-10) -> Whitening
```

* Σ = (X − μ)ᵀ(X − μ)/n, decomposed with `eigh`. Keep the eigenvalues λ_i > floor·λ_max.
* W = diag(λ_keep^{-1/2}) U_keepᵀ and W_pinv = U_keep diag(λ_keep^{1/2}).
* If λ_max ≤ 1e-12 or k = 0, the status is FEATURES_DEGENERATE with k = 0, and the arrays have shapes [d,0], [0], [0,d], [d,0].

```python
def apply_map(X, mu, M) -> ndarray      # (X − mu) @ M.T + mu
def eraser_from_basis(wh, Q_s) -> tuple[E, M]
```

* `eraser_from_basis`: Q_s [k, r] has orthonormal columns. E = W_pinv @ Q_s @ Q_s.T @ W and M = I − E.

```python
@dataclass(frozen=True, eq=False)
class Eraser:
    M, E, mu      # [d,d], [d,d], [d]
    rank: int
    status: str
    checks: dict  # keys: rho_max, idempotence, rank_loss, exactness_ratio, discarded_residual

def fit_oblique_eraser(X_cal, Z_cal, wh, rank_tol=1e-8, exact_tol=1e-8, idem_tol=1e-10) -> Eraser
```

Steps:

1. If `wh.status` ≠ ok, the status is that same status.
2. If trace Cov(Z) ≤ 1e-12: TARGET_ZERO_VARIANCE.
3. G = W Σ_xz, and ρ_max = σ_max(G) / sqrt(trace Cov(Z)). If ρ_max ≤ 1e-8: TARGET_UNCORRELATED.
4. r = #{σ > rank_tol·σ_max(G)}. Q_r = the r leading left singular vectors of G. E and M come from `eraser_from_basis`.

Checks; any failure gives ERASER_INVALID:

* `idempotence` = ‖MM − M‖_max ≤ idem_tol·max(1, ‖M‖_max);
* `rank_loss` = #{σ(E) > 1e-8·σ_max(E)} must equal r;
* `exactness_ratio` = ‖Cov(X′, Z)‖_max / ‖Σ_xz‖_max ≤ exact_tol, with X′ = apply_map(X_cal, μ, M);
* `discarded_residual` = ‖(I − U_keep U_keepᵀ)Σ_xz‖_max, reported only.

For the statuses from steps 1–3, M = I, E = 0 and rank = 0. For ERASER_INVALID, the computed M, E and r are kept, so they can be reported.

```python
def displacements(X, X_prime) -> ndarray[n]     # row L2 norms of X_prime − X

@dataclass(frozen=True, eq=False)
class Family:
    status: str
    accepted_draws: list[int]
    maps: list[ndarray]
    mean_displacements: list[float]
    target_displacement: float
    n_draws: int
    n_degenerate_draws: int

def random_family(X_cal, wh, rank, target_mean_disp, rng_for, n_accept=20, max_draws=10_000, tol=0.05) -> Family
```

* `rng_for` is a callable j → np.random.Generator.
* scale = mean_i ‖x_i − μ‖.
* If target_mean_disp ≤ 1e-12·scale: ZERO_DISPLACEMENT, with no draws.
* If wh.status ≠ ok: FEATURES_DEGENERATE.
* If rank > wh.k or rank < 1: RANK_EXCEEDS_RETAINED.
* For j = 0, 1, …, max_draws − 1:
  1. G = rng_for(j).standard_normal((k, rank)).
  2. Q, R = np.linalg.qr(G). If min|diag R| ≤ 1e-12·max|diag R|, count the draw as degenerate and continue.
  3. E, M from `eraser_from_basis(wh, Q)`.
  4. D_j = mean(displacements(X_cal, apply_map(X_cal, wh.mu, M))).
  5. Accept the draw iff |D_j − D_t| ≤ tol·D_t. Stop once n_accept draws are accepted.
* Fewer than n_accept accepted: FAMILY_UNMATCHED (the accepted draws are still returned).

```python
def mismatch_report(d_target, d_other, scale) -> dict
```

* Returns keys q10, q50, q90 (of d_other), mismatch_median, mismatch_q90 and n_excluded.
* Rows with d_target ≤ 1e-12·scale are excluded from the ratio |d_other − d_target|/d_target and counted in n_excluded.

### 2.3 Scores, support and verdict (`x4f_scores.py`)

```python
def standardizer(X_fit) -> (mean[d], scale[d])
```

* The scale is the population std; std ≤ 1e-12 → scale 1.0.

```python
def r2_pooled(Y_pred, Y_val, mean_cal) -> tuple[float | None, str]
```

* R² = 1 − Σ(Y_val − Y_pred)² / Σ(Y_val − mean_cal)², summed over all entries.
* SST ≤ 1e-12·n·q gives (None, "R2_UNDEFINED_ZERO_VARIANCE"). 1-D Y is treated as q = 1.

```python
def kl_rows(P, Q) -> tuple[ndarray | None, str]
```

* KL(P_i ‖ Q_i) in nats, per row. Terms with P = 0 contribute 0.
* Any Q = 0 where P > 0 gives (None, "KL_UNDEFINED").
* A shape mismatch raises `ALIGNMENT_ERROR`.

```python
def rbf_bandwidth(X_std_cal, rng, n_sub=1024) -> tuple[float | None, str]
```

* idx = rng.choice(n, min(n_sub, n), replace=False). The bandwidth is the median Euclidean distance over pairs i < j of those rows.
* A value ≤ 1e-12 gives (None, "RBF_DEGENERATE").

```python
def rbf_map(d, n_features, ell, rng) -> (Omega[d, F], b[F])
def rbf_features(X_std, Omega, b) -> sqrt(2/F)·cos(X_std @ Omega + b)
```

* `rbf_map` draws Ω = rng.standard_normal((d, F))/ell first, then b = rng.uniform(0, 2π, F).

```python
def ledoit_wolf(X) -> (mu[d], cov[d,d])
```

* The Ledoit–Wolf (2004) shrinkage of the population covariance toward μ_tr·I.

```python
def support_report(X_cal, X_val, patched: dict[str, ndarray]) -> dict
```

* Keys: status (ok | "SUPPORT_DEGENERATE" when λ_min(LW) ≤ 1e-12·λ_max), q99_cal, frac_unpatched_val, frac (a dict per name), knn_ratio (a dict per name, or the string "RATIO_UNDEFINED").
* `knn_ratio` = median over patched rows of the mean distance to the 10 nearest calibration rows, divided by the same quantity for unpatched X_val. A zero denominator gives "RATIO_UNDEFINED".

```python
def support_gate(frac_primary, fracs_random) -> bool
```

* True iff frac_primary ≤ 0.05 and frac_primary ≤ 2·median(fracs_random). This is literal: a zero median requires frac_primary = 0.

```python
def gate_verdict(per_model: dict[int, dict[str, str]]) -> tuple[str, str]
```

* Each model maps "G1".."G5" to one of "PASS", "FAIL", "INCONCLUSIVE" or "NOT_RUN".
* Returns "FEASIBLE" iff every gate is PASS in every model.
* Returns "NOT_FEASIBLE" iff G1 is FAIL in some model.
* Otherwise returns "INCONCLUSIVE". The reason names the first gate (G1 → G5 order) and the model that is not PASS.

## 3. experiment (`src/topo_pilot/experiment/x4f_probe.py`, imported as `topo_pilot.experiment.x4f_probe`)

```python
GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0)

@dataclass(frozen=True, eq=False)
class NestedResult:
    lam: float
    r2: float | None
    r2_status: str
    pred_val: ndarray
    fold_mse: dict[float, float]

def nested_ridge(X_cal, Y_cal, panel_cal, X_val, Y_val, grid=GRID) -> NestedResult
```

1. **Inner folds.** For each distinct panel value p (sorted), fit on the rows with panel_cal ≠ p and score MSE on the rows with panel_cal = p.
   - Standardisation (`analysis.standardizer`) uses the fit rows of that fold only.
   - The ridge is an affine ridge with RidgeProbe semantics: centre on the fit rows; W = (XcᵀXc + λI)⁻¹XcᵀYc; b = ȳ − x̄W.
2. **Choose λ.** fold_mse[λ] is the mean over folds. Take the minimal value; on exact equality, the larger λ wins.
3. **Refit and score.** Standardise on all of calibration, refit with that λ, predict validation, and compute R² with `r2_pooled(pred, Y_val, Y_cal.mean(0))`.
4. **Isolation.** X_val and Y_val are never read before step 3. A test passes NaN-filled validation arrays and checks that λ is identical; r2 and pred are then NaN or undefined.

Required tests:

* predictions equal `prediction.RidgeProbe([λ])` fitted on the same standardised data, within 1e-8;
* the tie rule;
* determinism;
* the isolation test above.
