# Authorship: independent test author B (job 0026, C1′)

These files were written by independent test author B, a separate clean-context Claude agent (model Claude Opus 5.5, `claude-opus-5-5`). The agent was dispatched after the written contract was committed (commit 60ff184, branch `c1p-0026`, worktree `topo-pilot-c1p`). It wrote everything below before seeing any module source.

| File | Lines | TEST_PLAN items |
|---|---|---|
| `test_b_identities.py` | 287 | B-1; B-4 item 5 |
| `test_b_inference.py` | 246 | B-2 (decision rule, tree mean, bootstrap streams, H5 wrapper, ranks, endpoint bounds); B-4 items 7 and 8 |
| `test_b_precision.py` | 206 | B-2 (ladder, k rule, fresh fraction, H5 and V3 entry points) |
| `test_b_fwl.py` | 211 | B-3 (FWL, the sequential-residualisation trap, F1, whitening, residual, forced state) |
| `test_b_frames.py` | 173 | B-3 (QR sign convention, Haar streams, isometry, same frame on both arms, M1 rules) |
| `test_b_gates.py` | 212 | B-3 (D_w, D_y, leakage, M2, wrap, V1, V2, M4, w_hat) |
| `test_b_decoder.py` | 77 | B-3 (RidgeProbe / nested_ridge equivalence, RBF_DEGENERATE) |
| `test_b_cert_oracle.py` | 379 | B-4 items 1, 2, 3, 6, 12 and 13 (zero-skip neutrality) |
| `test_b_cert_bounds.py` | 297 | B-4 items 4, 9 and 14 (row coverage) |
| `test_b_cert_guards.py` | 212 | B-4 items 10, 11 and 13 (source inspection) |
| `test_b_registry.py` | 177 | B-5 |

## What was read

- The contract documents, in full:
  - `tools/c1prime/PROTOCOL_C1PRIME_v1.md`, including all of §15.3; §21–§24 were read as well;
  - `tools/c1prime/API.md`;
  - `tools/c1prime/CONTRACT.json`;
  - `tools/c1prime/TEST_PLAN.md`;
  - `tools/c1prime/CERTIFICATE.md`.
- Production code that the tests call or that §18 field 1 names as reused:
  - `tools/x4_circle_history/`: `precision.py`, `error_bound.py`, `scores.py`, `stage_records.py` and `errors.py`;
  - `tools/x4_oracle_profile/oracle_profile.py`;
  - `tests/oracle_profile/independent_reference.py`.
- From `src/topo_pilot`:
  - read in full: `dataset/checks.py`, `dataset/sampler.py`, `oracle/_filter.py`, `oracle/_common.py`, `prediction/ridge.py`, `experiment/x4f_probe.py`, `contracts/errors.py` and `contracts/layout.py`;
  - read in part: `analysis/x4f_scores.py` (lines 1–110) and `contracts/ids.py` (`SeedTree`);
  - export lines only, by grep: `contracts/__init__.py`, `dataset/__init__.py` and `oracle/__init__.py`.
- `pyproject.toml` (grep for pytest markers and ruff settings) and `requirements.lock` (grep for pinned versions).
- For format only:
  - `tests/circle_history/AUTHORSHIP_B.md`;
  - the first 60 lines of `tests/circle_history/test_scores_precision_gates.py`;
  - a grep of the import lines (with two lines of context) of a few `tests/circle_history` test files, to match the import ordering. That covers more than the one file the dispatch allowed, but it is limited to import blocks.
- File names only (glob listings): `tools/x4_circle_history/*.py`, the `src/topo_pilot` subpackages listed above, `tests/circle_history/test_*.py`, and this author's own `tests/c1prime/test_b_*.py`.

## What was not read

- No file under `tools/c1prime/` other than the five documents. No `*.py` file there was read, listed, globbed, grepped or searched. That includes `materialise_protocol.py`.
- No author-A file in `tests/c1prime/`, and no `conftest.py`.
- No scratchpad or temp directory, no mailbox, no artifact store and no other worktree.
- `tools/x4_circle_history/chart.py` and `cochain.py` were not opened, because the chart items are author A's (A-1, A-2).

