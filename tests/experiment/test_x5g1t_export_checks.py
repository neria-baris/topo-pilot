"""Independent critical-safety tests (writer E, job 0010) for the x5g1-train-v4 API contract
(docs/proposals/X5_G1_TRAINING_API_V4.md): §3 config validation (production and synthetic-fixture
modes, read-only, before any sampler or model), §4 complete exports and §5 checkpoint identity and
full-hash integrity. Written from the contract only; every artifact lives under ``tmp_path``.
Split mechanically from test_x5g1t_config_checks.py (job 0011); tests unchanged.
"""

from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.experiment.x5g1_controls import BudgetExceeded, StopRequested
from topo_pilot.experiment.x5g1t_runtime import ResourceExceeded


# ---- lazy module access (x5g1t_config may land after these tests) ------------------------------
def _cm():
    return importlib.import_module("topo_pilot.experiment.x5g1t_config")


def _ex():
    return importlib.import_module("topo_pilot.experiment.x5g1t_exports")


def _ck():
    return importlib.import_module("topo_pilot.experiment.x5g1t_checks")


def _sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# =============================== §4 exports ======================================================
class FakeSC:
    """StudyControls stand-in: records each boundary and raises ``exc`` where ``stop_at``."""

    def __init__(self, stop_at=None, exc=StopRequested):
        self.calls: list[str] = []
        self.stop_at, self.exc = stop_at, exc

    def boundary(self, what, next_estimate=0.0, reserve=0.0, audit=dict):
        self.calls.append(what)
        if self.stop_at is not None and self.stop_at(what):
            raise self.exc(f"injected at {what}")


FILES = {"alpha.json": {"a": 1}, "beta.json": {"b": [1, 2]}, "gamma.json": {"g": "x"}}
STATUS = {StopRequested: "STOPPED_DURING_EXPORT", BudgetExceeded: "BUDGET_DURING_EXPORT",
          ResourceExceeded: "RESOURCE_DURING_EXPORT"}


def _out(tmp_path: Path) -> Path:
    out = tmp_path / "export"
    out.mkdir()
    return out


def _data_files(out: Path) -> list[str]:
    return sorted(p.name for p in out.iterdir()
                  if p.name not in ("MANIFEST.json", "EXPORT_STATUS.json"))


def _status(out: Path) -> dict:
    return json.loads((out / "EXPORT_STATUS.json").read_text(encoding="utf-8"))


def _complete(tmp_path: Path, arrays=None) -> Path:
    out = _out(tmp_path)
    _ex().study_export(FakeSC(), out, dict(FILES), arrays=arrays)
    return out


def test_export_roundtrip_complete_and_guarded(tmp_path):
    ex = _ex()
    out = _out(tmp_path)
    sc = FakeSC()
    ex.study_export(sc, out, dict(FILES))
    assert _status(out)["status"] == "COMPLETE"
    man = ex.verify_export_complete(out)
    assert isinstance(man, dict)
    names = {p.name for p in out.iterdir()}
    assert {"MANIFEST.json", "EXPORT_STATUS.json"} <= names
    assert len(_data_files(out)) == 3
    for n in _data_files(out):
        assert _sha_file(out / n) in json.dumps(man)
    done = _status(out)["completed_steps"]
    for stem in ("alpha", "beta", "gamma", "MANIFEST"):
        if stem != "MANIFEST":  # whether the manifest step is listed is not specified
            assert any(stem in str(s) for s in done)
        i = next(k for k, w in enumerate(sc.calls) if stem in w and not w.endswith("done"))
        assert sc.calls[i].startswith("export ")
        assert stem in sc.calls[i + 1] and sc.calls[i + 1].endswith(" done")
    order = [next(k for k, w in enumerate(sc.calls) if s in w)
             for s in ("alpha", "beta", "gamma", "MANIFEST")]
    assert order == sorted(order)


