"""Report for exit level E2 (S4) and the condition-P section of E3 (S5), from MetricRecords and
GateReports only.

``topo-pilot report --level E2`` writes ``reports/E2/summary.md`` and ``fig_f1_contrasts.png``:
the prediction-vs-oracle table, the F1 contrasts D_{r,i} with the four median S values and u_r,
the F1 verdict with its reasons, the baselines R1–R3 (D-028), Δgeom (H2, D-031), the Gaussian
floor, the H0 check and gate G-F. Anything missing is printed as "not run", never invented.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import numpy as np

from topo_pilot.contracts import ArtifactStore, GateReport, MetricRecords, MetricRow

from .report import GRID, INK, INK_MUTED, _fmt

DOT, SURFACE = "#2a78d6", "#fcfcfb"
WORLDS = ("cylinder", "square")
BASELINES = ("R1", "R2", "R3")


def _latest(store: ArtifactStore, cls, **filters) -> list[str]:
    """Ids matching ``filters``, newest first (``created_utc``)."""
    ids = list(store.find(cls, **filters))
    return sorted(ids, key=lambda a: store.meta(a).created_utc, reverse=True)


def run_rows(store: ArtifactStore, stage: str) -> dict[tuple, dict[str, float | None]]:
    """Per run key ``(world, condition, seed)``: the final-checkpoint training metrics of the
    newest run record."""
    out: dict[tuple, dict[str, float | None]] = {}
    for mid in _latest(store, MetricRecords, stage=stage, kind="run"):
        key = tuple(store.meta(mid).config["run_key"])
        if key in out:
            continue
        rows = store.load(MetricRecords, mid, consumer="experiment").rows
        vals = {r.metric_id: r.value for r in rows if r.metric_id != "dev_ce"}
        ce = sorted((r.checkpoint, r.value) for r in rows if r.metric_id == "dev_ce")
        vals["dev_ce_final"] = ce[-1][1] if ce else None
        out[key] = vals
    return out


def analysis_rows(store: ArtifactStore, stage: str) -> list[MetricRow]:
    ids = _latest(store, MetricRecords, stage=stage, kind="analysis")
    return list(store.load(MetricRecords, ids[0], consumer="experiment").rows) if ids else []


def _pick(rows: Sequence[MetricRow], space: str, metric: str, **kw) -> list[MetricRow]:
    return [r for r in rows if r.space == space and r.metric_id == metric
            and all(getattr(r, k) == v for k, v in kw.items())]


def _one(rows: Sequence[MetricRow], space: str, metric: str, **kw) -> float | None:
    hits = _pick(rows, space, metric, **kw)
    return hits[0].value if hits else None


def _median(values: Sequence[float | None]) -> float | None:
    vals = [v for v in values if v is not None]
    return float(np.median(vals)) if vals else None


def _act_space(rows: Sequence[MetricRow]) -> str:
    """The activation space name (``act:<primary hook>``) used by the analysis job."""
    act = sorted({r.space for r in rows if r.space.startswith("act:")})
    return act[0] if act else "act:"


def replicates(rows: Sequence[MetricRow]) -> list[int]:
    return sorted({r.replicate for r in rows if r.space == "F1" and r.metric_id == "u"})


def prediction_table(runs: dict[tuple, dict], cond: str) -> list[str]:
    lines = ["| run | captured | regret (nats) | G_C (nats) | dev CE, final | learning gate "
             "| wall (min) |", "|---|---|---|---|---|---|---|"]
    for (world, c, seed), v in sorted(runs.items()):
        if c not in (cond, "N"):
            continue
        gate = v.get("learning_gate_passed")
        lines.append(
            f"| {world}-{c}-{seed} | {_fmt(v.get('captured'))} | {_fmt(v.get('regret'), 4)} "
            f"| {_fmt(v.get('G_C'), 4)} | {_fmt(v.get('dev_ce_final'), 4)} "
            f"| {'not run' if gate is None else ('pass' if gate else 'fail')} "
            f"| {_fmt(None if v.get('wall_time_s') is None else v['wall_time_s'] / 60, 1)} |")
    return lines


def f1_table(rows: Sequence[MetricRow], final: int) -> list[str]:
    space = _act_space(rows)
    lines = ["| replicate | S cyl init | S cyl final | S sq init | S sq final | panels D > 0 "
             "| median D | u_r | median D > u_r |", "|---|---|---|---|---|---|---|---|---|"]
    for seed in replicates(rows):
        cells = [_median([r.value for r in _pick(rows, space, "S_H1", world=w, replicate=seed,
                                                 checkpoint=ck)])
                 for w in WORLDS for ck in (0, final)]
        D = [r.value for r in _pick(rows, "F1", "D", replicate=seed)]
        med, u = _one(rows, "F1", "median_D", replicate=seed), _one(rows, "F1", "u",
                                                                    replicate=seed)
        n_pos = sum(d is not None and d > 0 for d in D)
        ok = "not run" if med is None or u is None else ("yes" if med > u else "no")
        lines.append(f"| {seed} | " + " | ".join(_fmt(c) for c in cells)
                     + f" | {n_pos}/{len(D)} | {_fmt(med, 4)} | {_fmt(u, 4)} | {ok} |")
    return lines


def verdict(rows: Sequence[MetricRow]) -> tuple[str, str]:
    """``(status, reasons)`` of the F1 verdict row; ``("not run", "")`` if absent."""
    for r in rows:
        if r.space == "F1" and r.metric_id.startswith("F1_verdict_"):
            return r.metric_id.removeprefix("F1_verdict_"), r.uncertainty_kind or ""
    return "not run", ""


def baseline_table(rows: Sequence[MetricRow]) -> list[str]:
    lines = ["| replicate | model median D | " + " | ".join(
        f"{k}: median D (panels > 0, ratio)" for k in BASELINES) + " |",
        "|---|---|" + "---|" * len(BASELINES)]
    for seed in replicates(rows):
        cells = []
        for k in BASELINES:
            sp = f"F1:base:{k}"
            med, n, ratio = (_one(rows, sp, m, replicate=seed) for m in
                             ("median_D", "n_positive", "median_D_ratio_to_model"))
            cells.append(f"{_fmt(med, 4)} ({_fmt(n, 0)}, {_fmt(ratio, 2)})")
        lines.append(f"| {seed} | {_fmt(_one(rows, 'F1', 'median_D', replicate=seed), 4)} | "
                     + " | ".join(cells) + " |")
    return lines


def geometry_table(rows: Sequence[MetricRow]) -> list[str]:
    lines = ["| replicate | world | median Δgeom, all pairs | panels > 0 "
             "| median Δgeom, same w₃₂ | panels > 0 (of ok) |", "|---|---|---|---|---|---|"]
    for seed in replicates(rows):
        for w in WORLDS:
            row = [f"| {seed} | {w}"]
            for m in ("delta_geom_all", "delta_geom_same_last_symbol"):
                vals = [r.value for r in _pick(rows, "geometry", m, replicate=seed, world=w)]
                ok = [v for v in vals if v is not None]
                row += [_fmt(_median(ok), 3), f"{sum(v > 0 for v in ok)}/{len(ok)}"]
            lines.append(" | ".join(row) + " |")
    return lines


def floor_table(rows: Sequence[MetricRow], final: int) -> list[str]:
    space = _act_space(rows)
    lines = ["| replicate | world | S final, panel 1 | iso floor mean / q95 "
             "| cov floor mean / q95 |",
             "|---|---|---|---|---|"]
    for seed in replicates(rows):
        for w in WORLDS:
            s = _one(rows, space, "S_H1", world=w, replicate=seed, checkpoint=final, panel=1)
            cells = [f"{_fmt(_one(rows, f'null:{k}:act', 'S_H1_mean', world=w, replicate=seed))}"
                     f" / {_fmt(_one(rows, f'null:{k}:act', 'S_H1_q95', world=w, replicate=seed))}"
                     for k in ("iso", "cov")]
            lines.append(f"| {seed} | {w} | {_fmt(s)} | " + " | ".join(cells) + " |")
    return lines


def f1_figure(rows: Sequence[MetricRow], path: Path, title: str) -> Path:
    """Dot plot of D_{r,i} (8 panels) per replicate, with the median (diamond) and the noise
    envelope u_r (dashed tick); the F1 rule needs ≥ 7 dots right of 0 and the diamond right of
    the tick, in every replicate."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    seeds = replicates(rows)
    fig, ax = plt.subplots(figsize=(6.4, 0.9 + 0.7 * max(len(seeds), 1)), dpi=150)
    ax.set_facecolor(SURFACE)
    ax.axvline(0, color=INK_MUTED, linewidth=1, zorder=1)
    for y, seed in enumerate(seeds):
        D = [r.value for r in _pick(rows, "F1", "D", replicate=seed) if r.value is not None]
        ax.scatter(D, [y] * len(D), s=56, color=DOT, alpha=0.85, edgecolor=SURFACE,
                   linewidth=2, zorder=3)
        med, u = _one(rows, "F1", "median_D", replicate=seed), _one(rows, "F1", "u",
                                                                    replicate=seed)
        if med is not None:
            ax.scatter([med], [y], marker="D", s=44, color=INK, zorder=4)
            ax.annotate(f"median {med:.3f}", (med, y), xytext=(0, 10),
                        textcoords="offset points", ha="center", fontsize=7, color=INK_MUTED,
                        zorder=5, bbox={"boxstyle": "square,pad=0.1", "fc": SURFACE, "ec": "none"})
        if u is not None:
            ax.plot([u, u], [y - 0.22, y + 0.22], color=INK_MUTED, linewidth=1.2,
                    linestyle=(0, (3, 2)), zorder=2)
            ax.annotate("u_r", (u, y - 0.22), xytext=(0, -9), textcoords="offset points",
                        ha="center", fontsize=7, color=INK_MUTED)
    ax.set_yticks(range(len(seeds)), [f"seed {s}" for s in seeds], color=INK)
    ax.set_ylim(-0.7, len(seeds) - 0.3)
    ax.set_xlabel("D = (S_cyl final − S_cyl init) − (S_sq final − S_sq init), per panel",
                  color=INK, fontsize=8)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK_MUTED, labelsize=8, length=0)
    ax.set_title(title, fontsize=9, color=INK, loc="left")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def build_e2(store: ArtifactStore, out_dir: Path, stage: str = "S4", final: int = 5000,
             extra: Sequence[str] = ()) -> Path:
    """Write ``summary.md`` and ``fig_f1_contrasts.png`` for ``stage`` (S4: O, E2; S5: P);
    ``extra`` lines (e.g. the secondary X4 section) are appended after the F1 sections."""
    cond = "O" if stage == "S4" else "P"
    rows, runs = analysis_rows(store, stage), run_rows(store, stage)
    status, reasons = verdict(rows)
    missing = sorted({r.replicate for r in rows if r.metric_id == "replicate_available"})
    lines = [f"# {'E2' if stage == 'S4' else 'E3 (P)'}: F1 under condition {cond} ({stage})", "",
             f"**F1 verdict: {status}**" + (f" ({reasons})" if reasons else ""), "",
             "Missing replicates (not run): " + (", ".join(map(str, missing)) or "none"), "",
             "## Prediction vs oracle (p = 32, test panels)", "", *prediction_table(runs, cond),
             "", "## F1 contrasts (median S over 8 panels; RESEARCH_SUMMARY §7.4)", "",
             *f1_table(rows, final), "", "![D per panel](fig_f1_contrasts.png)", "",
             "## Representation baselines (D-028: baseline in place of the final checkpoint)",
             "", *baseline_table(rows), "",
             "## H2: Δgeom = ρ(d_A, d_B32) − ρ(d_A, d_B1) (D-031 for same-w₃₂ pairs)", "",
             *geometry_table(rows), "",
             "## Gaussian floor (reported, never a threshold; D-005)", "",
             *floor_table(rows, final), ""]
    if cond == "O":
        lines += ["## H0 (N model; D-029)", "",
                  f"Test NLL at p = 32: {_fmt(_one(rows, 'H0', 'nll_p32'), 4)}; "
                  f"H(W) = {_fmt(_one(rows, 'H0', 'H_W'), 4)}; bootstrap 95% half-width "
                  f"{_fmt(_one(rows, 'H0', 'ci_half_width'), 4)}.", ""]
    for gid in _latest(store, GateReport, stage=stage, gate="G-F")[:1]:
        g = store.load(GateReport, gid, consumer="experiment")
        lines.append(f"Gate {g.gate_id}: **{g.verdict}**")
        lines += [f"- {c.name}: {c.value} (threshold {c.threshold}) -> "
                  f"{'pass' if c.passed else 'fail'}" for c in g.checks]
    f1_figure(rows, out_dir / "fig_f1_contrasts.png",
              f"F1 contrasts under {cond}: D per panel, median (◆) and noise envelope u_r (┊)")
    if extra:
        lines += ["", *extra]
    summary = out_dir / "summary.md"
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary

