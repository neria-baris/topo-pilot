"""X6S1 cloud (leaf; Colab and local): bundle check, environment and session records, the chunked
Trainer-equivalent loop, checkpoint/record I/O, chain discovery, quarantine, run_wave, finalise and
the six notebook cells (X6S1-FROZEN-v1 §4.3, §5.3-§5.11; API.md §5, §12). Imports only the
standard library, numpy, torch and topo_pilot; no sys.path edit. Import performs no I/O."""
# fmt: off

from __future__ import annotations

import dataclasses
import hashlib
import io
import json
import os
import platform
import re
import subprocess
import sys
import tarfile
import time
import uuid
from pathlib import Path

import numpy as np
import torch

from topo_pilot.contracts import ObservationSet, SeedTree, SequenceLayout, canonical_json
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.dataset.checks import make_sequence_ids, process_code
from topo_pilot.learner import ModelConfig, TrainConfig, TransformerLM
from topo_pilot.learner.trainer import WarmupCosine, _materialise, lm_loss

HASH_PLACEHOLDER = "PASTE_BUNDLE_SHA256_HERE"
TICKET_SCHEMA, RECORD_SCHEMA = "x6s1-ticket-v1", "x6s1-record-v1"
MARKER_SCHEMA = "x6s1-nonfinite-v1"
SESSION_SCHEMA, MANIFEST_SCHEMA = "x6s1-session-v1", "x6s1-manifest-v1"
_MODEL_CFG = ModelConfig(vocab_in=19, vocab_out=18)  # = x6s1_data.MODEL_CFG (leaf module)
_ENV_FIELDS = ("python", "numpy", "torch", "cuda", "cudnn")
_TERMINAL = ("DONE", "INVALID:NONFINITE")
CELL_TEMPLATES = tuple(c.strip("\n") for c in """
# X6S1 cell 1: GPU
import subprocess, torch
print(subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version,memory.total", \
"--format=csv,noheader"], capture_output=True, text=True).stdout.strip())
if not torch.cuda.is_available():
    raise SystemExit("NO GPU")
print("GPU OK:", torch.cuda.get_device_name(0))
@@
# X6S1 cell 2: Drive
import glob
from google.colab import drive
drive.mount("/content/drive")
BUNDLE_SHA256 = "PASTE_BUNDLE_SHA256_HERE"
_hits = glob.glob("/content/drive/MyDrive/X6S1/*-" + BUNDLE_SHA256.strip().lower()[:12])
if len(_hits) != 1:
    raise SystemExit("STOP: BUNDLE DIRECTORY")
ROOT = _hits[0]
print("ROOT", ROOT[len("/content/drive/MyDrive/"):])
@@
# X6S1 cell 3: verify
import hashlib, sys, tarfile
def _h(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
if _h(ROOT + "/SHA256SUMS") != BUNDLE_SHA256.strip().lower():
    raise SystemExit("STOP: BUNDLE HASH MISMATCH")
_sums = {l[66:]: l[:64] for l in open(ROOT + "/SHA256SUMS", encoding="utf-8").read().splitlines()}
if _h(ROOT + "/code.tar") != _sums.get("code.tar"):
    raise SystemExit("STOP: BUNDLE HASH MISMATCH")
tarfile.open(ROOT + "/code.tar").extractall("/content/x6s1")
sys.path[:0] = ["/content/x6s1/src", "/content/x6s1/tools/x6_stage1"]
import x6s1_cloud
BUNDLE = x6s1_cloud.verify_bundle(ROOT, BUNDLE_SHA256.strip().lower())
@@
# X6S1 cell 4: environment
ENV = x6s1_cloud.environment(ROOT, BUNDLE)
x6s1_cloud.precheck(ROOT, ENV)
@@
# X6S1 cell 5: train
x6s1_cloud.run_wave(ROOT, ENV)
@@
# X6S1 cell 6: finalise
x6s1_cloud.finalise(ROOT)
drive.flush_and_unmount()
""".split("@@\n"))
_CURRENT_ENV: dict = {}

