"""HWSU needle search, hit classification, namespace overlap and G0-OF (API.md §6; protocol §4.2
OF-0; RC-3, J3, J5, J9, J10)."""

from __future__ import annotations  # noqa: I001

import hwsu_config as uc
import hwsu_records as ur
import json
import os
import re
from pathlib import Path

import hwsb_known
import stage_records
from c1_records import C1GateFailure

TEXT_SUFFIXES = (".json", ".jsonl", ".md", ".py", ".txt", ".yaml")
SKIP_DIRS = {".git", ".venv", "__pycache__", "sealed"}
AUTHORITY, SEED_SCOPE = "INCONCLUSIVE/AUTHORITY", "FAIL_TECHNICAL/SEED_SCOPE"


def _skip_dir(parent, name, groot) -> bool:
    low = name.lower()
    docs = low == "research_summary" and parent.name.lower() == "docs"
    return (name in SKIP_DIRS or low.startswith("00_read_me_first") or docs
            or uc.blinded(parent / name, groot))


def _line_matcher(needles):
    # R-0200-1: per line, one whole-token regex pass finds every digit needle (the
    # hwsc_known.needle_in rule: no [0-9A-Za-z_] on either side) and a plain substring test serves
    # every other needle, so the hits equal [nd for nd in needles if needle_in(nd, line)].
    digits = sorted({nd for nd in needles if nd.isdigit()}, key=len, reverse=True)
    rx = re.compile(r"(?<![0-9A-Za-z_])(?:" + "|".join(map(re.escape, digits))
                    + r")(?![0-9A-Za-z_])") if digits else None

    def found(line) -> list:
        dig = set(rx.findall(line)) if rx else set()
        return [nd for nd in needles if (nd in dig if nd.isdigit() else nd in line)]
    return found


def seed_search_u(root, needles, root_for_guard=None) -> list:
    groot, hits = Path(root_for_guard or root), []
    match = _line_matcher(needles)
    for folder, dirs, files in os.walk(root, topdown=True):
        here = Path(folder)
        dirs[:] = sorted(d for d in dirs if not _skip_dir(here, d, groot))
        for name in sorted(files):
            low = name.lower()
            if low.startswith("00_read_me_first") or not low.endswith(TEXT_SUFFIXES):
                continue
            if uc.blinded(here / name, groot):
                continue
            with open(here / name, encoding="utf-8", errors="replace") as handle:
                for i, line in enumerate(handle, 1):
                    found = match(line)
                    hits += [{"path": str(here / name), "needle": nd, "line": i} for nd in found]
    return hits


def classify_hits_u(hits, fragments=None, job_scratch=None) -> dict:
    g0 = uc.CONTRACT["g0"]
    return hwsb_known.classify_hits(
        hits, g0["declaration_fragments"] if fragments is None else fragments,
        g0["job_scratch"] if job_scratch is None else job_scratch, label="hwsu_declaration")


def needles(contract=None) -> tuple:
    g0 = (uc.CONTRACT if contract is None else contract)["g0"]
    return tuple(g0["needles_u"]) + tuple(g0["needles_d"])


def _tokens(track) -> tuple:
    strings = [s for s in track["scopes"]]
    strings.append(str(track["store"]).replace("\\", "/").rstrip("/").split("/")[-1])
    for k in ("dry_store_glob", "test_root_glob"):
        strings.append(str(track[k]).replace("\\", "/").split("/")[-1].replace("*", ""))
    return [s.lower() for s in strings], [tuple(int(x) for x in b) for b in track["seed_blocks"]]


def namespace_overlap(u, d) -> list:
    us, ub = _tokens(u)
    ds, db = _tokens(d)
    out = [("string", a, b) for a in us for b in ds if a and b and (a == b or a in b or b in a)]
    out += [("seed", a, b) for a in ub for b in db if a[0] <= b[1] and b[0] <= a[1]]
    return out


def _sha_ok(path, want, root) -> bool:
    try:
        return uc.sha256_file(path, root) == want
    except (OSError, C1GateFailure):
        return False


