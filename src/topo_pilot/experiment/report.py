"""Report generation from MetricRecords and GateReports only (W0/W1 scope: level E0).

``topo-pilot report --level E0`` writes ``reports/E0/`` with a summary table (markdown) and one
figure. It never reads specs, diagrams, or activations: figures are reproducible from
MetricRecords alone (``make reproduce-figures`` / ``.\\tasks.ps1 reproduce-figures``).
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from topo_pilot.contracts import ArtifactStore, GateReport, MetricRecords, MetricRow

SERIES = {"world_flat": ("flat metric $d_M$", "#2a78d6"),
          "world_graph": ("graph geodesic (sensitivity)", "#eb6834")}
INK, INK_MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def _rows(store: ArtifactStore, stage: str) -> list[MetricRow]:
    rows: list[MetricRow] = []
    for mid in store.find(MetricRecords, stage=stage):
        rows.extend(store.load(MetricRecords, mid, consumer="experiment").rows)
    return rows


def _value(rows: Sequence[MetricRow], space: str, metric: str, world: str | None) -> float | None:
    hits = [r.value for r in rows
            if r.space == space and r.metric_id == metric and r.world == world]
    return hits[0] if hits else None


def _fmt(v: float | None, digits: int = 3) -> str:
    return "not run" if v is None else f"{v:.{digits}f}"


def e0_table(rows: Sequence[MetricRow]) -> list[str]:
    """Markdown lines: graph cycles vs surface holes, and S per world and metric."""
    lines = ["| world | graph cycle rank | β₁ (GF(2)) | S, flat d_M | S, graph metric |",
             "|---|---|---|---|---|"]
    for w in ("square", "cylinder"):
        lines.append(f"| {w} | {_fmt(_value(rows, 'world', 'graph_cycle_rank', w), 0)} "
                     f"| {_fmt(_value(rows, 'world', 'beta1_gf2', w), 0)} "
                     f"| {_fmt(_value(rows, 'world_flat', 'S_H1', w))} "
                     f"| {_fmt(_value(rows, 'world_graph', 'S_H1', w))} |")
    return lines


def e0_figure(rows: Sequence[MetricRow], path: Path) -> Path:
    """Dot plot of S (longest H1 bar / q95 scale) per world, one series per metric, with the
    pre-registered G-A thresholds (D-016) as reference lines."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    worlds = ["square", "cylinder"]
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=150)
    ax.set_facecolor("#fcfcfb")
    for k, (space, (label, color)) in enumerate(SERIES.items()):
        ys = [i + (0.12 if k == 0 else -0.12) for i in range(len(worlds))]
        xs = [_value(rows, space, "S_H1", w) for w in worlds]
        ax.scatter(xs, ys, s=64, color=color, edgecolor="#fcfcfb", linewidth=2, zorder=3,
                   label=label)
        for x, y in zip(xs, ys):
            if x is not None:
                ax.annotate(f"{x:.3f}", (x, y), xytext=(8, 0), textcoords="offset points",
                            va="center", fontsize=8, color=INK_MUTED)
    for x, txt in ((0.10, "square must be < 0.10"), (0.20, "cylinder must be ≥ 0.20")):
        ax.axvline(x, color=INK_MUTED, linewidth=1, linestyle=(0, (3, 3)), zorder=1)
        ax.text(x, len(worlds) - 0.45, txt, fontsize=7, color=INK_MUTED, ha="center")
    ax.set_yticks(range(len(worlds)), worlds, color=INK)
    ax.set_ylim(-0.6, len(worlds) - 0.3)
    ax.set_xlim(0, 0.4)
    ax.set_xlabel("S = longest H₁ bar / q95 of distances", color=INK, fontsize=9)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK_MUTED, labelsize=8, length=0)
    ax.legend(loc="lower right", fontsize=7, frameon=False)
    ax.set_title("Vietoris–Rips on the latent world: one long H₁ bar, on the cylinder only",
                 fontsize=9, color=INK, loc="left")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor="#fcfcfb")
    plt.close(fig)
    return path


def build_e0(store: ArtifactStore, out_dir: Path) -> Path:
    """Write ``summary.md`` and ``fig_world_ph.png`` for exit level E0; returns the summary path."""
    rows = _rows(store, "S1")
    gates = [store.load(GateReport, g, consumer="experiment")
             for g in store.find(GateReport, stage="S1")]
    lines = ["# E0: ground-truth topology and PH calibration", "", *e0_table(rows), ""]
    for g in gates:
        lines.append(f"Gate {g.gate_id}: **{g.verdict}**")
        lines += [f"- {c.name}: {c.value} (threshold {c.threshold}) -> "
                  f"{'pass' if c.passed else 'fail'}" for c in g.checks]
    syn = {r.metric_id: r.value for r in rows if r.space == "synthetic"}
    lines += ["", f"Synthetic calibration (M=512, R^128): mean S circle "
              f"{_fmt(syn.get('S_circle_mean'))}, max S disk {_fmt(syn.get('S_disk_max'))}.",
              "", "![S per world](fig_world_ph.png)", ""]
    e0_figure(rows, out_dir / "fig_world_ph.png")
    summary = out_dir / "summary.md"
    summary.write_text("\n".join(lines), encoding="utf-8")
    return summary
