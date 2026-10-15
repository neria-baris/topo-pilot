"""Independent tests of the equal-gap templates in tools/d2a (job 0028, author A): T-TPL.

Written from D2A-FROZEN-v1 sections 5.2 (G0-TPL) and 9.2 and tools/d2a/API.md section 2.1 only.
Exact identities come from d1_seam.exact_history (Fractions); the enumeration order is
re-implemented here from the API text.
"""

from __future__ import annotations

import hashlib
import sys
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

import pytest

from topo_pilot.contracts import SeedTree

REPO_ROOT = Path(__file__).resolve().parents[2]
for _parts in (("tools", "d2a"), ("tools", "d1_seam"), ("tools", "x4_oracle_profile")):
    if str(REPO_ROOT.joinpath(*_parts)) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT.joinpath(*_parts)))

import d1_seam  # noqa: E402
import d2a_targets as TG  # noqa: E402
import d2a_world as W  # noqa: E402

pytestmark = pytest.mark.oracle

DATA = 2026101531
S0, S2, S3, A, B = 0, 1, 2, 3, 4
Q1_DECISION = [Q(1, 5), Q(1, 5), Q(3, 5), Q(0), Q(0)]
Y_LAW = [Q(2, 3), Q(1, 3), Q(0)]  # on column 3, states 3x + y = 9, 10, 11


def _member(r1, x5, r9, exc, j):
    h = [r1, S2, S3, S0, x5, S2, S3, S0, r9, S2, S3]
    if j == 0:
        h.append(S3)
    for i, e in enumerate(exc, 1):
        h += [e, S3]
        if i == j:
            h.append(S3)
    return tuple(h)


def _my_enumeration(t):
    n = (t - 12) // 2
    return [(_member(r1, A, r9, exc, j), _member(r1, B, r9, exc, j))
            for r1 in (A, B) for r9 in (A, B) for exc in product((S2, S0), repeat=n)
            for j in range(n + 1)]


# Hand-built templates (protocol section 9.2), one per t, with their API enumeration index.
HAND = {
    16: ((A, S2, S3, S0, A, S2, S3, S0, B, S2, S3, S2, S3, S3, S0, S3),
         (A, S2, S3, S0, B, S2, S3, S0, B, S2, S3, S2, S3, S3, S0, S3), 16),
    28: ((B, S2, S3, S0, A, S2, S3, S0, A, S2, S3, S0, S3, S2, S3, S0, S3, S0, S3, S2, S3, S2,
          S3, S0, S3, S2, S3, S3),
         (B, S2, S3, S0, B, S2, S3, S0, A, S2, S3, S0, S3, S2, S3, S0, S3, S0, S3, S2, S3, S2,
          S3, S0, S3, S2, S3, S3), 6218),
}


def _pairs(t):
    return [(tuple(a), tuple(b)) for a, b in W.template_enumeration(t)]


def test_T_TPL_counts():
    assert len(_pairs(16)) == 48 == 4 * 2**2 * 3
    assert len(_pairs(28)) == 9216 == 4 * 2**8 * 9
    assert len(set(_pairs(28))) == 9216


@pytest.mark.parametrize("t", [16, 28])
def test_T_TPL_enumeration_order_follows_api(t):
    assert _pairs(t) == _my_enumeration(t)
    a, b, idx = HAND[t]
    assert len(a) == len(b) == t
    assert _pairs(t)[idx] == (a, b)


@pytest.mark.parametrize("t", [16, 28])
def test_T_TPL_structure_of_every_pair(t):
    for a, b in _pairs(t):
        assert len(a) == len(b) == t and a[-1] == b[-1] == S3
        assert (a[4], b[4]) == (A, B)  # x5 = A member first
        assert a[:4] + a[5:] == b[:4] + b[5:]  # the pair differs only at position 5
        assert a[-8:] == b[-8:]  # identical final 8-symbol windows (position 5 <= t - 8)
        assert a[1:4] == (S2, S3, S0) and a[5:8] == (S2, S3, S0) and a[9:11] == (S2, S3)
        assert a.count(S3) == 3 + (t - 12) // 2 + 1  # base, one per excursion, one dwell


