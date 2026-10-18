import subprocess

import pytest

from hyfi import Project, RunManifest, Step, Workflow, compose, plan, run_workflow
from hyfi.manifest import git_info, lock_sha256
from hyfi.runner import load_workflow
from hyfi.workflow import WorkflowError, execute


def wf(*steps):
    return Workflow.model_validate({"name": "t", "steps": list(steps)})


def test_step_alias_and_default_name():
    s = Step.model_validate({"run": "fakeplug.steps.load", "with": {"n": 2}})
    assert s.name == "load"
    assert s.with_ == {"n": 2}
    with pytest.raises(ValueError):
        Step.model_validate({"run": "x", "unknown": 1})


def test_plan_reports_unresolvable(project):
    steps = plan(wf({"run": "fakeplug.steps.load"}, {"run": "fakeplug.steps.nope"}))
    assert [s["ok"] for s in steps] == [True, False]
    assert steps[1]["error"]


def test_execute_pipes_results(project):
    seen = []
    out, records = execute(
        wf(
            {"run": "fakeplug.steps.load", "with": {"n": 3}},
            {"run": "fakeplug.steps.double"},
            {"run": "fakeplug.steps.total"},
        ),
        on_record=seen.append,
    )
    assert out == 6
    assert [r.status for r in records] == ["ok", "ok", "ok"]
    assert len(seen) == 3


def test_execute_without_pipe(project):
    out, _ = execute(
        wf({"run": "fakeplug.steps.load"}, {"run": "fakeplug.steps.constant", "pipe": False})
    )
    assert out == 7


def test_execute_failure_marks_rest_skipped(project):
    seen = []
    with pytest.raises(WorkflowError) as err:
        execute(
            wf(
                {"run": "fakeplug.steps.load"},
                {"run": "fakeplug.steps.boom"},
                {"run": "fakeplug.steps.total"},
            ),
            on_record=seen.append,
        )
    assert [r.status for r in err.value.records] == ["ok", "error", "skipped"]
    assert "boom" in err.value.records[1].error
    assert seen[-1].status == "error"


def test_project_paths(tmp_path):
    p = Project(root=tmp_path)
    assert p.workspace == tmp_path.resolve() / "workspace"
    assert p.runs_dir == tmp_path.resolve() / ".hyfi" / "runs"
    made = p.path("a", "b", mkdir=True)
    assert made.is_dir()
    assert Project(root=tmp_path, workspace="/abs/ws").workspace.as_posix() == "/abs/ws"


def test_load_workflow_requires_selection(project):
    with pytest.raises(ValueError, match="no workflow selected"):
        load_workflow(compose())


def test_run_writes_manifest_and_rerun_matches(project):
    # AC6: rerun records a byte-identical resolved config.
    first = run_workflow(
        compose(["workflow=plug"]), overrides=["workflow=plug"], argv=["hyfi", "run"]
    )
    assert first.status == "ok"
    assert [s.status for s in first.steps] == ["ok", "ok", "ok"]
    runs = Project(root=project).runs_dir
    loaded = RunManifest.load(first.run_id, runs)
    assert loaded.finished_at is not None
    again = run_workflow(loaded.config, overrides=loaded.overrides, rerun_of=loaded.run_id)
    assert again.rerun_of == first.run_id
    assert again.config_json() == first.config_json()
    assert again.run_id != first.run_id


def test_run_records_failure(project):
    cfg = compose(["workflow=plug", "workflow.steps.1.run=fakeplug.steps.boom"])
    m = run_workflow(cfg)
    assert m.status == "error"
    assert "boom" in m.error
    assert RunManifest.load(m.run_id, Project(root=project).runs_dir).status == "error"


def test_manifest_load_missing_or_invalid(tmp_path):
    with pytest.raises(FileNotFoundError):
        RunManifest.load("20261019T000000Z-abcdef", tmp_path)
    for bad in ["nope", "../../etc/x", "20261019T000000Z-abcdef/../x"]:
        with pytest.raises(ValueError, match="not a run id"):
            RunManifest.load(bad, tmp_path)


def test_git_and_lock_info(tmp_path):
    assert git_info(tmp_path) is None
    assert lock_sha256(tmp_path) is None
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=t@e",
            "-c",
            "user.name=t",
            "commit",
            "-q",
            "--allow-empty",
            "-m",
            "x",
        ],
        cwd=tmp_path,
        check=True,
    )
    (tmp_path / "uv.lock").write_text("lock")
    info = git_info(tmp_path)
    assert len(info["sha"]) == 40
    assert info["dirty"] is True  # the untracked uv.lock
    assert len(lock_sha256(tmp_path)) == 64


def test_step_rejects_target_inside_with():
    with pytest.raises(ValueError, match="put the callable in `run`"):
        Step.model_validate({"run": "fakeplug.steps.load", "with": {"_target_": "os.system"}})


def test_plan_resolves_nested_targets(project):
    steps = plan(
        wf({"run": "fakeplug.steps.double", "with": {"xs": {"_target_": "fakeplug.steps.nope"}}})
    )
    assert steps[0]["ok"] is False
    assert "nope" in steps[0]["error"]


def test_env_values_are_not_recorded(project, monkeypatch, capsys):
    from hyfi.cli import main

    monkeypatch.setenv("HYFI_TEST_SECRET", "s3cr3t-value")
    overrides = ["workflow=plug", "+secret=${oc.env:HYFI_TEST_SECRET}"]
    assert main(["run", *overrides, "--json"]) == 0
    out = capsys.readouterr().out
    assert "s3cr3t-value" not in out
    first = RunManifest.model_validate_json(out)
    assert first.config["secret"] == "${oc.env:HYFI_TEST_SECRET}"
    path = Project(root=project).runs_dir / first.run_id / "manifest.json"
    assert "s3cr3t-value" not in path.read_text()
    # rerun re-reads the environment and records the same config
    again = run_workflow(first.config, rerun_of=first.run_id)
    assert again.status == "ok"
    assert again.config_json() == first.config_json()
    monkeypatch.delenv("HYFI_TEST_SECRET")
    with pytest.raises(Exception, match="HYFI_TEST_SECRET"):
        run_workflow(first.config)


def test_project_env_values_are_not_recorded(project, monkeypatch):
    monkeypatch.setenv("HYFI_PROJECT_NAME", "private-name")
    m = run_workflow(compose(["workflow=plug"]))
    assert m.status == "ok"
    assert m.config["project"]["name"] == "${oc.env:HYFI_PROJECT_NAME,hyfi-project}"
    assert m.config["project"]["root"] == str(project.resolve())  # paths are the exception
    path = Project(root=project).runs_dir / m.run_id / "manifest.json"
    assert "private-name" not in path.read_text()
