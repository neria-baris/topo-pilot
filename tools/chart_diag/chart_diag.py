"""Geometry-only chart diagnostic (CHART-DIAG-FROZEN-v1; job 0023; owner decision A1).

For the three E4 cylinder-O models (step 5000, resid_post_3, p32), panels 1 and 2: the frozen K4
chart path up to bar selection, reused unchanged from tools/x4_circle_history
(chart._check_landmarks, chart.cdist, chart.ripser over F47, chart.select_h1_bar,
cochain.edge_list, adapter.RestrictedE4Adapter).
Reports bar, H0 scale, 1-skeleton components at the midpoint, giant fraction, the points outside
the giant component and X's interval; verdict by the mechanical rule fixed in the spec. No phases,
lift, gauge, oracle, labels or endpoint.

Usage: python chart_diag.py <out_dir>
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

REPO = Path(__file__).resolve().parents[2]
K4 = REPO / "tools" / "x4_circle_history"
for _p in (K4, REPO / "tools" / "x4_oracle_profile", REPO / "tests" / "oracle_profile"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import chart as k4chart  # noqa: E402  (frozen K4, unchanged)
from cochain import edge_list  # noqa: E402  (frozen K4, unchanged)

SPEC_SHA = "11710D84FF991B097CDF28E47DCD103822CF4F5BF57D0202F0C84BF05E183793"
OWNER_SHA = "5BD1FDB0D66BCE5299644659B3E09436CA94B762A62D24D02E1AB064FDE537CD"
MODELS, PANELS, GIANT_MIN, FIELD = (1729, 2718, 3141), (1, 2), 0.95, 47
K4_STORE = Path(r"X:\Downloads\projects\topo-pilot\x4-circle-history-feas-store-0015")
REUSED = (
    "tools/x4_circle_history/chart.py",
    "tools/x4_circle_history/cochain.py",
    "tools/x4_circle_history/adapter.py",
)


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def components(D, r):
    """Connected components of the 1-skeleton {i < j : D[i, j] <= r} (cochain.edge_list rule)."""
    n = D.shape[0]
    E = edge_list(D, r)
    A = (
        coo_matrix((np.ones(len(E)), (E[:, 0], E[:, 1])), shape=(n, n))
        if len(E)
        else coo_matrix((n, n))
    )
    count, labels = connected_components(A, directed=False)
    return int(count), labels


def x_interval(l_max, d):
    """X's interval [l_max, d): descriptive only."""
    empty = not l_max < d
    return {"lower": l_max, "upper": d, "empty": empty, "length": 0.0 if empty else d - l_max}


def verdict(fractions, invalid=False):
    """Mechanical rule (fixed in the spec): GO iff every giant fraction >= 0.95."""
    if invalid:
        return "INVALID"
    return "GO" if all(f >= GIANT_MIN for f in fractions) else "STOP"


def geometry(X, ids):
    """The frozen K4 path to bar selection, then the diagnostic readouts."""
    X, ids = k4chart._check_landmarks(X, ids)  # K4 ordering/finiteness checks
    D = k4chart.cdist(X, X)
    res = k4chart.ripser.ripser(D, maxdim=1, coeff=FIELD, distance_matrix=True, do_cocycles=True)
    h0, h1 = np.asarray(res["dgms"][0]), np.asarray(res["dgms"][1])
    k = k4chart.select_h1_bar(h1)
    b, d = float(h1[k, 0]), float(h1[k, 1])
    r = (b + d) / 2.0
    fin0 = h0[:, 1][np.isfinite(h0[:, 1])]
    l_max = float(fin0.max()) if fin0.size else 0.0
    count, labels = components(D, r)
    sizes = np.bincount(labels)
    giant = int(np.argmax(sizes))
    outside = np.flatnonzero(labels != giant)
    Dm = D.copy()
    np.fill_diagonal(Dm, np.inf)
    nn = Dm.min(axis=1)
    norms = np.linalg.norm(X, axis=1)
    rank = np.empty(len(X), dtype=np.int64)
    rank[np.argsort(-norms, kind="stable")] = np.arange(1, len(X) + 1)
    finite1 = h1[np.isfinite(h1[:, 1])]
    return {
        "n": int(len(X)),
        "bar": {"b": b, "d": d, "r": r, "index": int(k)},
        "n_finite_h1_bars": int(len(finite1)),
        "n_finite_positive_h1_bars": int(np.sum(finite1[:, 1] > finite1[:, 0])),
        "l_max_h0": l_max,
        "components_at_r": {"count": count, "sizes": sorted(sizes.tolist(), reverse=True)},
        "giant_fraction": float(sizes[giant]) / len(X),
        "outside_giant": [
            {
                "history_id": str(ids[i]),
                "nn_distance": float(nn[i]),
                "norm_rank": int(rank[i]),
                "component_size": int(sizes[labels[i]]),
            }
            for i in outside
        ],
        "outside_summary": {
            "count": int(len(outside)),
            "nn_distance_min": float(nn[outside].min()) if len(outside) else None,
            "nn_distance_max": float(nn[outside].max()) if len(outside) else None,
            "norm_rank_min": int(rank[outside].min()) if len(outside) else None,
            "norm_rank_max": int(rank[outside].max()) if len(outside) else None,
        },
        "x_interval": x_interval(l_max, d),
    }


