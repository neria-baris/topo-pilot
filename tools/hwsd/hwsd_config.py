"""HWSD configuration: CONTRACT.json, constants, registry tables, plans, blindness guard (API.md §1).

Import puts the reused tool folders on sys.path, reads CONTRACT.json files only (hwsd's, and through
hwsc_config stage C's, stage B's, K4b's and C1''s) and computes constants. It never opens HANDOFF.json
or a store file.
"""

from __future__ import annotations  # noqa: I001

import copy
import dataclasses
import fnmatch
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (str(REPO / "tools" / "hwsc"), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
if sys.path[0] != str(HERE):
    sys.path.remove(str(HERE))
    sys.path.insert(0, str(HERE))

import hwsc_config  # noqa: E402
import hwsb_config  # noqa: E402
import k4b_config  # noqa: E402
import c1_means  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

CONTRACT_PATH = HERE / "CONTRACT.json"
PROTOCOL_PATH = HERE / "PROTOCOL_HWSD_v1.md"
API_PATH = HERE / "API.md"
TEST_PLAN_PATH = HERE / "TEST_PLAN.md"
ROOT = Path("X:/Downloads/projects/topo-pilot")
SCRATCH = Path("X:/Downloads/topo-scratch")
STORE = ROOT / "hwsd-store"
DRY_STORE = SCRATCH / "hwsd-dry"
HWSC_STORE = ROOT / "hwsc-store"
HWSU_STORE = ROOT / "hwsu-store"
MAILBOX = ROOT / "agent-handoff"
STUDY_LEDGER = MAILBOX / "HWSD_CPU_LEDGER.json"
HANDOFF_PATH = ROOT / "hwsb-store" / "HANDOFF.json"


def load_contract(path=CONTRACT_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


CONTRACT = load_contract()
_T = CONTRACT["thresholds"]
PROTOCOL_SHA256 = CONTRACT["protocol_sha256"]

SCOPE, DRY_SCOPE = "hwsd-v1", "hwsd-dry-v1"
KEY = "W12-q1-s1.75-p0.2"
PROCESS = ("cylinder", "overlap", "1.75")
TINY_PROCESS = ("cylinder", "overlap", "1.0")
MASTERS = tuple(int(m) for m in CONTRACT["masters"])
DRY_MASTERS = tuple(int(m) for m in CONTRACT["seeds"]["dry_masters"])
STEPS = (0, 50, 100, 200, 400, 700, 1000, 1500, 2000, 3000, 4000, 5000)
K_OF = {s: 1 + i for i, s in enumerate(STEPS)}
SEEDS = {k: int(v) for k, v in CONTRACT["seeds"]["k4b_seed_names"].items()}
STRONG_SEED = int(CONTRACT["seeds"]["strong_bound"])
DRY_SEEDS = {k: int(v) for k, v in CONTRACT["seeds"]["dry_seed_names"].items()}
DRY_STRONG_SEED = int(CONTRACT["seeds"]["dry_strong_bound"])
NEEDLES = tuple(CONTRACT["seeds"]["g0_needles"])
SPLITS = ("lgate", "cal", "val", "test")
SIZES = {"lgate": 4096, "cal": 3072, "val": 3072, "test": 3072}
N, PANEL, LGATE_N = 3072, 512, 4096
DRAWS, STRONG_DRAWS = 5000, 50000
RANKS = {k: int(v) for k, v in _T["ranks"].items()}
STRONG_RANKS = {"lo": 70, "hi": 49931}
M, ALPHA, LEARN = Fraction(1, 100), Fraction(1, 60), Fraction(4, 5)
CAP, FLOOR = Fraction(1, 10**4), Fraction(1, 10**9)
P_LO, P_HI = Fraction(1, 720), Fraction(719, 720)
F_PLANTED = Fraction(1, 10**9)
Z = NormalDist().inv_cdf(1 - 0.05 / 4)
Z_S = NormalDist().inv_cdf(1 - 1 / 720)
DISCLOSURE = CONTRACT["disclosure"]
CHECKPOINTS = {(int(r["master"]), int(r["step"])): r for r in CONTRACT["checkpoints"]["rows"]}
TRAIN_WHITELIST = ("status", "run_key", "checkpoint_ids", "checksums", "process_ids")
RESERVATION_PREFIX = "RES-HWSD-W2-a"


def _import_checks() -> None:
    def bad(msg):
        raise C1GateFailure("FAIL_TECHNICAL/BINDING", msg)

    for name, mine, theirs in (("M", M, k4b_config.MARGIN), ("ALPHA", ALPHA, k4b_config.ALPHA),
                               ("CAP", CAP, k4b_config.CAP), ("FLOOR", FLOOR, k4b_config.FLOOR),
                               ("DRAWS", DRAWS, k4b_config.DRAWS), ("PANEL", PANEL, k4b_config.PANEL),
                               ("N", N, k4b_config.BLOCK)):
        if mine != theirs:
            bad(f"{name} {mine!r} != K4b {theirs!r}")
    keys = ("alpha", "one_minus_alpha", "central_lo", "central_hi", "b4_lower")
    if {k: RANKS[k] for k in keys} != k4b_config.RANKS:
        bad("RANKS differ from K4b")
    if c1_means.rank_for(P_LO, STRONG_DRAWS) != 70 or c1_means.rank_for(P_HI, STRONG_DRAWS) != 49931:
        bad("strong ranks")
    if Z != hwsb_config.Z_B23:
        bad("Z != hwsb_config.Z_B23")
    if len(CHECKPOINTS) != 36 or set(CHECKPOINTS) != {(j, s) for j in MASTERS for s in STEPS}:
        bad("checkpoint rows are not MASTERS x STEPS")
    if CONTRACT["disclosure"] != CONTRACT["k4b_contract_view"]["authority"]["c1prime_disclosure"]:
        bad("disclosure differs from the K4b view")


_import_checks()


# ------------------------------------------------------------------ effective registry tables
def _sha_file(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inherited_sha_ok() -> bool:
    want = CONTRACT["registry"]["scratch_inventory"]["inherit"]["sha256"]
    return _sha_file(REPO / "tools" / "hwsc" / "CONTRACT.json") == want


def _need_inherit() -> None:
    if not inherited_sha_ok():
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "tools/hwsc/CONTRACT.json sha256 differs")


def scratch_table() -> dict:
    _need_inherit()
    t = copy.deepcopy(hwsc_config.CONTRACT["registry"]["scratch_inventory"])
    s = CONTRACT["registry"]["scratch_inventory"]
    t.update(copy.deepcopy(s["rows"]))
    t.update(copy.deepcopy(s["pattern_rows"]))
    return t


def root_table() -> dict:
    _need_inherit()
    t = copy.deepcopy(hwsc_config.CONTRACT["registry"]["inventory"])
    t.update(copy.deepcopy(CONTRACT["registry"]["inventory"]["rows"]))
    return t


# --------------------------------------------------------------------------------- plans
def dry_plan(kind, case):
    if kind not in ("dry_tiny", "dry_e4"):
        raise ValueError(f"unknown dry plan kind {kind!r}")
    base = hwsb_config.dry_plan(kind, case)
    if kind == "dry_tiny":
        cfg = dataclasses.replace(base.train_cfg, checkpoint_steps=[0, 50, 100, 200])
        return dataclasses.replace(base, masters=DRY_MASTERS, sizes={"train": 4096, "dev": 512},
                                   train_cfg=cfg)
    cfg = dataclasses.replace(base.train_cfg, steps=20, checkpoint_steps=[0, 20])
    return dataclasses.replace(base, masters=DRY_MASTERS[:1], sizes={"train": 2048, "dev": 256},
                               train_cfg=cfg)


# ----------------------------------------------------------------------- blindness guard
def _posix(path) -> str:
    return Path(path).resolve().as_posix().lower().rstrip("/")


def _under(p: str, d: str) -> bool:
    return p == d or p.startswith(d + "/")


def blinded(path, root=ROOT, scratch=SCRATCH) -> bool:
    if hwsc_config.blinded(path, root):
        return True
    p, r, sc = _posix(path), _posix(root), _posix(scratch)
    if _under(p, f"{r}/hwsc-store/stages/train") or _under(p, f"{r}/hwsc-store/logs"):
        return True
    if p == f"{r}/hwsc-store/stages/e1/l1.json":
        return True
    if p.startswith(sc + "/"):
        first = p[len(sc) + 1:].split("/")[0]
        if fnmatch.fnmatchcase(first, "hwsc-job-*"):
            return True
    if p in {f"{r}/agent-handoff/jobs/{n}/review.md" for n in ("0187", "0188", "0189")}:
        return True
    pl = f"{r}/agent-handoff/planning"
    if p.startswith(pl + "/"):
        for comp in p[len(pl) + 1:].split("/"):
            if "coord-hws-use-20261101" in comp or comp.startswith("hwsu-"):
                return True
    return False


def search_pruned(path, root=ROOT, scratch=SCRATCH) -> bool:
    if blinded(path, root, scratch):
        return True
    p, store = _posix(path), f"{_posix(root)}/hwsu-store"
    if not _under(p, store):
        return False
    if p == store or p == store + "/reservations":
        return False
    rel = p[len(store) + 1:].split("/")
    name = rel[-1]
    if len(rel) == 1 and (fnmatch.fnmatchcase(name, "registry_obligation*.json")
                          or fnmatch.fnmatchcase(name, "reservation*.json")):
        return False
    if len(rel) == 2 and rel[0] == "reservations" and name.endswith(".json"):
        return False
    return True


def public_summary(path) -> bool:
    return hwsc_config.public_summary(path)


def guard(path, root=ROOT) -> Path:
    if blinded(path, root) or public_summary(path):
        raise C1GateFailure("FAIL_TECHNICAL/BLINDNESS", str(path))
    return Path(path)


def read_bytes(path, root=ROOT) -> bytes:
    return guard(path, root).read_bytes()


def read_json(path, root=ROOT):
    return json.loads(guard(path, root).read_text(encoding="utf-8"))


# ------------------------------------------------------------------ the two exempt readers
def read_train_record(master, store=HWSC_STORE) -> tuple:
    path = Path(store) / "stages" / "TRAIN" / str(int(master)) / "TRAIN_RECORD.json"
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    obj = json.loads(data.decode("utf-8"))
    del data
    if not isinstance(obj, dict):
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"TRAIN record {master}: not an object")
    missing = [k for k in TRAIN_WHITELIST if k not in obj]
    if missing:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"TRAIN record {master}: {missing}")
    rec = {k: obj[k] for k in TRAIN_WHITELIST}
    del obj
    return sha, rec


def read_obs_inventory(store=HWSC_STORE, expected_sha256=None) -> dict:
    want = (CONTRACT["identity"]["rows"]["obs_inventory"]["sha256"]
            if expected_sha256 is None else expected_sha256)
    data = (Path(store) / "stages" / "TRAIN" / "OBS_INVENTORY.json").read_bytes()
    if hashlib.sha256(data).hexdigest() != want:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "OBS_INVENTORY.json sha256 differs")
    obj = json.loads(data.decode("utf-8"))
    ok = isinstance(obj, dict) and all(
        isinstance(k, str) and isinstance(v, str) and len(v) == 64
        and all(c in "0123456789abcdef" for c in v) for k, v in obj.items())
    if not ok:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "OBS_INVENTORY.json is not a flat hex map")
    return obj
