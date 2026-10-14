"""Independent contract tests for ``topo_pilot.experiment.x5g1t_usage`` (worker self-hold latch).

Written from X5_G1_TRAINING_API_V4.md §1 and §7 (usage latch), protocol x5g1-train-v4 §8 and
agent-handoff USAGE_PROTOCOL.md only, without reading the implementation. Every mailbox is a
``tmp_path``; nothing sleeps. ``read_controls`` v4 and ``hold_while_needed`` are covered in
``test_x5g1t_controls_v4.py``.
"""

from __future__ import annotations

import json
import math
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


# ------------------------------------------------------------------ constants and parse_utc


def test_constants() -> None:
    assert u.THRESHOLD_PERCENT == 85
    assert u.LATCH_NAME == "usage_hold_latch.json"
    assert u.LATCH_SCHEMA == SCHEMA
    assert issubclass(u.UsageMalformed, ValueError)


@pytest.mark.parametrize("text, expected", [
    ("2026-10-14T03:15:34Z", datetime(2026, 10, 14, 3, 15, 34, tzinfo=UTC)),
    ("2026-10-14T03:15:34+00:00", datetime(2026, 10, 14, 3, 15, 34, tzinfo=UTC)),
    ("2026-10-14T06:15:34+03:00", datetime(2026, 10, 14, 3, 15, 34, tzinfo=UTC)),
    ("2026-10-14T00:15:34-03:00", datetime(2026, 10, 14, 3, 15, 34, tzinfo=UTC)),
    ("2026-10-14T03:15:34.5Z", datetime(2026, 10, 14, 3, 15, 34, 500000, tzinfo=UTC)),
    ("2026-10-14T03:15:34.123456+00:00",
     datetime(2026, 10, 14, 3, 15, 34, 123456, tzinfo=UTC)),
])
def test_parse_utc_offsets(text, expected) -> None:
    got = u.parse_utc(text)
    assert got.tzinfo is not None and got.utcoffset() == timedelta(0)
    assert got == expected


@pytest.mark.parametrize("text", ["2026-10-14T03:15:34.0014496Z",
                                  "2026-10-14T06:15:34.0014496+03:00"])
def test_parse_utc_powershell_seven_digits(text) -> None:
    got = u.parse_utc(text)
    assert got.utcoffset() == timedelta(0)
    assert got.replace(microsecond=0) == datetime(2026, 10, 14, 3, 15, 34, tzinfo=UTC)
    assert got.microsecond in (1449, 1450)  # 0.0014496 s; truncation or rounding


@pytest.mark.parametrize("bad", ["2026-10-14T03:15:34", "2026-10-14T03:15:34.0014496",
                                 "2026-10-14", "yesterday", "", "2026-13-40T99:00:00Z",
                                 None, 1760411734, 1.5, ["2026-10-14T03:15:34Z"],
                                 datetime(2026, 10, 14, tzinfo=UTC)])
def test_parse_utc_rejects(bad) -> None:
    with pytest.raises(u.UsageMalformed):
        u.parse_utc(bad)


# ------------------------------------------------------------------ blocking_limits


def test_realistic_multi_limit_only_relevant_high_one_blocks() -> None:
    got = u.blocking_limits(usage(multi()))
    assert isinstance(got, list) and all(isinstance(d, dict) for d in got)
    assert kinds_of(got) == {"weekly_all_models"}


@pytest.mark.parametrize("pct, blocks", [(85, True), (85.0, True), (100, True),
                                         (84.99, False), (0, False), (None, False)])
def test_threshold_boundary(pct, blocks) -> None:
    got = u.blocking_limits(usage([lim("session", pct)]))
    assert bool(got) is blocks


def test_custom_threshold() -> None:
    assert kinds_of(u.blocking_limits(usage(multi()), threshold=30)) == {
        "session", "weekly_all_models"}


@pytest.mark.parametrize("obs", ["OBSERVED", "UNAVAILABLE"])
def test_relevant_warning_blocks_with_null_percent(obs) -> None:
    lims = [lim("session", None, warning="Approaching usage limit"), lim("weekly", None)]
    got = u.blocking_limits(usage(lims, obs=obs, source="warning"))
    assert kinds_of(got) == {"session"}


