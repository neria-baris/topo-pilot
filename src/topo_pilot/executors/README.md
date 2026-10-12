# `executors`

## Purpose

Run a job somewhere: in a local subprocess, through a portable bundle on any machine (a free notebook GPU, a rented GPU), or over `ssh`. Nothing here depends on a cloud drive, an account, or a service. Stage code is executor-agnostic: it reads inputs from an `ArtifactStore` and writes outputs to one, and the executor only decides where that store lives during the run. Imports allowed: the standard library and `topo_pilot.contracts`. `topo_pilot.experiment` is imported lazily inside `entry` only, so no science module is ever imported.

## Logic

### Jobs and `entry`

A `JobSpec` names a stage, its resolved config, the input artifact ids and the output types it may produce. `job.json` holds the JobSpec plus `store_root`, `repo_root`, `stages_yaml`, `executor` and `git_sha`; relative paths resolve against the folder of `job.json`.

`entry(job_json)`:

1. opens `ArtifactStore(LocalFSBackend(store_root))`;
2. imports every module listed in `resolved_config["import_modules"]` (how extensions and test stubs register stages in a fresh process);
3. imports `topo_pilot.experiment` lazily, loads the config with `load_config`, and runs `STAGE_REGISTRY[stage_id]().execute(resolved_config, cfg, store)`;
4. always saves a `RunManifest` (executor name, hardware from `platform`, wall time, failures, DAG of the written ids; its parents are the written outputs);
5. writes `<job>.result.json` (`ok`, `outputs`, `manifest`) and returns 0, or 1 after recording a failure.

Any exception in the stage becomes a failure entry (`StageFailure` fields kept; others wrapped as `EXECUTOR_ERROR`). An unreadable `job.json` raises `EXECUTOR_ERROR`.

### Executors

- `LocalExecutor`: `Popen([python, -m, topo_pilot.executors.entry, job.json])` on the same store. `status` is `running`, then `done` or `failed`. `fetch` waits, checks the output types, and returns the ids. The store must use `LocalFSBackend`.
- `BundleExecutor`: `submit` writes `bundle_<job>.tar.gz` and the state is `awaiting_user` (`instructions(handle)` says what to upload, run and download). `fetch(handle, store, outputs_path=...)` first reads the member names of the tarball to reject any artifact type outside `expected_output_types` (`RunManifest` is always allowed; `EXECUTOR_ERROR`), then calls `store.import_bundle`, which verifies ids, checksums and parents (`CHECKSUM_MISMATCH`, `MISSING_PARENT`) before writing anything. A manifest that records a failure makes `fetch` raise `EXECUTOR_ERROR` (state `failed`); otherwise the state becomes `done`.
- `SSHExecutor`: the same bundle with the system `scp` and `ssh`. Settings come from the `local` mapping of the resolved config (`configs/local.yaml`, untracked): `ssh: {host, user, remote_dir, python, install}`. Credentials come from the user's SSH config or agent. `upload_cmd`, `run_cmd`, `status_cmd`, `download_cmd` build the command lines. The remote job writes `exit_code`.
- `NotebookExporter.export(bundle, dest)`: a minimal nbformat-4 notebook with exactly three code cells (unpack; install the lock; run and pack). No Drive mount, no service call.

### Bundle contents and secrets

```
bundle_<job>/
  job.json  run_bundle.py  pyproject.toml  requirements.lock
  src/  configs/            # source tree; git SHA recorded in job.json
  inputs.tar.gz             # store.export_bundle(input ids, with_parents=True)
```

The walk skips `__pycache__`, `*.egg-info`, `local.yaml`, `.env`, `.env.*`, and any file matching `*key*` or `*token*` (case-insensitive). Passing such a file in `extra_files` raises `EXECUTOR_ERROR`.

### `run_bundle.py`

Standard library only until the environment exists. It (1) optionally installs `requirements.lock` (`--no-install` skips; local version suffixes such as `+cpu` are stripped from pins, `torch` is skipped if already importable, decision D-010; on a bulk failure it retries one package at a time and warns), (2) imports `inputs.tar.gz` into a fresh store under `work/store`, which verifies every checksum, (3) runs `entry` with `src/` first on `PYTHONPATH`, and (4) packs `outputs_<job>.tar.gz` with `export_bundle(outputs + RunManifest, with_parents=False)`. The exit code is the job's. `--install-only` stops after step 1.

### Why results match across machines

Artifact ids are content-addressed from config and parents, so a job run remotely yields the same ids as a local run. The RunManifest id includes the job id, the executor and the start time, so repeated runs never collide.

## Data

Reads input artifacts (any type) and writes whatever the stage writes, plus one `RunManifest` per run. It creates no artifact type of its own. Files: `job.json`, `<job>.result.json`, `bundle_<job>.tar.gz`, `outputs_<job>.tar.gz`, `notebook_<job>.ipynb`.

## Public API

`JobSpec`, `JobHandle`, `Executor`, `LocalExecutor`, `BundleExecutor`, `SSHExecutor`, `EXECUTOR_REGISTRY`, `entry`, `NotebookExporter`. Errors: `EXECUTOR_ERROR`, `CHECKSUM_MISMATCH`, `MISSING_PARENT`.

### Run on Colab or Kaggle (no Drive)

On the machine with the repository:

1. Submit the job with `BundleExecutor(out_dir=Path("bundles")).submit(job, store)`. This writes `bundles/bundle_<job>.tar.gz`, and `status` returns `awaiting_user`. Optionally write a notebook: `NotebookExporter().export(Path("bundles/bundle_<job>.tar.gz"), Path("bundles"))`.
2. Upload `bundle_<job>.tar.gz` by any means: the Colab Files panel (drag and drop), the Kaggle "Add data / upload" dialog, `scp`, or a browser download link. A Drive is not needed.

On the notebook machine (turn on a GPU runtime if wanted):

3. Either open the exported notebook and run its three cells, or in a terminal cell run:

   ```
   tar xzf bundle_<job>.tar.gz
   cd bundle_<job>
   python run_bundle.py            # installs the lock first; add --no-install if the environment is ready
   ```

   Kaggle: an uploaded dataset is under `/kaggle/input/...`; extract from there.
4. `run_bundle.py` verifies the input checksums, runs the stage, and writes `outputs_<job>.tar.gz` in the bundle folder. It also records the remote hardware in the RunManifest.
5. Download `outputs_<job>.tar.gz` (Colab file browser, Kaggle "Output" tab, or `scp`).

Back on the repository machine:

6. `BundleExecutor.fetch(handle, store, outputs_path=Path("outputs_<job>.tar.gz"))` verifies and imports the artifacts and the RunManifest and returns the ids; `status` becomes `done`. A tampered file raises `CHECKSUM_MISMATCH`, a missing parent `MISSING_PARENT`, and an unexpected output type `EXECUTOR_ERROR`, with nothing written.

## How to test

```powershell
.\.venv\Scripts\python.exe -m pytest tests/executors -q     # about 15 s; no network
.\.venv\Scripts\python.exe tools/check_imports.py
.\.venv\Scripts\python.exe tools/check_file_sizes.py
```
