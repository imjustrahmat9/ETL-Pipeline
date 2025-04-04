import pandas as pd
import re


def full_cleaning_pipeline(raw_data: list[dict], kurs_dollar: int = 16000) -> list[dict]:
    try:
        def clean_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
            return df[
                (df['Title'] != 'Unknown Product') &
                (df['Price'] != 'Price Unavailable') &
                (~df['Rating'].str.contains('Invalid Rating', na=False)) &
                (~df['Rating'].str.contains('Not Rated', na=False))
            ].copy()

        def transform_values(df: pd.DataFrame) -> pd.DataFrame:
            df['Price'] = df['Price'].str.replace('$', '', regex=False).astype(float)
            df['Price'] = df['Price'] * kurs_dollar

            df['Rating'] = df['Rating'].apply(
                lambda x: float(re.search(r"(\d+(\.\d+)?)", x).group()) if re.search(r"(\d+(\.\d+)?)", x) else None
            )

            df['Colors'] = df['Colors'].apply(
                lambda x: int(re.search(r"\d+", x).group()) if re.search(r"\d+", x) else None
            )

            df['Size'] = df['Size'].str.replace('Size:', '', regex=False).str.strip()
            df['Gender'] = df['Gender'].str.replace('Gender:', '', regex=False).str.strip()

            df = df.drop_duplicates()

            return df

        df = pd.DataFrame(raw_data)

        df_cleaned = clean_invalid_rows(df)

        df_transformed = transform_values(df_cleaned)

        return df_transformed.to_dict(orient="records")

    except Exception as e:
        print(f"[ERROR] Gagal menjalankan full cleaning pipeline: {e}")
        return []