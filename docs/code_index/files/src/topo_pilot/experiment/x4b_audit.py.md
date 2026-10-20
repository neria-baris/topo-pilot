# `src/topo_pilot/experiment/x4b_audit.py`

- Source: [src/topo_pilot/experiment/x4b_audit.py](../../../../../../src/topo_pilot/experiment/x4b_audit.py)
- Kind: python
- Lines: 166

## Module docstring

> X4 Phase B reachable audit per pool and the test-pool agreement checks (protocol §5–§6).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import Partners, PoolScreen, hellinger, nearest_partners, pair_d2, screen_pool, select_anchors` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 12, via package root)
- `from topo_pilot.contracts import OracleOutputs` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 21, via package root)
- `from .x4b import END, FutureMaps, Pool` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 23, via relative)

### External (third-party)

- `numpy` (lines 9, 10)

### Standard library

- `__future__` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x4b2_run.py](x4b2_run.py.md) (line 60, import)
- [src/topo_pilot/experiment/x4b_run.py](x4b_run.py.md) (line 52, import)
- [tests/experiment/test_x4b.py](../../../tests/experiment/test_x4b.py.md) (line 16, import)

## Top-level constants

- `Q1_EQUAL`

## Classes and functions

- **function `_q`** [L28-31]: `def _q(x: NDArray, ps: tuple[float, ...] = (0.0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0)) -> list`
- **function `screen`** [L34-38]: `def screen(pool: Pool, Q1: NDArray, Q2: NDArray, last: NDArray | None, anchors: NDArray) -> tuple[Partners, PoolScreen]` - Partners (same last symbol unless ``last`` is None) and the frozen screen.
- **function `describe`** [L41-78]: `def describe(pool: Pool, anchors: NDArray, partners: Partners, scr: PoolScreen) -> dict` - Descriptive record of one screen (protocol §6 'recorded, never a verdict').
- **function `anchor_table`** [L81-97]: `def anchor_table(pool: Pool, anchors: NDArray, partners: Partners, scr: PoolScreen) -> list[dict]` - One row per anchor with canonical/run ids, partners, distances and flags.
- **function `pool_audit`** [L100-108]: `def pool_audit(pool: Pool) -> dict` - Primary (same last symbol) and secondary (unrestricted) screens of one pool.
- **function `agreement_check`** [L111-150]: `def agreement_check(pool: Pool, primary: dict, seed: int, run_tokens: NDArray, oracle: OracleOutputs, maps_run: FutureMaps, perm: NDArray, b32_run_filter: NDArray) -> dict` - Precision reconciliation and permutation invariance for the test pool in one run.
- **function `agreement_failures`** [L153-166]: `def agreement_failures(a: dict, primary_status: str) -> list[str]` - Protocol §5/§6 agreement failures for one run's test-pool check.

