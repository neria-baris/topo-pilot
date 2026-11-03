"""Author B (job 0223, phase 2): the execution freeze FREEZE.json and S0 (API_U2 2.2; protocol 4.1,
6 row S0). The repository under test is this worktree (read-only: git ls-tree / cat-file / diff);
the store is a tmp_path copy holding byte copies of the real OF_ACCEPT.json and FREEZE_OF.json (so
the R-0206-1 hashes of CONTRACT hold). Nothing is written to the real store."""

from __future__ import annotations

import hashlib
import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
from c1_records import C1GateFailure  # noqa: E402

FREEZE_FAIL = "FAIL_TECHNICAL/FREEZE"
P2 = json.loads((REPO / "tools" / "hwsu" / "CONTRACT.json").read_text(encoding="utf-8"))


def _known():
    importlib.import_module("u2")
    return importlib.import_module("hwsu_known")


def _git(*args) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


def _canon_sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()  # noqa: E501


def _store(tmp_path) -> Path:
    real = uc.STORE
    if not (real / "OF_ACCEPT.json").exists() or not (real / "FREEZE_OF.json").exists():
        pytest.skip("no real hwsu-store records")
    s = tmp_path / "hwsu-store"
    s.mkdir()
    for n in ("OF_ACCEPT.json", "FREEZE_OF.json"):
        shutil.copyfile(real / n, s / n)
    return s


def _report(tmp_path, h, **over) -> Path:
    impl = _known().implementation_files_u(REPO, h)
    rec = {"all_pass": True, "implementation_sha256": _canon_sha(impl), "h_exec": h}
    rec.update(over)
    p = tmp_path / "DRY_U2_REPORT.json"
    p.write_bytes(json.dumps(rec).encode("utf-8"))
    return p


def _ju(tmp_path) -> list:
    p = tmp_path / "J-U-0300-a1.json"
    p.write_bytes(b'{"status": "PASS", "fixture": true}')
    return [p]


def _freeze(tmp_path, store, **over):
    h = _git("rev-parse", "HEAD")
    return _known().freeze_u(store, REPO, h, _report(tmp_path, h, **over), _ju(tmp_path),
                             "fixture coordinator")


def _status(fn, *a, **k):
    try:
        d = fn(*a, **k)
    except C1GateFailure as exc:
        return exc.status
    return (d or {}).get("status", "PASS")


@pytest.fixture(scope="module")
def frozen(tmp_path_factory):
    base = tmp_path_factory.mktemp("frzu")
    store = _store(base)
    h = _git("rev-parse", "HEAD")
    _freeze(base, store)
    return base, store, h


def _copy(frozen, tmp_path):
    base, store, h = frozen
    s = tmp_path / "hwsu-store"
    shutil.copytree(store, s)
    return s, h


def test_implementation_files_u_names_phase2_files_and_tests():
    h = _git("rev-parse", "HEAD")
    impl = _known().implementation_files_u(REPO, h)
    present = set(_git("ls-tree", "-r", "--name-only", h).splitlines())
    assert set(impl) <= set(P2["phase2_files"]) | {f for f in present if f.startswith("tests/hwsu/")}  # noqa: E501
    for f, sha in impl.items():
        blob = subprocess.run(["git", "-C", str(REPO), "cat-file", "blob", f"{h}:{f}"], check=True,
                              capture_output=True).stdout
        assert hashlib.sha256(blob).hexdigest() == sha
    assert all(f.startswith(("tools/hwsu/", "tests/hwsu/")) for f in impl)
    assert not any(f.endswith(("test_a_of_gates.py", "test_b_of_bind.py")) for f in impl)  # phase 1 tests  # noqa: E501
    assert any(f.startswith("tests/hwsu/test_b_u2_") for f in impl)


def test_freeze_u_writes_contract_fields(frozen):
    base, store, h = frozen
    rec = json.loads((store / "FREEZE.json").read_text(encoding="utf-8"))
    assert set(P2["freeze_u2_fields"]) <= set(rec)
    assert rec["h_exec"] == h and rec["r_ref"] == P2["s0_u2"]["r_ref"]
    assert rec["protocol_sha256"] == P2["contract_phase2"]["protocol_sha256"]
    assert rec["contract_of_sha256"] == P2["contract_of_sha256"]
    assert rec["freeze_of_sha256"] == uc.CONTRACT["authority_u2"]["freeze_of"]["sha256"]
    assert rec["of_accept_sha256"] == uc.CONTRACT["authority_u2"]["of_accept"]["sha256"]
    assert rec["implementation_sha256"] == _canon_sha(rec["implementation_files"])
    assert rec["dry_run_report_sha256"] == hashlib.sha256(
        (base / "DRY_U2_REPORT.json").read_bytes()).hexdigest()
    ru = {**uc.CONTRACT["reuse_sha256"], **uc.CONTRACT["reuse_sha256_u2"]}
    rt = rec["reuse_sha256"]
    flat = rt if all(isinstance(v, str) for v in rt.values()) else {k: v for t in rt.values() for k, v in t.items()}  # noqa: E501
    assert flat == ru  # phase-1 table union phase-2 table (a separate sub-dict form is also accepted)  # noqa: E501


