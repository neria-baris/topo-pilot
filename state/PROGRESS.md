# Progress (updated 2026-10-14 by conductor, claude-opus-5-5; branch x4-circle-k4-feas-isolated-0016)
Stage: **X4 K4 circular-history FEASIBILITY RAN (job 0018, D-078): overall INCONCLUSIVE at chart_calibration (model 1729: graph at the selected scale is disconnected); identity and process_and_reference PASS; precision not reached; scoring panels 3-8 untouched and NOT released** | **X4 oracle suffix profile EXECUTED, exploratory (job 0014, D-074): calibration B_K 0.369/0.198/0.067/0.00925/0.00018 at K 1/2/4/8/16 (validation agrees); recorded K8 reproduced exactly; oracle headroom vs 0.01 only at K <= 4; K8 FAIL unchanged; recommendation A not authorised; OWNER-APPROVAL CHECKPOINT** | **X5 G1 six-model study EXECUTED under the frozen contract (job 0013, D-073): registered H5 verdict REJECTED on dev (pair 310002 bootstrap q975 delay 0 < 250); all 6 models COMPLETE, no censoring; fresh final test NOT run; OWNER-APPROVAL CHECKPOINT: no further experiment without explicit owner authorisation**; contract frozen (job 0012, D-072); pool input identity accepted (job 0011, D-071); driver integration v4 (job 0010, review REVISE, D-070); implementation v3 SYNTHETIC ONLY (job 0009, D-069); scoring correction FITS 13,400.25 CPU s; B1 RESOLVED (D-068); verification CONSISTENT (D-067); gate FEASIBLE (D-066); X4-F execution v2 closed INCONCLUSIVE (D-062, D-063); X4-F draft and plan (D-058) unchanged | Circular audit: BEYOND_SYMBOL_AND_MIXING, descriptive (D-057) | Practical Q2-gap branch closed by owner (D-055) | Phase B INCONCLUSIVE (D-052) · B2 NO-GO (D-054) · H4C-I decoder experiment: NOT RUN — stopped at feasibility gate | Last exit reached: E4 (tagged, local), with documented G-H failure

## Modules
| module | status | owner tier | notes |
|---|---|---|---|
| contracts | accepted (frozen 1.0.0) | A / TW | 95 tests; unchanged |
| tools | accepted | C | Makefile + tasks.ps1 |
| world | accepted | B / TW | 30 tests |
| process | accepted | B | is_x_periodic from complex (D-043) |
| topology | accepted | B / TW | CircularCoordinates (T12 slow) used in S7 |
| executors | accepted | B | 27 tests |
| dataset | accepted | B | HMMSampler reused unchanged by B2 |
| oracle | accepted | B / TW | kernels reused unchanged by X4 Phase B/B2 |
| prediction | accepted (a,b,c) | B | RidgeProbe; run_probes stub, I/O in experiment (D-047) |
| analysis | accepted (a–e) | A | part (e) horizon feasibility |
| learner | accepted | B | V override for U (V = 144) |
| activations | accepted | B | dev extraction via ActivationStage |
| experiment | S0–S8, X4, reports E0–E4; X4 Phase B/B2 adapters | A | not registered stages, no config change |
| integration | I01, I02, I04, I06 | B | I03, I05 never built (gap, reported) |

