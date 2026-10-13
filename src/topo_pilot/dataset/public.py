"""The only loader the learner may use, and the latent-field guard."""

from __future__ import annotations

import dataclasses

import torch
from torch.utils.data import Dataset

from topo_pilot.contracts import ErrorCode, ObservationSet, SequenceLayout, StageFailure

_PUBLIC_FIELDS = frozenset({"split", "V", "sequence_id", "tokens", "layout_version"})


def assert_public(obs: object) -> ObservationSet:
    """Return ``obs`` if it is a latent-free ``ObservationSet``, else raise ``LEAKAGE``.

    Invariants: the object is an ``ObservationSet`` and carries no field or attribute beyond
    ``split, V, sequence_id, tokens, layout_version``.

    Raises
    ------
    StageFailure
        ``LEAKAGE`` for any other artifact type or any extra (latent) field.
    """
    if not isinstance(obs, ObservationSet):
        raise StageFailure(ErrorCode.LEAKAGE, "dataset.PublicTokenDataset", "artifact_type",
                           f"expected ObservationSet, got {type(obs).__name__}")
    names = {f.name for f in dataclasses.fields(obs)} | set(vars(obs))
    extra = sorted(names - _PUBLIC_FIELDS)
    if extra:
        raise StageFailure(ErrorCode.LEAKAGE, "dataset.PublicTokenDataset", "latent_field",
                           f"ObservationSet carries non-public fields {extra}")
    return obs


class PublicTokenDataset(Dataset):
    """Map-style dataset ``i -> (inputs [33], targets [33])`` of int64 tensors.

    Math: inputs ``[BOS=V, w_1..w_32]``, targets ``[w_1..w_33]`` via ``SequenceLayout``.

    Shapes: ``len(dataset) = R``; both tensors ``[33]`` int64.

    Raises
    ------
    StageFailure
        ``LEAKAGE`` if ``obs`` is not an ``ObservationSet`` (e.g. an ``EvalSidecar``) or has a
        latent field.
    """

    def __init__(self, obs: ObservationSet, layout: SequenceLayout):
        obs = assert_public(obs)
        self._inputs = torch.from_numpy(layout.model_inputs(obs.tokens, obs.V))
        self._targets = torch.from_numpy(layout.targets(obs.tokens))

    def __len__(self) -> int:
        return int(self._inputs.shape[0])

    def __getitem__(self, i: int) -> tuple[torch.Tensor, torch.Tensor]:
        return self._inputs[i], self._targets[i]
