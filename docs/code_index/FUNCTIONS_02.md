# Function key, part 2 of 2

| Name | Kind | Qualified name | Location | First docstring line |
|---|---|---|---|---|
| `RunControls` | class | `RunControls` | [src/topo_pilot/experiment/x5g1_controls.py:26](../../src/topo_pilot/experiment/x5g1_controls.py#L26) | Guard before/after operations and always persist a ledger entry on exit. |
| `RunLock` | class | `RunLock` | [src/topo_pilot/experiment/x5g1t_runtime.py:139](../../src/topo_pilot/experiment/x5g1t_runtime.py#L139) | Exclusive lock file for one live model run; removed on exit, never suppresses errors. |
| `RunLocked` | class | `RunLocked` | [src/topo_pilot/experiment/x5g1t_runtime.py:40](../../src/topo_pilot/experiment/x5g1t_runtime.py#L40) | A run lock or an outcome already exists; a second start is refused (no retry). |
| `RunManifest` | class | `RunManifest` | [src/topo_pilot/contracts/_schemas_results.py:238](../../src/topo_pilot/contracts/_schemas_results.py#L238) | What ran: the artifact DAG (``id -> parent ids``), resolved config and its hash, seeds, |
| `running_cpu` | function | `running_cpu` | [tools/hwsb/hwsb_driver.py:148](../../tools/hwsb/hwsb_driver.py#L148) |  |
| `RunResult` | class | `RunResult` | [src/topo_pilot/experiment/s3.py:122](../../src/topo_pilot/experiment/s3.py#L122) | Outputs of one training run: checkpoint ids (step order), ActivationSet ids by step, and |
| `runs` | method | `CircularJob.runs` | [src/topo_pilot/experiment/s7_circular.py:52](../../src/topo_pilot/experiment/s7_circular.py#L52) |  |
| `runs` | method | `ControlsJob.runs` | [src/topo_pilot/experiment/s7_controls.py:73](../../src/topo_pilot/experiment/s7_controls.py#L73) |  |
| `runs` | method | `DevData.runs` | [src/topo_pilot/experiment/s7_dev.py:73](../../src/topo_pilot/experiment/s7_dev.py#L73) |  |
| `runtime_acct` | function | `runtime_acct` | [tools/x6_stage1/x6s1_run.py:392](../../tools/x6_stage1/x6s1_run.py#L392) | §4.6 RUNTIME-ACCT items 1-5 (two normal children, one at 5 CPU-s; metered job). |
| `S` | method | `Summaries.S` | [src/topo_pilot/topology/summaries.py:27](../../src/topo_pilot/topology/summaries.py#L27) | Max finite persistence in ``dim`` divided by ``scale_s``; 0.0 if none or ``s <= 0``. |
| `s0` | function | `s0` | [tools/x6_stage1/x6s1_stage_post.py:81](../../tools/x6_stage1/x6s1_stage_post.py#L81) |  |
| `s0` | function | `s0` | [tools/x6_stage1/x6s1_stage_pre.py:108](../../tools/x6_stage1/x6s1_stage_pre.py#L108) |  |
| `s0_bindings` | function | `s0_bindings` | [tools/d2a/d2a_world.py:289](../../tools/d2a/d2a_world.py#L289) | Gate 1 (§10.6, API §3): protocol hash, dispatch identities from the store-local binding, |
| `s0_check` | function | `s0_check` | [tools/d1_seam/d1_seam_checks.py:252](../../tools/d1_seam/d1_seam_checks.py#L252) |  |
| `s0_check` | function | `s0_check` | [tools/x2a_stage0/x2a_ph.py:288](../../tools/x2a_stage0/x2a_ph.py#L288) |  |
| `s0_check` | function | `s0_check` | [tools/x6_stage0/x6_store.py:101](../../tools/x6_stage0/x6_store.py#L101) |  |
| `s0_check` | function | `s0_check` | [tools/x6_stage1/x6s1_run.py:163](../../tools/x6_stage1/x6s1_run.py#L163) |  |
| `s0_lineage` | function | `s0_lineage` | [tools/x6_stage0/x6_store.py:160](../../tools/x6_stage0/x6_store.py#L160) |  |
| `S0Stage` | class | `S0Stage` | [src/topo_pilot/experiment/stages.py:93](../../src/topo_pilot/experiment/stages.py#L93) | S0: the store is initialised, the environment lock exists, the contracts suite passes, |
| `S1Stage` | class | `S1Stage` | [src/topo_pilot/experiment/s1.py:76](../../src/topo_pilot/experiment/s1.py#L76) | S1: build both core worlds, their kernels, and O/P/N emissions for every σ candidate and |
| `s2_worklist` | function | `s2_worklist` | [tools/hws/hws_select.py:132](../../tools/hws/hws_select.py#L132) | §6.2 item 2 (RC-6 frozen p midpoints; choice 14). |
| `S2Stage` | class | `S2Stage` | [src/topo_pilot/experiment/s2.py:84](../../src/topo_pilot/experiment/s2.py#L84) | S2 as one job: calibrate σ, then build all replicate datasets, oracles and baselines. |
| `s3_bounds` | function | `s3_bounds` | [tools/hws/hws_stats.py:58](../../tools/hws/hws_stats.py#L58) |  |
| `s3_evaluate` | function | `s3_evaluate` | [tools/hws/hws_select.py:158](../../tools/hws/hws_select.py#L158) | §5.6 item 3, §7.1 BELOW_3X (erratum E5). |
| `s3e` | function | `s3e` | [tests/hws/test_a_outcomes.py:94](../../tests/hws/test_a_outcomes.py#L94) |  |
| `S3Stage` | class | `S3Stage` | [src/topo_pilot/experiment/s3.py:255](../../src/topo_pilot/experiment/s3.py#L255) | S3: the smoke run, throughput, the S4/S5 projection, and gate G-E. |
| `S4Stage` | class | `S4Stage` | [src/topo_pilot/experiment/s4.py:90](../../src/topo_pilot/experiment/s4.py#L90) | S4: 6 O runs + 1 N run, then F1, H2, R0–R3, Gaussian floor, H0 checks, gate G-F. |
| `S5Stage` | class | `S5Stage` | [src/topo_pilot/experiment/s4.py:99](../../src/topo_pilot/experiment/s4.py#L99) | S5: the 6 P runs and the same analysis (H3). |
| `s6_rows` | function | `s6_rows` | [src/topo_pilot/experiment/report_e3.py:61](../../src/topo_pilot/experiment/report_e3.py#L61) | Rows of the newest S6 record of ``kind`` (dynamics / layers / x4curves) for ``cond``. |
| `S6Job` | class | `S6Job` | [src/topo_pilot/experiment/s6.py:88](../../src/topo_pilot/experiment/s6.py#L88) | Dynamics and layer sweep of one condition, on top of the S4/S5 analysis lookups. |
| `S6Stage` | class | `S6Stage` | [src/topo_pilot/experiment/s6.py:267](../../src/topo_pilot/experiment/s6.py#L267) | S6: dynamics + H4 (D-034), checkpoint-order null, layer sweep; O, and P after S5. |
| `s7_records` | function | `s7_records` | [src/topo_pilot/experiment/s7.py:153](../../src/topo_pilot/experiment/s7.py#L153) | Ids of the S7 MetricRecords of one ``kind``. |
| `s7_rows` | function | `s7_rows` | [src/topo_pilot/experiment/report_e4_s7.py:26](../../src/topo_pilot/experiment/report_e4_s7.py#L26) | Rows of the newest S7 (or S8) record of ``kind``. |
| `S7Runs` | class | `S7Runs` | [src/topo_pilot/experiment/s7.py:78](../../src/topo_pilot/experiment/s7.py#L78) | Training jobs of S7: train (or reuse) one control run and write its run record. |
| `S7Stage` | class | `S7Stage` | [src/topo_pilot/experiment/s7.py:180](../../src/topo_pilot/experiment/s7.py#L180) | S7: control runs, probes, circular coordinates, sensitivity; gate G-G. |
| `S8Stage` | class | `S8Stage` | [src/topo_pilot/experiment/s8.py:241](../../src/topo_pilot/experiment/s8.py#L241) | S8: clean rerun, store integrity, report reproduction, test suites; gate G-H. |
| `S_h1` | function | `S_h1` | [tests/analysis/test_baselines_dynamics.py:46](../../tests/analysis/test_baselines_dynamics.py#L46) |  |
| `s_max` | function | `s_max` | [tools/c1prime/c1_oracle.py:183](../../tools/c1prime/c1_oracle.py#L183) |  |
| `s_max` | function | `s_max` | [tools/c2_readout/c2_oracle.py:152](../../tools/c2_readout/c2_oracle.py#L152) |  |
| `s_of` | function | `s_of` | [tests/topology/test_shapes_calibration.py:18](../../tests/topology/test_shapes_calibration.py#L18) | H1 signal S of a point cloud under the Euclidean pipeline. |
| `safe_sqrt` | function | `safe_sqrt` | [src/topo_pilot/analysis/horizon.py:88](../../src/topo_pilot/analysis/horizon.py#L88) | ``sqrt(max(P, 0))`` after checking that no entry is below ``-1e-14``. |
| `same` | function | `same` | [tests/c1prime/test_a_chart_lcc512.py:126](../../tests/c1prime/test_a_chart_lcc512.py#L126) |  |
| `same` | function | `same` | [tests/x6_stage1/test_b_train_chain.py:182](../../tests/x6_stage1/test_b_train_chain.py#L182) |  |
| `sample` | method | `HMMSampler.sample` | [src/topo_pilot/dataset/sampler.py:69](../../src/topo_pilot/dataset/sampler.py#L69) | Draw ``n`` trajectories; returns ``(tokens [n, 33], states [n, 33])``. |
| `sample` | function | `sample` | [tools/c2_readout/c2_stage_base.py:317](../../tools/c2_readout/c2_stage_base.py#L317) | H2 / H2': sample the splits; the Y-donor preparation (the natural-history oracle for b31(H) |
| `sample` | function | `sample` | [tools/hws/hws_oracle.py:41](../../tools/hws/hws_oracle.py#L41) | Exactly one HMMSampler.sample call; w_last and the states are dropped at once. |
| `sample` | function | `sample` | [tools/theory_exact/theory_exact.py:65](../../tools/theory_exact/theory_exact.py#L65) |  |
| `sample` | function | `sample` | [tools/x2a_stage0/x2a_mc.py:98](../../tools/x2a_stage0/x2a_mc.py#L98) |  |
| `sample` | function | `sample` | [tools/x6_stage0/x6_run.py:40](../../tools/x6_stage0/x6_run.py#L40) |  |
| `sample_block` | function | `sample_block` | [tools/c1prime/c1_data.py:32](../../tools/c1prime/c1_data.py#L32) | One HMMSampler.sample(4096, rng) call; w33 and the latent states dropped at once. |
| `sample_block` | function | `sample_block` | [tools/c2_readout/c2_data.py:48](../../tools/c2_readout/c2_data.py#L48) | One HMMSampler.sample(4096, rng) call; w33 and the latent states dropped at once. |
| `sample_block` | function | `sample_block` | [tools/hwsb/hwsb_data.py:204](../../tools/hwsb/hwsb_data.py#L204) |  |
| `sample_block` | function | `sample_block` | [tools/k4b/k4b_data.py:83](../../tools/k4b/k4b_data.py#L83) | One HMMSampler.sample(3072, rng) call; w33 and the states dropped; rows sorted by id. |
| `sample_histories` | function | `sample_histories` | [tests/analysis/test_baselines_dynamics.py:34](../../tests/analysis/test_baselines_dynamics.py#L34) |  |
| `sample_named` | function | `sample_named` | [src/topo_pilot/experiment/x5g1_lineage.py:34](../../src/topo_pilot/experiment/x5g1_lineage.py#L34) | One sampler call on ``E[:, perm]``; returns ``perm[canon]`` ``[n, 33]``; states dropped. |
| `sample_observations` | function | `sample_observations` | [tools/hwsb/hwsb_data.py:191](../../tools/hwsb/hwsb_data.py#L191) | One split of DatasetStage._sample_all: canonical draw, named = perm[canonical]. |
| `sample_pool` | function | `sample_pool` | [src/topo_pilot/experiment/x4b2.py:70](../../src/topo_pilot/experiment/x4b2.py#L70) | Canonical tokens ``[n, 33]`` from the frozen stream of ``role``; states are discarded. |
| `sample_pool` | function | `sample_pool` | [tools/d2a/d2a_world.py:109](../../tools/d2a/d2a_world.py#L109) |  |
| `sample_pool` | function | `sample_pool` | [tools/x6_stage1/x6s1_data.py:218](../../tools/x6_stage1/x6s1_data.py#L218) |  |
| `sample_s3` | function | `sample_s3` | [tools/c1prime/c1_driver.py:139](../../tools/c1prime/c1_driver.py#L139) |  |
| `sample_se` | function | `sample_se` | [tools/x6_stage0/x6_run.py:50](../../tools/x6_stage0/x6_run.py#L50) |  |
| `sample_segment` | function | `sample_segment` | [tools/x6_stage1/x6s1_pairs.py:120](../../tools/x6_stage1/x6s1_pairs.py#L120) |  |
| `sample_split` | function | `sample_split` | [tools/c2_readout/c2_data.py:58](../../tools/c2_readout/c2_data.py#L58) | Blocks 0..blocks-1 in block order: canonical uint8 [n, 32], sequence ids, panels. |
| `sample_test` | function | `sample_test` | [tools/k4b/k4b_fresh.py:70](../../tools/k4b/k4b_fresh.py#L70) |  |
| `sampler_cdf` | function | `sampler_cdf` | [tools/x4_circle_history/process_law.py:138](../../tools/x4_circle_history/process_law.py#L138) | The ACTUAL sampler thresholds (_cumulative_rows of the frozen dataset/sampler.py). |
| `sampler_law` | function | `sampler_law` | [tools/x6_stage1/x6s1_pairs.py:160](../../tools/x6_stage1/x6s1_pairs.py#L160) |  |
| `save` | method | `ArtifactStore.save` | [src/topo_pilot/contracts/store.py:90](../../src/topo_pilot/contracts/store.py#L90) | Validate, derive the id, and write; idempotent for identical content. |
| `save_block` | function | `save_block` | [tools/hwsb/hwsb_data.py:302](../../tools/hwsb/hwsb_data.py#L302) |  |
| `save_fit` | function | `save_fit` | [tools/c1prime/c1_driver_cal.py:235](../../tools/c1prime/c1_driver_cal.py#L235) |  |
| `save_hist` | function | `save_hist` | [tools/hws/hws_records.py:56](../../tools/hws/hws_records.py#L56) |  |
| `save_npz` | function | `save_npz` | [tools/x4_circle_history/stage_records.py:40](../../tools/x4_circle_history/stage_records.py#L40) |  |
| `save_npz` | function | `save_npz` | [tools/x4_oracle_profile/runtime.py:64](../../tools/x4_oracle_profile/runtime.py#L64) |  |
| `save_oracle` | function | `save_oracle` | [tools/c2_readout/c2_stage_base.py:346](../../tools/c2_readout/c2_stage_base.py#L346) |  |
| `save_parents` | function | `save_parents` | [tests/experiment/test_x4.py:90](../../tests/experiment/test_x4.py#L90) |  |
| `save_pool` | function | `save_pool` | [tools/x6_stage1/x6s1_data.py:240](../../tools/x6_stage1/x6s1_data.py#L240) |  |
| `save_pools` | function | `save_pools` | [tools/d2a/d2a_world.py:191](../../tools/d2a/d2a_world.py#L191) | Sample and save all 21 pools (POOLS order) once; write pools.json (refuses if present). |
| `save_tables` | function | `save_tables` | [tools/x6_stage1/x6s1_pairs.py:57](../../tools/x6_stage1/x6s1_pairs.py#L57) |  |
| `save_tool_gate` | function | `save_tool_gate` | [src/topo_pilot/experiment/stages.py:75](../../src/topo_pilot/experiment/stages.py#L75) | Save a GateReport whose checks embed tool output (test counts, file counts). |
| `saved` | function | `saved` | [tests/experiment/test_x5g1_safety.py:60](../../tests/experiment/test_x5g1_safety.py#L60) | A store with two lawfully saved TransitionSpecs and their full expected hashes. |
| `scale_of` | function | `scale_of` | [src/topo_pilot/topology/distance.py:40](../../src/topo_pilot/topology/distance.py#L40) | 95th percentile (linear interpolation) of the positive upper-triangle distances. |
| `scaled` | function | `scaled` | [tests/k4b/test_a_theorem_a.py:162](../../tests/k4b/test_a_theorem_a.py#L162) | u~ = sign * c * r * D / (k+1) on S^c: \|u~\| < 1, and u~ . r = sign * c * s D / (k+1). |
| `scan` | function | `scan` | [tools/check_imports.py:71](../../tools/check_imports.py#L71) |  |
| `sched` | function | `sched` | [tests/hwsb/test_b_records.py:118](../../tests/hwsb/test_b_records.py#L118) |  |
| `sched_ok` | function | `sched_ok` | [tools/hwsb/hwsb_driver.py:96](../../tools/hwsb/hwsb_driver.py#L96) |  |
| `schedule` | function | `schedule` | [tools/x6_stage1/x6s1_stage_post.py:144](../../tools/x6_stage1/x6s1_stage_post.py#L144) |  |
| `scientific_outcome` | function | `scientific_outcome` | [tools/x2a_stage0/x2a_mc.py:86](../../tools/x2a_stage0/x2a_mc.py#L86) |  |
| `score` | method | `RidgeProbe.score` | [src/topo_pilot/prediction/ridge.py:78](../../src/topo_pilot/prediction/ridge.py#L78) | Return ``{"mse": ..., "r2": ...}`` (no KL on raw ridge output). |
| `score` | function | `score` | [tests/d2a/test_b_behaviour.py:44](../../tests/d2a/test_b_behaviour.py#L44) |  |
| `score` | function | `score` | [tools/x6_stage1/x6s1_eval.py:187](../../tools/x6_stage1/x6s1_eval.py#L187) | x_hat_i = sum_j (q ln q)[code] - fl(q)[code] * ln p^Q[k] (§7.4 item 3). |
| `score` | function | `score` | [tools/x6_stage1/x6s1_stage_pre.py:256](../../tools/x6_stage1/x6s1_stage_pre.py#L256) | Quantiser on synthetic and gate laws, the certified tables (tables/log_tables.npz), the |
| `scores` | function | `scores` | [tools/x4_circle_history/scores.py:84](../../tools/x4_circle_history/scores.py#L84) |  |
| `scoring_authority` | function | `scoring_authority` | [tools/x4_circle_history/release.py:193](../../tools/x4_circle_history/release.py#L193) | The ONLY issuer of ScoringAuthority: a verified release with an owner scoring record. |
| `ScoringAuthority` | class | `ScoringAuthority` | [tools/x4_circle_history/errors.py:29](../../tools/x4_circle_history/errors.py#L29) | Positively verified owner scoring release (issued only by release.scoring_authority). |
| `scratch_ok` | function | `scratch_ok` | [tools/x6_stage0/x6_store.py:229](../../tools/x6_stage0/x6_store.py#L229) |  |
| `screen` | function | `screen` | [src/topo_pilot/experiment/x4b_audit.py:34](../../src/topo_pilot/experiment/x4b_audit.py#L34) | Partners (same last symbol unless ``last`` is None) and the frozen screen. |
| `screen_bounds` | function | `screen_bounds` | [tools/hws/hws_stats.py:52](../../tools/hws/hws_stats.py#L52) |  |
| `screen_pool` | function | `screen_pool` | [src/topo_pilot/analysis/horizon_pools.py:135](../../src/topo_pilot/analysis/horizon_pools.py#L135) | Apply the frozen screen: admissible ``d1 <= q1_max``; eligible = any admissible partner; |
| `Script` | class | `Script` | [tests/experiment/test_x5g1t_runtime.py:179](../../tests/experiment/test_x5g1t_runtime.py#L179) | A fake ``sleep`` that applies one mailbox mutation per call and records audits. |
| `sd_arg` | function | `sd_arg` | [tests/hwsb/test_a_capture.py:61](../../tests/hwsb/test_a_capture.py#L61) | API-AMBIGUITY: b5's sdU_minus may be keyed by j or by (j, "-") (the ladder's sdU keys); |
| `sd_b4_draws` | function | `sd_b4_draws` | [tools/x4_circle_history/precision.py:22](../../tools/x4_circle_history/precision.py#L22) | Joint whole-trajectory resamples: ONE index per draw shared by every model. |
| `sd_upper` | function | `sd_upper` | [tools/k4b/k4b_stats.py:92](../../tools/k4b/k4b_stats.py#L92) | SD^U per (model, side): rank-4,917 quantile of the sd draws (precision.sd_b4_draws). |
| `seal` | function | `seal` | [tools/c2_readout/c2_driver.py:149](../../tools/c2_readout/c2_driver.py#L149) |  |
| `seal` | function | `seal` | [tools/x6_stage1/x6s1_run.py:260](../../tools/x6_stage1/x6s1_run.py#L260) |  |
| `sealed` | function | `sealed` | [tests/k4b/test_b_registry_rules.py:322](../../tests/k4b/test_b_registry_rules.py#L322) |  |
| `sealed_d2a_predicate` | function | `sealed_d2a_predicate` | [tools/k4b/k4b_data.py:178](../../tools/k4b/k4b_data.py#L178) | True where all 32 symbols lie in {0,...,4} (the sealed D-2a alphabet, §3.4 e). |
| `seam_labels` | function | `seam_labels` | [tools/x6_stage0/x6_model.py:103](../../tools/x6_stage0/x6_model.py#L103) |  |
| `seam_letter` | function | `seam_letter` | [tools/x6_stage0/x6_model.py:88](../../tools/x6_stage0/x6_model.py#L88) |  |
| `searched_null` | function | `searched_null` | [tools/theory_exact/theory_exact3.py:30](../../tools/theory_exact/theory_exact3.py#L30) |  |
| `secondary` | function | `secondary` | [tools/d2a/d2a_eval.py:365](../../tools/d2a/d2a_eval.py#L365) | API §4 items 5 and 7 under the stage-3 budget: RBF at the primary cells, then the |
| `secondary_arrays` | function | `secondary_arrays` | [tools/k4b/k4b_scores.py:74](../../tools/k4b/k4b_scores.py#L74) |  |
| `seed` | method | `SeedTree.seed` | [src/topo_pilot/contracts/ids.py:122](../../src/topo_pilot/contracts/ids.py#L122) | Derived 63-bit seed for ``(master, name, *scope)``; identical on every OS. |
| `seed` | method | `_Seeds.seed` | [tests/x6_stage1/test_b_train_chain.py:142](../../tests/x6_stage1/test_b_train_chain.py#L142) |  |
| `seed` | method | `_Seeds.seed` | [tools/x6_stage1/x6s1_run.py:423](../../tools/x6_stage1/x6s1_run.py#L423) |  |
| `seed` | function | `seed` | [tools/c2_readout/c2_config.py:92](../../tools/c2_readout/c2_config.py#L92) |  |
| `seed_flags` | function | `seed_flags` | [tools/x6_stage1/x6s1_decide.py:132](../../tools/x6_stage1/x6s1_decide.py#L132) |  |
| `seed_fresh` | function | `seed_fresh` | [tools/x6_stage1/x6s1_run.py:118](../../tools/x6_stage1/x6s1_run.py#L118) |  |
| `seed_input` | function | `seed_input` | [tests/executors/exec_helpers.py:17](../../tests/executors/exec_helpers.py#L17) | Save the MetricRecords input (value 10.0) of the stub jobs. |
| `seed_key` | function | `seed_key` | [tests/k4b/test_b_h1_meta.py:58](../../tests/k4b/test_b_h1_meta.py#L58) |  |
| `seed_search` | function | `seed_search` | [tools/hws/hws_driver.py:64](../../tools/hws/hws_driver.py#L64) | §6.6 G0 discovery search; excluded folders are pruned before any listing or open. |
| `seeded` | function | `seeded` | [tests/oracle_profile/test_oracle_profile_kernels.py:44](../../tests/oracle_profile/test_oracle_profile_kernels.py#L44) |  |
| `seeds` | function | `seeds` | [tests/learner/conftest.py:35](../../tests/learner/conftest.py#L35) |  |
| `SeedTree` | class | `SeedTree` | [src/topo_pilot/contracts/ids.py:99](../../src/topo_pilot/contracts/ids.py#L99) | Deterministic, platform-independent seed derivation (the only source of randomness). |
| `segment` | function | `segment` | [tools/x6_stage1/x6s1_pairs.py:86](../../tools/x6_stage1/x6s1_pairs.py#L86) |  |
| `segment_dp` | function | `segment_dp` | [tools/x6_stage0/x6_dp.py:18](../../tools/x6_stage0/x6_dp.py#L18) | Yield (n, {(v, kappa, g): count}) for n = 0..n_max (anchor-avoiding paths from ANCHOR). |
| `segment_stats` | function | `segment_stats` | [tests/x6_stage1/test_a_designed.py:74](../../tests/x6_stage1/test_a_designed.py#L74) |  |
| `select` | method | `SigmaCalibrator.select` | [src/topo_pilot/analysis/sigma.py:68](../../src/topo_pilot/analysis/sigma.py#L68) | Apply the rule to rows ordered by candidate priority (see class docstring). |
| `select` | function | `select` | [tests/analysis/test_sigma_calibrator.py:25](../../tests/analysis/test_sigma_calibrator.py#L25) |  |
| `select_anchors` | function | `select_anchors` | [src/topo_pilot/analysis/horizon_pools.py:34](../../src/topo_pilot/analysis/horizon_pools.py#L34) | Rows of the ``n`` ids with the smallest ``sha256(salt + id)`` (hex order), in that order. |
| `select_h1_bar` | function | `select_h1_bar` | [tools/x4_circle_history/chart.py:78](../../tools/x4_circle_history/chart.py#L78) | Index of the largest strictly positive finite lifetime; ties birth, death, index. |
| `select_smoothing` | method | `NGramBaseline.select_smoothing` | [src/topo_pilot/prediction/ngram.py:117](../../src/topo_pilot/prediction/ngram.py#L117) | Pick alpha minimising dev CE of ``w_33`` given ``w_1..w_32`` (D-021). |
| `selected_sigma` | function | `selected_sigma` | [src/topo_pilot/experiment/s3.py:313](../../src/topo_pilot/experiment/s3.py#L313) | The σ selected in S2 (MetricRecords row ``space=sigma, metric_id=selected``). |
| `selection` | function | `selection` | [tools/hws/hws_select.py:172](../../tools/hws/hws_select.py#L172) | §5.6 item 4: first ordinary qualifier in the frozen order; next two are the fallbacks. |
| `selection_record` | function | `selection_record` | [tools/hws/hws_records.py:322](../../tools/hws/hws_records.py#L322) | §10.1 hand-off package (written only for HWS_SELECTED, choice 32). |
| `Sensitivity` | class | `Sensitivity` | [src/topo_pilot/analysis/sensitivity.py:28](../../src/topo_pilot/analysis/sensitivity.py#L28) | Distance-matrix variants for the one-factor-at-a-time sensitivity stage (S7). |
| `sensitivity_table` | function | `sensitivity_table` | [src/topo_pilot/experiment/report_e4_s7.py:161](../../src/topo_pilot/experiment/report_e4_s7.py#L161) |  |
| `SensitivityJob` | class | `SensitivityJob` | [src/topo_pilot/experiment/s7_sensitivity.py:39](../../src/topo_pilot/experiment/s7_sensitivity.py#L39) | Writes one MetricRecords (``kind = sensitivity``). |
| `SentinelStop` | class | `SentinelStop` | [tools/hwsb/hwsb_train.py:81](../../tools/hwsb/hwsb_train.py#L81) | Raised by the checkpoint callback to stop training after a step (KB2, KB3). |
| `separation` | function | `separation` | [tools/c1prime/c1_data.py:80](../../tools/c1prime/c1_data.py#L80) |  |
| `separation` | function | `separation` | [tools/c2_readout/c2_registry.py:360](../../tools/c2_readout/c2_registry.py#L360) | Every split's role union (H^Y where defined) disjoint from R and from every other split; ids |
| `separation` | function | `separation` | [tools/hwsb/hwsb_registry.py:61](../../tools/hwsb/hwsb_registry.py#L61) |  |
| `separation` | function | `separation` | [tools/x6_stage1/x6s1_registry.py:437](../../tools/x6_stage1/x6s1_registry.py#L437) | §6.5 on every row: test ∩ REG2 = ∅ per arm; tests pairwise disjoint; val ∩ (REG1 ∪ train ∪ |
| `separation_cal_val` | function | `separation_cal_val` | [tools/k4b/k4b_data.py:150](../../tools/k4b/k4b_data.py#L150) |  |
| `separation_fresh` | function | `separation_fresh` | [tools/k4b/k4b_data.py:154](../../tools/k4b/k4b_data.py#L154) |  |
| `seq_disjoint` | function | `seq_disjoint` | [tools/k4b/k4b_data.py:160](../../tools/k4b/k4b_data.py#L160) |  |
| `SeqClock` | class | `SeqClock` | [tests/circle_history/test_cochain_chart_v24.py:89](../../tests/circle_history/test_cochain_chart_v24.py#L89) | Returns `values` in order, then `tail` forever; counts readings. |
| `sequence_ids` | function | `sequence_ids` | [src/topo_pilot/experiment/x4b2.py:56](../../src/topo_pilot/experiment/x4b2.py#L56) | ``(process_code << 32) \| (5 << 28) \| index`` in namespace ``x4b2-v1:<role>``. |
| `sequence_ids` | function | `sequence_ids` | [src/topo_pilot/experiment/x5g1_lineage.py:52](../../src/topo_pilot/experiment/x5g1_lineage.py#L52) | ``(process_code(..., "x5g1-v1:calibration:" + arm) << 32) \| (8 << 28) \| index``. |
| `sequence_ids` | function | `sequence_ids` | [src/topo_pilot/experiment/x5g1t_lineage.py:50](../../src/topo_pilot/experiment/x5g1t_lineage.py#L50) | ``(process_code(..., f"{NAMESPACE}:{split}:{arm}:{master}") << 32) \| (code << 28) \| i``. |
| `sequence_ids` | function | `sequence_ids` | [tools/c1prime/c1_data.py:27](../../tools/c1prime/c1_data.py#L27) |  |
| `sequence_ids` | function | `sequence_ids` | [tools/c2_readout/c2_data.py:43](../../tools/c2_readout/c2_data.py#L43) |  |
| `sequence_ids` | function | `sequence_ids` | [tools/d2a/d2a_world.py:105](../../tools/d2a/d2a_world.py#L105) |  |
| `sequence_ids` | function | `sequence_ids` | [tools/hwsb/hwsb_data.py:174](../../tools/hwsb/hwsb_data.py#L174) |  |
| `sequence_ids` | function | `sequence_ids` | [tools/k4b/k4b_data.py:78](../../tools/k4b/k4b_data.py#L78) |  |
| `sequence_ids` | function | `sequence_ids` | [tools/x6_stage1/x6s1_data.py:209](../../tools/x6_stage1/x6s1_data.py#L209) |  |
| `SequenceLayout` | class | `SequenceLayout` | [src/topo_pilot/contracts/layout.py:13](../../src/topo_pilot/contracts/layout.py#L13) | Alignment between observed symbols, model positions, targets, and oracle quantities. |
| `serialise` | function | `serialise` | [tools/c1prime/c1_chart.py:147](../../tools/c1prime/c1_chart.py#L147) |  |
| `serialise_state` | function | `serialise_state` | [src/topo_pilot/learner/stage.py:29](../../src/topo_pilot/learner/stage.py#L29) | ``torch.save({"model": ...[, "optimizer", "scheduler"]})`` into bytes. |
| `set_at` | function | `set_at` | [tests/k4b/test_b_h1_meta.py:86](../../tests/k4b/test_b_h1_meta.py#L86) |  |
| `set_attr` | function | `set_attr` | [tests/hwsb/test_b_process.py:145](../../tests/hwsb/test_b_process.py#L145) |  |
| `set_control` | function | `set_control` | [tools/x4_oracle_profile/synthetic_child.py:16](../../tools/x4_oracle_profile/synthetic_child.py#L16) |  |
| `set_gap` | function | `set_gap` | [tools/x6_stage0/x6_exact.py:222](../../tools/x6_stage0/x6_exact.py#L222) |  |
| `set_precision` | function | `set_precision` | [tools/x6_stage1/x6s1_cloud.py:143](../../tools/x6_stage1/x6s1_cloud.py#L143) |  |
| `set_threads` | function | `set_threads` | [tools/hwsb/hwsb_train.py:56](../../tools/hwsb/hwsb_train.py#L56) |  |
| `set_threads` | function | `set_threads` | [tools/x6_stage1/x6s1_eval.py:42](../../tools/x6_stage1/x6s1_eval.py#L42) |  |
| `setup_split` | function | `setup_split` | [tools/c1prime/c1_driver_late.py:27](../../tools/c1prime/c1_driver_late.py#L27) | Models, frozen fits and split rows (activations only) for validation or fresh. |
| `sg` | function | `sg` | [tools/c2_readout/c2_stage_val.py:130](../../tools/c2_readout/c2_stage_val.py#L130) |  |
| `sh_page` | function | `sh_page` | [tools/code_index/render_pages.py:123](../../tools/code_index/render_pages.py#L123) |  |
| `sha` | function | `sha` | [tests/c1prime/test_a_release_meter.py:45](../../tests/c1prime/test_a_release_meter.py#L45) |  |
| `sha` | function | `sha` | [tests/hwsb/test_b_records.py:294](../../tests/hwsb/test_b_records.py#L294) |  |
| `sha` | function | `sha` | [tests/k4b/test_b_registry.py:39](../../tests/k4b/test_b_registry.py#L39) |  |
| `sha` | function | `sha` | [tests/k4b/test_b_rerun.py:33](../../tests/k4b/test_b_rerun.py#L33) |  |
| `sha` | function | `sha` | [tests/k4b/test_b_store_reader.py:52](../../tests/k4b/test_b_store_reader.py#L52) |  |
| `sha` | function | `sha` | [tests/x6_stage0/test_x6_stage0_dp.py:307](../../tests/x6_stage0/test_x6_stage0_dp.py#L307) |  |
| `sha` | function | `sha` | [tools/c1prime/materialise_protocol.py:29](../../tools/c1prime/materialise_protocol.py#L29) |  |
| `sha` | function | `sha` | [tools/c1prime_registry/c1_registry_sources.py:28](../../tools/c1prime_registry/c1_registry_sources.py#L28) |  |
| `sha` | function | `sha` | [tools/chart_diag/chart_diag.py:46](../../tools/chart_diag/chart_diag.py#L46) |  |
| `sha` | function | `sha` | [tools/x4_oracle_profile/freeze.py:63](../../tools/x4_oracle_profile/freeze.py#L63) |  |
| `sha256` | method | `DigestSet.sha256` | [tools/x6_stage1/x6s1_registry.py:163](../../tools/x6_stage1/x6s1_registry.py#L163) | sha256 of the sorted unique full digests (32 bytes each), concatenated. |
| `sha256` | function | `sha256` | [tools/x4_circle_history/stage_records.py:31](../../tools/x4_circle_history/stage_records.py#L31) |  |
| `sha256` | function | `sha256` | [tools/x4_oracle_profile/inputs.py:29](../../tools/x4_oracle_profile/inputs.py#L29) |  |
| `sha256_bytes` | function | `sha256_bytes` | [tools/x6_stage1/x6s1_cloud.py:95](../../tools/x6_stage1/x6s1_cloud.py#L95) |  |
| `sha256_file` | function | `sha256_file` | [tools/x6_stage0/x6_store.py:121](../../tools/x6_stage0/x6_store.py#L121) |  |
| `sha256_file` | function | `sha256_file` | [tools/x6_stage1/x6s1_cloud.py:99](../../tools/x6_stage1/x6s1_cloud.py#L99) |  |
| `sha256_json` | function | `sha256_json` | [tools/x6_stage1/x6s1_cloud.py:100](../../tools/x6_stage1/x6s1_cloud.py#L100) |  |
| `sha256_phase` | function | `sha256_phase` | [tools/x4_circle_history/scores.py:95](../../tools/x4_circle_history/scores.py#L95) |  |
| `sha_bytes` | function | `sha_bytes` | [tools/hws/hws_records.py:39](../../tools/hws/hws_records.py#L39) |  |
| `sha_phase` | function | `sha_phase` | [tools/k4b/k4b_scores.py:49](../../tools/k4b/k4b_scores.py#L49) |  |
| `shares` | function | `shares` | [tools/c2_readout/c2_attrib.py:324](../../tools/c2_readout/c2_attrib.py#L324) | psi_S, psi_Gamma, psi_rest and eta_S of one pair() result on its eligible rows. |
| `sharp_target` | function | `sharp_target` | [tools/x6_stage1/x6s1_decide.py:84](../../tools/x6_stage1/x6s1_decide.py#L84) |  |
| `short_tables` | function | `short_tables` | [tests/x6_stage1/test_a_pairs.py:136](../../tests/x6_stage1/test_a_pairs.py#L136) |  |
| `Show-Help` | function | `Show-Help` | [tasks.ps1:15](../../tasks.ps1#L15) |  |
| `shuffle_perm` | function | `shuffle_perm` | [tools/d2a/d2a_eval.py:107](../../tools/d2a/d2a_eval.py#L107) |  |
| `shuffled` | function | `shuffled` | [src/topo_pilot/experiment/x4f_gates.py:52](../../src/topo_pilot/experiment/x4f_gates.py#L52) | 20 shuffled-calibration-target refits through the identical pipeline; q95. |
| `shuffled_table_inputs` | function | `shuffled_table_inputs` | [tests/k4b/test_b_data.py:187](../../tests/k4b/test_b_data.py#L187) |  |
| `sigma_f` | method | `World.sigma_f` | [tools/hws/hws_worlds.py:88](../../tools/hws/hws_worlds.py#L88) |  |
| `sigma_table` | function | `sigma_table` | [src/topo_pilot/experiment/prereg.py:61](../../src/topo_pilot/experiment/prereg.py#L61) |  |
| `sigma_tok` | function | `sigma_tok` | [tools/x6_stage0/x6_model.py:156](../../tools/x6_stage0/x6_model.py#L156) |  |
| `SigmaCalibrator` | class | `SigmaCalibrator` | [src/topo_pilot/analysis/sigma.py:34](../../src/topo_pilot/analysis/sigma.py#L34) | Select sigma by the first-passing rule with a weak-context fallback. |
| `SigmaDecision` | class | `SigmaDecision` | [src/topo_pilot/analysis/sigma.py:25](../../src/topo_pilot/analysis/sigma.py#L25) | Outcome: ``status`` in ``ok \| weak_context \| stop_H3``; ``sigma`` is None on stop. |
| `SigmaRow` | class | `SigmaRow` | [src/topo_pilot/analysis/sigma.py:13](../../src/topo_pilot/analysis/sigma.py#L13) | Calibration measurements for one (sigma, world) pair (V symbols). |
| `sign` | function | `sign` | [tools/c2_readout/c2_decide.py:75](../../tools/c2_readout/c2_decide.py#L75) |  |
| `signature` | function | `signature` | [tools/affected_tests.py:41](../../tools/affected_tests.py#L41) | Return a comparable text signature of a top-level function or class. |
| `signature` | function | `signature` | [tools/code_index/pyinfo.py:53](../../tools/code_index/pyinfo.py#L53) |  |
| `size_text` | function | `size_text` | [tools/code_index/render_lists.py:15](../../tools/code_index/render_lists.py#L15) |  |
| `sizes_ok` | function | `sizes_ok` | [tools/x6_stage1/x6s1_stage_pre.py:143](../../tools/x6_stage1/x6s1_stage_pre.py#L143) | check_file_sizes lists no X6S1 file but the seven big modules (§13 items 28, 32, 37). |
| `small_checkpoint` | function | `small_checkpoint` | [tests/hwsb/test_b_e4path.py:200](../../tests/hwsb/test_b_e4path.py#L200) |  |
| `small_plan` | function | `small_plan` | [tests/hwsb/test_b_streams.py:275](../../tests/hwsb/test_b_streams.py#L275) |  |
| `small_tables` | function | `small_tables` | [tests/x6_stage1/test_a_numerics.py:91](../../tests/x6_stage1/test_a_numerics.py#L91) |  |
| `smoke_ingest` | function | `smoke_ingest` | [tools/x6_stage1/x6s1_stage_pre.py:398](../../tools/x6_stage1/x6s1_stage_pre.py#L398) | The four integrity gates on the smoke, the float64 forward (t = 32) on 1,024 smoke rows, |
| `smooth` | function | `smooth` | [tests/circle_history/test_cochain.py:233](../../tests/circle_history/test_cochain.py#L233) |  |
| `smooth_phase` | function | `smooth_phase` | [tools/x4_circle_history/cochain.py:238](../../tools/x4_circle_history/cochain.py#L238) | Least squares f (f[0] = 0) of \|\|beta + B f\|\|; phi = 2 pi f mod 2 pi (API.md). |
| `smoothing` | function | `smoothing` | [tests/c1prime/test_a_chart_exceptions.py:77](../../tests/c1prime/test_a_chart_exceptions.py#L77) |  |
| `smoothing_diagnostics` | function | `smoothing_diagnostics` | [tools/c1prime/c1_records.py:130](../../tools/c1prime/c1_records.py#L130) | f and residual from the failed smooth_phase frame (never rerun); None if unavailable. |
| `snap` | function | `snap` | [tests/x6_stage1/test_b_ingest_bundle.py:172](../../tests/x6_stage1/test_b_ingest_bundle.py#L172) |  |
| `snapshot` | function | `snapshot` | [tests/circle_history/test_chart.py:349](../../tests/circle_history/test_chart.py#L349) |  |
| `snapshot` | function | `snapshot` | [tests/hwsb/test_b_meter_law.py:308](../../tests/hwsb/test_b_meter_law.py#L308) |  |
| `snapshot` | function | `snapshot` | [tools/c1prime/c1_freeze.py:50](../../tools/c1prime/c1_freeze.py#L50) |  |
| `snapshot` | function | `snapshot` | [tools/x4_circle_history/freeze_bind.py:57](../../tools/x4_circle_history/freeze_bind.py#L57) |  |
| `snapshot` | function | `snapshot` | [tools/x4_oracle_profile/freeze.py:81](../../tools/x4_oracle_profile/freeze.py#L81) |  |
| `snapshot_bytes` | function | `snapshot_bytes` | [tools/x6_stage1/x6s1_cloud.py:191](../../tools/x6_stage1/x6s1_cloud.py#L191) |  |
| `softmax64` | function | `softmax64` | [tools/hwsb/hwsb_eval.py:47](../../tools/hwsb/hwsb_eval.py#L47) |  |
| `softmax_dec` | function | `softmax_dec` | [tests/hwsb/test_a_enclosure_proof.py:100](../../tests/hwsb/test_a_enclosure_proof.py#L100) |  |
| `softmax_enclosure` | function | `softmax_enclosure` | [tools/x4_circle_history/process_law.py:97](../../tools/x4_circle_history/process_law.py#L97) | (E_dec, lo, hi): every exact E*[s][j] lies in [E_dec/hi, E_dec/lo] (positive). |
| `softmax_enclosure_rounded` | function | `softmax_enclosure_rounded` | [tools/hwsb/hwsb_law.py:72](../../tools/hwsb/hwsb_law.py#L72) | (E_dec, lo, hi): every exact E*[s][j] lies in [E_dec/hi, E_dec/lo] (ENCLOSURE_PROOF). |
| `solve` | function | `solve` | [tests/k4b/test_a_prop1.py:38](../../tests/k4b/test_a_prop1.py#L38) |  |
| `some_prefixes` | function | `some_prefixes` | [tests/x6_stage1/test_a_designed.py:93](../../tests/x6_stage1/test_a_designed.py#L93) |  |
| `sorted_rows` | function | `sorted_rows` | [tests/topology/test_persistence.py:48](../../tests/topology/test_persistence.py#L48) |  |
| `source_a` | function | `source_a` | [tools/k4b/k4b_registry.py:144](../../tools/k4b/k4b_registry.py#L144) |  |
| `source_b` | function | `source_b` | [tools/k4b/k4b_registry.py:150](../../tools/k4b/k4b_registry.py#L150) |  |
| `source_c` | function | `source_c` | [tools/k4b/k4b_registry.py:154](../../tools/k4b/k4b_registry.py#L154) |  |
| `source_d` | function | `source_d` | [tools/k4b/k4b_registry.py:161](../../tools/k4b/k4b_registry.py#L161) |  |
| `source_e` | function | `source_e` | [tools/k4b/k4b_registry.py:205](../../tools/k4b/k4b_registry.py#L205) |  |
| `source_f` | function | `source_f` | [tools/k4b/k4b_registry.py:239](../../tools/k4b/k4b_registry.py#L239) | ObservationSet stores under other directories, canonicalised by their EmissionSpec perm |
| `source_identity` | function | `source_identity` | [tools/x4_oracle_profile/validation.py:181](../../tools/x4_oracle_profile/validation.py#L181) |  |
| `source_k` | function | `source_k` | [tools/k4b/k4b_registry_k.py:81](../../tools/k4b/k4b_registry_k.py#L81) | Classifies every file under k4b-store (§16 item 2 a-d); other non-empty -> INCOMPLETE. |
| `sources_digest` | function | `sources_digest` | [tools/code_index/scan.py:111](../../tools/code_index/scan.py#L111) |  |
| `SourceTampered` | class | `SourceTampered` | [src/topo_pilot/experiment/x5g1_safety.py:22](../../src/topo_pilot/experiment/x5g1_safety.py#L22) | A source artifact failed full-hash or payload verification. |
| `SpaceBuilder` | class | `SpaceBuilder` | [src/topo_pilot/analysis/spaces.py:35](../../src/topo_pilot/analysis/spaces.py#L35) | Builds :class:`PointSet` objects from stored artifacts. |
| `spec` | function | `spec` | [tests/x2a_stage0/test_x2a_stage0.py:106](../../tests/x2a_stage0/test_x2a_stage0.py#L106) |  |
| `spec` | function | `spec` | [tests/x6_stage0/test_x6_stage0.py:144](../../tests/x6_stage0/test_x6_stage0.py#L144) |  |
| `spec_checksums` | function | `spec_checksums` | [tools/hwsb/hwsb_data.py:133](../../tools/hwsb/hwsb_data.py#L133) |  |
| `spectral_embedding` | function | `spectral_embedding` | [src/topo_pilot/analysis/baselines.py:17](../../src/topo_pilot/analysis/baselines.py#L17) | Spectral embedding phi of the symbol transition matrix. |
| `spectrum_report` | function | `spectrum_report` | [src/topo_pilot/analysis/x5_kernel.py:55](../../src/topo_pilot/analysis/x5_kernel.py#L55) | Spectrum of a pi-reversible kernel and the bound |
| `SpectrumReport` | class | `SpectrumReport` | [src/topo_pilot/analysis/x5_kernel.py:43](../../src/topo_pilot/analysis/x5_kernel.py#L43) | Descending eigenvalues, ``gap = 1 - lam2``, ``abs_gap = 1 - max(\|lam2\|, \|lam_min\|)``, |
| `sphere` | method | `SyntheticShapes.sphere` | [src/topo_pilot/topology/shapes.py:101](../../src/topo_pilot/topology/shapes.py#L101) | Uniform points of the unit sphere ``S^dim`` in R^(dim+1). |
| `spies` | function | `spies` | [tests/experiment/test_x5g1t_config_checks.py:102](../../tests/experiment/test_x5g1t_config_checks.py#L102) |  |
| `spies` | function | `spies` | [tests/experiment/test_x5g1t_config_production.py:105](../../tests/experiment/test_x5g1t_config_production.py#L105) |  |
| `spies` | function | `spies` | [tests/experiment/test_x5g1t_config_synthetic.py:105](../../tests/experiment/test_x5g1t_config_synthetic.py#L105) |  |
| `split_check` | function | `split_check` | [tools/x2a_stage0/x2a_ph.py:102](../../tools/x2a_stage0/x2a_ph.py#L102) |  |
| `split_phases` | function | `split_phases` | [tests/circle_history/test_chart_extension.py:140](../../tests/circle_history/test_chart_extension.py#L140) | Phases for the 8 nearest of Q_BELOW (k3,k2,k4,k1,k5,k0,k6,k7): `at_zero` of them 0. |
| `split_profile` | function | `split_profile` | [tools/x4_oracle_profile/run_profile.py:37](../../tools/x4_oracle_profile/run_profile.py#L37) |  |
| `split_readout` | function | `split_readout` | [src/topo_pilot/analysis/readout.py:116](../../src/topo_pilot/analysis/readout.py#L116) | Split row-vectors into the readout-visible part and the null part. |
| `split_state` | function | `split_state` | [tools/x6_stage0/x6_model.py:70](../../tools/x6_stage0/x6_model.py#L70) |  |
| `split_states` | function | `split_states` | [tools/c1prime/c1_driver_cal.py:58](../../tools/c1prime/c1_driver_cal.py#L58) | phi, forced and control states, decodes and support for one model on one split. |
| `spy` | function | `spy` | [tests/hwsb/test_b_streams.py:180](../../tests/hwsb/test_b_streams.py#L180) |  |
| `spy` | function | `spy` | [tests/k4b/test_b_store_reader.py:197](../../tests/k4b/test_b_store_reader.py#L197) |  |
| `SqrtJS` | class | `SqrtJS` | [src/topo_pilot/topology/metrics.py:110](../../src/topo_pilot/topology/metrics.py#L110) | Square root of the Jensen-Shannon divergence (natural log); rows are distributions. |
| `square12` | function | `square12` | [tests/process/conftest.py:12](../../tests/process/conftest.py#L12) | 12 x 12 square (core-world size). |
| `square3` | function | `square3` | [tests/process/conftest.py:24](../../tests/process/conftest.py#L24) | 3 x 3 square. |
| `square_ring` | function | `square_ring` | [tests/circle_history/test_chart_extension.py:60](../../tests/circle_history/test_chart_extension.py#L60) | Boundary of [0,6]^2, counter-clockwise from (0,0): k0..5 bottom, k6..11 right |
| `SquareBuilder` | class | `SquareBuilder` | [src/topo_pilot/world/lattice.py:165](../../src/topo_pilot/world/lattice.py#L165) | Plain grid, no identifications: contractible, beta = (1, 0, 0), chi = 1. |
| `SSHExecutor` | class | `SSHExecutor` | [src/topo_pilot/executors/ssh.py:30](../../src/topo_pilot/executors/ssh.py#L30) | Runs a bundle on a reachable machine. Credentials come from the user's SSH config |
| `st` | function | `st` | [tools/d1_seam/d1_seam.py:37](../../tools/d1_seam/d1_seam.py#L37) |  |
| `Stage` | class | `Stage` | [src/topo_pilot/experiment/stages.py:31](../../src/topo_pilot/experiment/stages.py#L31) | A run stage: ``plan`` lists job descriptors; ``execute`` runs one, returns artifact ids. |
| `stage` | method | `ResolvedConfig.stage` | [src/topo_pilot/experiment/config.py:37](../../src/topo_pilot/experiment/config.py#L37) | The settings block of ``stage_id`` (empty if absent). |
| `stage` | method | `_Cfg.stage` | [tests/experiment/test_report_e3.py:104](../../tests/experiment/test_report_e3.py#L104) |  |
| `stage` | method | `_Cfg.stage` | [tests/experiment/test_s8_e4.py:195](../../tests/experiment/test_s8_e4.py#L195) |  |
| `stage0` | function | `stage0` | [tools/d2a/d2a_targets.py:365](../../tools/d2a/d2a_targets.py#L365) | CLI ``stage0``: S0, pools, gates in §10.6 order, STAGE0.json; returns the outcome. |
| `stage0_count_check` | function | `stage0_count_check` | [tools/x6_stage1/x6s1_data.py:301](../../tools/x6_stage1/x6s1_data.py#L301) |  |
| `stage0_counts` | function | `stage0_counts` | [tools/x6_stage1/x6s1_data.py:284](../../tools/x6_stage1/x6s1_data.py#L284) | Stage-0 G6 `hits` semantics (x6_run.gate_G6): E_cue = a cue in w_1..w_32; amb_nb = |
| `stage0_rows` | function | `stage0_rows` | [tools/x6_stage1/x6s1_registry.py:254](../../tools/x6_stage1/x6s1_registry.py#L254) | REG1 (a): regenerated stage-0 MC tokens per arm (NA counts checked) and the stage-0 |
| `stage0_value` | function | `stage0_value` | [tools/x6_stage1/x6s1_data.py:307](../../tools/x6_stage1/x6s1_data.py#L307) |  |
| `stage1_decision` | function | `stage1_decision` | [tools/d2a/d2a_decide.py:52](../../tools/d2a/d2a_decide.py#L52) |  |
| `stage1_main` | function | `stage1_main` | [tools/d2a/d2a_decide.py:169](../../tools/d2a/d2a_decide.py#L169) | CLI ``stage1``: learnability gate on val for H3-s1, H3-s2 (§6) plus descriptive R_π. |
| `stage3_data` | function | `stage3_data` | [tools/d2a/d2a_eval.py:259](../../tools/d2a/d2a_eval.py#L259) | Tokens, strata rows, positions and targets for cal and test (stage 3 only). |
| `stage3_main` | function | `stage3_main` | [tools/d2a/d2a_decide.py:340](../../tools/d2a/d2a_decide.py#L340) | CLI ``stage3`` (API §4): primary passes, decision, then budgeted secondary work. |
| `stage_b_cases` | function | `stage_b_cases` | [tests/hwsb/test_a_ladder.py:129](../../tests/hwsb/test_a_ladder.py#L129) |  |
| `stage_caps` | function | `stage_caps` | [tools/x4_circle_history/meter_bind.py:82](../../tools/x4_circle_history/meter_bind.py#L82) |  |
| `stage_charts` | function | `stage_charts` | [tools/x4_circle_history/runner.py:259](../../tools/x4_circle_history/runner.py#L259) |  |
| `stage_events` | function | `stage_events` | [tools/hws/hws_records.py:50](../../tools/hws/hws_records.py#L50) |  |
| `stage_export` | function | `stage_export` | [tools/x4_circle_history/runner.py:291](../../tools/x4_circle_history/runner.py#L291) |  |
| `stage_identity` | function | `stage_identity` | [tools/x4_circle_history/runner.py:64](../../tools/x4_circle_history/runner.py#L64) |  |
| `stage_oracle` | function | `stage_oracle` | [tools/x4_circle_history/runner.py:114](../../tools/x4_circle_history/runner.py#L114) |  |
| `stage_precision` | function | `stage_precision` | [tools/x4_circle_history/runner.py:282](../../tools/x4_circle_history/runner.py#L282) |  |
| `stage_spent` | function | `stage_spent` | [tools/d2a/d2a_train.py:154](../../tools/d2a/d2a_train.py#L154) |  |
| `stage_spent` | function | `stage_spent` | [tools/x4_circle_history/meter_bind.py:94](../../tools/x4_circle_history/meter_bind.py#L94) |  |
| `stage_tables` | function | `stage_tables` | [tests/k4b/test_b_store_reader.py:83](../../tests/k4b/test_b_store_reader.py#L83) |  |
| `StageFailure` | class | `StageFailure` | [src/topo_pilot/contracts/errors.py:54](../../src/topo_pilot/contracts/errors.py#L54) | The only exception type raised for invariant violations anywhere in the project. |
| `StageRefused` | class | `StageRefused` | [tools/x4_circle_history/stage_records.py:23](../../tools/x4_circle_history/stage_records.py#L23) | Out-of-order, repeated or integrity-failed stage invocation (no gate record). |
| `stages_so_far` | function | `stages_so_far` | [tools/x4_circle_history/stage_records.py:55](../../tools/x4_circle_history/stage_records.py#L55) |  |
| `standard_normal` | method | `_DuplicatingGenerator.standard_normal` | [tests/analysis/test_x4f_erasure_family.py:190](../../tests/analysis/test_x4f_erasure_family.py#L190) |  |
| `standardise` | function | `standardise` | [tools/c2_readout/c2_code.py:46](../../tools/c2_readout/c2_code.py#L46) |  |
| `standardise_nuisance` | function | `standardise_nuisance` | [tools/c1prime/c1_fit.py:21](../../tools/c1prime/c1_fit.py#L21) |  |
| `standardizer` | function | `standardizer` | [src/topo_pilot/analysis/x4f_scores.py:16](../../src/topo_pilot/analysis/x4f_scores.py#L16) | Fit-row mean and population std; columns with std <= 1e-12 get scale 1 (centred only). |
| `standin_cls` | function | `standin_cls` | [tests/activations/conftest.py:101](../../tests/activations/conftest.py#L101) |  |
| `StandInLM` | class | `StandInLM` | [tests/activations/conftest.py:23](../../tests/activations/conftest.py#L23) | Stand-in for ``learner.TransformerLM`` implementing only its public interface. |
| `star` | function | `star` | [tests/hwsb/test_b_meter_law.py:260](../../tests/hwsb/test_b_meter_law.py#L260) |  |
| `star` | function | `star` | [tests/hwsb/test_b_process.py:40](../../tests/hwsb/test_b_process.py#L40) |  |
| `start_reservation` | function | `start_reservation` | [tools/k4b/k4b_release.py:124](../../tools/k4b/k4b_release.py#L124) |  |
| `stat` | function | `stat` | [tests/x6_stage0/test_x6_stage0_dp.py:38](../../tests/x6_stage0/test_x6_stage0_dp.py#L38) |  |
| `stat_ref` | function | `stat_ref` | [tests/analysis/test_baselines_dynamics.py:76](../../tests/analysis/test_baselines_dynamics.py#L76) |  |
| `state` | function | `state` | [tests/c1prime/test_a_oracle.py:41](../../tests/c1prime/test_a_oracle.py#L41) |  |
| `state` | function | `state` | [tests/c1prime/test_a_oracle_named.py:38](../../tests/c1prime/test_a_oracle_named.py#L38) |  |
| `state` | function | `state` | [tests/hws/test_a_outcomes.py:99](../../tests/hws/test_a_outcomes.py#L99) |  |
| `state` | function | `state` | [tests/hwsb/test_a_outcomes.py:64](../../tests/hwsb/test_a_outcomes.py#L64) | An all-PASS state (API §6.5 keys); keyword arguments override. |
| `state` | function | `state` | [tests/oracle_profile/test_builder_controls.py:48](../../tests/oracle_profile/test_builder_controls.py#L48) |  |
| `state` | function | `state` | [tools/x2a_stage0/x2a_model.py:48](../../tools/x2a_stage0/x2a_model.py#L48) |  |
| `state` | function | `state` | [tools/x6_stage0/x6_model.py:68](../../tools/x6_stage0/x6_model.py#L68) |  |
| `state_sha` | function | `state_sha` | [tools/c1prime/c1_model.py:20](../../tools/c1prime/c1_model.py#L20) |  |
| `states` | function | `states` | [tools/c1prime/c1_driver_late.py:74](../../tools/c1prime/c1_driver_late.py#L74) |  |
| `stationary` | function | `stationary` | [tests/k4b/test_a_prop1.py:51](../../tests/k4b/test_a_prop1.py#L51) |  |
| `stationary` | function | `stationary` | [tests/k4b/test_a_theorem_a.py:42](../../tests/k4b/test_a_theorem_a.py#L42) |  |
| `statistic` | function | `statistic` | [tools/x6_stage0/x6_model.py:232](../../tools/x6_stage0/x6_model.py#L232) |  |
| `stats` | function | `stats` | [tools/x6_stage1/x6s1_stage_post.py:346](../../tools/x6_stage1/x6s1_stage_post.py#L346) |  |
| `Status` | class | `Status` | [src/topo_pilot/contracts/errors.py:41](../../src/topo_pilot/contracts/errors.py#L41) | Non-exception outcomes stored in results ("cannot decide" is a status, not an error). |
| `status` | method | `BundleExecutor.status` | [src/topo_pilot/executors/bundle.py:144](../../src/topo_pilot/executors/bundle.py#L144) | ``awaiting_user`` after submit, ``done`` after a successful fetch. |
| `status` | method | `Executor.status` | [src/topo_pilot/executors/base.py:64](../../src/topo_pilot/executors/base.py#L64) | Current state; ``awaiting_user`` means the user must move files by hand. |
| `status` | method | `LocalExecutor.status` | [src/topo_pilot/executors/local.py:86](../../src/topo_pilot/executors/local.py#L86) | ``running`` while the subprocess lives, then ``done`` (exit 0) or ``failed``. |
| `status` | method | `SSHExecutor.status` | [src/topo_pilot/executors/ssh.py:113](../../src/topo_pilot/executors/ssh.py#L113) | ``running`` until the remote ``exit_code`` file exists, then ``done`` or ``failed``. |
| `status` | function | `status` | [tests/k4b/test_a_decision.py:60](../../tests/k4b/test_a_decision.py#L60) |  |
| `status_cmd` | method | `SSHExecutor.status_cmd` | [src/topo_pilot/executors/ssh.py:83](../../src/topo_pilot/executors/ssh.py#L83) | ``ssh`` command printing the exit code, or ``running``. |
| `status_lines` | function | `status_lines` | [src/topo_pilot/experiment/cli.py:40](../../src/topo_pilot/experiment/cli.py#L40) | At most 40 lines: artifact counts per type, the latest verdict per gate, config hash. |
| `status_of` | function | `status_of` | [tools/c1prime/c1_config.py:53](../../tools/c1prime/c1_config.py#L53) | 'INCONCLUSIVE/SUPPORT' -> ('INCONCLUSIVE', 'SUPPORT'); 'PASS' -> ('PASS', None). |
| `status_of` | function | `status_of` | [tools/c2_readout/c2_config.py:88](../../tools/c2_readout/c2_config.py#L88) |  |
| `status_of` | function | `status_of` | [tools/hws/hws_driver.py:327](../../tools/hws/hws_driver.py#L327) | Choice 43 exception map. |
| `status_of` | function | `status_of` | [tools/hwsb/hwsb_driver.py:59](../../tools/hwsb/hwsb_driver.py#L59) | Choice 20 exception map. |
| `status_of` | function | `status_of` | [tools/k4b/k4b_config.py:100](../../tools/k4b/k4b_config.py#L100) |  |
| `stencil_filter` | function | `stencil_filter` | [tools/x2a_stage0/x2a_model.py:189](../../tools/x2a_stage0/x2a_model.py#L189) |  |
| `SteppingClock` | class | `SteppingClock` | [tests/circle_history/test_cochain_lift.py:123](../../tests/circle_history/test_cochain_lift.py#L123) | Reading k (k = 0, 1, ...) returns k * step. |
| `steps_in` | function | `steps_in` | [tests/hwsb/test_b_hold.py:166](../../tests/hwsb/test_b_hold.py#L166) |  |
| `stop_status` | function | `stop_status` | [tests/hwsb/test_a_learning.py:52](../../tests/hwsb/test_a_learning.py#L52) |  |
| `stop_status` | function | `stop_status` | [tests/hwsb/test_b_streams.py:34](../../tests/hwsb/test_b_streams.py#L34) |  |
| `Stopped` | class | `Stopped` | [tools/x4_oracle_profile/runtime.py:26](../../tools/x4_oracle_profile/runtime.py#L26) |  |
| `StopRequested` | class | `StopRequested` | [src/topo_pilot/experiment/x5g1_controls.py:14](../../src/topo_pilot/experiment/x5g1_controls.py#L14) | The mailbox STOP file exists. |
| `StopRequested` | class | `StopRequested` | [tools/x4_circle_history/live_context.py:26](../../tools/x4_circle_history/live_context.py#L26) | STOP or invalid runtime control observed at a safe boundary (not a gate result). |
| `store` | function | `store` | [tests/executors/conftest.py:37](../../tests/executors/conftest.py#L37) |  |
| `store` | function | `store` | [tests/experiment/test_report_e2.py:18](../../tests/experiment/test_report_e2.py#L18) |  |
| `store` | function | `store` | [tests/experiment/test_report_e3.py:30](../../tests/experiment/test_report_e3.py#L30) |  |
| `store` | function | `store` | [tests/experiment/test_report_x4.py:23](../../tests/experiment/test_report_x4.py#L23) |  |
| `store` | function | `store` | [tests/experiment/test_runner.py:32](../../tests/experiment/test_runner.py#L32) |  |
| `store` | function | `store` | [tests/experiment/test_x4.py:26](../../tests/experiment/test_x4.py#L26) |  |
| `store_admission` | function | `store_admission` | [tools/c2_readout/c2_data.py:281](../../tools/c2_readout/c2_data.py#L281) | G0 (vii): every store file is meter bookkeeping or recognised with its exact sha256; at |
| `store_and_id` | function | `store_and_id` | [tests/experiment/test_x5g1_controls.py:155](../../tests/experiment/test_x5g1_controls.py#L155) |  |
| `store_file_hashes` | function | `store_file_hashes` | [tools/c1prime_registry/c1_registry_sources.py:255](../../tools/c1prime_registry/c1_registry_sources.py#L255) | Content hash of every file of each scanned store (binding, not a filename listing). |
| `store_ids` | function | `store_ids` | [tests/learner/test_checkpoint.py:23](../../tests/learner/test_checkpoint.py#L23) |  |
| `store_lineage` | function | `store_lineage` | [tools/x6_stage1/x6s1_run.py:154](../../tools/x6_stage1/x6s1_run.py#L154) | §12 item 8: x6_store lineage + static files + earlier accepted outputs (relpath → sha). |
| `store_sources` | function | `store_sources` | [tools/c1prime_registry/c1_registry_sources.py:98](../../tools/c1prime_registry/c1_registry_sources.py#L98) | Source (b): the stores named in §2.4(b), each recorded explicitly (empty ones included). |
| `stored_checkpoints` | method | `TrainingRun.stored_checkpoints` | [src/topo_pilot/experiment/s3.py:184](../../src/topo_pilot/experiment/s3.py#L184) | Ids of a complete stored run (exactly one checkpoint per step), else None. |
| `stored_model_config` | function | `stored_model_config` | [src/topo_pilot/experiment/x5g1_scorebench.py:66](../../src/topo_pilot/experiment/x5g1_scorebench.py#L66) | Read-only metadata assertion of the stored E3 checkpoint; returns (model_config, sha). |
| `stored_sequence_ids` | function | `stored_sequence_ids` | [src/topo_pilot/experiment/x4b2.py:135](../../src/topo_pilot/experiment/x4b2.py#L135) | Every sequence id of every ObservationSet in ``store``. |
| `stored_timing` | method | `TrainingRun.stored_timing` | [src/topo_pilot/experiment/s3.py:208](../../src/topo_pilot/experiment/s3.py#L208) | Timing of the training that produced ``ckpt_ids``, from any MetricRecords of |
| `stored_value_checks` | function | `stored_value_checks` | [tools/x4_oracle_profile/validation.py:64](../../tools/x4_oracle_profile/validation.py#L64) |  |
| `StoreResolver` | class | `StoreResolver` | [src/topo_pilot/experiment/x4_inputs.py:78](../../src/topo_pilot/experiment/x4_inputs.py#L78) | ``resolver(source_stage) -> (runs, missing run keys)`` over the stored runs of a stage. |
| `stores` | function | `stores` | [src/topo_pilot/experiment/x5g1t_stages.py:66](../../src/topo_pilot/experiment/x5g1t_stages.py#L66) | (read-only sources, read-through study store writing only to ``study_root/store``). |
| `stores` | function | `stores` | [tests/hwsb/test_b_e4path.py:105](../../tests/hwsb/test_b_e4path.py#L105) |  |
| `strat_mean_se` | function | `strat_mean_se` | [tools/x2a_stage0/x2a_mc.py:60](../../tools/x2a_stage0/x2a_mc.py#L60) |  |
| `strata_rows` | function | `strata_rows` | [tools/d2a/d2a_eval.py:177](../../tools/d2a/d2a_eval.py#L177) | {stratum: (rows, positions)} for t = 16, t = 28 and the three bins. |
| `stray` | function | `stray` | [tests/k4b/test_b_store_reader.py:91](../../tests/k4b/test_b_store_reader.py#L91) |  |
| `stream` | function | `stream` | [src/topo_pilot/experiment/x5g1t_lineage.py:27](../../src/topo_pilot/experiment/x5g1t_lineage.py#L27) |  |
| `stream` | function | `stream` | [tools/c2_readout/c2_stage_post.py:166](../../tools/c2_readout/c2_stage_post.py#L166) | The whole family stream of one admitted model (§11.1), its guards (§9.2; M: C-44) and the |
| `stream` | function | `stream` | [tools/d2a/d2a_world.py:94](../../tools/d2a/d2a_world.py#L94) |  |
| `stream_bounds` | function | `stream_bounds` | [tools/c2_readout/c2_decide.py:38](../../tools/c2_readout/c2_decide.py#L38) | One shared index stream; per key the tree mean and the ranked bounds at alpha, 1 - alpha. |
| `stream_guards` | function | `stream_guards` | [tools/c2_readout/c2_decide.py:79](../../tools/c2_readout/c2_decide.py#L79) | Guards of one R/S* stream; geo: M, x/y = (d, dy, E), proj = {prefix: (P_S, delta_P)}. |
| `stream_record` | function | `stream_record` | [tools/hwsb/hwsb_data.py:161](../../tools/hwsb/hwsb_data.py#L161) |  |
| `strict_verdict` | function | `strict_verdict` | [src/topo_pilot/analysis/horizon_pools.py:174](../../src/topo_pilot/analysis/horizon_pools.py#L174) | SUFFICIENT_AMBIENT iff the ambient map factorizes; otherwise UNRESOLVED (numerical |
| `strings` | function | `strings` | [tests/oracle_profile/test_oracle_profile.py:71](../../tests/oracle_profile/test_oracle_profile.py#L71) | All V**length observation strings. |
| `strings` | function | `strings` | [tests/oracle_profile/test_oracle_profile_traps.py:48](../../tests/oracle_profile/test_oracle_profile_traps.py#L48) |  |
| `strip_volatile` | function | `strip_volatile` | [tools/x6_stage0/x6_store.py:204](../../tools/x6_stage0/x6_store.py#L204) |  |
| `StubStage` | class | `StubStage` | [tests/executors/stub_stage.py:23](../../tests/executors/stub_stage.py#L23) | Writes one tiny artifact so executors can be tested without science code. |
| `study_export` | function | `study_export` | [src/topo_pilot/experiment/x5g1t_exports.py:44](../../src/topo_pilot/experiment/x5g1t_exports.py#L44) | Guarded JSON files, npz arrays, manifest and COMPLETE status (in that order). |
| `study_pool_config` | function | `study_pool_config` | [src/topo_pilot/experiment/x5g1t_lineage.py:81](../../src/topo_pilot/experiment/x5g1t_lineage.py#L81) | Metadata of a NEW study pool (API v4.1 §A): ``lineage_protocol`` names the frozen |
| `study_run_key` | function | `study_run_key` | [src/topo_pilot/experiment/x5g1t_train.py:38](../../src/topo_pilot/experiment/x5g1t_train.py#L38) | The same for both arms of a pair: identical init and batch order. |
| `study_stop` | function | `study_stop` | [tools/x6_stage1/x6s1_run.py:255](../../tools/x6_stage1/x6s1_run.py#L255) |  |
| `study_train_config` | function | `study_train_config` | [src/topo_pilot/experiment/x5g1t_train.py:33](../../src/topo_pilot/experiment/x5g1t_train.py#L33) | Stored E3 values except ``checkpoint_steps`` = the grid and ``device = "cpu"``. |
| `StudyConfig` | class | `StudyConfig` | [src/topo_pilot/experiment/x5g1t_config.py:50](../../src/topo_pilot/experiment/x5g1t_config.py#L50) |  |
| `StudyControls` | class | `StudyControls` | [src/topo_pilot/experiment/x5g1t_runtime.py:223](../../src/topo_pilot/experiment/x5g1t_runtime.py#L223) | Guard, controls (with live hold), boundary budget and resources at one boundary. |
| `StudyFailed` | class | `StudyFailed` | [src/topo_pilot/experiment/x5g1t_stages.py:62](../../src/topo_pilot/experiment/x5g1t_stages.py#L62) | Collision, prerequisite or authorisation failure (not a scientific verdict). |
| `sub` | function | `sub` | [tests/x6_stage1/test_a_designed.py:85](../../tests/x6_stage1/test_a_designed.py#L85) |  |
| `sub` | function | `sub` | [tests/x6_stage1/test_a_pairs.py:153](../../tests/x6_stage1/test_a_pairs.py#L153) |  |
| `submit` | method | `BundleExecutor.submit` | [src/topo_pilot/executors/bundle.py:126](../../src/topo_pilot/executors/bundle.py#L126) | Write the bundle; the job is then ``awaiting_user``. |
| `submit` | method | `Executor.submit` | [src/topo_pilot/executors/base.py:60](../../src/topo_pilot/executors/base.py#L60) | Start (or prepare) the job. |
| `submit` | method | `LocalExecutor.submit` | [src/topo_pilot/executors/local.py:64](../../src/topo_pilot/executors/local.py#L64) | Start the subprocess; ``store`` must be a ``LocalFSBackend`` store. |
| `submit` | method | `SSHExecutor.submit` | [src/topo_pilot/executors/ssh.py:103](../../src/topo_pilot/executors/ssh.py#L103) | Build the bundle, copy it over, and start it remotely. |
| `submitted` | function | `submitted` | [tests/executors/test_bundle.py:45](../../tests/executors/test_bundle.py#L45) |  |
| `submodules` | method | `Resolver.submodules` | [tools/code_index/resolve.py:92](../../tools/code_index/resolve.py#L92) | Targets of `from M import names`: submodule files where they exist, else M. |
| `suffix_enumeration` | function | `suffix_enumeration` | [tools/hws/hws_exact.py:177](../../tools/hws/hws_exact.py#L177) |  |
| `suffix_posterior` | function | `suffix_posterior` | [tools/x4_oracle_profile/oracle_profile.py:128](../../tools/x4_oracle_profile/oracle_profile.py#L128) | ``[n, S]`` normalised filtering posteriors ``P(z_L \| w_{L-K+1:L})``, stationary restart. |
| `sum_ordered` | function | `sum_ordered` | [tests/c1prime/test_b_cert_bounds.py:82](../../tests/c1prime/test_b_cert_bounds.py#L82) |  |
| `Summaries` | class | `Summaries` | [src/topo_pilot/topology/summaries.py:15](../../src/topo_pilot/topology/summaries.py#L15) | Summaries of a ``DiagramResult`` (or an ``[n, 4]`` rows array); all are pure. |
| `summarise` | function | `summarise` | [tools/x2a_stage0/x2a_mc.py:153](../../tools/x2a_stage0/x2a_mc.py#L153) |  |
| `summarise` | function | `summarise` | [tools/x4_oracle_profile/run_profile.py:65](../../tools/x4_oracle_profile/run_profile.py#L65) |  |
| `summarize` | function | `summarize` | [src/topo_pilot/experiment/circ_audit.py:171](../../src/topo_pilot/experiment/circ_audit.py#L171) | Per-run counts and the frozen reading (all 3 / 0 / mixed). |
| `summary` | method | `CircularJob.summary` | [src/topo_pilot/experiment/s7_circular.py:80](../../src/topo_pilot/experiment/s7_circular.py#L80) |  |
| `summary` | function | `summary` | [tools/hws/hws_stats.py:45](../../tools/hws/hws_stats.py#L45) |  |
| `summary` | function | `summary` | [tools/k4b/k4b_registry_k.py:113](../../tools/k4b/k4b_registry_k.py#L113) | Manifest `k4b_store` (§16 item 4): counts and sha256s per group; None -> not read. |
| `supersede` | function | `supersede` | [tools/c2_readout/c2_driver.py:316](../../tools/c2_readout/c2_driver.py#L316) |  |
| `supervise` | function | `supervise` | [tools/x4_oracle_profile/meter.py:114](../../tools/x4_oracle_profile/meter.py#L114) | Run cmd in the job; return only after the job has NO active process. |
| `supervise` | function | `supervise` | [tools/x6_stage1/x6s1_run.py:310](../../tools/x6_stage1/x6s1_run.py#L310) | Poll every `poll_s` until every child has exited (§4.6, S6); STOP/HOLD at each poll. |
| `Supervisor` | class | `Supervisor` | [tools/d2a/d2a_train.py:168](../../tools/d2a/d2a_train.py#L168) | Polling per-model CPU, per-process memory and stage/total budget enforcement (S6). |
| `supervisor` | method | `Procs.supervisor` | [tests/d2a/test_b_resource.py:181](../../tests/d2a/test_b_resource.py#L181) |  |
| `support` | function | `support` | [tools/c2_readout/c2_stage_base.py:299](../../tools/c2_readout/c2_stage_base.py#L299) | UNSUPPORTED_H/PLUS/MINUS counts (§5.5; rows kept and phased) and Sup(H). |
| `support` | function | `support` | [tools/hwsb/hwsb_eval.py:172](../../tools/hwsb/hwsb_eval.py#L172) |  |
| `support_entries` | function | `support_entries` | [tools/k4b/k4b_scores.py:157](../../tools/k4b/k4b_scores.py#L157) |  |
| `support_gate` | function | `support_gate` | [src/topo_pilot/analysis/x4f_scores.py:126](../../src/topo_pilot/analysis/x4f_scores.py#L126) | ``frac_primary <= 0.05`` and ``<= 2 * median(fracs_random)`` (literal at median 0). |
| `support_inputs` | function | `support_inputs` | [tests/k4b/test_b_flow.py:81](../../tests/k4b/test_b_flow.py#L81) |  |
| `support_reasons` | function | `support_reasons` | [tools/k4b/k4b_scores.py:82](../../tools/k4b/k4b_scores.py#L82) |  |
| `support_report` | function | `support_report` | [src/topo_pilot/analysis/x4f_scores.py:102](../../src/topo_pilot/analysis/x4f_scores.py#L102) | Mahalanobis support of patched vectors against the calibration Ledoit-Wolf law. |
| `support_report` | function | `support_report` | [tools/k4b/k4b_scores.py:104](../../tools/k4b/k4b_scores.py#L104) | §10 support report; the sealed form omits the supported contribution (§7.5). |
| `supports` | function | `supports` | [tools/c1prime/c1_cert.py:55](../../tools/c1prime/c1_cert.py#L55) |  |
| `survival` | function | `survival` | [tools/c2_readout/c2_stage_pre.py:292](../../tools/c2_readout/c2_stage_pre.py#L292) | Each family needs >= 2 ok models; the FEAS per-model, per-family coverage tally. |
| `svg` | function | `svg` | [reports/he_summary/charts.py:57](../../reports/he_summary/charts.py#L57) |  |
| `Sym` | class | `Sym` | [tools/c1prime/c1_bounds.py:109](../../tools/c1prime/c1_bounds.py#L109) | Counting value for L5: nodes, formal monomials (with multiplicity) and degree. |
| `symbol_law` | function | `symbol_law` | [tools/hws/hws_exact.py:35](../../tools/hws/hws_exact.py#L35) |  |
| `symbol_only_bound` | function | `symbol_only_bound` | [src/topo_pilot/analysis/circular_bound.py:17](../../src/topo_pilot/analysis/circular_bound.py#L17) | Largest agreement any function of ``symbols`` can reach with ``theta`` on these rows. |
| `symbol_order_a` | function | `symbol_order_a` | [tools/c2_readout/c2_model.py:207](../../tools/c2_readout/c2_model.py#L207) | (a): the named input tokens are perm[w], by the independent inverse route canonical32. |
| `symbol_order_b` | function | `symbol_order_b` | [tools/c2_readout/c2_model.py:215](../../tools/c2_readout/c2_model.py#L215) | (b): named_from_canonical(e_c, perm) = e_{perm[c]} for every canonical c (bitwise). |
| `symbol_order_c` | function | `symbol_order_c` | [tools/c2_readout/c2_model.py:221](../../tools/c2_readout/c2_model.py#L221) | (c): canonical_from_named_cols(named_from_canonical(d, perm), perm) = d (bitwise). |
| `symbol_perm` | function | `symbol_perm` | [tools/theory_exact/sym_check.py:63](../../tools/theory_exact/sym_check.py#L63) | s with E[g z, s(w)] == E[z, w] for all z, w, or None. |
| `symbol_sizes` | function | `symbol_sizes` | [tools/hws/hws_worlds.py:166](../../tools/hws/hws_worlds.py#L166) |  |
| `symbols` | function | `symbols` | [tools/code_index/pyinfo.py:157](../../tools/code_index/pyinfo.py#L157) |  |
| `symbols_section` | function | `symbols_section` | [tools/code_index/render_pages.py:79](../../tools/code_index/render_pages.py#L79) |  |
| `symmetry_check` | function | `symmetry_check` | [tools/hws/hws_worlds.py:305](../../tools/hws/hws_worlds.py#L305) |  |
| `symmetry_group` | function | `symmetry_group` | [tools/theory_exact/theory_exact.py:47](../../tools/theory_exact/theory_exact.py#L47) |  |
| `symmetry_report` | function | `symmetry_report` | [tools/c1prime/c1_oracle.py:61](../../tools/c1prime/c1_oracle.py#L61) |  |
| `syn` | function | `syn` | [tests/experiment/test_x5g1t_config_synthetic.py:204](../../tests/experiment/test_x5g1t_config_synthetic.py#L204) |  |
| `sync_ledger_caps` | function | `sync_ledger_caps` | [tools/x4_circle_history/meter_bind.py:146](../../tools/x4_circle_history/meter_bind.py#L146) | Apply the recorded CONTRACT allocation and CPU policy to the ledger metadata (entries |
| `synth_state` | function | `synth_state` | [tests/x6_stage1/test_a_eval.py:50](../../tests/x6_stage1/test_a_eval.py#L50) |  |
| `synthetic_chart` | function | `synthetic_chart` | [tests/c1prime/test_a_chart_val.py:41](../../tests/c1prime/test_a_chart_val.py#L41) |  |
| `synthetic_process` | function | `synthetic_process` | [tests/k4b/test_b_data.py:38](../../tests/k4b/test_b_data.py#L38) |  |
| `synthetic_process` | function | `synthetic_process` | [tools/x4_circle_history/cost_probe.py:28](../../tools/x4_circle_history/cost_probe.py#L28) |  |
| `synthetic_repo` | function | `synthetic_repo` | [tests/hwsb/test_b_records.py:298](../../tests/hwsb/test_b_records.py#L298) |  |
| `synthetic_root` | function | `synthetic_root` | [tests/hwsb/test_b_records.py:154](../../tests/hwsb/test_b_records.py#L154) |  |
| `SyntheticShapes` | class | `SyntheticShapes` | [src/topo_pilot/topology/shapes.py:55](../../src/topo_pilot/topology/shapes.py#L55) | Samples of shapes with known Betti numbers, embedded in ``R^ambient``. |
| `T` | function | `T` | [reports/he_summary/charts.py:32](../../reports/he_summary/charts.py#L32) | Text with a *visual* anchor: 'left' = text starts at x and runs right, |
| `t_base_exact` | function | `t_base_exact` | [tools/x6_stage0/x6_model.py:144](../../tools/x6_stage0/x6_model.py#L144) |  |
| `t_pre` | function | `t_pre` | [tools/c2_readout/c2_stage_post.py:63](../../tools/c2_readout/c2_stage_post.py#L63) | §7 row 23 in order; FAIL_TECHNICAL ends it at once, unmet criteria give TEST_GATE. |
| `t_pre` | function | `t_pre` | [tools/k4b/k4b_fresh.py:114](../../tools/k4b/k4b_fresh.py#L114) | Oracle + references on every test row; determinism; extension; certificate; fresh B4. |
| `t_pre_model` | function | `t_pre_model` | [tools/c2_readout/c2_stage_post.py:100](../../tools/c2_readout/c2_stage_post.py#L100) | §7 row 24: Sup(TEST), L1 and R1 with the frozen FIT decoders, N2 (M); TEST tallies. |
| `table` | function | `table` | [tools/c2_readout/c2_stage_base.py:81](../../tools/c2_readout/c2_stage_base.py#L81) |  |
| `table_digests` | function | `table_digests` | [tools/c2_readout/c2_data.py:137](../../tools/c2_readout/c2_data.py#L137) |  |
| `table_entry` | function | `table_entry` | [tools/x6_stage1/x6s1_stats.py:101](../../tools/x6_stage1/x6s1_stats.py#L101) |  |
| `table_roles` | function | `table_roles` | [tools/c2_readout/c2_data.py:133](../../tools/c2_readout/c2_data.py#L133) |  |
| `table_union` | function | `table_union` | [tools/c1prime/c1_data.py:66](../../tools/c1prime/c1_data.py#L66) |  |
| `tables` | function | `tables` | [src/topo_pilot/experiment/x5g1t_stages.py:103](../../src/topo_pilot/experiment/x5g1t_stages.py#L103) |  |
| `tables` | function | `tables` | [tests/hwsb/test_b_streams.py:335](../../tests/hwsb/test_b_streams.py#L335) |  |
| `tables_bytes` | function | `tables_bytes` | [tools/x6_stage1/x6s1_pairs.py:52](../../tools/x6_stage1/x6s1_pairs.py#L52) |  |
| `tail` | function | `tail` | [tools/x6_stage1/x6s1_stats.py:190](../../tools/x6_stage1/x6s1_stats.py#L190) |  |
| `tail_identity` | function | `tail_identity` | [tools/c1prime/c1_model.py:94](../../tools/c1prime/c1_model.py#L94) |  |
| `tail_logits` | function | `tail_logits` | [tools/c1prime/c1_model.py:80](../../tools/c1prime/c1_model.py#L80) |  |
| `tamper_tar` | function | `tamper_tar` | [tests/executors/exec_helpers.py:32](../../tests/executors/exec_helpers.py#L32) | Copy a bundle, bumping the first metric value inside every ``extra.json`` that has rows |
| `tangent_audit` | function | `tangent_audit` | [src/topo_pilot/analysis/horizon.py:146](../../src/topo_pilot/analysis/horizon.py#L146) | Does ``G2`` vanish on the sum-zero kernel of ``G1``? |
| `TangentAudit` | class | `TangentAudit` | [src/topo_pilot/analysis/horizon.py:113](../../src/topo_pilot/analysis/horizon.py#L113) | Ambient tangent-kernel audit; ``verdict`` in ALLOWS_STABLE / FACTORIZES / |
| `target` | method | `SSHExecutor.target` | [src/topo_pilot/executors/ssh.py:61](../../src/topo_pilot/executors/ssh.py#L61) | ``user@host`` or ``host``. |
| `target` | function | `target` | [tools/c2_readout/c2_stage_base.py:239](../../tools/c2_readout/c2_stage_base.py#L239) |  |
| `target_threshold` | function | `target_threshold` | [tools/x6_stage1/x6s1_data.py:340](../../tools/x6_stage1/x6s1_data.py#L340) |  |
| `targets` | method | `SequenceLayout.targets` | [src/topo_pilot/contracts/layout.py:59](../../src/topo_pilot/contracts/layout.py#L59) | ``[w_1..w_33]`` per row: ``[R, 33] -> [R, 33]``, dtype int64 (a copy). |
| `targets_for` | function | `targets_for` | [tools/d2a/d2a_eval.py:188](../../tools/d2a/d2a_eval.py#L188) | Probe targets and ceiling features at (rows, positions) (§3, §7.3). |
| `tarjan` | function | `tarjan` | [tools/code_index/model.py:29](../../tools/code_index/model.py#L29) | Iterative Tarjan SCC; returns the list of components (each a sorted list). |
| `tau` | function | `tau` | [tools/c1prime/c1_oracle.py:39](../../tools/c1prime/c1_oracle.py#L39) |  |
| `tau_ref` | function | `tau_ref` | [tests/c1prime/test_a_oracle.py:45](../../tests/c1prime/test_a_oracle.py#L45) |  |
| `tb` | function | `tb` | [tools/c2_readout/c2_stage_post.py:42](../../tools/c2_readout/c2_stage_post.py#L42) |  |
| `template_enumeration` | function | `template_enumeration` | [tools/d2a/d2a_world.py:140](../../tools/d2a/d2a_world.py#L140) | All equal-gap template pairs at t (§9.2), in the API.md order. |
| `template_hashes` | function | `template_hashes` | [tools/d2a/d2a_world.py:170](../../tools/d2a/d2a_world.py#L170) |  |
| `terminate` | method | `FakeTree.terminate` | [tests/x6_stage1/test_b_nb_s0_ops.py:291](../../tests/x6_stage1/test_b_nb_s0_ops.py#L291) |  |
| `terminate` | method | `TrainingProcess.terminate` | [tools/d2a/process_tree.py:78](../../tools/d2a/process_tree.py#L78) |  |
| `terminate_and_drain` | function | `terminate_and_drain` | [tools/x4_oracle_profile/winjob.py:167](../../tools/x4_oracle_profile/winjob.py#L167) | Terminate every job process and wait (bounded) until none is active. |
| `test_01_literal_conventions` | test | `test_01_literal_conventions` | [tests/x6_stage0/test_x6_stage0.py:148](../../tests/x6_stage0/test_x6_stage0.py#L148) |  |
| `test_02_kernel_lift_complexes_covers` | test | `test_02_kernel_lift_complexes_covers` | [tests/x6_stage0/test_x6_stage0.py:199](../../tests/x6_stage0/test_x6_stage0.py#L199) |  |
| `test_03_faces_flux_fstar` | test | `test_03_faces_flux_fstar` | [tests/x6_stage0/test_x6_stage0.py:249](../../tests/x6_stage0/test_x6_stage0.py#L249) |  |
| `test_04_witness_path_sums` | test | `test_04_witness_path_sums` | [tests/x6_stage0/test_x6_stage0.py:278](../../tests/x6_stage0/test_x6_stage0.py#L278) |  |
| `test_05_kgram_locality` | test | `test_05_kgram_locality` | [tests/x6_stage0/test_x6_stage0.py:322](../../tests/x6_stage0/test_x6_stage0.py#L322) |  |
| `test_06_zc_witness_and_ab_fixed_point` | test | `test_06_zc_witness_and_ab_fixed_point` | [tests/x6_stage0/test_x6_stage0_dp.py:71](../../tests/x6_stage0/test_x6_stage0_dp.py#L71) |  |
| `test_07_gauge_nocue_tokperm_eta1` | test | `test_07_gauge_nocue_tokperm_eta1` | [tests/x6_stage0/test_x6_stage0_dp.py:93](../../tests/x6_stage0/test_x6_stage0_dp.py#L93) |  |
| `test_08_dp_against_brute_force` | test | `test_08_dp_against_brute_force` | [tests/x6_stage0/test_x6_stage0_dp.py:129](../../tests/x6_stage0/test_x6_stage0_dp.py#L129) |  |
| `test_09_block_comparator` | test | `test_09_block_comparator` | [tests/x6_stage0/test_x6_stage0.py:344](../../tests/x6_stage0/test_x6_stage0.py#L344) |  |
| `test_10_decimal_inputs_pass_through` | test | `test_10_decimal_inputs_pass_through` | [tests/x6_stage0/test_x6_stage0_dp.py:169](../../tests/x6_stage0/test_x6_stage0_dp.py#L169) |  |
| `test_11_enclosures_certification_memo` | test | `test_11_enclosures_certification_memo` | [tests/x6_stage0/test_x6_stage0_dp.py:195](../../tests/x6_stage0/test_x6_stage0_dp.py#L195) |  |
| `test_12_outcome_logic` | test | `test_12_outcome_logic` | [tests/x6_stage0/test_x6_stage0_dp.py:243](../../tests/x6_stage0/test_x6_stage0_dp.py#L243) |  |
| `test_13_registry_and_geometry_guards` | test | `test_13_registry_and_geometry_guards` | [tests/x6_stage0/test_x6_stage0.py:374](../../tests/x6_stage0/test_x6_stage0.py#L374) |  |
| `test_14_file_line_limits` | test | `test_14_file_line_limits` | [tests/x6_stage0/test_x6_stage0.py:395](../../tests/x6_stage0/test_x6_stage0.py#L395) |  |
| `test_15_indicator_se_and_rs_keys` | test | `test_15_indicator_se_and_rs_keys` | [tests/x6_stage0/test_x6_stage0_dp.py:282](../../tests/x6_stage0/test_x6_stage0_dp.py#L282) |  |
| `test_16_rerun_and_lineage_rule` | test | `test_16_rerun_and_lineage_rule` | [tests/x6_stage0/test_x6_stage0_dp.py:311](../../tests/x6_stage0/test_x6_stage0_dp.py#L311) |  |
| `test_17_eta1_markers_manifests` | test | `test_17_eta1_markers_manifests` | [tests/x6_stage0/test_x6_stage0_dp.py:366](../../tests/x6_stage0/test_x6_stage0_dp.py#L366) |  |
| `test_A01_row_order_equals_index_order_for_any_batch_size` | test | `test_A01_row_order_equals_index_order_for_any_batch_size` | [tests/activations/test_activations.py:35](../../tests/activations/test_activations.py#L35) |  |
| `test_a020_c_max_closed_form_and_entries` | test | `test_a020_c_max_closed_form_and_entries` | [tests/process/test_conductance.py:171](../../tests/process/test_conductance.py#L171) |  |
| `test_a020_connected` | test | `test_a020_connected` | [tests/process/test_conductance.py:164](../../tests/process/test_conductance.py#L164) |  |
| `test_a020_kernel_validity` | test | `test_a020_kernel_validity` | [tests/process/test_conductance.py:137](../../tests/process/test_conductance.py#L137) |  |
| `test_a020_support_only_edges_and_diagonal` | test | `test_a020_support_only_edges_and_diagonal` | [tests/process/test_conductance.py:153](../../tests/process/test_conductance.py#L153) |  |
| `test_A02_logits_equal_plain_forward_at_position_32` | test | `test_A02_logits_equal_plain_forward_at_position_32` | [tests/activations/test_activations.py:53](../../tests/activations/test_activations.py#L53) |  |
| `test_A03_w33_invisible_w32_visible` | test | `test_A03_w33_invisible_w32_visible` | [tests/activations/test_activations.py:67](../../tests/activations/test_activations.py#L67) |  |
| `test_A04_numerical_failure_when_hooked_path_disagrees` | test | `test_A04_numerical_failure_when_hooked_path_disagrees` | [tests/activations/test_activations.py:96](../../tests/activations/test_activations.py#L96) |  |
| `test_A04_unknown_hook_and_corrupted_hash` | test | `test_A04_unknown_hook_and_corrupted_hash` | [tests/activations/test_activations.py:79](../../tests/activations/test_activations.py#L79) |  |
| `test_A05_panel_filter_returns_exactly_the_panel_ids` | test | `test_A05_panel_filter_returns_exactly_the_panel_ids` | [tests/activations/test_activations.py:109](../../tests/activations/test_activations.py#L109) |  |
| `test_A06_sidecar_access_raises_leakage_and_stage_roundtrip` | test | `test_A06_sidecar_access_raises_leakage_and_stage_roundtrip` | [tests/activations/test_activations.py:142](../../tests/activations/test_activations.py#L142) |  |
| `test_A06_static_imports_are_allowed_only` | test | `test_A06_static_imports_are_allowed_only` | [tests/activations/test_activations.py:126](../../tests/activations/test_activations.py#L126) |  |
| `test_a0_equals_max_degree_lazy_walk` | test | `test_a0_equals_max_degree_lazy_walk` | [tests/process/test_conductance.py:124](../../tests/process/test_conductance.py#L124) |  |
| `test_a14_cap_passed_during_successful_solve_is_rejected` | test | `test_a14_cap_passed_during_successful_solve_is_rejected` | [tests/circle_history/test_cochain_lift.py:287](../../tests/circle_history/test_cochain_lift.py#L287) | The B=1 solve succeeds (unique z*), but the clock is past the cap afterwards. |
| `test_a14_cap_reached_during_local_passes` | test | `test_a14_cap_reached_during_local_passes` | [tests/circle_history/test_cochain_lift.py:316](../../tests/circle_history/test_cochain_lift.py#L316) |  |
| `test_a14_highs_options_pinned` | test | `test_a14_highs_options_pinned` | [tests/circle_history/test_cochain_lift.py:326](../../tests/circle_history/test_cochain_lift.py#L326) |  |
| `test_a14_over_cap_before_first_call` | test | `test_a14_over_cap_before_first_call` | [tests/circle_history/test_cochain_lift.py:282](../../tests/circle_history/test_cochain_lift.py#L282) |  |
| `test_a16_closed_branch_below_cap_returns_exact_lift` | test | `test_a16_closed_branch_below_cap_returns_exact_lift` | [tests/circle_history/test_cochain_chart_v24.py:131](../../tests/circle_history/test_cochain_chart_v24.py#L131) |  |
| `test_a16_closed_branch_cap_only_at_final_check` | test | `test_a16_closed_branch_cap_only_at_final_check` | [tests/circle_history/test_cochain_chart_v24.py:140](../../tests/circle_history/test_cochain_chart_v24.py#L140) |  |
| `test_a16_closed_branch_past_cap_at_return_is_unresolved` | test | `test_a16_closed_branch_past_cap_at_return_is_unresolved` | [tests/circle_history/test_cochain_chart_v24.py:124](../../tests/circle_history/test_cochain_chart_v24.py#L124) |  |
| `test_a16_corrected_branch_cap_only_at_final_check` | test | `test_a16_corrected_branch_cap_only_at_final_check` | [tests/circle_history/test_cochain_chart_v24.py:150](../../tests/circle_history/test_cochain_chart_v24.py#L150) |  |
| `test_a16_first_clock_call_precedes_defect` | test | `test_a16_first_clock_call_precedes_defect` | [tests/circle_history/test_cochain_chart_v24.py:168](../../tests/circle_history/test_cochain_chart_v24.py#L168) |  |
| `test_a17_extend_wraps_extension_distance` | test | `test_a17_extend_wraps_extension_distance` | [tests/circle_history/test_cochain_chart_v24.py:236](../../tests/circle_history/test_cochain_chart_v24.py#L236) |  |
| `test_a17_fit_chart_labels_in_order_and_same_chart` | test | `test_a17_fit_chart_labels_in_order_and_same_chart` | [tests/circle_history/test_cochain_chart_v24.py:212](../../tests/circle_history/test_cochain_chart_v24.py#L212) |  |
| `test_a17_timed_exception_propagates_and_stops` | test | `test_a17_timed_exception_propagates_and_stops` | [tests/circle_history/test_cochain_chart_v24.py:227](../../tests/circle_history/test_cochain_chart_v24.py#L227) |  |
| `test_a1_selftest_holds_on_this_platform` | test | `test_a1_selftest_holds_on_this_platform` | [tests/c1prime/test_b_cert_oracle.py:377](../../tests/c1prime/test_b_cert_oracle.py#L377) |  |
| `test_absence_shown_ignores_ineligible_worlds` | test | `test_absence_shown_ignores_ineligible_worlds` | [tests/hws/test_a_outcomes.py:188](../../tests/hws/test_a_outcomes.py#L188) |  |
| `test_absolute_resolution_is_separate_and_strict` | test | `test_absolute_resolution_is_separate_and_strict` | [tests/d2a/test_b_behaviour.py:96](../../tests/d2a/test_b_behaviour.py#L96) |  |
| `test_absolute_resolution_needs_both_members` | test | `test_absolute_resolution_needs_both_members` | [tests/d2a/test_b_behaviour.py:107](../../tests/d2a/test_b_behaviour.py#L107) |  |
| `test_accepted_reference_bounds_the_exact_projector_distance` | test | `test_accepted_reference_bounds_the_exact_projector_distance` | [tests/c2_readout/test_a_gls.py:315](../../tests/c2_readout/test_a_gls.py#L315) |  |
| `test_activation_ids_missing_run_is_empty_not_an_error` | test | `test_activation_ids_missing_run_is_empty_not_an_error` | [tests/experiment/test_runner.py:104](../../tests/experiment/test_runner.py#L104) |  |
| `test_activations3_are_the_three_hooks_at_position_32` | test | `test_activations3_are_the_three_hooks_at_position_32` | [tests/c2_readout/test_b_patch.py:104](../../tests/c2_readout/test_b_patch.py#L104) |  |
| `test_activations_at_site_equal_c1_model_bitwise` | test | `test_activations_at_site_equal_c1_model_bitwise` | [tests/hwsb/test_b_e4path.py:211](../../tests/hwsb/test_b_e4path.py#L211) |  |
| `test_additive_score_iid_toy_equals_full_llr` | test | `test_additive_score_iid_toy_equals_full_llr` | [tests/x2a_stage0/test_x2a_stage0_ph.py:78](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L78) |  |
| `test_additive_score_uses_disjoint_stationary_blocks` | test | `test_additive_score_uses_disjoint_stationary_blocks` | [tests/x2a_stage0/test_x2a_stage0_ph.py:91](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L91) |  |
| `test_admission_lock_before_import_blocks_retrain_and_restoration_rules` | test | `test_admission_lock_before_import_blocks_retrain_and_restoration_rules` | [tests/x6_stage1/test_b_ingest_bundle.py:317](../../tests/x6_stage1/test_b_ingest_bundle.py#L317) |  |
| `test_admit` | test | `test_admit` | [tests/d2a/test_b_resource.py:275](../../tests/d2a/test_b_resource.py#L275) |  |
| `test_aeff_on_known_zero_worlds` | test | `test_aeff_on_known_zero_worlds` | [tests/hws/test_b_exact.py:140](../../tests/hws/test_b_exact.py#L140) |  |
| `test_agreement_failures_flag_precision_and_permutation` | test | `test_agreement_failures_flag_precision_and_permutation` | [tests/experiment/test_x4b.py:76](../../tests/experiment/test_x4b.py#L76) |  |
| `test_agreement_known_answers` | test | `test_agreement_known_answers` | [tests/circle_history/test_chart_extension.py:270](../../tests/circle_history/test_chart_extension.py#L270) |  |
| `test_alignment_errors` | test | `test_alignment_errors` | [tests/oracle/test_oracle.py:250](../../tests/oracle/test_oracle.py#L250) |  |
| `test_all_pass_feasible` | test | `test_all_pass_feasible` | [tests/analysis/test_x5_context.py:93](../../tests/analysis/test_x5_context.py#L93) |  |
| `test_all_pass_is_hwsb_pass` | test | `test_all_pass_is_hwsb_pass` | [tests/hwsb/test_a_outcomes.py:101](../../tests/hwsb/test_a_outcomes.py#L101) |  |
| `test_all_qualifiers_together` | test | `test_all_qualifiers_together` | [tests/d2a/test_b_rules_qualifiers.py:208](../../tests/d2a/test_b_rules_qualifiers.py#L208) |  |
| `test_allowed_class` | test | `test_allowed_class` | [tests/x6_stage1/test_b_chain_ops.py:348](../../tests/x6_stage1/test_b_chain_ops.py#L348) |  |
| `test_allowlist` | test | `test_allowlist` | [tests/x6_stage1/test_b_nb_s0_ops.py:209](../../tests/x6_stage1/test_b_nb_s0_ops.py#L209) |  |
| `test_alpha_derivations` | test | `test_alpha_derivations` | [tests/hws/test_a_stats.py:57](../../tests/hws/test_a_stats.py#L57) |  |
| `test_ambient_match_requires_identical_result` | test | `test_ambient_match_requires_identical_result` | [tests/experiment/test_x4b2.py:87](../../tests/experiment/test_x4b2.py#L87) |  |
| `test_an_involutive_permutation_hides_the_direction_error` | test | `test_an_involutive_permutation_hides_the_direction_error` | [tests/c2_readout/test_a_readout.py:208](../../tests/c2_readout/test_a_readout.py#L208) |  |
| `test_anchored_labels_match_contract_and_formula` | test | `test_anchored_labels_match_contract_and_formula` | [tests/hws/test_b_worlds.py:219](../../tests/hws/test_b_worlds.py#L219) |  |
| `test_angular_instability_boundaries` | test | `test_angular_instability_boundaries` | [tests/circle_history/test_scores_precision.py:302](../../tests/circle_history/test_scores_precision.py#L302) |  |
| `test_angular_instability_rejects_bad_bound` | test | `test_angular_instability_rejects_bad_bound` | [tests/circle_history/test_scores_precision.py:342](../../tests/circle_history/test_scores_precision.py#L342) |  |
| `test_angular_instability_rejects_nonfinite_input` | test | `test_angular_instability_rejects_nonfinite_input` | [tests/circle_history/test_scores_precision.py:336](../../tests/circle_history/test_scores_precision.py#L336) |  |
| `test_angular_instability_uses_stable_magnitude_for_subnormals` | test | `test_angular_instability_uses_stable_magnitude_for_subnormals` | [tests/circle_history/test_scores_precision.py:328](../../tests/circle_history/test_scores_precision.py#L328) |  |
| `test_annotations_boundaries` | test | `test_annotations_boundaries` | [tests/hws/test_a_classify.py:233](../../tests/hws/test_a_classify.py#L233) |  |
| `test_append_stage_event_line_format` | test | `test_append_stage_event_line_format` | [tests/hws/test_b_records.py:85](../../tests/hws/test_b_records.py#L85) |  |
| `test_apply_gauge_known_values` | test | `test_apply_gauge_known_values` | [tests/circle_history/test_chart.py:314](../../tests/circle_history/test_chart.py#L314) |  |
| `test_apply_gauge_never_returns_two_pi` | test | `test_apply_gauge_never_returns_two_pi` | [tests/circle_history/test_builder_v25.py:237](../../tests/circle_history/test_builder_v25.py#L237) |  |
| `test_apply_map_batch_convention_non_symmetric` | test | `test_apply_map_batch_convention_non_symmetric` | [tests/analysis/test_x4f_erasure.py:125](../../tests/analysis/test_x4f_erasure.py#L125) |  |
| `test_apply_usage_blocking_writes_latch_and_reads_utf8_sig` | test | `test_apply_usage_blocking_writes_latch_and_reads_utf8_sig` | [tests/experiment/test_x5g1t_usage_files.py:97](../../tests/experiment/test_x5g1t_usage_files.py#L97) |  |
| `test_apply_usage_clears_and_archives` | test | `test_apply_usage_clears_and_archives` | [tests/experiment/test_x5g1t_usage_files.py:112](../../tests/experiment/test_x5g1t_usage_files.py#L112) |  |
| `test_apply_usage_existing_malformed_latch_file_raises` | test | `test_apply_usage_existing_malformed_latch_file_raises` | [tests/experiment/test_x5g1t_usage_files.py:131](../../tests/experiment/test_x5g1t_usage_files.py#L131) |  |
| `test_apply_usage_existing_malformed_usage_file_raises` | test | `test_apply_usage_existing_malformed_usage_file_raises` | [tests/experiment/test_x5g1t_usage_files.py:124](../../tests/experiment/test_x5g1t_usage_files.py#L124) |  |
| `test_apply_usage_hold_persists_without_usage_file` | test | `test_apply_usage_hold_persists_without_usage_file` | [tests/experiment/test_x5g1t_usage_files.py:106](../../tests/experiment/test_x5g1t_usage_files.py#L106) |  |
| `test_apply_usage_missing_files_no_hold` | test | `test_apply_usage_missing_files_no_hold` | [tests/experiment/test_x5g1t_usage_files.py:91](../../tests/experiment/test_x5g1t_usage_files.py#L91) |  |
| `test_archive_attempt_moves_files_with_sha256sums` | test | `test_archive_attempt_moves_files_with_sha256sums` | [tests/k4b/test_b_rerun.py:73](../../tests/k4b/test_b_rerun.py#L73) |  |
| `test_archive_partial_moves_only_unlisted_files` | test | `test_archive_partial_moves_only_unlisted_files` | [tests/hws/test_b_records.py:161](../../tests/hws/test_b_records.py#L161) |  |
| `test_archive_stale_marker` | test | `test_archive_stale_marker` | [tests/circle_history/test_builder_v24_runtime.py:98](../../tests/circle_history/test_builder_v24_runtime.py#L98) |  |
| `test_archived_suffixes_are_kept` | test | `test_archived_suffixes_are_kept` | [tests/k4b/test_b_rerun.py:96](../../tests/k4b/test_b_rerun.py#L96) |  |
| `test_arm_common_additive_perturbation_cancels_exactly` | test | `test_arm_common_additive_perturbation_cancels_exactly` | [tests/c1prime/test_b_identities.py:115](../../tests/c1prime/test_b_identities.py#L115) |  |
| `test_arm_op_failed_gives_failed` | test | `test_arm_op_failed_gives_failed` | [tests/analysis/test_x5_context.py:106](../../tests/analysis/test_x5_context.py#L106) |  |
| `test_arm_value_exhaustive` | test | `test_arm_value_exhaustive` | [tests/d2a/test_b_rules_flags.py:117](../../tests/d2a/test_b_rules_flags.py#L117) |  |
| `test_arm_value_named_cases` | test | `test_arm_value_named_cases` | [tests/d2a/test_b_rules_flags.py:131](../../tests/d2a/test_b_rules_flags.py#L131) |  |
| `test_arms_share_step0_weights_and_seeds_but_not_ids` | test | `test_arms_share_step0_weights_and_seeds_but_not_ids` | [tests/experiment/test_x5g1t_training.py:229](../../tests/experiment/test_x5g1t_training.py#L229) |  |
| `test_assert_can_start` | test | `test_assert_can_start` | [tests/experiment/test_x5g1t_runtime_boundary.py:101](../../tests/experiment/test_x5g1t_runtime_boundary.py#L101) |  |
| `test_asymmetric_cells` | test | `test_asymmetric_cells` | [tests/hws/test_b_worlds.py:326](../../tests/hws/test_b_worlds.py#L326) |  |
| `test_audit_mode` | test | `test_audit_mode` | [tests/oracle_profile/test_builder_controls.py:134](../../tests/oracle_profile/test_builder_controls.py#L134) |  |
| `test_audit_record_is_audit_only` | test | `test_audit_record_is_audit_only` | [tests/experiment/test_x5g1t_runtime.py:308](../../tests/experiment/test_x5g1t_runtime.py#L308) |  |
| `test_auth_ok` | test | `test_auth_ok` | [tests/c2_readout/test_b_lineage.py:227](../../tests/c2_readout/test_b_lineage.py#L227) |  |
| `test_auth_ok` | test | `test_auth_ok` | [tests/x6_stage1/test_b_ingest_bundle.py:393](../../tests/x6_stage1/test_b_ingest_bundle.py#L393) |  |
| `test_auth_ok_for_every_stage` | test | `test_auth_ok_for_every_stage` | [tests/hwsb/test_b_records.py:112](../../tests/hwsb/test_b_records.py#L112) |  |
| `test_auth_ok_missing_or_unparsable_never_raises` | test | `test_auth_ok_missing_or_unparsable_never_raises` | [tests/c2_readout/test_b_lineage.py:239](../../tests/c2_readout/test_b_lineage.py#L239) |  |
| `test_auth_ok_refuses_while_the_v2_auth_is_pending` | test | `test_auth_ok_refuses_while_the_v2_auth_is_pending` | [tests/c2_readout/test_b_lineage.py:232](../../tests/c2_readout/test_b_lineage.py#L232) |  |
| `test_authorized_worker` | test | `test_authorized_worker` | [tests/k4b/test_b_flow.py:228](../../tests/k4b/test_b_flow.py#L228) |  |
| `test_axis_state_perm_n3_hand_example` | test | `test_axis_state_perm_n3_hand_example` | [tests/process/test_controls.py:74](../../tests/process/test_controls.py#L74) |  |
| `test_b1_equality_at_point_eight_passes_and_just_below_fails` | test | `test_b1_equality_at_point_eight_passes_and_just_below_fails` | [tests/hwsb/test_a_learning.py:264](../../tests/hwsb/test_a_learning.py#L264) |  |
| `test_b1_inconclusive_is_numerical_failure` | test | `test_b1_inconclusive_is_numerical_failure` | [tests/hwsb/test_a_outcomes.py:123](../../tests/hwsb/test_a_outcomes.py#L123) |  |
| `test_b1_inconclusive_when_gc_at_floor` | test | `test_b1_inconclusive_when_gc_at_floor` | [tests/hwsb/test_a_learning.py:281](../../tests/hwsb/test_a_learning.py#L281) |  |
| `test_b1_last_symbol_model_captures_nothing` | test | `test_b1_last_symbol_model_captures_nothing` | [tests/hwsb/test_a_learning.py:237](../../tests/hwsb/test_a_learning.py#L237) |  |
| `test_b1_oracle_model_captures_all` | test | `test_b1_oracle_model_captures_all` | [tests/hwsb/test_a_learning.py:228](../../tests/hwsb/test_a_learning.py#L228) |  |
| `test_b1_regret_and_gc_match_reference` | test | `test_b1_regret_and_gc_match_reference` | [tests/hwsb/test_a_learning.py:245](../../tests/hwsb/test_a_learning.py#L245) |  |
| `test_b3_is_forcing_on_circular_marginals` | test | `test_b3_is_forcing_on_circular_marginals` | [tests/hwsb/test_a_learning.py:340](../../tests/hwsb/test_a_learning.py#L340) |  |
| `test_b3_suffix_model_zero_and_oracle_positive` | test | `test_b3_suffix_model_zero_and_oracle_positive` | [tests/hwsb/test_a_learning.py:356](../../tests/hwsb/test_a_learning.py#L356) |  |
| `test_b4_guard_headroom` | test | `test_b4_guard_headroom` | [tests/k4b/test_a_width_b4.py:165](../../tests/k4b/test_a_width_b4.py#L165) |  |
| `test_b4_guard_matches_reused_kernels` | test | `test_b4_guard_matches_reused_kernels` | [tests/k4b/test_a_width_b4.py:180](../../tests/k4b/test_a_width_b4.py#L180) |  |
| `test_b4_guard_numerical_band` | test | `test_b4_guard_numerical_band` | [tests/k4b/test_a_width_b4.py:171](../../tests/k4b/test_a_width_b4.py#L171) |  |
| `test_b4_guard_pass` | test | `test_b4_guard_pass` | [tests/k4b/test_a_width_b4.py:154](../../tests/k4b/test_a_width_b4.py#L154) |  |
| `test_b4_lower_equal_to_delta_is_not_pass` | test | `test_b4_lower_equal_to_delta_is_not_pass` | [tests/circle_history/test_scores_precision_gates.py:244](../../tests/circle_history/test_scores_precision_gates.py#L244) |  |
| `test_b4_lower_just_above_delta_passes` | test | `test_b4_lower_just_above_delta_passes` | [tests/circle_history/test_scores_precision_gates.py:257](../../tests/circle_history/test_scores_precision_gates.py#L257) |  |
| `test_b4_status_both_pass` | test | `test_b4_status_both_pass` | [tests/hwsb/test_a_endpoints.py:212](../../tests/hwsb/test_a_endpoints.py#L212) |  |
| `test_b4_status_cal_failure_is_c0_cal` | test | `test_b4_status_cal_failure_is_c0_cal` | [tests/hwsb/test_a_endpoints.py:221](../../tests/hwsb/test_a_endpoints.py#L221) |  |
| `test_b4_status_first_failing_model_in_master_order` | test | `test_b4_status_first_failing_model_in_master_order` | [tests/hwsb/test_a_endpoints.py:231](../../tests/hwsb/test_a_endpoints.py#L231) |  |
| `test_b4_status_no_chart_counts_against_c0_val` | test | `test_b4_status_no_chart_counts_against_c0_val` | [tests/hwsb/test_a_endpoints.py:240](../../tests/hwsb/test_a_endpoints.py#L240) |  |
| `test_b4_status_technical_status_reported` | test | `test_b4_status_technical_status_reported` | [tests/hwsb/test_a_endpoints.py:247](../../tests/hwsb/test_a_endpoints.py#L247) |  |
| `test_b4_summary_fail_closed` | test | `test_b4_summary_fail_closed` | [tests/circle_history/test_scores_precision_gates.py:284](../../tests/circle_history/test_scores_precision_gates.py#L284) |  |
| `test_b5_both_pass_status` | test | `test_b5_both_pass_status` | [tests/hwsb/test_a_capture.py:226](../../tests/hwsb/test_a_capture.py#L226) |  |
| `test_b5_default_seed_is_620214` | test | `test_b5_default_seed_is_620214` | [tests/hwsb/test_a_capture.py:197](../../tests/hwsb/test_a_capture.py#L197) |  |
| `test_b5_fallback_n_enters_c_min` | test | `test_b5_fallback_n_enters_c_min` | [tests/hwsb/test_a_capture.py:277](../../tests/hwsb/test_a_capture.py#L277) |  |
| `test_b5_matches_reference` | test | `test_b5_matches_reference` | [tests/hwsb/test_a_capture.py:190](../../tests/hwsb/test_a_capture.py#L190) |  |
| `test_b5_n_on_real_ladder_output` | test | `test_b5_n_on_real_ladder_output` | [tests/hwsb/test_a_ladder.py:289](../../tests/hwsb/test_a_ladder.py#L289) |  |
| `test_b5_n_returns_ladder_n_or_fallback` | test | `test_b5_n_returns_ladder_n_or_fallback` | [tests/hwsb/test_a_ladder.py:281](../../tests/hwsb/test_a_ladder.py#L281) |  |
| `test_b5_nonfinite_d4hat_is_numerical_failure` | test | `test_b5_nonfinite_d4hat_is_numerical_failure` | [tests/hwsb/test_a_capture.py:267](../../tests/hwsb/test_a_capture.py#L267) |  |
| `test_b5_nonpositive_d4hat_is_numerical_failure` | test | `test_b5_nonpositive_d4hat_is_numerical_failure` | [tests/hwsb/test_a_capture.py:258](../../tests/hwsb/test_a_capture.py#L258) |  |
| `test_b5_positive_below_planning_needs_every_model` | test | `test_b5_positive_below_planning_needs_every_model` | [tests/hwsb/test_a_capture.py:239](../../tests/hwsb/test_a_capture.py#L239) |  |
| `test_b5_ulp_boundary_drb10` | test | `test_b5_ulp_boundary_drb10` | [tests/hwsb/test_a_capture.py:207](../../tests/hwsb/test_a_capture.py#L207) |  |
| `test_b7_forecasts` | test | `test_b7_forecasts` | [tests/hwsb/test_a_outcomes.py:342](../../tests/hwsb/test_a_outcomes.py#L342) |  |
| `test_b7_without_measurements_is_unavailable` | test | `test_b7_without_measurements_is_unavailable` | [tests/hwsb/test_a_outcomes.py:355](../../tests/hwsb/test_a_outcomes.py#L355) |  |
| `test_b8a_and_b9a_failures_even_when_b1_fails` | test | `test_b8a_and_b9a_failures_even_when_b1_fails` | [tests/hwsb/test_a_outcomes.py:130](../../tests/hwsb/test_a_outcomes.py#L130) |  |
| `test_b9a_registry_cap_boundary_is_exact` | test | `test_b9a_registry_cap_boundary_is_exact` | [tests/hwsb/test_b_registry.py:201](../../tests/hwsb/test_b_registry.py#L201) |  |
| `test_b9a_registry_failure_gives_registry_status` | test | `test_b9a_registry_failure_gives_registry_status` | [tests/hwsb/test_b_registry.py:224](../../tests/hwsb/test_b_registry.py#L224) |  |
| `test_b9a_uses_12288_style_row_count_and_reference_tolerance` | test | `test_b9a_uses_12288_style_row_count_and_reference_tolerance` | [tests/hwsb/test_b_registry.py:214](../../tests/hwsb/test_b_registry.py#L214) |  |
| `test_B_constant_uses_tree_depth_plus_one` | test | `test_B_constant_uses_tree_depth_plus_one` | [tests/c1prime/test_b_cert_guards.py:109](../../tests/c1prime/test_b_cert_guards.py#L109) |  |
| `test_b_in_the_nuisance_span_is_degenerate` | test | `test_b_in_the_nuisance_span_is_degenerate` | [tests/c2_readout/test_a_readout.py:370](../../tests/c2_readout/test_a_readout.py#L370) |  |
| `test_b_num_is_monotone` | test | `test_b_num_is_monotone` | [tests/k4b/test_a_decision.py:97](../../tests/k4b/test_a_decision.py#L97) |  |
| `test_b_num_matches_B_constant_and_closed_form` | test | `test_b_num_matches_B_constant_and_closed_form` | [tests/k4b/test_a_decision.py:88](../../tests/k4b/test_a_decision.py#L88) |  |
| `test_bad_inputs_alignment_error` | test | `test_bad_inputs_alignment_error` | [tests/learner/test_patch.py:276](../../tests/learner/test_patch.py#L276) |  |
| `test_bad_source_never_clears` | test | `test_bad_source_never_clears` | [tests/experiment/test_x5g1t_usage.py:228](../../tests/experiment/test_x5g1t_usage.py#L228) |  |
| `test_band_edge_and_h_max_probe` | test | `test_band_edge_and_h_max_probe` | [tests/d1_seam/test_d1_seam.py:282](../../tests/d1_seam/test_d1_seam.py#L282) |  |
| `test_band_edge_d_equals_oracle_contrast` | test | `test_band_edge_d_equals_oracle_contrast` | [tests/d2a/test_b_targets.py:154](../../tests/d2a/test_b_targets.py#L154) |  |
| `test_band_edge_oracle_model_gives_rm_equal_d_and_beta_one` | test | `test_band_edge_oracle_model_gives_rm_equal_d_and_beta_one` | [tests/d2a/test_b_targets.py:167](../../tests/d2a/test_b_targets.py#L167) |  |
| `test_band_edge_pi_blind_model_gives_beta_zero` | test | `test_band_edge_pi_blind_model_gives_beta_zero` | [tests/d2a/test_b_targets.py:174](../../tests/d2a/test_b_targets.py#L174) |  |
| `test_band_edge_r8_uses_the_exact_window8_law` | test | `test_band_edge_r8_uses_the_exact_window8_law` | [tests/d2a/test_b_targets.py:159](../../tests/d2a/test_b_targets.py#L159) |  |
| `test_band_edge_rm_reads_model_index_p` | test | `test_band_edge_rm_reads_model_index_p` | [tests/d2a/test_b_targets.py:181](../../tests/d2a/test_b_targets.py#L181) | rm uses q_model[row, p] (index p sees w_1..w_p and predicts w_{p+1}); a model whose law |
| `test_band_edge_table_selects_exactly_sigma0_sigma2_rows` | test | `test_band_edge_table_selects_exactly_sigma0_sigma2_rows` | [tests/d2a/test_b_targets.py:143](../../tests/d2a/test_b_targets.py#L143) |  |
| `test_band_select_longest_tie_width_and_beta0` | test | `test_band_select_longest_tie_width_and_beta0` | [tests/x2a_stage0/test_x2a_stage0_ph.py:207](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L207) |  |
| `test_band_select_plateau_intersection` | test | `test_band_select_plateau_intersection` | [tests/x2a_stage0/test_x2a_stage0_ph.py:198](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L198) |  |
| `test_batched_scoring_equals_single_pass` | test | `test_batched_scoring_equals_single_pass` | [tests/experiment/test_x5g1_scorebench_smoke.py:34](../../tests/experiment/test_x5g1_scorebench_smoke.py#L34) |  |
| `test_bayes_cross_check_passes_and_detects_a_perturbed_e` | test | `test_bayes_cross_check_passes_and_detects_a_perturbed_e` | [tests/hws/test_b_exact.py:187](../../tests/hws/test_b_exact.py#L187) |  |
| `test_begin_and_complete_stage_records` | test | `test_begin_and_complete_stage_records` | [tests/k4b/test_b_rerun.py:142](../../tests/k4b/test_b_rerun.py#L142) |  |
| `test_begin_stage_accepts_a_complete_prerequisite` | test | `test_begin_stage_accepts_a_complete_prerequisite` | [tests/c1prime/test_a_gates.py:161](../../tests/c1prime/test_a_gates.py#L161) |  |
| `test_begin_stage_refuses_a_missing_pass` | test | `test_begin_stage_refuses_a_missing_pass` | [tests/c1prime/test_a_gates.py:170](../../tests/c1prime/test_a_gates.py#L170) |  |
| `test_begin_stage_refuses_a_retry` | test | `test_begin_stage_refuses_a_retry` | [tests/c1prime/test_a_gates.py:192](../../tests/c1prime/test_a_gates.py#L192) |  |
| `test_begin_stage_refuses_after_a_recorded_non_pass` | test | `test_begin_stage_refuses_after_a_recorded_non_pass` | [tests/c1prime/test_a_gates.py:185](../../tests/c1prime/test_a_gates.py#L185) |  |
| `test_begin_stage_refuses_an_uncompleted_prerequisite` | test | `test_begin_stage_refuses_an_uncompleted_prerequisite` | [tests/c1prime/test_a_gates.py:209](../../tests/c1prime/test_a_gates.py#L209) |  |
| `test_begin_stage_refuses_changed_evidence` | test | `test_begin_stage_refuses_changed_evidence` | [tests/c1prime/test_a_gates.py:201](../../tests/c1prime/test_a_gates.py#L201) |  |
| `test_behaviour_cells_exactly_the_true_ones` | test | `test_behaviour_cells_exactly_the_true_ones` | [tests/d2a/test_b_rules_qualifiers.py:198](../../tests/d2a/test_b_rules_qualifiers.py#L198) |  |
| `test_beliefs_chunked_equal_unchunked` | test | `test_beliefs_chunked_equal_unchunked` | [tests/experiment/test_x4b2.py:61](../../tests/experiment/test_x4b2.py#L61) |  |
| `test_below_3x_absence_not_shown` | test | `test_below_3x_absence_not_shown` | [tests/hws/test_a_outcomes.py:178](../../tests/hws/test_a_outcomes.py#L178) |  |
| `test_below_3x_absence_shown` | test | `test_below_3x_absence_shown` | [tests/hws/test_a_outcomes.py:168](../../tests/hws/test_a_outcomes.py#L168) |  |
| `test_beta2_oracle_and_pi_blind_on_decision_contrasts` | test | `test_beta2_oracle_and_pi_blind_on_decision_contrasts` | [tests/d2a/test_b_targets.py:192](../../tests/d2a/test_b_targets.py#L192) |  |
| `test_beta2_pass` | test | `test_beta2_pass` | [tests/d2a/test_b_rules_flags.py:164](../../tests/d2a/test_b_rules_flags.py#L164) |  |
| `test_beta_fsum_and_exact_agree_t7` | test | `test_beta_fsum_and_exact_agree_t7` | [tests/x6_stage1/test_a_pairs.py:303](../../tests/x6_stage1/test_a_pairs.py#L303) |  |
| `test_beta_is_slope_through_origin_on_hand_example` | test | `test_beta_is_slope_through_origin_on_hand_example` | [tests/d2a/test_b_targets.py:44](../../tests/d2a/test_b_targets.py#L44) |  |
| `test_beta_oracle_is_one_and_pi_blind_is_zero` | test | `test_beta_oracle_is_one_and_pi_blind_is_zero` | [tests/d2a/test_b_targets.py:36](../../tests/d2a/test_b_targets.py#L36) |  |
| `test_beta_pools_two_dimensional_contrasts` | test | `test_beta_pools_two_dimensional_contrasts` | [tests/d2a/test_b_targets.py:54](../../tests/d2a/test_b_targets.py#L54) |  |
| `test_beta_scale_and_sign` | test | `test_beta_scale_and_sign` | [tests/d2a/test_b_targets.py:62](../../tests/d2a/test_b_targets.py#L62) |  |
| `test_beta_tiny_positive_denominator_is_defined` | test | `test_beta_tiny_positive_denominator_is_defined` | [tests/d2a/test_b_targets.py:79](../../tests/d2a/test_b_targets.py#L79) |  |
| `test_beta_undefined_denominator` | test | `test_beta_undefined_denominator` | [tests/d2a/test_b_targets.py:75](../../tests/d2a/test_b_targets.py#L75) |  |
| `test_betti_at_beta1_band_and_k2` | test | `test_betti_at_beta1_band_and_k2` | [tests/x2a_stage0/test_x2a_stage0_ph.py:232](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L232) |  |
| `test_bigram_contexts_do_not_cross_sequences` | test | `test_bigram_contexts_do_not_cross_sequences` | [tests/prediction/test_ngram.py:47](../../tests/prediction/test_ngram.py#L47) |  |
| `test_bigram_unseen_context_alpha_zero_backs_off_to_unigram` | test | `test_bigram_unseen_context_alpha_zero_backs_off_to_unigram` | [tests/prediction/test_ngram.py:53](../../tests/prediction/test_ngram.py#L53) |  |
| `test_bin_positions_are_deterministic` | test | `test_bin_positions_are_deterministic` | [tests/d2a/test_a_world.py:201](../../tests/d2a/test_a_world.py#L201) |  |
| `test_bin_positions_follow_api_rule` | test | `test_bin_positions_follow_api_rule` | [tests/d2a/test_a_world.py:183](../../tests/d2a/test_a_world.py#L183) |  |
| `test_bind_defaults_temp_root_to_out` | test | `test_bind_defaults_temp_root_to_out` | [tests/hwsb/test_b_meter_law.py:86](../../tests/hwsb/test_b_meter_law.py#L86) |  |
| `test_bind_meter_sets_exactly_the_section_11_3_names` | test | `test_bind_meter_sets_exactly_the_section_11_3_names` | [tests/d2a/test_b_resource.py:148](../../tests/d2a/test_b_resource.py#L148) |  |
| `test_bind_rebinds_every_module_level_name` | test | `test_bind_rebinds_every_module_level_name` | [tests/c1prime/test_a_release_meter.py:193](../../tests/c1prime/test_a_release_meter.py#L193) |  |
| `test_bind_sets_every_registered_value` | test | `test_bind_sets_every_registered_value` | [tests/k4b/test_b_meter.py:53](../../tests/k4b/test_b_meter.py#L53) |  |
| `test_bind_sets_memory_cap_temp_root_and_meter_paths` | test | `test_bind_sets_memory_cap_temp_root_and_meter_paths` | [tests/hwsb/test_b_meter_law.py:69](../../tests/hwsb/test_b_meter_law.py#L69) |  |
| `test_bind_sets_the_hws_values` | test | `test_bind_sets_the_hws_values` | [tests/hws/test_b_records.py:284](../../tests/hws/test_b_records.py#L284) |  |
| `test_bind_to_the_dry_store_puts_child_temp_on_x` | test | `test_bind_to_the_dry_store_puts_child_temp_on_x` | [tests/hws/test_b_records.py:304](../../tests/hws/test_b_records.py#L304) |  |
| `test_binding_points_unchanged_modules_at_this_job` | test | `test_binding_points_unchanged_modules_at_this_job` | [tests/circle_history/test_builder_runtime.py:54](../../tests/circle_history/test_builder_runtime.py#L54) |  |
| `test_bins_and_resultant_use_all_512_queries_including_unsupported` | test | `test_bins_and_resultant_use_all_512_queries_including_unsupported` | [tests/c1prime/test_a_chart_val.py:134](../../tests/c1prime/test_a_chart_val.py#L134) | Bins and resultant count every production-extension query, supported or not. |
| `test_bins_fail_while_resultant_passes` | test | `test_bins_fail_while_resultant_passes` | [tests/c1prime/test_a_chart_val.py:149](../../tests/c1prime/test_a_chart_val.py#L149) |  |
| `test_bitwise_reading_is_gate_pass` | test | `test_bitwise_reading_is_gate_pass` | [tests/hwsb/test_r_0170_kb2_status.py:48](../../tests/hwsb/test_r_0170_kb2_status.py#L48) |  |
| `test_block_content_invariant_to_k` | test | `test_block_content_invariant_to_k` | [tests/k4b/test_b_data.py:146](../../tests/k4b/test_b_data.py#L146) |  |
| `test_block_round_trip_and_exclusive_create` | test | `test_block_round_trip_and_exclusive_create` | [tests/hwsb/test_b_streams.py:294](../../tests/hwsb/test_b_streams.py#L294) |  |
| `test_blocking_limits_malformed` | test | `test_blocking_limits_malformed` | [tests/experiment/test_x5g1t_usage.py:176](../../tests/experiment/test_x5g1t_usage.py#L176) |  |
| `test_blocking_usage_holds_despite_worker_continue` | test | `test_blocking_usage_holds_despite_worker_continue` | [tests/experiment/test_x5g1t_usage_files.py:220](../../tests/experiment/test_x5g1t_usage_files.py#L220) |  |
| `test_bom_json_contributes_through_source_c_like_the_reused_reader` | test | `test_bom_json_contributes_through_source_c_like_the_reused_reader` | [tests/k4b/test_b_registry_fixes.py:73](../../tests/k4b/test_b_registry_fixes.py#L73) |  |
| `test_boot_means_beta_and_stream` | test | `test_boot_means_beta_and_stream` | [tests/x6_stage1/test_a_numerics.py:303](../../tests/x6_stage1/test_a_numerics.py#L303) |  |
| `test_bootstrap_consumes_exactly_one_integers_call_per_draw` | test | `test_bootstrap_consumes_exactly_one_integers_call_per_draw` | [tests/analysis/test_x5_endpoint_bootstrap.py:116](../../tests/analysis/test_x5_endpoint_bootstrap.py#L116) |  |
| `test_bootstrap_default_grid_27_points` | test | `test_bootstrap_default_grid_27_points` | [tests/analysis/test_x5_endpoint_bootstrap.py:157](../../tests/analysis/test_x5_endpoint_bootstrap.py#L157) |  |
| `test_bootstrap_error_paths` | test | `test_bootstrap_error_paths` | [tests/oracle_profile/test_oracle_profile_kernels.py:230](../../tests/oracle_profile/test_oracle_profile_kernels.py#L230) |  |
| `test_bootstrap_guard_before_and_after_each_batch` | test | `test_bootstrap_guard_before_and_after_each_batch` | [tests/experiment/test_x5g1_lineage.py:249](../../tests/experiment/test_x5g1_lineage.py#L249) |  |
| `test_bootstrap_guard_brackets_the_draws` | test | `test_bootstrap_guard_brackets_the_draws` | [tests/analysis/test_x5_endpoint_bootstrap.py:132](../../tests/analysis/test_x5_endpoint_bootstrap.py#L132) |  |
| `test_bootstrap_guard_exception_propagates` | test | `test_bootstrap_guard_exception_propagates` | [tests/experiment/test_x5g1_lineage.py:270](../../tests/experiment/test_x5g1_lineage.py#L270) |  |
| `test_bootstrap_guard_strings_per_batch` | test | `test_bootstrap_guard_strings_per_batch` | [tests/analysis/test_x5_endpoint_bootstrap.py:125](../../tests/analysis/test_x5_endpoint_bootstrap.py#L125) |  |
| `test_bootstrap_inputs_fixed_order_one_dict` | test | `test_bootstrap_inputs_fixed_order_one_dict` | [tests/k4b/test_b_endpoint.py:219](../../tests/k4b/test_b_endpoint.py#L219) |  |
| `test_bootstrap_keeps_censored_draws_and_fractions` | test | `test_bootstrap_keeps_censored_draws_and_fractions` | [tests/analysis/test_x5_endpoint_bootstrap.py:96](../../tests/analysis/test_x5_endpoint_bootstrap.py#L96) |  |
| `test_bootstrap_matches_definition_and_is_deterministic` | test | `test_bootstrap_matches_definition_and_is_deterministic` | [tests/experiment/test_x5g1_lineage.py:238](../../tests/experiment/test_x5g1_lineage.py#L238) |  |
| `test_bootstrap_means_share_one_integers_call_per_draw` | test | `test_bootstrap_means_share_one_integers_call_per_draw` | [tests/c1prime/test_b_inference.py:150](../../tests/c1prime/test_b_inference.py#L150) |  |
| `test_bootstrap_quantiles_are_inverted_cdf_order_statistics` | test | `test_bootstrap_quantiles_are_inverted_cdf_order_statistics` | [tests/analysis/test_x5_endpoint_bootstrap.py:107](../../tests/analysis/test_x5_endpoint_bootstrap.py#L107) |  |
| `test_bootstrap_reproduces_documented_sampling_order` | test | `test_bootstrap_reproduces_documented_sampling_order` | [tests/oracle_profile/test_oracle_profile_kernels.py:208](../../tests/oracle_profile/test_oracle_profile_kernels.py#L208) |  |
| `test_bootstrap_reproduces_shared_whole_row_draws` | test | `test_bootstrap_reproduces_shared_whole_row_draws` | [tests/analysis/test_x5_endpoint_bootstrap.py:81](../../tests/analysis/test_x5_endpoint_bootstrap.py#L81) |  |
| `test_bootstrap_shape_errors` | test | `test_bootstrap_shape_errors` | [tests/analysis/test_x5_endpoint_bootstrap.py:168](../../tests/analysis/test_x5_endpoint_bootstrap.py#L168) |  |
| `test_bootstrap_threshold_passthrough` | test | `test_bootstrap_threshold_passthrough` | [tests/analysis/test_x5_endpoint_bootstrap.py:150](../../tests/analysis/test_x5_endpoint_bootstrap.py#L150) |  |
| `test_both_holds_give_hold_with_reasons` | test | `test_both_holds_give_hold_with_reasons` | [tests/experiment/test_x5g1t_runtime.py:168](../../tests/experiment/test_x5g1t_runtime.py#L168) |  |
| `test_both_trigger` | test | `test_both_trigger` | [tests/hwsb/test_b_hold.py:60](../../tests/hwsb/test_b_hold.py#L60) |  |
| `test_bound_dominates_every_symbol_function_and_is_attained` | test | `test_bound_dominates_every_symbol_function_and_is_attained` | [tests/analysis/test_circular_bound.py:23](../../tests/analysis/test_circular_bound.py#L23) |  |
| `test_bound_error_paths` | test | `test_bound_error_paths` | [tests/analysis/test_circular_bound.py:44](../../tests/analysis/test_circular_bound.py#L44) |  |
| `test_bound_hand_value_and_opposite_angles` | test | `test_bound_hand_value_and_opposite_angles` | [tests/analysis/test_circular_bound.py:17](../../tests/analysis/test_circular_bound.py#L17) |  |
| `test_bound_invariant_to_rotation_and_relabelling` | test | `test_bound_invariant_to_rotation_and_relabelling` | [tests/analysis/test_circular_bound.py:36](../../tests/analysis/test_circular_bound.py#L36) |  |
| `test_bound_is_one_when_symbol_determines_angle` | test | `test_bound_is_one_when_symbol_determines_angle` | [tests/analysis/test_circular_bound.py:11](../../tests/analysis/test_circular_bound.py#L11) |  |
| `test_bound_law_restores_after_an_exception` | test | `test_bound_law_restores_after_an_exception` | [tests/hwsb/test_b_meter_law.py:323](../../tests/hwsb/test_b_meter_law.py#L323) |  |
| `test_bound_law_restores_process_law_state` | test | `test_bound_law_restores_process_law_state` | [tests/hwsb/test_a_enclosure_proof.py:317](../../tests/hwsb/test_a_enclosure_proof.py#L317) |  |
| `test_bound_law_sets_and_restores_after_normal_exit` | test | `test_bound_law_sets_and_restores_after_normal_exit` | [tests/hwsb/test_b_meter_law.py:312](../../tests/hwsb/test_b_meter_law.py#L312) |  |
| `test_bound_values_follow_the_displayed_shapes_and_include_zeta` | test | `test_bound_values_follow_the_displayed_shapes_and_include_zeta` | [tests/c1prime/test_b_cert_bounds.py:231](../../tests/c1prime/test_b_cert_bounds.py#L231) |  |
| `test_boundaries_pass_exactly` | test | `test_boundaries_pass_exactly` | [tests/analysis/test_sigma_calibrator.py:57](../../tests/analysis/test_sigma_calibrator.py#L57) |  |
| `test_boundary_budget_exceeded` | test | `test_boundary_budget_exceeded` | [tests/experiment/test_x5g1t_runtime_boundary.py:344](../../tests/experiment/test_x5g1t_runtime_boundary.py#L344) |  |
| `test_boundary_budget_includes_prior` | test | `test_boundary_budget_includes_prior` | [tests/experiment/test_x5g1t_runtime_boundary.py:352](../../tests/experiment/test_x5g1t_runtime_boundary.py#L352) |  |
| `test_boundary_continue_records_guard_step` | test | `test_boundary_continue_records_guard_step` | [tests/experiment/test_x5g1t_runtime_boundary.py:253](../../tests/experiment/test_x5g1t_runtime_boundary.py#L253) |  |
| `test_boundary_continue_returns_at_once` | test | `test_boundary_continue_returns_at_once` | [tests/d2a/test_b_resource.py:343](../../tests/d2a/test_b_resource.py#L343) |  |
| `test_boundary_hold_then_release_proceeds` | test | `test_boundary_hold_then_release_proceeds` | [tests/experiment/test_x5g1t_runtime_boundary.py:317](../../tests/experiment/test_x5g1t_runtime_boundary.py#L317) |  |
| `test_boundary_hold_waits_then_continues` | test | `test_boundary_hold_waits_then_continues` | [tests/d2a/test_b_resource.py:350](../../tests/d2a/test_b_resource.py#L350) |  |
| `test_boundary_planner_sees_prior_plus_cpu` | test | `test_boundary_planner_sees_prior_plus_cpu` | [tests/experiment/test_x5g1t_runtime_boundary.py:262](../../tests/experiment/test_x5g1t_runtime_boundary.py#L262) |  |
| `test_boundary_request_stop` | test | `test_boundary_request_stop` | [tests/experiment/test_x5g1t_runtime_boundary.py:285](../../tests/experiment/test_x5g1t_runtime_boundary.py#L285) |  |
| `test_boundary_resources_fail_closed` | test | `test_boundary_resources_fail_closed` | [tests/experiment/test_x5g1t_runtime_boundary.py:359](../../tests/experiment/test_x5g1t_runtime_boundary.py#L359) |  |
| `test_boundary_stop_and_invalid_raise` | test | `test_boundary_stop_and_invalid_raise` | [tests/d2a/test_b_resource.py:359](../../tests/d2a/test_b_resource.py#L359) |  |
| `test_boundary_stop_file` | test | `test_boundary_stop_file` | [tests/experiment/test_x5g1t_runtime_boundary.py:277](../../tests/experiment/test_x5g1t_runtime_boundary.py#L277) |  |
| `test_boundary_stop_while_held` | test | `test_boundary_stop_while_held` | [tests/experiment/test_x5g1t_runtime_boundary.py:334](../../tests/experiment/test_x5g1t_runtime_boundary.py#L334) |  |
| `test_bounds_both_censored` | test | `test_bounds_both_censored` | [tests/analysis/test_x5_endpoint.py:245](../../tests/analysis/test_x5_endpoint.py#L245) |  |
| `test_bounds_both_observed` | test | `test_bounds_both_observed` | [tests/analysis/test_x5_endpoint.py:217](../../tests/analysis/test_x5_endpoint.py#L217) |  |
| `test_bounds_curved_censored_flat_observed` | test | `test_bounds_curved_censored_flat_observed` | [tests/analysis/test_x5_endpoint.py:231](../../tests/analysis/test_x5_endpoint.py#L231) |  |
| `test_bounds_custom_grid_censoring` | test | `test_bounds_custom_grid_censoring` | [tests/analysis/test_x5_endpoint.py:252](../../tests/analysis/test_x5_endpoint.py#L252) |  |
| `test_bounds_d_low_equality_250` | test | `test_bounds_d_low_equality_250` | [tests/analysis/test_x5_endpoint.py:225](../../tests/analysis/test_x5_endpoint.py#L225) |  |
| `test_bounds_flat_censored_curved_observed` | test | `test_bounds_flat_censored_curved_observed` | [tests/analysis/test_x5_endpoint.py:238](../../tests/analysis/test_x5_endpoint.py#L238) |  |
| `test_bounds_rank_check_failure_is_numerical` | test | `test_bounds_rank_check_failure_is_numerical` | [tests/k4b/test_a_ranks_ladder.py:97](../../tests/k4b/test_a_ranks_ladder.py#L97) |  |
| `test_bounds_ranks_on_distinct_draws` | test | `test_bounds_ranks_on_distinct_draws` | [tests/k4b/test_a_ranks_ladder.py:80](../../tests/k4b/test_a_ranks_ladder.py#L80) |  |
| `test_bounds_with_ties` | test | `test_bounds_with_ties` | [tests/k4b/test_a_ranks_ladder.py:91](../../tests/k4b/test_a_ranks_ladder.py#L91) |  |
| `test_budget_exceeded_per_run` | test | `test_budget_exceeded_per_run` | [tests/experiment/test_x5g1_controls.py:93](../../tests/experiment/test_x5g1_controls.py#L93) |  |
| `test_budget_stop_records_incomplete_and_inconclusive` | test | `test_budget_stop_records_incomplete_and_inconclusive` | [tests/experiment/test_x5g1t_e2e.py:58](../../tests/experiment/test_x5g1t_e2e.py#L58) |  |
| `test_build_chart_claims_first_and_passes_k4b_cfg` | test | `test_build_chart_claims_first_and_passes_k4b_cfg` | [tests/k4b/test_b_charts.py:124](../../tests/k4b/test_b_charts.py#L124) |  |
| `test_build_checkpoint_is_the_learner_stage_save_body` | test | `test_build_checkpoint_is_the_learner_stage_save_body` | [tests/hwsb/test_b_e4path.py:159](../../tests/hwsb/test_b_e4path.py#L159) |  |
| `test_build_coverage_complete_with_no_seq_in_a_problem` | test | `test_build_coverage_complete_with_no_seq_in_a_problem` | [tests/k4b/test_b_registry_fixes.py:228](../../tests/k4b/test_b_registry_fixes.py#L228) |  |
| `test_build_coverage_reports_the_missing_id` | test | `test_build_coverage_reports_the_missing_id` | [tests/k4b/test_b_registry_fixes.py:241](../../tests/k4b/test_b_registry_fixes.py#L241) |  |
| `test_build_e2_from_records_only` | test | `test_build_e2_from_records_only` | [tests/experiment/test_report_e2.py:56](../../tests/experiment/test_report_e2.py#L56) |  |
| `test_build_e2_without_analysis_says_not_run` | test | `test_build_e2_without_analysis_says_not_run` | [tests/experiment/test_report_e2.py:72](../../tests/experiment/test_report_e2.py#L72) |  |
| `test_build_never_opens_a_sealed_pool_array` | test | `test_build_never_opens_a_sealed_pool_array` | [tests/k4b/test_b_registry_rules.py:374](../../tests/k4b/test_b_registry_rules.py#L374) |  |
| `test_build_on_synthetic_root_is_incomplete_and_written_once` | test | `test_build_on_synthetic_root_is_incomplete_and_written_once` | [tests/k4b/test_b_registry.py:331](../../tests/k4b/test_b_registry.py#L331) |  |
| `test_build_refuses_existing_output` | test | `test_build_refuses_existing_output` | [tests/c2_readout/test_b_registry.py:269](../../tests/c2_readout/test_b_registry.py#L269) |  |
| `test_build_refuses_unknown_version` | test | `test_build_refuses_unknown_version` | [tests/k4b/test_b_registry.py:362](../../tests/k4b/test_b_registry.py#L362) |  |
| `test_build_tiny_process_masters_argument` | test | `test_build_tiny_process_masters_argument` | [tests/hwsb/test_b_process.py:192](../../tests/hwsb/test_b_process.py#L192) |  |
| `test_build_tiny_process_shapes_and_naming` | test | `test_build_tiny_process_shapes_and_naming` | [tests/hwsb/test_b_process.py:172](../../tests/hwsb/test_b_process.py#L172) |  |
| `test_build_tiny_world` | test | `test_build_tiny_world` | [tests/hws/test_b_worlds.py:271](../../tests/hws/test_b_worlds.py#L271) |  |
| `test_build_unreadable_sources_incomplete_and_R_prime_has_four_roles` | test | `test_build_unreadable_sources_incomplete_and_R_prime_has_four_roles` | [tests/c2_readout/test_b_registry.py:277](../../tests/c2_readout/test_b_registry.py#L277) |  |
| `test_build_with_only_derived_records_is_not_incomplete` | test | `test_build_with_only_derived_records_is_not_incomplete` | [tests/k4b/test_b_store_reader.py:246](../../tests/k4b/test_b_store_reader.py#L246) |  |
| `test_build_with_stray_file_makes_k4b_store_incomplete` | test | `test_build_with_stray_file_makes_k4b_store_incomplete` | [tests/k4b/test_b_store_reader.py:259](../../tests/k4b/test_b_store_reader.py#L259) |  |
| `test_builder_failures_are_e1` | test | `test_builder_failures_are_e1` | [tests/hws/test_b_worlds.py:379](../../tests/hws/test_b_worlds.py#L379) |  |
| `test_builders_hit_their_outcomes` | test | `test_builders_hit_their_outcomes` | [tests/d2a/test_b_rules_qualifiers.py:102](../../tests/d2a/test_b_rules_qualifiers.py#L102) |  |
| `test_builds_are_deterministic` | test | `test_builds_are_deterministic` | [tests/world/test_world.py:321](../../tests/world/test_world.py#L321) |  |
| `test_C01_id_independent_of_key_order` | test | `test_C01_id_independent_of_key_order` | [tests/contracts/test_ids.py:38](../../tests/contracts/test_ids.py#L38) |  |
| `test_C01_id_independent_of_parent_order_and_container` | test | `test_C01_id_independent_of_parent_order_and_container` | [tests/contracts/test_ids.py:45](../../tests/contracts/test_ids.py#L45) |  |
| `test_C01_id_known_answer_and_shape` | test | `test_C01_id_known_answer_and_shape` | [tests/contracts/test_ids.py:28](../../tests/contracts/test_ids.py#L28) |  |
| `test_C02_id_changes_with_each_input` | test | `test_C02_id_changes_with_each_input` | [tests/contracts/test_ids.py:50](../../tests/contracts/test_ids.py#L50) |  |
| `test_C03_canonical_json_floats_and_numpy` | test | `test_C03_canonical_json_floats_and_numpy` | [tests/contracts/test_ids.py:83](../../tests/contracts/test_ids.py#L83) |  |
| `test_C03_canonical_json_known_answers` | test | `test_C03_canonical_json_known_answers` | [tests/contracts/test_ids.py:69](../../tests/contracts/test_ids.py#L69) |  |
| `test_C03_canonical_json_rejects_nonfinite` | test | `test_C03_canonical_json_rejects_nonfinite` | [tests/contracts/test_ids.py:101](../../tests/contracts/test_ids.py#L101) |  |
| `test_C04_all_16_classes_covered` | test | `test_C04_all_16_classes_covered` | [tests/contracts/test_store.py:83](../../tests/contracts/test_store.py#L83) |  |
| `test_C04_find_filters_by_config` | test | `test_C04_find_filters_by_config` | [tests/contracts/test_store.py:132](../../tests/contracts/test_store.py#L132) |  |
| `test_C04_roundtrip_localfs` | test | `test_C04_roundtrip_localfs` | [tests/contracts/test_store.py:110](../../tests/contracts/test_store.py#L110) |  |
| `test_C04_roundtrip_memory` | test | `test_C04_roundtrip_memory` | [tests/contracts/test_store.py:94](../../tests/contracts/test_store.py#L94) |  |
| `test_C04_save_validates_first` | test | `test_C04_save_validates_first` | [tests/contracts/test_store.py:141](../../tests/contracts/test_store.py#L141) |  |
| `test_C05_same_id_different_content_is_checksum_mismatch` | test | `test_C05_same_id_different_content_is_checksum_mismatch` | [tests/contracts/test_store.py:160](../../tests/contracts/test_store.py#L160) |  |
| `test_C05_second_save_is_noop` | test | `test_C05_second_save_is_noop` | [tests/contracts/test_store.py:149](../../tests/contracts/test_store.py#L149) |  |
| `test_C05_tampered_checkpoint_blob_detected` | test | `test_C05_tampered_checkpoint_blob_detected` | [tests/contracts/test_store.py:194](../../tests/contracts/test_store.py#L194) |  |
| `test_C05_tampered_payload_detected` | test | `test_C05_tampered_payload_detected` | [tests/contracts/test_store.py:184](../../tests/contracts/test_store.py#L184) |  |
| `test_C06_incomplete_refused` | test | `test_C06_incomplete_refused` | [tests/contracts/test_store.py:211](../../tests/contracts/test_store.py#L211) |  |
| `test_C06_unknown_id_is_missing` | test | `test_C06_unknown_id_is_missing` | [tests/contracts/test_store.py:219](../../tests/contracts/test_store.py#L219) |  |
| `test_C07_schema_version` | test | `test_C07_schema_version` | [tests/contracts/test_store.py:227](../../tests/contracts/test_store.py#L227) |  |
| `test_C08_custom_policy` | test | `test_C08_custom_policy` | [tests/contracts/test_store.py:281](../../tests/contracts/test_store.py#L281) |  |
| `test_C08_default_policy_table` | test | `test_C08_default_policy_table` | [tests/contracts/test_store.py:261](../../tests/contracts/test_store.py#L261) |  |
| `test_C08_learner_cannot_load_evalsidecar` | test | `test_C08_learner_cannot_load_evalsidecar` | [tests/contracts/test_store.py:239](../../tests/contracts/test_store.py#L239) |  |
| `test_C08_policy_checked_before_existence` | test | `test_C08_policy_checked_before_existence` | [tests/contracts/test_store.py:247](../../tests/contracts/test_store.py#L247) |  |
| `test_C09_seed_known_answers` | test | `test_C09_seed_known_answers` | [tests/contracts/test_ids.py:112](../../tests/contracts/test_ids.py#L112) |  |
| `test_C09_seed_sensitivity` | test | `test_C09_seed_sensitivity` | [tests/contracts/test_ids.py:121](../../tests/contracts/test_ids.py#L121) |  |
| `test_c0_bundle_sums_ticket_and_chain_parameters` | test | `test_c0_bundle_sums_ticket_and_chain_parameters` | [tests/x6_stage1/test_b_nb_s0_ops.py:72](../../tests/x6_stage1/test_b_nb_s0_ops.py#L72) |  |
| `test_c0_val_direct_giant_failure_is_chart_unavailable` | test | `test_c0_val_direct_giant_failure_is_chart_unavailable` | [tests/k4b/test_b_charts.py:341](../../tests/k4b/test_b_charts.py#L341) |  |
| `test_c0_val_gate_refused_before_freeze_spends_no_construction` | test | `test_c0_val_gate_refused_before_freeze_spends_no_construction` | [tests/k4b/test_b_charts.py:268](../../tests/k4b/test_b_charts.py#L268) |  |
| `test_c0_val_support_506_is_chart_unavailable` | test | `test_c0_val_support_506_is_chart_unavailable` | [tests/k4b/test_b_charts.py:337](../../tests/k4b/test_b_charts.py#L337) |  |
| `test_c0_val_support_507_passes_without_gauge_or_refit` | test | `test_c0_val_support_507_passes_without_gauge_or_refit` | [tests/k4b/test_b_charts.py:323](../../tests/k4b/test_b_charts.py#L323) |  |
| `test_c0_val_support_threshold_with_k4b_cfg` | test | `test_c0_val_support_threshold_with_k4b_cfg` | [tests/k4b/test_b_charts.py:354](../../tests/k4b/test_b_charts.py#L354) |  |
| `test_C10_generator_streams` | test | `test_C10_generator_streams` | [tests/contracts/test_ids.py:128](../../tests/contracts/test_ids.py#L128) |  |
| `test_C11_alignment_errors` | test | `test_C11_alignment_errors` | [tests/contracts/test_layout.py:62](../../tests/contracts/test_layout.py#L62) |  |
| `test_C11_history` | test | `test_C11_history` | [tests/contracts/test_layout.py:35](../../tests/contracts/test_layout.py#L35) |  |
| `test_C11_inputs_targets_history_known_answer` | test | `test_C11_inputs_targets_history_known_answer` | [tests/contracts/test_layout.py:13](../../tests/contracts/test_layout.py#L13) |  |
| `test_C11_targets_is_a_copy` | test | `test_C11_targets_is_a_copy` | [tests/contracts/test_layout.py:44](../../tests/contracts/test_layout.py#L44) |  |
| `test_C12_bundle_into_memory_store` | test | `test_C12_bundle_into_memory_store` | [tests/contracts/test_store.py:323](../../tests/contracts/test_store.py#L323) |  |
| `test_C12_bundle_roundtrip` | test | `test_C12_bundle_roundtrip` | [tests/contracts/test_store.py:304](../../tests/contracts/test_store.py#L304) |  |
| `test_C12_bundle_without_parents_needs_parents` | test | `test_C12_bundle_without_parents_needs_parents` | [tests/contracts/test_store.py:332](../../tests/contracts/test_store.py#L332) |  |
| `test_C12_missing_parent_on_save` | test | `test_C12_missing_parent_on_save` | [tests/contracts/test_store.py:298](../../tests/contracts/test_store.py#L298) |  |
| `test_C12b_bundle_bytes_are_deterministic` | test | `test_C12b_bundle_bytes_are_deterministic` | [tests/contracts/test_bundle_determinism.py:8](../../tests/contracts/test_bundle_determinism.py#L8) | Equal content exported twice (to different file names) gives byte-identical bundles. |
| `test_C13_data_artifacts` | test | `test_C13_data_artifacts` | [tests/contracts/test_schemas.py:91](../../tests/contracts/test_schemas.py#L91) |  |
| `test_C13_emission_dead_symbol` | test | `test_C13_emission_dead_symbol` | [tests/contracts/test_schemas.py:39](../../tests/contracts/test_schemas.py#L39) |  |
| `test_C13_emission_other_violations` | test | `test_C13_emission_other_violations` | [tests/contracts/test_schemas.py:48](../../tests/contracts/test_schemas.py#L48) |  |
| `test_C13_history_index_other_violations` | test | `test_C13_history_index_other_violations` | [tests/contracts/test_schemas.py:67](../../tests/contracts/test_schemas.py#L67) |  |
| `test_C13_history_index_overlapping_panels` | test | `test_C13_history_index_overlapping_panels` | [tests/contracts/test_schemas.py:59](../../tests/contracts/test_schemas.py#L59) |  |
| `test_C13_misc_artifacts` | test | `test_C13_misc_artifacts` | [tests/contracts/test_schemas.py:103](../../tests/contracts/test_schemas.py#L103) |  |
| `test_C13_stagefailure_basics` | test | `test_C13_stagefailure_basics` | [tests/contracts/test_schemas.py:133](../../tests/contracts/test_schemas.py#L133) |  |
| `test_C13_transition_asymmetric_and_stationarity` | test | `test_C13_transition_asymmetric_and_stationarity` | [tests/contracts/test_schemas.py:30](../../tests/contracts/test_schemas.py#L30) |  |
| `test_C13_transition_row_sum` | test | `test_C13_transition_row_sum` | [tests/contracts/test_schemas.py:18](../../tests/contracts/test_schemas.py#L18) |  |
| `test_C13_world_spec` | test | `test_C13_world_spec` | [tests/contracts/test_schemas.py:76](../../tests/contracts/test_schemas.py#L76) |  |
| `test_C14_memory_store_is_fresh_and_works` | test | `test_C14_memory_store_is_fresh_and_works` | [tests/contracts/test_fixtures.py:64](../../tests/contracts/test_fixtures.py#L64) |  |
| `test_C14_tiny_hmm_is_a_valid_hmm` | test | `test_C14_tiny_hmm_is_a_valid_hmm` | [tests/contracts/test_fixtures.py:38](../../tests/contracts/test_fixtures.py#L38) |  |
| `test_C14_tiny_observations_valid_and_deterministic` | test | `test_C14_tiny_observations_valid_and_deterministic` | [tests/contracts/test_fixtures.py:51](../../tests/contracts/test_fixtures.py#L51) |  |
| `test_C14_tiny_world_spec_deterministic_and_sizes` | test | `test_C14_tiny_world_spec_deterministic_and_sizes` | [tests/contracts/test_fixtures.py:26](../../tests/contracts/test_fixtures.py#L26) |  |
| `test_C14_tiny_world_spec_valid_and_counts` | test | `test_C14_tiny_world_spec_valid_and_counts` | [tests/contracts/test_fixtures.py:15](../../tests/contracts/test_fixtures.py#L15) |  |
| `test_c1prime_landmarks_enter_R_through_reader_d` | test | `test_c1prime_landmarks_enter_R_through_reader_d` | [tests/c2_readout/test_b_registry.py:342](../../tests/c2_readout/test_b_registry.py#L342) |  |
| `test_c1stop_carries_gate_status_reason` | test | `test_c1stop_carries_gate_status_reason` | [tests/c1prime/test_a_exceptions.py:208](../../tests/c1prime/test_a_exceptions.py#L208) |  |
| `test_c_hor` | test | `test_c_hor` | [tests/d2a/test_b_rules_flags.py:204](../../tests/d2a/test_b_rules_flags.py#L204) |  |
| `test_c_len_gain_and_loss_at_boundaries` | test | `test_c_len_gain_and_loss_at_boundaries` | [tests/d2a/test_b_rules_flags.py:214](../../tests/d2a/test_b_rules_flags.py#L214) |  |
| `test_c_len_missing_input_is_unresolved` | test | `test_c_len_missing_input_is_unresolved` | [tests/d2a/test_b_rules_flags.py:239](../../tests/d2a/test_b_rules_flags.py#L239) |  |
| `test_c_len_missing_or_undefined_seed_is_unresolved` | test | `test_c_len_missing_or_undefined_seed_is_unresolved` | [tests/d2a/test_b_rules_flags.py:245](../../tests/d2a/test_b_rules_flags.py#L245) |  |
| `test_c_len_nan_mean_or_interval_endpoint_is_unresolved` | test | `test_c_len_nan_mean_or_interval_endpoint_is_unresolved` | [tests/d2a/test_b_rules_flags.py:252](../../tests/d2a/test_b_rules_flags.py#L252) |  |
| `test_c_len_not_detected` | test | `test_c_len_not_detected` | [tests/d2a/test_b_rules_flags.py:228](../../tests/d2a/test_b_rules_flags.py#L228) |  |
| `test_c_len_precision_failure_overrides_every_result` | test | `test_c_len_precision_failure_overrides_every_result` | [tests/d2a/test_b_rules_flags.py:233](../../tests/d2a/test_b_rules_flags.py#L233) |  |
| `test_c_min_expected_orientation` | test | `test_c_min_expected_orientation` | [tests/hwsb/test_a_capture.py:160](../../tests/hwsb/test_a_capture.py#L160) |  |
| `test_c_min_formula` | test | `test_c_min_formula` | [tests/hwsb/test_a_capture.py:151](../../tests/hwsb/test_a_capture.py#L151) |  |
| `test_c_min_literal_uses_z_one_minus_alpha_only_and_keeps_f_plan` | test | `test_c_min_literal_uses_z_one_minus_alpha_only_and_keeps_f_plan` | [tests/hwsb/test_a_capture.py:169](../../tests/hwsb/test_a_capture.py#L169) |  |
| `test_cache_filled_under_one_process_never_hits_under_another` | test | `test_cache_filled_under_one_process_never_hits_under_another` | [tests/circle_history/test_reference_binding.py:95](../../tests/circle_history/test_reference_binding.py#L95) |  |
| `test_cache_only_hits_a_filled_cache` | test | `test_cache_only_hits_a_filled_cache` | [tests/circle_history/test_reference_binding.py:115](../../tests/circle_history/test_reference_binding.py#L115) |  |
| `test_cache_only_miss_raises_before_any_reference` | test | `test_cache_only_miss_raises_before_any_reference` | [tests/circle_history/test_reference_binding.py:124](../../tests/circle_history/test_reference_binding.py#L124) | With E_BAD the reference itself would fail (impossible suffix); the miss error shows that |
| `test_calibration_obs_dev_v36` | test | `test_calibration_obs_dev_v36` | [tests/experiment/test_x5g1_lineage.py:138](../../tests/experiment/test_x5g1_lineage.py#L138) |  |
| `test_callback_identical_to_learner_stage` | test | `test_callback_identical_to_learner_stage` | [tests/experiment/test_x5g1t_training.py:126](../../tests/experiment/test_x5g1t_training.py#L126) |  |
| `test_cancellation_fixture_energy_blocks_not_used` | test | `test_cancellation_fixture_energy_blocks_not_used` | [tests/c2_readout/test_a_partition.py:231](../../tests/c2_readout/test_a_partition.py#L231) |  |
| `test_candidate_order_is_first_appearance_not_value` | test | `test_candidate_order_is_first_appearance_not_value` | [tests/analysis/test_sigma_calibrator.py:52](../../tests/analysis/test_sigma_calibrator.py#L52) |  |
| `test_canonical32_and_named32_invert_exactly` | test | `test_canonical32_and_named32_invert_exactly` | [tests/hwsb/test_b_streams.py:238](../../tests/hwsb/test_b_streams.py#L238) |  |
| `test_canonical32_inverts_the_named_permutation` | test | `test_canonical32_inverts_the_named_permutation` | [tests/c1prime_registry/test_registry_builder.py:25](../../tests/c1prime_registry/test_registry_builder.py#L25) |  |
| `test_canonical32_rejects_a_non_permutation` | test | `test_canonical32_rejects_a_non_permutation` | [tests/c1prime_registry/test_registry_builder.py:33](../../tests/c1prime_registry/test_registry_builder.py#L33) |  |
| `test_canonical_emission_is_the_column_permutation` | test | `test_canonical_emission_is_the_column_permutation` | [tests/oracle_profile/test_oracle_profile_traps.py:184](../../tests/oracle_profile/test_oracle_profile_traps.py#L184) | Item 4. |
| `test_canonical_emission_rejects_non_permutations` | test | `test_canonical_emission_rejects_non_permutations` | [tests/oracle_profile/test_oracle_profile_traps.py:218](../../tests/oracle_profile/test_oracle_profile_traps.py#L218) | Item 4. |
| `test_canonical_filtering_equals_named_filtering` | test | `test_canonical_filtering_equals_named_filtering` | [tests/oracle_profile/test_oracle_profile_traps.py:194](../../tests/oracle_profile/test_oracle_profile_traps.py#L194) | Item 4: canonical tokens with E_canon == named tokens symbol_perm[canonical] with E_named. |
| `test_canonical_from_named_inverse_permutation` | test | `test_canonical_from_named_inverse_permutation` | [tests/circle_history/test_scores_precision.py:78](../../tests/circle_history/test_scores_precision.py#L78) |  |
| `test_canonical_from_named_rejects_non_permutations` | test | `test_canonical_from_named_rejects_non_permutations` | [tests/circle_history/test_scores_precision.py:96](../../tests/circle_history/test_scores_precision.py#L96) |  |
| `test_canonical_from_named_round_trip_check_catches_negative_named` | test | `test_canonical_from_named_round_trip_check_catches_negative_named` | [tests/circle_history/test_scores_precision.py:102](../../tests/circle_history/test_scores_precision.py#L102) |  |
| `test_canonical_from_named_round_trips_contract_formula` | test | `test_canonical_from_named_round_trips_contract_formula` | [tests/circle_history/test_scores_precision.py:87](../../tests/circle_history/test_scores_precision.py#L87) |  |
| `test_canonical_tokens_invert_the_symbol_permutation` | test | `test_canonical_tokens_invert_the_symbol_permutation` | [tests/experiment/test_x4b.py:52](../../tests/experiment/test_x4b.py#L52) |  |
| `test_cap_constant_and_boundary` | test | `test_cap_constant_and_boundary` | [tests/k4b/test_a_lemma_n.py:245](../../tests/k4b/test_a_lemma_n.py#L245) |  |
| `test_cap_exceeded_before_first_bound` | test | `test_cap_exceeded_before_first_bound` | [tests/circle_history/test_cochain_lift.py:251](../../tests/circle_history/test_cochain_lift.py#L251) |  |
| `test_cap_is_exact_not_float` | test | `test_cap_is_exact_not_float` | [tests/k4b/test_a_lemma_n.py:254](../../tests/k4b/test_a_lemma_n.py#L254) |  |
| `test_cap_not_reached_succeeds` | test | `test_cap_not_reached_succeeds` | [tests/circle_history/test_cochain_lift.py:256](../../tests/circle_history/test_cochain_lift.py#L256) |  |
| `test_capture_pass_equality_and_one_ulp_below` | test | `test_capture_pass_equality_and_one_ulp_below` | [tests/hwsb/test_a_capture.py:180](../../tests/hwsb/test_a_capture.py#L180) |  |
| `test_carries` | test | `test_carries` | [tests/d2a/test_b_rules_flags.py:148](../../tests/d2a/test_b_rules_flags.py#L148) |  |
| `test_cauchy_schwarz_bound_holds_and_matches_its_formula` | test | `test_cauchy_schwarz_bound_holds_and_matches_its_formula` | [tests/c2_readout/test_a_partition.py:246](../../tests/c2_readout/test_a_partition.py#L246) |  |
| `test_causality_non_identity_patch` | test | `test_causality_non_identity_patch` | [tests/learner/test_patch.py:93](../../tests/learner/test_patch.py#L93) |  |
| `test_caveat_reread` | test | `test_caveat_reread` | [tests/d2a/test_b_rules_qualifiers.py:185](../../tests/d2a/test_b_rules_qualifiers.py#L185) |  |
| `test_caveat_reread_on_not_recovered` | test | `test_caveat_reread_on_not_recovered` | [tests/d2a/test_b_rules_qualifiers.py:191](../../tests/d2a/test_b_rules_qualifiers.py#L191) |  |
| `test_cc_oracle_null` | test | `test_cc_oracle_null` | [tests/d2a/test_a_targets.py:218](../../tests/d2a/test_a_targets.py#L218) |  |
| `test_cell_templates_verbatim_from_api` | test | `test_cell_templates_verbatim_from_api` | [tests/x6_stage1/test_b_nb_s0_ops.py:122](../../tests/x6_stage1/test_b_nb_s0_ops.py#L122) |  |
| `test_centered_draws_reproduce_manual_loop_with_shared_idx` | test | `test_centered_draws_reproduce_manual_loop_with_shared_idx` | [tests/circle_history/test_scores_precision_gates.py:116](../../tests/circle_history/test_scores_precision_gates.py#L116) |  |
| `test_centered_is_precision_centered_draws` | test | `test_centered_is_precision_centered_draws` | [tests/k4b/test_a_ranks_ladder.py:189](../../tests/k4b/test_a_ranks_ladder.py#L189) |  |
| `test_centres_in_softmax_enclosure_order` | test | `test_centres_in_softmax_enclosure_order` | [tests/hwsb/test_a_enclosure_proof.py:167](../../tests/hwsb/test_a_enclosure_proof.py#L167) |  |
| `test_centres_rectangular_and_gridcenters_bitwise` | test | `test_centres_rectangular_and_gridcenters_bitwise` | [tests/hws/test_b_worlds.py:143](../../tests/hws/test_b_worlds.py#L143) |  |
| `test_certified_kernel_calls_no_blas_matmul_or_numpy_reduction` | test | `test_certified_kernel_calls_no_blas_matmul_or_numpy_reduction` | [tests/c1prime/test_b_cert_guards.py:210](../../tests/c1prime/test_b_cert_guards.py#L210) |  |
| `test_certify_rows_certifies_exact_pipeline` | test | `test_certify_rows_certifies_exact_pipeline` | [tests/circle_history/test_error_bound.py:297](../../tests/circle_history/test_error_bound.py#L297) |  |
| `test_certify_rows_moment_shift_is_fail_technical` | test | `test_certify_rows_moment_shift_is_fail_technical` | [tests/circle_history/test_error_bound.py:321](../../tests/circle_history/test_error_bound.py#L321) |  |
| `test_certify_rows_operational_range_and_nonfinite_fail_technical` | test | `test_certify_rows_operational_range_and_nonfinite_fail_technical` | [tests/circle_history/test_error_bound.py:330](../../tests/circle_history/test_error_bound.py#L330) |  |
| `test_certify_rows_reports_moment_check_by_k` | test | `test_certify_rows_reports_moment_check_by_k` | [tests/circle_history/test_reference_binding.py:194](../../tests/circle_history/test_reference_binding.py#L194) |  |
| `test_certify_rows_shifted_score_is_inconclusive` | test | `test_certify_rows_shifted_score_is_inconclusive` | [tests/circle_history/test_error_bound.py:306](../../tests/circle_history/test_error_bound.py#L306) |  |
| `test_cfg_comes_from_contract_values` | test | `test_cfg_comes_from_contract_values` | [tests/circle_history/test_scores_precision_gates.py:65](../../tests/circle_history/test_scores_precision_gates.py#L65) |  |
| `test_changed_byte_fails_closed` | test | `test_changed_byte_fails_closed` | [tests/hwsb/test_b_registry.py:165](../../tests/hwsb/test_b_registry.py#L165) |  |
| `test_chart_arrays_round_trip_exact` | test | `test_chart_arrays_round_trip_exact` | [tests/circle_history/test_chart_arrays.py:84](../../tests/circle_history/test_chart_arrays.py#L84) |  |
| `test_chart_arrays_survive_npz_without_pickle` | test | `test_chart_arrays_survive_npz_without_pickle` | [tests/circle_history/test_chart_arrays.py:97](../../tests/circle_history/test_chart_arrays.py#L97) |  |
| `test_chart_cfg_equals_c1prime_cfg` | test | `test_chart_cfg_equals_c1prime_cfg` | [tests/k4b/test_b_charts.py:96](../../tests/k4b/test_b_charts.py#L96) |  |
| `test_chart_gates_all_pass_with_exactly_eight_per_bin` | test | `test_chart_gates_all_pass_with_exactly_eight_per_bin` | [tests/circle_history/test_chart_extension.py:333](../../tests/circle_history/test_chart_extension.py#L333) |  |
| `test_chart_gates_defects_invalid` | test | `test_chart_gates_defects_invalid` | [tests/circle_history/test_chart_extension.py:385](../../tests/circle_history/test_chart_extension.py#L385) |  |
| `test_chart_gates_fidelity_boundary` | test | `test_chart_gates_fidelity_boundary` | [tests/circle_history/test_chart_extension.py:350](../../tests/circle_history/test_chart_extension.py#L350) |  |
| `test_chart_gates_resultant_boundary` | test | `test_chart_gates_resultant_boundary` | [tests/circle_history/test_chart_extension.py:364](../../tests/circle_history/test_chart_extension.py#L364) |  |
| `test_chart_gates_seven_in_a_bin_is_inconclusive` | test | `test_chart_gates_seven_in_a_bin_is_inconclusive` | [tests/circle_history/test_chart_extension.py:343](../../tests/circle_history/test_chart_extension.py#L343) |  |
| `test_chart_gates_support_and_overall_order` | test | `test_chart_gates_support_and_overall_order` | [tests/circle_history/test_chart_extension.py:372](../../tests/circle_history/test_chart_extension.py#L372) |  |
| `test_charts_refuse_tampered_reference_identity` | test | `test_charts_refuse_tampered_reference_identity` | [tests/circle_history/test_builder_v24_stages.py:127](../../tests/circle_history/test_builder_v24_stages.py#L127) |  |
| `test_charts_reuse_reference_without_recomputation` | test | `test_charts_reuse_reference_without_recomputation` | [tests/circle_history/test_builder_v24_stages.py:101](../../tests/circle_history/test_builder_v24_stages.py#L101) |  |
| `test_check_boundary_equal_passes_above_raises` | test | `test_check_boundary_equal_passes_above_raises` | [tests/experiment/test_x5g1t_runtime_boundary.py:125](../../tests/experiment/test_x5g1t_runtime_boundary.py#L125) |  |
| `test_check_bundle_refuses_forbidden_classes` | test | `test_check_bundle_refuses_forbidden_classes` | [tests/x6_stage1/test_b_nb_s0_ops.py:109](../../tests/x6_stage1/test_b_nb_s0_ops.py#L109) |  |
| `test_check_causal_joint_passes_clean_model_and_catches_a_leak` | test | `test_check_causal_joint_passes_clean_model_and_catches_a_leak` | [tests/learner/test_multihorizon.py:223](../../tests/learner/test_multihorizon.py#L223) |  |
| `test_check_chart_equality_default_is_equal` | test | `test_check_chart_equality_default_is_equal` | [tests/k4b/test_b_charts.py:105](../../tests/k4b/test_b_charts.py#L105) |  |
| `test_check_chart_equality_detects_each_difference` | test | `test_check_chart_equality_detects_each_difference` | [tests/k4b/test_b_charts.py:111](../../tests/k4b/test_b_charts.py#L111) |  |
| `test_check_closure_explicit` | test | `test_check_closure_explicit` | [tests/circle_history/test_cochain.py:128](../../tests/circle_history/test_cochain.py#L128) |  |
| `test_check_congruence_explicit` | test | `test_check_congruence_explicit` | [tests/circle_history/test_cochain.py:146](../../tests/circle_history/test_cochain.py#L146) |  |
| `test_check_execution_accepts_registered_sequences` | test | `test_check_execution_accepts_registered_sequences` | [tests/x6_stage1/test_b_chain_ops.py:381](../../tests/x6_stage1/test_b_chain_ops.py#L381) |  |
| `test_check_execution_final_record_rules` | test | `test_check_execution_final_record_rules` | [tests/x6_stage1/test_b_chain_ops.py:393](../../tests/x6_stage1/test_b_chain_ops.py#L393) |  |
| `test_check_execution_refuses_edits_extra_code_and_order` | test | `test_check_execution_refuses_edits_extra_code_and_order` | [tests/x6_stage1/test_b_chain_ops.py:389](../../tests/x6_stage1/test_b_chain_ops.py#L389) |  |
| `test_check_handoff_accepts_clean_record` | test | `test_check_handoff_accepts_clean_record` | [tests/hwsb/test_a_outcomes.py:296](../../tests/hwsb/test_a_outcomes.py#L296) |  |
| `test_check_handoff_refuses_extra_top_level_key` | test | `test_check_handoff_refuses_extra_top_level_key` | [tests/hwsb/test_a_outcomes.py:315](../../tests/hwsb/test_a_outcomes.py#L315) |  |
| `test_check_handoff_refuses_forbidden_key_at_any_depth` | test | `test_check_handoff_refuses_forbidden_key_at_any_depth` | [tests/hwsb/test_a_outcomes.py:305](../../tests/hwsb/test_a_outcomes.py#L305) |  |
| `test_check_pass_set_names_the_prerequisite_gates` | test | `test_check_pass_set_names_the_prerequisite_gates` | [tests/c1prime/test_a_gates.py:177](../../tests/c1prime/test_a_gates.py#L177) |  |
| `test_check_resources_caps` | test | `test_check_resources_caps` | [tests/experiment/test_x5g1t_runtime_boundary.py:184](../../tests/experiment/test_x5g1t_runtime_boundary.py#L184) |  |
| `test_check_rows_boundary_at_tolerance` | test | `test_check_rows_boundary_at_tolerance` | [tests/hwsb/test_a_learning.py:196](../../tests/hwsb/test_a_learning.py#L196) |  |
| `test_check_rows_refuses_nan_negative_inf` | test | `test_check_rows_refuses_nan_negative_inf` | [tests/hwsb/test_a_learning.py:218](../../tests/hwsb/test_a_learning.py#L218) |  |
| `test_check_sequence` | test | `test_check_sequence` | [tests/c2_readout/test_b_policy.py:153](../../tests/c2_readout/test_b_policy.py#L153) |  |
| `test_check_unsealed_accepts_a_clean_report` | test | `test_check_unsealed_accepts_a_clean_report` | [tests/k4b/test_b_flow.py:53](../../tests/k4b/test_b_flow.py#L53) |  |
| `test_check_unsealed_refuses_any_sealed_key_anywhere` | test | `test_check_unsealed_refuses_any_sealed_key_anywhere` | [tests/k4b/test_b_flow.py:59](../../tests/k4b/test_b_flow.py#L59) |  |
| `test_checked_computation_before_failure_skips_fn` | test | `test_checked_computation_before_failure_skips_fn` | [tests/experiment/test_x5g1_safety.py:186](../../tests/experiment/test_x5g1_safety.py#L186) |  |
| `test_checked_computation_returns_result_when_clean` | test | `test_checked_computation_returns_result_when_clean` | [tests/experiment/test_x5g1_safety.py:174](../../tests/experiment/test_x5g1_safety.py#L174) |  |
| `test_checked_computation_tamper_inside_fn_raises_after` | test | `test_checked_computation_tamper_inside_fn_raises_after` | [tests/experiment/test_x5g1_safety.py:205](../../tests/experiment/test_x5g1_safety.py#L205) |  |
| `test_checkpoint_meta_reads_meta_json_only` | test | `test_checkpoint_meta_reads_meta_json_only` | [tests/k4b/test_b_h1_meta.py:302](../../tests/k4b/test_b_h1_meta.py#L302) |  |
| `test_checkpoint_meta_reads_the_named_id_only` | test | `test_checkpoint_meta_reads_the_named_id_only` | [tests/k4b/test_b_h1_meta.py:342](../../tests/k4b/test_b_h1_meta.py#L342) |  |
| `test_checkpoint_meta_unreadable_or_malformed_is_identity` | test | `test_checkpoint_meta_unreadable_or_malformed_is_identity` | [tests/k4b/test_b_h1_meta.py:320](../../tests/k4b/test_b_h1_meta.py#L320) |  |
| `test_checkpoint_not_published_when_reread_differs` | test | `test_checkpoint_not_published_when_reread_differs` | [tests/x6_stage1/test_b_train_chain.py:288](../../tests/x6_stage1/test_b_train_chain.py#L288) |  |
| `test_checkpoint_order_statistic_hand_values` | test | `test_checkpoint_order_statistic_hand_values` | [tests/analysis/test_baselines_dynamics.py:85](../../tests/analysis/test_baselines_dynamics.py#L85) |  |
| `test_checkpoint_write_single_buffer_fsync_and_duplicate_refusal` | test | `test_checkpoint_write_single_buffer_fsync_and_duplicate_refusal` | [tests/x6_stage1/test_b_train_chain.py:273](../../tests/x6_stage1/test_b_train_chain.py#L273) |  |
| `test_checkpoints_grid_differs_rejected` | test | `test_checkpoints_grid_differs_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:138](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L138) |  |
| `test_checkpoints_missing_one_rejected` | test | `test_checkpoints_missing_one_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:132](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L132) |  |
| `test_checkpoints_not_a_checkpoint_rejected` | test | `test_checkpoints_not_a_checkpoint_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:208](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L208) |  |
| `test_checkpoints_of_another_master_rejected` | test | `test_checkpoints_of_another_master_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:185](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L185) | outcome claims master 310001 but the checkpoints carry 310002's run key. |
| `test_checkpoints_outcome_arm_mismatch_rejected` | test | `test_checkpoints_outcome_arm_mismatch_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:171](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L171) |  |
| `test_checkpoints_outcome_master_mismatch_rejected` | test | `test_checkpoints_outcome_master_mismatch_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:178](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L178) |  |
| `test_checkpoints_recorded_sha_wrong_rejected` | test | `test_checkpoints_recorded_sha_wrong_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:202](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L202) |  |
| `test_checkpoints_reordered_rejected` | test | `test_checkpoints_reordered_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:118](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L118) |  |
| `test_checkpoints_same_metadata_mutated_payload_rejected` | test | `test_checkpoints_same_metadata_mutated_payload_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:215](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L215) |  |
| `test_checkpoints_saved_with_wrong_parents_rejected` | test | `test_checkpoints_saved_with_wrong_parents_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:146](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L146) |  |
| `test_checkpoints_saved_with_wrong_train_config_rejected` | test | `test_checkpoints_saved_with_wrong_train_config_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:162](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L162) |  |
| `test_checkpoints_swapped_ids_same_steps_rejected` | test | `test_checkpoints_swapped_ids_same_steps_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:124](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L124) |  |
| `test_checkpoints_wrong_dev_parent_rejected` | test | `test_checkpoints_wrong_dev_parent_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:142](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L142) |  |
| `test_checkpoints_wrong_model_config_rejected` | test | `test_checkpoints_wrong_model_config_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:154](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L154) |  |
| `test_checkpoints_wrong_observation_id_rejected` | test | `test_checkpoints_wrong_observation_id_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:194](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L194) |  |
| `test_checkpoints_wrong_steps_rejected` | test | `test_checkpoints_wrong_steps_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:158](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L158) |  |
| `test_chi2_skipped_below_200_and_passes_on_exact_counts` | test | `test_chi2_skipped_below_200_and_passes_on_exact_counts` | [tests/dataset/test_stage.py:91](../../tests/dataset/test_stage.py#L91) |  |
| `test_child_env_default_copies_os_environ` | test | `test_child_env_default_copies_os_environ` | [tests/k4b/test_b_meter.py:106](../../tests/k4b/test_b_meter.py#L106) |  |
| `test_child_env_temp_on_x_and_single_thread` | test | `test_child_env_temp_on_x_and_single_thread` | [tests/k4b/test_b_meter.py:93](../../tests/k4b/test_b_meter.py#L93) |  |
| `test_chord_hand_values` | test | `test_chord_hand_values` | [tests/topology/test_metrics.py:33](../../tests/topology/test_metrics.py#L33) |  |
| `test_chord_zero_row_raises` | test | `test_chord_zero_row_raises` | [tests/topology/test_metrics.py:90](../../tests/topology/test_metrics.py#L90) |  |
| `test_chunked_equals_trainer_bitwise_with_two_fresh_process_resumes` | test | `test_chunked_equals_trainer_bitwise_with_two_fresh_process_resumes` | [tests/x6_stage1/test_b_train_chain.py:207](../../tests/x6_stage1/test_b_train_chain.py#L207) |  |
| `test_circle_code_in_the_head_kernel_is_a_valid_not_used` | test | `test_circle_code_in_the_head_kernel_is_a_valid_not_used` | [tests/c2_readout/test_a_partition.py:278](../../tests/c2_readout/test_a_partition.py#L278) |  |
| `test_circle_expectation_errors` | test | `test_circle_expectation_errors` | [tests/analysis/test_x4f_targets.py:62](../../tests/analysis/test_x4f_targets.py#L62) |  |
| `test_circle_features_all_twelve_positions` | test | `test_circle_features_all_twelve_positions` | [tests/oracle_profile/test_oracle_profile_kernels.py:112](../../tests/oracle_profile/test_oracle_profile_kernels.py#L112) |  |
| `test_circle_features_known_answers` | test | `test_circle_features_known_answers` | [tests/oracle_profile/test_oracle_profile_kernels.py:100](../../tests/oracle_profile/test_oracle_profile_kernels.py#L100) |  |
| `test_circle_features_rejects_bad_coordinates` | test | `test_circle_features_rejects_bad_coordinates` | [tests/oracle_profile/test_oracle_profile_kernels.py:121](../../tests/oracle_profile/test_oracle_profile_kernels.py#L121) |  |
| `test_claims_survive_a_new_ledger_object` | test | `test_claims_survive_a_new_ledger_object` | [tests/c1prime/test_a_chart_val.py:212](../../tests/c1prime/test_a_chart_val.py#L212) |  |
| `test_classify_all_latches_synthetic_in_its_own_dir` | test | `test_classify_all_latches_synthetic_in_its_own_dir` | [tests/oracle_profile/test_builder_controls.py:234](../../tests/oracle_profile/test_builder_controls.py#L234) |  |
| `test_classify_all_most_restrictive` | test | `test_classify_all_most_restrictive` | [tests/oracle_profile/test_builder_controls.py:152](../../tests/oracle_profile/test_builder_controls.py#L152) |  |
| `test_classify_every_class` | test | `test_classify_every_class` | [tests/hws/test_a_classify.py:163](../../tests/hws/test_a_classify.py#L163) |  |
| `test_classify_exception` | test | `test_classify_exception` | [tests/c1prime/test_a_exceptions.py:130](../../tests/c1prime/test_a_exceptions.py#L130) |  |
| `test_classify_hits_defaults_use_contract_fragments` | test | `test_classify_hits_defaults_use_contract_fragments` | [tests/hwsb/test_b_records.py:232](../../tests/hwsb/test_b_records.py#L232) |  |
| `test_classify_hits_with_hws_lists_equals_hws_driver` | test | `test_classify_hits_with_hws_lists_equals_hws_driver` | [tests/hwsb/test_b_records.py:225](../../tests/hwsb/test_b_records.py#L225) |  |
| `test_classify_nan_bound_is_technical` | test | `test_classify_nan_bound_is_technical` | [tests/hws/test_a_classify.py:185](../../tests/hws/test_a_classify.py#L185) |  |
| `test_classify_not_scanned_only_with_inventory_reason` | test | `test_classify_not_scanned_only_with_inventory_reason` | [tests/k4b/test_b_registry.py:94](../../tests/k4b/test_b_registry.py#L94) |  |
| `test_classify_random_looks_match_the_protocol` | test | `test_classify_random_looks_match_the_protocol` | [tests/hws/test_a_classify.py:172](../../tests/hws/test_a_classify.py#L172) |  |
| `test_classify_seed_hits_declarations_pass` | test | `test_classify_seed_hits_declarations_pass` | [tests/hws/test_b_kc1.py:330](../../tests/hws/test_b_kc1.py#L330) |  |
| `test_classify_seed_hits_fails_closed_outside` | test | `test_classify_seed_hits_fails_closed_outside` | [tests/hws/test_b_kc1.py:336](../../tests/hws/test_b_kc1.py#L336) |  |
| `test_claude_release_refused_when_runtime_not_claude_active` | test | `test_claude_release_refused_when_runtime_not_claude_active` | [tests/circle_history/test_builder_v25.py:125](../../tests/circle_history/test_builder_v25.py#L125) |  |
| `test_claude_release_refuses_bad_binding` | test | `test_claude_release_refuses_bad_binding` | [tests/circle_history/test_builder_v25.py:114](../../tests/circle_history/test_builder_v25.py#L114) |  |
| `test_claude_release_verifies` | test | `test_claude_release_verifies` | [tests/circle_history/test_builder_v25.py:73](../../tests/circle_history/test_builder_v25.py#L73) |  |
| `test_claude_usage_malformed_is_stop` | test | `test_claude_usage_malformed_is_stop` | [tests/experiment/test_x5g1t_runtime.py:141](../../tests/experiment/test_x5g1t_runtime.py#L141) |  |
| `test_claude_usage_unavailable_is_no_hold` | test | `test_claude_usage_unavailable_is_no_hold` | [tests/experiment/test_x5g1t_runtime.py:135](../../tests/experiment/test_x5g1t_runtime.py#L135) |  |
| `test_cleared_kind_but_new_relevant_limit_blocks` | test | `test_cleared_kind_but_new_relevant_limit_blocks` | [tests/experiment/test_x5g1t_usage.py:349](../../tests/experiment/test_x5g1t_usage.py#L349) |  |
| `test_cli_resume_marker_and_batch_precheck` | test | `test_cli_resume_marker_and_batch_precheck` | [tests/x6_stage1/test_b_train_chain.py:363](../../tests/x6_stage1/test_b_train_chain.py#L363) |  |
| `test_closed_cocycle_is_centered_exact` | test | `test_closed_cocycle_is_centered_exact` | [tests/circle_history/test_cochain_lift.py:167](../../tests/circle_history/test_cochain_lift.py#L167) |  |
| `test_closed_form_agrees_with_the_direct_donor_filter_within_t_plus_t2` | test | `test_closed_form_agrees_with_the_direct_donor_filter_within_t_plus_t2` | [tests/c1prime/test_a_oracle.py:191](../../tests/c1prime/test_a_oracle.py#L191) |  |
| `test_closed_form_index_convention_on_a_nonsymmetric_posterior` | test | `test_closed_form_index_convention_on_a_nonsymmetric_posterior` | [tests/c1prime/test_a_oracle.py:177](../../tests/c1prime/test_a_oracle.py#L177) |  |
| `test_closed_form_tolerance_values_and_the_three_halves_switch` | test | `test_closed_form_tolerance_values_and_the_three_halves_switch` | [tests/c1prime/test_a_oracle.py:207](../../tests/c1prime/test_a_oracle.py#L207) |  |
| `test_cloud_prov_failures` | test | `test_cloud_prov_failures` | [tests/x6_stage1/test_b_ingest_bundle.py:237](../../tests/x6_stage1/test_b_ingest_bundle.py#L237) |  |
| `test_clusters_count_original_points_through_dedup_map` | test | `test_clusters_count_original_points_through_dedup_map` | [tests/x2a_stage0/test_x2a_stage0_ph.py:244](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L244) |  |
| `test_cm_descriptive_stream_24_arrays_shared_indices_and_undefined` | test | `test_cm_descriptive_stream_24_arrays_shared_indices_and_undefined` | [tests/c2_readout/test_a_partition.py:309](../../tests/c2_readout/test_a_partition.py#L309) |  |
| `test_cm_quantities_and_cancellation_fixture_is_routed_around` | test | `test_cm_quantities_and_cancellation_fixture_is_routed_around` | [tests/c2_readout/test_b_screens.py:276](../../tests/c2_readout/test_b_screens.py#L276) |  |
| `test_cm_replacements_F_S_C` | test | `test_cm_replacements_F_S_C` | [tests/c2_readout/test_b_screens.py:242](../../tests/c2_readout/test_b_screens.py#L242) |  |
| `test_cocycle_error_outside_the_chart_boundary_stays_technical` | test | `test_cocycle_error_outside_the_chart_boundary_stays_technical` | [tests/c1prime/test_a_chart_exceptions.py:98](../../tests/c1prime/test_a_chart_exceptions.py#L98) |  |
| `test_cocycle_to_edges_sign_centring_and_unknown_edges` | test | `test_cocycle_to_edges_sign_centring_and_unknown_edges` | [tests/circle_history/test_chart.py:148](../../tests/circle_history/test_chart.py#L148) |  |
| `test_code_missing_half_the_circle_fails` | test | `test_code_missing_half_the_circle_fails` | [tests/c2_readout/test_b_fwl_l1.py:246](../../tests/c2_readout/test_b_fwl_l1.py#L246) |  |
| `test_code_tar_is_git_archive_of_head` | test | `test_code_tar_is_git_archive_of_head` | [tests/x6_stage1/test_b_chain_ops.py:352](../../tests/x6_stage1/test_b_chain_ops.py#L352) |  |
| `test_codex_release_verifies_only_while_not_relinquished` | test | `test_codex_release_verifies_only_while_not_relinquished` | [tests/circle_history/test_builder_v25.py:131](../../tests/circle_history/test_builder_v25.py#L131) |  |
| `test_codex_release_with_claude_fields_refused` | test | `test_codex_release_with_claude_fields_refused` | [tests/circle_history/test_builder_v25.py:143](../../tests/circle_history/test_builder_v25.py#L143) |  |
| `test_cohort_verdict_accepts_tuple` | test | `test_cohort_verdict_accepts_tuple` | [tests/analysis/test_x5_endpoint_bootstrap.py:259](../../tests/analysis/test_x5_endpoint_bootstrap.py#L259) |  |
| `test_cohort_verdict_truth_table` | test | `test_cohort_verdict_truth_table` | [tests/analysis/test_x5_endpoint_bootstrap.py:253](../../tests/analysis/test_x5_endpoint_bootstrap.py#L253) |  |
| `test_collision_mass` | test | `test_collision_mass` | [tests/x6_stage1/test_b_seed_pool_reg.py:241](../../tests/x6_stage1/test_b_seed_pool_reg.py#L241) |  |
| `test_collision_with_R_is_lineage` | test | `test_collision_with_R_is_lineage` | [tests/c2_readout/test_b_registry.py:157](../../tests/c2_readout/test_b_registry.py#L157) |  |
| `test_collisions_counts` | test | `test_collisions_counts` | [tests/experiment/test_x5g1t_lineage_oracle.py:208](../../tests/experiment/test_x5g1t_lineage_oracle.py#L208) |  |
| `test_common_inverse_temperature_identity_for_log_probabilities` | test | `test_common_inverse_temperature_identity_for_log_probabilities` | [tests/c1prime/test_b_identities.py:211](../../tests/c1prime/test_b_identities.py#L211) |  |
| `test_common_inverse_temperature_scales_the_logit_form_exactly` | test | `test_common_inverse_temperature_scales_the_logit_form_exactly` | [tests/c1prime/test_b_identities.py:123](../../tests/c1prime/test_b_identities.py#L123) |  |
| `test_compare_panel_excludes_failed_baselines_and_counts_them` | test | `test_compare_panel_excludes_failed_baselines_and_counts_them` | [tests/experiment/test_circ_audit.py:23](../../tests/experiment/test_circ_audit.py#L23) |  |
| `test_compare_panel_fails_below_bound_or_baseline` | test | `test_compare_panel_fails_below_bound_or_baseline` | [tests/experiment/test_circ_audit.py:30](../../tests/experiment/test_circ_audit.py#L30) |  |
| `test_completed_exports_are_not_overwritten` | test | `test_completed_exports_are_not_overwritten` | [tests/experiment/test_x4f_maintenance.py:50](../../tests/experiment/test_x4f_maintenance.py#L50) |  |
| `test_components_follow_edge_list_rule` | test | `test_components_follow_edge_list_rule` | [tests/chart_diag/test_chart_diag.py:29](../../tests/chart_diag/test_chart_diag.py#L29) |  |
| `test_components_partition_and_sizes` | test | `test_components_partition_and_sizes` | [tests/c1prime/test_a_chart.py:196](../../tests/c1prime/test_a_chart.py#L196) |  |
| `test_concurrent_wave_is_refused_before_launch` | test | `test_concurrent_wave_is_refused_before_launch` | [tests/d2a/test_process_tree_repair.py:123](../../tests/d2a/test_process_tree_repair.py#L123) |  |
| `test_conditional_residual_vanishes_given_each_suffix` | test | `test_conditional_residual_vanishes_given_each_suffix` | [tests/k4b/test_a_prop1.py:132](../../tests/k4b/test_a_prop1.py#L132) |  |
| `test_conditioning_above_1e8_with_a_well_conditioned_fwl_design` | test | `test_conditioning_above_1e8_with_a_well_conditioned_fwl_design` | [tests/c2_readout/test_a_readout.py:377](../../tests/c2_readout/test_a_readout.py#L377) |  |
| `test_conditioning_failure_at_full_rank` | test | `test_conditioning_failure_at_full_rank` | [tests/c2_readout/test_b_fwl_l1.py:110](../../tests/c2_readout/test_b_fwl_l1.py#L110) |  |
| `test_conditioning_on_support_is_spurious_but_bounds_hold` | test | `test_conditioning_on_support_is_spurious_but_bounds_hold` | [tests/k4b/test_a_theorem_a.py:221](../../tests/k4b/test_a_theorem_a.py#L221) | u = e1 on S' (a suffix-only field). Delta4(e1) = 0 exactly (Proposition 1), yet the |
| `test_conductance_config_defaults` | test | `test_conductance_config_defaults` | [tests/process/test_conductance.py:113](../../tests/process/test_conductance.py#L113) |  |
| `test_conflicting_duplicate_landmarks_in_extension_are_technical` | test | `test_conflicting_duplicate_landmarks_in_extension_are_technical` | [tests/c1prime/test_a_chart_exceptions.py:200](../../tests/c1prime/test_a_chart_exceptions.py#L200) |  |
| `test_connected_circle_has_full_giant` | test | `test_connected_circle_has_full_giant` | [tests/chart_diag/test_chart_diag.py:46](../../tests/chart_diag/test_chart_diag.py#L46) |  |
| `test_connected_graph_equals_fit_chart_bitwise` | test | `test_connected_graph_equals_fit_chart_bitwise` | [tests/c1prime/test_a_chart.py:172](../../tests/c1prime/test_a_chart.py#L172) | Item 1: m = n, so steps 1-9 are fit_chart's operations; only info gains keys. |
| `test_constant_emissions_factorize_and_have_no_gap` | test | `test_constant_emissions_factorize_and_have_no_gap` | [tests/analysis/test_horizon.py:50](../../tests/analysis/test_horizon.py#L50) |  |
| `test_constant_field_is_zero` | test | `test_constant_field_is_zero` | [tests/k4b/test_a_prop1.py:153](../../tests/k4b/test_a_prop1.py#L153) |  |
| `test_constant_target_zero_variance` | test | `test_constant_target_zero_variance` | [tests/analysis/test_x4f_erasure.py:261](../../tests/analysis/test_x4f_erasure.py#L261) |  |
| `test_constants` | test | `test_constants` | [tests/analysis/test_x5_endpoint.py:68](../../tests/analysis/test_x5_endpoint.py#L68) |  |
| `test_constants` | test | `test_constants` | [tests/d1_seam/test_d1_seam.py:161](../../tests/d1_seam/test_d1_seam.py#L161) |  |
| `test_constants` | test | `test_constants` | [tests/d2a/test_a_world.py:58](../../tests/d2a/test_a_world.py#L58) |  |
| `test_constants` | test | `test_constants` | [tests/experiment/test_x5g1t_usage.py:68](../../tests/experiment/test_x5g1t_usage.py#L68) |  |
| `test_constants` | test | `test_constants` | [tests/hwsb/test_a_capture.py:140](../../tests/hwsb/test_a_capture.py#L140) |  |
| `test_constants_and_index_helpers` | test | `test_constants_and_index_helpers` | [tests/x2a_stage0/test_x2a_stage0.py:113](../../tests/x2a_stage0/test_x2a_stage0.py#L113) |  |
| `test_constants_frozen` | test | `test_constants_frozen` | [tests/experiment/test_x5g1t_lineage_oracle.py:49](../../tests/experiment/test_x5g1t_lineage_oracle.py#L49) |  |
| `test_constants_match_contract` | test | `test_constants_match_contract` | [tests/k4b/test_b_data.py:69](../../tests/k4b/test_b_data.py#L69) |  |
| `test_constructed_factorization_is_detected` | test | `test_constructed_factorization_is_detected` | [tests/analysis/test_horizon.py:71](../../tests/analysis/test_horizon.py#L71) |  |
| `test_context_none_is_inconclusive` | test | `test_context_none_is_inconclusive` | [tests/analysis/test_x5_context.py:135](../../tests/analysis/test_x5_context.py#L135) |  |
| `test_continue` | test | `test_continue` | [tests/oracle_profile/test_builder_controls.py:52](../../tests/oracle_profile/test_builder_controls.py#L52) |  |
| `test_continuity_path_exact_affine_family` | test | `test_continuity_path_exact_affine_family` | [tests/k4b/test_a_theorem_a.py:180](../../tests/k4b/test_a_theorem_a.py#L180) |  |
| `test_continuity_path_unit_rotation_float` | test | `test_continuity_path_unit_rotation_float` | [tests/k4b/test_a_theorem_a.py:196](../../tests/k4b/test_a_theorem_a.py#L196) | u~_theta = R_theta(-r/\|r\|): E[u~ . r] = E[X- 1_S] - cos(theta) E[\|r\| 1_{S^c}]. |
| `test_contract_chart_keys_match_job_values` | test | `test_contract_chart_keys_match_job_values` | [tests/circle_history/test_cochain.py:66](../../tests/circle_history/test_cochain.py#L66) |  |
| `test_contract_hold_numbers` | test | `test_contract_hold_numbers` | [tests/hwsb/test_b_hold.py:32](../../tests/hwsb/test_b_hold.py#L32) |  |
| `test_contract_inventory_lists_every_section_18_directory` | test | `test_contract_inventory_lists_every_section_18_directory` | [tests/c2_readout/test_b_registry.py:328](../../tests/c2_readout/test_b_registry.py#L328) |  |
| `test_contract_meta_passes_and_check_is_pure` | test | `test_contract_meta_passes_and_check_is_pure` | [tests/k4b/test_b_h1_meta.py:137](../../tests/k4b/test_b_h1_meta.py#L137) |  |
| `test_contraction_identity_and_the_wrong_conversion_differs` | test | `test_contraction_identity_and_the_wrong_conversion_differs` | [tests/c2_readout/test_a_readout.py:197](../../tests/c2_readout/test_a_readout.py#L197) |  |
| `test_contrast_error_exactly_one_half_is_reproduced` | test | `test_contrast_error_exactly_one_half_is_reproduced` | [tests/d2a/test_b_behaviour.py:56](../../tests/d2a/test_b_behaviour.py#L56) |  |
| `test_contrast_error_just_above_one_half_is_not_reproduced` | test | `test_contrast_error_just_above_one_half_is_not_reproduced` | [tests/d2a/test_b_behaviour.py:63](../../tests/d2a/test_b_behaviour.py#L63) |  |
| `test_contrasts_known_answer` | test | `test_contrasts_known_answer` | [tests/analysis/test_f1_rule.py:25](../../tests/analysis/test_f1_rule.py#L25) |  |
| `test_contrasts_missing_key_is_invalid_config` | test | `test_contrasts_missing_key_is_invalid_config` | [tests/analysis/test_f1_rule.py:41](../../tests/analysis/test_f1_rule.py#L41) |  |
| `test_contrasts_ordered_by_sorted_panel_ids` | test | `test_contrasts_ordered_by_sorted_panel_ids` | [tests/analysis/test_f1_rule.py:34](../../tests/analysis/test_f1_rule.py#L34) |  |
| `test_control_arrays_names_entries_shapes_and_values` | test | `test_control_arrays_names_entries_shapes_and_values` | [tests/k4b/test_b_endpoint.py:194](../../tests/k4b/test_b_endpoint.py#L194) |  |
| `test_control_displacement_isometry_and_the_same_frame_on_both_arms` | test | `test_control_displacement_isometry_and_the_same_frame_on_both_arms` | [tests/c1prime/test_b_frames.py:114](../../tests/c1prime/test_b_frames.py#L114) |  |
| `test_control_L1_label_leak` | test | `test_control_L1_label_leak` | [tests/d1_seam/test_d1_seam.py:379](../../tests/d1_seam/test_d1_seam.py#L379) |  |
| `test_control_L2_narrow_interior` | test | `test_control_L2_narrow_interior` | [tests/d1_seam/test_d1_seam.py:384](../../tests/d1_seam/test_d1_seam.py#L384) |  |
| `test_control_N3_symmetric_start` | test | `test_control_N3_symmetric_start` | [tests/d1_seam/test_d1_seam.py:373](../../tests/d1_seam/test_d1_seam.py#L373) |  |
| `test_control_scores_equal_unit_dot_residual` | test | `test_control_scores_equal_unit_dot_residual` | [tests/circle_history/test_controls.py:45](../../tests/circle_history/test_controls.py#L45) |  |
| `test_control_summary_fail_closed` | test | `test_control_summary_fail_closed` | [tests/circle_history/test_controls.py:140](../../tests/circle_history/test_controls.py#L140) |  |
| `test_control_summary_reproduces_shared_index_stream` | test | `test_control_summary_reproduces_shared_index_stream` | [tests/circle_history/test_controls.py:91](../../tests/circle_history/test_controls.py#L91) |  |
| `test_control_vectors_tiny_and_subnormal_vectors` | test | `test_control_vectors_tiny_and_subnormal_vectors` | [tests/circle_history/test_scores_precision.py:312](../../tests/circle_history/test_scores_precision.py#L312) |  |
| `test_control_vectors_zero_maps_to_unit_x_and_others_unit_norm` | test | `test_control_vectors_zero_maps_to_unit_x_and_others_unit_norm` | [tests/circle_history/test_scores_precision.py:276](../../tests/circle_history/test_scores_precision.py#L276) |  |
| `test_controls_N1_N2_null` | test | `test_controls_N1_N2_null` | [tests/d1_seam/test_d1_seam.py:367](../../tests/d1_seam/test_d1_seam.py#L367) |  |
| `test_controlstate_is_namedtuple` | test | `test_controlstate_is_namedtuple` | [tests/experiment/test_x5g1t_runtime.py:50](../../tests/experiment/test_x5g1t_runtime.py#L50) |  |
| `test_cord_draws_replays_registered_scheme_and_common_indices` | test | `test_cord_draws_replays_registered_scheme_and_common_indices` | [tests/x6_stage1/test_a_numerics.py:271](../../tests/x6_stage1/test_a_numerics.py#L271) |  |
| `test_cord_rule` | test | `test_cord_rule` | [tests/x6_stage1/test_a_rules.py:72](../../tests/x6_stage1/test_a_rules.py#L72) |  |
| `test_corrupt_ledger_raises_and_keeps_bytes` | test | `test_corrupt_ledger_raises_and_keeps_bytes` | [tests/experiment/test_x5g1_safety.py:392](../../tests/experiment/test_x5g1_safety.py#L392) |  |
| `test_corrupt_ledger_raises_and_keeps_bytes` | test | `test_corrupt_ledger_raises_and_keeps_bytes` | [tests/experiment/test_x5g1t_runtime_boundary.py:367](../../tests/experiment/test_x5g1t_runtime_boundary.py#L367) |  |
| `test_criteria_equality_passes` | test | `test_criteria_equality_passes` | [tests/hws/test_a_classify.py:128](../../tests/hws/test_a_classify.py#L128) |  |
| `test_cross_model_G_identity_within_1e_12` | test | `test_cross_model_G_identity_within_1e_12` | [tests/c1prime/test_a_oracle_named.py:137](../../tests/c1prime/test_a_oracle_named.py#L137) |  |
| `test_cross_model_join_mismatch_raises_join_error` | test | `test_cross_model_join_mismatch_raises_join_error` | [tests/circle_history/test_adapter.py:345](../../tests/circle_history/test_adapter.py#L345) |  |
| `test_cross_model_join_orders_by_sequence_id` | test | `test_cross_model_join_orders_by_sequence_id` | [tests/circle_history/test_adapter.py:312](../../tests/circle_history/test_adapter.py#L312) |  |
| `test_cross_split_collision_and_seq_id_overlap_are_lineage` | test | `test_cross_split_collision_and_seq_id_overlap_are_lineage` | [tests/c2_readout/test_b_registry.py:174](../../tests/c2_readout/test_b_registry.py#L174) |  |
| `test_ctrl_max_is_taken_inside_each_draw` | test | `test_ctrl_max_is_taken_inside_each_draw` | [tests/x6_stage1/test_a_numerics.py:288](../../tests/x6_stage1/test_a_numerics.py#L288) |  |
| `test_cue_mass_and_cue_normalise` | test | `test_cue_mass_and_cue_normalise` | [tests/x6_stage1/test_a_eval.py:162](../../tests/x6_stage1/test_a_eval.py#L162) |  |
| `test_cumulative_accumulates_and_is_never_reset` | test | `test_cumulative_accumulates_and_is_never_reset` | [tests/experiment/test_x5g1_controls.py:105](../../tests/experiment/test_x5g1_controls.py#L105) |  |
| `test_cumulative_cap_exceeded` | test | `test_cumulative_cap_exceeded` | [tests/experiment/test_x5g1_controls.py:130](../../tests/experiment/test_x5g1_controls.py#L130) |  |
| `test_cumulative_thresholds_of_the_protocol_table` | test | `test_cumulative_thresholds_of_the_protocol_table` | [tests/hws/test_a_budget.py:99](../../tests/hws/test_a_budget.py#L99) |  |
| `test_custom_cap_steps_and_from_step` | test | `test_custom_cap_steps_and_from_step` | [tests/hwsb/test_b_hold.py:65](../../tests/hwsb/test_b_hold.py#L65) |  |
| `test_custom_threshold` | test | `test_custom_threshold` | [tests/experiment/test_x5g1t_usage.py:123](../../tests/experiment/test_x5g1t_usage.py#L123) |  |
| `test_d0127_1_numeric_needles_match_whole_tokens` | test | `test_d0127_1_numeric_needles_match_whole_tokens` | [tests/hws/test_b_kc1.py:363](../../tests/hws/test_b_kc1.py#L363) |  |
| `test_D01_deterministic_cycle_known_answer` | test | `test_D01_deterministic_cycle_known_answer` | [tests/dataset/test_sampler.py:12](../../tests/dataset/test_sampler.py#L12) |  |
| `test_D02_empirical_frequencies_match_T_E_pi` | test | `test_D02_empirical_frequencies_match_T_E_pi` | [tests/dataset/test_sampler.py:25](../../tests/dataset/test_sampler.py#L25) |  |
| `test_D03_emission_before_transition` | test | `test_D03_emission_before_transition` | [tests/dataset/test_sampler.py:45](../../tests/dataset/test_sampler.py#L45) |  |
| `test_D04_disjoint_ids_test_shared_across_replicates_train_differs` | test | `test_D04_disjoint_ids_test_shared_across_replicates_train_differs` | [tests/dataset/test_stage.py:26](../../tests/dataset/test_stage.py#L26) |  |
| `test_D05_panels_disjoint_distinct_and_reproducible` | test | `test_D05_panels_disjoint_distinct_and_reproducible` | [tests/dataset/test_panels.py:30](../../tests/dataset/test_panels.py#L30) |  |
| `test_D06_observation_set_has_no_latent_field_and_sidecar_is_rejected` | test | `test_D06_observation_set_has_no_latent_field_and_sidecar_is_rejected` | [tests/dataset/test_public.py:20](../../tests/dataset/test_public.py#L20) |  |
| `test_D07_inputs_and_targets_via_layout` | test | `test_D07_inputs_and_targets_via_layout` | [tests/dataset/test_public.py:43](../../tests/dataset/test_public.py#L43) |  |
| `test_D08_no_train_sidecar_persisted` | test | `test_D08_no_train_sidecar_persisted` | [tests/dataset/test_stage.py:70](../../tests/dataset/test_stage.py#L70) |  |
| `test_D09_biased_sampler_caught_by_first_token_chi2` | test | `test_D09_biased_sampler_caught_by_first_token_chi2` | [tests/dataset/test_stage.py:80](../../tests/dataset/test_stage.py#L80) |  |
| `test_d4_rows_equal_k4b_delta4_orc` | test | `test_d4_rows_equal_k4b_delta4_orc` | [tests/hwsb/test_a_endpoints.py:180](../../tests/hwsb/test_a_endpoints.py#L180) |  |
| `test_d_named_scatters_canonical_into_named_order` | test | `test_d_named_scatters_canonical_into_named_order` | [tests/c2_readout/test_a_readout.py:191](../../tests/c2_readout/test_a_readout.py#L191) |  |
| `test_D_w_counts_both_arms_over_2n` | test | `test_D_w_counts_both_arms_over_2n` | [tests/c1prime/test_b_gates.py:41](../../tests/c1prime/test_b_gates.py#L41) |  |
| `test_D_y_and_leakage` | test | `test_D_y_and_leakage` | [tests/c1prime/test_b_gates.py:50](../../tests/c1prime/test_b_gates.py#L50) |  |
| `test_data_generator_refusals` | test | `test_data_generator_refusals` | [tests/hwsb/test_b_streams.py:88](../../tests/hwsb/test_b_streams.py#L88) |  |
| `test_data_id_failures` | test | `test_data_id_failures` | [tests/x6_stage1/test_b_ingest_bundle.py:264](../../tests/x6_stage1/test_b_ingest_bundle.py#L264) |  |
| `test_data_streams_distinct_and_scoped` | test | `test_data_streams_distinct_and_scoped` | [tests/x6_stage1/test_b_seed_pool_reg.py:69](../../tests/x6_stage1/test_b_seed_pool_reg.py#L69) |  |
| `test_dctx_dsolve_dinverse_against_exact_rationals` | test | `test_dctx_dsolve_dinverse_against_exact_rationals` | [tests/c2_readout/test_a_gls.py:330](../../tests/c2_readout/test_a_gls.py#L330) |  |
| `test_decide_not_run_after_first_validity_failure` | test | `test_decide_not_run_after_first_validity_failure` | [tests/x6_stage1/test_a_rules.py:270](../../tests/x6_stage1/test_a_rules.py#L270) |  |
| `test_decide_ordered_rules` | test | `test_decide_ordered_rules` | [tests/x6_stage1/test_a_rules.py:265](../../tests/x6_stage1/test_a_rules.py#L265) |  |
| `test_decimal_check_catches_planted_narrow_enclosure` | test | `test_decimal_check_catches_planted_narrow_enclosure` | [tests/hwsb/test_a_enclosure_proof.py:307](../../tests/hwsb/test_a_enclosure_proof.py#L307) |  |
| `test_decimal_check_passes_on_true_enclosure` | test | `test_decimal_check_passes_on_true_enclosure` | [tests/hwsb/test_a_enclosure_proof.py:297](../../tests/hwsb/test_a_enclosure_proof.py#L297) |  |
| `test_decimal_circular_mean_matches_exact_mean` | test | `test_decimal_circular_mean_matches_exact_mean` | [tests/oracle_profile/test_oracle_profile.py:209](../../tests/oracle_profile/test_oracle_profile.py#L209) | Item 12: decimal circular mean vs the exact Fraction mean of the enumerated posterior. |
| `test_decimal_cos_sin_against_exact_rational_taylor` | test | `test_decimal_cos_sin_against_exact_rational_taylor` | [tests/circle_history/test_error_bound.py:194](../../tests/circle_history/test_error_bound.py#L194) |  |
| `test_decimal_cos_sin_rejects_outside_analytic_interval` | test | `test_decimal_cos_sin_rejects_outside_analytic_interval` | [tests/circle_history/test_error_bound.py:210](../../tests/circle_history/test_error_bound.py#L210) |  |
| `test_decimal_posterior60_matches_the_exact_posterior` | test | `test_decimal_posterior60_matches_the_exact_posterior` | [tests/c1prime/test_a_oracle_named.py:228](../../tests/c1prime/test_a_oracle_named.py#L228) |  |
| `test_decimal_precision_context_is_honoured` | test | `test_decimal_precision_context_is_honoured` | [tests/oracle_profile/test_oracle_profile.py:193](../../tests/oracle_profile/test_oracle_profile.py#L193) | Item 12: >= 60 significant digits are carried; a lower request is refused. |
| `test_decimal_predictive_is_b_T_E` | test | `test_decimal_predictive_is_b_T_E` | [tests/c1prime/test_a_oracle_named.py:217](../../tests/c1prime/test_a_oracle_named.py#L217) |  |
| `test_decimal_reference_against_exact_rationals` | test | `test_decimal_reference_against_exact_rationals` | [tests/c1prime/test_a_oracle_named.py:199](../../tests/c1prime/test_a_oracle_named.py#L199) |  |
| `test_decimal_reference_matches_enumeration` | test | `test_decimal_reference_matches_enumeration` | [tests/oracle_profile/test_oracle_profile.py:175](../../tests/oracle_profile/test_oracle_profile.py#L175) | Items 1 and 12: decimal forward summation vs exact path enumeration on every suffix. |
| `test_decimal_spot_check_is_w12_only` | test | `test_decimal_spot_check_is_w12_only` | [tests/hws/test_b_exact.py:182](../../tests/hws/test_b_exact.py#L182) |  |
| `test_decimal_spot_check_passes_and_detects_a_perturbed_e` | test | `test_decimal_spot_check_passes_and_detects_a_perturbed_e` | [tests/hws/test_b_exact.py:170](../../tests/hws/test_b_exact.py#L170) |  |
| `test_decimal_trap` | test | `test_decimal_trap` | [tests/d1_seam/test_d1_seam.py:352](../../tests/d1_seam/test_d1_seam.py#L352) |  |
| `test_decimal_trap_in_m_ln_is_fail_technical_numerical` | test | `test_decimal_trap_in_m_ln_is_fail_technical_numerical` | [tests/c1prime/test_b_cert_oracle.py:307](../../tests/c1prime/test_b_cert_oracle.py#L307) |  |
| `test_decision_has_reasons_and_table` | test | `test_decision_has_reasons_and_table` | [tests/analysis/test_sigma_calibrator.py:111](../../tests/analysis/test_sigma_calibrator.py#L111) |  |
| `test_decision_naive_or_nonstring_evidence_time_never_releases` | test | `test_decision_naive_or_nonstring_evidence_time_never_releases` | [tests/experiment/test_x5g1t_usage.py:380](../../tests/experiment/test_x5g1t_usage.py#L380) |  |
| `test_decision_rows` | test | `test_decision_rows` | [tests/d2a/test_a_world.py:155](../../tests/d2a/test_a_world.py#L155) |  |
| `test_decision_tie_rule` | test | `test_decision_tie_rule` | [tests/x2a_stage0/test_x2a_stage0_ph.py:51](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L51) |  |
| `test_decision_with_malformed_usage_raises` | test | `test_decision_with_malformed_usage_raises` | [tests/experiment/test_x5g1t_usage.py:368](../../tests/experiment/test_x5g1t_usage.py#L368) |  |
| `test_decoder_agreement_and_unavailable_form` | test | `test_decoder_agreement_and_unavailable_form` | [tests/k4b/test_b_endpoint.py:243](../../tests/k4b/test_b_endpoint.py#L243) |  |
| `test_decoder_features_layout` | test | `test_decoder_features_layout` | [tests/c2_readout/test_b_fwl_l1.py:194](../../tests/c2_readout/test_b_fwl_l1.py#L194) |  |
| `test_decoder_refit_matches_nested_ridge_and_the_section7_recipe` | test | `test_decoder_refit_matches_nested_ridge_and_the_section7_recipe` | [tests/c1prime/test_b_decoder.py:57](../../tests/c1prime/test_b_decoder.py#L57) |  |
| `test_dedicated_dirs_are_not_deep_scanned_by_the_inventory` | test | `test_dedicated_dirs_are_not_deep_scanned_by_the_inventory` | [tests/k4b/test_b_registry_rules.py:354](../../tests/k4b/test_b_registry_rules.py#L354) |  |
| `test_default_legacy_is_the_original_meter_limit_reason` | test | `test_default_legacy_is_the_original_meter_limit_reason` | [tests/k4b/test_b_meter.py:248](../../tests/k4b/test_b_meter.py#L248) |  |
| `test_default_trainer_matches_golden` | test | `test_default_trainer_matches_golden` | [tests/learner/test_trainer_golden.py:94](../../tests/learner/test_trainer_golden.py#L94) |  |
| `test_degenerate_B_singular_values` | test | `test_degenerate_B_singular_values` | [tests/c2_readout/test_b_fwl_l1.py:119](../../tests/c2_readout/test_b_fwl_l1.py#L119) |  |
| `test_degenerate_bandwidth_is_rbf_degenerate` | test | `test_degenerate_bandwidth_is_rbf_degenerate` | [tests/c1prime/test_b_decoder.py:72](../../tests/c1prime/test_b_decoder.py#L72) |  |
| `test_degenerate_whitening_propagates` | test | `test_degenerate_whitening_propagates` | [tests/analysis/test_x4f_erasure.py:285](../../tests/analysis/test_x4f_erasure.py#L285) |  |
| `test_delta_belief_gives_unit_vector_at_state_angle` | test | `test_delta_belief_gives_unit_vector_at_state_angle` | [tests/analysis/test_x4f_targets.py:24](../../tests/analysis/test_x4f_targets.py#L24) |  |
| `test_delta_geom_known_answer_six_pairs` | test | `test_delta_geom_known_answer_six_pairs` | [tests/analysis/test_geometry.py:29](../../tests/analysis/test_geometry.py#L29) |  |
| `test_delta_geom_positive_for_planted_and_negative_when_swapped` | test | `test_delta_geom_positive_for_planted_and_negative_when_swapped` | [tests/analysis/test_geometry.py:37](../../tests/analysis/test_geometry.py#L37) |  |
| `test_derived_registry_records_are_listed_with_sha256` | test | `test_derived_registry_records_are_listed_with_sha256` | [tests/k4b/test_b_store_reader.py:144](../../tests/k4b/test_b_store_reader.py#L144) |  |
| `test_design_and_whitened_ranks` | test | `test_design_and_whitened_ranks` | [tests/c2_readout/test_b_fwl_l1.py:80](../../tests/c2_readout/test_b_fwl_l1.py#L80) |  |
| `test_designed_arrays_and_digest` | test | `test_designed_arrays_and_digest` | [tests/x6_stage1/test_a_designed.py:238](../../tests/x6_stage1/test_a_designed.py#L238) |  |
| `test_designed_history_composition` | test | `test_designed_history_composition` | [tests/x6_stage1/test_a_designed.py:108](../../tests/x6_stage1/test_a_designed.py#L108) |  |
| `test_designed_set_structure` | test | `test_designed_set_structure` | [tests/x6_stage1/test_a_designed.py:213](../../tests/x6_stage1/test_a_designed.py#L213) |  |
| `test_designed_stats_oracle_and_heuristic_references` | test | `test_designed_stats_oracle_and_heuristic_references` | [tests/x6_stage1/test_a_designed.py:258](../../tests/x6_stage1/test_a_designed.py#L258) |  |
| `test_determinism` | test | `test_determinism` | [tests/experiment/test_x4f_probe.py:150](../../tests/experiment/test_x4f_probe.py#L150) |  |
| `test_determinism_any_bitwise_difference_fails` | test | `test_determinism_any_bitwise_difference_fails` | [tests/k4b/test_b_charts.py:382](../../tests/k4b/test_b_charts.py#L382) |  |
| `test_determinism_identical_passes` | test | `test_determinism_identical_passes` | [tests/k4b/test_b_charts.py:374](../../tests/k4b/test_b_charts.py#L374) |  |
| `test_dev_analysis_calls_batch_and_oracle_guards` | test | `test_dev_analysis_calls_batch_and_oracle_guards` | [tests/experiment/test_x5g1t_integration.py:308](../../tests/experiment/test_x5g1t_integration.py#L308) |  |
| `test_dev_analysis_control_reaches_oracle` | test | `test_dev_analysis_control_reaches_oracle` | [tests/experiment/test_x5g1t_identity_eval.py:198](../../tests/experiment/test_x5g1t_identity_eval.py#L198) |  |
| `test_dev_analysis_mismatched_pool_never_scores` | test | `test_dev_analysis_mismatched_pool_never_scores` | [tests/experiment/test_x5g1t_identity_eval.py:217](../../tests/experiment/test_x5g1t_identity_eval.py#L217) |  |
| `test_dev_auc_on_study_grid` | test | `test_dev_auc_on_study_grid` | [tests/analysis/test_x5_endpoint.py:357](../../tests/analysis/test_x5_endpoint.py#L357) |  |
| `test_dev_auc_uneven_grid` | test | `test_dev_auc_uneven_grid` | [tests/analysis/test_x5_endpoint.py:351](../../tests/analysis/test_x5_endpoint.py#L351) |  |
| `test_diagnostics_values` | test | `test_diagnostics_values` | [tests/process/test_overlap.py:79](../../tests/process/test_overlap.py#L79) |  |
| `test_differing_e_canon_is_identity_failure` | test | `test_differing_e_canon_is_identity_failure` | [tests/hwsb/test_b_process.py:157](../../tests/hwsb/test_b_process.py#L157) |  |
| `test_digest_set_runs_full_confirmation_and_hash` | test | `test_digest_set_runs_full_confirmation_and_hash` | [tests/x6_stage1/test_b_seed_pool_reg.py:229](../../tests/x6_stage1/test_b_seed_pool_reg.py#L229) |  |
| `test_digests_are_sha256_of_uint8_rows` | test | `test_digests_are_sha256_of_uint8_rows` | [tests/k4b/test_b_data.py:172](../../tests/k4b/test_b_data.py#L172) |  |
| `test_digits_other_than_60_is_refused` | test | `test_digits_other_than_60_is_refused` | [tests/hwsb/test_b_meter_law.py:348](../../tests/hwsb/test_b_meter_law.py#L348) |  |
| `test_digits_other_than_60_raise_invalid` | test | `test_digits_other_than_60_raise_invalid` | [tests/hwsb/test_a_enclosure_proof.py:280](../../tests/hwsb/test_a_enclosure_proof.py#L280) |  |
| `test_dir_size` | test | `test_dir_size` | [tests/experiment/test_x5g1t_runtime_boundary.py:201](../../tests/experiment/test_x5g1t_runtime_boundary.py#L201) |  |
| `test_dirty_source_refused_before_io` | test | `test_dirty_source_refused_before_io` | [tests/circle_history/test_builder_guards.py:156](../../tests/circle_history/test_builder_guards.py#L156) |  |
| `test_discover_broken_interior_link` | test | `test_discover_broken_interior_link` | [tests/x6_stage1/test_b_chain_ops.py:118](../../tests/x6_stage1/test_b_chain_ops.py#L118) |  |
| `test_discover_full_chain_and_prefix` | test | `test_discover_full_chain_and_prefix` | [tests/x6_stage1/test_b_chain_ops.py:78](../../tests/x6_stage1/test_b_chain_ops.py#L78) |  |
| `test_discover_lists_nonterminal_orphans` | test | `test_discover_lists_nonterminal_orphans` | [tests/x6_stage1/test_b_chain_ops.py:97](../../tests/x6_stage1/test_b_chain_ops.py#L97) |  |
| `test_discover_read_failure_is_hold_then_stable_reread` | test | `test_discover_read_failure_is_hold_then_stable_reread` | [tests/x6_stage1/test_b_chain_ops.py:126](../../tests/x6_stage1/test_b_chain_ops.py#L126) |  |
| `test_disjoint_across_splits_arms_masters` | test | `test_disjoint_across_splits_arms_masters` | [tests/experiment/test_x5g1t_lineage_oracle.py:198](../../tests/experiment/test_x5g1t_lineage_oracle.py#L198) |  |
| `test_disk_floors` | test | `test_disk_floors` | [tests/x6_stage1/test_b_seed_pool_reg.py:396](../../tests/x6_stage1/test_b_seed_pool_reg.py#L396) |  |
| `test_disk_minima_registered` | test | `test_disk_minima_registered` | [tests/k4b/test_b_meter.py:271](../../tests/k4b/test_b_meter.py#L271) |  |
| `test_disk_reason` | test | `test_disk_reason` | [tests/d2a/test_b_resource.py:321](../../tests/d2a/test_b_resource.py#L321) |  |
| `test_disk_reason_below_minimum` | test | `test_disk_reason_below_minimum` | [tests/k4b/test_b_meter.py:281](../../tests/k4b/test_b_meter.py#L281) |  |
| `test_disk_reason_none_at_or_above_minimum` | test | `test_disk_reason_none_at_or_above_minimum` | [tests/k4b/test_b_meter.py:275](../../tests/k4b/test_b_meter.py#L275) |  |
| `test_disk_reason_unreadable_free_space` | test | `test_disk_reason_unreadable_free_space` | [tests/k4b/test_b_meter.py:289](../../tests/k4b/test_b_meter.py#L289) |  |
| `test_disk_safe_stop_fails_closed_on_unreadable_drive` | test | `test_disk_safe_stop_fails_closed_on_unreadable_drive` | [tests/c1prime/test_a_release_meter.py:232](../../tests/c1prime/test_a_release_meter.py#L232) |  |
| `test_disk_safe_stop_reason` | test | `test_disk_safe_stop_reason` | [tests/circle_history/test_builder_v24_runtime.py:80](../../tests/circle_history/test_builder_v24_runtime.py#L80) |  |
| `test_disk_safe_stop_thresholds` | test | `test_disk_safe_stop_thresholds` | [tests/c1prime/test_a_release_meter.py:225](../../tests/c1prime/test_a_release_meter.py#L225) |  |
| `test_displacements_known_answer` | test | `test_displacements_known_answer` | [tests/analysis/test_x4f_erasure.py:149](../../tests/analysis/test_x4f_erasure.py#L149) |  |
| `test_documented_transition_degrees_wrap_and_identities` | test | `test_documented_transition_degrees_wrap_and_identities` | [tests/circle_history/test_process_law.py:173](../../tests/circle_history/test_process_law.py#L173) |  |
| `test_donors_shift_w1_to_w31_and_keep_w32` | test | `test_donors_shift_w1_to_w31_and_keep_w32` | [tests/c1prime/test_a_oracle.py:112](../../tests/c1prime/test_a_oracle.py#L112) |  |
| `test_dr11_alignment_traps_are_detected` | test | `test_dr11_alignment_traps_are_detected` | [tests/hws/test_b_oracle.py:229](../../tests/hws/test_b_oracle.py#L229) |  |
| `test_dr3_forced_unanchored_world_has_zero_moments` | test | `test_dr3_forced_unanchored_world_has_zero_moments` | [tests/hws/test_b_oracle.py:254](../../tests/hws/test_b_oracle.py#L254) |  |
| `test_dr8_formula_bridge_at_w12` | test | `test_dr8_formula_bridge_at_w12` | [tests/hws/test_b_oracle.py:179](../../tests/hws/test_b_oracle.py#L179) |  |
| `test_draw_pair_first_symbol_identical_across_arms` | test | `test_draw_pair_first_symbol_identical_across_arms` | [tests/experiment/test_x5g1t_lineage_oracle.py:133](../../tests/experiment/test_x5g1t_lineage_oracle.py#L133) |  |
| `test_draw_pair_matches_sample_named_per_arm` | test | `test_draw_pair_matches_sample_named_per_arm` | [tests/experiment/test_x5g1t_lineage_oracle.py:123](../../tests/experiment/test_x5g1t_lineage_oracle.py#L123) |  |
| `test_draw_pair_test_split_is_master_independent` | test | `test_draw_pair_test_split_is_master_independent` | [tests/experiment/test_x5g1t_lineage_oracle.py:144](../../tests/experiment/test_x5g1t_lineage_oracle.py#L144) |  |
| `test_dry_plan_rejects_unknown_kind` | test | `test_dry_plan_rejects_unknown_kind` | [tests/hwsb/test_b_streams.py:68](../../tests/hwsb/test_b_streams.py#L68) |  |
| `test_dry_run_refuses_without_rule2_sched` | test | `test_dry_run_refuses_without_rule2_sched` | [tests/hwsb/test_b_records.py:345](../../tests/hwsb/test_b_records.py#L345) |  |
| `test_dry_sequence_ids_follow_contract_replicates` | test | `test_dry_sequence_ids_follow_contract_replicates` | [tests/hwsb/test_b_streams.py:118](../../tests/hwsb/test_b_streams.py#L118) |  |
| `test_dry_streams_match_contract` | test | `test_dry_streams_match_contract` | [tests/hwsb/test_b_streams.py:56](../../tests/hwsb/test_b_streams.py#L56) |  |
| `test_duplicates_are_counted_and_kept` | test | `test_duplicates_are_counted_and_kept` | [tests/hwsb/test_b_streams.py:379](../../tests/hwsb/test_b_streams.py#L379) |  |
| `test_duplicates_counted_never_removed` | test | `test_duplicates_counted_never_removed` | [tests/k4b/test_b_data.py:229](../../tests/k4b/test_b_data.py#L229) |  |
| `test_duplicates_none` | test | `test_duplicates_none` | [tests/k4b/test_b_data.py:243](../../tests/k4b/test_b_data.py#L243) |  |
| `test_E01_failing_stage_records_failure_and_raises_executor_error` | test | `test_E01_failing_stage_records_failure_and_raises_executor_error` | [tests/executors/test_local.py:58](../../tests/executors/test_local.py#L58) |  |
| `test_E01_local_runs_stub_in_subprocess_and_imports_output` | test | `test_E01_local_runs_stub_in_subprocess_and_imports_output` | [tests/executors/test_local.py:37](../../tests/executors/test_local.py#L37) |  |
| `test_E01_manifest_records_executor_hardware_and_time` | test | `test_E01_manifest_records_executor_hardware_and_time` | [tests/executors/test_local.py:47](../../tests/executors/test_local.py#L47) |  |
| `test_E01_registry_lists_all_executors` | test | `test_E01_registry_lists_all_executors` | [tests/executors/test_local.py:94](../../tests/executors/test_local.py#L94) |  |
| `test_E01_ssh_builds_expected_command_lines` | test | `test_E01_ssh_builds_expected_command_lines` | [tests/executors/test_exporter.py:63](../../tests/executors/test_exporter.py#L63) |  |
| `test_E01_ssh_requires_host_and_remote_dir` | test | `test_E01_ssh_requires_host_and_remote_dir` | [tests/executors/test_exporter.py:75](../../tests/executors/test_exporter.py#L75) |  |
| `test_E01_ssh_status_parses_remote_output` | test | `test_E01_ssh_status_parses_remote_output` | [tests/executors/test_exporter.py:81](../../tests/executors/test_exporter.py#L81) |  |
| `test_E01_type_whitelist_allows_manifest_and_rejects_others` | test | `test_E01_type_whitelist_allows_manifest_and_rejects_others` | [tests/executors/test_local.py:87](../../tests/executors/test_local.py#L87) |  |
| `test_E01_unknown_stage_returns_1_and_records_executor_error` | test | `test_E01_unknown_stage_returns_1_and_records_executor_error` | [tests/executors/test_local.py:67](../../tests/executors/test_local.py#L67) |  |
| `test_E01_unreadable_job_json_is_executor_error` | test | `test_E01_unreadable_job_json_is_executor_error` | [tests/executors/test_local.py:79](../../tests/executors/test_local.py#L79) |  |
| `test_E02_bundle_layout_and_git_sha_recorded` | test | `test_E02_bundle_layout_and_git_sha_recorded` | [tests/executors/test_bundle.py:68](../../tests/executors/test_bundle.py#L68) |  |
| `test_E02_bundle_round_trip_matches_local_run` | test | `test_E02_bundle_round_trip_matches_local_run` | [tests/executors/test_bundle.py:51](../../tests/executors/test_bundle.py#L51) |  |
| `test_E02_failed_remote_job_comes_back_as_failure` | test | `test_E02_failed_remote_job_comes_back_as_failure` | [tests/executors/test_bundle.py:79](../../tests/executors/test_bundle.py#L79) |  |
| `test_E03_missing_parent_is_reported` | test | `test_E03_missing_parent_is_reported` | [tests/executors/test_bundle.py:106](../../tests/executors/test_bundle.py#L106) |  |
| `test_E03_tampered_outputs_raise_checksum_mismatch` | test | `test_E03_tampered_outputs_raise_checksum_mismatch` | [tests/executors/test_bundle.py:88](../../tests/executors/test_bundle.py#L88) |  |
| `test_E03_unexpected_output_type_rejected_and_nothing_imported` | test | `test_E03_unexpected_output_type_rejected_and_nothing_imported` | [tests/executors/test_bundle.py:97](../../tests/executors/test_bundle.py#L97) |  |
| `test_E04_explicitly_requested_secret_is_refused` | test | `test_E04_explicitly_requested_secret_is_refused` | [tests/executors/test_exporter.py:28](../../tests/executors/test_exporter.py#L28) |  |
| `test_E04_forbidden_name_rule` | test | `test_E04_forbidden_name_rule` | [tests/executors/test_exporter.py:37](../../tests/executors/test_exporter.py#L37) |  |
| `test_E04_secrets_in_tree_are_left_out` | test | `test_E04_secrets_in_tree_are_left_out` | [tests/executors/test_exporter.py:16](../../tests/executors/test_exporter.py#L16) |  |
| `test_E05_status_awaiting_user_then_done` | test | `test_E05_status_awaiting_user_then_done` | [tests/executors/test_bundle.py:114](../../tests/executors/test_bundle.py#L114) |  |
| `test_E06_notebook_is_valid_nbformat_with_three_code_cells` | test | `test_E06_notebook_is_valid_nbformat_with_three_code_cells` | [tests/executors/test_exporter.py:42](../../tests/executors/test_exporter.py#L42) |  |
| `test_E07_no_science_or_experiment_imports` | test | `test_E07_no_science_or_experiment_imports` | [tests/executors/test_static.py:25](../../tests/executors/test_static.py#L25) |  |
| `test_E07_public_api_is_exactly_the_spec` | test | `test_E07_public_api_is_exactly_the_spec` | [tests/executors/test_static.py:35](../../tests/executors/test_static.py#L35) |  |
| `test_E07_requirements_filter_strips_local_suffix_and_skips_torch` | test | `test_E07_requirements_filter_strips_local_suffix_and_skips_torch` | [tests/executors/test_static.py:42](../../tests/executors/test_static.py#L42) |  |
| `test_e2_threshold_boundaries` | test | `test_e2_threshold_boundaries` | [tests/hws/test_b_worlds.py:347](../../tests/hws/test_b_worlds.py#L347) |  |
| `test_e4_boundary` | test | `test_e4_boundary` | [tests/hws/test_b_exact.py:102](../../tests/hws/test_b_exact.py#L102) |  |
| `test_e5_bin_count_boundary` | test | `test_e5_bin_count_boundary` | [tests/hws/test_a_stats.py:187](../../tests/hws/test_a_stats.py#L187) |  |
| `test_e5_norm_fraction_boundary` | test | `test_e5_norm_fraction_boundary` | [tests/hws/test_a_stats.py:170](../../tests/hws/test_a_stats.py#L170) |  |
| `test_e5_phase_conventions` | test | `test_e5_phase_conventions` | [tests/hws/test_a_stats.py:223](../../tests/hws/test_a_stats.py#L223) |  |
| `test_e5_resultant_boundary` | test | `test_e5_resultant_boundary` | [tests/hws/test_a_stats.py:212](../../tests/hws/test_a_stats.py#L212) |  |
| `test_E_A_matches_minimum_image_softmax` | test | `test_E_A_matches_minimum_image_softmax` | [tests/x2a_stage0/test_x2a_stage0.py:130](../../tests/x2a_stage0/test_x2a_stage0.py#L130) |  |
| `test_each_broken_binding_is_refused` | test | `test_each_broken_binding_is_refused` | [tests/c1prime/test_a_release_meter.py:151](../../tests/c1prime/test_a_release_meter.py#L151) |  |
| `test_each_criterion_in_each_world_can_fail` | test | `test_each_criterion_in_each_world_can_fail` | [tests/analysis/test_sigma_calibrator.py:46](../../tests/analysis/test_sigma_calibrator.py#L46) |  |
| `test_each_tamper_fails` | test | `test_each_tamper_fails` | [tests/hws/test_b_kc1.py:246](../../tests/hws/test_b_kc1.py#L246) |  |
| `test_early_jump_gives_small_p` | test | `test_early_jump_gives_small_p` | [tests/analysis/test_baselines_dynamics.py:103](../../tests/analysis/test_baselines_dynamics.py#L103) |  |
| `test_eb_bound_outward_against_independent_decimal` | test | `test_eb_bound_outward_against_independent_decimal` | [tests/x6_stage1/test_a_numerics.py:165](../../tests/x6_stage1/test_a_numerics.py#L165) |  |
| `test_eb_constants_registered_table` | test | `test_eb_constants_registered_table` | [tests/x6_stage1/test_a_numerics.py:172](../../tests/x6_stage1/test_a_numerics.py#L172) |  |
| `test_eb_exact_coverage_two_point_laws` | test | `test_eb_exact_coverage_two_point_laws` | [tests/x6_stage1/test_a_numerics.py:194](../../tests/x6_stage1/test_a_numerics.py#L194) | X in {0, B}: pair types (both 0, mixed, both B) are trinomial; P(mu <= U) >= 1 - delta. |
| `test_eb_monotone_in_xbar_and_zbar` | test | `test_eb_monotone_in_xbar_and_zbar` | [tests/x6_stage1/test_a_numerics.py:185](../../tests/x6_stage1/test_a_numerics.py#L185) |  |
| `test_eb_report_is_outward_bound_without_separation_term` | test | `test_eb_report_is_outward_bound_without_separation_term` | [tests/x6_stage1/test_a_numerics.py:223](../../tests/x6_stage1/test_a_numerics.py#L223) |  |
| `test_edge_classification_counts` | test | `test_edge_classification_counts` | [tests/process/test_conductance.py:185](../../tests/process/test_conductance.py#L185) |  |
| `test_edge_list_hand_graph_inclusive_and_lexicographic` | test | `test_edge_list_hand_graph_inclusive_and_lexicographic` | [tests/circle_history/test_cochain.py:84](../../tests/circle_history/test_cochain.py#L84) |  |
| `test_effective_settings` | test | `test_effective_settings` | [tests/hwsb/test_b_meter_law.py:92](../../tests/hwsb/test_b_meter_law.py#L92) |  |
| `test_eigen_order_is_descending` | test | `test_eigen_order_is_descending` | [tests/analysis/test_x4f_targets.py:110](../../tests/analysis/test_x4f_targets.py#L110) |  |
| `test_elapsed_time_and_reset_times_never_clear` | test | `test_elapsed_time_and_reset_times_never_clear` | [tests/experiment/test_x5g1t_usage.py:359](../../tests/experiment/test_x5g1t_usage.py#L359) |  |
| `test_eligibility_order_and_e6` | test | `test_eligibility_order_and_e6` | [tests/hws/test_a_classify.py:138](../../tests/hws/test_a_classify.py#L138) |  |
| `test_eligibility_rule_boundaries` | test | `test_eligibility_rule_boundaries` | [tests/c1prime/test_a_eligibility_support.py:54](../../tests/c1prime/test_a_eligibility_support.py#L54) |  |
| `test_eligible_fraction_and_the_h4_threshold` | test | `test_eligible_fraction_and_the_h4_threshold` | [tests/c1prime/test_a_eligibility_support.py:67](../../tests/c1prime/test_a_eligibility_support.py#L67) |  |
| `test_emission_variants_against_reference` | test | `test_emission_variants_against_reference` | [tests/x2a_stage0/test_x2a_stage0.py:192](../../tests/x2a_stage0/test_x2a_stage0.py#L192) |  |
| `test_enclosure_branch_corrupted_float_closed_form_fails` | test | `test_enclosure_branch_corrupted_float_closed_form_fails` | [tests/c1prime/test_a_oracle.py:296](../../tests/c1prime/test_a_oracle.py#L296) | Section 3.2 S1 fixture: corrupted float64 closed-form values on the enclosure branch, |
| `test_enclosure_contains_exact_entries_on_sampled_rows` | test | `test_enclosure_contains_exact_entries_on_sampled_rows` | [tests/hwsb/test_a_enclosure_proof.py:266](../../tests/hwsb/test_a_enclosure_proof.py#L266) | Steps (1)-(3) combined: E*_j in [E_dec (1 - 2 delta)/hi0, E_dec/(lo0 (1 - 2 delta))]. |
| `test_endpoint_arrays_row_construction` | test | `test_endpoint_arrays_row_construction` | [tests/k4b/test_a_theorem_a.py:237](../../tests/k4b/test_a_theorem_a.py#L237) |  |
| `test_endpoint_bounds_use_shared_draws_and_ranks_84_and_4917` | test | `test_endpoint_bounds_use_shared_draws_and_ranks_84_and_4917` | [tests/c1prime/test_b_inference.py:232](../../tests/c1prime/test_b_inference.py#L232) |  |
| `test_endpoint_guard_binding_B_and_equality` | test | `test_endpoint_guard_binding_B_and_equality` | [tests/c1prime/test_b_cert_guards.py:139](../../tests/c1prime/test_b_cert_guards.py#L139) |  |
| `test_endpoint_guard_far_from_zero_passes_with_either_sign` | test | `test_endpoint_guard_far_from_zero_passes_with_either_sign` | [tests/c1prime/test_b_cert_guards.py:125](../../tests/c1prime/test_b_cert_guards.py#L125) |  |
| `test_endpoint_guard_floor_is_exactly_ten_to_minus_nine` | test | `test_endpoint_guard_floor_is_exactly_ten_to_minus_nine` | [tests/c1prime/test_b_cert_guards.py:130](../../tests/c1prime/test_b_cert_guards.py#L130) |  |
| `test_endpoint_keys_single_stream_and_no_writes` | test | `test_endpoint_keys_single_stream_and_no_writes` | [tests/k4b/test_b_endpoint.py:324](../../tests/k4b/test_b_endpoint.py#L324) |  |
| `test_endpoint_logits_after_t_pre_passes` | test | `test_endpoint_logits_after_t_pre_passes` | [tests/c1prime/test_a_gates.py:138](../../tests/c1prime/test_a_gates.py#L138) |  |
| `test_endpoint_logits_never_follow_a_failed_t_pre` | test | `test_endpoint_logits_never_follow_a_failed_t_pre` | [tests/c1prime/test_a_gates.py:125](../../tests/c1prime/test_a_gates.py#L125) | Row 20 not passed: no fresh primary/control logits, and NUM cannot begin. |
| `test_endpoint_per_model_bounds_margins_status_support_and_overall` | test | `test_endpoint_per_model_bounds_margins_status_support_and_overall` | [tests/k4b/test_b_endpoint.py:347](../../tests/k4b/test_b_endpoint.py#L347) |  |
| `test_endpoint_status_new6` | test | `test_endpoint_status_new6` | [tests/c2_readout/test_a_inference.py:296](../../tests/c2_readout/test_a_inference.py#L296) |  |
| `test_endpoint_summaries_ratios_init_qualifier_and_agreement` | test | `test_endpoint_summaries_ratios_init_qualifier_and_agreement` | [tests/k4b/test_b_endpoint.py:384](../../tests/k4b/test_b_endpoint.py#L384) |  |
| `test_endpoints_no_or_full_support` | test | `test_endpoints_no_or_full_support` | [tests/hwsb/test_a_endpoints.py:118](../../tests/hwsb/test_a_endpoints.py#L118) |  |
| `test_endpoints_partial_support_exact` | test | `test_endpoints_partial_support_exact` | [tests/hwsb/test_a_endpoints.py:101](../../tests/hwsb/test_a_endpoints.py#L101) |  |
| `test_endpoints_supported_rows_use_the_extension_phase_only` | test | `test_endpoints_supported_rows_use_the_extension_phase_only` | [tests/hwsb/test_a_endpoints.py:131](../../tests/hwsb/test_a_endpoints.py#L131) |  |
| `test_energies_match_definitions_and_isotropic_ratio_is_one_tenth` | test | `test_energies_match_definitions_and_isotropic_ratio_is_one_tenth` | [tests/c2_readout/test_a_partition.py:208](../../tests/c2_readout/test_a_partition.py#L208) |  |
| `test_entropy_mass_logit_and_expit` | test | `test_entropy_mass_logit_and_expit` | [tests/x2a_stage0/test_x2a_stage0_ph.py:107](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L107) |  |
| `test_enumerate_histories_order_and_probabilities` | test | `test_enumerate_histories_order_and_probabilities` | [tests/hws/test_a_identities.py:317](../../tests/hws/test_a_identities.py#L317) |  |
| `test_env_changed_reports_only_real_changes` | test | `test_env_changed_reports_only_real_changes` | [tests/x6_stage1/test_b_chain_ops.py:285](../../tests/x6_stage1/test_b_chain_ops.py#L285) |  |
| `test_env_local_record_complete` | test | `test_env_local_record_complete` | [tests/x6_stage1/test_b_chain_ops.py:273](../../tests/x6_stage1/test_b_chain_ops.py#L273) |  |
| `test_envelopes_match_error_bound` | test | `test_envelopes_match_error_bound` | [tests/k4b/test_a_lemma_n.py:186](../../tests/k4b/test_a_lemma_n.py#L186) |  |
| `test_environment_refuses_cpu_runtime` | test | `test_environment_refuses_cpu_runtime` | [tests/x6_stage1/test_b_nb_s0_ops.py:190](../../tests/x6_stage1/test_b_nb_s0_ops.py#L190) |  |
| `test_equal_arms_give_exactly_zero` | test | `test_equal_arms_give_exactly_zero` | [tests/c1prime/test_b_identities.py:144](../../tests/c1prime/test_b_identities.py#L144) |  |
| `test_equal_ids_pass_silently` | test | `test_equal_ids_pass_silently` | [tests/analysis/test_spaces.py:15](../../tests/analysis/test_spaces.py#L15) |  |
| `test_equality_and_guard_are_never_declared` | test | `test_equality_and_guard_are_never_declared` | [tests/c2_readout/test_a_inference.py:153](../../tests/c2_readout/test_a_inference.py#L153) |  |
| `test_eraser_from_basis_formula` | test | `test_eraser_from_basis_formula` | [tests/analysis/test_x4f_erasure.py:138](../../tests/analysis/test_x4f_erasure.py#L138) |  |
| `test_eraser_invalid_keeps_computed_map` | test | `test_eraser_invalid_keeps_computed_map` | [tests/analysis/test_x4f_erasure.py:247](../../tests/analysis/test_x4f_erasure.py#L247) |  |
| `test_error_bad_p_stay_and_kind` | test | `test_error_bad_p_stay_and_kind` | [tests/process/test_transition.py:87](../../tests/process/test_transition.py#L87) |  |
| `test_error_classes_unchanged` | test | `test_error_classes_unchanged` | [tests/circle_history/test_controls.py:147](../../tests/circle_history/test_controls.py#L147) |  |
| `test_error_illegal_support` | test | `test_error_illegal_support` | [tests/process/test_transition.py:77](../../tests/process/test_transition.py#L77) |  |
| `test_error_paths` | test | `test_error_paths` | [tests/prediction/test_ngram.py:79](../../tests/prediction/test_ngram.py#L79) |  |
| `test_error_state_order_and_unknown_strategy` | test | `test_error_state_order_and_unknown_strategy` | [tests/process/test_overlap.py:146](../../tests/process/test_overlap.py#L146) |  |
| `test_error_state_order_mismatch` | test | `test_error_state_order_mismatch` | [tests/process/test_transition.py:95](../../tests/process/test_transition.py#L95) |  |
| `test_est_constants_and_defaults` | test | `test_est_constants_and_defaults` | [tests/experiment/test_x5g1t_runtime_boundary.py:119](../../tests/experiment/test_x5g1t_runtime_boundary.py#L119) |  |
| `test_euclidean_hand_values` | test | `test_euclidean_hand_values` | [tests/topology/test_metrics.py:24](../../tests/topology/test_metrics.py#L24) |  |
| `test_euclidean_variant_still_excludes_gamma` | test | `test_euclidean_variant_still_excludes_gamma` | [tests/c2_readout/test_a_readout.py:315](../../tests/c2_readout/test_a_readout.py#L315) |  |
| `test_evaluating_stage_record_holds_env_local` | test | `test_evaluating_stage_record_holds_env_local` | [tests/x6_stage1/test_b_chain_ops.py:292](../../tests/x6_stage1/test_b_chain_ops.py#L292) |  |
| `test_evaluation_reserve` | test | `test_evaluation_reserve` | [tests/experiment/test_x5g1t_runtime_boundary.py:158](../../tests/experiment/test_x5g1t_runtime_boundary.py#L158) |  |
| `test_every_latched_kind_must_be_present_relevant_numeric_low` | test | `test_every_latched_kind_must_be_present_relevant_numeric_low` | [tests/experiment/test_x5g1t_usage.py:246](../../tests/experiment/test_x5g1t_usage.py#L246) |  |
| `test_evidence_change_is_integrity_refusal_and_export_fails` | test | `test_evidence_change_is_integrity_refusal_and_export_fails` | [tests/circle_history/test_builder_v24_stages.py:63](../../tests/circle_history/test_builder_v24_stages.py#L63) |  |
| `test_exact_constants` | test | `test_exact_constants` | [tests/c1prime/test_b_cert_guards.py:62](../../tests/c1prime/test_b_cert_guards.py#L62) |  |
| `test_exact_enumeration_k2_k3` | test | `test_exact_enumeration_k2_k3` | [tests/x2a_stage0/test_x2a_stage0.py:265](../../tests/x2a_stage0/test_x2a_stage0.py#L265) |  |
| `test_exact_expectations_matches_the_fraction_values` | test | `test_exact_expectations_matches_the_fraction_values` | [tests/hws/test_a_identities.py:328](../../tests/hws/test_a_identities.py#L328) |  |
| `test_exact_features_rejects_bad_coordinates` | test | `test_exact_features_rejects_bad_coordinates` | [tests/circle_history/test_error_bound.py:173](../../tests/circle_history/test_error_bound.py#L173) |  |
| `test_exact_features_values` | test | `test_exact_features_values` | [tests/circle_history/test_error_bound.py:157](../../tests/circle_history/test_error_bound.py#L157) |  |
| `test_exact_filters_order_e1_e2_e3` | test | `test_exact_filters_order_e1_e2_e3` | [tests/hws/test_b_worlds.py:364](../../tests/hws/test_b_worlds.py#L364) |  |
| `test_exact_gap_boundary_at_one_over_ten_to_the_ten` | test | `test_exact_gap_boundary_at_one_over_ten_to_the_ten` | [tests/circle_history/test_reference_binding.py:179](../../tests/circle_history/test_reference_binding.py#L179) |  |
| `test_exact_invariance_fails_on_one_ulp` | test | `test_exact_invariance_fails_on_one_ulp` | [tests/c1prime/test_a_oracle.py:161](../../tests/c1prime/test_a_oracle.py#L161) |  |
| `test_exact_logits_equal_independent_fractions` | test | `test_exact_logits_equal_independent_fractions` | [tests/hwsb/test_a_enclosure_proof.py:155](../../tests/hwsb/test_a_enclosure_proof.py#L155) |  |
| `test_exact_model_matches_reference` | test | `test_exact_model_matches_reference` | [tests/d1_seam/test_d1_seam.py:167](../../tests/d1_seam/test_d1_seam.py#L167) |  |
| `test_exact_sign_fixture_plus_theta_moves_toward_the_plus_rolled_belief` | test | `test_exact_sign_fixture_plus_theta_moves_toward_the_plus_rolled_belief` | [tests/c2_readout/test_a_oracle.py:285](../../tests/c2_readout/test_a_oracle.py#L285) |  |
| `test_exact_world_e1_carries_only_e1` | test | `test_exact_world_e1_carries_only_e1` | [tests/hws/test_b_exact.py:276](../../tests/hws/test_b_exact.py#L276) |  |
| `test_exact_world_identity_fields_at_w0` | test | `test_exact_world_identity_fields_at_w0` | [tests/hws/test_b_exact.py:268](../../tests/hws/test_b_exact.py#L268) |  |
| `test_exact_world_on_a_symmetric_cell` | test | `test_exact_world_on_a_symmetric_cell` | [tests/hws/test_b_exact.py:253](../../tests/hws/test_b_exact.py#L253) |  |
| `test_exactly_7275_does_not_hold_and_just_above_holds` | test | `test_exactly_7275_does_not_hold_and_just_above_holds` | [tests/hwsb/test_b_hold.py:50](../../tests/hwsb/test_b_hold.py#L50) |  |
| `test_exactly_seven_of_eight_positive_passes` | test | `test_exactly_seven_of_eight_positive_passes` | [tests/analysis/test_f1_rule.py:134](../../tests/analysis/test_f1_rule.py#L134) |  |
| `test_exactly_uncorrelated_target` | test | `test_exactly_uncorrelated_target` | [tests/analysis/test_x4f_erasure.py:270](../../tests/analysis/test_x4f_erasure.py#L270) |  |
| `test_exclude_lower_boundary_is_strict` | test | `test_exclude_lower_boundary_is_strict` | [tests/k4b/test_a_decision.py:133](../../tests/k4b/test_a_decision.py#L133) |  |
| `test_exclude_upper_boundary_is_strict` | test | `test_exclude_upper_boundary_is_strict` | [tests/k4b/test_a_decision.py:125](../../tests/k4b/test_a_decision.py#L125) |  |
| `test_excluded_landmarks_get_extension_phases_only` | test | `test_excluded_landmarks_get_extension_phases_only` | [tests/c1prime/test_a_chart_lcc512.py:198](../../tests/c1prime/test_a_chart_lcc512.py#L198) | Item 5: satellites are never charted neighbours; their phase comes from extend. |
| `test_executed_cell_normalisation` | test | `test_executed_cell_normalisation` | [tests/x6_stage1/test_b_ingest_bundle.py:377](../../tests/x6_stage1/test_b_ingest_bundle.py#L377) |  |
| `test_exhausted_or_unreleased_stage_runs_noop` | test | `test_exhausted_or_unreleased_stage_runs_noop` | [tests/circle_history/test_builder_runtime.py:82](../../tests/circle_history/test_builder_runtime.py#L82) |  |
| `test_exhaustive_enumeration_to_depth_5` | test | `test_exhaustive_enumeration_to_depth_5` | [tests/d1_seam/test_d1_seam.py:302](../../tests/d1_seam/test_d1_seam.py#L302) |  |
| `test_existing_lock_refuses_start` | test | `test_existing_lock_refuses_start` | [tests/experiment/test_x5g1t_training.py:292](../../tests/experiment/test_x5g1t_training.py#L292) |  |
| `test_exited_launcher_does_not_hide_live_grandchild_or_its_usage` | test | `test_exited_launcher_does_not_hide_live_grandchild_or_its_usage` | [tests/d2a/test_process_tree_repair.py:49](../../tests/d2a/test_process_tree_repair.py#L49) |  |
| `test_expected_digests_independent` | test | `test_expected_digests_independent` | [tests/x6_stage1/test_b_train_chain.py:261](../../tests/x6_stage1/test_b_train_chain.py#L261) |  |
| `test_expected_envelope_reproduces_process_stage` | test | `test_expected_envelope_reproduces_process_stage` | [tests/hws/test_b_kc1.py:203](../../tests/hws/test_b_kc1.py#L203) |  |
| `test_expected_meta_from_contract` | test | `test_expected_meta_from_contract` | [tests/k4b/test_b_h1_meta.py:105](../../tests/k4b/test_b_h1_meta.py#L105) |  |
| `test_expected_meta_unknown_model_or_label_raises` | test | `test_expected_meta_unknown_model_or_label_raises` | [tests/k4b/test_b_h1_meta.py:129](../../tests/k4b/test_b_h1_meta.py#L129) |  |
| `test_expected_payload_sha_is_bound_never_none` | test | `test_expected_payload_sha_is_bound_never_none` | [tests/k4b/test_b_h1_meta.py:120](../../tests/k4b/test_b_h1_meta.py#L120) |  |
| `test_export_budget_exceeded` | test | `test_export_budget_exceeded` | [tests/experiment/test_x5g1_safety.py:333](../../tests/experiment/test_x5g1_safety.py#L333) |  |
| `test_export_cap_is_80_without_release` | test | `test_export_cap_is_80_without_release` | [tests/circle_history/test_builder_runtime.py:89](../../tests/circle_history/test_builder_runtime.py#L89) |  |
| `test_export_entries_sorted_and_exact` | test | `test_export_entries_sorted_and_exact` | [tests/circle_history/test_reference_cache.py:99](../../tests/circle_history/test_reference_cache.py#L99) |  |
| `test_export_error_classes_are_runtime_errors` | test | `test_export_error_classes_are_runtime_errors` | [tests/experiment/test_x5g1t_export_checks.py:201](../../tests/experiment/test_x5g1t_export_checks.py#L201) |  |
| `test_export_extra_file_incomplete` | test | `test_export_extra_file_incomplete` | [tests/experiment/test_x5g1t_export_checks.py:167](../../tests/experiment/test_x5g1t_export_checks.py#L167) |  |
| `test_export_interrupted_before_second_file` | test | `test_export_interrupted_before_second_file` | [tests/experiment/test_x5g1t_export_checks.py:113](../../tests/experiment/test_x5g1t_export_checks.py#L113) |  |
| `test_export_missing_data_file_incomplete` | test | `test_export_missing_data_file_incomplete` | [tests/experiment/test_x5g1t_export_checks.py:181](../../tests/experiment/test_x5g1t_export_checks.py#L181) |  |
| `test_export_missing_manifest_incomplete` | test | `test_export_missing_manifest_incomplete` | [tests/experiment/test_x5g1t_export_checks.py:174](../../tests/experiment/test_x5g1t_export_checks.py#L174) |  |
| `test_export_missing_or_non_complete_status_incomplete` | test | `test_export_missing_or_non_complete_status_incomplete` | [tests/experiment/test_x5g1t_export_checks.py:188](../../tests/experiment/test_x5g1t_export_checks.py#L188) |  |
| `test_export_other_exception_propagates_without_status` | test | `test_export_other_exception_propagates_without_status` | [tests/experiment/test_x5g1_safety.py:349](../../tests/experiment/test_x5g1_safety.py#L349) |  |
| `test_export_round_trips_all_maps_without_pickle_and_records_hash` | test | `test_export_round_trips_all_maps_without_pickle_and_records_hash` | [tests/experiment/test_x4f_maintenance.py:113](../../tests/experiment/test_x4f_maintenance.py#L113) |  |
| `test_export_roundtrip_complete_and_guarded` | test | `test_export_roundtrip_complete_and_guarded` | [tests/experiment/test_x5g1t_export_checks.py:79](../../tests/experiment/test_x5g1t_export_checks.py#L79) |  |
| `test_export_roundtrip_with_arrays` | test | `test_export_roundtrip_with_arrays` | [tests/experiment/test_x5g1t_export_checks.py:104](../../tests/experiment/test_x5g1t_export_checks.py#L104) |  |
| `test_export_stop_after_file_done_writes_nothing_further` | test | `test_export_stop_after_file_done_writes_nothing_further` | [tests/experiment/test_x5g1t_export_checks.py:131](../../tests/experiment/test_x5g1t_export_checks.py#L131) |  |
| `test_export_stop_before_manifest` | test | `test_export_stop_before_manifest` | [tests/experiment/test_x5g1t_export_checks.py:144](../../tests/experiment/test_x5g1t_export_checks.py#L144) |  |
| `test_export_stop_file_created_in_step1` | test | `test_export_stop_file_created_in_step1` | [tests/experiment/test_x5g1_safety.py:286](../../tests/experiment/test_x5g1_safety.py#L286) |  |
| `test_export_stop_in_middle_step_keeps_completed` | test | `test_export_stop_in_middle_step_keeps_completed` | [tests/experiment/test_x5g1_safety.py:305](../../tests/experiment/test_x5g1_safety.py#L305) |  |
| `test_export_stop_present_before_start_runs_nothing` | test | `test_export_stop_present_before_start_runs_nothing` | [tests/experiment/test_x5g1_safety.py:320](../../tests/experiment/test_x5g1_safety.py#L320) |  |
| `test_export_tampered_file_bytes_incomplete` | test | `test_export_tampered_file_bytes_incomplete` | [tests/experiment/test_x5g1t_export_checks.py:159](../../tests/experiment/test_x5g1t_export_checks.py#L159) |  |
| `test_export_without_stop_runs_all_in_order` | test | `test_export_without_stop_runs_all_in_order` | [tests/experiment/test_x5g1_safety.py:272](../../tests/experiment/test_x5g1_safety.py#L272) |  |
| `test_expression_counts_do_not_exceed_the_section_15_3_5_table` | test | `test_expression_counts_do_not_exceed_the_section_15_3_5_table` | [tests/c1prime/test_b_cert_bounds.py:289](../../tests/c1prime/test_b_cert_bounds.py#L289) |  |
| `test_extend_eighth_distance_boundary` | test | `test_extend_eighth_distance_boundary` | [tests/circle_history/test_chart_extension.py:130](../../tests/circle_history/test_chart_extension.py#L130) |  |
| `test_extend_exact_duplicates_average_all` | test | `test_extend_exact_duplicates_average_all` | [tests/circle_history/test_chart_extension.py:168](../../tests/circle_history/test_chart_extension.py#L168) |  |
| `test_extend_formula_and_stable_ties` | test | `test_extend_formula_and_stable_ties` | [tests/circle_history/test_chart_extension.py:104](../../tests/circle_history/test_chart_extension.py#L104) |  |
| `test_extend_held_out_circle_agrees_with_direct` | test | `test_extend_held_out_circle_agrees_with_direct` | [tests/circle_history/test_chart_extension.py:213](../../tests/circle_history/test_chart_extension.py#L213) |  |
| `test_extend_never_mutates` | test | `test_extend_never_mutates` | [tests/circle_history/test_chart_extension.py:194](../../tests/circle_history/test_chart_extension.py#L194) |  |
| `test_extend_never_returns_two_pi` | test | `test_extend_never_returns_two_pi` | [tests/circle_history/test_builder_v25.py:265](../../tests/circle_history/test_builder_v25.py#L265) | A query equidistant from 8 landmarks whose mean angle is a tiny negative number. |
| `test_extend_nonfinite_z_invalid` | test | `test_extend_nonfinite_z_invalid` | [tests/circle_history/test_chart_extension.py:257](../../tests/circle_history/test_chart_extension.py#L257) |  |
| `test_extend_phase_is_the_frozen_extend` | test | `test_extend_phase_is_the_frozen_extend` | [tests/c1prime/test_a_chart_val.py:178](../../tests/c1prime/test_a_chart_val.py#L178) |  |
| `test_extend_resultant_boundary` | test | `test_extend_resultant_boundary` | [tests/circle_history/test_chart_extension.py:149](../../tests/circle_history/test_chart_extension.py#L149) |  |
| `test_extra_file_in_train_export_refuses_dev_analysis` | test | `test_extra_file_in_train_export_refuses_dev_analysis` | [tests/experiment/test_x5g1t_integration.py:368](../../tests/experiment/test_x5g1t_integration.py#L368) |  |
| `test_extra_unlisted_file_fails_closed` | test | `test_extra_unlisted_file_fails_closed` | [tests/hwsb/test_b_registry.py:151](../../tests/hwsb/test_b_registry.py#L151) |  |
| `test_f1_rank_and_condition_boundaries` | test | `test_f1_rank_and_condition_boundaries` | [tests/c1prime/test_b_fwl.py:159](../../tests/c1prime/test_b_fwl.py#L159) |  |
| `test_f1_singular_value_boundaries` | test | `test_f1_singular_value_boundaries` | [tests/c1prime/test_b_fwl.py:169](../../tests/c1prime/test_b_fwl.py#L169) |  |
| `test_f1_symbol_determined_phase_is_degenerate` | test | `test_f1_symbol_determined_phase_is_degenerate` | [tests/c1prime/test_b_fwl.py:130](../../tests/c1prime/test_b_fwl.py#L130) |  |
| `test_f1_table_reports_four_medians_and_positive_count` | test | `test_f1_table_reports_four_medians_and_positive_count` | [tests/experiment/test_report_e2.py:45](../../tests/experiment/test_report_e2.py#L45) |  |
| `test_F_plan_conditions_are_needed` | test | `test_F_plan_conditions_are_needed` | [tests/k4b/test_a_decision.py:281](../../tests/k4b/test_a_decision.py#L281) |  |
| `test_F_plan_desk_values` | test | `test_F_plan_desk_values` | [tests/k4b/test_a_decision.py:263](../../tests/k4b/test_a_decision.py#L263) |  |
| `test_F_plan_exact` | test | `test_F_plan_exact` | [tests/k4b/test_a_decision.py:255](../../tests/k4b/test_a_decision.py#L255) |  |
| `test_F_test_never_exceeds_F_plan_under_cap_and_p2` | test | `test_F_test_never_exceeds_F_plan_under_cap_and_p2` | [tests/k4b/test_a_decision.py:269](../../tests/k4b/test_a_decision.py#L269) |  |
| `test_factor_is_applied_to_estimate_only` | test | `test_factor_is_applied_to_estimate_only` | [tests/experiment/test_x5g1t_runtime_boundary.py:137](../../tests/experiment/test_x5g1t_runtime_boundary.py#L137) |  |
| `test_fail_technical_first_then_inconclusive` | test | `test_fail_technical_first_then_inconclusive` | [tests/hws/test_a_outcomes.py:136](../../tests/hws/test_a_outcomes.py#L136) |  |
| `test_failed_construction_keeps_its_claim_and_is_never_retried` | test | `test_failed_construction_keeps_its_claim_and_is_never_retried` | [tests/k4b/test_b_charts.py:141](../../tests/k4b/test_b_charts.py#L141) |  |
| `test_fallback_only_2x_set_cap_and_ties` | test | `test_fallback_only_2x_set_cap_and_ties` | [tests/hws/test_a_classify.py:290](../../tests/hws/test_a_classify.py#L290) |  |
| `test_fallback_only_2x_set_membership` | test | `test_fallback_only_2x_set_membership` | [tests/hws/test_a_classify.py:274](../../tests/hws/test_a_classify.py#L274) |  |
| `test_fallback_only_worlds_give_below_3x_never_selected` | test | `test_fallback_only_worlds_give_below_3x_never_selected` | [tests/hws/test_a_outcomes.py:145](../../tests/hws/test_a_outcomes.py#L145) |  |
| `test_fallback_threshold_exactly_003_accepted` | test | `test_fallback_threshold_exactly_003_accepted` | [tests/analysis/test_sigma_calibrator.py:93](../../tests/analysis/test_sigma_calibrator.py#L93) |  |
| `test_fallback_uses_min_over_worlds_not_max_or_mean` | test | `test_fallback_uses_min_over_worlds_not_max_or_mean` | [tests/analysis/test_sigma_calibrator.py:82](../../tests/analysis/test_sigma_calibrator.py#L82) |  |
| `test_fallback_weak_context_picks_argmax_min_G_C` | test | `test_fallback_weak_context_picks_argmax_min_G_C` | [tests/analysis/test_sigma_calibrator.py:69](../../tests/analysis/test_sigma_calibrator.py#L69) |  |
| `test_family_degenerate_draws_rejected_and_counted` | test | `test_family_degenerate_draws_rejected_and_counted` | [tests/analysis/test_x4f_erasure_family.py:199](../../tests/analysis/test_x4f_erasure_family.py#L199) |  |
| `test_family_degenerate_features` | test | `test_family_degenerate_features` | [tests/analysis/test_x4f_erasure_family.py:156](../../tests/analysis/test_x4f_erasure_family.py#L156) |  |
| `test_family_deterministic_given_rng_for` | test | `test_family_deterministic_given_rng_for` | [tests/analysis/test_x4f_erasure_family.py:124](../../tests/analysis/test_x4f_erasure_family.py#L124) |  |
| `test_family_matches_spec_draw_procedure_and_window` | test | `test_family_matches_spec_draw_procedure_and_window` | [tests/analysis/test_x4f_erasure_family.py:66](../../tests/analysis/test_x4f_erasure_family.py#L66) |  |
| `test_family_rank_deficient_maps_live_in_retained_range` | test | `test_family_rank_deficient_maps_live_in_retained_range` | [tests/analysis/test_x4f_erasure_family.py:93](../../tests/analysis/test_x4f_erasure_family.py#L93) |  |
| `test_family_rank_equal_to_k_allowed_and_rank_above_k_rejected` | test | `test_family_rank_equal_to_k_allowed_and_rank_above_k_rejected` | [tests/analysis/test_x4f_erasure_family.py:111](../../tests/analysis/test_x4f_erasure_family.py#L111) |  |
| `test_family_stop_before_second_draw` | test | `test_family_stop_before_second_draw` | [tests/analysis/test_x4f_family_maintenance.py:11](../../tests/analysis/test_x4f_family_maintenance.py#L11) |  |
| `test_family_unmatched_impossible_target` | test | `test_family_unmatched_impossible_target` | [tests/analysis/test_x4f_erasure_family.py:174](../../tests/analysis/test_x4f_erasure_family.py#L174) |  |
| `test_family_unmatched_small_budget_returns_accepted` | test | `test_family_unmatched_small_budget_returns_accepted` | [tests/analysis/test_x4f_erasure_family.py:163](../../tests/analysis/test_x4f_erasure_family.py#L163) |  |
| `test_family_zero_displacement_makes_no_draws` | test | `test_family_zero_displacement_makes_no_draws` | [tests/analysis/test_x4f_erasure_family.py:139](../../tests/analysis/test_x4f_erasure_family.py#L139) |  |
| `test_far_outlier_is_reported_outside_giant` | test | `test_far_outlier_is_reported_outside_giant` | [tests/chart_diag/test_chart_diag.py:56](../../tests/chart_diag/test_chart_diag.py#L56) |  |
| `test_far_query_keeps_exact_normalised_weights` | test | `test_far_query_keeps_exact_normalised_weights` | [tests/circle_history/test_chart_extension.py:230](../../tests/circle_history/test_chart_extension.py#L230) |  |
| `test_far_query_with_fitted_scale_unsupported` | test | `test_far_query_with_fitted_scale_unsupported` | [tests/circle_history/test_chart_extension.py:249](../../tests/circle_history/test_chart_extension.py#L249) |  |
| `test_feature_posterior_and_moment_envelopes_match_formulas` | test | `test_feature_posterior_and_moment_envelopes_match_formulas` | [tests/circle_history/test_error_bound.py:107](../../tests/circle_history/test_error_bound.py#L107) |  |
| `test_features_equal_circle_features_and_posterior_means` | test | `test_features_equal_circle_features_and_posterior_means` | [tests/hws/test_b_worlds.py:190](../../tests/hws/test_b_worlds.py#L190) |  |
| `test_fidelity_below_080_fails` | test | `test_fidelity_below_080_fails` | [tests/c1prime/test_a_chart_val.py:168](../../tests/c1prime/test_a_chart_val.py#L168) |  |
| `test_fidelity_uses_the_complete_direct_component_unmasked_by_support` | test | `test_fidelity_uses_the_complete_direct_component_unmasked_by_support` | [tests/c1prime/test_a_chart_val.py:155](../../tests/c1prime/test_a_chart_val.py#L155) |  |
| `test_field_mixing_suffix_and_residual_sign_is_nonzero` | test | `test_field_mixing_suffix_and_residual_sign_is_nonzero` | [tests/k4b/test_a_prop1.py:170](../../tests/k4b/test_a_prop1.py#L170) | A suffix table multiplied by a residual-sign indicator is no longer suffix-only. |
| `test_filter_inputs_untouched_and_rows_independent` | test | `test_filter_inputs_untouched_and_rows_independent` | [tests/oracle/test_oracle.py:99](../../tests/oracle/test_oracle.py#L99) |  |
| `test_filtration_boundary_cocycle_error_is_chart_unavailable` | test | `test_filtration_boundary_cocycle_error_is_chart_unavailable` | [tests/c1prime/test_a_chart_exceptions.py:83](../../tests/c1prime/test_a_chart_exceptions.py#L83) |  |
| `test_final_test_collision_input_mutated_after_load_refused` | test | `test_final_test_collision_input_mutated_after_load_refused` | [tests/experiment/test_x5g1t_identity_eval.py:276](../../tests/experiment/test_x5g1t_identity_eval.py#L276) | The collision check runs before the fresh draw (§D), so the bytes are changed when the |
| `test_final_test_control_draws_and_records_test_provenance` | test | `test_final_test_control_draws_and_records_test_provenance` | [tests/experiment/test_x5g1t_identity_eval.py:230](../../tests/experiment/test_x5g1t_identity_eval.py#L230) |  |
| `test_final_test_control_draws_once` | test | `test_final_test_control_draws_once` | [tests/experiment/test_x5g1t_integration.py:243](../../tests/experiment/test_x5g1t_integration.py#L243) | Positive control: the draw spy sees the fresh draw when nothing stops it. |
| `test_final_test_prerequisite_identity_failure_never_draws` | test | `test_final_test_prerequisite_identity_failure_never_draws` | [tests/experiment/test_x5g1t_identity_eval.py:260](../../tests/experiment/test_x5g1t_identity_eval.py#L260) |  |
| `test_finalists_first_16_ordinary_never_marginal` | test | `test_finalists_first_16_ordinary_never_marginal` | [tests/hws/test_a_classify.py:256](../../tests/hws/test_a_classify.py#L256) |  |
| `test_finalization_only_for_export` | test | `test_finalization_only_for_export` | [tests/circle_history/test_builder_guards.py:91](../../tests/circle_history/test_builder_guards.py#L91) |  |
| `test_finalization_reserve_binding` | test | `test_finalization_reserve_binding` | [tests/circle_history/test_builder_guards.py:81](../../tests/circle_history/test_builder_guards.py#L81) |  |
| `test_finite_f_with_infinite_residual_is_technical` | test | `test_finite_f_with_infinite_residual_is_technical` | [tests/c1prime/test_a_chart_exceptions.py:138](../../tests/c1prime/test_a_chart_exceptions.py#L138) |  |
| `test_finite_f_with_nan_residual_is_technical` | test | `test_finite_f_with_nan_residual_is_technical` | [tests/c1prime/test_a_chart_exceptions.py:148](../../tests/c1prime/test_a_chart_exceptions.py#L148) | A NaN normaliser makes the residual NaN while f stays finite. |
| `test_finite_smoothing_residual_above_tolerance_is_chart_unavailable` | test | `test_finite_smoothing_residual_above_tolerance_is_chart_unavailable` | [tests/c1prime/test_a_chart_exceptions.py:112](../../tests/c1prime/test_a_chart_exceptions.py#L112) |  |
| `test_first_candidate_passes` | test | `test_first_candidate_passes` | [tests/analysis/test_sigma_calibrator.py:30](../../tests/analysis/test_sigma_calibrator.py#L30) |  |
| `test_first_fails_in_one_world_second_passes` | test | `test_first_fails_in_one_world_second_passes` | [tests/analysis/test_sigma_calibrator.py:36](../../tests/analysis/test_sigma_calibrator.py#L36) |  |
| `test_first_match_ladder` | test | `test_first_match_ladder` | [tests/d2a/test_b_rules_decide.py:302](../../tests/d2a/test_b_rules_decide.py#L302) | All of rules 5-9 hold; removing one condition at a time walks down the order. |
| `test_first_non_pass_stops_and_later_gates_not_run` | test | `test_first_non_pass_stops_and_later_gates_not_run` | [tests/k4b/test_b_flow.py:172](../../tests/k4b/test_b_flow.py#L172) |  |
| `test_first_step` | test | `test_first_step` | [tests/experiment/test_s6_rules.py:11](../../tests/experiment/test_s6_rules.py#L11) |  |
| `test_first_token_ok_is_check_first_token_not_raising` | test | `test_first_token_ok_is_check_first_token_not_raising` | [tests/c1prime/test_b_registry.py:160](../../tests/c1prime/test_b_registry.py#L160) |  |
| `test_first_token_p_detects_bias` | test | `test_first_token_p_detects_bias` | [tests/experiment/test_x4b2.py:54](../../tests/experiment/test_x4b2.py#L54) |  |
| `test_fit_chart_bar_radius_and_edges` | test | `test_fit_chart_bar_radius_and_edges` | [tests/circle_history/test_chart.py:175](../../tests/circle_history/test_chart.py#L175) |  |
| `test_fit_chart_certificates_explicit` | test | `test_fit_chart_certificates_explicit` | [tests/circle_history/test_chart.py:206](../../tests/circle_history/test_chart.py#L206) |  |
| `test_fit_chart_cocycle_matches_ripser_rows` | test | `test_fit_chart_cocycle_matches_ripser_rows` | [tests/circle_history/test_chart.py:192](../../tests/circle_history/test_chart.py#L192) |  |
| `test_fit_chart_duplicate_counts_at_distance_zero` | test | `test_fit_chart_duplicate_counts_at_distance_zero` | [tests/circle_history/test_chart.py:241](../../tests/circle_history/test_chart.py#L241) |  |
| `test_fit_chart_exists` | test | `test_fit_chart_exists` | [tests/circle_history/test_chart.py:163](../../tests/circle_history/test_chart.py#L163) |  |
| `test_fit_chart_extension_scale_recomputed` | test | `test_fit_chart_extension_scale_recomputed` | [tests/circle_history/test_chart.py:232](../../tests/circle_history/test_chart.py#L232) |  |
| `test_fit_chart_invalid_inputs` | test | `test_fit_chart_invalid_inputs` | [tests/circle_history/test_chart.py:253](../../tests/circle_history/test_chart.py#L253) |  |
| `test_fit_chart_phi_ascending_up_to_reflection` | test | `test_fit_chart_phi_ascending_up_to_reflection` | [tests/circle_history/test_chart.py:220](../../tests/circle_history/test_chart.py#L220) |  |
| `test_fit_chart_spread_clusters_positive_bandwidth` | test | `test_fit_chart_spread_clusters_positive_bandwidth` | [tests/circle_history/test_chart.py:287](../../tests/circle_history/test_chart.py#L287) |  |
| `test_fit_chart_zero_bandwidth_unresolved` | test | `test_fit_chart_zero_bandwidth_unresolved` | [tests/circle_history/test_chart.py:278](../../tests/circle_history/test_chart.py#L278) |  |
| `test_fit_decoder_recipe_and_equivalence` | test | `test_fit_decoder_recipe_and_equivalence` | [tests/c2_readout/test_b_fwl_l1.py:206](../../tests/c2_readout/test_b_fwl_l1.py#L206) |  |
| `test_fit_gauge_alignment_zero_unresolved` | test | `test_fit_gauge_alignment_zero_unresolved` | [tests/circle_history/test_chart.py:329](../../tests/circle_history/test_chart.py#L329) |  |
| `test_fit_gauge_exact_tie_chooses_plus` | test | `test_fit_gauge_exact_tie_chooses_plus` | [tests/circle_history/test_chart.py:321](../../tests/circle_history/test_chart.py#L321) |  |
| `test_fit_gauge_invalid_inputs` | test | `test_fit_gauge_invalid_inputs` | [tests/circle_history/test_chart.py:335](../../tests/circle_history/test_chart.py#L335) |  |
| `test_fit_gauge_sign_shift_alignment` | test | `test_fit_gauge_sign_shift_alignment` | [tests/circle_history/test_chart.py:300](../../tests/circle_history/test_chart.py#L300) |  |
| `test_fixed_forecasts` | test | `test_fixed_forecasts` | [tests/hws/test_a_budget.py:52](../../tests/hws/test_a_budget.py#L52) |  |
| `test_fixture1_first_solve_error_propagation_independent_exact` | test | `test_fixture1_first_solve_error_propagation_independent_exact` | [tests/c2_readout/test_a_gls.py:167](../../tests/c2_readout/test_a_gls.py#L167) |  |
| `test_fixture1_module_bound_covers_the_true_error_and_is_not_accepted` | test | `test_fixture1_module_bound_covers_the_true_error_and_is_not_accepted` | [tests/c2_readout/test_a_gls.py:187](../../tests/c2_readout/test_a_gls.py#L187) |  |
| `test_fixture2_independent_r_c_and_r_g_perturbations_lemma_gr` | test | `test_fixture2_independent_r_c_and_r_g_perturbations_lemma_gr` | [tests/c2_readout/test_a_gls.py:215](../../tests/c2_readout/test_a_gls.py#L215) |  |
| `test_fixture2_perturbed_operator_residual_r_g` | test | `test_fixture2_perturbed_operator_residual_r_g` | [tests/c2_readout/test_a_gls.py:200](../../tests/c2_readout/test_a_gls.py#L200) |  |
| `test_fixture3_lemma_inv_bound_and_non_acceptance` | test | `test_fixture3_lemma_inv_bound_and_non_acceptance` | [tests/c2_readout/test_a_gls.py:237](../../tests/c2_readout/test_a_gls.py#L237) |  |
| `test_fixture4_euclidean_case_conditioning_differs_from_whitened` | test | `test_fixture4_euclidean_case_conditioning_differs_from_whitened` | [tests/c2_readout/test_a_gls.py:258](../../tests/c2_readout/test_a_gls.py#L258) |  |
| `test_fixture5_reduced_precision_enclosure_and_trap` | test | `test_fixture5_reduced_precision_enclosure_and_trap` | [tests/c2_readout/test_a_gls.py:278](../../tests/c2_readout/test_a_gls.py#L278) |  |
| `test_fixture6_eps_p_enters_delta_p_and_the_gate` | test | `test_fixture6_eps_p_enters_delta_p_and_the_gate` | [tests/c2_readout/test_a_gls.py:302](../../tests/c2_readout/test_a_gls.py#L302) |  |
| `test_fixture_arithmetic` | test | `test_fixture_arithmetic` | [tests/circle_history/test_cochain_lift.py:157](../../tests/circle_history/test_cochain_lift.py#L157) |  |
| `test_fixture_defects` | test | `test_fixture_defects` | [tests/circle_history/test_cochain_chart_v24.py:117](../../tests/circle_history/test_cochain_chart_v24.py#L117) |  |
| `test_fixture_has_one_487_component_and_25_singletons` | test | `test_fixture_has_one_487_component_and_25_singletons` | [tests/c1prime/test_a_chart_lcc512.py:131](../../tests/c1prime/test_a_chart_lcc512.py#L131) |  |
| `test_fixture_hmm_is_exactly_stationary_and_asymmetric` | test | `test_fixture_hmm_is_exactly_stationary_and_asymmetric` | [tests/circle_history/test_scores_precision.py:70](../../tests/circle_history/test_scores_precision.py#L70) |  |
| `test_fixture_is_a_valid_rational_process` | test | `test_fixture_is_a_valid_rational_process` | [tests/hws/test_a_identities.py:251](../../tests/hws/test_a_identities.py#L251) |  |
| `test_fixture_is_exactly_symmetric` | test | `test_fixture_is_exactly_symmetric` | [tests/c1prime/test_a_oracle.py:132](../../tests/c1prime/test_a_oracle.py#L132) |  |
| `test_fixture_is_seedtree_only_and_positive` | test | `test_fixture_is_seedtree_only_and_positive` | [tests/experiment/test_x5g1_scorebench_smoke.py:26](../../tests/experiment/test_x5g1_scorebench_smoke.py#L26) |  |
| `test_fixture_with_more_than_1024_rows_is_incomplete` | test | `test_fixture_with_more_than_1024_rows_is_incomplete` | [tests/k4b/test_b_registry_rules.py:130](../../tests/k4b/test_b_registry_rules.py#L130) |  |
| `test_fixtures_in_a_basetemp_segment_are_not_scanned` | test | `test_fixtures_in_a_basetemp_segment_are_not_scanned` | [tests/k4b/test_b_registry_rules.py:115](../../tests/k4b/test_b_registry_rules.py#L115) |  |
| `test_fixtures_raise_what_they_claim` | test | `test_fixtures_raise_what_they_claim` | [tests/c1prime/test_a_exceptions.py:123](../../tests/c1prime/test_a_exceptions.py#L123) |  |
| `test_float64_determinism_vector_t_and_normalisation` | test | `test_float64_determinism_vector_t_and_normalisation` | [tests/x6_stage1/test_a_eval.py:111](../../tests/x6_stage1/test_a_eval.py#L111) |  |
| `test_float_model_is_the_production_kernels` | test | `test_float_model_is_the_production_kernels` | [tests/d1_seam/test_d1_seam.py:173](../../tests/d1_seam/test_d1_seam.py#L173) |  |
| `test_floors_both_ways` | test | `test_floors_both_ways` | [tests/hws/test_a_classify.py:119](../../tests/hws/test_a_classify.py#L119) |  |
| `test_fold_mse_is_unweighted_mean_over_sorted_panels` | test | `test_fold_mse_is_unweighted_mean_over_sorted_panels` | [tests/experiment/test_x4f_probe.py:140](../../tests/experiment/test_x4f_probe.py#L140) |  |
| `test_forbidden` | test | `test_forbidden` | [tests/x6_stage1/test_b_chain_ops.py:337](../../tests/x6_stage1/test_b_chain_ops.py#L337) |  |
| `test_forced_state_is_a_plus_B_times_the_phase_difference` | test | `test_forced_state_is_a_plus_B_times_the_phase_difference` | [tests/c1prime/test_b_fwl.py:205](../../tests/c1prime/test_b_fwl.py#L205) |  |
| `test_forcing_general_and_explicit_z` | test | `test_forcing_general_and_explicit_z` | [tests/hwsb/test_a_learning.py:325](../../tests/hwsb/test_a_learning.py#L325) |  |
| `test_forcing_oracle_model_has_positive_lower_bound` | test | `test_forcing_oracle_model_has_positive_lower_bound` | [tests/hwsb/test_a_learning.py:314](../../tests/hwsb/test_a_learning.py#L314) |  |
| `test_forcing_ratio_undefined_without_gain` | test | `test_forcing_ratio_undefined_without_gain` | [tests/hwsb/test_a_learning.py:333](../../tests/hwsb/test_a_learning.py#L333) |  |
| `test_forcing_suffix_model_has_zero_gain` | test | `test_forcing_suffix_model_has_zero_gain` | [tests/hwsb/test_a_learning.py:302](../../tests/hwsb/test_a_learning.py#L302) |  |
| `test_foreign_tree_is_refused` | test | `test_foreign_tree_is_refused` | [tests/hwsb/test_b_streams.py:93](../../tests/hwsb/test_b_streams.py#L93) |  |
| `test_four_gates_pass_on_consistent_snapshot` | test | `test_four_gates_pass_on_consistent_snapshot` | [tests/x6_stage1/test_b_ingest_bundle.py:182](../../tests/x6_stage1/test_b_ingest_bundle.py#L182) |  |
| `test_four_state_path_known_answer` | test | `test_four_state_path_known_answer` | [tests/analysis/test_horizon.py:61](../../tests/analysis/test_horizon.py#L61) |  |
| `test_fps_overlap_builds_on_tiny_world` | test | `test_fps_overlap_builds_on_tiny_world` | [tests/process/test_controls.py:148](../../tests/process/test_controls.py#L148) |  |
| `test_frac_beyond_is_strict` | test | `test_frac_beyond_is_strict` | [tests/c1prime/test_a_eligibility_support.py:126](../../tests/c1prime/test_a_eligibility_support.py#L126) |  |
| `test_fraction_ranks` | test | `test_fraction_ranks` | [tests/c2_readout/test_a_inference.py:368](../../tests/c2_readout/test_a_inference.py#L368) |  |
| `test_frame_mean_is_an_ordered_left_to_right_sum` | test | `test_frame_mean_is_an_ordered_left_to_right_sum` | [tests/c1prime/test_b_identities.py:270](../../tests/c1prime/test_b_identities.py#L270) |  |
| `test_freeze_field_set_and_implementation_hash` | test | `test_freeze_field_set_and_implementation_hash` | [tests/hwsb/test_b_records.py:317](../../tests/hwsb/test_b_records.py#L317) |  |
| `test_freeze_fields_and_implementation_hash` | test | `test_freeze_fields_and_implementation_hash` | [tests/hws/test_b_records.py:202](../../tests/hws/test_b_records.py#L202) |  |
| `test_fresh_b4_low_basis` | test | `test_fresh_b4_low_basis` | [tests/k4b/test_a_width_b4.py:196](../../tests/k4b/test_a_width_b4.py#L196) | FRESH_B4_LOW (implementation choice 7) is set iff the guard status is not PASS, i.e. |
| `test_fresh_fraction_rule` | test | `test_fresh_fraction_rule` | [tests/c1prime/test_b_precision.py:144](../../tests/c1prime/test_b_precision.py#L144) |  |
| `test_fresh_full_clearance_clears` | test | `test_fresh_full_clearance_clears` | [tests/experiment/test_x5g1t_usage.py:195](../../tests/experiment/test_x5g1t_usage.py#L195) |  |
| `test_fresh_full_clearance_continues_and_clears` | test | `test_fresh_full_clearance_continues_and_clears` | [tests/experiment/test_x5g1t_usage.py:343](../../tests/experiment/test_x5g1t_usage.py#L343) |  |
| `test_fresh_id_collision_refuses_without_draw` | test | `test_fresh_id_collision_refuses_without_draw` | [tests/experiment/test_x5g1t_integration.py:286](../../tests/experiment/test_x5g1t_integration.py#L286) |  |
| `test_frozen_builder_unions_and_hashes_sources` | test | `test_frozen_builder_unions_and_hashes_sources` | [tests/c1prime_registry/test_registry_builder.py:74](../../tests/c1prime_registry/test_registry_builder.py#L74) |  |
| `test_frozen_constants` | test | `test_frozen_constants` | [tests/experiment/test_x5g1_lineage.py:63](../../tests/experiment/test_x5g1_lineage.py#L63) |  |
| `test_frozen_file_set_change_refused` | test | `test_frozen_file_set_change_refused` | [tests/circle_history/test_builder_guards.py:165](../../tests/circle_history/test_builder_guards.py#L165) |  |
| `test_frozen_files_bind_project_dependencies` | test | `test_frozen_files_bind_project_dependencies` | [tests/circle_history/test_builder_v24_runtime.py:192](../../tests/circle_history/test_builder_v24_runtime.py#L192) |  |
| `test_frozen_orientation_rotates_every_harmonic_by_k_theta` | test | `test_frozen_orientation_rotates_every_harmonic_by_k_theta` | [tests/c2_readout/test_a_oracle.py:249](../../tests/c2_readout/test_a_oracle.py#L249) |  |
| `test_frozen_thresholds_stop_inconclusive_at_coverage` | test | `test_frozen_thresholds_stop_inconclusive_at_coverage` | [tests/circle_history/test_builder_e2e.py:164](../../tests/circle_history/test_builder_e2e.py#L164) |  |
| `test_full_log_tables_spot_checks` | test | `test_full_log_tables_spot_checks` | [tests/x6_stage1/test_a_numerics.py:137](../../tests/x6_stage1/test_a_numerics.py#L137) |  |
| `test_full_staged_run` | test | `test_full_staged_run` | [tests/experiment/test_x5g1t_e2e.py:26](../../tests/experiment/test_x5g1t_e2e.py#L26) |  |
| `test_full_walk_in_order` | test | `test_full_walk_in_order` | [tests/c2_readout/test_b_policy.py:71](../../tests/c2_readout/test_b_policy.py#L71) |  |
| `test_future_maps_four_state_path` | test | `test_future_maps_four_state_path` | [tests/experiment/test_x4b.py:37](../../tests/experiment/test_x4b.py#L37) |  |
| `test_future_maps_routes_agree_and_checks_pass` | test | `test_future_maps_routes_agree_and_checks_pass` | [tests/experiment/test_x4b.py:26](../../tests/experiment/test_x4b.py#L26) |  |
| `test_fwl_design_column_order` | test | `test_fwl_design_column_order` | [tests/c1prime/test_b_fwl.py:70](../../tests/c1prime/test_b_fwl.py#L70) |  |
| `test_fwl_matches_the_frisch_waugh_lovell_formula_with_noise` | test | `test_fwl_matches_the_frisch_waugh_lovell_formula_with_noise` | [tests/c1prime/test_b_fwl.py:104](../../tests/c1prime/test_b_fwl.py#L104) |  |
| `test_fwl_recovers_a_known_B_noiselessly` | test | `test_fwl_recovers_a_known_B_noiselessly` | [tests/c1prime/test_b_fwl.py:77](../../tests/c1prime/test_b_fwl.py#L77) |  |
| `test_fwl_recovers_known_B_with_K3` | test | `test_fwl_recovers_known_B_with_K3` | [tests/c2_readout/test_b_fwl_l1.py:65](../../tests/c2_readout/test_b_fwl_l1.py#L65) |  |
| `test_g0_fix_gate_passes` | test | `test_g0_fix_gate_passes` | [tests/d2a/test_a_targets.py:143](../../tests/d2a/test_a_targets.py#L143) |  |
| `test_g0_item_i_accepts_the_exact_copy` | test | `test_g0_item_i_accepts_the_exact_copy` | [tests/c2_readout/test_b_lineage.py:183](../../tests/c2_readout/test_b_lineage.py#L183) |  |
| `test_g0_refuses_a_protocol_copy_mismatch` | test | `test_g0_refuses_a_protocol_copy_mismatch` | [tests/c2_readout/test_b_lineage.py:172](../../tests/c2_readout/test_b_lineage.py#L172) |  |
| `test_g0_tpl_gate_passes` | test | `test_g0_tpl_gate_passes` | [tests/d2a/test_a_templates.py:152](../../tests/d2a/test_a_templates.py#L152) |  |
| `test_g1_check_is_scale_invariant_and_rejects_a_non_self_adjoint_projector` | test | `test_g1_check_is_scale_invariant_and_rejects_a_non_self_adjoint_projector` | [tests/c2_readout/test_a_gls.py:114](../../tests/c2_readout/test_a_gls.py#L114) |  |
| `test_g1_identities_and_closed_form` | test | `test_g1_identities_and_closed_form` | [tests/c2_readout/test_a_readout.py:293](../../tests/c2_readout/test_a_readout.py#L293) |  |
| `test_g1_ignores_validation_targets_for_selection` | test | `test_g1_ignores_validation_targets_for_selection` | [tests/experiment/test_x4f_gates_smoke.py:70](../../tests/experiment/test_x4f_gates_smoke.py#L70) |  |
| `test_g2_interchange_takes_code_from_arm1_and_the_rest_from_arm2` | test | `test_g2_interchange_takes_code_from_arm1_and_the_rest_from_arm2` | [tests/c2_readout/test_a_readout.py:327](../../tests/c2_readout/test_a_readout.py#L327) |  |
| `test_g3_monte_carlo_within_state_covariance_vanishes` | test | `test_g3_monte_carlo_within_state_covariance_vanishes` | [tests/c2_readout/test_a_readout.py:342](../../tests/c2_readout/test_a_readout.py#L342) |  |
| `test_g5_reference_inputs_and_tolerances` | test | `test_g5_reference_inputs_and_tolerances` | [tests/x6_stage0/test_x6_stage0_dp.py:186](../../tests/x6_stage0/test_x6_stage0_dp.py#L186) |  |
| `test_G_hat_is_the_ordered_C3_kernel` | test | `test_G_hat_is_the_ordered_C3_kernel` | [tests/c1prime/test_a_oracle_named.py:110](../../tests/c1prime/test_a_oracle_named.py#L110) |  |
| `test_G_named_uses_the_permuted_canonical_arrays` | test | `test_G_named_uses_the_permuted_canonical_arrays` | [tests/c1prime/test_a_oracle_named.py:123](../../tests/c1prime/test_a_oracle_named.py#L123) |  |
| `test_gain_identities_kl_rows_equal_entropy_differences` | test | `test_gain_identities_kl_rows_equal_entropy_differences` | [tests/hws/test_a_identities.py:290](../../tests/hws/test_a_identities.py#L290) |  |
| `test_garbage_evidence_time_never_clears` | test | `test_garbage_evidence_time_never_clears` | [tests/experiment/test_x5g1t_usage.py:267](../../tests/experiment/test_x5g1t_usage.py#L267) |  |
| `test_gate_G2_values` | test | `test_gate_G2_values` | [tests/d1_seam/test_d1_seam.py:342](../../tests/d1_seam/test_d1_seam.py#L342) |  |
| `test_gate_order_equals_protocol_section_7` | test | `test_gate_order_equals_protocol_section_7` | [tests/c2_readout/test_b_policy.py:66](../../tests/c2_readout/test_b_policy.py#L66) |  |
| `test_gate_order_is_the_section_16_order` | test | `test_gate_order_is_the_section_16_order` | [tests/c1prime/test_a_gates.py:57](../../tests/c1prime/test_a_gates.py#L57) |  |
| `test_gate_order_release_a` | test | `test_gate_order_release_a` | [tests/k4b/test_b_flow.py:130](../../tests/k4b/test_b_flow.py#L130) |  |
| `test_gate_pass_fail_unresolved` | test | `test_gate_pass_fail_unresolved` | [tests/x6_stage1/test_a_numerics.py:353](../../tests/x6_stage1/test_a_numerics.py#L353) |  |
| `test_gate_quantities_batching_is_rowwise` | test | `test_gate_quantities_batching_is_rowwise` | [tests/experiment/test_x5g1_lineage.py:217](../../tests/experiment/test_x5g1_lineage.py#L217) |  |
| `test_gate_quantities_lawful_nonnegative` | test | `test_gate_quantities_lawful_nonnegative` | [tests/experiment/test_x5g1_lineage.py:187](../../tests/experiment/test_x5g1_lineage.py#L187) |  |
| `test_gate_quantities_match_reference_filter` | test | `test_gate_quantities_match_reference_filter` | [tests/experiment/test_x5g1_lineage.py:175](../../tests/experiment/test_x5g1_lineage.py#L175) |  |
| `test_gate_quantities_permutation_equivalence` | test | `test_gate_quantities_permutation_equivalence` | [tests/experiment/test_x5g1_lineage.py:195](../../tests/experiment/test_x5g1_lineage.py#L195) |  |
| `test_gates_begin_only_in_order` | test | `test_gates_begin_only_in_order` | [tests/c1prime/test_a_gates.py:114](../../tests/c1prime/test_a_gates.py#L114) |  |
| `test_gates_end_to_end` | test | `test_gates_end_to_end` | [tests/experiment/test_x4f_gates_smoke.py:45](../../tests/experiment/test_x4f_gates_smoke.py#L45) |  |
| `test_gates_pass` | test | `test_gates_pass` | [tests/d1_seam/test_d1_seam.py:339](../../tests/d1_seam/test_d1_seam.py#L339) |  |
| `test_gauge_isolation_from_validation_arrays` | test | `test_gauge_isolation_from_validation_arrays` | [tests/circle_history/test_chart.py:362](../../tests/circle_history/test_chart.py#L362) |  |
| `test_gauge_points_are_the_cstar_landmarks_only` | test | `test_gauge_points_are_the_cstar_landmarks_only` | [tests/c1prime/test_a_chart_lcc512.py:215](../../tests/c1prime/test_a_chart_lcc512.py#L215) |  |
| `test_generic_hmm_has_certificate_and_tolerance_rows` | test | `test_generic_hmm_has_certificate_and_tolerance_rows` | [tests/analysis/test_horizon.py:81](../../tests/analysis/test_horizon.py#L81) |  |
| `test_geometry_helpers_are_never_called` | test | `test_geometry_helpers_are_never_called` | [tests/d1_seam/test_d1_seam.py:230](../../tests/d1_seam/test_d1_seam.py#L230) |  |
| `test_geometry_helpers_are_never_called` | test | `test_geometry_helpers_are_never_called` | [tests/x2a_stage0/test_x2a_stage0.py:363](../../tests/x2a_stage0/test_x2a_stage0.py#L363) |  |
| `test_giant_486_of_512_stops_after_the_pre_raise_record` | test | `test_giant_486_of_512_stops_after_the_pre_raise_record` | [tests/c1prime/test_a_chart.py:244](../../tests/c1prime/test_a_chart.py#L244) | Item 3 (fail side): GIANT_BELOW_0.95, with the step-5 record persisted first. |
| `test_giant_487_passes_486_fails` | test | `test_giant_487_passes_486_fails` | [tests/k4b/test_b_charts.py:347](../../tests/k4b/test_b_charts.py#L347) |  |
| `test_giant_487_passes_and_restriction_keeps_cstar_only` | test | `test_giant_487_passes_and_restriction_keeps_cstar_only` | [tests/c1prime/test_a_chart_lcc512.py:139](../../tests/c1prime/test_a_chart_lcc512.py#L139) |  |
| `test_giant_largest_component_ties_to_smallest_index` | test | `test_giant_largest_component_ties_to_smallest_index` | [tests/c1prime/test_a_chart.py:219](../../tests/c1prime/test_a_chart.py#L219) |  |
| `test_giant_pass_integer_rule` | test | `test_giant_pass_integer_rule` | [tests/c1prime/test_a_chart.py:238](../../tests/c1prime/test_a_chart.py#L238) |  |
| `test_global_failed_beats_everything` | test | `test_global_failed_beats_everything` | [tests/analysis/test_x5_context.py:98](../../tests/analysis/test_x5_context.py#L98) |  |
| `test_global_failed_writes_tables_without_save` | test | `test_global_failed_writes_tables_without_save` | [tests/experiment/test_x5g1_export_integration.py:197](../../tests/experiment/test_x5g1_export_integration.py#L197) |  |
| `test_global_inconclusive` | test | `test_global_inconclusive` | [tests/analysis/test_x5_context.py:140](../../tests/analysis/test_x5_context.py#L140) |  |
| `test_graph_metric_uses_manhattan` | test | `test_graph_metric_uses_manhattan` | [tests/process/test_overlap.py:157](../../tests/process/test_overlap.py#L157) |  |
| `test_grid_completions_lie_in_bounds` | test | `test_grid_completions_lie_in_bounds` | [tests/k4b/test_a_theorem_a.py:139](../../tests/k4b/test_a_theorem_a.py#L139) |  |
| `test_grid_constant` | test | `test_grid_constant` | [tests/experiment/test_x4f_probe.py:61](../../tests/experiment/test_x4f_probe.py#L61) |  |
| `test_grid_event_accepts_numpy_bool_array` | test | `test_grid_event_accepts_numpy_bool_array` | [tests/analysis/test_x5_endpoint.py:138](../../tests/analysis/test_x5_endpoint.py#L138) |  |
| `test_grid_event_default_grid_is_GRID` | test | `test_grid_event_default_grid_is_GRID` | [tests/analysis/test_x5_endpoint.py:143](../../tests/analysis/test_x5_endpoint.py#L143) |  |
| `test_grid_event_is_frozen` | test | `test_grid_event_is_frozen` | [tests/analysis/test_x5_endpoint.py:160](../../tests/analysis/test_x5_endpoint.py#L160) |  |
| `test_grid_event_length_mismatch` | test | `test_grid_event_length_mismatch` | [tests/analysis/test_x5_endpoint.py:171](../../tests/analysis/test_x5_endpoint.py#L171) |  |
| `test_grid_event_non_increasing_grid` | test | `test_grid_event_non_increasing_grid` | [tests/analysis/test_x5_endpoint.py:197](../../tests/analysis/test_x5_endpoint.py#L197) |  |
| `test_grid_event_rejects_non_bool` | test | `test_grid_event_rejects_non_bool` | [tests/analysis/test_x5_endpoint.py:177](../../tests/analysis/test_x5_endpoint.py#L177) |  |
| `test_grid_event_rejects_none_incomplete_curve` | test | `test_grid_event_rejects_none_incomplete_curve` | [tests/analysis/test_x5_endpoint.py:184](../../tests/analysis/test_x5_endpoint.py#L184) |  |
| `test_grid_event_short_grid` | test | `test_grid_event_short_grid` | [tests/analysis/test_x5_endpoint.py:191](../../tests/analysis/test_x5_endpoint.py#L191) |  |
| `test_grid_event_small_custom_grids` | test | `test_grid_event_small_custom_grids` | [tests/analysis/test_x5_endpoint.py:148](../../tests/analysis/test_x5_endpoint.py#L148) |  |
| `test_grid_has_225_worlds_in_the_stated_order` | test | `test_grid_has_225_worlds_in_the_stated_order` | [tests/hws/test_b_worlds.py:78](../../tests/hws/test_b_worlds.py#L78) |  |
| `test_guard_admits_stage3_and_ignores_other_pools` | test | `test_guard_admits_stage3_and_ignores_other_pools` | [tests/d2a/test_a_world.py:230](../../tests/d2a/test_a_world.py#L230) |  |
| `test_guard_exception_propagates` | test | `test_guard_exception_propagates` | [tests/circle_history/test_cochain_lift.py:270](../../tests/circle_history/test_cochain_lift.py#L270) |  |
| `test_h0_star` | test | `test_h0_star` | [tests/x2a_stage0/test_x2a_stage0_ph.py:274](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L274) |  |
| `test_h3_compare_branches_and_zero_posterior_entries` | test | `test_h3_compare_branches_and_zero_posterior_entries` | [tests/c1prime/test_a_oracle.py:270](../../tests/c1prime/test_a_oracle.py#L270) |  |
| `test_h4_class` | test | `test_h4_class` | [tests/experiment/test_s6_rules.py:23](../../tests/experiment/test_s6_rules.py#L23) |  |
| `test_h4_failed_gate_or_no_rise_is_inconclusive` | test | `test_h4_failed_gate_or_no_rise_is_inconclusive` | [tests/experiment/test_s6_rules.py:37](../../tests/experiment/test_s6_rules.py#L37) |  |
| `test_h4_rejected_by_any_violation_with_gates_passed` | test | `test_h4_rejected_by_any_violation_with_gates_passed` | [tests/experiment/test_s6_rules.py:33](../../tests/experiment/test_s6_rules.py#L33) |  |
| `test_h4_supported_needs_all_three_consistent` | test | `test_h4_supported_needs_all_three_consistent` | [tests/experiment/test_s6_rules.py:27](../../tests/experiment/test_s6_rules.py#L27) |  |
| `test_h5_guard` | test | `test_h5_guard` | [tests/c1prime/test_b_cert_guards.py:157](../../tests/c1prime/test_b_cert_guards.py#L157) |  |
| `test_h5_pass_headroom_and_guard_band` | test | `test_h5_pass_headroom_and_guard_band` | [tests/c1prime/test_b_precision.py:158](../../tests/c1prime/test_b_precision.py#L158) |  |
| `test_h5_wrapper_index_stream_equals_bootstrap_profile` | test | `test_h5_wrapper_index_stream_equals_bootstrap_profile` | [tests/c1prime/test_b_inference.py:165](../../tests/c1prime/test_b_inference.py#L165) |  |
| `test_h5_wrapper_uses_the_tree_kernel_on_real_valued_data` | test | `test_h5_wrapper_uses_the_tree_kernel_on_real_valued_data` | [tests/c1prime/test_b_inference.py:175](../../tests/c1prime/test_b_inference.py#L175) |  |
| `test_h_star_closed_forms_and_chain_identity` | test | `test_h_star_closed_forms_and_chain_identity` | [tests/d1_seam/test_d1_seam.py:248](../../tests/d1_seam/test_d1_seam.py#L248) |  |
| `test_haar_frames_are_the_seeded_streams` | test | `test_haar_frames_are_the_seeded_streams` | [tests/c1prime/test_b_frames.py:94](../../tests/c1prime/test_b_frames.py#L94) |  |
| `test_haar_frames_streams` | test | `test_haar_frames_streams` | [tests/c2_readout/test_b_policy.py:342](../../tests/c2_readout/test_b_policy.py#L342) |  |
| `test_hand_computed_known_answers` | test | `test_hand_computed_known_answers` | [tests/oracle_profile/test_oracle_profile.py:154](../../tests/oracle_profile/test_oracle_profile.py#L154) | Exact rational model (T_Q, E_Q, PI_Q): posteriors derived by hand. |
| `test_hand_example_1000_then_fail` | test | `test_hand_example_1000_then_fail` | [tests/analysis/test_x5_endpoint.py:100](../../tests/analysis/test_x5_endpoint.py#L100) |  |
| `test_hand_example_4500_edge_observed` | test | `test_hand_example_4500_edge_observed` | [tests/analysis/test_x5_endpoint.py:116](../../tests/analysis/test_x5_endpoint.py#L116) |  |
| `test_hand_example_first_pass_4750_censored` | test | `test_hand_example_first_pass_4750_censored` | [tests/analysis/test_x5_endpoint.py:121](../../tests/analysis/test_x5_endpoint.py#L121) |  |
| `test_hand_example_non_monotone_2500` | test | `test_hand_example_non_monotone_2500` | [tests/analysis/test_x5_endpoint.py:95](../../tests/analysis/test_x5_endpoint.py#L95) |  |
| `test_hand_example_tau_zero` | test | `test_hand_example_tau_zero` | [tests/analysis/test_x5_endpoint.py:106](../../tests/analysis/test_x5_endpoint.py#L106) |  |
| `test_hand_values_mixed_beliefs_and_non_integer_positions` | test | `test_hand_values_mixed_beliefs_and_non_integer_positions` | [tests/analysis/test_x4f_targets.py:41](../../tests/analysis/test_x4f_targets.py#L41) |  |
| `test_handoff_json_with_or_without_bom_passes` | test | `test_handoff_json_with_or_without_bom_passes` | [tests/k4b/test_b_registry_fixes.py:66](../../tests/k4b/test_b_registry_fixes.py#L66) |  |
| `test_handoff_record_keeps_exactly_the_contract_keys` | test | `test_handoff_record_keeps_exactly_the_contract_keys` | [tests/hwsb/test_a_outcomes.py:322](../../tests/hwsb/test_a_outcomes.py#L322) |  |
| `test_handoff_record_refuses_missing_key_and_nested_forbidden` | test | `test_handoff_record_refuses_missing_key_and_nested_forbidden` | [tests/hwsb/test_a_outcomes.py:329](../../tests/hwsb/test_a_outcomes.py#L329) |  |
| `test_handoff_rows_keeps_x6_valid_lists` | test | `test_handoff_rows_keeps_x6_valid_lists` | [tests/x6_stage1/test_b_seed_pool_reg.py:276](../../tests/x6_stage1/test_b_seed_pool_reg.py#L276) |  |
| `test_handoff_rows_malformed_json_is_incomplete` | test | `test_handoff_rows_malformed_json_is_incomplete` | [tests/x6_stage1/test_b_seed_pool_reg.py:269](../../tests/x6_stage1/test_b_seed_pool_reg.py#L269) |  |
| `test_handoff_scan_finds_token_lists_and_ignores_others` | test | `test_handoff_scan_finds_token_lists_and_ignores_others` | [tests/c1prime_registry/test_registry_builder.py:61](../../tests/c1prime_registry/test_registry_builder.py#L61) |  |
| `test_harmonic_dependent_when_the_k1_variant_changes_the_category` | test | `test_harmonic_dependent_when_the_k1_variant_changes_the_category` | [tests/c2_readout/test_a_scope.py:301](../../tests/c2_readout/test_a_scope.py#L301) |  |
| `test_harmonics_column_order` | test | `test_harmonics_column_order` | [tests/c2_readout/test_b_fwl_l1.py:57](../../tests/c2_readout/test_b_fwl_l1.py#L57) |  |
| `test_head_without_subprocess_matches_git` | test | `test_head_without_subprocess_matches_git` | [tests/circle_history/test_builder_guards.py:113](../../tests/circle_history/test_builder_guards.py#L113) |  |
| `test_heads_read_ln_final_out_and_forward_returns_requested_hooks` | test | `test_heads_read_ln_final_out_and_forward_returns_requested_hooks` | [tests/learner/test_multihorizon.py:151](../../tests/learner/test_multihorizon.py#L151) |  |
| `test_held_and_continued_run_equals_unheld_run_bitwise` | test | `test_held_and_continued_run_equals_unheld_run_bitwise` | [tests/hwsb/test_b_hold.py:170](../../tests/hwsb/test_b_hold.py#L170) |  |
| `test_hellinger_bounds_and_negative_error` | test | `test_hellinger_bounds_and_negative_error` | [tests/analysis/test_horizon.py:119](../../tests/analysis/test_horizon.py#L119) |  |
| `test_hellinger_hand_values` | test | `test_hellinger_hand_values` | [tests/topology/test_metrics.py:45](../../tests/topology/test_metrics.py#L45) |  |
| `test_helmert_basis_orthonormal_sum_zero` | test | `test_helmert_basis_orthonormal_sum_zero` | [tests/analysis/test_horizon.py:41](../../tests/analysis/test_horizon.py#L41) |  |
| `test_helmert_formula_orthonormal_and_orthogonal_to_ones` | test | `test_helmert_formula_orthonormal_and_orthogonal_to_ones` | [tests/c2_readout/test_a_readout.py:71](../../tests/c2_readout/test_a_readout.py#L71) |  |
| `test_history_digests_known_values_and_shape` | test | `test_history_digests_known_values_and_shape` | [tests/circle_history/test_scores_precision.py:108](../../tests/circle_history/test_scores_precision.py#L108) |  |
| `test_history_file_inside_the_os_root_counts_as_covered` | test | `test_history_file_inside_the_os_root_counts_as_covered` | [tests/k4b/test_b_registry_rules.py:274](../../tests/k4b/test_b_registry_rules.py#L274) |  |
| `test_history_generator_is_the_registered_seedtree_stream` | test | `test_history_generator_is_the_registered_seedtree_stream` | [tests/k4b/test_b_data.py:99](../../tests/k4b/test_b_data.py#L99) |  |
| `test_history_inventory_lists_every_file_with_sha256` | test | `test_history_inventory_lists_every_file_with_sha256` | [tests/hwsb/test_b_registry.py:82](../../tests/hwsb/test_b_registry.py#L82) |  |
| `test_history_law_sums_to_one` | test | `test_history_law_sums_to_one` | [tests/k4b/test_a_prop1.py:106](../../tests/k4b/test_a_prop1.py#L106) |  |
| `test_history_outside_a_basetemp_segment_is_incomplete` | test | `test_history_outside_a_basetemp_segment_is_incomplete` | [tests/k4b/test_b_registry_rules.py:157](../../tests/k4b/test_b_registry_rules.py#L157) |  |
| `test_history_stream_and_sequence_ids` | test | `test_history_stream_and_sequence_ids` | [tests/c1prime/test_b_registry.py:67](../../tests/c1prime/test_b_registry.py#L67) |  |
| `test_history_streams_differ_by_split_and_block` | test | `test_history_streams_differ_by_split_and_block` | [tests/k4b/test_b_data.py:107](../../tests/k4b/test_b_data.py#L107) |  |
| `test_history_streams_match_the_seedtree_scopes` | test | `test_history_streams_match_the_seedtree_scopes` | [tests/hws/test_b_oracle.py:75](../../tests/hws/test_b_oracle.py#L75) |  |
| `test_history_table_cal_columns_by_sequence_id` | test | `test_history_table_cal_columns_by_sequence_id` | [tests/k4b/test_b_data.py:195](../../tests/k4b/test_b_data.py#L195) |  |
| `test_history_table_digests_of_H_and_both_donors` | test | `test_history_table_digests_of_H_and_both_donors` | [tests/c1prime/test_b_registry.py:109](../../tests/c1prime/test_b_registry.py#L109) |  |
| `test_history_table_val_landmarks` | test | `test_history_table_val_landmarks` | [tests/k4b/test_b_data.py:217](../../tests/k4b/test_b_data.py#L217) |  |
| `test_history_table_with_the_y_donor` | test | `test_history_table_with_the_y_donor` | [tests/c2_readout/test_b_registry.py:123](../../tests/c2_readout/test_b_registry.py#L123) |  |
| `test_hmm_is_asymmetric_stationary_and_positive` | test | `test_hmm_is_asymmetric_stationary_and_positive` | [tests/k4b/test_a_prop1.py:97](../../tests/k4b/test_a_prop1.py#L97) |  |
| `test_hmm_is_asymmetric_with_exact_nonuniform_stationary_pi` | test | `test_hmm_is_asymmetric_with_exact_nonuniform_stationary_pi` | [tests/oracle_profile/test_oracle_profile.py:103](../../tests/oracle_profile/test_oracle_profile.py#L103) |  |
| `test_hold_modes_hold` | test | `test_hold_modes_hold` | [tests/experiment/test_x5g1t_usage_files.py:241](../../tests/experiment/test_x5g1t_usage_files.py#L241) |  |
| `test_hold_released_by_sleep_completes` | test | `test_hold_released_by_sleep_completes` | [tests/experiment/test_x5g1t_integration.py:196](../../tests/experiment/test_x5g1t_integration.py#L196) |  |
| `test_hold_report_refuses_overwrite` | test | `test_hold_report_refuses_overwrite` | [tests/hwsb/test_b_hold.py:140](../../tests/hwsb/test_b_hold.py#L140) |  |
| `test_hold_with_disk_failure_kills_and_keeps_hold` | test | `test_hold_with_disk_failure_kills_and_keeps_hold` | [tests/k4b/test_b_meter.py:219](../../tests/k4b/test_b_meter.py#L219) |  |
| `test_hold_with_overdue_operation_kills_and_keeps_hold` | test | `test_hold_with_overdue_operation_kills_and_keeps_hold` | [tests/k4b/test_b_meter.py:209](../../tests/k4b/test_b_meter.py#L209) |  |
| `test_hold_without_resource_failure_never_kills` | test | `test_hold_without_resource_failure_never_kills` | [tests/k4b/test_b_meter.py:199](../../tests/k4b/test_b_meter.py#L199) |  |
| `test_hold_writes_report_without_dev_ce_and_continue_exempts` | test | `test_hold_writes_report_without_dev_ce_and_continue_exempts` | [tests/hwsb/test_b_hold.py:108](../../tests/hwsb/test_b_hold.py#L108) |  |
| `test_holds` | test | `test_holds` | [tests/oracle_profile/test_builder_controls.py:115](../../tests/oracle_profile/test_builder_controls.py#L115) |  |
| `test_hook_at_site_shows_replacement` | test | `test_hook_at_site_shows_replacement` | [tests/learner/test_patch.py:149](../../tests/learner/test_patch.py#L149) |  |
| `test_hooks_downstream_are_after_the_patch` | test | `test_hooks_downstream_are_after_the_patch` | [tests/learner/test_patch.py:162](../../tests/learner/test_patch.py#L162) |  |
| `test_horizon_outside_2_3_is_invalid_config` | test | `test_horizon_outside_2_3_is_invalid_config` | [tests/learner/test_multihorizon.py:172](../../tests/learner/test_multihorizon.py#L172) |  |
| `test_hws_collisions_are_reported_not_gating` | test | `test_hws_collisions_are_reported_not_gating` | [tests/hwsb/test_b_streams.py:393](../../tests/hwsb/test_b_streams.py#L393) |  |
| `test_I01_s1_core_config` | test | `test_I01_s1_core_config` | [tests/integration/test_s1.py:23](../../tests/integration/test_s1.py#L23) |  |
| `test_I02_s2_mini_end_to_end` | test | `test_I02_s2_mini_end_to_end` | [tests/integration/test_s2_mini.py:39](../../tests/integration/test_s2_mini.py#L39) |  |
| `test_I04_scrambled_latents_do_not_reach_learner` | test | `test_I04_scrambled_latents_do_not_reach_learner` | [tests/integration/test_leakage_end_to_end.py:17](../../tests/integration/test_leakage_end_to_end.py#L17) |  |
| `test_I06_rerun_identity` | test | `test_I06_rerun_identity` | [tests/integration/test_rerun_identity.py:15](../../tests/integration/test_rerun_identity.py#L15) |  |
| `test_i1_fails_for_a_prefix_dependent_function` | test | `test_i1_fails_for_a_prefix_dependent_function` | [tests/hws/test_a_identities.py:266](../../tests/hws/test_a_identities.py#L266) |  |
| `test_i1_suffix_functions_have_zero_covariance_with_r_k` | test | `test_i1_suffix_functions_have_zero_covariance_with_r_k` | [tests/hws/test_a_identities.py:259](../../tests/hws/test_a_identities.py#L259) |  |
| `test_i2_i4_and_d4_positive` | test | `test_i2_i4_and_d4_positive` | [tests/hws/test_a_identities.py:280](../../tests/hws/test_a_identities.py#L280) |  |
| `test_i3_v_k_identity_and_monotone` | test | `test_i3_v_k_identity_and_monotone` | [tests/hws/test_a_identities.py:273](../../tests/hws/test_a_identities.py#L273) |  |
| `test_iat_affine_invariance` | test | `test_iat_affine_invariance` | [tests/analysis/test_x5_kernel.py:168](../../tests/analysis/test_x5_kernel.py#L168) |  |
| `test_iat_constant_function_undefined` | test | `test_iat_constant_function_undefined` | [tests/analysis/test_x5_kernel.py:183](../../tests/analysis/test_x5_kernel.py#L183) |  |
| `test_iat_eigenfunction_of_lazy_cycle` | test | `test_iat_eigenfunction_of_lazy_cycle` | [tests/analysis/test_x5_kernel.py:158](../../tests/analysis/test_x5_kernel.py#L158) |  |
| `test_iat_reducible` | test | `test_iat_reducible` | [tests/analysis/test_x5_kernel.py:191](../../tests/analysis/test_x5_kernel.py#L191) |  |
| `test_iat_two_state_hand_value` | test | `test_iat_two_state_hand_value` | [tests/analysis/test_x5_kernel.py:146](../../tests/analysis/test_x5_kernel.py#L146) |  |
| `test_iat_two_state_p01_is_nine` | test | `test_iat_two_state_p01_is_nine` | [tests/analysis/test_x5_kernel.py:153](../../tests/analysis/test_x5_kernel.py#L153) |  |
| `test_identical_emission_has_no_beyond_k_information` | test | `test_identical_emission_has_no_beyond_k_information` | [tests/hws/test_b_oracle.py:263](../../tests/hws/test_b_oracle.py#L263) |  |
| `test_identical_observation_sets_in_both_stores` | test | `test_identical_observation_sets_in_both_stores` | [tests/hwsb/test_b_e4path.py:112](../../tests/hwsb/test_b_e4path.py#L112) |  |
| `test_identity_fields` | test | `test_identity_fields` | [tests/circle_history/test_reference_cache.py:84](../../tests/circle_history/test_reference_cache.py#L84) |  |
| `test_identity_on_shorter_sequence` | test | `test_identity_on_shorter_sequence` | [tests/learner/test_patch.py:80](../../tests/learner/test_patch.py#L80) |  |
| `test_identity_passes_without_touching_any_payload` | test | `test_identity_passes_without_touching_any_payload` | [tests/hws/test_b_kc1.py:224](../../tests/hws/test_b_kc1.py#L224) |  |
| `test_identity_patch_bitwise_at_three_sites` | test | `test_identity_patch_bitwise_at_three_sites` | [tests/c2_readout/test_b_patch.py:112](../../tests/c2_readout/test_b_patch.py#L112) |  |
| `test_identity_patch_detects_a_one_entry_change` | test | `test_identity_patch_detects_a_one_entry_change` | [tests/c2_readout/test_b_patch.py:125](../../tests/c2_readout/test_b_patch.py#L125) |  |
| `test_identity_replacement_reproduces_all_logits` | test | `test_identity_replacement_reproduces_all_logits` | [tests/learner/test_patch.py:68](../../tests/learner/test_patch.py#L68) |  |
| `test_identity_report_returns_no_arrays` | test | `test_identity_report_returns_no_arrays` | [tests/circle_history/test_adapter.py:277](../../tests/circle_history/test_adapter.py#L277) |  |
| `test_identity_report_runs_every_lineage_check` | test | `test_identity_report_runs_every_lineage_check` | [tests/circle_history/test_adapter.py:287](../../tests/circle_history/test_adapter.py#L287) |  |
| `test_ill_conditioned_solver_gap_is_within_bound` | test | `test_ill_conditioned_solver_gap_is_within_bound` | [tests/c1prime/test_c_ridge_tolerance.py:38](../../tests/c1prime/test_c_ridge_tolerance.py#L38) |  |
| `test_implementation_mismatch_still_fails` | test | `test_implementation_mismatch_still_fails` | [tests/c1prime/test_c_ridge_tolerance.py:49](../../tests/c1prime/test_c_ridge_tolerance.py#L49) |  |
| `test_impossible_history_sets_invalid_without_raising` | test | `test_impossible_history_sets_invalid_without_raising` | [tests/experiment/test_x5g1_lineage.py:227](../../tests/experiment/test_x5g1_lineage.py#L227) |  |
| `test_impossible_strings_are_exactly_those_with_two_consecutive_twos` | test | `test_impossible_strings_are_exactly_those_with_two_consecutive_twos` | [tests/oracle_profile/test_oracle_profile.py:115](../../tests/oracle_profile/test_oracle_profile.py#L115) |  |
| `test_incomplete_before_any_scientific_outcome` | test | `test_incomplete_before_any_scientific_outcome` | [tests/hwsb/test_a_outcomes.py:145](../../tests/hwsb/test_a_outcomes.py#L145) |  |
| `test_index_out_of_range` | test | `test_index_out_of_range` | [tests/learner/test_patch.py:241](../../tests/learner/test_patch.py#L241) |  |
| `test_index_out_of_range_for_short_sequence` | test | `test_index_out_of_range_for_short_sequence` | [tests/learner/test_patch.py:246](../../tests/learner/test_patch.py#L246) |  |
| `test_indicator_form_sign_and_eligible_row_ratio` | test | `test_indicator_form_sign_and_eligible_row_ratio` | [tests/c2_readout/test_a_partition.py:339](../../tests/c2_readout/test_a_partition.py#L339) |  |
| `test_ineligible_world_with_passing_bounds_is_not_unresolved` | test | `test_ineligible_world_with_passing_bounds_is_not_unresolved` | [tests/hws/test_a_outcomes.py:209](../../tests/hws/test_a_outcomes.py#L209) |  |
| `test_infinite_mass_rejected` | test | `test_infinite_mass_rejected` | [tests/oracle_profile/test_builder_kernels.py:49](../../tests/oracle_profile/test_builder_kernels.py#L49) |  |
| `test_init_and_batch_order_identical_across_arms` | test | `test_init_and_batch_order_identical_across_arms` | [tests/x6_stage1/test_b_train_chain.py:233](../../tests/x6_stage1/test_b_train_chain.py#L233) |  |
| `test_init_gauge_integrity_defect_stops` | test | `test_init_gauge_integrity_defect_stops` | [tests/k4b/test_b_charts.py:228](../../tests/k4b/test_b_charts.py#L228) |  |
| `test_init_ledger_refuses_any_role_but_production` | test | `test_init_ledger_refuses_any_role_but_production` | [tests/k4b/test_b_charts.py:178](../../tests/k4b/test_b_charts.py#L178) |  |
| `test_init_ledger_three_production_claims` | test | `test_init_ledger_three_production_claims` | [tests/k4b/test_b_charts.py:188](../../tests/k4b/test_b_charts.py#L188) |  |
| `test_init_qualifier_strict_exact` | test | `test_init_qualifier_strict_exact` | [tests/k4b/test_b_endpoint.py:274](../../tests/k4b/test_b_endpoint.py#L274) |  |
| `test_init_shared_code_fail_technical_stops_immediately` | test | `test_init_shared_code_fail_technical_stops_immediately` | [tests/k4b/test_b_charts.py:218](../../tests/k4b/test_b_charts.py#L218) |  |
| `test_init_unavailable_is_non_gating` | test | `test_init_unavailable_is_non_gating` | [tests/k4b/test_b_charts.py:201](../../tests/k4b/test_b_charts.py#L201) |  |
| `test_inline_bootstrap_refuses_modified_bundle` | test | `test_inline_bootstrap_refuses_modified_bundle` | [tests/x6_stage1/test_b_nb_s0_ops.py:175](../../tests/x6_stage1/test_b_nb_s0_ops.py#L175) |  |
| `test_inputs_and_replacement_not_mutated` | test | `test_inputs_and_replacement_not_mutated` | [tests/learner/test_patch.py:202](../../tests/learner/test_patch.py#L202) |  |
| `test_inputs_are_not_mutated` | test | `test_inputs_are_not_mutated` | [tests/oracle_profile/test_oracle_profile_traps.py:264](../../tests/oracle_profile/test_oracle_profile_traps.py#L264) |  |
| `test_inputs_not_mutated` | test | `test_inputs_not_mutated` | [tests/experiment/test_x4f_probe.py:115](../../tests/experiment/test_x4f_probe.py#L115) |  |
| `test_integer_certificate_defect_is_technical` | test | `test_integer_certificate_defect_is_technical` | [tests/c1prime/test_a_chart_exceptions.py:185](../../tests/c1prime/test_a_chart_exceptions.py#L185) |  |
| `test_integer_dtypes_and_numpy_integer_K_are_accepted` | test | `test_integer_dtypes_and_numpy_integer_K_are_accepted` | [tests/oracle_profile/test_oracle_profile_traps.py:253](../../tests/oracle_profile/test_oracle_profile_traps.py#L253) |  |
| `test_interaction_fixture_is_orthogonal_to_the_additive_regressors` | test | `test_interaction_fixture_is_orthogonal_to_the_additive_regressors` | [tests/c2_readout/test_a_scope.py:197](../../tests/c2_readout/test_a_scope.py#L197) |  |
| `test_interrupted_stage_without_gate_record_is_replayed_under_rule` | test | `test_interrupted_stage_without_gate_record_is_replayed_under_rule` | [tests/k4b/test_b_rerun.py:157](../../tests/k4b/test_b_rerun.py#L157) |  |
| `test_interval_estimate` | test | `test_interval_estimate` | [tests/experiment/test_x5g1t_runtime_boundary.py:149](../../tests/experiment/test_x5g1t_runtime_boundary.py#L149) |  |
| `test_interval_rule_three_way_at_its_boundaries` | test | `test_interval_rule_three_way_at_its_boundaries` | [tests/c1prime/test_a_oracle.py:249](../../tests/c1prime/test_a_oracle.py#L249) |  |
| `test_invalid_accepted_map_fails_closed` | test | `test_invalid_accepted_map_fails_closed` | [tests/analysis/test_x4f_family_maintenance.py:30](../../tests/analysis/test_x4f_family_maintenance.py#L30) |  |
| `test_invalid_flag_beats_values` | test | `test_invalid_flag_beats_values` | [tests/analysis/test_x5_context.py:85](../../tests/analysis/test_x5_context.py#L85) |  |
| `test_invalid_kernel_plus_weak_arm_is_inconclusive` | test | `test_invalid_kernel_plus_weak_arm_is_inconclusive` | [tests/analysis/test_x5_context.py:114](../../tests/analysis/test_x5_context.py#L114) |  |
| `test_invalid_landmark_ids_are_a_technical_failure` | test | `test_invalid_landmark_ids_are_a_technical_failure` | [tests/c1prime/test_a_chart.py:294](../../tests/c1prime/test_a_chart.py#L294) | Input defects keep FAIL_TECHNICAL even at the chart boundary. |
| `test_invalid_ledger_raises_at_construction_and_keeps_bytes` | test | `test_invalid_ledger_raises_at_construction_and_keeps_bytes` | [tests/experiment/test_x5g1_export_integration.py:242](../../tests/experiment/test_x5g1_export_integration.py#L242) |  |
| `test_invalid_predictive_is_inconclusive` | test | `test_invalid_predictive_is_inconclusive` | [tests/analysis/test_x5_context.py:131](../../tests/analysis/test_x5_context.py#L131) |  |
| `test_invalid_request` | test | `test_invalid_request` | [tests/oracle_profile/test_builder_controls.py:89](../../tests/oracle_profile/test_builder_controls.py#L89) |  |
| `test_invalid_scoring_release_denies_panel_3_before_any_load` | test | `test_invalid_scoring_release_denies_panel_3_before_any_load` | [tests/circle_history/test_adapter.py:229](../../tests/circle_history/test_adapter.py#L229) |  |
| `test_invalid_unknown_control_and_usage` | test | `test_invalid_unknown_control_and_usage` | [tests/oracle_profile/test_builder_controls.py:104](../../tests/oracle_profile/test_builder_controls.py#L104) |  |
| `test_invalid_unreadable_and_task_bytes` | test | `test_invalid_unreadable_and_task_bytes` | [tests/oracle_profile/test_builder_controls.py:94](../../tests/oracle_profile/test_builder_controls.py#L94) |  |
| `test_inventory_admits_an_unlisted_empty_directory_alone` | test | `test_inventory_admits_an_unlisted_empty_directory_alone` | [tests/c2_readout/test_b_registry.py:222](../../tests/c2_readout/test_b_registry.py#L222) |  |
| `test_inventory_diff_detects_new_history_identity_and_obs_root` | test | `test_inventory_diff_detects_new_history_identity_and_obs_root` | [tests/hwsb/test_b_records.py:184](../../tests/hwsb/test_b_records.py#L184) |  |
| `test_inventory_diff_new_top_level_directory_is_new` | test | `test_inventory_diff_new_top_level_directory_is_new` | [tests/hwsb/test_b_records.py:198](../../tests/hwsb/test_b_records.py#L198) |  |
| `test_inventory_diff_unchanged_root_is_ok` | test | `test_inventory_diff_unchanged_root_is_ok` | [tests/hwsb/test_b_records.py:177](../../tests/hwsb/test_b_records.py#L177) |  |
| `test_inventory_includes_superseded_tree` | test | `test_inventory_includes_superseded_tree` | [tests/hwsb/test_b_registry.py:90](../../tests/hwsb/test_b_registry.py#L90) |  |
| `test_inventory_is_recursive_and_counts_worktrees_and_temp_dirs` | test | `test_inventory_is_recursive_and_counts_worktrees_and_temp_dirs` | [tests/k4b/test_b_registry.py:82](../../tests/k4b/test_b_registry.py#L82) |  |
| `test_inventory_registered_copy_passes` | test | `test_inventory_registered_copy_passes` | [tests/x6_stage1/test_b_seed_pool_reg.py:293](../../tests/x6_stage1/test_b_seed_pool_reg.py#L293) |  |
| `test_inventory_snapshot_lists_kinds` | test | `test_inventory_snapshot_lists_kinds` | [tests/hwsb/test_b_records.py:168](../../tests/hwsb/test_b_records.py#L168) |  |
| `test_inventory_unclassified_x6_directory_is_incomplete` | test | `test_inventory_unclassified_x6_directory_is_incomplete` | [tests/x6_stage1/test_b_seed_pool_reg.py:319](../../tests/x6_stage1/test_b_seed_pool_reg.py#L319) |  |
| `test_inventory_unregistered_npy_is_incomplete` | test | `test_inventory_unregistered_npy_is_incomplete` | [tests/x6_stage1/test_b_seed_pool_reg.py:301](../../tests/x6_stage1/test_b_seed_pool_reg.py#L301) |  |
| `test_inventory_unregistered_observation_set_root_is_incomplete` | test | `test_inventory_unregistered_observation_set_root_is_incomplete` | [tests/x6_stage1/test_b_seed_pool_reg.py:310](../../tests/x6_stage1/test_b_seed_pool_reg.py#L310) |  |
| `test_inventory_violations_and_admitted_empty_directory` | test | `test_inventory_violations_and_admitted_empty_directory` | [tests/c2_readout/test_b_registry.py:207](../../tests/c2_readout/test_b_registry.py#L207) |  |
| `test_irrelevant_warning_does_not_block` | test | `test_irrelevant_warning_does_not_block` | [tests/experiment/test_x5g1t_usage.py:135](../../tests/experiment/test_x5g1t_usage.py#L135) |  |
| `test_is_connected_true_false` | test | `test_is_connected_true_false` | [tests/analysis/test_x5_kernel.py:63](../../tests/analysis/test_x5_kernel.py#L63) |  |
| `test_is_connected_uses_either_direction` | test | `test_is_connected_uses_either_direction` | [tests/analysis/test_x5_kernel.py:70](../../tests/analysis/test_x5_kernel.py#L70) |  |
| `test_isqrt_bracket_property_random` | test | `test_isqrt_bracket_property_random` | [tests/k4b/test_a_lemma_n.py:92](../../tests/k4b/test_a_lemma_n.py#L92) |  |
| `test_isqrt_perfect_squares_are_exact` | test | `test_isqrt_perfect_squares_are_exact` | [tests/k4b/test_a_lemma_n.py:69](../../tests/k4b/test_a_lemma_n.py#L69) |  |
| `test_isqrt_sqrt2_digits_and_bracket` | test | `test_isqrt_sqrt2_digits_and_bracket` | [tests/k4b/test_a_lemma_n.py:76](../../tests/k4b/test_a_lemma_n.py#L76) |  |
| `test_isqrt_tiny_values` | test | `test_isqrt_tiny_values` | [tests/k4b/test_a_lemma_n.py:84](../../tests/k4b/test_a_lemma_n.py#L84) |  |
| `test_isqrt_zero` | test | `test_isqrt_zero` | [tests/k4b/test_a_lemma_n.py:64](../../tests/k4b/test_a_lemma_n.py#L64) |  |
| `test_jensen_bias_at_most_root_variance` | test | `test_jensen_bias_at_most_root_variance` | [tests/oracle_profile/test_oracle_profile_kernels.py:170](../../tests/oracle_profile/test_oracle_profile_kernels.py#L170) |  |
| `test_job_paths_test_and_store_kinds` | test | `test_job_paths_test_and_store_kinds` | [tests/hwsb/test_b_meter_law.py:106](../../tests/hwsb/test_b_meter_law.py#L106) |  |
| `test_join_failure_is_join_error_never_unresolved` | test | `test_join_failure_is_join_error_never_unresolved` | [tests/circle_history/test_controls.py:155](../../tests/circle_history/test_controls.py#L155) |  |
| `test_join_mismatch_fails_technical` | test | `test_join_mismatch_fails_technical` | [tests/circle_history/test_builder_e2e.py:210](../../tests/circle_history/test_builder_e2e.py#L210) | Spec v2.4 item 1: a technical identity mismatch is FAIL_TECHNICAL (overall FAIL). |
| `test_joint_fwl_is_not_sequential_residualisation` | test | `test_joint_fwl_is_not_sequential_residualisation` | [tests/c1prime/test_b_fwl.py:91](../../tests/c1prime/test_b_fwl.py#L91) |  |
| `test_joint_order_and_marginals_catch_bT2E_and_transposed_order` | test | `test_joint_order_and_marginals_catch_bT2E_and_transposed_order` | [tests/analysis/test_horizon.py:104](../../tests/analysis/test_horizon.py#L104) |  |
| `test_js_on_toy_laws_and_series_branch` | test | `test_js_on_toy_laws_and_series_branch` | [tests/x2a_stage0/test_x2a_stage0.py:292](../../tests/x2a_stage0/test_x2a_stage0.py#L292) |  |
| `test_json_atomic_canonical_and_exclusive` | test | `test_json_atomic_canonical_and_exclusive` | [tests/x6_stage1/test_b_train_chain.py:303](../../tests/x6_stage1/test_b_train_chain.py#L303) |  |
| `test_json_str_step_on_disk_fails_identity` | test | `test_json_str_step_on_disk_fails_identity` | [tests/k4b/test_b_h1_meta.py:352](../../tests/k4b/test_b_h1_meta.py#L352) |  |
| `test_k4_landmark_checks_are_applied` | test | `test_k4_landmark_checks_are_applied` | [tests/chart_diag/test_chart_diag.py:72](../../tests/chart_diag/test_chart_diag.py#L72) |  |
| `test_k4_meter_bind_is_not_imported_by_the_c1_binding` | test | `test_k4_meter_bind_is_not_imported_by_the_c1_binding` | [tests/c1prime/test_a_release_meter.py:208](../../tests/c1prime/test_a_release_meter.py#L208) |  |
| `test_k_blocks` | test | `test_k_blocks` | [tests/c1prime/test_b_precision.py:128](../../tests/c1prime/test_b_precision.py#L128) |  |
| `test_k_blocks_never_exceeds_five_for_admissible_fractions` | test | `test_k_blocks_never_exceeds_five_for_admissible_fractions` | [tests/c1prime/test_b_precision.py:134](../../tests/c1prime/test_b_precision.py#L134) |  |
| `test_k_y_sign_rule` | test | `test_k_y_sign_rule` | [tests/c2_readout/test_b_policy.py:268](../../tests/c2_readout/test_b_policy.py#L268) |  |
| `test_k_y_sign_rule_with_the_tie_going_to_minus_one` | test | `test_k_y_sign_rule_with_the_tie_going_to_minus_one` | [tests/c2_readout/test_a_oracle.py:102](../../tests/c2_readout/test_a_oracle.py#L102) |  |
| `test_kappa_is_known_exactly` | test | `test_kappa_is_known_exactly` | [tests/k4b/test_a_lemma_t.py:92](../../tests/k4b/test_a_lemma_t.py#L92) |  |
| `test_kappa_nu_population_covariance_and_eligible_mean` | test | `test_kappa_nu_population_covariance_and_eligible_mean` | [tests/c1prime/test_a_eligibility_support.py:76](../../tests/c1prime/test_a_eligibility_support.py#L76) |  |
| `test_kappa_x1_matches_the_written_formula` | test | `test_kappa_x1_matches_the_written_formula` | [tests/c2_readout/test_b_patch.py:294](../../tests/c2_readout/test_b_patch.py#L294) |  |
| `test_kc9_float_floor_contract_key` | test | `test_kc9_float_floor_contract_key` | [tests/hws/test_a_stats.py:255](../../tests/hws/test_a_stats.py#L255) |  |
| `test_kc9_float_floor_rule` | test | `test_kc9_float_floor_rule` | [tests/hws/test_a_stats.py:273](../../tests/hws/test_a_stats.py#L273) |  |
| `test_kc9_row_constant_summary` | test | `test_kc9_row_constant_summary` | [tests/hws/test_a_stats.py:280](../../tests/hws/test_a_stats.py#L280) |  |
| `test_kernel_matches_fraction_formula` | test | `test_kernel_matches_fraction_formula` | [tests/x2a_stage0/test_x2a_stage0.py:167](../../tests/x2a_stage0/test_x2a_stage0.py#L167) |  |
| `test_kernel_rejects_abs_a_ge_1` | test | `test_kernel_rejects_abs_a_ge_1` | [tests/process/test_conductance.py:235](../../tests/process/test_conductance.py#L235) |  |
| `test_kernel_rejects_bad_state_order` | test | `test_kernel_rejects_bad_state_order` | [tests/process/test_conductance.py:216](../../tests/process/test_conductance.py#L216) |  |
| `test_kernel_rejects_invalid_model` | test | `test_kernel_rejects_invalid_model` | [tests/oracle_profile/test_builder_kernels.py:43](../../tests/oracle_profile/test_builder_kernels.py#L43) |  |
| `test_kl_hand_value_and_invalid_q` | test | `test_kl_hand_value_and_invalid_q` | [tests/experiment/test_x5g1t_lineage_oracle.py:300](../../tests/experiment/test_x5g1t_lineage_oracle.py#L300) |  |
| `test_kl_rows_hand_values_in_nats` | test | `test_kl_rows_hand_values_in_nats` | [tests/analysis/test_x4f_scores.py:105](../../tests/analysis/test_x4f_scores.py#L105) |  |
| `test_kl_rows_mean_equals_context_gain_on_random_rows` | test | `test_kl_rows_mean_equals_context_gain_on_random_rows` | [tests/hws/test_a_identities.py:391](../../tests/hws/test_a_identities.py#L391) |  |
| `test_kl_rows_numerical_failures` | test | `test_kl_rows_numerical_failures` | [tests/hws/test_a_identities.py:377](../../tests/hws/test_a_identities.py#L377) |  |
| `test_kl_rows_shape_mismatch` | test | `test_kl_rows_shape_mismatch` | [tests/analysis/test_x4f_scores.py:129](../../tests/analysis/test_x4f_scores.py#L129) |  |
| `test_kl_rows_undefined_when_q_zero_where_p_positive` | test | `test_kl_rows_undefined_when_q_zero_where_p_positive` | [tests/analysis/test_x4f_scores.py:122](../../tests/analysis/test_x4f_scores.py#L122) |  |
| `test_kl_rows_zero_p_terms_contribute_nothing_even_where_q_is_zero` | test | `test_kl_rows_zero_p_terms_contribute_nothing_even_where_q_is_zero` | [tests/analysis/test_x4f_scores.py:114](../../tests/analysis/test_x4f_scores.py#L114) |  |
| `test_kl_rows_zero_support_convention_and_entropy_rows` | test | `test_kl_rows_zero_support_convention_and_entropy_rows` | [tests/hws/test_a_identities.py:365](../../tests/hws/test_a_identities.py#L365) |  |
| `test_kl_rows_zeros_and_infinity` | test | `test_kl_rows_zeros_and_infinity` | [tests/x6_stage1/test_a_eval.py:150](../../tests/x6_stage1/test_a_eval.py#L150) |  |
| `test_kl_zero_and_support_rules` | test | `test_kl_zero_and_support_rules` | [tests/experiment/test_x5g1_scorebench_smoke.py:48](../../tests/experiment/test_x5g1_scorebench_smoke.py#L48) |  |
| `test_kneser_ney_hand_value_and_rows_normalised` | test | `test_kneser_ney_hand_value_and_rows_normalised` | [tests/prediction/test_ngram.py:59](../../tests/prediction/test_ngram.py#L59) |  |
| `test_known_zero_builders` | test | `test_known_zero_builders` | [tests/hws/test_b_worlds.py:294](../../tests/hws/test_b_worlds.py#L294) |  |
| `test_kreg2_reader_equals_k4b_load` | test | `test_kreg2_reader_equals_k4b_load` | [tests/x6_stage1/test_b_seed_pool_reg.py:353](../../tests/x6_stage1/test_b_seed_pool_reg.py#L353) |  |
| `test_kreg2_reader_refuses_mismatch` | test | `test_kreg2_reader_refuses_mismatch` | [tests/x6_stage1/test_b_seed_pool_reg.py:377](../../tests/x6_stage1/test_b_seed_pool_reg.py#L377) |  |
| `test_L01_causality_every_position` | test | `test_L01_causality_every_position` | [tests/learner/test_model.py:30](../../tests/learner/test_model.py#L30) |  |
| `test_L01b_causal_mask_failed_raised_at_construction` | test | `test_L01b_causal_mask_failed_raised_at_construction` | [tests/learner/test_model.py:41](../../tests/learner/test_model.py#L41) |  |
| `test_L02_shapes_and_hook_names` | test | `test_L02_shapes_and_hook_names` | [tests/learner/test_model.py:51](../../tests/learner/test_model.py#L51) |  |
| `test_L03_resid_to_logits_exact` | test | `test_L03_resid_to_logits_exact` | [tests/learner/test_model.py:66](../../tests/learner/test_model.py#L66) |  |
| `test_L04_overfit_eight_sequences` | test | `test_L04_overfit_eight_sequences` | [tests/learner/test_training.py:25](../../tests/learner/test_training.py#L25) |  |
| `test_L05_step0_is_initial_weights_and_runs_repeat` | test | `test_L05_step0_is_initial_weights_and_runs_repeat` | [tests/learner/test_training.py:39](../../tests/learner/test_training.py#L39) |  |
| `test_L05b_global_rng_untouched` | test | `test_L05b_global_rng_untouched` | [tests/learner/test_training.py:59](../../tests/learner/test_training.py#L59) |  |
| `test_L06_save_load_reproduces_logits` | test | `test_L06_save_load_reproduces_logits` | [tests/learner/test_checkpoint.py:40](../../tests/learner/test_checkpoint.py#L40) |  |
| `test_L06b_optimizer_flags_and_byte_determinism` | test | `test_L06b_optimizer_flags_and_byte_determinism` | [tests/learner/test_checkpoint.py:57](../../tests/learner/test_checkpoint.py#L57) |  |
| `test_L06c_load_model_rejects_bad_checkpoint` | test | `test_L06c_load_model_rejects_bad_checkpoint` | [tests/learner/test_checkpoint.py:73](../../tests/learner/test_checkpoint.py#L73) |  |
| `test_L07_non_public_dataset_is_leakage` | test | `test_L07_non_public_dataset_is_leakage` | [tests/learner/test_training.py:67](../../tests/learner/test_training.py#L67) |  |
| `test_L08_nan_loss_raises` | test | `test_L08_nan_loss_raises` | [tests/learner/test_training.py:78](../../tests/learner/test_training.py#L78) |  |
| `test_L09_no_forbidden_imports` | test | `test_L09_no_forbidden_imports` | [tests/learner/test_model.py:77](../../tests/learner/test_model.py#L77) |  |
| `test_L10_schedule_and_optimizer_only_at_final` | test | `test_L10_schedule_and_optimizer_only_at_final` | [tests/learner/test_training.py:94](../../tests/learner/test_training.py#L94) |  |
| `test_L10b_invalid_schedules_rejected` | test | `test_L10b_invalid_schedules_rejected` | [tests/learner/test_training.py:106](../../tests/learner/test_training.py#L106) |  |
| `test_l1_denominator_fixtures_fail_link` | test | `test_l1_denominator_fixtures_fail_link` | [tests/c2_readout/test_b_fwl_l1.py:302](../../tests/c2_readout/test_b_fwl_l1.py#L302) |  |
| `test_l1_thresholds_exact` | test | `test_l1_thresholds_exact` | [tests/c2_readout/test_b_fwl_l1.py:295](../../tests/c2_readout/test_b_fwl_l1.py#L295) |  |
| `test_ladder_passes_at_3072` | test | `test_ladder_passes_at_3072` | [tests/k4b/test_a_ranks_ladder.py:235](../../tests/k4b/test_a_ranks_ladder.py#L235) |  |
| `test_ladder_passes_at_6144` | test | `test_ladder_passes_at_6144` | [tests/k4b/test_a_ranks_ladder.py:244](../../tests/k4b/test_a_ranks_ladder.py#L244) | SD 0.2: MDE fails at 3,072 (0.2082 > 0.02) and passes at 6,144 (0.0177). |
| `test_ladder_picks_the_smallest_passing_N` | test | `test_ladder_picks_the_smallest_passing_N` | [tests/c1prime/test_b_precision.py:100](../../tests/c1prime/test_b_precision.py#L100) |  |
| `test_ladder_pilot_defaults_are_stage_b` | test | `test_ladder_pilot_defaults_are_stage_b` | [tests/hwsb/test_a_ladder.py:197](../../tests/hwsb/test_a_ladder.py#L197) |  |
| `test_ladder_pilot_equals_k4b_ladder` | test | `test_ladder_pilot_equals_k4b_ladder` | [tests/hwsb/test_a_ladder.py:163](../../tests/hwsb/test_a_ladder.py#L163) |  |
| `test_ladder_pilot_stage_b_rule` | test | `test_ladder_pilot_stage_b_rule` | [tests/hwsb/test_a_ladder.py:177](../../tests/hwsb/test_a_ladder.py#L177) |  |
| `test_ladder_pilot_width_diagnostic_with_d_bar` | test | `test_ladder_pilot_width_diagnostic_with_d_bar` | [tests/hwsb/test_a_ladder.py:208](../../tests/hwsb/test_a_ladder.py#L208) |  |
| `test_ladder_underpowered` | test | `test_ladder_underpowered` | [tests/k4b/test_a_ranks_ladder.py:265](../../tests/k4b/test_a_ranks_ladder.py#L265) |  |
| `test_ladder_underpowered_when_no_N_passes` | test | `test_ladder_underpowered_when_no_N_passes` | [tests/c1prime/test_b_precision.py:116](../../tests/c1prime/test_b_precision.py#L116) |  |
| `test_landmark_ids_are_20_digit_zero_padded_strings` | test | `test_landmark_ids_are_20_digit_zero_padded_strings` | [tests/c1prime/test_a_chart.py:167](../../tests/c1prime/test_a_chart.py#L167) |  |
| `test_large_negative_placebo_passes_y1_and_licence_states_only_the_inequality` | test | `test_large_negative_placebo_passes_y1_and_licence_states_only_the_inequality` | [tests/c2_readout/test_a_scope.py:234](../../tests/c2_readout/test_a_scope.py#L234) |  |
| `test_latch_from_coordinator_hold_and_stop_precedence` | test | `test_latch_from_coordinator_hold_and_stop_precedence` | [tests/oracle_profile/test_builder_controls.py:221](../../tests/oracle_profile/test_builder_controls.py#L221) |  |
| `test_latch_without_fresh_full_clearance_holds` | test | `test_latch_without_fresh_full_clearance_holds` | [tests/experiment/test_x5g1t_usage.py:339](../../tests/experiment/test_x5g1t_usage.py#L339) |  |
| `test_latched_kind_just_below_threshold_clears` | test | `test_latched_kind_just_below_threshold_clears` | [tests/experiment/test_x5g1t_usage.py:257](../../tests/experiment/test_x5g1t_usage.py#L257) |  |
| `test_latent_field_added_to_observation_subclass_is_leakage` | test | `test_latent_field_added_to_observation_subclass_is_leakage` | [tests/dataset/test_public.py:30](../../tests/dataset/test_public.py#L30) |  |
| `test_later_stage_accepted_prefix_plus_own_lines` | test | `test_later_stage_accepted_prefix_plus_own_lines` | [tests/c2_readout/test_b_fwl_l1.py:383](../../tests/c2_readout/test_b_fwl_l1.py#L383) |  |
| `test_latest_report_per_gate_wins` | test | `test_latest_report_per_gate_wins` | [tests/experiment/test_runner.py:73](../../tests/experiment/test_runner.py#L73) |  |
| `test_lattice_states_and_rejections` | test | `test_lattice_states_and_rejections` | [tests/circle_history/test_process_law.py:163](../../tests/circle_history/test_process_law.py#L163) |  |
| `test_law_bound_default_arguments_are_w_star` | test | `test_law_bound_default_arguments_are_w_star` | [tests/hwsb/test_b_meter_law.py:276](../../tests/hwsb/test_b_meter_law.py#L276) |  |
| `test_law_bound_report_nonterminating_logit` | test | `test_law_bound_report_nonterminating_logit` | [tests/hws/test_b_exact.py:204](../../tests/hws/test_b_exact.py#L204) |  |
| `test_law_bound_report_with_injected_enclosures` | test | `test_law_bound_report_with_injected_enclosures` | [tests/hws/test_b_exact.py:218](../../tests/hws/test_b_exact.py#L218) |  |
| `test_law_bound_restores_after_normal_return_and_after_a_failure` | test | `test_law_bound_restores_after_normal_return_and_after_a_failure` | [tests/hwsb/test_b_meter_law.py:333](../../tests/hwsb/test_b_meter_law.py#L333) |  |
| `test_law_bound_sigma_3_2_is_bounded` | test | `test_law_bound_sigma_3_2_is_bounded` | [tests/hwsb/test_b_meter_law.py:282](../../tests/hwsb/test_b_meter_law.py#L282) |  |
| `test_law_bound_w0_equals_contract_with_zero_delta` | test | `test_law_bound_w0_equals_contract_with_zero_delta` | [tests/hwsb/test_b_meter_law.py:292](../../tests/hwsb/test_b_meter_law.py#L292) |  |
| `test_law_bound_w_star_is_bounded_with_kappa_below_one` | test | `test_law_bound_w_star_is_bounded_with_kappa_below_one` | [tests/hwsb/test_b_meter_law.py:268](../../tests/hwsb/test_b_meter_law.py#L268) |  |
| `test_law_constants` | test | `test_law_constants` | [tests/circle_history/test_process_law.py:230](../../tests/circle_history/test_process_law.py#L230) |  |
| `test_layernorm_eps_scale_not_removed_but_u_minus_beta_in_U0` | test | `test_layernorm_eps_scale_not_removed_but_u_minus_beta_in_U0` | [tests/c2_readout/test_a_readout.py:134](../../tests/c2_readout/test_a_readout.py#L134) |  |
| `test_leading_components_errors` | test | `test_leading_components_errors` | [tests/analysis/test_x4f_targets.py:127](../../tests/analysis/test_x4f_targets.py#L127) |  |
| `test_leading_components_hand_case` | test | `test_leading_components_hand_case` | [tests/analysis/test_x4f_targets.py:87](../../tests/analysis/test_x4f_targets.py#L87) |  |
| `test_leading_components_match_eigh_of_population_covariance` | test | `test_leading_components_match_eigh_of_population_covariance` | [tests/analysis/test_x4f_targets.py:95](../../tests/analysis/test_x4f_targets.py#L95) |  |
| `test_leakage_trigger_at_001` | test | `test_leakage_trigger_at_001` | [tests/c1prime/test_a_eligibility_support.py:92](../../tests/c1prime/test_a_eligibility_support.py#L92) |  |
| `test_learned_defined_fail_on_any_single_condition` | test | `test_learned_defined_fail_on_any_single_condition` | [tests/d2a/test_b_rules_flags.py:47](../../tests/d2a/test_b_rules_flags.py#L47) |  |
| `test_learned_four_none_is_unresolved_unless_model_status_says_missing_or_invalid` | test | `test_learned_four_none_is_unresolved_unless_model_status_says_missing_or_invalid` | [tests/d2a/test_b_rules_flags.py:74](../../tests/d2a/test_b_rules_flags.py#L74) |  |
| `test_learned_pass_at_exact_boundaries` | test | `test_learned_pass_at_exact_boundaries` | [tests/d2a/test_b_rules_flags.py:34](../../tests/d2a/test_b_rules_flags.py#L34) |  |
| `test_learned_single_none_statistic_of_present_model_is_unresolved` | test | `test_learned_single_none_statistic_of_present_model_is_unresolved` | [tests/d2a/test_b_rules_flags.py:67](../../tests/d2a/test_b_rules_flags.py#L67) |  |
| `test_learned_undefined_statistic_is_unresolved_not_fail` | test | `test_learned_undefined_statistic_is_unresolved_not_fail` | [tests/d2a/test_b_rules_flags.py:54](../../tests/d2a/test_b_rules_flags.py#L54) |  |
| `test_learned_undefined_with_another_failing_condition_is_still_unresolved` | test | `test_learned_undefined_with_another_failing_condition_is_still_unresolved` | [tests/d2a/test_b_rules_flags.py:60](../../tests/d2a/test_b_rules_flags.py#L60) |  |
| `test_learning_gate_failure_beats_a_rejecting_replicate` | test | `test_learning_gate_failure_beats_a_rejecting_replicate` | [tests/analysis/test_f1_rule.py:105](../../tests/analysis/test_f1_rule.py#L105) |  |
| `test_learning_gate_reason_present_even_with_few_replicates` | test | `test_learning_gate_reason_present_even_with_few_replicates` | [tests/analysis/test_f1_rule.py:127](../../tests/analysis/test_f1_rule.py#L127) |  |
| `test_ledger_allocation_sync_preserves_entries` | test | `test_ledger_allocation_sync_preserves_entries` | [tests/circle_history/test_builder_v24_runtime.py:117](../../tests/circle_history/test_builder_v24_runtime.py#L117) |  |
| `test_ledger_append_entries_sum_and_atomic_replace` | test | `test_ledger_append_entries_sum_and_atomic_replace` | [tests/hwsb/test_b_records.py:71](../../tests/hwsb/test_b_records.py#L71) |  |
| `test_ledger_duplicate_job_is_refused` | test | `test_ledger_duplicate_job_is_refused` | [tests/hwsb/test_b_records.py:95](../../tests/hwsb/test_b_records.py#L95) |  |
| `test_ledger_policy_sync_preserves_entries` | test | `test_ledger_policy_sync_preserves_entries` | [tests/circle_history/test_builder_v25.py:216](../../tests/circle_history/test_builder_v25.py#L216) |  |
| `test_ledger_preserves_history_on_error_and_is_atomic` | test | `test_ledger_preserves_history_on_error_and_is_atomic` | [tests/experiment/test_x5g1_safety.py:370](../../tests/experiment/test_x5g1_safety.py#L370) |  |
| `test_ledger_read_default` | test | `test_ledger_read_default` | [tests/hwsb/test_b_records.py:66](../../tests/hwsb/test_b_records.py#L66) |  |
| `test_ledger_written_on_exception_and_exception_propagates` | test | `test_ledger_written_on_exception_and_exception_propagates` | [tests/experiment/test_x5g1_controls.py:63](../../tests/experiment/test_x5g1_controls.py#L63) |  |
| `test_ledger_written_on_normal_exit` | test | `test_ledger_written_on_normal_exit` | [tests/experiment/test_x5g1_controls.py:47](../../tests/experiment/test_x5g1_controls.py#L47) |  |
| `test_ledger_written_on_stage_failure` | test | `test_ledger_written_on_stage_failure` | [tests/experiment/test_x5g1_controls.py:73](../../tests/experiment/test_x5g1_controls.py#L73) |  |
| `test_ledoit_wolf_shrinks_population_covariance_toward_scaled_identity` | test | `test_ledoit_wolf_shrinks_population_covariance_toward_scaled_identity` | [tests/analysis/test_x4f_scores.py:182](../../tests/analysis/test_x4f_scores.py#L182) |  |
| `test_ledoit_wolf_zero_shrinkage_known_answer` | test | `test_ledoit_wolf_zero_shrinkage_known_answer` | [tests/analysis/test_x4f_scores.py:200](../../tests/analysis/test_x4f_scores.py#L200) |  |
| `test_lemma_C_credits` | test | `test_lemma_C_credits` | [tests/x2a_stage0/test_x2a_stage0_ph.py:58](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L58) |  |
| `test_lemma_d1_interventional_identity_and_source_independence` | test | `test_lemma_d1_interventional_identity_and_source_independence` | [tests/c2_readout/test_a_partition.py:93](../../tests/c2_readout/test_a_partition.py#L93) |  |
| `test_lemma_d2_logit_and_log_softmax_forms_agree_when_sum_d_is_zero` | test | `test_lemma_d2_logit_and_log_softmax_forms_agree_when_sum_d_is_zero` | [tests/c2_readout/test_a_partition.py:111](../../tests/c2_readout/test_a_partition.py#L111) |  |
| `test_lemma_fw_m_exhaustive_grid` | test | `test_lemma_fw_m_exhaustive_grid` | [tests/c2_readout/test_a_inference.py:184](../../tests/c2_readout/test_a_inference.py#L184) |  |
| `test_lemma_fw_r_exhaustive_grid` | test | `test_lemma_fw_r_exhaustive_grid` | [tests/c2_readout/test_a_inference.py:102](../../tests/c2_readout/test_a_inference.py#L102) |  |
| `test_lemma_p1_exact_zero_and_oracle_normalisation` | test | `test_lemma_p1_exact_zero_and_oracle_normalisation` | [tests/x6_stage1/test_a_pairs.py:324](../../tests/x6_stage1/test_a_pairs.py#L324) |  |
| `test_lemma_p2_scope_prefix_cue_counterexample` | test | `test_lemma_p2_scope_prefix_cue_counterexample` | [tests/x6_stage1/test_a_pairs.py:379](../../tests/x6_stage1/test_a_pairs.py#L379) | L-E5: a predictor that combines the segment with a prefix cue is not covered by P2. |
| `test_lemma_p2_zero_in_expectation_over_uniform_y` | test | `test_lemma_p2_zero_in_expectation_over_uniform_y` | [tests/x6_stage1/test_a_pairs.py:356](../../tests/x6_stage1/test_a_pairs.py#L356) |  |
| `test_lemma_R_reconstruction_and_closed_logits` | test | `test_lemma_R_reconstruction_and_closed_logits` | [tests/c2_readout/test_a_readout.py:101](../../tests/c2_readout/test_a_readout.py#L101) |  |
| `test_lemma_t_is_not_vacuous` | test | `test_lemma_t_is_not_vacuous` | [tests/k4b/test_a_lemma_t.py:150](../../tests/k4b/test_a_lemma_t.py#L150) |  |
| `test_lemma_t_transport_bound` | test | `test_lemma_t_transport_bound` | [tests/k4b/test_a_lemma_t.py:142](../../tests/k4b/test_a_lemma_t.py#L142) |  |
| `test_length_qualifier_on_outcomes_4_to_10` | test | `test_length_qualifier_on_outcomes_4_to_10` | [tests/d2a/test_b_rules_qualifiers.py:116](../../tests/d2a/test_b_rules_qualifiers.py#L116) |  |
| `test_length_qualifier_on_rule4_learning_unresolved` | test | `test_length_qualifier_on_rule4_learning_unresolved` | [tests/d2a/test_b_rules_qualifiers.py:124](../../tests/d2a/test_b_rules_qualifiers.py#L124) |  |
| `test_level_constants_match_contract` | test | `test_level_constants_match_contract` | [tests/hws/test_b_worlds.py:99](../../tests/hws/test_b_worlds.py#L99) |  |
| `test_licence_from_outcome_end_to_end` | test | `test_licence_from_outcome_end_to_end` | [tests/hwsb/test_a_outcomes.py:283](../../tests/hwsb/test_a_outcomes.py#L283) |  |
| `test_licence_missing_field_is_na` | test | `test_licence_missing_field_is_na` | [tests/hwsb/test_a_outcomes.py:226](../../tests/hwsb/test_a_outcomes.py#L226) |  |
| `test_licence_no_circle_uses_head_template` | test | `test_licence_no_circle_uses_head_template` | [tests/hwsb/test_a_outcomes.py:245](../../tests/hwsb/test_a_outcomes.py#L245) |  |
| `test_licence_no_statement` | test | `test_licence_no_statement` | [tests/hwsb/test_a_outcomes.py:277](../../tests/hwsb/test_a_outcomes.py#L277) |  |
| `test_licence_not_learned` | test | `test_licence_not_learned` | [tests/hwsb/test_a_outcomes.py:234](../../tests/hwsb/test_a_outcomes.py#L234) |  |
| `test_licence_other_outcomes` | test | `test_licence_other_outcomes` | [tests/hws/test_a_outcomes.py:306](../../tests/hws/test_a_outcomes.py#L306) |  |
| `test_licence_pass_filled` | test | `test_licence_pass_filled` | [tests/hwsb/test_a_outcomes.py:215](../../tests/hwsb/test_a_outcomes.py#L215) |  |
| `test_licence_selected` | test | `test_licence_selected` | [tests/hws/test_a_outcomes.py:294](../../tests/hws/test_a_outcomes.py#L294) |  |
| `test_licence_sentences_and_designed_counts` | test | `test_licence_sentences_and_designed_counts` | [tests/x6_stage1/test_a_rules.py:297](../../tests/x6_stage1/test_a_rules.py#L297) |  |
| `test_licence_underpowered_with_annotation` | test | `test_licence_underpowered_with_annotation` | [tests/hwsb/test_a_outcomes.py:260](../../tests/hwsb/test_a_outcomes.py#L260) |  |
| `test_lift_primitive_smoothing_are_the_frozen_kernels_on_cstar` | test | `test_lift_primitive_smoothing_are_the_frozen_kernels_on_cstar` | [tests/c1prime/test_a_chart_lcc512.py:156](../../tests/c1prime/test_a_chart_lcc512.py#L156) |  |
| `test_limiter_checks_disk_every_eighth_poll_and_never_caps_cpu` | test | `test_limiter_checks_disk_every_eighth_poll_and_never_caps_cpu` | [tests/c1prime/test_a_release_meter.py:245](../../tests/c1prime/test_a_release_meter.py#L245) |  |
| `test_limiter_kills_an_overdue_native_operation` | test | `test_limiter_kills_an_overdue_native_operation` | [tests/c1prime/test_a_release_meter.py:253](../../tests/c1prime/test_a_release_meter.py#L253) |  |
| `test_limiter_kills_overdue_operation_only` | test | `test_limiter_kills_overdue_operation_only` | [tests/circle_history/test_builder_v24_runtime.py:66](../../tests/circle_history/test_builder_v24_runtime.py#L66) |  |
| `test_limits_and_resource_constants` | test | `test_limits_and_resource_constants` | [tests/x6_stage1/test_b_nb_s0_ops.py:319](../../tests/x6_stage1/test_b_nb_s0_ops.py#L319) |  |
| `test_limits_defaults_are_the_s6_values` | test | `test_limits_defaults_are_the_s6_values` | [tests/d2a/test_b_resource.py:69](../../tests/d2a/test_b_resource.py#L69) |  |
| `test_lineage_join_error_is_technical` | test | `test_lineage_join_error_is_technical` | [tests/c1prime/test_a_chart_exceptions.py:216](../../tests/c1prime/test_a_chart_exceptions.py#L216) |  |
| `test_lineage_mismatch_raises_join_error` | test | `test_lineage_mismatch_raises_join_error` | [tests/circle_history/test_adapter.py:168](../../tests/circle_history/test_adapter.py#L168) |  |
| `test_lineage_ok_absent_store_passes` | test | `test_lineage_ok_absent_store_passes` | [tests/k4b/test_b_rerun.py:107](../../tests/k4b/test_b_rerun.py#L107) |  |
| `test_lineage_ok_accepts_exactly_the_superseded_manifest` | test | `test_lineage_ok_accepts_exactly_the_superseded_manifest` | [tests/k4b/test_b_rerun.py:127](../../tests/k4b/test_b_rerun.py#L127) |  |
| `test_lineage_ok_empty_store_passes` | test | `test_lineage_ok_empty_store_passes` | [tests/k4b/test_b_rerun.py:112](../../tests/k4b/test_b_rerun.py#L112) |  |
| `test_lineage_ok_refuses_unrecorded_prior_file` | test | `test_lineage_ok_refuses_unrecorded_prior_file` | [tests/k4b/test_b_rerun.py:119](../../tests/k4b/test_b_rerun.py#L119) |  |
| `test_lineage_passes_for_every_model` | test | `test_lineage_passes_for_every_model` | [tests/circle_history/test_adapter.py:148](../../tests/circle_history/test_adapter.py#L148) |  |
| `test_linear_in_belief_and_bounded` | test | `test_linear_in_belief_and_bounded` | [tests/analysis/test_x4f_targets.py:51](../../tests/analysis/test_x4f_targets.py#L51) |  |
| `test_ln_final_out_has_no_second_layernorm` | test | `test_ln_final_out_has_no_second_layernorm` | [tests/learner/test_patch.py:129](../../tests/learner/test_patch.py#L129) |  |
| `test_ln_final_out_patch_is_linear_and_input_independent` | test | `test_ln_final_out_patch_is_linear_and_input_independent` | [tests/c2_readout/test_b_patch.py:132](../../tests/c2_readout/test_b_patch.py#L132) |  |
| `test_ln_final_out_patch_touches_only_index` | test | `test_ln_final_out_patch_touches_only_index` | [tests/learner/test_patch.py:120](../../tests/learner/test_patch.py#L120) |  |
| `test_load_cache_rejects_a_different_expected_identity` | test | `test_load_cache_rejects_a_different_expected_identity` | [tests/circle_history/test_reference_cache.py:164](../../tests/circle_history/test_reference_cache.py#L164) |  |
| `test_load_cache_rejects_every_mutation` | test | `test_load_cache_rejects_every_mutation` | [tests/circle_history/test_reference_cache.py:157](../../tests/circle_history/test_reference_cache.py#L157) |  |
| `test_load_config_malformed_json` | test | `test_load_config_malformed_json` | [tests/experiment/test_x5g1t_config_checks.py:265](../../tests/experiment/test_x5g1t_config_checks.py#L265) |  |
| `test_load_config_missing_key` | test | `test_load_config_missing_key` | [tests/experiment/test_x5g1t_config_checks.py:244](../../tests/experiment/test_x5g1t_config_checks.py#L244) |  |
| `test_load_config_unknown_key` | test | `test_load_config_unknown_key` | [tests/experiment/test_x5g1t_config_checks.py:238](../../tests/experiment/test_x5g1t_config_checks.py#L238) |  |
| `test_load_config_valid_is_frozen_exact_keys_and_root` | test | `test_load_config_valid_is_frozen_exact_keys_and_root` | [tests/experiment/test_x5g1t_config_checks.py:229](../../tests/experiment/test_x5g1t_config_checks.py#L229) |  |
| `test_load_config_wrong_type` | test | `test_load_config_wrong_type` | [tests/experiment/test_x5g1t_config_checks.py:259](../../tests/experiment/test_x5g1t_config_checks.py#L259) |  |
| `test_load_contract_refuses_a_protocol_mismatch` | test | `test_load_contract_refuses_a_protocol_mismatch` | [tests/c2_readout/test_b_lineage.py:142](../../tests/c2_readout/test_b_lineage.py#L142) |  |
| `test_local_passes_follow_cfg` | test | `test_local_passes_follow_cfg` | [tests/circle_history/test_cochain_lift.py:232](../../tests/circle_history/test_cochain_lift.py#L232) |  |
| `test_local_passes_hand_case` | test | `test_local_passes_hand_case` | [tests/circle_history/test_cochain_lift.py:216](../../tests/circle_history/test_cochain_lift.py#L216) |  |
| `test_local_passes_stop_at_vertex_128` | test | `test_local_passes_stop_at_vertex_128` | [tests/circle_history/test_cochain_lift.py:238](../../tests/circle_history/test_cochain_lift.py#L238) |  |
| `test_log_softmax_form_differs_from_logit_form_by_the_normaliser_term` | test | `test_log_softmax_form_differs_from_logit_form_by_the_normaliser_term` | [tests/c1prime/test_b_identities.py:191](../../tests/c1prime/test_b_identities.py#L191) |  |
| `test_log_tables_small_q_complete_and_correctly_rounded` | test | `test_log_tables_small_q_complete_and_correctly_rounded` | [tests/x6_stage1/test_a_numerics.py:95](../../tests/x6_stage1/test_a_numerics.py#L95) |  |
| `test_logit_difference_form_is_the_exact_rational_on_dyadic_fixture` | test | `test_logit_difference_form_is_the_exact_rational_on_dyadic_fixture` | [tests/c1prime/test_b_identities.py:87](../../tests/c1prime/test_b_identities.py#L87) |  |
| `test_logit_form_equals_log_softmax_form_exactly_when_sum_d_is_zero` | test | `test_logit_form_equals_log_softmax_form_exactly_when_sum_d_is_zero` | [tests/c1prime/test_b_identities.py:132](../../tests/c1prime/test_b_identities.py#L132) |  |
| `test_logit_policy_table` | test | `test_logit_policy_table` | [tests/c1prime/test_a_gates.py:93](../../tests/c1prime/test_a_gates.py#L93) |  |
| `test_logits32_equals_activation_extractor_bitwise` | test | `test_logits32_equals_activation_extractor_bitwise` | [tests/hwsb/test_b_e4path.py:187](../../tests/hwsb/test_b_e4path.py#L187) |  |
| `test_logsumexp_no_underflow_nan_with_tiny_sigma` | test | `test_logsumexp_no_underflow_nan_with_tiny_sigma` | [tests/process/test_overlap.py:59](../../tests/process/test_overlap.py#L59) |  |
| `test_low_increment` | test | `test_low_increment` | [tests/d2a/test_b_rules_flags.py:156](../../tests/d2a/test_b_rules_flags.py#L156) |  |
| `test_lower_exactly_threshold_passes` | test | `test_lower_exactly_threshold_passes` | [tests/analysis/test_x5_context.py:62](../../tests/analysis/test_x5_context.py#L62) |  |
| `test_lowest_rows_are_the_512_lowest_ids_ascending` | test | `test_lowest_rows_are_the_512_lowest_ids_ascending` | [tests/k4b/test_b_data.py:179](../../tests/k4b/test_b_data.py#L179) |  |
| `test_lowest_rows_picks_the_lowest_ids` | test | `test_lowest_rows_picks_the_lowest_ids` | [tests/hwsb/test_b_streams.py:260](../../tests/hwsb/test_b_streams.py#L260) |  |
| `test_lowest_selects_the_n_lowest_ids_in_ascending_id_order` | test | `test_lowest_selects_the_n_lowest_ids_in_ascending_id_order` | [tests/c1prime/test_b_registry.py:100](../../tests/c1prime/test_b_registry.py#L100) |  |
| `test_lr_schedule_known_values` | test | `test_lr_schedule_known_values` | [tests/learner/test_training.py:114](../../tests/learner/test_training.py#L114) |  |
| `test_m1_all_zero_displacements_use_the_zero_spectrum_rule` | test | `test_m1_all_zero_displacements_use_the_zero_spectrum_rule` | [tests/c1prime/test_b_frames.py:161](../../tests/c1prime/test_b_frames.py#L161) |  |
| `test_m1_fails_on_a_frame_that_is_not_orthonormal` | test | `test_m1_fails_on_a_frame_that_is_not_orthonormal` | [tests/c1prime/test_b_frames.py:136](../../tests/c1prime/test_b_frames.py#L136) |  |
| `test_m1_fails_when_the_coordinates_lose_norm` | test | `test_m1_fails_when_the_coordinates_lose_norm` | [tests/c1prime/test_b_frames.py:142](../../tests/c1prime/test_b_frames.py#L142) |  |
| `test_m1_fails_when_the_displacement_leaves_span_WB` | test | `test_m1_fails_when_the_displacement_leaves_span_WB` | [tests/c1prime/test_b_frames.py:146](../../tests/c1prime/test_b_frames.py#L146) |  |
| `test_m1_frame_from_an_exactly_rank_deficient_draw_fails` | test | `test_m1_frame_from_an_exactly_rank_deficient_draw_fails` | [tests/c1prime/test_b_frames.py:166](../../tests/c1prime/test_b_frames.py#L166) |  |
| `test_m1_passes_on_a_consistent_family` | test | `test_m1_passes_on_a_consistent_family` | [tests/c1prime/test_b_frames.py:132](../../tests/c1prime/test_b_frames.py#L132) |  |
| `test_m1_zero_primary_norm_requires_exact_zeros` | test | `test_m1_zero_primary_norm_requires_exact_zeros` | [tests/c1prime/test_b_frames.py:152](../../tests/c1prime/test_b_frames.py#L152) |  |
| `test_m2_dispersion_needs_28_of_32_frames` | test | `test_m2_dispersion_needs_28_of_32_frames` | [tests/c1prime/test_b_gates.py:90](../../tests/c1prime/test_b_gates.py#L90) |  |
| `test_m2_family_ceiling_fails_even_when_dispersion_holds` | test | `test_m2_family_ceiling_fails_even_when_dispersion_holds` | [tests/c1prime/test_b_gates.py:85](../../tests/c1prime/test_b_gates.py#L85) |  |
| `test_m2_leakage_only_when_active_and_after_family` | test | `test_m2_leakage_only_when_active_and_after_family` | [tests/c1prime/test_b_gates.py:99](../../tests/c1prime/test_b_gates.py#L99) |  |
| `test_m2_matching_bounds_are_inclusive` | test | `test_m2_matching_bounds_are_inclusive` | [tests/c1prime/test_b_gates.py:78](../../tests/c1prime/test_b_gates.py#L78) |  |
| `test_m2_primary_ceilings_are_inclusive` | test | `test_m2_primary_ceilings_are_inclusive` | [tests/c1prime/test_b_gates.py:71](../../tests/c1prime/test_b_gates.py#L71) |  |
| `test_m3_family_ceiling` | test | `test_m3_family_ceiling` | [tests/c1prime/test_a_eligibility_support.py:177](../../tests/c1prime/test_a_eligibility_support.py#L177) |  |
| `test_m3_matching_within_002` | test | `test_m3_matching_within_002` | [tests/c1prime/test_a_eligibility_support.py:183](../../tests/c1prime/test_a_eligibility_support.py#L183) |  |
| `test_m3_primary_ceiling` | test | `test_m3_primary_ceiling` | [tests/c1prime/test_a_eligibility_support.py:170](../../tests/c1prime/test_a_eligibility_support.py#L170) |  |
| `test_m3_support_fractions` | test | `test_m3_support_fractions` | [tests/c1prime/test_a_eligibility_support.py:193](../../tests/c1prime/test_a_eligibility_support.py#L193) |  |
| `test_m4_boundaries` | test | `test_m4_boundaries` | [tests/c1prime/test_b_gates.py:183](../../tests/c1prime/test_b_gates.py#L183) |  |
| `test_mahalanobis_with_source_or_donor_nuisance` | test | `test_mahalanobis_with_source_or_donor_nuisance` | [tests/c1prime/test_a_eligibility_support.py:142](../../tests/c1prime/test_a_eligibility_support.py#L142) |  |
| `test_main_binds_and_hands_over_to_the_meter` | test | `test_main_binds_and_hands_over_to_the_meter` | [tests/hws/test_b_records.py:316](../../tests/hws/test_b_records.py#L316) |  |
| `test_main_binds_and_hands_over_to_the_meter` | test | `test_main_binds_and_hands_over_to_the_meter` | [tests/hwsb/test_b_meter_law.py:152](../../tests/hwsb/test_b_meter_law.py#L152) |  |
| `test_main_file_failing_rule_2a_prime_makes_main_incomplete` | test | `test_main_file_failing_rule_2a_prime_makes_main_incomplete` | [tests/k4b/test_b_registry_rules.py:227](../../tests/k4b/test_b_registry_rules.py#L227) |  |
| `test_main_inventory_is_deep_including_tests_and_venv` | test | `test_main_inventory_is_deep_including_tests_and_venv` | [tests/k4b/test_b_registry_rules.py:206](../../tests/k4b/test_b_registry_rules.py#L206) |  |
| `test_main_refuses_a_foreign_run_lock_and_missing_out` | test | `test_main_refuses_a_foreign_run_lock_and_missing_out` | [tests/hws/test_b_records.py:340](../../tests/hws/test_b_records.py#L340) |  |
| `test_main_refuses_foreign_run_lock_and_missing_arguments` | test | `test_main_refuses_foreign_run_lock_and_missing_arguments` | [tests/hwsb/test_b_meter_law.py:173](../../tests/hwsb/test_b_meter_law.py#L173) |  |
| `test_main_refuses_without_freeze_auth_or_accept` | test | `test_main_refuses_without_freeze_auth_or_accept` | [tests/hws/test_b_records.py:238](../../tests/hws/test_b_records.py#L238) |  |
| `test_main_with_only_tests_venv_and_basetemp_fixtures_is_not_incomplete` | test | `test_main_with_only_tests_venv_and_basetemp_fixtures_is_not_incomplete` | [tests/k4b/test_b_registry_rules.py:214](../../tests/k4b/test_b_registry_rules.py#L214) |  |
| `test_main_without_valid_release_never_runs_the_meter` | test | `test_main_without_valid_release_never_runs_the_meter` | [tests/k4b/test_b_meter.py:113](../../tests/k4b/test_b_meter.py#L113) |  |
| `test_make_block_matches_independent_sampling` | test | `test_make_block_matches_independent_sampling` | [tests/hwsb/test_b_streams.py:280](../../tests/hwsb/test_b_streams.py#L280) |  |
| `test_make_latch_shape` | test | `test_make_latch_shape` | [tests/experiment/test_x5g1t_usage.py:183](../../tests/experiment/test_x5g1t_usage.py#L183) |  |
| `test_malformed_histories_invalid_before_any_reference_work` | test | `test_malformed_histories_invalid_before_any_reference_work` | [tests/circle_history/test_reference_binding.py:163](../../tests/circle_history/test_reference_binding.py#L163) |  |
| `test_malformed_inputs_raise_profile_error` | test | `test_malformed_inputs_raise_profile_error` | [tests/oracle_profile/test_builder_kernels.py:99](../../tests/oracle_profile/test_builder_kernels.py#L99) |  |
| `test_malformed_latch` | test | `test_malformed_latch` | [tests/experiment/test_x5g1t_usage.py:290](../../tests/experiment/test_x5g1t_usage.py#L290) |  |
| `test_malformed_percent_fails_closed` | test | `test_malformed_percent_fails_closed` | [tests/oracle_profile/test_builder_controls.py:165](../../tests/oracle_profile/test_builder_controls.py#L165) |  |
| `test_malformed_release_session_is_refused` | test | `test_malformed_release_session_is_refused` | [tests/c1prime/test_c_release_worker.py:43](../../tests/c1prime/test_c_release_worker.py#L43) |  |
| `test_map_failures_flag_a_corrupted_joint` | test | `test_map_failures_flag_a_corrupted_joint` | [tests/experiment/test_x4b.py:45](../../tests/experiment/test_x4b.py#L45) |  |
| `test_margin_floor_and_transport` | test | `test_margin_floor_and_transport` | [tests/k4b/test_a_decision.py:105](../../tests/k4b/test_a_decision.py#L105) |  |
| `test_marginal_index_conventions` | test | `test_marginal_index_conventions` | [tests/hws/test_b_oracle.py:293](../../tests/hws/test_b_oracle.py#L293) |  |
| `test_marginal_never_fills_an_ordinary_slot` | test | `test_marginal_never_fills_an_ordinary_slot` | [tests/hws/test_a_classify.py:266](../../tests/hws/test_a_classify.py#L266) |  |
| `test_masked_oracle_phase_features` | test | `test_masked_oracle_phase_features` | [tests/c2_readout/test_b_screens.py:139](../../tests/c2_readout/test_b_screens.py#L139) |  |
| `test_masters_are_registered_and_fresh_against_known_lineages` | test | `test_masters_are_registered_and_fresh_against_known_lineages` | [tests/x6_stage1/test_b_seed_pool_reg.py:51](../../tests/x6_stage1/test_b_seed_pool_reg.py#L51) |  |
| `test_matched_statistics_and_control_spread_zero` | test | `test_matched_statistics_and_control_spread_zero` | [tests/x6_stage1/test_a_designed.py:122](../../tests/x6_stage1/test_a_designed.py#L122) |  |
| `test_maxdiff_nested_values` | test | `test_maxdiff_nested_values` | [tests/experiment/test_x5g1_verify.py:11](../../tests/experiment/test_x5g1_verify.py#L11) |  |
| `test_maxdiff_structure_mismatch_is_infinite` | test | `test_maxdiff_structure_mismatch_is_infinite` | [tests/experiment/test_x5g1_verify.py:17](../../tests/experiment/test_x5g1_verify.py#L17) |  |
| `test_maximal_s1_and_x1_forecasts` | test | `test_maximal_s1_and_x1_forecasts` | [tests/hws/test_a_budget.py:57](../../tests/hws/test_a_budget.py#L57) |  |
| `test_maxmin_landmarks` | test | `test_maxmin_landmarks` | [tests/topology/test_persistence.py:202](../../tests/topology/test_persistence.py#L202) |  |
| `test_mde_boundary_equality_passes` | test | `test_mde_boundary_equality_passes` | [tests/hwsb/test_a_ladder.py:255](../../tests/hwsb/test_a_ladder.py#L255) |  |
| `test_mde_formula_via_normal_dist` | test | `test_mde_formula_via_normal_dist` | [tests/circle_history/test_scores_precision_gates.py:124](../../tests/circle_history/test_scores_precision_gates.py#L124) |  |
| `test_mde_ok_boundary` | test | `test_mde_ok_boundary` | [tests/k4b/test_a_ranks_ladder.py:212](../../tests/k4b/test_a_ranks_ladder.py#L212) |  |
| `test_measure_only_caps_in_the_contract` | test | `test_measure_only_caps_in_the_contract` | [tests/c2_readout/test_b_lineage.py:387](../../tests/c2_readout/test_b_lineage.py#L387) |  |
| `test_measure_only_limiter_has_no_cpu_reason_but_keeps_other_guards` | test | `test_measure_only_limiter_has_no_cpu_reason_but_keeps_other_guards` | [tests/circle_history/test_builder_v25.py:204](../../tests/circle_history/test_builder_v25.py#L204) |  |
| `test_measure_only_never_stops_on_cpu` | test | `test_measure_only_never_stops_on_cpu` | [tests/circle_history/test_builder_v25.py:186](../../tests/circle_history/test_builder_v25.py#L186) |  |
| `test_measure_only_unreleased_stage_still_refused` | test | `test_measure_only_unreleased_stage_still_refused` | [tests/circle_history/test_builder_v25.py:197](../../tests/circle_history/test_builder_v25.py#L197) |  |
| `test_measured_discrepancy_contains_the_exact_error` | test | `test_measured_discrepancy_contains_the_exact_error` | [tests/c1prime/test_b_cert_oracle.py:183](../../tests/c1prime/test_b_cert_oracle.py#L183) |  |
| `test_measured_log_error_matches_forty_digit_ln_and_grows_with_injected_error` | test | `test_measured_log_error_matches_forty_digit_ln_and_grows_with_injected_error` | [tests/c1prime/test_b_cert_oracle.py:292](../../tests/c1prime/test_b_cert_oracle.py#L292) |  |
| `test_median_equal_to_envelope_fails_strictly` | test | `test_median_equal_to_envelope_fails_strictly` | [tests/analysis/test_f1_rule.py:144](../../tests/analysis/test_f1_rule.py#L144) |  |
| `test_merge_columns_sums_never_averages` | test | `test_merge_columns_sums_never_averages` | [tests/hws/test_b_worlds.py:246](../../tests/hws/test_b_worlds.py#L246) |  |
| `test_merge_q1_w12_is_identity_and_tiny_merge` | test | `test_merge_q1_w12_is_identity_and_tiny_merge` | [tests/hws/test_b_worlds.py:260](../../tests/hws/test_b_worlds.py#L260) |  |
| `test_metadata_matches_warp_profile` | test | `test_metadata_matches_warp_profile` | [tests/process/test_conductance.py:204](../../tests/process/test_conductance.py#L204) |  |
| `test_meter_active_lock_admitted_at_s1` | test | `test_meter_active_lock_admitted_at_s1` | [tests/c2_readout/test_b_patch.py:353](../../tests/c2_readout/test_b_patch.py#L353) |  |
| `test_meter_active_lock_near_misses_stay_unrecognised` | test | `test_meter_active_lock_near_misses_stay_unrecognised` | [tests/c2_readout/test_b_patch.py:368](../../tests/c2_readout/test_b_patch.py#L368) |  |
| `test_meter_bind_check_refusals` | test | `test_meter_bind_check_refusals` | [tests/x6_stage1/test_b_chain_ops.py:311](../../tests/x6_stage1/test_b_chain_ops.py#L311) |  |
| `test_meter_binding_sha_and_import_directory` | test | `test_meter_binding_sha_and_import_directory` | [tests/c2_readout/test_b_policy.py:385](../../tests/c2_readout/test_b_policy.py#L385) |  |
| `test_meter_values` | test | `test_meter_values` | [tests/x6_stage1/test_b_chain_ops.py:304](../../tests/x6_stage1/test_b_chain_ops.py#L304) |  |
| `test_metric_axioms_random` | test | `test_metric_axioms_random` | [tests/topology/test_metrics.py:65](../../tests/topology/test_metrics.py#L65) |  |
| `test_mismatch_report_hand_values_and_exclusion` | test | `test_mismatch_report_hand_values_and_exclusion` | [tests/analysis/test_x4f_erasure_family.py:217](../../tests/analysis/test_x4f_erasure_family.py#L217) |  |
| `test_mismatch_report_threshold_scales_with_scale` | test | `test_mismatch_report_threshold_scales_with_scale` | [tests/analysis/test_x4f_erasure_family.py:231](../../tests/analysis/test_x4f_erasure_family.py#L231) |  |
| `test_mismatch_symmetric` | test | `test_mismatch_symmetric` | [tests/analysis/test_spaces.py:34](../../tests/analysis/test_spaces.py#L34) |  |
| `test_mismatched_ids_raise` | test | `test_mismatched_ids_raise` | [tests/analysis/test_spaces.py:28](../../tests/analysis/test_spaces.py#L28) |  |
| `test_missing_config_fails_run_key_and_step` | test | `test_missing_config_fails_run_key_and_step` | [tests/k4b/test_b_h1_meta.py:228](../../tests/k4b/test_b_h1_meta.py#L228) |  |
| `test_missing_file_fails_closed` | test | `test_missing_file_fails_closed` | [tests/hwsb/test_b_registry.py:137](../../tests/hwsb/test_b_registry.py#L137) |  |
| `test_missing_key_is_a_mismatch_not_an_exception` | test | `test_missing_key_is_a_mismatch_not_an_exception` | [tests/k4b/test_b_h1_meta.py:223](../../tests/k4b/test_b_h1_meta.py#L223) |  |
| `test_missing_ledger_starts_at_zero` | test | `test_missing_ledger_starts_at_zero` | [tests/experiment/test_x5g1_controls.py:142](../../tests/experiment/test_x5g1_controls.py#L142) |  |
| `test_missing_parent_id_gives_no_save` | test | `test_missing_parent_id_gives_no_save` | [tests/experiment/test_x5g1_export_integration.py:210](../../tests/experiment/test_x5g1_export_integration.py#L210) |  |
| `test_missing_parents_is_failed_not_a_scientific_verdict` | test | `test_missing_parents_is_failed_not_a_scientific_verdict` | [tests/experiment/test_x5g1_smoke.py:14](../../tests/experiment/test_x5g1_smoke.py#L14) |  |
| `test_missing_runtime_file_fails_closed` | test | `test_missing_runtime_file_fails_closed` | [tests/circle_history/test_builder_v25.py:152](../../tests/circle_history/test_builder_v25.py#L152) |  |
| `test_missing_sched_record_is_refused` | test | `test_missing_sched_record_is_refused` | [tests/hwsb/test_b_records.py:142](../../tests/hwsb/test_b_records.py#L142) |  |
| `test_missing_source_never_clears` | test | `test_missing_source_never_clears` | [tests/experiment/test_x5g1t_usage.py:232](../../tests/experiment/test_x5g1t_usage.py#L232) |  |
| `test_mixing_bound_eps_and_pi_min` | test | `test_mixing_bound_eps_and_pi_min` | [tests/analysis/test_x5_kernel.py:119](../../tests/analysis/test_x5_kernel.py#L119) |  |
| `test_mixing_bound_uses_ceil` | test | `test_mixing_bound_uses_ceil` | [tests/analysis/test_x5_kernel.py:109](../../tests/analysis/test_x5_kernel.py#L109) |  |
| `test_mixture_blocks_and_stationarity` | test | `test_mixture_blocks_and_stationarity` | [tests/x2a_stage0/test_x2a_stage0.py:178](../../tests/x2a_stage0/test_x2a_stage0.py#L178) |  |
| `test_model_equal_to_q_reindexes_to_q` | test | `test_model_equal_to_q_reindexes_to_q` | [tests/hwsb/test_a_learning.py:179](../../tests/hwsb/test_a_learning.py#L179) |  |
| `test_model_inputs_have_bos_36_and_width_33` | test | `test_model_inputs_have_bos_36_and_width_33` | [tests/hwsb/test_b_streams.py:250](../../tests/hwsb/test_b_streams.py#L250) |  |
| `test_model_predictive_is_canonical_softmax` | test | `test_model_predictive_is_canonical_softmax` | [tests/hwsb/test_b_e4path.py:231](../../tests/hwsb/test_b_e4path.py#L231) |  |
| `test_model_predictor_from_verified_file` | test | `test_model_predictor_from_verified_file` | [tests/x6_stage1/test_a_eval.py:122](../../tests/x6_stage1/test_a_eval.py#L122) |  |
| `test_model_streams_scope_map_and_arm_sharing` | test | `test_model_streams_scope_map_and_arm_sharing` | [tests/x6_stage1/test_b_seed_pool_reg.py:79](../../tests/x6_stage1/test_b_seed_pool_reg.py#L79) |  |
| `test_module_file_at_most_400_lines` | test | `test_module_file_at_most_400_lines` | [tests/d1_seam/test_d1_seam.py:242](../../tests/d1_seam/test_d1_seam.py#L242) |  |
| `test_module_files_at_most_400_lines` | test | `test_module_files_at_most_400_lines` | [tests/x2a_stage0/test_x2a_stage0.py:382](../../tests/x2a_stage0/test_x2a_stage0.py#L382) |  |
| `test_module_set_and_400_line_limit` | test | `test_module_set_and_400_line_limit` | [tests/c2_readout/test_b_policy.py:363](../../tests/c2_readout/test_b_policy.py#L363) |  |
| `test_module_set_line_limits_and_test_files` | test | `test_module_set_line_limits_and_test_files` | [tests/x6_stage1/test_b_nb_s0_ops.py:268](../../tests/x6_stage1/test_b_nb_s0_ops.py#L268) |  |
| `test_module_top_level_has_no_calls_with_io` | test | `test_module_top_level_has_no_calls_with_io` | [tests/circle_history/test_builder_runtime.py:195](../../tests/circle_history/test_builder_runtime.py#L195) |  |
| `test_movement_rate_hand_value_nonuniform_pi` | test | `test_movement_rate_hand_value_nonuniform_pi` | [tests/analysis/test_x5_kernel.py:48](../../tests/analysis/test_x5_kernel.py#L48) |  |
| `test_movement_rate_lazy_cycle` | test | `test_movement_rate_lazy_cycle` | [tests/analysis/test_x5_kernel.py:54](../../tests/analysis/test_x5_kernel.py#L54) |  |
| `test_N13_circular_rows_are_privileged_eval` | test | `test_N13_circular_rows_are_privileged_eval` | [tests/analysis/test_sensitivity_circular.py:360](../../tests/analysis/test_sensitivity_circular.py#L360) |  |
| `test_N13_oracle_id_mismatch_raises` | test | `test_N13_oracle_id_mismatch_raises` | [tests/analysis/test_sensitivity_circular.py:380](../../tests/analysis/test_sensitivity_circular.py#L380) |  |
| `test_N14_ln_gauge_free_affine_invariance` | test | `test_N14_ln_gauge_free_affine_invariance` | [tests/analysis/test_readout.py:51](../../tests/analysis/test_readout.py#L51) |  |
| `test_N14_ln_gauge_free_hand_computed_row` | test | `test_N14_ln_gauge_free_hand_computed_row` | [tests/analysis/test_readout.py:94](../../tests/analysis/test_readout.py#L94) |  |
| `test_N14_ln_gauge_free_matches_reference_and_accepts_float32` | test | `test_N14_ln_gauge_free_matches_reference_and_accepts_float32` | [tests/analysis/test_readout.py:105](../../tests/analysis/test_readout.py#L105) |  |
| `test_N14_ln_gauge_free_not_scale_invariant_with_eps_at_small_variance` | test | `test_N14_ln_gauge_free_not_scale_invariant_with_eps_at_small_variance` | [tests/analysis/test_readout.py:80](../../tests/analysis/test_readout.py#L80) |  |
| `test_N14_ln_gauge_free_rows_have_mean_zero_and_shape` | test | `test_N14_ln_gauge_free_rows_have_mean_zero_and_shape` | [tests/analysis/test_readout.py:86](../../tests/analysis/test_readout.py#L86) |  |
| `test_N14_ln_gauge_free_scaling_with_eps_is_an_eps_rescaling` | test | `test_N14_ln_gauge_free_scaling_with_eps_is_an_eps_rescaling` | [tests/analysis/test_readout.py:72](../../tests/analysis/test_readout.py#L72) |  |
| `test_N14_ln_gauge_free_shift_exact_with_eps` | test | `test_N14_ln_gauge_free_shift_exact_with_eps` | [tests/analysis/test_readout.py:61](../../tests/analysis/test_readout.py#L61) |  |
| `test_N15_readout_projector_accepts_float32` | test | `test_N15_readout_projector_accepts_float32` | [tests/analysis/test_readout.py:181](../../tests/analysis/test_readout.py#L181) |  |
| `test_N15_readout_projector_full_rank` | test | `test_N15_readout_projector_full_rank` | [tests/analysis/test_readout.py:132](../../tests/analysis/test_readout.py#L132) |  |
| `test_N15_readout_projector_gamma_with_zeros` | test | `test_N15_readout_projector_gamma_with_zeros` | [tests/analysis/test_readout.py:152](../../tests/analysis/test_readout.py#L152) |  |
| `test_N15_readout_projector_gamma_zeros_make_rank_drop` | test | `test_N15_readout_projector_gamma_zeros_make_rank_drop` | [tests/analysis/test_readout.py:164](../../tests/analysis/test_readout.py#L164) |  |
| `test_N15_readout_projector_rank_deficient_duplicate_rows` | test | `test_N15_readout_projector_rank_deficient_duplicate_rows` | [tests/analysis/test_readout.py:141](../../tests/analysis/test_readout.py#L141) |  |
| `test_N15_readout_projector_zero_A_gives_zero_P` | test | `test_N15_readout_projector_zero_A_gives_zero_P` | [tests/analysis/test_readout.py:175](../../tests/analysis/test_readout.py#L175) |  |
| `test_N16_split_readout_null_part_is_invisible` | test | `test_N16_split_readout_null_part_is_invisible` | [tests/analysis/test_readout.py:223](../../tests/analysis/test_readout.py#L223) |  |
| `test_N16_split_readout_sums_and_orthogonality` | test | `test_N16_split_readout_sums_and_orthogonality` | [tests/analysis/test_readout.py:204](../../tests/analysis/test_readout.py#L204) |  |
| `test_N16_split_readout_vector_already_visible_has_zero_null` | test | `test_N16_split_readout_vector_already_visible_has_zero_null` | [tests/analysis/test_readout.py:214](../../tests/analysis/test_readout.py#L214) |  |
| `test_N17_tiny_model_against_hand_layernorm` | test | `test_N17_tiny_model_against_hand_layernorm` | [tests/analysis/test_readout.py:260](../../tests/analysis/test_readout.py#L260) |  |
| `test_N17_tiny_model_visible_part_reproduces_logits` | test | `test_N17_tiny_model_visible_part_reproduces_logits` | [tests/analysis/test_readout.py:248](../../tests/analysis/test_readout.py#L248) |  |
| `test_N18_predictive_pointset_custom_space_and_float32` | test | `test_N18_predictive_pointset_custom_space_and_float32` | [tests/analysis/test_readout.py:313](../../tests/analysis/test_readout.py#L313) |  |
| `test_N18_predictive_pointset_known_answer` | test | `test_N18_predictive_pointset_known_answer` | [tests/analysis/test_readout.py:277](../../tests/analysis/test_readout.py#L277) |  |
| `test_N18_predictive_pointset_row_shift_invariant_and_stable` | test | `test_N18_predictive_pointset_row_shift_invariant_and_stable` | [tests/analysis/test_readout.py:301](../../tests/analysis/test_readout.py#L301) |  |
| `test_N18_predictive_pointset_rows_sum_to_one_and_match_hand_softmax` | test | `test_N18_predictive_pointset_rows_sum_to_one_and_match_hand_softmax` | [tests/analysis/test_readout.py:289](../../tests/analysis/test_readout.py#L289) |  |
| `test_N19_ln_gauge_free_errors` | test | `test_N19_ln_gauge_free_errors` | [tests/analysis/test_readout.py:324](../../tests/analysis/test_readout.py#L324) |  |
| `test_N19_ln_gauge_free_zero_variance_row` | test | `test_N19_ln_gauge_free_zero_variance_row` | [tests/analysis/test_readout.py:337](../../tests/analysis/test_readout.py#L337) |  |
| `test_N19_predictive_pointset_errors` | test | `test_N19_predictive_pointset_errors` | [tests/analysis/test_readout.py:372](../../tests/analysis/test_readout.py#L372) |  |
| `test_N19_readout_projector_errors` | test | `test_N19_readout_projector_errors` | [tests/analysis/test_readout.py:346](../../tests/analysis/test_readout.py#L346) |  |
| `test_N19_split_readout_errors` | test | `test_N19_split_readout_errors` | [tests/analysis/test_readout.py:362](../../tests/analysis/test_readout.py#L362) |  |
| `test_N20_chord_equals_normalised_cdist_and_scale_invariant` | test | `test_N20_chord_equals_normalised_cdist_and_scale_invariant` | [tests/analysis/test_sensitivity_circular.py:55](../../tests/analysis/test_sensitivity_circular.py#L55) |  |
| `test_N20_euclidean_equals_cdist` | test | `test_N20_euclidean_equals_cdist` | [tests/analysis/test_sensitivity_circular.py:48](../../tests/analysis/test_sensitivity_circular.py#L48) |  |
| `test_N20_pca_fit_set_defines_projection` | test | `test_N20_pca_fit_set_defines_projection` | [tests/analysis/test_sensitivity_circular.py:86](../../tests/analysis/test_sensitivity_circular.py#L86) |  |
| `test_N20_pca_full_dims_equals_euclidean` | test | `test_N20_pca_full_dims_equals_euclidean` | [tests/analysis/test_sensitivity_circular.py:65](../../tests/analysis/test_sensitivity_circular.py#L65) |  |
| `test_N20_pca_one_dim_matches_hand_singular_vector` | test | `test_N20_pca_one_dim_matches_hand_singular_vector` | [tests/analysis/test_sensitivity_circular.py:73](../../tests/analysis/test_sensitivity_circular.py#L73) |  |
| `test_N21_bounds_and_disjoint_supports` | test | `test_N21_bounds_and_disjoint_supports` | [tests/analysis/test_sensitivity_circular.py:130](../../tests/analysis/test_sensitivity_circular.py#L130) |  |
| `test_N21_hand_values_two_point_distributions` | test | `test_N21_hand_values_two_point_distributions` | [tests/analysis/test_sensitivity_circular.py:115](../../tests/analysis/test_sensitivity_circular.py#L115) |  |
| `test_N21_head` | test | `test_N21_head` | [tests/analysis/test_sensitivity_circular.py:142](../../tests/analysis/test_sensitivity_circular.py#L142) |  |
| `test_N22_agreement_hand_four_points` | test | `test_N22_agreement_hand_four_points` | [tests/analysis/test_sensitivity_circular.py:171](../../tests/analysis/test_sensitivity_circular.py#L171) |  |
| `test_N22_agreement_identity` | test | `test_N22_agreement_identity` | [tests/analysis/test_sensitivity_circular.py:151](../../tests/analysis/test_sensitivity_circular.py#L151) |  |
| `test_N22_agreement_independent_uniform_small` | test | `test_N22_agreement_independent_uniform_small` | [tests/analysis/test_sensitivity_circular.py:180](../../tests/analysis/test_sensitivity_circular.py#L180) |  |
| `test_N22_agreement_reflection_invariant` | test | `test_N22_agreement_reflection_invariant` | [tests/analysis/test_sensitivity_circular.py:164](../../tests/analysis/test_sensitivity_circular.py#L164) |  |
| `test_N22_agreement_rotation_invariant` | test | `test_N22_agreement_rotation_invariant` | [tests/analysis/test_sensitivity_circular.py:157](../../tests/analysis/test_sensitivity_circular.py#L157) |  |
| `test_N23_belief_delta_returns_state_angle` | test | `test_N23_belief_delta_returns_state_angle` | [tests/analysis/test_sensitivity_circular.py:205](../../tests/analysis/test_sensitivity_circular.py#L205) |  |
| `test_N23_belief_split_returns_midpoint` | test | `test_N23_belief_split_returns_midpoint` | [tests/analysis/test_sensitivity_circular.py:214](../../tests/analysis/test_sensitivity_circular.py#L214) |  |
| `test_N23_lattice_angle_hand_values` | test | `test_N23_lattice_angle_hand_values` | [tests/analysis/test_sensitivity_circular.py:195](../../tests/analysis/test_sensitivity_circular.py#L195) |  |
| `test_N24_collinear_points_no_h1_class` | test | `test_N24_collinear_points_no_h1_class` | [tests/analysis/test_sensitivity_circular.py:257](../../tests/analysis/test_sensitivity_circular.py#L257) |  |
| `test_N24_compare_independent_angle_not_significant` | test | `test_N24_compare_independent_angle_not_significant` | [tests/analysis/test_sensitivity_circular.py:244](../../tests/analysis/test_sensitivity_circular.py#L244) |  |
| `test_N24_compare_recovers_true_angle` | test | `test_N24_compare_recovers_true_angle` | [tests/analysis/test_sensitivity_circular.py:234](../../tests/analysis/test_sensitivity_circular.py#L234) |  |
| `test_N25_compare_errors` | test | `test_N25_compare_errors` | [tests/analysis/test_sensitivity_circular.py:296](../../tests/analysis/test_sensitivity_circular.py#L296) |  |
| `test_N25_errors` | test | `test_N25_errors` | [tests/analysis/test_sensitivity_circular.py:269](../../tests/analysis/test_sensitivity_circular.py#L269) |  |
| `test_n2_fit_class_mean_mahalanobis_and_q99` | test | `test_n2_fit_class_mean_mahalanobis_and_q99` | [tests/c2_readout/test_b_screens.py:171](../../tests/c2_readout/test_b_screens.py#L171) |  |
| `test_n2_fraction_rule_and_cap_exact` | test | `test_n2_fraction_rule_and_cap_exact` | [tests/c2_readout/test_b_screens.py:199](../../tests/c2_readout/test_b_screens.py#L199) |  |
| `test_n2_paired_gaussian_counterexample_passes_the_radial_screen` | test | `test_n2_paired_gaussian_counterexample_passes_the_radial_screen` | [tests/c2_readout/test_b_screens.py:213](../../tests/c2_readout/test_b_screens.py#L213) |  |
| `test_n_run_learning_gate_is_not_applicable` | test | `test_n_run_learning_gate_is_not_applicable` | [tests/experiment/test_report_e2.py:77](../../tests/experiment/test_report_e2.py#L77) |  |
| `test_n_test_is_the_max_over_alive_families` | test | `test_n_test_is_the_max_over_alive_families` | [tests/c2_readout/test_a_oracle.py:397](../../tests/c2_readout/test_a_oracle.py#L397) |  |
| `test_n_test_smaller_than_panels_is_alignment_error` | test | `test_n_test_smaller_than_panels_is_alignment_error` | [tests/dataset/test_stage.py:98](../../tests/dataset/test_stage.py#L98) |  |
| `test_named_canonical_column_permutations_round_trip` | test | `test_named_canonical_column_permutations_round_trip` | [tests/c1prime/test_a_oracle_named.py:146](../../tests/c1prime/test_a_oracle_named.py#L146) |  |
| `test_named_canonical_four_e_minus_12_rule_boundary` | test | `test_named_canonical_four_e_minus_12_rule_boundary` | [tests/c1prime/test_a_oracle.py:234](../../tests/c1prime/test_a_oracle.py#L234) |  |
| `test_named_from_canonical_round_trip` | test | `test_named_from_canonical_round_trip` | [tests/k4b/test_b_data.py:162](../../tests/k4b/test_b_data.py#L162) |  |
| `test_named_space_filter_agrees_with_canonical_within_4e_12` | test | `test_named_space_filter_agrees_with_canonical_within_4e_12` | [tests/c1prime/test_a_oracle_named.py:155](../../tests/c1prime/test_a_oracle_named.py#L155) | Section 3.3: q_named[perm[j]] = q_canon[j], checked against direct named-space filtering |
| `test_named_tokens_are_inverted_to_canonical` | test | `test_named_tokens_are_inverted_to_canonical` | [tests/hwsb/test_b_registry.py:115](../../tests/hwsb/test_b_registry.py#L115) |  |
| `test_namespace_initial_admission` | test | `test_namespace_initial_admission` | [tests/c2_readout/test_b_lineage.py:326](../../tests/c2_readout/test_b_lineage.py#L326) |  |
| `test_namespace_legitimate_continuation` | test | `test_namespace_legitimate_continuation` | [tests/c2_readout/test_b_lineage.py:339](../../tests/c2_readout/test_b_lineage.py#L339) |  |
| `test_namespace_unrelated_collision_is_lineage` | test | `test_namespace_unrelated_collision_is_lineage` | [tests/c2_readout/test_b_lineage.py:376](../../tests/c2_readout/test_b_lineage.py#L376) |  |
| `test_natural_prefix_rule_independent` | test | `test_natural_prefix_rule_independent` | [tests/x6_stage1/test_a_designed.py:199](../../tests/x6_stage1/test_a_designed.py#L199) |  |
| `test_nb_static_refuses` | test | `test_nb_static_refuses` | [tests/x6_stage1/test_b_nb_s0_ops.py:153](../../tests/x6_stage1/test_b_nb_s0_ops.py#L153) |  |
| `test_near_threshold_plus_fail_is_inconclusive` | test | `test_near_threshold_plus_fail_is_inconclusive` | [tests/analysis/test_x5_context.py:126](../../tests/analysis/test_x5_context.py#L126) |  |
| `test_near_unit_gap_is_inconclusive` | test | `test_near_unit_gap_is_inconclusive` | [tests/analysis/test_x5_context.py:122](../../tests/analysis/test_x5_context.py#L122) |  |
| `test_nearest_partners_excludes_self_duplicates_and_other_symbols` | test | `test_nearest_partners_excludes_self_duplicates_and_other_symbols` | [tests/analysis/test_horizon.py:139](../../tests/analysis/test_horizon.py#L139) |  |
| `test_needs_owner` | test | `test_needs_owner` | [tests/k4b/test_b_rerun.py:210](../../tests/k4b/test_b_rerun.py#L210) |  |
| `test_negative_alignment_label` | test | `test_negative_alignment_label` | [tests/k4b/test_a_decision.py:150](../../tests/k4b/test_a_decision.py#L150) |  |
| `test_never_pass_censored` | test | `test_never_pass_censored` | [tests/analysis/test_x5_endpoint.py:134](../../tests/analysis/test_x5_endpoint.py#L134) |  |
| `test_new_pools_record_lineage_and_execution_protocol` | test | `test_new_pools_record_lineage_and_execution_protocol` | [tests/experiment/test_x5g1t_identity.py:316](../../tests/experiment/test_x5g1t_identity.py#L316) |  |
| `test_no_circle_with_criterion_and_models` | test | `test_no_circle_with_criterion_and_models` | [tests/hwsb/test_a_outcomes.py:170](../../tests/hwsb/test_a_outcomes.py#L170) |  |
| `test_no_fit_logit_outside_m0_and_no_feas_logit` | test | `test_no_fit_logit_outside_m0_and_no_feas_logit` | [tests/c2_readout/test_b_policy.py:92](../../tests/c2_readout/test_b_policy.py#L92) |  |
| `test_no_fresh_access_without_release_b` | test | `test_no_fresh_access_without_release_b` | [tests/k4b/test_b_flow.py:236](../../tests/k4b/test_b_flow.py#L236) |  |
| `test_no_hits_pass` | test | `test_no_hits_pass` | [tests/k4b/test_b_flow.py:266](../../tests/k4b/test_b_flow.py#L266) |  |
| `test_no_hold_returns_none_and_writes_nothing` | test | `test_no_hold_returns_none_and_writes_nothing` | [tests/hwsb/test_b_hold.py:103](../../tests/hwsb/test_b_hold.py#L103) |  |
| `test_no_hold_returns_zero_without_sleep_or_audit` | test | `test_no_hold_returns_zero_without_sleep_or_audit` | [tests/experiment/test_x5g1t_runtime.py:221](../../tests/experiment/test_x5g1t_runtime.py#L221) |  |
| `test_no_hooks_by_default` | test | `test_no_hooks_by_default` | [tests/learner/test_patch.py:181](../../tests/learner/test_patch.py#L181) |  |
| `test_no_latch_blocking_sets_latch` | test | `test_no_latch_blocking_sets_latch` | [tests/experiment/test_x5g1t_usage.py:308](../../tests/experiment/test_x5g1t_usage.py#L308) |  |
| `test_no_latch_not_blocking_continues` | test | `test_no_latch_not_blocking_continues` | [tests/experiment/test_x5g1t_usage.py:325](../../tests/experiment/test_x5g1t_usage.py#L325) |  |
| `test_no_latch_warning_sets_latch_even_unavailable` | test | `test_no_latch_warning_sets_latch_even_unavailable` | [tests/experiment/test_x5g1t_usage.py:316](../../tests/experiment/test_x5g1t_usage.py#L316) |  |
| `test_no_logit_kind_at_calibration_gates_except_the_m0_identity_check` | test | `test_no_logit_kind_at_calibration_gates_except_the_m0_identity_check` | [tests/c1prime/test_a_gates.py:103](../../tests/c1prime/test_a_gates.py#L103) |  |
| `test_no_projection_before_step_1000` | test | `test_no_projection_before_step_1000` | [tests/hwsb/test_b_hold.py:37](../../tests/hwsb/test_b_hold.py#L37) |  |
| `test_no_qualifiers_for_outcomes_1_to_3` | test | `test_no_qualifiers_for_outcomes_1_to_3` | [tests/d2a/test_b_rules_qualifiers.py:225](../../tests/d2a/test_b_rules_qualifiers.py#L225) |  |
| `test_no_reading_fails_known_case` | test | `test_no_reading_fails_known_case` | [tests/hwsb/test_r_0170_kb2_status.py:68](../../tests/hwsb/test_r_0170_kb2_status.py#L68) |  |
| `test_no_release_session_falls_back_to_contract` | test | `test_no_release_session_falls_back_to_contract` | [tests/c1prime/test_c_release_worker.py:49](../../tests/c1prime/test_c_release_worker.py#L49) |  |
| `test_no_sealed_d2a_predicate` | test | `test_no_sealed_d2a_predicate` | [tests/x6_stage1/test_b_seed_pool_reg.py:326](../../tests/x6_stage1/test_b_seed_pool_reg.py#L326) |  |
| `test_no_second_claim_of_the_same_model_and_role` | test | `test_no_second_claim_of_the_same_model_and_role` | [tests/c1prime/test_a_chart_val.py:202](../../tests/c1prime/test_a_chart_val.py#L202) |  |
| `test_no_suitable_world_filter` | test | `test_no_suitable_world_filter` | [tests/hws/test_a_outcomes.py:230](../../tests/hws/test_a_outcomes.py#L230) |  |
| `test_no_suitable_world_headroom` | test | `test_no_suitable_world_headroom` | [tests/hws/test_a_outcomes.py:220](../../tests/hws/test_a_outcomes.py#L220) |  |
| `test_no_world_confirmed_needs_an_unresolved_world` | test | `test_no_world_confirmed_needs_an_unresolved_world` | [tests/hws/test_a_outcomes.py:201](../../tests/hws/test_a_outcomes.py#L201) |  |
| `test_noise_envelope_known_answer` | test | `test_noise_envelope_known_answer` | [tests/analysis/test_f1_rule.py:50](../../tests/analysis/test_f1_rule.py#L50) |  |
| `test_noise_envelope_matches_bruteforce_and_picks_max_cell` | test | `test_noise_envelope_matches_bruteforce_and_picks_max_cell` | [tests/analysis/test_f1_rule.py:58](../../tests/analysis/test_f1_rule.py#L58) |  |
| `test_noise_free_scalar_target_has_rho_one` | test | `test_noise_free_scalar_target_has_rho_one` | [tests/analysis/test_x4f_erasure.py:223](../../tests/analysis/test_x4f_erasure.py#L223) |  |
| `test_non_finite_f_is_technical` | test | `test_non_finite_f_is_technical` | [tests/c1prime/test_a_chart_exceptions.py:128](../../tests/c1prime/test_a_chart_exceptions.py#L128) |  |
| `test_non_finite_is_invalid` | test | `test_non_finite_is_invalid` | [tests/analysis/test_x5_context.py:81](../../tests/analysis/test_x5_context.py#L81) |  |
| `test_non_finite_replacement` | test | `test_non_finite_replacement` | [tests/learner/test_patch.py:261](../../tests/learner/test_patch.py#L261) |  |
| `test_non_metric_input_raises` | test | `test_non_metric_input_raises` | [tests/topology/test_persistence.py:177](../../tests/topology/test_persistence.py#L177) |  |
| `test_non_monotone_runs_of_two_do_not_qualify` | test | `test_non_monotone_runs_of_two_do_not_qualify` | [tests/analysis/test_x5_endpoint.py:111](../../tests/analysis/test_x5_endpoint.py#L111) |  |
| `test_non_permutation_perm_is_identity_failure` | test | `test_non_permutation_perm_is_identity_failure` | [tests/hwsb/test_b_process.py:149](../../tests/hwsb/test_b_process.py#L149) |  |
| `test_nondistribution_raises` | test | `test_nondistribution_raises` | [tests/topology/test_metrics.py:81](../../tests/topology/test_metrics.py#L81) |  |
| `test_none_latch_is_absence_sentinel_in_decision_but_malformed_for_latch_clears` | test | `test_none_latch_is_absence_sentinel_in_decision_but_malformed_for_latch_clears` | [tests/experiment/test_x5g1t_usage.py:373](../../tests/experiment/test_x5g1t_usage.py#L373) |  |
| `test_nonfinite_analysis_value_is_stored_as_inconclusive` | test | `test_nonfinite_analysis_value_is_stored_as_inconclusive` | [tests/experiment/test_runner.py:109](../../tests/experiment/test_runner.py#L109) |  |
| `test_nonstationary_start_breaks_the_identity` | test | `test_nonstationary_start_breaks_the_identity` | [tests/k4b/test_a_prop1.py:184](../../tests/k4b/test_a_prop1.py#L184) | Sanity of the enumerator: with z1 from a non-stationary start and the suffix filter |
| `test_norm_bound_adversarial_n_hat` | test | `test_norm_bound_adversarial_n_hat` | [tests/k4b/test_a_lemma_n.py:126](../../tests/k4b/test_a_lemma_n.py#L126) |  |
| `test_norm_bound_covers_perturbed_true_residual` | test | `test_norm_bound_covers_perturbed_true_residual` | [tests/k4b/test_a_lemma_n.py:160](../../tests/k4b/test_a_lemma_n.py#L160) | Lemma N soundness: every r* within eps4 + eps32 per coordinate of r~ is covered. |
| `test_norm_bound_exact_pythagorean` | test | `test_norm_bound_exact_pythagorean` | [tests/k4b/test_a_lemma_n.py:114](../../tests/k4b/test_a_lemma_n.py#L114) |  |
| `test_norm_bound_irrational_norms` | test | `test_norm_bound_irrational_norms` | [tests/k4b/test_a_lemma_n.py:135](../../tests/k4b/test_a_lemma_n.py#L135) |  |
| `test_norm_bound_other_K_uses_its_envelope` | test | `test_norm_bound_other_K_uses_its_envelope` | [tests/k4b/test_a_lemma_n.py:176](../../tests/k4b/test_a_lemma_n.py#L176) |  |
| `test_norm_bound_s_zero` | test | `test_norm_bound_s_zero` | [tests/k4b/test_a_lemma_n.py:103](../../tests/k4b/test_a_lemma_n.py#L103) |  |
| `test_norm_bound_tiny_values` | test | `test_norm_bound_tiny_values` | [tests/k4b/test_a_lemma_n.py:148](../../tests/k4b/test_a_lemma_n.py#L148) |  |
| `test_normal95_and_bootstrap_kernel` | test | `test_normal95_and_bootstrap_kernel` | [tests/hws/test_a_stats.py:133](../../tests/hws/test_a_stats.py#L133) |  |
| `test_normal_export_single_save_and_manifest` | test | `test_normal_export_single_save_and_manifest` | [tests/experiment/test_x5g1_export_integration.py:149](../../tests/experiment/test_x5g1_export_integration.py#L149) |  |
| `test_not_cocycle_mod_p_is_invalid_before_any_cap` | test | `test_not_cocycle_mod_p_is_invalid_before_any_cap` | [tests/circle_history/test_cochain_lift.py:208](../../tests/circle_history/test_cochain_lift.py#L208) |  |
| `test_not_learned_with_k` | test | `test_not_learned_with_k` | [tests/hwsb/test_a_outcomes.py:156](../../tests/hwsb/test_a_outcomes.py#L156) |  |
| `test_not_yet_overdue_and_disk_only_every_eighth_poll` | test | `test_not_yet_overdue_and_disk_only_every_eighth_poll` | [tests/k4b/test_b_meter.py:238](../../tests/k4b/test_b_meter.py#L238) |  |
| `test_notebook_sha_binding` | test | `test_notebook_sha_binding` | [tests/x6_stage1/test_b_nb_s0_ops.py:260](../../tests/x6_stage1/test_b_nb_s0_ops.py#L260) |  |
| `test_notebook_static_independent_and_nb_static` | test | `test_notebook_static_independent_and_nb_static` | [tests/x6_stage1/test_b_nb_s0_ops.py:130](../../tests/x6_stage1/test_b_nb_s0_ops.py#L130) |  |
| `test_nuisance_predictive_fixture_fails_the_incremental_link` | test | `test_nuisance_predictive_fixture_fails_the_incremental_link` | [tests/c2_readout/test_b_fwl_l1.py:260](../../tests/c2_readout/test_b_fwl_l1.py#L260) |  |
| `test_null_and_swap_identities_on_short_histories` | test | `test_null_and_swap_identities_on_short_histories` | [tests/x2a_stage0/test_x2a_stage0.py:322](../../tests/x2a_stage0/test_x2a_stage0.py#L322) |  |
| `test_null_clouds_contract` | test | `test_null_clouds_contract` | [tests/topology/test_shapes_calibration.py:38](../../tests/topology/test_shapes_calibration.py#L38) |  |
| `test_null_projector_is_the_orthogonal_projector_onto_ker_CM` | test | `test_null_projector_is_the_orthogonal_projector_onto_ker_CM` | [tests/c2_readout/test_a_partition.py:128](../../tests/c2_readout/test_a_partition.py#L128) |  |
| `test_null_z_se_zero_cases` | test | `test_null_z_se_zero_cases` | [tests/hws/test_a_stats.py:149](../../tests/hws/test_a_stats.py#L149) |  |
| `test_null_z_threshold_is_strict` | test | `test_null_z_threshold_is_strict` | [tests/hws/test_a_stats.py:156](../../tests/hws/test_a_stats.py#L156) |  |
| `test_numerical_identity_record_is_deterministic` | test | `test_numerical_identity_record_is_deterministic` | [tests/circle_history/test_builder_v24_runtime.py:213](../../tests/circle_history/test_builder_v24_runtime.py#L213) |  |
| `test_O01_belief_at_matches_run` | test | `test_O01_belief_at_matches_run` | [tests/oracle/test_oracle.py:82](../../tests/oracle/test_oracle.py#L82) |  |
| `test_O01_bruteforce_all_length4_sequences` | test | `test_O01_bruteforce_all_length4_sequences` | [tests/oracle/test_oracle.py:47](../../tests/oracle/test_oracle.py#L47) |  |
| `test_O01_evidence_is_sum_of_ce` | test | `test_O01_evidence_is_sum_of_ce` | [tests/oracle/test_oracle.py:92](../../tests/oracle/test_oracle.py#L92) |  |
| `test_O02_q0_is_pi_E` | test | `test_O02_q0_is_pi_E` | [tests/oracle/test_oracle.py:114](../../tests/oracle/test_oracle.py#L114) |  |
| `test_O03_unique_emission_belief_is_delta` | test | `test_O03_unique_emission_belief_is_delta` | [tests/oracle/test_oracle.py:128](../../tests/oracle/test_oracle.py#L128) |  |
| `test_O04_uniform_emission_beliefs_stay_pi` | test | `test_O04_uniform_emission_beliefs_stay_pi` | [tests/oracle/test_oracle.py:149](../../tests/oracle/test_oracle.py#L149) |  |
| `test_O05_F1_F2` | test | `test_O05_F1_F2` | [tests/oracle/test_oracle.py:160](../../tests/oracle/test_oracle.py#L160) |  |
| `test_O05_F2_from_prior_matches_brute_force` | test | `test_O05_F2_from_prior_matches_brute_force` | [tests/oracle/test_oracle.py:179](../../tests/oracle/test_oracle.py#L179) |  |
| `test_O06_last_symbol_posterior` | test | `test_O06_last_symbol_posterior` | [tests/oracle/test_oracle.py:188](../../tests/oracle/test_oracle.py#L188) |  |
| `test_O07_context_gain_nonneg_and_zero` | test | `test_O07_context_gain_nonneg_and_zero` | [tests/oracle/test_oracle.py:207](../../tests/oracle/test_oracle.py#L207) |  |
| `test_O08_impossible_history_raises` | test | `test_O08_impossible_history_raises` | [tests/oracle/test_oracle.py:228](../../tests/oracle/test_oracle.py#L228) |  |
| `test_O09_long_near_deterministic_no_underflow` | test | `test_O09_long_near_deterministic_no_underflow` | [tests/oracle/test_oracle.py:263](../../tests/oracle/test_oracle.py#L263) |  |
| `test_O10_observability_ranks` | test | `test_O10_observability_ranks` | [tests/oracle/test_oracle.py:286](../../tests/oracle/test_oracle.py#L286) |  |
| `test_O11_policy_refuses_sidecar_for_oracle` | test | `test_O11_policy_refuses_sidecar_for_oracle` | [tests/oracle/test_oracle.py:304](../../tests/oracle/test_oracle.py#L304) |  |
| `test_oblique_eraser_keeps_orthogonal_signal` | test | `test_oblique_eraser_keeps_orthogonal_signal` | [tests/analysis/test_x4f_erasure.py:187](../../tests/analysis/test_x4f_erasure.py#L187) |  |
| `test_oblique_eraser_planted_2d_target` | test | `test_oblique_eraser_planted_2d_target` | [tests/analysis/test_x4f_erasure.py:166](../../tests/analysis/test_x4f_erasure.py#L166) |  |
| `test_obs_variant_helper_is_a_faithful_copy` | test | `test_obs_variant_helper_is_a_faithful_copy` | [tests/experiment/test_x5g1t_identity.py:276](../../tests/experiment/test_x5g1t_identity.py#L276) | Control for the content variants: a re-save with nothing changed still trains. |
| `test_observation_set_store_is_scanned_via_source_f` | test | `test_observation_set_store_is_scanned_via_source_f` | [tests/k4b/test_b_registry_rules.py:249](../../tests/k4b/test_b_registry_rules.py#L249) |  |
| `test_observation_set_without_emission_parent_fails_closed` | test | `test_observation_set_without_emission_parent_fails_closed` | [tests/hwsb/test_b_registry.py:173](../../tests/hwsb/test_b_registry.py#L173) |  |
| `test_observed_empty_limits_is_not_blocking` | test | `test_observed_empty_limits_is_not_blocking` | [tests/experiment/test_x5g1t_usage.py:146](../../tests/experiment/test_x5g1t_usage.py#L146) |  |
| `test_off_grid_rows_form_no_donor` | test | `test_off_grid_rows_form_no_donor` | [tests/c2_readout/test_b_registry.py:163](../../tests/c2_readout/test_b_registry.py#L163) |  |
| `test_off_grid_rule_never_clamps_or_wraps_and_forms_no_HY` | test | `test_off_grid_rule_never_clamps_or_wraps_and_forms_no_HY` | [tests/c2_readout/test_a_oracle.py:133](../../tests/c2_readout/test_a_oracle.py#L133) |  |
| `test_offset_comparison_is_by_instant_not_text` | test | `test_offset_comparison_is_by_instant_not_text` | [tests/experiment/test_x5g1t_usage.py:212](../../tests/experiment/test_x5g1t_usage.py#L212) |  |
| `test_older_or_equal_evidence_is_stale` | test | `test_older_or_equal_evidence_is_stale` | [tests/experiment/test_x5g1t_usage.py:208](../../tests/experiment/test_x5g1t_usage.py#L208) |  |
| `test_one_fail_other_pass_is_weak_context` | test | `test_one_fail_other_pass_is_weak_context` | [tests/analysis/test_x5_context.py:146](../../tests/analysis/test_x5_context.py#L146) |  |
| `test_one_failing_replicate_among_three_is_enough_to_reject` | test | `test_one_failing_replicate_among_three_is_enough_to_reject` | [tests/analysis/test_f1_rule.py:149](../../tests/analysis/test_f1_rule.py#L149) |  |
| `test_one_file_outside_the_segment_spoils_the_directory` | test | `test_one_file_outside_the_segment_spoils_the_directory` | [tests/k4b/test_b_registry_rules.py:165](../../tests/k4b/test_b_registry_rules.py#L165) |  |
| `test_one_large_array_in_a_small_file_is_incomplete` | test | `test_one_large_array_in_a_small_file_is_incomplete` | [tests/k4b/test_b_registry_rules.py:138](../../tests/k4b/test_b_registry_rules.py#L138) |  |
| `test_one_of_two_latched_kinds_missing` | test | `test_one_of_two_latched_kinds_missing` | [tests/experiment/test_x5g1t_usage.py:251](../../tests/experiment/test_x5g1t_usage.py#L251) |  |
| `test_op_guard_deadline_is_per_operation` | test | `test_op_guard_deadline_is_per_operation` | [tests/k4b/test_b_meter.py:131](../../tests/k4b/test_b_meter.py#L131) |  |
| `test_open_ledgers_two_files` | test | `test_open_ledgers_two_files` | [tests/k4b/test_b_charts.py:157](../../tests/k4b/test_b_charts.py#L157) |  |
| `test_operation_is_the_originating_function` | test | `test_operation_is_the_originating_function` | [tests/c1prime/test_a_exceptions.py:173](../../tests/c1prime/test_a_exceptions.py#L173) |  |
| `test_operator_decomposition_sums_and_converts_null_source_variation` | test | `test_operator_decomposition_sums_and_converts_null_source_variation` | [tests/c2_readout/test_a_partition.py:139](../../tests/c2_readout/test_a_partition.py#L139) |  |
| `test_opposition_fixture_rc4_not_used_with_negative_qualifier_and_licence` | test | `test_opposition_fixture_rc4_not_used_with_negative_qualifier_and_licence` | [tests/c2_readout/test_a_partition.py:258](../../tests/c2_readout/test_a_partition.py#L258) |  |
| `test_oracle_equals_bayes_filter_on_w1_to_w32` | test | `test_oracle_equals_bayes_filter_on_w1_to_w32` | [tests/experiment/test_x5g1t_lineage_oracle.py:230](../../tests/experiment/test_x5g1t_lineage_oracle.py#L230) |  |
| `test_oracle_guard_and_batch_invariance` | test | `test_oracle_guard_and_batch_invariance` | [tests/experiment/test_x5g1t_lineage_oracle.py:257](../../tests/experiment/test_x5g1t_lineage_oracle.py#L257) |  |
| `test_oracle_identities` | test | `test_oracle_identities` | [tests/d2a/test_a_targets.py:192](../../tests/d2a/test_a_targets.py#L192) |  |
| `test_oracle_ignores_column_33` | test | `test_oracle_ignores_column_33` | [tests/experiment/test_x5g1t_lineage_oracle.py:238](../../tests/experiment/test_x5g1t_lineage_oracle.py#L238) |  |
| `test_oracle_moments_equals_posterior_means_and_decimal_reference` | test | `test_oracle_moments_equals_posterior_means_and_decimal_reference` | [tests/circle_history/test_scores_precision.py:121](../../tests/circle_history/test_scores_precision.py#L121) |  |
| `test_oracle_moments_rejects_any_width_but_32` | test | `test_oracle_moments_rejects_any_width_but_32` | [tests/circle_history/test_scores_precision.py:137](../../tests/circle_history/test_scores_precision.py#L137) |  |
| `test_oracle_named_equals_canonical_under_perm` | test | `test_oracle_named_equals_canonical_under_perm` | [tests/experiment/test_x5g1t_lineage_oracle.py:248](../../tests/experiment/test_x5g1t_lineage_oracle.py#L248) |  |
| `test_oracle_perfect_readout_gives_G_minus_mass_correction` | test | `test_oracle_perfect_readout_gives_G_minus_mass_correction` | [tests/c1prime/test_b_identities.py:170](../../tests/c1prime/test_b_identities.py#L170) |  |
| `test_oracle_persists_bound_reference` | test | `test_oracle_persists_bound_reference` | [tests/circle_history/test_builder_v24_stages.py:89](../../tests/circle_history/test_builder_v24_stages.py#L89) |  |
| `test_oracle_predictions_reproduce_and_resolve` | test | `test_oracle_predictions_reproduce_and_resolve` | [tests/d2a/test_b_behaviour.py:48](../../tests/d2a/test_b_behaviour.py#L48) |  |
| `test_oracle_predictor_and_qstar_codes` | test | `test_oracle_predictor_and_qstar_codes` | [tests/x6_stage1/test_a_eval.py:136](../../tests/x6_stage1/test_a_eval.py#L136) |  |
| `test_oracle_split_HY_by_exact_forward_eligibility_f_y_and_x_leakage` | test | `test_oracle_split_HY_by_exact_forward_eligibility_f_y_and_x_leakage` | [tests/c2_readout/test_a_oracle.py:159](../../tests/c2_readout/test_a_oracle.py#L159) |  |
| `test_ord_d_missing_model_fails_the_seed` | test | `test_ord_d_missing_model_fails_the_seed` | [tests/x6_stage1/test_a_rules.py:143](../../tests/x6_stage1/test_a_rules.py#L143) |  |
| `test_ord_d_pass_fail_and_regret_bar_exact` | test | `test_ord_d_pass_fail_and_regret_bar_exact` | [tests/x6_stage1/test_a_rules.py:102](../../tests/x6_stage1/test_a_rules.py#L102) |  |
| `test_ord_d_unresolved_routing` | test | `test_ord_d_unresolved_routing` | [tests/x6_stage1/test_a_rules.py:134](../../tests/x6_stage1/test_a_rules.py#L134) |  |
| `test_ordinary_overdue_beats_disk_and_returns_control_state` | test | `test_ordinary_overdue_beats_disk_and_returns_control_state` | [tests/k4b/test_b_meter.py:228](../../tests/k4b/test_b_meter.py#L228) |  |
| `test_orthogonal_movement_fixture_gives_zero_share_low_aligned` | test | `test_orthogonal_movement_fixture_gives_zero_share_low_aligned` | [tests/c2_readout/test_a_partition.py:239](../../tests/c2_readout/test_a_partition.py#L239) |  |
| `test_osum_is_left_to_right` | test | `test_osum_is_left_to_right` | [tests/c1prime/test_b_cert_guards.py:96](../../tests/c1prime/test_b_cert_guards.py#L96) |  |
| `test_other_circumferences_build` | test | `test_other_circumferences_build` | [tests/hws/test_b_worlds.py:169](../../tests/hws/test_b_worlds.py#L169) |  |
| `test_other_models_meta_fails_on_every_model_bound_field` | test | `test_other_models_meta_fails_on_every_model_bound_field` | [tests/k4b/test_b_h1_meta.py:236](../../tests/k4b/test_b_h1_meta.py#L236) | 2718's complete meta checked against 1729's expectation: id, run_key, seed, payload. |
| `test_other_relevant_limit_blocking_prevents_clear` | test | `test_other_relevant_limit_blocking_prevents_clear` | [tests/experiment/test_x5g1t_usage.py:262](../../tests/experiment/test_x5g1t_usage.py#L262) |  |
| `test_other_stage_failures_keep_code_and_message` | test | `test_other_stage_failures_keep_code_and_message` | [tests/c1prime/test_a_exceptions.py:137](../../tests/c1prime/test_a_exceptions.py#L137) |  |
| `test_OUT_is_exact` | test | `test_OUT_is_exact` | [tests/c1prime/test_b_cert_guards.py:91](../../tests/c1prime/test_b_cert_guards.py#L91) |  |
| `test_out_of_code_and_excluded_direction_fixtures` | test | `test_out_of_code_and_excluded_direction_fixtures` | [tests/c2_readout/test_a_scope.py:177](../../tests/c2_readout/test_a_scope.py#L177) |  |
| `test_out_of_order_gates_are_refused` | test | `test_out_of_order_gates_are_refused` | [tests/c2_readout/test_b_policy.py:121](../../tests/c2_readout/test_b_policy.py#L121) |  |
| `test_out_of_order_stage_refused_without_gate` | test | `test_out_of_order_stage_refused_without_gate` | [tests/circle_history/test_builder_v24_stages.py:43](../../tests/circle_history/test_builder_v24_stages.py#L43) |  |
| `test_outcome_fallthrough_is_fail_technical_outcome` | test | `test_outcome_fallthrough_is_fail_technical_outcome` | [tests/hws/test_a_outcomes.py:248](../../tests/hws/test_a_outcomes.py#L248) |  |
| `test_outcome_path_and_roundtrip` | test | `test_outcome_path_and_roundtrip` | [tests/experiment/test_x5g1t_runtime_boundary.py:79](../../tests/experiment/test_x5g1t_runtime_boundary.py#L79) |  |
| `test_output_cap_reason_is_a_resource_stop` | test | `test_output_cap_reason_is_a_resource_stop` | [tests/k4b/test_b_meter.py:301](../../tests/k4b/test_b_meter.py#L301) |  |
| `test_output_dir_new_path_is_created` | test | `test_output_dir_new_path_is_created` | [tests/experiment/test_x5g1_safety.py:226](../../tests/experiment/test_x5g1_safety.py#L226) |  |
| `test_output_dir_non_empty_raises_and_is_untouched` | test | `test_output_dir_non_empty_raises_and_is_untouched` | [tests/experiment/test_x5g1_safety.py:237](../../tests/experiment/test_x5g1_safety.py#L237) |  |
| `test_outward_inputs_exact` | test | `test_outward_inputs_exact` | [tests/x6_stage1/test_a_numerics.py:212](../../tests/x6_stage1/test_a_numerics.py#L212) |  |
| `test_overall_and_strict_verdicts` | test | `test_overall_and_strict_verdicts` | [tests/analysis/test_horizon.py:182](../../tests/analysis/test_horizon.py#L182) |  |
| `test_overall_resultant_known_answers` | test | `test_overall_resultant_known_answers` | [tests/circle_history/test_chart_extension.py:298](../../tests/circle_history/test_chart_extension.py#L298) |  |
| `test_overall_rule` | test | `test_overall_rule` | [tests/c1prime/test_b_inference.py:106](../../tests/c1prime/test_b_inference.py#L106) |  |
| `test_overall_table` | test | `test_overall_table` | [tests/k4b/test_a_decision.py:179](../../tests/k4b/test_a_decision.py#L179) |  |
| `test_overall_two_of_three_rules` | test | `test_overall_two_of_three_rules` | [tests/c2_readout/test_a_inference.py:254](../../tests/c2_readout/test_a_inference.py#L254) |  |
| `test_own_declarations_are_not_prior_use` | test | `test_own_declarations_are_not_prior_use` | [tests/k4b/test_b_flow.py:258](../../tests/k4b/test_b_flow.py#L258) |  |
| `test_own_pre_g0_records_admitted_at_s1` | test | `test_own_pre_g0_records_admitted_at_s1` | [tests/c2_readout/test_b_fwl_l1.py:358](../../tests/c2_readout/test_b_fwl_l1.py#L358) |  |
| `test_own_readers_excludes_k4b_store_from_the_deep_scan` | test | `test_own_readers_excludes_k4b_store_from_the_deep_scan` | [tests/k4b/test_b_store_reader.py:217](../../tests/k4b/test_b_store_reader.py#L217) |  |
| `test_own_records_near_misses_are_not_admitted` | test | `test_own_records_near_misses_are_not_admitted` | [tests/c2_readout/test_b_fwl_l1.py:378](../../tests/c2_readout/test_b_fwl_l1.py#L378) |  |
| `test_P01_square_n3_hand_values` | test | `test_P01_square_n3_hand_values` | [tests/process/test_transition.py:22](../../tests/process/test_transition.py#L22) |  |
| `test_P02_cylinder_n3_no_corners_and_wrap` | test | `test_P02_cylinder_n3_no_corners_and_wrap` | [tests/process/test_transition.py:37](../../tests/process/test_transition.py#L37) |  |
| `test_P03_contract_invariants` | test | `test_P03_contract_invariants` | [tests/process/test_transition.py:54](../../tests/process/test_transition.py#L54) |  |
| `test_P04_cylinder_x_distance_is_periodic` | test | `test_P04_cylinder_x_distance_is_periodic` | [tests/process/test_overlap.py:46](../../tests/process/test_overlap.py#L46) |  |
| `test_P04_rows_sum_to_one_and_direct_formula_square` | test | `test_P04_rows_sum_to_one_and_direct_formula_square` | [tests/process/test_overlap.py:32](../../tests/process/test_overlap.py#L32) |  |
| `test_P05_factorizes_on_core_worlds` | test | `test_P05_factorizes_on_core_worlds` | [tests/process/test_overlap.py:66](../../tests/process/test_overlap.py#L66) |  |
| `test_P06_axis_permuted_preserves_rows_and_structure` | test | `test_P06_axis_permuted_preserves_rows_and_structure` | [tests/process/test_controls.py:50](../../tests/process/test_controls.py#L50) |  |
| `test_P06_full_permutation_keeps_rows_but_not_product` | test | `test_P06_full_permutation_keeps_rows_but_not_product` | [tests/process/test_controls.py:66](../../tests/process/test_controls.py#L66) |  |
| `test_P06_row_multiset_check_error_path` | test | `test_P06_row_multiset_check_error_path` | [tests/process/test_controls.py:80](../../tests/process/test_controls.py#L80) |  |
| `test_P07_permutations_depend_on_world_not_replicate` | test | `test_P07_permutations_depend_on_world_not_replicate` | [tests/process/test_controls.py:90](../../tests/process/test_controls.py#L90) |  |
| `test_P08_identical_all_rows_equal` | test | `test_P08_identical_all_rows_equal` | [tests/process/test_controls.py:102](../../tests/process/test_controls.py#L102) |  |
| `test_P08_unique_is_permutation_matrix` | test | `test_P08_unique_is_permutation_matrix` | [tests/process/test_controls.py:110](../../tests/process/test_controls.py#L110) |  |
| `test_P09_symbol_names_permute_columns_only` | test | `test_P09_symbol_names_permute_columns_only` | [tests/process/test_overlap.py:89](../../tests/process/test_overlap.py#L89) |  |
| `test_p0_constants_in_exact_rationals` | test | `test_p0_constants_in_exact_rationals` | [tests/c1prime/test_b_cert_oracle.py:333](../../tests/c1prime/test_b_cert_oracle.py#L333) |  |
| `test_p0_failures` | test | `test_p0_failures` | [tests/c1prime/test_b_cert_oracle.py:356](../../tests/c1prime/test_b_cert_oracle.py#L356) |  |
| `test_P10_center_outside_chart_raises` | test | `test_P10_center_outside_chart_raises` | [tests/process/test_overlap.py:117](../../tests/process/test_overlap.py#L117) |  |
| `test_P10_dead_symbol_helper_and_constructed_build` | test | `test_P10_dead_symbol_helper_and_constructed_build` | [tests/process/test_overlap.py:126](../../tests/process/test_overlap.py#L126) |  |
| `test_P10_nonpositive_sigma_raises` | test | `test_P10_nonpositive_sigma_raises` | [tests/process/test_overlap.py:111](../../tests/process/test_overlap.py#L111) |  |
| `test_P11_emission_builder_does_not_accept_transition` | test | `test_P11_emission_builder_does_not_accept_transition` | [tests/process/test_controls.py:123](../../tests/process/test_controls.py#L123) |  |
| `test_P11_transition_builder_does_not_accept_emission` | test | `test_P11_transition_builder_does_not_accept_emission` | [tests/process/test_transition.py:102](../../tests/process/test_transition.py#L102) |  |
| `test_P12_fps_greedy_maxmin_by_hand` | test | `test_P12_fps_greedy_maxmin_by_hand` | [tests/process/test_controls.py:134](../../tests/process/test_controls.py#L134) |  |
| `test_P13_core_worlds` | test | `test_P13_core_worlds` | [tests/process/test_geometry.py:16](../../tests/process/test_geometry.py#L16) |  |
| `test_P13_family_name_is_ignored` | test | `test_P13_family_name_is_ignored` | [tests/process/test_geometry.py:21](../../tests/process/test_geometry.py#L21) |  |
| `test_P13_flipped_wrap_is_not_periodic` | test | `test_P13_flipped_wrap_is_not_periodic` | [tests/process/test_geometry.py:31](../../tests/process/test_geometry.py#L31) | Möbius-style crossed wrap edges (11, y) ~ (0, 11 - y) do not make axis 0 periodic. |
| `test_P13_partial_or_declared_without_edges_raises` | test | `test_P13_partial_or_declared_without_edges_raises` | [tests/process/test_geometry.py:39](../../tests/process/test_geometry.py#L39) |  |
| `test_p1_calls_kernels_with_the_registered_cfg_and_seeds` | test | `test_p1_calls_kernels_with_the_registered_cfg_and_seeds` | [tests/c2_readout/test_a_oracle.py:359](../../tests/c2_readout/test_a_oracle.py#L359) |  |
| `test_p1_is_an_exact_rational_threshold` | test | `test_p1_is_an_exact_rational_threshold` | [tests/c1prime/test_b_cert_oracle.py:270](../../tests/c1prime/test_b_cert_oracle.py#L270) |  |
| `test_p1_n_f_rules_and_precision_limited` | test | `test_p1_n_f_rules_and_precision_limited` | [tests/c2_readout/test_a_oracle.py:390](../../tests/c2_readout/test_a_oracle.py#L390) |  |
| `test_p2_analogue` | test | `test_p2_analogue` | [tests/k4b/test_a_lemma_n.py:263](../../tests/k4b/test_a_lemma_n.py#L263) |  |
| `test_p32_requires_33_inputs` | test | `test_p32_requires_33_inputs` | [tests/experiment/test_x5g1t_lineage_oracle.py:312](../../tests/experiment/test_x5g1t_lineage_oracle.py#L312) |  |
| `test_p3_p4_a3_labels` | test | `test_p3_p4_a3_labels` | [tests/x2a_stage0/test_x2a_stage0_ph.py:132](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L132) |  |
| `test_p4_boundary_and_a_discrepancy_above_one_half` | test | `test_p4_boundary_and_a_discrepancy_above_one_half` | [tests/c1prime/test_b_cert_oracle.py:199](../../tests/c1prime/test_b_cert_oracle.py#L199) |  |
| `test_p_d2a_equals_brute_force_on_the_tiny_world` | test | `test_p_d2a_equals_brute_force_on_the_tiny_world` | [tests/hws/test_b_exact.py:79](../../tests/hws/test_b_exact.py#L79) |  |
| `test_p_d2a_equals_exact_fractions_on_a_rational_hmm` | test | `test_p_d2a_equals_exact_fractions_on_a_rational_hmm` | [tests/hws/test_b_exact.py:96](../../tests/hws/test_b_exact.py#L96) |  |
| `test_p_d2a_full_alphabet_and_symbols_beyond_v` | test | `test_p_d2a_full_alphabet_and_symbols_beyond_v` | [tests/hws/test_b_exact.py:86](../../tests/hws/test_b_exact.py#L86) |  |
| `test_p_stay_changes_values_only_by_formula` | test | `test_p_stay_changes_values_only_by_formula` | [tests/process/test_transition.py:71](../../tests/process/test_transition.py#L71) |  |
| `test_p_value_has_plus_one_form` | test | `test_p_value_has_plus_one_form` | [tests/analysis/test_baselines_dynamics.py:96](../../tests/analysis/test_baselines_dynamics.py#L96) |  |
| `test_p_value_matches_independent_monte_carlo` | test | `test_p_value_matches_independent_monte_carlo` | [tests/analysis/test_baselines_dynamics.py:109](../../tests/analysis/test_baselines_dynamics.py#L109) |  |
| `test_pad` | test | `test_pad` | [tests/d2a/test_a_world.py:166](../../tests/d2a/test_a_world.py#L166) |  |
| `test_pad_and_model_inputs` | test | `test_pad_and_model_inputs` | [tests/x6_stage1/test_a_eval.py:75](../../tests/x6_stage1/test_a_eval.py#L75) |  |
| `test_padding_independence` | test | `test_padding_independence` | [tests/x6_stage1/test_a_eval.py:104](../../tests/x6_stage1/test_a_eval.py#L104) |  |
| `test_pair_evidence_deterministic_observed` | test | `test_pair_evidence_deterministic_observed` | [tests/analysis/test_x5_endpoint_bootstrap.py:188](../../tests/analysis/test_x5_endpoint_bootstrap.py#L188) |  |
| `test_pair_evidence_point_from_full_sample_and_quantiles_from_bootstrap` | test | `test_pair_evidence_point_from_full_sample_and_quantiles_from_bootstrap` | [tests/analysis/test_x5_endpoint_bootstrap.py:177](../../tests/analysis/test_x5_endpoint_bootstrap.py#L177) |  |
| `test_pair_flags` | test | `test_pair_flags` | [tests/analysis/test_x5_endpoint_bootstrap.py:218](../../tests/analysis/test_x5_endpoint_bootstrap.py#L218) |  |
| `test_pair_terms_hand_values` | test | `test_pair_terms_hand_values` | [tests/x6_stage1/test_a_pairs.py:284](../../tests/x6_stage1/test_a_pairs.py#L284) |  |
| `test_paired_arms_share_first_symbol_and_misuse_is_detected` | test | `test_paired_arms_share_first_symbol_and_misuse_is_detected` | [tests/experiment/test_x5g1_lineage.py:77](../../tests/experiment/test_x5g1_lineage.py#L77) |  |
| `test_paired_generators_distinct_objects_identical_draws` | test | `test_paired_generators_distinct_objects_identical_draws` | [tests/experiment/test_x5g1_lineage.py:68](../../tests/experiment/test_x5g1_lineage.py#L68) |  |
| `test_paired_generators_invalid` | test | `test_paired_generators_invalid` | [tests/experiment/test_x5g1t_lineage_oracle.py:117](../../tests/experiment/test_x5g1t_lineage_oracle.py#L117) |  |
| `test_paired_generators_separate_and_identical` | test | `test_paired_generators_separate_and_identical` | [tests/experiment/test_x5g1t_lineage_oracle.py:98](../../tests/experiment/test_x5g1t_lineage_oracle.py#L98) |  |
| `test_paired_generators_test_split_uses_seed_zero` | test | `test_paired_generators_test_split_uses_seed_zero` | [tests/experiment/test_x5g1t_lineage_oracle.py:108](../../tests/experiment/test_x5g1t_lineage_oracle.py#L108) |  |
| `test_panel_config_sizes_and_too_few_trajectories` | test | `test_panel_config_sizes_and_too_few_trajectories` | [tests/dataset/test_panels.py:52](../../tests/dataset/test_panels.py#L52) |  |
| `test_panel_outside_calibration_validation_denied_before_any_load` | test | `test_panel_outside_calibration_validation_denied_before_any_load` | [tests/circle_history/test_adapter.py:204](../../tests/circle_history/test_adapter.py#L204) |  |
| `test_panels_follow_rank_in_block` | test | `test_panels_follow_rank_in_block` | [tests/c1prime/test_b_registry.py:90](../../tests/c1prime/test_b_registry.py#L90) |  |
| `test_panels_rows_in_history_id_order_without_w33` | test | `test_panels_rows_in_history_id_order_without_w33` | [tests/circle_history/test_adapter.py:175](../../tests/circle_history/test_adapter.py#L175) |  |
| `test_parameters_and_buffers_bitwise_unchanged` | test | `test_parameters_and_buffers_bitwise_unchanged` | [tests/learner/test_patch.py:189](../../tests/learner/test_patch.py#L189) |  |
| `test_parse_model` | test | `test_parse_model` | [tests/x6_stage1/test_b_seed_pool_reg.py:113](../../tests/x6_stage1/test_b_seed_pool_reg.py#L113) |  |
| `test_parse_model_refuses` | test | `test_parse_model_refuses` | [tests/x6_stage1/test_b_seed_pool_reg.py:118](../../tests/x6_stage1/test_b_seed_pool_reg.py#L118) |  |
| `test_parse_utc_offsets` | test | `test_parse_utc_offsets` | [tests/experiment/test_x5g1t_usage.py:84](../../tests/experiment/test_x5g1t_usage.py#L84) |  |
| `test_parse_utc_powershell_seven_digits` | test | `test_parse_utc_powershell_seven_digits` | [tests/experiment/test_x5g1t_usage.py:92](../../tests/experiment/test_x5g1t_usage.py#L92) |  |
| `test_parse_utc_rejects` | test | `test_parse_utc_rejects` | [tests/experiment/test_x5g1t_usage.py:103](../../tests/experiment/test_x5g1t_usage.py#L103) |  |
| `test_partition_sums_exactly_and_matches_closed_forms` | test | `test_partition_sums_exactly_and_matches_closed_forms` | [tests/c2_readout/test_a_partition.py:81](../../tests/c2_readout/test_a_partition.py#L81) |  |
| `test_partner_and_bootstrap_streams` | test | `test_partner_and_bootstrap_streams` | [tests/x6_stage1/test_b_seed_pool_reg.py:98](../../tests/x6_stage1/test_b_seed_pool_reg.py#L98) |  |
| `test_partner_full_tables_t32` | test | `test_partner_full_tables_t32` | [tests/x6_stage1/test_a_pairs.py:267](../../tests/x6_stage1/test_a_pairs.py#L267) |  |
| `test_partner_key_probability_validity_and_determinism` | test | `test_partner_key_probability_validity_and_determinism` | [tests/x6_stage1/test_a_pairs.py:233](../../tests/x6_stage1/test_a_pairs.py#L233) |  |
| `test_partner_seed_is_registered_stream` | test | `test_partner_seed_is_registered_stream` | [tests/x6_stage1/test_a_pairs.py:227](../../tests/x6_stage1/test_a_pairs.py#L227) |  |
| `test_partners_batch_rows_and_padding` | test | `test_partners_batch_rows_and_padding` | [tests/x6_stage1/test_a_pairs.py:254](../../tests/x6_stage1/test_a_pairs.py#L254) |  |
| `test_pass_at_4750_only_censored` | test | `test_pass_at_4750_only_censored` | [tests/analysis/test_x5_endpoint.py:130](../../tests/analysis/test_x5_endpoint.py#L130) |  |
| `test_pass_needs_every_gate` | test | `test_pass_needs_every_gate` | [tests/hwsb/test_a_outcomes.py:195](../../tests/hwsb/test_a_outcomes.py#L195) |  |
| `test_pass_only_at_5000_censored` | test | `test_pass_only_at_5000_censored` | [tests/analysis/test_x5_endpoint.py:126](../../tests/analysis/test_x5_endpoint.py#L126) |  |
| `test_pass_sequence_custom_threshold` | test | `test_pass_sequence_custom_threshold` | [tests/analysis/test_x5_endpoint.py:83](../../tests/analysis/test_x5_endpoint.py#L83) |  |
| `test_pass_sequence_rejects_nan` | test | `test_pass_sequence_rejects_nan` | [tests/analysis/test_x5_endpoint.py:87](../../tests/analysis/test_x5_endpoint.py#L87) |  |
| `test_pass_sequence_threshold_equality_passes` | test | `test_pass_sequence_threshold_equality_passes` | [tests/analysis/test_x5_endpoint.py:77](../../tests/analysis/test_x5_endpoint.py#L77) |  |
| `test_patch_matches_spec_reference_computation` | test | `test_patch_matches_spec_reference_computation` | [tests/learner/test_patch.py:103](../../tests/learner/test_patch.py#L103) |  |
| `test_patch_module_imports_no_forbidden_modules` | test | `test_patch_module_imports_no_forbidden_modules` | [tests/learner/test_patch.py:291](../../tests/learner/test_patch.py#L291) |  |
| `test_path_law_l1_within_rho` | test | `test_path_law_l1_within_rho` | [tests/k4b/test_a_lemma_t.py:104](../../tests/k4b/test_a_lemma_t.py#L104) |  |
| `test_pause_check_is_strictly_greater_than_three_times` | test | `test_pause_check_is_strictly_greater_than_three_times` | [tests/hwsb/test_b_records.py:42](../../tests/hwsb/test_b_records.py#L42) |  |
| `test_pause_check_numbers_from_the_protocol` | test | `test_pause_check_numbers_from_the_protocol` | [tests/hwsb/test_b_records.py:56](../../tests/hwsb/test_b_records.py#L56) |  |
| `test_pause_check_strict_triggers` | test | `test_pause_check_strict_triggers` | [tests/hws/test_a_budget.py:78](../../tests/hws/test_a_budget.py#L78) |  |
| `test_paused_search_never_gets_the_no_world_licence` | test | `test_paused_search_never_gets_the_no_world_licence` | [tests/hws/test_a_outcomes.py:240](../../tests/hws/test_a_outcomes.py#L240) |  |
| `test_pc_scores_definition_on_new_rows` | test | `test_pc_scores_definition_on_new_rows` | [tests/analysis/test_x4f_targets.py:136](../../tests/analysis/test_x4f_targets.py#L136) |  |
| `test_pc_scores_hand_case_and_decorrelation` | test | `test_pc_scores_hand_case_and_decorrelation` | [tests/analysis/test_x4f_targets.py:145](../../tests/analysis/test_x4f_targets.py#L145) |  |
| `test_per_model_status_boundaries` | test | `test_per_model_status_boundaries` | [tests/c1prime/test_b_inference.py:98](../../tests/c1prime/test_b_inference.py#L98) |  |
| `test_per_stage_thresholds_of_the_protocol_table` | test | `test_per_stage_thresholds_of_the_protocol_table` | [tests/hws/test_a_budget.py:108](../../tests/hws/test_a_budget.py#L108) |  |
| `test_percentile_interval_equals_inverted_cdf_quantile` | test | `test_percentile_interval_equals_inverted_cdf_quantile` | [tests/oracle_profile/test_oracle_profile_kernels.py:251](../../tests/oracle_profile/test_oracle_profile_kernels.py#L251) |  |
| `test_percentile_interval_hand_case` | test | `test_percentile_interval_hand_case` | [tests/oracle_profile/test_oracle_profile_kernels.py:259](../../tests/oracle_profile/test_oracle_profile_kernels.py#L259) | n = 4: inverted CDF picks x_(ceil(n p)): p = .25 -> 1, .3 -> 2, .5 -> 2, 1 -> 4. |
| `test_percentile_interval_hand_value` | test | `test_percentile_interval_hand_value` | [tests/analysis/test_x5_context.py:50](../../tests/analysis/test_x5_context.py#L50) |  |
| `test_percentile_interval_matches_numpy_linear` | test | `test_percentile_interval_matches_numpy_linear` | [tests/analysis/test_x5_context.py:41](../../tests/analysis/test_x5_context.py#L41) |  |
| `test_percentile_interval_rejects_bad_probs` | test | `test_percentile_interval_rejects_bad_probs` | [tests/oracle_profile/test_builder_kernels.py:91](../../tests/oracle_profile/test_builder_kernels.py#L91) |  |
| `test_permutation_fixture_is_non_involutive` | test | `test_permutation_fixture_is_non_involutive` | [tests/c2_readout/test_a_readout.py:183](../../tests/c2_readout/test_a_readout.py#L183) |  |
| `test_permuting_rows_within_calibration_does_not_change_result` | test | `test_permuting_rows_within_calibration_does_not_change_result` | [tests/experiment/test_x4f_probe.py:159](../../tests/experiment/test_x4f_probe.py#L159) |  |
| `test_persist_order_and_values` | test | `test_persist_order_and_values` | [tests/c1prime/test_a_chart_lcc512.py:179](../../tests/c1prime/test_a_chart_lcc512.py#L179) | Items 3 and 9: giant before the lift, then lift kind, g and the smoothing residual. |
| `test_persistent_latch_requires_fresh_clearance_and_release` | test | `test_persistent_latch_requires_fresh_clearance_and_release` | [tests/oracle_profile/test_builder_controls.py:181](../../tests/oracle_profile/test_builder_controls.py#L181) |  |
| `test_phase_bin_counts_known_answers` | test | `test_phase_bin_counts_known_answers` | [tests/circle_history/test_chart_extension.py:287](../../tests/circle_history/test_chart_extension.py#L287) |  |
| `test_phase_bound_at_K_equals_row_bound` | test | `test_phase_bound_at_K_equals_row_bound` | [tests/k4b/test_a_lemma_n.py:197](../../tests/k4b/test_a_lemma_n.py#L197) |  |
| `test_phase_bound_closed_form_at_phi_zero` | test | `test_phase_bound_closed_form_at_phi_zero` | [tests/k4b/test_a_lemma_n.py:210](../../tests/k4b/test_a_lemma_n.py#L210) |  |
| `test_phase_bound_detects_a_wrong_score` | test | `test_phase_bound_detects_a_wrong_score` | [tests/k4b/test_a_lemma_n.py:228](../../tests/k4b/test_a_lemma_n.py#L228) |  |
| `test_phase_bound_K1_K2_differ_by_envelopes` | test | `test_phase_bound_K1_K2_differ_by_envelopes` | [tests/k4b/test_a_lemma_n.py:220](../../tests/k4b/test_a_lemma_n.py#L220) |  |
| `test_phase_bound_refuses_phase_outside_domain` | test | `test_phase_bound_refuses_phase_outside_domain` | [tests/k4b/test_a_lemma_n.py:235](../../tests/k4b/test_a_lemma_n.py#L235) |  |
| `test_pinsker_violations_counts_only_below_minus_tol` | test | `test_pinsker_violations_counts_only_below_minus_tol` | [tests/hws/test_a_stats.py:232](../../tests/hws/test_a_stats.py#L232) |  |
| `test_pipeline_matches_independent_reference` | test | `test_pipeline_matches_independent_reference` | [tests/circle_history/test_error_bound.py:286](../../tests/circle_history/test_error_bound.py#L286) |  |
| `test_pipeline_null_any_single_check_fails` | test | `test_pipeline_null_any_single_check_fails` | [tests/d2a/test_b_rules_flags.py:277](../../tests/d2a/test_b_rules_flags.py#L277) |  |
| `test_pipeline_null_mean_below_threshold_does_not_rescue` | test | `test_pipeline_null_mean_below_threshold_does_not_rescue` | [tests/d2a/test_b_rules_flags.py:288](../../tests/d2a/test_b_rules_flags.py#L288) |  |
| `test_pipeline_null_needs_all_four_checks` | test | `test_pipeline_null_needs_all_four_checks` | [tests/d2a/test_b_rules_flags.py:282](../../tests/d2a/test_b_rules_flags.py#L282) |  |
| `test_pipeline_null_passes_at_boundary` | test | `test_pipeline_null_passes_at_boundary` | [tests/d2a/test_b_rules_flags.py:270](../../tests/d2a/test_b_rules_flags.py#L270) |  |
| `test_placement_ok_for_test_paths_and_planted_inside_root` | test | `test_placement_ok_for_test_paths_and_planted_inside_root` | [tests/hwsb/test_b_meter_law.py:118](../../tests/hwsb/test_b_meter_law.py#L118) |  |
| `test_plain_support_exclude_unresolved` | test | `test_plain_support_exclude_unresolved` | [tests/k4b/test_a_decision.py:141](../../tests/k4b/test_a_decision.py#L141) |  |
| `test_planted_narrow_enclosure_is_caught_by_the_reference` | test | `test_planted_narrow_enclosure_is_caught_by_the_reference` | [tests/hwsb/test_b_meter_law.py:250](../../tests/hwsb/test_b_meter_law.py#L250) |  |
| `test_planted_y_direction_inside_col_B_fails_y1` | test | `test_planted_y_direction_inside_col_B_fails_y1` | [tests/c2_readout/test_a_scope.py:225](../../tests/c2_readout/test_a_scope.py#L225) |  |
| `test_poll_bounds_inclusive_upper` | test | `test_poll_bounds_inclusive_upper` | [tests/experiment/test_x5g1t_runtime.py:348](../../tests/experiment/test_x5g1t_runtime.py#L348) |  |
| `test_poll_bounds_rejected_even_without_hold` | test | `test_poll_bounds_rejected_even_without_hold` | [tests/experiment/test_x5g1t_runtime.py:341](../../tests/experiment/test_x5g1t_runtime.py#L341) |  |
| `test_poll_bounds_rejected_while_held` | test | `test_poll_bounds_rejected_while_held` | [tests/experiment/test_x5g1t_runtime.py:331](../../tests/experiment/test_x5g1t_runtime.py#L331) |  |
| `test_pool_audit_end_to_end_is_deterministic` | test | `test_pool_audit_end_to_end_is_deterministic` | [tests/experiment/test_x4b.py:96](../../tests/experiment/test_x4b.py#L96) |  |
| `test_pool_config_contents` | test | `test_pool_config_contents` | [tests/experiment/test_x5g1t_lineage_oracle.py:176](../../tests/experiment/test_x5g1t_lineage_oracle.py#L176) |  |
| `test_pool_observation_rejects_invalid` | test | `test_pool_observation_rejects_invalid` | [tests/experiment/test_x5g1t_lineage_oracle.py:166](../../tests/experiment/test_x5g1t_lineage_oracle.py#L166) |  |
| `test_pool_observation_valid` | test | `test_pool_observation_valid` | [tests/experiment/test_x5g1t_lineage_oracle.py:154](../../tests/experiment/test_x5g1t_lineage_oracle.py#L154) |  |
| `test_pool_spec_streams_and_codes` | test | `test_pool_spec_streams_and_codes` | [tests/x6_stage1/test_b_seed_pool_reg.py:149](../../tests/x6_stage1/test_b_seed_pool_reg.py#L149) |  |
| `test_pool_table_follows_api` | test | `test_pool_table_follows_api` | [tests/d2a/test_a_world.py:67](../../tests/d2a/test_a_world.py#L67) |  |
| `test_pool_table_order_sizes_splits_names` | test | `test_pool_table_order_sizes_splits_names` | [tests/x6_stage1/test_b_seed_pool_reg.py:124](../../tests/x6_stage1/test_b_seed_pool_reg.py#L124) |  |
| `test_pools_collision_check_loads_the_old_id_store` | test | `test_pools_collision_check_loads_the_old_id_store` | [tests/experiment/test_x5g1t_identity_eval.py:179](../../tests/experiment/test_x5g1t_identity_eval.py#L179) |  |
| `test_pools_read_root_payload_mutated_after_load_refused` | test | `test_pools_read_root_payload_mutated_after_load_refused` | [tests/experiment/test_x5g1t_identity_eval.py:185](../../tests/experiment/test_x5g1t_identity_eval.py#L185) |  |
| `test_post_desc_values_are_labelled_unlicensed_point_ratios` | test | `test_post_desc_values_are_labelled_unlicensed_point_ratios` | [tests/c2_readout/test_a_inference.py:306](../../tests/c2_readout/test_a_inference.py#L306) |  |
| `test_posterior_isolation_pair` | test | `test_posterior_isolation_pair` | [tests/d1_seam/test_d1_seam.py:264](../../tests/d1_seam/test_d1_seam.py#L264) |  |
| `test_posterior_means_contract` | test | `test_posterior_means_contract` | [tests/oracle_profile/test_builder_kernels.py:55](../../tests/oracle_profile/test_builder_kernels.py#L55) |  |
| `test_posterior_means_matches_suffix_posterior_and_reference` | test | `test_posterior_means_matches_suffix_posterior_and_reference` | [tests/oracle_profile/test_oracle_profile.py:225](../../tests/oracle_profile/test_oracle_profile.py#L225) | posterior_means = suffix_posterior @ features for every K; vs the decimal reference. |
| `test_posteriors_within_rho` | test | `test_posteriors_within_rho` | [tests/k4b/test_a_lemma_t.py:115](../../tests/k4b/test_a_lemma_t.py#L115) |  |
| `test_practical_verdict_two_of_three_rule` | test | `test_practical_verdict_two_of_three_rule` | [tests/analysis/test_horizon.py:178](../../tests/analysis/test_horizon.py#L178) |  |
| `test_precision_cross_model_sequence_mismatch_fails_technical` | test | `test_precision_cross_model_sequence_mismatch_fails_technical` | [tests/circle_history/test_builder_v24_stages.py:172](../../tests/circle_history/test_builder_v24_stages.py#L172) |  |
| `test_precision_just_over_mde_or_under_power_is_inconclusive` | test | `test_precision_just_over_mde_or_under_power_is_inconclusive` | [tests/circle_history/test_scores_precision_gates.py:202](../../tests/circle_history/test_scores_precision_gates.py#L202) |  |
| `test_precision_limited_on_h1_or_h2_failure_when_both_arms_enter` | test | `test_precision_limited_on_h1_or_h2_failure_when_both_arms_enter` | [tests/d2a/test_b_rules_qualifiers.py:141](../../tests/d2a/test_b_rules_qualifiers.py#L141) |  |
| `test_precision_limited_on_rule8_counts_only_h2_models` | test | `test_precision_limited_on_rule8_counts_only_h2_models` | [tests/d2a/test_b_rules_qualifiers.py:153](../../tests/d2a/test_b_rules_qualifiers.py#L153) |  |
| `test_precision_limited_turns_outcome9_into_inconclusive` | test | `test_precision_limited_turns_outcome9_into_inconclusive` | [tests/d2a/test_b_rules_qualifiers.py:161](../../tests/d2a/test_b_rules_qualifiers.py#L161) |  |
| `test_precision_ok` | test | `test_precision_ok` | [tests/d2a/test_b_rules_flags.py:183](../../tests/d2a/test_b_rules_flags.py#L183) |  |
| `test_precision_pass_at_exact_equalities` | test | `test_precision_pass_at_exact_equalities` | [tests/circle_history/test_scores_precision_gates.py:192](../../tests/circle_history/test_scores_precision_gates.py#L192) |  |
| `test_precision_summary_fail_closed` | test | `test_precision_summary_fail_closed` | [tests/circle_history/test_scores_precision_gates.py:279](../../tests/circle_history/test_scores_precision_gates.py#L279) |  |
| `test_precision_summary_inverted_cdf_quantiles_power_and_mde_fields` | test | `test_precision_summary_inverted_cdf_quantiles_power_and_mde_fields` | [tests/circle_history/test_scores_precision_gates.py:133](../../tests/circle_history/test_scores_precision_gates.py#L133) |  |
| `test_precision_summary_nonfinite_raises_invalid` | test | `test_precision_summary_nonfinite_raises_invalid` | [tests/circle_history/test_scores_precision_gates.py:220](../../tests/circle_history/test_scores_precision_gates.py#L220) |  |
| `test_precision_written_after_b4_stop_with_controls` | test | `test_precision_written_after_b4_stop_with_controls` | [tests/circle_history/test_builder_v24_stages.py:160](../../tests/circle_history/test_builder_v24_stages.py#L160) |  |
| `test_predecessors_sum_to_class_count` | test | `test_predecessors_sum_to_class_count` | [tests/x6_stage1/test_a_pairs.py:184](../../tests/x6_stage1/test_a_pairs.py#L184) |  |
| `test_predicate_hit_is_registry_incomplete_and_rows_kept` | test | `test_predicate_hit_is_registry_incomplete_and_rows_kept` | [tests/k4b/test_b_data.py:341](../../tests/k4b/test_b_data.py#L341) |  |
| `test_predicate_hits_count_planted_alphabet_rows` | test | `test_predicate_hits_count_planted_alphabet_rows` | [tests/hwsb/test_b_registry.py:230](../../tests/hwsb/test_b_registry.py#L230) |  |
| `test_predicate_pass_without_hits` | test | `test_predicate_pass_without_hits` | [tests/k4b/test_b_data.py:351](../../tests/k4b/test_b_data.py#L351) |  |
| `test_predicted_pair_tv_band_boundaries` | test | `test_predicted_pair_tv_band_boundaries` | [tests/d2a/test_b_behaviour.py:77](../../tests/d2a/test_b_behaviour.py#L77) |  |
| `test_predictions_equal_ridgeprobe_on_calibration_standardised_data` | test | `test_predictions_equal_ridgeprobe_on_calibration_standardised_data` | [tests/experiment/test_x4f_probe.py:79](../../tests/experiment/test_x4f_probe.py#L79) |  |
| `test_prefix_dependent_field_is_nonzero` | test | `test_prefix_dependent_field_is_nonzero` | [tests/k4b/test_a_prop1.py:159](../../tests/k4b/test_a_prop1.py#L159) |  |
| `test_prefix_invariance_of_qstar` | test | `test_prefix_invariance_of_qstar` | [tests/x6_stage1/test_a_designed.py:146](../../tests/x6_stage1/test_a_designed.py#L146) |  |
| `test_prefix_permuted_and_p4_rows` | test | `test_prefix_permuted_and_p4_rows` | [tests/hws/test_b_oracle.py:273](../../tests/hws/test_b_oracle.py#L273) |  |
| `test_prerequisite_dict_and_binding` | test | `test_prerequisite_dict_and_binding` | [tests/c1prime/test_a_gates.py:72](../../tests/c1prime/test_a_gates.py#L72) |  |
| `test_primary_coordinates_basis_and_isometry` | test | `test_primary_coordinates_basis_and_isometry` | [tests/c1prime/test_b_frames.py:106](../../tests/c1prime/test_b_frames.py#L106) |  |
| `test_primitive_class_bfs_not_dfs_order` | test | `test_primitive_class_bfs_not_dfs_order` | [tests/circle_history/test_cochain.py:179](../../tests/circle_history/test_cochain.py#L179) |  |
| `test_primitive_class_cycle_known_period` | test | `test_primitive_class_cycle_known_period` | [tests/circle_history/test_cochain.py:166](../../tests/circle_history/test_cochain.py#L166) |  |
| `test_primitive_class_gcd_of_two_periods` | test | `test_primitive_class_gcd_of_two_periods` | [tests/circle_history/test_cochain.py:191](../../tests/circle_history/test_cochain.py#L191) |  |
| `test_primitive_class_non_closed_alpha_invalid` | test | `test_primitive_class_non_closed_alpha_invalid` | [tests/circle_history/test_cochain.py:216](../../tests/circle_history/test_cochain.py#L216) |  |
| `test_primitive_class_unresolved_cases` | test | `test_primitive_class_unresolved_cases` | [tests/circle_history/test_cochain.py:203](../../tests/circle_history/test_cochain.py#L203) |  |
| `test_prior_cumulative_is_kept` | test | `test_prior_cumulative_is_kept` | [tests/experiment/test_x5g1_controls.py:118](../../tests/experiment/test_x5g1_controls.py#L118) |  |
| `test_prior_or_unclassified_hit_fails_closed` | test | `test_prior_or_unclassified_hit_fails_closed` | [tests/k4b/test_b_flow.py:271](../../tests/k4b/test_b_flow.py#L271) |  |
| `test_process_blocks` | test | `test_process_blocks` | [tests/d2a/test_a_world.py:129](../../tests/d2a/test_a_world.py#L129) |  |
| `test_process_digest_matches_written_formula_and_binds_every_input` | test | `test_process_digest_matches_written_formula_and_binds_every_input` | [tests/circle_history/test_reference_binding.py:73](../../tests/circle_history/test_reference_binding.py#L73) |  |
| `test_process_law_bound_invalid_only_for_nonfinite_or_misshaped` | test | `test_process_law_bound_invalid_only_for_nonfinite_or_misshaped` | [tests/circle_history/test_process_law.py:272](../../tests/circle_history/test_process_law.py#L272) |  |
| `test_process_law_bound_on_the_rounded_documented_law` | test | `test_process_law_bound_on_the_rounded_documented_law` | [tests/circle_history/test_process_law.py:236](../../tests/circle_history/test_process_law.py#L236) |  |
| `test_process_law_bound_unavailable_with_reason` | test | `test_process_law_bound_unavailable_with_reason` | [tests/circle_history/test_process_law.py:266](../../tests/circle_history/test_process_law.py#L266) |  |
| `test_process_rekeys_e_named_to_int` | test | `test_process_rekeys_e_named_to_int` | [tests/c1prime/test_c_process_keys.py:25](../../tests/c1prime/test_c_process_keys.py#L25) |  |
| `test_process_stage_saves_with_world_parent` | test | `test_process_stage_saves_with_world_parent` | [tests/process/test_conductance.py:243](../../tests/process/test_conductance.py#L243) |  |
| `test_production_cfg_env_matching_environ_but_not_spec_rejected` | test | `test_production_cfg_env_matching_environ_but_not_spec_rejected` | [tests/experiment/test_x5g1t_config_production.py:258](../../tests/experiment/test_x5g1t_config_production.py#L258) |  |
| `test_production_correct_config_passes_read_only` | test | `test_production_correct_config_passes_read_only` | [tests/experiment/test_x5g1t_config_checks.py:278](../../tests/experiment/test_x5g1t_config_checks.py#L278) |  |
| `test_production_each_tampered_field_rejected` | test | `test_production_each_tampered_field_rejected` | [tests/experiment/test_x5g1t_config_production.py:251](../../tests/experiment/test_x5g1t_config_production.py#L251) |  |
| `test_production_env_differing_in_os_environ_rejected` | test | `test_production_env_differing_in_os_environ_rejected` | [tests/experiment/test_x5g1t_config_production.py:272](../../tests/experiment/test_x5g1t_config_production.py#L272) |  |
| `test_production_env_missing_from_os_environ_rejected` | test | `test_production_env_missing_from_os_environ_rejected` | [tests/experiment/test_x5g1t_config_production.py:266](../../tests/experiment/test_x5g1t_config_production.py#L266) |  |
| `test_production_lineage_constants_mismatch_rejected` | test | `test_production_lineage_constants_mismatch_rejected` | [tests/experiment/test_x5g1t_config_production.py:369](../../tests/experiment/test_x5g1t_config_production.py#L369) |  |
| `test_production_matches_exhaustive_enumeration` | test | `test_production_matches_exhaustive_enumeration` | [tests/oracle_profile/test_oracle_profile.py:124](../../tests/oracle_profile/test_oracle_profile.py#L124) | Item 1: every string of length L <= 4 and every K in 1..L; impossible suffixes raise. |
| `test_production_paths_compared_after_resolve_and_normcase` | test | `test_production_paths_compared_after_resolve_and_normcase` | [tests/experiment/test_x5g1t_config_checks.py:285](../../tests/experiment/test_x5g1t_config_checks.py#L285) |  |
| `test_production_protocol_doc_bytes_changed_rejected` | test | `test_production_protocol_doc_bytes_changed_rejected` | [tests/experiment/test_x5g1t_config_production.py:277](../../tests/experiment/test_x5g1t_config_production.py#L277) |  |
| `test_production_source_of_wrong_artifact_type_rejected` | test | `test_production_source_of_wrong_artifact_type_rejected` | [tests/experiment/test_x5g1t_config_production.py:308](../../tests/experiment/test_x5g1t_config_production.py#L308) | cfg and spec agree, but the 'world' source is a TransitionSpec. |
| `test_production_source_payload_mutated_on_disk_rejected` | test | `test_production_source_payload_mutated_on_disk_rejected` | [tests/experiment/test_x5g1t_config_production.py:300](../../tests/experiment/test_x5g1t_config_production.py#L300) | Same metadata, mutated payload: the full re-hash must catch it. |
| `test_production_spec_doc_sha_differs_from_consistent_cfg_rejected` | test | `test_production_spec_doc_sha_differs_from_consistent_cfg_rejected` | [tests/experiment/test_x5g1t_config_production.py:286](../../tests/experiment/test_x5g1t_config_production.py#L286) | cfg and the repo document agree but the spec pins another sha256. |
| `test_production_spec_holds_frozen_v4_values` | test | `test_production_spec_holds_frozen_v4_values` | [tests/experiment/test_x5g1t_config_checks.py:192](../../tests/experiment/test_x5g1t_config_checks.py#L192) |  |
| `test_production_stored_checkpoint_not_a_checkpoint_rejected` | test | `test_production_stored_checkpoint_not_a_checkpoint_rejected` | [tests/experiment/test_x5g1t_config_production.py:357](../../tests/experiment/test_x5g1t_config_production.py#L357) |  |
| `test_production_stored_model_config_differs_from_cfg_rejected` | test | `test_production_stored_model_config_differs_from_cfg_rejected` | [tests/experiment/test_x5g1t_config_production.py:351](../../tests/experiment/test_x5g1t_config_production.py#L351) |  |
| `test_production_stored_producer_differs_from_consistent_cfg_rejected` | test | `test_production_stored_producer_differs_from_consistent_cfg_rejected` | [tests/experiment/test_x5g1t_config_production.py:316](../../tests/experiment/test_x5g1t_config_production.py#L316) | cfg and spec agree on a producer that is not the stored producer_version. |
| `test_production_stored_train_config_device_and_grid_are_replaced` | test | `test_production_stored_train_config_device_and_grid_are_replaced` | [tests/experiment/test_x5g1t_config_production.py:343](../../tests/experiment/test_x5g1t_config_production.py#L343) | Only checkpoint_steps (-> grid) and device (-> "cpu") may differ from the stored dict. |
| `test_production_stored_train_config_differs_beyond_grid_and_device_rejected` | test | `test_production_stored_train_config_differs_beyond_grid_and_device_rejected` | [tests/experiment/test_x5g1t_config_production.py:336](../../tests/experiment/test_x5g1t_config_production.py#L336) |  |
| `test_production_write_root_safety` | test | `test_production_write_root_safety` | [tests/experiment/test_x5g1t_config_production.py:377](../../tests/experiment/test_x5g1t_config_production.py#L377) | spec and cfg agree, so only the write-root rule can reject. |
| `test_profile_point_and_bootstrap_error_paths` | test | `test_profile_point_and_bootstrap_error_paths` | [tests/oracle_profile/test_builder_kernels.py:73](../../tests/oracle_profile/test_builder_kernels.py#L73) |  |
| `test_projection_at_step_1000_is_cpu_times_five` | test | `test_projection_at_step_1000_is_cpu_times_five` | [tests/hwsb/test_b_hold.py:43](../../tests/hwsb/test_b_hold.py#L43) |  |
| `test_projection_exact_threshold_passes` | test | `test_projection_exact_threshold_passes` | [tests/k4b/test_a_ranks_ladder.py:143](../../tests/k4b/test_a_ranks_ladder.py#L143) |  |
| `test_projection_exclusion_per_model_one_below_fails` | test | `test_projection_exclusion_per_model_one_below_fails` | [tests/k4b/test_a_ranks_ladder.py:161](../../tests/k4b/test_a_ranks_ladder.py#L161) |  |
| `test_projection_joint_one_below_fails` | test | `test_projection_joint_one_below_fails` | [tests/k4b/test_a_ranks_ladder.py:151](../../tests/k4b/test_a_ranks_ladder.py#L151) |  |
| `test_projection_matches_reference_and_is_mean_shift_invariant` | test | `test_projection_matches_reference_and_is_mean_shift_invariant` | [tests/k4b/test_a_ranks_ladder.py:197](../../tests/k4b/test_a_ranks_ladder.py#L197) |  |
| `test_projection_replaces_only_scoring_terms` | test | `test_projection_replaces_only_scoring_terms` | [tests/experiment/test_x5g1_scorebench_smoke.py:15](../../tests/experiment/test_x5g1_scorebench_smoke.py#L15) |  |
| `test_projection_support_per_model_one_below_fails` | test | `test_projection_support_per_model_one_below_fails` | [tests/k4b/test_a_ranks_ladder.py:173](../../tests/k4b/test_a_ranks_ladder.py#L173) |  |
| `test_projector_dependent_when_euclidean_complement_changes_the_category` | test | `test_projector_dependent_when_euclidean_complement_changes_the_category` | [tests/c2_readout/test_a_scope.py:273](../../tests/c2_readout/test_a_scope.py#L273) |  |
| `test_proof_note_exists_and_names_delta_and_rounding` | test | `test_proof_note_exists_and_names_delta_and_rounding` | [tests/hwsb/test_a_enclosure_proof.py:333](../../tests/hwsb/test_a_enclosure_proof.py#L333) | OPEN-3: the reviewed proof note is in tools/hwsb (content reviewed elsewhere). |
| `test_proposition_f_for_three_suffix_predictors` | test | `test_proposition_f_for_three_suffix_predictors` | [tests/hws/test_a_identities.py:303](../../tests/hws/test_a_identities.py#L303) |  |
| `test_protocol_and_authority_bindings` | test | `test_protocol_and_authority_bindings` | [tests/c2_readout/test_b_lineage.py:102](../../tests/c2_readout/test_b_lineage.py#L102) |  |
| `test_protocol_and_stage0_hash_bindings` | test | `test_protocol_and_stage0_hash_bindings` | [tests/x6_stage1/test_b_nb_s0_ops.py:228](../../tests/x6_stage1/test_b_nb_s0_ops.py#L228) |  |
| `test_public_api_exports` | test | `test_public_api_exports` | [tests/oracle/test_oracle.py:316](../../tests/oracle/test_oracle.py#L316) |  |
| `test_pytest_basetemp_is_outside_the_project_root` | test | `test_pytest_basetemp_is_outside_the_project_root` | [tests/c2_readout/test_b_registry.py:350](../../tests/c2_readout/test_b_registry.py#L350) |  |
| `test_pytest_basetemp_is_outside_the_project_root` | test | `test_pytest_basetemp_is_outside_the_project_root` | [tests/hws/test_b_records.py:80](../../tests/hws/test_b_records.py#L80) |  |
| `test_q1_and_q2_outcomes` | test | `test_q1_and_q2_outcomes` | [tests/x2a_stage0/test_x2a_stage0_ph.py:181](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L181) |  |
| `test_q8_difference_on_r_ord_rows_t5` | test | `test_q8_difference_on_r_ord_rows_t5` | [tests/x6_stage1/test_a_pairs.py:342](../../tests/x6_stage1/test_a_pairs.py#L342) |  |
| `test_q99_inverted_cdf_rank` | test | `test_q99_inverted_cdf_rank` | [tests/c1prime/test_a_eligibility_support.py:120](../../tests/c1prime/test_a_eligibility_support.py#L120) | 100 * 0.99 = 99 exactly in float -> 99th smallest (98); ceil(8110.08) = 8111 -> 8110. |
| `test_qr_pos_matches_numpy_with_a_positive_diagonal` | test | `test_qr_pos_matches_numpy_with_a_positive_diagonal` | [tests/c1prime/test_b_frames.py:83](../../tests/c1prime/test_b_frames.py#L83) |  |
| `test_qualifiers_order_dissent_and_licence_texts` | test | `test_qualifiers_order_dissent_and_licence_texts` | [tests/c2_readout/test_a_inference.py:322](../../tests/c2_readout/test_a_inference.py#L322) |  |
| `test_qualifiers_registered_names_order_and_designed_unresolved` | test | `test_qualifiers_registered_names_order_and_designed_unresolved` | [tests/x6_stage1/test_a_rules.py:285](../../tests/x6_stage1/test_a_rules.py#L285) |  |
| `test_quant_invalid` | test | `test_quant_invalid` | [tests/x6_stage1/test_a_eval.py:236](../../tests/x6_stage1/test_a_eval.py#L236) |  |
| `test_quantile_2000_draws_order_statistics` | test | `test_quantile_2000_draws_order_statistics` | [tests/analysis/test_x5_endpoint.py:309](../../tests/analysis/test_x5_endpoint.py#L309) |  |
| `test_quantile_errors` | test | `test_quantile_errors` | [tests/analysis/test_x5_endpoint.py:343](../../tests/analysis/test_x5_endpoint.py#L343) |  |
| `test_quantile_matches_numpy_on_random_finite` | test | `test_quantile_matches_numpy_on_random_finite` | [tests/analysis/test_x5_endpoint.py:290](../../tests/analysis/test_x5_endpoint.py#L290) |  |
| `test_quantile_returns_float_and_accepts_list` | test | `test_quantile_returns_float_and_accepts_list` | [tests/analysis/test_x5_endpoint.py:331](../../tests/analysis/test_x5_endpoint.py#L331) |  |
| `test_quantile_with_infinities` | test | `test_quantile_with_infinities` | [tests/analysis/test_x5_endpoint.py:315](../../tests/analysis/test_x5_endpoint.py#L315) |  |
| `test_quantile_with_rank_rejects_a_wrong_order_statistic` | test | `test_quantile_with_rank_rejects_a_wrong_order_statistic` | [tests/c1prime/test_b_inference.py:214](../../tests/c1prime/test_b_inference.py#L214) |  |
| `test_quantile_with_rank_returns_the_input_element_at_the_rank` | test | `test_quantile_with_rank_returns_the_input_element_at_the_rank` | [tests/c1prime/test_b_inference.py:195](../../tests/c1prime/test_b_inference.py#L195) |  |
| `test_quantile_wrapper_levels` | test | `test_quantile_wrapper_levels` | [tests/x6_stage1/test_a_numerics.py:324](../../tests/x6_stage1/test_a_numerics.py#L324) |  |
| `test_quantise_conservation_and_independent_reference` | test | `test_quantise_conservation_and_independent_reference` | [tests/x6_stage1/test_a_eval.py:203](../../tests/x6_stage1/test_a_eval.py#L203) |  |
| `test_quantise_ties_and_zero_rule_hand_cases` | test | `test_quantise_ties_and_zero_rule_hand_cases` | [tests/x6_stage1/test_a_eval.py:214](../../tests/x6_stage1/test_a_eval.py#L214) |  |
| `test_quarantine_never_touches_chain_elements` | test | `test_quarantine_never_touches_chain_elements` | [tests/x6_stage1/test_b_chain_ops.py:172](../../tests/x6_stage1/test_b_chain_ops.py#L172) |  |
| `test_quiet_table_carries_only_the_length_qualifier` | test | `test_quiet_table_carries_only_the_length_qualifier` | [tests/d2a/test_b_rules_qualifiers.py:108](../../tests/d2a/test_b_rules_qualifiers.py#L108) |  |
| `test_qvals_independent_set` | test | `test_qvals_independent_set` | [tests/x6_stage1/test_a_numerics.py:71](../../tests/x6_stage1/test_a_numerics.py#L71) |  |
| `test_R01_kl_error_paths` | test | `test_R01_kl_error_paths` | [tests/prediction/test_metrics.py:33](../../tests/prediction/test_metrics.py#L33) |  |
| `test_R01_kl_zero_hand_value_and_nonnegative` | test | `test_R01_kl_zero_hand_value_and_nonnegative` | [tests/prediction/test_metrics.py:14](../../tests/prediction/test_metrics.py#L14) |  |
| `test_R01_kl_zero_log_zero_convention_and_regret_mean` | test | `test_R01_kl_zero_log_zero_convention_and_regret_mean` | [tests/prediction/test_metrics.py:26](../../tests/prediction/test_metrics.py#L26) |  |
| `test_R02_nll_picks_target_column` | test | `test_R02_nll_picks_target_column` | [tests/prediction/test_metrics.py:51](../../tests/prediction/test_metrics.py#L51) |  |
| `test_R02_nll_uniform_is_log_v` | test | `test_R02_nll_uniform_is_log_v` | [tests/prediction/test_metrics.py:45](../../tests/prediction/test_metrics.py#L45) |  |
| `test_R03_additive_smoothing_hand_value` | test | `test_R03_additive_smoothing_hand_value` | [tests/prediction/test_ngram.py:26](../../tests/prediction/test_ngram.py#L26) |  |
| `test_R03_kneser_ney_order1_equals_mle` | test | `test_R03_kneser_ney_order1_equals_mle` | [tests/prediction/test_ngram.py:32](../../tests/prediction/test_ngram.py#L32) |  |
| `test_R03_unigram_exact_frequencies` | test | `test_R03_unigram_exact_frequencies` | [tests/prediction/test_ngram.py:18](../../tests/prediction/test_ngram.py#L18) |  |
| `test_R04_bigram_on_cycle_predicts_successor` | test | `test_R04_bigram_on_cycle_predicts_successor` | [tests/prediction/test_ngram.py:39](../../tests/prediction/test_ngram.py#L39) |  |
| `test_R05_run_baselines_uses_train_for_fit_dev_for_select` | test | `test_R05_run_baselines_uses_train_for_fit_dev_for_select` | [tests/prediction/test_stage.py:42](../../tests/prediction/test_stage.py#L42) |  |
| `test_R05_select_smoothing_uses_dev_and_picks_argmin` | test | `test_R05_select_smoothing_uses_dev_and_picks_argmin` | [tests/prediction/test_ngram.py:69](../../tests/prediction/test_ngram.py#L69) |  |
| `test_R06_captured_and_gate_hand_values` | test | `test_R06_captured_and_gate_hand_values` | [tests/prediction/test_metrics.py:57](../../tests/prediction/test_metrics.py#L57) |  |
| `test_R06_zero_context_gain_is_inconclusive` | test | `test_R06_zero_context_gain_is_inconclusive` | [tests/prediction/test_metrics.py:69](../../tests/prediction/test_metrics.py#L69) |  |
| `test_R07_bootstrap_resamples_groups_not_rows` | test | `test_R07_bootstrap_resamples_groups_not_rows` | [tests/prediction/test_metrics.py:77](../../tests/prediction/test_metrics.py#L77) |  |
| `test_R07_constant_array_has_degenerate_ci` | test | `test_R07_constant_array_has_degenerate_ci` | [tests/prediction/test_metrics.py:87](../../tests/prediction/test_metrics.py#L87) |  |
| `test_R08_join_mismatch_raises` | test | `test_R08_join_mismatch_raises` | [tests/prediction/test_metrics.py:101](../../tests/prediction/test_metrics.py#L101) |  |
| `test_R08_join_returns_alignment_permutation` | test | `test_R08_join_returns_alignment_permutation` | [tests/prediction/test_metrics.py:93](../../tests/prediction/test_metrics.py#L93) |  |
| `test_R09_recovers_planted_affine_map` | test | `test_R09_recovers_planted_affine_map` | [tests/prediction/test_ridge.py:20](../../tests/prediction/test_ridge.py#L20) |  |
| `test_R09_shuffled_labels_give_near_zero_r2` | test | `test_R09_shuffled_labels_give_near_zero_r2` | [tests/prediction/test_ridge.py:29](../../tests/prediction/test_ridge.py#L29) |  |
| `test_R10_probe_fit_touching_test_raises_leakage` | test | `test_R10_probe_fit_touching_test_raises_leakage` | [tests/prediction/test_ridge.py:45](../../tests/prediction/test_ridge.py#L45) |  |
| `test_r1_failure_routes_to_cnhs` | test | `test_r1_failure_routes_to_cnhs` | [tests/c2_readout/test_b_screens.py:129](../../tests/c2_readout/test_b_screens.py#L129) |  |
| `test_r1_median_ties_use_inverted_cdf` | test | `test_r1_median_ties_use_inverted_cdf` | [tests/c2_readout/test_b_screens.py:83](../../tests/c2_readout/test_b_screens.py#L83) |  |
| `test_r1_sign_zero_is_disagreement_and_three_quarters_passes` | test | `test_r1_sign_zero_is_disagreement_and_three_quarters_passes` | [tests/c2_readout/test_b_screens.py:73](../../tests/c2_readout/test_b_screens.py#L73) |  |
| `test_r1_without_overrides_reproduces_c1_gates_v1_bitwise` | test | `test_r1_without_overrides_reproduces_c1_gates_v1_bitwise` | [tests/c2_readout/test_b_screens.py:48](../../tests/c2_readout/test_b_screens.py#L48) |  |
| `test_r1_wraps_at_plus_minus_pi` | test | `test_r1_wraps_at_plus_minus_pi` | [tests/c2_readout/test_b_screens.py:65](../../tests/c2_readout/test_b_screens.py#L65) |  |
| `test_r1_zero_modulus_override_before_median_and_no_row_deleted` | test | `test_r1_zero_modulus_override_before_median_and_no_row_deleted` | [tests/c2_readout/test_b_screens.py:92](../../tests/c2_readout/test_b_screens.py#L92) |  |
| `test_r2_points_on_ring_process_have_h1_above_gaussian_null` | test | `test_r2_points_on_ring_process_have_h1_above_gaussian_null` | [tests/analysis/test_baselines_dynamics.py:61](../../tests/analysis/test_baselines_dynamics.py#L61) |  |
| `test_r2_pooled_hand_values_around_calibration_mean` | test | `test_r2_pooled_hand_values_around_calibration_mean` | [tests/analysis/test_x4f_scores.py:67](../../tests/analysis/test_x4f_scores.py#L67) |  |
| `test_r2_pooled_is_pooled_over_coordinates` | test | `test_r2_pooled_is_pooled_over_coordinates` | [tests/analysis/test_x4f_scores.py:75](../../tests/analysis/test_x4f_scores.py#L75) |  |
| `test_r2_pooled_one_dimensional_and_negative` | test | `test_r2_pooled_one_dimensional_and_negative` | [tests/analysis/test_x4f_scores.py:83](../../tests/analysis/test_x4f_scores.py#L83) |  |
| `test_r2_pooled_zero_variance_threshold_scales_with_n_q` | test | `test_r2_pooled_zero_variance_threshold_scales_with_n_q` | [tests/analysis/test_x4f_scores.py:92](../../tests/analysis/test_x4f_scores.py#L92) |  |
| `test_r2_uses_calibration_mean_and_pooled_sst` | test | `test_r2_uses_calibration_mean_and_pooled_sst` | [tests/experiment/test_x4f_probe.py:87](../../tests/experiment/test_x4f_probe.py#L87) |  |
| `test_r3_needs_n_test_k_and_registry_v2` | test | `test_r3_needs_n_test_k_and_registry_v2` | [tests/c1prime/test_a_release_meter.py:171](../../tests/c1prime/test_a_release_meter.py#L171) |  |
| `test_raising_source_k_makes_k4b_store_incomplete` | test | `test_raising_source_k_makes_k4b_store_incomplete` | [tests/k4b/test_b_store_reader.py:272](../../tests/k4b/test_b_store_reader.py#L272) |  |
| `test_random_sequences_are_not_systematically_small_p` | test | `test_random_sequences_are_not_systematically_small_p` | [tests/analysis/test_baselines_dynamics.py:117](../../tests/analysis/test_baselines_dynamics.py#L117) |  |
| `test_random_subspace_constants_exact` | test | `test_random_subspace_constants_exact` | [tests/c2_readout/test_a_partition.py:167](../../tests/c2_readout/test_a_partition.py#L167) |  |
| `test_random_suffix_table_has_zero_expectation` | test | `test_random_suffix_table_has_zero_expectation` | [tests/k4b/test_a_prop1.py:119](../../tests/k4b/test_a_prop1.py#L119) |  |
| `test_randomised_completion_lies_in_bounds` | test | `test_randomised_completion_lies_in_bounds` | [tests/k4b/test_a_theorem_a.py:152](../../tests/k4b/test_a_theorem_a.py#L152) | Auxiliary randomness w': u~ = v1 w.p. 1/3 and v2 w.p. 2/3 (Fubini). |
| `test_rank_check_accepts_order_statistics_and_rejects_others` | test | `test_rank_check_accepts_order_statistics_and_rejects_others` | [tests/c1prime/test_b_inference.py:203](../../tests/c1prime/test_b_inference.py#L203) |  |
| `test_rank_constants` | test | `test_rank_constants` | [tests/k4b/test_a_ranks_ladder.py:67](../../tests/k4b/test_a_ranks_ladder.py#L67) |  |
| `test_rank_deficient_nuisance_plus_code_block_is_degenerate` | test | `test_rank_deficient_nuisance_plus_code_block_is_degenerate` | [tests/c2_readout/test_a_readout.py:362](../../tests/c2_readout/test_a_readout.py#L362) |  |
| `test_rank_deficient_X_erasure_stays_in_retained_range` | test | `test_rank_deficient_X_erasure_stays_in_retained_range` | [tests/analysis/test_x4f_erasure.py:295](../../tests/analysis/test_x4f_erasure.py#L295) |  |
| `test_rank_f_is_16` | test | `test_rank_f_is_16` | [tests/hws/test_a_stats.py:81](../../tests/hws/test_a_stats.py#L81) |  |
| `test_rank_failures_keep_every_column` | test | `test_rank_failures_keep_every_column` | [tests/c2_readout/test_b_fwl_l1.py:97](../../tests/c2_readout/test_b_fwl_l1.py#L97) |  |
| `test_rank_for_protocol_ranks` | test | `test_rank_for_protocol_ranks` | [tests/c1prime/test_b_inference.py:187](../../tests/c1prime/test_b_inference.py#L187) |  |
| `test_rank_key_every_tie_break_level` | test | `test_rank_key_every_tie_break_level` | [tests/hws/test_a_classify.py:222](../../tests/hws/test_a_classify.py#L222) |  |
| `test_rank_key_tuple` | test | `test_rank_key_tuple` | [tests/hws/test_a_classify.py:228](../../tests/hws/test_a_classify.py#L228) |  |
| `test_rank_rule_one_zero_gamma_keeps_rank_two_zeros_do_not` | test | `test_rank_rule_one_zero_gamma_keeps_rank_two_zeros_do_not` | [tests/c2_readout/test_a_readout.py:125](../../tests/c2_readout/test_a_readout.py#L125) |  |
| `test_rank_tolerance_is_relative_and_used` | test | `test_rank_tolerance_is_relative_and_used` | [tests/analysis/test_x4f_erasure.py:238](../../tests/analysis/test_x4f_erasure.py#L238) |  |
| `test_rate_matched_diag_below_floor_invalid` | test | `test_rate_matched_diag_below_floor_invalid` | [tests/analysis/test_x5_kernel.py:227](../../tests/analysis/test_x5_kernel.py#L227) |  |
| `test_rate_matched_diag_boundary` | test | `test_rate_matched_diag_boundary` | [tests/analysis/test_x5_kernel.py:207](../../tests/analysis/test_x5_kernel.py#L207) |  |
| `test_rate_matched_negative_entry_invalid` | test | `test_rate_matched_negative_entry_invalid` | [tests/analysis/test_x5_kernel.py:221](../../tests/analysis/test_x5_kernel.py#L221) |  |
| `test_rate_matched_nonpositive_alpha_invalid` | test | `test_rate_matched_nonpositive_alpha_invalid` | [tests/analysis/test_x5_kernel.py:215](../../tests/analysis/test_x5_kernel.py#L215) |  |
| `test_rate_matched_valid_equals_formula` | test | `test_rate_matched_valid_equals_formula` | [tests/analysis/test_x5_kernel.py:199](../../tests/analysis/test_x5_kernel.py#L199) |  |
| `test_ratio_curve_bad_gc` | test | `test_ratio_curve_bad_gc` | [tests/analysis/test_x5_endpoint.py:271](../../tests/analysis/test_x5_endpoint.py#L271) |  |
| `test_ratio_curve_empty_rows` | test | `test_ratio_curve_empty_rows` | [tests/analysis/test_x5_endpoint.py:276](../../tests/analysis/test_x5_endpoint.py#L276) |  |
| `test_ratio_curve_values` | test | `test_ratio_curve_values` | [tests/analysis/test_x5_endpoint.py:263](../../tests/analysis/test_x5_endpoint.py#L263) |  |
| `test_ratio_to_mean_reduction` | test | `test_ratio_to_mean_reduction` | [tests/c1prime/test_b_inference.py:87](../../tests/c1prime/test_b_inference.py#L87) |  |
| `test_ratios_values_and_undefined_denominators` | test | `test_ratios_values_and_undefined_denominators` | [tests/k4b/test_b_endpoint.py:254](../../tests/k4b/test_b_endpoint.py#L254) |  |
| `test_rbf_bandwidth_degenerate_for_identical_rows` | test | `test_rbf_bandwidth_degenerate_for_identical_rows` | [tests/analysis/test_x4f_scores.py:154](../../tests/analysis/test_x4f_scores.py#L154) |  |
| `test_rbf_bandwidth_median_rule_hand_value` | test | `test_rbf_bandwidth_median_rule_hand_value` | [tests/analysis/test_x4f_scores.py:139](../../tests/analysis/test_x4f_scores.py#L139) |  |
| `test_rbf_bandwidth_subsample_follows_rng_choice` | test | `test_rbf_bandwidth_subsample_follows_rng_choice` | [tests/analysis/test_x4f_scores.py:145](../../tests/analysis/test_x4f_scores.py#L145) |  |
| `test_rbf_features_formula` | test | `test_rbf_features_formula` | [tests/analysis/test_x4f_scores.py:169](../../tests/analysis/test_x4f_scores.py#L169) |  |
| `test_rbf_map_draw_order_and_shapes` | test | `test_rbf_map_draw_order_and_shapes` | [tests/analysis/test_x4f_scores.py:159](../../tests/analysis/test_x4f_scores.py#L159) |  |
| `test_rc1_binomial_tails_add` | test | `test_rc1_binomial_tails_add` | [tests/k4b/test_a_decision.py:220](../../tests/k4b/test_a_decision.py#L220) |  |
| `test_rc1_family_arithmetic` | test | `test_rc1_family_arithmetic` | [tests/k4b/test_a_decision.py:247](../../tests/k4b/test_a_decision.py#L247) |  |
| `test_rc1_three_point_law_attains_two_alpha` | test | `test_rc1_three_point_law_attains_two_alpha` | [tests/k4b/test_a_decision.py:236](../../tests/k4b/test_a_decision.py#L236) |  |
| `test_reachable_counts_by_recursion` | test | `test_reachable_counts_by_recursion` | [tests/d1_seam/test_d1_seam.py:296](../../tests/d1_seam/test_d1_seam.py#L296) |  |
| `test_read_controls_coordinator_wait_holds_despite_clearance` | test | `test_read_controls_coordinator_wait_holds_despite_clearance` | [tests/experiment/test_x5g1t_usage_files.py:213](../../tests/experiment/test_x5g1t_usage_files.py#L213) |  |
| `test_read_controls_existing_malformed_file_is_stop` | test | `test_read_controls_existing_malformed_file_is_stop` | [tests/experiment/test_x5g1t_usage_files.py:140](../../tests/experiment/test_x5g1t_usage_files.py#L140) |  |
| `test_read_controls_fresh_clearance_plus_continue_releases_and_archives` | test | `test_read_controls_fresh_clearance_plus_continue_releases_and_archives` | [tests/experiment/test_x5g1t_usage_files.py:203](../../tests/experiment/test_x5g1t_usage_files.py#L203) |  |
| `test_read_controls_missing_usage_files_continue` | test | `test_read_controls_missing_usage_files_continue` | [tests/experiment/test_x5g1t_usage_files.py:147](../../tests/experiment/test_x5g1t_usage_files.py#L147) |  |
| `test_read_controls_mode_edited_to_working_does_not_release` | test | `test_read_controls_mode_edited_to_working_does_not_release` | [tests/experiment/test_x5g1t_usage_files.py:195](../../tests/experiment/test_x5g1t_usage_files.py#L195) |  |
| `test_read_controls_multi_limit_hold_and_latch` | test | `test_read_controls_multi_limit_hold_and_latch` | [tests/experiment/test_x5g1t_usage_files.py:154](../../tests/experiment/test_x5g1t_usage_files.py#L154) |  |
| `test_read_controls_naive_or_nonstring_time_not_release` | test | `test_read_controls_naive_or_nonstring_time_not_release` | [tests/experiment/test_x5g1t_usage_files.py:188](../../tests/experiment/test_x5g1t_usage_files.py#L188) |  |
| `test_read_controls_stale_evidence_holds` | test | `test_read_controls_stale_evidence_holds` | [tests/experiment/test_x5g1t_usage_files.py:180](../../tests/experiment/test_x5g1t_usage_files.py#L180) |  |
| `test_read_controls_unavailable_alone_continues` | test | `test_read_controls_unavailable_alone_continues` | [tests/experiment/test_x5g1t_usage_files.py:167](../../tests/experiment/test_x5g1t_usage_files.py#L167) |  |
| `test_read_controls_unknown_values_stop` | test | `test_read_controls_unknown_values_stop` | [tests/experiment/test_x5g1t_usage_files.py:173](../../tests/experiment/test_x5g1t_usage_files.py#L173) |  |
| `test_read_controls_warning_hold` | test | `test_read_controls_warning_hold` | [tests/experiment/test_x5g1t_usage_files.py:161](../../tests/experiment/test_x5g1t_usage_files.py#L161) |  |
| `test_read_json_refuses_other_files` | test | `test_read_json_refuses_other_files` | [tests/hws/test_b_kc1.py:257](../../tests/hws/test_b_kc1.py#L257) |  |
| `test_read_through_backend_never_writes_to_the_main_store` | test | `test_read_through_backend_never_writes_to_the_main_store` | [tests/experiment/test_x4b.py:59](../../tests/experiment/test_x4b.py#L59) |  |
| `test_readout_and_placebo_checks` | test | `test_readout_and_placebo_checks` | [tests/x6_stage1/test_a_rules.py:150](../../tests/x6_stage1/test_a_rules.py#L150) |  |
| `test_readout_basis_is_positive_diagonal_qr_of_diag_gamma_helmert` | test | `test_readout_basis_is_positive_diagonal_qr_of_diag_gamma_helmert` | [tests/c2_readout/test_a_readout.py:80](../../tests/c2_readout/test_a_readout.py#L80) |  |
| `test_readout_exact_positivity_and_float` | test | `test_readout_exact_positivity_and_float` | [tests/x6_stage1/test_a_eval.py:254](../../tests/x6_stage1/test_a_eval.py#L254) |  |
| `test_readout_floor_on_exact_laws_t17` | test | `test_readout_floor_on_exact_laws_t17` | [tests/x6_stage1/test_a_eval.py:273](../../tests/x6_stage1/test_a_eval.py#L273) |  |
| `test_readout_identity_rule` | test | `test_readout_identity_rule` | [tests/c2_readout/test_b_patch.py:284](../../tests/c2_readout/test_b_patch.py#L284) |  |
| `test_readout_position_index` | test | `test_readout_position_index` | [tests/x6_stage1/test_a_eval.py:87](../../tests/x6_stage1/test_a_eval.py#L87) |  |
| `test_real_block_streams_match_contract` | test | `test_real_block_streams_match_contract` | [tests/hwsb/test_b_streams.py:50](../../tests/hwsb/test_b_streams.py#L50) |  |
| `test_real_downstream_margin_and_f_plan` | test | `test_real_downstream_margin_and_f_plan` | [tests/k4b/test_a_transport_bound.py:82](../../tests/k4b/test_a_transport_bound.py#L82) |  |
| `test_real_kernel_unavailable_raises_identity` | test | `test_real_kernel_unavailable_raises_identity` | [tests/k4b/test_a_transport_bound.py:143](../../tests/k4b/test_a_transport_bound.py#L143) | Unpatched: coords that are not the documented 12x12 lattice make the reused kernel |
| `test_real_meter_kills_overdue_marked_operation` | test | `test_real_meter_kills_overdue_marked_operation` | [tests/circle_history/test_builder_v24_runtime.py:170](../../tests/circle_history/test_builder_v24_runtime.py#L170) |  |
| `test_real_status_bounded_and_reused_keys_kept` | test | `test_real_status_bounded_and_reused_keys_kept` | [tests/k4b/test_a_transport_bound.py:59](../../tests/k4b/test_a_transport_bound.py#L59) |  |
| `test_real_tables_have_pairwise_disjoint_ids` | test | `test_real_tables_have_pairwise_disjoint_ids` | [tests/hwsb/test_b_streams.py:127](../../tests/hwsb/test_b_streams.py#L127) |  |
| `test_real_train_dev_streams_match_contract` | test | `test_real_train_dev_streams_match_contract` | [tests/hwsb/test_b_streams.py:40](../../tests/hwsb/test_b_streams.py#L40) |  |
| `test_real_z_bound_is_exact_fraction_of_exact_upper` | test | `test_real_z_bound_is_exact_fraction_of_exact_upper` | [tests/k4b/test_a_transport_bound.py:68](../../tests/k4b/test_a_transport_bound.py#L68) |  |
| `test_real_z_bound_sanity_band` | test | `test_real_z_bound_sanity_band` | [tests/k4b/test_a_transport_bound.py:77](../../tests/k4b/test_a_transport_bound.py#L77) |  |
| `test_realistic_boundary_with_prior_ledger` | test | `test_realistic_boundary_with_prior_ledger` | [tests/experiment/test_x5g1t_runtime_boundary.py:170](../../tests/experiment/test_x5g1t_runtime_boundary.py#L170) |  |
| `test_realistic_multi_limit_only_relevant_high_one_blocks` | test | `test_realistic_multi_limit_only_relevant_high_one_blocks` | [tests/experiment/test_x5g1t_usage.py:110](../../tests/experiment/test_x5g1t_usage.py#L110) |  |
| `test_recipe_equals_contract_and_passes` | test | `test_recipe_equals_contract_and_passes` | [tests/hwsb/test_b_e4path.py:46](../../tests/hwsb/test_b_e4path.py#L46) |  |
| `test_recipe_equals_the_e4_checkpoint_extra_json` | test | `test_recipe_equals_the_e4_checkpoint_extra_json` | [tests/hwsb/test_b_e4path.py:52](../../tests/hwsb/test_b_e4path.py#L52) |  |
| `test_recipe_model_field_change_is_refused` | test | `test_recipe_model_field_change_is_refused` | [tests/hwsb/test_b_e4path.py:75](../../tests/hwsb/test_b_e4path.py#L75) |  |
| `test_recipe_train_field_change_is_refused` | test | `test_recipe_train_field_change_is_refused` | [tests/hwsb/test_b_e4path.py:82](../../tests/hwsb/test_b_e4path.py#L82) |  |
| `test_record_outcome_refuses_overwrite` | test | `test_record_outcome_refuses_overwrite` | [tests/experiment/test_x5g1t_runtime_boundary.py:90](../../tests/experiment/test_x5g1t_runtime_boundary.py#L90) |  |
| `test_record_published_only_after_checkpoint_verifies` | test | `test_record_published_only_after_checkpoint_verifies` | [tests/x6_stage1/test_b_train_chain.py:386](../../tests/x6_stage1/test_b_train_chain.py#L386) |  |
| `test_recorded_technical_failure_beats_everything` | test | `test_recorded_technical_failure_beats_everything` | [tests/hwsb/test_a_outcomes.py:112](../../tests/hwsb/test_a_outcomes.py#L112) |  |
| `test_reference_boundary_construction` | test | `test_reference_boundary_construction` | [tests/hwsb/test_a_learning.py:146](../../tests/hwsb/test_a_learning.py#L146) |  |
| `test_reference_boundary_sd_exists` | test | `test_reference_boundary_sd_exists` | [tests/hwsb/test_a_ladder.py:248](../../tests/hwsb/test_a_ladder.py#L248) |  |
| `test_reference_cache_reader_keeps_only_32_symbol_entries` | test | `test_reference_cache_reader_keeps_only_32_symbol_entries` | [tests/c1prime_registry/test_registry_builder.py:38](../../tests/c1prime_registry/test_registry_builder.py#L38) |  |
| `test_reference_cases_land_as_planted` | test | `test_reference_cases_land_as_planted` | [tests/hwsb/test_a_ladder.py:139](../../tests/hwsb/test_a_ladder.py#L139) |  |
| `test_reference_check_rows_pass_and_fail` | test | `test_reference_check_rows_pass_and_fail` | [tests/circle_history/test_error_bound.py:345](../../tests/circle_history/test_error_bound.py#L345) |  |
| `test_reference_code_agrees_with_the_old_enclosure_at_5_4` | test | `test_reference_code_agrees_with_the_old_enclosure_at_5_4` | [tests/hwsb/test_b_meter_law.py:231](../../tests/hwsb/test_b_meter_law.py#L231) |  |
| `test_reference_contract_licences_carry_protocol_clauses` | test | `test_reference_contract_licences_carry_protocol_clauses` | [tests/hwsb/test_a_outcomes.py:87](../../tests/hwsb/test_a_outcomes.py#L87) |  |
| `test_reference_endpoints_match_reused` | test | `test_reference_endpoints_match_reused` | [tests/hwsb/test_a_endpoints.py:91](../../tests/hwsb/test_a_endpoints.py#L91) |  |
| `test_reference_has_informed_band_edges` | test | `test_reference_has_informed_band_edges` | [tests/d2a/test_b_targets.py:138](../../tests/d2a/test_b_targets.py#L138) |  |
| `test_reference_kl_matches_reused` | test | `test_reference_kl_matches_reused` | [tests/hwsb/test_a_learning.py:141](../../tests/hwsb/test_a_learning.py#L141) |  |
| `test_reference_marginal_matches_reused` | test | `test_reference_marginal_matches_reused` | [tests/hwsb/test_a_learning.py:132](../../tests/hwsb/test_a_learning.py#L132) |  |
| `test_reference_oracle_is_C0_bitwise_and_obeys_theorem1` | test | `test_reference_oracle_is_C0_bitwise_and_obeys_theorem1` | [tests/c1prime/test_b_cert_oracle.py:146](../../tests/c1prime/test_b_cert_oracle.py#L146) |  |
| `test_reference_round60_agrees_with_decimal_division` | test | `test_reference_round60_agrees_with_decimal_division` | [tests/hwsb/test_a_enclosure_proof.py:133](../../tests/hwsb/test_a_enclosure_proof.py#L133) |  |
| `test_reference_rule_equals_k4b_ladder` | test | `test_reference_rule_equals_k4b_ladder` | [tests/hwsb/test_a_ladder.py:145](../../tests/hwsb/test_a_ladder.py#L145) |  |
| `test_reference_sigma_5_4_logits_terminate` | test | `test_reference_sigma_5_4_logits_terminate` | [tests/hwsb/test_a_enclosure_proof.py:141](../../tests/hwsb/test_a_enclosure_proof.py#L141) |  |
| `test_reference_states_are_the_documented_lattice` | test | `test_reference_states_are_the_documented_lattice` | [tests/hwsb/test_a_enclosure_proof.py:127](../../tests/hwsb/test_a_enclosure_proof.py#L127) |  |
| `test_reference_step3_inequalities_for_u_qmax` | test | `test_reference_step3_inequalities_for_u_qmax` | [tests/hwsb/test_a_enclosure_proof.py:146](../../tests/hwsb/test_a_enclosure_proof.py#L146) |  |
| `test_reference_tree_mean_matches_reused` | test | `test_reference_tree_mean_matches_reused` | [tests/hwsb/test_a_endpoints.py:84](../../tests/hwsb/test_a_endpoints.py#L84) |  |
| `test_reference_ulp_construction_is_exact` | test | `test_reference_ulp_construction_is_exact` | [tests/hwsb/test_a_capture.py:129](../../tests/hwsb/test_a_capture.py#L129) |  |
| `test_reference_z_b23_value` | test | `test_reference_z_b23_value` | [tests/hwsb/test_a_learning.py:126](../../tests/hwsb/test_a_learning.py#L126) |  |
| `test_reference_z_values_match_contract_report_values` | test | `test_reference_z_values_match_contract_report_values` | [tests/hwsb/test_a_capture.py:122](../../tests/hwsb/test_a_capture.py#L122) |  |
| `test_refinalisation_creates_new_snapshot_and_preserves_earlier` | test | `test_refinalisation_creates_new_snapshot_and_preserves_earlier` | [tests/x6_stage1/test_b_ingest_bundle.py:347](../../tests/x6_stage1/test_b_ingest_bundle.py#L347) |  |
| `test_reflection_symmetric_cells` | test | `test_reflection_symmetric_cells` | [tests/hws/test_b_worlds.py:315](../../tests/hws/test_b_worlds.py#L315) |  |
| `test_regen_compare_bit_identical` | test | `test_regen_compare_bit_identical` | [tests/c2_readout/test_b_lineage.py:299](../../tests/c2_readout/test_b_lineage.py#L299) |  |
| `test_regenerated_identical` | test | `test_regenerated_identical` | [tests/k4b/test_b_rerun.py:178](../../tests/k4b/test_b_rerun.py#L178) |  |
| `test_regenerated_init_states_are_bit_identical` | test | `test_regenerated_init_states_are_bit_identical` | [tests/x6_stage1/test_b_chain_ops.py:238](../../tests/x6_stage1/test_b_chain_ops.py#L238) |  |
| `test_registered_constants_and_flat_face` | test | `test_registered_constants_and_flat_face` | [tests/x6_stage1/test_a_designed.py:99](../../tests/x6_stage1/test_a_designed.py#L99) |  |
| `test_registered_templates_exact_g0_tpl_sample` | test | `test_registered_templates_exact_g0_tpl_sample` | [tests/d2a/test_a_templates.py:140](../../tests/d2a/test_a_templates.py#L140) | Every 32nd registered t = 28 pair and every 8th t = 16 pair, exactly (G0-TPL values). |
| `test_registry_digests_are_the_history_digest_set` | test | `test_registry_digests_are_the_history_digest_set` | [tests/c1prime/test_b_registry.py:127](../../tests/c1prime/test_b_registry.py#L127) |  |
| `test_registry_digests_pass_and_match_history_digests` | test | `test_registry_digests_pass_and_match_history_digests` | [tests/hwsb/test_b_registry.py:98](../../tests/hwsb/test_b_registry.py#L98) |  |
| `test_registry_digests_without_expected_also_pass` | test | `test_registry_digests_without_expected_also_pass` | [tests/hwsb/test_b_registry.py:110](../../tests/hwsb/test_b_registry.py#L110) |  |
| `test_registry_load_rehash_mismatch_is_lineage` | test | `test_registry_load_rehash_mismatch_is_lineage` | [tests/c2_readout/test_b_registry.py:298](../../tests/c2_readout/test_b_registry.py#L298) |  |
| `test_registry_names` | test | `test_registry_names` | [tests/topology/test_metrics.py:17](../../tests/topology/test_metrics.py#L17) |  |
| `test_registry_untouched_by_import_and_build` | test | `test_registry_untouched_by_import_and_build` | [tests/d1_seam/test_d1_seam.py:220](../../tests/d1_seam/test_d1_seam.py#L220) |  |
| `test_registry_untouched_by_import_and_build` | test | `test_registry_untouched_by_import_and_build` | [tests/x2a_stage0/test_x2a_stage0.py:346](../../tests/x2a_stage0/test_x2a_stage0.py#L346) |  |
| `test_regret_batch_invariant_and_training_flag_restored` | test | `test_regret_batch_invariant_and_training_flag_restored` | [tests/experiment/test_x5g1t_lineage_oracle.py:288](../../tests/experiment/test_x5g1t_lineage_oracle.py#L288) |  |
| `test_regret_zero_on_own_softmax_and_nonnegative` | test | `test_regret_zero_on_own_softmax_and_nonnegative` | [tests/experiment/test_x5g1t_lineage_oracle.py:277](../../tests/experiment/test_x5g1t_lineage_oracle.py#L277) |  |
| `test_rejection_before_sampler_leaves_no_study_root` | test | `test_rejection_before_sampler_leaves_no_study_root` | [tests/experiment/test_x5g1t_config_checks.py:294](../../tests/experiment/test_x5g1t_config_checks.py#L294) | Rejection happens before any sampler/model: spies record nothing, study root absent. |
| `test_rel_agree_at_the_relative_boundary` | test | `test_rel_agree_at_the_relative_boundary` | [tests/c1prime/test_a_oracle.py:225](../../tests/c1prime/test_a_oracle.py#L225) | 9007 * 2^-52 < 2e-12 < 9008 * 2^-52 (exact rationals). |
| `test_relaxed_thresholds_reach_precision_and_export` | test | `test_relaxed_thresholds_reach_precision_and_export` | [tests/circle_history/test_builder_e2e.py:182](../../tests/circle_history/test_builder_e2e.py#L182) |  |
| `test_release_accepts_exact_binding` | test | `test_release_accepts_exact_binding` | [tests/circle_history/test_builder_runtime.py:129](../../tests/circle_history/test_builder_runtime.py#L129) |  |
| `test_release_binding_refusals` | test | `test_release_binding_refusals` | [tests/c2_readout/test_b_policy.py:248](../../tests/c2_readout/test_b_policy.py#L248) |  |
| `test_release_constants` | test | `test_release_constants` | [tests/c1prime/test_a_release_meter.py:112](../../tests/c1prime/test_a_release_meter.py#L112) |  |
| `test_release_in_other_order` | test | `test_release_in_other_order` | [tests/experiment/test_x5g1t_runtime.py:248](../../tests/experiment/test_x5g1t_runtime.py#L248) |  |
| `test_release_outside_the_dispatched_job_directory_is_refused` | test | `test_release_outside_the_dispatched_job_directory_is_refused` | [tests/c1prime/test_a_release_meter.py:163](../../tests/c1prime/test_a_release_meter.py#L163) |  |
| `test_release_r5_must_carry_n_test_and_k` | test | `test_release_r5_must_carry_n_test_and_k` | [tests/c2_readout/test_b_policy.py:258](../../tests/c2_readout/test_b_policy.py#L258) |  |
| `test_release_refuses_any_mismatch` | test | `test_release_refuses_any_mismatch` | [tests/circle_history/test_builder_runtime.py:148](../../tests/circle_history/test_builder_runtime.py#L148) |  |
| `test_release_refuses_wrong_location_and_unreadable` | test | `test_release_refuses_wrong_location_and_unreadable` | [tests/circle_history/test_builder_runtime.py:155](../../tests/circle_history/test_builder_runtime.py#L155) |  |
| `test_release_session_named_in_task` | test | `test_release_session_named_in_task` | [tests/c1prime/test_c_release_worker.py:31](../../tests/c1prime/test_c_release_worker.py#L31) |  |
| `test_release_session_not_in_task_is_refused` | test | `test_release_session_not_in_task_is_refused` | [tests/c1prime/test_c_release_worker.py:36](../../tests/c1prime/test_c_release_worker.py#L36) |  |
| `test_release_strict_boolean_in_verify` | test | `test_release_strict_boolean_in_verify` | [tests/circle_history/test_builder_guards.py:174](../../tests/circle_history/test_builder_guards.py#L174) |  |
| `test_released_and_withheld_labels` | test | `test_released_and_withheld_labels` | [tests/x2a_stage0/test_x2a_stage0_ph.py:171](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L171) |  |
| `test_relevant_warning_blocks_with_null_percent` | test | `test_relevant_warning_blocks_with_null_percent` | [tests/experiment/test_x5g1t_usage.py:129](../../tests/experiment/test_x5g1t_usage.py#L129) |  |
| `test_removing_worker_control_releases_coordinator_hold` | test | `test_removing_worker_control_releases_coordinator_hold` | [tests/experiment/test_x5g1t_runtime.py:257](../../tests/experiment/test_x5g1t_runtime.py#L257) |  |
| `test_renamed_hist_file_fails_closed` | test | `test_renamed_hist_file_fails_closed` | [tests/hwsb/test_b_registry.py:144](../../tests/hwsb/test_b_registry.py#L144) |  |
| `test_repair_ancestry_and_d2a_unchanged` | test | `test_repair_ancestry_and_d2a_unchanged` | [tests/x6_stage1/test_b_nb_s0_ops.py:221](../../tests/x6_stage1/test_b_nb_s0_ops.py#L221) |  |
| `test_repair_blob_hashes_at_head` | test | `test_repair_blob_hashes_at_head` | [tests/x6_stage1/test_b_nb_s0_ops.py:214](../../tests/x6_stage1/test_b_nb_s0_ops.py#L214) |  |
| `test_repeated_builds_are_identical` | test | `test_repeated_builds_are_identical` | [tests/hws/test_b_worlds.py:207](../../tests/hws/test_b_worlds.py#L207) |  |
| `test_replacement_wrong_shape` | test | `test_replacement_wrong_shape` | [tests/learner/test_patch.py:253](../../tests/learner/test_patch.py#L253) |  |
| `test_report_with_width_and_supported_contribution_refused` | test | `test_report_with_width_and_supported_contribution_refused` | [tests/k4b/test_b_flow.py:73](../../tests/k4b/test_b_flow.py#L73) | C = mean(A u r4) beside D = width/2 would unseal X-bar(+/-) = C +/- D (RC3). |
| `test_request_and_control_stop` | test | `test_request_and_control_stop` | [tests/oracle_profile/test_builder_controls.py:63](../../tests/oracle_profile/test_builder_controls.py#L63) |  |
| `test_request_missing_or_bad_fails_closed` | test | `test_request_missing_or_bad_fails_closed` | [tests/experiment/test_x5g1t_runtime.py:80](../../tests/experiment/test_x5g1t_runtime.py#L80) |  |
| `test_request_stop_command` | test | `test_request_stop_command` | [tests/experiment/test_x5g1t_runtime.py:72](../../tests/experiment/test_x5g1t_runtime.py#L72) |  |
| `test_require_frozen_refuses_without_record` | test | `test_require_frozen_refuses_without_record` | [tests/k4b/test_b_charts.py:262](../../tests/k4b/test_b_charts.py#L262) |  |
| `test_require_int_keys_rejects_str_missing_or_extra` | test | `test_require_int_keys_rejects_str_missing_or_extra` | [tests/k4b/test_b_data.py:91](../../tests/k4b/test_b_data.py#L91) |  |
| `test_require_int_keys_returns_the_same_dict` | test | `test_require_int_keys_returns_the_same_dict` | [tests/k4b/test_b_data.py:80](../../tests/k4b/test_b_data.py#L80) |  |
| `test_require_scoring_accepts_verified_shape` | test | `test_require_scoring_accepts_verified_shape` | [tests/circle_history/test_builder_guards.py:109](../../tests/circle_history/test_builder_guards.py#L109) |  |
| `test_require_scoring_denies_non_authority` | test | `test_require_scoring_denies_non_authority` | [tests/circle_history/test_builder_guards.py:97](../../tests/circle_history/test_builder_guards.py#L97) |  |
| `test_require_scoring_denies_wrong_scope_or_sha` | test | `test_require_scoring_denies_wrong_scope_or_sha` | [tests/circle_history/test_builder_guards.py:103](../../tests/circle_history/test_builder_guards.py#L103) |  |
| `test_require_table_over_every_gate` | test | `test_require_table_over_every_gate` | [tests/c2_readout/test_b_policy.py:83](../../tests/c2_readout/test_b_policy.py#L83) |  |
| `test_resid_post_0_patch_propagates_to_later_positions` | test | `test_resid_post_0_patch_propagates_to_later_positions` | [tests/learner/test_patch.py:111](../../tests/learner/test_patch.py#L111) | The forward continues through blocks[1]: later positions attend to the patched vector. |
| `test_resid_post_2_prefix_unchanged_and_own_patched_key_value` | test | `test_resid_post_2_prefix_unchanged_and_own_patched_key_value` | [tests/c2_readout/test_b_patch.py:171](../../tests/c2_readout/test_b_patch.py#L171) |  |
| `test_residual_difference_within_two_rho` | test | `test_residual_difference_within_two_rho` | [tests/k4b/test_a_lemma_t.py:122](../../tests/k4b/test_a_lemma_t.py#L122) |  |
| `test_residual_is_not_identically_zero` | test | `test_residual_is_not_identically_zero` | [tests/k4b/test_a_prop1.py:113](../../tests/k4b/test_a_prop1.py#L113) |  |
| `test_residual_keeps_the_phase_term` | test | `test_residual_keeps_the_phase_term` | [tests/c1prime/test_b_fwl.py:196](../../tests/c1prime/test_b_fwl.py#L196) |  |
| `test_residual_rows_and_profile_point_known_answer` | test | `test_residual_rows_and_profile_point_known_answer` | [tests/oracle_profile/test_oracle_profile_kernels.py:136](../../tests/oracle_profile/test_oracle_profile_kernels.py#L136) | r_1 = ((3, 4), (0, 1)) -> norm (5, 1), sq (25, 1); r_4 = ((0, 2), (0, 0)) -> (2, 0), (4, 0). |
| `test_residual_rows_custom_full_and_errors` | test | `test_residual_rows_custom_full_and_errors` | [tests/oracle_profile/test_oracle_profile_kernels.py:156](../../tests/oracle_profile/test_oracle_profile_kernels.py#L156) |  |
| `test_residual_rows_rejects_nonfinite_and_shape` | test | `test_residual_rows_rejects_nonfinite_and_shape` | [tests/oracle_profile/test_builder_kernels.py:64](../../tests/oracle_profile/test_builder_kernels.py#L64) |  |
| `test_restart_uses_stationary_pi` | test | `test_restart_uses_stationary_pi` | [tests/oracle_profile/test_oracle_profile_traps.py:177](../../tests/oracle_profile/test_oracle_profile_traps.py#L177) | Item 2: post_1 of (..., 0) is pi * E[:, 0] normalised, whatever came before. |
| `test_restore_records_is_byte_exact` | test | `test_restore_records_is_byte_exact` | [tests/k4b/test_b_rerun.py:88](../../tests/k4b/test_b_rerun.py#L88) |  |
| `test_restrict_reindexes_ascending_and_keeps_matching_cocycle_entries` | test | `test_restrict_reindexes_ascending_and_keeps_matching_cocycle_entries` | [tests/c1prime/test_a_chart.py:224](../../tests/c1prime/test_a_chart.py#L224) |  |
| `test_resultant_fails_while_bins_pass` | test | `test_resultant_fails_while_bins_pass` | [tests/c1prime/test_a_chart_val.py:143](../../tests/c1prime/test_a_chart_val.py#L143) |  |
| `test_resume_only_after_both_holds_released` | test | `test_resume_only_after_both_holds_released` | [tests/experiment/test_x5g1t_runtime.py:235](../../tests/experiment/test_x5g1t_runtime.py#L235) |  |
| `test_resume_regenerates_the_interrupted_world_bit_identically` | test | `test_resume_regenerates_the_interrupted_world_bit_identically` | [tests/hws/test_b_records.py:179](../../tests/hws/test_b_records.py#L179) |  |
| `test_resume_restores_state_and_checks_internal_consistency` | test | `test_resume_restores_state_and_checks_internal_consistency` | [tests/x6_stage1/test_b_train_chain.py:321](../../tests/x6_stage1/test_b_train_chain.py#L321) |  |
| `test_retrain_route_refused_after_admission_or_any_local_evaluation` | test | `test_retrain_route_refused_after_admission_or_any_local_evaluation` | [tests/x6_stage1/test_b_chain_ops.py:244](../../tests/x6_stage1/test_b_chain_ops.py#L244) |  |
| `test_returned_non_pass_dict_stops_the_cohort` | test | `test_returned_non_pass_dict_stops_the_cohort` | [tests/c1prime/test_a_exceptions.py:193](../../tests/c1prime/test_a_exceptions.py#L193) |  |
| `test_returned_pass_dict_is_recorded_and_returned` | test | `test_returned_pass_dict_is_recorded_and_returned` | [tests/c1prime/test_a_exceptions.py:185](../../tests/c1prime/test_a_exceptions.py#L185) |  |
| `test_reused_blob_hashes_equal_section_13_1_and_the_files` | test | `test_reused_blob_hashes_equal_section_13_1_and_the_files` | [tests/c2_readout/test_b_lineage.py:128](../../tests/c2_readout/test_b_lineage.py#L128) |  |
| `test_reused_k4_files_match_freeze` | test | `test_reused_k4_files_match_freeze` | [tests/chart_diag/test_chart_diag.py:81](../../tests/chart_diag/test_chart_diag.py#L81) |  |
| `test_reused_writers_refuse_existing_paths` | test | `test_reused_writers_refuse_existing_paths` | [tests/hws/test_b_records.py:120](../../tests/hws/test_b_records.py#L120) |  |
| `test_revalidate_coverage_complete_when_source_a_ids_cover_refs` | test | `test_revalidate_coverage_complete_when_source_a_ids_cover_refs` | [tests/k4b/test_b_registry_fixes.py:211](../../tests/k4b/test_b_registry_fixes.py#L211) |  |
| `test_revalidate_coverage_reports_the_removed_id` | test | `test_revalidate_coverage_reports_the_removed_id` | [tests/k4b/test_b_registry_fixes.py:217](../../tests/k4b/test_b_registry_fixes.py#L217) |  |
| `test_reversed_contrast_is_not_reproduced` | test | `test_reversed_contrast_is_not_reproduced` | [tests/d2a/test_b_behaviour.py:89](../../tests/d2a/test_b_behaviour.py#L89) |  |
| `test_rewrite_argv_appends_inf_caps` | test | `test_rewrite_argv_appends_inf_caps` | [tests/hwsb/test_b_meter_law.py:101](../../tests/hwsb/test_b_meter_law.py#L101) |  |
| `test_rewrite_argv_forces_infinite_cpu_and_wall` | test | `test_rewrite_argv_forces_infinite_cpu_and_wall` | [tests/k4b/test_b_meter.py:83](../../tests/k4b/test_b_meter.py#L83) |  |
| `test_rho_bar_ref_constants` | test | `test_rho_bar_ref_constants` | [tests/c1prime/test_b_cert_oracle.py:174](../../tests/c1prime/test_b_cert_oracle.py#L174) |  |
| `test_rho_index_from_coordinates` | test | `test_rho_index_from_coordinates` | [tests/c1prime/test_a_oracle.py:125](../../tests/c1prime/test_a_oracle.py#L125) |  |
| `test_rho_m_index_maps_on_the_full_grid` | test | `test_rho_m_index_maps_on_the_full_grid` | [tests/c2_readout/test_a_oracle.py:208](../../tests/c2_readout/test_a_oracle.py#L208) |  |
| `test_ridge_intercept_unpenalised_and_lambda_chosen_on_val` | test | `test_ridge_intercept_unpenalised_and_lambda_chosen_on_val` | [tests/prediction/test_ridge.py:36](../../tests/prediction/test_ridge.py#L36) |  |
| `test_ridge_stop_inside_solver_grid` | test | `test_ridge_stop_inside_solver_grid` | [tests/experiment/test_x4f_maintenance.py:61](../../tests/experiment/test_x4f_maintenance.py#L61) |  |
| `test_root_wrong_arm_cli_exits_3` | test | `test_root_wrong_arm_cli_exits_3` | [tests/experiment/test_x5g1t_identity.py:185](../../tests/experiment/test_x5g1t_identity.py#L185) |  |
| `test_root_wrong_arm_train_pool_refused_before_train_one` | test | `test_root_wrong_arm_train_pool_refused_before_train_one` | [tests/experiment/test_x5g1t_identity.py:175](../../tests/experiment/test_x5g1t_identity.py#L175) |  |
| `test_rotated_and_reflected_suffix_fields_stay_zero` | test | `test_rotated_and_reflected_suffix_fields_stay_zero` | [tests/k4b/test_a_prop1.py:142](../../tests/k4b/test_a_prop1.py#L142) | Gauge invariance: a rotation or reflection of a suffix-only field is suffix-only. |
| `test_rotation_oracle_rolls_b31_and_reapplies_w32` | test | `test_rotation_oracle_rolls_b31_and_reapplies_w32` | [tests/c2_readout/test_a_oracle.py:221](../../tests/c2_readout/test_a_oracle.py#L221) |  |
| `test_round_trip_is_exact_without_float` | test | `test_round_trip_is_exact_without_float` | [tests/circle_history/test_reference_cache.py:109](../../tests/circle_history/test_reference_cache.py#L109) |  |
| `test_round_trip_preserves_extension` | test | `test_round_trip_preserves_extension` | [tests/circle_history/test_chart_arrays.py:110](../../tests/circle_history/test_chart_arrays.py#L110) |  |
| `test_rounded_enclosure_contains_every_exact_w_star_entry_at_7_4` | test | `test_rounded_enclosure_contains_every_exact_w_star_entry_at_7_4` | [tests/hwsb/test_b_meter_law.py:240](../../tests/hwsb/test_b_meter_law.py#L240) |  |
| `test_route_f_is_taken_when_p1_fails_and_bounds_the_exact_error` | test | `test_route_f_is_taken_when_p1_fails_and_bounds_the_exact_error` | [tests/c1prime/test_b_cert_oracle.py:240](../../tests/c1prime/test_b_cert_oracle.py#L240) |  |
| `test_route_f_rejects_x_above_one_half` | test | `test_route_f_rejects_x_above_one_half` | [tests/c1prime/test_b_cert_oracle.py:259](../../tests/c1prime/test_b_cert_oracle.py#L259) |  |
| `test_row_arrays_keys_shapes_dtypes_and_formulas` | test | `test_row_arrays_keys_shapes_dtypes_and_formulas` | [tests/hws/test_b_oracle.py:134](../../tests/hws/test_b_oracle.py#L134) |  |
| `test_row_arrays_on_every_history` | test | `test_row_arrays_on_every_history` | [tests/hws/test_a_identities.py:346](../../tests/hws/test_a_identities.py#L346) |  |
| `test_row_bound_equals_independently_assembled_fractions` | test | `test_row_bound_equals_independently_assembled_fractions` | [tests/circle_history/test_error_bound.py:227](../../tests/circle_history/test_error_bound.py#L227) |  |
| `test_row_digests_keys_and_hex` | test | `test_row_digests_keys_and_hex` | [tests/x6_stage1/test_b_seed_pool_reg.py:216](../../tests/x6_stage1/test_b_seed_pool_reg.py#L216) |  |
| `test_row_tv_grid_and_documented` | test | `test_row_tv_grid_and_documented` | [tests/circle_history/test_process_law.py:123](../../tests/circle_history/test_process_law.py#L123) |  |
| `test_rows` | function | `test_rows` | [src/topo_pilot/experiment/s8.py:229](../../src/topo_pilot/experiment/s8.py#L229) |  |
| `test_rows_are_normalised_and_nonnegative` | test | `test_rows_are_normalised_and_nonnegative` | [tests/oracle_profile/test_oracle_profile.py:144](../../tests/oracle_profile/test_oracle_profile.py#L144) | Item 5. |
| `test_rowwise_pinsker` | test | `test_rowwise_pinsker` | [tests/hws/test_a_identities.py:311](../../tests/hws/test_a_identities.py#L311) |  |
| `test_rs1_rs2_monte_carlo_against_random_ref` | test | `test_rs1_rs2_monte_carlo_against_random_ref` | [tests/c2_readout/test_a_partition.py:178](../../tests/c2_readout/test_a_partition.py#L178) |  |
| `test_rule1_stop_failures` | test | `test_rule1_stop_failures` | [tests/d2a/test_b_rules_decide.py:97](../../tests/d2a/test_b_rules_decide.py#L97) |  |
| `test_rule2_stage1_stops_precede_validity_and_have_no_qualifiers` | test | `test_rule2_stage1_stops_precede_validity_and_have_no_qualifiers` | [tests/d2a/test_b_rules_decide.py:104](../../tests/d2a/test_b_rules_decide.py#L104) |  |
| `test_rule3_pipeline_invalid_precedes_rule4_and_has_no_qualifiers` | test | `test_rule3_pipeline_invalid_precedes_rule4_and_has_no_qualifiers` | [tests/d2a/test_b_rules_decide.py:110](../../tests/d2a/test_b_rules_decide.py#L110) |  |
| `test_rule4_branches` | test | `test_rule4_branches` | [tests/d2a/test_b_rules_decide.py:130](../../tests/d2a/test_b_rules_decide.py#L130) |  |
| `test_rule4_l1_true_continues` | test | `test_rule4_l1_true_continues` | [tests/d2a/test_b_rules_decide.py:142](../../tests/d2a/test_b_rules_decide.py#L142) |  |
| `test_rule4_precedes_rule5` | test | `test_rule4_precedes_rule5` | [tests/d2a/test_b_rules_decide.py:151](../../tests/d2a/test_b_rules_decide.py#L151) |  |
| `test_rule5_horizon_dependent` | test | `test_rule5_horizon_dependent` | [tests/d2a/test_b_rules_decide.py:159](../../tests/d2a/test_b_rules_decide.py#L159) |  |
| `test_rule5_missing_h2_model_counts_as_failing` | test | `test_rule5_missing_h2_model_counts_as_failing` | [tests/d2a/test_b_rules_decide.py:189](../../tests/d2a/test_b_rules_decide.py#L189) |  |
| `test_rule5_needs_the_same_three_seeds_for_all_conditions` | test | `test_rule5_needs_the_same_three_seeds_for_all_conditions` | [tests/d2a/test_b_rules_decide.py:163](../../tests/d2a/test_b_rules_decide.py#L163) |  |
| `test_rule5_nonpositive_or_missing_delta_fails_that_seed` | test | `test_rule5_nonpositive_or_missing_delta_fails_that_seed` | [tests/d2a/test_b_rules_decide.py:180](../../tests/d2a/test_b_rules_decide.py#L180) |  |
| `test_rule5_two_joint_seeds_is_not_enough` | test | `test_rule5_two_joint_seeds_is_not_enough` | [tests/d2a/test_b_rules_decide.py:171](../../tests/d2a/test_b_rules_decide.py#L171) |  |
| `test_rule6_horizon_enhanced` | test | `test_rule6_horizon_enhanced` | [tests/d2a/test_b_rules_decide.py:198](../../tests/d2a/test_b_rules_decide.py#L198) |  |
| `test_rule7_carried_without_horizon_effect` | test | `test_rule7_carried_without_horizon_effect` | [tests/d2a/test_b_rules_decide.py:214](../../tests/d2a/test_b_rules_decide.py#L214) |  |
| `test_rule7_needs_both_arms` | test | `test_rule7_needs_both_arms` | [tests/d2a/test_b_rules_decide.py:219](../../tests/d2a/test_b_rules_decide.py#L219) |  |
| `test_rule8_needs_three_seeds_of_each` | test | `test_rule8_needs_three_seeds_of_each` | [tests/d2a/test_b_rules_decide.py:255](../../tests/d2a/test_b_rules_decide.py#L255) |  |
| `test_rule8_precedes_rule9` | test | `test_rule8_precedes_rule9` | [tests/d2a/test_b_rules_decide.py:246](../../tests/d2a/test_b_rules_decide.py#L246) |  |
| `test_rule8_predictive_without_linear_posterior` | test | `test_rule8_predictive_without_linear_posterior` | [tests/d2a/test_b_rules_decide.py:242](../../tests/d2a/test_b_rules_decide.py#L242) |  |
| `test_rule9_needs_low_increment_in_both_arms` | test | `test_rule9_needs_low_increment_in_both_arms` | [tests/d2a/test_b_rules_decide.py:288](../../tests/d2a/test_b_rules_decide.py#L288) |  |
| `test_rule9_needs_valid_controls` | test | `test_rule9_needs_valid_controls` | [tests/d2a/test_b_rules_decide.py:279](../../tests/d2a/test_b_rules_decide.py#L279) |  |
| `test_rule9_not_recovered` | test | `test_rule9_not_recovered` | [tests/d2a/test_b_rules_decide.py:264](../../tests/d2a/test_b_rules_decide.py#L264) |  |
| `test_rule9_precision_failure_gives_inconclusive_precision_limited` | test | `test_rule9_precision_failure_gives_inconclusive_precision_limited` | [tests/d2a/test_b_rules_decide.py:271](../../tests/d2a/test_b_rules_decide.py#L271) |  |
| `test_run_c1_gate_records_and_stops` | test | `test_run_c1_gate_records_and_stops` | [tests/c1prime/test_a_exceptions.py:145](../../tests/c1prime/test_a_exceptions.py#L145) |  |
| `test_run_gate_taxonomy` | test | `test_run_gate_taxonomy` | [tests/circle_history/test_builder_v24_stages.py:33](../../tests/circle_history/test_builder_v24_stages.py#L33) |  |
| `test_run_gates_all_pass_in_order` | test | `test_run_gates_all_pass_in_order` | [tests/k4b/test_b_flow.py:155](../../tests/k4b/test_b_flow.py#L155) |  |
| `test_run_kb_default_store_reaches_kb0` | test | `test_run_kb_default_store_reaches_kb0` | [tests/hwsb/test_r_0168_kb_default_store.py:24](../../tests/hwsb/test_r_0168_kb_default_store.py#L24) |  |
| `test_run_lock_identity_follows_the_release_session` | test | `test_run_lock_identity_follows_the_release_session` | [tests/k4b/test_b_meter.py:69](../../tests/k4b/test_b_meter.py#L69) |  |
| `test_run_metrics_and_probes_deferred` | test | `test_run_metrics_and_probes_deferred` | [tests/prediction/test_stage.py:70](../../tests/prediction/test_stage.py#L70) |  |
| `test_run_oracle_is_bayesfilter_with_the_section_3_3_indices` | test | `test_run_oracle_is_bayesfilter_with_the_section_3_3_indices` | [tests/c1prime/test_a_oracle_named.py:101](../../tests/c1prime/test_a_oracle_named.py#L101) |  |
| `test_run_with_failed_preflight_is_invalid` | test | `test_run_with_failed_preflight_is_invalid` | [tests/x2a_stage0/test_x2a_stage0_ph.py:288](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L288) |  |
| `test_run_without_passing_preflight_is_invalid` | test | `test_run_without_passing_preflight_is_invalid` | [tests/d1_seam/test_d1_seam.py:393](../../tests/d1_seam/test_d1_seam.py#L393) |  |
| `test_runlock_is_exclusive_and_removed` | test | `test_runlock_is_exclusive_and_removed` | [tests/experiment/test_x5g1t_runtime_boundary.py:40](../../tests/experiment/test_x5g1t_runtime_boundary.py#L40) |  |
| `test_runlock_refuses_stale_lock_of_unknown_state` | test | `test_runlock_refuses_stale_lock_of_unknown_state` | [tests/experiment/test_x5g1t_runtime_boundary.py:57](../../tests/experiment/test_x5g1t_runtime_boundary.py#L57) |  |
| `test_runlock_removed_on_error_and_never_suppresses` | test | `test_runlock_removed_on_error_and_never_suppresses` | [tests/experiment/test_x5g1t_runtime_boundary.py:66](../../tests/experiment/test_x5g1t_runtime_boundary.py#L66) |  |
| `test_runner_persists_prior_cpu_and_failure` | test | `test_runner_persists_prior_cpu_and_failure` | [tests/experiment/test_x4f_maintenance.py:22](../../tests/experiment/test_x4f_maintenance.py#L22) |  |
| `test_runner_refuses_without_release` | test | `test_runner_refuses_without_release` | [tests/circle_history/test_builder_runtime.py:165](../../tests/circle_history/test_builder_runtime.py#L165) |  |
| `test_runs_are_the_fourteen_registered_models` | test | `test_runs_are_the_fourteen_registered_models` | [tests/d2a/test_b_resource.py:44](../../tests/d2a/test_b_resource.py#L44) |  |
| `test_runtime_state_malformed_is_stop` | test | `test_runtime_state_malformed_is_stop` | [tests/experiment/test_x5g1t_runtime.py:128](../../tests/experiment/test_x5g1t_runtime.py#L128) |  |
| `test_runtime_state_other_modes_are_noop` | test | `test_runtime_state_other_modes_are_noop` | [tests/experiment/test_x5g1t_runtime.py:115](../../tests/experiment/test_x5g1t_runtime.py#L115) |  |
| `test_runtime_state_unknown_mode_is_stop` | test | `test_runtime_state_unknown_mode_is_stop` | [tests/experiment/test_x5g1t_runtime.py:122](../../tests/experiment/test_x5g1t_runtime.py#L122) |  |
| `test_runtime_state_wait_is_hold` | test | `test_runtime_state_wait_is_hold` | [tests/experiment/test_x5g1t_runtime.py:108](../../tests/experiment/test_x5g1t_runtime.py#L108) |  |
| `test_s2_and_s3_forecasts_are_sums_over_the_actual_worklist` | test | `test_s2_and_s3_forecasts_are_sums_over_the_actual_worklist` | [tests/hws/test_a_budget.py:65](../../tests/hws/test_a_budget.py#L65) |  |
| `test_s2_worklist_cap_40_by_changed_distance_key` | test | `test_s2_worklist_cap_40_by_changed_distance_key` | [tests/hws/test_a_classify.py:363](../../tests/hws/test_a_classify.py#L363) |  |
| `test_s2_worklist_edges_lowest_tier` | test | `test_s2_worklist_edges_lowest_tier` | [tests/hws/test_a_classify.py:341](../../tests/hws/test_a_classify.py#L341) |  |
| `test_s2_worklist_uses_x1_levels_that_ran` | test | `test_s2_worklist_uses_x1_levels_that_ran` | [tests/hws/test_a_classify.py:355](../../tests/hws/test_a_classify.py#L355) |  |
| `test_s3_bounds_l3_is_the_smaller_side` | test | `test_s3_bounds_l3_is_the_smaller_side` | [tests/hws/test_a_stats.py:111](../../tests/hws/test_a_stats.py#L111) |  |
| `test_s3_evaluate` | test | `test_s3_evaluate` | [tests/hws/test_a_outcomes.py:281](../../tests/hws/test_a_outcomes.py#L281) |  |
| `test_s3_rates_and_s0_refused` | test | `test_s3_rates_and_s0_refused` | [tests/hws/test_a_budget.py:43](../../tests/hws/test_a_budget.py#L43) |  |
| `test_s_max_inverted_cdf_rank` | test | `test_s_max_inverted_cdf_rank` | [tests/c1prime/test_a_eligibility_support.py:37](../../tests/c1prime/test_a_eligibility_support.py#L37) | Ranks: 1000 * 0.999 = 999 exactly in float -> 999th smallest (value 998); |
| `test_s_max_with_ties_at_the_boundary_returns_an_input_value` | test | `test_s_max_with_ties_at_the_boundary_returns_an_input_value` | [tests/c1prime/test_a_eligibility_support.py:46](../../tests/c1prime/test_a_eligibility_support.py#L46) | n = 1000: the 999th smallest value (sorted index 998) is returned, never interpolated. |
| `test_s_star_fit_uses_masked_regressors_and_is_deterministic` | test | `test_s_star_fit_uses_masked_regressors_and_is_deterministic` | [tests/c2_readout/test_b_screens.py:153](../../tests/c2_readout/test_b_screens.py#L153) |  |
| `test_same_gate_again_and_stage_entry_keep_the_position` | test | `test_same_gate_again_and_stage_entry_keep_the_position` | [tests/c2_readout/test_b_policy.py:132](../../tests/c2_readout/test_b_policy.py#L132) |  |
| `test_same_last_symbol_finite_when_b1_is_a_function_of_w32` | test | `test_same_last_symbol_finite_when_b1_is_a_function_of_w32` | [tests/analysis/test_geometry.py:93](../../tests/analysis/test_geometry.py#L93) |  |
| `test_same_last_symbol_none_when_activation_distances_constant` | test | `test_same_last_symbol_none_when_activation_distances_constant` | [tests/analysis/test_geometry.py:110](../../tests/analysis/test_geometry.py#L110) |  |
| `test_same_last_symbol_value_matches_restricted_spearman` | test | `test_same_last_symbol_value_matches_restricted_spearman` | [tests/analysis/test_geometry.py:79](../../tests/analysis/test_geometry.py#L79) |  |
| `test_same_message_not_raised_by_integer_lift_is_technical` | test | `test_same_message_not_raised_by_integer_lift_is_technical` | [tests/c1prime/test_a_chart_exceptions.py:103](../../tests/c1prime/test_a_chart_exceptions.py#L103) |  |
| `test_same_pair_count_hand_array_and_inconclusive` | test | `test_same_pair_count_hand_array_and_inconclusive` | [tests/analysis/test_geometry.py:55](../../tests/analysis/test_geometry.py#L55) |  |
| `test_same_pairs_199_inconclusive_and_200_ok` | test | `test_same_pairs_199_inconclusive_and_200_ok` | [tests/analysis/test_geometry.py:69](../../tests/analysis/test_geometry.py#L69) |  |
| `test_same_pairs_below_200_inconclusive` | test | `test_same_pairs_below_200_inconclusive` | [tests/analysis/test_geometry.py:62](../../tests/analysis/test_geometry.py#L62) |  |
| `test_sample_block_is_one_fixed_4096_row_stream_with_w33_dropped` | test | `test_sample_block_is_one_fixed_4096_row_stream_with_w33_dropped` | [tests/c1prime/test_b_registry.py:80](../../tests/c1prime/test_b_registry.py#L80) |  |
| `test_sample_block_is_one_sampler_call_sorted_by_id` | test | `test_sample_block_is_one_sampler_call_sorted_by_id` | [tests/k4b/test_b_data.py:135](../../tests/k4b/test_b_data.py#L135) |  |
| `test_sample_block_one_call_contiguous_uint8_without_w33` | test | `test_sample_block_one_call_contiguous_uint8_without_w33` | [tests/hwsb/test_b_streams.py:191](../../tests/hwsb/test_b_streams.py#L191) |  |
| `test_sample_calls_the_sampler_once_and_drops_the_last_symbol` | test | `test_sample_calls_the_sampler_once_and_drops_the_last_symbol` | [tests/hws/test_b_oracle.py:102](../../tests/hws/test_b_oracle.py#L102) |  |
| `test_sample_named_is_perm_of_canonical` | test | `test_sample_named_is_perm_of_canonical` | [tests/experiment/test_x5g1_lineage.py:95](../../tests/experiment/test_x5g1_lineage.py#L95) |  |
| `test_sample_named_one_call_deterministic` | test | `test_sample_named_one_call_deterministic` | [tests/experiment/test_x5g1_lineage.py:114](../../tests/experiment/test_x5g1_lineage.py#L114) |  |
| `test_sample_named_shape_dtype_and_no_states` | test | `test_sample_named_shape_dtype_and_no_states` | [tests/experiment/test_x5g1_lineage.py:107](../../tests/experiment/test_x5g1_lineage.py#L107) |  |
| `test_sample_observations_equals_dataset_stage_bitwise` | test | `test_sample_observations_equals_dataset_stage_bitwise` | [tests/hwsb/test_b_streams.py:154](../../tests/hwsb/test_b_streams.py#L154) |  |
| `test_sample_observations_one_call_named_tokens` | test | `test_sample_observations_one_call_named_tokens` | [tests/hwsb/test_b_streams.py:199](../../tests/hwsb/test_b_streams.py#L199) |  |
| `test_sample_pool_is_deterministic_and_returns_no_states` | test | `test_sample_pool_is_deterministic_and_returns_no_states` | [tests/experiment/test_x4b2.py:42](../../tests/experiment/test_x4b2.py#L42) |  |
| `test_sample_pool_returns_tokens_only_and_matches_sampler` | test | `test_sample_pool_returns_tokens_only_and_matches_sampler` | [tests/x6_stage1/test_b_seed_pool_reg.py:174](../../tests/x6_stage1/test_b_seed_pool_reg.py#L174) |  |
| `test_sample_segment_equals_independent_backward_sampler` | test | `test_sample_segment_equals_independent_backward_sampler` | [tests/x6_stage1/test_a_pairs.py:194](../../tests/x6_stage1/test_a_pairs.py#L194) |  |
| `test_sampler_cdf_matches_frozen_cumulative_rows` | test | `test_sampler_cdf_matches_frozen_cumulative_rows` | [tests/circle_history/test_process_law.py:79](../../tests/circle_history/test_process_law.py#L79) |  |
| `test_sampler_defects_fail_technical` | test | `test_sampler_defects_fail_technical` | [tests/hwsb/test_b_streams.py:228](../../tests/hwsb/test_b_streams.py#L228) |  |
| `test_sampler_law_exhaustively_uniform_n_le_6` | test | `test_sampler_law_exhaustively_uniform_n_le_6` | [tests/x6_stage1/test_a_pairs.py:172](../../tests/x6_stage1/test_a_pairs.py#L172) |  |
| `test_sampler_never_draws_zero_probability_symbols` | test | `test_sampler_never_draws_zero_probability_symbols` | [tests/dataset/test_sampler.py:54](../../tests/dataset/test_sampler.py#L54) |  |
| `test_save_and_load_pool` | test | `test_save_and_load_pool` | [tests/x6_stage1/test_b_seed_pool_reg.py:191](../../tests/x6_stage1/test_b_seed_pool_reg.py#L191) |  |
| `test_save_hist_paths_key_and_exclusive_create` | test | `test_save_hist_paths_key_and_exclusive_create` | [tests/hws/test_b_records.py:104](../../tests/hws/test_b_records.py#L104) |  |
| `test_saved_ids_must_match_reloaded_rows` | test | `test_saved_ids_must_match_reloaded_rows` | [tests/circle_history/test_builder_v24_stages.py:136](../../tests/circle_history/test_builder_v24_stages.py#L136) |  |
| `test_scale_s_is_q95_of_positive_distances` | test | `test_scale_s_is_q95_of_positive_distances` | [tests/topology/test_persistence.py:93](../../tests/topology/test_persistence.py#L93) |  |
| `test_scale_statistics_use_the_cstar_submatrix_only` | test | `test_scale_statistics_use_the_cstar_submatrix_only` | [tests/c1prime/test_a_chart_lcc512.py:168](../../tests/c1prime/test_a_chart_lcc512.py#L168) | Item 6: d8, sigma and support_radius from _neighbor_scale(D[np.ix_(C*, C*)]). |
| `test_sched_rule2_and_rule3` | test | `test_sched_rule2_and_rule3` | [tests/hwsb/test_b_records.py:127](../../tests/hwsb/test_b_records.py#L127) |  |
| `test_scientific_outcome` | test | `test_scientific_outcome` | [tests/x2a_stage0/test_x2a_stage0_ph.py:149](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L149) |  |
| `test_scope_and_history_streams` | test | `test_scope_and_history_streams` | [tests/c2_readout/test_b_policy.py:287](../../tests/c2_readout/test_b_policy.py#L287) |  |
| `test_score_e_row_check_against_80_digit_decimal` | test | `test_score_e_row_check_against_80_digit_decimal` | [tests/x6_stage1/test_a_numerics.py:112](../../tests/x6_stage1/test_a_numerics.py#L112) | §7.4 item 3 / T15: \|x_hat - X\| <= 1e-13 with X recomputed in 80-digit Decimal. |
| `test_scoring_authority_constructed_only_in_release_and_errors` | test | `test_scoring_authority_constructed_only_in_release_and_errors` | [tests/circle_history/test_builder_guards.py:149](../../tests/circle_history/test_builder_guards.py#L149) |  |
| `test_scoring_authority_requires_strict_true_and_owner_record` | test | `test_scoring_authority_requires_strict_true_and_owner_record` | [tests/circle_history/test_builder_guards.py:127](../../tests/circle_history/test_builder_guards.py#L127) |  |
| `test_scoring_authority_unlocks_panel_3` | test | `test_scoring_authority_unlocks_panel_3` | [tests/circle_history/test_adapter.py:243](../../tests/circle_history/test_adapter.py#L243) |  |
| `test_scoring_authority_unlocks_scoring` | test | `test_scoring_authority_unlocks_scoring` | [tests/circle_history/test_error_bound.py:390](../../tests/circle_history/test_error_bound.py#L390) |  |
| `test_scoring_guard_is_a_real_boundary` | test | `test_scoring_guard_is_a_real_boundary` | [tests/experiment/test_x5g1t_integration.py:324](../../tests/experiment/test_x5g1t_integration.py#L324) | A STOP that appears at 'score batch 1' stops dev-analysis with no result export. |
| `test_scoring_lock_precedes_any_computation` | test | `test_scoring_lock_precedes_any_computation` | [tests/circle_history/test_error_bound.py:374](../../tests/circle_history/test_error_bound.py#L374) |  |
| `test_screen_bounds_formulas` | test | `test_screen_bounds_formulas` | [tests/hws/test_a_stats.py:98](../../tests/hws/test_a_stats.py#L98) |  |
| `test_screen_pool_and_pair_d2` | test | `test_screen_pool_and_pair_d2` | [tests/analysis/test_horizon.py:151](../../tests/analysis/test_horizon.py#L151) |  |
| `test_screening_rates` | test | `test_screening_rates` | [tests/hws/test_a_budget.py:38](../../tests/hws/test_a_budget.py#L38) |  |
| `test_sd_b4_draws_reproduce_manual_loop_with_shared_idx` | test | `test_sd_b4_draws_reproduce_manual_loop_with_shared_idx` | [tests/circle_history/test_scores_precision_gates.py:103](../../tests/circle_history/test_scores_precision_gates.py#L103) |  |
| `test_sealed_d2a_predicate` | test | `test_sealed_d2a_predicate` | [tests/k4b/test_b_data.py:335](../../tests/k4b/test_b_data.py#L335) |  |
| `test_sealed_d2a_predicate_hit_is_incomplete` | test | `test_sealed_d2a_predicate_hit_is_incomplete` | [tests/c2_readout/test_b_registry.py:192](../../tests/c2_readout/test_b_registry.py#L192) |  |
| `test_sealed_keys_are_the_registered_tuple` | test | `test_sealed_keys_are_the_registered_tuple` | [tests/k4b/test_b_flow.py:41](../../tests/k4b/test_b_flow.py#L41) |  |
| `test_second_attempt_refused_even_without_completion` | test | `test_second_attempt_refused_even_without_completion` | [tests/circle_history/test_builder_v24_stages.py:51](../../tests/circle_history/test_builder_v24_stages.py#L51) |  |
| `test_second_candidate_chosen_even_if_third_better` | test | `test_second_candidate_chosen_even_if_third_better` | [tests/analysis/test_sigma_calibrator.py:64](../../tests/analysis/test_sigma_calibrator.py#L64) |  |
| `test_second_start_refused_after_complete` | test | `test_second_start_refused_after_complete` | [tests/experiment/test_x5g1t_training.py:269](../../tests/experiment/test_x5g1t_training.py#L269) |  |
| `test_second_start_refused_after_incomplete` | test | `test_second_start_refused_after_incomplete` | [tests/experiment/test_x5g1t_training.py:280](../../tests/experiment/test_x5g1t_training.py#L280) |  |
| `test_secondary_reading_keeps_its_status` | test | `test_secondary_reading_keeps_its_status` | [tests/hwsb/test_r_0170_kb2_status.py:57](../../tests/hwsb/test_r_0170_kb2_status.py#L57) |  |
| `test_seed_flags_and_designed_counts` | test | `test_seed_flags_and_designed_counts` | [tests/x6_stage1/test_a_rules.py:161](../../tests/x6_stage1/test_a_rules.py#L161) |  |
| `test_seed_fresh_compares_values_recursively` | test | `test_seed_fresh_compares_values_recursively` | [tests/x6_stage1/test_b_seed_pool_reg.py:64](../../tests/x6_stage1/test_b_seed_pool_reg.py#L64) |  |
| `test_seed_map_620501_to_620518` | test | `test_seed_map_620501_to_620518` | [tests/c2_readout/test_b_policy.py:330](../../tests/c2_readout/test_b_policy.py#L330) |  |
| `test_seed_search_skips_and_never_opens_excluded_paths` | test | `test_seed_search_skips_and_never_opens_excluded_paths` | [tests/hws/test_b_kc1.py:294](../../tests/hws/test_b_kc1.py#L294) |  |
| `test_seed_search_whole_token_rule_and_excluded_folders` | test | `test_seed_search_whole_token_rule_and_excluded_folders` | [tests/hwsb/test_b_records.py:258](../../tests/hwsb/test_b_records.py#L258) |  |
| `test_segment_parse_and_r_ord` | test | `test_segment_parse_and_r_ord` | [tests/x6_stage1/test_a_pairs.py:208](../../tests/x6_stage1/test_a_pairs.py#L208) |  |
| `test_select_anchors_is_deterministic_and_order_free` | test | `test_select_anchors_is_deterministic_and_order_free` | [tests/analysis/test_horizon.py:128](../../tests/analysis/test_horizon.py#L128) |  |
| `test_select_h1_bar` | test | `test_select_h1_bar` | [tests/circle_history/test_chart.py:136](../../tests/circle_history/test_chart.py#L136) |  |
| `test_select_h1_bar_none` | test | `test_select_h1_bar_none` | [tests/circle_history/test_chart.py:143](../../tests/circle_history/test_chart.py#L143) |  |
| `test_selected_first_ordinary_qualifier_in_finalist_order` | test | `test_selected_first_ordinary_qualifier_in_finalist_order` | [tests/hws/test_a_outcomes.py:122](../../tests/hws/test_a_outcomes.py#L122) |  |
| `test_selection_and_fold_mse_match_reference` | test | `test_selection_and_fold_mse_match_reference` | [tests/experiment/test_x4f_probe.py:66](../../tests/experiment/test_x4f_probe.py#L66) |  |
| `test_sentinel_stop_keeps_in_memory_checkpoints` | test | `test_sentinel_stop_keeps_in_memory_checkpoints` | [tests/hwsb/test_b_e4path.py:138](../../tests/hwsb/test_b_e4path.py#L138) |  |
| `test_separation_cal_val_every_collision_is_lineage` | test | `test_separation_cal_val_every_collision_is_lineage` | [tests/k4b/test_b_data.py:258](../../tests/k4b/test_b_data.py#L258) |  |
| `test_separation_clean_tables_pass` | test | `test_separation_clean_tables_pass` | [tests/hwsb/test_b_streams.py:347](../../tests/hwsb/test_b_streams.py#L347) |  |
| `test_separation_collision_is_lineage` | test | `test_separation_collision_is_lineage` | [tests/x6_stage1/test_b_seed_pool_reg.py:247](../../tests/x6_stage1/test_b_seed_pool_reg.py#L247) |  |
| `test_separation_collision_is_lineage_failure` | test | `test_separation_collision_is_lineage_failure` | [tests/c1prime/test_b_registry.py:146](../../tests/c1prime/test_b_registry.py#L146) |  |
| `test_separation_eval_eval_collision_fails_lineage` | test | `test_separation_eval_eval_collision_fails_lineage` | [tests/hwsb/test_b_streams.py:364](../../tests/hwsb/test_b_streams.py#L364) |  |
| `test_separation_eval_train_collision_fails_lineage` | test | `test_separation_eval_train_collision_fails_lineage` | [tests/hwsb/test_b_streams.py:355](../../tests/hwsb/test_b_streams.py#L355) |  |
| `test_separation_fresh_collision_is_lineage` | test | `test_separation_fresh_collision_is_lineage` | [tests/k4b/test_b_data.py:275](../../tests/k4b/test_b_data.py#L275) |  |
| `test_separation_id_overlap_fails_lineage` | test | `test_separation_id_overlap_fails_lineage` | [tests/hwsb/test_b_streams.py:372](../../tests/hwsb/test_b_streams.py#L372) |  |
| `test_separation_pass_with_duplicates_kept` | test | `test_separation_pass_with_duplicates_kept` | [tests/c2_readout/test_b_registry.py:144](../../tests/c2_readout/test_b_registry.py#L144) |  |
| `test_separation_passes_when_all_three_intersections_are_empty` | test | `test_separation_passes_when_all_three_intersections_are_empty` | [tests/c1prime/test_b_registry.py:139](../../tests/c1prime/test_b_registry.py#L139) |  |
| `test_seq_disjoint_frozen_union_hit_is_lineage` | test | `test_seq_disjoint_frozen_union_hit_is_lineage` | [tests/k4b/test_b_data.py:300](../../tests/k4b/test_b_data.py#L300) |  |
| `test_seq_disjoint_overlap_between_blocks_is_lineage` | test | `test_seq_disjoint_overlap_between_blocks_is_lineage` | [tests/k4b/test_b_data.py:292](../../tests/k4b/test_b_data.py#L292) |  |
| `test_seq_disjoint_pass` | test | `test_seq_disjoint_pass` | [tests/k4b/test_b_data.py:287](../../tests/k4b/test_b_data.py#L287) |  |
| `test_seq_disjoint_ranges_are_half_open` | test | `test_seq_disjoint_ranges_are_half_open` | [tests/k4b/test_b_data.py:308](../../tests/k4b/test_b_data.py#L308) |  |
| `test_sequence_id_codes` | test | `test_sequence_id_codes` | [tests/c2_readout/test_b_policy.py:314](../../tests/c2_readout/test_b_policy.py#L314) |  |
| `test_sequence_id_rule_known_answer` | test | `test_sequence_id_rule_known_answer` | [tests/dataset/test_stage.py:117](../../tests/dataset/test_stage.py#L117) |  |
| `test_sequence_ids_disjoint_across_k4b_blocks` | test | `test_sequence_ids_disjoint_across_k4b_blocks` | [tests/k4b/test_b_data.py:124](../../tests/k4b/test_b_data.py#L124) |  |
| `test_sequence_ids_exact_and_disjoint_across_all_pools` | test | `test_sequence_ids_exact_and_disjoint_across_all_pools` | [tests/x6_stage1/test_b_seed_pool_reg.py:163](../../tests/x6_stage1/test_b_seed_pool_reg.py#L163) |  |
| `test_sequence_ids_follow_contract_replicates` | test | `test_sequence_ids_follow_contract_replicates` | [tests/hwsb/test_b_streams.py:104](../../tests/hwsb/test_b_streams.py#L104) |  |
| `test_sequence_ids_follow_the_registered_rule` | test | `test_sequence_ids_follow_the_registered_rule` | [tests/k4b/test_b_data.py:117](../../tests/k4b/test_b_data.py#L117) |  |
| `test_sequence_ids_formula_and_bits` | test | `test_sequence_ids_formula_and_bits` | [tests/experiment/test_x5g1t_lineage_oracle.py:75](../../tests/experiment/test_x5g1t_lineage_oracle.py#L75) |  |
| `test_sequence_ids_frozen_namespace_and_disjoint` | test | `test_sequence_ids_frozen_namespace_and_disjoint` | [tests/experiment/test_x4b2.py:30](../../tests/experiment/test_x4b2.py#L30) |  |
| `test_sequence_ids_invalid` | test | `test_sequence_ids_invalid` | [tests/experiment/test_x5g1t_lineage_oracle.py:89](../../tests/experiment/test_x5g1t_lineage_oracle.py#L89) |  |
| `test_sequence_ids_namespace_and_disjoint` | test | `test_sequence_ids_namespace_and_disjoint` | [tests/experiment/test_x5g1_lineage.py:121](../../tests/experiment/test_x5g1_lineage.py#L121) |  |
| `test_sequence_ids_refusals` | test | `test_sequence_ids_refusals` | [tests/hwsb/test_b_streams.py:99](../../tests/hwsb/test_b_streams.py#L99) |  |
| `test_sequence_ids_unknown_arm` | test | `test_sequence_ids_unknown_arm` | [tests/experiment/test_x5g1_lineage.py:132](../../tests/experiment/test_x5g1_lineage.py#L132) |  |
| `test_serialise_roles_and_identity_carrier` | test | `test_serialise_roles_and_identity_carrier` | [tests/c1prime/test_a_chart_lcc512.py:226](../../tests/c1prime/test_a_chart_lcc512.py#L226) |  |
| `test_session_and_weekly_both_latched_then_partial_clear_holds` | test | `test_session_and_weekly_both_latched_then_partial_clear_holds` | [tests/experiment/test_x5g1t_usage.py:390](../../tests/experiment/test_x5g1t_usage.py#L390) |  |
| `test_set_threads_records_values` | test | `test_set_threads_records_values` | [tests/hwsb/test_b_e4path.py:248](../../tests/hwsb/test_b_e4path.py#L248) |  |
| `test_several_mismatches_are_all_reported_in_checked_order` | test | `test_several_mismatches_are_all_reported_in_checked_order` | [tests/k4b/test_b_h1_meta.py:248](../../tests/k4b/test_b_h1_meta.py#L248) |  |
| `test_sha256_phase_hand_derived_from_hashlib` | test | `test_sha256_phase_hand_derived_from_hashlib` | [tests/circle_history/test_scores_precision.py:269](../../tests/circle_history/test_scores_precision.py#L269) |  |
| `test_shape_generators_contract` | test | `test_shape_generators_contract` | [tests/topology/test_shapes_calibration.py:25](../../tests/topology/test_shapes_calibration.py#L25) |  |
| `test_shared_index_stream_resp_spec_first_then_endpoint` | test | `test_shared_index_stream_resp_spec_first_then_endpoint` | [tests/c2_readout/test_a_inference.py:348](../../tests/c2_readout/test_a_inference.py#L348) |  |
| `test_sharp_target_statuses_at_exact_edges` | test | `test_sharp_target_statuses_at_exact_edges` | [tests/x6_stage1/test_a_rules.py:52](../../tests/x6_stage1/test_a_rules.py#L52) |  |
| `test_sharpness_extremal_completions` | test | `test_sharpness_extremal_completions` | [tests/k4b/test_a_theorem_a.py:168](../../tests/k4b/test_a_theorem_a.py#L168) |  |
| `test_shuffle_perm_depends_on_scope` | test | `test_shuffle_perm_depends_on_scope` | [tests/d2a/test_b_behaviour.py:144](../../tests/d2a/test_b_behaviour.py#L144) |  |
| `test_shuffle_perm_is_deterministic_and_a_permutation` | test | `test_shuffle_perm_is_deterministic_and_a_permutation` | [tests/d2a/test_b_behaviour.py:136](../../tests/d2a/test_b_behaviour.py#L136) |  |
| `test_shuffle_perm_is_the_registered_stream` | test | `test_shuffle_perm_is_the_registered_stream` | [tests/d2a/test_b_behaviour.py:131](../../tests/d2a/test_b_behaviour.py#L131) |  |
| `test_shuffle_stop_inside_refits` | test | `test_shuffle_stop_inside_refits` | [tests/experiment/test_x4f_maintenance.py:77](../../tests/experiment/test_x4f_maintenance.py#L77) |  |
| `test_sigma_5_4_delta_zero_and_identical_to_old_enclosure` | test | `test_sigma_5_4_delta_zero_and_identical_to_old_enclosure` | [tests/hwsb/test_a_enclosure_proof.py:174](../../tests/hwsb/test_a_enclosure_proof.py#L174) |  |
| `test_sigma_7_4_e_dec_computed_from_q_tilde` | test | `test_sigma_7_4_e_dec_computed_from_q_tilde` | [tests/hwsb/test_a_enclosure_proof.py:226](../../tests/hwsb/test_a_enclosure_proof.py#L226) | Step (1): the existing analysis applies to the exact inputs q~ (process_law.py:117-124). |
| `test_sigma_7_4_rounded_logits_are_q_tilde` | test | `test_sigma_7_4_rounded_logits_are_q_tilde` | [tests/hwsb/test_a_enclosure_proof.py:208](../../tests/hwsb/test_a_enclosure_proof.py#L208) |  |
| `test_sigma_7_4_rounding_delta` | test | `test_sigma_7_4_rounding_delta` | [tests/hwsb/test_a_enclosure_proof.py:194](../../tests/hwsb/test_a_enclosure_proof.py#L194) |  |
| `test_sigma_7_4_widened_lo_hi` | test | `test_sigma_7_4_widened_lo_hi` | [tests/hwsb/test_a_enclosure_proof.py:216](../../tests/hwsb/test_a_enclosure_proof.py#L216) |  |
| `test_sign_convention_largest_abs_entry_positive_and_stable_under_negation` | test | `test_sign_convention_largest_abs_entry_positive_and_stable_under_negation` | [tests/analysis/test_x4f_targets.py:117](../../tests/analysis/test_x4f_targets.py#L117) |  |
| `test_single_field_value_mismatch_is_identity` | test | `test_single_field_value_mismatch_is_identity` | [tests/k4b/test_b_h1_meta.py:179](../../tests/k4b/test_b_h1_meta.py#L179) |  |
| `test_single_out_of_vocab_token` | test | `test_single_out_of_vocab_token` | [tests/learner/test_patch.py:282](../../tests/learner/test_patch.py#L282) |  |
| `test_single_triangle_centred_modular_cocycle_is_lifted` | test | `test_single_triangle_centred_modular_cocycle_is_lifted` | [tests/circle_history/test_cochain_lift.py:180](../../tests/circle_history/test_cochain_lift.py#L180) |  |
| `test_six_constructions_then_refusal` | test | `test_six_constructions_then_refusal` | [tests/c1prime/test_a_chart_val.py:191](../../tests/c1prime/test_a_chart_val.py#L191) |  |
| `test_skipping_zero_transition_entries_is_bitwise_neutral` | test | `test_skipping_zero_transition_entries_is_bitwise_neutral` | [tests/c1prime/test_b_cert_oracle.py:165](../../tests/c1prime/test_b_cert_oracle.py#L165) |  |
| `test_smallest_valid_forward_product_does_not_trap` | test | `test_smallest_valid_forward_product_does_not_trap` | [tests/circle_history/test_error_bound.py:140](../../tests/circle_history/test_error_bound.py#L140) | Exponent reasoning of section 2: 64 factors of 2^-1074 stay far above 10^Emin. |
| `test_smooth_phase_cycle_five_winding_two` | test | `test_smooth_phase_cycle_five_winding_two` | [tests/circle_history/test_cochain.py:250](../../tests/circle_history/test_cochain.py#L250) |  |
| `test_smooth_phase_cycle_four` | test | `test_smooth_phase_cycle_four` | [tests/circle_history/test_cochain.py:240](../../tests/circle_history/test_cochain.py#L240) |  |
| `test_smooth_phase_path_is_exact` | test | `test_smooth_phase_path_is_exact` | [tests/circle_history/test_cochain.py:257](../../tests/circle_history/test_cochain.py#L257) |  |
| `test_smoothing_style_invalid_without_a_smooth_phase_frame_is_technical` | test | `test_smoothing_style_invalid_without_a_smooth_phase_frame_is_technical` | [tests/c1prime/test_a_chart_exceptions.py:176](../../tests/c1prime/test_a_chart_exceptions.py#L176) |  |
| `test_snr_fixture_registered_comparator_passes_where_raw_gls_fails` | test | `test_snr_fixture_registered_comparator_passes_where_raw_gls_fails` | [tests/c2_readout/test_b_fwl_l1.py:231](../../tests/c2_readout/test_b_fwl_l1.py#L231) |  |
| `test_softmax64_bitwise_s3_formula` | test | `test_softmax64_bitwise_s3_formula` | [tests/hwsb/test_a_learning.py:155](../../tests/hwsb/test_a_learning.py#L155) |  |
| `test_softmax_enclosure_contains_80_digit_values` | test | `test_softmax_enclosure_contains_80_digit_values` | [tests/circle_history/test_process_law.py:189](../../tests/circle_history/test_process_law.py#L189) |  |
| `test_source_a_explicit_store_reads_that_root` | test | `test_source_a_explicit_store_reads_that_root` | [tests/k4b/test_b_registry.py:277](../../tests/k4b/test_b_registry.py#L277) |  |
| `test_source_a_non_default_root_without_store_refused` | test | `test_source_a_non_default_root_without_store_refused` | [tests/k4b/test_b_registry.py:265](../../tests/k4b/test_b_registry.py#L265) |  |
| `test_source_c_malformed_json_refused_never_empty` | test | `test_source_c_malformed_json_refused_never_empty` | [tests/k4b/test_b_registry.py:234](../../tests/k4b/test_b_registry.py#L234) |  |
| `test_source_c_valid_mailbox_delegates_unchanged` | test | `test_source_c_valid_mailbox_delegates_unchanged` | [tests/k4b/test_b_registry.py:241](../../tests/k4b/test_b_registry.py#L241) |  |
| `test_source_d_reads_digest_list_and_columns_incl_superseded` | test | `test_source_d_reads_digest_list_and_columns_incl_superseded` | [tests/k4b/test_b_registry.py:133](../../tests/k4b/test_b_registry.py#L133) |  |
| `test_source_d_refuses_unbound_registry_v1` | test | `test_source_d_refuses_unbound_registry_v1` | [tests/k4b/test_b_registry.py:145](../../tests/k4b/test_b_registry.py#L145) |  |
| `test_source_e_never_opens_sealed_token_arrays` | test | `test_source_e_never_opens_sealed_token_arrays` | [tests/k4b/test_b_registry.py:170](../../tests/k4b/test_b_registry.py#L170) |  |
| `test_source_e_unresolved_pool_inventory_is_incomplete` | test | `test_source_e_unresolved_pool_inventory_is_incomplete` | [tests/k4b/test_b_registry.py:206](../../tests/k4b/test_b_registry.py#L206) |  |
| `test_source_head_mismatch_is_refused` | test | `test_source_head_mismatch_is_refused` | [tests/c1prime/test_a_release_meter.py:158](../../tests/c1prime/test_a_release_meter.py#L158) |  |
| `test_spectral_embedding_shape_and_r2_r3_definitions` | test | `test_spectral_embedding_shape_and_r2_r3_definitions` | [tests/analysis/test_baselines_dynamics.py:52](../../tests/analysis/test_baselines_dynamics.py#L52) |  |
| `test_spectrum_abs_gap_uses_negative_eigenvalue` | test | `test_spectrum_abs_gap_uses_negative_eigenvalue` | [tests/analysis/test_x5_kernel.py:90](../../tests/analysis/test_x5_kernel.py#L90) |  |
| `test_spectrum_eigenvalues_descending_lazy_cycle` | test | `test_spectrum_eigenvalues_descending_lazy_cycle` | [tests/analysis/test_x5_kernel.py:99](../../tests/analysis/test_x5_kernel.py#L99) |  |
| `test_spectrum_near_unit_gap_status` | test | `test_spectrum_near_unit_gap_status` | [tests/analysis/test_x5_kernel.py:133](../../tests/analysis/test_x5_kernel.py#L133) |  |
| `test_spectrum_reducible_status` | test | `test_spectrum_reducible_status` | [tests/analysis/test_x5_kernel.py:127](../../tests/analysis/test_x5_kernel.py#L127) |  |
| `test_spectrum_two_state_hand_values` | test | `test_spectrum_two_state_hand_values` | [tests/analysis/test_x5_kernel.py:79](../../tests/analysis/test_x5_kernel.py#L79) |  |
| `test_split_check` | test | `test_split_check` | [tests/x2a_stage0/test_x2a_stage0_ph.py:263](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L263) |  |
| `test_split_overlap_and_range_errors` | test | `test_split_overlap_and_range_errors` | [tests/dataset/test_stage.py:105](../../tests/dataset/test_stage.py#L105) |  |
| `test_split_overlap_maps_to_lineage` | test | `test_split_overlap_maps_to_lineage` | [tests/k4b/test_b_flow.py:186](../../tests/k4b/test_b_flow.py#L186) |  |
| `test_split_seeds_are_inconclusive` | test | `test_split_seeds_are_inconclusive` | [tests/d2a/test_b_rules_decide.py:294](../../tests/d2a/test_b_rules_decide.py#L294) |  |
| `test_sqrt_js_hand_values` | test | `test_sqrt_js_hand_values` | [tests/topology/test_metrics.py:54](../../tests/topology/test_metrics.py#L54) |  |
| `test_stage0_constants_exact_string_equality` | test | `test_stage0_constants_exact_string_equality` | [tests/x6_stage1/test_b_nb_s0_ops.py:248](../../tests/x6_stage1/test_b_nb_s0_ops.py#L248) |  |
| `test_stage0_regeneration_count_check` | test | `test_stage0_regeneration_count_check` | [tests/x6_stage1/test_b_seed_pool_reg.py:212](../../tests/x6_stage1/test_b_seed_pool_reg.py#L212) |  |
| `test_stage0_thresholds_are_exact_rationals` | test | `test_stage0_thresholds_are_exact_rationals` | [tests/x6_stage1/test_a_rules.py:41](../../tests/x6_stage1/test_a_rules.py#L41) |  |
| `test_stage1_decision_all_branches` | test | `test_stage1_decision_all_branches` | [tests/d2a/test_b_rules_flags.py:94](../../tests/d2a/test_b_rules_flags.py#L94) |  |
| `test_stage1_named_branches` | test | `test_stage1_named_branches` | [tests/d2a/test_b_rules_flags.py:98](../../tests/d2a/test_b_rules_flags.py#L98) |  |
| `test_stage_and_total_spent_on_a_synthetic_ledger` | test | `test_stage_and_total_spent_on_a_synthetic_ledger` | [tests/d2a/test_b_resource.py:280](../../tests/d2a/test_b_resource.py#L280) |  |
| `test_stage_gates_and_required_pass_sets` | test | `test_stage_gates_and_required_pass_sets` | [tests/c1prime/test_a_gates.py:66](../../tests/c1prime/test_a_gates.py#L66) |  |
| `test_stage_history_tables_are_sources_with_sha256` | test | `test_stage_history_tables_are_sources_with_sha256` | [tests/k4b/test_b_store_reader.py:160](../../tests/k4b/test_b_store_reader.py#L160) |  |
| `test_stage_label_and_ceiling` | test | `test_stage_label_and_ceiling` | [tests/circle_history/test_builder_runtime.py:63](../../tests/circle_history/test_builder_runtime.py#L63) |  |
| `test_stage_limiter_delegates_to_unchanged_global_limiter` | test | `test_stage_limiter_delegates_to_unchanged_global_limiter` | [tests/circle_history/test_builder_guards.py:51](../../tests/circle_history/test_builder_guards.py#L51) |  |
| `test_stage_limiter_grows_with_supervisor_cpu` | test | `test_stage_limiter_grows_with_supervisor_cpu` | [tests/circle_history/test_builder_guards.py:41](../../tests/circle_history/test_builder_guards.py#L41) |  |
| `test_stage_limiter_includes_supervisor_and_tail` | test | `test_stage_limiter_includes_supervisor_and_tail` | [tests/circle_history/test_builder_guards.py:30](../../tests/circle_history/test_builder_guards.py#L30) |  |
| `test_stage_reads_observations_only_with_learner_policy` | test | `test_stage_reads_observations_only_with_learner_policy` | [tests/learner/test_checkpoint.py:82](../../tests/learner/test_checkpoint.py#L82) |  |
| `test_stage_round_trip_and_lineage` | test | `test_stage_round_trip_and_lineage` | [tests/process/test_controls.py:156](../../tests/process/test_controls.py#L156) |  |
| `test_stage_saves_expected_lineage_and_split_labels` | test | `test_stage_saves_expected_lineage_and_split_labels` | [tests/dataset/test_stage.py:59](../../tests/dataset/test_stage.py#L59) |  |
| `test_stage_unknown_mode` | test | `test_stage_unknown_mode` | [tests/process/test_controls.py:180](../../tests/process/test_controls.py#L180) |  |
| `test_standardise_nuisance_population_sd_and_constant_columns` | test | `test_standardise_nuisance_population_sd_and_constant_columns` | [tests/c1prime/test_b_fwl.py:118](../../tests/c1prime/test_b_fwl.py#L118) |  |
| `test_standardizer_population_std_and_zero_floor` | test | `test_standardizer_population_std_and_zero_floor` | [tests/analysis/test_x4f_scores.py:53](../../tests/analysis/test_x4f_scores.py#L53) |  |
| `test_star_arrays_sha256_equal_selection` | test | `test_star_arrays_sha256_equal_selection` | [tests/hwsb/test_b_process.py:80](../../tests/hwsb/test_b_process.py#L80) |  |
| `test_star_canonical_symbol_is_axial_cell_centre` | test | `test_star_canonical_symbol_is_axial_cell_centre` | [tests/hwsb/test_b_process.py:104](../../tests/hwsb/test_b_process.py#L104) |  |
| `test_star_e_canon_is_shared_and_named_inverts` | test | `test_star_e_canon_is_shared_and_named_inverts` | [tests/hwsb/test_b_process.py:90](../../tests/hwsb/test_b_process.py#L90) |  |
| `test_star_ids_match_contract` | test | `test_star_ids_match_contract` | [tests/hwsb/test_b_process.py:52](../../tests/hwsb/test_b_process.py#L52) |  |
| `test_star_shapes_and_constants` | test | `test_star_shapes_and_constants` | [tests/hwsb/test_b_process.py:59](../../tests/hwsb/test_b_process.py#L59) |  |
| `test_star_spec_checksums_match_contract` | test | `test_star_spec_checksums_match_contract` | [tests/hwsb/test_b_process.py:70](../../tests/hwsb/test_b_process.py#L70) |  |
| `test_start_law_artefact_and_decision_phase_mass` | test | `test_start_law_artefact_and_decision_phase_mass` | [tests/d1_seam/test_d1_seam.py:327](../../tests/d1_seam/test_d1_seam.py#L327) |  |
| `test_state_maps` | test | `test_state_maps` | [tests/hws/test_b_worlds.py:304](../../tests/hws/test_b_worlds.py#L304) |  |
| `test_state_sha_chart_and_freeze_hashes_equal_the_contract` | test | `test_state_sha_chart_and_freeze_hashes_equal_the_contract` | [tests/c2_readout/test_b_lineage.py:117](../../tests/c2_readout/test_b_lineage.py#L117) |  |
| `test_static_scored_access_audit` | test | `test_static_scored_access_audit` | [tests/circle_history/test_builder_runtime.py:222](../../tests/circle_history/test_builder_runtime.py#L222) |  |
| `test_status_of_splits_full_strings` | test | `test_status_of_splits_full_strings` | [tests/c1prime/test_a_exceptions.py:202](../../tests/c1prime/test_a_exceptions.py#L202) |  |
| `test_status_table_and_exclusivity` | test | `test_status_table_and_exclusivity` | [tests/k4b/test_a_decision.py:162](../../tests/k4b/test_a_decision.py#L162) |  |
| `test_step2_ratio_bound_at_200_digits` | test | `test_step2_ratio_bound_at_200_digits` | [tests/hwsb/test_a_enclosure_proof.py:240](../../tests/hwsb/test_a_enclosure_proof.py#L240) |  |
| `test_step3_on_actual_delta` | test | `test_step3_on_actual_delta` | [tests/hwsb/test_a_enclosure_proof.py:255](../../tests/hwsb/test_a_enclosure_proof.py#L255) |  |
| `test_stop_and_hold_controls` | test | `test_stop_and_hold_controls` | [tests/experiment/test_x5g1t_e2e.py:72](../../tests/experiment/test_x5g1t_e2e.py#L72) |  |
| `test_stop_and_invalid_keep_precedence_over_overdue_and_disk` | test | `test_stop_and_invalid_keep_precedence_over_overdue_and_disk` | [tests/k4b/test_b_meter.py:190](../../tests/k4b/test_b_meter.py#L190) |  |
| `test_stop_at_a_hold_leaves_only_earlier_checkpoints` | test | `test_stop_at_a_hold_leaves_only_earlier_checkpoints` | [tests/hwsb/test_b_hold.py:184](../../tests/hwsb/test_b_hold.py#L184) |  |
| `test_stop_beats_everything` | test | `test_stop_beats_everything` | [tests/experiment/test_x5g1t_usage_files.py:227](../../tests/experiment/test_x5g1t_usage_files.py#L227) |  |
| `test_stop_beats_hold_from_any_source` | test | `test_stop_beats_hold_from_any_source` | [tests/experiment/test_x5g1t_runtime.py:150](../../tests/experiment/test_x5g1t_runtime.py#L150) |  |
| `test_stop_beats_invalid_and_hold` | test | `test_stop_beats_invalid_and_hold` | [tests/oracle_profile/test_builder_controls.py:71](../../tests/oracle_profile/test_builder_controls.py#L71) |  |
| `test_stop_before_data_is_inconclusive` | test | `test_stop_before_data_is_inconclusive` | [tests/experiment/test_x5g1_smoke.py:36](../../tests/experiment/test_x5g1_smoke.py#L36) |  |
| `test_stop_before_export_saves_nothing` | test | `test_stop_before_export_saves_nothing` | [tests/experiment/test_x5g1_export_integration.py:131](../../tests/experiment/test_x5g1_export_integration.py#L131) |  |
| `test_stop_before_first_write_leaves_store_empty` | test | `test_stop_before_first_write_leaves_store_empty` | [tests/experiment/test_x5g1t_training.py:184](../../tests/experiment/test_x5g1t_training.py#L184) |  |
| `test_stop_before_fresh_draw_never_draws` | test | `test_stop_before_fresh_draw_never_draws` | [tests/experiment/test_x5g1t_integration.py:254](../../tests/experiment/test_x5g1t_integration.py#L254) |  |
| `test_stop_before_hold_raises` | test | `test_stop_before_hold_raises` | [tests/experiment/test_x5g1t_runtime.py:228](../../tests/experiment/test_x5g1t_runtime.py#L228) |  |
| `test_stop_created_during_save_skips_remaining_steps` | test | `test_stop_created_during_save_skips_remaining_steps` | [tests/experiment/test_x5g1_export_integration.py:177](../../tests/experiment/test_x5g1_export_integration.py#L177) |  |
| `test_stop_during_collision_check_never_draws` | test | `test_stop_during_collision_check_never_draws` | [tests/experiment/test_x5g1t_integration.py:266](../../tests/experiment/test_x5g1t_integration.py#L266) | The STOP appears after the stage started, while the fresh IDs are being planned. |
| `test_stop_during_pools_export_writes_no_further_file` | test | `test_stop_during_pools_export_writes_no_further_file` | [tests/experiment/test_x5g1t_integration.py:167](../../tests/experiment/test_x5g1t_integration.py#L167) |  |
| `test_stop_ends_inconclusive` | test | `test_stop_ends_inconclusive` | [tests/hwsb/test_b_hold.py:124](../../tests/hwsb/test_b_hold.py#L124) |  |
| `test_stop_file_beats_worker_hold` | test | `test_stop_file_beats_worker_hold` | [tests/experiment/test_x5g1t_runtime.py:65](../../tests/experiment/test_x5g1t_runtime.py#L65) |  |
| `test_stop_file_is_stop_with_owner_reason` | test | `test_stop_file_is_stop_with_owner_reason` | [tests/experiment/test_x5g1t_runtime.py:58](../../tests/experiment/test_x5g1t_runtime.py#L58) |  |
| `test_stop_files` | test | `test_stop_files` | [tests/oracle_profile/test_builder_controls.py:57](../../tests/oracle_profile/test_builder_controls.py#L57) |  |
| `test_stop_h3_when_fallback_below_003` | test | `test_stop_h3_when_fallback_below_003` | [tests/analysis/test_sigma_calibrator.py:100](../../tests/analysis/test_sigma_calibrator.py#L100) |  |
| `test_stop_in_before_writes_no_artifact_for_that_step` | test | `test_stop_in_before_writes_no_artifact_for_that_step` | [tests/experiment/test_x5g1t_training.py:162](../../tests/experiment/test_x5g1t_training.py#L162) |  |
| `test_stop_precedes_any_source_load` | test | `test_stop_precedes_any_source_load` | [tests/experiment/test_x4f_maintenance.py:42](../../tests/experiment/test_x4f_maintenance.py#L42) |  |
| `test_stop_requested_mid_run` | test | `test_stop_requested_mid_run` | [tests/experiment/test_x5g1_controls.py:81](../../tests/experiment/test_x5g1_controls.py#L81) |  |
| `test_stop_while_held_raises` | test | `test_stop_while_held_raises` | [tests/experiment/test_x5g1t_runtime.py:298](../../tests/experiment/test_x5g1t_runtime.py#L298) |  |
| `test_store_file_hashes_bind_every_file_by_content` | test | `test_store_file_hashes_bind_every_file_by_content` | [tests/c1prime_registry/test_registry_builder.py:96](../../tests/c1prime_registry/test_registry_builder.py#L96) |  |
| `test_store_sources_record_every_listed_store_explicitly` | test | `test_store_sources_record_every_listed_store_explicitly` | [tests/c1prime_registry/test_registry_builder.py:85](../../tests/c1prime_registry/test_registry_builder.py#L85) |  |
| `test_stored_timing_is_read_from_a_record_of_the_same_checkpoints` | test | `test_stored_timing_is_read_from_a_record_of_the_same_checkpoints` | [tests/experiment/test_runner.py:133](../../tests/experiment/test_runner.py#L133) |  |
| `test_stratified_se_interval_and_hoeffding` | test | `test_stratified_se_interval_and_hoeffding` | [tests/x2a_stage0/test_x2a_stage0_ph.py:119](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L119) |  |
| `test_stray_file_is_other_and_not_clean` | test | `test_stray_file_is_other_and_not_clean` | [tests/k4b/test_b_store_reader.py:184](../../tests/k4b/test_b_store_reader.py#L184) |  |
| `test_stray_history_outside_the_os_root_is_incomplete` | test | `test_stray_history_outside_the_os_root_is_incomplete` | [tests/k4b/test_b_registry_rules.py:267](../../tests/k4b/test_b_registry_rules.py#L267) |  |
| `test_stream` | test | `test_stream` | [tests/experiment/test_x5g1t_lineage_oracle.py:60](../../tests/experiment/test_x5g1t_lineage_oracle.py#L60) |  |
| `test_stream_record_lists_the_scope` | test | `test_stream_record_lists_the_scope` | [tests/hwsb/test_b_streams.py:139](../../tests/hwsb/test_b_streams.py#L139) |  |
| `test_stream_refusals` | test | `test_stream_refusals` | [tests/hws/test_b_oracle.py:92](../../tests/hws/test_b_oracle.py#L92) |  |
| `test_stream_unknown_split` | test | `test_stream_unknown_split` | [tests/experiment/test_x5g1t_lineage_oracle.py:64](../../tests/experiment/test_x5g1t_lineage_oracle.py#L64) |  |
| `test_study_pool_config_is_exactly_section_a` | test | `test_study_pool_config_is_exactly_section_a` | [tests/experiment/test_x5g1t_identity.py:305](../../tests/experiment/test_x5g1t_identity.py#L305) |  |
| `test_study_run_key` | test | `test_study_run_key` | [tests/experiment/test_x5g1t_training.py:109](../../tests/experiment/test_x5g1t_training.py#L109) |  |
| `test_study_train_config_custom_grid` | test | `test_study_train_config_custom_grid` | [tests/experiment/test_x5g1t_training.py:101](../../tests/experiment/test_x5g1t_training.py#L101) |  |
| `test_study_train_config_defaults` | test | `test_study_train_config_defaults` | [tests/experiment/test_x5g1t_training.py:89](../../tests/experiment/test_x5g1t_training.py#L89) |  |
| `test_suffix_enumeration_against_brute_force` | test | `test_suffix_enumeration_against_brute_force` | [tests/hws/test_b_exact.py:147](../../tests/hws/test_b_exact.py#L147) |  |
| `test_suffix_identity_holds_for_other_suffix_lengths` | test | `test_suffix_identity_holds_for_other_suffix_lengths` | [tests/k4b/test_a_prop1.py:126](../../tests/k4b/test_a_prop1.py#L126) |  |
| `test_suffix_posterior_error_paths` | test | `test_suffix_posterior_error_paths` | [tests/oracle_profile/test_oracle_profile_traps.py:246](../../tests/oracle_profile/test_oracle_profile_traps.py#L246) | Item 6. |
| `test_summaries_hand_values` | test | `test_summaries_hand_values` | [tests/topology/test_persistence.py:185](../../tests/topology/test_persistence.py#L185) |  |
| `test_summarize_three_run_reading` | test | `test_summarize_three_run_reading` | [tests/experiment/test_circ_audit.py:53](../../tests/experiment/test_circ_audit.py#L53) |  |
| `test_summary_tree_mean_and_ddof1` | test | `test_summary_tree_mean_and_ddof1` | [tests/hws/test_a_stats.py:85](../../tests/hws/test_a_stats.py#L85) |  |
| `test_summed_images_differ_from_minimum_image` | test | `test_summed_images_differ_from_minimum_image` | [tests/x2a_stage0/test_x2a_stage0.py:142](../../tests/x2a_stage0/test_x2a_stage0.py#L142) |  |
| `test_supersede_manifest_and_bit_identical_regeneration` | test | `test_supersede_manifest_and_bit_identical_regeneration` | [tests/x6_stage1/test_b_chain_ops.py:205](../../tests/x6_stage1/test_b_chain_ops.py#L205) |  |
| `test_supersede_moves_append_only_and_records` | test | `test_supersede_moves_append_only_and_records` | [tests/c2_readout/test_b_lineage.py:273](../../tests/c2_readout/test_b_lineage.py#L273) |  |
| `test_superseded_hist_is_read` | test | `test_superseded_hist_is_read` | [tests/hwsb/test_b_registry.py:126](../../tests/hwsb/test_b_registry.py#L126) |  |
| `test_supervise_enforces_s6_limits` | test | `test_supervise_enforces_s6_limits` | [tests/x6_stage1/test_b_nb_s0_ops.py:332](../../tests/x6_stage1/test_b_nb_s0_ops.py#L332) |  |
| `test_supervise_hold_waits_then_continues` | test | `test_supervise_hold_waits_then_continues` | [tests/x6_stage1/test_b_nb_s0_ops.py:353](../../tests/x6_stage1/test_b_nb_s0_ops.py#L353) |  |
| `test_supervise_stop_propagates_and_closes_children` | test | `test_supervise_stop_propagates_and_closes_children` | [tests/x6_stage1/test_b_nb_s0_ops.py:342](../../tests/x6_stage1/test_b_nb_s0_ops.py#L342) |  |
| `test_supervisor_enforces_limits_on_grandchild` | test | `test_supervisor_enforces_limits_on_grandchild` | [tests/d2a/test_process_tree_repair.py:69](../../tests/d2a/test_process_tree_repair.py#L69) |  |
| `test_supervisor_model_cpu_kills_only_that_child` | test | `test_supervisor_model_cpu_kills_only_that_child` | [tests/d2a/test_b_resource.py:213](../../tests/d2a/test_b_resource.py#L213) |  |
| `test_supervisor_process_memory_kills_only_that_child` | test | `test_supervisor_process_memory_kills_only_that_child` | [tests/d2a/test_b_resource.py:222](../../tests/d2a/test_b_resource.py#L222) |  |
| `test_supervisor_quiet_when_every_limit_is_met_exactly` | test | `test_supervisor_quiet_when_every_limit_is_met_exactly` | [tests/d2a/test_b_resource.py:205](../../tests/d2a/test_b_resource.py#L205) |  |
| `test_supervisor_reasons_record_the_polling_interval` | test | `test_supervisor_reasons_record_the_polling_interval` | [tests/d2a/test_b_resource.py:258](../../tests/d2a/test_b_resource.py#L258) |  |
| `test_supervisor_stage_budget_kills_all` | test | `test_supervisor_stage_budget_kills_all` | [tests/d2a/test_b_resource.py:232](../../tests/d2a/test_b_resource.py#L232) |  |
| `test_supervisor_total_budget_kills_all` | test | `test_supervisor_total_budget_kills_all` | [tests/d2a/test_b_resource.py:246](../../tests/d2a/test_b_resource.py#L246) |  |
| `test_support_506_of_512_fails` | test | `test_support_506_of_512_fails` | [tests/c1prime/test_a_chart_val.py:126](../../tests/c1prime/test_a_chart_val.py#L126) |  |
| `test_support_507_of_512_passes` | test | `test_support_507_of_512_passes` | [tests/c1prime/test_a_chart_val.py:121](../../tests/c1prime/test_a_chart_val.py#L121) |  |
| `test_support_boundary_is_strict` | test | `test_support_boundary_is_strict` | [tests/k4b/test_a_decision.py:116](../../tests/k4b/test_a_decision.py#L116) |  |
| `test_support_degenerate_covariance` | test | `test_support_degenerate_covariance` | [tests/analysis/test_x4f_scores.py:244](../../tests/analysis/test_x4f_scores.py#L244) |  |
| `test_support_gate_literal_rule` | test | `test_support_gate_literal_rule` | [tests/analysis/test_x4f_scores.py:264](../../tests/analysis/test_x4f_scores.py#L264) |  |
| `test_support_identity_patch_and_planted_shift` | test | `test_support_identity_patch_and_planted_shift` | [tests/analysis/test_x4f_scores.py:215](../../tests/analysis/test_x4f_scores.py#L215) |  |
| `test_support_is_mixed_and_prefix_correlated` | test | `test_support_is_mixed_and_prefix_correlated` | [tests/k4b/test_a_theorem_a.py:127](../../tests/k4b/test_a_theorem_a.py#L127) |  |
| `test_support_missing_mass_and_width_exact` | test | `test_support_missing_mass_and_width_exact` | [tests/hwsb/test_a_endpoints.py:144](../../tests/hwsb/test_a_endpoints.py#L144) |  |
| `test_support_ratio_undefined_with_duplicated_rows` | test | `test_support_ratio_undefined_with_duplicated_rows` | [tests/analysis/test_x4f_scores.py:235](../../tests/analysis/test_x4f_scores.py#L235) |  |
| `test_support_reasons_count_unsupported_rows` | test | `test_support_reasons_count_unsupported_rows` | [tests/hwsb/test_a_endpoints.py:166](../../tests/hwsb/test_a_endpoints.py#L166) |  |
| `test_support_report_sealed_form_has_no_reconstructing_keys` | test | `test_support_report_sealed_form_has_no_reconstructing_keys` | [tests/k4b/test_b_flow.py:94](../../tests/k4b/test_b_flow.py#L94) |  |
| `test_support_report_unsealed_form_is_refused_in_a_validation_report` | test | `test_support_report_unsealed_form_is_refused_in_a_validation_report` | [tests/k4b/test_b_flow.py:107](../../tests/k4b/test_b_flow.py#L107) |  |
| `test_supported_c_hor_without_carries_is_inconclusive` | test | `test_supported_c_hor_without_carries_is_inconclusive` | [tests/d2a/test_b_rules_decide.py:205](../../tests/d2a/test_b_rules_decide.py#L205) |  |
| `test_symbol_constant_arm_difference_contributes_half_k_delta_m` | test | `test_symbol_constant_arm_difference_contributes_half_k_delta_m` | [tests/c1prime/test_b_identities.py:96](../../tests/c1prime/test_b_identities.py#L96) |  |
| `test_symbol_constant_cancels_exactly_when_masses_are_equal` | test | `test_symbol_constant_cancels_exactly_when_masses_are_equal` | [tests/c1prime/test_b_identities.py:107](../../tests/c1prime/test_b_identities.py#L107) |  |
| `test_symbol_law_aeff_and_last_entropy_direct` | test | `test_symbol_law_aeff_and_last_entropy_direct` | [tests/hws/test_b_exact.py:128](../../tests/hws/test_b_exact.py#L128) |  |
| `test_symbol_order_a_accepts_correct_map_rejects_inverse` | test | `test_symbol_order_a_accepts_correct_map_rejects_inverse` | [tests/c2_readout/test_a_readout.py:221](../../tests/c2_readout/test_a_readout.py#L221) |  |
| `test_symbol_order_b_accepts_correct_map_rejects_inverse` | test | `test_symbol_order_b_accepts_correct_map_rejects_inverse` | [tests/c2_readout/test_a_readout.py:215](../../tests/c2_readout/test_a_readout.py#L215) |  |
| `test_symbol_order_c_accepts_correct_map_rejects_inverse` | test | `test_symbol_order_c_accepts_correct_map_rejects_inverse` | [tests/c2_readout/test_a_readout.py:231](../../tests/c2_readout/test_a_readout.py#L231) |  |
| `test_symbol_perm_uses_replicate_seed_stream` | test | `test_symbol_perm_uses_replicate_seed_stream` | [tests/process/test_overlap.py:102](../../tests/process/test_overlap.py#L102) |  |
| `test_symbol_permutation_invariance` | test | `test_symbol_permutation_invariance` | [tests/analysis/test_horizon.py:91](../../tests/analysis/test_horizon.py#L91) |  |
| `test_symbol_renaming_keeps_test_latents_and_relabels_tokens` | test | `test_symbol_renaming_keeps_test_latents_and_relabels_tokens` | [tests/dataset/test_stage.py:46](../../tests/dataset/test_stage.py#L46) |  |
| `test_symmetry_report_measures_r_E_exactly_for_a_perturbed_emission` | test | `test_symmetry_report_measures_r_E_exactly_for_a_perturbed_emission` | [tests/c1prime/test_a_oracle.py:146](../../tests/c1prime/test_a_oracle.py#L146) |  |
| `test_symmetry_report_on_the_exact_fixture` | test | `test_symmetry_report_on_the_exact_fixture` | [tests/c1prime/test_a_oracle.py:140](../../tests/c1prime/test_a_oracle.py#L140) |  |
| `test_synthetic_correct_config_passes_read_only` | test | `test_synthetic_correct_config_passes_read_only` | [tests/experiment/test_x5g1t_config_synthetic.py:223](../../tests/experiment/test_x5g1t_config_synthetic.py#L223) |  |
| `test_synthetic_each_violation_rejected` | test | `test_synthetic_each_violation_rejected` | [tests/experiment/test_x5g1t_config_synthetic.py:268](../../tests/experiment/test_x5g1t_config_synthetic.py#L268) |  |
| `test_synthetic_exact_upper_gives_exact_fraction` | test | `test_synthetic_exact_upper_gives_exact_fraction` | [tests/k4b/test_a_transport_bound.py:120](../../tests/k4b/test_a_transport_bound.py#L120) |  |
| `test_synthetic_non_bounded_raises_identity` | test | `test_synthetic_non_bounded_raises_identity` | [tests/k4b/test_a_transport_bound.py:136](../../tests/k4b/test_a_transport_bound.py#L136) |  |
| `test_synthetic_production_source_id_rejected` | test | `test_synthetic_production_source_id_rejected` | [tests/experiment/test_x5g1t_config_synthetic.py:274](../../tests/experiment/test_x5g1t_config_synthetic.py#L274) | The synthetic store holds the production world content under the production config, so |
| `test_synthetic_source_payload_mutated_on_disk_rejected` | test | `test_synthetic_source_payload_mutated_on_disk_rejected` | [tests/experiment/test_x5g1t_config_synthetic.py:286](../../tests/experiment/test_x5g1t_config_synthetic.py#L286) |  |
| `test_synthetic_store_reproduces_the_contract_identities` | test | `test_synthetic_store_reproduces_the_contract_identities` | [tests/hws/test_b_kc1.py:198](../../tests/hws/test_b_kc1.py#L198) |  |
| `test_T03_unit_square_known_answer` | test | `test_T03_unit_square_known_answer` | [tests/topology/test_persistence.py:53](../../tests/topology/test_persistence.py#L53) |  |
| `test_T04_scale_covariance` | test | `test_T04_scale_covariance` | [tests/topology/test_persistence.py:72](../../tests/topology/test_persistence.py#L72) |  |
| `test_T05_permutation_invariance` | test | `test_T05_permutation_invariance` | [tests/topology/test_persistence.py:105](../../tests/topology/test_persistence.py#L105) |  |
| `test_T06_circle_above_gaussian_floor` | test | `test_T06_circle_above_gaussian_floor` | [tests/topology/test_shapes_calibration.py:49](../../tests/topology/test_shapes_calibration.py#L49) |  |
| `test_T07_disk_and_gaussian_below_threshold` | test | `test_T07_disk_and_gaussian_below_threshold` | [tests/topology/test_shapes_calibration.py:57](../../tests/topology/test_shapes_calibration.py#L57) |  |
| `test_T08_all_identical_cloud_collapsed` | test | `test_T08_all_identical_cloud_collapsed` | [tests/topology/test_persistence.py:137](../../tests/topology/test_persistence.py#L137) |  |
| `test_T08_all_zero_D_collapsed_and_S_zero` | test | `test_T08_all_zero_D_collapsed_and_S_zero` | [tests/topology/test_persistence.py:144](../../tests/topology/test_persistence.py#L144) |  |
| `test_T08_dedup_same_diagrams` | test | `test_T08_dedup_same_diagrams` | [tests/topology/test_persistence.py:123](../../tests/topology/test_persistence.py#L123) |  |
| `test_T09_small_threshold_marks_censored_not_dropped` | test | `test_T09_small_threshold_marks_censored_not_dropped` | [tests/topology/test_persistence.py:151](../../tests/topology/test_persistence.py#L151) |  |
| `test_T10_coeff_p_passed_through` | test | `test_T10_coeff_p_passed_through` | [tests/topology/test_persistence.py:227](../../tests/topology/test_persistence.py#L227) |  |
| `test_T11_gate_GA_circle_vs_disk` | test | `test_T11_gate_GA_circle_vs_disk` | [tests/topology/test_shapes_calibration.py:79](../../tests/topology/test_shapes_calibration.py#L79) |  |
| `test_T12_circular_coordinates_recover_angle` | test | `test_T12_circular_coordinates_recover_angle` | [tests/topology/test_circular_pca.py:17](../../tests/topology/test_circular_pca.py#L17) |  |
| `test_T13_pca_fit_on_one_set_applied_to_another` | test | `test_T13_pca_fit_on_one_set_applied_to_another` | [tests/topology/test_circular_pca.py:30](../../tests/topology/test_circular_pca.py#L30) |  |
| `test_T13_pca_none_is_noop` | test | `test_T13_pca_none_is_noop` | [tests/topology/test_circular_pca.py:52](../../tests/topology/test_circular_pca.py#L52) |  |
| `test_T1_T2_and_lemma_U_closed_forms` | test | `test_T1_T2_and_lemma_U_closed_forms` | [tests/x2a_stage0/test_x2a_stage0.py:239](../../tests/x2a_stage0/test_x2a_stage0.py#L239) |  |
| `test_T_CAUS_next_symbol_and_joint_logits` | test | `test_T_CAUS_next_symbol_and_joint_logits` | [tests/learner/test_multihorizon.py:179](../../tests/learner/test_multihorizon.py#L179) |  |
| `test_T_DECAY_groups_equal_transformer_plus_joint_matrices` | test | `test_T_DECAY_groups_equal_transformer_plus_joint_matrices` | [tests/learner/test_multihorizon.py:385](../../tests/learner/test_multihorizon.py#L385) |  |
| `test_T_FIX_named_histories_match_exact` | test | `test_T_FIX_named_histories_match_exact` | [tests/d2a/test_a_targets.py:88](../../tests/d2a/test_a_targets.py#L88) |  |
| `test_T_FIX_three_step_laws_match_independent_fractions` | test | `test_T_FIX_three_step_laws_match_independent_fractions` | [tests/d2a/test_a_targets.py:107](../../tests/d2a/test_a_targets.py#L107) |  |
| `test_T_FIX_tv_values_of_g0_fix` | test | `test_T_FIX_tv_values_of_g0_fix` | [tests/d2a/test_a_targets.py:122](../../tests/d2a/test_a_targets.py#L122) |  |
| `test_T_GRAD_ce2_alone_reaches_trunk_through_position_p` | test | `test_T_GRAD_ce2_alone_reaches_trunk_through_position_p` | [tests/learner/test_multihorizon.py:297](../../tests/learner/test_multihorizon.py#L297) |  |
| `test_T_HEAD_init_shared_between_horizons_and_matches_spec` | test | `test_T_HEAD_init_shared_between_horizons_and_matches_spec` | [tests/learner/test_multihorizon.py:137](../../tests/learner/test_multihorizon.py#L137) |  |
| `test_T_LOAD_horizon1_checkpoint_uses_load_model` | test | `test_T_LOAD_horizon1_checkpoint_uses_load_model` | [tests/learner/test_multihorizon.py:375](../../tests/learner/test_multihorizon.py#L375) |  |
| `test_T_LOAD_rejections_are_invalid_config` | test | `test_T_LOAD_rejections_are_invalid_config` | [tests/learner/test_multihorizon.py:368](../../tests/learner/test_multihorizon.py#L368) |  |
| `test_T_LOAD_round_trip` | test | `test_T_LOAD_round_trip` | [tests/learner/test_multihorizon.py:331](../../tests/learner/test_multihorizon.py#L331) |  |
| `test_T_LOSS_horizon_one_is_lm_loss_exactly` | test | `test_T_LOSS_horizon_one_is_lm_loss_exactly` | [tests/learner/test_multihorizon.py:288](../../tests/learner/test_multihorizon.py#L288) |  |
| `test_T_LOSS_joint_index_hand_values` | test | `test_T_LOSS_joint_index_hand_values` | [tests/learner/test_multihorizon.py:245](../../tests/learner/test_multihorizon.py#L245) |  |
| `test_T_LOSS_multi_horizon_loss_hand_values_and_exclusion` | test | `test_T_LOSS_multi_horizon_loss_hand_values_and_exclusion` | [tests/learner/test_multihorizon.py:267](../../tests/learner/test_multihorizon.py#L267) |  |
| `test_T_PAD_padding_after_t_changes_nothing_up_to_t` | test | `test_T_PAD_padding_after_t_changes_nothing_up_to_t` | [tests/d2a/test_a_pad.py:50](../../tests/d2a/test_a_pad.py#L50) |  |
| `test_T_PRIOR_whole_window_equals_full_filter` | test | `test_T_PRIOR_whole_window_equals_full_filter` | [tests/d2a/test_a_targets.py:256](../../tests/d2a/test_a_targets.py#L256) |  |
| `test_T_PRIOR_window8_equals_full_oracle_up_to_t8` | test | `test_T_PRIOR_window8_equals_full_oracle_up_to_t8` | [tests/d2a/test_a_targets.py:265](../../tests/d2a/test_a_targets.py#L265) |  |
| `test_T_PRIOR_window_prior_is_mu_T_power` | test | `test_T_PRIOR_window_prior_is_mu_T_power` | [tests/d2a/test_a_targets.py:241](../../tests/d2a/test_a_targets.py#L241) |  |
| `test_T_PRIOR_windows_use_the_true_time_marginal` | test | `test_T_PRIOR_windows_use_the_true_time_marginal` | [tests/d2a/test_a_targets.py:281](../../tests/d2a/test_a_targets.py#L281) |  |
| `test_T_RNG_global_rng_untouched_by_fit_with_factory` | test | `test_T_RNG_global_rng_untouched_by_fit_with_factory` | [tests/learner/test_multihorizon.py:313](../../tests/learner/test_multihorizon.py#L313) |  |
| `test_T_SEED_master_collisions` | test | `test_T_SEED_master_collisions` | [tests/d2a/test_a_world.py:113](../../tests/d2a/test_a_world.py#L113) |  |
| `test_T_SEED_pool_streams_follow_api_and_are_deterministic` | test | `test_T_SEED_pool_streams_follow_api_and_are_deterministic` | [tests/d2a/test_a_world.py:77](../../tests/d2a/test_a_world.py#L77) |  |
| `test_T_SEED_sequence_ids_disjoint_across_pools` | test | `test_T_SEED_sequence_ids_disjoint_across_pools` | [tests/d2a/test_a_world.py:93](../../tests/d2a/test_a_world.py#L93) |  |
| `test_T_SEED_streams_pairwise_distinct` | test | `test_T_SEED_streams_pairwise_distinct` | [tests/d2a/test_a_world.py:84](../../tests/d2a/test_a_world.py#L84) |  |
| `test_T_SUPP_support_lists_equal_independent_enumeration` | test | `test_T_SUPP_support_lists_equal_independent_enumeration` | [tests/d2a/test_a_targets.py:173](../../tests/d2a/test_a_targets.py#L173) |  |
| `test_T_SUPP_targets_vanish_off_support` | test | `test_T_SUPP_targets_vanish_off_support` | [tests/d2a/test_a_targets.py:180](../../tests/d2a/test_a_targets.py#L180) |  |
| `test_T_TARGET_tokens_after_p_change_nothing_at_p` | test | `test_T_TARGET_tokens_after_p_change_nothing_at_p` | [tests/learner/test_multihorizon.py:193](../../tests/learner/test_multihorizon.py#L193) |  |
| `test_T_TPL_canonical_pair_windows_differ_and_are_not_required_equal` | test | `test_T_TPL_canonical_pair_windows_differ_and_are_not_required_equal` | [tests/d2a/test_a_templates.py:109](../../tests/d2a/test_a_templates.py#L109) |  |
| `test_T_TPL_counts` | test | `test_T_TPL_counts` | [tests/d2a/test_a_templates.py:70](../../tests/d2a/test_a_templates.py#L70) |  |
| `test_T_TPL_enumeration_order_follows_api` | test | `test_T_TPL_enumeration_order_follows_api` | [tests/d2a/test_a_templates.py:77](../../tests/d2a/test_a_templates.py#L77) |  |
| `test_T_TPL_exact_identities_at_hand_template` | test | `test_T_TPL_exact_identities_at_hand_template` | [tests/d2a/test_a_templates.py:96](../../tests/d2a/test_a_templates.py#L96) |  |
| `test_T_TPL_registered_templates` | test | `test_T_TPL_registered_templates` | [tests/d2a/test_a_templates.py:120](../../tests/d2a/test_a_templates.py#L120) |  |
| `test_T_TPL_structure_of_every_pair` | test | `test_T_TPL_structure_of_every_pair` | [tests/d2a/test_a_templates.py:85](../../tests/d2a/test_a_templates.py#L85) |  |
| `test_T_TRUNK_model_level_trunk_and_logits_bitwise` | test | `test_T_TRUNK_model_level_trunk_and_logits_bitwise` | [tests/learner/test_multihorizon.py:100](../../tests/learner/test_multihorizon.py#L100) |  |
| `test_T_TRUNK_trainer_step0_trunks_equal_across_horizons` | test | `test_T_TRUNK_trainer_step0_trunks_equal_across_horizons` | [tests/learner/test_multihorizon.py:112](../../tests/learner/test_multihorizon.py#L112) |  |
| `test_table_entries_against_independent_decimal` | test | `test_table_entries_against_independent_decimal` | [tests/x6_stage1/test_a_numerics.py:76](../../tests/x6_stage1/test_a_numerics.py#L76) |  |
| `test_tables_equal_independent_dp_and_validate` | test | `test_tables_equal_independent_dp_and_validate` | [tests/x6_stage1/test_a_pairs.py:158](../../tests/x6_stage1/test_a_pairs.py#L158) |  |
| `test_tail_diagnostics_d1_d2` | test | `test_tail_diagnostics_d1_d2` | [tests/x6_stage1/test_a_numerics.py:333](../../tests/x6_stage1/test_a_numerics.py#L333) |  |
| `test_tampered_digest_fails_load_block` | test | `test_tampered_digest_fails_load_block` | [tests/hwsb/test_b_streams.py:315](../../tests/hwsb/test_b_streams.py#L315) |  |
| `test_tampered_frozen_artefact_refused` | test | `test_tampered_frozen_artefact_refused` | [tests/k4b/test_b_charts.py:281](../../tests/k4b/test_b_charts.py#L281) |  |
| `test_tampered_pools_export_refuses_train` | test | `test_tampered_pools_export_refuses_train` | [tests/experiment/test_x5g1t_integration.py:350](../../tests/experiment/test_x5g1t_integration.py#L350) |  |
| `test_targets` | method | `DevData.test_targets` | [src/topo_pilot/experiment/s7_dev.py:161](../../src/topo_pilot/experiment/s7_dev.py#L161) | Stored test oracle targets in HistoryIndex order. |
| `test_tau_maps_symbol_columns_and_inverts` | test | `test_tau_maps_symbol_columns_and_inverts` | [tests/c1prime/test_a_oracle.py:103](../../tests/c1prime/test_a_oracle.py#L103) |  |
| `test_taylor_constants_and_exact_tail_inequalities` | test | `test_taylor_constants_and_exact_tail_inequalities` | [tests/circle_history/test_error_bound.py:179](../../tests/circle_history/test_error_bound.py#L179) |  |
| `test_taylor_series_bounds_each_parity_separately` | test | `test_taylor_series_bounds_each_parity_separately` | [tests/circle_history/test_reference_binding.py:205](../../tests/circle_history/test_reference_binding.py#L205) |  |
| `test_techbench_plumbing` | test | `test_techbench_plumbing` | [tests/experiment/test_x5g1_techbench_smoke.py:13](../../tests/experiment/test_x5g1_techbench_smoke.py#L13) |  |
| `test_template_hashes` | test | `test_template_hashes` | [tests/d2a/test_a_templates.py:131](../../tests/d2a/test_a_templates.py#L131) |  |
| `test_template_scale_pair` | test | `test_template_scale_pair` | [tests/d2a/test_b_behaviour.py:115](../../tests/d2a/test_b_behaviour.py#L115) |  |
| `test_terminal_marker_survives_quarantine` | test | `test_terminal_marker_survives_quarantine` | [tests/x6_stage1/test_b_chain_ops.py:146](../../tests/x6_stage1/test_b_chain_ops.py#L146) |  |
| `test_test_endpoint_refused_before_t_pre_and_t_pre_model` | test | `test_test_endpoint_refused_before_t_pre_and_t_pre_model` | [tests/c2_readout/test_b_policy.py:100](../../tests/c2_readout/test_b_policy.py#L100) |  |
| `test_test_pools_need_stage3` | test | `test_test_pools_need_stage3` | [tests/d2a/test_a_world.py:209](../../tests/d2a/test_a_world.py#L209) |  |
| `test_theorem2_b_G_contains_the_exact_G_and_does_not_blow_up` | test | `test_theorem2_b_G_contains_the_exact_G_and_does_not_blow_up` | [tests/c1prime/test_b_cert_bounds.py:137](../../tests/c1prime/test_b_cert_bounds.py#L137) |  |
| `test_theorem3_b_A_needs_and_is_saved_by_the_omega_term` | test | `test_theorem3_b_A_needs_and_is_saved_by_the_omega_term` | [tests/c1prime/test_b_cert_bounds.py:171](../../tests/c1prime/test_b_cert_bounds.py#L171) |  |
| `test_this_suites_tmp_path_is_outside_the_project_root` | test | `test_this_suites_tmp_path_is_outside_the_project_root` | [tests/hwsb/test_b_meter_law.py:134](../../tests/hwsb/test_b_meter_law.py#L134) |  |
| `test_threshold_boundary` | test | `test_threshold_boundary` | [tests/experiment/test_x5g1t_usage.py:118](../../tests/experiment/test_x5g1t_usage.py#L118) |  |
| `test_threshold_constant` | test | `test_threshold_constant` | [tests/analysis/test_x5_context.py:37](../../tests/analysis/test_x5_context.py#L37) |  |
| `test_threshold_constants` | test | `test_threshold_constants` | [tests/k4b/test_a_decision.py:79](../../tests/k4b/test_a_decision.py#L79) |  |
| `test_threshold_law_equals_direct_counting` | test | `test_threshold_law_equals_direct_counting` | [tests/circle_history/test_process_law.py:93](../../tests/circle_history/test_process_law.py#L93) |  |
| `test_threshold_law_hand_values` | test | `test_threshold_law_hand_values` | [tests/circle_history/test_process_law.py:102](../../tests/circle_history/test_process_law.py#L102) |  |
| `test_tie_rule_larger_lambda_wins` | test | `test_tie_rule_larger_lambda_wins` | [tests/experiment/test_x4f_probe.py:123](../../tests/experiment/test_x4f_probe.py#L123) |  |
| `test_tiers` | test | `test_tiers` | [tests/hws/test_b_worlds.py:131](../../tests/hws/test_b_worlds.py#L131) |  |
| `test_time_never_resumes` | test | `test_time_never_resumes` | [tests/experiment/test_x5g1t_runtime.py:264](../../tests/experiment/test_x5g1t_runtime.py#L264) |  |
| `test_timed_error_is_logged_and_reraised` | test | `test_timed_error_is_logged_and_reraised` | [tests/circle_history/test_builder_v24_runtime.py:43](../../tests/circle_history/test_builder_v24_runtime.py#L43) |  |
| `test_timed_post_return_check_with_injected_clock` | test | `test_timed_post_return_check_with_injected_clock` | [tests/circle_history/test_builder_v24_runtime.py:50](../../tests/circle_history/test_builder_v24_runtime.py#L50) |  |
| `test_timed_records_start_end_and_marker` | test | `test_timed_records_start_end_and_marker` | [tests/circle_history/test_builder_v24_runtime.py:35](../../tests/circle_history/test_builder_v24_runtime.py#L35) |  |
| `test_to_canonical_random_perm_exact` | test | `test_to_canonical_random_perm_exact` | [tests/hwsb/test_a_learning.py:167](../../tests/hwsb/test_a_learning.py#L167) |  |
| `test_token_readers_reject_out_of_range_values_instead_of_wrapping` | test | `test_token_readers_reject_out_of_range_values_instead_of_wrapping` | [tests/c1prime_registry/test_registry_builder.py:51](../../tests/c1prime_registry/test_registry_builder.py#L51) |  |
| `test_tokens_before_suffix_have_no_effect` | test | `test_tokens_before_suffix_have_no_effect` | [tests/oracle_profile/test_oracle_profile_traps.py:160](../../tests/oracle_profile/test_oracle_profile_traps.py#L160) | Item 2: every prefix (even ones making the full row impossible) leaves post_K unchanged. |
| `test_tolerance_boundary` | test | `test_tolerance_boundary` | [tests/experiment/test_x5g1_verify.py:24](../../tests/experiment/test_x5g1_verify.py#L24) |  |
| `test_tool_gate_rerun_never_collides` | test | `test_tool_gate_rerun_never_collides` | [tests/experiment/test_runner.py:96](../../tests/experiment/test_runner.py#L96) |  |
| `test_tool_line_strips_pytest_wall_time` | test | `test_tool_line_strips_pytest_wall_time` | [tests/experiment/test_runner.py:92](../../tests/experiment/test_runner.py#L92) |  |
| `test_torch_versions_reads_the_lock_line` | test | `test_torch_versions_reads_the_lock_line` | [tests/hwsb/test_b_e4path.py:262](../../tests/hwsb/test_b_e4path.py#L262) |  |
| `test_train_complete_statuses` | test | `test_train_complete_statuses` | [tests/x6_stage1/test_b_ingest_bundle.py:290](../../tests/x6_stage1/test_b_ingest_bundle.py#L290) |  |
| `test_train_equals_learner_stage_bitwise` | test | `test_train_equals_learner_stage_bitwise` | [tests/hwsb/test_b_e4path.py:127](../../tests/hwsb/test_b_e4path.py#L127) |  |
| `test_train_one_complete_matches_learner_stage` | test | `test_train_one_complete_matches_learner_stage` | [tests/experiment/test_x5g1t_training.py:204](../../tests/experiment/test_x5g1t_training.py#L204) |  |
| `test_train_one_incomplete_recorded_and_reraised` | test | `test_train_one_incomplete_recorded_and_reraised` | [tests/experiment/test_x5g1t_training.py:252](../../tests/experiment/test_x5g1t_training.py#L252) |  |
| `test_trained_ledger_holds_six` | test | `test_trained_ledger_holds_six` | [tests/k4b/test_b_charts.py:166](../../tests/k4b/test_b_charts.py#L166) |  |
| `test_trained_meta_against_step0_expectation_fails` | test | `test_trained_meta_against_step0_expectation_fails` | [tests/k4b/test_b_h1_meta.py:261](../../tests/k4b/test_b_h1_meta.py#L261) |  |
| `test_trainer_uses_loss_fn_for_joint_heads` | test | `test_trainer_uses_loss_fn_for_joint_heads` | [tests/learner/test_multihorizon.py:129](../../tests/learner/test_multihorizon.py#L129) |  |
| `test_training_and_model_configs` | test | `test_training_and_model_configs` | [tests/d2a/test_b_resource.py:63](../../tests/d2a/test_b_resource.py#L63) |  |
| `test_training_mode_is_invalid_config` | test | `test_training_mode_is_invalid_config` | [tests/learner/test_patch.py:219](../../tests/learner/test_patch.py#L219) |  |
| `test_trap_differs_from_enumeration_while_production_matches` | test | `test_trap_differs_from_enumeration_while_production_matches` | [tests/oracle_profile/test_oracle_profile_traps.py:138](../../tests/oracle_profile/test_oracle_profile_traps.py#L138) | Item 3 (a)-(d), plus the two restart traps of item 2. |
| `test_trapping_context_settings` | test | `test_trapping_context_settings` | [tests/circle_history/test_error_bound.py:117](../../tests/circle_history/test_error_bound.py#L117) |  |
| `test_tree_accounting_reads_interpreter_and_kill_reaches_it` | test | `test_tree_accounting_reads_interpreter_and_kill_reaches_it` | [tests/x6_stage1/test_b_nb_s0_ops.py:373](../../tests/x6_stage1/test_b_nb_s0_ops.py#L373) |  |
| `test_tree_mean_is_the_balanced_pairwise_tree` | test | `test_tree_mean_is_the_balanced_pairwise_tree` | [tests/c1prime/test_b_inference.py:114](../../tests/c1prime/test_b_inference.py#L114) |  |
| `test_tree_mean_order_differs_from_left_to_right` | test | `test_tree_mean_order_differs_from_left_to_right` | [tests/c1prime/test_b_inference.py:124](../../tests/c1prime/test_b_inference.py#L124) |  |
| `test_tree_mean_within_theorem5_with_cancellation_and_subnormals` | test | `test_tree_mean_within_theorem5_with_cancellation_and_subnormals` | [tests/c1prime/test_b_inference.py:130](../../tests/c1prime/test_b_inference.py#L130) |  |
| `test_tree_sha_definition` | test | `test_tree_sha_definition` | [tests/hws/test_b_records.py:130](../../tests/hws/test_b_records.py#L130) |  |
| `test_triangle_system_hand_graph_rows` | test | `test_triangle_system_hand_graph_rows` | [tests/circle_history/test_cochain.py:94](../../tests/circle_history/test_cochain.py#L94) |  |
| `test_triangle_system_k4_and_tree` | test | `test_triangle_system_k4_and_tree` | [tests/circle_history/test_cochain.py:112](../../tests/circle_history/test_cochain.py#L112) |  |
| `test_trivial_restricted_class_stops_unresolved_after_lift_record` | test | `test_trivial_restricted_class_stops_unresolved_after_lift_record` | [tests/c1prime/test_a_chart.py:270](../../tests/c1prime/test_a_chart.py#L270) | Items 4 and 9: g = 0 on C* -> primitive_class raises Unresolved, which the chart gate |
| `test_truncated_json_is_registry_incomplete` | test | `test_truncated_json_is_registry_incomplete` | [tests/k4b/test_b_registry_fixes.py:83](../../tests/k4b/test_b_registry_fixes.py#L83) |  |
| `test_truth_is_neither_support_nor_exclude` | test | `test_truth_is_neither_support_nor_exclude` | [tests/k4b/test_a_decision.py:216](../../tests/k4b/test_a_decision.py#L216) |  |
| `test_two_column_target_in_one_direction_has_rank_one` | test | `test_two_column_target_in_one_direction_has_rank_one` | [tests/analysis/test_x4f_erasure.py:209](../../tests/analysis/test_x4f_erasure.py#L209) |  |
| `test_two_route_accepts_correct_map_rejects_inverse` | test | `test_two_route_accepts_correct_map_rejects_inverse` | [tests/c2_readout/test_a_readout.py:239](../../tests/c2_readout/test_a_readout.py#L239) |  |
| `test_two_route_cancellation_and_zero_rows_new7` | test | `test_two_route_cancellation_and_zero_rows_new7` | [tests/c2_readout/test_a_readout.py:257](../../tests/c2_readout/test_a_readout.py#L257) |  |
| `test_two_stage_bootstrap_equals_full_row_multinomial` | test | `test_two_stage_bootstrap_equals_full_row_multinomial` | [tests/x6_stage1/test_a_numerics.py:258](../../tests/x6_stage1/test_a_numerics.py#L258) |  |
| `test_u_and_gamma_digits_exact` | test | `test_u_and_gamma_digits_exact` | [tests/circle_history/test_error_bound.py:95](../../tests/circle_history/test_error_bound.py#L95) |  |
| `test_unanchored_and_tiny_maps` | test | `test_unanchored_and_tiny_maps` | [tests/hws/test_b_worlds.py:334](../../tests/hws/test_b_worlds.py#L334) |  |
| `test_unanchored_labels` | test | `test_unanchored_labels` | [tests/hws/test_b_worlds.py:237](../../tests/hws/test_b_worlds.py#L237) |  |
| `test_unavailable_never_blocks_by_itself` | test | `test_unavailable_never_blocks_by_itself` | [tests/experiment/test_x5g1t_usage.py:139](../../tests/experiment/test_x5g1t_usage.py#L139) |  |
| `test_unavailable_never_clears` | test | `test_unavailable_never_clears` | [tests/experiment/test_x5g1t_usage.py:221](../../tests/experiment/test_x5g1t_usage.py#L221) |  |
| `test_unavailable_smoothing_diagnostics_are_technical` | test | `test_unavailable_smoothing_diagnostics_are_technical` | [tests/c1prime/test_a_chart_exceptions.py:167](../../tests/c1prime/test_a_chart_exceptions.py#L167) |  |
| `test_underpowered_capture_and_annotation` | test | `test_underpowered_capture_and_annotation` | [tests/hwsb/test_a_outcomes.py:188](../../tests/hwsb/test_a_outcomes.py#L188) |  |
| `test_underpowered_ladder_before_capture` | test | `test_underpowered_ladder_before_capture` | [tests/hwsb/test_a_outcomes.py:179](../../tests/hwsb/test_a_outcomes.py#L179) |  |
| `test_unfrozen_project_module_detected` | test | `test_unfrozen_project_module_detected` | [tests/circle_history/test_builder_v24_runtime.py:202](../../tests/circle_history/test_builder_v24_runtime.py#L202) |  |
| `test_uniform_belief_over_full_period_is_zero` | test | `test_uniform_belief_over_full_period_is_zero` | [tests/analysis/test_x4f_targets.py:34](../../tests/analysis/test_x4f_targets.py#L34) |  |
| `test_unit_vectors_scores_and_r4_norms_known_answers` | test | `test_unit_vectors_scores_and_r4_norms_known_answers` | [tests/circle_history/test_scores_precision.py:252](../../tests/circle_history/test_scores_precision.py#L252) |  |
| `test_unknown_mode_rejected` | test | `test_unknown_mode_rejected` | [tests/experiment/test_x5g1t_config_checks.py:273](../../tests/experiment/test_x5g1t_config_checks.py#L273) |  |
| `test_unknown_or_missing_mode_is_stop` | test | `test_unknown_or_missing_mode_is_stop` | [tests/experiment/test_x5g1t_usage_files.py:249](../../tests/experiment/test_x5g1t_usage_files.py#L249) |  |
| `test_unknown_or_unreadable_decision_is_hold_failure` | test | `test_unknown_or_unreadable_decision_is_hold_failure` | [tests/hwsb/test_b_hold.py:133](../../tests/hwsb/test_b_hold.py#L133) |  |
| `test_unknown_return_hook` | test | `test_unknown_return_hook` | [tests/learner/test_patch.py:235](../../tests/learner/test_patch.py#L235) |  |
| `test_unknown_site` | test | `test_unknown_site` | [tests/learner/test_patch.py:229](../../tests/learner/test_patch.py#L229) |  |
| `test_unmatched_family_keeps_partial_and_control_maps` | test | `test_unmatched_family_keeps_partial_and_control_maps` | [tests/experiment/test_x4f_maintenance.py:94](../../tests/experiment/test_x4f_maintenance.py#L94) |  |
| `test_unmatched_state_is_returned_not_raised` | test | `test_unmatched_state_is_returned_not_raised` | [tests/hwsb/test_a_outcomes.py:204](../../tests/hwsb/test_a_outcomes.py#L204) |  |
| `test_unreadable_file_inside_a_segment_counts_as_fixture` | test | `test_unreadable_file_inside_a_segment_counts_as_fixture` | [tests/k4b/test_b_registry_rules.py:175](../../tests/k4b/test_b_registry_rules.py#L175) |  |
| `test_unreadable_file_outside_a_segment_is_incomplete` | test | `test_unreadable_file_outside_a_segment_is_incomplete` | [tests/k4b/test_b_registry_rules.py:186](../../tests/k4b/test_b_registry_rules.py#L186) |  |
| `test_unreadable_marker_stops_recovery` | test | `test_unreadable_marker_stops_recovery` | [tests/x6_stage1/test_b_chain_ops.py:182](../../tests/x6_stage1/test_b_chain_ops.py#L182) |  |
| `test_unreadable_npz_fails_closed` | test | `test_unreadable_npz_fails_closed` | [tests/hwsb/test_b_registry.py:159](../../tests/hwsb/test_b_registry.py#L159) |  |
| `test_unregistered_pool_refused` | test | `test_unregistered_pool_refused` | [tests/x6_stage1/test_b_seed_pool_reg.py:158](../../tests/x6_stage1/test_b_seed_pool_reg.py#L158) |  |
| `test_unreleased_hold_never_returns` | test | `test_unreleased_hold_never_returns` | [tests/experiment/test_x5g1t_runtime.py:275](../../tests/experiment/test_x5g1t_runtime.py#L275) |  |
| `test_unresolved_c_hor_can_still_match_a_later_rule` | test | `test_unresolved_c_hor_can_still_match_a_later_rule` | [tests/d2a/test_b_rules_decide.py:231](../../tests/d2a/test_b_rules_decide.py#L231) |  |
| `test_unresolved_c_hor_never_fires_rule7` | test | `test_unresolved_c_hor_never_fires_rule7` | [tests/d2a/test_b_rules_decide.py:225](../../tests/d2a/test_b_rules_decide.py#L225) |  |
| `test_unresolved_chart_kernel_is_chart_unavailable` | test | `test_unresolved_chart_kernel_is_chart_unavailable` | [tests/c1prime/test_a_chart_exceptions.py:225](../../tests/c1prime/test_a_chart_exceptions.py#L225) | Unresolved from a frozen chart kernel (protocol section 14: INCONCLUSIVE/ |
| `test_unsatisfiable_within_all_bounds_is_unresolved` | test | `test_unsatisfiable_within_all_bounds_is_unresolved` | [tests/circle_history/test_cochain_lift.py:261](../../tests/circle_history/test_cochain_lift.py#L261) |  |
| `test_untouched_fixture_reaches_train_one_with_intended_pools` | test | `test_untouched_fixture_reaches_train_one_with_intended_pools` | [tests/experiment/test_x5g1t_identity.py:166](../../tests/experiment/test_x5g1t_identity.py#L166) |  |
| `test_up_is_the_smallest_float_not_below_c` | test | `test_up_is_the_smallest_float_not_below_c` | [tests/c1prime/test_b_cert_guards.py:78](../../tests/c1prime/test_b_cert_guards.py#L78) |  |
| `test_up_of_floats_and_bound_constants` | test | `test_up_of_floats_and_bound_constants` | [tests/c1prime/test_b_cert_guards.py:85](../../tests/c1prime/test_b_cert_guards.py#L85) |  |
| `test_upper_below_threshold_fails` | test | `test_upper_below_threshold_fails` | [tests/analysis/test_x5_context.py:72](../../tests/analysis/test_x5_context.py#L72) |  |
| `test_upper_exactly_threshold_is_near` | test | `test_upper_exactly_threshold_is_near` | [tests/analysis/test_x5_context.py:67](../../tests/analysis/test_x5_context.py#L67) |  |
| `test_upstream_used_licence_names_the_residual_skip_and_no_block3_claim` | test | `test_upstream_used_licence_names_the_residual_skip_and_no_block3_claim` | [tests/c2_readout/test_b_screens.py:323](../../tests/c2_readout/test_b_screens.py#L323) |  |
| `test_utc_parsing_accepts_coordinator_timestamps` | test | `test_utc_parsing_accepts_coordinator_timestamps` | [tests/oracle_profile/test_builder_controls.py:170](../../tests/oracle_profile/test_builder_controls.py#L170) |  |
| `test_v1_counts_median_ties_wraps_and_treats_sign_zero_as_disagreement` | test | `test_v1_counts_median_ties_wraps_and_treats_sign_zero_as_disagreement` | [tests/c1prime/test_b_gates.py:140](../../tests/c1prime/test_b_gates.py#L140) |  |
| `test_v1_sign_zero_on_both_sides_is_still_disagreement` | test | `test_v1_sign_zero_on_both_sides_is_still_disagreement` | [tests/c1prime/test_b_gates.py:145](../../tests/c1prime/test_b_gates.py#L145) |  |
| `test_v2_coverage_reasons_and_h4` | test | `test_v2_coverage_reasons_and_h4` | [tests/c2_readout/test_b_policy.py:277](../../tests/c2_readout/test_b_policy.py#L277) |  |
| `test_v2_kappa_agreement_wrap_and_sign_zero` | test | `test_v2_kappa_agreement_wrap_and_sign_zero` | [tests/c1prime/test_b_gates.py:176](../../tests/c1prime/test_b_gates.py#L176) |  |
| `test_v3_guard` | test | `test_v3_guard` | [tests/c1prime/test_b_cert_guards.py:170](../../tests/c1prime/test_b_cert_guards.py#L170) |  |
| `test_v3_guard_band_is_numerical_and_uses_rank_84_of_shared_draws` | test | `test_v3_guard_band_is_numerical_and_uses_rank_84_of_shared_draws` | [tests/c1prime/test_b_precision.py:199](../../tests/c1prime/test_b_precision.py#L199) |  |
| `test_v3_pass_and_model_headroom` | test | `test_v3_pass_and_model_headroom` | [tests/c1prime/test_b_precision.py:192](../../tests/c1prime/test_b_precision.py#L192) |  |
| `test_val_sealed_arrays_refused_before_the_outcome` | test | `test_val_sealed_arrays_refused_before_the_outcome` | [tests/c2_readout/test_b_policy.py:168](../../tests/c2_readout/test_b_policy.py#L168) |  |
| `test_valid_baseline` | test | `test_valid_baseline` | [tests/oracle_profile/test_builder_kernels.py:25](../../tests/oracle_profile/test_builder_kernels.py#L25) |  |
| `test_valid_histories_pass_for_signed_and_unsigned_dtypes` | test | `test_valid_histories_pass_for_signed_and_unsigned_dtypes` | [tests/circle_history/test_reference_binding.py:154](../../tests/circle_history/test_reference_binding.py#L154) |  |
| `test_valid_ledger_survives_run_that_raises` | test | `test_valid_ledger_survives_run_that_raises` | [tests/experiment/test_x5g1_export_integration.py:253](../../tests/experiment/test_x5g1_export_integration.py#L253) |  |
| `test_valid_releases_verify` | test | `test_valid_releases_verify` | [tests/c1prime/test_a_release_meter.py:118](../../tests/c1prime/test_a_release_meter.py#L118) |  |
| `test_valid_substitution_refused_before_train_one` | test | `test_valid_substitution_refused_before_train_one` | [tests/experiment/test_x5g1t_identity.py:266](../../tests/experiment/test_x5g1t_identity.py#L266) |  |
| `test_validate_checkpoints_model_config_compared_with_defaults_filled` | test | `test_validate_checkpoints_model_config_compared_with_defaults_filled` | [tests/experiment/test_x5g1t_checkpoint_checks.py:103](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L103) |  |
| `test_validate_checkpoints_real_store_passes` | test | `test_validate_checkpoints_real_store_passes` | [tests/experiment/test_x5g1t_checkpoint_checks.py:91](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L91) |  |
| `test_validate_handoff_json_reports_parse_failure` | test | `test_validate_handoff_json_reports_parse_failure` | [tests/k4b/test_b_registry.py:225](../../tests/k4b/test_b_registry.py#L225) |  |
| `test_validate_is_read_only` | test | `test_validate_is_read_only` | [tests/experiment/test_x5g1t_integration.py:383](../../tests/experiment/test_x5g1t_integration.py#L383) |  |
| `test_validate_pool_accepts_intended_and_refuses_others` | test | `test_validate_pool_accepts_intended_and_refuses_others` | [tests/experiment/test_x5g1t_identity.py:288](../../tests/experiment/test_x5g1t_identity.py#L288) |  |
| `test_validate_process_accepts_valid_models` | test | `test_validate_process_accepts_valid_models` | [tests/oracle_profile/test_oracle_profile_kernels.py:49](../../tests/oracle_profile/test_oracle_profile_kernels.py#L49) |  |
| `test_validate_process_rejects` | test | `test_validate_process_rejects` | [tests/oracle_profile/test_oracle_profile_kernels.py:93](../../tests/oracle_profile/test_oracle_profile_kernels.py#L93) |  |
| `test_validate_process_reports_known_maxima` | test | `test_validate_process_reports_known_maxima` | [tests/oracle_profile/test_oracle_profile_kernels.py:58](../../tests/oracle_profile/test_oracle_profile_kernels.py#L58) | Dyadic perturbations: row error 2^-10 in T, 2^-11 in E, pi sum error 2^-9. |
| `test_validation_isolation_nan_poison` | test | `test_validation_isolation_nan_poison` | [tests/experiment/test_x4f_probe.py:99](../../tests/experiment/test_x4f_probe.py#L99) |  |
| `test_validation_needs_the_calibration_pass_set` | test | `test_validation_needs_the_calibration_pass_set` | [tests/c1prime/test_a_gates.py:216](../../tests/c1prime/test_a_gates.py#L216) |  |
| `test_validity_rule` | test | `test_validity_rule` | [tests/x2a_stage0/test_x2a_stage0_ph.py:162](../../tests/x2a_stage0/test_x2a_stage0_ph.py#L162) |  |
| `test_verdict_all_ok_statuses_do_not_block` | test | `test_verdict_all_ok_statuses_do_not_block` | [tests/analysis/test_f1_rule.py:116](../../tests/analysis/test_f1_rule.py#L116) |  |
| `test_verdict_all_pass_is_feasible` | test | `test_verdict_all_pass_is_feasible` | [tests/analysis/test_x4f_scores.py:279](../../tests/analysis/test_x4f_scores.py#L279) |  |
| `test_verdict_any_single_non_pass_blocks_feasible` | test | `test_verdict_any_single_non_pass_blocks_feasible` | [tests/analysis/test_x4f_scores.py:319](../../tests/analysis/test_x4f_scores.py#L319) |  |
| `test_verdict_g1_fail_is_not_feasible_even_with_inconclusive_gates` | test | `test_verdict_g1_fail_is_not_feasible_even_with_inconclusive_gates` | [tests/analysis/test_x4f_scores.py:284](../../tests/analysis/test_x4f_scores.py#L284) |  |
| `test_verdict_g2_inconclusive_names_g2_and_model` | test | `test_verdict_g2_inconclusive_names_g2_and_model` | [tests/analysis/test_x4f_scores.py:293](../../tests/analysis/test_x4f_scores.py#L293) |  |
| `test_verdict_inconclusive_on_input_status` | test | `test_verdict_inconclusive_on_input_status` | [tests/analysis/test_f1_rule.py:110](../../tests/analysis/test_f1_rule.py#L110) |  |
| `test_verdict_inconclusive_on_learning_gate` | test | `test_verdict_inconclusive_on_learning_gate` | [tests/analysis/test_f1_rule.py:99](../../tests/analysis/test_f1_rule.py#L99) |  |
| `test_verdict_inconclusive_with_fewer_than_three_replicates` | test | `test_verdict_inconclusive_with_fewer_than_three_replicates` | [tests/analysis/test_f1_rule.py:121](../../tests/analysis/test_f1_rule.py#L121) |  |
| `test_verdict_is_pure` | test | `test_verdict_is_pure` | [tests/analysis/test_x5_context.py:153](../../tests/analysis/test_x5_context.py#L153) |  |
| `test_verdict_names_first_gate_in_g1_to_g5_order` | test | `test_verdict_names_first_gate_in_g1_to_g5_order` | [tests/analysis/test_x4f_scores.py:300](../../tests/analysis/test_x4f_scores.py#L300) |  |
| `test_verdict_not_run_after_later_failure_is_inconclusive` | test | `test_verdict_not_run_after_later_failure_is_inconclusive` | [tests/analysis/test_x4f_scores.py:309](../../tests/analysis/test_x4f_scores.py#L309) |  |
| `test_verdict_reads_status_and_reasons` | test | `test_verdict_reads_status_and_reasons` | [tests/experiment/test_report_e2.py:51](../../tests/experiment/test_report_e2.py#L51) |  |
| `test_verdict_rejected_when_median_below_envelope` | test | `test_verdict_rejected_when_median_below_envelope` | [tests/analysis/test_f1_rule.py:93](../../tests/analysis/test_f1_rule.py#L93) |  |
| `test_verdict_rejected_when_six_of_eight_positive` | test | `test_verdict_rejected_when_six_of_eight_positive` | [tests/analysis/test_f1_rule.py:87](../../tests/analysis/test_f1_rule.py#L87) |  |
| `test_verdict_supported` | test | `test_verdict_supported` | [tests/analysis/test_f1_rule.py:81](../../tests/analysis/test_f1_rule.py#L81) |  |
| `test_verify_broken_backend_is_failure_not_raise` | test | `test_verify_broken_backend_is_failure_not_raise` | [tests/experiment/test_x5g1_safety.py:164](../../tests/experiment/test_x5g1_safety.py#L164) |  |
| `test_verify_disallowed_consumer_is_failure_not_raise` | test | `test_verify_disallowed_consumer_is_failure_not_raise` | [tests/experiment/test_x5g1_safety.py:149](../../tests/experiment/test_x5g1_safety.py#L149) |  |
| `test_verify_full_hash_of_lawful_artifacts_passes` | test | `test_verify_full_hash_of_lawful_artifacts_passes` | [tests/experiment/test_x5g1_safety.py:107](../../tests/experiment/test_x5g1_safety.py#L107) |  |
| `test_verify_full_missing_id_rejected` | test | `test_verify_full_missing_id_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:231](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L231) |  |
| `test_verify_full_mutated_payload_rejected` | test | `test_verify_full_mutated_payload_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:251](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L251) |  |
| `test_verify_full_passes_on_lawful_artifacts` | test | `test_verify_full_passes_on_lawful_artifacts` | [tests/experiment/test_x5g1t_checkpoint_checks.py:224](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L224) |  |
| `test_verify_full_wrong_class_rejected` | test | `test_verify_full_wrong_class_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:244](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L244) |  |
| `test_verify_full_wrong_sha_rejected` | test | `test_verify_full_wrong_sha_rejected` | [tests/experiment/test_x5g1t_checkpoint_checks.py:237](../../tests/experiment/test_x5g1t_checkpoint_checks.py#L237) |  |
| `test_verify_identity_accepts_the_correct_identity` | test | `test_verify_identity_accepts_the_correct_identity` | [tests/d2a/test_b_resource.py:101](../../tests/d2a/test_b_resource.py#L101) |  |
| `test_verify_identity_fails_closed_without_a_lock` | test | `test_verify_identity_fails_closed_without_a_lock` | [tests/d2a/test_b_resource.py:126](../../tests/d2a/test_b_resource.py#L126) |  |
| `test_verify_identity_rejects_each_wrong_identity` | test | `test_verify_identity_rejects_each_wrong_identity` | [tests/d2a/test_b_resource.py:117](../../tests/d2a/test_b_resource.py#L117) |  |
| `test_verify_meta_hash_mutated_fails` | test | `test_verify_meta_hash_mutated_fails` | [tests/experiment/test_x5g1_safety.py:141](../../tests/experiment/test_x5g1_safety.py#L141) |  |
| `test_verify_missing_artifact_is_failure_not_raise` | test | `test_verify_missing_artifact_is_failure_not_raise` | [tests/experiment/test_x5g1_safety.py:155](../../tests/experiment/test_x5g1_safety.py#L155) |  |
| `test_verify_parents_backend_error_never_raises` | test | `test_verify_parents_backend_error_never_raises` | [tests/experiment/test_x5g1_controls.py:187](../../tests/experiment/test_x5g1_controls.py#L187) |  |
| `test_verify_parents_matching_prefix` | test | `test_verify_parents_matching_prefix` | [tests/experiment/test_x5g1_controls.py:162](../../tests/experiment/test_x5g1_controls.py#L162) |  |
| `test_verify_parents_missing_id_never_raises` | test | `test_verify_parents_missing_id_never_raises` | [tests/experiment/test_x5g1_controls.py:178](../../tests/experiment/test_x5g1_controls.py#L178) |  |
| `test_verify_parents_wrong_prefix` | test | `test_verify_parents_wrong_prefix` | [tests/experiment/test_x5g1_controls.py:170](../../tests/experiment/test_x5g1_controls.py#L170) |  |
| `test_verify_payload_mutated_with_meta_intact_fails` | test | `test_verify_payload_mutated_with_meta_intact_fails` | [tests/experiment/test_x5g1_safety.py:132](../../tests/experiment/test_x5g1_safety.py#L132) |  |
| `test_verify_prefix_only_hash_rejected` | test | `test_verify_prefix_only_hash_rejected` | [tests/experiment/test_x5g1_safety.py:125](../../tests/experiment/test_x5g1_safety.py#L125) |  |
| `test_verify_release_refuses_mismatches` | test | `test_verify_release_refuses_mismatches` | [tests/k4b/test_b_flow.py:221](../../tests/k4b/test_b_flow.py#L221) |  |
| `test_verify_rows_passes_on_the_exact_table` | test | `test_verify_rows_passes_on_the_exact_table` | [tests/circle_history/test_reference_cache.py:187](../../tests/circle_history/test_reference_cache.py#L187) |  |
| `test_verify_rows_rejects_every_mismatch` | test | `test_verify_rows_rejects_every_mismatch` | [tests/circle_history/test_reference_cache.py:207](../../tests/circle_history/test_reference_cache.py#L207) |  |
| `test_verify_rows_rejects_missing_record_entry_and_duplicate_record` | test | `test_verify_rows_rejects_missing_record_entry_and_duplicate_record` | [tests/circle_history/test_reference_cache.py:212](../../tests/circle_history/test_reference_cache.py#L212) |  |
| `test_verify_wrong_full_hash_fails` | test | `test_verify_wrong_full_hash_fails` | [tests/experiment/test_x5g1_safety.py:115](../../tests/experiment/test_x5g1_safety.py#L115) |  |
| `test_volatile_fields_ignored_in_report_comparison` | test | `test_volatile_fields_ignored_in_report_comparison` | [tests/x6_stage1/test_b_chain_ops.py:226](../../tests/x6_stage1/test_b_chain_ops.py#L226) |  |
| `test_w01_boundary_squared_is_zero_over_integers` | test | `test_w01_boundary_squared_is_zero_over_integers` | [tests/world/test_world.py:135](../../tests/world/test_world.py#L135) |  |
| `test_w02_betti_known_answers` | test | `test_w02_betti_known_answers` | [tests/world/test_world.py:151](../../tests/world/test_world.py#L151) |  |
| `test_w03_cell_counts_n12` | test | `test_w03_cell_counts_n12` | [tests/world/test_world.py:162](../../tests/world/test_world.py#L162) |  |
| `test_w03_vertex_ids_and_coords` | test | `test_w03_vertex_ids_and_coords` | [tests/world/test_world.py:171](../../tests/world/test_world.py#L171) |  |
| `test_w04_graph_cycle_rank_differs_from_surface_betti1` | test | `test_w04_graph_cycle_rank_differs_from_surface_betti1` | [tests/world/test_world.py:180](../../tests/world/test_world.py#L180) |  |
| `test_w05_flat_metric_class_matches_built_dist` | test | `test_w05_flat_metric_class_matches_built_dist` | [tests/world/test_world.py:197](../../tests/world/test_world.py#L197) |  |
| `test_w05_flat_metric_cylinder_known_and_axioms` | test | `test_w05_flat_metric_cylinder_known_and_axioms` | [tests/world/test_world.py:187](../../tests/world/test_world.py#L187) |  |
| `test_w06_flat_vs_graph_sandwich` | test | `test_w06_flat_vs_graph_sandwich` | [tests/world/test_world.py:206](../../tests/world/test_world.py#L206) |  |
| `test_w06_graph_metric_option_is_graph_geodesic` | test | `test_w06_graph_metric_option_is_graph_geodesic` | [tests/world/test_world.py:213](../../tests/world/test_world.py#L213) |  |
| `test_w07_betti_invariant_under_vertex_relabelling` | test | `test_w07_betti_invariant_under_vertex_relabelling` | [tests/world/test_world.py:223](../../tests/world/test_world.py#L223) |  |
| `test_w08_face_repeating_a_vertex_raises_invalid_glue` | test | `test_w08_face_repeating_a_vertex_raises_invalid_glue` | [tests/world/test_world.py:238](../../tests/world/test_world.py#L238) |  |
| `test_w09_wrong_expected_betti_raises` | test | `test_w09_wrong_expected_betti_raises` | [tests/world/test_world.py:248](../../tests/world/test_world.py#L248) |  |
| `test_w0_emission_identity_matches_contract` | test | `test_w0_emission_identity_matches_contract` | [tests/hwsb/test_b_process.py:117](../../tests/hwsb/test_b_process.py#L117) |  |
| `test_w10_registry_dispatch_and_unknown_family` | test | `test_w10_registry_dispatch_and_unknown_family` | [tests/world/test_world.py:256](../../tests/world/test_world.py#L256) |  |
| `test_w11_torus_extension` | test | `test_w11_torus_extension` | [tests/world/test_world.py:280](../../tests/world/test_world.py#L280) |  |
| `test_w12_emission_is_the_canonical_overlap_bitwise` | test | `test_w12_emission_is_the_canonical_overlap_bitwise` | [tests/hws/test_b_worlds.py:158](../../tests/hws/test_b_worlds.py#L158) |  |
| `test_w12_klein_extension` | test | `test_w12_klein_extension` | [tests/world/test_world.py:292](../../tests/world/test_world.py#L292) |  |
| `test_w13_world_stage_saves_valid_spec_with_stable_id` | test | `test_w13_world_stage_saves_valid_spec_with_stable_id` | [tests/world/test_world.py:306](../../tests/world/test_world.py#L306) |  |
| `test_w2_beta_table_and_per_cue_heuristics` | test | `test_w2_beta_table_and_per_cue_heuristics` | [tests/x6_stage1/test_a_designed.py:170](../../tests/x6_stage1/test_a_designed.py#L170) |  |
| `test_w2_beta_zero_for_every_ladder_statistic` | test | `test_w2_beta_zero_for_every_ladder_statistic` | [tests/x6_stage1/test_a_designed.py:192](../../tests/x6_stage1/test_a_designed.py#L192) |  |
| `test_w33_isolation` | test | `test_w33_isolation` | [tests/experiment/test_x5g1_lineage.py:205](../../tests/experiment/test_x5g1_lineage.py#L205) |  |
| `test_w_hat_breaks_ties_to_the_lowest_index` | test | `test_w_hat_breaks_ties_to_the_lowest_index` | [tests/c1prime/test_b_gates.py:209](../../tests/c1prime/test_b_gates.py#L209) |  |
| `test_waiver_in_the_same_second_as_a_failure_counts` | test | `test_waiver_in_the_same_second_as_a_failure_counts` | [tests/experiment/test_runner.py:79](../../tests/experiment/test_runner.py#L79) |  |
| `test_warp_profile_a0_is_flat` | test | `test_warp_profile_a0_is_flat` | [tests/process/test_conductance.py:94](../../tests/process/test_conductance.py#L94) |  |
| `test_warp_profile_exact_mid_row_when_ny_odd` | test | `test_warp_profile_exact_mid_row_when_ny_odd` | [tests/process/test_conductance.py:84](../../tests/process/test_conductance.py#L84) |  |
| `test_warp_profile_hand_values_12x12` | test | `test_warp_profile_hand_values_12x12` | [tests/process/test_conductance.py:68](../../tests/process/test_conductance.py#L68) |  |
| `test_warp_profile_rejects_abs_a_ge_1` | test | `test_warp_profile_rejects_abs_a_ge_1` | [tests/process/test_conductance.py:101](../../tests/process/test_conductance.py#L101) |  |
| `test_warp_profile_rejects_ny_below_2` | test | `test_warp_profile_rejects_ny_below_2` | [tests/process/test_conductance.py:107](../../tests/process/test_conductance.py#L107) |  |
| `test_wave_exception_closes_all_started_trees` | test | `test_wave_exception_closes_all_started_trees` | [tests/d2a/test_process_tree_repair.py:83](../../tests/d2a/test_process_tree_repair.py#L83) |  |
| `test_wave_lease_rejects_path_components_before_creating_files` | test | `test_wave_lease_rejects_path_components_before_creating_files` | [tests/d2a/test_process_tree_repair.py:136](../../tests/d2a/test_process_tree_repair.py#L136) |  |
| `test_wave_refuses_duplicate_training_before_launch` | test | `test_wave_refuses_duplicate_training_before_launch` | [tests/d2a/test_process_tree_repair.py:111](../../tests/d2a/test_process_tree_repair.py#L111) |  |
| `test_waves_follow_the_fixed_order` | test | `test_waves_follow_the_fixed_order` | [tests/d2a/test_b_resource.py:50](../../tests/d2a/test_b_resource.py#L50) |  |
| `test_weight_decay_groups` | test | `test_weight_decay_groups` | [tests/learner/test_training.py:122](../../tests/learner/test_training.py#L122) |  |
| `test_weights_digest_definition_and_pickling_independence` | test | `test_weights_digest_definition_and_pickling_independence` | [tests/x6_stage1/test_b_train_chain.py:246](../../tests/x6_stage1/test_b_train_chain.py#L246) |  |
| `test_weights_digest_mismatch_fails_even_with_redownload` | test | `test_weights_digest_mismatch_fails_even_with_redownload` | [tests/x6_stage1/test_b_ingest_bundle.py:219](../../tests/x6_stage1/test_b_ingest_bundle.py#L219) |  |
| `test_weights_hash_honours_explicit_exclusions` | test | `test_weights_hash_honours_explicit_exclusions` | [tests/x6_stage1/test_b_ingest_bundle.py:209](../../tests/x6_stage1/test_b_ingest_bundle.py#L209) |  |
| `test_weights_hash_transfer_failures` | test | `test_weights_hash_transfer_failures` | [tests/x6_stage1/test_b_ingest_bundle.py:192](../../tests/x6_stage1/test_b_ingest_bundle.py#L192) |  |
| `test_well_conditioned_keeps_frozen_1e10` | test | `test_well_conditioned_keeps_frozen_1e10` | [tests/c1prime/test_c_ridge_tolerance.py:29](../../tests/c1prime/test_c_ridge_tolerance.py#L29) |  |
| `test_wheel_disk_lift_certificate` | test | `test_wheel_disk_lift_certificate` | [tests/circle_history/test_cochain_lift.py:193](../../tests/circle_history/test_cochain_lift.py#L193) |  |
| `test_whiten_anisotropic_correlated` | test | `test_whiten_anisotropic_correlated` | [tests/analysis/test_x4f_erasure.py:67](../../tests/analysis/test_x4f_erasure.py#L67) |  |
| `test_whiten_degenerate` | test | `test_whiten_degenerate` | [tests/analysis/test_x4f_erasure.py:115](../../tests/analysis/test_x4f_erasure.py#L115) |  |
| `test_whiten_floor_is_relative_to_lambda_max` | test | `test_whiten_floor_is_relative_to_lambda_max` | [tests/analysis/test_x4f_erasure.py:106](../../tests/analysis/test_x4f_erasure.py#L106) |  |
| `test_whiten_rank_deficient_keeps_exact_rank` | test | `test_whiten_rank_deficient_keeps_exact_rank` | [tests/analysis/test_x4f_erasure.py:88](../../tests/analysis/test_x4f_erasure.py#L88) |  |
| `test_whitened_rank_and_conditioning_failures` | test | `test_whitened_rank_and_conditioning_failures` | [tests/c2_readout/test_b_fwl_l1.py:129](../../tests/c2_readout/test_b_fwl_l1.py#L129) |  |
| `test_whitening_degenerate_covariance` | test | `test_whitening_degenerate_covariance` | [tests/c1prime/test_b_fwl.py:191](../../tests/c1prime/test_b_fwl.py#L191) |  |
| `test_whitening_is_the_symmetric_inverse_root_of_ledoit_wolf` | test | `test_whitening_is_the_symmetric_inverse_root_of_ledoit_wolf` | [tests/c1prime/test_b_fwl.py:176](../../tests/c1prime/test_b_fwl.py#L176) |  |
| `test_width_at_zero_equals_registered_exclusion_projection` | test | `test_width_at_zero_equals_registered_exclusion_projection` | [tests/k4b/test_a_width_b4.py:99](../../tests/k4b/test_a_width_b4.py#L99) |  |
| `test_width_D_shift_on_designed_draws` | test | `test_width_D_shift_on_designed_draws` | [tests/k4b/test_a_width_b4.py:107](../../tests/k4b/test_a_width_b4.py#L107) | Success draws have e+ + q+ + F = 0.0091 and e- + q- - F = -0.0091, so a shift by |
| `test_width_invariant_to_C_bar` | test | `test_width_invariant_to_C_bar` | [tests/k4b/test_a_width_b4.py:129](../../tests/k4b/test_a_width_b4.py#L129) |  |
| `test_width_matches_reference` | test | `test_width_matches_reference` | [tests/k4b/test_a_width_b4.py:92](../../tests/k4b/test_a_width_b4.py#L92) |  |
| `test_width_monotone_in_D_bar` | test | `test_width_monotone_in_D_bar` | [tests/k4b/test_a_width_b4.py:117](../../tests/k4b/test_a_width_b4.py#L117) |  |
| `test_width_signature_never_takes_C_bar` | test | `test_width_signature_never_takes_C_bar` | [tests/k4b/test_a_width_b4.py:87](../../tests/k4b/test_a_width_b4.py#L87) |  |
| `test_windows_count_identical_histories` | test | `test_windows_count_identical_histories` | [tests/experiment/test_x4b2.py:69](../../tests/experiment/test_x4b2.py#L69) |  |
| `test_worker_control_commands` | test | `test_worker_control_commands` | [tests/experiment/test_x5g1t_runtime.py:91](../../tests/experiment/test_x5g1t_runtime.py#L91) |  |
| `test_worker_control_malformed_or_unknown_is_stop` | test | `test_worker_control_malformed_or_unknown_is_stop` | [tests/experiment/test_x5g1t_runtime.py:98](../../tests/experiment/test_x5g1t_runtime.py#L98) |  |
| `test_worker_control_missing_is_allowed` | test | `test_worker_control_missing_is_allowed` | [tests/experiment/test_x5g1t_runtime.py:103](../../tests/experiment/test_x5g1t_runtime.py#L103) |  |
| `test_world_conditional_ceiling_threshold` | test | `test_world_conditional_ceiling_threshold` | [tests/d2a/test_b_rules_qualifiers.py:172](../../tests/d2a/test_b_rules_qualifiers.py#L172) |  |
| `test_world_counts_betti_and_builder` | test | `test_world_counts_betti_and_builder` | [tests/x2a_stage0/test_x2a_stage0.py:149](../../tests/x2a_stage0/test_x2a_stage0.py#L149) |  |
| `test_world_helpers` | test | `test_world_helpers` | [tests/hws/test_a_classify.py:194](../../tests/hws/test_a_classify.py#L194) |  |
| `test_world_kernels` | test | `test_world_kernels` | [tests/d2a/test_a_world.py:143](../../tests/d2a/test_a_world.py#L143) |  |
| `test_world_keys` | test | `test_world_keys` | [tests/hws/test_b_worlds.py:89](../../tests/hws/test_b_worlds.py#L89) |  |
| `test_world_look_streams_and_bit_identical_regeneration` | test | `test_world_look_streams_and_bit_identical_regeneration` | [tests/hws/test_b_oracle.py:114](../../tests/hws/test_b_oracle.py#L114) |  |
| `test_worlds_edges_boundary_and_orientability` | test | `test_worlds_edges_boundary_and_orientability` | [tests/d1_seam/test_d1_seam.py:203](../../tests/d1_seam/test_d1_seam.py#L203) |  |
| `test_wrap_edges_carry_horizontal_conductance` | test | `test_wrap_edges_carry_horizontal_conductance` | [tests/process/test_conductance.py:196](../../tests/process/test_conductance.py#L196) |  |
| `test_wrap_maps_into_minus_pi_exclusive_pi_inclusive` | test | `test_wrap_maps_into_minus_pi_exclusive_pi_inclusive` | [tests/c1prime/test_b_gates.py:109](../../tests/c1prime/test_b_gates.py#L109) |  |
| `test_wrap_maps_two_pi_to_zero` | test | `test_wrap_maps_two_pi_to_zero` | [tests/circle_history/test_builder_v25.py:228](../../tests/circle_history/test_builder_v25.py#L228) |  |
| `test_write_manifest_exclusive_and_hashes` | test | `test_write_manifest_exclusive_and_hashes` | [tests/c2_readout/test_b_lineage.py:255](../../tests/c2_readout/test_b_lineage.py#L255) |  |
| `test_write_sealed_never_overwrites` | test | `test_write_sealed_never_overwrites` | [tests/k4b/test_b_flow.py:119](../../tests/k4b/test_b_flow.py#L119) |  |
| `test_wrong_type_follows_pinned_strictness` | test | `test_wrong_type_follows_pinned_strictness` | [tests/k4b/test_b_h1_meta.py:204](../../tests/k4b/test_b_h1_meta.py#L204) |  |
| `test_X02_missing_gate_blocks` | test | `test_X02_missing_gate_blocks` | [tests/experiment/test_runner.py:66](../../tests/experiment/test_runner.py#L66) |  |
| `test_X02_required_stage_needs_every_gate` | test | `test_X02_required_stage_needs_every_gate` | [tests/experiment/test_runner.py:56](../../tests/experiment/test_runner.py#L56) |  |
| `test_X07_prereg_refuses_to_overwrite` | test | `test_X07_prereg_refuses_to_overwrite` | [tests/experiment/test_runner.py:146](../../tests/experiment/test_runner.py#L146) |  |
| `test_X08_run_rule_all_runs_pass_is_supported` | test | `test_X08_run_rule_all_runs_pass_is_supported` | [tests/experiment/test_x4.py:162](../../tests/experiment/test_x4.py#L162) |  |
| `test_X08_run_rule_exactly_min_passes_is_supported` | test | `test_X08_run_rule_exactly_min_passes_is_supported` | [tests/experiment/test_x4.py:169](../../tests/experiment/test_x4.py#L169) |  |
| `test_X08_run_rule_failed_gate_beats_failed_count` | test | `test_X08_run_rule_failed_gate_beats_failed_count` | [tests/experiment/test_x4.py:189](../../tests/experiment/test_x4.py#L189) |  |
| `test_X08_run_rule_failed_gate_is_inconclusive_with_reason` | test | `test_X08_run_rule_failed_gate_is_inconclusive_with_reason` | [tests/experiment/test_x4.py:181](../../tests/experiment/test_x4.py#L181) |  |
| `test_X08_run_rule_one_run_below_min_is_rejected` | test | `test_X08_run_rule_one_run_below_min_is_rejected` | [tests/experiment/test_x4.py:174](../../tests/experiment/test_x4.py#L174) |  |
| `test_X08_run_rule_replicate_with_one_world_is_inconclusive` | test | `test_X08_run_rule_replicate_with_one_world_is_inconclusive` | [tests/experiment/test_x4.py:203](../../tests/experiment/test_x4.py#L203) |  |
| `test_X08_run_rule_two_of_three_replicates_is_inconclusive` | test | `test_X08_run_rule_two_of_three_replicates_is_inconclusive` | [tests/experiment/test_x4.py:196](../../tests/experiment/test_x4.py#L196) |  |
| `test_X08_x4c_category` | test | `test_X08_x4c_category` | [tests/experiment/test_x4.py:149](../../tests/experiment/test_x4.py#L149) |  |
| `test_X09_grains_of_the_rows` | test | `test_X09_grains_of_the_rows` | [tests/experiment/test_x4.py:279](../../tests/experiment/test_x4.py#L279) |  |
| `test_X09_n_run_only_contributes_sh1_and_check` | test | `test_X09_n_run_only_contributes_sh1_and_check` | [tests/experiment/test_x4.py:333](../../tests/experiment/test_x4.py#L333) |  |
| `test_X09_x4job_writes_expected_rows` | test | `test_X09_x4job_writes_expected_rows` | [tests/experiment/test_x4.py:213](../../tests/experiment/test_x4.py#L213) |  |
| `test_X10_rerun_returns_same_id` | test | `test_X10_rerun_returns_same_id` | [tests/experiment/test_x4.py:350](../../tests/experiment/test_x4.py#L350) |  |
| `test_X11_missing_run_is_not_run_and_verdicts_inconclusive` | test | `test_X11_missing_run_is_not_run_and_verdicts_inconclusive` | [tests/experiment/test_x4.py:365](../../tests/experiment/test_x4.py#L365) |  |
| `test_X12_x4_registered_with_requires_s4_and_no_gates` | test | `test_X12_x4_registered_with_requires_s4_and_no_gates` | [tests/experiment/test_x4.py:394](../../tests/experiment/test_x4.py#L394) |  |
| `test_X13_missing_record_says_not_run` | test | `test_X13_missing_record_says_not_run` | [tests/experiment/test_report_x4.py:32](../../tests/experiment/test_report_x4.py#L32) |  |
| `test_X13_quotes_prereg_interpretation_and_addendum` | test | `test_X13_quotes_prereg_interpretation_and_addendum` | [tests/experiment/test_report_x4.py:41](../../tests/experiment/test_report_x4.py#L41) |  |
| `test_X14_empty_store_says_not_run` | test | `test_X14_empty_store_says_not_run` | [tests/experiment/test_report_e3.py:60](../../tests/experiment/test_report_e3.py#L60) |  |
| `test_X14_rejected_h3_is_read_one_sided` | test | `test_X14_rejected_h3_is_read_one_sided` | [tests/experiment/test_report_e3.py:71](../../tests/experiment/test_report_e3.py#L71) |  |
| `test_X15_dynamics_table_and_figures` | test | `test_X15_dynamics_table_and_figures` | [tests/experiment/test_report_e3.py:79](../../tests/experiment/test_report_e3.py#L79) |  |
| `test_X16_s6_plan_includes_x4curves_and_p_after_s5` | test | `test_X16_s6_plan_includes_x4curves_and_p_after_s5` | [tests/experiment/test_report_e3.py:108](../../tests/experiment/test_report_e3.py#L108) |  |
| `test_X16_x4_section_p_wording` | test | `test_X16_x4_section_p_wording` | [tests/experiment/test_report_e3.py:90](../../tests/experiment/test_report_e3.py#L90) |  |
| `test_X17_plan_missing_s6_raises_missing_parent` | test | `test_X17_plan_missing_s6_raises_missing_parent` | [tests/experiment/test_s7.py:69](../../tests/experiment/test_s7.py#L69) |  |
| `test_X17_plan_order_with_s6_records` | test | `test_X17_plan_order_with_s6_records` | [tests/experiment/test_s7.py:81](../../tests/experiment/test_s7.py#L81) |  |
| `test_X17_registry_requires_and_gates` | test | `test_X17_registry_requires_and_gates` | [tests/experiment/test_s7.py:63](../../tests/experiment/test_s7.py#L63) |  |
| `test_X18_gate_gg_failed_run_record_counts_as_documented` | test | `test_X18_gate_gg_failed_run_record_counts_as_documented` | [tests/experiment/test_s7.py:116](../../tests/experiment/test_s7.py#L116) |  |
| `test_X18_gate_gg_fails_for_missing_job_record` | test | `test_X18_gate_gg_fails_for_missing_job_record` | [tests/experiment/test_s7.py:123](../../tests/experiment/test_s7.py#L123) |  |
| `test_X18_gate_gg_fails_for_undocumented_run` | test | `test_X18_gate_gg_fails_for_undocumented_run` | [tests/experiment/test_s7.py:107](../../tests/experiment/test_s7.py#L107) |  |
| `test_X18_gate_gg_passes_when_all_documented` | test | `test_X18_gate_gg_passes_when_all_documented` | [tests/experiment/test_s7.py:94](../../tests/experiment/test_s7.py#L94) |  |
| `test_X19_failed_run_is_recorded_not_raised` | test | `test_X19_failed_run_is_recorded_not_raised` | [tests/experiment/test_s7.py:132](../../tests/experiment/test_s7.py#L132) |  |
| `test_X19_non_stagefailure_exception_uses_type_name` | test | `test_X19_non_stagefailure_exception_uses_type_name` | [tests/experiment/test_s7.py:155](../../tests/experiment/test_s7.py#L155) |  |
| `test_x1_and_t_pre_cannot_write_endpoint_arrays` | test | `test_x1_and_t_pre_cannot_write_endpoint_arrays` | [tests/c2_readout/test_b_policy.py:111](../../tests/c2_readout/test_b_policy.py#L111) |  |
| `test_x1_attainability_product_form_exact` | test | `test_x1_attainability_product_form_exact` | [tests/c2_readout/test_b_patch.py:303](../../tests/c2_readout/test_b_patch.py#L303) |  |
| `test_x1_closed_form_equals_patch_path_and_returns_diagnostics_only` | test | `test_x1_closed_form_equals_patch_path_and_returns_diagnostics_only` | [tests/c2_readout/test_b_patch.py:215](../../tests/c2_readout/test_b_patch.py#L215) |  |
| `test_x1_fail_closed_on_one_row_and_tolerance_is_relative` | test | `test_x1_fail_closed_on_one_row_and_tolerance_is_relative` | [tests/c2_readout/test_b_patch.py:261](../../tests/c2_readout/test_b_patch.py#L261) |  |
| `test_x1_injected_defect_fails_by_1e6_tau` | test | `test_x1_injected_defect_fails_by_1e6_tau` | [tests/c2_readout/test_b_patch.py:248](../../tests/c2_readout/test_b_patch.py#L248) |  |
| `test_x1_non_finite_replacement_is_fail_closed` | test | `test_x1_non_finite_replacement_is_fail_closed` | [tests/c2_readout/test_b_patch.py:273](../../tests/c2_readout/test_b_patch.py#L273) |  |
| `test_x1_signature_has_no_store_access` | test | `test_x1_signature_has_no_store_access` | [tests/c2_readout/test_b_patch.py:211](../../tests/c2_readout/test_b_patch.py#L211) |  |
| `test_x1_trigger_condition` | test | `test_x1_trigger_condition` | [tests/hws/test_a_classify.py:310](../../tests/hws/test_a_classify.py#L310) |  |
| `test_x1_trigger_ties_ineligible_and_empty` | test | `test_x1_trigger_ties_ineligible_and_empty` | [tests/hws/test_a_classify.py:323](../../tests/hws/test_a_classify.py#L323) |  |
| `test_x1_world_counts_and_order` | test | `test_x1_world_counts_and_order` | [tests/hws/test_b_worlds.py:116](../../tests/hws/test_b_worlds.py#L116) |  |
| `test_x1_worlds_counts_and_order` | test | `test_x1_worlds_counts_and_order` | [tests/hws/test_a_classify.py:380](../../tests/hws/test_a_classify.py#L380) |  |
| `test_X20_circular_summary_known_answer` | test | `test_X20_circular_summary_known_answer` | [tests/experiment/test_s7.py:174](../../tests/experiment/test_s7.py#L174) |  |
| `test_X20_probe_recovers_planted_map_and_lambda_uses_val_rows_only` | test | `test_X20_probe_recovers_planted_map_and_lambda_uses_val_rows_only` | [tests/experiment/test_s7.py:210](../../tests/experiment/test_s7.py#L210) |  |
| `test_X20_probe_shuffled_labels_give_low_r2` | test | `test_X20_probe_shuffled_labels_give_low_r2` | [tests/experiment/test_s7.py:241](../../tests/experiment/test_s7.py#L241) |  |
| `test_X21_on_test_split_distinguishes_dev_and_test` | test | `test_X21_on_test_split_distinguishes_dev_and_test` | [tests/experiment/test_s7.py:267](../../tests/experiment/test_s7.py#L267) |  |
| `test_X22_artifact_absent_from_main_is_missing` | test | `test_X22_artifact_absent_from_main_is_missing` | [tests/experiment/test_s8_e4.py:87](../../tests/experiment/test_s8_e4.py#L87) |  |
| `test_X22_gate_reports_compared_by_gate_and_verdict_only` | test | `test_X22_gate_reports_compared_by_gate_and_verdict_only` | [tests/experiment/test_s8_e4.py:132](../../tests/experiment/test_s8_e4.py#L132) |  |
| `test_X22_identical_stores_ok_and_every_type_counted` | test | `test_X22_identical_stores_ok_and_every_type_counted` | [tests/experiment/test_s8_e4.py:60](../../tests/experiment/test_s8_e4.py#L60) |  |
| `test_X22_run_timing_differs_only_in_timing_rows_is_equal` | test | `test_X22_run_timing_differs_only_in_timing_rows_is_equal` | [tests/experiment/test_s8_e4.py:100](../../tests/experiment/test_s8_e4.py#L100) |  |
| `test_X22_run_timing_with_other_row_differing_is_mismatch` | test | `test_X22_run_timing_with_other_row_differing_is_mismatch` | [tests/experiment/test_s8_e4.py:115](../../tests/experiment/test_s8_e4.py#L115) |  |
| `test_X22_same_id_different_payload_is_checksum_mismatch` | test | `test_X22_same_id_different_payload_is_checksum_mismatch` | [tests/experiment/test_s8_e4.py:76](../../tests/experiment/test_s8_e4.py#L76) |  |
| `test_X22_untimed_kind_differing_in_wall_time_is_mismatch` | test | `test_X22_untimed_kind_differing_in_wall_time_is_mismatch` | [tests/experiment/test_s8_e4.py:125](../../tests/experiment/test_s8_e4.py#L125) |  |
| `test_X23_intact_store_ok_with_n_equal_n_verified` | test | `test_X23_intact_store_ok_with_n_equal_n_verified` | [tests/experiment/test_s8_e4.py:149](../../tests/experiment/test_s8_e4.py#L149) |  |
| `test_X23_missing_parent_is_reported` | test | `test_X23_missing_parent_is_reported` | [tests/experiment/test_s8_e4.py:161](../../tests/experiment/test_s8_e4.py#L161) |  |
| `test_X24_rerun_job_rejects_s3_runs_differing_from_identity_check` | test | `test_X24_rerun_job_rejects_s3_runs_differing_from_identity_check` | [tests/experiment/test_s8_e4.py:199](../../tests/experiment/test_s8_e4.py#L199) |  |
| `test_X24_s8_registered_with_requires_and_gate` | test | `test_X24_s8_registered_with_requires_and_gate` | [tests/experiment/test_s8_e4.py:181](../../tests/experiment/test_s8_e4.py#L181) |  |
| `test_X25_circular_table_hand_computed` | test | `test_X25_circular_table_hand_computed` | [tests/experiment/test_s8_e4.py:244](../../tests/experiment/test_s8_e4.py#L244) |  |
| `test_X25_empty_store_prints_not_run_and_invents_nothing` | test | `test_X25_empty_store_prints_not_run_and_invents_nothing` | [tests/experiment/test_s8_e4.py:211](../../tests/experiment/test_s8_e4.py#L211) |  |
| `test_X25_failed_control_run_prints_failed_reason` | test | `test_X25_failed_control_run_prints_failed_reason` | [tests/experiment/test_s8_e4.py:279](../../tests/experiment/test_s8_e4.py#L279) |  |
| `test_X25_probe_table_hand_computed` | test | `test_X25_probe_table_hand_computed` | [tests/experiment/test_s8_e4.py:231](../../tests/experiment/test_s8_e4.py#L231) |  |
| `test_X25_sensitivity_table_hand_computed` | test | `test_X25_sensitivity_table_hand_computed` | [tests/experiment/test_s8_e4.py:263](../../tests/experiment/test_s8_e4.py#L263) |  |
| `test_x6_source_binding_and_history_arrays` | test | `test_x6_source_binding_and_history_arrays` | [tests/c2_readout/test_b_registry.py:248](../../tests/c2_readout/test_b_registry.py#L248) |  |
| `test_x_interval_and_verdict_rule` | test | `test_x_interval_and_verdict_rule` | [tests/chart_diag/test_chart_diag.py:38](../../tests/chart_diag/test_chart_diag.py#L38) |  |
| `test_y2_activity_and_resp_in_the_m_stream` | test | `test_y2_activity_and_resp_in_the_m_stream` | [tests/c2_readout/test_b_screens.py:334](../../tests/c2_readout/test_b_screens.py#L334) |  |
| `test_y_donor_map_and_off_grid_rows` | test | `test_y_donor_map_and_off_grid_rows` | [tests/c2_readout/test_b_registry.py:109](../../tests/c2_readout/test_b_registry.py#L109) |  |
| `test_y_donor_preparation_from_the_cached_natural_oracle` | test | `test_y_donor_preparation_from_the_cached_natural_oracle` | [tests/c2_readout/test_b_registry.py:363](../../tests/c2_readout/test_b_registry.py#L363) |  |
| `test_y_donor_preparation_order_new10` | test | `test_y_donor_preparation_order_new10` | [tests/c2_readout/test_b_policy.py:191](../../tests/c2_readout/test_b_policy.py#L191) |  |
| `test_y_donor_shifts_the_symbol_row_and_keeps_column_and_w32` | test | `test_y_donor_shifts_the_symbol_row_and_keeps_column_and_w32` | [tests/c2_readout/test_a_oracle.py:117](../../tests/c2_readout/test_a_oracle.py#L117) |  |
| `test_y_marginal_m32_and_nuisance` | test | `test_y_marginal_m32_and_nuisance` | [tests/c1prime/test_a_eligibility_support.py:98](../../tests/c1prime/test_a_eligibility_support.py#L98) |  |
| `test_y_rot_rotates_the_code_and_holds_every_other_coordinate` | test | `test_y_rot_rotates_the_code_and_holds_every_other_coordinate` | [tests/c2_readout/test_a_oracle.py:273](../../tests/c2_readout/test_a_oracle.py#L273) |  |
| `test_Y_Z_Zfull_kernels_follow_C5_and_C6_bitwise` | test | `test_Y_Z_Zfull_kernels_follow_C5_and_C6_bitwise` | [tests/c1prime/test_b_identities.py:259](../../tests/c1prime/test_b_identities.py#L259) |  |
| `test_z_b23_constant` | test | `test_z_b23_constant` | [tests/hwsb/test_a_learning.py:296](../../tests/hwsb/test_a_learning.py#L296) |  |
| `test_z_constants` | test | `test_z_constants` | [tests/hws/test_a_stats.py:72](../../tests/hws/test_a_stats.py#L72) |  |
| `test_zero_code_threshold_and_override` | test | `test_zero_code_threshold_and_override` | [tests/c2_readout/test_b_screens.py:113](../../tests/c2_readout/test_b_screens.py#L113) |  |
| `test_zero_contrast_is_not_positive` | test | `test_zero_contrast_is_not_positive` | [tests/analysis/test_f1_rule.py:139](../../tests/analysis/test_f1_rule.py#L139) |  |
| `test_zero_contrast_prediction_is_not_reproduced` | test | `test_zero_contrast_prediction_is_not_reproduced` | [tests/d2a/test_b_behaviour.py:83](../../tests/d2a/test_b_behaviour.py#L83) |  |
| `test_zero_identity_exact_for_rational_suffix_functions` | test | `test_zero_identity_exact_for_rational_suffix_functions` | [tests/circle_history/test_scores_precision.py:219](../../tests/circle_history/test_scores_precision.py#L219) |  |
| `test_zero_identity_exact_for_the_three_controls` | test | `test_zero_identity_exact_for_the_three_controls` | [tests/circle_history/test_scores_precision.py:231](../../tests/circle_history/test_scores_precision.py#L231) |  |
| `test_zero_identity_exact_per_suffix` | test | `test_zero_identity_exact_per_suffix` | [tests/circle_history/test_scores_precision.py:200](../../tests/circle_history/test_scores_precision.py#L200) | sum_prefix P(prefix + s) (P_L - P_k(s)) == 0 for every suffix s: by linearity this is the |
| `test_zero_identity_float_controls_within_1e12` | test | `test_zero_identity_float_controls_within_1e12` | [tests/circle_history/test_scores_precision.py:241](../../tests/circle_history/test_scores_precision.py#L241) |  |
| `test_zero_patch_contrast_and_scores` | test | `test_zero_patch_contrast_and_scores` | [tests/c1prime/test_b_identities.py:278](../../tests/c1prime/test_b_identities.py#L278) |  |
| `test_zero_perturbation_gives_zero_bound_and_zero_gap` | test | `test_zero_perturbation_gives_zero_bound_and_zero_gap` | [tests/k4b/test_a_lemma_t.py:164](../../tests/k4b/test_a_lemma_t.py#L164) |  |
| `test_zero_variance_validation_target_status` | test | `test_zero_variance_validation_target_status` | [tests/experiment/test_x4f_probe.py:170](../../tests/experiment/test_x4f_probe.py#L170) |  |
| `text` | function | `text` | [tests/k4b/test_b_store_reader.py:56](../../tests/k4b/test_b_store_reader.py#L56) |  |
| `theta` | function | `theta` | [tools/c2_readout/c2_stats.py:84](../../tools/c2_readout/c2_stats.py#L84) | theta_q = q u_D / (1 - q u_D), u_D = 1/2 10^(1 - p) at the active precision p. |
| `threshold_arrays` | function | `threshold_arrays` | [tools/c2_readout/c2_attrib.py:260](../../tools/c2_readout/c2_attrib.py#L260) | Z010, Z050, Vabs, Vrand of one pair() result (x pair, E_x). |
| `threshold_law` | function | `threshold_law` | [tools/x4_circle_history/process_law.py:147](../../tools/x4_circle_history/process_law.py#L147) | Exact law of j = min(#{i: c'_i <= u}, V-1) for u on the 2^-53 grid, c' clamped to [0, 1]. |
| `through_oracle` | function | `through_oracle` | [tests/circle_history/test_builder_v24_stages.py:76](../../tests/circle_history/test_builder_v24_stages.py#L76) |  |
| `tier` | function | `tier` | [tools/hws/hws_worlds.py:112](../../tools/hws/hws_worlds.py#L112) |  |
| `tier_of` | function | `tier_of` | [tests/hws/test_a_classify.py:72](../../tests/hws/test_a_classify.py#L72) |  |
| `timed` | function | `timed` | [src/topo_pilot/experiment/s8.py:80](../../src/topo_pilot/experiment/s8.py#L80) | MetricRecords whose rows include measured wall time or throughput. |
| `timed_factory` | function | `timed_factory` | [tools/x4_circle_history/op_guard.py:38](../../tools/x4_circle_history/op_guard.py#L38) |  |
| `tiny` | function | `tiny` | [tests/c2_readout/test_b_patch.py:70](../../tests/c2_readout/test_b_patch.py#L70) |  |
| `tiny` | function | `tiny` | [tests/experiment/test_x4f_gates_smoke.py:18](../../tests/experiment/test_x4f_gates_smoke.py#L18) |  |
| `tiny` | function | `tiny` | [tests/hws/test_b_exact.py:67](../../tests/hws/test_b_exact.py#L67) |  |
| `tiny` | function | `tiny` | [tests/hws/test_b_oracle.py:38](../../tests/hws/test_b_oracle.py#L38) |  |
| `tiny_cfg` | function | `tiny_cfg` | [tests/dataset/conftest.py:19](../../tests/dataset/conftest.py#L19) |  |
| `tiny_ds` | function | `tiny_ds` | [tests/learner/conftest.py:19](../../tests/learner/conftest.py#L19) |  |
| `tiny_hmm` | function | `tiny_hmm` | [src/topo_pilot/contracts/testing.py:63](../../src/topo_pilot/contracts/testing.py#L63) | A hand-chosen 4-state, 3-symbol HMM: ``(T [4,4], E [4,3], pi [4])``. |
| `tiny_index` | function | `tiny_index` | [tests/activations/conftest.py:91](../../tests/activations/conftest.py#L91) |  |
| `tiny_model` | function | `tiny_model` | [tests/activations/conftest.py:61](../../tests/activations/conftest.py#L61) |  |
| `tiny_obs` | function | `tiny_obs` | [tests/activations/conftest.py:86](../../tests/activations/conftest.py#L86) |  |
| `tiny_obs` | function | `tiny_obs` | [tests/learner/conftest.py:14](../../tests/learner/conftest.py#L14) |  |
| `tiny_observations` | function | `tiny_observations` | [src/topo_pilot/contracts/testing.py:82](../../src/topo_pilot/contracts/testing.py#L82) | ``R`` test-split trajectories of 33 symbols sampled from :func:`tiny_hmm`. |
| `tiny_plan` | function | `tiny_plan` | [tests/hwsb/test_b_e4path.py:89](../../tests/hwsb/test_b_e4path.py#L89) |  |
| `tiny_proc` | function | `tiny_proc` | [tests/hwsb/test_b_streams.py:271](../../tests/hwsb/test_b_streams.py#L271) |  |
| `tiny_world_spec` | function | `tiny_world_spec` | [src/topo_pilot/contracts/testing.py:22](../../src/topo_pilot/contracts/testing.py#L22) | An ``n x n`` square or cylinder (axis 0 periodic) built by direct enumeration. |
| `to_arrays` | function | `to_arrays` | [tools/k4b/k4b_decoder.py:96](../../tools/k4b/k4b_decoder.py#L96) |  |
| `to_canonical` | function | `to_canonical` | [tools/hwsb/hwsb_eval.py:54](../../tools/hwsb/hwsb_eval.py#L54) |  |
| `to_decimal` | function | `to_decimal` | [tools/x6_stage0/x6_dp.py:80](../../tools/x6_stage0/x6_dp.py#L80) |  |
| `to_float` | function | `to_float` | [tools/x6_stage0/x6_model.py:168](../../tools/x6_stage0/x6_model.py#L168) |  |
| `to_json_dict` | method | `ArtifactMeta.to_json_dict` | [src/topo_pilot/contracts/base.py:49](../../src/topo_pilot/contracts/base.py#L49) | Plain-JSON form for ``meta.json``. |
| `to_named` | function | `to_named` | [tests/c1prime/test_a_oracle_named.py:84](../../tests/c1prime/test_a_oracle_named.py#L84) |  |
| `to_payload` | method | `Artifact.to_payload` | [src/topo_pilot/contracts/base.py:125](../../src/topo_pilot/contracts/base.py#L125) | Split the artifact into ``(arrays, extra)``; blob fields appear in ``arrays`` as |
| `tok` | function | `tok` | [tests/x6_stage0/test_x6_stage0.py:70](../../tests/x6_stage0/test_x6_stage0.py#L70) |  |
| `tok` | function | `tok` | [tools/x6_stage0/x6_model.py:72](../../tools/x6_stage0/x6_model.py#L72) |  |
| `token` | function | `token` | [tools/x2a_stage0/x2a_model.py:51](../../tools/x2a_stage0/x2a_model.py#L51) |  |
| `token_digest` | function | `token_digest` | [tools/x6_stage1/x6s1_data.py:232](../../tools/x6_stage1/x6s1_data.py#L232) |  |
| `token_sources` | function | `token_sources` | [tools/c2_readout/c2_registry.py:132](../../tools/c2_readout/c2_registry.py#L132) | Readers a, b, c, d, e, k through the reused K4b/C1' functions; failures become problems |
| `tokens` | function | `tokens` | [tests/d2a/test_b_targets.py:97](../../tests/d2a/test_b_targets.py#L97) | 64 natural C/M episodes plus the padded canonical pair (w_12..w_33 = sigma0, so p = 33 |
| `tokens_hash` | function | `tokens_hash` | [src/topo_pilot/contracts/ids.py:87](../../src/topo_pilot/contracts/ids.py#L87) | Hash of a token history ``w_1..w_p``: ``sha1(int64 little-endian bytes)[:16]``. |
| `tol` | function | `tol` | [tools/c1prime/c1_oracle.py:34](../../tools/c1prime/c1_oracle.py#L34) |  |
| `ToleranceRow` | class | `ToleranceRow` | [src/topo_pilot/analysis/horizon.py:97](../../src/topo_pilot/analysis/horizon.py#L97) | Tangent audit at one relative tolerance ``tau`` (see :func:`tangent_audit`). |
| `tool_line` | function | `tool_line` | [src/topo_pilot/experiment/stages.py:61](../../src/topo_pilot/experiment/stages.py#L61) | Last output line of a tool run, with pytest's wall time removed (``95 passed in 3.7s`` |
| `top_dim` | method | `CubicalComplex.top_dim` | [src/topo_pilot/world/complex.py:152](../../src/topo_pilot/world/complex.py#L152) | Highest cell dimension K. |
| `top_k_persistence` | method | `Summaries.top_k_persistence` | [src/topo_pilot/topology/summaries.py:42](../../src/topo_pilot/topology/summaries.py#L42) | The ``k`` largest finite persistences in ``dim``, decreasing, zero padded to ``[k]``. |
| `topo` | function | `topo` | [tools/theory_exact/theory_exact2.py:119](../../tools/theory_exact/theory_exact2.py#L119) |  |
| `torch_threads` | function | `torch_threads` | [src/topo_pilot/experiment/s3.py:56](../../src/topo_pilot/experiment/s3.py#L56) | Thread count from ``device_policy.torch_threads``: ``physical_cores`` or an integer. |
| `torch_versions` | function | `torch_versions` | [tools/hwsb/hwsb_train.py:70](../../tools/hwsb/hwsb_train.py#L70) |  |
| `total_mass` | function | `total_mass` | [tools/x6_stage0/x6_dp.py:68](../../tools/x6_stage0/x6_dp.py#L68) |  |
| `total_spent` | function | `total_spent` | [tools/d2a/d2a_train.py:159](../../tools/d2a/d2a_train.py#L159) |  |
| `tpre` | function | `tpre` | [tools/c1prime/c1_driver_fresh.py:46](../../tools/c1prime/c1_driver_fresh.py#L46) |  |
| `tracked_files` | function | `tracked_files` | [tools/check_file_sizes.py:33](../../tools/check_file_sizes.py#L33) |  |
| `tracked_files` | function | `tracked_files` | [tools/check_state_files.py:42](../../tools/check_state_files.py#L42) |  |
| `train` | function | `train` | [tools/hwsb/hwsb_train.py:265](../../tools/hwsb/hwsb_train.py#L265) | LearnerStage.run, composed: same loads, datasets, Trainer and checkpoint identities. |
| `train_cfg` | function | `train_cfg` | [tests/learner/conftest.py:29](../../tests/learner/conftest.py#L29) |  |
| `train_chunk` | function | `train_chunk` | [tools/x6_stage1/x6s1_cloud.py:175](../../tools/x6_stage1/x6s1_cloud.py#L175) |  |
| `train_chunked` | function | `train_chunked` | [tools/x6_stage1/x6s1_cloud.py:327](../../tools/x6_stage1/x6s1_cloud.py#L327) |  |
| `train_config` | function | `train_config` | [tools/d2a/d2a_train.py:49](../../tools/d2a/d2a_train.py#L49) |  |
| `train_core` | function | `train_core` | [tools/hwsb/hwsb_stages.py:34](../../tools/hwsb/hwsb_stages.py#L34) | make_train_dev, then ht.train; TRAIN_RECORD.json (also written on a stop). |
| `train_dev_canonical` | function | `train_dev_canonical` | [tools/hwsb/hwsb_registry.py:34](../../tools/hwsb/hwsb_registry.py#L34) |  |
| `train_equiv` | function | `train_equiv` | [tools/x6_stage1/x6s1_run.py:468](../../tools/x6_stage1/x6s1_run.py#L468) | §4.6 TRAIN-EQUIV: chunked training (K = 20, two fresh-process resumes) = Trainer.fit. |
| `train_known` | function | `train_known` | [tools/hwsb/hwsb_train.py:286](../../tools/hwsb/hwsb_train.py#L286) | KB2/KB3: in-memory ObservationSets, stopped by a sentinel; nothing persisted. |
| `train_one` | function | `train_one` | [src/topo_pilot/experiment/x5g1t_train.py:74](../../src/topo_pilot/experiment/x5g1t_train.py#L74) | Train one model under a run lock; always record COMPLETE or INCOMPLETE, then re-raise. |
| `TrainConfig` | class | `TrainConfig` | [src/topo_pilot/learner/config.py:33](../../src/topo_pilot/learner/config.py#L33) | Optimisation hyper-parameters (RESEARCH_SUMMARY section 6). |
| `trained` | function | `trained` | [tests/experiment/test_x5g1t_identity_eval.py:156](../../tests/experiment/test_x5g1t_identity_eval.py#L156) |  |
| `trained` | function | `trained` | [tests/hwsb/test_b_e4path.py:118](../../tests/hwsb/test_b_e4path.py#L118) |  |
| `trained_root` | function | `trained_root` | [tests/experiment/test_x5g1t_integration.py:106](../../tests/experiment/test_x5g1t_integration.py#L106) |  |
| `Trainer` | class | `Trainer` | [src/topo_pilot/learner/trainer.py:75](../../src/topo_pilot/learner/trainer.py#L75) | Trains a ``TransformerLM`` on public tokens only. |
| `trainer_init` | function | `trainer_init` | [tests/x6_stage1/test_b_train_chain.py:176](../../tests/x6_stage1/test_b_train_chain.py#L176) |  |
| `TrainingProcess` | class | `TrainingProcess` | [tools/d2a/process_tree.py:34](../../tools/d2a/process_tree.py#L34) | Popen-compatible training handle with accounting for launcher and descendants. |
| `TrainingRun` | class | `TrainingRun` | [src/topo_pilot/experiment/s3.py:133](../../src/topo_pilot/experiment/s3.py#L133) | Train one model (or reuse a stored run) and extract its activations. |
| `TrainingStageBase` | class | `TrainingStageBase` | [src/topo_pilot/experiment/s4.py:41](../../src/topo_pilot/experiment/s4.py#L41) | Shared plan/execute for S4 and S5. |
| `TrainSummary` | class | `TrainSummary` | [src/topo_pilot/learner/trainer.py:26](../../src/topo_pilot/learner/trainer.py#L26) | Outcome of ``Trainer.fit``. |
| `transfer_check` | function | `transfer_check` | [tools/x6_stage1/x6s1_ingest.py:191](../../tools/x6_stage1/x6s1_ingest.py#L191) | WEIGHTS-HASH (a)-(b) for the whole snapshot: (manifest or None, problems). |
| `TransformerLM` | class | `TransformerLM` | [src/topo_pilot/learner/model.py:69](../../src/topo_pilot/learner/model.py#L69) | Decoder-only, pre-LN, learned positional embeddings, final LN, untied unembedding. |
| `transition` | function | `transition` | [tools/theory_exact/sym_check.py:28](../../tools/theory_exact/sym_check.py#L28) |  |
| `TransitionBuilder` | class | `TransitionBuilder` | [src/topo_pilot/process/transition.py:46](../../src/topo_pilot/process/transition.py#L46) | Builds ``TransitionSpec`` from a world; never sees an emission matrix. |
| `TransitionConfig` | class | `TransitionConfig` | [src/topo_pilot/process/transition.py:16](../../src/topo_pilot/process/transition.py#L16) | Config of the transition kernel: ``kind`` and the self-loop floor ``p_stay`` in [0, 1). |
| `TransitionSpec` | class | `TransitionSpec` | [src/topo_pilot/contracts/_schemas_world.py:126](../../src/topo_pilot/contracts/_schemas_world.py#L126) | Transition kernel ``T[i, j] = P(z_{t+1} = j \| z_t = i)`` (``[N, N] float64``) and ``pi [N]``. |
| `translate_states` | function | `translate_states` | [tools/hws/hws_worlds.py:295](../../tools/hws/hws_worlds.py#L295) |  |
| `transport_bound` | function | `transport_bound` | [tools/k4b/k4b_cert.py:158](../../tools/k4b/k4b_cert.py#L158) |  |
| `trap_checks` | function | `trap_checks` | [tools/x4_oracle_profile/validation.py:162](../../tools/x4_oracle_profile/validation.py#L162) | Wrong symbol mapping and an extra trailing transition must be detectable on real rows. |
| `trapping_context` | function | `trapping_context` | [tools/x4_circle_history/error_bound.py:54](../../tools/x4_circle_history/error_bound.py#L54) |  |
| `tree` | function | `tree` | [tools/x4_oracle_profile/freeze.py:71](../../tools/x4_oracle_profile/freeze.py#L71) |  |
| `tree_digest` | function | `tree_digest` | [tools/x4_circle_history/env_identity.py:99](../../tools/x4_circle_history/env_identity.py#L99) | sha256 over sorted 'relpath:sha256' lines (a file: its own sha256). |
| `tree_lines` | function | `tree_lines` | [tools/code_index/render_deps.py:44](../../tools/code_index/render_deps.py#L44) |  |
| `tree_mean` | function | `tree_mean` | [tools/c1prime/c1_means.py:15](../../tools/c1prime/c1_means.py#L15) | Mean over the last axis: adjacent pairs added level by level (an unmatched last entry is |
| `tree_mean_ref` | function | `tree_mean_ref` | [tests/hwsb/test_a_endpoints.py:50](../../tests/hwsb/test_a_endpoints.py#L50) | Own balanced-tree mean: adjacent pairs level by level (odd last entry carried), / n. |
| `tree_sha` | function | `tree_sha` | [tools/hws/hws_records.py:74](../../tools/hws/hws_records.py#L74) |  |
| `triangle_sums` | function | `triangle_sums` | [tests/circle_history/test_chart.py:95](../../tests/circle_history/test_chart.py#L95) |  |
| `triangle_sums` | function | `triangle_sums` | [tests/circle_history/test_cochain.py:54](../../tests/circle_history/test_cochain.py#L54) | Explicit c(j,k) - c(i,k) + c(i,j) for every triangle, as Python ints. |
| `triangle_sums` | function | `triangle_sums` | [tests/circle_history/test_cochain_chart_v24.py:69](../../tests/circle_history/test_cochain_chart_v24.py#L69) |  |
| `triangle_sums` | function | `triangle_sums` | [tests/circle_history/test_cochain_lift.py:65](../../tests/circle_history/test_cochain_lift.py#L65) | Explicit c(j,k) - c(i,k) + c(i,j) for every triangle, as Python ints. |
| `triangle_system` | function | `triangle_system` | [tools/x4_circle_history/cochain.py:38](../../tools/x4_circle_history/cochain.py#L38) | D1 (int64 sparse [T, E]) and triangles (int64 [T, 3]) of the clique 2-skeleton. |
| `truncated` | function | `truncated` | [tests/k4b/test_b_registry_rules.py:77](../../tests/k4b/test_b_registry_rules.py#L77) |  |
| `tv` | function | `tv` | [tests/d1_seam/test_d1_seam.py:62](../../tests/d1_seam/test_d1_seam.py#L62) |  |
| `tv` | function | `tv` | [tools/d1_seam/d1_seam.py:116](../../tools/d1_seam/d1_seam.py#L116) |  |
| `tv_histories` | function | `tv_histories` | [tests/k4b/test_a_lemma_t.py:83](../../tests/k4b/test_a_lemma_t.py#L83) |  |
| `two` | function | `two` | [tests/k4b/test_b_endpoint.py:121](../../tests/k4b/test_b_endpoint.py#L121) |  |
| `two_blocks` | function | `two_blocks` | [tests/k4b/test_b_data.py:283](../../tests/k4b/test_b_data.py#L283) |  |
| `two_route` | function | `two_route` | [tools/c2_readout/c2_model.py:192](../../tools/c2_readout/c2_model.py#L192) | M0 SYMBOL-ORDER two-route rule per row (T18, NEW-7). |
| `two_stage_by_hand` | function | `two_stage_by_hand` | [tests/x6_stage1/test_a_numerics.py:246](../../tests/x6_stage1/test_a_numerics.py#L246) |  |
| `two_stage_law` | function | `two_stage_law` | [tools/x6_stage1/x6s1_stats.py:177](../../tools/x6_stage1/x6s1_stats.py#L177) |  |
| `typeset` | function | `typeset` | [reports/he_summary/build.py:85](../../reports/he_summary/build.py#L85) |  |
| `u_context_gain` | function | `u_context_gain` | [src/topo_pilot/experiment/s7.py:58](../../src/topo_pilot/experiment/s7.py#L58) | ``G_U = mean KL(q_C \|\| pi E)`` over the run's final-checkpoint histories (D-047): the |
| `u_digits` | function | `u_digits` | [tools/x4_circle_history/error_bound.py:43](../../tools/x4_circle_history/error_bound.py#L43) |  |
| `unanchored_labels` | function | `unanchored_labels` | [tools/hws/hws_worlds.py:150](../../tools/hws/hws_worlds.py#L150) |  |
| `unfrozen_project_modules` | function | `unfrozen_project_modules` | [tools/x4_circle_history/env_identity.py:129](../../tools/x4_circle_history/env_identity.py#L129) | Loaded modules from this worktree's src/, tools/ or tests/ outside the frozen file set. |
| `Unique` | class | `Unique` | [src/topo_pilot/process/emission.py:203](../../src/topo_pilot/process/emission.py#L203) | U: ``V = N`` and E is a permutation matrix (identity up to symbol names). |
| `unit` | function | `unit` | [tests/d1_seam/test_d1_seam.py:52](../../tests/d1_seam/test_d1_seam.py#L52) |  |
| `unit` | function | `unit` | [tools/c1prime/c1_fit.py:27](../../tools/c1prime/c1_fit.py#L27) |  |
| `unit_columns` | function | `unit_columns` | [tests/circle_history/test_chart.py:101](../../tests/circle_history/test_chart.py#L101) |  |
| `unit_var_rows` | function | `unit_var_rows` | [tests/analysis/test_readout.py:25](../../tests/analysis/test_readout.py#L25) | Random rows rescaled so that each row has population variance exactly 1. |
| `unit_vectors` | function | `unit_vectors` | [tools/x4_circle_history/scores.py:65](../../tools/x4_circle_history/scores.py#L65) |  |
| `Unresolved` | class | `Unresolved` | [tools/x4_circle_history/errors.py:16](../../tools/x4_circle_history/errors.py#L16) | Valid criterion not met, unsupported, or exhausted: the runner reports INCONCLUSIVE. |
| `unseal` | function | `unseal` | [tools/c2_readout/c2_driver.py:161](../../tools/c2_readout/c2_driver.py#L161) |  |
| `unseal` | function | `unseal` | [tools/x6_stage1/x6s1_run.py:263](../../tools/x6_stage1/x6s1_run.py#L263) |  |
| `unsealed` | function | `unsealed` | [tools/c2_readout/c2_stage_val.py:200](../../tools/c2_readout/c2_stage_val.py#L200) | Point values of one opened VAL bundle (secondary; API.md §15.2 val_unsealed). |
| `untimed_digest` | function | `untimed_digest` | [src/topo_pilot/experiment/s8.py:86](../../src/topo_pilot/experiment/s8.py#L86) |  |
| `up` | function | `up` | [tools/c1prime/c1_cert.py:38](../../tools/c1prime/c1_cert.py#L38) |  |
| `upload_cmd` | method | `SSHExecutor.upload_cmd` | [src/topo_pilot/executors/ssh.py:69](../../src/topo_pilot/executors/ssh.py#L69) | ``scp`` of the bundle into ``remote_dir``. |
| `usage` | function | `usage` | [tests/experiment/test_x5g1t_usage.py:42](../../tests/experiment/test_x5g1t_usage.py#L42) |  |
| `usage` | function | `usage` | [tests/experiment/test_x5g1t_usage_files.py:43](../../tests/experiment/test_x5g1t_usage_files.py#L43) |  |
| `usage` | function | `usage` | [tests/oracle_profile/test_builder_controls.py:40](../../tests/oracle_profile/test_builder_controls.py#L40) |  |
| `usage_decision` | function | `usage_decision` | [src/topo_pilot/experiment/x5g1t_usage.py:124](../../src/topo_pilot/experiment/x5g1t_usage.py#L124) |  |
| `usage_of` | function | `usage_of` | [tests/c1prime/test_a_release_meter.py:213](../../tests/c1prime/test_a_release_meter.py#L213) |  |
| `usage_of` | function | `usage_of` | [tests/k4b/test_b_meter.py:265](../../tests/k4b/test_b_meter.py#L265) |  |
| `UsageDecision` | class | `UsageDecision` | [src/topo_pilot/experiment/x5g1t_usage.py:31](../../src/topo_pilot/experiment/x5g1t_usage.py#L31) |  |
| `UsageMalformed` | class | `UsageMalformed` | [src/topo_pilot/experiment/x5g1t_usage.py:27](../../src/topo_pilot/experiment/x5g1t_usage.py#L27) | Malformed usage evidence or latch; callers treat it as STOP (fail closed). |
| `utc` | function | `utc` | [tools/hws/hws_records.py:35](../../tools/hws/hws_records.py#L35) |  |
| `utc` | function | `utc` | [tools/hwsb/hwsb_driver.py:45](../../tools/hwsb/hwsb_driver.py#L45) |  |
| `utc` | function | `utc` | [tools/hwsb/hwsb_records.py:27](../../tools/hwsb/hwsb_records.py#L27) |  |
| `utc_iso` | function | `utc_iso` | [tools/x6_stage1/x6s1_cloud.py:91](../../tools/x6_stage1/x6s1_cloud.py#L91) |  |
| `utc_iso` | function | `utc_iso` | [tools/x6_stage1/x6s1_registry.py:55](../../tools/x6_stage1/x6s1_registry.py#L55) |  |
| `utc_stamp` | function | `utc_stamp` | [tools/x6_stage1/x6s1_cloud.py:92](../../tools/x6_stage1/x6s1_cloud.py#L92) |  |
| `v1` | function | `v1` | [tools/c1prime/c1_gates.py:86](../../tools/c1prime/c1_gates.py#L86) |  |
| `v12` | function | `v12` | [tools/c1prime/c1_driver_late.py:101](../../tools/c1prime/c1_driver_late.py#L101) |  |
| `v2` | function | `v2` | [tools/c1prime/c1_gates.py:98](../../tools/c1prime/c1_gates.py#L98) |  |
| `v3` | function | `v3` | [tools/c1prime/c1_endpoint.py:79](../../tools/c1prime/c1_endpoint.py#L79) |  |
| `v3` | function | `v3` | [tools/c2_readout/c2_stage_val.py:228](../../tools/c2_readout/c2_stage_val.py#L228) |  |
| `v3x` | function | `v3x` | [tools/c2_readout/c2_stage_val.py:240](../../tools/c2_readout/c2_stage_val.py#L240) |  |
| `v3y` | function | `v3y` | [tools/c2_readout/c2_stage_val.py:244](../../tools/c2_readout/c2_stage_val.py#L244) |  |
| `v_prime` | function | `v_prime` | [tools/hws/hws_worlds.py:162](../../tools/hws/hws_worlds.py#L162) |  |
| `val` | function | `val` | [tests/k4b/test_a_ranks_ladder.py:56](../../tests/k4b/test_a_ranks_ladder.py#L56) |  |
| `val` | function | `val` | [tests/k4b/test_b_endpoint.py:58](../../tests/k4b/test_b_endpoint.py#L58) |  |
| `ValForward` | class | `ValForward` | [src/topo_pilot/experiment/x4f_gates.py:138](../../src/topo_pilot/experiment/x4f_gates.py#L138) | Frozen model on the validation inputs: base logits, captured hooks, patched runs. |
| `valid` | function | `valid` | [tests/circle_history/test_adapter.py:143](../../tests/circle_history/test_adapter.py#L143) |  |
| `valid_hook_names` | function | `valid_hook_names` | [src/topo_pilot/activations/_extractor.py:30](../../src/topo_pilot/activations/_extractor.py#L30) | Hook names of a model with ``n_layers`` blocks (learner SPEC). |
| `valid_record` | function | `valid_record` | [tools/x6_stage1/x6s1_cloud.py:240](../../tools/x6_stage1/x6s1_cloud.py#L240) |  |
| `validate` | method | `ActivationSet.validate` | [src/topo_pilot/contracts/_schemas_results.py:66](../../src/topo_pilot/contracts/_schemas_results.py#L66) |  |
| `validate` | method | `Artifact.validate` | [src/topo_pilot/contracts/base.py:119](../../src/topo_pilot/contracts/base.py#L119) | Check every invariant of this artifact. Raises ``StageFailure``. |
| `validate` | method | `BaselineOutputs.validate` | [src/topo_pilot/contracts/_schemas_data.py:231](../../src/topo_pilot/contracts/_schemas_data.py#L231) |  |
| `validate` | method | `Checkpoint.validate` | [src/topo_pilot/contracts/_schemas_results.py:39](../../src/topo_pilot/contracts/_schemas_results.py#L39) |  |
| `validate` | method | `Diagrams.validate` | [src/topo_pilot/contracts/_schemas_results.py:141](../../src/topo_pilot/contracts/_schemas_results.py#L141) |  |
| `validate` | method | `DistanceArtifact.validate` | [src/topo_pilot/contracts/_schemas_results.py:107](../../src/topo_pilot/contracts/_schemas_results.py#L107) |  |
| `validate` | method | `EmissionSpec.validate` | [src/topo_pilot/contracts/_schemas_world.py:185](../../src/topo_pilot/contracts/_schemas_world.py#L185) |  |
| `validate` | method | `EvalSidecar.validate` | [src/topo_pilot/contracts/_schemas_data.py:81](../../src/topo_pilot/contracts/_schemas_data.py#L81) |  |
| `validate` | method | `GateReport.validate` | [src/topo_pilot/contracts/_schemas_results.py:226](../../src/topo_pilot/contracts/_schemas_results.py#L226) |  |
| `validate` | method | `HistoryIndex.validate` | [src/topo_pilot/contracts/_schemas_data.py:121](../../src/topo_pilot/contracts/_schemas_data.py#L121) |  |
| `validate` | method | `MetricRecords.validate` | [src/topo_pilot/contracts/_schemas_results.py:192](../../src/topo_pilot/contracts/_schemas_results.py#L192) |  |
| `validate` | method | `ObservationSet.validate` | [src/topo_pilot/contracts/_schemas_data.py:49](../../src/topo_pilot/contracts/_schemas_data.py#L49) |  |
| `validate` | method | `OracleOutputs.validate` | [src/topo_pilot/contracts/_schemas_data.py:167](../../src/topo_pilot/contracts/_schemas_data.py#L167) |  |
| `validate` | method | `ProcessDiagnostics.validate` | [src/topo_pilot/contracts/_schemas_data.py:211](../../src/topo_pilot/contracts/_schemas_data.py#L211) |  |
| `validate` | method | `RunManifest.validate` | [src/topo_pilot/contracts/_schemas_results.py:258](../../src/topo_pilot/contracts/_schemas_results.py#L258) |  |
| `validate` | method | `TransitionSpec.validate` | [src/topo_pilot/contracts/_schemas_world.py:143](../../src/topo_pilot/contracts/_schemas_world.py#L143) |  |
| `validate` | method | `WorldSpec.validate` | [src/topo_pilot/contracts/_schemas_world.py:66](../../src/topo_pilot/contracts/_schemas_world.py#L66) |  |
| `validate` | function | `validate` | [tools/x4_oracle_profile/validation.py:197](../../tools/x4_oracle_profile/validation.py#L197) |  |
| `validate_checkpoints` | function | `validate_checkpoints` | [src/topo_pilot/experiment/x5g1t_checks.py:69](../../src/topo_pilot/experiment/x5g1t_checks.py#L69) | ``{checkpoint_id: (Checkpoint, sha)}`` after checking every identity field. |
| `validate_config` | function | `validate_config` | [src/topo_pilot/experiment/x5g1t_config.py:383](../../src/topo_pilot/experiment/x5g1t_config.py#L383) | Read-only report (resolved roots, mode, checked hashes); ``ConfigInvalid`` otherwise. |
| `validate_handoff_json` | function | `validate_handoff_json` | [tools/k4b/k4b_registry.py:134](../../tools/k4b/k4b_registry.py#L134) |  |
| `validate_pool` | function | `validate_pool` | [src/topo_pilot/experiment/x5g1t_checks.py:35](../../src/topo_pilot/experiment/x5g1t_checks.py#L35) | ``{pool_id: (ObservationSet, sha)}`` once the pool is proven to be ``split/arm/master``: |
| `validate_pools` | function | `validate_pools` | [src/topo_pilot/experiment/x5g1t_stages.py:130](../../src/topo_pilot/experiment/x5g1t_stages.py#L130) | Semantic identity of each ``(split, arm, master)`` pool in the table (API v4.1 §B). |
| `validate_process` | function | `validate_process` | [tools/x4_oracle_profile/oracle_profile.py:69](../../tools/x4_oracle_profile/oracle_profile.py#L69) | Check shapes, finiteness, nonnegativity, stochastic rows and stationarity of ``pi``. |
| `validate_tables` | function | `validate_tables` | [tools/x6_stage1/x6s1_pairs.py:76](../../tools/x6_stage1/x6s1_pairs.py#L76) | Σ_{v ≠ a★, κ} c_m equals x6_dp.avoid_counts totals for every layer m ≥ 1 present. |
| `validity` | function | `validity` | [tools/x2a_stage0/x2a_ph.py:144](../../tools/x2a_stage0/x2a_ph.py#L144) |  |
| `values` | method | `Records.values` | [tests/hws/test_a_classify.py:50](../../tests/hws/test_a_classify.py#L50) |  |
| `values` | method | `Records.values` | [tests/hws/test_a_outcomes.py:46](../../tests/hws/test_a_outcomes.py#L46) |  |
| `variant_category` | function | `variant_category` | [tools/c2_readout/c2_decide.py:164](../../tools/c2_readout/c2_decide.py#L164) | The R category rule on the variant arrays, with the primary RESP/SPEC prerequisites. |
| `variant_model` | function | `variant_model` | [tools/x2a_stage0/x2a_model.py:105](../../tools/x2a_stage0/x2a_model.py#L105) |  |
| `vector_phase` | function | `vector_phase` | [tools/k4b/k4b_scores.py:35](../../tools/k4b/k4b_scores.py#L35) |  |
| `verdict` | method | `F1Decision.verdict` | [src/topo_pilot/analysis/f1.py:105](../../src/topo_pilot/analysis/f1.py#L105) | Apply the rule to ``[(D_r, u_r)]`` with one learning-gate flag per replicate. |
| `verdict` | function | `verdict` | [src/topo_pilot/experiment/report_e2.py:115](../../src/topo_pilot/experiment/report_e2.py#L115) | ``(status, reasons)`` of the F1 verdict row; ``("not run", "")`` if absent. |
| `verdict` | function | `verdict` | [tools/chart_diag/chart_diag.py:69](../../tools/chart_diag/chart_diag.py#L69) | Mechanical rule (fixed in the spec): GO iff every giant fraction >= 0.95. |
| `verdicts` | function | `verdicts` | [tests/experiment/test_x4.py:131](../../tests/experiment/test_x4.py#L131) | Suffixes (statuses) of the verdict rows `prefix + <STATUS>` of one space and condition. |
| `verify` | function | `verify` | [tests/c1prime/test_a_release_meter.py:104](../../tests/c1prime/test_a_release_meter.py#L104) |  |
| `verify` | function | `verify` | [tools/c1prime/c1_release.py:127](../../tools/c1prime/c1_release.py#L127) |  |
| `verify` | function | `verify` | [tools/x4_circle_history/release.py:82](../../tools/x4_circle_history/release.py#L82) | Return the release dict if every binding holds; ReleaseError otherwise. |
| `verify` | function | `verify` | [tools/x4_oracle_profile/freeze.py:159](../../tools/x4_oracle_profile/freeze.py#L159) |  |
| `verify_admitted` | function | `verify_admitted` | [tools/x6_stage1/x6s1_ingest.py:441](../../tools/x6_stage1/x6s1_ingest.py#L441) |  |
| `verify_bundle` | function | `verify_bundle` | [tools/x6_stage1/x6s1_cloud.py:397](../../tools/x6_stage1/x6s1_cloud.py#L397) |  |
| `verify_export_complete` | function | `verify_export_complete` | [src/topo_pilot/experiment/x5g1t_exports.py:81](../../src/topo_pilot/experiment/x5g1t_exports.py#L81) | Manifest of a COMPLETE export whose files match exactly; else ``ExportIncomplete``. |
| `verify_freeze` | function | `verify_freeze` | [tools/hws/hws_records.py:269](../../tools/hws/hws_records.py#L269) | Every stage job checks FREEZE.json against the working tree before any sampling. |
| `verify_freeze` | function | `verify_freeze` | [tools/hwsb/hwsb_records.py:146](../../tools/hwsb/hwsb_records.py#L146) |  |
| `verify_full` | function | `verify_full` | [src/topo_pilot/experiment/x5g1t_checks.py:29](../../src/topo_pilot/experiment/x5g1t_checks.py#L29) |  |
| `verify_identity` | function | `verify_identity` | [tools/d2a/d2a_train.py:214](../../tools/d2a/d2a_train.py#L214) | Dispatch identities (ruling D6): request, task.json, task.md digest, RUN.lock session. |
| `verify_input_hashes` | function | `verify_input_hashes` | [tools/x4_oracle_profile/inputs.py:42](../../tools/x4_oracle_profile/inputs.py#L42) |  |
| `verify_parents` | function | `verify_parents` | [src/topo_pilot/experiment/x5g1_controls.py:94](../../src/topo_pilot/experiment/x5g1_controls.py#L94) | Failures for artifacts that are missing or whose payload_sha256 lacks the expected |
| `verify_release` | function | `verify_release` | [tools/k4b/k4b_release.py:43](../../tools/k4b/k4b_release.py#L43) |  |
| `verify_reservation` | function | `verify_reservation` | [tools/k4b/k4b_release.py:131](../../tools/k4b/k4b_release.py#L131) |  |
| `verify_rows` | function | `verify_rows` | [tools/x4_circle_history/reference_cache.py:109](../../tools/x4_circle_history/reference_cache.py#L109) | Invalid unless the stored row table for (model, split) equals the reloaded rows exactly |
| `verify_sources_full` | function | `verify_sources_full` | [src/topo_pilot/experiment/x5g1_safety.py:26](../../src/topo_pilot/experiment/x5g1_safety.py#L26) | Failures for artifacts whose metadata hash differs from the full expected hash or whose |
| `vertex` | function | `vertex` | [tools/x6_stage0/x6_model.py:76](../../tools/x6_stage0/x6_model.py#L76) |  |
| `view_curve` | method | `S6Job.view_curve` | [src/topo_pilot/experiment/s6.py:189](../../src/topo_pilot/experiment/s6.py#L189) | (S, status) on panel 1 at every checkpoint for each view in ``views``. |
| `view_envelopes` | method | `S6Job.view_envelopes` | [src/topo_pilot/experiment/s6.py:178](../../src/topo_pilot/experiment/s6.py#L178) | u_r per (view, replicate) from the newest X4 record, for this condition. |
| `view_table` | function | `view_table` | [src/topo_pilot/experiment/report_x4.py:50](../../src/topo_pilot/experiment/report_x4.py#L50) |  |
| `violations_for` | function | `violations_for` | [tools/check_imports.py:46](../../tools/check_imports.py#L46) | Return the rule messages that importing topo_pilot.<parts> from <module> breaks. |
| `visit` | method | `Collector.visit` | [tools/code_index/pyinfo.py:95](../../tools/code_index/pyinfo.py#L95) |  |
| `visit_Name` | method | `_Subst.visit_Name` | [tools/code_index/pathval.py:53](../../tools/code_index/pathval.py#L53) |  |
| `vphase` | function | `vphase` | [tests/k4b/test_b_endpoint.py:49](../../tests/k4b/test_b_endpoint.py#L49) |  |
| `w0` | function | `w0` | [tests/hws/test_b_exact.py:72](../../tests/hws/test_b_exact.py#L72) |  |
| `w0` | function | `w0` | [tests/hws/test_b_oracle.py:43](../../tests/hws/test_b_oracle.py#L43) |  |
| `w0` | function | `w0` | [tests/hwsb/test_b_process.py:46](../../tests/hwsb/test_b_process.py#L46) |  |
| `w0` | function | `w0` | [tests/hwsb/test_b_streams.py:148](../../tests/hwsb/test_b_streams.py#L148) |  |
| `w0_process` | function | `w0_process` | [tools/hwsb/hwsb_known.py:158](../../tools/hwsb/hwsb_known.py#L158) |  |
| `w32` | function | `w32` | [tools/c2_readout/c2_stage_base.py:226](../../tools/c2_readout/c2_stage_base.py#L226) |  |
| `w_hat` | function | `w_hat` | [tools/c1prime/c1_fit.py:206](../../tools/c1prime/c1_fit.py#L206) |  |
| `w_path` | function | `w_path` | [tests/x6_stage0/test_x6_stage0.py:115](../../tests/x6_stage0/test_x6_stage0.py#L115) |  |
| `w_tokens` | function | `w_tokens` | [tests/x6_stage0/test_x6_stage0.py:123](../../tests/x6_stage0/test_x6_stage0.py#L123) |  |
| `wait` | method | `FakeTree.wait` | [tests/x6_stage1/test_b_nb_s0_ops.py:293](../../tests/x6_stage1/test_b_nb_s0_ops.py#L293) |  |
| `wait` | method | `TrainingProcess.wait` | [tools/d2a/process_tree.py:82](../../tools/d2a/process_tree.py#L82) |  |
| `walk` | function | `walk` | [tests/hwsb/test_b_registry.py:72](../../tests/hwsb/test_b_registry.py#L72) |  |
| `walk` | function | `walk` | [tools/check_file_sizes.py:26](../../tools/check_file_sizes.py#L26) |  |
| `walks` | function | `walks` | [tests/x6_stage1/test_a_designed.py:41](../../tests/x6_stage1/test_a_designed.py#L41) |  |
| `walks` | function | `walks` | [tests/x6_stage1/test_a_eval.py:39](../../tests/x6_stage1/test_a_eval.py#L39) |  |
| `walks` | function | `walks` | [tests/x6_stage1/test_a_pairs.py:119](../../tests/x6_stage1/test_a_pairs.py#L119) | Synthetic positive-probability histories: random walk, a random cue at the anchor. |
| `WarmupCosine` | class | `WarmupCosine` | [src/topo_pilot/learner/trainer.py:45](../../src/topo_pilot/learner/trainer.py#L45) | LR multiplier after ``s`` finished updates (picklable, so scheduler state is plain data). |
| `warp_profile` | function | `warp_profile` | [src/topo_pilot/process/conductance.py:28](../../src/topo_pilot/process/conductance.py#L28) | Warped circumference profile and horizontal edge lengths. |
| `wave_lease` | function | `wave_lease` | [tools/d2a/process_tree.py:17](../../tools/d2a/process_tree.py#L17) | Exclusive wave lease; an abandoned lease is never silently cleared. |
| `wave_main` | function | `wave_main` | [tools/d2a/d2a_train.py:317](../../tools/d2a/d2a_train.py#L317) |  |
| `wcounts` | function | `wcounts` | [tests/k4b/test_a_width_b4.py:57](../../tests/k4b/test_a_width_b4.py#L57) |  |
| `weights` | function | `weights` | [tools/x6_stage0/x6_dp.py:47](../../tools/x6_stage0/x6_dp.py#L47) |  |
| `weights_digest` | function | `weights_digest` | [tools/x6_stage1/x6s1_cloud.py:106](../../tools/x6_stage1/x6s1_cloud.py#L106) |  |
| `weights_hash` | function | `weights_hash` | [src/topo_pilot/experiment/x4f_gates.py:124](../../src/topo_pilot/experiment/x4f_gates.py#L124) |  |
| `whiten` | function | `whiten` | [src/topo_pilot/analysis/x4f_erasure.py:40](../../src/topo_pilot/analysis/x4f_erasure.py#L40) | Whitening of ``X [n, d]`` on its retained eigen-range. |
| `whitened_fixture` | function | `whitened_fixture` | [tests/c1prime/test_a_eligibility_support.py:130](../../tests/c1prime/test_a_eligibility_support.py#L130) |  |
| `Whitening` | class | `Whitening` | [src/topo_pilot/analysis/x4f_erasure.py:27](../../src/topo_pilot/analysis/x4f_erasure.py#L27) | Retained-range whitening: ``W = diag(lam^-1/2) U_keep^T`` ``[k, d]``, |
| `whitening` | function | `whitening` | [tools/c1prime/c1_fit.py:73](../../tools/c1prime/c1_fit.py#L73) |  |
| `width_diagnostic` | function | `width_diagnostic` | [tools/k4b/k4b_stats.py:146](../../tools/k4b/k4b_stats.py#L146) | §7.6 (report only): [D + e+ + q(e+) + F < 0.01] and [-D + e- + q(e-) - F > -0.01]. |
| `window8_features` | function | `window8_features` | [tools/d2a/d2a_eval.py:111](../../tools/d2a/d2a_eval.py#L111) |  |
| `window_law` | function | `window_law` | [tools/x2a_stage0/x2a_model.py:124](../../tools/x2a_stage0/x2a_model.py#L124) |  |
| `window_posterior` | function | `window_posterior` | [tools/d2a/d2a_targets.py:46](../../tools/d2a/d2a_targets.py#L46) |  |
| `window_prior` | function | `window_prior` | [tools/d2a/d2a_targets.py:41](../../tools/d2a/d2a_targets.py#L41) |  |
| `windows` | function | `windows` | [src/topo_pilot/experiment/x4b2.py:129](../../src/topo_pilot/experiment/x4b2.py#L129) | Unique 32-symbol windows as fixed-width byte records (for overlap counting). |
| `with_payload_files` | function | `with_payload_files` | [tests/k4b/test_b_h1_meta.py:276](../../tests/k4b/test_b_h1_meta.py#L276) |  |
| `with_satellites` | function | `with_satellites` | [tests/c1prime/test_a_chart.py:70](../../tests/c1prime/test_a_chart.py#L70) | Loop plus n_sat isolated satellites at interleaved landmark positions 7, 27, 47, ... |
| `witness_path` | function | `witness_path` | [tools/x6_stage0/x6_exact.py:97](../../tools/x6_stage0/x6_exact.py#L97) |  |
| `witness_tokens` | function | `witness_tokens` | [tools/x6_stage0/x6_exact.py:107](../../tools/x6_stage0/x6_exact.py#L107) |  |
| `World` | class | `World` | [tools/hws/hws_worlds.py:77](../../tools/hws/hws_worlds.py#L77) |  |
| `world` | method | `SpaceBuilder.world` | [src/topo_pilot/analysis/spaces.py:61](../../src/topo_pilot/analysis/spaces.py#L61) | The N states with the world distance as D, metric ``flat``. |
| `world` | function | `world` | [tests/c1prime/test_a_release_meter.py:59](../../tests/c1prime/test_a_release_meter.py#L59) |  |
| `world` | function | `world` | [tests/hwsb/test_b_e4path.py:98](../../tests/hwsb/test_b_e4path.py#L98) |  |
| `world` | function | `world` | [tests/hwsb/test_b_hold.py:159](../../tests/hwsb/test_b_hold.py#L159) |  |
| `world` | function | `world` | [tests/process/test_conductance.py:43](../../tests/process/test_conductance.py#L43) | 12 x 12 cylinder from the world package (state id = x * 12 + y). |
| `world_difference` | method | `S2Stage.world_difference` | [src/topo_pilot/experiment/s2.py:164](../../src/topo_pilot/experiment/s2.py#L164) | Per space × condition: number of panels with S_cyl > S_sq (D-023). |
| `world_id` | function | `world_id` | [src/topo_pilot/experiment/s2.py:55](../../src/topo_pilot/experiment/s2.py#L55) | The unique WorldSpec of ``family`` with the configured dims and metric. |
| `world_identity` | function | `world_identity` | [tools/x4_oracle_profile/inputs.py:93](../../tools/x4_oracle_profile/inputs.py#L93) | 12x12 cylinder (x periodic) from coords; stored edges and T support match that lattice. |
| `world_kernels` | function | `world_kernels` | [tools/d2a/d2a_world.py:86](../../tools/d2a/d2a_world.py#L86) | Per-block filters: ``T_C``, ``T_M`` (``T_C`` twice for CC), ``E``, ``mu_C``, ``mu_M``. |
| `world_key` | function | `world_key` | [tools/hws/hws_worlds.py:72](../../tools/hws/hws_worlds.py#L72) |  |
| `world_look` | function | `world_look` | [tools/hws/hws_oracle.py:162](../../tools/hws/hws_oracle.py#L162) |  |
| `world_ph` | function | `world_ph` | [src/topo_pilot/experiment/s1.py:49](../../src/topo_pilot/experiment/s1.py#L49) | Diagrams (H0, H1) of the world's ``dist`` or ``dist_graph`` and the scale s (q95). |
| `world_record` | function | `world_record` | [tools/hws/hws_driver.py:173](../../tools/hws/hws_driver.py#L173) | One world-look: sample once, keep the tokens, aggregate, null rule, write the record. |
| `WorldBuilder` | class | `WorldBuilder` | [src/topo_pilot/world/registry.py:15](../../src/topo_pilot/world/registry.py#L15) | Builds a :class:`WorldSpec` for one family. |
| `WorldConfig` | class | `WorldConfig` | [src/topo_pilot/world/config.py:10](../../src/topo_pilot/world/config.py#L10) | Configuration of a latent world. |
| `WorldSpec` | class | `WorldSpec` | [src/topo_pilot/contracts/_schemas_world.py:22](../../src/topo_pilot/contracts/_schemas_world.py#L22) | A latent world: states, the cubical complex defining the surface, metrics, homology. |
| `WorldStage` | class | `WorldStage` | [src/topo_pilot/world/stage.py:16](../../src/topo_pilot/world/stage.py#L16) | Build and persist a world (deterministic; no RNG, empty seed map, no parents). |
| `wrap` | function | `wrap` | [tests/analysis/test_sensitivity_circular.py:40](../../tests/analysis/test_sensitivity_circular.py#L40) | Wrap angles to (-pi, pi]. |
| `wrap` | function | `wrap` | [tools/c1prime/c1_gates.py:76](../../tools/c1prime/c1_gates.py#L76) | Angle to (-pi, pi]. |
| `wrap_phase` | function | `wrap_phase` | [tools/k4b/k4b_scores.py:27](../../tools/k4b/k4b_scores.py#L27) |  |
| `write` | function | `write` | [tests/oracle_profile/test_builder_controls.py:36](../../tests/oracle_profile/test_builder_controls.py#L36) |  |
| `write` | function | `write` | [tools/code_index/build.py:65](../../tools/code_index/build.py#L65) |  |
| `write_admission_lock` | function | `write_admission_lock` | [tools/x6_stage1/x6s1_ingest.py:409](../../tools/x6_stage1/x6s1_ingest.py#L409) |  |
| `write_checkpoint` | function | `write_checkpoint` | [tools/x6_stage1/x6s1_cloud.py:220](../../tools/x6_stage1/x6s1_cloud.py#L220) |  |
| `write_gate` | function | `write_gate` | [tools/x6_stage0/x6_store.py:214](../../tools/x6_stage0/x6_store.py#L214) |  |
| `write_gate` | function | `write_gate` | [tools/x6_stage1/x6s1_run.py:282](../../tools/x6_stage1/x6s1_run.py#L282) |  |
| `write_job_json` | function | `write_job_json` | [src/topo_pilot/executors/local.py:32](../../src/topo_pilot/executors/local.py#L32) | Write the ``job.json`` that ``entry`` reads. |
| `write_json` | function | `write_json` | [tests/k4b/test_b_registry_fixes.py:48](../../tests/k4b/test_b_registry_fixes.py#L48) |  |
| `write_json` | function | `write_json` | [tools/d2a/d2a_train.py:208](../../tools/d2a/d2a_train.py#L208) | Exclusive-create JSON write of ``jsonable(rec)`` (stage records are never overwritten). |
| `write_json_atomic` | function | `write_json_atomic` | [tools/x6_stage1/x6s1_cloud.py:223](../../tools/x6_stage1/x6s1_cloud.py#L223) |  |
| `write_look` | function | `write_look` | [tools/hws/hws_records.py:208](../../tools/hws/hws_records.py#L208) |  |
| `write_manifest` | function | `write_manifest` | [tools/c2_readout/c2_driver.py:273](../../tools/c2_readout/c2_driver.py#L273) |  |
| `write_manifest` | function | `write_manifest` | [tools/x6_stage0/x6_store.py:122](../../tools/x6_stage0/x6_store.py#L122) |  |
| `write_marker` | function | `write_marker` | [tools/x4_circle_history/op_guard.py:27](../../tools/x4_circle_history/op_guard.py#L27) |  |
| `write_marker` | function | `write_marker` | [tools/x6_stage0/x6_store.py:209](../../tools/x6_stage0/x6_store.py#L209) |  |
| `write_marker` | function | `write_marker` | [tools/x6_stage1/x6s1_cloud.py:295](../../tools/x6_stage1/x6s1_cloud.py#L295) |  |
| `write_new` | function | `write_new` | [tools/x4_circle_history/stage_records.py:35](../../tools/x4_circle_history/stage_records.py#L35) |  |
| `write_new` | function | `write_new` | [tools/x4_oracle_profile/freeze.py:101](../../tools/x4_oracle_profile/freeze.py#L101) |  |
| `write_preflight` | function | `write_preflight` | [tools/x6_stage0/x6_store.py:231](../../tools/x6_stage0/x6_store.py#L231) |  |
| `write_prereg` | function | `write_prereg` | [src/topo_pilot/experiment/prereg.py:115](../../src/topo_pilot/experiment/prereg.py#L115) | Write ``PREREGISTRATION.md`` at the repository root; returns its path. |
| `write_report` | function | `write_report` | [tools/hws/hws_records.py:311](../../tools/hws/hws_records.py#L311) |  |
| `write_sealed` | function | `write_sealed` | [tools/k4b/k4b_stats.py:185](../../tools/k4b/k4b_stats.py#L185) | The only writer of SEALED_VALIDATION.json (exclusive create, once); returns its sha256. |
| `write_selection` | function | `write_selection` | [tools/hws/hws_records.py:349](../../tools/hws/hws_records.py#L349) |  |
| `write_stage` | function | `write_stage` | [tools/x6_stage1/x6s1_run.py:289](../../tools/x6_stage1/x6s1_run.py#L289) |  |
| `write_tables` | function | `write_tables` | [tools/x4_oracle_profile/run_profile.py:109](../../tools/x4_oracle_profile/run_profile.py#L109) |  |
| `write_world_summaries` | function | `write_world_summaries` | [tools/hws/hws_records.py:355](../../tools/hws/hws_records.py#L355) | worlds/<key>.json once per evaluated world: every look path and sha256, latest class. |
| `wrong_filter` | function | `wrong_filter` | [tests/oracle_profile/test_oracle_profile_traps.py:76](../../tests/oracle_profile/test_oracle_profile_traps.py#L76) | Plain float forward filter with switchable MISTAKES (test-only, never production). |
| `x1` | function | `x1` | [tools/c2_readout/c2_model.py:261](../../tools/c2_readout/c2_model.py#L261) | Closed form vs the network on every arm; arms[name] = (inputs, y_hat, z_ref, seq_ids), |
| `x1` | function | `x1` | [tools/c2_readout/c2_stage_val.py:223](../../tools/c2_readout/c2_stage_val.py#L223) |  |
| `x1_arms` | function | `x1_arms` | [tools/c2_readout/c2_stage_val.py:86](../../tools/c2_readout/c2_stage_val.py#L86) | X1 arms (§7 row 17): natural arms (H^Y on its Y_def rows); the R interchange arms on every |
| `x1_attainable` | function | `x1_attainable` | [tools/c2_readout/c2_model.py:187](../../tools/c2_readout/c2_model.py#L187) | 4 * 128 * 2**-53 * kappa_X1 <= 1e-10 in exact rationals (API.md C-6). |
| `x1_run` | function | `x1_run` | [tools/c2_readout/c2_stage_val.py:113](../../tools/c2_readout/c2_stage_val.py#L113) | X1 (ephemeral, §5.7): identity diagnostics only; the natural logits are cleared after. |
| `x1_trigger` | function | `x1_trigger` | [tools/hws/hws_select.py:116](../../tools/hws/hws_select.py#L116) | §6.2 item 1 (RC-6, choice 41). |
| `x1_worlds` | function | `x1_worlds` | [tools/hws/hws_worlds.py:104](../../tools/hws/hws_worlds.py#L104) |  |
| `x4_compare` | function | `x4_compare` | [src/topo_pilot/experiment/report_e3.py:121](../../src/topo_pilot/experiment/report_e3.py#L121) | Secondary X4 outcomes under O and P side by side. |
| `x4_curves` | method | `S6Job.x4_curves` | [src/topo_pilot/experiment/s6.py:207](../../src/topo_pilot/experiment/s6.py#L207) |  |
| `x4_rows` | function | `x4_rows` | [src/topo_pilot/experiment/report_x4.py:29](../../src/topo_pilot/experiment/report_x4.py#L29) |  |
| `x4_section` | function | `x4_section` | [src/topo_pilot/experiment/report_x4.py:87](../../src/topo_pilot/experiment/report_x4.py#L87) | Markdown lines of the X4 section (secondary; F1 stays the headline). |
| `x4c_category` | function | `x4c_category` | [src/topo_pilot/experiment/x4.py:55](../../src/topo_pilot/experiment/x4.py#L55) | X4-c category: a view counts iff its F1-rule status is ``SUPPORTED``. |
| `X4Job` | class | `X4Job` | [src/topo_pilot/experiment/x4.py:96](../../src/topo_pilot/experiment/x4.py#L96) | Builds the views, computes every X4 quantity and saves one MetricRecords. |
| `X4Panel` | class | `X4Panel` | [src/topo_pilot/experiment/x4_inputs.py:43](../../src/topo_pilot/experiment/x4_inputs.py#L43) | One panel of one run at one checkpoint: ``Z [M, d]`` (resid_post_3), ``ln_out [M, d]`` |
| `X4Run` | class | `X4Run` | [src/topo_pilot/experiment/x4_inputs.py:54](../../src/topo_pilot/experiment/x4_inputs.py#L54) | Everything X4 needs from one training run (see experiment/SPEC.md, Stage X4). |
| `X4Stage` | class | `X4Stage` | [src/topo_pilot/experiment/x4.py:339](../../src/topo_pilot/experiment/x4.py#L339) | X4: secondary readout-geometry analyses on the stored runs of ``X4.sources``. |
| `x5_overall_verdict` | function | `x5_overall_verdict` | [src/topo_pilot/analysis/x5_context.py:33](../../src/topo_pilot/analysis/x5_context.py#L33) | Precedence FAILED > INCONCLUSIVE > WEAK_CONTEXT > FEASIBLE (a weak arm never conceals an |
| `x6_source` | function | `x6_source` | [tools/c2_readout/c2_registry.py:99](../../tools/c2_readout/c2_registry.py#L99) | X6-REG2 (re-hashed, manifest bound by CONTRACT.json) as base plus every other history- |
| `x_interval` | function | `x_interval` | [tools/chart_diag/chart_diag.py:63](../../tools/chart_diag/chart_diag.py#L63) | X's interval [l_max, d): descriptive only. |
| `x_leakage` | function | `x_leakage` | [tools/c2_readout/c2_oracle.py:181](../../tools/c2_readout/c2_oracle.py#L181) | lambda_x at b31 and b32: mean_{E_y} \|m32(H^Y) - m32(H)\| / mean_{E_x} \|m32(H+) - m32(H-)\| |
| `x_marginal` | function | `x_marginal` | [tools/hws/hws_oracle.py:68](../../tools/hws/hws_oracle.py#L68) |  |
| `xcheck` | function | `xcheck` | [tools/x6_stage1/x6s1_stage_post.py:297](../../tools/x6_stage1/x6s1_stage_post.py#L297) |  |
| `y1` | function | `y1` | [tools/c2_readout/c2_stage_val.py:269](../../tools/c2_readout/c2_stage_val.py#L269) |  |
| `y1s` | function | `y1s` | [tools/c2_readout/c2_stage_val.py:273](../../tools/c2_readout/c2_stage_val.py#L273) |  |
| `y2` | function | `y2` | [tools/c2_readout/c2_stage_val.py:277](../../tools/c2_readout/c2_stage_val.py#L277) | Y2 (M): activity L(A^Y_M,F - 0.10 A^Y_full) > g, then U(A^Y_M,S - 0.10 A^Y_M,F) < -g. |
| `y_active` | function | `y_active` | [tools/c2_readout/c2_oracle.py:172](../../tools/c2_readout/c2_oracle.py#L172) |  |
| `y_donor` | function | `y_donor` | [tools/c2_readout/c2_data.py:80](../../tools/c2_readout/c2_data.py#L80) | H^Y = (6a + (b + k) on w1..w31, w32) and Y_def; an off-grid row is OFF in full (never |
| `Y_hat` | function | `Y_hat` | [tools/c1prime/c1_endpoint.py:35](../../tools/c1prime/c1_endpoint.py#L35) |  |
| `y_marginal` | function | `y_marginal` | [tools/c1prime/c1_oracle.py:166](../../tools/c1prime/c1_oracle.py#L166) |  |
| `y_on` | function | `y_on` | [tools/c2_readout/c2_stage_val.py:248](../../tools/c2_readout/c2_stage_val.py#L248) |  |
| `y_rot` | function | `y_rot` | [tools/c2_readout/c2_attrib.py:176](../../tools/c2_readout/c2_attrib.py#L176) | y + B (R_K(theta) - I) f-hat, f-hat = L_B (y - alpha_w): the code rotates, the rest holds. |
| `Yf` | function | `Yf` | [tools/c2_readout/c2_stage_base.py:235](../../tools/c2_readout/c2_stage_base.py#L235) |  |
| `ygrid` | function | `ygrid` | [reports/he_summary/charts.py:110](../../reports/he_summary/charts.py#L110) |  |
| `yplac` | function | `yplac` | [tools/c2_readout/c2_stage_val.py:252](../../tools/c2_readout/c2_stage_val.py#L252) | Y1 (R) / Y1* (S*): U(A^Y_S - 0.10 A^Y_full) < -g on VAL E_y rows, if active. |
| `z_bound` | function | `z_bound` | [tests/k4b/test_a_lemma_t.py:88](../../tests/k4b/test_a_lemma_t.py#L88) |  |
| `Z_hat` | function | `Z_hat` | [tools/c1prime/c1_endpoint.py:42](../../tools/c1prime/c1_endpoint.py#L42) |  |
| `z_of` | function | `z_of` | [tools/hws/hws_stats.py:22](../../tools/hws/hws_stats.py#L22) |  |
| `zero_code_threshold` | function | `zero_code_threshold` | [tools/c2_readout/c2_code.py:182](../../tools/c2_readout/c2_code.py#L182) | 1e-12 x the inverted_cdf median of the FIT modulus (per model and family; NEW-3). |
| `zero_max` | function | `zero_max` | [tools/hws/hws_known.py:47](../../tools/hws/hws_known.py#L47) |  |
| `Zfull_hat` | function | `Zfull_hat` | [tools/c1prime/c1_endpoint.py:46](../../tools/c1prime/c1_endpoint.py#L46) |  |
| `zt` | function | `zt` | [tools/c2_readout/c2_stage_base.py:230](../../tools/c2_readout/c2_stage_base.py#L230) |  |
