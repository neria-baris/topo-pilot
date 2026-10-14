"""Two-panel B_K / V_K figure from the exported PROFILE_TABLE.json (venv interpreter, Agg).

Pointwise central 95 % bootstrap intervals; K on a log2 axis; K = 32 drawn hollow as the
definitional zero endpoint (no evidence). The dashed 0.01 line on the B panel is ONLY the
historical practical-margin reference of the failed K = 8 gate, not a new gate.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(r"X:\Downloads\projects\topo-pilot\x4-oracle-profile-store-0014") / "profile"
STYLE = {"calibration": ("#1f5aa6", "o", -0.04), "validation": ("#c2571a", "s", 0.04)}


def main() -> int:
    table = json.loads((OUT / "PROFILE_TABLE.json").read_text(encoding="utf-8"))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), constrained_layout=True)
    for ax, stat, label in (
        (axes[0], "B", r"$B_K=\mathrm{E}\,\|m_{32}-m_K\|$"),
        (axes[1], "V", r"$V_K=\mathrm{E}\,\|m_{32}-m_K\|^2$"),
    ):
        for split, (color, marker, shift) in STYLE.items():
            rows = sorted(
                (r for r in table if r["split"] == split and r["stat"] == stat),
                key=lambda r: r["K"],
            )
            live = [r for r in rows if r["K"] != 32]
            ks = [r["K"] * 2**shift for r in live]
            est = [r["estimate"] for r in live]
            err = [
                [r["estimate"] - r["q025"] for r in live],
                [r["q975"] - r["estimate"] for r in live],
            ]
            ax.errorbar(
                ks,
                est,
                yerr=err,
                color=color,
                marker=marker,
                ms=5,
                lw=1.2,
                capsize=3,
                label=f"{split} (n={rows[0]['n']})",
            )
            end = next(r for r in rows if r["K"] == 32)
            ax.plot(
                [32 * 2**shift], [end["estimate"]], marker=marker, mfc="none", color=color, ms=6
            )
        if stat == "B":
            ax.axhline(0.01, color="0.35", ls="--", lw=1)
            ax.text(
                1.05,
                0.0106,
                "0.01: historical practical-margin reference (not a gate)",
                fontsize=7.5,
                color="0.3",
            )
        ax.set_xscale("log", base=2)
        ax.set_xticks([1, 2, 4, 8, 16, 32], ["1", "2", "4", "8", "16", "32"])
        ax.set_xlabel("suffix length K (observations)")
        ax.set_ylabel(label)
        ax.grid(alpha=0.25)
        ax.annotate(
            "K=32: zero by definition",
            xy=(32, 0),
            xytext=(9, 0.0),
            fontsize=7.5,
            color="0.3",
            textcoords="data",
            va="bottom",
        )
    axes[0].legend(fontsize=8, frameon=False)
    fig.suptitle(
        "Cylinder-O oracle first-harmonic suffix profile (exploratory; pointwise central "
        "95% whole-trajectory bootstrap)",
        fontsize=9.5,
    )
    for ext in ("png", "pdf", "svg"):
        target = OUT / f"oracle_profile_BV.{ext}"
        if target.exists():
            raise SystemExit(f"immutable figure exists: {target.name}")
        fig.savefig(target, dpi=160 if ext == "png" else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
