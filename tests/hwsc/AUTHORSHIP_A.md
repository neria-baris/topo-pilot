# tests/hwsc, author A (job 0176)

Independent test author A, clean context, working from the specification at commit 70e8e27 (`tools/hwsc/PROTOCOL_HWSC_v1.md`, `API.md` incl. §18 rulings R-0176-G1…G12, `CONTRACT.json`, `TEST_PLAN.md` §1–§2). Task `agent-handoff/jobs/0176/task.md` (sha256 4A697742…4A12, verified before starting).

## Files (author A only)

| File | Tests | Scope (TEST_PLAN §2) |
|---|---|---|
| `test_a_decision.py` | 27 | `k4b_stats.model_status`/`overall` under `bound_stage_c()`; boundaries; `positive_below_margin`; `annotations` (DRC5) |
| `test_a_outcomes.py` | 44 | `outcome` precedence, `state_from_gates`, `licence` heads and sentences, §6.4 disclosure |
| `test_a_ladder.py` | 27 | `p1c_ladder` = `hwsb_gates.ladder_pilot` = an independent re-implementation; seed-sensitive fixture; mean-shift invariance; `choose_N`; `registry_risk`; `p_d2a_check` (DRC6) |
| `test_a_learning.py` | 8 | `l1` on planted predictives (DRC7) |
| `test_a_law.py` | 10 | `law_identity`, `exclusion_check`, `load_handoff` values, w0 enclosure (DRC8) |
| `test_a_k4b_known_bound.py` | 33 | KC8: Proposition 1 (exact enumeration), Theorem A, Lemma N, cap/F/F_plan, §8.1 boundaries, ranks, `write_sealed`, chart equality, restoration |

## What I read

- `agent-handoff/jobs/0176/task.md`; `topo-pilot-hws/CLAUDE.md`.
- `tools/hwsc/PROTOCOL_HWSC_v1.md` (§2–§6), `tools/hwsc/API.md` (all), `tools/hwsc/TEST_PLAN.md` (all), `tools/hwsc/CONTRACT.json` (sections `licences`, `outcomes`, `annotations`, `thresholds`, `handoff`, `seeds`, `masters`, `gates`, `known_cases`, `tests`, `disclosure`).
- Public documents of reused modules: `tools/k4b/PROTOCOL_K4B_v1.md` (§0, §1, §5, §6, §7, §8, §11.3–§11.4), `tools/k4b/CERTIFICATE.md`, `tools/k4b/API.md`; `tools/hwsb/API.md` (entries for `build_process`, `b1`, `model_predictive`, `oracle_predictives`, `law_bound`, `bound_law`, `ladder_pilot`, `w0_process`, `kb4`); `tools/x4_circle_history/API.md` (`precision`); `tools/c1prime/API.md` (`c1_means`).
- Signatures and docstrings only (via `inspect`) of reused public functions: `k4b_stats`, `k4b_cert`, `k4b_scores.endpoint_arrays`, `k4b_config.check_chart_equality`, `c1_means`, `c1_bounds.B_constant`, `hwsb_gates.ladder_pilot`, `hwsb_eval.b1`, `hwsb_known.w0_process`, `hwsb_law.law_bound`, `hws_oracle.kl_rows`, `hws_exact.p_d2a`, `c1_records.C1GateFailure`.
- Behaviour probes of reused functions on synthetic inputs (scratch under `X:/Downloads/topo-scratch/test_hwsc-0176/authorA/`): `b1` at p = q32, q1, G_C = 0 and a NaN row; `k4b_stats.bounds` return shape; `c1_bounds.B_constant` against the CERTIFICATE §6 formula.

## What I did not read

- I did **not** open, list, search or import-inspect any `tools/hwsc/*.py` file (the code under test). My tests only import those modules and call them.
- I did **not** read any `tests/hwsc/test_b_*` file (author B), nor `tests/k4b` or `tests/hwsb` test code.
- I did not open the public research-summary paths, `hwsb-store/REPORT.json`, `hwsb-store/stages/EVAL/`, `hwsb-store/GATES.jsonl`, `hwsb-store/CHART_CONSTRUCTIONS_*.json`, `agent-handoff/jobs/0175/` or any `payload.npz`, `state.pt`, `sealed/` or `hist/**` array. `hwsb-store/HANDOFF.json` is read only by the code under test (`cc.load_handoff`) in `test_a_law.py`.

## Hygiene

Synthetic and in-memory only (Dirichlet predictives, planted float arrays, a 3-state rational HMM, `MemoryBackend` builders of w\* and w0 that draw nothing). Files are written only under pytest `tmp_path`. Run with `-s`, `PYTHONPATH=<worktree>/src`, TEMP/TMP/TMPDIR and `--basetemp` under `X:/Downloads/topo-scratch/test_hwsc-0176/authorA/`. No formatter was run; `ruff check` (lint only) on these six files by name.

## Readings of open details (marked `# API-AMBIGUITY:` in the tests)

1. **Registry-risk equality at 1/100** (`test_a_ladder.py`). `registry_risk` uses `Fraction(float(p))`, which is dyadic, so `rows · Fraction(float(p)) = 1/100` exactly is unattainable. The boundary is tested at float resolution: the largest float p with `rows·p ≤ 1/100` passes, the next float fails.
2. **Exact 0.8 in L1** (`test_a_learning.py`). Found by bisection on a mixture weight and `hwsb_eval.b1` (a reused function); the test skips only if no float mixture gives captured == 0.8 exactly (it did not skip).
3. **NaN predictive row** may surface as `C1GateFailure` or as the reused `hws_worlds.HwsStop` from `kl_rows`; both carry `FAIL_TECHNICAL/NUMERICAL`, which is what is asserted.
4. **`l1` return value** ("per-model records"): accepted as the L1 record shape (`per_model`) or a dict keyed by model.
5. **`state_from_gates` L1 details**: supplied both in the gate record (`k`, `models`) and as `l1_record`.
6. **"Empty state"** for `outcome`: tested both as all keys None and as `{}`.
7. **FRESH_B4_LOW in the ENDPOINT result**: the flag's location is not pinned; the planted `fresh_B4` carries every plausible marker.
8. **Per-model `UNRESOLVED/NUMERICAL` annotation**: accepted with or without a model suffix.
9. **Boundary statuses**: at `L − F− = 1/100` (or `U + F+ = 1/100`, or `L − F− = −1/100`) with F > 0, the same L, U with F = 0 are definite, so the status is `UNRESOLVED/NUMERICAL` (an UNRESOLVED status), which the tests assert exactly.
10. **§6.4 disclosure byte equality**: the protocol is Markdown, so `w\*` is read as `w*` before comparing with CONTRACT `disclosure`.
