# D-2a runtime maintenance v1 — prospective source, 17 October 2026

Scope: repair the launcher-accounting defect accepted in job 0033, and prevent a repeat
of its duplicate-wave launch. D2A-FROZEN-v1, its API, test-authorship records, historic
store and NOT_LEARNED verdict are unchanged. This source is not a released D-2a rerun.

## Reuse and interface

Keep the existing `Supervisor`, thresholds, stage accounting, wave order, seeds,
models and training objective. Reuse `tools/x4_oracle_profile/winjob.py` unchanged.
The additional runtime file `tools/d2a/process_tree.py` is deliberately outside the old
five-file implementation footprint. A future protocol must allowlist and hash this file
and bind a new source freeze; the old protected-path validator should refuse this delta.

`TrainingProcess(args, **Popen_kwargs)` exposes `poll`, `wait`, `returncode`, `cpu_s`,
`memory_bytes`, `terminate` and `close`. It creates a kill-on-close Job Object, launches
the interpreter suspended, assigns it to the job, then resumes. This avoids racing a
launcher that spawns the real interpreter before supervision attaches. Descendants
inherit job membership; existing enclosing job limits are not modified or weakened.

CPU is cumulative job user+kernel time, including exited descendants. Memory is the
job's peak per-process committed-memory figure, so a short-lived process cannot hide
a peak before the next poll. The memory criterion therefore conservatively enforces
the per-process bound on measured peaks. Measurement failures raise, never return zero.
`poll` remains unfinished while any descendant is live, even if the launcher exited.
`terminate` kills and drains the whole job, with the existing 30-second drain bound.
`close` releases the job handle; kill-on-close is a final resource guard.

`wave_main` takes an exclusive `waves/<wave>.lock` lease before any work; a concurrent
invocation fails before launching a child. A lease abandoned by a hard kill is never
automatically cleared; investigate it before starting a replacement. The lease is
released on normal completion or a Python exception. It measures through that wrapper.
On a Python exception its finally block
terminates and closes started trees. It refuses any existing final wave, final run or
attempt record before launching children. It does not delete historical files or try
to infer that an abandoned attempt can safely resume. The original per-run S5 retry
inside one new wave remains governed by its existing rule.

## Verification

New implementation-author tests launch only tiny synthetic Python processes, with no
torch model or research histories. They verify CPU and 32 MiB memory in a real grandchild
after its launcher exits; retention of charged CPU after termination; actual CPU/memory
limit enforcement; cleanup on monitoring failure; and refusal of duplicate training.
Existing independent `test_b_resource.py` is retained unchanged. New tests do not replace
the independent review and acceptance needed for a new scientific execution freeze.

This repair does not explain why D-2a failed its learning criterion. The separate
`D2_LEARNABILITY_DIAGNOSTIC_V1.md` proposal addresses that open scientific question.
