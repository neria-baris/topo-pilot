"""Report for exit level E3 (S5 + S6, with X4 under O and P), from MetricRecords only.

``topo-pilot report --level E3`` writes ``reports/E3/``:

- ``summary.md``: the primary hypotheses first (H3 = the F1 rule under P; H4 = the D-034 rule
  over the cylinder runs under O), then the approved decision rule H3′ (D-037), then the
  secondary X4 verdicts under O and P side by side, then descriptive S6 material (checkpoint
  times, checkpoint-order null, layer sweep, V1/V5 curves) and the comparison with E2;
- ``condition_P.md``: the full S5 tables in the E2 layout, with the X4 section for P;
- ``fig_dynamics.png`` and ``fig_x4_curves.png`` (panel 1, 12 checkpoints).

Rule texts are quoted verbatim from ``PREREGISTRATION.md`` and ``state/DECISIONS.md``; the
reading of each status is fixed below, before any S5 result existed. Missing data prints
"not run", never a number.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from topo_pilot.contracts import ArtifactStore, MetricRecords, MetricRow

from .report import GRID, INK, INK_MUTED, _fmt
from .report_e2 import (
    SURFACE,
    WORLDS,
    _latest,
    _median,
    _one,
    _pick,
    analysis_rows,
    build_e2,
    replicates,
    verdict,
)
from .report_x4 import _prereg_line, _verdict, run_table, x4_rows, x4_section

WORLD_COLOR = {"cylinder": "#2a78d6", "square": "#eb6834"}
HOOKS = ("embed", "resid_post_0", "resid_post_1", "resid_post_2", "resid_post_3",
         "ln_final_out", "concat")
H3_READING = {
    "SUPPORTED": "H3 supported: the F1 rule holds under P with every learning gate passed.",
    "REJECTED": "The F1 rule fails under P although every learning gate passed. Pre-registered "
                "one-sided reading (PREREGISTRATION §3, conductor note below): this outcome is "
                "expected even for the ideal predictor and is NOT read as evidence that the "
                "structure comes from emission geometry; H3 is uninformative in this direction.",
    "INCONCLUSIVE": "H3 inconclusive; the reason is named above.",
    "not run": "H3 not run (S5 analysis missing).",
}
H4_READING = {
    "SUPPORTED": "H4 supported: in every cylinder run under O, S first exceeds S_0 + u_r at or "
                 "after the first checkpoint with regret < G_C.",
    "REJECTED": "H4 rejected: in at least one cylinder run under O, S rose before history use, "
                "with every learning gate passed.",
    "INCONCLUSIVE": "H4 inconclusive; the run classes are named above.",
    "not run": "H4 not run (S6 dynamics missing).",
}


def s6_rows(store: ArtifactStore, kind: str, cond: str) -> list[MetricRow]:
    """Rows of the newest S6 record of ``kind`` (dynamics / layers / x4curves) for ``cond``."""
    ids = _latest(store, MetricRecords, stage="S6", kind=kind, condition=cond)
    return list(store.load(MetricRecords, ids[0], consumer="experiment").rows) if ids else []


def h4_status(rows: Sequence[MetricRow]) -> tuple[str, str]:
    for r in rows:
        if r.space == "H4" and r.metric_id.startswith("H4_verdict_"):
            return r.metric_id.removeprefix("H4_verdict_"), r.uncertainty_kind or ""
    return "not run", ""


def _runs(rows: Sequence[MetricRow], space: str, metric: str) -> list[tuple[int, str]]:
    return sorted({(r.replicate, r.world) for r in _pick(rows, space, metric)})


def h4_table(dyn: Sequence[MetricRow], curves: Sequence[MetricRow]) -> list[str]:
    """Per run: G_C, u_r, t_history, t_rise (V0; and V1/V5, descriptive), D-034 class and the
    checkpoint-order null (descriptive)."""
    lines = ["| run | G_C | u_r | t_history | t_rise (V0) | D-034 class | t_rise V1 | t_rise V5 "
             "| order-null share first third | order-null p |", "|---" * 10 + "|"]
    for seed, world in _runs(dyn, "dyn", "t_history"):
        kw = {"world": world, "replicate": seed}
        cls = next((r.uncertainty_kind for r in _pick(dyn, "dyn", "h4_consistent", **kw)), None)
        t_v = [_one(curves, f"dyn:x4:{v}", "t_rise", **kw) for v in ("V1", "V5")]
        lines.append(
            f"| {world}-{seed} | {_fmt(_one(dyn, 'dyn', 'G_C', **kw), 4)} "
            f"| {_fmt(_one(dyn, 'dyn', 'u_r', **kw), 4)} "
            f"| {_step(_one(dyn, 'dyn', 't_history', **kw))} "
            f"| {_step(_one(dyn, 'dyn', 't_rise', **kw))} | {cls or 'not run'} "
            + " ".join(f"| {_step(t) if curves else 'not run'}" for t in t_v)
            + f" | {_fmt(_one(dyn, 'dyn', 'order_null_first_third_share', **kw), 3)} "
            f"| {_fmt(_one(dyn, 'dyn', 'order_null_p', **kw), 3)} |")
    return lines


def _step(t: float | None) -> str:
    return "never" if t is None else f"{t:.0f}"


def layer_table(by_cond: dict[str, Sequence[MetricRow]]) -> list[str]:
    """Layer sweep (descriptive): per hook and condition, median D, panels D > 0 and u_r per
    replicate."""
    lines = ["| hook | condition | median D per replicate | panels D > 0 | u_r per replicate "
             "| replicates with median D > u_r |", "|---|---|---|---|---|---|"]
    for hook in HOOKS:
        for cond, rows in by_cond.items():
            seeds = sorted({r.replicate for r in _pick(rows, f"layer:{hook}", "median_D")})
            if not seeds:
                continue
            med, n, u = ([_one(rows, f"layer:{hook}", m, replicate=s) for s in seeds]
                         for m in ("median_D", "n_positive", "u"))
            above = sum(a is not None and b is not None and a > b for a, b in zip(med, u))
            lines.append(f"| {hook} | {cond} | " + " / ".join(_fmt(x, 3) for x in med)
                         + " | " + " / ".join(f"{_fmt(x, 0)}/8" for x in n) + " | "
                         + " / ".join(_fmt(x, 3) for x in u) + f" | {above}/{len(seeds)} |")
    return lines


def x4_compare(rows: Sequence[MetricRow]) -> list[str]:
    """Secondary X4 outcomes under O and P side by side."""
    items = [(f"F1 rule under {v}", f"x4:{v}", "F1rule_verdict")
             for v in ("V0", "V1", "V2", "V3", "V4", "V5")]
    items += [("X4-b (V5 functional geometry)", "x4:b", "X4b_verdict"),
              ("X4-d, A = V0", "x4:d:V0", "X4d_verdict"),
              ("X4-d, A = V1", "x4:d:V1", "X4d_verdict"),
              ("H3′ rule, A = V0", "x4:h3p:V0", "H3prime_verdict"),
              ("H3′ rule, A = V1", "x4:h3p:V1", "H3prime_verdict")]
    lines = ["| item | O (S4) | P (S5) |", "|---|---|---|"]
    for label, space, prefix in items:
        lines.append(f"| {label} | " + " | ".join(_verdict(rows, space, prefix, c)[0]
                                                  for c in ("O", "P")) + " |")
    for label, space, metric in (("X4-a verdicts V0 = V1", "x4:a", "X4a_verdicts_equal"),
                                 ("X4-b positive control passed", "x4:b",
                                  "positive_control_passed")):
        vals = [_one(rows, space, metric, condition=c) for c in ("O", "P")]
        lines.append(f"| {label} | " + " | ".join(
            "not run" if v is None else ("yes" if v else "no") for v in vals) + " |")
    cats = [next((r.metric_id.removeprefix("X4c_") for r in rows if r.space == "x4:c"
                  and r.condition == c and r.metric_id.startswith("X4c_")), "not run")
            for c in ("O", "P")]
    lines.append("| X4-c category | " + " | ".join(cats) + " |")
    return lines


def compare_table(rows_o: Sequence[MetricRow], rows_p: Sequence[MetricRow]) -> list[str]:
    """F1 contrast and baselines per replicate, O (E2) vs P (E3)."""
    lines = ["| replicate | condition | panels D > 0 | median D | u_r | R1 median D (ratio) "
             "| R2 ratio | R3 ratio |", "|---|---|---|---|---|---|---|---|"]
    for seed in sorted(set(replicates(rows_o)) | set(replicates(rows_p))):
        for cond, rows in (("O", rows_o), ("P", rows_p)):
            D = [r.value for r in _pick(rows, "F1", "D", replicate=seed)]
            if not D:
                lines.append(f"| {seed} | {cond} | not run |  |  |  |  |  |")
                continue
            ratio = {k: _one(rows, f"F1:base:{k}", "median_D_ratio_to_model", replicate=seed)
                     for k in ("R1", "R2", "R3")}
            lines.append(
                f"| {seed} | {cond} | {sum(d is not None and d > 0 for d in D)}/{len(D)} "
                f"| {_fmt(_one(rows, 'F1', 'median_D', replicate=seed), 4)} "
                f"| {_fmt(_one(rows, 'F1', 'u', replicate=seed), 4)} "
                f"| {_fmt(_one(rows, 'F1:base:R1', 'median_D', replicate=seed), 4)} "
                f"({_fmt(ratio['R1'], 2)}) | {_fmt(ratio['R2'], 2)} | {_fmt(ratio['R3'], 2)} |")
    return lines


def geometry_compare(rows_o: Sequence[MetricRow], rows_p: Sequence[MetricRow]) -> list[str]:
    lines = ["| condition | world | median Δgeom, all pairs (panels > 0) "
             "| median Δgeom, same w₃₂ (panels > 0 of ok) |", "|---|---|---|---|"]
    for cond, rows in (("O", rows_o), ("P", rows_p)):
        for w in WORLDS:
            cells = []
            for m in ("delta_geom_all", "delta_geom_same_last_symbol"):
                ok = [r.value for r in _pick(rows, "geometry", m, world=w) if r.value is not None]
                cells.append(f"{_fmt(_median(ok), 3)} ({sum(v > 0 for v in ok)}/{len(ok)})"
                             if ok else "not run")
            lines.append(f"| {cond} | {w} | " + " | ".join(cells) + " |")
    return lines


# ---- figures --------------------------------------------------------------------------------
def _series(rows: Sequence[MetricRow], space: str, metric: str) -> dict[tuple, list[tuple]]:
    out: dict[tuple, list[tuple]] = {}
    for r in _pick(rows, space, metric):
        if r.checkpoint is not None and r.value is not None:
            out.setdefault((r.world, r.replicate), []).append((r.checkpoint, r.value))
    return {k: sorted(v) for k, v in out.items()}


def _grid_figure(cells: list[list[dict]], path: Path, title: str) -> Path:
    """Small multiples: each cell holds ``series`` {(world, seed): [(step, value)]}, ``ylabel``,
    ``log`` and optional ``refs`` {(world, label): y} drawn as dashed reference lines."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n_r, n_c = len(cells), len(cells[0])
    fig, axes = plt.subplots(n_r, n_c, figsize=(3.4 * n_c, 2.5 * n_r), dpi=150, squeeze=False)
    steps = sorted({s for row in cells for c in row for v in c["series"].values() for s, _ in v})
    pos = {s: i for i, s in enumerate(steps)}
    for i, row in enumerate(cells):
        for j, cell in enumerate(row):
            ax = axes[i][j]
            ax.set_facecolor(SURFACE)
            for (world, _seed), pts in sorted(cell["series"].items()):
                ax.plot([pos[s] for s, _ in pts], [v for _, v in pts], color=WORLD_COLOR[world],
                        linewidth=1.6, alpha=0.85, marker="o", markersize=3)
            for (world, label), y in cell.get("refs", {}).items():
                ax.axhline(y, color=WORLD_COLOR[world], linewidth=1, linestyle=(0, (3, 3)))
                ax.annotate(label, (len(steps) - 1, y), xytext=(2, 2),
                            textcoords="offset points", fontsize=6, color=INK_MUTED, ha="right")
            if cell.get("log"):
                ax.set_yscale("log")
            ax.set_title(cell["title"], fontsize=8, color=INK, loc="left")
            ax.set_ylabel(cell["ylabel"], fontsize=7, color=INK_MUTED)
            ax.set_xticks(range(len(steps)), [str(s) for s in steps], rotation=60)
            ax.grid(color=GRID, linewidth=0.6)
            for side in ("top", "right"):
                ax.spines[side].set_visible(False)
            for side in ("left", "bottom"):
                ax.spines[side].set_color(GRID)
            ax.tick_params(colors=INK_MUTED, labelsize=6, length=0)
    handles = [plt.Line2D([], [], color=c, linewidth=1.6, marker="o", markersize=3, label=w)
               for w, c in WORLD_COLOR.items()]
    fig.legend(handles=handles, loc="upper right", fontsize=7, frameon=False, ncol=2)
    fig.suptitle(title, fontsize=9, color=INK, x=0.01, ha="left")
    fig.supxlabel("checkpoint (training step; one line per replicate)", fontsize=7,
                  color=INK_MUTED)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def dynamics_figure(dyn: dict[str, Sequence[MetricRow]], path: Path) -> Path:
    cells = []
    for cond, rows in dyn.items():
        g_c = {(r.world, f"G_C {r.world}"): r.value for r in _pick(rows, "dyn", "G_C")
               if r.value is not None}
        cells.append([{"title": f"{cond}: S (resid_post_3), panel 1", "ylabel": "S",
                       "series": _series(rows, "dyn:S", "S_H1")},
                      {"title": f"{cond}: regret KL(q_C ‖ p_model)", "ylabel": "nats (log)",
                       "series": _series(rows, "dyn:regret", "regret"), "log": True,
                       "refs": g_c}])
    return _grid_figure(cells, path, "Training dynamics on panel 1 (H4, D-034)")


