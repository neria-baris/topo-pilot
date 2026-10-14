# Progress (updated 2026-10-14 by conductor, claude-opus-5-5; branch x5-g1-input-identity-fix)
Stage: **X5 G1 contract FROZEN, metadata only (job 0012, D-072): config sha256 2D4E17ED… (jobs/0012/STUDY_CONFIG_FROZEN.json), protocol/plan/API v4 + v4.1 addendum and source 94342e3 pinned in jobs/0012/FREEZE_MANIFEST.json; NO study histories yet; six-model execution awaits a distinct coordinator task**; pool input identity accepted (job 0011, D-071); driver integration v4 (job 0010, review REVISE, D-070); implementation v3 SYNTHETIC ONLY (job 0009, D-069); scoring correction FITS 13,400.25 CPU s; B1 RESOLVED (D-068); verification CONSISTENT (D-067); gate FEASIBLE (D-066); X4-F execution v2 closed INCONCLUSIVE (D-062, D-063); X4-F draft and plan (D-058) unchanged | Circular audit: BEYOND_SYMBOL_AND_MIXING, descriptive (D-057) | Practical Q2-gap branch closed by owner (D-055) | Phase B INCONCLUSIVE (D-052) · B2 NO-GO (D-054) · H4C-I decoder experiment: NOT RUN — stopped at feasibility gate | Last exit reached: E4 (tagged, local), with documented G-H failure

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
- Unresolved: short-context origin (w31, w32 vs longer history) and causal use of the coordinate; recoverability at resid_post_1/p32 is recorded (X4-F G1 PASS x3, D-062) but linear erasure left nonlinear recoverability and the controls were unmatched; the audit was descriptive, in-sample, on unblinded data
- X4-F execution v2 is closed INCONCLUSIVE (D-062, D-063): G5 NOT_RUN, no rescue or fresh causal test now; finite failed draws are not an impossibility proof
- G-H FAIL stands (D-049, D-050); no causal claims; H4 rejected; R1 limitation stands
- Integration tests I03 and I05 never built; cross-machine and GPU determinism untested

## Next actions (≤5)
1. STOP: coordinator review of the job 0012 freeze record; only a DISTINCT coordinator task may start the six-model execution (no launch on CONTINUE or because freeze files exist); research tree stays clean during science, heartbeats in the mailbox
2. No scientific sampling, six-model training, dev analysis or fresh test before that separately authorised freeze/job; movement-speed confound remains (no curvature attribution)
3. No Phase C, coverage extension, threshold change, intervention, merge, push or tag change
