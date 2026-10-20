"""X6S1 eval: the predictor interface (float64 model wrapper, exact oracle and reference wrappers),
the quantised readout, scoring, cue mass, pair terms, designed statistics and the E3.A chunk outputs
(X6S1-FROZEN-v1 §2.2-§2.8, §7.4; API.md §7). Import performs no I/O."""
# fmt: off

from __future__ import annotations

import copy
import io
import json
import math
import sys
from dataclasses import asdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
_EXTRA = [REPO / p for p in ("tools/x6_stage1", "tools/x6_stage0", "tools/x4_oracle_profile",
                             "tools/d2a", "tools/k4b", "tools/c1prime_registry",
                             "tests/oracle_profile")]
sys.path[:0] = [str(p) for p in _EXTRA if str(p) not in sys.path]
import numpy as np  # noqa: E402
import torch  # noqa: E402
import x6_exact as xe  # noqa: E402
import x6_model as xm  # noqa: E402
import x6s1_cloud as sc  # noqa: E402
import x6s1_data as sd  # noqa: E402
import x6s1_pairs as sp  # noqa: E402
import x6s1_stats as ss  # noqa: E402

from topo_pilot.contracts import Checkpoint, canonical_json  # noqa: E402
from topo_pilot.learner.stage import load_model  # noqa: E402

BOS = 18
ORACLE_KINDS = ("qstar", "q_empty", "q_parity", "q_counts", "q_H1", "q_Parikh", "q_8", "h_last",
                "h_first", "h_rev")
PROFILE_T = (16, 24)


def set_threads() -> None:
    import d2a_train
    if (torch.get_num_threads(), torch.get_num_interop_threads()) != (2, 1):
        d2a_train._set_threads()
    assert (torch.get_num_threads(), torch.get_num_interop_threads()) == (2, 1)
    assert sd.THREADS == {"intra": 2, "interop": 1} == d2a_train.THREADS


def pad(histories, n_obs=33) -> np.ndarray:
    out = np.zeros((len(histories), n_obs), np.uint8)
    for i, h in enumerate(histories):
        out[i, :len(h)] = h
    return out


def model_inputs(tokens) -> torch.Tensor:
    tok = np.asarray(tokens)
    x = np.concatenate([np.full((len(tok), 1), BOS, np.int64), tok[:, :32].astype(np.int64)], 1)
    return torch.from_numpy(np.ascontiguousarray(x))


def _ts(t, n) -> np.ndarray:
    return np.broadcast_to(np.asarray(t, np.int64), (n,)).copy()


class ModelPredictor:
    """The float64 CPU evaluation of a model's verified float32 weights (§2.2)."""

    def __init__(self, ckpt_path, file_sha256, weights_sha256):
        data = Path(ckpt_path).read_bytes()
        if sc.sha256_bytes(data).lower() != str(file_sha256).lower():
            raise ValueError(f"checkpoint file sha256 mismatch: {ckpt_path}")
        obj = torch.load(io.BytesIO(data), map_location="cpu", weights_only=True)
        sd_ = obj["model"]
        if sc.weights_digest(sd_) != str(weights_sha256).lower():
            raise ValueError(f"weights digest mismatch: {ckpt_path}")
        self._build(sd_, Path(ckpt_path).parent.parent.name, int(obj.get("step", 0)))

    @classmethod
    def from_state(cls, sd_, name) -> ModelPredictor:
        self = cls.__new__(cls)
        self._build(sd_, name, 0)
        return self

    def _build(self, sd_, name, step) -> None:
        buf = io.BytesIO()
        torch.save({"model": sd_}, buf)
        ck = Checkpoint(run_id=str(name), step=step, observation_id="x6s1", state=buf.getvalue(),
                        model_config=asdict(sd.MODEL_CFG))
        self.name, self.step, self.m32 = str(name), step, None
        self.model = load_model(ck).double().eval()

    def __call__(self, tokens, t) -> np.ndarray:
        return self._run(self.model, tokens, t)

    def float32(self, tokens, t) -> np.ndarray:
        """The same readout from a float32 copy (the weights are float32, so the copy is exact):
        the §2.8 float32-versus-float64 difference (R-0082-2)."""
        if self.m32 is None:
            self.m32 = copy.deepcopy(self.model).float().eval()
        return self._run(self.m32, tokens, t)

    @staticmethod
    def _run(model, tokens, t) -> np.ndarray:
        tok = np.asarray(tokens)
        ts, out = _ts(t, len(tok)), np.empty((len(tok), 18), np.float64)
        with torch.no_grad():
            for a in range(0, len(tok), sd.EVAL_BATCH):
                b = min(a + sd.EVAL_BATCH, len(tok))
                lg = model(model_inputs(tok[a:b])).logits
                row = lg[torch.arange(b - a), torch.from_numpy(ts[a:b])]
                out[a:b] = torch.softmax(row, -1).numpy()
        return out


