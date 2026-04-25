import requests
import pytest
import os

TMDB_BASE_URL = "https://api.themoviedb.org/3"
VALID_TOKEN = os.environ.get("TMDB_TOKEN")
INVALID_TOKEN = "this_is_a_bad_token"

HEADERS_VALID = {
    "Authorization": f"Bearer {VALID_TOKEN}",
    "accept": "application/json"
}

HEADERS_INVALID = {
    "Authorization": f"Bearer {INVALID_TOKEN}",
    "accept": "application/json"
}

PARAMS = {
    "with_watch_monetization_types": "flatrate",
    "watch_region": "IN"
}

session = requests.Session()

# Warm up the connection before tests run
import time
time.sleep(2)
try:
    session.get(f"{TMDB_BASE_URL}/discover/movie", headers=HEADERS_VALID, params=PARAMS)
except Exception:
    pass

def test_api_status_200():
    url = f"{TMDB_BASE_URL}/discover/movie"
    response = session.get(url, headers=HEADERS_VALID, params=PARAMS)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

def test_response_has_results():
    url = f"{TMDB_BASE_URL}/discover/movie"
    response = session.get(url, headers=HEADERS_VALID, params=PARAMS)
    data = response.json()
    assert "results" in data, "Response missing 'results' key"
    assert isinstance(data["results"], list), "'results' is not a list"

def test_each_movie_has_title_and_rating():
    url = f"{TMDB_BASE_URL}/discover/movie"
    response = session.get(url, headers=HEADERS_VALID, params=PARAMS)
    data = response.json()
    movies = data["results"]
    for movie in movies:
        assert "title" in movie, f"Movie missing title: {movie}"
        assert "vote_average" in movie, f"Movie missing rating: {movie}"

def test_invalid_token_returns_401():
    url = f"{TMDB_BASE_URL}/discover/movie"
    response = session.get(url, headers=HEADERS_INVALID, params=PARAMS)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"