## Gates
| gate | verdict | date | key value |
|---|---|---|---|
| G-S0, G-A … G-F (S4, S5) | pass | 2026-10-13 | unchanged since E3 |
| G-G | pass | 2026-10-13 | unchanged |
| G-H | **FAIL** | 2026-10-13 | rerun_ok only (D-049); unchanged |
| X4 Phase B (protocol-local) | **INCONCLUSIVE** | 2026-10-13 | all 4 pools UNDERCOVERED (D-052) |
| X4 Phase B2 (protocol-local) | **NO-GO** | 2026-10-14 | 4 covered pools, 0 witnesses (D-054) |
| H4C-I (Phase C) | **NOT RUN** | 2026-10-14 | stopped at the feasibility gate (D-055) |
| X4 K4 circular-history feasibility, implementation (job 0016; isolated worktree) | **IMPLEMENTED (spec v2.4) + FROZEN; NOT EXECUTED** | 2026-10-14 | run_04: 508 tests pass (independent authors A/B + builder + 0014 regressions); freeze 15cbbef3 at 2149f37 (supersedes a6e457d3 at 8880919); ledger 115.53 CPU s measured+tail (implementation stage); store x4-circle-history-feas-store-0015 (D-075, D-076) |
| X4 K4 release/resource binding (job 0017; isolated worktree, branch x4-circle-k4-0017) | **IMPLEMENTED + FROZEN; NOT EXECUTED** | 2026-10-15 | run_05: 527 tests pass; freeze e3049fee at 041433c (supersedes 15cbbef3); Claude-coordinator release binding, measure-only CPU (owner override), phase [0, 2pi) F4; ledger 183.41 CPU s (D-077) |
| X4 K4 circular-history numerical feasibility, panels 1-2 (job 0018; release c351b245, freeze e3049fee, HEAD ab2be87) | **INCONCLUSIVE** (first non-PASS: chart_calibration, model 1729, criterion_met=false) | 2026-10-15 | identity PASS (4096 joined rows); process_and_reference PASS (max moment gap 8.0e-16; Z_bound 2.12e-12 BOUNDED); chart_calibration INCONCLUSIVE: primitive class Unresolved, graph at the frozen midpoint scale disconnected; no retry/refit; stages 325.1 CPU s; D-078 |
| D-1 seam oracle-only check (job 0019; D1-FROZEN-v1) | **BLOCKED (S6: module > 400 lines); no gate run** | 2026-10-15 | contract 6803a66, independent tests 70fc3a8; partial draft preserved in d1-seam-oracle-store/draft; awaiting coordinator ruling (D-079) |
| X4 oracle suffix profile (job 0014, exploratory; existing x4-history-feas histories) | **DESCRIPTIVE: headroom at K <= 4 only** | 2026-10-14 | B_K cal 0.369/0.198/0.0670/0.00925/0.000178 (K 1/2/4/8/16), val 0.377/0.195/0.0697/0.00929/0.000181; split differences include 0; K8 B/V reproduced to 0.0; V_K nonincreasing; 59.75 of 3,600 CPU s; store x4-oracle-profile-store-0014 (D-074) |
| X5 G1 H5 (a020 delay >= 250 updates in each pair; dev, x5g1-train-v4) | **REJECTED** | 2026-10-14 | events a0/a020: 310001 1750/2000, 310002 2000/2000, 310003 2000/2000; q975 delay 250/0/250; none censored; ledger 16,134.174 CPU s (D-073) |
| X5 G1 pool input identity (job 0011, not scientific) | **SYNTHETIC ONLY; config pending** | 2026-10-14 | semantic pool identity before any model/oracle/scoring/draw; lineage vs execution provenance; root wrong-arm probe now refused (0 train_one calls); independent regressions 47 (D-071) |
| X5 G1 driver integration (job 0010, not scientific) | **SYNTHETIC ONLY; config pending** | 2026-10-14 | six integration gaps fixed (actual-stage STOP/hold guards at exports, draws, 512-row scoring and oracle batches; frozen production validator; COMPLETE-manifest prerequisites; checkpoint identity and full hashes before use and before export; usage latch fail closed; latency/no hard-kill wording); no study data; ledgers 17.016 s / 152.188 s unchanged (D-070) |
| X5 G1 scoring-only correction (job 0009, not scientific) | **FITS** | 2026-10-14 | batched-512 p32 3.875 CPU s/4,096 rows; corrected projection 13,400.25 ≤ 17,266.39; tech ledger 152.188 s, scientific 17.016 s (D-069) |
| X5 G1 technical benchmark (job 0008, not scientific) | **B1 RESOLVED** | 2026-10-14 | 1 thread 0.383 CPU s/update; projected 13,428.8 ≤ 17,266.4 (80%); 6 threads 39,049.9 do not fit; tech ledger 140.4 s, scientific ledger 17.016 s (D-068) |
| X5 G1 verification (job 0007) | **CONSISTENT** | 2026-10-14 | 27/27 quantities identical (diff 0.0); X5 ledger 17.0 s (D-067) |
| X5 G1 gate (x5g1-feas-v2) | **FEASIBLE** | 2026-10-14 | G_C a0 0.271 [0.267, 0.275], a020 0.294 [0.290, 0.298] nats; kernels valid; 8.9 CPU s (D-066) |
| X4-F gates (x4f-exec-v2) | **INCONCLUSIVE; formulation closed (D-063)** | 2026-10-14 | G1–G3 PASS ×3 (G3 LINEAR_COMPONENT_ONLY), G4 FAMILY_UNMATCHED ×3, G5 NOT_RUN (D-062) |
| E4 circular-baseline audit (descriptive) | **BEYOND_SYMBOL_AND_MIXING** (direct R1 gap resolved descriptively) | 2026-10-14 | 24/24 run-panels: model 0.884–0.892 > A*_symbol 0.817 and best baseline; S7 rows reproduced exactly; 79 CPU s, 0.41 GB (D-057) |

## Open issues (≤5)
- Closure is scoped (cylinder O, σ 1.25, horizon 2, p32, registered screen); strict Q1 sufficiency UNRESOLVED; no general sufficiency proof and no decoder ceiling measured
- Unresolved: short-context origin (w31, w32 vs longer history) and causal use of the coordinate; recoverability at resid_post_1/p32 is recorded (X4-F G1 PASS x3, D-062) but linear erasure left nonlinear recoverability and the controls were unmatched; the audit was descriptive, in-sample, on unblinded data Oracle profile (D-074): the first-harmonic history signal is concentrated at K <= 4 (B4 0.067, B8 0.0092, B16 0.0002).
- X4-F execution v2 is closed INCONCLUSIVE (D-062, D-063): G5 NOT_RUN, no rescue or fresh causal test now; finite failed draws are not an impossibility proof
- G-H FAIL stands (D-049, D-050); no causal claims; H4 rejected; R1 limitation stands
- Integration tests I03 and I05 never built; cross-machine and GPU determinism untested

## Next actions (≤5)
1. Coordinator (c351b245) review of job 0018 (K4 feasibility INCONCLUSIVE at chart_calibration); no scoring release follows from a non-PASS feasibility cohort
2. No scientific sampling, six-model training, dev analysis or fresh test before that separately authorised freeze/job; movement-speed confound remains (no curvature attribution)
3. No Phase C, coverage extension, threshold change, intervention, merge, push or tag change
