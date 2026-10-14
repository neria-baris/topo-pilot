"""Independent input-identity regressions for X5 G1 API v4.1 in the evaluation paths (§D; §E items
3, 4 and the test-pool half of 5).

Written from the contract only (test writer G, job 0011): actual ``pools``, ``dev-analysis`` and
``final-test`` stages on a tiny SYNTHETIC fixture whose read root also holds a tiny old-ID
``ObservationSet`` (never the real main store). Substitutions keep every checksum valid.
"""

from __future__ import annotations

import hashlib
import io
import json
import shutil
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import ArtifactStore, LocalFSBackend, ObservationSet
from topo_pilot.experiment import x5g1t_stages, x5g1t_stages_eval
from topo_pilot.experiment.x4b import ReadThroughBackend
from topo_pilot.experiment.x5g1t_checks import IntegrityFailed
from topo_pilot.experiment.x5g1t_config import load_config, read_chain
from topo_pilot.experiment.x5g1t_fixture import build_fixture
from topo_pilot.experiment.x5g1t_lineage import CODES, MASTERS, TEST_MASTER, stream

pytestmark = pytest.mark.experiment

REPO = Path(__file__).resolve().parents[2]
SIZES = {"train": 8, "dev": 4, "test": 4}
M1, M2, M3 = MASTERS
ARMS = ("a0", "a020")
_REAL_GET = LocalFSBackend.get


class _Reached(Exception):
    """Raised by a spy: the stage got past every check to the guarded call."""


# --- helpers -----------------------------------------------------------------------------------

def _clone(src: Path, dst: Path):
    shutil.copytree(src, dst)
    cfg_path = dst / "study_config.json"
    text = cfg_path.read_text(encoding="utf-8")
    old, new = json.dumps(str(src))[1:-1], json.dumps(str(dst))[1:-1]
    cfg_path.write_text(text.replace(old, new), encoding="utf-8")
    return load_config(cfg_path)


def _out(root: Path, *parts: str) -> Path:
    return root / "study" / "tables" / Path(*parts)


def _pools(root: Path) -> dict:
    return json.loads((_out(root, "pools") / "pools.json").read_text(encoding="utf-8"))


def _existing(root: Path, key: str) -> tuple[str, str]:
    p = _pools(root)
    return p["pools"][key], p["pool_sha256"][key]


