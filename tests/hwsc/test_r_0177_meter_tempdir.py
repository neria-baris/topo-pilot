"""Regression D-0177-1 (coordinator 08ad4eaf, job 0177).

The metered child's TEMP/TMP/TMPDIR point at <TEMP_ROOT>/tmp-<job>; the folder was never
created, so tempfile.gettempdir() in the child fell back to C: (J-C1 tempdir check).
child_env_c must create it, and a child process must then use it.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsc") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsc"))

import hwsc_meter_bind as cm  # noqa: E402
import k4b_meter_bind  # noqa: E402


def test_child_env_creates_temp_and_child_uses_it(tmp_path, monkeypatch):
    monkeypatch.setattr(k4b_meter_bind, "TEMP_ROOT", str(tmp_path))
    env = cm.child_env_c("9999")
    tmp = Path(env["TEMP"])
    assert tmp.is_dir()
    assert env["TMP"] == env["TMPDIR"] == env["TEMP"]
    out = subprocess.run(
        [sys.executable, "-s", "-c", "import tempfile; print(tempfile.gettempdir())"],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert Path(out).resolve() == tmp.resolve()
