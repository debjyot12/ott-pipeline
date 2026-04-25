import pytest
import psycopg2
import os

# --- Database connection config ---
DB_CONFIG = {
    "host": "localhost",
    "database": "ott_pipeline",
    "user": "postgres",
    "password": os.environ.get("DB_PASSWORD"), 
    "port": 5432
}

# --- TMDB API config ---
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# --- Shared DB connection fixture ---
@pytest.fixture(scope="session")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    yield conn
    conn.close()
    