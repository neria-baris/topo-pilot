"""Author B, round 2: API §14.1 and coordinator ruling R19 (API §15). The H1 checkpoint-meta
identity check: `expected_meta` from CONTRACT (payload_sha256 from
checkpoints[j].meta_payload_sha256, never None), `check_checkpoint_meta` with exact,
type-strict comparisons (`==` plus `type(...) is` for ints; a list run_key is never equal to a
tuple), and `checkpoint_meta`, which reads <root>/Checkpoint/<id>/meta.json and nothing else.

Synthetic Checkpoint directories under tmp_path only; no checkpoint, payload or state is loaded.
Field names in `mismatches`/`checked` are not pinned; they are matched by substring."""

from __future__ import annotations

import builtins
import copy
import io
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import numpy as np  # noqa: E402
import pytest  # noqa: E402

import k4b_config  # noqa: E402
import k4b_driver  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

IDENTITY = "FAIL_TECHNICAL/IDENTITY"
MODELS = (1729, 2718, 3141)
LABELS = ("step5000", "step0")
CASES = [(j, s) for j in MODELS for s in LABELS]
CK = k4b_config.CONTRACT["checkpoints"]
RUN_KEY = k4b_config.CONTRACT["run_key"]
ORDER = ("artifact_id", "artifact_type", "run_key", "step", "status", "seed", "payload")
FORBIDDEN = {"payload.npz", "state.pt", "extra.json"}

# R19: the six meta payload_sha256 values bound in CONTRACT (copied here as an independent check)
PAYLOAD = {
    (1729, "step5000"): "bcd024efc2ff30f76940d459dba95a693f536fb7cc3b2441c4ee5145dcf8596b",
    (1729, "step0"): "d49284f57b8d3194b0ef8667624b2181252977567683e9c541bc689e75740922",
    (2718, "step5000"): "48c5b743d0c500aa4d14c4f40e1b5f115a8421af01e6a383b1927ce006f05efc",
    (2718, "step0"): "ffe2fb57af77d7acd8addc208681f4cea7a0814671502828e77a0176f18ad4d1",
    (3141, "step5000"): "ac7cff661c45bdba1e2fd13d668332bc58866715d9d4d475ec5af76c0814e062",
    (3141, "step0"): "9defde302fb3d57443f6a95c24a0a2608184af6b8738f3cb3695e9282bbd8cbb",
}
IDS = {(1729, "step5000"): "c3358e3cb9c352fb", (1729, "step0"): "bd8813115bbd970b",
       (2718, "step5000"): "98b0e703a337d513", (2718, "step0"): "5e6e6b7c446907f9",
       (3141, "step5000"): "036b670743ffbbaf", (3141, "step0"): "995f11b1120ccb36"}
SEEDS = {1729: 1959191081547677733, 2718: 1650155370212577495, 3141: 7028749409156379047}
STEP = {"step5000": 5000, "step0": 0}


def seed_key(j) -> str:
    return f"init/cylinder/O/{j}"


def good_meta(j, label) -> dict:
    """A meta.json as ArtifactStore writes it (extra keys included), built from the literals."""
    return {"artifact_type": "Checkpoint", "artifact_id": IDS[(j, label)],
            "schema_version": "1.0", "parent_ids": ["3633ac27dab50cf4"],
            "config": {"run_key": ["cylinder", "O", j], "step": STEP[label], "lr": 0.001},
            "seed_map": {seed_key(j): SEEDS[j], "data/train": 11},
            "producer_version": "abc123", "created_utc": "2026-10-01T00:00:00+00:00",
            "shapes": {}, "dtypes": {}, "payload_sha256": PAYLOAD[(j, label)],
            "status": "complete", "consumer": "learner"}


def check(meta, j=1729, label="step5000") -> dict:
    return k4b_driver.check_checkpoint_meta(meta, k4b_driver.expected_meta(j, label))


def only_mismatch(res, token) -> dict:
    assert res["status"] == IDENTITY, res
    assert len(res["mismatches"]) == 1, res
    mm = res["mismatches"][0]
    assert {"field", "expected", "found"} <= set(mm)
    assert token in str(mm["field"]), mm
    return mm


def set_at(meta, path, value) -> dict:
    d = meta
    for key in path[:-1]:
        d = d[key]
    d[path[-1]] = value
    return meta


