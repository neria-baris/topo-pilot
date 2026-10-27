"""Store-local binding of the unchanged job-0014 meter for the C2ND runs (C2ND API.md 9.8; the
C2 c2_meter_bind.py pattern). Template: the coordinator copies it into c2nd-store (or into a
dry-run store) and binds its sha256 in FREEZE.json (DRY.json) "meter_bind_sha256".

Standard library only; run with the base interpreter and -I. Rebinds module-level names only
(the x6s1_meter_bind pattern): this store's ledger, lock, emergency, active and log paths;
CAP_S = STOP_NEW_S = inf (CPU measured, not capped); OUTPUT_CAP 16 GiB; winjob.MEMORY_CAP 12 GiB;
--max-cpu inf --max-wall inf forced; the owner disk floors (C: 2 GB, X: 30 GB) as a launch
refusal and a periodic safe-STOP. controls.JOB_ID, controls.TASK_SHA256 and meter.WORKER_SESSION
are read at launch from the dispatch record named by the ND_DISPATCH environment variable (keys
"job", "task_sha256", "worker_session"), so this file's sha256 does not depend on the run job.

Fail closed, before the meter starts: the record must name this file's sha256
("meter_bind_sha256") and the import directory ("meter_import_dir") = the C2ND execution
worktree's tools/x4_oracle_profile, and must carry the three identities; controls, meter and
winjob must be imported from that directory and have the sha256 they have at H.

Usage: ND_DISPATCH=<record.json> python -I nd_meter_bind.py --label <stage>__<label>
       [meter options] -- CMD...
"""

import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

WORKTREE = Path(r"X:\Downloads\projects\topo-pilot\topo-pilot-c2nd")
IMPORT_DIR = WORKTREE / "tools" / "x4_oracle_profile"
OUT = Path(__file__).resolve().parent
GIB = 1024**3
DISK_MIN_FREE = {"C:\\": 2_000_000_000, "X:\\": 30_000_000_000}
METER_FILES = {  # sha256 at H (tools/x4_oracle_profile is protected; C2's values)
    "controls": "c4fac9946c0fed21d6ac9eee913bad15e49cdc4595843e2737e7d8f4817f23eb",
    "meter": "738ea68accc7a02c0e5645fca75d1b0919cac66b9bdbe357d910f515d7de4903",
    "winjob": "3b29e863ab6ae97c16540c0d56dbf678d18b88922e54fbc731f5cc0ec5405785",
}


def _norm(p):
    return os.path.normcase(os.path.abspath(str(p)))


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _fail(why):
    sys.exit(f"nd_meter_bind: {why}")


RECORD = json.loads(Path(os.environ["ND_DISPATCH"]).read_text(encoding="utf-8-sig"))
if str(RECORD.get("meter_bind_sha256", "")).strip().lower() != _sha(__file__):
    _fail("the dispatch record does not bind this file's sha256")
if _norm(RECORD.get("meter_import_dir", "?")) != _norm(IMPORT_DIR):
    _fail(f"the dispatch record's meter_import_dir is not {IMPORT_DIR}")
if any(not str(RECORD.get(k) or "").strip() for k in ("job", "task_sha256", "worker_session")):
    _fail("the dispatch record lacks job, task_sha256 or worker_session")
for name, want in METER_FILES.items():
    if _sha(IMPORT_DIR / f"{name}.py") != want:
        _fail(f"{IMPORT_DIR / name}.py differs from its sha256 at H")
sys.path.insert(0, str(IMPORT_DIR))

import controls  # noqa: E402  (job-0014, unchanged)
import meter  # noqa: E402  (job-0014, unchanged)
import winjob  # noqa: E402  (job-0014, unchanged)

for _mod in (controls, meter, winjob):
    if _norm(Path(_mod.__file__).parent) != _norm(IMPORT_DIR):
        _fail(f"{_mod.__name__} was imported from {_mod.__file__}, not from {IMPORT_DIR}")

controls.JOB_ID = str(RECORD["job"])
controls.TASK_SHA256 = str(RECORD["task_sha256"]).strip().upper()
meter.WORKER_SESSION = str(RECORD["worker_session"])
meter.OUT, meter.LEDGER, meter.LOCK = OUT, OUT / "cpu_ledger.json", OUT / "RUN.lock"
meter.EMERGENCY, meter.ACTIVE = OUT / "cpu_ledger.emergency.jsonl", OUT / "METER_ACTIVE.lock"
meter.LOG_DIR = OUT / "logs"
meter.CAP_S = meter.STOP_NEW_S = float("inf")  # owner override: CPU measured, not capped
meter.OUTPUT_CAP = 16 * GIB
winjob.MEMORY_CAP = 12 * GIB


def disk_reason(usage=shutil.disk_usage):
    for drive, minimum in DISK_MIN_FREE.items():
        try:
            free = usage(drive).free
        except OSError as exc:
            return f"disk safe-STOP: {drive} free space unreadable ({type(exc).__name__})"
        if free < minimum:
            return f"disk safe-STOP: {drive} free {free} < {minimum} bytes"
    return None


def make_limiter(disk=disk_reason, legacy=None):
    legacy = legacy or meter.limit_reason

    def limit_reason(ledger, child, args, active_wall, polls, mailboxes):
        if disk is not None and polls % 8 == 0:
            reason = disk()
            if reason:
                return reason, "CONTINUE"
        return legacy(ledger, child, args, active_wall, polls, mailboxes)

    return limit_reason


def _drop(args, flag):
    while flag in args:
        i = args.index(flag)
        del args[i : i + 2]


def rewrite_argv(argv):
    args = list(argv)
    sep = args.index("--") if "--" in args else len(args)
    head, tail = args[:sep], args[sep:]
    _drop(head, "--max-cpu")
    _drop(head, "--max-wall")
    return head + ["--max-cpu", "inf", "--max-wall", "inf"] + tail


def main():
    args = rewrite_argv(sys.argv[1:])
    reason = disk_reason()
    if reason:
        i = args.index("--label")
        args[i + 1] += "__REFUSED_disk_safe_stop"
        sep = args.index("--")
        args = args[:sep] + ["--", sys.executable, "-I", "-c", "raise SystemExit(4)"]
    meter.limit_reason = make_limiter()
    sys.argv = [sys.argv[0]] + args
    return meter.main()


if __name__ == "__main__":
    sys.exit(main())
