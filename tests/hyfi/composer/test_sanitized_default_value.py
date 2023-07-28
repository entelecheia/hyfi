import pytest
from hyfi.composer.generator import sanitized_default_value


@pytest.mark.parametrize(
    "value, expected",
    [
        # Test common primitives
        (None, None),
        ("string", "string"),
        (123, 123),
        (True, True),
        (3.14, 3.14),
        # Test non-str collection
        ([1, 2, 3], [1, 2, 3]),
        ((1, 2, 3), (1, 2, 3)),
        ({1, 2, 3}, None),
        ({1: "one", 2: "two"}, {1: "one", 2: "two"}),
        # Test importable callable
        (str.upper, None),
        (list.append, None),
        (dict.fromkeys, {"_target_": "None.fromkeys", "iterable": None, "value": None}),
        # Test unsupported types
        (object(), None),
        (lambda x: x, {"_target_": "test_sanitized_default_value.<lambda>", "x": None}),
    ],
)
def test_sanitized_default_value(value, expected):
    """
    Test sanitized_default_value function.
    """
    # Act
    result = sanitized_default_value(value)
    print(result)

    # Assert
    assert result == expected


if __name__ == "__main__":
    pytest.main([__file__])
