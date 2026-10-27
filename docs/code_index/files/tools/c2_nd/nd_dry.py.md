# `tools/c2_nd/nd_dry.py`

- Source: [tools/c2_nd/nd_dry.py](../../../../../tools/c2_nd/nd_dry.py)
- Kind: python
- Lines: 336

## Module docstring

> C2ND synthetic dry run (API.md §11; C2ND-DESIGN-v1 §10.1): planted models (random-initialised
> TransformerLMs with the trained architecture whose head reads a planted 6-d harmonic code of a
> synthetic phase with share 0.85), the synthetic C2-prerequisite fixture (the c2/ stand-in of the
> C2 store: FIT projectors, decoders, N2 fit, frozen oracle constants, made by the C2 kernels on
> synthetic activations of cylinder-O histories from a dry-only stream), the synthetic phase, the
> broken decoys of pass criterion 3 (the J-built decoy fails; the Euclidean one is reported,
> E-C2ND-2) and the forbidden-access and planted-collision checks. Every function refuses with
> FAIL_TECHNICAL/AUTHORITY outside a dry-run store (G0 (x)); no trained weight, no C2 store file
> and no c2nd-v1 stream is touched.

## Imports

### Internal (repo files)

- `import nd_config` -> [tools/c2_nd/nd_config.py](nd_config.py.md) (line 15, via same directory)
- `import c1_data` -> [tools/c1prime/c1_data.py](../c1prime/c1_data.py.md) (line 18, via unique basename)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](../c1prime/c1_oracle.py.md) (line 19, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../c2_readout/c2_attrib.py.md) (line 20, via unique basename)
- `import c2_code` -> [tools/c2_readout/c2_code.py](../c2_readout/c2_code.py.md) (line 21, via unique basename)
- `import c2_config` -> [tools/c2_readout/c2_config.py](../c2_readout/c2_config.py.md) (line 22, via unique basename)
- `import c2_data` -> [tools/c2_readout/c2_data.py](../c2_readout/c2_data.py.md) (line 23, via unique basename)
- `import c2_model` -> [tools/c2_readout/c2_model.py](../c2_readout/c2_model.py.md) (line 24, via unique basename)
- `import c2_oracle` -> [tools/c2_readout/c2_oracle.py](../c2_readout/c2_oracle.py.md) (line 25, via unique basename)
- `import c2_stats` -> [tools/c2_readout/c2_stats.py](../c2_readout/c2_stats.py.md) (line 26, via unique basename)
- `import nd_attrib` -> [tools/c2_nd/nd_attrib.py](nd_attrib.py.md) (line 27, via same directory)
- `import nd_decoy` -> [tools/c2_nd/nd_decoy.py](nd_decoy.py.md) (line 28, via same directory)
- `import nd_driver` -> [tools/c2_nd/nd_driver.py](nd_driver.py.md) (line 29, via same directory)
- `import nd_registry` -> [tools/c2_nd/nd_registry.py](nd_registry.py.md) (line 30, via same directory)
- `import nd_stage_base` -> [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 31, via same directory)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 34, via unique basename)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 36, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 37, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 38, via package root)
- `from topo_pilot.learner.config import ModelConfig` -> [src/topo_pilot/learner/config.py](../../src/topo_pilot/learner/config.py.md) (line 39, via package root)
- `from topo_pilot.learner.model import TransformerLM` -> [src/topo_pilot/learner/model.py](../../src/topo_pilot/learner/model.py.md) (line 40, via package root)

### External (third-party)

- `numpy` (lines 32)
- `torch` (lines 33)

### Standard library

- `__future__` (lines 11)
- `pathlib` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/c2_nd/test_impl_dry_hs.py](../../tests/c2_nd/test_impl_dry_hs.py.md) (line 33, import)
- [tools/c2_nd/nd_driver.py](nd_driver.py.md) (line 356, dynamic)
- [tools/c2_nd/nd_stage_base.py](nd_stage_base.py.md) (line 286, dynamic)

## Top-level constants

- `CFG`
- `ROLES3`

## Classes and functions

- **function `guard`** [L47-49]: `def guard(ctx) -> None`
- **function `_model`** [L53-58]: `def _model(state=None, seed=0) -> TransformerLM`
- **function `planted_models`** [L61-68]: `def planted_models(ctx) -> dict` - {j: (model64, sha256 of its c2/models file)}, the file re-hashed against c2/TABLE.json.
- **function `synthetic_phase`** [L71-77]: `def synthetic_phase(ctx, j, a3) -> tuple` - phi = atan2 of (resid_post_3 - mu) @ U.T, the belief chart of the stand-in fit (_chart);
- **function `_chart`** [L80-91]: `def _chart(acts, o, Ex) -> dict` - The belief chart (D-0158-1, ND-C59): mu, the mean of resid_post_3, and U, the 2 x d_model
- **function `_sample`** [L95-103]: `def _sample(P, b) -> tuple` - One 4,096-row block of the dry-only stream (scope c2nd-dry-v1, split c2prereq).
- **function `_write`** [L106-108]: `def _write(ctx, rel, arrays=None, obj=None) -> None`
- **function `_plant`** [L111-126]: `def _plant(m64, y, d, dy, Ex, G, logq, P_S) -> dict` - The head: least squares of the oracle's named log-predictive on y, split into the code
- **function `prepare`** [L129-228]: `def prepare(ctx) -> dict` - PREP: the c2/ stand-in subtree, c2/TABLE.json and the PREP manifest (accepted by the
- **function `broken_decoys`** [L232-262]: `def broken_decoys(ctx, j, inputs, acts, z, d, dy) -> dict` - Wrong g_D, another model's projector, transposed P_S and the J-built decoy must fail M0-D
- **function `_refused`** [L265-270]: `def _refused(fn) -> bool`
- **function `checks`** [L273-312]: `def checks(ctx, j, inputs, acts, z) -> dict` - §10.1: the broken decoys, the forbidden accesses (DTEST before ACCEPT, a construction
- **function `sealed_check`** [L315-322]: `def sealed_check(ctx) -> dict` - A sealed/ read before the TEST outcome must be refused (§10.1 forbidden access).
- **function `registry_c2`** [L325-336]: `def registry_c2(ctx) -> dict` - Registry row 2 in the dry run (R-0125-2, ND-C55): nd_registry.source_c2 on the c2/

