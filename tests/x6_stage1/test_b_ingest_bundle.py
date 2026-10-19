"""Author B (cloud): T-INGEST, T-ENV normalisation (X6S1-FROZEN-v1 §5.6-§5.8, §12 items 9-10;
API.md §5.6, §5.7, §6). A tiny CPU lineage (ticket steps 2, K 1) stands in for a Colab export
snapshot; its records claim a CUDA device so that the provenance gate can pass. Synthetic only.
"""
from __future__ import annotations

import copy
import dataclasses
import hashlib
import io
import json
import platform
import shutil
import subprocess
import sys
import tarfile
import time
from pathlib import Path

import numpy as np
import pytest
import torch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6_stage1"))

import x6s1_cloud as sc  # noqa: E402
import x6s1_data as sd  # noqa: E402
import x6s1_ingest as si  # noqa: E402
from topo_pilot.contracts import (  # noqa: E402
    ObservationSet, SeedTree, SequenceLayout, canonical_json)
from topo_pilot.dataset import PublicTokenDataset  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402
from topo_pilot.learner import TrainConfig  # noqa: E402
from topo_pilot.learner.trainer import _materialise  # noqa: E402

STEPS, K, N, SID, UTC, ISO = 2, 1, 256, "a" * 32, "20261019T000000Z", "2026-10-19T00:00:00Z"
RUN_KEY, M = ("x6s1", "smoke"), "SMOKE"
WH, PROV, DATA, CHAIN = ("FAIL_TECHNICAL/WEIGHTS_HASH", "FAIL_TECHNICAL/CLOUD_PROV",
                         "FAIL_TECHNICAL/DATA_ID", "FAIL_TECHNICAL/CHAIN")


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _fsha(p):
    return _sha(Path(p).read_bytes())


def _cj(obj):
    return canonical_json(obj).encode("utf-8")


def _put(root, rel, obj):
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(_cj(obj))
    return _fsha(p)


def _head():
    return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()


def _ckpt_edit(path):
    ck = torch.load(path, weights_only=False)
    key = sorted(ck["model"])[0]
    ck["model"][key] = ck["model"][key] + 1.0
    buf = io.BytesIO()
    torch.save(ck, buf)
    Path(path).write_bytes(buf.getvalue())


