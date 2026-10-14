# Builder tests (job 0016): authorship note

`test_builder_runtime.py` and `test_builder_e2e.py` were written by the job-0016 BUILDER, the
worker that also wrote the production code. They are NOT independent.

They cover:
- the job binding of the reused job-0014 meter, controls and winjob, and the stage ceilings;
- the export cap of 80 CPU s;
- coordinator-release refusals;
- the absence of import side effects;
- a static scored-access audit of runner.py;
- a fully synthetic end-to-end run of the runner stages on contracts.testing.memory_store(). It
  checks both that the frozen thresholds stop INCONCLUSIVE at a coverage gate and that relaxed
  test-only thresholds reach precision and export.

The independent tests are written by separate Claude test authors A and B from the written
specification only. They are the files listed in AUTHORSHIP_A.md and AUTHORSHIP_B.md.

The job-0014 tests in tests/oracle_profile are re-run unchanged, as regressions of the reused
oracle kernels and reference.
