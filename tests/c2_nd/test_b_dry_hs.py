"""Author B, regression for D-0158-1 (job 0159): the dry-run planted circle is history-sensitive.

Written from API.md section 11 (nd_dry), section 20.11 (ND-C59, the belief chart), sections 8.3
and 10 (stage helpers, known cases) and protocol 10.1 / 5.1-5.3 only. On a reduced dry fixture
(sequence blocks of 1,024 rows; DFIT 4,096 rows; DFEAS and DVAL one block each) the stage helpers
are called directly, in gate order, on one planted store:

  PREP -> H2 -> H3 -> M0-D -> F1 -> R1 -> V3x' -> KC -> KC-R -> the D stream on DVAL.

The registry is replaced by a stub (it scans scratch stores; the registry is not what is tested).
Everything lives under pytest's tmp_path (a test_ path). One module-scope run feeds all tests."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if sys.path[:1] != [str(REPO / "tools" / "c2_nd")]:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first, API.md section 1 "Test imports")

# isort: split
import nd_attrib as nat  # noqa: E402
import nd_decide as ndc  # noqa: E402
import nd_driver as ndr  # noqa: E402
import nd_dry  # noqa: E402
import nd_registry as nrg  # noqa: E402
import nd_split as sp  # noqa: E402
import nd_stage_base as sb  # noqa: E402
import nd_stage_pre as pre  # noqa: E402
import nd_stage_val as sv  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

ORDER = tuple(ndr.GATE_ORDER)
R1_MIN = 0.80  # the R1 gate passes at 3/4 (API.md 20.11); require a clear margin above it
KNOWN_D = {"D0": "USED", "DONLY": "USED", "DDOSE": "PARTIAL"}


def at(ctx, gate):
    """A fresh policy positioned at `gate` (the earlier gates counted as done)."""
    ctx.policy = ndr.LogitPolicy(done=ORDER[: ORDER.index(gate)])
    ctx.policy.begin(gate)


def d_null_family(ctx):
    """The planted D-NULL on DVAL: d_stream arrays under the refit projector RD, bounds (C2
    bootstrap, seed name val_p1_sd), then nd_decide.d_model per model and the family rule."""
    per = {}
    for j in nc.MODELS:
        arrays, _, _ = sv._fam_arrays(ctx, "D", j)
        Q = ctx.data["sealD"][j]["Q"]
        geo = dict(Q["geo"], proj={"": (Q["P"]["P_S"], Q["P"]["delta"])})
        guards = nat.d_guards(arrays, geo, None)
        keyed = {f"{k}|{j}": v for k, v in arrays.items()}
        b = sp.bounds(keyed, {f"{k}|{j}": g for k, g in guards.items()}, "val_p1_sd")
        per[j] = ndc.d_model(sp.split_b(b, j), False)
    status = {j: r["status"] for j, r in per.items()}
    return status, ndc.overall("D", status, [])


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    mp = pytest.MonkeyPatch()
    mp.setattr(nc, "BLOCK", 1024)
    mp.setattr(nc, "SPLIT_BLOCKS", {"fit": 4, "feas": 1, "val": 1})
    mp.setattr(nrg, "load", lambda *a, **k: None)
    mp.setattr(nrg, "separation", lambda *a, **k: {"status": "PASS"})
    root = tmp_path_factory.mktemp("test_dry_hs")
    mp.setattr(nc, "SCRATCH_ROOT", root)  # a dry-run store lies under SCRATCH_ROOT (API.md 11)
    store = root / "store"
    store.mkdir()
    own = {k: "x" for k in ndr.OWNER} | {"sha256": nc.AUTH_SHA256}
    auth = {k: "x" for k in ndr.AUTH_KEYS} | {
        "schema": ndr.SCHEMA["AUTH_IMPL.json"],
        "protocol_sha256": nc.PROTOCOL_SHA256,
        "owner_record": own,
        "budget": {"central_cpu_h": 1},
    }
    (store / "AUTH_IMPL.json").write_text(json.dumps(auth), encoding="utf-8")
    ctx = ndr.Ctx(store=store, worktree=REPO, head="c0ffee", job="0159b", task_sha256="ab" * 32,
                  session="sess-b", release=None, policy=ndr.LogitPolicy(), data={}, dry=True)
    out = {"ctx": ctx}
    try:
        nd_dry.prepare(ctx)
        for gate, step in (("H2", pre.h2), ("H3", pre.h3)):
            at(ctx, gate)
            out[gate] = step(ctx)
        at(ctx, "M0-D")
        out["M0-D"] = pre.m0d(ctx)
        at(ctx, "F1")
        out["F1"] = pre.f1(ctx)
        at(ctx, "R1")
        out["R1"] = pre.r1(ctx)
        at(ctx, "V3x'")
        out["V3x'"] = sv.v3x_d(ctx)
        at(ctx, "KC")
        out["KC"] = sv.kc_eval(ctx, "val", "val_KC", nc.KC_CASES)
        at(ctx, "KC-R")
        out["KC-R"] = sv.kc_eval(ctx, "val", "val_KC", nc.KCR_CASES)
        at(ctx, "P1")
        out["D-stream"] = d_null_family(ctx)
        yield out
    finally:
        mp.undo()


def test_belief_chart_files(run):
    """ND-C59: c2/charts/CHART_<j>_dry.npz holds mu (d_model) and U (2 x 128) only."""
    c2 = Path(run["ctx"].store) / "c2" / "charts"
    for j in nc.MODELS:
        with np.load(c2 / f"CHART_{j}_dry.npz", allow_pickle=False) as z:
            assert sorted(z.files) == ["U", "mu"]
            assert z["U"].shape == (2, 128) and z["mu"].shape == (128,)
            assert np.isfinite(z["U"]).all() and np.linalg.norm(z["U"]) > 0


def test_fixture_reaches_r1(run):
    """The stages before R1 record PASS on the planted models (the 0158 run stopped only at R1)."""
    assert run["H2"]["status"] == "PASS" and run["H3"]["status"] == "PASS"
    assert [r["status"] for r in run["M0-D"]["records"]] == ["PASS"] * 3
    f1 = run["F1"]["records"]
    assert len(f1) == 6 and {r["status"] for r in f1} == {"PASS"}
    assert {r["problem"] for r in f1} == {"RD", "RT"}


def test_r1_passes_on_every_planted_model(run):
    """Pass criterion 2 of 10.1 / D-0158-1: the planted models are R1-history-sensitive, for every
    model and family (N-R, D, N-M) and for the report-only R@T problem of D (0158 gave CNHS on
    all 12 rows at agreement 0.43-0.58)."""
    recs = run["R1"]["records"]
    assert len(recs) == 12
    assert {(r["model"], r["family"]) for r in recs if "problem" not in r} == {
        (j, f) for j in nc.MODELS for f in nc.FAMILIES
    }
    for r in recs:
        who = (r["model"], r["family"], r.get("problem"))
        assert r["status"] == "PASS", who
        v = r["values"]
        assert v["agreement"] >= R1_MIN, (who, v["agreement"])
        assert v["kappa_reg"] > 0, (who, v["kappa_reg"])


def test_d_only_is_necessary(run):
    """KC (8.3): D0 USED, D-ONLY USED and NECESSARY, D-DOSE PARTIAL and NOT_NECESSARY. No model
    contradicts a known case; at least two models (the 2-of-3 rule) pass every case, and D-ONLY's
    N-R category on its own keys is NECESSARY."""
    kc = run["KC"]
    assert set(kc) == set(nc.MODELS)
    for j, res in kc.items():
        assert set(res) == set(KNOWN_D) and "CONTRADICTED" not in res.values(), (j, res)
    assert sum(all(v == "PASS" for v in r.values()) for r in kc.values()) >= 2
    seen = 0
    for (split, cases, j), (_, b) in run["ctx"].data["sealKC"].items():
        if cases != nc.KC_CASES:
            continue
        own = {k.split(":", 1)[1]: v for k, v in b.items() if k.startswith("DONLY:")}
        st = ndc.nr_model(own, False)["status"]
        assert st in ("NECESSARY", "INC", "INC/NUMERICAL"), (j, st)  # never another category
        seen += st == "NECESSARY"
    assert seen >= 2


def test_d_null_is_not_used(run):
    """The planted D-NULL: (a) KC-R, the coordinate decoys D-NULL-R NOT_USED and D-ID USED, never
    contradicted, at least two models PASS; (b) the D stream on DVAL gives DECOY_NOT_USED per
    model (INC allowed per model at reduced size, 20.11 Test) and DECOY_NOT_USED for the family;
    no model says DECOY_USED, DECOY_PARTIAL or DECOY_LOW_ALIGNED."""
    kcr = run["KC-R"]
    for j, res in kcr.items():
        assert set(res) == {"DNULLR", "DID"} and "CONTRADICTED" not in res.values(), (j, res)
    assert sum(all(v == "PASS" for v in r.values()) for r in kcr.values()) >= 2
    assert all(r["status"] == "PASS" for r in run["V3x'"]["records"])  # D-NULL headroom (V3x')
    status, overall = run["D-stream"]
    assert set(status.values()) <= {"DECOY_NOT_USED", "INC", "INC/NUMERICAL"}, status
    assert sum(s == "DECOY_NOT_USED" for s in status.values()) >= 2, status
    assert overall == "DECOY_NOT_USED"
