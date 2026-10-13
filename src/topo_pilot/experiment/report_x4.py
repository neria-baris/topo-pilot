"""X4 section of the E2 report (secondary; PREREGISTRATION_X4.md), from the X4 MetricRecords.

Interpretation sentences and the blinding disclosure are copied verbatim from
``PREREGISTRATION_X4.md`` (selected by the verdicts, never written here), followed by the
D-040 caveats addendum. Anything missing prints "not run".
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow

from .report import _fmt
from .report_e2 import WORLDS, _latest, _median, _one, _pick

VIEWS = ("V0", "V1", "V2", "V3", "V4", "V5")
VIEW_NAMES = {"V0": "resid_post_3, raw (primary metric)", "V1": "LN-gauge-free u",
              "V2": "ln_final_out", "V3": "readout-visible P_A u", "V4": "readout-null u − P_A u",
              "V5": "softmax(logits), Hellinger"}
X4C_LINE = {"V3_only": "  V3 supported, V4 not", "V4_only": "  V4 supported, V3 not",
            "both": "  both / neither", "neither": "  both / neither"}


def x4_rows(store: ArtifactStore) -> list[MetricRow]:
    ids = _latest(store, MetricRecords, stage="X4", kind="analysis")
    return list(store.load(MetricRecords, ids[0], consumer="experiment").rows) if ids else []


def _verdict(rows: Sequence[MetricRow], space: str, prefix: str, cond: str) -> tuple[str, str]:
    for r in rows:
        if r.space == space and r.condition == cond and r.metric_id.startswith(prefix + "_"):
            return r.metric_id.removeprefix(prefix + "_"), r.uncertainty_kind or ""
    return "not run", ""


def _prereg_line(lines: Sequence[str], prefix: str) -> str:
    return next((ln.strip() for ln in lines if ln.startswith(prefix)), f"({prefix}: not found)")


def _addendum(lines: Sequence[str]) -> list[str]:
    start = next((i for i, ln in enumerate(lines) if ln.startswith("## Addendum")), None)
    return [] if start is None else [ln for ln in lines[start + 1:] if ln.strip()]


def view_table(rows: Sequence[MetricRow], cond: str, final: int) -> list[str]:
    out = ["| view | replicate | S cyl init | S cyl final | S sq init | S sq final "
           "| panels D > 0 | median D | u_r | F1-rule under view |", "|---" * 10 + "|"]
    seeds = sorted({r.replicate for r in rows if r.metric_id == "u" and r.condition == cond})
    for v in VIEWS:
        status, _ = _verdict(rows, f"x4:{v}", "F1rule_verdict", cond)
        for seed in seeds:
            cells = [_median([r.value for r in _pick(rows, f"x4:{v}", "S_H1", world=w,
                                                     replicate=seed, checkpoint=ck,
                                                     condition=cond)])
                     for w in WORLDS for ck in (0, final)]
            n, med, u = (_one(rows, f"x4:{v}", m, replicate=seed, condition=cond)
                         for m in ("n_positive", "median_D", "u"))
            out.append(f"| {v} | {seed} | " + " | ".join(_fmt(c) for c in cells)
                       + f" | {_fmt(n, 0)}/8 | {_fmt(med, 4)} | {_fmt(u, 4)} | {status} |")
    return out


def geometry_lines(rows: Sequence[MetricRow], cond: str) -> list[str]:
    out = ["| view | median Δgeom, all pairs | panels > 0 | median Δgeom, same w₃₂ "
           "| panels > 0 (of ok) |", "|---|---|---|---|---|"]
    for v in VIEWS:
        cells = []
        for m in ("delta_geom_all", "delta_geom_same_last_symbol"):
            vals = [r.value for r in _pick(rows, f"x4:{v}", m, condition=cond)
                    if r.value is not None]
            cells += [_fmt(_median(vals), 3), f"{sum(x > 0 for x in vals)}/{len(vals)}"]
        out.append(f"| {v} | " + " | ".join(cells) + " |")
    return out


def run_table(rows: Sequence[MetricRow], space: str, metric: str, cond: str, digits=0) -> str:
    vals = {(r.world, r.replicate): r.value for r in _pick(rows, space, metric, condition=cond)}
    return ", ".join(f"{w}-{s}: {_fmt(v, digits)}" for (w, s), v in sorted(vals.items())) \
        or "not run"


def x4_section(store: ArtifactStore, prereg: Path, cond: str = "O", final: int = 5000
               ) -> list[str]:
    """Markdown lines of the X4 section (secondary; F1 stays the headline)."""
    rows = x4_rows(store)
    text = prereg.read_text(encoding="utf-8").splitlines() if prereg.is_file() else []
    out = ["## X4 (SECONDARY; PREREGISTRATION_X4.md): representation vs readout geometry", "",
           "Secondary analyses; they never replace the F1 verdict above.", "",
           _prereg_line(text, "Blinding:"), ""]
    if not rows:
        return out + ["X4: not run", ""]
    missing = [f"{r.world}-{r.condition}-{r.replicate}" for r in rows
               if r.metric_id == "run_available"]
    out += ["Missing runs (not run): " + (", ".join(missing) or "none"), "",
            "Views: " + "; ".join(f"{v} = {VIEW_NAMES[v]}" for v in VIEWS) + ".", "",
            "### F1 rule under each view (median S over 8 panels)", "",
            *view_table(rows, cond, final), "", "### Δgeom per view (checkpoint final)", "",
            *geometry_lines(rows, cond), ""]
    checks = {m: max((r.value for r in _pick(rows, "x4:check", m) if r.value is not None),
                     default=None)
              for m in ("ln_reconstruction_max_abs", "logits_from_U_max_abs",
                        "logits_from_visible_max_abs")}
    out += ["Pipeline checks (max over runs and checkpoints): " + "; ".join(
        f"{m} = {_fmt(v, 7)}" for m, v in checks.items()) + ".", ""]
    v0, v1 = (_verdict(rows, f"x4:{v}", "F1rule_verdict", cond)[0] for v in ("V0", "V1"))
    caveat = _one(rows, "x4:a", "X4a_caveat", condition=cond)
    out += ["### X4-a (gauge robustness)", "", _prereg_line(text, "X4-a"), "",
            f"Result: V0 {v0}, V1 {v1}; equal: "
            f"{'yes' if _one(rows, 'x4:a', 'X4a_verdicts_equal', condition=cond) else 'no'}"
            f"; caveat case (V0 supported, V1 not): {'yes' if caveat else 'no'}.", ""]
    b_status, b_reason = _verdict(rows, "x4:b", "X4b_verdict", cond)
    out += ["### X4-b (functional geometry)", "", _prereg_line(text, "X4-b"), "",
            "Positive control, median over panels of ρ_s(d_V5, d_future1) per run: "
            + run_table(rows, "x4:b", "rho_V5_future1_median", cond, 3) + "; passed: "
            + ("yes" if _one(rows, "x4:b", "positive_control_passed", condition=cond)
               else "no") + ".", "",
            f"Result: X4-b {b_status}" + (f" ({b_reason})" if b_reason else "") + ".", ""]
    cat = next((r.metric_id.removeprefix("X4c_") for r in rows if r.space == "x4:c"
                and r.condition == cond and r.metric_id.startswith("X4c_")), None)
    ratios = "; ".join(
        f"{s}: V3 {_fmt(_one(rows, 'x4:c', 'median_D_V3', replicate=s, condition=cond), 4)}, "
        f"V4 {_fmt(_one(rows, 'x4:c', 'median_D_V4', replicate=s, condition=cond), 4)}, "
        f"ratio {_fmt(_one(rows, 'x4:c', 'ratio_V3_V4', replicate=s, condition=cond), 2)}"
        for s in sorted({r.replicate for r in _pick(rows, "x4:c", "median_D_V3")}))
    out += ["### X4-c (where the structure lives)", "", _prereg_line(text, "X4-c"), "",
            f"median_i D per replicate: {ratios or 'not run'}.", "",
            f"Category: {cat or 'not run'}. Pre-registered interpretation: "
            + (_prereg_line(text, X4C_LINE[cat]) if cat else "not run"), ""]
    out += ["### X4-d (same-last-symbol H2 baseline)", "", _prereg_line(text, "X4-d"), ""]
    for a in ("V0", "V1"):
        st, reason = _verdict(rows, f"x4:d:{a}", "X4d_verdict", cond)
        out.append(f"- A = {a}: panels passing per run "
                   f"{run_table(rows, f'x4:d:{a}', 'n_pass', cond)}; X4-d {st}"
                   + (f" ({reason})" if reason else ""))
    out += ["", "### H3′ (approved at H3, D-037; decided under P only)", "",
            _prereg_line(text, "H3′"), "",
            f"Condition {cond}: comparison only (descriptive); the decision needs S5 (P)."]
    for a in ("V0", "V1"):
        st, reason = _verdict(rows, f"x4:h3p:{a}", "H3prime_verdict", cond)
        out.append(f"- A = {a}: panels passing per run "
                   f"{run_table(rows, f'x4:h3p:{a}', 'n_pass', cond)}; rule outcome {st}"
                   + (f" ({reason})" if reason else ""))
    out += ["", "### Interpretation caveats (addendum D-040, fixed before results)", "",
            *_addendum(text), ""]
    return out
