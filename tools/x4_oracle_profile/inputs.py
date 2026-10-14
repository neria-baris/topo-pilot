"""Read-only inputs for job 0014: hashes, process artifacts, histories and environment.

Only WorldSpec, TransitionSpec and EmissionSpec payloads are opened (never checkpoints or
state.pt). Artifact identity uses the repository checksum convention
(``topo_pilot.contracts.base.payload_checksum``) plus the manifest's metadata and payload hashes.
The original feasibility runner/core are NOT imported.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
from oracle_profile import ProfileError, canonical_emission, circle_features, validate_process

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CONFIG_PATH = HERE / "config.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def sha256(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump_json(path, obj) -> None:
    path = Path(path)
    if path.exists():
        raise ProfileError(f"immutable output already exists: {path.name}")
    data = json.dumps(obj, indent=1, sort_keys=True, allow_nan=False) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(data)


def verify_input_hashes(cfg: dict) -> dict:
    store = Path(cfg["input_store"])
    found = {name: sha256(store / name) for name in cfg["inputs_sha256"]}
    bad = {k: v for k, v in found.items() if v != cfg["inputs_sha256"][k]}
    if bad:
        raise ProfileError(f"input hash mismatch: {bad}")
    return found


def _manifest(cfg: dict) -> dict:
    return json.loads((Path(cfg["input_store"]) / "INPUT_IDENTITIES.json").read_text())


def load_artifact(cfg: dict, kind: str, artifact_id: str) -> tuple[dict, dict, dict]:
    """Verify meta hash, status, payload hash and canonical payload checksum; return arrays."""
    from topo_pilot.contracts.base import payload_checksum

    if kind not in ("WorldSpec", "TransitionSpec", "EmissionSpec"):
        raise ProfileError(f"artifact kind {kind} not permitted")
    manifest = _manifest(cfg)
    expected = manifest["artifacts"][f"{kind}/{artifact_id}"]
    root = Path(manifest["artifact_root"]) / kind / artifact_id
    meta = json.loads((root / "meta.json").read_text())
    if sha256(root / "meta.json") != expected["meta_sha256"]:
        raise ProfileError(f"meta.json hash mismatch {kind}/{artifact_id}")
    if meta["status"] != "complete" or meta["payload_sha256"] != expected["sha256"]:
        raise ProfileError(f"metadata identity {kind}/{artifact_id}")
    extra = json.loads((root / "extra.json").read_text())
    with np.load(root / "payload.npz", allow_pickle=False) as payload:
        arrays = {name: payload[name] for name in payload.files}
    if payload_checksum(arrays, extra) != expected["sha256"]:
        raise ProfileError(f"payload checksum mismatch {kind}/{artifact_id}")
    record = {
        "meta_sha256": expected["meta_sha256"],
        "payload_checksum": expected["sha256"],
        "payload_npz_file_sha256": sha256(root / "payload.npz"),
        "extra_json_file_sha256": sha256(root / "extra.json"),
    }
    return arrays, extra, record


def _expected_edges(coords: np.ndarray, period: int) -> set:
    index = {(int(x), int(y)): s for s, (x, y) in enumerate(coords)}
    edges = set()
    for (x, y), s in index.items():
        for nx, ny in (((x + 1) % period, y), (x, y + 1)):
            if (nx, ny) in index:
                edges.add((min(s, index[(nx, ny)]), max(s, index[(nx, ny)])))
    return edges


def world_identity(cfg: dict, world: dict, extra: dict, T: np.ndarray) -> dict:
    """12x12 cylinder (x periodic) from coords; stored edges and T support match that lattice."""
    coords = np.asarray(world["coords"], dtype=np.float64)
    nx, ny = cfg["world"]["dims"]
    if coords.shape != (nx * ny, 2) or np.any(coords != np.round(coords)):
        raise ProfileError("coords shape/integrality")
    pairs = {(int(x), int(y)) for x, y in coords}
    if pairs != {(x, y) for x in range(nx) for y in range(ny)}:
        raise ProfileError("coords are not the full 12x12 lattice")
    if extra.get("family") != "cylinder" or extra.get("identifications") != ["x periodic"]:
        raise ProfileError("world family/identifications")
    expected = _expected_edges(coords, nx)
    stored = {tuple(sorted(map(int, e))) for e in np.asarray(world["edges"])}
    if stored != expected or len(expected) != cfg["world"]["edges"]:
        raise ProfileError("stored world edges differ from the x-periodic lattice")
    tc, p_stay, d_max = cfg["transition"], cfg["transition"]["p_stay"], cfg["transition"]["d_max"]
    rebuilt = np.zeros_like(T)
    for i, j in expected:
        rebuilt[i, j] = rebuilt[j, i] = (1.0 - p_stay) / d_max
    rebuilt[np.diag_indices_from(rebuilt)] = 1.0 - rebuilt.sum(axis=1)
    t_err = float(np.max(np.abs(rebuilt - T)))
    if t_err > cfg["tolerances"]["process"] or tc["kind"] != "max_degree_lazy_walk":
        raise ProfileError(f"T differs from the lazy max-degree walk on coords: {t_err}")
    return {
        "states": int(coords.shape[0]),
        "edges": len(expected),
        "T_rebuild_max_abs": t_err,
        "x_values": sorted({int(x) for x in coords[:, 0]}),
        "state_order": "coords row s",
    }


def emission_identity(
    cfg: dict, coords: np.ndarray, E_canon: np.ndarray, centers: np.ndarray
) -> float:
    """Rebuild E_canon = softmax_j(-d(z, c_j)^2 / 2 sigma^2) on the x-periodic flat chart."""
    rb = cfg["emission_rebuild"]
    k = rb["grid_side"]
    a, b = np.meshgrid(np.arange(k), np.arange(k), indexing="ij")
    grid = np.stack([0.5 + 2.0 * a.ravel(), 0.5 + 2.0 * b.ravel()], axis=1)
    if not np.array_equal(grid, centers):
        raise ProfileError("stored centers differ from the documented grid")
    diff = np.abs(coords[:, None, :] - grid[None, :, :])
    period = float(cfg["world"]["dims"][0])
    wrapped = np.mod(diff[..., 0], period)
    diff[..., 0] = np.minimum(wrapped, period - wrapped)
    logits = -np.sum(diff**2, axis=2) / (2.0 * rb["sigma"] ** 2)
    logits -= logits.max(axis=1, keepdims=True)
    rebuilt = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
    err = float(np.max(np.abs(rebuilt - E_canon)))
    if err > rb["rebuild_tol"]:
        raise ProfileError(f"canonical emission rebuild mismatch {err}")
    return err


def load_process(cfg: dict) -> dict:
    """Verified T, pi, canonical E, named emissions/permutations, features and identity record."""
    world, wextra, wrec = load_artifact(cfg, "WorldSpec", cfg["world"]["artifact"])
    trans, textra, trec = load_artifact(cfg, "TransitionSpec", cfg["transition"]["artifact"])
    if textra.get("event_order") != "emit_then_transition":
        raise ProfileError("transition event order")
    T, pi = np.asarray(trans["T"], np.float64), np.asarray(trans["pi"], np.float64)
    named, perms, centers = {}, {}, {}
    records = {"WorldSpec": wrec, "TransitionSpec": trec}
    for seed, aid in cfg["emissions"].items():
        arrays, _, rec = load_artifact(cfg, "EmissionSpec", aid)
        named[seed], perms[seed] = (
            np.asarray(arrays["E"], np.float64),
            np.asarray(arrays["symbol_perm"]),
        )
        records[f"EmissionSpec/{seed}"] = rec
        centers[seed] = np.asarray(arrays["centers"], np.float64)
    canon = {seed: canonical_emission(named[seed], perms[seed]) for seed in named}
    first = canon[next(iter(canon))]
    tol = cfg["tolerances"]["canonical_emission_atol"]
    spread = max(float(np.max(np.abs(c - first))) for c in canon.values())
    if spread > tol:
        raise ProfileError(f"canonical emissions differ across models: {spread}")
    checks = {
        seed: validate_process(T, canon[seed], pi, cfg["tolerances"]["process"]) for seed in canon
    }
    coords = np.asarray(world["coords"], np.float64)
    identity = world_identity(cfg, world, wextra, T)
    identity["E_rebuild_max_abs"] = {
        seed: emission_identity(cfg, coords, canon[seed], centers[seed]) for seed in canon
    }
    identity["canonical_emission_max_spread"] = spread
    identity["perms_distinct"] = len({tuple(map(int, p)) for p in perms.values()}) == len(perms)
    identity["pi_uniform_max_abs"] = float(np.max(np.abs(pi - 1.0 / pi.size)))
    return {
        "T": T,
        "pi": pi,
        "E": first,
        "E_named": named,
        "perm": perms,
        "features": circle_features(coords),
        "coords": coords,
        "records": records,
        "process_checks": checks,
        "identity": identity,
    }


def load_split(cfg: dict, split: str) -> dict:
    """Load one split with schema, shape, ID, range and finiteness checks."""
    path = Path(cfg["input_store"]) / f"{split}.npz"
    with np.load(path, allow_pickle=False) as payload:
        data = {name: payload[name] for name in payload.files}
    n, length = cfg["splits"][split], cfg["history_length"]
    if set(data) != {"tokens", "m1", "m8", "m32", "r8", "ids"}:
        raise ProfileError(f"{split}: keys {sorted(data)}")
    tokens = data["tokens"]
    if tokens.shape != (n, length) or tokens.dtype.kind not in "iu":
        raise ProfileError(f"{split}: tokens {tokens.shape} {tokens.dtype}")
    if tokens.min() < 0 or tokens.max() > 35:
        raise ProfileError(f"{split}: token range")
    for key in ("m1", "m8", "m32", "r8"):
        if data[key].shape != (n, 2) or not np.isfinite(data[key]).all():
            raise ProfileError(f"{split}: {key} shape/finite")
    ids = [str(v) for v in data["ids"]]
    want = [
        cfg["id_format"].format(split=split, master=cfg["old_master"], index=i) for i in range(n)
    ]
    if ids != want or len(set(ids)) != n:
        raise ProfileError(f"{split}: IDs differ from the documented ordered format")
    data["ids"] = np.asarray(ids)
    return data


def environment() -> dict:
    import numpy
    from threadpoolctl import threadpool_info

    pools = threadpool_info()
    record = {
        "python": sys.version,
        "executable": sys.executable,
        "numpy": numpy.__version__,
        "thread_env": {
            k: os.environ.get(k)
            for k in (
                "OPENBLAS_NUM_THREADS",
                "MKL_NUM_THREADS",
                "OMP_NUM_THREADS",
                "NUMEXPR_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
            )
        },
        "threadpools": [
            {
                k: p.get(k)
                for k in ("user_api", "internal_api", "num_threads", "version", "filepath")
            }
            for p in pools
        ],
        "pid": os.getpid(),
    }
    import topo_pilot

    record["topo_pilot_file"] = topo_pilot.__file__
    if Path(topo_pilot.__file__).resolve().parents[1] != (REPO / "src").resolve():
        raise ProfileError("topo_pilot does not resolve to the research worktree src")
    if any(v != "1" for v in record["thread_env"].values()):
        raise ProfileError("thread environment not pinned to 1")
    if any(p["num_threads"] != 1 for p in record["threadpools"]):
        raise ProfileError("a native thread pool is not single-threaded")
    return record


def peak_working_set() -> int:
    import ctypes
    import ctypes.wintypes as wt

    class Counters(ctypes.Structure):
        _fields_ = [("cb", wt.DWORD), ("PageFaultCount", wt.DWORD)] + [
            (name, ctypes.c_size_t)
            for name in (
                "PeakWorkingSetSize",
                "WorkingSetSize",
                "a",
                "b",
                "c",
                "d",
                "PagefileUsage",
                "PeakPagefileUsage",
            )
        ]

    counters = Counters()
    counters.cb = ctypes.sizeof(counters)
    kernel = ctypes.WinDLL("kernel32")
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    if not ctypes.WinDLL("psapi").GetProcessMemoryInfo(
        ctypes.c_void_p(kernel.GetCurrentProcess()), ctypes.byref(counters), counters.cb
    ):
        raise ProfileError("peak working set unavailable")
    return int(counters.PeakWorkingSetSize)
