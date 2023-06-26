import os
from hyfi.project import ProjectConfig
from pathlib import Path
from pprint import pprint


def test_project_config():
    os.environ["HYFI_PROJECT_NAME"] = "hyfi"
    config = ProjectConfig(project_name="test", project_root="./workspace/tmp", num_workers=2)
    # config.init_project()
    pprint(config.dict())
    assert config.project_name == "test"
    assert Path(config.project_root).absolute() == (Path.cwd() / "workspace/workspacetmp").absolute()
    assert config.num_workers == 2
    # pprint(config.path.dict())


if __name__ == "__main__":
    test_project_config()
