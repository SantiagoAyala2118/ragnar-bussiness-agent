import unicodedata

from ..configuration import LARGO_MAXIMO_TEXTO


def simplificar_texto(texto: str) -> str:
    """
    Pasa un texto a minusculas, sin tildes ni guiones, para comparar nombres.
    Ejemplo: "La Serenisima Coca-Cola" -> "la serenisima coca cola".
    """
    sin_tildes = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sin_tildes.lower().replace("-", " ")


def recortar_texto(texto: str) -> str:
    """
    Recorta un texto externo (de una web) al largo maximo permitido.
    Limita el contenido malicioso o innecesario que llega al modelo.
    """
    return texto.strip()[:LARGO_MAXIMO_TEXTO]