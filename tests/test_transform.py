import unittest
from utils.transform import full_cleaning_pipeline


class TestTransform(unittest.TestCase):
    def test_transform_with_invalid_price(self):
        raw_data = [{
            "Title": "T-shirt 1",
            "Price": "$invalid",  # ini akan gagal di cast float
            "Rating": "Rating: ⭐ 4.2 / 5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Men",
            "Timestamp": "2025-03-30T00:00:00"
        }]

        result = full_cleaning_pipeline(raw_data)
        self.assertEqual(result, [])  # fungsi harus menangkap exception dan return []

    def test_transform_with_valid_data(self):
        raw_data = [{
            "Title": "T-shirt 2",
            "Price": "$200.00",
            "Rating": "Rating: ⭐ 4.5 / 5",
            "Colors": "4 Colors",
            "Size": "Size: L",
            "Gender": "Gender: Unisex",
            "Timestamp": "2025-03-30T00:00:00"
        }]
        result = full_cleaning_pipeline(raw_data)
        self.assertEqual(result[0]["Price"], 200.0 * 16000)
        self.assertEqual(result[0]["Rating"], 4.5)
        self.assertEqual(result[0]["Colors"], 4)
        self.assertEqual(result[0]["Size"], "L")
        self.assertEqual(result[0]["Gender"], "Unisex")
