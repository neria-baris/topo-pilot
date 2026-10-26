"""C2 data: sampling (scope c2-v1), sequence ids, panels, the y-translation donor H^Y (the sign
rule k_Y and the off-grid rule), the rho^(m) index map, history tables with the H^Y digest where
defined, the coverage tally, namespace admission and store admission (API.md §4, §19.3;
C2-FROZEN-v2 §2.2, §2.11, §5.2-§5.5, §11).

Nothing here samples at import. w33 and the latent states are dropped inside sample_block. An
OFF_GRID_Y row forms no H^Y: its token row is OFF (an index error, never a symbol), and every
use of H^Y goes through role_arrays, which keeps only the defined rows.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
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

N_SIDE_X, OFF = 12, 255
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


# ---- donors and index maps (§2.2, §2.11; API.md §4.2, §19.3) -------------------------------
def k_y(b31, coords) -> np.ndarray:
    """k_Y(H) = +1 iff ybar(b31(H)) < 11/2, else -1 (toward the interior; fy_alt.py)."""
    ybar = np.asarray(b31, dtype=np.float64) @ np.asarray(coords, dtype=np.float64)[:, 1]
    return np.where(ybar < float(cc.Y_MID), 1, -1).astype(np.int64)


def y_donor(canon32, k) -> tuple:
    """H^Y = (6a + (b + k) on w1..w31, w32) and Y_def; an off-grid row is OFF in full (never
    clamped or wrapped)."""
    H = np.asarray(canon32).astype(np.int64)
    a, b = H[:, :31] // 6, H[:, :31] % 6
    nb = b + np.asarray(k, dtype=np.int64)[:, None]
    ok = np.all((nb >= 0) & (nb <= 5), axis=1)
    out = H.copy()
    out[:, :31] = 6 * a + nb
    out[~ok] = OFF
    return out, ok


def donors4(canon32, k) -> tuple:
    """(H, H+, H-, H^Y) in ROLES order (c1_oracle.donors for the first three)."""
    return (*c1_oracle.donors(canon32), y_donor(canon32, k)[0])


def role_arrays(canon32, k) -> dict:
    """{role: (tokens, rows)}: every row for H, H+, H-; the Y_def rows only for H^Y."""
    roles = c1_oracle.donors(canon32)
    out = {r: (H, np.arange(len(H))) for r, H in zip(cc.ROLES[:3], roles)}
    HY, ok = y_donor(canon32, k)
    rows = np.flatnonzero(ok)
    return dict(out, HY=(HY[rows], rows))


def rho_m_index(coords, m) -> np.ndarray:
    """idx[i] = the state with coordinates ((x_i + m) mod 12, y_i), one grid cell per unit."""
    xy = np.rint(np.asarray(coords, dtype=np.float64)).astype(np.int64)
    pos = {(int(x), int(y)): i for i, (x, y) in enumerate(xy)}
    return np.array([pos[((int(x) + int(m)) % N_SIDE_X, int(y))] for x, y in xy], dtype=np.int64)


# ---- history tables and the coverage tally (§5.3, §5.5; API.md §4.3) -------------------------
def history_table(canon32, seq_ids, panel, k) -> dict:
    """Canonical tokens, ids, panels, k_Y, Y_def and the four digest columns ("" where H^Y is
    not defined)."""
    n = len(canon32)
    out = {
        "canonical": np.asarray(canon32, dtype=np.uint8),
        "sequence_id": np.asarray(seq_ids, dtype=np.int64),
        "panel": np.asarray(panel, dtype=np.int64),
        "k_Y": np.asarray(k, dtype=np.int8),
    }
    for role, (H, rows) in role_arrays(canon32, k).items():
        col = np.full(n, "", dtype="<U64")
        col[rows] = np.array(scores.history_digests(H), dtype="<U64") if len(rows) else col[rows]
        out[f"digest_{role}"] = col
    out["Y_def"] = out["digest_HY"] != ""
    return out


def table_roles(table) -> dict:
    return role_arrays(table["canonical"], table["k_Y"])


def table_digests(table) -> set:
    out = set()
    for role in cc.ROLES:
        out |= set(np.asarray(table[f"digest_{role}"]).astype(str).tolist())
    return out - {""}


REASONS = (
    "S_PLUS",
    "S_MINUS",
    "S_Y",
    "LIK_H",
    "LIK_PLUS",
    "LIK_MINUS",
    "LIK_Y",
    "OFF_GRID_Y",
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


OWN_GATES = ("IMPL", "AUTH-ADMIT")


def _own_suffix_ok(name, rows, stage) -> bool:
    """R-0107-2: STAGES.jsonl gets exactly one STARTED line of this stage; GATES.jsonl only
    this stage's study-scope IMPL / AUTH-ADMIT lines."""
    if name == "STAGES.jsonl":
        one = len(rows) == 1
        return one and rows[0].get("stage") == stage and rows[0].get("event") == "STARTED"
    return all(
        r.get("stage") == stage and r.get("gate") in OWN_GATES and r.get("scope") == "study"
        for r in rows
    )


def own_records(store, stage, lineage) -> dict:
    """G0 (vii), R-0107-2 (D-0107-1): {name: sha256} for GATES.jsonl and STAGES.jsonl, each an
    accepted prefix (empty, or the line-boundary prefix whose sha256 is the lineage's
    append_only value) plus this stage's own pre-G0 lines; a file failing the rule is omitted."""
    lin, out = _norm(lineage), {}
    for name in ("GATES.jsonl", "STAGES.jsonl"):
        path = Path(store) / name
        if not path.is_file():
            continue
        try:
            lines = path.read_bytes().splitlines(keepends=True)
        except OSError:
            continue
        want = lin.get(name)
        h = hashlib.sha256()
        cut = 0 if want in (None, h.hexdigest()) else None
        for i, line in enumerate(lines, 1):
            h.update(line)
            cut = i if want is not None and h.hexdigest() == want else cut
        try:
            rows = None if cut is None else [json.loads(x) for x in lines[cut:]]
        except ValueError:
            continue
        if rows is not None and all(isinstance(r, dict) for r in rows):
            if _own_suffix_ok(name, rows, stage):
                out[name] = file_sha(path)
    return out
