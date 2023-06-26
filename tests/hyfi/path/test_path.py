from hyfi.path import PathConfig
from hyfi.utils.envs import ENVs
from pathlib import Path
from pprint import pprint


def test_path_config():
    config = PathConfig(
        project_root="tmp",
        global_hyfi_root=ENVs.expand_posix_vars("$HOME/.hyfi"),
        project_workspace_name="testspace",
    )
    pprint(config.dict())
    # Test that the default values are set correctly
    assert config.config_name == "__init__"
    assert config.home == ENVs.expand_posix_vars("$HOME")
    assert Path(config.project_root).absolute() == (Path.cwd() / "tmp").absolute()
    assert (
        Path(config.project_workspace_root).absolute()
        == Path.cwd().absolute() / "tmp/testspace"
    )

    # Test that the log_dir and cache_dir properties return the correct values
    assert Path(config.log_dir).is_dir()
    assert Path(config.cache_dir).is_dir()


if __name__ == "__main__":
    test_path_config()
