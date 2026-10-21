"""C2 oracle: process loading, the H1 static checks, the canonical oracle for the four
histories, the normalised predictive, d and G for the x and y pairs, the five nuisance
covariates, eligibility, kappa_m, zero-modulus flags, the H3 composition with the Decimal rows
for H^R, and the rotation oracle (API.md §6; C2-FROZEN-v1 §2.2, §2.3, §2.11, §5.4, §7 rows 3, 6).

The oracle is canonical; every d is converted to the model's named order only by
c1_oracle.named_from_canonical (RC-1). c2_model is imported inside the functions that use its
SYMBOL-ORDER checks (no import cycle; API.md §1 order c2_oracle <- c2_model).
"""

from __future__ import annotations

from fractions import Fraction

import c2_config as cc  # first: the API.md §1 sys.path convention

# isort: split
import c1_cert
import c1_oracle
import c2_data as cd
import error_bound
import numpy as np

ORACLE, IDENTITY = "FAIL_TECHNICAL/ORACLE", "FAIL_TECHNICAL/IDENTITY"
NUMERICAL = "INCONCLUSIVE/NUMERICAL"
_RANK = {"PASS": 0, NUMERICAL: 1, ORACLE: 2}


# ---- process and H1 (§7 row 3; API.md §6.1) --------------------------------------------------
def load_process() -> dict:
    """The job-0014 inputs.load_config/load_process (unchanged), keyed by int model seed."""
    import inputs
    import oracle_profile

    cfg = inputs.load_config()
    c = cc.CONTRACT
    ids_ok = (
        cfg["world"]["artifact"] == c["shared"]["WorldSpec"]
        and cfg["transition"]["artifact"] == c["shared"]["TransitionSpec"]
        and {int(k): v for k, v in cfg["emissions"].items()}
        == {int(m): v["EmissionSpec"] for m, v in c["models"].items()}
    )
    proc = inputs.load_process(cfg)
    E_named = {int(k): np.asarray(v, dtype=np.float64) for k, v in proc["E_named"].items()}
    perm = {int(k): np.asarray(v, dtype=np.int64) for k, v in proc["perm"].items()}
    E_canon = {j: oracle_profile.canonical_emission(E_named[j], perm[j]) for j in E_named}
    return {
        "T": proc["T"],
        "pi": proc["pi"],
        "coords": proc["coords"],
        "E_named": E_named,
        "perm": perm,
        "E_canon": E_canon,
        "ids_ok": bool(ids_ok),
        "identity": proc["identity"],
        "process_checks": proc["process_checks"],
    }


def h1_static(proc) -> dict:
    """C1 H1 unchanged (ids, validate_process, permutations, round trip, identical canonical
    emissions, the C1' P0 precondition of the reused H3 fast path) and SYMBOL-ORDER (b)."""
    import c2_model as cm

    models, perm, Ec = cc.MODELS, proc["perm"], proc["E_canon"]
    first = Ec[models[0]]
    checks = {
        "ids": bool(proc["ids_ok"]),
        "process": set(int(k) for k in proc["process_checks"]) == set(models),
        "perms": all(sorted(perm[j].tolist()) == list(range(cc.V)) for j in models),
        "roundtrip": all(
            np.array_equal(np.argsort(perm[j])[perm[j][np.arange(cc.V)]], np.arange(cc.V))
            for j in models
        ),
        "E_identical": all(
            np.array_equal(Ec[j], first) and Ec[j].tobytes() == first.tobytes() for j in models
        ),
    }
    checks["order_b"] = all(bool(cm.symbol_order_b(perm[j])) for j in models)
    p0 = c1_cert.p0(proc["T"], [Ec[j] for j in models], proc["pi"])
    checks["p0"] = bool(p0["ok"])
    return {"status": "PASS" if all(checks.values()) else IDENTITY, "checks": checks, "p0": p0}


