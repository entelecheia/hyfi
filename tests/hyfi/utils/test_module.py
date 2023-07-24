from hyfi.utils.packages import PKGs


def test_is_importable():
    assert PKGs.is_importable("hyfi.conf")
    assert not PKGs.is_importable("hyfi.config")
    assert PKGs.is_importable("hyfi.main")


if __name__ == "__main__":
    test_is_importable()
