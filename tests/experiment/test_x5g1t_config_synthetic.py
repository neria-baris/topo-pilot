"""Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
(docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
Split mechanically from test_x5g1t_config_checks.py (job 0011); tests unchanged.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import importlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from topo_pilot.contracts import ArtifactStore, Checkpoint, LocalFSBackend, TransitionSpec
from topo_pilot.contracts.testing import tiny_world_spec
from topo_pilot.experiment import x5g1t_lineage, x5g1t_train
from topo_pilot.experiment.x5g1t_fixture import E0, T0, _emission
from topo_pilot.learner import ModelConfig, TrainConfig


# ---- lazy module access (x5g1t_config may land after these tests) ------------------------------
def _cm():
    return importlib.import_module("topo_pilot.experiment.x5g1t_config")
MODEL = dataclasses.asdict(ModelConfig(vocab_in=4, vocab_out=3, n_layers=1, d_model=8, n_heads=2,
                                       d_mlp=16))
PRODUCER = "prod-sources-v1"


def _rt(obj):
    return json.loads(json.dumps(obj))


def _flip(h: str) -> str:
    return h[:-1] + ("0" if h[-1] != "0" else "1")


def _sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _snapshot(root: Path) -> dict:
    out = {}
    for p in sorted(Path(root).rglob("*")):
        rel = p.relative_to(root).as_posix()
        out[rel] = _sha_file(p) if p.is_file() else "<dir>"
    return out


def _put(d: dict, path: tuple, value) -> None:
    for k in path[:-1]:
        d = d[k]
    d[path[-1]] = value


# ---- tiny source stores --------------------------------------------------------------------------
def _save_sources(root: Path, tag: str, producer: str):
    st = ArtifactStore(LocalFSBackend(root), producer_version=producer)
    pi = np.full(4, 0.25)
    T1 = 0.4 * np.eye(4) + 0.6 * T0
    perm = np.array([2, 0, 1], dtype=np.int64)
    kw = dict(parents=[], seed_map={}, consumer="experiment")
    ids = {"world": st.save(tiny_world_spec(), config={tag: "world"}, **kw),
           "a0": st.save(TransitionSpec(T=T0, pi=pi), config={tag: "a0"}, **kw),
           "a020": st.save(TransitionSpec(T=T1, pi=pi), config={tag: "a020"}, **kw),
           "E": st.save(_emission(E0, pi, perm), config={tag: "E"}, **kw)}
    return st, ids


def _sources(st: ArtifactStore, ids: dict) -> dict:
    def pair(k):
        return [ids[k], st.meta(ids[k]).payload_sha256]
    return {"world": pair("world"), "T": {"a0": pair("a0"), "a020": pair("a020")},
            "E": pair("E")}


def _save_stored_ckpt(st: ArtifactStore, model: dict, train: dict, tag: str = "e3") -> str:
    ck = Checkpoint(run_id="e3-run", step=5000, observation_id="e3obs", state=b"stored-weights",
                    model_config=model, train_config=train)
    return st.save(ck, config={"tag": tag, "model_config": model, "train_config": train},
                   parents=[], seed_map={}, consumer="experiment")


def _cfg_from_spec(spec, mode: str = "production") -> dict:
    return {"mode": mode, "protocol": spec.protocol, "protocol_doc": spec.protocol_doc,
            "protocol_doc_sha256": spec.protocol_doc_sha256, "read_roots": list(spec.read_roots),
            "study_root": spec.study_root, "ledger_path": spec.ledger_path,
            "mailbox": spec.mailbox, "sources": _rt(spec.sources),
            "source_producers": dict(spec.source_producers),
            "stored_checkpoint": list(spec.stored_checkpoint), "masters": list(spec.masters),
            "sizes": dict(spec.sizes), "model_config": dict(spec.stored_model_config),
            "steps": spec.steps, "grid": [int(t) for t in spec.grid], "gc": dict(spec.gc),
            "threads": spec.threads, "bootstrap_draws": spec.bootstrap_draws,
            "cap_s": float(spec.cap_s), "cumulative_cap_s": float(spec.cumulative_cap_s),
            "check_stored_ids": spec.check_stored_ids, "env": dict(spec.env)}


@pytest.fixture
def spies(monkeypatch):
    calls: list = []

    def spy(name):
        def f(*a, **k):
            calls.append(name)
            raise AssertionError(f"{name} called during config validation")
        return f

    monkeypatch.setattr(x5g1t_lineage, "draw_pair", spy("draw_pair"))
    monkeypatch.setattr(x5g1t_train, "train_one", spy("train_one"))
    monkeypatch.setattr(x5g1t_train, "Trainer", spy("Trainer"))
    return calls


@pytest.fixture
def prod(tmp_path, monkeypatch, spies):
    """A synthetic stand-in for PRODUCTION: dataclasses.replace(PRODUCTION, ...) pointed at three
    temporary read stores, a temporary repo with a protocol document and a fresh study root."""
    C = _cm()
    for k, v in C.PRODUCTION.env.items():
        monkeypatch.setenv(k, v)
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    doc = repo / "docs" / "PROTO.md"
    doc.write_bytes(b"# x5g1-train-v4 test protocol document\n")
    reads = [tmp_path / "main" / "artifacts", tmp_path / "x5g1" / "store",
             tmp_path / "x4b2" / "store"]
    stored_train = _rt(dataclasses.asdict(TrainConfig()))  # E3 dict: list grid, device "auto"
    stores = []
    for r in reads:  # identical copies in every read root: ids are content/config addressed
        st, ids = _save_sources(r, "role", PRODUCER)
        cid = _save_stored_ckpt(st, MODEL, stored_train)
        stores.append(st)
    assert isinstance(stores[0].meta(cid).config["train_config"]["checkpoint_steps"], list)
    mailbox = tmp_path / "mailbox"
    mailbox.mkdir()
    sources = _sources(stores[0], ids)
    spec = dataclasses.replace(
        C.PRODUCTION, protocol_doc="docs/PROTO.md", protocol_doc_sha256=_sha_file(doc),
        read_roots=tuple(str(r) for r in reads), study_root=str(tmp_path / "study"),
        ledger_path=str(tmp_path / "x5g1" / "cpu_ledger.json"), mailbox=str(mailbox),
        sources=sources, source_producers={i: PRODUCER for i in ids.values()},
        stored_checkpoint=(cid, stores[0].meta(cid).payload_sha256),
        stored_model_config=dict(MODEL), stored_train_config=stored_train)
    cfgdir = tmp_path / "cfgs"
    cfgdir.mkdir()
    return SimpleNamespace(C=C, spec=spec, cfgd=_cfg_from_spec(spec), repo=repo, doc=doc,
                           reads=reads, stores=stores, ids=ids, cid=cid, tmp=tmp_path,
                           cfgdir=cfgdir, calls=spies, stored_train=stored_train)


def _write(env, d: dict, name: str = "cfg.json") -> Path:
    p = env.cfgdir / name
    p.write_text(json.dumps(d, indent=1), encoding="utf-8")
    return p


def _load(env, d: dict, name: str = "cfg.json"):
    return env.C.load_config(_write(env, d, name))


def _assert_accepts(env, d: dict, spec=None) -> dict:
    cfg = _load(env, d)
    before = _snapshot(env.tmp)
    report = env.C.validate_config(cfg, env.repo, spec=spec or env.spec)
    assert _snapshot(env.tmp) == before, "validate_config must be read-only"
    assert isinstance(report, dict)
    assert d["mode"] in json.dumps(report, default=str)
    assert env.calls == []
    return report


def _assert_rejects(env, d: dict, spec=None) -> None:
    """Rejected by load_config or by validate_config with ConfigInvalid; nothing created and no
    sampler/model touched."""
    path = _write(env, d)
    before = _snapshot(env.tmp)
    try:
        cfg = env.C.load_config(path)
    except env.C.ConfigInvalid:
        cfg = None
    if cfg is not None:
        with pytest.raises(env.C.ConfigInvalid):
            env.C.validate_config(cfg, env.repo, spec=spec or env.spec)
    assert _snapshot(env.tmp) == before, "a rejected config must not create or change anything"
    assert env.calls == []


def _mutate_npz(path: Path) -> None:
    with np.load(path, allow_pickle=False) as z:
        arrays = {k: z[k].copy() for k in z.files}
    k = next(k for k, v in arrays.items() if v.dtype.kind == "f" and v.size)
    arrays[k].flat[0] += 1.0
    np.savez(path, **arrays)


# =============================== §3 validate_config: synthetic-fixture ===========================
@pytest.fixture
def syn(prod):
    t = prod.tmp / "syn"
    st, ids = _save_sources(t / "sources", "fixture", "syn-producer")
    (t / "mailbox").mkdir(parents=True)
    d = {"mode": "synthetic-fixture", "protocol": "x5g1-train-v4 SYNTHETIC FIXTURE",
         "protocol_doc": prod.spec.protocol_doc,
         "protocol_doc_sha256": prod.spec.protocol_doc_sha256,
         "read_roots": [str(t / "sources")], "study_root": str(t / "study"),
         "ledger_path": str(t / "ledger.json"), "mailbox": str(t / "mailbox"),
         "sources": _sources(st, ids), "source_producers": {i: "syn-producer" for i in
                                                           ids.values()},
         "stored_checkpoint": None, "masters": [310001, 310002, 310003],
         "sizes": {"train": 64, "dev": 24, "test": 24}, "model_config": dict(MODEL), "steps": 6,
         "grid": list(range(7)), "gc": {"a0": 0.05, "a020": 0.05}, "threads": 1,
         "bootstrap_draws": 40, "cap_s": 21600.0, "cumulative_cap_s": 21600.0,
         "check_stored_ids": True, "env": dict(prod.C.PRODUCTION.env)}
    return SimpleNamespace(**vars(prod), sd=d, sstore=st, sids=ids, sroot=t)


def test_synthetic_correct_config_passes_read_only(syn):
    assert not Path(syn.sd["study_root"]).exists()
    _assert_accepts(syn, syn.sd)
    assert not Path(syn.sd["study_root"]).exists()


SYN_TAMPER = {
    "protocol_without_SYNTHETIC": lambda d, e: _put(d, ("protocol",), "x5g1-train-v4 fixture"),
    "protocol_production": lambda d, e: _put(d, ("protocol",), "x5g1-train-v4"),
    "read_root_is_production_read_root": lambda d, e: d["read_roots"].append(e.spec.read_roots[0]),
    "read_root_inside_production_read_root": lambda d, e: d["read_roots"].append(
        str(Path(e.spec.read_roots[1]) / "sub")),
    "study_root_is_production_study_root": lambda d, e: _put(d, ("study_root",),
                                                             e.spec.study_root),
    "study_root_inside_production_study_root": lambda d, e: _put(
        d, ("study_root",), str(Path(e.spec.study_root) / "fixture")),
    "study_root_inside_production_read_root": lambda d, e: _put(
        d, ("study_root",), str(Path(e.spec.read_roots[0]) / "syn_study")),
    "ledger_is_production_ledger": lambda d, e: _put(d, ("ledger_path",), e.spec.ledger_path),
    "ledger_inside_production_read_root": lambda d, e: _put(
        d, ("ledger_path",), str(Path(e.spec.read_roots[2]) / "ledger.json")),
    "mailbox_is_production_mailbox": lambda d, e: _put(d, ("mailbox",), e.spec.mailbox),
    "grid_not_strictly_increasing": lambda d, e: _put(d, ("grid",), [0, 1, 1, 2, 3, 4, 5, 6]),
    "grid_decreasing": lambda d, e: _put(d, ("grid",), [0, 3, 2, 6]),
    "grid_two_points": lambda d, e: _put(d, ("grid",), [0, 6]),
    "grid_start_not_zero": lambda d, e: _put(d, ("grid",), [1, 2, 4, 6]),
    "grid_end_not_steps": lambda d, e: _put(d, ("grid",), [0, 1, 2, 3, 4, 5]),
    "grid_beyond_steps": lambda d, e: _put(d, ("grid",), [0, 2, 4, 6, 8]),
    "gc_zero": lambda d, e: _put(d, ("gc", "a0"), 0.0),
    "gc_negative": lambda d, e: _put(d, ("gc", "a020"), -0.05),
    "gc_nan": lambda d, e: _put(d, ("gc", "a0"), float("nan")),
    "gc_inf": lambda d, e: _put(d, ("gc", "a020"), float("inf")),
    "masters_empty": lambda d, e: _put(d, ("masters",), []),
    "masters_str": lambda d, e: _put(d, ("masters",), ["a"]),
    "masters_float": lambda d, e: _put(d, ("masters",), [1.5]),
    "threads_zero": lambda d, e: _put(d, ("threads",), 0),
    "sizes_zero": lambda d, e: _put(d, ("sizes", "train"), 0),
    "sizes_negative": lambda d, e: _put(d, ("sizes", "dev"), -1),
    "source_sha": lambda d, e: _put(d, ("sources", "E", 1), _flip(d["sources"]["E"][1])),
    "source_unknown_id": lambda d, e: _put(d, ("sources", "T", "a0", 0), "deadbeefdeadbeef"),
    "mode_other": lambda d, e: _put(d, ("mode",), "synthetic"),
}


@pytest.mark.parametrize("case", sorted(SYN_TAMPER))
def test_synthetic_each_violation_rejected(syn, case):
    d = copy.deepcopy(syn.sd)
    SYN_TAMPER[case](d, syn)
    _assert_rejects(syn, d)


def test_synthetic_production_source_id_rejected(syn):
    """The synthetic store holds the production world content under the production config, so
    the ID and hashes verify; only the production-ID rule can reject."""
    wid = syn.sstore.save(tiny_world_spec(), config={"role": "world"}, parents=[], seed_map={},
                          consumer="experiment")
    assert wid == syn.spec.sources["world"][0]
    d = _rt(syn.sd)
    d["sources"]["world"] = [wid, syn.sstore.meta(wid).payload_sha256]
    d["source_producers"][wid] = "syn-producer"
    _assert_rejects(syn, d)


def test_synthetic_source_payload_mutated_on_disk_rejected(syn):
    _mutate_npz(syn.sroot / "sources" / "WorldSpec" / syn.sids["world"] / "payload.npz")
    _assert_rejects(syn, syn.sd)
