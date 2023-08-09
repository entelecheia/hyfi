import pandas as pd
import pytest
from hyfi.utils.datasets import DATASETs


@pytest.fixture
def data():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "text": [
                "Lorem ipsum",
                "dolor sit amet",
                "consectetur adipiscing elit",
                "sed do eiusmod",
                "tempor incididunt",
            ],
            "length": [11, 15, 24, 14, 19],
        }
    )


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "id": [1, 3, 5],
            "text": ["Lorem ipsum", "consectetur adipiscing elit", "tempor incididunt"],
            "length": [11, 24, 19],
        }
    )


@pytest.fixture
def train_data():
    return pd.DataFrame(
        {"id": [2, 4], "text": ["dolor sit amet", "sed do eiusmod"], "length": [15, 14]}
    )


@pytest.fixture
def discard_data():
    return pd.DataFrame({"id": [], "text": [], "length": []})


def test_filter_and_sample_data_with_queries(
    data, sample_data, train_data, discard_data
):
    queries = ["length > 13", "length < 16"]
    output_dir = "workspace/datasets/test_funcs"
    sample_filename = "sample.parquet"
    train_filename = "train.parquet"
    discard_filename = "discard.parquet"
    verbose = True

    result = DATASETs.filter_and_sample_data(
        data,
        queries,
        output_dir=output_dir,
        sample_filename=sample_filename,
        train_filename=train_filename,
        discard_filename=discard_filename,
        verbose=verbose,
    )
    assert result is not None


def test_filter_and_sample_data_without_queries(
    data, sample_data, train_data, discard_data
):
    output_dir = "workspace/datasets/test_funcs"
    sample_filename = "sample.parquet"
    train_filename = "train.parquet"
    discard_filename = "discard.parquet"
    verbose = True

    result = DATASETs.filter_and_sample_data(
        data,
        output_dir=output_dir,
        sample_filename=sample_filename,
        train_filename=train_filename,
        discard_filename=discard_filename,
        verbose=verbose,
    )

    assert result is not None


def test_filter_and_sample_data_with_sample_size(
    data, sample_data, train_data, discard_data
):
    sample_size = 2
    output_dir = "workspace/datasets/test_funcs"
    sample_filename = "sample.parquet"
    train_filename = "train.parquet"
    discard_filename = "discard.parquet"
    verbose = True

    result = DATASETs.filter_and_sample_data(
        data,
        sample_size=sample_size,
        output_dir=output_dir,
        sample_filename=sample_filename,
        train_filename=train_filename,
        discard_filename=discard_filename,
        verbose=verbose,
    )

    assert len(result) == len(data)


def test_filter_and_sample_data_with_sample_size_zero(
    data, sample_data, train_data, discard_data
):
    sample_size = 0
    output_dir = "workspace/datasets/test_funcs"
    sample_filename = "sample.parquet"
    train_filename = "train.parquet"
    discard_filename = "discard.parquet"
    verbose = True

    result = DATASETs.filter_and_sample_data(
        data,
        sample_size=sample_size,
        output_dir=output_dir,
        sample_filename=sample_filename,
        train_filename=train_filename,
        discard_filename=discard_filename,
        verbose=verbose,
    )

    assert len(result) == 5
