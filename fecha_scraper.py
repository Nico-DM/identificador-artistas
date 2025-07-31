import requests
from bs4 import BeautifulSoup
import re
import dateparser
from datetime import datetime, timezone

def obtener_fechas_candidatas(html):
    soup = BeautifulSoup(html, "html.parser")
    fechas = []

    # 1. Etiquetas <time>
    for time_tag in soup.find_all("time"):
        if time_tag.get("datetime"): # type: ignore
            fechas.append((time_tag["datetime"], "time-datetime")) # type: ignore
        elif time_tag.text:
            fechas.append((time_tag.text.strip(), "time-text"))

    # 2. Metadatos comunes
    metas = [
        "article:published_time", "og:published_time", "date", "dc.date",
        "dc.date.issued", "pubdate", "publish-date", "datePublished"
    ]
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower() # type: ignore
        prop = meta.get("property", "").lower() # type: ignore
        value = meta.get("content") or meta.get("value") # type: ignore
        if value:
            if name in metas or prop in metas:
                fechas.append((value, f"meta:{name or prop}"))

    # 3. Texto plano
    texto = soup.get_text()
    patrones = re.findall(
        r"\b(\d{1,2} de \w+ de \d{4}|\w+ \d{1,2}, \d{4}|\d{4}-\d{2}-\d{2})\b",
        texto, re.IGNORECASE
    )
    for p in patrones:
        fechas.append((p, "texto"))

    return fechas

def seleccionar_mejor_fecha(fechas_raw):
    puntuadas = []
    for texto, fuente in fechas_raw:
        fecha = dateparser.parse(texto)
        if fecha:
            fecha_sin_tz = fecha.astimezone(timezone.utc).replace(tzinfo=None) if fecha.tzinfo else fecha
            if fecha_sin_tz <= datetime.now():
                puntaje = 0
                if "published" in fuente or "datePublished" in fuente:
                    puntaje += 3
                if "meta" in fuente:
                    puntaje += 2
                if "time" in fuente:
                    puntaje += 1
                puntuadas.append((fecha_sin_tz, puntaje))

    puntuadas.sort(key=lambda x: (-x[1], x[0]))  # mayor puntaje y más antigua
    return puntuadas[0][0] if puntuadas else None

def obtener_fecha_publicacion(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if r.status_code != 200:
            return None
        html = r.text
        fechas_raw = obtener_fechas_candidatas(html)
        return seleccionar_mejor_fecha(fechas_raw)
    except Exception as e:
        print("Error:", e)
        return None
