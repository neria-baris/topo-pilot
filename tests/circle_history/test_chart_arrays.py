"""Independent synthetic tests, author A (spec v2.3): chart_to_arrays / chart_from_arrays
exact round trip (TEST_PLAN A13).

Written from tools/x4_circle_history/API.md, CONTRACT.json and TEST_PLAN.md only.
"""

from __future__ import annotations

import io
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PKG = REPO_ROOT / "tools" / "x4_circle_history"
if str(PKG) not in sys.path:
    sys.path.insert(0, str(PKG))

import chart  # noqa: E402

pytestmark = pytest.mark.analysis

TWO_PI = 2.0 * math.pi
CHART_KEYS = (
    "field", "lift_bounds", "lift_node_limit", "lift_cpu_cap_s", "lift_rounding_tol",
    "local_passes", "local_vertices", "extension_k", "support_min_resultant",
    "fidelity_min_agreement", "phase_bins", "phase_bin_min_rows", "overall_resultant_max",
    "smoothing_residual_max",
)
ARRAY_FIELDS = ("landmark_ids", "landmarks", "phi", "d8", "edges", "cocycle", "integer_lift",
                "lift_correction", "primitive", "tree_potential")
INT_FIELDS = ("edges", "cocycle", "integer_lift", "lift_correction", "primitive",
              "tree_potential")
INFO_KEYS = ("birth", "death", "radius", "bar_index", "n_edges", "n_triangles",
             "smoothing_residual")


def make_cfg(**overrides):
    chart_cfg = json.loads((PKG / "CONTRACT.json").read_text(encoding="utf-8"))["chart"]
    cfg = {key: chart_cfg[key] for key in CHART_KEYS}
    cfg["lift_bounds"] = list(cfg["lift_bounds"])
    cfg.update(overrides)
    return cfg


THETA = TWO_PI * np.arange(48) / 48


def circle_points(theta):
    r = 1.0 + 0.02 * np.cos(7 * theta + 0.4)
    return np.column_stack([r * np.cos(theta), r * np.sin(theta),
                            0.03 * np.sin(3 * theta + 1.1), 0.02 * np.cos(5 * theta + 2.3)])


@pytest.fixture(scope="module")
def fitted():
    ids = np.array([f"h{k:04d}" for k in range(48)])
    c = chart.fit_chart(circle_points(THETA), ids, make_cfg())
    gauge = chart.fit_gauge(c, np.column_stack([np.cos(THETA), np.sin(THETA)]))
    return c, gauge


def assert_round_trip(back, gback, original, gauge):
    for name in ARRAY_FIELDS:
        got, want = np.asarray(getattr(back, name)), np.asarray(getattr(original, name))
        assert got.shape == want.shape and np.array_equal(got, want), name
        if name in INT_FIELDS:
            assert got.dtype == np.int64, name
        if name in ("landmarks", "phi", "d8"):
            assert got.dtype == np.float64, name
    assert back.landmark_ids.tolist() == original.landmark_ids.tolist()
    assert back.sigma == original.sigma and back.support_radius == original.support_radius
    assert int(back.period_gcd) == int(original.period_gcd)
    for key in INFO_KEYS:
        assert back.info[key] == original.info[key], key
    assert (int(gback.sign), gback.shift, gback.alignment) == (
        int(gauge.sign), gauge.shift, gauge.alignment)


def test_chart_arrays_round_trip_exact(fitted):
    c, gauge = fitted
    arrays = chart.chart_to_arrays(c, gauge)
    assert all(isinstance(k, str) and isinstance(v, np.ndarray) for k, v in arrays.items())
    back, gback = chart.chart_from_arrays(arrays)
    assert isinstance(back, chart.Chart) and isinstance(gback, chart.Gauge)
    assert_round_trip(back, gback, c, gauge)
    again = chart.chart_to_arrays(back, gback)  # second trip is the identity on arrays
    assert sorted(again) == sorted(arrays)
    for key, value in arrays.items():
        assert again[key].dtype == value.dtype and np.array_equal(again[key], value), key


def test_chart_arrays_survive_npz_without_pickle(fitted):
    # Possibly strict: assumes the arrays are plain (non-object) so allow_pickle=False loads them,
    # in line with docs/CONVENTIONS.md "never use pickle".
    c, gauge = fitted
    buffer = io.BytesIO()
    np.savez(buffer, **chart.chart_to_arrays(c, gauge))
    buffer.seek(0)
    with np.load(buffer, allow_pickle=False) as npz:
        loaded = {key: npz[key] for key in npz.files}
    back, gback = chart.chart_from_arrays(loaded)
    assert_round_trip(back, gback, c, gauge)


def test_round_trip_preserves_extension(fitted):
    c, gauge = fitted
    back, gback = chart.chart_from_arrays(chart.chart_to_arrays(c, gauge))
    queries = circle_points(THETA + 0.05)
    first = chart.extend(c, gauge, queries, make_cfg())
    second = chart.extend(back, gback, queries, make_cfg())
    for name in ("phase", "resultant", "eighth_distance", "supported", "duplicate"):
        assert np.array_equal(getattr(first, name), getattr(second, name)), name
