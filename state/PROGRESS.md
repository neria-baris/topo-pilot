# Progress (updated 2026-10-13 by conductor, claude-opus-5-5)
Stage: S2 done (H1 approved) | Wave: W3 building | Last exit reached: E1 (tagged)

## Modules
| module | status | owner tier | notes |
|---|---|---|---|
| contracts | accepted (frozen 1.0.0) | A / TW | 95 tests |
| tools | accepted | C | Makefile + tasks.ps1 |
| world | accepted | B / TW | 30 tests |
| process | accepted | B | 38 tests |
| topology | accepted | B / TW | 31 + 3 slow (G-A calib) |
| executors | accepted | B | 27 tests |
| dataset | accepted | B | 18 tests |
| oracle | accepted | B / TW | 17 tests, brute force |
| prediction | accepted (a,b,c) | B | run_metrics W4, run_probes W5 |
| analysis | accepted part (a) | B / TW | parts (b),(c) in W4/W5 |
| learner | todo | B | W3 |
| activations | todo | B | W3 |
| experiment | S0–S2, report E0, prereg | A | runner/gates full in W4 |

## Gates
| gate | verdict | date | key value |
|---|---|---|---|
| G-S0 | pass | 2026-10-13 | contracts green |
| G-A | pass | 2026-10-13 | S_cyl 0.299, S_sq 0.037, synthetic 20/20 |
| G-B | pass | 2026-10-13 | oracle brute force; N, U controls exact |
| G-C | pass | 2026-10-13 | σ = 1.25 first-pass |
| G-D | pass | 2026-10-13 | no latent fields; learner→sidecar LEAKAGE |

## Open issues (≤5)
- E1 README sentence needs H4 approval
- H3 decidable one-sidedly only (P: oracle b32 shows 5/8)
- ~40 lines over 100 chars (style cleanup by Tier C)
- process.is_x_periodic detects the cylinder by name (extension fragility)

## Next actions (≤5)
1. After H1: commit PREREGISTRATION.md, tag E1, README at E1 (needs H4).
2. W3: learner ∥ activations (brief both; PublicTokenDataset is the only loader).
3. S3 smoke run + CPU throughput → H2 (executor choice).
