from hyfi.path import PathConfig
from hyfi.utils.env import expand_posix_vars
from pathlib import Path
from pprint import pprint


def test_path_config():
    config = PathConfig(project_root="./tmp")
    pprint(config.dict())
    # Test that the default values are set correctly
    assert config.config_name == "__init__"
    assert config.home == expand_posix_vars("$HOME")
    assert config.global_hyfi_root == expand_posix_vars("$HOME/.hyfi")
    assert config.global_workspace_root == expand_posix_vars("$HOME/.hyfi/workspace")
    assert Path(config.project_root).absolute() == (Path.cwd() / "tmp").absolute()
    assert (
        Path(config.project_workspace_root).absolute()
        == Path.cwd().absolute() / "tmp/workspace"
    )

    # Test that the log_dir and cache_dir properties return the correct values
    assert Path(config.log_dir).is_dir()
    assert Path(config.cache_dir).is_dir()


if __name__ == "__main__":
    test_path_config()
