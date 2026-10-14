"""Run tests/oracle_profile under the meter and record the result (venv interpreter).

Writes OUT/tests/run_NN.json (immutable) with pytest outcome and the hashes of every frozen
implementation/test file; on success, ACCEPTED.json points at that run (replaced atomically).
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = Path(r"X:\Downloads\projects\topo-pilot\x4-oracle-profile-store-0014") / "tests"


def main() -> int:
    import freeze
    import pytest

    OUT.mkdir(exist_ok=True)
    number = 1 + max((int(p.stem.split("_")[1]) for p in OUT.glob("run_*.json")), default=0)
    junit = OUT / f"run_{number:02d}.xml"
    os.chdir(REPO)
    files = freeze.frozen_files()
    start = time.process_time()
    code = pytest.main(
        [
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
    path = OUT / f"run_{number:02d}.json"
    with path.open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(record, indent=1, sort_keys=True) + "\n")
    if record["passed"]:
        tmp = OUT / "ACCEPTED.json.tmp"
        tmp.write_text(
            json.dumps(dict(record, record=path.name), indent=1, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.replace(tmp, OUT / "ACCEPTED.json")
    return int(code)


if __name__ == "__main__":
    sys.exit(main())
