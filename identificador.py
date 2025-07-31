from fecha_scraper import obtener_fecha_publicacion
from datetime import datetime

def get_sorted_dates(results):
    publicaciones = []
    for result in results:
        print("-----")
        print("Obteniendo fecha de publicación...")
        result["created_utc"] = obtener_fecha_publicacion(result["link"])
        
        print(f"Source: {result["source"]}")
        print(f"Link: {result["link"]}")
        print(f"Fecha y hora: {result["created_utc"]}")

        if result["created_utc"]:
            publicaciones.append(result)
    
    publicaciones.sort(key=lambda x: x["created_utc"])
        
    return publicaciones