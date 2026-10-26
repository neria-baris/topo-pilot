# `tools/hws/hws_exact.py`

- Source: [tools/hws/hws_exact.py](../../../../../tools/hws/hws_exact.py)
- Kind: python
- Lines: 364

## Module docstring

> HWS exact pieces: symbol law, A_eff, p_D2a, enumeration, spot checks, tier-0 law report and
> the payload-free KC1 identity check (API.md §4; protocol §2.4, §2.6, §3 KC1/KC9/KC10, §8).

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](hws_worlds.py.md) (line 19, via same directory)
- `import error_bound` -> [tools/x4_circle_history/error_bound.py](../x4_circle_history/error_bound.py.md) (line 20, via unique basename)
- `import hws_oracle` -> [tools/hws/hws_oracle.py](hws_oracle.py.md) (line 21, via same directory)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 23, via unique basename)
- `import process_law` -> [tools/x4_circle_history/process_law.py](../x4_circle_history/process_law.py.md) (line 24, via unique basename)
- `from topo_pilot.contracts import SeedTree, canonical_json, make_artifact_id, payload_checksum` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 25, via package root)
- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 26, via package root)
- `from topo_pilot.process import EmissionConfig, OverlapGaussian, TransitionConfig` -> [src/topo_pilot/process/__init__.py](../../src/topo_pilot/process/__init__.py.md) (line 27, via package root)
- `from topo_pilot.world import WorldConfig` -> [src/topo_pilot/world/__init__.py](../../src/topo_pilot/world/__init__.py.md) (line 28, via package root)

### External (third-party)

- `numpy` (lines 22)

### Standard library

- `__future__` (lines 8)
- `dataclasses` (lines 15)
- `decimal` (lines 10)
- `fractions` (lines 16)
- `hashlib` (lines 11)
- `itertools` (lines 12)
- `json` (lines 13)
- `math` (lines 14)
- `pathlib` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hws/test_a_identities.py](../../tests/hws/test_a_identities.py.md) (line 30, import)
- [tests/hws/test_b_exact.py](../../tests/hws/test_b_exact.py.md) (line 26, import)
- [tests/hws/test_b_kc1.py](../../tests/hws/test_b_kc1.py.md) (line 34, import)
- [tools/hws/hws_driver.py](hws_driver.py.md) (line 17, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 15, import)
- [tools/hws/hws_known.py](hws_known.py.md) (line 17, import)

## Top-level constants

- `JSON_READS`
- `KC1`
- `TOL`

## Classes and functions

- **function `symbol_law`** [L35-36]: `def symbol_law(proc) -> np.ndarray`
- **function `last_symbol_posteriors`** [L39-41]: `def last_symbol_posteriors(proc) -> np.ndarray`
- **function `mean_last_entropy`** [L44-45]: `def mean_last_entropy(proc) -> float`
- **function `a_eff`** [L48-49]: `def a_eff(proc) -> float`
- **function `p_d2a`** [L52-59]: `def p_d2a(T, E, pi, alphabet=(0, 1, 2, 3, 4), Lh=32) -> float`
- **function `e4_check`** [L62-64]: `def e4_check(value, tau=Fraction(1, 2000000)) -> dict`
- **function `exact_world`** [L67-100]: `def exact_world(proc) -> dict` - §4.6 step 6: exact per-world values and E1-E4 before any sampling.
- **function `_forward`** [L106-111]: `def _forward(proc, hist) -> np.ndarray`
- **function `enumerate_histories`** [L114-119]: `def enumerate_histories(proc, Lh) -> tuple`
- **function `_flag`** [L122-123]: `def _flag(value, ok) -> dict`
- **function `exact_expectations`** [L126-174]: `def exact_expectations(proc, Lh, Ks) -> dict` - Probability-weighted means of row_arrays over every history, plus I1-I4, Prop. F and
- **function `suffix_enumeration`** [L177-192]: `def suffix_enumeration(proc, Ks=(1, 2, 3)) -> dict`
- **function `decimal_spot_check`** [L198-209]: `def decimal_spot_check(proc, tok, Ks) -> dict`
- **function `bayes_cross_check`** [L212-217]: `def bayes_cross_check(proc, tok) -> dict`
- **function `law_bound_report`** [L220-232]: `def law_bound_report(proc, enclosure=None) -> dict` - Tier-0 report only (§8, RC-3); never changes eligibility, ranking or selection.
- **function `_read`** [L238-244]: `def _read(path) -> tuple`
- **function `read_json`** [L247-248]: `def read_json(path) -> object`
- **function `_sha`** [L251-252]: `def _sha(data: bytes) -> str`
- **function `_rebuild`** [L255-263]: `def _rebuild(kind, seed=None)`
- **function `expected_envelope`** [L266-290]: `def expected_envelope(kind, seed=None, world_id=None) -> dict` - KC1 (d): the serialization envelope of ProcessStage, reconstructed without a loader.
- **function `_same`** [L293-294]: `def _same(a, b) -> bool`
- **function `_check_artifact`** [L297-328]: `def _check_artifact(root, name, env, manifest, seed) -> dict`
- **function `kc1_identity`** [L331-364]: `def kc1_identity(artifact_root, manifest_path, config_json_path, seeds=(1729, 2718, 3141)) -> dict` - §3 KC1 (a)-(d) with JSON reads only; a failure is returned, never raised (erratum E11).

