"""Author A (job 0223): KO1-KO3 at VAL and TEST (protocol 5.2; API_U2 4.1 KC-U, 4.6) and KS-RULES.

Synthetic oracle arrays: KO1 (A = G) RESPONDS, KO2 (A = 0) LOW_RESPONSE, KO3 (A = G/5)
WEAK_RESPONSE with rule 6; the categories are drawn through the phase-1 ko_categories with the
phase-2 seeds 640112 (VAL) and 640118 (TEST); a planted lambda != 1/5 is caught."""

from __future__ import annotations  # noqa: I001

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402
import hwsu_oracle as uo  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402


def mod(name):
    import u2  # noqa: F401

    return importlib.import_module(name)


def _probs(rng, n, V=36):
    x = rng.random((n, V)) + 0.05
    return x / x.sum(axis=1, keepdims=True)


@pytest.fixture(scope="module")
def world():
    """Tiny synthetic oracle: q32 per arm, a shared suffix predictive q4."""
    rng = np.random.default_rng(41)
    n = 600
    q1, q2, q4 = _probs(rng, n), _probs(rng, n), _probs(rng, n)
    o1, o2 = {"logq": np.log(q1)}, {"logq": np.log(q2)}
    s1 = s2 = {"logq4": np.log(q4)}
    d = q1 - q2
    G = 0.5 * np.sum(d * (o1["logq"] - o2["logq"]), axis=1)
    N = uo.helmert(36)
    A = {k: uo.readout_A(d, uo.ko_logits(o1, s1, k), uo.ko_logits(o2, s2, k), N)
         for k in ("KO1", "KO2", "KO3")}
    return G, A, (o1, o2, s1, s2, d, N)


def test_ko_identities(world):
    G, A, _ = world
    ids = uo.ko_identities(G, A)
    assert all(ids[k]["ok"] for k in ("KO1", "KO2", "KO3"))


@pytest.mark.parametrize("seed", [640112, 640118])
def test_ko_categories_at_val_and_test_seeds(world, seed):
    G, A, _ = world
    c = uo.ko_categories(G, A, seed)
    assert c["ok"]
    assert c["KO1"]["category"] == "RESPONDS" and c["KO1"]["rule6"] is False
    assert c["KO2"]["category"] == "LOW_RESPONSE" and c["KO2"]["rule6"] is False
    assert c["KO3"]["category"] == "WEAK_RESPONSE" and c["KO3"]["rule6"] is True


def test_contract_seed_uses():
    uses = uc.CONTRACT["seeds"]["uses_u2"]
    assert "VAL" in uses["640112"] and "TEST" in uses["640118"]


def test_planted_lambda_breaks_ko3(world):
    G, A, (o1, o2, s1, s2, d, N) = world
    l1 = s1["logq4"] + 0.25 * (o1["logq"] - s1["logq4"])
    l2 = s2["logq4"] + 0.25 * (o2["logq"] - s2["logq4"])
    bad = dict(A, KO3=uo.readout_A(d, l1, l2, N))
    assert not uo.ko_identities(G, bad)["KO3"]["ok"]


def test_kc_u_planted_lambda_fails_known_case(world, monkeypatch):
    """kc_u must fail closed FAIL_TECHNICAL/KNOWN_CASE when KO3 uses lambda != 1/5."""
    import c1_records

    G, A, (o1, o2, s1, s2, d, N) = world
    real = uo.ko_logits

    def planted(o, s, case):
        if case == "KO3":
            return s["logq4"] + 0.3 * (o["logq"] - s["logq4"])
        return real(o, s, case)

    monkeypatch.setattr(uo, "ko_logits", planted)
    ug = mod("hwsu_gates")
    ctx = {"o1": o1, "o2": o2, "s1": s1, "s2": s2, "G": G, "d": d,
           "pc": {"d": d, "G": G}, "val": {"o1": o1, "o2": o2, "s1": s1, "s2": s2, "G": G, "d": d}}
    with pytest.raises(c1_records.C1GateFailure) as e:
        ug.kc_u(ctx)
    assert e.value.status == "FAIL_TECHNICAL/KNOWN_CASE"


def test_ks_rules_passes(tmp_path):
    r = mod("hwsu_dry2").ks_rules(tmp_path)
    assert r["status"] == "PASS"
