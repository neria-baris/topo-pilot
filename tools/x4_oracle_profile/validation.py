"""Job-0014 pre-freeze numerical validation on the existing histories (via run_profile)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "tests" / "oracle_profile"))

import independent_reference as ref  # noqa: E402
import inputs  # noqa: E402
import oracle_profile as op  # noqa: E402

CFG = inputs.load_config()
OUT = Path(CFG["output_root"])
SPLITS = tuple(CFG["splits"])


from runtime import guard  # noqa: E402


def reference_rows(n: int) -> list[int]:
    return sorted({0, 1, 2, 3, n // 4, n // 2, 3 * n // 4, n - 1})


def decimal_moments(proc, E, suffix) -> tuple[np.ndarray, np.ndarray]:
    post = ref.decimal_suffix_posterior(proc["T"], E, proc["pi"], suffix, CFG["reference_digits"])
    mean = ref.decimal_circular_mean(post, proc["features"])
    return np.array([float(p) for p in post]), np.array([float(v) for v in mean])


def k8_reproduction(proc, cal) -> dict:
    """Recorded calibration B8/V8 from actual T/E/pi/tokens (never cached m8/r8)."""
    tol = CFG["tolerances"]["k8_reproduction_abs"]
    post = {
        K: op.suffix_posterior(proc["T"], proc["E"], proc["pi"], cal["tokens"], K) for K in (8, 32)
    }
    r_old = (post[32] - post[8]) @ proc["features"]  # original posterior-difference form
    r_new = post[32] @ proc["features"] - post[8] @ proc["features"]  # difference of means
    out = {"rows": int(cal["tokens"].shape[0]), "recorded": CFG["k8_recorded"], "tolerance": tol}
    for name, r in (
        ("posterior_difference", r_old),
        ("mean_difference", r_new),
        ("stored_r8", cal["r8"]),
    ):
        sq = np.sum(r * r, axis=1)
        out[name] = {"B8": float(np.mean(np.sqrt(sq))), "V8": float(np.mean(sq))}
        out[name]["abs_err"] = {k: abs(out[name][k] - CFG["k8_recorded"][k]) for k in ("B8", "V8")}
    out["rounding_new_vs_old_max_abs_row"] = float(np.max(np.abs(r_old - r_new)))
    gated = [
        *out["posterior_difference"]["abs_err"].values(),
        *out["mean_difference"]["abs_err"].values(),
    ]
    out["gate"] = "both reconstructed forms within tolerance; stored r8 corroborative only"
    out["status"] = "PASS" if max(gated) <= tol else "HARD_STOP"
    return out


def stored_value_checks(proc, data) -> dict:
    out = {}
    for split, d in data.items():
        guard(f"stored/{split}")
        means = op.posterior_means(
            proc["T"], proc["E"], proc["pi"], d["tokens"], (1, 8, 32), proc["features"]
        )
        errs = {f"m{K}": float(np.max(np.abs(means[K] - d[f"m{K}"]))) for K in (1, 8, 32)}
        errs["r8_vs_stored"] = float(np.max(np.abs((means[32] - means[8]) - d["r8"])))
        errs["stored_r8_vs_stored_m32_minus_m8"] = float(
            np.max(np.abs(d["m32"] - d["m8"] - d["r8"]))
        )
        out[split] = errs
    worst = max(max(v.values()) for v in out.values())
    return {
        "max_abs": out,
        "worst": worst,
        "tolerance": CFG["tolerances"]["stored_values_abs"],
        "status": "PASS" if worst <= CFG["tolerances"]["stored_values_abs"] else "FAIL",
    }


def reference_checks(proc, data) -> dict:
    """Independent Decimal reference on fixed rows, all K; canonical/named; trap detectability."""
    per, worst_post, worst_mean, named, traps = [], 0.0, 0.0, [], []
    for split, d in data.items():
        rows = reference_rows(d["tokens"].shape[0])
        sub = d["tokens"][rows]
        for K in CFG["K_grid"]:
            guard(f"reference/{split}/{K}")
            post = op.suffix_posterior(proc["T"], proc["E"], proc["pi"], sub, K)
            mean = post @ proc["features"]
            for i, row in enumerate(rows):
                rp, rm = decimal_moments(proc, proc["E"], sub[i, -K:])
                ep, em = float(np.max(np.abs(rp - post[i]))), float(np.max(np.abs(rm - mean[i])))
                per.append(
                    {
                        "split": split,
                        "K": K,
                        "row": row,
                        "id": str(d["ids"][row]),
                        "posterior_max_abs": ep,
                        "moment_max_abs": em,
                    }
                )
                worst_post, worst_mean = max(worst_post, ep), max(worst_mean, em)
        for seed, E_named in proc["E_named"].items():
            named_tokens = proc["perm"][seed][sub]
            for K in CFG["named_reference_K"]:
                guard(f"named/{split}/{seed}/{K}")
                prod_named = op.suffix_posterior(proc["T"], E_named, proc["pi"], named_tokens, K)
                prod_canon = op.suffix_posterior(proc["T"], proc["E"], proc["pi"], sub, K)
                ref_err = max(
                    float(
                        np.max(
                            np.abs(
                                decimal_moments(proc, E_named, named_tokens[i, -K:])[0]
                                - prod_canon[i]
                            )
                        )
                    )
                    for i in range(len(rows))
                )
                named.append(
                    {
                        "split": split,
                        "model": seed,
                        "K": K,
                        "production_named_vs_canonical": float(
                            np.max(np.abs(prod_named - prod_canon))
                        ),
                        "decimal_named_vs_production_canonical": ref_err,
                    }
                )
        traps.append(trap_checks(proc, split, sub))
    tol = CFG["tolerances"]
    named_worst = max(
        max(v["production_named_vs_canonical"], v["decimal_named_vs_production_canonical"])
        for v in named
    )
    trap_ok = all(t["min_over_traps"] > tol["trap_min_detectable"] for t in traps)
    ok = (
        worst_post <= tol["reference_max_abs"]
        and worst_mean <= tol["reference_max_abs"]
        and named_worst <= tol["canonical_named_agreement"]
        and trap_ok
    )
    return {
        "rows": per,
        "worst_posterior_max_abs": worst_post,
        "worst_moment_max_abs": worst_mean,
        "named": named,
        "named_worst": named_worst,
        "traps": traps,
        "status": "PASS" if ok else "FAIL",
    }


def trap_checks(proc, split, sub) -> dict:
    """Wrong symbol mapping and an extra trailing transition must be detectable on real rows."""
    K = 8
    correct = op.suffix_posterior(proc["T"], proc["E"], proc["pi"], sub, K)
    seed = next(iter(proc["E_named"]))
    wrong_map = op.suffix_posterior(proc["T"], proc["E_named"][seed], proc["pi"], sub, K)
    extra = correct @ proc["T"]
    out = {
        "split": split,
        "K": K,
        "wrong_symbol_mapping_max_abs": float(np.max(np.abs(wrong_map - correct))),
        "extra_transition_max_abs": float(np.max(np.abs(extra - correct))),
    }
    out["min_over_traps"] = min(
        out["wrong_symbol_mapping_max_abs"], out["extra_transition_max_abs"]
    )
    return out


def source_identity() -> dict:
    import freeze

    dirty = freeze.git(
        freeze.REPO,
        "status",
        "--porcelain",
        "--",
        "tools/x4_oracle_profile",
        "tests/oracle_profile",
    )
    if dirty:
        raise op.ProfileError(f"implementation/test/config paths not committed and clean: {dirty}")
    return {"commit": freeze.git(freeze.REPO, "rev-parse", "HEAD"), "files": freeze.frozen_files()}


def validate() -> int:
    sources = source_identity()
    root = OUT / "validation"
    root.mkdir(exist_ok=True)
    attempt = 1 + max((int(d.name.split("_")[1]) for d in root.glob("attempt_*")), default=0)
    vdir = root / f"attempt_{attempt:02d}"
    vdir.mkdir(exist_ok=False)
    inputs.dump_json(vdir / "SOURCES.json", sources)
    guard("validate/start")
    env = inputs.environment()
    hashes = inputs.verify_input_hashes(CFG)
    proc = inputs.load_process(CFG)
    data = {s: inputs.load_split(CFG, s) for s in SPLITS}
    cross = set(data["calibration"]["ids"].tolist()) & set(data["validation"]["ids"].tolist())
    if cross:
        raise op.ProfileError("IDs shared across splits")
    inputs.dump_json(
        vdir / "IDENTITY.json",
        {
            "environment": env,
            "inputs_sha256": hashes,
            "artifacts": proc["records"],
            "process_checks": proc["process_checks"],
            "identity": proc["identity"],
            "splits": {
                s: {
                    "rows": int(d["tokens"].shape[0]),
                    "tokens_dtype": str(d["tokens"].dtype),
                    "token_min": int(d["tokens"].min()),
                    "token_max": int(d["tokens"].max()),
                    "first_id": str(d["ids"][0]),
                    "last_id": str(d["ids"][-1]),
                }
                for s, d in data.items()
            },
            "ids_unique_within_and_across_splits": True,
            "trajectory_provenance": "rows drawn independently (z1 ~ pi per row, 32 "
            "emissions) by the "
            "frozen x4-history-feas-v1 sampler; streams in input STREAMS.json",
        },
    )
    guard("validate/k8")
    k8 = k8_reproduction(proc, data["calibration"])
    inputs.dump_json(vdir / "K8_REPRODUCTION.json", k8)
    if k8["status"] != "PASS":
        print(json.dumps({"stage": "validate", "status": "HARD_STOP_K8"}))
        return 4
    stored = stored_value_checks(proc, data)
    refs = reference_checks(proc, data)
    status = "PASS" if stored["status"] == refs["status"] == "PASS" else "FAIL"
    if source_identity() != sources:
        status = "FAIL"
        refs["source_changed_during_validation"] = True
    inputs.dump_json(
        vdir / "NUMERICAL_VERIFICATION.json",
        {
            "status": status,
            "stored_values": stored,
            "reference": refs,
            "reference_digits": CFG["reference_digits"],
            "limitation": "selected-row references and enumerated synthetic checks; not a proof of "
            "every floating-point operation",
            "peak_working_set_bytes": inputs.peak_working_set(),
        },
    )
    print(json.dumps({"stage": "validate", "status": status, "k8": k8["status"]}))
    return 0 if status == "PASS" else 5
