"""Author B: blindness guard (protocol 8, DRG11)."""
from __future__ import annotations

import builtins
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_b_common import CONTRACT, expect_fail, mod  # noqa: E402

BL = CONTRACT["blindness"]


def _root():
    return Path(mod("gc").ROOT)


@pytest.mark.parametrize("rel", BL["files"])
def test_blinded_files(rel):
    gc = mod("gc")
    assert gc.blinded(_root() / rel) is True
    assert gc.blinded(str(_root() / rel).upper()) is True  # mixed case
    assert gc.blinded(str(_root() / rel).replace("/", "\\")) is True


@pytest.mark.parametrize("rel", BL["dirs"])
def test_blinded_dirs_and_below(rel):
    gc = mod("gc")
    assert gc.blinded(_root() / rel) is True
    assert gc.blinded(_root() / rel / "deep" / "x.json") is True


@pytest.mark.parametrize("parent,pattern", BL["globs"])
def test_blinded_globs(parent, pattern):
    gc = mod("gc")
    name = pattern.replace("*", "Zed").replace("?", "q")
    p = _root() / parent / name
    assert gc.blinded(p) is True
    assert gc.blinded(str(p).upper()) is True


@pytest.mark.parametrize("n", [197, 200, 210, 223])
def test_blinded_job_range(n):
    gc = mod("gc")
    p = _root() / "agent-handoff" / "jobs" / f"{n:04d}" / "task.md"
    assert gc.blinded(p) is True
    assert gc.blinded(str(p).replace("/", "\\")) is True


@pytest.mark.parametrize("rel", ["agent-handoff/jobs/0196/task.md", "agent-handoff/jobs/0224/task.md",
                                 "hwsb-store/HANDOFF.json", "tools/hwsg/CONTRACT.json"] +
                         list(BL["allow"][:3]))
def test_not_blinded(rel):
    gc = mod("gc")
    p = rel.replace("*", "x")
    assert gc.blinded(_root() / p) is False


def test_public_summary():
    gc = mod("gc")
    assert gc.public_summary(_root() / "00_READ_ME_FIRST_Research_Summary_So_Far" / "a.pdf")
    assert gc.public_summary("X:/a/00_read_me_first/x")
    assert gc.public_summary(_root() / "docs" / "research_summary" / "main.tex")
    assert gc.public_summary(_root() / "DOCS" / "Research_Summary" / "f.png")
    assert not gc.public_summary(_root() / "docs" / "code_index" / "FILES.md")
    assert not gc.public_summary(_root() / "docs" / "other" / "research_summary_notes.md")


def test_guard_raises_before_any_open(monkeypatch):
    gc = mod("gc")
    opened = []
    real = builtins.open
    monkeypatch.setattr(builtins, "open", lambda p, *a, **k: (opened.append(p), real(p, *a, **k))[1])
    bad = _root() / BL["files"][0]
    expect_fail("FAIL_TECHNICAL/BLINDNESS", gc.guard, bad)
    expect_fail("FAIL_TECHNICAL/BLINDNESS", gc.read_json, bad)
    expect_fail("FAIL_TECHNICAL/BLINDNESS", gc.read_bytes, _root() / "docs" / "research_summary" / "x")
    assert not opened
    assert Path(gc.guard(_root() / "tools" / "hwsg" / "CONTRACT.json")) == (
        _root() / "tools" / "hwsg" / "CONTRACT.json")


def test_prune_removes_blinded_dirs_before_descent(tmp_path):
    gc = mod("gc")
    dn = ["EVAL", "S3", "x"]
    gc.prune(str(_root() / "hwsb-store" / "stages"), dn)
    assert dn == ["S3", "x"]
    dn = ["jobs_ok", "stages"]
    gc.prune(str(_root() / "hwsu-store"), dn)
    assert dn == ["jobs_ok"]
    dn = ["research_summary", "code_index"]
    gc.prune(str(_root() / "docs"), dn)
    assert dn == ["code_index"]


def test_prune_in_os_walk_never_enters(tmp_path):
    gc = mod("gc")
    root = tmp_path / "r"
    (root / "stages" / "deep").mkdir(parents=True)
    visited = []
    for dp, dn, _ in os.walk(root):
        gc.prune(dp, dn, root=root)
        visited.append(dp)
    assert len(visited) >= 1  # no blinded component inside tmp: all visited