# ---- oracle rows (§2.3, §5.4; API.md §6.2) ---------------------------------------------------
def oracle_role(T, E, pi, tokens32, coords=None) -> dict:
    """c1_oracle.run_oracle plus q-bar; "m32" only when coords is given (API.md §19.1 E-5)."""
    r = c1_oracle.run_oracle(T, E, pi, tokens32)
    q = r["q"]
    out = {
        "b31": r["b31"],
        "b32": r["b32"],
        "q": q,
        "qbar": q / q.sum(1, keepdims=True),
        "s": r["s"],
        "le": r["log_evidence"],
    }
    if coords is not None:
        out["m32"] = c1_oracle.m32(r["b32"], coords)
    return out


def oracle_split(T, E, pi, coords, canon32) -> dict:
    o = {role: oracle_role(T, E, pi, H, coords) for role, H in zip(cc.ROLES, cd.donors4(canon32))}
    for pair, (a, b) in cc.PAIRS.items():
        o[f"G_{pair}"], o[f"d_{pair}"] = c1_oracle.G_hat(o[a]["qbar"], o[b]["qbar"])[:2]
    o["nuis"] = nuisance5(o["H"]["b32"], coords)
    return o


def nuisance5(b32, coords) -> np.ndarray:
    """(y-bar, Var y, |m32|) of c1_oracle.nuisance, the entropy (nats, 0 log 0 = 0) and the
    second x-harmonic modulus |sum_z b(z) exp(2i 2 pi x(z) / 12)|."""
    b = np.asarray(b32, dtype=np.float64)
    ent = -np.sum(np.where(b > 0, b * np.log(np.where(b > 0, b, 1.0)), 0.0), axis=1)
    x = np.rint(np.asarray(coords, dtype=np.float64)[:, 0])
    ang = 2.0 * 2.0 * np.pi * x / 12.0
    h2 = np.hypot(b @ np.cos(ang), b @ np.sin(ang))
    return np.column_stack((c1_oracle.nuisance(b, coords), ent, h2))


def d_named(d_canon, perm) -> np.ndarray:
    return c1_oracle.named_from_canonical(d_canon, perm)


def s_max(s_fit_H) -> float:
    return c1_oracle.s_max(s_fit_H)


def eligibility(o, smax) -> dict:
    le = {r: np.asarray(o[r]["le"]) for r in cc.ROLES}
    E_x = c1_oracle.eligible(o["Hp"]["s"], o["Hm"]["s"], smax, le["H"], le["Hp"], le["Hm"])
    E_y = (np.asarray(o["HR"]["s"]) <= smax) & np.isfinite(le["H"]) & np.isfinite(le["HR"])
    return {"E_x": np.asarray(E_x, dtype=bool), "E_y": np.asarray(E_y, dtype=bool)}


def kappa_m(m32_H, m32_HR, E_y_fit, m32_H_fit) -> float:
    diff = (np.asarray(m32_H) - np.asarray(m32_HR))[np.asarray(E_y_fit, dtype=bool)]
    num = float(np.mean(np.sum(diff * diff, axis=1)))
    return num / float(np.trace(np.cov(np.asarray(m32_H_fit, dtype=np.float64).T, ddof=0)))


def y_active(kappa) -> bool:
    return Fraction(float(kappa)) < cc.KAPPA_M


def kappa_nu(o_fit, E_x_fit, coords) -> float:
    nu = {r: c1_oracle.y_marginal(o_fit[r]["b32"], coords) for r in ("H", "Hp", "Hm")}
    return c1_oracle.kappa_nu(nu["Hp"], nu["Hm"], nu["H"], E_x_fit)


def phi_star(m32) -> tuple:
    """Oracle x-phase arg m32 and m_valid = |m32| > 1e-12; the phase is 0.0 on invalid rows."""
    m = np.asarray(m32, dtype=np.float64)
    valid = np.linalg.norm(m, axis=1) > cc.ZERO_MOD
    return np.where(valid, np.arctan2(m[:, 1], m[:, 0]), 0.0), valid


