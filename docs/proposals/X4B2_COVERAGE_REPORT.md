# X4 Phase B2: coverage-extension report

14 October 2026.

| | |
|---|---|
| Protocol | [x4b2-v1](X4B2_COVERAGE_PROTOCOL.md), frozen before sampling (D-053, commit a50e166) |
| Branch | `x4-phase-b2` (continues `x4-phase-b`) |
| Code | commit c62590a |
| Tables | [X4B2_OUTPUTS/](X4B2_OUTPUTS/) |
| Independent store | `topo-pilot/x4b2-research-store/`: MetricRecords `49ee640ccf257be7`; npz exports of each pool's canonical tokens and screen arrays; checksums are in `pools.json` and `run.json` |

Phase B ([report](X4_FEASIBILITY_REPORT.md)) remains **INCONCLUSIVE**. B2 is a new check, not a revision of B. **Stopped after B2.**

## Verdict

| Question | Verdict | Basis |
|---|---|---|
| (i) Ambient algebra | **ALLOWS_STABLE** (inherited) | Recomputed G1/G2, spectra and ρ match Phase B's `ambient.json` exactly (max differences 0). |
| (ii) Practical reachable gap | **NO_GAP** | All four pools covered (141–159 eligible anchors ≥ 128), with 0 witnesses in every pool. |
| (iii) Strict sufficiency of Q1 on the reachable set | **UNRESOLVED** | No exact reachable witness. A sampled negative is not proof of sufficiency. |
| (iv) Overall | **NO-GO** | Covered pools show no material gap, consistently. Every validity, separation, permutation and precision check passed. |

**Scope of the NO-GO.** It covers cylinder O, 12×12, σ 1.25, the original T/E and π, horizon 2 (joint Q2), the belief at p32, and the frozen screen: same-symbol 5-nearest Q1 neighbours, H(Q1) ≤ 0.01, H(Q2) ≥ 0.05. It is a sampled result for four pools of 16,384 trajectories. It is not a theorem about every reachable belief. It also does not prove that Q1 is sufficient: Q2 does strictly refine Q1 on the full simplex.

## Lineage and separation

The four pools are repetitions of sampling from one process, not independent worlds or models.

| Pool | Stream seed | Sequence-ID process code | First-token χ² p | Tokens export sha256 (prefix) |
|---|---|---|---|---|
| reference | 4472965773301758267 | 2076810545 | 0.377 | 9bf08552… |
| repetition1 | 9041520877900685805 | 662554568 | 0.793 | 6e2faa9e… |
| repetition2 | 1190608976536703855 | 31366180 | 0.539 | e8544a70… |
| repetition3 | 264034718665583389 | 2024988825 | 0.256 | 0842e839… |

* **Frozen values.** All seeds and codes equal the values frozen in the protocol; the code rejects any other value. The process identity check passed:
  - same T, π and EmissionSpecs as Phase B;
  - identical canonical E (difference 0);
  - π stationary to 9e-19;
  - all §3 future-map checks pass.
* **No latent states kept.** States were drawn by `HMMSampler` and discarded immediately; none was persisted.
* **Separation checks:**
  - sequence IDs are disjoint from all 3,342,336 IDs in the 72 stored ObservationSets, and pairwise disjoint between pools;
  - 0 identical 32-symbol windows with the old cylinder-O test, dev or train data, or between pools;
  - each pool holds 16,384 distinct windows.
* **Main store.** Its listing hash (2,568 files) was identical before and after the run.

## Reachable screen (`pools.json`, `anchors_*.csv`)

Each pool used 512 anchors with 5 same-symbol partners each, i.e. 2,560 slots. The last-symbol groups held 400–518 candidates. No anchor had fewer than 5 candidates, and no identical-history pair occurred.

| Pool | Eligible (≥ 128?) | Witnesses | Status | Admissible pairs | Max d2 over admissible pairs | Median nearest d1 |
|---|---|---|---|---|---|---|
| reference | 159 (yes) | 0 | NO_MATERIAL_GAP | 276 | 0.0130 | 0.015 |
| repetition1 | 141 (yes) | 0 | NO_MATERIAL_GAP | 228 | 0.0127 | 0.015 |
| repetition2 | 159 (yes) | 0 | NO_MATERIAL_GAP | 269 | 0.0129 | 0.016 |
| repetition3 | 156 (yes) | 0 | NO_MATERIAL_GAP | 254 | 0.0125 | 0.015 |

