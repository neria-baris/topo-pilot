"""HWS worlds: constants, grid, keys, tiers, builders, alias map, symmetry, E1-E3 (API.md §1).

Protocol §4.1-§4.6 and §5.1 E1-E3. Import puts the reused tool folders on sys.path (insert if
absent) and reads CONTRACT.json; it performs no other I/O and no computation beyond constants.
"""

from __future__ import annotations

import itertools
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for _sub in ("hws", "k4b", "c1prime", "x4_circle_history", "x4_oracle_profile"):
    _p = str(REPO / "tools" / _sub)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np  # noqa: E402, I001
import oracle_profile  # noqa: E402
from scipy.special import logsumexp  # noqa: E402

from topo_pilot.contracts import SeedTree, StageFailure  # noqa: E402
from topo_pilot.process import EmissionConfig, Identical, OverlapGaussian  # noqa: E402
from topo_pilot.process import TransitionBuilder, TransitionConfig, Unique  # noqa: E402
from topo_pilot.process._geometry import point_distances  # noqa: E402
from topo_pilot.process.centers import check_centers_in_chart  # noqa: E402
from topo_pilot.world import WorldConfig  # noqa: E402
from topo_pilot.world import build_world as _src_build_world  # noqa: E402

CONTRACT_PATH = HERE / "CONTRACT.json"
PROTOCOL_PATH = HERE / "PROTOCOL_HWS_v1.md"
ROOT = Path("X:/Downloads/projects/topo-pilot")
STORE = ROOT / "hws-store"
DRY_STORE = Path("X:/Downloads/topo-scratch/hws-dry")


def load_contract(path=CONTRACT_PATH) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


CONTRACT = load_contract()


class HwsStop(RuntimeError):
    """A technical stop with a full status string (API.md §0)."""

    def __init__(self, status: str, reason: str = ""):
        super().__init__(f"{status}: {reason}")
        self.status = str(status)
        self.reason = str(reason)


_LEV = CONTRACT["levels"]
H, L, N_AXIAL = 12, 32, 6
P_LEVELS = tuple(Fraction(s) for s in _LEV["p"])
SIGMA_LEVELS = tuple(Fraction(s) for s in _LEV["sigma"])
Q_LEVELS = tuple(int(q) for q in _LEV["q"])
W_LEVELS = tuple(int(w) for w in _LEV["W"])
X1_P = tuple(Fraction(s) for s in _LEV["x1"]["p"])
X1_SIGMA = tuple(Fraction(s) for s in _LEV["x1"]["sigma"])
S2_P_MID = {(Fraction(a), Fraction(b)): Fraction(m) for a, b, m in _LEV["s2_p_edges"]}
S2_SIGMA_MID = {(Fraction(a), Fraction(b)): Fraction(m) for a, b, m in _LEV["s2_sigma_edges"]}
P_INDEX = {Fraction(k): Fraction(v) for k, v in _LEV["index"]["p"].items()}
SIGMA_INDEX = {Fraction(k): Fraction(v) for k, v in _LEV["index"]["sigma"].items()}


def world_key(W, q, sigma, p) -> str:
    return f"W{int(W)}-q{int(q)}-s{float(sigma)!r}-p{float(p)!r}"


@dataclass(frozen=True, order=False)
class World:
    W: int
    q: int
    sigma: Fraction
    p: Fraction

    @property
    def key(self) -> str:
        return world_key(self.W, self.q, self.sigma, self.p)

    @property
    def sigma_f(self) -> float:
        return float(self.sigma)

    @property
    def p_f(self) -> float:
        return float(self.p)


W0 = World(12, 1, Fraction(5, 4), Fraction(1, 5))


def grid() -> list:
    """The 225 grid worlds of §4.4: W, then q, sigma, p ascending (choice 4)."""
    return [World(*t) for t in itertools.product(W_LEVELS, Q_LEVELS, SIGMA_LEVELS, P_LEVELS)]


def x1_worlds(add_p: bool, add_sigma: bool, cells) -> list:
    ps = P_LEVELS + (X1_P if add_p else ())
    ss = SIGMA_LEVELS + (X1_SIGMA if add_sigma else ())
    cs = sorted({(int(a), int(b)) for a, b in cells})
    out = [World(W, q, s, p) for (W, q), s, p in itertools.product(cs, ss, ps)]
    return [w for w in out if not (w.sigma in SIGMA_LEVELS and w.p in P_LEVELS)]


def tier(w) -> int:
    if w.W == 12 and w.q == 1:
        return 0
    if w.W == 12 and w.q == 2:
        return 1
    if w.W in (8, 16):
        return 2
    raise ValueError(f"no tier for W = {w.W}, q = {w.q} (never eligible)")


def changed_factors(w) -> int:
    return int(w.p != W0.p) + int(w.sigma != W0.sigma) + int(w.q != 1) + int(w.W != 12)


def distance(w) -> Fraction:
    off_w = 0 if w.W == 12 else 1
    return P_INDEX[Fraction(w.p)] + SIGMA_INDEX[Fraction(w.sigma)] + (w.q - 1) + off_w


