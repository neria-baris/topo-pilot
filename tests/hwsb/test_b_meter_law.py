"""Author B (job 0161), TEST_PLAN section 3 `test_b_meter_law.py`: the meter binding and placement
(section 6.4 rule 1, RC-5, DRB13b) and the INDEPENDENT test of the B8a enclosure (OPEN-3, DRB12):
exact rational exp bounds written here contain every exact w* emission entry inside the returned
enclosure; `law_bound` on w*, w(3/2) and w0; process_law state restored. tools/hwsb/*.py unread."""

from __future__ import annotations

import json
import os
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import hwsb_config as hc  # noqa: E402
import hwsb_data as hd  # noqa: E402
import hwsb_law as hl  # noqa: E402
import hwsb_meter_bind as hm  # noqa: E402
import controls  # noqa: E402
import k4b_meter_bind  # noqa: E402
import meter  # noqa: E402
import op_guard  # noqa: E402
import process_law  # noqa: E402
import winjob  # noqa: E402
from topo_pilot.contracts import ArtifactStore, MemoryBackend  # noqa: E402
from topo_pilot.process.emission import EmissionConfig  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "hwsb" / "CONTRACT.json").read_text(encoding="utf-8"))
GIB, INF = 1024**3, float("inf")
PROJECT = Path("X:/Downloads/projects/topo-pilot").resolve()
SCRATCH = Path("X:/Downloads/topo-scratch")


def code_of(fn):
    try:
        return fn()
    except SystemExit as e:
        return e.code


# ------------------------------------------------------------------ meter binding
@pytest.fixture
def preserved(monkeypatch):
    for name in ("OUT", "LEDGER", "EMERGENCY", "LOCK", "ACTIVE", "LOG_DIR", "CAP_S",
                 "STOP_NEW_S", "OUTPUT_CAP", "WORKER_SESSION", "limit_reason", "main"):
        monkeypatch.setattr(meter, name, getattr(meter, name))
    for name in ("JOB_ID", "TASK_SHA256"):
        monkeypatch.setattr(controls, name, getattr(controls, name))
    monkeypatch.setattr(winjob, "MEMORY_CAP", winjob.MEMORY_CAP)
    monkeypatch.setattr(k4b_meter_bind, "TEMP_ROOT", k4b_meter_bind.TEMP_ROOT)
    monkeypatch.setattr(op_guard, "archive_stale", op_guard.archive_stale)
    for var in ("TEMP", "TMP", "TMPDIR") + tuple(meter.THREAD_VARS):
        if var in os.environ:
            monkeypatch.setenv(var, os.environ[var])
        else:
            monkeypatch.setenv(var, "unset")
            monkeypatch.delenv(var)
    monkeypatch.setattr(sys, "argv", list(sys.argv))
    return monkeypatch


def test_bind_sets_memory_cap_temp_root_and_meter_paths(tmp_path, preserved):
    out, temp = tmp_path / "out", tmp_path / "temp"
    hm.bind("0161B", "ab" * 32, out, "sess-b", temp)
    assert winjob.MEMORY_CAP == hm.MEMORY_CAP == 8 * GIB == CONTRACT["resources"]["memory_cap_bytes"]
    assert k4b_meter_bind.TEMP_ROOT == str(temp)
    assert Path(meter.LEDGER) == out / "cpu_ledger.json"
    assert Path(meter.LOCK) == out / "RUN.lock" and Path(meter.LOG_DIR) == out / "logs"
    assert Path(meter.ACTIVE) == out / "METER_ACTIVE.lock"
    assert meter.CAP_S == INF and meter.STOP_NEW_S == INF
    assert meter.OUTPUT_CAP == 4 * GIB == CONTRACT["resources"]["output_cap_bytes"]
    assert meter.WORKER_SESSION == "sess-b" and controls.JOB_ID == "0161B"
    env = k4b_meter_bind.child_env("0161B", base={})
    assert Path(env["TEMP"]) == temp / "tmp-0161B"
    assert env["TEMP"] == env["TMP"] == env["TMPDIR"]
    assert all(env[v] == "1" for v in meter.THREAD_VARS)


def test_bind_defaults_temp_root_to_out(tmp_path, preserved):
    hm.bind("0161B", "ab" * 32, tmp_path, "sess-b")
    assert k4b_meter_bind.TEMP_ROOT == str(tmp_path)
    assert Path(k4b_meter_bind.child_env("0161B", base={})["TEMP"]) == tmp_path / "tmp-0161B"


