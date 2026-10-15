# C1′ implementation freeze: outputs of job 0026 (code and synthetic tests only; no data)

**Protocol:** `tools/c1prime/PROTOCOL_C1PRIME_v1.md`, sha256 0B1F107EC7BB241E97D812EE995AD91DFB1416D719B70942DC3A567B766CF33A. It was materialised from C1-FROZEN-v1 (D1DF1AEF…5DBA) plus C1PRIME-DELTA-FROZEN-v1 (4556EB91…9A58) by `materialise_protocol.py`. All 34 anchors occur exactly once.

**Scope:** implementation freeze only. No payload was decoded, no history was sampled, no model forward ran on real histories, and no stage was executed.

## Commits (branch c1p-0026; contract → tests → code)

| Commit | Step |
|---|---|
| 38a460f | Step 0: materialised C1′-v1 and the materialiser |
| 60ff184 | Step 1: the written contract (API.md, CONTRACT.json, TEST_PLAN.md, CERTIFICATE.md) |
| 8a41804 | Step 2: independent tests by authors A and B (21 files), with authorship records |
| db583f7 | Step 3: 20 module files under `tools/c1prime/` |
| a3c84df | The authors' own corrections of two test-side defects |

## Freeze (`X:/Downloads/projects/topo-pilot/c1prime-store/`)

| Record | sha256 |
|---|---|
| FREEZE.json (commit a3c84df; 242 bound files; reused K4 and job-0014 files unchanged) | 0a7707c857baca94f1fbe7ab79e9ea52dd1c608fe64b12bce39807bc37cebf11 |
| tests/ACCEPTED.json (496 passed) | 41eb9f6939daa5cf3fb0ed816e7d5cdb8f967fe3bb5d40550480d769d8fdf028 |
| snapshots/before.json | 73a41267acbaa9a0c22669fde0df4abd7a139bc611beb8a4f2369579fe3c9ac7 |
| snapshots/after.json | c46c971e1cf2ab941a7f8ed29e97367a5927be74b96e14037f7f191cd22db740 |
| compare_before_after.json (0 of 1,338 protected files changed; artifact listing equal) | 1b507758ebed1c1944e9a025031efee6e70eb80f719064363c1a37f54d8d04c2 |
| PIN_CHECK_20261015T085351Z.json (fresh venv process: ACCEPTED, 242 files) | 316f15222f5d14b0b11a39ce7d86776bab647e983356959890b5c2dd8cfbae77 |
| CONTRACT.json | 7519b93861264494480e23b7754e29027f6c64a017ebe0cd6a1bb46447406aac |

## C1 release schema (`c1_release.verify`, schema `c1prime-release-v1`)

**Required fields:** schema, job_id, task_sha256, released_stages (⊆ {oracle, calibration, validation, fresh}), source_commit (the worktree HEAD), freeze_sha256, contract_sha256, issued_by = "claude-coordinator", coordinator_session_id and coordinator_assumption_ref {path, sha256}.

**Stage-specific fields:**
- **R1** (`oracle`): `authority` {owner_decisions, diag_json, job_0023_accept}, each {path, sha256}, and `registry_v1` {path, sha256}.
- **R3** (`fresh`): N_test ∈ {4096, 8192, 16384}, an integer k ∈ 1..5, and `registry_v2` {path, sha256}.

The release must live in the dispatched job's mailbox directory and match the live RUN_NEXT request.

**Example (R1, for the data-stage job):**

```json
{
 "schema": "c1prime-release-v1",
 "job_id": "<data job id>",
 "task_sha256": "<sha256 of jobs/<id>/task.md>",
 "released_stages": ["oracle"],
 "source_commit": "<HEAD of topo-pilot-c1p at the data job>",
 "freeze_sha256": "0a7707c857baca94f1fbe7ab79e9ea52dd1c608fe64b12bce39807bc37cebf11",
 "contract_sha256": "7519b93861264494480e23b7754e29027f6c64a017ebe0cd6a1bb46447406aac",
 "issued_by": "claude-coordinator",
 "coordinator_session_id": "<coordinator session id>",
 "coordinator_assumption_ref": {"path": "<agent-handoff/archive/.../ASSUMPTION.json>", "sha256": "<sha256>"},
 "authority": {
  "owner_decisions": {"path": "<immutable copy of OWNER_DECISIONS.md as of mailbox commit a73c869>",
                      "sha256": "5bd1fdb0d66bce5299644659b3e09436ca94b762a62d24d02e1ab064fde537cd"},
  "diag_json": {"path": "X:/Downloads/projects/topo-pilot/chart-diag-store-0023/DIAG.json",
                "sha256": "d01d21c0c28d6af0a0f64b7f00ec548009b2158d61ce045b1625a618cedaffa5"},
  "job_0023_accept": {"path": "X:/Downloads/projects/topo-pilot/agent-handoff/jobs/0023/review.md",
                      "sha256": "d5667d6b0016df5bd3a462115ba6cdcb7a2038b373ad2be0fcd732b123890e92"}
 },
 "registry_v1": {"path": "<registry v1 manifest JSON with 'digests' (and optional 'sequence_ids')>",
                 "sha256": "<sha256>"}
}
```

**Driver use:** `python tools/c1prime/c1_meter_bind.py --release <R> --label <stage>__run -- <venv python> tools/c1prime/c1_driver.py <stage> <R>`.
