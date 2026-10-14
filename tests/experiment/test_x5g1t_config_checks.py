"""Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
(docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
"""

from __future__ import annotations

import copy
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
from topo_pilot.contracts import (
    ArtifactStore,
    Checkpoint,
    LocalFSBackend,
    ObservationSet,
    TransitionSpec,
)
from topo_pilot.contracts.testing import tiny_observations, tiny_world_spec
from topo_pilot.experiment import x5g1t_lineage, x5g1t_train
from topo_pilot.experiment.x5g1_controls import BudgetExceeded, StopRequested
from topo_pilot.experiment.x5g1t_fixture import E0, T0, _emission
from topo_pilot.experiment.x5g1t_lineage import CODES, NAMESPACE
from topo_pilot.experiment.x5g1t_runtime import ResourceExceeded
from topo_pilot.experiment.x5g1t_train import study_run_key, study_train_config
from topo_pilot.learner import ModelConfig, TrainConfig


# ---- lazy module access (x5g1t_config may land after these tests) ------------------------------
def _cm():
    return importlib.import_module("topo_pilot.experiment.x5g1t_config")


def _ex():
    return importlib.import_module("topo_pilot.experiment.x5g1t_exports")


def _ck():
    return importlib.import_module("topo_pilot.experiment.x5g1t_checks")


KEYS = {"mode", "protocol", "protocol_doc", "protocol_doc_sha256", "read_roots", "study_root",
        "ledger_path", "mailbox", "sources", "source_producers", "stored_checkpoint", "masters",
        "sizes", "model_config", "steps", "grid", "gc", "threads", "bootstrap_draws", "cap_s",
        "cumulative_cap_s", "check_stored_ids", "env"}
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


PROD_TAMPER = {
    "source_world_id_is_other_artifact":
        lambda d, e: _put(d, ("sources", "world"), list(d["sources"]["T"]["a0"])),
    "source_world_sha": lambda d, e: _put(d, ("sources", "world", 1),
                                          _flip(d["sources"]["world"][1])),
    "source_world_unknown_id": lambda d, e: _put(d, ("sources", "world", 0), "deadbeefdeadbeef"),
    "source_T_a0_sha": lambda d, e: _put(d, ("sources", "T", "a0", 1),
                                         _flip(d["sources"]["T"]["a0"][1])),
    "source_T_a020_sha": lambda d, e: _put(d, ("sources", "T", "a020", 1),
                                           _flip(d["sources"]["T"]["a020"][1])),
    "source_T_arms_swapped": lambda d, e: _put(d, ("sources", "T"), {
        "a0": d["sources"]["T"]["a020"], "a020": d["sources"]["T"]["a0"]}),
    "source_E_sha": lambda d, e: _put(d, ("sources", "E", 1), _flip(d["sources"]["E"][1])),
    "source_E_is_world": lambda d, e: _put(d, ("sources", "E"), list(d["sources"]["world"])),
    "source_producer": lambda d, e: _put(d, ("source_producers", d["sources"]["world"][0]),
                                         "other-producer"),
    "stored_ckpt_sha": lambda d, e: _put(d, ("stored_checkpoint", 1),
                                         _flip(d["stored_checkpoint"][1])),
    "stored_ckpt_id": lambda d, e: _put(d, ("stored_checkpoint", 0), d["sources"]["world"][0]),
    "stored_ckpt_null": lambda d, e: _put(d, ("stored_checkpoint",), None),
    "gc_a0": lambda d, e: _put(d, ("gc", "a0"), 0.2713),
    "gc_a020": lambda d, e: _put(d, ("gc", "a020"), d["gc"]["a020"] + 1e-9),
    "gc_swapped": lambda d, e: _put(d, ("gc",), {"a0": d["gc"]["a020"], "a020": d["gc"]["a0"]}),
    "cap_s_up": lambda d, e: _put(d, ("cap_s",), 21601.0),
    "cap_s_down": lambda d, e: _put(d, ("cap_s",), 3600.0),
    "cumulative_cap_s": lambda d, e: _put(d, ("cumulative_cap_s",), 43200.0),
    "grid_dropped_point": lambda d, e: _put(d, ("grid",), d["grid"][:-2] + d["grid"][-1:]),
    "grid_changed_point": lambda d, e: _put(d, ("grid", 1), d["grid"][1] + 1),
    "masters_dropped": lambda d, e: _put(d, ("masters",), [310001, 310002]),
    "masters_other": lambda d, e: _put(d, ("masters",), [310001, 310002, 310004]),
    "sizes_train": lambda d, e: _put(d, ("sizes", "train"), 131071),
    "sizes_dev": lambda d, e: _put(d, ("sizes", "dev"), 4097),
    "sizes_test": lambda d, e: _put(d, ("sizes", "test"), 1024),
    "steps": lambda d, e: _put(d, ("steps",), 4999),
    "steps_and_grid_end": lambda d, e: (_put(d, ("steps",), 6000),
                                        _put(d, ("grid", -1), 6000)),
    "model_d_model": lambda d, e: _put(d, ("model_config", "d_model"), 16),
    "model_n_layers": lambda d, e: _put(d, ("model_config", "n_layers"), 2),
    "threads": lambda d, e: _put(d, ("threads",), 2),
    "bootstrap_draws": lambda d, e: _put(d, ("bootstrap_draws",), 1999),
    "check_stored_ids_off": lambda d, e: _put(d, ("check_stored_ids",), False),
    "protocol": lambda d, e: _put(d, ("protocol",), "x5g1-train-v3"),
    "protocol_doc_sha": lambda d, e: _put(d, ("protocol_doc_sha256",),
                                          _flip(d["protocol_doc_sha256"])),
    "protocol_doc_path": lambda d, e: _put(d, ("protocol_doc",), "docs/OTHER.md"),
    "read_roots_dropped": lambda d, e: _put(d, ("read_roots",), d["read_roots"][:2]),
    "read_roots_other": lambda d, e: _put(d, ("read_roots", 2), str(e.tmp / "other" / "store")),
    "study_root_other": lambda d, e: _put(d, ("study_root",), str(e.tmp / "study2")),
    "ledger_other": lambda d, e: _put(d, ("ledger_path",), str(e.tmp / "x5g1" / "ledger2.json")),
    "mailbox_other": lambda d, e: _put(d, ("mailbox",), str(e.tmp / "mailbox2")),
    "env_cfg_differs_from_spec": lambda d, e: _put(d, ("env", "OMP_NUM_THREADS"), "2"),
    "env_cfg_missing_key": lambda d, e: d["env"].pop("MKL_NUM_THREADS"),
    "mode_switched_to_synthetic": lambda d, e: _put(d, ("mode",), "synthetic-fixture"),
}


