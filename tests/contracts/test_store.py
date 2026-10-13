import dataclasses
import json
from collections.abc import Mapping

import numpy as np
import pytest

from topo_pilot import contracts as C
from topo_pilot.contracts import ErrorCode, StageFailure
from topo_pilot.contracts import testing as T

pytestmark = pytest.mark.contracts

CONSUMER = "experiment"


# ---------------------------------------------------------------- helpers
def _norm(v):
    if dataclasses.is_dataclass(v) and not isinstance(v, type):
        return {f.name: _norm(getattr(v, f.name)) for f in dataclasses.fields(v)}
    if isinstance(v, Mapping):
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_norm(x) for x in v]
    if isinstance(v, np.generic):
        return v.item()
    return v


def _same_array(a, b, where):
    a, b = np.asarray(a), np.asarray(b)
    assert a.dtype == b.dtype, f"{where}: dtype {a.dtype} != {b.dtype}"
    assert a.shape == b.shape, f"{where}: shape"
    assert a.tobytes() == b.tobytes(), f"{where}: bytes differ"


def assert_same(a, b):
    assert type(a) is type(b)
    for f in dataclasses.fields(a):
        x, y = getattr(a, f.name), getattr(b, f.name)
        if isinstance(x, np.ndarray):
            _same_array(x, y, f.name)
        elif isinstance(x, Mapping) and x and all(isinstance(v, np.ndarray) for v in x.values()):
            assert {str(k) for k in x} == {str(k) for k in y}
            ymap = {str(k): v for k, v in y.items()}
            for k, v in x.items():
                _same_array(v, ymap[str(k)], f"{f.name}[{k}]")
        elif isinstance(x, (bytes, bytearray)):
            assert bytes(x) == bytes(y)
        else:
            assert json.dumps(_norm(x), sort_keys=True, default=repr) == \
                json.dumps(_norm(y), sort_keys=True, default=repr), f.name


def _snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def _save(store, art, cfg=None, parents=()):
    return store.save(art, config=cfg if cfg is not None else {"case": type(art).__name__},
                      parents=list(parents), seed_map={"init": 1}, consumer=CONSUMER)


def _dir(root, art_type, aid):
    return root / art_type / aid


def _failure(fn, code):
    with pytest.raises(StageFailure) as ei:
        fn()
    assert ei.value.code == code, str(ei.value)
    return ei.value


# ---------------------------------------------------------------- C04
ALL_TYPES = ["WorldSpec", "TransitionSpec", "EmissionSpec", "ObservationSet", "EvalSidecar",
             "HistoryIndex", "OracleOutputs", "ProcessDiagnostics", "BaselineOutputs", "Checkpoint",
             "ActivationSet", "DistanceArtifact", "Diagrams", "MetricRecords", "GateReport",
             "RunManifest"]


def test_C04_all_16_classes_covered(builders):
    assert len(ALL_TYPES) == 16 and set(builders) == set(ALL_TYPES)
    classes = C.ARTIFACT_CLASSES
    classes = classes.values() if isinstance(classes, Mapping) else classes
    names = {getattr(c, "ARTIFACT_TYPE", c) for c in classes}
    assert names == set(ALL_TYPES)
    for name in ALL_TYPES:
        assert builders[name]().ARTIFACT_TYPE == name


@pytest.mark.parametrize("name", ALL_TYPES)
def test_C04_roundtrip_memory(name, builders):
    art = builders[name]()
    art.validate()
    store = T.memory_store()
    cfg = {"case": name, "x": 0.1}
    aid = _save(store, art, cfg)
    assert aid == C.make_artifact_id(name, cfg, [])
    assert_same(art, store.load(type(art), aid, consumer=CONSUMER))
    meta = store.meta(aid)
    assert meta.artifact_id == aid and meta.artifact_type == name
    assert meta.status == "complete" and meta.schema_version == C.SCHEMA_VERSION
    assert meta.seed_map == {"init": 1}
    assert aid in store.find(type(art))


@pytest.mark.parametrize("name", ALL_TYPES)
def test_C04_roundtrip_localfs(name, builders, fs_store):
    store, root = fs_store
    art = builders[name]()
    aid = _save(store, art)
    d = _dir(root, name, aid)
    assert (d / "meta.json").is_file()
    assert (d / "payload.npz").is_file() or name == "Checkpoint"
    if name == "Checkpoint":
        assert (d / "state.pt").is_file()
    loaded = store.load(type(art), aid, consumer=CONSUMER)
    assert_same(art, loaded)
    # a second store over the same root sees the same bits
    store2 = C.ArtifactStore(C.LocalFSBackend(root))
    assert_same(art, store2.load(type(art), aid, consumer=CONSUMER))
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    for key in ("artifact_type", "artifact_id", "schema_version", "parent_ids", "config",
                "seed_map", "producer_version", "created_utc", "shapes", "dtypes",
                "payload_sha256", "status"):
        assert key in meta
    assert meta["status"] == "complete" and meta["artifact_id"] == aid