class CloudStop(RuntimeError):
    """The exact `STOP: ...` line (API.md §5.2)."""

def _req(ok, stop: str) -> None:
    if not ok:
        raise CloudStop(stop)
def utc_iso() -> str: return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def utc_stamp() -> str: return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

# ---- hashing and digests (§5.3) ----
def sha256_bytes(b) -> str: return hashlib.sha256(b).hexdigest()
def _read(path) -> bytes:
    with open(path, "rb") as fh:  # builtins open: a Drive read failure is an OSError
        return fh.read()
def sha256_file(path) -> str: return sha256_bytes(_read(path))
def sha256_json(obj) -> str: return sha256_bytes(canonical_json(obj).encode("utf-8"))
def _rjson(path): return json.loads(_read(path).decode("utf-8"))
def batch_digest(arrays) -> str:
    return sha256_bytes(b"".join(np.asarray(a, "<i8").tobytes() for a in arrays))
def pcg64_state(gen) -> dict: return json.loads(json.dumps(gen.bit_generator.state))
def pcg64_digest(state) -> str: return sha256_json(state)
def weights_digest(state_dict) -> str:
    h = hashlib.sha256()
    for key in sorted(state_dict):
        t = state_dict[key].detach().cpu().contiguous()
        a = t.numpy()
        h.update(key.encode("utf-8") + b"\x00" + str(t.dtype).removeprefix("torch.").encode("utf-8")
                 + b"\x00" + np.asarray(t.shape, "<i8").tobytes()
                 + a.astype(a.dtype.newbyteorder("<"), copy=False).tobytes())
    return h.hexdigest()
def generator_from_state(state) -> np.random.Generator:
    bg = np.random.PCG64()
    bg.state = state
    return np.random.Generator(bg)
def draw_indices(gen, n_rows, k, batch=128) -> list:
    return [np.asarray(gen.integers(0, n_rows, size=batch), np.int64) for _ in range(k)]
def expected_digests(model_master, run_key, n_rows, steps, k, batch=128) -> list:
    gen, out = SeedTree(model_master).generator("batch_order", *run_key), []
    for s in range(0, steps + 1, k):
        b = batch_digest(draw_indices(gen, n_rows, k, batch)) if s else None
        out.append({"step": s, "batch_sha256": b,
                    "pcg64_state_sha256": pcg64_digest(pcg64_state(gen))})
    return out

# ---- training core (§4.3; API.md §5.4) ----
TrainState = dataclasses.make_dataclass("TrainState", [
    "model", "opt", "sched", "gen", ("step", int), "device", "model_cfg", "train_cfg"])
def _groups(model) -> tuple:
    decay, plain = [], []
    for name, p in model.named_parameters():
        (decay if p.ndim == 2 and not name.startswith(("tok_emb", "pos_emb")) else plain).append(p)
    return decay, plain
def build_optimizer(model, train_cfg) -> torch.optim.AdamW:
    decay, plain = _groups(model)
    return torch.optim.AdamW([{"params": decay, "weight_decay": train_cfg.weight_decay},
                              {"params": plain, "weight_decay": 0.0}], lr=train_cfg.lr)
def build_scheduler(opt, cfg):
    return torch.optim.lr_scheduler.LambdaLR(opt, WarmupCosine(cfg.warmup, cfg.steps))
