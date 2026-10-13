"""Stage X4 inputs: plain arrays per run, resolved from the store (consumer "experiment").

Only stored artifacts are read: the all-panel ActivationSets at checkpoints 0 and final, the
weights of the same checkpoints (final LN gamma, beta and W_U, through ``learner.load_model``),
the oracle beliefs and futures, the panel tokens (w_32 and the R2/R3 baselines), the learning
gate of the run record and, when present, the S values of the primary hook from the source
analysis (PREREGISTRATION_X4: V0 is recomputed only if not stored). Nothing is trained or
extracted.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass

import numpy as np

from topo_pilot.analysis import SpaceBuilder, require_same_ids
from topo_pilot.contracts import (
    ActivationSet,
    ArtifactStore,
    Checkpoint,
    ErrorCode,
    HistoryIndex,
    MetricRecords,
    StageFailure,
    TransitionSpec,
)
from topo_pilot.learner import load_model

from .config import ResolvedConfig
from .s2 import child_of
from .s4_analysis import AnalysisJob

log = logging.getLogger(__name__)
CONS = "experiment"
CONDITION_OF = {"S4": "O", "S5": "P"}
Weights = tuple[np.ndarray, np.ndarray, np.ndarray]


@dataclass(frozen=True, eq=False)
class X4Panel:
    """One panel of one run at one checkpoint: ``Z [M, d]`` (resid_post_3), ``ln_out [M, d]``
    (ln_final_out), ``logits [M, V]``; rows follow ``ids`` (HistoryIndex order)."""

    ids: tuple[str, ...]
    Z: np.ndarray
    ln_out: np.ndarray
    logits: np.ndarray


@dataclass(frozen=True, eq=False)
class X4Run:
    """Everything X4 needs from one training run (see experiment/SPEC.md, Stage X4).

    ``panels[(step, panel)]``; ``weights[step] = (gamma [d], beta [d], W_U [V, d])``;
    ``oracle[panel]`` holds ``b32, b1, q, last_symbol, R2, R3`` in the panel's id order (None for
    N, where b is constant); ``stored_S_V0[(step, panel)] = (S, status)``; ``parents`` lists
    every artifact the data came from.
    """

    world: str
    condition: str
    seed: int
    panels: Mapping[tuple[int, int], X4Panel]
    weights: Mapping[int, Weights]
    oracle: Mapping[int, Mapping[str, np.ndarray]] | None
    learning_gate: bool | None
    stored_S_V0: Mapping[tuple[int, int], tuple[float, str]]
    parents: tuple[str, ...]


def _fail(check: str, detail: str, aid: str | None = None) -> StageFailure:
    return StageFailure(ErrorCode.MISSING_PARENT, "experiment.X4", check, detail, aid)


class StoreResolver:
    """``resolver(source_stage) -> (runs, missing run keys)`` over the stored runs of a stage."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore):
        self.cfg, self.store = cfg, store
        self.hook = cfg.base["model"]["primary_hook"]
        self.final = int(cfg.base["training"]["primary_checkpoint"])

    def __call__(self, source: str) -> tuple[list[X4Run], list[tuple[str, str, int]]]:
        if source not in CONDITION_OF:
            raise StageFailure(ErrorCode.INVALID_CONFIG, "experiment.X4", "sources",
                               f"unknown X4 source {source!r} (S4 or S5)")
        aj = AnalysisJob(source, self.cfg, self.store)
        stored, analysis_id = self._stored_S(source)
        runs, missing = [], []
        for job in self.cfg.stage(source).get("runs_ordered", []):
            key = (job["world"], job["condition"], int(job["seed"]))
            try:
                runs.append(self._run(aj, key, source, stored, analysis_id))
            except KeyError as exc:  # run not done: reported as not_run, never invented
                log.warning("X4: run %s missing (%s)", key, exc)
                missing.append(key)
        return runs, missing

    # ---- one run --------------------------------------------------------------------------
    def _run(self, aj: AnalysisJob, key: tuple[str, str, int], source: str,
             stored: dict, analysis_id: str | None) -> X4Run:
        world, cond, seed = key
        acts = {step: aj.acts(world, cond, seed, step) for step in (0, self.final)}
        family = "cylinder" if world == "any" else world  # N data is the cylinder's (D-029)
        inputs = aj.inputs(family, cond, seed)
        parents = set(acts.values()) | {inputs["history_index"]}
        panels, weights = {}, {}
        for step, aid in acts.items():
            act = self.store.load(ActivationSet, aid, consumer=CONS)
            weights[step], cid = self._weights(act, step, aid)
            parents.add(cid)
            panels.update({(step, p): pan for p, pan in self._panels(act, aid).items()})
        oracle = None
        if cond != "N":
            oracle = self._oracle(aj, inputs, acts[self.final], panels)
            parents |= {inputs[k] for k in ("oracle", "obs_test", "emission")}
            parents.add(child_of(self.store, TransitionSpec, inputs["world"]))
        gate, run_mid = self._learning_gate(source, key)
        if run_mid:
            parents.add(run_mid)
        s0 = {k[3:]: v for k, v in stored.items() if k[:3] == key}
        if s0 and analysis_id:
            parents.add(analysis_id)
        return X4Run(world, cond, seed, panels, weights, oracle, gate, s0, tuple(sorted(parents)))

    def _weights(self, act: ActivationSet, step: int, aid: str) -> tuple[Weights, str]:
        if not act.checkpoint_id:
            raise _fail("checkpoint_id", "ActivationSet without checkpoint", aid)
        ckpt = self.store.load(Checkpoint, act.checkpoint_id, consumer=CONS)
        if ckpt.step != step:
            raise _fail("checkpoint_step", f"checkpoint step {ckpt.step} != {step}", aid)
        model = load_model(ckpt)
        as_np = [t.detach().cpu().double().numpy() for t in
                 (model.ln_final.weight, model.ln_final.bias, model.unembed.weight)]
        return (as_np[0], as_np[1], as_np[2]), act.checkpoint_id

    def _panels(self, act: ActivationSet, aid: str) -> dict[int, X4Panel]:
        index_id = next((p for p in self.store.meta(aid).parent_ids
                         if self.store.meta(p).artifact_type == "HistoryIndex"), None)
        if index_id is None:
            raise _fail("history_index", "ActivationSet has no HistoryIndex parent", aid)
        index = self.store.load(HistoryIndex, index_id, consumer=CONS)
        row_of = {str(h): i for i, h in enumerate(act.history_id.tolist())}
        k_z, k_ln = act.hooks.index(self.hook), act.hooks.index("ln_final_out")
        hist, panel_of = np.asarray(index.history_id), np.asarray(index.panel)
        out = {}
        for p in sorted({int(x) for x in panel_of.tolist()}):
            ids = tuple(str(h) for h in hist[panel_of == p])
            rows = [row_of[h] for h in ids]
            out[p] = X4Panel(ids, act.A[rows, k_z].astype(np.float64),
                             act.A[rows, k_ln].astype(np.float64),
                             act.logits[rows].astype(np.float64))
        return out

    def _oracle(self, aj: AnalysisJob, inputs: dict, final_aid: str,
                panels: dict) -> dict[int, dict[str, np.ndarray]]:
        last = aj._history_tokens(inputs, offset=-1)
        refs = {"emission_id": inputs["emission"],
                "transition_id": child_of(self.store, TransitionSpec, inputs["world"]),
                "obs_test_id": inputs["obs_test"], "history_index_id": inputs["history_index"],
                "k": self.cfg.base["baselines"]["spectral_components"]}
        sb, out = SpaceBuilder(self.store), {}
        for p in sorted({p for (_, p) in panels}):
            sets = {"b32": sb.beliefs(inputs["oracle"], "b32", p),
                    "b1": sb.beliefs(inputs["oracle"], "b1", p),
                    "q": sb.futures(inputs["oracle"], 1, p),
                    "R2": sb.baseline("R2", p, **refs), "R3": sb.baseline("R3", p, **refs)}
            ids = list(panels[(self.final, p)].ids)
            for ps in sets.values():
                if list(ps.ids) != ids:
                    raise StageFailure(ErrorCode.SAMPLE_ID_MISMATCH, "experiment.X4", "ids",
                                       f"{ps.space} panel {p} ids differ from activations",
                                       final_aid)
            require_same_ids(sets["b32"], sets["R2"])
            out[p] = {k: np.asarray(ps.X, dtype=np.float64) for k, ps in sets.items()}
            out[p]["last_symbol"] = np.array([last[h] for h in ids])
        return out

    # ---- records --------------------------------------------------------------------------
    def _learning_gate(self, source: str, key: tuple) -> tuple[bool | None, str | None]:
        for mid in self.store.find(MetricRecords, stage=source, kind="run", run_key=list(key)):
            for r in self.store.load(MetricRecords, mid, consumer=CONS).rows:
                if r.metric_id == "learning_gate_passed":
                    return (None if r.value is None else bool(r.value)), mid
        return None, None

    def _stored_S(self, source: str) -> tuple[dict, str | None]:
        """S of the primary hook per (world, cond, seed, step, panel) from the newest source
        analysis; values are passed through, never inspected here."""
        ids = sorted(self.store.find(MetricRecords, stage=source, kind="analysis"),
                     key=lambda a: self.store.meta(a).created_utc, reverse=True)
        if not ids:
            return {}, None
        out = {}
        for r in self.store.load(MetricRecords, ids[0], consumer=CONS).rows:
            if (r.space == f"act:{self.hook}" and r.metric_id == "S_H1" and r.value is not None
                    and r.checkpoint in (0, self.final)):
                out[(r.world, r.condition, r.replicate, r.checkpoint, r.panel)] = (r.value,
                                                                                   r.status)
        return out, ids[0]
