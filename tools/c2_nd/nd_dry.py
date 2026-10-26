"""C2ND synthetic dry run (API.md §11; C2ND-DESIGN-v1 §10.1): planted models (random-initialised
TransformerLMs with the trained architecture whose head reads a planted 6-d harmonic code of a
synthetic phase with share 0.85), the synthetic C2-prerequisite fixture (the c2/ stand-in of the
C2 store: FIT projectors, decoders, N2 fit, frozen oracle constants, made by the C2 kernels on
synthetic activations of cylinder-O histories from a dry-only stream), the synthetic phase, the
broken decoys of pass criterion 3 (the J-built decoy fails; the Euclidean one is reported,
E-C2ND-2) and the forbidden-access and planted-collision checks. Every function refuses with
FAIL_TECHNICAL/AUTHORITY outside a dry-run store (G0 (x)); no trained weight, no C2 store file
and no c2nd-v1 stream is touched."""

from __future__ import annotations

from pathlib import Path

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c1_data
import c1_oracle
import c2_attrib as ca
import c2_code as ck
import c2_config as cc
import c2_data as cd
import c2_model as cm
import c2_oracle as co2
import c2_stats as cs
import nd_attrib as nat
import nd_decoy as ndy
import nd_driver as ndr
import nd_registry as nrg
import nd_stage_base as sb
import numpy as np
import torch
from c1_records import C1GateFailure

from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset import HMMSampler
from topo_pilot.dataset.checks import make_sequence_ids, process_code
from topo_pilot.learner.config import ModelConfig
from topo_pilot.learner.model import TransformerLM

STREAM, SHARE, KP = "c2prereq", 0.85, {"R": 3, "R_K1": 1, "R_K2": 2, "R_E": 3, "M": 3}
CFG = {"vocab_in": cc.V + 1, "vocab_out": cc.V, "d_model": cc.D_MODEL, "n_heads": 4, "d_mlp": 512}


def guard(ctx) -> None:
    if not (getattr(ctx, "dry", False) and ndr.is_dry_store(ctx.store)):
        raise C1GateFailure("FAIL_TECHNICAL/AUTHORITY", "dry-run switch outside a dry-run store")


# ---- planted models and the synthetic phase (§10.1) -------------------------------------------
def _model(state=None, seed=0) -> TransformerLM:
    torch.manual_seed(int(seed))
    m = TransformerLM(ModelConfig(**CFG)).to(torch.float64).eval()
    if state is not None:
        m.load_state_dict({k: torch.from_numpy(np.asarray(v)) for k, v in state.items()})
    return m


def planted_models(ctx) -> dict:
    """{j: (model64, sha256 of its c2/models file)}, the file re-hashed against c2/TABLE.json."""
    guard(ctx)
    out = {}
    for j in nc.MODELS:
        rel = f"models/PLANTED_{j}.npz"
        out[j] = (_model(sb.c2npz(ctx, rel)), sb.c2_store(ctx)[1][rel])
    return out


def synthetic_phase(ctx, j, a3) -> tuple:
    """phi = atan2 of resid_post_3 (centred) on the two leading within-symbol principal
    directions of the stand-in fit; every row supported (replaces the chart phase)."""
    guard(ctx)
    C = sb.c2npz(ctx, f"charts/CHART_{j}_dry.npz")
    c = (np.asarray(a3, np.float64) - C["mu"]) @ C["U"].T
    return np.arctan2(c[:, 1], c[:, 0]), np.ones(len(c), dtype=bool)


def _chart(a3, w) -> dict:
    """mu and the two leading principal directions of resid_post_3 minus its symbol means."""
    means = np.zeros((cc.V, a3.shape[1]))
    for s in np.unique(w):
        means[s] = a3[w == s].mean(axis=0)
    _, _, Vt = np.linalg.svd(a3 - means[w], full_matrices=False)
    return {"mu": a3.mean(axis=0), "U": Vt[:2].copy()}


# ---- the synthetic C2-prerequisite fixture (PREP) ---------------------------------------------
def _sample(P, b) -> tuple:
    """One 4,096-row block of the dry-only stream (scope c2nd-dry-v1, split c2prereq)."""
    rng = SeedTree(0).generator("data", nc.DRY_SCOPE, STREAM, int(b), *nc.PROCESS)
    tok, st = HMMSampler(P["T"], P["E_canon"][nc.MODELS[0]], P["pi"], SequenceLayout()).sample(
        nc.BLOCK, rng
    )
    code = process_code(*nc.PROCESS, f"{nc.DRY_SCOPE}/{STREAM}/b{int(b)}")
    ids = np.asarray(make_sequence_ids(code, "test", nc.BLOCK), dtype=np.int64)
    return np.ascontiguousarray(tok[:, :32]).astype(np.uint8), ids


