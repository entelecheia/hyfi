from pydantic import BaseModel


class DirnamesConfig(BaseModel):
    _config_name_: str = "__init__"
    _config_group_: str = "path/dirnames"
    # directory names
    inputs: str = "inputs"
    outputs: str = "outputs"
    archive: str = "archive"
    datasets: str = "datasets"
    models: str = "models"
    modules: str = "modules"
    library: str = "libs"
    logs: str = "logs"
    cache: str = ".cache"
    tmp: str = "tmp"
