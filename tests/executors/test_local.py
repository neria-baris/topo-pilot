import json
from collections import namedtuple

import pytest

pytestmark = pytest.mark.executors

from exec_helpers import STUB_ENV, make_job, make_store, seed_input  # noqa: E402

from topo_pilot.contracts import ErrorCode, MetricRecords, RunManifest, StageFailure  # noqa: E402
from topo_pilot.executors import EXECUTOR_REGISTRY, LocalExecutor, entry  # noqa: E402
from topo_pilot.executors._outputs import check_types  # noqa: E402
from topo_pilot.executors.base import job_to_dict  # noqa: E402
from topo_pilot.executors.local import write_job_json  # noqa: E402

Ran = namedtuple("Ran", "ex handle store")


def run_local(fake_repo, root, **job_kwargs):
    store = make_store(root / "store")
    ex = LocalExecutor(work_dir=root / "jobs", repo_root=fake_repo, env=STUB_ENV)
    handle = ex.submit(make_job(seed_input(store), **job_kwargs), store)
    ex._procs[handle.job_id].wait()
    return Ran(ex, handle, store)


@pytest.fixture(scope="module")
def local_ok(fake_repo, tmp_path_factory):
    return run_local(fake_repo, tmp_path_factory.mktemp("local_ok"))


@pytest.fixture(scope="module")
def local_fail(fake_repo, tmp_path_factory):
    return run_local(fake_repo, tmp_path_factory.mktemp("local_fail"), fail=True)


def test_E01_local_runs_stub_in_subprocess_and_imports_output(local_ok):
    ran = local_ok
    ids = ran.ex.fetch(ran.handle, ran.store)
    assert ran.ex.status(ran.handle) == "done"
    assert len(ids) == 1
    rec = ran.store.load(MetricRecords, ids[0], consumer="experiment")
    assert rec.rows[0].value == 12.5
    assert len(ran.store.meta(ids[0]).parent_ids) == 1


def test_E01_manifest_records_executor_hardware_and_time(local_ok):
    store = local_ok.store
    (mid,) = [k.split("/")[1] for k in store.backend.list("RunManifest/")
              if k.endswith("meta.json")]
    manifest = store.load(RunManifest, mid, consumer="experiment")
    assert manifest.executor == "local"
    assert manifest.hardware["platform"] and manifest.hardware["python"]
    assert manifest.wall_time_s > 0 and manifest.failures == ()
    assert manifest.stage_status == {"STUB": "ok"}


def test_E01_failing_stage_records_failure_and_raises_executor_error(local_fail):
    ran = local_fail
    with pytest.raises(StageFailure) as err:
        ran.ex.fetch(ran.handle, ran.store)
    assert err.value.code is ErrorCode.EXECUTOR_ERROR
    assert "NUMERICAL_FAILURE" in err.value.detail
    assert ran.ex.status(ran.handle) == "failed"


def test_E01_unknown_stage_returns_1_and_records_executor_error(fake_repo, tmp_path):
    store = make_store(tmp_path / "store")
    job = make_job(seed_input(store))
    job = type(job)(**{**job.__dict__, "stage_id": "NOPE", "resolved_config": {}})
    path = write_job_json(tmp_path / "j" / "job.json", job, store_root=str(tmp_path / "store"),
                          repo_root=str(fake_repo), executor="local", sha="x")
    assert entry(path) == 1
    result = json.loads(path.with_name("job.result.json").read_text())
    assert result["ok"] is False and result["failures"][0]["code"] == "EXECUTOR_ERROR"
    assert job_to_dict(job)["stage_id"] == "NOPE"


def test_E01_unreadable_job_json_is_executor_error(tmp_path):
    bad = tmp_path / "job.json"
    bad.write_text("{not json")
    with pytest.raises(StageFailure) as err:
        entry(bad)
    assert err.value.code is ErrorCode.EXECUTOR_ERROR


def test_E01_type_whitelist_allows_manifest_and_rejects_others():
    check_types(["MetricRecords", "RunManifest"], ["MetricRecords"], "x")
    with pytest.raises(StageFailure) as err:
        check_types(["GateReport"], ["MetricRecords"], "x")
    assert err.value.code is ErrorCode.EXECUTOR_ERROR


def test_E01_registry_lists_all_executors():
    assert set(EXECUTOR_REGISTRY) == {"local", "bundle", "ssh"}
    assert EXECUTOR_REGISTRY["local"] is LocalExecutor
