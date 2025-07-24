from source_id.reddit import obtener_fecha_post
from datetime import datetime

def get_oldest(results):
    accepted_sources = ["Reddit"]
    filtered_results = list(filter(lambda x: x["source"] in accepted_sources, results))
    
    oldest = {
        "created_utc": datetime.now()
    }
    for result in filtered_results:
        if result["source"] == "Reddit":
            result["created_utc"] = obtener_fecha_post(result["link"])
        
        print("-----")
        print(f"Link: {result["link"]}")
        print(f"Fecha y hora: {result["created_utc"]}")

        if result["created_utc"] < oldest["created_utc"]:
            oldest = result
            print("^ MÁS VIEJO HASTA AHORA")
        
    return oldest