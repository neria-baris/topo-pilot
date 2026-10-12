import os
import subprocess
import sys
import tarfile
from collections import namedtuple

import pytest

pytestmark = pytest.mark.executors

from exec_helpers import make_job, make_store, seed_input, tamper_tar  # noqa: E402

from topo_pilot.contracts import ErrorCode, MetricRecords, RunManifest, StageFailure  # noqa: E402
from topo_pilot.executors import BundleExecutor  # noqa: E402

Remote = namedtuple("Remote", "outputs returncode stderr")


def run_remote(fake_repo, root, job_kwargs):
    """Build the bundle for a stub job, unpack it in a fresh folder, run run_bundle.py there."""
    store = make_store(root / "src_store")
    job = make_job(seed_input(store), **job_kwargs)
    handle = BundleExecutor(out_dir=root / "out", repo_root=fake_repo).submit(job, store)
    dest = root / "remote"
    with tarfile.open(handle.location) as tar:
        tar.extractall(dest)
    (top,) = list(dest.iterdir())
    stub_dir = os.path.dirname(os.path.abspath(__file__))
    env = {**os.environ, "PYTHONPATH": stub_dir}
    proc = subprocess.run([sys.executable, "run_bundle.py", "--no-install"], cwd=top, env=env,
                          capture_output=True, text=True, timeout=120)
    return Remote(top / "outputs_j1.tar.gz", proc.returncode, proc.stderr)


@pytest.fixture(scope="module")
def remote_ok(fake_repo, tmp_path_factory):
    return run_remote(fake_repo, tmp_path_factory.mktemp("ok"), {})


@pytest.fixture(scope="module")
def remote_fail(fake_repo, tmp_path_factory):
    return run_remote(fake_repo, tmp_path_factory.mktemp("fail"), {"fail": True})


def submitted(fake_repo, tmp_path, store, **job_kwargs):
    input_id = seed_input(store)
    bex = BundleExecutor(out_dir=tmp_path / "out", repo_root=fake_repo)
    return bex, bex.submit(make_job(input_id, **job_kwargs), store)


def test_E02_bundle_round_trip_matches_local_run(store, fake_repo, tmp_path, remote_ok):
    assert remote_ok.returncode == 0, remote_ok.stderr
    from stub_stage import StubStage
    local_store = make_store(tmp_path / "local_store")
    job = make_job(seed_input(local_store))
    local_ids = StubStage().execute(job.resolved_config, None, local_store)

    bex, handle = submitted(fake_repo, tmp_path, store)
    ids = bex.fetch(handle, store, outputs_path=remote_ok.outputs)
    assert ids == local_ids
    assert store.load(MetricRecords, ids[0], consumer="experiment").rows[0].value == 12.5
    (mid,) = [k.split("/")[1] for k in store.backend.list("RunManifest/")
              if k.endswith("meta.json")]
    manifest = store.load(RunManifest, mid, consumer="experiment")
    assert manifest.executor == "bundle" and manifest.hardware["cpu_count"] >= 1


def test_E02_bundle_layout_and_git_sha_recorded(store, fake_repo, tmp_path):
    _, handle = submitted(fake_repo, tmp_path, store)
    with tarfile.open(handle.location) as tar:
        names = set(tar.getnames())
        job_doc = tar.extractfile("bundle_j1/job.json").read().decode()
    for need in ("run_bundle.py", "job.json", "inputs.tar.gz", "requirements.lock",
                 "pyproject.toml", "configs/base.yaml", "src/topo_pilot/contracts/__init__.py"):
        assert f"bundle_j1/{need}" in names
    assert '"git_sha"' in job_doc


def test_E02_failed_remote_job_comes_back_as_failure(store, fake_repo, tmp_path, remote_fail):
    assert remote_fail.returncode == 1
    bex, handle = submitted(fake_repo, tmp_path, store, fail=True)
    with pytest.raises(StageFailure) as err:
        bex.fetch(handle, store, outputs_path=remote_fail.outputs)
    assert err.value.code is ErrorCode.EXECUTOR_ERROR
    assert bex.status(handle) == "failed"


def test_E03_tampered_outputs_raise_checksum_mismatch(store, fake_repo, tmp_path, remote_ok):
    bex, handle = submitted(fake_repo, tmp_path, store)
    bad = tamper_tar(remote_ok.outputs, tmp_path / "bad.tar.gz")
    with pytest.raises(StageFailure) as err:
        bex.fetch(handle, store, outputs_path=bad)
    assert err.value.code is ErrorCode.CHECKSUM_MISMATCH
    assert bex.status(handle) == "awaiting_user"


def test_E03_unexpected_output_type_rejected_and_nothing_imported(store, fake_repo, tmp_path,
                                                                  remote_ok):
    bex, handle = submitted(fake_repo, tmp_path, store, expected=("GateReport",))
    with pytest.raises(StageFailure) as err:
        bex.fetch(handle, store, outputs_path=remote_ok.outputs)
    assert err.value.code is ErrorCode.EXECUTOR_ERROR
    assert store.find(MetricRecords, stage="STUB") == []


def test_E03_missing_parent_is_reported(fake_repo, tmp_path, remote_ok):
    bex, handle = submitted(fake_repo, tmp_path, make_store(tmp_path / "s"))
    empty = make_store(tmp_path / "empty")
    with pytest.raises(StageFailure) as err:
        bex.fetch(handle, empty, outputs_path=remote_ok.outputs)
    assert err.value.code is ErrorCode.MISSING_PARENT


def test_E05_status_awaiting_user_then_done(store, fake_repo, tmp_path, remote_ok):
    bex, handle = submitted(fake_repo, tmp_path, store)
    assert bex.status(handle) == "awaiting_user"
    assert "outputs_j1.tar.gz" in bex.instructions(handle)
    bex.fetch(handle, store, outputs_path=remote_ok.outputs)
    assert bex.status(handle) == "done"
    other = BundleExecutor(out_dir=tmp_path / "out", repo_root=fake_repo)
    with pytest.raises(StageFailure):  # per-instance state, no globals
        other.status(handle)
