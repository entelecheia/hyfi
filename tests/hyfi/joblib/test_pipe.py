from hyfi.main import HyFI


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
    pipe_config = HyFI.compose("pipe=__init__")
    pipe_config._method_ = "filter"
    pipe_config.apply_to = ""
    pipe_config.rcParams = {"items": ["text"]}
    pipe_config.verbose = True
    print(pipe_config)
    df4 = HyFI.pipe(df, pipe_config)
    print(df4)
    print(df4["text"].str.replace("Economic", "ECON").head())


if __name__ == "__main__":
    test_pipe()
