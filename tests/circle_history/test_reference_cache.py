"""Independent tests (author B) for reference_cache.py: TEST_PLAN item B12 (spec v2.4).

Written from API.md (spec v2.4 item 3), ERROR_BOUND.md v2.2 and TEST_PLAN.md only; no production
code was read. Caches are built by hand from exact Decimal strings; expected entries, identities
and hex encodings are recomputed here with hashlib and numpy.

Interpretations (reported): FEATURE_DIGITS = 80 and REF_DIGITS = 60 (the documented feature and
reference precisions); sha256 values are hex strings compared case-insensitively; a row record's
"panel" is a single int.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from decimal import Decimal
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_circle_history", "tools/x4_oracle_profile", "tests/oracle_profile"):
    if str(REPO_ROOT / _sub) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT / _sub))

import error_bound  # noqa: E402
import errors  # noqa: E402
import reference_cache  # noqa: E402

pytestmark = pytest.mark.analysis

T = np.array([[0.5, 0.5, 0.0], [0.25, 0.25, 0.5], [0.5, 0.0, 0.5]])
E = np.array([[0.5, 0.25, 0.25], [0.125, 0.625, 0.25], [0.25, 0.0, 0.75]])
PI = np.array([3 / 7, 2 / 7, 2 / 7])
COORDS = np.array([[0.0, 2.0], [3.0, 0.0], [7.0, 1.0]])
HIST = np.array([[r // 3, r % 3] + [(r + t * t) % 3 for t in range(2, 32)] for r in range(4)],
                dtype=np.int64)
SEQ = np.array([907, 15, 333, 48], dtype=np.int64)
HIDS = np.array(["c3a1", "07ff", "b2b2", "1e40"])
# moments with awkward exact decimal forms: trailing zeros, exponents, long expansions, signs
VALUES = [Decimal("0.10"), Decimal("-1E-30"), Decimal("0.333333333333333333333333333333333333"),
          Decimal("-0.5"), Decimal("1"), Decimal("2.5E-61"), Decimal("-0.000"), Decimal("0.7")]


def _sha_file(rel: str) -> str:
    return hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest()


def _hex(row) -> str:
    return np.asarray(row, dtype=np.int64).tobytes().hex()


@pytest.fixture(scope="module")
def ident() -> dict:
    return reference_cache.identity(T, E, PI, COORDS)


def _cache(digest: str, rows=range(4), ks=(4, 32)) -> dict:
    out, i = {}, 0
    for r in rows:
        for k in ks:
            out[(digest, k, np.asarray(HIST[r], dtype=np.int64).tobytes())] = (
                VALUES[i % len(VALUES)], VALUES[(i + 3) % len(VALUES)])
            i += 1
    return out


def _rows() -> list[dict]:
    return [{"model": 1729, "split": "calibration", "panel": 1, "history_id": HIDS[:2].tolist(),
             "sequence_id": SEQ[:2].tolist(), "history": [_hex(r) for r in HIST[:2]]},
            {"model": 1729, "split": "validation", "panel": 2, "history_id": HIDS[2:].tolist(),
             "sequence_id": SEQ[2:].tolist(), "history": [_hex(r) for r in HIST[2:]]}]


@pytest.fixture()
def obj(ident) -> dict:
    exported = reference_cache.export_cache(_cache(ident["process_digest"]), ident, _rows())
    return json.loads(json.dumps(exported))            # what a persisted file reloads as


def test_identity_fields(ident) -> None:
    assert reference_cache.SCHEMA == "x4-circle-reference-cache-v2"
    assert ident["process_digest"] == error_bound.process_digest(T, E, PI, COORDS)
    feats = error_bound.exact_features(np.arange(12).reshape(12, 1))
    text = "\n".join(f"{c}|{s}" for (c, s) in feats) + "|80|60"
    assert ident["feature_identity"].lower() == hashlib.sha256(text.encode()).hexdigest()
    src = ident["source_identity"]
    assert src["independent_reference"].lower() == _sha_file(
        "tests/oracle_profile/independent_reference.py")
    assert src["error_bound"].lower() == _sha_file("tools/x4_circle_history/error_bound.py")
    other = reference_cache.identity(T, E[[1, 0, 2]], PI, COORDS)
    assert other["process_digest"] != ident["process_digest"]
    assert other["feature_identity"] == ident["feature_identity"]


def test_export_entries_sorted_and_exact(ident) -> None:
    cache = _cache(ident["process_digest"])
    out = reference_cache.export_cache(cache, ident, _rows())
    assert out["schema"] == reference_cache.SCHEMA
    assert out["identity"] == ident and out["rows"] == _rows()
    want = [{"process_digest": d, "K": k, "history": b.hex(), "mx": str(mx), "my": str(my)}
            for (d, k, b), (mx, my) in sorted(cache.items())]
    assert [dict(e) for e in out["entries"]] == want


def test_round_trip_is_exact_without_float(ident, obj) -> None:
    cache = _cache(ident["process_digest"])
    loaded = reference_cache.load_cache(obj, ident)
    assert set(loaded) == set(cache)
    for key, (mx, my) in cache.items():
        got_x, got_y = loaded[key]
        assert isinstance(got_x, Decimal) and isinstance(got_y, Decimal)
        assert str(got_x) == str(mx) and str(got_y) == str(my)     # digits and exponent kept
        assert got_x.as_tuple() == mx.as_tuple() and got_y.as_tuple() == my.as_tuple()


def _mutations() -> dict:
    def set_schema(o):
        o["schema"] = "x4-circle-reference-cache-v1"

    def ident_field(path):
        def mutate(o):
            target = o["identity"]
            for p in path[:-1]:
                target = target[p]
            target[path[-1]] = "0" * 64
        return mutate

    def other_digest(o):
        o["entries"][0]["process_digest"] = "f" * 64

    def duplicate(o):
        o["entries"].append(dict(o["entries"][0]))

    def bad_value(field, text):
        def mutate(o):
            o["entries"][1][field] = text
        return mutate

    out = {"schema": set_schema, "dup_key": duplicate, "other_digest": other_digest}
    for path in (("process_digest",), ("feature_identity",),
                 ("source_identity", "independent_reference"), ("source_identity", "error_bound")):
        out["identity_" + "_".join(path)] = ident_field(path)
    for text in ("NaN", "Infinity", "-Infinity", "sNaN", "garbage", ""):
        out[f"mx_{text or 'empty'}"] = bad_value("mx", text)
    out["my_NaN"] = bad_value("my", "NaN")
    return out


MUTATIONS = _mutations()


@pytest.mark.parametrize("name", sorted(MUTATIONS))
def test_load_cache_rejects_every_mutation(ident, obj, name: str) -> None:
    bad = copy.deepcopy(obj)
    MUTATIONS[name](bad)
    with pytest.raises(errors.Invalid):
        reference_cache.load_cache(bad, ident)


def test_load_cache_rejects_a_different_expected_identity(ident, obj) -> None:
    for field in ("process_digest", "feature_identity"):
        expected = copy.deepcopy(ident)
        expected[field] = "0" * 64
        with pytest.raises(errors.Invalid):
            reference_cache.load_cache(obj, expected)
    expected = copy.deepcopy(ident)
    expected["source_identity"]["error_bound"] = "0" * 64
    with pytest.raises(errors.Invalid):
        reference_cache.load_cache(obj, expected)


# ---- verify_rows ----
def _verify(o, **changes):
    args = {"model": 1729, "split": "calibration", "panel": 1, "history_id": HIDS[:2],
            "sequence_id": SEQ[:2], "canonical32": HIST[:2]}
    args.update(changes)
    extra = {"Ks": args["Ks"]} if "Ks" in args else {}
    return reference_cache.verify_rows(o, args["model"], args["split"], args["panel"],
                                       args["history_id"], args["sequence_id"],
                                       args["canonical32"], **extra)


def test_verify_rows_passes_on_the_exact_table(obj) -> None:
    assert _verify(obj) is None
    assert _verify(obj, split="validation", panel=2, history_id=HIDS[2:], sequence_id=SEQ[2:],
                   canonical32=HIST[2:]) is None
    assert _verify(obj, history_id=HIDS[:2].tolist(), Ks=(4,)) is None


_CHANGED_HIST = HIST[:2].copy()
_CHANGED_HIST[1, 20] = (_CHANGED_HIST[1, 20] + 1) % 3        # still a valid history
MISMATCHES = {
    "reordered_history_id": {"history_id": HIDS[:2][::-1]},
    "changed_sequence_id": {"sequence_id": np.array([907, 16], dtype=np.int64)},
    "changed_panel": {"panel": 2},
    "changed_history_byte": {"canonical32": _CHANGED_HIST},
    "missing_model": {"model": 2718},
    "missing_K": {"Ks": (1, 4, 32)},                         # no K1 entries were stored
}


@pytest.mark.parametrize("name", sorted(MISMATCHES))
def test_verify_rows_rejects_every_mismatch(obj, name: str) -> None:
    with pytest.raises(errors.Invalid):
        _verify(obj, **MISMATCHES[name])


def test_verify_rows_rejects_missing_record_entry_and_duplicate_record(obj) -> None:
    no_record = copy.deepcopy(obj)
    no_record["rows"] = [r for r in no_record["rows"] if r["split"] != "validation"]
    with pytest.raises(errors.Invalid):                       # missing (model, split) record
        _verify(no_record, split="validation", panel=2, history_id=HIDS[2:],
                sequence_id=SEQ[2:], canonical32=HIST[2:])
    missing = copy.deepcopy(obj)
    drop = (32, _hex(HIST[1]))
    missing["entries"] = [e for e in missing["entries"] if (e["K"], e["history"]) != drop]
    assert len(missing["entries"]) == len(obj["entries"]) - 1
    with pytest.raises(errors.Invalid):
        _verify(missing)
    doubled = copy.deepcopy(obj)
    doubled["rows"].append(copy.deepcopy(doubled["rows"][0]))   # not exactly one record
    with pytest.raises(errors.Invalid):
        _verify(doubled)
