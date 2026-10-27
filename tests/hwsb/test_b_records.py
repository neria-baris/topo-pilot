"""Author B (job 0161), TEST_PLAN section 3 `test_b_records.py`: pause check (section 8.2), study
ledger (RC-7), AUTH/SCHED rules, store inventory snapshot/diff (section 6.4 rule 1), the G0
needle classification and search (RC-3, DRB15), FREEZE fields, and the dry-run refusal.
tools/hwsb/*.py unread; everything under pytest tmp_path."""

from __future__ import annotations

import builtins
import copy
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import hwsb_config as hc  # noqa: E402
import hwsb_driver as hdr  # noqa: E402
import hwsb_dry as hdry  # noqa: E402
import hwsb_known as hk  # noqa: E402
import hws_driver  # noqa: E402
from topo_pilot.contracts import canonical_json  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "hwsb" / "CONTRACT.json").read_text(encoding="utf-8"))
HWS_CONTRACT = json.loads((REPO / "tools" / "hws" / "CONTRACT.json").read_text(encoding="utf-8"))
CPU = CONTRACT["cpu"]
OWNER_SHA = CONTRACT["authority"]["owner_addendum_32"]["sha256"]
STAGES = ("DRY", "KB", "TRAIN", "EVAL")


# ------------------------------------------------------------------ pause_check
@pytest.mark.parametrize("stage", ["J-B1", "DRY", "KB", "TRAIN", "EVAL"])
def test_pause_check_is_strictly_greater_than_three_times(stage):
    fc, cum = CPU["central_s"][stage], CPU["cumulative_central_s"][stage]
    ok = hdr.pause_check(stage, 3 * fc, 3 * cum)
    assert ok["pause"] is False and ok["trigger"] is None
    assert ok["stage_threshold"] == 3 * fc and ok["cum_threshold"] == 3 * cum
    assert (ok["stage_cpu"], ok["cum_cpu"]) == (3 * fc, 3 * cum)
    st = hdr.pause_check(stage, 3 * fc + 0.01, 0.0)
    assert st["pause"] is True and st["trigger"] == "STAGE"
    cu = hdr.pause_check(stage, 0.0, 3 * cum + 0.01)
    assert cu["pause"] is True and cu["trigger"] == "CUMULATIVE"
    both = hdr.pause_check(stage, 3 * fc + 1, 3 * cum + 1)
    assert both["pause"] is True and both["trigger"] == "BOTH"


def test_pause_check_numbers_from_the_protocol():
    assert CPU["central_s"] == {"P0": 0, "J-B1": 600, "DRY": 300, "KB": 500, "TRAIN": 4850,
                                "EVAL": 400}
    r = hdr.pause_check("TRAIN", 14550.0, 18750.0)
    assert r["pause"] is False and r["stage_threshold"] == 14550 and r["cum_threshold"] == 18750
    assert hdr.pause_check("EVAL", 1200.0, 19950.0)["pause"] is False
    assert hdr.pause_check("EVAL", 1200.5, 0)["pause"] is True


# ------------------------------------------------------------------ study ledger
def test_ledger_read_default(tmp_path):
    assert hdr.ledger_read(tmp_path / "L.json") == {
        "study": "hwsb-v1", "entries": [], "cumulative_cpu_s": 0.0}


def test_ledger_append_entries_sum_and_atomic_replace(tmp_path, monkeypatch):
    path = tmp_path / "HWSB_CPU_LEDGER.json"
    replaced = []
    real = os.replace

    def spy(src, dst, *a, **k):
        replaced.append((Path(src).name, Path(dst).name))
        return real(src, dst, *a, **k)

    monkeypatch.setattr(os, "replace", spy)
    hdr.ledger_append(path, "0170", "KB", 410.25, "kb/cpu_ledger.json")
    hdr.ledger_append(path, "0171", "TRAIN", 4800.5, "t/cpu_ledger.json", master=620201)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["study"] == "hwsb-v1" and data["cumulative_cpu_s"] == pytest.approx(5210.75)
    e0, e1 = data["entries"]
    assert set(e0) == {"job", "stage", "cpu_s", "source", "master", "utc"}
    assert (e0["job"], e0["stage"], e0["cpu_s"], e0["master"]) == ("0170", "KB", 410.25, None)
    assert e1["master"] == 620201 and e1["source"] == "t/cpu_ledger.json"
    assert hdr.ledger_read(path)["cumulative_cpu_s"] == pytest.approx(5210.75)
    assert [p.name for p in tmp_path.iterdir()] == ["HWSB_CPU_LEDGER.json"]  # no .tmp left
    assert replaced and all(s.endswith(".json.tmp") and d == "HWSB_CPU_LEDGER.json"
                            for s, d in replaced)


