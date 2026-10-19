# AUTHORSHIP_A: independent test author A (science and numerics), X6S1 job 0069

**Protocol:** X6S1-FROZEN-v1 §14.3 (sha256 2A909ACE38231FBC6647E8FFDB5E6B5F22669A7C92182AE84240F32CD36EFB9E); contract `tools/x6_stage1/API.md` at commit d8cc373 (sha256 3c80e0f81c7af52a7ee0850e0bf93cf06500f4bc6796d741d1d55f9f8360c293).

**Author:** a separate clean-context subagent (agent id ae36420f529903722), launched by worker session b98609d8-a522-4406-94ee-5e30d7b6b142 with a short brief. It did not share context with author B or with the worker's API.md drafting. Tool uses: 65; subagent tokens: 291216.

**Assigned tests:** T-PAIR, T-BETA, T-DESIGN, T-EVAL, T-QUANT, T-LOGTAB, T-EB, T-STAT, T-RULES.

## Read (allowed inputs named in the brief)
- `tools/x6_stage1/PROTOCOL_X6S1_v1.md` (by section) and `tools/x6_stage1/API.md`.
- The reused production and reference code of protocol §14.2 field 1: `src/topo_pilot/**`, `tools/x6_stage0/*`, `tools/d2a/*` including the committed repair `tools/d2a/process_tree.py` (P = 0c341aa), `tools/k4b/k4b_registry.py`, `tools/k4b/k4b_registry_k.py`, `tools/c1prime_registry/*`.
- `tools/x4_oracle_profile/*`, `tests/oracle_profile/*` (`suffix_posterior`)
- `pyproject.toml` (pytest markers).

## Not read
- `tools/x6_stage1/*.py` and the notebook: they did not exist when the tests were written (the worktree held only API.md and the protocol copy under `tools/x6_stage1`), and the brief forbade reading, listing or searching them.
- The other author's test files; any store, pool, sealed file, K-REG2 itself, transcripts or the mailbox.

## Executed
- Nothing. The author used only read and write tools on the allowed paths and its own test files (author's report). It ran no Python, pytest or formatter.
- The worker afterwards compiled each file in memory (`ast.parse` + `compile`, no import, no run): all compile; every file ≤ 400 lines, LF line endings, lines ≤ 100 characters. No formatter was run over `tests/x6_stage1`.

## Files
test_a_pairs.py (15 tests; T-PAIR, T-BETA), test_a_designed.py (10; T-DESIGN), test_a_eval.py (13; T-EVAL, T-QUANT), test_a_numerics.py (18; T-LOGTAB, T-EB, T-STAT), test_a_rules.py (12; T-RULES): 68 test functions.

## Notes
- The list of read files is as instructed and as reported by the author; the worker did not audit the subagent's transcript.
- API ambiguities reported by the author are recorded in `agent-handoff/jobs/0069/report.md`. Corrections to these files are made only by this author (§14.3).

## Correction round (job 0072)
- **Authority:** review of job 0071, ruling R-0071-1, covering defects D3 and D4 in `test_a_numerics.py`. The contract is API.md at bdbdab1, the erratum that sets 35 pools.
- **Author:** the same author-A subagent (agent ae36420f529903722), resumed with SendMessage. It used 5 tool calls.
- **Read:**
  - the D3 and D4 entries of `agent-handoff/jobs/0071/report.md` §5, and `jobs/0071/review.md`;
  - API.md;
  - its own test file.
- **Not read:** `tools/x6_stage1/*.py`, `test_b_*`, and any job-0071 module code or diff.
- **Executed:** nothing. No formatter was run.
- **D3** (`test_eb_constants_registered_table`): the upper check now compares `cl = Decimal(c["L"])` exactly against the reference L, with `L <= cl and cl - L <= Decimal("1e-54")`. Before, it compared against `L + 1e-54`, which was rounded in the default 28-digit context.
- **D4** (`test_two_stage_bootstrap_equals_full_row_multinomial`): the helper `two_stage_by_hand` skips zero-probability count vectors (`if pm == 0: continue`), as the full-row law does.
- **Result:** the file is 374 lines (was 372) with LF line endings. The worker compiled it in memory only.
