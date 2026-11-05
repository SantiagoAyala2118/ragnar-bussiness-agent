from ..configuration import VARIANTES
from ..utils import extraer_contenido, normalizar_unidad, respuesta_error, respuesta_ok, simplificar_texto


def verificar_coincidencia(
    producto_ragnar: str,
    marca_ragnar: str,
    contenido_ragnar: float,
    unidad_ragnar: str,
    titulo_competidor: str,
) -> dict:
    """
    Herramienta para verificar si un producto de un competidor es el mismo articulo que el de Ragnar.
    Compara marca, contenido neto, unidad de medida y variantes (zero, light, retornable, etc.).
    Utilizala SIEMPRE antes de comparar precios.
    Args:
        producto_ragnar: str -> Nombre del producto de Ragnar (ej: "Gaseosa cola").
        marca_ragnar: str -> Marca del producto de Ragnar (ej: "Coca-Cola").
        contenido_ragnar: float -> Contenido neto del producto de Ragnar (ej: 1500).
        unidad_ragnar: str -> Unidad del contenido de Ragnar: g, kg, ml, cc, l, lt o un.
        titulo_competidor: str -> Titulo del producto tal como aparece en el sitio del competidor.
    """
    # 1. Validar
    if not titulo_competidor.strip() or not marca_ragnar.strip():
        return respuesta_error("La marca de Ragnar y el titulo del competidor son obligatorios.")
    contenido_ragnar_base = normalizar_unidad(contenido_ragnar, unidad_ragnar)
    if contenido_ragnar_base is None:
        return respuesta_error(f"Unidad no reconocida: {unidad_ragnar}.")

    titulo = simplificar_texto(titulo_competidor)
    nombre_ragnar = simplificar_texto(f"{producto_ragnar} {marca_ragnar}")
    motivos = []

    # 2. Comparar marca
    marca_coincide = simplificar_texto(marca_ragnar) in titulo
    if not marca_coincide:
        motivos.append(f"La marca '{marca_ragnar}' no aparece en el titulo.")

    # 3. Comparar contenido neto y unidad
    contenido_competidor = extraer_contenido(titulo_competidor)
    if contenido_competidor is None:
        motivos.append("No se pudo leer el contenido neto en el titulo del competidor.")
    elif contenido_competidor != contenido_ragnar_base:
        motivos.append(
            f"Contenido distinto: Ragnar {contenido_ragnar_base[0]:g} {contenido_ragnar_base[1]}, "
            f"competidor {contenido_competidor[0]:g} {contenido_competidor[1]}."
        )

    # 4. Buscar variantes que estan en el competidor pero no en Ragnar
    variantes_distintas = [v for v in VARIANTES if v in titulo and v not in nombre_ragnar]
    if variantes_distintas:
        motivos.append(f"Variante distinta: {', '.join(variantes_distintas)}.")

    # 5. Decidir el nivel de coincidencia
    if not motivos:
        nivel = "confiable"
    elif not marca_coincide or variantes_distintas or contenido_competidor is not None:
        nivel = "no_coincide"
    else:
        nivel = "dudosa"  # solo falto leer el contenido: requiere revision

    return respuesta_ok(coincidencia=nivel, motivos=motivos or ["Marca, contenido y variante coinciden."])