"""SYNTHETIC fixture for the X5 G1 training-study CLI (jobs 0009-0010): a tiny N4/V3 process pair
and a tiny world in a temporary store, a tiny model and a ``mode = "synthetic-fixture"`` config
(API v4 §6) that ``validate_config`` keeps apart from production; never real pools, models or
study data."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    TransitionSpec,
)
from topo_pilot.contracts.testing import tiny_world_spec

from .x5g1t_config import PRODUCTION
from .x5g1t_lineage import MASTERS

_REPO = Path(__file__).resolve().parents[3]  # the source tree this fixture ships with

# The hand-chosen 4-state, 3-symbol HMM of contracts.testing.tiny_hmm (lazy 4-cycle walk).
T0 = np.array([[0.50, 0.25, 0.00, 0.25], [0.25, 0.50, 0.25, 0.00],
               [0.00, 0.25, 0.50, 0.25], [0.25, 0.00, 0.25, 0.50]])
E0 = np.array([[0.7, 0.2, 0.1], [0.1, 0.7, 0.2], [0.2, 0.1, 0.7], [0.4, 0.4, 0.2]])


def _entropy(p: np.ndarray) -> float:
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def _emission(E: np.ndarray, pi: np.ndarray, perm: np.ndarray) -> EmissionSpec:
    p_w = pi @ E
    diag = {"H_W_given_Z": float(np.sum(pi * [_entropy(r) for r in E])), "H_W": _entropy(p_w),
            "p_w": p_w.tolist(), "coverage_radius": 0.0, "row_entropy_quantiles": [0.0] * 5,
            "factorizes": False}
    return EmissionSpec(E=E, symbol_perm=perm, mode="overlap", sigma=1.0, diagnostics=diag)


def build_fixture(root: Path, sizes: dict | None = None, steps: int = 6,
                  bootstrap_draws: int = 40, cap_s: float = 21600.0) -> Path:
    """Create ``root/{sources,study,mailbox}`` and return the study config path.

    The fixture ledger is its own file ``root/ledger.json``, outside the study root (never the
    scientific ledger); the budget planner uses the real-scale estimates, so a small ``cap_s``
    exercises the budget stop.
    """
    root = Path(root)
    E, pi = E0, np.full(4, 0.25)
    T1 = 0.4 * np.eye(4) + 0.6 * T0  # a slower lazy walk; symmetric, pi uniform
    perm = np.array([2, 0, 1], dtype=np.int64)
    src = ArtifactStore(LocalFSBackend(root / "sources"))
    tids = {arm: src.save(TransitionSpec(T=T, pi=pi), config={"fixture": arm}, parents=[],
                          seed_map={}, consumer="experiment")
            for arm, T in (("a0", T0), ("a020", T1))}
    eid = src.save(_emission(E, pi, perm), config={"fixture": "E"}, parents=[], seed_map={},
                   consumer="experiment")
    wid = src.save(tiny_world_spec(), config={"fixture": "world"}, parents=[], seed_map={},
                   consumer="experiment")
    doc = PRODUCTION.protocol_doc
    mailbox = root / "mailbox"
    mailbox.mkdir(parents=True, exist_ok=True)
    (mailbox / "request.json").write_text(json.dumps({"command": "RUN_NEXT"}), encoding="utf-8")
    cfg = {"mode": "synthetic-fixture", "protocol": "x5g1-train-v4 SYNTHETIC FIXTURE",
           "protocol_doc": doc,
           "protocol_doc_sha256": hashlib.sha256((_REPO / doc).read_bytes()).hexdigest(),
           "read_roots": [str(root / "sources")],
           "study_root": str(root / "study"), "ledger_path": str(root / "ledger.json"),
           "mailbox": str(mailbox),
           "sources": {"world": [wid, src.meta(wid).payload_sha256],
                       "T": {a: [i, src.meta(i).payload_sha256] for a, i in tids.items()},
                       "E": [eid, src.meta(eid).payload_sha256]},
           "source_producers": {i: src.meta(i).producer_version
                                for i in (wid, eid, *tids.values())},
           "stored_checkpoint": None,
           "masters": list(MASTERS), "sizes": sizes or {"train": 64, "dev": 24, "test": 24},
           "model_config": {"vocab_in": 4, "vocab_out": 3, "n_layers": 1, "d_model": 8,
                            "n_heads": 2, "d_mlp": 16},
           "steps": steps, "grid": list(range(steps + 1)), "gc": {"a0": 0.05, "a020": 0.05},
           "threads": 1, "bootstrap_draws": bootstrap_draws, "cap_s": cap_s,
           "cumulative_cap_s": cap_s, "check_stored_ids": True, "env": {}}
    path = root / "study_config.json"
    path.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    return path
