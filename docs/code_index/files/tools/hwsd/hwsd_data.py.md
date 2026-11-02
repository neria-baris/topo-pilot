# `tools/hwsd/hwsd_data.py`

- Source: [tools/hwsd/hwsd_data.py](../../../../../tools/hwsd/hwsd_data.py)
- Kind: python
- Lines: 400

## Module docstring

> HWSD data: blocks and tables, H2-D separation, registry risk, ORACLE-D, reference persistence,
> B4-TEST, LGATE-ORACLE, shared controls, obligations (J11), reservations, end_reservation, W2
> attestation (API.md section 3 and section 22). Reused functions are called through their module
> attributes at call time, so the binding applies.

## Imports

### Internal (repo files)

- `import hwsd_config` -> [tools/hwsd/hwsd_config.py](hwsd_config.py.md) (line 8, via same directory)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../hwsb/hwsb_eval.py.md) (line 17, via unique basename)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](../hwsc/hwsc_data.py.md) (line 18, via unique basename)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 19, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 20, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 21, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 22, via unique basename)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 23, via unique basename)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 24, via unique basename)
- `import reference_cache` -> [tools/x4_circle_history/reference_cache.py](../x4_circle_history/reference_cache.py.md) (line 26, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 27, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 28, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 29, via unique basename)
- `from topo_pilot.contracts import SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 31, via package root)
- `from topo_pilot.dataset import HMMSampler` -> [src/topo_pilot/dataset/__init__.py](../../src/topo_pilot/dataset/__init__.py.md) (line 32, via package root)

### External (third-party)

- `numpy` (lines 25)

### Standard library

- `__future__` (lines 6)
- `copy` (lines 9)
- `decimal` (lines 13)
- `fnmatch` (lines 10)
- `fractions` (lines 14)
- `os` (lines 11)
- `pathlib` (lines 15)
- `re` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsd/test_b_binding.py](../../tests/hwsd/test_b_binding.py.md) (line 230, import)
- [tests/hwsd/test_b_data.py](../../tests/hwsd/test_b_data.py.md) (line 17, import)
- [tests/hwsd/test_b_registry_r10.py](../../tests/hwsd/test_b_registry_r10.py.md) (line 15, import)
- [tests/hwsd/test_b_reservation.py](../../tests/hwsd/test_b_reservation.py.md) (line 14, import)
- [tests/hwsd/test_c_continue.py](../../tests/hwsd/test_c_continue.py.md) (line 144, import)
- [tools/hwsd/hwsd_driver.py](hwsd_driver.py.md) (line 18, import)
- [tools/hwsd/hwsd_dry.py](hwsd_dry.py.md) (line 37, import)
- [tools/hwsd/hwsd_dry2.py](hwsd_dry2.py.md) (line 26, import)
- [tools/hwsd/hwsd_dry3.py](hwsd_dry3.py.md) (line 37, import)
- [tools/hwsd/hwsd_jobs.py](hwsd_jobs.py.md) (line 17, import)
- [tools/hwsd/hwsd_known.py](hwsd_known.py.md) (line 25, import)
- [tools/hwsd/hwsd_known2.py](hwsd_known2.py.md) (line 18, import)

## Top-level constants

- `ARRAY_SUFFIXES`
- `MOMENT_KEYS`
- `REF_KS`
- `_ART_RE`

## Classes and functions

- **function `_obl`** [L41-42]: `def _obl()`
- **function `block_generator`** [L46-48]: `def block_generator(split, scope=None, process=None)`
- **function `block_ids`** [L51-53]: `def block_ids(split, n, scope=None, process=None) -> np.ndarray`
- **function `sample_block_d`** [L56-63]: `def sample_block_d(T, E, pi, split, n, scope=None, process=None) -> tuple`
- **function `hist_name`** [L66-67]: `def hist_name(split, dry=False) -> str`
- **function `sample_tables`** [L70-77]: `def sample_tables(proc, scope=None, process=None, sizes=None) -> dict`
- **function `save_tables`** [L80-82]: `def save_tables(out, tables, dry=False) -> list`
- **function `load_tables`** [L85-91]: `def load_tables(out, dry=False) -> dict`
- **function `separation_d`** [L95-98]: `def separation_d(reg, tables) -> dict`
- **function `registry_risk_d`** [L101-104]: `def registry_risk_d(p_d2a) -> dict`
- **function `oracle_d`** [L108-124]: `def oracle_d(proc, tables) -> dict`
- **function `_save`** [L127-131]: `def _save(path, **arrays) -> Path`
- **function `save_oracle`** [L134-137]: `def save_oracle(out, moments) -> list`
- **function `refs_to_json`** [L140-145]: `def refs_to_json(refs, proc, test_table_sha256) -> dict`
- **function `refs_from_json`** [L148-167]: `def refs_from_json(obj, proc, n, test_table_sha256) -> list`
- **function `b4_test`** [L170-176]: `def b4_test(m_test, refs_test, eps, Z, seed=None) -> dict`
- **function `lgate_oracle`** [L179-185]: `def lgate_oracle(proc, canon32) -> dict`
- **function `save_lgate_q`** [L188-190]: `def save_lgate_q(out, q) -> Path`
- **function `shared_controls`** [L193-201]: `def shared_controls(m_test, canon32) -> dict`
- **function `save_shared`** [L204-214]: `def save_shared(out, shared, bounds) -> list`
- **function `_meta_type`** [L218-222]: `def _meta_type(store, rel)`
- **function `classify_file`** [L225-239]: `def classify_file(store, rel) -> tuple`
- **function `is_checkpoint_payload`** [L242-244]: `def is_checkpoint_payload(rel) -> bool`
- **function `obligation_files`** [L247-261]: `def obligation_files(store) -> list`
- **function `write_obligation`** [L264-276]: `def write_obligation(store, name, job, attempt, utc, reservation_id=None, dry_stores=(), written_by='hwsd') -> tuple`
- **function `stop_obligation`** [L279-282]: `def stop_obligation(store, job, attempt, reservation_id, utc) -> dict`
- **function `reservation_path`** [L286-287]: `def reservation_path(store, attempt) -> Path`
- **function `start_reservation_d`** [L290-303]: `def start_reservation_d(store, attempt, utc) -> tuple`
- **function `verify_reservation_d`** [L306-307]: `def verify_reservation_d(path, reservation_id, sampling_began=False) -> dict`
- **function `end_reservation`** [L310-338]: `def end_reservation(store, reservation_id, utc, obligation_path, written_by='hwsd_data.end_reservation') -> dict`
- **function `reservation_ended`** [L341-371]: `def reservation_ended(res_path, root=None) -> dict`
- **function `w2_attest`** [L374-400]: `def w2_attest(root=None, exclude=()) -> dict`

