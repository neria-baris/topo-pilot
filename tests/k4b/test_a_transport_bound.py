"""K4b author A, correction round 2 (ruling R25): k4b_cert.transport_bound (API.md §7).

transport_bound(T, E, pi, coords) returns the reused process_law.process_law_bound result with
Z_bound as an exact fractions.Fraction. The reused function reports Z_bound as the dict
{"exact_upper": str(x), "float": float(x)}, so the Fraction must be Fraction(exact_upper),
never Fraction(float). A non-BOUNDED status raises C1GateFailure("FAIL_TECHNICAL/IDENTITY").

The real law is loaded on the job-0014 path (inputs.load_config(), inputs.load_process(cfg));
E is the canonical emission shared bitwise by the three models (API §2, E_canon_shared)."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry",
             "tools/x4_circle_history", "tools/x4_oracle_profile"):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import k4b_cert  # noqa: E402
import process_law  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

FLOOR = Fraction(1, 10 ** 9)
GRID40 = 10 ** 40  # process_law reports upper bounds on the 1e-40 grid


@pytest.fixture(scope="module")
def law_args():
    import inputs
    import oracle_profile

    proc = inputs.load_process(inputs.load_config())
    canon = [oracle_profile.canonical_emission(proc["E_named"][s], proc["perm"][s])
             for s in proc["E_named"]]
    assert len(canon) == 3
    for c in canon[1:]:  # E_canon_shared: bitwise identical across the three models
        assert np.array_equal(c, canon[0]) and c.tobytes() == canon[0].tobytes()
    assert proc["T"].shape == (144, 144) and canon[0].shape == (144, 36)
    return proc["T"], canon[0], proc["pi"], proc["coords"]


@pytest.fixture(scope="module")
def real(law_args):
    ref = process_law.process_law_bound(*law_args)
    assert ref["status"] == "BOUNDED"  # the frozen kernel itself bounds the documented law
    return ref, k4b_cert.transport_bound(*law_args)


# ---------------------------------------------------------------- real documented law

def test_real_status_bounded_and_reused_keys_kept(real):
    ref, res = real
    assert isinstance(res, dict) and res["status"] == "BOUNDED"
    for key, value in ref.items():  # the reused result is returned, only Z_bound converted
        assert key in res
        if key != "Z_bound":
            assert res[key] == value, key


def test_real_z_bound_is_exact_fraction_of_exact_upper(real):
    ref, res = real
    z = res["Z_bound"]
    assert type(z) is Fraction
    assert isinstance(ref["Z_bound"], dict) and isinstance(ref["Z_bound"]["exact_upper"], str)
    assert z == Fraction(ref["Z_bound"]["exact_upper"])
    assert (z * GRID40).denominator == 1  # on the report grid: an exact string, not a float


def test_real_z_bound_sanity_band(real):
    z = real[1]["Z_bound"]
    assert Fraction(0) < z < Fraction(1, 10 ** 6)  # job 0018 reported about 2.12e-12


def test_real_downstream_margin_and_f_plan(real):
    z = real[1]["Z_bound"]
    for b in (Fraction(3, 10 ** 8), Fraction(1, 10 ** 12), Fraction(0)):
        m = k4b_cert.margin(b, z)
        assert type(m) is Fraction and m == max(b, FLOOR) + z
    fp = k4b_cert.F_plan(z)
    assert type(fp) is Fraction and fp > z
    assert fp == k4b_cert.F_plan(Fraction(0)) + z


# ---------------------------------------------------------------- synthetic reused report

def _dummy():
    S, V = 144, 36
    return np.eye(S), np.full((S, V), 1.0 / V), np.full(S, 1.0 / S), np.zeros((S, 2))


def _patch(monkeypatch, report):
    calls = []

    def fake(T, E, pi, coords):
        calls.append((T, E, pi, coords))
        return report

    monkeypatch.setattr(process_law, "process_law_bound", fake)
    monkeypatch.setattr(k4b_cert, "process_law_bound", fake, raising=False)
    return calls


def _bounded(exact):
    return {"status": "BOUNDED", "kappa": {"exact_upper": "1/100", "float": 0.01},
            "Z_bound": {"exact_upper": exact, "float": float(Fraction(exact))}, "claim": "x"}


@pytest.mark.parametrize("exact,want", [
    ("3/7", Fraction(3, 7)),
    (f"{212 * 10 ** 26 + 1}/{GRID40}", Fraction(212 * 10 ** 26 + 1, GRID40)),
])
def test_synthetic_exact_upper_gives_exact_fraction(monkeypatch, exact, want):
    args = _dummy()
    calls = _patch(monkeypatch, _bounded(exact))
    res = k4b_cert.transport_bound(*args)
    assert len(calls) == 1
    for got, sent in zip(calls[0], args):  # the matrices are passed through unchanged
        assert np.array_equal(np.asarray(got), sent)
    z = res["Z_bound"]
    assert res["status"] == "BOUNDED" and type(z) is Fraction and z == want
    assert z != Fraction(float(want)) and res["kappa"]["exact_upper"] == "1/100"
    m = k4b_cert.margin(Fraction(1, 10 ** 12), z)
    assert type(m) is Fraction and m == FLOOR + want
    assert k4b_cert.F_plan(z) > z


@pytest.mark.parametrize("status", ["UNAVAILABLE", "bounded", "INVALID"])
def test_synthetic_non_bounded_raises_identity(monkeypatch, status):
    _patch(monkeypatch, {"status": status, "reason": "synthetic", "claim": "no bound"})
    with pytest.raises(C1GateFailure) as exc:
        k4b_cert.transport_bound(*_dummy())
    assert exc.value.status == "FAIL_TECHNICAL/IDENTITY"


def test_real_kernel_unavailable_raises_identity():
    """Unpatched: coords that are not the documented 12x12 lattice make the reused kernel
    return UNAVAILABLE (lattice mismatch at state 1); transport_bound must refuse it."""
    args = _dummy()
    assert process_law.process_law_bound(*args)["status"] == "UNAVAILABLE"
    with pytest.raises(C1GateFailure) as exc:
        k4b_cert.transport_bound(*args)
    assert exc.value.status == "FAIL_TECHNICAL/IDENTITY"
