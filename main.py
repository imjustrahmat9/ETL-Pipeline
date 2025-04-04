# Import fungsi-fungsi yang dibutuhkan dari modul internal
from utils.extract import extract_all_products
from utils.transform import full_cleaning_pipeline
from utils.load import save_to_csv, save_to_existing_google_sheet, save_to_postgresql

# Mengimpor pustaka dotenv dan os untuk mengelola variabel lingkungan
from dotenv import load_dotenv
import os

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mengambil data produk mentah dari situs Fashion Studio dengan batas maksimal 50 halaman
data_mentah = extract_all_products("https://fashion-studio.dicoding.dev", max_pages=50)

# Melakukan pembersihan dan transformasi data melalui pipeline pembersihan menyeluruh
data_bersih = full_cleaning_pipeline(data_mentah)

# Menyimpan data bersih ke dalam file CSV
save_to_csv(data_bersih)

# Mengambil ID spreadsheet dari variabel lingkungan
id_spreadsheet = os.getenv("SHEETS_ID")

# Menyimpan data ke Google Sheet yang sudah ada
save_to_existing_google_sheet(data_bersih, id_spreadsheet)

# Menyimpan data ke basis data PostgreSQL
save_to_postgresql(data_bersih)
