// Textos y datos estaticos del sitio (separados de los componentes)

export const NAVEGACION = [
  { id: 'inicio', texto: 'Inicio' },
  { id: 'funciones', texto: 'Qué hace' },
  { id: 'agente', texto: 'Agente' },
  { id: 'equipo', texto: 'Equipo' },
]

// Cada funcion tiene un atajo: una consulta lista que se le envia al agente.
// Solo usan productos y supermercados que existen y permiten consultas.
export const FUNCIONES = [
  {
    runa: 'ᚱ',
    titulo: 'Catálogo',
    texto: 'Consulta los productos de Ragnar: marca, presentación y precio vigente.',
    atajo: 'Mostrame 5 productos de la categoría Bebidas',
  },
  {
    runa: 'ᚨ',
    titulo: 'Competencia',
    texto: 'Busca el mismo producto en Jumbo, Disco, Vea, Día y Changomás, y verifica que coincida.',
    atajo: 'Compará la yerba Playadito de 500 g con Día y Changomás',
  },
  {
    runa: 'ᚷ',
    titulo: 'Informes',
    texto: 'Calcula diferencias, separa promociones y arma un informe con fuentes y fechas.',
    atajo: 'Generá el informe de la investigación actual',
  },
  {
    runa: 'ᚾ',
    titulo: 'Historial',
    texto: 'Recuerda investigaciones anteriores y responde sobre sus conclusiones.',
    atajo: '¿Qué se concluyó sobre la yerba en investigaciones anteriores?',
  },
]

export const SUGERENCIAS = [
  'Compará la yerba Playadito de 500 g con Día y Changomás',
  '¿Qué gaseosas Coca-Cola vende Ragnar?',
  '¿Qué se concluyó sobre la yerba en investigaciones anteriores?',
]

export const NOMBRES_HERRAMIENTAS = {
  consultar_catalogo: 'Catálogo de Ragnar',
  buscar_productos_competencia: 'Búsqueda en competencia',
  obtener_precio_competidor: 'Precio del competidor',
  verificar_coincidencia: 'Verificación de coincidencia',
  comparar_precios: 'Comparación de precios',
  detectar_promocion: 'Detección de promoción',
  registrar_resultado: 'Registro de resultado',
  reiniciar_investigacion: 'Nueva investigación',
  generar_informe: 'Informe',
  guardar_investigacion: 'Guardado en historial',
  consultar_investigaciones: 'Consulta del historial',
}

export const FRASE_RAGNAR = "Don't waste your time looking back. You're not going that way."

export const EQUIPO = [
  {
    nombre: 'Santiago Ayala',
    redes: {
      github: 'https://github.com/SantiagoAyala2118',
      linkedin: 'https://www.linkedin.com/in/santiago-tom%C3%A1s-ayala-641436390/',
      instagram: 'https://www.instagram.com/ssanti21_/',
    },
  },
  {
    nombre: 'Lucas Zigaran',
    redes: {
      github: 'https://github.com/Simetriq',
      linkedin: 'https://www.linkedin.com/in/lucas-natanael-zigaran-595b44321/',
      instagram: 'https://www.instagram.com/luca.sz9946/',
    },
  },
  {
    nombre: 'Axel Gaona',
    redes: {
      github: 'https://github.com/AxelGaona1453',
      linkedin: 'https://www.linkedin.com/in/axel-gaona-68a009397/',
      instagram: 'https://www.instagram.com/axelgaona_54/',
    },
  },
]
