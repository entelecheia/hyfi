import pandas as pd

from hyfi.main import HyFI
from hyfi.pipeline import PipelineConfig
from hyfi.pipeline.configs import PipeConfig, RunningConfig


def test_running_config():
    config = RunningConfig(**{"with": {"a": 1, "b": 2}})
    print(config.dict())
    assert config.kwargs == {"a": 1, "b": 2}


def test_pipe():
    data_path = "https://assets.entelecheia.ai/datasets/bok_minutes/meta-bok_minutes-train.parquet"
    config = HyFI.compose("pipe=load_dataframes")
    config._with_ = {"data_files": data_path}
    config.verbose = True
    HyFI.print(config)
    pipe = PipeConfig(**config)
    HyFI.print(pipe.dict())
    print(pipe.kwargs)
    assert pipe._run_ == "hyfi.main.HyFI.load_dataframes"


def test_pipeline():
    data_path = (
        "https://assets.entelecheia.ai/datasets/esg_coverage/ESG_ratings_raw.csv"
    )
    config = HyFI.compose("pipeline=__test_dataframe__")
    config.pipe1._with_ = {"data_files": data_path}
    config = PipelineConfig(**config)
    HyFI.print(config.dict(exclude_none=True))
    data = HyFI.run_pipeline(config)
    assert type(data) == pd.DataFrame
    print(data[data.code == "A005930"])


if __name__ == "__main__":
    test_running_config()
    test_pipe()
    test_pipeline()
