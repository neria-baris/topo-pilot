"""Author B, K4b TEST_PLAN B9, B10, B11, B14, B21: the sealed file and the refusal of any
report that would let X-bar(+/-) = C +/- D be reconstructed; gate order and first-non-PASS
stop; no fresh access without a verified release B; the G0 seed classification (RC5).

Synthetic stores and release files under tmp_path only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import chart  # noqa: E402
import errors  # noqa: E402
import k4b_config  # noqa: E402
import k4b_driver  # noqa: E402
import k4b_fresh  # noqa: E402
import k4b_release  # noqa: E402
import k4b_scores  # noqa: E402
import k4b_stats  # noqa: E402
import scores  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

SEALED_KEYS = ("mean_X_minus", "mean_X_plus", "control_means", "init_means", "decoder_means",
               "delta1_mean", "delta2_mean", "delta4_orc_mean", "supported_contribution",
               "supported_conditional_mean", "endpoint_ratios")
AUTHORITY = "FAIL_TECHNICAL/AUTHORITY"


# ------------------------------------------------------------------- sealing (B9, B14)

def test_sealed_keys_are_the_registered_tuple():
    assert tuple(k4b_stats.SEALED_KEYS) == SEALED_KEYS


def clean_report():
    return {"gates": [{"gate": "P1", "status": "PASS"}],
            "support": {"1729": {"val": {"n": 3072, "n_supported": 3000, "missing_mass": 0.002,
                                         "width": 0.004}}},
            "B4": {"point": 0.03, "lower": 0.02}, "sdU": {"1729/-": 0.1},
            "ladder": {"candidates": {"3072": {"mde_ok": True}}}, "sealed_sha256": "0" * 64}


def test_check_unsealed_accepts_a_clean_report():
    assert k4b_stats.check_unsealed(clean_report()) is None


@pytest.mark.parametrize("key", SEALED_KEYS)
@pytest.mark.parametrize("where", ["top", "nested", "in_list"])
def test_check_unsealed_refuses_any_sealed_key_anywhere(key, where):
    report = clean_report()
    if where == "top":
        report[key] = 0.01
    elif where == "nested":
        report["support"]["1729"]["val"][key] = 0.01
    else:
        report["gates"].append({"gate": "X", "details": [{"a": 1}, {key: [0.1, 0.2]}]})
    with pytest.raises(C1GateFailure) as exc:
        k4b_stats.check_unsealed(report)
    assert exc.value.status == "FAIL_TECHNICAL/SEALING"
    assert key in exc.value.reason


def test_report_with_width_and_supported_contribution_refused():
    """C = mean(A u r4) beside D = width/2 would unseal X-bar(+/-) = C +/- D (RC3)."""
    report = clean_report()
    report["support"]["1729"]["val"]["supported_contribution"] = 0.011
    with pytest.raises(C1GateFailure):
        k4b_stats.check_unsealed(report)


def support_inputs():
    rng = np.random.default_rng(41)
    res = np.array([0.9] * 8 + [0.1] * 4)
    d8 = np.array([0.5] * 6 + [1.5] * 2 + [0.5, 0.5, 1.5, 1.5])
    R = 1.0
    supported = (res >= 0.2) & (d8 <= R)
    phase = rng.uniform(0.0, 2 * np.pi, 12)
    ext = chart.Extension(phase, res, d8, supported, np.zeros(12, dtype=bool))
    m32 = rng.normal(scale=0.1, size=(12, 2))
    m4 = rng.normal(scale=0.1, size=(12, 2))
    return ext, R, scores.r4_norms(m32, m4), phase, m32, m4


def test_support_report_sealed_form_has_no_reconstructing_keys():
    ext, R, r4n, phi, m32, m4 = support_inputs()
    rep = k4b_scores.support_report(ext, R, r4n, phi, m32, m4, True)
    assert "supported_contribution" not in rep
    assert "supported_conditional_mean" not in rep
    assert rep["n"] == 12 and rep["n_supported"] == 6
    A = ext.supported.astype(float)
    missing = float(np.mean((1.0 - A) * r4n))
    assert float(rep["missing_mass"]) == pytest.approx(missing, rel=1e-12, abs=1e-15)
    assert float(rep["width"]) == pytest.approx(2 * missing, rel=1e-12, abs=1e-15)
    k4b_stats.check_unsealed({"support": {"1729": {"val": rep}}})


def test_support_report_unsealed_form_is_refused_in_a_validation_report():
    ext, R, r4n, phi, m32, m4 = support_inputs()
    rep = k4b_scores.support_report(ext, R, r4n, phi, m32, m4, False)
    A = ext.supported.astype(float)
    x = scores.scores(scores.unit_vectors(phi), m32, m4)
    assert float(rep["supported_contribution"]) == pytest.approx(float(np.mean(A * x)),
                                                                 rel=1e-12, abs=1e-15)
    assert "supported_conditional_mean" in rep
    with pytest.raises(C1GateFailure):
        k4b_stats.check_unsealed({"support": {"1729": {"val": rep}}})


def test_write_sealed_never_overwrites(tmp_path):
    path = tmp_path / "SEALED_VALIDATION.json"
    path.write_text('{"sealed": "earlier"}\n', encoding="utf-8")
    before = path.read_bytes()
    with pytest.raises(Exception):
        k4b_stats.write_sealed(tmp_path, {})
    assert path.read_bytes() == before


# ------------------------------------------------------------------ gate order (B10)

def test_gate_order_release_a():
    assert tuple(k4b_driver.GATE_ORDER) == ("G0", "H1", "REG1", "H2", "ORACLE-VAL", "B4-VAL",
                                            "C0-CAL", "C0-VAL", "CERT-VAL", "P1")


def gate_lines(out):
    path = Path(out) / "GATES.jsonl"
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x]


def full(rec):
    return rec.get("full_status", rec["status"])


def make_steps(failure_at, exc, calls):
    def step(gate):
        def fn():
            calls.append(gate)
            if gate == failure_at:
                raise exc
            return {"value": len(calls)}
        return fn
    return [(g, step(g)) for g in k4b_driver.GATE_ORDER]


def test_run_gates_all_pass_in_order(tmp_path):
    calls = []
    recs = k4b_driver.run_gates(tmp_path, make_steps(None, None, calls))
    assert calls == list(k4b_driver.GATE_ORDER)
    lines = gate_lines(tmp_path)
    assert [r["gate"] for r in lines] == list(k4b_driver.GATE_ORDER)
    assert all(r["status"] == "PASS" for r in lines)
    assert lines[2]["value"] == 3
    assert len(recs) == len(k4b_driver.GATE_ORDER)


@pytest.mark.parametrize("exc,expected", [
    (C1GateFailure("INCONCLUSIVE/HEADROOM", "lower 0.009"), "INCONCLUSIVE/HEADROOM"),
    (C1GateFailure("FAIL_TECHNICAL/ORACLE", "moment gap"), "FAIL_TECHNICAL/ORACLE"),
    (ValueError("boom"), "FAIL_TECHNICAL"),
    (errors.Unresolved("zero gauge alignment"), "INCONCLUSIVE"),
])
def test_first_non_pass_stops_and_later_gates_not_run(tmp_path, exc, expected):
    calls = []
    order = list(k4b_driver.GATE_ORDER)
    stop = order.index("B4-VAL")
    recs = k4b_driver.run_gates(tmp_path, make_steps("B4-VAL", exc, calls))
    assert calls == order[:stop + 1]
    lines = gate_lines(tmp_path)
    assert [r["gate"] for r in lines] == order
    assert all(r["status"] == "PASS" for r in lines[:stop])
    assert full(lines[stop]) == expected or lines[stop]["status"] == expected
    assert all(r["status"] == "NOT_RUN" for r in lines[stop + 1:])
    assert len(recs) == len(order)


def test_split_overlap_maps_to_lineage(tmp_path):
    from topo_pilot.dataset.checks import check_disjoint

    def overlap():
        check_disjoint(a=np.array([1, 2], dtype=np.int64), b=np.array([2, 3], dtype=np.int64))
        return {}

    k4b_driver.run_gates(tmp_path, [("H2", overlap), ("ORACLE-VAL", lambda: {})])
    lines = gate_lines(tmp_path)
    assert "FAIL_TECHNICAL/LINEAGE" in (full(lines[0]), lines[0]["status"])
    assert lines[1]["status"] == "NOT_RUN"


# ------------------------------------------------------------- release B (B11)

def release(path, **over):
    base = {"kind": "B", "job_id": "0048", "task_sha256": "AB" * 32, "worker_session": "sess-1",
            "protocol_sha256": k4b_config.CONTRACT["protocol_sha256"], "freeze_sha256": "0" * 64,
            "reservation": "RES-K-REG2", "N": 3072, "k": 1, "kreg2_sha256": "1" * 64,
            "kreg2_sources": [], "accept": {"verdict": "ACCEPT"}}
    base.update(over)
    for k in [k for k, v in base.items() if v is None]:
        del base[k]
    Path(path).write_text(json.dumps(base), encoding="utf-8")
    return Path(path)


@pytest.mark.parametrize("over,kind,task,session", [
    ({"kind": "A"}, "B", "AB" * 32, "sess-1"),
    ({}, "B", "AB" * 32, "sess-2"),
    ({}, "B", "CD" * 32, "sess-1"),
    ({"protocol_sha256": "f" * 64}, "B", "AB" * 32, "sess-1"),
    ({"N": None, "k": None}, "B", "AB" * 32, "sess-1"),
    ({"worker_session": ""}, "B", "AB" * 32, ""),
])
def test_verify_release_refuses_mismatches(tmp_path, over, kind, task, session):
    path = release(tmp_path / "release.json", **over)
    with pytest.raises(C1GateFailure) as exc:
        k4b_release.verify_release(path, kind, task, session)
    assert exc.value.status == AUTHORITY


def test_authorized_worker():
    assert k4b_release.authorized_worker({"worker_session": "s-1"}, "s-1") is True
    assert k4b_release.authorized_worker({"worker_session": "s-1"}, "s-2") is False
    assert k4b_release.authorized_worker({"worker_session": ""}, "") is False
    assert k4b_release.authorized_worker({}, "s-1") is False


@pytest.mark.parametrize("case", ["missing", "malformed", "kind_A", "session"])
def test_no_fresh_access_without_release_b(tmp_path, case):
    out = tmp_path / "k4b-store"
    out.mkdir()
    path = tmp_path / "release_B.json"
    if case == "malformed":
        path.write_text('{"kind": "B",', encoding="utf-8")
    elif case == "kind_A":
        release(path, kind="A")
    elif case == "session":
        release(path, worker_session="someone-else")
    with pytest.raises(C1GateFailure) as exc:
        k4b_fresh.require_release_b(out, path, "sess-1")
    assert exc.value.status == AUTHORITY
    assert not (out / "stages" / "S7").exists()


# ------------------------------------------------------------- G0 seed classification (B21)

def hit(kind, i=0):
    return {"path": f"tools/k4b/file_{i}.py", "text": f"610101 k4b-sf-v1 #{i}", "kind": kind}


def test_own_declarations_are_not_prior_use():
    hits = [hit("k4b_declaration", i) for i in range(4)]
    r = k4b_driver.classify_seed_hits(hits)
    assert r["status"] == "PASS"
    dumped = json.dumps(r, default=str)
    assert all(h["path"] in dumped for h in hits)


def test_no_hits_pass():
    assert k4b_driver.classify_seed_hits([])["status"] == "PASS"


@pytest.mark.parametrize("bad", ["prior_issuance", "unclassified", "maybe"])
def test_prior_or_unclassified_hit_fails_closed(bad):
    hits = [hit("k4b_declaration", 0), {"path": "jobs/0007/seed_map.json",
                                        "text": "610103", "kind": bad}]
    r = k4b_driver.classify_seed_hits(hits)
    if bad == "maybe":
        assert r["status"] != "PASS"
    else:
        assert r["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
    assert "jobs/0007/seed_map.json" in json.dumps(r, default=str)
