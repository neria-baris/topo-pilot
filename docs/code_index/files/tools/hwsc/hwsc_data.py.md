# `tools/hwsc/hwsc_data.py`

- Source: [tools/hwsc/hwsc_data.py](../../../../../tools/hwsc/hwsc_data.py)
- Kind: python
- Lines: 245

## Module docstring

> HWSC data: process, train/dev mirror, evaluation blocks, H2, H2-FRESH, registry risk
> (API.md §3; protocol §2.3, §2.4, §3.3, §3.4). Reused functions are called through their module
> attributes at call time, so the binding of hwsc_bind applies.

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 7, via same directory)
- `import c2_registry` -> [tools/c2_readout/c2_registry.py](../c2_readout/c2_registry.py.md) (line 13, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../hwsb/hwsb_data.py.md) (line 14, via unique basename)
- `import hws_exact` -> [tools/hws/hws_exact.py](../hws/hws_exact.py.md) (line 15, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 16, via unique basename)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 17, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 18, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 19, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 21, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 22, via unique basename)
- `from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 24, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 25, via package root)
- `from topo_pilot.dataset.checks import check_disjoint, make_sequence_ids, process_code` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 26, via package root)
- `from topo_pilot.dataset.public import assert_public` -> [src/topo_pilot/dataset/public.py](../../src/topo_pilot/dataset/public.py.md) (line 27, via package root)

### External (third-party)

- `numpy` (lines 20)

### Standard library

- `__future__` (lines 5)
- `fractions` (lines 9)
- `itertools` (lines 10)
- `json` (lines 8)
- `pathlib` (lines 11)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_a_ladder.py](../../tests/hwsc/test_a_ladder.py.md) (line 25, import)
- [tests/hwsc/test_a_law.py](../../tests/hwsc/test_a_law.py.md) (line 24, import)
- [tests/hwsc/test_b_registry.py](../../tests/hwsc/test_b_registry.py.md) (line 26, import)
- [tests/hwsc/test_b_registry2.py](../../tests/hwsc/test_b_registry2.py.md) (line 25, import)
- [tests/hwsc/test_b_streams.py](../../tests/hwsc/test_b_streams.py.md) (line 24, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 26, import)
- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 15, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 22, import)
- [tools/hwsc/hwsc_dry2.py](hwsc_dry2.py.md) (line 15, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 93, import)
- [tools/hwsc/hwsc_gates.py](hwsc_gates.py.md) (line 17, import)
- [tools/hwsc/hwsc_jobs.py](hwsc_jobs.py.md) (line 16, import)
- [tools/hwsc/hwsc_known.py](hwsc_known.py.md) (line 19, import)

## Top-level constants

- none

## Classes and functions

- **function `build_process_c`** [L33-34]: `def build_process_c(store, masters=cc.MASTERS) -> dict`
- **function `process_identity`** [L37-56]: `def process_identity(store, proc) -> dict`
- **function `sequence_ids_c`** [L60-66]: `def sequence_ids_c(role, n, plan, master, scope=cc.SCOPE) -> np.ndarray`
- **function `make_train_dev_c`** [L69-94]: `def make_train_dev_c(store, proc, master, plan, scope=cc.SCOPE) -> dict` - hwsb_data.make_train_dev line for line, with `scope` in place of the literal hwsb-v1.
- **function `block_generator`** [L98-100]: `def block_generator(split, block, scope=None, process=None)`
- **function `block_ids`** [L103-106]: `def block_ids(split, block, n, scope=None, process=None) -> np.ndarray`
- **function `sample_block_c`** [L109-116]: `def sample_block_c(T, E_canon, pi, split, block, n) -> tuple`
- **function `sample_lgate`** [L119-120]: `def sample_lgate(proc) -> tuple`
- **function `sample_eval`** [L123-128]: `def sample_eval(proc, split, block=0) -> tuple`
- **function `hist_name`** [L131-132]: `def hist_name(split, block, dry=False) -> str`
- **function `save_table`** [L135-139]: `def save_table(path, table) -> Path`
- **function `sample_test_c`** [L142-162]: `def sample_test_c(out, proc, release, reservation_path, dry) -> dict` - Real run: k4b_fresh.sample_test unchanged; dry run: its mirror with DRYHIST_ names.
- **function `separation_c`** [L166-188]: `def separation_c(reg, tables) -> dict`
- **function `h2c`** [L191-207]: `def h2c(out, ctx) -> dict`
- **function `h2_fresh_c`** [L210-232]: `def h2_fresh_c(out, ctx) -> dict`
- **function `p_d2a_check`** [L236-239]: `def p_d2a_check(proc, p_ref) -> dict`
- **function `registry_risk`** [L242-245]: `def registry_risk(p_d2a, N) -> dict`

