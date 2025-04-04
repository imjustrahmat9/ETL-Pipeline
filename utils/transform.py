import pandas as pd
import re

def full_cleaning_pipeline(raw_data: list[dict], kurs_dollar: int = 16000) -> list[dict]:
    try:
        # Fungsi untuk menghapus baris dengan data yang tidak valid
        def hapus_baris_tidak_valid(df: pd.DataFrame) -> pd.DataFrame:
            return df[
                (df['Title'] != 'Unknown Product') &
                (df['Price'] != 'Price Unavailable') &
                (~df['Rating'].str.contains('Invalid Rating', na=False)) &
                (~df['Rating'].str.contains('Not Rated', na=False))
            ].copy()

        # Fungsi untuk membersihkan dan mengubah format nilai-nilai pada kolom tertentu
        def transformasi_nilai(df: pd.DataFrame) -> pd.DataFrame:
            # Ubah kolom harga dari string ke float dan konversi ke rupiah
            df['Price'] = df['Price'].str.replace('$', '', regex=False).astype(float)
            df['Price'] = df['Price'] * kurs_dollar

            # Ekstrak nilai rating numerik dari string
            df['Rating'] = df['Rating'].apply(
                lambda x: float(re.search(r"(\d+(\.\d+)?)", x).group()) if re.search(r"(\d+(\.\d+)?)", x) else None
            )

            # Ekstrak jumlah warna dari deskripsi
            df['Colors'] = df['Colors'].apply(
                lambda x: int(re.search(r"\d+", x).group()) if re.search(r"\d+", x) else None
            )

            # Bersihkan string ukuran dan gender
            df['Size'] = df['Size'].str.replace('Size:', '', regex=False).str.strip()
            df['Gender'] = df['Gender'].str.replace('Gender:', '', regex=False).str.strip()

            # Hapus duplikat
            df = df.drop_duplicates()

            return df

        # Ubah data mentah menjadi DataFrame
        df = pd.DataFrame(raw_data)

        # Tahap pembersihan data tidak valid
        df_bersih = hapus_baris_tidak_valid(df)

        # Tahap transformasi nilai
        df_akhir = transformasi_nilai(df_bersih)

        # Kembalikan hasil sebagai list of dict
        return df_akhir.to_dict(orient="records")

    except Exception as e:
        print(f"[ERROR] Gagal menjalankan full cleaning pipeline: {e}")
        return []
