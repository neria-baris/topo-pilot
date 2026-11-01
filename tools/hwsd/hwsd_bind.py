"""HWSD versioned binding: the hwsd binding table on hwsc_bind.bound_stage_c, the dry and identity
tables, the audit (API.md §2; protocol §3.3; KD2, DRD3)."""

from __future__ import annotations  # noqa: I001

import hwsd_config as dc
import copy
import importlib
import sys
from contextlib import contextmanager
from pathlib import Path

import hwsc_bind
import k4b_config
from c1_records import C1GateFailure


def decode(value, repo=None):
    """hwsc_bind.decode semantics, with hwsd's contract views and this worktree's REPO."""
    repo = dc.REPO if repo is None else repo
    if isinstance(value, list):
        return tuple(decode(v, repo) for v in value)
    if isinstance(value, dict) and len(value) == 1:
        (k, v), = value.items()
        if k == "__contract_view__":
            return copy.deepcopy(dc.CONTRACT[v])
        if k == "__repo__":
            return Path(repo) / v
    return hwsc_bind.decode(value, repo)


def _live(module, name):
    return getattr(importlib.import_module(module), name)


def load_table(which="hwsd", case=None, case_dir=None, process=None) -> list:
    if which not in ("hwsd", "identity", "dry"):
        raise ValueError(f"unknown table {which!r}")
    rows = [{"module": r["module"], "name": r["name"], "old": decode(r["old"]),
             "new": decode(r["new"])} for r in dc.CONTRACT["binding"]["table"]]
    if which == "hwsd":
        return rows
    if which == "identity":
        for r in rows:
            r["new"] = _live(r["module"], r["name"])
        return rows
    if case is None or case_dir is None:
        raise ValueError("the dry table needs case and case_dir")
    scope = f"{dc.DRY_SCOPE}/{case}"
    for r in rows:
        key = (r["module"], r["name"])
        if r["name"] == "MODELS":
            r["new"] = tuple(dc.DRY_MASTERS)
        elif r["name"] == "SCOPE" and r["module"] in ("k4b_config", "k4b_data", "k4b_decoder"):
            r["new"] = scope
        elif r["name"] == "PROCESS":
            r["new"] = tuple(process or dc.TINY_PROCESS)
        elif r["name"] == "SEEDS":
            r["new"] = dict(dc.DRY_SEEDS)
        elif key == ("k4b_config", "STORE"):
            r["new"] = Path(case_dir)
        elif key == ("k4b_driver", "ARTIFACTS"):
            r["new"] = Path(case_dir) / "artifacts"
    rows.append({"module": "hwsb_config", "name": "SCOPE", "old": "hwsb-v1", "new": dc.DRY_SCOPE})
    rows.append({"module": "hwsb_config", "name": "DRY_MASTERS", "old": (629901, 629902),
                 "new": tuple(dc.DRY_MASTERS)})
    return rows


@contextmanager
def bound_hwsd(table=None):
    with hwsc_bind.bound_stage_c(table if table is not None else load_table()) as info:
        yield info


def scope_modules() -> list:
    dirs = [(dc.REPO / d).resolve() for d in dc.CONTRACT["binding"]["audit"]["module_dirs"]]
    out = []
    for mod in list(sys.modules.values()):
        f = getattr(mod, "__file__", None)
        if f and any(Path(f).resolve().parent == d for d in dirs):
            out.append(mod)
    return sorted(out, key=lambda m: m.__name__)


def audit(modules=None) -> dict:
    b = dc.CONTRACT["binding"]
    return hwsc_bind.audit(modules if modules is not None else scope_modules(),
                           left_unchanged=b["left_unchanged"], forbidden=b["audit"]["forbidden"])


def never_called() -> tuple:
    return tuple(dc.CONTRACT["binding"]["never_called"])


def strong_seed() -> int:
    if k4b_config.SEEDS == dc.SEEDS:
        return dc.STRONG_SEED
    if k4b_config.SEEDS == dc.DRY_SEEDS:
        return dc.DRY_STRONG_SEED
    raise C1GateFailure("FAIL_TECHNICAL/BINDING", "strong seed outside a binding")
