# `tools/hws/hws_worlds.py`

- Source: [tools/hws/hws_worlds.py](../../../../../tools/hws/hws_worlds.py)
- Kind: python
- Lines: 335

## Module docstring

> HWS worlds: constants, grid, keys, tiers, builders, alias map, symmetry, E1-E3 (API.md §1).

## Imports

### Internal (repo files)

- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 24, via sys.path edit)
- `from topo_pilot.contracts import SeedTree, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from topo_pilot.process import EmissionConfig, Identical, OverlapGaussian` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 28, via package root)
- `from topo_pilot.process import TransitionBuilder, TransitionConfig, Unique` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 29, via package root)
- `from topo_pilot.process._geometry import point_distances` -> [src/topo_pilot/process/_geometry.py](../../src/topo_pilot/process/_geometry.py.md) (line 30, via package root)
- `from topo_pilot.process.centers import check_centers_in_chart` -> [src/topo_pilot/process/centers.py](../../src/topo_pilot/process/centers.py.md) (line 31, via package root)
- `from topo_pilot.world import WorldConfig` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 32, via package root)
- `from topo_pilot.world import build_world` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 33, via package root)

### External (third-party)

- `numpy` (lines 23)
- `scipy` (lines 25)

### Standard library

- `__future__` (lines 7)
- `dataclasses` (lines 12)
- `fractions` (lines 13)
- `itertools` (lines 9)
- `json` (lines 10)
- `pathlib` (lines 14)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `_p` -> `tools/c1prime`, `tools/hws`, `tools/k4b`, `tools/x4_circle_history`, `tools/x4_oracle_profile`

## Imported by

- [tests/hws/test_a_budget.py](../../tests/hws/test_a_budget.py.md) (line 18, import)
- [tests/hws/test_a_classify.py](../../tests/hws/test_a_classify.py.md) (line 21, import)
- [tests/hws/test_a_identities.py](../../tests/hws/test_a_identities.py.md) (line 28, import)
- [tests/hws/test_a_outcomes.py](../../tests/hws/test_a_outcomes.py.md) (line 23, import)
- [tests/hws/test_a_stats.py](../../tests/hws/test_a_stats.py.md) (line 23, import)
- [tests/hws/test_b_exact.py](../../tests/hws/test_b_exact.py.md) (line 25, import)
- [tests/hws/test_b_kc1.py](../../tests/hws/test_b_kc1.py.md) (line 33, import)
- [tests/hws/test_b_oracle.py](../../tests/hws/test_b_oracle.py.md) (line 24, import)
- [tests/hws/test_b_records.py](../../tests/hws/test_b_records.py.md) (line 29, import)
- [tests/hws/test_b_worlds.py](../../tests/hws/test_b_worlds.py.md) (line 26, import)
- [tests/hwsb/test_b_process.py](../../tests/hwsb/test_b_process.py.md) (line 24, import)
- [tests/hwsb/test_b_streams.py](../../tests/hwsb/test_b_streams.py.md) (line 20, import)
- [tests/hwsc/test_b_records.py](../../tests/hwsc/test_b_records.py.md) (line 34, import)
- [tools/hws/hws_driver.py](hws_driver.py.md) (line 16, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 13, import)
- [tools/hws/hws_exact.py](hws_exact.py.md) (line 19, import)
- [tools/hws/hws_known.py](hws_known.py.md) (line 15, import)
- [tools/hws/hws_meter_bind.py](hws_meter_bind.py.md) (line 14, import)
- [tools/hws/hws_oracle.py](hws_oracle.py.md) (line 10, import)
- [tools/hws/hws_records.py](hws_records.py.md) (line 20, import)
- [tools/hws/hws_select.py](hws_select.py.md) (line 13, import)
- [tools/hws/hws_stats.py](hws_stats.py.md) (line 13, import)
- [tools/hwsb/hwsb_driver.py](../hwsb/hwsb_driver.py.md) (line 62, import)
- [tools/hwsb/hwsb_dry.py](../hwsb/hwsb_dry.py.md) (line 19, import)
- [tools/hwsc/hwsc_records.py](../hwsc/hwsc_records.py.md) (line 40, import)

## Top-level constants

- `CONTRACT`
- `CONTRACT_PATH`
- `DRY_STORE`
- `HERE`
- `PROTOCOL_PATH`
- `P_INDEX`
- `P_LEVELS`
- `Q_LEVELS`
- `REPO`
- `ROOT`
- `S2_P_MID`
- `S2_SIGMA_MID`
- `SIGMA_INDEX`
- `SIGMA_LEVELS`
- `STORE`
- `W0`
- `W_LEVELS`
- `X1_P`
- `X1_SIGMA`
- `_LEV`

## Classes and functions

