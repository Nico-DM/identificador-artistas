from scraper_estatico import obtener_fecha_estatica
from scraper_dinamico import obtener_fecha_dinamica


def get_sorted_dates(results):
    publicaciones = []
    i = 0
    for result in results:
        i += 1
        print(f"----- {i}/{len(results)} -----")
        print(f"Source: {result["source"]}")
        print(f"Link: {result["link"]}")
        print("Obteniendo fecha de publicación estática...")
        result["created_utc"] = obtener_fecha_estatica(result["link"])
        if not result["created_utc"]:
            print("No se encontró fecha estática; buscando dinámica...")
            result["created_utc"] = obtener_fecha_dinamica(result["link"])

        if result["created_utc"]:
            print(f"Fecha y hora: {result["created_utc"]}")
            publicaciones.append(result)
        else:
            print("No se encontró fecha dinámica; ignorando resultado")
    
    publicaciones.sort(key=lambda x: x["created_utc"])
        
    return publicaciones