"""Author A (job 0224): world selection O0 and headroom O5 (protocol §3; API §4; TEST_PLAN §2).

Expected values come from CONTRACT.json and an independent recomputation of the selection rule
on the hash-checked stage-A JSON records (read-only). Synthetic REPORT fixtures live in tmp_path.
"""

from __future__ import annotations  # noqa: I001

import copy
import hashlib
import json
import math
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _d in ("c1prime", "k4b", "hws", "hwsb", "hwsc", "hwsg"):
    if str(REPO / "tools" / _d) not in sys.path:
        sys.path.insert(0, str(REPO / "tools" / _d))
_ERR = None
try:
    import hwsg_config as gc
    import hwsg_oracle as go
except Exception as e:  # collectable before the implementation exists
    _ERR = e

ROOT = Path("X:/Downloads/projects/topo-pilot")
C = json.loads((REPO / "tools" / "hwsg" / "CONTRACT.json").read_text(encoding="utf-8"))
SEL = C["selection"]
W_STAR = C["w_star"]["key"]


@pytest.fixture(autouse=True)
def _imports():
    if _ERR is not None:
        pytest.fail(f"hwsg modules not importable: {_ERR!r}")


def _status(fn, *a, **k):
    try:
        r = fn(*a, **k)
    except Exception as e:  # C1GateFailure carries .status
        return getattr(e, "status", repr(e)), None
    return (r.get("status") if isinstance(r, dict) else None), r


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _rule(order, d4, bounded):
    """Independent recomputation of the §3 rule."""
    pool = [k for k in order if k != W_STAR and bounded[k]]
    lo = min(pool, key=lambda k: (d4[k], pool.index(k)))
    hi = max(pool, key=lambda k: (d4[k], -pool.index(k)))
    rest = [k for k in pool if k not in (lo, hi)]
    c = (math.log(d4[lo]) + math.log(d4[hi])) / 2
    mid = min(rest, key=lambda k: (abs(math.log(d4[k]) - c), rest.index(k)))
    return pool, lo, mid, hi


def _real_records():
    rp = ROOT / SEL["report"]
    if not rp.is_file():
        pytest.skip("stage-A REPORT.json not present")
    assert _sha(rp) == SEL["report_sha256"]
    rep = json.loads(rp.read_text(encoding="utf-8"))
    bounded = {}
    for k, h in SEL["s3_record_sha256"].items():
        f = ROOT / SEL["s3_world_dir"] / f"{k}.json"
        assert _sha(f) == h
        bounded[k] = json.loads(f.read_text(encoding="utf-8"))["law_bound"].get("status") == "BOUNDED"
    return rep, bounded


def test_independent_rule_reproduces_registered():
    rep, bounded = _real_records()
    order = rep["finalists"]["ordinary"]
    d4 = {k: rep["s3"][k]["L3"]["D4"] for k in order}
    pool, lo, mid, hi = _rule(order, d4, bounded)
    assert pool == SEL["pool_expected"] and len(pool) == 9
    assert {"lo": lo, "mid": mid, "hi": hi} == SEL["registered"]
    for tag in ("lo", "mid", "hi"):
        assert C["worlds"][tag]["key"] == SEL["registered"][tag]


def test_go_selection_agrees_on_real_records():
    _real_records()
    r = go.selection(ROOT / SEL["report"], ROOT / SEL["s3_world_dir"])
    assert list(r["pool"]) == SEL["pool_expected"]
    assert (r["lo"], r["mid"], r["hi"]) == tuple(SEL["registered"][t] for t in ("lo", "mid", "hi"))
    assert r["registered_ok"] is True


# ----------------------------------------------------------------------------- synthetic fixtures

KEYS = [W_STAR, "W-a", "W-b", "W-c", "W-d", "W-e"]


def _plant(tmp_path, monkeypatch, d4, unavailable=(), registered=None):
    s3 = tmp_path / "s3"
    s3.mkdir()
    shas = {}
    for k in KEYS:
        st = "UNAVAILABLE/NONTERMINATING_LOGIT" if k in unavailable else "BOUNDED"
        f = s3 / f"{k}.json"
        f.write_text(json.dumps({"key": k, "law_bound": {"status": st}}), encoding="utf-8")
        shas[k] = _sha(f)
    rep = {"finalists": {"ordinary": list(KEYS), "fallback_only": []},
           "s3": {k: {"L3": {"D4": d4[k]}, "at_3x": True} for k in KEYS}}
    rp = tmp_path / "REPORT.json"
    rp.write_text(json.dumps(rep), encoding="utf-8")
    sel = copy.deepcopy(gc.CONTRACT["selection"])
    sel["report_sha256"] = _sha(rp)
    sel["s3_record_sha256"] = shas
    pool, lo, mid, hi = _rule(KEYS, d4, {k: k not in unavailable for k in KEYS})
    sel["pool_expected"] = pool
    sel["registered"] = registered or {"lo": lo, "mid": mid, "hi": hi}
    # API-AMBIGUITY: selection reads CONTRACT values through gc.CONTRACT at call time.
    monkeypatch.setitem(gc.CONTRACT, "selection", sel)
    return rp, s3, (pool, lo, mid, hi)


