"""D-2a evaluation: activations at arbitrary positions, model predictions, probes, behaviour and
the per-model stage-3 pass (D2A-FROZEN-v1 §7, §9, §10.1; tools/d2a/API.md §2.4, §4)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d2a_targets as TG  # noqa: E402
import d2a_world as W  # noqa: E402
from d2a_world import d1  # noqa: E402

from topo_pilot.analysis import rbf_bandwidth, rbf_features, rbf_map, standardizer  # noqa: E402
from topo_pilot.contracts import (  # noqa: E402
    Checkpoint, ErrorCode, SeedTree, SequenceLayout, StageFailure)
from topo_pilot.experiment.x4f_probe import nested_ridge  # noqa: E402
from topo_pilot.learner import load_model  # noqa: E402
from topo_pilot.learner.multihorizon import load_multi_horizon  # noqa: E402

HOOKS = ("embed", "resid_post_0", "resid_post_1", "resid_post_2", "resid_post_3",
         "ln_final_out")
PRIMARY_HOOK, N_RBF, BATCH = "resid_post_3", 2048, 512
STRATA = ("t16", "t28", "bin1", "bin2", "bin3")
TARGETS = ("pi", "r8", "T2", "T3")
CONTRAST = ((8, 9), (3, 4))  # (σ2,A)-(σ2,B), (σ0,A)-(σ0,B) in the 25-index of J2


def load_run(run_id: str, step: int, store_root=W.STORE):
    import d2a_train

    rec = json.loads((Path(store_root) / "runs" / f"{run_id}.json").read_text("utf-8"))
    cid = {c["step"]: c["checkpoint_id"] for c in rec["checkpoints"]}[step]
    ckpt = W.open_store(store_root).load(Checkpoint, cid, consumer="experiment")
    H = d2a_train.RUNS[run_id][1]
    return (load_model(ckpt) if H == 1 else load_multi_horizon(ckpt, H)), cid


def _inputs(tokens) -> torch.Tensor:
    return torch.from_numpy(SequenceLayout().model_inputs(np.asarray(tokens), 5))


@torch.no_grad()
def position_activations(model, tokens, rows, positions, hooks=HOOKS) -> dict:
    """``{hook: [n, d]}`` at ``[i, positions[i]]`` of ``tokens[rows]`` (public forward)."""
    model.eval()
    tok, rows, pos = np.asarray(tokens), np.asarray(rows), np.asarray(positions)
    out = {h: [] for h in hooks}
    for i in range(0, rows.size, BATCH):
        x = _inputs(tok[rows[i:i + BATCH]])
        res = model(x, return_hooks=tuple(hooks))
        if i == 0:
            gap = float((res.logits - model(x).logits).abs().max())
            if gap > 1e-5:
                raise StageFailure(ErrorCode.NUMERICAL_FAILURE, "d2a.eval", "hooked_plain", str(gap))
        at = torch.from_numpy(pos[i:i + BATCH].astype(np.int64))
        idx = torch.arange(x.shape[0])
        for h in hooks:
            out[h].append(res.hooks[h][idx, at].double().numpy())
    return {h: np.concatenate(v) if v else np.zeros((0, 0)) for h, v in out.items()}


@torch.no_grad()
def next_symbol_probs(model, tokens) -> np.ndarray:
    model.eval()
    tok = np.asarray(tokens)
    parts = [torch.softmax(model(_inputs(tok[i:i + BATCH])).logits.double(), -1).numpy()
             for i in range(0, tok.shape[0], BATCH)]
    return np.concatenate(parts)


@torch.no_grad()
def direct_two_step(model, tokens, rows, positions, k: int = 2) -> np.ndarray:
    model.eval()
    tok, rows, pos = np.asarray(tokens), np.asarray(rows), np.asarray(positions, dtype=np.int64)
    parts = []
    for i in range(0, rows.size, BATCH):
        lg = model(_inputs(tok[rows[i:i + BATCH]])).joint_logits[k]
        parts.append(torch.softmax(lg[torch.arange(lg.shape[0]), torch.from_numpy(
            pos[i:i + BATCH])].double(), -1).numpy())
    return np.concatenate(parts) if parts else np.zeros((0, 5**k))


@torch.no_grad()
def ar_two_step(model, tokens, rows, positions) -> np.ndarray:
    """``q1(i | h) q1(j | h i)``: w_{t+1} := i, read at index t + 1; no renormalisation."""
    model.eval()
    tok, rows, pos = np.asarray(tokens), np.asarray(rows), np.asarray(positions, dtype=np.int64)
    out = np.zeros((rows.size, 25))
    for i in range(0, rows.size, BATCH):
        base, p = tok[rows[i:i + BATCH]].copy(), pos[i:i + BATCH]
        r = np.arange(base.shape[0])
        q1 = torch.softmax(model(_inputs(base)).logits.double(), -1).numpy()[r, p]
        for s in range(5):
            alt = base.copy()
            alt[r, p] = s  # tokens[:, t] holds w_{t+1}
            q2 = torch.softmax(model(_inputs(alt)).logits.double(), -1).numpy()[r, p + 1]
            out[i + r, 5 * s:5 * s + 5] = q1[:, [s]] * q2
    return out


def shuffle_perm(n: int, scope) -> np.ndarray:
    return SeedTree(W.DATA).generator("d2a", "shuffle", *scope).permutation(n)


def window8_features(tokens, rows, positions) -> np.ndarray:
    tok, pos = np.asarray(tokens)[np.asarray(rows)], np.asarray(positions)
    idx = pos[:, None] - 8 + np.arange(8)[None, :]
    return np.eye(5)[tok[np.arange(tok.shape[0])[:, None], idx]].reshape(tok.shape[0], 40)


def fit(X_cal, Y_cal, panel_cal, X_out, Y_out, family: str, rng_scope=()) -> dict:
    """Linear: nested_ridge unchanged. RBF: the x4f_gates.rbf_probe pattern (F = 2048)."""
    if family == "linear":
        r = nested_ridge(X_cal, Y_cal, panel_cal, X_out, Y_out)
        return {"r2": r.r2, "status": r.r2_status, "lam": r.lam, "fold_mse": r.fold_mse,
                "pred": r.pred_val}
    mean, scale = standardizer(X_cal)
    Xs = (np.asarray(X_cal, float) - mean) / scale
    gen = SeedTree(W.DATA).generator
    ell, status = rbf_bandwidth(Xs, gen("d2a", "rbf_bandwidth", *rng_scope))
    if ell is None:
        return {"r2": None, "status": status, "lam": None, "fold_mse": {}, "pred": None,
                "ell": None}
    om, b = rbf_map(Xs.shape[1], N_RBF, ell, gen("d2a", "rbf", *rng_scope))
    r = nested_ridge(rbf_features(Xs, om, b), Y_cal, panel_cal,
                     rbf_features((np.asarray(X_out, float) - mean) / scale, om, b), Y_out)
    return {"r2": r.r2, "status": r.r2_status, "lam": r.lam, "fold_mse": r.fold_mse,
            "pred": r.pred_val, "ell": ell}


def pair_scores(J_a, J_b, q_a, q_b) -> dict:
    d, dh = np.asarray(J_a) - np.asarray(J_b), np.asarray(q_a) - np.asarray(q_b)
    delta = 0.5 * float(np.abs(d).sum())
    e = 0.5 * float(np.abs(dh - d).sum()) / delta
    tv_pred = 0.5 * float(np.abs(dh).sum())
    tv = [0.5 * float(np.abs(np.asarray(q) - np.asarray(j)).sum())
          for q, j in ((q_a, J_a), (q_b, J_b))]
    return {"Delta": delta, "E_contrast": e, "tv_pred": tv_pred,
            "reproduced": e <= 0.5 and 0.5 * delta <= tv_pred <= 1.5 * delta,
            "abs_resolved": tv[0] < delta / 2 and tv[1] < delta / 2}


def _exact_J(h) -> np.ndarray:
    return np.array([float(v) for row in d1.exact_history(h)["J"] for v in row])


def behaviour_model(model, H: int) -> dict:
    """Canonical pair and registered templates; direct (H >= 2) and AR routes (§9.2-9.3)."""
    pairs = {11: [(d1.H_A, d1.H_B)], 16: W.registered_templates(16),
             28: W.registered_templates(28)}
    out = {"routes": {}, "native": "direct" if H >= 2 else "ar"}
    for route in (("direct", "ar") if H >= 2 else ("ar",)):
        cell = {}
        for t, plist in pairs.items():
            hs = [h for pr in plist for h in pr]
            tok = np.stack([W.pad(h) for h in hs])
            rows, pos = np.arange(len(hs)), np.full(len(hs), t)
            q = (direct_two_step(model, tok, rows, pos) if route == "direct"
                 else ar_two_step(model, tok, rows, pos))
            sc = [pair_scores(_exact_J(a), _exact_J(b), q[2 * i], q[2 * i + 1])
                  for i, (a, b) in enumerate(plist)]
            cell[t] = {"scores": sc, "frac_reproduced": float(np.mean([s["reproduced"]
                                                                       for s in sc]))}
        canon = cell[11]["scores"][0]["reproduced"]
        cell["BEHAVIOUR"] = {11: canon, 16: canon and cell[16]["frac_reproduced"] >= 0.9,
                             28: canon and cell[28]["frac_reproduced"] >= 0.9}
        out["routes"][route] = cell
    return out


def strata_rows(tokens, pool: str) -> dict:
    """{stratum: (rows, positions)} for t = 16, t = 28 and the three bins."""
    bins = W.bin_positions(tokens, pool)
    out = {f"t{t}": (W.decision_rows(tokens, t), None) for t in W.POSITIONS}
    out = {k: (r, np.full(r.size, int(k[1:]))) for k, (r, _) in out.items()}
    for b, _, _ in W.BINS:
        rows = np.flatnonzero(bins[b - 1] > 0)
        out[f"bin{b}"] = (rows, bins[b - 1][rows])
    return out


def targets_for(tokens, rows, pos) -> dict:
    """Probe targets and ceiling features at (rows, positions) (§3, §7.3)."""
    full = np.zeros(np.asarray(tokens).shape[0], dtype=np.int64)
    full[rows] = pos
    got_rows, q = TG.oracle_rows(tokens, full)
    if not np.array_equal(got_rows, np.sort(rows)):
        raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "d2a.eval", "targets", "row mismatch")
    order = np.argsort(np.argsort(rows))
    q = {k: v[order] for k, v in q.items()}
    return {"pi": q["pi"], "r8": q["pi"] - q["pi8"], "T2": q["T2"][:, list(W.S2)],
            "T3": q["T3"][:, list(W.S3)], "b_mix": q["b_mix"],
            "b_CM": np.hstack([q["b_C"], q["b_M"]]), "J2": q["J2"], "J2_half": q["J2_half"],
            "T2_full": q["T2"]}


def contrasts(law, J2_half, T2) -> tuple[np.ndarray, np.ndarray]:
    """(r, d) of §9.4: model two-step law minus J2_half, and T2, on the two A-B contrasts."""
    r = np.stack([(law[:, a] - law[:, b]) - (J2_half[:, a] - J2_half[:, b])
                  for a, b in CONTRAST], 1)
    d = np.stack([T2[:, a] - T2[:, b] for a, b in CONTRAST], 1)
    return r, d


def _hash(a) -> str:
    return hashlib.sha256(np.ascontiguousarray(a, dtype=np.float64).tobytes()).hexdigest()


def model_pass(model_id: str, model, H, data: dict, families=("linear",), shuffle=True,
               cells=None) -> tuple[dict, dict]:
    """One model's probe fits on cal -> test for every (stratum, target, hook) in ``cells``.

    ``data[pool][stratum]`` holds rows, positions, targets; ``data["panel"]`` is the cal panel
    vector. Returns (records, primary predictions). Shuffle fits permute calibration targets
    with the registered stream (per model, stratum, target, hook, family)."""
    recs, preds = {}, {}
    cells = cells or [(s, tg, h) for s in STRATA for tg in TARGETS for h in HOOKS]
    for s in sorted({c[0] for c in cells}):
        cal, test = data["cal"][s], data["test"][s]
        hooks = sorted({c[2] for c in cells if c[0] == s})
        Xc = position_activations(model, data["tok_cal"], cal["rows"], cal["pos"], hooks)
        Xt = position_activations(model, data["tok_test"], test["rows"], test["pos"], hooks)
        panel = data["panel"][cal["rows"]]
        for _, tg, h in [c for c in cells if c[0] == s]:
            for fam in families:
                for kind in (("model", "shuffle") if shuffle else ("model",)):
                    Yc = cal["y"][tg]
                    scope = (model_id, s, tg, h, fam)
                    if kind == "shuffle":
                        Yc = Yc[shuffle_perm(Yc.shape[0], scope)]
                    r = fit(Xc[h], Yc, panel, Xt[h], test["y"][tg], fam, scope)
                    key = f"{kind}|{s}|{tg}|{h}|{fam}"
                    pred = r.pop("pred")
                    recs[key] = dict(r, pred_sha256=None if pred is None else _hash(pred),
                                     n_cal=int(Yc.shape[0]), n_test=int(test["y"][tg].shape[0]))
                    if pred is not None and h == PRIMARY_HOOK and s in ("t16", "t28") \
                            and tg in ("pi", "r8"):
                        preds[key] = pred
                    if pred is not None:
                        recs[key]["_pred"] = pred
    return recs, preds


def model_list() -> list[tuple[str, str, int, int]]:
    """(model id, run id, step, horizon): 12 C/M finals, 2 N finals, 4 step-0 init(s)."""
    import d2a_train as TR

    finals = [(r, r, 10000, TR.RUNS[r][1]) for r in TR.RUNS if not r.endswith("-N")]
    finals += [(r, r, 10000, 3) for r in ("d2a-s1-N", "d2a-s2-N")]
    return finals + [(f"init-s{s}", f"d2a-s{s}-H1", 0, 1) for s in (1, 2, 3, 4)]


def stage3_data(store_root=W.STORE) -> dict:
    """Tokens, strata rows, positions and targets for cal and test (stage 3 only)."""
    data = {"tok_cal": W.load_tokens("cal", store_root), "tok_test": W.load_tokens("test",
                                                                                  store_root)}
    data["panel"] = 1 + np.arange(data["tok_cal"].shape[0]) % 6
    for pool, tok in (("cal", data["tok_cal"]), ("test", data["tok_test"])):
        data[pool] = {}
        for s, (rows, pos) in strata_rows(tok, pool).items():
            y = targets_for(tok, rows, pos)
            data[pool][s] = {"rows": rows, "pos": pos, "y": y}
    return data


def _cells(kind: str) -> list:
    if kind == "full":
        return [(s, tg, h) for s in STRATA for tg in TARGETS for h in HOOKS]
    return [(s, "pi", PRIMARY_HOOK) for s in ("t16", "t28")]


def collect_model(mid, run, step, H, data, store_root=W.STORE) -> dict:
    """One model's stage-3 pass: linear fits (+ shuffle), band-edge and two-step laws."""
    import d2a_decide as DC

    model, cid = load_run(run, step, store_root)
    cm, out = mid.startswith("d2a-") and not mid.endswith("-N"), {"checkpoint_id": cid}
    recs, preds = model_pass(mid, model, H, data, shuffle=not mid.startswith("init"))
    if mid.endswith("-N"):  # validity shuffle at the primary cell only (API §6)
        recs = {k: v for k, v in recs.items() if k.startswith("model") or (
            k.split("|")[2] == "pi" and k.split("|")[3] == PRIMARY_HOOK
            and k.split("|")[1] in ("t16", "t28"))}
    n, cols, keys = data["tok_test"].shape[0], [], []
    for key, r in recs.items():
        p = r.pop("_pred", None)
        if p is not None:
            s, tg = key.split("|")[1:3]
            y = data["test"][s]["y"][tg]
            cols.append(DC.r2_columns(n, data["test"][s]["rows"], y, p,
                                      data["cal"][s]["y"][tg].mean(0)))
            keys.append(key)
    if cols:
        tot = DC.boot_totals(np.hstack(cols), 2000, ("test", "B2000"))
        for i, key in enumerate(keys):
            ci = DC.interval(DC.r2_from_sums(tot[:, 3 * i], tot[:, 3 * i + 1],
                                             tot[:, 3 * i + 2]))
            recs[key]["ci"] = ci
            recs[key]["half_width"] = None if ci is None else (ci[1] - ci[0]) / 2
    out["fits"] = recs
    if cm:
        tok = data["tok_test"]
        be = TG.band_edge_table(tok, next_symbol_probs(model, tok))
        preds.update({f"be|{k}": v for k, v in be.items()})
        for t in W.POSITIONS:
            dt = data["test"][f"t{t}"]
            laws = {"ar": ar_two_step(model, tok, dt["rows"], dt["pos"])}
            if H >= 2:
                laws["direct"] = direct_two_step(model, tok, dt["rows"], dt["pos"])
            for route, law in laws.items():
                r, d = contrasts(law, dt["y"]["J2_half"], dt["y"]["T2_full"])
                preds[f"b2|{route}|t{t}|r"], preds[f"b2|{route}|t{t}|d"] = r, d
        out["behaviour"] = behaviour_model(model, H)
    if mid.endswith("-N"):
        out["pipeline_null"] = pipeline_null(model, store_root)
    return {"record": out, "preds": preds}


