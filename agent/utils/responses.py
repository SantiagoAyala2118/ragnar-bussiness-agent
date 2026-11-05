from typing import Any


def respuesta_ok(**datos: Any) -> dict:
    """
    Arma la respuesta de una herramienta que se ejecuto correctamente.
    Ejemplo: respuesta_ok(cantidad=2) -> {"status": "ok", "cantidad": 2}
    """
    return {"status": "ok", **datos}


def respuesta_vacia(mensaje: str, **datos: Any) -> dict:
    """
    Arma la respuesta de una herramienta que no encontro resultados.
    Ejemplo: respuesta_vacia("Sin resultados") -> {"status": "vacio", "mensaje": "Sin resultados"}
    """
    return {"status": "vacio", "mensaje": mensaje, **datos}


def respuesta_error(mensaje: str) -> dict:
    """
    Arma la respuesta de una herramienta que fallo o recibio argumentos invalidos.
    Ejemplo: respuesta_error("Precio invalido") -> {"status": "error", "mensaje": "Precio invalido"}
    """
    return {"status": "error", "mensaje": mensaje}