def test_irrelevant_warning_does_not_block() -> None:
    assert u.blocking_limits(usage([lim("opus", 95, relevant=False, warning="limit")])) == []


def test_unavailable_never_blocks_by_itself() -> None:
    assert u.blocking_limits(UNAVAILABLE) == []
    # UNAVAILABLE numbers are not observations: only warnings count.
    assert u.blocking_limits(usage([lim("session", 95)], obs="UNAVAILABLE")) == []
    assert u.blocking_limits(usage([], obs="UNAVAILABLE", source="unavailable")) == []


def test_observed_empty_limits_is_not_blocking() -> None:
    assert u.blocking_limits(usage([])) == []


def _mut(**limit_overrides) -> dict:
    return usage([{**lim("session", 50), **limit_overrides}])


def _drop(key) -> dict:
    d = lim("session", 50)
    d.pop(key)
    return usage([d])


@pytest.mark.parametrize("bad", [
    None, [], "OBSERVED",
    {**usage(multi()), "observability": "observed"},
    {**usage(multi()), "observability": None},
    {k: v for k, v in usage(multi()).items() if k != "observability"},
    {k: v for k, v in usage(multi()).items() if k != "limits"},
    {**usage(multi()), "limits": None},
    {**usage(multi()), "limits": {"session": 40}},
    usage(["session"]), usage([None]), usage([[40]]),
    _mut(kind=None), _mut(kind=3), _drop("kind"),
    _mut(relevant="true"), _mut(relevant=1), _mut(relevant=None), _drop("relevant"),
    _mut(used_percent=True), _mut(used_percent=False), _mut(used_percent="86"),
    _mut(used_percent=math.nan), _mut(used_percent=math.inf), _mut(used_percent=-math.inf),
    _mut(used_percent=-0.5), _mut(used_percent=100.01), _mut(used_percent=[86]),
    _mut(warning=5), _mut(warning=True), _mut(warning=["limit"]),
])
def test_blocking_limits_malformed(bad) -> None:
    with pytest.raises(u.UsageMalformed):
        u.blocking_limits(bad)


# ------------------------------------------------------------------ make_latch


def test_make_latch_shape() -> None:
    blocking = u.blocking_limits(usage(multi()))
    got = u.make_latch(blocking, "owner report", T0)
    assert got == {"schema": SCHEMA, "set_at_utc": T0.isoformat(), "source": "owner report",
                   "blocking": [{"kind": "weekly_all_models", "used_percent": 86,
                                 "warning": None}]}
    assert u.parse_utc(got["set_at_utc"]) == T0
    json.dumps(got)  # serialisable as written to the mailbox


# ------------------------------------------------------------------ latch_clears


def test_fresh_full_clearance_clears() -> None:
    ok, reason = u.latch_clears(latch(), fresh_clear())
    assert ok is True and isinstance(reason, str)


def _not_cleared(lt, us) -> str:
    ok, reason = u.latch_clears(lt, us)
    assert ok is False
    assert isinstance(reason, str) and reason
    return reason


@pytest.mark.parametrize("at", [T0 - timedelta(minutes=1), T0])
def test_older_or_equal_evidence_is_stale(at) -> None:
    _not_cleared(latch(), usage(multi(12, 20, 99), at=at))


def test_offset_comparison_is_by_instant_not_text() -> None:
    older = {**fresh_clear(), "observed_at_utc": "2026-10-14T05:30:00.0000000+03:00"}
    _not_cleared(latch(), older)  # 02:30Z: lexically later, actually older
    newer = {**fresh_clear(), "observed_at_utc": "2026-10-14T06:30:00+03:00"}
    assert u.latch_clears(latch(), newer)[0] is True
    equal = {**fresh_clear(), "observed_at_utc": "2026-10-14T03:00:00.0000000Z"}
    _not_cleared(latch(), equal)


