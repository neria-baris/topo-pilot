"""HWS exact pieces: symbol law, A_eff, p_D2a, enumeration, spot checks, tier-0 law report and
the payload-free KC1 identity check (API.md §4; protocol §2.4, §2.6, §3 KC1/KC9/KC10, §8).

KC1 reads JSON only (meta.json, extra.json, the manifest and config.json) through `read_json`;
no payload.npz is opened or hashed and no store loader is called (R-HWS-2, RC-2).
"""

from __future__ import annotations  # noqa: I001  (hws_worlds sets sys.path first)

import decimal
import hashlib
import itertools
import json
import math
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path

import hws_worlds as hw
import error_bound
import hws_oracle as ho
import numpy as np
import oracle_profile
import process_law
from topo_pilot.contracts import SeedTree, canonical_json, make_artifact_id, payload_checksum
from topo_pilot.oracle import BayesFilter
from topo_pilot.process import EmissionConfig, OverlapGaussian, TransitionConfig
from topo_pilot.world import WorldConfig

JSON_READS: list = []
TOL = 1e-12
KC1 = "FAIL_TECHNICAL/KNOWN_CASE"


def symbol_law(proc) -> np.ndarray:
    return proc["pi"] @ proc["E"]


def last_symbol_posteriors(proc) -> np.ndarray:
    p = symbol_law(proc)
    return (proc["pi"][None, :] * proc["E"].T) / p[:, None]


def mean_last_entropy(proc) -> float:
    return float(symbol_law(proc) @ ho.entropy_rows(last_symbol_posteriors(proc)))


def a_eff(proc) -> float:
    return math.exp(mean_last_entropy(proc))


def p_d2a(T, E, pi, alphabet=(0, 1, 2, 3, 4), Lh=32) -> float:
    E = np.asarray(E, dtype=np.float64)
    cols = [int(v) for v in alphabet if int(v) < E.shape[1]]
    s = E[:, cols].sum(axis=1)
    a = np.asarray(pi, dtype=np.float64) * s
    for _ in range(int(Lh) - 1):
        a = (a @ T) * s
    return float(a.sum())


def e4_check(value, tau=Fraction(1, 2000000)) -> dict:
    ok = Fraction(float(value)) <= Fraction(tau)
    return {"status": "PASS" if ok else "INELIGIBLE/E4", "p_D2a": value}


def exact_world(proc) -> dict:
    """§4.6 step 6: exact per-world values and E1-E4 before any sampling."""
    base = {"key": proc["key"], "tier": proc.get("tier")}
    if "E" not in proc:
        return dict(base, e1=proc["e1"], status=proc["e1"]["status"])
    p_v = symbol_law(proc)
    filt = hw.exact_filters(proc, p_v)
    pd = p_d2a(proc["T"], proc["E"], proc["pi"])
    e4 = e4_check(pd)
    status = filt["status"] if filt["status"] != "PASS" else e4["status"]
    try:
        w = proc["world_key"]
        changed, dist = hw.changed_factors(w), str(hw.distance(w))
    except (KeyError, AttributeError, TypeError):
        changed, dist = None, None
    mle = mean_last_entropy(proc)
    return dict(
        base,
        p_v=[float(x) for x in p_v],
        min_p=float(np.min(p_v)),
        A_eff=math.exp(mle),
        mean_last_entropy=mle,
        p_D2a=pd,
        V=int(proc["V"]),
        n_A=int(proc["V"]) // int(proc["n_axial"]),
        symmetry=filt["e3"]["symmetry"],
        e1=filt["e1"],
        e2=filt["e2"],
        e3=filt["e3"],
        e4=e4,
        status=status,
        changed=changed,
        distance=dist,
    )


# --------------------------------------------------------------------------- enumeration


def _forward(proc, hist) -> np.ndarray:
    T, E, pi = proc["T"], proc["E"], proc["pi"]
    a = pi[None, :] * E[:, hist[:, 0]].T
    for t in range(1, hist.shape[1]):
        a = (a @ T) * E[:, hist[:, t]].T
    return a


