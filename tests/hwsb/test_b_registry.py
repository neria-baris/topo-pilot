"""Author B (job 0161), TEST_PLAN section 3 `test_b_registry.py`: B9a(i)/(ii) (history inventory
and the fail-closed registry reader, section 6.3; DRB13) and B9a(iii)/(iv) (the registry cap and
the sealed-alphabet predicate). A synthetic stage-B store under pytest tmp_path with the tiny
world; ObservationSets of two dry masters plus three hist blocks. tools/hwsb/*.py unread."""

from __future__ import annotations

import dataclasses
import hashlib
import shutil
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "tools" / "hwsb") not in sys.path:
    sys.path.insert(0, str(REPO / "tools" / "hwsb"))

import hwsb_config as hc  # noqa: E402
import hwsb_data as hd  # noqa: E402
import hwsb_dry as hdry  # noqa: E402
import hwsb_gates as hg  # noqa: E402
import k4b_data  # noqa: E402
import scores  # noqa: E402
from topo_pilot.contracts import ArtifactStore, LocalFSBackend, ObservationSet  # noqa: E402

REG = "FAIL_TECHNICAL/REGISTRY"
ROLES = ("LGATE", "CAL", "VAL")


def plan():
    base = hc.dry_plan("dry_tiny", "BREG")
    sizes = {"train": 256, "dev": 64, "LGATE": 128, "CAL": 96, "VAL": 96}
    return dataclasses.replace(base, sizes=sizes)


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    root = tmp_path_factory.mktemp("regbase") / "store"
    store = ArtifactStore(LocalFSBackend(root / "artifacts"))
    proc = hdry.build_tiny_process(store)
    pl = plan()
    expected, n_rows, obs_ids = [], 0, []
    for m in hc.DRY_MASTERS:
        ids = hd.make_train_dev(store, proc, m, pl)
        for split in ("train", "dev"):
            obs_ids.append(ids[split])
            tok = store.load(ObservationSet, ids[split], consumer="experiment").tokens
            canon = scores.canonical_from_named(tok[:, :32], proc["perm"][m])
            expected += scores.history_digests(canon)
            n_rows += tok.shape[0]
    blocks = {}
    for role in ROLES:
        blocks[role] = hd.make_block(proc, role, pl)
        hd.save_block(root, blocks[role])
        expected += list(blocks[role]["digest_canon32"])
        n_rows += len(blocks[role]["canon32"])
    return {"root": root, "proc": proc, "blocks": blocks, "digests": set(expected),
            "n_rows": n_rows, "obs_ids": obs_ids}


@pytest.fixture
def copy(base, tmp_path):
    dst = tmp_path / "store"
    shutil.copytree(base["root"], dst)
    return dst


