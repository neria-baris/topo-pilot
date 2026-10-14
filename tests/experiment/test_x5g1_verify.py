"""Builder-authored tests of the X5 G1 verification comparison helper (job 0007)."""
import math

import pytest

from topo_pilot.experiment.x5g1_verify import TOL, _maxdiff

pytestmark = pytest.mark.experiment


def test_maxdiff_nested_values():
    assert _maxdiff({"a": [1.0, 2.0], "b": 3}, {"a": [1.0, 2.0 + 1e-13], "b": 3}) == \
        pytest.approx(1e-13, abs=1e-15)
    assert _maxdiff([None, True, "ok"], [None, True, "ok"]) == 0.0


def test_maxdiff_structure_mismatch_is_infinite():
    assert math.isinf(_maxdiff({"a": 1}, {"b": 1}))
    assert math.isinf(_maxdiff([1, 2], [1]))
    assert math.isinf(_maxdiff(None, 0.0))
    assert math.isinf(_maxdiff("ok", "NEAR_UNIT_GAP"))


def test_tolerance_boundary():
    assert _maxdiff(0.1, 0.1 + 0.5 * TOL) <= TOL
    assert _maxdiff(0.1, 0.1 + 2 * TOL) > TOL
