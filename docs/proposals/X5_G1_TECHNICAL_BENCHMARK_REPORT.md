# X5 G1 technical throughput benchmark — report

14 October 2026, handoff job 0008.

| Item | Value |
|---|---|
| Protocol | [x5g1-techbench-v1](X5_G1_TECHNICAL_BENCHMARK_PROTOCOL.md), frozen before timing |
| Producer | 6ffe8fa (clean tree) |
| Outputs | [X5_G1_TECHNICAL_BENCHMARK_OUTPUTS/](X5_G1_TECHNICAL_BENCHMARK_OUTPUTS/): timings.json, projection.json, MANIFEST.json |

**A technical fixture, not a scientific pilot.** The inputs were uniformly random public tokens, with no world, oracle, study data or study checkpoint. Only times and sizes were persisted.

## Result: B1 RESOLVED — 1 intra-op thread fits; 6 threads do not

**Run conditions.** Process CPU (`time.process_time`) includes all torch threads, and no CPU time was multiplied by a thread count. torch 2.14.1+cpu, 12 logical CPUs, interop threads 6. The BLAS environment variables were unset.

| Measurement | 1 thread | 6 threads |
|---|---|---|
| CPU per optimizer update (batch 128) | **0.383 s** | 1.148 s |
| Wall time per update | 0.389 s | 0.192 s |
| P1: init + materialisation of 131,072 rows + 3 warm-up updates (CPU) | 3.9 s | 6.3 s |
| P4: dev CE on 4,096 × 33, median of 3 (CPU) | 3.92 s | 11.19 s |
| P5: p32 scoring on 4,096, median of 3 (CPU) | 4.08 s | 12.63 s |
| Checkpoint size, intermediate / final | 3,243,204 / 9,741,911 bytes | same |
| P6: serialisation CPU, intermediate / final | ≈ 0.00–0.016 / ≈ 0.016–0.047 s | ≈ 0.00–0.09 / ≈ 0.19–0.28 s |

**Projection of the scientific study, in CPU seconds** (protocol §4: measured terms plus conservative allocations):

| Term | 1 thread | 6 threads |
|---|---|---|
| train: 6 × 5,000 × update | 11,484.4 | 34,429.7 |
| init: 6 × P1 | 23.2 | 37.9 |
| devCE: 6 × 27 × P4 | 635.3 | 1,812.4 |
| scoring: 6 × 27 × P5 + oracle 60 | 720.7 | 2,105.2 |
| ckpt_io: 6 × (26·P6i + P6f) × 3 | 0.8 | 48.9 |
| generation (allocated) | 300 | 300 |
| bootstrap (allocated) | 120 | 120 |
| fresh test: 6 × P5 + 60 | 84.5 | 135.8 |
| exports (allocated) | 60 | 60 |
| **Total** | **13,428.8** | 39,049.9 |
| Limit: 0.8 × 21,582.984 | 17,266.4 | 17,266.4 |
| Fits | **yes** | no |
| Training wall time per model | ≈ 0.54 h | ≈ 0.27 h |

**Chosen setting.** Under the frozen rule, **torch intra-op threads = 1**. The projected total is about 62% of the remaining scientific budget, leaving about 38% in reserve. Six threads finish faster in wall time but cost about 3× the CPU, which confirms the B1 concern.

## Limitations

* **P2 single run.** The update cost comes from one 20-update window per setting; its variability is not measured. The repeated phases (P3–P5) varied by less than about 8%.
* **No transients.** The extrapolation assumes a stationary per-update cost; thermal, memory or OS effects are not captured.
* **Timer resolution.** `process_time` resolves to about 15.6 ms on Windows, so the small P3 and P6 values are quantised. Their contribution to the total is negligible.
* **Allocations are not measured.** Generation, oracle, bootstrap and exports are conservative allocations. Generation of 6 × 131,072 histories was not timed, because study-like sampling is excluded here.
* **Fixture schedule.** steps = 23 with warmup 200 changes the LR schedule, not the arithmetic cost. No learning inference was made, and no loss or CE was persisted.
* **Not a guarantee.** The later study must still run under cumulative hard guards, and the CPU of an abruptly killed process would remain unknown.

## Cost

* **Technical ledger** (`topo-pilot/x5g1-techbench-store/tech_ledger.json`): **140.4 CPU s** of the 300 s cap. Status ok, outcome RESOLVED.
* **Scientific ledger:** **17.016 s**, unchanged. No entry was added for fixture timing.
* **Storage:** timing JSON only, a few KB.
* **Disposal:** fixture models, tokens and losses were discarded at process exit.
