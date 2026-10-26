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

## v2 update (C2-FROZEN-v2, sha256 51f78976…4583; job 0105)
- **Why.** This update follows the protocol and is not a test defect. The coordinator dcecc9ff requested it.
- **Read:**
  - `agent-handoff/planning/responses/C2-FROZEN-v2.md`: §21 and the parts it touches (§2.2, §2.3, §5.2–§5.7, §7 rows 1–8 with the Y-donor preparation note, §13.1, §13.3 Author B);
  - `API.md` §19.1–§19.3 (erratum 19.3, commit 9c81b54);
  - the `CONTRACT.json` v2 diff (dbe3aa4).
- **Not read:** `tools/c2_readout/*.py` (including the v2 `c2_config.py` change).
- **T-SIZE** (`test_b_policy.py`): 14 modules, each ≤ 400 lines, total ceiling 5,600 lines. The test also requires `CONTRACT.json` `modules` and `module_limits` to match.
- **T-G0** (`test_b_lineage.py`):
  - The byte copy is `PROTOCOL_C2_v2.md` with the v2 hash, and the v1 copy must be absent. `V1_SHA256` is the superseded hash, and the mailbox file is `C2-FROZEN-v2.md`.
  - The AUTH is pending (`None`) until an owner AUTH names v2. `auth_ok` must refuse while it is pending; its other cases run against a synthetic bound AUTH.
  - The G0 mailbox copy is written at both readings of `mailbox_file`.
- **H^Y donor** (`test_b_registry.py`):
  - `y_donor`, the `OFF` rows, the `k_y` sign rule, `history_table(..., k_y)`, `digest_HY` and `table_roles` are checked.
  - The separation duplicate formula is (3n + |Y_def|) − |U|.
  - OFF_GRID_Y rows form no donor: no clamped or wrapped variant is formed.
  - Every separation fixture uses H^Y in place of H^R.
- **Coverage and H4:** the reasons S_Y, LIK_Y and OFF_GRID_Y, and H4 = {x: 9/10, y: 17/20}.
- **NEW-10:**
  - Policy fixture: no preparation before REG; no model output inside H2 or REG2; H3 and T-PRE begin only after H2 and REG2 end.
  - Data fixture: k_Y is computed from the cached natural b31 only. Separation runs over the defined donors before H3. `oracle_split` consumes the cache (a marked cache value comes through), and HY is formed only on Y_def rows.
- **The whitened G1 identity (D-0104-2):** no file of author B checked the old WP − PᵀW form, so nothing changed.
- **Files rebalanced to stay ≤ 400 lines (meaning unchanged):**
  - T-NAMESPACE moved from `test_b_registry.py` to `test_b_lineage.py`.
  - The release-binding tests and the measure-only caps test were exchanged between `test_b_lineage.py` and `test_b_policy.py`.
  - The k_Y sign rule, the coverage reasons and the H4 test sit in `test_b_policy.py`.
- **Executed:** only an in-memory `ast.parse` + `compile`. No formatter was run.

## D-0107-1 regression (job 0108; ruling R-0107-2)
- **Why.** The coordinator dcecc9ff asked for this regression test after a defect.
- **Read:** `agent-handoff/jobs/0107/review.md` (D-0107-1, R-0107-2) and the coordinator's message giving `c2_data.own_records(store, stage, lineage) -> dict[str, str]`. The API.md erratum for `own_records` had not landed when this was written, so the review's rule and that signature were followed (API-AMBIGUITY comment in the file).
- **Where:** `test_b_fwl_l1.py` (T-NAMESPACE in part), because it had room within 400 lines. All stores are synthetic, under `tmp_path`.
- **Cases covered:**
  - **S1 accepted:** one STARTED line, and only IMPL and AUTH-ADMIT gate lines (stage S1, scope study). `own_records` returns both files with their sha256, and `store_admission(first_sampling=True)` passes with the merged map. The defect itself (no merge, no PASS) is asserted too.
  - **Near misses, none admitted:** an extra G0 or PF gate, another stage, a non-study scope, two STARTED lines, a STARTED line of another stage, a COMPLETED line, and a foreign line.
  - **Later stage (S2):** an accepted prefix whose sha256 equals the lineage `append_only` value, followed by this stage's STARTED and AUTH-ADMIT lines, is accepted; with one altered byte in the prefix it is not.
- **Executed:** only an in-memory `ast.parse` + `compile`. No formatter was run, and `tools/c2_readout/*.py` was not read.

## D-0109-1 regression (job 0110; ruling R-0109-1)
- **Why.** The coordinator 23e2334b asked for this regression test after a defect: while a metered run is active the meter keeps `METER_ACTIVE.lock` at the store root; `c2_data.store_admission` reported it unrecognised, so G0 item (vii) failed at every stage.
- **Read:** `agent-handoff/jobs/0110/task.md` (Author B), `agent-handoff/jobs/0109/review.md` (D-0109-1, R-0109-1), API.md §16 and §19.4. The §19.5 erratum had not landed when this was written, so the ruling text was followed (API-AMBIGUITY comment in the file).
- **Where:** `test_b_patch.py` (appended section; 311 lines before), because it had room within 400 lines. All stores are synthetic, under `tmp_path`.
- **Cases covered:**
  - **S1 admitted with the lock:** a store at G0 time (FREEZE, AUTH, one STARTED line, IMPL and AUTH-ADMIT lines) plus `METER_ACTIVE.lock`; `store_admission(store, {**lin, **own_records(store, "S1", lin)}, True)` has status PASS and an empty `unrecognised` list. The same store without the lock passes too (control).
  - **Near misses, none admitted:** `METER_ACTIVE.lock.bak` and `METER_ACTIVE.json` at the root, and `registry/METER_ACTIVE.lock` in a subdirectory other than `logs/`. Each makes the status not PASS and is named in `unrecognised`. The subdirectory case rests on the ruling's words "at the store root" and §16.1's list of bookkeeping by path; it is marked API-AMBIGUITY.
  - **Not covered:** a later stage (S2-S5) with the lock; the ruling names it, but the S2 prefix fixture is already covered for the records themselves (D-0107-1 entry) and the lock rule is stage-independent.
- **Executed:** only an in-memory `ast.parse` + `compile`. No pytest, no formatter, and `tools/c2_readout/*.py` was not read.
