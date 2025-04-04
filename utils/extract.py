import requests
from bs4 import BeautifulSoup
from datetime import datetime


def extract_all_products(base_url: str, max_pages: int = 50):
    all_products = []

    for page in range(1, max_pages + 1):
        url = base_url if page == 1 else f"{base_url}/page{page}"
        print(f"Scraping {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Gagal memuat halaman {page}. Status: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        product_cards = soup.find_all('div', class_='collection-card')

        if not product_cards:
            print(f"Tidak ada produk di halaman {page}. Berhenti.")
            break

        for card in product_cards:
            try:
                details = card.find('div', class_='product-details')
                if details is None:
                    print("Tidak ada detail produk, dilewati.")
                    continue

                name_tag = details.find('h3', class_='product-title')
                name = name_tag.text.strip() if name_tag else None

                price_tag = details.find('span', class_='price')
                if price_tag:
                    price = price_tag.text.strip()
                else:
                    p_price_tag = details.find('p', class_='price')
                    price = p_price_tag.text.strip() if p_price_tag else None

                all_p = details.find_all('p')
                meta = []

                for p in all_p:
                    if 'price' in p.get('class', []):
                        continue
                    meta.append(p.text.strip())

                rating = meta[0] if len(meta) > 0 else None
                colors = meta[1] if len(meta) > 1 else None
                size = meta[2] if len(meta) > 2 else None
                gender = meta[3] if len(meta) > 3 else None

                product = {
                    "Title": name,
                    "Price": price,
                    "Rating": rating,
                    "Colors": colors,
                    "Size": size,
                    "Gender": gender,
                    "Timestamp": datetime.now().isoformat()
                }

                all_products.append(product)

            except Exception as e:
                print(f"Error parsing product: {e}")

    return all_products