The test `test_b_cert_guards.py::test_certified_kernel_calls_no_blas_matmul_or_numpy_reduction` reads the named c1prime kernels with `inspect.getsource` when the test runs, as TEST_PLAN B-4 item 13 allows. The author never viewed that source.

## Execution

Nothing was executed:
- no Python, pytest or ruff;
- no shell command;
- no git command.

The only tools used were file read, glob and grep on permitted paths, and file write and edit on the new author-B files.

## Approach

- **Synthetic fixtures only.** No test writes to disk; there was no need for `tmp_path`.
- **References.**
  - Exact `Fraction` filters on tiny HMMs, using the literal stored weights.
  - A pure-Python replica of the prescribed C0 expressions, used as a bitwise target.
  - A pure-Python balanced tree for the tree mean.
  - Identically seeded `Generator(PCG64(seed))` and `SeedTree` streams.
  - 40- and 60-digit Decimal logarithms and log-softmax.
  - The unchanged `precision.py`, `oracle_profile`, `error_bound`, `independent_reference`, `BayesFilter`, `HMMSampler`, `x4f_scores`, `nested_ridge` and `RidgeProbe`.
  - Nothing is taken from a c1prime function under test, apart from the composition checks noted in the files: for example, the `b_Y` and `b_Z` counts are built on `b_A` and `b_G`, as the §15.3.5 table counts them.
- **Exact identities.** Where the protocol states an identity in exact rationals, the fixtures are dyadic, so every float64 operation of the prescribed kernel is exact. The identity is then asserted bitwise.
- **Runtime estimate** (not measured): about 1–2 minutes for the author-B set on one thread. The largest costs are `test_b_decoder.py` (two 2048-feature ridge paths on 160 rows) and the ladder tests (5000-draw `centered_draws` at N = 16384).

## Correction after the builder's dev run

The builder's dev run reported one author-B failure, in `test_b_identities.py::test_log_softmax_form_differs_from_logit_form_by_the_normaliser_term`. The cause was the test's own precondition `abs(corr) > 1e-3`, which failed on row 1 of the seed-9 fixture (|corr| = 2.47·10⁻⁴). The fixture's random masses and logits had left δ_m·Δlse small on that row. The identity assertion itself held on every row: the residuals were at most 5.6·10⁻¹⁷.

**Fix.** Only the fixture changed:
- the masses are fixed at 1.06 and 0.95 through `_masses_fixture(9, (1.06, 0.95), rows=3)`, so δ_m ≈ 0.11;
- the logits are now `zm = zp + 0.7 + 0.1·N(0, 1)`, so Δlse is about −0.7, give or take 0.35, on every row.

Together these keep |corr| at about 0.02 or more, so the precondition now holds by construction. The precondition and the identity check (tolerance 10⁻¹³) are unchanged. The author executed nothing for this correction either, and still read no `tools/c1prime/*.py` file.

## Ambiguities and conflicts noticed

The protocol wins in every case. Each item below states the rule the tests apply.

