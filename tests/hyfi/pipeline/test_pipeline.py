import pandas as pd

from hyfi.composer import Composer
from hyfi.main import HyFI
from hyfi.pipeline import PipelineConfig
from hyfi.pipeline.configs import PipeConfig, RunningConfig


def test_running_config():
    assert Composer.generate_alias_for_special_keys("_run_") == "run"
    assert Composer.generate_alias_for_special_keys("_pipe_") == "pipe_target"
    assert Composer.generate_alias_for_special_keys("_with_") == "run"
    assert Composer.generate_alias_for_special_keys("with") == "run"

    config = RunningConfig(**{"with": {"a": 1, "b": 2}})
    print(config.model_dump())
    print(config.run_config)
    assert config.run_config == {"a": 1, "b": 2}


def test_pipe():
    data_path = "https://assets.entelecheia.ai/datasets/bok_minutes/meta-bok_minutes-train.parquet"
    config = HyFI.compose("pipe=_test_dataframes_load")
    config.run.update({"data_files": data_path})
    config.verbose = True
    HyFI.print(config)
    pipe = PipeConfig(**config)
    HyFI.print(pipe.model_dump())
    print(pipe.run_config)
    assert pipe.run_config["_target_"] == "hyfi.main.HyFI.load_dataframes"


def test_pipeline():
    data_path = (
        "https://assets.entelecheia.ai/datasets/esg_coverage/ESG_ratings_raw.csv"
    )
    config = HyFI.compose("pipeline=__test_dataframe__")
    config.pipe1.run.update({"data_files": data_path})
    # HyFI.print(config)
    config = PipelineConfig(**config)
    HyFI.print(config.model_dump(exclude_none=True))
    data = HyFI.run_pipeline(config)
    assert type(data) == pd.DataFrame
    print(data[data.code == "A005930"])


if __name__ == "__main__":
    test_running_config()
    test_pipe()
    test_pipeline()
