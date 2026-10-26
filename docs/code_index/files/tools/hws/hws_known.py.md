# `tools/hws/hws_known.py`

- Source: [tools/hws/hws_known.py](../../../../../tools/hws/hws_known.py)
- Kind: python
- Lines: 286

## Module docstring

> HWS known-answer checks: stage S0 (KC1-KC14, protocol §3) and the exact and numerical dry-run
> cases DR1-DR8 (§13, TEST_PLAN §4). Split from hws_driver by size (erratum E16, the R-0118-6
> pattern); hws_driver.run_s0 delegates here. The DR cases touch synthetic worlds and
> deterministic rows only; DR2 samples the known-zero U and N controls, never a sweep world.

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](hws_worlds.py.md) (line 15, via same directory)
- `import hws_driver` -> [tools/hws/hws_driver.py](hws_driver.py.md) (line 16, via same directory)
- `import hws_exact` -> [tools/hws/hws_exact.py](hws_exact.py.md) (line 17, via same directory)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](hws_oracle.py.md) (line 18, via same directory)
- `import hws_records` -> [tools/hws/hws_records.py](hws_records.py.md) (line 19, via same directory)
- `import hws_select` -> [tools/hws/hws_select.py](hws_select.py.md) (line 20, via same directory)
- `import hws_stats` -> [tools/hws/hws_stats.py](hws_stats.py.md) (line 21, via same directory)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 22, via unique basename)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 24, via unique basename)
- `import stage_records` -> [tools/x4_circle_history/stage_records.py](../x4_circle_history/stage_records.py.md) (line 25, via unique basename)
- `from topo_pilot.contracts import ArtifactStore, LocalFSBackend, SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 26, via package root)
- `from topo_pilot.process import EmissionConfig, GridCenters, ProcessStage, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 27, via package root)
- `from topo_pilot.world import WorldConfig, WorldStage` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 23)

### Standard library

- `__future__` (lines 7)
- `fractions` (lines 12)
- `itertools` (lines 9)
- `json` (lines 10)
- `math` (lines 11)
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

- [tools/hws/hws_driver.py](hws_driver.py.md) (line 197, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 16, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 23, import)

## Top-level constants

- none

## Classes and functions

- **function `_tol`** [L37-40]: `def _tol(x, ref, s, n_r) -> dict`
- **function `_ok`** [L43-44]: `def _ok(flag) -> str`
- **function `zero_max`** [L47-50]: `def zero_max(rows) -> float`
- **function `known_cases`** [L53-90]: `def known_cases(w0, ex0, rec0, look0, zero) -> dict` - KC1-KC14 on the S0 rows (§3; tolerance rule with the sweep's own per-row SD).
- **function `run_s0`** [L93-132]: `def run_s0(out, auth) -> dict` - §3: w0 at 32,768 rows, U and N at 4,096; KC1-KC14 gate; freezes g4* and g4A*.
- **function `_dry`** [L138-139]: `def _dry(proc, case, n, Ks=(1, 2, 4), layout=TINY) -> dict`
- **function `_fixed_tok`** [L142-143]: `def _fixed_tok(n=64, V=36, a=11, b=5) -> np.ndarray`
- **function `dr1`** [L146-166]: `def dr1(out)`
- **function `dr2`** [L169-176]: `def dr2(out)`
- **function `dr3`** [L179-185]: `def dr3(out)`
- **function `dr4`** [L188-206]: `def dr4(out)`
- **function `dr5`** [L209-220]: `def dr5(out)`
- **function `dr6`** [L223-231]: `def dr6(out)`
- **function `_artifacts`** [L234-246]: `def _artifacts(root) -> dict`
- **function `_seal`** [L249-259]: `def _seal(root, metas, base) -> None`
- **function `dr7`** [L262-275]: `def dr7(out)`
- **function `dr8`** [L278-286]: `def dr8(out)`

