# `tests/x6_stage0/test_x6_stage0.py`

- Source: [tests/x6_stage0/test_x6_stage0.py](../../../../../tests/x6_stage0/test_x6_stage0.py)
- Kind: python
- Lines: 400

## Module docstring

> X6 stage 0 independent tests (X6-FROZEN-v1 section 10.4: tests 1-5, 9, 13, 14), written from
> the protocol and API.md only; references use the protocol's formulas (Fractions, ints, Decimal),
> never a module kernel. test_x6_stage0_dp.py reuses the helpers below.

## Imports

### Internal (repo files)

- `import x6_exact` -> [tools/x6_stage0/x6_exact.py](../../tools/x6_stage0/x6_exact.py.md) (line 23, via sys.path edit)
- `import x6_model` -> [tools/x6_stage0/x6_model.py](../../tools/x6_stage0/x6_model.py.md) (line 24, via sys.path edit)
- `from topo_pilot.world import CubicalComplex` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 25, via package root)
- `import topo_pilot.process._geometry` -> [src/topo_pilot/process/_geometry.py](../../src/topo_pilot/process/_geometry.py.md) (line 375, via package root) (inside a function)
- `import topo_pilot.process.emission` -> [src/topo_pilot/process/emission.py](../../src/topo_pilot/process/emission.py.md) (line 376, via package root) (inside a function)
- `from topo_pilot.world import WORLD_REGISTRY, QuotientLatticeBuilder` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 377, via package root) (inside a function)

### External (third-party)

- `numpy` (lines 14)
- `pytest` (lines 15)

### Standard library

- `__future__` (lines 5)
- `collections` (lines 9)
- `decimal` (lines 10)
- `fractions` (lines 11)
- `itertools` (lines 7)
- `pathlib` (lines 12)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 21: `str(_p)` -> `tests/oracle_profile`, `tools/x4_oracle_profile`, `tools/x6_stage0`

## Imported by

- [tests/x6_stage0/test_x6_stage0_dp.py](test_x6_stage0_dp.py.md) (line 21, import)

## Top-level constants

- `ARMS`
- `FACETS`
- `GAUGE`
- `H_COV`
- `H_FIX`
- `LOOPS`
- `NAME`
- `ORDS`
- `REPO`
- `S3`
- `SEAM`
- `SEAM_ARMS`
- `TOOLS`

## Classes and functions

- **function `comp`** [L43-44]: `def comp(g, h)`
- **function `inv`** [L46-47]: `def inv(g)`
- **function `nbrs`** [L49-52]: `def nbrs(i)`
- **function `letter`** [L54-60]: `def letter(i, j)`
- **function `labels`** [L62-68]: `def labels(arm)`
- **function `tok`** [L70-71]: `def tok(i)`
- **function `lam`** [L73-74]: `def lam(m, eta=ETA)`
- **function `mu`** [L76-77]: `def mu(m, z, eta=ETA)`
- **function `hol`** [L79-83]: `def hol(path, lab)`
- **function `lift`** [L85-90]: `def lift(arm)`
- **function `emis`** [L92-99]: `def emis(kind='E')`
- **function `filt`** [L101-113]: `def filt(T, E, toks)` - Exact forward filter (emit, then transition; pi = 1/48): ([q_0..q_t], P, [b_1..b_t]).
- **function `w_path`** [L115-121]: `def w_path(fam, mem)`
- **function `w_tokens`** [L123-124]: `def w_tokens(fam, mem, y)`
- **function `dec`** [L126-129]: `def dec(fr, prec=90)`
- **function `dkl`** [L131-135]: `def dkl(p, q, prec=80)`
- **function `dent`** [L137-140]: `def dent(p)`
- **function `spec`** [L144-145]: `def spec()` decorators: @pytest.fixture(scope='module')
- **test `test_01_literal_conventions`** [L148-173]: `def test_01_literal_conventions()`
- **function `cover_cells`** [L176-183]: `def cover_cells(spec, lab)`
- **function `edge_use`** [L185-186]: `def edge_use(squares)`
- **function `boundary_components`** [L188-196]: `def boundary_components(c1, c2)`
- **test `test_02_kernel_lift_complexes_covers`** [L199-246]: `def test_02_kernel_lift_complexes_covers(spec)`
- **test `test_03_faces_flux_fstar`** [L249-275]: `def test_03_faces_flux_fstar(spec)`
- **test `test_04_witness_path_sums`** [L278-319]: `def test_04_witness_path_sums()`
- **test `test_05_kgram_locality`** [L322-341]: `def test_05_kgram_locality()`
- **test `test_09_block_comparator`** [L344-371]: `def test_09_block_comparator()`
- **test `test_13_registry_and_geometry_guards`** [L374-392]: `def test_13_registry_and_geometry_guards(monkeypatch)`
- **test `test_14_file_line_limits`** [L395-400]: `def test_14_file_line_limits()`

