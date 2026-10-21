"""Author B (job 0101): T-G0 (RC-16) and T-LINEAGE (C2-FROZEN-v1 §13.3, §4, §7 row 1, §11,
§13.1; API.md §3.1, §12.3, §12.5, §12.6, §16.2; CONTRACT.json hashes).

Written from the protocol, API.md and CONTRACT.json only; tools/c2_readout/*.py never read.
Refusal fixtures use synthetic stores and worktrees under pytest's tmp_path with the c2_config
path constants redirected there. The hash-binding tests read the repository's own pinned files
(code and documents), never a store payload.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "c2_readout"))

import c2_config as cc  # noqa: E402  (first: the sys.path convention)
import c2_data as cd  # noqa: E402
import c2_driver as cdr  # noqa: E402
import c2_registry as cg  # noqa: E402
import stage_records  # noqa: E402

PROTO = "4d97d8e258cfab906ccfe1d99564d4dd74202edd96dd63eb836abd64c277a3d8"
AUTH_SHA = "5a8430f36eb1432030c3ca8c2b3fa3a152193a4d3d80931a73015c413b3fe786"
STATE_SHA = {"1729": "062d0a0aa71c41ad5afd9d3f76e58cf38a81419d629defcf2e3ac6316ffaf8f8",
             "2718": "501d9c9ad80d4ffe272d7e03003cdee24b7fe3b25bed40e044f2111afd69aa5c",
             "3141": "197cccd6cf5491143171fe8ccd6ce79f71cb2f16995aa99af4e9dffe4bec94c8"}  # §4
CHARTS = {"1729": "6154af0ee1a5ad01d378b507272365d1f0e797b4a843835d7dc09525d5c9cc71",
          "2718": "6a5d8c1cbe4aea9909b85aff258a31d2dfdfb8d12c1f93f33a79b245d69370da",
          "3141": "ce0c0192d243ff9e8fa4ddc6b07750db31a637ff059a4e8cc55535b8dd21cf2d"}  # §2.4
BLOBS = {  # protocol §13.1 (three K4 kernel files are given there as prefix…suffix)
    "src/topo_pilot/learner/model.py":
        "ee1c124ce83da147ccc2a4b4c0be167de902d61ecd00ead5748b8566f62ae039",
    "src/topo_pilot/learner/patch.py":
        "64d742e85ddba3d121a5c72af0abaef910c9b986a03a7b87caa26c4c20dd0ad4",
    "tools/c1prime/c1_oracle.py":
        "077ea1489262d15075624fd6116900c74a6e5b0eb2fe02e5d4f6127cbc0323b3",
    "tools/c1prime/c1_chart.py": "45b6aa0d8c8db28ce291eca320b1f322baddc9c70cee6588843f10935f4418df",
    "tools/c1prime/c1_fit.py": "13962c7a46541b9abbd53b2e9e69d6ce7c2f58de042499ba6f48c062228edf61",
    "tools/c1prime/c1_gates.py": "017499e0c434321ceae95c78ad584c15e93e82efd0ce768137f452d5668db485",
    "tools/c1prime/c1_endpoint.py":
        "bdb283efbed04119cf23a5875835d08e1c21b4935d5f9cff334e3e88525d6e46",
    "tools/c1prime/c1_means.py": "e0630816942224933d3380897eb90b374522ca0ac4c4c8f3f6b62edcead2d00c",
    "tools/c1prime/c1_model.py": "37665037dd4d6b29a45b5981016c3a965d98f9ee47d474e21c74c616f2324d0a",
    "tools/c1prime/c1_data.py": "262418b2f0272e8425a038c53bb120c8f40402a4100b8a71e257f71b560106e9",
    "tools/c1prime/c1_records.py":
        "d0299ff4621c699a9439184b72e125a2dea34f304e50772c0c190fb9f628fdb5",
    "tools/c1prime/c1_config.py":
        "8e170b5144b732527d41aeeb2ab71e41da2bfcd5b33b2d580527711b3ea6e207",
    "tools/c1prime/CONTRACT.json":
        "f8df2e43bc24a3e992ce4323a8577ec4a7e2657a4e00bdf3ff0323b909a7a379",
    "tools/x4_circle_history/chart.py": ("938821a0", "9ccb"),
    "tools/x4_circle_history/cochain.py": ("e53f6725", "3075"),
    "tools/x4_circle_history/errors.py": ("8aa309c4", "f99f"),
    "tools/x4_circle_history/precision.py":
        "5ae1e632eee0ac5767a9b536c6f7aebbc2d7328a9a664db828f37afc643329c8",
    "tools/x4_circle_history/scores.py":
        "8cf9a5f810ad41a412379bfe2786e9ce7fafe4efbd31122ea66a7d7c70f989a6",
    "tools/c1prime_registry/c1_registry_sources.py":
        "4f40840d8eb88d515556aeb7058640761d4b44a7a6ee8045fb3bce9987a5a253",
    "src/topo_pilot/analysis/x4f_scores.py":
        "03e2d736a734cf8d45d158112d1955b4faba267b235777064814dee3bafc563b"}
PATHS = {"PROJECT_ROOT": "", "STORE": "c2-readout-store", "WORKTREE": "topo-pilot-c2",
         "MAILBOX": "agent-handoff", "ARTIFACT_ROOT": "topo-pilot/artifacts",
         "C1P_STORE": "c1prime-store", "X6S1_STORE": "x6-stage1-store",
         "K4_FREEZE": "x4-circle-history-feas-store-0015/FREEZE.json"}


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else json.dumps(data).encode())
    return _sha(path)


def _isolate(monkeypatch, root):
    for name, rel in PATHS.items():
        for mod in (cc, cd, cg, cdr):
            monkeypatch.setattr(mod, name, root / rel, raising=False)
        key = name.lower().replace("c1p_", "c1prime_")
        monkeypatch.setitem(cc.CONTRACT["paths"], key, str(root / rel))
    return root


def _ctx(store, worktree=REPO, job="0199", task="a" * 64):
    return cdr.Ctx(store=store, worktree=worktree, head="1" * 40, job=job, task_sha256=task,
                   session="synthetic", release=None, policy=None, data={})


# ---- T-G0: the frozen bindings ----
def test_protocol_and_authority_bindings():
    assert _sha(REPO / "tools" / "c2_readout" / "PROTOCOL_C2_v1.md") == PROTO
    assert cc.PROTOCOL_SHA256 == PROTO == cc.CONTRACT["protocol"]["sha256"]
    assert cc.PROTOCOL_ID == "C2-FROZEN-v1" and cc.AUTH_SHA256 == AUTH_SHA
    assert cc.ADDENDUM1_SHA256 == (
        "2db09007a1ff9f9706ffe323c0c1d2c49197648473c481c1776a46ae884011a8")
    assert cc.R_COMMIT == "d44548b073523d402cc31fbfc5440c0d6df37a23" == cc.CONTRACT["protocol"]["R"]


def test_state_sha_chart_and_freeze_hashes_equal_the_contract():
    h = cc.CONTRACT["hashes"]
    assert h["state_sha_f32"] == STATE_SHA  # the three full 64-hex strings of §4
    for j, sha in STATE_SHA.items():
        assert cc.CONTRACT["models"][j]["state_sha_f32"] == sha and len(sha) == 64
    assert h["charts"] == {f"c1prime-store/CHART_{j}_production.npz": s for j, s in CHARTS.items()}
    assert h["k4_freeze"] == "e3049feedf0fadfb004c9422effe560af031addb846a7b8d1c1bffd52ce3c94a"
    assert h["c1prime_contract"] == BLOBS["tools/c1prime/CONTRACT.json"]
    assert cc.CONTRACT["chart"]["contract_sha256"] == BLOBS["tools/c1prime/CONTRACT.json"]


def test_reused_blob_hashes_equal_section_13_1_and_the_files():
    blobs = cc.CONTRACT["hashes"]["reused_blobs"]
    assert set(blobs) == set(BLOBS)
    for path, want in BLOBS.items():
        if isinstance(want, tuple):
            assert blobs[path].startswith(want[0]) and blobs[path].endswith(want[1]), path
        else:
            assert blobs[path] == want, path
    extra = cc.CONTRACT["hashes"]["reused_extra"]
    assert not set(extra) & set(blobs)
    for path, sha in {**blobs, **extra}.items():  # working files at H (core.autocrlf false)
        assert _sha(REPO / path) == sha, path


def test_load_contract_refuses_a_protocol_mismatch(tmp_path):
    raw = json.loads((REPO / "tools" / "c2_readout" / "CONTRACT.json").read_text("utf-8"))
    good = tmp_path / "good.json"
    good.write_text(json.dumps(raw), encoding="utf-8")
    assert cc.load_contract(good)["protocol"]["sha256"] == PROTO
    raw["protocol"]["sha256"] = "0" * 64
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ValueError):
        cc.load_contract(bad)


def _g0_env(tmp_path, monkeypatch, alter):
    root = _isolate(monkeypatch, tmp_path / "proj")
    wt = root / "topo-pilot-c2"
    for name in ("PROTOCOL_C2_v1.md", "CONTRACT.json"):
        _write(wt / "tools" / "c2_readout" / name,
               (REPO / "tools" / "c2_readout" / name).read_bytes())
    proto = (REPO / "tools" / "c2_readout" / "PROTOCOL_C2_v1.md").read_bytes()
    mail = proto[:-1] + bytes([proto[-1] ^ 1]) if alter else proto
    _write(root / "agent-handoff" / "planning" / "responses" / "C2-FROZEN-v1.md", mail)
    task = _write(root / "agent-handoff" / "jobs" / "0199" / "task.md", b"synthetic task")
    (root / "c2-readout-store").mkdir()
    return _ctx(root / "c2-readout-store", worktree=wt, task=task)


def test_g0_refuses_a_protocol_copy_mismatch(tmp_path, monkeypatch):
    ctx = _g0_env(tmp_path, monkeypatch, alter=True)
    try:
        res = cdr.g0(ctx)
    except Exception:  # noqa: BLE001  a raised refusal is a refusal
        return
    assert res["status"] != "PASS" and str(res["status"]).startswith("FAIL_TECHNICAL")
    assert res["i"]["status"] != "PASS"
    assert set("i ii iii iv v vi vii viii".split()) <= set(res)


def test_g0_item_i_accepts_the_exact_copy(tmp_path, monkeypatch):
    ctx = _g0_env(tmp_path, monkeypatch, alter=False)
    res = cdr.g0(ctx)  # API.md 12.3: g0 returns the item dict (fail-closed elsewhere)
    assert res["i"]["status"] == "PASS"
    assert res["status"] != "PASS"  # synthetic: no K4 FREEZE, charts or release exist


# ---- T-G0: AUTH-ADMIT and the release binding ----
def _auth(**over):
    rec = {"schema": "c2-auth-v1", "protocol_sha256": PROTO,
           "owner_record": {"path": cc.AUTH_PATH, "sha256": AUTH_SHA,
                            "owner_verbatim": "synthetic owner text",
                            "granted_utc": "2026-10-21T00:00:00Z"},
           "budget": {"central_cpu_h": 2.1, "range_cpu_h": [0.9, 4.8],
                      "cpu_policy": "measure-only, --max-cpu inf"},
           "coordinator": "synthetic", "written_utc": "2026-10-21T00:00:00Z"}
    for k, v in over.items():
        if k.startswith("owner_"):
            rec["owner_record"][k[6:]] = v
        else:
            rec[k] = v
    return rec


@pytest.mark.parametrize("over, ok", [
    ({}, True), ({"protocol_sha256": PROTO.upper()}, True), ({"schema": "c2-auth-v0"}, False),
    ({"protocol_sha256": "0" * 64}, False), ({"owner_sha256": "0" * 64}, False),
    ({"owner_owner_verbatim": ""}, False), ({"coordinator": ""}, False)])
def test_auth_ok(tmp_path, over, ok):
    _write(tmp_path / "AUTH.json", _auth(**over))
    assert bool(cdr.auth_ok(tmp_path)) is ok


def test_auth_ok_missing_or_unparsable_never_raises(tmp_path):
    assert not cdr.auth_ok(tmp_path)
    (tmp_path / "AUTH.json").write_bytes(b"{not json")
    assert not cdr.auth_ok(tmp_path)


def _released(ctx, stage):
    # API-AMBIGUITY: API.md 12.6 release_ok returns "dict" without naming its verdict key; a
    # pass is read as {"ok": True} or {"status": "PASS"}, a refusal also as a raised error.
    try:
        res = cdr.release_ok(ctx, stage)
    except Exception:  # noqa: BLE001
        return False
    if isinstance(res, dict):
        return res.get("ok") is True or res.get("status") == "PASS"
    return bool(res)


def _release(store, ctx, k, **over):
    rec = {"schema": "c2-release-v1", "release": f"R{k}", "stages": [f"S{k}"], "job": ctx.job,
           "task_sha256": ctx.task_sha256, "head": ctx.head, "protocol_sha256": PROTO,
           "freeze_sha256": _sha(store / "FREEZE.json"), "N_test": None, "k": None,
           "accept_review_sha256": None, "coordinator": "synthetic", "utc": "x"}
    rec.update(over)
    _write(store / f"RELEASE_R{k}.json", rec)


@pytest.mark.parametrize("over", [{"job": "0198"}, {"task_sha256": "b" * 64},
                                  {"head": "2" * 40}, {"protocol_sha256": "0" * 64},
                                  {"freeze_sha256": "0" * 64}, {"stages": ["S2"]},
                                  {"schema": "c2-release-v0"}])
def test_release_binding_refusals(tmp_path, over):
    _write(tmp_path / "FREEZE.json", {"schema": "c2-freeze-v1", "protocol_sha256": PROTO})
    ctx = _ctx(tmp_path)
    _release(tmp_path, ctx, 1)
    assert _released(ctx, "S1")
    (tmp_path / "RELEASE_R1.json").unlink()
    _release(tmp_path, ctx, 1, **over)
    assert not _released(ctx, "S1")


def test_release_r5_must_carry_n_test_and_k(tmp_path):
    _write(tmp_path / "FREEZE.json", {"schema": "c2-freeze-v1", "protocol_sha256": PROTO})
    ctx = _ctx(tmp_path)
    _release(tmp_path, ctx, 5)  # N_test, k and accept_review_sha256 null
    assert not _released(ctx, "S5")
    assert not _released(ctx, "S2")  # no RELEASE_R2.json


# ---- T-LINEAGE ----
def _store(tmp_path):
    store = tmp_path / "store"
    _write(store / "GATES.jsonl", b'{"gate": "G0"}\n')
    _write(store / "STAGES.jsonl", b'{"event": "STARTED", "stage": "S1"}\n')
    _write(store / "hist" / "HIST_fit_b0.npz", b"synthetic table bytes")
    _write(store / "stages" / "S1" / "record.json", {"stage": "S1"})
    return store


def test_write_manifest_exclusive_and_hashes(tmp_path):
    store = _store(tmp_path)
    ctx = _ctx(store)
    path = Path(cdr.write_manifest(ctx, "S1"))
    assert path == store / "manifests" / "0199.json"
    man = json.loads(path.read_text(encoding="utf-8"))
    assert man["schema"] == "c2-manifest-v1" and man["job"] == "0199" and man["stage"] == "S1"
    assert man["head"] == ctx.head
    assert man["append_only"] == {"GATES.jsonl": _sha(store / "GATES.jsonl"),
                                  "STAGES.jsonl": _sha(store / "STAGES.jsonl")}
    for rel, sha in man["files"].items():
        assert _sha(store / rel) == sha, rel
    with pytest.raises(FileExistsError):
        cdr.write_manifest(ctx, "S1")
    with pytest.raises(FileExistsError):
        stage_records.write_new(path, {"again": True})


def test_supersede_moves_append_only_and_records(tmp_path):
    store = _store(tmp_path)
    rels = ["hist/HIST_fit_b0.npz", "stages/S1/record.json"]
    before = {r: (store / r).read_bytes() for r in rels}
    rul = tmp_path / "ruling.md"
    rsha = _write(rul, b"synthetic ruling")
    # API-AMBIGUITY: API.md 12.5 does not fix the form of `ruling`; a dict carrying the
    # SUPERSEDED.json fields (defect, ruling path and sha256) is passed.
    cdr.supersede(_ctx(store), "0199", 1, rels, {"defect": "D1 (synthetic)", "path": str(rul),
                                                 "ruling_path": str(rul), "sha256": rsha,
                                                 "ruling_sha256": rsha})
    dest = store / "superseded" / "0199-a1"
    for r in rels:
        assert not (store / r).exists() and (dest / r).read_bytes() == before[r]
    sums = (dest / "SHA256SUMS").read_text(encoding="utf-8").replace("\\", "/").splitlines()
    for r in rels:
        want = hashlib.sha256(before[r]).hexdigest()
        assert any(x.startswith(want + "  ") and x.endswith(r) for x in sums), r
    rec = json.loads((dest / "SUPERSEDED.json").read_text(encoding="utf-8"))
    assert {"job", "attempt", "defect", "ruling_path", "ruling_sha256", "moved"} <= set(rec)
    assert rec["job"] == "0199" and int(rec["attempt"]) == 1
    moved = sorted(str(m).replace("\\", "/") for m in rec["moved"])
    assert rec["ruling_sha256"] == rsha and moved == sorted(rels)
    assert (store / "GATES.jsonl").exists()  # nothing else touched, nothing deleted


def test_regen_compare_bit_identical(tmp_path):
    store = _store(tmp_path)
    ctx, path = _ctx(store), store / "hist" / "HIST_fit_b0.npz"
    assert bool(cdr.regen_compare(ctx, path, _sha(path))) is True
    np.save(store / "x.npy", np.arange(3))
    try:
        same = cdr.regen_compare(ctx, store / "x.npy", "0" * 64)
    except Exception:  # noqa: BLE001  FAIL_TECHNICAL/LINEAGE may be raised
        return
    assert not same
