"""D-2a world, pools, seed map, bins, templates and S0 bindings (D2A-FROZEN-v1 §2, §9.2, §11.3;
tools/d2a/API.md §2.1, §3). D-1's 4x3 construction is imported unchanged from tools/d1_seam."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from itertools import product
from pathlib import Path

import numpy as np

from topo_pilot.analysis import percentile_interval
from topo_pilot.contracts import ErrorCode, ObservationSet, SeedTree, SequenceLayout, StageFailure
from topo_pilot.dataset import HMMSampler

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ROOT = REPO.parent
for _p in (HERE, REPO / "tools" / "d1_seam", REPO / "tools" / "x4_oracle_profile"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import d1_seam as d1  # noqa: E402  (unchanged D-1 module)

STORE = ROOT / "d2a-store"
DATA, MODEL = 2026101531, 2026101532
CHUNK = 4096
POSITIONS = (16, 28)
BINS = ((1, 8, 16), (2, 17, 24), (3, 25, 31))
S2 = (3, 4, 8, 9)
S3 = (3, 4, 15, 16, 18, 19, 20, 21, 23, 24, 33, 34, 40, 41, 43, 44, 45, 46, 48, 49, 53, 54,
      58, 59)
S0_, S2_, S3_, A_, B_ = d1.S0, d1.S2, d1.S3, d1.A, d1.B
POOLS: dict[str, tuple] = {}
for _s in (1, 2, 3, 4):
    POOLS[f"train-s{_s}"] = ("CM", 2**18, "train", _s)
for _s in (1, 2, 3, 4):
    POOLS[f"dev-s{_s}"] = ("CM", 2**12, "dev", _s)
for _s in (1, 2):
    POOLS[f"trainN-s{_s}"] = ("CC", 2**18, "train", _s)
for _s in (1, 2):
    POOLS[f"devN-s{_s}"] = ("CC", 2**12, "dev", _s)
POOLS.update({"stage0": ("CM", 2**16, "dev", None), "stage0N": ("CC", 2**14, "dev", None),
              "cal": ("CM", 2**16, "dev", None), "val": ("CM", 2**14, "dev", None),
              "test": ("CM", 2**16, "test", None), "valN": ("CC", 2**14, "dev", None),
              "testN": ("CC", 2**14, "test", None)})
SEQ_CODE = {name: i + 1 for i, name in enumerate(POOLS)}
GUARDED = ("test", "testN")
PROTECTED = ("src", "configs/stages.yaml", "docs/proposals/X4F_EXECUTION_PROTOCOL_V2.md",
             "docs/proposals/X4F_GATES_API.md", "tools/d1_seam", "tools/x4_oracle_profile",
             "tools/check_imports.py", "tools/check_file_sizes.py", "tools/d2a", "tests/learner",
             "tests/activations", "tests/experiment", "tests/dataset", "tests/oracle",
             "tests/oracle_profile", "tests/d1_seam", "tests/world", "tests/process",
             "tests/d2a")
ALLOWED_A = ("src/topo_pilot/learner/multihorizon.py", "tests/learner/test_multihorizon.py",
             "tests/learner/test_trainer_golden.py", "tests/learner/golden_default_trainer.json")
PROTOCOL = ROOT / "agent-handoff/planning/responses/D2A-FROZEN-v1.md"
PROTOCOL_SHA = "CBE3117F70DD7BA95046FA11D510132682A377782321A97723BE77E269C1C90B"
_FM: dict = {}


def _float_model() -> dict:
    if not _FM:
        _FM.update(d1.float_model())
    return _FM


def process(proc: str) -> dict:
    """``{"T", "E", "mu"}`` of the CM mixture or the C⊕C null (blockdiag(T_C, T_C))."""
    fm = _float_model()
    if proc == "CM":
        return {"T": fm["T"].copy(), "E": fm["E_mix"].copy(), "mu": fm["mu"].copy()}
    if proc == "CC":
        z = np.zeros_like(fm["T_C"])
        return {"T": np.block([[fm["T_C"], z], [z, fm["T_C"]]]), "E": fm["E_mix"].copy(),
                "mu": fm["mu"].copy()}
    raise StageFailure(ErrorCode.INVALID_CONFIG, "d2a.world", "proc", f"unknown {proc!r}")


def world_kernels(proc: str) -> dict:
    """Per-block filters: ``T_C``, ``T_M`` (``T_C`` twice for CC), ``E``, ``mu_C``, ``mu_M``."""
    fm = _float_model()
    second = fm["T_M"] if proc == "CM" else fm["T_C"]
    return {"T_C": fm["T_C"].copy(), "T_M": second.copy(), "E": fm["E"].copy(),
            "mu_C": fm["mu_C"].copy(), "mu_M": fm["mu_M"].copy()}


def stream(pool: str) -> tuple:
    proc, _, _, seed = POOLS[pool]
    if pool.startswith(("train", "dev")):
        return ("d2a", "train" if pool.startswith("train") else "dev", proc, seed)
    return ("d2a", pool[:-1] if proc == "CC" else pool, proc)


def pool_generator(pool: str) -> np.random.Generator:
    return SeedTree(DATA).generator(*stream(pool))


def sequence_ids(pool: str) -> np.ndarray:
    return SEQ_CODE[pool] * 2**32 + np.arange(POOLS[pool][1], dtype=np.int64)


def sample_pool(pool: str) -> tuple[np.ndarray, np.ndarray]:
    proc, n = POOLS[pool][:2]
    p = process(proc)
    return HMMSampler(p["T"], p["E"], p["mu"], SequenceLayout()).sample(n, pool_generator(pool))


def decision_rows(tokens: np.ndarray, t: int) -> np.ndarray:
    return np.flatnonzero(np.asarray(tokens)[:, t - 1] == S3_)


def bin_positions(tokens: np.ndarray, pool: str) -> np.ndarray:
    """``[3, R]``: per bin one decision t chosen uniformly (registered stream), or 0."""
    tok = np.asarray(tokens)
    out = np.zeros((len(BINS), tok.shape[0]), dtype=np.int64)
    for b, lo, hi in BINS:
        u = SeedTree(DATA).generator("d2a", "bin", pool, b).random(tok.shape[0])
        ts = np.arange(lo, hi + 1)
        mask = tok[:, lo - 1:hi] == S3_
        k = mask.sum(axis=1)
        pick = np.floor(u * k).astype(np.int64)
        for r in np.flatnonzero(k):
            out[b - 1, r] = ts[mask[r]][pick[r]]
    return out


def pad(history) -> np.ndarray:
    row = np.full(33, S0_, dtype=np.uint8)
    row[:len(history)] = np.asarray(history, dtype=np.uint8)
    return row


def template_enumeration(t: int) -> list[tuple[tuple, tuple]]:
    """All equal-gap template pairs at t (§9.2), in the API.md order."""
    n = (t - 12) // 2
    pairs = []
    for r1 in (A_, B_):
        for r9 in (A_, B_):
            for exc in product((S2_, S0_), repeat=n):
                for j in range(n + 1):
                    members = []
                    for x5 in (A_, B_):
                        h = [r1, S2_, S3_, S0_, x5, S2_, S3_, S0_, r9, S2_, S3_]
                        if j == 0:
                            h.append(S3_)
                        for i, e in enumerate(exc, start=1):
                            h += [e, S3_]
                            if j == i:
                                h.append(S3_)
                        members.append(tuple(h))
                    pairs.append((members[0], members[1]))
    return pairs


def registered_templates(t: int) -> list[tuple[tuple, tuple]]:
    pairs = template_enumeration(t)
    if t == 16:
        return pairs
    idx = SeedTree(DATA).generator("d2a", "templates", 28).choice(len(pairs), 256, replace=False)
    return [pairs[int(i)] for i in idx]


def template_hashes(t: int) -> list[str]:
    return [hashlib.sha256(bytes(a + b)).hexdigest() for a, b in registered_templates(t)]


def coverage(tokens: np.ndarray, pool: str) -> dict:
    bins = bin_positions(tokens, pool)
    return {"decision_rows": {str(t): int(decision_rows(tokens, t).size) for t in POSITIONS},
            "bin_rows": {str(b): int((bins[b - 1] > 0).sum()) for b, _, _ in BINS}}


def open_store(store_root=STORE):
    from topo_pilot.contracts import ArtifactStore
    from topo_pilot.contracts.backends import LocalFSBackend

    return ArtifactStore(LocalFSBackend(Path(store_root) / "store"), producer_version="d2a-0028")


def _sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_pools(store_root=STORE) -> dict:
    """Sample and save all 21 pools (POOLS order) once; write pools.json (refuses if present)."""
    root = Path(store_root)
    index = root / "pools.json"
    if index.exists():
        raise StageFailure(ErrorCode.INVALID_CONFIG, "d2a.world", "pools", "pools.json exists")
    (root / "private").mkdir(parents=True, exist_ok=True)
    store, out = open_store(root), {}
    for pool, (proc, n, split, seed) in POOLS.items():
        tokens, states = sample_pool(pool)
        obs = ObservationSet(split=split, V=5, sequence_id=sequence_ids(pool), tokens=tokens)
        cfg = {"d2a_pool": pool, "proc": proc, "n": n, "master": DATA,
               "stream": list(stream(pool))}
        seeds = SeedTree(DATA)
        seeds.seed(*stream(pool))
        oid = store.save(obs, config=cfg, parents=[], seed_map=dict(seeds.issued),
                         consumer="experiment")
        side = root / "private" / f"{pool}.npz"
        with side.open("xb") as f:
            np.savez(f, states=states.astype(np.uint8), Z=states[:, 0] >= 12)
        out[pool] = {"id": oid, "payload_sha256": store.meta(oid).payload_sha256,
                     "sidecar_sha256": _sha(side), "proc": proc, "n": n, "split": split,
                     "coverage": coverage(tokens, pool)}
    with index.open("x", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    return out


def _guard(pool: str) -> None:
    if pool in GUARDED and os.environ.get("D2A_STAGE") != "3":
        raise StageFailure(ErrorCode.LEAKAGE, "d2a.world", "test_guard",
                           f"pool {pool!r} is readable in stage 3 only (S9)")


def pool_index(store_root=STORE) -> dict:
    return json.loads((Path(store_root) / "pools.json").read_text(encoding="utf-8"))


def load_tokens(pool: str, store_root=STORE) -> np.ndarray:
    _guard(pool)
    rec = pool_index(store_root)[pool]
    obs = open_store(store_root).load(ObservationSet, rec["id"], consumer="experiment")
    return np.asarray(obs.tokens)


def load_private(pool: str, store_root=STORE) -> tuple[np.ndarray, np.ndarray]:
    _guard(pool)
    path = Path(store_root) / "private" / f"{pool}.npz"
    if _sha(path) != pool_index(store_root)[pool]["sidecar_sha256"]:
        raise StageFailure(ErrorCode.CHECKSUM_MISMATCH, "d2a.world", "sidecar", pool)
    with np.load(path) as z:
        return z["states"], z["Z"]


def master_collisions(roots) -> list[str]:
    """meta.json files whose seed_map values or config text contain DATA or MODEL (§2.6)."""
    hits = []
    for root in roots:
        for meta in sorted(Path(root).rglob("meta.json")):
            try:
                m = json.loads(meta.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            vals = {int(v) for v in (m.get("seed_map") or {}).values()
                    if isinstance(v, int) and not isinstance(v, bool)}
            text = json.dumps(m.get("config", {}))
            if vals & {DATA, MODEL} or str(DATA) in text or str(MODEL) in text:
                hits.append(str(meta))
    return hits


def _git(*args) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True,
                          check=True).stdout


def protected_diff(R: str = "2babe9d", H: str = "HEAD") -> tuple[list[str], list[str]]:
    """(entries, violations) of ``git diff --no-renames --name-status R H -- PROTECTED``."""
    entries = [ln for ln in _git("diff", "--no-renames", "--name-status", R, H, "--",
                                 *PROTECTED).splitlines() if ln.strip()]
    bad = []
    for ln in entries:
        status, path = ln.split("\t", 1)
        ok = (status == "M" and path == "src/topo_pilot/learner/trainer.py") or (
            status == "A" and (path in ALLOWED_A or path.startswith(("tools/d2a/",
                                                                      "tests/d2a/"))))
        if not ok:
            bad.append(ln)
    return entries, bad


def s0_bindings(job_id: str, task_sha256: str, session: str, store_root=STORE,
                mailbox=ROOT / "agent-handoff") -> dict:
    """Gate 1 (§10.6): protocol hash, dispatch identities, pinned commit, protected-path diff,
    master freshness. Returns the record; ``status`` is PASS or FAIL."""
    import d2a_train

    checks, rec = {}, {}
    sha = _sha(PROTOCOL).upper()
    recorded = (PROTOCOL.parent / "D2A-FROZEN-v1.sha256").read_text().split()[0].upper()
    checks["protocol_hash"] = sha == recorded == PROTOCOL_SHA
    try:
        d2a_train.verify_identity(mailbox, job_id, task_sha256, session,
                                  Path(store_root) / "RUN.lock")
        checks["identity"] = True
    except StageFailure as exc:
        checks["identity"], rec["identity_error"] = False, exc.detail
    head = _git("rev-parse", "HEAD").strip()
    dirty = [ln for ln in _git("status", "--porcelain").splitlines() if ln.strip()]
    checks["commit_pinned"] = not dirty
    entries, bad = protected_diff("2babe9d", head)
    checks["protected_diff"] = not bad
    roots = [ROOT / "topo-pilot/artifacts", ROOT / "d1-seam-oracle-store",
             ROOT / "x2a-stage0-oracle-store", ROOT / "c1prime-store"]
    hits = master_collisions(roots)
    checks["masters_fresh"] = not hits
    rec.update(protocol_sha256=sha, execution_commit=head, dirty=dirty, diff=entries,
               violations=bad, collisions=hits, job_id=job_id, task_sha256=task_sha256,
               session=session, checks=checks,
               status="PASS" if all(checks.values()) else "FAIL")
    return rec


# Episode-cluster bootstrap and pooled-R² primitives (API §2.5; used by d2a_decide, d2a_eval)

def boot_counts(n: int, B: int, scope, chunk: int = 250):
    """Episode-cluster resamples as count matrices ``[b, n]`` (registered ``boot`` stream)."""
    rng = SeedTree(DATA).generator("d2a", "boot", *scope)
    for start in range(0, B, chunk):
        idx = rng.integers(0, n, size=(min(chunk, B - start), n))
        yield np.stack([np.bincount(r, minlength=n) for r in idx]).astype(np.int32)


def boot_totals(columns, B: int, scope) -> np.ndarray:
    """``[B, k]`` resampled totals of per-episode columns ``[n, k]``."""
    cols = np.asarray(columns, float)
    return np.concatenate([c @ cols for c in boot_counts(cols.shape[0], B, scope)])


def r2_columns(n: int, ep, Y, pred, mean_cal) -> np.ndarray:
    """Per-episode ``(sse, sst, count)`` for the pooled R² with the calibration mean."""
    Y, P = np.asarray(Y, float).reshape(len(ep), -1), np.asarray(pred, float).reshape(len(ep), -1)
    out = np.zeros((n, 3))
    out[ep, 0] = ((Y - P) ** 2).sum(1)
    out[ep, 1] = ((Y - np.asarray(mean_cal, float).reshape(1, -1)) ** 2).sum(1)
    out[ep, 2] = Y.shape[1]
    return out


def r2_from_sums(sse, sst, count) -> np.ndarray:
    """``1 - sse/sst``; NaN where ``sst ≤ 1e-12·count``, and NaN inputs propagate (6c)."""
    sse, sst = np.asarray(sse, float), np.asarray(sst, float)
    ok = sst > 1e-12 * np.asarray(count, float)
    return np.where(ok, 1.0 - sse / np.where(ok, sst, 1.0), np.nan)


def ratio_from_sums(num, den) -> np.ndarray:
    num, den = np.asarray(num, float), np.asarray(den, float)
    ok = np.isfinite(den) & (den > 0)
    return np.where(ok, num / np.where(ok, den, 1.0), np.nan)


def quantiles(draws, qs) -> list | None:
    """None when any draw is undefined: the interval is invalidated, never redrawn (§6)."""
    d = np.asarray(draws, float)
    if d.size == 0 or not np.all(np.isfinite(d)):
        return None
    return [float(v) for v in np.quantile(d, qs, method="linear")]


def interval(draws) -> tuple | None:
    d = np.asarray(draws, float)
    return None if d.size == 0 or not np.all(np.isfinite(d)) else percentile_interval(d)


def beta_draws(ep, r, d, n, B, scope, extra=None) -> dict:
    """Point and resampled β = Σrd/Σd² (and Σ r8·d for the window baseline), per episode."""
    r, d = np.asarray(r, float).reshape(len(ep), -1), np.asarray(d, float).reshape(len(ep), -1)
    cols = np.zeros((n, 3))
    np.add.at(cols[:, 0], ep, (r * d).sum(1))
    np.add.at(cols[:, 1], ep, (d * d).sum(1))
    if extra is not None:
        np.add.at(cols[:, 2], ep, (np.asarray(extra, float).reshape(len(ep), -1) * d).sum(1))
    tot, pt = boot_totals(cols, B, scope), cols.sum(0)
    return {"point": ratio_from_sums(pt[0], pt[1]).item(), "point8": ratio_from_sums(pt[2], pt[1])
            .item(), "draws": ratio_from_sums(tot[:, 0], tot[:, 1]),
            "draws8": ratio_from_sums(tot[:, 2], tot[:, 1])}


def pooled_r2(cols: list, B: int, scope) -> tuple:
    """``(point(i), draws(i))``: pooled R² of the i-th stacked ``(sse, sst, count)`` triple."""
    allc = np.hstack(cols)
    tot, pt = boot_totals(allc, B, scope), allc.sum(0)

    def r2(x, i):
        return r2_from_sums(x[..., 3 * i], x[..., 3 * i + 1], x[..., 3 * i + 2])

    return (lambda i: r2(pt, i).item()), (lambda i: r2(tot, i))
