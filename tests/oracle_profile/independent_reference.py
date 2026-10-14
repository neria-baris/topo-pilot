"""Independent numerical reference for x4_oracle_profile suffix posteriors (job 0014).

Written from ``tools/x4_oracle_profile/API.md`` section 3 only, without access to the production
module. Two structurally different exact-arithmetic computations of the same quantity:

- ``decimal_suffix_posterior``: UNNORMALISED forward summation in ``decimal`` arithmetic with a
  context precision of at least 60 significant digits;
- ``enumerate_posterior``: exhaustive summation over every state path with ``fractions.Fraction``.

Math (HMM conventions of API.md section 1). For a window ``w_1 .. w_K``:
``P(z_1 .. z_K, w_1 .. w_K) = pi(z_1) E(z_1, w_1) prod_{t=2..K} T(z_{t-1}, z_t) E(z_t, w_t)``;
exactly one emission per state, transitions only between emissions, none after the last.
The suffix posterior is ``P(z_K = s | w_1 .. w_K)``.

Shapes: ``T: [S, S]``, ``E: [S, V]``, ``pi: [S]``, ``suffix: [K]`` symbols in ``0 .. V-1``.
Raises ``ValueError`` for an impossible suffix (zero total probability) or malformed input.
numpy is used only to read inputs; nothing is imported from ``tools/`` or ``topo_pilot``.
"""

from __future__ import annotations

import itertools
from decimal import Decimal, localcontext
from fractions import Fraction
from typing import Any, Sequence

import numpy as np

MIN_DIGITS = 60
_MEAN_DIGITS = 80


def _matrix(values: Any, name: str) -> list[list[Any]]:
    """Read a 2-D input (numpy array or nested sequence) into a list of rows of scalars."""
    arr = np.asarray(values, dtype=object)
    if arr.ndim != 2 or arr.shape[0] < 1 or arr.shape[1] < 1:
        raise ValueError(f"{name} must be a non-empty 2-D array, got shape {arr.shape}")
    return [list(row) for row in arr]


def _vector(values: Any, name: str) -> list[Any]:
    """Read a 1-D input into a list of scalars."""
    arr = np.asarray(values, dtype=object)
    if arr.ndim != 1 or arr.shape[0] < 1:
        raise ValueError(f"{name} must be a non-empty 1-D array, got shape {arr.shape}")
    return list(arr)


def _check_shapes(T: list[list[Any]], E: list[list[Any]], pi: list[Any]) -> tuple[int, int]:
    """Return (S, V) after checking T [S, S], E [S, V], pi [S]."""
    n_states = len(pi)
    if len(T) != n_states or any(len(row) != n_states for row in T):
        raise ValueError("T must be [S, S] with S = len(pi)")
    if len(E) != n_states:
        raise ValueError("E must have S rows")
    return n_states, len(E[0])


def _symbols(suffix: Any, n_symbols: int) -> list[int]:
    """Read the suffix as a non-empty list of Python ints in 0 .. V-1."""
    raw = np.asarray(suffix).reshape(-1)
    if raw.shape[0] < 1:
        raise ValueError("suffix must contain at least one symbol")
    out = [int(w) for w in raw]
    if any(w < 0 or w >= n_symbols for w in out):
        raise ValueError("suffix symbol out of range")
    return out


