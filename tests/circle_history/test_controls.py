"""Independent tests (author B) for the validation controls and the error taxonomy: TEST_PLAN
items B15 and B16 (spec v2.4).

Written from API.md (spec v2.4 items 1 and 10), CONTRACT.json and TEST_PLAN.md only; no
production code was read. Expected values: hand-made rows normalised here, sha256 phases from
hashlib, and a manual re-run of the documented resampling loop with an identically seeded
Generator(PCG64(seed)).

Interpretation (reported): control_summary's result is read as out[name][model] with keys
"point", "central95" and "bonferroni" ("Per name and model" in API.md).
"""

from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_circle_history", "tools/x4_oracle_profile", "tests/oracle_profile"):
    if str(REPO_ROOT / _sub) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT / _sub))

import adapter  # noqa: E402
import errors  # noqa: E402
import precision  # noqa: E402
import scores  # noqa: E402

pytestmark = pytest.mark.analysis

NAMES = ("m1_unit", "m4_unit", "sha256_last4")
MODELS = (1729, 2718, 3141)


# ---- B15: control_scores ----
def _hand_phase(last4) -> float:
    digest = hashlib.sha256(bytes(int(v) for v in last4)).digest()
    return 2 * math.pi * int.from_bytes(digest[:8], "big") / 2**64


def test_control_scores_equal_unit_dot_residual() -> None:
    m1 = np.array([[0.0, 0.0], [3.0, -4.0], [1e-3, 2e-3]])
    m4 = np.array([[0.25, -0.5], [0.0, 0.0], [-7.0, 0.0]])
    m32 = np.array([[1.0, 1.0], [0.5, -0.25], [2.0, 3.0]])
    hist = np.zeros((3, 32), dtype=np.int64)
    hist[:, 28:] = [[0, 1, 2, 3], [2, 2, 2, 2], [1, 0, 1, 0]]
    out = scores.control_scores(m1, m4, m32, hist)
    assert set(out) == set(NAMES)
    resid = m32 - m4
    units = {"m1_unit": [], "m4_unit": [], "sha256_last4": []}
    for r in range(3):
        for name, m in (("m1_unit", m1), ("m4_unit", m4)):
            norm = math.hypot(*m[r])
            units[name].append((1.0, 0.0) if norm == 0.0 else tuple(m[r] / norm))
        phase = _hand_phase(hist[r, 28:])
        units["sha256_last4"].append((math.cos(phase), math.sin(phase)))
    for name in NAMES:
        want = [u[0] * resid[r, 0] + u[1] * resid[r, 1] for r, u in enumerate(units[name])]
        np.testing.assert_allclose(np.asarray(out[name]), want, rtol=0, atol=1e-14)
    assert float(np.asarray(out["m1_unit"])[0]) == 0.75     # exact (0, 0) -> (1, 0): 1 - 0.25
    assert float(np.asarray(out["m4_unit"])[1]) == 0.5      # exact (0, 0) -> (1, 0): 0.5 - 0


# ---- B15: control_summary ----
N_ROWS, DRAWS, SEED = 9, 130, 410201
BASE = 0.05 * np.cos(np.arange(N_ROWS) * 1.7)     # off any grid: draw means rarely tie


def _controls() -> dict:
    return {"m1_unit": {m: BASE + 0.001 * k for k, m in enumerate(MODELS)},
            "m4_unit": {m: 2.0 * (BASE + 0.001 * k) + 0.5 for k, m in enumerate(MODELS)},
            "sha256_last4": {m: np.sin(np.arange(N_ROWS) * (k + 1.0))
                             for k, m in enumerate(MODELS)}}


def _manual_draws(C: dict) -> dict:
    rng = np.random.Generator(np.random.PCG64(SEED))
    vals = {name: {m: [] for m in MODELS} for name in C}
    for _ in range(DRAWS):
        idx = rng.integers(0, N_ROWS, size=N_ROWS)      # ONE call per draw, shared by all
        for name in C:
            for m in MODELS:
                vals[name][m].append(np.mean(C[name][m][idx]))
    return {name: {m: np.array(v) for m, v in per.items()} for name, per in vals.items()}


