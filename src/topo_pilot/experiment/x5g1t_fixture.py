"""SYNTHETIC fixture for the X5 G1 training-study CLI (job 0009): a tiny N4/V3 process pair in a
temporary store and a tiny model; never real pools, models or study data."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    TransitionSpec,
)

from .x5g1t_lineage import MASTERS

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

    The fixture ledger is its own file under ``root/study`` (never the scientific ledger); the
    budget planner uses the real-scale estimates, so a small ``cap_s`` exercises the budget stop.
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
    mailbox = root / "mailbox"
    mailbox.mkdir(parents=True, exist_ok=True)
    (mailbox / "request.json").write_text(json.dumps({"command": "RUN_NEXT"}), encoding="utf-8")
    cfg = {"protocol": "x5g1-train-v3 SYNTHETIC FIXTURE", "read_roots": [str(root / "sources")],
           "study_root": str(root / "study"), "ledger_path": str(root / "study" / "ledger.json"),
           "mailbox": str(mailbox),
           "sources": {"T": {a: [i, src.meta(i).payload_sha256] for a, i in tids.items()},
                       "E": [eid, src.meta(eid).payload_sha256]},
           "masters": list(MASTERS), "sizes": sizes or {"train": 64, "dev": 24, "test": 24},
           "model_config": {"vocab_in": 4, "vocab_out": 3, "n_layers": 1, "d_model": 8,
                            "n_heads": 2, "d_mlp": 16},
           "steps": steps, "grid": list(range(steps + 1)), "gc": {"a0": 0.05, "a020": 0.05},
           "threads": 1, "bootstrap_draws": bootstrap_draws, "cap_s": cap_s,
           "cumulative_cap_s": cap_s, "check_stored_ids": True}
    path = root / "study_config.json"
    path.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    return path