def test_C04_find_filters_by_config(builders):
    store = T.memory_store()
    a = _save(store, builders["ObservationSet"](), {"k": 1})
    b = _save(store, T.tiny_observations(8, 1), {"k": 2})
    assert set(store.find(C.ObservationSet)) == {a, b}
    assert store.find(C.ObservationSet, k=2) == [b]
    assert store.find(C.EvalSidecar) == []


def test_C04_save_validates_first(builders):
    store = T.memory_store()
    bad = dataclasses.replace(builders["TransitionSpec"](), T=np.full((4, 4), 0.3))
    _failure(lambda: _save(store, bad), ErrorCode.NONSTOCHASTIC)
    assert store.find(C.TransitionSpec) == []


# ---------------------------------------------------------------- C05
def test_C05_second_save_is_noop(builders, fs_store):
    store, root = fs_store
    art = builders["ObservationSet"]()
    a1 = _save(store, art)
    before = _snapshot(root)
    a2 = _save(store, art)
    assert a1 == a2
    assert _snapshot(root) == before  # no rewrite, created_utc untouched
    assert store.find(C.ObservationSet) == [a1]


def test_C05_same_id_different_content_is_checksum_mismatch(builders):
    store = T.memory_store()
    obs = builders["ObservationSet"]()
    aid = _save(store, obs, {"same": 1})
    other = dataclasses.replace(obs, tokens=(obs.tokens + 1) % 3)
    err = _failure(lambda: _save(store, other, {"same": 1}), ErrorCode.CHECKSUM_MISMATCH)
    assert err is not None
    assert_same(obs, store.load(C.ObservationSet, aid, consumer=CONSUMER))


def _tamper_rewrite(path):
    with np.load(path, allow_pickle=False) as z:
        arrays = {k: z[k].copy() for k in z.files}
    arrays["tokens"][0, 0] = (int(arrays["tokens"][0, 0]) + 1) % 3
    np.savez(path, **arrays)


