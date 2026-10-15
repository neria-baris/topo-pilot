"""Independent tests, author A (job 0026): the gate table, the computation-order rule and the
stage machinery (TEST_PLAN A-6, first three bullets; protocol section 2.2, section 16 and
section 18 field 2; API.md section 2 GATE_ORDER, LogitPolicy, PREREQUISITE, begin_stage).

Stores are pytest tmp_path directories; records are written with the unchanged K4
stage_records helpers. The expected tables are transcribed from protocol section 16.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tests/oracle_profile", "tools/x4_oracle_profile", "tools/x4_circle_history",
             "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))
if str(REPO / "src") not in sys.path:
    sys.path.append(str(REPO / "src"))

import c1_records  # noqa: E402
import stage_records  # noqa: E402

MODELS = (1729, 2718, 3141)
ORDER = [
    ("0", "pre-data", "G0"), ("1", "S3", "H1"), ("2", "S3", "H2"), ("3", "S3", "H3"),
    ("4", "S3", "H4"), ("4a", "S3", "N0"), ("5", "S3", "H5"), ("6", "S4", "M0"),
    ("7", "S4", "C0-cal"), ("8", "S4", "F1"), ("9", "S4", "M1"), ("10", "S4", "M2-cal"),
    ("11", "S4", "M3-cal"), ("12", "S5", "C0-val"), ("13", "S5", "M4"), ("14", "S5", "M2-val"),
    ("15", "S5", "M3-val"), ("16", "S5", "V1"), ("17", "S5", "V2"), ("18", "S5", "V3"),
    ("19", "S5", "P1"), (None, "S6", "ACCEPT"), ("20", "S7", "T-PRE"), ("21", "S7", "NUM"),
    ("22", "S7", "ENDPOINT"),
]
GATES = [g for _, _, g in ORDER]
STAGE_GATES = {
    "oracle": ["G0", "H1", "H2", "H3", "H4", "N0", "H5"],
    "calibration": ["M0", "C0-cal", "F1", "M1", "M2-cal", "M3-cal"],
    "validation": ["C0-val", "M4", "M2-val", "M3-val", "V1", "V2", "V3", "P1"],
    "fresh": ["T-PRE", "NUM", "ENDPOINT"],
}
ALLOWED = {  # API.md section 2 LogitPolicy table (protocol section 2.2)
    "identity_check": {"M0", "P1", "T-PRE"},
    "donor": {"V3", "P1", "T-PRE", "NUM", "ENDPOINT"},
    "endpoint": {"P1", "NUM", "ENDPOINT"},
}


@pytest.fixture(autouse=True)
def restore_prerequisite(monkeypatch):
    """begin_stage rebinds the shared K4 global; restore it for the other suites."""
    monkeypatch.setattr(stage_records, "PREREQUISITE", dict(stage_records.PREREQUISITE))


def test_gate_order_is_the_section_16_order():
    got = list(c1_records.GATE_ORDER)
    assert [g for _, _, g in got] == GATES
    assert [s for _, s, _ in got] == [s for _, s, _ in ORDER]
    for (row, _, gate), (want, _, _) in zip(got, ORDER):
        if want is not None:
            assert str(row) == want, gate


def test_stage_gates_and_required_pass_sets():
    assert {k: list(v) for k, v in c1_records.STAGE_GATES.items()} == STAGE_GATES
    want = {k: STAGE_GATES[k] for k in ("oracle", "calibration", "validation")}
    assert {k: list(v) for k, v in c1_records.REQUIRED_PASS.items()} == want


def test_prerequisite_dict_and_binding():
    expected = {"oracle": None, "calibration": "oracle", "validation": "calibration",
                "fresh": "validation"}
    assert c1_records.PREREQUISITE == expected
    module = c1_records.bind_stage_records()
    assert module is stage_records and stage_records.PREREQUISITE == expected


def policy_at(gate):
    """A fresh LogitPolicy advanced through every earlier gate (each begun, then passed)."""
    policy = c1_records.LogitPolicy()
    for name in GATES:
        policy.begin(name)
        if name == gate:
            return policy
        policy.passed(name)
    raise AssertionError(gate)


@pytest.mark.parametrize("gate", GATES)
@pytest.mark.parametrize("kind", sorted(ALLOWED))
def test_logit_policy_table(gate, kind):
    policy = policy_at(gate)
    if gate in ALLOWED[kind]:
        policy.require(kind)
    else:
        with pytest.raises(c1_records.C1GateFailure) as caught:
            policy.require(kind)
        assert str(caught.value.status).startswith("FAIL_TECHNICAL")


def test_no_logit_kind_at_calibration_gates_except_the_m0_identity_check():
    for gate in STAGE_GATES["calibration"]:
        for kind in ALLOWED:
            policy = policy_at(gate)
            if gate == "M0" and kind == "identity_check":
                policy.require(kind)
                continue
            with pytest.raises(c1_records.C1GateFailure):
                policy.require(kind)


def test_gates_begin_only_in_order():
    policy = c1_records.LogitPolicy()
    with pytest.raises(c1_records.C1GateFailure):
        policy.begin("H1")  # G0 has not passed
    policy = c1_records.LogitPolicy()
    policy.begin("G0")
    policy.passed("G0")
    with pytest.raises(c1_records.C1GateFailure):
        policy.begin("H2")  # skips H1


def test_endpoint_logits_never_follow_a_failed_t_pre():
    """Row 20 not passed: no fresh primary/control logits, and NUM cannot begin."""
    policy = policy_at("T-PRE")
    policy.require("donor")  # A_full / Z_full inside T-PRE for V3
    policy.require("identity_check")
    with pytest.raises(c1_records.C1GateFailure):
        policy.require("endpoint")
    with pytest.raises(c1_records.C1GateFailure):
        policy.begin("NUM")
    with pytest.raises(c1_records.C1GateFailure):
        policy.require("endpoint")


def test_endpoint_logits_after_t_pre_passes():
    policy = policy_at("T-PRE")
    policy.passed("T-PRE")
    policy.begin("NUM")
    policy.require("endpoint")


def pass_gates(out, names):
    for name in names:
        stage_records.record_gate(out, name, "PASS")


def oracle_done(out, omit=()):
    c1_records.begin_stage(out, "oracle", MODELS)
    pass_gates(out, [g for g in STAGE_GATES["oracle"] if g not in omit])
    stage_records.write_new(Path(out) / "EVIDENCE.json", {"stage": "oracle"})
    stage_records.complete(out, "oracle", ["EVIDENCE.json"])


def last_stage_event(out):
    return stage_records.stages_so_far(out)[-1]


def test_begin_stage_accepts_a_complete_prerequisite(tmp_path):
    oracle_done(tmp_path)
    c1_records.begin_stage(tmp_path, "calibration", MODELS)
    event = last_stage_event(tmp_path)
    assert (event["stage"], event["event"]) == ("calibration", "STARTED")
    assert stage_records.PREREQUISITE["calibration"] == "oracle"


@pytest.mark.parametrize("missing", ["G0", "N0", "H5"])
def test_begin_stage_refuses_a_missing_pass(tmp_path, missing):
    oracle_done(tmp_path, omit=(missing,))
    with pytest.raises(stage_records.StageRefused):
        c1_records.begin_stage(tmp_path, "calibration", MODELS)
    assert last_stage_event(tmp_path)["event"] == "REFUSED"


def test_check_pass_set_names_the_prerequisite_gates(tmp_path):
    oracle_done(tmp_path, omit=("H3",))
    with pytest.raises(stage_records.StageRefused):
        c1_records.check_pass_set(tmp_path, "calibration")
    pass_gates(tmp_path, ["H3"])
    c1_records.check_pass_set(tmp_path, "calibration")


def test_begin_stage_refuses_after_a_recorded_non_pass(tmp_path):
    oracle_done(tmp_path)
    stage_records.record_gate(tmp_path, "H5", "INCONCLUSIVE", reason="HEADROOM")
    with pytest.raises(stage_records.StageRefused):
        c1_records.begin_stage(tmp_path, "calibration", MODELS)


def test_begin_stage_refuses_a_retry(tmp_path):
    oracle_done(tmp_path)
    c1_records.begin_stage(tmp_path, "calibration", MODELS)
    with pytest.raises(stage_records.StageRefused):
        c1_records.begin_stage(tmp_path, "calibration", MODELS)
    with pytest.raises(stage_records.StageRefused):
        c1_records.begin_stage(tmp_path, "oracle", MODELS)


def test_begin_stage_refuses_changed_evidence(tmp_path):
    oracle_done(tmp_path)
    (tmp_path / "EVIDENCE.json").write_text('{"stage": "tampered"}\n', encoding="utf-8")
    with pytest.raises(stage_records.StageRefused):
        c1_records.begin_stage(tmp_path, "calibration", MODELS)
    assert last_stage_event(tmp_path)["integrity"] is True


def test_begin_stage_refuses_an_uncompleted_prerequisite(tmp_path):
    c1_records.begin_stage(tmp_path, "oracle", MODELS)
    pass_gates(tmp_path, STAGE_GATES["oracle"])
    with pytest.raises(stage_records.StageRefused):
        c1_records.begin_stage(tmp_path, "calibration", MODELS)


def test_validation_needs_the_calibration_pass_set(tmp_path):
    oracle_done(tmp_path)
    c1_records.begin_stage(tmp_path, "calibration", MODELS)
    pass_gates(tmp_path, [g for g in STAGE_GATES["calibration"] if g != "M3-cal"])
    stage_records.write_new(tmp_path / "CAL.json", {"stage": "calibration"})
    stage_records.complete(tmp_path, "calibration", ["CAL.json"])
    with pytest.raises(stage_records.StageRefused):
        c1_records.begin_stage(tmp_path, "validation", MODELS)
