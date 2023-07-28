from hyfi import HyFI
from hyfi.pipe.datasets import (
    sample_dataset,
    save_dataset_to_disk,
    load_dataset_from_disk,
)


def test_generate_config():
    cfg = HyFI.save_hyfi_pipe_config(sample_dataset)
    print(cfg)
    cfg = HyFI.save_hyfi_pipe_config(save_dataset_to_disk)
    print(cfg)
    cfg = HyFI.save_hyfi_pipe_config(load_dataset_from_disk, use_pipe_obj=False)
    print(cfg)


if __name__ == "__main__":
    test_generate_config()
