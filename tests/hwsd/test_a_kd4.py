"""Author A (job 0197): KD4 known-case fixtures (§6 KD4; API.md §12 plant_acts/seq_cases, §17.3).

Three layers:
1. the planted activations of cases (i)-(v) against an independent construction;
2. the §17.3 sequence readings on planted per-checkpoint rows that stand for each case
   (covariance before, with and after the chart; NEVER; NO_CHART; the step-0 control),
   through the real hwsd_statements.evaluate (fast, no chart code);
3. (slow) hwsd_dry.seq_cases end to end with the frozen KD4 parameter record.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(REPO / "tools" / "hwsd"), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import hwsd_config as dc  # noqa: E402, I001
import hwsd_dry as ddry  # noqa: E402
import hwsd_statements as dst  # noqa: E402
import k4b_scores  # noqa: E402
import test_a_hwsd_ref as ref  # noqa: E402

TWO_PI = 2.0 * math.pi
DRY = (629951, 629952, 629953)


def u_of(i):
    return int(hashlib.sha256(str(int(i)).encode()).hexdigest()[:16], 16) / 2**64


def g_ref(theta, a):
    """API.md §12: [0, 2*pi*a) -> [0, pi/6) and [2*pi*a, 2*pi) -> [pi/6, 2*pi), linear."""
    lo = TWO_PI * a
    th = np.asarray(theta, dtype=np.float64)
    return np.where(th < lo, th * (math.pi / 6) / lo,
                    math.pi / 6 + (th - lo) * (TWO_PI - math.pi / 6) / (TWO_PI - lo))


def fixture(n=256, seed=11):
    rng = np.random.default_rng(seed)
    ids = np.sort(rng.choice(10**9, size=n, replace=False)).astype(np.int64)
    ang32 = rng.uniform(0, TWO_PI, n)
    ang4 = rng.uniform(0, TWO_PI, n)
    m = {1: rng.normal(size=(n, 2)), 2: rng.normal(size=(n, 2)),
         4: 0.3 * np.column_stack((np.cos(ang4), np.sin(ang4))),
         32: 0.5 * np.column_stack((np.cos(ang32), np.sin(ang32)))}
    table = {"seq_ids": ids, "canon32": rng.integers(0, 36, size=(n, 32)).astype(np.uint8)}
    return table, m


def params(noise=0.0, g_mass=0.01):
    cases = dc.CONTRACT["known_cases"]["KD4"]["cases"]
    return {"noise": {c: noise for c in cases},
            "seeds": {c: 629970 + i for i, c in enumerate(cases)}, "g_mass": g_mass}


# ---- 1. planted activations ----
def test_case_ids_and_sequences_are_the_protocol_ones():
    kd4 = dc.CONTRACT["known_cases"]["KD4"]
    assert kd4["cases"] == ["i", "ii", "iii", "iv", "v"]
    assert {k: tuple(v) for k, v in kd4["sequences"].items()} == {
        k: v[0] for k, v in ref.KD4_EXPECTED.items()}
    assert kd4["expected_order_at_chart"] == {k: v[1] for k, v in ref.KD4_EXPECTED.items()}
    assert kd4["rows"] == 3072


@pytest.mark.parametrize("case", ["i", "ii", "iii", "iv", "v"])
def test_plant_acts_noise_free_matches_construction(case):
    table, m = fixture()
    A = ddry.plant_acts(case, table, m, params())
    n = len(table["seq_ids"])
    assert isinstance(A, np.ndarray) and A.dtype == np.float64 and A.shape == (n, 128)
    assert np.all(A[:, 2:] == 0.0)
    u = np.array([u_of(i) for i in table["seq_ids"]])
    if case == "i":
        np.testing.assert_allclose(A[:, 0], u, rtol=0, atol=1e-15)
        assert np.all(A[:, 1] == 0.0)
        return
    theta = {"ii": k4b_scores.m4_phase(m[4]), "iii": k4b_scores.oracle_phase(m[32]),
             "iv": g_ref(k4b_scores.oracle_phase(m[32]), 0.01), "v": TWO_PI * u}[case]
    np.testing.assert_allclose(A[:, 0], np.cos(theta), rtol=0, atol=1e-12)
    np.testing.assert_allclose(A[:, 1], np.sin(theta), rtol=0, atol=1e-12)
    np.testing.assert_allclose(A[:, 0] ** 2 + A[:, 1] ** 2, 1.0, rtol=0, atol=1e-12)


def test_plant_acts_case_iv_mass_in_first_arc():
    table, m = fixture(n=2000, seed=5)
    a = 0.05
    A = ddry.plant_acts("iv", table, m, params(g_mass=a))
    th_in = k4b_scores.oracle_phase(m[32])
    th_out = np.mod(np.arctan2(A[:, 1], A[:, 0]), TWO_PI)
    inside = th_in < TWO_PI * a
    assert np.all(th_out[inside] < math.pi / 6 + 1e-12)
    assert np.all(th_out[~inside] >= math.pi / 6 - 1e-12)
    order_in, order_out = np.argsort(th_in), np.argsort(th_out)  # g is monotone
    assert np.array_equal(order_in, order_out)


def test_plant_acts_noise_scale_and_seeds():
    table, m = fixture(n=512)
    p = params(noise=1e-6)
    A = ddry.plant_acts("i", table, m, p)
    rest = A[:, 2:]
    assert np.max(np.abs(rest)) <= 8e-6
    assert 0.8e-6 < float(np.std(rest)) < 1.2e-6
    assert abs(float(np.mean(rest))) < 1e-7
    u = np.array([u_of(i) for i in table["seq_ids"]])
    assert np.max(np.abs(A[:, 0] - u)) <= 8e-6
    assert np.array_equal(A, ddry.plant_acts("i", table, m, p))  # deterministic
    p2 = dict(p, seeds=dict(p["seeds"], i=p["seeds"]["i"] + 1))
    assert not np.array_equal(A, ddry.plant_acts("i", table, m, p2))
    B = ddry.plant_acts("iii", table, m, dict(p, noise=dict(p["noise"], iii=1e-3)))
    assert 0.8e-3 < float(np.std(B[:, 2:])) < 1.2e-3


# ---- 2. §17.3 readings on planted rows (each sequence identical for the three dry masters) ----
@pytest.mark.parametrize("name", list(ref.KD4_EXPECTED))
def test_kd4_sequence_readings_on_planted_rows(name):
    cases, order_c, e2, e3, e6 = ref.KD4_EXPECTED[name]
    t = ref.kd4_table(cases)
    ev = dst.evaluate(t)
    for j in DRY:
        o = ev["order"][j]["chart"]
        assert (o["category"] if isinstance(o, dict) else o) == order_c
    for s, e in (("D2", e2), ("D3", e3), ("D6", e6)):
        st = ev["statements"][s]
        assert st["reading"] == e[0], (name, s)
        if e[0] == "NOT_EVALUABLE":
            assert {r: sorted(v) for r, v in st["reasons"].items()} == {e[1]: list(DRY)}


def test_step0_control_reports_sigma_step0_and_k_C_plus():
    t = ref.kd4_table(("ii", "iii"))
    ev = dst.evaluate(t)
    for j in DRY:
        assert ev["onsets"][j]["k_C"] == 1 and ev["onsets"][j]["k_C_plus"] is None
        d = ev["diagnostics"][j]["chart_at_init"]
        assert d["sigma_step0"] == "EXCLUDE" and d["order_at_k_C_plus"] == "NO_CHART"


def test_before_sequence_unvalidated_case_is_not_an_onset():
    t = ref.kd4_table(("i", "iv", "iii", "iii"))
    ev = dst.evaluate(t)
    for j in DRY:
        assert ev["onsets"][j]["k_C"] == 3 and ev["onsets"][j]["k_B_S"] == 2
        assert ev["n_pre"][j] == 1


# ---- 3. end to end (slow; needs the frozen KD4 parameter record) ----
def _kd4_params():
    frozen = dc.CONTRACT["known_cases"]["KD4"]["parameters"]
    if not str(frozen.get("g", "")).startswith("TO_FREEZE"):
        return None  # seq_cases uses the frozen record by default
    path = os.environ.get("HWSD_KD4_PARAMS")
    if not path:
        # SPEC-QUESTION: before the freeze the DRD4-recorded parameters have no documented
        # location a test can read; set HWSD_KD4_PARAMS to that JSON record to run this test.
        pytest.skip("KD4 parameters are TO_FREEZE and HWSD_KD4_PARAMS is not set")
    return json.loads(Path(path).read_text(encoding="utf-8"))


@pytest.mark.slow
def test_seq_cases_end_to_end(tmp_path):
    p = _kd4_params()
    res = ddry.seq_cases(tmp_path / "kd4", params=p) if p else ddry.seq_cases(tmp_path / "kd4")
    assert res["status"] == "PASS"
    # API-AMBIGUITY: the result layout is "every case's status, label, point and SE and every
    # sequence's ORDER and D2/D3/D6 readings"; read it as res["cases"][c], res["sequences"][s].
    cases = res["cases"]
    assert cases["i"]["status"] == "CHART_UNAVAILABLE"
    assert cases["ii"]["status"] == "SCORED"
    assert abs(cases["ii"]["point"]) <= 4 * cases["ii"]["se"]
    assert cases["iii"]["status"] == "SCORED"
    assert cases["iv"]["status"] in ("SCORED_UNVALIDATED", "SCORED")  # fallback is recorded
    assert cases["v"]["status"] == "SCORED"
    for name, (_, order_c, e2, e3, e6) in ref.KD4_EXPECTED.items():
        if name == "BEFORE" and cases["iv"]["status"] != "SCORED_UNVALIDATED":
            continue  # §6: the BEFORE route is then checked by DRD5's planted tables only
        text = json.dumps(res["sequences"][name], default=str)
        for want in (order_c, e2[0], e3[0], e6[0]):
            assert want in text, (name, want)
    leftovers = [p for p in tmp_path.rglob("*") if p.name.startswith("HIST_")]
    assert leftovers == []
