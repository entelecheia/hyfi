from hyfi.path import ProjectPathConfig
from hyfi.utils.envs import ENVs
from pathlib import Path
from pprint import pprint


def test_path_config():
    config = ProjectPathConfig(
        project_root="workspace/tmp",
        global_hyfi_root=ENVs.expand_posix_vars("$HOME/.hyfi"),
        project_workspace_name="testspace",
    )
    pprint(config.model_dump())
    # Test that the default values are set correctly
    assert config._config_name_ == "__project__"
    assert config.home == ENVs.expand_posix_vars("$HOME")
    assert (
        Path(config.project_root).absolute()
        == (Path.cwd() / "workspace/tmp").absolute()
    )
    assert config.workspace_dir == Path("workspace/tmp/testspace")

    # Test that the log_dir and cache_dir properties return the correct values
    assert Path(config.log_dir).is_dir()
    assert Path(config.cache_dir).is_dir()
    config.project_name = "newproject"
    config.print_config()
    print(config.config_jsonpath)
    assert config.config_filepath == Path(
        "workspace/tmp/testspace/configs/newproject_config.yaml"
    )


if __name__ == "__main__":
    test_path_config()
