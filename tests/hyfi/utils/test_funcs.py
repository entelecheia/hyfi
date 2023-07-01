from hyfi.utils.funcs import FUNCs


def test_lower_case_with_underscores():
    assert FUNCs.lower_case_with_underscores("CamelCased") == "camel_cased"
    assert FUNCs.lower_case_with_underscores("Camel Cased") == "camel_cased"
    assert FUNCs.lower_case_with_underscores("Camel-Cased") == "camel_cased"


def test_ordinal():
    assert FUNCs.ordinal(1) == "1st"
    assert FUNCs.ordinal(2) == "2nd"
    assert FUNCs.ordinal(3) == "3rd"
    assert FUNCs.ordinal(4) == "4th"
    assert FUNCs.ordinal(11) == "11th"
    assert FUNCs.ordinal(12) == "12th"
    assert FUNCs.ordinal(13) == "13th"
    assert FUNCs.ordinal(14) == "14th"


def test_get_offset_ranges():
    assert FUNCs.get_offset_ranges(10, 2) == [0, 6, 11]
    assert FUNCs.get_offset_ranges(100, 5) == [0, 21, 41, 61, 81, 101]


def test_humanbytes():
    assert FUNCs.humanbytes(1023) == "1023.0 Byte"
    assert FUNCs.humanbytes(1024) == "1.00 KiB"
    assert FUNCs.humanbytes(1024**2) == "1.00 MiB"
    assert FUNCs.humanbytes(1024**3) == "1.00 GiB"
    assert FUNCs.humanbytes(1024**4) == "1.00 TiB"


def test_parse_size():
    assert FUNCs.parse_size("16K") == 16 * 1024
    assert FUNCs.parse_size("1M") == 1024**2
    assert FUNCs.parse_size("1G") == 1024**3
    assert FUNCs.parse_size("1T") == 1024**4


def test_unescape_dict():
    d = {"a": 1, "b": "hello\\nworld"}
    assert FUNCs.unescape_dict(d) == {"a": 1, "b": "hello\nworld"}
