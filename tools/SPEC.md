# SPEC: `tools/` (repository checks; built in W0 by Tier C, reviewed by the conductor)

Small standalone scripts (standard library only), each under 150 lines, each with a `--help`.

| Script | Behaviour |
|---|---|
| `affected_tests.py --changed <paths...>` | Prints the minimal list of test folders to run. Rules: a path inside `src/topo_pilot/<m>/` maps to `tests/<m>`. If the module's public API changed (detected by diffing the `__all__` names and signatures of `<m>/__init__.py` against `HEAD`), it also maps to `tests/<d>` for each direct dependent `d`, read from `DEPENDENTS` below. `src/topo_pilot/contracts/` maps to all module suites. `configs/`, `docs/`, and `state/` map to nothing. Prints a ready-to-run `python -m pytest ... -q` command |
| `check_imports.py` | Parses the AST of `src/`. Fails on: (1) imports of another module's internals (anything deeper than `topo_pilot.<m>`); (2) the leakage rules: `learner` and `activations` must not import `world`, `process`, `oracle`, `analysis`, or `prediction`; `topology` must not import any project module except `contracts`; `executors` must not import science modules; (3) `contracts.testing` imported from `src/` |
| `check_file_sizes.py` | Fails if any `.py` file exceeds 400 lines or any tracked file exceeds 5 MB |
| `check_process_rebuild.py [--root artifacts]` | Rebuilds every stored `TransitionSpec` and `EmissionSpec` from its stored parent world and config into a memory store; fails unless every rebuilt id and `payload_sha256` equal the stored ones (regression check for `process` changes; read-only) |
| `check_state_files.py` | Fails if `state/PROGRESS.md` exceeds 80 lines, if `state/DECISIONS.md` has malformed lines, or if transcript-like files (`*transcript*`, `*chat*`, `*.log`) are tracked |

**Direct dependents**, used by `affected_tests.py`:

```text
contracts   -> all
world       -> process, analysis
process     -> dataset, oracle, analysis
dataset     -> learner, activations
oracle      -> prediction, analysis
learner     -> activations
activations -> prediction, analysis
prediction  -> experiment
topology    -> analysis
analysis    -> experiment
executors   -> experiment
experiment  -> (none)
(additionally, every module -> experiment, because experiment wires all *Stage classes)
```

**Make targets** (in `Makefile`):

| Target | Runs |
|---|---|
| `make test m=<module>` | `python -m pytest tests/<module> -q` |
| `make affected` | `affected_tests.py --changed $(git diff --name-only HEAD)` |
| `make checks` | the three `check_*` scripts |
| `make reproduce-figures` | `topo-pilot report` |
