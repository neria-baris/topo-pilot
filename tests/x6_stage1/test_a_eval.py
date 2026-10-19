"""Author A: T-EVAL and T-QUANT (X6S1-FROZEN-v1 §2.2, §10.2 T13/T17/T20/T25, §14.3; API.md §2, §7).

Model-dependent checks use a synthetic TransformerLM (MODEL_CFG shapes, an arbitrary torch seed;
never a real checkpoint). The quantiser has an independent reference implementation here; the
readout floor is checked in 50-digit Decimal on exact closed-form laws."""
from __future__ import annotations

import copy
import hashlib
import math
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np
import pytest
import torch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6_stage1"))

import x6s1_data as sd  # noqa: E402
import x6s1_cloud as sc  # noqa: E402
import x6s1_eval as se  # noqa: E402
import x6s1_stats as ss  # noqa: E402

if str(REPO / "tools" / "x6_stage0") not in sys.path:  # reused code (the modules add it too)
    sys.path.append(str(REPO / "tools" / "x6_stage0"))
import x6_model as xm  # noqa: E402
from topo_pilot.learner import TransformerLM  # noqa: E402

Q, EPS = 2**20, Fraction(1, 10**6)
FLOOR = Fraction(1012287, 10**12)
ANCHOR = 10


def walks(n_rows: int, seed: int) -> np.ndarray:
    rng, out = np.random.default_rng(seed), np.zeros((n_rows, 33), np.uint8)
    for i in range(n_rows):
        v = int(rng.integers(16))
        for c in range(33):
            out[i, c] = 15 + int(rng.integers(3)) if v == ANCHOR else xm.tok(v)
            v = xm.NEIGHBOURS[v][int(rng.integers(5))]
    return out


@lru_cache(maxsize=None)
def synth_state():
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(1234567)
        model = TransformerLM(sd.MODEL_CFG)
    return {k: v.detach().clone() for k, v in model.state_dict().items()}


@lru_cache(maxsize=None)
def predictor():
    return se.ModelPredictor.from_state(synth_state(), "init-s1")


def ref_probs(tokens, t):
    """Independent float64 forward: input [BOS, w_1..w_32], softmax of logits[i, t_i]."""
    model = TransformerLM(sd.MODEL_CFG)
    model.load_state_dict(copy.deepcopy(synth_state()))
    model = model.double().eval()
    x = np.concatenate([np.full((len(tokens), 1), 18), tokens[:, :32].astype(np.int64)], 1)
    with torch.no_grad():
        logits = model(torch.from_numpy(x)).logits
    t = np.broadcast_to(np.asarray(t, np.int64), (len(tokens),)).copy()
    return torch.softmax(logits[torch.arange(len(tokens)), torch.from_numpy(t)], -1).numpy()


# ---------------------------------------------------------------- T-EVAL
def test_pad_and_model_inputs():
    hs = [(1, 2, 3), (), tuple(range(15)) + (16,) * 18]
    p = se.pad(hs)
    assert p.dtype == np.uint8 and p.shape == (3, 33) and p.flags["C_CONTIGUOUS"]
    assert p[0].tolist() == [1, 2, 3] + [0] * 30 and not p[1].any() and p[2].tolist() == list(hs[2])
    toks = walks(5, 1)
    x = se.model_inputs(toks)
    x = x.numpy() if isinstance(x, torch.Tensor) else np.asarray(x)
    assert x.dtype == np.int64 and x.shape == (5, 33)
    assert (x[:, 0] == 18).all() and (x[:, 1:] == toks[:, :32]).all()


def test_readout_position_index():
    toks = walks(6, 2)
    for t in (1, 5, 17, 32):
        got = predictor()(toks, t)
        assert got.dtype == np.float64 and got.shape == (6, 18)
        assert np.max(np.abs(got - ref_probs(toks, t))) <= 1e-13
        for other in (t - 1, t + 1):
            if 0 <= other <= 32:
                assert np.max(np.abs(got - ref_probs(toks, other))) > 1e-9
        moved = toks.copy()                       # w_{t+1}..w_33 never reach the readout at t
        moved[:, t:] = (moved[:, t:] + 7) % 18
        assert np.array_equal(predictor()(moved, t), got)
        moved = toks.copy()                       # w_t does
        moved[:, t - 1] = (moved[:, t - 1] + 5) % 18
        assert np.max(np.abs(predictor()(moved, t) - got)) > 1e-9


def test_padding_independence():
    toks = walks(8, 3)
    for t in (1, 7, 20, 31, 32):
        padded = se.pad([tuple(r[:t]) for r in toks])
        assert np.array_equal(predictor()(padded, t), predictor()(toks, t))


