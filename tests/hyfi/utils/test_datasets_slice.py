import pandas as pd
from hyfi.utils.datasets import DATASETs
from hyfi import HyFI


def test_slice():
    data = pd.DataFrame({"text": ["hello world", "hello", "world"]})
    rst = DATASETs.split_dataframe(data, indices_or_sections=2)
    assert len(rst) == 2
    HyFI.generate_pipe_config(DATASETs.split_dataframe)


if __name__ == "__main__":
    test_slice()
