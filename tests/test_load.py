import unittest
import pandas as pd
import os
from utils.load import load_to_csv

class TestLoad(unittest.TestCase):
    def test_load_to_csv(self):
        df = pd.DataFrame({
            'title': ['Shirt'],
            'price': [160000],
            'rating': [4.5],
            'colors': [2],
            'size': ['M'],
            'gender': ['Men'],
            'timestamp': [pd.Timestamp.now()]
        })
        filename = 'test_products.csv'

        try:
            load_to_csv(df, filename)
            self.assertTrue(os.path.exists(filename))

            # Opsional: Periksa isi file jika ingin lebih ketat
            loaded_df = pd.read_csv(filename)
            self.assertEqual(len(loaded_df), 1)
            self.assertIn('title', loaded_df.columns)

        finally:
            # Opsional: Cleanup file setelah test
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == '__main__':
    unittest.main()
