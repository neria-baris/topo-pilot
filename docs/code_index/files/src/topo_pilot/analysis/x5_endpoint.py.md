# `src/topo_pilot/analysis/x5_endpoint.py`

- Source: [src/topo_pilot/analysis/x5_endpoint.py](../../../../../../src/topo_pilot/analysis/x5_endpoint.py)
- Kind: python
- Lines: 196

## Module docstring

> X5 G1 training endpoint (x5g1-train-v3 §4–§6): grid-defined event, infinity-safe bounds,
> paired whole-curve bootstrap and the all-pair cohort rule. Pure; no I/O, no torch.

## Imports

### Internal (repo files)

- none

### External (third-party)

- `numpy` (lines 11, 12)

### Standard library

- `__future__` (lines 5)
- `collections` (lines 8)
- `dataclasses` (lines 9)
- `math` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 65, import)
- [tests/analysis/test_x5_endpoint.py](../../../tests/analysis/test_x5_endpoint.py.md) (line 21, import)
- [tests/analysis/test_x5_endpoint_bootstrap.py](../../../tests/analysis/test_x5_endpoint_bootstrap.py.md) (line 20, import)

## Top-level constants

- `DELAY`
- `GRID`
- `THRESHOLD`

## Classes and functions

- **class `GridEvent`** [L21-31] decorators: @dataclass(frozen=True) - Observed: ``tau = lower = upper = t_j``. Censored: ``tau None``, ``lower = grid[-3]``
- **class `DiffBounds`** [L35-41] decorators: @dataclass(frozen=True) - Bounds on ``Delta = tau(curved) - tau(flat)``; ``*_strict`` marks open bounds.
- **class `BootstrapResult`** [L45-53] decorators: @dataclass(frozen=True)
- **class `PairEvidence`** [L57-61] decorators: @dataclass(frozen=True)
- **function `_check_grid`** [L64-68]: `def _check_grid(grid: Sequence[int]) -> tuple[int, ...]`
- **function `pass_sequence`** [L71-76]: `def pass_sequence(ratios, threshold: float = THRESHOLD) -> NDArray[np.bool_]` - ``ratios <= threshold`` element-wise; NaN is an error.
- **function `grid_event`** [L79-91]: `def grid_event(passes: Sequence, grid: Sequence[int] = GRID) -> GridEvent` - First ``t_j`` with PASS at ``j, j+1, j+2`` (``j <= len(grid) - 3``), else censored.
- **function `difference_bounds`** [L94-98]: `def difference_bounds(curved: GridEvent, flat: GridEvent) -> DiffBounds` - ``low = Lc - Uf``, ``high = Uc - Lf``; lowers are finite, so never NaN.
- **function `ratio_curve`** [L101-108]: `def ratio_curve(regret, gc: float) -> NDArray[np.float64]` - ``regret[R, K].mean(axis=0) / gc``.
- **function `quantile_inverted_cdf`** [L111-117]: `def quantile_inverted_cdf(values, q: float) -> float` - The ``k``-th smallest value, ``k = max(1, ceil(q n - 1e-9))``; works with +-inf.
- **function `_event_from_regret`** [L120-122]: `def _event_from_regret(reg: NDArray, gc: float, grid: tuple[int, ...], threshold: float) -> GridEvent`
- **function `paired_bootstrap_endpoint`** [L125-150]: `def paired_bootstrap_endpoint(reg_curved, reg_flat, gc_curved: float, gc_flat: float, rng: np.random.Generator, n_draws: int = 2000, batch: int = 500, grid: Sequence[int] = GRID, threshold: float = THRESHOLD, guard: Callable[[str], None] | None = None) -> BootstrapResult` - One shared ``rng.integers(0, R, size=R)`` per draw, applied to whole rows of both arms.
- **function `pair_evidence`** [L153-161]: `def pair_evidence(reg_curved, reg_flat, gc_curved: float, gc_flat: float, rng: np.random.Generator, **kw) -> PairEvidence` - Point events from the full-sample curves; quantiles from the paired bootstrap.
- **function `pair_flags`** [L164-166]: `def pair_flags(ev: PairEvidence) -> tuple[bool, bool]` - ``(supported, rejected)`` for one pair (protocol §6).
- **function `cohort_verdict`** [L169-187]: `def cohort_verdict(pairs: Sequence[PairEvidence | None], failures: Sequence[str] = (), n_required: int = 3) -> tuple[str, str]` - All-pair rule; contradiction, failures, missing or failed pairs give INCONCLUSIVE.
- **function `dev_auc`** [L190-196]: `def dev_auc(ratios, grid: Sequence[int] = GRID) -> float` - Trapezoid area of the ratio curve over the actual step values.

