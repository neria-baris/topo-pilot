"""Author B: blindness guard, J9 search pruning, G0d needles and declarations (§9.2, J5, J9)."""

from __future__ import annotations  # noqa: I001

import json
import sys
from pathlib import Path

for _p in (Path(__file__).resolve().parent, Path(__file__).resolve().parents[2] / "tools" / "hwsd"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hwsd_config as dc  # noqa: E402
import hwsd_known as dk  # noqa: E402
import test_b_util as bu  # noqa: E402

import hwsc_known  # noqa: E402
import pytest  # noqa: E402

BLIND = "FAIL_TECHNICAL/BLINDNESS"
TRUE_REL = [
    "hwsc-store/stages/TRAIN", "hwsc-store/stages/TRAIN/x", "hwsc-store/stages/TRAIN/620301/TRAIN_RECORD.json",
    "hwsc-store/logs/meter.log", "hwsc-store/logs", "hwsc-store/stages/E1/L1.json",
    "agent-handoff/jobs/0187/review.md", "agent-handoff/jobs/0188/review.md",
    "agent-handoff/jobs/0189/review.md",
    "agent-handoff/planning/requests/coord-hws-use-20261101.md",
    "agent-handoff/planning/responses/coord-hws-use-20261101.v2.claude-reviewer.md",
    "agent-handoff/planning/responses/HWSU-v1.md", "agent-handoff/planning/responses/hwsu-x/y.md",
    "hwsb-store/REPORT.json", "hwsb-store/GATES.jsonl", "hwsb-store/stages/EVAL/a/b.json",
    "hwsb-store/CHART_CONSTRUCTIONS_trained.json", "agent-handoff/jobs/0175/review.md",
]
FALSE_REL = [
    "hwsc-store/stages/TRAIN.json", "hwsc-store/stages/TRAINING/x", "hwsc-store/logsx/a",
    "hwsc-store/stages/E1/L1.json.bak", "hwsc-store/stages/S8/RESULT.json",
    "hwsc-store/stages/TRAIN_x/OBS.json",
    "agent-handoff/jobs/0186/review.md", "agent-handoff/jobs/01870/review.md",
    "agent-handoff/jobs/0187/task.md", "agent-handoff/planning/responses/HWSD-v2.md",
    "agent-handoff/jobs/0200/HWSU-v1.md", "agent-handoff/records/HWS_UD_NAMESPACE.json",
    "hwsc-store/RESERVATION_W2.json",
]


@pytest.fixture
def roots(tmp_path):
    return tmp_path / "Root", tmp_path / "Scratch"


@pytest.mark.parametrize("rel", TRUE_REL)
def test_blinded_true(roots, rel):
    root, scratch = roots
    assert dc.blinded(root / rel, root, scratch) is True
    mixed = str(root / rel).upper().replace("/", "\\")
    assert dc.blinded(mixed, root, scratch) is True


@pytest.mark.parametrize("rel", FALSE_REL)
def test_blinded_false(roots, rel):
    root, scratch = roots
    assert dc.blinded(root / rel, root, scratch) is False


def test_blinded_scratch_job_folders(roots):
    root, scratch = roots
    assert dc.blinded(scratch / "hwsc-job-0181", root, scratch)
    assert dc.blinded(scratch / "hwsc-job-0196" / "logs" / "a.txt", root, scratch)
    assert dc.blinded(str(scratch / "HWSC-JOB-0187" / "x.json") + "/", root, scratch)
    assert not dc.blinded(scratch / "hwsc-jobs" / "a", root, scratch)
    assert not dc.blinded(scratch / "test_hwsd-0197" / "hwsc-job-1" / "a", root, scratch)
    assert not dc.blinded(scratch / "hwsc-dry-0177" / "a.npz", root, scratch)


SEARCHABLE = ["hwsu-store", "hwsu-store/reservations", "hwsu-store/REGISTRY_OBLIGATION_OF.json",
              "hwsu-store/REGISTRY_OBLIGATION.json", "hwsu-store/RESERVATION_W2.json",
              "hwsu-store/reservations/X.END.json", "hwsu-store/reservations/RES-HWSU-OF-a1.json"]
PRUNED = ["hwsu-store/artifacts", "hwsu-store/artifacts/ObservationSet/ab/meta.json",
          "hwsu-store/stages/x.json", "hwsu-store/reservations/sub/x.json",
          "hwsu-store/reservations/x.txt", "hwsu-store/GATES.jsonl", "hwsu-store/registry/K.json"]


@pytest.mark.parametrize("rel", SEARCHABLE)
def test_search_pruned_hwsu_searchable(roots, rel):
    root, scratch = roots
    assert dc.search_pruned(root / rel, root, scratch) is False
    assert dc.blinded(root / rel, root, scratch) is False  # decision 25: readers may read U data


@pytest.mark.parametrize("rel", PRUNED + TRUE_REL[:4])
def test_search_pruned_true(roots, rel):
    root, scratch = roots
    assert dc.search_pruned(root / rel, root, scratch) is True


def test_public_summary():
    assert dc.public_summary("X:/a/00_READ_ME_FIRST_Research_Summary_So_Far/x.pdf")
    assert dc.public_summary("X:/a/topo-pilot/docs/research_summary/main.tex")
    assert not dc.public_summary("X:/a/topo-pilot/docs/code_index/FILES.md")


def test_guard_refuses_before_any_open(tmp_path, monkeypatch):
    spy = bu.OpenSpy().install(monkeypatch)
    for p in (dc.ROOT / "hwsc-store/stages/TRAIN/620301/TRAIN_RECORD.json",
              dc.ROOT / "hwsc-store/logs/x.txt", dc.SCRATCH / "hwsc-job-0181/a.json",
              dc.ROOT / "topo-pilot/00_READ_ME_FIRST_Research_Summary_So_Far/a.pdf",
              dc.ROOT / "topo-pilot/docs/research_summary/a.tex"):
        for fn in (dc.guard, dc.read_json, dc.read_bytes):
            with pytest.raises(bu.C1GateFailure) as e:
                fn(p)
            assert bu.status_of(e.value) == BLIND
    assert spy.paths == []
    ok = bu.write_json(tmp_path / "ok.json", {"a": 1})
    assert dc.guard(ok) == ok and dc.read_json(ok) == {"a": 1} and dc.read_bytes(ok) == ok.read_bytes()


def _root(tmp_path) -> tuple[Path, Path]:
    root = tmp_path / "proj"
    scratch = root / "topo-scratch"
    files = {
        "tools/hwsd/CONTRACT.json": '{"u": "640101", "d": "hwsd-v1"}\n',
        "src/x.py": 'S = "hwsd-v1"\n',
        "hwsd-store/FREEZE.json": '{"seed": 620413}\n',
        "hwsc-store/stages/TRAIN/620301/TRAIN_RECORD.json": '{"seed": 620413}\n',
        "hwsc-store/logs/meter.log.txt": "620413\n",
        "hwsc-store/stages/E1/L1.json": '{"s": "620413"}\n',
        "agent-handoff/planning/responses/coord-hws-use-20261101.v2.md": "640101 hwsd-v1\n",
        "agent-handoff/planning/responses/HWSU-v2.md": "640101\n",
        "agent-handoff/jobs/0188/review.md": "620413\n",
        "topo-scratch/hwsc-job-0187/log.txt": "620413\n",
        "hwsu-store/artifacts/x.json": '{"s": 640101}\n',
        "hwsu-store/stages/S/a.json": '{"s": "hwsd-v1"}\n',
        "hwsu-store/REGISTRY_OBLIGATION_OF.json": '{"store": "hwsu-store", "n": 640101}\n',
        "hwsu-store/reservations/RES-HWSU-OF-a1.END.json": '{"r": "hwsd-dry-v1"}\n',
        "hwsb-store/REPORT.json": '{"s": 620413}\n',
    }
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return root, scratch


PRUNED_FILES = ["hwsc-store/stages/TRAIN", "hwsc-store/logs", "hwsc-store/stages/E1/L1.json",
                "agent-handoff/planning", "agent-handoff/jobs/0188/review.md",
                "topo-scratch/hwsc-job-0187", "hwsu-store/artifacts", "hwsu-store/stages",
                "hwsb-store/REPORT.json"]


def test_seed_search_d_prunes_before_opening(tmp_path, monkeypatch):
    root, scratch = _root(tmp_path)
    trip = bu.tripwire(monkeypatch, ["hwsc_known.seed_search_c"])
    spy = bu.OpenSpy().install(monkeypatch)
    hits = dk.seed_search_d(root, ["640101", "hwsd-v1", "620413", "hwsd-dry-v1"], scratch)
    assert trip == []
    got = {(Path(h["path"]).resolve().relative_to(root.resolve()).as_posix(), h["needle"])
           for h in hits}
    assert got == {("tools/hwsd/CONTRACT.json", "640101"), ("tools/hwsd/CONTRACT.json", "hwsd-v1"),
                   ("src/x.py", "hwsd-v1"), ("hwsd-store/FREEZE.json", "620413"),
                   ("hwsu-store/REGISTRY_OBLIGATION_OF.json", "640101"),
                   ("hwsu-store/reservations/RES-HWSU-OF-a1.END.json", "hwsd-dry-v1")}
    for rel in PRUNED_FILES:
        assert spy.opened_under(root / rel) == [], rel
    assert all(set(h) >= {"path", "needle", "line"} for h in hits)


def test_seed_search_d_equals_stage_c_search_without_pruned_paths(tmp_path, monkeypatch):
    root = tmp_path / "plain"
    for rel, text in {"a/b.json": '{"x": 620413}\n', "a/c.md": "x 6204130 620413\n",
                      "d.py": "s = 'hwsd-dry-v1'\n", "e.txt": "nothing\n", "f.bin": "620413",
                      ".git/x.json": "620413", "sealed/y.json": "620413"}.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    needles = ["620413", "hwsd-dry-v1", "hwsd-v1"]
    ref = hwsc_known.seed_search_c(root, needles)
    assert ref  # non-vacuous
    bu.tripwire(monkeypatch, ["hwsc_known.seed_search_c"])
    assert dk.seed_search_d(root, needles, scratch=tmp_path / "scr") == ref


def _ns() -> dict:
    p = dc.MAILBOX / "records" / "HWS_UD_NAMESPACE.json"
    assert bu.sha(p) == dc.CONTRACT["identity"]["rows"]["namespace"]["sha256"]
    return json.loads(p.read_text(encoding="utf-8"))


def test_needles_d_from_the_namespace_record():
    ns = _ns()
    n = dk.needles_d(ns)
    assert list(n["own"]) == list(dc.NEEDLES) == dc.CONTRACT["seeds"]["g0_needles"]
    want = {"hwsu-of-v1", "hwsu-v1", "hwsu-dry-v1"} | {str(i) for i in range(640101, 640121)} \
        | {str(i) for i in range(649901, 649921)}
    assert set(n["other"]) == want and len(n["other"]) == len(want) == 43


def test_overlap_check():
    ns = _ns()
    r = dk.overlap_check(ns)
    assert r["status"] == "PASS" and not r["common"]
    bad = json.loads(json.dumps(ns))
    bad["tracks"]["U"]["seed_blocks"].append([620450, 620451])
    r = dk.overlap_check(bad)
    assert r["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
    assert {str(x) for x in r["common"]} >= {"620450", "620451"} or len(r["common"]) >= 2
    bad = json.loads(json.dumps(ns))
    bad["tracks"]["U"]["scopes"].append("hwsd-dry-v1")
    assert dk.overlap_check(bad)["status"] == "FAIL_TECHNICAL/SEED_SCOPE"


TP = "X:/Downloads/projects/topo-pilot"
DECLARED = [
    (f"{TP}/hwsd-store/FREEZE.json", "620413"),
    (f"{TP}/topo-pilot/docs/code_index/files/tools/hwsd/hwsd_config.md", "hwsd-v1"),
    (f"{TP}/topo-pilot/tools/hwsu/CONTRACT.json", "629965"),
    (f"{TP}/topo-pilot-hwsd/tools/hwsd/CONTRACT.json", "640101"),
    (f"{TP}/topo-pilot-hwsd/tests/hwsd/test_b_x.py", "hwsu-v1"),
    (f"{TP}/hwsu-store/REGISTRY_OBLIGATION_OF.json", "620413"),
    ("X:/Downloads/topo-scratch/hwsd-dry/DRD1/x.json", "640101"),
    ("X:/Downloads/topo-scratch/test_hwsu-0198/pytest/a.json", "629951"),
    ("X:/Downloads/topo-scratch/hwsu-dry-0199/REGISTRY_OBLIGATION.json", "hwsd-v1"),
    (f"{TP}/agent-handoff/records/HWS_UD_NAMESPACE.json", "640101"),
    (f"{TP}/coord-scratch/d9a66698/note.md", "620416"),
]


def _classify(hits):
    frags = dc.CONTRACT["seeds"]["g0_declaration_fragments"]
    return hwsc_known.classify_hits_c(hits, fragments=frags, job_scratch=[])


def test_j9_fragments_classify_declarations():
    hits = [{"path": p.replace("/", "\\"), "needle": n, "line": 1} for p, n in DECLARED]
    r = _classify(hits)
    assert r["status"] == "PASS", [h for h in r["hits"] if h["kind"] == "unclassified"]
    assert dc.CONTRACT["seeds"]["g0_job_scratch"] == []


@pytest.mark.parametrize("path", [f"{TP}/topo-pilot/src/x.py", f"{TP}/topo-pilot/tools/hwsc/x.py",
                                  "X:/Downloads/topo-scratch/0089/a.json",
                                  f"{TP}/hwsc-store/stages/S8/RESULT.json"])
def test_j9_tokens_elsewhere_are_unclassified(path):
    hits = [{"path": p, "needle": n, "line": 1} for p, n in DECLARED]
    hits += [{"path": path, "needle": "640101", "line": 3}, {"path": path, "needle": "hwsd-v1", "line": 4}]
    assert _classify(hits)["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
