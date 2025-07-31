from serpapi import GoogleSearch
from api_key import API_KEY
import json, sys

from identificador import get_sorted_dates

EXAMPLE_PATH = "devito_example.json"
EXAMPLE_URL = "gunslinger_url.txt"

def save_example(dictionary):
    with open(EXAMPLE_PATH, "w") as f:
        json.dump(dictionary, f, indent=4)

def read_example():
    with open(EXAMPLE_PATH, "r") as f:
        result = json.loads(f.read())
    
    return result

def read_url(path):
    try:
        with open(path, "r") as f:
            result = f.read()
        return result
    except FileNotFoundError:
        return path

def main():
    if len(sys.argv) != 2:
        try:
            exact_matches = read_example()
            print("Leyendo ejemplo...")
        except FileNotFoundError:
            params = {
                "engine": "google_lens",
                "type": "exact_matches",
                "url": read_url(EXAMPLE_URL),
                "api_key": API_KEY
            }

            print("Buscando ejemplo...")
            search = GoogleSearch(params)
            results = search.get_dict()
            exact_matches = results["exact_matches"]
            save_example(exact_matches)
    else:
        params = {
                "engine": "google_lens",
                "type": "exact_matches",
                "url": read_url(sys.argv[1]),
                "api_key": API_KEY
            }

        print("Buscando imagen...")
        search = GoogleSearch(params)
        results = search.get_dict()
        exact_matches = results["exact_matches"]

    #print(json.dumps(exact_matches, indent=4))

    results = []
    for match in exact_matches:
        result = {
            "source": match["source"],
            "link": match["link"],
            "thumnail": match["thumbnail"]
        }
        results.append(result)
        #print(result)

    publicaciones = get_sorted_dates(results)
    top_10 = publicaciones[:9]
    print("------------------ TOP 10 --------------------")
    for i in range(len(top_10)):
        print(f"- {i+1} -")
        print(f"Source: {top_10[i]["source"]}")
        print(f"Link: {top_10[i]["link"]}")
        print(f"Thumnail: {top_10[i]["thumnail"]}")
        print(f"Fecha y hora: {top_10[i]["created_utc"]}")

if __name__ == "__main__":
    main()