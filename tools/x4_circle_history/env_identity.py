"""Numerical implementation identity (API.md spec v2.4 item 12; builder-tested).

Standard library at import. `record()` describes the running interpreter after the fixed
scientific imports: interpreter and base DLL hashes, a tree digest of the base standard
library (Lib without site-packages/test/__pycache__, and DLLs), a tree digest of every
site-packages top-level distribution with a loaded module (plus its "<name>.libs"), and
informational platform / CPU-dispatch / thread-pool facts, which are verified too.

LIMITATION: OS DLLs outside these trees, CPU microarchitecture, microcode and runtime SIMD /
BLAS kernel selection are not bound by hashes. The per-row certificate measures the actual
float result in the same run, so certificate validity does not depend on them; bit-for-bit
reproducibility on other hardware is not claimed.

Usage (probe, venv interpreter): python -I env_identity.py   -> prints the JSON record.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import platform
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCIENTIFIC_IMPORTS = (
    "argparse",
    "decimal",
    "fractions",
    "hashlib",
    "json",
    "statistics",
    "zipfile",
    "zlib",
    "importlib.util",
    "numpy",
    "scipy",
    "scipy.optimize",
    "scipy.sparse",
    "scipy.sparse.linalg",
    "scipy.spatial.distance",
    "scipy.special",
    "ripser",
    "threadpoolctl",
    "topo_pilot.contracts",
    "topo_pilot.contracts.backends",
    "oracle_profile",
    "inputs",
    "controls",
    "independent_reference",
    "errors",
    "cochain",
    "chart",
    "scores",
    "precision",
    "error_bound",
    "reference_cache",
    "process_law",
    "stage_records",
    "op_guard",
    "precision_stage",
    "adapter",
    "release",
    "runner",
    "live_context",
)
_SKIP_DIRS = {"__pycache__", "site-packages", "test"}
LIMITATION = (
    "OS DLLs outside these trees, CPU microarchitecture, microcode and runtime SIMD / BLAS kernel "
    "selection are not bound by hashes. The per-row certificate measures the actual float result "
    "in the same run, so certificate validity does not depend on them; bit-for-bit "
    "reproducibility on other hardware is not claimed."
)


def ensure_paths() -> None:
    for extra in (
        REPO / "src",
        HERE,
        HERE.parent / "x4_oracle_profile",
        REPO / "tests" / "oracle_profile",
    ):
        if str(extra) not in sys.path:
            sys.path.insert(0, str(extra))


def import_scientific() -> None:
    ensure_paths()
    for name in SCIENTIFIC_IMPORTS:
        importlib.import_module(name)


def file_sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tree_digest(path: Path) -> str:
    """sha256 over sorted 'relpath:sha256' lines (a file: its own sha256)."""
    path = Path(path)
    if path.is_file():
        return file_sha(path)
    lines = []
    for p in sorted(path.rglob("*")):
        rel = p.relative_to(path)
        if p.is_file() and not (_SKIP_DIRS & set(rel.parts)):
            lines.append(f"{rel.as_posix()}:{file_sha(p)}")
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def _site_packages() -> Path:
    return Path(sys.prefix) / "Lib" / "site-packages"


def loaded_distributions(modules=None) -> list[str]:
    site = _site_packages().resolve()
    tops = set()
    for module in list((modules or sys.modules).values()):
        f = getattr(module, "__file__", None)
        if not f:
            continue
        p = Path(f).resolve()
        if site in p.parents:
            tops.add(p.relative_to(site).parts[0])
    return sorted(tops)


def unfrozen_project_modules(frozen_rel: set, modules=None) -> list[str]:
    """Loaded modules from this worktree's src/, tools/ or tests/ outside the frozen file set."""
    roots = [(REPO / d).resolve() for d in ("src", "tools", "tests")]
    bad = []
    for name, module in list((modules or sys.modules).items()):
        f = getattr(module, "__file__", None)
        if not f:
            continue
        p = Path(f).resolve()
        if any(r in p.parents for r in roots):
            rel = p.relative_to(REPO.resolve()).as_posix()
            if rel not in frozen_rel:
                bad.append(f"{name}: {rel}")
    return sorted(bad)


def _cpu_features() -> list[str]:
    try:
        from numpy._core._multiarray_umath import __cpu_features__
    except ImportError:  # pragma: no cover - numpy layout
        from numpy.core._multiarray_umath import __cpu_features__
    return sorted(k for k, v in __cpu_features__.items() if v)


def _threadpools() -> list[dict]:
    from threadpoolctl import threadpool_info

    keys = ("user_api", "internal_api", "version", "architecture", "filepath")
    return sorted(
        ({k: p.get(k) for k in keys} for p in threadpool_info()), key=lambda d: str(d["filepath"])
    )


def record(modules=None) -> dict:
    site = _site_packages()
    base = Path(sys.base_prefix)
    dists = {}
    for top in loaded_distributions(modules):
        dists[top] = tree_digest(site / top)
        name = top.split(".")[0]
        libs = site / f"{name}.libs"
        if libs.exists():
            dists[f"{name}.libs"] = tree_digest(libs)
    base_dlls = {
        p.name: file_sha(p) for p in sorted(base.glob("*.dll")) + sorted(base.glob("python.exe"))
    }
    return {
        "schema": "x4-circle-numerical-identity-v1",
        "python": {
            "version": sys.version,
            "executable": str(Path(sys.executable)),
            "executable_sha256": file_sha(sys.executable),
            "base_prefix": str(base),
            "base_binaries_sha256": base_dlls,
            "stdlib_lib_tree": tree_digest(base / "Lib"),
            "stdlib_dlls_tree": tree_digest(base / "DLLs"),
        },
        "site_packages": str(site),
        "distributions": dists,
        "informational_verified": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "numpy_cpu_features": _cpu_features(),
            "threadpools": _threadpools(),
        },
        "limitation": LIMITATION,
    }


def main() -> int:
    import_scientific()
    print(json.dumps(record(), indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
