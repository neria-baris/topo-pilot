"""P13: x-periodicity is read from the world's complex, not from its family name."""

from __future__ import annotations

import dataclasses

import numpy as np
import pytest

from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.process._geometry import is_x_periodic, point_distances

pytestmark = pytest.mark.process


def test_P13_core_worlds(square12, cylinder12, square3, cylinder3):
    assert is_x_periodic(cylinder12) and is_x_periodic(cylinder3)
    assert not is_x_periodic(square12) and not is_x_periodic(square3)


def test_P13_family_name_is_ignored(square12, cylinder12):
    renamed_cyl = dataclasses.replace(cylinder12, family="square", identifications=())
    renamed_sq = dataclasses.replace(square12, family="cylinder")
    assert is_x_periodic(renamed_cyl)
    assert not is_x_periodic(renamed_sq)
    centers = np.array([[0.5, 0.5], [11.0, 3.0]])
    np.testing.assert_array_equal(point_distances(renamed_cyl, centers),
                                  point_distances(cylinder12, centers))


def test_P13_flipped_wrap_is_not_periodic(square12):
    """Möbius-style crossed wrap edges (11, y) ~ (0, 11 - y) do not make axis 0 periodic."""
    crossed = np.array([(11 - y, 11 * 12 + y) for y in range(12)], dtype=np.int32)
    edges = np.concatenate([square12.edges, np.sort(crossed, axis=1)])
    mobius = dataclasses.replace(square12, family="cylinder", edges=edges)
    assert not is_x_periodic(mobius)


def test_P13_partial_or_declared_without_edges_raises(square12, cylinder12):
    keep = [e for e in cylinder12.edges.tolist() if tuple(e) != (0, 132)]
    partial = dataclasses.replace(cylinder12, edges=np.array(keep, dtype=np.int32))
    declared = dataclasses.replace(square12, identifications=("x periodic",))
    for world in (partial, declared):
        with pytest.raises(StageFailure) as err:
            is_x_periodic(world)
        assert err.value.code == ErrorCode.INVALID_GLUE
