import pytest as _pytest
pytestmark = _pytest.mark.contracts

"""Hand-built small valid instances of every artifact class (independent of the implementation)."""
import numpy as np
import pytest

from topo_pilot import contracts as C
from topo_pilot.contracts import testing as T

CONSUMER = "experiment"  # allowed to read and write every artifact type per DATA_SCHEMAS section 7


def _emission():
    _, E, pi = T.tiny_hmm()
    return C.EmissionSpec(
        E=E, symbol_perm=np.arange(3, dtype=np.int32), mode="overlap", sigma=0.5,
        centers=np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]), center_strategy="hand",
        state_perm=None,
        diagnostics={"H_W_given_Z": 0.9, "H_W": 1.09, "p_w": (pi @ E).tolist(),
                     "coverage_radius": 1.5, "row_entropy_quantiles": [0.5, 0.8, 1.0],
                     "factorizes": False})


def make_history_index(sequence_id=(0, 1, 2, 3), end=(32, 32, 32, 32), panel=(1, 1, 2, 2),
                       panel_size=2, n_panels=2):
    sid = np.array(sequence_id, dtype=np.int64)
    end = np.array(end, dtype=np.int64)
    th = np.array([C.tokens_hash(np.arange(int(e)) + int(s)) for s, e in zip(sid, end)],
                  dtype="<U16")
    hid = np.array([C.make_history_id("ds", int(s), int(e), h) for s, e, h in zip(sid, end, th)],
                   dtype="<U16")
    return C.HistoryIndex(dataset_id="ds", history_id=hid, sequence_id=sid, end=end,
                          panel=np.array(panel, dtype=np.int64), tokens_hash=th,
                          panel_size=panel_size, n_panels=n_panels)


def _dist(m=3):
    D = np.abs(np.arange(m)[:, None] - np.arange(m)[None, :]).astype(np.float64)
    return D


def _oracle():
    hid = np.array(["a" * 16, "b" * 16], dtype="<U16")
    b = np.array([[0.25, 0.25, 0.25, 0.25], [0.5, 0.5, 0.0, 0.0]])
    q = np.array([[0.5, 0.25, 0.25], [0.2, 0.3, 0.5]])
    F2 = np.full((2, 3, 3), 1 / 9, dtype=np.float32)
    return C.OracleOutputs(
        history_id=hid, b32=b, b1=b.copy(), q=q, q_last=q.copy(),
        belief_entropy=np.array([1.3, 0.7]), log_evidence=np.array([-20.0, -21.5]),
        F2=F2, ce_oracle_all_positions=np.ones((4, 33), dtype=np.float32))


BUILDERS = {
    "WorldSpec": lambda: T.tiny_world_spec("cylinder", 3),
    "TransitionSpec": lambda: C.TransitionSpec(T=T.tiny_hmm()[0], pi=T.tiny_hmm()[2],
                                               p_stay=0.5, d_max=1),
    "EmissionSpec": _emission,
    "ObservationSet": lambda: T.tiny_observations(8, 0),
    "EvalSidecar": lambda: C.EvalSidecar(
        split="test", N=4, sequence_id=np.arange(5, dtype=np.int64),
        z=(np.arange(5 * 33).reshape(5, 33) % 4).astype(np.int16)),
    "HistoryIndex": make_history_index,
    "OracleOutputs": _oracle,
    "ProcessDiagnostics": lambda: C.ProcessDiagnostics(
        G_C=0.12, mean_H_b1=0.9, O_singular_values=((1.0, 0.5), (0.9,)),
        sigma_table=({"sigma": 0.5, "H": 1.2},), sigma=0.5, world_family="cylinder"),
    "BaselineOutputs": lambda: C.BaselineOutputs(
        ngram_order=2, smoothing="add-k", history_id=np.array(["a" * 16, "b" * 16], dtype="<U16"),
        probs=np.array([[0.5, 0.25, 0.25], [0.1, 0.2, 0.7]]), extra_info={"k": 0.5}),
    "Checkpoint": lambda: C.Checkpoint(run_id="r1", step=10, observation_id="o" * 16,
                                       state=b"\x00\x01opaque-blob\xff", model_config={"d": 128},
                                       train_config={"lr": 0.001}, has_optimizer_state=True),
    "ActivationSet": lambda: C.ActivationSet(
        hooks=("resid_0", "resid_1"), source="model",
        history_id=np.array(["a" * 16, "b" * 16], dtype="<U16"),
        A=np.arange(2 * 2 * 4, dtype=np.float32).reshape(2, 2, 4) / 7,
        logits=np.arange(6, dtype=np.float32).reshape(2, 3), checkpoint_id="c" * 16),
    "DistanceArtifact": lambda: C.DistanceArtifact(
        metric_id="euclid", scale_s=2.0, point_ids=np.array(["p0", "p1", "p2"], dtype="<U8"),
        D=_dist(3), dedup_map=np.array([0, 1, 2, 2], dtype=np.int64), pca_ref=None),
    "Diagrams": lambda: C.Diagrams(
        coeff_p=2, maxdim=1, threshold=3.0, library_version="hand",
        rows=np.array([[0, 0.0, np.inf, 1], [1, 0.1, 0.5, 0]], dtype=np.float64)),
    "MetricRecords": lambda: C.MetricRecords(rows=(
        C.MetricRow(run_id="r", space="A", metric_id="m1", value=0.25, replicate=1, world="cyl",
                    panel=2, hook="resid_0", units="nats", parent_ids=("x" * 16,)),
        C.MetricRow(run_id="r", space="A", metric_id="m2", value=None, status="collapsed"))),
    "GateReport": lambda: C.GateReport(
        stage="s", gate_id="g", verdict="pass",
        checks=(C.GateCheck("c1", True, 0.5, 1.0), C.GateCheck("c2", True))),
    "RunManifest": lambda: C.RunManifest(
        run_key="k", executor="local", config_hash="h" * 8, config={"a": 1},
        dag={"a" * 16: ("b" * 16,)}, seed_bundle={"init": 7}, stage_status={"world": "ok"},
        hardware={"cpu": "x"}, wall_time_s=1.5, peak_mem_mb=100.0,
        failures=({"code": "X"},), waivers=()),
}


@pytest.fixture
def builders():
    return BUILDERS


@pytest.fixture
def fs_store(tmp_path):
    root = tmp_path / "store"
    return C.ArtifactStore(C.LocalFSBackend(root)), root


@pytest.fixture
def make_hist():
    return make_history_index
