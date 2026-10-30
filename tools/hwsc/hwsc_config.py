"""HWSC configuration: CONTRACT.json, constants, plans, HANDOFF loader, blindness guard (API.md §1).

Import puts the reused tool folders on sys.path (insert if absent), reads CONTRACT.json files only
(stage C's, and through hwsb_config/k4b_config stage B's, K4b's and C1''s) and computes constants.
It never opens HANDOFF.json or any store file.
"""

from __future__ import annotations  # noqa: I001

import dataclasses
import fnmatch
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
_ORDER = ("hwsc", "hwsb", "hws", "k4b", "c1prime", "c1prime_registry", "x4_circle_history",
          "x4_oracle_profile", "c2_nd", "c2_readout", "x6_stage1")
for _sub in reversed(_ORDER):
    _p = str(REPO / "tools" / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import hwsb_config  # noqa: E402
import k4b_config  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

CONTRACT_PATH = HERE / "CONTRACT.json"
PROTOCOL_PATH = HERE / "PROTOCOL_HWSC_v1.md"
API_PATH = HERE / "API.md"
TEST_PLAN_PATH = HERE / "TEST_PLAN.md"
ROOT = Path("X:/Downloads/projects/topo-pilot")
STORE = ROOT / "hwsc-store"
SCRATCH = Path("X:/Downloads/topo-scratch")
DRY_STORE = SCRATCH / "hwsc-dry"
MAILBOX = ROOT / "agent-handoff"
STUDY_LEDGER = MAILBOX / "HWSC_CPU_LEDGER.json"
HANDOFF_PATH = ROOT / "hwsb-store" / "HANDOFF.json"
HWS_STORE = ROOT / "hws-store"
HWSB_STORE = ROOT / "hwsb-store"
SELECTION_PATH = ROOT / "hws-store" / "SELECTION.json"


def load_contract(path=CONTRACT_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


CONTRACT = load_contract()
_W, _T, _CPU = CONTRACT["world"], CONTRACT["thresholds"], CONTRACT["cpu"]

SCOPE = "hwsc-v1"
KEY = _W["key"]
PROCESS = tuple(_W["process_code_args"])
MASTERS = tuple(int(m) for m in CONTRACT["masters"])
DRY_MASTERS = tuple(int(m) for m in CONTRACT["dry_masters"])
SEEDS = {k: int(v) for k, v in CONTRACT["seeds"]["k4b_seed_names"].items()}
P1C_SEEDS = tuple(int(s) for s in CONTRACT["seeds"]["p1c_seeds"])
DRY_SEEDS = {"val_sd": 629921, "val_b4": 629922, "endpoint": 629923, "fresh_b4": 629924,
             "val_projection": 629925}
NEEDLES = tuple(CONTRACT["seeds"]["g0_needles"])
SIZES = {k: int(CONTRACT["sizes"][k]) for k in ("train", "dev", "lgate", "cal", "val")}
BLOCK, LGATE_N, PANEL = 3072, 4096, 512
LADDER = tuple(int(n) for n in _T["ladder"])
DRAWS = int(_T["draws"])
KS = (1, 2, 4, 32)
SITE, INDEX, BOS, D_MODEL = "resid_post_3", 32, 36, 128
GATE_STEP, INIT_STEP = 5000, 0
M = Fraction(_T["margin_M"])
ALPHA = Fraction(_T["alpha"])
LEARN = Fraction(_T["learning_captured"])
CAP = Fraction(_T["cap"])
FLOOR = Fraction(_T["floor"])
RANKS = {k: int(v) for k, v in _T["ranks"].items()}
SIGMA = Fraction(_W["sigma"])
NEIGHBOUR = Fraction(_W["neighbour"])
HOLD_S = float(_CPU["per_model_hold_s"])
HOLD_FROM = int(_CPU["hold_from_step"])
STEPS = 5000
DISCLOSURE = CONTRACT["disclosure"]
RESERVATION_FILE, RESERVATION_ID = "RESERVATION_W2.json", "RES-HWSC-W2"
PROTOCOL_SHA256 = CONTRACT["protocol_sha256"]

_CHECKS = (
    (M, k4b_config.MARGIN), (ALPHA, k4b_config.ALPHA), (CAP, k4b_config.CAP),
    (FLOOR, k4b_config.FLOOR), (RANKS, k4b_config.RANKS), (LADDER, k4b_config.LADDER),
    (BLOCK, k4b_config.BLOCK), (PANEL, k4b_config.PANEL), (DRAWS, k4b_config.DRAWS),
)
for _a, _b in _CHECKS:
    if _a != _b:
        raise C1GateFailure("FAIL_TECHNICAL/BINDING", f"constant {_a!r} != K4b {_b!r}")
if CONTRACT["disclosure"] != CONTRACT["k4b_contract_view"]["authority"]["c1prime_disclosure"]:
    raise C1GateFailure("FAIL_TECHNICAL/BINDING", "disclosure differs from the K4b view")

# ------------------------------------------------------------------------------- HANDOFF (§1.2)
_FRACTION_KEYS = ("Z_bound", "F_plan", "registry_value")
_INT_KEYS = ("N_C", "k_C", "model_count")


def _forbidden_anywhere(obj, forbidden) -> list:
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in forbidden:
                out.append(k)
            out += _forbidden_anywhere(v, forbidden)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            out += _forbidden_anywhere(v, forbidden)
    return out


def load_handoff(path=HANDOFF_PATH, expected_sha256=None) -> dict:
    h = CONTRACT["handoff"]
    want = h["sha256"] if expected_sha256 is None else expected_sha256
    data = read_bytes(path)
    if hashlib.sha256(data).hexdigest() != want:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "HANDOFF.json sha256 differs")
    try:
        obj = json.loads(data.decode("utf-8"))
    except ValueError as exc:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"HANDOFF.json: {exc!r}") from exc
    if not isinstance(obj, dict) or set(obj) != set(h["keys"]):
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "HANDOFF.json key set differs")
    bad = _forbidden_anywhere(obj, set(h["forbidden_keys"]))
    if bad:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"HANDOFF.json forbidden keys {bad}")
    out = dict(obj)
    for k in _FRACTION_KEYS:
        out[k] = Fraction(str(obj[k]))
    for k in _INT_KEYS:
        out[k] = int(obj[k])
    out["p_D2a"] = float(obj["p_D2a"])
    out["stage_c_exclusions"] = tuple(str(x) for x in obj["stage_c_exclusions"])
    return out


