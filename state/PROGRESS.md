# Progress (updated 2026-10-13 by conductor, claude-opus-5-5)
Stage: S5 running (LocalExecutor, CPU; started 2026-10-13 after commit eadd330) | Wave: E3 tooling built (D-044) | Last exit reached: E2 (tagged)

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

All module suites: 450 passed at E2 (+4 process, +5 experiment since), 5 deselected (slow/integration); check_imports clean; ruff clean.

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
- H3 decidable one-sidedly only; H3′ approved (D-037), decided under P only
- Extensions suggested by review (horizons, density, curvature, optimisation, orientability, sheaves) deferred to research planning after E3 (D-040)

## Next actions (≤5)
1. If S5 was interrupted: re-run `topo-pilot stage S5` (stored runs are reused, D-032); check `topo-pilot status` (Checkpoint count 84 → 156 when done).
2. Then `topo-pilot stage X4` (sources [S4, S5]; verify O rows equal record 78c86738c6c8ae34), then `topo-pilot stage S6` (O + P; needs X4 first for x4curves).
3. `topo-pilot report --level E3`; conductor writes reports/E3/discussion.md (post hoc, labelled); STOP at H4 (no README change, no E3 tag before owner approval).
4. Not in scope before approval: S7, S8, X4-causal, X5, X6.