def test_freeze_u_is_exclusive(frozen, tmp_path):
    base, store, h = frozen
    s, _ = _copy(frozen, tmp_path)
    before = (s / "FREEZE.json").read_bytes()
    assert _status(_freeze, tmp_path, s) != "PASS"
    assert (s / "FREEZE.json").read_bytes() == before


def test_freeze_u_refuses_other_implementation_sha256_and_writes_nothing(tmp_path):
    store = _store(tmp_path)
    assert _status(_freeze, tmp_path, store, implementation_sha256="0" * 64) == FREEZE_FAIL
    assert not (store / "FREEZE.json").exists()


def test_freeze_u_refuses_all_pass_false_and_writes_nothing(tmp_path):
    store = _store(tmp_path)
    assert _status(_freeze, tmp_path, store, all_pass=False) == FREEZE_FAIL
    assert not (store / "FREEZE.json").exists()


def test_freeze_u_refuses_when_verify_freeze_of_fails(tmp_path):
    store = _store(tmp_path)
    p = store / "FREEZE_OF.json"
    rec = json.loads(p.read_text(encoding="utf-8"))
    k = sorted(rec["implementation_files"])[0]
    rec["implementation_files"][k] = "0" * 64
    p.write_text(json.dumps(rec), encoding="utf-8")
    assert _status(_freeze, tmp_path, store) in (FREEZE_FAIL, "INCONCLUSIVE/AUTHORITY", "INVALID")
    assert not (store / "FREEZE.json").exists()


def test_verify_freeze_u_passes_on_the_unmodified_freeze(frozen, tmp_path):
    s, _ = _copy(frozen, tmp_path)
    assert _status(_known().verify_freeze_u, s, REPO) == "PASS"


def test_verify_freeze_u_absent_is_invalid(tmp_path):
    store = _store(tmp_path)
    assert _status(_known().verify_freeze_u, store, REPO) == "INVALID"


def _tamper(s, table, key=None):
    p = s / "FREEZE.json"
    rec = json.loads(p.read_text(encoding="utf-8"))
    t = rec[table]
    k = key or sorted(t)[0]
    t[k] = "0" * 64
    p.write_text(json.dumps(rec), encoding="utf-8")
    return k


def test_verify_freeze_u_detects_a_changed_phase2_file(frozen, tmp_path):
    s, _ = _copy(frozen, tmp_path)
    rec = json.loads((s / "FREEZE.json").read_text(encoding="utf-8"))
    py = [k for k in rec["implementation_files"] if k.startswith("tools/hwsu/u2/")]
    _tamper(s, "implementation_files", py[0] if py else None)
    assert _status(_known().verify_freeze_u, s, REPO) == "INVALID"


def test_verify_freeze_u_detects_a_changed_reused_file_in_either_table(frozen, tmp_path):
    for sel in (0, -1):
        s = tmp_path / f"s{sel}"
        shutil.copytree(frozen[1], s)
        p = s / "FREEZE.json"
        rec = json.loads(p.read_text(encoding="utf-8"))
        rt = rec["reuse_sha256"]
        # either one merged table or the two tables keyed separately
        flat = rt if all(isinstance(v, str) for v in rt.values()) else rt[sorted(rt)[sel]]
        flat[sorted(flat)[sel]] = "0" * 64
        p.write_text(json.dumps(rec), encoding="utf-8")
        assert _status(_known().verify_freeze_u, s, REPO) == "INVALID"


def test_s0_u_refuses_a_diff_touching_a_phase1_file(frozen, tmp_path):
    """r_ref far enough back that the diff contains phase-1 files (status A): refused."""
    s, _ = _copy(frozen, tmp_path)
    old = json.loads((REPO / "tools" / "hwsu" / "CONTRACT_OF.json").read_text(encoding="utf-8"))["of_b"]["r_ref"]  # noqa: E501
    assert _status(_known().s0_u, s, REPO, r_ref=old) == "INVALID"


def test_s0_u_accepts_the_real_diff_once_the_tree_is_committed(frozen, tmp_path):
    s, h = _copy(frozen, tmp_path)
    diff = _git("diff", "--no-renames", "--name-status", P2["s0_u2"]["r_ref"], h).splitlines()
    ok = []
    for ln in diff:
        st, path = ln.split("\t", 1)
        a = (st == "A" and (path in P2["phase2_files"] or path.startswith("docs/code_index/")
                            or path.startswith(("tests/hwsu/test_a_u2_", "tests/hwsu/test_b_u2_"))
                            or path in ("tests/hwsu/AUTHORSHIP_A_U2.md", "tests/hwsu/AUTHORSHIP_B_U2.md")))  # noqa: E501
        m = (st == "M" and path.startswith("docs/code_index/"))
        ok.append(a or m)
    if not all(ok):
        pytest.skip("HEAD diff from r_ref contains lines outside the S0 allow list (work in progress)")  # noqa: E501
    r = _known().s0_u(s, REPO)
    assert r["status"] == "PASS" and r["h_exec"] == h and r["audit"]
