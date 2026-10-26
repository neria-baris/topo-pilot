"""C2 model evaluation: model loading, the three-hook pass, the readout basis Q0/M (Lemma R),
the closed-form logits, the M0 checks, the SYMBOL-ORDER checks, X1 (ephemeral) and its
attainability, and the site-parameterised patch wrappers (API.md §7; C2-FROZEN-v1 §2.1, §2.3,
§2.7, §5.7, §7 rows 9, 17, 23).

Every function that forms logits calls policy.require(kind) first (API.md §19.1 E-26); the
logits of activation passes are deleted unread (computation-order rule, §5.7).
"""

from __future__ import annotations

from fractions import Fraction

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_fit
import c1_model
import c1_oracle
import c1_registry_sources as crs
import numpy as np
import torch

from topo_pilot.learner import forward_with_patch

MODEL, NUMERICAL, X1_FAIL = "FAIL_TECHNICAL/MODEL", "INCONCLUSIVE/NUMERICAL", "FAIL_TECHNICAL/X1"
PROTOCOL_IDS = {
    1729: ("c3358e3cb9c352fb", "3633ac27dab50cf4"),
    2718: ("98b0e703a337d513", "97838b9e13a26f74"),
    3141: ("036b670743ffbbaf", "8c29c329c197c79e"),
}  # protocol §0


# ---- models and passes (API.md §7.1) ---------------------------------------------------------
def load_models() -> dict:
    """{model: (model64, float32 state_sha)} through c1_model.load_model64 (exact float64 cast,
    bitwise round trip, single thread)."""
    from topo_pilot.contracts import ArtifactStore, Checkpoint
    from topo_pilot.contracts.backends import LocalFSBackend

    store = ArtifactStore(LocalFSBackend(cc.ARTIFACT_ROOT))
    out = {}
    for j in cc.MODELS:
        ck = store.load(
            Checkpoint, cc.CONTRACT["models"][str(j)]["checkpoint"], consumer="experiment"
        )
        out[j] = c1_model.load_model64(ck)
    return out


def _batches(n, batch):
    for s in range(0, n, int(batch)):
        yield slice(s, min(n, s + int(batch)))


def _tokens(inputs) -> torch.Tensor:
    return (
        torch.as_tensor(np.asarray(inputs, dtype=np.int64))
        if not torch.is_tensor(inputs)
        else inputs
    )


def _pass(model64, inputs, keep_logits, batch):
    inputs = _tokens(inputs)
    acts = {s: [] for s in cc.SITES}
    logits = []
    with torch.no_grad():
        for sl in _batches(inputs.shape[0], batch):
            res = model64(inputs[sl], return_hooks=cc.SITES)
            for s in cc.SITES:
                acts[s].append(res.hooks[s][:, cc.INDEX, :].to(torch.float64).numpy().copy())
            if keep_logits:
                logits.append(res.logits[:, cc.INDEX].to(torch.float64).numpy().copy())
            del res  # activation-pass logits are discarded unread
    acts = {s: np.vstack(v) for s, v in acts.items()}
    return acts, (np.vstack(logits) if keep_logits else None)


def activations3(model64, inputs, batch=1024) -> dict:
    """resid_post_2, resid_post_3 and ln_final_out at position 32 (float64 [n, 128])."""
    return _pass(model64, inputs, False, batch)[0]


def natural_pass(model64, inputs, policy, kind, batch=1024) -> tuple:
    policy.require(kind)
    return _pass(model64, inputs, True, batch)


def patched_logits(model64, inputs, site, rep, policy, kind, batch=1024) -> np.ndarray:
    """forward_with_patch at (site, 32) with rep [n, 128]; logits at position 32."""
    policy.require(kind)
    inputs, rep = _tokens(inputs), torch.as_tensor(np.asarray(rep, dtype=np.float64))
    out = []
    with torch.no_grad():
        for sl in _batches(inputs.shape[0], batch):
            res = forward_with_patch(model64, inputs[sl], site, cc.INDEX, rep[sl])
            out.append(res.logits[:, cc.INDEX].to(torch.float64).numpy().copy())
    return np.vstack(out)


# ---- readout coordinates (§2.1, Lemma R; API.md §7.2) ----------------------------------------
def helmert(n=128) -> np.ndarray:
    """Orthonormal Helmert basis of 1-perp: column k has 1/sqrt(k(k+1)) in rows 1..k and
    -k/sqrt(k(k+1)) in row k+1 (1-based)."""
    out = np.zeros((int(n), int(n) - 1))
    for k in range(1, int(n)):
        s = np.sqrt(k * (k + 1.0))
        out[:k, k - 1] = 1.0 / s
        out[k, k - 1] = -k / s
    return out


