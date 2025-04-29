import pandas as pd
import re

def transform_product_data(df):
    if 'title' not in df.columns:
        raise ValueError("Kolom 'title' tidak ditemukan dalam DataFrame.")

    # Filter produk valid
    df = df[df['title'] != 'Unknown Product']
    df = df[df['rating'].str.contains(r'\d', na=False)]
    df = df.drop_duplicates()
    df = df.dropna()

    # Ubah harga ke float dan kalikan dengan kurs IDR (contoh: 1 USD = 16,000)
    def convert_price(price_str):
        try:
            return float(price_str.replace('$', '').replace(',', '')) * 16000
        except:
            return 0.0

    df['price'] = df['price'].apply(convert_price)

    # Ambil angka pertama dari string rating (contoh: "Rating: 4.5/5")
    def extract_rating(rating_str):
        match = re.search(r'\d+(\.\d+)?', rating_str)
        return float(match.group()) if match else 0.0

    df['rating'] = df['rating'].apply(extract_rating)

    # Ambil jumlah warna dari string (contoh: "4 Colors")
    def extract_colors(color_str):
        match = re.search(r'\d+', color_str)
        return int(match.group()) if match else 0

    df['colors'] = df['colors'].apply(extract_colors)

    # Bersihkan string ukuran dan gender
    df['size'] = df['size'].apply(lambda x: x.split('Size: ')[-1].strip() if isinstance(x, str) and 'Size:' in x else '')
    df['gender'] = df['gender'].apply(lambda x: x.split('Gender: ')[-1].strip() if isinstance(x, str) and 'Gender:' in x else '')

    return df
