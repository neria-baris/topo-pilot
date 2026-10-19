"""X6S1 ingest (local): CLOUD-PREP (allowed-class guard, code.tar, tickets, bundles), the four
integrity gates with execution-record validation, the admission lock, store import, E3.0
verification, retrain eligibility, LOSS-ECHO and the learning-curve record (X6S1-FROZEN-v1 §4.5,
§5.3, §5.6-§5.8, §12 items 9-10; API.md §6, §13 item 25). Import performs no I/O."""
# fmt: off

from __future__ import annotations

import copy
import dataclasses
import io
import json
import os
import re
import shutil
import subprocess
import uuid
from pathlib import Path

import numpy as np
import torch
import x6s1_cloud as sc
import x6s1_data as sd
import x6s1_eval as se

from topo_pilot.contracts import canonical_json
from topo_pilot.learner import ModelConfig
from topo_pilot.learner.trainer import lm_loss

WEIGHTS_HASH, CLOUD_PROV = "FAIL_TECHNICAL/WEIGHTS_HASH", "FAIL_TECHNICAL/CLOUD_PROV"
DATA_ID, CHAIN = "FAIL_TECHNICAL/DATA_ID", "FAIL_TECHNICAL/CHAIN"
ALLOWED = ("code.tar", "X6S1_colab.ipynb", "SHA256SUMS", "ticket_<wave>.json",
           "data/train_<arm>_s<s>.npy", "data/smoke.npy", "init/init_s<s>.pt", "init/init_smoke.pt")
_SUB = {"<wave>": "[A-Za-z0-9]+", "<arm>": "(NA|AB|ZC)", "<s>": "[1-4]"}
_ALLOWED_RE = tuple(re.compile(re.sub("|".join(_SUB), lambda m: _SUB[m.group()], p.replace(
    ".", r"\."))) for p in ALLOWED)
_FORBID = ("val", "test", "gate", "prefix", "dev", "sealed", "registry", "state", "latent")
_NB, _SUMS = "X6S1_colab.ipynb", "SHA256SUMS"
_LOCK_KEYS = ("model", "bundle_id", "manifest_sha256", "final_file_sha256",
              "final_weights_sha256", "chain_record_sha256", "utc")
_CHUNK_ONLY = ("batch_sha256", "train_loss_first", "train_loss_last", "loss_finite", "wall_s")
_N = type(None)
_T = {"s": str, "i": int, "d": dict, "l": list, "S": (str, _N), "D": (dict, _N), "x": (int, str),
      "F": (float, _N), "B": (bool, _N), "W": (float, int, _N)}
def _spec(text) -> dict: return {f[:-2]: _T[f[-1]] for f in text.split()}  # "name:code" fields
_MAN_F = _spec("schema:s protocol_id:s protocol_sha256:s code_commit:s code_tar_sha256:s "
               "bundle_sha256:s bundle_id:s ticket_sha256:s models:l orphans:l inventory:d")
_ENTRY_F = _spec("model:s arm:s seed:x run_key:l model_master:i data_master:i batch_stream:l "
                 "data_stream:l data_sha256:s init_weights_sha256:s chain:l final_file_sha256:S "
                 "final_weights_sha256:S status:s devices:l marker:D")
_REC_F = _spec("schema:s model:s step:i file:s file_sha256:s weights_sha256:s batch_sha256:S "
               "pcg64_state:d pcg64_state_sha256:s prev_record_sha256:s record_sha256:s "
               "session_id:s device_name:s cuda_capability:s train_loss_first:F "
               "train_loss_last:F loss_finite:B wall_s:W utc:s")
_START_F = _spec("schema:s kind:s session_id:s utc:s python:s numpy:s torch:s cuda:s cudnn:i "
                 "gpu:d flags:d code_commit:s code_tar_sha256:s ticket_sha256:s "
                 "sha256sums_sha256:s env_compare:l models:l orphans:l stops:l executed_cells:l")
_FINAL_F = _spec("schema:s kind:s session_id:s start_record:d utc:s executed_cells:l models:l "
                 "export:s")
