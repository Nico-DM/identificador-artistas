from serpapi import GoogleSearch

def main():
    params = {
    "engine": "google_lens",
    "url": "https://i.imgur.com/HBrB8p0.png",
    "api_key": "ded253e555b914cd3e4a74f5a08fef21dfda4a119ddb75167967ed3d66b81328"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    visual_matches = results["visual_matches"]
    print(visual_matches)

if __name__ == "__main__":
    main()