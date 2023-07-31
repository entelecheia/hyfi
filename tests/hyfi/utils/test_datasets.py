from hyfi.main import HyFI
from pathlib import Path
from datasets.arrow_dataset import Dataset
from datasets.dataset_dict import DatasetDict


def test_datasets():
    """Test datasets"""
    dset = HyFI.load_dataset("lhoestq/demo1")
    print(type(dset))
    print(dset)
    assert isinstance(dset, DatasetDict)
    data = HyFI.sample_dataset(dset, num_samples=1, split="train")
    print(data)
    assert isinstance(data, Dataset)
    HyFI.save_dataset_to_disk(data, "workspace/tmp/demo1")
    data = HyFI.load_dataset_from_disk("workspace/tmp/demo1")
    print(data)
    print(type(data))
    HyFI.save_dataset_to_disk(dset, "workspace/tmp/demo2", verbose=True)
    data = HyFI.load_dataset_from_disk("workspace/tmp/demo2", verbose=True)
    print(data)
    print(type(data))


def test_dataframe_load_and_save():
    """Test dataframe loading"""
    data_path = "https://assets.entelecheia.ai/datasets/bok_minutes/meta-bok_minutes-train.parquet"
    df = HyFI.load_data(data_files=data_path, use_cached=False)
    assert df is not None
    print(df)
    # assert df.shape == (10, 2)
    HyFI.save_dataframes(df, "workspace/tmp/meta-test.parquet")


def test_data_load_and_concat():
    dataset = HyFI.load_data("glue", "mrpc")
    print(dataset)
    ds = dataset["train"].to_pandas()
    ds["text"] = ds["sentence1"] + ds["sentence2"]
    print(ds.head())
    _path = HyFI.cached_path(
        "https://assets.entelecheia.ai/datasets/bok_minutes.zip",
        extract_archive=True,
    )
    print(_path)
    data_path = Path(str(_path)) / "bok_minutes" / "bok_minutes-train.parquet"
    data = HyFI.load_data(data_files=data_path)
    df = data["train"]
    concated_data = HyFI.concatenate_data([df["text"], ds["text"]])
    print(concated_data.head())
    print(concated_data.tail())


if __name__ == "__main__":
    test_datasets()
    # test_dataframe_load_and_save()
    # test_data_load_and_concat()
