# Progress (updated 2026-10-13 by conductor, claude-opus-5-5)
Stage: S5 + X4 (S4, S5) + S6 complete; H4 approved (D-046) | Last exit reached: E3 (tagged, local)

## Modules
| module | status | owner tier | notes |
|---|---|---|---|
| contracts | accepted (frozen 1.0.0) | A / TW | 95 tests; style-only line wraps since freeze |
| tools | accepted | C | Makefile + tasks.ps1 |
| world | accepted | B / TW | 30 tests |
| process | accepted | B | 42 tests; is_x_periodic from complex (D-043) |
| topology | accepted | B / TW | 31 + 3 slow (G-A calib) |
| executors | accepted | B | 27 tests |
| dataset | accepted | B | 18 tests |
| oracle | accepted | B / TW | 17 tests, brute force |
| prediction | accepted (a,b,c) | B | run_probes used in S7 |
| analysis | accepted (a,b,d) | B / TW | F1 rule, Δgeom (D-031), R0–R3, null, layer sweep; (d) readout helpers (WX4); part (c) W5 |
| learner | accepted | B | pre-LN transformer, deterministic trainer |
| activations | accepted | B | hook extraction at p = 32 |
| experiment | S0–S6, X4 + report E0/E2/E3 | A / TW (X4) | idempotent re-runs (D-032); H4 rule D-034; S6 x4curves + E3 report (D-044); S7–S8 todo |

All module suites: 459 passed, 5 deselected (slow/integration); integration 2 passed; check_imports clean; ruff clean.

## Gates
| gate | verdict | date | key value |
|---|---|---|---|
| G-S0 | pass | 2026-10-13 | contracts green |
| G-A | pass | 2026-10-13 | S_cyl 0.299, S_sq 0.037, synthetic 20/20 |
| G-B | pass | 2026-10-13 | oracle brute force; N, U controls exact |
| G-C | pass | 2026-10-13 | σ = 1.25 first-pass |
| G-D | pass | 2026-10-13 | no latent fields; learner→sidecar LEAKAGE |
| G-E | pass | 2026-10-13 | captured 0.986; 22k tok/s, 16 min/run; S4 proj 1.6 h |
| G-F | pass | 2026-10-13 | S4: 7 runs × 12 checkpoints (84 Checkpoint, 84 ActivationSet); analysis done ~13:15 local |
| G-F (S5) | pass | 2026-10-13 | P: 6 runs × 12 checkpoints; captured 0.874–0.914 |

## Open issues (≤5)
- E3 verdicts (D-045/D-046): H3 rule REJECTED under P (uninformative by design); H4 REJECTED (raw S rises at step 50 in both worlds; regret < G_C at 100); H3′ SUPPORTED under P
- R1 limitation stands: history integration vs learned symbol-level transition statistics undecided (README caveat 3; reports/E3/exploratory.md)
- No interventions: V3/V4 and H3′ are representational, not causal
- Extensions suggested by review (horizons, density, curvature, optimisation, orientability, sheaves) deferred to research planning after E3 (D-040)

## Next actions (≤5)
1. STOP: wait for the owner before starting S7, S8, X4-causal, X5, X6 or any extension.
2. Candidate follow-ups (each needs its own preregistration): contrast-based dynamics rule on a denser early grid; embedding-level control (reports/E3/exploratory.md §9).
3. Tags E0–E3 are local only; push only on explicit owner instruction.
