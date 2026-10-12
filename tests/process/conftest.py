"""Module-local fixtures for the process tests."""

from __future__ import annotations

import pytest

from topo_pilot.contracts import WorldSpec
from topo_pilot.contracts.testing import tiny_world_spec


@pytest.fixture(scope="session")
def square12() -> WorldSpec:
    """12 x 12 square (core-world size)."""
    return tiny_world_spec("square", n=12)


@pytest.fixture(scope="session")
def cylinder12() -> WorldSpec:
    """12 x 12 cylinder, x periodic with period 12."""
    return tiny_world_spec("cylinder", n=12)


@pytest.fixture(scope="session")
def square3() -> WorldSpec:
    """3 x 3 square."""
    return tiny_world_spec("square", n=3)


@pytest.fixture(scope="session")
def cylinder3() -> WorldSpec:
    """3 x 3 cylinder."""
    return tiny_world_spec("cylinder", n=3)
