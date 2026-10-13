"""circ-audit-v1: frozen per-panel comparison (C1, C2) and the three-run reading."""
import pytest

from topo_pilot.experiment.circ_audit import BASELINES, compare_panel, summarize

pytestmark = pytest.mark.experiment


def _reps(model, r1="no_h1_class", r2=0.5, r3=0.4):
    out = {"model": {"status": "ok" if model is not None else "no_h1_class",
                     "agreement": model, "null_q95": 0.1},
           "R0": {"status": "ok", "agreement": 0.3, "null_q95": 0.1}}
    for k, v in zip(BASELINES, (r1, r2, r3)):
        out[k] = ({"status": v} if isinstance(v, str) else
                  {"status": "ok", "agreement": v, "null_q95": 0.1})
    return out


def _panel(bound=0.8, b1=0.7):
    return {"A_symbol_bound": bound, "A_b1_angle": b1, "A_b32_angle": 0.9}


def test_compare_panel_excludes_failed_baselines_and_counts_them():
    c = compare_panel(_panel(), _reps(0.85))
    assert c["C1"] and c["C2"] and c["best_baseline"] == "b1_angle"
    assert c["baselines_not_ok"] == ["R1"]
    assert c["margin_vs_symbol_bound"] == pytest.approx(0.05)


def test_compare_panel_fails_below_bound_or_baseline():
    assert not compare_panel(_panel(bound=0.9), _reps(0.85))["C1"]
    c = compare_panel(_panel(), _reps(0.85, r2=0.86))
    assert c["C1"] and not c["C2"] and c["best_baseline"] == "R2"
    c = compare_panel(_panel(), _reps(None))
    assert not c["C1"] and not c["C2"] and c["margin_vs_symbol_bound"] is None


def _rows(seed, n_pass):
    rows = []
    for p in range(1, 9):
        model = 0.85 if p <= n_pass else 0.75
        panel = {"seed": seed, "panel": p, **_panel()}
        reps = _reps(model)
        rows.append({**panel, "reps": reps, **compare_panel(panel, reps)})
    return rows


@pytest.mark.parametrize("passes,reading", [
    ((8, 7, 8), "BEYOND_SYMBOL_AND_MIXING"),
    ((6, 0, 2), "SYMBOL_MIXING_SUFFICES_FOR_NOW"),
    ((8, 6, 8), "NOT_ESTABLISHED_MIXED"),
])
def test_summarize_three_run_reading(passes, reading):
    rows = sum((_rows(s, n) for s, n in zip((1729, 2718, 3141), passes)), [])
    out = summarize(rows)
    assert out["reading"] == reading
    assert out["runs"][1729]["n_both"] == passes[0]
    assert out["runs"][1729]["n_ok_R1"] == 0
