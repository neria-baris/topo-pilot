# `tests/c2_nd/test_b_registry.py`

- Source: [tests/c2_nd/test_b_registry.py](../../../../../tests/c2_nd/test_b_registry.py)
- Kind: python
- Lines: 394

## Module docstring

> Author B, T-REG-ND (protocol §6.2-§6.5; API.md §5; rulings R-0116-3, R-0116-4).

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](../../tools/c2_nd/nd_config.py.md) (line 20, via sys.path edit)
- `import c1_data` -> [tools/c1prime/c1_data.py](../../tools/c1prime/c1_data.py.md) (line 23, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../../tools/c2_readout/c2_data.py.md) (line 24, via unique basename)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../../tools/c2_readout/c2_registry.py.md) (line 25, via unique basename)
- `import k4b_registry` -> [tools/k4b/k4b_registry.py](../../tools/k4b/k4b_registry.py.md) (line 26, via unique basename)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](../../tools/c2_nd/nd_registry.py.md) (line 27, via sys.path edit)

### External (third-party)

- `numpy` (lines 28)
- `pytest` (lines 29)

### Standard library

- `__future__` (lines 9)
- `hashlib` (lines 11)
- `json` (lines 12)
- `pathlib` (lines 14)
- `sys` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 18: `str(REPO / 'tools' / 'c2_nd')` -> `tools/c2_nd`

## Imported by

- none

## Top-level constants

- `REPO`

## Classes and functions

- **function `sha`** [L35-36]: `def sha(path)`
- **function `table`** [L39-43]: `def table(seed, n=8)`
- **function `save`** [L46-50]: `def save(path, **arrays)`
- **function `garbage`** [L53-55]: `def garbage(path)`
- **function `tokens`** [L58-59]: `def tokens(seed, n=4)`
- **function `row_hex`** [L62-63]: `def row_hex(tok)`
- **function `loads`** [L67-76]: `def loads(monkeypatch)` decorators: @pytest.fixture - Every np.load path (a registry reader must never np.load a payload or sealed file).
- **function `scratch`** [L80-83]: `def scratch(tmp_path_factory, monkeypatch)` decorators: @pytest.fixture
- **function `expected_roots`** [L87-96]: `def expected_roots()` decorators: @pytest.fixture - Replace CONTRACT scratch_roots_expected in place (restored afterwards).
- **function `c2_store`** [L100-106]: `def c2_store(tmp_path, monkeypatch)` decorators: @pytest.fixture
- **function `union`** [L109-113]: `def union(tabs)`
- **test `test_source_c2`** [L117-125]: `def test_source_c2(c2_store)`
- **test `test_source_c2_missing_and_mismatch`** [L128-134]: `def test_source_c2_missing_and_mismatch(c2_store)`
- **test `test_planted_collision_with_a_c2_test_table`** [L137-150]: `def test_planted_collision_with_a_c2_test_table(c2_store)`
- **test `test_source_c2_superseded`** [L154-164]: `def test_source_c2_superseded(tmp_path, loads)`
- **test `test_source_scratch`** [L168-182]: `def test_source_scratch(scratch, expected_roots, loads)`
- **test `test_source_scratch_skips_test_trees`** [L188-198]: `def test_source_scratch_skips_test_trees(scratch, expected_roots, loads)`
- **test `test_source_scratch_expected_roots`** [L201-211]: `def test_source_scratch_expected_roots(scratch, expected_roots)`
- **function `frozen`** [L215-218]: `def frozen(store)`
- **test `test_parallel_absent_and_unfrozen`** [L221-230]: `def test_parallel_absent_and_unfrozen(tmp_path, scratch)`
- **test `test_parallel_hws_reader`** [L233-243]: `def test_parallel_hws_reader(tmp_path, scratch)`
- **test `test_parallel_hws_dry_scratch`** [L248-257]: `def test_parallel_hws_dry_scratch(tmp_path, scratch)` - R-0116-3: reader hws also reads <SCRATCH_ROOT>/hws-dry/hist/** when present.
- **test `test_parallel_hws_non_32_wide_is_non_c2_format`** [L262-279]: `def test_parallel_hws_non_32_wide_is_non_c2_format(tmp_path, scratch)` - D-0139-1 regression: a uint8 [n, 8] token array (the HWS null-check fixtures) is listed
- **test `test_parallel_payload_or_sealed_is_never_opened`** [L283-288]: `def test_parallel_payload_or_sealed_is_never_opened(tmp_path, scratch, loads, where)` decorators: @pytest.mark.parametrize('where', ('run/payload.npz', 'sealed/k9.npz'))
- **test `test_parallel_x6zc_layout`** [L293-302]: `def test_parallel_x6zc_layout(tmp_path, scratch, loads)`
- **function `names`** [L306-307]: `def names(res)`
- **test `test_inventory_adapter`** [L310-321]: `def test_inventory_adapter(tmp_path)`
- **test `test_build_writes_a_c2_format_manifest`** [L328-360]: `def test_build_writes_a_c2_format_manifest(tmp_path, monkeypatch)`
- **function `reservation`** [L363-379]: `def reservation(tmp_path, monkeypatch, **change)`
- **test `test_reservation_check`** [L382-394]: `def test_reservation_check(tmp_path, monkeypatch)`

