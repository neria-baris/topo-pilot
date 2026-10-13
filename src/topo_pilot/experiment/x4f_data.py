"""X4-F gate data (x4f-exec-v2 §2–§3): frozen inputs, dev activations and oracle targets.

Reads existing artifacts only; new dev ActivationSets go to an independent store through
``ReadThroughBackend``. Targets come from the public dev tokens and the approved T/E/pi through
the existing oracle kernels; no EvalSidecar is read.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from topo_pilot.activations import ActivationStage
from topo_pilot.analysis import circle_expectation
from topo_pilot.contracts import (
    ActivationSet,
    ArtifactStore,
    Checkpoint,
    EmissionSpec,
    ErrorCode,
    HistoryIndex,
    ObservationSet,
    SequenceLayout,
    StageFailure,
    TransitionSpec,
    WorldSpec,
    tokens_hash,
)
from topo_pilot.oracle import BayesFilter, LastSymbolPosterior

from .s2 import child_of
from .s4_analysis import AnalysisJob
from .x4b import EXPECTED, S7_RECORDS, SHARED, ancestors

CONS = "experiment"
SEEDS = (1729, 2718, 3141)
STEP = 5000
HOOKS = ("embed", "resid_post_1", "resid_post_3", "ln_final_out")
INDEX = 32
PERIOD = 12.0
CAL_PANELS = (1, 2, 3, 4, 5, 6)
VAL_PANELS = (7, 8)


def _missing(check: str, detail: str) -> StageFailure:
    return StageFailure(ErrorCode.MISSING_PARENT, "experiment.X4F", check, detail)


def resolve(aj: AnalysisJob, store: ArtifactStore, seed: int) -> dict[str, str]:
    """Frozen ids of one model: checkpoint (step 5000), dev index/obs, emission, T, world.

    Raises
    ------
    StageFailure
        ``MISSING_PARENT`` on any mismatch with the frozen Phase-B table or the S7 lineage.
    """
    inp = aj.inputs("cylinder", "O", seed)
    ids = {"world": inp["world"], "emission": inp["emission"], "obs_dev": inp["obs_dev"],
           "transition": child_of(store, TransitionSpec, inp["world"]),
           "dev_index": child_of(store, HistoryIndex, inp["obs_dev"], split="dev")}
    cids = store.find(Checkpoint, run_key=["cylinder", "O", seed], step=STEP,
                      train_config=aj.train_config)
    if len(cids) != 1:
        raise _missing("checkpoint", f"{len(cids)} step-{STEP} checkpoints for seed {seed}")
    ids["checkpoint"] = cids[0]
    want = {k: EXPECTED[seed][k] for k in ("emission", "obs_dev", "dev_index")}
    want.update(world=SHARED["world"], transition=SHARED["transition"])
    bad = {k: (ids[k], v) for k, v in want.items() if ids[k] != v}
    if bad:
        raise _missing("frozen_inputs", f"seed {seed}: {bad}")
    if not {ids["checkpoint"], ids["dev_index"]} <= ancestors(store, S7_RECORDS["dev_extract"]):
        raise _missing("s7_lineage", f"seed {seed}: checkpoint or dev index not under S7")
    return ids


def extract(rw_store: ArtifactStore, ids: dict[str, str]) -> str:
    """Dev ActivationSet (HOOKS, panels 1-8) of one step-5000 checkpoint in ``rw_store``."""
    return ActivationStage(device="cpu").run(ids["checkpoint"], ids["obs_dev"], ids["dev_index"],
                                             HOOKS, list(range(1, 9)), rw_store)


@dataclass(frozen=True, eq=False)
class ModelData:
    """Per-model dev rows in HistoryIndex order; ``cal``/``val`` are boolean row masks."""

    seed: int
    history_id: tuple[str, ...]
    panel: NDArray[np.int64]
    inputs: NDArray[np.int64]
    acts: dict[str, NDArray[np.float64]]
    targets: dict[str, NDArray[np.float64]]
    cal: NDArray[np.bool_]
    val: NDArray[np.bool_]


def _incidence(world: WorldSpec) -> NDArray[np.float64]:
    n = int(np.asarray(world.coords).shape[0])
    N = np.eye(n)
    e = np.asarray(world.edges, dtype=np.int64)
    N[e[:, 0], e[:, 1]] = 1.0
    N[e[:, 1], e[:, 0]] = 1.0
    return N


def load_model_data(store: ArtifactStore, ids: dict[str, str], act_id: str, seed: int) -> ModelData:
    """Tokens, activations at input index 32 and oracle targets of one model's dev pool."""
    index = store.load(HistoryIndex, ids["dev_index"], consumer=CONS)
    obs = store.load(ObservationSet, ids["obs_dev"], consumer=CONS)
    row = {int(s): i for i, s in enumerate(obs.sequence_id.tolist())}
    tok = np.asarray(obs.tokens[[row[int(s)] for s in index.sequence_id.tolist()]],
                     dtype=np.int64)
    if [tokens_hash(t[:INDEX]) for t in tok] != [str(h) for h in index.tokens_hash]:
        raise StageFailure(ErrorCode.SAMPLE_ID_MISMATCH, "experiment.X4F", "tokens_hash",
                           f"dev index {ids['dev_index']} vs obs {ids['obs_dev']}")
    act = store.load(ActivationSet, act_id, consumer=CONS)
    hid = [str(h) for h in index.history_id]
    if [str(h) for h in act.history_id] != hid:
        raise StageFailure(ErrorCode.SAMPLE_ID_MISMATCH, "experiment.X4F", "activation_ids",
                           f"{act_id} rows differ from HistoryIndex order")
    acts = {h: np.asarray(act.A[:, act.hooks.index(h), :], dtype=np.float64) for h in HOOKS}
    trans = store.load(TransitionSpec, ids["transition"], consumer=CONS)
    emis = store.load(EmissionSpec, ids["emission"], consumer=CONS)
    world = store.load(WorldSpec, ids["world"], consumer=CONS)
    T, E, pi = (np.asarray(a, dtype=np.float64) for a in (trans.T, emis.E, trans.pi))
    hist = tok[:, :INDEX]
    filt = BayesFilter(T, E, pi)
    b32 = filt.run(hist).b[:, INDEX - 1]
    b2 = filt.run(hist[:, INDEX - 2:]).b[:, 1]
    b1 = LastSymbolPosterior(T, E, pi).r(hist[:, -1])
    x = np.asarray(world.coords, dtype=np.float64)[:, 0]
    if x.max() + 1 != PERIOD:
        raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "experiment.X4F", "period",
                           f"x period {x.max() + 1} != {PERIOD}")
    m32, m2 = circle_expectation(b32, x, PERIOD), circle_expectation(b2, x, PERIOD)
    V = E.shape[1]
    targets = {"m32": m32, "m2": m2, "m1": circle_expectation(b1, x, PERIOD), "r2": m32 - m2,
               "Q1": b32 @ (T @ E), "onehot_w32": np.eye(V)[hist[:, -1]],
               "local": b32 @ _incidence(world)}
    panel = np.asarray(index.panel, dtype=np.int64)
    inputs = SequenceLayout().model_inputs(tok, V)
    return ModelData(seed, tuple(hid), panel, inputs, acts, targets,
                     np.isin(panel, CAL_PANELS), np.isin(panel, VAL_PANELS))
