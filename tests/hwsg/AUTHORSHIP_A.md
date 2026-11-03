# HWSG tests, author A (job 0224)

Clean-context test author A. I am not the implementer and did not read `tools/hwsg/*.py` or author B's files.

## What I read
- `tools/hwsg/PROTOCOL_HWSG_v1.md` (by section reference), `API.md`, `CONTRACT.json`, `TEST_PLAN.md`, and `agent-handoff/jobs/0224/task.md` plus `RULINGS.md`.
- Public signatures and docstrings of the reused modules: `k4b_stats` (`joint_bootstrap`, `bounds`, `model_status`, `overall`), `k4b_fresh.bootstrap_inputs`, `k4b_cert` (`F_plan`, `norm_bound`, `transport_bound`), `hwsb_law` (`law_bound`, `bound_law`, `softmax_enclosure_rounded`, `rounding_delta`), `hwsc_outcome`, `c1_means`, and the statements in `tools/k4b/PROTOCOL_K4B_v1.md` (Proposition 1, Theorem A, Lemma N).
- Hash-checked JSON records, read-only: `hws-store/stages/FINAL/REPORT.json`, the S3 world records, `hwsb-store/HANDOFF.json`.
- I did not read `tests/k4b` or `tests/hwsc`. The KG6 port is written from the protocol statements.

## Files
| File | Covers |
|---|---|
| `test_a_selection.py` | O0 rule recomputed independently from the hashed records; agreement with `go.selection`; synthetic REPORT fixtures for a tie, an UNAVAILABLE world, changed bytes and a wrong registered triple; O5 headroom (OPEN-13) |
| `test_a_law.py` | exact σ and neighbour override (lo 1/24, mid 1/5, hi 1/8); the float-repr neighbour refused; `go.law` per world against CONTRACT `Z_exact_upper` and `k4b_cert.F_plan`; F_plan > 1/1000, Z off by one in the numerator and non-BOUNDED all give `LAW_BOUND`; w* Z and F_plan equal HANDOFF; at σ 5/4, δ = 0 and the enclosure equals the original; the O3 float boundary |
| `test_a_kg6_port.py` | inside `gb.world("hi")`, with restoration checked: Proposition 1 by exact enumeration (3-state HMM, L = 6, K = 2); Theorem A completion grid and extremes; Lemma N coverage, including s = 0, tiny values and an adversarial n̂; transport bound on planted reports; decision equalities; POSITIVE_BELOW_MARGIN; `overall` on the hi masters |
| `test_a_ratio.py` | `D_KEY`; draws bitwise equal to `joint_bootstrap(bootstrap_inputs)`; KG7 fixture with c ∈ {1/2, 9/10, 3/2}; rank 84 and rank 4,917 from an independent sort; seed sensitivity; values left unclipped; `ratio_gate` DEFINED, identity mismatch → NUMERICAL, D_L ≤ 0, a single D* = 0 (OPEN-11) and B4 not passed → RATIO_UNRESOLVED |
| `test_a_cross.py` | `general`, including the RC-1 boundaries (SUPPORT + MIXED without EXCLUDE → GENERAL_UNAVAILABLE; a P1-passed MIXED world containing EXCLUDE → NOT_GENERAL, naming the world and model; EXCLUDE without P1 is not counted); `capture` with ρL exactly 1/2, ρU exactly 1/2, unresolved worlds and the order (OPEN-7); `annotations`; `similarity`, with spread pairing from an independent PCG64(620640) computation (OPEN-8) |
| `test_a_outcomes_licences.py` | `grec.outcome_g` precedence rows; licences (SUPPORT, EXCLUSION, NOT_GENERAL, CAPTURE_AT_LEAST_HALF, GENERAL_UNAVAILABLE "n/a", SIMILARITY wording); the disclosure and does-not-establish items 1–26 |

## Independent computations
- The selection rule (argmin, argmax and log-midpoint, ties going to the first in order).
- Exact Fraction neighbours.
- A float bisection for the O3 boundary.
- Exact HMM enumeration.
- Squared-bracket coverage for Lemma N.
- Numpy sort ranks 84, 125, 4,875 and 4,917.
- A PCG64(620640) permutation of the spread.

## Markers
- `# OPEN-7`, `OPEN-8`, `OPEN-11` and `OPEN-13`, plus OPEN-6 for the dry endpoint seed 620913.
- `# API-AMBIGUITY` (each test accepts every reading the API allows):
  1. `selection` may read CONTRACT values through `gc.CONTRACT` at call time. The fixtures patch `gc.CONTRACT["selection"]`.
  2. `identity` and `d2a` may return `ok: False` or raise or return the status.
  3. The output directory of `ratio_gate` is not named in its signature. `ctx` carries both `out` and `world_dir`.
  4. Planted CROSS summaries:
     - per-model `rhoL` and `rhoU` are floats;
     - the ratio status is set at both world and model level;
     - central intervals are given both as floats and in the `k4b_stats.bounds` shape (`central95_minus`);
     - the similarity label is either a boolean `compatible` or a string.
  5. The SIMILARITY licence fill may be a word or a boolean.
  6. Rank-3 statuses (REGISTRY_RISK, ORACLE_FEASIBILITY, REGISTRY_INCOMPLETE) are planted in the `k4b` slot of the outcome state.

## Hygiene
- Synthetic data, in memory or under pytest `tmp_path`.
- No array file is written or committed.
- Basetemp and TEMP are under `X:/Downloads/topo-scratch/test_hwsg-0224/a/`.
- No formatter was run.
