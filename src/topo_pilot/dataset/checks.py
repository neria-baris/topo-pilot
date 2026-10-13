"""Pure checks and the sequence-id rule."""

from __future__ import annotations

import hashlib

import numpy as np
from scipy import stats

from topo_pilot.contracts import ErrorCode, StageFailure, canonical_json

SPLIT_CODES = {"train": 1, "dev": 2, "test": 3}
MIN_FOR_CHI2 = 200
P_THRESHOLD = 1e-4


def process_code(family: str, mode: str, sigma: str, replicate: int | str) -> int:
    """First 31 bits of ``sha256(canonical_json([family, mode, sigma, replicate]))``."""
    digest = hashlib.sha256(canonical_json([family, mode, sigma, replicate]).encode()).digest()
    return int.from_bytes(digest[:4], "big") >> 1


def make_sequence_ids(code: int, split: str, n: int) -> np.ndarray:
    """``int64 = (process_code << 32) | (split_code << 28) | index`` for ``index = 0..n-1``.

    Non-negative (``code < 2**31``); unique across splits (distinct ``split_code``); needs
    ``n <= 2**28``.
    """
    if n > 1 << 28:
        raise StageFailure(ErrorCode.INVALID_CONFIG, "dataset.checks", "n_too_large", str(n))
    base = (int(code) << 32) | (SPLIT_CODES[split] << 28)
    return base + np.arange(n, dtype=np.int64)


def check_ranges(tokens: np.ndarray, states: np.ndarray, V: int, N: int) -> None:
    """Raise ``ALIGNMENT_ERROR`` if any token is >= V or any state is outside ``0..N-1``."""
    bad_tok = tokens.size > 0 and int(tokens.max()) >= V
    bad_state = states.size > 0 and (int(states.max()) >= N or int(states.min()) < 0)
    if bad_tok or bad_state:
        raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "dataset.checks", "range",
                           f"token>=V({V}) or state outside 0..{N - 1}")


def check_disjoint(**splits: np.ndarray) -> None:
    """Raise ``SPLIT_OVERLAP`` if any ``sequence_id`` occurs in more than one split."""
    names = list(splits)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if np.intersect1d(splits[a], splits[b]).size:
                raise StageFailure(ErrorCode.SPLIT_OVERLAP, "dataset.checks", "sequence_id",
                                   f"splits {a} and {b} share sequence ids")


def check_first_token(first: np.ndarray, p_w: np.ndarray, split: str) -> float | None:
    """Chi-square test of first-token counts against ``n * (pi E)``; returns the p-value.

    Cells with expected count < 5 are pooled into one. Skipped (returns ``None``) when
    ``n < 200``. Raises ``NUMERICAL_FAILURE`` (detail ``sampler_bias``) if ``p < 1e-4``.
    """
    n = int(first.shape[0])
    if n < MIN_FOR_CHI2:
        return None
    obs = np.bincount(first.astype(np.int64), minlength=p_w.shape[0]).astype(np.float64)
    exp = n * p_w / p_w.sum()
    small = exp < 5.0
    obs = np.append(obs[~small], obs[small].sum())
    exp = np.append(exp[~small], exp[small].sum())
    keep = exp > 0
    obs, exp = obs[keep], exp[keep]
    if obs.size < 2:
        return None
    p = float(stats.chisquare(obs, exp).pvalue)
    if p < P_THRESHOLD:
        raise StageFailure(ErrorCode.NUMERICAL_FAILURE, "dataset.DatasetStage",
                           "first_token_chi2", f"sampler_bias: split={split}, p={p:.3g}")
    return p
