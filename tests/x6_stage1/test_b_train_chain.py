"""Author B (cloud): T-TRAIN-EQUIV, T-CHAIN (X6S1-FROZEN-v1 §4.3, §4.6, §5.4, §5.5; API.md §5).

CPU only, synthetic token pools in tmp_path; ticket steps/K are small. Fresh-process resumes run
`python -s x6s1_cloud.py train` (API §5.7). Chain discovery/marker tests: test_b_chain_ops.py.
"""
from __future__ import annotations

import copy
import dataclasses
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
from pathlib import Path

import numpy as np
import pytest
import torch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6_stage1"))

import x6s1_cloud as sc  # noqa: E402
import x6s1_data as sd  # noqa: E402
from topo_pilot.contracts import (  # noqa: E402
    ObservationSet, SeedTree, SequenceLayout, canonical_json)
from topo_pilot.dataset import PublicTokenDataset  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402
from topo_pilot.learner import TrainConfig, Trainer, TransformerLM  # noqa: E402
from topo_pilot.learner.trainer import _materialise  # noqa: E402

CPU, RUN_KEY, MODEL = torch.device("cpu"), ("x6s1", "smoke"), "SMOKE"
CLOUD = REPO / "tools" / "x6_stage1" / "x6s1_cloud.py"


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _head() -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001
        return "0" * 40


def _tokens(n, seed=7):
    return np.random.default_rng(seed).integers(0, 18, size=(n, 33), dtype=np.uint8)


def _cfg(steps, warmup):
    return TrainConfig(steps=steps, warmup=warmup, checkpoint_steps=(0, steps), device="cpu")


def _ds(toks):
    ids = make_sequence_ids(process_code("x6s1", "NA", "smoke", 0), "dev", len(toks))
    return PublicTokenDataset(ObservationSet(split="dev", V=18, sequence_id=ids, tokens=toks),
                              SequenceLayout())


def make_bundle(root, steps, k, n=256, warmup=2, wrong_stream=False):
    """A C0-shaped bundle (§5.3, API §5.1/§5.6) with the ticket's steps/K set by the caller."""
    (root / "data").mkdir(parents=True)
    (root / "init").mkdir()
    toks = _tokens(n)
    np.save(root / "data" / "smoke.npy", toks, allow_pickle=False)
    init = sd.init_state(MODEL)
    torch.save(init, root / "init" / "init_smoke.pt")
    head = _head()
    with tarfile.open(root / "code.tar", "w", format=tarfile.PAX_FORMAT,
                      pax_headers={"comment": head}) as tf:
        info = tarfile.TarInfo("pyproject.toml")
        info.size = 6
        tf.addfile(info, io.BytesIO(b"x = 1\n"))
    cfg = _cfg(steps, warmup)
    expected = sc.expected_digests(sd.MODEL_MASTER, RUN_KEY, n, steps, k)
    if wrong_stream:  # step-0 state right, chunk digests from another registered stream
        expected = expected[:1] + sc.expected_digests(sd.MODEL_MASTER, ("x6s1", 1), n, steps, k)[1:]
    files = ["code.tar", "data/smoke.npy", "init/init_smoke.pt", "ticket_C0.json"]
    entry = {"model": MODEL, "arm": "NA", "seed": "smoke", "run_key": list(RUN_KEY),
             "init_seed": sd.init_seed(MODEL), "batch_stream": ["batch_order", *RUN_KEY],
             "data_stream": ["x6s1", "smoke", "NA"],
             "data_seed": SeedTree(sd.DATA_MASTER).seed("x6s1", "smoke", "NA"),
             "data_file": "data/smoke.npy", "data_sha256": _sha((root / files[1]).read_bytes()),
             "token_sha256": sd.token_digest(toks), "n_rows": n, "init_file": files[2],
             "init_file_sha256": _sha((root / files[2]).read_bytes()),
             "init_weights_sha256": sc.weights_digest(init["model"]), "expected": expected}
    ticket = {"schema": sc.TICKET_SCHEMA, "wave": "C0", "bundle_files": files,
              "protocol_id": sd.PROTOCOL_ID, "protocol_sha256": sd.PROTOCOL_SHA256,
              "code_commit": head, "data_master": sd.DATA_MASTER, "model_master": sd.MODEL_MASTER,
              "model_config": dataclasses.asdict(sd.MODEL_CFG),
              "train_config": dataclasses.asdict(cfg), "steps": steps, "K": k, "batch_size": 128,
              "smoke_resume": True,
              "cell_templates_sha256": [_sha(t.encode("utf-8")) for t in sc.CELL_TEMPLATES],
              "models": [entry]}
    (root / "ticket_C0.json").write_bytes(canonical_json(ticket).encode("utf-8"))
    sums = "".join(f"{_sha((root / f).read_bytes())}  {f}\n" for f in sorted(files))
    (root / "SHA256SUMS").write_bytes(sums.encode("ascii"))
    return {"tokens": toks, "cfg": cfg, "entry": entry, "ticket": ticket, "init": init}


