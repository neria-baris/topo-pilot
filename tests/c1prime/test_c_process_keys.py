"""Coordinator regression test (job 0039 review, ruling R11): `c1_driver._process` must return
`E_named` keyed by int model ids like `canon` and `perm`. The reused job-0014
`inputs.load_process` keys it by the config's emission keys, which are strings ('1729', ...),
and H3's named-order check indexes it with int MODELS (the KeyError: 1729 of job 0039).
Synthetic: `inputs` is replaced by a stub, so no artifact is read."""

from __future__ import annotations

import sys
import types
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
for _sub in ("tests/oracle_profile", "tools/x4_oracle_profile", "tools/x4_circle_history",
             "tools/c1prime"):
    if str(REPO / _sub) not in sys.path:
        sys.path.insert(0, str(REPO / _sub))

import c1_config  # noqa: E402
import c1_driver  # noqa: E402


def test_process_rekeys_e_named_to_int(monkeypatch):
    art = c1_config.CONTRACT["artifacts"]
    keys = [str(m) for m in c1_config.MODELS]
    rng = np.random.default_rng(0)
    E = {k: rng.dirichlet(np.ones(36), size=144) for k in keys}
    perm = {k: np.arange(36)[::-1].copy() for k in keys}
    stub = types.ModuleType("inputs")
    stub.load_config = lambda: {
        "world": {"artifact": art["shared"]["WorldSpec"]},
        "transition": {"artifact": art["shared"]["TransitionSpec"]},
        "emissions": {str(m): v["EmissionSpec"] for m, v in art["per_model"].items()}}
    stub.load_process = lambda cfg: {"E_named": E, "perm": perm}
    monkeypatch.setitem(sys.modules, "inputs", stub)
    ctx = types.SimpleNamespace(contract=c1_config.CONTRACT)
    p = c1_driver._process(ctx)
    assert p["ids_ok"] is True
    for name in ("E_named", "canon", "perm"):
        assert set(p[name]) == set(c1_config.MODELS), name
        assert all(isinstance(k, int) for k in p[name]), name
    for m in c1_config.MODELS:
        assert np.array_equal(p["E_named"][m], E[str(m)])
        assert np.array_equal(p["canon"][m], E[str(m)][:, perm[str(m)]])
