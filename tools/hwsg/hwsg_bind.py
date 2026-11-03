"""HWSG world rebinding and audit (API.md §2; protocol §2.3). No existing file is edited: the
HWSB/HWSC/K4b module attributes are rebound inside `world(w)` and restored in `finally`."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import dataclasses
import importlib
import sys
from contextlib import contextmanager
from fractions import Fraction
from pathlib import Path

import hwsb_config
import hwsc_bind
import hwsc_config
import hwsc_data
from c1_records import C1GateFailure

BAD = "FAIL_TECHNICAL/BINDING"
ACTIVE = None
_ROWS = [tuple(r.split(".", 1)) for r in gc.CONTRACT["binding"]["rows_per_world"]]
_IMPORT_VALUES = {(m, n): getattr(importlib.import_module(m), n) for m, n in _ROWS}


def _values(d, store_dir, dry_case=None) -> dict:
    import hwsg_handoff
    import hwsg_oracle

    led, key = gc.STUDY_LEDGER, d.key
    plan = gc.plan(d.tag)
    v = {
        ("hwsb_config", "SCOPE"): gc.SCOPE, ("hwsb_config", "KEY"): key,
        ("hwsb_config", "PROCESS"): d.process, ("hwsb_config", "MASTERS"): d.masters,
        ("hwsb_config", "SIGMA"): d.sigma, ("hwsb_config", "NEIGHBOUR"): d.neighbour,
        ("hwsb_config", "TRANS_CFG"): d.transition_cfg, ("hwsb_config", "EMIS_CFG"): d.emission_cfg,
        ("hwsb_config", "STORE"): store_dir, ("hwsb_config", "STUDY_LEDGER"): led,
        ("hwsb_config", "REAL_PLAN"): plan,
        ("hwsc_config", "SCOPE"): gc.SCOPE, ("hwsc_config", "KEY"): key,
        ("hwsc_config", "PROCESS"): d.process, ("hwsc_config", "MASTERS"): d.masters,
        ("hwsc_config", "SEEDS"): dict(d.seeds), ("hwsc_config", "P1C_SEEDS"): d.p1_seeds,
        ("hwsc_config", "SIGMA"): d.sigma, ("hwsc_config", "NEIGHBOUR"): d.neighbour,
        ("hwsc_config", "STORE"): store_dir, ("hwsc_config", "DRY_STORE"): gc.DRY_STORE,
        ("hwsc_config", "STUDY_LEDGER"): led,
        ("hwsc_config", "HANDOFF_PATH"): store_dir / "WORLD_HANDOFF.json",
        ("hwsc_config", "HWSC_PLAN"): plan,
        ("hwsc_config", "RESERVATION_ID"): d.reservation_id,
        ("hwsc_config", "DISCLOSURE"): gc.DISCLOSURE,
        ("hwsc_config", "load_handoff"): hwsg_handoff.loader(key),
        ("hwsc_data", "build_process_c"): hwsg_oracle.process_builder(key),
        ("hwsc_data", "process_identity"): hwsg_oracle.identity_checker(key),
    }
    if dry_case is not None:
        dm, case = gc.DRY_MASTERS[d.tag], f"hwsg-v1/DRY/{dry_case}/{d.tag}"
        v.update({("hwsb_config", "MASTERS"): dm, ("hwsc_config", "MASTERS"): dm,
                  ("hwsb_config", "SCOPE"): case, ("hwsc_config", "SCOPE"): case,
                  ("hwsc_config", "SEEDS"): dict(gc.DRY_SEEDS),
                  ("hwsc_config", "P1C_SEEDS"): (gc.DRY_SEEDS["val_sd"],
                                                 gc.DRY_SEEDS["val_projection"]),
                  ("hwsb_config", "REAL_PLAN"): gc.dry_plan(d.tag, dry_case),
                  ("hwsc_config", "HWSC_PLAN"): gc.dry_plan(d.tag, dry_case)})
    return v


def rows(w, dry_case=None) -> list:
    d = gc.world(w)
    store_dir = (gc.DRY_STORE / dry_case / d.tag) if dry_case is not None else \
        gc.world_dir(gc.STORE, d.tag)
    new = _values(d, store_dir, dry_case)
    return [{"module": m, "name": n, "old": _IMPORT_VALUES[(m, n)], "new": new[(m, n)]}
            for m, n in _ROWS]


def stage_c_table(w, dry_case=None) -> list:
    d = gc.world(w)
    key = d.key
    masters = gc.DRY_MASTERS[d.tag] if dry_case is not None else d.masters
    seeds = dict(gc.DRY_SEEDS if dry_case is not None else d.seeds)
    scope = f"hwsg-v1/DRY/{dry_case}/{d.tag}" if dry_case is not None else "hwsg-v1/" + key
    wdir = (gc.DRY_STORE / dry_case / d.tag) if dry_case is not None else \
        gc.world_dir(gc.STORE, d.tag)
    out = []
    for r in hwsc_bind.load_table():
        m, n = r["module"], r["name"]
        if m == "hwsb_config":
            continue
        new = r["new"]
        if m.startswith("k4b_") and n == "MODELS":
            new = tuple(masters)
        elif m.startswith("k4b_") and n == "SCOPE":
            new = scope
        elif m.startswith("k4b_") and n == "PROCESS":
            new = d.process
        elif m.startswith("k4b_") and n == "SEEDS":
            new = dict(seeds)
        elif (m, n) == ("k4b_config", "STORE"):
            new = wdir
        elif (m, n) == ("k4b_driver", "ARTIFACTS"):
            new = wdir / "artifacts"
        elif (m, n) == ("k4b_config", "CONTRACT"):
            new = gc.k4b_view()
        elif (m, n) == ("k4b_config", "CONTRACT_PATH"):
            new = gc.CONTRACT_PATH
        elif (m, n) == ("k4b_config", "PROTOCOL_PATH"):
            new = gc.PROTOCOL_PATH
        out.append(dict(r, new=new))
    return out


@contextmanager
def world(w, dry_case=None):
    global ACTIVE
    d = gc.world(w)
    if ACTIVE is not None:
        raise C1GateFailure(BAD, "nested world binding")
    if hwsc_bind.ACTIVE:
        raise C1GateFailure(BAD, "stage-C binding already active")
    rs = rows(d.tag, dry_case)
    drift = [f"{r['module']}.{r['name']}" for r in rs
             if getattr(importlib.import_module(r["module"]), r["name"]) is not r["old"]]
    if drift:
        raise C1GateFailure(BAD, f"code drift: {drift}")
    saved = []
    ACTIVE = d.tag
    try:
        for r in rs:
            mod = importlib.import_module(r["module"])
            saved.append((mod, r["name"], getattr(mod, r["name"])))
            setattr(mod, r["name"], r["new"])
        with hwsc_bind.bound_stage_c(stage_c_table(d.tag, dry_case)) as info:
            yield {"tag": d.tag, "key": d.key, "rows": len(rs),
                   "table_sha256": info["table_sha256"], "stage_c": info}
    finally:
        for mod, name, obj in reversed(saved):
            setattr(mod, name, obj)
        ACTIVE = None


# ------------------------------------------------------------------------------------- audit
class _Forbidden:
    def __init__(self, f, own_floats=(), own_fractions=()):
        self.floats = {float(x) for x in f["floats"]} - set(own_floats)
        self.fractions = {Fraction(x) for x in f["fractions"]} - set(own_fractions)
        self.strings, self.ints = set(f["strings"]), {int(i) for i in f["ints"]}
        self.tuples = [tuple(t) for t in f["tuples"]]
        self.paths = {hwsc_bind._norm(p) for p in f["paths"]}

    def hit(self, v):
        if isinstance(v, bool):
            return None
        if isinstance(v, int) and v in self.ints:
            return f"int {v}"
        if isinstance(v, float) and v in self.floats:
            return f"float {v}"
        if isinstance(v, Fraction) and v in self.fractions:
            return f"fraction {v}"
        if isinstance(v, str):
            if v in self.strings:
                return f"str {v}"
            if hwsc_bind._norm(v) in self.paths:
                return f"path {v}"
        if isinstance(v, Path) and hwsc_bind._norm(v.as_posix()) in self.paths:
            return f"path {v}"
        if isinstance(v, tuple) and v in self.tuples:
            return f"tuple {v}"
        return None


def scope_modules() -> list:
    dirs = [(gc.REPO / d).resolve() for d in gc.CONTRACT["binding"]["audit"]["module_dirs"]]
    out = []
    for mod in list(sys.modules.values()):
        f = getattr(mod, "__file__", None)
        if f and Path(f).resolve().parent in dirs:
            out.append(mod)
    return sorted(out, key=lambda m: m.__name__)


def audit(w, modules=None, left_unchanged=None) -> dict:
    import types

    d = gc.world(w)
    a = gc.CONTRACT["binding"]["audit"]
    own_f = {float(d.p_float)} if d.p == Fraction(1, 5) else set()
    own_fr = {d.p} if d.p == Fraction(1, 5) else set()
    forb = _Forbidden(a["w_star_forbidden"], own_f, own_fr)
    mods = scope_modules() if modules is None else list(modules)
    left = left_unchanged if left_unchanged is not None else a["left_unchanged"]
    allowed = {(r["module"], r["name"]) for r in left} if isinstance(left, list) else set()
    hits = []
    for mod in mods:
        for name, v in list(vars(mod).items()):
            if (name.startswith("__") and name.endswith("__")) or isinstance(v, types.ModuleType):
                continue
            if callable(v) and not dataclasses.is_dataclass(v):
                continue
            found = []
            hwsc_bind._walk(v, name, forb, found)
            hits += [{"module": mod.__name__, "where": x, "kind": "global", "hit": h,
                      "top": name} for x, h in found]
        for qual, fn in hwsc_bind._functions(mod):
            for attr in ("__defaults__", "__kwdefaults__"):
                found = []
                hwsc_bind._walk(getattr(fn, attr) or (), f"{qual}.{attr}", forb, found)
                hits += [{"module": mod.__name__, "where": x, "kind": "default", "hit": h,
                          "top": f"{qual}.{attr}"} for x, h in found]
    unlisted = [h for h in hits if (h["module"], h["top"]) not in allowed]
    return {"status": "PASS" if not unlisted else BAD, "hits": hits, "unlisted": unlisted,
            "modules": [m.__name__ for m in mods], "n_hits": len(hits)}


_REQUIRED = {"ladder_pilot": ("models", "seeds", "ladder"),
             "law_bound": ("sigma", "neighbour"),
             "build_process": ("emission_cfg", "world_cfg", "transition_cfg")}


def check_explicit(fn_name, kwargs) -> None:
    need = _REQUIRED.get(str(fn_name).rsplit(".", 1)[-1], ())
    missing = [k for k in need if kwargs.get(k) is None]
    if missing:
        raise C1GateFailure(BAD, f"{fn_name} called without explicit {missing}")


_ = hwsb_config, hwsc_config, hwsc_data  # attributes are rebound by name through importlib