def test_export_roundtrip_with_arrays(tmp_path):
    out = _complete(tmp_path, arrays={"delta.npz": {"x": np.arange(3)}})
    man = _ex().verify_export_complete(out)
    assert len(_data_files(out)) == 4
    for n in _data_files(out):
        assert _sha_file(out / n) in json.dumps(man)


@pytest.mark.parametrize("exc", [StopRequested, BudgetExceeded, ResourceExceeded])
def test_export_interrupted_before_second_file(tmp_path, exc):
    ex = _ex()
    out = _out(tmp_path)
    sc = FakeSC(stop_at=lambda w: "beta" in w and not w.endswith("done"), exc=exc)
    with pytest.raises(exc):
        ex.study_export(sc, out, dict(FILES))
    assert len(_data_files(out)) == 1 and _data_files(out)[0].startswith("alpha")
    assert not (out / "MANIFEST.json").exists()
    st = _status(out)
    assert st["status"] == STATUS[exc]
    assert any("alpha" in str(s) for s in st["completed_steps"])
    assert not any(("beta" in str(s)) or ("gamma" in str(s)) for s in st["completed_steps"])
    assert "cause" in st
    assert "beta" in sc.calls[-1], "no boundary (hence no further step) after the stop"
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)


def test_export_stop_after_file_done_writes_nothing_further(tmp_path):
    ex = _ex()
    out = _out(tmp_path)
    sc = FakeSC(stop_at=lambda w: "beta" in w and w.endswith("done"))
    with pytest.raises(StopRequested):
        ex.study_export(sc, out, dict(FILES))
    assert not any(n.startswith("gamma") for n in _data_files(out))
    assert not (out / "MANIFEST.json").exists()
    assert _status(out)["status"] == "STOPPED_DURING_EXPORT"
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)


def test_export_stop_before_manifest(tmp_path):
    ex = _ex()
    out = _out(tmp_path)
    sc = FakeSC(stop_at=lambda w: "MANIFEST" in w and not w.endswith("done"))
    with pytest.raises(StopRequested):
        ex.study_export(sc, out, dict(FILES))
    assert not (out / "MANIFEST.json").exists()
    st = _status(out)
    assert st["status"] == "STOPPED_DURING_EXPORT"
    assert sum(any(s in str(x) for x in st["completed_steps"])
               for s in ("alpha", "beta", "gamma")) == 3
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)


def test_export_tampered_file_bytes_incomplete(tmp_path):
    out = _complete(tmp_path)
    p = out / _data_files(out)[0]
    p.write_bytes(p.read_bytes() + b" ")
    with pytest.raises(_ex().ExportIncomplete):
        _ex().verify_export_complete(out)


def test_export_extra_file_incomplete(tmp_path):
    out = _complete(tmp_path)
    (out / "zeta.json").write_text("{}", encoding="utf-8")
    with pytest.raises(_ex().ExportIncomplete):
        _ex().verify_export_complete(out)


def test_export_missing_manifest_incomplete(tmp_path):
    out = _complete(tmp_path)
    (out / "MANIFEST.json").unlink()
    with pytest.raises(_ex().ExportIncomplete):
        _ex().verify_export_complete(out)


def test_export_missing_data_file_incomplete(tmp_path):
    out = _complete(tmp_path)
    (out / _data_files(out)[1]).unlink()
    with pytest.raises(_ex().ExportIncomplete):
        _ex().verify_export_complete(out)


def test_export_missing_or_non_complete_status_incomplete(tmp_path):
    ex = _ex()
    out = _complete(tmp_path)
    st = _status(out)
    (out / "EXPORT_STATUS.json").write_text(
        json.dumps({**st, "status": "STOPPED_DURING_EXPORT"}), encoding="utf-8")
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)
    (out / "EXPORT_STATUS.json").unlink()
    with pytest.raises(ex.ExportIncomplete):
        ex.verify_export_complete(out)


def test_export_error_classes_are_runtime_errors():
    assert issubclass(_ex().ExportIncomplete, RuntimeError)
    assert issubclass(_ck().IntegrityFailed, RuntimeError)
    assert issubclass(_cm().ConfigInvalid, RuntimeError)
