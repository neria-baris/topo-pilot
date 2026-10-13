"""Stage X4 (TEST_PLAN X08-X12), from SPEC.md "Stage X4" only; tiny runs, fake resolver."""
from collections import defaultdict
from pathlib import Path

import numpy as np
import pytest

from topo_pilot.contracts import ArtifactStore, LocalFSBackend, MetricRecords, MetricRow
from topo_pilot.experiment import STAGE_REGISTRY, load_config
from topo_pilot.experiment.x4 import X4Job, X4Panel, X4Run, run_rule_verdict, x4c_category

pytestmark = pytest.mark.experiment

REPO = Path(__file__).resolve().parents[2]

SEEDS = (1729, 2718, 3141)
FINAL = 5000
N_PANELS = 8
M, D_MODEL, V, N_STATES, K = 20, 8, 5, 6, 3
VIEWS = tuple(f"V{i}" for i in range(6))
STATUSES = ("SUPPORTED", "REJECTED", "INCONCLUSIVE")
CATEGORIES = ("V3_only", "V4_only", "both", "neither")


@pytest.fixture
def store(tmp_path):
    return ArtifactStore(LocalFSBackend(tmp_path / "artifacts"), producer_version="test")


@pytest.fixture
def cfg():
    return load_config(REPO / "configs" / "stages.yaml", repo_root=REPO)


# ---------------------------------------------------------------------------------------------
# synthetic data
# ---------------------------------------------------------------------------------------------
def _softmax_rows(rng, n_rows, n_cols):
    a = rng.random((n_rows, n_cols)) + 0.05
    return a / a.sum(axis=1, keepdims=True)


def _weights(rng):
    gamma = 1.0 + 0.1 * rng.normal(size=D_MODEL)
    beta = 0.1 * rng.normal(size=D_MODEL)
    W_U = rng.normal(size=(V, D_MODEL))
    return gamma, beta, W_U


def _panel(rng, tag, gamma, beta, W_U):
    Z = rng.normal(size=(M, D_MODEL))
    centred = Z - Z.mean(axis=1, keepdims=True)
    normed = centred / np.sqrt(centred.var(axis=1, keepdims=True) + 1e-5)
    ln_out = gamma * normed + beta
    logits = ln_out @ W_U.T
    ids = tuple(f"{tag}_h{i}" for i in range(M))
    return X4Panel(ids=ids, Z=Z, ln_out=ln_out, logits=logits)


def _oracle(rng):
    return {
        p: {
            "b32": _softmax_rows(rng, M, N_STATES),
            "b1": _softmax_rows(rng, M, N_STATES),
            "q": _softmax_rows(rng, M, V),
            "last_symbol": rng.integers(0, 2, size=M),
            "R2": rng.normal(size=(M, K)),
            "R3": rng.normal(size=(M, K)),
        }
        for p in range(N_PANELS)
    }


def make_run(world, condition, seed, parents, with_oracle=True):
    rng = np.random.default_rng([seed, {"cylinder": 0, "square": 1}.get(world, 2), ord(condition)])
    weights = {step: _weights(rng) for step in (0, FINAL)}
    panels = {}
    for step in (0, FINAL):
        gamma, beta, W_U = weights[step]
        for p in range(N_PANELS):
            panels[(step, p)] = _panel(rng, f"{world}{condition}{seed}s{step}p{p}",
                                       gamma, beta, W_U)
    return X4Run(
        world=world, condition=condition, seed=seed, panels=panels, weights=weights,
        oracle=_oracle(rng) if with_oracle else None,
        learning_gate=True, stored_S_V0={}, parents=tuple(parents),
    )


def save_parents(store, n=5):
    return [
        store.save(MetricRecords(rows=()), config={"stage": "fake_parent", "i": i}, parents=[],
                   seed_map={}, consumer="experiment")
        for i in range(n)
    ]


def make_runs(parents, skip=()):
    """3 replicates x 2 worlds (condition O) + one N run. ``parents`` has >= 5 ids."""
    runs, missing = [], []
    for si, seed in enumerate(SEEDS):
        for wi, world in enumerate(("cylinder", "square")):
            key = (world, "O", seed)
            if key in skip:
                missing.append(key)
                continue
            runs.append(make_run(world, "O", seed, parents[(si + wi) % 3: (si + wi) % 3 + 2]))
    runs.append(make_run("any", "N", SEEDS[0], (parents[3], parents[4]), with_oracle=False))
    return runs, missing


