"""BUILDER tests (not independent) for spec v2.4 items 1, 8, 9 and 10: gate taxonomy, stage
prerequisites / no retry / evidence integrity, persisted reference reuse, saved-ID alignment,
precision-stage controls and cross-model checks. Synthetic memory store only (the
test_builder_e2e harness). See BUILDER_TESTS.md."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

pytestmark = pytest.mark.analysis
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import runner  # noqa: E402
import stage_records as sr  # noqa: E402
from errors import Invalid, JoinError, Unresolved  # noqa: E402
from test_builder_e2e import MODELS, _context, _gates  # noqa: E402


@pytest.mark.parametrize(
    "exc,status",
    [
        (Invalid("x"), "FAIL_TECHNICAL"),
        (JoinError("x"), "FAIL_TECHNICAL"),
        (Unresolved("x"), "INCONCLUSIVE"),
    ],
)
def test_run_gate_taxonomy(tmp_path, exc, status):
    def body():
        raise exc

    with pytest.raises(type(exc)):
        sr.run_gate(tmp_path, "g", body)
    assert _gates(tmp_path) == [("g", status)]


@pytest.mark.parametrize("stage", ["oracle", "charts", "precision"])
def test_out_of_order_stage_refused_without_gate(tmp_path, stage):
    ctx = _context(tmp_path, relaxed=True)
    with pytest.raises(sr.StageRefused, match="prerequisite"):
        getattr(runner, f"stage_{stage}")(ctx)
    assert _gates(tmp_path) == []
    assert sr.stages_so_far(tmp_path)[-1]["event"] == "REFUSED"


def test_second_attempt_refused_even_without_completion(tmp_path):
    ctx = _context(tmp_path, relaxed=True)
    runner.stage_identity(ctx)
    with pytest.raises(sr.StageRefused, match="already attempted"):
        runner.stage_identity(ctx)
    sr.begin(tmp_path, "oracle", MODELS)  # simulated killed attempt: STARTED, never COMPLETED
    with pytest.raises(sr.StageRefused, match="already attempted"):
        runner.stage_oracle(ctx)
    assert sr.attempts_without_completion(tmp_path) == ["oracle"]
    assert runner.stage_export(ctx)["overall"] == "INCONCLUSIVE"


def test_evidence_change_is_integrity_refusal_and_export_fails(tmp_path):
    ctx = _context(tmp_path, relaxed=True)
    runner.stage_identity(ctx)
    path = tmp_path / "IDENTITY.json"
    path.write_text(path.read_text(encoding="utf-8") + " ", encoding="utf-8")
    with pytest.raises(sr.StageRefused, match="changed"):
        runner.stage_oracle(ctx)
    refused = sr.stages_so_far(tmp_path)[-1]
    assert refused["event"] == "REFUSED" and refused["integrity"] is True
    assert runner.stage_export(ctx)["overall"] == "FAIL"


@pytest.fixture(scope="module")
def through_oracle(tmp_path_factory):
    out = tmp_path_factory.mktemp("oracle")
    ctx = _context(out, relaxed=True)
    runner.stage_identity(ctx)
    result = runner.stage_oracle(ctx)
    return out, result


def _copy_store(src: Path, dst: Path) -> None:
    for p in src.iterdir():
        (dst / p.name).write_bytes(p.read_bytes())


def test_oracle_persists_bound_reference(through_oracle):
    out, result = through_oracle
    meta = result["reference_cache"]
    obj = json.loads((out / "REFERENCE_CACHE.json").read_text(encoding="utf-8"))
    assert obj["schema"] == "x4-circle-reference-cache-v2" and obj["identity"] == meta["identity"]
    assert {(r["model"], r["split"]) for r in obj["rows"]} == {
        (m, s) for m in MODELS for s in ("calibration", "validation")
    }
    assert {e["K"] for e in obj["entries"]} == {1, 4, 32}
    assert sr.sha256(out / "REFERENCE_CACHE.json") == meta["sha256"]


def test_charts_reuse_reference_without_recomputation(through_oracle, tmp_path, monkeypatch):
    import independent_reference

    _copy_store(through_oracle[0], tmp_path)
    ctx = _context(tmp_path, relaxed=True)
    labels = []
    ctx.timed = lambda label, fn: labels.append(label) or fn()

    def forbidden(*a, **k):
        raise AssertionError("charts stage recomputed a Decimal reference")

    monkeypatch.setattr(independent_reference, "decimal_suffix_posterior", forbidden)
    charts = runner.stage_charts(ctx)
    assert "stopped_at" not in charts, charts
    assert labels[:7] == [
        "distance",
        "ph",
        "edges",
        "two_skeleton",
        "integer_lift",
        "primitive",
        "smoothing",
    ]
    assert "extension_distance" in labels


def test_charts_refuse_tampered_reference_identity(through_oracle, tmp_path):
    _copy_store(through_oracle[0], tmp_path)
    ctx = _context(tmp_path, relaxed=True)
    ctx.process["E"] = ctx.process["E"] * (1 + 1e-15)
    with pytest.raises(Invalid, match="identity"):
        runner.stage_charts(ctx)
    assert _gates(tmp_path)[-1] == ("chart_calibration", "FAIL_TECHNICAL")


def test_saved_ids_must_match_reloaded_rows(through_oracle):
    out = through_oracle[0]
    ctx = _context(out, relaxed=True)
    data = runner._panel_rows(ctx, MODELS[0])
    orc = runner._load_npz(out / f"oracle_{MODELS[0]}.npz")
    obj = json.loads((out / "REFERENCE_CACHE.json").read_text(encoding="utf-8"))
    runner._check_alignment(MODELS[0], data, orc, obj)
    swapped = dict(orc, validation_sequence_id=orc["validation_sequence_id"][::-1].copy())
    with pytest.raises(Invalid, match="sequence_id"):
        runner._check_alignment(MODELS[0], data, swapped, obj)
    obj2 = json.loads(json.dumps(obj))
    obj2["rows"][0]["history_id"] = obj2["rows"][0]["history_id"][::-1]
    with pytest.raises(Invalid, match="row table"):
        runner._check_alignment(MODELS[0], data, orc, obj2)


def _through_charts(tmp_path, through_oracle, **precision):
    _copy_store(through_oracle[0], tmp_path)
    ctx = _context(tmp_path, relaxed=True)
    ctx.contract["precision"].update(precision)
    assert "stopped_at" not in runner.stage_charts(ctx)
    return ctx


def test_precision_written_after_b4_stop_with_controls(through_oracle, tmp_path):
    ctx = _through_charts(tmp_path, through_oracle, delta=10.0)
    result = runner.stage_precision(ctx)
    assert result["stopped_at"] == "B4_lower"
    saved = json.loads((tmp_path / "PRECISION.json").read_text(encoding="utf-8"))
    assert set(saved["controls"]["summary"]) == {"m1_unit", "m4_unit", "sha256_last4"}
    per = saved["controls"]["summary"]["sha256_last4"][str(MODELS[0])]
    assert per["central95"][0] <= per["point"] <= per["central95"][1]
    assert set(saved["controls"]["angular_instability"][str(MODELS[0])]) == {"m1_unit", "m4_unit"}
    assert saved["Z_bound"]["status"] == "UNAVAILABLE"


def test_precision_cross_model_sequence_mismatch_fails_technical(through_oracle, tmp_path):
    ctx = _through_charts(tmp_path, through_oracle)
    path = tmp_path / f"oracle_{MODELS[1]}.npz"
    with np.load(path, allow_pickle=False) as z:
        arrays = {k: z[k] for k in z.files}
    arrays["validation_sequence_id"] = arrays["validation_sequence_id"] + 100000
    path.unlink()
    sr.save_npz(path, **arrays)
    with pytest.raises(Invalid, match="sequence_id"):
        runner.stage_precision(ctx)
    assert _gates(tmp_path)[-1] == ("B4_lower", "FAIL_TECHNICAL")
