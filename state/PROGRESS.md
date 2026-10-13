# Progress (updated 2026-10-14 by conductor, claude-opus-5-5; branch x4-phase-b2)
Stage: **X4 Phase B2 running** (oracle-only coverage extension, protocol x4b2-v1, D-053) | Phase B: complete — INCONCLUSIVE (D-052, unchanged) | Last exit reached: E4 (tagged, local), with documented G-H failure

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
| analysis | accepted (a–e) | A | part (e) horizon feasibility (Phase B) |
| learner | accepted | B | V override for U (V = 144) |
| activations | accepted | B | dev extraction via ActivationStage |
| experiment | S0–S8, X4, reports E0–E4; X4 Phase B adapter; B2 lineage adapter in progress | A | not registered stages, no config change |
| integration | I01, I02, I04, I06 | B | I03, I05 never built (gap, reported) |

## Gates
| gate | verdict | date | key value |
|---|---|---|---|
| G-S0, G-A … G-F (S4, S5) | pass | 2026-10-13 | unchanged since E3 |
| G-G | pass | 2026-10-13 | unchanged |
| G-H | **FAIL** | 2026-10-13 | rerun_ok only (D-049); unchanged |
| X4 Phase B (protocol-local) | **INCONCLUSIVE** | 2026-10-13 | all 4 pools UNDERCOVERED (D-052); unchanged |
| X4 Phase B2 (protocol-local) | running | 2026-10-14 | x4b2-v1 frozen before sampling (D-053) |

## Open issues (≤5)
- Phase B INCONCLUSIVE on coverage stands; B2 is a new check, not a repair of B
- Strict Q1 sufficiency on reachable beliefs unresolved; no model examined in B or B2
- G-H FAIL stands (D-049, D-050); no causal claims; H4 rejected; R1 limitation stands
- Integration tests I03 and I05 never built; cross-machine and GPU determinism untested

## Next actions (≤5)
1. Implement and test the B2 lineage adapter, then run x4b2-v1 once (four 16,384-trajectory pools, one at a time)
2. Write docs/proposals/X4B2_COVERAGE_REPORT.md; record the B2 outcome as a new decision
3. STOP for owner review; no Phase C, third extension, fitting or training without a new instruction
