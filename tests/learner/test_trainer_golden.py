"""T-GOLD (D2A-FROZEN-v1 §4.6): the default Trainer path is byte-identical to golden values
generated at commit A by the unchanged Trainer, for two configurations at one and two intra-op
threads (one inter-op thread). Each case runs in its own subprocess so the thread settings are
applied before any torch work. Regenerate (commit A only): python test_trainer_golden.py --write
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
GOLDEN = HERE / "golden_default_trainer.json"
CASES = [(name, n) for name in ("tiny", "pilot") for n in (1, 2)]


def _configs(name):
    from topo_pilot.learner import ModelConfig, TrainConfig

    if name == "tiny":
        return (ModelConfig(6, 5, n_layers=1, d_model=16, n_heads=2, d_mlp=32),
                TrainConfig(steps=4, warmup=2, batch_size=8, checkpoint_steps=(0, 2, 4),
                            device="cpu"))
    return ModelConfig(6, 5), TrainConfig(steps=3, warmup=2, checkpoint_steps=(0, 1, 3),
                                          device="cpu")


def _worker(name: str, n: int) -> dict:
    import torch

    torch.set_num_interop_threads(1)
    torch.set_num_threads(n)
    import numpy as np

    sys.path.insert(0, str(REPO / "tools" / "d1_seam"))
    from d1_seam import float_model

    from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout
    from topo_pilot.dataset import HMMSampler, PublicTokenDataset
    from topo_pilot.learner import Trainer, serialise_state

    fm, seeds, layout = float_model(), SeedTree(7), SequenceLayout()
    sampler = HMMSampler(fm["T"], fm["E_mix"], fm["mu"], layout)
    sets = {}
    for split, size in (("train", 64), ("dev", 16)):
        tokens, _ = sampler.sample(size, seeds.generator("golden", split))
        obs = ObservationSet(split=split, V=5, sequence_id=np.arange(size, dtype=np.int64),
                             tokens=tokens)
        sets[split] = PublicTokenDataset(obs, layout)
    model_cfg, train_cfg = _configs(name)
    record = {"checkpoints": []}

    def on_checkpoint(step, model, info):
        blob = serialise_state(model, info)
        record["checkpoints"].append({"step": step, "dev_ce": repr(info["dev_ce"]),
                                      "state_sha256": hashlib.sha256(blob).hexdigest()})

    summary = Trainer(model_cfg, train_cfg, SeedTree(7), ("golden", name)).fit(
        sets["train"], sets["dev"], on_checkpoint)
    record["final_train_loss"] = repr(summary.final_train_loss)
    record["threads"] = {"intra": torch.get_num_threads(),
                         "interop": torch.get_num_interop_threads()}
    return record


def _run_case(name: str, n: int) -> dict:
    env = dict(os.environ, PYTHONPATH=str(REPO / "src"))
    for var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
        env[var] = str(n)
    out = subprocess.run([sys.executable, str(Path(__file__)), "--worker", name, str(n)],
                         capture_output=True, text=True, env=env, cwd=str(REPO), check=True)
    return json.loads(out.stdout.strip().splitlines()[-1])


def _environment() -> dict:
    import numpy
    import torch

    head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True,
                          text=True).stdout.strip()
    return {"source_commit": head, "python": sys.version, "torch": torch.__version__,
            "numpy": numpy.__version__, "platform": platform.platform(),
            "torch_config_parallel": torch.__config__.parallel_info().splitlines()[:6],
            "fixture": "d1_seam.float_model CM; HMMSampler; SeedTree(7) golden/train 64, "
                       "golden/dev 16; run_key (golden, name)"}


def test_default_trainer_matches_golden():
    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
    for name, n in CASES:
        got = _run_case(name, n)
        assert got == golden["cases"][f"{name}/{n}"], f"{name} at {n} threads differs"


if __name__ == "__main__":
    if sys.argv[1:2] == ["--worker"]:
        print(json.dumps(_worker(sys.argv[2], int(sys.argv[3]))))
    elif sys.argv[1:2] == ["--write"]:
        if GOLDEN.exists():
            raise SystemExit("golden file exists; regenerate only at commit A")
        cases = {f"{name}/{n}": _run_case(name, n) for name, n in CASES}
        GOLDEN.write_text(json.dumps({"environment": _environment(), "cases": cases},
                                     indent=1, sort_keys=True) + "\n", encoding="utf-8")
