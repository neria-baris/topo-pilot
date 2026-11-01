"""Author B shared helpers for tests/hwsd (job 0197). Holds no tests.

Written from tools/hwsd/{PROTOCOL_HWSD_v1.md, API.md, CONTRACT.json, TEST_PLAN.md}
and the public APIs of the reused modules only. Every store and root built here
lives under the caller's pytest tmp_path.
"""

from __future__ import annotations  # noqa: I001

import builtins
import copy
import dataclasses
import hashlib
import importlib
import io
import json
import os
import pathlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for _p in (Path(__file__).resolve().parent, REPO / "tools" / "hwsd"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import hwsd_config as dc  # noqa: E402

import numpy as np  # noqa: E402

import c1_records  # noqa: E402
import hwsb_config  # noqa: E402
import hwsb_data  # noqa: E402
import hwsb_dry  # noqa: E402
import k4b_data  # noqa: E402
import stage_records  # noqa: E402
from topo_pilot.contracts import ArtifactStore, LocalFSBackend  # noqa: E402

C1GateFailure = c1_records.C1GateFailure
UTC = "2026-11-01T12:00:00Z"
GIB = 1024**3


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def norm(p) -> str:
    return os.path.abspath(os.fspath(p)).replace("\\", "/").rstrip("/").lower()


def under(p, d) -> bool:
    a, b = norm(p), norm(d)
    return a == b or a.startswith(b + "/")


def write_json(path, obj) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, sort_keys=True), encoding="utf-8")
    return path


def junk(path, data: bytes = b"\x00junk-bytes-never-opened") -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


class OpenSpy:
    """Records every path opened through open/io.open/os.open/pathlib (Python 3.10)."""

    def __init__(self):
        self.paths: list[str] = []

    def _wrap(self, f):
        def w(p, *a, **k):
            if isinstance(p, (str, os.PathLike)):
                self.paths.append(norm(p))
            return f(p, *a, **k)

        return w

    def install(self, monkeypatch):
        monkeypatch.setattr(builtins, "open", self._wrap(builtins.open))
        monkeypatch.setattr(io, "open", self._wrap(io.open))
        monkeypatch.setattr(os, "open", self._wrap(os.open))
        acc = getattr(pathlib, "_NormalAccessor", None)
        if acc is not None and "open" in vars(acc):
            monkeypatch.setattr(acc, "open", staticmethod(self._wrap(vars(acc)["open"])))
        return self

    def opened_under(self, d) -> list:
        return [p for p in self.paths if under(p, d)]


def never_called_names() -> list:
    return [n for n in dc.CONTRACT["binding"]["never_called"] if " " not in n]


def tripwire(monkeypatch, names=None) -> list:
    """Replace never-called functions by tripwires; returns the list of names hit."""
    hits: list = []
    for full in names or never_called_names():
        mod, _, name = full.partition(".")
        m = importlib.import_module(mod)
        if not hasattr(m, name):
            continue

        def boom(*a, _n=full, **k):
            hits.append(_n)
            raise AssertionError(f"never-called function called: {_n}")

        monkeypatch.setattr(m, name, boom)
    return hits


def status_of(exc) -> str:
    return getattr(exc, "status", type(exc).__name__)


# ---------------------------------------------------------------- fixtures


def tiny_artifacts(artifacts: Path, n_train: int = 48, n_dev: int = 24) -> dict:
    """WorldSpec, TransitionSpec, two EmissionSpecs, two ObservationSets (tiny world)."""
    artifacts.mkdir(parents=True, exist_ok=True)
    st = ArtifactStore(LocalFSBackend(artifacts))
    proc = hwsb_dry.build_tiny_process(st)
    plan = hwsb_config.dry_plan("dry_tiny", "B0197")
    plan = dataclasses.replace(plan, sizes={"train": n_train, "dev": n_dev})
    ids = hwsb_data.make_train_dev(st, proc, hwsb_config.DRY_MASTERS[0], plan)
    return {"store": st, "proc": proc, "ids": ids}


def os_payloads(artifacts: Path) -> list:
    return sorted((artifacts / "ObservationSet").glob("*/payload.npz"))


def expected_os_digests(artifacts: Path) -> set:
    """Independent canonical digests of every ObservationSet of an artifacts root."""
    import scores
    from topo_pilot.contracts import EmissionSpec, ObservationSet

    st = ArtifactStore(LocalFSBackend(artifacts))
    out: set = set()
    for p in os_payloads(artifacts):
        oid = p.parent.name
        obs = st.load(ObservationSet, oid, consumer="experiment")
        pid = [q for q in st.meta(oid).parent_ids if st.meta(q).artifact_type == "EmissionSpec"]
        spec = st.load(EmissionSpec, pid[0], consumer="experiment")
        out |= set(scores.history_digests(hwsb_data.canonical32(obs.tokens, spec.symbol_perm)))
    return out


