"""HWS oracle: streams, sampling, per-row arrays, nulls, P4 (API.md §3).

Protocol §2.1-§2.4 and §4.7: one HMMSampler.sample call per world-look (RC-5), suffix filters
restarted from pi (oracle_profile.suffix_posterior), D_K by k4b_scores (K4b's own definition),
gains as per-row KL values (R-HWS-5), the seven suffix-only nulls (§5.3 item 5).
"""

from __future__ import annotations  # noqa: I001  (hws_worlds sets sys.path first)

import hws_worlds as hw
import k4b_scores
import numpy as np
import oracle_profile
import scores
from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset.sampler import HMMSampler

KS_SCREEN = (1, 2, 4, 8, 16, 32)
KS_S0 = (1, 2, 3, 4, 8, 16, 32)
KS_S3 = (1, 2, 4, 6, 8, 12, 16, 24, 32)
NULL_NAMES = ("m4_phase", "sha_suffix", "orth_1", "orth_2", "orth_4", "orth_8", "orth_16")
STREAM_STAGES = ("S0", "S1", "X1", "S2", "S3", "DRY")
ORTH_KS = (1, 2, 4, 8, 16)


def history_generator(stage, key, origin=None):
    if stage == "NULLCHK":
        if origin is None:
            raise ValueError("a NULLCHK stream needs its origin stage")
        return SeedTree(0).generator("data", "hws-v1", "NULLCHK", origin, key)
    if stage not in STREAM_STAGES:
        raise ValueError(f"unknown stream stage {stage!r}")
    return SeedTree(0).generator("data", "hws-v1", stage, key)


def perm_generator(key):
    return SeedTree(0).generator("hws-v1", "prefix_perm", key)


def sample(proc, n, rng, layout=SequenceLayout()) -> np.ndarray:
    """Exactly one HMMSampler.sample call; w_last and the states are dropped at once."""
    tokens, states = HMMSampler(proc["T"], proc["E"], proc["pi"], layout).sample(int(n), rng)
    del states
    lh = layout.n_obs - 1
    out = np.ascontiguousarray(tokens[:, :lh], dtype=np.uint8)
    del tokens
    return out


def beliefs(proc, tok, Ks) -> dict:
    lh = int(np.asarray(tok).shape[1])
    return {
        int(K): oracle_profile.suffix_posterior(proc["T"], proc["E"], proc["pi"], tok, int(K))
        for K in sorted(set(int(k) for k in Ks) | {lh})
    }


def predictive(b, T, E) -> np.ndarray:
    return (b @ T) @ E


