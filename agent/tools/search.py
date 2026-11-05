from datetime import datetime

from ddgs import DDGS

from ..configuration import MAX_RESULTADOS_PERMITIDOS, REGION_BUSQUEDA, SUPERMERCADOS
from ..utils import recortar_texto, respuesta_error, respuesta_ok, respuesta_vacia


def buscar_productos_competencia(producto: str, supermercado: str, max_resultados: int = 5) -> dict:
    """
    Herramienta para buscar un producto en el sitio web de un supermercado competidor.
    Devuelve titulo, enlace, fragmento de texto y fecha de consulta de cada resultado.
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

    # 2. Buscar solo dentro del sitio del supermercado
    dominio = SUPERMERCADOS[supermercado]
    sin_resultados = f"No se encontro '{producto}' en {supermercado}."
    try:
        resultados = DDGS().text(f"{producto.strip()} site:{dominio}", region=REGION_BUSQUEDA, max_results=max_resultados)
    except Exception as e:
        if "No results found" in str(e):  # ddgs lanza una excepcion cuando no hay resultados
            return respuesta_vacia(sin_resultados)
        print("Error interno al utilizar la herramienta", e)
        return respuesta_error(f"No se pudo realizar la busqueda: {e}")

    # 3. Armar resultados (descarta los que no son del sitio permitido)
    fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M")
    productos = [
        {
            "supermercado": supermercado,
            "titulo": recortar_texto(resultado.get("title", "")),
            "url": resultado.get("href", ""),
            "fragmento": recortar_texto(resultado.get("body", "")),
            "fecha_consulta": fecha_consulta,
        }
        for resultado in resultados
        if dominio in resultado.get("href", "")
    ]

    # 4. Responder
    if not productos:
        return respuesta_vacia(sin_resultados)
    return respuesta_ok(cantidad=len(productos), productos=productos)