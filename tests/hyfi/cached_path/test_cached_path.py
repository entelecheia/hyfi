from hyfi.main import HyFI


def test_cached_path_hf() -> None:
    """
    Test the cached_path function with huggingface.
    """
    # check version format
    assert (
        HyFI.cached_path("hf://epwalsh/bert-xsmall-dummy/pytorch_model.bin") is not None
    )
