"""C2ND decoys: the head edits D-NULL, D-NULL1, D-ONLY, D-DOSE (Lemmas DC1-DC3), the null basis
V0, the move U and the map T (Lemma DC4), the coordinate wrapper and its basis adapter,
decoy_sha64 and the construction record, M0-D (§3 row 11) and DX (§3 row 20) (API.md §6, §20;
C2ND-DESIGN-v1 §2.6-§2.7).

Every dimension comes from the inputs (ND-C33). The construction projector P_S is reachable in
M0-D and DX only, which call policy.require("construction") first (ND-C26); no method statistic
is formed here. The C2 model, readout and patch functions are reused unchanged.
"""

from __future__ import annotations

import copy
import hashlib
import json
from fractions import Fraction

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c1_model
import c2_config as cc
import c2_model as cm
import numpy as np
import torch

DECOY, CONSTRUCTION = "FAIL_TECHNICAL/DECOY", "EXCLUDED/CONSTRUCTION"
NUMERICAL = "INCONCLUSIVE/NUMERICAL"
BASIS_KEYS = ("Q0", "M", "beta", "WU", "WUbeta")


def _f(x) -> np.ndarray:
    return np.asarray(x, dtype=np.float64)


def _np(t) -> np.ndarray:
    return t.detach().to(torch.float64).cpu().numpy().copy()


def _mx(x) -> float:
    x = _f(x)
    return float(np.max(np.abs(x))) if x.size else 0.0


def _le(x, tol) -> bool:
    """x <= tol (CONTRACT string) in exact rationals; a non-finite x fails."""
    return bool(np.isfinite(x)) and Fraction(float(x)) <= nc.frac(tol)


# ---- inputs and head edits (§6.1-§6.2; Lemmas DC1-DC3) ---------------------------------------
def base_inputs(c2_fit, basis) -> dict:
    """The readout basis of model64 and the frozen C2 problem R (P_S, B, L_B = R_L[5:], Gamma)."""
    out = {k: _f(basis[k]) for k in BASIS_KEYS}
    out.update(P_S=_f(c2_fit["R_P_S"]), B=_f(c2_fit["R_B"]), Gamma=_f(c2_fit["R_Gamma"]))
    out["L_B"] = _f(c2_fit["R_L"])[cc.N_NUIS :]
    return out


def pi_S(Q0, P_S) -> np.ndarray:
    return _f(Q0) @ _f(P_S) @ _f(Q0).T


def head_edit(kind, WU, Q0, P_S, g=nc.G_D, rho=nc.RHO) -> np.ndarray:
    """W'_U in exactly the CONTRACT association g * (WU @ (I - Pi_S)) (ND-C15, §20 B-8)."""
    WU, Pi = _f(WU), pi_S(Q0, P_S)
    eye = np.eye(Pi.shape[0])
    if kind == "DNULL":
        return float(g) * (WU @ (eye - Pi))
    if kind == "DNULL1":
        return WU @ (eye - Pi)
    if kind == "DONLY":
        return WU @ Pi
    if kind == "DDOSE":
        return float(g) * (WU @ (eye - float(rho) * Pi))
    raise ValueError(f"unknown head edit {kind!r}")


def _with_head(dec, W):
    old = dec.unembed.weight
    new = torch.from_numpy(np.array(W, dtype=np.float64))
    dec.unembed.weight = torch.nn.Parameter(new, requires_grad=old.requires_grad)
    return dec.eval()


def make_head_decoy(model64, W):
    """A deep copy of model64 with only unembed.weight replaced (float64)."""
    return _with_head(copy.deepcopy(model64), W)


# ---- coordinate decoys (Lemma DC4; §6.3) -----------------------------------------------------
def null_basis(M) -> np.ndarray:
    """An orthonormal basis of ker(M): right singular vectors with sv <= 1e-12 sigma_max."""
    _, s, Vt = np.linalg.svd(_f(M))
    r = int(np.count_nonzero(s > float(nc.NULL_SV_REL) * s[0])) if s.size else 0
    return Vt[r:].T


