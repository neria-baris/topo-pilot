"""Author B (job 0119), TEST_PLAN §3 `test_b_kc1.py` (KC1, DR7, RC-2) plus the G0 seed-scope
search of `test_b_records.py` (§6.6, choice 33, ruling R-0118-5), which shares the "never opened"
proof: patched `open`/`io.open`/`Path.open`/`os.open`/`np.load` record every touched path.

The synthetic artifact store is written under tmp_path by the src stages themselves
(`WorldStage`, `ProcessStage.run_transition`, `ProcessStage.run_emission` on a `LocalFSBackend`),
so meta.json, extra.json and the serialization envelope are the producer's own. Then every
`payload.npz` is deleted (or replaced by unreadable bytes), and a manifest
(`INPUT_IDENTITIES.json`: artifact_root, artifacts[kind/id] = {sha256, meta_sha256}) and a
config.json (`inputs_sha256["INPUT_IDENTITIES.json"]`) are written. Each tamper changes one item
and re-seals everything downstream, so only the targeted check can fail.

Written without reading tools/hws/*.py."""

from __future__ import annotations

import builtins
import hashlib
import io
import json
import os
import shutil
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hws") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hws"))

import hws_worlds as hw  # noqa: E402
import hws_exact as he  # noqa: E402
import hws_driver as hd  # noqa: E402

from topo_pilot.contracts import (  # noqa: E402
    ArtifactStore,
    LocalFSBackend,
    SeedTree,
    canonical_json,
    make_artifact_id,
)
from topo_pilot.process import EmissionConfig, ProcessStage, TransitionConfig  # noqa: E402
from topo_pilot.world import WorldConfig, WorldStage  # noqa: E402

CONTRACT = json.loads((REPO / "tools" / "hws" / "CONTRACT.json").read_text(encoding="utf-8"))
SEEDS = (1729, 2718, 3141)
FAIL = "FAIL_TECHNICAL/KNOWN_CASE"
FORBIDDEN = ("payload.npz",)


def _sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _status(fn, *args, **kwargs) -> str:
    """A KC1 failure may come back as a status or as a raised HwsStop; both are accepted."""
    try:
        return fn(*args, **kwargs)["status"]
    except hw.HwsStop as exc:
        return exc.status


def _guard(monkeypatch, touched, bad):
    """Record (and refuse) every open of a path for which `bad(path)` is true."""
    real = {"open": builtins.open, "io": io.open, "path": Path.open, "os": os.open,
            "load": np.load}

    def check(p):
        if bad(str(p).replace("\\", "/")):
            touched.append(str(p))
            raise PermissionError(f"test guard: {p} must not be opened")

    def g_open(file, *a, **k):
        check(file)
        return real["open"](file, *a, **k)

    def g_io(file, *a, **k):
        check(file)
        return real["io"](file, *a, **k)

    def g_path(self, *a, **k):
        check(self)
        return real["path"](self, *a, **k)

    def g_os(path, *a, **k):
        check(path)
        return real["os"](path, *a, **k)

    def g_load(file, *a, **k):
        check(file)
        return real["load"](file, *a, **k)

    monkeypatch.setattr(builtins, "open", g_open)
    monkeypatch.setattr(io, "open", g_io)
    monkeypatch.setattr(Path, "open", g_path)
    monkeypatch.setattr(os, "open", g_os)
    monkeypatch.setattr(np, "load", g_load)


# ------------------------------------------------------------------ synthetic store

@pytest.fixture(scope="module")
def base(tmp_path_factory):
    root = tmp_path_factory.mktemp("kc1base") / "artifacts"
    store = ArtifactStore(LocalFSBackend(root), producer_version="synthetic-0119-author-b")
    wid = WorldStage().run(WorldConfig("cylinder", (12, 12), "flat"), store)
    tid = ProcessStage().run_transition(wid, TransitionConfig(p_stay=0.2), store)
    cfg = EmissionConfig("overlap", 36, 1.25, "grid")
    eids = [ProcessStage().run_emission(wid, cfg, SeedTree(s), store) for s in SEEDS]
    names = [f"WorldSpec/{wid}", f"TransitionSpec/{tid}"] + [f"EmissionSpec/{e}" for e in eids]
    for n in names:
        (root / n / "payload.npz").unlink()
    return {"root": root, "names": names, "wid": wid}


