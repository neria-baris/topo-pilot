"""Independent pool input-identity regressions for X5 G1 API v4.1 (§A, §B, §D; §E items 1, 2, 5).

Written from the contract only (test writer G, job 0011): the actual ``pools`` and ``train``
stages on a tiny SYNTHETIC fixture. Every substituted pool is a real, checksum-valid
``ObservationSet`` in the study store, and every ``pools.json`` edit carries a recomputed
COMPLETE manifest, so only the identity checks can refuse it.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import ArtifactStore, LocalFSBackend, ObservationSet
from topo_pilot.experiment import x5g1t_stages
from topo_pilot.experiment.x4b import ReadThroughBackend
from topo_pilot.experiment.x5g1t_checks import IntegrityFailed, validate_pool
from topo_pilot.experiment.x5g1t_config import load_config, read_chain
from topo_pilot.experiment.x5g1t_fixture import build_fixture
from topo_pilot.experiment.x5g1t_lineage import (
    CODES,
    MASTERS,
    PROTOCOL,
    pool_config,
    sequence_ids,
    stream,
    study_pool_config,
)
from topo_pilot.experiment.x5g1t_main import main

pytestmark = pytest.mark.experiment

REPO = Path(__file__).resolve().parents[2]
SIZES = {"train": 8, "dev": 4, "test": 4}
M1, M2 = MASTERS[0], MASTERS[1]
V = 3  # the fixture emission's symbol count


class _Reached(Exception):
    """Raised by a spy: the stage got past every check to the guarded call."""


# --- helpers -----------------------------------------------------------------------------------

def _clone(src: Path, dst: Path) -> Path:
    """Copy a fixture root and re-point its config's absolute paths at the copy."""
    shutil.copytree(src, dst)
    cfg_path = dst / "study_config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    def fix(v):
        if isinstance(v, str):
            return v.replace(str(src), str(dst))
        if isinstance(v, list):
            return [fix(x) for x in v]
        if isinstance(v, dict):
            return {k: fix(x) for k, x in v.items()}
        return v

    for key in ("read_roots", "study_root", "ledger_path", "mailbox"):
        cfg[key] = fix(cfg[key])
    cfg_path.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    return cfg_path


def _out(root: Path, *parts: str) -> Path:
    return root / "study" / "tables" / Path(*parts)


def _pools(root: Path) -> dict:
    return json.loads((_out(root, "pools") / "pools.json").read_text(encoding="utf-8"))


def _store(root: Path) -> ArtifactStore:
    """Writes into the study store; parents resolve through the fixture's read root."""
    return ArtifactStore(ReadThroughBackend(read_chain([root / "sources"]),
                                            LocalFSBackend(root / "study" / "store")))


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


def _existing(root: Path, key: str) -> tuple[str, str]:
    p = _pools(root)
    return p["pools"][key], p["pool_sha256"][key]


def _resave(root: Path, key: str, *, config=None, parents=None, obs=None) -> tuple[str, str]:
    """Save a checksum-valid variant of pool ``key``. With only ``obs`` changed the artifact id
    is unchanged, so the original is removed first and the variant takes its place."""
    store = _store(root)
    pid = _pools(root)["pools"][key]
    meta = store.meta(pid)
    if config is None and parents is None:
        shutil.rmtree(root / "study" / "store" / "ObservationSet" / pid)
        assert obs is not None
    real = obs if obs is not None else ArtifactStore(
        LocalFSBackend(root / "study" / "store")).load(ObservationSet, pid, consumer="experiment")
    new = store.save(real, config=meta.config if config is None else config,
                     parents=list(meta.parent_ids if parents is None else parents),
                     seed_map=dict(meta.seed_map), consumer="experiment")
    return new, store.meta(new).payload_sha256


def _expected_config(split: str, arm: str, master, protocol: str) -> dict:
    """§A, written out literally."""
    return {"role": f"x5g1t-{split}", "lineage_protocol": "x5g1-train-v3",
            "execution_protocol": protocol, "arm": arm, "master": master,
            "stream": "/".join(stream(split)), "namespace_code": CODES[split]}


def _parents(cfg, arm: str) -> tuple:
    return tuple(sorted({cfg.sources["T"][arm][0], cfg.sources["E"][0]}))


def _train_spy(monkeypatch) -> list:
    calls = []

    def spy(*a, **k):
        calls.append(tuple(a[1:3]))
        raise _Reached("train_one reached")

    monkeypatch.setattr(x5g1t_stages, "train_one", spy)
    return calls


def _assert_no_train_export(root: Path, arm: str, master) -> None:
    out = _out(root, "train", f"{arm}_{master}")
    assert not (out / "outcome.json").exists()
    assert not (out / "MANIFEST.json").exists()


# --- shared state ------------------------------------------------------------------------------

