import os

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .configuration import MODELO, URL_OLLAMA
from .instructions import INSTRUCCIONES
from .tools import (
    buscar_productos_competencia,
    comparar_precios,
    consultar_catalogo,
    consultar_investigaciones,
    detectar_promocion,
    generar_informe,
    guardar_investigacion,
    obtener_precio_competidor,
    registrar_resultado,
    reiniciar_investigacion,
    verificar_coincidencia,
)

os.environ["OLLAMA_API_BASE"] = URL_OLLAMA

root_agent = Agent(
    model=LiteLlm(MODELO),
    name="agente_ragnar",
    description="Agente que investiga y compara precios de Ragnar S.A. con supermercados competidores.",
    instruction=INSTRUCCIONES,
    tools=[
        consultar_catalogo,
        buscar_productos_competencia,
        obtener_precio_competidor,
        verificar_coincidencia,
        detectar_promocion,
        comparar_precios,
        registrar_resultado,
        reiniciar_investigacion,
        generar_informe,
        guardar_investigacion,
        consultar_investigaciones,
    ],
)