def _law(arm, kind, h, t):
    if kind == "qstar":
        return sp.q_exact(arm, h, t)
    if arm != "NA":
        raise ValueError(f"reference {kind} is defined on the NA arm only")
    if kind == "q_8":
        return sp.q_window(h, t, 8)
    if kind.startswith("h_"):
        return sp.q_heuristic(kind[2:], h, t)
    return sp.q_stat(kind[2:], h, t)


class OraclePredictor:
    def __init__(self, arm, kind):
        if kind not in ORACLE_KINDS:
            raise ValueError(f"unknown oracle kind {kind}")
        self.arm, self.kind, self.name = arm, kind, kind

    def __call__(self, tokens, t) -> np.ndarray:
        tok = np.asarray(tokens)
        ts = _ts(t, len(tok))
        return np.array([[float(x) for x in _law(self.arm, self.kind, r, int(k))]
                         for r, k in zip(tok, ts)], np.float64).reshape(len(tok), 18)


@lru_cache(maxsize=None)
def _qcode() -> dict:
    return {v: i for i, v in enumerate(ss.qvals())}


def qstar(arm, tokens, t) -> tuple:
    tok, code = np.asarray(tokens), _qcode()
    ts = _ts(t, len(tok))
    q, codes = np.empty((len(tok), 18), np.float64), np.empty((len(tok), 18), np.int16)
    for i, (r, k) in enumerate(zip(tok, ts)):
        law = sp.q_exact(arm, r, int(k))
        q[i], codes[i] = [float(x) for x in law], [code[Fraction(x)] for x in law]
    return q, codes


class QuantInvalid(ValueError):
    pass


def quantise(s) -> np.ndarray:
    """§2.2 steps 1-3 (T13, T25): Q = 2**20, the R largest fractional parts get +1, ties by the
    lower token index."""
    s = np.asarray(s, np.float64)
    if not np.isfinite(s).all() or (s < 0).any() or (np.abs(s.sum(1) - 1) > sd.SUM_TOL).any():
        raise QuantInvalid("readout precondition failed (sum, sign or finiteness)")
    r = s * sd.Q
    f = np.floor(r)
    R = sd.Q - f.sum(1).astype(np.int64)
    if (R < 0).any() or (R > 18).any():
        raise QuantInvalid("remainder outside 0..18")
    k = f.astype(np.int64)
    order = np.argsort(-(r - f), axis=1, kind="stable")
    rank = np.empty_like(order)
    np.put_along_axis(rank, order, np.arange(18)[None].repeat(len(s), 0), axis=1)
    return k + (rank < R[:, None])


def readout_exact(k_row) -> tuple:
    return tuple((1 - sd.EPS) * Fraction(int(x), sd.Q) + sd.EPS / 18 for x in k_row)


def readout(k) -> np.ndarray:
    return np.array([[float(x) for x in readout_exact(r)] for r in np.asarray(k)], np.float64)