def _store(base, dest: Path, unreadable=False) -> dict:
    root = dest / "artifacts"
    shutil.copytree(base["root"], root)
    if unreadable:
        for n in base["names"]:
            (root / n / "payload.npz").write_bytes(b"not an npz archive")
    st = dict(base, root=root, manifest=dest / "INPUT_IDENTITIES.json",
              config=dest / "config.json")
    _seal(st)
    return st


def _seal(st, manifest_edit=None, config_edit=None):
    arts = {}
    for n in st["names"]:
        meta = json.loads((st["root"] / n / "meta.json").read_text(encoding="utf-8"))
        arts[n] = {"sha256": meta["payload_sha256"], "meta_sha256": _sha(st["root"] / n /
                                                                         "meta.json")}
    if manifest_edit:
        manifest_edit(arts)
    st["manifest"].write_text(json.dumps({"artifact_root": str(st["root"]), "artifacts": arts},
                                         indent=1, sort_keys=True), encoding="utf-8")
    cfg = {"inputs_sha256": {"INPUT_IDENTITIES.json": _sha(st["manifest"])}}
    if config_edit:
        config_edit(cfg)
    st["config"].write_text(json.dumps(cfg, indent=1, sort_keys=True), encoding="utf-8")


def _edit(st, index, filename, fn):
    p = st["root"] / st["names"][index] / filename
    obj = json.loads(p.read_text(encoding="utf-8"))
    fn(obj)
    data = json.dumps(obj, sort_keys=True, indent=1) if filename == "meta.json" \
        else canonical_json(obj)
    p.write_bytes(data.encode("utf-8"))
    _seal(st)


def _set(*path_and_value):
    *path, value = path_and_value

    def fn(obj):
        for k in path[:-1]:
            obj = obj[k]
        obj[path[-1]] = value
    return fn


def _run(st):
    return he.kc1_identity(st["root"], st["manifest"], st["config"], seeds=SEEDS)


TAMPERS = {
    "extra_field": lambda st: _edit(st, 2, "extra.json", _set("sigma", 1.5)),
    "config_field": lambda st: _edit(st, 2, "meta.json", _set("config", "sigma", 1.5)),
    "replicate": lambda st: _edit(st, 2, "meta.json", _set("config", "replicate", 2718)),
    "world_scope_master": lambda st: _edit(st, 3, "meta.json",
                                           _set("config", "world_scope_master", 1)),
    "world_scope_seed": lambda st: _edit(st, 4, "meta.json", _set(
        "seed_map", "world_scope/centers/cylinder", 4772093464253776385)),
    "world_seed_map": lambda st: _edit(st, 0, "meta.json", _set("seed_map", {"x": 1})),
    "transition_parents": lambda st: _edit(st, 1, "meta.json", _set("parent_ids", [])),
    "emission_parents": lambda st: _edit(st, 2, "meta.json",
                                         _set("parent_ids", ["0000000000000000"])),
    "status": lambda st: _edit(st, 0, "meta.json", _set("status", "incomplete")),
    "artifact_type": lambda st: _edit(st, 3, "meta.json", _set("artifact_type",
                                                                 "TransitionSpec")),
    "artifact_id": lambda st: _edit(st, 4, "meta.json", _set("artifact_id", "0" * 16)),
    "meta_file_checksum": lambda st: _seal(
        st, manifest_edit=lambda a: a[st["names"][0]].__setitem__("meta_sha256", "0" * 64)),
    "manifest_checksum": lambda st: _seal(
        st, manifest_edit=lambda a: a[st["names"][1]].__setitem__("sha256", "0" * 64)),
    "config_manifest_hash": lambda st: _seal(
        st, config_edit=lambda c: c["inputs_sha256"].__setitem__("INPUT_IDENTITIES.json",
                                                                 "0" * 64)),
}


# ------------------------------------------------------------------------- KC1 tests

def test_synthetic_store_reproduces_the_contract_identities(base):
    want = CONTRACT["s0"]["KC1"]["artifacts"]
    assert set(base["names"]) == set(want)


