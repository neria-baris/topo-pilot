"""Public API of ``topo_pilot.experiment`` (W0 skeleton: CLI, config layering, stage registry)."""

from . import s1 as _s1  # noqa: F401  (registers S1)
from . import s2 as _s2  # noqa: F401  (registers S2)
from .cli import main, status_lines
from .config import ResolvedConfig, load_config, producer_version
from .stages import STAGE_REGISTRY, Stage, register_stage, run_stage

__all__ = ["STAGE_REGISTRY", "ResolvedConfig", "Stage", "load_config", "main",
           "producer_version", "register_stage", "run_stage", "status_lines"]
