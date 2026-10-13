"""DiscriminabilityTable: S for every reference space (stage S2)."""

from __future__ import annotations

from typing import Mapping, Sequence

from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow

from .pointset import PointSet, ph_summary
from .spaces import SpaceBuilder

_RUN_ID = "S2"


class DiscriminabilityTable:
    """Compute S (H1 signal) and the scale s for world, emission, beliefs and futures.

    Math
    ----
    ``S = max finite H1 persistence / s`` of each space (RESEARCH_SUMMARY 7.3); Hellinger for
    distributions, the world metric for the world.

    Shapes
    ------
    ``refs[(world, condition)] = {"world": id, "emission": id, "oracle": id}``; ``panels`` are
    panel numbers 1..8. World rows are computed once per world (condition None, panel None);
    emission rows once per (world, condition) (panel None); belief32, belief1, future1, future2
    once per (world, condition, panel).

    Returns
    -------
    ``MetricRecords`` (not saved) with rows ``run_id="S2"``, metric ids ``S_H1`` and ``scale_s``,
    the PH status propagated, and ``parent_ids`` the artifacts the row came from.
    """

    def __init__(self, store: ArtifactStore):
        self._spaces = SpaceBuilder(store)

    @staticmethod
    def _rows(ps: PointSet, world: str, condition: str | None, panel: int | None,
              parents: tuple[str, ...]) -> list[MetricRow]:
        res = ph_summary(ps)
        common = dict(run_id=_RUN_ID, space=ps.space, status=res["status"], world=world,
                      condition=condition, panel=panel, parent_ids=parents)
        return [MetricRow(metric_id="S_H1", value=float(res["S_H1"]), **common),
                MetricRow(metric_id="scale_s", value=float(res["scale_s"]), **common)]

    def compute(self, refs: Mapping[tuple[str, str], Mapping[str, str]],
                panels: Sequence[int]) -> MetricRecords:
        """Build the table (see class docstring); never saves."""
        rows: list[MetricRow] = []
        done_worlds: set[str] = set()
        for (world, condition), ref in refs.items():
            if world not in done_worlds:
                done_worlds.add(world)
                rows += self._rows(self._spaces.world(ref["world"]), world, None, None,
                                   (ref["world"],))
            rows += self._rows(self._spaces.emission(ref["emission"]), world, condition, None,
                               (ref["emission"],))
            oid = ref["oracle"]
            for panel in panels:
                sets = (self._spaces.beliefs(oid, "b32", panel),
                        self._spaces.beliefs(oid, "b1", panel),
                        self._spaces.futures(oid, 1, panel),
                        self._spaces.futures(oid, 2, panel))
                for ps in sets:
                    rows += self._rows(ps, world, condition, panel, (oid,))
        return MetricRecords(rows=tuple(rows))
