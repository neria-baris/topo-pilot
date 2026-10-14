# X5 G1 scoring-only timing correction — frozen protocol (x5g1-techbench-scoring-v2)

14 October 2026. Handoff job 0009. Branch `x5-g1-implementation`.

**Status.** Frozen before any timing. The producer commit has a clean tree before the single run.

**What this is.**

* A technical fixture, not a scientific pilot.
* It covers scoring only: no training update, no study checkpoint, no oracle, no pool and no study data.

**What it is not.** It does not repeat the v1 training benchmark. The v1 protocol, report and outputs stay byte-identical. Its deviations are disclosed additively in [X5_G1_SCORING_CORRECTION_REPORT.md](X5_G1_SCORING_CORRECTION_REPORT.md).

## 1. Purpose

v1 P5 timed `model(xf)` as **one** 4,096-row forward pass. That contradicts the batched scoring the study will use. P5 also drew its reference distribution from `np.random.default_rng(0)` rather than `SeedTree`, and v1 saved no peak RAM.

This correction times the study scoring function itself, `x5g1t_score.regret_rows`:

* p32 log-probabilities computed in batches of 512 rows (equal to the learner's dev-CE batch);
* a numerically stable float64 `log_softmax`;
* the KL against a strictly positive q.

The study projection is then recomputed with the corrected scoring term.

## 2. Fixed configuration

**Metadata assertion (read only).** At run start the producer reads `ArtifactStore.meta("c3358e3cb9c352fb")` from the main store `topo-pilot/artifacts`. Only metadata is read, never weights, and nothing is written.

* It **asserts** that `model_config` equals the fixed architecture: vocab_in 37, vocab_out 36, n_ctx 33, 4 layers, d_model 128, 4 heads, d_mlp 512, GELU, dropout 0, untied.
* It asserts that `train_config` equals the stored E3 dict.
* It records the artifact's payload_sha256. The fixture model is built **from that metadata dict**, not from a hard-coded literal.

**Threads.** `torch.set_num_threads(1)` only. Interop threads and the BLAS environment variables are recorded, not changed.

**Randomness.** `SeedTree(871901)` only, scope `"x5g1-techbench-scoring-v2"`:

| Item | Source |
|---|---|
| fixture weights | `torch.manual_seed(seed("x5g1-techbench-scoring-v2", "init"))` inside `torch.random.fork_rng` |
| tokens | `generator("x5g1-techbench-scoring-v2", "tokens")`: uniform integers 0..35, shape [4096, 33] |
| q | `generator("x5g1-techbench-scoring-v2", "q")`: Dirichlet(1₃₆) rows [4096, 36], asserted strictly positive with row sums within 1e-12 |

**Inputs.** Tokens become an in-memory public `ObservationSet` (split dev). Inputs come through `PublicTokenDataset` (`[BOS, w1..w32]`), never saved. Their shape [4096, 33] is asserted at runtime.

## 3. Phases (one process, one run, no automatic retry)

| Phase | Method |
|---|---|
| S0 setup | metadata read, fixture init and data build: CPU, wall and peak RAM |
| S1 scoring | `regret_rows(model, inputs, q, batch=512)`, 3 repeats. Per repeat: CPU, wall, peak working set after, number of batches (must be 8), output shape (must be [4096]), all finite. |
| S2 checkpoint load overhead | `learner.load_model(Checkpoint(..., state=serialise_state(model, {})))` from in-memory bytes, 3 repeats. Measures the per-checkpoint deserialisation the study adds before scoring. |

**Persisted:** times, sizes, shapes, booleans, configuration and versions.

**Never persisted:** tokens, q, weights, logits, CE or KL values.

## 4. Corrected projection (CPU s, 1 thread)

The v1 1-thread terms are kept **unchanged** except the two scoring terms:

```text
scoring    = 6 × 27 × (median S1 + median S2) + 60        (oracle allowance, unchanged)
fresh_test = 6 × (median S1 + median S2) + 60
setup      = 6 × S0                                         (new, separately accounted overhead)
total      = v1 train + init + devCE + ckpt_io + generation + bootstrap + exports
             + scoring + fresh_test + setup
```

* **Fit rule (frozen, unchanged):** total ≤ 0.8 × 21,582.984 = **17,266.3872** CPU s.
* The v1 projection is preserved and shown side by side.
* **If the corrected total does not fit:** report that honestly as the remaining blocker. No study implementation is executed, and no budget is raised.

## 5. Controls

* **Ledger.** The existing validated atomic technical ledger, `x5g1-techbench-store/tech_ledger.json`, via `RunControls`, with job tag `0009-scoring-v2`.
* **Cumulative technical cap: 300 CPU s**, including the original 140.422 s. The per-run cap is 300 s; the cumulative check enforces the total.
* **Guards.** STOP and budget checks run before and after every phase and repeat.
* **Outputs.** A new immutable directory, `docs/proposals/X5_G1_SCORING_CORRECTION_OUTPUTS/`, holding `timings.json`, `projection.json` and `MANIFEST.json`. They are written through `guarded_export`.
* **Ledgers.** No scientific ledger entry is made; the X5 scientific cumulative stays 17.016 s.
