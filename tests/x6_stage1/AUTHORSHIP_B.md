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