def _authority(out, ctx, checks) -> None:
    A = (ctx.get("contract") or uc.CONTRACT)["authority"]
    mb, root = Path(ctx["mailbox"]), ctx["root"]
    bad = [f"addendum {a['addendum']}" for a in A["addenda"]
           if not _sha_ok(mb / a["path"], a["sha256"], root)]
    d = A["design"]
    bad += [n for n, p, h in (("design", mb / d["path"], d["sha256"]),
                              ("protocol copy", uc.PROTOCOL_PATH, d["sha256"]),
                              ("design freeze", mb / d["freeze_record"]["path"],
                               d["freeze_record"]["sha256"])) if not _sha_ok(p, h, root)]
    auth = Path(out) / f"AUTH_OF_{ctx['job']}.json"
    try:
        rec = json.loads(auth.read_text(encoding="utf-8"))
        ap = rec["owner_approval"]
        if not _sha_ok(mb / ap["path"], ap["sha256"], root):
            bad.append("owner approval")
        if rec["freeze_of_sha256"] != stage_records.sha256(Path(out) / "FREEZE_OF.json"):
            bad.append("AUTH freeze_of_sha256")
    except (OSError, ValueError, KeyError, TypeError):
        bad.append("AUTH_OF record")
    checks["authority"] = not bad
    if bad:
        raise C1GateFailure(AUTHORITY, f"authority: {bad}")


def _records(ctx, checks) -> None:
    A = (ctx.get("contract") or uc.CONTRACT)["authority"]
    mb, root = Path(ctx["mailbox"]), ctx["root"]
    bad = [k for k, r in A["records"].items() if not _sha_ok(mb / r["path"], r["sha256"], root)]
    if not bad:
        w2 = uc.read_json(mb / A["records"]["HWSC_W2_END"]["path"], root)
        for f, h in (("reservation_file", "reservation_file_sha256"),
                     ("run_lock_file", "run_lock_sha256"),
                     ("operation_active_file", "operation_active_sha256")):
            if not _sha_ok(Path(root) / w2[f], w2[h], root):
                bad.append(f)
    checks["records"] = not bad
    if bad:
        raise C1GateFailure(AUTHORITY, f"records: {bad}")


def g0_of(out, ctx) -> dict:
    C, mb, root, checks = ctx.get("contract") or uc.CONTRACT, Path(ctx["mailbox"]), ctx["root"], {}
    _authority(out, ctx, checks)
    _records(ctx, checks)
    ns = uc.read_json(mb / C["authority"]["records"]["HWS_UD_NAMESPACE"]["path"], root)["tracks"]
    if ns["U"] != C["namespace"]["U"]:
        raise C1GateFailure(AUTHORITY, "namespace record tracks.U differs from CONTRACT")
    over = namespace_overlap(ns["U"], ns["D"])
    checks["namespace"] = not over
    if over:
        raise C1GateFailure(SEED_SCOPE, f"namespace overlap: {over[:5]}")
    checks["store"] = ur.lineage_u(out)["status"] == "PASS"
    w2 = ur.w2_attestation(root, own=ctx["reservation_id"], w2_end=mb / "records" /
                           "HWSC_W2_END.json",
                           w2_end_sha256=C["authority"]["records"]["HWSC_W2_END"]["sha256"])
    checks["attestation"] = w2["status"] == "PASS"
    if not checks["attestation"]:
        raise C1GateFailure(AUTHORITY, f"live reservations: {w2['live']}")
    c = classify_hits_u(seed_search_u(root, needles(C)), C["g0"]["declaration_fragments"],
                        C["g0"]["job_scratch"])
    f = Path(out) / "stages" / "OF" / "G0_OF.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    stage_records.write_new(f, {"hits": c["hits"], "status": c["status"], "checks": checks})
    if c["status"] != "PASS":
        raise C1GateFailure(SEED_SCOPE, f"unclassified needle hits: {c['status']}")
    return {"status": "PASS", "n_hits": len(c["hits"]), "checks": checks}