_FLAGS = {"deterministic": True, "tf32_matmul": False, "tf32_cudnn": False,
          "matmul_precision": "highest"}


def _posix(rel) -> str: return str(rel).replace("\\", "/")
def _lo(x): return x.strip().lower() if isinstance(x, str) else x
def _cj(obj) -> bytes: return canonical_json(obj).encode("utf-8")
def _gate(g, model, status, detail): return dict(gate=g, model=model, status=status, detail=detail)
def _xwrite(path, data: bytes) -> str:  # exclusive create, fsync, re-read and verify
    with open(path, "xb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    if sc.sha256_file(path) != sc.sha256_bytes(data):
        raise OSError(f"re-read of {path} does not verify")
    return sc.sha256_bytes(data)
def _typed(obj, spec, where) -> list:
    if not isinstance(obj, dict):
        return [f"{where}: not an object"]
    return [f"{where}.{k}" for k, t in spec.items() if k not in obj or not isinstance(obj[k], t)]
def _entry(manifest, model):
    ms = manifest.get("models") if isinstance(manifest, dict) else None
    return next((e for e in ms or [] if isinstance(e, dict) and e.get("model") == model), None)
def _weights(path) -> str:
    return sc.weights_digest(torch.load(path, map_location="cpu", weights_only=True)["model"])

# ---- CLOUD-PREP (§5.3; gate 9) ----
def _files(model) -> tuple:  # (data file, init file) of a model inside a bundle
    if model == "SMOKE":
        return "data/smoke.npy", "init/init_smoke.pt"
    s = sd.parse_model(model)[1]
    return f"data/train_{model.replace('-', '_')}.npy", f"init/init_s{s}.pt"
def _names(wave, models) -> set:
    return {"code.tar", _NB, _SUMS, f"ticket_{wave}.json"} | {f for m in models for f in _files(m)}
def forbidden(relpath) -> bool:
    rel = _posix(relpath)
    return any(w in c.lower() for c in rel.split("/") for w in _FORBID) or not any(
        r.fullmatch(rel) for r in _ALLOWED_RE)
def allowed_class(relpath, wave, models) -> bool:
    return not forbidden(relpath) and _posix(relpath) in _names(wave, models)
def code_tar(worktree, head, out_path) -> str:
    data = subprocess.run(["git", "-C", str(worktree), "archive", "--format=tar", str(head), "--",
                           "src", "tools/x6_stage1", "pyproject.toml"],
                          capture_output=True, check=True).stdout
    return _xwrite(out_path, data)
def _tsha() -> list: return [sc.sha256_bytes(t.encode("utf-8")) for t in sc.CELL_TEMPLATES]
def make_ticket(wave, head, pools, inits) -> dict:
    (cfg, k), models = (sd.SMOKE_CFG, sd.K_SMOKE) if wave == "C0" else (sd.TRAIN_CFG, sd.K), []
    for m in sd.WAVES[wave]:
        (arm, seed), p, i, (df, inf) = sd.parse_model(m), pools[m], inits[m], _files(m)
        rk, n = list(sd.run_key(m)), int(p["n_rows"])
        spec = sd.pool_spec("smoke") if m == "SMOKE" else sd.pool_spec("train", arm, seed)
        models.append({
            "model": m, "arm": arm, "seed": seed, "run_key": rk, "init_seed": sd.init_seed(m),
            "batch_stream": ["batch_order", *rk], "data_stream": list(spec["stream"]),
            "data_seed": int(p["data_seed"]), "data_file": df, "data_sha256": _lo(p["file_sha256"]),
            "token_sha256": _lo(p["token_sha256"]), "n_rows": n, "init_file": inf,
            "init_file_sha256": _lo(i["file_sha256"]),
            "init_weights_sha256": _lo(i["weights_sha256"]),
            "expected": sc.expected_digests(sd.MODEL_MASTER, rk, n, cfg.steps, k, cfg.batch_size)})
    return {"schema": sc.TICKET_SCHEMA, "wave": wave,
            "bundle_files": sorted(_names(wave, sd.WAVES[wave]) - {_NB, _SUMS}),
            "protocol_id": sd.PROTOCOL_ID, "protocol_sha256": sd.PROTOCOL_SHA256,
            "code_commit": _lo(head), "data_master": sd.DATA_MASTER,
            "model_master": sd.MODEL_MASTER,
            "model_config": json.loads(_cj(dataclasses.asdict(sd.MODEL_CFG))),
            "train_config": json.loads(_cj(dataclasses.asdict(cfg))), "steps": cfg.steps, "K": k,
            "batch_size": cfg.batch_size, "smoke_resume": wave == "C0",
            "cell_templates_sha256": _tsha(), "models": models}
def _sums(d: Path, files) -> bytes:
    return "".join(f"{sc.sha256_file(d / f)}  {f}\n" for f in sorted(files)).encode("ascii")
def build_bundle(wave, out_root, head, worktree, pools, inits, notebook) -> dict:
    (out_root := Path(out_root)).mkdir(parents=True, exist_ok=True)
    (stage := out_root / f".staging-{uuid.uuid4().hex}").mkdir()
    try:
        code_tar(worktree, head, stage / "code.tar")
        for m in sd.WAVES[wave]:
            for src, rel in zip((pools[m], inits[m]), _files(m)):
                (dst := stage / rel).parent.mkdir(exist_ok=True)
                if not dst.exists():  # an init shared by two models of one seed is copied once
                    shutil.copyfile(src["path"], dst)
                if sc.sha256_file(dst) != _lo(src["file_sha256"]):
                    raise ValueError(f"{m}: {rel} does not match its file_sha256")
            toks = np.load(stage / _files(m)[0], allow_pickle=False)
            if (sd.token_digest(toks), len(toks), _weights(stage / _files(m)[1])) != (
                    _lo(pools[m]["token_sha256"]), pools[m]["n_rows"],
                    _lo(inits[m]["weights_sha256"])):
                raise ValueError(f"{m}: token digest, row count or init weights digest mismatch")
        ticket = make_ticket(wave, head, pools, inits)
        _xwrite(stage / f"ticket_{wave}.json", _cj(ticket))
        bsha = _xwrite(stage / _SUMS, _sums(stage, ticket["bundle_files"]))
        shutil.copyfile(notebook, stage / _NB)
        target = out_root / f"{wave}-{bsha[:12]}"
        if target.exists():
            raise FileExistsError(str(target))
        os.rename(stage, target)  # one immutable directory per bundle id
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    chk = check_bundle(target, wave)
    if chk["status"] != "PASS":
        raise RuntimeError(f"CLOUD-PREP: bundle {target.name} fails check_bundle: {chk}")
    return {"bundle_dir": str(target), "bundle_id": target.name, "bundle_sha256": bsha,
            "files": sorted([*ticket["bundle_files"], _SUMS, _NB])}
def check_bundle(bundle_dir, wave) -> dict:
    d, models, bsha = Path(bundle_dir), sd.WAVES[wave], None
    files = sorted(p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file())
    refused = [f for f in files if not allowed_class(f, wave, models)]
    listed = sorted(set(files) - {_SUMS, _NB})
    detail = [f"missing {f}" for f in sorted(_names(wave, models) - set(files))]
    try:
        raw = (d / _SUMS).read_bytes()
        bsha = sc.sha256_bytes(raw)
        detail += ["SHA256SUMS coverage, order or hashes"] * (raw != _sums(d, listed))
        t = json.loads((d / f"ticket_{wave}.json").read_bytes())
        detail += ["ticket"] * ((t.get("schema"), t.get("wave"), t.get("bundle_files"),
                                 [e["model"] for e in t["models"]], t.get("cell_templates_sha256"))
                                != (sc.TICKET_SCHEMA, wave, listed, list(models), _tsha()))
        detail += ["directory name"] * (d.name != f"{wave}-{bsha[:12]}")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        detail.append(f"unreadable: {exc!r}")
    return {"status": "INVALID" if refused or detail else "PASS", "refused": refused,
            "bundle_sha256": bsha, "detail": detail}

# ---- integrity gates (§5.8; gates 12, 14, 18) ----
def find_manifest(snapshot, manifest_sha256) -> tuple:
    """(path, manifest) of the export whose MANIFEST.json bytes have the relayed sha256."""
    for p in sorted((Path(snapshot) / "exports").glob("*/MANIFEST.json")):
        if sc.sha256_bytes(raw := p.read_bytes()) == _lo(manifest_sha256):
            return p, json.loads(raw)
    return None, None
def transfer_check(snapshot, manifest_sha256) -> tuple:
    """WEIGHTS-HASH (a)-(b) for the whole snapshot: (manifest or None, problems)."""
    root, probs = Path(snapshot), []
    try:
        _, man = find_manifest(root, manifest_sha256)
        if man is None:
            return None, ["(a) no exports/<utc>/MANIFEST.json has the relayed MANIFEST_SHA256"]
        inv = man["inventory"]
        have = {p.relative_to(root).as_posix() for d in ("out", "sessions") if (root / d).is_dir()
                for p in (root / d).rglob("*") if p.is_file() and not p.name.endswith(".part")}
        probs += [f"(b) not covered: {r}" for r in sorted(set(inv) ^ have)]
        probs += [f"(b) sha256: {r}" for r in sorted(set(inv) & have)
                  if sc.sha256_file(root / r) != inv[r]]
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return None, [f"(a)-(b) unreadable: {exc!r}"]
    return man, probs
def gate_weights_hash(snapshot, manifest_sha256, model, redownload_ok=False, transfer=None):
    g = "WEIGHTS-HASH"
    man, probs = transfer if transfer is not None else transfer_check(snapshot, manifest_sha256)
    if probs:
        return _gate(g, model, "TRANSFER_RETRY" if redownload_ok else WEIGHTS_HASH, probs)
    probs = []
    try:
        ch, md = (e := _entry(man, model))["chain"], Path(snapshot) / "out" / model
        ck = {f"out/{model}/{r['file']}": r["file_sha256"] for r in ch}
        inv = {k: v for k, v in man["inventory"].items() if k.startswith(f"out/{model}/ckpt/")}
        probs += ["(b) inventory checkpoints differ from the chain file_sha256s"] * (inv != ck)
        probs += [f"(c) weights digest step {r['step']}" for r in ch
                  if _weights(md / r["file"]) != r["weights_sha256"]]
        fin = (e["final_file_sha256"], e["final_weights_sha256"])
        if fin != (None, None) or e["status"] == "DONE":
            last = (ch[-1]["file_sha256"], ch[-1]["weights_sha256"])
            probs += ["(c) final digests differ from the last record"] * (fin != last)
    except Exception as exc:  # an absent model, a malformed entry or an unloadable checkpoint
        probs.append(f"(c) {exc!r}")
    return _gate(g, model, WEIGHTS_HASH if probs else "PASS", probs)
def _seq(cells, templates):
    ok = isinstance(cells, list) and all(isinstance(c, str) for c in cells)
    norm = [sc.normalise_source(c) for c in cells] if ok else [None]
    return [templates.index(c) + 1 for c in norm] if all(c in templates for c in norm) else None
def check_execution(records, templates=sc.CELL_TEMPLATES) -> dict:
    tpl, bad = tuple(sc.normalise_source(t) for t in templates), []
    seqs = [_seq(r.get("executed_cells"), tpl) if isinstance(r, dict) else None for r in records]
    starts = {(r.get("session_id"), sc.sha256_json(r)): s for r, s in zip(records, seqs)
              if isinstance(r, dict) and r.get("kind") == "start"}
    for i, (r, s) in enumerate(zip(records, seqs)):
        kind = r.get("kind") if isinstance(r, dict) else None
        if not s or r.get("schema") != sc.SESSION_SCHEMA or kind not in ("start", "final"):
            bad.append(f"record {i}: schema, kind or a non-template source")
        elif s[0] != 1 or any(b > a + 1 for a, b in zip(s, s[1:])):
            bad.append(f"record {i}: cell order {s}")
        elif kind == "start" and s[-1] != 5:
            bad.append(f"record {i}: a start record must end with its cell-5 execution")
        elif kind == "final":
            ref, sid = r.get("start_record"), r.get("session_id")
            ref = ref if isinstance(ref, dict) else {}
            st = starts.get((sid, _lo(ref.get("sha256"))))
            if s[-1] != 6 or st is None or s[:len(st)] != st or \
                    not str(ref.get("file", "")).endswith(f"-{sid}.start.json"):
                bad.append(f"record {i}: final record without its start record or cell 6")
    return {"status": "FAIL" if bad else "PASS", "detail": bad}
def _diff(rows) -> list: return [n for n, a, b in rows if a != b]
def _prov(root: Path, man, model, frozen) -> list:
    tk, h = json.loads(_cj(frozen["ticket"])), _lo(frozen["code_commit"])  # tuples as lists
    bsha, tsha = _lo(frozen["bundle_sha256"]), _lo(frozen["ticket_sha256"])
    probs = _typed(man, _MAN_F, "manifest")
    e, raw = _entry(man, model), (root / f"ticket_{tk['wave']}.json").read_bytes()
    te, tar = next(x for x in tk["models"] if x["model"] == model), root / "code.tar"
    probs += _diff((
        ("schema", man["schema"], sc.MANIFEST_SCHEMA),
        ("protocol_id", man["protocol_id"], sd.PROTOCOL_ID),
        ("protocol_sha256", man["protocol_sha256"], _lo(frozen["protocol_sha256"])),
        ("code_commit", man["code_commit"], h), ("code.tar commit", sc._tar_commit(tar), h),
        ("code_tar_sha256", man["code_tar_sha256"], sc.sha256_file(tar)),
        ("bundle_sha256", man["bundle_sha256"], bsha),
        ("SHA256SUMS", sc.sha256_file(root / _SUMS), bsha),
        ("bundle_id", man["bundle_id"], f"{tk['wave']}-{bsha[:12]}"),
        ("ticket_sha256", man["ticket_sha256"], tsha), ("ticket file", sc.sha256_bytes(raw), tsha),
        ("ticket", json.loads(raw), tk), ("steps", tk["steps"], frozen["steps"]),
        ("K", tk["K"], frozen["K"])))
    probs += _typed(e, _ENTRY_F, model) + [k for k in (
        "arm", "seed", "run_key", "batch_stream", "data_stream", "data_sha256",
        "init_weights_sha256") if e[k] != te[k]]
    probs += [k for k in ("model_master", "data_master") if e[k] != tk[k]]
    ch = e["chain"]
    probs += ["devices"] * (e["devices"] != sorted({r.get("device_name") for r in ch}))
    probs += ["step-0 link to the ticket entry"] * (
        not ch or ch[0].get("prev_record_sha256") != sc.sha256_json(te))
    for r in ch:
        st, cuda = r.get("step"), re.fullmatch(r"\d+\.\d+", str(r.get("cuda_capability")))
        probs += _typed(r, _REC_F, f"record {st}") + [f"record {st}: schema, model or device"] * (
            (r.get("schema"), r.get("model")) != (sc.RECORD_SCHEMA, model) or not cuda
            or r.get("device_name") in (None, "cpu"))
        probs += [f"record {st}: chunk-only fields"] * any(
            (r.get(k) is None) != (st == 0) for k in _CHUNK_ONLY)
    recs, starts = [], set()
    for p in sorted((root / "sessions").glob("*.json")):
        s = json.loads(p.read_bytes())
        kind, sid = (s.get("kind"), s.get("session_id")) if isinstance(s, dict) else (None, None)
        probs += _typed(s, _START_F if kind == "start" else _FINAL_F, p.name)
        probs += [f"{p.name}: file name"] * (not p.name.endswith(f"-{sid}.{kind}.json"))
        if kind == "start":
            starts.add(sid)
            want = {"code_commit": h, "code_tar_sha256": man["code_tar_sha256"],
                    "ticket_sha256": tsha, "sha256sums_sha256": bsha}
            vers = [s[k] for k in ("python", "numpy", "torch", "cuda", "cudnn")] + [
                s["gpu"].get(k) for k in ("name", "driver", "memory")]
            probs += [f"{p.name}: {k}" for k, v in want.items() if s[k] != v] + [
                f"{p.name}: flag {k}" for k, v in _FLAGS.items() if s["flags"].get(k) != v]
            probs += [f"{p.name}: versions"] * (not all(v not in ("", None) for v in vers))
        recs.append(s)
    probs += check_execution(recs)["detail"]
    probs += [f"session {s} has no start record" for s in sorted(
        {str(r.get("session_id")) for r in ch} - starts)]
    return probs
def gate_cloud_prov(snapshot, manifest, model, frozen) -> dict:
    try:
        probs = _prov(Path(snapshot), manifest, model, frozen)
    except Exception as exc:  # a missing or badly typed field, or an unreadable file
        probs = [f"unreadable or malformed: {exc!r}"]
    return _gate("CLOUD-PROV", model, CLOUD_PROV if probs else "PASS", probs)
def gate_data_id(snapshot, manifest, model, local) -> dict:
    try:
        root, e, loc, probs = Path(snapshot), _entry(manifest, model), local[model], []
        tk = json.loads((root / f"ticket_{manifest['bundle_id'].split('-')[0]}.json").read_bytes())
        te = next(x for x in tk["models"] if x["model"] == model)
        data, exp = root / te["data_file"], {x["step"]: x for x in loc["expected"]}
        toks = np.load(data, allow_pickle=False)
        probs += [n for n, ok in (
            ("data file sha256", sc.sha256_file(data) == _lo(loc["data_sha256"])
             == e["data_sha256"] == te["data_sha256"]),
            ("raw token digest", sd.token_digest(toks) == _lo(loc["token_sha256"])
             == te["token_sha256"]),
            ("step-0 weights digest", e["chain"][0]["weights_sha256"]
             == _lo(loc["init_weights_sha256"]) == e["init_weights_sha256"])) if not ok]
        cfg = ModelConfig(**tk["model_config"])
        for r in e["chain"]:
            x = exp.get(r["step"], {})
            probs += [f"step {r['step']}: batch or PCG64 digest"] * (
                (r["batch_sha256"], r["pcg64_state_sha256"], sc.pcg64_digest(r["pcg64_state"]))
                != (x.get("batch_sha256"), x.get("pcg64_state_sha256"), r["pcg64_state_sha256"]))
            ck = torch.load(root / "out" / model / r["file"], map_location="cpu", weights_only=True)
            probs += [f"step {r['step']}: {n}" for n in sc.check_internal(ck, r, x, cfg)]
    except Exception as exc:
        probs = [f"unreadable or malformed: {exc!r}"]
    return _gate("DATA-ID", model, DATA_ID if probs else "PASS", probs)
def _linked(ch, model) -> bool:
    return all(isinstance(r, dict) and r.get("model") == model and
               r.get("record_sha256") == sc.record_sha(r) for r in ch) and all(
        b.get("prev_record_sha256") == a["record_sha256"] for a, b in zip(ch, ch[1:]))
def gate_train_complete(manifest, model, steps, k) -> dict:
    g, e, k = "TRAIN-COMPLETE", _entry(manifest, model) or {}, int(k)
    ch, st, mk = e.get("chain") or [], e.get("status"), e.get("marker")
    got = [r.get("step") if isinstance(r, dict) else None for r in ch]
    want = list(range(0, int(steps) + 1, k))
    prefix = bool(ch) and got == want[:len(got)] and _linked(ch, model)
    if mk is not None or st == "INVALID:NONFINITE":  # terminal markers first (§5.4 step 0)
        body = {x: v for x, v in mk.items() if x != "marker_sha256"} if isinstance(mk, dict) else {}
        ok = bool(body) and prefix and st == "INVALID:NONFINITE" and (
            mk.get("marker_sha256"), body.get("model"), body.get("prev_record_sha256")) == (
            sc.sha256_json(body), model, ch[-1]["record_sha256"]) and isinstance(
            body.get("step"), int) and got[-1] < body["step"] <= got[-1] + k
        return _gate(g, model, "INVALID:NONFINITE" if ok else "HOLD:MARKER",
                     "valid terminal marker" if ok else "unreadable or ambiguous terminal marker")
    if not prefix:
        return _gate(g, model, CHAIN, f"steps {got}: gap, duplicate, bad link or out of order")
    if got != want:
        return _gate(g, model, "HOLD:CLOUD_INCOMPLETE" if st == "INCOMPLETE" else CHAIN,
                     f"valid prefix to step {got[-1]} of {steps}; status {st}")
    fin = (e.get("final_file_sha256"), e.get("final_weights_sha256"))
    ok = st == "DONE" and fin == (ch[-1]["file_sha256"], ch[-1]["weights_sha256"])
    return _gate(g, model, "PASS" if ok else CHAIN, "complete" if ok else f"status {st} or final")
def ingest(snapshot, manifest_sha256, wave, store, local, frozen, redownload_ok=False) -> dict:
    if frozen["ticket"]["wave"] != wave:
        raise ValueError(f"the frozen ticket is for wave {frozen['ticket']['wave']}, not {wave}")
    tr, out, msha = transfer_check(snapshot, manifest_sha256), {}, _lo(manifest_sha256)
    man = tr[0]
    for m in (x["model"] for x in frozen["ticket"]["models"]):
        if admitted(store, m) is not None:  # RC9: an admitted chain is never re-gated or replaced
            out[m] = {"status": "DONE", "gates": [], "admitted": True, "earlier": True}
            continue
        gates = [gate_weights_hash(snapshot, msha, m, redownload_ok, tr)]
        for fn in (lambda: gate_cloud_prov(snapshot, man, m, frozen),
                   lambda: gate_data_id(snapshot, man, m, local),
                   lambda: gate_train_complete(man, m, frozen["steps"], frozen["K"])):
            if gates[-1]["status"] != "PASS":
                break
            gates.append(fn())
        ok = [x["status"] for x in gates] == ["PASS"] * 4
        if ok:
            e = _entry(man, m)
            write_admission_lock(store, m, dict(zip(_LOCK_KEYS, (
                m, man["bundle_id"], msha, e["final_file_sha256"], e["final_weights_sha256"],
                [r["record_sha256"] for r in e["chain"]], sc.utc_iso()))))
            import_model(snapshot, store, wave, m, man)
        out[m] = {"status": "DONE" if ok else gates[-1]["status"], "gates": gates, "admitted": ok}
    return out

# ---- admission, import and retrain eligibility (§5.7, §12 items 9-10) ----
def _lock_path(store, model) -> Path: return Path(store) / "cloud" / "ADMITTED" / f"{model}.json"
def write_admission_lock(store, model, info) -> Path:
    p = _lock_path(store, model)
    p.parent.mkdir(parents=True, exist_ok=True)
    body = {k: info.get(k) for k in _LOCK_KEYS} | {"model": model}
    body["utc"] = body["utc"] or sc.utc_iso()
    _xwrite(p, _cj(body))  # exclusive create: an existing lock raises FileExistsError
    return p
def admitted(store, model):
    p = _lock_path(store, model)
    return json.loads(p.read_bytes()) if p.is_file() else None
def import_model(snapshot, store, wave, model, manifest) -> dict:
    src, e = Path(snapshot) / "out" / model, _entry(manifest, model)
    dst, files = Path(store) / "cloud" / wave / model, {}
    for d in ("ckpt", "rec"):
        (dst / d).mkdir(parents=True, exist_ok=True)
    for r in e["chain"]:
        for rel in (r["file"], f"rec/{r['step']:06d}.json"):
            files[rel] = _xwrite(dst / rel, (src / rel).read_bytes())
            if files[rel] != manifest["inventory"][f"out/{model}/{rel}"]:
                raise OSError(f"store copy of out/{model}/{rel} differs from the inventory")
    files["MANIFEST.json"] = _xwrite(dst / "MANIFEST.json", _cj(manifest))
    _xwrite(dst / "STORE_MANIFEST.json", _cj(files))
    return files
def _store_chain(store, model, wave=None) -> tuple:
    lock = admitted(store, model)
    if lock is None:
        raise ValueError(f"{model} has no admission lock")
    d = Path(store) / "cloud" / (wave or lock["bundle_id"].split("-")[0]) / model
    e = _entry(json.loads((d / "MANIFEST.json").read_bytes()), model)
    if [r["record_sha256"] for r in e["chain"]] != lock["chain_record_sha256"]:
        raise ValueError(f"{model}: the store chain differs from the admission lock")
    return d, e, lock
def verify_admitted(store, model) -> dict:
    try:
        d, e, lock = _store_chain(store, model)
        p = d / e["chain"][-1]["file"]
        data = p.read_bytes()
        got = (sc.sha256_bytes(data), sc.weights_digest(
            torch.load(io.BytesIO(data), map_location="cpu", weights_only=True)["model"]))
    except Exception as exc:
        return {"status": "INVALID", "detail": f"unreadable admitted model: {exc!r}"}
    ok = got == (lock["final_file_sha256"], lock["final_weights_sha256"])
    return {"status": "PASS" if ok else "INVALID", "path": str(p), "file_sha256": got[0],
            "weights_sha256": got[1], "detail": f"{'equal to' if ok else 'differs from'} the lock"}
def retrain_eligible(store, model, evaluations) -> bool:
    return admitted(store, model) is None and not list(evaluations)
def refinalised(snapshots, earlier_sha256=None) -> bool:
    try:
        a, b = (Path(p) for p in snapshots)
        ra, rb = ((p / "MANIFEST.json").read_bytes() for p in (a, b))
        ia, ib = (json.loads(r)["inventory"] for r in (ra, rb))
        return a.resolve() != b.resolve() and a.name < b.name and ra != rb and sorted(
            os.listdir(a)) == ["MANIFEST.json"] and all(ib.get(k) == v for k, v in ia.items()) \
            and earlier_sha256 in (None, sc.sha256_bytes(ra))
    except (OSError, ValueError, KeyError, TypeError):
        return False

# ---- descriptive local records (§4.5, §5.7; after admission) ----
def _xy(tokens) -> tuple:
    tok = np.asarray(getattr(tokens, "tokens", tokens))
    return se.model_inputs(tok), torch.from_numpy(tok.astype(np.int64))
def _model64(d, r):
    return se.ModelPredictor(d / r["file"], r["file_sha256"], r["weights_sha256"]).model
def loss_echo(store, wave, model, pool) -> dict:
    d, e, _ = _store_chain(store, model, wave)
    (x, y), chunks = _xy(pool), []
    for prev, r in zip(e["chain"], e["chain"][1:]):
        a = sc.draw_indices(sc.generator_from_state(prev["pcg64_state"]), len(x), 1,
                            sd.TRAIN_CFG.batch_size)[0]
        idx, m64 = torch.from_numpy(a), _model64(d, prev)
        with torch.no_grad():
            l32 = float(lm_loss(copy.deepcopy(m64).float()(x[idx]).logits, y[idx]))
            l64 = float(lm_loss(m64(x[idx]).logits, y[idx]))
        chunks.append(dict(step=r["step"], cloud=r["train_loss_first"], local32=l32, local64=l64))
    dev = {f"max_abs_{b}": max((abs(c["cloud"] - c[f"local{b}"]) for c in chunks), default=None)
           for b in (32, 64)}
    return {"model": model, "chunks": chunks} | dev
def learning_curve(store, models, dev_pools) -> dict:
    out = {}
    for m in models:
        (d, e, _), (arm, s) = _store_chain(store, m), sd.parse_model(m)
        x, y = _xy(dev_pools[m] if m in dev_pools else dev_pools[f"dev_{arm}_s{s}"])
        by, out[m] = {r["step"]: r for r in e["chain"]}, {}
        for step in sd.LC_STEPS:
            mod, tot = _model64(d, by[step]), 0.0
            with torch.no_grad():
                for a in range(0, len(x), b := sd.EVAL_BATCH):
                    tot += float(lm_loss(mod(x[a:a + b]).logits, y[a:a + b])) * len(x[a:a + b])
            out[m][step] = tot / len(x)
    return out
