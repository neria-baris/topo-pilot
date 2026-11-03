# `tools/hwsu/u2/hwsu_decide.py`

- Source: [tools/hwsu/u2/hwsu_decide.py](../../../../../../tools/hwsu/u2/hwsu_decide.py)
- Kind: python
- Lines: 238

## Module docstring

> HWSU decision side: P1 ladder, family stream, per-model statements, aggregation, outcomes,
> licences, descriptives, sealing (API_U2.md sections 4.2, 4.4-4.7). Split from hwsu_gates by size
> (API erratum); every name stays reachable as hwsu_gates.<name>. Response family only.

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](../hwsu_config.py.md) (line 8, via unique basename)
- `import hwsu_model` -> [tools/hwsu/u2/hwsu_model.py](hwsu_model.py.md) (line 9, via same directory)
- `import hwsu_of` -> [tools/hwsu/hwsu_of.py](../hwsu_of.py.md) (line 10, via unique basename)
- `import u2` -> [tools/hwsu/u2/__init__.py](__init__.py.md) (line 11, via unique basename)
- `import c1_means` -> [tools/c1prime/c1_means.py](../../c1prime/c1_means.py.md) (line 17, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../../c2_readout/c2_attrib.py.md) (line 18, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../../c2_readout/c2_decide.py.md) (line 19, via unique basename)
- `import precision` -> [tools/x4_circle_history/precision.py](../../x4_circle_history/precision.py.md) (line 21, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../../x4_circle_history/stage_records.py.md) (line 22, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../../c1prime/c1_records.py.md) (line 23, via unique basename)

### External (third-party)

- `numpy` (lines 20)

### Standard library

- `__future__` (lines 6)
- `fractions` (lines 14)
- `json` (lines 12)
- `pathlib` (lines 15)
- `re` (lines 13)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tools/hwsu/u2/hwsu_driver.py](hwsu_driver.py.md) (line 9, import)
- [tools/hwsu/u2/hwsu_dry2b.py](hwsu_dry2b.py.md) (line 11, import)
- [tools/hwsu/u2/hwsu_e2.py](hwsu_e2.py.md) (line 9, import)
- [tools/hwsu/u2/hwsu_gates.py](hwsu_gates.py.md) (line 11, import)

## Top-level constants

- `NUMERICAL`
- `SEALED_KEYS_U`
- `SHARE_OUTCOME`
- `_CAT`
- `_REGIONS`
- `_SEALED_RE`
- `_ST`

## Classes and functions

- **function `_tm`** [L35-36]: `def _tm(x) -> float`
- **function `p1_u`** [L40-70]: `def p1_u(A, G, models, seeds, ladder=uc.LADDER) -> dict`
- **function `family_bounds`** [L74-84]: `def family_bounds(A, G, models, seed=640111, alpha=Fraction(1, 300), draws=20000) -> dict`
- **function `model_status`** [L87-97]: `def model_status(bj) -> dict`
- **function `_region`** [L103-109]: `def _region(x) -> str`
- **function `fw_events`** [L112-121]: `def fw_events(theta_region) -> int` - Lemma FW-U, response part: events whose union holds 'a declared statement is false'.
- **function `_base`** [L129-131]: `def _base(st) -> str`
- **function `response_outcome`** [L134-155]: `def response_outcome(per_model, rule6=None) -> dict`
- **function `share_outcome`** [L158-160]: `def share_outcome(of_bind) -> dict`
- **function `study_outcome`** [L163-171]: `def study_outcome(records, resp, share=None) -> str`
- **function `licences`** [L174-196]: `def licences(resp, per_model, bounds, desc, contract=None) -> dict`
- **function `descriptives`** [L199-207]: `def descriptives(A, G, rowA, models) -> dict`
- **function `write_sealed_u`** [L211-224]: `def write_sealed_u(store, arrays) -> str`
- **function `check_unsealed_u`** [L227-237]: `def check_unsealed_u(report) -> None`

