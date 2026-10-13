"""S6 H4 rule (D-034): per-run classification and the verdict over the cylinder runs."""
import pytest

from topo_pilot.experiment.s6 import first_step, h4_class, h4_verdict

pytestmark = pytest.mark.experiment

STEPS = [0, 50, 100, 200, 400]


def test_first_step():
    assert first_step(STEPS, [False, False, True, True, False]) == 100
    assert first_step(STEPS, [False] * 5) is None


@pytest.mark.parametrize("t_h, t_s, cls", [
    (100, 200, "consistent"),
    (100, 100, "consistent"),  # same checkpoint: grid resolution
    (200, 100, "violated"),
    (100, None, "no_rise"),
    (None, 100, "no_history_use"),
])
def test_h4_class(t_h, t_s, cls):
    assert h4_class(t_h, t_s) == cls


def test_h4_supported_needs_all_three_consistent():
    assert h4_verdict(["consistent"] * 3, [True] * 3, 3) == ("SUPPORTED", "")
    status, reason = h4_verdict(["consistent", "consistent"], [True] * 2, 3)
    assert status == "INCONCLUSIVE" and "2 < 3" in reason


def test_h4_rejected_by_any_violation_with_gates_passed():
    assert h4_verdict(["consistent", "violated", "consistent"], [True] * 3, 3)[0] == "REJECTED"


def test_h4_failed_gate_or_no_rise_is_inconclusive():
    assert h4_verdict(["violated"] * 3, [True, False, True], 3)[0] == "INCONCLUSIVE"
    status, reason = h4_verdict(["consistent", "no_rise", "consistent"], [True] * 3, 3)
    assert status == "INCONCLUSIVE" and "no_rise" in reason