@pytest.mark.parametrize("case", sorted(PROD_TAMPER))
def test_production_each_tampered_field_rejected(prod, case):
    d = _rt(prod.cfgd)
    PROD_TAMPER[case](d, prod)
    assert d != prod.cfgd
    _assert_rejects(prod, d)


def test_production_cfg_env_matching_environ_but_not_spec_rejected(prod, monkeypatch):
    d = _rt(prod.cfgd)
    d["env"]["OMP_NUM_THREADS"] = "4"
    monkeypatch.setenv("OMP_NUM_THREADS", "4")
    _assert_rejects(prod, d)


@pytest.mark.parametrize("name", ["OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"])
def test_production_env_missing_from_os_environ_rejected(prod, monkeypatch, name):
    monkeypatch.delenv(name, raising=False)
    _assert_rejects(prod, prod.cfgd)


@pytest.mark.parametrize("name", ["OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"])
def test_production_env_differing_in_os_environ_rejected(prod, monkeypatch, name):
    monkeypatch.setenv(name, "8")
    _assert_rejects(prod, prod.cfgd)


def test_production_protocol_doc_bytes_changed_rejected(prod):
    cfg = _load(prod, prod.cfgd)
    prod.doc.write_bytes(prod.doc.read_bytes() + b"edited\n")
    before = _snapshot(prod.tmp)
    with pytest.raises(prod.C.ConfigInvalid):
        prod.C.validate_config(cfg, prod.repo, spec=prod.spec)
    assert _snapshot(prod.tmp) == before


def test_production_spec_doc_sha_differs_from_consistent_cfg_rejected(prod):
    """cfg and the repo document agree but the spec pins another sha256."""
    spec = dataclasses.replace(prod.spec, protocol_doc_sha256="0" * 64)
    _assert_rejects(prod, prod.cfgd, spec=spec)


def _mutate_npz(path: Path) -> None:
    with np.load(path, allow_pickle=False) as z:
        arrays = {k: z[k].copy() for k in z.files}
    k = next(k for k, v in arrays.items() if v.dtype.kind == "f" and v.size)
    arrays[k].flat[0] += 1.0
    np.savez(path, **arrays)


