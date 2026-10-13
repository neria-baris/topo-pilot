"""``topo-pilot prereg``: write PREREGISTRATION.md from S2 outputs and base.yaml (H1 draft).

Reads only MetricRecords and GateReports (plus the repository docs and configs); refuses with
``GATE_FAILED`` unless G-B, G-C and G-D have passed.
"""

from __future__ import annotations

import re
import statistics
from collections import defaultdict
from datetime import date
from pathlib import Path

import yaml

from topo_pilot.contracts import (
    ArtifactStore,
    ErrorCode,
    GateReport,
    MetricRecords,
    MetricRow,
    StageFailure,
)

from .config import ResolvedConfig, producer_version

S2_GATES = ("G-B", "G-C", "G-D")
SPACES = ("emission", "belief32", "belief1", "future1", "future2")


def _section(text: str, heading: str) -> str:
    """The markdown block starting at ``heading`` up to the next heading of the same level."""
    level = heading.split(" ")[0]
    pattern = rf"^{re.escape(heading)}.*?(?=^{level} |\Z)"
    match = re.search(pattern, text, flags=re.S | re.M)
    return match.group(0).strip() if match else f"(section {heading!r} not found)"


def _s2_rows(store: ArtifactStore) -> list[MetricRow]:
    rows: list[MetricRow] = []
    for mid in store.find(MetricRecords, stage="S2"):
        rows += store.load(MetricRecords, mid, consumer="experiment").rows
    return rows


def _gates(store: ArtifactStore) -> dict[str, GateReport]:
    out = {}
    for gid in store.find(GateReport, stage="S2"):
        g = store.load(GateReport, gid, consumer="experiment")
        out[g.gate_id] = g
    return out


def sigma_table(rows: list[MetricRow]) -> list[str]:
    vals: dict[tuple[str, str], dict[str, float]] = defaultdict(dict)
    for r in rows:
        if r.space.startswith("sigma:"):
            vals[(r.space[6:], r.world or "")][r.metric_id] = r.value
    lines = ["| σ | world | mean H(b¹) (nats) | G_C (nats) | min p(w) |", "|---|---|---|---|---|"]
    lines += [f"| {s} | {w} | {v['mean_H_b1']:.3f} | {v['G_C']:.4f} | {v['min_p_w']:.4f} |"
              for (s, w), v in vals.items()]
    return lines


def disc_table(rows: list[MetricRow], n_panels: int) -> list[str]:
    """Median S over panels per space × world × condition, and panels with S_cyl > S_sq."""
    S: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    worlds: dict[tuple[str, str], float] = {}
    for r in rows:
        if r.metric_id != "S_H1" or r.value is None:
            continue
        if r.space in SPACES and r.panel is not None:
            S[(r.space, r.world, r.condition)].append(r.value)
        elif r.space in ("world", "emission"):
            worlds[(r.space, f"{r.world}/{r.condition}")] = r.value
    pos = {(r.space, r.condition): int(r.value) for r in rows
           if r.metric_id == "n_panels_cyl_gt_sq"}
    lines = ["| space | cond | median S cylinder | median S square | panels cyl > sq |",
             "|---|---|---|---|---|"]
    for space in SPACES:
        for cond in ("O", "P"):
            cyl, sq = S.get((space, "cylinder", cond)), S.get((space, "square", cond))
            if not cyl or not sq:
                continue
            lines.append(f"| {space} | {cond} | {statistics.median(cyl):.3f} | "
                         f"{statistics.median(sq):.3f} | {pos.get((space, cond), 0)}/{n_panels} |")
    for space, cond in (("world", None), ("emission", "O"), ("emission", "P")):
        key = f"{{w}}/{cond}"
        cyl, sq = worlds.get((space, key.format(w="cylinder"))), worlds.get(
            (space, key.format(w="square")))
        if cyl is not None and sq is not None:
            label = "—" if cond is None else cond
            lines.append(f"| {space} (all 144 states) | {label} | {cyl:.3f} | {sq:.3f} | — |")
    floor = {(r.space, r.world, r.condition, r.metric_id): r.value for r in rows
             if r.space.startswith("null:")}
    lines += ["", "Gaussian floor of S (belief32, panel 1, Hellinger embedding; context only):", "",
              "| world | cond | iso mean | iso q95 | cov mean | cov q95 |",
              "|---|---|---|---|---|---|"]
    for w in ("cylinder", "square"):
        for c in ("O", "P"):
            g = [floor.get((f"null:{k}:belief32", w, c, m)) for k in ("iso", "cov")
                 for m in ("S_H1_mean", "S_H1_q95")]
            if all(v is not None for v in g):
                lines.append(f"| {w} | {c} | " + " | ".join(f"{v:.3f}" for v in g) + " |")
    return lines


