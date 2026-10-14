"""Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
(docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
Split mechanically from test_x5g1t_config_checks.py (job 0011); tests unchanged.
"""

from __future__ import annotations

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
from topo_pilot.experiment.x5g1t_lineage import CODES, NAMESPACE
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
