"""Implementer test, D-0158-1 (job 0159; API.md §20.11 ND-C59; protocol §10.1 criterion 2).

The dry fixture at reduced size (blocks of 1,024 rows instead of 4,096, with four panels per
block as at full size) in a scratch store under tmp_path. The stage helpers themselves run
(nd_dry.prepare, nd_split.h3_run's oracle writer, nd_stage_pre.m0d, f1, r1,
nd_stage_val.v3x_d, y1_d, kc, kc_r, nd_stage_post.stream) with a policy opened at each
gate. Skipped as not part of D-0158-1: C2's H3 identity check and nd_dry.checks (pass
criteria 3 and 5). The D bounds use the TEST level with the VAL draw count.
Expected: the planted circle is history-sensitive (R1 PASS with margin on every model and
problem), M0-D passes on every decoy (D-NULL-R's X1 attainability included), the known cases
return their constructed answers (KC: D0 USED, D-ONLY USED and NECESSARY, D-DOSE PARTIAL and
NOT_NECESSARY; KC-R: D-NULL-R NOT_USED, D-ID USED) and the D stream at the TEST level gives
D-NULL DECOY_NOT_USED. Run time about six minutes (one module fixture)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if sys.path[:1] != [str(REPO / "tools" / "c2_nd")]:
    sys.path.insert(0, str(REPO / "tools" / "c2_nd"))

import nd_config as nc  # noqa: E402  (first, API.md §1 "Test imports")

# isort: split
import c1_data  # noqa: E402
import c2_data as cd  # noqa: E402
import c2_oracle as co2  # noqa: E402
import nd_data as nda  # noqa: E402
import nd_decide as ndc  # noqa: E402
import nd_driver as ndr  # noqa: E402
import nd_dry  # noqa: E402
import nd_split as sp  # noqa: E402
import nd_stage_base as sb  # noqa: E402
import nd_stage_post as post  # noqa: E402
import nd_stage_pre as pre  # noqa: E402
import nd_stage_val as sv  # noqa: E402
import numpy as np  # noqa: E402
import pytest  # noqa: E402

BLOCK, SPLITS = 1024, {"fit": 4, "feas": 1, "val": 1, "test": 1}  # DFIT 4,096 rows (leak)
R1_MARGIN = 0.80  # R1 passes at 3/4; full size gives 0.86-0.87 (job 0159)


def panels(seq_ids, block):
    """c1_data.panels with 1,024 replaced by BLOCK / 4: four panels per block, as at 4,096."""
    seq_ids = np.asarray(seq_ids, dtype=np.int64)
    rank = np.empty(len(seq_ids), dtype=np.int64)
    rank[np.argsort(seq_ids, kind="stable")] = np.arange(len(seq_ids))
    return 4 * int(block) + rank // (BLOCK // 4)


def at(ctx, gate):
    """A policy opened at `gate` with every earlier gate done."""
    ctx.policy = ndr.LogitPolicy(done=ndr.GATE_ORDER[: ndr.GATE_ORDER.index(gate)])
    ctx.policy.begin(gate)
    return ctx


@pytest.fixture(scope="module")
def world(tmp_path_factory):
    store = tmp_path_factory.mktemp("dry_hs") / "dry"
    store.mkdir()
    mp = pytest.MonkeyPatch()
    mp.setattr(nc, "BLOCK", BLOCK)
    mp.setattr(c1_data, "panels", panels)
    mp.setattr(ndr, "is_dry_store", lambda s: Path(s) == store)
    mp.setattr(co2, "h3", lambda *a, **k: {"status": "PASS"})
    mp.setattr(nd_dry, "checks", lambda *a, **k: {})  # pass criteria 3, 5: not D-0158-1
    ctx = ndr.Ctx(store=store, worktree=REPO, head="0" * 40, job="t0159", task_sha256="0" * 64,
                  session="test", dry=True)
    try:
        nd_dry.prepare(ctx)
        P = sb.proc(ctx)
        T, E, pi, co = P["T"], P["E_canon"][nc.MODELS[0]], P["pi"], P["coords"]
        for s, nb in SPLITS.items():
            canon, ids, panel = nda.sample_split(T, E, pi, s, nb, nc.DRY_SCOPE)
            oH = ctx.data[f"oH:{s}"] = co2.oracle_role(T, E, pi, canon, co)
            t = cd.history_table(canon, ids, panel, cd.k_y(oH["b31"], co))
            for b in range(nb):
                sl = slice(b * BLOCK, (b + 1) * BLOCK)
                sb.put(ctx, f"hist/HIST_{s}_b{b}.npz", **{k: v[sl] for k, v in t.items()})
        sp.h3_run(ctx, tuple(SPLITS))
        out = {"m0d": pre.m0d(at(ctx, "M0-D"))["records"]}
        out["f1"] = pre.f1(at(ctx, "F1"))["records"]
        out["r1"] = pre.r1(at(ctx, "R1"))["records"]
        out["planted"] = sb.c2js(ctx, "manifests/0115.json")["planted"]
        sv.v3x_d(at(ctx, "V3x'"))
        y1 = sv.y1_d(at(ctx, "Y1'"))["records"]
        out["y_on"] = {j: sv.y_on(ctx, j, "V3yD") for j in nc.MODELS}
        out["y1"] = {r["model"]: r["status"] for r in y1}
        out["kc"] = sv.kc(at(ctx, "KC"))["records"]
        out["kcr"] = sv.kc_r(at(ctx, "KC-R"))["records"]
        per = {j: post.stream(ctx, j, "D")[:2] for j in nc.MODELS}
        b = sp.bounds(*post.keyed(per), "test_D", nc.ALPHA["D"], nc.VAL_DRAWS)
        out["d"] = {}
        for j in nc.MODELS:
            bj = sp.split_b(b, j)
            r = ndc.d_model(bj, out["y_on"][j])
            out["d"][j] = (r["status"], ndc.dnullr_category(bj, r))
        yield out
    finally:
        mp.undo()


def test_planted_code_carries_the_contrast(world):
    """Before rescaling, the head's code part carries a substantial share of the oracle
    contrast (E[A_S] > 0.3 E[G]; 0158: 0.06-0.12 of 1.13), so the code is not amplified 8-15x."""
    for j, r in world["planted"].items():
        assert r["mean_AS0"] > 0.3 * r["mean_G"], (j, r)
        assert 0 < r["a_code"] < 3, (j, r)


def test_r1_history_sensitive_with_margin(world):
    """R1 PASS on N-R (R), D (R), N-M (M) and the report-only D refit RT, every model."""
    recs = world["r1"]
    assert len(recs) == 3 * len(nc.MODELS) + len(nc.MODELS), recs
    for r in recs:
        assert r["status"] == "PASS", r
        assert r["values"]["agreement"] >= R1_MARGIN, r
        assert r["values"]["kappa_reg"] > 0, r


def test_m0d_every_decoy_passes(world):
    """No INCONCLUSIVE/NUMERICAL D-NULL-R row: (viii) holds for every decoy (D-0158-1)."""
    recs = world["m0d"]
    assert [r["status"] for r in recs] == ["PASS"] * len(nc.MODELS), recs
    for r in recs:
        assert all(r["values"]["checks"].values()), r
        kap = {k: v["kappa_x1"] for k, v in r["values"]["values"].items() if "kappa_x1" in v}
        assert set(kap) == set(nc.HEAD_EDITS + nc.COORD_DECOYS), kap
        assert max(kap.values()) < 1.76e3, kap


def test_refits_pass(world):
    assert {r["status"] for r in world["f1"]} == {"PASS"}, world["f1"]
    assert {r["problem"] for r in world["f1"]} == set(nc.REFITS)


def test_known_cases_return_their_constructed_answers(world):
    """KC: D0 USED; D-ONLY USED and NECESSARY; D-DOSE PARTIAL and NOT_NECESSARY. KC-R:
    D-NULL-R NOT_USED, D-ID USED. PASS per case means the declared category is the known one."""
    for name, cases in (("kc", nc.KC_CASES), ("kcr", nc.KCR_CASES)):
        recs = world[name]
        assert sorted(r["model"] for r in recs) == sorted(nc.MODELS), recs
        for r in recs:
            assert r["status"] == "PASS", r
            assert r["values"]["cases"] == {c: "PASS" for c in cases}, r


def test_dnull_not_used_at_test_level(world):
    """The D stream at the TEST level (alpha 1/300; VAL draw count; Y1' as at S4): no model
    declares D-NULL (or the report-only D-NULL-R) anything but NOT_USED, and the family
    outcome is DECOY_NOT_USED. At this reduced size one model may stay INC (an interval
    across a threshold); at full size all three are NOT_USED (job 0159 run)."""
    assert all(world["y1"].get(j, "NOT_RUN") in ("PASS", "NOT_RUN") for j in nc.MODELS)
    for k in (0, 1):
        st = {j: world["d"][j][k] for j in nc.MODELS}
        assert set(st.values()) <= {"DECOY_NOT_USED", "INC"}, st
        assert ndc.overall("D", st, []) == "DECOY_NOT_USED", st