def circ_marginal(q, n_axial) -> np.ndarray:
    n = q.shape[0]
    return q.reshape(n, q.shape[1] // int(n_axial), int(n_axial)).sum(axis=2)


def x_marginal(b, W, Hh) -> np.ndarray:
    return b.reshape(b.shape[0], int(W), int(Hh)).sum(axis=2)


def kl_rows(p, q) -> np.ndarray:
    """sum_v p (log p - log q), p = 0 terms 0 (the context_gain convention, choice 9)."""
    p, q = np.asarray(p, dtype=np.float64), np.asarray(q, dtype=np.float64)
    if p.shape != q.shape or p.ndim != 2:
        raise hw.HwsStop("FAIL_TECHNICAL/NUMERICAL", f"kl_rows shapes {p.shape} vs {q.shape}")
    if not (np.all(np.isfinite(p)) and np.all(np.isfinite(q))):
        raise hw.HwsStop("FAIL_TECHNICAL/NUMERICAL", "kl_rows: non-finite input")
    support = p > 0
    if np.any(q[support] <= 0):
        raise hw.HwsStop("FAIL_TECHNICAL/NUMERICAL", "kl_rows: q = 0 where p > 0")
    terms = np.zeros_like(p)
    terms[support] = p[support] * (np.log(p[support]) - np.log(q[support]))
    return terms.sum(axis=1)


def entropy_rows(p) -> np.ndarray:
    p = np.asarray(p, dtype=np.float64)
    terms = np.zeros_like(p)
    pos = p > 0
    terms[pos] = -p[pos] * np.log(p[pos])
    return terms.sum(axis=1)


def row_arrays(proc, tok, Ks) -> dict:
    """The per-row arrays of §4.7 step 3 (API.md §3 keys; int K, erratum E3)."""
    tok = np.asarray(tok)
    lh = int(tok.shape[1])
    ks = sorted({int(k) for k in Ks if int(k) != lh})
    T, E, pi, feats = proc["T"], proc["E"], proc["pi"], proc["features"]
    W, nax = int(proc["W"]), int(proc["n_axial"])
    hh = int(pi.shape[0]) // W
    b = beliefs(proc, tok, set(ks) | ({4} if lh >= 4 else set()))
    m = {K: b[K] @ feats for K in b}
    q = {K: predictive(b[K], T, E) for K in b}
    mL, qL = m[lh], q[lh]
    phase = k4b_scores.oracle_phase(mL)
    rows = {"m": {K: m[K] for K in sorted(set(ks) | {lh})}, "D": {}, "rn": {}, "G": {}}
    for K in ks:
        rows["D"][K] = k4b_scores.phase_scores(phase, mL, m[K])
        rows["rn"][K] = scores.r4_norms(mL, m[K])
        rows["G"][K] = kl_rows(qL, q[K])
    q0 = np.broadcast_to(pi @ T @ E, qL.shape)
    rows["G0"] = kl_rows(qL, q0)
    qa = {K: circ_marginal(q[K], nax) for K in (4, lh)}
    bx = {K: x_marginal(b[K], W, hh) for K in (4, lh)}
    rows["G4A"] = kl_rows(qa[lh], qa[4])
    rows["IZ4"] = kl_rows(b[lh], b[4])
    rows["IX4"] = kl_rows(bx[lh], bx[4])
    rows["Hq"] = {K: entropy_rows(q[K]) for K in (4, lh)}
    rows["HqA"] = {K: entropy_rows(qa[K]) for K in (4, lh)}
    rows["Hb"] = {K: entropy_rows(b[K]) for K in (4, lh)}
    rows["Hbx"] = {K: entropy_rows(bx[K]) for K in (4, lh)}
    if 1 in b:
        rows["Hb1"] = entropy_rows(b[1])
    rows["m_norm"] = np.sqrt(np.sum(mL * mL, axis=1))
    rows["phase"] = phase
    nulls = {"m4_phase": k4b_scores.phase_scores(k4b_scores.m4_phase(m[4]), mL, m[4])}
    if lh == 32:
        nulls["sha_suffix"] = k4b_scores.phase_scores(k4b_scores.sha_phase(tok), mL, m[4])
    for K in ORTH_KS:
        if K in ks:
            nulls[f"orth_{K}"] = np.sum(m[K] * (mL - m[K]), axis=1)
    rows["nulls"] = nulls
    r4 = scores.r4_norms(mL, m[4])
    rows["pinsker_slack"] = 2 * rows["IX4"] - r4**2
    rows["gain_ind"] = (rows["G4A"] >= 0.005).astype(np.float64)
    rows["weak_ind"] = (rows["m_norm"] < 0.1).astype(np.float64)
    rows["m_sq"] = rows["m_norm"] ** 2
    rows["norm_err"] = float(max(np.max(np.abs(v.sum(axis=1) - 1.0)) for v in b.values()))
    return rows


def prefix_permuted(tok, rng) -> np.ndarray:
    tok = np.asarray(tok)
    lh = tok.shape[1]
    out = np.array(tok, copy=True)
    out[:, : lh - 4] = rng.permuted(tok[:, : lh - 4], axis=1)
    return out


def p4_rows(proc, tok, mL, rng) -> np.ndarray:
    perm = prefix_permuted(tok, rng)
    lh = perm.shape[1]
    mP = oracle_profile.suffix_posterior(proc["T"], proc["E"], proc["pi"], perm, lh)
    d = np.asarray(mL, dtype=np.float64) - mP @ proc["features"]
    return np.sum(d * d, axis=1)


def world_look(proc, stage, n, Ks, origin=None, layout=SequenceLayout(), p4=False) -> dict:
    rng = history_generator(stage, proc["key"], origin)
    tok = sample(proc, n, rng, layout)
    rows = row_arrays(proc, tok, Ks)
    if p4:
        rows["P4"] = p4_rows(proc, tok, rows["m"][tok.shape[1]], perm_generator(proc["key"]))
    stream = ["data", "hws-v1", stage] + ([origin] if stage == "NULLCHK" else []) + [proc["key"]]
    return {"tok": tok, "rows": rows, "stream": stream}