**Descriptive only:**

* **The witness threshold is not approached.** Across all 10,240 primary slots, d2/d1 lies between 1.11 and 1.48, with a median of about 1.18. The largest d2 among pairs with d1 ≤ 0.02 is 0.024–0.025, against the witness threshold of 0.05.
* **Sanity checks.** No pair violates d2 ≥ d1. No exact Q1 tie occurs. A partner is reused at most 3 times.
* **Eligibility vs entropy.** Eligible and non-eligible anchors have overlapping posterior entropy, 1.7–2.8 nats.
* **Secondary screen.** Without the same-symbol restriction: 213–229 eligible anchors per pool, 0 witnesses, max admissible d2 0.0154, ratio ≤ 1.93.
* **Coverage margin.** Coverage cleared the floor with a modest margin: the smallest pool had 141 eligible anchors against 128.
* **Same pattern as Phase B.** These distances reproduce what Phase B saw with 4,096-trajectory pools. The denser pools moved the median nearest d1 from about 0.029 to 0.015, but not the Q2/Q1 relationship.

## Agreement and validity checks

All four pools pass their validity checks:

* Q1/Q2 rows sum to 1 within 8e-16.
* Σ_j Q2 = Q1 within 4e-16.
* Every entry is nonnegative.

**Permutation (reference pool).** Recomputed in replicate 1729's vocabulary:

* beliefs are identical (difference 0);
* partners and flags are identical;
* distances differ by at most 6e-17.

**Precision.** Recomputing d2 from float32-cast Q2 changes distances by at most 5.9e-9. No witness flips and no pool status changes.

## Code, cost and notes

* **Code.** B2 reuses `HMMSampler`, `BayesFilter`, `FutureOperator` and the unchanged x4b-v1 analysis and screen code. It adds one lineage adapter, `experiment/x4b2.py`, plus the run module `x4b2_run.py`.
* **Tests.** 6 new adapter tests, and 227 passing across the analysis and experiment suites. Ruff, import and file-size checks are clean.
* **Inherited code notes:**
  - the zero-map guard in `tangent_audit` (5b2f384), inert here: the ambient result was reproduced bit-for-bit;
  - the corrected memory query (741333c), which measured correctly in this run.
* **Cost.** 48.9 CPU-s and 33.7 s wall, against a cap of 3,600 CPU-s. Peak working set **1.19 GB**, against the 8 GB target. The external store holds about 93 MB, mostly p32 belief exports; within Phase B's ≤ 100 MB planning bound.
* **Process.** There was one run, with no threshold changes, no re-sampling and no pool enlargement. Nothing was fitted. No checkpoint, activation or EvalSidecar was read.

## What this licenses — and what it does not

**Can be stated.** For this process at p32, the joint two-symbol future carries extra distinctions on the full belief simplex. But among beliefs the process actually produces, at the screen's resolution, near-equal Q1 implies near-equal Q2: H(Q2) ≈ 1.2 × H(Q1), and no near-Q1 pair reached half the 0.05 witness distance. The practical horizon-gap premise behind the proposed H4C-I test is not supported at this horizon and resolution.

**Cannot be stated:**

* That Q1 is information-theoretically sufficient for Q2 on all reachable beliefs.
* Anything about the trained models, their representations or decoders, since none was examined.
* Anything about other horizons, positions, processes, emission widths or finer Q2 differences below the 0.05 screen.
* Anything about topology or causality.

## Recommendation (one)

**Close the practical Q2-gap hypothesis at p32 for this process (NO-GO, scoped as above), and do not propose Phase C.**

The reasons:

1. **The frozen rule is met cleanly.** All four pools are covered and show no witness, so the outcome is consistent.
2. **The result is far from the threshold.** The largest admissible Q2 distance (0.013) is about four times below the witness threshold, and the Q2/Q1 ratio is stable across pool sizes. A modestly different screen is unlikely to reverse it.
3. **It removes Phase C's rationale.** Phase C's H4C-I test was premised on a residual horizon gap. Running it now would mainly measure decoder capacity against an information ceiling.

Phase B's INCONCLUSIVE verdict is unchanged.

**STOP — owner review.**
