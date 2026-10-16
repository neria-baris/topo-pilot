# K4b independent tests: authorship (protocol §11.4; job 0045)

Two clean-context subagents wrote these tests. Each was launched by worker session 452805bb-b062-4942-9585-f3e97e8a587c with a short brief: its §11.4 list (including the "Added in v2" items and the v3 wording), the allowed inputs, and the rules. Neither author saw the other's files, the worker's conversation or any module code. **No module code existed** when the tests were written and committed: `tools/k4b/*.py` was absent (verified with `ls` before the test commits). The contract they worked from is commit 6e5d97b.

| | Author A (mathematics and certificate) | Author B (data, chart reuse, registry and flow) |
|---|---|---|
| Files written | `test_a_prop1.py` (11), `test_a_theorem_a.py` (8), `test_a_lemma_t.py` (7), `test_a_lemma_n.py` (21), `test_a_decision.py` (19), `test_a_ranks_ladder.py` (14), `test_a_width_b4.py` (11): **91 tests** | `test_b_data.py` (25), `test_b_registry.py` (13), `test_b_charts.py` (22), `test_b_flow.py` (17), `test_b_rerun.py` (11), `test_b_meter.py` (19): **107 tests** |
| Read: contract | `tools/k4b/PROTOCOL_K4B_v1.md` (§0, §1.1–1.4, §5, §7, §8.1–8.3, §11.3–11.4), `API.md`, `CONTRACT.json`, `TEST_PLAN.md`, `CERTIFICATE.md` | `tools/k4b/PROTOCOL_K4B_v1.md` (§3–4, §6–7, §11), `API.md`, `CONTRACT.json`, `TEST_PLAN.md`, `CERTIFICATE.md` |
| Read: reused frozen code | `c1_means`, `c1_bounds`, `c1_cert` (constants), `c1_records` (C1GateFailure), `error_bound`, `precision`, `scores`, `process_law` (κ only) | `c1_chart`, `c1_records`, `c1_config`, `c1_data`, `c1_registry_sources`, `stage_records`, `op_guard`, `meter`, `controls`, `winjob`, `dataset/sampler.py`; parts of `scores.py` and `chart.py` |
| Did not read | `tools/k4b/*.py` (none existed); B's files; any store, payload, transcript or log | `tools/k4b/*.py` (none existed); A's files; any store, payload, transcript or log |
| Executed | Nothing | Nothing |
| Formatter | None | None |

The worker checked syntax only: each file was compiled in memory with `compile()` (no bytecode was written). No test was run, because the modules do not exist yet. Commits: author A 72d9935, author B babbc57.

**Corrections.** Only a file's own author may correct it (§11.4). **No formatter is ever run over `tests/k4b`.**

**Author A:** correction round 1 (2026-10-16): test_lemma_t_is_not_vacuous asserted `0 < zb < 1`, but with KAPPA = 1/40 the toy bound is zb ~ 1.1533 (implementer report), so the bound was nearly vacuous and the assertion false. Fix in `test_a_lemma_t.py`: KAPPA 1/40 -> 1/100 (docstring updated), assertion kept, hand proof added as a comment: RHO = (101/99)^9 < e^(18/99) < 6/5 and 4 TV <= 2(1.01^8 - 1) < 0.167, so zb < 0.567. Nothing else changed. Author A read only the allowed inputs (protocol sections, API.md, CONTRACT.json, TEST_PLAN.md, CERTIFICATE.md, own test file); read no `tools/k4b/*.py` module code, executed nothing, ran no formatter.

**Author B:** round 2 (2026-10-16): added test_b_h1_meta, test_b_endpoint, test_b_registry_rules from API §14–§15; read no module code.
