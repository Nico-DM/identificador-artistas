from serpapi import GoogleSearch
from api_key import API_KEY
import json

from identificador import get_oldest

def save_example(dictionary):
    with open("example.json", "w") as f:
        json.dump(dictionary, f, indent=4)

def read_example():
    with open("example.json", "r") as f:
        result = json.loads(f.read())
    
    return result

def main():
    try:
        exact_matches = read_example()
    except FileNotFoundError:
        params = {
            "engine": "google_lens",
            "type": "exact_matches",
            "url": "https://i.imgur.com/HBrB8p0.png",
            "api_key": API_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        exact_matches = results["exact_matches"]
        save_example(exact_matches)
    
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

    oldest = get_oldest(results)
    print("-------------------------------------------------")
    print(f"Source: {oldest["source"]}")
    print(f"Link: {oldest["link"]}")
    print(f"Thumnail: {oldest["thumnail"]}")
    print(f"Fecha y hora: {oldest["created_utc"]}")

if __name__ == "__main__":
    main()