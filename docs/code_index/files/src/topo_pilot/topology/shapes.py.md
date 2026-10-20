# `src/topo_pilot/topology/shapes.py`

- Source: [src/topo_pilot/topology/shapes.py](../../../../../../src/topo_pilot/topology/shapes.py)
- Kind: python
- Lines: 106

## Module docstring

> Null clouds and synthetic shapes with known topology (all randomness injected).

## Imports

### Internal (repo files)

- `from topo_pilot.contracts import ErrorCode, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 8, via package root)

### External (third-party)

- `numpy` (lines 5, 6)

### Standard library

- `__future__` (lines 3)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/topology/__init__.py](__init__.py.md) (line 7, import)

## Top-level constants

- `_COMPONENT`

## Classes and functions

- **function `_require_rng`** [L13-17]: `def _require_rng(rng: np.random.Generator | None, component: str) -> np.random.Generator`
- **class `NullClouds`** [L20-41] - Gaussian null clouds for the noise floor (RESEARCH_SUMMARY 7.3). Shapes: ``[M, F]``.
- **method `NullClouds.isotropic`** [L24-26]: `def isotropic(M: int, F: int, rng: np.random.Generator) -> NDArray[np.float64]` decorators: @staticmethod - ``M`` draws of ``N(0, I_F)``.
- **method `NullClouds.covariance_matched`** [L29-41]: `def covariance_matched(X: NDArray[np.float64], rng: np.random.Generator) -> NDArray[np.float64]` decorators: @staticmethod - ``M`` draws of ``N(mean(X), cov(X))`` (sample covariance, ddof=1), same shape as ``X``.
- **function `_embed`** [L44-52]: `def _embed(core: NDArray[np.float64], ambient: int, noise: float, rng: np.random.Generator) -> NDArray[np.float64]` - Place ``core [M, k]`` in the first ``k`` axes of R^ambient and add N(0, noise^2) per axis.
- **class `SyntheticShapes`** [L55-106] - Samples of shapes with known Betti numbers, embedded in ``R^ambient``.
- **method `SyntheticShapes.circle`** [L75-80]: `def circle(M: int, ambient: int = 128, noise: float = 0.05, rng: np.random.Generator | None = None) -> NDArray[np.float64]` decorators: @staticmethod - Uniform angles on the unit circle (beta_1 = 1).
- **method `SyntheticShapes.disk`** [L83-89]: `def disk(M: int, ambient: int = 128, noise: float = 0.05, rng: np.random.Generator | None = None) -> NDArray[np.float64]` decorators: @staticmethod - Uniform points of the unit disk (contractible).
- **method `SyntheticShapes.flat_torus`** [L92-98]: `def flat_torus(M: int, ambient: int = 128, noise: float = 0.05, rng: np.random.Generator | None = None) -> NDArray[np.float64]` decorators: @staticmethod - Uniform angles on the Clifford torus in R^4 (beta_1 = 2).
- **method `SyntheticShapes.sphere`** [L101-106]: `def sphere(M: int, dim: int = 2, ambient: int = 128, noise: float = 0.05, rng: np.random.Generator | None = None) -> NDArray[np.float64]` decorators: @staticmethod - Uniform points of the unit sphere ``S^dim`` in R^(dim+1).

