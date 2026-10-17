"""K4b process assembly, sampling, sequence IDs, history tables, separation (API.md §2).

Protocol §2.2 (fixed objects), §3.1 (splits and fixed 3,072-row blocks), §3.4 (separation and
the sealed-D-2a predicate). Every model map is keyed by the int seeds (R11 lesson).
"""

from __future__ import annotations

from collections import Counter

import c1_data
import k4b_config
import numpy as np
import scores
from c1_records import C1GateFailure
from k4b_config import BLOCK, MODELS, PANEL, PROCESS, SCOPE

from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset import HMMSampler
from topo_pilot.dataset.checks import check_disjoint, make_sequence_ids, process_code

IDENTITY = "FAIL_TECHNICAL/IDENTITY"
LINEAGE = "FAIL_TECHNICAL/LINEAGE"
INCOMPLETE = "INCONCLUSIVE/REGISTRY_INCOMPLETE"
PREDICATE_REASON = "potential overlap with sealed D-2a histories"


def _int_map(d, what) -> dict:
    try:
        out = {int(k): v for k, v in d.items()}
    except (TypeError, ValueError) as exc:
        raise C1GateFailure(IDENTITY, f"{what}: {exc!r}") from exc
    return k4b_config.require_int_keys(out, what)


def load_process(cfg=None) -> dict:
    """inputs.load_process, re-keyed by int seed; perms and canonical emissions checked."""
    import inputs
    import oracle_profile

    try:
        cfg = inputs.load_config() if cfg is None else cfg
        proc = inputs.load_process(cfg)
    except C1GateFailure:
        raise
    except Exception as exc:  # noqa: BLE001  any load defect is an identity defect
        raise C1GateFailure(IDENTITY, f"load_process: {exc!r}") from exc
    E_named = _int_map(proc["E_named"], "E_named")
    perm = _int_map(proc["perm"], "perm")
    E_canon = {}
    for j in MODELS:
        p = np.asarray(perm[j])
        inv = np.argsort(p)
        if sorted(p.tolist()) != list(range(36)) or not np.array_equal(p[inv], np.arange(36)):
            raise C1GateFailure(IDENTITY, f"perm {j} is not a permutation of 0..35")
        E_canon[j] = oracle_profile.canonical_emission(E_named[j], p)
    first = E_canon[MODELS[0]]
    for j in MODELS[1:]:
        if not (np.array_equal(E_canon[j], first) and E_canon[j].tobytes() == first.tobytes()):
            raise C1GateFailure(IDENTITY, f"E_canon {j} differs from {MODELS[0]}")
    return {
        "T": proc["T"],
        "pi": proc["pi"],
        "coords": proc["coords"],
        "features": oracle_profile.circle_features(proc["coords"]),
        "E_named": E_named,
        "perm": perm,
        "E_canon": E_canon,
        "E_canon_shared": first,
        "specs": proc.get("records", {}),
    }


def history_generator(split, block) -> np.random.Generator:
    return SeedTree(0).generator("data", SCOPE, split, int(block), *PROCESS)


def sequence_ids(split, block) -> np.ndarray:
    code = process_code(*PROCESS, f"{SCOPE}/{split}/b{int(block)}")
    return np.asarray(make_sequence_ids(code, "test", BLOCK), dtype=np.int64)


def sample_block(T, E_canon, pi, split, block) -> tuple:
    """One HMMSampler.sample(3072, rng) call; w33 and the states dropped; rows sorted by id."""
    tokens, states = HMMSampler(T, E_canon, pi, SequenceLayout()).sample(
        BLOCK, history_generator(split, block)
    )
    canon32 = np.asarray(tokens[:, :32], dtype=np.uint8)
    del tokens, states
    ids = sequence_ids(split, block)
    order = np.argsort(ids, kind="stable")
    return np.ascontiguousarray(canon32[order]), np.ascontiguousarray(ids[order])


def named_from_canonical(canon32, perm) -> np.ndarray:
    return np.asarray(np.asarray(perm)[np.asarray(canon32)], dtype=np.uint8)


