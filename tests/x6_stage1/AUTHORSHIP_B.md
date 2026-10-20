# AUTHORSHIP_B: independent test author B (operations and cloud), X6S1 job 0069

**Protocol:** X6S1-FROZEN-v1 §14.3 (sha256 2A909ACE38231FBC6647E8FFDB5E6B5F22669A7C92182AE84240F32CD36EFB9E); contract `tools/x6_stage1/API.md` at commit d8cc373 (sha256 3c80e0f81c7af52a7ee0850e0bf93cf06500f4bc6796d741d1d55f9f8360c293).

**Author:** a separate clean-context subagent (agent id a97c557b125e6d7e9), launched by worker session b98609d8-a522-4406-94ee-5e30d7b6b142 with a short brief. It did not share context with author A or with the worker's API.md drafting. Tool uses: 122; subagent tokens: 422351.

**Assigned tests:** T-SEED, T-POOL, T-REG, T-TRAIN-EQUIV, T-CHAIN, T-INGEST, T-BUNDLE, T-NB, T-ENV, T-RESOURCE, T-S0, T-LINEAGE, T-ENV-LOCAL, T-METER, T-SIZE.

## Read (allowed inputs named in the brief)
- `tools/x6_stage1/PROTOCOL_X6S1_v1.md` (by section) and `tools/x6_stage1/API.md`.
- The reused production and reference code of protocol §14.2 field 1: `src/topo_pilot/**`, `tools/x6_stage0/*`, `tools/d2a/*` including the committed repair `tools/d2a/process_tree.py` (P = 0c341aa), `tools/k4b/k4b_registry.py`, `tools/k4b/k4b_registry_k.py`, `tools/c1prime_registry/*`.
- `tools/x4_oracle_profile/*` (winjob, meter, controls), `tests/d2a/test_process_tree_repair.py` (the committed repair's tests)
- `pyproject.toml` (pytest markers).

## Not read
- `tools/x6_stage1/*.py` and the notebook: they did not exist when the tests were written (the worktree held only API.md and the protocol copy under `tools/x6_stage1`), and the brief forbade reading, listing or searching them.
- The other author's test files; any store, pool, sealed file, K-REG2 itself, transcripts or the mailbox.

## Executed
- Nothing. The author used only read and write tools on the allowed paths and its own test files (author's report). It ran no Python, pytest or formatter.
- The worker afterwards compiled each file in memory (`ast.parse` + `compile`, no import, no run): all compile; every file ≤ 400 lines, LF line endings, lines ≤ 100 characters. No formatter was run over `tests/x6_stage1`.

## Files
test_b_seed_pool_reg.py (28 tests), test_b_train_chain.py (10), test_b_chain_ops.py (22), test_b_ingest_bundle.py (10), test_b_nb_s0_ops.py (19): 89 test functions.

## Notes
- The list of read files is as instructed and as reported by the author; the worker did not audit the subagent's transcript.
- API ambiguities reported by the author are recorded in `agent-handoff/jobs/0069/report.md`. Corrections to these files are made only by this author (§14.3).

## Correction round (job 0070)
- **Authority:** review of job 0069, ruling Q4 (no isolated S0 owner-authorisation check). The API.md erratum at commit d0e31d3 (sha256 e7403ad99bb3ed0dc58d197d1d9b19e75f87f85a6b163b71419f0f995c41178d) added `x6s1_run.auth_ok(store, protocol_sha256) -> bool`.
- **Author:** the same author-B subagent (agent id a97c557b125e6d7e9), resumed with SendMessage. Not a successor.
  - Phase 1 was read-only. The author reported the exact schemas its tests use, and these were recorded in API.md §13.1 B1–B16 (ruling Q3). It used 0 tool calls.
  - Phase 2 wrote the tests, with 20 tool calls.
- **Read:**
  - the amended API.md (§11.1, §13.1);
  - its own `test_b_*.py` files;
  - inputs allowed in job 0069.
- **Not read:** `tools/x6_stage1/*.py` (none exist), notebooks, `test_a_*`.
- **Executed:** nothing. No formatter was run.
- **Change:** `test_b_ingest_bundle.py` gains `test_auth_ok`, parametrised over synthetic `tmp_path` stores:
  - a valid record (upper-case stored hash, so the match must be case-insensitive);
  - a wrong protocol hash;
  - a missing field;
  - empty string, list and object, and a null field;
  - an absent file;
  - unparsable JSON;
  - a JSON array.

  Each case asserts `is True` or `is False`.
- **Compacted to make room (the author's own code only):** `_sha`, `_fsha`, `_cj`, `_remanifest`, `_put`, `_head`, `_ckpt_edit` and the module docstring.
- **Line counts:**

| File | Lines |
|---|---|
| `test_b_seed_pool_reg.py` | 398 |
| `test_b_train_chain.py` | 400 |
| `test_b_chain_ops.py` | 396 |
| `test_b_ingest_bundle.py` | 399 |
| `test_b_nb_s0_ops.py` | 400 |

- **The worker's check:** an in-memory compile only. The file compiles, uses LF line endings, and has no line over 100 characters. There are now 90 author-B test functions.

## Correction round (job 0072)
- **Authority:** review of job 0071, ruling R-0071-1, covering defects D1 and D2 in `test_b_seed_pool_reg.py`. The contract is API.md at bdbdab1, the erratum that sets 35 pools per protocol §6.1.
- **Author:** the same author-B subagent (agent a97c557b125e6d7e9), resumed with SendMessage. It used 8 tool calls.
- **Read:**
  - the D1 and D2 entries of `agent-handoff/jobs/0071/report.md` §5, and `jobs/0071/review.md`;
  - API.md and the protocol;
  - its own test file.
- **Not read:** `tools/x6_stage1/*.py`, `test_a_*`, and any job-0071 module code or diff.
- **Executed:** nothing. No formatter was run.
- **D1** (`test_pool_table_order_sizes_splits_names`): the assertion `len(sd.NONTEST_POOLS) == 33` became `== 32`, with the comment `# §6.1 (35 pools in all)`.
- **D2** (`test_data_streams_distinct_and_scoped`): the three counts of 36 became 35. These are the streams, the distinct streams and the distinct seeds.
- **Result:** the file is still 398 lines, with LF line endings. The worker compiled it in memory only.

## Correction round (job 0074, T-SIZE)
- **Authority:** `agent-handoff/planning/responses/X6S1-FROZEN-v1.coordinator-addendum-2.md` (coordinator addendum 2, sha256 cb851e26c6f1a12bfe8a6909928ff9024324487b3348f690ded90449359d562a), ruling R-0073-1 (§2) and consequent change §3(a). This is a protocol-driven amendment, not a test defect.
- **Author:** an author-B successor subagent with a clean context (not the original author a97c557b125e6d7e9).
- **Read:**
  - addendum 2, §2 and §3 only;
  - in `test_b_nb_s0_ops.py`, only `test_module_set_line_limits_and_test_files` (T-SIZE);
  - this file.
- **Not read:** `tools/x6_stage1/*.py` or any other module code, notebooks, other tests (`test_a_*` and the other `test_b_*` files).
- **Change** (`test_module_set_line_limits_and_test_files` only): the assertion `<= 400` for every module became the §2 limits. `x6s1_cloud.py`, `x6s1_registry.py`, `x6s1_ingest.py` and `x6s1_run.py` are each ≤ 560 lines, the other five ≤ 400, and the total over all nine ≤ 3,600. The line count is still `len(read_bytes().splitlines())`.
- **Compacted to make room (same function, same meaning):** the per-author test-file loop builds `mine` in its `for` header, and the test-file line-limit assertion is on one line (`REPO / "tests/x6_stage1"`).
- **Executed:** `python -m py_compile` (compiles) and `ruff check` (only the pre-existing I001 import-order finding at lines 25-30, also present at HEAD). No formatter and no pytest were run.
- **Result:** the file is still 400 lines, LF line endings, no BOM, longest line 99 characters.

## Correction round (job 0076, D-0075-1)
- **Authority:** `agent-handoff/jobs/0075/review.md`, ruling R-0075-1. D-0075-1 is a test defect: `[0] * 32` is X6-valid (vertex 0 has the lazy self-loop), so the module correctly keeps it.
- **Author:** an author-B successor subagent with a clean context (not the original author a97c557b125e6d7e9).
- **Read:**
  - `jobs/0075/review.md`, the section "Ruling R-0075-1";
  - in `test_b_seed_pool_reg.py`, `test_handoff_rows_keeps_x6_valid_lists` and the helper `_x6_rows`. The excerpt used to view them (lines 265-295) also showed `test_handoff_rows_malformed_json_is_incomplete`, `_scratch` and the first lines of `test_inventory_registered_copy_passes`;
  - this file.
- **Not read:** `tools/x6_stage1/*.py` or any other module code, notebooks, other tests (`test_a_*` and the other `test_b_*` files).
- **Change** (`test_handoff_rows_keeps_x6_valid_lists` only): the literal `"junk": [0] * 32` became `"junk": [0, 2] * 16`. This list is not X6-valid, because 0 → 2 is not an edge, so `x6_model.parse` rejects it. No other edit.
- **Executed:** `python -m py_compile` only (compiles). No formatter and no pytest were run.
- **Result:** the file is still 398 lines, LF line endings, no line over 100 characters.

## Correction round (job 0080, T-SIZE per addendum 3)
- **Authority:** `agent-handoff/planning/responses/X6S1-FROZEN-v1.coordinator-addendum-3.md` (coordinator addendum 3, sha256 fd1c7d501c7921505a494deb29325c58afab7a07b248803bd7ba8ee94c810fa3), ruling R-0079-1 (§2 item 2) and consequent change §4(a). This is a protocol-driven amendment, not a test defect.
- **Author:** an author-B successor subagent with a clean context (not the original author a97c557b125e6d7e9), brief `agent-handoff/jobs/0080/task.md`.
- **Read:**
  - addendum 3, §2 and §4 only (a heading list of the file was used to locate them);
  - in `test_b_nb_s0_ops.py`, `test_module_set_line_limits_and_test_files` (T-SIZE) and the definitions of the names it uses (`REPO`, `TOOL`, `sr`, and line 196, which defines `A, NOTES`). A `grep` used to locate them also listed the import lines and the `def` lines of the file (names only), and the excerpt used to view T-SIZE (lines 266-301) also showed the first lines of `FakeTree`;
  - this file.
- **Not read:** `tools/x6_stage1/*.py` or any other module code, notebooks, the bodies of other tests (`test_a_*`, the other `test_b_*` files and the other functions of this file).
- **Change** (`test_module_set_line_limits_and_test_files` only):
  - a local tuple `big = ("cloud", "registry", "ingest", "run", "stage_pre", "stage_post")`;
  - the module set is the eleven names, `big` plus data, pairs, stats, decide and eval. The `sorted(sr.MODULES)` equality stays;
  - each module in `big` is ≤ 560 lines, the other five ≤ 400, and the total over all modules ≤ 4,500 (was 3,600). The line count is still `len(read_bytes().splitlines())`.
  - The notes-file rule and the test-file rules (≤ 5 per author, names, ≤ 400 lines) are unchanged. The limit assertion now fits on one line, which makes room for `big`.
- **Executed:** `python -m py_compile` only (compiles). No formatter and no pytest were run.
- **Result:** the file is still 400 lines, LF line endings, no BOM, longest line 99 characters.

## Correction round (job 0083, T-SIZE per addendum 4)
- **Authority:** `agent-handoff/planning/responses/X6S1-FROZEN-v1.coordinator-addendum-4.md` (coordinator addendum 4, sha256 eabf5c69ece6b7b1b517866c7a7a9514a62d6989dcf61eb173d3665e80326129), ruling R-0082-0 (§2). This is a protocol-driven amendment, not a test defect.
- **Author:** an author-B successor subagent with a clean context (not the original author a97c557b125e6d7e9), brief `agent-handoff/jobs/0083/task.md`.
- **Read:**
  - addendum 4, §2 only (a heading list of the file was used to locate it);
  - in `test_b_nb_s0_ops.py`, only `test_module_set_line_limits_and_test_files` (T-SIZE). A `grep` used to locate it also listed the names of the next two `def` lines (`_quiet_controls`, `test_limits_and_resource_constants`), the excerpt used to view T-SIZE (lines 268-301) also showed the T-RESOURCE banner and the first lines of `FakeTree`, and the `git diff` context showed the `test_notebook_sha_binding` header line;
  - this file (its heading list and the rounds for jobs 0074, 0076 and 0080).
- **Not read:** `tools/x6_stage1/*.py` or any other module code, notebooks, the bodies of other tests (`test_a_*`, the other `test_b_*` files and the other functions of this file).
- **Change** (`test_module_set_line_limits_and_test_files` only):
  - `"eval"` joined the tuple `big` (the ≤ 560 group), which is now cloud, registry, ingest, run, stage_pre, stage_post and eval;
  - the module-set literal no longer lists `"eval"` separately, so the set is still the same eleven names with `eval` exactly once (through `big`). The `sorted(sr.MODULES)` equality stays;
  - the total over all modules is ≤ 4,800 (was 4,500). data, pairs, stats and decide stay ≤ 400. The line count is still `len(read_bytes().splitlines())`;
  - the notes-file rule and the test-file rules are unchanged. No other edit (the `# R-0079-1` comment on `big` is kept).
- **Executed:** `python -m py_compile` only (compiles). No formatter and no pytest were run.
- **Result:** the file is still 400 lines, LF line endings, no BOM, longest line 99 characters.
