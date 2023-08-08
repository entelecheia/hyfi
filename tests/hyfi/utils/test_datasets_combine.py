import pandas as pd
from hyfi.utils.datasets import DATASETs
from hyfi import HyFI


def test_combine():
    df1 = pd.DataFrame({"id": [0, 1, 2], "a": [1, 2, 3]})
    df2 = pd.DataFrame({"id": [1, 2, 4], "b": [4, 5, 6]})
    df = DATASETs.merge_dataframes(df1, df2, on="id", how="outer")
    print(df)
    assert df["a"].iloc[0] == 1 and df["b"].iloc[1] == 4
    df = DATASETs.merge_dataframes(df1, df2, on="id", how="inner")
    print(df)
    assert df["a"].iloc[0] == 2 and df["b"].iloc[1] == 5
    df = DATASETs.merge_dataframes(df1, df2, on="id", how="left")
    print(df)
    assert df["a"].iloc[0] == 1 and df["b"].iloc[1] == 4
    df = DATASETs.merge_dataframes(df1, df2, on="id", how="right")
    print(df)
    assert df["a"].iloc[0] == 2 and df["b"].iloc[1] == 5
    HyFI.generate_pipe_config(DATASETs.merge_dataframes)


if __name__ == "__main__":
    test_combine()
