"""NotebookExporter: a minimal three-cell ``.ipynb`` that runs a bundle (no Drive, no services)."""

from __future__ import annotations

import json
from pathlib import Path

CELL_UNPACK = '''\
# 1. Unpack the bundle. Upload {name} to the working directory first (Colab: Files panel;
#    Kaggle: add it as a dataset input and set BUNDLE below to its path).
import pathlib, tarfile
BUNDLE = None
found = [pathlib.Path(BUNDLE)] if BUNDLE else (
    sorted(pathlib.Path(".").glob("{name}"))
    + sorted(pathlib.Path("/kaggle/input").rglob("{name}")))
assert found, "{name} not found: upload it, or set BUNDLE"
with tarfile.open(found[0]) as tar:
    tar.extractall(".")
import os
os.chdir("{top}")
'''

CELL_INSTALL = '''\
# 2. Install requirements.lock (local version suffixes stripped; torch kept if present).
import subprocess, sys
subprocess.run([sys.executable, "run_bundle.py", "--install-only"], check=True)
'''

CELL_RUN = '''\
# 3. Run the job and pack the outputs, then download outputs_{job}.tar.gz from the file browser.
import subprocess, sys
result = subprocess.run([sys.executable, "run_bundle.py", "--no-install"])
print("exit code", result.returncode)
print(sorted(p.name for p in __import__("pathlib").Path(".").glob("outputs_*.tar.gz")))
'''


class NotebookExporter:
    """Writes a minimal nbformat-4 notebook: unpack, install the lock, run and pack."""

    def export(self, bundle_path: Path, dest: Path) -> Path:
        """Write the notebook for ``bundle_<job>.tar.gz``.

        Parameters
        ----------
        bundle_path : the bundle produced by ``BundleExecutor.submit``.
        dest : a ``.ipynb`` file path, or a folder (then ``notebook_<job>.ipynb`` is created).

        Returns
        -------
        Path of the notebook. It has exactly 3 code cells and no outputs.
        """
        name = Path(bundle_path).name
        top = name[: -len(".tar.gz")] if name.endswith(".tar.gz") else Path(name).stem
        job = top[len("bundle_"):] if top.startswith("bundle_") else top
        dest = Path(dest)
        if dest.suffix != ".ipynb":
            dest = dest / f"notebook_{job}.ipynb"
        dest.parent.mkdir(parents=True, exist_ok=True)
        sources = [CELL_UNPACK.format(name=name, top=top), CELL_INSTALL, CELL_RUN.format(job=job)]
        cells = [{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [],
                  "source": src.splitlines(keepends=True)} for src in sources]
        notebook = {"cells": cells, "metadata": {"language_info": {"name": "python"}},
                    "nbformat": 4, "nbformat_minor": 5}
        dest.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
        return dest
