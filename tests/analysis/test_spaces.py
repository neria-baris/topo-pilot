import numpy as np
import pytest

from topo_pilot.analysis import PointSet, require_same_ids
from topo_pilot.contracts import ErrorCode, StageFailure

pytestmark = pytest.mark.analysis


def ps(space, ids):
    n = len(ids)
    return PointSet(space=space, X=np.zeros((n, 2)), D=None, ids=list(ids), metric="euclidean")


def test_equal_ids_pass_silently():
    assert require_same_ids(ps("belief32", ["a", "b", "c"]), ps("future1", ["a", "b", "c"])) is None


@pytest.mark.parametrize(
    "other",
    [
        ["a", "c", "b"],       # different order
        ["a", "b", "d"],       # different member
        ["a", "b"],            # shorter
        ["a", "b", "c", "d"],  # longer
    ],
)
def test_mismatched_ids_raise(other):
    with pytest.raises(StageFailure) as ei:
        require_same_ids(ps("belief32", ["a", "b", "c"]), ps("act:h", other))
    assert ei.value.code == ErrorCode.SAMPLE_ID_MISMATCH


def test_mismatch_symmetric():
    with pytest.raises(StageFailure) as ei:
        require_same_ids(ps("x", ["b", "a"]), ps("y", ["a", "b"]))
    assert ei.value.code == ErrorCode.SAMPLE_ID_MISMATCH
