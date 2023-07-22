from hyfi import global_hyfi


def test_get_version() -> None:
    """
    Test the get_version function.

    version format: major.minor.patch[.devN+g<git hash>]
    """
    version = global_hyfi.version
    # check version format
    assert version.count(".") in range(2, 5)
