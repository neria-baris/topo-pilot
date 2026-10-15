# Authorship: independent test author A (job 0026, C1′ S1 tests)

**Author.** A separate clean-context Claude agent (model Claude Opus 5.5, `claude-opus-5-5`), dispatched only as independent test author A. I wrote these tests after the written contract was committed (worktree branch `c1p-0026`, HEAD 60ff184, "written contract for C1′-v1"). I had not seen any module source when I wrote them. I am not the module builder.

**Files written** (all new, under `tests/c1prime/`):
- `test_a_chart.py`
- `test_a_chart_lcc512.py`
- `test_a_chart_val.py`
- `test_a_chart_exceptions.py`
- `test_a_oracle.py`
- `test_a_oracle_named.py`
- `test_a_eligibility_support.py`
- `test_a_gates.py`
- `test_a_exceptions.py`
- `test_a_release_meter.py`
- this file

No `conftest.py` and no helper module. No other file was edited.

## What I read

- **The protocol, in full.** `tools/c1prime/PROTOCOL_C1PRIME_v1.md`. I read §1–§20 and §25 closely and skimmed §21–§24 and the freeze record.
- **The rest of the written contract, in full.** `tools/c1prime/API.md`, `CONTRACT.json`, `TEST_PLAN.md` and `CERTIFICATE.md`.
- **Reference and production code** that the tests call or that protocol §18 field 1 names as reused:
  - `tools/x4_circle_history/`: `chart.py`, `cochain.py`, `errors.py`, `stage_records.py`, `scores.py`, `error_bound.py`, `op_guard.py`, `release.py`, `meter_bind.py`, and the chart section of `CONTRACT.json`;
  - `tools/x4_oracle_profile/`: `oracle_profile.py`, the header and constants of `meter.py`, the header of `controls.py`, and the `MEMORY_CAP` line and header of `winjob.py`;
  - `tests/oracle_profile/independent_reference.py`;
  - `src/topo_pilot/oracle/` (`_filter.py`, `_common.py`, `__init__.py`), `src/topo_pilot/contracts/errors.py` and the head of `contracts/__init__.py`, the head of `analysis/__init__.py`, and the function signatures of `analysis/x4f_scores.py`;
  - `tools/chart_diag/chart_diag.py` and `pyproject.toml`.
- **For format only.** `tests/circle_history/AUTHORSHIP_A.md` and the first 120 lines of `tests/circle_history/test_chart.py`.

## What I did not read

- No `*.py` file under `tools/c1prime/`. That covers module code and `materialise_protocol.py`: I did not open, glob, grep or search any of them.
  - One shell listing of `tools/c1prime` was piped through a filter that removed every `*.py` name, so it showed only the five documents.
- No Author B test file. A line-count listing of `tests/c1prime/*.py` showed the names and line counts of the `test_b_*.py` files, but none of their contents.
- No scratchpad or temp directory, artifact store, checkpoint, mailbox or network resource.

## What I executed

- No Python, no pytest, no ruff and no numerical code.
- The only shell commands were read-only file inspection: `wc -l`, `ls`, `sed -n`, `cat`, `grep` and `awk`. The `awk` call checked line lengths. I also used `sed -i` on my own new test files, to wrap boolean results in `bool()`.
- **Disclosure.** I ran one read-only `git log --oneline -5` to confirm the contract commit (60ff184). No other git command was run, and nothing changed state.

## How expected values are obtained

Expected values come from three sources:
- the protocol formulas, recomputed with numpy, `fractions.Fraction` and `decimal`;
- the unchanged frozen kernels, called directly: `chart.fit_chart`, `chart.extend`, `chart._neighbor_scale`, the `cochain.*` functions, `oracle.BayesFilter`, `error_bound.posterior_envelope`, `x4f_scores.ledoit_wolf`, ripser and scipy `connected_components`;
- hand-derived ranks and constants, which are commented in the tests.

A c1prime function is never used to check itself. Two c1prime calls are used only to build fixture inputs:
- `c1_fit.whitening` builds the `white` object for `c1_gates.mahalanobis`, because API.md does not name its keys. The expected W and r̄ are recomputed independently.
- `c1_oracle.decimal_posterior60` supplies b̃₃₁ for the enclosure-branch fixture. It is itself checked against an exact Fraction filter in `test_a_oracle_named.py`.

