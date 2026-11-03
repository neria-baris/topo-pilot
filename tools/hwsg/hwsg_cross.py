"""HWSG cross-world readings: generality, annotations, capture, similarity, licences (API.md §8;
protocol §2.7, §7.1 X, §7.4). Inputs are the sha256-bound RESULT.json files of the worlds."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import json
from fractions import Fraction
from pathlib import Path

import c1_means
import numpy as np
import stage_records
from c1_records import C1GateFailure

LINEAGE, NUM = "FAIL_TECHNICAL/LINEAGE", "FAIL_TECHNICAL/NUMERICAL"
LIC = gc.CONTRACT["licences"]
CROSS = gc.CONTRACT["cross"]


def _bound_sha(wd, rel):
    found = None
    for e in stage_records.stages_so_far(wd):
        if e.get("event") == "STAGE_COMPLETE" and rel in e.get("files", {}):
            found = e["files"][rel]
    return found


def load_world(store, w) -> dict:
    d = gc.world(w)
    wd = gc.world_dir(store, d.tag)
    s8, term = wd / "stages/S8/RESULT.json", wd / "stages/TERMINAL/RESULT.json"
    endpoint = s8.is_file()
    path = s8 if endpoint else term
    if not path.is_file():
        raise C1GateFailure(LINEAGE, f"world {d.tag} has neither an S8 nor a TERMINAL RESULT")
    rel = path.relative_to(wd).as_posix()
    if _bound_sha(wd, rel) != stage_records.sha256(path):
        raise C1GateFailure(LINEAGE, f"{rel} of {d.tag} is not bound by its STAGE_COMPLETE")
    res = json.loads(path.read_text(encoding="utf-8"))
    ratio, draws = None, None
    if endpoint:
        files = {}
        for name in ("RATIO.json", "RATIO_DRAWS.npz"):
            f = wd / "stages/S8" / name
            if f.is_file():
                if _bound_sha(wd, f.relative_to(wd).as_posix()) != stage_records.sha256(f):
                    raise C1GateFailure(LINEAGE, f"{name} of {d.tag} is not bound")
                files[name] = f
        if "RATIO.json" in files:
            ratio = json.loads(files["RATIO.json"].read_text(encoding="utf-8"))
        if "RATIO_DRAWS.npz" in files:
            with np.load(files["RATIO_DRAWS.npz"], allow_pickle=False) as z:
                draws = {k[len("rho_minus_"):]: np.asarray(z[k]) for k in z.files}
    per = res.get("per_model") or {}
    return {"tag": d.tag, "outcome": res["outcome"], "endpoint": endpoint,
            "p1_passed": True if endpoint else bool(res.get("p1_passed")),
            "per_model_status": {str(j): p.get("status") for j, p in per.items()},
            "per_model": per, "ratio": ratio, "rho_draws": draws}


def general(worlds) -> dict:
    tags = [w["tag"] for w in worlds]
    if len(worlds) == 3 and all(w["outcome"] == "SUPPORT" for w in worlds):
        return {"reading": "GENERAL", "worlds": tags}
    ex = {w["tag"]: sorted(j for j, s in w["per_model_status"].items() if s == "EXCLUDE")
          for w in worlds if w["p1_passed"] and w["endpoint"]}
    ex = {t: m for t, m in ex.items() if m}
    if ex:
        return {"reading": "NOT_GENERAL", "worlds": sorted(ex), "models": ex}
    return {"reading": "GENERAL_UNAVAILABLE",
            "reasons": {w["tag"]: w["outcome"] for w in worlds}}


def _ep(worlds) -> list:
    return [w for w in worlds if w["endpoint"]]


def annotations(worlds) -> list:
    ep, out = _ep(worlds), []
    if len(ep) >= 2 and all(w["outcome"] == "EXCLUSION" for w in ep):
        out.append("ALL_EXCLUSION")
    if ep and all(Fraction(float(p["L"])) - Fraction(str(p["F_minus"])) > 0
                  for w in ep for p in w["per_model"].values()):
        out.append("POSITIVE_EVERYWHERE")
    return out


def _models(w) -> dict:
    return (w["ratio"] or {}).get("per_model", {}) if w["ratio"] else {}


def capture(worlds) -> dict:
    ep = _ep(worlds)
    models = {(w["tag"], j): _models(w).get(j, {"status": "RATIO_UNRESOLVED"})
              for w in ep for j in w["per_model"]}
    out = {"worlds_covered": [w["tag"] for w in ep], "n_models": len(models),
           "unavailable": [t for t in gc.TAGS if t not in {w["tag"] for w in ep}]}
    defined = {k: m for k, m in models.items() if m.get("status") == "DEFINED"}
    out["unavailable"] += [f"{t}:{j}" for (t, j), m in models.items() if (t, j) not in defined]
    if len(ep) < 2:
        return dict(out, reading="CAPTURE_UNAVAILABLE")
    half = gc.CAPTURE_FLOOR
    if any(Fraction(float(m["rhoU"])) < half for m in defined.values()):
        return dict(out, reading="CAPTURE_BELOW_HALF")
    if models and len(defined) == len(models) and all(
            Fraction(float(m["rhoL"])) >= half for m in defined.values()):
        return dict(out, reading="CAPTURE_AT_LEAST_HALF")
    return dict(out, reading="CAPTURE_UNRESOLVED")


def similarity(worlds, seed=None) -> dict:
    seed = gc.CROSS_SEED if seed is None else seed
    ep = [w for w in _ep(worlds) if w["ratio"] and w["rho_draws"]]
    dm = {(w["tag"], j): m for w in ep for j, m in _models(w).items()
          if m.get("status") == "DEFINED"}
    if not dm:
        return {"reading": "SIMILARITY_UNAVAILABLE", "compatible": None, "spread": None,
                "spread_bound": None, "rho_bar": {}}
    lo = max(m["central95_minus"][0] for m in dm.values())
    hi = min(m["central95_minus"][1] for m in dm.values())
    rho_bar, bar_draws = {}, {}
    for w in ep:
        js = [j for j in w["rho_draws"] if (w["tag"], j) in dm]
        if js:
            rho_bar[w["tag"]] = float(c1_means.tree_mean(
                np.array([dm[(w["tag"], j)]["rho"] for j in js])))
            bar_draws[w["tag"]] = np.mean([w["rho_draws"][j] for j in js], axis=0)
    out = {"reading": "SIMILARITY", "compatible": bool(lo <= hi), "common_interval": [lo, hi],
           "rho_bar": rho_bar, "spread": None, "spread_bound": None}
    if len(rho_bar) >= 2:
        g = np.random.Generator(np.random.PCG64(int(seed)))
        n = gc.DRAWS
        v = [bar_draws[t][g.permutation(n)] for t in gc.TAGS if t in bar_draws]
        s_star = np.max(v, axis=0) - np.min(v, axis=0)
        val, k = c1_means.quantile_with_rank(s_star, 1 - float(gc.ALPHA))
        if k != gc.RANKS["one_minus_alpha"] or not c1_means.rank_check(s_star, val, k):
            raise C1GateFailure(NUM, f"spread rank check failed (rank {k})")
        out["spread"] = float(max(rho_bar.values()) - min(rho_bar.values()))
        out["spread_bound"] = float(val)
    return out


def licence(reading, fill=None) -> str:
    name = reading.get("reading") if isinstance(reading, dict) else str(reading)
    if isinstance(reading, dict):
        fill = dict(reading, **(fill or {}))
    f = _Fill(fill or {})
    for k in ("worlds", "models", "unavailable"):
        if isinstance(f.get(k), (list, tuple)):
            f[k] = ", ".join(map(str, f[k]))
        elif isinstance(f.get(k), dict):
            f[k] = "; ".join(f"{t}: {', '.join(map(str, m))}" for t, m in f[k].items())
    if name == "SIMILARITY" or name == "SIMILARITY_UNAVAILABLE":
        f["compatible"] = "compatible" if (fill or {}).get("compatible") else "not compatible"
        name = "SIMILARITY"
    if isinstance(f.get("reasons"), dict):
        f["reasons"] = "; ".join(f"{t} {o}" for t, o in f["reasons"].items())
    if name not in LIC:
        return ""
    text = LIC[name].format_map(f)
    if name == "NOT_GENERAL":
        text += " " + CROSS["error_statements"]["NOT_GENERAL"]
    return text


class _Fill(dict):
    def __missing__(self, key):
        return "n/a"


def run_cross(out, auth, sched, job) -> dict:
    import hwsg_records as rec
    import k4b_driver

    out = Path(out)
    pf = rec.preflight(out, "CROSS", auth, sched)
    if pf.get("refused"):
        return pf
    try:
        worlds = [load_world(out, t) for t in gc.TAGS]
        gen, ann, cap, sim = general(worlds), annotations(worlds), capture(worlds), \
            similarity(worlds)
    except Exception as exc:  # noqa: BLE001
        status = rec.status_of(exc)
        stage_records.record_gate(out, "CROSS", status, reason=str(exc)[:2000])
        return {"status": status}
    lic = {"general": licence(gen, {"n": len(worlds)}),
           "capture": licence(cap, {"n": cap["n_models"]}), "similarity": licence(sim)}
    body = {"worlds": {w["tag"]: w["outcome"] for w in worlds}, "general": gen,
            "annotations": ann, "capture": cap, "similarity": sim, "licences": lic,
            "error_statements": CROSS["error_statements"], "disclosure": gc.DISCLOSURE,
            "does_not_establish": LIC["does_not_establish"],
            "w_star_context": "descriptive only"}
    f = out / "stages" / "CROSS" / "CROSS.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(f, json.loads(json.dumps(body, default=str)))
    k4b_driver.complete_stage(out, "CROSS", [f])
    stage_records.record_gate(out, "CROSS", "PASS")
    return dict(body, status="PASS")
