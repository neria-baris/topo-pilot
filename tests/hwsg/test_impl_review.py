"""Implementer regression tests for R-0224-3 items 1-6 (one per item)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / "tools" / "hwsg"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import hwsg_bind as gb  # noqa: E402
import hwsg_config as gc  # noqa: E402
import hwsg_handoff as gh  # noqa: E402
import hwsg_known as gk  # noqa: E402
import hwsg_oracle as go  # noqa: E402
import hwsg_records as grec  # noqa: E402
import hwsg_registry as gr  # noqa: E402
import hwsg_train as gt  # noqa: E402
import hwsc_registry  # noqa: E402
import k4b_release  # noqa: E402
import stage_records  # noqa: E402


def test_1_inventory_g_passes_readers(monkeypatch, tmp_path):
    seen = {}

    def spy(root, readers=None):
        seen["readers"] = readers
        return {"status": "PASS", "inv": {}, "classes": {}, "unlisted": [], "violations": []}

    monkeypatch.setattr(hwsc_registry, "inventory_c", spy)
    gr.inventory_g(tmp_path, {"hws-store": ["hws"]})
    assert seen["readers"] == {"hws-store": ["hws"]}
    a, _ = gr._inv_sha(tmp_path, {"inv": {"x": 1}, "classes": {"a": 1}})
    b, _ = gr._inv_sha(tmp_path, {"inv": {"x": 1}, "classes": {"a": 2}})
    assert a == b


def test_2_run_train_creates_reservation(monkeypatch, tmp_path):
    out = tmp_path / "store"
    kc = out / "stages" / "KC" / "KG_RECORD.json"
    kc.parent.mkdir(parents=True)
    stage_records.write_new(kc, {"status": "PASS"})
    monkeypatch.setattr(grec, "preflight", lambda *a, **k: {"refused": False})
    monkeypatch.setattr(gh, "load", lambda *a, **k: {})
    monkeypatch.setattr(gt, "ram_ok", lambda *a, **k: {"ok": True})

    class P:
        def wait(self):
            return 0

    acc = {"accept": True, "kc_record_sha256": stage_records.sha256(kc)}
    gt.run_train(out, "lo", {}, {}, acc, "jobx", launcher=lambda argv, env: P())
    r = gc.world_dir(out, "lo") / "RESERVATION_W2.json"
    assert json.loads(r.read_text())["id"] == "RES-HWSG-LO-W2"


def test_3_sources_passes_contract_scratch_table(monkeypatch, tmp_path):
    rows = [{"name": "paper", "decision": "EXCLUSION"}]
    monkeypatch.setitem(gr.REG, "scratch_dirs_at_0224", rows)
    seen = {}
    monkeypatch.setattr(gr, "source_scratch_g",
                        lambda scratch, table=None: seen.setdefault("t", table) or gr._new())
    gr.sources(tmp_path, tmp_path, gc.TAGS)["scratch_g"]()
    assert seen["t"] == rows


def test_4_rerun_archives_and_kg4_takes_newest(monkeypatch, tmp_path):
    f = tmp_path / "stages" / "KC" / "KG_RECORD.json"
    f.parent.mkdir(parents=True)
    f.write_text("{}")
    gk._archive(tmp_path, f, "KC")
    assert not f.exists() and (tmp_path / "superseded" / "KC-a1" / "stages/KC/KG_RECORD.json").is_file()
    counter = {"n": 0}

    class P:
        def wait(self):
            return 0

    def launcher(argv, env):
        d = Path(argv[argv.index("--out") + 1])
        m = argv[argv.index("--master") + 1]
        counter["n"] += 1
        d.mkdir(parents=True, exist_ok=True)
        (d / f"KG4_{m}_{counter['n']}.json").write_text(json.dumps({"checksums": {"0": "a"}}))
        return P()

    old = tmp_path / "kg4" / "concurrent"
    old.mkdir(parents=True)
    (old / "KG4_620901_0.json").write_text(json.dumps({"checksums": {"0": "STALE"}}))
    import os
    os.utime(old / "KG4_620901_0.json", (1, 1))
    r = gk.kg4(tmp_path, launcher)
    assert r["status"] == "PASS"


def test_5_superseded_name_accepted(tmp_path):
    from hwsc_records import superseded_ok

    f = tmp_path / "stages" / "TRAIN" / "620611" / "TRAIN_RECORD.json"
    f.parent.mkdir(parents=True)
    f.write_text("{}")
    k4b_release.archive_attempt(tmp_path, "jobx-620611-a1", [f], {})
    assert superseded_ok(tmp_path) == []


def test_6_identity_checker_uses_passed_store(monkeypatch, tmp_path):
    monkeypatch.setattr(gc, "STORE", tmp_path)
    seen = {}

    def fake_load(w, store=None, expected_sha256=None):
        seen["store"] = store
        return {"process_identities": {"ids": {}, "arrays_sha256": {}}}

    monkeypatch.setattr(gh, "load", fake_load)
    monkeypatch.setattr(go, "identity", lambda *a, **k: {"ok": True, "checks": {}, "ids": {},
                                                         "arrays_sha256": {}})
    with gb.world("lo"):
        go.identity_checker("lo")(None, {})
    assert Path(seen["store"]) == tmp_path