def move_map(B, L_B, M) -> dict:
    """U = V0 (L_B V0)^+, T = I + (U - B) L_B, Tinv = I + (B - U) L_B and the construction gates."""
    B, L_B = _f(B), _f(L_B)
    V0 = null_basis(M)
    eye = np.eye(B.shape[0])
    out = {"V0": V0, "U": None, "T": None, "Tinv": None, "sv": None, "rank": 0}
    out.update(cond_T=float("inf"), ok=False, status=CONSTRUCTION)
    try:
        A = L_B @ V0
        sv = np.linalg.svd(A, compute_uv=False)
        U = V0 @ np.linalg.pinv(A)
        T, Tinv = eye + (U - B) @ L_B, eye + (B - U) @ L_B
        cond = float(np.linalg.cond(T, 2))
    except (np.linalg.LinAlgError, ValueError):
        return out
    rank = int(np.count_nonzero(sv > 0))
    ratio = float(sv[-1] / sv[0]) if sv.size and sv[0] > 0 else 0.0
    sv_ok = bool(np.isfinite(ratio)) and Fraction(ratio) >= nc.U_SV_RATIO
    ok = rank == nc.U_RANK and sv_ok and bool(np.isfinite(cond)) and Fraction(cond) <= nc.T_COND_MAX
    out.update(U=U, T=T, Tinv=Tinv, sv=sv, rank=rank, cond_T=cond, ok=bool(ok))
    out["status"] = "PASS" if ok else CONSTRUCTION
    return out


class CoordMap(torch.nn.Module):
    """u -> beta + ((u - beta) @ Q0) @ T.T @ Q0.T over the last dimension (float64 buffers)."""

    def __init__(self, beta, Q0, T):
        super().__init__()
        for name, x in (("beta", beta), ("Q0", Q0), ("T", T)):
            self.register_buffer(name, torch.from_numpy(np.array(x, dtype=np.float64)))

    def forward(self, u):
        return self.beta + ((u - self.beta) @ self.Q0) @ self.T.T @ self.Q0.T


def coord_head(kind, WU, Q0, Tinv, g=nc.G_D) -> np.ndarray:
    if kind == "DNULLR":
        return float(g) * _f(WU)
    if kind == "DID":
        return _f(WU) @ _f(Q0) @ _f(Tinv) @ _f(Q0).T
    raise ValueError(f"unknown coordinate decoy {kind!r}")


def make_coord_decoy(model64, kind, Q0, beta, T, Tinv, WU, g=nc.G_D):
    """A deep copy whose ln_final is Sequential(the base LayerNorm, CoordMap) and whose head is
    g W_U (DNULLR) or W_U Q0 Tinv Q0' (DID) (ND-C27)."""
    dec = copy.deepcopy(model64)
    dec.ln_final = torch.nn.Sequential(dec.ln_final, CoordMap(beta, Q0, T))
    return _with_head(dec, coord_head(kind, WU, Q0, Tinv, g))


def coord_basis(decoy, base_basis) -> dict:
    """The readout_basis keys with the base LayerNorm basis and the decoy's head (§11.2)."""
    out = dict(base_basis)
    out["WU"] = _np(decoy.unembed.weight)
    out["M"], out["WUbeta"] = out["WU"] @ _f(out["Q0"]), out["WU"] @ _f(out["beta"])
    return out


def decoy_basis(decoy, base_basis) -> dict:
    return coord_basis(decoy, base_basis) if _is_coord(decoy) else cm.readout_basis(decoy)


def _is_coord(decoy) -> bool:
    return isinstance(decoy.ln_final, torch.nn.Sequential)


# ---- identity (§2.7; §6.4) -------------------------------------------------------------------
def decoy_sha64(decoy, record) -> str:
    """sha256 over (key, NUL, shape, NUL, float64 bytes) per sorted state_dict key, then the
    record as compact sorted JSON (ND-C28)."""
    h, sd = hashlib.sha256(), decoy.state_dict()
    for k in sorted(sd):
        t = np.ascontiguousarray(_np(sd[k]))
        h.update(k.encode("utf-8") + b"\0" + str(tuple(t.shape)).encode("ascii") + b"\0")
        h.update(t.tobytes())
    h.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    return h.hexdigest()