def score(codes, k, tables) -> np.ndarray:
    """x_hat_i = sum_j (q ln q)[code] - fl(q)[code] * ln p^Q[k] (§7.4 item 3)."""
    codes, k = np.asarray(codes, np.int64), np.asarray(k, np.int64)
    terms = tables["qlnq"][codes] - tables["fl_q"][codes] * tables["lnp"][k]
    return np.array([math.fsum(r) for r in terms], np.float64)


def kl_rows(q, p) -> np.ndarray:
    q, p = np.asarray(q, np.float64), np.asarray(p, np.float64)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(q > 0, q * (np.log(q) - np.log(p)), 0.0)
    return np.array([math.fsum(r) for r in t], np.float64)


def cue_mass(p) -> np.ndarray:
    return np.asarray(p, np.float64)[:, 15:18].sum(1)


def cue_normalise(p) -> np.ndarray:
    c = np.asarray(p, np.float64)[:, 15:18]
    m = c.sum(1)
    ok = np.isfinite(m) & (m > 0)
    out = np.full(c.shape, np.nan)
    out[ok] = c[ok] / m[ok, None]
    return out


def pair_terms(ph, ph2, qh, qh2) -> tuple:
    dp = cue_normalise(ph) - cue_normalise(ph2)
    dq = cue_normalise(qh) - cue_normalise(qh2)
    return (dp * dq).sum(1), (dq * dq).sum(1)


def beta_fsum(num, den) -> float:
    d = math.fsum(np.asarray(den, np.float64))
    return math.fsum(np.asarray(num, np.float64)) / d if d else math.nan


def beta_exact(num, den, informative=None) -> Fraction:
    """x6_exact.beta with pair i as a two-member set of weight den_i, oracle cue difference e_0
    and predictor difference (num_i / den_i) e_0: centring halves num and den alike (E3.5)."""
    rows = []
    for i, (a, b) in enumerate(zip(np.asarray(num, np.float64), np.asarray(den, np.float64))):
        if b > 0 and (informative is None or informative[i]):
            a, b = Fraction(float(a)), Fraction(float(b))
            z, e = (Fraction(0),) * 3, (Fraction(1), Fraction(0), Fraction(0))
            rows += [(i, b, e, (a / b, 0, 0)), (i, b, z, z)]
    return xe.beta(rows)


# ---- designed statistics (§2.5; T17) ----
def _fam(A, fam, pred, qstar_fn, tables) -> dict:
    out = {}
    for m in ("a", "b"):
        if f"{fam}_{m}" in A:
            tok, t = A[f"{fam}_{m}"], A[f"{fam}_t"].astype(np.int64)
            p = pred(tok, t)
            q, codes = qstar_fn(tok, t)
            out[m] = {"p": p, "q": q, "codes": codes, "tok": tok, "t": t}
    return out


def _xhat(r, tables) -> np.ndarray:
    return score(r["codes"], quantise(r["p"]), tables)


def _mean(x) -> float:
    return math.fsum(np.asarray(x, np.float64)) / len(x)


def _set_beta(tok, t, p, q, balanced=False) -> float:
    """beta over sets (x6_exact.beta semantics in float64): a set is the histories sharing w_{1:s}
    (prefix and cue); balanced weights identity-holonomy members 1/4 (x6_exact.beta_table)."""
    sets, lab = {}, xm.edge_labels("NA")
    for i, (r, k) in enumerate(zip(tok, t)):
        pr = xm.parse(r[:k])
        w = 0.25 if balanced and xm.holonomy(pr["segment"], lab) == xm.S3_E else 1.0
        sets.setdefault(tuple(int(x) for x in r[:pr["s"]]), []).append((i, w))
    cp, cq, num, den = cue_normalise(p), cue_normalise(q), [], []
    for items in sets.values():
        idx, w = np.array([i for i, _ in items]), np.array([w for _, w in items])
        mp, mq = (w[:, None] * cp[idx]).sum(0) / w.sum(), (w[:, None] * cq[idx]).sum(0) / w.sum()
        num += list(w * ((cp[idx] - mp) * (cq[idx] - mq)).sum(1))
        den += list(w * ((cq[idx] - mq) ** 2).sum(1))
    return beta_fsum(num, den)


