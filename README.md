
# ETL Pipeline: Fashion Studio

Proyek ini adalah ETL pipeline untuk mengambil data produk dari website Fashion Studio, membersihkannya, dan menyimpannya ke file CSV, Google Sheets, serta PostgreSQL.

---

## Cara Menjalankan

### 1. Install dependensi
```bash
pip install -r requirements.txt
```

### 2. Jalankan ETL
```bash
python3 main.py
```

---

## Konfigurasi

### File `.env` (untuk PostgreSQL)
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password

SHEETS_ID=spreadsheet_id
```
---

## Testing

### Jalankan semua unit test
```bash
python3 -m unittest discover tests
```

### Jalankan dengan coverage
```bash
pytest --cov=utils --cov-report=term-missing tests/
```

---

## Output
- `products.csv`
- Google Spreadsheet `Fashion Products`
- Tabel PostgreSQL (`products`)
