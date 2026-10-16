"""K4b configuration: CONTRACT.json loading, constants, chart-cfg equality with C1' (API.md §1).

Import puts the reused tool directories on sys.path (insert-if-absent) and imports c1_config,
which reads C1''s CONTRACT.json. Import reads only CONTRACT.json files (protocol §11.3).
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _sub in (
    "tools/k4b",
    "tools/c1prime",
    "tools/c1prime_registry",
    "tools/x4_circle_history",
    "tools/x4_oracle_profile",
):
    _p = str(REPO / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import c1_bounds  # noqa: E402
import c1_config  # noqa: E402
import c1_means  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

CONTRACT_PATH = HERE / "CONTRACT.json"
PROTOCOL_PATH = HERE / "PROTOCOL_K4B_v1.md"
ROOT = Path("X:/Downloads/projects/topo-pilot")
STORE = ROOT / "k4b-store"

MODELS = (1729, 2718, 3141)
SITE, INDEX, BOS, D_MODEL = "resid_post_3", 32, 36, 128
SCOPE = "k4b-sf-v1"
PROCESS = ("cylinder", "overlap", "1.25")
BLOCK, PANEL = 3072, 512
LADDER = (3072, 6144, 12288)
KS = (1, 2, 4, 32)
DRAWS = 5000
SEEDS = {
    "val_sd": 610101,
    "val_b4": 610102,
    "endpoint": 610103,
    "fresh_b4": 610104,
    "val_projection": 610105,
}
RANKS = {
    "alpha": 84,
    "one_minus_alpha": 4917,
    "b4_lower": 250,
    "central_lo": 125,
    "central_hi": 4875,
}
MARGIN = Fraction(1, 100)
CAP = Fraction(1, 10**4)
FLOOR = c1_bounds.FLOOR
ALPHA = c1_means.P_THIRD
P2_MAX_ABS = 4

_RANK_P = {
    "alpha": ALPHA,
    "one_minus_alpha": 1 - ALPHA,
    "b4_lower": 0.05,
    "central_lo": 0.025,
    "central_hi": 0.975,
}
for _name, _p in _RANK_P.items():
    if c1_means.rank_for(_p, DRAWS) != RANKS[_name]:
        raise C1GateFailure("FAIL_TECHNICAL/NUMERICAL", f"rank {_name} != {RANKS[_name]}")


def load_contract(path=CONTRACT_PATH) -> dict:
    """CONTRACT.json; chart.lift_cpu_cap_s and resources.cpu_cap_s null -> +inf."""
    return c1_config.load_contract(path)


CONTRACT = load_contract()


def chart_cfg(contract=None) -> dict:
    """The kernel cfg (12 CHART_KERNEL_KEYS, lift cap +inf, operation wall 600 s)."""
    return c1_config.chart_cfg(CONTRACT if contract is None else contract)


def check_chart_equality(k4b=None, c1=None) -> dict:
    """C2 (§4.2): the K4b chart cfg, giant and val_support equal C1''s, key for key."""
    k = CONTRACT if k4b is None else k4b
    c = c1_config.CONTRACT if c1 is None else c1
    a, b = c1_config.chart_cfg(k), c1_config.chart_cfg(c)
    diff = sorted(set(a) ^ set(b)) + sorted(key for key in set(a) & set(b) if a[key] != b[key])
    giant = k["chart"].get("giant") == c["chart"].get("giant")
    support = k["chart"].get("val_support") == c["chart"].get("val_support")
    return {"equal": not diff, "cfg_diff": diff, "giant_equal": giant, "val_support_equal": support}


def status_of(full: str) -> tuple:
    return c1_config.status_of(full)


def require_int_keys(d, what) -> dict:
    """Return d iff its keys are exactly the int seeds of MODELS (R11 lesson)."""
    keys = list(d.keys()) if isinstance(d, dict) else None
    if (
        keys is None
        or not all(type(key) is int for key in keys)
        or set(keys) != set(MODELS)
        or len(keys) != len(MODELS)
    ):
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"{what}: keys must be the int seeds")
    return d


def expected_meta(model, step_label) -> dict:
    if type(model) is not int or model not in MODELS or step_label not in ("step5000", "step0"):
        raise ValueError(f"no checkpoint {model!r}/{step_label!r}")
    c, ck = CONTRACT, CONTRACT["checkpoints"][str(model)]
    fam, mode = c["run_key"][0], c["run_key"][1]
    return {
        "artifact_id": ck[step_label],
        "artifact_type": "Checkpoint",
        "run_key": [fam, mode, model],
        "status": "complete",
        "step": c["steps"]["trained" if step_label == "step5000" else "init"],
        "init_seed_key": f"init/{fam}/{mode}/{model}",
        "init_seed": ck["init_seed"],
        "payload_sha256": ck["meta_payload_sha256"][step_label],
    }


def _same(a, b) -> bool:  # exact and type-strict; lists element-wise
    return type(a) is type(b) and (
        all(map(_same, a, b)) and len(a) == len(b) if isinstance(a, list) else a == b
    )


def check_checkpoint_meta(meta, expected) -> dict:
    """Pure (API.md §14.1, R19); a missing key is a mismatch, never an exception."""
    sk, missing, mismatches = expected["init_seed_key"], object(), []
    items = [
        ("artifact_id", ("artifact_id",), "artifact_id"),
        ("artifact_type", ("artifact_type",), "artifact_type"),
        ("config.run_key", ("config", "run_key"), "run_key"),
        ("config.step", ("config", "step"), "step"),
        ("status", ("status",), "status"),
        (f"seed_map[{sk}]", ("seed_map", sk), "init_seed"),
        ("payload_sha256", ("payload_sha256",), "payload_sha256"),
    ]
    for field, path, key in items:
        found = meta
        for k in path:
            found = found.get(k, missing) if isinstance(found, dict) else missing
        if found is missing or not _same(found, expected[key]):
            mismatches.append(
                {
                    "field": field,
                    "expected": expected[key],
                    "found": None if found is missing else found,
                }
            )
    return {
        "status": "FAIL_TECHNICAL/IDENTITY" if mismatches else "PASS",
        "mismatches": mismatches,
        "checked": [f for f, _, _ in items],
    }
