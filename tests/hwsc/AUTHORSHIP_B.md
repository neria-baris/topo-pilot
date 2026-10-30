# Author B (job 0176): authorship record

Independent test author B, clean context, for HWS stage C (`tools/hwsc`, HWSC-DESIGN-v1). Scope: TEST_PLAN.md section 3, plus coordinator ruling R-0176-P10 (`agent-handoff/jobs/0176/RULINGS_PHASE2.md`).

## Files

| File | Tests (collected) | Covers |
|---|---|---|
| `test_b_binding.py` | 34 | `cc` constants; `cb.decode`, `load_table` (21 rows; identity; dry), `check_old`, `bound_stage_c` (identity restore, exception, nesting, drift), `audit` (planted globals, dict keys, `__defaults__`/`__kwdefaults__`, methods, staticmethod, dataclass field, Path/str paths, nested strings, seed dict, bool, foreign functions, top-name coverage), KC7-type stream check (DRC3) |
| `test_b_streams.py` | 35 | `HWSC_PLAN`, `cc.dry_plan`, `cc.run_key`; `cd.sequence_ids_c` real/dry and refusals; DRC4 mirror (`make_train_dev_c` against `hwsb_data.make_train_dev`); `block_generator`, `block_ids`, `sample_block_c` (bitwise vs `k4b_data.sample_block`, one sampler call); `hist_name`; `save_table`; H2 `cd.separation_c` (moved here from `test_b_registry2.py` for the 400-line limit) |
| `test_b_registry.py` | 19 | R2 `source_c2nd`, R4 `source_hwsb`, R5 `source_dry` (DRB13-style store, planted fixture, canonical ObservationSet digests by the EmissionSpec parent's `symbol_perm`, missing parent, `hwsb-dry*` glob, `test_*` not pruned), R7 `source_own` |
| `test_b_registry2.py` | 23 | R6 `scratch_scan`/`scratch_check` (pruning, classes, header-only reads, R-0176-G9 stage-B folders, empty rows, fixture rows), R8 `inventory_c`, `cr.build` with stub sources (Registry.load round trip, status precedence, extra, REHEARSAL, exclusivity), H2-FRESH `cd.h2_fresh_c` |
| `test_b_records.py` | 59 | `cdr.status_of`, `run_gates_c`, `lineage_c`, `auth_ok` (refusals), `sched_ok`, the study ledger, `pause_check_c`, `pause_or_raise_c`, D6 `export_c` (RESULT.json annotations, licence, disclosure; SEALED_OPENED.json; one S8 STAGE_COMPLETE), `k4b_stats.check_unsealed` under the binding, `cc.load_handoff` (DRC10, DRC12) |
| `test_b_train_hold.py` | 15 | `cdr.run_train` with spies (plan, master, HoldRule cap 6,006.6282 / 5,000 / 1,000, bound run key, RERUN, KC_ACCEPT, owner STOP, NONFINITE); the hold with the stage-C constants (from step 1,000, strict, CONTINUE, STOP); a tiny held-and-continued training equal bitwise to an unheld one; R-0176-P10: a failing `BINDING_AUDIT` stops E2, REG2, KC and TRAIN |
| `test_b_guard_meter.py` | 74 | `cc.blinded` (exactly the five R-0176-G1 rules, case, separators), `public_summary`, `guard`/`read_json`/`read_bytes` (refuse before any open), `ck.needle_in`, `seed_search_c` (pruning, never opens blinded fixtures, equality with `hws_driver.seed_search`), `classify_hits_c`, the meter binding (`bind`, `memory_cap`, `job_paths`, `placement_ok`, `effective_settings`, `main` exit codes 2 and 3), suite placement (DRC11, DRC13, DRC14) |

## What I read

- `agent-handoff/jobs/0176/task.md` (sha256 4A697742…4A12, verified), `agent-handoff/jobs/0176/RULINGS_PHASE2.md` (the R-0176-P10 entry), `topo-pilot-hws/CLAUDE.md`.
- `tools/hwsc/PROTOCOL_HWSC_v1.md` (by reference through API.md/TEST_PLAN.md), `tools/hwsc/API.md`, `tools/hwsc/CONTRACT.json`, `tools/hwsc/TEST_PLAN.md` at 70e8e27.
- Reused modules' public documents: `tools/hwsb/API.md`, `tools/k4b/API.md` (sections 2, 3, 12, 13), `tools/c2_readout/API.md` (sections 5, 16.3).
- Reused modules' signatures and docstrings (`inspect`), and these reused function bodies to learn their call shapes: `c2_registry.Registry` (`load`, `_x6`, `contains`, `_x6_manifest`, `_ok_readers`, `_violation`), `nd_registry` (`inventory`, `build`, `_new`), `x6s1_registry._headers`/`_history_bearing`, `hws_driver.seed_search`/`_needle_in`, `hwsb_driver.pause_or_raise`/`run_train`/`_json`, `hwsb_meter_bind.placement_ok`, `k4b_fresh.sample_test`/`h2_fresh`, `k4b_release.archive_attempt`.
- Probes of reused functions on scratch data under `X:/Downloads/topo-scratch/test_hwsc-0176/authorB/` (stage-B tiny stores, reservations, `complete_stage`, `history_table`, `record_gate`).
- The real `hwsb-store/HANDOFF.json` (through `cc.load_handoff` in a test, and as bytes to make modified copies under tmp_path), as allowed.

## What I did not read

- I did **not** read, list or search `tools/hwsc/*.py` (the code under test). When my own tests failed, I read only pytest's failure output. That output named the files and line numbers of some frames (`hwsc_driver.py`, `hwsc_jobs.py`, `hwsc_records.py`, `hwsc_data.py`) and the `GATES.jsonl` records my synthetic stores produced. I did not open those files.
- I did **not** read `tests/hwsc/test_a_*` (author A), `tests/k4b`, `tests/hwsb`, the public research-summary paths, `hwsb-store/REPORT.json`, `hwsb-store/stages/EVAL/`, `hwsb-store/GATES.jsonl`, `hwsb-store/CHART_CONSTRUCTIONS_*.json` or `agent-handoff/jobs/0175/`. I opened no `payload.npz`, `state.pt`, `sealed/` or `hist/**` array of any real store.

## Hygiene

- Every store, root and fixture is under pytest's `tmp_path`. My runs used `--basetemp X:/Downloads/topo-scratch/test_hwsc-0176/authorB/pytest`, TEMP/TMP/TMPDIR under `…/authorB/tmp`, `PYTHONPATH=<worktree>/src` and `python -s`. No array file is written under the project root, and no `.npz`/`.npy` is committed.
- The R5 tests install an audit hook that refuses any open or listing of the real `X:/Downloads/topo-scratch/hws*` dry stores, so a default-path fallback cannot read them.
- No formatter was run. `ruff check` passes on my files. Each file has at most 400 lines.