def test_production_source_payload_mutated_on_disk_rejected(prod):
    """Same metadata, mutated payload: the full re-hash must catch it."""
    wid = prod.ids["world"]
    for r in prod.reads:
        _mutate_npz(r / "WorldSpec" / wid / "payload.npz")
    _assert_rejects(prod, prod.cfgd)


def test_production_source_of_wrong_artifact_type_rejected(prod):
    """cfg and spec agree, but the 'world' source is a TransitionSpec."""
    sources = _rt(prod.spec.sources)
    sources["world"] = list(sources["T"]["a0"])
    spec = dataclasses.replace(prod.spec, sources=sources)
    _assert_rejects(prod, _cfg_from_spec(spec), spec=spec)


def test_production_stored_producer_differs_from_consistent_cfg_rejected(prod):
    """cfg and spec agree on a producer that is not the stored producer_version."""
    producers = {i: "forged-producer" for i in prod.spec.source_producers}
    spec = dataclasses.replace(prod.spec, source_producers=producers)
    _assert_rejects(prod, _cfg_from_spec(spec), spec=spec)


def _with_stored(prod, model: dict, train: dict, spec_model: dict | None = None):
    for st in prod.stores:
        cid = _save_stored_ckpt(st, model, train, tag="alt")
    sha = prod.stores[0].meta(cid).payload_sha256
    spec = dataclasses.replace(prod.spec, stored_checkpoint=(cid, sha),
                               stored_model_config=dict(spec_model or model),
                               stored_train_config=train)
    return spec


@pytest.mark.parametrize("field,value", [("lr", 2e-3), ("batch_size", 64), ("warmup", 100),
                                         ("weight_decay", 0.0), ("grad_clip", 0.5),
                                         ("steps", 4000)])
def test_production_stored_train_config_differs_beyond_grid_and_device_rejected(prod, field,
                                                                               value):
    train = _rt(dataclasses.asdict(dataclasses.replace(TrainConfig(), **{field: value})))
    spec = _with_stored(prod, MODEL, train)
    _assert_rejects(prod, _cfg_from_spec(spec), spec=spec)


def test_production_stored_train_config_device_and_grid_are_replaced(prod):
    """Only checkpoint_steps (-> grid) and device (-> "cpu") may differ from the stored dict."""
    train = _rt(dataclasses.asdict(dataclasses.replace(
        TrainConfig(), device="cuda", checkpoint_steps=(0, 5000))))
    spec = _with_stored(prod, MODEL, train)
    _assert_accepts(prod, _cfg_from_spec(spec), spec=spec)


def test_production_stored_model_config_differs_from_cfg_rejected(prod):
    other = dict(MODEL, d_model=16)
    spec = _with_stored(prod, other, prod.stored_train, spec_model=MODEL)
    _assert_rejects(prod, _cfg_from_spec(spec), spec=spec)


def test_production_stored_checkpoint_not_a_checkpoint_rejected(prod):
    spec = dataclasses.replace(prod.spec, stored_checkpoint=tuple(prod.spec.sources["world"]))
    _assert_rejects(prod, _cfg_from_spec(spec), spec=spec)


@pytest.mark.parametrize("lineage", [
    {"namespace": "x5g1-train-v9", "codes": dict(CODES),
     "stream_tail": ("cylinder", "overlap", "1.25")},
    {"namespace": NAMESPACE, "codes": {**CODES, "test": 12},
     "stream_tail": ("cylinder", "overlap", "1.25")},
    {"namespace": NAMESPACE, "codes": dict(CODES), "stream_tail": ("cylinder", "overlap", "1.5")},
])
def test_production_lineage_constants_mismatch_rejected(prod, lineage):
    spec = dataclasses.replace(prod.spec, lineage=lineage)
    _assert_rejects(prod, prod.cfgd, spec=spec)


@pytest.mark.parametrize("where", ["equals_read_root", "inside_read_root", "inside_repo",
                                   "equals_repo", "inside_main_repository",
                                   "ledger_inside_study_root"])
