from functools import lru_cache

import pandas as pd

from ..configuration import RUTA_CATALOGO


@lru_cache(maxsize=1)
def cargar_catalogo() -> pd.DataFrame:
    """
    Lee el catalogo de Ragnar desde el CSV una sola vez y lo guarda en memoria.
    Lanza FileNotFoundError si el archivo no existe.
    """
    return pd.read_csv(RUTA_CATALOGO, dtype={"producto_id": str}, encoding="utf-8")


def buscar_producto_por_id(producto_id: str) -> dict | None:
    """
    Devuelve un producto del catalogo como diccionario a partir de su id (ej: "RAG-00001").
    Devuelve None si el id no existe.
    """
    catalogo = cargar_catalogo()
    coincidencias = catalogo[catalogo["producto_id"] == producto_id.strip().upper()]
    if coincidencias.empty:
        return None
    return coincidencias.iloc[0].to_dict()