"""Author B (job 0161), TEST_PLAN section 3 `test_b_hold.py`: the hold rule (section 8.2, RC-14,
X-2; DRB14): `hold_check` boundaries and triggers, `HoldRule` files and decisions with a planted
CPU function and a fake sleep, and tiny trainings held at step 10. tools/hwsb/*.py unread."""

from __future__ import annotations

import dataclasses
import json
import sys
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import hwsb_config as hc  # noqa: E402
import hwsb_data as hd  # noqa: E402
import hwsb_dry as hdry  # noqa: E402
import hwsb_train as ht  # noqa: E402
from topo_pilot.contracts import ArtifactStore, Checkpoint, MemoryBackend  # noqa: E402
from topo_pilot.learner import ModelConfig, TrainConfig  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "hwsb" / "CONTRACT.json").read_text(encoding="utf-8"))
MASTER = 629902
REFUSE = "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"


# ------------------------------------------------------------------ hold_check
def test_contract_hold_numbers():
    cpu = CONTRACT["cpu"]
    assert cpu["per_model_hold_s"] == 7275 and cpu["hold_from_step"] == 1000


def test_no_projection_before_step_1000():
    r = ht.hold_check(999, 7000.0)
    assert r["projected_s"] is None and r["hold"] is False and r["trigger"] is None
    assert (r["step"], r["cpu_s"]) == (999, 7000.0)


def test_projection_at_step_1000_is_cpu_times_five():
    r = ht.hold_check(1000, 1000.0)
    assert r["projected_s"] == pytest.approx(5000.0) and r["hold"] is False
    r = ht.hold_check(2500, 2000.0)
    assert r["projected_s"] == pytest.approx(4000.0)


def test_exactly_7275_does_not_hold_and_just_above_holds():
    assert ht.hold_check(1000, 1455.0)["hold"] is False  # 1455 * 5000 / 1000 == 7275
    assert ht.hold_check(1000, 1455.0)["projected_s"] == 7275.0
    just = ht.hold_check(1000, 1455.0001)
    assert just["hold"] is True and just["trigger"] == "PROJECTED"
    assert ht.hold_check(500, 7275.0)["hold"] is False  # spent, strict
    spent = ht.hold_check(500, 7275.5)
    assert spent["hold"] is True and spent["trigger"] == "SPENT" and spent["projected_s"] is None


def test_both_trigger():
    r = ht.hold_check(1000, 7300.0)
    assert r["hold"] is True and r["trigger"] == "BOTH"


def test_custom_cap_steps_and_from_step():
    assert ht.hold_check(10, 100.0, steps=20, cap_s=150.0, from_step=10)["hold"] is True
    assert ht.hold_check(10, 100.0, steps=20, cap_s=200.0, from_step=10)["hold"] is False
    assert ht.hold_check(5, 100.0, steps=20, cap_s=150.0, from_step=10)["hold"] is False


# ------------------------------------------------------------------ HoldRule
class FakeSleep:
    """Counts calls; writes the decision file on the n-th call."""

    def __init__(self, out, step, decision, n=3, cpu_calls=None, cpu_log=None):
        self.out, self.step, self.decision, self.n = Path(out), step, decision, n
        self.calls, self.hold_seen, self.cpu_calls, self.cpu_log = 0, [], cpu_calls, cpu_log

    def __call__(self, seconds):
        self.calls += 1
        self.hold_seen.append((self.out / f"HOLD_{self.step}.json").is_file())
        if self.cpu_calls is not None:
            self.cpu_log.append(len(self.cpu_calls))
        if self.calls == self.n:
            body = {"decision": self.decision, "by": "test-owner", "utc": "2026-10-27T00:00:00Z"}
            text = self.decision if self.decision.startswith("{") else json.dumps(body)
            (self.out / f"DECISION_{self.step}.json").write_text(text, encoding="utf-8")


def make_rule(tmp_path, decision, step=10, **kw):
    cpu_calls = []

    def cpu_fn():
        cpu_calls.append(1)
        return 100.0

    sleep = FakeSleep(tmp_path, step, decision, cpu_calls=cpu_calls, cpu_log=[])
    rule = ht.HoldRule(tmp_path, cap_s=150.0, steps=20, from_step=10, cpu_fn=cpu_fn,
                       poll_s=0.01, sleep=sleep, **kw)
    return rule, sleep, cpu_calls


