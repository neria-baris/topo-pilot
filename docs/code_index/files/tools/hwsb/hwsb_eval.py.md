# `tools/hwsb/hwsb_eval.py`

- Source: [tools/hwsb/hwsb_eval.py](../../../../../tools/hwsb/hwsb_eval.py)
- Kind: python
- Lines: 173

## Module docstring

> HWSB evaluation: logits, B1-B3, activations, oracle moments, X+- and support (API.md §4).

## Imports

### Internal (repo files)

- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](hwsb_config.py.md) (line 10, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 13, via unique basename)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 14, via unique basename)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](../hws/hws_oracle.py.md) (line 15, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 16, via unique basename)
- `from hwsb_data import model_inputs` -> [tools/hwsb/hwsb_data.py](hwsb_data.py.md) (line 19, via same directory)
- `from topo_pilot.contracts import Status` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 21, via package root)
- `from topo_pilot.learner.stage import load_model` -> [src/topo_pilot/learner/stage.py](../../src/topo_pilot/learner/stage.py.md) (line 22, via package root)
- `from topo_pilot.prediction.metrics import LearningGate, PredictiveMetrics` -> [src/topo_pilot/prediction/metrics.py](../../src/topo_pilot/prediction/metrics.py.md) (line 23, via package root)

### External (third-party)

- `numpy` (lines 17)
- `torch` (lines 18)

### Standard library

- `__future__` (lines 8)
- `math` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsb/test_a_endpoints.py](../../tests/hwsb/test_a_endpoints.py.md) (line 34, import)
- [tests/hwsb/test_a_learning.py](../../tests/hwsb/test_a_learning.py.md) (line 36, import)
- [tests/hwsb/test_b_e4path.py](../../tests/hwsb/test_b_e4path.py.md) (line 25, import)
- [tests/hwsc/test_a_learning.py](../../tests/hwsc/test_a_learning.py.md) (line 27, import)
- [tools/hwsb/hwsb_dry.py](hwsb_dry.py.md) (line 22, import)
- [tools/hwsb/hwsb_dry2.py](hwsb_dry2.py.md) (line 17, import)
- [tools/hwsb/hwsb_kb.py](hwsb_kb.py.md) (line 14, import)
- [tools/hwsb/hwsb_stages.py](hwsb_stages.py.md) (line 16, import)
- [tools/hwsc/hwsc_dry2.py](../hwsc/hwsc_dry2.py.md) (line 11, import)
- [tools/hwsc/hwsc_gates.py](../hwsc/hwsc_gates.py.md) (line 14, import)

## Top-level constants

- `NUMERICAL`

## Classes and functions

- **function `_mean`** [L28-29]: `def _mean(x) -> float`
- **function `load_float32`** [L32-33]: `def load_float32(checkpoint)`
- **function `logits32`** [L36-44]: `def logits32(model, inputs, batch=256) -> np.ndarray` - ActivationExtractor's logits path: plain forward, position 32, float32.
- **function `softmax64`** [L47-51]: `def softmax64(logits) -> np.ndarray`
- **function `to_canonical`** [L54-55]: `def to_canonical(p_named, perm) -> np.ndarray`
- **function `check_rows`** [L58-67]: `def check_rows(p, tol=1e-06) -> np.ndarray`
- **function `model_predictive`** [L70-72]: `def model_predictive(checkpoint, canon32, perm, batch=256) -> np.ndarray`
- **function `oracle_predictives`** [L75-79]: `def oracle_predictives(proc, canon32, Ks=(1, 4)) -> dict`
- **function `_sd_se`** [L82-85]: `def _sd_se(x) -> tuple`
- **function `b1`** [L88-105]: `def b1(q, p) -> dict`
- **function `forcing`** [L108-123]: `def forcing(q_full, q_base, p, z=hc.Z_B23) -> dict`
- **function `b2`** [L126-127]: `def b2(q, p) -> dict`
- **function `b3`** [L130-134]: `def b3(q, p, n_axial=6) -> dict`
- **function `load64`** [L137-138]: `def load64(checkpoint) -> tuple`
- **function `activations`** [L141-150]: `def activations(model64, inputs, site=hc.SITE, index=hc.INDEX, batch=1024) -> np.ndarray`
- **function `moments`** [L153-156]: `def moments(proc, canon32) -> dict`
- **function `d4_rows`** [L159-160]: `def d4_rows(m) -> np.ndarray`
- **function `endpoints`** [L163-169]: `def endpoints(ext, m) -> dict`
- **function `support`** [L172-173]: `def support(ext, R, a, m) -> dict`

