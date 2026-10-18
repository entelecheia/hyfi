"""AC11: the execution allowlist behaves the same on Hydra 1.3 and 1.4."""

import json
import warnings

import pytest

from hyfi import Workflow, compose, plan, run_workflow
from hyfi.cli import main
from hyfi.config import TargetNotAllowed, instantiate, is_allowed, iter_targets


def test_is_allowed_patterns():
    assert is_allowed("pkg.mod.fn", ["pkg.*"])
    assert is_allowed("pkg.mod.fn", ["pkg.mod.fn"])
    assert not is_allowed("pkgx.fn", ["pkg.*"])
    assert not is_allowed("pkg", ["pkg.*"])
    assert not is_allowed("anything", [])


def test_iter_targets_is_recursive():
    cfg = {"_target_": "a.f", "x": {"_target_": "b.g"}, "ys": [{"_target_": "c.h"}, 1]}
    assert sorted(iter_targets(cfg)) == ["a.f", "b.g", "c.h"]


def test_instantiate_enforces_nested_targets(project):
    cfg = {"_target_": "fakeplug.steps.double", "xs": {"_target_": "fakeplug.steps.load"}}
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # allowed targets raise no Hydra 1.4 legacy warning
        assert instantiate(cfg, allow=["fakeplug.steps.*"]) == [0, 2, 4]
    with pytest.raises(TargetNotAllowed, match=r"fakeplug\.steps\.load"):
        instantiate(cfg, allow=["fakeplug.steps.double"])


def test_plan_and_run_respect_allow(project):
    cfg = compose(["workflow=plug"])
    wf = Workflow.model_validate(dict(cfg.workflow))
    assert all(s["ok"] for s in plan(wf, allow=["fakeplug.*"]))
    denied = plan(wf, allow=["fakeplug.steps.load"])
    assert [s["ok"] for s in denied] == [True, False, False]
    assert "allowlist" in denied[1]["error"]
    m = run_workflow(cfg, allow=["fakeplug.steps.load"])
    assert m.status == "error"
    assert m.allow == ["fakeplug.steps.load"]
    assert [s.status for s in m.steps] == ["ok", "error", "skipped"]


def test_cli_allow(project, capsys, monkeypatch):
    assert main(["run", "workflow=plug", "--dry-run", "--allow", "other.*"]) == 1
    assert main(["run", "workflow=plug", "--allow", "other.*"]) == 1
    capsys.readouterr()
    monkeypatch.setenv("HYFI_ALLOW", "fakeplug.steps.load, fakeplug.steps.double")
    assert main(["run", "workflow=plug", "--allow", "fakeplug.steps.total", "--json"]) == 0
    first = json.loads(capsys.readouterr().out)
    assert sorted(first["allow"]) == [
        "fakeplug.steps.double",
        "fakeplug.steps.load",
        "fakeplug.steps.total",
    ]
    monkeypatch.delenv("HYFI_ALLOW")
    # rerun keeps the recorded allowlist unless told otherwise
    assert main(["rerun", first["run_id"], "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["allow"] == first["allow"]
    assert main(["rerun", first["run_id"], "--allow", "nope.*"]) == 1


def test_allowlist_covers_every_executable_form(project):
    import builtins

    # tuple-hidden nested target
    with pytest.raises(TargetNotAllowed, match=r"builtins\.str"):
        instantiate(
            {"_target_": "builtins.len", "obj": ({"_target_": "builtins.str", "object": 1},)},
            allow=["builtins.len"],
        )
    # nested target passed through call-site kwargs
    with pytest.raises(TargetNotAllowed, match=r"builtins\.str"):
        instantiate(
            {"_target_": "builtins.dict"},
            allow=["builtins.dict"],
            x={"_target_": "builtins.str", "object": 1},
        )
    # nested target passed through call-site args
    with pytest.raises(TargetNotAllowed, match=r"builtins\.str"):
        instantiate(
            {"_target_": "builtins.len"},
            {"_target_": "builtins.str", "object": 1},
            allow=["builtins.len"],
        )
    # callable target
    with pytest.raises(TargetNotAllowed, match=r"builtins\.len"):
        instantiate({"_target_": builtins.len, "obj": [1, 2]}, allow=["other.*"])
    assert instantiate({"_target_": builtins.len, "_args_": [[1, 2]]}, allow=["builtins.len"]) == 2
