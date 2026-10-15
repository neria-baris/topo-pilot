"""C1' histories, sequence ids, panels, history tables, exposure registry and separation (API.md
§12; protocol §2.2-§2.4). Sampling functions exist for the data stages; job 0026 runs none."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import c1_config  # noqa: F401  (sys.path)
import c1_oracle
import numpy as np
import scores

from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset import HMMSampler
from topo_pilot.dataset.checks import check_first_token, make_sequence_ids, process_code

BLOCK = 4096
PROCESS = ("cylinder", "overlap", "1.25")


def history_generator(split, block):
    return SeedTree(0).generator("data", "c1-sf-v1", split, int(block), *PROCESS)


def sequence_ids(split, block) -> np.ndarray:
    return make_sequence_ids(process_code(*PROCESS, f"c1-sf-v1/{split}/b{int(block)}"), "test",
                             BLOCK)


def sample_block(T, E_canon, pi, split, block) -> tuple:
    """One HMMSampler.sample(4096, rng) call; w33 and the latent states dropped at once."""
    tokens, states = HMMSampler(T, E_canon, pi, SequenceLayout()).sample(
        BLOCK, history_generator(split, block))
    canon32 = np.ascontiguousarray(tokens[:, :32]).astype(np.uint8)
    del tokens, states
    return canon32, sequence_ids(split, block)


def panels(seq_ids, block) -> np.ndarray:
    seq_ids = np.asarray(seq_ids, dtype=np.int64)
    rank = np.empty(len(seq_ids), dtype=np.int64)
    rank[np.argsort(seq_ids, kind="stable")] = np.arange(len(seq_ids))
    return 4 * int(block) + rank // 1024


def lowest(seq_ids, n) -> np.ndarray:
    return np.argsort(np.asarray(seq_ids, dtype=np.int64), kind="stable")[: int(n)]


def history_table(canon32, seq_ids, panel) -> dict:
    H, Hp, Hm = c1_oracle.donors(canon32)
    return {"canonical": np.asarray(canon32, dtype=np.uint8),
            "sequence_id": np.asarray(seq_ids, dtype=np.int64),
            "panel": np.asarray(panel, dtype=np.int64),
            "digest_H": np.array(scores.history_digests(H)),
            "digest_Hp": np.array(scores.history_digests(Hp)),
            "digest_Hm": np.array(scores.history_digests(Hm))}


def registry_digests(canon32) -> set:
    return set(scores.history_digests(np.asarray(canon32)))


def table_union(table) -> set:
    return set(table["digest_H"].tolist()) | set(table["digest_Hp"].tolist()) \
        | set(table["digest_Hm"].tolist())


def _union(x) -> set:
    if isinstance(x, dict):
        out = set()
        for v in x.values():
            out |= set(v)
        return out
    return set(x)


def separation(U_cal, U_val, R1) -> dict:
    cal, val, reg = _union(U_cal), _union(U_val), _union(R1)
    hits = {"cal_R1": len(cal & reg), "val_R1": len(val & reg), "cal_val": len(cal & val)}
    return {"collisions": hits,
            "status": "PASS" if not any(hits.values()) else "FAIL_TECHNICAL/LINEAGE"}


def _file_sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_registry(sources) -> dict:
    """Each source: {name, path, meta, reader?}. reader(path) -> canonical uint8 [n, 32]; the
    default reads key 'canonical32' of an NPZ. Unreadable -> INCONCLUSIVE/REGISTRY_INCOMPLETE."""
    entries, digests, missing = [], set(), []
    for src in sources:
        path = Path(src["path"])
        try:
            reader = src.get("reader") or (lambda p: np.load(p)["canonical32"])
            canon = np.asarray(reader(path))
            sha = _file_sha(path)
        except Exception as exc:  # noqa: BLE001  an unreadable source blocks the release
            missing.append({"name": src.get("name"), "path": str(path), "error": repr(exc)})
            continue
        got = registry_digests(canon) if canon.size else set()
        digests |= got
        entries.append({"name": src.get("name"), "path": str(path), "sha256": sha,
                        "meta": src.get("meta", {}), "rows": int(canon.shape[0]) if canon.ndim
                        else 0, "contributes": len(got)})
    union = hashlib.sha256(json.dumps(sorted(digests)).encode()).hexdigest()
    return {"entries": entries, "missing": missing, "digests": sorted(digests),
            "union_sha256": union, "n_digests": len(digests),
            "status": "PASS" if not missing else "INCONCLUSIVE/REGISTRY_INCOMPLETE"}


def first_token_ok(first, pE, split) -> bool:
    try:
        check_first_token(np.asarray(first), np.asarray(pE, dtype=np.float64), split)
    except Exception:  # noqa: BLE001  NUMERICAL_FAILURE (p < 1e-4) -> lineage alarm
        return False
    return True
