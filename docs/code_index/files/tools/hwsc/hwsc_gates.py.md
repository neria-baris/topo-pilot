# `tools/hwsc/hwsc_gates.py`

- Source: [tools/hwsc/hwsc_gates.py](../../../../../tools/hwsc/hwsc_gates.py)
- Kind: python
- Lines: 228

## Module docstring

> HWSC gates: H1-C, L1, P1 (p1c and the N rule), the POSITIVE_BELOW_MARGIN annotation, the
> outcome precedence and the licences (API.md §6, §11.2, §12; protocol §5, §6).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 6, via same directory)
- `import c1_cert` -> [tools/c1prime/c1_cert.py](../c1prime/c1_cert.py.md) (line 12, via unique basename)
- `import c1_model` -> [tools/c1prime/c1_model.py](../c1prime/c1_model.py.md) (line 13, via unique basename)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../hwsb/hwsb_eval.py.md) (line 14, via unique basename)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](../hwsb/hwsb_gates.py.md) (line 15, via unique basename)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](../hwsb/hwsb_law.py.md) (line 16, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](hwsc_data.py.md) (line 17, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 18, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 19, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 20, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 21, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 23, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 24, via unique basename)
- `from topo_pilot.contracts import SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 26, via package root)
- `from hwsc_outcome import annotations, licence, outcome, positive_below_margin, state_from_gates` -> [tools/hwsc/hwsc_outcome.py](hwsc_outcome.py.md) (line 222, via same directory)

### External (third-party)

- `numpy` (lines 22)
- `torch` (lines 89)

### Standard library

- `__future__` (lines 4)
- `fractions` (lines 9)
- `json` (lines 7)
- `math` (lines 8)
- `pathlib` (lines 10)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_a_decision.py](../../tests/hwsc/test_a_decision.py.md) (line 26, import)
- [tests/hwsc/test_a_ladder.py](../../tests/hwsc/test_a_ladder.py.md) (line 26, import)
- [tests/hwsc/test_a_law.py](../../tests/hwsc/test_a_law.py.md) (line 25, import)
- [tests/hwsc/test_a_learning.py](../../tests/hwsc/test_a_learning.py.md) (line 26, import)
- [tests/hwsc/test_a_outcomes.py](../../tests/hwsc/test_a_outcomes.py.md) (line 24, import)
- [tests/hwsc/test_b_records.py](../../tests/hwsc/test_b_records.py.md) (line 28, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 28, import)
- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 16, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 23, import)
- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 16, import)
- [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 17, import)
- [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 20, import)
- [tools/hwsc/hwsc_records.py](hwsc_records.py.md) (line 319, import)

## Top-level constants

- `STEP_LABEL`

## Classes and functions

- **function `_fr`** [L33-41]: `def _fr(x) -> Fraction`
- **function `_write`** [L44-48]: `def _write(out, name, obj) -> Path`
- **function `expected_meta_c`** [L52-58]: `def expected_meta_c(j, step, record) -> dict`
- **function `exclusion_check`** [L61-63]: `def exclusion_check(ids, handoff) -> dict`
- **function `law_identity`** [L66-77]: `def law_identity(proc, handoff) -> dict`
- **function `_stage_complete_sha`** [L80-85]: `def _stage_complete_sha(out, stage, rel) -> str | None`
- **function `h1c`** [L88-149]: `def h1c(out, ctx, handoff, store, stage='E1') -> dict`
- **function `l1`** [L153-170]: `def l1(out, ctx) -> dict`
- **function `p1c_ladder`** [L174-176]: `def p1c_ladder(X_minus, X_plus, r4n, F_plan, D_bar) -> dict`
- **function `choose_N`** [L179-186]: `def choose_N(N_C, ladder_result) -> dict`
- **function `p1c`** [L189-219]: `def p1c(out, ctx, handoff) -> dict`