def build_snapshot(root):
    """§5.3 bundle files + §5.5 chain + §5.6 session records and manifest (API §5.1 layout)."""
    head, rng = _head(), np.random.default_rng(7)
    toks = rng.integers(0, 18, size=(N, 33), dtype=np.uint8)
    (root / "data").mkdir(parents=True)
    (root / "init").mkdir()
    np.save(root / "data" / "smoke.npy", toks, allow_pickle=False)
    init = sd.init_state(M)
    torch.save(init, root / "init" / "init_smoke.pt")
    with tarfile.open(root / "code.tar", "w", format=tarfile.PAX_FORMAT,
                      pax_headers={"comment": head}) as tf:
        info = tarfile.TarInfo("pyproject.toml")
        info.size = 6
        tf.addfile(info, io.BytesIO(b"x = 1\n"))
    cfg = TrainConfig(steps=STEPS, warmup=1, checkpoint_steps=(0, STEPS), device="cpu")
    exp = sc.expected_digests(sd.MODEL_MASTER, RUN_KEY, N, STEPS, K)
    files = ["code.tar", "data/smoke.npy", "init/init_smoke.pt", "ticket_C0.json"]
    iw = sc.weights_digest(init["model"])
    entry = {"model": M, "arm": "NA", "seed": "smoke", "run_key": list(RUN_KEY),
             "init_seed": sd.init_seed(M), "batch_stream": ["batch_order", *RUN_KEY],
             "data_stream": ["x6s1", "smoke", "NA"],
             "data_seed": SeedTree(sd.DATA_MASTER).seed("x6s1", "smoke", "NA"),
             "data_file": files[1], "data_sha256": _fsha(root / files[1]),
             "token_sha256": sd.token_digest(toks), "n_rows": N, "init_file": files[2],
             "init_file_sha256": _fsha(root / files[2]), "init_weights_sha256": iw, "expected": exp}
    ticket = {"schema": sc.TICKET_SCHEMA, "wave": "C0", "bundle_files": files,
              "protocol_id": sd.PROTOCOL_ID, "protocol_sha256": sd.PROTOCOL_SHA256,
              "code_commit": head, "data_master": sd.DATA_MASTER, "model_master": sd.MODEL_MASTER,
              "model_config": dataclasses.asdict(sd.MODEL_CFG),
              "train_config": dataclasses.asdict(cfg), "steps": STEPS, "K": K, "batch_size": 128,
              "smoke_resume": True, "models": [entry],
              "cell_templates_sha256": [_sha(t.encode("utf-8")) for t in sc.CELL_TEMPLATES]}
    tsha = _put(root, "ticket_C0.json", ticket)
    sums = "".join(f"{_fsha(root / f)}  {f}\n" for f in sorted(files)).encode("ascii")
    (root / "SHA256SUMS").write_bytes(sums)
    bsha = _sha(sums)
    mdir = root / "out" / M
    (mdir / "ckpt").mkdir(parents=True)
    (mdir / "rec").mkdir()
    ids = make_sequence_ids(process_code("x6s1", "NA", "smoke", 0), "dev", N)
    x, y = _materialise(PublicTokenDataset(ObservationSet(split="dev", V=18, sequence_id=ids,
                                                          tokens=toks), SequenceLayout()))
    gen = SeedTree(sd.MODEL_MASTER).generator("batch_order", *RUN_KEY)
    st = sc.fresh_state(init["model"], sd.MODEL_CFG, cfg, gen, torch.device("cpu"))
    prev, recs = sc.sha256_json(entry), []
    for step in range(0, STEPS + 1, K):
        chunk = (None,) * 5
        if step:
            idx = sc.draw_indices(st.gen, N, K)
            out = sc.train_chunk(st, x, y, idx)
            chunk = (sc.batch_digest(idx), out["loss_first"], out["loss_last"], True, 0.5)
        fsha = sc.write_checkpoint(mdir, step, sc.snapshot_bytes(st))
        rec = sc.make_record(M, step, fsha, sc.weights_digest(st.model.state_dict()), chunk[0],
                             sc.pcg64_state(st.gen), prev, SID, "Tesla T4", "7.5", *chunk[1:])
        sc.write_json_atomic(mdir / "rec" / f"{step:06d}.json", rec)
        prev = rec["record_sha256"]
        recs.append(rec)
    cells = list(sc.CELL_TEMPLATES)
    flags = {"deterministic": True, "tf32_matmul": False, "tf32_cudnn": False,
             "matmul_precision": "highest", "cublas_workspace_config": ":4096:8"}
    start = {"schema": sc.SESSION_SCHEMA, "kind": "start", "session_id": SID, "utc": ISO,
             "python": platform.python_version(), "numpy": np.__version__,
             "torch": torch.__version__, "cuda": "12.4", "cudnn": 90100,
             "gpu": {"name": "Tesla T4", "driver": "550.54.15", "memory": "15360 MiB"},
             "flags": flags, "code_commit": head, "code_tar_sha256": _fsha(root / "code.tar"),
             "ticket_sha256": tsha, "sha256sums_sha256": bsha, "env_compare": [],
             "models": [{"model": M, "resume_step": 0, "status": "DONE"}], "orphans": [],
             "stops": [], "executed_cells": cells[:5]}
    sname = f"sessions/{UTC}-{SID}.start.json"
    final = {"schema": sc.SESSION_SCHEMA, "kind": "final", "session_id": SID, "utc": ISO,
             "start_record": {"file": Path(sname).name, "sha256": _put(root, sname, start)},
             "executed_cells": cells, "models": [{"model": M, "status": "DONE"}],
             "export": f"exports/{UTC}/MANIFEST.json"}
    _put(root, f"sessions/{UTC}-{SID}.final.json", final)
    inv = {p.relative_to(root).as_posix(): _fsha(p) for d in ("out", "sessions")
           for p in sorted((root / d).rglob("*")) if p.is_file()}
    # API-AMBIGUITY: manifest "models" is read as a list of per-model objects (each with "model").
    man = {"schema": sc.MANIFEST_SCHEMA, "protocol_id": sd.PROTOCOL_ID,
           "protocol_sha256": sd.PROTOCOL_SHA256, "code_commit": head,
           "code_tar_sha256": _fsha(root / "code.tar"), "bundle_sha256": bsha,
           "bundle_id": f"C0-{bsha[:12]}", "ticket_sha256": tsha, "orphans": [], "inventory": inv,
           "models": [{"model": M, "arm": "NA", "seed": "smoke", "run_key": list(RUN_KEY),
                       "model_master": sd.MODEL_MASTER, "data_master": sd.DATA_MASTER,
                       "batch_stream": entry["batch_stream"], "data_stream": entry["data_stream"],
                       "data_sha256": entry["data_sha256"], "init_weights_sha256": iw,
                       "chain": recs, "final_file_sha256": recs[-1]["file_sha256"],
                       "final_weights_sha256": recs[-1]["weights_sha256"], "status": "DONE",
                       "devices": ["Tesla T4"], "marker": None}]}
    msha = _put(root, f"exports/{UTC}/MANIFEST.json", man)
    # API-AMBIGUITY: the schemas of `local` (gate_data_id, ingest) and `frozen` (gate_cloud_prov,
    # ingest) are not fixed by API.md; per-model local digests keyed by model and the frozen
    # release values are used.
    local = {M: {"data_sha256": entry["data_sha256"], "token_sha256": entry["token_sha256"],
                 "init_weights_sha256": iw, "expected": exp}}
    frozen = {"code_commit": head, "protocol_sha256": sd.PROTOCOL_SHA256, "bundle_sha256": bsha,
              "ticket_sha256": tsha, "ticket": ticket, "steps": STEPS, "K": K}
    return {"root": root, "manifest": man, "msha": msha, "local": local, "frozen": frozen,
            "start": start, "recs": recs, "head": head}


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    return build_snapshot(tmp_path_factory.mktemp("snap") / "C0-snapshot")


