# `src/topo_pilot/experiment/x5g1t_oracle.py`

- Source: [src/topo_pilot/experiment/x5g1t_oracle.py](../../../../../../src/topo_pilot/experiment/x5g1t_oracle.py)
- Kind: python
- Lines: 31

## Module docstring

> X5 G1 training-study oracle rows (x5g1-train-v3 §4): the exact predictive for w33 from the
> public history w1..w32 only; column 33 (the target) is never read.

## Imports

### Internal (repo files)

- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../oracle/__init__.py.md) (line 11, via package root)

### External (third-party)

- `numpy` (lines 8, 9)

### Standard library

- `__future__` (lines 4)
- `collections` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/x5g1t_stages_eval.py](x5g1t_stages_eval.py.md) (line 58, import)
- [tests/experiment/test_x5g1t_lineage_oracle.py](../../../tests/experiment/test_x5g1t_lineage_oracle.py.md) (line 27, import)

## Top-level constants

- `END`

## Classes and functions

- **function `oracle_q32`** [L16-31]: `def oracle_q32(T: NDArray, E: NDArray, pi: NDArray, tokens: NDArray, guard: Callable[[str], None] | None = None, batch: int = 4096) -> NDArray` - ``BayesFilter(T, E, pi).run(tokens[:, :32]).q[:, 32]`` in batches; ``[R, V]`` float64.

