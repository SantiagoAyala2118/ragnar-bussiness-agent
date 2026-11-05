from ..configuration import PATRONES_PROMOCION
from ..utils.responses import respuesta_error, respuesta_ok, respuesta_vacia


def detectar_promocion(texto: str = "", precio_regular: float = 0, precio_actual: float = 0) -> dict:
    """
    Herramienta para detectar promociones y descuentos de un producto.
    Analiza el texto del producto (2x1, 3x2, 2da unidad al 70%, 20% off, oferta)
    y, si se informan ambos precios, calcula el descuento entre el precio regular y el actual.
    Utilizala para diferenciar precios regulares de precios promocionales.
    Args:
        texto: str -> Titulo o descripcion del producto en el sitio del competidor.
        precio_regular: float -> Precio de lista sin descuento (0 si se desconoce).
        precio_actual: float -> Precio que se cobra hoy (0 si se desconoce).
    """
    # 1. Validar
    if precio_regular < 0 or precio_actual < 0:
        return respuesta_error("Los precios no pueden ser negativos.")
    hay_precios = precio_regular > 0 and precio_actual > 0
    if not texto.strip() and not hay_precios:
        return respuesta_error("Indica un texto o ambos precios para analizar.")

    # 2. Buscar promociones en el texto
    promociones = []
    for tipo, patron in PATRONES_PROMOCION.items():
        encontrado = patron.search(texto)
        if not encontrado:
            continue
        # "2x1" es promocion solo si N > M (evita confundir "1 x 6 un" con una promo)
        if tipo == "NxM" and int(encontrado.group(1)) <= int(encontrado.group(2)):
            continue
        promociones.append({"tipo": tipo, "texto": encontrado.group(0)})

    # 3. Calcular descuento si el precio actual es menor al regular
    descuento = {}
    if hay_precios and precio_actual < precio_regular:
        porcentaje = (precio_regular - precio_actual) / precio_regular * 100
        descuento = {
            "precio_regular": precio_regular,
            "precio_promocional": precio_actual,
            "descuento_porcentual": round(porcentaje, 2),
        }
        promociones.append({"tipo": "precio rebajado", "texto": f"{porcentaje:.0f}% menos que el precio regular"})

    # 4. Responder
    if not promociones:
        return respuesta_vacia("No se detectaron promociones: el precio se considera regular.", tiene_promocion=False)
    return respuesta_ok(tiene_promocion=True, promociones=promociones, **descuento)