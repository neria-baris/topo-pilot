# X5 G1 technical throughput benchmark — frozen protocol (x5g1-techbench-v1)

14 October 2026. Handoff job 0008. Branch `x5-g1-bench`.

**Frozen before any timing.** The producer commit is clean before the run.

**This is a technical fixture, not a scientific pilot.** It uses uniformly random public tokens only:

* no world, emissions, oracle, history or study data;
* no study checkpoint;
* nothing about learning is inspected, persisted or used.

Only timing tables and sizes are persisted.

## 1. Purpose

Resolve blocker B1 from the training draft: does the proposed six-model study fit the remaining X5 scientific budget of **21,582.984 CPU s** with at least a 20% reserve? CPU here means **process CPU time**, which includes all torch threads.

## 2. Fixed configuration

* **Model.** The stored E3 `ModelConfig`, read from checkpoint metadata c3358e3cb9c352fb and asserted:
  - vocab_in 37 and vocab_out 36;
  - n_ctx 33;
  - 4 layers, d_model 128, 4 heads, d_mlp 512;
  - GELU, dropout 0, untied embeddings.
* **Optimizer.** The stored `TrainConfig` semantics: AdamW, lr 1e-3, warmup 200, cosine, weight decay 0.1, clip 1.0, batch 128, device "auto" (CPU with this CPU-only torch).
* **Fixture schedule.** steps = 23 (3 warm-up updates + 20 measured) and `checkpoint_steps` = (3, 23).
  - The LR schedule therefore differs from the 5,000-step schedule, because warmup 200 exceeds 23 steps. That has no effect on per-update arithmetic cost and is irrelevant to timing; no learning inference is made.
* **Seed.** `SeedTree(871901)` with scope "x5g1-techbench-v1": `generator("x5g1-techbench-v1", "tokens", split)` for the tokens, and run_key ("x5g1-techbench-v1",).
* **Tokens.** Uniform over 0..35, shape [n, 33], as public `ObservationSet`s built in memory and never saved:
  - train: n = 131,072 (representative of the real size, so materialisation cost is realistic);
  - dev inside `fit`: 128 rows;
  - full dev: 4,096 rows.
* **Thread settings.** `torch.set_num_threads(1)` and then `torch.set_num_threads(6)`, **in that fixed order**, in one process.
  - interop threads and the BLAS environment variables are recorded, not changed: OPENBLAS/MKL/OMP_NUM_THREADS stay unset;
  - the 12 logical processors are recorded.

## 3. Phases measured per thread setting

Each phase records process CPU (`time.process_time`) and wall time (`time.perf_counter`) separately. A measured CPU time is never multiplied by the thread count.

| Phase | Method |
|---|---|
| P1 init + materialise + first checkpoint | from the start of `Trainer(...).fit(train, dev128, cb)` to the end of the step-3 callback. Includes init, materialising 131,072 rows, 3 warm-up updates and the step-3 dev CE on 128 rows. |
| P2 measured updates | from the end of the step-3 callback to the start of the step-23 callback, i.e. 20 updates plus one dev CE on 128 rows |
| P3 dev CE on 128 rows | `Trainer.dev_ce` on the 128-row dev set, 3 repeats, timed separately. The update cost is (P2 − median P3)/20. |
| P4 full dev CE (4,096 × 33) | `Trainer.dev_ce` on 4,096 rows, 3 repeats |
| P5 endpoint scoring | the batched p32 forward on 4,096 rows (model in eval mode, `torch.no_grad`), then softmax and a KL against a fixed random distribution in float64. 3 repeats. |
| P6 checkpoint serialisation | `torch.save` into BytesIO of {"model": state_dict} (intermediate) and of {"model", "optimizer", "scheduler"} (final) of the in-memory fixture model. 3 repeats each; sizes recorded. |

* The fixture weights and tokens are discarded at process end.
* Losses, CE values and logits are **not** persisted, only times and sizes.

## 4. Projection of the scientific study cost

Per thread setting, in CPU seconds:

```text
train     = 6 × 5000 × u                    (u = measured CPU per update, from P2/P3)
init      = 6 × P1                          (measured; includes materialisation)
devCE     = 6 × 27 × P4                     (the trainer's dev CE at every grid checkpoint)
scoring   = 6 × 27 × P5 + oracle allowance
ckpt_io   = 6 × (26 × P6_intermediate + P6_final) + store-write allowance
```

**Conservative allocations (not measured):**

| Item | Allocation |
|---|---|
| generation of 6 × 131,072 train + 6 × 4,096 dev + 2 × 4,096 test histories | 300 s |
| oracle beliefs for the dev and test pools | 60 s |
| paired bootstraps of 3 pairs × 2,000 draws over the 27-point curves | 120 s |
| fresh-test evaluation of 6 models | 6 × P5 + 60 s |
| exports and manifests | 60 s |
| store-write allowance for checkpoints | 2 × the measured serialisation total |

* **Total** = the sum of the above.
* **Fit rule (frozen).** A setting **fits** iff Total ≤ 0.8 × 21,582.984 = **17,266.387 CPU s**.
* **Choice.** Among fitting settings, choose the one with the lower Total; ties go to 1 thread.
* **If neither fits:** B1 stays unresolved. Stop and report for a coordinator/owner decision. The budget and scope are not changed.

**Limitations to report.**

* Extrapolating from 20 updates assumes a stationary per-update cost, with no thermal, memory or OS noise.
* The variability is shown by the 3 repeats of P3–P6 only, since P2 runs once per setting.
* The projection is not a guarantee; the later study still needs cumulative hard guards.

## 5. Controls and outputs

* **Technical cap.** 300 CPU s and 8 GB, enforced by `RunControls` with a **separate technical ledger** in the independent store `topo-pilot/x5g1-techbench-store/tech_ledger.json`.
* **STOP and cap checks.** Before and after every phase. On a trigger, a small technical audit record is written and the run aborts. No automatic repeat.
* **No scientific ledger entry.** The X5 scientific cumulative stays 17.016 s.
* **Outputs.** The immutable `docs/proposals/X5_G1_TECHNICAL_BENCHMARK_OUTPUTS/` holds `timings.json` (all phases, both settings, versions, threads, sizes), `projection.json` and `MANIFEST.json`. The report is X5_G1_TECHNICAL_BENCHMARK_REPORT.md.