@pytest.mark.parametrize("t", [16, 28])
def test_T_TPL_exact_identities_at_hand_template(t):
    a, b, _ = HAND[t]
    ea, eb = d1_seam.exact_history(a), d1_seam.exact_history(b)
    assert ea["P"] > 0 and eb["P"] > 0  # reachable
    assert (ea["pi"], eb["pi"]) == (Q(1, 4), Q(3, 4))
    for e in (ea, eb):
        assert e["b_C"] == e["b_M"] == [Q(0)] * 9 + Y_LAW
        assert e["Q1"] == Q1_DECISION
    assert d1_seam.tv(ea["J"], eb["J"]) == Q(1, 150)
    assert d1_seam.tv(ea["Q2dist"], eb["Q2dist"]) == Q(1, 150)
    assert a[-8:] == b[-8:]


def test_T_TPL_canonical_pair_windows_differ_and_are_not_required_equal():
    ha, hb = d1_seam.H_A, d1_seam.H_B
    ea, eb = d1_seam.exact_history(ha), d1_seam.exact_history(hb)
    assert len(ha) == 11 and ha[-8:] != hb[-8:]  # members differ at position 5, inside w4..w11
    assert (ea["pi"], eb["pi"]) == (Q(1, 4), Q(3, 4))
    delta = [Q(int(s == 9)) for s in range(12)]
    assert ea["b_C"] == ea["b_M"] == eb["b_C"] == eb["b_M"] == delta
    assert d1_seam.tv(ea["J"], eb["J"]) == Q(1, 100)
    assert d1_seam.tv(ea["Q2dist"], eb["Q2dist"]) == Q(1, 100)


def test_T_TPL_registered_templates():
    assert [tuple(map(tuple, p)) for p in W.registered_templates(16)] == _pairs(16)
    reg = [tuple(map(tuple, p)) for p in W.registered_templates(28)]
    assert len(reg) == 256 and len(set(reg)) == 256
    idx = SeedTree(DATA).generator("d2a", "templates", 28).choice(9216, 256, replace=False)
    full = _pairs(28)
    assert reg == [full[int(i)] for i in idx]
    assert [tuple(map(tuple, p)) for p in W.registered_templates(28)] == reg  # deterministic


@pytest.mark.parametrize("t", [16, 28])
def test_template_hashes(t):
    got = list(W.template_hashes(t))
    reg = W.registered_templates(t)
    assert len(got) == len(reg)
    for h, (a, b) in zip(got, reg, strict=True):
        want = hashlib.sha256(bytes(tuple(a) + tuple(b))).hexdigest()
        assert str(h).lower() == want


def test_registered_templates_exact_g0_tpl_sample():
    """Every 32nd registered t = 28 pair and every 8th t = 16 pair, exactly (G0-TPL values)."""
    for t, step in ((16, 8), (28, 32)):
        for a, b in list(W.registered_templates(t))[::step]:
            ea, eb = d1_seam.exact_history(tuple(a)), d1_seam.exact_history(tuple(b))
            assert (ea["pi"], eb["pi"]) == (Q(1, 4), Q(3, 4))
            assert ea["b_C"] == ea["b_M"] == eb["b_C"] == eb["b_M"] == [Q(0)] * 9 + Y_LAW
            assert ea["Q1"] == eb["Q1"] == Q1_DECISION
            assert d1_seam.tv(ea["J"], eb["J"]) == Q(1, 150)
            assert d1_seam.tv(ea["Q2dist"], eb["Q2dist"]) == Q(1, 150)


def test_g0_tpl_gate_passes():
    gate = TG.g0_tpl()
    assert gate["status"] == "PASS"
    assert gate["checks"] and all(bool(v) for v in gate["checks"].values())
