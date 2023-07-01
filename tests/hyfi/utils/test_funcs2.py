import unittest
from datetime import datetime
from hyfi.utils.funcs import FUNCs


class TestFUNCs(unittest.TestCase):
    def test_any_to_utf8(self):
        # Test that any_to_utf8 returns a utf-8 encoded string
        b = b"hello world"
        self.assertEqual(FUNCs.any_to_utf8(b), "hello world")

    def test_today(self):
        # Test that today returns a string in the format "%Y-%m-%d"
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertEqual(FUNCs.today(), today)

    def test_now(self):
        # Test that now returns a string in the format "%Y-%m-%d %H:%M:%S"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(FUNCs.now(), now)

    def test_strptime(self):
        # Test that strptime returns a datetime object
        date_str = "2022-01-01"
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        self.assertEqual(FUNCs.strptime(date_str), date_obj)

    def test_to_dateparm(self):
        # Test that to_dateparm returns a string in the format "%Y-%m-%d"
        date_obj = datetime.strptime("2022-01-01", "%Y-%m-%d")
        self.assertEqual(
            FUNCs.to_dateparm(date_obj), "${to_datetime:2022-01-01,%Y-%m-%d}"
        )

    def test_human_readable_type_name(self):
        # Test that human_readable_type_name returns a string representation of a type
        self.assertEqual(FUNCs.human_readable_type_name(int), "int")

    def test_readable_types_list(self):
        # Test that readable_types_list returns a comma-separated string of type names
        types = [int, str, bool]
        self.assertEqual(FUNCs.readable_types_list(types), "int, str, bool")

    def test_dict_product(self):
        # Test that dict_product returns a list of dictionaries
        dicts = {"a": [1, 2], "b": [3, 4]}
        products = [
            {"a": 1, "b": 3},
            {"a": 1, "b": 4},
            {"a": 2, "b": 3},
            {"a": 2, "b": 4},
        ]
        self.assertEqual(FUNCs.dict_product(dicts), products)

    def test_printf(self):
        # Test that printf returns a string
        action = "test"
        msg = "hello world"
        self.assertIsInstance(FUNCs.printf(action, msg), str)

    def test_printf_exception(self):
        # Test that printf_exception prints to stderr
        svar: str = "test"
        try:
            svar += 1
        except Exception:
            FUNCs.printf_exception(Exception("test"), "test", quiet=True)

    def test_cast_str_to_bool(self):
        # Test that cast_str_to_bool returns a boolean
        self.assertIsInstance(FUNCs.cast_str_to_bool("True"), bool)

    def test_force_str_end(self):
        # Test that force_str_end returns a string ending with "\n"
        original_str = "hello world"
        self.assertEqual(FUNCs.force_str_end(original_str), "hello world\n")