def _write(ctx, rel, arrays=None, obj=None) -> None:
    rel = f"c2/{rel}"
    (sb.put(ctx, rel, **arrays) if arrays is not None else sb.putj(ctx, rel, obj))


def _plant(m64, y, d, dy, Ex, G, logq, P_S) -> dict:
    """The head: least squares of the oracle's named log-predictive on y, split into the code
    part (P_S) and the rest and rescaled so that the code carries SHARE of the response and
    the whole response equals the oracle contrast on average (theta = 1, psi = SHARE)."""
    X1 = np.hstack([np.ones((len(y), 1)), y])
    Mp = np.linalg.lstsq(X1, logq - logq.mean(axis=1, keepdims=True), rcond=None)[0][1:].T
    Id = np.eye(P_S.shape[0])
    aS = float(np.mean(ca.half_dot(d, dy @ (Mp @ P_S).T)[Ex]))
    aC = float(np.mean(ca.half_dot(d, dy @ (Mp @ (Id - P_S)).T)[Ex]))
    g = float(np.mean(G[Ex]))
    a, c = SHARE * g / aS, (1.0 - SHARE) * g / aC
    M = a * Mp @ P_S + c * Mp @ (Id - P_S)
    Q0 = cm.readout_basis(m64)["Q0"]
    with torch.no_grad():
        m64.unembed.weight.copy_(torch.from_numpy(M @ Q0.T))
    return {"a_code": a, "a_rest": c, "mean_AS0": aS, "mean_Acomp0": aC, "mean_G": g}


