"""C2 configuration: bindings, paths, CONTRACT.json loading, constants, exact Fraction levels
and ranks, seeds, and the sys.path convention (API.md §1, §3; C2-FROZEN-v1 §5.2, §6.2, §9.1).

Import reads CONTRACT.json (and, through the reused c1_config, the C1' CONTRACT.json) only. Other
C2 modules read the path constants and CONTRACT through this module at call time (API.md §19.1
E-24), so a monkeypatch of these names takes effect.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
_PATHS = [
    REPO / p
    for p in (
        "tools/c2_readout",
        "tools/c1prime",
        "tools/c1prime_registry",
        "tools/k4b",
        "tools/x6_stage1",
        "tools/x4_circle_history",
        "tools/x4_oracle_profile",
        "tests/oracle_profile",
    )
]
sys.path[:0] = [str(p) for p in _PATHS if str(p) not in sys.path]

import c1_config  # noqa: E402  (its own sys.path convention, unchanged)
import c1_means  # noqa: E402

# ---- bindings (API.md §3.1) ------------------------------------------------------------------
PROTOCOL_ID = "C2-FROZEN-v1"
PROTOCOL_FILE = HERE / "PROTOCOL_C2_v1.md"
PROTOCOL_SHA256 = "4d97d8e258cfab906ccfe1d99564d4dd74202edd96dd63eb836abd64c277a3d8"
ADDENDUM1_SHA256 = "2db09007a1ff9f9706ffe323c0c1d2c49197648473c481c1776a46ae884011a8"
AUTH_PATH = "agent-handoff/archive/owner-decisions-20261015/OWNER_DECISIONS.addendum-22.md"
AUTH_SHA256 = "5a8430f36eb1432030c3ca8c2b3fa3a152193a4d3d80931a73015c413b3fe786"
R_COMMIT = "d44548b073523d402cc31fbfc5440c0d6df37a23"
BASE_COMMIT = "967605c256bcb554f43d4681326d32efc95bfcc9"
CONTRACT_PATH = HERE / "CONTRACT.json"

PROJECT_ROOT = Path("X:/Downloads/projects/topo-pilot")
STORE = PROJECT_ROOT / "c2-readout-store"
WORKTREE = PROJECT_ROOT / "topo-pilot-c2"
MAILBOX = PROJECT_ROOT / "agent-handoff"
ARTIFACT_ROOT = PROJECT_ROOT / "topo-pilot" / "artifacts"
C1P_STORE = PROJECT_ROOT / "c1prime-store"
K4_FREEZE = PROJECT_ROOT / "x4-circle-history-feas-store-0015" / "FREEZE.json"
X6S1_STORE = PROJECT_ROOT / "x6-stage1-store"
SCRATCH_ROOT = Path("X:/Downloads/topo-scratch")


def load_contract(path=CONTRACT_PATH) -> dict:
    """CONTRACT.json (utf-8); ValueError unless it names the frozen protocol sha256."""
    contract = json.loads(Path(path).read_text(encoding="utf-8"))
    if contract["protocol"]["sha256"] != PROTOCOL_SHA256:
        raise ValueError(
            f"{path}: protocol sha256 {contract['protocol']['sha256']} is not {PROTOCOL_SHA256}"
        )
    return contract


CONTRACT = load_contract()


def frac(s) -> Fraction:
    """The exact rational a CONTRACT string names ("1/240", "1e-9", "0.75")."""
    return Fraction(str(s))


def chart_cfg() -> dict:
    """The C1' CONTRACT chart block (f8df2e43...a379), unchanged."""
    return c1_config.chart_cfg()


def status_of(full) -> tuple:
    return c1_config.status_of(full)


def seed(name) -> int:
    return int(CONTRACT["seeds"][name])


# ---- constants (API.md §2, §3.3) -------------------------------------------------------------
SCOPE = CONTRACT["scope"]
REG_VERSION = CONTRACT["registry_version"]
MODELS = (1729, 2718, 3141)
ROLES = ("H", "Hp", "Hm", "HR")
PAIRS = {"x": ("Hp", "Hm"), "y": ("H", "HR")}
SITES = ("resid_post_2", "resid_post_3", "ln_final_out")
HOOK_KEYS = {"resid_post_2": "rp2", "resid_post_3": "rp3", "ln_final_out": "ln"}
INDEX, BOS, V, N_STATES, D_MODEL, N_READ = 32, 36, 36, 144, 128, 127
BLOCK = int(CONTRACT["splits"]["block_rows"])
SPLIT_BLOCKS = {"fit": 2, "feas": 1, "val": 1}
TEST_K = (1, 2, 4)
N_LADDER = (4096, 8192, 16384)
PROCESS = ("cylinder", "overlap", "1.25")
K_PRIMARY, K_VARIANTS, N_NUIS = 3, (1, 2), 5
M0_ROWS, X1_LOWID_ROWS, C0V_ROWS, H3_ROWS = 1024, 1024, 512, 4
FAMILIES = ("R", "M", "S*")
PROBLEMS = ("R", "R_K1", "R_K2", "R_E", "M", "S*")
VARIANTS = ("R_K1", "R_K2", "R_E")
FILE_FAMILY = {"R": "R", "M": "M", "S*": "Sstar"}  # file names use Sstar (API.md C-2)

