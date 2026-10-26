# Authorship record, independent test author B (job 0121)

Author: Claude subagent (author B), clean context, 2026-10-26. Worktree `topo-pilot-c2nd`, branch
`c2nd-impl` from 28e54b4. Assignment: T-DECOY-EXACT, KM1-KM4, T-RESP, T-POLICY-ND, T-SEAL-ND,
T-REG-ND (with R-0116-3 and R-0116-4), T-NAMESPACE-ND, T-G0-ND, T-METER, T-SIZE.

## Files written (only these)

| File | Items |
|---|---|
| `tests/c2_nd/test_b_decoy_model.py` | T-DECOY-EXACT |
| `tests/c2_nd/test_b_layer2.py` | KM1-KM4, T-RESP (with ORACLE-FEAS (i)) |
| `tests/c2_nd/test_b_policy.py` | T-POLICY-ND, T-SEAL-ND |
| `tests/c2_nd/test_b_registry.py` | T-REG-ND |
| `tests/c2_nd/test_b_lineage.py` | T-NAMESPACE-ND (moved here from the registry file for the 400-line budget; TEST_PLAN §4 allows a split over the author's own files), T-G0-ND, T-METER, T-SIZE |
| `tests/c2_nd/AUTHORSHIP_B.md` | this record |

## What I read

- `agent-handoff/jobs/0121/task.md`; `agent-handoff/jobs/0116/review.md` (rulings R-0116-1..5,
  erratum E-C2ND-1).
- `tools/c2_nd/PROTOCOL_C2ND_v1.md`: §2.1-§2.10, §3, §4.1-§4.6, §5, §6, §9-§12 (and the
  section headings). `tools/c2_nd/API.md` (whole), `tools/c2_nd/CONTRACT.json` (whole),
  `tools/c2_nd/TEST_PLAN.md` (whole).
- Reused production code, read-only, excerpts only: `src/topo_pilot/learner/{model.py, patch.py,
  config.py, __init__.py}`, `src/topo_pilot/dataset/checks.py` (`check_disjoint`), `grep` hits
  for `process_code`, `make_sequence_ids`, `SeedTree`; `tools/c2_readout/{c2_model.py,
  c2_attrib.py, c2_decide.py, c2_driver.py, c2_data.py, c2_registry.py, c2_config.py}`;
  `tools/c1prime/{c1_endpoint.py, c1_means.py, c1_oracle.py, c1_records.py, c1_model.py}`;
  `tools/x4_circle_history/{stage_records.py, scores.py}`; `tools/x6_stage1/x6s1_registry.py`
  (`row_digests`, `hex_to_digests`, `_headers`, `_history_bearing`); `tools/k4b/k4b_registry.py`
  (`inventory`, `classify`), `k4b_data.predicate_check`, `k4b_registry_k.HISTORY_KEYS`;
  the pytest section of `pyproject.toml`; the directory names under `tests/`.

## What I did not read

- No file `tools/c2_nd/*.py`: none was read, listed or searched (one `ls` named only
  `tools/c2_nd/*.md` and `tools/c2_nd/*.json`). `test_b_lineage.py` lists that directory at run
  time only (T-SIZE).
- No store (`c2-readout-store`, `c2nd-store`, any other `*-store`), no scratch history, no
  payload, checkpoint or `sealed/` file.
- No other test file (neither author A's `test_a_*.py` nor `tests/c2_readout`).
- Never `00_READ_ME_FIRST*` or `docs/research_summary/`.

## What I executed

- No test, no pytest, no import of project code.
- `python -I X:/Downloads/topo-scratch/0121b/check_b.py <my files>`: `ast.parse` + `compile` of
  my own files' text in memory, plus LF / line-count / line-length / scope-literal checks; the
  helper imports nothing from the project.
- Once, a `python` here-document that did a plain string replacement in my own
  `test_b_decoy_model.py` (two edits; no project import). Later edits used the editor tool.
- Read-only shell commands (`cat`, `sed`, `grep`, `wc`, `ls`) on the sources above; `git add`
  and `git commit` of my own files by name. No formatter was run.
