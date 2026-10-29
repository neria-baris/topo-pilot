# `tools/hwsc/hwsc_known.py`

- Source: [tools/hwsc/hwsc_known.py](../../../../../tools/hwsc/hwsc_known.py)
- Kind: python
- Lines: 316

## Module docstring

> HWSC G0c and the known cases KC0-KC9 (API.md §5; protocol §4; rulings R-0176-G1, G2).
> hwsc_driver is imported lazily inside g0c and run_kc (the hwsb_known.kb0 pattern).

## Imports

### Internal (repo files)

- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](hwsc_config.py.md) (line 6, via same directory)
- `import hwsb_kb` -> [tools/hwsb/hwsb_kb.py](../hwsb/hwsb_kb.py.md) (line 16, via unique basename)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../hwsb/hwsb_known.py.md) (line 17, via unique basename)
- `import hwsc_bind` -> [tools/hwsc/hwsc_bind.py](hwsc_bind.py.md) (line 18, via same directory)
- `import hwsc_data` -> [tools/hwsc/hwsc_data.py](hwsc_data.py.md) (line 19, via same directory)
- `import hwsc_gates` -> [tools/hwsc/hwsc_gates.py](hwsc_gates.py.md) (line 20, via same directory)
- `import hwsc_registry` -> [tools/hwsc/hwsc_registry.py](hwsc_registry.py.md) (line 21, via same directory)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 22, via unique basename)
- `import k4b_config` -> [tools/k4b/k4b_config.py](../k4b/k4b_config.py.md) (line 23, via unique basename)
- `import k4b_data` -> [tools/k4b/k4b_data.py](../k4b/k4b_data.py.md) (line 24, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 26, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 27, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 29, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 30, via package root)
- `import hwsc_driver` -> [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 84, via same directory) (inside a function)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 172, via unique basename) (inside a function)
- `import hwsb_gates` -> [tools/hwsb/hwsb_gates.py](../hwsb/hwsb_gates.py.md) (line 200, via unique basename) (inside a function)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../hwsb/hwsb_known.py.md) (line 249, via unique basename) (inside a function)
- `import hwsc_driver` -> [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 250, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 25)

### Standard library

- `__future__` (lines 4)
- `fractions` (lines 13)
- `importlib` (lines 7)
- `os` (lines 8)
- `pathlib` (lines 14)
- `re` (lines 9)
- `subprocess` (lines 10)
- `sys` (lines 11)
- `time` (lines 12)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- `import_module` line 189: `dynamic: r['module']`
- `import_module` line 209: `dynamic: m`

### sys.path additions

- none

## Imported by

- [tests/hwsc/test_b_guard_meter.py](../../tests/hwsc/test_b_guard_meter.py.md) (line 27, import)
- [tests/hwsc/test_b_train_hold.py](../../tests/hwsc/test_b_train_hold.py.md) (line 29, import)
- [tests/hwsc/test_r_0181_g0c_lineage_order.py](../../tests/hwsc/test_r_0181_g0c_lineage_order.py.md) (line 19, import)
- [tests/hwsc/test_r_0181_kc_records_rehearsal.py](../../tests/hwsc/test_r_0181_kc_records_rehearsal.py.md) (line 18, import)
- [tests/hwsc/test_r_0184_kc7_inside_binding.py](../../tests/hwsc/test_r_0184_kc7_inside_binding.py.md) (line 19, import)
- [tools/hwsc/hwsc_driver.py](hwsc_driver.py.md) (line 17, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 24, import)
- [tools/hwsc/hwsc_dry.py](hwsc_dry.py.md) (line 243, import)
- [tools/hwsc/hwsc_dry3.py](hwsc_dry3.py.md) (line 14, import)

## Top-level constants

- `SKIP_DIRS`
- `TEXT_SUFFIXES`

## Classes and functions

- **function `needle_in`** [L38-41]: `def needle_in(needle, line) -> bool`
- **function `_skip_dir`** [L44-48]: `def _skip_dir(parent, name, groot) -> bool`
- **function `seed_search_c`** [L51-66]: `def seed_search_c(root, needles, root_for_guard=None) -> list`
- **function `classify_hits_c`** [L69-73]: `def classify_hits_c(hits, fragments=None, job_scratch=None) -> dict`
- **function `_sha_ok`** [L76-80]: `def _sha_ok(path, want) -> bool | None`
- **function `g0c`** [L83-134]: `def g0c(out, stage, auth=None, sched=None, release=None, root=cc.ROOT, mailbox=cc.MAILBOX) -> dict`
- **function `kc1`** [L138-143]: `def kc1(store, masters=cc.MASTERS) -> tuple`
- **function `kc4`** [L146-153]: `def kc4(proc_w0, proc_star, handoff) -> dict`
- **function `_fixture`** [L157-168]: `def _fixture()`
- **function `_identity_calls`** [L171-180]: `def _identity_calls(T, E, pi) -> dict`
- **function `kc7`** [L183-212]: `def kc7(table=None) -> dict`
- **function `kc8`** [L216-235]: `def kc8(job) -> dict`
- **function `kc9`** [L238-244]: `def kc9(out) -> dict`
- **function `run_kc`** [L248-316]: `def run_kc(out, auth, sched, job, store=None) -> dict`

