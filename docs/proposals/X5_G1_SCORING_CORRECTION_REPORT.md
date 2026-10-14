# X5 G1 technical benchmark — deviation addendum and scoring-only correction

14 October 2026, handoff job 0009.

* Additive to [the v1 report](X5_G1_TECHNICAL_BENCHMARK_REPORT.md).
* The v1 protocol, report and outputs are unchanged and are **not** relabelled as conforming.
* This is technical fixture timing only, not a scientific result.

## 1. v1 deviations (disclosed; v1 outputs preserved)

**v1 evidence.**

| Item | Value |
|---|---|
| Protocol | `X5_G1_TECHNICAL_BENCHMARK_PROTOCOL.md`, sha256 3b72ef01acce3927ace5e2a8e8bd8110539b8ea603c7743b7ca41c539cb9782b |
| Producer | 6ffe8fa; `x5g1_techbench.py` sha256 04f533765f2e9bf5abcc4c4ebb4df77b9fe4fb1f61c950c5a2f9774ee3d0e0f6 |
| Outputs: timings.json | d648d914…a24d |
| Outputs: projection.json | 98719354…731c |
| Outputs: MANIFEST.json | 68241589…f4b7 |

**Deviations.**

1. **P5 was not batched.** `score()` called `model(xf)` on all 4,096 rows at once. The job-0008 task required batched study-like scoring, and the v1 report's description was therefore inaccurate.
2. **Non-SeedTree randomness.** P5's reference distribution came from `np.random.default_rng(0)` rather than `SeedTree`, contrary to the repository convention.
3. **Hard-coded configuration.** The architecture was a literal (`STORED_MODEL`). The protocol promised a runtime metadata assertion, and none was made.
4. **No peak RAM recorded.** v1 recorded no peak RAM, so the v1 memory use is **unknown**. No value is reconstructed for it.

**Read-only metadata verification (this job).** `ArtifactStore.meta("c3358e3cb9c352fb")` in `topo-pilot/artifacts` (payload sha256 bcd024ef…f8596b) has:

* the `model_config` {vocab_in 37, vocab_out 36, n_ctx 33, 4 layers, d_model 128, 4 heads, d_mlp 512, GELU, dropout 0, untied}, equal to v1's literal;
* the stored `train_config` (5000 steps, batch 128, lr 1e-3, warmup 200, cosine, wd 0.1, clip 1.0, device "auto").

So v1's update, dev-CE and checkpoint timings refer to the correct architecture. Only P5 is corrected below.

## 2. Correction run (x5g1-techbench-scoring-v2)

| Item | Value |
|---|---|
| Protocol | [`X5_G1_SCORING_CORRECTION_PROTOCOL.md`](X5_G1_SCORING_CORRECTION_PROTOCOL.md), sha256 9f5e8300e983a2f784ae59dde23e27689c4c134cd6ef98db92a772747939231a, frozen in producer **a5b3a05** before timing (clean tree, one run, no retry) |
| Outputs | [`X5_G1_SCORING_CORRECTION_OUTPUTS/`](X5_G1_SCORING_CORRECTION_OUTPUTS/): timings.json 234a01df…907a, projection.json a3ac3423…bba1, MANIFEST.json 651da18f…5e46 |
| Fixture | 1 thread (interop 6, BLAS environment unset); SeedTree(871901), scope "x5g1-techbench-scoring-v2"; uniform public tokens [4096, 33]; Dirichlet q [4096, 36] (strictly positive, asserted); model built from the asserted metadata dict |
| Scored function | the study function `x5g1t_score.regret_rows`: 8 batches of 512, float64 `log_softmax` at p32, KL with 0·log 0 = 0 |

| Phase (CPU s, 1 thread) | Value |
|---|---|
| S0 setup (metadata read, fixture build) | 0.047 |
| S1 batched p32 scoring of 4,096 rows, 3 repeats | 3.891, 3.875, 3.844 (median **3.875**); wall ≈ 3.88–3.91 s; output [4096], finite |
| S2 checkpoint deserialisation (`load_model`, 3,243,204 bytes), 3 repeats | 0.031 each |
| Peak working set (process, including torch) | 276.6 MB after setup; **456.4 MB** after scoring |

Batched scoring (3.875 s) is slightly cheaper than v1's unbatched P5 (4.08 s). The v1 scoring term was therefore not an underestimate.

## 3. Corrected projection (CPU s, 1 thread)

| Term | v1 | corrected |
|---|---|---|
| train | 11,484.4 | 11,484.4 (kept) |
| init | 23.2 | 23.2 (kept) |
| dev CE | 635.3 | 635.3 (kept) |
| scoring = 6·27·(S1 + S2) + 60 | 720.7 | **692.8** |
| fresh test = 6·(S1 + S2) + 60 | 84.5 | **83.4** |
| setup = 6·S0 (new, separately accounted) | — | 0.3 |
| checkpoint I/O, generation, bootstrap, exports | 480.8 | 480.8 (kept) |
| **Total** | 13,428.8 | **13,400.25** |
| Limit (0.8 × 21,582.984) | 17,266.3872 | 17,266.3872 |
| Fits | yes | **yes** (62.1% of the remaining budget) |

**Limitations.**

* S1 has 3 repeats with a spread under 2%.
* The process-level peak working set includes the torch runtime.
* Checkpoint store reads and hashing remain covered by the v1 allowance (2× serialisation), not measured.
* The allocations are unchanged, and the projection is not a guarantee.

## 4. Cost

| Ledger | Value |
|---|---|
| Technical ledger (`x5g1-techbench-store/tech_ledger.json`) | entry `0009-scoring-v2`, **11.766 CPU s**, status ok, outcome FITS; technical cumulative **152.188 s** of 300 |
| Scientific X5 ledger | **17.016 s, unchanged** |

No tokens, q, weights, logits or regret values were persisted.
