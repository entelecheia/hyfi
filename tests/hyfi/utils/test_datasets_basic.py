import pandas as pd
from hyfi.utils.datasets import DATASETs
from hyfi import HyFI


def test_basics():
    data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    DATASETs.dataframe_drop_columns(data, columns=["a"])
    assert "a" not in data.columns
    HyFI.generate_pipe_config(DATASETs.dataframe_drop_columns)

    data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    DATASETs.dataframe_drop(data, labels=["a"], axis=1)
    assert "a" not in data.columns
    HyFI.generate_pipe_config(DATASETs.dataframe_drop)

    data = pd.DataFrame({"a": ["1,2", "3,4", "5,6"]})
    DATASETs.dataframe_split_str_column(data, column="a", sep=",")
    print(data)
    assert isinstance(data["a"].iloc[0], list)
    HyFI.generate_pipe_config(DATASETs.dataframe_split_str_column)

    data = pd.DataFrame({"a": ["1", "3", "5"], "b": ["2", "4", "6"]})
    DATASETs.dataframe_combine_str_columns(data, columns=["a", "b"], sep=",")
    assert data["a_b"].iloc[0] == "1,2"
    HyFI.generate_pipe_config(DATASETs.dataframe_combine_str_columns)

    data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    DATASETs.dataframe_eval_columns(data, expressions={"c": "a + b"})
    DATASETs.dataframe_eval_columns(data, expressions=["c = a + b"])
    assert data["c"].iloc[0] == 5
    HyFI.generate_pipe_config(DATASETs.dataframe_eval_columns)

    data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    DATASETs.dataframe_eval_columns_with_pd_eval(
        data, expressions={"c": "data.a + data.b"}
    )
    DATASETs.dataframe_eval_columns_with_pd_eval(
        data, expressions=["c = data.a + data.b"]
    )
    print(data)
    DATASETs.dataframe_eval_columns_with_pd_eval(
        data, expressions={"c": "data.a + data.b"}
    )
    print(data)
    assert data["c"].iloc[0] == 5
    HyFI.generate_pipe_config(DATASETs.dataframe_eval_columns_with_pd_eval)

    data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    DATASETs.dataframe_print_head_and_tail(data, num_heads=1, num_tails=1)
    HyFI.generate_pipe_config(DATASETs.dataframe_print_head_and_tail)


if __name__ == "__main__":
    test_basics()
