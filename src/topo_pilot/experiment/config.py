"""Layered config loading: base.yaml -> stages.yaml -> local.yaml (untracked)."""

from __future__ import annotations

import hashlib
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from topo_pilot.contracts import ErrorCode, StageFailure, canonical_json


@dataclass(frozen=True)
class ResolvedConfig:
    """The resolved configuration of one invocation.

    ``base`` holds the closed decisions, ``stages`` the per-stage overrides, ``local`` the
    machine-specific settings (executor hosts, artifact root). ``config_hash`` is
    ``sha256(canonical_json({"base": base, "stages": stages}))[:16]``; ``local`` is excluded so
    that the hash, like artifact ids, does not depend on the machine.
    """

    repo_root: Path
    base: Mapping[str, Any]
    stages: Mapping[str, Any]
    local: Mapping[str, Any] = field(default_factory=dict)

    @property
    def config_hash(self) -> str:
        blob = canonical_json({"base": self.base, "stages": self.stages})
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]

    def stage(self, stage_id: str) -> Mapping[str, Any]:
        """The settings block of ``stage_id`` (empty if absent)."""
        return self.stages.get(stage_id) or {}

    @property
    def artifact_root(self) -> Path:
        """Store root: ``local.yaml: artifact_root`` if set, else ``<repo>/artifacts``."""
        root = self.local.get("artifact_root")
        return Path(root) if root else self.repo_root / "artifacts"


def _read_yaml(path: Path, required: bool) -> dict[str, Any]:
    if not path.is_file():
        if required:
            raise StageFailure(ErrorCode.INVALID_CONFIG, "experiment.config", "missing_file",
                               f"config file not found: {path.name}")
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise StageFailure(ErrorCode.INVALID_CONFIG, "experiment.config", "yaml_mapping",
                           f"{path.name} must hold a mapping")
    return data


def load_config(stages_path: Path, repo_root: Path | None = None) -> ResolvedConfig:
    """Read ``base.yaml`` and ``local.yaml`` from the folder of ``stages_path``."""
    stages_path = Path(stages_path)
    cfg_dir = stages_path.parent
    root = Path(repo_root) if repo_root else cfg_dir.resolve().parent
    return ResolvedConfig(repo_root=root, base=_read_yaml(cfg_dir / "base.yaml", True),
                          stages=_read_yaml(stages_path, True),
                          local=_read_yaml(cfg_dir / "local.yaml", False))


def producer_version(repo_root: Path) -> str:
    """``<git sha>`` plus ``+dirty`` when the work tree has uncommitted changes; ``unknown``
    if git is unavailable."""
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=repo_root, capture_output=True, text=True,
                              check=True, timeout=30).stdout.strip()
    try:
        sha = git("rev-parse", "--short=12", "HEAD")
        dirty = bool(git("status", "--porcelain", "--untracked-files=no"))
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return f"{sha}+dirty" if dirty else sha
