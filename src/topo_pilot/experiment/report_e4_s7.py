"""S7 and S8 tables and figures of the E4 report, from MetricRecords and GateReports only.

Every table reads the newest S7 / S8 record of its kind. Missing data prints "not run".
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from topo_pilot.contracts import ArtifactStore, GateReport, MetricRecords, MetricRow

from .report import GRID, INK, INK_MUTED, _fmt
from .report_e2 import SURFACE, WORLDS, _latest, _median, _one, _pick

WORLD_COLOR = {"cylinder": "#2a78d6", "square": "#eb6834"}  # validated pair (dataviz checks)
PROBES = (("A5000->b32", "activations, step 5000 → b³² (main)"),
          ("A0->b32", "activations, step 0 → b³²"),
          ("F1->b32", "exact next-symbol distribution F₁ → b³²"),
          ("onehot_w32->b32", "one-hot last symbol w₃₂ → b³²"),
          ("A5000->r_w", "activations, step 5000 → r_w (last-symbol posterior)"),
          ("A5000->b32_shuffled", "activations, step 5000 → shuffled b³² (label control)"))
CIRC = "privileged_eval:circular"


def s7_rows(store: ArtifactStore, kind: str) -> list[MetricRow]:
    """Rows of the newest S7 (or S8) record of ``kind``."""
    for stage in ("S7", "S8"):
        ids = _latest(store, MetricRecords, stage=stage, kind=kind)
        if ids:
            return list(store.load(MetricRecords, ids[0], consumer="experiment").rows)
    return []


def control_runs(store: ArtifactStore) -> dict[tuple, dict[str, float | None]]:
    """Newest S7 run record per run key: final metrics, H0 rows and failure notes."""
    out: dict[tuple, dict] = {}
    for mid in _latest(store, MetricRecords, stage="S7", kind="run"):
        key = tuple(store.meta(mid).config["run_key"])
        if key in out:
            continue
        rows = store.load(MetricRecords, mid, consumer="experiment").rows
        vals: dict = {r.metric_id: r.value for r in rows if r.metric_id != "dev_ce"}
        vals["_failure"] = next((r.uncertainty_kind for r in rows
                                 if r.metric_id == "run_available"), None)
        out[key] = vals
    return out


def control_table(runs: dict[tuple, dict], s4_h0: Sequence[MetricRow]) -> list[str]:
    lines = ["| run | V | regret (nats) | gain over the unigram G_U (U) / G_C | captured "
             "(captured_U for U) | learning gate | H0: NLL p=32 vs H(W) − CI/2 | wall (min) |",
             "|---|---|---|---|---|---|---|---|"]
    for key, v in sorted(runs.items(), key=lambda kv: str(kv[0])):
        world, cond, seed = key
        name = f"{world}-{cond}-{seed}"
        if v.get("_failure"):
            lines.append(f"| {name} | failed: {v['_failure']} |  |  |  |  |  |  |")
            continue
        gain = v.get("G_U") if cond == "U" else v.get("G_C")
        cap = v.get("captured_U") if cond == "U" else v.get("captured")
        gate = v.get("learning_gate_passed")
        gate_cell = ("n/a (G_C = 0)" if gate is None else ("pass" if gate else "fail"))
        h0 = "n/a"
        if cond == "N":
            ok = v.get("h0_passed")
            h0 = (f"{_fmt(v.get('nll_p32'), 4)} vs {_fmt(_h0_floor(v), 4)}: "
                  + ("not run" if ok is None else ("pass" if ok else "FAIL")))
        wall = v.get("wall_time_s")
        lines.append(f"| {name} | {_fmt(v.get('V'), 0)} | {_fmt(v.get('regret'), 4)} "
                     f"| {_fmt(gain, 4)} | {_fmt(cap)} | {gate_cell} | {h0} "
                     f"| {_fmt(None if wall is None else wall / 60, 1)} |")
    nll, hw = _one(s4_h0, "H0", "nll_p32"), _one(s4_h0, "H0", "H_W")
    half = _one(s4_h0, "H0", "ci_half_width")
    if nll is not None and hw is not None and half is not None:
        lines.append(f"| any-N-1729 (S4) | 36 |  |  |  | n/a (G_C = 0) | {_fmt(nll, 4)} vs "
                     f"{_fmt(hw - half, 4)}: {'pass' if nll >= hw - half else 'FAIL'} |  |")
    return lines


def _h0_floor(v: dict) -> float | None:
    if v.get("H_W") is None or v.get("ci_half_width") is None:
        return None
    return v["H_W"] - v["ci_half_width"]


def controls_ph_table(rows: Sequence[MetricRow], final: int) -> list[str]:
    lines = ["| run | median S, step 0 | median S, step final | panels |", "|---|---|---|---|"]
    keys = sorted({(r.world, r.condition, r.replicate) for r in rows
                   if r.metric_id == "S_H1_median"}, key=str)
    for w, c, s in keys:
        a = _one(rows, r_space(rows), "S_H1_median", world=w, condition=c, replicate=s,
                 checkpoint=0)
        b = _one(rows, r_space(rows), "S_H1_median", world=w, condition=c, replicate=s,
                 checkpoint=final)
        n = len(_pick(rows, r_space(rows), "S_H1", world=w, condition=c, replicate=s,
                      checkpoint=final))
        lines.append(f"| {w}-{c}-{s} | {_fmt(a)} | {_fmt(b)} | {n} |")
    D = [r.value for r in _pick(rows, "controls:U", "D")]
    if D:
        lines += ["", f"U pair, cylinder − square contrast D per panel (one replicate, "
                      f"descriptive): median {_fmt(_median(D))}, D > 0 in "
                      f"{sum(d is not None and d > 0 for d in D)}/{len(D)} panels."]
    return lines


def r_space(rows: Sequence[MetricRow]) -> str:
    spaces = sorted({r.space for r in rows if r.space.startswith("controls:act:")})
    return spaces[0] if spaces else "controls:act:"


def probe_table(rows: Sequence[MetricRow]) -> list[str]:
    lines = ["| probe (features → target) | O: median test R² (range over 6 runs) "
             "| P: median test R² (range) |", "|---|---|---|"]
    for key, label in PROBES:
        cells = []
        for cond in ("O", "P"):
            vals = [r.value for r in _pick(rows, f"probe:{key}", "r2_test", condition=cond)
                    if r.value is not None]
            cells.append(f"{_fmt(_median(vals))} ({_fmt(min(vals))}–{_fmt(max(vals))})"
                         if vals else "not run")
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    lam = {c: sorted({r.value for r in _pick(rows, "probe:A5000->b32", "lambda", condition=c)})
           for c in ("O", "P")}
    pat = {c: (_one(rows, "probe:summary", "n_pattern", condition=c),
               _one(rows, "probe:summary", "n_runs", condition=c)) for c in ("O", "P")}
    lines += ["", "λ chosen on dev panels 7–8 for the main probe: "
              + "; ".join(f"{c}: {', '.join(_fmt(x, 3) for x in v) or 'not run'}"
                          for c, v in lam.items())
              + " (grid 1e-3 … 10).",
              "Predeclared descriptive pattern (D-047), R²(A5000 → b³²) above all of A0, one-hot "
              "and F₁: " + "; ".join(f"{c}: {_fmt(n, 0)}/{_fmt(t, 0)} runs"
                                       for c, (n, t) in pat.items()) + "."]
    return lines


def circular_table(rows: Sequence[MetricRow], final: int) -> list[str]:
    lines = ["| condition | world | step | median agreement with x angle (per-run medians) "
             "| panels above null q95 | panels with an H₁ class | control: y angle "
             "| oracle b³² vs x |", "|---|---|---|---|---|---|---|---|"]
    for cond in ("O", "P", "U"):
        for w in WORLDS:
            for step in (0, final):
                kw = {"condition": cond, "world": w, "checkpoint": step}
                med = [r.value for r in _pick(rows, CIRC, "agreement_x_median", **kw)]
                if not med:
                    continue
                above = sum(r.value or 0 for r in _pick(rows, CIRC, "n_panels_above_null_q95",
                                                        **kw))
                h1 = sum(r.value or 0 for r in _pick(rows, CIRC, "n_panels_with_h1_class", **kw))
                n = 8 * len(med)
                ctrl = [r.value for r in _pick(rows, CIRC, "agreement_control_median", **kw)]
                orc = [r.value for r in _pick(rows, CIRC, "agreement_oracle_x_median", **kw)]
                lines.append(f"| {cond} | {w} | {step} | {_fmt(_median(med))} "
                             f"({', '.join(_fmt(m) for m in med)}) | {above:.0f}/{n} "
                             f"| {h1:.0f}/{n} | {_fmt(_median(ctrl))} | {_fmt(_median(orc))} |")
    return lines


def sensitivity_table(rows: Sequence[MetricRow], primary: dict) -> list[str]:
    lines = ["| variant | condition | F1 rule (median D per replicate / u_r) | H3′ rule "
             "| Δgeom > 0 (fraction of run-panels) |", "|---|---|---|---|---|"]
    for cond in ("O", "P"):
        f1, h3p, dg = primary[cond]
        lines.append(f"| primary (S4/S5, X4) | {cond} | {f1} | {h3p} | {dg} |")
    variants = list(dict.fromkeys(r.space.removeprefix("sens:") for r in rows
                                  if r.space.startswith("sens:")))
    for v in variants:
        for cond in ("O", "P"):
            space = f"sens:{v}"
            st = next((r.metric_id.removeprefix("F1rule_verdict_") for r in rows
                       if r.space == space and r.condition == cond
                       and r.metric_id.startswith("F1rule_verdict_")), None)
            meds = [f"{_fmt(_one(rows, space, 'median_D', condition=cond, replicate=s))}/"
                    f"{_fmt(_one(rows, space, 'u', condition=cond, replicate=s))}"
                    for s in sorted({r.replicate for r in _pick(rows, space, "u",
                                                                condition=cond)})]
            f1 = "unchanged (activation S not affected)" if st is None else \
                f"{st} ({', '.join(meds)})"
            h3p = next((r.metric_id.removeprefix("H3prime_verdict_") for r in rows
                        if r.space == space and r.condition == cond
                        and r.metric_id.startswith("H3prime_verdict_")), "not run")
            frac = _one(rows, space, "delta_geom_all_fraction_positive", condition=cond)
            lines.append(f"| {v} | {cond} | {f1} | {h3p} | {_fmt(frac, 2)} |")
    return lines


def gate_lines(store: ArtifactStore, stage: str, gate_id: str) -> list[str]:
    ids = _latest(store, GateReport, stage=stage)
    reports = [store.load(GateReport, g, consumer="experiment") for g in ids]
    reports = [r for r in reports if r.gate_id == gate_id]
    if not reports:
        return [f"Gate {gate_id}: not run"]
    g = reports[0]
    return [f"Gate {gate_id}: **{g.verdict}**",
            *[f"- {c.name}: {c.value} -> {'pass' if c.passed else 'fail'}" for c in g.checks]]


def rerun_table(rows: Sequence[MetricRow]) -> list[str]:
    if not rows:
        return ["S8 rerun: not run"]
    lines = ["| artifact type | in rerun | id found in main store | checksum equal "
             "| gate verdict equal |", "|---|---|---|---|---|"]
    types = sorted({r.space.removeprefix("rerun:") for r in rows if r.space.startswith("rerun:")
                    and r.metric_id == "n"})
    for t in types:
        get = {m: _one(rows, f"rerun:{t}", m) for m in ("n", "id_found", "checksum_equal",
                                                        "verdict_match")}
        lines.append(f"| {t} | " + " | ".join(_fmt(get[m], 0) if get[m] is not None else "–"
                                              for m in ("n", "id_found", "checksum_equal",
                                                        "verdict_match")) + " |")
    walls = [(r.space.removeprefix("rerun:"), r.value) for r in rows
             if r.metric_id == "rerun_wall_time_s"]
    env = next((r.uncertainty_kind for r in rows if r.metric_id == "cpu_count"), "")
    mism = next((r for r in rows if r.metric_id == "mismatches"), None)
    lines += ["", "Rerun wall time: " + ", ".join(f"{s} {_fmt(v / 60, 1)} min"
                                                  for s, v in walls) + f". Environment: {env}.",
              f"Mismatches: {_fmt(mism.value, 0) if mism else 'not run'}"
              + (f" ({mism.uncertainty_kind})" if mism and mism.uncertainty_kind else "") + "."]
    return lines


def _dot_panel(ax, groups: list[tuple[str, dict[str, list[float]]]], xlabel: str) -> None:
    for i, (_, by_world) in enumerate(groups):
        for k, w in enumerate(WORLDS):
            vals = by_world.get(w, [])
            y = [i + (0.14 if k == 0 else -0.14)] * len(vals)
            ax.scatter(vals, y, s=48, color=WORLD_COLOR[w], edgecolor=SURFACE, linewidth=2,
                       zorder=3, label=w if i == 0 else None)
    ax.set_yticks(range(len(groups)), [g for g, _ in groups], color=INK, fontsize=7)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel, color=INK, fontsize=8)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK_MUTED, labelsize=7, length=0)


def _save(fig, path: Path) -> Path:
    import matplotlib.pyplot as plt

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, facecolor=SURFACE)
    plt.close(fig)
    return path


def probe_figure(rows: Sequence[MetricRow], path: Path) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.0), dpi=150, sharex=True, sharey=True)
    for ax, cond in zip(axes, ("O", "P")):
        groups = [(label.split(" (")[0], {w: [r.value for r in _pick(
                      rows, f"probe:{key}", "r2_test", condition=cond, world=w)
                      if r.value is not None] for w in WORLDS}) for key, label in PROBES]
        _dot_panel(ax, groups, "test R² (pooled over 8 panels)")
        ax.set_facecolor(SURFACE)
        ax.set_title(f"condition {cond}", fontsize=8, color=INK, loc="left")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", ncol=2, fontsize=7, frameon=False)
    fig.suptitle("Ridge probes: one dot per run (3 replicates per world)", fontsize=9, color=INK,
                 x=0.01, ha="left")
    return _save(fig, path)


def circular_figure(rows: Sequence[MetricRow], final: int, path: Path) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.4, 3.0), dpi=150)
    ax.set_facecolor(SURFACE)
    groups = []
    for cond in ("O", "P", "U"):
        for step in (0, final):
            by = {w: [r.value for r in _pick(rows, CIRC, "agreement_x", condition=cond,
                                             world=w, checkpoint=step) if r.value is not None]
                  for w in WORLDS}
            if any(by.values()):
                groups.append((f"{cond}, step {step}", by))
    _dot_panel(ax, groups, "agreement of circular coordinates with the latent x angle "
                           "(one dot per run-panel)")
    ax.set_xlim(0, 1)
    ax.legend(loc="lower right", fontsize=7, frameon=False)
    ax.set_title("Circular coordinates (top H₁ cocycle) vs latent x angle", fontsize=9,
                 color=INK, loc="left")
    return _save(fig, path)