def fake_resolver(runs, missing):
    """Source-aware like StoreResolver: S4 holds the O and N runs, S5 the P runs."""
    conds = {"S4": ("O", "N"), "S5": ("P",)}

    def resolver(source_stage):
        keep = conds[source_stage]
        return ([r for r in runs if r.condition in keep],
                [m for m in missing if m[1] in keep])
    return resolver


def all_files(store):
    return {k: store.backend.get(k) for k in store.backend.list("")}


def load_rows(store, aid):
    return store.load(MetricRecords, aid, consumer="experiment").rows


def verdicts(rows, space, prefix, condition="O"):
    """Suffixes (statuses) of the verdict rows `prefix + <STATUS>` of one space and condition."""
    return [r.metric_id[len(prefix):] for r in rows
            if r.space == space and r.condition == condition and r.metric_id.startswith(prefix)]


# ---------------------------------------------------------------------------------------------
# X08 known answers
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("v3, v4, expected", [
    ("SUPPORTED", "SUPPORTED", "both"),
    ("SUPPORTED", "REJECTED", "V3_only"),
    ("REJECTED", "SUPPORTED", "V4_only"),
    ("REJECTED", "REJECTED", "neither"),
    ("INCONCLUSIVE", "SUPPORTED", "V4_only"),
    ("SUPPORTED", "INCONCLUSIVE", "V3_only"),
    ("INCONCLUSIVE", "INCONCLUSIVE", "neither"),
])
def test_X08_x4c_category(v3, v4, expected):
    assert x4c_category(v3, v4) == expected


def _keys(seeds=SEEDS, worlds=("cylinder", "square")):
    return [(w, s) for s in seeds for w in worlds]


def _args(n_pass_value=8, seeds=SEEDS, gate=True):
    keys = _keys(seeds)
    return {k: n_pass_value for k in keys}, {k: gate for k in keys}


def test_X08_run_rule_all_runs_pass_is_supported():
    n_pass, gates = _args(8)
    status, reason = run_rule_verdict(n_pass, gates, 7, 3)
    assert status == "SUPPORTED"
    assert isinstance(reason, str)


def test_X08_run_rule_exactly_min_passes_is_supported():
    n_pass, gates = _args(7)
    assert run_rule_verdict(n_pass, gates, 7, 3)[0] == "SUPPORTED"


def test_X08_run_rule_one_run_below_min_is_rejected():
    n_pass, gates = _args(8)
    n_pass[("square", 2718)] = 6
    assert run_rule_verdict(n_pass, gates, 7, 3)[0] == "REJECTED"


@pytest.mark.parametrize("bad", [False, None])
def test_X08_run_rule_failed_gate_is_inconclusive_with_reason(bad):
    n_pass, gates = _args(8)
    gates[("cylinder", 3141)] = bad
    status, reason = run_rule_verdict(n_pass, gates, 7, 3)
    assert status == "INCONCLUSIVE"
    assert isinstance(reason, str) and reason.strip()


def test_X08_run_rule_failed_gate_beats_failed_count():
    n_pass, gates = _args(8)
    n_pass[("cylinder", 1729)] = 0
    gates[("square", 1729)] = False
    assert run_rule_verdict(n_pass, gates, 7, 3)[0] == "INCONCLUSIVE"


def test_X08_run_rule_two_of_three_replicates_is_inconclusive():
    n_pass, gates = _args(8, seeds=SEEDS[:2])
    status, reason = run_rule_verdict(n_pass, gates, 7, 3)
    assert status == "INCONCLUSIVE"
    assert reason.strip()


def test_X08_run_rule_replicate_with_one_world_is_inconclusive():
    n_pass, gates = _args(8)
    del n_pass[("square", 3141)]
    del gates[("square", 3141)]
    assert run_rule_verdict(n_pass, gates, 7, 3)[0] == "INCONCLUSIVE"


