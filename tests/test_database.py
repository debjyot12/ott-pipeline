import pytest


# --- Test 1: Total row count is 80 ---
def test_total_row_count(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM raw_content;")
    count = cursor.fetchone()[0]
    assert count >= 4, f"Expected at least 4 rows, got {count}"

# --- Test 2: No nulls in title, rating, platform ---
def test_no_nulls_in_key_columns(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM raw_content
        WHERE title IS NULL
        OR rating IS NULL
        OR platform IS NULL;
    """)
    null_count = cursor.fetchone()[0]
    assert null_count == 0, f"Found {null_count} rows with null values"

# --- Test 3: Ratings are between 0 and 10 ---
def test_ratings_in_valid_range(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM raw_content
        WHERE rating < 0 OR rating > 10;
    """)
    bad_count = cursor.fetchone()[0]
    assert bad_count == 0, f"Found {bad_count} rows with invalid ratings"

# --- Test 4: All 4 platforms are present ---
def test_all_platforms_present(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT DISTINCT platform FROM raw_content;")
    platforms = [row[0] for row in cursor.fetchall()]
    expected = {"Netflix", "Prime Video", "JioHotstar", "SonyLIV"}
    assert set(platforms) == expected, f"Platforms found: {platforms}"