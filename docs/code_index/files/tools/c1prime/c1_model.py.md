# `tools/c1prime/c1_model.py`

- Source: [tools/c1prime/c1_model.py](../../../../../tools/c1prime/c1_model.py)
- Kind: python
- Lines: 97

## Module docstring

> C1' float64 model evaluation: exact float64 cast of the frozen float32 weights, activations
> at resid_post_3/32, patched and tail-path logits, identity checks (API.md §8; protocol §5.1,
> §5.4, §15.1). Logits of activation forwards are discarded unread (computation-order rule).

## Imports

### Internal (repo files)

- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 9, via same directory)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 12, via same directory)
- `from topo_pilot.learner import forward_with_patch` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 14, via package root)
- `from topo_pilot.learner.stage import load_model` -> [src/topo_pilot/learner/stage.py](../../src/topo_pilot/learner/stage.py.md) (line 15, via package root)

### External (third-party)

- `numpy` (lines 10)
- `torch` (lines 11)

### Standard library

- `__future__` (lines 5)
- `hashlib` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsb/test_b_e4path.py](../../tests/hwsb/test_b_e4path.py.md) (line 27, import)
- [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 15, import)
- [tools/c1prime/c1_driver_late.py](c1_driver_late.py.md) (line 18, import)
- [tools/c2_nd/nd_decoy.py](../c2_nd/nd_decoy.py.md) (line 21, import)
- [tools/c2_nd/nd_stage_base.py](../c2_nd/nd_stage_base.py.md) (line 20, import)
- [tools/c2_readout/c2_model.py](../c2_readout/c2_model.py.md) (line 18, import)
- [tools/c2_readout/c2_stage_base.py](../c2_readout/c2_stage_base.py.md) (line 19, import)
- [tools/hwsb/hwsb_data.py](../hwsb/hwsb_data.py.md) (line 15, import)
- [tools/hwsb/hwsb_eval.py](../hwsb/hwsb_eval.py.md) (line 14, import)
- [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 100, import)
- [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 170, import)
- [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 274, import)
- [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 347, import)

## Top-level constants

- none

## Classes and functions

- **function `state_sha`** [L20-25]: `def state_sha(model) -> str`
- **function `load_model64`** [L28-38]: `def load_model64(checkpoint) -> tuple`
- **function `model_inputs`** [L41-44]: `def model_inputs(named32) -> torch.Tensor`
- **function `_batches`** [L47-49]: `def _batches(n, batch)`
- **function `activations`** [L52-59]: `def activations(model64, inputs, batch=1024) -> np.ndarray`
- **function `patched_logits`** [L62-69]: `def patched_logits(model64, inputs, a, batch=1024) -> np.ndarray`
- **function `natural_logits`** [L72-77]: `def natural_logits(model64, inputs, batch=1024) -> np.ndarray`
- **function `tail_logits`** [L80-83]: `def tail_logits(model64, a) -> np.ndarray`
- **function `identity_patch_ok`** [L86-87]: `def identity_patch_ok(model64, inputs, a) -> bool`
- **function `_log_softmax`** [L90-91]: `def _log_softmax(z) -> np.ndarray`
- **function `tail_identity`** [L94-97]: `def tail_identity(model64, inputs, a_forced) -> float`

