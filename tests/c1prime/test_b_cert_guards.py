"""Independent tests (author B, job 0026), TEST_PLAN B-4 items 10, 11 and 13 (plus OUT and osum).

Protocol §15.3.4 constants, §15.3.2 kernels (ordered sums; no BLAS or numpy reduction), §15.3.11
B constants and the signed guards (E), (H), (V); CERTIFICATE.md §4 and §8; API.md §5 and §7.
Written from the protocol and the four contract documents only; no tools/c1prime source was read
and nothing was executed by the author. Item 13 inspects the named kernels at test run time with
`inspect.getsource` + `ast` (TEST_PLAN B-4 item 13); the author never viewed that source.

Guard floors and thresholds (10**-9, 1/100) are exact rationals (§15.3.11; CONTRACT numerics
"floor": "1e-9" as a string). The float 1e-9 is slightly above 10**-9, so |L| = 1e-9 clears the
floor while nextafter(1e-9, 0) does not. API.md does not fix whether `guard_endpoint` takes
per-model dicts; these tests pass dicts keyed by model seed.
"""

from __future__ import annotations

import ast
import importlib
import inspect
import math
import sys
import textwrap
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/c1prime", "tools/x4_circle_history", "tools/x4_oracle_profile",
             "tests/oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_bounds  # noqa: E402
import c1_cert  # noqa: E402

pytestmark = pytest.mark.analysis

U = Fraction(1, 2**53)
U1 = U / (1 - U)
ZETA = Fraction(1, 2**800)
MODELS = (1729, 2718, 3141)
NUM = "INCONCLUSIVE/NUMERICAL"


def _status(res) -> str:
    return res if isinstance(res, str) else res["status"]


def _gamma(n) -> Fraction:
    return n * U / (1 - n * U)


def _out(x) -> Fraction:
    return (1 + Fraction(1, 2**30)) * Fraction(x) + ZETA


# --- constants (item 11) ---


def test_exact_constants():
    assert Fraction(c1_cert.U) == U and Fraction(c1_cert.U1) == U1
    assert Fraction(c1_cert.ZETA) == ZETA
    for n in (1, 13, 16, 31, 35, 36):
        assert Fraction(c1_cert.gamma(n)) == _gamma(n)
    assert Fraction(c1_cert.C1HAT) == Fraction(0.1)
    assert Fraction(c1_cert.C3HAT) == Fraction(0.3)
    assert Fraction(c1_cert.DELTA1) == Fraction(1, 5 * 2**55)
    assert Fraction(c1_cert.DELTA1) == abs(Fraction(0.1) - Fraction(1, 10))
    assert Fraction(c1_cert.DELTA3) == Fraction(1, 5 * 2**54)
    assert Fraction(c1_cert.DELTA3) == abs(Fraction(0.3) - Fraction(3, 10))


@pytest.mark.parametrize("c", [Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), U1, _gamma(36),
                               Fraction(1, 10), Fraction(3, 10), ZETA, 1 / (1 - U),
                               Fraction(10**20 + 1), Fraction(1, 10**300)])
def test_up_is_the_smallest_float_not_below_c(c):
    v = c1_cert.up(c)
    assert isinstance(v, float)
    assert Fraction(v) >= c
    assert Fraction(math.nextafter(v, -math.inf)) < c


def test_up_of_floats_and_bound_constants():
    assert c1_cert.up(0.1) == 0.1 and c1_cert.up(Fraction(0.5)) == 0.5
    for value in c1_bounds.bound_constants().values():
        assert isinstance(float(value), float) and math.isfinite(float(value))


def test_OUT_is_exact():
    for x in (0.0, 0.5, 3e-12, 2.0**-1074, Fraction(1, 3)):
        assert Fraction(c1_cert.OUT(x)) == _out(x)


def test_osum_is_left_to_right():
    cols = [np.array([1e16, 1.0]), np.array([1.0, 1e16]), np.array([-1e16, -1e16]),
            np.array([1.0, 0.0])]
    got = np.asarray(c1_cert.osum(cols), dtype=np.float64)
    # row 0: ((1e16 + 1) - 1e16) + 1 = 1; row 1: ((1 + 1e16) - 1e16) + 0 = 0 (ties to even)
    assert got.tolist() == [1.0, 0.0]


# --- B constants (§15.3.11) ---


@pytest.mark.parametrize("n,depth", [(1, 0), (2, 1), (3, 2), (4096, 12), (4097, 13),
                                     (16384, 14), (20480, 15)])
def test_B_constant_uses_tree_depth_plus_one(n, depth):
    got = Fraction(c1_bounds.B_constant(3e-12, 0.7, n))
    assert got == _out(3e-12) + _gamma(depth + 1) * Fraction(0.7) + ZETA


# --- guards (item 10) ---


def _endpoint(L, U_, B):
    return _status(c1_bounds.guard_endpoint(L, U_, B))


def _models(*values):
    return dict(zip(MODELS, values))


def test_endpoint_guard_far_from_zero_passes_with_either_sign():
    B = _models(*(Fraction(1, 10**12),) * 3)
    assert _endpoint(_models(0.2, -0.3, 0.01), _models(0.4, -0.1, 0.5), B) == "PASS"


