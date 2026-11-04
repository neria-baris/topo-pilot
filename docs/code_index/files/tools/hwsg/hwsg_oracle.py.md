# `tools/hwsg/hwsg_oracle.py`

- Source: [tools/hwsg/hwsg_oracle.py](../../../../../tools/hwsg/hwsg_oracle.py)
- Kind: python
- Lines: 322

## Module docstring

> HWSG process, identity and stage O (API.md §4; protocol §2.3, §2.6, §3; gates O0-O5).

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 5, via same directory)
- `import hwsg_bind` -> [tools/hwsg/hwsg_bind.py](hwsg_bind.py.md) (line 6, via same directory)
- `import c1_means` -> [tools/c1prime/c1_means.py](../c1prime/c1_means.py.md) (line 13, via unique basename)
- `import hws_exact` -> [tools/hws/hws_exact.py](../hws/hws_exact.py.md) (line 14, via unique basename)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](../hws/hws_oracle.py.md) (line 15, via unique basename)
- `import hws_worlds` -> [tools/hws/hws_worlds.py](../hws/hws_worlds.py.md) (line 16, via unique basename)
- `import hwsb_data` -> [tools/hwsb/hwsb_data.py](../hwsb/hwsb_data.py.md) (line 17, via unique basename)
- `import hwsb_eval` -> [tools/hwsb/hwsb_eval.py](../hwsb/hwsb_eval.py.md) (line 18, via unique basename)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](../hwsb/hwsb_law.py.md) (line 19, via unique basename)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 20, via unique basename)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 22, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 23, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 24, via unique basename)
- `from topo_pilot.contracts import ArtifactStore` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 26, via package root)
- `from topo_pilot.contracts.backends import LocalFSBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 27, via package root)
- `from topo_pilot.contracts import WorldSpec` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 28, via package root)
- `from topo_pilot.process.transition import TransitionBuilder` -> [src/topo_pilot/process/transition.py](../../src/topo_pilot/process/transition.py.md) (line 29, via package root)
- `from topo_pilot.process import TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 55, via package root) (inside a function)
- `import hwsg_handoff` -> [tools/hwsg/hwsg_handoff.py](hwsg_handoff.py.md) (line 88, via same directory) (inside a function)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 90, via unique basename) (inside a function)
- `import hwsg_handoff` -> [tools/hwsg/hwsg_handoff.py](hwsg_handoff.py.md) (line 244, via same directory) (inside a function)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 245, via same directory) (inside a function)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 246, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 21)

### Standard library

- `__future__` (lines 3)
- `fractions` (lines 10)
- `hashlib` (lines 7)
- `json` (lines 8)
- `math` (lines 9)
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

- [tests/hwsg/test_a_law.py](../../tests/hwsg/test_a_law.py.md) (line 25, import)
- [tests/hwsg/test_a_selection.py](../../tests/hwsg/test_a_selection.py.md) (line 25, import)
- [tests/hwsg/test_impl_review.py](../../tests/hwsg/test_impl_review.py.md) (line 14, import)
- [tools/hwsg/hwsg_bind.py](hwsg_bind.py.md) (line 43, import)
- [tools/hwsg/hwsg_dry.py](hwsg_dry.py.md) (line 10, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 241, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 7, import)
- [tools/hwsg/hwsg_known.py](hwsg_known.py.md) (line 315, import)
- [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 100, import)
- [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 242, import)

## Top-level constants

- none

## Classes and functions

- **function `build_process_g`** [L34-41]: `def build_process_g(store, w, masters=None) -> dict`
- **function `process_builder`** [L44-45]: `def process_builder(key)`
- **function `identity`** [L48-79]: `def identity(store, proc, w) -> dict`
- **function `identity_checker`** [L82-103]: `def identity_checker(key)`
- **function `_sha`** [L107-108]: `def _sha(path) -> str`
- **function `selection`** [L111-134]: `def selection(report_path=None, s3_dir=None) -> dict`
- **function `_s3`** [L137-142]: `def _s3(w, s3_dir=None) -> dict`
- **function `law`** [L146-167]: `def law(proc, w, s3_dir=None) -> dict`
- **function `d2a`** [L170-177]: `def d2a(proc) -> dict`
- **function `headroom`** [L180-186]: `def headroom(w, report) -> dict`
- **function `_means`** [L190-202]: `def _means(proc, tok) -> dict`
- **function `reproduce`** [L205-226]: `def reproduce(proc_hws, w, hist_path=None, s3_dir=None) -> dict`
- **function `stage_a_process`** [L229-231]: `def stage_a_process(w)`
- **function `store_for`** [L234-235]: `def store_for(wdir) -> ArtifactStore`
- **function `_files`** [L238-240]: `def _files(d) -> set`
- **function `run_o`** [L243-322]: `def run_o(out, auth, sched, job, store=None) -> dict`

