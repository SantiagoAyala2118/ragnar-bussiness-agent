import os

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

from .configuration import MODELO, URL_OLLAMA
from .instructions import INSTRUCCIONES
from .tools import (
    buscar_productos_competencia,
    comparar_precios,
    detectar_promocion,
    verificar_coincidencia,
)

os.environ["OLLAMA_API_BASE"] = URL_OLLAMA

root_agent = Agent(
    model=LiteLlm(MODELO),
    name="agente_ragnar",
    description="Agente que investiga y compara precios de Ragnar S.A. con supermercados competidores.",
    instruction=INSTRUCCIONES,
    tools=[
        buscar_productos_competencia,
        verificar_coincidencia,
        comparar_precios,
        detectar_promocion,
    ],
)