def enumerate_histories(proc, Lh) -> tuple:
    V = int(proc["E"].shape[1])
    if V ** int(Lh) > 10**6:
        raise ValueError(f"V'^Lh = {V}^{Lh} exceeds 10^6")
    hist = np.array(list(itertools.product(range(V), repeat=int(Lh))), dtype=np.int64)
    return hist, _forward(proc, hist).sum(axis=1)


def _flag(value, ok) -> dict:
    return {"value": float(value), "pass": bool(ok)}


def exact_expectations(proc, Lh, Ks) -> dict:
    """Probability-weighted means of row_arrays over every history, plus I1-I4, Prop. F and
    row-wise Pinsker as {"value", "pass"} flags (erratum E4)."""
    hist, prob = enumerate_histories(proc, Lh)
    V = int(proc["E"].shape[1])
    rows = ho.row_arrays(proc, hist.astype(np.uint8), Ks)
    ks = sorted(rows["D"])
    E_ = {name: {K: float(prob @ rows[name][K]) for K in ks} for name in ("D", "rn", "G")}
    Vk = {K: float(prob @ rows["rn"][K] ** 2) for K in ks}
    out = {"D": E_["D"], "B": E_["rn"], "V": Vk, "G": E_["G"]}
    for name in ("G4A", "IZ4", "IX4", "G0"):
        out[name] = float(prob @ rows[name])
    mL = rows["m"][int(Lh)]
    i1 = 0.0
    for K in ks:
        r = mL - rows["m"][K]
        idx = hist[:, int(Lh) - K :] @ (V ** np.arange(K - 1, -1, -1))
        acc = np.zeros((V**K, 2))
        np.add.at(acc, idx, prob[:, None] * r)
        i1 = max(i1, float(np.max(np.abs(acc))))
    em = {K: float(prob @ np.sum(rows["m"][K] ** 2, axis=1)) for K in ks}
    emL = float(prob @ np.sum(mL**2, axis=1))
    i3 = max(abs(Vk[K] - (emL - em[K])) for K in ks)
    mono = all(Vk[a] >= Vk[b] - TOL for a, b in zip(ks, ks[1:]))
    i4 = max(float(np.max(rows["D"][K] - rows["rn"][K])) for K in ks)
    b4 = ho.beliefs(proc, hist.astype(np.uint8), (4,))
    q4 = ho.predictive(b4[4], proc["T"], proc["E"])
    qL = ho.predictive(b4[int(Lh)], proc["T"], proc["E"])
    preds = {
        "q4": q4,
        "uniform": np.full_like(q4, 1.0 / V),
        "stationary": np.broadcast_to(proc["pi"] @ proc["T"] @ proc["E"], q4.shape),
    }
    g4 = E_["G"][4]
    pf = 0.0
    for f in preds.values():
        lhs, extra = prob @ ho.kl_rows(qL, f), prob @ ho.kl_rows(q4, f)
        pf = max(pf, abs(lhs - g4 - extra), max(0.0, g4 - lhs))
    slack = float(np.min(rows["pinsker_slack"]))
    d4, b4m = E_["D"][4], E_["rn"][4]
    out["identities"] = {
        "I1": _flag(i1, i1 <= TOL),
        "I2": _flag(d4, -TOL <= d4 <= b4m + TOL),
        "I3": _flag(i3, i3 <= TOL and mono),
        "I4": _flag(i4, i4 <= TOL),
        "prop_F": _flag(pf, pf <= TOL),
        "pinsker": _flag(slack, slack >= -TOL),
    }
    return out


