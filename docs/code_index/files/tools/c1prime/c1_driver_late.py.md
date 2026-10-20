# `tools/c1prime/c1_driver_late.py`

- Source: [tools/c1prime/c1_driver_late.py](../../../../../tools/c1prime/c1_driver_late.py)
- Kind: python
- Lines: 265

## Module docstring

> C1' stage driver, part 3: shared split evaluation (C0-val, M4, M2, M3, V1, V2, V3, P1
> statistics) and the validation stage S5 (protocol §16 rows 12-19, §10-§12). Implemented in job
> 0026; never run on data in job 0026. Validation means are written sealed and never read here.

## Imports

### Internal (repo files)

- `import c1_bounds` -> [tools/c1prime/c1_bounds.py](c1_bounds.py.md) (line 9, via same directory)
- `import c1_cert` -> [tools/c1prime/c1_cert.py](c1_cert.py.md) (line 10, via same directory)
- `import c1_chart` -> [tools/c1prime/c1_chart.py](c1_chart.py.md) (line 11, via same directory)
- `import c1_config` -> [tools/c1prime/c1_config.py](c1_config.py.md) (line 12, via same directory)
- `import c1_driver` -> [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 13, via same directory)
- `import c1_driver_cal` -> [tools/c1prime/c1_driver_cal.py](c1_driver_cal.py.md) (line 14, via same directory)
- `import c1_endpoint` -> [tools/c1prime/c1_endpoint.py](c1_endpoint.py.md) (line 15, via same directory)
- `import c1_fit` -> [tools/c1prime/c1_fit.py](c1_fit.py.md) (line 16, via same directory)
- `import c1_gates` -> [tools/c1prime/c1_gates.py](c1_gates.py.md) (line 17, via same directory)
- `import c1_model` -> [tools/c1prime/c1_model.py](c1_model.py.md) (line 18, via same directory)
- `import c1_oracle` -> [tools/c1prime/c1_oracle.py](c1_oracle.py.md) (line 19, via same directory)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 21, via unique basename)
- `from c1_records import begin_stage` -> [tools/c1prime/c1_records.py](c1_records.py.md) (line 22, via same directory)
- `import c1_driver_fresh` -> [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 261, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 20)

### Standard library

- `__future__` (lines 5)
- `json` (lines 7)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/c1prime/c1_driver.py](c1_driver.py.md) (line 314, import)
- [tools/c1prime/c1_driver_fresh.py](c1_driver_fresh.py.md) (line 15, import)

## Top-level constants

- none

## Classes and functions

- **function `setup_split`** [L27-46]: `def setup_split(ctx, split) -> dict` - Models, frozen fits and split rows (activations only) for validation or fresh.
- **function `_b32`** [L49-50]: `def _b32(r, k)`
- **function `c0_val_gate`** [L53-71]: `def c0_val_gate(ctx, S) -> dict`
- **function `states`** [L74-78]: `def states(ctx, S) -> None`
- **function `m4_gate`** [L81-87]: `def m4_gate(S) -> dict`
- **function `m23`** [L90-98]: `def m23(ctx, S) -> dict`
- **function `v12`** [L101-113]: `def v12(S, which) -> dict`
- **function `donor_contrast`** [L116-141]: `def donor_contrast(ctx, S, cert, seed) -> dict` - V3: A_full from the model's own donor logits, Z_full, b^Zf, B^V3 and the guard.
- **function `endpoint_arrays`** [L144-164]: `def endpoint_arrays(ctx, S) -> dict` - Primary and control logits (reference and tail paths), A_T, A_C, Y and Z per model.
- **function `identity_checks_split`** [L167-181]: `def identity_checks_split(ctx, S, tail) -> dict` - Identity patch bitwise on every eligible row (tail=False) or the tail-path identity on
- **function `identity_checks`** [L184-187]: `def identity_checks(ctx, S) -> dict`
- **function `run_validation`** [L190-225]: `def run_validation(ctx) -> None`
- **function `_strip`** [L228-230]: `def _strip(res, S) -> dict`
- **function `_seal`** [L233-242]: `def _seal(ctx, S, v3res) -> None` - Sealed validation means (§12.5): written once, never read by the driver.
- **function `_jsonable`** [L245-252]: `def _jsonable(x)`
- **function `run`** [L255-265]: `def run(ctx, stage) -> None`

