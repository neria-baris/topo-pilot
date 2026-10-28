"""Figures for docs/research_summary/research_summary.tex ("READ ME FIRST").

Every plotted number comes from a file in the repository or in the execution records
next to it, named in a comment beside the number and in the figure caption. Nothing is
estimated or invented here.

Usage (from any directory):

    .venv/Scripts/python.exe -s docs/research_summary/make_figures.py            # use snapshots
    .venv/Scripts/python.exe -s docs/research_summary/make_figures.py --refresh  # re-read stores

Inputs that live outside this repository (the X6 stage-1 store and the per-study CPU
ledgers) are copied into two small snapshot files under docs/research_summary/data/ by
``--refresh``, so the figures can be rebuilt on a machine that has only the repository.

X6 stage 1 (X6S1) is sealed until its decision stage E3 (protocol X6S1-FROZEN-v1 §4.7,
§9 S9, §12 item 11). ``--refresh`` therefore copies ONLY the gate name, status and UTC
time of each GATES.jsonl record (never its ``values`` field), the stage name, stop and
time of each STAGES.jsonl record, the CPU/wall accounting of each metered run, and the
bundle id, steps and K of each wave. It never opens ``sealed/``, ``stages/*/`` payloads,
pools, tables or cloud files, and it never writes into any store.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Patch, Rectangle  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]                      # .../topo-pilot/topo-pilot
ROOT = REPO.parent                          # .../topo-pilot (stores, mailbox)
FIG = HERE / "figures"
DATA = HERE / "data"
STORE_X6S1 = ROOT / "x6-stage1-store"

# ---- palette (dataviz reference palette, light mode; print document) -------------------
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
S1, S2, S3, S4, S5, S7 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6"
GOOD, WARN, SERIOUS, CRIT = "#0ca30c", "#fab219", "#ec835a", "#d03b3b"
OUTCOME = {  # outcome class -> (colour, marker, legend label)
    "pass": (GOOD, "o", "supported / PASS / GO"),
    "fail": (CRIT, "X", "rejected / FAIL / NO-GO / NOT_LEARNED"),
    "inc": (WARN, "s", "INCONCLUSIVE (stopped at a gate)"),
    "excl": (S1, "D", "EXCLUSION (bounded null)"),
    "desc": (MUTED, "^", "descriptive / exploratory / uninformative"),
    "open": ("#ffffff", "o", "sealed / pending"),
}

plt.rcParams.update({
    "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5, "legend.fontsize": 7.5,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.edgecolor": INK2,
    "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "lines.linewidth": 1.6, "figure.dpi": 100, "savefig.bbox": "tight",
    "pdf.fonttype": 42, "font.family": "DejaVu Sans",
})


def save(fig, name: str) -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f"{name}.pdf")
    fig.savefig(FIG / f"{name}.png", dpi=200)
    plt.close(fig)
    print("wrote", FIG / f"{name}.pdf")


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8-sig"))


# =========================================================================================
# Snapshot refresh (read-only access to the stores; see module docstring)
# =========================================================================================
LEDGERS = [  # (label, store directory, note) -- cumulative_cpu_s of each cpu_ledger.json
    ("learning speed (6 models)", "x5g1-research-store", "training"),
    ("orientability, trained (2 models)", "d2a-store", "training"),
    ("crossing order, oracle", "x6-stage0-oracle-store", "oracle"),
    ("crossing order, trained", "x6-stage1-store", "eval"),
    ("counterfactual forcing (incl. tests)", "c1prime-store", "oracle+model"),
    ("beyond 4 symbols", "k4b-store", "oracle+model"),
    ("component identity, oracle", "x2a-stage0-oracle-store", "oracle"),
    ("orientability, oracle", "d1-seam-oracle-store", "oracle"),
    ("beyond 4 symbols, 1st attempt", "x4-circle-history-feas-store-0015", "oracle+model"),
    ("erasing the coordinate (gates)", "x4f-gates-research-store", "model"),
    ("oracle suffix profile", "x4-oracle-profile-store-0014", "oracle"),
    ("beyond 8 symbols (cohort)", "x4-history-feas-store", "oracle"),
    ("chart diagnostic", "chart-diag-store-0023", "model"),
    ("world sweep, oracle", "hws-store", "oracle"),
    ("control placebo check", "x6zc-store", "model"),
    ("necessity and decoy", "c2nd-store", "model"),
    ("training pilot (2 models)", "hwsb-store", "training"),
]


def _jsonl(path: Path):
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            yield json.loads(line)


def refresh() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    s = {"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         "source": "x6-stage1-store: GATES.jsonl (gate,status,utc only), STAGES.jsonl "
                   "(stage,stop,utc), superseded/*/GATES.jsonl (gate,status,utc), "
                   "cpu_ledger.json (accounting only), stages/E0/frozen_C*.json "
                   "(bundle_id, steps, K only)"}
    # --- gate records: gate, status, utc ONLY (never 'values') ---
    s["gates"] = [{"utc": r["utc"], "gate": r["gate"], "status": r["status"]}
                  for r in _jsonl(STORE_X6S1 / "GATES.jsonl")]
    s["superseded_gates"] = {}
    for d in sorted((STORE_X6S1 / "superseded").iterdir()):
        g = d / "GATES.jsonl"
        if g.is_file():
            s["superseded_gates"][d.name] = [
                {"utc": r["utc"], "gate": r["gate"], "status": r["status"]} for r in _jsonl(g)]
    s["stages"] = [{"utc": r["utc"], "stage": r["stage"], "stop": r["stop"]}
                   for r in _jsonl(STORE_X6S1 / "STAGES.jsonl")]
    led = load_json(STORE_X6S1 / "cpu_ledger.json")
    keep = ("label", "status", "utc_started", "utc_end", "measured_cpu_s", "wall_s",
            "exit_code")
    s["ledger"] = [{k: e.get(k) for k in keep} for e in led["entries"]]
    s["cumulative_cpu_s"] = led["cumulative_cpu_s"]
    s["waves"] = {}
    for w in ("C0", "C1", "C2"):
        f = load_json(STORE_X6S1 / "stages" / "E0" / f"frozen_{w}.json")
        s["waves"][w] = {"bundle_id": f["bundle_id"], "steps": f["steps"], "K": f["K"]}
    (DATA / "x6s1_status.json").write_text(json.dumps(s, indent=1), encoding="utf-8")
    rep = STORE_X6S1 / "stages" / "E3z" / "report.json"
    if rep.is_file():  # written by E3.9, which unseals; only the decision-stage report is read
        r = load_json(rep)
        keep_r = {k: r[k] for k in ("outcome", "rule", "licence", "qualifiers", "beta_bar", "lb",
                                    "learn", "learn_test", "models", "flags", "sharp_target")}
        keep_r["natural"] = {k: r["natural"][k] for k in ("beta_ord", "C_s", "mean", "lb", "cord",
                                                          "tail", "ctrl")}
        keep_r["designed"] = {m: {k: v for k, v in d.items() if k in ("R_W2", "beta_W2",
                              "Delta_W3", "rho_W2")} for m, d in r["designed"].items()
                              if isinstance(d, dict) and "R_W2" in d}
        keep_r["ord_d"] = r["designed"]["ord_d"]
        keep_r["source"] = "x6-stage1-store/stages/E3z/report.json (E3.9, after unsealing)"
        (DATA / "x6s1_result.json").write_text(json.dumps(keep_r, indent=1), encoding="utf-8")
    comp = {"generated_utc": s["generated_utc"], "studies": []}
    for label, store, kind in LEDGERS:
        p = ROOT / store / "cpu_ledger.json"
        if p.is_file():
            comp["studies"].append({"label": label, "store": store, "kind": kind,
                                    "cumulative_cpu_s": load_json(p)["cumulative_cpu_s"]})
    (DATA / "compute_ledgers.json").write_text(json.dumps(comp, indent=1), encoding="utf-8")
    print("refreshed", DATA)


# =========================================================================================
# Figure 1: programme timeline
# =========================================================================================
# (date, lane, label, outcome class, source)
EVENTS = [
    ("10-13", 0, "pilot: measurement gate PASS", "pass", "state/DECISIONS.md D-017"),
    ("10-13", 0, "pilot: F1 supported (O)", "pass", "reports/E2/summary.md"),
    ("10-13", 0, "pilot: H3 uninformative;\nH3′ supported", "desc", "reports/E3/summary.md"),
    ("10-13", 0, "pilot: H4 (timing) rejected", "fail", "reports/E3/summary.md"),
    ("10-13", 0, "pilot: clean rerun FAIL\n(1 missing record)", "fail", "state/DECISIONS.md D-049"),
    ("10-13", 3, "two-step distinctions\nINCONCLUSIVE", "inc", "state/DECISIONS.md D-052"),
    ("10-14", 3, "two-step distinctions\n(fresh) scoped NO-GO", "fail", "state/DECISIONS.md D-054/055"),
    ("10-14", 1, "circular-baseline\naudit (descr.)", "desc", "state/DECISIONS.md D-057"),
    ("10-14", 2, "erasing the coordinate\nINCONCLUSIVE", "inc", "state/DECISIONS.md D-063"),
    ("10-14", 1, "beyond 8 symbols:\nheadroom FAIL", "fail", "x4-history-feas-store/GATE_REPORT.json"),
    ("10-14", 4, "learning speed\nREJECTED", "fail", "state/DECISIONS.md D-073"),
    ("10-14", 1, "oracle suffix\nprofile (expl.)", "desc", "state/DECISIONS.md D-074"),
    ("10-15", 1, "beyond 4 symbols, 1st\nattempt INCONCLUSIVE", "inc", "agent-handoff/jobs/0018/review.md"),
    ("10-15", 3, "orientability (oracle)\nPASS", "pass", "agent-handoff/jobs/0020/review.md"),
    ("10-15", 1, "chart diagnostic\nGO", "pass", "agent-handoff/jobs/0023/review.md"),
    ("10-15", 1, "component identity\n(oracle) GO", "pass", "agent-handoff/jobs/0025/review.md"),
    ("10-15", 3, "orientability (trained)\nNOT_LEARNED", "fail", "agent-handoff/jobs/0033/review.md"),
    ("10-16", 2, "counterfactual forcing\nINCONCLUSIVE", "inc", "agent-handoff/jobs/0044/review.md"),
    ("10-17", 1, "beyond 4 symbols\nEXCLUSION", "excl", "agent-handoff/jobs/0057/review.md"),
    ("10-18", 5, "crossing order (oracle)\nGO", "pass", "agent-handoff/jobs/0066/review.md"),
    ("10-20", 5, "crossing order (trained):\npreparation PASS", "pass", "agent-handoff/jobs/0089, 0092 review.md"),
    ("10-20", 5, "crossing order (trained):\nlearnability GO", "pass", "agent-handoff/jobs/0093/review.md"),
    ("10-20", 5, "crossing order (trained):\n12 models admitted", "pass", "agent-handoff/jobs/0094/review.md"),
    ("10-21", 5, "crossing order (trained):\nINCONCLUSIVE", "inc", "agent-handoff/jobs/0099/review.md"),
    ("10-26", 2, "readout attribution:\nUSED (3/3 models)", "pass", "agent-handoff/jobs/0115/review.md"),
    ("10-26", 1, "world sweep (oracle):\nworld SELECTED", "pass", "agent-handoff/jobs/0136/review.md"),
    ("10-27", 5, "control placebo check:\nUNEXPLAINED", "desc", "agent-handoff/jobs/0155/review.md"),
    ("10-27", 2, "necessity: code dominant;\ndecoy NOT_USED", "pass", "agent-handoff/jobs/0167/review.md"),
    ("10-28", 1, "training pilot (new world):\nPASS", "pass", "agent-handoff/jobs/0175/review.md"),
]
LANE_HEAD = [chr(10).join(x) for x in (("Pilot",), ("P1", "origin"), ("P2", "causal use"),
             ("P3", "horizons"), ("learning", "speed"), ("crossing", "order"))]
LANES = ["Pilot", "P1: origin of\ncircular structure", "P2: causal use",
         "P3: necessity &\nhorizons", "Secondary:\nlearning speed",
         "Secondary: crossing\norder (non-abelian)"]


def fig_timeline() -> None:
    n = len(EVENTS)
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    prev = None
    for i, (d, lane, label, oc, _src) in enumerate(EVENTS):
        if d != prev:
            ax.axhline(i - 0.5, color=GRID, lw=0.8)
            ax.text(-0.75, i, "2026-" + d, ha="right", va="center", fontsize=7, color=INK2)
            prev = d
        col, mk, _ = OUTCOME[oc]
        ax.plot([0, len(LANES) - 1], [i, i], color="#f3f2ef", lw=0.6, zorder=1)
        ax.scatter([lane], [i], s=46, marker=mk, color=col,
                   edgecolor=INK if oc == "open" else "white", linewidth=0.9, zorder=3)
        ax.text(len(LANES) - 0.55, i, label.replace("\n", " "), ha="left", va="center",
                fontsize=6.6, color=INK)
    ax.set_xticks(range(len(LANES)))
    ax.set_xticklabels(LANE_HEAD, fontsize=6.4)
    ax.xaxis.tick_top()
    ax.set_yticks([])
    ax.set_ylim(n - 0.5, -0.6)
    ax.set_xlim(-0.6, len(LANES) + 2.6)
    ax.grid(False)
    for sp in ("left", "bottom", "top", "right"):
        ax.spines[sp].set_visible(False)
    handles = [Line2D([], [], marker=m, ls="", color=c, markeredgecolor=INK if k == "open" else c,
                      markersize=6, label=l) for k, (c, m, l) in OUTCOME.items()]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.45, 0.0), ncol=3,
              frameon=False, fontsize=6.5)
    save(fig, "fig01_timeline")


def fig_outcomes() -> None:
    counts = {}
    for _d, lane, _l, oc, _s in EVENTS:
        counts.setdefault(lane, {}).setdefault(oc, 0)
        counts[lane][oc] += 1
    order = ["pass", "excl", "desc", "inc", "fail", "open"]
    fig, ax = plt.subplots(figsize=(6.6, 2.7))
    for lane in range(len(LANES)):
        left = 0
        for oc in order:
            n = counts.get(lane, {}).get(oc, 0)
            if not n:
                continue
            col = OUTCOME[oc][0]
            ax.barh(lane, n, left=left, color=col, edgecolor=INK if oc == "open" else "white",
                    linewidth=1.5 if oc != "open" else 0.8, height=0.62)
            ax.text(left + n / 2, lane, str(n), ha="center", va="center", fontsize=7,
                    color=INK)
            left += n
    ax.set_yticks(range(len(LANES)))
    ax.set_yticklabels([l.replace("\n", " ") for l in LANES])
    ax.invert_yaxis()
    ax.set_xlabel("number of recorded stage outcomes (events of Fig. 1)")
    ax.grid(axis="y", visible=False)
    handles = [Patch(facecolor=OUTCOME[k][0], edgecolor=INK if k == "open" else OUTCOME[k][0],
                     label=OUTCOME[k][2]) for k in order]
    ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=6.5)
    save(fig, "fig02_outcomes")


# =========================================================================================
# Figure 3: E1, unlearned spaces (README.md "Earlier exit (E1, no model)")
# =========================================================================================
def fig_e1() -> None:
    spaces = ["belief $b^{(32)}$", "last-symbol $b^{(1)}$", "next-symbol $F_1$",
              "two-symbol $F_2$"]
    O_cyl, O_sq = [0.671, 0.324, 0.556, 0.614], [0.321, 0.165, 0.189, 0.216]
    P_cyl, P_sq = [0.323, 0.324, 0.194, 0.202], [0.310, 0.165, 0.241, 0.242]
    panels_O, panels_P = ["8/8"] * 4, ["5/8", "8/8", "1/8", "2/8"]
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.6), sharey=True)
    w = 0.38
    for ax, cyl, sq, pan, t in ((axs[0], O_cyl, O_sq, panels_O, "smooth emission O"),
                                (axs[1], P_cyl, P_sq, panels_P, "axis-permuted emission P")):
        xs = range(len(spaces))
        ax.bar([i - w / 2 for i in xs], cyl, w, color=S1, label="cylinder", edgecolor="white")
        ax.bar([i + w / 2 for i in xs], sq, w, color=S2, label="square", edgecolor="white")
        for i in xs:
            ax.text(i, max(cyl[i], sq[i]) + 0.02, f"cyl>sq {pan[i]}", ha="center", fontsize=6.3,
                    color=INK2)
        ax.axhline(0.10, color=MUTED, ls="--", lw=1)
        ax.text(-0.45, 0.105, "Gaussian floor ≤ 0.10", ha="left", va="bottom", fontsize=6.3,
                color=INK2)
        ax.set_xticks(list(xs))
        ax.set_xticklabels(spaces, rotation=15)
        ax.set_title(t, loc="left")
        ax.grid(axis="x", visible=False)
    axs[0].set_ylabel("median $S$ over 8 panels")
    axs[1].legend(*axs[0].get_legend_handles_labels(), frameon=False, loc="upper right")
    axs[0].set_ylim(0, 0.75)
    save(fig, "fig03_e1_oracle_spaces")


# =========================================================================================
# Figure 4: F1 contrast per panel (reports/he_summary/data/d.json) and baselines
# =========================================================================================
UR = {"O": {"1729": 0.0966, "2718": 0.0839, "3141": 0.0842},   # reports/E2/summary.md
      "P": {"1729": 0.0656, "2718": 0.0893, "3141": 0.0722}}   # reports/E3/summary.md


def fig_f1() -> None:
    d = load_json(REPO / "reports" / "he_summary" / "data" / "d.json")
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.7), gridspec_kw={"width_ratios": [1.5, 1]})
    ax = axs[0]
    x = 0
    ticks, labels = [], []
    for cond, col in (("O", S1), ("P", S2)):
        for seed in ("1729", "2718", "3141"):
            vals = d[cond][seed]
            xs = [x + (i - 3.5) * 0.05 for i in range(len(vals))]
            ax.scatter(xs, vals, s=14, color=col, edgecolor="white", linewidth=0.5, zorder=3)
            med = sorted(vals)[3:5]
            ax.plot([x - 0.25, x + 0.25], [sum(med) / 2] * 2, color=INK, lw=1.6)
            ax.plot([x - 0.25, x + 0.25], [UR[cond][seed]] * 2, color=CRIT, lw=1.2, ls="--")
            ticks.append(x)
            labels.append(f"{cond}\n{seed}")
            x += 1
        x += 0.5
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    ax.set_ylabel("$D_{r,i}$ per panel")
    ax.set_title("(a) F1 contrast, 8 panels per replicate", loc="left")
    ax.legend(handles=[Line2D([], [], color=INK, lw=1.6, label="median"),
                       Line2D([], [], color=CRIT, lw=1.2, ls="--", label="noise envelope $u_r$")],
              frameon=False, loc="upper right", fontsize=6.5)
    ax.grid(axis="x", visible=False)
    # (b) baseline ratios under O -- reports/E2/summary.md "Representation baselines"
    ax = axs[1]
    ratios = {"R1 last-symbol emb.": [0.89, 0.47, 0.54], "R2 prev.-token mix": [0.17, 0.20, 0.19],
              "R3 context average": [0.02, 0.10, 0.08]}
    cols = [S1, S3, S4]
    for j, (k, v) in enumerate(ratios.items()):
        for i, r in enumerate(v):
            ax.bar(j + (i - 1) * 0.26, r, 0.24, color=cols[j], edgecolor="white")
    ax.set_xticks(range(3))
    ax.set_xticklabels([k.replace(" ", chr(10)) for k in ratios], fontsize=6.3)
    ax.set_ylabel("baseline median $D$ / model median $D$")
    ax.set_ylim(0, 1)
    ax.set_title("(b) baselines under O (bars: 1729, 2718, 3141)", loc="left", fontsize=8)
    ax.grid(axis="x", visible=False)
    save(fig, "fig04_f1_contrast")


# =========================================================================================
# Figure 5: training dynamics (reports/he_summary/data/dyn.json)
# =========================================================================================
GC = {"cylinder": 0.2649, "square": 0.2360}   # reports/E2/summary.md, G_C under O


def fig_dynamics() -> None:
    dyn = load_json(REPO / "reports" / "he_summary" / "data" / "dyn.json")["O"]
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.7))
    for key, series in dyn["S"].items():
        world = key.split("-")[0]
        xs = [max(p[0], 10) for p in series]
        axs[0].plot(xs, [p[1] for p in series], color=S1 if world == "cylinder" else S2,
                    marker="o", ms=3, alpha=0.9)
    for key, series in dyn["regret"].items():
        world = key.split("-")[0]
        xs = [max(p[0], 10) for p in series]
        axs[1].plot(xs, [p[1] for p in series], color=S1 if world == "cylinder" else S2,
                    marker="o", ms=3, alpha=0.9)
    for w, c in (("cylinder", S1), ("square", S2)):
        axs[1].axhline(GC[w], color=c, ls="--", lw=1)
    axs[1].text(4800, GC["cylinder"] * 1.12, "$G_C$ (cyl., sq.)", ha="right", fontsize=6.5,
                color=INK2)
    for ax in axs:
        ax.set_xscale("log")
        ax.set_xlabel("training step (step 0 drawn at 10)")
        ax.axvline(50, color=MUTED, lw=0.8, ls=":")
        ax.axvline(100, color=MUTED, lw=0.8, ls=":")
    axs[0].set_ylabel("$S$ (panel 1, resid_post_3)")
    axs[1].set_ylabel("regret (nats)")
    axs[1].set_yscale("log")
    axs[0].set_title("(a) persistent-$H_1$ score, condition O", loc="left")
    axs[1].set_title("(b) regret vs. context gain $G_C$", loc="left")
    axs[0].legend(handles=[Line2D([], [], color=S1, label="cylinder (3 seeds)"),
                           Line2D([], [], color=S2, label="square (3 seeds)")], frameon=False)
    save(fig, "fig05_dynamics")


# =========================================================================================
# Figure 6: layer sweep (reports/E3/summary.md "Layer sweep")
# =========================================================================================
def fig_layers() -> None:
    hooks = ["embed", "resid_post_0", "resid_post_1", "resid_post_2", "resid_post_3",
             "ln_final_out", "concat"]
    O = [[0.110, 0.104, 0.105], [0.130, 0.153, 0.161], [0.148, 0.184, 0.162],
         [0.175, 0.186, 0.172], [0.158, 0.176, 0.173], [0.283, 0.290, 0.273],
         [0.166, 0.188, 0.170]]
    P = [[-0.040, 0.025, -0.003], [-0.003, 0.008, 0.003], [0.013, 0.002, -0.006],
         [-0.004, 0.044, 0.005], [0.021, 0.034, 0.034], [0.016, 0.043, 0.013],
         [0.008, 0.046, 0.010]]
    fig, ax = plt.subplots(figsize=(6.6, 2.5))
    for vals, col, lab, off in ((O, S1, "O", -0.12), (P, S2, "P", 0.12)):
        for i, v in enumerate(vals):
            ax.scatter([i + off] * 3, v, color=col, s=16, edgecolor="white", linewidth=0.5,
                       zorder=3, label=lab if i == 0 else None)
            ax.plot([i + off - 0.08, i + off + 0.08], [sorted(v)[1]] * 2, color=INK, lw=1.2)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xticks(range(len(hooks)))
    ax.set_xticklabels(hooks, rotation=12)
    ax.set_ylabel("median $D$ per replicate")
    ax.legend(frameon=False, title=None, loc="upper left")
    ax.grid(axis="x", visible=False)
    save(fig, "fig06_layer_sweep")


# =========================================================================================
# Figure 7: probes and circular coordinates (reports/E4/summary.md §4, §5)
# =========================================================================================
def fig_probes_circular() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw={"width_ratios": [1.25, 1],
                                                                  "wspace": 0.55})
    ax = axs[0]
    probes = [("activations (5000) → $b^{(32)}$", 0.829, (0.822, 0.835), 0.378, (0.355, 0.398)),
              ("activations (0) → $b^{(32)}$", 0.483, (0.458, 0.508), 0.167, (0.148, 0.185)),
              ("exact $F_1$ → $b^{(32)}$", 0.838, (0.832, 0.843), 0.382, (0.367, 0.396)),
              ("one-hot $w_{32}$ → $b^{(32)}$", 0.421, (0.401, 0.438), 0.144, (0.133, 0.153)),
              ("activations (5000) → $r_w$", 0.974, (0.965, 0.985), 0.825, (0.817, 0.835)),
              ("activations → shuffled $b^{(32)}$", -0.010, (-0.018, -0.005), -0.027, (-0.028, -0.025))]
    for i, (lab, o, orr, p, pr) in enumerate(probes):
        ax.barh(i - 0.19, o, 0.36, color=S1, edgecolor="white", label="O" if i == 0 else None)
        ax.barh(i + 0.19, p, 0.36, color=S2, edgecolor="white", label="P" if i == 0 else None)
        ax.plot(orr, [i - 0.19] * 2, color=INK, lw=1)
        ax.plot(pr, [i + 0.19] * 2, color=INK, lw=1)
    ax.set_yticks(range(len(probes)))
    ax.set_yticklabels([p[0] for p in probes], fontsize=6.8)
    ax.invert_yaxis()
    ax.set_xlabel("test $R^2$ (median over 6 runs; line: range)")
    ax.set_title("(a) ridge probes", loc="left")
    ax.legend(frameon=False, loc="center right", bbox_to_anchor=(1.0, 0.35))
    ax.grid(axis="y", visible=False)
    ax = axs[1]
    rows = [("O cyl., step 0", 0.069), ("O cyl., step 5000", 0.891), ("O sq., step 5000", 0.256),
            ("P cyl., step 5000", 0.053), ("U cyl., step 5000", 0.601)]
    ceil = {"O cyl., step 0": 0.915, "O cyl., step 5000": 0.915, "O sq., step 5000": 0.921,
            "P cyl., step 5000": 0.819, "U cyl., step 5000": 1.000}
    for i, (lab, v) in enumerate(rows):
        ax.barh(i, v, 0.55, color=S3, edgecolor="white")
        ax.plot([ceil[lab]] * 2, [i - 0.3, i + 0.3], color=INK, lw=1.4)
        ax.text(v + 0.02, i, f"{v:.3f}", va="center", fontsize=6.5)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=6.8)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("agreement $A$ with $x$-angle (median)")
    ax.set_title("(b) circular coordinate", loc="left")
    ax.legend(handles=[Line2D([], [], color=INK, lw=1.4, label="exact-belief ceiling")],
              frameon=False, loc="lower right", fontsize=6.5)
    ax.grid(axis="y", visible=False)
    save(fig, "fig07_probes_circular")


# =========================================================================================
# Figure 8: oracle profile (agent-handoff/jobs/0014/review.md) and K4b (jobs/0057/review.md)
# =========================================================================================
def fig_origin() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.7))
    ax = axs[0]
    K = [1, 2, 4, 8, 16]
    cal = [0.369099, 0.198450, 0.067034, 0.009247, 0.000177886]
    val = [0.376588, 0.195106, 0.069660, 0.009290, 0.000181326]
    ax.plot(K, cal, marker="o", color=S1, label="calibration")
    ax.plot(K, val, marker="s", color=S2, ls="--", label="validation")
    ax.axhline(0.01, color=CRIT, ls=":", lw=1.2)
    ax.text(1.05, 0.0115, "0.01 practical margin", fontsize=6.5, color=INK2)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(K)
    ax.set_xticklabels([str(k) for k in K])
    ax.set_xlabel("suffix length $K$  ($B_{32}=0$ by definition)")
    ax.set_ylabel("$B_K = E\\,\\|m_{32}-m_K\\|$")
    ax.set_title("(a) oracle profile (job 0014)", loc="left")
    ax.legend(frameon=False)
    ax = axs[1]
    models = ["1729", "2718", "3141"]
    L = [0.00640, 0.00740, 0.00667]
    U = [0.00777, 0.00891, 0.00823]
    pt = [0.00708, 0.00815, 0.00744]
    ax.axvspan(-0.01, 0.01, color="#eef5fd", lw=0)
    for i in range(3):
        ax.plot([L[i], U[i]], [i, i], color=S1, lw=2.2)
        ax.scatter([pt[i]], [i], color=S1, s=26, zorder=3, edgecolor="white")
    ax.plot([0.00791, 0.00933], [3.1, 3.1], color=S7, lw=2.2)
    ax.scatter([0.00854], [3.1], color=S7, s=26, zorder=3, edgecolor="white")
    ax.axvline(0.01, color=CRIT, ls=":", lw=1.2)
    ax.axvline(-0.01, color=CRIT, ls=":", lw=1.2)
    ax.axvline(0, color=INK2, lw=0.8)
    ax.set_yticks([0, 1, 2, 3.1])
    ax.set_yticklabels(["model 1729", "model 2718", "model 3141", "phase-only\noracle $\\Delta_4^{orc}$"])
    ax.set_xlim(-0.012, 0.014)
    ax.set_ylim(-0.5, 3.6)
    ax.set_xlabel("$\\Delta_4$ = E[$u\\cdot r_4$], fresh test (bounds at 0.05/3)")
    ax.set_title("(b) Beyond four symbols, fresh test: EXCLUSION", loc="left")
    ax.grid(axis="y", visible=False)
    save(fig, "fig08_origin_profile_k4b")


# =========================================================================================
# Figure 9: D-2a learnability gate (agent-handoff/jobs/0033/review.md)
# =========================================================================================
def fig_d2a() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.3))
    m = ["H3-s1", "H3-s2"]
    beta, lo, kap = [0.393, 0.262], [0.278, 0.136], [-0.890, -1.301]
    ax = axs[0]
    ax.bar(range(2), beta, 0.5, color=S1, edgecolor="white")
    for i in range(2):
        ax.plot([i, i], [lo[i], beta[i]], color=INK, lw=1)
        ax.scatter([i], [lo[i]], marker="_", color=INK, s=80)
    ax.axhline(0.30, color=CRIT, ls="--", lw=1)
    ax.text(-0.42, 0.31, "$\\beta_1\\geq0.30$", ha="left", fontsize=6.5, color=INK2)
    ax.axhline(0.679, color=S7, ls=":", lw=1.2)
    ax.text(-0.42, 0.70, "window-8 oracle $\\beta_1^{(8)}=0.679$", ha="left", fontsize=6.5,
            color=INK2)
    ax.set_xticks(range(2))
    ax.set_xticklabels(m)
    ax.set_ylim(0, 0.8)
    ax.set_ylabel("$\\beta_1$ (tick: 95% lower bound)")
    ax.set_title("(a) band-edge alignment", loc="left")
    ax.grid(axis="x", visible=False)
    ax = axs[1]
    ax.bar(range(2), kap, 0.5, color=S2, edgecolor="white")
    ax.axhline(0.20, color=CRIT, ls="--", lw=1)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.text(-0.42, 0.25, "$\\kappa_1\\geq0.20$", ha="left", fontsize=6.5, color=INK2)
    ax.set_xticks(range(2))
    ax.set_xticklabels(m)
    ax.set_ylim(-1.5, 0.5)
    ax.set_ylabel("$\\kappa_1$")
    ax.set_title("(b) gain over window-8", loc="left")
    ax.grid(axis="x", visible=False)
    save(fig, "fig09_d2a_gate")


# =========================================================================================
# Figure 10: X6 stage-0 oracle ladder (X6S1-FROZEN-v1 §2.1, quoting jobs/0066 certified values)
# =========================================================================================
def fig_x6_ladder() -> None:
    names = ["$G_\\emptyset$ (no transport)", "$G_8$ (last 8 symbols)", "$G_{parity}$",
             "$G_{H_1}$", "$G_{counts}$", "$G_{Parikh}$", "$D_{blk}$ (8-block)",
             "$J_8$ (window ≤ 8 share)"]
    vals = [10.5935, 8.85531, 7.7918, 2.9868, 2.7360, 2.6358965, 1.30972, 0.037201925]
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    cols = [MUTED, S7, S4, S3, S3, S1, S5, MUTED]
    ax.barh(range(len(vals)), vals, 0.6, color=cols, edgecolor="white")
    for i, v in enumerate(vals):
        ax.text(v + 0.12, i, f"{v:.3g}", va="center", fontsize=6.6)
    ax.axvline(1.0, color=CRIT, ls="--", lw=1)
    ax.legend(handles=[Line2D([], [], color=CRIT, ls="--", lw=1,
                              label="stage-0 O2 threshold for $G_{Parikh}$ (1e-3 nats)")],
              frameon=False, loc="lower right", fontsize=6.5)
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(names)
    ax.invert_yaxis()
    ax.set_xlabel("excess log-loss at $t=32$ under the natural law ($10^{-3}$ nats), exact")
    ax.grid(axis="y", visible=False)
    save(fig, "fig10_x6_stage0_ladder")


# =========================================================================================
# Figure 11: compute (cpu_ledger.json snapshots + artifacts/MetricRecords wall_time_s)
# =========================================================================================
PILOT_WALL_S = {  # artifacts/MetricRecords/<id>/extra.json, metric_id == "wall_time_s"
    "any-N-1729": 908.1, "any-N-2718": 1029.5, "any-N-3141": 1127.4,
    "cylinder-O-1729": 957.1, "cylinder-O-2718": 921.2, "cylinder-O-3141": 863.7,
    "cylinder-P-1729": 828.0, "cylinder-P-2718": 863.0, "cylinder-P-3141": 840.7,
    "cylinder-U-1729": 1290.2, "square-O-1729": 931.8, "square-O-2718": 817.0,
    "square-O-3141": 931.5, "square-P-1729": 788.4, "square-P-2718": 958.0,
    "square-P-3141": 934.5, "square-U-1729": 872.0}


def fig_compute() -> None:
    comp = load_json(DATA / "compute_ledgers.json")["studies"]
    st = load_json(DATA / "x6s1_status.json")
    fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw={"width_ratios": [1.3, 1]})
    ax = axs[0]
    shown = {store: label for label, store, _ in LEDGERS}  # descriptive labels by store
    rows = [(shown.get(c["store"], c["label"]), c["cumulative_cpu_s"] / 3600) for c in comp]
    rows.append(("Pilot: 17 trainings\n(wall-clock h, not CPU)",
                 sum(PILOT_WALL_S.values()) / 3600))
    rows.sort(key=lambda r: r[1])
    for i, (lab, h) in enumerate(rows):
        hatch = "///" if lab.startswith("Pilot") else None
        ax.barh(i, h, 0.62, color=S1 if not hatch else "white", edgecolor=S1, hatch=hatch,
                linewidth=0.8)
        ax.text(h + 0.06, i, f"{h:.2f}" if h >= 0.01 else f"{h:.3f}", va="center", fontsize=6.3)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=6.5)
    ax.set_xlabel("CPU-hours (ledger cumulative, measured + tail allowance)")
    ax.set_title("(a) local compute per study", loc="left")
    ax.grid(axis="y", visible=False)
    ax = axs[1]
    labs, vals, cols = [], [], []
    names = {"E0__run": "E0", "E0b__run": "E0b", "E1__run": "E1", "E2__run": "E2"}
    seen = {}
    for e in st["ledger"]:
        n = names.get(e["label"], e["label"])
        seen[n] = seen.get(n, 0) + 1
        labs.append(f"{n} a{seen[n]}")
        if e.get("measured_cpu_s") is None:
            vals.append(0)
            cols.append("open")
        else:
            vals.append(e["measured_cpu_s"] / 3600)
            cols.append("pass" if e.get("exit_code") == 0 else "fail")
    for i, (v, c) in enumerate(zip(vals, cols)):
        if c == "open":
            ax.barh(i, 0.05, 0.6, color="white", edgecolor=INK, linewidth=0.8)
            ax.text(0.1, i, "running at snapshot", va="center", fontsize=6.3, color=INK2)
        else:
            ax.barh(i, v, 0.6, color=GOOD if c == "pass" else CRIT, edgecolor="white")
            txt = f"{v * 3600:.0f} s" if v < 0.1 else f"{v:.2f} h"
            ax.text(v + 0.03, i, txt + ("" if c == "pass" else "  (stopped: INVALID)"),
                    va="center", fontsize=6.3, color=INK if c == "pass" else CRIT)
    ax.set_yticks(range(len(labs)))
    ax.set_yticklabels(labs)
    ax.invert_yaxis()
    ax.set_xlabel("measured CPU-hours per metered job")
    ax.set_title(f"(b) Crossing order (trained): {st['cumulative_cpu_s'] / 3600:.2f} CPU-h", loc="left")
    ax.legend(handles=[Patch(color=GOOD, label="exit 0"), Patch(color=CRIT, label="stopped (INVALID)")],
              frameon=False, loc="lower right", fontsize=6.5)
    ax.grid(axis="y", visible=False)
    save(fig, "fig11_compute")


# =========================================================================================
# Figure 12: X6S1 design (X6S1-FROZEN-v1 §4.1, §4.4, §8)
# =========================================================================================
def fig_x6s1_design() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.set_xlim(0, 14.4)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    arms = ["NA (non-abelian S$_3$)", "AB (abelian: a on both seams)", "ZC (abelian: 3-cycles)"]
    wave = {("NA", 1): "C1", ("NA", 2): "C1", ("ZC", 1): "C1"}
    x0, y0, cw, ch = 3.1, 1.2, 0.95, 0.85
    for s in range(4):
        ax.text(x0 + s * cw + cw / 2, y0 + 3 * ch + 0.15, f"seed {s + 1}", ha="center",
                fontsize=7, color=INK2)
        ax.add_patch(Rectangle((x0 + s * cw + 0.05, y0 - 0.85), cw - 0.1, 0.6, facecolor="#f3f2ef",
                               edgecolor=MUTED, lw=0.6))
        ax.text(x0 + s * cw + cw / 2, y0 - 0.55, f"init({s + 1})", ha="center", va="center",
                fontsize=6.5)
    for a, name in enumerate(arms):
        code = name.split()[0]
        yy = y0 + (2 - a) * ch
        ax.text(x0 - 0.1, yy + ch / 2, name, ha="right", va="center", fontsize=7)
        for s in range(4):
            w = wave.get((code, s + 1), "C2")
            col = S1 if w == "C1" else S3
            ax.add_patch(Rectangle((x0 + s * cw + 0.05, yy + 0.05), cw - 0.1, ch - 0.1,
                                   facecolor=col, edgecolor="white", alpha=0.9))
            ax.text(x0 + s * cw + cw / 2, yy + ch / 2, f"{code}-s{s + 1}\n{w}", ha="center",
                    va="center", fontsize=6.5, color="white")
    ax.text(x0 + 2 * cw, y0 - 1.1, "same initial state and batch-index sequence per seed, in every arm",
            ha="center", fontsize=6.3, color=INK2)
    # right: execution flow
    steps = [("E0 (local)", "pools, registry, oracle and\nscoring checks, bundles"),
             ("C0 (Colab)", "smoke: 200 updates, resume"),
             ("E0b (local)", "SMOKE-INGEST"),
             ("C1 (Colab)", "NA-s1, NA-s2, ZC-s1; 30k upd."),
             ("E1 (local)", "INGEST-C1, LEARN gate, LC-1"),
             ("C2 (Colab)", "9 models, after LEARN GO"),
             ("E2 (local)", "INGEST-C2, LC-2"),
             ("E3 (local)", "float64 evaluation, decision,\nunsealing")]
    bx, by = 8.5, 6.15
    for i, (h, t) in enumerate(steps):
        yy = by - i * 0.74
        cloud = "Colab" in h
        ax.add_patch(FancyBboxPatch((bx, yy - 0.3), 1.6, 0.56, boxstyle="round,pad=0.02",
                                    facecolor=S2 if cloud else "#f3f2ef",
                                    edgecolor=S2 if cloud else MUTED, lw=0.8))
        ax.text(bx + 0.8, yy - 0.02, h, ha="center", va="center", fontsize=6.6,
                color="white" if cloud else INK)
        ax.text(bx + 1.75, yy - 0.02, t, ha="left", va="center", fontsize=6.2, color=INK2)
        if i < len(steps) - 1:
            ax.annotate("", xy=(bx + 0.8, yy - 0.44), xytext=(bx + 0.8, yy - 0.3),
                        arrowprops=dict(arrowstyle="->", color=INK2, lw=0.8))
    ax.legend(handles=[Patch(color=S1, label="wave C1 (pilot; NA-s1/s2 gate)"),
                       Patch(color=S3, label="wave C2 (released after LEARN = GO)"),
                       Patch(color=S2, label="owner-run cloud training (GPU)")],
              loc="upper left", bbox_to_anchor=(0.0, 1.0), frameon=False, fontsize=6.5)
    save(fig, "fig12_x6s1_design")


# =========================================================================================
# Figure 13: X6S1 gate pipeline with statuses (snapshot of GATES.jsonl: gate/status/utc only)
# =========================================================================================
PIPE = [  # (stage, [gates]) in protocol §8 order
    ("E0", ["AUTH-ADMIT", "S0", "PF", "G0-ORC", "SCORE", "G0-POS", "REG", "G0-FEAS",
            "HEADROOM-D", "CLOUD-PREP", "AUTH-VERIFY"]),
    ("E0b", ["S0", "SMOKE-INGEST"]),
    ("E1", ["S0", "INGEST-C1", "LEARN", "LC-1"]),
    ("E2", ["S0", "INGEST-C2", "LC-2"]),
    ("E3", ["E3.0 BIND", "E3.1 DET", "E3.A EVAL", "E3.2 LEARN-TEST", "E3.3 READOUT",
            "E3.4 PLACEBO", "E3.5 XCHECK", "E3.6 STATS", "E3.7 PREC", "E3.8 CONFIRM",
            "E3.9 RULES"]),
]
STATUS_COL = {"PASS": GOOD, "INVALID": CRIT, "FAIL": CRIT, "NOT_RUN": "#ffffff",
              "PENDING": "#ffffff"}


def _stage_status(st):
    """Assign each GATES.jsonl record (gate, status, utc only) to a stage in time order.
    AUTH-ADMIT opens E0; after E0's CLOUD-PREP, every S0 opens the next local stage of the
    protocol sequence (E0b ran twice: jobs 0090 and 0092; E3 ran as jobs 0095, 0097, 0098 and 0099). Returns {stage: {gate: [statuses]}}."""
    out = {"E0": {}, "E0b": {}, "E1": {}, "E2": {}, "E3": {}}
    after_e0 = iter(["E0b", "E0b", "E1", "E2", "E3"])
    stage = None
    for r in st["gates"]:
        if r["gate"] == "AUTH-ADMIT":
            stage = "E0"
        elif r["gate"] == "S0" and not (stage == "E0" and "CLOUD-PREP" not in out["E0"]):
            stage = next(after_e0, "E3")  # E3a, E3w and E3z jobs each start with S0
        out[stage].setdefault(r["gate"], []).append(r["status"])
    return out


def fig_x6s1_pipeline() -> None:
    st = load_json(DATA / "x6s1_status.json")
    per = _stage_status(st)
    sup = st.get("superseded_gates", {}).get("0087-a1", [])
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.axis("off")
    ax.set_xlim(0, 12.1)
    ax.set_ylim(-0.6, len(PIPE) + 0.9)
    bw, bh, gap = 0.98, 0.52, 0.06
    for row, (stage, gates) in enumerate(PIPE):
        y = len(PIPE) - row
        ax.text(0.0, y, stage, ha="left", va="center", fontsize=8.5, fontweight="bold")
        for j, g in enumerate(gates):
            x = 0.55 + j * (bw + gap)
            hist = per.get(stage, {}).get(g, [])
            status = hist[-1] if hist else "PENDING"
            if stage == "E2" and g == "LC-2" and not hist:
                status = "PENDING"
            col = STATUS_COL.get(status, "#ffffff")
            sealed = stage == "E3" or g in ("LEARN", "LC-1", "LC-2", "HEADROOM-D")
            ax.add_patch(FancyBboxPatch((x, y - bh / 2), bw, bh, boxstyle="round,pad=0.01",
                                        facecolor=col, edgecolor=INK2 if col == "#ffffff" else col,
                                        lw=0.8, ls="--" if status == "PENDING" else "-"))
            label = g.replace(" ", "\n", 1) if " " in g else (
                g.replace("-", "-\n", 1) if len(g) > 7 and "-" in g else g)
            txtcol = "white" if col not in ("#ffffff",) else INK
            ax.text(x + bw / 2, y + 0.02, label, ha="center", va="center", fontsize=5.4,
                    color=txtcol)
            if len(hist) > 1:
                ax.text(x + bw / 2, y - bh / 2 - 0.05, "→".join(h[:3] for h in hist),
                        ha="center", va="top", fontsize=4.8, color=INK2)
            if sealed:
                ax.text(x + bw - 0.04, y + bh / 2 - 0.04, "S", ha="right", va="top", fontsize=4.6,
                        color=txtcol, fontweight="bold")
    # E0 attempt 1 (superseded/0087-a1)
    if sup:
        y = len(PIPE) + 0.65
        txt = "E0 attempt 1 (superseded/0087-a1): " + ", ".join(
            f"{r['gate']} {r['status']}" for r in sup[:3]) + f", {len(sup) - 3} later gates NOT_RUN"
        ax.text(0.0, y, txt, fontsize=6.2, color=INK2, va="center")
    ax.legend(handles=[Patch(facecolor=GOOD, label="PASS"),
                       Patch(facecolor=CRIT, label="INVALID (first attempt; corrected)"),
                       Patch(facecolor="white", edgecolor=INK2, ls="--", label="not yet run"),
                       Line2D([], [], ls="", marker="$S$", color=INK, label="value sealed until the decision stage")],
              loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=4, frameon=False, fontsize=6.5)
    ax.text(12.05, -0.45, f"snapshot {st['generated_utc']}", ha="right", fontsize=5.5, color=MUTED)
    save(fig, "fig13_x6s1_pipeline")



def fig_x6s1_results() -> None:
    p = DATA / "x6s1_result.json"
    if not p.is_file():
        return
    r = load_json(p)
    col = {"NA": S1, "AB": S2, "ZC": S3, "in": MUTED}
    fig, ax = plt.subplots(2, 2, figsize=(9.2, 6.4))
    # (a) natural beta_ord per predictor
    b = r["natural"]["beta_ord"]
    names = [n for n in b if not n.startswith("init")] + [n for n in b if n.startswith("init")]
    a = ax[0, 0]
    a.bar(range(len(names)), [b[n] for n in names], color=[col[n[:2]] for n in names])
    a.set_xticks(range(len(names)), names, rotation=70)
    a.axhline(0, color=INK2, lw=0.8)
    a.set_ylabel(r"natural $\beta_{ord}$ (oracle = 1)")
    a.set_title("(a) Order-dependent share, natural pairs (t = 32)", loc="left", fontsize=9)
    # (b) C_s per seed with 95% interval, against the registered 0.25 threshold
    a = ax[0, 1]
    cs = r["natural"]["C_s"]; seeds = sorted(cs, key=int)
    v = [cs[s]["value"] for s in seeds]
    err = [[cs[s]["value"] - cs[s]["lb"] for s in seeds], [cs[s]["ub"] - cs[s]["value"] for s in seeds]]
    a.errorbar(range(len(seeds)), v, yerr=err, fmt="o", color=S1, capsize=4)
    a.axhline(0.25, color=CRIT, ls="--", lw=1.2, label="registered C-ORD size (0.25)")
    a.axhline(r["natural"]["mean"], color=S7, lw=1.0, label=f"mean {r['natural']['mean']:.3f}")
    a.axhline(r["natural"]["lb"], color=S7, ls=":", lw=1.0, label=f"LB$_{{0.975}}$ {r['natural']['lb']:.4f}")
    a.set_xticks(range(len(seeds)), [f"seed {s}" for s in seeds]); a.set_ylim(0, 0.3)
    a.set_ylabel(r"$C_s$ (NA minus controls)"); a.legend(fontsize=7, loc="upper right")
    a.set_title("(b) C-ORD per seed: clearly > 0, far below 0.25", loc="left", fontsize=9)
    # (c) designed W2 regret against the bar
    a = ax[1, 0]
    d = r["designed"]; mods = [m for m in d if not m.startswith("init")]
    a.bar(range(len(mods)), [d[m]["R_W2"] for m in mods], color=[col[m[:2]] for m in mods])
    a.axhline(0.0458395285, color=CRIT, ls="--", lw=1.2, label=r"bar $(3/4)\Delta_{W2}^{lo}\approx0.0458$")
    a.set_xticks(range(len(mods)), mods, rotation=70); a.legend(fontsize=7)
    a.set_ylabel(r"designed W2 regret $R_{W2}$")
    a.set_title("(c) Designed W2 regret: bar not beaten", loc="left", fontsize=9)
    # (d) designed placebo beta_W2 of the controls
    a = ax[1, 1]
    ctr = [m for m in d if m[:2] in ("AB", "ZC") or m.startswith("init")]
    a.bar(range(len(ctr)), [d[m]["beta_W2"] for m in ctr], color=[col[m[:2]] for m in ctr])
    a.set_xticks(range(len(ctr)), ctr, rotation=70); a.axhline(0, color=INK2, lw=0.8)
    a.set_ylabel(r"designed placebo $\beta_{W2}$")
    a.set_title("(d) Designed placebo: ZC-s1 responds (control-limited)", loc="left", fontsize=9)
    fig.legend(handles=[Patch(color=col[k], label=l) for k, l in
                        (("NA", "NA (non-abelian)"), ("AB", "AB control"), ("ZC", "ZC control"),
                         ("in", "init"))], loc="lower center", ncol=4, fontsize=7.5,
               frameon=False, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(f"Crossing order in trained models: {r['outcome']}", fontsize=10)
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
    save(fig, "fig14_x6s1_results")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--refresh", action="store_true",
                    help="re-read the X6S1 store and CPU ledgers into data/ snapshots first")
    a = ap.parse_args(argv)
    if a.refresh:
        refresh()
    for f in (fig_timeline, fig_outcomes, fig_e1, fig_f1, fig_dynamics, fig_layers,
              fig_probes_circular, fig_origin, fig_d2a, fig_x6_ladder, fig_compute,
              fig_x6s1_design, fig_x6s1_pipeline, fig_x6s1_results):
        f()
    return 0


if __name__ == "__main__":
    sys.exit(main())
