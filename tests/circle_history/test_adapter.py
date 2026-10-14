"""Independent tests (author B) for adapter.py: TEST_PLAN item B7 (spec v2.2).

Written from API.md and the public topo_pilot.contracts API only; no production code was read.
Synthetic ObservationSet / HistoryIndex / Checkpoint / ActivationSet artifacts are saved with
store.save into contracts.testing.memory_store(); sizes are tiny (panel_size 4, n_panels 3,
3 models, activation width 3). Expected rows are derived here from the artifacts we built.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import numpy as np
import pytest
from topo_pilot.contracts import (
    ActivationSet,
    ArtifactStore,
    Checkpoint,
    HistoryIndex,
    ObservationSet,
    make_history_id,
    tokens_hash,
)
from topo_pilot.contracts.testing import memory_store

REPO_ROOT = Path(__file__).resolve().parents[2]
for _sub in ("tools/x4_circle_history", "tools/x4_oracle_profile", "tests/oracle_profile"):
    if str(REPO_ROOT / _sub) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT / _sub))

import adapter  # noqa: E402
import errors  # noqa: E402

pytestmark = pytest.mark.analysis

MODELS = (1729, 2718, 3141)
PERMS = {1729: np.array([0, 1, 2]), 2718: np.array([2, 0, 1]), 3141: np.array([1, 2, 0])}
PANEL_SIZE, N_PANELS, WIDTH = 4, 3, 3
N_ROWS = PANEL_SIZE * N_PANELS
HOOKS = ("resid_post_2", "resid_post_3")
SEQ_IDS = np.array([907, 15, 333, 48, 121, 760, 5, 412, 89, 650, 271, 1003], dtype=np.int64)


def _canonical() -> np.ndarray:
    rows = np.zeros((N_ROWS, 33), dtype=np.uint8)
    for r in range(N_ROWS):
        rows[r, :3] = (r // 9, (r // 3) % 3, r % 3)     # base-3 digits: all rows distinct
        rows[r, 3:32] = [(r + t * t) % 3 for t in range(3, 32)]
        rows[r, 32] = (r + 1) % 3                        # w33: must never be returned
    return rows


CANONICAL = _canonical()
DEFAULTS = {"split": "test", "end": 32, "hooks": HOOKS, "swap": False, "bad_hash": False,
            "drop_hi_parent": False, "ckpt_field": None, "source": "model",
            "layout": (PANEL_SIZE, N_PANELS)}


def _save_model(store: ArtifactStore, m: int, opt: dict) -> tuple[dict, dict]:
    order = np.roll(np.arange(N_ROWS), m % 5)            # model-specific ObservationSet row order
    named = PERMS[m][CANONICAL[order]].astype(np.uint8)
    seq = SEQ_IDS[order]
    obs = ObservationSet(split=opt["split"], V=3, sequence_id=seq, tokens=named)
    obs_id = store.save(obs, config={"obs": m}, parents=[], seed_map={}, consumer="dataset")
    ckpt = Checkpoint(run_id=f"run-{m}", step=5000, observation_id=f"train-{m}",
                      state=f"opaque-{m}".encode())
    ckpt_id = store.save(ckpt, config={"ckpt": m}, parents=[], seed_map={}, consumer="learner")
    size, n_pan = opt["layout"]
    panel = np.array([1 + int(order[i]) % n_pan for i in range(N_ROWS)], dtype=np.int64)
    hashes = [tokens_hash(named[i, :32]) for i in range(N_ROWS)]
    if opt["bad_hash"]:
        wrong = named[0, :32].copy()
        wrong[5] = (wrong[5] + 1) % 3
        hashes[0] = tokens_hash(wrong)
    hid = [make_history_id(obs_id, int(seq[i]), opt["end"], hashes[i]) for i in range(N_ROWS)]
    # HistoryIndex row order: by panel, then DESCENDING history_id (never the landmark order)
    rows = sorted(sorted(range(N_ROWS), key=lambda i: hid[i], reverse=True),
                  key=lambda i: panel[i])
    hi = HistoryIndex(dataset_id=obs_id, history_id=np.array([hid[i] for i in rows]),
                      sequence_id=seq[rows], end=np.full(N_ROWS, opt["end"], dtype=np.int64),
                      panel=panel[rows], tokens_hash=np.array([hashes[i] for i in rows]),
                      panel_size=size, n_panels=n_pan)
    hi_id = store.save(hi, config={"hi": m}, parents=[obs_id], seed_map={}, consumer="dataset")
    act_hid = [hid[i] for i in rows]
    A = np.zeros((N_ROWS, len(opt["hooks"]), WIDTH), dtype=np.float32)
    for j, i in enumerate(rows):
        for h in range(len(opt["hooks"])):
            A[j, h] = [int(seq[i]) % 97 + 0.25 * h + 0.5 * c + 0.125 * (m % 7)
                       for c in range(WIDTH)]
    if opt["swap"]:
        act_hid[0], act_hid[1] = act_hid[1], act_hid[0]
        A[[0, 1]] = A[[1, 0]]
    act = ActivationSet(hooks=tuple(opt["hooks"]), source=opt["source"],
                        history_id=np.array(act_hid), A=A, logits=None,
                        checkpoint_id=opt["ckpt_field"] or ckpt_id)
    parents = [obs_id, ckpt_id] + ([] if opt["drop_hi_parent"] else [hi_id])
    act_id = store.save(act, config={"act": m}, parents=parents, seed_map={},
                        consumer="activations")
    ids = {"ObservationSet": obs_id, "HistoryIndex": hi_id, "ActivationSet": act_id,
           "checkpoint": ckpt_id}
    hook_idx = list(opt["hooks"]).index("resid_post_3") if "resid_post_3" in opt["hooks"] else 0
    facts = {
        "panel_hids": {p: sorted(hid[i] for i in range(N_ROWS) if panel[i] == p)
                       for p in range(1, n_pan + 1)},
        "seq_of_hid": {hid[i]: int(seq[i]) for i in range(N_ROWS)},
        "named_of_seq": {int(seq[i]): named[i] for i in range(N_ROWS)},
        "act_of_hid": {act_hid[j]: A[j, hook_idx].astype(np.float64) for j in range(N_ROWS)},
    }
    return ids, facts


def build(**bad) -> tuple[ArtifactStore, adapter.E4Manifest, dict]:
    """Store + manifest for three models; overrides in ``bad`` apply to model 1729 only."""
    foreign = bad.pop("foreign_obs", False)
    store = memory_store()
    per_model, truth = {}, {}
    for m in MODELS:
        opt = dict(DEFAULTS, **(bad if m == MODELS[0] else {}))
        per_model[m], truth[m] = _save_model(store, m, opt)
    if foreign:   # manifest names another model's ObservationSet for model 1729
        per_model[MODELS[0]] = dict(per_model[MODELS[0]],
                                    ObservationSet=per_model[MODELS[1]]["ObservationSet"])
    manifest = adapter.E4Manifest(per_model=per_model, hook="resid_post_3", end=32,
                                  panel_size=PANEL_SIZE, n_panels=N_PANELS)
    return store, manifest, truth


class CountingStore(ArtifactStore):
    """Shares the inner store's backend and policy and records every load call."""

    def __init__(self, inner: ArtifactStore) -> None:
        super().__init__(inner.backend, inner.policy)
        self.loads: list[tuple[str, str, str]] = []

    def load(self, cls, artifact_id, *, consumer):
        self.loads.append((cls.__name__, artifact_id, consumer))
        return super().load(cls, artifact_id, consumer=consumer)


