# tests/x2a_stage0: independence record (job 0025)

**Author:** independent test author (a Claude Code subagent), 2026-10-15. I am a separate agent from the module author. I worked in a clean context, after the protocol was frozen (X2A-FROZEN-v1) and after API.md was committed (commit 2238123, as stated in my task; I made no git call to check it). I wrote the tests before seeing any module source. I did not write the module.

**Files written:**
- `tests/x2a_stage0/test_x2a_stage0.py`: 386 lines, 15 test functions, 17 collected tests (one function has 3 parameters).
- `tests/x2a_stage0/test_x2a_stage0_ph.py`: 296 lines, 18 test functions, 18 collected tests.
- `tests/x2a_stage0/AUTHORSHIP.md`: this file.

## What I read

- `agent-handoff/planning/responses/X2A-FROZEN-v1.md`, all 1040 lines. This is the authoritative protocol.
- `topo-pilot-x2a/tools/x2a_stage0/API.md`, the written contract. It is the only file under `tools/x2a_stage0/` that I opened.
- Production and reference code that the tests call (protocol §8.2 field 1):
  - `src/topo_pilot/world/__init__.py`, `lattice.py`, `complex.py`, `registry.py`, `metrics.py`, `config.py` and `identification.py`;
  - `src/topo_pilot/process/__init__.py`, `_geometry.py`, `transition.py` and `emission.py`;
  - `src/topo_pilot/oracle/__init__.py`, `_filter.py` and `_common.py`;
  - `src/topo_pilot/contracts/_schemas_world.py` (WorldSpec and TransitionSpec fields);
  - `src/topo_pilot/dataset/sampler.py`;
  - `src/topo_pilot/topology/distance.py` (the `dedup_map` convention) and `summaries.py`. In `persistence.py` I read only a content search for the `DiagramResult.rows` layout;
  - `tools/x4_oracle_profile/oracle_profile.py`: a search for its function definitions, then lines 60–153 (`validate_process`, `suffix_posterior`);
  - `tests/oracle_profile/independent_reference.py`.
- `pyproject.toml`.
- `tests/d1_seam/AUTHORSHIP.md` as the format example, and `tests/d1_seam/test_d1_seam.py` for style only.
- Two file listings: `src/topo_pilot/**/*.py`, and the `world`, `process`, `oracle` and `topology` package directories.

## What I did not read

- Any file under `tools/x2a_stage0/` except `API.md`. I never opened, listed, globbed or searched that directory, so I do not know whether its `.py` files exist.
- The scratchpad and temp directories, any output store, any report, and the git history.
- Any other test directory, apart from the two `tests/d1_seam` files and `tests/oracle_profile/independent_reference.py` named above.
- My session context contained the coordinator's auto-memory index, a list of one-line notes. It holds no module content.

## What I executed

Nothing. I ran no Python, no pytest, no ruff, no shell command and no git command. My only tools were file reads, file writes, file listings and content searches. I used content searches on my own two test files to check that no line is longer than 100 characters and to count lines and test functions. The tests have never been run.

## Independence of the references

