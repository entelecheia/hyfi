import os
from hyfi.project import Project
from pathlib import Path
from pprint import pprint


def test_project_config():
    os.environ["HYFI_PROJECT_NAME"] = "hyfi-test"
    config = Project(
        project_root="./workspace/tmp", num_workers=2
    )
    # config.init_project()
    pprint(config.model_dump())
    assert config.project_name == "hyfi-test"
    print(config.workspace_dir)
    assert config.workspace_dir == Path("workspace/tmp/workspace").absolute()
    assert config.num_workers == 2
    # pprint(config.path.model_dump())


if __name__ == "__main__":
    test_project_config()
