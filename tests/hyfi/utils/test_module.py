from hyfi.utils.packages import PKGs

import inspect


def get_first_caller():
    # Get the bottom frame
    frame = inspect.stack()[-1]

    return frame[3]


# Usage
def foo():
    print(get_first_caller())  # Prints "<module>" if called from the global scope


def test_is_importable():
    assert PKGs.is_importable("hyfi.conf")
    assert not PKGs.is_importable("hyfi.config")
    assert PKGs.is_importable("hyfi.main")


if __name__ == "__main__":
    test_is_importable()
    foo()