def test_production_write_root_safety(prod, where):
    """spec and cfg agree, so only the write-root rule can reject."""
    t, reads = prod.tmp, prod.reads
    roots = {
        "equals_read_root": {"study_root": str(reads[0])},
        "inside_read_root": {"study_root": str(reads[1] / "x5g1t")},
        "inside_repo": {"study_root": str(prod.repo / "x5g1t")},
        "equals_repo": {"study_root": str(prod.repo)},
        "inside_main_repository": {"study_root": str(t / "main" / "x5g1t")},
        "ledger_inside_study_root": {
            "ledger_path": str(t / "study" / "cpu_ledger.json")},
    }[where]
    spec = dataclasses.replace(prod.spec, **roots)
    _assert_rejects(prod, _cfg_from_spec(spec), spec=spec)


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


# =============================== §4 exports ======================================================
class FakeSC:
    """StudyControls stand-in: records each boundary and raises ``exc`` where ``stop_at``."""

    def __init__(self, stop_at=None, exc=StopRequested):
        self.calls: list[str] = []
        self.stop_at, self.exc = stop_at, exc

    def boundary(self, what, next_estimate=0.0, reserve=0.0, audit=dict):
        self.calls.append(what)
        if self.stop_at is not None and self.stop_at(what):
            raise self.exc(f"injected at {what}")


FILES = {"alpha.json": {"a": 1}, "beta.json": {"b": [1, 2]}, "gamma.json": {"g": "x"}}
STATUS = {StopRequested: "STOPPED_DURING_EXPORT", BudgetExceeded: "BUDGET_DURING_EXPORT",
          ResourceExceeded: "RESOURCE_DURING_EXPORT"}


def _out(tmp_path: Path) -> Path:
    out = tmp_path / "export"
    out.mkdir()
    return out


def _data_files(out: Path) -> list[str]:
    return sorted(p.name for p in out.iterdir()
                  if p.name not in ("MANIFEST.json", "EXPORT_STATUS.json"))


def _status(out: Path) -> dict:
    return json.loads((out / "EXPORT_STATUS.json").read_text(encoding="utf-8"))


def _complete(tmp_path: Path, arrays=None) -> Path:
    out = _out(tmp_path)
    _ex().study_export(FakeSC(), out, dict(FILES), arrays=arrays)
    return out


def test_export_roundtrip_complete_and_guarded(tmp_path):
    ex = _ex()
    out = _out(tmp_path)
    sc = FakeSC()
    ex.study_export(sc, out, dict(FILES))
    assert _status(out)["status"] == "COMPLETE"
    man = ex.verify_export_complete(out)
    assert isinstance(man, dict)
    names = {p.name for p in out.iterdir()}
    assert {"MANIFEST.json", "EXPORT_STATUS.json"} <= names
    assert len(_data_files(out)) == 3
    for n in _data_files(out):
        assert _sha_file(out / n) in json.dumps(man)
    done = _status(out)["completed_steps"]
    for stem in ("alpha", "beta", "gamma", "MANIFEST"):
        if stem != "MANIFEST":  # whether the manifest step is listed is not specified
            assert any(stem in str(s) for s in done)
        i = next(k for k, w in enumerate(sc.calls) if stem in w and not w.endswith("done"))
        assert sc.calls[i].startswith("export ")
        assert stem in sc.calls[i + 1] and sc.calls[i + 1].endswith(" done")
    order = [next(k for k, w in enumerate(sc.calls) if s in w)
             for s in ("alpha", "beta", "gamma", "MANIFEST")]
    assert order == sorted(order)


def test_export_roundtrip_with_arrays(tmp_path):
    out = _complete(tmp_path, arrays={"delta.npz": {"x": np.arange(3)}})
    man = _ex().verify_export_complete(out)
    assert len(_data_files(out)) == 4
    for n in _data_files(out):
        assert _sha_file(out / n) in json.dumps(man)


@pytest.mark.parametrize("exc", [StopRequested, BudgetExceeded, ResourceExceeded])
def test_export_interrupted_before_second_file(tmp_path, exc):
    ex = _ex()
    out = _out(tmp_path)
    sc = FakeSC(stop_at=lambda w: "beta" in w and not w.endswith("done"), exc=exc)
    with pytest.raises(exc):
        ex.study_export(sc, out, dict(FILES))
    assert len(_data_files(out)) == 1 and _data_files(out)[0].startswith("alpha")
    assert not (out / "MANIFEST.json").exists()
    st = _status(out)
    assert st["status"] == STATUS[exc]
    assert any("alpha" in str(s) for s in st["completed_steps"])
    assert not any(("beta" in str(s)) or ("gamma" in str(s)) for s in st["completed_steps"])
    assert "cause" in st
    assert "beta" in sc.calls[-1], "no boundary (hence no further step) after the stop"
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)


