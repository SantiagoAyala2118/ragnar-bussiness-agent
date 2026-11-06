import re

# Un numero con separadores de miles o decimales: "2745", "2.745,14", "3945.0"
PATRON_NUMERO = re.compile(r"\d+(?:[.,]\d+)*")
# Montos en una respuesta: "$2.745,14", "-$83,86", "30,41%", "4500 pesos"
PATRON_MONTO = re.compile(r"\$\s*-?\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:%|pesos\b|ars\b)", re.IGNORECASE)


def interpretar_numero(texto: str) -> list[tuple[float, int]]:
    """
    Devuelve las lecturas posibles de un numero escrito como texto, con su cantidad de decimales.
    Se prueban el formato argentino ("2.745,14") y el ingles ("2745.14").
    Ejemplo: "2.745,14" -> [(2745.14, 2), (2.74514, 5)].
    """
    lecturas = []
    for candidato in (texto.replace(".", "").replace(",", "."), texto.replace(",", "")):
        try:
            valor = float(candidato)
        except ValueError:
            continue
        decimales = len(candidato.split(".")[1]) if "." in candidato else 0
        if (valor, decimales) not in lecturas:
            lecturas.append((valor, decimales))
    return lecturas


def recolectar_numeros(dato: object) -> set[float]:
    """
    Junta todos los numeros que aparecen en un dato (dict, lista, texto o numero), en valor absoluto.
    Se usa para saber que valores devolvieron las herramientas.
    """
    if isinstance(dato, bool) or dato is None:
        return set()
    if isinstance(dato, (int, float)):
        return {round(abs(float(dato)), 2)}
    if isinstance(dato, dict):
        dato = list(dato.values())
    if isinstance(dato, (list, tuple, set)):
        return set().union(*(recolectar_numeros(elemento) for elemento in dato)) if dato else set()
    numeros = set()
    for token in PATRON_NUMERO.findall(str(dato)):
        numeros.update(round(valor, 2) for valor, _ in interpretar_numero(token))
    return numeros


def extraer_montos(texto: str) -> list[str]:
    """
    Devuelve los precios y porcentajes escritos en un texto, tal como aparecen.
    Ejemplo: "Ragnar sale $2.745,14, un 30,41% menos" -> ["2.745,14", "30,41"].
    """
    return [monto_pesos or monto_otro for monto_pesos, monto_otro in PATRON_MONTO.findall(texto)]


def esta_verificado(monto: str, permitidos: set[float]) -> bool:
    """
    Indica si un monto de la respuesta coincide con algun valor permitido.
    Tolera el redondeo segun los decimales escritos: "$2.745" coincide con 2745.14.
    """
    for valor, decimales in interpretar_numero(monto):
        tolerancia = 0.5 * 10 ** -decimales + 0.001
        if any(abs(valor - permitido) <= tolerancia for permitido in permitidos):
            return True
    return False