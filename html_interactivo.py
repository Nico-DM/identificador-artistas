from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dateutil import parser
from datetime import timezone

def obtener_fecha_js(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)
    driver.get(url)

    try:
        time_element = driver.find_element(By.TAG_NAME, "time")
        datetime_str = time_element.get_attribute("datetime")
        fecha = parser.parse(datetime_str) # type: ignore
        fecha_sin_tz = fecha.astimezone(timezone.utc).replace(tzinfo=None) if fecha.tzinfo else fecha
        return fecha_sin_tz
    except Exception as e:
        print("Error:", str(e).split("\n", maxsplit=1)[0])
        return None
    finally:
        driver.quit()

# Ejemplo
if __name__ == "__main__":
    url = "https://x.com/_Woong_Bi_/status/1940043620599603367"
    fecha = obtener_fecha_js(url)
    print("Fecha extraída:", fecha)
