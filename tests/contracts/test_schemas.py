import dataclasses

import numpy as np
import pytest

from topo_pilot import contracts as C
from topo_pilot.contracts import ErrorCode, StageFailure

pytestmark = pytest.mark.contracts


def _fails(art, code):
    with pytest.raises(StageFailure) as ei:
        art.validate()
    assert ei.value.code == code, str(ei.value)


def test_C13_transition_row_sum(builders):
    ts = builders["TransitionSpec"]()
    ts.validate()
    T_bad = ts.T.copy()
    T_bad[0, 0] += 0.01  # row 0 sums to 1.01 (and T stays "almost" symmetric: irrelevant)
    _fails(dataclasses.replace(ts, T=T_bad), ErrorCode.NONSTOCHASTIC)
    _fails(dataclasses.replace(ts, T=ts.T * 0.5), ErrorCode.NONSTOCHASTIC)
    T_neg = ts.T.copy()
    T_neg[0, 0], T_neg[0, 1] = -0.25, 1.0  # row sums still 1 but negative entry
    _fails(dataclasses.replace(ts, T=T_neg), ErrorCode.NONSTOCHASTIC)


def test_C13_transition_asymmetric_and_stationarity(builders):
    ts = builders["TransitionSpec"]()
    asym = np.array([[0.5, 0.5, 0.0, 0.0], [0.0, 0.5, 0.5, 0.0],
                     [0.0, 0.0, 0.5, 0.5], [0.5, 0.0, 0.0, 0.5]])
    _fails(dataclasses.replace(ts, T=asym), ErrorCode.NONSTOCHASTIC)
    _fails(dataclasses.replace(ts, pi=np.array([0.4, 0.2, 0.2, 0.2])),
           ErrorCode.STATIONARITY_FAILURE)


def test_C13_emission_dead_symbol(builders):
    em = builders["EmissionSpec"]()
    em.validate()
    E = np.array([[0.5, 0.5, 0.0], [0.25, 0.75, 0.0], [0.5, 0.5, 0.0], [0.1, 0.9, 0.0]])
    diag = dict(em.diagnostics, p_w=(0.25 * E.sum(axis=0)).tolist())
    assert diag["p_w"][2] == 0.0
    _fails(dataclasses.replace(em, E=E, diagnostics=diag), ErrorCode.INVALID_SIGMA)


def test_C13_emission_other_violations(builders):
    em = builders["EmissionSpec"]()
    _fails(dataclasses.replace(em, E=em.E * 0.9), ErrorCode.NONSTOCHASTIC)
    _fails(dataclasses.replace(em, sigma=0.0), ErrorCode.INVALID_SIGMA)
    _fails(dataclasses.replace(em, mode="nonsense"), ErrorCode.INVALID_CONFIG)
    _fails(dataclasses.replace(em, symbol_perm=np.array([0, 0, 1], dtype=np.int32)),
           ErrorCode.INVALID_CONFIG)
    _fails(dataclasses.replace(em, mode="identical"), ErrorCode.INVALID_CONFIG)  # rows differ
    _fails(dataclasses.replace(em, mode="unique"), ErrorCode.INVALID_CONFIG)  # not a permutation


def test_C13_history_index_overlapping_panels(make_hist):
    make_hist().validate()
    # trajectory 0 appears in panel 1 (end 32) and panel 2 (end 31): unique history ids,
    # shared trajectory
    overlapping = make_hist(sequence_id=(0, 1, 0, 3), end=(32, 32, 31, 31))
    _fails(overlapping, ErrorCode.SPLIT_OVERLAP)


def test_C13_history_index_other_violations(make_hist):
    good = make_hist()
    _fails(dataclasses.replace(good, history_id=good.history_id[::-1].copy()),
           ErrorCode.SAMPLE_ID_MISMATCH)
    _fails(make_hist(panel=(1, 1, 1, 2)), ErrorCode.JOIN_CARDINALITY)
    _fails(dataclasses.replace(good, panel_size=3), ErrorCode.JOIN_CARDINALITY)
    _fails(dataclasses.replace(good, end=good.end[:3]), ErrorCode.ALIGNMENT_ERROR)


