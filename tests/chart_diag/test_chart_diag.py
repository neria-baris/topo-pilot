"""Builder tests of tools/chart_diag (job 0023): synthetic geometry only, no E4 artifact access."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "tools" / "chart_diag") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "tools" / "chart_diag"))

import chart_diag as cd  # noqa: E402


def _ids(n):
    return np.array([f"h{k:04d}" for k in range(n)])


def _circle(n, rng, radius=1.0, noise=0.01, dim=4):
    t = np.sort(rng.uniform(0, 2 * np.pi, n))
    X = np.zeros((n, dim))
    X[:, 0], X[:, 1] = radius * np.cos(t), radius * np.sin(t)
    return X + noise * rng.standard_normal((n, dim))


def test_components_follow_edge_list_rule():
    D = np.array([[0, 1, 5, 5], [1, 0, 5, 5], [5, 5, 0, 2], [5, 5, 2, 0]], dtype=float)
    count, labels = cd.components(D, 1.0)  # edge (0,1) only: D <= r is inclusive
    assert count == 3 and labels[0] == labels[1] and len({labels[2], labels[3]}) == 2
    assert cd.components(D, 2.0)[0] == 2
    assert cd.components(D, 0.5)[0] == 4  # no edges at all
    assert cd.components(D, 5.0)[0] == 1


def test_x_interval_and_verdict_rule():
    assert cd.x_interval(1.0, 3.0) == {"lower": 1.0, "upper": 3.0, "empty": False, "length": 2.0}
    assert cd.x_interval(3.0, 3.0)["empty"] and cd.x_interval(4.0, 3.0)["length"] == 0.0
    assert cd.verdict([0.95] * 6) == "GO"
    assert cd.verdict([1.0] * 5 + [0.9499]) == "STOP"
    assert cd.verdict([1.0] * 6, invalid=True) == "INVALID"


def test_connected_circle_has_full_giant():
    X = _circle(60, np.random.default_rng(0))
    g = cd.geometry(X, _ids(60))
    assert g["n"] == 60 and g["components_at_r"] == {"count": 1, "sizes": [60]}
    assert g["giant_fraction"] == 1.0 and g["outside_giant"] == []
    assert g["bar"]["r"] == pytest.approx((g["bar"]["b"] + g["bar"]["d"]) / 2)
    # MST of a dense circle is far shorter than the circle's death: X's interval is non-empty
    assert g["l_max_h0"] < g["bar"]["d"] and not g["x_interval"]["empty"]


def test_far_outlier_is_reported_outside_giant():
    rng = np.random.default_rng(1)
    X = _circle(60, rng)
    X[17] = [0.0, 0.0, 50.0, 0.0]  # isolated point with the largest norm
    g = cd.geometry(X, _ids(60))
    assert g["components_at_r"]["count"] == 2 and g["components_at_r"]["sizes"] == [59, 1]
    assert g["giant_fraction"] == pytest.approx(59 / 60)
    (out,) = g["outside_giant"]
    assert out["history_id"] == "h0017" and out["norm_rank"] == 1 and out["component_size"] == 1
    assert out["nn_distance"] == pytest.approx(
        np.linalg.norm(X[17] - np.delete(X, 17, 0), axis=1).min()
    )
    # the outlier's MST edge dominates: l_max >= d, so X's interval is empty
    assert g["l_max_h0"] >= g["bar"]["d"] and g["x_interval"]["empty"]


def test_k4_landmark_checks_are_applied():
    X = _circle(20, np.random.default_rng(2))
    with pytest.raises(Exception, match="ascending"):
        cd.geometry(X, _ids(20)[::-1])
    X[3, 0] = np.nan
    with pytest.raises(Exception, match="finite"):
        cd.geometry(X, _ids(20))


def test_reused_k4_files_match_freeze():
    rep = cd.integrity()
    assert rep["reused_unchanged"], rep["reused"]
    assert not rep["job0018"]["bar_recoverable"]  # 0018 logged operation timings only
    assert rep["job0018"]["chart_calibration_gate"]["status"] == "INCONCLUSIVE"
