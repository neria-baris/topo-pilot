"""X6ZC run: the CLI (API.md §11.5). It re-exports the store, pipeline, dry-run and stage
modules (API.md §1, §20 C-52), so every API name stays reachable as zr.<name>. Torch-heavy X6S1
modules are imported lazily inside the functions that need them."""
# fmt: off

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import x6zc_core as zc  # first: applies the X6S1 sys.path convention

# isort: split
# isort: off
from x6zc_store import (_utc, _sha, _norm, _js, _cj, xwrite, _append, _lines,  # noqa: E402, F401
    log_exposure, guard, log_evaluation, write_stage, write_ruling, rulings,  # noqa: E402, F401
    x6s1_inventory, inventory_equal, env_check, closure_diff, _hit,  # noqa: E402, F401
    master_fresh, meter_bind_check, BIND_TEMPLATE, bind_template, ledger_cpu,  # noqa: E402, F401
    pause_check, _head, _frozen)  # noqa: E402, F401
# isort: on
# isort: off
from x6zc_pipeline import (predict_variants, stage_c_statistics, _f4,  # noqa: E402, F401
    licence_values, decide_report, TOP, CELL_KEYS, _OUTS, _outcome_ok,  # noqa: E402, F401
    validate_report)  # noqa: E402, F401
# isort: on
# isort: off
from x6zc_dry import (Planted, sd_parse, _jitter, _pool, _ev, dry, se_qstar)  # noqa: E402, F401
# isort: on
# isort: off
from x6zc_stage_a import (RUN, _x6, _payload, _npz, _dirs, _record, _begin,  # noqa: E402, F401
    _finish, _find, _passes, a1_check, _A2_ROW, a2_check, stage_a, _cache,  # noqa: E402, F401
    _spec, _predictor, _Memo, _children, chunk)  # noqa: E402, F401
# isort: on
# isort: off
from x6zc_stage_bc import (_terms, _boot, _arm, stage_b, _ev_base, stage_c)  # noqa: E402, F401
# isort: on

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="x6zc_run.py")
    ap.add_argument("command", choices=("dry", "A", "B", "C", "report", "chunk", "ruling",
                                        "master-check", "bind-template"))
    for a in ("--store", "--job", "--dispatch", "--stage", "--model", "--out", "--id", "--check",
              "--cause", "--defect-md", "--session", "--cause-identified", "--affects-beta"):
        ap.add_argument(a)
    ap.add_argument("--setup", action="store_true")
    a = ap.parse_args(argv)
    st = a.store or (zc.DRY_STORE if a.command == "dry" else zc.STORE)
    try:
        if a.command == "dry":
            cpu0, rep = time.process_time(), dry(st)
            if (Path(zc.STORE) / "cpu_ledger.json").exists():  # the stage-0 record (API §11.4)
                write_stage(zc.STORE, "0", {"stage": "0", "head": _head(), "utc": _utc(),
                                            "dry_report_sha256": rep["sha256"], "stop": None,
                                            "all_pass": rep["all_pass"], "scratch": st,
                                            "cpu_s": time.process_time() - cpu0,
                                            "cpu_cumulative_s": ledger_cpu(zc.STORE)})
            print(json.dumps(_js(rep), indent=1))
            return 0 if rep["all_pass"] else 2
        if a.command == "master-check":
            r = master_fresh()
            print(json.dumps(r))
            return 0 if r["fresh"] else 2
        if a.command == "bind-template":
            print(bind_template(a.out, a.session, st))
            return 0
        if a.command == "ruling":
            print(write_ruling(st, a.id, a.check, a.stage, a.cause_identified == "1",
                               a.affects_beta == "1", a.cause, a.defect_md, a.setup))
            return 0
        if a.command == "report":
            errs = validate_report(json.loads((Path(st) / "report.json").read_text("utf-8")))
            print(json.dumps(errs))
            return 2 if errs else 0
        if a.command == "chunk":
            return chunk(a.stage, a.model, a.out, st)
        return {"A": stage_a, "B": stage_b, "C": stage_c}[a.command](st)
    except (RuntimeError, ValueError, OSError) as e:
        print(f"x6zc_run: {e!r}", file=sys.stderr)
        return 1
if __name__ == "__main__":
    sys.exit(main())
