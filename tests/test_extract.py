import unittest
import pandas as pd
from utils.extract import extract_product_data

class TestExtract(unittest.TestCase):
    def test_extract_product_data(self):
        df = extract_product_data()

        # Pastikan hasil berupa DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Tidak boleh kosong
        self.assertFalse(df.empty)

        # Pastikan kolom penting tersedia
        required_columns = ['title', 'price', 'rating', 'timestamp']
        for col in required_columns:
            self.assertIn(col, df.columns)

        # Opsional: Cek tipe data dari beberapa kolom
        if not df.empty:
            self.assertIsInstance(df.iloc[0]['title'], str)
            self.assertIsInstance(df.iloc[0]['price'], str)
            self.assertIsInstance(df.iloc[0]['rating'], str)

if __name__ == '__main__':
    unittest.main()