@pytest.fixture(scope="module")
def valid():
    return build()


# ---- lineage ----------------------------------------------------------------------------------
def test_lineage_passes_for_every_model(valid) -> None:
    store, manifest, _ = valid
    ad = adapter.RestrictedE4Adapter(store, manifest, scoring_release=None)
    for m in MODELS:
        assert isinstance(ad.lineage(m), dict)


@pytest.mark.parametrize("bad", [
    {"drop_hi_parent": True},                        # ActivationSet parents lack HistoryIndex
    {"split": "dev"},                                 # ObservationSet split must be "test"
    {"end": 31},                                      # every end must be 32
    {"hooks": ("resid_post_2", "resid_post_4")},      # hook missing
    {"swap": True},                                   # ActivationSet history_id order differs
    {"bad_hash": True},                               # tokens_hash of one row is wrong
    {"ckpt_field": "00000000deadbeef"},               # checkpoint_id != manifest checkpoint
    {"source": "baseline:R0"},                        # source must be "model"
    {"layout": (6, 2)},                               # panel_size / n_panels differ
    {"foreign_obs": True},                            # HistoryIndex parent is another dataset
], ids=["parent", "split", "end", "hook", "order", "tokens_hash", "checkpoint", "source",
        "panel_layout", "dataset"])
