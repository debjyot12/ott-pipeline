import requests
import json
import time
import os


#Phase 1 Step 1

API_TOKEN = os.environ.get("TMDB_TOKEN")

def fetch_movies_by_platform(platform_id, platform_name):
    url = "https://api.themoviedb.org/3/discover/movie"

    headers = {
        "Authorization": "Bearer " + API_TOKEN,
        "accept": "application/json",
        "User-Agent": "ott-pipeline/1.0"
    }

    params = {
        "watch_region": "IN",
        "with_watch_providers": platform_id,
        "sort_by": "popularity.desc"
    }

    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            break
        except Exception as e:
            print(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(2)
    else:
        print("All attempts failed.")
        return []

    netflix_movies = []
    for movie in data["results"]:
        netflix_movies.append({
            "title": movie["title"],
            "rating": movie["vote_average"],
            "platform": platform_name
        })

    return netflix_movies


netflix_movies = fetch_movies_by_platform(8, "Netflix")

print("Total fetched:", len(netflix_movies))
print(json.dumps(netflix_movies[0], indent=2))

with open("D:/my_python_project/ott-pipeline/data/netflix_raw.json", "w") as f:
    json.dump(netflix_movies, f, indent=4)

print("Saved to data/netflix_raw.json")

#Phase 1 Step 2

netflix_movies = fetch_movies_by_platform(8, "Netflix")
prime_movies = fetch_movies_by_platform(119, "Prime Video")
hotstar_movies = fetch_movies_by_platform(2336, "JioHotstar")
sonyliv_movies = fetch_movies_by_platform(237, "SonyLIV")

all_movies = netflix_movies + prime_movies + hotstar_movies + sonyliv_movies

print("Total fetched:", len(all_movies))
print(json.dumps(all_movies[0], indent=2))

with open("D:/my_python_project/ott-pipeline/data/raw_all_platforms.json", "w") as f:
    json.dump(all_movies, f, indent=4)

print("Saved to data/raw_all_platforms.json")



