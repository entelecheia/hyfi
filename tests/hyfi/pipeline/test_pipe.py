from hyfi.main import HyFI
from hyfi.pipeline import DataframePipe


def test_pipe():
    """Test dataframe loading"""
    data_path = (
        "https://assets.entelecheia.ai/datasets/bok_minutes/bok_minutes-train.parquet"
    )
    df = HyFI.load_data(data_files=data_path, use_cached=False)["train"]
    assert df is not None
    df2 = HyFI.apply(
        lambda x: x.lower(),
        df["text"],
        "lowercase",
        use_batcher=False,
        num_workers=10,
    )
    print(df2)
    df3 = HyFI.apply(
        lambda x: x.upper(),
        df["text"],
        "lowercase",
        use_batcher=True,
        num_workers=10,
    )
    print(df3)
    config = HyFI.compose("pipe=__dataframe_instance_methods__")
    pipe_config = DataframePipe(**config)
    pipe_config.run = {"_target_": "filter", "items": ["id"]}
    print(pipe_config)
    df4 = HyFI.run_pipe(df, pipe_config)
    print(df4)


if __name__ == "__main__":
    test_pipe()
