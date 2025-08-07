from serpapi import GoogleSearch
from api_key import API_KEY
import json, sys

from identificador import get_sorted_dates

EXAMPLE_URL = "https://i.imgur.com/HBrB8p0.png"
CACHE_PATH = "cache.json"

def read_url(path):
    try:
        with open(path, "r") as f:
            result = f.read()
        return result
    except FileNotFoundError:
        return path

def read_cache(url):
    try:
        with open(CACHE_PATH, "r") as f:
            result = json.loads(f.read())
        return 0, result[url]
    except FileNotFoundError:
        return -1, []
    except KeyError:
        return -2, []

def save_cache(url, exact_matches):
    try:
        with open(CACHE_PATH, "r") as f:
            result = json.loads(f.read())
    except FileNotFoundError:
        result = {}
    result[url] = exact_matches
    with open(CACHE_PATH, "w") as f:
        json.dump(result, f, indent=4)

def main():
    url = ""
    if len(sys.argv) != 2:
        url = read_url(EXAMPLE_URL)
    else:
        url = read_url(sys.argv[1])
    
    error, exact_matches = read_cache(url)
    print("Leyendo del cache...")
    if error < 0:
        print("No se encontró en el cache")
        params = {
                "engine": "google_lens",
                "type": "exact_matches",
                "url": url,
                "api_key": API_KEY
            }

        print("Buscando imagen...")
        search = GoogleSearch(params)
        results = search.get_dict()
        exact_matches = results["exact_matches"]
        save_cache(url, exact_matches)
        print("Registrado en el cache")

    results = []
    for match in exact_matches:
        result = {
            "source": match["source"],
            "link": match["link"],
            "thumnail": match["thumbnail"]
        }
        results.append(result)

    publicaciones = get_sorted_dates(results)
    top_10 = publicaciones[:10]
    print("------------------ TOP 10 --------------------")
    for i in range(len(top_10)):
        print(f"- {i+1} -")
        print(f"Source: {top_10[i]["source"]}")
        print(f"Link: {top_10[i]["link"]}")
        print(f"Thumnail: {top_10[i]["thumnail"]}")
        print(f"Fecha y hora: {top_10[i]["created_utc"]}")

if __name__ == "__main__":
    main()