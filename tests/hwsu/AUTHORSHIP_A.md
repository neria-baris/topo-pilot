# Authorship record: test author A (job 0198, phase 2; oracle and estimand side)

Author: a clean-context Claude subagent (Opus 5.5) acting as independent test author A, 2026-11-01.
Task: `agent-handoff/jobs/0198/task.md` (sha256 f569c03c…8d), section "Test author A", and
`jobs/0198/RULINGS_PHASE1.md`.

## What I read

- `tools/hwsu/PROTOCOL_HWSU_v1.md`: §2.1–§2.10, §4 (all), §5.1–§5.4, §9 (DRO cases); headings
  of the rest.
- `tools/hwsu/API.md` (phase 1, all sections incl. §14 decisions and §15), and the appended
  "J11 erratum" section (commit 75a8e56; the diff of `API.md` and `CONTRACT_OF.json` only).
- `tools/hwsu/CONTRACT_OF.json`: `number_format`, `world`, `seeds`, `sizes`, `streams`,
  `sequence_ids`, `thresholds`, `gates_of`, `dry_run`, `name_rule`, `tests`, `handoff`,
  `stage_c`, `binding.from_imports`, the key list of `binding.allowlist`.
- `tools/hwsu/TEST_PLAN.md` (all).
- Public APIs (signatures, docstrings and the bodies of the named reused functions) of:
  `topo_pilot.dataset.sampler` (`_cumulative_rows`, `_draw`, `HMMSampler` docstring),
  `topo_pilot.oracle._filter` (`FilterResult`, `BayesFilter` docstrings), `c1_oracle`
  (`F`, `tol`, `rel_agree`, `interval_rule`, `run_oracle`, `G_hat`, `m32`, `nuisance`,
  `decimal_*`, `h3_compare`), `c1_means` (all), `c1_endpoint.A_hat`, `c2_oracle`
  (`oracle_role`, `nuisance5`, `phi_star`), `c2_decide` (`stream_bounds`, `guard`, `beta_A`,
  `beta_E`, `sign`, `_category`), `c2_attrib` (`half_dot`, `partition`, `ratio_intervals`),
  `c2_code` (`harmonics`, `standardise`, `fwl`, `f1_fwl`, `gls`, `fstar`, `problem`),
  `c2_stats` (`f1_problem`, `delta_p`), `c2_model.helmert`, `precision` (all),
  `oracle_profile` (`circle_features`, `posterior_means`, `validate_process` signature),
  `hwsb_dry.build_tiny_process`.
- Git metadata of the worktree (`git log`, `git status`, `ls tools/hwsu`).

## What I did not read

- No `tools/hwsu/*.py` file was opened, listed for content, searched or diffed. I only imported
  and executed the modules (pytest runs with `--tb=line`, and two scratch scripts that called
  `hwsu_of.of_2`, `hwsu_oracle.problem_o` and printed their return values).
- No `tests/hwsu/test_b_*` file and no `AUTHORSHIP_B.md`.
- No public research-summary path, no track-D file, no blinded stage-C file, no store file,
  no `payload.npz`, `state.pt`, `sealed/` or history array.

## How expected values were obtained

- KS-PAIR chain: exact Fractions from CONTRACT `dry_run.ks_pair_chain`; the joint law by a
  test-side forward recursion; conditionals by Bayes; β by direct enumeration of the suffix
  states; the implied prefix law by enumeration of the API §2.1 formula over z₁..z₄.
- Lemmas: exact pair law P(s)P(p¹|s)P(p²|s) by enumeration (L = 8); logs enter as fixed
  rational stand-ins, so every identity (which is algebraic in those values) holds exactly.
- Tiny world: a test-side forward filter (q̄, b, m32, q4, m4) and the D-18 emission formula.
- Problem O, KO categories, OF-4 ladder, OF-5: the reused kernels called directly by the test
  with the protocol's arrays, seeds, α and ranks, and the §2.9 rule table written out.
- Before `hwsu_dry.py` landed, a scratch stub of `tiny_world()` (outside the project tree)
  was used to dry-run `test_a_of_oracle.py` and `test_a_of_gates.py`.

## Coverage map (TEST_PLAN §2 rows)

