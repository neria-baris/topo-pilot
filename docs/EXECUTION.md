# Execution: local and external

**Goal:** any stage can run on a machine other than the one holding the repository. Examples:

- the laptop has no GPU or not enough disk;
- a cloud drive is unavailable;
- a free notebook GPU is the only option.

No component may assume a specific cloud service, drive, or account.

## 1. Model

```
JobSpec (stage, config hash, input artifact ids, resources, env lock hash)
   │
Executor.submit(job) ──► JobHandle ──► Executor.status(handle) ──► Executor.fetch(handle) ──► imported artifacts
```

- **Stage code is executor-agnostic.** A stage reads inputs from an `ArtifactStore` and writes outputs to one. The executor only decides **where** that store lives during the run.
- **Identical results wherever the job runs.** Artifact ids are content-addressed, so a job run remotely produces the same ids as a local run. GPU nondeterminism is the one exception: it affects only floating-point payloads, so the id is unchanged and the payload checksum is re-recorded on import.

## 2. Backends

| Executor | When | How |
|---|---|---|
| `LocalExecutor` | default | runs the stage in a subprocess with the same Python environment |
| `BundleExecutor` | no local GPU, disk, or drive; Colab, Kaggle, a rented GPU | `export` creates `bundle_<job>.tar.gz` with the source tree, `requirements.lock`, the stage config, the input artifacts, and a `run_bundle.py` entry point. The user uploads it by any means, runs `python run_bundle.py` remotely, and downloads `outputs_<job>.tar.gz`. `import` then verifies checksums and parent ids and ingests the outputs |
| `SSHExecutor` (optional) | the user has a reachable machine | the same bundle, copied and run over `ssh` and `scp`. The host comes from untracked `configs/local.yaml`. Keys are never stored in the repository |

A notebook helper, `topo-pilot export-notebook --stage S4`, writes a minimal `.ipynb` with three cells:

1. upload or unpack the bundle;
2. install `requirements.lock`;
3. run `run_bundle.py`, then pack the outputs.

The helper makes no Drive mounts and no service calls. The user may add those manually.

## 3. Bundle format

```
bundle_<job_id>/
  job.json            # JobSpec + expected output artifact types
  src/                # exact source tree (git SHA recorded)
  requirements.lock
  configs/            # resolved stage config
  artifacts/          # input artifacts only (content-addressed layout)
  run_bundle.py       # entry: verifies inputs, runs stage, writes outputs/ + RunManifest, packs tar
```

- **Size limits:**
  - S4 inputs are the datasets of 7 runs (≈ 30–60 MB).
  - Outputs are the checkpoints and activations (≤ 2 GB). Split the job per run if necessary: one job per (world, condition, seed).
- **On import:**
  - verify every `payload_sha256`;
  - verify that the parent ids exist locally;
  - write the `RunManifest` with `executor = "bundle"` and the remote hardware info.

## 4. Splitting work

| Location | Stages |
|---|---|
| Remote (GPU) | training runs (S3–S5, S7) and activation extraction |
| Local (CPU) | S1, S2, and all PH and analysis |

The run plan from `experiment` emits one JobSpec per training run, in the priority order of `STAGES.md` §2. This allows a mixture: some runs local, some remote.

## 5. No local GPU: decision rule

The owner may have **no GPU**. The model is small (about 0.8M parameters, about 21M target tokens per run), so a GPU is a convenience, not a requirement.

**Rough estimate** (to be replaced by the S3 measurement):

| Hardware | Per run | To E2 (7 runs) | To E4 (17 runs) |
|---|---|---|---|
| Modern multi-core CPU, fp32 PyTorch | 15–45 min | 2–5 h | 4–13 h |
| Free notebook GPU | a few minutes | — | — |

**Rule**, applied at S3 and recorded at checkpoint H2:

1. S3 runs on whatever device is available (`device: auto` falls back to CPU). It measures tokens per second over 100 steps after warm-up.
2. Project the wall time of the next stage from the measured rate.
3. If the projection is **≤ 8 h** (one overnight run), use `LocalExecutor` on CPU. Set the torch thread count to the number of physical cores, and run one training at a time.
4. If the projection is **> 8 h**, use `BundleExecutor` with **one job per run**, in the priority order of `STAGES.md` §2, on any free GPU notebook (Colab, Kaggle) or a rented GPU. Meanwhile, keep doing CPU-only work locally: activation extraction can run locally after import, and all PH and analysis are CPU-only.
5. Mixed mode is allowed. The run planner may send some runs to bundles and keep others local, because artifact ids are the same either way.

GPU-only code paths are forbidden. Every stage must run on CPU (CONVENTIONS §1). Tests never require CUDA, except those marked `gpu`.

## 6. Storage without local disk

`ArtifactBackend` is an abstract base class. The core provides `LocalFSBackend`. A `MirrorBackend` may wrap any directory path that the operating system exposes, such as a mounted external disk or a synced folder. No other backend is required. Optional rclone-style backends are out of scope for the pilot.