# --------------------------------------------------------------------------- plans (§1.3)
HWSC_PLAN = hwsb_config.Plan("real", MASTERS, hwsb_config.MODEL_CFG, hwsb_config.TRAIN_CFG,
                             {"train": SIZES["train"], "dev": SIZES["dev"]}, SITE, KEY, PROCESS,
                             GATE_STEP, INIT_STEP)
_DRY_SIZES = {"dry_tiny": {"train": 4096, "dev": 512}, "dry_e4": {"train": 2048, "dev": 256}}


def dry_plan(kind, case):
    if kind not in _DRY_SIZES:
        raise ValueError(f"unknown dry plan kind {kind!r}")
    base = hwsb_config.dry_plan(kind, case)
    return dataclasses.replace(base, masters=DRY_MASTERS, sizes=dict(_DRY_SIZES[kind]))


def run_key(plan, master) -> tuple:
    if plan.dry:
        return (SCOPE, "DRY", plan.key, int(master))
    return (SCOPE, KEY, int(master))


# --------------------------------------------------------------- blindness guard (§1.4, §18)
BLINDED_FILES = ("hwsb-store/report.json", "hwsb-store/gates.jsonl",
                 "agent-handoff/jobs/0175/review.md")
BLINDED_DIRS = ("hwsb-store/stages/eval",)
BLINDED_GLOBS = (("hwsb-store", "chart_constructions_*.json"),)


def _posix(path) -> str:
    return Path(path).resolve().as_posix().lower().rstrip("/")


def blinded(path, root=ROOT) -> bool:
    p, r = _posix(path), _posix(root)
    if p in {f"{r}/{f}" for f in BLINDED_FILES}:
        return True
    for d in BLINDED_DIRS:
        base = f"{r}/{d}"
        if p == base or p.startswith(base + "/"):
            return True
    for parent, pattern in BLINDED_GLOBS:
        q = Path(p)
        if q.parent.as_posix() == f"{r}/{parent}" and fnmatch.fnmatchcase(q.name, pattern):
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


def read_bytes(path, root=ROOT) -> bytes:
    return guard(path, root).read_bytes()


def read_json(path, root=ROOT):
    return json.loads(guard(path, root).read_text(encoding="utf-8"))
