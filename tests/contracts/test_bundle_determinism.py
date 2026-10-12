import pytest

from topo_pilot.contracts.testing import memory_store, tiny_world_spec

pytestmark = pytest.mark.contracts


def test_C12b_bundle_bytes_are_deterministic(tmp_path):
    """Equal content exported twice (to different file names) gives byte-identical bundles."""
    store = memory_store()
    wid = store.save(tiny_world_spec("cylinder"), config={"family": "cylinder", "n": 3},
                     parents=[], seed_map={}, consumer="world")
    first = store.export_bundle([wid], tmp_path / "a.tar.gz")
    second = store.export_bundle([wid], tmp_path / "sub" / "b.tar.gz")
    assert first.read_bytes() == second.read_bytes()
