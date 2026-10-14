"""Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
(docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
"""

from __future__ import annotations

import dataclasses
import hashlib
import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from topo_pilot.analysis import X5_GRID
from topo_pilot.contracts import ArtifactStore, Checkpoint, LocalFSBackend, TransitionSpec
from topo_pilot.contracts.testing import tiny_world_spec
from topo_pilot.experiment import x5g1t_lineage, x5g1t_train
from topo_pilot.experiment.x5g1t_fixture import E0, T0, _emission
from topo_pilot.experiment.x5g1t_lineage import CODES, NAMESPACE
from topo_pilot.learner import ModelConfig, TrainConfig


# ---- lazy module access (x5g1t_config may land after these tests) ------------------------------
def _cm():
    return importlib.import_module("topo_pilot.experiment.x5g1t_config")


KEYS = {"mode", "protocol", "protocol_doc", "protocol_doc_sha256", "read_roots", "study_root",
        "ledger_path", "mailbox", "sources", "source_producers", "stored_checkpoint", "masters",
        "sizes", "model_config", "steps", "grid", "gc", "threads", "bootstrap_draws", "cap_s",
        "cumulative_cap_s", "check_stored_ids", "env"}
MODEL = dataclasses.asdict(ModelConfig(vocab_in=4, vocab_out=3, n_layers=1, d_model=8, n_heads=2,
                                       d_mlp=16))
PRODUCER = "prod-sources-v1"


def _rt(obj):
    return json.loads(json.dumps(obj))


def _sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _snapshot(root: Path) -> dict:
    out = {}
    for p in sorted(Path(root).rglob("*")):
        rel = p.relative_to(root).as_posix()
        out[rel] = _sha_file(p) if p.is_file() else "<dir>"
    return out


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


# =============================== §3 PRODUCTION constants =========================================
def test_production_spec_holds_frozen_v4_values():
    C = _cm()
    P = C.PRODUCTION
    assert dataclasses.is_dataclass(P) and isinstance(P, C.ProductionSpec)
    with pytest.raises(dataclasses.FrozenInstanceError):
        P.steps = 1  # type: ignore[misc]
    assert P.protocol == "x5g1-train-v4"
    assert tuple(P.masters) == (310001, 310002, 310003)
    assert dict(P.sizes) == {"train": 131072, "dev": 4096, "test": 4096}
    assert P.steps == 5000
    assert tuple(P.grid) == tuple(int(t) for t in X5_GRID) and len(P.grid) == 27
    assert P.gc == {"a0": 0.27133797235249024, "a020": 0.2939268960103646}
    assert P.bootstrap_draws == 2000 and P.threads == 1
    assert P.cap_s == 21600 and P.cumulative_cap_s == 21600
    assert P.check_stored_ids is True
    assert dict(P.env) == {"OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
                           "OMP_NUM_THREADS": "1"}
    assert P.sources["world"][0] == "21feee1d8ee5422e"
    assert P.sources["world"][1].startswith("b6f0746e") and P.sources["world"][1].endswith("f77f")
    assert P.sources["T"]["a0"][0] == "e4dafc7b9785c172"
    assert P.sources["T"]["a020"][0] == "08a22a03727d2295"
    assert P.sources["E"][0] == "3633ac27dab50cf4"
    for pair in (P.sources["world"], P.sources["T"]["a0"], P.sources["T"]["a020"],
                 P.sources["E"]):
        assert len(pair[1]) == 64
    assert tuple(P.stored_checkpoint) == (
        "c3358e3cb9c352fb", "bcd024efc2ff30f76940d459dba95a693f536fb7cc3b2441c4ee5145dcf8596b")
    assert P.lineage["namespace"] == NAMESPACE
    assert dict(P.lineage["codes"]) == CODES
    assert tuple(P.lineage["stream_tail"]) == ("cylinder", "overlap", "1.25")
    assert len(P.read_roots) == 3
    for r in (*P.read_roots, P.study_root, P.ledger_path, P.mailbox):
        assert Path(r).is_absolute()
    assert len(P.protocol_doc_sha256) == 64


# =============================== §3 StudyConfig / load_config ====================================
def test_load_config_valid_is_frozen_exact_keys_and_root(prod):
    cfg = _load(prod, prod.cfgd)
    assert isinstance(cfg, prod.C.StudyConfig)
    assert {f.name for f in dataclasses.fields(prod.C.StudyConfig)} == KEYS
    assert cfg.root == Path(prod.cfgd["study_root"])
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.steps = 1  # type: ignore[misc]


def test_load_config_unknown_key(prod):
    with pytest.raises(prod.C.ConfigInvalid):
        _load(prod, {**prod.cfgd, "extra_knob": 1})


@pytest.mark.parametrize("key", sorted(KEYS))
def test_load_config_missing_key(prod, key):
    d = dict(prod.cfgd)
    del d[key]
    with pytest.raises(prod.C.ConfigInvalid):
        _load(prod, d)


@pytest.mark.parametrize("key,value", [
    ("steps", "5000"), ("threads", 1.5), ("masters", "310001"), ("sizes", [131072, 4096, 4096]),
    ("gc", "0.27"), ("read_roots", "C:/single"), ("check_stored_ids", "yes"),
    ("env", ["OMP_NUM_THREADS=1"]), ("protocol", 4), ("grid", "0,50"),
    ("stored_checkpoint", "c3358e3cb9c352fb"), ("model_config", [1, 2]), ("cap_s", "21600"),
    ("bootstrap_draws", "2000"), ("protocol_doc_sha256", "not-a-hex-sha"),
    ("sources", ["world"]),
])
def test_load_config_wrong_type(prod, key, value):
    with pytest.raises(prod.C.ConfigInvalid):
        _load(prod, {**prod.cfgd, key: value})


@pytest.mark.parametrize("text", ['{"mode": "production",', "not json", "[]", "", "null"])
def test_load_config_malformed_json(prod, text):
    p = prod.cfgdir / "bad.json"
    p.write_text(text, encoding="utf-8")
    with pytest.raises(prod.C.ConfigInvalid):
        prod.C.load_config(p)


@pytest.mark.parametrize("mode", ["prod", "PRODUCTION", "synthetic", "fixture", "", "test"])
def test_unknown_mode_rejected(prod, mode):
    _assert_rejects(prod, {**prod.cfgd, "mode": mode})


# =============================== §3 validate_config: production ==================================
def test_production_correct_config_passes_read_only(prod):
    assert not Path(prod.cfgd["study_root"]).exists()
    report = _assert_accepts(prod, prod.cfgd)
    assert not Path(prod.cfgd["study_root"]).exists()
    assert prod.spec.sources["world"][1] in json.dumps(report, default=str)


def test_production_paths_compared_after_resolve_and_normcase(prod):
    d = _rt(prod.cfgd)
    d["study_root"] = str(prod.tmp / "x5g1" / ".." / "study")
    d["mailbox"] = str(prod.tmp / "repo" / ".." / "mailbox")
    if sys.platform == "win32":
        d["ledger_path"] = d["ledger_path"].upper()
    _assert_accepts(prod, d)


def test_rejection_before_sampler_leaves_no_study_root(prod):
    """Rejection happens before any sampler/model: spies record nothing, study root absent."""
    d = _rt(prod.cfgd)
    d["gc"]["a0"] = 0.5
    _assert_rejects(prod, d)
    assert prod.calls == [] and not (prod.tmp / "study").exists()
