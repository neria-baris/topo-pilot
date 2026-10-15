# Builder tests (job 0016): authorship note

`test_builder_runtime.py`, `test_builder_guards.py` and `test_builder_e2e.py` were written by the job-0016 BUILDER, the
worker that also wrote the production code. They are NOT independent.

They cover:
- the job binding of the reused job-0014 meter, controls and winjob, and the stage ceilings;
- the export cap of 80 CPU s;
- coordinator-release refusals;
- the spec v2.3 guards: supervisor-inclusive stage limiter, finalization reserve, strict
  scoring authority and dirty-source refusal;
- the absence of import side effects;
- a static scored-access audit of runner.py;
- a fully synthetic end-to-end run of the runner stages on contracts.testing.memory_store(). It
  checks both that the frozen thresholds stop INCONCLUSIVE at a coverage gate and that relaxed
  test-only thresholds reach precision and export.

The independent tests are written by separate Claude test authors A and B from the written
specification only. They are the files listed in AUTHORSHIP_A.md and AUTHORSHIP_B.md.

The job-0014 tests in tests/oracle_profile are re-run unchanged, as regressions of the reused
oracle kernels and reference.

## Spec v2.4 builder tests (job 0016)

`test_builder_v24_stages.py` and `test_builder_v24_runtime.py` were added by the same BUILDER and are NOT independent. They cover:
- the gate taxonomy (Invalid and JoinError become FAIL_TECHNICAL; Unresolved becomes INCONCLUSIVE);
- stage prerequisites: an out-of-order stage is refused without a gate record, a second attempt is refused even after a simulated kill, an evidence change is an integrity refusal and export then reports FAIL;
- the persisted, identity-bound reference cache: charts reuse it with zero Decimal recomputation (a forbidden stub), refuse a different process, and require the saved IDs and row table to match exactly;
- the timed labels from the runner;
- PRECISION.json, written after a B4 stop with controls, instability counts and Z_bound;
- a cross-model sequence mismatch, which fails FAIL_TECHNICAL at B4_lower;
- op_guard events and its post-return check, run with injected clocks;
- the meter_bind limiter: the operation-deadline kill reason and the disk safe-STOP;
- ONE short real metered child on a temporary store, killed by the 1 s operation wall, with its stale marker then archived;
- ledger allocation sync that preserves every entry;
- the frozen dependency manifest and unfrozen-module detection;
- deterministic numerical-identity records.

Revised existing builder tests:
- `test_builder_e2e.py`: a join mismatch is now FAIL_TECHNICAL / overall FAIL; precision after a stop is StageRefused; the oracle result keys moved under "rows".
- `test_builder_runtime.py`: the import-hygiene list was extended, and the fixture ledgers carry cap metadata.

The earlier revisions are in git.

## Spec v2.5 builder tests (job 0017)

`test_builder_v25.py` was written by the same BUILDER and is NOT independent. It covers:
- the claude-coordinator release binding: accepted with a valid assumption record; refused for a wrong session, a wrong sha256, a wrong schema, a record outside the archive, missing fields, an unknown issuer, a non-active runtime or a missing runtime file;
- codex-coordinator releases: still verified while Codex is active, refused once the Claude coordinator is active or when the release carries Claude fields;
- the measure-only CPU policy: no CPU stop and --max-cpu set to inf, an unreleased stage still a refused no-op, the disk reason still raised, and a ledger policy sync that preserves entries;
- the phase interval F4: _wrap, apply_gauge and extend never return 2π.

Revised builder tests:
- `test_builder_runtime.py` and `test_builder_guards.py` pin the legacy capped path by removing cpu_policy from their copied contract, give their release mailboxes a Codex-era runtime file, and assert the job id from CONTRACT.
- `test_builder_v24_runtime.py` finds the caps record among the ledger history records.

The earlier revisions are in git.

## Post-closure revision (job 0021; K4 closed INCONCLUSIVE in job 0018)

`test_builder_v24_runtime.py::test_real_meter_kills_overdue_marked_operation` is now hermetic. Its driver points the unchanged job-0014 controls at a temporary mailbox in tmp_path (`controls.MAILBOX`) and binds the test contract copy to the synthetic job 9999, whose request digest matches.

Before this change, the live mailbox request.json decided whether the meter run was KILLED or REFUSED; jobs/0020/review.md records the failure.

- No production module changed.
- K4 is closed, so no re-freeze was made. The test file's hash therefore differs from the frozen K4 build e3049fee.
