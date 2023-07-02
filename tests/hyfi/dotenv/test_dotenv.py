import os
from hyfi.dotenv import DotEnvConfig
from hyfi.utils.envs import ENVs
from pprint import pprint


def test_dotenv_config():
    os.environ["HYFI_PROJECT_NAME"] = "hyfi"
    os.environ["HYFI_GLOBAL_ROOT"] = ENVs.expand_posix_vars("$WORKSPACE_ROOT")
    os.environ["HYFI_VERBOSE"] = "True"
    config = DotEnvConfig()
    print(type(config))
    pprint(config.model_dump())
    # Test that the default values are set correctly
    assert config._config_name_ == "__init__"
    assert config.HYFI_PROJECT_NAME == "hyfi"


if __name__ == "__main__":
    test_dotenv_config()
