import re

from ..configuration import CATEGORIAS, MAX_RESULTADOS_CATALOGO
from ..utils import buscar_producto_por_id, cargar_catalogo, respuesta_error, respuesta_ok, respuesta_vacia, simplificar_texto


def consultar_catalogo(texto: str = "", categoria: str = "", producto_id: str = "", max_resultados: int = 10) -> dict:
    """
    Herramienta para consultar el catalogo de productos de Ragnar (precio, marca, presentacion, etc.).
    Busca por id, por texto (nombre, marca o presentacion) y/o por categoria.
    Utilizala SIEMPRE para obtener los datos y el precio de Ragnar antes de investigar a la competencia.
    Args:
        texto: str -> Palabras a buscar en nombre, marca o presentacion (ej: "yerba playadito 1000 g").
        categoria: str -> Una de: Alimentos, Bebidas, Limpieza, Higiene personal, Hogar. Vacio para todas.
        producto_id: str -> Id exacto del producto (ej: "RAG-00023"). Si se indica, se ignoran los demas filtros.
        max_resultados: int -> Cantidad maxima de productos a devolver (entre 1 y 20).
    """
    # 1. Validar
    if not texto.strip() and not categoria.strip() and not producto_id.strip():
        return respuesta_error("Indica un texto, una categoria o un producto_id para buscar.")
    if not 1 <= max_resultados <= MAX_RESULTADOS_CATALOGO:
        return respuesta_error(f"max_resultados debe estar entre 1 y {MAX_RESULTADOS_CATALOGO}.")
    categorias_validas = {simplificar_texto(c): c for c in CATEGORIAS}
    if categoria.strip() and simplificar_texto(categoria) not in categorias_validas:
        return respuesta_error(f"Categoria no valida. Opciones: {', '.join(CATEGORIAS)}.")

    try:
        catalogo = cargar_catalogo()
    except (OSError, ValueError) as e:
        print("Error interno al utilizar la herramienta", e)
        return respuesta_error(f"No se pudo leer el catalogo de Ragnar: {e}")

    # 2. Buscar por id (busqueda exacta)
    if producto_id.strip():
        producto = buscar_producto_por_id(producto_id)
        if producto is None:
            return respuesta_vacia(f"No existe el producto '{producto_id}' en el catalogo.")
        return respuesta_ok(cantidad=1, productos=[producto])

    # 3. Filtrar por categoria y por palabras completas (todas deben aparecer: "500" no coincide con "1500")
    resultados = catalogo
    if categoria.strip():
        resultados = resultados[resultados["categoria"] == categorias_validas[simplificar_texto(categoria)]]
    if texto.strip():
        descripcion = (resultados["producto"] + " " + resultados["marca"] + " " + resultados["presentacion"]).map(simplificar_texto)
        for palabra in simplificar_texto(texto).split():
            patron = rf"\b{re.escape(palabra)}"  # la palabra debe empezar en un limite: "yerb" sigue encontrando "yerba"
            resultados = resultados[descripcion.str.contains(patron, regex=True)]
            descripcion = descripcion[resultados.index]

    # 4. Responder
    if resultados.empty:
        return respuesta_vacia("No se encontraron productos con esos filtros en el catalogo de Ragnar.")
    return respuesta_ok(
        cantidad_total=len(resultados),
        cantidad=min(len(resultados), max_resultados),
        productos=resultados.head(max_resultados).to_dict(orient="records"),
    )