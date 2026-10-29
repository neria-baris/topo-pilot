"""Coordinator-written regression test for defect D-0192-1 (API.md §28): the meter's output cap
applies to the whole out directory (for store jobs, all of hwsc-store with its three registries),
so it is read from CONTRACT resources.output_cap_bytes (16 GiB), not fixed at 4 GiB."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsc"))

import hwsc_config as cc  # noqa: E402
import hwsc_meter_bind as cm  # noqa: E402
import k4b_meter_bind  # noqa: E402
import meter  # noqa: E402
import winjob  # noqa: E402


def test_output_cap_comes_from_the_contract(tmp_path, monkeypatch):
    for mod in (meter, winjob, k4b_meter_bind):  # restore every bound global after the test
        for name in [n for n in vars(mod) if n.isupper()]:
            monkeypatch.setattr(mod, name, getattr(mod, name))
    cap = cc.CONTRACT["resources"]["output_cap_bytes"]
    assert cap == 16 * 1024**3
    cm.bind("0192r", "ab" * 32, tmp_path / "out", "sess-r", "E2", tmp_path / "tr")
    assert meter.OUTPUT_CAP == cap
    assert meter.OUTPUT_CAP > 4.3e9  # the REG2 kill of job 0192 happened at 4,296,569,273 bytes
