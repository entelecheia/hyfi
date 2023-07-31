from hyfi import HyFI
from hyfi.composer import PipeTargetTypes


def test_generate_config():
    cfg = HyFI.save_hyfi_pipe_config(HyFI.sample_dataset)
    print(cfg)
    cfg = HyFI.save_hyfi_pipe_config(HyFI.save_dataset_to_disk)
    print(cfg)
    cfg = HyFI.save_hyfi_pipe_config(HyFI.load_dataset_from_disk, use_pipe_obj=False)
    print(cfg)


def test_generate_config_for_HyFI():
    cfg = HyFI.save_hyfi_pipe_config(
        HyFI.load_dataframes,
        pipe_target_type=PipeTargetTypes.DATAFRAME_EXTERNAL_FUNCS,
        use_pipe_obj=False,
    )
    print(cfg)
    cfg = HyFI.save_hyfi_pipe_config(
        HyFI.save_dataframes,
        pipe_target_type=PipeTargetTypes.DATAFRAME_EXTERNAL_FUNCS,
        use_pipe_obj=True,
    )
    print(cfg)
    cfg = HyFI.save_hyfi_pipe_config(
        HyFI.load_dataset,
        use_pipe_obj=False,
    )
    print(cfg)
    cfg = HyFI.save_hyfi_pipe_config(
        HyFI.load_data,
        use_pipe_obj=False,
    )
    print(cfg)


if __name__ == "__main__":
    test_generate_config()
    test_generate_config_for_HyFI()
