# `tools/hwsg/hwsg_known.py`

- Source: [tools/hwsg/hwsg_known.py](../../../../../tools/hwsg/hwsg_known.py)
- Kind: python
- Lines: 376

## Module docstring

> HWSG known cases KG0-KG8 (API.md §10; protocol §5) and the KC job.

## Imports

### Internal (repo files)

- `import hwsg_config` -> [tools/hwsg/hwsg_config.py](hwsg_config.py.md) (line 5, via same directory)
- `import hwsg_bind` -> [tools/hwsg/hwsg_bind.py](hwsg_bind.py.md) (line 6, via same directory)
- `import hwsg_oracle` -> [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 7, via same directory)
- `import hwsg_ratio` -> [tools/hwsg/hwsg_ratio.py](hwsg_ratio.py.md) (line 8, via same directory)
- `import hwsb_config` -> [tools/hwsb/hwsb_config.py](../hwsb/hwsb_config.py.md) (line 16, via unique basename)
- `import hwsb_known` -> [tools/hwsb/hwsb_known.py](../hwsb/hwsb_known.py.md) (line 17, via unique basename)
- `import hwsb_law` -> [tools/hwsb/hwsb_law.py](../hwsb/hwsb_law.py.md) (line 18, via unique basename)
- `import hwsc_config` -> [tools/hwsc/hwsc_config.py](../hwsc/hwsc_config.py.md) (line 19, via unique basename)
- `import hwsc_known` -> [tools/hwsc/hwsc_known.py](../hwsc/hwsc_known.py.md) (line 20, via unique basename)
- `import k4b_fresh` -> [tools/k4b/k4b_fresh.py](../k4b/k4b_fresh.py.md) (line 21, via unique basename)
- `import k4b_stats` -> [tools/k4b/k4b_stats.py](../k4b/k4b_stats.py.md) (line 22, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 24, via unique basename)
- `from c1_records import C1GateFailure` -> [tools/c1prime/c1_records.py](../c1prime/c1_records.py.md) (line 25, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, SeedTree` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 27, via package root)
- `from topo_pilot.contracts.backends import MemoryBackend` -> [src/topo_pilot/contracts/backends.py](../../src/topo_pilot/contracts/backends.py.md) (line 28, via package root)
- `from topo_pilot.dataset.checks import make_sequence_ids` -> [src/topo_pilot/dataset/checks.py](../../src/topo_pilot/dataset/checks.py.md) (line 29, via package root)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 58, via same directory) (inside a function)
- `from hwsg_train import child_argv, child_env` -> [tools/hwsg/hwsg_train.py](hwsg_train.py.md) (line 166, via same directory) (inside a function)
- `import k4b_cert` -> [tools/k4b/k4b_cert.py](../k4b/k4b_cert.py.md) (line 206, via unique basename) (inside a function)
- `import k4b_release` -> [tools/k4b/k4b_release.py](../k4b/k4b_release.py.md) (line 294, via unique basename) (inside a function)
- `import hwsg_registry` -> [tools/hwsg/hwsg_registry.py](hwsg_registry.py.md) (line 304, via same directory) (inside a function)
- `import hwsg_records` -> [tools/hwsg/hwsg_records.py](hwsg_records.py.md) (line 314, via same directory) (inside a function)
- `from hwsg_oracle import store_for` -> [tools/hwsg/hwsg_oracle.py](hwsg_oracle.py.md) (line 315, via same directory) (inside a function)
- `import k4b_driver` -> [tools/k4b/k4b_driver.py](../k4b/k4b_driver.py.md) (line 372, via unique basename) (inside a function)

### External (third-party)

- `numpy` (lines 23)
- `pytest` (lines 221)

### Standard library

- `__future__` (lines 3)
- `fractions` (lines 13)
- `hashlib` (lines 9)
- `json` (lines 10)
- `os` (lines 11)
- `pathlib` (lines 14)
- `subprocess` (lines 12)
- `tempfile` (lines 248)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hwsg/test_impl_review.py](../../tests/hwsg/test_impl_review.py.md) (line 13, import)
- [tools/hwsg/hwsg_dry.py](hwsg_dry.py.md) (line 9, import)
- [tools/hwsg/hwsg_jobs.py](hwsg_jobs.py.md) (line 9, import)

## Top-level constants

- `ORDER`

## Classes and functions

- **function `_sha`** [L35-36]: `def _sha(path) -> str`
- **function `seed_search_g`** [L39-54]: `def seed_search_g(root, needles) -> list`
- **function `kg0`** [L57-89]: `def kg0(out, auth, sched, root=None, cache=None) -> dict`
- **function `_wstar_def`** [L92-100]: `def _wstar_def() -> gc.WorldDef`
- **function `kg1`** [L103-124]: `def kg1(store) -> dict`
- **function `_draws`** [L127-128]: `def _draws(scope, split, process, n=64)`
- **function `kg2`** [L131-151]: `def kg2() -> dict`
- **function `kg3`** [L154-158]: `def kg3(proc_w0) -> dict`
- **function `_launch`** [L161-162]: `def _launch(argv, env)`
- **function `kg4`** [L165-189]: `def kg4(out, launcher=None) -> dict`
- **function `_law`** [L192-195]: `def _law(p, sigma, nb)`
- **function `kg5`** [L198-217]: `def kg5(proc_w0, proc_star, handoff, worlds_procs) -> dict`
- **function `kg6`** [L220-236]: `def kg6(job) -> dict`
- **function `_fixture`** [L239-244]: `def _fixture(c, rows=3072, seed=7)`
- **function `kg7`** [L247-289]: `def kg7() -> dict`
- **function `_archive`** [L292-300]: `def _archive(out, target, tag) -> None` - Move an earlier attempt's files to superseded/<tag>-a<k>/ (k4b_release.archive_attempt).
- **function `kg8`** [L303-310]: `def kg8(out) -> dict`
- **function `run_kc`** [L313-375]: `def run_kc(out, auth, sched, job) -> dict`

