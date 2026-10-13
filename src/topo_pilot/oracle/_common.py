"""Shared validation helpers for the oracle kernels (no I/O)."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from topo_pilot.contracts import ErrorCode, StageFailure

COMPONENT = "oracle"
SUM_TOL = 1e-10


def fail(code: ErrorCode, check: str, detail: str) -> StageFailure:
    """Build a ``StageFailure`` attributed to the oracle."""
    return StageFailure(code, COMPONENT, check, detail)


def check_rows_sum_to_one(rows: NDArray[np.float64], check: str) -> None:
    """Raise ``NUMERICAL_FAILURE`` unless every last-axis sum is 1 within ``SUM_TOL``."""
    sums = rows.sum(axis=-1)
    if not np.all(np.isfinite(sums)) or np.max(np.abs(sums - 1.0)) > SUM_TOL:
        raise fail(ErrorCode.NUMERICAL_FAILURE, check, "rows do not sum to 1")


def as_model(T: np.ndarray, E: np.ndarray, pi: np.ndarray | None) -> tuple:
    """Float64 copies of ``T [N,N]``, ``E [N,V]`` and ``pi [N]`` (or ``None``), shape-checked.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` for inconsistent shapes; ``NUMERICAL_FAILURE`` for non-stochastic rows.
    """
    T_ = np.array(T, dtype=np.float64)
    E_ = np.array(E, dtype=np.float64)
    pi_ = None if pi is None else np.array(pi, dtype=np.float64)
    n = T_.shape[0] if T_.ndim == 2 else -1
    bad = T_.ndim != 2 or T_.shape != (n, n) or E_.ndim != 2 or E_.shape[0] != n
    if pi_ is not None:
        bad = bad or pi_.shape != (n,)
    if bad:
        raise fail(ErrorCode.ALIGNMENT_ERROR, "model_shapes", "T, E, pi shapes are inconsistent")
    named = [("T", T_), ("E", E_)] + ([("pi", pi_)] if pi_ is not None else [])
    for name, arr in named:
        check_rows_sum_to_one(arr, f"{name}_stochastic")
        if np.any(arr < 0):
            raise fail(ErrorCode.NUMERICAL_FAILURE, f"{name}_nonnegative", "negative entries")
    return T_, E_, pi_


def check_tokens(tokens: np.ndarray, n_symbols: int, max_len: int = 33) -> np.ndarray:
    """Return ``tokens`` as int64 ``[R, P]``; raise ``ALIGNMENT_ERROR`` if malformed.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` if not 2-D integer, ``P > max_len``, or a symbol is outside ``0..V-1``.
    """
    arr = np.asarray(tokens)
    if arr.ndim != 2 or not np.issubdtype(arr.dtype, np.integer):
        raise fail(ErrorCode.ALIGNMENT_ERROR, "tokens_shape",
                   f"expected integer [R, P], got {arr.dtype} {arr.shape}")
    if arr.shape[1] > max_len:
        raise fail(ErrorCode.ALIGNMENT_ERROR, "tokens_length", f"P={arr.shape[1]} > {max_len}")
    if arr.size and (int(arr.min()) < 0 or int(arr.max()) >= n_symbols):
        raise fail(ErrorCode.ALIGNMENT_ERROR, "tokens_vocab", f"symbol outside 0..{n_symbols - 1}")
    return arr.astype(np.int64)


def normalise_rows(unnorm: NDArray[np.float64], check: str) -> tuple:
    """Divide rows by their sums; return ``(rows, sums)``.

    Raises
    ------
    StageFailure
        ``IMPOSSIBLE_HISTORY`` if a sum is 0; ``NUMERICAL_FAILURE`` if a sum is not finite.
    """
    sums = unnorm.sum(axis=-1)
    if not np.all(np.isfinite(sums)):
        raise fail(ErrorCode.NUMERICAL_FAILURE, check, "non-finite normaliser")
    if np.any(sums <= 0.0):
        raise fail(ErrorCode.IMPOSSIBLE_HISTORY, check, "zero evidence for a history")
    return unnorm / sums[..., None], sums