def test_export_stop_after_file_done_writes_nothing_further(tmp_path):
    ex = _ex()
    out = _out(tmp_path)
    sc = FakeSC(stop_at=lambda w: "beta" in w and w.endswith("done"))
    with pytest.raises(StopRequested):
        ex.study_export(sc, out, dict(FILES))
    assert not any(n.startswith("gamma") for n in _data_files(out))
    assert not (out / "MANIFEST.json").exists()
    assert _status(out)["status"] == "STOPPED_DURING_EXPORT"
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)


def test_export_stop_before_manifest(tmp_path):
    ex = _ex()
    out = _out(tmp_path)
    sc = FakeSC(stop_at=lambda w: "MANIFEST" in w and not w.endswith("done"))
    with pytest.raises(StopRequested):
        ex.study_export(sc, out, dict(FILES))
    assert not (out / "MANIFEST.json").exists()
    st = _status(out)
    assert st["status"] == "STOPPED_DURING_EXPORT"
    assert sum(any(s in str(x) for x in st["completed_steps"])
               for s in ("alpha", "beta", "gamma")) == 3
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)


def test_export_tampered_file_bytes_incomplete(tmp_path):
    out = _complete(tmp_path)
    p = out / _data_files(out)[0]
    p.write_bytes(p.read_bytes() + b" ")
    with pytest.raises(_ex().ExportIncomplete):
        _ex().verify_export_complete(out)


def test_export_extra_file_incomplete(tmp_path):
    out = _complete(tmp_path)
    (out / "zeta.json").write_text("{}", encoding="utf-8")
    with pytest.raises(_ex().ExportIncomplete):
        _ex().verify_export_complete(out)


def test_export_missing_manifest_incomplete(tmp_path):
    out = _complete(tmp_path)
    (out / "MANIFEST.json").unlink()
    with pytest.raises(_ex().ExportIncomplete):
        _ex().verify_export_complete(out)


def test_export_missing_data_file_incomplete(tmp_path):
    out = _complete(tmp_path)
    (out / _data_files(out)[1]).unlink()
    with pytest.raises(_ex().ExportIncomplete):
        _ex().verify_export_complete(out)


def test_export_missing_or_non_complete_status_incomplete(tmp_path):
    ex = _ex()
    out = _complete(tmp_path)
    st = _status(out)
    (out / "EXPORT_STATUS.json").write_text(
        json.dumps({**st, "status": "STOPPED_DURING_EXPORT"}), encoding="utf-8")
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)
    (out / "EXPORT_STATUS.json").unlink()
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)


def test_export_error_classes_are_runtime_errors():
    assert issubclass(_ex().ExportIncomplete, RuntimeError)
    assert issubclass(_ck().IntegrityFailed, RuntimeError)
    assert issubclass(_cm().ConfigInvalid, RuntimeError)


# =============================== §5 checkpoints and full hashes ==================================
STEPS, GRID = 4, (0, 2, 4)
MASTER = 310001


def _obs(split: str, seed: int) -> ObservationSet:
    base = tiny_observations(R=8, seed=seed)
    return ObservationSet(split=split, V=3, sequence_id=np.arange(8, dtype=np.int64) + 100 * seed,
                          tokens=base.tokens)


def _ckstore(root: Path):
    st = ArtifactStore(LocalFSBackend(root))
    kw = dict(parents=[], seed_map={}, consumer="experiment")
    train = st.save(_obs("train", 1), config={"role": "train"}, **kw)
    dev = st.save(_obs("dev", 2), config={"role": "dev"}, **kw)
    other = st.save(_obs("dev", 3), config={"role": "other"}, **kw)
    return st, train, dev, other


def _save_run(st, train_id, dev_id, *, master=MASTER, run_master=None, grid=GRID, steps=STEPS,
              model=MODEL, train_cfg=None, parents=None, obs_id=None) -> dict:
    run_key = study_run_key(run_master if run_master is not None else master)
    tc = train_cfg or dataclasses.asdict(study_train_config(steps, grid))
    rec = []
    for step in grid:
        ck = Checkpoint(run_id="-".join(map(str, run_key)), step=step,
                        observation_id=obs_id or train_id, state=f"weights-{step}".encode(),
                        model_config=model, train_config=tc)
        config = {"run_key": list(run_key), "step": step, "model_config": model,
                  "train_config": tc}
        cid = st.save(ck, config=config, parents=parents or [train_id, dev_id], seed_map={},
                      consumer="experiment")
        rec.append({"step": step, "checkpoint_id": cid,
                    "payload_sha256": st.meta(cid).payload_sha256})
    return {"status": "COMPLETE", "arm": "a0", "master": master, "checkpoints": rec,
            "cause": None}