def pipeline_null(model, store_root=W.STORE) -> dict:
    """Linear probe from resid_post_3 to the block tag Z_N: fit valN, score testN (§10.1)."""
    import d2a_decide as DC

    tv, tt = W.load_tokens("valN", store_root), W.load_tokens("testN", store_root)
    zv, zt = W.load_private("valN", store_root)[1], W.load_private("testN", store_root)[1]
    out = {}
    for t in W.POSITIONS:
        rv, rt = W.decision_rows(tv, t), W.decision_rows(tt, t)
        Xv = position_activations(model, tv, rv, np.full(rv.size, t), (PRIMARY_HOOK,))
        Xt = position_activations(model, tt, rt, np.full(rt.size, t), (PRIMARY_HOOK,))
        yv, yt = zv[rv].astype(float), zt[rt].astype(float)
        f = fit(Xv[PRIMARY_HOOK], yv, 1 + rv % 6, Xt[PRIMARY_HOOK], yt, "linear")
        cols = DC.r2_columns(tt.shape[0], rt, yt, f["pred"], yv.mean(0))
        tot = DC.boot_totals(cols, 2000, ("testN", "B2000"))
        ci = DC.interval(DC.r2_from_sums(tot[:, 0], tot[:, 1], tot[:, 2]))
        out[t] = {"r2": f["r2"], "lam": f["lam"], "ci": ci, "upper": None if ci is None else ci[1]}
    return out