def test_lineage_mismatch_raises_join_error(bad: dict) -> None:
    store, manifest, _ = build(**bad)
    with pytest.raises(errors.JoinError):
        adapter.RestrictedE4Adapter(store, manifest).lineage(MODELS[0])


# ---- panels -----------------------------------------------------------------------------------
def test_panels_rows_in_history_id_order_without_w33(valid) -> None:
    store, manifest, truth = valid
    spy = CountingStore(store)
    ad = adapter.RestrictedE4Adapter(spy, manifest)
    for m in MODELS:
        out = ad.panels(m)
        assert sorted(out) == [1, 2]
        for p in (1, 2):
            rec, facts = out[p], truth[m]
            assert {"history_id", "sequence_id", "named32", "activation"} <= set(rec)
            hids = facts["panel_hids"][p]
            assert np.asarray(rec["history_id"]).tolist() == hids     # ascending history_id
            seq = np.asarray(rec["sequence_id"]).tolist()
            assert seq == [facts["seq_of_hid"][h] for h in hids]
            named = np.asarray(rec["named32"])
            assert named.shape == (PANEL_SIZE, 32)
            assert np.array_equal(named, np.stack([facts["named_of_seq"][s][:32] for s in seq]))
            act = np.asarray(rec["activation"])
            assert act.dtype == np.float64 and act.shape == (PANEL_SIZE, WIDTH)
            assert np.array_equal(act, np.stack([facts["act_of_hid"][h] for h in hids]))
            for value in rec.values():
                if isinstance(value, np.ndarray) and value.ndim == 2:
                    assert value.shape[1] != 33
    assert spy.loads and all(consumer == "analysis" for _, _, consumer in spy.loads)
    assert not any(name == "Checkpoint" for name, _, _ in spy.loads)
    assert sorted(ad.panels(MODELS[1], (1,))) == [1]


@pytest.mark.parametrize("request_panels", [(3,), (1, 3), (2, 3, 1), (0,), (9,)])
def test_panel_outside_calibration_validation_denied_before_any_load(
        valid, request_panels) -> None:
    store, manifest, _ = valid
    spy = CountingStore(store)
    ad = adapter.RestrictedE4Adapter(spy, manifest)
    before = len(spy.loads)
    with pytest.raises(errors.AccessDenied):
        ad.panels(MODELS[0], request_panels)
    assert len(spy.loads) == before


# ---- B10 (spec v2.3): only an errors.ScoringAuthority unlocks panels outside {1, 2} -----------
def _auth(**changes) -> object:
    fields = {"owner_record_path": "x", "owner_record_sha256": "0" * 64, "scope": ("scoring",),
              "release_job_id": "0099"}
    return errors.ScoringAuthority(**dict(fields, **changes))


BAD_RELEASES = {"None": lambda: None, "False": lambda: False, "True": lambda: True,
                "empty_dict": dict, "str": lambda: "token", "object": object,
                "scope": lambda: _auth(scope=("feasibility",)),
                "short_sha": lambda: _auth(owner_record_sha256="0" * 63)}


@pytest.mark.parametrize("kind", sorted(BAD_RELEASES))
def test_invalid_scoring_release_denies_panel_3_before_any_load(valid, kind: str) -> None:
    try:   # Interpretation: an authority that cannot even be constructed is also fail-closed.
        release = BAD_RELEASES[kind]()
    except (errors.AccessDenied, ValueError, TypeError):
        return
    store, manifest, _ = valid
    spy = CountingStore(store)
    ad = adapter.RestrictedE4Adapter(spy, manifest, scoring_release=release)
    before = len(spy.loads)
    with pytest.raises(errors.AccessDenied):
        ad.panels(MODELS[0], (3,))
    assert len(spy.loads) == before


def test_scoring_authority_unlocks_panel_3(valid) -> None:
    store, manifest, truth = valid
    spy = CountingStore(store)
    ad = adapter.RestrictedE4Adapter(spy, manifest, scoring_release=_auth())
    for m in MODELS:
        out = ad.panels(m, (3,))
        assert sorted(out) == [3]
        hids = truth[m]["panel_hids"][3]
        assert np.asarray(out[3]["history_id"]).tolist() == hids
        named = np.asarray(out[3]["named32"])
        assert named.shape == (PANEL_SIZE, 32)
        seq = np.asarray(out[3]["sequence_id"]).tolist()
        assert np.array_equal(named, np.stack([truth[m]["named_of_seq"][s][:32] for s in seq]))
        act = np.stack([truth[m]["act_of_hid"][h] for h in hids])
        assert np.array_equal(np.asarray(out[3]["activation"]), act)
    assert spy.loads and all(consumer == "analysis" for _, _, consumer in spy.loads)


