import unittest
import pandas as pd
from utils.transform import transform_product_data

class TestTransform(unittest.TestCase):
    def test_transform_product_data(self):
        data = {
            'title': ['Shirt', 'Unknown Product'],
            'price': ['$10.00', '$15.00'],
            'rating': ['Rating: 4.5', 'Invalid Rating'],
            'colors': ['2 colors', '3 colors'],
            'size': ['Size: M', 'Size: L'],
            'gender': ['Gender: Men', 'Gender: Women'],
            'timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
        }
        df = pd.DataFrame(data)

        # Transformasi
        clean_df = transform_product_data(df)

        # Hanya 1 baris valid
        self.assertEqual(len(clean_df), 1)

        # Validasi hasil transformasi
        self.assertAlmostEqual(clean_df.iloc[0]['price'], 160000.0)
        self.assertAlmostEqual(clean_df.iloc[0]['rating'], 4.5)
        self.assertEqual(clean_df.iloc[0]['colors'], 2)
        self.assertEqual(clean_df.iloc[0]['size'], 'M')
        self.assertEqual(clean_df.iloc[0]['gender'], 'Men')

        # Opsional: Pastikan tidak ada nilai kosong
        self.assertFalse(clean_df.isnull().values.any())

if __name__ == '__main__':
    unittest.main()