def model_inputs(canon32, perm):
    import c1_model

    return c1_model.model_inputs(named_from_canonical(canon32, perm))


def digests(canon32) -> list:
    return scores.history_digests(np.asarray(canon32, dtype=np.uint8))


def lowest_rows(seq_ids, n=PANEL) -> np.ndarray:
    return c1_data.lowest(seq_ids, n)


def duplicates(canon32) -> dict:
    """Counted by digest, never removed. n_duplicate_rows = n_rows - n_unique (API §13 item 24)."""
    counts = Counter(digests(canon32))
    n = int(np.asarray(canon32).shape[0])
    return {
        "n_rows": n,
        "n_unique": len(counts),
        "n_duplicate_rows": n - len(counts),
        "max_multiplicity": max(counts.values()) if counts else 0,
    }


def history_table(canon32, seq_ids, split, block) -> dict:
    """Rows in ascending sequence_id; landmarks (cal, val), ref rows and decoder panels (cal)."""
    ids = np.asarray(seq_ids, dtype=np.int64)
    order = np.argsort(ids, kind="stable")
    canon = np.ascontiguousarray(np.asarray(canon32, dtype=np.uint8)[order])
    ids = np.ascontiguousarray(ids[order])
    n = len(ids)
    rank = np.arange(n)
    landmark = (rank < PANEL) if split in ("cal", "val") else np.zeros(n, dtype=bool)
    ref_row = (rank < 4) if split == "cal" else np.zeros(n, dtype=bool)
    panel = np.full(n, -1, dtype=np.int8)
    if split == "cal":
        panel[~landmark] = ((rank[~landmark] - PANEL) // PANEL).astype(np.int8)
    return {
        "canon32": canon,
        "seq_ids": ids,
        "digest": np.array(digests(canon)),
        "landmark": np.asarray(landmark, dtype=bool),
        "ref_row": np.asarray(ref_row, bool),
        "decoder_panel": panel,
        "split": split,
        "block": int(block),
    }


def separation_cal_val(U_cal, U_val, reg1) -> dict:
    return c1_data.separation(U_cal, U_val, reg1)


def separation_fresh(U_test, reg2) -> dict:
    reg = set(reg2)
    hits = sum(1 for d in U_test if d in reg)
    return {"collisions": {"test_R2": int(hits)}, "status": "PASS" if not hits else LINEAGE}


def seq_disjoint(blocks, frozen_union, frozen_ranges=()) -> dict:
    arrays = {k: np.asarray(v, dtype=np.int64) for k, v in blocks.items()}
    hits = {}
    try:
        check_disjoint(**arrays)
    except Exception as exc:  # noqa: BLE001  SPLIT_OVERLAP -> lineage
        hits["between_blocks"] = repr(exc)
    union = np.asarray(sorted(int(x) for x in frozen_union), dtype=np.int64)
    for name, ids in arrays.items():
        n_union = int(np.isin(ids, union).sum()) if union.size else 0
        n_range = sum(int(((ids >= int(lo)) & (ids < int(hi))).sum()) for lo, hi in frozen_ranges)
        if n_union:
            hits[f"{name}:frozen_union"] = n_union
        if n_range:
            hits[f"{name}:frozen_ranges"] = n_range
    return {"status": "PASS" if not hits else LINEAGE, "hits": hits}


def sealed_d2a_predicate(canon32) -> np.ndarray:
    """True where all 32 symbols lie in {0,...,4} (the sealed D-2a alphabet, §3.4 e)."""
    return np.all(np.asarray(canon32) <= 4, axis=1)


PREDICATES = {"sealed_d2a": sealed_d2a_predicate}


def predicate_check(canon32, predicates) -> dict:
    hits = {name: int(np.sum(PREDICATES[name](canon32))) for name in predicates}
    if any(hits.values()):
        return {"status": INCOMPLETE, "hits": hits, "reason": PREDICATE_REASON}
    return {"status": "PASS", "hits": hits}
