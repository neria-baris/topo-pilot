# `src/topo_pilot/dataset/public.py`

- Source: [src/topo_pilot/dataset/public.py](../../../../../../src/topo_pilot/dataset/public.py)
- Kind: python
- Lines: 60

## Module docstring

> The only loader the learner may use, and the latent-field guard.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, ObservationSet, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)

### External (third-party)

- `torch` (lines 7, 8)

### Standard library

- `__future__` (lines 3)
- `dataclasses` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/dataset/__init__.py](__init__.py.md) (line 5, import)
- [src/topo_pilot/dataset/stage.py](stage.py.md) (line 32, import)

## Top-level constants

- `_PUBLIC_FIELDS`

## Classes and functions

- **function `assert_public`** [L15-34]: `def assert_public(obs: object) -> ObservationSet` - Return ``obs`` if it is a latent-free ``ObservationSet``, else raise ``LEAKAGE``.
- **class `PublicTokenDataset(Dataset)`** [L37-60] - Map-style dataset ``i -> (inputs [33], targets [33])`` of int64 tensors.
- **method `PublicTokenDataset.__init__`** [L51-54]: `def __init__(self, obs: ObservationSet, layout: SequenceLayout)`
- **method `PublicTokenDataset.__len__`** [L56-57]: `def __len__(self) -> int`
- **method `PublicTokenDataset.__getitem__`** [L59-60]: `def __getitem__(self, i: int) -> tuple[torch.Tensor, torch.Tensor]`

