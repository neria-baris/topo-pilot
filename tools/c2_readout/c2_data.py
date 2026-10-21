"""C2 data: sampling (scope c2-v1), sequence ids, panels, the sigma donor, the rho_R and rho^(m)
index maps, the rho_R symmetry report, history tables with the H^R digest, the coverage tally,
namespace admission and store admission (API.md §4; C2-FROZEN-v1 §2.2, §2.11, §5.2-§5.5, §11).

Nothing here samples at import. w33 and the latent states are dropped inside sample_block.
"""

from __future__ import annotations

import fnmatch
import hashlib
import os
from pathlib import Path

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_data
import c1_oracle
import numpy as np
import scores

from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset import HMMSampler
from topo_pilot.dataset.checks import make_sequence_ids, process_code

N_SIDE_X, Y_MAX = 12, 11
LINEAGE = "FAIL_TECHNICAL/LINEAGE"
SPLITS = ("fit", "feas", "val", "test")


# ---- sampling and identifiers (§5.2; API.md §4.1) --------------------------------------------
def history_generator(split, block) -> np.random.Generator:
    if split not in SPLITS:
        raise ValueError(f"unknown split {split!r}")
    return SeedTree(0).generator("data", cc.SCOPE, split, int(block), *cc.PROCESS)


def sequence_ids(split, block) -> np.ndarray:
    code = process_code(*cc.PROCESS, f"{cc.SCOPE}/{split}/b{int(block)}")
    return np.asarray(make_sequence_ids(code, "test", cc.BLOCK), dtype=np.int64)


def sample_block(T, E_canon, pi, split, block) -> tuple:
    """One HMMSampler.sample(4096, rng) call; w33 and the latent states dropped at once."""
    tokens, states = HMMSampler(T, E_canon, pi, SequenceLayout()).sample(
        cc.BLOCK, history_generator(split, block)
    )
    canon32 = np.ascontiguousarray(tokens[:, :32]).astype(np.uint8)
    del tokens, states
    return canon32, sequence_ids(split, block)


def sample_split(T, E_canon, pi, split, blocks) -> tuple:
    """Blocks 0..blocks-1 in block order: canonical uint8 [n, 32], sequence ids, panels."""
    canon, ids, panel = [], [], []
    for b in range(int(blocks)):
        c, s = sample_block(T, E_canon, pi, split, b)
        canon.append(c)
        ids.append(s)
        panel.append(c1_data.panels(s, b))
    return np.vstack(canon), np.concatenate(ids), np.concatenate(panel)


def lowest(seq_ids, n) -> np.ndarray:
    return c1_data.lowest(seq_ids, n)


