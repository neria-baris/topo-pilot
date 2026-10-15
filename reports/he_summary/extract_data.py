"""Read-only extraction of the two data sets the summary plots from the artifact store.

Run from the repository root with the project venv:

    .venv/Scripts/python.exe reports/he_summary/extract_data.py

Writes data/dyn.json (S6 dynamics: S and regret on panel 1 at the 12 checkpoints, primary
hook) and data/d.json (per-panel F1 contrast D under O = S4 and P = S5). Nothing is written
to the store.
"""
from __future__ import annotations

import json
from pathlib import Path

import topo_pilot.contracts as C
from topo_pilot.experiment.report_e2 import _pick, analysis_rows
from topo_pilot.experiment.report_e3 import _series, s6_rows

OUT = Path(__file__).resolve().parent / "data"
SEEDS = (1729, 2718, 3141)


def main() -> None:
    store = C.ArtifactStore(C.LocalFSBackend(Path("artifacts")))
    dyn = {}
    for cond in ("O", "P"):
        rows = s6_rows(store, "dynamics", cond)
        dyn[cond] = {name: {f"{w}-{r}": v for (w, r), v in _series(rows, space, metric).items()}
                     for name, space, metric in (("S", "dyn:S", "S_H1"),
                                                 ("regret", "dyn:regret", "regret"))}
    d = {cond: {str(s): [r.value for r in _pick(analysis_rows(store, stage), "F1", "D", replicate=s)
                         if r.value is not None] for s in SEEDS}
         for cond, stage in (("O", "S4"), ("P", "S5"))}
    OUT.mkdir(exist_ok=True)
    (OUT / "dyn.json").write_text(json.dumps(dyn, indent=1), encoding="utf-8")
    (OUT / "d.json").write_text(json.dumps(d), encoding="utf-8")
    print("wrote", OUT / "dyn.json", OUT / "d.json")


if __name__ == "__main__":
    main()