def readout_basis(model64) -> dict:
    def arr(t):
        return t.detach().to(torch.float64).cpu().numpy().copy()

    gamma, beta = arr(model64.ln_final.weight), arr(model64.ln_final.bias)
    WU = arr(model64.unembed.weight)
    N1 = helmert(gamma.shape[0])
    A = np.diag(gamma) @ N1
    Q0 = c1_fit.qr_pos(A)
    R_diag = np.abs(np.diag(np.linalg.qr(A, mode="r")))
    rank_ok = bool(R_diag.min() > float(cc.frac(cc.RANK_R)) * R_diag.max())
    return {
        "gamma": gamma,
        "beta": beta,
        "WU": WU,
        "N1": N1,
        "Q0": Q0,
        "R_diag": R_diag,
        "rank_ok": rank_ok,
        "M": WU @ Q0,
        "WUbeta": WU @ beta,
        "ln_eps": float(model64.ln_final.eps),
    }


def readout_coords(u, basis) -> np.ndarray:
    return (np.asarray(u, dtype=np.float64) - basis["beta"]) @ basis["Q0"]


def closed_logits(y, basis) -> np.ndarray:
    """W_U beta + M y (the stored WUbeta, so a defective beta or Q0 shows in X1)."""
    return basis["WUbeta"] + np.asarray(y, dtype=np.float64) @ np.asarray(basis["M"]).T


def placed(y_hat, basis) -> np.ndarray:
    return (
        np.asarray(basis["beta"]) + np.asarray(y_hat, dtype=np.float64) @ np.asarray(basis["Q0"]).T
    )


# ---- M0 (§7 row 9; API.md §7.3) --------------------------------------------------------------
def identity_patch(model64, inputs, acts, policy) -> dict:
    """{site: patched logits bitwise equal to the natural logits} at the three sites."""
    policy.require("m0")
    z_nat = c1_model.natural_logits(model64, _tokens(inputs))
    return {
        s: bool(np.array_equal(patched_logits(model64, inputs, s, acts[s], policy, "m0"), z_nat))
        for s in cc.SITES
    }


def _row_check(z, z_closed) -> tuple:
    z = np.asarray(z, dtype=np.float64)
    dev = np.max(np.abs(z - z_closed), axis=1)
    tol = float(cc.frac(cc.TAU_X1)) * np.maximum(1.0, np.max(np.abs(z), axis=1))
    over = ~(dev <= tol)  # a non-finite deviation or tolerance counts as over (fail-closed)
    max_dev = float(np.max(np.where(np.isfinite(dev), dev, np.inf))) if dev.size else 0.0
    return max_dev, over


def readout_identity(z_net, y, basis) -> dict:
    max_dev, over = _row_check(z_net, closed_logits(y, basis))
    n_over = int(np.count_nonzero(over))
    return {"max_dev": max_dev, "n_over": n_over, "ok": n_over == 0}


def kappa_x1(u, y, basis, z) -> float:
    """max_{i,v} S_iv / max(1, |z_i|_inf), S_iv the head-arithmetic sum of §2.7."""
    WU, Q0, beta = (np.abs(np.asarray(basis[k])) for k in ("WU", "Q0", "beta"))
    S = (np.abs(u) + beta[None, :]) @ WU.T + np.abs(y) @ (WU @ Q0).T
    return float(np.max(S / np.maximum(1.0, np.max(np.abs(z), axis=1))[:, None]))


def x1_attainable(kappa) -> bool:
    """4 * 128 * 2**-53 * kappa_X1 <= 1e-10 in exact rationals (API.md C-6)."""
    return 4 * 128 * cc.UNIT_ROUNDOFF * Fraction(float(kappa)) <= cc.frac(cc.X1_ATTAIN)


def two_route(d_canon, d_named, z_named, perm) -> dict:
    """M0 SYMBOL-ORDER two-route rule per row (T18, NEW-7)."""
    d_canon, d_named = np.asarray(d_canon, np.float64), np.asarray(d_named, np.float64)
    z_named = np.asarray(z_named, np.float64)
    s_n = 0.5 * np.sum(d_named * z_named, axis=1)
    z_c = c1_oracle.canonical_from_named_cols(z_named, perm)
    s_c = 0.5 * np.sum(d_canon * z_c, axis=1)
    bound = float(cc.frac(cc.T18)) * np.maximum(1.0, np.sum(np.abs(d_canon * z_c), axis=1))
    gap = np.abs(s_n - s_c)
    return {
        "max_ratio": float(np.max(gap / bound)) if gap.size else 0.0,
        "ok": bool(np.all(gap <= bound)),
    }