def prepare(ctx) -> dict:
    """PREP: the c2/ stand-in subtree, c2/TABLE.json and the PREP manifest (accepted by the
    coordinator before S1). Activations only for the fit; logits never formed here."""
    guard(ctx)
    P, canon, ids, panel = co2.load_process(), [], [], []
    for b in range(2):
        c, i = _sample(P, b)
        canon, ids, panel = canon + [c], ids + [i], panel + [c1_data.panels(i, b)]
    canon, ids, panel = np.vstack(canon), np.concatenate(ids), np.concatenate(panel)
    T, E, pi, co = P["T"], P["E_canon"][nc.MODELS[0]], P["pi"], P["coords"]
    oH = co2.oracle_role(T, E, pi, canon, co)
    tab = cd.history_table(canon, ids, panel, cd.k_y(oH["b31"], co))
    for b in range(2):
        sl = slice(b * nc.BLOCK, (b + 1) * nc.BLOCK)
        _write(ctx, f"hist/HIST_{STREAM}_b{b}.npz", {k: v[sl] for k, v in tab.items()})
    o = co2.oracle_split(T, E, pi, co, canon, tab["k_Y"], o_H=oH)
    smax = co2.s_max(o["H"]["s"])
    el = co2.eligibility(o, smax)
    km = co2.kappa_m(o["H"]["m32"], o["HY"]["m32"], el["E_y"], o["H"]["m32"])
    fz = {"s_max": smax, "kappa_m": km, "kappa_nu": co2.kappa_nu(o, el["E_x"], co)}
    _write(ctx, "oracle/ORACLE_FROZEN.json", obj=dict(fz, y_active=co2.y_active(km)))
    w, Ex = canon[:, 31].astype(np.int64), np.asarray(el["E_x"], bool)
    mu, sd = ck.standardise(o["nuis"])
    z, nu = (o["nuis"] - mu) / sd, c1_oracle.y_marginal(o["H"]["b32"], co)
    rec = {}
    for j in nc.MODELS:
        m64, roles = _model(seed=j), cd.table_roles(tab)
        acts = {r: cm.activations3(m64, sb.inputs(ctx, j, roles[r][0])) for r in ("H", "Hp", "Hm")}
        basis = cm.readout_basis(m64)
        y = {r: cm.readout_coords(a["ln_final_out"], basis) for r, a in acts.items()}
        ch = _chart(acts["H"]["resid_post_3"], w)
        _write(ctx, f"charts/CHART_{j}_dry.npz", ch)
        phi = np.arctan2(*((acts["H"]["resid_post_3"] - ch["mu"]) @ ch["U"].T)[:, ::-1].T)
        arr, info, dec, prs = {"zt_mu": mu, "zt_sd": sd}, {"status": {}, "delta": {}}, {}, {}
        for p in ("R", "R_K1", "R_K2", "R_E", "M"):
            Y = acts["H"]["resid_post_2"] if p == "M" else y["H"]
            base = prs["R"]["fit"] if p == "R_E" else None
            pr = prs[p] = cs.f1_problem(
                Y, w, z, ck.harmonics(phi, KP[p]), euclidean=p == "R_E", fit=base
            )
            fit, g = pr["fit"], pr["g"]
            info["status"][p] = pr["status"]
            info["delta"][p] = cs.delta_p(pr["ref"]) if pr.get("ref") else float("inf")
            arr.update({f"{p}_{k}": fit[k] for k in ("alpha", "Gamma", "B")})
            arr.update({f"{p}_{k}": g[k] for k in ("L", "P_S", "P_G")})
            arr.update({f"{p}_Sigma": pr["Sigma"]} if p != "R_E" else {})
            arr[f"{p}_mtilde"] = np.float64(
                ck.zero_code_threshold(ck.code_phase(Y, fit["alpha"], w, g["L_B"])[1])
            )
            if p in ("R", "M"):
                dec[p] = cs.fit_decoders(w, z, Y @ g["L_B"].T, Y, ck.harmonics(phi, 1), panel)
        arr.update(
            {
                f"S*_{k[2:]}": v
                for k, v in arr.items()
                if k.startswith("R_") and not k.startswith(("R_E", "R_K"))
            }
        )
        d = co2.d_named(o["Hp"]["qbar"] - o["Hm"]["qbar"], P["perm"][j])
        logq = c1_oracle.named_from_canonical(np.log(o["H"]["qbar"]), P["perm"][j])
        rec[j] = _plant(m64, y["H"], d, y["Hp"] - y["Hm"], Ex, o["G_x"], logq, arr["R_P_S"])
        B = cm.readout_basis(m64)
        arr.update({k: B[k] for k in ("Q0", "M", "beta", "gamma", "WU", "WUbeta")})
        n2 = ck.n2_fit(acts["H"]["resid_post_2"], w)
        aff = ca.affine_readouts(y["H"], w, nu)
        W = n2["W"] if n2["W"] is not None else np.zeros((cc.D_MODEL,) * 2)
        arr.update(J=ca.null_projector(B["M"]), aff_w=aff["R_w"], aff_nu=aff["R_nu"])
        arr.update(n2_mu=n2["mu"], n2_W=W, n2_q99=n2["q99"])
        info["n2"] = n2["status"]
        _write(ctx, f"fits/FIT_{j}.npz", arr)
        _write(ctx, f"fits/FIT_{j}.json", obj=info)
        dec["Sstar"] = dec["R"]
        da = {
            f"{cc.FILE_FAMILY.get(F, F)}_{k}_{x}": a
            for F, ds in dec.items()
            for k, dd in ds.items()
            for x, a in cs.decoder_arrays(dd).items()
        }
        _write(ctx, f"fits/DEC_{j}.npz", da)
        _write(ctx, f"models/PLANTED_{j}.npz", {k: v.numpy() for k, v in m64.state_dict().items()})
    root = Path(ctx.store) / "c2"
    files = {
        p.relative_to(root).as_posix(): sb.cd.file_sha(p)
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }
    _write(
        ctx,
        "manifests/0115.json",
        obj={"schema": "c2nd-dry-standin-v1", "files": files, "planted": rec},
    )
    man = sb.cd.file_sha(root / "manifests" / "0115.json")
    _write(ctx, "manifests/0115.accepted.json", obj={"job": "0115", "manifest_sha256": man})
    files = {
        p.relative_to(root).as_posix(): sb.cd.file_sha(p)
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }
    _write(ctx, "TABLE.json", obj={"schema": "c2nd-dry-table-v1", "files": files})
    return {"stage": "PREP", "stopped": None, "manifest": str(sb.write_manifest(ctx, "PREP"))}