def _cfg(grid=GRID, steps=STEPS, model=None):
    return SimpleNamespace(grid=grid, steps=steps, model_config=dict(model or MODEL))


@pytest.fixture
def ckrun(tmp_path):
    st, train, dev, other = _ckstore(tmp_path / "store")
    outcome = _save_run(st, train, dev)
    return SimpleNamespace(st=st, train=train, dev=dev, other=other, outcome=outcome,
                           root=tmp_path / "store", tmp=tmp_path)


@pytest.mark.parametrize("grid", [list(GRID), tuple(GRID)])
def test_validate_checkpoints_real_store_passes(ckrun, grid):
    cid0 = ckrun.outcome["checkpoints"][0]["checkpoint_id"]
    assert isinstance(ckrun.st.meta(cid0).config["train_config"]["checkpoint_steps"], list)
    got = _ck().validate_checkpoints(ckrun.st, ckrun.outcome, _cfg(grid=grid), "a0", MASTER,
                                     ckrun.train, ckrun.dev)
    assert set(got) == {c["checkpoint_id"] for c in ckrun.outcome["checkpoints"]}
    for c in ckrun.outcome["checkpoints"]:
        ck, sha = got[c["checkpoint_id"]]
        # "(Checkpoint, sha)": the verify_full expected form (class) or a loaded instance
        assert (ck is Checkpoint or isinstance(ck, Checkpoint)) and sha == c["payload_sha256"]


def test_validate_checkpoints_model_config_compared_with_defaults_filled(ckrun):
    partial = {"vocab_in": 4, "vocab_out": 3, "n_layers": 1, "d_model": 8, "n_heads": 2,
               "d_mlp": 16}
    _ck().validate_checkpoints(ckrun.st, ckrun.outcome, _cfg(model=partial), "a0", MASTER,
                               ckrun.train, ckrun.dev)


def _fails(ckrun, outcome=None, cfg=None, arm="a0", master=MASTER, train=None, dev=None,
           st=None):
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st or ckrun.st, outcome or ckrun.outcome, cfg or _cfg(), arm,
                                master, train or ckrun.train, dev or ckrun.dev)


def test_checkpoints_reordered_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["checkpoints"] = o["checkpoints"][::-1]
    _fails(ckrun, outcome=o)


def test_checkpoints_swapped_ids_same_steps_rejected(ckrun):
    o = _rt(ckrun.outcome)
    a, b = o["checkpoints"][0], o["checkpoints"][1]
    a["checkpoint_id"], b["checkpoint_id"] = b["checkpoint_id"], a["checkpoint_id"]
    a["payload_sha256"], b["payload_sha256"] = b["payload_sha256"], a["payload_sha256"]
    _fails(ckrun, outcome=o)


def test_checkpoints_missing_one_rejected(ckrun):
    o = _rt(ckrun.outcome)
    del o["checkpoints"][1]
    _fails(ckrun, outcome=o)


def test_checkpoints_grid_differs_rejected(ckrun):
    _fails(ckrun, cfg=_cfg(grid=(0, 1, 4)))


def test_checkpoints_wrong_dev_parent_rejected(ckrun):
    _fails(ckrun, dev=ckrun.other)


def test_checkpoints_saved_with_wrong_parents_rejected(tmp_path):
    st, train, dev, other = _ckstore(tmp_path / "s2")
    outcome = _save_run(st, train, dev, parents=[train, other])
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st, outcome, _cfg(), "a0", MASTER, train, dev)


def test_checkpoints_wrong_model_config_rejected(ckrun):
    _fails(ckrun, cfg=_cfg(model=dict(MODEL, d_model=16)))


def test_checkpoints_wrong_steps_rejected(ckrun):
    _fails(ckrun, cfg=_cfg(steps=STEPS + 2, grid=GRID))


