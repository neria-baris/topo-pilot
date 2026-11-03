# `tools/hwsu/hwsu_of.py`

- Source: [tools/hwsu/hwsu_of.py](../../../../../tools/hwsu/hwsu_of.py)
- Kind: python
- Lines: 377

## Module docstring

> HWSU stage OF gates OF-P .. OF-5, outcome and report (API.md §4; protocol §4.2).

## Imports

### Internal (repo files)

- `import hwsu_config` -> [tools/hwsu/hwsu_config.py](hwsu_config.py.md) (line 10, via same directory)
- `import hwsu_oracle` -> [tools/hwsu/hwsu_oracle.py](hwsu_oracle.py.md) (line 11, via same directory)
- `import hwsu_pairs` -> [tools/hwsu/hwsu_pairs.py](hwsu_pairs.py.md) (line 12, via same directory)
- `import hwsu_records` -> [tools/hwsu/hwsu_records.py](hwsu_records.py.md) (line 13, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 18, via unique basename)
- `import c2_attrib` -> [tools/c2_readout/c2_attrib.py](../c2_readout/c2_attrib.py.md) (line 19, via unique basename)
- `import c2_decide` -> [tools/c2_readout/c2_decide.py](../c2_readout/c2_decide.py.md) (line 20, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../hwsb/hwsb_data.py.md) (line 21, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 22, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 23, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 24, via unique basename)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 26, via unique basename)
- `import precision` -> [tools/x4_circle_history/precision.py](../x4_circle_history/precision.py.md) (line 27, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 28, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 29, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, MemoryBackend` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 30, via package root)

### External (third-party)

- `numpy` (lines 25)

### Standard library

- `__future__` (lines 8)
- `fractions` (lines 15)
- `json` (lines 14)
- `pathlib` (lines 16)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsu/test_a_of_gates.py](../../tests/hwsu/test_a_of_gates.py.md) (line 17, import)
- [tests/hwsu/test_a_of_ladder.py](../../tests/hwsu/test_a_of_ladder.py.md) (line 13, import)
- [tests/hwsu/test_a_of_oracle.py](../../tests/hwsu/test_a_of_oracle.py.md) (line 16, import)
- [tests/hwsu/test_b_of_driver.py](../../tests/hwsu/test_b_of_driver.py.md) (line 21, import)
- [tests/hwsu/test_b_of_obligation.py](../../tests/hwsu/test_b_of_obligation.py.md) (line 318, import)
- [tests/hwsu/test_b_of_obligation.py](../../tests/hwsu/test_b_of_obligation.py.md) (line 325, import)
- [tests/hwsu/test_b_of_obligation.py](../../tests/hwsu/test_b_of_obligation.py.md) (line 340, import)
- [tests/hwsu/test_b_of_obligation.py](../../tests/hwsu/test_b_of_obligation.py.md) (line 349, import)
- [tests/hwsu/test_b_of_obligation.py](../../tests/hwsu/test_b_of_obligation.py.md) (line 357, import)
- [tools/hwsu/hwsu_driver_of.py](hwsu_driver_of.py.md) (line 6, import)
- [tools/hwsu/hwsu_dry.py](hwsu_dry.py.md) (line 10, import)
- [tools/hwsu/hwsu_dry_b.py](hwsu_dry_b.py.md) (line 8, import)
- [tools/hwsu/u2/hwsu_decide.py](u2/hwsu_decide.py.md) (line 10, import)
- [tools/hwsu/u2/hwsu_driver.py](u2/hwsu_driver.py.md) (line 15, import)
- [tools/hwsu/u2/hwsu_gates.py](u2/hwsu_gates.py.md) (line 14, import)
- [tools/hwsu/u2/hwsu_known.py](u2/hwsu_known.py.md) (line 12, import)

## Top-level constants

- `FEAS`
- `ORACLE`

## Classes and functions

- **function `_draws`** [L37-38]: `def _draws(ctx) -> int`
- **function `_bounds`** [L41-52]: `def _bounds(arrays, seed, alpha, draws) -> tuple` - Gate bounds from c2_decide.stream_bounds (through its module at call time) and, from a
- **function `_tm`** [L55-56]: `def _tm(x) -> float`
- **function `of_p`** [L60-90]: `def of_p(ctx) -> dict`
- **function `reservation_check`** [L93-100]: `def reservation_check(ctx) -> dict`
- **function `of_s`** [L104-133]: `def of_s(out, ctx) -> dict`
- **function `of_h`** [L137-150]: `def of_h(ctx) -> dict`
- **function `of_1`** [L154-184]: `def of_1(ctx) -> dict`
- **function `of_2`** [L188-198]: `def of_2(ctx) -> dict`
- **function `_psi`** [L201-207]: `def _psi(ctx, K=None, euclidean=False)`
- **function `of_3`** [L210-240]: `def of_3(ctx) -> dict`
- **function `of_4`** [L244-283]: `def of_4(ctx) -> dict`
- **function `of_5`** [L287-303]: `def of_5(ctx) -> dict`
- **function `of_outcome`** [L307-312]: `def of_outcome(records) -> str`
- **function `tails`** [L315-320]: `def tails(G) -> dict`
- **function `of_report`** [L323-377]: `def of_report(out, ctx, records) -> Path`

