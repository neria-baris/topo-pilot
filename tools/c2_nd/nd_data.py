"""C2ND data: the c2nd-v1 samplers and sequence ids, the needle scan, the cross-lineage hygiene
check and store admission (API.md §4, §20.3 ND-C35; C2ND-DESIGN-v1 §6.1, §6.6, §3 row 1 (vii)).

Donors, H^Y, history tables and the coverage tally are the C2 functions unchanged (c2_data);
only the scope differs (§6.1: "the c2_data lines 37-55 recipe with the scope replaced"). Nothing
here samples at import. Paths are read through nd_config at call time.
"""

from __future__ import annotations

from pathlib import Path

import nd_config as nc  # first: the API.md §1 sys.path convention

# isort: split
import c1_data
import c2_config as cc
import c2_data as cd
import numpy as np

from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.dataset import HMMSampler
from topo_pilot.dataset.checks import make_sequence_ids, process_code

LINEAGE = "FAIL_TECHNICAL/LINEAGE"
SPLITS = nc.SPLITS

# C2 functions reused unchanged (API.md §4.1, §17)
k_y, y_donor, donors4, role_arrays = cd.k_y, cd.y_donor, cd.donors4, cd.role_arrays
history_table, table_roles, table_digests = cd.history_table, cd.table_roles, cd.table_digests
coverage_tally, lowest, file_sha = cd.coverage_tally, cd.lowest, cd.file_sha


# ---- sampling and identifiers (§6.1; API.md §4.1, §12) ---------------------------------------
def _scope(scope) -> str:
    scope = nc.SCOPE if scope is None else str(scope)
    if scope not in (nc.SCOPE, nc.DRY_SCOPE):
        raise ValueError(f"unknown scope {scope!r}")
    return scope


def history_generator(split, block, scope=None) -> np.random.Generator:
    if split not in SPLITS:
        raise ValueError(f"unknown split {split!r}")
    return SeedTree(0).generator("data", _scope(scope), split, int(block), *nc.PROCESS)


def sequence_ids(split, block, scope=None) -> np.ndarray:
    if split not in SPLITS:
        raise ValueError(f"unknown split {split!r}")
    code = process_code(*nc.PROCESS, f"{_scope(scope)}/{split}/b{int(block)}")
    return np.asarray(make_sequence_ids(code, "test", nc.BLOCK), dtype=np.int64)


def sample_block(T, E_canon, pi, split, block, scope=None) -> tuple:
    """One HMMSampler.sample(4096, rng) call; w33 and the latent states dropped at once."""
    tokens, states = HMMSampler(T, E_canon, pi, SequenceLayout()).sample(
        nc.BLOCK, history_generator(split, block, scope)
    )
    canon32 = np.ascontiguousarray(tokens[:, :32]).astype(np.uint8)
    del tokens, states
    return canon32, sequence_ids(split, block, scope)


def sample_split(T, E_canon, pi, split, blocks, scope=None) -> tuple:
    """Blocks 0..blocks-1 in block order: canonical uint8 [n, 32], sequence ids, panels."""
    canon, ids, panel = [], [], []
    for b in range(int(blocks)):
        c, s = sample_block(T, E_canon, pi, split, b, scope)
        canon.append(c)
        ids.append(s)
        panel.append(c1_data.panels(s, b))
    return np.vstack(canon), np.concatenate(ids), np.concatenate(panel)


# ---- namespace scan and hygiene (§6.6; API.md §4.2) ------------------------------------------
NEEDLE = nc.SCOPE.encode("ascii")
C2_NEEDLE = cc.SCOPE.encode("ascii")  # C2's scope, never written as a literal in C2ND files
PARALLEL_NEEDLES = tuple(bytes.fromhex(h) for h in nc.CONTRACT["namespace"]["parallel_needles_hex"])


def _under(path, base) -> bool:
    return cd._rel(path, base) is not None


def namespace_scan(root=None, pinned=None, lineage=None) -> dict:
    """G0 (vi): every file of C2's scanned set whose bytes contain "c2nd-v1" must be pinned C2ND
    code/configuration or a recognised lineage record of the C2ND store; any other hit (one in a
    parallel store included, RC-11) -> FAIL_TECHNICAL/LINEAGE."""
    root = Path(nc.PROJECT_ROOT if root is None else root)
    pins, lin = cd._norm(pinned), cd._norm(lineage)
    own = Path(nc.WORKTREE) / "tools" / "c2_nd"
    hits, n = [], 0
    for f in cd._walk(root, cd.SKIP_DIRS):
        rel = cd._rel(f, root)
        if rel is None or not cd._scanned(rel.split("/")):
            continue
        n += 1
        if not cd.contains_scope(f, needle=NEEDLE):
            continue
        sha, srel = cd.file_sha(f), cd._rel(f, nc.STORE)
        if _under(f, own) or cd._pinned(rel, sha, pins):
            kind = "PINNED"
        elif srel is not None and lin.get(srel) == sha:
            kind = "LINEAGE"
        else:
            kind = "FOREIGN"
        hits.append({"path": str(f), "sha256": sha, "class": kind})
    bad = any(h["class"] == "FOREIGN" for h in hits)
    return {"status": LINEAGE if bad else "PASS", "hits": hits, "scanned": n}


def _scanned_files(base, root, skip=()):
    """The files under `base` in C2's scanned set, judged on the path relative to `root` (or to
    the parent of `base` when it lies outside `root`)."""
    base = Path(base)
    if not base.is_dir():
        return
    anchor = root if _under(base, root) else base.parent
    for f in cd._walk(base, skip):
        rel = cd._rel(f, anchor)
        if rel is not None and cd._scanned(rel.split("/")):
            yield f


def hygiene_check(root=None) -> dict:
    """§6.6: no C2ND file of C2's scanned set (tools/c2_nd/ except the protocol copy; the C2ND
    store) contains C2's scope, and no store file contains a parallel round's scope (ND-C35)."""
    root = Path(nc.PROJECT_ROOT if root is None else root)
    own, store = Path(nc.WORKTREE) / "tools" / "c2_nd", Path(nc.STORE)
    hits = []
    for f in _scanned_files(own, root, cd.SKIP_DIRS):
        if f.name != nc.PROTOCOL_FILE.name and cd.contains_scope(f, needle=C2_NEEDLE):
            hits.append(str(f))
    for f in _scanned_files(store, root, cd.SKIP_DIRS + ("sealed",)):
        needles = (C2_NEEDLE,) + PARALLEL_NEEDLES
        if any(cd.contains_scope(f, needle=x) for x in needles):
            hits.append(str(f))
    return {"status": LINEAGE if hits else "PASS", "hits": hits}


# ---- store admission (§3 row 1 (vii); §10.2; API.md §4.3) ------------------------------------
PAYLOAD_DIRS = ("hist", "oracle", "fits", "decoys", "registry", "stages", "sealed")
ND_PAYLOAD = tuple(d for d in PAYLOAD_DIRS if d not in cd.PAYLOAD_DIRS)  # decoys, registry


def store_admission(store, lineage, first_sampling) -> dict:
    """c2_data.store_admission, and at first sampling also no file under decoys/ or registry/."""
    out = dict(cd.store_admission(store, lineage, first_sampling))
    if first_sampling and Path(store).is_dir():
        extra = [
            cd._rel(f, store)
            for f in cd._walk(Path(store))
            if cd._rel(f, store).split("/")[0] in ND_PAYLOAD
        ]
        out["payload"] = list(out["payload"]) + extra
        if extra:
            out["status"] = LINEAGE
    return out


def own_records(store, stage, lineage) -> dict:
    return cd.own_records(store, stage, lineage)
