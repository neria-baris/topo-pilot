"""Public API of ``topo_pilot.executors`` (see SPEC.md): run a job locally, through a portable
bundle, or over ssh."""

from .base import EXECUTOR_REGISTRY, Executor, JobHandle, JobSpec
from .bundle import BundleExecutor
from .entry import entry
from .local import LocalExecutor
from .notebook import NotebookExporter
from .ssh import SSHExecutor

__all__ = ["BundleExecutor", "EXECUTOR_REGISTRY", "Executor", "JobHandle", "JobSpec",
           "LocalExecutor", "NotebookExporter", "SSHExecutor", "entry"]
