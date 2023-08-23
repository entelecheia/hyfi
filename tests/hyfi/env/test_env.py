import os
from hyfi.env import Env, ProjectEnv
from hyfi.utils.envs import ENVs
from pprint import pprint


def test_env_config():
    os.environ["HYFI_PROJECT_NAME"] = "hyfi"
    os.environ["HYFI_GLOBAL_ROOT"] = ENVs.expand_posix_vars("$WORKSPACE_ROOT")
    os.environ["HYFI_VERBOSE"] = "True"
    config = Env()
    print(type(config))
    pprint(config.model_dump())
    # Test that the default values are set correctly
    assert config._config_name_ == "__init__"
    assert config.HYFI_PROJECT_NAME == "hyfi"
    assert config.os["HYFI_PROJECT_NAME"] == "hyfi"
    print(config.DOTENV_FILE)


def test_projectenv_config():
    os.environ["HYFI_PROJECT_NAME"] = "hyfi"
    os.environ["HYFI_VERBOSE"] = "True"
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "all")
    config = ProjectEnv()
    print(type(config))
    pprint(config.model_dump())
    # Test that the default values are set correctly
    assert config._config_name_ == "__project__"
    assert config.CUDA_VISIBLE_DEVICES == "all"
    config.CUDA_VISIBLE_DEVICES == "all"
    print(config.OPENAI_API_KEY.get_secret_value())


if __name__ == "__main__":
    test_env_config()
    test_projectenv_config()