def designed_stats(pred, D_arrays, qstar_fn, tables) -> dict:
    A, out, masses, finite = D_arrays, {}, [], True
    fams = {f: _fam(A, f, pred, qstar_fn, tables) for f in sp.PAIR_FAMILIES + ("W3", "W3p")}
    for f, r in fams.items():
        for m in r.values():
            masses.append(cue_mass(m["p"]))
            finite &= bool(np.isfinite(m["p"]).all())
    w2 = fams["W2"]
    num, den = pair_terms(w2["a"]["p"], w2["b"]["p"], w2["a"]["q"], w2["b"]["q"])
    y = A["W2_y"]
    out["beta_W2"] = beta_fsum(num, den)
    out["beta_W2_y"] = [beta_fsum(num[y == z], den[y == z]) for z in range(3)]
    out["R_W2"] = _mean(np.concatenate([_xhat(w2["a"], tables), _xhat(w2["b"], tables)]))
    out["Delta_W3"] = _mean(_xhat(fams["W3"]["a"], tables))
    dq2 = (cue_normalise(w2["a"]["q"]) - cue_normalise(w2["b"]["q"])) ** 2
    denom = _mean(dq2.sum(1))
    ctrl = np.concatenate([((cue_normalise(fams[c]["a"]["p"]) - cue_normalise(fams[c]["b"]["p"]))
                            ** 2).sum(1) for c in ("C1", "C2", "C3", "C4")])
    out["rho_C"] = _mean(ctrl) / denom
    out["rho_W2"] = _mean(((cue_normalise(w2["a"]["p"]) - cue_normalise(w2["b"]["p"])) ** 2)
                          .sum(1)) / denom
    out["cue_mass_median"] = float(np.median(np.concatenate(masses)))
    w1 = fams["W1"]
    out["beta_W1"] = beta_fsum(*pair_terms(w1["a"]["p"], w1["b"]["p"], w1["a"]["q"], w1["b"]["q"]))
    for f, key, bal in (("W3", "beta_W3", False), ("W3", "beta_W3_bal", True),
                        ("W3p", "beta_W3p", False)):
        r = fams[f]["a"]
        out[key] = _set_beta(r["tok"], r["t"], r["p"], r["q"], bal)
    out["nonfinite"] = not finite or not all(
        math.isfinite(v) for k, v in out.items() if k in ("beta_W2", "R_W2", "rho_C"))
    return out


def natural_pairs(pred, test_tokens, partner_tokens, rows, t=32) -> dict:
    h = np.asarray(test_tokens)[np.asarray(rows, np.int64)]
    ph, ph2 = pred(h, t), pred(partner_tokens, t)
    qh, qh2 = qstar("NA", h, t)[0], qstar("NA", partner_tokens, t)[0]
    num, den = pair_terms(ph, ph2, qh, qh2)
    return {"rows": np.asarray(rows, np.int64), "num": num, "den": den,
            "cue_mass_h": cue_mass(ph), "cue_mass_h2": cue_mass(ph2), "p_h": ph, "p_h2": ph2,
            "nonfinite": not (np.isfinite(ph).all() and np.isfinite(ph2).all())}


def own_arm(pred, arm, tokens, tables, t=32, p=None) -> dict:
    p = pred(tokens, t) if p is None else p  # p: the readout of `tokens` if already computed
    q, codes = qstar(arm, tokens, t)
    return {"xhat": score(codes, quantise(p), tables), "raw_kl": kl_rows(q, p),
            "cue_mass": cue_mass(p)}


