from fecha_scraper import obtener_fecha_publicacion
from html_interactivo import obtener_fecha_js
from datetime import datetime


def get_sorted_dates(results):
    publicaciones = []
    for result in results:
        print("-----")
        print(f"Source: {result["source"]}")
        print(f"Link: {result["link"]}")
        print("Obteniendo fecha de publicación...")
        result["created_utc"] = obtener_fecha_publicacion(result["link"])
        if not result["created_utc"]:
            result["created_utc"] = obtener_fecha_js(result["link"])
        
        print(f"Fecha y hora: {result["created_utc"]}")

        if result["created_utc"]:
            publicaciones.append(result)
    
    publicaciones.sort(key=lambda x: x["created_utc"])
        
    return publicaciones