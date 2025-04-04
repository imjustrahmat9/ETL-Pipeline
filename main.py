from utils.extract import extract_all_products
from utils.transform import full_cleaning_pipeline
from utils.load import save_to_csv, save_to_existing_google_sheet, save_to_postgresql
from dotenv import load_dotenv
import os

load_dotenv()

raw_data = extract_all_products("https://fashion-studio.dicoding.dev", max_pages=50)
cleaned_json = full_cleaning_pipeline(raw_data)

save_to_csv(cleaned_json)
spreadsheet_id = os.getenv("SHEETS_ID")
save_to_existing_google_sheet(cleaned_json, spreadsheet_id)
save_to_postgresql(cleaned_json)