# ---- donors and index maps (§2.2, §2.11; API.md §4.2) ----------------------------------------
def sigma(canonical) -> np.ndarray:
    """y-reflection of canonical symbols: 6a + b -> 6a + (5 - b)."""
    c = np.asarray(canonical).astype(np.int64)
    return 6 * (c // 6) + (5 - c % 6)


def reflect_donor(canon32) -> np.ndarray:
    """H^R = (sigma(w1..w31), w32), int64 [n, 32]."""
    H = np.asarray(canon32).astype(np.int64)
    out = H.copy()
    out[:, :31] = sigma(H[:, :31])
    return out


def donors4(canon32) -> tuple:
    """(H, H+, H-, H^R) in ROLES order (c1_oracle.donors for the first three)."""
    return (*c1_oracle.donors(canon32), reflect_donor(canon32))


def _positions(coords) -> tuple:
    xy = np.rint(np.asarray(coords, dtype=np.float64)).astype(np.int64)
    return xy, {(int(x), int(y)): i for i, (x, y) in enumerate(xy)}


def rho_R_index(coords) -> np.ndarray:
    """idx[i] = the state with coordinates (x_i, 11 - y_i)."""
    xy, pos = _positions(coords)
    return np.array([pos[(int(x), Y_MAX - int(y))] for x, y in xy], dtype=np.int64)


def rho_m_index(coords, m) -> np.ndarray:
    """idx[i] = the state with coordinates ((x_i + m) mod 12, y_i), one grid cell per unit."""
    xy, pos = _positions(coords)
    return np.array([pos[((int(x) + int(m)) % N_SIDE_X, int(y))] for x, y in xy], dtype=np.int64)


def symmetry_report_R(T, E, pi, coords) -> dict:
    """The rho_R/sigma analogue of c1_oracle.symmetry_report (§7 row 6, T2)."""
    T, E, pi = (np.asarray(a, dtype=np.float64) for a in (T, E, pi))
    N, V = E.shape
    rho, s = rho_R_index(coords), sigma(np.arange(V))
    Er = E[rho][:, s]
    dev = max(
        float(np.abs(T[np.ix_(rho, rho)] - T).max()),
        float(np.abs(Er - E).max()),
        float(np.abs(pi - 1.0 / N).max()),
    )
    exact = bool(np.array_equal(T[np.ix_(rho, rho)], T) and np.array_equal(pi[rho], pi))
    r_E = max(
        abs(c1_oracle.F(Er[z, v]) / c1_oracle.F(E[z, v]) - 1) for z in range(N) for v in range(V)
    )
    eps = r_E / (1 - r_E) if r_E < 1 else None
    return {
        "max_dev": dev,
        "symmetry_ok": dev <= float(cc.frac(cc.T_SYM_R)),
        "exact_invariance": exact,
        "r_E": r_E,
        "eps_sym": eps,
    }


# ---- history tables and the coverage tally (§5.3, §5.5; API.md §4.3) -------------------------
def history_table(canon32, seq_ids, panel) -> dict:
    roles = donors4(canon32)
    out = {
        "canonical": np.asarray(canon32, dtype=np.uint8),
        "sequence_id": np.asarray(seq_ids, dtype=np.int64),
        "panel": np.asarray(panel, dtype=np.int64),
    }
    for role, H in zip(cc.ROLES, roles):
        out[f"digest_{role}"] = np.array(scores.history_digests(H), dtype="<U64")
    return out


def table_digests(table) -> set:
    out = set()
    for role in cc.ROLES:
        out |= set(np.asarray(table[f"digest_{role}"]).astype(str).tolist())
    return out


REASONS = (
    "S_PLUS",
    "S_MINUS",
    "S_REFL",
    "LIK_H",
    "LIK_PLUS",
    "LIK_MINUS",
    "LIK_REFL",
    "ZERO_MOD_H",
    "ZERO_MOD_PLUS",
    "ZERO_MOD_MINUS",
)
MODEL_REASONS = (
    "UNSUPPORTED_H",
    "UNSUPPORTED_PLUS",
    "UNSUPPORTED_MINUS",
    "ZERO_CODE_PLUS",
    "ZERO_CODE_MINUS",
    "R1_ZERO",
    "R1_UNSELECTED",
)


def coverage_tally(flags) -> dict:
    """Rows per reason key, in the given order; a row counts under every reason it carries."""
    return {k: int(np.count_nonzero(np.asarray(v, dtype=bool))) for k, v in flags.items()}


# ---- namespace and store admission (§5.2 G0 vi-vii, §11 item 7; API.md §4.4) -----------------
NEEDLE = cc.SCOPE.encode("ascii")
NAMED = ("CONTRACT*.json", "FREEZE*.json", "STAGES*.jsonl", "GATES*.jsonl")
STORE_SUFFIXES = (".json", ".jsonl", ".md", ".txt", ".py")
SKIP_DIRS = (".git", ".venv")
PAYLOAD_DIRS = ("hist", "oracle", "fits", "stages", "sealed")
METER_FILES = ("cpu_ledger.json", "RUN.lock", "OPERATION_ACTIVE.json", "OPERATIONS.jsonl")
CHUNK = 1 << 20


def file_sha(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def contains_scope(path, needle=NEEDLE) -> bool:
    """True iff the file bytes contain `needle` (1 MiB chunks, len(needle) - 1 bytes overlap)."""
    tail = b""
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            if needle in tail + block:
                return True
            tail = (tail + block)[-(len(needle) - 1) :]
    return False


def _rel(path, base):
    """The posix path of `path` relative to `base`, or None if it lies outside."""
    for p, b in ((Path(path), Path(base)), (Path(path).resolve(), Path(base).resolve())):
        try:
            return p.relative_to(b).as_posix()
        except ValueError:
            continue
    return None


def _walk(top, skip=()):
    for dirpath, dirnames, filenames in os.walk(top):
        dirnames[:] = sorted(d for d in dirnames if d not in skip)
        for name in sorted(filenames):
            yield Path(dirpath) / name


def _scanned(rel_parts) -> bool:
    name = rel_parts[-1]
    if any(fnmatch.fnmatchcase(name, p) for p in NAMED):
        return True
    return (
        len(rel_parts) > 1
        and fnmatch.fnmatchcase(rel_parts[0], "*-store*")
        and Path(name).suffix in STORE_SUFFIXES
    )


def _norm(mapping) -> dict:
    return {str(k).replace("\\", "/"): str(v).lower() for k, v in (mapping or {}).items()}


def _pinned(rel, sha, pins) -> bool:
    """A byte copy of a pinned file at the same repository-relative path (e.g. main's merge)."""
    return any(pins[k] == sha and (rel == k or rel.endswith("/" + k)) for k in pins)


def namespace_scan(root=None, pinned=None, lineage=None) -> dict:
    """G0 (vi): every file of the §4.4 file set whose bytes contain "c2-v1" must be pinned
    code/configuration or a recognised lineage record; any other hit -> FAIL_TECHNICAL/LINEAGE."""
    root = Path(cc.PROJECT_ROOT if root is None else root)
    pins, lin = _norm(pinned), _norm(lineage)
    hits, n = [], 0
    for f in _walk(root, SKIP_DIRS):
        rel = _rel(f, root)
        if rel is None or not _scanned(rel.split("/")):
            continue
        n += 1
        if not contains_scope(f):
            continue
        sha = file_sha(f)
        srel = _rel(f, cc.STORE)
        if _rel(f, Path(cc.WORKTREE) / "tools" / "c2_readout") is not None or _pinned(
            rel, sha, pins
        ):
            kind = "PINNED"
        elif srel is not None and lin.get(srel) == sha:
            kind = "LINEAGE"
        else:
            kind = "FOREIGN"
        hits.append({"path": str(f), "sha256": sha, "class": kind})
    bad = any(h["class"] == "FOREIGN" for h in hits)
    return {"status": LINEAGE if bad else "PASS", "hits": hits, "scanned": n}


def _meter_file(rel) -> bool:
    return (
        rel.startswith("logs/")
        or rel in METER_FILES
        or ("/" not in rel and fnmatch.fnmatchcase(rel, "LOCK_RELEASED_*.json"))
    )


def store_admission(store, lineage, first_sampling) -> dict:
    """G0 (vii): every store file is meter bookkeeping or recognised with its exact sha256; at
    first sampling no file may exist under hist/, oracle/, fits/, stages/ or sealed/."""
    store, lin = Path(store), _norm(lineage)
    unrecognised, payload = [], []
    for f in _walk(store) if store.is_dir() else ():
        rel = _rel(f, store)
        if first_sampling and rel.split("/")[0] in PAYLOAD_DIRS:
            payload.append(rel)
        if not (_meter_file(rel) or lin.get(rel) == file_sha(f)):
            unrecognised.append(rel)
    ok = not unrecognised and not (first_sampling and payload)
    return {"status": "PASS" if ok else LINEAGE, "unrecognised": unrecognised, "payload": payload}