1. **`rank_for` (API.md §6).** API.md says "⌈draws·p⌉ in exact rationals". For the float p = 0.05, 5000·Fraction(0.05) exceeds 250 by 1.4·10⁻¹⁴, so that ceiling is 251. The protocol (§15.3.2 C7, §23.4 item 18) fixes rank 250, the rank numpy's inverted_cdf uses. The tests require 250, 84 and 4917 for the float p values.
2. **`A_logsoftmax` inputs.** API.md does not say whether its log-probability arguments are re-normalised. Every case passes properly normalised log-probabilities, so both readings agree. The exact symbol-constant and arm-common identities are tested on `A_hat`, whose contract is explicit.
3. **Bound-function leaves (`b_G`, `b_A`, ...).** API.md says these functions use only binary + and *. The tests therefore pass |d̂|, |λ̂| and |Δ̂| as nonnegative leaves, which is correct whether or not the function applies abs itself. `omega_TE` is passed as `up(ω_TE)`, a float.
4. **`classify_exception` return shape.** API.md does not say whether it returns `("FAIL_TECHNICAL/NUMERICAL", msg)` or `("FAIL_TECHNICAL", "NUMERICAL: ...")`. The tests accept either form: the status must start with FAIL_TECHNICAL, and the kind must appear in the status or the reason.
5. **P4 on the main route.** API.md does not say whether `rho_main` itself raises for r_h > 1/2. The test requires r_h = 1/2 to be accepted (giving ρ̄ + 1). For r_h > 1/2 it accepts either a raise that maps to FAIL_TECHNICAL/ORACLE, or the Theorem 1′ value, in which case P4 must be enforced by the caller. This case is therefore weakly tested.
6. **`route_f` shapes.** The function returns scalar `r`, `x`, `rho_F` and `ok`, so it is called on one 32-token history with its [V] predictive. `r` is compared with an independent 60-digit computation within 10⁻⁴⁵, because the Decimal summation order is not fixed. `x` and `rho_F` are checked exactly against the module's own `r`.
7. **`measured_log_error` shape.** The tests pass [R, k] arrays and expect the maximum over each row's k values, which is the row's 72 values when k = 2V. The Decimal-trap test triggers `InvalidOperation` with a negative q, because a positive float cannot trap a 40-digit `ln`. If the module pre-validates and raises a non-Decimal exception there, the test fails: the protocol's rule is trap → FAIL_TECHNICAL/NUMERICAL.
8. **`p2_leaves(**arrays)`.** API.md does not name the keyword arguments, so P2 (part of B-4 item 12) is **not tested**. P0 and the A1 self-test are tested.
9. **`build_registry(sources)`.** API.md does not specify the `sources` format, so the INCONCLUSIVE/REGISTRY_INCOMPLETE rule (part of B-5) is **not tested**.
10. **`separation(U_cal, U_val, R1)`.** It is given union digest sets, following the protocol's U_s notation. The role combinations are covered because collisions are planted from different roles.
11. **`lowest(seq_ids, n)`.** "Ascending" is read as ascending sequence_id, the §14 landmark order. The test shuffles the ids, so this reading is distinguished from ascending row index.
12. **Result-dict layouts are not fixed by API.md.** This applies to `history_table` (key names), `endpoint_bounds`, `ladder`, `h5` and `v3`, and to whether `guard_endpoint` and `v3` take dicts or lists. The tests read L, U, N_test and status flexibly. `B_V3` and the `guard_endpoint` inputs are dicts keyed by model seed; `guard_V3` takes lists, as API.md states.
13. **Other shapes and field names.**
    - `m1_report(W, Delta_pm, Qt, frames, c_pm)` receives `(plus, minus)` tuples.
    - `fwl_design(w32, zt, f)` receives f = [R, 2] (cos, sin), not φ.
    - `whitening` is read through the keys `W` and `W_inv`.
    - `f1_check` is assumed to read `rank`, `cond`, `B` and `sv_B` from the fit dict. The boundary cases edit those fields, and B and sv_B are always edited together.
14. **Exact floors.** The guard floor 10⁻⁹ and the H5 threshold 1/100 are treated as exact rationals (§15.3.11; CONTRACT `"floor": "1e-9"` is a string). The float 1e-9 lies just above 10⁻⁹, so the tests require |L| = 1e-9 to clear the floor and nextafter(1e-9, 0) not to.
15. **TEST_PLAN B-4 item 14 (coverage and order).** Only the kernel-level part is testable here:
    - one bound per row;
    - ζ included in every bound;
    - all 32 control bounds entering b^Y.

    Sealing of validation bounds and the T-PRE ordering are driver-level. They fall under author A's A-6 and are not tested in these files.
16. **Theorem 1 history length.** The test uses L = 32 only, because API.md defines `reference_oracle` on 32-token histories. The "L ≤ 33" variants of §15.3.16 item 1 are not exercised.
17. **Items assigned to author A.** Several items on the protocol §17 author-B list were reassigned to author A by TEST_PLAN.md and are not duplicated here:
    - D_M and q99 (A-5);
    - gate order and the computation-order rule, `stage_records` rebinding, and the exception mapping (A-6);
    - the C1′ chart wrapper (A-1, A-2);
    - "zero operational posterior entries do not fail P4" (A-3).
18. **Smaller readings.**
    - `w_hat` is given a duck-typed decoder with `.predict`.
    - `forced` with φ_d = φ_S is required to return `a` bitwise (Δ = 0, the zero patch).
    - `wrap` is required to map both −π and π to the closed end, near +π.
    - `tree_mean` on a 1-D input may return a scalar or a size-1 array.