def _remap(root: Path, cfg, changes: dict) -> None:
    """Point pools.json keys at ``(pool_id, sha)`` and recompute the COMPLETE manifest."""
    out = _out(root, "pools")
    pools = _pools(root)
    for key, (pid, sha) in changes.items():
        pools["pools"][key], pools["pool_sha256"][key] = pid, sha
    (out / "pools.json").write_text(json.dumps(pools, indent=1), encoding="utf-8")
    manifest = json.loads((out / "MANIFEST.json").read_text(encoding="utf-8"))
    manifest["pools.json"] = hashlib.sha256((out / "pools.json").read_bytes()).hexdigest()
    (out / "MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
    x5g1t_stages.complete_pools(cfg)  # setup sanity: every checksum is valid


def _reordered_ids(root: Path, key: str) -> tuple[str, str]:
    """Replace pool ``key`` in place (same id, same config and parents) by a checksum-valid copy
    whose sequence IDs are reversed: right set, wrong order."""
    pid = _pools(root)["pools"][key]
    sdir = root / "study" / "store"
    # Writes go to the study store; the parents resolve through the fixture read root.
    store = ArtifactStore(ReadThroughBackend(read_chain([root / "sources"]), LocalFSBackend(sdir)))
    meta, real = store.meta(pid), store.load(ObservationSet, pid, consumer="experiment")
    shutil.rmtree(sdir / "ObservationSet" / pid)
    obs = ObservationSet(split=real.split, V=real.V, tokens=np.asarray(real.tokens),
                         sequence_id=np.asarray(real.sequence_id)[::-1].copy())
    new = store.save(obs, config=meta.config, parents=list(meta.parent_ids),
                     seed_map=dict(meta.seed_map), consumer="experiment")
    assert new == pid
    return new, store.meta(new).payload_sha256


def _old_ids_pool(root: Path) -> str:
    """A tiny old-ID reference ObservationSet in the fixture read root (no ID overlap)."""
    src = ArtifactStore(LocalFSBackend(root / "sources"))
    obs = ObservationSet(split="dev", V=3, tokens=np.zeros((4, 33), dtype=np.uint8),
                         sequence_id=(np.int64(1) << 40) + np.arange(4, dtype=np.int64))
    return src.save(obs, config={"fixture": "old-ids"}, parents=[], seed_map={},
                    consumer="experiment")


def _payload(store_root: Path, aid: str) -> Path:
    return store_root / "ObservationSet" / aid / "payload.npz"


def _mutate(path: Path) -> None:
    """Reverse every array's rows: still loadable and valid, different payload checksum."""
    with np.load(path, allow_pickle=False) as z:
        arrays = {k: np.ascontiguousarray(z[k][::-1]) for k in z.files}
    buf = io.BytesIO()
    np.savez(buf, **arrays)
    path.write_bytes(buf.getvalue())


def _watch(monkeypatch, target: Path, mutate: bool) -> dict:
    """Count backend reads of ``target``; with ``mutate``, change its bytes right after the first
    read returns (metadata untouched), i.e. after the stage has loaded it."""
    state = {"reads": 0}
    target = target.resolve()

    def get(self, key):
        data = _REAL_GET(self, key)
        if self._path(key).resolve() == target:
            state["reads"] += 1
            if mutate and state["reads"] == 1:
                _mutate(target)
        return data

    monkeypatch.setattr(LocalFSBackend, "get", get)
    return state


def _spy(monkeypatch, name: str, stop: bool = False) -> list:
    calls, real = [], getattr(x5g1t_stages_eval, name)

    def wrapped(*a, **k):
        calls.append(1)
        if stop:
            raise _Reached(name)
        return real(*a, **k)

    monkeypatch.setattr(x5g1t_stages_eval, name, wrapped)
    return calls


def _assert_no_result(root: Path, stage: str) -> None:
    assert not (_out(root, stage) / "result.json").exists()
    assert not (_out(root, stage) / "MANIFEST.json").exists()


# --- shared states -----------------------------------------------------------------------------

@pytest.fixture(scope="module")
def trained(tmp_path_factory):
    root = tmp_path_factory.mktemp("idev_trained") / "fx"
    cfg = load_config(build_fixture(root, sizes=SIZES, steps=2, bootstrap_draws=4))
    old = _old_ids_pool(root)
    with pytest.MonkeyPatch.context() as mp:
        seen = _watch(mp, _payload(root / "sources", old), mutate=False)
        x5g1t_stages.run_pools(cfg, REPO)
    for m in cfg.masters:
        for a in ARMS:
            x5g1t_stages.run_train(cfg, REPO, a, m)
    return root, old, seen["reads"]


@pytest.fixture(scope="module")
def dev_done(trained, tmp_path_factory):
    root = tmp_path_factory.mktemp("idev_dev") / "fx"
    cfg = _clone(trained[0], root)
    x5g1t_stages_eval.run_dev_analysis(cfg, REPO)
    return root, trained[1]


# --- §E.4 collision inputs in the pools stage --------------------------------------------------

def test_pools_collision_check_loads_the_old_id_store(trained):
    root, _, reads = trained
    assert reads >= 1, "the pools collision check never read the read-root ObservationSet"
    assert (_out(root, "pools") / "MANIFEST.json").exists()


def test_pools_read_root_payload_mutated_after_load_refused(tmp_path, monkeypatch):
    cfg = load_config(build_fixture(tmp_path, sizes=SIZES, steps=2, bootstrap_draws=4))
    old = _old_ids_pool(tmp_path)
    seen = _watch(monkeypatch, _payload(tmp_path / "sources", old), mutate=True)
    with pytest.raises(IntegrityFailed):
        x5g1t_stages.run_pools(cfg, REPO)
    assert seen["reads"] >= 1
    assert not (_out(tmp_path, "pools") / "pools.json").exists()
    assert not (_out(tmp_path, "pools") / "MANIFEST.json").exists()


# --- §E.3 dev-analysis -------------------------------------------------------------------------

def test_dev_analysis_control_reaches_oracle(trained, tmp_path, monkeypatch):
    cfg = _clone(trained[0], tmp_path / "fx")
    checks = _spy(monkeypatch, "validate_checkpoints")
    oracle = _spy(monkeypatch, "oracle_q32", stop=True)
    with pytest.raises(_Reached):
        x5g1t_stages_eval.run_dev_analysis(cfg, REPO)
    assert checks and oracle == [1]


DEV_SUBSTITUTIONS = {
    "dev_other_arm": lambda r: {f"dev:a0:{M1}": _existing(r, f"dev:a020:{M1}")},
    "train_other_arm": lambda r: {f"train:a0:{M1}": _existing(r, f"train:a020:{M1}")},
    "dev_other_master": lambda r: {f"dev:a020:{M2}": _existing(r, f"dev:a020:{M3}")},
    "dev_train_swapped": lambda r: {f"dev:a0:{M3}": _existing(r, f"train:a0:{M3}")},
    "dev_ids_reordered": lambda r: {f"dev:a020:{M3}": _reordered_ids(r, f"dev:a020:{M3}")},
}


@pytest.mark.parametrize("name", list(DEV_SUBSTITUTIONS))
def test_dev_analysis_mismatched_pool_never_scores(trained, tmp_path, monkeypatch, name):
    root = tmp_path / "fx"
    cfg = _clone(trained[0], root)
    _remap(root, cfg, DEV_SUBSTITUTIONS[name](root))
    calls = {n: _spy(monkeypatch, n) for n in ("validate_checkpoints", "oracle_q32", "regret_rows")}
    with pytest.raises(IntegrityFailed):
        x5g1t_stages_eval.run_dev_analysis(cfg, REPO)
    assert calls == {"validate_checkpoints": [], "oracle_q32": [], "regret_rows": []}
    _assert_no_result(root, "dev_analysis")


# --- §E.3 final-test, plus the test half of §E.5 -----------------------------------------------

def test_final_test_control_draws_and_records_test_provenance(dev_done, tmp_path, monkeypatch):
    src, old = dev_done
    root = tmp_path / "fx"
    cfg = _clone(src, root)
    seen = _watch(monkeypatch, _payload(root / "sources", old), mutate=False)
    draws = _spy(monkeypatch, "draw_pair")
    x5g1t_stages_eval.run_final_test(cfg, REPO, True)
    assert draws == [1]
    assert seen["reads"] >= 1, "the final-test collision check never read the old-ID store"
    result = json.loads((_out(root, "final_test") / "result.json").read_text(encoding="utf-8"))
    store = ArtifactStore(LocalFSBackend(root / "study" / "store"))
    assert set(result["test_pools"]) == set(ARMS)
    for arm, pid in result["test_pools"].items():
        meta = store.meta(pid)
        assert meta.config == {
            "role": "x5g1t-test", "lineage_protocol": "x5g1-train-v3",
            "execution_protocol": cfg.protocol, "arm": arm, "master": TEST_MASTER,
            "stream": "/".join(stream("test")), "namespace_code": CODES["test"]}
        assert tuple(meta.parent_ids) == tuple(sorted({cfg.sources["T"][arm][0],
                                                       cfg.sources["E"][0]}))


FINAL_SUBSTITUTIONS = {
    "train_other_arm": lambda r: {f"train:a0:{M1}": _existing(r, f"train:a020:{M1}")},
    "dev_other_master": lambda r: {f"dev:a0:{M2}": _existing(r, f"dev:a0:{M3}")},
    "train_ids_reordered": lambda r: {f"train:a020:{M3}": _reordered_ids(r, f"train:a020:{M3}")},
}


@pytest.mark.parametrize("name", list(FINAL_SUBSTITUTIONS))
def test_final_test_prerequisite_identity_failure_never_draws(dev_done, tmp_path, monkeypatch,
                                                              name):
    root = tmp_path / "fx"
    cfg = _clone(dev_done[0], root)
    _remap(root, cfg, FINAL_SUBSTITUTIONS[name](root))
    draws = _spy(monkeypatch, "draw_pair")
    checks = _spy(monkeypatch, "validate_checkpoints")
    with pytest.raises(IntegrityFailed):
        x5g1t_stages_eval.run_final_test(cfg, REPO, True)
    assert draws == [] and checks == []
    _assert_no_result(root, "final_test")


# --- §E.4 collision inputs in final-test -------------------------------------------------------

@pytest.mark.parametrize("target", ["read_root_old_ids", f"train:a0:{M1}", f"dev:a020:{M2}"])
def test_final_test_collision_input_mutated_after_load_refused(dev_done, tmp_path, monkeypatch,
                                                               target):
    """The collision check runs before the fresh draw (§D), so the bytes are changed when the
    draw starts: after the collision load, before the result export."""
    src, old = dev_done
    root = tmp_path / "fx"
    cfg = _clone(src, root)
    path = (_payload(root / "sources", old) if target == "read_root_old_ids"
            else _payload(root / "study" / "store", _pools(root)["pools"][target]))
    seen = _watch(monkeypatch, path, mutate=False)
    at_draw, real = [], x5g1t_stages_eval.draw_pair

    def draw(*a, **k):
        at_draw.append(seen["reads"])
        _mutate(path)
        return real(*a, **k)

    monkeypatch.setattr(x5g1t_stages_eval, "draw_pair", draw)
    with pytest.raises(IntegrityFailed):
        x5g1t_stages_eval.run_final_test(cfg, REPO, True)
    assert len(at_draw) == 1 and at_draw[0] >= 1, "input not loaded before the draw"
    _assert_no_result(root, "final_test")
