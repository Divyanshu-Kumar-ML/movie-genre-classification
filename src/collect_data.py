import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# --------------------------------------------------
# 1. Load API token
# --------------------------------------------------

load_dotenv()

token = os.getenv("TMDB_API_TOKEN")

if not token:
    raise ValueError("TMDB_API_TOKEN not found in .env")


# --------------------------------------------------
# 2. TMDB configuration
# --------------------------------------------------

BASE_URL = "https://api.themoviedb.org/3"

headers = {
    "Authorization": f"Bearer {token}",
    "accept": "application/json"
}


# --------------------------------------------------
# 3. Create a session with automatic retries
# --------------------------------------------------

session = requests.Session()

retry_strategy = Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)
session.mount("http://", adapter)


# --------------------------------------------------
# 4. Get genre mapping
# --------------------------------------------------

def get_genres():

    url = f"{BASE_URL}/genre/movie/list"

    while True:
        try:
            response = session.get(
                url,
                headers=headers,
                params={"language": "en"},
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            return {
                genre["id"]: genre["name"]
                for genre in data["genres"]
            }

        except requests.exceptions.RequestException as e:

            print("Could not get genre list.")
            print("Error:", e)
            print("Retrying in 10 seconds...")

            time.sleep(10)

# --------------------------------------------------
# 5. Collect movies
# --------------------------------------------------

def collect_movies(num_pages=500):

    genre_map = get_genres()

    movies = []

    os.makedirs("data/raw", exist_ok=True)

    checkpoint_file = "data/raw/last_completed_page.txt"

    # Resume from previous progress
    if os.path.exists(checkpoint_file):

        with open(checkpoint_file, "r") as f:
            last_page = int(f.read().strip())

        start_page = last_page + 1

        print(f"Resuming from page {start_page}...")

    else:

        start_page = 1

        print("Starting collection from page 1...")


    # Load previously collected data if available
    output_file = "data/raw/tmdb_movies.csv"

    if os.path.exists(output_file):

        old_df = pd.read_csv(output_file)

        movies = old_df.to_dict("records")

        print(f"Previously collected records: {len(movies)}")


    # --------------------------------------------------
    # Collect pages
    # --------------------------------------------------

    for page in range(start_page, num_pages + 1):

        url = f"{BASE_URL}/discover/movie"

        params = {
            "language": "en-US",
            "sort_by": "popularity.desc",
            "include_adult": "false",
            "page": page
        }

        try:

            response = session.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as e:

            print(f"\nPage {page} failed:")
            print(e)

            print("Waiting 10 seconds before trying again...\n")

            time.sleep(10)

            continue


        # --------------------------------------------------
        # Store raw movie information
        # --------------------------------------------------

        for movie in data.get("results", []):

            genre_names = [
                genre_map[g]
                for g in movie.get("genre_ids", [])
                if g in genre_map
            ]

            movies.append({
                "id": movie.get("id"),
                "title": movie.get("title"),
                "overview": movie.get("overview"),
                "genres": "|".join(genre_names),
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average"),
                "popularity": movie.get("popularity")
            })


        print(
            f"Page {page}/{num_pages} collected | "
            f"Total records: {len(movies)}"
        )


        # --------------------------------------------------
        # Save progress after every page
        # --------------------------------------------------

        df = pd.DataFrame(movies)

        df.to_csv(
            output_file,
            index=False,
            encoding="utf-8"
        )

        with open(checkpoint_file, "w") as f:
            f.write(str(page))


        # Wait before next request
        time.sleep(1)


    return movies


# --------------------------------------------------
# 6. Main
# --------------------------------------------------

if __name__ == "__main__":

    movies = collect_movies(num_pages=500)

    print("\n" + "=" * 50)
    print("DATA COLLECTION FINISHED")
    print("=" * 50)

    print(f"Total records collected: {len(movies)}")

    print("Saved to:")
    print("data/raw/tmdb_movies.csv")