def decoy_record(j, kind) -> dict:
    dc = nc.CONTRACT["decoys"]
    return {
        "version": nc.DECOY_VERSION,
        "kind": kind,
        "model": int(j),
        "base_state_sha": nc.CONTRACT["models"][str(j)]["state_sha_f32"],
        "c2_fit_sha256": nc.CONTRACT["c2_store"]["files"][f"fits/FIT_{j}.npz"],
        "g_D": dc["g_D"],
        "rho": dc["rho"],
    }


def construction_record(j, kind, decoy, extra=None) -> dict:
    """The record plus decoy_sha64 and `extra` (coordinate decoys: cond_T, sv_LBV0, k0, U/B)."""
    rec = decoy_record(j, kind)
    return dict(rec, decoy_sha64=decoy_sha64(decoy, rec), **(extra or {}))


# ---- M0-D (§3 row 11) ------------------------------------------------------------------------
def nullity(heads, B) -> dict:
    """{"null_<kind>": ||C M' B||_max / (||C M'||_max ||B||_max)} (C centres the outputs)."""
    out = {}
    for kind, Mp in heads.items():
        CMp = _f(Mp) - _f(Mp).mean(axis=0)
        out[f"null_{kind}"] = _mx(CMp @ _f(B)) / (_mx(CMp) * _mx(B))
    return out


def adapter_identities(V0, U, T, Tinv, B, Gamma, L_B, M, heads, dz=None) -> dict:
    """The 1e-10 adapter identities of §3 row 11 (vii), norm-scaled (API.md §6.5, §20 A-2)."""
    V0, U, T, Tinv, B, Gamma, L_B, M = (_f(x) for x in (V0, U, T, Tinv, B, Gamma, L_B, M))
    eye = np.eye(T.shape[0])
    out = {"V0tV0": _mx(V0.T @ V0 - np.eye(V0.shape[1])), "LBU": _mx(L_B @ U - np.eye(U.shape[1]))}
    out["MU"] = _mx(M @ U) / (_mx(M) * _mx(U))
    out["TTinv"], out["TB"] = _mx(T @ Tinv - eye), _mx(T @ B - U) / _mx(U)
    out["TG"], out["LBT"] = _mx(T @ Gamma - Gamma) / _mx(Gamma), _mx(L_B @ T - L_B) / _mx(L_B)
    out.update(nullity(heads, B))
    for a, b in (("DNULLR", "DNULL"), ("DID", "base")) if dz is not None else ():
        za, zb = _f(dz[a]), _f(dz[b])
        rows = np.max(np.abs(za - zb), axis=1) / np.maximum(1.0, np.max(np.abs(zb), axis=1))
        out[f"pred_{a}"] = float(np.max(rows)) if rows.size else 0.0
    return out


def _tokens(inputs) -> torch.Tensor:
    if torch.is_tensor(inputs):
        return inputs
    return torch.as_tensor(np.asarray(inputs, dtype=np.int64))


def _pairs(z) -> np.ndarray:
    z, h = _f(z), len(z) // 2
    return z[:h] - z[h : 2 * h]


