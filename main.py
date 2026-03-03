import os

from serpapi import GoogleSearch
from dotenv import load_dotenv
import json, sys

from identificador import get_sorted_dates

load_dotenv()
API_KEY = os.environ.get("SERPAPI_API_KEY")
EXAMPLE_URL = "https://i.pinimg.com/originals/f8/0f/2b/f80f2bcfe71701829515ec7dcfc2a5c7.jpg"
CACHE_PATH = "cache.json"
OUTPUT_PATH = "output.json"

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
    if len(sys.argv) != 2:
        print("Uso:")
        print("\tpython3 main.py <url>")
        print()
        print("Si la url es demasiado larga, puedes pegarla en un archivo de texto cualquiera y copiar el path:")
        print("\tpython3 main.py <path>")
        sys.exit()

    if not API_KEY:
        print("Falta SERPAPI_API_KEY en el entorno. Configurala antes de ejecutar.")
        sys.exit(1)

    url = read_url(sys.argv[1])

    error, exact_matches = read_cache(url)
    print("Leyendo del cache...")
    if error < 0:
        print("No se encontro en el cache")
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
            "thumbnail": match["thumbnail"],
        }
        results.append(result)

    publicaciones = get_sorted_dates(results)
    for p in publicaciones:
        p["created_utc"] = f"{p['created_utc']}"

    with open(OUTPUT_PATH, "w") as f:
        json.dump(publicaciones, f, indent=4)

    top_10 = publicaciones[:10]
    if len(publicaciones) <= 10:
        print(f"---------- RESULTADOS (copiados en {OUTPUT_PATH}) ----------")
    else:
        print(f"---------- TOP 10 ({len(publicaciones)} resultados en {OUTPUT_PATH}) ----------")
    for i in range(len(top_10)):
        print(f"{i+1}.\tFuente: {top_10[i]['source']}")
        print(f"\tLink: {top_10[i]['link']}")
        print(f"\tMiniatura: {top_10[i]['thumbnail']}")
        print(f"\tFecha y hora: {top_10[i]['created_utc']}")


if __name__ == "__main__":
    main()