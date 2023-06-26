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
    config = HyFI.compose("pipe=__dataframe_instance_methods__")
    pipe_config = HyFI.pipe_config(**config)
    pipe_config.run._target_ = "filter"
    pipe_config.run._with_ = {"items": ["id"]}
    pipe_config.verbose = True
    print(pipe_config)
    df4 = HyFI.run_pipe(df, pipe_config)
    print(df4)
    config = HyFI.compose("pipe=__dataframe_external_funcs__")
    pipe_config = HyFI.pipe_config(**config)
    pipe_config.run._target_ = "lambda x: x.replace('Economic', 'ECON')"
    pipe_config.run.columns_to_apply = "text"
    pipe_config.run.num_workers = 5
    pipe_config.verbose = True
    print(pipe_config)
    df5 = HyFI.run_pipe(df, pipe_config)
    print(df5)


if __name__ == "__main__":
    test_pipe()
