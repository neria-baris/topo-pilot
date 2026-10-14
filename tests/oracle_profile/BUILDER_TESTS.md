# Builder tests (job 0014): authorship note

`test_builder_controls.py` and `test_builder_kernels.py` are written by the job-0014 BUILDER, the
worker that also wrote the production code. They are not independent. They respond to the three
coordinator pre-freeze reviews of the draft implementation:

- `coordinator-0014-preflight-resource-review`;
- `coordinator-0014-meter-lifecycle-review`;
- `coordinator-0014-validation-provenance-review`.

They cover:

- the runtime-control classifier, including STOP, INVALID and HOLD precedence, malformed usage
  values, the persistent usage latch and its release rule, and audit mode;
- the hardened kernel error paths.

The independent numerical tests and reference are `independent_reference.py`,
`test_oracle_profile.py`, `test_oracle_profile_traps.py` and `test_oracle_profile_kernels.py`,
described in `AUTHORSHIP.md`. A separate test author wrote them from `API.md` only, and they were
committed unmodified at 027e3e0, before the builder read them.

The meter lifecycle paths (Job Object accounting, descendants, fault injection and the emergency
record) are exercised by bounded synthetic meter runs under the same ledger, recorded in the job
report, because they need real child processes.
