"""C2ND configuration: bindings, paths, CONTRACT.json loading, constants, exact Fraction levels
and ranks, seeds, and the sys.path convention (API.md §1, §3, §20; C2ND-DESIGN-v1 §2.1, §4.1,
§6.1, §11.3).

Import reads the two CONTRACT.json files (C2's through c2_config, this one) and nothing else.
Other C2ND modules read the path constants and CONTRACT through this module at call time, so a
monkeypatch of these names takes effect (C2 API §19.1 E-24). The C2 path constants
(ARTIFACT_ROOT, C1P_STORE, X6S1_STORE, K4_FREEZE) stay in c2_config and are read there.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (REPO / "tools" / "c2_readout", HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import c2_config  # noqa: E402  (the C2 sys.path convention, unchanged)

# isort: split
import c1_means  # noqa: E402

# ---- bindings (API.md §3.1) ------------------------------------------------------------------
PROTOCOL_ID = "C2ND-FROZEN-v1"
DESIGN_ID = "C2ND-DESIGN-v1"
PROTOCOL_FILE = HERE / "PROTOCOL_C2ND_v1.md"
PROTOCOL_SHA256 = "4381655dc0b1e0f8ce50b48c91c756e5eb8e7fae3d4c8592599ab84368d8f0fd"
MAILBOX_FILE = "agent-handoff/planning/responses/C2ND-DESIGN-v1.md"
BASE_COMMIT = "b67f3327e9220a0a17f665eec888f39859cc4096"
C2_H2 = "3e234b38077f84ddebfa380120938b8847f40e03"
CONTRACT_PATH = HERE / "CONTRACT.json"

PROJECT_ROOT = Path("X:/Downloads/projects/topo-pilot")
STORE = PROJECT_ROOT / "c2nd-store"
C2_STORE = PROJECT_ROOT / "c2-readout-store"
WORKTREE = PROJECT_ROOT / "topo-pilot-c2nd"
MAILBOX = PROJECT_ROOT / "agent-handoff"
HWS_STORE = PROJECT_ROOT / "hws-store"
X6ZC_STORE = PROJECT_ROOT / "x6zc-store"
SCRATCH_ROOT = Path("X:/Downloads/topo-scratch")


def load_contract(path=CONTRACT_PATH) -> dict:
    """CONTRACT.json (utf-8); ValueError unless it names the C2ND protocol sha256."""
    contract = json.loads(Path(path).read_text(encoding="utf-8"))
    if contract["protocol"]["sha256"] != PROTOCOL_SHA256:
        raise ValueError(
            f"{path}: protocol sha256 {contract['protocol']['sha256']} is not {PROTOCOL_SHA256}"
        )
    return contract


CONTRACT = load_contract()
AUTH_PATH = CONTRACT["protocol"]["auth"]["file"]
AUTH_SHA256 = CONTRACT["protocol"]["auth"]["sha256"]


def frac(s) -> Fraction:
    """The exact rational a CONTRACT string names ("1/300", "1e-9", "6")."""
    return c2_config.frac(s)


def status_of(full) -> tuple:
    return c2_config.status_of(full)


def seed(name) -> int:
    return int(CONTRACT["seeds"][name])


def rank(draws, p) -> int:
    """The rank ceil(draws * p) of c1_means.rank_for."""
    return c1_means.rank_for(p, int(draws))


# ---- constants (API.md §2, §3.3) -------------------------------------------------------------
SCOPE = CONTRACT["scope"]
DRY_SCOPE = CONTRACT["dry_scope"]
REG_VERSION = CONTRACT["registry_version"]
REG_NAMES = tuple(CONTRACT["registry_names"])
MODELS = (1729, 2718, 3141)
ROLES = c2_config.ROLES
PAIRS = c2_config.PAIRS
SITES = c2_config.SITES
INDEX = int(CONTRACT["sites"]["index"])
BLOCK = int(CONTRACT["splits"]["block_rows"])
SPLITS = ("fit", "feas", "val", "test")
SPLIT_BLOCKS = {"fit": 2, "feas": 1, "val": 1}
TEST_K = tuple(CONTRACT["splits"]["test"]["k"])
N_LADDER = tuple(CONTRACT["thresholds"]["ladder_N"])
PROCESS = ("cylinder", "overlap", "1.25")
M0_ROWS = int(CONTRACT["splits"]["m0_rows"])
LOWID_ROWS = int(CONTRACT["splits"]["lowid_rows"])
H3_ROWS = int(CONTRACT["splits"]["h3_rows"])
FAMILIES = tuple(CONTRACT["families"])
FILE_FAMILY = dict(CONTRACT["file_family"])
_DC = CONTRACT["decoys"]
DECOYS = tuple(_DC["keys"])
HEAD_EDITS = tuple(_DC["head_edits"])
COORD_DECOYS = tuple(_DC["coordinate"])
KC_CASES = tuple(_DC["kc_cases"])
KCR_CASES = tuple(_DC["kcr_cases"])
REFITS = ("RD", "RT")
VARIANTS = ("R_E", "R_K1", "R_K2")
MODULES = tuple(CONTRACT["modules"])

# ---- decoy constants (exact; §2.6, Lemma DC4) ------------------------------------------------
G_D = int(frac(_DC["g_D"]))
RHO = frac(_DC["rho"])
DECOY_VERSION = _DC["version"]
NULL_SV_REL = frac(_DC["null_sv_relative"])
U_SV_RATIO = frac(_DC["construction_gates"]["sv_ratio_min"])
U_RANK = int(_DC["construction_gates"]["rank_LBV0"])
T_COND_MAX = frac(_DC["construction_gates"]["cond_T_max"])
if (G_D, RHO) != (6, Fraction(23, 25)):
    raise ValueError(f"decoy constants g_D={G_D}, rho={RHO} differ from protocol §2.6")

# ---- levels and ranks (Fractions; §4.1) ------------------------------------------------------
_LV, _BS = CONTRACT["levels"], CONTRACT["bootstrap"]
ALPHA = {k: frac(v) for k, v in _LV["alpha"].items()}
VAL_ALPHA = frac(_LV["val_alpha"])
H5_ALPHA = frac(_LV["h5_alpha"])
DESC_ALPHA = frac(_LV["desc_alpha_two_sided"])
POWER = frac(_LV["power"])
TEST_DRAWS, VAL_DRAWS, DESC_DRAWS = _BS["test_draws"], _BS["val_draws"], _BS["desc_draws"]
H5_DRAWS, KC_TEST_DRAWS = _BS["h5_draws"], _BS["kc_test_draws"]


def ranks(draws, alpha) -> tuple:
    """(rank of the lower bound, rank of the upper bound) of `draws` at level `alpha`."""
    return rank(draws, alpha), rank(draws, 1 - Fraction(alpha))


RANKS = {
    "N-R": ranks(TEST_DRAWS, ALPHA["N-R"]),
    "D": ranks(TEST_DRAWS, ALPHA["D"]),
    "N-M": ranks(TEST_DRAWS, ALPHA["N-M"]),
    "val": ranks(VAL_DRAWS, VAL_ALPHA),
    "h5": rank(H5_DRAWS, H5_ALPHA),
    "desc": ranks(DESC_DRAWS, DESC_ALPHA),
}
_RK = _BS["ranks"]
_WANT = {
    "N-R": (_RK["test_NR_D"]["L"], _RK["test_NR_D"]["U"]),
    "D": (_RK["test_NR_D"]["L"], _RK["test_NR_D"]["U"]),
    "N-M": (_RK["test_NM"]["L"], _RK["test_NM"]["U"]),
    "val": (_RK["val"]["L"], _RK["val"]["U"]),
    "h5": _RK["h5"],
    "desc": (_RK["desc_and_kc_test"]["L"], _RK["desc_and_kc_test"]["U"]),
}
_PROTO = {"N-R": (67, 19934), "D": (67, 19934), "N-M": (56, 19945), "val": (84, 4917)}
_PROTO.update(h5=250, desc=(125, 4875))
if RANKS != _WANT or RANKS != _PROTO:
    raise ValueError(f"bootstrap ranks {RANKS} differ from CONTRACT.json {_RK} or §4.1")

# ---- thresholds (Fractions; C2's owner-approved values, unchanged) ---------------------------
_T = CONTRACT["thresholds"]
PSI_LOW, PSI_HIGH, PSI_090 = frac(_T["psi_low"]), frac(_T["psi_high"]), frac(_T["psi_090"])
NEG_LOW = frac(_T["wc_lower_line"])  # the Wc line: psi_comp > -1/10
V3, PLACEBO, TAU_M = frac(_T["v3"]), frac(_T["placebo"]), frac(_T["tau_M"])
E_ABS, E_RAND = frac(_T["energy_abs"]), frac(_T["energy_rand_multiple"])
RS_A, RS_B, KAPPA_M = frac(_T["rs_a"]), frac(_T["rs_b"]), frac(_T["kappa_m"])
H4 = {"x": frac(_T["h4_x"]), "y": frac(_T["h4_y"])}
H5, ORACLE_HEADROOM = frac(_T["h5_nat"]), frac(_T["oracle_headroom_nat"])
L1_R2, L1_RHO, R1 = frac(_T["l1_r2_code_0"]), frac(_T["l1_rho_inc"]), frac(_T["r1_agreement"])
N2_FLOOR, N2_SLACK = frac(_T["n2_floor"]), frac(_T["n2_slack"])
SUP_MIN, F_DRIFT = frac(_T["support_min"]), frac(_T["f_drift"])
P1_ALT_NR_NM, P1_ALT_D = Fraction(1, 10), Fraction(3, 100)  # §4.5 (CONTRACT p1_alternative)
P1_GATED = {k: tuple(v) for k, v in _T["p1_gated"].items()}

# ---- tolerances (exact strings, read with frac) ----------------------------------------------
_TL = CONTRACT["tolerances"]
TAU_X1, X1_ATTAIN = _TL["tau_x1_relative"], _TL["x1_attainability"]
ORACLE_ID, M0D_READOUT = _TL["oracle_identity"], _TL["m0d_readout"]
M0D_COORD, ADAPTER = _TL["m0d_coordinate_map"], _TL["adapter_identities"]
DX_A, DX_E, GUARD_REL = _TL["dx_A"], _TL["dx_E"], _TL["guard_relative"]
