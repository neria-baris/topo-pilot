# `src/topo_pilot/prediction/ngram.py`

- Source: [src/topo_pilot/prediction/ngram.py](../../../../../../src/topo_pilot/prediction/ngram.py)
- Kind: python
- Lines: 133

## Module docstring

> n-gram baselines (part a): additive and interpolated Kneser-Ney smoothing.

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, ObservationSet, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 11, via package root)

### External (third-party)

- `numpy` (lines 8, 9)

### Standard library

- `__future__` (lines 3)
- `collections` (lines 5)
- `typing` (lines 6)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/prediction/__init__.py](__init__.py.md) (line 4, import)
- [src/topo_pilot/prediction/stage.py](stage.py.md) (line 19, import)

## Top-level constants

- `_COMPONENT`
- `_DEFAULT_ALPHA`

## Classes and functions

- **function `_fail`** [L17-18]: `def _fail(code: ErrorCode, check: str, detail: str) -> StageFailure`
- **class `NGramBaseline`** [L21-133] - Order-1 (unigram) or order-2 (bigram) next-token model fitted on train tokens only.
- **method `NGramBaseline.__init__`** [L52-63]: `def __init__(self, order: int, smoothing: Literal['additive', 'kneser_ney'], alpha: float | None = None) -> None`
- **method `NGramBaseline._check_alpha`** [L66-69]: `def _check_alpha(alpha: float) -> float` decorators: @staticmethod
- **method `NGramBaseline.fit`** [L71-79]: `def fit(self, train: ObservationSet) -> NGramBaseline` - Count unigrams (all positions) and within-sequence bigrams on ``train``.
- **method `NGramBaseline._require_fit`** [L81-84]: `def _require_fit(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]`
- **method `NGramBaseline._unigram_probs`** [L86-87]: `def _unigram_probs(self, uni: NDArray[np.float64], alpha: float) -> NDArray[np.float64]`
- **method `NGramBaseline._context_table`** [L89-104]: `def _context_table(self, alpha: float) -> NDArray[np.float64]` - Return ``[V, V]`` table ``P[c, w]`` for order 2 (one row per possible context).
- **method `NGramBaseline.predict`** [L106-115]: `def predict(self, histories: np.ndarray) -> np.ndarray` - Map histories ``[M, p]`` of token ids to next-token distributions ``[M, V]``.
- **method `NGramBaseline.select_smoothing`** [L117-133]: `def select_smoothing(self, dev: ObservationSet, grid: Sequence[float]) -> float` - Pick alpha minimising dev CE of ``w_33`` given ``w_1..w_32`` (D-021).

