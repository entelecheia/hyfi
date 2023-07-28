import pytest
from hyfi.composer.utils import get_obj_path
from hyfi.composer import Composer


@pytest.mark.parametrize(
    "obj, expected",
    [
        # Test objects with __name__ attribute
        (int, "builtins.int"),
        # Test objects with __module__ and __qualname__ attributes
        (Composer, "hyfi.composer.composer.Composer"),
        (Composer.compose, "hyfi.composer.composer.compose"),
        # Test objects without __module__ attribute but with __qualname__ attribute
        (Composer.print_config, "hyfi.composer.composer.print_config"),
    ],
)
def test_get_obj_path(obj, expected):
    """
    Test get_obj_path function.
    """
    # Act
    result = get_obj_path(obj)
    print(result)
    # Assert
    assert result == expected


def test_function():
    pass


if __name__ == "__main__":
    pytest.main([__file__])