def test_ledger_duplicate_job_is_refused(tmp_path):
    path = tmp_path / "L.json"
    hdr.ledger_append(path, "0170", "KB", 1.0, "s")
    before = path.read_bytes()
    with pytest.raises(hc.HwsbStop) as e:
        hdr.ledger_append(path, "0170", "KB", 2.0, "s")
    assert str(e.value.status) == "FAIL_TECHNICAL/LEDGER" and path.read_bytes() == before


# ------------------------------------------------------------------ AUTH and SCHED
def auth(**kw):
    base = {"job_id": "0170", "stages": list(STAGES), "owner_auth_sha256": OWNER_SHA,
            "hws_store_reads": ["KB5 S3 w* table", "H2-B hist identity count"]}
    return {**base, **kw}


@pytest.mark.parametrize("stage", STAGES)
def test_auth_ok_for_every_stage(stage):
    assert hdr.auth_ok(auth(), stage)["ok"] is True
    assert hdr.auth_ok(auth(stages=[s for s in STAGES if s != stage]), stage)["ok"] is False
    assert hdr.auth_ok(auth(owner_auth_sha256="0" * 64), stage)["ok"] is False


def sched(**kw):
    base = {f: None for f in CONTRACT["p_sched"]["record_fields"]}
    base.update(record="SCHED", utc="2026-10-27T00:00:00Z", coordinator_session="x",
                c2nd_state="S5", c2nd_s5_accepted=True, c2nd_pending_s5_rerun=False,
                c2nd_terminal=False, live_history_reservations=[])
    return {**base, **kw}


@pytest.mark.parametrize("stage", STAGES)
def test_sched_rule2_and_rule3(stage):
    need3 = stage != "DRY"
    r = hdr.sched_ok(sched(), stage)
    assert r["ok"] is True and r["rule2"] is True and r["rule3"] is True
    r = hdr.sched_ok(sched(live_history_reservations=["c2nd-run-1"]), stage)
    assert r["ok"] is False and r["rule2"] is False
    for kw in (dict(c2nd_s5_accepted=False), dict(c2nd_pending_s5_rerun=True)):
        r = hdr.sched_ok(sched(**kw), stage)
        assert r["rule3"] is False and r["ok"] is (not need3)
    r = hdr.sched_ok(sched(c2nd_s5_accepted=False, c2nd_terminal=True), stage)
    assert r["rule3"] is True and r["ok"] is True
    r = hdr.sched_ok(sched(c2nd_pending_s5_rerun=True, c2nd_terminal=True), stage)
    assert r["rule3"] is True and r["ok"] is True


def test_missing_sched_record_is_refused():
    for stage in STAGES:
        assert hdr.sched_ok(None, stage)["ok"] is False


# ------------------------------------------------------------------ inventory
def put_npz(path, **arrays):
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, **arrays)
    return str(path)


def synthetic_root(tmp_path):
    root = tmp_path / "root"
    put_npz(root / "alpha" / "h.npz", canon32=np.zeros((4, 32), np.uint8))
    put_npz(root / "alpha" / "ids.npz", seq_ids=np.arange(4))
    put_npz(root / "beta" / "other.npz", w=np.zeros(3))
    (root / "beta" / "artifacts" / "ObservationSet" / "abc").mkdir(parents=True)
    (root / "beta" / "artifacts" / "ObservationSet" / "abc" / "meta.json").write_text("{}")
    return root


def flat(snap):
    return {(top, kind): v for top, d in snap.items() for kind, v in d.items()}


def test_inventory_snapshot_lists_kinds(tmp_path):
    snap = hdr.inventory_snapshot(synthetic_root(tmp_path))
    assert set(snap) == {"alpha", "beta"}
    assert len(snap["alpha"]["history_files"]) == 1 and snap["alpha"]["history_files"][0].endswith("h.npz")
    assert len(snap["alpha"]["identity_refs"]) == 1
    assert len(snap["beta"]["observation_set_roots"]) == 1
    assert snap["alpha"]["unreadable"] == [] and snap["beta"]["history_files"] == []


def test_inventory_diff_unchanged_root_is_ok(tmp_path):
    root = synthetic_root(tmp_path)
    before = hdr.inventory_snapshot(root)
    d = hdr.inventory_diff(before, hdr.inventory_snapshot(root))
    assert d["ok"] is True and not any(v for t in d["new"].values() for v in t.values())


