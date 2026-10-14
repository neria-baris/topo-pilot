"""Real-data Context for runner.py. Imported ONLY after a verified coordinator release.

Pins every scientific module to this worktree and checks it against the freeze. Binds the
unchanged job-0014 controls to the released job for the safe-boundary guard. Builds the real
read-only artifact store. Loads the process through the unchanged job-0014
`inputs.load_process`, with its own unchanged config: the WorldSpec, TransitionSpec and three
EmissionSpecs are identical artifacts.

Spec v2.4: before any store access the frozen project dependency files (contracts subtree,
dataset/sampler.py) and the numerical implementation identity (env_identity) are verified and
no unfrozen project module may be loaded; check_loaded_modules repeats the module check at
stage end. The Context carries the native-operation timed hook (op_guard).
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


class StopRequested(RuntimeError):
    """STOP or invalid runtime control observed at a safe boundary (not a gate result)."""


def _sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _pin_modules(freeze: dict) -> dict:
    import independent_reference
    import oracle_profile

    import topo_pilot

    pinned = {}
    for mod in (topo_pilot, oracle_profile, independent_reference):
        path = Path(mod.__file__).resolve()
        if REPO.resolve() not in path.parents:
            raise RuntimeError(f"{mod.__name__} resolves outside this worktree: {path}")
        pinned[mod.__name__] = str(path)
    for rel, digest in freeze["files"].items():
        if _sha(REPO / rel) != digest:
            raise RuntimeError(f"frozen file changed: {rel}")
    import freeze_bind

    if set(freeze_bind.frozen_files()) != set(freeze["files"]):
        raise RuntimeError("frozen file set changed (file added or removed)")
    if freeze_bind.environment()["dist_info"] != freeze["environment"]["dist_info"]:
        raise RuntimeError("installed numerical dependencies differ from the freeze")
    import env_identity

    env_identity.import_scientific()
    unfrozen = env_identity.unfrozen_project_modules(set(freeze["files"]))
    if unfrozen:
        raise RuntimeError(f"unfrozen project modules loaded: {unfrozen}")
    if env_identity.record() != freeze["environment"]["numerical_identity"]:
        raise RuntimeError("numerical implementation identity differs from the freeze")
    return pinned


def check_loaded_modules(ctx) -> None:
    """Stage-end re-check: no unfrozen project module and no new site-packages distribution."""
    import env_identity
    from errors import Invalid

    frozen = ctx.notes["freeze"]
    unfrozen = env_identity.unfrozen_project_modules(set(frozen["files"]))
    known = set(frozen["environment"]["numerical_identity"]["distributions"])
    extra = [d for d in env_identity.loaded_distributions() if d not in known]
    if unfrozen or extra:
        raise Invalid(f"unfrozen modules loaded during the stage: {unfrozen} {extra}")


def _guard_factory(rel: dict, out: Path):
    import controls

    controls.JOB_ID = str(rel["job_id"])
    controls.TASK_SHA256 = str(rel["task_sha256"]).upper()

    def guard() -> None:
        state, why = controls.classify_all([controls.MAILBOX], out)
        while state == controls.HOLD:
            time.sleep(30)
            state, why = controls.classify_all([controls.MAILBOX], out)
        if state != controls.CONTINUE:
            raise StopRequested(f"{state}: {why}")

    return guard


def build(rel: dict):
    from runner import Context

    contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
    out = Path(contract["resources"]["output_root"])
    freeze = json.loads((out / "FREEZE.json").read_text(encoding="utf-8"))
    pinned = _pin_modules(freeze)
    guard = _guard_factory(rel, out)
    guard()
    import inputs
    import op_guard
    from adapter import E4Manifest

    from topo_pilot.contracts import ArtifactStore
    from topo_pilot.contracts.backends import LocalFSBackend

    cfg14 = inputs.load_config()
    proc = inputs.load_process(cfg14)
    process = {
        "T": proc["T"],
        "pi": proc["pi"],
        "E": proc["E"],
        "features": proc["features"],
        "coords": proc["coords"],
        "perm": {int(k): v for k, v in proc["perm"].items()},
        "canonical_spread": proc["identity"]["canonical_emission_max_spread"],
        "identity": proc["identity"],
        "process_checks": proc["process_checks"],
    }
    per_model = {
        int(m): {k: v for k, v in ids.items()}
        for m, ids in contract["artifacts"]["per_model"].items()
    }
    store = ArtifactStore(LocalFSBackend(Path(contract["artifacts"]["artifact_root"])))
    return Context(
        out=out,
        store=store,
        manifest=E4Manifest(per_model=per_model),
        models=[int(m) for m in contract["scope"]["models"]],
        process=process,
        contract=contract,
        guard=guard,
        timed=op_guard.timed_factory(out, contract["resources"]["native_operation_wall_s"]),
        notes={"pinned_modules": pinned, "freeze": freeze},
    )
