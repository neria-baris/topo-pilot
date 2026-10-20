# `src/topo_pilot/experiment/x4b_run.py`

- Source: [src/topo_pilot/experiment/x4b_run.py](../../../../../../src/topo_pilot/experiment/x4b_run.py)
- Kind: python
- Lines: 337

## Module docstring

> X4 Phase B run (M7): orchestrate protocol x4b-v1, enforce the budget, export outputs.

## Imports

### Internal (repo files)

- `from topo_pilot.analysis import overall_verdict, practical_verdict, strict_verdict, tangent_audit` -> [src/topo_pilot/analysis/__init__.py](../analysis/__init__.py.md) (line 22, via package root)
- `from topo_pilot.contracts import ArtifactStore, EmissionSpec, LocalFSBackend, MetricRecords, MetricRow, OracleOutputs, ProcessDiagnostics, TransitionSpec` -> [src/topo_pilot/contracts/__init__.py](../contracts/__init__.py.md) (line 23, via package root)
- `from topo_pilot.oracle import BayesFilter` -> [src/topo_pilot/oracle/__init__.py](../oracle/__init__.py.md) (line 33, via package root)
- `from .config import load_config, producer_version` -> [src/topo_pilot/experiment/config.py](config.py.md) (line 35, via relative)
- `from .x4b import END, PROTOCOL_VERSION, S7_RECORDS, SEEDS, SHARED, ReadThroughBackend, build_pool, future_maps, index_tokens, map_failures, pool_checks, pool_failures, provenance_row, resolve_inputs` -> [src/topo_pilot/experiment/x4b.py](x4b.py.md) (line 36, via relative)
- `from .x4b_audit import agreement_check, agreement_failures, pool_audit` -> [src/topo_pilot/experiment/x4b_audit.py](x4b_audit.py.md) (line 52, via relative)

### External (third-party)

- `numpy` (lines 20)

### Standard library

- `__future__` (lines 8)
- `argparse` (lines 10)
- `csv` (lines 11)
- `ctypes` (lines 12)
- `hashlib` (lines 13)
- `json` (lines 14)
- `logging` (lines 15)
- `os` (lines 16)
- `pathlib` (lines 18)
- `resource` (lines 82)
- `time` (lines 17)

### Unresolved internal-looking imports

- none

### Ambiguous imports (several candidate files)

- none

### Dynamic imports

- none

### sys.path additions

- none

## Imported by

- [src/topo_pilot/experiment/circ_audit.py](circ_audit.py.md) (line 47, import)
- [src/topo_pilot/experiment/x4b2_run.py](x4b2_run.py.md) (line 61, import)
- [src/topo_pilot/experiment/x4f_run.py](x4f_run.py.md) (line 35, import)
- [src/topo_pilot/experiment/x5g1_main.py](x5g1_main.py.md) (line 30, import)
- [src/topo_pilot/experiment/x5g1_run.py](x5g1_run.py.md) (line 40, import)
- [src/topo_pilot/experiment/x5g1_scorebench.py](x5g1_scorebench.py.md) (line 36, import)
- [src/topo_pilot/experiment/x5g1_verify.py](x5g1_verify.py.md) (line 44, import)
- [src/topo_pilot/experiment/x5g1t_runtime.py](x5g1t_runtime.py.md) (line 22, import)
- [src/topo_pilot/experiment/x5g1t_stages.py](x5g1t_stages.py.md) (line 37, import)
- [tests/experiment/test_x5g1t_runtime_boundary.py](../../../tests/experiment/test_x5g1t_runtime_boundary.py.md) (line 19, import)

## Top-level constants

- `CPU_CAP_S`
- `PROTOCOL_DOC`

## Classes and functions

- **class `BudgetExceeded(RuntimeError)`** [L59-60] - The 1 CPU-hour cap of protocol §9 was reached.
- **function `peak_memory_bytes`** [L63-85]: `def peak_memory_bytes() -> int | None` - Peak working set of this process (Windows) or max RSS (POSIX); None if unavailable.
- **function `listing_hash`** [L88-97]: `def listing_hash(root: Path) -> tuple[str, int]` - sha256 over sorted (relative path, size, mtime_ns) of every file under ``root``.
- **function `_sha256`** [L100-101]: `def _sha256(path: Path) -> str`
- **class `Budget`** [L104-116] - Process CPU time since construction, checked between steps.
- **method `Budget.__init__`** [L107-108]: `def __init__(self, cap_s: float = CPU_CAP_S) -> None`
- **method `Budget.check`** [L110-116]: `def check(self, step: str) -> None`
- **function `_ambient_json`** [L119-126]: `def _ambient_json(audit) -> dict`
- **function `_load_process`** [L129-138]: `def _load_process(main: ArtifactStore, inputs: dict) -> dict`
- **function `_maps_section`** [L141-160]: `def _maps_section(main: ArtifactStore, inputs: dict, proc: dict) -> tuple[dict, dict, list]`
- **function `_pools`** [L163-175]: `def _pools(main: ArtifactStore, inputs: dict, proc: dict, maps: dict) -> tuple[dict, dict]`
- **function `_metric_rows`** [L178-197]: `def _metric_rows(ambient, results: dict, verdicts: dict, parents: tuple) -> list[MetricRow]`
- **function `run_phase_b`** [L200-254]: `def run_phase_b(repo_root: Path, main_root: Path, out_root: Path, tables: Path) -> dict` - Run protocol x4b-v1 once; write tables/exports; return the verdict summary.
- **function `_export`** [L257-312]: `def _export(repo_root, main_root, out_root, tables, inputs, main, proc, map_checks, ambient, amb_runs, pool_chk, results, agreement, pools, summary, budget, before, after)`
- **function `main`** [L315-333]: `def main(argv: list[str] | None = None) -> int`

