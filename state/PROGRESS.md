# Progress (updated 2026-10-13 by conductor, claude-opus-5-5)
Stage: S4 + X4 complete; E2 report built, unblinded; awaiting H4 (README E2, tag E2) | Wave: WX4 built | Last exit reached: E1 (tagged)

## Modules
| module | status | owner tier | notes |
|---|---|---|---|
| contracts | accepted (frozen 1.0.0) | A / TW | 95 tests; style-only line wraps since freeze |
| tools | accepted | C | Makefile + tasks.ps1 |
| world | accepted | B / TW | 30 tests |
| process | accepted | B | 38 tests |
| topology | accepted | B / TW | 31 + 3 slow (G-A calib) |
| executors | accepted | B | 27 tests |
| dataset | accepted | B | 18 tests |
| oracle | accepted | B / TW | 17 tests, brute force |
| prediction | accepted (a,b,c) | B | run_probes used in S7 |
| analysis | accepted (a,b,d) | B / TW | F1 rule, Δgeom (D-031), R0–R3, null, layer sweep; (d) readout helpers (WX4); part (c) W5 |
| learner | accepted | B | pre-LN transformer, deterministic trainer |
| activations | accepted | B | hook extraction at p = 32 |
| experiment | S0–S6, X4 + report E0/E2(+X4) | A / TW (X4) | idempotent re-runs (D-032); H4 rule D-034; S7–S8 todo |

All module suites: 449 passed, 5 deselected (slow/integration); check_imports clean; ruff clean.

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

## Open issues (≤5)
- R1 (last-symbol embedding) reaches 0.47–0.89 of the model's F1 contrast under O (exploratory, reports/E2/exploratory.md); P (S5, H3′) is what separates emission geometry from history
- E2 report: N run's learning-gate cell shows "fail" (G_C = 0); should read "n/a" (cosmetic, before README E2)
- H3 decidable one-sidedly only; H3′ approved (D-037), decided under P only
- process.is_x_periodic detects periodicity by family name (or an identification string); fix before any extension (prompt 3)
- Extensions suggested by review (horizons, density, curvature, optimisation, orientability, sheaves) deferred to research planning after E3 (D-040)

## Next actions (≤5)
1. H4: owner approves the E2 finding sentence; then README at E2 (+ N gate cell fix) and tag E2.
2. S5 (6 P runs, ~1.6 h) on LocalExecutor; then X4 with sources [S4, S5] (H3′ decision) and `stage S6` (O + P) → E3 report.
3. experiment: S7–S8 stages; E3/E4 report levels.