| TEST_PLAN row | File | Tests |
|---|---|---|
| sampler (a) T̃ exact, ≠ T; check_process refusals | `test_a_of_sampler.py` | `test_time_reversal_exact_and_differs_from_T`, `test_check_process_accepts_chain_and_refuses_bad_pi` |
| sampler (b) implied law = Bayes conditional, exact | same | `test_backward_messages_and_bridge_exact`, `test_implied_prefix_law_equals_bayes_conditional` (16 suffixes) |
| sampler (c) arm-2 marginal = process law | same | `test_arm2_marginal_equals_process_law` |
| sampler (d) planted T-for-T̃ and β-dropped fail | same | `test_planted_defective_samplers_are_caught` |
| sampler (e) 10⁵ draws within 4 SE, suffix bitwise, dtype/shape | same | `test_sample_prefix_frequencies_within_4se` |
| sampler (f) draw order, uniform count, replay | same | `test_draw_order_and_uniform_count`, `test_rows_are_paired_by_index_not_sorted` |
| sampler (g) zero column never drawn; (h) impossible suffix | same | `test_zero_probability_column_never_drawn`, `test_bridge_refuses_impossible_suffix`; also `test_suffix_equal_flags_a_changed_suffix_cell`, `test_float_kernels_match_exact_kernels` |
| lemmas P2 (pair covariance), E[A_full] = E[zᵀρ4] | `test_a_of_lemmas.py` | `test_predictives_and_tower_property`, `test_lemma_p2_pair_covariance_identity` |
| lemma J (E[G] = Jeffreys ≥ KL) | same | `test_lemma_j_oracle_response_is_jeffreys` |
| lemma P1 (suffix-only A ≡ 0), P3 (Δc = Δc_b) | same | `test_lemma_p1_suffix_only_predictor_reads_nothing`, `test_lemma_p3_code_interchange_moves_only_the_beyond_four_part` |
| `pair_core`, `readout_A`, `lemma_p_arrays`, `label_share` | same | `test_pair_core_equals_c1_oracle_G_hat`, `test_readout_A_formula_and_suffix_only_zero`, `test_lemma_p_arrays_match_the_formulas`, `test_label_share_formula`, `test_label_share_zero_when_circular_marginals_agree` |
| oracle: tiny world, `arm_oracle`, `suffix_oracle` (+ wrong window), `m4_check`, `helmert` | `test_a_of_oracle.py` | `test_tiny_world_matches_d18`, `test_arm_oracle_against_test_side_filter`, `test_suffix_oracle_bitwise_across_arms_and_correct`, `test_helmert_mirror` |
| KO identities, planted λ = 1/4, KO categories and rule 6 | same | `test_ko_logits_and_identities`, `test_ko_categories` |
| Decimal rows (k = 4) and a planted 1e-8 error | same | `test_decimal_rows` |
| problem O (K = 3, K = 1, Euclidean), degenerate fit | same | `test_problem_o_is_the_f1_composition` (3 cases), `test_problem_o_degenerate_fit_is_not_pass` |
| `share_arrays`, `share_guard_beta` | same | `test_share_arrays_and_guard` |
| OF-1 gate (not in the plan's targets; added) | same | `test_of_1_passes_and_fills_ctx`, `test_of_1_suffix_defect_is_a_sampler_failure` |
| OF-2 (boundary, rank, status) | `test_a_of_gates.py` | `test_of_2_boundary_is_exact`, `test_of_2_rank_is_checked`, `test_of_2_real_bounds` |
| OF-3 (c = 0.5 PASS, c = 0.1 SHARE_DROPPED, ψ point, variants, degenerate) | same | `test_of_3_share_ceiling` (2 cases), `test_of_3_degenerate_primary_fit` |
| OF-4 (calls, seeds, α, alternatives, family rules, after OF-3 drop) | same | `test_of_4_calls_and_alternatives`, `test_of_4_family_rules` (4 cases) |
| OF-5 (real sampler PASS; π-for-bridge FAIL) | same | `test_of_5_real_sampler_passes`, `test_of_5_planted_pi_sampler_fails` |
| outcome (DRO8), tails | same | `test_of_outcome`, `test_tails` |
| ladder vs independent recomputation; mean(A_full) invariance | `test_a_of_ladder.py` | `test_design_of_the_planted_arrays`, `test_of_4_ladder_equals_independent_recomputation`, `test_shift_of_mean_A_full_changes_nothing`, `test_share_dropped_at_of_3_keeps_response_rule` |

Test counts (collected): sampler 28, lemmas 10, oracle 14, gates 15, ladder 4; total 71.

## SPEC-QUESTIONs and API-AMBIGUITYs (marked in the files)

1. **OF-2 boundary** (`test_a_of_gates.py`): TEST_PLAN says a bound L = 0.02 "is not a pass";
   under the protocol's exact comparison (API: `Fraction(float(L)) > 1/50`) the double 0.02
   equals 0.0200000000000000004163… > 1/50 and passes. The test follows the protocol: the
   largest double below 1/50 fails, the double 0.02 passes.
2. **OF-4 response arrays** (`test_a_of_ladder.py`): protocol §4.2 names only ZR°030 = (1 − 0.30)·G
   but also says "run the P1 rule of §2.9" (ZR010 and ZR030); API D-12 forms both. The planted
   arrays separate the readings (ZR030 alone powered at 8,192, ZR010 at 16,384); the test
   asserts D-12 (16,384).
3. **Share arrays after an OF-3 drop** (`test_a_of_gates.py`): protocol §4.1 S3 / DRO8 say "no
   share array is formed downstream"; API OF-4 / D-21 still compute OF-4's share proxy arrays.
   Not asserted either way; only the response-decided status is.
4. **Problem O K = 3 on the tiny world** (`test_a_of_oracle.py`): TEST_PLAN expects PASS on 2,048
   tiny-world fit rows. A test-side composition fails the G1 identities (EXCLUDED/NUMERICAL) on
   several tiny-world row sets (on the dry-scope rows: K = 3 PASS at 2,048 rows but
   EXCLUDED/NUMERICAL at 1,024, the DRO1 size; Euclidean EXCLUDED/NUMERICAL at both). The test
   asserts equality with the reused composition and PASS for K = 1 only.
- API-AMBIGUITY: where OF-3 puts ψ_orc and the variant values (details or `ctx["psi"]`); the
  status of a wrong `rank_L` in OF-2; the `ctx["proxy"]` layout; `N_share` after a raised OF-4.
  Each test accepts every reading consistent with API.md.