def test_unavailable_never_clears() -> None:
    later = {**UNAVAILABLE, "observed_at_utc": ps(T0 + timedelta(hours=9))}
    _not_cleared(latch(), later)
    _not_cleared(latch(), fresh_clear(obs="UNAVAILABLE"))


@pytest.mark.parametrize("source", ["unavailable", None, 7])
def test_bad_source_never_clears(source) -> None:
    _not_cleared(latch(), fresh_clear(source=source))


def test_missing_source_never_clears() -> None:
    us = fresh_clear()
    us.pop("source")
    try:
        ok, _ = u.latch_clears(latch(), us)
    except u.UsageMalformed:
        return
    assert ok is False


@pytest.mark.parametrize("weekly", [
    None, lim("weekly_all_models", None), lim("weekly_all_models", 20, relevant=False),
    lim("weekly_all_models", 85), lim("weekly_all_models", 20, warning="approaching"),
])
def test_every_latched_kind_must_be_present_relevant_numeric_low(weekly) -> None:
    lims = [lim("session", 12)] + ([weekly] if weekly else [])
    _not_cleared(latch(), usage(lims, at=T0 + timedelta(minutes=30)))


def test_one_of_two_latched_kinds_missing() -> None:
    lt = latch(("session", "weekly_all_models"))
    _not_cleared(lt, usage([lim("session", 3)], at=T0 + timedelta(hours=6)))
    assert u.latch_clears(lt, fresh_clear())[0] is True


def test_latched_kind_just_below_threshold_clears() -> None:
    lims = [lim("session", 10), lim("weekly_all_models", 84.99)]
    assert u.latch_clears(latch(), usage(lims, at=T0 + timedelta(seconds=1)))[0] is True


def test_other_relevant_limit_blocking_prevents_clear() -> None:
    lims = [lim("session", 91), lim("weekly_all_models", 20)]
    _not_cleared(latch(), usage(lims, at=T0 + timedelta(hours=1)))


def test_garbage_evidence_time_never_clears() -> None:
    us = {**fresh_clear(), "observed_at_utc": "2026-10-14T09:00:00"}  # naive
    try:
        ok, _ = u.latch_clears(latch(), us)
    except u.UsageMalformed:
        return
    assert ok is False


def _bad_latches() -> list:
    good = latch()
    return [
        [], {**good, "schema": "usage-hold-latch-v0"},
        {k: v for k, v in good.items() if k != "schema"},
        {**good, "set_at_utc": "2026-10-14T03:00:00"}, {**good, "set_at_utc": "soon"},
        {**good, "set_at_utc": None}, {k: v for k, v in good.items() if k != "set_at_utc"},
        {**good, "blocking": []}, {**good, "blocking": None}, {**good, "blocking": "weekly"},
        {**good, "blocking": ["weekly"]}, {**good, "blocking": [{"kind": 3}]},
        {**good, "blocking": [{"used_percent": 90}]},
    ]


@pytest.mark.parametrize("bad", _bad_latches())
def test_malformed_latch(bad) -> None:
    with pytest.raises(u.UsageMalformed):
        u.latch_clears(bad, fresh_clear())
    with pytest.raises(u.UsageMalformed):
        u.usage_decision(fresh_clear(), bad, T0 + timedelta(hours=1))


# ------------------------------------------------------------------ usage_decision

LATER = T0 + timedelta(minutes=31)


def _hold(d) -> None:
    assert isinstance(d, u.UsageDecision) and isinstance(d, tuple)
    assert d.action == "HOLD"
    assert len(d.reasons) > 0 and all(isinstance(r, str) and r for r in d.reasons)
    assert not d.clear_latch


def test_no_latch_blocking_sets_latch() -> None:
    d = u.usage_decision(usage(multi()), None, T0)
    _hold(d)
    assert d.set_latch["schema"] == SCHEMA
    assert kinds_of(d.set_latch["blocking"]) == {"weekly_all_models"}
    assert u.parse_utc(d.set_latch["set_at_utc"]) == T0


def test_no_latch_warning_sets_latch_even_unavailable() -> None:
    us = usage([lim("session", None, warning="You are close to your limit")],
               obs="UNAVAILABLE", source="warning")
    d = u.usage_decision(us, None, T0)
    _hold(d)
    assert kinds_of(d.set_latch["blocking"]) == {"session"}


