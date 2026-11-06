import re
from pathlib import Path

# --- Rutas ---
CARPETA_AGENTE = Path(__file__).resolve().parent
RUTA_CATALOGO = CARPETA_AGENTE / "data" / "ragnar_catalog.csv"
CARPETA_INFORMES = CARPETA_AGENTE / "reports"
CARPETA_VECTOR_STORE = CARPETA_AGENTE / "vector_store"

# --- Modelo ---
URL_OLLAMA = "http://localhost:11434"
MODELO = "ollama_chat/gemma4:31b-cloud"

# --- Catalogo de Ragnar ---
MAX_RESULTADOS_CATALOGO = 20
CATEGORIAS = ["Alimentos", "Bebidas", "Limpieza", "Higiene personal", "Hogar"]

# --- Busqueda en la competencia ---
# Lista cerrada de competidores: el agente solo puede consultar estos sitios
SUPERMERCADOS = {
    "carrefour": "www.carrefour.com.ar",
    "jumbo": "www.jumbo.com.ar",
    "disco": "www.disco.com.ar",
    "vea": "www.vea.com.ar",
    "dia": "diaonline.supermercadosdia.com.ar",
    "changomas": "www.masonline.com.ar",
}
REGION_BUSQUEDA = "ar-es"
MAX_RESULTADOS_PERMITIDOS = 10
LARGO_MAXIMO_TEXTO = 300  # recorta textos externos para limitar contenido malicioso o innecesario

# --- Scraper (consultas a los sitios de la competencia) ---
# El agente se identifica honestamente y respeta el robots.txt de cada sitio
USER_AGENT = "RagnarPriceAgent/1.0 (proyecto academico; comparacion de precios)"
TIEMPO_ESPERA = 15  # segundos maximos de espera por respuesta
PAUSA_ENTRE_CONSULTAS = 1.0  # segundos entre consultas, para no sobrecargar los sitios
RUTA_API_PRODUCTOS = "/api/catalog_system/pub/products/search"  # API publica de catalogo (plataforma VTEX)
MONEDA_COMPETENCIA = "ARS"

# --- RAG (historial de investigaciones) ---
MODELO_EMBEDDINGS = "nomic-embed-text"
COLECCION_INVESTIGACIONES = "investigaciones"
TAMANO_FRAGMENTO = 1000
SOLAPAMIENTO_FRAGMENTO = 200

# --- Unidades de medida ---
# Cada unidad aceptada se convierte a una unidad base: (unidad_base, factor de conversion)
CONVERSIONES = {
    "g": ("g", 1),
    "gr": ("g", 1),
    "kg": ("g", 1000),
    "ml": ("ml", 1),
    "cc": ("ml", 1),
    "l": ("ml", 1000),
    "lt": ("ml", 1000),
    "lts": ("ml", 1000),
    "litro": ("ml", 1000),
    "litros": ("ml", 1000),
    "un": ("un", 1),
}
# Unidad en la que se muestran los precios por unidad: (nombre, escala)
UNIDADES_REFERENCIA = {"g": ("kg", 1000), "ml": ("litro", 1000), "un": ("unidad", 1)}

# --- Comparacion ---
DIFERENCIA_SIGNIFICATIVA = 10.0  # porcentaje a partir del cual una diferencia se considera significativa

# --- Coincidencia de productos ---
# Palabras que indican una variante distinta del producto (no es el mismo articulo)
VARIANTES = ["zero", "light", "diet", "sin azucar", "sin tacc", "descremada", "retornable", "combo", "pack", "repuesto"]

# --- Promociones ---
# Patrones de promociones comunes en supermercados argentinos
PATRONES_PROMOCION = {
    "NxM": re.compile(r"\b(\d)\s*x\s*(\d)\b", re.IGNORECASE),  # 2x1, 3x2
    "segunda unidad": re.compile(r"(\d+)\s*%.{0,25}(2da|segunda)|(2da|segunda).{0,25}?(\d+)\s*%", re.IGNORECASE),
    "descuento": re.compile(r"(\d+)\s*%\s*(off|de descuento|dto)", re.IGNORECASE),
    "oferta": re.compile(r"\b(oferta|promo|promocion|precio especial|liquidacion)\b", re.IGNORECASE),
}

# --- Guard (filtro de entrada y salida del agente) ---
MAX_CARACTERES_ENTRADA = 1000  # mensajes mas largos se rechazan (suelen esconder instrucciones)
MAX_CARACTERES_RESPUESTA = 8000  # respuestas mas largas se recortan