@pytest.fixture(scope="module")
def pools_root(tmp_path_factory) -> Path:
    root = tmp_path_factory.mktemp("id_pools") / "fx"
    cfg = load_config(build_fixture(root, sizes=SIZES, steps=2, bootstrap_draws=4))
    x5g1t_stages.run_pools(cfg, REPO)
    return root


@pytest.fixture
def clone(pools_root, tmp_path):
    root = tmp_path / "fx"
    return root, load_config(_clone(pools_root, root))


# --- §E.1 root wrong-arm substitution ----------------------------------------------------------

def test_untouched_fixture_reaches_train_one_with_intended_pools(clone, monkeypatch):
    root, cfg = clone
    calls = _train_spy(monkeypatch)
    with pytest.raises(_Reached):
        x5g1t_stages.run_train(cfg, REPO, "a0", M1)
    p = _pools(root)["pools"]
    assert calls == [(p[f"train:a0:{M1}"], p[f"dev:a0:{M1}"])]


def test_root_wrong_arm_train_pool_refused_before_train_one(clone, monkeypatch):
    root, cfg = clone
    _remap(root, cfg, {f"train:a0:{M1}": _existing(root, f"train:a020:{M1}")})
    calls = _train_spy(monkeypatch)
    with pytest.raises(IntegrityFailed):
        x5g1t_stages.run_train(cfg, REPO, "a0", M1)
    assert calls == []
    _assert_no_train_export(root, "a0", M1)


def test_root_wrong_arm_cli_exits_3(clone, monkeypatch):
    root, cfg = clone
    _remap(root, cfg, {f"train:a0:{M1}": _existing(root, f"train:a020:{M1}")})
    calls = _train_spy(monkeypatch)
    rc = main(["--config", str(root / "study_config.json"), "--repo", str(REPO),
               "train", "--arm", "a0", "--master", str(M1)])
    assert rc == 3
    assert calls == []
    _assert_no_train_export(root, "a0", M1)


# --- §E.2 other checksum-valid substitutions ---------------------------------------------------

def _swap_train_dev(root, cfg):
    return {f"train:a0:{M1}": _existing(root, f"dev:a0:{M1}"),
            f"dev:a0:{M1}": _existing(root, f"train:a0:{M1}")}


def _cfg_variant(edit):
    def make(root, cfg):
        c = _expected_config("train", "a0", M1, cfg.protocol)
        edit(c)
        return {f"train:a0:{M1}": _resave(root, f"train:a0:{M1}", config=c)}
    return make


def _parents_variant(pick):
    def make(root, cfg):
        return {f"train:a0:{M1}": _resave(root, f"train:a0:{M1}", parents=pick(cfg))}
    return make


def _obs_variant(edit):
    def make(root, cfg):
        ids = sequence_ids("train", "a0", M1, SIZES["train"])
        real = ArtifactStore(LocalFSBackend(root / "study" / "store")).load(
            ObservationSet, _pools(root)["pools"][f"train:a0:{M1}"], consumer="experiment")
        kw = dict(split="train", V=V, sequence_id=ids, tokens=np.asarray(real.tokens))
        edit(kw)
        obs = ObservationSet(**kw)
        obs.validate()
        return {f"train:a0:{M1}": _resave(root, f"train:a0:{M1}", obs=obs)}
    return make


SUBSTITUTIONS = {
    "other_master": lambda r, c: {f"train:a0:{M1}": _existing(r, f"train:a0:{M2}")},
    "train_dev_swapped": _swap_train_dev,
    "dev_other_arm": lambda r, c: {f"dev:a0:{M1}": _existing(r, f"dev:a020:{M1}")},
    "dev_other_master": lambda r, c: {f"dev:a0:{M1}": _existing(r, f"dev:a0:{M2}")},
    "parents_other_arm_kernel": _parents_variant(
        lambda c: [c.sources["T"]["a020"][0], c.sources["E"][0]]),
    "parents_extra": _parents_variant(
        lambda c: [c.sources["T"]["a0"][0], c.sources["T"]["a020"][0], c.sources["E"][0]]),
    "parents_missing_E": _parents_variant(lambda c: [c.sources["T"]["a0"][0]]),
    "cfg_role": _cfg_variant(lambda c: c.update(role="x5g1t-dev")),
    "cfg_lineage_protocol": _cfg_variant(lambda c: c.update(lineage_protocol="x5g1-train-v2")),
    "cfg_execution_protocol": _cfg_variant(lambda c: c.update(execution_protocol="x5g1-train-v4")),
    "cfg_stream": _cfg_variant(lambda c: c.update(stream="/".join(stream("dev")))),
    "cfg_namespace_code": _cfg_variant(lambda c: c.update(namespace_code=CODES["dev"])),
    "cfg_arm": _cfg_variant(lambda c: c.update(arm="a020")),
    "cfg_master_as_string": _cfg_variant(lambda c: c.update(master=str(M1))),
    "cfg_extra_key": _cfg_variant(lambda c: c.update(note="extra")),
    "cfg_bare_protocol_key": _cfg_variant(lambda c: c.update(protocol=PROTOCOL)),
    "cfg_missing_key": _cfg_variant(lambda c: c.pop("execution_protocol")),
    "cfg_legacy_pool_config": lambda r, c: {f"train:a0:{M1}": _resave(
        r, f"train:a0:{M1}", config=pool_config("train", "a0", M1))},
    "ids_reordered": _obs_variant(lambda kw: kw.update(sequence_id=kw["sequence_id"][::-1].copy())),
    "ids_other_master": _obs_variant(
        lambda kw: kw.update(sequence_id=sequence_ids("train", "a0", M2, SIZES["train"]))),
    "ids_other_arm": _obs_variant(
        lambda kw: kw.update(sequence_id=sequence_ids("train", "a020", M1, SIZES["train"]))),
    "wrong_V": _obs_variant(lambda kw: kw.update(V=V + 1)),
    "wrong_layout": _obs_variant(lambda kw: kw.update(layout_version="2")),
    "wrong_split_field": _obs_variant(lambda kw: kw.update(split="dev")),
    "wrong_row_count": _obs_variant(lambda kw: kw.update(sequence_id=kw["sequence_id"][:-1],
                                                         tokens=kw["tokens"][:-1])),
}


