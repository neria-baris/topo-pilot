"""Part (c) circular correspondence: agreement of circular coordinates with a latent angle.

The only analysis code (with boundary extensions) that reads ``EvalSidecar``; every value is
labelled ``privileged_eval`` in its MetricRow ``space``.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.spatial.distance import cdist

from topo_pilot.contracts import (
    ArtifactStore,
    ErrorCode,
    EvalSidecar,
    MetricRow,
    StageFailure,
    WorldSpec,
)
from topo_pilot.topology import CircularCoordinates

from .spaces import SpaceBuilder

_COMPONENT = "analysis.CircularCorrespondence"
_SPACE = "privileged_eval:circular"


def _fail(code: ErrorCode, check: str, detail: str, aid: str | None = None) -> StageFailure:
    return StageFailure(code, _COMPONENT, check, detail, aid)


def circular_agreement(phi: ArrayLike, theta: ArrayLike) -> float:
    """Rotation- and reflection-invariant agreement of two angle vectors.

    Math
    ----
    ``A = max(|mean_i e^{i(phi_i - theta_i)}|, |mean_i e^{i(phi_i + theta_i)}|)``. A rotation
    ``phi -> phi + c`` multiplies both resultants by ``e^{ic}``, and a reflection
    ``phi -> -phi`` swaps them up to conjugation, so their moduli and hence ``A`` are
    unchanged. ``A(theta, theta) = 1``.

    Shapes
    ------
    ``phi, theta [M]`` -> float in ``[0, 1]``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (shapes differ, not 1-D, or M = 0), ``NUMERICAL_FAILURE``
        (non-finite).
    """
    p = np.asarray(phi, dtype=np.float64)
    t = np.asarray(theta, dtype=np.float64)
    if p.ndim != 1 or p.shape != t.shape or p.size == 0:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "shapes",
                    f"phi {p.shape} and theta {t.shape} must be equal non-empty 1-D")
    if not (np.all(np.isfinite(p)) and np.all(np.isfinite(t))):
        raise _fail(ErrorCode.NUMERICAL_FAILURE, "finite", "angles are not finite")
    a = abs(np.mean(np.exp(1j * (p - t))))
    b = abs(np.mean(np.exp(1j * (p + t))))
    return float(min(1.0, max(a, b)))


def _axis_coords(coords: NDArray, axis: int, period: float) -> NDArray[np.float64]:
    c = np.asarray(coords, dtype=np.float64)
    if c.ndim != 2 or not 0 <= axis < c.shape[1]:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "axis", f"axis {axis} invalid for {c.shape}")
    if not period > 0:
        raise _fail(ErrorCode.INVALID_CONFIG, "period", f"period={period} must be > 0")
    return c[:, axis]


def lattice_angle(coords: NDArray, states: ArrayLike, axis: int,
                  period: float) -> NDArray[np.float64]:
    """Angle of each state along one lattice axis.

    Math
    ----
    ``theta_i = 2 pi * coords[states_i, axis] / period``.

    Shapes
    ------
    ``coords [N, D]``, ``states [M]`` ints -> ``[M]``.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (state or axis out of range), ``INVALID_CONFIG`` (period <= 0).
    """
    col = _axis_coords(coords, axis, period)
    s = np.asarray(states)
    if s.size and (s.min() < 0 or s.max() >= col.shape[0]):
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "state_range", "state outside 0..N-1")
    return 2.0 * np.pi * col[s.astype(np.int64)] / period


def belief_angle(b: NDArray, coords: NDArray, axis: int, period: float) -> NDArray[np.float64]:
    """Circular mean of each belief along one lattice axis.

    Math
    ----
    ``theta_hat_i = arg sum_z b_{iz} exp(2 pi i coords[z, axis] / period)``; a zero resultant
    gives 0.

    Shapes
    ------
    ``b [M, N]`` -> ``[M]`` in ``(-pi, pi]``.

    Invariants
    ----------
    A delta belief at z gives ``lattice_angle`` of z modulo 2 pi.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (b width != N, axis out of range), ``INVALID_CONFIG`` (period <= 0).
    """
    col = _axis_coords(coords, axis, period)
    B = np.asarray(b, dtype=np.float64)
    if B.ndim != 2 or B.shape[1] != col.shape[0]:
        raise _fail(ErrorCode.ALIGNMENT_ERROR, "belief_width",
                    f"b shape {B.shape} does not match N={col.shape[0]}")
    resultant = B @ np.exp(2j * np.pi * col / period)
    theta = np.angle(resultant)
    theta[np.abs(resultant) < 1e-12] = 0.0
    return theta


class CircularCorrespondence:
    """Do the circular coordinates of an activation cloud track a latent angle?

    Math
    ----
    ``phi = CircularCoordinates(coeff_p).fit_transform(D)``, ``A = circular_agreement(phi,
    theta)``; permutation null ``A_k = circular_agreement(phi, theta[perm_k])``,
    ``k = 1..n_perm``; ``p = (1 + #{A_k >= A}) / (1 + n_perm)``.

    Shapes
    ------
    ``D [M, M]``, ``theta [M]``.

    Invariants
    ----------
    ``A`` does not depend on the arbitrary origin or orientation of ``phi``. With no finite H1
    bar the result is a status (``no_h1_class``), not an exception.

    Raises
    ------
    StageFailure
        ``compare``: ``ALIGNMENT_ERROR``, ``INVALID_CONFIG``, topology codes for a bad D.
        ``run``: ``SAMPLE_ID_MISMATCH`` (sequence missing from the sidecar, oracle ids differ).
    """

    def __init__(self, coeff_p: int = 47, n_perm: int = 1000):
        self.coeff_p = coeff_p
        self.n_perm = n_perm

    def compare(self, D: NDArray, theta: NDArray, rng: np.random.Generator) -> dict:
        """Circular coordinates of ``D`` against ``theta`` with a permutation null."""
        D = np.asarray(D, dtype=np.float64)
        th = np.asarray(theta, dtype=np.float64)
        if th.ndim != 1 or D.ndim != 2 or th.shape[0] != D.shape[0]:
            raise _fail(ErrorCode.ALIGNMENT_ERROR, "theta_length",
                        f"theta {th.shape} does not match D {D.shape}")
        if self.n_perm < 1:
            raise _fail(ErrorCode.INVALID_CONFIG, "n_perm", f"n_perm={self.n_perm} < 1")
        try:
            phi = CircularCoordinates(self.coeff_p).fit_transform(D)
        except StageFailure as exc:
            if exc.check != "no_h1_class":
                raise
            return {"status": "no_h1_class", "agreement": None, "null_q95": None,
                    "p_value": None, "phi": None}
        agreement = circular_agreement(phi, th)
        null = np.array([circular_agreement(phi, th[rng.permutation(th.shape[0])])
                         for _ in range(self.n_perm)])
        return {"status": "ok", "agreement": agreement,
                "null_q95": float(np.quantile(null, 0.95)),
                "p_value": float((1 + np.sum(null >= agreement)) / (1 + self.n_perm)),
                "phi": phi}

    def _states(self, store: ArtifactStore, builder: SpaceBuilder, activation_set_id: str,
                sidecar_id: str, ids: list[str], panel: int) -> NDArray[np.int64]:
        index = builder._index_of(activation_set_id)
        mask = np.asarray(index.panel) == panel
        pids = [str(h) for h in np.asarray(index.history_id)[mask]]
        if pids != ids:
            raise _fail(ErrorCode.SAMPLE_ID_MISMATCH, "panel_ids",
                        "activation ids differ from the HistoryIndex panel", activation_set_id)
        side = store.load(EvalSidecar, sidecar_id, consumer="analysis")
        row_of = {int(s): i for i, s in enumerate(side.sequence_id)}
        seqs = np.asarray(index.sequence_id)[mask]
        ends = np.asarray(index.end)[mask]
        if any(int(s) not in row_of for s in seqs):
            raise _fail(ErrorCode.SAMPLE_ID_MISMATCH, "sidecar_rows",
                        "a history's sequence is absent from the EvalSidecar", sidecar_id)
        rows = np.array([row_of[int(s)] for s in seqs], dtype=np.int64)
        return np.asarray(side.z)[rows, np.asarray(ends, dtype=np.int64) - 1].astype(np.int64)

    def run(self, store: ArtifactStore, activation_set_id: str, sidecar_id: str, world_id: str,
            oracle_id: str, hook: str, panel: int, rng: np.random.Generator,
            axis: int = 0, control_axis: int = 1, **row_fields) -> list[MetricRow]:
        """Compare the circular coordinates of a panel cloud with latent angles (privileged_eval).

        Metrics: ``agreement_x`` (+ ``_null_q95``, ``_p``), ``agreement_control`` (control axis,
        same phi), ``agreement_oracle_x`` (belief-mean angle vs lattice angle, no PH).
        """
        builder = SpaceBuilder(store)
        cloud = builder.activations(activation_set_id, hook, panel)
        b32 = builder.beliefs(oracle_id, "b32", panel)
        if list(cloud.ids) != list(b32.ids):
            raise _fail(ErrorCode.SAMPLE_ID_MISMATCH, "oracle_ids",
                        "oracle b32 ids differ from the activation ids", oracle_id)
        coords = np.asarray(store.load(WorldSpec, world_id, consumer="analysis").coords,
                            dtype=np.float64)
        z = self._states(store, builder, activation_set_id, sidecar_id, list(cloud.ids), panel)
        period = float(coords[:, axis].max() + 1)
        period_c = float(coords[:, control_axis].max() + 1)
        theta = lattice_angle(coords, z, axis, period)
        theta_c = lattice_angle(coords, z, control_axis, period_c)
        theta_hat = belief_angle(b32.X, coords, axis, period)
        res = self.compare(cdist(cloud.X, cloud.X), theta, rng)
        phi = res["phi"]
        values = {
            "agreement_x": res["agreement"],
            "agreement_x_null_q95": res["null_q95"],
            "agreement_x_p": res["p_value"],
            "agreement_control": None if phi is None else circular_agreement(phi, theta_c),
            "agreement_oracle_x": circular_agreement(theta_hat, theta),
        }
        return [self._row(activation_set_id, hook, panel, name, val, row_fields)
                for name, val in values.items()]

    @staticmethod
    def _row(run_id: str, hook: str, panel: int, name: str, value: float | None,
             row_fields: dict) -> MetricRow:
        missing = value is None
        return MetricRow(run_id=run_id, space=_SPACE, metric_id=name, value=value,
                         status="inconclusive" if missing else "ok",
                         uncertainty_kind="no_h1_class" if missing else None,
                         hook=hook, panel=panel, **row_fields)
