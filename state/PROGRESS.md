# Progress (updated 2026-10-13 by conductor, claude-opus-5-5)
Stage: S4 running (H2 approved, D-033) | Wave: W4 built (S4–S6 + E2 report) | Last exit reached: E1 (tagged)

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
| analysis | accepted (a,b) | B / TW | F1 rule, Δgeom (D-031), R0–R3, null, layer sweep; part (c) W5 |
| learner | accepted | B | pre-LN transformer, deterministic trainer |
| activations | accepted | B | hook extraction at p = 32 |
| experiment | S0–S6 + report E0/E2 | A | idempotent re-runs (D-032); H4 rule D-034; S7–S8 todo |

All module suites: 379 passed, 3 deselected (slow); check_imports clean; ruff clean.

## Gates
| gate | verdict | date | key value |
|---|---|---|---|
| G-S0 | pass | 2026-10-13 | contracts green |
| G-A | pass | 2026-10-13 | S_cyl 0.299, S_sq 0.037, synthetic 20/20 |
| G-B | pass | 2026-10-13 | oracle brute force; N, U controls exact |
| G-C | pass | 2026-10-13 | σ = 1.25 first-pass |
| G-D | pass | 2026-10-13 | no latent fields; learner→sidecar LEAKAGE |
| G-E | pass | 2026-10-13 | captured 0.986; 22k tok/s, 16 min/run; S4 proj 1.6 h |

## Open issues (≤5)
- H3 decidable one-sidedly only (P: oracle b32 shows 5/8)
- process.is_x_periodic detects the cylinder by name (extension fragility)
- Δgeom same-last-symbol pairs: d_B1 ≡ 0 there (D-031), so the term reduces to ρ_s(d_A, d_B32)

## Next actions (≤5)
1. S4 is running (`topo-pilot stage S4`; re-running resumes: stored runs are reused). Then G-F.
2. `topo-pilot report --level E2`; present the E2 finding sentence at H4; README at E2; tag E2.
3. S5 (6 P runs, ~1.6 h) on the same executor; then `stage S6` (O + P) → E3 report.
4. experiment: S7–S8 stages; E3/E4 report levels.
