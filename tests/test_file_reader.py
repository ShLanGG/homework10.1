import unittest
from unittest.mock import patch, mock_open
import pandas as pd
from src.file_reader import read_csv_file, read_excel_file


class TestFileReader(unittest.TestCase):
    @patch("pandas.read_csv")
    def test_read_csv_file(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame([{"id": 1, "amount": 100}])
        result = read_csv_file("dummy_path.csv")
        self.assertEqual(result, [{"id": 1, "amount": 100}])

    @patch("pandas.read_excel")
    def test_read_excel_file(self, mock_read_excel):
        mock_read_excel.return_value = pd.DataFrame([{"id": 1, "amount": 200}])
        result = read_excel_file("dummy_path.xlsx")
        self.assertEqual(result, [{"id": 1, "amount": 200}])