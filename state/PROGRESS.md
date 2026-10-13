# Progress (updated 2026-10-13 by conductor, claude-opus-5-5)
Stage: S7 + S8 complete; H4 approved (D-050) | Wave: W5 done | Last exit reached: E4 (tagged, local), with documented G-H failure

## Modules
| module | status | owner tier | notes |
|---|---|---|---|
| contracts | accepted (frozen 1.0.0) | A / TW | 95 tests |
| tools | accepted | C | Makefile + tasks.ps1 |
| world | accepted | B / TW | 30 tests |
| process | accepted | B | is_x_periodic from complex (D-043) |
| topology | accepted | B / TW | CircularCoordinates (T12 slow) used in S7 |
| executors | accepted | B | 27 tests |
| dataset | accepted | B | PanelBuilder reused for dev panels (D-047) |
| oracle | accepted | B / TW | kernels reused for dev beliefs |
| prediction | accepted (a,b,c) | B | RidgeProbe; run_probes stub, I/O in experiment (D-047) |
| analysis | accepted (a–d) | B / TW | part (c): Sensitivity, CircularCorrespondence, N13/N20–N25 |
| learner | accepted | B | V override for U (V = 144) |
| activations | accepted | B | dev extraction via ActivationStage |
| experiment | S0–S8, X4, reports E0–E4 | A / TW | S7 (D-047), S8 + G-H (D-048), X17–X25 |
| integration | I01, I02, I04, I06 | B | I03, I05 never built (gap, reported) |

Suites: module 511 passed (7 deselected), slow 3 passed, integration 4 passed; imports, file sizes, ruff clean.

## Gates
| gate | verdict | date | key value |
|---|---|---|---|
| G-S0, G-A … G-F (S4, S5) | pass | 2026-10-13 | unchanged since E3 |
| G-G | pass | 2026-10-13 | 4 runs + 5 analysis records documented, no failures |
| G-H | **FAIL** | 2026-10-13 | rerun_ok only: 307/307 shared artifacts bitwise equal, 1 rerun-only run_timing record (D-049); integrity 785/785, reports 9/9, tests pass |

## Open issues (≤5)
- G-H FAIL stands (D-049, D-050): rerun reproduced 307/307 shared artifacts bitwise and 6/6 gate verdicts; one historical run_timing record missing from the original store; same machine, 1 of 17 runs repeated
- No causal claims: all evidence is representational; X4-causal not run
- H4 rejected; R1 last-symbol limitation stands (circular statistic has no last-symbol baseline)
- Probes decode b32 no better than the exact next-symbol distribution; λ at grid edge under O
- Integration tests I03 and I05 never built; cross-machine and GPU determinism untested

## Next actions (≤5)
1. STOP: E4 reached and tagged locally; wait for the owner
2. Do not push; do not start X4-causal, X5, X6, extensions or any training without a new owner instruction
3. Candidate follow-ups (each needs its own preregistration): circular statistic on R1/b1/R2/R3; non-linear probes vs the F1 baseline; interventions along the circular coordinate