# ---------------------------------------------------------------------------------------------
# X09 rows table + store contract
# ---------------------------------------------------------------------------------------------
def test_X09_x4job_writes_expected_rows(store, cfg):
    parents = save_parents(store)
    runs, missing = make_runs(parents)
    before = all_files(store)

    aid = X4Job(cfg, store, resolver=fake_resolver(runs, missing)).run()

    # store contract: exactly one new artifact, a MetricRecords with config stage X4
    after = all_files(store)
    for key, data in before.items():
        assert after[key] == data, f"pre-existing file changed: {key}"
    new_keys = set(after) - set(before)
    assert new_keys
    assert all(k.startswith(f"MetricRecords/{aid}/") for k in new_keys)
    assert sum(k.endswith("/meta.json") for k in new_keys) == 1
    meta = store.meta(aid)
    assert meta.artifact_type == "MetricRecords"
    assert meta.config["stage"] == "X4"
    assert meta.config["kind"] == "analysis"
    expected_parents = sorted({p for r in runs for p in r.parents})
    assert len(expected_parents) == 5
    assert list(meta.parent_ids) == expected_parents

    rows = load_rows(store, aid)
    assert rows and all(isinstance(r, MetricRow) for r in rows)
    by_space = defaultdict(set)
    for r in rows:
        by_space[r.space].add(r.metric_id)

    # space set is exactly the SPEC table (no run is missing, so no bare "x4" space)
    expected_spaces = ({f"x4:{v}" for v in VIEWS}
                       | {"x4:check", "x4:b", "x4:a", "x4:c", "x4:d:V0", "x4:d:V1",
                          "x4:h3p:V0", "x4:h3p:V1"})
    assert set(by_space) == expected_spaces

    def exact(space, ids):
        assert set(ids) <= by_space[space], (space, set(ids) - by_space[space])

    def verdict_present(space, prefix, suffixes=STATUSES):
        got = verdicts(rows, space, prefix)
        assert len(got) == 1, (space, prefix, got)
        assert got[0] in suffixes

    for v in VIEWS:
        sp = f"x4:{v}"
        exact(sp, ["S_H1", "D", "median_D", "n_positive", "u",
                   "delta_geom_all", "delta_geom_same_last_symbol"])
        verdict_present(sp, "F1rule_verdict_")
    exact("x4:check", ["ln_reconstruction_max_abs", "logits_from_U_max_abs",
                       "logits_from_visible_max_abs"])
    exact("x4:b", ["rho_V5_future1", "rho_V5_future1_median", "positive_control_passed"])
    verdict_present("x4:b", "X4b_verdict_")
    exact("x4:a", ["X4a_verdicts_equal", "X4a_caveat"])
    exact("x4:c", ["median_D_V3", "median_D_V4", "ratio_V3_V4"])
    verdict_present("x4:c", "X4c_", CATEGORIES)
    for a in ("V0", "V1"):
        exact(f"x4:d:{a}", ["rho_same_model", "rho_same_R2", "rho_same_R3", "panel_pass", "n_pass"])
        verdict_present(f"x4:d:{a}", "X4d_verdict_")
        exact(f"x4:h3p:{a}", ["rho_all_final", "rho_all_init", "rho_all_R2", "rho_all_R3",
                              "panel_pass", "n_pass"])
        verdict_present(f"x4:h3p:{a}", "H3prime_verdict_")

    # no row is an invented value for something that did not run
    assert not [r for r in rows if r.status == "not_run"]


def test_X09_grains_of_the_rows(store, cfg):
    parents = save_parents(store)
    runs, missing = make_runs(parents)
    rows = load_rows(store, X4Job(cfg, store, resolver=fake_resolver(runs, missing)).run())

    def sel(space, metric):
        return [r for r in rows if r.space == space and r.metric_id == metric]

    panels = set(range(N_PANELS))
    o_runs = {(w, s) for w in ("cylinder", "square") for s in SEEDS}
    for v in VIEWS:
        sh1 = [r for r in sel(f"x4:{v}", "S_H1") if r.condition == "O"]
        assert {(r.world, r.replicate, r.checkpoint, r.panel) for r in sh1} == {
            (w, s, st, p) for (w, s) in o_runs for st in (0, FINAL) for p in panels}
        n_rows = [r for r in sel(f"x4:{v}", "S_H1") if r.condition == "N"]
        assert {(r.checkpoint, r.panel) for r in n_rows} == {
            (st, p) for st in (0, FINAL) for p in panels}
        d = sel(f"x4:{v}", "D")
        assert {(r.replicate, r.panel) for r in d} == {(s, p) for s in SEEDS for p in panels}
        assert {r.condition for r in d} == {"O"}
        assert {r.replicate for r in sel(f"x4:{v}", "median_D")} == set(SEEDS)
        for metric in ("delta_geom_all", "delta_geom_same_last_symbol"):
            dg = sel(f"x4:{v}", metric)
            assert {(r.world, r.replicate, r.panel) for r in dg} == {
                (w, s, p) for (w, s) in o_runs for p in panels}
            assert {r.checkpoint for r in dg} == {FINAL}
        for r in sel(f"x4:{v}", "S_H1"):  # None values must carry a non-ok status
            assert (r.value is None) == (r.status != "ok")

    for a in ("V0", "V1"):
        for sp in (f"x4:d:{a}", f"x4:h3p:{a}"):
            assert {(r.world, r.replicate, r.panel) for r in sel(sp, "panel_pass")} == {
                (w, s, p) for (w, s) in o_runs for p in panels}
            assert {(r.world, r.replicate) for r in sel(sp, "n_pass")} == o_runs
    assert {(r.world, r.replicate, r.panel) for r in sel("x4:b", "rho_V5_future1")} == {
        (w, s, p) for (w, s) in o_runs for p in panels}
    assert {(r.world, r.replicate) for r in sel("x4:b", "rho_V5_future1_median")} == o_runs
    assert {r.replicate for r in sel("x4:c", "median_D_V3")} == set(SEEDS)
    assert {r.replicate for r in sel("x4:c", "ratio_V3_V4")} == set(SEEDS)

    check = [r for r in rows if r.space == "x4:check"]
    for metric in ("ln_reconstruction_max_abs", "logits_from_U_max_abs",
                   "logits_from_visible_max_abs"):
        mrows = [r for r in check if r.metric_id == metric]
        assert {(r.world, r.condition, r.replicate, r.checkpoint) for r in mrows} == (
            {(w, "O", s, st) for (w, s) in o_runs for st in (0, FINAL)}
            | {("any", "N", SEEDS[0], st) for st in (0, FINAL)})
        assert all(r.value is None or r.value >= 0 for r in mrows)
    # the synthetic ln_out is exactly gamma * LN(Z) + beta, so the reconstruction error is ~0
    for r in check:
        if r.metric_id == "ln_reconstruction_max_abs":
            assert r.value is not None and r.value < 1e-3


