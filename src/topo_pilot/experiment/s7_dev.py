"""S7 dev data (D-047): dev panels, dev activations, dev and test probe targets.

Probes and the PCA-32 sensitivity variant are fitted on dev histories, never on test. The dev
panels are drawn by ``dataset.PanelBuilder`` from ``obs_dev`` (8 × 512 = all 4096 dev
trajectories) with the stream ``SeedTree(master).generator("panels", "dev", family, mode,
sigma)``. Dev ActivationSets hold the primary hook only and record ``panels`` as the explicit
list ``[1..8]`` (test sets use ``"all"`` or ``[1]``); ``s3.activation_ids`` also keeps only
test-split sets, so dev sets never enter a test-panel analysis. Dev beliefs come from the
public oracle kernels and are not stored.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np

from topo_pilot.activations import ActivationStage
from topo_pilot.contracts import (
    ActivationSet,
    ArtifactStore,
    Checkpoint,
    EmissionSpec,
    ErrorCode,
    HistoryIndex,
    ObservationSet,
    OracleOutputs,
    SeedTree,
    StageFailure,
    TransitionSpec,
)
from topo_pilot.dataset import DatasetConfig, PanelBuilder
from topo_pilot.oracle import BayesFilter, LastSymbolPosterior

from .config import ResolvedConfig
from .s2 import child_of
from .s4_analysis import WORLDS, AnalysisJob

log = logging.getLogger(__name__)
CONS = "experiment"
END = 32


@dataclass(frozen=True)
class ProbeData:
    """Rows of one split: ``ids [M]``, ``panel [M]``, targets ``b32, b1 [M, N]``, ``q [M, V]``
    (the exact one-step future F1), ``w32 [M]`` (last symbol)."""

    ids: list[str]
    panel: np.ndarray
    b32: np.ndarray
    b1: np.ndarray
    q: np.ndarray
    w32: np.ndarray


class DevData:
    """Dev panels, dev activations and aligned probe targets for the O/P runs."""

    def __init__(self, cfg: ResolvedConfig, store: ArtifactStore):
        self.cfg, self.store = cfg, store
        s7 = cfg.stage("S7")
        self.hook = s7["dev_extract"]["hook"]
        self.steps = tuple(int(s) for s in s7["dev_extract"]["checkpoints"])
        self.conditions = tuple(s7["analysis_conditions"])
        data = cfg.base["data"]
        self.dcfg = DatasetConfig(n_panels=data["n_panels"], panel_size=data["panel_size"],
                                  analysis_position=END)
        self.panel_list = list(range(1, self.dcfg.n_panels + 1))
        self.aj = AnalysisJob("S4", cfg, store)

    def runs(self) -> list[tuple[str, str, int]]:
        return [(w, c, int(s)) for c in self.conditions for s in self.cfg.base["seeds"]["masters"]
                for w in WORLDS]

    # ---- dev panels and activations ------------------------------------------------------
    def dev_index(self, world: str, cond: str, seed: int) -> str:
        """The dev HistoryIndex of a run (built and stored on first use)."""
        obs_id = self.aj.inputs(world, cond, seed)["obs_dev"]
        found = [h for h in self.store.find(HistoryIndex, split="dev")
                 if obs_id in self.store.meta(h).parent_ids]
        if found:
            return found[0]
        meta = self.store.meta(obs_id).config
        tree = SeedTree(seed)
        rng = tree.generator("panels", "dev", meta["family"], meta["mode"], meta["sigma"])
        obs = self.store.load(ObservationSet, obs_id, consumer=CONS)
        index = PanelBuilder().build(obs, self.dcfg, rng, dataset_id=obs_id)
        conf = {k: meta[k] for k in ("family", "mode", "sigma", "V", "N", "replicate")}
        conf.update(split="dev", n_panels=self.dcfg.n_panels, panel_size=self.dcfg.panel_size,
                    end=END)
        return self.store.save(index, config=conf, parents=[obs_id], seed_map=dict(tree.issued),
                               consumer=CONS)

    def checkpoint(self, world: str, cond: str, seed: int, step: int) -> str:
        cids = self.store.find(Checkpoint, run_key=[world, cond, seed], step=step,
                               train_config=self.aj.train_config)
        if len(cids) != 1:
            raise StageFailure(ErrorCode.MISSING_PARENT, "experiment.S7", "checkpoint",
                               f"{len(cids)} checkpoints for {world}-{cond}-{seed} step {step}")
        return cids[0]

    def dev_acts(self, world: str, cond: str, seed: int, step: int) -> str:
        """Dev ActivationSet (primary hook, all dev panels) of a run at ``step``."""
        cid = self.checkpoint(world, cond, seed, step)
        index_id = self.dev_index(world, cond, seed)
        found = [a for a in self.store.find(ActivationSet, checkpoint_id=cid, hooks=[self.hook],
                                            panels=self.panel_list)
                 if index_id in self.store.meta(a).parent_ids]
        if found:
            return found[0]
        obs_id = self.aj.inputs(world, cond, seed)["obs_dev"]
        return ActivationStage().run(cid, obs_id, index_id, (self.hook,), self.panel_list,
                                     self.store)

    def extract_all(self) -> list[str]:
        out = []
        for world, cond, seed in self.runs():
            for step in self.steps:
                out.append(self.dev_acts(world, cond, seed, step))
        log.info("S7 dev_extract: %d dev ActivationSets", len(out))
        return out

    # ---- features and targets ------------------------------------------------------------
    def features(self, act_id: str, ids: list[str]) -> np.ndarray:
        """Primary-hook rows ``[M, d]`` of an ActivationSet in the order of ``ids``."""
        act = self.store.load(ActivationSet, act_id, consumer=CONS)
        row = {h: i for i, h in enumerate(act.history_id.tolist())}
        return np.asarray(act.A, dtype=np.float64)[[row[h] for h in ids],
                                                   act.hooks.index(self.hook), :]

    def all_rows(self, act_id: str) -> np.ndarray:
        """Every primary-hook row ``[M, d]`` of an ActivationSet (e.g. all dev histories)."""
        act = self.store.load(ActivationSet, act_id, consumer=CONS)
        return np.asarray(act.A, dtype=np.float64)[:, act.hooks.index(self.hook), :]

    def _kernels(self, world: str, cond: str, seed: int):
        inputs = self.aj.inputs(world, cond, seed)
        trans = self.store.load(TransitionSpec, child_of(self.store, TransitionSpec,
                                                         inputs["world"]), consumer=CONS)
        emis = self.store.load(EmissionSpec, inputs["emission"], consumer=CONS)
        return inputs, trans, emis

    def _index_tokens(self, index_id: str, obs_id: str):
        index = self.store.load(HistoryIndex, index_id, consumer=CONS)
        obs = self.store.load(ObservationSet, obs_id, consumer=CONS)
        row = {int(s): i for i, s in enumerate(obs.sequence_id.tolist())}
        tokens = obs.tokens[[row[int(s)] for s in index.sequence_id.tolist()], :END]
        return index, np.asarray(tokens, dtype=np.int64)

    def dev_targets(self, world: str, cond: str, seed: int) -> ProbeData:
        """Exact dev targets from the oracle kernels (b32, r_w, F1 = q at p = 32)."""
        inputs, trans, emis = self._kernels(world, cond, seed)
        index, tokens = self._index_tokens(self.dev_index(world, cond, seed), inputs["obs_dev"])
        res = BayesFilter(trans.T, emis.E, trans.pi).run(tokens)
        b1 = LastSymbolPosterior(trans.T, emis.E, trans.pi).r(tokens[:, -1])
        return ProbeData([str(h) for h in index.history_id], np.asarray(index.panel),
                         res.b[:, END - 1], b1, res.q[:, END], tokens[:, -1])

    def test_targets(self, world: str, cond: str, seed: int) -> ProbeData:
        """Stored test oracle targets in HistoryIndex order."""
        inputs = self.aj.inputs(world, cond, seed)
        index, tokens = self._index_tokens(inputs["history_index"], inputs["obs_test"])
        oracle = self.store.load(OracleOutputs, inputs["oracle"], consumer=CONS)
        row = {h: i for i, h in enumerate(oracle.history_id.tolist())}
        rows = [row[str(h)] for h in index.history_id]
        return ProbeData([str(h) for h in index.history_id], np.asarray(index.panel),
                         oracle.b32[rows], oracle.b1[rows], oracle.q[rows], tokens[:, -1])