def test_inventory_diff_detects_new_history_identity_and_obs_root(tmp_path):
    root = synthetic_root(tmp_path)
    before = hdr.inventory_snapshot(root)
    new_hist = put_npz(root / "alpha" / "hist" / "LGATE.npz", canon32=np.ones((2, 32), np.uint8))
    new_id = put_npz(root / "beta" / "ids2.npz", sequence_id=np.arange(2))
    (root / "beta" / "more" / "ObservationSet" / "z").mkdir(parents=True)
    (root / "beta" / "more" / "ObservationSet" / "z" / "meta.json").write_text("{}")
    d = hdr.inventory_diff(before, hdr.inventory_snapshot(root))
    assert d["ok"] is False
    assert d["new"]["alpha"]["history_files"] == [new_hist]
    assert d["new"]["beta"]["identity_refs"] == [new_id]
    assert len(d["new"]["beta"]["observation_set_roots"]) == 1


def test_inventory_diff_new_top_level_directory_is_new(tmp_path):
    root = synthetic_root(tmp_path)
    before = hdr.inventory_snapshot(root)
    put_npz(root / "gamma" / "x.npz", canon32=np.ones((1, 32), np.uint8))
    d = hdr.inventory_diff(before, hdr.inventory_snapshot(root))
    assert d["ok"] is False and len(d["new"]["gamma"]["history_files"]) == 1
    quiet = tmp_path / "root" / "delta"
    quiet.mkdir()
    assert hdr.inventory_diff(hdr.inventory_snapshot(root), hdr.inventory_snapshot(root))["ok"]


# ------------------------------------------------------------------ G0 classification and search
HWS_FRAGS = HWS_CONTRACT["seeds"]["g0_declaration_fragments"]
HWS_JOBS = HWS_CONTRACT["seeds"]["g0_hws_job_scratch"]
P = "X:/Downloads/projects/topo-pilot"


def hit(path, needle="620201"):
    return {"path": path, "needle": needle, "line": 3}


PLANTED = ([hit(f"{P}/x{f}file.md") for f in HWS_FRAGS] + [hit(j + "n.md") for j in HWS_JOBS]
           + [hit(f"{P}/c2nd-store/x.json"), hit(f"{P}/topo-pilot/tools/k4b/n.md"),
              hit("X:\\Downloads\\projects\\topo-pilot\\AGENT-HANDOFF\\jobs\\0001\\t.md")])


@pytest.mark.parametrize("subset", ["declared", "mixed", "outside", "empty"])
def test_classify_hits_with_hws_lists_equals_hws_driver(subset):
    n = len(HWS_FRAGS) + len(HWS_JOBS)
    hits = {"declared": PLANTED[:n], "mixed": PLANTED, "outside": PLANTED[n:n + 2], "empty": []}[subset]
    got = hk.classify_hits(copy.deepcopy(hits), HWS_FRAGS, HWS_JOBS, "hws_declaration")
    assert got == hws_driver.classify_seed_hits(copy.deepcopy(hits))


def test_classify_hits_defaults_use_contract_fragments():
    for frag in CONTRACT["seeds"]["g0_declaration_fragments"]:
        res = hk.classify_hits([hit(f"{P}/x{frag}file.md")])
        assert res["status"] == "PASS" and res["hits"][0]["kind"] == "hwsb_declaration", frag
        up = hk.classify_hits([hit((P + "/x" + frag + "FILE.MD").replace("/", "\\").upper())])
        assert up["status"] == "PASS", frag
    res = hk.classify_hits([hit(f"{P}/tools/hwsb/a.py"), hit(f"{P}/c2nd-store/x.json")])
    assert res["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
    assert [h["kind"] for h in res["hits"]] == ["hwsb_declaration", "unclassified"]
    assert hk.classify_hits([])["status"] == "PASS"


def guard(monkeypatch, touched, bad):
    real = {"open": builtins.open, "io": io.open, "path": Path.open, "os": os.open}

    def check(p):
        if bad(str(p).replace("\\", "/")):
            touched.append(str(p))
            raise PermissionError(f"test guard: {p} must not be opened")

    monkeypatch.setattr(builtins, "open", lambda f, *a, **k: (check(f), real["open"](f, *a, **k))[1])
    monkeypatch.setattr(io, "open", lambda f, *a, **k: (check(f), real["io"](f, *a, **k))[1])
    monkeypatch.setattr(Path, "open", lambda s, *a, **k: (check(s), real["path"](s, *a, **k))[1])
    monkeypatch.setattr(os, "open", lambda f, *a, **k: (check(f), real["os"](f, *a, **k))[1])


def test_seed_search_whole_token_rule_and_excluded_folders(tmp_path, monkeypatch):
    root = tmp_path / "root"
    plant = {
        "keep/hit.json": '{"seed": 620201}\n',
        "keep/list.md": "seeds 620202, 7\n",
        "keep/scope.txt": "xhwsb-v1y\n",
        "keep/nohit1.json": '{"x": "6202019"}\n',
        "keep/nohit2.json": '{"x": "a620201"}\n',
        "keep/nohit3.json": '{"x": 1.6202011e-5}\n',
        ".git/config": "620201\n",
        "00_READ_ME_FIRST_Research_Summary_So_Far/s.md": "620201\n",
        "docs/research_summary/s.md": "620201\n",
    }
    for rel, text in plant.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    touched = []
    guard(monkeypatch, touched, lambda p: any(s in p for s in (".git/", "00_READ_ME_FIRST", "docs/research_summary/")))
    hits = hws_driver.seed_search(root, CONTRACT["seeds"]["g0_needles"])
    monkeypatch.undo()
    assert touched == []
    found = {(Path(h["path"]).name, h["needle"]) for h in hits}
    assert ("hit.json", "620201") in found and ("list.md", "620202") in found
    assert ("scope.txt", "hwsb-v1") in found
    assert not [f for f in found if f[0].startswith("nohit")]
    assert not [h for h in hits if ".git" in h["path"] or "research_summary" in h["path"]
                or "00_READ_ME" in h["path"]]


# ------------------------------------------------------------------ FREEZE and dry refusal
def git(cwd, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                           "-c", "commit.gpgsign=false", "-C", str(cwd), *args],
                          capture_output=True, text=True, check=True).stdout


