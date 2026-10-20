# `tools/d2a/d2a_eval.py`

- Source: [tools/d2a/d2a_eval.py](../../../../../tools/d2a/d2a_eval.py)
- Kind: python
- Lines: 381

## Module docstring

> D-2a evaluation: activations at arbitrary positions, model predictions, probes, behaviour and
> the per-model stage-3 pass (D2A-FROZEN-v1 §7, §9, §10.1; tools/d2a/API.md §2.4, §4).

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import rbf_bandwidth, rbf_features, rbf_map, standardizer` -> [src/topo_pilot/analysis/__init__.py](../../src/topo_pilot/analysis/__init__.py.md) (line 14, via package root)
- `from topo_pilot.contracts import Checkpoint, ErrorCode, SeedTree, SequenceLayout, StageFailure` -> [src/topo_pilot/contracts/__init__.py](../../src/topo_pilot/contracts/__init__.py.md) (line 15, via package root)
- `from topo_pilot.experiment.x4f_probe import nested_ridge` -> [src/topo_pilot/experiment/x4f_probe.py](../../src/topo_pilot/experiment/x4f_probe.py.md) (line 16, via package root)
- `from topo_pilot.learner import load_model` -> [src/topo_pilot/learner/__init__.py](../../src/topo_pilot/learner/__init__.py.md) (line 17, via package root)
- `from topo_pilot.learner.multihorizon import load_multi_horizon` -> [src/topo_pilot/learner/multihorizon.py](../../src/topo_pilot/learner/multihorizon.py.md) (line 18, via package root)
- `import d2a_targets` -> [tools/d2a/d2a_targets.py](d2a_targets.py.md) (line 21, via same directory)
- `import d2a_world` -> [tools/d2a/d2a_world.py](d2a_world.py.md) (line 22, via same directory)
- `from d2a_world import d1` -> [tools/d2a/d2a_world.py](d2a_world.py.md) (line 23, via same directory)
- `import d2a_train` -> [tools/d2a/d2a_train.py](d2a_train.py.md) (line 34, via same directory) (inside a function)
- `import d2a_train` -> [tools/d2a/d2a_train.py](d2a_train.py.md) (line 252, via same directory) (inside a function)

### External (third-party)

- `numpy` (lines 11)
- `torch` (lines 12)

### Standard library

- `__future__` (lines 4)
- `hashlib` (lines 6)
- `json` (lines 7)
- `pathlib` (lines 9)
- `sys` (lines 8)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- line 20: `str(Path(__file__).resolve().parent)` -> `tools/d2a`

## Imported by

- [tests/d2a/test_b_behaviour.py](../../tests/d2a/test_b_behaviour.py.md) (line 26, import)
- [tools/d2a/d2a_decide.py](d2a_decide.py.md) (line 171, import)
- [tools/d2a/d2a_decide.py](d2a_decide.py.md) (line 342, import)

## Top-level constants

- `CONTRAST`
- `HOOKS`
- `STRATA`
- `TARGETS`

## Classes and functions

- **function `load_run`** [L33-40]: `def load_run(run_id: str, step: int, store_root=W.STORE)`
- **function `_inputs`** [L43-44]: `def _inputs(tokens) -> torch.Tensor`
- **function `position_activations`** [L48-65]: `def position_activations(model, tokens, rows, positions, hooks=HOOKS) -> dict` decorators: @torch.no_grad() - ``{hook: [n, d]}`` at ``[i, positions[i]]`` of ``tokens[rows]`` (public forward).
- **function `next_symbol_probs`** [L69-74]: `def next_symbol_probs(model, tokens) -> np.ndarray` decorators: @torch.no_grad()
- **function `direct_two_step`** [L78-86]: `def direct_two_step(model, tokens, rows, positions, k: int = 2) -> np.ndarray` decorators: @torch.no_grad()
- **function `ar_two_step`** [L90-104]: `def ar_two_step(model, tokens, rows, positions) -> np.ndarray` decorators: @torch.no_grad() - ``q1(i | h) q1(j | h i)``: w_{t+1} := i, read at index t + 1; no renormalisation.
- **function `shuffle_perm`** [L107-108]: `def shuffle_perm(n: int, scope) -> np.ndarray`
- **function `window8_features`** [L111-114]: `def window8_features(tokens, rows, positions) -> np.ndarray`
- **function `fit`** [L117-134]: `def fit(X_cal, Y_cal, panel_cal, X_out, Y_out, family: str, rng_scope=()) -> dict` - Linear: nested_ridge unchanged. RBF: the x4f_gates.rbf_probe pattern (F = 2048).
- **function `pair_scores`** [L137-146]: `def pair_scores(J_a, J_b, q_a, q_b) -> dict`
- **function `_exact_J`** [L149-150]: `def _exact_J(h) -> np.ndarray`
- **function `behaviour_model`** [L153-174]: `def behaviour_model(model, H: int) -> dict` - Canonical pair and registered templates; direct (H >= 2) and AR routes (§9.2-9.3).
- **function `strata_rows`** [L177-185]: `def strata_rows(tokens, pool: str) -> dict` - {stratum: (rows, positions)} for t = 16, t = 28 and the three bins.
- **function `targets_for`** [L188-200]: `def targets_for(tokens, rows, pos) -> dict` - Probe targets and ceiling features at (rows, positions) (§3, §7.3).
- **function `contrasts`** [L203-208]: `def contrasts(law, J2_half, T2) -> tuple[np.ndarray, np.ndarray]` - (r, d) of §9.4: model two-step law minus J2_half, and T2, on the two A-B contrasts.
- **function `_hash`** [L211-212]: `def _hash(a) -> str`
- **function `model_pass`** [L215-247]: `def model_pass(model_id: str, model, H, data: dict, families=('linear',), shuffle=True, cells=None) -> tuple[dict, dict]` - One model's probe fits on cal -> test for every (stratum, target, hook) in ``cells``.
- **function `model_list`** [L250-256]: `def model_list() -> list[tuple[str, str, int, int]]` - (model id, run id, step, horizon): 12 C/M finals, 2 N finals, 4 step-0 init(s).
- **function `stage3_data`** [L259-269]: `def stage3_data(store_root=W.STORE) -> dict` - Tokens, strata rows, positions and targets for cal and test (stage 3 only).
- **function `_cells`** [L272-275]: `def _cells(kind: str) -> list`
- **function `collect_model`** [L278-317]: `def collect_model(mid, run, step, H, data, store_root=W.STORE) -> dict` - One model's stage-3 pass: linear fits (+ shuffle), band-edge and two-step laws.
- **function `pipeline_null`** [L320-334]: `def pipeline_null(model, store_root=W.STORE) -> dict` - Linear probe from resid_post_3 to the block tag Z_N: fit valN, score testN (§10.1).
- **function `oracle_fits`** [L337-362]: `def oracle_fits(data, store_root=W.STORE) -> dict` - window8 (one-hot w_{t-7..t}) and the oracle ceilings on test; positive control on val.
- **function `secondary`** [L365-381]: `def secondary(data, P, R, can, store_root=W.STORE) -> dict` - API §4 items 5 and 7 under the stage-3 budget: RBF at the primary cells, then the

