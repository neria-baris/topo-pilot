"""HWSG dry run, part 1: synthetic cases DRG3-DRG8, DRG10, DRG11 (API.md §16; protocol §10.1).
Synthetic inputs only: no real master, stream, store write or array file under the project root."""

from __future__ import annotations  # noqa: I001

import hwsg_config as gc
import hwsg_bind
import hwsg_cross
import hwsg_known
import hwsg_oracle
import dataclasses
import types
from fractions import Fraction
from pathlib import Path

import hwsb_config
import hwsc_config
import hwsc_gates
import hwsc_outcome
import k4b_config
import k4b_stats
import numpy as np
from c1_records import C1GateFailure

from topo_pilot.process import TransitionConfig


def _res(checks, **extra) -> dict:
    return dict({"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}, **extra)


def _raises(fn, status=None) -> bool:
    try:
        fn()
    except C1GateFailure as exc:
        return status is None or exc.status == status
    return False


def drg3() -> dict:
    ch, seen = {}, []
    for t in gc.TAGS:
        with hwsg_bind.world(t):
            seen.append((hwsc_config.KEY, hwsc_config.PROCESS, hwsc_config.MASTERS,
                         hwsc_config.SIGMA, hwsc_config.NEIGHBOUR, k4b_config.MODELS,
                         k4b_config.SCOPE, str(hwsc_config.STORE)))
            ch[f"nested_refused_{t}"] = _raises(lambda: hwsg_bind.world(t).__enter__(),
                                                "FAIL_TECHNICAL/BINDING")
    ch["constants_change_per_world"] = len(set(seen)) == 3
    ch["restored"] = (hwsc_config.KEY, k4b_config.MODELS) == (
        hwsg_bind._IMPORT_VALUES[("hwsc_config", "KEY")], (1729, 2718, 3141))
    try:
        with hwsg_bind.world("hi"):
            raise RuntimeError("planted")
    except RuntimeError:
        pass
    ch["restored_after_exception"] = hwsc_config.KEY == hwsg_bind._IMPORT_VALUES[
        ("hwsc_config", "KEY")] and hwsg_bind.ACTIVE is None
    fake = types.ModuleType("planted_g")
    fake.__file__ = str(gc.REPO / "tools" / "k4b" / "planted_g.py")
    fake.GLOBAL = 1.75
    fake.TRIPLE = (620301, 620302, 620303)
    fake.CFG = TransitionConfig(p_stay=0.2)
    exec("def f(p_stay=0.2):\n    return p_stay", fake.__dict__)
    fake.f.__module__ = "planted_g"
    a = hwsg_bind.audit("lo", modules=[fake], left_unchanged=[])
    ch["planted_copies_caught"] = a["status"] == gc.BAD and a["n_hits"] >= 4
    ch["stale_ladder_defaults_refused"] = _raises(
        lambda: hwsg_bind.check_explicit("ladder_pilot", {"models": (1, 2, 3)}), gc.BAD)
    ch["identity_at_w_star"] = hwsg_known.kg1(None)["status"] == "PASS"
    return _res(ch)


def drg4() -> dict:
    r = hwsg_known.kg2()
    return _res({"shared_sigma_collides_only_under_sigma_tags":
                 r["planted_pair_collides_under_sigma_only"],
                 "key_tags_disjoint": r["ids_disjoint"], "draws_differ": r["draws_differ"]})


def _model(L, U, Fm, Fp):
    st = k4b_stats.model_status(L, U, Fm, Fp)
    return {"L": float(L), "U": float(U), "F_minus": Fraction(Fm), "F_plus": Fraction(Fp),
            "status": st["status"], "labels": st["labels"]}


def _overall(rows) -> dict:
    per = {j: r for j, r in zip(k4b_config.MODELS, rows)}
    return {"overall": k4b_stats.overall({j: r["status"] for j, r in per.items()}),
            "per_model": per}


def drg5() -> dict:
    z = Fraction(0)
    sup = _model(0.05, 0.06, z, z)
    exc = _model(0.0, 0.001, z, z)
    unr = _model(0.0105, 0.02, Fraction(1, 1000), z)
    pbm = _model(1e-9, 0.001, z, z)
    nul = _model(0.0, 0.001, z, z)
    tiny = _model(float(np.nextafter(0.0, 1.0)), 0.001, z, z)
    ch = {"SUPPORT": _overall([sup] * 3)["overall"] == "SUPPORT",
          "EXCLUSION": _overall([exc] * 3)["overall"] == "EXCLUSION",
          "MIXED": _overall([sup, exc, exc])["overall"] == "MIXED",
          "UNRESOLVED/NUMERICAL": unr["status"] == "UNRESOLVED/NUMERICAL",
          "pbm_listed": "POSITIVE_BELOW_MARGIN_" + str(k4b_config.MODELS[0]) in
          hwsc_outcome.annotations(_overall([pbm, exc, exc])),
          "exact_zero_not_positive": not hwsc_outcome.positive_below_margin(
              {1: nul})["positive"][1],
          "nextafter_zero_positive": hwsc_outcome.positive_below_margin(
              {1: tiny})["positive"][1]}
    return _res(ch)


def drg6() -> dict:
    ch = {}
    for n_p1 in (3072, 6144, 12288, None):
        r = hwsc_gates.choose_N(gc.N_C, {"N": n_p1})
        ch[str(n_p1)] = (r["status"] == "INCONCLUSIVE/UNDERPOWERED" if n_p1 is None
                         else r["N"] == n_p1 and r["k"] == n_p1 // 3072)
    return _res(ch)


def _w(tag, outcome, endpoint=True, p1=True, status=None, ratio=None, draws=None):
    return {"tag": tag, "outcome": outcome, "endpoint": endpoint, "p1_passed": p1,
            "per_model_status": status or {}, "per_model": {}, "ratio": ratio,
            "rho_draws": draws}


def drg7() -> dict:
    ws = [_w("lo", "INCONCLUSIVE/NOT_LEARNED", False, False),
          _w("mid", "SUPPORT", status={"1": "SUPPORT"}), _w("hi", "SUPPORT")]
    g = hwsg_cross.general(ws)
    import tempfile

    with tempfile.TemporaryDirectory(dir=str(gc.SCRATCH)) as td:
        (gc.world_dir(td, "lo")).mkdir(parents=True)
        missing = _raises(lambda: hwsg_cross.load_world(td, "lo"), "FAIL_TECHNICAL/LINEAGE")
    return _res({"general_unavailable": g["reading"] == "GENERAL_UNAVAILABLE",
                 "missing_world_is_lineage_failure": missing})


def drg8() -> dict:
    ch = {}
    d = gc.WORLDS["lo"]
    bad_nb = (1 - Fraction(repr(5 / 6))) / 4
    ch["repr_float_neighbour_differs"] = bad_nb != d.neighbour
    old = gc.F_PLAN_MAX
    try:
        gc.F_PLAN_MAX = Fraction(1, 10**12)
        mid = gc.WORLDS["mid"]
        from topo_pilot.contracts import ArtifactStore
        from topo_pilot.contracts.backends import MemoryBackend

        st = ArtifactStore(MemoryBackend())
        proc = hwsg_oracle.build_process_g(st, "mid")
        ch["F_plan_too_large_drops_world"] = _raises(
            lambda: hwsg_oracle.law(proc, "mid"), "FAIL_TECHNICAL/LAW_BOUND")
        gc.F_PLAN_MAX = old
        proc["neighbour"] = bad_nb
        ch["O1_refuses_float_neighbour"] = not hwsg_oracle.identity(st, proc, "lo")["ok"]
        ch["mid_neighbour_is_p_complement"] = mid.neighbour == (1 - mid.p) / 4
    finally:
        gc.F_PLAN_MAX = old
    return _res(ch)


def _ratio_world(tag, rho_l, rho_u, rho=0.8, n=5000, seed=1):
    g = np.random.default_rng(seed)
    per = {str(j): {"status": "DEFINED", "rho": rho, "rhoL": rho_l, "rhoU": rho_u,
                    "central95_minus": [rho_l, rho_u], "central95_plus": [rho_l, rho_u]}
           for j in (1, 2, 3)}
    draws = {str(j): rho + 0.01 * g.standard_normal(n) for j in (1, 2, 3)}
    w = _w(tag, "SUPPORT", ratio={"per_model": per, "status": "DEFINED"}, draws=draws)
    w["per_model"] = {str(j): {"L": 0.05, "F_minus": "0", "status": "SUPPORT"} for j in (1, 2, 3)}
    w["per_model_status"] = {str(j): "SUPPORT" for j in (1, 2, 3)}
    return w


def drg10() -> dict:
    ch = {}
    half = [_ratio_world("lo", 0.5, 0.9), _ratio_world("mid", 0.6, 0.9, seed=2),
            _ratio_world("hi", 0.7, 0.9, seed=3)]
    ch["rhoL_half_passes"] = hwsg_cross.capture(half)["reading"] == "CAPTURE_AT_LEAST_HALF"
    below = [_ratio_world("lo", 0.1, 0.4), _ratio_world("mid", 0.6, 0.9, seed=2)]
    ch["below_half"] = hwsg_cross.capture(below)["reading"] == "CAPTURE_BELOW_HALF"
    ch["unavailable_one_world"] = hwsg_cross.capture(half[:1])["reading"] == "CAPTURE_UNAVAILABLE"
    ch["unresolved"] = hwsg_cross.capture(
        [_ratio_world("lo", 0.4, 0.9), _ratio_world("mid", 0.6, 0.9, seed=2)])["reading"] \
        == "CAPTURE_UNRESOLVED"
    s = hwsg_cross.similarity(half)
    ch["similarity_labels_only"] = s["compatible"] in (True, False) and s["spread_bound"] > 0
    unr = _w("lo", "INCONCLUSIVE", True, True, {"1": "UNRESOLVED"})
    ch["support_plus_unresolved_unavailable"] = hwsg_cross.general(
        [_w("mid", "SUPPORT"), _w("hi", "SUPPORT"), unr])["reading"] == "GENERAL_UNAVAILABLE"
    mixed = _w("lo", "MIXED", True, True, {"1": "SUPPORT", "2": "EXCLUDE"})
    ch["mixed_with_exclude_not_general"] = hwsg_cross.general(
        [mixed, _w("mid", "SUPPORT"), _w("hi", "SUPPORT")])["reading"] == "NOT_GENERAL"
    return _res(ch)


def drg11() -> dict:
    root = gc.ROOT
    bl = [root / "hwsb-store/REPORT.json", root / "hwsb-store/stages/EVAL/x.json",
          root / "hwsu-store/stages/OF/a.npz", root / "tools/hwsd/hwsd_data.py",
          root / "agent-handoff/jobs/0200/task.md", root / "docs/research_summary/a.tex"]
    ok = [root / "tools/hwsd/CONTRACT.json", root / "agent-handoff/jobs/0224/task.md"]
    ch = {f"blocked_{i}": _raises(lambda p=p: gc.guard(p), "FAIL_TECHNICAL/BLINDNESS")
          for i, p in enumerate(bl)}
    ch.update({f"allowed_{i}": not gc.blinded(p) for i, p in enumerate(ok)})
    return _res(ch)


_ = (dataclasses, Path, hwsb_config)