def test_X09_n_run_only_contributes_sh1_and_check(store, cfg):
    parents = save_parents(store)
    runs, missing = make_runs(parents)
    rows = load_rows(store, X4Job(cfg, store, resolver=fake_resolver(runs, missing)).run())
    n_rows = [r for r in rows if r.condition == "N" or r.world == "any"]
    assert n_rows
    for r in n_rows:
        assert r.condition == "N" and r.world == "any"
        assert (r.space in {f"x4:{v}" for v in VIEWS} and r.metric_id == "S_H1") \
            or r.space == "x4:check", (r.space, r.metric_id)
    # and the N run reaches no O-condition aggregate (replicate sets are the O seeds)
    assert {r.space for r in n_rows if r.space != "x4:check"} == {f"x4:{v}" for v in VIEWS}


# ---------------------------------------------------------------------------------------------
# X10 idempotence
# ---------------------------------------------------------------------------------------------
def test_X10_rerun_returns_same_id(store, cfg):
    parents = save_parents(store)
    runs, missing = make_runs(parents)
    job = X4Job(cfg, store, resolver=fake_resolver(runs, missing))
    first = job.run()
    files = all_files(store)
    second = X4Job(cfg, store, resolver=fake_resolver(runs, missing)).run()
    assert second == first
    assert set(all_files(store)) == set(files)
    assert len(store.find(MetricRecords, stage="X4")) == 1


# ---------------------------------------------------------------------------------------------
# X11 missing run
# ---------------------------------------------------------------------------------------------
def test_X11_missing_run_is_not_run_and_verdicts_inconclusive(store, cfg):
    parents = save_parents(store)
    gone = ("square", "O", 3141)
    runs, missing = make_runs(parents, skip={gone})
    assert missing == [gone]
    rows = load_rows(store, X4Job(cfg, store, resolver=fake_resolver(runs, missing)).run())

    avail = [r for r in rows if r.space == "x4" and r.metric_id == "run_available"]
    assert len(avail) == 1
    r = avail[0]
    assert r.status == "not_run" and r.value is None
    assert (r.world, r.condition, r.replicate) == ("square", "O", 3141)

    # nothing is invented for the missing run
    for row in rows:
        if (row.world, row.condition, row.replicate) == ("square", "O", 3141):
            assert row is r or row.status != "ok", (row.space, row.metric_id)

    # the affected verdicts cannot be decided
    for v in VIEWS:
        assert verdicts(rows, f"x4:{v}", "F1rule_verdict_") == ["INCONCLUSIVE"], v
    for a in ("V0", "V1"):
        assert verdicts(rows, f"x4:d:{a}", "X4d_verdict_") == ["INCONCLUSIVE"], a
        assert verdicts(rows, f"x4:h3p:{a}", "H3prime_verdict_") == ["INCONCLUSIVE"], a


# ---------------------------------------------------------------------------------------------
# X12 registry
# ---------------------------------------------------------------------------------------------
def test_X12_x4_registered_with_requires_s4_and_no_gates():
    assert "X4" in STAGE_REGISTRY
    stage = STAGE_REGISTRY["X4"]
    assert stage.stage_id == "X4"
    assert stage.requires == ("S4",)
    assert stage.gates == ()