def test_effective_settings(tmp_path, preserved):
    hm.bind("0161B", "ab" * 32, tmp_path / "o", "sess-b", tmp_path / "t")
    eff = hm.effective_settings()
    assert set(eff) >= {"memory_cap", "temp_root", "ledger", "cap_s", "output_cap", "thread_vars"}
    assert eff["memory_cap"] == 8 * GIB and eff["temp_root"] == str(tmp_path / "t")
    assert Path(eff["ledger"]) == tmp_path / "o" / "cpu_ledger.json" and eff["cap_s"] == INF
    assert eff["output_cap"] == 4 * GIB and list(eff["thread_vars"]) == list(meter.THREAD_VARS)


def test_rewrite_argv_appends_inf_caps():
    got = k4b_meter_bind.rewrite_argv(["--label", "t", "--max-cpu", "600", "--", "python", "-c", "0"])
    assert got == ["--label", "t", "--max-cpu", "inf", "--max-wall", "inf", "--", "python", "-c", "0"]


def test_job_paths_test_and_store_kinds():
    p = hm.job_paths("0161", "test")
    assert Path(p["out"]) == SCRATCH / "test_hwsb-0161" and Path(p["temp_root"]) == Path(p["out"])
    assert Path(p["basetemp"]) == SCRATCH / "test_hwsb-0161" / "pytest"
    s = hm.job_paths("0170", "store")
    store = Path(CONTRACT["resources"]["store"])
    assert Path(s["out"]) == store and Path(s["temp_root"]) == store / "tmp"
    assert s["basetemp"] is None
    with pytest.raises(ValueError):
        hm.job_paths("0161", "other")


def test_placement_ok_for_test_paths_and_planted_inside_root():
    ok = hm.placement_ok(hm.job_paths("0161", "test"))
    assert ok["ok"] is True
    assert ok["checks"] == {"out_outside_root": True, "temp_outside_root": True,
                            "basetemp_outside_root": True, "test_prefixed": True}
    inside = {"out": PROJECT / "scratch" / "test_hwsb-1", "temp_root": PROJECT / "tmp",
              "basetemp": PROJECT / "tmp" / "pytest"}
    bad = hm.placement_ok(inside)
    assert bad["ok"] is False and not any(bad["checks"][k] for k in (
        "out_outside_root", "temp_outside_root", "basetemp_outside_root"))
    elsewhere = {"out": SCRATCH / "hwsb-dry", "temp_root": SCRATCH / "hwsb-dry", "basetemp": None}
    res = hm.placement_ok(elsewhere)
    assert res["checks"]["test_prefixed"] is False and res["ok"] is False
    assert res["checks"]["basetemp_outside_root"] is True  # None counts as outside


def test_this_suites_tmp_path_is_outside_the_project_root(tmp_path):
    assert PROJECT not in tmp_path.resolve().parents and tmp_path.resolve() != PROJECT


def argv(*extra, kind="test"):
    return ["hwsb_meter_bind.py", "--job", "0161B", "--task-sha256", "ab" * 32, "--session",
            "sess-b", "--kind", kind, *extra]


@pytest.fixture
def paths(tmp_path, preserved):
    out = tmp_path / "out"
    out.mkdir()
    pt = {"out": out, "temp_root": out, "basetemp": out / "pytest"}
    preserved.setattr(hm, "job_paths", lambda job, kind: dict(pt))
    return out


def test_main_binds_and_hands_over_to_the_meter(paths, preserved):
    seen, archived = {}, []

    def fake_main():
        seen.update(argv=list(sys.argv), temp=os.environ.get("TEMP"), cap=winjob.MEMORY_CAP,
                    threads={v: os.environ.get(v) for v in meter.THREAD_VARS},
                    limiter=meter.limit_reason)
        return 0

    original = meter.limit_reason
    preserved.setattr(meter, "main", fake_main)
    preserved.setattr(op_guard, "archive_stale", lambda out: archived.append(Path(out)))
    preserved.setattr(sys, "argv", argv("--label", "t", "--max-cpu", "600", "--", "python", "-c", "0"))
    assert hm.main() == 0
    assert seen["argv"] == ["hwsb_meter_bind.py", "--label", "t", "--max-cpu", "inf", "--max-wall",
                            "inf", "--", "python", "-c", "0"]
    assert seen["cap"] == 8 * GIB and Path(seen["temp"]) == paths / "tmp-0161B"
    assert all(v == "1" for v in seen["threads"].values())
    assert seen["limiter"] is not original and archived == [paths]


