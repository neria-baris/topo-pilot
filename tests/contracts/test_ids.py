import hashlib
import json
import random

import numpy as np
import pytest

from topo_pilot.contracts import (ErrorCode, SCHEMA_VERSION, SeedTree, StageFailure,
                                  canonical_json, make_artifact_id)

pytestmark = pytest.mark.contracts

CFG = {"b": 1, "a": {"y": 0.5, "x": [1, 2], "z": {"q": "s", "p": None}}, "c": 0.1}


def _shuffled(d, rng):
    items = list(d.items())
    rng.shuffle(items)
    return {k: (_shuffled(v, rng) if isinstance(v, dict) else v) for k, v in items}


def test_C01_id_known_answer_and_shape():
    expected = hashlib.sha256(json.dumps(
        ["WorldSpec", CFG, ["p1", "p2"], SCHEMA_VERSION], sort_keys=True, separators=(",", ":"),
        ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
    got = make_artifact_id("WorldSpec", CFG, ["p2", "p1"])
    assert got == expected
    assert len(got) == 16 and int(got, 16) >= 0
    assert make_artifact_id("WorldSpec", CFG, ["p1", "p2"], SCHEMA_VERSION) == expected


def test_C01_id_independent_of_key_order():
    rng = random.Random(7)
    ref = make_artifact_id("T", CFG, ["x"])
    for _ in range(25):
        assert make_artifact_id("T", _shuffled(CFG, rng), ["x"]) == ref


def test_C01_id_independent_of_parent_order_and_container():
    assert make_artifact_id("T", CFG, ["a", "b", "c"]) == make_artifact_id("T", CFG, ("c", "a", "b"))


def test_C02_id_changes_with_each_input():
    base = make_artifact_id("T", CFG, ["a"], "1.0.0")
    cfg2 = json.loads(json.dumps(CFG))
    cfg2["a"]["z"]["q"] = "t"  # nested change
    cfg3 = dict(CFG, extra=1)
    cfg4 = dict(CFG, c=0.1000001)
    ids = {base,
           make_artifact_id("T", cfg2, ["a"], "1.0.0"),
           make_artifact_id("T", cfg3, ["a"], "1.0.0"),
           make_artifact_id("T", cfg4, ["a"], "1.0.0"),
           make_artifact_id("T", CFG, ["b"], "1.0.0"),
           make_artifact_id("T", CFG, ["a", "b"], "1.0.0"),
           make_artifact_id("T", CFG, [], "1.0.0"),
           make_artifact_id("T", CFG, ["a"], "1.0.1"),
           make_artifact_id("T", CFG, ["a"], "2.0.0"),
           make_artifact_id("U", CFG, ["a"], "1.0.0")}
    assert len(ids) == 10


def test_C03_canonical_json_known_answers():
    assert canonical_json({"b": 1, "a": 2}) == '{"a":2,"b":1}'
    assert canonical_json({2: 1, 1: 2}) == '{"1":2,"2":1}'
    assert canonical_json({10: 1, 9: 2}) == '{"10":1,"9":2}'  # keys sorted after str()
    assert canonical_json({"a": {"d": 1, "c": [1, {"f": 1, "e": 2}]}}) == '{"a":{"c":[1,{"e":2,"f":1}],"d":1}}'
    assert canonical_json((1, 2)) == canonical_json([1, 2]) == "[1,2]"
    assert canonical_json({"t": (1, (2, 3))}) == canonical_json({"t": [1, [2, 3]]}) == '{"t":[1,[2,3]]}'
    assert canonical_json([True, False, None]) == "[true,false,null]"
    assert canonical_json("é") == '"é"'  # ensure_ascii=False
    assert canonical_json([]) == "[]" and canonical_json({}) == "{}"


def test_C03_canonical_json_floats_and_numpy():
    assert canonical_json(0.1) == "0.1"
    assert canonical_json(1.0) == "1.0"
    assert canonical_json(1e-7) == repr(1e-7)
    assert canonical_json(1e22) == repr(1e22)
    assert canonical_json(np.float32(0.1)) == "0.10000000149011612"
    assert canonical_json(np.float64(0.5)) == "0.5"
    assert canonical_json(np.int64(3)) == "3"
    assert canonical_json(np.int32(-4)) == "-4"
    assert canonical_json(np.bool_(True)) == "true"
    assert canonical_json(np.array([[1, 2], [3, 4]])) == "[[1,2],[3,4]]"
    assert canonical_json(np.array([0.5, 1.0])) == "[0.5,1.0]"
    assert canonical_json({"k": np.array([1, 2])}) == '{"k":[1,2]}'
    assert " " not in canonical_json({"a": [1, 2, {"b": 3.5}]})


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf"), np.float32("nan"),
                                 [1, {"a": float("nan")}], np.array([1.0, np.inf])])
def test_C03_canonical_json_rejects_nonfinite(bad):
    with pytest.raises(StageFailure) as ei:
        canonical_json(bad)
    assert ei.value.code == ErrorCode.INVALID_CONFIG


def _ref_seed(*a):
    text = json.dumps(list(a), separators=(",", ":"), ensure_ascii=False)
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:8], "big") & (2**63 - 1)


def test_C09_seed_known_answers():
    assert _ref_seed(1729, "init") == 1836043674253666241
    assert _ref_seed(1729, "train", 3) == 8928180980268890711
    assert SeedTree(1729).seed("init") == 1836043674253666241
    assert SeedTree(1729).seed("train", 3) == 8928180980268890711
    assert SeedTree(1729).seed("train", 4) == 2161881191223164821
    assert 0 <= SeedTree(1729).seed("init") < 2**63


def test_C09_seed_sensitivity():
    s = SeedTree(1729)
    vals = {s.seed("init"), s.seed("train"), s.seed("train", 3), s.seed("train", "3"),
            s.seed("train", 3, 0), SeedTree(1730).seed("init")}
    assert len(vals) == 6


def test_C10_generator_streams():
    t = SeedTree(1729)
    a1 = t.generator("data").integers(0, 2**32, 8)
    a2 = t.generator("data").integers(0, 2**32, 8)
    b = t.generator("model").integers(0, 2**32, 8)
    c = t.generator("data", 1).integers(0, 2**32, 8)
    d = SeedTree(1730).generator("data").integers(0, 2**32, 8)
    assert np.array_equal(a1, a2)
    for other in (b, c, d):
        assert not np.array_equal(a1, other)
    g = t.generator("data")
    assert isinstance(g, np.random.Generator) and isinstance(g.bit_generator, np.random.PCG64)
    expected = np.random.Generator(np.random.PCG64(t.seed("data"))).integers(0, 2**32, 8)
    assert np.array_equal(a1, expected)