def test_C13_world_spec(builders):
    w = builders["WorldSpec"]()
    w.validate()
    _fails(dataclasses.replace(w, betti_computed={2: (1, 0, 0), 3: (1, 0, 0)}),
           ErrorCode.BETTI_MISMATCH)
    bad = w.dist.copy()
    bad[0, 1] = bad[1, 0] = 50.0  # breaks the triangle inequality
    _fails(dataclasses.replace(w, dist=bad), ErrorCode.NON_METRIC)
    asym = w.dist.copy()
    asym[0, 1] += 1.0
    _fails(dataclasses.replace(w, dist=asym), ErrorCode.NON_METRIC)
    _fails(dataclasses.replace(w, edges=w.edges[:-1]), ErrorCode.INVALID_GLUE)
    _fails(dataclasses.replace(w, edges=w.edges[:, ::-1].copy()), ErrorCode.INVALID_GLUE)


def test_C13_data_artifacts(builders):
    obs = builders["ObservationSet"]()
    _fails(dataclasses.replace(obs, V=2), ErrorCode.ALIGNMENT_ERROR)  # tokens up to 2 >= V
    _fails(dataclasses.replace(obs, tokens=obs.tokens[:, :32]), ErrorCode.ALIGNMENT_ERROR)
    _fails(dataclasses.replace(obs, sequence_id=np.zeros(8, dtype=np.int64)),
           ErrorCode.SAMPLE_ID_MISMATCH)
    _fails(dataclasses.replace(obs, split="val"), ErrorCode.INVALID_CONFIG)
    es = builders["EvalSidecar"]()
    _fails(dataclasses.replace(es, split="train"), ErrorCode.INVALID_CONFIG)
    _fails(dataclasses.replace(es, N=2), ErrorCode.ALIGNMENT_ERROR)  # states up to 3


def test_C13_misc_artifacts(builders):
    b = builders
    _fails(dataclasses.replace(b["GateReport"](), verdict="fail"), ErrorCode.INVALID_CONFIG)
    _fails(dataclasses.replace(b["GateReport"](), verdict="waived"), ErrorCode.INVALID_CONFIG)
    _fails(dataclasses.replace(b["Diagrams"](), coeff_p=4), ErrorCode.INVALID_CONFIG)
    _fails(dataclasses.replace(b["Checkpoint"](), state=b""), ErrorCode.INVALID_CONFIG)
    _fails(dataclasses.replace(b["Checkpoint"](), step=-1), ErrorCode.INVALID_CONFIG)
    _fails(dataclasses.replace(b["RunManifest"](), executor=""), ErrorCode.INVALID_CONFIG)
    _fails(dataclasses.replace(b["ProcessDiagnostics"](), G_C=float("nan")),
           ErrorCode.NUMERICAL_FAILURE)
    bad_q = b["BaselineOutputs"]()
    _fails(dataclasses.replace(bad_q, probs=bad_q.probs * 2), ErrorCode.NUMERICAL_FAILURE)
    act = b["ActivationSet"]()
    _fails(dataclasses.replace(act, hooks=("resid_0", "resid_0")), ErrorCode.UNKNOWN_HOOK)
    _fails(dataclasses.replace(act, hooks=("resid_0",)), ErrorCode.ALIGNMENT_ERROR)
    A = act.A.copy()
    A[0, 0, 0] = np.nan
    _fails(dataclasses.replace(act, A=A), ErrorCode.NUMERICAL_FAILURE)
    dist = b["DistanceArtifact"]()
    D = dist.D.copy()
    D[0, 1] += 1.0
    _fails(dataclasses.replace(dist, D=D), ErrorCode.NON_METRIC)
    orc = b["OracleOutputs"]()
    q = orc.q.copy()
    q[0, 0] += 0.5
    _fails(dataclasses.replace(orc, q=q), ErrorCode.NUMERICAL_FAILURE)
    mr = C.MetricRecords(rows=(C.MetricRow(run_id="r", space="s", metric_id="m", value=None),))
    _fails(mr, ErrorCode.INVALID_CONFIG)  # status ok without a value


def test_C13_stagefailure_basics():
    e = StageFailure(ErrorCode.LEAKAGE, "comp", "chk", "detail", artifact_id="x")
    assert e.code == ErrorCode.LEAKAGE and e.artifact_id == "x" and e.recoverable is False
    assert isinstance(e, Exception)
    assert "LEAKAGE" in str(e)
    assert len(list(ErrorCode)) == 26
    assert {s.value for s in C.Status} == {"ok", "collapsed", "censored", "nonseparable",
                                           "inconclusive", "not_run", "approximate"}
