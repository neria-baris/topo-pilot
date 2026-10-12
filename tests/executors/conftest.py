"""Fixtures for the executors tests: a throw-away repository copy, stores, subprocess env."""

import shutil
from pathlib import Path

import pytest
from exec_helpers import make_store

from topo_pilot.contracts import ArtifactStore

REAL_REPO = Path(__file__).resolve().parents[2]
STUB_DIR = Path(__file__).resolve().parent


@pytest.fixture(scope="module")
def fake_repo(tmp_path_factory) -> Path:
    """A minimal repository (src, configs, pyproject, lock) plus planted secrets."""
    root = tmp_path_factory.mktemp("repo")
    shutil.copytree(REAL_REPO / "src", root / "src",
                    ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
    shutil.copytree(REAL_REPO / "configs", root / "configs",
                    ignore=shutil.ignore_patterns("local.yaml"))
    for name in ("pyproject.toml", "requirements.lock"):
        shutil.copy(REAL_REPO / name, root / name)
    (root / "configs" / "local.yaml").write_text("ssh: {host: secret-host}\n")
    (root / "configs" / "api_token.txt").write_text("hunter2\n")
    (root / ".env").write_text("KEY=1\n")
    return root


@pytest.fixture
def store(tmp_path) -> ArtifactStore:
    return make_store(tmp_path / "store")