# ---- identity_report ----------------------------------------------------------------------------
def _leaves(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            yield key
            yield from _leaves(value)
    elif isinstance(obj, (list, tuple)):
        numbers = [v for v in obj if isinstance(v, (int, float, np.number))
                   and not isinstance(v, (bool, np.bool_))]
        assert len(numbers) < 8, "numeric sequence looks like a token/activation array"
        for value in obj:
            yield from _leaves(value)
    else:
        yield obj


def test_identity_report_returns_no_arrays(valid) -> None:
    store, manifest, _ = valid
    report = adapter.RestrictedE4Adapter(store, manifest).identity_report()  # panel 3 included
    assert isinstance(report, dict) and report
    for leaf in _leaves(report):
        assert not isinstance(leaf, (np.ndarray, bytes, bytearray, memoryview)), type(leaf)
        assert isinstance(leaf, (bool, int, float, str, type(None), np.bool_, np.integer,
                                 np.floating)), type(leaf)


def test_identity_report_runs_every_lineage_check() -> None:
    store, manifest, _ = build(bad_hash=True)
    with pytest.raises(errors.JoinError):
        adapter.RestrictedE4Adapter(store, manifest).identity_report()


# ---- cross_model_join ---------------------------------------------------------------------------
JOIN_SEQ = np.array([40, 7, 19, 3, 88, 25], dtype=np.int64)
JOIN_PANEL = np.array([1, 1, 1, 2, 2, 2], dtype=np.int64)
JOIN_CANON = np.array([[i // 3, i % 3] + [(i * t + 1) % 3 for t in range(30)] for i in range(6)],
                      dtype=np.int64)
JOIN_ROWS = {1729: [0, 1, 2, 3, 4, 5], 2718: [5, 3, 1, 0, 2, 4], 3141: [2, 4, 0, 5, 1, 3]}


def _join_input(edits: dict | None = None) -> dict:
    out = {}
    for m, rows in JOIN_ROWS.items():
        rec = {"sequence_id": JOIN_SEQ[rows].copy(), "canonical32": JOIN_CANON[rows].copy(),
               "panel": JOIN_PANEL[rows].copy()}
        if edits and m in edits:
            edits[m](rec)
        out[m] = rec
    return out


def test_cross_model_join_orders_by_sequence_id() -> None:
    per_model = _join_input()
    out = adapter.cross_model_join(per_model)
    assert np.asarray(out["sequence_id"]).tolist() == sorted(JOIN_SEQ.tolist())
    want_rows = None
    for m in MODELS:
        order = np.asarray(out["order"][m])
        assert np.array_equal(order, np.argsort(per_model[m]["sequence_id"]))
        assert per_model[m]["sequence_id"][order].tolist() == sorted(JOIN_SEQ.tolist())
        rows = per_model[m]["canonical32"][order]
        digests = [hashlib.sha256(bytes(int(v) for v in row)).hexdigest() for row in rows]
        want_rows = digests if want_rows is None else want_rows
        assert digests == want_rows


def _replace_seq(rec: dict) -> None:
    rec["sequence_id"][rec["sequence_id"] == 88] = 89


def _change_tokens(rec: dict) -> None:
    row = int(np.flatnonzero(rec["sequence_id"] == 19)[0])
    rec["canonical32"][row, 17] = (rec["canonical32"][row, 17] + 1) % 3


def _swap_panels(rec: dict) -> None:
    a = int(np.flatnonzero(rec["sequence_id"] == 3)[0])
    b = int(np.flatnonzero(rec["sequence_id"] == 19)[0])
    rec["panel"][a], rec["panel"][b] = rec["panel"][b], rec["panel"][a]


@pytest.mark.parametrize("edits", [{3141: _replace_seq}, {2718: _change_tokens},
                                   {2718: _swap_panels}],
                         ids=["sequence_set", "digest", "panel_sets"])
def test_cross_model_join_mismatch_raises_join_error(edits: dict) -> None:
    with pytest.raises(errors.JoinError):
        adapter.cross_model_join(_join_input(edits))