def walk(root):
    out = {}
    for sub in ("artifacts/ObservationSet", "hist", "superseded"):
        for f in sorted((Path(root) / sub).rglob("*")):
            if f.is_file():
                out[f.relative_to(root).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


# ------------------------------------------------------------------ inventory
def test_history_inventory_lists_every_file_with_sha256(base):
    inv = hd.history_inventory(base["root"])
    assert inv == walk(base["root"])
    assert {f"hist/{r}.npz" for r in ROLES} <= set(inv)
    assert len([k for k in inv if k.startswith("artifacts/ObservationSet/")]) >= 4 * 2
    assert not any(k.startswith("artifacts/EmissionSpec") for k in inv)


def test_inventory_includes_superseded_tree(copy):
    (copy / "superseded" / "old1" / "hist").mkdir(parents=True)
    shutil.copyfile(copy / "hist" / "CAL.npz", copy / "superseded" / "old1" / "hist" / "CAL.npz")
    inv = hd.history_inventory(copy)
    assert "superseded/old1/hist/CAL.npz" in inv and inv == walk(copy)


# ------------------------------------------------------------------ reader passes
def test_registry_digests_pass_and_match_history_digests(base):
    inv = hd.history_inventory(base["root"])
    res = hd.registry_digests(base["root"], expected=inv)
    assert res["status"] == "PASS" and res["failures"] == []
    assert res["digests"] == base["digests"]
    assert res["n_rows"] == res["n_digests"] == base["n_rows"]
    kinds = sorted(s["kind"] for s in res["sources"])
    assert kinds == ["ObservationSet"] * 4 + ["hist"] * 3
    for s in res["sources"]:
        assert s["n_rows"] == s["n_digests"] and set(s) >= {"path", "kind", "n_rows", "n_digests"}


def test_registry_digests_without_expected_also_pass(base):
    res = hd.registry_digests(base["root"])
    assert res["status"] == "PASS" and res["digests"] == base["digests"]


def test_named_tokens_are_inverted_to_canonical(base):
    res = hd.registry_digests(base["root"])
    store = ArtifactStore(LocalFSBackend(base["root"] / "artifacts"))
    named = set()
    for oid in base["obs_ids"]:
        tok = store.load(ObservationSet, oid, consumer="experiment").tokens
        named |= set(scores.history_digests(tok[:, :32]))
    assert res["digests"] == base["digests"]
    assert not named <= base["digests"]  # digesting the named rows would give other values


def test_superseded_hist_is_read(copy):
    (copy / "superseded" / "old1" / "hist").mkdir(parents=True)
    shutil.copyfile(copy / "hist" / "VAL.npz", copy / "superseded" / "old1" / "hist" / "VAL.npz")
    inv = hd.history_inventory(copy)
    res = hd.registry_digests(copy, expected=inv)
    assert res["status"] == "PASS"
    assert any("superseded" in s["path"] for s in res["sources"] if s["kind"] == "hist")
    assert res["n_rows"] == res["n_digests"]


# ------------------------------------------------------------------ fail-closed defects
def test_missing_file_fails_closed(copy):
    inv = hd.history_inventory(copy)
    (copy / "hist" / "CAL.npz").unlink()
    res = hd.registry_digests(copy, expected=inv)
    assert res["status"] == REG and any("CAL" in f["path"] for f in res["failures"])


def test_renamed_hist_file_fails_closed(copy):
    inv = hd.history_inventory(copy)
    (copy / "hist" / "CAL.npz").rename(copy / "hist" / "CAL_renamed.npz")
    assert hd.registry_digests(copy, expected=inv)["status"] == REG
    assert hd.registry_digests(copy)["status"] == REG  # a name that is not a role is refused


def test_extra_unlisted_file_fails_closed(copy):
    inv = hd.history_inventory(copy)
    (copy / "superseded").mkdir()
    (copy / "superseded" / "note.txt").write_text("unlisted", encoding="utf-8")
    res = hd.registry_digests(copy, expected=inv)
    assert res["status"] == REG and any("note.txt" in f["path"] for f in res["failures"])


def test_unreadable_npz_fails_closed(copy):
    (copy / "hist" / "VAL.npz").write_bytes(b"not a zip archive")
    res = hd.registry_digests(copy)
    assert res["status"] == REG and any("VAL" in f["path"] for f in res["failures"])


def test_changed_byte_fails_closed(copy):
    inv = hd.history_inventory(copy)
    path = copy / "hist" / "LGATE.npz"
    path.write_bytes(path.read_bytes() + b"\x00")
    res = hd.registry_digests(copy, expected=inv)
    assert res["status"] == REG and any("LGATE" in f["path"] for f in res["failures"])


def test_observation_set_without_emission_parent_fails_closed(copy):
    shutil.rmtree(copy / "artifacts" / "EmissionSpec")
    res = hd.registry_digests(copy)
    assert res["status"] == REG and res["failures"]
    assert any("ObservationSet" in f["path"] for f in res["failures"])


# ------------------------------------------------------------------ B9a (iii), (iv)
def largest_passing_p(rows):
    cap = Fraction(1, 100)
    p = float(cap / rows)
    while Fraction(p) * rows > cap:
        p = float(np.nextafter(p, 0.0))
    while Fraction(float(np.nextafter(p, 1.0))) * rows <= cap:
        p = float(np.nextafter(p, 1.0))
    return p


def eval_blocks():
    rng = np.random.default_rng(9)
    out = {}
    for i, role in enumerate(ROLES):
        c = rng.integers(5, 36, size=(20, 32)).astype(np.uint8)
        c[: 3 + i] = rng.integers(0, 5, size=(3 + i, 32))  # planted all-{0..4} rows
        out[role] = {"canon32": c}
    return out


def test_b9a_registry_cap_boundary_is_exact(base):
    n_c = 3072
    rows = 3072 + 3072 + n_c
    p = largest_passing_p(rows)
    over = float(np.nextafter(p, 1.0))
    assert Fraction(p) * rows <= Fraction(1, 100) < Fraction(over) * rows
    ok = hg.b9a(base["root"], n_c, p, p, eval_blocks())
    assert ok["status"] == "PASS" and ok["value"] == str(Fraction(p) * rows)
    assert ok["inventory"] == walk(base["root"])
    bad = hg.b9a(base["root"], n_c, over, over, eval_blocks())
    assert bad["status"] == REG and bad["value"] == str(Fraction(over) * rows)


def test_b9a_uses_12288_style_row_count_and_reference_tolerance(base):
    rows = 3072 + 3072 + 12288
    p = largest_passing_p(rows)
    assert hg.b9a(base["root"], 12288, p, p, eval_blocks())["status"] == "PASS"
    drift = p * (1 + 1e-9)
    assert hg.b9a(base["root"], 12288, p, drift, eval_blocks())["status"] == REG
    near = hg.b9a(base["root"], 12288, p, p * (1 + 1e-13), eval_blocks())
    assert near["status"] == "PASS" and near["rel_diff"] == pytest.approx(1e-13, rel=0.5)


def test_b9a_registry_failure_gives_registry_status(copy):
    (copy / "hist" / "VAL.npz").write_bytes(b"junk")
    res = hg.b9a(copy, 3072, 1e-7, 1e-7, eval_blocks())
    assert res["status"] == REG


def test_predicate_hits_count_planted_alphabet_rows(base):
    blocks = eval_blocks()
    res = hg.b9a(base["root"], 3072, 1e-7, 1e-7, blocks)
    want = {r: int(np.all(blocks[r]["canon32"] <= 4, axis=1).sum()) for r in ROLES}
    assert res["predicate_hits"] == want == {"LGATE": 3, "CAL": 4, "VAL": 5}
    assert want == {r: int(k4b_data.sealed_d2a_predicate(blocks[r]["canon32"]).sum())
                    for r in ROLES}
    assert "digests" not in res["registry"]
