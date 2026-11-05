from ..configuration import CONVERSIONES, DIFERENCIA_SIGNIFICATIVA, UNIDADES_REFERENCIA
from ..utils.responses import respuesta_error, respuesta_ok
from ..utils.units import normalizar_unidad


def comparar_precios(
    precio_ragnar: float,
    contenido_ragnar: float,
    unidad_ragnar: str,
    precio_competidor: float,
    contenido_competidor: float,
    unidad_competidor: str,
) -> dict:
    """
    Herramienta para comparar el precio de un producto de Ragnar con el de un competidor.
    Normaliza ambos precios por unidad de medida y calcula la diferencia absoluta y porcentual.
    Utilizala SIEMPRE que necesites comparar precios, en lugar de hacer cuentas por tu cuenta.
    Args:
        precio_ragnar: float -> Precio del producto en Ragnar.
        contenido_ragnar: float -> Contenido neto del producto de Ragnar (ej: 1000).
        unidad_ragnar: str -> Unidad del contenido de Ragnar: g, kg, ml, cc, l, lt o un.
        precio_competidor: float -> Precio del producto en el competidor.
        contenido_competidor: float -> Contenido neto del producto del competidor.
        unidad_competidor: str -> Unidad del contenido del competidor: g, kg, ml, cc, l, lt o un.
    """
    # 1. Validar
    if precio_ragnar <= 0 or precio_competidor <= 0:
        return respuesta_error("Los precios deben ser mayores a 0.")
    if contenido_ragnar <= 0 or contenido_competidor <= 0:
        return respuesta_error("Los contenidos deben ser mayores a 0.")

    normalizado_ragnar = normalizar_unidad(contenido_ragnar, unidad_ragnar)
    normalizado_competidor = normalizar_unidad(contenido_competidor, unidad_competidor)
    if normalizado_ragnar is None or normalizado_competidor is None:
        return respuesta_error(f"Unidad no reconocida. Unidades validas: {', '.join(CONVERSIONES)}.")

    cantidad_ragnar, unidad_base = normalizado_ragnar
    cantidad_competidor, unidad_base_competidor = normalizado_competidor
    if unidad_base != unidad_base_competidor:
        return respuesta_error(f"No se pueden comparar unidades distintas: {unidad_base} y {unidad_base_competidor}.")

    # 2. Calcular (precio por kg, por litro o por unidad)
    unidad_referencia, escala = UNIDADES_REFERENCIA[unidad_base]
    precio_unitario_ragnar = precio_ragnar / cantidad_ragnar * escala
    precio_unitario_competidor = precio_competidor / cantidad_competidor * escala
    diferencia_absoluta = precio_unitario_ragnar - precio_unitario_competidor
    diferencia_porcentual = diferencia_absoluta / precio_unitario_competidor * 100

    if diferencia_porcentual > 0:
        posicion = "Ragnar es mas caro"
    elif diferencia_porcentual < 0:
        posicion = "Ragnar es mas barato"
    else:
        posicion = "Mismo precio"

    # 3. Responder
    return respuesta_ok(
        unidad_referencia=unidad_referencia,
        precio_por_unidad_ragnar=round(precio_unitario_ragnar, 2),
        precio_por_unidad_competidor=round(precio_unitario_competidor, 2),
        diferencia_absoluta_por_unidad=round(diferencia_absoluta, 2),
        diferencia_porcentual=round(diferencia_porcentual, 2),
        posicion=posicion,
        diferencia_significativa=abs(diferencia_porcentual) >= DIFERENCIA_SIGNIFICATIVA,
        misma_presentacion=cantidad_ragnar == cantidad_competidor,
    )