"""Author B, K4b TEST_PLAN B13 and B18: the §11.8 rerun and lineage rule. Superseded moves with
a SHA256SUMS manifest, byte restore of the record files, refusal of unrecorded prior files,
an interrupted stage without a terminal gate record, bit-identical regeneration and the
owner-escalation rule (an unchanged quantity computed before the failure point alone does not
escalate).

Synthetic stores under tmp_path only."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tools/k4b", "tools/c1prime", "tools/c1prime_registry", "tools/x4_circle_history",
             "tools/x4_oracle_profile"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import pytest  # noqa: E402

import k4b_driver  # noqa: E402
import k4b_release  # noqa: E402
import op_guard  # noqa: E402
from c1_records import C1GateFailure  # noqa: E402

LINEAGE = "FAIL_TECHNICAL/LINEAGE"
TRAINED = "CHART_CONSTRUCTIONS_trained.json"


def sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def outcome(fn, *args, **kwargs):
    try:
        result = fn(*args, **kwargs)
    except C1GateFailure as exc:
        return exc.status, None
    return result["status"], result


def jl(*entries) -> bytes:
    return "".join(json.dumps(e, sort_keys=True) + "\n" for e in entries).encode("utf-8")


def attempt_store(tmp_path):
    """A store whose S4a attempt failed technically after earlier PASS gates."""
    out = tmp_path / "k4b-store"
    (out / "stages" / "S3").mkdir(parents=True)
    (out / "stages" / "S4a").mkdir(parents=True)
    gates_ok = jl({"gate": "G0", "status": "PASS"}, {"gate": "H1", "status": "PASS"})
    gates_suffix = jl({"gate": "C0-CAL", "status": "FAIL_TECHNICAL", "reason": "defect"})
    stages_ok = jl({"stage": "S3", "event": "STAGE_COMPLETE"})
    stages_suffix = jl({"stage": "S4a", "event": "BEGIN"})
    ledger_ok = json.dumps({"claims": []}, indent=1).encode("utf-8")
    ledger_after = json.dumps({"claims": [[1729, "production"]]}, indent=1).encode("utf-8")
    (out / "GATES.jsonl").write_bytes(gates_ok + gates_suffix)
    (out / "STAGES.jsonl").write_bytes(stages_ok + stages_suffix)
    (out / TRAINED).write_bytes(ledger_after)
    failed = out / "stages" / "S4a" / "CHART_1729.npz"
    failed.write_bytes(b"attempt payload 1729")
    verified = {"GATES.jsonl": gates_ok, "STAGES.jsonl": stages_ok, TRAINED: ledger_ok}
    suffixes = {"GATES.jsonl": gates_suffix.decode("utf-8"),
                "STAGES.jsonl": stages_suffix.decode("utf-8")}
    return out, failed, verified, suffixes


# --------------------------------------------------------------- superseded moves (B13)

def test_archive_attempt_moves_files_with_sha256sums(tmp_path):
    out, failed, _, suffixes = attempt_store(tmp_path)
    digest = sha(failed)
    dest = Path(k4b_release.archive_attempt(out, "0047", [failed], suffixes))
    root = (out / "superseded" / "0047").resolve()
    assert dest.resolve() == root or root in dest.resolve().parents
    assert not failed.exists()
    moved = [p for p in root.rglob("*") if p.is_file() and p.name != "SHA256SUMS"
             and sha(p) == digest]
    assert moved, "the failed attempt's payload is kept under superseded/<job>/"
    sums = [p for p in root.rglob("SHA256SUMS")]
    assert len(sums) == 1
    assert digest in sums[0].read_text(encoding="utf-8")


def test_restore_records_is_byte_exact(tmp_path):
    out, failed, verified, suffixes = attempt_store(tmp_path)
    k4b_release.archive_attempt(out, "0047", [failed], suffixes)
    k4b_release.restore_records(out, verified)
    for name, data in verified.items():
        assert (out / name).read_bytes() == data, name


def test_archived_suffixes_are_kept(tmp_path):
    out, failed, _, suffixes = attempt_store(tmp_path)
    k4b_release.archive_attempt(out, "0047", [failed], suffixes)
    root = out / "superseded" / "0047"
    text = "".join(p.read_text(encoding="utf-8", errors="replace")
                   for p in root.rglob("*") if p.is_file())
    assert "C0-CAL" in text and "FAIL_TECHNICAL" in text


# ------------------------------------------------------------------ lineage_ok (B13)

def test_lineage_ok_absent_store_passes(tmp_path):
    status, _ = outcome(k4b_release.lineage_ok, tmp_path / "k4b-store")
    assert status == "PASS"


def test_lineage_ok_empty_store_passes(tmp_path):
    out = tmp_path / "k4b-store"
    out.mkdir()
    status, _ = outcome(k4b_release.lineage_ok, out)
    assert status == "PASS"


def test_lineage_ok_refuses_unrecorded_prior_file(tmp_path):
    out = tmp_path / "k4b-store"
    (out / "stages" / "S3").mkdir(parents=True)
    (out / "stages" / "S3" / "HIST_cal_b0.npz").write_bytes(b"prior unrecorded histories")
    status, _ = outcome(k4b_release.lineage_ok, out)
    assert status == LINEAGE


def test_lineage_ok_accepts_exactly_the_superseded_manifest(tmp_path):
    out = tmp_path / "k4b-store"
    (out / "stages" / "S3").mkdir(parents=True)
    f = out / "stages" / "S3" / "HIST_cal_b0.npz"
    f.write_bytes(b"attempt histories")
    k4b_release.archive_attempt(out, "0047", [f], {})
    status, _ = outcome(k4b_release.lineage_ok, out)
    assert status == "PASS"
    (out / "superseded" / "0047" / "ROGUE.bin").write_bytes(b"not in the manifest")
    status, _ = outcome(k4b_release.lineage_ok, out)
    assert status == LINEAGE


# --------------------------------------------------- interrupted-stage replay (B18)

def test_begin_and_complete_stage_records(tmp_path):
    out = tmp_path / "k4b-store"
    out.mkdir()
    k4b_driver.begin_stage(out, "S3")
    assert (out / op_guard.MARKER).exists()
    (out / "stages" / "S3").mkdir(parents=True, exist_ok=True)
    f = out / "stages" / "S3" / "HIST_cal_b0.npz"
    f.write_bytes(b"histories")
    k4b_driver.complete_stage(out, "S3", [f])
    lines = (out / "STAGES.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) >= 2
    assert "S3" in lines[0]
    assert "STAGE_COMPLETE" in lines[-1] and sha(f) in lines[-1]


def test_interrupted_stage_without_gate_record_is_replayed_under_rule(tmp_path):
    out = tmp_path / "k4b-store"
    out.mkdir()
    k4b_driver.begin_stage(out, "S3")
    (out / "stages" / "S3").mkdir(parents=True, exist_ok=True)
    partial = out / "stages" / "S3" / "HIST_cal_b0.npz"
    partial.write_bytes(b"partial histories, interrupted")
    assert not (out / "GATES.jsonl").exists()  # no terminal gate record
    status, _ = outcome(k4b_release.lineage_ok, out)
    assert status == LINEAGE  # the partial payload is not a recorded file
    stages_before = b""
    suffix = (out / "STAGES.jsonl").read_text(encoding="utf-8")
    digest = sha(partial)
    k4b_release.archive_attempt(out, "0047", [partial], {"STAGES.jsonl": suffix})
    k4b_release.restore_records(out, {"STAGES.jsonl": stages_before})
    assert not partial.exists()
    assert (out / "STAGES.jsonl").read_bytes() == stages_before
    sums = list((out / "superseded" / "0047").rglob("SHA256SUMS"))
    assert sums and digest in sums[0].read_text(encoding="utf-8")


def test_regenerated_identical(tmp_path):
    old = tmp_path / "old.npz"
    old.write_bytes(b"unaffected artefact")
    new = tmp_path / "new.npz"
    new.write_bytes(b"unaffected artefact")
    assert k4b_release.regenerated_identical(sha(old), new) is True
    new2 = tmp_path / "new2.npz"
    new2.write_bytes(b"unaffected artefact!")
    try:
        same = k4b_release.regenerated_identical(sha(old), new2)
    except C1GateFailure as exc:
        assert exc.status == LINEAGE
    else:
        assert same is False


# ------------------------------------------------------------- owner escalation (B18)

def q(name, outcome_bearing=True, changed=False, at_or_after_failure=False):
    return {"name": name, "outcome_bearing": outcome_bearing, "changed": changed,
            "at_or_after_failure": at_or_after_failure}


@pytest.mark.parametrize("quantities,expected", [
    ([q("B4 bounds")], False),
    ([q("SD bounds"), q("N")], False),
    ([q("B4 bounds", changed=True)], True),
    ([q("chart-validation criteria", at_or_after_failure=True)], True),
    ([q("SD bounds"), q("endpoint means", at_or_after_failure=True)], True),
    ([q("OPERATIONS.jsonl", outcome_bearing=False, changed=True)], False),
    ([], False),
])
def test_needs_owner(quantities, expected):
    assert k4b_release.needs_owner({"defect": "synthetic", "quantities": quantities}) is expected
