# Conventions

These rules are binding for every agent. They exist to keep the code readable, testable per module, parallel-buildable, and portable to another model or machine.

## 1. Environment

- **Python:** 3.10 or newer.
- **Core dependencies:** `numpy`, `scipy`, `torch`, `ripser`, `pyyaml`, `pytest`.
- **Optional dependencies:**
  - `gudhi`: cross-checks in tests, and the extension X3;
  - `matplotlib`: figures.
- Versions are pinned once, in wave W0, into `requirements.lock`, and the lock is recorded in `state/DECISIONS.md`. After that, version changes go through the conductor.
- **CPU-first.** Every module except `learner` and `activations` must run on CPU, and those two must also run on CPU, just slowly.

## 2. Repository layout

```
src/topo_pilot/<module>/
    __init__.py      # public API only (__all__); nothing else may be imported from outside
    SPEC.md          # contract (given; builders do not edit)
    README.md        # Purpose / Logic / Data / Public API / How to test (written by the builder)
    *.py             # internal files, at most 400 lines each
tests/<module>/
    TEST_PLAN.md     # given
    conftest.py      # module-local fixtures only
    test_*.py
tests/integration/   # cross-module; runs at gates only
configs/             # base.yaml, stages.yaml, extensions/*.yaml; local.yaml (untracked)
artifacts/           # content-addressed store (untracked; .gitignore)
tools/               # repo checks (see tools/SPEC.md)
state/               # PROGRESS.md (overwritten), DECISIONS.md (append-only)
```

Modules: `contracts, world, process, dataset, oracle, learner, activations, prediction, topology, analysis, experiment, executors`.

## 3. Object-oriented design rules

- **Values are frozen dataclasses.** Configs and artifacts are `@dataclass(frozen=True)`, and every artifact class has a `validate()` method.
- **Variation points are abstract base classes with registries.** Examples: `WorldBuilder`, `Metric`, `EmissionModel`, `CenterStrategy`, `Executor`, `ArtifactBackend`, and `Gate`. Adding a world family, emission mode, metric, or executor means adding a class and registering it. Existing classes are not edited.
- **Composition over inheritance.** Inheritance depth is at most 2: the ABC and its concrete class.
- **Dependency injection.** RNGs (`np.random.Generator` from `SeedTree`), the `ArtifactStore`, and executors are passed in as constructor or method arguments. No module-level singletons, no global mutable state, and no hidden I/O inside math classes.
- **Pure kernels.** Mathematical routines (filtering, distances, homology ranks) are pure functions or methods without side effects, so they can be tested in isolation.
- **Thin I/O layer.** Each module has at most one place that touches the artifact store. This is the `*Stage` or `*Service` class, and the experiment runner calls it.

## 4. Typing and docstrings

- Full type hints. Arrays use `numpy.typing.NDArray[np.float64]` and similar.
- Numpy-style docstrings. Every public object documents:
  - **Math:** the formula or definition it implements;
  - **Shapes:** for example `E: [N, V] float64, rows sum to 1`;
  - **Invariants** and **Raises:** the `StageFailure` codes.
- Each module README has a **Logic** section that explains the algorithm, why it is correct, and its edge cases. Formulas must match RESEARCH_SUMMARY notation.

## 5. Errors and logging

- Errors are `contracts.StageFailure(code, component, artifact_id, check, detail, recoverable)`, with codes from `contracts.ErrorCode`. Never use a bare `assert` for runtime checks.
- "Cannot decide" outcomes (`NONSEPARABLE`, `COLLAPSED`, `CENSORED`, `INCONCLUSIVE`) are **statuses** stored in results. They are not exceptions.
- Logging uses Python `logging`: INFO is one line per stage step, DEBUG is off by default. Never print arrays, and never write logs into `state/` or the docs.

## 6. Tests

- **Location and markers:** `tests/<module>/`. Every test file starts with `pytestmark = pytest.mark.<module>`. The extra markers are `slow`, `gpu`, and `integration`, all excluded by default via `pyproject.toml`.
- **Imports:** tests import only the module under test, `topo_pilot.contracts`, and `topo_pilot.contracts.testing` (shared tiny fixtures). They never import another module's internals, and they never read real artifacts.
- **Budget:** under 60 seconds per module suite on CPU.
- **Kinds required in every TEST_PLAN:**
  - contract tests for invariants;
  - a known-answer test (hand-computed values);
  - a property test where it applies, such as permutation invariance or scale covariance;
  - an error-path test for each error code the module raises.
- **What to run after a change:**

  ```bash
  python tools/affected_tests.py --changed <paths>
  ```

## 7. Data and artifacts

- All schemas are defined in `topo_pilot.contracts` and documented in `docs/DATA_SCHEMAS.md`. A module never invents an artifact type. If it needs a new one, it asks the conductor.
- **Identity:** artifacts are content-addressed (`artifact_id = sha256(canonical(type, config, parents, schema_version))[:16]`) and immutable. Writing an existing id verifies the checksum and skips the write.
- **Storage format:** metadata in JSON, arrays in a single `.npz` per artifact, torch state in `.pt`. Never use pickle for anything except torch state.

## 8. Git and commits

- One module per commit: `<module>: <what>` (for example `oracle: forward filter + futures`).
- Never commit `artifacts/`, `local.yaml`, notebooks with outputs, or anything larger than 5 MB.
- The conductor tags exit points: `E0`, `E1`, and so on.

## 9. Style

- `ruff` with the repository defaults. Line length is 100.
- Functions should stay under about 60 lines.
- No commented-out code.
- Names follow the math. Use `T`, `E`, `pi`, `b`, `q` only inside math kernels, where the docstring defines them. Elsewhere use descriptive names.