def test_tie_resolved_by_finalists_order(tmp_path, monkeypatch):
    d4 = {W_STAR: 0.001, "W-a": 0.05, "W-b": 0.04, "W-c": 0.04, "W-d": 0.2, "W-e": 0.09}
    rp, s3, (pool, lo, mid, hi) = _plant(tmp_path, monkeypatch, d4)
    assert lo == "W-b"  # tie with W-c: first in finalists.ordinary wins
    r = go.selection(rp, s3)
    assert (r["lo"], r["mid"], r["hi"]) == (lo, mid, hi)
    assert W_STAR not in r["pool"]


def test_unavailable_world_excluded(tmp_path, monkeypatch):
    d4 = {W_STAR: 0.5, "W-a": 0.05, "W-b": 0.01, "W-c": 0.04, "W-d": 0.2, "W-e": 0.09}
    rp, s3, (pool, lo, mid, hi) = _plant(tmp_path, monkeypatch, d4, unavailable=("W-b",))
    r = go.selection(rp, s3)
    assert "W-b" not in r["pool"] and r["lo"] == "W-c" == lo
    assert list(r["pool"]) == pool


def test_changed_record_byte_fails_binding(tmp_path, monkeypatch):
    d4 = {W_STAR: 0.5, "W-a": 0.05, "W-b": 0.01, "W-c": 0.04, "W-d": 0.2, "W-e": 0.09}
    rp, s3, _ = _plant(tmp_path, monkeypatch, d4)
    f = s3 / "W-c.json"
    f.write_bytes(f.read_bytes() + b" ")
    assert _status(go.selection, rp, s3)[0] == "FAIL_TECHNICAL/BINDING"


def test_changed_report_byte_fails_binding(tmp_path, monkeypatch):
    d4 = {W_STAR: 0.5, "W-a": 0.05, "W-b": 0.01, "W-c": 0.04, "W-d": 0.2, "W-e": 0.09}
    rp, s3, _ = _plant(tmp_path, monkeypatch, d4)
    rp.write_bytes(rp.read_bytes() + b"\n")
    assert _status(go.selection, rp, s3)[0] == "FAIL_TECHNICAL/BINDING"


def test_unregistered_result_fails_binding(tmp_path, monkeypatch):
    d4 = {W_STAR: 0.5, "W-a": 0.05, "W-b": 0.01, "W-c": 0.04, "W-d": 0.2, "W-e": 0.09}
    rp, s3, _ = _plant(tmp_path, monkeypatch, d4,
                       registered={"lo": "W-a", "mid": "W-c", "hi": "W-d"})
    assert _status(go.selection, rp, s3)[0] == "FAIL_TECHNICAL/BINDING"


# ----------------------------------------------------------------------------- O5 headroom


def _rep(key, at3, d4):
    return {"s3": {key: {"at_3x": at3, "L3": {"D4": d4}}}}


def _ok(r):
    return isinstance(r, dict) and r.get("status", "PASS") == "PASS" and r.get("ok", True) is True


@pytest.mark.parametrize("tag", ["lo", "mid", "hi"])
def test_headroom_at_3x_false(tag):
    key = C["worlds"][tag]["key"]
    st, r = _status(go.headroom, tag, _rep(key, False, 0.2))
    assert st == "INCONCLUSIVE/ORACLE_FEASIBILITY"


def test_headroom_threshold_equality_passes():  # OPEN-13
    key = C["worlds"]["hi"]["key"]
    st, r = _status(go.headroom, "hi", _rep(key, True, 0.03))
    assert st in (None, "PASS") and _ok(r)


def test_headroom_below_threshold_fails():  # OPEN-13
    key = C["worlds"]["hi"]["key"]
    st, _ = _status(go.headroom, "hi", _rep(key, True, math.nextafter(0.03, 0)))
    assert st == "INCONCLUSIVE/ORACLE_FEASIBILITY"