def oracle_fits(data, store_root=W.STORE) -> dict:
    """window8 (one-hot w_{t-7..t}) and the oracle ceilings on test; positive control on val."""
    out, preds = {}, {}
    for s in STRATA:
        c, t = data["cal"][s], data["test"][s]
        panel = data["panel"][c["rows"]]
        Fc = window8_features(data["tok_cal"], c["rows"], c["pos"])
        Ft = window8_features(data["tok_test"], t["rows"], t["pos"])
        for tg in TARGETS:
            r = fit(Fc, c["y"][tg], panel, Ft, t["y"][tg], "linear")
            preds[f"window8|{s}|{tg}"] = r.pop("pred")
            out[f"window8|{s}|{tg}"] = r
        for name, feat in (("full_belief", "b_mix"), ("world_conditional", "b_CM"),
                           ("J2_to_pi", "J2")):
            r = fit(c["y"][feat], c["y"]["pi"], panel, t["y"][feat], t["y"]["pi"], "linear")
            r.pop("pred")
            out[f"ceiling|{s}|{name}"] = r
    val = W.load_tokens("val", store_root)
    for tt in W.POSITIONS:
        rv = W.decision_rows(val, tt)
        yv, c = targets_for(val, rv, np.full(rv.size, tt)), data["cal"][f"t{tt}"]
        r = fit(c["y"]["b_mix"], c["y"]["pi"], data["panel"][c["rows"]], yv["b_mix"], yv["pi"],
                "linear")
        r.pop("pred")
        out[f"positive_control_val|t{tt}"] = r
    return {"fits": out, "preds": preds}


def secondary(data, P, R, can, store_root=W.STORE) -> dict:
    """API §4 items 5 and 7 under the stage-3 budget: RBF at the primary cells, then the
    descriptive RBF cells, model-major. Anything not admitted is listed as not run."""
    out, not_run = {"rbf_primary": {}, "rbf_descriptive": {}}, []
    todo = [m for m in model_list() if m[0] in P]
    for group, cells, need in (("rbf_primary", _cells("primary"), 900),
                               ("rbf_descriptive", None, 5400)):
        for mid, run, step, H in todo:
            if not can(need):
                not_run.append(f"{group}:{mid}")
                continue
            model = load_run(run, step, store_root)[0]
            sel = cells or [c for c in _cells("full") if c not in _cells("primary")]
            recs, _ = model_pass(mid, model, H, data, ("rbf",), not mid.startswith("init"), sel)
            out[group][mid] = {k: {a: b for a, b in v.items() if a != "_pred"}
                               for k, v in recs.items()}
    return dict(out, not_run=not_run)
