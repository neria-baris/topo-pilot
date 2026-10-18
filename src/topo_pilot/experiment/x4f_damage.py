"""X4-F gates G3-G5 for one model: primary erasure, F-primary family, damage profiles, support
(x4f-exec-v2 §5, §6, §8, §9). Validation regret is never computed here."""

from __future__ import annotations

import numpy as np

from topo_pilot.analysis import (
    apply_map,
    displacements,
    fit_oblique_eraser,
    mismatch_report,
    random_family,
    support_gate,
    support_report,
)

from .x4f_data import ModelData
from .x4f_gates import (
    CONTROLS,
    G3_LINEAR,
    G3_RBF_LABEL,
    ValForward,
    gen,
    probe,
    rbf_probe,
)


def g3(d: ModelData, wh, primary, checkpoint=lambda _: None) -> dict:
    """Primary eraser validity and post-erasure linear / RBF recoverability of m32."""
    out = {"whitening_k": wh.k, "whitening_status": wh.status, "rank": primary.rank,
           "eraser_status": primary.status, "checks": primary.checks}
    if primary.status != "ok":
        out["status"] = "INCONCLUSIVE:" + primary.status
        return out
    h, m32 = d.acts["resid_post_1"], d.targets["m32"]
    hp = apply_map(h, primary.mu, primary.M)
    out["linear"] = probe(d, hp, m32, checkpoint=checkpoint)
    out["rbf"] = rbf_probe(d, hp[d.cal], hp[d.val], m32[d.cal], m32[d.val], checkpoint)
    r2 = out["linear"]["r2"]
    if r2 is None:
        out["status"] = "INCONCLUSIVE:R2_UNDEFINED_ZERO_VARIANCE"
        return out
    out["status"] = "PASS" if r2 <= G3_LINEAR else "FAIL"
    rbf = out["rbf"]["r2"]
    out["label"] = ("LINEAR_COMPONENT_ONLY" if rbf is not None and rbf >= G3_RBF_LABEL else
                    "RBF_UNKNOWN_DEGENERATE" if rbf is None else "none")
    return out


def _profile(d: ModelData, vf: ValForward, mu, M, base_q1: dict, d_primary_val, scale,
             checkpoint=lambda _: None) -> dict:
    """Damage profile of one map on validation (units kept separate)."""
    h, t = d.acts["resid_post_1"], d.targets
    hp = apply_map(h, mu, M)
    q1 = probe(d, hp, t["Q1"], checkpoint=checkpoint)
    lin = probe(d, hp, t["m32"], checkpoint=checkpoint)
    rbf = rbf_probe(d, hp[d.cal], hp[d.val], t["m32"][d.cal], t["m32"][d.val], checkpoint)
    checkpoint("damage model forward")
    kl, kl_status = vf.kl(vf.patch("resid_post_1", hp[d.val]))
    checkpoint("damage model forward complete")
    dv = displacements(h[d.val], hp[d.val])
    return {"dR2_Q1": (None if base_q1["r2"] is None or q1["r2"] is None
                       else base_q1["r2"] - q1["r2"]),
            "r2_m32_linear": lin["r2"], "r2_m32_rbf": rbf["r2"], "rbf_status": rbf["status"],
            "kl_output_nats": kl, "kl_status": kl_status,
            "disp_cal_mean": float(np.mean(displacements(h[d.cal], hp[d.cal]))),
            "disp_val": mismatch_report(d_primary_val, dv, scale),
            "patched_val": hp[d.val]}


def g4(d: ModelData, vf: ValForward, wh, primary, controls: dict,
       checkpoint=lambda _: None) -> tuple[dict, dict]:
    """F-primary construction plus damage profiles; returns (gate record, patched clouds)."""
    h = d.acts["resid_post_1"]
    hp_cal = apply_map(h[d.cal], primary.mu, primary.M)
    target = float(np.mean(displacements(h[d.cal], hp_cal)))
    fam = random_family(h[d.cal], wh, primary.rank, target,
                        lambda j: gen("random_eraser", "F-primary", d.seed, j),
                        checkpoint=checkpoint)
    out = {"target_disp_cal": target, "family_status": fam.status, "n_draws": fam.n_draws,
           "n_degenerate": fam.n_degenerate_draws, "accepted": fam.accepted_draws,
           "family_disp_cal": fam.mean_displacements}
    maps = {"primary": (primary.mu, primary.M, primary.rank, "ok")}
    maps.update({f"random_{j}": (wh.mu, M, primary.rank, "ok")
                 for j, M in zip(fam.accepted_draws, fam.maps)})
    for name in CONTROLS:
        checkpoint(f"control map {name}")
        er = fit_oblique_eraser(h[d.cal], controls[name][d.cal], wh)
        maps[name] = (er.mu, er.M, er.rank, er.status)
        out[f"control_{name}"] = {"rank": er.rank, "status": er.status, "checks": er.checks}
    out["_maps"] = maps
    if fam.status != "ok":
        out["status"] = "INCONCLUSIVE:" + fam.status
        return out, {}
    scale = float(np.mean(np.linalg.norm(h[d.val] - h[d.cal].mean(axis=0), axis=1)))
    d_prim = displacements(h[d.val], apply_map(h[d.val], primary.mu, primary.M))
    base_q1 = probe(d, h, d.targets["Q1"], checkpoint=checkpoint)
    out["base_r2_Q1"] = base_q1["r2"]
    prof, clouds = {}, {}
    for name, (mu, M, rank, status) in maps.items():
        checkpoint(f"damage profile {name}")
        if status != "ok":
            prof[name] = {"status": status, "rank": rank}
            continue
        p = _profile(d, vf, mu, M, base_q1, d_prim, scale, checkpoint)
        clouds[name] = p.pop("patched_val")
        prof[name] = {"status": "ok", "rank": rank, **p,
                      "matched_to_primary": rank == primary.rank and abs(
                          p["disp_cal_mean"] - target) <= 0.05 * target}
    out["profiles"] = prof
    g = prof.get("generic", {})
    out["S1_eligible"] = (None if g.get("status") != "ok" or prof["primary"]["dR2_Q1"] is None
                          or g.get("dR2_Q1") is None
                          else prof["primary"]["dR2_Q1"] <= g["dR2_Q1"])
    out["status"] = "PASS" if prof["primary"]["dR2_Q1"] is not None else \
        "INCONCLUSIVE:PRIMARY_PROFILE_UNDEFINED"
    return out, clouds


def g5(d: ModelData, clouds: dict) -> dict:
    """Mahalanobis support of patched validation vectors (primary vs its F-primary family)."""
    h = d.acts["resid_post_1"]
    rep = support_report(h[d.cal], h[d.val], clouds)
    if rep["status"] != "ok":
        return {"status": "INCONCLUSIVE:" + rep["status"], "report": rep}
    fr = [v for k, v in rep["frac"].items() if k.startswith("random_")]
    passed = support_gate(rep["frac"]["primary"], fr)
    return {"status": "PASS" if passed else "FAIL", "report": rep,
            "frac_primary": rep["frac"]["primary"], "median_random": float(np.median(fr))}
