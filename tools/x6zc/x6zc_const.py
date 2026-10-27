"""X6ZC constants: CONTRACT loading, names and bindings, streams (X6ZC-DESIGN-v1; API.md
§3, §20 C-52). Re-exported by x6zc_core. Import reads CONTRACT.json and the protocol only."""
# fmt: off

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _p in (REPO / "tools" / "x6_stage1", HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
import x6s1_data as sd  # noqa: E402, F401  (first: applies the X6S1 sys.path convention)

# isort: split
import numpy as np  # noqa: E402
import x6_model as xm  # noqa: E402

from topo_pilot.contracts import SeedTree  # noqa: E402

# ---- loading, names and bindings (API §3) ----
CONTRACT_PATH, PROTOCOL_FILE = HERE / "CONTRACT.json", HERE / "PROTOCOL_X6ZC_v1.md"
def load_contract(path=CONTRACT_PATH) -> dict:
    c = json.loads(Path(path).read_text("utf-8"))
    if hashlib.sha256(PROTOCOL_FILE.read_bytes()).hexdigest() != c["protocol"]["sha256"].lower():
        raise ValueError("PROTOCOL_X6ZC_v1.md sha256 differs from CONTRACT.json protocol.sha256")
    return c
def frac(s) -> Fraction: return Fraction(str(s))
CONTRACT = load_contract()
KC, _PA, _X = CONTRACT["constants"], CONTRACT["paths"], CONTRACT["x6s1"]
PROTOCOL_ID, PROTOCOL_SHA256 = CONTRACT["protocol"]["id"], CONTRACT["protocol"]["sha256"]
PROJECT_ROOT, X6S1_STORE, STORE = _PA["project_root"], _PA["x6s1_store"], _PA["store"]
WORKTREE, SCRATCH_ROOT, DRY_STORE = _PA["worktree"], _PA["scratch_root"], _PA["dry_store"]
METER_IMPORT_DIR, NA_DIR = _PA["meter_import_dir"], "ZC_NOT_COMMUTATIVE/NA_DIRECTION"
H3, MERGE_COMMIT, CLOSURE = _X["H3"], _X["merge_commit"], tuple(_X["closure_paths"])
X6ZC_MASTER, FAMILIES, VARIANT_ORDER = int(KC["x6zc_master"]), tuple(KC["families"]), tuple(
    KC["variant_order"])
VARIANT_SIGN, W1_TAIL = dict(KC["variant_sign"]), dict(KC["w1_tail_tokens"])
VARIANTS = {F: {v: tuple(tuple(m) for m in ms) for v, ms in KC["variants"][F].items()}
            for F in FAMILIES}
W1_CROSS_STEPS = {v: tuple(s) for v, s in KC["w1_crossing_steps"].items()}
READOUT_OFFSET, LAMBDA_INDEX = dict(KC["readout_offset"]), dict(KC["lambda_index"])
ANSWERS = {v: {k: tuple(x) for k, x in KC["answers"][v].items()} for v in VARIANT_ORDER}
CELLS = {c: {**d, "beta_D": float(d["beta_D"]), "sign": int(d["sign"]), "z": float(d["z"]),
             "b_q": tuple(map(Fraction, d["b_q"])), "r_q": tuple(map(Fraction, d["r_q"]))}
         for c, d in KC["cells"].items()}
CELL_ORDER, _PR = tuple(KC["cell_order"]), {k: tuple(v) for k, v in KC["predictors"].items()}
MODELS, INITS, STAGE_B_ORDER = _PR["models"], _PR["inits"], _PR["stage_b_order"]
FOCAL, K5_MODELS, NA_MODELS = _PR["focal"], _PR["k5"], _PR["na_models"]
K6_CONTROLS, K6_MIN = {F: tuple(m) for F, m in KC["k6_controls"].items()}, dict(KC["k6_min_pass"])
T = {k: (tuple(map(frac, v)) if isinstance(v, list) else frac(v) if isinstance(v, str) else v)
     for k, v in CONTRACT["thresholds"].items()}
B_DRAWS, N_FLOOR, N_D = int(T["b_draws"]), int(T["n_floor"]), int(T["n_d"])
N_LADDER, _S3N = tuple(int(x) for x in T["n_ladder"]), {xm.perm_name(g): g for g in xm.S3_LIST}
_MISS = {"miss1": frozenset({0}), "miss2": frozenset({1}), "miss_both": frozenset({0, 1})}
def stream(name) -> np.random.Generator:
    return SeedTree(X6ZC_MASTER).generator(*KC["streams"][name])
def dry_stream(*names) -> np.random.Generator:
    return SeedTree(X6ZC_MASTER).generator("x6zc", "dry", *names)
def _fl(x) -> float: return float(x)  # a bar compared in float, as written (§20 E-1)
def _ints(row) -> tuple: return tuple(int(w) for w in row)
