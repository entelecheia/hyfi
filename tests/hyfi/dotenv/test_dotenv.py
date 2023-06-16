import os
from hyfi.dotenv import DotEnvConfig
from hyfi.utils.env import expand_posix_vars
from pprint import pprint


def test_dotenv_config():
    os.environ["HYFI_PROJECT_NAME"] = "hyfi"
    os.environ["HYFI_GLOBAL_ROOT"] = expand_posix_vars("$WORKSPACE_ROOT")
    config = DotEnvConfig()
    pprint(config.dict())
    # Test that the default values are set correctly
    assert config.config_name == "__init__"
    assert config.HYFI_PROJECT_NAME == "hyfi"


if __name__ == "__main__":
    test_dotenv_config()