def _as_fraction(x: Any) -> Fraction:
    """Exact conversion: Fractions and ints kept, everything else via float (exact binary value)."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, (int, np.integer)) and not isinstance(x, (bool, np.bool_)):
        return Fraction(int(x))
    return Fraction(float(x))


def _as_decimal(x: Any) -> Decimal:
    """Exact conversion Decimal(float(x)) as required by API.md section 3."""
    if isinstance(x, Decimal):
        return x
    return Decimal(float(x))


def decimal_suffix_posterior(
    T: Any, E: Any, pi: Any, suffix: Any, digits: int = MIN_DIGITS
) -> list[Decimal]:
    """Suffix posterior by unnormalised forward summation in decimal arithmetic.

    Math: ``alpha_1(i) = pi(i) E(i, w_1)``;
    ``alpha_{t+1}(j) = sum_i alpha_t(i) T(i, j) E(j, w_{t+1})``;
    ``posterior = alpha_K / sum(alpha_K)``. No intermediate normalisation.
    All inputs are converted with ``Decimal(float(x))`` (exact); every arithmetic operation runs
    in a local decimal context with precision ``digits`` (at least 60).

    Raises
    ------
    ValueError
        ``digits < 60``, malformed shapes or symbols, or an impossible suffix (zero total).
    """
    prec = int(digits)
    if prec < MIN_DIGITS:
        raise ValueError(f"digits must be >= {MIN_DIGITS}, got {digits}")
    t_rows = [[_as_decimal(x) for x in row] for row in _matrix(T, "T")]
    e_rows = [[_as_decimal(x) for x in row] for row in _matrix(E, "E")]
    pi_vec = [_as_decimal(x) for x in _vector(pi, "pi")]
    n_states, n_symbols = _check_shapes(t_rows, e_rows, pi_vec)
    symbols = _symbols(suffix, n_symbols)
    with localcontext() as ctx:
        ctx.prec = prec
        alpha = [pi_vec[i] * e_rows[i][symbols[0]] for i in range(n_states)]
        for sym in symbols[1:]:
            alpha = [
                sum((alpha[i] * t_rows[i][j] for i in range(n_states)), Decimal(0))
                * e_rows[j][sym]
                for j in range(n_states)
            ]
        total = sum(alpha, Decimal(0))
        if total == 0:
            raise ValueError("impossible suffix: zero probability under the model")
        return [a / total for a in alpha]


def decimal_circular_mean(
    posterior: Sequence[Decimal], features: Any
) -> tuple[Decimal, Decimal]:
    """Posterior circular mean ``sum_s posterior[s] * features[s]`` in decimal arithmetic.

    Shapes: ``posterior: [S]`` Decimals (floats accepted, converted exactly); ``features: [S, 2]``,
    each entry converted with ``Decimal(float(feature))`` (exact). Products and sums use an
    80-digit local context.
    """
    rows = _matrix(features, "features")
    if len(rows) != len(posterior) or any(len(row) != 2 for row in rows):
        raise ValueError("features must be [S, 2] with S = len(posterior)")
    weights = [_as_decimal(p) for p in posterior]
    with localcontext() as ctx:
        ctx.prec = _MEAN_DIGITS
        out = [
            sum((w * Decimal(float(row[k])) for w, row in zip(weights, rows)), Decimal(0))
            for k in (0, 1)
        ]
    return out[0], out[1]


def enumerate_posterior(T: Any, E: Any, pi: Any, suffix: Any) -> list[Fraction]:
    """Suffix posterior by exhaustive enumeration of all S**K state paths, in exact Fractions.

    Math: ``P(z_K = s, w_1..w_K) = sum over paths (z_1..z_K) with z_K = s of
    pi(z_1) E(z_1, w_1) prod_{t=2..K} T(z_{t-1}, z_t) E(z_t, w_t)``, then normalised over s.
    Inputs given as Fractions are used as they are; floats are converted exactly.
    Only for tiny S and K (cost S**K paths).

    Raises
    ------
    ValueError
        Malformed shapes or symbols, or an impossible suffix (zero total probability).
    """
    t_rows = [[_as_fraction(x) for x in row] for row in _matrix(T, "T")]
    e_rows = [[_as_fraction(x) for x in row] for row in _matrix(E, "E")]
    pi_vec = [_as_fraction(x) for x in _vector(pi, "pi")]
    n_states, n_symbols = _check_shapes(t_rows, e_rows, pi_vec)
    symbols = _symbols(suffix, n_symbols)
    joint = [Fraction(0)] * n_states
    for path in itertools.product(range(n_states), repeat=len(symbols)):
        prob = pi_vec[path[0]] * e_rows[path[0]][symbols[0]]
        for t in range(1, len(symbols)):
            if prob == 0:
                break
            prob *= t_rows[path[t - 1]][path[t]] * e_rows[path[t]][symbols[t]]
        joint[path[-1]] += prob
    total = sum(joint, Fraction(0))
    if total == 0:
        raise ValueError("impossible suffix: zero probability under the model")
    return [j / total for j in joint]