# ---- levels and ranks (Fractions; §6.2) ------------------------------------------------------
_LV = CONTRACT["levels"]
ALPHA = {k: frac(v) for k, v in _LV["alpha"].items()}
VAL_ALPHA = frac(_LV["val_alpha"])
H5_ALPHA = frac(_LV["h5_alpha"])
DESC_ALPHA = frac(_LV["desc_alpha_two_sided"])
POWER = frac(_LV["power"])
_BS = CONTRACT["bootstrap"]
TEST_DRAWS, VAL_DRAWS, DESC_DRAWS = _BS["test_draws"], _BS["val_draws"], _BS["desc_draws"]
ROT_DRAWS, H5_DRAWS = _BS["rot_draws"], _BS["h5_draws"]


def ranks(draws, alpha) -> tuple:
    """(rank of the lower bound, rank of the upper bound) of `draws` at level `alpha`."""
    return c1_means.rank_for(alpha, draws), c1_means.rank_for(1 - alpha, draws)


RANKS = {
    "R": ranks(TEST_DRAWS, ALPHA["R"]),
    "S*": ranks(TEST_DRAWS, ALPHA["S*"]),
    "M": ranks(TEST_DRAWS, ALPHA["M"]),
    "val": ranks(VAL_DRAWS, VAL_ALPHA),
    "h5": c1_means.rank_for(H5_ALPHA, H5_DRAWS),
    "desc": ranks(DESC_DRAWS, DESC_ALPHA),
}
_RK = _BS["ranks"]
if (
    RANKS["R"] != (_RK["test_R_S"]["L"], _RK["test_R_S"]["U"])
    or RANKS["S*"] != RANKS["R"]
    or RANKS["M"] != (_RK["test_M"]["L"], _RK["test_M"]["U"])
    or RANKS["val"] != (_RK["val"]["L"], _RK["val"]["U"])
    or RANKS["h5"] != _RK["h5"]
    or RANKS["desc"] != (_RK["desc_and_rot"]["L"], _RK["desc_and_rot"]["U"])
):
    raise ValueError(f"bootstrap ranks {RANKS} differ from CONTRACT.json {_RK}")

# ---- thresholds (Fractions; §9.1) ------------------------------------------------------------
_T = CONTRACT["thresholds"]
PSI_LOW, PSI_HIGH, V3 = frac(_T["psi_low"]), frac(_T["psi_high"]), frac(_T["v3"])
PLACEBO, TAU_M, E_ABS = frac(_T["placebo"]), frac(_T["tau_M"]), frac(_T["energy_abs"])
E_RAND = frac(_T["energy_rand_multiple"])
RS_A, RS_B, RS_K, RS_N = frac(_T["rs_a"]), frac(_T["rs_b"]), int(_T["rs_k"]), int(_T["rs_n"])
KAPPA_M, H4, H5 = frac(_T["kappa_m"]), frac(_T["h4"]), frac(_T["h5_nat"])
L1_R2, L1_RHO, R1 = frac(_T["l1_r2_code_0"]), frac(_T["l1_rho_inc"]), frac(_T["r1_agreement"])
N2_FLOOR, N2_SLACK = frac(_T["n2_floor"]), frac(_T["n2_slack"])
C0V_SUPPORT = (_T["c0v_support"]["num"], _T["c0v_support"]["den"])
C0V_FIDELITY, C0V_BIN_MIN = frac(_T["c0v_fidelity"]), int(_T["c0v_bin_min_rows"])
C0V_RESULTANT, SUP_MIN = frac(_T["c0v_resultant_max"]), frac(_T["support_min"])
F_DRIFT = frac(_T["f_drift"])
ZERO_MOD, ZERO_CODE = float(_T["zero_modulus"]), float(_T["zero_code_relative"])
RIDGE_GRID = tuple(float(x) for x in _T["ridge_grid"])
ROT_DOSES = ((1, math.pi / 6), (2, math.pi / 3))
if RS_A + RS_N * RS_B != Fraction(RS_K, RS_N) or E_RAND * Fraction(RS_K, RS_N) != PSI_LOW:
    raise ValueError("RS2 constants or the 127/60 multiple are inconsistent")

# ---- tolerances (exact strings, read with frac; §9.3) ----------------------------------------
_TL = CONTRACT["tolerances"]
TAU_X1, X1_ATTAIN = _TL["tau_x1_relative"], _TL["x1_attainability"]
RANK_R = _TL["readout_rank_ratio"]
T_SYM, T_SYM_R = _TL["t1_tau_symmetry"], _TL["t2_rho_R_symmetry"]
T_DEC_POST = _TL["t4_decimal_posterior_predictive_relative"]
T_DEC_SURPRISAL, T_DEC_G = _TL["t5_decimal_surprisal"], "2e-11"
T_NAMED, T_CROSS_G, T_QSUM = (
    _TL["t7_named_canonical_relative"],
    _TL["t8_cross_model_G"],
    _TL["q_sum"],
)
T_GLS_ID, COND_MAX = _TL["t11_gls_identities"], _TL["cond_max"]
SV_RATIO, LW_RATIO = _TL["sv_ratio_min"], _TL["lw_ratio_min"]
GLSREF_PREC, GLSREF_RHO = int(_TL["t12_glsref_precision_digits"]), _TL["t12_glsref_rho_ref_max"]
GLSREF_PROJ, GLSREF_INFLATE = _TL["t12_glsref_projector_relative"], _TL["t12_glsref_inflation"]
T18, GUARD_REL = "1e-12", _TL["guard_relative"]
UNIT_ROUNDOFF = Fraction(1, 2**53)
