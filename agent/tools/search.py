from datetime import datetime

import requests
from ddgs import DDGS

from ..configuration import MAX_RESULTADOS_PERMITIDOS, REGION_BUSQUEDA, SUPERMERCADOS
from ..utils import consultar_json, puede_consultarse, recortar_texto, respuesta_error, respuesta_ok, respuesta_vacia, url_api_por_texto


def buscar_con_ddgs(producto: str, dominio: str, max_resultados: int) -> list[dict]:
    """
    Busca el producto en internet con DuckDuckGo, limitado al sitio del supermercado.
    Devuelve una lista de {titulo, url} solo con paginas de producto. Lista vacia si no hay resultados.
    """
    try:
        resultados = DDGS().text(f"{producto} site:{dominio}", region=REGION_BUSQUEDA, max_results=max_resultados)
    except Exception as e:
        print("Busqueda en DDGS sin resultados o con error:", e)
        return []
    return [
        {"titulo": r.get("title", ""), "url": r.get("href", "")}
        for r in resultados
        if dominio in r.get("href", "") and r.get("href", "").rstrip("/").endswith("/p")
    ]


def buscar_en_sitio(producto: str, dominio: str, max_resultados: int) -> list[dict]:
    """
    Busca el producto con el buscador publico del propio sitio (respaldo si DDGS no encuentra nada).
    Respeta el robots.txt. Devuelve una lista de {titulo, url}.
    """
    url = url_api_por_texto(dominio, producto, max_resultados)
    try:
        if not puede_consultarse(url):
            return []
        productos = consultar_json(url)
    except (requests.exceptions.RequestException, ValueError) as e:
        print("Error interno al buscar en el sitio", e)
        return []
    return [{"titulo": p.get("productName", ""), "url": p.get("link", "")} for p in productos]


def buscar_productos_competencia(producto: str, supermercado: str, max_resultados: int = 5) -> dict:
    """
    Herramienta para buscar un producto en el sitio web de un supermercado competidor.
    Devuelve titulo, URL de la pagina del producto, origen de la busqueda y fecha de consulta.
    No devuelve precios: para eso usa obtener_precio_competidor con la URL.
    Utilizala una vez por cada supermercado que quieras consultar.
    Args:
        producto: str -> Producto a buscar, con marca y presentacion (ej: "yerba Playadito 1 kg").
        supermercado: str -> Uno de: carrefour, jumbo, disco, vea, dia, changomas.
        max_resultados: int -> Cantidad maxima de resultados (entre 1 y 10).
    """
    # 1. Validar
    supermercado = supermercado.strip().lower()
    if supermercado not in SUPERMERCADOS:
        return respuesta_error(f"Supermercado no valido. Opciones: {', '.join(SUPERMERCADOS)}.")
    if len(producto.strip()) < 3:
        return respuesta_error("El producto debe tener al menos 3 caracteres.")
    if not 1 <= max_resultados <= MAX_RESULTADOS_PERMITIDOS:
        return respuesta_error(f"max_resultados debe estar entre 1 y {MAX_RESULTADOS_PERMITIDOS}.")

    # 2. Buscar: primero en internet (DDGS) y, si no hay resultados, en el buscador del sitio
    dominio = SUPERMERCADOS[supermercado]
    resultados, origen = buscar_con_ddgs(producto.strip(), dominio, max_resultados), "ddgs"
    if not resultados:
        resultados, origen = buscar_en_sitio(producto.strip(), dominio, max_resultados), "buscador del sitio"

    # 3. Responder
    if not resultados:
        return respuesta_vacia(f"No se encontro '{producto}' en {supermercado}.")
    fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M")
    productos = [
        {
            "supermercado": supermercado,
            "titulo": recortar_texto(r["titulo"]),
            "url": r["url"],
            "origen": origen,
            "fecha_consulta": fecha_consulta,
        }
        for r in resultados
    ]
    return respuesta_ok(cantidad=len(productos), productos=productos)