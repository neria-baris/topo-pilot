"""Dummy child for bounded synthetic meter checks (stdlib only; touches only a synthetic dir).

Usage: python -I synthetic_child.py MODE SYNTHETIC_DIR
MODE: finish | stop | invalid | hold | descendant | grandchild | sleep
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path


def set_control(root: Path, command: str) -> None:
    path = root / "worker_control.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["command"] = command
    path.write_text(json.dumps(data), encoding="utf-8")


def main() -> int:
    mode, root = sys.argv[1], Path(sys.argv[2])
    if mode == "finish":
        time.sleep(1.0)
    elif mode == "stop":
        time.sleep(1.0)
        (root / "STOP").write_text("synthetic", encoding="utf-8")
        time.sleep(60)
    elif mode == "invalid":
        time.sleep(1.0)
        (root / "request.json").write_text("{not json", encoding="utf-8")
        time.sleep(60)
    elif mode == "hold":
        time.sleep(0.5)
        set_control(root, "WAIT_USAGE_RESET")
        time.sleep(3.0)
        set_control(root, "CONTINUE")
        time.sleep(1.0)
    elif mode == "descendant":
        subprocess.Popen([sys.executable, "-I", __file__, "grandchild", str(root)])
    elif mode == "grandchild":
        end = time.monotonic() + 3.0
        while time.monotonic() < end:
            sum(i * i for i in range(1000))
        (root / "grandchild_done.txt").write_text("done", encoding="utf-8")
    elif mode == "sleep":
        time.sleep(60)
    else:
        return 64
    return 0


if __name__ == "__main__":
    sys.exit(main())
