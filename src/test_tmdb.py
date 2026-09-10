import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TMDB_API_TOKEN")

url = "https://api.themoviedb.org/3/movie/550"

headers = {
    "Authorization": f"Bearer {token}",
    "accept": "application/json"
}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("Movie:", data["title"])
    print("Overview:", data["overview"])
else:
    print("Request failed:")
    print(response.text)