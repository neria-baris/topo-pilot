# Authorship record: independent test author B (job 0101)

**Author:** a clean-context Claude subagent, independent test author B for C2 (C2-FROZEN-v1 §13.3), launched by coordinator session dcecc9ff. **Scope:** model, gates and operations (TEST_PLAN.md §3). **Worktree:** `X:/Downloads/projects/topo-pilot/topo-pilot-c2`, branch `c2-0100`, base 018c608.

## Files written (only these)
| File | §13.3 items |
|---|---|
| `test_b_patch.py` | T-PATCH, T-X1 |
| `test_b_fwl_l1.py` | T-FWL, T-L1 |
| `test_b_screens.py` | T-R1, T-N2, T-CMODE |
| `test_b_policy.py` | T-POLICY, T-SEED, T-SIZE, T-METER |
| `test_b_registry.py` | T-REG, T-NAMESPACE |
| `test_b_lineage.py` | T-G0, T-LINEAGE |

## What was read
- `agent-handoff/jobs/0101/task.md` (the dispatch).
- `tools/c2_readout/PROTOCOL_C2_v1.md`: §0–§2.12, §3, §4, §5, §6.1–§6.2 and §6.4–§11, §13; the heading list of the rest.
- `tools/c2_readout/API.md`, `tools/c2_readout/CONTRACT.json`, `tools/c2_readout/TEST_PLAN.md`, all in full.
- Reused production code (protocol §13.1 and `hashes.reused_extra`), for signatures and behaviour only:
  - `src/topo_pilot/learner/{patch.py, model.py, config.py, __init__.py}`;
  - `src/topo_pilot/experiment/x4f_probe.py` (`nested_ridge`), `src/topo_pilot/prediction/ridge.py` (`RidgeProbe`), `src/topo_pilot/analysis/x4f_scores.py` (`standardizer`, `ledoit_wolf`);
  - `src/topo_pilot/dataset/checks.py` (`check_disjoint`, `process_code`/`make_sequence_ids` signatures), `src/topo_pilot/contracts/ids.py` (`SeedTree`);
  - `tools/c1prime/{c1_model, c1_fit, c1_gates, c1_config}.py` in full; `c1_data.py`, `c1_records.py`, `c1_means.py` and `c1_oracle.py` in part;
  - `tools/k4b/k4b_registry.py`, `k4b_registry_k.py`, and the predicate part of `k4b_data.py`;
  - `tools/x6_stage1/x6s1_registry.py` (digests, `DigestSet`, headers, `open_reg`, `_write_reg`);
  - `tools/x4_circle_history/stage_records.py`, and `scores.history_digests`.
- Repository metadata: `git log`/`git status` of the worktree, line counts of the four contract documents.

## What was not read
- `tools/c2_readout/*.py`: never read, listed or searched (none existed). Only `test_b_policy.py::test_module_set_and_400_line_limit` lists that directory, at test run time.
- Author A's files (`tests/c2_readout/test_a_*.py`, `AUTHORSHIP_A.md`).
- The contents of `tests/c1prime` (its file names were listed once, and nothing more).
- `topo-pilot/00_READ_ME_FIRST_*` and `docs/research_summary/`.
- Any store payload or store file, any checkpoint, the job-0100 rulings and every other mailbox file except this job's `task.md`.

## What was executed
- No test, module or stage was run.
- The only Python executed: an in-memory `ast.parse` + `compile` of the six test files with `X:/Downloads/projects/topo-pilot/topo-pilot/.venv/Scripts/python.exe -s`.
- Shell inspection and editing of this author's own files only:
  - `wc`, `grep`, `sed`, `awk` and `od`;
  - line-length and CR checks;
  - converting CRLF to LF;
  - wrapping three long lines.
- No formatter was run.

## Fixtures
- All fixtures are synthetic:
  - a tiny float64 `TransformerLM` built from `ModelConfig`;
  - seeded Gaussian designs;
  - synthetic stores, registries, mailboxes, X6-style stores and project roots under pytest's `tmp_path`.
- The registry, namespace and G0 tests redirect the `c2_config` path constants (and `CONTRACT["paths"]`) into `tmp_path`, so no real store is opened or hashed.
- The G0 binding tests hash only the repository's own pinned code and documents, at run time.

## Correction round (0102 review)
- Requested by coordinator dcecc9ff. The coordinator's message was read, and so was `agent-handoff/planning/responses/C2-FROZEN-v1.coordinator-addendum-2.md` §E-0102-1.
- **`test_b_registry.py`:** `test_namespace_unrelated_collision_is_lineage` now gives its parametrize short explicit `ids`. Before, the 1 MiB payload ended up in the test id and in `PYTEST_CURRENT_TEST`, beyond the Windows environment limit. The cases themselves are unchanged.
- **`test_b_lineage.py`:** the `errors.py` expectation now uses the full binding hash `8aa309c4…eb99f`. Addendum 2 (E-0102-1) rules that the protocol's abbreviation "…f99f" is a typo.
- **Executed:** only an in-memory `ast.parse` + `compile` again. No formatter was run, and `tools/c2_readout/*.py` was not read.

## Amendment (coordinator addendum 3, R-0103-1)
- **Driven by the protocol, not a test defect.** Requested by coordinator dcecc9ff. The author read `agent-handoff/planning/responses/C2-FROZEN-v1.coordinator-addendum-3.md`, ruling R-0103-1.
- **`test_b_policy.py`:** the T-SIZE module set is now 12 modules: the previous 10 plus `c2_stage_pre.py` and `c2_stage_post.py`. Each module is limited to 400 lines, with a total ceiling of 4,800 lines.
- **Executed:** only an in-memory `ast.parse` + `compile`. No formatter was run, and `tools/c2_readout/*.py` was not read.
