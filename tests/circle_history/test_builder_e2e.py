"""BUILDER end-to-end test (not independent): runner stages on a fully synthetic store.

Uses a tiny 12-state ring HMM (x = 0..11), deterministic token strings, circle-shaped synthetic
activations and three models with different symbol permutations, all inside
contracts.testing.memory_store(). No real artifact is read. See BUILDER_TESTS.md.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.analysis
REPO = Path(__file__).resolve().parents[2]
TOOL = REPO / "tools" / "x4_circle_history"
for extra in (TOOL, REPO / "tools" / "x4_oracle_profile", REPO / "tests" / "oracle_profile"):
    sys.path.insert(0, str(extra))

import oracle_profile  # noqa: E402
import runner  # noqa: E402
from adapter import E4Manifest  # noqa: E402
from errors import Unresolved  # noqa: E402

from topo_pilot.contracts import (  # noqa: E402
    ActivationSet,
    Checkpoint,
    HistoryIndex,
    ObservationSet,
    make_history_id,
    tokens_hash,
)
from topo_pilot.contracts.testing import memory_store  # noqa: E402

S, V, R, PANEL, NPAN = 12, 4, 48, 16, 3
MODELS = [1729, 2718, 3141]
PERMS = {1729: np.array([0, 1, 2, 3]), 2718: np.array([2, 0, 3, 1]), 3141: np.array([3, 2, 1, 0])}


def _process():
    T = np.zeros((S, S))
    for s in range(S):
        T[s, s], T[s, (s + 1) % S], T[s, (s - 1) % S] = 0.5, 0.25, 0.25
    x = np.arange(S)
    raw = np.stack([1.0 + np.cos(2 * np.pi * (x - 3 * k) / S) for k in range(V)], axis=1) + 0.1
    E = raw / raw.sum(axis=1, keepdims=True)
    pi = np.full(S, 1.0 / S)
    coords = np.column_stack((x, np.zeros(S)))
    return {
        "T": T,
        "pi": pi,
        "E": E,
        "coords": coords,
        "features": oracle_profile.circle_features(coords),
        "perm": dict(PERMS),
        "canonical_spread": 0.0,
    }


def _canonical_tokens():
    r, t = np.meshgrid(np.arange(R), np.arange(33), indexing="ij")
    return ((r * 7 + t * 3 + (r * t) % 5) % V).astype(np.uint8)


def _activations(model):
    angles = 2 * np.pi * (np.arange(R) * 5 % R) / R + 0.01 * (model % 7)
    base = np.column_stack(
        [
            np.cos(angles),
            np.sin(angles),
            0.05 * np.cos(2 * angles),
            0.05 * np.sin(3 * angles),
            np.zeros(R),
            np.zeros(R),
        ]
    )
    return np.stack([base * 0.5, base], axis=1).astype(np.float32)


def _store():
    store, per_model = memory_store(), {}
    canon = _canonical_tokens()
    seq = (1000 + np.arange(R)).astype(np.int64)
    panel = (np.arange(R) % NPAN + 1).astype(np.int64)
    for model in MODELS:
        named = PERMS[model][canon.astype(np.int64)].astype(np.uint8)
        obs = ObservationSet(split="test", V=V, sequence_id=seq, tokens=named)
        oid = store.save(obs, config={"model": model}, parents=[], seed_map={}, consumer="dataset")
        th = np.array([tokens_hash(named[i, :32]) for i in range(R)])
        hid = np.array([make_history_id(oid, int(s), 32, h) for s, h in zip(seq, th)])
        hist = HistoryIndex(
            dataset_id=oid,
            history_id=hid,
            sequence_id=seq,
            end=np.full(R, 32, np.int64),
            panel=panel,
            tokens_hash=th,
            panel_size=PANEL,
            n_panels=NPAN,
        )
        hix = store.save(
            hist, config={"model": model}, parents=[oid], seed_map={}, consumer="dataset"
        )
        ck = store.save(
            Checkpoint(run_id=f"r{model}", step=5000, observation_id=oid, state=b"x"),
            config={"model": model},
            parents=[oid],
            seed_map={},
            consumer="learner",
        )
        acts = ActivationSet(
            hooks=("resid_post_2", "resid_post_3"),
            source="model",
            history_id=hid,
            A=_activations(model),
            checkpoint_id=ck,
        )
        aid = store.save(
            acts,
            config={"model": model},
            parents=[oid, hix, ck],
            seed_map={},
            consumer="activations",
        )
        per_model[model] = {
            "ObservationSet": oid,
            "HistoryIndex": hix,
            "ActivationSet": aid,
            "checkpoint": ck,
        }
    return store, E4Manifest(per_model=per_model, panel_size=PANEL, n_panels=NPAN)


def _contract(relaxed: bool):
    c = copy.deepcopy(json.loads((TOOL / "CONTRACT.json").read_text(encoding="utf-8")))
    c["precision"].update(sd_draws=40, centered_draws=40)
    if relaxed:
        c["chart"].update(
            phase_bin_min_rows=0, overall_resultant_max=1.0, fidelity_min_agreement=0.0
        )
    return c


def _context(tmp_path, relaxed):
    store, manifest = _store()
    return runner.Context(
        out=tmp_path,
        store=store,
        manifest=manifest,
        models=MODELS,
        process=_process(),
        contract=_contract(relaxed),
    )


def _gates(tmp_path):
    return [(g["gate"], g["status"]) for g in runner.gates_so_far(tmp_path)]


def test_frozen_thresholds_stop_inconclusive_at_coverage(tmp_path):
    ctx = _context(tmp_path, relaxed=False)
    runner.stage_identity(ctx)
    runner.stage_oracle(ctx)
    result = runner.stage_charts(ctx)
    assert result.get("stopped_at") in (
        "phase_bins",
        "overall_resultant",
        "fidelity_A",
        "extension_support",
    )
    first_bad = next(s for _, s in _gates(tmp_path) if s != "PASS")
    assert first_bad == "INCONCLUSIVE"
    with pytest.raises(Unresolved):
        runner.stage_precision(ctx)
    assert runner.stage_export(ctx)["overall"] == "INCONCLUSIVE"


def test_relaxed_thresholds_reach_precision_and_export(tmp_path):
    ctx = _context(tmp_path, relaxed=True)
    runner.stage_identity(ctx)
    oracle = runner.stage_oracle(ctx)
    assert all(
        v["four_lowest"]["status"] == "PASS" and v["all_rows"]["status"] == "PASS"
        for v in oracle.values()
    )
    charts = runner.stage_charts(ctx)
    assert "stopped_at" not in charts, charts
    for model in MODELS:
        certs = charts[model]["certificates"]
        assert all(c["status"] == "CERTIFIED" for c in certs.values())
    runner.stage_precision(ctx)
    summary = runner.stage_export(ctx)
    gate_names = [g for g, _ in _gates(tmp_path)]
    assert (
        gate_names[0] == "identity"
        and "precision_projection" in gate_names
        or "B4_lower" in gate_names
    )
    assert summary["overall"] in ("PASS", "INCONCLUSIVE")
    assert (tmp_path / "chart_1729.npz").exists() and (
        tmp_path / "FEASIBILITY_SUMMARY.json"
    ).exists()


def test_join_mismatch_stops_inconclusive(tmp_path):
    ctx = _context(tmp_path, relaxed=True)
    ctx.process["perm"][2718] = PERMS[3141]
    with pytest.raises(Exception):
        runner.stage_identity(ctx)
    assert _gates(tmp_path)[0][1] in ("INCONCLUSIVE", "FAIL_TECHNICAL")
