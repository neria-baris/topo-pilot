# X5 G1 — coordinator verification addendum (job 0007)

14 October 2026. Branch `x5-g1-verify`, from fe3fdc5.

**Additive only.** The [feasibility report](X5_G1_FEASIBILITY_REPORT.md), [X5_G1_FEASIBILITY_OUTPUTS/](X5_G1_FEASIBILITY_OUTPUTS/), D-065 and D-066 are byte-identical and unchanged.

## 1. Corrections to the job-0006 report

* **Full protocol hash.** The frozen protocol hash is **E5B0DCEBA7C43917A8921A69DB396700477BA5C9693B7F5D70F50B94B1CFB312**. The report's truncated suffix ("…9E45") was wrong.
* **The E3 comparison is descriptive.** The a0 calibration G_C (0.2713) against the stored E3 ProcessDiagnostics G_C (0.265, test panels) is a descriptive comparison only. No formal equality or replication test was made.
* **Missing old-window counts.** The identical-window counts against old data, which the original run did not compute, are a declared descriptive deviation, not a gate failure. They are still not computed: this job does not sample, and no window comparison was added.

## 2. Audit repairs (commit 5ccf0dc; no numerical rule changed)

| Weakness found in job-0006 code | Repair |
|---|---|
| Parents checked by a 16-hex **prefix** plus a listing hash, which cannot detect an in-place payload change | `verify_sources_full`: the **full** 64-hex payload_sha256 must equal the frozen value, **and** a lawful `store.load` must re-hash the payload. This runs **before and after** computation (`checked_computation`); a failure invalidates the run (`SourceTampered` → FAILED). |
| Exports were not covered by STOP/budget guards | `guarded_export`: a guard before and after every export step. On STOP or budget, only a small `EXPORT_STATUS.json` is written, the remaining steps are skipped, and the exception propagates, so the ledger records `stopped` or `budget` with its cause. |
| The ledger was written non-atomically, without the cause | Temp file plus `os.replace`; all entries are preserved and cumulative CPU never resets; a `cause` field is added; a corrupt ledger raises `LedgerCorrupt` and is left untouched. |
| Outputs could be overwritten | `ensure_new_output_dir`: an existing non-empty output version is refused **before** computation (`OutputExists`). Nothing is deleted. |

**Known limitation.** `try/finally` cannot record the CPU of a process killed abruptly (task kill, power loss). Such costs would be missing from the ledger and must be reported as unknown.

**Tests.**

* **Independent tests:** `tests/experiment/test_x5g1_safety.py`, 23 cases, written by a separate test-writer agent from `X5_G1_REPAIR_API.md` before reading the implementation. All 23 passed on first contact.
* **Builder smoke tests:** updated for the refused-reuse and stopped-export behaviour.
* **Suites:** experiment + process + analysis, 515 passed; ruff, import and file-size checks clean.

## 3. Deterministic post-hoc verification of the SAME data (commit 166711c)

**Method.**

* Inputs, all source-verified by full hash before and after: the saved calibration ObservationSets eb3170a226f03bd0 (a0) and e574367fd00ccf02 (a020), the transitions e4dafc7b9785c172 and 08a22a03727d2295, E 3633ac27dab50cf4 with named tokens, and the world.
* No `HMMSampler` call; the gate driver was not rerun.
* Everything was recomputed with the same functions and frozen streams (bootstrap ("x5g1-v1", "gc_bootstrap", arm); paired ("x5g1-v1", "gc_bootstrap_paired"); linear 2.5/97.5).
* **This is not an independent replication.**

**Outputs.** New immutable version [X5_G1_VERIFICATION_OUTPUTS/](X5_G1_VERIFICATION_OUTPUTS/) (MANIFEST sha256 per file). It contains:

* `verification_arrays.npz`:
  - exact T (a0, a020, rate-matched), π, E and perm;
  - f(y) and l_h(y), and the edge-conductance matrix **(a labelled reconstruction from the metadata rule)**;
  - full spectra of all three kernels;
  - full O1 and O2 singular values per arm;
  - per-history KL to the last-symbol, stationary and two-symbol predictives, with aligned sequence IDs;
  - positional entropies;
  - all 2,000 per-arm bootstrap means and all 2,000 paired-difference values.
* `summary.json`: validity checks, diagnostics including **all** 36 g_w IAT values and statuses, and the conductance metadata.
* `comparison.json`, `run.json` (producer 166711c, versions, full source hashes, CPU and memory).

**Result: CONSISTENT.**

* All **27** compared quantities match job 0006 **exactly**, with maximum absolute difference **0.0** against a tolerance of 1e-12. The quantities are:
  - G_C, its CI, the stationary-marginal G_C, the two-token regret and the positional entropy for both arms;
  - validity and all diagnostics for both arms and the rate-matched kernel;
  - O1, the top-10 O2 values and the O2 rank;
  - α;
  - the paired-difference CI;
  - C_max, l_h and f_y;
  - the a0 equivalence.
* The a020 kernel rebuilt from the metadata rule equals the stored TransitionSpec exactly (difference 0).
* No verdict was reselected; FEASIBLE (D-066) stands as recorded.

**Cost.**

* Verification: 8.094 CPU s, single-threaded BLAS, peak working set 0.67 GB.
* X5 cumulative ledger: **17.016 s**, being 8.922 (gate) + 8.094 (verification). The combined first stage is well under 3,600 s, and the total under 21,600 s.
* Added storage: about 1.8 MB.

## 4. What this does and does not change

**Does:** it confirms that the recorded job-0006 numbers are reproducible from the saved pools with the frozen code path, and it supplies the full arrays.

**Does not:**

* establish learning speed or curvature specificity;
* remove the movement-speed confound, which the full spectra and IATs now show in full;
* constitute a training authorisation.
