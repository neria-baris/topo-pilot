# Progress (updated 2026-10-13 by conductor, claude-opus-5-5)
Stage: S3 done (G-E pass) | Wave: W4 built (S4/S5 jobs + analysis) | Last exit reached: E1 (tagged) | **Waiting: H2**

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
| experiment | S0–S5 implemented | A | idempotent re-runs + per-gate requires (D-032); S6–S8 todo |

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
1. H2: owner approves S4 plan (6 new runs + analysis, LocalExecutor CPU, ~1.6 h + analysis).
2. Run `topo-pilot stage S4 --config configs/stages.yaml`; evaluate G-F; E2 report; H4 for the E2 README sentence.
3. S5 (6 P runs, ~1.6 h) on the same executor; then S6 (dynamics, checkpoint-order null, layer sweep) → E3.
4. experiment: implement S6–S8 stages and report levels E2/E3.