- **function `load_contract`** [L42-43]: `def load_contract(path=CONTRACT_PATH) -> dict`
- **class `HwsStop(RuntimeError)`** [L49-55] - A technical stop with a full status string (API.md §0).
- **method `HwsStop.__init__`** [L52-55]: `def __init__(self, status: str, reason: str = '')`
- **function `world_key`** [L72-73]: `def world_key(W, q, sigma, p) -> str`
- **class `World`** [L77-93] decorators: @dataclass(frozen=True, order=False)
- **method `World.key`** [L84-85]: `def key(self) -> str` decorators: @property
- **method `World.sigma_f`** [L88-89]: `def sigma_f(self) -> float` decorators: @property
- **method `World.p_f`** [L92-93]: `def p_f(self) -> float` decorators: @property
- **function `grid`** [L99-101]: `def grid() -> list` - The 225 grid worlds of §4.4: W, then q, sigma, p ascending (choice 4).
- **function `x1_worlds`** [L104-109]: `def x1_worlds(add_p: bool, add_sigma: bool, cells) -> list`
- **function `tier`** [L112-119]: `def tier(w) -> int`
- **function `changed_factors`** [L122-123]: `def changed_factors(w) -> int`
- **function `distance`** [L126-128]: `def distance(w) -> Fraction`
- **function `cells_of`** [L131-132]: `def cells_of(worlds) -> list`
- **function `centres`** [L138-141]: `def centres(W, n_axial=N_AXIAL) -> np.ndarray` - Rectangular spacing-2 centres, row j = n_axial*i + b at (0.5 + 2i, 0.5 + 2b) (MD-5).
- **function `anchored_labels`** [L144-147]: `def anchored_labels(W, q) -> np.ndarray`
- **function `unanchored_labels`** [L150-155]: `def unanchored_labels(W, q) -> np.ndarray`
- **function `n_labels`** [L158-159]: `def n_labels(labels) -> int`
- **function `v_prime`** [L162-163]: `def v_prime(labels, n_axial=N_AXIAL) -> int`
- **function `symbol_sizes`** [L166-168]: `def symbol_sizes(labels, n_axial=N_AXIAL) -> np.ndarray`
- **function `merge_columns`** [L171-182]: `def merge_columns(E_centres, labels, n_axial=N_AXIAL) -> np.ndarray` - E'[:, n_axial*g + b] = sum over i with g(i) = g of E[:, n_axial*i + b], ascending i.
- **function `features`** [L185-187]: `def features(coords, W) -> np.ndarray`
- **function `build_world`** [L193-194]: `def build_world(W, Hh=H)`
- **function `build_transition`** [L197-198]: `def build_transition(world, p)`
- **function `_mirrored`** [L201-206]: `def _mirrored(world, cen, sigma) -> np.ndarray` - The 4-line softmax of emission._overlap_core (mirrored, not imported; §12.2 item 3).
- **function `centre_emission`** [L209-214]: `def centre_emission(world, W, sigma, n_axial=N_AXIAL) -> np.ndarray`
- **function `_base`** [L217-219]: `def _base(key, wk, t, nax, hh, sigma) -> dict`
- **function `_finish`** [L222-230]: `def _finish(base: dict, world, tr, E_centres, labels) -> dict`
- **function `_guarded`** [L233-237]: `def _guarded(base: dict, build) -> dict`
- **function `_labels`** [L240-243]: `def _labels(alias, W, q) -> np.ndarray`
- **function `build_process`** [L246-256]: `def build_process(w, alias='anchored', Hh=H, n_axial=N_AXIAL) -> dict` - §4.6 steps 1-5 in memory (no store writes); tier None for the cell (12, 3) (E13).
- **function `build_known_zero`** [L259-275]: `def build_known_zero(kind) -> dict` - U (Unique, V = 144, n_axial 12) or N (Identical, V = 36, n_axial 6) at w0 geometry.
- **function `build_tiny`** [L278-289]: `def build_tiny(sigma=Fraction(1), p=Fraction(1, 2), alias='anchored', q=1) -> dict` - DR1 tiny cylinder W = 6, H = 2, three centres (0.5 + 2i, 0.5), n_axial 1 (E13).
- **function `translate_states`** [L295-297]: `def translate_states(W, Hh, s) -> np.ndarray`
- **function `reflect_states`** [L300-302]: `def reflect_states(W, Hh, c) -> np.ndarray`
- **function `symmetry_check`** [L305-312]: `def symmetry_check(E, W, Hh=H, tol=1e-09) -> dict`
- **function `e2_check`** [L315-324]: `def e2_check(p_v, sizes, V_centres) -> dict`
- **function `exact_filters`** [L327-335]: `def exact_filters(proc, p_v) -> dict`