# ---- pass criterion 3 (broken decoys) and the forbidden-access checks (§10.1) -----------------
def broken_decoys(ctx, j, inputs, acts, z, d, dy) -> dict:
    """Wrong g_D, another model's projector, transposed P_S and the J-built decoy must fail M0-D
    or DX; the Euclidean-projector decoy is reported (E-C2ND-2). DX runs on the M0 rows' pairs
    under a private policy at DX (diagnostic only; no value enters a gate)."""
    guard(ctx)
    m64, F = sb.models(ctx)[j][0], sb.c2fit(ctx, j)
    B, P = cm.readout_basis(m64), F["R_P_S"]
    other = sb.c2fit(ctx, next(k for k in nc.MODELS if k != j))["R_P_S"]
    Bm = F["R_B"]
    Pe = Bm @ np.linalg.solve(Bm.T @ Bm, Bm.T)
    kinds = {"wrong_gD": (P, 5), "other_model": (other, nc.G_D), "transposed": (P.T, nc.G_D)}
    kinds.update(J_built=(F["J"], nc.G_D), euclidean=(Pe, nc.G_D))
    pol, out = ndr.LogitPolicy(done=ndr.GATE_ORDER[: ndr.GATE_ORDER.index("DX")]), {}
    pol.begin("DX")
    for name, (Pk, g) in kinds.items():
        W = ndy.head_edit("DNULL", F["WU"], F["Q0"], Pk, g=g)
        dec = ndy.make_head_decoy(m64, W)
        r = ndy.m0d(j, m64, {"DNULL": dec}, B, F, inputs, acts, z, ctx.policy)
        q = nat.nr_quantities(d, W @ F["Q0"], dy, np.zeros_like(dy), P)
        x = ndy.dx({"DNULL": q}, pol)
        fails = r["status"] != "PASS" or x["status"] != "PASS"
        out[name] = {
            "m0d": r["status"],
            "m0d_vii": r["checks"]["vii"],
            "dx": x["status"],
            "fails": fails,
        }
    out["criterion_3"] = all(
        out[k]["fails"] for k in ("wrong_gD", "other_model", "transposed", "J_built")
    )
    return out


def _refused(fn) -> bool:
    try:
        fn()
    except Exception:  # noqa: BLE001  a refusal of any kind
        return True
    return False


def checks(ctx, j, inputs, acts, z) -> dict:
    """§10.1: the broken decoys, the forbidden accesses (DTEST before ACCEPT, a construction
    projector in a method statistic, a value beyond PASS/FAIL in a release-only record, an
    out-of-order gate) and a planted registry collision (a stand-in C2 digest in DFIT)."""
    guard(ctx)
    T, half = sb.table(ctx, "fit"), len(inputs) // 2
    ob = sb.orc(ctx, "fit")
    rows = cd.lowest(T["sequence_id"], nc.M0_ROWS)
    qb = ob["H_qbar"][rows]
    d = co2.d_named(qb[:half] - qb[half : 2 * half], sb.proc(ctx)["perm"][j])
    y = cm.readout_coords(acts["ln_final_out"], sb.c2fit(ctx, j))
    out = {"broken": broken_decoys(ctx, j, inputs, acts, z, d, y[:half] - y[half : 2 * half])}
    q = {
        "A_full": np.ones(4),
        "A_S": np.zeros(4),
        "e_full": np.ones(4),
        "e_S": np.zeros(4),
        "r": np.ones(4),
    }
    E4 = np.ones(4, bool)
    out["forbidden"] = {
        "dtest_before_accept": not ndr.release_ok(ctx, "S5")["ok"],
        "construction_projector": _refused(
            lambda: nat.d_stream(q, q, q["A_full"], E4, E4, refit={"problem": "construction"})
        ),
        "release_beyond_pass_fail": all(
            _refused(lambda g=g: ndr.require_release(None, g, {"mean": 0.1}))
            for g in ndr.RELEASE_ONLY
        ),
        "out_of_order_gate": _refused(lambda: ndr.LogitPolicy().begin("G0")),
    }
    fake = {k: np.array(v, copy=True) for k, v in T.items()}
    stand = sb.c2npz(ctx, f"hist/HIST_{STREAM}_b0.npz")
    fake["digest_H"][0] = stand["digest_H"][0]
    try:
        st = nrg.separation(nrg.load(ctx.store, "ND-REG1"), {"fit": fake})["status"]
    except Exception as exc:  # noqa: BLE001  a lineage exception is a caught collision
        st = getattr(exc, "status", repr(exc))
    out["planted_collision"] = {"status": st, "caught": st == "FAIL_TECHNICAL/LINEAGE"}
    return out


def sealed_check(ctx) -> dict:
    """A sealed/ read before the TEST outcome must be refused (§10.1 forbidden access)."""
    guard(ctx)
    s = sb._jr(Path(ctx.store) / "stages" / "S4" / "SEALED.json") or {}
    name = next(iter(s), None)
    return {
        "sealed_read_refused": name is not None and _refused(lambda: ndr.unseal(ctx, name, s[name]))
    }
