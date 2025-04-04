import unittest
from unittest.mock import patch, Mock
from utils.extract import extract_all_products


class TestExtract(unittest.TestCase):
    @patch("utils.extract.requests.get")
    def test_extract_all_products_success(self, mock_get):
        html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">T-shirt 1</h3>
                <span class="price">$123.45</span>
                <p>Rating: ⭐ 4.4 / 5</p>
                <p>3 Colors</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
            </div>
        </div>
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = html
        mock_get.return_value = mock_response

        base_url = "https://fake-url.com"
        result = extract_all_products(base_url, max_pages=1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Title"], "T-shirt 1")
        self.assertEqual(result[0]["Price"], "$123.45")

    @patch("utils.extract.requests.get")
    def test_empty_product_page(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><div class='collection-grid'></div></body></html>"
        mock_get.return_value = mock_response

        result = extract_all_products("https://fake-url.com", max_pages=1)
        self.assertEqual(result, [])

    @patch("utils.extract.requests.get")
    def test_page_failed_to_load(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = ""
        mock_get.return_value = mock_response

        result = extract_all_products("https://fake-url.com", max_pages=1)
        self.assertEqual(result, [])

    @patch("utils.extract.requests.get")
    def test_product_missing_fields(self, mock_get):
        html = """
        <div class="collection-card">
            <div class="product-details">
                <!-- No h3 title, no price -->
                <p>Rating: ⭐ 4.4 / 5</p>
                <p>3 Colors</p>
                <p>Size: M</p>
                <p>Gender: Men</p>
            </div>
        </div>
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = html
        mock_get.return_value = mock_response

        result = extract_all_products("https://fake-url.com", max_pages=1)
        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]["Title"])
        self.assertIsNone(result[0]["Price"])

    @patch("utils.extract.requests.get")
    def test_card_without_product_details(self, mock_get):
        html = """
        <div class="collection-card">
            <!-- no product-details div at all -->
        </div>
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = html
        mock_get.return_value = mock_response

        result = extract_all_products("https://fake-url.com", max_pages=1)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