def cells_of(worlds) -> list:
    return sorted({(w.W, w.q) for w in worlds})


# ------------------------------------------------------------------ centres, alias map, features


def centres(W, n_axial=N_AXIAL) -> np.ndarray:
    """Rectangular spacing-2 centres, row j = n_axial*i + b at (0.5 + 2i, 0.5 + 2b) (MD-5)."""
    ib = itertools.product(range(int(W) // 2), range(int(n_axial)))
    return np.array([(0.5 + 2 * i, 0.5 + 2 * b) for i, b in ib], dtype=np.float64)


def anchored_labels(W, q) -> np.ndarray:
    half = int(W) // 2
    m = -(-(half - 1) // int(q))
    return np.array([0] + [1 + ((i - 1) % m) for i in range(1, half)], dtype=np.int64)


def unanchored_labels(W, q) -> np.ndarray:
    half = int(W) // 2
    if half % int(q):
        raise ValueError(f"unanchored map needs (W/2) mod q == 0, got W = {W}, q = {q}")
    period = half // int(q)
    return np.array([i % period for i in range(half)], dtype=np.int64)


def n_labels(labels) -> int:
    return int(np.max(labels)) + 1


def v_prime(labels, n_axial=N_AXIAL) -> int:
    return int(n_axial) * n_labels(labels)


def symbol_sizes(labels, n_axial=N_AXIAL) -> np.ndarray:
    counts = np.bincount(np.asarray(labels, dtype=np.int64), minlength=n_labels(labels))
    return np.repeat(counts, int(n_axial)).astype(np.int64)


def merge_columns(E_centres, labels, n_axial=N_AXIAL) -> np.ndarray:
    """E'[:, n_axial*g + b] = sum over i with g(i) = g of E[:, n_axial*i + b], ascending i."""
    E = np.asarray(E_centres, dtype=np.float64)
    lab = np.asarray(labels, dtype=np.int64)
    nax = int(n_axial)
    out = np.zeros((E.shape[0], nax * n_labels(lab)), dtype=np.float64)
    first = np.zeros(n_labels(lab), dtype=bool)
    for i, g in enumerate(lab):
        src, dst = E[:, nax * i : nax * i + nax], slice(nax * g, nax * g + nax)
        out[:, dst] = src if not first[g] else out[:, dst] + src
        first[g] = True
    return out


def features(coords, W) -> np.ndarray:
    a = 2.0 * np.pi * np.asarray(coords, dtype=np.float64)[:, 0] / W
    return np.column_stack((np.cos(a), np.sin(a)))


# ------------------------------------------------------------------------------------ builders


def build_world(W, Hh=H):
    return _src_build_world(WorldConfig("cylinder", (int(W), int(Hh)), "flat"))


def build_transition(world, p):
    return TransitionBuilder().build(world, TransitionConfig(p_stay=float(p)))


def _mirrored(world, cen, sigma) -> np.ndarray:
    """The 4-line softmax of emission._overlap_core (mirrored, not imported; §12.2 item 3)."""
    check_centers_in_chart(world, cen)
    d = point_distances(world, cen, "flat")
    logits = -(d**2) / (2.0 * float(sigma) ** 2)
    return np.exp(logits - logsumexp(logits, axis=1, keepdims=True))


def centre_emission(world, W, sigma, n_axial=N_AXIAL) -> np.ndarray:
    if int(W) == 12 and int(n_axial) == 6:
        cfg = EmissionConfig("overlap", 36, float(sigma), "grid")
        spec = OverlapGaussian().build(world, cfg, SeedTree(1729))
        return oracle_profile.canonical_emission(spec.E, spec.symbol_perm)
    return _mirrored(world, centres(W, n_axial), sigma)


def _base(key, wk, t, nax, hh, sigma) -> dict:
    keys = ("key", "world_key", "W", "q", "sigma", "p", "tier", "n_axial", "Hh")
    return dict(zip(keys, (key, wk, wk.W, wk.q, sigma, wk.p, t, int(nax), int(hh))))


def _finish(base: dict, world, tr, E_centres, labels) -> dict:
    nax, T, pi = base["n_axial"], np.asarray(tr.T, np.float64), np.asarray(tr.pi, np.float64)
    E = merge_columns(E_centres, labels, nax)
    coords = np.asarray(world.coords, dtype=np.float64)
    check = oracle_profile.validate_process(T, E, pi, tol=1e-12)
    arrays = {"world": world, "T": T, "pi": pi, "E_centres": E_centres, "E": E}
    arrays.update(labels=labels, sizes=symbol_sizes(labels, nax), V=v_prime(labels, nax))
    arrays.update(N=int(pi.shape[0]), coords=coords, features=features(coords, base["W"]))
    return dict(base, **arrays, e1={"status": "PASS", "validate": check})


def _guarded(base: dict, build) -> dict:
    try:
        return build()
    except (StageFailure, oracle_profile.ProfileError) as exc:
        return dict(base, e1={"status": "INELIGIBLE/E1", "reason": f"{type(exc).__name__}: {exc}"})


def _labels(alias, W, q) -> np.ndarray:
    if alias not in ("anchored", "unanchored"):
        raise ValueError(f"alias must be anchored or unanchored, got {alias!r}")
    return (anchored_labels if alias == "anchored" else unanchored_labels)(W, q)


def build_process(w, alias="anchored", Hh=H, n_axial=N_AXIAL) -> dict:
    """§4.6 steps 1-5 in memory (no store writes); tier None for the cell (12, 3) (E13)."""
    lab = _labels(alias, w.W, w.q)
    base = _base(w.key, w, None if (w.W, w.q) == (12, 3) else tier(w), n_axial, Hh, w.sigma)

    def build():
        world = build_world(w.W, Hh)
        tr = build_transition(world, w.p)
        return _finish(base, world, tr, centre_emission(world, w.W, w.sigma, n_axial), lab)

    return _guarded(base, build)


def build_known_zero(kind) -> dict:
    """U (Unique, V = 144, n_axial 12) or N (Identical, V = 36, n_axial 6) at w0 geometry."""
    if kind not in ("U", "N"):
        raise ValueError(f"kind must be U or N, got {kind!r}")
    nax, model, mode, V = (
        (12, Unique, "unique", 144) if kind == "U" else (6, Identical, "identical", 36)
    )
    base = _base(f"{kind}-W12", W0, 0, nax, H, None)

    def build():
        world = build_world(12)
        spec = model().build(world, EmissionConfig(mode, V, None, "grid"), SeedTree(1729))
        E = oracle_profile.canonical_emission(spec.E, spec.symbol_perm)
        lab = np.arange(V // nax, dtype=np.int64)
        return _finish(base, world, build_transition(world, W0.p), E, lab)

    return _guarded(base, build)


def build_tiny(sigma=Fraction(1), p=Fraction(1, 2), alias="anchored", q=1) -> dict:
    """DR1 tiny cylinder W = 6, H = 2, three centres (0.5 + 2i, 0.5), n_axial 1 (E13)."""
    lab = _labels(alias, 6, q)
    wk = World(6, int(q), Fraction(sigma), Fraction(p))
    base = _base("TINY-" + wk.key, wk, None, 1, 2, wk.sigma)

    def build():
        world = build_world(6, 2)
        E_c = _mirrored(world, centres(6, n_axial=1), sigma)
        return _finish(base, world, build_transition(world, p), E_c, lab)

    return _guarded(base, build)


# ---------------------------------------------------------------------- symmetry, E1-E3


def translate_states(W, Hh, s) -> np.ndarray:
    z = np.arange(int(W) * int(Hh), dtype=np.int64)
    return ((z // Hh + s) % W) * Hh + z % Hh


def reflect_states(W, Hh, c) -> np.ndarray:
    z = np.arange(int(W) * int(Hh), dtype=np.int64)
    return ((c - z // Hh) % W) * Hh + z % Hh


def symmetry_check(E, W, Hh=H, tol=1e-9) -> dict:
    E = np.asarray(E, dtype=np.float64)
    dt = {s: float(np.max(np.abs(E[translate_states(W, Hh, s)] - E))) for s in range(1, W)}
    dr = {c: float(np.max(np.abs(E[reflect_states(W, Hh, c)] - E))) for c in range(W)}
    tr = [s for s, d in dt.items() if d <= tol]
    rf = [c for c, d in dr.items() if d <= tol]
    rec = {"translations": tr, "reflections": rf, "min_dev_translation": min(dt.values())}
    return dict(rec, min_dev_reflection=min(dr.values()), symmetric=bool(tr or rf))


def e2_check(p_v, sizes, V_centres) -> dict:
    worst, ok = None, True
    for v, (pv, sz) in enumerate(zip(np.asarray(p_v, dtype=np.float64), sizes)):
        thr = Fraction(int(sz), 2 * int(V_centres))
        exact = Fraction(float(pv))
        ok = ok and exact >= thr
        ratio = exact / thr
        if worst is None or ratio < worst[0]:
            worst = (ratio, {"v": v, "p_v": float(pv), "threshold": str(thr)})
    return {"status": "PASS" if ok else "INELIGIBLE/E2", "worst": worst[1] if worst else None}


def exact_filters(proc, p_v) -> dict:
    e1 = proc["e1"]
    if "E" not in proc:
        return {"status": e1["status"], "e1": e1, "e2": None, "e3": None}
    e2 = e2_check(p_v, proc["sizes"], int(np.sum(proc["sizes"])))
    sym = symmetry_check(proc["E"], proc["W"], proc["Hh"])
    e3 = {"status": "INELIGIBLE/E3" if sym["symmetric"] else "PASS", "symmetry": sym}
    status = next((r["status"] for r in (e1, e2, e3) if r["status"] != "PASS"), "PASS")
    return {"status": status, "e1": e1, "e2": e2, "e3": e3}
