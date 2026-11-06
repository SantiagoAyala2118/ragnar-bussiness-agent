from datetime import datetime

import requests
from google.adk.tools import ToolContext

from ..configuration import MONEDA_COMPETENCIA
from ..utils import (
    consultar_json,
    extraer_oferta,
    obtener_supermercado,
    puede_consultarse,
    recortar_texto,
    respuesta_error,
    respuesta_ok,
    respuesta_vacia,
    url_api_por_producto,
)


def obtener_precio_competidor(url: str, tool_context: ToolContext) -> dict:
    """
    Herramienta para obtener el precio real de un producto desde su pagina en un supermercado competidor.
    Devuelve nombre, marca, precio actual, precio regular, promociones, disponibilidad, fuente y fecha.
    Utilizala con las URLs que devuelve buscar_productos_competencia, antes de registrar un resultado.
    Args:
        url: str -> URL de la pagina del producto (ej: "https://www.jumbo.com.ar/gaseosa-coca-cola-1-5-lt/p").
    """
    # 1. Validar: solo sitios permitidos y paginas de producto
    supermercado = obtener_supermercado(url)
    if supermercado is None:
        return respuesta_error("La URL no pertenece a un supermercado permitido.")
    if not url.rstrip("/").endswith("/p"):
        return respuesta_error("La URL no es la pagina de un producto (debe terminar en /p).")

    # 2. Respetar las condiciones de acceso del sitio
    url_api = url_api_por_producto(url)
    try:
        if not puede_consultarse(url_api):
            return respuesta_error(f"El sitio de {supermercado} no permite consultas automatizadas (robots.txt).")
        productos = consultar_json(url_api)
    except (requests.exceptions.RequestException, ValueError) as e:
        print("Error interno al utilizar la herramienta", e)
        return respuesta_error(f"No se pudo consultar el sitio de {supermercado}: {e}")

    if not productos:
        return respuesta_vacia(f"El producto ya no esta publicado en {supermercado}.")

    # 3. Extraer los datos del producto
    producto = productos[0]
    try:
        oferta = extraer_oferta(producto)
    except (KeyError, IndexError):
        return respuesta_vacia(f"{supermercado} no informa el precio de este producto.")
    if not oferta["precio_actual"]:
        return respuesta_vacia(f"{supermercado} no informa el precio de este producto.")

    datos = {
        "supermercado": supermercado,
        "nombre": recortar_texto(producto.get("productName", "")),
        "marca": recortar_texto(producto.get("brand", "")),
        **oferta,
        "en_promocion": oferta["precio_actual"] < oferta["precio_regular"] or bool(oferta["promociones"]),
        "moneda": MONEDA_COMPETENCIA,
        "url": url,
        "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    # 4. Guardar en la sesion: es la fuente de verdad para registrar_resultado
    precios_consultados = tool_context.state.get("precios_consultados", {})
    precios_consultados[url] = datos
    tool_context.state["precios_consultados"] = precios_consultados

    return respuesta_ok(**datos)