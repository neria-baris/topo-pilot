"""HWSB data: process build, streams, IDs, sampling, blocks, H2-B, registry reader (API.md §2).

Protocol §2.3 (streams, scopes, sampling as DatasetStage._sample_all), §6.3 (registry entry).
B9a reads and hashes stage B's OWN history payloads (ObservationSet payload.npz, hist/*.npz)
inside its own store (ruling c7); no other store's payload is opened or hashed.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
import hashlib
from fractions import Fraction
from pathlib import Path

import c1_model
import numpy as np
import oracle_profile
import scores
import stage_records

from topo_pilot.contracts import (
    EmissionSpec,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
    TransitionSpec,
    WorldSpec,
    payload_checksum,
)
from topo_pilot.dataset import HMMSampler
from topo_pilot.dataset.checks import (
    check_disjoint,
    check_first_token,
    check_ranges,
    make_sequence_ids,
    process_code,
)
from topo_pilot.dataset.public import assert_public
from topo_pilot.process.stage import ProcessStage
from topo_pilot.world.stage import WorldStage

READER = "experiment"
ROLES = ("train", "dev", "LGATE", "CAL", "VAL")
BLOCKS = ("LGATE", "CAL", "VAL")
IDENTITY, SAMPLER = "FAIL_TECHNICAL/IDENTITY", "FAIL_TECHNICAL/SAMPLER"
LINEAGE, REGISTRY = "FAIL_TECHNICAL/LINEAGE", "FAIL_TECHNICAL/REGISTRY"


def _check_perm(perm, V) -> np.ndarray:
    perm = np.asarray(perm, dtype=np.int64)
    if (
        perm.shape != (V,)
        or not np.array_equal(np.sort(perm), np.arange(V))
        or not np.array_equal(perm[np.argsort(perm)], np.arange(V))
    ):
        raise hc.HwsbStop(IDENTITY, "symbol_perm is not a permutation with an exact round trip")
    return perm


def assemble(world, trans, emissions, ids, features=None, n_axial=6) -> dict:
    """The process dict of API §2.1 from loaded specs (also used by the dry tiny world)."""
    T = np.asarray(trans.T, dtype=np.float64)
    pi = np.asarray(trans.pi, dtype=np.float64)
    coords = np.asarray(world.coords, dtype=np.float64)
    E_named, perm, E_canon = {}, {}, {}
    for m, spec in emissions.items():
        E_named[m] = np.asarray(spec.E, dtype=np.float64)
        perm[m] = _check_perm(spec.symbol_perm, E_named[m].shape[1])
        E_canon[m] = oracle_profile.canonical_emission(E_named[m], perm[m])
    first = E_canon[next(iter(E_canon))]
    if any(e.tobytes() != first.tobytes() or e.shape != first.shape for e in E_canon.values()):
        raise hc.HwsbStop(IDENTITY, "canonical emissions differ between masters")
    try:
        oracle_profile.validate_process(T, first, pi, 1e-12)
    except oracle_profile.ProfileError as exc:
        raise hc.HwsbStop(IDENTITY, f"validate_process: {exc}") from exc
    dims = tuple(int(d) for d in world.dims) if hasattr(world, "dims") else (12, 12)
    feats = oracle_profile.circle_features(coords) if features is None else features
    return {
        "ids": ids,
        "T": T,
        "pi": pi,
        "coords": coords,
        "features": feats,
        "E_named": E_named,
        "perm": perm,
        "E_canon": E_canon,
        "E_canon_shared": first,
        "V": int(first.shape[1]),
        "N": int(T.shape[0]),
        "W": dims[0],
        "Hh": dims[-1],
        "n_axial": int(n_axial),
    }


def build_process(
    store,
    masters=hc.MASTERS,
    emission_cfg=hc.EMIS_CFG,
    world_cfg=hc.WORLD_CFG,
    transition_cfg=hc.TRANS_CFG,
) -> dict:
    wid = WorldStage().run(world_cfg, store)
    tid = ProcessStage().run_transition(wid, transition_cfg, store)
    eid = {
        int(m): ProcessStage().run_emission(wid, emission_cfg, SeedTree(int(m)), store)
        for m in masters
    }
    world = store.load(WorldSpec, wid, consumer=READER)
    trans = store.load(TransitionSpec, tid, consumer=READER)
    ems = {m: store.load(EmissionSpec, e, consumer=READER) for m, e in eid.items()}
    proc = assemble(world, trans, ems, {"world": wid, "transition": tid, "emission": eid})
    proc["sigma"] = Fraction(repr(float(emission_cfg.sigma)))
    proc["neighbour"] = (1 - Fraction(repr(float(transition_cfg.p_stay)))) / 4
    return proc


def _sha_array(x) -> str:
    return hashlib.sha256(np.ascontiguousarray(x, dtype=np.float64).tobytes()).hexdigest()


def arrays_sha256(proc) -> dict:
    return {
        "T": _sha_array(proc["T"]),
        "E": _sha_array(proc["E_canon_shared"]),
        "pi": _sha_array(proc["pi"]),
        "coords": _sha_array(proc["coords"]),
    }


def spec_checksums(store, proc) -> dict:
    ids = proc["ids"]

    def ck(cls, aid):
        return payload_checksum(*store.load(cls, aid, consumer=READER).to_payload())

    return {
        "WorldSpec": ck(WorldSpec, ids["world"]),
        "TransitionSpec": ck(TransitionSpec, ids["transition"]),
        "EmissionSpec": {m: ck(EmissionSpec, e) for m, e in ids["emission"].items()},
    }


def _check_role(role, plan, master, tree=None) -> None:
    if role not in ROLES:
        raise ValueError(f"unknown role {role!r}")
    if role in ("train", "dev"):
        if master is None:
            raise ValueError(f"role {role} needs a master")
        allowed = hc.DRY_MASTERS if plan.dry else hc.MASTERS
        if int(master) not in plan.masters or int(master) not in allowed:
            raise ValueError(f"master {master!r} not allowed for plan {plan.kind}")
        if tree is not None and int(tree.master) != int(master):
            raise ValueError("tree master differs from master")
    elif master is not None or tree is not None:
        raise ValueError(f"block role {role} takes no master")


def stream_record(role, plan, master=None) -> list:
    _check_role(role, plan, master)
    base = ["data", hc.SCOPE] + (["DRY", plan.key, role] if plan.dry else [role, hc.KEY])
    return base + ([int(master)] if master is not None else [])


def data_generator(role, plan, master=None, tree=None):
    _check_role(role, plan, master, tree)
    scope = stream_record(role, plan, master)[1:]
    t = tree if tree is not None else SeedTree(int(master) if master is not None else 0)
    return t.generator("data", *scope)


def sequence_ids(role, n, plan, master=None) -> np.ndarray:
    _check_role(role, plan, master)
    rep = f"hwsb-v1/DRY/{plan.key}/{role}" if plan.dry else f"hwsb-v1/{role}"
    if role in ("train", "dev"):
        rep += f"/{int(master)}"
    split = role if role in ("train", "dev") else "test"
    return make_sequence_ids(process_code(*plan.process, rep), split, int(n))


def _checks(tokens, states, V, N, p_w, split) -> None:
    try:
        check_ranges(tokens, states, V, N)
        check_first_token(tokens[:, 0], p_w, split)
    except StageFailure as exc:
        raise hc.HwsbStop(SAMPLER, f"{split}: {exc}") from exc


def sample_observations(T, E_named, pi, perm, n, rng, split, layout=None) -> np.ndarray:
    """One split of DatasetStage._sample_all: canonical draw, named = perm[canonical]."""
    layout = layout or SequenceLayout()
    perm = np.asarray(perm, dtype=np.int64)
    E_named = np.asarray(E_named, dtype=np.float64)
    N, V = E_named.shape
    canon, states = HMMSampler(T, E_named[:, perm], pi, layout).sample(int(n), rng)
    tokens = perm[canon.astype(np.int64)].astype(canon.dtype)
    _checks(tokens, states, V, N, np.asarray(pi) @ E_named, split)
    del states
    return tokens


def sample_block(T, E_canon, pi, n, rng, layout=None) -> np.ndarray:
    layout = layout or SequenceLayout()
    E_canon = np.asarray(E_canon, dtype=np.float64)
    N, V = E_canon.shape
    tokens, states = HMMSampler(T, E_canon, pi, layout).sample(int(n), rng)
    _checks(tokens, states, V, N, np.asarray(pi) @ E_canon, "test")
    del states
    out = np.ascontiguousarray(tokens[:, :32], dtype=np.uint8)
    del tokens
    return out


def canonical32(named, perm) -> np.ndarray:
    return scores.canonical_from_named(np.asarray(named)[:, :32], np.asarray(perm)).astype(np.uint8)


def named32(canon32, perm) -> np.ndarray:
    return np.asarray(perm)[np.asarray(canon32, dtype=np.int64)].astype(np.uint8)


def model_inputs(canon32, perm):
    """[BOS, named w1..w32]: c1_model.model_inputs (BOS 36) for V = 36; BOS = V otherwise
    (the dry tiny world, V = 3)."""
    named = named32(canon32, perm)
    if len(perm) == hc.BOS:
        return c1_model.model_inputs(named)
    import torch

    bos = np.full((named.shape[0], 1), len(perm), dtype=np.int64)
    return torch.from_numpy(np.hstack((bos, named.astype(np.int64))))


def make_train_dev(store, proc, master, plan) -> dict:
    m, tree = int(master), SeedTree(int(master))
    tok, ids = {}, {}
    for split in ("train", "dev"):
        n = int(plan.sizes[split])
        tok[split] = sample_observations(
            proc["T"],
            proc["E_named"][m],
            proc["pi"],
            proc["perm"][m],
            n,
            data_generator(split, plan, m, tree),
            split,
        )
        ids[split] = sequence_ids(split, n, plan, m)
    check_disjoint(train=ids["train"], dev=ids["dev"])
    out = {"streams": {}, "n": {}}
    for split in ("train", "dev"):
        obs = assert_public(
            ObservationSet(split=split, V=proc["V"], sequence_id=ids[split], tokens=tok[split])
        )
        cfg = {
            "family": "cylinder",
            "mode": "overlap",
            "sigma": plan.process[2],
            "V": proc["V"],
            "N": proc["N"],
            "split": split,
            "n": int(plan.sizes[split]),
            "replicate": m,
            "study": hc.SCOPE,
            "key": plan.key,
        }
        out[split] = store.save(
            obs,
            config=cfg,
            parents=[proc["ids"]["transition"], proc["ids"]["emission"][m]],
            seed_map=dict(tree.issued),
            consumer="dataset",
        )
        out["streams"][split] = stream_record(split, plan, m)
        out["n"][split] = int(plan.sizes[split])
    return out


def make_block(proc, role, plan) -> dict:
    if role not in BLOCKS:
        raise ValueError(f"not a block role: {role!r}")
    n = int(plan.sizes[role])
    canon32 = sample_block(
        proc["T"], proc["E_canon_shared"], proc["pi"], n, data_generator(role, plan)
    )
    return {
        "role": role,
        "canon32": canon32,
        "seq_ids": sequence_ids(role, n, plan),
        "digest_canon32": scores.history_digests(canon32),
        "stream": stream_record(role, plan),
    }


def lowest_rows(seq_ids, n=hc.PANEL) -> np.ndarray:
    order = np.argsort(np.asarray(seq_ids), kind="stable")[: int(n)]
    return np.sort(order).astype(np.int64)


def save_block(out, block) -> Path:
    d = Path(out) / "hist"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{block['role']}.npz"
    stage_records.save_npz(
        path,
        canon32=np.ascontiguousarray(block["canon32"], dtype=np.uint8),
        seq_ids=np.asarray(block["seq_ids"], dtype=np.int64),
        digest_canon32=np.asarray(block["digest_canon32"], dtype="<U64"),
    )
    return path


def load_block(path) -> dict:
    try:
        with np.load(path, allow_pickle=False) as z:
            keys = set(z.files)
            a = {k: z[k] for k in keys}
    except Exception as exc:  # noqa: BLE001  unreadable -> lineage defect
        raise hc.HwsbStop(LINEAGE, f"{path}: unreadable ({type(exc).__name__}: {exc})") from exc
    if keys != {"canon32", "seq_ids", "digest_canon32"}:
        raise hc.HwsbStop(LINEAGE, f"{path}: keys {sorted(keys)}")
    c, s, d = a["canon32"], a["seq_ids"], a["digest_canon32"]
    n = c.shape[0] if c.ndim == 2 else -1
    if (
        c.dtype != np.uint8
        or c.ndim != 2
        or c.shape[1] != 32
        or s.dtype != np.int64
        or s.shape != (n,)
        or d.dtype != np.dtype("<U64")
        or d.shape != (n,)
    ):
        raise hc.HwsbStop(LINEAGE, f"{path}: dtypes or shapes")
    if scores.history_digests(c) != [str(x) for x in d]:
        raise hc.HwsbStop(LINEAGE, f"{path}: digest column does not match canon32")
    role = Path(path).stem
    return {"role": role, "canon32": c, "seq_ids": s, "digest_canon32": [str(x) for x in d]}


_REGISTRY_NAMES = ("train_dev_canonical", "hws_store_digests", "duplicates", "separation",
                   "history_inventory", "registry_digests")


def __getattr__(name):
    """API names that live in hwsb_registry (split by size), re-exported lazily."""
    if name in _REGISTRY_NAMES:
        import hwsb_registry

        return getattr(hwsb_registry, name)
    raise AttributeError(f"module 'hwsb_data' has no attribute {name!r}")