def test_checkpoints_saved_with_wrong_train_config_rejected(tmp_path):
    st, train, dev, _ = _ckstore(tmp_path / "s3")
    tc = dataclasses.asdict(dataclasses.replace(study_train_config(STEPS, GRID), lr=5e-3))
    outcome = _save_run(st, train, dev, train_cfg=tc)
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st, outcome, _cfg(), "a0", MASTER, train, dev)


def test_checkpoints_outcome_arm_mismatch_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["arm"] = "a020"
    _fails(ckrun, outcome=o)
    _fails(ckrun, arm="a020")


def test_checkpoints_outcome_master_mismatch_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["master"] = 310002
    _fails(ckrun, outcome=o)
    _fails(ckrun, master=310002)


def test_checkpoints_of_another_master_rejected(tmp_path):
    """outcome claims master 310001 but the checkpoints carry 310002's run key."""
    st, train, dev, _ = _ckstore(tmp_path / "s4")
    outcome = _save_run(st, train, dev, master=MASTER, run_master=310002)
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st, outcome, _cfg(), "a0", MASTER, train, dev)


def test_checkpoints_wrong_observation_id_rejected(tmp_path):
    st, train, dev, _ = _ckstore(tmp_path / "s5")
    outcome = _save_run(st, train, dev, obs_id=dev)
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.validate_checkpoints(st, outcome, _cfg(), "a0", MASTER, train, dev)


def test_checkpoints_recorded_sha_wrong_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["checkpoints"][2]["payload_sha256"] = _flip(o["checkpoints"][2]["payload_sha256"])
    _fails(ckrun, outcome=o)


def test_checkpoints_not_a_checkpoint_rejected(ckrun):
    o = _rt(ckrun.outcome)
    o["checkpoints"][0]["checkpoint_id"] = ckrun.train
    o["checkpoints"][0]["payload_sha256"] = ckrun.st.meta(ckrun.train).payload_sha256
    _fails(ckrun, outcome=o)


def test_checkpoints_same_metadata_mutated_payload_rejected(ckrun):
    cid = ckrun.outcome["checkpoints"][1]["checkpoint_id"]
    meta_before = (ckrun.root / "Checkpoint" / cid / "meta.json").read_bytes()
    (ckrun.root / "Checkpoint" / cid / "state.pt").write_bytes(b"tampered-weights")
    assert (ckrun.root / "Checkpoint" / cid / "meta.json").read_bytes() == meta_before
    _fails(ckrun)


# ---- verify_full ------------------------------------------------------------------------------
def test_verify_full_passes_on_lawful_artifacts(ckrun):
    exp = {ckrun.train: (ObservationSet, ckrun.st.meta(ckrun.train).payload_sha256)}
    for c in ckrun.outcome["checkpoints"]:
        exp[c["checkpoint_id"]] = (Checkpoint, c["payload_sha256"])
    assert _ck().verify_full(ckrun.st, exp, "before") is None


def test_verify_full_missing_id_rejected(ckrun):
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.verify_full(ckrun.st, {"0123456789abcdef": (ObservationSet, "0" * 64)}, "before")


def test_verify_full_wrong_sha_rejected(ckrun):
    ck = _ck()
    sha = ckrun.st.meta(ckrun.train).payload_sha256
    with pytest.raises(ck.IntegrityFailed):
        ck.verify_full(ckrun.st, {ckrun.train: (ObservationSet, _flip(sha))}, "before")


def test_verify_full_wrong_class_rejected(ckrun):
    ck = _ck()
    sha = ckrun.st.meta(ckrun.train).payload_sha256
    with pytest.raises(ck.IntegrityFailed):
        ck.verify_full(ckrun.st, {ckrun.train: (Checkpoint, sha)}, "before")


def test_verify_full_mutated_payload_rejected(ckrun):
    c = ckrun.outcome["checkpoints"][0]
    (ckrun.root / "Checkpoint" / c["checkpoint_id"] / "state.pt").write_bytes(b"x")
    ck = _ck()
    with pytest.raises(ck.IntegrityFailed):
        ck.verify_full(ckrun.st, {c["checkpoint_id"]: (Checkpoint, c["payload_sha256"])},
                       "after")


def test_rejection_before_sampler_leaves_no_study_root(prod):
    """Rejection happens before any sampler/model: spies record nothing, study root absent."""
    d = _rt(prod.cfgd)
    d["gc"]["a0"] = 0.5
    _assert_rejects(prod, d)
    assert prod.calls == [] and not (prod.tmp / "study").exists()