def own_pairs(pred, tokens, partner_tokens, rows, t=32, p_h=None) -> dict:
    """§2.8 abelian own-process spread (R-0082-2): per own-process R_ord(t) pair, the within-
    Parikh-class spread ||Δp̂_c||² of the cue-normalised readouts (the own oracle's is exactly 0:
    an abelian q* is a function of the Parikh class)."""
    h = np.asarray(tokens)[np.asarray(rows, np.int64)]
    ph, ph2 = pred(h, t) if p_h is None else p_h, pred(partner_tokens, t)
    dp = cue_normalise(ph) - cue_normalise(ph2)
    return {"rows": np.asarray(rows, np.int64), "spread": (dp * dp).sum(1),
            "nonfinite": not (np.isfinite(ph).all() and np.isfinite(ph2).all())}


def float32_diff(pred, tokens, t=32) -> dict:
    """§2.8 raw values (R-0082-2): a float32 forward next to the float64 one on the same rows;
    the maximum absolute readout difference and the raw full-vocabulary log-loss of each."""
    p64, p32 = pred(tokens, t), pred.float32(tokens, t)
    q = qstar("NA", tokens, t)[0]
    k64, k32 = _mean(kl_rows(q, p64)), _mean(kl_rows(q, p32))
    return {"rows": len(p64), "max_abs": float(np.max(np.abs(p32 - p64))), "raw_kl_f64": k64,
            "raw_kl_f32": k32, "raw_kl_diff": k32 - k64}


def _cue_rows(x, cue, name) -> np.ndarray:
    """Cue-normalised rows of a reference law where q* has cue mass; undefined there raises."""
    c = cue_normalise(np.asarray(x)[cue])
    if not np.isfinite(c).all():
        raise ValueError(f"gamma: {name} has no cue mass on a row where q* has (R-0081-1)")
    return c


def gamma(pred, val_tokens, t=32) -> dict:
    """gamma_m (§2.8; descriptive; R-0081-1): beta = sum<p_c - q_Parikh,c, d> / sum ||d||^2 with
    d = q*_c - q_Parikh,c over all val(NA) rows; a row where q* has no cue mass has d = 0 and
    contributes 0 to both sums. Other undefined cases raise, except the predictor's own zero cue
    mass: beta_m and gamma are then None, undefined (canonical JSON; "p_undefined" rows, §2.6)."""
    q, qp = qstar("NA", val_tokens, t)[0], OraclePredictor("NA", "q_Parikh")(val_tokens, t)
    q8, p = OraclePredictor("NA", "q_8")(val_tokens, t), pred(val_tokens, t)
    cue = cue_mass(q) > 0
    c0 = _cue_rows(qp, cue, "q_Parikh")
    d = _cue_rows(q, cue, "q*") - c0
    dd = math.fsum((d * d).sum(1))
    if not dd > 0:
        raise ValueError("gamma: sum ||d||^2 = 0 on val(NA)")
    def beta(c): return math.fsum(((c - c0) * d).sum(1)) / dd
    cp = cue_normalise(np.asarray(p)[cue])
    b_m, b_8 = beta(cp) if np.isfinite(cp).all() else None, beta(_cue_rows(q8, cue, "q_8"))
    if b_8 == 1:
        raise ValueError("gamma: beta_8 = 1")
    g = None if b_m is None else (b_m - b_8) / (1 - b_8)
    return {"beta_m": b_m, "beta_8": b_8, "gamma": g, "d2_mean": dd / len(q),
            "rows": int(cue.sum()), "p_undefined": int((~np.isfinite(cp).all(1)).sum())}


# ---- E3.A chunk (§13.3; API.md §13 item 21) ----
def _predictor(name, spec):
    if spec.get("state") is not None:
        return ModelPredictor.from_state(spec["state"], name)
    return ModelPredictor(spec["ckpt_path"], spec["file_sha256"], spec["weights_sha256"])


def _excl(path: Path, data: bytes) -> str:
    with open(path, "xb") as fh:
        fh.write(data)
    return sc.sha256_bytes(data)


