from pydantic import BaseModel


class DirnamesConfig(BaseModel):
    _config_name_: str = "__init__"
    _config_group_: str = "path/dirnames"
    # directory names
    inputs: str = "inputs"
    outputs: str = "outputs"
    archives: str = "archives"
    datasets: str = "datasets"
    models: str = "models"
    modules: str = "modules"
    library: str = "libs"
    logs: str = "logs"
    cache: str = ".cache"
    tmp: str = "tmp"
    # to reuse the same config file for different runs
    configs: str = "configs"
    config_yaml: str = "config.yaml"
    config_json: str = "config.json"