def test_control_summary_reproduces_shared_index_stream() -> None:
    C = _controls()
    out = precision.control_summary(C, MODELS, SEED, DRAWS)
    assert not {"status", "decision", "criterion_met"} & set(out)   # reported, never gated
    vals = _manual_draws(C)
    probs = {"central95": (0.025, 0.975), "bonferroni": (0.05 / 3, 1 - 0.05 / 3)}
    for name in NAMES:
        for m in MODELS:
            rec = out[name][m]
            assert rec["point"] == pytest.approx(float(np.mean(C[name][m])), rel=1e-14,
                                                 abs=1e-16)
            for key, (lo, hi) in probs.items():
                want = [np.quantile(vals[name][m], p, method="inverted_cdf") for p in (lo, hi)]
                np.testing.assert_allclose(np.asarray(rec[key], dtype=float), want,
                                           rtol=1e-12, atol=1e-15)
    # 130 draws: .025 -> 4th, .975 -> 127th, .05/3 -> 3rd, 1 - .05/3 -> 128th order statistic,
    # so the two intervals use different order statistics
    srt = np.sort(vals["m1_unit"][MODELS[0]])
    assert out["m1_unit"][MODELS[0]]["central95"][0] == pytest.approx(srt[3], abs=1e-15)
    assert out["m1_unit"][MODELS[0]]["bonferroni"][0] == pytest.approx(srt[2], abs=1e-15)
    # sharing across controls: m4_unit = 2 * m1_unit + 0.5 row-wise, so every quantile maps
    for m in MODELS:
        for key in probs:
            np.testing.assert_allclose(np.asarray(out["m4_unit"][m][key], dtype=float),
                                       2.0 * np.asarray(out["m1_unit"][m][key], dtype=float)
                                       + 0.5, rtol=1e-12, atol=1e-14)
    # sharing across models: model k is model 0 shifted by 0.001 k
    for k, m in enumerate(MODELS):
        np.testing.assert_allclose(np.asarray(out["m1_unit"][m]["central95"], dtype=float),
                                   np.asarray(out["m1_unit"][MODELS[0]]["central95"],
                                              dtype=float) + 0.001 * k, rtol=0, atol=1e-14)


def _bad_summaries() -> dict:
    nonfinite = _controls()
    nonfinite["m4_unit"][MODELS[1]] = nonfinite["m4_unit"][MODELS[1]].copy()
    nonfinite["m4_unit"][MODELS[1]][4] = np.nan
    unequal = _controls()
    unequal["sha256_last4"][MODELS[2]] = unequal["sha256_last4"][MODELS[2]][:-1]
    single = {name: {m: v[:1] for m, v in per.items()} for name, per in _controls().items()}
    unknown = dict(_controls(), m2_unit={m: BASE for m in MODELS})
    duplicate = {name: {m: per[m] for m in MODELS[:2]} for name, per in _controls().items()}
    return {"nonfinite": (nonfinite, MODELS), "unequal_lengths": (unequal, MODELS),
            "n_lt_2": (single, MODELS), "unknown_name": (unknown, MODELS),
            "duplicate_models": (duplicate, (1729, 1729, 2718)),
            "empty_models": ({name: {} for name in NAMES}, ())}


@pytest.mark.parametrize("case", sorted(_bad_summaries()))
def test_control_summary_fail_closed(case: str) -> None:
    C, models = _bad_summaries()[case]
    with pytest.raises(errors.Invalid):
        precision.control_summary(C, models, SEED, DRAWS)


# ---- B16: taxonomy ----
def test_error_classes_unchanged() -> None:
    classes = (errors.Invalid, errors.Unresolved, errors.AccessDenied, errors.JoinError)
    for a in classes:
        assert issubclass(a, RuntimeError)
        for b in classes:
            assert a is b or not issubclass(a, b), (a, b)


def test_join_failure_is_join_error_never_unresolved() -> None:
    canon = np.zeros((2, 32), dtype=np.int64)
    canon[1, 0] = 1
    per_model = {1729: {"sequence_id": np.array([1, 2]), "canonical32": canon,
                        "panel": np.array([1, 1])},
                 2718: {"sequence_id": np.array([1, 3]), "canonical32": canon.copy(),
                        "panel": np.array([1, 1])}}
    with pytest.raises(errors.JoinError) as exc:
        adapter.cross_model_join(per_model)
    assert not isinstance(exc.value, errors.Unresolved)
