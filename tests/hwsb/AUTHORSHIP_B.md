# Authorship record: independent test author B, job 0161

**Author:** Claude subagent (clean context), assigned as author B by coordinator Claude db858736.
**Worktree:** `X:/Downloads/projects/topo-pilot/topo-pilot-hws`, branch `hwsb-impl`, base 8407a76.

## Files written (author B only)
- `tests/hwsb/test_b_streams.py` (50 tests): streams and sequence IDs, refusals, DRB4, sampler spy and planted defects, canonical/named maps, hist blocks, H2-B (DRB16).
- `tests/hwsb/test_b_process.py` (11): `build_process` identities (KB1), `arrays_sha256`, `spec_checksums`, IDENTITY failures, tiny process.
- `tests/hwsb/test_b_e4path.py` (28): recipe check (DRB3), `train` vs `LearnerStage` (DRB2-type), `CheckpointSaver`/`SentinelStop`, DRB6, threads, torch lock.
- `tests/hwsb/test_b_hold.py` (14): `hold_check`, `HoldRule`, held and stopped tiny trainings (DRB14).
- `tests/hwsb/test_b_records.py` (31): `pause_check`, study ledger, AUTH/SCHED, inventory snapshot/diff, G0 classification and search (DRB15), FREEZE on a synthetic repo, dry-run refusal.
- `tests/hwsb/test_b_registry.py` (16): `history_inventory`, `registry_digests`, `b9a` (DRB13).
- `tests/hwsb/test_b_meter_law.py` (20): meter binding and placement (DRB13b), independent B8a enclosure test with exact rational exp bounds (OPEN-3), `law_bound` on w*, w(3/2), w0, state restoration (DRB12).

## What I read
- `agent-handoff/jobs/0161/task.md`, `agent-handoff/jobs/0161/rulings-phase1.md`.
- `tools/hwsb/PROTOCOL_HWSB_v1.md` (not opened; API/CONTRACT/TEST_PLAN sufficed), `tools/hwsb/API.md`, `tools/hwsb/CONTRACT.json` (all top-level keys, via a JSON load), `tools/hwsb/TEST_PLAN.md`.
- Reused production code: `src/topo_pilot/dataset/{stage,checks,config,public,__init__}.py`, `src/topo_pilot/learner/{stage,config,trainer,__init__}.py`, `src/topo_pilot/activations/_extractor.py`, `src/topo_pilot/contracts/{__init__,base,store}.py` (parts), `_schemas_data.py` (HistoryIndex), `_schemas_world.py` (EmissionSpec).
- Reused tools: `tools/x4_circle_history/process_law.py`, `scores.py` (parts), `tools/c1prime/c1_model.py`, `tools/hws/{hws_driver,hws_worlds,hws_exact}.py` (parts), `tools/hws/CONTRACT.json` (seeds), `tools/k4b/{k4b_registry,k4b_registry_k,k4b_data}.py` (parts).
- Earlier tests for patterns: `tests/hws/test_b_records.py`, `tests/hws/test_b_kc1.py`, `tests/hws/AUTHORSHIP_B.md`.
- Metadata only: `topo-pilot/artifacts/Checkpoint/c3358e3cb9c352fb/{extra.json,meta.json}` (JSON; `payload.npz` and `state.pt` were listed by `ls` but never opened).
- `requirements.lock` (the `torch==` line).

## What I did not read
- No `tools/hwsb/*.py` file was opened, searched or read. I listed the directory (`ls tools/hwsb`) three times to see which modules existed, and I imported the modules by running the tests.
- Tests were run with `--tb=line` to avoid printing implementation source. Incidental exposure: one traceback line naming `hwsb_data.py:161 IndexError` (an out-of-range planted token reached `perm[...]` before `check_ranges`; I changed the planted defect to an out-of-range state), and a returned value `{'status': 'REFUSED', 'reason': 'P-SCHED rule 2 not met'}` from `run_dry` (I widened the accepted refusal forms; see SPEC-QUESTION in the file).
- No `tests/hwsb/test_a_*` file and no `AUTHORSHIP_A.md`.
- No `00_READ_ME_FIRST*` path and nothing under `docs/research_summary/`.
- No payload of any store: no `payload.npz`, `state.pt`, `sealed/` or `hist/` of a real store was opened or hashed. The only npz files written are synthetic ones under pytest `tmp_path`.

## What I executed
- pytest on my own seven files with `--basetemp X:/Downloads/topo-scratch/test_hwsb-0161/B/pytest*`, TEMP/TMP at `X:/Downloads/topo-scratch/test_hwsb-0161/B/tmp`, venv python with `-s` and `PYTHONPATH=<worktree>/src`. Final run against the implementation as it stood: 170 passed. Nothing was written under `X:/Downloads/projects/topo-pilot/` except the test files themselves.
- While `hwsb_dry.py` was missing or still incomplete I used a scratch stub of `build_tiny_process` (in `X:/Downloads/topo-scratch/test_hwsb-0161/B/stub/`, never committed) to check my test logic.
- Expected values come from the protocol, API, CONTRACT, the reused modules and independent recomputation in the tests (exact Fraction exp bounds for B8a; hashes of arrays; `LearnerStage` as reference).
