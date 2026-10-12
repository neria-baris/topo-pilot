"""World configuration value."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping


@dataclass(frozen=True)
class WorldConfig:
    """Configuration of a latent world.

    Parameters
    ----------
    family : registry key, ``"square"`` | ``"cylinder"`` (core); extensions add more.
    dims : lattice size per axis, e.g. ``(12, 12)``.
    metric : name of the primary metric ``dist`` (``"flat"`` or ``"graph"``).
    params : family-specific options.
    """

    family: str
    dims: tuple[int, ...] = (12, 12)
    metric: Literal["flat", "graph"] = "flat"
    params: Mapping[str, Any] = field(default_factory=dict)
