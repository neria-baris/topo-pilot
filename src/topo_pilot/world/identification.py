"""Gluing rule for one lattice axis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Identification:
    """Gluing rule for a lattice axis: kind in {'none','periodic','flipped'}; for 'flipped' the
    listed other axis is reversed when crossing (Möbius/Klein).

    Math
    ----
    Axis ``a`` of length ``n_a``: ``'periodic'`` glues ``(.., n_a, ..) ~ (.., 0, ..)``;
    ``'flipped'`` with ``flip_axis = f`` glues ``(x_a = n_a, y_f) ~ (0, n_f - 1 - y_f)``.

    Invariants
    ----------
    ``flip_axis`` is required for (and only allowed with) ``'flipped'`` and differs from
    ``axis``. Consistency against the lattice dims is checked by the builder (``INVALID_GLUE``).
    """

    axis: int
    kind: Literal["none", "periodic", "flipped"]
    flip_axis: int | None = None
