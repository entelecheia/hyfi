from pathlib import Path
from typing import List

from hyfi.core import global_hyfi
from hyfi.utils import LOGGING, ENVs

from .model import BaseModel

logger = LOGGING.getLogger(__name__)


class DocGenerator(BaseModel):
    """
    A class for generating reference documentation and configuration documentation.

    This class provides methods for generating reference documentation for modules and configuration documentation for directories.

    Attributes:
        _config_name_: The name of the configuration.
        _config_group_: The group of the configuration.
        config_docs_dirname: The name of the directory for configuration documentation.
        reference_docs_dirname: The name of the directory for reference documentation.
        exclude_configs: A list of configurations to exclude.
        exclude_references: A list of references to exclude.

    Properties:
        root_dir: The root directory.
        package_dir: The package directory.
        package_name: The package name.
        config_dir: The configuration directory.
        config_docs_dir: The directory for configuration documentation.
        reference_docs_dir: The directory for reference documentation.

    Methods:
        generate_reference_docs: Generates reference documentation for modules.
        write_ref_doc: Writes reference documentation for a module.
        generate_config_docs: Generates configuration documentation for directories.
        write_config_doc: Writes configuration documentation for a directory.

    Example:
        ```python
        doc_generator = DocGenerator()
        doc_generator.generate_reference_docs()
        doc_generator.generate_config_docs()
        ```
    """

    _config_name_: str = "__init__"
    _config_group_: str = "/docs"

    config_docs_dirname: str = "docs/configs"
    reference_docs_dirname: str = "docs/reference"

    exclude_configs: List[str] = [
        "docs",
        "hydra",
    ]
    exclude_references: List[str] = [
        "conf",
        "__cli__.py",
        "__click__.py",
        "__init__.py",
        "_version.py",
        "__pycache__",
    ]

    def __call__(self) -> None:
        self.generate_config_docs()
        self.generate_reference_docs()

    @property
    def root_dir(self) -> Path:
        return Path(ENVs.getcwd())

    @property
    def package_dir(self) -> Path:
        return Path(global_hyfi.package_path)

    @property
    def package_name(self) -> str:
        return global_hyfi.package_name

    @property
    def config_dir(self) -> Path:
        return self.package_dir / global_hyfi.config_dirname

    @property
    def config_docs_dir(self) -> Path:
        path_ = self.root_dir / self.config_docs_dirname
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    @property
    def reference_docs_dir(self) -> Path:
        path_ = self.root_dir / self.reference_docs_dirname
        path_.mkdir(parents=True, exist_ok=True)
        return path_

    def generate_reference_docs(self):
        exclude_refs = self.exclude_references or []
        logger.info("Generating reference documentation excluding %s", exclude_refs)
        for _path in self.package_dir.iterdir():
            module_name = _path.name
            if _path.is_file() or module_name in exclude_refs:
                continue
            self.write_ref_doc(_path)
            # for file in _path.iterdir():
            #     if file.name in exclude_refs:
            #         continue
            #     self.write_ref_doc(file)

    def write_ref_doc(self, module_path: Path):
        module_name = module_path.relative_to(self.package_dir)
        if module_path.is_dir():
            ref_file = self.reference_docs_dir / str(module_name) / "index.md"
        else:
            module_name = module_name.with_suffix("")
            ref_file = self.reference_docs_dir / f"{module_name}.md"
        module_name = module_name.as_posix().replace("/", ".")
        module_name = f"{self.package_name}.{module_name}"
        ref_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(
            "Writing reference documentation for %s to %s", module_name, ref_file
        )
        with open(ref_file, "w") as f:
            f.write(f"# `{module_name}`\n\n")
            f.write(f"::: {module_name}\n")

    def generate_config_docs(self):
        exclude_configs = self.exclude_configs or []
        logger.info(
            "Generating configuration documentation excluding %s", exclude_configs
        )
        for config_path in sorted(self.config_dir.iterdir()):
            if (
                config_path.is_file()
                or config_path.name in exclude_configs
                or config_path.name.startswith("__")
            ):
                continue
            self.write_config_doc(config_path)

    def write_config_doc(self, config_path: Path):
        dirname = config_path.name
        output_file = self.config_docs_dir / f"{dirname}.md"
        logger.info(
            "Writing configuration documentation for %s to %s", dirname, output_file
        )
        with open(output_file, "w") as f:
            f.write(f"# {dirname}\n\n")
            f.write(f"Config location: `conf/{dirname}`\n\n")
            for file in sorted(config_path.iterdir()):
                if file.is_dir():
                    continue
                if file.suffix == ".yaml":
                    f.write(f"## `{file.name}`\n\n")
                    f.write("```yaml\n")
                    lvl = self.config_docs_dir.relative_to(self.root_dir)
                    lvl = "/".join([".."] * len(lvl.as_posix().split("/")))
                    rel_path = f"{lvl}/{file.relative_to(self.root_dir)}"
                    f.write("{% include '" + str(rel_path) + "' %}")
                    f.write("\n```\n\n")
