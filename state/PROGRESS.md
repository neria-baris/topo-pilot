# Progress (updated 2026-10-14 by conductor, claude-opus-5-5; branch x5-g1-gates)
Stage: **X5 G1 gates implementation running (job 0006; contract x5g1-feas-v2 frozen, D-065)**; X4-F execution v2 closed INCONCLUSIVE (D-062, D-063); X4-F draft and plan (D-058) unchanged | Circular audit: BEYOND_SYMBOL_AND_MIXING, descriptive (D-057) | Practical Q2-gap branch closed by owner (D-055) | Phase B INCONCLUSIVE (D-052) · B2 NO-GO (D-054) · H4C-I decoder experiment: NOT RUN — stopped at feasibility gate | Last exit reached: E4 (tagged, local), with documented G-H failure

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
| X4-F gates (x4f-exec-v2) | **INCONCLUSIVE; formulation closed (D-063)** | 2026-10-14 | G1–G3 PASS ×3 (G3 LINEAR_COMPONENT_ONLY), G4 FAMILY_UNMATCHED ×3, G5 NOT_RUN (D-062) |
| E4 circular-baseline audit (descriptive) | **BEYOND_SYMBOL_AND_MIXING** (direct R1 gap resolved descriptively) | 2026-10-14 | 24/24 run-panels: model 0.884–0.892 > A*_symbol 0.817 and best baseline; S7 rows reproduced exactly; 79 CPU s, 0.41 GB (D-057) |

## Open issues (≤5)
- Closure is scoped (cylinder O, σ 1.25, horizon 2, p32, registered screen); strict Q1 sufficiency UNRESOLVED; no general sufficiency proof and no decoder ceiling measured
- Unresolved: short-context origin (w31, w32 vs longer history), recoverability at resid_post_1, and causal use of the coordinate; audit was descriptive, in-sample, on unblinded data
- X4-F is a draft (x4f-draft-1): every [P] threshold, the dev resid_post_1 extraction, the fresh test lineage and the learner adapter need owner approval
- G-H FAIL stands (D-049, D-050); no causal claims; H4 rejected; R1 limitation stands
- Integration tests I03 and I05 never built; cross-machine and GPU determinism untested

## Next actions (≤5)
1. Implement conductance/process, x5_kernel/x5_context, lineage/run with independent tests; commit before data
2. Run the exact-process/calibration gate once; report; STOP (no training; X4-F code reuse still blocked)
3. No implementation, sampling, fitting, extraction, PH, intervention or training before approval; no Phase C, coverage extension, threshold change, intervention, training, merge, push or tag change
