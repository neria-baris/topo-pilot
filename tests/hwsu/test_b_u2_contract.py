"""Author B (job 0223, phase 2): CONTRACT.json and its loader (TEST_PLAN_U2 section 3 row
test_b_u2_contract; API_U2 section 0, U-D-2). Written from the protocol, API_U2, CONTRACT_OF.json
and CONTRACT.json only."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "hwsu"))

import hwsu_config as uc  # noqa: E402,I001
from c1_records import C1GateFailure  # noqa: E402

HWSU = REPO / "tools" / "hwsu"
OF = json.loads((HWSU / "CONTRACT_OF.json").read_text(encoding="utf-8"))
P2 = json.loads((HWSU / "CONTRACT.json").read_text(encoding="utf-8"))
GIB = 1024**3


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _new_keys_only(of, p2, path=""):
    """Every key of p2 is absent from of, or both are dicts and the rule recurses."""
    bad = []
    for k, v in p2.items():
        if k not in of:
            continue
        if isinstance(v, dict) and isinstance(of[k], dict):
            bad += _new_keys_only(of[k], v, f"{path}{k}.")
        else:
            bad.append(f"{path}{k}")
    return bad


def test_contract_of_sha256_binds_phase1_bytes():
    assert P2["contract_of_sha256"] == _sha(HWSU / "CONTRACT_OF.json")


def test_loader_succeeds_without_override():
    c = uc.load_contract()
    assert isinstance(c, dict) and "binding" in c and "resources" in c
    assert uc.CONTRACT_SHA256["phase2"] == _sha(HWSU / "CONTRACT.json")
    assert uc.CONTRACT_SHA256["of"] == _sha(HWSU / "CONTRACT_OF.json")


def test_every_phase2_key_is_new_or_a_new_key_in_a_phase1_dict():
    body = {k: v for k, v in P2.items() if k != "contract_of_sha256"}
    assert _new_keys_only(OF, body) == []


def test_no_phase1_leaf_changed_in_merged_contract():
    merged = uc.load_contract()

    def walk(a, b, path=""):
        for k, v in a.items():
            assert k in b, path + k
            if isinstance(v, dict):
                walk(v, b[k], path + k + ".")
            else:
                assert b[k] == v, path + k  # lists included: never concatenated or changed

    walk(OF, merged)


def test_wrong_contract_of_sha256_refused(tmp_path):
    bad = copy.deepcopy(P2)
    bad["contract_of_sha256"] = "0" * 64
    p = tmp_path / "CONTRACT.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(C1GateFailure) as e:
        uc.load_contract(phase2_path=p)
    assert e.value.status == "FAIL_TECHNICAL/BINDING"


def test_override_of_a_phase1_leaf_refused(tmp_path):
    bad = copy.deepcopy(P2)
    bad.setdefault("resources", {})["memory_cap_bytes"] = {"J-OF": 1}
    p = tmp_path / "CONTRACT.json"
    p.write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(C1GateFailure) as e:
        uc.load_contract(phase2_path=p)
    assert e.value.status == "FAIL_TECHNICAL/BINDING"


def test_reuse_sha256_u2_disjoint_from_phase1_table():
    u2 = P2["reuse_sha256_u2"]
    assert u2 and not (set(u2) & set(OF["reuse_sha256"]))
    assert {"tools/c2_readout/c2_model.py", "tools/hwsc/hwsc_drystore.py"} <= set(u2)
    assert all(len(v) == 64 for v in u2.values())


def test_u2_memory_caps():
    caps = P2["resources"]["u2_memory_cap_bytes"]
    for s in ("KC", "E1", "REG2", "E2"):
        assert caps[s] == 12 * GIB
    for s in ("J-U", "DRU"):
        assert caps[s] == 8 * GIB
    assert set(caps) == {"KC", "E1", "REG2", "E2", "J-U", "DRU"}
    # the phase-1 table is untouched (phase-1 tests expect E1 refused there)
    assert "E1" not in OF["resources"]["memory_cap_bytes"]


def test_name_rule_unchanged_merged_rule_refuses_acts():
    import hwsu_records as ur

    for name in ("ACTS_x.npz", "Y_x.npz", "DECODER_x.npz", "SCORES_x.npz", "CERT_x.npz"):
        assert ur.name_class(f"stages/E1/{name}") is None
    for name in ("ORACLE_E1_val.npz", "PAIR_E1_val.npz", "BOOT_E1.npz", "PREC_E1.npz"):
        assert ur.name_class(f"stages/E1/{name}") == "NON_HISTORY"
    assert ur.name_class("stages/E1/HIST_fit_s_b0.npz") == "K4b history table"
    assert P2["name_rule_u2"]["written_under_S3"] == []


def test_phase2_files_names_modules_and_documents():
    files = P2["phase2_files"]
    for m in ("hwsu_model", "hwsu_known", "hwsu_registry", "hwsu_gates", "hwsu_driver",
              "hwsu_dry2"):
        assert f"tools/hwsu/u2/{m}.py" in files, m
    for d in ("API_U2.md", "CONTRACT.json", "TEST_PLAN_U2.md"):
        assert f"tools/hwsu/{d}" in files, d
    assert "tools/hwsu/u2/hwsu_bind_u2.py" in files and "tools/hwsu/u2/__init__.py" in files
    assert all(f.startswith("tools/hwsu/") for f in files)


def test_phase2_files_not_in_phase1_files():
    assert not (set(P2["phase2_files"]) & set(OF["phase1_files"]))


def test_authority_and_dry_seeds_present():
    a = P2["authority_u2"]
    assert a["of_accept"]["outcome"] == "OF_PASS_RESPONSE_ONLY" and a["of_accept"]["N_resp"] == 4096
    assert a["of_accept"]["freeze_of_sha256"] == a["freeze_of"]["sha256"]
    assert a["run_approval"]["addendum"] == 43
    assert P2["contract_phase2"]["protocol_sha256"] == _sha(HWSU / "PROTOCOL_HWSU_v1.md")