def suffix_enumeration(proc, Ks=(1, 2, 3)) -> dict:
    V = int(proc["E"].shape[1])
    out = {}
    for K in Ks:
        suf = np.array(list(itertools.product(range(V), repeat=int(K))), dtype=np.int64)
        a = _forward(proc, suf)
        P = a.sum(axis=1)
        b = a / P[:, None]
        m = b @ proc["features"]
        q = ho.predictive(b, proc["T"], proc["E"])
        out[int(K)] = {
            "E_m_sq": float(P @ np.sum(m * m, axis=1)),
            "E_Hq": float(P @ ho.entropy_rows(q)),
            "n_suffixes": int(V**K),
        }
    return out


# ------------------------------------------------------------------------------ spot checks


def decimal_spot_check(proc, tok, Ks) -> dict:
    if int(proc["W"]) != 12:
        raise ValueError("the Decimal spot check uses the 12-gon features (W = 12 only)")
    T, E, pi = proc["T"], proc["E"], proc["pi"]
    refs = error_bound.reference_moments(T, E, pi, proc["coords"], tok, tuple(Ks))
    m = oracle_profile.posterior_means(T, E, pi, tok, tuple(Ks), proc["features"])
    gap = Fraction(0)
    for i, ref in enumerate(refs):
        for K in Ks:
            for j in (0, 1):
                gap = max(gap, abs(Fraction(float(m[int(K)][i, j])) - Fraction(ref[int(K)][j])))
    return {"max_gap": str(gap), "pass": gap <= error_bound.MOMENT_TOL_EXACT}


def bayes_cross_check(proc, tok) -> dict:
    lh = int(np.asarray(tok).shape[1])
    a = BayesFilter(proc["T"], proc["E"], proc["pi"]).belief_at(tok, lh)
    b = oracle_profile.suffix_posterior(proc["T"], proc["E"], proc["pi"], tok, lh)
    mx = float(np.max(np.abs(np.asarray(a) - b)))
    return {"max_abs": mx, "pass": mx <= 1e-12}


def law_bound_report(proc, enclosure=None) -> dict:
    """Tier-0 report only (§8, RC-3); never changes eligibility, ranking or selection."""
    law = process_law.LAW
    saved = (law["sigma"], law["neighbour"])
    try:
        law["sigma"] = Fraction(proc["sigma"])
        law["neighbour"] = (1 - Fraction(proc["p"])) / 4
        fn = enclosure or process_law.process_law_bound
        return fn(proc["T"], proc["E"], proc["pi"], proc["coords"])
    except decimal.Inexact as exc:
        return {"status": "UNAVAILABLE/NONTERMINATING_LOGIT", "reason": f"decimal.Inexact: {exc}"}
    finally:
        law["sigma"], law["neighbour"] = saved


# ------------------------------------------------------------------------------------- KC1


def _read(path) -> tuple:
    p = Path(path)
    if p.suffix.lower() != ".json":
        raise hw.HwsStop(KC1, f"read_json refuses a non-JSON path: {p}")
    data = p.read_bytes()
    JSON_READS.append(str(path))
    return data, json.loads(data.decode("utf-8"))


def read_json(path) -> object:
    return _read(path)[1]


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _rebuild(kind, seed=None):
    world = hw.build_world(12)
    if kind == "WorldSpec":
        return world, None
    if kind == "TransitionSpec":
        return hw.build_transition(world, Fraction(1, 5)), None
    tree = SeedTree(int(seed))
    spec = OverlapGaussian().build(world, EmissionConfig("overlap", 36, 1.25, "grid"), tree)
    return spec, tree


def expected_envelope(kind, seed=None, world_id=None) -> dict:
    """KC1 (d): the serialization envelope of ProcessStage, reconstructed without a loader."""
    if kind == "WorldSpec":
        return {
            "config": asdict(WorldConfig("cylinder", (12, 12), "flat")),
            "parent_ids": [],
            "seed_map": {},
        }
    if kind == "TransitionSpec":
        return {
            "config": asdict(TransitionConfig(p_stay=0.2)),
            "parent_ids": [world_id],
            "seed_map": {},
        }
    _, tree = _rebuild(kind, seed)
    world_tree = SeedTree(0)
    world_tree.seed("centers", "cylinder")
    seed_map = dict(tree.issued)
    seed_map.update({f"world_scope/{k}": v for k, v in world_tree.issued.items()})
    cfg = dict(
        asdict(EmissionConfig("overlap", 36, 1.25, "grid")),
        replicate=int(seed),
        world_scope_master=0,
    )
    return {"config": cfg, "parent_ids": [world_id], "seed_map": seed_map}


