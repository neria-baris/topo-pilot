"""HWSG configuration: CONTRACT.json, constants, worlds, plans, paths, blindness guard (API.md §1).

Import puts the reused tool folders on sys.path (insert if absent), reads CONTRACT.json files only
and computes constants. It opens no store file.
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

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
_ORDER = ("hwsg", "hwsc", "hwsb", "hws", "k4b", "c1prime", "c1prime_registry",
          "x4_circle_history", "x4_oracle_profile", "c2_nd", "c2_readout", "x6_stage1")
for _sub in reversed(_ORDER):
    _p = str(REPO / "tools" / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import hwsb_config  # noqa: E402
import hwsc_config  # noqa: E402
import k4b_config  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

from topo_pilot.process import EmissionConfig, TransitionConfig  # noqa: E402

CONTRACT_PATH = HERE / "CONTRACT.json"
PROTOCOL_PATH = HERE / "PROTOCOL_HWSG_v1.md"
API_PATH = HERE / "API.md"
TEST_PLAN_PATH = HERE / "TEST_PLAN.md"
ROOT = Path("X:/Downloads/projects/topo-pilot")
STORE = ROOT / "hwsg-store"
SCRATCH = Path("X:/Downloads/topo-scratch")
DRY_STORE = SCRATCH / "hwsg-dry"
MAILBOX = ROOT / "agent-handoff"
STUDY_LEDGER = MAILBOX / "HWSG_CPU_LEDGER.json"
HWS_STORE = ROOT / "hws-store"
HWSB_STORE = ROOT / "hwsb-store"
HWSC_STORE = ROOT / "hwsc-store"
HWSU_STORE = ROOT / "hwsu-store"
HWSD_STORE = ROOT / "hwsd-store"
REPORT_PATH = HWS_STORE / "stages/FINAL/REPORT.json"
S3_DIR = HWS_STORE / "stages/S3/worlds"
BAD = "FAIL_TECHNICAL/BINDING"


def load_contract(path=CONTRACT_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


CONTRACT = load_contract()
_T, _S = CONTRACT["thresholds"], CONTRACT["sizes"]
PROTOCOL_SHA = CONTRACT["protocol_sha256"]
PROTOCOL_SHA256 = PROTOCOL_SHA


def protocol_ok() -> bool:
    return hashlib.sha256(PROTOCOL_PATH.read_bytes()).hexdigest() == PROTOCOL_SHA


SCOPE = CONTRACT["scope"]
W_STAR = CONTRACT["w_star"]["key"]
TAGS = tuple(CONTRACT["worlds_order"])
CROSS_SEED = int(CONTRACT["seeds"]["cross"])
DRY_MASTERS = {t: tuple(int(m) for m in v)
               for t, v in CONTRACT["seeds"]["dry_masters_by_world"].items()}
DRY_SEEDS = {k: int(v) for k, v in CONTRACT["seeds"]["dry_seeds"].items()}
NEEDLES = tuple(CONTRACT["seeds"]["kg0_needles"])
SIZES = {"train": int(_S["train"]), "dev": int(_S["dev"]), "lgate": int(_S["lgate"]),
         "cal": int(_S["cal"]), "val": int(_S["val"])}
BLOCK, LGATE_N, PANEL = 3072, 4096, 512
LADDER = tuple(int(n) for n in _S["ladder"])
DRAWS = int(_T["draws"])
KS = tuple(int(k) for k in _S["ks"])
N_C, MODEL_COUNT = int(_S["N_C"]), int(_S["model_count"])
M = Fraction(_T["margin_M"])
ALPHA = Fraction(_T["alpha"])
LEARN = Fraction(_T["learning_captured"])
CAP = Fraction(_T["cap"])
FLOOR = Fraction(_T["floor"])
F_PLAN_MAX = Fraction(_T["F_plan_max"])
CAPTURE_FLOOR = Fraction(_T["capture_floor"])
RISK_MAX = Fraction(_T["registry_risk_max"])
RANKS = {k: int(v) for k, v in _T["ranks"].items()}
O3_ROWS = int(_T["registry_risk_rows_O3"])
HOLD_S = float(CONTRACT["cpu"]["per_model_hold_s"])
HOLD_FROM = int(CONTRACT["cpu"]["hold_from_step"])
STEPS = 5000
DISCLOSURE = CONTRACT["disclosure"]

for _a, _b in ((M, k4b_config.MARGIN), (ALPHA, k4b_config.ALPHA), (CAP, k4b_config.CAP),
               (FLOOR, k4b_config.FLOOR), (RANKS, k4b_config.RANKS)):
    if _a != _b:
        raise C1GateFailure(BAD, f"constant {_a!r} != K4b {_b!r}")


def exclusions(handoff_path=None) -> tuple:
    path = Path(HWSB_STORE / "HANDOFF.json" if handoff_path is None else handoff_path)
    data = guard(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != CONTRACT["w_star"]["handoff_sha256"]:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "stage-B HANDOFF.json sha256 differs")
    ids = json.loads(data.decode("utf-8"))["stage_c_exclusions"]
    return tuple(str(x) for x in ids) + tuple(CONTRACT["exclusions"]["stage_c_ids"])


# ---------------------------------------------------------------------------------- worlds (§1.2)
@dataclasses.dataclass(frozen=True)
class WorldDef:
    tag: str
    key: str
    sigma: Fraction
    p: Fraction
    neighbour: Fraction
    sigma_str: str
    p_str: str
    sigma_float: float
    p_float: float
    masters: tuple
    seeds: dict
    p1_seeds: tuple
    process: tuple
    world_cfg: object
    transition_cfg: object
    emission_cfg: object
    stage_a: dict
    reservation_id: str


def _make(tag, d) -> WorldDef:
    sigma, p, nb = Fraction(d["sigma"]), Fraction(d["p"]), Fraction(d["neighbour"])
    if (1 - p) / 4 != nb:
        raise C1GateFailure(BAD, f"neighbour of {tag} differs from (1-p)/4")
    key = d["key"]
    return WorldDef(
        tag=tag, key=key, sigma=sigma, p=p, neighbour=nb, sigma_str=d["sigma_str"],
        p_str=d["p_str"], sigma_float=float(d["sigma_float"]), p_float=float(d["p_float"]),
        masters=tuple(int(m) for m in d["masters"]),
        seeds={k: int(v) for k, v in d["seeds"].items()},
        p1_seeds=tuple(int(s) for s in d["p1_seeds"]),
        process=("cylinder", "overlap", d["sigma_str"], d["p_str"], key),
        world_cfg=hwsb_config.WORLD_CFG,
        transition_cfg=TransitionConfig(p_stay=float(d["p_float"])),
        emission_cfg=EmissionConfig("overlap", 36, float(d["sigma_float"]), "grid"),
        stage_a=dict(d["stage_a"]), reservation_id=d["reservation_id"])


WORLDS = {t: _make(t, CONTRACT["worlds"][t]) for t in TAGS}


def world(w) -> WorldDef:
    if isinstance(w, WorldDef):
        return w
    if w in WORLDS:
        return WORLDS[w]
    for d in WORLDS.values():
        if w == d.key:
            return d
    raise ValueError(f"unknown world {w!r}")


def world_dir(store, w) -> Path:
    return Path(store) / "worlds" / world(w).key


def plan(w) -> hwsb_config.Plan:
    d = world(w)
    return hwsb_config.Plan("real", d.masters, hwsb_config.MODEL_CFG, hwsb_config.TRAIN_CFG,
                            {"train": SIZES["train"], "dev": SIZES["dev"]}, "resid_post_3",
                            d.key, d.process, 5000, 0)


def dry_plan(w, case, kind="dry_tiny") -> hwsb_config.Plan:
    d = world(w)
    base = hwsb_config.dry_plan(kind, case)
    sizes = dict(hwsc_config._DRY_SIZES[kind])
    return dataclasses.replace(base, masters=DRY_MASTERS[d.tag], key=f"DRY-{d.tag}",
                               process=("cylinder", "overlap", f"dry-{d.tag}", case),
                               sizes=sizes)


def run_key(w, master, case=None) -> tuple:
    d = world(w)
    if case is not None:
        return (SCOPE, "DRY", case, d.tag, int(master))
    return (SCOPE, d.key, int(master))


def k4b_view() -> dict:
    v = copy.deepcopy(hwsc_config.CONTRACT["k4b_contract_view"])
    v["protocol_sha256"] = PROTOCOL_SHA
    v["authority"]["c1prime_disclosure"] = DISCLOSURE
    return v


# --------------------------------------------------------------------- blindness guard (§1.3)
def _posix(path) -> str:
    return Path(path).resolve().as_posix().lower().rstrip("/")


def _rel(path, root):
    p, r = _posix(path), _posix(root)
    if p == r:
        return ""
    return p[len(r) + 1:] if p.startswith(r + "/") else None


def blinded(path, root=ROOT) -> bool:
    rel = _rel(path, root)
    if rel is None:
        return False
    b = CONTRACT["blindness"]
    for a in b["allow"]:
        a = a.lower()
        if rel == a or fnmatch.fnmatchcase(rel, a):
            return False
    if rel in {f.lower() for f in b["files"]}:
        return True
    for d in b["dirs"]:
        d = d.lower()
        if rel == d or rel.startswith(d + "/"):
            return True
    head, _, name = rel.rpartition("/")
    for parent, pat in b["globs"]:
        if head == parent.lower() and fnmatch.fnmatchcase(name, pat.lower()):
            return True
    parts = rel.split("/")
    jr = b["job_range"]
    if len(parts) >= 3 and "/".join(parts[:2]) == jr["prefix"].strip("/").lower() \
            and parts[2].isdigit() and int(jr["from"]) <= int(parts[2]) <= int(jr["to"]):
        return True
    return False


def public_summary(path) -> bool:
    parts = [c.lower() for c in Path(str(path).replace("\\", "/")).parts]
    if any(c.startswith("00_read_me_first") for c in parts):
        return True
    return any(a == "docs" and b == "research_summary" for a, b in zip(parts, parts[1:]))


def guard(path, root=ROOT) -> Path:
    if blinded(path, root) or public_summary(path):
        raise C1GateFailure("FAIL_TECHNICAL/BLINDNESS", str(path))
    return Path(path)


def read_json(path, root=ROOT):
    return json.loads(guard(path, root).read_text(encoding="utf-8"))


def read_bytes(path, root=ROOT) -> bytes:
    return guard(path, root).read_bytes()


def prune(dirpath, dirnames, root=ROOT) -> None:
    here = Path(dirpath)
    dirnames[:] = sorted(d for d in dirnames
                         if not (blinded(here / d, root) or public_summary(here / d)))
