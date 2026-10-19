import json
import subprocess
import sys

from hyfi.cli import main


def run(capsys, *argv):
    code = main(list(argv))
    out, err = capsys.readouterr()
    return code, out, err


def test_version_via_module():
    out = subprocess.run(
        [sys.executable, "-m", "hyfi", "--version"], capture_output=True, text=True, check=True
    )
    assert out.stdout.startswith("hyfi ")


def test_config_show(project, capsys):
    code, out, _ = run(capsys, "config", "show", "project.name=demo")
    assert code == 0
    assert "name: demo" in out
    code, out, _ = run(capsys, "config", "show", "--json", "--no-resolve")
    assert json.loads(out)["project"]["name"].startswith("${oc.env:")


def test_config_schema(capsys):
    # AC7
    code, out, _ = run(capsys, "config", "schema", "workflow")
    assert code == 0
    schema = json.loads(out)
    assert schema["title"] == "Workflow"
    assert "steps" in schema["properties"]
    code, out, _ = run(capsys, "config", "schema", "hyfi.project.Project")
    assert json.loads(out)["title"] == "Project"
    code, _, err = run(capsys, "config", "schema", "pathlib.Path")
    assert code == 2
    assert "not a Pydantic model" in err


def test_plugins(project, capsys):
    code, out, _ = run(capsys, "plugins", "--json")
    assert code == 0
    rows = {r["name"]: r for r in json.loads(out)}
    assert rows["fakeplug"]["available"] is True
    assert rows["ghost"]["available"] is False
    code, out, _ = run(capsys, "plugins")
    assert code == 0
    assert "MISSING" in out


def test_run_dry_run(project, capsys):
    # AC5
    code, out, _ = run(capsys, "run", "workflow=plug", "--dry-run", "--json")
    assert code == 0
    data = json.loads(out)
    assert data["workflow"] == "plug"
    assert [s["name"] for s in data["steps"]] == ["load", "double", "total"]
    code, out, _ = run(
        capsys, "run", "workflow=plug", "workflow.steps.0.run=nowhere.fn", "--dry-run", "--json"
    )
    assert code == 1
    assert json.loads(out)["steps"][0]["ok"] is False


def test_run_and_rerun(project, capsys):
    code, out, _ = run(capsys, "run", "workflow=plug", "--json")
    assert code == 0
    first = json.loads(out)
    assert first["status"] == "ok"
    code, out, _ = run(capsys, "rerun", first["run_id"], "--json")
    assert code == 0
    second = json.loads(out)
    assert second["rerun_of"] == first["run_id"]
    assert second["config"] == first["config"]
    code, out, _ = run(capsys, "rerun", first["run_id"])
    assert code == 0
    assert "manifest:" in out
    code, out, _ = run(capsys, "rerun", first["run_id"], "--dry-run")
    assert code == 0


def test_run_failure_exit_codes(project, capsys):
    code, out, _ = run(capsys, "run", "workflow=plug", "workflow.steps.1.run=fakeplug.steps.boom")
    assert code == 1
    assert "error" in out
    code, out, err = run(capsys, "run", "--json")
    assert code == 2
    assert "no workflow selected" in json.loads(out)["error"]
    assert "hyfi: error:" in err


def test_usage_error_exits_2(capsys):
    assert main([]) == 2
    assert "hyfi --help" in capsys.readouterr().err
    assert main(["bogus", "--json"]) == 2
    assert json.loads(capsys.readouterr().out)["error"].startswith("UsageError:")
    assert main(["config", "schema", "project", "--json"]) == 0


def test_dry_run_does_not_print_env_values(project, capsys, monkeypatch):
    monkeypatch.setenv("HYFI_TEST_SECRET", "s3cr3t-value")
    args = ["run", "workflow=plug", "+workflow.steps.2.with.token=${oc.env:HYFI_TEST_SECRET}"]
    assert main([*args, "--dry-run", "--json"]) == 0
    out = capsys.readouterr().out
    assert "s3cr3t-value" not in out
    assert json.loads(out)["steps"][2]["with"]["token"] == "${oc.env:HYFI_TEST_SECRET}"


def test_rerun_from_elsewhere_writes_to_recorded_root(project, capsys, monkeypatch, tmp_path):
    assert main(["run", "workflow=plug", "--json"]) == 0
    first = json.loads(capsys.readouterr().out)
    assert first["argv"] == ["hyfi", "run", "workflow=plug", "--json"]
    assert first["config"]["project"]["root"] == str(project.resolve())
    other = tmp_path / "other"
    other.mkdir()
    monkeypatch.chdir(other)
    assert main(["rerun", first["run_id"], "--root", str(project), "--json"]) == 0
    second = json.loads(capsys.readouterr().out)
    assert (project / ".hyfi" / "runs" / second["run_id"] / "manifest.json").is_file()
    assert not (other / ".hyfi").exists()
    assert main(["rerun", second["run_id"], "--root", str(project)]) == 0


def test_error_output_is_redacted(project, capsys, monkeypatch):
    monkeypatch.setenv("HYFI_TEST_SECRET", "s3cr3t-value")
    for extra in ([], ["--dry-run"]):
        bad = "+workflow.bogus=${oc.env:HYFI_TEST_SECRET}"  # ValidationError quotes the input
        assert main(["run", "workflow=plug", bad, "--json", *extra]) == 2
        out, err = capsys.readouterr()
        assert "s3cr3t-value" not in out + err
        assert "${oc.env:HYFI_TEST_SECRET}" in json.loads(out)["error"]


def test_missing_config_dir_is_an_error(project, capsys):
    assert main(["config", "show", "--config-dir", "nope", "--json"]) == 2
    assert "config directory not found" in json.loads(capsys.readouterr().out)["error"]


def test_invalid_log_level_falls_back(project, capsys, monkeypatch):
    # hyfi#469: a bad HYFI_LOG_LEVEL warns instead of crashing
    monkeypatch.setenv("HYFI_LOG_LEVEL", "BOGUS")
    assert main(["config", "show", "--json"]) == 0
    out, err = capsys.readouterr()
    assert "unknown HYFI_LOG_LEVEL" in err
    assert json.loads(out)["project"]


def test_interpolated_project_paths_are_absolute_and_survive_rerun(
    project, capsys, monkeypatch, tmp_path
):
    # hyfi#477: ${project.workspace} in step arguments resolves to the absolute project path
    args = [
        "run",
        "workflow=plug",
        "workflow.steps.2.run=fakeplug.steps.touch",
        "+workflow.steps.2.with.target=${project.workspace}/artifact.txt",
        "+workflow.steps.2.pipe=false",
        "--json",
    ]
    assert main(args) == 0
    first = json.loads(capsys.readouterr().out)
    target = first["config"]["workflow"]["steps"][2]["with"]["target"]
    assert target == str(project.resolve() / "workspace" / "artifact.txt")
    (project / "workspace" / "artifact.txt").unlink()
    other = tmp_path / "elsewhere"
    other.mkdir()
    monkeypatch.chdir(other)
    assert main(["rerun", first["run_id"], "--root", str(project), "--json"]) == 0
    assert (project / "workspace" / "artifact.txt").is_file()
    assert not (other / "workspace").exists()