def test_expected_envelope_reproduces_process_stage(base):
    want = CONTRACT["s0"]["KC1"]["artifacts"]
    for n in base["names"]:
        kind, aid = n.split("/")
        meta = json.loads((base["root"] / n / "meta.json").read_text(encoding="utf-8"))
        if kind == "EmissionSpec":
            env = he.expected_envelope(kind, seed=meta["config"]["replicate"],
                                       world_id=base["wid"])
        elif kind == "TransitionSpec":
            env = he.expected_envelope(kind, world_id=base["wid"])
        else:
            env = he.expected_envelope(kind)
        assert canonical_json(env["config"]) == canonical_json(meta["config"]) \
            == canonical_json(want[n]["config"]), n
        assert list(env["parent_ids"]) == meta["parent_ids"] == want[n]["parent_ids"], n
        assert canonical_json(env["seed_map"]) == canonical_json(meta["seed_map"]) \
            == canonical_json(want[n]["seed_map"]), n
        assert make_artifact_id(kind, env["config"], list(env["parent_ids"])) == aid


@pytest.mark.parametrize("unreadable", [False, True])
def test_identity_passes_without_touching_any_payload(base, tmp_path, monkeypatch, unreadable):
    st = _store(base, tmp_path, unreadable=unreadable)
    if isinstance(he.JSON_READS, list):
        he.JSON_READS.clear()
    touched = []
    _guard(monkeypatch, touched, lambda p: any(f in p for f in FORBIDDEN))
    res = _run(st)
    monkeypatch.undo()
    assert touched == []
    assert res["status"] == "PASS"
    assert set(base["names"]) <= set(res["artifacts"])
    for n in base["names"]:
        assert all(bool(v) for v in res["artifacts"][n]["checks"].values()), n
    reads = [str(p) for p in he.JSON_READS]
    assert reads and all(p.endswith(".json") for p in reads)
    names = {Path(p).name for p in reads}
    assert {"meta.json", "extra.json", "INPUT_IDENTITIES.json", "config.json"} <= names
    assert names <= {"meta.json", "extra.json", "INPUT_IDENTITIES.json", "config.json"}
    assert all(str(p).endswith(".json") for p in res["json_reads"])


@pytest.mark.parametrize("name", sorted(TAMPERS))
def test_each_tamper_fails(base, tmp_path, monkeypatch, name):
    st = _store(base, tmp_path)
    TAMPERS[name](st)
    touched = []
    _guard(monkeypatch, touched, lambda p: any(f in p for f in FORBIDDEN))
    status = _status(he.kc1_identity, st["root"], st["manifest"], st["config"], seeds=SEEDS)
    monkeypatch.undo()
    assert status == FAIL, name
    assert touched == []


def test_read_json_refuses_other_files(tmp_path, monkeypatch):
    npz = tmp_path / "payload.npz"
    npz.write_bytes(b"PK\x03\x04 synthetic")
    txt = tmp_path / "notes.txt"
    txt.write_text("{}", encoding="utf-8")
    good = tmp_path / "x.json"
    good.write_text('{"a": 1}', encoding="utf-8")
    touched = []
    _guard(monkeypatch, touched, lambda p: p.endswith(("payload.npz", "notes.txt")))
    for p in (npz, txt):
        with pytest.raises(hw.HwsStop) as info:
            he.read_json(p)
        assert info.value.status == FAIL
    assert he.read_json(good) == {"a": 1}
    monkeypatch.undo()
    assert touched == []
    assert str(good) in [str(p) for p in he.JSON_READS]


# --------------------------------------------------------------- G0 seed-scope search

PLANT = {
    "tools/hws/notes.md": "uses hws-v1\n",
    "other/readme.txt": "seed 620101 here\n",
    ".git/config": "hws-v1\n",
    ".venv/lib/x.py": "620103\n",
    "__pycache__/m.txt": "hws-v1\n",
    "00_READ_ME_FIRST_Research_Summary_So_Far/s.md": "hws-v1\n",
    "docs/research_summary/s.md": "620101\n",
    "wt/docs/research_summary/sec.md": "620103\n",
    "wt/00_READ_ME_FIRST_copy/t.txt": "hws-v1\n",
    "data/blob.npz": "hws-v1",
}
SKIPPED = (".git/", ".venv/", "__pycache__/", "00_READ_ME_FIRST", "docs/research_summary/",
           ".npz")


def test_seed_search_skips_and_never_opens_excluded_paths(tmp_path, monkeypatch):
    root = tmp_path / "root"
    for rel, text in PLANT.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    touched = []
    _guard(monkeypatch, touched, lambda p: any(s in p for s in SKIPPED))
    hits = hd.seed_search(root, CONTRACT["seeds"]["g0_needles"])
    monkeypatch.undo()
    assert touched == []
    paths = {str(h["path"]).replace("\\", "/") for h in hits}
    assert any(p.endswith("tools/hws/notes.md") for p in paths)
    assert any(p.endswith("other/readme.txt") for p in paths)
    assert not any(s in p for p in paths for s in SKIPPED)
    assert {h["needle"] for h in hits} <= set(CONTRACT["seeds"]["g0_needles"])


