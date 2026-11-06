from .catalog import consultar_catalogo
from .coincidense import verificar_coincidencia
from .comparation import comparar_precios
from .memory import consultar_investigaciones, guardar_investigacion
from .prices import obtener_precio_competidor
from .promotions import detectar_promocion
from .report import generar_informe
from .research import registrar_resultado, reiniciar_investigacion
from .search import buscar_productos_competencia

__all__ = [
    "consultar_catalogo",
    "buscar_productos_competencia",
    "obtener_precio_competidor",
    "verificar_coincidencia",
    "detectar_promocion",
    "comparar_precios",
    "registrar_resultado",
    "reiniciar_investigacion",
    "generar_informe",
    "guardar_investigacion",
    "consultar_investigaciones",
]