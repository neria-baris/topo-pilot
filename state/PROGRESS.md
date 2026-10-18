# Current progress ? 17 October 2026 (maintenance reconciliation)

Stage: **D-2a NOT_LEARNED; C1prime INCONCLUSIVE/FAMILY_UNMATCHED; K4b job 0051 recorded RUNNING**.
Scientific protocols, data and earlier decisions remain unchanged. Historical progress is
available in git; decisions and execution reviews are the durable research record.

## Accepted scientific outcomes
- E0?E4: unchanged; G-H FAIL remains (missing historical timing record).
- X4 B INCONCLUSIVE; B2 scoped NO-GO; Phase C/H4C-I NOT_RUN.
- X4-F closed INCONCLUSIVE/FAMILY_UNMATCHED; no causal endpoint.
- K8 oracle headroom FAIL; K4 closed INCONCLUSIVE at chart_calibration; original C1 blocked.
- X5 G1 H5 REJECTED; all six models complete; closed without fresh test (D-081).
- D-1 all gates PASS (0020); X2a stage 0 GO_P1_NONADDITIVE (0025).
- D-2a closed NOT_LEARNED (0033): both H3 models complete, no remaining grid or stage 3.
- C1prime closed INCONCLUSIVE/FAMILY_UNMATCHED at M2-cal (0044); chart calibration PASS;
  no validation or fresh endpoint. R13 ratified by owner addendum 10.

## Current execution and maintenance
- K4b Z_bound integration repair accepted (0050); freeze 8df3d24d at 3f5c6a23.
- 0051 recorded RUNNING with no final report at inspection. This is a recorded state,
  not independent process-liveness evidence. RES-K-REG1 remains ACTIVE; no competing
  scientific history generation is dispatched by this maintenance task.
- Main maintenance: D-2a nested Job Object accounting/termination, exception cleanup and
  duplicate-run refusal; X4-F accepted-map checks, complete map exports, inner-loop STOP
  and reused exception-safe RunControls. These source changes require a new freeze before
  any future scientific use; they do not rewrite the historical D-2a or X4-F execution.
- Verification: 1962 affected regressions PASS; 91 targeted PASS; final process-tree delta
  11 PASS (overlapping runs). Ruff, imports and diff checks PASS; the unchanged legacy
  reports/he_summary/charts.py remains 712 lines. Source hashes and JUnit references:
  docs/maintenance/REMEDIATION_VERIFICATION_20261017.json.
- Reviewable successor plans and limitations: docs/REMEDIATION_PLAN_HE.md.
- A separate owner window is drafting C2; its files and the active K4b worktree/store are
  left to their existing owners.

## Next actions
1. Review the maintenance source before binding it into any new scientific execution freeze.
2. Existing coordinator reviews the terminal result of 0051 before any new scientific job.
3. For a later study: C2 constrained intervention, D2 learnability development, or X5
   mean-rate-matched comparison; each is a distinct reviewed protocol with its own freeze.

Sources: ../agent-handoff/jobs/{0033,0044,0050}/review.md,
../agent-handoff/jobs/0051/status.json and COORDINATOR_STATE.md; owner addendum 10.
