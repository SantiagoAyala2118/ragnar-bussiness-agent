from google.adk.tools import ToolContext

from ..configuration import SUPERMERCADOS
from ..utils import buscar_producto_por_id, respuesta_error, respuesta_ok
from .coincidense import verificar_coincidencia
from .comparation import comparar_precios


def registrar_resultado(producto_id: str, supermercado: str, tool_context: ToolContext, url: str = "") -> dict:
    """
    Herramienta para registrar en la investigacion actual el resultado de un producto en un supermercado.
    Toma el precio de Ragnar del catalogo y el del competidor de obtener_precio_competidor (nunca de la conversacion),
    verifica la coincidencia y calcula las diferencias. Si el producto no se encontro, llamala sin url.
    Utilizala una vez por cada producto y supermercado investigado, antes de generar_informe.
    Args:
        producto_id: str -> Id del producto de Ragnar (ej: "RAG-00023").
        supermercado: str -> Uno de: carrefour, jumbo, disco, vea, dia, changomas.
        url: str -> URL ya consultada con obtener_precio_competidor. Vacio si el producto no se encontro.
    """
    # 1. Validar
    producto = buscar_producto_por_id(producto_id)
    if producto is None:
        return respuesta_error(f"No existe el producto '{producto_id}' en el catalogo.")
    supermercado = supermercado.strip().lower()
    if supermercado not in SUPERMERCADOS:
        return respuesta_error(f"Supermercado no valido. Opciones: {', '.join(SUPERMERCADOS)}.")
    precio = tool_context.state.get("precios_consultados", {}).get(url) if url else None
    if url and precio is None:
        return respuesta_error("Primero consulta esa URL con obtener_precio_competidor.")

    fila = {
        "producto_id": producto["producto_id"],
        "producto": producto["producto"],
        "marca": producto["marca"],
        "categoria": producto["categoria"],
        "presentacion": producto["presentacion"],
        "precio_ragnar": producto["precio"],
        "supermercado": supermercado,
        "url": url,
        "fecha_consulta": precio["fecha_consulta"] if precio else "",
    }

    # 2. Clasificar el resultado
    if precio is None:
        fila.update(estado="no_encontrado", motivos=["No se encontro el producto en el sitio."])
    else:
        coincidencia = verificar_coincidencia(
            producto["producto"], producto["marca"], producto["contenido"], producto["unidad_medida"], precio["nombre"]
        )
        fila.update(producto_competidor=precio["nombre"], motivos=coincidencia["motivos"])
        if coincidencia["coincidencia"] != "confiable":
            fila["estado"] = "coincidencia_no_confiable"
        elif not precio["disponible"]:
            # Los sitios suelen mostrar precios desactualizados en productos sin stock
            fila.update(estado="sin_stock", motivos=["El producto figura sin stock: su precio no se considera confiable."])
        else:
            # 3. Comparar contra el precio regular (mismo contenido, porque la coincidencia es confiable)
            comparacion = comparar_precios(
                producto["precio"], producto["contenido"], producto["unidad_medida"],
                precio["precio_regular"], producto["contenido"], producto["unidad_medida"],
            )
            fila.update(
                estado="comparado",
                precio_regular=precio["precio_regular"],
                precio_promocional=precio["precio_actual"] if precio["en_promocion"] else None,
                promociones=precio["promociones"],
                diferencia_absoluta=comparacion["diferencia_absoluta_precio"],
                diferencia_porcentual=comparacion["diferencia_porcentual"],
                posicion=comparacion["posicion"],
                diferencia_significativa=comparacion["diferencia_significativa"],
            )

    # 4. Guardar en la investigacion de la sesion (reemplaza si ya estaba ese producto y supermercado)
    investigacion = [
        f for f in tool_context.state.get("investigacion", [])
        if not (f["producto_id"] == fila["producto_id"] and f["supermercado"] == supermercado)
    ]
    investigacion.append(fila)
    tool_context.state["investigacion"] = investigacion

    return respuesta_ok(registrados=len(investigacion), resultado=fila)


def reiniciar_investigacion(tool_context: ToolContext) -> dict:
    """
    Herramienta para borrar los resultados registrados y empezar una investigacion nueva.
    Utilizala solo cuando el usuario pida una investigacion nueva o distinta a la actual.
    """
    tool_context.state["investigacion"] = []
    tool_context.state["precios_consultados"] = {}
    return respuesta_ok(mensaje="Investigacion reiniciada.")