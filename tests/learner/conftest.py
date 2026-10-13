"""Module-local fixtures: tiny model / data on CPU."""

import dataclasses

import pytest

from topo_pilot.contracts import SeedTree, SequenceLayout
from topo_pilot.contracts.testing import tiny_observations
from topo_pilot.dataset import PublicTokenDataset
from topo_pilot.learner import ModelConfig, TrainConfig


@pytest.fixture(scope="session")
def tiny_obs():
    return dataclasses.replace(tiny_observations(R=8, seed=0), split="train")


@pytest.fixture(scope="session")
def tiny_ds(tiny_obs):
    return PublicTokenDataset(tiny_obs, SequenceLayout())


@pytest.fixture()
def model_cfg():
    return ModelConfig(vocab_in=4, vocab_out=3, n_layers=2, d_model=16, n_heads=2, d_mlp=32)


@pytest.fixture()
def train_cfg():
    return TrainConfig(steps=12, batch_size=4, lr=3e-3, warmup=3, checkpoint_steps=(0, 5, 12),
                       device="cpu")


@pytest.fixture()
def seeds():
    return SeedTree(1729)
