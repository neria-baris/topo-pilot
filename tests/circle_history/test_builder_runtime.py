"""BUILDER tests (not independent): job binding, stage ceilings, release refusals, static
scored-access audit and import hygiene. See BUILDER_TESTS.md."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.analysis
REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools" / "x4_circle_history"
for extra in (TOOL, REPO / "tools" / "x4_oracle_profile", REPO / "tests" / "oracle_profile"):
    sys.path.insert(0, str(extra))

import meter_bind  # noqa: E402
import release  # noqa: E402


def _ledger(tmp_path, entries):
    caps = meter_bind.CONTRACT["resources"]["stage_caps_s"]  # v2.4: ledgers carry cap metadata
    ledger = {"entries": entries, "stage_caps_s": caps}
    (tmp_path / "cpu_ledger.json").write_text(json.dumps(ledger), encoding="utf-8")


@pytest.fixture()
def bound(tmp_path, monkeypatch):
    contract = copy.deepcopy(meter_bind.CONTRACT)
    contract["resources"]["output_root"] = str(tmp_path)
    contract["resources"].pop("cpu_policy", None)  # v2.5: these tests pin the legacy capped path
    monkeypatch.setattr(meter_bind, "CONTRACT", contract)
    for name in ("JOB_ID", "TASK_SHA256"):
        monkeypatch.setattr(meter_bind.controls, name, getattr(meter_bind.controls, name))
    for name in (
        "OUT",
        "LEDGER",
        "EMERGENCY",
        "LOCK",
        "ACTIVE",
        "LOG_DIR",
        "CAP_S",
        "STOP_NEW_S",
        "OUTPUT_CAP",
    ):
        monkeypatch.setattr(meter_bind.meter, name, getattr(meter_bind.meter, name))
    return tmp_path


def test_binding_points_unchanged_modules_at_this_job(bound):
    _ledger(bound, [])
    meter_bind.rewrite_argv(["--stage", "implementation", "--label", "x", "--", "cmd"])
    assert meter_bind.controls.JOB_ID == meter_bind.CONTRACT["job_id"]  # v2.5: job-bound
    assert meter_bind.controls.TASK_SHA256 == meter_bind.CONTRACT["task_sha256"].upper()
    assert meter_bind.meter.LEDGER == bound / "cpu_ledger.json"
    assert meter_bind.meter.CAP_S == 3600.0 and meter_bind.meter.STOP_NEW_S == 3480.0


def test_stage_label_and_ceiling(bound):
    _ledger(
        bound,
        [
            {"label": "implementation:a", "charged_cpu_s": 390.5},
            {"label": "export:b", "charged_cpu_s": 10.0},
        ],
    )
    args = meter_bind.rewrite_argv(
        ["--stage", "implementation", "--label", "t", "--max-cpu", "600", "--", "cmd", "arg"]
    )
    assert args[args.index("--label") + 1] == "implementation__t"
    assert float(args[args.index("--max-cpu") + 1]) == pytest.approx(400 - 390.5 - 1.0)
    assert args[args.index("--") + 1 :] == ["cmd", "arg"]


@pytest.mark.parametrize(
    "stage,spent", [("implementation", 399.5), ("export", 79.2), ("charts", 0.0), ("oracle", 0.0)]
)
def test_exhausted_or_unreleased_stage_runs_noop(bound, stage, spent):
    _ledger(bound, [{"label": f"{stage}:a", "charged_cpu_s": spent}])
    args = meter_bind.rewrite_argv(["--stage", stage, "--label", "t", "--", "cmd"])
    assert args[args.index("--label") + 1].endswith("__REFUSED_stage_ceiling_or_unreleased")
    assert args[-1] == "raise SystemExit(4)" and "cmd" not in args


def test_export_cap_is_80_without_release(bound):
    _ledger(bound, [])
    args = meter_bind.rewrite_argv(["--stage", "export", "--label", "t", "--", "cmd"])
    assert float(args[args.index("--max-cpu") + 1]) == pytest.approx(79.0)


def _mailbox(tmp_path, job="0099"):
    box = tmp_path / "box"
    (box / "jobs" / job).mkdir(parents=True)
    task = b"synthetic release task\n"
    (box / "jobs" / job / "task.md").write_bytes(task)
    digest = hashlib.sha256(task).hexdigest().upper()
    (box / "request.json").write_text(
        json.dumps({"command": "RUN_NEXT", "job_id": job, "task_sha256": digest}), encoding="utf-8"
    )
    runtime = {"mode": "ISOLATED_IMPLEMENTATION_RUNNING"}  # v2.5: Codex-era runtime
    (box / "coordinator_runtime.json").write_text(json.dumps(runtime), encoding="utf-8")
    out = tmp_path / "out"
    out.mkdir()
    (out / "FREEZE.json").write_text("{}", encoding="utf-8")
    rel = {
        "schema": release.SCHEMA,
        "job_id": job,
        "task_sha256": digest,
        "released_stages": ["identity"],
        "source_commit": release._head(),
        "freeze_sha256": hashlib.sha256(b"{}").hexdigest(),
        "contract_sha256": hashlib.sha256((TOOL / "CONTRACT.json").read_bytes()).hexdigest(),
        "scoring_released": False,
        "issued_by": "codex-coordinator",
    }
    return box, out, rel


def _write(box, rel, job="0099"):
    path = box / "jobs" / job / "RELEASE.json"
    path.write_text(json.dumps(rel), encoding="utf-8")
    return path


def test_release_accepts_exact_binding(tmp_path):
    box, out, rel = _mailbox(tmp_path)
    assert release.verify(_write(box, rel), mailbox=box, out=out)["job_id"] == "0099"


@pytest.mark.parametrize(
    "field,value",
    [
        ("task_sha256", "0" * 64),
        ("job_id", "0098"),
        ("source_commit", "0" * 40),
        ("freeze_sha256", "0" * 64),
        ("contract_sha256", "0" * 64),
        ("issued_by", "someone"),
        ("schema", "other"),
        ("released_stages", ["identity", "scoring_everything"]),
        ("scoring_released", True),
    ],
)
def test_release_refuses_any_mismatch(tmp_path, field, value):
    box, out, rel = _mailbox(tmp_path)
    rel[field] = value
    with pytest.raises(release.ReleaseError):
        release.verify(_write(box, rel), mailbox=box, out=out)


def test_release_refuses_wrong_location_and_unreadable(tmp_path):
    box, out, rel = _mailbox(tmp_path)
    elsewhere = tmp_path / "RELEASE.json"
    elsewhere.write_text(json.dumps(rel), encoding="utf-8")
    with pytest.raises(release.ReleaseError):
        release.verify(elsewhere, mailbox=box, out=out)
    with pytest.raises(release.ReleaseError):
        release.verify(tmp_path / "missing.json", mailbox=box, out=out)


def test_runner_refuses_without_release(tmp_path):
    import runner

    assert runner.main(["--release", str(tmp_path / "none.json"), "--stage", "identity"]) == 3


SIDE_EFFECT_FREE = (
    "errors",
    "cochain",
    "chart",
    "scores",
    "precision",
    "error_bound",
    "adapter",
    "runner",
    "live_context",
    "release",
    "meter_bind",
    "freeze_bind",
    "run_tests_bind",
    "process_law",
    "reference_cache",
    "stage_records",
    "precision_stage",
    "op_guard",
    "env_identity",
)


@pytest.mark.parametrize("name", SIDE_EFFECT_FREE)
def test_module_top_level_has_no_calls_with_io(name):
    tree = ast.parse((TOOL / f"{name}.py").read_text(encoding="utf-8"))
    allowed_calls = {
        "insert",
        "Path",
        "resolve",
        "frozenset",
        "dict",
        "str",
        "_verify_taylor_constants",
        "_eps_v",
        "loads",
        "read_text",
        "Fraction",
        "float",
        "range",
    }
    for node in tree.body:
        for sub in ast.walk(node):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.If)):
                break
            if isinstance(sub, ast.Call):
                func = sub.func
                fname = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
                assert fname in allowed_calls, f"{name}: top-level call {fname}"


def test_static_scored_access_audit():
    runner_src = (TOOL / "runner.py").read_text(encoding="utf-8")
    tree = ast.parse(runner_src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "panels":
                assert ast.literal_eval(node.args[1]) == (1, 2)
            if node.func.attr in ("certify_rows", "reference_check_rows"):
                assert not any(k.arg == "scoring_release" for k in node.keywords)
        if isinstance(node, ast.keyword) and node.arg == "scoring_release":
            raise AssertionError("runner must never pass a scoring release")
    for name in ("runner", "live_context"):
        assert "scoring_release=" not in (TOOL / f"{name}.py").read_text(encoding="utf-8")
    assert 'SPLITS = (("calibration", 1), ("validation", 2))' in runner_src
