# `src/topo_pilot/prediction/metrics.py`

- Source: [src/topo_pilot/prediction/metrics.py](../../../../../../src/topo_pilot/prediction/metrics.py)
- Kind: python
- Lines: 138

## Module docstring

> Predictive metrics, learning gate, and join helper (part b). Pure numpy.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, GateCheck, StageFailure, Status` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 10, via package root)

### External (third-party)

- `numpy` (lines 7, 8)

### Standard library

- `__future__` (lines 3)
- `math` (lines 5)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/prediction/__init__.py](__init__.py.md) (line 3, import)
- [tests/hwsb/test_a_learning.py](../../../tests/hwsb/test_a_learning.py.md) (line 32, import)
- [tools/hwsb/hwsb_eval.py](../../../tools/hwsb/hwsb_eval.py.md) (line 23, import)
- [tools/hwsb/hwsb_kb.py](../../../tools/hwsb/hwsb_kb.py.md) (line 23, import)

## Top-level constants

- `_COMPONENT`
- `_G_C_FLOOR`
- `_NORM_TOL`

## Classes and functions

- **function `_fail`** [L17-18]: `def _fail(code: ErrorCode, check: str, detail: str, comp: str = _COMPONENT) -> StageFailure`
- **function `_check_dist`** [L21-28]: `def _check_dist(name: str, arr: np.ndarray) -> NDArray[np.float64]`
- **class `PredictiveMetrics`** [L31-96] - Pure functions on aligned arrays; all quantities in nats.
- **method `PredictiveMetrics.nll`** [L45-52]: `def nll(probs: np.ndarray, targets: np.ndarray) -> np.ndarray` decorators: @staticmethod - Per-row ``-log probs[i, targets[i]]`` -> ``[M]`` (``inf`` if the probability is 0).
- **method `PredictiveMetrics.kl`** [L55-64]: `def kl(p: np.ndarray, q: np.ndarray) -> np.ndarray` decorators: @staticmethod - Rowwise ``KL(p||q) = sum_i p_i log(p_i/q_i)`` with ``0 log 0 = 0``; ``[M, V] -> [M]``.
- **method `PredictiveMetrics.regret`** [L67-69]: `def regret(q_oracle: np.ndarray, p_model: np.ndarray) -> float` decorators: @staticmethod - Mean ``KL(q_C || p_model)`` over rows (exact, not a difference of sampled NLLs).
- **method `PredictiveMetrics.captured`** [L72-76]: `def captured(regret: float, G_C: float) -> float` decorators: @staticmethod - ``1 - regret / G_C``; ``nan`` when ``G_C <= 1e-6`` (the gate maps it to INCONCLUSIVE).
- **method `PredictiveMetrics.bootstrap_ci`** [L79-96]: `def bootstrap_ci(values: np.ndarray, groups: np.ndarray, n: int, rng: np.random.Generator) -> tuple[float, float]` decorators: @staticmethod - 2.5/97.5 percentile CI of the mean from ``n`` resamples of whole groups.
- **class `LearningGate`** [L99-119] - Gate ``captured >= threshold`` (RESEARCH_SUMMARY §6).
- **method `LearningGate.__init__`** [L107-108]: `def __init__(self, threshold: float = 0.8) -> None`
- **method `LearningGate.evaluate_with_status`** [L110-115]: `def evaluate_with_status(self, captured: float) -> tuple[GateCheck, Status]` - Return ``(GateCheck, Status)`` for a captured fraction.
- **method `LearningGate.evaluate`** [L117-119]: `def evaluate(self, captured: float) -> GateCheck` - Return the ``GateCheck`` only (see :meth:`evaluate_with_status`).
- **function `join_by_history_id`** [L122-138]: `def join_by_history_id(ids_a: np.ndarray, ids_b: np.ndarray) -> np.ndarray` - One-to-one join: returns ``idx`` with ``ids_b[idx[i]] == ids_a[i]``.