def hist_table(split: str, n: int, seed: int, start: int, low: int = 5) -> dict:
    rng = np.random.default_rng(seed)
    canon = rng.integers(low, 36, size=(n, 32)).astype(np.uint8)
    ids = np.arange(start, start + n, dtype=np.int64)
    return k4b_data.history_table(canon, ids, split, 0)


def save_table(path, table) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.save_npz(path, **{k: v for k, v in table.items() if isinstance(v, np.ndarray)})
    return path


def stage_complete(store: Path, stage: str, rels) -> None:
    """Append one STAGE_COMPLETE event (the k4b_driver.complete_stage line format)."""
    files = {r: sha(store / r) for r in rels}
    line = {"event": "STAGE_COMPLETE", "files": files, "stage": stage, "utc": UTC}
    with (store / "STAGES.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(line, sort_keys=True) + "\n")


def fake_artifact(artifacts: Path, kind: str, hexid: str, names=("payload.npz",), meta=None):
    d = artifacts / kind / hexid
    write_json(d / "meta.json", {"artifact_id": hexid, "artifact_type": meta or kind})
    for n in names:
        junk(d / n)
    return d


def array_npz(path, **arrays) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    stage_records.save_npz(path, **(arrays or {"x": np.zeros((3, 2))}))
    return path


# --------------------------------------------- J11 obligation, track U's form

U_RULES = [
    {"kind": "chart", "regex": r"stages/OF/charts/CHART_\d+\.npz"},
    {"kind": "oracle-moment", "regex": r"stages/OF/ORACLE_[a-z]+\.npz"},
]
READER = {"ObservationSet": "hwsb_registry.registry_digests",
          "K4b history table": "k4b_history_table", "NON_HISTORY": None}


def u_entry(store: Path, rel: str, cls: str, basis) -> dict:
    p = store / rel
    ckpt = "/artifacts/Checkpoint/" in "/" + rel
    return {"relpath": rel, "sha256": None if ckpt else sha(p), "bytes": p.stat().st_size,
            "class": cls, "reader": READER[cls], "basis": basis}


def u_obligation(store: Path, entries, utc=UTC, rules=None, track="U") -> dict:
    return {"schema": "hws-registry-obligation-v1", "store": store.as_posix(), "track": track,
            "job": "0198-OF", "attempt": 1, "written_utc": utc,
            "written_by": "hwsu_records.write_obligation", "reservation_id": "RES-HWSU-OF-a1",
            "name_rules": copy.deepcopy(U_RULES if rules is None else rules), "dry_stores": [],
            "files": sorted(copy.deepcopy(list(entries)), key=lambda e: e["relpath"]),
            "rule": "fail closed"}


def build_u_store(store: Path) -> dict:
    """A store as track U would leave it after its oracle-only stage (J6, J10, J11)."""
    art = store / "artifacts"
    tiny_artifacts(art)
    fake_artifact(art, "Checkpoint", "c0ffee0000000001", ("payload.npz", "state.pt"))
    hist = hist_table("lgate", 40, 11, 7_000_000)
    save_table(store / "stages/OF/HIST_of_b0.npz", hist)
    array_npz(store / "stages/OF/charts/CHART_1.npz")
    array_npz(store / "stages/OF/ORACLE_cal.npz")
    array_npz(store / "registry/K-REG1_digests.npz", digests=np.array(["a" * 64], "<U64"))
    entries = []
    for p in sorted(store.rglob("*")):
        if p.suffix not in (".npz", ".npy", ".pt"):
            continue
        rel = p.relative_to(store).as_posix()
        parts = rel.split("/")
        if "artifacts" in parts:
            t = parts[parts.index("artifacts") + 1]
            cls = "ObservationSet" if t == "ObservationSet" else "NON_HISTORY"
            entries.append(u_entry(store, rel, cls, None if cls != "NON_HISTORY" else "artifact"))
        elif rel.startswith("registry/"):
            entries.append(u_entry(store, rel, "NON_HISTORY", "registry"))
        elif rel.endswith("HIST_of_b0.npz"):
            entries.append(u_entry(store, rel, "K4b history table", None))
        else:
            entries.append(u_entry(store, rel, "NON_HISTORY", "name_rule"))
    return {"entries": entries, "hist_digests": set(np.asarray(hist["digest"]).astype(str).tolist()),
            "os_digests": expected_os_digests(art)}


def put_obligation(store: Path, obl: dict, name="REGISTRY_OBLIGATION_OF.json") -> Path:
    return write_json(store / name, obl)