def _same(a, b) -> bool:
    return canonical_json(a) == canonical_json(b)


def _check_artifact(root, name, env, manifest, seed) -> dict:
    kind, aid = name.split("/")
    checks, diff = {}, []
    entry = manifest.get("artifacts", {}).get(name)
    checks["manifest_entry"] = isinstance(entry, dict)
    meta_bytes, meta = _read(Path(root) / kind / aid / "meta.json")
    checks["meta_sha256"] = bool(entry) and _sha(meta_bytes) == entry.get("meta_sha256")
    checks["status_complete"] = meta.get("status") == "complete"
    checks["artifact_type"] = meta.get("artifact_type") == kind
    checks["artifact_id"] = meta.get("artifact_id") == aid
    checks["config"] = _same(meta.get("config"), env["config"])
    checks["recomputed_id"] = (
        make_artifact_id(
            kind,
            meta.get("config", {}),
            list(meta.get("parent_ids", [])),
            meta.get("schema_version", ""),
        )
        == aid
    )
    checks["parent_ids"] = list(meta.get("parent_ids", [])) == list(env["parent_ids"])
    checks["seed_map"] = _same(meta.get("seed_map"), env["seed_map"])
    _, extra = _read(Path(root) / kind / aid / "extra.json")
    spec = _rebuild(kind, seed)[0]
    arrays, rebuilt_extra = spec.to_payload()
    content = payload_checksum(arrays, extra)
    checks["content_meta"] = content == meta.get("payload_sha256")
    checks["content_manifest"] = bool(entry) and content == entry.get("sha256")
    for field in sorted(set(extra) | set(rebuilt_extra)):
        if not _same(extra.get(field), rebuilt_extra.get(field)):
            diff.append(field)
    return {"checks": checks, "extra_diff": diff}


def kc1_identity(artifact_root, manifest_path, config_json_path, seeds=(1729, 2718, 3141)) -> dict:
    """§3 KC1 (a)-(d) with JSON reads only; a failure is returned, never raised (erratum E11)."""
    reads_before = len(JSON_READS)
    cfg_bytes, cfg = _read(config_json_path)
    man_bytes, manifest = _read(manifest_path)
    top = {
        "manifest_sha256": _sha(man_bytes)
        == cfg.get("inputs_sha256", {}).get("INPUT_IDENTITIES.json")
    }
    wid = make_artifact_id("WorldSpec", expected_envelope("WorldSpec")["config"], [])
    envs = {f"WorldSpec/{wid}": (expected_envelope("WorldSpec"), None)}
    t_env = expected_envelope("TransitionSpec", world_id=wid)
    envs[f"TransitionSpec/{make_artifact_id('TransitionSpec', t_env['config'], [wid])}"] = (
        t_env,
        None,
    )
    for s in seeds:
        e_env = expected_envelope("EmissionSpec", seed=s, world_id=wid)
        envs[f"EmissionSpec/{make_artifact_id('EmissionSpec', e_env['config'], [wid])}"] = (
            e_env,
            s,
        )
    arts = {
        name: _check_artifact(artifact_root, name, env, manifest, seed)
        for name, (env, seed) in envs.items()
    }
    ok = all(top.values()) and all(all(a["checks"].values()) for a in arts.values())
    return {
        "status": "PASS" if ok else KC1,
        "top": top,
        "artifacts": arts,
        "config_json_sha256": _sha(cfg_bytes),
        "json_reads": JSON_READS[reads_before:],
    }
