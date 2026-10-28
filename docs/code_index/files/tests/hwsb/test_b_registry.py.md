# `tests/hwsb/test_b_registry.py`

- Source: [tests/hwsb/test_b_registry.py](../../../../../tests/hwsb/test_b_registry.py)
- Kind: python
- Lines: 237

## Module docstring

> Author B (job 0161), TEST_PLAN section 3 `test_b_registry.py`: B9a(i)/(ii) (history inventory
> and the fail-closed registry reader, section 6.3; DRB13) and B9a(iii)/(iv) (the registry cap and
> the sealed-alphabet predicate). A synthetic stage-B store under pytest tmp_path with the tiny
> world; ObservationSets of two dry masters plus three hist blocks. tools/hwsb/*.py unread.

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../../tools/hwsb/hwsb_config.py.md) (line 22, via sys.path edit)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../../tools/hwsb/hwsb_data.py.md) (line 23, via sys.path edit)
- `import hwsb_dry` -> [tools/hwsb/hwsb_dry.py](../../tools/hwsb/hwsb_dry.py.md) (line 24, via sys.path edit)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](../../tools/hwsb/hwsb_gates.py.md) (line 25, via sys.path edit)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../../tools/k4b/k4b_data.py.md) (line 26, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../../tools/x4_circle_history/scores.py.md) (line 27, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, ObservationSet` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 15)
- `pytest` (lines 16)

### Standard library

- `__future__` (lines 6)
- `dataclasses` (lines 8)
- `fractions` (lines 12)
- `hashlib` (lines 9)
- `pathlib` (lines 13)
- `shutil` (lines 10)
- `sys` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(REPO / 'tools' / 'hwsb')` -> `tools/hwsb`

## Imported by

- none

## Top-level constants

- `REG`
- `REPO`
- `ROLES`

## Classes and functions

- **function `plan`** [L34-37]: `def plan()`
- **function `base`** [L41-62]: `def base(tmp_path_factory)` decorators: @pytest.fixture(scope='module')
- **function `copy`** [L66-69]: `def copy(base, tmp_path)` decorators: @pytest.fixture
- **function `walk`** [L72-78]: `def walk(root)`
- **test `test_history_inventory_lists_every_file_with_sha256`** [L82-87]: `def test_history_inventory_lists_every_file_with_sha256(base)`
- **test `test_inventory_includes_superseded_tree`** [L90-94]: `def test_inventory_includes_superseded_tree(copy)`
- **test `test_registry_digests_pass_and_match_history_digests`** [L98-107]: `def test_registry_digests_pass_and_match_history_digests(base)`
- **test `test_registry_digests_without_expected_also_pass`** [L110-112]: `def test_registry_digests_without_expected_also_pass(base)`
- **test `test_named_tokens_are_inverted_to_canonical`** [L115-123]: `def test_named_tokens_are_inverted_to_canonical(base)`
- **test `test_superseded_hist_is_read`** [L126-133]: `def test_superseded_hist_is_read(copy)`
- **test `test_missing_file_fails_closed`** [L137-141]: `def test_missing_file_fails_closed(copy)`
- **test `test_renamed_hist_file_fails_closed`** [L144-148]: `def test_renamed_hist_file_fails_closed(copy)`
- **test `test_extra_unlisted_file_fails_closed`** [L151-156]: `def test_extra_unlisted_file_fails_closed(copy)`
- **test `test_unreadable_npz_fails_closed`** [L159-162]: `def test_unreadable_npz_fails_closed(copy)`
- **test `test_changed_byte_fails_closed`** [L165-170]: `def test_changed_byte_fails_closed(copy)`
- **test `test_observation_set_without_emission_parent_fails_closed`** [L173-177]: `def test_observation_set_without_emission_parent_fails_closed(copy)`
- **function `largest_passing_p`** [L181-188]: `def largest_passing_p(rows)`
- **function `eval_blocks`** [L191-198]: `def eval_blocks()`
- **test `test_b9a_registry_cap_boundary_is_exact`** [L201-211]: `def test_b9a_registry_cap_boundary_is_exact(base)`
- **test `test_b9a_uses_12288_style_row_count_and_reference_tolerance`** [L214-221]: `def test_b9a_uses_12288_style_row_count_and_reference_tolerance(base)`
- **test `test_b9a_registry_failure_gives_registry_status`** [L224-227]: `def test_b9a_registry_failure_gives_registry_status(copy)`
- **test `test_predicate_hits_count_planted_alphabet_rows`** [L230-237]: `def test_predicate_hits_count_planted_alphabet_rows(base)`

