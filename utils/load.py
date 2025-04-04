import pandas as pd
import os
import psycopg2
import gspread
from gspread_dataframe import set_with_dataframe
from sqlalchemy import create_engine
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

def save_to_csv(data: list[dict], filename="products.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"[CSV] Data saved to {filename}")

def save_to_existing_google_sheet(data: list[dict], spreadsheet_id: str, worksheet_index: int = 0):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google-sheets-api.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(spreadsheet_id)
    worksheet = sheet.get_worksheet(worksheet_index)

    worksheet.clear()

    df = pd.DataFrame(data)
    set_with_dataframe(worksheet, df)

    print(f"[Google Sheets] Data berhasil ditulis ulang ke spreadsheet dengan nama Fashion Products")

def save_to_postgresql(data: list[dict], table_name="products"):
    df = pd.DataFrame(data)

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url)

    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"[PostgreSQL] Data uploaded to table: {table_name}")