def sha(data):
    return hashlib.sha256(data).hexdigest()


def synthetic_repo(tmp_path):
    repo = tmp_path / "repo"
    for rel in list(CONTRACT["reuse_sha256"]) + [
            f"tools/hwsb/{n}" for n in ("PROTOCOL_HWSB_v1.md", "CONTRACT.json", "API.md",
                                         "TEST_PLAN.md")]:
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / rel, repo / rel)
    extra = {"tools/hwsb/ENCLOSURE_PROOF.md": b"proof note\n", "tools/hwsb/fake_a.py": b"A = 1\n",
             "tests/hwsb/test_fake.py": b"def test_x():\n    pass\n",
             "tests/hwsb/AUTHORSHIP_Z.md": b"z\n"}
    for rel, data in extra.items():
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_bytes(data)
    git(repo, "init", "-q")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "synthetic")
    return repo, git(repo, "rev-parse", "HEAD").strip(), extra


def test_freeze_field_set_and_implementation_hash(tmp_path):
    repo, head, extra = synthetic_repo(tmp_path)
    files = {n: sha(extra[n]) for n in ("tools/hwsb/fake_a.py", "tests/hwsb/test_fake.py",
                                        "tests/hwsb/AUTHORSHIP_Z.md")}
    impl = sha(canonical_json(files).encode("utf-8"))
    dry = tmp_path / "DRY_RUN_REPORT.json"
    dry.write_text(json.dumps({"cases": {}, "all_pass": True, "implementation_sha256": impl}))
    out = tmp_path / "store"
    out.mkdir()
    rec = hdr.freeze(out, repo, head, dry)
    on_disk = json.loads((out / "FREEZE.json").read_text(encoding="utf-8"))
    assert set(CONTRACT["freeze_fields"]) <= set(on_disk) and set(CONTRACT["freeze_fields"]) <= set(rec)
    assert on_disk["h_exec"] == head and on_disk["protocol_sha256"] == CONTRACT["protocol_sha256"]
    assert on_disk["implementation_files"] == files and on_disk["implementation_sha256"] == impl
    assert on_disk["reuse_sha256"] == CONTRACT["reuse_sha256"]
    assert on_disk["dry_run_report_sha256"] == sha(dry.read_bytes())
    with pytest.raises(Exception):
        hdr.freeze(out, repo, head, dry)  # exclusive create
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"implementation_sha256": "0" * 64}))
    out2 = tmp_path / "store2"
    out2.mkdir()
    with pytest.raises(Exception):
        hdr.freeze(out2, repo, head, bad)  # differing implementation hash is refused
    assert not (out2 / "FREEZE.json").exists()


@pytest.mark.parametrize("record", [None, {"live_history_reservations": ["r1"]}])
def test_dry_run_refuses_without_rule2_sched(tmp_path, record):
    out = tmp_path / "dry"
    sch = None if record is None else sched(**record)
    # SPEC-QUESTION: API section 9 says only "refused"; accepted forms: a raised HwsbStop with
    # status INCONCLUSIVE/RESOURCE_OR_AUTHORITY, or a returned dict marked refused, never a pass.
    try:
        res = hdry.run_dry(out, sch)
    except hc.HwsbStop as e:
        assert str(e.value.status) == "INCONCLUSIVE/RESOURCE_OR_AUTHORITY"
    else:
        word = str(res.get("status", "")).upper()
        assert res.get("refused") is True or word.startswith(("INCONCLUSIVE", "REFUS"))
        assert res.get("all_pass") is not True
    assert not list(out.rglob("*.npz")) if out.exists() else True
    assert not (out / "stages" / "DRY" / "DRY_REPORT.json").exists()