def set_precision(device) -> dict:
    torch.backends.cuda.matmul.allow_tf32 = torch.backends.cudnn.allow_tf32 = False
    torch.set_float32_matmul_precision("highest")
    torch.use_deterministic_algorithms(True, warn_only=True)
    return {"deterministic": torch.are_deterministic_algorithms_enabled(), "tf32_matmul": False,
            "tf32_cudnn": False, "matmul_precision": torch.get_float32_matmul_precision(),
            "cublas_workspace_config": os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")}
def fresh_state(init_sd, model_cfg, train_cfg, gen, device):
    with torch.random.fork_rng(devices=[]):
        model = TransformerLM(model_cfg)
    model.load_state_dict(init_sd, strict=True)
    model = model.to(device).train()
    opt = build_optimizer(model, train_cfg)
    return TrainState(model, opt, build_scheduler(opt, train_cfg), gen, 0, device, model_cfg,
                      train_cfg)
def restore_state(ckpt, model_cfg, train_cfg, device):
    gen = generator_from_state(ckpt["rng"]["pcg64"])
    st = fresh_state(ckpt["model"], model_cfg, train_cfg, gen, device)
    st.opt.load_state_dict(ckpt["optimizer"])
    st.sched.load_state_dict(ckpt["scheduler"])
    st.step = int(ckpt["step"])
    return st
def check_internal(ckpt, record, expected, model_cfg=None) -> list:
    with torch.random.fork_rng(devices=[]):
        sizes = tuple(len(g) for g in _groups(TransformerLM(model_cfg or _MODEL_CFG)))
    step, groups = ckpt.get("step"), ckpt.get("optimizer", {}).get("param_groups", [])
    pcg = (pcg64_digest(ckpt.get("rng", {}).get("pcg64")), record.get("pcg64_state_sha256"))
    return [name for name, ok in (
        ("step", step == record.get("step") == expected.get("step")),
        ("scheduler phase", ckpt.get("scheduler", {}).get("last_epoch") == step),
        ("optimizer groups", tuple(len(g["params"]) for g in groups) == sizes),
        ("pcg64 state", pcg[0] == pcg[1] == expected.get("pcg64_state_sha256"))) if not ok]
def train_chunk(st, x, y, idx_arrays) -> dict:
    losses = []
    for a in idx_arrays:
        idx = torch.from_numpy(np.asarray(a, np.int64)).to(st.device)
        loss = lm_loss(st.model(x[idx]).logits, y[idx])
        if not torch.isfinite(loss):
            v = np.asarray(float(loss.detach()), "<f4" if loss.dtype == torch.float32 else "<f8")
            return {"finite": False, "step": st.step + 1, "loss_bits": v.tobytes().hex()}
        st.opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(st.model.parameters(), st.train_cfg.grad_clip)
        st.opt.step()
        st.sched.step()
        st.step += 1
        losses.append(float(loss.detach()))
    return {"finite": True, "loss_first": losses[0], "loss_last": losses[-1]}
def snapshot_bytes(st) -> bytes:
    buf, cuda = io.BytesIO(), torch.cuda.get_rng_state_all() if st.device.type == "cuda" else []
    torch.save({"model": {k: v.detach().cpu().clone() for k, v in st.model.state_dict().items()},
                "optimizer": st.opt.state_dict(), "scheduler": st.sched.state_dict(),
                "rng": {"pcg64": pcg64_state(st.gen), "torch_cpu": torch.get_rng_state(),
                        "torch_cuda": cuda}, "step": int(st.step)}, buf)
    return buf.getvalue()
def load_checkpoint(path, device) -> dict:
    return torch.load(path, map_location=device, weights_only=False)
def materialise(tokens, arm="NA", seed="smoke") -> tuple:
    sm = seed == "smoke"
    split, code = ("dev", ("NA", "smoke", 0)) if sm else ("train", (arm, "train", seed))
    ids = make_sequence_ids(process_code("x6s1", *code), split, len(tokens))
    return _materialise(PublicTokenDataset(ObservationSet(split, 18, ids, np.asarray(tokens)),
                                           SequenceLayout()))

# ---- atomic I/O and the chain (§5.4, §5.5) ----
def _publish(target: Path, data: bytes, stop: str) -> str:
    _req(not target.exists(), stop)
    part, want = target.with_name(target.name + ".part"), sha256_bytes(data)
    with open(part, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    if sha256_file(part) != want:
        raise OSError(f"re-read of {part.name} does not verify")
    _req(not target.exists(), stop)
    os.replace(part, target)
    return want
def write_checkpoint(model_dir, step, data: bytes) -> str:
    md = Path(model_dir)
    return _publish(md / "ckpt" / f"{step:06d}.pt", data, f"STOP: DUPLICATE STEP {md.name} {step}")
def write_json_atomic(path, obj) -> str:
    if Path(path).exists():
        raise FileExistsError(str(path))
    return _publish(Path(path), canonical_json(obj).encode("utf-8"), f"STOP: DUPLICATE STEP {path}")
def record_sha(rec) -> str:
    return sha256_json({k: v for k, v in rec.items() if k != "record_sha256"})
def make_record(model, step, file_sha, weights_sha, batch_sha, pcg_state, prev_sha, session_id,
                device_name, cuda_capability, loss_first, loss_last, loss_finite, wall_s) -> dict:
    rec = {"schema": RECORD_SCHEMA, "model": model, "step": int(step),
           "file": f"ckpt/{step:06d}.pt", "file_sha256": file_sha, "weights_sha256": weights_sha,
           "batch_sha256": batch_sha,
           "pcg64_state": pcg_state, "pcg64_state_sha256": pcg64_digest(pcg_state),
           "prev_record_sha256": prev_sha, "session_id": session_id, "device_name": device_name,
           "cuda_capability": cuda_capability, "train_loss_first": loss_first,
           "train_loss_last": loss_last, "loss_finite": loss_finite, "wall_s": wall_s,
           "utc": utc_iso()}
    return dict(rec, record_sha256=record_sha(rec))
def valid_record(model_dir, rec) -> bool:
    try:
        f = Path(model_dir) / rec["file"]
        return rec["record_sha256"] == record_sha(rec) and f.is_file() and \
            sha256_file(f) == rec["file_sha256"]
    except (KeyError, TypeError):
        return False
def _parse(raw: bytes):
    try:
        rec = json.loads(raw.decode("utf-8"))
        ok = isinstance(rec, dict) and rec.get("record_sha256") == record_sha(rec)
        return rec if ok else None
    except ValueError:
        return None
def _wsha(path) -> str:
    return weights_digest(torch.load(path, map_location="cpu", weights_only=True)["model"])
def discover(model_dir, entry, steps, k) -> dict:
    md, out = Path(model_dir), {"chain": [], "last_step": None, "terminal": None, "orphans": []}
    try:
        out["terminal"] = read_marker(md)
    except CloudStop:
        return dict(out, status="MARKER_UNREADABLE")
    try:
        files = sorted(p.relative_to(md).as_posix() for d in ("ckpt", "rec") if (md / d).is_dir()
                       for p in (md / d).iterdir())
        prev, used = sha256_json(entry), set()
        for s in range(0, steps + 1, k):
            rp, cp, nx = f"rec/{s:06d}.json", f"ckpt/{s:06d}.pt", f"rec/{s + k:06d}.json"
            rec = _parse(_read(md / rp)) if rp in files else None
            if not (rec and rec.get("step") == s and rec.get("prev_record_sha256") == prev
                    and cp in files and sha256_file(md / cp) == rec.get("file_sha256")
                    and _wsha(md / cp) == rec.get("weights_sha256")):
                later = _parse(_read(md / nx)) if rec and nx in files else None
                if later and later.get("prev_record_sha256") == rec.get("record_sha256"):
                    return dict(out, status="CHAIN_BROKEN")  # broken interior link (§5.8)
                break
            out["chain"].append(rec)
            used, prev = used | {rp, cp}, rec["record_sha256"]
    except OSError:
        return dict(out, status="HOLD")
    out["last_step"] = out["chain"][-1]["step"] if out["chain"] else None
    out["orphans"] = [f for f in files if f not in used and f != "rec/NONFINITE.json"]
    return dict(out, status="OK")
def read_marker(model_dir):
    rec = Path(model_dir) / "rec"
    names = sorted(p.name for p in rec.glob("NONFINITE*") if not p.name.endswith(".part"))
    if not names:
        return None
    try:
        m = _rjson(rec / names[0]) if names == ["NONFINITE.json"] else None
        body = {k: v for k, v in m.items() if k != "marker_sha256"}
        _req(m.get("marker_sha256") == sha256_json(body), "")
        return m
    except (OSError, ValueError, AttributeError, CloudStop) as exc:
        raise CloudStop(f"STOP: MARKER UNREADABLE {Path(model_dir).name}") from exc
def write_marker(model_dir, info) -> dict:
    m = {k: v for k, v in info.items() if k != "marker_sha256"}
    m = dict(m, marker_sha256=sha256_json(m))
    write_json_atomic(Path(model_dir) / "rec" / "NONFINITE.json", m)
    return m
def quarantine(root, model, orphans, utc) -> list:
    out, md = [], Path(root) / "out" / model
    for rel in (o for o in orphans if o != "rec/NONFINITE.json"):
        src, dst = md / rel, Path(root) / "orphans" / f"{utc}-{model}" / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(_read(src))
        if (h := sha256_file(dst)) != sha256_file(src):
            raise OSError(f"preservation copy of {rel} does not verify")
        src.unlink()
        out.append({"original": f"out/{model}/{rel}",
                    "preserved": dst.relative_to(root).as_posix(), "sha256": h})
    return out
def _save(md, st, entry, env, prev, chunk) -> dict:
    fsha = write_checkpoint(md, st.step, snapshot_bytes(st))
    rec = make_record(entry["model"], st.step, fsha, weights_digest(st.model.state_dict()),
                      chunk[0], pcg64_state(st.gen), prev, env.get("session_id"),
                      env.get("device_name"),
                      env.get("cuda_capability"), *chunk[1:])
    write_json_atomic(md / "rec" / f"{st.step:06d}.json", rec)
    return rec
def _next_chunk(entry, ticket, gen, step) -> list:
    """§5.4 step 6: the next chunk's index arrays, drawn from a copy and checked before use."""
    idx = draw_indices(generator_from_state(pcg64_state(gen)), entry["n_rows"], int(ticket["K"]),
                       ticket.get("batch_size", 128))
    _req(batch_digest(idx) == entry["expected"][step // int(ticket["K"]) + 1]["batch_sha256"],
         f"STOP: BATCH-ID MISMATCH {entry['model']}")
    return idx
def train_chunked(root, entry, ticket, env, device, max_chunks=None, log=print, _reenter=True):
    model, steps, K, root = entry["model"], int(ticket["steps"]), int(ticket["K"]), Path(root)
    md, p, pi = root / "out" / model, root / entry["data_file"], root / entry["init_file"]
    (md / "rec").mkdir(parents=True, exist_ok=True)
    (md / "ckpt").mkdir(exist_ok=True)
    if read_marker(md) is not None:
        return "INVALID:NONFINITE"
    d = discover(md, entry, steps, K)
    _req(d["status"] == "OK", f"STOP: CHAIN BROKEN {model}" if d["status"] == "CHAIN_BROKEN"
         else f"STOP: HOLD {model} {d['status']}")
    if d["orphans"]:
        env.setdefault("orphans", []).extend(quarantine(root, model, d["orphans"], utc_stamp()))
    mcfg, tcfg = ModelConfig(**ticket["model_config"]), TrainConfig(**ticket["train_config"])
    _req(sha256_file(p) == entry["data_sha256"], f"STOP: TICKET data {model}")
    toks = np.load(p, allow_pickle=False)
    x, y = (t.to(device) for t in materialise(toks, entry["arm"], entry["seed"]))
    if d["last_step"] is None:  # step 0 from the uploaded init state (§5.4 step 2)
        init = torch.load(pi, map_location="cpu", weights_only=True)["model"]
        gen = SeedTree(ticket["model_master"]).generator("batch_order", *entry["run_key"])
        _req(sha256_file(pi) == entry["init_file_sha256"] and weights_digest(init) ==
             entry["init_weights_sha256"], f"STOP: TICKET init {model}")
        _req(pcg64_digest(pcg64_state(gen)) == entry["expected"][0]["pcg64_state_sha256"],
             f"STOP: RNG STATE MISMATCH {model}")
        st = fresh_state(init, mcfg, tcfg, gen, device)
        rec = _save(md, st, entry, env, sha256_json(entry), (None,) * 5)
    else:
        rec = d["chain"][-1]
        ckpt = load_checkpoint(md / rec["file"], device)
        _req(not check_internal(ckpt, rec, entry["expected"][rec["step"] // K], mcfg),
             f"STOP: RNG STATE MISMATCH {model}")
        st = restore_state(ckpt, mcfg, tcfg, device)
    chunk = 0
    while st.step < steps:
        if max_chunks is not None and chunk >= max_chunks:
            return "PAUSED"
        idx = _next_chunk(entry, ticket, st.gen, st.step)
        draw_indices(st.gen, entry["n_rows"], K, ticket.get("batch_size", 128))  # identical draws
        t0, c, out = time.perf_counter(), st.step // K + 1, train_chunk(st, x, y, idx)
        if not out["finite"]:
            write_marker(md, {"schema": MARKER_SCHEMA, "model": model, "step": out["step"],
                              "chunk": c, "session_id": env.get("session_id"),
                              "loss_bits": out["loss_bits"],
                              "prev_record_sha256": rec["record_sha256"], "utc": utc_iso()})
            log(f"[{model}] NONFINITE at step {out['step']}")
            return "INVALID:NONFINITE"
        rec = _save(md, st, entry, env, rec["record_sha256"], (
            batch_digest(idx), out["loss_first"], out["loss_last"], True, time.perf_counter() - t0))
        log(f"[{model}] step {st.step:05d}/{steps:05d} ok ckpt {rec['file_sha256'][:8]} "
            f"{rec['wall_s']:.1f} s")
        chunk += 1
        if ticket.get("smoke_resume") and _reenter and st.step < steps:  # §5.9: re-enter once
            del st, x, y
            left = None if max_chunks is None else max_chunks - chunk
            return train_chunked(root, entry, ticket, env, device, left, log, False)
    log(f"MODEL DONE {model} weights {rec['weights_sha256'][:4]}…")
    return "DONE"

# ---- notebook-facing functions (§5.7) ----
def executed_sources() -> list:
    try:
        return list(get_ipython().user_ns["In"][1:])  # noqa: F821
    except NameError:
        return []
def normalise_source(src) -> str:
    s = "\n".join(line.rstrip() for line in src.replace("\r\n", "\n").split("\n")).rstrip("\n")
    return re.sub(r'BUNDLE_SHA256 = "[0-9A-Fa-f]{64}"', f'BUNDLE_SHA256 = "{HASH_PLACEHOLDER}"', s)
def _cells() -> list: return [normalise_source(s) for s in executed_sources()]
def _tar_commit(path) -> str:
    with tarfile.open(path) as tf:
        return tf.pax_headers.get("comment", "")
def verify_bundle(root, bundle_sha256) -> dict:
    root, want = Path(root), str(bundle_sha256).strip().lower()
    sums = _read(root / "SHA256SUMS")
    listed = {line[66:]: line[:64] for line in sums.decode("utf-8").splitlines()}
    _req(sha256_bytes(sums) == want and all(sha256_file(root / f) == h for f, h in listed.items()),
         "STOP: BUNDLE HASH MISMATCH")
    tk = [f for f in listed if f.startswith("ticket_")]
    ticket = _rjson(root / tk[0]) if len(tk) == 1 else {}
    _req(ticket.get("schema") == TICKET_SCHEMA and sorted(ticket["bundle_files"]) == sorted(listed),
         "STOP: TICKET schema")
    commit = _tar_commit(root / "code.tar")
    _req(commit == ticket["code_commit"], "STOP: BUNDLE HASH MISMATCH")
    print(f"BUNDLE OK {want[:8].upper()}… wave {ticket['wave']}, {len(ticket['models'])} models, "
          f"code {commit[:7]}")
    return {"root": str(root), "bundle_sha256": want, "bundle_id": f"{ticket['wave']}-{want[:12]}",
            "ticket": ticket, "ticket_sha256": listed[tk[0]], "code_commit": commit}
def environment(root, bundle) -> dict:
    _req(torch.cuda.is_available(), "STOP: NO GPU")
    q = subprocess.run(["nvidia-smi", "--query-gpu=name,driver_version,memory.total",
                        "--format=csv,noheader"], capture_output=True, text=True).stdout
    gpu = dict(zip(("name", "driver", "memory"), [s.strip() for s in (q + ",,").split(",")]))
    tar = Path(root) / "code.tar"
    env = {"schema": SESSION_SCHEMA, "kind": "start", "session_id": uuid.uuid4().hex,
           "utc": utc_iso(),
           "python": platform.python_version(), "numpy": np.__version__, "torch": torch.__version__,
           "cuda": torch.version.cuda, "cudnn": torch.backends.cudnn.version(), "gpu": gpu,
           "flags": set_precision(torch.device("cuda")), "code_commit": _tar_commit(tar),
           "code_tar_sha256": sha256_file(tar), "ticket_sha256": bundle["ticket_sha256"],
           "sha256sums_sha256": bundle["bundle_sha256"], "env_compare": [], "models": [],
           "orphans": [], "stops": [], "executed_cells": _cells(), "bundle": bundle,
           "device_name": torch.cuda.get_device_name(0),
           "cuda_capability": ".".join(map(str, torch.cuda.get_device_capability(0)))}
    _CURRENT_ENV.clear()
    _CURRENT_ENV.update(env)
    print(f"ENV OK torch {env['torch']} cuda {env['cuda']} {gpu['name']}")
    return env
def _sessions(root, kind) -> list: return sorted((Path(root) / "sessions").glob(f"*.{kind}.json"))
def _model_status(root, entry, ticket) -> tuple:
    d = discover(Path(root) / "out" / entry["model"], entry, ticket["steps"], ticket["K"])
    done = "DONE" if d["last_step"] == ticket["steps"] else "INCOMPLETE"
    return ("INVALID:NONFINITE" if d["terminal"] else done), d
def precheck(root, env) -> dict:
    old = _rjson(_sessions(root, "start")[-1]) if _sessions(root, "start") else {}
    for f in (f for f in _ENV_FIELDS if old and old.get(f) != env.get(f)):
        env["env_compare"].append({"field": f, "old": old.get(f), "new": env.get(f)})
        print(f"ENV CHANGED {f}: {old.get(f)} → {env.get(f)}")
    ticket = env["bundle"]["ticket"]
    for e in ticket["models"]:
        status, d = _model_status(root, e, ticket)
        _req(d["status"] == "OK", f"STOP: HOLD {e['model']} {d['status']}")
        if status == "INCOMPLETE" and d["chain"]:
            rec = d["chain"][-1]
            _req(pcg64_digest(rec["pcg64_state"]) == e["expected"][rec["step"] // ticket["K"]][
                "pcg64_state_sha256"], f"STOP: RNG STATE MISMATCH {e['model']}")
            _next_chunk(e, ticket, generator_from_state(rec["pcg64_state"]), rec["step"])
        env["models"].append({"model": e["model"], "resume_step": d["last_step"] or 0,
                              "status": status})
    print(f"PRECHECK OK {len(env['models'])}/{len(ticket['models'])}")
    return env
def run_wave(root, env) -> dict:
    root, ticket = Path(root), env["bundle"]["ticket"]
    stamp = env["utc"].replace("-", "").replace(":", "")
    rec = {k: v for k, v in env.items() if k not in ("bundle", "device_name", "cuda_capability")}
    (root / "sessions").mkdir(exist_ok=True)
    write_json_atomic(root / "sessions" / f"{stamp}-{env['session_id']}.start.json",
                      dict(rec, executed_cells=_cells() or env["executed_cells"]))
    out = {e["model"]: train_chunked(root, e, ticket, env, torch.device("cuda"))
           for e in ticket["models"]}
    print(f"WAVE DONE {sum(s in _TERMINAL for s in out.values())}/{len(out)}")
    return out
def finalise(root, env=None) -> dict:
    env = env if env is not None else (_CURRENT_ENV or None)
    if env is None:
        raise RuntimeError("no current environment: run cells 1-4 first")
    root, bundle, models, statuses = Path(root), env["bundle"], [], {}
    ticket, utc, sid = bundle["ticket"], utc_stamp(), env["session_id"]
    for e in ticket["models"]:
        status, d = _model_status(root, e, ticket)
        _req(d["status"] == "OK" and status in _TERMINAL,
             f"STOP: HOLD {e['model']} {status if d['status'] == 'OK' else d['status']}")
        ch, done, statuses[e["model"]] = d["chain"], status == "DONE", status
        keys = ("model", "arm", "seed", "run_key", "batch_stream", "data_stream", "data_sha256",
                "init_weights_sha256")
        models.append({k: e[k] for k in keys}
                      | {"model_master": ticket["model_master"],
                         "data_master": ticket["data_master"],
                         "chain": ch, "status": status, "marker": d["terminal"],
                         "final_file_sha256": ch[-1]["file_sha256"] if done else None,
                         "final_weights_sha256": ch[-1]["weights_sha256"] if done else None,
                         "devices": sorted({r["device_name"] for r in ch})})
    start = [p for p in _sessions(root, "start") if p.name.endswith(f"-{sid}.start.json")]
    _req(len(start) == 1, f"STOP: HOLD session start record {sid}")
    export = f"exports/{utc}/MANIFEST.json"
    write_json_atomic(root / "sessions" / f"{utc}-{sid}.final.json", {
        "schema": SESSION_SCHEMA, "kind": "final", "session_id": sid, "utc": utc_iso(),
        "start_record": {"file": start[0].name, "sha256": sha256_file(start[0])},
        "executed_cells": _cells() or list(env.get("executed_cells", [])),
        "models": [{"model": m, "status": s} for m, s in statuses.items()], "export": export})
    inv = {p.relative_to(root).as_posix(): sha256_file(p) for d in ("out", "sessions")
           for p in sorted((root / d).rglob("*")) if p.is_file() and not p.name.endswith(".part")}
    man = {"schema": MANIFEST_SCHEMA, "protocol_id": ticket["protocol_id"],
           "protocol_sha256": ticket["protocol_sha256"], "code_commit": bundle["code_commit"],
           "code_tar_sha256": sha256_file(root / "code.tar"),
           "bundle_sha256": bundle["bundle_sha256"],
           "bundle_id": bundle["bundle_id"], "ticket_sha256": bundle["ticket_sha256"],
           "models": models, "inventory": inv,
           "orphans": [o for p in _sessions(root, "start") for o in _rjson(p).get("orphans", [])]}
    (root / "exports" / utc).mkdir(parents=True, exist_ok=False)
    msha = write_json_atomic(root / export, man)
    print(f"WAVE DONE {sum(s in _TERMINAL for s in statuses.values())}/{len(statuses)}\n"
          f"MANIFEST_SHA256 = {msha}")
    return {"manifest": export, "manifest_sha256": msha, "statuses": statuses}
def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    opt = {k: a[a.index(k) + 1] for k in ("--max-chunks", "--device") if k in a}
    try:
        _req(len(a) >= 3 and a[0] == "train",
             "STOP: usage: train <root> <model> [--max-chunks N] [--device cpu]")
        tk = sorted(Path(a[1]).glob("ticket_*.json"))
        device = torch.device(opt.get("--device", "cpu"))
        ticket = _rjson(tk[0]) if len(tk) == 1 else {"models": []}
        entry = next((e for e in ticket["models"] if e["model"] == a[2]), None)
        _req(entry is not None, f"STOP: TICKET model {a[2]}")
        if device.type == "cpu":
            torch.set_num_threads(2)
        set_precision(device)
        env = {"session_id": uuid.uuid4().hex, "device_name": str(device), "cuda_capability": None}
        mc = int(opt["--max-chunks"]) if "--max-chunks" in opt else None
        print(status := train_chunked(a[1], entry, ticket, env, device, mc))
    except CloudStop as exc:
        print(str(exc))
        return 2
    return 3 if status == "INVALID:NONFINITE" else 0

if __name__ == "__main__":
    sys.exit(main())
