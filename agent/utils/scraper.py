import time
from functools import lru_cache
from urllib.parse import quote, urlparse
from urllib.robotparser import RobotFileParser

import requests

from ..configuration import PAUSA_ENTRE_CONSULTAS, RUTA_API_PRODUCTOS, SUPERMERCADOS, TIEMPO_ESPERA, USER_AGENT


def obtener_supermercado(url: str) -> str | None:
    """
    Devuelve el nombre del supermercado al que pertenece una URL, o None si no esta permitido.
    Ejemplo: "https://www.jumbo.com.ar/yerba/p" -> "jumbo".
    """
    host = urlparse(url).netloc.lower()
    for nombre, dominio in SUPERMERCADOS.items():
        if host == dominio:
            return nombre
    return None


@lru_cache(maxsize=None)
def leer_robots(dominio: str) -> RobotFileParser:
    """
    Descarga y guarda en memoria el robots.txt de un sitio (las reglas de acceso para bots).
    """
    robots = RobotFileParser(f"https://{dominio}/robots.txt")
    robots.read()
    return robots


def puede_consultarse(url: str) -> bool:
    """
    Indica si el robots.txt del sitio permite que nuestro agente consulte esa URL.
    """
    return leer_robots(urlparse(url).netloc).can_fetch(USER_AGENT, url)


def consultar_json(url: str) -> list | dict:
    """
    Hace una consulta GET identificandose con nuestro USER_AGENT y devuelve la respuesta JSON.
    Espera PAUSA_ENTRE_CONSULTAS antes de cada consulta para no sobrecargar el sitio.
    Lanza una excepcion de requests si la consulta falla.
    """
    time.sleep(PAUSA_ENTRE_CONSULTAS)
    respuesta = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIEMPO_ESPERA)
    respuesta.raise_for_status()
    return respuesta.json()


def url_api_por_producto(url_producto: str) -> str:
    """
    Arma la URL de la API publica a partir de la pagina de un producto.
    Ejemplo: ".../gaseosa-coca-cola-1-5-lt/p" -> ".../api/catalog_system/pub/products/search/gaseosa-coca-cola-1-5-lt/p".
    """
    partes = urlparse(url_producto)
    identificador = partes.path.strip("/").removesuffix("/p")
    return f"{partes.scheme}://{partes.netloc}{RUTA_API_PRODUCTOS}/{identificador}/p"


def url_api_por_texto(dominio: str, texto: str, cantidad: int) -> str:
    """
    Arma la URL del buscador publico de un sitio para un texto (ej: "yerba playadito").
    """
    return f"https://{dominio}{RUTA_API_PRODUCTOS}?ft={quote(texto)}&_from=0&_to={cantidad - 1}"


def extraer_oferta(producto: dict) -> dict:
    """
    Extrae de la respuesta de la API los datos de precio del primer articulo del producto:
    precio actual, precio regular (sin descuento), disponibilidad y nombres de promociones.
    """
    articulo = producto["items"][0]
    vendedor = next((v for v in articulo["sellers"] if v.get("sellerDefault")), articulo["sellers"][0])
    oferta = vendedor["commertialOffer"]
    teasers = (oferta.get("Teasers") or []) + (oferta.get("PromotionTeasers") or [])
    return {
        "precio_actual": oferta.get("Price"),
        "precio_regular": oferta.get("PriceWithoutDiscount") or oferta.get("Price"),
        "disponible": bool(oferta.get("IsAvailable")),
        "promociones": [t.get("<Name>k__BackingField") or t.get("Name", "") for t in teasers],
    }