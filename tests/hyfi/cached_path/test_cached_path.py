from hyfi.main import HyFI


def test_cached_path_hf() -> None:
    """
    Test the cached_path function with huggingface.
    """
    # check version format
    assert (
        HyFI.cached_path("hf://epwalsh/bert-xsmall-dummy/pytorch_model.bin") is not None
    )


def test_cached_path_http() -> None:
    """
    Test the cached_path function with http.
    """
    # check version format
    assert (
        HyFI.cached_path(
            "https://github.com/entelecheia/ekorpkit-book/raw/main/assets/data/bok_minutes.zip",
            extract_archive=True,
        )
        is not None
    )
