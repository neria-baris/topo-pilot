"""K4b ledgers, chart construction wrappers, C0 gates, freeze and determinism (API.md §6).

Protocol §4 (charts through the unchanged C1' kernels; ledgers of 6 trained and 3 step-0
constructions), §6 (C0-CAL, C0-VAL), RC10 (a FAIL_TECHNICAL in shared code stops at once).
Kernels are looked up on c1_chart at call time.
"""

from __future__ import annotations

import json
from pathlib import Path

import c1_chart
import chart
import k4b_config  # noqa: F401  (sys.path)
import numpy as np
import stage_records
from c1_records import C1GateFailure, adapt_chart_exception, classify_exception

TRAINED_LEDGER = "CHART_CONSTRUCTIONS_trained.json"
INIT_LEDGER = "CHART_CONSTRUCTIONS_init.json"
FROZEN = Path("stages") / "S4a" / "PRODUCTION_FROZEN.json"
UNAVAILABLE = "INCONCLUSIVE/CHART_UNAVAILABLE"
LINEAGE = "FAIL_TECHNICAL/LINEAGE"


class InitLedger:
    """The step-0 ledger: production claims only (at most 3, one per model)."""

    def __init__(self, path):
        self.path = Path(path)
        self._ledger = c1_chart.ConstructionLedger(path)

    def claim(self, model, role) -> None:
        if role != "production":
            raise C1GateFailure("FAIL_TECHNICAL", f"role {role!r} refused on the step-0 ledger")
        self._ledger.claim(model, role)

    def claims(self) -> list:
        return self._ledger.claims()


def open_ledgers(out) -> tuple:
    return (c1_chart.ConstructionLedger(Path(out) / TRAINED_LEDGER),
            InitLedger(Path(out) / INIT_LEDGER))


def _status_of_exception(exc) -> tuple:
    mapped = adapt_chart_exception(exc)
    status, reason = mapped if mapped is not None else classify_exception(exc)
    if status == "INCONCLUSIVE" and str(reason).startswith("CHART_UNAVAILABLE"):
        status = UNAVAILABLE
    return status, reason


def _diagnostics(ch, gauge) -> dict:
    info = dict(getattr(ch, "info", {}) or {})
    keep = ("m", "n", "lift_kind", "excluded_ids", "n_components", "component_sizes", "b", "d",
            "r", "ell_max", "g", "residual")
    d = {k: info[k] for k in keep if k in info}
    d["alignment"] = float(gauge.alignment) if gauge is not None else None
    return d


def build_chart(X, ids, m32, ledger, model, role, cfg, guard=None, timed=None,
                persist=None) -> dict:
    """Claim (model, role) first, then fit once; never retried."""
    try:
        ledger.claim(model, role)
        ch = c1_chart.fit_chart_lcc(X, ids, cfg, guard, timed, persist)
        if role == "production":
            m = np.asarray(m32, dtype=np.float64)
            if not np.all(np.isfinite(m)):
                raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", "non-finite oracle m32")
            gauge = c1_chart.fit_production_gauge(ch, m[np.asarray(ch.info["cstar"])])
            if not (np.isfinite(gauge.alignment) and gauge.alignment > 0):
                return {"status": UNAVAILABLE, "reason": "gauge alignment not positive",
                        "chart": ch, "gauge": gauge, "serial": None,
                        "diagnostics": _diagnostics(ch, gauge)}
        else:
            gauge = c1_chart.IDENTITY_CARRIER
    except Exception as exc:  # noqa: BLE001  mapped by the §16 rules
        status, reason = _status_of_exception(exc)
        return {"status": status, "reason": reason, "chart": None, "gauge": None,
                "serial": None, "diagnostics": {}}
    label = "production" if role == "production" else "validation_only"
    return {"status": "PASS", "reason": "", "chart": ch, "gauge": gauge,
            "serial": c1_chart.serialise(ch, gauge, label), "diagnostics": _diagnostics(ch, gauge)}


def _m32_for(m32_land, j):
    return m32_land[j] if isinstance(m32_land, dict) else m32_land


def c0_cal(models, X_cal, ids, m32_land, out, cfg, guard=None, timed=None,
           persist=None) -> dict:
    trained, _ = open_ledgers(out)
    per = {}
    for j in models:
        per[j] = build_chart(X_cal[j], ids, _m32_for(m32_land, j), trained, j, "production",
                             cfg, guard, timed, persist)
        if per[j]["status"] != "PASS":
            return {"status": per[j]["status"], "reason": per[j]["reason"], "per_model": per}
    return {"status": "PASS", "per_model": per}


