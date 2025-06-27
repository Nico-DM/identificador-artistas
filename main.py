from serpapi import GoogleSearch
from api_key import API_KEY

def main():
    params = {
        "engine": "google_lens",
        "type": "exact_matches",
        "url": "https://i.imgur.com/HBrB8p0.png",
        "api_key": API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    exact_matches = results["exact_matches"]
    print(exact_matches)

if __name__ == "__main__":
    main()