def _npz(path: Path, arrays: dict) -> str:
    buf = io.BytesIO()
    np.savez(buf, **arrays)
    return _excl(path, buf.getvalue())


def _clean(v):  # canonical JSON refuses NaN and inf: a non-finite float is recorded as None
    if isinstance(v, dict):
        return {k: _clean(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_clean(x) for x in v]
    return (float(v) if math.isfinite(v) else None) if isinstance(v, (float, np.floating)) else v


def _json(path: Path, obj) -> str:  # non-finite values are written as null (R-0082-5)
    return _excl(path, canonical_json(_clean(obj)).encode("utf-8"))


def eval_chunk(name, plan, out_dir) -> dict:
    set_threads()
    d = Path(out_dir) / name
    d.mkdir(parents=True, exist_ok=False)
    pred, tab, files = _predictor(name, plan["predictor"]), plan["tables"], {}
    own_tok, orows = plan["own_tokens"], plan.get("own_rows")
    p_own = pred(own_tok, 32)
    files["own.npz"] = _npz(d / "own.npz", own_arm(pred, plan["arm"], own_tok, tab, p=p_own))
    if orows is not None:  # AB/ZC: the own-process pairs (§2.8; R-0082-2)
        o = own_pairs(pred, own_tok, plan["own_partner_tokens"], orows,
                      p_h=p_own[np.asarray(orows, np.int64)])
        files["own_pairs.npz"] = _npz(d / "own_pairs.npz", {k: o[k] for k in ("rows", "spread")})
    del p_own
    files["float32.json"] = _json(d / "float32.json", float32_diff(
        pred, np.asarray(plan["test_tokens"])[:sd.N_DET]))  # the E3.1 (DET) rows, t = 32
    pr = natural_pairs(pred, plan["test_tokens"], plan["partner_tokens"], plan["rows"])
    files["pairs.npz"] = _npz(d / "pairs.npz", {k: v for k, v in pr.items() if k != "nonfinite"})
    des = designed_stats(pred, plan["designed"], lambda tk, t: qstar("NA", tk, t), tab)
    files["designed.json"] = _json(d / "designed.json", des)
    if name.startswith("NA-"):
        prof = {}
        for t, part in plan.get("profile", {}).items():
            q = natural_pairs(pred, plan["test_tokens"], part["partner_tokens"], part["rows"], t)
            o = own_arm(pred, "NA", np.asarray(plan["test_tokens"])[:part["n_rows"]], tab, t)
            prof |= {f"num_t{t}": q["num"], f"den_t{t}": q["den"], f"rows_t{t}": q["rows"],
                     f"xhat_t{t}": o["xhat"]}
        files["profile.npz"] = _npz(d / "profile.npz", prof)
        em, n = {}, plan.get("emergence_rows", sd.N_EMERGE)
        sel = np.asarray(plan["rows"]) < n  # the pairs among the first 2**14 rows (R-0082-3)
        for step, spec in sorted(plan.get("emergence", {}).items()):
            ep = _predictor(name, spec)
            q = natural_pairs(ep, plan["test_tokens"], np.asarray(plan["partner_tokens"])[sel],
                              np.asarray(plan["rows"])[sel])
            em[str(step)] = {"beta_ord": beta_fsum(q["num"], q["den"]), "pairs": int(sel.sum()),
                             "delta_nat": _mean(own_arm(ep, "NA", plan["own_tokens"][:n],
                                                        tab)["xhat"])}
        files["emergence.json"] = _json(d / "emergence.json", em)
        files["gamma.json"] = _json(d / "gamma.json", gamma(pred, plan["val_tokens"]))
    chunk = {"name": name, "files": files, "env_local": plan.get("env_local"),
             "nonfinite": bool(pr["nonfinite"] or des["nonfinite"])}
    _json(d / "chunk.json", chunk)
    return json.loads(canonical_json(chunk))