def init_charts(models, X_cal_init, ids, m32_land, out, cfg, guard=None, timed=None,
                persist=None) -> dict:
    """Step-0 charts: a valid CHART_UNAVAILABLE is INIT_UNAVAILABLE (non-gating); any
    FAIL_TECHNICAL stops the cohort at once (RC10)."""
    _, init = open_ledgers(out)
    per = {}
    for j in models:
        res = build_chart(X_cal_init[j], ids, _m32_for(m32_land, j), init, j, "production",
                          cfg, guard, timed, persist)
        if res["status"].startswith("FAIL_TECHNICAL"):
            raise C1GateFailure(res["status"], f"step-0 chart {j}: {res['reason']}")
        if res["status"] != "PASS":
            res = {"status": "INIT_UNAVAILABLE", "reason": f"{res['status']}: {res['reason']}"}
        per[j] = res
    return {"status": "PASS", "per_model": per}


def _sha(path) -> str:
    return stage_records.sha256(path)


def freeze_production(out, charts, init, decoders) -> dict:
    """Writes every production chart, step-0 chart and decoder, then PRODUCTION_FROZEN.json."""
    import k4b_decoder

    out = Path(out)
    stage = out / "stages" / "S4a"
    stage.mkdir(parents=True, exist_ok=True)
    init = init.get("per_model", init)
    files = {}
    for j, res in charts.items():
        stage_records.save_npz(stage / f"CHART_{j}.npz", **res["serial"])
        files[f"CHART_{j}.npz"] = None
    for j, res in init.items():
        if res.get("status") == "PASS":
            stage_records.save_npz(stage / f"INIT_CHART_{j}.npz", **res["serial"])
            files[f"INIT_CHART_{j}.npz"] = None
    for j, dec in decoders.items():
        stage_records.save_npz(stage / f"DECODER_{j}.npz", **k4b_decoder.to_arrays(dec))
        files[f"DECODER_{j}.npz"] = None
    record = {"files": {name: _sha(stage / name) for name in files},
              "init_status": {str(j): r.get("status") for j, r in init.items()},
              "decoder_status": {str(j): d.get("status") for j, d in decoders.items()},
              "gauges": {str(j): [int(r["gauge"].sign), float(r["gauge"].shift),
                                  float(r["gauge"].alignment)] for j, r in charts.items()}}
    stage_records.write_new(out / FROZEN, record)
    return record


def require_frozen(out) -> dict:
    path = Path(out) / FROZEN
    if not path.is_file():
        raise C1GateFailure(LINEAGE, "PRODUCTION_FROZEN.json absent")
    record = json.loads(path.read_text(encoding="utf-8"))
    for name, digest in record["files"].items():
        f = path.parent / name
        if not f.is_file() or _sha(f) != digest:
            raise C1GateFailure(LINEAGE, f"frozen artefact {name} does not re-hash")
    return record


def extend(prod, gauge, Q, cfg, timed=None):
    ext = c1_chart.extend_phase(prod, gauge, Q, cfg, timed)
    ph = np.asarray(ext.phase, dtype=np.float64)
    if not (np.all(np.isfinite(ph)) and np.all((ph >= 0) & (ph < 2 * np.pi))):
        raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", "extension phase outside [0, 2pi)")
    return ext


def c0_val_gate(models, prod, val_X, ids_val, out, cfg, guard=None, timed=None,
                persist=None) -> dict:
    """require_frozen; one direct chart per model; c1_chart.c0_val unchanged."""
    require_frozen(out)
    trained, _ = open_ledgers(out)
    per, status = {}, "PASS"
    for j in models:
        direct = build_chart(val_X[j], ids_val, None, trained, j, "direct", cfg, guard, timed,
                             persist)
        if direct["status"] != "PASS":
            per[j] = {"status": direct["status"], "reason": direct["reason"]}
        else:
            try:
                per[j] = c1_chart.c0_val(prod[j]["chart"], prod[j]["gauge"], val_X[j],
                                         direct["chart"], cfg)
            except Exception as exc:  # noqa: BLE001
                s, r = _status_of_exception(exc)
                per[j] = {"status": s, "reason": r}
            per[j]["direct_diagnostics"] = direct["diagnostics"]
        if status == "PASS" and per[j]["status"] != "PASS":
            status = per[j]["status"]
    return {"status": status, "per_model": per}


def init_val_diagnostics(prod_init, gauge_init, val_X_panel, cfg) -> dict:
    ext = extend(prod_init, gauge_init, val_X_panel, cfg)
    return {"n": int(len(ext.supported)), "n_supported": int(np.sum(ext.supported)),
            "bins": chart.phase_bin_counts(ext.phase, int(cfg["phase_bins"])).tolist(),
            "resultant": float(chart.overall_resultant(ext.phase))}


def determinism_check(stored, recomputed) -> dict:
    mismatch = []
    for label in stored:
        a, b = np.asarray(stored[label]), np.asarray(recomputed.get(label))
        if a.dtype != b.dtype or a.shape != b.shape or a.tobytes() != b.tobytes():
            mismatch.append(label)
    mismatch += [k for k in recomputed if k not in stored]
    return {"status": "FAIL_TECHNICAL/DETERMINISM" if mismatch else "PASS",
            "mismatch": mismatch}
