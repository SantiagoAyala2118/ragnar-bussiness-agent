import re

from ..configuration import CONVERSIONES

# Busca cantidades como "1 kg", "1,5 L", "500gr", "x 6 un"
PATRON_CONTENIDO = re.compile(r"(\d+(?:[.,]\d+)?)\s*(kg|gr|g|ml|cc|litros|litro|lts|lt|l|un)\b", re.IGNORECASE)


def normalizar_unidad(contenido: float, unidad: str) -> tuple[float, str] | None:
    """
    Convierte un contenido a su unidad base (g, ml o un).
    Ejemplo: (1.5, "l") -> (1500.0, "ml").
    Devuelve None si la unidad no es reconocida.
    """
    unidad = unidad.strip().lower()
    if unidad not in CONVERSIONES:
        return None
    unidad_base, factor = CONVERSIONES[unidad]
    return contenido * factor, unidad_base


def extraer_contenido(texto: str) -> tuple[float, str] | None:
    """
    Busca la primera cantidad con unidad dentro de un texto y la normaliza.
    Ejemplo: "Yerba Playadito 1 Kg." -> (1000.0, "g").
    Devuelve None si no encuentra ninguna.
    """
    coincidencia = PATRON_CONTENIDO.search(texto)
    if not coincidencia:
        return None
    numero = float(coincidencia.group(1).replace(",", "."))
    return normalizar_unidad(numero, coincidencia.group(2))