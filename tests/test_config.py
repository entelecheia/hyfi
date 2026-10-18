import os
import subprocess
import sys
import textwrap

import pytest
from omegaconf import DictConfig
from pydantic import BaseModel

import hyfi
from conftest import write_tree
from hyfi import plugins
from hyfi.config import BaseConfig, compose, compose_group, instantiate, search_path, to_dict


def test_import_has_no_side_effects():
    # AC3: no resolver, no GlobalHydra, no environment change at import time.
    code = textwrap.dedent(
        """
        import os
        import hydra, hydra.utils, hydra.errors
        from hydra.core.global_hydra import GlobalHydra
        from omegaconf.basecontainer import BaseContainer
        resolvers = set(BaseContainer._resolvers)
        env = dict(os.environ)
        import hyfi, hyfi.cli
        assert set(BaseContainer._resolvers) == resolvers, set(BaseContainer._resolvers) - resolvers
        assert not GlobalHydra.instance().is_initialized()
        assert dict(os.environ) == env
        """
    )
    subprocess.run([sys.executable, "-c", code], check=True)


def test_compose_defaults(project):
    cfg = compose()
    assert isinstance(cfg, DictConfig)
    assert cfg.project.name == "hyfi-project"
    assert cfg.get("workflow") is None  # selected later with workflow=<name>


def test_compose_overrides_and_dotenv(project, monkeypatch):
    (project / ".env").write_text("HYFI_PROJECT_NAME=from-dotenv\nHYFI_PROJECT_ROOT=/kept\n")
    monkeypatch.setenv("HYFI_PROJECT_ROOT", "/already-set")
    cfg = compose(["+extra=1"])
    assert cfg.project.name == "from-dotenv"
    assert cfg.project.root == "/already-set"  # .env never overrides the environment
    assert cfg.extra == 1
    monkeypatch.delenv("HYFI_PROJECT_NAME")
    assert compose(dotenv=False).project.name == "hyfi-project"


def test_plugin_group_is_selectable(project):
    # AC4, first half: a group option shipped by an installed plugin.
    cfg = compose(["workflow=plug"])
    assert cfg.workflow.name == "plug"


@pytest.mark.parametrize("with_primary", [False, True])
def test_user_dir_overrides_plugin(project, with_primary):
    # AC4, second half: the user directory wins over the plugin, primary or not.
    files = {"conf/workflow/plug.yaml": "name: mine\nsteps: []\n"}
    if with_primary:
        files["conf/config.yaml"] = (
            "defaults:\n  - project: default\n  - workflow: null\n  - _self_\nmine: true\n"
        )
    write_tree(project, files)
    cfg = compose(["workflow=plug"])
    assert cfg.workflow.name == "mine"
    assert cfg.get("mine", False) is with_primary


def test_search_path_order(project, tmp_path):
    primary, extras = search_path()
    assert primary == "pkg://hyfi._primary"
    # ghost plugin is not importable, so skipped; HyFI's groups always come last
    assert extras == ["pkg://fakeplug.conf", "pkg://hyfi.conf"]
    (project / "conf").mkdir()
    primary, extras = search_path(plugins=False)
    assert primary == "pkg://hyfi._primary"
    assert extras == [f"file://{(project / 'conf').resolve()}", "pkg://hyfi.conf"]
    explicit = tmp_path / "elsewhere"
    explicit.mkdir()
    (explicit / "app.yaml").write_text("a: 1\n")
    primary, extras = search_path(explicit, "app")
    assert primary == f"file://{explicit.resolve()}"
    assert extras == ["pkg://fakeplug.conf", "pkg://hyfi.conf"]
    assert compose(config_dir=explicit, config_name="app").a == 1


def test_user_dir_overrides_hyfi_defaults_without_primary(project):
    # A user option with the same name as HyFI's wins even with no conf/config.yaml.
    write_tree(project, {"conf/project/default.yaml": "name: mine\nroot: /srv/mine\n"})
    cfg = compose()
    assert cfg.project.name == "mine"
    assert cfg.project.root == "/srv/mine"


def test_plugins_discover(project):
    found = {p.name: p for p in plugins.discover()}
    assert found["fakeplug"].available
    assert found["fakeplug"].distribution == "fakeplug"
    assert not found["ghost"].available
    assert plugins.config_modules() == ["fakeplug.conf"]


class Tokenizer(BaseConfig):
    _config_group_ = "/tokenizer"
    _config_name_ = "simple"

    lowercase: bool = False
    min_len: int = 1


def test_base_config_compose(project):
    tok = Tokenizer.compose()
    assert tok.lowercase is True
    assert tok.min_len == 2
    assert Tokenizer.compose(overrides=["tokenizer.min_len=5"]).min_len == 5


def test_base_config_requires_group():
    class NoGroup(BaseConfig):
        pass

    with pytest.raises(TypeError):
        NoGroup.compose()


def test_compose_group_errors(project):
    write_tree(project, {"conf/scalar/one.yaml": "# @package _global_\nvalue: 1\n"})
    with pytest.raises(ValueError, match="did not compose to a mapping"):
        compose_group("scalar", "one")
    assert compose_group("workflow", "plug").name == "plug"  # group already in defaults


class Point(BaseModel):
    x: int
    y: int = 0


def test_instantiate_and_to_dict():
    p = instantiate({"_target_": "test_config.Point", "x": "3"})
    assert p == Point(x=3)
    assert to_dict(p) == {"x": 3, "y": 0}
    assert instantiate(Point(x=1)) == {"x": 1, "y": 0}  # no _target_: plain data back
    assert to_dict(DictConfig({"a": "${b}", "b": 2})) == {"a": 2, "b": 2}
    assert to_dict(DictConfig({"a": "${b}", "b": 2}), resolve=False) == {"a": "${b}", "b": 2}
    assert to_dict(5) == 5


def test_public_api():
    assert hyfi.__version__
    assert set(hyfi.__all__) <= set(dir(hyfi))
    with pytest.raises(AttributeError):
        _ = hyfi.not_a_thing


@pytest.mark.parametrize("name", ["HyFI", "hyfi_main"])
def test_removed_1x_names_point_to_migration(name):
    # AC8
    with pytest.raises(ImportError, match=r"docs/migration\.md"):
        getattr(hyfi, name)
    out = subprocess.run(
        [sys.executable, "-c", f"from hyfi import {name}"], capture_output=True, text=True
    )
    assert out.returncode != 0
    assert "docs/migration.md" in out.stderr
    assert "HYFI_NEVER_SET" not in os.environ


def test_compose_emits_no_warnings(project):
    # Hydra 1.4 deprecates version_base; compose must not trigger its migration warning.
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        compose()


def test_workspace_interpolation_has_a_real_default(project):
    cfg = compose(["+out=${project.workspace}/out.csv"])
    assert cfg.out == "./workspace/out.csv"
