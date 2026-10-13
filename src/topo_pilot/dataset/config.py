"""Dataset sizes (SPEC: DatasetConfig)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetConfig:
    """Sizes of the three splits and of the analysis panels.

    Invariants: ``n_test >= n_panels * panel_size`` (checked by ``PanelBuilder`` and the stage,
    ``ALIGNMENT_ERROR`` otherwise).
    """

    n_train: int = 131_072
    n_dev: int = 4_096
    n_test: int = 4_096
    n_panels: int = 8
    panel_size: int = 512
    analysis_position: int = 32
