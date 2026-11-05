import re

# --- Modelo ---
URL_OLLAMA = "http://localhost:11434"
MODELO = "ollama_chat/gemma4:31b-cloud"

# --- Busqueda en la competencia ---
# Lista cerrada de competidores: el agente solo puede buscar en estos sitios
SUPERMERCADOS = {
    "carrefour": "carrefour.com.ar",
    "jumbo": "jumbo.com.ar",
    "disco": "disco.com.ar",
    "vea": "vea.com.ar",
    "dia": "supermercadosdia.com.ar",
    "changomas": "masonline.com.ar",
}
REGION_BUSQUEDA = "ar-es"
MAX_RESULTADOS_PERMITIDOS = 10
LARGO_MAXIMO_TEXTO = 300  # recorta textos externos para limitar contenido malicioso o innecesario

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