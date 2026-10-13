# Progress (updated 2026-10-14 by conductor, claude-opus-5-5; branch e4-circular-audit)
Stage: **E4 circular-baseline audit complete — BEYOND_SYMBOL_AND_MIXING (descriptive)** (D-057; circ-audit-v1, D-056) | Practical Q2-gap branch closed by owner (D-055) | Phase B INCONCLUSIVE (D-052) · B2 NO-GO (D-054) · H4C-I decoder experiment: NOT RUN — stopped at feasibility gate | Last exit reached: E4 (tagged, local), with documented G-H failure

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
| E4 circular-baseline audit (descriptive) | **BEYOND_SYMBOL_AND_MIXING** | 2026-10-14 | 24/24 run-panels: model 0.884–0.892 > A*_symbol 0.817 and best baseline; S7 rows reproduced exactly; 79 CPU s, 0.41 GB (D-057) |

## Open issues (≤5)
- Closure is scoped (cylinder O, σ 1.25, horizon 2, p32, registered screen); strict Q1 sufficiency UNRESOLVED; no general sufficiency proof and no decoder ceiling measured
- Circular audit is descriptive and in-sample on unblinded data; it does not separate short-context (w31,w32) from long-history information, nor show causal use or H1 necessity
- G-H FAIL stands (D-049, D-050); no causal claims; H4 rejected; R1 limitation stands
- Integration tests I03 and I05 never built; cross-machine and GPU determinism untested

## Next actions (≤5)
1. **STOP: owner review of docs/proposals/CIRCULAR_BASELINE_AUDIT_REPORT.md**
2. Recommendation: planning (not running) a coordinate causal-use test is justified, with short-context and held-out recoverability controls; no intervention without separate approval
3. No Phase C, coverage extension, threshold change, intervention, training, merge, push or tag change