def test_main_refuses_foreign_run_lock_and_missing_arguments(paths, preserved):
    called = []
    preserved.setattr(meter, "main", lambda: called.append(1) or 0)
    preserved.setattr(op_guard, "archive_stale", lambda out: None)
    (paths / "RUN.lock").write_text(json.dumps({"session": "someone-else"}), encoding="utf-8")
    preserved.setattr(sys, "argv", argv("--label", "t", "--", "python"))
    assert code_of(hm.main) == 3 and called == []
    (paths / "RUN.lock").write_text(json.dumps({"session": "sess-b"}), encoding="utf-8")
    assert code_of(hm.main) == 0 and called == [1]
    preserved.setattr(sys, "argv", ["hwsb_meter_bind.py", "--job", "0161B", "--session", "s",
                                    "--kind", "test", "--label", "t", "--", "py"])
    assert code_of(hm.main) == 2 and called == [1]


# ------------------------------------------------------------------ independent exact reference
def exp_neg_bounds(t):
    """Rational lo <= exp(-t) <= hi, t >= 0 rational: Taylor sums of exp(t) with a geometric tail."""
    n = int(4 * t) + 100  # tail < t^n/n! < 1e-100 for every t used here (t <= 50)
    s = term = Fraction(1)
    for k in range(1, n + 1):
        term = term * t / k
        s += term
    tail = term * t / (n + 1) / (1 - t / (n + 2))
    return 1 / (s + tail), 1 / s


def reference_entries(states, sigma):
    """{(s, j): (lo, hi)} rational bounds on the exact softmax entry exp(q_j)/sum_k exp(q_k)."""
    centres = [(Fraction(1, 2) + 2 * a, Fraction(1, 2) + 2 * b) for a in range(6) for b in range(6)]
    cache, out = {}, {}
    for s, (x, y) in enumerate(states):
        rows = []
        for cx, cy in centres:
            dx = abs(Fraction(x) - cx) % 12
            d2 = min(dx, 12 - dx) ** 2 + (Fraction(y) - cy) ** 2
            t = d2 / (2 * sigma**2)
            if t not in cache:
                cache[t] = exp_neg_bounds(t)
            rows.append(cache[t])
        s_lo, s_hi = sum(r[0] for r in rows), sum(r[1] for r in rows)
        for j, (lo, hi) in enumerate(rows):
            out[(s, j)] = (lo / s_hi, hi / s_lo)
    return out