def curves_figure(curves: dict[str, Sequence[MetricRow]], path: Path) -> Path:
    cells = [[{"title": f"{cond}: S under {v}", "ylabel": "S",
               "series": _series(rows, f"dyn:x4:{v}", "S_H1")} for v in ("V1", "V5")]
             for cond, rows in curves.items()]
    return _grid_figure(cells, path, "X4 views V1 / V5 over training, panel 1 (descriptive)")


# ---- driver ---------------------------------------------------------------------------------
def _quote(path: Path, prefix: str) -> str:
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    return _prereg_line(lines, prefix)


def _decision(path: Path, did: str) -> str:
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    return next((ln.strip() for ln in lines if f"| {did} |" in ln), f"({did}: not found)")


def build_e3(store: ArtifactStore, out_dir: Path, repo_root: Path, final: int = 5000) -> Path:
    """Write ``summary.md``, ``condition_P.md`` and the two figures; returns the summary path."""
    prereg, prereg_x4 = repo_root / "PREREGISTRATION.md", repo_root / "PREREGISTRATION_X4.md"
    decisions = repo_root / "state" / "DECISIONS.md"
    rows_o, rows_p = analysis_rows(store, "S4"), analysis_rows(store, "S5")
    dyn = {c: s6_rows(store, "dynamics", c) for c in ("O", "P")}
    layers = {c: s6_rows(store, "layers", c) for c in ("O", "P")}
    curves = {c: s6_rows(store, "x4curves", c) for c in ("O", "P")}
    x4 = x4_rows(store)
    build_e2(store, out_dir, "S5", final, x4_section(store, prereg_x4, "P", final),
             name="condition_P.md", figure="fig_f1_contrasts_P.png")
    h3, h3_reason = verdict(rows_p)
    h4, h4_reason = h4_status(dyn["O"])
    h4_p, h4_p_reason = h4_status(dyn["P"])
    lines = [
        "# E3: condition P (S5), training dynamics (S6), X4 under O and P", "",
        "Primary hypotheses (PREREGISTRATION.md) come first; H3′ is a decision rule approved "
        "at H3 (D-037); X4 items are secondary; S6 extras are descriptive.", "",
        "## Primary: H3 (F1 rule under P)", "", _quote(prereg, "| H3 |"), "",
        f"**F1 rule under P: {h3}**" + (f" ({h3_reason})" if h3_reason else ""), "",
        H3_READING.get(h3, H3_READING["INCONCLUSIVE"]), "",
        _quote(prereg, "**Which hypotheses are decidable"), "",
        "Full S5 tables (prediction vs oracle, F1 contrasts, baselines, Δgeom, Gaussian floor, "
        "G-F, X4 under P): [condition_P.md](condition_P.md).", "",
        "## Primary: H4 (training dynamics, cylinder runs under O)", "",
        _quote(prereg, "| H4 |"), "", "Rule (fixed before any S4 result):", "",
        _decision(decisions, "D-034"), "",
        f"**H4 under O: {h4}**" + (f" ({h4_reason})" if h4_reason else ""), "",
        H4_READING.get(h4, H4_READING["INCONCLUSIVE"]), "",
        *h4_table(dyn["O"], curves["O"]), "",
        f"Under P (descriptive only, D-034): rule outcome {h4_p}"
        + (f" ({h4_p_reason})" if h4_p_reason else "") + ".", "",
        *h4_table(dyn["P"], curves["P"]), "",
        "t_history = first checkpoint with regret < G_C; t_rise = first checkpoint with "
        "S_t − S_0 > u_r. The V1 / V5 columns use the same rule with that view's u_r from X4 "
        "(D-044, descriptive). The checkpoint-order null is descriptive, never decisive.", "",
        "![dynamics](fig_dynamics.png)", "",
        "## Decision rule H3′ (approved at H3, D-037)", "", _quote(prereg_x4, "H3′"), ""]
    for a in ("V0", "V1"):
        for cond, role in (("P", "decision"), ("O", "comparison only")):
            st, reason = _verdict(x4, f"x4:h3p:{a}", "H3prime_verdict", cond)
            lines.append(f"- {cond} ({role}), A = {a}: panels passing per run "
                         f"{run_table(x4, f'x4:h3p:{a}', 'n_pass', cond)}; **{st}**"
                         + (f" ({reason})" if reason else ""))
    lines += ["", "## Secondary: X4 under O and P (PREREGISTRATION_X4.md)", "",
              *x4_compare(x4), "",
              "X4-b's expectation is pre-registered for O only; under P it is descriptive. "
              "Per-view tables for P: [condition_P.md](condition_P.md); for O: "
              "[../E2/summary.md](../E2/summary.md).", "",
              "## Comparison with E2 (O) — F1 contrast and baselines", "",
              *compare_table(rows_o, rows_p), "", *geometry_compare(rows_o, rows_p), "",
              "## Layer sweep (descriptive, RESEARCH_SUMMARY §7.7)", "",
              *layer_table(layers), "",
              "![X4 view curves](fig_x4_curves.png)", "",
              "**Not run:** S7 (U and extra N controls, probes, sensitivity, circular "
              "coordinates), S8 (clean rerun), X4-causal and other extensions.", ""]
    if any(dyn.values()):
        dynamics_figure({c: r for c, r in dyn.items() if r}, out_dir / "fig_dynamics.png")
    if any(curves.values()):
        curves_figure({c: r for c, r in curves.items() if r}, out_dir / "fig_x4_curves.png")
    summary = out_dir / "summary.md"
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary
