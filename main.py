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
        result = (match["source"], match["link"])
        results.append(result)
        print(result)

    oldest = get_oldest(results)
    print(f"Source: {oldest[0]}")
    print(f"Link: {oldest[1]}")

if __name__ == "__main__":
    main()