import gspread
import logging
import traceback
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_to_csv(df, filename='products.csv'):
    try:
        df.to_csv(filename, index=False)
        logging.info(f"Data berhasil disimpan ke file CSV: {filename}")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke CSV: {e}")
        logging.debug(traceback.format_exc())

def load_to_google_sheets(df, sheet_id, creds_file='your sheets api'):
    import pandas as pd
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).sheet1

        # ✅ Konversi semua datetime menjadi string (format ISO atau sesuaikan)
        df = df.copy()
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)  # atau df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        logging.info("Data berhasil dimuat ke Google Sheets.")
    except Exception as e:
        logging.error(f"Gagal memuat data ke Google Sheets: {e}")
        logging.debug(traceback.format_exc())

def load_to_postgresql(df, db_url, table_name='products'):
    try:
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Data berhasil dimuat ke PostgreSQL table '{table_name}'.")
    except Exception as e:
        logging.error(f"Gagal memuat data ke PostgreSQL: {e}")
        logging.debug(traceback.format_exc())