All fixtures are synthetic.
- A thin rectangular loop has one dominant H1 bar and a sparse midpoint graph.
- Isolated satellites at distance 7 give 487/512 and 486/512 giant components.
- A straight chain plus a far ring centred on the chain axis gives a class that is trivial on C*.
- A 120-landmark synthetic `chart.Chart` is used for C0-val.
- A tiny periodic 12 × 2 cylinder HMM has emission rows that are exact column permutations, so `E[ρz, τj] == E[z, j]` bitwise.

Store-writing tests use `tmp_path`. The meter, controls and winjob globals and `stage_records.PREREQUISITE` are restored by monkeypatch.

## Coverage by TEST_PLAN item

- **A-1** (`test_a_chart.py`, `test_a_chart_lcc512.py`, `test_a_chart_val.py`):
  - items 1 and 2: connected bitwise equality with `fit_chart`; components, ties and restriction;
  - item 3: GIANT 487 passes and 486 fails, with the pre-raise record;
  - item 4: the trivial restricted class;
  - item 5: excluded landmarks are extension-only and never gauge points;
  - item 6: d8, σ and support radius are computed on C*, and differ from the all-512 values;
  - item 7: the ledger;
  - item 8: C0-val support 507/506, fidelity unmasked, bins and resultant over all 512, and `chart_gates` never called;
  - item 9: the persistence order, and preservation on failure.
- **A-2** (`test_a_chart_exceptions.py`): every listed mapping, raised from the real kernel frames.
- **A-3** (`test_a_oracle.py`, `test_a_oracle_named.py`):
  - τ_k, the donors and ρ_k;
  - the symmetry report: r_E exact, ε_sym, and exact-invariance failure on one ulp of T or π;
  - the closed-form index convention, and closed form against direct within t + t²;
  - `closed_form_tolerance`, including the t = 3/2 switch;
  - the 2·10⁻¹² and 4·10⁻¹² relative boundaries;
  - the §3.4 interval rule at its three boundaries;
  - `h3_compare`, including zero posterior entries;
  - the corrupted float closed form on the enclosure branch;
  - `run_oracle`, the C3 `G_hat`, `G_named` on the permuted arrays, the cross-model 1e-12 check, named-space filtering within 4·10⁻¹², and the Decimal reference against exact rationals.
- **A-4** (`test_a_eligibility_support.py`): `s_max` inverted_cdf ranks and ties, the eligibility boundaries, the H4 fraction, κ_ν (population covariance, eligible mean) and the 0.01 trigger. Also the covariates ν, m32 and z.
- **A-5** (`test_a_eligibility_support.py`): D_M with the source's or the donor's z̃, q99 ranks, and the four M3 requirements at their boundaries.
- **A-6**:
  - `test_a_gates.py`: GATE_ORDER, STAGE_GATES, REQUIRED_PASS, the PREREQUISITE rebinding, the full LogitPolicy table, the T-PRE ordering, and the `begin_stage` refusals;
  - `test_a_exceptions.py`: the exception mapping and `run_c1_gate`;
  - `test_a_release_meter.py`: the release checks and the meter rebindings.

TEST_PLAN reassigns items relative to the protocol's §17 lists. The chart-wrapper and stage-machinery items move to A; the A identities, the ratio reduction, the bootstrap, the ladder and the certificate move to B. I followed TEST_PLAN, which is the dispatching split.

## Ambiguities and conflicts noted (the protocol wins; none were resolved silently)

1. **Unresolved at the chart boundary (conflict).** API.md §2 maps `errors.Unresolved` to plain `INCONCLUSIVE`, and its `adapt_chart_exception` covers only two Invalid cases. Protocol §14 says that an "unresolved construction yields INCONCLUSIVE/CHART_UNAVAILABLE … and Unresolved from the frozen kernels" does too, and TEST_PLAN A-1.4 agrees. The tests require `run_c1_gate(..., chart=True)` to record INCONCLUSIVE/CHART_UNAVAILABLE for an Unresolved raised by a chart kernel:
   - `test_trivial_restricted_class_stops_unresolved_after_lift_record`;
   - `test_unresolved_chart_kernel_is_chart_unavailable`.
