from hyfi.main import HyFI


def test_pipe_datasets():
    data = HyFI.load_dataset("lhoestq/demo1")["train"]
    print(data)
    assert data is not None
    config = HyFI.compose("pipe=dataset_save_to_disk")
    config.run.update({"dataset_path": "workspace/test_dataset"})
    print(config)
    HyFI.run_pipe(data, HyFI.to_dict(config))
    config = HyFI.compose("pipe=dataset_load_from_disk")
    config.run.update({"dataset_path": "workspace/test_dataset"})
    print(config)
    data2 = HyFI.run_pipe(data, HyFI.to_dict(config))
    print(data2)
    config = HyFI.compose("pipe=dataset_sample")
    config.run.update({"num_samples": 1})
    print(config)
    data3 = HyFI.run_pipe(data, HyFI.to_dict(config))
    print(data3)
    assert len(data3) == 1


if __name__ == "__main__":
    test_pipe_datasets()