def _one(kind, dec, model64, inp, base_basis, inputs, acts, policy, mm) -> tuple:
    """Items (i)-(v) and (viii) of one decoy; returns (items, values, logits)."""
    coord, it, val = kind in nc.COORD_DECOYS, {}, {}
    W = _np(dec.unembed.weight)
    if coord:
        it["i"] = bool(mm["ok"]) and np.array_equal(
            W, coord_head(kind, inp["WU"], inp["Q0"], mm["Tinv"])
        )
        cmap = dec.ln_final[1]
        it["i"] = it["i"] and np.array_equal(_np(cmap.T), mm["T"])
        it["i"] = it["i"] and np.array_equal(_np(cmap.Q0), inp["Q0"])
        it["i"] = it["i"] and np.array_equal(_np(cmap.beta), inp["beta"])
    else:
        it["i"] = np.array_equal(W, head_edit(kind, inp["WU"], inp["Q0"], inp["P_S"]))
    base_sd, sd = model64.state_dict(), dec.state_dict()
    keys = [k for k in base_sd if k != "unembed.weight"]
    alias = {k: k.replace("ln_final.", "ln_final.0.", 1) if coord else k for k in keys}
    it["ii"] = all(alias[k] in sd and torch.equal(sd[alias[k]], base_sd[k]) for k in keys)
    da = cm.activations3(dec, inputs)
    up = all(np.array_equal(da[s], acts[s]) for s in cc.SITES if s != "ln_final_out")
    u, b, Q0 = _f(acts["ln_final_out"]), inp["beta"], inp["Q0"]
    if coord:
        want = b + ((u - b) @ Q0) @ _f(mm["T"]).T @ Q0.T
        dev = np.max(np.abs(da["ln_final_out"] - want), axis=1)
        tol = float(nc.frac(nc.M0D_COORD)) * np.maximum(1.0, np.max(np.abs(want), axis=1))
        it["iii"], val["iii_max_dev"] = up and bool(np.all(dev <= tol)), float(np.max(dev))
    else:
        it["iii"] = up and np.array_equal(da["ln_final_out"], acts["ln_final_out"])
    z = c1_model.natural_logits(dec, _tokens(inputs))
    zp = cm.patched_logits(dec, inputs, "ln_final_out", da["ln_final_out"], policy, "m0")
    it["iv"] = bool(np.array_equal(zp, z))
    basis = decoy_basis(dec, base_basis)
    y = cm.readout_coords(da["ln_final_out"], basis)
    ri = cm.readout_identity(z, y, basis)
    it["v"], val["v_max_dev"] = bool(ri["ok"]), ri["max_dev"]
    kappa = cm.kappa_x1(da["ln_final_out"], y, basis, z)
    it["viii"], val["kappa_x1"] = bool(cm.x1_attainable(kappa)), kappa
    return it, val, z


def m0d(j, model64, decoys, base_basis, c2_fit, inputs, acts, z_base, policy) -> dict:
    """M0-D on the given rows (API.md §6.5, §20 B-1): items (i)-(viii) per decoy. A head edit
    failing (i)-(v) or (vii) -> FAIL_TECHNICAL/DECOY; a coordinate decoy failing any item -> that
    kind EXCLUDED/CONSTRUCTION (report-only, NOT_COMPUTED; ND-C41); (viii) false ->
    INCONCLUSIVE/NUMERICAL for that decoy (study status only for DNULL)."""
    policy.require("m0")
    policy.require("construction")
    inp = base_inputs(c2_fit, base_basis)
    basis_ok = all(np.array_equal(_f(base_basis[k]), _f(c2_fit[k])) for k in BASIS_KEYS)
    mm = move_map(inp["B"], inp["L_B"], inp["M"])
    per, z = {}, {}
    values = {"move": {"rank": mm["rank"], "cond_T": mm["cond_T"]}}
    for kind in [k for k in nc.HEAD_EDITS + nc.COORD_DECOYS if k in decoys]:
        dec = decoys[kind]
        it, val, z[kind] = _one(kind, dec, model64, inp, base_basis, inputs, acts, policy, mm)
        it["i"] = it["i"] and basis_ok
        val["decoy_sha64"] = construction_record(j, kind, dec)["decoy_sha64"]
        per[kind], values[kind] = {"items": it}, val
    hk = [k for k in ("DNULL", "DNULL1") if k in decoys]
    heads = {k: _np(decoys[k].unembed.weight) @ inp["Q0"] for k in hk}
    ai = nullity(heads, inp["B"])
    if mm["ok"]:
        dz = None
        if {"DNULLR", "DNULL", "DID"} <= set(z):
            dz = {k: _pairs(z[k]) for k in ("DNULLR", "DNULL", "DID")}
            dz["base"] = _pairs(z_base)
        ai = adapter_identities(
            mm["V0"],
            mm["U"],
            mm["T"],
            mm["Tinv"],
            inp["B"],
            inp["Gamma"],
            inp["L_B"],
            inp["M"],
            heads,
            dz,
        )
    values["adapter"] = ai
    ok7 = {k: _le(v, nc.ADAPTER) for k, v in ai.items()}
    for kind, rec in per.items():
        it = rec["items"]
        if kind in nc.HEAD_EDITS:
            it["vii"] = ok7.get(f"null_{kind}", True)
            need, fail = ("i", "ii", "iii", "iv", "v", "vii"), DECOY
        else:
            it["vi"] = bool(mm["ok"])
            it["vii"] = it["vi"] and all(v for k, v in ok7.items() if not k.startswith("null_"))
            need, fail = ("i", "ii", "iii", "iv", "v", "vi", "vii"), CONSTRUCTION
        bad = not all(it[x] for x in need)
        rec["status"] = fail if bad else NUMERICAL if not it["viii"] else "PASS"
    head_st = [per[k]["status"] for k in per if k in nc.HEAD_EDITS]
    status = DECOY if DECOY in head_st else "PASS"
    if status == "PASS" and per.get("DNULL", {}).get("status") == NUMERICAL:
        status = NUMERICAL
    items = ("i", "ii", "iii", "iv", "v", "vi", "vii", "viii")
    checks = {x: all(per[k]["items"].get(x, True) for k in per) for x in items}
    return {"status": status, "checks": checks, "values": values, "per_decoy": per}


