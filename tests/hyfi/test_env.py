import os
from hyfi.env import PathConfig, DotEnvConfig
from hyfi.utils.env import expand_posix_vars
from pathlib import Path
from pprint import pprint


def test_path_config():
    config = PathConfig()
    pprint(config.dict())
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


def test_dotenv_config():
    os.environ["HYFI_PROJECT_NAME"] = "hyfi"
    os.environ["HYFI_GLOBAL_WORKSPACE_ROOT"] = expand_posix_vars("$WORKSPACE_ROOT")
    config = DotEnvConfig()
    pprint(config.dict())
    # Test that the default values are set correctly
    assert config.config_name == "__init__"
    assert config.HYFI_PROJECT_NAME == "hyfi"


if __name__ == "__main__":
    # test_path_config()
    test_dotenv_config()
