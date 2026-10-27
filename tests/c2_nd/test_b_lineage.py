"""Author B, T-NAMESPACE-ND (protocol §6.6, RC-11; split here from test_b_registry.py),
T-G0-ND (§3 row 1), T-METER (§9, §6.8) and T-SIZE (§11.3); API.md §4.2-§4.3, §9.3, §9.5,
§9.8, §12. Synthetic worktrees, stores and project roots under pytest's tmp_path only."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if sys.path[:1] != [str(REPO / "tools" / "c2_nd")]:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first, API.md §1 "Test imports")

# isort: split
import c2_config as cc  # noqa: E402
import nd_data as nda  # noqa: E402
import nd_driver as ndr  # noqa: E402
import nd_registry as nrg  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

from topo_pilot.contracts import SeedTree  # noqa: E402
from topo_pilot.dataset.checks import make_sequence_ids, process_code  # noqa: E402

PKG = REPO / "tools" / "c2_nd"
LIN, AUTH = "FAIL_TECHNICAL/LINEAGE", "FAIL_TECHNICAL/AUTHORITY"
ND = b"c2nd-v1"
C2 = cc.SCOPE.encode("ascii")  # C2's scope, built at run time (never a literal here)
HWS = bytes.fromhex(nc.CONTRACT["namespace"]["parallel_needles_hex"][0])


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(data)
    return Path(path)


@pytest.fixture
def world(tmp_path, monkeypatch):
    root = tmp_path / "root"
    paths = {"PROJECT_ROOT": root, "WORKTREE": root / "topo-pilot-c2nd",
             "STORE": root / "c2nd-store", "C2_STORE": root / "c2-readout-store",
             "MAILBOX": root / "agent-handoff", "HWS_STORE": root / "hws-store",
             "X6ZC_STORE": root / "x6zc-store", "SCRATCH_ROOT": tmp_path / "scratch"}
    for attr, p in paths.items():
        monkeypatch.setattr(nc, attr, p)
    for attr in ("ARTIFACT_ROOT", "C1P_STORE", "X6S1_STORE", "K4_FREEZE"):  # no real store read
        fake = tmp_path / "c2paths" / attr
        monkeypatch.setattr(cc, attr, fake)
        monkeypatch.setattr(nc, attr, fake, raising=False)
    for p in ("WORKTREE", "STORE", "SCRATCH_ROOT"):
        paths[p].mkdir(parents=True)
    return paths


# ---- T-NAMESPACE-ND ---------------------------------------------------------------------------
def classes(res):
    return {Path(h["path"]).name: h["class"] for h in res["hits"]}


def test_namespace_scan(world):
    root, store = world["PROJECT_ROOT"], world["STORE"]
    put(world["WORKTREE"] / "tools" / "c2_nd" / "CONTRACT.json", b'{"scope": "' + ND + b'"}')
    rec = put(store / "GATES.jsonl", b'{"note": "' + ND + b'"}\n')
    lineage = {"GATES.jsonl": sha(rec)}
    res = nda.namespace_scan(root, {}, lineage)
    assert res["status"] == "PASS" and res["scanned"] >= 2
    assert classes(res) == {"CONTRACT.json": "PINNED", "GATES.jsonl": "LINEAGE"}
    assert nda.namespace_scan(root, {}, {})["status"] == LIN  # an unrecognised store record
    put(root / "other-store" / "foreign.json", ND)
    res = nda.namespace_scan(root, {}, lineage)
    assert res["status"] == LIN and classes(res)["foreign.json"] == "FOREIGN"


def test_namespace_hit_in_a_parallel_store_is_foreign(world):
    root = world["PROJECT_ROOT"]
    for store in ("hws-store", "x6zc-store"):
        put(root / store / "stages" / f"{store}.json", ND)
    res = nda.namespace_scan(root, {}, {f"{s}.json": "x" for s in ("hws-store", "x6zc-store")})
    assert res["status"] == LIN
    assert classes(res) == {"hws-store.json": "FOREIGN", "x6zc-store.json": "FOREIGN"}


@pytest.mark.parametrize("where, needle, want", [
    ("WORKTREE/tools/c2_nd/CONTRACT.json", C2, LIN),
    ("STORE/stages/S1/record.json", C2, LIN),
    ("STORE/GATES.jsonl", C2, LIN),
    ("STORE/stages/S1/notes.json", HWS, LIN),
    ("WORKTREE/tools/c2_nd/PROTOCOL_C2ND_v1.md", C2, "PASS"),  # the exempt protocol copy
    ("STORE/stages/S1/record.json", ND, "PASS"),
])
def test_hygiene_check(world, where, needle, want):
    put(world["WORKTREE"] / "tools" / "c2_nd" / "CONTRACT.json", b'{"scope": "' + ND + b'"}')
    assert nda.hygiene_check(world["PROJECT_ROOT"])["status"] == "PASS"
    base, _, rel = where.partition("/")
    path = put(world[base] / rel, b"{" + needle + b"}")
    res = nda.hygiene_check(world["PROJECT_ROOT"])
    assert res["status"] == want
    if want != "PASS":
        assert any(Path(h).name == path.name for h in res["hits"])


def test_needles_and_the_real_contract():
    assert nda.NEEDLE == ND and nc.SCOPE == "c2nd-v1"
    assert nda.C2_NEEDLE == C2 and C2 not in ND
    assert tuple(nda.PARALLEL_NEEDLES) == (HWS,)
    raw = (PKG / "CONTRACT.json").read_bytes()
    assert C2 not in raw and HWS not in raw
    assert nc.CONTRACT["namespace"]["x6zc_needle"] is None  # R-0116-4


def test_store_admission_payload_at_first_sampling(world):
    store = world["STORE"]
    lin = {rel: sha(put(store / rel, b"{}")) for rel in
           ("decoys/DECOY_1729.json", "registry/ND-REG1.json", "FREEZE.json")}
    res = nda.store_admission(store, lin, True)
    assert res["status"] == LIN
    assert {"decoys/DECOY_1729.json", "registry/ND-REG1.json"} <= set(res["payload"])
    assert nda.store_admission(store, lin, False)["status"] == "PASS"
    assert tuple(nda.PAYLOAD_DIRS) == ("hist", "oracle", "fits", "decoys", "registry",
                                        "stages", "sealed")


# ---- T-G0-ND ----------------------------------------------------------------------------------
def fit_keys():
    fk = nc.CONTRACT["c2_store"]["fit_keys"]
    keys = list(fk["basis"]) + list(fk["other"])
    for p in fk["problems"]:
        for x in ("alpha", "Gamma", "B", "L", "P_S", "P_G", "Sigma", "mtilde"):
            if not (x == "Sigma" and p == "R_E"):
                keys.append(f"{p}_{x}")
    return keys


def dec_keys():
    dk = nc.CONTRACT["c2_store"]["dec_keys"]
    return [f"{F}_{k}_{x}" for F in dk["F"] for k in dk["k"] for x in dk["x"]]


def c2_store_files(world, monkeypatch, drop=None):
    """A synthetic C2 store whose files re-hash to the (in-place patched) CONTRACT table."""
    store, table = world["C2_STORE"], nc.CONTRACT["c2_store"]["files"]
    for rel in sorted(table):
        p = store / rel
        if rel.startswith("fits/") and rel.endswith(".npz"):
            keys = fit_keys() if "FIT_" in rel else dec_keys()
            put(p, b"")
            with open(p, "wb") as fh:
                np.savez(fh, **{k: np.zeros(1) for k in keys if k != drop})
        elif rel == "manifests/0115.accepted.json":
            continue
        else:
            put(p, json.dumps({"synthetic": rel}).encode("utf-8"))
    acc = {"job": "0115", "manifest_sha256": sha(store / "manifests" / "0115.json")}
    put(store / "manifests" / "0115.accepted.json", json.dumps(acc).encode("utf-8"))
    for rel in table:
        monkeypatch.setitem(table, rel, sha(store / rel))


def g0_world(world, monkeypatch, drop=None, dry=False, freeze_ok=True):
    root, wt, store = world["PROJECT_ROOT"], world["WORKTREE"], world["STORE"]
    proto = (PKG / "PROTOCOL_C2ND_v1.md").read_bytes()
    put(wt / "tools" / "c2_nd" / "PROTOCOL_C2ND_v1.md", proto)
    put(root / nc.CONTRACT["protocol"]["mailbox_file"], proto)
    put(wt / "tools" / "c2_nd" / "CONTRACT.json", (PKG / "CONTRACT.json").read_bytes())
    want = sha(PKG / "CONTRACT.json") if freeze_ok else "0" * 64
    put(store / "FREEZE.json", json.dumps({"schema": "c2nd-freeze-v1",
                                           "contract_sha256": want}).encode("utf-8"))
    c2_store_files(world, monkeypatch, drop)
    return ndr.Ctx(store=store, worktree=wt, head="0" * 40, job="0130", task_sha256="ab" * 32,
                   session="sess-b", release=None, policy=None, data={"stage": "S1"}, dry=dry)


@pytest.fixture
def loads(monkeypatch):
    seen, real = [], np.load

    def spy(file, *a, **k):
        seen.append(str(getattr(file, "name", file)).replace("\\", "/"))
        return real(file, *a, **k)

    monkeypatch.setattr(np, "load", spy)
    return seen


# API-AMBIGUITY: g0's item keys are taken as the C2 form "i" ... "x" (API.md §9.3 numbers the
# items (i)-(x) but does not name the dict keys).
def test_g0_items_on_a_synthetic_world(world, monkeypatch, loads):
    ctx = g0_world(world, monkeypatch)
    out = ndr.g0(ctx)
    for item in ("i", "ii", "iv", "x"):
        assert out[item]["status"] == "PASS", (item, out[item])
    assert out["status"] == AUTH  # blobs, charts, dispatch and the reservation are absent
    assert out["ix"]["status"] == "FAIL"  # no RESERVATION_S1.json
    assert not [p for p in loads if "/fits/" in p]  # key sets from the zip directory only


def test_g0_protocol_contract_and_c2_store_failures(world, monkeypatch):
    ctx = g0_world(world, monkeypatch, freeze_ok=False)
    assert ndr.g0(ctx)["ii"]["status"] == "FAIL"
    put(world["PROJECT_ROOT"] / nc.CONTRACT["protocol"]["mailbox_file"], b"edited copy\n")
    out = ndr.g0(ctx)
    assert out["i"]["status"] == "FAIL" and out["status"] == AUTH
    rel = "fits/FIT_1729.json"
    put(world["C2_STORE"] / rel, b'{"edited": true}')  # a C2 store re-hash mismatch
    assert ndr.g0(ctx)["iv"]["status"] == "FAIL"


def test_g0_fit_key_set(world, monkeypatch):
    ctx = g0_world(world, monkeypatch, drop="R_P_S")
    assert ndr.g0(ctx)["iv"]["status"] == "FAIL"


def test_g0_store_admission_and_dry_guard(world, monkeypatch):
    ctx = g0_world(world, monkeypatch)
    put(world["STORE"] / "decoys" / "DECOY_1729.json", b"{}")
    assert ndr.g0(ctx)["vii"]["status"] == "FAIL"  # decoys/ before the first sampling
    ctx.dry = True  # the dry switch outside a dry-run store
    assert ndr.g0(ctx)["x"]["status"] == "FAIL"


def auth_record(schema, **change):
    rec = {"schema": schema, "protocol_sha256": nc.PROTOCOL_SHA256,
           "owner_record": {"path": nc.CONTRACT["protocol"]["auth"]["file"],
                            "sha256": nc.AUTH_SHA256, "owner_verbatim": "yes",
                            "granted_utc": "2026-10-26T00:00:00Z"},
           "budget": {"central_cpu_h": "0.4", "range_cpu_h": ["0.25", "0.8"],
                      "cpu_policy": "measure-only", "combined_cap_cpu_h": 12},
           "coordinator": "c", "written_utc": "2026-10-26T00:00:00Z"}
    rec.update(change)
    return json.dumps(rec).encode("utf-8")


def test_auth_ok(tmp_path):
    put(tmp_path / "AUTH.json", auth_record("c2nd-auth-v1"))
    assert ndr.auth_ok(tmp_path) is True
    put(tmp_path / "AUTH_IMPL.json", auth_record("c2nd-auth-impl-v1"))
    assert ndr.auth_ok(tmp_path, "AUTH_IMPL.json") is True
    put(tmp_path / "AUTH.json", auth_record("c2-auth-v1"))
    assert ndr.auth_ok(tmp_path) is False
    put(tmp_path / "AUTH.json", auth_record("c2nd-auth-v1", coordinator=""))
    assert ndr.auth_ok(tmp_path) is False
    put(tmp_path / "AUTH.json", b"not json")
    assert ndr.auth_ok(tmp_path) is False


def test_contract_values():
    assert nc.CONTRACT["seeds"] == {
        "test_NR": 630503, "test_D": 630504, "test_NM": 630505, "val_KC": 630506,
        "test_KC": 630507, "desc": 630508, "val_V3x": 630511, "val_V3y": 630512,
        "val_Y1": 630513, "val_V3xD": 630514, "val_Y1D": 630515, "val_p1_sd": 630516,
        "val_p1_c": 630517, "h5": 630518, "val_V3xD_g1": 630519}
    assert all(nc.seed(k) == v for k, v in nc.CONTRACT["seeds"].items())
    dec = nc.CONTRACT["decoys"]
    assert (dec["g_D"], dec["rho"]) == ("6", "23/25")
    assert nc.G_D == 6 and nc.RHO == Fraction(23, 25)
    assert nc.CONTRACT["hashes"]["state_sha_f32"] == {
        "1729": "062d0a0aa71c41ad5afd9d3f76e58cf38a81419d629defcf2e3ac6316ffaf8f8",
        "2718": "501d9c9ad80d4ffe272d7e03003cdee24b7fe3b25bed40e044f2111afd69aa5c",
        "3141": "197cccd6cf5491143171fe8ccd6ce79f71cb2f16995aa99af4e9dffe4bec94c8"}
    assert {j: m["state_sha_f32"] for j, m in nc.CONTRACT["models"].items()} == \
        nc.CONTRACT["hashes"]["state_sha_f32"]
    assert nc.ALPHA == {"N-R": Fraction(1, 300), "D": Fraction(1, 300), "N-M": Fraction(1, 360)}
    assert nc.CONTRACT["levels"]["alpha"] == {"N-R": "1/300", "D": "1/300", "N-M": "1/360"}
    assert nc.PROTOCOL_SHA256 == nc.CONTRACT["protocol"]["sha256"] == sha(
        PKG / "PROTOCOL_C2ND_v1.md")


def test_sequence_ids_and_streams():
    seq = nc.CONTRACT["sequence_ids"]
    spot = {"fit/b0": 154628954, "val/b0": 1752527724, "test/b0": 445333687}
    assert all(seq["codes"][k] == v for k, v in spot.items())
    assert seq["dry_codes"]["fit/b0"] == 706028483
    c2_codes = set()
    for key, code in seq["codes"].items():
        split, block = key.split("/")
        assert process_code("cylinder", "overlap", "1.25", f"c2nd-v1/{key}") == code
        assert process_code("cylinder", "overlap", "1.25", f"c2nd-dry-v1/{key}") == \
            seq["dry_codes"][key]
        ids = make_sequence_ids(code, "test", 4096)
        assert int(ids[0]) == seq["first_ids"][key] == (code << 32) | (3 << 28)
        got = nda.sequence_ids(split, int(block[1:]))
        assert got.dtype == np.int64 and np.array_equal(got, np.asarray(ids, np.int64))
        c2_codes.add(process_code("cylinder", "overlap", "1.25", f"{cc.SCOPE}/{key}"))
    assert not c2_codes & (set(seq["codes"].values()) | set(seq["dry_codes"].values()))
    want = SeedTree(0).generator("data", "c2nd-v1", "val", 0, "cylinder", "overlap", "1.25")
    a = nda.history_generator("val", 0).integers(0, 2**32, size=8)
    assert np.array_equal(a, want.integers(0, 2**32, size=8))
    assert np.array_equal(a, nda.history_generator("val", 0).integers(0, 2**32, size=8))
    dry = nda.history_generator("val", 0, scope=nc.DRY_SCOPE).integers(0, 2**32, size=8)
    assert not np.array_equal(a, dry)
    with pytest.raises(ValueError):
        nda.history_generator("pilot", 0)


# ---- T-METER ----------------------------------------------------------------------------------
def test_meter_bind_check(world):
    meter_dir = world["WORKTREE"] / "tools" / "x4_oracle_profile"
    meter_dir.mkdir(parents=True)
    bind = put(world["STORE"] / "nd_meter_bind.py", b"# store-local meter binding\n")
    ndr.meter_bind_check(bind, sha(bind), meter_dir)
    with pytest.raises(Exception):
        ndr.meter_bind_check(bind, "0" * 64, meter_dir)
    other = world["PROJECT_ROOT"] / "topo-pilot" / "tools" / "x4_oracle_profile"
    other.mkdir(parents=True)
    with pytest.raises(Exception):
        ndr.meter_bind_check(bind, sha(bind), other)


# API-AMBIGUITY: no API.md function returns the meter command line; the measure-only caps
# are checked in CONTRACT["resources"]["cpu_policy"] (API.md §9.7-§9.8).
def test_measure_only_caps():
    assert "--max-cpu inf --max-wall inf" in nc.CONTRACT["resources"]["cpu_policy"]


def lineage_ctx(tmp_path):
    store = tmp_path / "store"
    for rel in ("hist/HIST_fit_b0.npz", "stages/S1/record.json", "logs/run.log",
                "cpu_ledger.json"):
        put(store / rel, rel.encode("utf-8"))
    put(store / "GATES.jsonl", b'{"gate": "G0"}\n')
    return ndr.Ctx(store=store, worktree=tmp_path, head="0" * 40, job="0130",
                   task_sha256="ab" * 32, session="s", release=None, policy=None,
                   data={}, dry=False)


def test_write_manifest(tmp_path):
    ctx = lineage_ctx(tmp_path)
    path = ndr.write_manifest(ctx, "S1")
    man = json.loads(Path(path).read_text(encoding="utf-8"))
    assert Path(path) == ctx.store / "manifests" / "0130.json"
    assert man["schema"] == "c2nd-manifest-v1" and man["job"] == "0130"
    for rel in ("hist/HIST_fit_b0.npz", "stages/S1/record.json"):
        assert man["files"][rel] == sha(ctx.store / rel)
    assert not [k for k in man["files"] if k.startswith("logs/") or k == "cpu_ledger.json"]
    assert man["append_only"]["GATES.jsonl"] == sha(ctx.store / "GATES.jsonl")
    with pytest.raises(FileExistsError):
        ndr.write_manifest(ctx, "S1")


def test_supersede_and_regen_compare(tmp_path):
    ctx = lineage_ctx(tmp_path)
    rel = "stages/S1/record.json"
    before = sha(ctx.store / rel)
    ruling = {"defect": "d", "ruling_path": "r.md", "ruling_sha256": "cd" * 32}
    dest = Path(ndr.supersede(ctx, "0130", 1, [rel], ruling))
    assert dest == ctx.store / "superseded" / "0130-a1"
    assert not (ctx.store / rel).exists() and sha(dest / rel) == before
    sums = (dest / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    assert sums == [f"{before}  {rel}"]
    assert json.loads((dest / "SUPERSEDED.json").read_text(encoding="utf-8"))["attempt"] == 1
    put(ctx.store / rel, b"regenerated")
    with pytest.raises(Exception):
        ndr.supersede(ctx, "0130", 1, [rel], ruling)  # append-only: no second a1
    assert ndr.regen_compare(ctx, dest / rel, before) is True
    assert ndr.regen_compare(ctx, ctx.store / rel, before) is False


# ---- T-REG-ND, D-0151-1 (here: test_b_registry.py is at 394 of its 400 lines) --------------
def test_parallel_x6zc_rerun_directories(tmp_path, monkeypatch, loads):
    """D-0151-1: the NON_HISTORY names in X6ZC attempt directories stages/<S>-r<k> are listed
    and never opened (PASS); a non-numeric suffix or another name stays INCOMPLETE."""
    monkeypatch.setattr(nc, "SCRATCH_ROOT", tmp_path / "scratch")  # no real scratch read
    store = put(tmp_path / "x6zc-store" / "FREEZE.json", b'{"schema": "frozen"}\n').parent
    names = ("stages/A-r1/qstar_NA.npz", "stages/B-r2/m1/pairs.npz")
    for rel in names:
        put(store / rel, b"x6zc output, never opened")
    res = nrg.source_parallel(store, "x6zc")
    assert res["status"] == "PASS" and not res["digests"], res["status"]
    listed = sorted(str(x["path"]).replace("\\", "/") for x in res["non_history"])
    assert len(listed) == 2 and all(map(str.endswith, listed, names)), listed
    assert not [p for p in loads if p.endswith(names)]  # listed, not read
    for rel in ("stages/A-rx/qstar_NA.npz", "stages/A-r1/other.npz"):
        put(store / rel, b"x6zc output, never opened")
        assert nrg.source_parallel(store, "x6zc")["status"] == "INCONCLUSIVE/REGISTRY_INCOMPLETE"
        (store / rel).unlink()


# ---- T-SIZE (run time; the author never lists tools/c2_nd) -------------------------------------
def test_module_files_and_sizes():
    names = sorted(p.name for p in PKG.glob("*.py"))
    modules = list(nc.CONTRACT["modules"])  # R-0125-1: CONTRACT's list, whatever its length
    assert modules and len(set(modules)) == len(modules), modules
    assert names == sorted(modules), (names, modules)
    assert tuple(nc.MODULES) == tuple(nc.CONTRACT["modules"])
    lines = {n: len((PKG / n).read_text(encoding="utf-8").splitlines()) for n in names}
    assert all(v <= 400 for v in lines.values()), lines
    assert sum(lines.values()) <= 4400
