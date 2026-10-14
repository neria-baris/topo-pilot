"""X5 G1 training-study CLI (x5g1-train-v3 §10). Stages run separately so that the root can
authorise pools/training/dev analysis first and the fresh test last.

``python -m topo_pilot.experiment.x5g1t_main --config <json> [--repo .] pools``
``... train --arm a0 --master 310001`` | ``... dev-analysis``
| ``... final-test --authorized-final``
``python -m topo_pilot.experiment.x5g1t_main fixture --root <dir>`` builds the SYNTHETIC fixture.

Exit codes: 0 done; 2 STOP/budget/resource/hold-stop; 3 failure or refusal.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from .x5g1_controls import BudgetExceeded, LedgerCorrupt, StopRequested
from .x5g1_safety import OutputExists
from .x5g1t_fixture import build_fixture
from .x5g1t_runtime import ResourceExceeded, RunLocked
from .x5g1t_stages import (
    StudyConfig,
    StudyFailed,
    run_dev_analysis,
    run_final_test,
    run_pools,
    run_train,
)

log = logging.getLogger(__name__)


def _master(text: str):
    return int(text) if text.isdigit() else text


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="X5 G1 six-model training study (staged)")
    ap.add_argument("--config", type=Path)
    ap.add_argument("--repo", type=Path, default=Path("."))
    sub = ap.add_subparsers(dest="stage", required=True)
    sub.add_parser("pools")
    tr = sub.add_parser("train")
    tr.add_argument("--arm", required=True, choices=("a0", "a020"))
    tr.add_argument("--master", required=True, type=_master)
    sub.add_parser("dev-analysis")
    ft = sub.add_parser("final-test")
    ft.add_argument("--authorized-final", action="store_true")
    fx = sub.add_parser("fixture")
    fx.add_argument("--root", type=Path, required=True)
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if args.stage == "fixture":
        log.info("x5g1t fixture config: %s", build_fixture(args.root))
        return 0
    if args.config is None:
        ap.error("--config is required for study stages")
    cfg = StudyConfig.load(args.config)
    try:
        if args.stage == "pools":
            res = {"pools": len(run_pools(cfg, args.repo)["pools"])}
        elif args.stage == "train":
            res = {"status": run_train(cfg, args.repo, args.arm, args.master)["status"]}
        elif args.stage == "dev-analysis":
            r = run_dev_analysis(cfg, args.repo)
            res = {"verdict": r["verdict"], "reason": r["reason"]}
        else:
            res = {"models": len(run_final_test(cfg, args.repo, args.authorized_final)["models"])}
    except (StopRequested, BudgetExceeded, ResourceExceeded) as exc:
        log.error("x5g1t %s stopped: %s: %s", args.stage, type(exc).__name__, exc)
        return 2
    except (StudyFailed, RunLocked, OutputExists, LedgerCorrupt) as exc:
        log.error("x5g1t %s refused/failed: %s: %s", args.stage, type(exc).__name__, exc)
        return 3
    log.info("x5g1t %s: %s", args.stage, json.dumps(res))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
