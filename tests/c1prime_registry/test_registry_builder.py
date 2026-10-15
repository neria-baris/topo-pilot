"""Builder tests for tools/c1prime/c1_registry_sources.py (job 0027; synthetic fixtures only)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
for _p in (REPO / "tools" / "c1prime_registry", REPO / "tools" / "c1prime",
           REPO / "tools" / "x4_circle_history", REPO / "tools" / "x4_oracle_profile",
           REPO / "tests" / "oracle_profile"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import c1_data  # noqa: E402
import c1_registry_sources as rs  # noqa: E402
import pytest  # noqa: E402
import scores  # noqa: E402


def test_canonical32_inverts_the_named_permutation():
    rng = np.random.default_rng(0)
    perm = rng.permutation(36)
    canon = rng.integers(0, 36, (50, 33))
    named = perm[canon]  # named = perm[canonical]
    np.testing.assert_array_equal(rs.canonical32(named, perm), canon[:, :32].astype(np.uint8))


def test_canonical32_rejects_a_non_permutation():
    with pytest.raises(ValueError):
        rs.canonical32(np.zeros((2, 33), dtype=int), np.zeros(36, dtype=int))


def test_reference_cache_reader_keeps_only_32_symbol_entries(tmp_path):
    import reference_cache  # K4 producer of REFERENCE_CACHE.json (unchanged)

    h = (np.arange(64).reshape(2, 32) * 7) % 36
    enc = reference_cache.history_hex(h)
    data = {"entries": [{"K": 32, "history": enc[0]}, {"K": 4, "history": enc[0][:64]},
                        {"K": 32, "history": enc[1]}]}
    p = tmp_path / "ref.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    got = rs.reference_cache_reader(p)
    np.testing.assert_array_equal(got, h.astype(np.uint8))


def test_token_readers_reject_out_of_range_values_instead_of_wrapping():
    with pytest.raises(ValueError):
        rs._u8(np.full((1, 32), 256, dtype=np.int64))
    with pytest.raises(ValueError):
        rs._u8(np.full((1, 32), -1, dtype=np.int64))
    with pytest.raises(ValueError):
        rs._u8(np.zeros((1, 31), dtype=np.int64))
    np.testing.assert_array_equal(rs._u8(np.arange(33)[None, :]), np.arange(32)[None, :])


def test_handoff_scan_finds_token_lists_and_ignores_others(tmp_path):
    good = list(range(32))
    (tmp_path / "a.json").write_text(json.dumps({"x": {"h": good, "n": [1, 2]}}), "utf-8")
    (tmp_path / "b.json").write_text(json.dumps({"big": list(range(300, 332))}), "utf-8")
    (tmp_path / "c.json").write_text("not json", "utf-8")
    srcs = {s["name"]: s for s in rs.handoff_sources(tmp_path)}
    assert rs.handoff_sources(tmp_path)[0]["meta"]["source"] == "c"
    np.testing.assert_array_equal(srcs["c:a.json"]["reader"](tmp_path / "a.json"),
                                  np.asarray([good], dtype=np.uint8))
    assert srcs["c:b.json"]["reader"](tmp_path / "b.json").shape == (0, 32)
    assert srcs["c:c.json"]["reader"](tmp_path / "c.json").shape == (0, 32)


def test_frozen_builder_unions_and_hashes_sources(tmp_path):
    a = np.random.default_rng(1).integers(0, 36, (5, 32)).astype(np.uint8)
    np.savez(tmp_path / "s.npz", canonical32=a)
    reg = c1_data.build_registry([
        {"name": "x", "path": tmp_path / "s.npz", "meta": {"source": "b"}},
        {"name": "empty", "path": tmp_path / "s.npz", "reader": lambda p: rs.EMPTY,
         "meta": {"source": "b", "reason": "none"}}])
    assert reg["status"] == "PASS" and reg["n_digests"] == len(set(scores.history_digests(a)))
    assert [e["contributes"] for e in reg["entries"]] == [len(set(scores.history_digests(a))), 0]


def test_store_sources_record_every_listed_store_explicitly():
    names = {s["name"] for s in rs.store_sources()}
    for required in ("b:X4/x4b-research-store", "b:job-0014/x4-oracle-profile-store-0014",
                     "b:X4-F/x4f-gates-research-store", "b:d1-seam-oracle-store",
                     "b:chart-diag-store-0023", "b:x2a-stage0-oracle-store",
                     "b:K4-0015/REFERENCE_CACHE K=32"):
        assert required in names
    assert any(n.startswith("b:X4-B2/") for n in names)
    assert any(n.startswith("b:X4/x4-history-feas/") for n in names)
