"""C1' numerical-environment identity (API.md §14; protocol §18 field 2, review RC8): rebind
env_identity.SCIENTIFIC_IMPORTS to the C1 set (adds torch and the c1prime modules), then call
import_scientific(), then record(). record() itself does not consult SCIENTIFIC_IMPORTS."""

from __future__ import annotations

import c1_config  # noqa: F401  (sys.path)
import env_identity

SCIENTIFIC_IMPORTS = (
    "argparse", "decimal", "fractions", "hashlib", "json", "statistics", "zipfile", "zlib",
    "importlib.util", "numpy", "scipy", "scipy.optimize", "scipy.sparse", "scipy.sparse.csgraph",
    "scipy.sparse.linalg", "scipy.spatial.distance", "scipy.special", "ripser", "threadpoolctl",
    "torch", "topo_pilot.contracts", "topo_pilot.contracts.backends", "topo_pilot.oracle",
    "topo_pilot.dataset", "topo_pilot.learner", "topo_pilot.analysis.x4f_scores",
    "topo_pilot.experiment.x4f_probe", "topo_pilot.prediction.ridge", "oracle_profile",
    "independent_reference", "errors", "cochain", "chart", "scores", "precision", "error_bound",
    "stage_records", "op_guard", "adapter", "c1_config", "c1_records", "c1_chart", "c1_oracle",
    "c1_cert", "c1_means", "c1_bounds", "c1_model", "c1_fit", "c1_gates", "c1_endpoint",
    "c1_data", "c1_release")


def record() -> dict:
    env_identity.SCIENTIFIC_IMPORTS = SCIENTIFIC_IMPORTS
    env_identity.import_scientific()
    rec = env_identity.record()
    rec["c1_scientific_imports"] = list(SCIENTIFIC_IMPORTS)
    return rec