def test_no_hold_returns_none_and_writes_nothing(tmp_path):
    rule, sleep, _ = make_rule(tmp_path, "CONTINUE")
    assert rule(5) is None and sleep.calls == 0 and list(tmp_path.iterdir()) == []


def test_hold_writes_report_without_dev_ce_and_continue_exempts(tmp_path):
    rule, sleep, cpu_calls = make_rule(tmp_path, "CONTINUE")
    t0 = time.process_time()
    event = rule(10)
    assert time.process_time() - t0 < 1.0
    assert sleep.calls == 3 and all(sleep.hold_seen)
    assert len(set(sleep.cpu_log)) == 1  # nothing but sleep runs while waiting
    rep = json.loads((tmp_path / "HOLD_10.json").read_text(encoding="utf-8"))
    assert set(rep) == {"step", "cpu_s", "projected_s", "trigger", "utc"}
    assert rep["step"] == 10 and rep["cpu_s"] == 100.0 and rep["projected_s"] == 200.0
    assert rep["trigger"] == "PROJECTED" and "dev_ce" not in json.dumps(rep).lower()
    assert event is not None and len(rule.events) == 1 and rule.exempt is True
    assert rule(20) is None and not (tmp_path / "HOLD_20.json").exists()
    assert rule.events and len(rule.events) == 1


def test_stop_ends_inconclusive(tmp_path):
    rule, _, _ = make_rule(tmp_path, "STOP")
    with pytest.raises(hc.HwsbStop) as e:
        rule(10)
    assert str(e.value.status) == REFUSE
    assert (tmp_path / "HOLD_10.json").is_file()


@pytest.mark.parametrize("decision", ["MAYBE", "{not json"])
def test_unknown_or_unreadable_decision_is_hold_failure(tmp_path, decision):
    rule, _, _ = make_rule(tmp_path, decision)
    with pytest.raises(hc.HwsbStop) as e:
        rule(10)
    assert str(e.value.status) == "FAIL_TECHNICAL/HOLD"


def test_hold_report_refuses_overwrite(tmp_path):
    rule, _, _ = make_rule(tmp_path, "CONTINUE")
    (tmp_path / "HOLD_10.json").write_text("{}", encoding="utf-8")
    with pytest.raises(Exception):
        rule(10)  # exclusive create
    assert (tmp_path / "HOLD_10.json").read_text(encoding="utf-8") == "{}"


# ------------------------------------------------------------------ held trainings (RC-14)
def plan20():
    train = TrainConfig(steps=20, batch_size=32, lr=1e-3, warmup=2, schedule="cosine",
                        weight_decay=0.1, grad_clip=1.0, checkpoint_steps=(0, 10, 20),
                        device="auto")
    base = hc.dry_plan("dry_tiny", "BHOLD")
    return dataclasses.replace(base, train_cfg=train,
                               model_cfg=ModelConfig(**CONTRACT["dry_run"]["tiny_model"]),
                               sizes={**base.sizes, "train": 512, "dev": 128})


def world(plan):
    store = ArtifactStore(MemoryBackend())
    proc = hdry.build_tiny_process(store)
    ids = hd.make_train_dev(store, proc, MASTER, plan)
    return store, {"train": ids["train"], "dev": ids["dev"]}


def steps_in(store):
    return sorted(store.meta(i).config["step"] for i in store.find(Checkpoint))


def test_held_and_continued_run_equals_unheld_run_bitwise(tmp_path):
    plan = plan20()
    s1, ids1 = world(plan)
    s2, ids2 = world(plan)
    plain = ht.train(s1, ids1, MASTER, plan)
    rule, sleep, _ = make_rule(tmp_path, "CONTINUE")
    held = ht.train(s2, ids2, MASTER, plan, hold=rule)
    assert sleep.calls == 3 and (tmp_path / "HOLD_10.json").is_file()
    assert held["checksums"] == plain["checksums"] and set(held["checksums"]) == {0, 10, 20}
    assert held["checkpoint_ids"] == plain["checkpoint_ids"]
    assert len(held["holds"]) == 1 and plain["holds"] == []
    assert steps_in(s2) == [0, 10, 20]


def test_stop_at_a_hold_leaves_only_earlier_checkpoints(tmp_path):
    plan = plan20()
    store, ids = world(plan)
    rule, _, _ = make_rule(tmp_path, "STOP")
    with pytest.raises(hc.HwsbStop) as e:
        ht.train(store, ids, MASTER, plan, hold=rule)
    assert str(e.value.status) == REFUSE
    got = steps_in(store)
    assert 0 in got and 20 not in got and max(got) <= 10