@pytest.fixture
def snap(base, tmp_path):
    root = tmp_path / "C0-snapshot"
    shutil.copytree(base["root"], root)
    return dict(copy.deepcopy({k: v for k, v in base.items() if k != "root"}), root=root)


def _remanifest(s):
    p = s["root"] / "exports" / UTC / "MANIFEST.json"
    p.write_bytes(_cj(s["manifest"]))
    return _fsha(p)


# ---------------------------------------------------------------- T-INGEST
def test_four_gates_pass_on_consistent_snapshot(snap):
    r, m = snap["root"], snap["manifest"]
    outs = [si.gate_weights_hash(r, snap["msha"].upper(), M),
            si.gate_cloud_prov(r, m, M, snap["frozen"]), si.gate_data_id(r, m, M, snap["local"]),
            si.gate_train_complete(m, M, STEPS, K)]
    assert [o["status"] for o in outs] == ["PASS"] * 4
    assert all(set(o) >= {"gate", "model", "status", "detail"} and o["model"] == M for o in outs)


@pytest.mark.parametrize("case", ["byte", "relayed", "missing", "extra"])
def test_weights_hash_transfer_failures(snap, case):
    r, msha = snap["root"], snap["msha"]
    if case == "byte":
        p = r / "out" / M / "ckpt" / "000001.pt"
        b = bytearray(p.read_bytes())
        b[len(b) // 2] ^= 1
        p.write_bytes(bytes(b))
    elif case == "relayed":
        msha = "0" * 64
    elif case == "missing":
        (r / "out" / M / "rec" / "000001.json").unlink()
    else:
        (r / "sessions" / f"{UTC}-{'b' * 32}.start.json").write_bytes(b"{}")
    assert si.gate_weights_hash(r, msha, M)["status"] == WH
    assert si.gate_weights_hash(r, msha, M, redownload_ok=True)["status"] == "TRANSFER_RETRY"


def test_weights_hash_honours_explicit_exclusions(snap):
    r = snap["root"]
    (r / "out" / M / "ckpt" / "000003.pt.part").write_bytes(b"partial")
    (r / "out" / M / "rec" / "000003.json.part").write_bytes(b"{")
    old = r / "exports" / "20261018T000000Z" / "MANIFEST.json"
    old.parent.mkdir()
    old.write_bytes(b"{}")  # an earlier export snapshot
    assert si.gate_weights_hash(r, snap["msha"], M)["status"] == "PASS"


def test_weights_digest_mismatch_fails_even_with_redownload(snap):
    r, m = snap["root"], snap["manifest"]
    p = r / "out" / M / "ckpt" / f"{STEPS:06d}.pt"
    _ckpt_edit(p)  # file and inventory consistent, weights digest differs from the record
    rec = m["models"][0]["chain"][-1]
    rec["file_sha256"] = _fsha(p)
    rec["record_sha256"] = sc.record_sha(rec)
    (r / "out" / M / "rec" / f"{STEPS:06d}.json").write_bytes(_cj(rec))
    m["models"][0]["final_file_sha256"] = rec["file_sha256"]
    for rel in (f"out/{M}/ckpt/{STEPS:06d}.pt", f"out/{M}/rec/{STEPS:06d}.json"):
        m["inventory"][rel] = _fsha(r / rel)
    msha = _remanifest(snap)
    assert si.gate_weights_hash(r, msha, M, redownload_ok=True)["status"] == WH


@pytest.mark.parametrize("case", ["missing_field", "commit", "protocol", "bundle", "edited_cell",
                                  "extra_code", "no_cuda", "tf32", "nondeterministic",
                                  "session_field"])
def test_cloud_prov_failures(snap, case):
    r, m, fr = snap["root"], snap["manifest"], snap["frozen"]
    start, sname = snap["start"], f"sessions/{UTC}-{SID}.start.json"
    edits = {"edited_cell": lambda: start["executed_cells"].__setitem__(
                 3, start["executed_cells"][3] + "\nprint('x')"),
             "extra_code": lambda: start["executed_cells"].insert(4, "import os"),
             "tf32": lambda: start["flags"].__setitem__("tf32_matmul", True),
             "nondeterministic": lambda: start["flags"].__setitem__("deterministic", False),
             "session_field": lambda: start.pop("cudnn")}
    if case in edits:
        edits[case]()
        m["inventory"][sname] = _put(r, sname, start)
    elif case == "missing_field":
        del m["code_tar_sha256"]
    elif case == "commit":
        m["code_commit"] = "f" * 40
    elif case == "protocol":
        m["protocol_sha256"] = "0" * 64
    elif case == "bundle":
        fr = dict(fr, bundle_sha256="1" * 64)
    else:
        m["models"][0]["chain"][1].update(device_name="cpu", cuda_capability=None)
    assert si.gate_cloud_prov(r, m, M, fr)["status"] == PROV


# check_execution unit tests (execution records): test_b_chain_ops.py
@pytest.mark.parametrize("case", ["init", "batch", "pcg", "data", "tokens"])
def test_data_id_failures(snap, case):
    loc = snap["local"][M]
    key = {"init": "init_weights_sha256", "data": "data_sha256", "tokens": "token_sha256"}
    if case in key:
        loc[key[case]] = "0" * 64
    elif case == "batch":
        loc["expected"][1]["batch_sha256"] = "1" * 64
    else:
        loc["expected"][2]["pcg64_state_sha256"] = "2" * 64
    assert si.gate_data_id(snap["root"], snap["manifest"], M, snap["local"])["status"] == DATA


def _relink(chain, prev="e" * 64):
    out = []
    for r in chain:
        r = dict(r, prev_record_sha256=prev)
        r["record_sha256"] = sc.record_sha(r)
        prev = r["record_sha256"]
        out.append(r)
    return out


@pytest.mark.parametrize("case,status", [
    ("full", "PASS"), ("prefix", "HOLD:CLOUD_INCOMPLETE"), ("gap", CHAIN), ("duplicate", CHAIN),
    ("badlink", CHAIN), ("order", CHAIN), ("marker", "INVALID:NONFINITE"),
    ("bad_marker", "HOLD:MARKER")])
def test_train_complete_statuses(case, status):
    ch = _relink([sc.make_record(M, s, "f" * 64, "1" * 64, None if s == 0 else "2" * 64, {"s": s},
                                 "", SID, "Tesla T4", "7.5", None, None, None, None)
                  for s in (0, 2, 4, 6)])
    st, marker = "DONE", None
    if case == "prefix":
        ch, st = ch[:3], "INCOMPLETE"
    elif case in ("gap", "duplicate", "order"):
        ch = _relink({"gap": [ch[0], ch[1], ch[3]], "duplicate": ch[:3] + [ch[2]] + ch[3:],
                      "order": [ch[0], ch[2], ch[1], ch[3]]}[case])
    elif case == "badlink":
        ch[2] = dict(ch[2], prev_record_sha256="9" * 64)
        ch[2]["record_sha256"] = sc.record_sha(ch[2])
    elif case in ("marker", "bad_marker"):
        ch, st = ch[:2], "INVALID:NONFINITE"
        marker = {"schema": sc.MARKER_SCHEMA, "model": M, "step": 3, "chunk": 2, "session_id": SID,
                  "loss_bits": "7fc00000", "prev_record_sha256": ch[-1]["record_sha256"],
                  "utc": ISO}
        marker["marker_sha256"] = sc.sha256_json(marker)
        if case == "bad_marker":
            marker["step"] = 4
    man = {"models": [{"model": M, "chain": ch, "status": st, "marker": marker,
                       "final_file_sha256": ch[-1]["file_sha256"],
                       "final_weights_sha256": ch[-1]["weights_sha256"] if st == "DONE" else None}]}
    assert si.gate_train_complete(man, M, 6, 2)["status"] == status


def test_admission_lock_before_import_blocks_retrain_and_restoration_rules(snap, tmp_path,
                                                                          monkeypatch):
    store, seen, real = tmp_path / "store", [], si.import_model
    store.mkdir()

    def spy(*args, **kwargs):
        seen.append(si.admitted(store, M))
        return real(*args, **kwargs)
    monkeypatch.setattr(si, "import_model", spy)
    res = si.ingest(snap["root"], snap["msha"], "C0", store, snap["local"], snap["frozen"])
    assert res[M]["admitted"] is True and [g["status"] for g in res[M]["gates"]] == ["PASS"] * 4
    assert seen and seen[0] is not None  # lock written before import and any evaluation
    lock = si.admitted(store, M)
    assert lock["final_weights_sha256"] == snap["recs"][-1]["weights_sha256"]
    assert lock["final_file_sha256"] == snap["recs"][-1]["file_sha256"]
    assert lock["manifest_sha256"] == snap["msha"]
    assert lock["chain_record_sha256"] == [r["record_sha256"] for r in snap["recs"]]
    assert (store / "cloud" / "C0" / M / "STORE_MANIFEST.json").is_file()
    assert si.retrain_eligible(store, M, []) is False
    with pytest.raises(FileExistsError):
        si.write_admission_lock(store, M, lock)
    assert si.verify_admitted(store, M)["status"] == "PASS"
    final = store / "cloud" / "C0" / M / "ckpt" / f"{STEPS:06d}.pt"
    good = final.read_bytes()
    _ckpt_edit(final)
    assert si.verify_admitted(store, M)["status"] == "INVALID"  # different weights refused
    final.write_bytes(good)  # byte-identical restoration is transport recovery (RC9)
    assert si.verify_admitted(store, M)["status"] == "PASS"


def test_refinalisation_creates_new_snapshot_and_preserves_earlier(snap):
    r = snap["root"]
    bundle = sc.verify_bundle(r, snap["frozen"]["bundle_sha256"])
    assert bundle["bundle_id"] == f"C0-{snap['frozen']['bundle_sha256'][:12]}"
    assert bundle["code_commit"] == snap["head"]
    env = dict(snap["start"], bundle=bundle)  # API-AMBIGUITY: env built by hand (no CPU env API)
    m1 = sc.finalise(r, env)
    p1 = r / m1["manifest"]
    b1, ours = p1.read_bytes(), (r / "exports" / UTC / "MANIFEST.json").read_bytes()
    assert _sha(b1) == m1["manifest_sha256"]
    time.sleep(1.1)
    m2 = sc.finalise(r, env)
    assert m2["manifest"] != m1["manifest"] and p1.read_bytes() == b1
    assert (r / "exports" / UTC / "MANIFEST.json").read_bytes() == ours
    # API-AMBIGUITY: refinalised(snapshots) read as a list of snapshot directories, earliest first.
    assert si.refinalised([p1.parent, (r / m2["manifest"]).parent]) is True
    inv = json.loads((r / m2["manifest"]).read_text(encoding="utf-8"))["inventory"]
    assert not [k for k in inv if k.endswith((".part", "MANIFEST.json"))]
    assert si.gate_weights_hash(r, m2["manifest_sha256"], M)["status"] == "PASS"


# ---------------------------------------------------------------- T-ENV (executed-cell hashing)
HEX, T2 = "0123456789abcdef" * 4, sc.CELL_TEMPLATES[1]


@pytest.mark.parametrize("raw,want", [
    ("a = 1  \r\nb = 2\t\n\n\n", "a = 1\nb = 2"), (T2.replace(sc.HASH_PLACEHOLDER, HEX), T2),
    (T2.replace(sc.HASH_PLACEHOLDER, HEX.upper()).replace("\n", "\r\n") + "\n", T2),
    ('BUNDLE_SHA256 = "' + "g" * 64 + '"', 'BUNDLE_SHA256 = "' + "g" * 64 + '"'),
    ('BUNDLE_SHA256 = "' + HEX[:63] + '"', 'BUNDLE_SHA256 = "' + HEX[:63] + '"')])
def test_executed_cell_normalisation(raw, want):
    assert sc.normalise_source(raw) == want
    assert [sc.normalise_source(t) for t in sc.CELL_TEMPLATES] == list(sc.CELL_TEMPLATES)
    assert sc.executed_sources() == []  # outside IPython
