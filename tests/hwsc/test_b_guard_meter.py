"""Author B (job 0176): the blindness guard (exactly the R-0176-G1 five-path list), the G0c seed
search and its mirror equality (R-0176-G2), hit classification, and the meter binding (DRC11,
DRC13, DRC14, KC0 pieces).

Written from PROTOCOL_HWSC_v1.md sections 4 (KC0), 8.3, 9.2, API.md sections 1.4, 5, 9 and 18,
CONTRACT.json `blindness`, `seeds`, `resources` and TEST_PLAN.md section 3 only. Every blinded
file here is a fixture copy under tmp_path; the real blinded paths are only passed to the pure
`blinded` predicate as strings.
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_HWSC = str(REPO / "tools" / "hwsc")
if sys.path[0] != _HWSC:
    sys.path.insert(0, _HWSC)

import hwsc_config as cc  # noqa: E402, I001
import hwsc_known as ck  # noqa: E402
import hwsc_meter_bind as cm  # noqa: E402
import c1_records  # noqa: E402
import controls  # noqa: E402
import hwsb_known  # noqa: E402
import hws_driver  # noqa: E402
import k4b_meter_bind as kmb  # noqa: E402
import meter  # noqa: E402
import winjob  # noqa: E402

C = cc.CONTRACT
GiB = 1024**3
PROJECT = Path("X:/Downloads/projects/topo-pilot")
_REC: list | None = None


def _audit(event, args):
    if _REC is not None and event in ("open", "os.scandir", "os.listdir") and args:
        _REC.append((event, str(args[0]).replace("\\", "/").lower()))


sys.addaudithook(_audit)


@pytest.fixture
def rec():
    global _REC
    _REC = []
    yield _REC
    _REC = None


def _opened(records, path):
    p = Path(path).as_posix().lower()
    return [x for e, x in records if e == "open" and x.endswith(p.split(":", 1)[-1])]


def _write(path, text="{}"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


BLINDED = ["hwsb-store/REPORT.json", "hwsb-store/GATES.jsonl", "hwsb-store/stages/EVAL",
           "hwsb-store/stages/EVAL/x.json", "hwsb-store/stages/EVAL/a/b/ACTS.npz",
           "hwsb-store/CHART_CONSTRUCTIONS_trained.json",
           "hwsb-store/CHART_CONSTRUCTIONS_init.json", "agent-handoff/jobs/0175/review.md",
           "HWSB-Store/Report.JSON", "hwsb-store/Stages/Eval/y.json",
           "Agent-Handoff/Jobs/0175/REVIEW.md"]
READABLE = ["agent-handoff/jobs/0175/task.json", "agent-handoff/jobs/0175/request.before.json",
            "agent-handoff/jobs/0175/task.md", "hwsb-store/HANDOFF.json",
            "hwsb-store/superseded/0168-a1/GATES.jsonl", "agent-handoff/jobs/01750/review.md",
            "hwsb-store/stages/EVALX/x.json", "hwsb-store/stages",
            "hwsb-store/stages/S4a/CHART_CONSTRUCTIONS_x.json", "hwsb-store/REPORT.json.bak",
            "other-store/REPORT.json", "hwsb-store/FREEZE.json"]


# ---------------------------------------------------------------- blinded / public_summary
def test_blindness_list_is_exactly_the_five_rules():
    assert C["blindness"]["stage_b"] == [
        "hwsb-store/REPORT.json", "hwsb-store/stages/EVAL/**", "hwsb-store/GATES.jsonl",
        "hwsb-store/CHART_CONSTRUCTIONS_*.json", "agent-handoff/jobs/0175/review.md"]


@pytest.mark.parametrize("rel", BLINDED)
def test_blinded_true(tmp_path, rel):
    p = tmp_path / rel
    assert cc.blinded(p, root=tmp_path) is True
    assert cc.blinded(str(p).replace("/", "\\"), root=tmp_path) is True
    assert cc.blinded(p.as_posix(), root=tmp_path) is True


@pytest.mark.parametrize("rel", READABLE)
def test_blinded_false(tmp_path, rel):
    assert cc.blinded(tmp_path / rel, root=tmp_path) is False


def test_blinded_default_root_is_pure():
    assert cc.blinded(PROJECT / "hwsb-store" / "REPORT.json") is True
    assert cc.blinded("X:/Downloads/projects/topo-pilot/hwsb-store/stages/EVAL/B1.json") is True
    assert cc.blinded(PROJECT / "hwsb-store" / "HANDOFF.json") is False


@pytest.mark.parametrize("rel,want", [
    ("00_READ_ME_FIRST_Research_Summary/a.pdf", True), ("x/00_read_me_first.md", True),
    ("docs/research_summary/main.tex", True), ("docs/research_summary", True),
    ("Docs/Research_Summary/fig.png", True), ("docs/research_summary_old/x", False),
    ("mydocs/research_summary/x", False), ("docs/code_index/FILES.md", False),
    ("x/read_me_first.md", False)])
def test_public_summary(tmp_path, rel, want):
    assert cc.public_summary(tmp_path / rel) is want


# ---------------------------------------------------------------- guard / read_json
@pytest.mark.parametrize("rel", ["hwsb-store/REPORT.json", "hwsb-store/GATES.jsonl",
                                 "hwsb-store/stages/EVAL/x.json",
                                 "hwsb-store/CHART_CONSTRUCTIONS_trained.json",
                                 "agent-handoff/jobs/0175/review.md",
                                 "00_READ_ME_FIRST_x/a.json", "docs/research_summary/b.json"])
def test_guard_refuses_before_any_open(tmp_path, rec, rel):
    p = _write(tmp_path / rel, '{"blinded": 620301}')
    rec.clear()
    for fn in (cc.guard, cc.read_json, cc.read_bytes):
        with pytest.raises(c1_records.C1GateFailure) as e:
            fn(p, root=tmp_path)
        assert e.value.status == "FAIL_TECHNICAL/BLINDNESS"
    assert not _opened(rec, p)


@pytest.mark.parametrize("rel", ["agent-handoff/jobs/0175/task.json",
                                 "agent-handoff/jobs/0175/request.before.json",
                                 "hwsb-store/HANDOFF.json"])
def test_guard_reads_dispatch_metadata(tmp_path, rel):
    p = _write(tmp_path / rel, '{"job": "0175", "ok": true}')
    assert Path(cc.guard(p, root=tmp_path)) == p
    assert cc.read_json(p, root=tmp_path) == {"job": "0175", "ok": True}
    assert cc.read_bytes(p, root=tmp_path) == p.read_bytes()
    md = _write(tmp_path / "agent-handoff/jobs/0175/task.md", "# task")
    assert cc.read_bytes(md, root=tmp_path) == b"# task"


# ---------------------------------------------------------------- G0c pieces
@pytest.mark.parametrize("needle,line,want", [
    ("620301", "seed 620301,", True), ("620301", "620301", True), ("620301", '"620301"', True),
    ("620301", "a620301b", False), ("620301", "6203011", False), ("620301", "x620301f9", False),
    ("620301", "_620301", False), ("620301", "1620301", False),
    ("hwsc-v1", "xhwsc-v1y", True), ("hwsc-v1", "hwsc-v2", False)])
def test_needle_in(needle, line, want):
    assert ck.needle_in(needle, line) is want
    assert hws_driver._needle_in(needle, line) is want  # the mirrored rule


def _seed_root(root, blinded=True):
    _write(root / "a" / "decl.json", 'x = "620301",\n')
    _write(root / "a" / "notes.md", "seed 620301,\nnothing\nhwsc-v1 here\n")
    _write(root / "a" / "bad.txt", "a620301b 6203011 0x620301f\n")
    _write(root / "a" / "data.bin", "620301\n")
    _write(root / "b" / "c" / "conf.yaml", "k: 629911\n")
    _write(root / "b" / "x.jsonl", '{"s": 620315}\n')
    _write(root / "b" / "code.py", "M = (620301, 620302)\n")
    _write(root / "b" / "table.csv", "620301\n")
    for rel in (".git/c.json", "sealed/s.json", "__pycache__/p.py", "00_READ_ME_FIRST_x/r.md",
                "docs/research_summary/m.md", "a/00_read_me_first.txt", ".venv/v.py"):
        _write(root / rel, "620301 hwsc-v1\n")
    if blinded:
        for rel in ("hwsb-store/REPORT.json", "hwsb-store/GATES.jsonl",
                    "hwsb-store/stages/EVAL/e.json", "hwsb-store/CHART_CONSTRUCTIONS_init.json",
                    "agent-handoff/jobs/0175/review.md"):
            _write(root / rel, "620301 hwsc-v1\n")
        _write(root / "agent-handoff" / "jobs" / "0175" / "task.json", '{"seed": 620301}\n')
        _write(root / "hwsb-store" / "HANDOFF.json", '{"x": "hwsc-v1"}\n')


def _rel(root, hits):
    return {(Path(h["path"]).relative_to(root).as_posix(), h["needle"], h["line"]) for h in hits}


def test_seed_search_c_prunes_and_never_opens_blinded(tmp_path, rec):
    root = tmp_path / "root"
    _seed_root(root)
    rec.clear()
    hits = ck.seed_search_c(root, ["620301", "hwsc-v1"])
    assert _rel(root, hits) == {("a/decl.json", "620301", 1), ("a/notes.md", "620301", 1),
                                ("a/notes.md", "hwsc-v1", 3), ("b/code.py", "620301", 1),
                                ("agent-handoff/jobs/0175/task.json", "620301", 1),
                                ("hwsb-store/HANDOFF.json", "hwsc-v1", 1)}
    for rel in ("hwsb-store/REPORT.json", "hwsb-store/GATES.jsonl", "hwsb-store/stages/EVAL/e.json",
                "hwsb-store/CHART_CONSTRUCTIONS_init.json", "agent-handoff/jobs/0175/review.md",
                "00_READ_ME_FIRST_x/r.md", "docs/research_summary/m.md"):
        assert not _opened(rec, root / rel), rel
    assert not [x for e, x in rec if e != "open" and x.endswith("hwsb-store/stages/eval")]


def test_seed_search_c_equals_hws_mirror_without_blinded_paths(tmp_path):
    root = tmp_path / "root"
    _seed_root(root, blinded=False)
    needles = ["620301", "hwsc-v1", "629911", "620315", "620302"]
    mine, ref = ck.seed_search_c(root, needles), hws_driver.seed_search(root, needles)
    assert mine == ref and len(ref) >= 5


def test_classify_hits_c(tmp_path):
    paths = ["X:/Downloads/projects/topo-pilot/topo-pilot-hws/tools/hwsc/CONTRACT.json",
             "X:/Downloads/projects/topo-pilot/topo-pilot-hws/tests/hwsc/test_b_x.py",
             "X:\\Downloads\\projects\\topo-pilot\\agent-handoff\\jobs\\0176\\task.md",
             "X:/Downloads/projects/topo-pilot/hwsc-store/GATES.jsonl",
             "X:/Downloads/projects/topo-pilot/coord-scratch/n.md",
             "X:/Downloads/projects/topo-pilot/topo-pilot/docs/code_index/FILES.md",
             "X:\\Downloads\\topo-scratch\\hwsc-dry-0180\\stages\\DRY\\DRY_REPORT.json",
             "X:/Downloads/topo-scratch/hwsc-dry/x.json",
             "X:/Downloads/topo-scratch/test_hwsc-0176/pytest/x.json"]
    hits = [{"path": p, "needle": "620301", "line": 1} for p in paths]
    r = ck.classify_hits_c(hits)
    assert r["status"] == "PASS" and {h["kind"] for h in r["hits"]} == {"hwsc_declaration"}
    assert r == hwsb_known.classify_hits(hits, C["seeds"]["g0_declaration_fragments"],
                                         C["seeds"]["g0_job_scratch"], label="hwsc_declaration")
    for bad in ("X:/Downloads/projects/topo-pilot/topo-pilot/README.md",
                "X:/Downloads/topo-scratch/hwsb-dry/x.json", "X:/Downloads/topo-scratch/0180/x"):
        r = ck.classify_hits_c(hits + [{"path": bad, "needle": "620301", "line": 2}])
        assert r["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
        assert r["hits"][-1]["kind"] != "hwsc_declaration"


# ---------------------------------------------------------------- meter binding
@pytest.fixture
def meter_state(monkeypatch):
    for mod in (meter, winjob, kmb, controls):
        for name in [n for n in vars(mod) if n.isupper()]:
            monkeypatch.setattr(mod, name, getattr(mod, name))
    monkeypatch.setattr(meter, "limit_reason", meter.limit_reason)
    saved = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(saved)


CAPS = {"TRAIN": 8 * GiB, "J-C1": 8 * GiB, "DRY": 12 * GiB, "KC": 12 * GiB, "E1": 12 * GiB,
        "E2": 12 * GiB, "REG2": 12 * GiB}


@pytest.mark.parametrize("stage", list(CAPS))
def test_bind_per_stage(tmp_path, meter_state, stage):
    out, temp = tmp_path / "out", tmp_path / "tr"
    assert cm.memory_cap(stage) == CAPS[stage]
    cm.bind("0176b", "ab" * 32, out, "sess-b", stage, temp)
    assert winjob.MEMORY_CAP == CAPS[stage]
    assert kmb.TEMP_ROOT == str(temp)
    assert Path(meter.OUT) == out and Path(meter.LEDGER) == out / "cpu_ledger.json"
    assert Path(meter.LOCK) == out / "RUN.lock" and Path(meter.LOG_DIR) == out / "logs"
    assert meter.CAP_S == math.inf and meter.STOP_NEW_S == math.inf
    assert meter.OUTPUT_CAP == 4 * GiB
    env = kmb.child_env("0176b")
    for k in ("TEMP", "TMP", "TMPDIR"):
        assert Path(env[k]) == temp / "tmp-0176b"
    assert all(env[v] == "1" for v in meter.THREAD_VARS)
    argv = kmb.rewrite_argv(["run", "--max-cpu", "60", "--max-wall", "90"])
    assert argv[-4:] == ["--max-cpu", "inf", "--max-wall", "inf"] and "60" not in argv
    s = cm.effective_settings()
    assert {"memory_cap", "temp_root", "ledger", "cap_s", "output_cap", "thread_vars"} <= set(s)
    assert s["memory_cap"] == CAPS[stage]


def test_bind_default_temp_root_and_unknown_stage(tmp_path, meter_state):
    cm.bind("0176b", "ab" * 32, tmp_path / "out", "sess-b", "KC")
    assert kmb.TEMP_ROOT == str(tmp_path / "out")
    assert cm.memory_cap("REG2") == cm.memory_cap("E2") == C["resources"]["memory_cap_bytes"]["E2"]
    with pytest.raises(ValueError):
        cm.memory_cap("EVAL")


def test_job_paths_and_placement():
    t = cm.job_paths("0180", "test")
    assert Path(t["out"]) == Path(cc.SCRATCH) / "test_hwsc-0180" == Path(t["temp_root"])
    assert Path(t["basetemp"]) == Path("X:/Downloads/topo-scratch/test_hwsc-0180/pytest")
    s = cm.job_paths("0180", "store")
    assert Path(s["out"]) == PROJECT / "hwsc-store" and s["basetemp"] is None
    assert Path(s["temp_root"]) == PROJECT / "hwsc-store" / "tmp"
    with pytest.raises(ValueError):
        cm.job_paths("0180", "dry")
    assert cm.placement_ok(t)["ok"] is True and cm.placement_ok(s)["ok"] is True
    inside = dict(t, out=PROJECT / "test_x", temp_root=PROJECT / "test_x",
                  basetemp=PROJECT / "test_x" / "pytest")
    assert cm.placement_ok(inside)["ok"] is False
    unprefixed = dict(t, out=Path(cc.SCRATCH) / "hwsc-x", temp_root=Path(cc.SCRATCH) / "hwsc-x")
    assert cm.placement_ok(unprefixed)["ok"] is False


def test_this_suite_runs_outside_the_project(tmp_path):
    p = tmp_path.resolve().as_posix().lower()
    assert not p.startswith(PROJECT.as_posix().lower())
    assert any(part.lower().startswith("test_hwsc-") for part in tmp_path.resolve().parts)
    import tempfile

    assert not Path(tempfile.gettempdir()).resolve().as_posix().lower().startswith(
        PROJECT.as_posix().lower())


def _argv(**drop):
    a = {"--job": "b0176", "--task-sha256": "ab" * 32, "--session": "mine-session-b",
         "--kind": "test", "--stage": "DRY"}
    for k in drop:
        a.pop("--" + k.replace("_", "-"))
    return ["hwsc_meter_bind"] + [x for kv in a.items() for x in kv] + ["python", "-c", "pass"]


def _main_code():
    try:
        return cm.main()
    except SystemExit as e:
        return e.code


@pytest.mark.parametrize("drop", ["stage", "job", "kind", "session", "task_sha256"])
def test_main_missing_argument_is_2(monkeypatch, meter_state, drop):
    called = []
    monkeypatch.setattr(meter, "main", lambda *a, **k: called.append(1) or 0)
    monkeypatch.setattr(sys, "argv", _argv(**{drop: True}))
    assert _main_code() == 2 and not called


def test_main_unknown_stage_is_2(monkeypatch, meter_state):
    monkeypatch.setattr(meter, "main", lambda *a, **k: 0)
    argv = _argv()
    argv[argv.index("--stage") + 1] = "EVAL"
    monkeypatch.setattr(sys, "argv", argv)
    assert _main_code() == 2


def test_main_refuses_a_foreign_run_lock(tmp_path, monkeypatch, meter_state):
    scr = tmp_path / "scr"
    monkeypatch.setattr(cc, "SCRATCH", scr)
    monkeypatch.setattr(cm, "SCRATCH", scr, raising=False)
    out = Path(cm.job_paths("b0176", "test")["out"])
    if scr not in out.parents:
        pytest.skip("API-AMBIGUITY: job_paths does not read SCRATCH at call time")
    _write(out / "RUN.lock", json.dumps({"session": "another-session", "job": "x"}))
    called = []
    monkeypatch.setattr(meter, "main", lambda *a, **k: called.append(1) or 0)
    monkeypatch.setattr(sys, "argv", _argv())
    assert _main_code() == 3 and not called
