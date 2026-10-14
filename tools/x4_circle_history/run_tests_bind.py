"""Run tests/circle_history (plus the reused job-0014 oracle regressions) under the meter.

Writes OUT/tests/run_NN.json (immutable) with the pytest outcome and the job-0016 frozen file
hashes. On success, ACCEPTED.json points at that run (replaced atomically). Venv interpreter;
PYTHONPATH = this worktree's src.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))


def main() -> int:
    import freeze_bind
    import pytest

    out = freeze_bind.OUT / "tests"
    out.mkdir(parents=True, exist_ok=True)
    number = 1 + max((int(p.stem.split("_")[1]) for p in out.glob("run_*.json")), default=0)
    junit = out / f"run_{number:02d}.xml"
    os.chdir(REPO)
    files = freeze_bind.frozen_files()
    start = time.process_time()
    code = pytest.main(
        [
            "tests/circle_history",
            "tests/oracle_profile",
            "-q",
            "-p",
            "no:cacheprovider",
            f"--junitxml={junit}",
            "-W",
            "ignore::pytest.PytestUnknownMarkWarning",
        ]
    )
    record = {
        "run": number,
        "exit_code": int(code),
        "passed": int(code) == 0,
        "pytest": pytest.__version__,
        "files": files,
        "junit": junit.name,
        "in_process_cpu_s": time.process_time() - start,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    path = out / f"run_{number:02d}.json"
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(record, indent=1, sort_keys=True) + "\n")
    if record["passed"]:
        tmp = out / "ACCEPTED.json.tmp"
        tmp.write_text(
            json.dumps(dict(record, record=path.name), indent=1, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(tmp, out / "ACCEPTED.json")
    return int(code)


if __name__ == "__main__":
    sys.exit(main())
