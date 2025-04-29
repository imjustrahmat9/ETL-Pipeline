import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = 'https://fashion-studio.dicoding.dev/'

def extract_product_data():
    products = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for page in range(1, 51):
        try:
            print(f"Memproses halaman {page}")
            response = requests.get(f'{BASE_URL}?page={page}', headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Halaman {page} gagal dimuat.")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            product_elements = soup.find_all('div', class_='collection-card')

            if not product_elements:
                print(f"Tidak ada produk di halaman {page}.")
                continue

            for product in product_elements:
                try:
                    # Judul produk
                    title_tag = product.find('h3', class_='product-title')
                    title = title_tag.text.strip() if title_tag else 'Unknown Product'

                    # Harga
                    price_tag = product.find('span', class_='price')
                    price = price_tag.text.strip() if price_tag else '$0.00'

                    # Info tambahan
                    info_paragraphs = product.find_all('p')
                    rating = next((p.text.strip() for p in info_paragraphs if 'Rating:' in p.text), 'Rating: 0')
                    colors = next((p.text.strip() for p in info_paragraphs if 'Color' in p.text), '0 Colors')
                    size = next((p.text.strip() for p in info_paragraphs if 'Size:' in p.text), 'Size: -')
                    gender = next((p.text.strip() for p in info_paragraphs if 'Gender:' in p.text), 'Gender: -')

                    # Tambahkan ke list
                    products.append({
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'colors': colors,
                        'size': size,
                        'gender': gender,
                        'timestamp': pd.Timestamp.now()
                    })
                except Exception as e:
                    print(f"Error parsing produk di halaman {page}: {e}")
        except Exception as e:
            print(f"Request ke halaman {page} gagal: {e}")
        time.sleep(1)  # Agar tidak overload

    return pd.DataFrame(products)
