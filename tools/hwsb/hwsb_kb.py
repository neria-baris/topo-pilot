"""HWSB known cases KB5-KB7 (API.md §7; protocol §3). Split out of hwsb_known by size;
hwsb_known re-exports kb5, kb6 and kb7. KB5 reads the AUTH-named S3 w* history table of
hws-store (sha256-checked); KB6 regenerates the E4 test split in memory only.
"""

from __future__ import annotations  # noqa: I001  (hwsb_config sets sys.path first)

import hwsb_config as hc
from fractions import Fraction

import c1_means
import hws_oracle
import hwsb_data as hd
import hwsb_eval as he
import numpy as np
import stage_records
from hwsb_known import E4, KC, KNOWN, _ck, _e4_obs, _ok, _read_json

from topo_pilot.activations import ActivationExtractor
from topo_pilot.contracts import SeedTree
from topo_pilot.dataset import DatasetConfig, PanelBuilder
from topo_pilot.oracle import BayesFilter, LastSymbolPosterior, context_gain
from topo_pilot.prediction.metrics import PredictiveMetrics


def kb5(proc_star) -> dict:
    k5 = KC["KB5"]
    rec = _read_json(k5["record"]["path"])
    rec_ok = stage_records.sha256(k5["record"]["path"]) == k5["record"]["sha256"]
    hist_ok = (
        rec.get("hist_sha256") == k5["hist"]["sha256"]
        and stage_records.sha256(k5["hist"]["path"]) == k5["hist"]["sha256"]
    )
    if not (rec_ok and hist_ok):
        raise hc.HwsbStop(KNOWN, "KB5: S3 record or table hash differs")
    with np.load(k5["hist"]["path"], allow_pickle=False) as z:
        tok = np.asarray(z[k5["hist"]["array_key"]])
    q = he.oracle_predictives(proc_star, tok, (1, 4))
    m = he.moments(proc_star, tok)

    def mean(x):
        return float(c1_means.tree_mean(x))

    def c(x):
        return hws_oracle.circ_marginal(x, 6)

    got = {
        "D4": mean(he.d4_rows(m)),
        "GC": mean(hws_oracle.kl_rows(q[32], q[1])),
        "G4": mean(hws_oracle.kl_rows(q[32], q[4])),
        "G4A": mean(hws_oracle.kl_rows(c(q[32]), c(q[4]))),
    }
    tol = float(k5["abs_tol"])
    refs = {}
    for name, path in k5["references"].items():
        v = rec
        for key in path:
            v = v[key]
        refs[name] = float(v)
    ok = all(refs[k] == float(k5["values"][k]) and abs(got[k] - refs[k]) <= tol for k in got)
    return {
        "status": _ok(ok),
        "values": got,
        "references": refs,
        "tolerance": tol,
        "n": int(tok.shape[0]),
    }


def _src_path(proc_w0, obs, index, ckpt):
    model = he.load_float32(ckpt)
    _, logits, _ = ActivationExtractor((hc.SITE,), 256).extract(model, obs, index)
    pos = {int(s): i for i, s in enumerate(obs.sequence_id.tolist())}
    rows = np.array([pos[int(s)] for s in index.sequence_id.tolist()])
    w = np.asarray(obs.tokens)[rows, :32]
    E, T, pi = proc_w0["E_named"][E4], proc_w0["T"], proc_w0["pi"]
    q_C = BayesFilter(T, E, pi).belief_at(w, 32) @ T @ E
    q_last = LastSymbolPosterior(T, E, pi).q_last(w[:, 31])
    p = he.softmax64(logits)
    regret, G_C = PredictiveMetrics.regret(q_C, p), context_gain(q_C, q_last)
    return {"regret": regret, "G_C": G_C, "captured": PredictiveMetrics.captured(regret, G_C)}


def kb6(proc_w0, ckpt100) -> dict:
    k6 = KC["KB6"]
    obs = _e4_obs(
        proc_w0,
        "test",
        k6["ObservationSet_test"]["n"],
        SeedTree(0).generator("data", "test", "cylinder", "overlap", "1.25"),
        "shared",
    )
    rng = SeedTree(0).generator("panels", "cylinder", "overlap", "1.25")
    index = PanelBuilder().build(
        obs, DatasetConfig(**k6["DatasetConfig"]), rng, dataset_id=k6["ObservationSet_test"]["id"]
    )
    ids_ok = (
        _ck(obs) == k6["ObservationSet_test"]["payload_sha256"]
        and _ck(index) == k6["HistoryIndex"]["payload_sha256"]
    )
    perm = proc_w0["perm"][E4]
    canon = hd.canonical32(obs.tokens, perm)
    q = he.oracle_predictives(proc_w0, canon, (1, 4))
    gc = float(c1_means.tree_mean(hws_oracle.kl_rows(q[32], q[1])))
    tol = float(k6["abs_tol"])
    a_ok = abs(gc - float(k6["G_C"])) <= tol
    pos = {int(v): i for i, v in enumerate(obs.sequence_id.tolist())}
    rows = np.array([pos[int(v)] for v in index.sequence_id.tolist()])  # the src batch order
    ci = canon[rows]
    qi = he.oracle_predictives(proc_w0, ci, (1, 4))
    ours = he.b1(qi, he.model_predictive(ckpt100, ci, perm)) if ckpt100 is not None else None
    src = _src_path(proc_w0, obs, index, ckpt100) if ckpt100 is not None else None
    b_ok = ours is not None and all(
        abs(ours[k] - src[k]) <= tol for k in ("regret", "G_C", "captured")
    )
    return {
        "status": _ok(ids_ok and a_ok and b_ok),
        "G_C": gc,
        "G_C_reference": k6["G_C"],
        "ids_ok": ids_ok,
        "stage_b": ours and {k: ours[k] for k in ("regret", "G_C", "captured")},
        "src": src,
        "tolerance": tol,
    }


def kb7(proc_star, val) -> dict:
    import error_bound
    import k4b_scores

    rows = hd.lowest_rows(val["seq_ids"], 4)
    tok = np.asarray(val["canon32"])[rows]
    s = proc_star
    refs = error_bound.reference_moments(
        s["T"], s["E_canon_shared"], s["pi"], s["coords"], tok, Ks=(4, 32)
    )
    m = he.moments(s, tok)
    gap = Fraction(0)
    for i, ref in enumerate(refs):
        for K in (4, 32):
            for c in range(2):
                gap = max(gap, abs(Fraction(float(m[K][i, c])) - Fraction(ref[K][c])))
    mv = he.moments(s, val["canon32"])
    nulls = {
        "m4_phase": k4b_scores.phase_scores(k4b_scores.m4_phase(mv[4]), mv[32], mv[4]),
        "sha_suffix": k4b_scores.phase_scores(k4b_scores.sha_phase(val["canon32"]), mv[32], mv[4]),
    }
    out = {
        name: {
            "mean": float(c1_means.tree_mean(x)),
            "se": float(np.std(x, ddof=1) / np.sqrt(x.size)),
        }
        for name, x in nulls.items()
    }
    return {"status": "REPORTED", "max_moment_gap": gap, "nulls": out}


# ------------------------------------------------------------------------------------ run_kb
