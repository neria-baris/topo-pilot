import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.executors

SRC = Path(__file__).resolve().parents[2] / "src" / "topo_pilot" / "executors"
FORBIDDEN = {"world", "process", "dataset", "oracle", "learner", "activations", "prediction",
             "topology", "analysis", "experiment"}


def imported_modules(path: Path) -> list[str]:
    names = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            names.append(base)
            names += [f"{base}.{a.name}" for a in node.names]
    return names


def test_E07_no_science_or_experiment_imports():
    files = sorted(SRC.glob("*.py"))
    assert len(files) >= 8
    for path in files:
        for name in imported_modules(path):
            parts = name.split(".")
            assert not (parts[0] == "topo_pilot" and len(parts) > 1 and parts[1] in FORBIDDEN), \
                f"{path.name} imports {name}"


def test_E07_public_api_is_exactly_the_spec():
    import topo_pilot.executors as ex
    assert sorted(ex.__all__) == sorted([
        "BundleExecutor", "EXECUTOR_REGISTRY", "Executor", "JobHandle", "JobSpec",
        "LocalExecutor", "NotebookExporter", "SSHExecutor", "entry"])


def test_E07_requirements_filter_strips_local_suffix_and_skips_torch():
    from topo_pilot.executors import run_bundle_script as rb
    lock = "numpy==2.0.0\ntorch==2.3.0+cpu\ntorchvision==0.18.0+cpu  # c\nscipy==1.13.0\n"
    assert rb.filtered_requirements(lock, True) == [
        "numpy==2.0.0", "torchvision==0.18.0", "scipy==1.13.0"]
    assert "torch==2.3.0" in rb.filtered_requirements(lock, False)
