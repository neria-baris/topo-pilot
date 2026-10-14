"""Independent contract tests for ``topo_pilot.experiment.x5g1t_usage`` (worker self-hold latch).

Written from X5_G1_TRAINING_API_V4.md §1 and §7 (usage latch), protocol x5g1-train-v4 §8 and
agent-handoff USAGE_PROTOCOL.md only, without reading the implementation. Every mailbox is a
``tmp_path``; nothing sleeps. ``read_controls`` v4 and ``hold_while_needed`` are covered in
``test_x5g1t_controls_v4.py``.
Split mechanically from test_x5g1t_usage.py (job 0011); tests unchanged.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from topo_pilot.experiment import x5g1t_usage as u

pytestmark = pytest.mark.experiment

UTC = timezone.utc
T0 = datetime(2026, 10, 14, 3, 0, tzinfo=UTC)  # the latch time used throughout
SCHEMA = "usage-hold-latch-v1"


def ps(t: datetime) -> str:
    """PowerShell ``"o"`` format: 7 fractional digits and a Z suffix."""
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f") + "0Z"


def lim(kind, pct, *, relevant=True, warning=None, reset=None) -> dict:
    return {"kind": kind, "used_percent": pct, "reset_at_iso": reset, "reset_text": None,
            "warning": warning, "relevant": relevant}


def multi(session=40, weekly=86, model=90) -> list[dict]:
    """Realistic multi-limit snapshot; the per-model allowance is irrelevant."""
    return [lim("session", session), lim("weekly_all_models", weekly),
            lim("weekly_opus", model, relevant=False)]


def usage(limits, *, at=T0 - timedelta(minutes=1), obs="OBSERVED", source="owner report"):
    return {"schema": "usage-watch-v1", "author": "claude", "observed_at_utc": ps(at),
            "observability": obs, "active_job_id": "0010", "source": source,
            "limits": limits, "threshold_percent": 85, "mode": "WORKING",
            "next_expected_resume_at_utc": None}


UNAVAILABLE = usage([lim("session", None), lim("weekly_all_models", None)],
                    obs="UNAVAILABLE", source="unavailable")


def latch(kinds=("weekly_all_models",), at=T0) -> dict:
    return {"schema": SCHEMA, "set_at_utc": at.isoformat(), "source": "owner report",
            "blocking": [{"kind": k, "used_percent": 86.0, "warning": None} for k in kinds]}


def fresh_clear(minutes=30, **kw) -> dict:
    return usage(multi(session=12, weekly=20, model=99), at=T0 + timedelta(minutes=minutes), **kw)


def kinds_of(items) -> set[str]:
    return {d["kind"] for d in items}


# ------------------------------------------------------------------ file level: apply_usage

from topo_pilot.experiment import x5g1t_runtime as rt  # noqa: E402

NOW = T0 + timedelta(minutes=31)


def put(box: Path, name: str, content) -> None:
    text = content if isinstance(content, str) else json.dumps(content)
    (box / name).write_text(text, encoding="utf-8")


@pytest.fixture
def box(tmp_path: Path) -> Path:
    b = tmp_path / "mailbox"
    b.mkdir()
    put(b, "request.json", {"command": "RUN_NEXT"})
    return b


def cleared_files(b: Path) -> list[Path]:
    return sorted(b.glob("usage_hold_latch.cleared-*.json"))


def test_apply_usage_missing_files_no_hold(tmp_path: Path) -> None:
    action, reasons = u.apply_usage(tmp_path, NOW)
    assert action == "CONTINUE" and isinstance(reasons, tuple)
    assert not (tmp_path / u.LATCH_NAME).exists()


def test_apply_usage_blocking_writes_latch_and_reads_utf8_sig(tmp_path: Path) -> None:
    (tmp_path / "claude_usage.json").write_bytes(
        b"\xef\xbb\xbf" + json.dumps(usage(multi())).encode())
    action, reasons = u.apply_usage(tmp_path, NOW)
    assert action == "HOLD" and reasons
    written = json.loads((tmp_path / u.LATCH_NAME).read_text(encoding="utf-8-sig"))
    assert written["schema"] == SCHEMA and kinds_of(written["blocking"]) == {"weekly_all_models"}


def test_apply_usage_hold_persists_without_usage_file(tmp_path: Path) -> None:
    put(tmp_path, u.LATCH_NAME, latch())
    assert u.apply_usage(tmp_path, NOW)[0] == "HOLD"
    assert (tmp_path / u.LATCH_NAME).exists()


def test_apply_usage_clears_and_archives(tmp_path: Path) -> None:
    put(tmp_path, u.LATCH_NAME, latch())
    put(tmp_path, "claude_usage.json", fresh_clear())
    action, _ = u.apply_usage(tmp_path, NOW)
    assert action == "CONTINUE"
    assert not (tmp_path / u.LATCH_NAME).exists()
    arch = cleared_files(tmp_path)
    assert len(arch) == 1
    assert "observed_at_utc" in arch[0].read_text(encoding="utf-8")  # clearing evidence kept


@pytest.mark.parametrize("content", ["null", "[]", '"x"', "42", "{bad", ""])
def test_apply_usage_existing_malformed_usage_file_raises(tmp_path: Path, content) -> None:
    put(tmp_path, "claude_usage.json", content)
    with pytest.raises(u.UsageMalformed):
        u.apply_usage(tmp_path, NOW)


@pytest.mark.parametrize("content", ["null", "[]", '"x"', "42", "{bad", ""])
def test_apply_usage_existing_malformed_latch_file_raises(tmp_path: Path, content) -> None:
    put(tmp_path, u.LATCH_NAME, content)
    put(tmp_path, "claude_usage.json", fresh_clear())
    with pytest.raises(u.UsageMalformed):
        u.apply_usage(tmp_path, NOW)


@pytest.mark.parametrize("content", ["null", "[]", '"x"', "{bad"])
@pytest.mark.parametrize("name", ["claude_usage.json", u.LATCH_NAME])
def test_read_controls_existing_malformed_file_is_stop(box: Path, name, content) -> None:
    put(box, name, content)
    state = rt.read_controls(box, NOW)
    assert state.action == "STOP"
    assert any(r.startswith("usage_malformed") for r in state.reasons)


def test_read_controls_missing_usage_files_continue(box: Path) -> None:
    assert rt.read_controls(box, NOW).action == "CONTINUE"


# ------------------------------------------------------------------ file level: read_controls


def test_read_controls_multi_limit_hold_and_latch(box: Path) -> None:
    put(box, "claude_usage.json", usage(multi()))
    state = rt.read_controls(box, NOW)
    assert state.action == "HOLD" and state.reasons
    assert (box / u.LATCH_NAME).exists()


def test_read_controls_warning_hold(box: Path) -> None:
    put(box, "claude_usage.json", usage([lim("session", None, warning="close to limit")],
                                        obs="UNAVAILABLE", source="warning"))
    assert rt.read_controls(box, NOW).action == "HOLD"


def test_read_controls_unavailable_alone_continues(box: Path) -> None:
    put(box, "claude_usage.json", UNAVAILABLE)
    assert rt.read_controls(box, NOW).action == "CONTINUE"
    assert not (box / u.LATCH_NAME).exists()


def test_read_controls_unknown_values_stop(box: Path) -> None:
    put(box, "claude_usage.json", usage([lim("session", "86%")]))
    assert rt.read_controls(box, NOW).action == "STOP"
    put(box, "claude_usage.json", {**usage(multi()), "observability": "MAYBE"})
    assert rt.read_controls(box, NOW).action == "STOP"


def test_read_controls_stale_evidence_holds(box: Path) -> None:
    put(box, u.LATCH_NAME, latch())
    put(box, "claude_usage.json", usage(multi(12, 20, 99), at=T0))  # observed_at == set_at
    assert rt.read_controls(box, NOW).action == "HOLD"
    put(box, "claude_usage.json", usage(multi(12, 20, 99), at=T0 - timedelta(hours=1)))
    assert rt.read_controls(box, NOW).action == "HOLD"


def test_read_controls_naive_or_nonstring_time_not_release(box: Path) -> None:
    put(box, u.LATCH_NAME, latch())
    for bad in ("2026-10-14T09:00:00", 12345, None):
        put(box, "claude_usage.json", {**fresh_clear(), "observed_at_utc": bad})
        assert rt.read_controls(box, NOW).action in ("HOLD", "STOP")


def test_read_controls_mode_edited_to_working_does_not_release(box: Path) -> None:
    put(box, u.LATCH_NAME, latch())
    put(box, "runtime_state.json", {"mode": "WORKING"})
    assert rt.read_controls(box, NOW).action == "HOLD"
    put(box, "claude_usage.json", {**usage(multi(40, 86, 90)), "mode": "WORKING"})
    assert rt.read_controls(box, NOW).action == "HOLD"


def test_read_controls_fresh_clearance_plus_continue_releases_and_archives(box: Path) -> None:
    put(box, u.LATCH_NAME, latch())
    put(box, "claude_usage.json", fresh_clear())
    put(box, "worker_control.json", {"command": "CONTINUE"})
    put(box, "runtime_state.json", {"mode": "USAGE_READY"})
    assert rt.read_controls(box, NOW).action == "CONTINUE"
    assert not (box / u.LATCH_NAME).exists()
    assert len(cleared_files(box)) == 1


def test_read_controls_coordinator_wait_holds_despite_clearance(box: Path) -> None:
    put(box, u.LATCH_NAME, latch())
    put(box, "claude_usage.json", fresh_clear())
    put(box, "worker_control.json", {"command": "WAIT_USAGE_RESET"})
    assert rt.read_controls(box, NOW).action == "HOLD"


def test_blocking_usage_holds_despite_worker_continue(box: Path) -> None:
    put(box, "claude_usage.json", usage(multi()))
    put(box, "worker_control.json", {"command": "CONTINUE"})
    assert rt.read_controls(box, NOW).action == "HOLD"


@pytest.mark.parametrize("stop_src", ["file", "request", "worker"])
def test_stop_beats_everything(box: Path, stop_src: str) -> None:
    put(box, u.LATCH_NAME, latch())
    put(box, "claude_usage.json", usage(multi()))
    put(box, "runtime_state.json", {"mode": "WAIT_USAGE_RESET"})
    if stop_src == "file":
        (box / "STOP").write_text("", encoding="utf-8")
    elif stop_src == "request":
        put(box, "request.json", {"command": "STOP"})
    else:
        put(box, "worker_control.json", {"command": "STOP"})
    assert rt.read_controls(box, NOW).action == "STOP"


@pytest.mark.parametrize("mode", ["RUNTIME_BLOCKED", "NEEDS_USAGE_INFO", "WAIT_USAGE_RESET"])
def test_hold_modes_hold(box: Path, mode: str) -> None:
    put(box, "runtime_state.json", {"mode": mode})
    put(box, "claude_usage.json", fresh_clear())
    assert rt.read_controls(box, NOW).action == "HOLD"


@pytest.mark.parametrize("state", [{"mode": "BOGUS"}, {"mode": 3}, {"mode": None}, {},
                                   {"state": "WORKING"}])
def test_unknown_or_missing_mode_is_stop(box: Path, state) -> None:
    put(box, "runtime_state.json", state)
    assert rt.read_controls(box, NOW).action == "STOP"