The `ref_*` functions and the expected values come from the protocol's formulas, and they import nothing from the module:
- the 9-image minimum-image 2-D softmax and the summed-image negative case (§2.3, A1);
- the 1-D field `e`;
- δ₁₂, the torus neighbours and the flat metric;
- T as a Fraction formula: 1/5 on the 4 neighbours and on the diagonal;
- G(d), Δ_rep and the pair laws, plus the K_B walk of Lemma U;
- the k = 2 law, as an explicit sum over z₁;
- the k = 3 law, as a backward recursion with a loop over w₂. This is structurally different from the forward recursion of §4.1 item 2;
- JS in KL form (not the module's φ form);
- φ in 50-digit `decimal`;
- the toy-HMM block log-likelihoods for Lemma A;
- every label, verdict and PH reading case, worked out by hand from §5.6, §5.9, §7.3–§7.6 and API.md.

The tests also use, unchanged, the production `TransitionBuilder`, `CubicalComplex`, `BayesFilter`, `draw_axis_permutation`, `axis_state_perm` and `oracle_profile.validate_process`, as §8.4 permits. Module outputs are only compared against these references.

## Coverage of protocol §8.4

| §8.4 item | Test(s) |
|---|---|
| 1 | `test_E_A_matches_minimum_image_softmax`, `test_summed_images_differ_from_minimum_image` |
| 2 | `test_world_counts_betti_and_builder`, `test_kernel_matches_fraction_formula` (plus `test_mixture_blocks_and_stationarity` for G0.5–G0.6) |
| 3 | `test_T1_T2_and_lemma_U_closed_forms`; `test_emission_variants_against_reference` (column sums of E_A, E_B, E_N, E_P) |
| 4 | `test_exact_enumeration_k2_k3` |
| 5 | `test_js_on_toy_laws_and_series_branch` |
| 6 | `test_decision_tie_rule`, `test_lemma_C_credits` |
| 7 | `test_additive_score_iid_toy_equals_full_llr` (plus `test_additive_score_uses_disjoint_stationary_blocks`) |
| 8 | `test_null_and_swap_identities_on_short_histories` |
| 9 | `test_registry_untouched_by_import_and_build`; `test_run_with_failed_preflight_is_invalid` |
| 10 | `test_geometry_helpers_are_never_called` |
| 11 | `test_band_select_plateau_intersection`, `test_band_select_longest_tie_width_and_beta0`, `test_betti_at_beta1_band_and_k2`, `test_clusters_count_original_points_through_dedup_map`, `test_split_check`, `test_h0_star` |
| 12 | `test_p3_p4_a3_labels`, `test_scientific_outcome`, `test_validity_rule`, `test_released_and_withheld_labels`, `test_q1_and_q2_outcomes` |

## Ambiguities and interpretations (none silently guessed)

I found no conflict between API.md and the protocol that affects these tests. The following points are interpretations:

1. **§8.4 item 7 ("every row of T equal to π").** For the two-component mixture, I read this as: every row of each component's block equals that component's own stationary law, and the start law gives each component ½. With this reading the blocks are conditionally independent given c, and s_add equals the full LLR. A second toy, with a sticky component A, checks that the score is built from disjoint stationary-restart blocks. In that toy s_add is not the full LLR, and symbols after block·n_blocks are ignored.
2. **§8.4 item 4 ("by explicit loops").** The reference does not loop over every string and every state path, because that would be too slow. It loops over z₁ for k = 2, and over w₂ in a backward recursion for k = 3. Both are independent of the module.
3. **§8.4 item 9 ("after import and run").** The registry is checked at four points:
   - before and after importing the three module files;
   - after a fresh re-execution of each file;
   - after `build_world` and `variant_model`;
   - after `run()` with a failed preflight.

   It is not checked after a full run, which needs a frozen store, S0 and the full CPU budget.
4. **`band_select` when the longest interval is narrower than `min_width`.** API.md does not say whether `"interval"` is then `None` or the narrow interval. For that case the tests assert only the status and `band is None`. For an empty S they also assert `interval is None`.
5. **Upper end of the search range.** API.md writes S_ρ over the closed range [lo, hi] = [0, 0.99], but segments are half-open. No test probes a plateau that crosses 0.99.
6. **`released`.** The tests check only the label keys passed in; the result may hold other keys. "WITHHELD" is tested for verdict FAIL with first_failed G5. The case of G5 INVALID is not tested: API.md says WITHHELD whenever first_failed is G5, while protocol S3 describes WITHHELD for a G5 FAIL.
7. **`validity` and `run`.** The tests assume that `first_failed` is the gate key string, for example `"PF"`. After a failed preflight they require:
   - verdict INVALID with first_failed "PF";
   - S0 and G0–G5 NOT_RUN;
   - a PF status that is not PASS. API.md does not fix whether it is FAIL or INVALID.
8. **G1.1.** I read "abs ≤ 1e-15 and rel ≤ 1e-12" as two conditions that every entry must meet.
9. **"φ(±1) = ln 2 exactly".** Tested to a relative 1e-15, not bitwise.
10. **G5 exact rows.** The N-iso and N-same exact I_k are tested for k ≤ 2 only, to keep runtime low. The protocol gates k ≤ 4.
11. **Tolerances the protocol does not state**, chosen from float-error estimates:
    - window laws: relative 1e-12;
    - exact I_k against the KL-form reference: relative 1e-9; acc_k: 1e-13;
    - `G_overlap` and `delta_rep_closed`: 1e-14, the G2.2 tolerance;
    - φ: series branch relative 1e-15, closed form relative 1e-11;
    - additive score: 1e-12;
    - stencil log-evidence: 1e-10 absolute in log, equivalent to the protocol's relative 1e-10 on the evidence.
12. **Hand values ([W], not gates in the protocol).** I recomputed them by hand from the §2.3 table and found them consistent:
    - G(0), G(1) and Δ_rep: within 1e-5, as §8.4 item 3 requires;
    - the repeat probabilities 0.179622 and 0.169355: within 1e-5;
    - JS = 9.149e-5: within 1e-7;
    - column 0 of `e`, from the p(d) table: within 1e-6.

    A failure on one of these alone would point first to [W] rounding and only then to the module.
13. **`decision` dtype.** I assert int8, because API.md states it.