def symbol_order_a(named_inputs, canon32, perm) -> bool:
    """(a): the named input tokens are perm[w], by the independent inverse route canonical32."""
    named = np.asarray(named_inputs, dtype=np.int64)
    return bool(
        np.array_equal(crs.canonical32(named[:, 1:], perm), np.asarray(canon32).astype(np.uint8))
    )


def symbol_order_b(perm) -> bool:
    """(b): named_from_canonical(e_c, perm) = e_{perm[c]} for every canonical c (bitwise)."""
    eye = np.eye(cc.V)
    return bool(np.array_equal(c1_oracle.named_from_canonical(eye, perm), eye[np.asarray(perm)]))


def symbol_order_c(d_canon, perm) -> bool:
    """(c): canonical_from_named_cols(named_from_canonical(d, perm), perm) = d (bitwise)."""
    d = np.asarray(d_canon)
    back = c1_oracle.canonical_from_named_cols(c1_oracle.named_from_canonical(d, perm), perm)
    return bool(np.array_equal(back, d))


def m0(model64, sha, contract_j, inputs, acts, z_net, basis, d_canon, perm, policy) -> dict:
    """§7 row 9 in order: ids, state_sha, round trip, identity patches, rank, readout identity,
    two-route SYMBOL-ORDER, X1 attainability (on the 1024 lowest-id FIT rows)."""
    policy.require("m0")
    ident = (contract_j.get("checkpoint"), contract_j.get("EmissionSpec"))
    j = next((m for m, ids in PROTOCOL_IDS.items() if ids == ident), None)
    want = cc.CONTRACT["models"][str(j)]["state_sha_f32"] if j is not None else None
    y = readout_coords(acts["ln_final_out"], basis)
    checks = {
        "ids": j is not None and contract_j.get("state_sha_f32") == want,
        "state_sha": want is not None and str(sha).lower() == str(want).lower(),
        "roundtrip": True,
    }  # load_model64 raises FAIL_TECHNICAL/MODEL otherwise
    patch = identity_patch(model64, inputs, acts, policy)
    checks.update(identity=all(patch.values()), rank=bool(basis["rank_ok"]))
    rid = readout_identity(z_net, y, basis)
    route = two_route(d_canon, c1_oracle.named_from_canonical(d_canon, perm), z_net, perm)
    kappa = kappa_x1(acts["ln_final_out"], y, basis, z_net)
    checks.update(readout=rid["ok"], two_route=route["ok"], attainable=x1_attainable(kappa))
    model_ok = all(v for k, v in checks.items() if k != "attainable")
    status = MODEL if not model_ok else "PASS" if checks["attainable"] else NUMERICAL
    values = {
        "model": j,
        "patch": patch,
        "readout": rid,
        "two_route": route,
        "kappa_x1": kappa,
        "R_diag_min_max": [float(basis["R_diag"].min()), float(basis["R_diag"].max())],
    }
    return {"status": status, "checks": checks, "values": values}


# ---- X1, ephemeral (§2.7, §5.7; API.md §7.4) -------------------------------------------------
def x1(model64, arms, basis, policy) -> dict:
    """Closed form vs the network on every arm; arms[name] = (inputs, y_hat, z_ref, seq_ids),
    z_ref None for a patched arm. Returns identity diagnostics only; every logit is deleted."""
    policy.require("x1")
    out, ids_over = {}, set()
    for name, (inputs, y_hat, z_ref, seq_ids) in arms.items():
        y_hat = np.asarray(y_hat, dtype=np.float64)
        if z_ref is None:
            rep = placed(y_hat, basis)
            bad = ~np.all(np.isfinite(rep), axis=1)
            z = patched_logits(
                model64, inputs, "ln_final_out", np.where(bad[:, None], 0.0, rep), policy, "x1"
            )
            z[bad] = np.nan  # a non-finite replacement is never forwarded; it fails closed
        else:
            z = np.asarray(z_ref, dtype=np.float64)
        max_dev, over = _row_check(z, closed_logits(y_hat, basis))
        del z
        out[name] = {"max_dev": max_dev, "n_over": int(np.count_nonzero(over))}
        ids_over |= {int(i) for i in np.asarray(seq_ids)[over].tolist()}
    status = "PASS" if all(a["n_over"] == 0 for a in out.values()) else X1_FAIL
    return {"arms": out, "ids_over": sorted(ids_over), "status": status}