def run_child(root, max_chunks=None):
    args = [sys.executable, "-s", str(CLOUD), "train", str(root), MODEL, "--device", "cpu"]
    args += ["--max-chunks", str(max_chunks)] if max_chunks else []
    env = dict(os.environ, PYTHONPATH=str(REPO / "src"), OMP_NUM_THREADS="2",
               MKL_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2")
    return subprocess.run(args, env=env, capture_output=True, text=True, timeout=900)


def main_in_process(root, max_chunks=None):
    argv = ["train", str(root), MODEL, "--device", "cpu"]
    return sc.main(argv + (["--max-chunks", str(max_chunks)] if max_chunks else []))


class _RecGen:
    """Delegates to the real PCG64 generator and records every batch-index array."""

    def __init__(self, gen):
        self._g, self.draws = gen, []

    @property
    def bit_generator(self):
        return self._g.bit_generator

    def integers(self, *args, **kwargs):
        out = self._g.integers(*args, **kwargs)
        self.draws.append(np.array(out, copy=True))
        return out


class _Seeds:
    """Test-only delegating SeedTree wrapper exposing the reference generator (RC11)."""

    def __init__(self, master):
        self._tree, self.gen = SeedTree(master), None
        self.issued = self._tree.issued

    def seed(self, name, *scope):
        return self._tree.seed(name, *scope)

    def generator(self, name, *scope):
        gen = self._tree.generator(name, *scope)
        if name == "batch_order":
            self.gen = _RecGen(gen)
            return self.gen
        return gen


def reference(toks, cfg):
    """The unchanged Trainer.fit on CPU with 2 intra-op threads (§4.6 item 1)."""
    seeds, final = _Seeds(sd.MODEL_MASTER), {}
    trainer = Trainer(sd.MODEL_CFG, cfg, seeds, RUN_KEY)

    def on_checkpoint(step, model, info):
        if info["is_final"]:
            buf = io.BytesIO()
            torch.save({"optimizer": info["optimizer_state"],
                        "scheduler": info["scheduler_state"]}, buf)
            buf.seek(0)
            final.update(torch.load(buf, weights_only=False))
    old = torch.get_num_threads()
    torch.set_num_threads(2)
    try:
        trainer.fit(_ds(toks), _ds(toks[:64]), on_checkpoint)
    finally:
        torch.set_num_threads(old)
    final["model"] = {k: v.detach().clone() for k, v in trainer.model.state_dict().items()}
    final["pcg64"], final["draws"] = seeds.gen.bit_generator.state, seeds.gen.draws
    return final


def trainer_init():
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(SeedTree(sd.MODEL_MASTER).seed("init", *RUN_KEY))
        return TransformerLM(sd.MODEL_CFG).state_dict()


def same(a, b, path="$"):
    if isinstance(a, torch.Tensor):
        assert isinstance(b, torch.Tensor) and a.dtype == b.dtype and a.shape == b.shape, path
        assert torch.equal(a.cpu(), b.cpu()), path
    elif isinstance(a, dict):
        assert set(a) == set(b), (path, sorted(map(str, set(a) ^ set(b))))
        for key in a:
            same(a[key], b[key], f"{path}.{key}")
    elif isinstance(a, (list, tuple)):
        assert len(a) == len(b), path
        for i, (x, y) in enumerate(zip(a, b)):
            same(x, y, f"{path}[{i}]")
    else:
        assert a == b, (path, a, b)


def _batch_sha(arrays):
    return _sha(b"".join(np.asarray(a, "<i8").tobytes() for a in arrays))


# ---------------------------------------------------------------- T-TRAIN-EQUIV
@pytest.mark.parametrize("steps,k,warmup", [
    pytest.param(6, 2, 2, id="small"),
    pytest.param(60, 20, 10, id="equiv-cfg", marks=pytest.mark.slow),
])
def test_chunked_equals_trainer_bitwise_with_two_fresh_process_resumes(tmp_path, steps, k, warmup):
    root = tmp_path / "bundle"
    b = make_bundle(root, steps, k, warmup=warmup)
    for max_chunks in (1, 1, None):  # kill after K and 2K, resuming from disk each time
        res = run_child(root, max_chunks)
        assert res.returncode == 0, res.stdout + res.stderr
    ref = reference(b["tokens"], b["cfg"])
    mdir = root / "out" / MODEL
    final = torch.load(mdir / "ckpt" / f"{steps:06d}.pt", map_location="cpu", weights_only=False)
    same(final["model"], ref["model"], "model")
    same(final["optimizer"], ref["optimizer"], "optimizer")
    same(final["scheduler"], ref["scheduler"], "scheduler")
    lrs = [g["lr"] for g in final["optimizer"]["param_groups"]]
    assert lrs == list(ref["scheduler"]["_last_lr"])
    assert final["rng"]["pcg64"] == ref["pcg64"]
    assert final["step"] == steps and final["scheduler"]["last_epoch"] == steps
    init = torch.load(mdir / "ckpt" / "000000.pt", map_location="cpu", weights_only=False)
    same(init["model"], trainer_init(), "init")
    assert len(ref["draws"]) == steps
    for c, s in enumerate(range(k, steps + 1, k), start=1):
        rec = json.loads((mdir / "rec" / f"{s:06d}.json").read_text(encoding="utf-8"))
        want = _batch_sha(ref["draws"][(c - 1) * k:c * k])
        assert rec["batch_sha256"] == want == b["entry"]["expected"][c]["batch_sha256"]
        assert rec["step"] == s


def test_init_and_batch_order_identical_across_arms():
    states = [sd.init_state(f"{arm}-s1")["model"] for arm in sd.ARMS]
    for other in states[1:]:
        same(other, states[0])
    assert len({sc.weights_digest(s) for s in states}) == 1
    gens = [sd.batch_generator(f"{arm}-s1").integers(0, 2**20, size=128) for arm in sd.ARMS]
    assert all(np.array_equal(g, gens[0]) for g in gens)
    with torch.random.fork_rng(devices=[]):
        torch.manual_seed(SeedTree(sd.MODEL_MASTER).seed("init", "x6s1", 1))
        same(TransformerLM(sd.MODEL_CFG).state_dict(), states[0], "Trainer init")


# ---------------------------------------------------------------- T-CHAIN (formats)
def test_weights_digest_definition_and_pickling_independence():
    sd_ = {"b": torch.arange(2, dtype=torch.int64), "a": torch.ones(2, 3) * 0.5}
    h = hashlib.sha256()
    for key in sorted(sd_):
        t = sd_[key]
        h.update(key.encode() + b"\x00" + str(t.dtype).removeprefix("torch.").encode() + b"\x00")
        h.update(np.asarray(t.shape, "<i8").tobytes() + t.contiguous().numpy().tobytes())
    assert sc.weights_digest(sd_) == h.hexdigest()
    buf = io.BytesIO()
    torch.save(sd_, buf)
    buf.seek(0)
    assert sc.weights_digest(torch.load(buf, weights_only=True)) == h.hexdigest()


@pytest.mark.parametrize("steps,k", [(4, 2), (6, 3), (200, 100)])
def test_expected_digests_independent(steps, k):
    gen = SeedTree(sd.MODEL_MASTER).generator("batch_order", *RUN_KEY)

    def pcg():
        return _sha(canonical_json(gen.bit_generator.state).encode("utf-8"))
    want = [{"step": 0, "batch_sha256": None, "pcg64_state_sha256": pcg()}]
    for s in range(k, steps + 1, k):
        bsha = _batch_sha([gen.integers(0, 4096, size=128) for _ in range(k)])
        want.append({"step": s, "batch_sha256": bsha, "pcg64_state_sha256": pcg()})
    assert sc.expected_digests(sd.MODEL_MASTER, RUN_KEY, 4096, steps, k) == want


def test_checkpoint_write_single_buffer_fsync_and_duplicate_refusal(tmp_path, monkeypatch):
    mdir = tmp_path / "m"
    (mdir / "ckpt").mkdir(parents=True)
    calls, real = [], os.fsync
    monkeypatch.setattr(os, "fsync", lambda fd: (calls.append(fd), real(fd))[1])
    data = b"\x00checkpoint" * 100
    assert sc.write_checkpoint(mdir, 2, data) == _sha(data)
    target = mdir / "ckpt" / "000002.pt"
    assert target.read_bytes() == data and calls
    assert not list((mdir / "ckpt").glob("*.part"))
    with pytest.raises(sc.CloudStop, match="STOP: DUPLICATE STEP"):
        sc.write_checkpoint(mdir, 2, b"other bytes")
    assert target.read_bytes() == data


def test_checkpoint_not_published_when_reread_differs(tmp_path, monkeypatch):
    mdir = tmp_path / "m"
    (mdir / "ckpt").mkdir(parents=True)
    real = os.fsync

    def corrupt(fd):
        real(fd)
        for p in (mdir / "ckpt").glob("*.part"):
            p.write_bytes(b"torn write")
    monkeypatch.setattr(os, "fsync", corrupt)
    with pytest.raises(Exception):
        sc.write_checkpoint(mdir, 4, b"payload" * 50)
    assert not (mdir / "ckpt" / "000004.pt").exists()


def test_json_atomic_canonical_and_exclusive(tmp_path):
    obj = {"b": 1, "a": [1, 2], "c": None}
    p = tmp_path / "rec" / "000000.json"
    p.parent.mkdir()
    assert sc.write_json_atomic(p, obj) == _sha(canonical_json(obj).encode("utf-8"))
    assert p.read_bytes() == canonical_json(obj).encode("utf-8")
    with pytest.raises((sc.CloudStop, FileExistsError)):
        sc.write_json_atomic(p, {"x": 1})


# ---------------------------------------------------------------- T-CHAIN (resume)
def _marker(mdir, recs):
    return sc.write_marker(mdir, {"schema": sc.MARKER_SCHEMA, "model": MODEL, "step": 3,
                                  "chunk": 2, "session_id": "sess", "loss_bits": "7fc00000",
                                  "prev_record_sha256": recs[-1]["record_sha256"],
                                  "utc": "2026-10-19T00:00:00Z"})


def test_resume_restores_state_and_checks_internal_consistency(tmp_path):
    cfg, toks = _cfg(4, 2), _tokens(256)
    x, y = _materialise(_ds(toks))
    gen = SeedTree(sd.MODEL_MASTER).generator("batch_order", *RUN_KEY)
    st = sc.fresh_state(sd.init_state(MODEL)["model"], sd.MODEL_CFG, cfg, gen, CPU)
    idx = sc.draw_indices(st.gen, 256, 2)
    assert sc.train_chunk(st, x, y, idx)["finite"] and st.step == 2
    ckpt = torch.load(io.BytesIO(sc.snapshot_bytes(st)), weights_only=False)
    assert ckpt["step"] == 2 and ckpt["scheduler"]["last_epoch"] == 2
    pcg = sc.pcg64_state(st.gen)
    rec = sc.make_record(MODEL, 2, "f" * 64, sc.weights_digest(ckpt["model"]),
                         sc.batch_digest(idx), pcg, "0" * 64, "s", "cpu", None, 1.0, 1.0, True, 1.0)
    exp = {"step": 2, "batch_sha256": sc.batch_digest(idx),
           "pcg64_state_sha256": sc.pcg64_digest(pcg)}
    assert sc.check_internal(ckpt, rec, exp) == []
    st2 = sc.restore_state(ckpt, sd.MODEL_CFG, cfg, CPU)
    same(st2.model.state_dict(), st.model.state_dict())
    same(st2.opt.state_dict(), st.opt.state_dict())
    same(st2.sched.state_dict(), st.sched.state_dict())
    assert st2.gen.bit_generator.state == st.gen.bit_generator.state
    assert st2.step == 2 and st2.model.training and st2.train_cfg == cfg
    assert st2.model_cfg == sd.MODEL_CFG
    nxt = sc.draw_indices(st.gen, 256, 2)
    assert all(np.array_equal(a, b) for a, b in zip(nxt, sc.draw_indices(st2.gen, 256, 2)))
    sc.train_chunk(st, x, y, nxt)
    sc.train_chunk(st2, x, y, nxt)
    same(st2.model.state_dict(), st.model.state_dict(), "continued")
    bad = []
    for edit in ("step", "phase", "groups"):
        c = copy.deepcopy(ckpt)
        if edit == "step":
            c["step"] = 3
        elif edit == "phase":
            c["scheduler"]["last_epoch"] = 1
        else:
            c["optimizer"]["param_groups"] = c["optimizer"]["param_groups"][:1]
        bad.append(sc.check_internal(c, rec, exp))
    other = dict(exp, pcg64_state_sha256="0" * 64)
    bad.append(sc.check_internal(ckpt, rec, other))
    assert all(b for b in bad)


def test_cli_resume_marker_and_batch_precheck(tmp_path):
    root = tmp_path / "bundle"
    b = make_bundle(root, 4, 2)
    mdir = root / "out" / MODEL
    assert main_in_process(root, 1) == 0  # PAUSED after step 2
    assert sorted(p.name for p in (mdir / "rec").glob("*.json")) == ["000000.json", "000002.json"]
    d = sc.discover(mdir, b["entry"], 4, 2)
    assert d["status"] == "OK" and d["last_step"] == 2
    _marker(mdir, d["chain"])  # terminal NONFINITE blocks further updates and retraining
    assert main_in_process(root) == 3
    assert not (mdir / "ckpt" / "000004.pt").exists()
    garbage = tmp_path / "garbage"
    make_bundle(garbage, 4, 2)
    assert main_in_process(garbage, 1) == 0
    (garbage / "out" / MODEL / "rec" / "NONFINITE.json").write_bytes(b"{")
    assert main_in_process(garbage) == 2  # STOP: MARKER UNREADABLE stops recovery
    assert not (garbage / "out" / MODEL / "ckpt" / "000004.pt").exists()
    bad = tmp_path / "wrong"
    make_bundle(bad, 4, 2, wrong_stream=True)
    assert main_in_process(bad) == 2  # STOP: BATCH-ID MISMATCH before any update
    assert not (bad / "out" / MODEL / "ckpt" / "000002.pt").exists()


def test_record_published_only_after_checkpoint_verifies(tmp_path, monkeypatch):
    root = tmp_path / "bundle"
    make_bundle(root, 4, 2)
    real = sc.write_checkpoint

    def failing(model_dir, step, data):
        if step == 2:
            raise OSError("synthetic Drive write failure")
        return real(model_dir, step, data)
    monkeypatch.setattr(sc, "write_checkpoint", failing)
    try:
        main_in_process(root)
    except Exception:  # noqa: BLE001  the failure may propagate
        pass
    assert not (root / "out" / MODEL / "rec" / "000002.json").exists()