def test_float64_determinism_vector_t_and_normalisation():
    toks = walks(40, 4)
    t = np.array([1 + (i % 32) for i in range(40)])
    a, b = predictor()(toks, t), predictor()(toks, t)
    assert np.array_equal(a, b)                                   # bitwise repeatable
    assert np.max(np.abs(a.sum(1) - 1)) <= 1e-12 and (a >= 0).all()   # T20 precondition
    assert np.max(np.abs(a - ref_probs(toks, t))) <= 1e-13
    for i in (0, 13, 31):                                           # row-wise t semantics
        assert np.max(np.abs(a[i] - predictor()(toks[i:i + 1], int(t[i]))[0])) <= 1e-15


def test_model_predictor_from_verified_file(tmp_path):
    buf = tmp_path / "w.pt"
    torch.save({"model": synth_state()}, buf)
    fsha = hashlib.sha256(buf.read_bytes()).hexdigest()
    wsha = sc.weights_digest(synth_state())
    toks = walks(4, 5)
    p = se.ModelPredictor(str(buf), fsha, wsha)
    assert np.array_equal(p(toks, 32), predictor()(toks, 32))
    with pytest.raises(Exception):
        se.ModelPredictor(str(buf), "0" * 64, wsha)
    with pytest.raises(Exception):
        se.ModelPredictor(str(buf), fsha, "0" * 64)


def test_oracle_predictor_and_qstar_codes():
    toks = walks(30, 6)
    qv = ss.qvals()
    for t in (1, 9, 32):
        exact = [xm.closed_form("NA", tuple(int(w) for w in r[:t]))["q"] for r in toks]
        want = np.array([[float(x) for x in q] for q in exact])
        assert np.array_equal(se.OraclePredictor("NA", "qstar")(toks, t), want)
        q, codes = se.qstar("NA", toks, t)
        assert np.array_equal(q, want) and codes.dtype == np.int16 and codes.shape == (30, 18)
        for i, law in enumerate(exact):
            assert [qv[c] for c in codes[i]] == list(law)
            assert all((c == 0) == (x == 0) for c, x in zip(codes[i], law))


def test_kl_rows_zeros_and_infinity():
    q = np.array([[0.5, 0.5, 0.0, 0.0], [0.25, 0.25, 0.5, 0.0], [0.0, 1.0, 0.0, 0.0]])
    p = np.array([[0.25, 0.25, 0.25, 0.25], [0.25, 0.25, 0.0, 0.5], [0.5, 0.5, 0.0, 0.0]])
    q, p = np.pad(q, ((0, 0), (0, 14))), np.pad(p, ((0, 0), (0, 14)))
    kl = se.kl_rows(q, p)
    assert kl.dtype == np.float64 and kl.shape == (3,)
    assert kl[0] == pytest.approx(math.log(2), abs=1e-15)          # zeros in q* contribute 0
    assert kl[1] == math.inf                                       # q > 0 = p
    assert kl[2] == pytest.approx(math.log(2), abs=1e-15)
    assert se.kl_rows(q[:1], q[:1])[0] == 0.0


def test_cue_mass_and_cue_normalise():
    p = np.zeros((4, 18))
    p[0, :15], p[0, 15:] = 0.8 / 15, (0.1, 0.05, 0.05)
    p[1, :15] = 1 / 15                                              # no cue mass
    p[2, 15:] = (np.inf, 0.0, 0.0)                                  # non-finite normaliser
    p[3, 15:] = 1 / 3
    m = se.cue_mass(p)
    assert m[0] == pytest.approx(0.2, abs=1e-15) and m[1] == 0.0 and m[3] == pytest.approx(1.0)
    c = se.cue_normalise(p)
    assert c.dtype == np.float64 and c.shape == (4, 3)
    assert c[0] == pytest.approx([0.5, 0.25, 0.25], abs=1e-15)
    assert np.isnan(c[1]).all() and np.isnan(c[2]).all()
    assert c[3] == pytest.approx([1 / 3] * 3, abs=1e-15)


# ---------------------------------------------------------------- T-QUANT
def my_quantise(s):
    r = s * Q
    f = np.floor(r)
    out = np.zeros(s.shape, np.int64)
    for i in range(len(s)):
        R = Q - int(f[i].sum())
        assert 0 <= R <= 18
        fr = r[i] - f[i]
        k = f[i].astype(np.int64)
        for j in sorted(range(18), key=lambda j: (-fr[j], j))[:R]:
            k[j] += 1
        out[i] = k
    return out


