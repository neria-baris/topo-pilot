"""Author B: T-BUNDLE (C0 build), T-NB, T-ENV (GPU refusal), T-S0, T-SIZE, T-RESOURCE (protocol
§4.6, §5.3, §5.11, §8, §13.4, §14). Synthetic fixtures; controls rebound to a tmp mailbox."""
from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest
import torch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "x6_stage1"))

import x6s1_cloud as sc  # noqa: E402
import x6s1_data as sd  # noqa: E402
import x6s1_ingest as si  # noqa: E402
import x6s1_run as sr  # noqa: E402
import d2a_train  # noqa: E402
from topo_pilot.contracts import SeedTree, canonical_json  # noqa: E402

TOOL, M = REPO / "tools" / "x6_stage1", "SMOKE"
NB, RUN_KEY = TOOL / "X6S1_colab.ipynb", ("x6s1", "smoke")


def _sha(b): return hashlib.sha256(b).hexdigest()  # noqa: E704
def _fsha(p): return _sha(Path(p).read_bytes())  # noqa: E704
def _head(): return _git("rev-parse", "HEAD").decode().strip()  # noqa: E704


def _git(*args) -> bytes:
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, check=True).stdout


def _api_cells():
    text = (TOOL / "API.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    sec = text.split("\n## 12. ", 1)[1].split("\n## 13. ", 1)[0]
    return re.findall(r"```python\n(.*?)\n```", sec, flags=re.S)


def _norm(src):
    src = "".join(src) if isinstance(src, list) else src
    return "\n".join(ln.rstrip() for ln in src.replace("\r\n", "\n").split("\n")).rstrip("\n")


# ---------------------------------------------------------------- T-BUNDLE (C0 build)
@pytest.fixture(scope="module")
def c0(tmp_path_factory):
    src, out_root = tmp_path_factory.mktemp("c0src"), tmp_path_factory.mktemp("cloud_bundle")
    toks = np.random.default_rng(1).integers(0, 18, size=(4096, 33), dtype=np.uint8)
    pool, ip, init = src / "smoke.npy", src / "init_smoke.pt", sd.init_state(M)
    torch.save(init, ip)
    pools = {M: {"path": str(pool), "file_sha256": sd.save_pool(pool, toks), "n_rows": 4096,
                 "token_sha256": sd.token_digest(toks),
                 "data_seed": SeedTree(sd.DATA_MASTER).seed("x6s1", "smoke", "NA")}}
    inits = {M: {"path": str(ip), "file_sha256": _fsha(ip),
                 "weights_sha256": sc.weights_digest(init["model"])}}
    args = ("C0", out_root, _head(), REPO, pools, inits, NB)
    return {"res": si.build_bundle(*args), "args": args}


def test_c0_bundle_sums_ticket_and_chain_parameters(c0):
    res, d = c0["res"], Path(c0["res"]["bundle_dir"])
    sums = (d / "SHA256SUMS").read_bytes()
    assert res["bundle_sha256"] == _sha(sums) and res["bundle_id"] == f"C0-{_sha(sums)[:12]}"
    assert d.name == res["bundle_id"] and b"\r" not in sums and sums.endswith(b"\n")
    lines = sums.decode("ascii").splitlines()
    listed = {ln[66:]: ln[:64] for ln in lines}
    assert [ln[66:] for ln in lines] == sorted(listed) and all(ln[64:66] == "  " for ln in lines)
    files = {p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file()}
    assert files == {"code.tar", "X6S1_colab.ipynb", "SHA256SUMS", "ticket_C0.json",
                     "data/smoke.npy", "init/init_smoke.pt"}
    assert set(listed) == files - {"SHA256SUMS", "X6S1_colab.ipynb"}
    assert all(_fsha(d / rel) == h for rel, h in listed.items())
    t = json.loads((d / "ticket_C0.json").read_text(encoding="utf-8"))
    assert (t["schema"], t["wave"], t["steps"], t["K"], t["batch_size"], t["smoke_resume"]) == (
        sc.TICKET_SCHEMA, "C0", 200, 100, 128, True)
    assert t["train_config"] == json.loads(canonical_json(dataclasses.asdict(sd.SMOKE_CFG)))
    assert t["model_config"] == json.loads(canonical_json(dataclasses.asdict(sd.MODEL_CFG)))
    assert (t["data_master"], t["model_master"]) == (sd.DATA_MASTER, sd.MODEL_MASTER)
    assert t["protocol_sha256"] == sd.PROTOCOL_SHA256 and t["code_commit"] == c0["args"][2]
    assert t["cell_templates_sha256"] == [_sha(x.encode("utf-8")) for x in sc.CELL_TEMPLATES]
    assert t["bundle_files"] == sorted(listed) and [e["model"] for e in t["models"]] == [M]
    e = t["models"][0]
    assert e["run_key"] == list(RUN_KEY) and e["init_seed"] == sd.init_seed(M)
    assert e["expected"] == sc.expected_digests(sd.MODEL_MASTER, RUN_KEY, 4096, 200, 100)
    assert [x["step"] for x in e["expected"]] == [0, 100, 200]  # C0 chain: steps 200, K 100
    assert e["data_sha256"] == listed["data/smoke.npy"]
    assert e["init_weights_sha256"] == c0["args"][5][M]["weights_sha256"]
    assert si.check_bundle(d, "C0")["status"] == "PASS"
    with pytest.raises(FileExistsError):  # one immutable directory per bundle id
        si.build_bundle(*c0["args"])


@pytest.mark.parametrize("rel", ["data/val_NA.npy", "data/test_NA.npy", "data/gate_NA.npy",
                                 "data/prefix.npy", "data/dev_NA_s1.npy", "sealed/learn.json",
                                 "registry/X6-REG2.json", "data/train_AB_s1.npy",
                                 "init/init_s3.pt", "data/latent_states.npy"])
def test_check_bundle_refuses_forbidden_classes(c0, tmp_path, rel):
    d = tmp_path / Path(c0["res"]["bundle_dir"]).name
    shutil.copytree(c0["res"]["bundle_dir"], d)
    (d / rel).parent.mkdir(parents=True, exist_ok=True)
    (d / rel).write_bytes(b"\x93NUMPY synthetic")
    files = sorted(p.relative_to(d).as_posix() for p in d.rglob("*")
                   if p.is_file() and p.name not in ("SHA256SUMS", "X6S1_colab.ipynb"))
    (d / "SHA256SUMS").write_bytes("".join(f"{_fsha(d / f)}  {f}\n" for f in files).encode())
    out = si.check_bundle(d, "C0")
    assert out["status"] == "INVALID" and rel in out["refused"]


# ---------------------------------------------------------------- T-NB
def test_cell_templates_verbatim_from_api():
    cells = _api_cells()
    assert len(cells) == 6 and tuple(cells) == tuple(sc.CELL_TEMPLATES)
    assert sum(len(c.split("\n")) for c in cells) == 36
    assert all("\r" not in c and not c.endswith("\n") for c in sc.CELL_TEMPLATES)
    assert sc.HASH_PLACEHOLDER == "PASTE_BUNDLE_SHA256_HERE" in sc.CELL_TEMPLATES[1]


def test_notebook_static_independent_and_nb_static():
    nb = json.loads(NB.read_text(encoding="utf-8"))
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    assert nb["nbformat"] == 4 and len(code) == 6
    assert {c["cell_type"] for c in nb["cells"]} <= {"code", "markdown"}
    assert [_norm(c["source"]) for c in code] == list(sc.CELL_TEMPLATES)
    assert all(c.get("outputs") == [] and c.get("execution_count") is None for c in code)
    assert sum(len(_norm(c["source"]).split("\n")) for c in code) <= 60
    assert sr.nb_static(NB)["status"] == "PASS"


NB_EDITS = {
    "edited": lambda nb, c: c[3].update(source=_norm(c[3]["source"]) + "\nprint('x')"),
    "output": lambda nb, c: c[4].update(outputs=[{"output_type": "stream", "name": "stdout",
                                                  "text": ["x\n"]}]),
    "count": lambda nb, c: c[0].update(execution_count=1),
    "seventh": lambda nb, c: nb["cells"].append(json.loads(json.dumps(c[4]))),
    "missing": lambda nb, c: nb["cells"].remove(c[5]),
    "order": lambda nb, c: nb.update(cells=[x for x in nb["cells"] if x is not c[3]] + [c[3]]),
    "nbformat": lambda nb, c: nb.update(nbformat=3)}


@pytest.mark.parametrize("case", [*NB_EDITS, "json"])
def test_nb_static_refuses(tmp_path, case):
    nb = json.loads(NB.read_text(encoding="utf-8"))
    if case in NB_EDITS:
        NB_EDITS[case](nb, [c for c in nb["cells"] if c["cell_type"] == "code"])
    p = tmp_path / "X6S1_colab.ipynb"
    p.write_text("{not json" if case == "json" else json.dumps(nb), encoding="utf-8")
    assert sr.nb_static(p)["status"] != "PASS"


def _exec_bootstrap(root, sha):  # the inline hashlib bootstrap, independently of the module
    # API-AMBIGUITY: API §12 says "lines 2-9" but also "from import hashlib through the second
    # raise" (= lines 2-8; line 9 extracts code.tar); the latter is executed (never extract).
    lines = _api_cells()[2].split("\n")
    end = [i for i, ln in enumerate(lines) if "raise SystemExit" in ln][1]
    try:
        exec("\n".join(lines[1:end + 1]), {"ROOT": Path(root).as_posix(), "BUNDLE_SHA256": sha})
    except SystemExit as exc:
        return str(exc)
    return "OK"


@pytest.mark.parametrize("case", ["ok", "upper", "sums", "tar"])
def test_inline_bootstrap_refuses_modified_bundle(tmp_path, case):
    d = tmp_path / "C1-0123456789ab"
    d.mkdir()
    (d / "code.tar").write_bytes(b"tar bytes")
    (d / "SHA256SUMS").write_bytes(f"{_sha(b'tar bytes')}  code.tar\n".encode("ascii"))
    sha = f"  {_fsha(d / 'SHA256SUMS').upper()} " if case == "upper" else _fsha(d / "SHA256SUMS")
    if case == "sums":
        (d / "SHA256SUMS").write_bytes((d / "SHA256SUMS").read_bytes() + b"0" * 64 + b"  x\n")
    elif case == "tar":
        (d / "code.tar").write_bytes(b"tampered")
    want = "OK" if case in ("ok", "upper") else "STOP: BUNDLE HASH MISMATCH"
    assert _exec_bootstrap(d, sha) == want and sr.bootstrap_check(d, sha) == want


@pytest.mark.skipif(torch.cuda.is_available(), reason="a CUDA device is present")
def test_environment_refuses_cpu_runtime(tmp_path):  # T-ENV
    with pytest.raises(sc.CloudStop, match="STOP: NO GPU"):
        sc.environment(tmp_path, {})


# ---------------------------------------------------------------- T-S0
A, NOTES = "A\t", ("API.md", "PROTOCOL_X6S1_v1.md", "X6S1_colab.ipynb")
GOOD = ([A + f"tools/x6_stage1/{m}" for m in sr.MODULES]
        + [A + f"tools/x6_stage1/{f}" for f in NOTES]
        + [A + f"tests/x6_stage1/AUTHORSHIP_{x}.md" for x in "AB"]
        + [A + f"tests/x6_stage1/test_{x}_n{i}.py" for x in "ab" for i in range(4)])


@pytest.mark.parametrize("extra,ok", [
    ([], True), ([A + "tests/x6_stage1/test_b_n4.py"], True),
    ([A + "tests/x6_stage1/test_b_n4.py", A + "tests/x6_stage1/test_b_n5.py"], False),
    ([A + "tests/x6_stage1/test_b_Bad.py"], False), ([A + "tests/x6_stage1/conftest.py"], False),
    (["M\tsrc/topo_pilot/learner/trainer.py"], False), (["M\ttools/x6_stage1/API.md"], False),
    ([A + "tools/x6_stage1/x6s1_extra.py"], False), (["D\ttools/d2a/d2a_train.py"], False)])
def test_allowlist(extra, ok):
    assert sr.allowlist_ok(GOOD + extra) is ok


@pytest.mark.parametrize("path", sorted(sd.REPAIR_BLOBS))
def test_repair_blob_hashes_at_head(path):
    sha, blob = sd.REPAIR_BLOBS[path]
    data = _git("cat-file", "blob", f"HEAD:{path}")
    assert _sha(data) == sha
    assert hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest() == blob


def test_repair_ancestry_and_d2a_unchanged():
    anc = ["git", "-C", str(REPO), "merge-base", "--is-ancestor", sd.P_COMMIT, sd.R_COMMIT]
    assert subprocess.run(anc).returncode == 0
    assert _git("diff", "--name-only", sd.P_COMMIT, "HEAD", "--", "tools/d2a").strip() == b""
    assert sr.repair_ok(REPO, _head())["status"] == "PASS"


def test_protocol_and_stage0_hash_bindings():
    assert sd.PROTOCOL_ID == "X6S1-FROZEN-v1"
    assert _sha(_git("cat-file", "blob", "HEAD:tools/x6_stage1/PROTOCOL_X6S1_v1.md")) == \
        sd.PROTOCOL_SHA256 == "2a909ace38231fbc6647e8ffdb5e6b5f22669a7c92182ae84240f32cd36efb9e"
    assert {k: (v[:8], v[-4:]) for k, v in sd.STAGE0_FILES.items()} == {  # §8 row 1 (v)
        "run/report.json": ("e7846911", "3aca"), "run/GATES.jsonl": ("c871f5e4", "2462"),
        "run/model.npz": ("e1b9a753", "230b")} and sd.STAGE0_OUTCOME == "GO_X6_NATURAL"


def _report(edit=None):
    rep = {}
    for name, spec in sd.CONST_MAP.items():
        node, keys = rep, spec["path"].split("/")
        for k in keys[:-1]:
            node = node.setdefault(k, {})
        leaf = {k: spec[k] for k in ("lo", "hi") if k in spec} if "lo" in spec else spec["value"]
        node[keys[-1]] = dict(leaf, lo=edit[name]) if edit and name in edit else leaf
    return rep


def test_stage0_constants_exact_string_equality():
    lo = sd.CONST_MAP["G_Parikh_32"]["lo"]
    assert sd.CONST_MAP["G_Parikh_32"]["path"] == "natural/NA/G/Parikh/32"
    assert lo == ("0.00263589648067905165440741952994185251908766707464276216269519347935792934"
                  "30931071")
    assert "G_Parikh_32" not in sd.check_stage0_constants(_report())["mismatches"]
    for bad in (lo[:-1] + "2", lo + "0", str(float(lo))):  # exact strings, no reformatting (T24)
        out = sd.check_stage0_constants(_report({"G_Parikh_32": bad}))
        assert out["status"] == "FAIL" and "G_Parikh_32" in out["mismatches"]
    assert sd.g0_lo() == Fraction(lo) and sd.target_threshold() == Fraction(3, 4) * Fraction(lo)


def test_notebook_sha_binding():
    sha = _sha(_git("cat-file", "blob", "HEAD:tools/x6_stage1/X6S1_colab.ipynb"))
    # API-AMBIGUITY: the FREEZE.json key for the notebook sha256 is not fixed; "notebook_sha256".
    assert sr.notebook_sha_ok(REPO, _head(), {"notebook_sha256": sha}) is True
    assert sr.notebook_sha_ok(REPO, _head(), {"notebook_sha256": "0" * 64}) is False


# ---------------------------------------------------------------- T-SIZE
def test_module_set_line_limits_and_test_files():
    mods = sorted(p.name for p in TOOL.glob("*.py"))
    assert mods == sorted(sr.MODULES) and set(mods) == {f"x6s1_{m}.py" for m in (
        "data", "pairs", "cloud", "ingest", "eval", "decide", "run", "registry", "stats")}
    assert {p.name for p in TOOL.iterdir() if p.is_file()} - set(mods) == set(NOTES)
    n = {m[5:-3]: len((TOOL / m).read_bytes().splitlines()) for m in mods}  # R-0073-1
    assert all(v <= (560 if k in ("cloud", "registry", "ingest", "run") else 400)
               for k, v in n.items()) and sum(n.values()) <= 3600
    tests = sorted(p.name for p in (REPO / "tests" / "x6_stage1").glob("*.py"))
    for tag, mine in ((g, [t for t in tests if t.startswith(f"test_{g}_")]) for g in "ab"):
        assert len(mine) <= 5 and all(re.fullmatch(rf"test_{tag}_[a-z0-9_]+\.py", t) for t in mine)
    assert all(t.startswith(("test_a_", "test_b_")) for t in tests)
    assert all(len((REPO / "tests/x6_stage1" / t).read_bytes().splitlines()) <= 400 for t in tests)


# ---------------------------------------------------------------- T-RESOURCE
class FakeTree:
    def __init__(self, cpu=1.0, mem=2**28, polls=2):
        self.cpu, self.mem, self.left = cpu, mem, polls
        self.killed, self.closed, self.returncode = False, False, None

    def cpu_s(self): return self.cpu  # noqa: E704
    def memory_bytes(self): return self.mem  # noqa: E704
    def terminate(self): self.killed = True  # noqa: E704
    def close(self): self.closed = True  # noqa: E704
    def wait(self, timeout=None): return self.poll()  # noqa: E704

    def poll(self):
        self.left -= 1
        if self.killed or self.left <= 0:
            self.returncode = 1 if self.killed else 0
        return self.returncode


def _quiet_controls(monkeypatch, tmp_path, states=()):
    import controls
    seq, calls, real = list(states), [], d2a_train.boundary

    def classify():
        calls.append(1)
        return seq.pop(0) if seq else ("CONTINUE", "test")
    monkeypatch.setattr(controls, "MAILBOX", tmp_path / "mailbox")
    monkeypatch.setattr(sd, "MAILBOX", str(tmp_path / "mailbox"))
    for mod in (d2a_train, sr):
        monkeypatch.setattr(mod, "bound_controls", lambda *a, **k: classify, raising=False)
    monkeypatch.setattr(d2a_train, "boundary", lambda c, sleep=None, poll_s=30.0: real(
        c, sleep=lambda _: None, poll_s=poll_s))
    monkeypatch.setattr(sr, "boundary", d2a_train.boundary, raising=False)
    return calls


def test_limits_and_resource_constants():
    lim = sr.limits()
    assert isinstance(lim, d2a_train.Limits) and lim.poll_s == 2.0
    assert (lim.model_cpu_s, lim.total_cpu_s) == (math.inf, math.inf)
    assert (lim.process_mem, lim.job_mem) == (3 * 2**30, 12 * 2**30)
    assert lim.stage_cpu_s["E3"] == lim.stage_cpu_s["PF"] == math.inf
    assert sr.limits(model_cpu_s=5.0).model_cpu_s == 5.0 and sd.MAX_CHILDREN == 3
    assert (sd.THREADS, sd.MAX_WALL_S, sd.ALARM_CPU_S) == ({"intra": 2, "interop": 1}, 43200,
                                                           90 * 3600)


@pytest.mark.parametrize("kind,status", [("ok", "DONE"), ("cpu", "INCOMPLETE:MODEL_CPU"),
                                         ("mem", "INCOMPLETE:PROCESS_MEMORY")])
def test_supervise_enforces_s6_limits(tmp_path, monkeypatch, kind, status):
    _quiet_controls(monkeypatch, tmp_path)
    tree = FakeTree(cpu=6.0 if kind == "cpu" else 1.0, mem=4 * 2**30 if kind == "mem" else 2**28,
                    polls=2 if kind == "ok" else 10**6)
    lim = dataclasses.replace(sr.limits(model_cpu_s=5.0), poll_s=0.01)
    out = sr.supervise({"c": tree}, lim, "E3")
    assert out["c"]["status"] == status and tree.closed and (kind == "ok" or tree.killed)
    assert not (tmp_path / "mailbox").exists()  # no mailbox writes


def test_supervise_stop_propagates_and_closes_children(tmp_path, monkeypatch):
    calls = _quiet_controls(monkeypatch, tmp_path, [("STOP", "owner STOP")])
    trees = {"a": FakeTree(polls=10**6), "b": FakeTree(polls=10**6)}
    try:
        res = sr.supervise(trees, dataclasses.replace(sr.limits(), poll_s=0.01), "E3")
    except d2a_train.D2AStop:
        res = None
    assert res is None or "STOP" in json.dumps(res, default=str)
    assert calls and all(t.killed and t.closed for t in trees.values())


def test_supervise_hold_waits_then_continues(tmp_path, monkeypatch):
    calls = _quiet_controls(monkeypatch, tmp_path, [("HOLD", "pause"), ("HOLD", "pause")])
    tree = FakeTree(polls=3)
    out = sr.supervise({"c": tree}, dataclasses.replace(sr.limits(), poll_s=0.01), "E3")
    assert out["c"]["status"] == "DONE" and len(calls) >= 3 and tree.closed


def _alive(pid):
    import ctypes
    k32 = ctypes.windll.kernel32
    h = k32.OpenProcess(0x00100000 | 0x1000, False, pid)  # SYNCHRONIZE | QUERY_LIMITED_INFO
    if not h:
        return False
    try:
        return k32.WaitForSingleObject(h, 0) == 0x102  # WAIT_TIMEOUT: still running
    finally:
        k32.CloseHandle(h)


@pytest.mark.skipif(os.name != "nt", reason="Windows Job Objects")
def test_tree_accounting_reads_interpreter_and_kill_reaches_it(tmp_path, monkeypatch):
    _quiet_controls(monkeypatch, tmp_path)
    ready = tmp_path / "ready.json"
    code = ("import json,os,time; from pathlib import Path; data=bytearray(64*1024**2); "
            "s=time.process_time(); exec('while time.process_time()-s < 1.5: pass'); "
            f"Path({str(ready)!r}).write_text(json.dumps([os.getpid(), time.process_time()-s]));"
            " time.sleep(120)")
    launcher = f"import subprocess,sys; sys.exit(subprocess.call([sys.executable,'-c',{code!r}]))"
    child = sr.launch([sys.executable, "-c", launcher], tmp_path / "child.log")
    try:
        deadline = time.monotonic() + 60
        while not ready.exists():
            assert time.monotonic() < deadline, "grandchild never became ready"
            time.sleep(0.05)
        time.sleep(0.3)
        pid, burned = json.loads(ready.read_text())
        assert child.cpu_s() >= 0.8 * burned  # the interpreter, not the waiting launcher
        assert child.memory_bytes() >= 64 * 1024**2
        lim = dataclasses.replace(sr.limits(model_cpu_s=1.0), poll_s=0.5)
        t0 = time.monotonic()
        assert sr.supervise({"burn": child}, lim, "E3")["burn"]["status"] == "INCOMPLETE:MODEL_CPU"
        assert not _alive(pid) and time.monotonic() - t0 <= 2 * lim.poll_s + 10
    finally:
        for fn in (child.terminate, child.close):
            try:
                fn()
            except Exception:  # noqa: BLE001  already closed by supervise
                pass