STATES = [(s // 12, s % 12) for s in range(144)]


def contained(enclosure, ref):
    E_dec, lo, hi = enclosure
    bad = []
    for (s, j), (r_lo, r_hi) in ref.items():
        e = Fraction(E_dec[s][j])
        if not (e / hi <= r_lo and r_hi <= e / lo):
            bad.append((s, j))
    return bad


def test_reference_code_agrees_with_the_old_enclosure_at_5_4():
    # pure reference check (no hwsb code): the unchanged process_law enclosure contains it
    old = process_law.softmax_enclosure(STATES[::7])
    saved = dict(process_law.LAW)
    assert saved["sigma"] == Fraction(5, 4)
    ref = reference_entries(STATES[::7], Fraction(5, 4))
    assert contained(old, ref) == []


def test_rounded_enclosure_contains_every_exact_w_star_entry_at_7_4():
    with hl.bound_law(Fraction(7, 4), Fraction(1, 5)):
        enc = hl.softmax_enclosure_rounded(STATES)
    ref = reference_entries(STATES, Fraction(7, 4))
    assert len(ref) == 144 * 36
    assert contained(enc, ref) == []
    _, lo, hi = enc
    assert 0 < lo < 1 < hi and hi / lo - 1 < Fraction(1, 10**50)  # sound and not vacuous


def test_planted_narrow_enclosure_is_caught_by_the_reference():
    with hl.bound_law(Fraction(7, 4), Fraction(1, 5)):
        E_dec, lo, hi = hl.softmax_enclosure_rounded(STATES[:3])
    ref = reference_entries(STATES[:3], Fraction(7, 4))
    shifted = [[v * (Decimal(1) + Decimal(1) / Decimal(10**30)) for v in row] for row in E_dec]
    assert contained((shifted, Fraction(1), Fraction(1)), ref)


# ------------------------------------------------------------------ law_bound
@pytest.fixture(scope="module")
def star():
    return hd.build_process(ArtifactStore(MemoryBackend()), masters=(620201,))


def law(proc, sigma, nb=Fraction(1, 5)):
    return hl.law_bound(proc["T"], proc["E_canon_shared"], proc["pi"], proc["coords"], sigma, nb)


def test_law_bound_w_star_is_bounded_with_kappa_below_one(star):
    res = law(star, Fraction(7, 4))
    assert res["status"] == "BOUNDED"
    assert isinstance(res["Z_bound"], Fraction) and res["Z_bound"] > 0
    assert res["kappa"] < 1 and res["delta"] > 0 and res["delta"] <= res["u"] * res["Q_max"]
    assert res["sigma"] == Fraction(7, 4) and res["neighbour"] == Fraction(1, 5)


def test_law_bound_default_arguments_are_w_star(star):
    res = hl.law_bound(star["T"], star["E_canon_shared"], star["pi"], star["coords"])
    assert res["status"] == "BOUNDED" and res["sigma"] == Fraction(7, 4)
    assert res["Z_bound"] == law(star, Fraction(7, 4))["Z_bound"]


def test_law_bound_sigma_3_2_is_bounded():
    # SPEC-QUESTION: TEST_PLAN says "at sigma = 3/2 BOUNDED"; read as a w(3/2) process
    # (emission sigma 1.5, same transition) so that the process matches the law's sigma.
    store = ArtifactStore(MemoryBackend())
    proc = hd.build_process(store, masters=(620201,),
                            emission_cfg=EmissionConfig("overlap", 36, 1.5, "grid"))
    res = law(proc, Fraction(3, 2))
    assert res["status"] == "BOUNDED" and res["Z_bound"] > 0 and res["delta"] > 0


def test_law_bound_w0_equals_contract_with_zero_delta():
    store = ArtifactStore(MemoryBackend())
    proc = hd.build_process(store, masters=(1729,),
                            emission_cfg=EmissionConfig("overlap", 36, 1.25, "grid"))
    res = law(proc, Fraction(5, 4))
    w0 = CONTRACT["known_cases"]["KB4"]["w0"]
    assert res["status"] == "BOUNDED"
    assert res["Z_bound"] == Fraction(w0["Z_bound"]) == Fraction(2116763197780003590583470649,
                                                                  10**39)
    assert res["delta"] == Fraction(w0["delta"]) == 0
    old = process_law.process_law_bound(proc["T"], proc["E_canon_shared"], proc["pi"],
                                        proc["coords"])
    assert Fraction(old["Z_bound"]["exact_upper"]) == res["Z_bound"]


# ------------------------------------------------------------------ restoration
def snapshot():
    return dict(process_law.LAW), process_law.softmax_enclosure


def test_bound_law_sets_and_restores_after_normal_exit():
    before, enc = snapshot()
    with hl.bound_law(Fraction(7, 4), Fraction(1, 5)):
        assert process_law.LAW["sigma"] == Fraction(7, 4)
        assert process_law.LAW["neighbour"] == Fraction(1, 5)
        assert process_law.softmax_enclosure is hl.softmax_enclosure_rounded
    after, enc_after = snapshot()
    assert after == before and enc_after is enc
    assert after["sigma"] == Fraction(5, 4) and enc_after is not hl.softmax_enclosure_rounded


def test_bound_law_restores_after_an_exception():
    before, enc = snapshot()
    with pytest.raises(RuntimeError, match="boom"):
        with hl.bound_law(Fraction(3, 2), Fraction(1, 5)):
            assert process_law.LAW["sigma"] == Fraction(3, 2)
            raise RuntimeError("boom")
    after, enc_after = snapshot()
    assert after == before and enc_after is enc


def test_law_bound_restores_after_normal_return_and_after_a_failure(star, monkeypatch):
    before, enc = snapshot()
    law(star, Fraction(7, 4))
    assert snapshot()[0] == before and snapshot()[1] is enc

    def fail(*a, **k):
        raise ValueError("planted")

    monkeypatch.setattr(process_law, "process_law_bound", fail)
    with pytest.raises(ValueError, match="planted"):
        law(star, Fraction(7, 4))
    monkeypatch.undo()
    assert snapshot()[0] == before and snapshot()[1] is enc


def test_digits_other_than_60_is_refused():
    from errors import Invalid
    with hl.bound_law(Fraction(7, 4), Fraction(1, 5)):
        with pytest.raises(Invalid):
            hl.softmax_enclosure_rounded(STATES[:2], digits=50)