@pytest.mark.parametrize("us", [None, UNAVAILABLE, usage(multi(40, 60, 99)), usage([])])
def test_no_latch_not_blocking_continues(us) -> None:
    d = u.usage_decision(us, None, T0)
    assert d.action == "CONTINUE"
    assert d.set_latch is None and not d.clear_latch


@pytest.mark.parametrize("us", [
    None, UNAVAILABLE, {**UNAVAILABLE, "observed_at_utc": ps(LATER)},
    usage(multi(12, 20, 99), at=T0 - timedelta(minutes=5)),   # older
    usage(multi(12, 20, 99), at=T0),                          # equal
    usage([lim("session", 3)], at=LATER),                     # latched kind missing
    usage([lim("session", 3), lim("weekly_all_models", None)], at=LATER),
    fresh_clear(source="unavailable"),
])
def test_latch_without_fresh_full_clearance_holds(us) -> None:
    _hold(u.usage_decision(us, latch(), LATER))


def test_fresh_full_clearance_continues_and_clears() -> None:
    d = u.usage_decision(fresh_clear(), latch(), LATER)
    assert d.action == "CONTINUE" and d.clear_latch is True
    assert d.set_latch is None


def test_cleared_kind_but_new_relevant_limit_blocks() -> None:
    us = usage([lim("session", 92), lim("weekly_all_models", 20)], at=LATER)
    d = u.usage_decision(us, latch(), LATER)
    assert d.action == "HOLD" and d.reasons
    # The new blocking kind must be latched so its later disappearance cannot clear.
    assert d.set_latch is not None and "session" in kinds_of(d.set_latch["blocking"])


@pytest.mark.parametrize("now", [datetime(2099, 1, 1, tzinfo=UTC),
                                 T0 + timedelta(days=30)])
def test_elapsed_time_and_reset_times_never_clear(now) -> None:
    passed = lim("weekly_all_models", 86, reset="2026-10-14T05:00:00+00:00")
    _hold(u.usage_decision(None, latch(), now))
    _hold(u.usage_decision(usage([passed]), latch(), now))
    _hold(u.usage_decision(UNAVAILABLE, latch(), now))


@pytest.mark.parametrize("bad", [{**usage(multi()), "observability": "MAYBE"},
                                 usage([lim("session", "86%")])])
def test_decision_with_malformed_usage_raises(bad) -> None:
    with pytest.raises(u.UsageMalformed):
        u.usage_decision(bad, None, T0)


def test_none_latch_is_absence_sentinel_in_decision_but_malformed_for_latch_clears() -> None:
    # API §1: usage_decision(latch=None) = "no latch file"; latch_clears(None, ...) is malformed.
    assert u.usage_decision(None, None, T0).action == "CONTINUE"
    with pytest.raises(u.UsageMalformed):
        u.latch_clears(None, fresh_clear())


def test_decision_naive_or_nonstring_evidence_time_never_releases() -> None:
    for bad in ("2026-10-14T09:00:00", 12345, None):
        us = {**fresh_clear(), "observed_at_utc": bad}
        try:
            d = u.usage_decision(us, latch(), LATER)
        except u.UsageMalformed:
            continue
        assert d.action == "HOLD"


def test_session_and_weekly_both_latched_then_partial_clear_holds() -> None:
    us = usage([lim("session", 90), lim("weekly_all_models", 88)])
    d = u.usage_decision(us, None, T0)
    assert d.action == "HOLD"
    assert kinds_of(d.set_latch["blocking"]) == {"session", "weekly_all_models"}
    lt = d.set_latch
    part = usage([lim("session", 10), lim("weekly_all_models", 88)], at=LATER)
    assert u.usage_decision(part, lt, LATER).action == "HOLD"
    full = usage([lim("session", 10), lim("weekly_all_models", 30)], at=LATER)
    dd = u.usage_decision(full, lt, LATER)
    assert dd.action == "CONTINUE" and dd.clear_latch is True


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
