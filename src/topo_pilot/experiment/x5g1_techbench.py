"""X5 G1 technical throughput benchmark (x5g1-techbench-v1; job 0008). NOT a scientific pilot.

Uniform random public tokens only; no world, oracle, study data or study checkpoint. Persists
timings and sizes only. ``python -m topo_pilot.experiment.x5g1_techbench --repo . --store <dir>
--out <dir> --mailbox <dir>``.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import io
import json
import logging
import os
import statistics
import sys
import time
from pathlib import Path

import numpy as np
import torch

from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.learner import ModelConfig, TrainConfig, Trainer

from .x5g1_controls import RunControls
from .x5g1_safety import ensure_new_output_dir, guarded_export

log = logging.getLogger(__name__)
MASTER, SCOPE = 871901, "x5g1-techbench-v1"
THREADS = (1, 6)
N_TRAIN, N_DEV_FIT, N_DEV_FULL = 131_072, 128, 4096
WARMUP_UPDATES, MEASURED_UPDATES, REPEATS = 3, 20, 3
TECH_CAP_S = 300.0
REMAINING_SCIENTIFIC_S = 21582.984
STORED_MODEL = {"activation": "gelu", "d_mlp": 512, "d_model": 128, "dropout": 0.0, "n_ctx": 33,
                "n_heads": 4, "n_layers": 4, "tie_embeddings": False, "vocab_in": 37,
                "vocab_out": 36}
ALLOC = {"generation_s": 300.0, "oracle_s": 60.0, "bootstrap_s": 120.0,
         "fresh_test_extra_s": 60.0, "exports_s": 60.0, "store_write_factor": 2.0}


def _clock() -> tuple[float, float]:
    return time.process_time(), time.perf_counter()


def _delta(a: tuple[float, float], b: tuple[float, float]) -> dict:
    return {"cpu_s": b[0] - a[0], "wall_s": b[1] - a[1]}


def _dataset(split: str, n: int) -> PublicTokenDataset:
    rng = SeedTree(MASTER).generator(SCOPE, "tokens", split)
    tokens = rng.integers(0, 36, size=(n, 33)).astype(np.uint8)
    obs = ObservationSet(split="train" if split == "train" else "dev", V=36,
                         sequence_id=np.arange(n, dtype=np.int64), tokens=tokens)
    return PublicTokenDataset(obs, SequenceLayout())


def _tensors(ds: PublicTokenDataset) -> tuple[torch.Tensor, torch.Tensor]:
    items = [ds[i] for i in range(len(ds))]
    return torch.stack([a for a, _ in items]), torch.stack([b for _, b in items])


def _repeat(fn, n: int = REPEATS) -> list[dict]:
    out = []
    for _ in range(n):
        a = _clock()
        fn()
        out.append(_delta(a, _clock()))
    return out


def bench_setting(threads: int, ctl: RunControls, data: dict) -> dict:
    """All phases for one intra-op thread setting (see the frozen protocol §3)."""
    torch.set_num_threads(threads)
    model_cfg = ModelConfig(**STORED_MODEL)
    train_cfg = TrainConfig(steps=WARMUP_UPDATES + MEASURED_UPDATES,
                            checkpoint_steps=(WARMUP_UPDATES, WARMUP_UPDATES + MEASURED_UPDATES))
    trainer = Trainer(model_cfg, train_cfg, SeedTree(MASTER), (SCOPE,))
    marks, hold = {}, {}

    def on_checkpoint(step: int, model, info: dict) -> None:
        marks[(step, "enter")] = _clock()
        hold["model"], hold["info"] = model, info
        marks[(step, "exit")] = _clock()

    ctl.guard(f"threads {threads} fit")
    t0 = _clock()
    trainer.fit(data["train"], data["dev_fit"], on_checkpoint)
    ctl.guard(f"threads {threads} fit done")
    first, last = WARMUP_UPDATES, WARMUP_UPDATES + MEASURED_UPDATES
    res = {"threads": threads, "interop_threads": torch.get_num_interop_threads(),
           "P1_init_materialise_warmup": _delta(t0, marks[(first, "exit")]),
           "P2_updates_plus_devce128": _delta(marks[(first, "exit")], marks[(last, "enter")])}
    model, info = hold["model"], hold["info"]
    x128, y128 = data["dev_fit_tensors"]
    xf, yf = data["dev_full_tensors"]
    res["P3_devce128"] = _repeat(lambda: trainer.dev_ce(model, x128, y128))
    ctl.guard(f"threads {threads} P3")
    res["P4_devce4096"] = _repeat(lambda: trainer.dev_ce(model, xf, yf))
    ctl.guard(f"threads {threads} P4")
    q = np.random.default_rng(0).dirichlet(np.ones(36), size=xf.shape[0])

    def score() -> None:
        model.eval()
        with torch.no_grad():
            logits = model(xf).logits[:, 32, :].double().numpy()
        z = logits - logits.max(axis=1, keepdims=True)
        p = np.exp(z) / np.exp(z).sum(axis=1, keepdims=True)
        float(np.sum(q * (np.log(q) - np.log(p))) / q.shape[0])
        model.train()

    res["P5_scoring4096"] = _repeat(score)
    ctl.guard(f"threads {threads} P5")
    sizes = {}

    def save(final: bool) -> None:
        payload = {"model": {k: v.detach().cpu() for k, v in model.state_dict().items()}}
        if final:
            payload["optimizer"] = info["optimizer_state"]
            payload["scheduler"] = info["scheduler_state"]
        buf = io.BytesIO()
        torch.save(payload, buf)
        sizes["final" if final else "intermediate"] = buf.getbuffer().nbytes

    res["P6_save_intermediate"] = _repeat(lambda: save(False))
    res["P6_save_final"] = _repeat(lambda: save(True))
    res["checkpoint_bytes"] = sizes
    ctl.guard(f"threads {threads} P6")
    med = lambda rows, k="cpu_s": statistics.median(r[k] for r in rows)  # noqa: E731
    res["update_cpu_s"] = (res["P2_updates_plus_devce128"]["cpu_s"] - med(res["P3_devce128"])) \
        / MEASURED_UPDATES
    res["update_wall_s"] = (res["P2_updates_plus_devce128"]["wall_s"]
                            - med(res["P3_devce128"], "wall_s")) / MEASURED_UPDATES
    res["projection"] = project(res, med)
    return res


def project(r: dict, med) -> dict:
    """Frozen projection (protocol §4), CPU seconds."""
    ser = 26 * med(r["P6_save_intermediate"]) + med(r["P6_save_final"])
    p = {"train": 6 * 5000 * r["update_cpu_s"],
         "init": 6 * r["P1_init_materialise_warmup"]["cpu_s"],
         "devCE": 6 * 27 * med(r["P4_devce4096"]),
         "scoring": 6 * 27 * med(r["P5_scoring4096"]) + ALLOC["oracle_s"],
         "ckpt_io": 6 * ser * (1 + ALLOC["store_write_factor"]),
         "generation": ALLOC["generation_s"], "bootstrap": ALLOC["bootstrap_s"],
         "fresh_test": 6 * med(r["P5_scoring4096"]) + ALLOC["fresh_test_extra_s"],
         "exports": ALLOC["exports_s"]}
    p["total"] = sum(p.values())
    p["limit_80pct"] = 0.8 * REMAINING_SCIENTIFIC_S
    p["fits"] = p["total"] <= p["limit_80pct"]
    p["train_wall_h_per_model"] = 5000 * r["update_wall_s"] / 3600.0
    return p


def run(repo: Path, store: Path, out: Path, mailbox: Path) -> dict:
    ensure_new_output_dir(out)
    store.mkdir(parents=True, exist_ok=True)
    ctl = RunControls(store / "tech_ledger.json", TECH_CAP_S, mailbox / "STOP", "0008-techbench",
                      TECH_CAP_S)
    result: dict = {"protocol": "x5g1-techbench-v1", "kind": "technical fixture timing only; "
                    "uniform random public tokens; not a scientific pilot"}
    with ctl:
        ctl.guard("data")
        dev_fit, dev_full = _dataset("dev_fit", N_DEV_FIT), _dataset("dev_full", N_DEV_FULL)
        data = {"train": _dataset("train", N_TRAIN), "dev_fit": dev_fit,
                "dev_fit_tensors": _tensors(dev_fit), "dev_full_tensors": _tensors(dev_full)}
        ctl.guard("data done")
        result["settings"] = [bench_setting(t, ctl, data) for t in THREADS]
        fits = [s for s in result["settings"] if s["projection"]["fits"]]
        best = min(fits, key=lambda s: (s["projection"]["total"], s["threads"])) if fits else None
        result["decision"] = {"chosen_threads": best["threads"] if best else None,
                              "B1": "RESOLVED" if best else "UNRESOLVED"}
        result["env"] = {"python": sys.executable, "torch": torch.__version__,
                         "numpy": np.__version__, "logical_cpus": os.cpu_count(),
                         "blas_env": {k: os.environ.get(k) for k in (
                             "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS")},
                         "model_config": STORED_MODEL,
                         "train_config_fixture": dataclasses.asdict(TrainConfig(
                             steps=WARMUP_UPDATES + MEASURED_UPDATES,
                             checkpoint_steps=(WARMUP_UPDATES,
                                               WARMUP_UPDATES + MEASURED_UPDATES)))}
        ctl.outcome = result["decision"]["B1"]

        def write(name: str, obj) -> None:
            (out / name).write_text(json.dumps(obj, indent=1, default=str), encoding="utf-8")

        def manifest() -> None:
            sums = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                    for f in sorted(out.iterdir()) if f.name != "MANIFEST.json"}
            (out / "MANIFEST.json").write_text(json.dumps(sums, indent=1), encoding="utf-8")

        guarded_export(ctl, [("timings", lambda: write("timings.json", result)),
                             ("projection", lambda: write("projection.json", {
                                 "settings": {s["threads"]: s["projection"]
                                              for s in result["settings"]},
                                 "decision": result["decision"]})),
                             ("manifest", manifest)], out / "EXPORT_STATUS.json")
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="X5 G1 technical throughput benchmark")
    ap.add_argument("--repo", type=Path, default=Path("."))
    ap.add_argument("--store", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mailbox", type=Path, required=True)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    res = run(args.repo, args.store, args.out, args.mailbox)
    log.info("techbench: %s", json.dumps(res["decision"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
