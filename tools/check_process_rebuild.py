"""Rebuild every stored TransitionSpec and EmissionSpec and compare id + payload checksum.

Regression check for changes to ``process`` (e.g. the ``is_x_periodic`` fix): each spec is
rebuilt from its stored parent WorldSpec and its stored config into an in-memory store, and the
rebuilt artifact id and ``payload_sha256`` must equal the stored ones. Reads ``artifacts/``,
writes nothing. Exit code 0 iff every spec matches.

Usage: ``python tools/check_process_rebuild.py [--root artifacts]``
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    LocalFSBackend,
    MemoryBackend,
    SeedTree,
    TransitionSpec,
    WorldSpec,
)
from topo_pilot.process import EmissionConfig, ProcessStage, TransitionConfig

PROCESS_KEYS = {"replicate", "world_scope_master"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="artifacts")
    args = ap.parse_args()
    src = ArtifactStore(LocalFSBackend(Path(args.root)))
    proc, bad, n = ProcessStage(), [], 0
    for cls in (TransitionSpec, EmissionSpec):
        for aid in src.find(cls):
            meta = src.meta(aid)
            (wid,) = meta.parent_ids
            wmeta = src.meta(wid)
            mem = ArtifactStore(MemoryBackend())
            mem.save(src.load(WorldSpec, wid, consumer="process"), config=wmeta.config,
                     parents=list(wmeta.parent_ids), seed_map=dict(wmeta.seed_map),
                     consumer="world")
            cfg = {k: v for k, v in meta.config.items() if k not in PROCESS_KEYS}
            if cls is TransitionSpec:
                new = proc.run_transition(wid, TransitionConfig(**cfg), mem)
            else:
                new = proc.run_emission(wid, EmissionConfig(**cfg),
                                        SeedTree(int(meta.config["replicate"])), mem)
            same = new == aid and mem.meta(new).payload_sha256 == meta.payload_sha256
            n += 1
            if not same:
                bad.append(f"{cls.ARTIFACT_TYPE} {aid} -> {new}")
    print(f"rebuilt {n} process specs; mismatches: {len(bad)}")
    for line in bad:
        print("  " + line)
    return 0 if n and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