2. **δ and a are exact decimals.** Protocol §3.2 sets δ = 2·10⁻¹² and §3.4 sets a = 2·10⁻¹², with numbers "exactly as written". API.md gives the float defaults `delta=2e-12` and `a=2e-12`. The exact-boundary tests use the rational 2/10¹²: `closed_form_tolerance` values, t = 3/2 exactly, and D_high = a. A binary `Fraction(2e-12)` would fail them. The near-boundary cases use margins of 10⁻²⁰ or more, or float steps of 2⁻⁵², so they hold under either reading.
3. **GIANT persist record keys.** API.md lists the fields of `persist("giant", …)` but not their key names. The tests accept the protocol name or the info-style name, for example `b`/`birth`, `l_max`/`ell_max`, `excluded_ids`/`excluded_landmark_ids`, and `giant_pass`/`pass`.
4. **`ConstructionLedger(path)`.** API.md does not say whether `path` is the store directory or the file. The tests pass the file `CHART_CONSTRUCTIONS.json` and check that it exists after a claim.
5. **Status convention of `classify_exception` and `adapt_chart_exception`.** API.md writes some returned statuses in full (`FAIL_TECHNICAL/ORACLE`). §0 and `adapt_chart_exception` split them into a status prefix and a reason suffix. The tests accept either form. They do require any suffix to be the first token of the reason: a `PH_RESOURCE_LIMIT` reason must start with `RESOURCE`.
6. **`c0_val` result shapes.** The container type of `"criteria"` is unspecified, so the tests accept a dict keyed by criterion or a 4-sequence in the order support, fidelity, bins, resultant.
7. **`m3` `Sup` keys.** These are unspecified. The tests pass `S`, `D`, `T` and `C`, plus the aliases `C_mean`, `Cbar` and `C_bar`.
8. **`kappa_nu` argument shapes.** The tests assume that `nu_p` and `nu_m` cover all calibration rows and that `elig_cal` selects the eligible ones.
9. **"Beyond q99".** This is read as strict, D_M > q99 (`test_frac_beyond_is_strict`).
10. **Operational gates use float semantics.** M3 is operational (§15.3.1), so its inequalities are compared as float64. The F(T) = 0.05 equality case is expected to pass. The frame fractions are dyadic, so F(C̄) is exact under any summation order.
11. **The release's common fields.** API.md names only the stage-specific fields. The valid fixture carries the K4 `release.py` field set plus the C1 fields; each negative case breaks one binding. API.md also does not say how authority paths are resolved, so the files sit where the contract's relative paths and the release's absolute paths name the same file. All hashes are lowercase in both the synthetic contract and the release.
12. **`GATE_FAILED` with `c1_status`.** `StageFailure` is a frozen dataclass, so the tests attach `c1_status` with `object.__setattr__`. Without `c1_status`, `GATE_FAILED` is expected to be FAIL_TECHNICAL. API.md calls this "any other StageFailure", and protocol §16 limits the INCONCLUSIVE mapping to "an explicitly declared unmet criterion".
13. **The `LogitPolicy()` constructor.** The tests assume it takes no arguments. They also assume an out-of-order `begin` raises `C1GateFailure` with a FAIL_TECHNICAL status.
14. **`disk_reason` on an unreadable drive.** The tests expect a STOP reason, the fail-closed K4 behaviour that the C1 helper is "extracted with provenance and regression checks" from. API.md is silent. `rewrite_argv` is not tested: its K4 counterpart touches the real store (ledger sync), and API.md does not specify its argv requirements.
15. **NaN smoothing residual with finite f.** This cannot be reached through the unchanged kernel's arithmetic. The test induces it by replacing `numpy.linalg.norm` for one call; the frozen file is unchanged.
16. **The enclosure branch of §3.2.** API.md exposes no dedicated function for it. The S1 fixture uses `interval_rule` with `posterior_envelope(32, N)` against a Decimal closed form built in the test.
17. **Package and store paths.** API.md names `tools/c1prime/` and `c1prime-store/`, while protocol §18 and §17 name `tools/c1_state_forcing/` and `c1-state-forcing-store/`. API.md records these as task paths, not scientific choices. The tests only follow API.md §0 imports and use tmp_path stores.

## Correction after the builder's first run

This was a defect in the test's own reference, not in the module. In `test_a_oracle_named.py::test_decimal_reference_against_exact_rationals`, the reference surprisal was `s_exact = -exact_ln(...)`. The unary minus ran outside the 90-digit context, so Decimal negation rounded to the ambient 28 digits, and the reference differed from the module's 80-digit value by 8.4·10⁻²⁹. The line now reads `s_exact = -Fraction(exact_ln(...))`, which negates exactly in rationals. No tolerance and no other test changed. I made this correction under the same rules as before: without reading module source and without executing anything.