@pytest.mark.parametrize("name", list(SUBSTITUTIONS))
def test_valid_substitution_refused_before_train_one(clone, monkeypatch, name):
    root, cfg = clone
    _remap(root, cfg, SUBSTITUTIONS[name](root, cfg))
    calls = _train_spy(monkeypatch)
    with pytest.raises(IntegrityFailed):
        x5g1t_stages.run_train(cfg, REPO, "a0", M1)
    assert calls == []
    _assert_no_train_export(root, "a0", M1)


def test_obs_variant_helper_is_a_faithful_copy(clone, monkeypatch):
    """Control for the content variants: a re-save with nothing changed still trains."""
    root, cfg = clone
    _remap(root, cfg, _obs_variant(lambda kw: None)(root, cfg))
    calls = _train_spy(monkeypatch)
    with pytest.raises(_Reached):
        x5g1t_stages.run_train(cfg, REPO, "a0", M1)
    assert len(calls) == 1


# --- §B validate_pool directly -----------------------------------------------------------------

def test_validate_pool_accepts_intended_and_refuses_others(clone):
    root, cfg = clone
    store = _store(root)
    pid, sha = _existing(root, f"dev:a020:{M2}")
    got = validate_pool(store, pid, sha, cfg, "dev", "a020", M2, V)
    # The re-verification record (§B, §D): the artifact class and the payload checksum.
    assert got == {pid: (ObservationSet, sha)}
    for args in [("dev", "a0", M2, V), ("dev", "a020", M1, V), ("train", "a020", M2, V),
                 ("dev", "a020", M2, V + 1)]:
        with pytest.raises(IntegrityFailed):
            validate_pool(store, pid, sha, cfg, *args)
    with pytest.raises(IntegrityFailed):
        validate_pool(store, pid, "0" * 64, cfg, "dev", "a020", M2, V)


# --- §E.5 provenance mapping -------------------------------------------------------------------

def test_study_pool_config_is_exactly_section_a(clone):
    _, cfg = clone
    assert study_pool_config("train", "a0", M1, cfg.protocol) == {
        "role": "x5g1t-train", "lineage_protocol": "x5g1-train-v3",
        "execution_protocol": "x5g1-train-v4 SYNTHETIC FIXTURE", "arm": "a0", "master": M1,
        "stream": "x5g1-train-v1/train/cylinder/overlap/1.25", "namespace_code": 9}
    for split, arm, master in [("dev", "a020", M2), ("test", "a0", "shared")]:
        assert study_pool_config(split, arm, master, "x5g1-train-v4") == \
            _expected_config(split, arm, master, "x5g1-train-v4")


def test_new_pools_record_lineage_and_execution_protocol(pools_root):
    cfg = load_config(pools_root / "study_config.json")
    store = ArtifactStore(LocalFSBackend(pools_root / "study" / "store"))
    pools = _pools(pools_root)
    expected_keys = {f"{s}:{a}:{m}" for s in ("train", "dev") for a in ("a0", "a020")
                     for m in cfg.masters}
    assert set(pools["pools"]) == expected_keys
    for key, pid in pools["pools"].items():
        split, arm, m = key.split(":")
        meta = store.meta(pid)
        assert meta.config == _expected_config(split, arm, int(m), cfg.protocol), key
        assert meta.config["lineage_protocol"] == "x5g1-train-v3"
        assert meta.config["execution_protocol"] == cfg.protocol
        assert "protocol" not in meta.config
        assert tuple(meta.parent_ids) == _parents(cfg, arm)
        assert meta.payload_sha256 == pools["pool_sha256"][key]
