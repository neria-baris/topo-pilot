"""HWSB configuration: CONTRACT.json, constants, plans (API.md §1; protocol §2, §4, §8).

Import puts the reused tool folders on sys.path (insert if absent), reads CONTRACT.json and
computes small constants only. It performs no other I/O.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist
from typing import Mapping

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _sub in reversed(
    ("hwsb", "hws", "k4b", "c1prime", "c1prime_registry", "x4_circle_history", "x4_oracle_profile")
):
    _p = str(REPO / "tools" / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import c1_means  # noqa: E402

from topo_pilot.learner.config import ModelConfig, TrainConfig  # noqa: E402
from topo_pilot.process import EmissionConfig, TransitionConfig  # noqa: E402
from topo_pilot.world import WorldConfig  # noqa: E402

CONTRACT_PATH = HERE / "CONTRACT.json"
PROTOCOL_PATH = HERE / "PROTOCOL_HWSB_v1.md"
PROOF_PATH = HERE / "ENCLOSURE_PROOF.md"
ROOT = Path("X:/Downloads/projects/topo-pilot")
STORE = ROOT / "hwsb-store"
DRY_STORE = Path("X:/Downloads/topo-scratch/hwsb-dry")
SCRATCH = Path("X:/Downloads/topo-scratch")
HWS_STORE = ROOT / "hws-store"
STUDY_LEDGER = ROOT / "agent-handoff" / "HWSB_CPU_LEDGER.json"


def load_contract(path=CONTRACT_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


CONTRACT = load_contract()


class HwsbStop(RuntimeError):
    """A technical or resource stop carrying a full status string (API.md §0)."""

    def __init__(self, status: str, reason: str = ""):
        super().__init__(f"{status}: {reason}")
        self.status = str(status)
        self.reason = str(reason)


SCOPE = "hwsb-v1"
KEY = CONTRACT["world"]["key"]
PROCESS = tuple(CONTRACT["world"]["process_code_args"])
MASTERS = tuple(int(m) for m in CONTRACT["masters"])
DRY_MASTERS = tuple(int(m) for m in CONTRACT["dry_masters"])
SEEDS = {k: int(CONTRACT["seeds"][k]) for k in ("sd_upper", "projection", "capture_ci")}
NEEDLES = tuple(CONTRACT["seeds"]["g0_needles"])
SIGMA = Fraction(CONTRACT["world"]["sigma"])
NEIGHBOUR = Fraction(CONTRACT["world"]["neighbour"])

WORLD_CFG = WorldConfig("cylinder", (12, 12), "flat")
TRANS_CFG = TransitionConfig(p_stay=0.2)
EMIS_CFG = EmissionConfig("overlap", 36, 1.75, "grid")
W0_EMIS_CFG = EmissionConfig("overlap", 36, 1.25, "grid")


def _train_cfg(d) -> TrainConfig:
    d = dict(d)
    d["checkpoint_steps"] = tuple(int(s) for s in d["checkpoint_steps"])
    return TrainConfig(**d)


MODEL_CFG = ModelConfig(**CONTRACT["recipe"]["model_config"])
TRAIN_CFG = _train_cfg(CONTRACT["recipe"]["train_config"])

_S = CONTRACT["sizes"]
SIZES = {k: int(_S[k]) for k in ("train", "dev", "LGATE", "CAL", "VAL")}
PANEL = int(_S["panel"])
_T = CONTRACT["thresholds"]
LADDER = tuple(int(n) for n in _T["ladder"])
DRAWS = int(_T["draws"])
KS = (1, 2, 4, 32)
SITE, INDEX, BOS = "resid_post_3", 32, 36
GATE_STEP, INIT_STEP = 5000, 0
M = Fraction(_T["margin_M"])
ALPHA_C = Fraction(_T["alpha_stage_c"])
POWER = Fraction(_T["power"])
ALPHA_B23 = Fraction(_T["B2_B3_alpha"])
LEARN = Fraction(_T["learning_captured"])
MDE_MAX = Fraction(_T["mde_max"])
Z_C = NormalDist().inv_cdf(1.0 - float(ALPHA_C))
Z_P = NormalDist().inv_cdf(0.8)
Z_SUM = Z_C + Z_P
Z_B23 = NormalDist().inv_cdf(float(1 - ALPHA_B23))
RANKS = {"sd_upper": 4917, "proj_alpha": 84, "ci_lo": 125, "ci_hi": 4875}
for _name, _p in (
    ("sd_upper", 1 - ALPHA_C),
    ("proj_alpha", ALPHA_C),
    ("ci_lo", 0.025),
    ("ci_hi", 0.975),
):
    if c1_means.rank_for(_p, DRAWS) != RANKS[_name]:
        raise HwsbStop("FAIL_TECHNICAL/NUMERICAL", f"rank {_name} != {RANKS[_name]}")
C_MIN_FALLBACK_N = int(_T["c_min_fallback_N"])
Z_STANDIN = Fraction(_T["Z_bound_standin"])
REGISTRY_CAP = Fraction(_T["registry_cap"])
MIN_SUCCESSES = int(_T["min_successes"])
HIST_NAMES = tuple(CONTRACT["hist_file"]["names"])
CPU = CONTRACT["cpu"]
ADDENDUM_32_SHA = CONTRACT["authority"]["owner_addendum_32"]["sha256"]


@dataclass(frozen=True)
class Plan:
    """One code path for the real run and the dry run (API.md §1.2, choice 2)."""

    kind: str
    masters: tuple
    model_cfg: ModelConfig
    train_cfg: TrainConfig
    sizes: Mapping[str, int] = field(default_factory=dict)
    site: str = SITE
    key: str = KEY
    process: tuple = PROCESS
    gate_step: int = GATE_STEP
    init_step: int = INIT_STEP

    @property
    def dry(self) -> bool:
        return self.kind != "real"


REAL_PLAN = Plan("real", MASTERS, MODEL_CFG, TRAIN_CFG, SIZES, SITE, KEY, PROCESS, 5000, 0)


def dry_plan(kind, case) -> Plan:
    d = CONTRACT["dry_run"]
    if kind == "dry_tiny":
        return Plan(
            "dry_tiny",
            DRY_MASTERS,
            ModelConfig(**d["tiny_model"]),
            _train_cfg(d["tiny_train"]),
            {k: int(v) for k, v in d["tiny_sizes"].items()},
            d["tiny_site"],
            str(case),
            ("cylinder", "overlap", "1.0"),
            200,
            0,
        )
    if kind == "dry_e4":
        t = dict(CONTRACT["recipe"]["train_config"])
        t.update(
            steps=int(d["drb2_train"]["steps"]),
            checkpoint_steps=list(d["drb2_train"]["checkpoint_steps"]),
        )
        sizes = {
            "train": int(d["drb2_train"]["rows"]),
            "dev": int(d["drb2_train"]["dev_rows"]),
            "LGATE": 512,
            "CAL": 512,
            "VAL": 512,
        }
        return Plan(
            "dry_e4",
            DRY_MASTERS,
            MODEL_CFG,
            _train_cfg(t),
            sizes,
            SITE,
            str(case),
            PROCESS,
            int(d["drb2_train"]["steps"]),
            0,
        )
    raise ValueError(f"unknown dry plan kind {kind!r}")


def run_key(plan, master) -> tuple:
    if plan.dry:
        return (SCOPE, "DRY", plan.key, int(master))
    return (SCOPE, KEY, int(master))