def del_at(meta, path) -> dict:
    d = meta
    for key in path[:-1]:
        d = d[key]
    del d[path[-1]]
    return meta


# --------------------------------------------------------------------- expected_meta (R19)

@pytest.mark.parametrize("j,label", CASES)
def test_expected_meta_from_contract(j, label):
    exp = k4b_driver.expected_meta(j, label)
    assert set(exp) == {"artifact_id", "artifact_type", "run_key", "step", "status",
                        "init_seed_key", "init_seed", "payload_sha256"}
    assert exp["artifact_id"] == IDS[(j, label)] == CK[str(j)][label]
    assert exp["artifact_type"] == "Checkpoint"
    assert type(exp["run_key"]) is list and exp["run_key"] == [RUN_KEY[0], RUN_KEY[1], j]
    assert type(exp["run_key"][2]) is int
    assert type(exp["step"]) is int and exp["step"] == STEP[label]
    assert exp["status"] == "complete"
    assert exp["init_seed_key"] == seed_key(j)
    assert type(exp["init_seed"]) is int and exp["init_seed"] == SEEDS[j]


@pytest.mark.parametrize("j,label", CASES)
def test_expected_payload_sha_is_bound_never_none(j, label):
    exp = k4b_driver.expected_meta(j, label)
    assert exp["payload_sha256"] is not None
    assert isinstance(exp["payload_sha256"], str)
    assert exp["payload_sha256"] == PAYLOAD[(j, label)]
    assert exp["payload_sha256"] == CK[str(j)]["meta_payload_sha256"][label]


@pytest.mark.parametrize("j,label", [(1234, "step5000"), (1729, "step100"), (1729, "emission")])
def test_expected_meta_unknown_model_or_label_raises(j, label):
    with pytest.raises(Exception):
        k4b_driver.expected_meta(j, label)


# -------------------------------------------------------------- check_checkpoint_meta (§14.1)

@pytest.mark.parametrize("j,label", CASES)
def test_contract_meta_passes_and_check_is_pure(j, label, monkeypatch):
    exp = k4b_driver.expected_meta(j, label)
    meta = good_meta(j, label)
    before = copy.deepcopy(meta)

    def no_file(*args, **kwargs):
        raise AssertionError("check_checkpoint_meta is pure and opens no file")

    monkeypatch.setattr(builtins, "open", no_file)
    monkeypatch.setattr(io, "open", no_file)
    res = k4b_driver.check_checkpoint_meta(meta, exp)
    monkeypatch.undo()
    assert res["status"] == "PASS" and res["mismatches"] == []
    assert meta == before
    checked = [str(f) for f in res["checked"]]
    assert len(checked) == 7
    pos = [next(i for i, f in enumerate(checked) if tok in f) for tok in ORDER]
    assert pos == sorted(pos) and len(set(pos)) == 7


VALUE_CASES = [
    ("artifact_id", ("artifact_id",), lambda s: IDS[(2718, s)]),
    ("artifact_type", ("artifact_type",), lambda s: "ObservationSet"),
    ("run_key", ("config", "run_key"), lambda s: ["square", "O", 1729]),
    ("run_key", ("config", "run_key"), lambda s: ["cylinder", "B", 1729]),
    ("run_key", ("config", "run_key"), lambda s: ["cylinder", "O", 2718]),
    ("run_key", ("config", "run_key"), lambda s: ["cylinder", "O"]),
    ("step", ("config", "step"), lambda s: 0 if s == "step5000" else 5000),
    ("step", ("config", "step"), lambda s: 4999),
    ("status", ("status",), lambda s: "incomplete"),
    ("seed", ("seed_map", seed_key(1729)), lambda s: SEEDS[2718]),
    ("seed", ("seed_map", seed_key(1729)), lambda s: SEEDS[1729] + 1),
    ("payload", ("payload_sha256",), lambda s: PAYLOAD[(1729, "step0" if s == "step5000"
                                                           else "step5000")]),
    ("payload", ("payload_sha256",), lambda s: PAYLOAD[(1729, s)].upper()),
    ("payload", ("payload_sha256",), lambda s: PAYLOAD[(2718, s)]),
    ("payload", ("payload_sha256",), lambda s: PAYLOAD[(1729, s)] + " "),
]


