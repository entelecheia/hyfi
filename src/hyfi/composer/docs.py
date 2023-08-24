# TODO: #209 add functionality to generate documentation for configs and models automatically
from pathlib import Path
from typing import List

from hyfi.core import global_hyfi

from .model import BaseModel


class DocGenerator(BaseModel):
    _config_name_: str = "__init__"
    _config_group_: str = "/docs"

    config_docs_dir: str = "docs/configs"

    exclude_configs: List[str] = []

    @property
    def config_dir(self) -> Path:
        return Path(global_hyfi.package_path) / global_hyfi.config_dirname

    @property
    def config_docs_dir(self) -> Path:
        path_ = Path().cwd() / self.config_docs_dir
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    def generate_config_docs(self):
        exclude_configs = self.exclude_configs or []
        for _path in self.config_dir.iterdir():
            dirname = _path.name
            if (
                _path.is_file()
                or dirname in exclude_configs
                or dirname.startswith("__")
            ):
                continue
            output_file = self.config_docs_dir / f"{dirname}.md"
            with open(output_file, "w") as f:
                f.write(f"# {dirname}\n\n")
                f.write(f"Config location: `conf/{dirname}`\n\n")
                for file in sorted(_path.iterdir()):
                    if file.suffix == ".yaml":
                        f.write(f"## `{file}`\n\n")
                        f.write("```yaml\n")
                        rel_file = file.relative_to(self.config_docs_dir)
                        f.write("{% include '" + str(rel_file) + " %}")
                        f.write("\n```\n\n")
