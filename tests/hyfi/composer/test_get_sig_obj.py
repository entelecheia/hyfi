import pytest
from hyfi.composer.utils import get_sig_obj


# Arrange
class NoMethodsClass:
    pass


class InitOnlyClass:
    def __init__(self):
        pass


class TestClass:
    def __new__(cls):
        pass


class TestClassInit:
    def __init__(self):
        pass


def test_get_sig_obj_non_class():
    """
    Test get_sig_obj function with a non-class target.
    """
    # Arrange
    target = lambda x: x

    # Act
    result = get_sig_obj(target)

    # Assert
    assert result == target


def test_get_sig_obj_with_new():
    """
    Test get_sig_obj function with a class target that has __new__ method.
    """
    # Arrange
    target = TestClass

    # Act
    result = get_sig_obj(target)

    # Assert
    assert result == target.__new__


def test_get_sig_obj_with_init():
    """
    Test get_sig_obj function with a class target that has __init__ method.
    """
    # Arrange
    target = TestClassInit

    # Act
    result = get_sig_obj(target)
    print(result)
    # Assert
    assert result == target.__init__


def test_get_sig_obj_with_parent_new():
    """
    Test get_sig_obj function with a class target that has parent class with __new__ method.
    """

    # Arrange
    class ChildClass(TestClass):
        pass

    target = ChildClass

    # Act
    result = get_sig_obj(target)
    print(result)

    # Assert
    assert result == target.__new__


def test_get_sig_obj_with_init_only():
    """
    Test get_sig_obj function with a class target that has only __init__ method.
    """

    # Arrange
    target = InitOnlyClass

    # Act
    result = get_sig_obj(target)

    # Assert
    assert result == target.__init__


if __name__ == "__main__":
    pytest.main([__file__])
