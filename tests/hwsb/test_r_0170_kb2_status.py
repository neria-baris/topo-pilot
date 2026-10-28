"""Regression D-0170-1 (coordinator 08ad4eaf, job 0170).

kb2_kb3 must give KB2 the gate status PASS for the bitwise reading (API §12), so that
run_kb continues to KB3. Job 0170 recorded KB2 = "BITWISE" (the reading name) and stopped
with KB3-KB6 NOT_RUN although E4 was reproduced bitwise. Sampling and training are stubbed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import hwsb_known as hk  # noqa: E402
import hwsb_train as ht  # noqa: E402

K2 = hk.KC["KB2"]
REF_CK = {int(s): v["payload_sha256"] for s, v in K2["checkpoints"].items()}
REF_CE = {int(s): float(v) for s, v in K2["dev_ce"].items()}


class _Obs:
    def __init__(self, split):
        self.split = split


def _stub(monkeypatch, checksums, dev_ce):
    monkeypatch.setattr(hk, "_e4_obs", lambda proc, split, n, rng, rep: _Obs(split))
    monkeypatch.setattr(hk, "_ck", lambda o: K2[f"ObservationSet_{o.split}"]["payload_sha256"])

    def train_known(*args, stop_after, threads):
        return {
            "checksums": dict(checksums),
            "dev_ce": dict(dev_ce),
            "checkpoints": {100: None},
            "threads": {"requested": threads},
            "stopped_at": stop_after,
        }

    monkeypatch.setattr(ht, "train_known", train_known)


def test_bitwise_reading_is_gate_pass(monkeypatch):
    _stub(monkeypatch, REF_CK, REF_CE)
    r = hk.kb2_kb3(None)
    assert r["reading"] == "BITWISE"
    assert r["KB2"]["status"] == "PASS"
    assert r["KB2"]["deviation_flags"] == []
    assert r["KB3"]["status"] == "PASS"


def test_secondary_reading_keeps_its_status(monkeypatch):
    ck = dict(REF_CK)
    ck[100] = "0" * 64
    _stub(monkeypatch, ck, {s: v + 1e-4 for s, v in REF_CE.items()})
    r = hk.kb2_kb3(None)
    assert r["reading"] == "PASS_WITH_NUMERIC_DRIFT"
    assert r["KB2"]["status"] == "PASS_WITH_NUMERIC_DRIFT"
    assert r["KB2"]["deviation_flags"] == ["KB2_SECONDARY_READING"]


@pytest.mark.parametrize("delta", [1e-2])
def test_no_reading_fails_known_case(monkeypatch, delta):
    _stub(monkeypatch, {s: "0" * 64 for s in REF_CK}, {s: v + delta for s, v in REF_CE.items()})
    r = hk.kb2_kb3(None)
    assert r["reading"] is None
    assert r["KB2"]["status"] == hk.KNOWN
