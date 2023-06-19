from hyfi.main import HyFI
from pathlib import Path


def test_dataframe_load_and_save():
    """Test dataframe loading"""
    _path = HyFI.cached_path(
        "https://github.com/entelecheia/ekorpkit-book/raw/main/assets/data/bok_minutes.zip",
        extract_archive=True,
    )
    print(_path)
    data_path = Path(str(_path)) / "bok_minutes" / "bok_minutes-train.parquet"
    df = HyFI.load_data(data_path)
    assert df is not None
    print(df.head())
    # assert df.shape == (10, 2)
    HyFI.save_data(df, "tmp/test.parquet")


if __name__ == "__main__":
    test_dataframe_load_and_save()
