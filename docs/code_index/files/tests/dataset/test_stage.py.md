# `tests/dataset/test_stage.py`

- Source: [tests/dataset/test_stage.py](../../../../../tests/dataset/test_stage.py)
- Kind: python
- Lines: 124

## Module docstring

(none)

## Imports

### Internal (repo files)

- `from topo_pilot import contracts` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 4, via package root)
- `from topo_pilot.dataset import DatasetConfig, DatasetStage, HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 5, via package root)
- `from topo_pilot.dataset.checks import check_disjoint, check_first_token, check_ranges, make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 6, via package root)

### External (third-party)

- `numpy` (lines 1)
- `pytest` (lines 2)

### Standard library

- none

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- none

## Top-level constants

- none

## Classes and functions

- **function `_run`** [L17-19]: `def _run(process, cfg, master=1, eid=None)`
- **function `_load`** [L22-23]: `def _load(store, cls, aid)`
- **test `test_D04_disjoint_ids_test_shared_across_replicates_train_differs`** [L26-43]: `def test_D04_disjoint_ids_test_shared_across_replicates_train_differs(process, tiny_cfg)`
- **test `test_symbol_renaming_keeps_test_latents_and_relabels_tokens`** [L46-56]: `def test_symbol_renaming_keeps_test_latents_and_relabels_tokens(process, tiny_cfg, add_emission)`
- **test `test_stage_saves_expected_lineage_and_split_labels`** [L59-67]: `def test_stage_saves_expected_lineage_and_split_labels(process, tiny_cfg)`
- **test `test_D08_no_train_sidecar_persisted`** [L70-77]: `def test_D08_no_train_sidecar_persisted(process, tiny_cfg)`
- **test `test_D09_biased_sampler_caught_by_first_token_chi2`** [L80-88]: `def test_D09_biased_sampler_caught_by_first_token_chi2(process, tiny_cfg, monkeypatch)`
- **test `test_chi2_skipped_below_200_and_passes_on_exact_counts`** [L91-95]: `def test_chi2_skipped_below_200_and_passes_on_exact_counts()`
- **test `test_n_test_smaller_than_panels_is_alignment_error`** [L98-102]: `def test_n_test_smaller_than_panels_is_alignment_error(process)`
- **test `test_split_overlap_and_range_errors`** [L105-114]: `def test_split_overlap_and_range_errors()`
- **test `test_sequence_id_rule_known_answer`** [L117-124]: `def test_sequence_id_rule_known_answer()`

