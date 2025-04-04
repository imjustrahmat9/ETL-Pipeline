import unittest
from unittest.mock import patch, MagicMock
from utils.load import save_to_csv, save_to_existing_google_sheet, save_to_postgresql
import os


class TestLoad(unittest.TestCase):
    def setUp(self):
        self.sample_data = [{
            "Title": "T-shirt 1",
            "Price": 100000,
            "Rating": 4.0,
            "Colors": 3,
            "Size": "M",
            "Gender": "Men",
            "Timestamp": "2025-03-30T00:00:00"
        }]

    def test_save_to_csv(self):
        test_file = "test_products.csv"
        save_to_csv(self.sample_data, filename=test_file)
        self.assertTrue(os.path.exists(test_file))
        os.remove(test_file)

    @patch("utils.load.create_engine")
    def test_save_to_postgresql(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        save_to_postgresql(self.sample_data, table_name="test_table")
        self.assertTrue(mock_create_engine.called)
        mock_engine.dispose.assert_not_called()  # opsional: cek tidak ada dispose jika tidak digunakan

    @patch("utils.load.set_with_dataframe")
    @patch("utils.load.ServiceAccountCredentials.from_json_keyfile_name")
    @patch("utils.load.gspread.authorize")
    def test_save_to_existing_google_sheet(self, mock_authorize, mock_creds, mock_set_df):
        mock_client = MagicMock()
        mock_sheet = MagicMock()
        mock_worksheet = MagicMock()

        # Fix: atur atribut worksheet.row_count secara eksplisit agar tidak jadi MagicMock
        mock_worksheet.row_count = 100
        mock_worksheet.col_count = 10

        mock_authorize.return_value = mock_client
        mock_client.open_by_key.return_value = mock_sheet
        mock_sheet.get_worksheet.return_value = mock_worksheet

        spreadsheet_id = "dummy_spreadsheet_id"
        save_to_existing_google_sheet(self.sample_data, spreadsheet_id)

        mock_client.open_by_key.assert_called_with(spreadsheet_id)
        mock_worksheet.clear.assert_called_once()
        mock_set_df.assert_called_once()


if __name__ == "__main__":
    unittest.main()