def write_prereg(cfg: ResolvedConfig, store: ArtifactStore, conductor_note: str = "") -> Path:
    """Write ``PREREGISTRATION.md`` at the repository root; returns its path."""
    gates = _gates(store)
    missing = [g for g in S2_GATES if g not in gates or gates[g].verdict == "fail"]
    if missing:
        raise StageFailure(ErrorCode.GATE_FAILED, "experiment.prereg", "s2_gates",
                           f"S2 gates not passed: {missing}")
    rows = _s2_rows(store)
    sigma = next(r.value for r in rows if r.space == "sigma" and r.metric_id == "selected")
    status = gates["G-C"].checks[0].threshold
    summary = (cfg.repo_root / "docs" / "RESEARCH_SUMMARY.md").read_text(encoding="utf-8")
    n_panels = cfg.base["data"]["n_panels"]
    lines = [
        "# Preregistration (generated by `topo-pilot prereg` at the end of S2)", "",
        f"- **Date / git SHA:** {date.today().isoformat()} / {producer_version(cfg.repo_root)}",
        f"- **Resolved config hash:** {cfg.config_hash}; full `base.yaml` embedded in §7.", "",
        "## 1. Hypotheses and decision rules (verbatim from RESEARCH_SUMMARY)", "",
        _section(summary, "## 2."), "", _section(summary, "### 7.4"), "",
        _section(summary, "### 7.5"), "", _section(summary, "### 7.6"), "",
        "## 2. Calibration outcome (S2)", "", *sigma_table(rows), "",
        f"**Selected σ = {sigma!r}**. Rule path: "
        f"{'first-pass' if status == 'ok' else status}.", "",
        "## 3. Discriminability of unlearned spaces (S2, replicate "
        f"{cfg.base['seeds']['masters'][0]}, all {n_panels} panels)", "",
        *disc_table(rows, n_panels), "",
        "World-difference rule (D-023): a space differs if S_cyl > S_sq in ≥ 7 of 8 panels.", "",
        f"**Which hypotheses are decidable (conductor note):** {conductor_note or '<to fill>'}",
        "", "## 4. Fixed analysis choices", "",
        f"Primary hook `{cfg.base['model']['primary_hook']}` at checkpoint "
        f"{cfg.base['training']['primary_checkpoint']}; {n_panels} panels × "
        f"{cfg.base['data']['panel_size']} histories at p = 32 (HistoryIndex artifacts of S2); "
        "activations: raw Euclidean; distributions: Hellinger; S = max finite H₁ persistence / "
        "q95 of positive distances; F1 rule: ≥ 7/8 positive panels in each of 3 replicates and "
        "median D > u_r (strict); learning gate captured ≥ 0.8.", "",
        "## 5. Planned runs and cut paths", "", "```yaml",
        yaml.safe_dump({k: cfg.stages[k] for k in ("S3", "S4", "S5", "cut_paths")},
                       sort_keys=False).strip(), "```", "",
        "## 6. Approval", "", "Owner approval at checkpoint H1: <name, date>.", "",
        "## 7. base.yaml", "", "```yaml",
        (cfg.repo_root / "configs" / "base.yaml").read_text(encoding="utf-8").strip(), "```", ""]
    path = cfg.repo_root / "PREREGISTRATION.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
