"""Small pure validation helpers shared by the schema classes (internal)."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .errors import ErrorCode, StageFailure


def fail(owner: str, code: ErrorCode, check: str, detail: str) -> StageFailure:
    """Build a ``StageFailure`` attributed to ``contracts.<owner>``."""
    return StageFailure(code, f"contracts.{owner}", check, detail)


def require_array(owner: str, name: str, arr: object, ndim: int,
                  kinds: str = "iuf", code: ErrorCode = ErrorCode.ALIGNMENT_ERROR) -> np.ndarray:
    """Require a numpy array of the given rank whose dtype kind is in ``kinds``."""
    if not isinstance(arr, np.ndarray) or arr.ndim != ndim or arr.dtype.kind not in kinds:
        got = f"{arr.dtype} {arr.shape}" if isinstance(arr, np.ndarray) else type(arr).__name__
        raise fail(owner, code, f"{name}_shape", f"{name}: expected {ndim}-d array, got {got}")
    return arr


def require_dtype(owner: str, name: str, arr: np.ndarray, dtypes: Sequence[str]) -> None:
    """Require ``arr.dtype`` to be one of ``dtypes`` (numpy dtype names)."""
    if arr.dtype.name not in dtypes:
        raise fail(owner, ErrorCode.ALIGNMENT_ERROR, f"{name}_dtype",
                   f"{name}: dtype {arr.dtype.name} not in {list(dtypes)}")


def require_len(owner: str, name: str, arr: np.ndarray, n: int) -> None:
    """Require ``arr.shape[0] == n``."""
    if arr.shape[0] != n:
        raise fail(owner, ErrorCode.ALIGNMENT_ERROR, f"{name}_length",
                   f"{name}: expected {n} rows, got {arr.shape[0]}")


def require_finite(owner: str, name: str, arr: np.ndarray) -> None:
    """Require every entry to be finite."""
    if not np.all(np.isfinite(arr)):
        raise fail(owner, ErrorCode.NUMERICAL_FAILURE, f"{name}_finite",
                   f"{name} has non-finite entries")


def require_distribution_rows(owner: str, name: str, P: np.ndarray, tol: float,
                              code: ErrorCode = ErrorCode.NUMERICAL_FAILURE) -> None:
    """Require nonnegative finite rows summing to 1 (over the last axis, or the last two for
    3-d arrays)."""
    require_finite(owner, name, P)
    if np.any(P < 0):
        raise fail(owner, code, f"{name}_nonnegative", f"{name} has negative entries")
    sums = P.reshape(P.shape[0], -1).sum(axis=1) if P.ndim == 3 else P.sum(axis=-1)
    err = float(np.max(np.abs(sums - 1.0))) if sums.size else 0.0
    if err > tol:
        raise fail(owner, code, f"{name}_rows_sum_to_one", f"{name}: max |row sum - 1| = {err:.3e}")


def require_permutation(owner: str, name: str, perm: np.ndarray, n: int) -> None:
    """Require ``perm`` to be an integer permutation of ``0..n-1``."""
    if (not isinstance(perm, np.ndarray) or perm.ndim != 1 or perm.dtype.kind not in "iu"
            or perm.shape[0] != n or not np.array_equal(np.sort(perm), np.arange(n))):
        raise fail(owner, ErrorCode.INVALID_CONFIG, f"{name}_permutation",
                   f"{name} is not a permutation of 0..{n - 1}")


def require_unique(owner: str, name: str, values: np.ndarray, code: ErrorCode) -> None:
    """Require all entries of a 1-d array to be distinct."""
    if np.unique(values).shape[0] != values.shape[0]:
        raise fail(owner, code, f"{name}_unique", f"{name} has duplicate entries")


def require_metric_matrix(owner: str, name: str, D: np.ndarray, tol: float = 1e-9,
                          triangle: bool = True, positive: bool = False) -> None:
    """Require a finite symmetric matrix with zero diagonal, nonnegative entries and, optionally,
    the triangle inequality and strictly positive off-diagonal entries. Raises ``NON_METRIC``."""
    def bad(check: str, detail: str) -> StageFailure:
        return fail(owner, ErrorCode.NON_METRIC, f"{name}_{check}", f"{name}: {detail}")

    if D.ndim != 2 or D.shape[0] != D.shape[1]:
        raise bad("square", f"expected a square matrix, got {D.shape}")
    if not np.all(np.isfinite(D)):
        raise bad("finite", "non-finite entries")
    if np.max(np.abs(D - D.T), initial=0.0) > tol:
        raise bad("symmetric", "asymmetric")
    if np.max(np.abs(np.diag(D)), initial=0.0) > tol:
        raise bad("zero_diagonal", "nonzero diagonal")
    if np.min(D, initial=0.0) < -tol:
        raise bad("nonnegative", "negative entries")
    n = D.shape[0]
    if positive and n > 1 and np.min(D + np.eye(n) * (1.0 + np.max(D))) <= tol:
        raise bad("positive", "two distinct points at distance 0")
    if triangle:
        for k in range(n):
            if np.any(D > D[:, k : k + 1] + D[k : k + 1, :] + tol):
                raise bad("triangle", f"triangle inequality violated via point {k}")
