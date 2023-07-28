from hyfi import HyFI
from hyfi.pipe.datasets import (
    sample_dataset,
    save_dataset_to_disk,
    load_dataset_from_disk,
)


def test_generate_config():
    cfg = HyFI.save_hyfi_config(sample_dataset)
    print(HyFI.to_yaml(cfg))
    cfg = HyFI.save_hyfi_config(save_dataset_to_disk)
    print(HyFI.to_yaml(cfg))
    cfg = HyFI.save_hyfi_config(load_dataset_from_disk)
    print(HyFI.to_yaml(cfg))


if __name__ == "__main__":
    test_generate_config()
