"""HWSU configuration: CONTRACT loader, constants, blindness guard, HANDOFF mirror (API.md §1).

Import puts the reused tool folders on sys.path (insert if absent), reads CONTRACT JSON files
only and computes constants. It never opens HANDOFF.json or any store file.
"""

from __future__ import annotations  # noqa: I001

import copy
import fnmatch
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
_ORDER = ("hwsu", "hwsc", "hwsb", "hws", "k4b", "c1prime", "c1prime_registry",
          "x4_circle_history", "x4_oracle_profile", "c2_nd", "c2_readout", "x6_stage1")
for _sub in reversed(_ORDER):
    _p = str(REPO / "tools" / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import hwsc_config  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

CONTRACT_OF_PATH = HERE / "CONTRACT_OF.json"
CONTRACT_PATH = HERE / "CONTRACT.json"
PROTOCOL_PATH = HERE / "PROTOCOL_HWSU_v1.md"
API_PATH = HERE / "API.md"
TEST_PLAN_PATH = HERE / "TEST_PLAN.md"
ROOT = Path("X:/Downloads/projects/topo-pilot")
STORE = ROOT / "hwsu-store"
SCRATCH = Path("X:/Downloads/topo-scratch")
DRY_STORE = SCRATCH / "hwsu-dry-of"
MAILBOX = ROOT / "agent-handoff"
STUDY_LEDGER = MAILBOX / "HWSU_CPU_LEDGER.json"
HWSC_STORE = ROOT / "hwsc-store"
HANDOFF_PATH = ROOT / "hwsb-store" / "HANDOFF.json"
SELECTION_PATH = ROOT / "hws-store" / "SELECTION.json"

BINDING = "FAIL_TECHNICAL/BINDING"


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def merge(a, b, path="") -> dict:
    """Recursive union of two dicts; any shared non-dict key is an override (D-2)."""
    out = {}
    for k in list(a) + [k for k in b if k not in a]:
        here = f"{path}.{k}" if path else str(k)
        if k in a and k in b:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                out[k] = merge(a[k], b[k], here)
            else:
                raise C1GateFailure(BINDING, f"override: {here}")
        else:
            out[k] = copy.deepcopy(a[k] if k in a else b[k])
    return out


def load_contract(of_path=CONTRACT_OF_PATH, phase2_path=CONTRACT_PATH) -> dict:
    try:
        raw = Path(of_path).read_bytes()
        of = json.loads(raw.decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise C1GateFailure(BINDING, f"CONTRACT_OF unreadable: {exc!r}") from exc
    if phase2_path is None or not Path(phase2_path).exists():
        return copy.deepcopy(of)
    try:
        p2 = json.loads(Path(phase2_path).read_bytes().decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise C1GateFailure(BINDING, f"CONTRACT unreadable: {exc!r}") from exc
    if not isinstance(p2, dict) or p2.get("contract_of_sha256") != _sha_bytes(raw):
        raise C1GateFailure(BINDING, "contract_of_sha256 absent or unequal")
    return merge(of, p2)


CONTRACT = load_contract()
CONTRACT_SHA256 = {
    "of": _sha_bytes(CONTRACT_OF_PATH.read_bytes()),
    "phase2": _sha_bytes(CONTRACT_PATH.read_bytes()) if CONTRACT_PATH.exists() else None,
}

KEY = "W12-q1-s1.75-p0.2"
PROC = ("cylinder", "overlap", "1.75")
SCOPE_OF, SCOPE_U, SCOPE_DRY = "hwsu-of-v1", "hwsu-v1", "hwsu-dry-v1"
MASTERS = (620301, 620302, 620303)
SEEDS_OF = {"headroom": 640101, "share": 640102, "p1_sd": 640103, "p1_centred": 640104,
            "lemma_p": 640105}
DRY_SEEDS_OF = {"headroom": 649901, "share": 649902, "p1_sd": 649903, "p1_centred": 649904,
                "lemma_p": 649905}
BLOCK_OF, BLOCKS_OF, N_FIT, N_EVAL = 4096, (0, 1), 8192, 8192
DRAWS, LADDER, POWER = 5000, (4096, 8192, 16384, 32768), 0.80
ALPHA_HEADROOM, ALPHA_VAL, ALPHA_FAMILY = Fraction(1, 20), Fraction(1, 60), Fraction(1, 300)
HEADROOM, SHARE_CEIL = Fraction(1, 50), Fraction(1, 5)
RESP_LO, RESP_HI, SHARE_LO, SHARE_HI = (Fraction(1, 10), Fraction(3, 10), Fraction(1, 10),
                                        Fraction(1, 2))
LAMBDA_KO3 = Fraction(1, 5)
ALT_RESP, ALT_SHARE = Fraction(1, 10), Fraction(3, 100)
KO_TOL, DEC_TOL, STAT_TOL, M4_TOL, LEMMA_P_SE = 1e-12, Fraction(1, 10**10), 1e-12, 1e-12, 5
K_HARM, V, N_NUIS, DESIGN_RANK = 3, 36, 5, 47
DECIMAL_ROWS = 4


# ------------------------------------------------------------------ blindness guard (§8.1, J9)
def _posix(path) -> str:
    return Path(path).resolve().as_posix().lower().rstrip("/")


def _hwsd_allowed(q: str) -> bool:
    parts = q.split("/")
    if len(parts) == 1:
        return (fnmatch.fnmatchcase(q, "registry_obligation*.json")
                or fnmatch.fnmatchcase(q, "reservation*.json") or q == "reservations")
    return len(parts) == 2 and parts[0] == "reservations" and parts[1].endswith(".json")


def blinded(path, root=ROOT) -> bool:
    if hwsc_config.blinded(path, root):
        return True
    p, r = _posix(path), _posix(root)
    for d in ("hwsc-store/stages/s8", "hwsc-store/stages/s5"):
        if p == f"{r}/{d}" or p.startswith(f"{r}/{d}/"):
            return True
    if p in {f"{r}/hwsc-store/stages/e1/l1.json", f"{r}/hwsc-store/sealed_validation.json",
             f"{r}/hwsc-store/sealed_opened.json"}:
        return True
    m = r + "/agent-handoff"
    if p.startswith(m + "/"):
        for comp in p[len(m) + 1:].split("/"):
            if "hws-dyn" in comp or comp.startswith(("hwsd-", "hwsd_")):
                return True
    if p.startswith(r + "/hwsd-store/"):
        return not _hwsd_allowed(p[len(r + "/hwsd-store/"):])
    return False


def public_summary(path) -> bool:
    return hwsc_config.public_summary(path)


def guard(path, root=ROOT) -> Path:
    if blinded(path, root) or public_summary(path):
        raise C1GateFailure("FAIL_TECHNICAL/BLINDNESS", str(path))
    return Path(path)


def read_bytes(path, root=ROOT) -> bytes:
    return guard(path, root).read_bytes()


def read_json(path, root=ROOT):
    return json.loads(read_bytes(path, root).decode("utf-8-sig"))


def sha256_file(path, root=ROOT) -> str:
    return _sha_bytes(read_bytes(path, root))


# ----------------------------------------------------------------------- HANDOFF mirror (D-4)
def load_handoff_u(path=HANDOFF_PATH, expected_sha256=None) -> dict:
    want = CONTRACT["handoff"]["sha256"] if expected_sha256 is None else expected_sha256
    raw = read_bytes(path)
    if _sha_bytes(raw) != want:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", "HANDOFF.json sha256 differs")
    d = json.loads(raw)
    try:
        return {"p_D2a": float(d["p_D2a"]),
                "stage_c_exclusions": tuple(str(x) for x in d["stage_c_exclusions"])}
    except (KeyError, TypeError) as exc:
        raise C1GateFailure("FAIL_TECHNICAL/IDENTITY", f"HANDOFF.json key: {exc!r}") from exc


def dry_store_ok(path) -> bool:
    """True iff path lies under SCRATCH/hwsu-dry* or SCRATCH/test_hwsu-* (dry guard, E-4)."""
    try:
        rel = Path(path).resolve().relative_to(SCRATCH.resolve())
    except (ValueError, OSError):
        return False
    first = rel.parts[0].lower() if rel.parts else ""
    return first.startswith(("hwsu-dry", "test_hwsu-"))