def reason_flags(o, smax) -> dict:
    """The §5.5 oracle reasons of c2_data.REASONS (every applicable reason of every row)."""
    tag = {"H": "H", "Hp": "PLUS", "Hm": "MINUS", "HR": "REFL"}
    out = {f"S_{tag[r]}": np.asarray(o[r]["s"]) > smax for r in ("Hp", "Hm", "HR")}
    out.update({f"LIK_{tag[r]}": ~np.isfinite(np.asarray(o[r]["le"])) for r in cc.ROLES})
    out.update(
        {
            f"ZERO_MOD_{tag[r]}": np.linalg.norm(o[r]["m32"], axis=1) <= cc.ZERO_MOD
            for r in ("H", "Hp", "Hm")
        }
    )
    return {k: out[k] for k in cd.REASONS}


# ---- H3 (§7 row 6; T1-T8; API.md §6.3) -------------------------------------------------------
def _rel_rows(xh, xr, tol) -> bool:
    return all(c1_oracle.rel_agree(a, b, tol) for a, b in zip(xh, xr))


def _worst(a, b) -> str:
    return a if _RANK[a] >= _RANK[b] else b


def _closed_forms(T, E, coords, canon, o, tols) -> bool:
    w32 = np.asarray(canon)[:, 31].astype(np.int64)
    maps = (
        ("Hp", c1_oracle.rho_index(coords, 1), tols["tau"]),
        ("Hm", c1_oracle.rho_index(coords, -1), tols["tau"]),
        ("HR", cd.rho_R_index(coords), tols["rho_R"]),
    )
    return all(
        _rel_rows(o[role]["b32"], c1_oracle.closed_form_b32(o["H"]["b31"], T, E, w32, rho), tol[1])
        for role, rho, tol in maps
    )


def _named_and_cross(T, pi, perms, E_named, canon, o) -> tuple:
    roles = dict(zip(cc.ROLES, cd.donors4(canon)))
    named_ok = cross_ok = True
    for j in cc.MODELS:
        perm = np.asarray(perms[j])
        for role, H in roles.items():
            qn = c1_oracle.run_oracle(T, E_named[j], pi, perm[H])["q"]
            named_ok &= _rel_rows(
                c1_oracle.canonical_from_named_cols(qn, perm), o[role]["q"], cc.T_NAMED
            )
        for pair, (a, b) in cc.PAIRS.items():
            G, d, lam = c1_oracle.G_hat(o[a]["qbar"], o[b]["qbar"])[:3]
            Gn = c1_oracle.G_named(d, lam, perm)
            cross_ok &= bool(np.max(np.abs(Gn - o[f"G_{pair}"])) <= float(cc.T_CROSS_G))
    return named_ok, cross_ok


def h3(T, E, pi, coords, perms, E_named, splits, p0=None) -> dict:
    """H3 in the API.md §6.3 order; `splits` = {split: (canon32, o, E_x, E_y, seq_ids)}.
    SYMBOL-ORDER (c) runs on the d arrays of the FIT split (S1) or the TEST split (T-PRE)."""
    import c2_model as cm

    T, E, pi = (np.asarray(a, dtype=np.float64) for a in (T, E, pi))
    sym = {
        "tau": c1_oracle.symmetry_report(T, E, pi, coords),
        "rho_R": cd.symmetry_report_R(T, E, pi, coords),
    }
    out = {
        "status": ORACLE,
        "checks": {},
        "symmetry": {k: {a: str(b) for a, b in v.items()} for k, v in sym.items()},
    }
    if not all(s["symmetry_ok"] and s["exact_invariance"] for s in sym.values()):
        return out
    tols = {k: c1_oracle.closed_form_tolerance(s["eps_sym"]) for k, s in sym.items()}
    if any(t is None for t in tols.values()):
        return out
    p0 = c1_cert.p0(T, [E], pi) if p0 is None else p0
    ck = {"closed_form": True, "named": True, "G_cross": True, "q_sum": True, "order_c": True}
    decimal = "PASS"
    for split, (canon, o, E_x, E_y, seq) in splits.items():
        ck["closed_form"] &= _closed_forms(T, E, coords, canon, o, tols)
        named_ok, cross_ok = _named_and_cross(T, pi, perms, E_named, canon, o)
        ck["named"], ck["G_cross"] = ck["named"] and named_ok, ck["G_cross"] and cross_ok
        ck["q_sum"] &= all(
            bool(np.max(np.abs(np.sum(o[r]["q"], axis=1) - 1.0)) <= float(cc.T_QSUM))
            for r in cc.ROLES
        )
        both = np.flatnonzero(np.asarray(E_x, dtype=bool) & np.asarray(E_y, dtype=bool))
        rows = both[np.argsort(np.asarray(seq)[both], kind="stable")[: cc.H3_ROWS]]
        decimal = _worst(decimal, decimal_rows(T, E, pi, canon, o, rows, p0))
        if split in ("fit", "test"):
            ck["order_c"] &= all(
                bool(cm.symbol_order_c(o[f"d_{p}"], perms[j])) for j in cc.MODELS for p in cc.PAIRS
            )
    out["checks"] = dict(ck, decimal=decimal)
    oracle_ok = ck["closed_form"] and ck["named"] and ck["G_cross"] and ck["q_sum"]
    out["status"] = ORACLE if not oracle_ok else IDENTITY if not ck["order_c"] else decimal
    return out