def test_endpoint_guard_floor_is_exactly_ten_to_minus_nine():
    B = _models(*(Fraction(0),) * 3)
    up_ = _models(1.0, 1.0, 1.0)
    assert _endpoint(_models(1e-9, 0.5, 0.5), up_, B) == "PASS"
    below = float(np.nextafter(1e-9, 0.0))
    assert _endpoint(_models(0.5, below, 0.5), up_, B) == NUM
    assert _endpoint(_models(0.5, 0.5, 0.5), _models(1.0, 1.0, -below), B) == NUM


def test_endpoint_guard_binding_B_and_equality():
    B = _models(Fraction(1, 10**8), Fraction(1, 10**12), Fraction(0.25))
    assert _endpoint(_models(1e-8, 0.5, 0.5), _models(1.0, 1.0, 1.0), B) == "PASS"
    below = float(np.nextafter(1e-8, 0.0))
    assert _endpoint(_models(below, 0.5, 0.5), _models(1.0, 1.0, 1.0), B) == NUM
    assert _endpoint(_models(0.5, 0.5, 0.5), _models(1.0, 1.0, -0.25), B) == NUM  # |U| == F


@pytest.mark.parametrize("lower,B_H,expected", [
    (0.5, Fraction(1, 10**12), "PASS"),
    (0.5, Fraction(0.5) - Fraction(1, 100), NUM),  # Gamma == g
    (0.5, Fraction(0.5) - Fraction(1, 100) - Fraction(1, 10**40), "PASS"),
    (0.005, Fraction(1, 100) - Fraction(0.005), "INCONCLUSIVE/HEADROOM"),  # Gamma == -g
    (0.005, Fraction(1, 100) - Fraction(0.005) + Fraction(1, 10**40), NUM),
    (0.01, Fraction(0), NUM),  # Gamma = 2.1e-19 > 0 but inside the 1e-9 floor
    (0.01 + 2e-9, Fraction(0), "PASS"),
    (0.01 - 2e-9, Fraction(0), "INCONCLUSIVE/HEADROOM"),
])
def test_h5_guard(lower, B_H, expected):
    assert _status(c1_bounds.guard_H5(lower, B_H)) == expected


@pytest.mark.parametrize("L,B,expected", [
    ([0.3, 0.2, 0.1], [Fraction(1, 10**12)] * 3, "PASS"),
    ([0.3, -0.2, 0.1], [Fraction(1, 10**12)] * 3, "INCONCLUSIVE/MODEL_HEADROOM"),
    ([0.3, 5e-10, 0.1], [Fraction(0)] * 3, NUM),
    ([0.3, 5e-10, -0.1], [Fraction(0)] * 3, "INCONCLUSIVE/MODEL_HEADROOM"),
    ([0.25, 0.3, 0.3], [Fraction(0.25), Fraction(0), Fraction(0)], NUM),  # Gamma_j == g_j
    ([-0.25, 0.3, 0.3], [Fraction(0.25), Fraction(0), Fraction(0)],
     "INCONCLUSIVE/MODEL_HEADROOM"),  # Gamma_j == -g_j
])
def test_v3_guard(L, B, expected):
    assert _status(c1_bounds.guard_V3(L, B)) == expected


# --- kernels: no BLAS, matmul or numpy reduction (item 13) ---

KERNELS = [
    ("c1_cert", "reference_oracle"), ("c1_cert", "osum"), ("c1_oracle", "G_hat"),
    ("c1_oracle", "G_named"), ("c1_endpoint", "A_hat"), ("c1_endpoint", "Y_hat"),
    ("c1_endpoint", "Z_hat"), ("c1_endpoint", "Zfull_hat"), ("c1_means", "tree_mean"),
    ("c1_means", "bootstrap_means"), ("c1_means", "c1_bootstrap_means"),
    ("c1_bounds", "b_G"), ("c1_bounds", "b_A"), ("c1_bounds", "b_Y"), ("c1_bounds", "b_Z"),
    ("c1_bounds", "b_Zf"),
]
FORBIDDEN = {"dot", "vdot", "inner", "matmul", "einsum", "tensordot", "sum", "nansum", "mean",
             "nanmean", "average", "prod", "cumsum"}


def _violations(func) -> list:
    tree = ast.parse(textwrap.dedent(inspect.getsource(func)))
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.BinOp, ast.AugAssign)) and isinstance(node.op, ast.MatMult):
            bad.append("@")
        elif isinstance(node, ast.Attribute) and node.attr == "linalg":
            bad.append("linalg")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            f = node.func
            if f.attr in FORBIDDEN:
                bad.append(f.attr)
            ufunc = f.value.attr if isinstance(f.value, ast.Attribute) else None
            if f.attr == "reduce" and ufunc in ("add", "multiply"):
                bad.append(f"{ufunc}.reduce")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"dot", "matmul", "einsum", "tensordot"}:
                bad.append(node.func.id)
    return bad


@pytest.mark.parametrize("module,name", KERNELS)
def test_certified_kernel_calls_no_blas_matmul_or_numpy_reduction(module, name):
    func = getattr(importlib.import_module(module), name)
    assert _violations(func) == []