def random_laws(n, seed):
    rng = np.random.default_rng(seed)
    s = rng.dirichlet(np.full(18, 0.4), size=n)
    s[rng.random((n, 18)) < 0.3] = 0.0
    s[:, 0] += (s.sum(1) == 0)
    s[: n // 4] *= rng.random((n // 4, 18)) ** 8                   # tiny entries too
    s[: n // 4, 1] += 1e-3
    return s / s.sum(1, keepdims=True)


def test_quantise_conservation_and_independent_reference():
    s = random_laws(4000, 7)
    k = se.quantise(s)
    assert k.dtype == np.int64 and k.shape == s.shape
    assert (k.sum(1) == Q).all()                                    # T13 conservation
    up = k - np.floor(s * Q).astype(np.int64)
    assert ((up == 0) | (up == 1)).all() and (up.sum(1) <= 18).all()   # 0 <= R <= 18
    assert np.array_equal(k, my_quantise(s))
    assert (k[s == 0] == 0).all()                                   # zero rule


def test_quantise_ties_and_zero_rule_hand_cases():
    def law(entries):
        s = np.zeros(18)
        for j, v in entries.items():
            s[j] = v
        return s
    third = law({0: 1 / 3, 1: 1 / 3, 2: 1 / 3})
    k = se.quantise(third[None])[0]
    assert k[:3].tolist() == [349526, 349525, 349525] and not k[3:].any()   # tie: lower index
    eighteenth = se.quantise(np.full((1, 18), 1 / 18))[0]
    assert eighteenth.tolist() == [58255] * 4 + [58254] * 14              # R = 4
    z = law({1: 1 / 3, 2: 1 / 3, 3: 1 / 3})                                 # zero at index 0
    kz = se.quantise(z[None])[0]
    assert kz[0] == 0 and kz[1:4].tolist() == [349526, 349525, 349525]
    h = law({1: 0.5, 2: 1 / 6, 3: 1 / 6, 4: 1 / 6})                         # frac 0 at index 1
    kh = se.quantise(h[None])[0]
    assert kh[:5].tolist() == [0, 524288, 174763, 174763, 174762]
    exact = law({5: 0.25, 6: 0.25, 7: 0.5})                                  # R = 0
    assert se.quantise(exact[None])[0][5:8].tolist() == [262144, 262144, 524288]


@pytest.mark.parametrize("bad", ["sum_high", "sum_low", "negative", "nan", "inf"])
def test_quant_invalid(bad):
    s = np.full((2, 18), 1 / 18)
    if bad == "sum_high":
        s[1, 0] += 1e-9
    elif bad == "sum_low":
        s[1, 0] -= 1e-11
    elif bad == "negative":
        s[1, 0], s[1, 1] = -1e-20, 2 / 18                         # sum still 1: sign only
    else:
        s[1, 0] = np.nan if bad == "nan" else np.inf
    with pytest.raises(se.QuantInvalid):
        se.quantise(s)
    assert issubclass(se.QuantInvalid, ValueError)
    ok = np.full((1, 18), 1 / 18)
    ok[0, 0] += 5e-13                                               # inside |sum - 1| <= 1e-12
    assert se.quantise(ok).sum() == Q


def test_readout_exact_positivity_and_float():
    k = se.quantise(random_laws(50, 8))
    for row in k[:10]:
        p = se.readout_exact(row)
        assert all(isinstance(x, Fraction) for x in p) and sum(p) == 1
        assert list(p) == [(1 - EPS) * Fraction(int(x), Q) + EPS / 18 for x in row]
        assert min(p) >= EPS / 18
    r = se.readout(k)
    want = np.array([[float((1 - EPS) * Fraction(int(x), Q) + EPS / 18) for x in row] for row in k])
    assert r.dtype == np.float64 and np.allclose(r, want, rtol=1e-15, atol=0)
    assert (r >= float(EPS / 18) * (1 - 1e-15)).all()
    # B = 17 bounds every per-row excess: ln(18 / eps) < 17
    assert math.log(18 / 1e-6) < 17


def _dec(fr):
    return Decimal(fr.numerator) / Decimal(fr.denominator)


def test_readout_floor_on_exact_laws_t17():
    hists = [(15,), (16,) + (9,) * 31, (0, 1, 2, 3, 7, 6, 5, 4, 8), (17, 9, 5, 4)]
    toks = walks(150, 9)
    hists += [tuple(int(w) for w in r[:1 + i % 32]) for i, r in enumerate(toks)]
    with localcontext() as ctx:
        ctx.prec = 50
        worst = Decimal(0)
        for h in hists:
            q = [Fraction(x) for x in xm.closed_form("NA", h)["q"]]
            assert min(x for x in q if x) >= Fraction(1, 750)
            k = se.quantise(np.array([[float(x) for x in q]]))[0]
            p = se.readout_exact(k)
            kl = sum((_dec(a) * (_dec(a).ln() - _dec(b).ln()) for a, b in zip(q, p) if a),
                     Decimal(0))
            worst = max(worst, kl)
        assert worst <= _dec(FLOOR) + Decimal("1e-12")
