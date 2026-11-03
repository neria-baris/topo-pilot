"""HWSG WORLD_HANDOFF: build, write, load, view for stage-C functions (API.md §3; protocol §2.6)."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import k4b_cert
import stage_records
from c1_records import C1GateFailure

IDENT = "FAIL_TECHNICAL/IDENTITY"
FILE = gc.CONTRACT["handoff"]["file"]


def build(w, o_result) -> dict:
    d = gc.world(w)
    law, ident = o_result["law"], o_result["identity"]
    return {"key": d.key, "sigma": str(d.sigma), "p": str(d.p), "neighbour": str(d.neighbour),
            "Z_bound": str(law["Z_bound"]), "F_plan": str(law["F_plan"]),
            "p_D2a": float(o_result["p_D2a"]), "N_C": gc.N_C, "model_count": gc.MODEL_COUNT,
            "process_identities": json.loads(json.dumps(ident, default=str)),
            "exclusions": list(gc.exclusions()), "protocol_sha256": gc.PROTOCOL_SHA}


def write(world_dir, handoff) -> str:
    path = Path(world_dir) / FILE
    stage_records.write_new(path, handoff)
    return stage_records.sha256(path)


def _recorded_sha(store, d):
    f = Path(store) / "STAGES.jsonl"
    if not f.is_file():
        return None
    found = None
    rel = f"worlds/{d.key}/{FILE}"
    for line in f.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        if e.get("event") == "STAGE_COMPLETE" and e.get("stage") == "O":
            found = e.get("files", {}).get(rel, found)
    return found


def load(w, store=None, expected_sha256=None) -> dict:
    d = gc.world(w)
    store = gc.STORE if store is None else store
    path = gc.world_dir(store, d.tag) / FILE
    want = expected_sha256 if expected_sha256 is not None else _recorded_sha(store, d)
    if want is None:
        raise C1GateFailure(IDENT, "no recorded WORLD_HANDOFF sha256")
    data = gc.guard(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != want:
        raise C1GateFailure(IDENT, "WORLD_HANDOFF.json sha256 differs")
    h = gc.CONTRACT["handoff"]
    try:
        obj = json.loads(data.decode("utf-8"))
    except ValueError as exc:
        raise C1GateFailure(IDENT, f"WORLD_HANDOFF.json: {exc!r}") from exc
    if not isinstance(obj, dict) or set(obj) != set(h["keys"]):
        raise C1GateFailure(IDENT, "WORLD_HANDOFF key set differs")
    bad = _forbidden(obj, set(h["forbidden_keys"]))
    if bad:
        raise C1GateFailure(IDENT, f"WORLD_HANDOFF forbidden keys {bad}")
    out = dict(obj)
    for k in h["fraction_keys"]:
        out[k] = Fraction(str(obj[k]))
    for k in h["int_keys"]:
        out[k] = int(obj[k])
    out["p_D2a"] = float(obj["p_D2a"])
    out["exclusions"] = tuple(str(x) for x in obj["exclusions"])
    if out["key"] != d.key:
        raise C1GateFailure(IDENT, "WORLD_HANDOFF key differs from the world")
    if out["neighbour"] != (1 - out["p"]) / 4:
        raise C1GateFailure(IDENT, "neighbour != (1 - p)/4")
    if out["F_plan"] != k4b_cert.F_plan(out["Z_bound"]):
        raise C1GateFailure(IDENT, "F_plan != F_plan(Z_bound)")
    return out


def _forbidden(obj, names) -> list:
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in names:
                out.append(k)
            out += _forbidden(v, names)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            out += _forbidden(v, names)
    return out


def as_hwsc(h) -> dict:
    n = int(h["N_C"])
    return {"Z_bound": h["Z_bound"], "F_plan": h["F_plan"], "p_D2a": h["p_D2a"], "N_C": n,
            "k_C": 1, "model_count": int(h["model_count"]),
            "stage_c_exclusions": tuple(h["exclusions"]),
            "registry_value": (10240 + n) * Fraction(h["p_D2a"])}


def loader(key):
    """Function with the hwsc_config.load_handoff signature returning the stage-C view."""
    d = gc.world(key)

    def load_handoff(path=None, expected_sha256=None):
        store = gc.STORE if path is None else Path(path).parent.parent.parent
        return as_hwsc(load(d.tag, store, expected_sha256))

    return load_handoff
