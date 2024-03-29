from hyfi import global_hyfi
from hyfi import HyFI


def test_get_version() -> None:
    """
    Test the get_version function.

    version format: major.minor.patch[.devN+g<git hash>]
    """
    version = global_hyfi.version
    # check version format
    assert version.count(".") in range(2, 5)


def test_init():
    HyFI.initialize_global_hyfi(package_path="src/hyfi", version="0.0.1")
    global_hyfi.initialize(
        package_path="src/hyfi", version="0.0.1", plugins=["hyfi", "lexikanon"]
    )
    print(global_hyfi.plugins)
    HyFI.print_about()


if __name__ == "__main__":
    test_get_version()
    test_init()
