"""I/O layer of the module: the only place that touches the artifact store."""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

from topo_pilot.contracts import (
    ArtifactStore,
    EmissionSpec,
    ErrorCode,
    EvalSidecar,
    HistoryIndex,
    ObservationSet,
    SeedTree,
    SequenceLayout,
    StageFailure,
    TransitionSpec,
)

from .checks import (
    check_disjoint,
    check_first_token,
    check_ranges,
    make_sequence_ids,
    process_code,
)
from .config import DatasetConfig
from .panels import PanelBuilder
from .public import assert_public
from .sampler import HMMSampler

log = logging.getLogger(__name__)
CONSUMER = "dataset"


def _sigma_str(sigma: Any) -> str:
    return "none" if sigma is None else repr(float(sigma))


class DatasetStage:
    """Samples, splits, checks, and saves the public and privileged data of one process.

    Seed scheme (D-012, D-019), with ``sigma`` as ``repr`` string or ``"none"``:

    - test: ``SeedTree(0).generator("data", "test", family, mode, sigma)``;
    - panels: ``SeedTree(0).generator("panels", family, mode, sigma)``;
    - train/dev: ``seeds.generator("data", split, family, mode, sigma, seeds.master)``.

    Sequence ids: see ``checks.make_sequence_ids``; the test split uses replicate ``"shared"``.

    Math: emissions are sampled in canonical symbol order, ``E_canon = E[:, symbol_perm]``,
    drawing canonical index ``j`` and emitting token ``symbol_perm[j]``.

    Shapes: returns ids of obs_train, obs_dev, obs_test, sidecar_dev, sidecar_test,
    history_index. Train latents are never persisted.

    Raises
    ------
    StageFailure
        ``ALIGNMENT_ERROR`` (ranges, panel sizes), ``SPLIT_OVERLAP``, ``LEAKAGE``,
        ``NUMERICAL_FAILURE`` (``sampler_bias``).
    """

    def run(self, transition_id: str, emission_id: str, cfg: DatasetConfig,
            seeds: SeedTree, store: ArtifactStore) -> dict[str, str]:
        if cfg.n_test < cfg.n_panels * cfg.panel_size:
            raise StageFailure(ErrorCode.ALIGNMENT_ERROR, "dataset.DatasetStage", "n_test",
                               f"n_test={cfg.n_test} < {cfg.n_panels}*{cfg.panel_size}")
        trans = store.load(TransitionSpec, transition_id, consumer=CONSUMER)
        emis = store.load(EmissionSpec, emission_id, consumer=CONSUMER)
        meta = store.meta(emission_id)
        world = store.meta(meta.parent_ids[0]).config["family"]
        mode = meta.config.get("mode", emis.mode)
        sigma = _sigma_str(meta.config.get("sigma", emis.sigma))
        scope = (world, mode, sigma)
        data = self._sample_all(trans, emis, cfg, seeds, scope)
        return self._save_all(data, scope, (transition_id, emission_id), cfg, seeds, store)

    def _sample_all(self, trans: TransitionSpec, emis: EmissionSpec, cfg: DatasetConfig,
                    seeds: SeedTree, scope: tuple[str, str, str]) -> dict[str, Any]:
        layout = SequenceLayout()
        perm = np.asarray(emis.symbol_perm, dtype=np.int64)
        N, V = emis.E.shape
        sampler = HMMSampler(trans.T, emis.E[:, perm], trans.pi, layout)
        p_w = trans.pi @ emis.E
        tree0 = SeedTree(0)
        rngs = {"train": seeds.generator("data", "train", *scope, seeds.master),
                "dev": seeds.generator("data", "dev", *scope, seeds.master),
                "test": tree0.generator("data", "test", *scope)}
        sizes = {"train": cfg.n_train, "dev": cfg.n_dev, "test": cfg.n_test}
        out: dict[str, Any] = {"V": V, "N": N, "tree0": tree0}
        for split in ("train", "dev", "test"):
            canon, states = sampler.sample(sizes[split], rngs[split])
            tokens = perm[canon.astype(np.int64)].astype(canon.dtype)
            check_ranges(tokens, states, V, N)
            check_first_token(tokens[:, 0], p_w, split)
            out[split] = (tokens, states)
        return out

    def _save_all(self, data: dict[str, Any], scope: tuple[str, str, str],
                  parents: tuple[str, str], cfg: DatasetConfig, seeds: SeedTree,
                  store: ArtifactStore) -> dict[str, str]:
        family, mode, sigma = scope
        replicate = seeds.master
        test_tree = data["tree0"]
        obs: dict[str, ObservationSet] = {}
        for split in ("train", "dev", "test"):
            rep: int | str = "shared" if split == "test" else replicate
            ids = make_sequence_ids(process_code(family, mode, sigma, rep), split,
                                    data[split][0].shape[0])
            obs[split] = assert_public(ObservationSet(
                split=split, V=data["V"], sequence_id=ids, tokens=data[split][0]))
        check_disjoint(**{k: v.sequence_id for k, v in obs.items()})
        base = {"family": family, "mode": mode, "sigma": sigma, "V": data["V"], "N": data["N"]}
        sizes = {"train": cfg.n_train, "dev": cfg.n_dev, "test": cfg.n_test}

        def conf(split: str) -> dict[str, Any]:
            c = {**base, "split": split, "n": sizes[split]}
            if split != "test":
                c["replicate"] = replicate
            return c

        out: dict[str, str] = {}
        for split in ("train", "dev", "test"):
            seed_map = dict(test_tree.issued if split == "test" else seeds.issued)
            out[f"obs_{split}"] = store.save(obs[split], config=conf(split), parents=parents,
                                             seed_map=seed_map, consumer=CONSUMER)
        for split in ("dev", "test"):
            side = EvalSidecar(split=split, N=data["N"], sequence_id=obs[split].sequence_id,
                               z=data[split][1])
            out[f"sidecar_{split}"] = store.save(side, config=conf(split), parents=parents,
                                                 seed_map={}, consumer=CONSUMER)
        out["history_index"] = self._save_panels(obs["test"], out["obs_test"], base, cfg, store)
        log.info("dataset stage saved %s", sorted(out))
        return out

    def _save_panels(self, test: ObservationSet, test_id: str, base: dict[str, Any],
                     cfg: DatasetConfig, store: ArtifactStore) -> str:
        tree = SeedTree(0)
        rng = tree.generator("panels", base["family"], base["mode"], base["sigma"])
        index: HistoryIndex = PanelBuilder().build(test, cfg, rng, dataset_id=test_id)
        conf = {**base, "n_panels": cfg.n_panels, "panel_size": cfg.panel_size,
                "end": cfg.analysis_position}
        return store.save(index, config=conf, parents=[test_id], seed_map=dict(tree.issued),
                          consumer=CONSUMER)
