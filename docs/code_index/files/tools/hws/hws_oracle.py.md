# `tools/hws/hws_oracle.py`

- Source: [tools/hws/hws_oracle.py](../../../../../tools/hws/hws_oracle.py)
- Kind: python
- Lines: 169

## Module docstring

> HWS oracle: streams, sampling, per-row arrays, nulls, P4 (API.md §3).

## Imports

### Internal (repo files)

- `import hws_worlds` -> [tools/hws/hws_worlds.py](hws_worlds.py.md) (line 10, via same directory)
- `import k4b_scores` -> [tools/k4b/k4b_scores.py](../k4b/k4b_scores.py.md) (line 11, via unique basename)
- `import oracle_profile` -> [tools/x4_oracle_profile/oracle_profile.py](../x4_oracle_profile/oracle_profile.py.md) (line 13, via unique basename)
- `import scores` -> [tools/x4_circle_history/scores.py](../x4_circle_history/scores.py.md) (line 14, via unique basename)
- `from topo_pilot.contracts import SeedTree, SequenceLayout` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 15, via package root)
- `from topo_pilot.dataset.sampler import HMMSampler` -> [src/topo_pilot/dataset/sampler.py](../../src/topo_pilot/dataset/sampler.py.md) (line 16, via package root)
- `from topo_pilot.oracle import context_gain` -> [src/topo_pilot/oracle/__init__.py](../../src/topo_pilot/oracle/__init__.py.md) (line 17, via package root)

### External (third-party)

- `numpy` (lines 12)

### Standard library

- `__future__` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [tests/hws/test_a_identities.py](../../tests/hws/test_a_identities.py.md) (line 29, import)
- [tests/hws/test_b_oracle.py](../../tests/hws/test_b_oracle.py.md) (line 25, import)
- [tests/hws/test_b_records.py](../../tests/hws/test_b_records.py.md) (line 30, import)
- [tools/hws/hws_driver.py](hws_driver.py.md) (line 18, import)
- [tools/hws/hws_dry.py](hws_dry.py.md) (line 17, import)
- [tools/hws/hws_exact.py](hws_exact.py.md) (line 21, import)
- [tools/hws/hws_known.py](hws_known.py.md) (line 18, import)

## Top-level constants

- `KS_S0`
- `KS_S3`
- `KS_SCREEN`
- `NULL_NAMES`
- `ORTH_KS`
- `STREAM_STAGES`

## Classes and functions

- **function `history_generator`** [L27-34]: `def history_generator(stage, key, origin=None)`
- **function `perm_generator`** [L37-38]: `def perm_generator(key)`
- **function `sample`** [L41-48]: `def sample(proc, n, rng, layout=SequenceLayout()) -> np.ndarray` - Exactly one HMMSampler.sample call; w_last and the states are dropped at once.
- **function `beliefs`** [L51-56]: `def beliefs(proc, tok, Ks) -> dict`
- **function `predictive`** [L59-60]: `def predictive(b, T, E) -> np.ndarray`
- **function `circ_marginal`** [L63-65]: `def circ_marginal(q, n_axial) -> np.ndarray`
- **function `x_marginal`** [L68-69]: `def x_marginal(b, W, Hh) -> np.ndarray`
- **function `kl_rows`** [L72-84]: `def kl_rows(p, q) -> np.ndarray` - sum_v p (log p - log q), p = 0 terms 0 (the context_gain convention, choice 9).
- **function `entropy_rows`** [L87-92]: `def entropy_rows(p) -> np.ndarray`
- **function `row_arrays`** [L95-143]: `def row_arrays(proc, tok, Ks) -> dict` - The per-row arrays of §4.7 step 3 (API.md §3 keys; int K, erratum E3).
- **function `prefix_permuted`** [L146-151]: `def prefix_permuted(tok, rng) -> np.ndarray`
- **function `p4_rows`** [L154-159]: `def p4_rows(proc, tok, mL, rng) -> np.ndarray`
- **function `world_look`** [L162-169]: `def world_look(proc, stage, n, Ks, origin=None, layout=SequenceLayout(), p4=False) -> dict`

