import json
import psycopg2
import os
from psycopg2.extras import execute_values

# --- Config ---
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "ott_pipeline",
    "user": "postgres",
    "password": os.environ.get("DB_PASSWORD")
}

RAW_FILE = r"D:\my_python_project\ott-pipeline\data\raw_all_platforms.json"

def load_data():
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        rows_raw = json.load(f)

    rows = [
        (item.get("title"), item.get("rating"), item.get("platform"))
        for item in rows_raw
    ]

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("TRUNCATE TABLE raw_content;")

    execute_values(cur, """
        INSERT INTO raw_content (title, rating, platform)
        VALUES %s
    """, rows)

    conn.commit()
    print(f"Loaded {len(rows)} records into raw_content.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_data()