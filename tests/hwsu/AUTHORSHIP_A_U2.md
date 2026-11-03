# Authorship record: test author A, phase 2 (job 0223; estimand and decision side)

Author: a clean-context Claude subagent (Opus 5.5) acting as independent test author A, 2026-11-03.
Task: `agent-handoff/jobs/0223/task.md` (Phase 2, "Test author A") and `jobs/0223/RULINGS.md`
(R-0223-1..6).

## What I read

- `tools/hwsu/TEST_PLAN_U2.md` (all), `tools/hwsu/API_U2.md` (all), `PROTOCOL_HWSU_v1.md` §2.9
  (statistics and decision rules) and grep lines, phase-1 `API.md` (oracle and KO rows, constants),
  `CONTRACT.json` (`outcomes_u2`, `seeds`, `gates_u2.continuing_statuses`, key list).
- Public reused code: `c2_decide.py` lines 1-125 (`stream_bounds`, `guard`, `sign`, `_category`),
  `precision.py` (`sd_b4_draws`, `centered_draws`, `mde`, `precision_summary`),
  `c2_model.closed_logits`/`readout_coords`, `c1_oracle.named_from_canonical`,
  `c2_attrib.half_dot`, `c1_records.C1GateFailure`; phase-1 `tests/hwsu/test_a_of_lemmas.py` header
  (my own phase-1 pattern).

## What I did not read

No `tools/hwsu/*.py` or `tools/hwsu/u2/*.py` file, no `tests/hwsu/test_b_*`/`AUTHORSHIP_B*`, no store
file, no OF value, no blinded or track-D path, no public research-summary path.

## Expected values

From the protocol and API_U2 only: hand reimplementations of the §2.9 table, the 2-of-3 rule, the
P1 ladder rule (on the reused `precision` module) and the Lemma FW-U event count; Lemmas P1/P2/J by
exact Fraction enumeration on `hwsu_dry.nonreversible_chain` (L = 8). Synthetic data only. Tests
import phase-2 modules lazily (`import u2` then `importlib.import_module`) so the files collect
before the code exists. At writing: 205 collected; 21 pass (protocol-only checks), the rest fail
with ModuleNotFoundError until the code lands.

## Spec ambiguities (to the coordinator)

1. Status strings: API_U2 writes `RESPONDS_j` etc. without saying whether `j` is literal or the
   master; tests normalise `_j`/`_<digits>` suffixes.
2. `response_outcome(per_model)` takes `{j: status}`, but rule 6 needs per-model rule-6 flags;
   the rule-6 test passes `model_status`-shaped dicts `{"status", "rule6"}`. Return keys assumed:
   `outcome`, `dissent` (list), `rule6` (str or list; "in 2 models"/"all three" text).
3. `fw_events(theta_region)`: argument form unspecified; tests pass a `Fraction` θ and expect the
   protocol counts (2, 2 at θ = 0.10, 2, 2, 1).
4. `write_sealed_u(store, arrays)`: key names of `arrays` unspecified; tests pass `A_<j>`,
   `ZR010_<j>`, `ZR030_<j>` and `G`, and expect `means["theta_<j>"]` = mean A_j / mean G.
5. `study_outcome(records, …)`: records assumed `[{"gate", "status"}]`.
6. `kc_u(ctx)`: ctx keys unspecified; the planted-λ test guesses `o1, o2, s1, s2, G, d`
   (and nested `pc`/`val`). Expect to adapt.
7. P1 UNDERPOWERED: returned (`N_RESP` None) or raised `INCONCLUSIVE/UNDERPOWERED`; both accepted.
8. `licences(...)` input/output shapes: tests only search all returned strings for the scope
   clause, disclosure, the S3 share text, LOW_RESPONSE's not-licensed sentence and absent share
   licence names.
