"""C1' configuration: CONTRACT.json loading and constants (API.md §1; protocol §14, §17).

JSON null decodes to +inf for chart.lift_cpu_cap_s and resources.cpu_cap_s (owner resource
override, §14; review flag F5) before any cfg reaches cochain. Import reads CONTRACT.json only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (HERE, REPO / "tools" / "x4_circle_history", REPO / "tools" / "x4_oracle_profile"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
CONTRACT_PATH = HERE / "CONTRACT.json"

MODELS = (1729, 2718, 3141)
SITE = "resid_post_3"
INDEX = 32
BOS = 36
CHART_KERNEL_KEYS = ("field", "lift_bounds", "lift_node_limit", "lift_rounding_tol",
                     "local_passes", "local_vertices", "extension_k", "support_min_resultant",
                     "fidelity_min_agreement", "phase_bins", "phase_bin_min_rows",
                     "overall_resultant_max")


def _inf_if_null(value):
    return float("inf") if value is None else value


def load_contract(path=CONTRACT_PATH) -> dict:
    contract = json.loads(Path(path).read_text(encoding="utf-8"))
    contract["chart"]["lift_cpu_cap_s"] = _inf_if_null(contract["chart"].get("lift_cpu_cap_s"))
    contract["resources"]["cpu_cap_s"] = _inf_if_null(contract["resources"].get("cpu_cap_s"))
    return contract


CONTRACT = load_contract()


def chart_cfg(contract=None) -> dict:
    """The cfg dict for the frozen chart/cochain kernels (lift cap +inf; operation wall 600)."""
    c = CONTRACT if contract is None else contract
    cfg = {k: c["chart"][k] for k in CHART_KERNEL_KEYS}
    cfg["lift_cpu_cap_s"] = _inf_if_null(c["chart"].get("lift_cpu_cap_s"))
    cfg["native_operation_wall_s"] = float(c["chart"]["native_operation_wall_s"])
    return cfg


def status_of(full: str) -> tuple:
    """'INCONCLUSIVE/SUPPORT' -> ('INCONCLUSIVE', 'SUPPORT'); 'PASS' -> ('PASS', None)."""
    head, _, tail = str(full).partition("/")
    return head, (tail or None)
