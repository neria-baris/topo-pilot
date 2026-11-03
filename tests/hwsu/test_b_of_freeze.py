"""Author B (job 0198): FREEZE_OF.json, its verification with the append-only prefix check for
API.md/TEST_PLAN.md (D-0, coordinator ruling on D-0), and OF-B (protocol §4.1, §4.2 OF-B; API
§5.3-§5.4; DRO7). Every git repository is a fixture under tmp_path; the reused files are copied
byte for byte from their blobs at r_ref = e3710d2 of this worktree's history (read-only)."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
import hwsu_bind as ub  # noqa: E402
import hwsu_records as ur  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

C = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))
R_REF = C["of_b"]["r_ref"]
DOCS = ["tools/hwsu/PROTOCOL_HWSU_v1.md", "tools/hwsu/API.md", "tools/hwsu/CONTRACT_OF.json",
        "tools/hwsu/TEST_PLAN.md"]
TESTS = ["tests/hwsu/test_a_of_fixture.py", "tests/hwsu/test_b_of_fixture.py",
         "tests/hwsu/AUTHORSHIP_A.md", "tests/hwsu/AUTHORSHIP_B.md"]
GIT = ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
       "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false"]


def _git(repo, *args) -> str:
    return subprocess.run(GIT + ["-C", str(repo), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _put(repo, rel, data: bytes):
    p = Path(repo) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def _reuse_blobs() -> dict:
    keys = sorted(C["reuse_sha256"])
    inp = "".join(f"{R_REF}:{k}\n" for k in keys).encode("utf-8")
    raw = subprocess.run(["git", "-C", str(REPO), "cat-file", "--batch"], input=inp, check=True,
                         capture_output=True).stdout
    out, i = {}, 0
    for k in keys:
        j = raw.index(b"\n", i)
        size = int(raw[i:j].split()[2])
        out[k] = raw[j + 1:j + 1 + size]
        i = j + 1 + size + 1
    return out


@pytest.fixture(scope="module")
def base_repo(tmp_path_factory):
    repo = tmp_path_factory.mktemp("frz") / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    blobs = _reuse_blobs()
    for k, b in blobs.items():
        assert _sha(b) == C["reuse_sha256"][k], k  # the CONTRACT table equals the blobs at r_ref
        _put(repo, k, b)
    _put(repo, "docs/code_index/FILES.md", b"index v0\n")
    _put(repo, "notes/keep.txt", b"keep\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "r_ref fixture")
    r_ref = _git(repo, "rev-parse", "HEAD")
    for rel in DOCS:
        _put(repo, rel, (REPO / rel).read_bytes())
    for rel in C["phase1_files"]:
        if rel.endswith(".py"):
            _put(repo, rel, f"# fixture {rel}\n".encode("utf-8"))
    for rel in TESTS:
        _put(repo, rel, f"# fixture {rel}\n".encode("utf-8"))
    _put(repo, "docs/code_index/FILES.md", b"index v1\n")
    _put(repo, "docs/code_index/files/tools/hwsu/hwsu_config.py.md", b"page\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "h_exec fixture")
    return repo, r_ref, _git(repo, "rev-parse", "HEAD")


def _clone(base_repo, tmp_path):
    repo, r_ref, h = base_repo
    dst = tmp_path / "repo"
    shutil.copytree(repo, dst)
    store = tmp_path / "hwsu-store"
    store.mkdir()
    return dst, r_ref, h, store


def _impl(repo, h) -> dict:
    files = _git(repo, "ls-tree", "-r", "--name-only", h).splitlines()
    want = set(C["phase1_files"]) | set(TESTS)
    return {f: _sha(subprocess.run(["git", "-C", str(repo), "cat-file", "blob", f"{h}:{f}"],
                                   check=True, capture_output=True).stdout)
            for f in files if f in want}


def _canon_sha(obj) -> str:
    return _sha(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _report(tmp_path, repo, h, **over) -> Path:
    rec = {"all_pass": True, "implementation_sha256": _canon_sha(_impl(repo, h)), "h_exec": h}
    rec.update(over)
    p = tmp_path / "DRY_OF_REPORT.json"
    p.write_bytes(json.dumps(rec).encode("utf-8"))
    return p


def _jof(tmp_path) -> list:
    p = tmp_path / "J-OF-0300-a1.json"
    p.write_bytes(b'{"status": "PASS", "fixture": true}')
    return [p]


def _freeze(tmp_path, repo, h, store, **over):
    return ur.freeze_of(store, repo, h, _report(tmp_path, repo, h, **over), _jof(tmp_path),
                        "fixture coordinator")


def _status(fn, *a, **k):
    try:
        d = fn(*a, **k)
    except C1GateFailure as exc:
        return exc.status
    return (d or {}).get("status", "PASS")


# ------------------------------------------------------------------ freeze_of (API §5.3)
@pytest.fixture(scope="module")
def frozen_base(base_repo, tmp_path_factory):
    repo, r_ref, h, store = _clone(base_repo, tmp_path_factory.mktemp("frozen"))
    _freeze(store.parent, repo, h, store)
    return repo, r_ref, h, store


def test_freeze_of_fields(frozen_base, tmp_path):
    repo, r_ref, h, store = _frozen(frozen_base, tmp_path)
    raw = (store / "FREEZE_OF.json").read_bytes()
    f = json.loads(raw)
    assert set(f) == set(C["freeze_of_fields"])
    blob = {rel: (repo / rel).read_bytes() for rel in DOCS}
    assert f["protocol_sha256"] == _sha(blob[DOCS[0]]) == C["protocol_sha256"]
    assert f["contract_of_sha256"] == _sha(blob[DOCS[2]])
    assert (f["api_sha256"], f["api_bytes"]) == (_sha(blob[DOCS[1]]), len(blob[DOCS[1]]))
    assert (f["test_plan_sha256"], f["test_plan_bytes"]) == (_sha(blob[DOCS[3]]), len(blob[DOCS[3]]))
    assert f["h_exec"] == h and f["r_ref"] == R_REF
    impl = _impl(repo, h)
    assert len(impl) == len(C["phase1_files"]) + len(TESTS)
    assert f["implementation_files"] == impl
    assert f["implementation_sha256"] == _canon_sha(impl)
    assert f["reuse_sha256"] == C["reuse_sha256"]
    assert f["dry_run_report_sha256"] == _sha((frozen_base[3].parent / "DRY_OF_REPORT.json").read_bytes())
    assert [e["sha256"] for e in f["j_of_records"]] == [_sha(_jof(tmp_path)[0].read_bytes())]
    assert set(f["environment"]) >= {"python", "numpy", "platform"}
    assert f["written_by"] == "fixture coordinator"


@pytest.mark.parametrize("over", [{"implementation_sha256": "0" * 64}, {"all_pass": False}])
def test_freeze_of_refuses_dro_report(base_repo, tmp_path, over):
    repo, r_ref, h, store = _clone(base_repo, tmp_path)
    assert _status(_freeze, tmp_path, repo, h, store, **over) == "FAIL_TECHNICAL/FREEZE"
    assert not (store / "FREEZE_OF.json").exists()


def test_freeze_of_refuses_changed_reuse_blob(base_repo, tmp_path):
    repo, r_ref, h, store = _clone(base_repo, tmp_path)
    rel = "tools/hwsc/hwsc_config.py"
    _put(repo, rel, (repo / rel).read_bytes() + b"\n# changed\n")
    _git(repo, "commit", "-q", "-am", "changes a reused file")
    h2 = _git(repo, "rev-parse", "HEAD")
    assert _status(_freeze, tmp_path, repo, h2, store) == "FAIL_TECHNICAL/FREEZE"
    assert not (store / "FREEZE_OF.json").exists()


# ------------------------------------------------------------------ verify_freeze_of (D-0)
def _frozen(frozen_base, tmp_path):
    repo, r_ref, h, store = frozen_base
    shutil.copytree(repo, tmp_path / "repo")
    shutil.copytree(store, tmp_path / "hwsu-store")
    return tmp_path / "repo", r_ref, h, tmp_path / "hwsu-store"


def test_verify_passes_and_allows_appends(frozen_base, tmp_path):
    repo, r_ref, h, store = _frozen(frozen_base, tmp_path)
    assert _status(ur.verify_freeze_of, store, repo) == "PASS"
    for rel in ("tools/hwsu/API.md", "tools/hwsu/TEST_PLAN.md"):
        _put(repo, rel, (repo / rel).read_bytes() + b"\n## 17. Phase 2 section (fixture)\n")
    assert _status(ur.verify_freeze_of, store, repo) == "PASS"


@pytest.mark.parametrize("rel", ["tools/hwsu/API.md", "tools/hwsu/TEST_PLAN.md"])
@pytest.mark.parametrize("where", ["first", "middle", "last"])
def test_verify_refuses_byte_change_inside_prefix(frozen_base, tmp_path, rel, where):
    repo, r_ref, h, store = _frozen(frozen_base, tmp_path)
    b = bytearray((repo / rel).read_bytes())
    i = {"first": 0, "middle": len(b) // 2, "last": len(b) - 1}[where]
    b[i] = (b[i] + 1) % 256
    _put(repo, rel, bytes(b) + b"appended\n")
    assert _status(ur.verify_freeze_of, store, repo) == "INVALID"


@pytest.mark.parametrize("rel", ["tools/hwsu/API.md", "tools/hwsu/TEST_PLAN.md"])
def test_verify_refuses_truncated_document(frozen_base, tmp_path, rel):
    repo, r_ref, h, store = _frozen(frozen_base, tmp_path)
    _put(repo, rel, (repo / rel).read_bytes()[:-1])
    assert _status(ur.verify_freeze_of, store, repo) == "INVALID"


@pytest.mark.parametrize("rel", ["tools/hwsu/hwsu_config.py", "tools/hwsu/hwsu_records.py",
                                 "tools/hwsu/CONTRACT_OF.json", "tools/hwsu/PROTOCOL_HWSU_v1.md",
                                 "tests/hwsu/test_b_of_fixture.py", "tests/hwsu/AUTHORSHIP_A.md",
                                 "tools/hwsb/hwsb_known.py"])
def test_verify_refuses_any_other_change(frozen_base, tmp_path, rel):
    repo, r_ref, h, store = _frozen(frozen_base, tmp_path)
    _put(repo, rel, (repo / rel).read_bytes() + b"\n")  # an append is a change for these
    assert _status(ur.verify_freeze_of, store, repo) == "INVALID"


def test_verify_absent_freeze(base_repo, tmp_path):
    repo, r_ref, h, store = _clone(base_repo, tmp_path)
    assert _status(ur.verify_freeze_of, store, repo) == "INVALID"


# ------------------------------------------------------------------ OF-B (API §5.4; DRO7)
def _audit(status):
    """A stub with the API §7 shape of hwsu_bind.audit."""
    return {"status": status, "calls": {"status": status, "unlisted": [], "never_called": [],
                                        "n_refs": 0},
            "reads": {"status": status, "unlisted": [], "forbidden": []}}


@pytest.fixture
def audit_pass(monkeypatch):
    calls = []
    monkeypatch.setattr(ub, "audit", lambda *a, **k: (calls.append(1), _audit("PASS"))[1])
    return calls


def test_of_b_refuses_changed_phase1_file_after_freeze(frozen_base, tmp_path, audit_pass):
    repo, r_ref, h, store = _frozen(frozen_base, tmp_path)
    _put(repo, "tools/hwsu/hwsu_of.py", b"# changed after FREEZE_OF\n")
    assert _status(ur.of_b, store, repo, r_ref) == "INVALID"


def _commit_and_freeze(frozen_base, tmp_path, change):
    """A freeze record at a new commit that leaves every phase-1 and test file unchanged: the
    module freeze record with h_exec replaced (same implementation map, so equally valid)."""
    repo, r_ref, h, store = _frozen(frozen_base, tmp_path)
    change(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture change")
    h2 = _git(repo, "rev-parse", "HEAD")
    f = json.loads((store / "FREEZE_OF.json").read_text(encoding="utf-8"))
    assert _impl(repo, h2) == f["implementation_files"]
    f["h_exec"] = h2
    (store / "FREEZE_OF.json").unlink()
    (store / "FREEZE_OF.json").write_bytes(json.dumps(f, indent=1).encode("utf-8"))
    return repo, r_ref, store


@pytest.mark.parametrize("name,change", [
    ("new file outside the allowlist", lambda r: _put(r, "tools/hwsc/new_helper.py", b"x\n")),
    ("modified non-index file", lambda r: _put(r, "notes/keep.txt", b"changed\n")),
    ("deleted file", lambda r: (r / "notes" / "keep.txt").unlink()),
    ("unlisted tests file", lambda r: _put(r, "tests/hwsu/conftest.py", b"x\n")),
    ("unlisted hwsu module", lambda r: _put(r, "tools/hwsu/hwsu_extra.py", b"x\n")),
])
def test_of_b_refuses_diff_outside_allowlist(frozen_base, tmp_path, audit_pass, name, change):
    repo, r_ref, store = _commit_and_freeze(frozen_base, tmp_path, change)
    assert _status(ur.verify_freeze_of, store, repo) == "PASS"  # the freeze itself is consistent
    assert _status(ur.of_b, store, repo, r_ref) == "INVALID", name


def test_of_b_pass_with_code_index_changes(frozen_base, tmp_path, audit_pass):
    """OF-B PASS: phase-1 and test files added, docs/code_index/** added and modified."""
    repo, r_ref, store = _commit_and_freeze(
        frozen_base, tmp_path, lambda r: _put(r, "docs/code_index/files/tools/hwsu/new.md", b"p\n"))
    r = ur.of_b(store, repo, r_ref)
    assert r["status"] == "PASS" and audit_pass
    assert r["h_exec"] == json.loads((store / "FREEZE_OF.json").read_text(encoding="utf-8"))["h_exec"]
    diff = json.dumps(r["diff"])
    assert "tools/hwsu/hwsu_config.py" in diff and "docs/code_index/FILES.md" in diff
    assert "tests/hwsu/AUTHORSHIP_B.md" in diff and "docs/code_index/files/tools/hwsu/new.md" in diff


def test_of_b_refuses_reused_file_change_in_tree(frozen_base, tmp_path, audit_pass):
    repo, r_ref, h, store = _frozen(frozen_base, tmp_path)
    rel = "tools/c1prime/c1_records.py"
    _put(repo, rel, (repo / rel).read_bytes() + b"\n")
    assert _status(ur.of_b, store, repo, r_ref) == "INVALID"


def test_of_b_refuses_failed_audit_and_absent_freeze(base_repo, frozen_base, tmp_path, monkeypatch):
    repo, r_ref, h, store = _frozen(frozen_base, tmp_path)
    monkeypatch.setattr(ub, "audit", lambda *a, **k: _audit("FAIL_TECHNICAL/BINDING"))
    assert _status(ur.of_b, store, repo, r_ref) == "INVALID"
    repo2, r2, h2, store2 = _clone(base_repo, tmp_path / "b")
    assert _status(ur.of_b, store2, repo2, r2) == "INVALID"