P = "X:/Downloads/projects/topo-pilot"
DECLARED = [f"{P}/topo-pilot-hws/tools/hws/API.md", f"{P}/topo-pilot/tests/hws/test_b_kc1.py",
            f"{P}/agent-handoff/jobs/0119/task.md", f"{P}/hws-store/STAGES.jsonl",
            "X:/Downloads/topo-scratch/hws-dry/GATES.jsonl",
            "X:\\Downloads\\projects\\topo-pilot\\agent-handoff\\jobs\\0118\\review.md",
            # ruling R-0118-5 extensions
            f"{P}/coord-scratch/notes.md", f"{P}/topo-pilot/docs/code_index/FILES.md",
            f"{P}/topo-pilot-c2nd/tools/c2_nd/reg.py", f"{P}/topo-pilot-c2nd/tests/c2_nd/t.py",
            f"{P}/topo-pilot-x6zc/tools/x6zc/reg.py", f"{P}/topo-pilot-x6zc/tests/x6zc/t.py"]
OUTSIDE = [f"{P}/c2nd-store/x.json", f"{P}/x6zc-store/y.json", f"{P}/topo-pilot/tools/k4b/n.md"]


def _hits(paths):
    return [{"path": p, "needle": "hws-v1", "line": 1} for p in paths]


# API-AMBIGUITY: API §6.2 does not name the result keys of classify_seed_hits; "status" assumed.
# R-0118-5's "topo-scratch/<job>/ folders of HWS jobs listed in CONTRACT" is not tested:
# CONTRACT lists no such job folders.
def test_classify_seed_hits_declarations_pass():
    assert hd.classify_seed_hits(_hits(DECLARED))["status"] == "PASS"
    assert hd.classify_seed_hits([])["status"] == "PASS"


@pytest.mark.parametrize("outside", OUTSIDE)
def test_classify_seed_hits_fails_closed_outside(outside):
    res = hd.classify_seed_hits(_hits(DECLARED + [outside]))
    assert res["status"] == "FAIL_TECHNICAL/SEED_SCOPE"
    text = json.dumps(res, default=str)
    assert outside in text and DECLARED[0] in text  # every hit is listed


# ------------------------------------------------- D-0127-1 regression (job 0128, author B)
# Review 0127: a seed "appears" only as a whole token. A digit-only needle hits only when not
# preceded or followed by [0-9A-Za-z_]; the scope needle "hws-v1" keeps substring matching.
# The no-hit texts are the 0127 false hits (fraction, hex digest, float mantissa, count).

TOKEN_NO_HIT = {
    "c1prime-store/CERT_val.json": '{"value": "66201016285"}\n',
    "c1prime-store/registry/registry_v1.json": '{"sha256": "f6201019b8"}\n',
    "artifacts/ProcessDiagnostics/a/extra.json": '{"mi": 6.662010328e-50}\n',
    "x6-store/tables/class_tables_NA.json": '{"count": 254342562010128}\n',
}
TOKEN_HIT = {
    "old/seed_map.json": ('{"seed": 620101}\n', "620101"),
    "old/list.json": ("[620101]\n", "620101"),
    "old/manifest.txt": ("bootstrap seeds 620103, 7\n", "620103"),
    "old/record.json": ('{"s": "620101"}\n', "620101"),
    "old/scope.md": ("xhws-v1y\n", "hws-v1"),
}


def test_d0127_1_numeric_needles_match_whole_tokens(tmp_path):
    root = tmp_path / "tree"
    plant = dict(TOKEN_NO_HIT, **{rel: text for rel, (text, _) in TOKEN_HIT.items()})
    for rel, text in plant.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")
    hits = hd.seed_search(root, ["hws-v1", "620101", "620103"])
    found = {rel: set() for rel in plant}
    for h in hits:
        p = str(h["path"]).replace("\\", "/")
        owners = [rel for rel in plant if p == rel or p.endswith("/" + rel)]
        assert len(owners) == 1, p
        found[owners[0]].add(h["needle"])
    bad = [(rel, found[rel]) for rel in TOKEN_NO_HIT if found[rel]]
    bad += [(rel, found[rel]) for rel, (_, nd) in TOKEN_HIT.items() if found[rel] != {nd}]
    assert bad == []