# ---- DX (§3 row 20; API.md §20 A-3) ----------------------------------------------------------
def _rows_over(num, den_scale, tol) -> np.ndarray:
    num, den = np.abs(_f(num)), np.maximum(1.0, np.abs(_f(den_scale)))
    return ~(num <= float(nc.frac(tol)) * den), num / den


def dx(arrays, policy) -> dict:
    """Per row with the construction projector: the exact non-use, dose, code-only and
    compensated-move identities; diagnostics only; a failure -> FAIL_TECHNICAL/DECOY."""
    policy.require("dx")
    policy.require("construction")
    per, ids = {}, {}
    for kind, a in arrays.items():
        if kind in ("DNULL", "DNULL1", "DNULLR"):
            over, rel = _rows_over(a["A_S"], a["A_full"], nc.DX_A)
            over_e, _ = _rows_over(a["e_S"], a["e_full"], nc.DX_E)
            over = over | over_e
        elif kind == "DONLY":
            comp = a["A_comp"] if "A_comp" in a else _f(a["A_full"]) - _f(a["A_S"])
            over, rel = _rows_over(comp, a["A_full"], nc.DX_A)
        elif kind == "DDOSE":
            want = float(nc.G_D) * float(1 - nc.RHO) * _f(a["A_S_base"])
            over, rel = _rows_over(_f(a["A_S"]) - want, a["A_S"], nc.DX_A)
        elif kind == "DID":
            dzz = _f(a["z"]) - _f(a["z_base"])
            dzz = dzz - dzz.mean(axis=1, keepdims=True)
            scale = np.max(np.abs(_f(a["z_base"])), axis=1)
            over, rel = _rows_over(np.max(np.abs(dzz), axis=1), scale, nc.DX_A)
        else:
            raise ValueError(f"unknown decoy {kind!r}")
        rel = np.where(np.isfinite(rel), rel, np.inf)
        per[kind] = {
            "max_rel": float(np.max(rel)) if rel.size else 0.0,
            "n_over": int(np.count_nonzero(over)),
        }
        if per[kind]["n_over"]:
            ids[kind] = np.flatnonzero(over).tolist()
    status = DECOY if ids else "PASS"
    return {"status": status, "per_decoy": per, "ids_over": ids}