def _adapter():
    from adapter import E4Manifest, RestrictedE4Adapter

    from topo_pilot.contracts import ArtifactStore
    from topo_pilot.contracts.backends import LocalFSBackend

    contract = json.loads((K4 / "CONTRACT.json").read_text(encoding="utf-8"))
    per_model = {int(m): dict(ids) for m, ids in contract["artifacts"]["per_model"].items()}
    store = ArtifactStore(LocalFSBackend(Path(contract["artifacts"]["artifact_root"])))
    return RestrictedE4Adapter(store, E4Manifest(per_model=per_model))


def integrity():
    """Reused K4 files must equal the frozen K4 build (FREEZE.json); record the 0018 evidence."""
    freeze = json.loads((K4_STORE / "FREEZE.json").read_text(encoding="utf-8"))
    reused = {
        rel: {"sha256": sha(REPO / rel), "frozen": freeze["files"].get(rel)} for rel in REUSED
    }
    ops, gates = K4_STORE / "OPERATIONS.jsonl", K4_STORE / "GATES.jsonl"
    op_rows = [json.loads(x) for x in ops.read_text(encoding="utf-8").splitlines() if x]
    gate_rows = [json.loads(x) for x in gates.read_text(encoding="utf-8").splitlines() if x]
    bar_logged = any(k in row for row in op_rows for k in ("b", "d", "birth", "death", "bar"))
    chart_gate = next((g for g in gate_rows if g["gate"] == "chart_calibration"), None)
    return {
        "reused_unchanged": all(v["sha256"] == v["frozen"] for v in reused.values()),
        "reused": reused,
        "freeze_sha256": sha(K4_STORE / "FREEZE.json"),
        "job0018": {
            "operations_sha256": sha(ops),
            "gates_sha256": sha(gates),
            "bar_recoverable": bar_logged,
            "chart_calibration_gate": chart_gate,
        },
    }


def run(out_dir):
    out, t0 = Path(out_dir), time.process_time()
    rep = {
        "spec": "CHART-DIAG-FROZEN-v1",
        "spec_sha256": SPEC_SHA,
        "owner_decision_sha256": OWNER_SHA,
        "rule": "GO iff giant fraction >= 0.95 in all 6 cases; STOP otherwise; INVALID on failure",
        "cases": {},
        "verdict": None,
    }
    invalid, reason = False, None
    try:
        rep["integrity"] = integrity()
        if not rep["integrity"]["reused_unchanged"]:
            raise RuntimeError("reused K4 files differ from the frozen K4 build")
        adapter = _adapter()
        for model in MODELS:
            data = adapter.panels(model, PANELS)  # panels 1-2 only; scored panels refused by K4
            for panel in PANELS:
                rep["cases"][f"{model}/panel{panel}"] = geometry(
                    data[panel]["activation"], data[panel]["history_id"]
                )
        case = rep["cases"]["1729/panel1"]
        j18 = rep["integrity"]["job0018"]
        disconnected = case["components_at_r"]["count"] > 1
        rep["reproduction_1729_panel1"] = {
            "bar_recoverable_from_0018_log": j18["bar_recoverable"],
            "exact_bar_check": "not checkable (job 0018 logged operation timings only)"
            if not j18["bar_recoverable"]
            else "see log",
            "consistency_with_0018_stop": disconnected,
            "0018_reason": (j18["chart_calibration_gate"] or {}).get("reason"),
        }
        if not disconnected:
            raise RuntimeError(
                "1729/panel1 is connected at r, contradicting job 0018's recorded stop"
            )
    except Exception as exc:  # noqa: BLE001  any computational or integrity failure -> INVALID
        invalid, reason = True, repr(exc)
    fractions = [c["giant_fraction"] for c in rep["cases"].values()]
    rep["verdict"] = verdict(fractions, invalid or len(fractions) != 6)
    rep["invalid_reason"] = reason
    rep["cpu_s"] = time.process_time() - t0
    out.mkdir(parents=True, exist_ok=True)
    (out / "DIAG.json").write_text(json.dumps(rep, indent=1, sort_keys=True), encoding="utf-8")
    (out / "DIAG.md").write_text(markdown(rep), encoding="utf-8")
    return rep


def _row(name, c) -> str:
    xi, bar = c["x_interval"], c["bar"]
    interval = (
        "empty" if xi["empty"] else f"[{xi['lower']:.6f}, {xi['upper']:.6f}), {xi['length']:.6f}"
    )
    cells = [
        name,
        f"{bar['b']:.6f}",
        f"{bar['d']:.6f}",
        f"{bar['r']:.6f}",
        f"{c['l_max_h0']:.6f}",
        str(c["n_finite_h1_bars"]),
        str(c["components_at_r"]["count"]),
        f"{c['giant_fraction']:.4f}",
        str(c["outside_summary"]["count"]),
        interval,
    ]
    return "| " + " | ".join(cells) + " |"


def markdown(rep) -> str:
    lines = [
        "# Chart geometry diagnostic (CHART-DIAG-FROZEN-v1)",
        "",
        f"**Verdict: {rep['verdict']}** (GO iff giant fraction >= 0.95 in all 6 cases)",
        "",
        "| case | b | d | r | l_max (H0) | finite H1 bars | components at r | giant fraction "
        "| outside giant | X's interval [l_max, d), length |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    lines += [_row(name, c) for name, c in rep["cases"].items()]
    if rep.get("invalid_reason"):
        lines += ["", f"INVALID reason: {rep['invalid_reason']}"]
    lines += ["", "X's interval is descriptive only and plays no part in the verdict."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(json.dumps(run(Path(sys.argv[1]))["verdict"]))