@pytest.mark.parametrize("label", LABELS)
@pytest.mark.parametrize("token,path,value", VALUE_CASES)
def test_single_field_value_mismatch_is_identity(token, path, value, label):
    exp = k4b_driver.expected_meta(1729, label)
    bad = value(label)
    res = k4b_driver.check_checkpoint_meta(set_at(good_meta(1729, label), path, bad), exp)
    mm = only_mismatch(res, token)
    assert mm["found"] == bad


TYPE_CASES = [
    ("step", ("config", "step"), lambda s: str(STEP[s]), LABELS),
    ("step", ("config", "step"), lambda s: float(STEP[s]), LABELS),
    ("step", ("config", "step"), lambda s: np.int64(STEP[s]), LABELS),
    ("step", ("config", "step"), lambda s: False, ("step0",)),
    ("run_key", ("config", "run_key"), lambda s: ["cylinder", "O", "1729"], LABELS),
    ("run_key", ("config", "run_key"), lambda s: ("cylinder", "O", 1729), LABELS),
    ("run_key", ("config", "run_key"), lambda s: ["cylinder", "O", 1729.0], LABELS),
    ("run_key", ("config", "run_key"), lambda s: ["cylinder", "O", np.int64(1729)], LABELS),
    ("seed", ("seed_map", seed_key(1729)), lambda s: str(SEEDS[1729]), LABELS),
    ("seed", ("seed_map", seed_key(1729)), lambda s: np.int64(SEEDS[1729]), LABELS),
    ("payload", ("payload_sha256",), lambda s: PAYLOAD[(1729, s)].encode(), LABELS),
    ("artifact_id", ("artifact_id",), lambda s: [IDS[(1729, s)]], LABELS),
]


@pytest.mark.parametrize("token,path,value,labels", TYPE_CASES)
def test_wrong_type_follows_pinned_strictness(token, path, value, labels):
    for label in labels:
        res = check(set_at(good_meta(1729, label), path, value(label)), 1729, label)
        only_mismatch(res, token)


MISSING = [
    ("artifact_id", ("artifact_id",)),
    ("artifact_type", ("artifact_type",)),
    ("run_key", ("config", "run_key")),
    ("step", ("config", "step")),
    ("status", ("status",)),
    ("seed", ("seed_map", seed_key(1729))),
    ("seed", ("seed_map",)),
    ("payload", ("payload_sha256",)),
]


@pytest.mark.parametrize("token,path", MISSING)
def test_missing_key_is_a_mismatch_not_an_exception(token, path):
    res = check(del_at(good_meta(1729, "step5000"), path))
    only_mismatch(res, token)


def test_missing_config_fails_run_key_and_step():
    res = check(del_at(good_meta(1729, "step0"), ("config",)), 1729, "step0")
    assert res["status"] == IDENTITY
    fields = " ".join(str(m["field"]) for m in res["mismatches"])
    assert "run_key" in fields and "step" in fields
    assert len(res["mismatches"]) == 2


def test_other_models_meta_fails_on_every_model_bound_field():
    """2718's complete meta checked against 1729's expectation: id, run_key, seed, payload."""
    res = check(good_meta(2718, "step5000"), 1729, "step5000")
    assert res["status"] == IDENTITY
    fields = [str(m["field"]) for m in res["mismatches"]]
    for tok in ("artifact_id", "run_key", "payload"):
        assert any(tok in f for f in fields), fields
    # the seed entry of 1729 is absent from 2718's seed_map: a missing key is a mismatch
    assert any("seed" in f for f in fields), fields
    assert not any("artifact_type" in f or "status" in f for f in fields)


def test_several_mismatches_are_all_reported_in_checked_order():
    meta = good_meta(3141, "step0")
    meta["payload_sha256"] = PAYLOAD[(3141, "step5000")]
    meta["artifact_id"] = IDS[(3141, "step5000")]
    res = check(meta, 3141, "step0")
    assert res["status"] == IDENTITY
    fields = [str(m["field"]) for m in res["mismatches"]]
    assert len(fields) == 2
    assert "artifact_id" in fields[0] and "payload" in fields[1]
    assert res["mismatches"][0]["expected"] == IDS[(3141, "step0")]
    assert res["mismatches"][1]["expected"] == PAYLOAD[(3141, "step0")]


def test_trained_meta_against_step0_expectation_fails():
    res = check(good_meta(1729, "step5000"), 1729, "step0")
    fields = " ".join(str(m["field"]) for m in res["mismatches"])
    assert res["status"] == IDENTITY
    assert "artifact_id" in fields and "step" in fields and "payload" in fields


