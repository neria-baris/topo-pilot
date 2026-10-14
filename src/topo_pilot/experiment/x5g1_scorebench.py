"""X5 G1 scoring-only timing correction (x5g1-techbench-scoring-v2; job 0009). NOT scientific.

Uniform random public tokens and a Dirichlet q from ``SeedTree`` only; no training update, study
checkpoint, oracle or pool. Persists timings, sizes, shapes and flags only.
``python -m topo_pilot.experiment.x5g1_scorebench --repo . --main-store <artifacts>
--store <tech store> --out <dir> --mailbox <dir>``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import torch

from topo_pilot.contracts import (
    ArtifactStore,
    Checkpoint,
    LocalFSBackend,
    ObservationSet,
    SeedTree,
    SequenceLayout,
)
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.learner import ModelConfig, TransformerLM, load_model, serialise_state

from .x4b_run import peak_memory_bytes
from .x5g1_controls import RunControls
from .x5g1_safety import ensure_new_output_dir, guarded_export
from .x5g1t_score import SCORE_BATCH, regret_rows

log = logging.getLogger(__name__)
PROTOCOL = "x5g1-techbench-scoring-v2"
PROTOCOL_DOC = "docs/proposals/X5_G1_SCORING_CORRECTION_PROTOCOL.md"
V1_PROJECTION = "docs/proposals/X5_G1_TECHNICAL_BENCHMARK_OUTPUTS/projection.json"
MASTER, N_ROWS, REPEATS = 871901, 4096, 3
STORED_CKPT = "c3358e3cb9c352fb"
FIXED_MODEL = {"activation": "gelu", "d_mlp": 512, "d_model": 128, "dropout": 0.0, "n_ctx": 33,
               "n_heads": 4, "n_layers": 4, "tie_embeddings": False, "vocab_in": 37,
               "vocab_out": 36}
STORED_TRAIN = {"batch_size": 128, "checkpoint_steps": [0, 50, 100, 200, 400, 700, 1000, 1500,
                                                        2000, 3000, 4000, 5000],
                "device": "auto", "grad_clip": 1.0, "lr": 0.001, "schedule": "cosine",
                "steps": 5000, "warmup": 200, "weight_decay": 0.1}
TECH_CAP_S = 300.0
LIMIT_S = 0.8 * 21582.984


def _clock() -> tuple[float, float]:
    return time.process_time(), time.perf_counter()


def _delta(a: tuple[float, float], b: tuple[float, float]) -> dict:
    return {"cpu_s": b[0] - a[0], "wall_s": b[1] - a[1], "peak_rss_bytes": peak_memory_bytes()}


def stored_model_config(main_root: Path) -> tuple[dict, str]:
    """Read-only metadata assertion of the stored E3 checkpoint; returns (model_config, sha)."""
    meta = ArtifactStore(LocalFSBackend(main_root)).meta(STORED_CKPT)
    mc, tc = dict(meta.config["model_config"]), dict(meta.config["train_config"])
    if mc != FIXED_MODEL or tc != STORED_TRAIN:
        raise AssertionError(f"stored config differs: model {mc} train {tc}")
    return mc, str(meta.payload_sha256)


def fixture(model_cfg: dict) -> tuple[TransformerLM, torch.Tensor, np.ndarray]:
    seeds = SeedTree(MASTER)
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(seeds.seed(PROTOCOL, "init"))
        model = TransformerLM(ModelConfig(**model_cfg))
    tokens = seeds.generator(PROTOCOL, "tokens").integers(0, 36, size=(N_ROWS, 33))
    obs = ObservationSet(split="dev", V=36, sequence_id=np.arange(N_ROWS, dtype=np.int64),
                         tokens=tokens.astype(np.uint8))
    ds = PublicTokenDataset(obs, SequenceLayout())
    inputs = torch.stack([ds[i][0] for i in range(len(ds))])
    q = seeds.generator(PROTOCOL, "q").dirichlet(np.ones(36), size=N_ROWS)
    if inputs.shape != (N_ROWS, 33) or q.min() <= 0 or np.max(np.abs(q.sum(1) - 1)) > 1e-12:
        raise AssertionError("fixture shape or q positivity check failed")
    return model, inputs, q


def project(v1: dict, s1: float, s2: float, s0: float) -> dict:
    """Frozen corrected projection (protocol §4); v1 terms other than scoring kept."""
    keep = ("train", "init", "devCE", "ckpt_io", "generation", "bootstrap", "exports")
    p = {k: v1[k] for k in keep}
    p["scoring"] = 6 * 27 * (s1 + s2) + 60.0
    p["fresh_test"] = 6 * (s1 + s2) + 60.0
    p["setup"] = 6 * s0
    p["total"] = sum(p.values())
    p["limit_80pct"] = LIMIT_S
    p["fits"] = p["total"] <= LIMIT_S
    return p


def _sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(repo: Path, main_root: Path, store: Path, out: Path, mailbox: Path) -> dict:
    ensure_new_output_dir(out)
    ctl = RunControls(store / "tech_ledger.json", TECH_CAP_S, mailbox / "STOP",
                      "0009-scoring-v2", TECH_CAP_S)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()
    res: dict = {"protocol": PROTOCOL, "kind": "technical fixture timing only; not scientific",
                 "producer_head": head, "protocol_doc_sha256": _sha(repo / PROTOCOL_DOC),
                 "prior_tech_cumulative_s": ctl.prior}
    with ctl:
        torch.set_num_threads(1)
        ctl.guard("S0")
        a = _clock()
        model_cfg, ckpt_sha = stored_model_config(main_root)
        model, inputs, q = fixture(model_cfg)
        res["S0_setup"] = _delta(a, _clock())
        res["stored_checkpoint"] = {"id": STORED_CKPT, "payload_sha256": ckpt_sha,
                                    "model_config": model_cfg, "asserted": True}
        res["shapes"] = {"inputs": list(inputs.shape), "q": list(q.shape)}
        ctl.guard("S0 done")
        res["S1_scoring"] = []
        for r in range(REPEATS):
            ctl.guard(f"S1 {r}")
            a = _clock()
            out_rows = regret_rows(model, inputs, q, SCORE_BATCH)
            row = _delta(a, _clock())
            row.update({"batches": -(-N_ROWS // SCORE_BATCH), "out_shape": list(out_rows.shape),
                        "finite": bool(np.all(np.isfinite(out_rows)))})
            res["S1_scoring"].append(row)
            del out_rows
            ctl.guard(f"S1 {r} done")
        state = serialise_state(model, {})
        res["state_bytes"] = len(state)
        res["S2_load"] = []
        for r in range(REPEATS):
            ctl.guard(f"S2 {r}")
            a = _clock()
            load_model(Checkpoint(run_id="techbench", step=0, observation_id="fixture",
                                  state=state, model_config=model_cfg))
            res["S2_load"].append(_delta(a, _clock()))
            ctl.guard(f"S2 {r} done")
        med = lambda rows: statistics.median(x["cpu_s"] for x in rows)  # noqa: E731
        v1 = json.loads((repo / V1_PROJECTION).read_text(encoding="utf-8"))["settings"]["1"]
        res["projection_v1_1thread"] = v1
        res["projection_corrected"] = project(v1, med(res["S1_scoring"]), med(res["S2_load"]),
                                              res["S0_setup"]["cpu_s"])
        res["env"] = {"python": sys.executable, "torch": torch.__version__,
                      "numpy": np.__version__, "threads": torch.get_num_threads(),
                      "interop_threads": torch.get_num_interop_threads(),
                      "logical_cpus": os.cpu_count(),
                      "blas_env": {k: os.environ.get(k) for k in (
                          "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS")},
                      "topo_pilot_file": __import__("topo_pilot").__file__}
        ctl.outcome = "FITS" if res["projection_corrected"]["fits"] else "DOES_NOT_FIT"
        res["outcome"] = ctl.outcome
        res["tech_cpu_s_before_export"] = round(ctl.cpu(), 3)

        def write(name: str, obj) -> None:
            (out / name).write_text(json.dumps(obj, indent=1, default=str), encoding="utf-8")

        def manifest() -> None:
            sums = {f.name: _sha(f) for f in sorted(out.iterdir()) if f.name != "MANIFEST.json"}
            (out / "MANIFEST.json").write_text(json.dumps(sums, indent=1), encoding="utf-8")

        guarded_export(ctl, [("timings", lambda: write("timings.json", res)),
                             ("projection", lambda: write("projection.json", {
                                 "v1_1thread": v1, "corrected": res["projection_corrected"],
                                 "outcome": res["outcome"]})),
                             ("manifest", manifest)], out / "EXPORT_STATUS.json")
    return res


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="X5 G1 scoring-only timing correction")
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--main-store", type=Path, required=True)
    ap.add_argument("--store", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mailbox", type=Path, required=True)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    res = run(args.repo, args.main_store, args.store, args.out, args.mailbox)
    log.info("scoring-v2: %s total %.1f", res["outcome"], res["projection_corrected"]["total"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
