"""HWSU exact conditional prefix sampler, blocks, ids and history tables (API.md §2; protocol §2.1,
§2.8). Kernel functions keep the input dtype: object arrays of Fraction give exact results."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import numpy as np

import k4b_data
import topo_pilot.dataset.checks as checks
import topo_pilot.dataset.sampler as sampler
from c1_records import C1GateFailure
from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset.sampler import HMMSampler

SAMPLER = "FAIL_TECHNICAL/SAMPLER"


def _flat(x):
    return list(np.asarray(x, dtype=object).ravel())


def stationarity_error(T, pi) -> float:
    d = np.asarray(pi) @ np.asarray(T) - np.asarray(pi)
    return float(max(abs(x) for x in _flat(d)))


def check_process(T, E, pi) -> None:
    T, E, pi = (np.asarray(a) for a in (T, E, pi))
    n = pi.shape[0]
    if T.shape != (n, n) or E.ndim != 2 or E.shape[0] != n:
        raise C1GateFailure(SAMPLER, f"shapes T {T.shape}, E {E.shape}, pi {pi.shape}")
    if not all(x > 0 for x in _flat(pi)):
        raise C1GateFailure(SAMPLER, "pi has a non-positive entry")
    err = stationarity_error(T, pi)
    if not err <= 1e-12:
        raise C1GateFailure(SAMPLER, f"stationarity error {err!r} > 1e-12")


def time_reversal(T, pi):
    T, pi = np.asarray(T), np.asarray(pi)
    return (pi[None, :] * T.T) / pi[:, None]


def backward_messages(T, E, tokens, suffix_len=4):
    T, E, tok = np.asarray(T), np.asarray(E), np.asarray(tokens).astype(np.int64)
    n, length = tok.shape
    if length < suffix_len + 1:
        raise ValueError("tokens too short for the suffix")
    beta = np.ones((n, T.shape[0]), dtype=E.dtype)
    for t in range(length - 1, length - suffix_len - 1, -1):
        beta = (E[:, tok[:, t]].T * beta) @ T.T
    return beta


def bridge(pi, beta):
    w = np.asarray(pi)[None, :] * np.asarray(beta)
    s = w.sum(axis=1, keepdims=True)
    flat = _flat(s)
    if any(x == 0 for x in flat) or (s.dtype != object and not np.all(np.isfinite(s))):
        raise C1GateFailure(SAMPLER, "impossible suffix")
    return w / s


def prefix_kernels(T, E, pi, suffix_row, prefix_len) -> dict:
    row = np.array([0] * int(prefix_len) + list(suffix_row), dtype=np.int64)[None, :]
    beta = backward_messages(T, E, row, suffix_len=len(suffix_row))[0]
    return {"beta": beta, "bridge": bridge(pi, beta[None])[0], "T_rev": time_reversal(T, pi),
            "E": np.asarray(E)}


def sample_prefix(T, E, pi, arm1, rng, suffix_len=4):
    T, E, pi = (np.asarray(a, dtype=np.float64) for a in (T, E, pi))
    check_process(T, E, pi)
    arm1 = np.asarray(arm1)
    n, length = arm1.shape
    p = length - suffix_len
    B = bridge(pi, backward_messages(T, E, arm1, suffix_len))
    cum_e, cum_r = sampler._cumulative_rows(E), sampler._cumulative_rows(time_reversal(T, pi))
    arm2 = np.array(arm1, copy=True)
    z = sampler._draw(sampler._cumulative_rows(B), np.arange(n), rng.random(n))
    for t in range(p, 0, -1):
        arm2[:, t - 1] = sampler._draw(cum_e, z, rng.random(n))
        if t > 1:
            z = sampler._draw(cum_r, z, rng.random(n))
    arm2[:, p:] = arm1[:, p:]
    return arm2


def suffix_equal(arm1, arm2, suffix_len=4):
    a, b = np.asarray(arm1), np.asarray(arm2)
    return np.all(a[:, -suffix_len:] == b[:, -suffix_len:], axis=1)


# ----------------------------------------------------------------------- streams, ids, blocks
def generator(scope, split, block, process=None):
    return SeedTree(0).generator("data", scope, split, int(block), *(process or uc.PROC))


def seq_ids(scope, split, block, arm, n, process=None):
    if arm not in ("s", "a1", "a2"):
        raise ValueError(f"unknown arm {arm!r}")
    code = checks.process_code(*(process or uc.PROC), f"{scope}/{split}/b{int(block)}/{arm}")
    return checks.make_sequence_ids(code, "test", int(n))


def _singles(T, E, pi, scope, split, block, n, arm, process):
    tokens, states = HMMSampler(T, E, pi, SequenceLayout()).sample(
        int(n), generator(scope, split, block, process))
    canon32 = np.asarray(tokens[:, :32], dtype=np.uint8)
    del tokens, states
    ids = seq_ids(scope, split, block, arm, n, process)
    order = np.argsort(ids, kind="stable")
    return np.ascontiguousarray(canon32[order]), np.ascontiguousarray(ids[order])


def sample_singles(T, E, pi, scope, split, block, n, process=None) -> dict:
    canon32, ids = _singles(T, E, pi, scope, split, block, n, "s", process)
    return {"canon32": canon32, "ids": ids}


def sample_pairs(T, E, pi, scope, split, block, n, process=None) -> dict:
    a1, ids1 = _singles(T, E, pi, scope, split, block, n, "a1", process)
    a2 = sample_prefix(T, E, pi, a1, generator(scope, split + "/cf", block, process))
    return {"a1": a1, "a2": a2, "ids_a1": ids1,
            "ids_a2": seq_ids(scope, split, block, "a2", n, process)}


def history_table(canon32, ids, label, block) -> dict:
    if label not in ("of-fit", "of-eval-a1", "of-eval-a2"):
        raise ValueError(f"unknown label {label!r}")
    return k4b_data.history_table(canon32, ids, label, block)


def table_arrays(table) -> dict:
    return {k: table[k] for k in ("canon32", "seq_ids", "digest", "landmark", "ref_row",
                                  "decoder_panel")}


def hist_name(kind, block, dry=False) -> str:
    if kind not in ("fit", "eval_a1", "eval_a2"):
        raise ValueError(f"unknown kind {kind!r}")
    return f"{'DRYHIST' if dry else 'HIST'}_OF_{kind}_b{block}.npz"