# ------------------------------------------------------------------- checkpoint_meta (§14.1)

def ck_dir(root: Path, aid: str) -> Path:
    d = root / "Checkpoint" / aid
    d.mkdir(parents=True, exist_ok=True)
    return d


def with_payload_files(d: Path) -> None:
    np.savez(d / "payload.npz", w=np.zeros(3))
    (d / "state.pt").write_bytes(b"\x80\x02not-a-real-state")
    (d / "extra.json").write_text("{}", encoding="utf-8")


def guard_payload(monkeypatch, seen: list) -> None:
    real = builtins.open

    def spy(file, *args, **kwargs):
        if isinstance(file, (str, bytes, os.PathLike)):
            name = Path(os.fsdecode(os.fspath(file))).name
            seen.append(name)
            if name in FORBIDDEN:
                raise AssertionError(f"checkpoint_meta opened {name}")
        return real(file, *args, **kwargs)

    def no_load(*args, **kwargs):
        raise AssertionError("checkpoint_meta called np.load")

    monkeypatch.setattr(builtins, "open", spy)
    monkeypatch.setattr(io, "open", spy)
    monkeypatch.setattr(np, "load", no_load)


@pytest.mark.parametrize("j,label", CASES)
def test_checkpoint_meta_reads_meta_json_only(tmp_path, monkeypatch, j, label):
    root = tmp_path / "artifacts"
    d = ck_dir(root, IDS[(j, label)])
    meta = good_meta(j, label)
    (d / "meta.json").write_text(json.dumps(meta, sort_keys=True, indent=1), encoding="utf-8")
    with_payload_files(d)
    seen: list = []
    guard_payload(monkeypatch, seen)
    got = k4b_driver.checkpoint_meta(root, IDS[(j, label)])
    monkeypatch.undo()
    assert got == meta
    assert not FORBIDDEN & set(seen)
    res = k4b_driver.check_checkpoint_meta(got, k4b_driver.expected_meta(j, label))
    assert res["status"] == "PASS"


@pytest.mark.parametrize("case", ["missing_dir", "missing_file", "empty", "truncated",
                                  "not_json", "bad_utf8", "is_directory"])
def test_checkpoint_meta_unreadable_or_malformed_is_identity(tmp_path, monkeypatch, case):
    root = tmp_path / "artifacts"
    aid = IDS[(1729, "step5000")]
    if case != "missing_dir":
        d = ck_dir(root, aid)
        with_payload_files(d)
        text = json.dumps(good_meta(1729, "step5000"))
        payload = {"empty": b"", "truncated": text[: len(text) // 2].encode(),
                   "not_json": b"meta: complete\n", "bad_utf8": b"\xff\xfe{\x00\x80"}
        if case in payload:
            (d / "meta.json").write_bytes(payload[case])
        elif case == "is_directory":
            (d / "meta.json").mkdir()
    seen: list = []
    guard_payload(monkeypatch, seen)
    with pytest.raises(C1GateFailure) as exc:
        k4b_driver.checkpoint_meta(root, aid)
    monkeypatch.undo()
    assert exc.value.status == IDENTITY
    assert not FORBIDDEN & set(seen)


def test_checkpoint_meta_reads_the_named_id_only(tmp_path):
    root = tmp_path / "artifacts"
    for (j, label), aid in IDS.items():
        ck_dir(root, aid).joinpath("meta.json").write_text(json.dumps(good_meta(j, label)),
                                                            encoding="utf-8")
    got = k4b_driver.checkpoint_meta(root, IDS[(2718, "step0")])
    assert got["artifact_id"] == IDS[(2718, "step0")]
    assert got["payload_sha256"] == PAYLOAD[(2718, "step0")]


def test_json_str_step_on_disk_fails_identity(tmp_path):
    root = tmp_path / "artifacts"
    meta = good_meta(3141, "step5000")
    meta["config"]["step"] = "5000"
    ck_dir(root, IDS[(3141, "step5000")]).joinpath("meta.json").write_text(
        json.dumps(meta), encoding="utf-8")
    got = k4b_driver.checkpoint_meta(root, IDS[(3141, "step5000")])
    only_mismatch(check(got, 3141, "step5000"), "step")
