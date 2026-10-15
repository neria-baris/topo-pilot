"""Independent tests (author B, job 0026), TEST_PLAN B-3: RidgeProbe / nested_ridge equivalence.

Protocol §7 pipeline steps 1-5 (correction C-14) and §16 row 9 (equivalence <= 1e-10, part of
M1); API.md §9 `fit_decoder`. Written from the protocol and the four contract documents only; no
tools/c1prime source was read and nothing was executed by the author. The reference re-runs the
§7 recipe with the unchanged `x4f_scores`, `x4f_probe.nested_ridge`, `RidgeProbe` and the §2.3
SeedTree streams for the bandwidth subsample and the RFF map.

The fixture's target is pure noise, so the selected lambda is large and the Cholesky (nested
ridge) and least-squares (RidgeProbe) solves agree far below 1e-10 on the calibration features.
This is the most expensive file of the author-B set (two 2048-feature ridge paths on 160 rows).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest
from topo_pilot.analysis.x4f_scores import rbf_bandwidth, rbf_features, rbf_map, standardizer
from topo_pilot.contracts import SeedTree
from topo_pilot.experiment.x4f_probe import nested_ridge
from topo_pilot.prediction.ridge import RidgeProbe

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/c1prime", "tools/x4_circle_history", "tools/x4_oracle_profile",
             "tests/oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_fit  # noqa: E402
import c1_records  # noqa: E402

pytestmark = pytest.mark.analysis

GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0)
MODEL, TARGET = 1729, "m32"


def _reference(a_cal, Y, panel, a_new):
    mu_a, s_a = standardizer(a_cal)
    at = (a_cal - mu_a) / s_a
    bw = SeedTree(0).generator("c1-sf-v1", "rbf_bandwidth", MODEL, TARGET)
    ell, _ = rbf_bandwidth(at, bw, 1024)
    omega, beta = rbf_map(128, 2048, ell, SeedTree(0).generator("c1-sf-v1", "rbf", MODEL, TARGET))
    F = rbf_features(at, omega, beta)
    nr = nested_ridge(F, Y, panel, F, Y, grid=GRID)
    mu_F, s_F = standardizer(F)
    Ft = (F - mu_F) / s_F
    probe = RidgeProbe([nr.lam]).fit(Ft, Y, Ft, Y)
    equivalence = float(np.max(np.abs(probe.predict(Ft) - nr.pred_val)))
    Fn = (rbf_features((a_new - mu_a) / s_a, omega, beta) - mu_F) / s_F
    return probe.predict(Fn), equivalence


def test_decoder_refit_matches_nested_ridge_and_the_section7_recipe():
    rng = np.random.default_rng(1)
    a_cal = rng.normal(size=(160, 128))
    Y = rng.normal(size=(160, 2))
    panel = np.repeat(np.arange(8), 20)
    a_new = rng.normal(size=(9, 128))
    expected, equivalence = _reference(a_cal, Y, panel, a_new)
    assert equivalence <= 1e-10  # fixture precondition (protocol claim, C-14)
    dec = c1_fit.fit_decoder(a_cal, Y, panel, MODEL, TARGET)
    assert float(dec.equivalence) <= 1e-10
    assert abs(float(dec.equivalence) - equivalence) <= 1e-12
    got = np.asarray(dec.predict(a_new), dtype=np.float64).reshape(expected.shape)
    np.testing.assert_allclose(got, expected, rtol=0, atol=1e-9)


def test_degenerate_bandwidth_is_rbf_degenerate():
    a_cal = np.tile(np.linspace(-1.0, 1.0, 128), (40, 1))  # identical rows: median distance 0
    Y = np.random.default_rng(2).normal(size=(40, 2))
    with pytest.raises(c1_records.C1GateFailure) as info:
        c1_fit.fit_decoder(a_cal, Y, np.repeat(np.arange(8), 5), MODEL, TARGET)
    assert info.value.status == "INCONCLUSIVE/RBF_DEGENERATE"
