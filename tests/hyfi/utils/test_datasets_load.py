import unittest
from hyfi.utils.datasets.load import DSLoad
from hyfi.utils.datasets.save import DSSave
import pandas as pd


class TestLoadDataFrame(unittest.TestCase):
    def test_load_dataframe_existing_file(self):
        # Test loading an existing file
        data_file = "data.csv"
        data_dir = "tests/data"
        dataframe = DSLoad.load_dataframe(data_file, data_dir=data_dir)
        self.assertIsNotNone(dataframe)
        self.assertIsInstance(dataframe, pd.DataFrame)

    def test_load_dataframe_nonexistent_file(self):
        # Test loading a nonexistent file
        data_file = "nonexistent.csv"
        data_dir = "tests/data"
        with self.assertRaises(FileNotFoundError):
            DSLoad.load_dataframe(data_file, data_dir=data_dir)

    def test_load_dataframe_with_columns(self):
        # Test loading a file with specific columns
        data_file = "data.csv"
        data_dir = "tests/data"
        columns = ["column1", "column2"]
        dataframe = DSLoad.load_dataframe(data_file, data_dir=data_dir, columns=columns)
        self.assertIsNotNone(dataframe)
        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertListEqual(list(dataframe.columns), columns)

    def test_save_dataframe(self):
        # Test saving a dataframe
        data = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})
        data_file = "saved-data.csv"
        data_dir = "tests/data"
        DSSave.save_dataframe(data, data_file, data_dir=data_dir)
        dataframe = DSLoad.load_dataframe(data_file, data_dir=data_dir)
        self.assertIsNotNone(dataframe)
        self.assertIsInstance(dataframe, pd.DataFrame)
        self.assertListEqual(list(dataframe.columns), list(data.columns))


if __name__ == "__main__":
    unittest.main()