def _tamper_flip(path):
    data = bytearray(path.read_bytes())
    data[len(data) // 2] ^= 0xFF
    path.write_bytes(bytes(data))


@pytest.mark.parametrize("tamper", [_tamper_rewrite, _tamper_flip], ids=["rewrite", "flip"])
def test_C05_tampered_payload_detected(tamper, builders, fs_store):
    store, root = fs_store
    art = builders["ObservationSet"]()
    aid = _save(store, art)
    tamper(_dir(root, "ObservationSet", aid) / "payload.npz")
    _failure(lambda: store.load(C.ObservationSet, aid, consumer=CONSUMER),
             ErrorCode.CHECKSUM_MISMATCH)
    _failure(lambda: _save(store, art), ErrorCode.CHECKSUM_MISMATCH)


def test_C05_tampered_checkpoint_blob_detected(builders, fs_store):
    store, root = fs_store
    art = builders["Checkpoint"]()
    aid = _save(store, art)
    blob = _dir(root, "Checkpoint", aid) / "state.pt"
    blob.write_bytes(blob.read_bytes() + b"x")
    _failure(lambda: store.load(C.Checkpoint, aid, consumer=CONSUMER), ErrorCode.CHECKSUM_MISMATCH)


# ---------------------------------------------------------------- C06 / C07
def _edit_meta(root, art_type, aid, **changes):
    p = _dir(root, art_type, aid) / "meta.json"
    meta = json.loads(p.read_text(encoding="utf-8"))
    meta.update(changes)
    p.write_text(json.dumps(meta), encoding="utf-8")


def test_C06_incomplete_refused(builders, fs_store):
    store, root = fs_store
    aid = _save(store, builders["ObservationSet"]())
    _edit_meta(root, "ObservationSet", aid, status="incomplete")
    _failure(lambda: store.load(C.ObservationSet, aid, consumer=CONSUMER),
             ErrorCode.ARTIFACT_MISSING)


def test_C06_unknown_id_is_missing(fs_store):
    store, _ = fs_store
    _failure(lambda: store.load(C.ObservationSet, "0" * 16, consumer=CONSUMER),
             ErrorCode.ARTIFACT_MISSING)
    _failure(lambda: T.memory_store().load(C.ObservationSet, "0" * 16, consumer=CONSUMER),
             ErrorCode.ARTIFACT_MISSING)


def test_C07_schema_version(builders, fs_store):
    store, root = fs_store
    art = builders["ObservationSet"]()
    aid = _save(store, art)
    _edit_meta(root, "ObservationSet", aid, schema_version="1.7.0")
    assert_same(art, store.load(C.ObservationSet, aid, consumer=CONSUMER))
    _edit_meta(root, "ObservationSet", aid, schema_version="2.0.0")
    _failure(lambda: store.load(C.ObservationSet, aid, consumer=CONSUMER),
             ErrorCode.SCHEMA_VERSION_MISMATCH)


# ---------------------------------------------------------------- C08
def test_C08_learner_cannot_load_evalsidecar(builders):
    store = T.memory_store()
    aid = _save(store, builders["EvalSidecar"]())
    _failure(lambda: store.load(C.EvalSidecar, aid, consumer="learner"), ErrorCode.LEAKAGE)
    _failure(lambda: store.load(C.EvalSidecar, aid, consumer="activations"), ErrorCode.LEAKAGE)
    assert_same(builders["EvalSidecar"](), store.load(C.EvalSidecar, aid, consumer="analysis"))


def test_C08_policy_checked_before_existence():
    store = T.memory_store()
    _failure(lambda: store.load(C.EvalSidecar, "0" * 16, consumer="learner"), ErrorCode.LEAKAGE)


def _allowed(art_type, consumer):
    try:
        C.DEFAULT_ACCESS_POLICY.check(art_type, consumer)
        return True
    except StageFailure as e:
        assert e.code == ErrorCode.LEAKAGE
        return False


def test_C08_default_policy_table():
    for c in ("analysis", "prediction", "experiment"):
        assert _allowed("EvalSidecar", c)
    for c in ("learner", "activations", "process", "dataset", "oracle"):
        assert not _allowed("EvalSidecar", c)
    for t in ("WorldSpec", "TransitionSpec", "EmissionSpec"):
        for c in ("process", "dataset", "oracle", "analysis", "experiment"):
            assert _allowed(t, c), (t, c)
        for c in ("learner", "activations"):
            assert not _allowed(t, c), (t, c)
    for c in C.MODULES:
        assert _allowed("ObservationSet", c) == (c != "world"), c
        assert _allowed("OracleOutputs", c), c
        assert _allowed("Diagrams", c), c
    for c in ("learner", "activations", "experiment"):
        assert _allowed("Checkpoint", c)
    for c in ("oracle", "analysis", "dataset", "topology"):
        assert not _allowed("Checkpoint", c)


def test_C08_custom_policy():
    pol = C.AccessPolicy({"WorldSpec": frozenset({"a"})})
    pol.check("WorldSpec", "a")
    _failure(lambda: pol.check("WorldSpec", "b"), ErrorCode.LEAKAGE)
    store = C.ArtifactStore(C.MemoryBackend(), pol)
    aid = store.save(T.tiny_world_spec(), config={}, parents=[], seed_map={}, consumer="a")
    store.load(C.WorldSpec, aid, consumer="a")
    _failure(lambda: store.load(C.WorldSpec, aid, consumer="b"), ErrorCode.LEAKAGE)


# ---------------------------------------------------------------- C12
def _chain(store, builders):
    wid = _save(store, builders["WorldSpec"]())
    oid = _save(store, builders["ObservationSet"](), {"child": 1}, [wid])
    return wid, oid


def test_C12_missing_parent_on_save(builders):
    store = T.memory_store()
    _failure(lambda: _save(store, builders["ObservationSet"](), parents=["f" * 16]),
             ErrorCode.MISSING_PARENT)


def test_C12_bundle_roundtrip(builders, tmp_path):
    src = C.ArtifactStore(C.LocalFSBackend(tmp_path / "a"))
    wid, oid = _chain(src, builders)
    assert src.meta(oid).parent_ids == (wid,) or list(src.meta(oid).parent_ids) == [wid]
    bundle = src.export_bundle([oid], tmp_path / "out")
    assert bundle.is_file() and "".join(bundle.suffixes).endswith(".tar.gz")
    dst = C.ArtifactStore(C.LocalFSBackend(tmp_path / "b"))
    ids = dst.import_bundle(bundle)
    assert set(ids) == {wid, oid} and len(ids) == 2
    assert ids.index(wid) < ids.index(oid)
    for aid in (wid, oid):
        assert dst.meta(aid).payload_sha256 == src.meta(aid).payload_sha256
        assert dst.meta(aid).artifact_id == aid
    assert_same(builders["ObservationSet"](), dst.load(C.ObservationSet, oid, consumer=CONSUMER))
    assert_same(builders["WorldSpec"](), dst.load(C.WorldSpec, wid, consumer=CONSUMER))
    # importing again is harmless
    assert set(dst.import_bundle(bundle)) <= {wid, oid}


def test_C12_bundle_into_memory_store(builders, tmp_path):
    src = T.memory_store()
    wid, oid = _chain(src, builders)
    bundle = src.export_bundle([oid], tmp_path)
    dst = T.memory_store()
    assert set(dst.import_bundle(bundle)) == {wid, oid}
    assert_same(builders["ObservationSet"](), dst.load(C.ObservationSet, oid, consumer=CONSUMER))


def test_C12_bundle_without_parents_needs_parents(builders, tmp_path):
    src = T.memory_store()
    wid, oid = _chain(src, builders)
    bundle = src.export_bundle([oid], tmp_path, with_parents=False)
    fresh = T.memory_store()
    _failure(lambda: fresh.import_bundle(bundle), ErrorCode.MISSING_PARENT)
    # with the parent already present the same bundle imports
    full = src.export_bundle([wid], tmp_path / "w", with_parents=True)
    holder = T.memory_store()
    holder.import_bundle(full)
    assert holder.import_bundle(bundle) == [oid]
