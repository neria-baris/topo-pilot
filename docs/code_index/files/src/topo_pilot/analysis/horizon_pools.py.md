# `src/topo_pilot/analysis/horizon_pools.py`

- Source: [src/topo_pilot/analysis/horizon_pools.py](../../../../../../src/topo_pilot/analysis/horizon_pools.py)
- Kind: python
- Lines: 195

## Module docstring

> Horizon feasibility (part e, X4 Phase B): reachable near-Q1 / distinct-Q2 screening.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 16, via package root)
- `from .horizon import hellinger, safe_sqrt` -> [src/topo_pilot/analysis/horizon.py](horizon.py.md) (line 18, via relative)

### External (third-party)

- `numpy` (lines 13, 14)

### Standard library

- `__future__` (lines 7)
- `collections` (lines 10)
- `dataclasses` (lines 11)
- `hashlib` (lines 9)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/analysis/__init__.py](__init__.py.md) (line 18, import)

## Top-level constants

- `ANCHOR_SALT`
- `MIN_ELIGIBLE`
- `MIN_FRACTION`
- `N_ANCHORS`
- `N_NEIGHBOURS`
- `Q1_MAX`
- `Q2_MIN`
- `_COMPONENT`

## Classes and functions

- **function `_fail`** [L30-31]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `select_anchors`** [L34-47]: `def select_anchors(canonical_ids: Sequence[str], n: int = N_ANCHORS, salt: str = ANCHOR_SALT) -> NDArray[np.int64]` - Rows of the ``n`` ids with the smallest ``sha256(salt + id)`` (hex order), in that order.
- **class `Partners`** [L51-59] decorators: @dataclass(frozen=True, eq=False) - Nearest-Q1 partners of each anchor: ``idx [A, k]`` (-1 = none), ``d1 [A, k]`` (NaN = none),
- **function `nearest_partners`** [L62-107]: `def nearest_partners(Q1: NDArray, history_keys: Sequence[str], anchors: NDArray, last_symbol: NDArray | None, canonical_ids: Sequence[str], k: int = N_NEIGHBOURS) -> Partners` - ``k`` nearest Hellinger-Q1 neighbours of each anchor inside one pool.
- **class `PoolScreen`** [L111-121] decorators: @dataclass(frozen=True, eq=False) - Frozen screen of one pool: per-anchor flags, partner Q2 distances and the pool status.
- **function `pair_d2`** [L124-132]: `def pair_d2(Q2: NDArray, anchors: NDArray, partners: Partners) -> NDArray[np.float64]` - ``H(Q2_a, Q2_partner)`` for every anchor/partner slot (NaN where there is no partner).
- **function `screen_pool`** [L135-151]: `def screen_pool(d1: NDArray, d2: NDArray, q1_max: float = Q1_MAX, q2_min: float = Q2_MIN, min_eligible: int = MIN_ELIGIBLE, min_fraction: float = MIN_FRACTION) -> PoolScreen` - Apply the frozen screen: admissible ``d1 <= q1_max``; eligible = any admissible partner;
- **function `practical_verdict`** [L154-171]: `def practical_verdict(statuses: Mapping[str, str], test_pool: str = 'test') -> tuple[str, str]` - ``(GAP | NO_GAP | INCONCLUSIVE, reason)`` from pool statuses (test + dev pools).
- **function `strict_verdict`** [L174-177]: `def strict_verdict(ambient: str) -> str` - SUFFICIENT_AMBIENT iff the ambient map factorizes; otherwise UNRESOLVED (numerical
- **function `overall_verdict`** [L180-195]: `def overall_verdict(ambient: str, factor_conditioned: bool, practical: str, checks_ok: bool) -> tuple[str, str]` - ``(GO | NO-GO | INCONCLUSIVE, reason)`` per protocol x4b-v1 section 7.

