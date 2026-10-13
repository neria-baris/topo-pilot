"""Report for exit level E4 (S7 + S8), from MetricRecords and GateReports only.

``topo-pilot report --level E4`` writes ``reports/E4/summary.md``, ``fig_probes.png`` and
``fig_circular.png``. Order: the primary hypotheses as decided at E2/E3 (unchanged), the
decision rule H3′, the secondary X4 items, then the S7 controls, probes, circular coordinates
and sensitivity (all descriptive or robustness checks, D-047), then the S8 reproducibility
checks (D-048). Missing data prints "not run", never a number.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from topo_pilot.contracts import ArtifactStore, MetricRow

from .report import _fmt
from .report_e2 import _one, _pick, analysis_rows, replicates, verdict
from .report_e3 import H3_READING, H4_READING, h4_status, s6_rows, x4_compare
from .report_e4_s7 import (
    circular_figure,
    circular_table,
    control_runs,
    control_table,
    controls_ph_table,
    gate_lines,
    probe_figure,
    probe_table,
    rerun_table,
    s7_rows,
    sensitivity_table,
)
from .report_x4 import _verdict, x4_rows

ORDER_NOTE = ("Primary hypotheses (PREREGISTRATION.md) were decided at E2/E3 and are repeated "
              "unchanged. H3′ is a decision rule approved at H3 (D-037). X4 items are "
              "secondary. Everything from S7 is either descriptive or a robustness check of a "
              "primary verdict, with its details fixed before any S7 result existed (D-047). "
              "None of it changes a primary verdict.")
U_NOTE = ("Under U the last symbol reveals the state, so G_C = 0 and the learning gate is "
          "undefined by construction. The U sanity check compares regret with the gain "
          "G_U = KL(q_C ‖ πE) of the exact predictor over the unigram marginal (D-047, "
          "descriptive). Its belief cloud is the set of simplex vertices, so U is not a PH "
          "positive control (RESEARCH_PLAN §3.3). The PH of the U models is descriptive.")
PROBE_NOTE = ("Fit on dev panels 1–6, λ chosen on dev panels 7–8, scored once on the 8 test "
              "panels. One-hot w₃₂ is the best affine decoder from the last symbol, so it "
              "bounds every decoder that uses r_w alone. F₁ = b³²TE is the exact next-symbol "
              "distribution: decoding b³² from it measures how much of the belief is linearly "
              "recoverable from what the next-token objective requires.")
CIRC_NOTE = ("Agreement A = max(|mean e^{i(φ−θ)}|, |mean e^{i(φ+θ)}|) ∈ [0, 1], with φ the "
             "circular coordinate from the top H₁ cocycle (F₄₇, mid-lifetime) and θ = 2πx(z₃₂)/12. "
             "The null permutes θ over the 512 histories of a panel (1000 draws). These values "
             "use the latent state (privileged_eval) and are descriptive. On the square, x is "
             "not periodic, so the same statistic serves as a comparison.")
SENS_NOTE = ("One factor at a time: chord = Euclidean distance of normalised activations; pca32 "
             "= PCA-32 fitted on the same run's dev activations at the same checkpoint; M256 = "
             "the first 256 histories of each panel; sqrt_js = √JSD for belief clouds (it "
             "changes Δgeom and H3′ only). Verdicts are robustness checks and never replace "
             "the primary verdict. Under P, the F1 rule stays one-sided (PREREGISTRATION §3).")
S8_NOTE = ("Clean rerun: a fresh clone of the committed HEAD with an empty artifact store, "
           "run with the same interpreter and the same locked environment on the same machine. "
           "It is not a different machine. Records that embed measured wall time or "
           "throughput are compared without those rows (D-048).")


def _h2_summary(rows: Sequence[MetricRow]) -> str:
    out = []
    for m in ("delta_geom_all", "delta_geom_same_last_symbol"):
        vals = [r.value for r in _pick(rows, "geometry", m) if r.value is not None]
        out.append(f"{sum(v > 0 for v in vals)}/{len(vals)}" if vals else "not run")
    return f"Δgeom > 0 in {out[0]} run-panels (all pairs), {out[1]} (same w₃₂)"


def _f1_values(rows: Sequence[MetricRow]) -> str:
    """``median D/u_r`` per replicate."""
    return ", ".join(f"{_fmt(_one(rows, 'F1', 'median_D', replicate=s))}/"
                     f"{_fmt(_one(rows, 'F1', 'u', replicate=s))}" for s in replicates(rows))


def _dg_fraction(rows: Sequence[MetricRow]) -> str:
    vals = [r.value for r in _pick(rows, "geometry", "delta_geom_all") if r.value is not None]
    return _fmt(sum(v > 0 for v in vals) / len(vals), 2) if vals else "not run"


def primary_section(rows_o, rows_p, dyn_o, x4, s4_h0, ctrl) -> list[str]:
    h4, h4_reason = h4_status(dyn_o)
    h3p, h3p_reason = _verdict(x4, "x4:h3p:V0", "H3prime_verdict", "P")
    n_h0 = [v.get("h0_passed") for (w, c, s), v in ctrl.items() if c == "N"]
    s4_ok = _one(s4_h0, "H0", "nll_p32")
    lines = ["| hypothesis | decided at | verdict | key values |", "|---|---|---|---|",
             f"| F1 (O, primary) | E2 | {verdict(rows_o)[0]} | median D / u_r per replicate: "
             f"{_f1_values(rows_o)} |",
             f"| H2 (O) | E2 | sign-consistent (see values) | {_h2_summary(rows_o)} |",
             f"| H3 (F1 rule under P) | E3 | {verdict(rows_p)[0]}: uninformative by design "
             f"| median D / u_r: {_f1_values(rows_p)} |",
             f"| H4 (timing, cylinder runs under O) | E3 | {h4} | {h4_reason or '–'} |",
             f"| H3′ (decision rule under P, D-037) | E3 | {h3p} | {h3p_reason or '–'} |",
             f"| H0 (N models) | E2 + S7 | {'pass' if s4_ok is not None else 'not run'} (S4), "
             f"{sum(bool(x) for x in n_h0 if x is not None)}/{len(n_h0)} S7 N runs pass "
             "| NLL at p = 32 not below H(W) beyond the bootstrap CI |", ""]
    lines += [H3_READING.get(verdict(rows_p)[0], ""), "", H4_READING.get(h4, ""), ""]
    return lines


def build_e4(store: ArtifactStore, out_dir: Path, final: int = 5000) -> Path:
    """Write ``summary.md`` and the two figures; returns the summary path."""
    rows_o, rows_p = analysis_rows(store, "S4"), analysis_rows(store, "S5")
    dyn_o = s6_rows(store, "dynamics", "O")
    x4 = x4_rows(store)
    ctrl = control_runs(store)
    probes, circ = s7_rows(store, "probes"), s7_rows(store, "circular")
    sens, controls = s7_rows(store, "sensitivity"), s7_rows(store, "controls")
    primary = {c: (f"{verdict(r)[0]} ({_f1_values(r)})",
                   _verdict(x4, "x4:h3p:V0", "H3prime_verdict", c)[0], _dg_fraction(r))
               for c, r in (("O", rows_o), ("P", rows_p))}
    lines = ["# E4: controls, probes, circular coordinates, sensitivity (S7) and clean rerun (S8)",
             "", ORDER_NOTE, "",
             "## 1. Primary hypotheses (unchanged since E2/E3)", "",
             *primary_section(rows_o, rows_p, dyn_o, x4, rows_o, ctrl),
             "## 2. Secondary: X4 under O and P (PREREGISTRATION_X4.md)", "",
             *x4_compare(x4), "",
             "## 3. S7 controls: U and extra N runs", "", U_NOTE, "",
             *control_table(ctrl, rows_o), "", *controls_ph_table(controls, final), "",
             "## 4. S7 probes (descriptive)", "", PROBE_NOTE, "", *probe_table(probes), "",
             "![probes](fig_probes.png)", "",
             "## 5. S7 circular coordinates (descriptive, privileged_eval)", "", CIRC_NOTE, "",
             *circular_table(circ, final), "", "![circular](fig_circular.png)", "",
             "## 6. S7 sensitivity (robustness checks, one factor at a time)", "", SENS_NOTE,
             "", *sensitivity_table(sens, primary), "",
             *gate_lines(store, "S7", "G-G"), "",
             "## 7. S8 reproducibility", "", S8_NOTE, "", *rerun_table(s7_rows(store, "rerun")),
             "", *_integrity_lines(s7_rows(store, "integrity"), s7_rows(store, "reports")), "",
             *gate_lines(store, "S8", "G-H"), "",
             "Interpretation, limitations and post hoc observations, written after these "
             "tables: [interpretation.md](interpretation.md).", "",
             "**Not run:** X4-causal (interventions), X5, X6 and the extensions X1–X3. No "
             "claim is made about causal use of the structure or about natural-language "
             "LLMs.", ""]
    if probes:
        probe_figure(probes, out_dir / "fig_probes.png")
    if circ:
        circular_figure(circ, final, out_dir / "fig_circular.png")
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = out_dir / "summary.md"
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def _integrity_lines(integ: Sequence[MetricRow], reports: Sequence[MetricRow]) -> list[str]:
    if not integ and not reports:
        return ["Store integrity and report reproduction: not run"]
    n, ok = _one(integ, "integrity", "n_artifacts"), _one(integ, "integrity", "n_verified")
    bad = next((r for r in integ if r.metric_id == "n_problems"), None)
    same = [r for r in reports if r.metric_id == "identical"]
    return [f"Store integrity: {_fmt(ok, 0)}/{_fmt(n, 0)} artifacts complete with present "
            f"parents and verified payload checksums; problems: "
            f"{_fmt(bad.value, 0) if bad else 'not run'}"
            + (f" ({bad.uncertainty_kind})" if bad and bad.uncertainty_kind else "") + ".",
            f"Report reproduction (E0/E2/E3, every generated file, byte for byte): "
            f"{sum(r.value == 1 for r in same)}/{len(same)} identical"
            + (" (" + ", ".join(r.space.removeprefix("reports:") for r in same if r.value != 1)
               + " differ)" if any(r.value != 1 for r in same) else "") + "."]
