"""HWSC type rule for the stage-C dry stores `hwsc-dry*` (defect D-0178-1; API.md §22).

Each metered dry run writes a new store, so the frozen R6 table cannot list its files one by
one. Instead every file that scratch_scan lists under a `hwsc-dry*` top-level folder (and only
there) must match exactly one class derived from what hwsc_dry.run_dry writes; anything else
fails closed. Classes: R5 (read and digested by source_dry), c2scratch (a C2-format table read by
the C2ND scratch reader), CHECKPOINT, REGISTRY_FIXTURE (digest sets, non-history),
PLANTED_FIXTURE (the planted byte fixtures of DRC9 and DRC11, matched by sha256)."""

from __future__ import annotations  # noqa: I001

import hwsc_config as cc
import json
import re
from pathlib import Path

import numpy as np
import stage_records
import x6s1_registry

PREFIX = "hwsc-dry"
RULE = cc.CONTRACT["registry"]["dry_stores"]["type_rule"]
PLANTED = {p["sha256"]: p for p in RULE["planted"]}
_CASE, _UTC = re.compile(r"DRC\d+"), re.compile(r"\d{8}T\d{6}Z")
_RUN = re.compile(r"run_\d{5}\.npy")
_ARTS = ("WorldSpec", "TransitionSpec", "EmissionSpec", "Checkpoint", "ObservationSet")


def is_dry_store(name) -> bool:
    return str(name).startswith(PREFIX)


def _meta(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


def _os_parent_ok(os_dir) -> bool:
    """An ObservationSet whose single EmissionSpec parent lies in the same artifacts dir."""
    meta = _meta(Path(os_dir) / "meta.json") or {}
    arts = Path(os_dir).parent.parent
    ems = [p for p in meta.get("parent_ids", [])
           if (_meta(arts / "EmissionSpec" / p / "meta.json") or {}).get("artifact_type")
           == "EmissionSpec"]
    return len(ems) == 1


def _heads(f) -> dict:
    return {k: (dt, tuple(sh)) for k, dt, sh in x6s1_registry._headers(f)}


def _registry_npz(f) -> bool:
    h = _heads(f)
    return set(h) == {"digests", "seq_ids"} and h["digests"][0].kind == "U"


def _digest_run(f) -> bool:
    h = _heads(f)
    dt, sh = h[""]
    return dt == np.uint8 and len(sh) == 2 and sh[1] == 32


def _c2_table(f) -> bool:
    h = _heads(f)
    return all(k in h and h[k][0].kind == "U" for k in ("digest_H", "digest_Hp", "digest_Hm"))


def _tokens(f) -> bool:
    h = _heads(f)
    return "canon32" in h and h["canon32"][0].kind in "iu" and h["canon32"][1][-1] == 32


def dry_class(store, rel, rec):
    """The class of one listed file of a hwsc-dry* store, or None (fails closed)."""
    store, parts = Path(store), rel.split("/")
    if len(parts) < 3 or not _CASE.fullmatch(parts[0]) or not _UTC.fullmatch(parts[1]):
        return _planted(store / rel, parts)
    f, tail, case, cls = store / rel, parts[2:], parts[0], rec["class"]
    try:
        if len(tail) == 4 and tail[0] == "artifacts" and tail[1] in _ARTS:
            if tail[1] == "Checkpoint" and tail[3] == "state.pt" and cls == "pt":
                return "CHECKPOINT"
            if tail[1] == "ObservationSet" and tail[3] in ("meta.json", "payload.npz") and \
                    cls in ("os_root", "history") and _os_parent_ok(f.parent):
                return "R5"
            return None
        if cls == "history" and len(tail) == 3 and tail[0] == "stages" and \
                tail[1] in ("S3", "S7") and f.name.startswith("DRYHIST_") and _tokens(f):
            return "R5"
        if cls == "history" and tail[-2:-1] == ["registry"] and re.fullmatch(
                r"K-REG[12]_digests\.npz", f.name) and _registry_npz(f):
            return "REGISTRY_FIXTURE"
        if cls == "history" and _RUN.fullmatch(f.name) and (
                (case == "DRC9" and tail[:-1] == ["scale"]) or
                (len(tail) == 4 and tail[:2] == ["registry", "runs"])) and _digest_run(f):
            return "REGISTRY_FIXTURE"
        if case == "DRC9" and tail[0] in ("syn", "syn2") and cls == "history":
            if f.name.startswith("HIST_") and _c2_table(f):
                return "c2scratch"
            if _tokens(f):
                return "R5"
    except Exception:  # noqa: BLE001  an unreadable header is not an allowed class
        return _planted(f, parts)
    return _planted(f, parts)


def _planted(f, parts):
    try:
        p = PLANTED.get(stage_records.sha256(f))
    except OSError:
        return None
    if p and parts[0] == p["case"] and Path(f).name == p["name"] and \
            Path(f).stat().st_size == p["bytes"]:
        return "PLANTED_FIXTURE"
    return None


def check_store(store, listed, ok_tags, out) -> None:
    """scratch_check for one hwsc-dry* store: every listed file needs an allowed class."""
    for rel, rec in listed.items():
        cls = dry_class(store, rel, rec)
        where = f"{Path(store).name}/{rel}"
        if cls is None:
            out["other"].append({"path": where, "reason": "not allowed by the hwsc-dry type "
                                 "rule (D-0178-1)"})
        elif cls in ("R5", "c2scratch") and cls not in ok_tags:
            out["other"].append({"path": where, "reason": f"reader {cls} not PASS"})
