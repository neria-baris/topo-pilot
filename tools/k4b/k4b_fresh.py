"""K4b release-B stages: K-REG2, H2-FRESH, T-PRE, ENDPOINT, export (API.md §10).

Protocol §6 rows 10-12, §8 (decision), §9 (controls, reported only), §11 (report keys). No test
row is sampled or read before require_release_b passes.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import k4b_cert
import k4b_charts
import k4b_config
import k4b_data
import k4b_driver
import k4b_registry
import k4b_release
import k4b_scores
import k4b_stats
import numpy as np
import stage_records
from c1_records import C1GateFailure
from k4b_config import MODELS, SEEDS

AUTHORITY = "FAIL_TECHNICAL/AUTHORITY"
FRESH_ORDER = ("H2-FRESH", "T-PRE", "ENDPOINT")


def kreg2_step(out, release_b_draft, tables) -> dict:
    """Identity-only K-REG2 inside the W2 reservation (extra: K4b's cal b0 and val b0 tables)."""
    reg_dir = Path(out) / "registry"
    m = k4b_registry.build("K-REG2", reg_dir, extra=[tables["cal"], tables["val"]])
    k4b_driver.complete_stage(out, "REG2", [reg_dir / "K-REG2.json",
                                            reg_dir / "K-REG2_digests.npz"])
    return m


def require_release_b(out, release_path, session) -> dict:
    try:
        rel = json.loads(Path(release_path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise C1GateFailure(AUTHORITY, f"no release B: {exc!r}") from exc
    rel = k4b_release.verify_release(release_path, "B", str(rel.get("task_sha256", "")), session)
    if rel.get("w3_attestation") is None or rel["accept"].get("verdict") != "ACCEPT":
        raise C1GateFailure(AUTHORITY, "release B lacks the W3 record or the coordinator ACCEPT")
    reg = Path(out) / "registry" / "K-REG2.json"
    if not reg.is_file() or stage_records.sha256(reg) != rel["kreg2_sha256"]:
        raise C1GateFailure(AUTHORITY, "release B does not bind this store's K-REG2")
    if int(rel["N"]) != int(rel["k"]) * k4b_config.BLOCK or int(rel["N"]) not in \
            k4b_config.LADDER:
        raise C1GateFailure(AUTHORITY, "release B N/k inconsistent")
    return rel


def sample_test(out, proc, release, reservation_path) -> dict:
    res = k4b_release.verify_reservation(reservation_path, release)
    if res["status"] != "PASS":
        raise C1GateFailure("INCONCLUSIVE/AUTHORITY", f"{res['status']}: {res['reason']}")
    k4b_driver.begin_stage(out, "S7")
    d = Path(out) / "stages" / "S7"
    d.mkdir(parents=True, exist_ok=True)
    tabs, files = [], []
    for b in range(int(release["k"])):
        canon, ids = k4b_data.sample_block(proc["T"], proc["E_canon_shared"], proc["pi"],
                                           "test", b)
        t = k4b_data.history_table(canon, ids, "test", b)
        f = d / f"HIST_test_b{b}.npz"
        stage_records.save_npz(f, **{k: v for k, v in t.items() if isinstance(v, np.ndarray)})
        tabs.append(t)
        files.append(f)
    k4b_driver.complete_stage(out, "S7", files)
    return {"canon32": np.concatenate([t["canon32"] for t in tabs]),
            "seq_ids": np.concatenate([t["seq_ids"] for t in tabs]),
            "digest": np.concatenate([t["digest"] for t in tabs]), "blocks": tabs}


def h2_fresh(out, ctx) -> dict:
    res = k4b_release.verify_reservation(ctx["reservation_path"], ctx["release"],
                                         sampling_began=True)
    if res["status"] != "PASS":
        raise C1GateFailure(res["status"], res["reason"])
    digests, seq_union, ranges, predicates, _ = k4b_registry.load(Path(out) / "registry",
                                                                  "K-REG2")
    test = ctx["test"]
    blocks = {f"test_b{i}": t["seq_ids"] for i, t in enumerate(test["blocks"])}
    blocks.update({s: ctx["tables"][s]["seq_ids"] for s in ("cal", "val")})
    k4b_union = set(ctx["tables"]["cal"]["seq_ids"].tolist()) | set(
        ctx["tables"]["val"]["seq_ids"].tolist())
    checks = {"separation": k4b_data.separation_fresh(test["digest"].tolist(), digests),
              "seq_disjoint": k4b_data.seq_disjoint(blocks, set(seq_union) - k4b_union,
                                                    list(ranges.values())),
              "predicates": k4b_data.predicate_check(test["canon32"], predicates)}
    for r in checks.values():
        if r["status"] != "PASS":
            raise C1GateFailure(r["status"], json.dumps(r, default=str)[:2000])
    return checks


def t_pre(out, ctx) -> dict:
    """Oracle + references on every test row; determinism; extension; certificate; fresh B4."""
    p, test, cfg = ctx["proc"], ctx["test"], k4b_config.chart_cfg()
    k4b_charts.require_frozen(out)
    m = k4b_scores.oracle_moments(p["T"], p["E_canon_shared"], p["pi"], test["canon32"],
                                  p["features"])
    refs = k4b_cert.references(p["T"], p["E_canon_shared"], p["pi"], p["coords"],
                               test["canon32"])
    chk = k4b_cert.moment_check(m, refs)
    if not chk["ok"]:
        raise C1GateFailure("FAIL_TECHNICAL/ORACLE", f"{chk['n_fail']} test rows")
    det = k4b_charts.determinism_check(ctx["stored_cal_acts"], ctx["recompute_cal_acts"]())
    if det["status"] != "PASS":
        raise C1GateFailure(det["status"], str(det["mismatch"]))
    eps, arrays, primary, controls = k4b_cert.envelopes(), {}, {}, {}
    for j in MODELS:
        X = ctx["test_acts"](j, "step5000")
        ext = k4b_charts.extend(ctx["prod"][j]["chart"], ctx["prod"][j]["gauge"], X, cfg)
        a = k4b_scores.endpoint_arrays(ext.phase, ext.supported, m[32], m[4])
        b = k4b_cert.endpoint_bounds(a, ext.supported, ext.phase, refs, eps)
        arrays[j] = dict(a, phi=ext.phase, supported=ext.supported, bounds=b)
        primary[f"X_minus_{j}"] = {"X": a["X_minus"], "max_B": b["max"]["minus"]}
        primary[f"X_plus_{j}"] = {"X": a["X_plus"], "max_B": b["max"]["plus"]}
    for name, phi in (("m4_phase", k4b_scores.m4_phase(m[4])),
                      ("sha_suffix", k4b_scores.sha_phase(test["canon32"]))):
        x = k4b_scores.phase_scores(phi, m[32], m[4])
        cb = k4b_cert.control_bounds(x, phi, refs, eps)
        controls[name] = {"X": x, "max_B": cb["max"]}
        arrays[name] = x
    r4n = arrays[MODELS[0]]["r4n"]
    primary["n_hat"] = {"X": r4n, "max_B": max(arrays[j]["bounds"]["max"]["norm"]
                                                for j in MODELS)}
    cert = k4b_cert.certify(primary, controls)
    b4 = k4b_cert.b4_guard(r4n, primary["n_hat"]["max_B"], ctx["Z"], SEEDS["fresh_b4"],
                           len(r4n))
    b4["FRESH_B4_LOW"] = b4["status"] != "PASS"
    ctx.update(test_moments=m, test_arrays=arrays, certificate=cert, fresh_b4=b4)
    if cert["status"] != "PASS":
        raise C1GateFailure(cert["status"], "a primary test row bound exceeds the cap")
    return {"max_gap": str(chk["max_gap"]), "determinism": det["status"],
            "certificate": {k: str(v) for k, v in cert["max_B"].items()},
            "fresh_B4_status": b4["status"]}


def _str(x):
    return str(x) if isinstance(x, Fraction) else x


def endpoint(out, ctx) -> dict:
    a, n = ctx["test_arrays"], len(ctx["test"]["seq_ids"])
    boot_in = {}
    for j in MODELS:
        boot_in[f"minus_{j}"], boot_in[f"plus_{j}"] = a[j]["X_minus"], a[j]["X_plus"]
    for name in ("m4_phase", "sha_suffix"):
        boot_in[name] = a[name]
    draws = k4b_stats.joint_bootstrap(boot_in, SEEDS["endpoint"])
    per, statuses = {}, {}
    for j in MODELS:
        bd = k4b_stats.bounds(draws[f"minus_{j}"], draws[f"plus_{j}"])
        Bm = k4b_cert.b_num(a[j]["bounds"]["max"]["minus"], float(np.max(np.abs(a[j]["X_minus"]))), n)
        Bp = k4b_cert.b_num(a[j]["bounds"]["max"]["plus"], float(np.max(np.abs(a[j]["X_plus"]))), n)
        Fm, Fp = k4b_cert.margin(Bm, ctx["Z"]), k4b_cert.margin(Bp, ctx["Z"])
        st = k4b_stats.model_status(bd["L"], bd["U"], Fm, Fp)
        statuses[j] = st["status"]
        per[j] = {"L": bd["L"][0], "U": bd["U"][0], "L_rank": bd["L_rank"],
                  "U_rank": bd["U_rank"], "F_minus": str(Fm), "F_plus": str(Fp),
                  "B_num_minus": str(Bm), "B_num_plus": str(Bp), "status": st["status"],
                  "labels": st["labels"], "status_without_F": st["status_without_F"],
                  "central95_minus": bd["central95_minus"],
                  "central95_plus": bd["central95_plus"],
                  "point_minus": float(np.mean(a[j]["X_minus"])),
                  "point_plus": float(np.mean(a[j]["X_plus"])),
                  "width": float(np.mean(a[j]["X_plus"] - a[j]["X_minus"]))}
    controls = {name: {"point": float(np.mean(a[name])), "max_B": _str(
        ctx["certificate"]["max_B"][name]), "certified": ctx["certificate"]["certified"][name]}
        for name in ("m4_phase", "sha_suffix")}
    return {"per_model": per, "controls": controls, "overall": k4b_stats.overall(statuses),
            "fresh_B4": {k: _str(v) for k, v in ctx["fresh_b4"].items()},
            "Z_bound": str(ctx["Z"]), "N": n, "k": n // k4b_config.BLOCK,
            "c1prime_disclosure": k4b_config.CONTRACT["authority"]["c1prime_disclosure"]}


def export(out, result) -> Path:
    d = Path(out) / "stages" / "S8"
    d.mkdir(parents=True, exist_ok=True)
    f = d / "RESULT.json"
    stage_records.write_new(f, result)
    k4b_driver.complete_stage(out, "S8", [f])
    sealed = Path(out) / k4b_stats.SEALED_FILE
    if sealed.is_file():
        stage_records.write_new(d / "SEALED_OPENED.json",
                                json.loads(sealed.read_text(encoding="utf-8")))
    return f


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="K4b release B: H2-FRESH -> ENDPOINT")
    ap.add_argument("--release", required=True)
    ap.add_argument("--out", default=str(k4b_config.STORE))
    ap.add_argument("--session", required=True)
    ap.add_argument("--mailbox", default=str(k4b_config.ROOT / "agent-handoff"))
    a = ap.parse_args(argv)
    out = Path(a.out)
    rel = require_release_b(out, a.release, a.session)
    raise C1GateFailure("NOT_RUN", f"release B {rel['job_id']}: the fresh stages are run by "
                        "the dispatched job with its context (validation tables, charts)")


if __name__ == "__main__":
    raise SystemExit(main())
