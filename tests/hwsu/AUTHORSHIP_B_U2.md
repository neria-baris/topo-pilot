# Test author B, job 0223 (HWSU phase 2, response family only): records and registry side

Author: Claude (Opus 5.5) subagent, 2026-11-03. A clean-context author, distinct from the implementer and from author A.

## What I read

- `jobs/0223/task.md` and `jobs/0223/RULINGS.md` (R-0223-1..6).
- `tools/hwsu/PROTOCOL_HWSU_v1.md` (by reference through the API), `API_U2.md`, `API.md` (phase 1, including the J11 obligation erratum), `CONTRACT_OF.json`, `CONTRACT.json`, `TEST_PLAN_U2.md`, `TEST_PLAN.md` (phase 1, rows only).
- Phase-1 test files of author B (`test_b_of_bind.py`, `test_b_of_freeze.py`, `test_b_of_meter.py`) as style templates.
- Public APIs of reused modules: `k4b_data.history_table`/`digests`, `hwsc_registry.source_own`, `hwsc_gates.expected_meta_c` and `c2_model` (signatures), the `c2_readout` tiny-model fixture pattern (`tests/c2_readout/test_b_patch.py`).

## What I did not read

- `tools/hwsu/*.py` and `tools/hwsu/u2/*.py` (never opened; the implementer worked in parallel). Two incidental traceback lines of the implementation (file and line of a call frame) were shown by pytest output; no code was read from them.
- Author A's `tests/hwsu/test_a_*` and `AUTHORSHIP_A*.md`; the public research-summary paths; blinded stage-C paths; track-D round files and reports.
- Real stores: only the JSON/hash reads of `hwsu-store/OF_ACCEPT.json`, `hwsu-store/FREEZE_OF.json` and the `hwsc-store` records listed in CONTRACT `stage_c_u2` (`FREEZE.json`, `STAGES.jsonl`, `PRODUCTION_FROZEN.json`, the three TRAIN_RECORDs, `OBS_INVENTORY.json`, `registry/K-REG2.json`) were hashed; never an array, `payload.npz`, `state.pt`, `sealed/` or `HIST_*`.

## Footprint

Every store, root, mailbox fixture and array is under pytest `tmp_path` (basetemp `X:/Downloads/topo-scratch/test_hwsu-0223/b/pytest`, TEMP/TMP/TMPDIR under `X:/Downloads/topo-scratch/test_hwsu-0223/`). The only git use is read-only (`ls-tree`, `cat-file`, `diff`, `rev-parse`) on this worktree. The freeze tests write FREEZE.json only into a tmp copy of the store. No formatter was run; the only mechanical edit was adding `# noqa: E501` to long lines.

## Files and coverage (TEST_PLAN_U2 section 3 rows)

| File | Covers |
|---|---|
| `test_b_u2_contract.py` | `contract_of_sha256`; loader union without override (and refusals for a wrong hash / an override); every phase-2 key new; merged phase-1 leaves unchanged; `reuse_sha256_u2` disjoint; U2 memory caps; unchanged name rule (`ACTS_` refused); `phase2_files` |
| `test_b_u2_binding.py` | `read_train_record` (drops `dev_ce`, BOM, missing key), `stage_complete_sha`, `identity_c` refusals (CONTRACT hash, STAGE_COMPLETE hash, status, id, exclusion), `charts_identity` (no `np.load`, off-by-one byte, gauges, PRODUCTION_FROZEN re-hash), `load_stage_c` one-thread rule, real hashes of stage-C records |
| `test_b_u2_of_binding.py` | R-0206-1 `of_binding` on fixtures (PASS and every refusal: freeze_of hash both ways, OF_ACCEPT bytes, outcome, verdict, N_resp, missing file) and the real records |
| `test_b_u2_audit.py` | `audit_u2` on planted modules (never-called names, unlisted names, from-imports, C2 seed default), `train`/`make_train_dev_c` only from `hwsu_dry2`, read audit by contract mutation (unlisted read, extra read, no conditional entry, foreign forbidden read, `ast_refs` mismatch, ImportError not swallowed), `u2_files`, phase-1 globs never see `u2/`, `reads_by_path` equals `ast_refs` without importing (subprocess) |
| `test_b_u2_freeze.py` | `implementation_files_u`, `freeze_u` fields and refusals (nothing written), `verify_freeze_u` (absent, phase-2 file hash, reuse tables), `s0_u` refusal on a phase-1 diff and acceptance of the real diff |
| `test_b_u2_registry.py` | `source_hwsc` (planted S3/S7 tables, sha mismatch, missing, unlisted, digest column, zero opens of Checkpoint payload and `sealed/`), `source_kreg2_c`, `superset_diagnostic` (chunk-invariant, head cap), `source_own_u`, `source_own_dry`, `inventory_u` (R8, root-table rows) |
| `test_b_u2_hwsd.py` | `source_hwsd` (absent, no obligation, known-case only, listed history reader, unlisted chart, newest governs both ways, `hwsd-dry*`), `read_obligation_u2` with each obligation's own `name_rules`, only obligation/reservation/END files opened, R-0213-1 `end_obligation_path` (store-relative, root-relative inside the store, store wins, outside refused) and `w2_attestation_u2` |
| `test_b_u2_records.py` | `write_sealed_u` / `check_unsealed_u` / `SEALED_KEYS_U`, share-dropped entry points, `run_gates_u` continuing through `NOT_RUN/SHARE_DROPPED`, phase-1-prefix arrays and obligations, stopped drawing job and `RES-HWSU-U-a2`, `memory_cap_u2`, `job_paths_u2`, DRU paths outside the root (R-0213-2), `meter_main` cap and measure-only argv, `run_dru` refusals |
| `test_b_u2_dx_policy.py` | `UPolicy` (order, nesting, allowed kinds, T-PRE gate for the endpoint), `m0_u` on a 4-layer d128 random model (PASS, wrong state sha, wrong id, attainability-only) |

## Spec ambiguities and judgement calls (for the coordinator)

1. **Obligation shape.** TEST_PLAN_U2 and API_U2 5.3 speak of "basis `name_rule`" and the phase-1 `n_history_files`; the J11 erratum fixes the real form (`name_rules`, `class`, `reader`, `basis`). The tests use the J11 form.
2. **`identity_c` with an excluded id** cannot be isolated on a synthetic store (the checkpoint-meta step fails first); the test asserts IDENTITY only.
3. **`write_sealed_u(store, arrays)` key layout** is not fixed: I pass `A_<j>`, `ZR010_<j>`, `ZR030_<j>` and `G`, and expect `theta_<j>` = mean A_j / mean G.
4. **`x1_gate` and `validation_report` inputs** (`val`, `ctx`) are not fixed by API_U2, so they are not unit-tested here (DRU1 covers them); `load_stage_c` is tested only for the thread rule.
5. **`freeze_u` has no `contract` argument**, so freeze tests run against this worktree (HEAD) with tmp copies of the real OF records; they cannot pass until every phase-2 file is committed.
6. **`hwsu_bind._default_files`** (named in TEST_PLAN_U2) is probed by two possible attribute names; the real guarantee tested is that `audit()` passes and no CONTRACT phase-1 file is under `u2/`.
7. Stage-C TRAIN_RECORD fixtures need `checksums["5000"]` (read by the reused `expected_meta_c`).
