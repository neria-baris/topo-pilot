"""Author A (job 0198): the OF-4 proxy ladder (protocol §2.9 P1 rule, §4.2 OF-4; DRO4) with the
real precision kernels on planted oracle arrays, against a test-side re-computation."""

from __future__ import annotations  # noqa: I001

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402
import hwsu_of as uof  # noqa: E402
import hwsu_driver_of as udr  # noqa: E402
import c1_means  # noqa: E402
import c1_records  # noqa: E402
import numpy as np  # noqa: E402
import precision  # noqa: E402
import pytest  # noqa: E402

SEEDS = uc.DRY_SEEDS_OF
LADDER = (4096, 8192, 16384, 32768)
ORDER = ("ZR010", "ZR030", "Z010", "Z050")


def planted(shift=0.0):
    """The oracle as a model: A°_full = G (Lemma D2); A°_S = 0.3 G + noise. Designed so that the
    response family is first powered at N = 16,384 (ZR010 binds; ZR030 alone would pass at
    8,192) and the share family at N = 8,192."""
    rng = np.random.Generator(np.random.PCG64(19801))
    n = 2048
    G = 1.0 + 3.3 * rng.standard_normal(n)
    A_S = 0.3 * G + 0.2 * rng.standard_normal(n)
    return G, G.copy() + shift, A_S


def make_ctx(tmp_path, G, A_full, A_S, prior="PASS"):
    ctx = udr.build_ctx(tmp_path / "hwsu-dry-of", "0198t", 1, "RES-HWSU-OF", root=tmp_path,
                        mailbox=tmp_path / "agent-handoff", hwsc_store=tmp_path / "hwsc-store",
                        scope=uc.SCOPE_DRY, seeds=SEEDS, dry=True)
    z = np.zeros_like(G)
    ctx.update(sa={"A_full": A_full, "A_S": A_S, "A_G": z, "A_rest": z},
               pc={"G": G, "d": np.zeros((len(G), 36))}, results={"OF-3": prior})
    return ctx


def status(ctx):
    try:
        det = uof.of_4(ctx) or {}
    except c1_records.C1GateFailure as exc:
        return exc.status
    return det.get("status", "PASS")


def my_ladder(G, A_full, A_S):
    """§2.9 P1 rule, single model "oracle", written out with the reused kernels."""
    arrays = {"ZR010": A_full - 0.1 * G, "ZR030": A_full - 0.3 * G,
              "Z010": A_S - 0.1 * G, "Z050": A_S - 0.5 * G}
    mG = float(c1_means.tree_mean(G))
    met, mde = {}, {}
    for name, X in arrays.items():
        alt = (0.10 if name.startswith("ZR") else 0.03) * mG
        sd, _ = precision.sd_b4_draws({"oracle": X}, {"oracle": G}, ["oracle"], SEEDS["p1_sd"],
                                      5000, len(G))
        for N in LADDER:
            e = precision.centered_draws({"oracle": X}, ["oracle"], SEEDS["p1_centred"], 5000, N)
            cfg = {"alpha": 1 / 300, "power": 0.8, "delta": 0.0, "alternative": alt,
                   "projected_N": N}
            s = precision.precision_summary(sd, e, ["oracle"], cfg)
            met[name, N] = s["criterion_met"]
            mde[name, N] = s["models"]["oracle"]["mde_upper"]

    def first(fam):
        ok = [N for N in LADDER if all(met[k, N] for k in fam)]
        return ok[0] if ok else None

    return first(ORDER[:2]), first(ORDER[2:]), met, mde


@pytest.fixture(scope="module")
def reference():
    return my_ladder(*planted())


def test_design_of_the_planted_arrays(reference):
    n_resp, n_share, met, _ = reference
    assert (n_resp, n_share) == (16384, 8192)
    # SPEC-QUESTION: protocol §4.2 OF-4 names only ZR°030 = (1 − 0.30)·G as the response proxy
    # but also says "run the P1 rule of §2.9" (ZR010 and ZR030); API D-12 forms both. On these
    # arrays the two readings differ: ZR030 alone is powered at 8,192, ZR010 only at 16,384.
    assert met["ZR030", 8192] and not met["ZR010", 8192]


def test_of_4_ladder_equals_independent_recomputation(tmp_path, reference):
    G, A_full, A_S = planted()
    ctx = make_ctx(tmp_path, G, A_full, A_S)
    assert status(ctx) == "PASS"
    n_resp, n_share, _, mde = reference
    assert (ctx["N_resp"], ctx["N_share"]) == (n_resp, n_share)
    # API-AMBIGUITY: the layout of ctx["proxy"] is open (OF_REPORT: {array: {N: {mde_upper,
    # power, criterion_met}}}); every recomputed MDE must be present in it.
    flat = []

    def walk(x):
        if isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                walk(v)
        elif isinstance(x, float):
            flat.append(x)

    walk(ctx.get("proxy", {}))
    for key, v in mde.items():
        assert any(f == pytest.approx(v, rel=1e-12) for f in flat), key


def test_shift_of_mean_A_full_changes_nothing(tmp_path, monkeypatch):
    """P1 reads no model mean: shifting A_full (SDs fixed) leaves the alternatives (mean G only)
    and both ladder values unchanged (§5.1 KS-P1, §2.9)."""
    seen = []
    real = precision.precision_summary

    def spy(sd, e, models, cfg):
        seen.append(cfg["alternative"])
        return real(sd, e, models, cfg)

    monkeypatch.setattr(precision, "precision_summary", spy)
    out = []
    for shift in (0.0, 5.0):
        G, A_full, A_S = planted(shift)
        ctx = make_ctx(tmp_path / f"s{int(shift)}", G, A_full, A_S)
        out.append((status(ctx), ctx.get("N_resp"), ctx.get("N_share")))
    assert out[0] == out[1] == ("PASS", 16384, 8192)
    half = len(seen) // 2
    assert seen[:half] == seen[half:]
    mG = float(c1_means.tree_mean(planted()[0]))
    assert sorted(set(round(a / mG, 12) for a in seen)) == [0.03, 0.1]


def test_share_dropped_at_of_3_keeps_response_rule(tmp_path):
    G, A_full, A_S = planted()
    ctx = make_ctx(tmp_path, G, A_full, A_S, prior="SHARE_DROPPED")
    assert status(ctx) == "SHARE_DROPPED"
    assert ctx["N_resp"] == 16384