def decimal_rows(T, E, pi, canon32, o, rows, p0) -> str:
    """C1' H3 Decimal rows for the four roles with the C1' fast-path rule (API.md C-7):
    b31, b32 and q by h3_compare, surprisal (T5), and G of the x and y pairs (T6)."""
    roles = dict(zip(cc.ROLES, cd.donors4(canon32)))
    beta = Fraction(error_bound.posterior_envelope(32, p0["N"]))
    status = "PASS"
    for i in np.asarray(rows, dtype=np.int64).tolist():
        refs = {}
        for role, H in roles.items():
            ref = refs[role] = c1_oracle.decimal_reference(T, E, pi, H[i])
            ref0 = c1_cert.reference_oracle(T, E, pi, H[i : i + 1])
            p1 = bool(c1_cert.p1(ref0["nu_min"], ref0["finite"], p0["nu0"])[0])
            for key, dkey in (("b31", "b31"), ("b32", "b32"), ("q", "q32")):
                status = _worst(status, c1_oracle.h3_compare(o[role][key][i], ref[dkey], p1, beta))
            if abs(Fraction(float(o[role]["s"][i])) - Fraction(ref["s"])) > cc.frac(
                cc.T_DEC_SURPRISAL
            ):
                status = ORACLE
        for pair, (a, b) in cc.PAIRS.items():
            Gt = Fraction(c1_oracle.decimal_G(refs[a]["q32"], refs[b]["q32"]))
            lam = np.log(o[a]["qbar"][i]) - np.log(o[b]["qbar"][i])
            bound = cc.frac(cc.T_DEC_G) * (1 + Fraction(float(np.max(np.abs(lam)))))
            if abs(Fraction(float(o[f"G_{pair}"][i])) - Gt) > bound:
                status = ORACLE
    return status


# ---- rotation oracle (§2.11; API.md §6.4) ----------------------------------------------------
def rotation_oracle(b31_H, T, E, w32, coords, m) -> dict:
    """Roll the pre-last-symbol belief by +-m cells and re-apply w32 (corrected oracle, Q1)."""
    out = {}
    for sign, tag in ((1, "plus"), (-1, "minus")):
        b = c1_oracle.closed_form_b32(b31_H, T, E, w32, cd.rho_m_index(coords, sign * int(m)))
        q = (b @ np.asarray(T)) @ np.asarray(E)
        out[f"b_{tag}"], out[f"q_{tag}"] = b, q / q.sum(axis=1, keepdims=True)
    out["d"] = out["q_plus"] - out["q_minus"]
    out["G"] = c1_oracle.G_hat(out["q_plus"], out["q_minus"])[0]
    return out
