import re
import tarfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.executors

from exec_helpers import make_job, seed_input  # noqa: E402

from topo_pilot.contracts import ErrorCode, StageFailure  # noqa: E402
from topo_pilot.executors import BundleExecutor, NotebookExporter, SSHExecutor  # noqa: E402
from topo_pilot.executors.bundle import is_forbidden  # noqa: E402


def test_E04_secrets_in_tree_are_left_out(store, fake_repo, tmp_path):
    input_id = seed_input(store)
    path = BundleExecutor(out_dir=tmp_path / "out", repo_root=fake_repo).submit(
        make_job(input_id), store).location
    with tarfile.open(path) as tar:
        names = tar.getnames()
    assert not [n for n in names if re.search(r"local\.yaml|\.env|token|key", Path(n).name, re.I)]
    assert "bundle_j1/configs/stages.yaml" in names


@pytest.mark.parametrize("secret", ["configs/local.yaml", "configs/api_token.txt", ".env",
                                    "configs/my_KEY.json"])
def test_E04_explicitly_requested_secret_is_refused(store, fake_repo, tmp_path, secret):
    input_id = seed_input(store)
    bex = BundleExecutor(out_dir=tmp_path / "out", repo_root=fake_repo,
                         extra_files=[Path(secret)])
    with pytest.raises(StageFailure) as err:
        bex.submit(make_job(input_id), store)
    assert err.value.code is ErrorCode.EXECUTOR_ERROR


def test_E04_forbidden_name_rule():
    assert all(map(is_forbidden, ["local.yaml", ".env", ".env.prod", "TOKEN.txt", "a_key.pem"]))
    assert not any(map(is_forbidden, ["base.yaml", "stages.yaml", "main.py"]))


def test_E06_notebook_is_valid_nbformat_with_three_code_cells(tmp_path):
    import json
    nb_path = NotebookExporter().export(tmp_path / "bundle_j1.tar.gz", tmp_path / "nb")
    assert nb_path.name == "notebook_j1.ipynb"
    nb = json.loads(nb_path.read_text())
    assert nb["nbformat"] == 4 and "nbformat_minor" in nb and "metadata" in nb
    assert len(nb["cells"]) == 3
    for cell in nb["cells"]:
        assert cell["cell_type"] == "code" and cell["outputs"] == []
        assert cell["execution_count"] is None and isinstance(cell["source"], list)
        code = "".join(line for line in cell["source"] if not line.startswith("%"))
        compile(code, "cell", "exec")
    text = nb_path.read_text()
    assert "drive.mount" not in text and "google.colab" not in text
    assert "--install-only" in "".join(nb["cells"][1]["source"])
    assert "bundle_j1.tar.gz" in "".join(nb["cells"][0]["source"])


LOCAL = {"ssh": {"host": "gpu.example.org", "user": "me", "remote_dir": "/data/tp x"}}


def test_E01_ssh_builds_expected_command_lines(tmp_path):
    ex = SSHExecutor(LOCAL, out_dir=tmp_path)
    assert ex.upload_cmd(Path("b.tar.gz")) == ["scp", "b.tar.gz", "me@gpu.example.org:/data/tp x/"]
    run = ex.run_cmd("j1")
    assert run[:2] == ["ssh", "me@gpu.example.org"]
    assert "'/data/tp x'" in run[2] and "tar xzf bundle_j1.tar.gz" in run[2]
    assert "run_bundle.py" in run[2] and "exit_code" in run[2]
    assert ex.status_cmd("j1")[:2] == ["ssh", "me@gpu.example.org"]
    assert ex.download_cmd("j1", Path("o.tar.gz")) == [
        "scp", "me@gpu.example.org:/data/tp x/bundle_j1/outputs_j1.tar.gz", "o.tar.gz"]


def test_E01_ssh_requires_host_and_remote_dir(tmp_path):
    with pytest.raises(StageFailure) as err:
        SSHExecutor({"ssh": {"host": "h"}}, out_dir=tmp_path)
    assert err.value.code is ErrorCode.EXECUTOR_ERROR


def test_E01_ssh_status_parses_remote_output(tmp_path, monkeypatch):
    from topo_pilot.executors import JobHandle
    ex = SSHExecutor(LOCAL, out_dir=tmp_path)
    handle = JobHandle("j1", "ssh", "x")
    for out, want in [("running\n", "running"), ("0\n", "done"), ("1\n", "failed")]:
        monkeypatch.setattr(ex, "_exec", lambda cmd, out=out: out)
        assert ex.status(handle) == want
