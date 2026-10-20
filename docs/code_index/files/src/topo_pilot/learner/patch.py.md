# `src/topo_pilot/learner/patch.py`

- Source: [src/topo_pilot/learner/patch.py](../../../../../../src/topo_pilot/learner/patch.py)
- Kind: python
- Lines: 118

## Module docstring

> Frozen forward pass with one replaced vector (X4-F, x4f-exec-v2 §7; no science imports).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 14, via package root)
- `from .model import TransformerLM` -> [src/topo_pilot/learner/model.py](model.py.md) (line 16, via relative)

### External (third-party)

- `torch` (lines 12)

### Standard library

- `__future__` (lines 7)
- `collections` (lines 9)
- `dataclasses` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/learner/__init__.py](__init__.py.md) (line 5, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **class `PatchedOutput`** [L22-27] decorators: @dataclass(frozen=True) - ``logits [R, L, vocab_out]`` at every position and the requested ``hooks`` (each
- **function `_fail`** [L30-31]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **function `_check`** [L34-63]: `def _check(model: TransformerLM, inputs: torch.Tensor, site: str, index: int, replacement: torch.Tensor, return_hooks: Sequence[str]) -> int | None` - Validate arguments; return the block index k for ``resid_post_k`` (None for final LN).
- **function `forward_with_patch`** [L66-118]: `def forward_with_patch(model: TransformerLM, inputs: torch.Tensor, site: str, index: int, replacement: torch.Tensor, *, return_hooks: Sequence[str] = ()) -> PatchedOutput` - Run the frozen model with the vector at ``(site, index)`` replaced.

