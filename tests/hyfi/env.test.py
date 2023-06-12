from hyfi.env import PathConfig
from hyfi.utils.env import expand_posix_vars
from pathlib import Path


def test_path_config():
    config = PathConfig()
    print(config.dict())
    # Test that the default values are set correctly
    assert config.config_name == "__init__"
    assert config.home == expand_posix_vars("$HOME")
    assert config.global_workspace_root == expand_posix_vars("$HOME/.hyfi")
    assert config.global_data_root == expand_posix_vars("$HOME/.hyfi/data")
    assert Path(config.project_root).absolute() == Path.cwd().absolute()
    assert (
        Path(config.project_data_root).absolute() == Path.cwd().absolute() / "workspace"
    )

    # Test that the log_dir and cache_dir properties return the correct values
    assert Path(config.log_dir).is_dir()
    assert Path(config.cache_dir).is_dir()


if __name__ == "__main__":
    test_path_config()
