import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import logo from '../assets/ragnar_logo_light.png'
import { NOMBRES_HERRAMIENTAS } from '../data/contenido'

const COMPONENTES_MARKDOWN = {
  a: (props) => <a {...props} target="_blank" rel="noreferrer" />,
  table: (props) => (
    <div className="tabla-contenedor">
      <table {...props} />
    </div>
  ),
}

export function AvatarAgente() {
  return (
    <span className="flex size-10 shrink-0 items-center justify-center rounded-full border border-cuero/60 bg-corteza">
      <img src={logo} alt="" className="h-7 w-auto" />
    </span>
  )
}

/** Agrupa las herramientas usadas: { nombre, veces } en orden de aparicion. */
function agruparHerramientas(toolCalls) {
  const conteo = new Map()
  for (const { name } of toolCalls) conteo.set(name, (conteo.get(name) || 0) + 1)
  return [...conteo].map(([nombre, veces]) => ({ nombre, veces }))
}

function Herramientas({ toolCalls }) {
  if (!toolCalls?.length) return null
  return (
    <ul className="mb-4 flex flex-wrap gap-2" aria-label="Herramientas usadas">
      {agruparHerramientas(toolCalls).map(({ nombre, veces }) => (
        <li
          key={nombre}
          className="flex items-center gap-1.5 rounded-full border border-petroleo/70 bg-noche px-3 py-1 text-[11px] text-hielo"
        >
          <span className="font-runa text-ambar" aria-hidden="true">ᛟ</span>
          {NOMBRES_HERRAMIENTAS[nombre] || nombre}
          {veces > 1 && <span className="text-crema/50">×{veces}</span>}
        </li>
      ))}
    </ul>
  )
}

/** Un mensaje del chat: burbuja del usuario o tarjeta del agente con markdown. */
export default function Mensaje({ mensaje }) {
  const { role, text, toolCalls, error } = mensaje

  if (role === 'user') {
    return (
      <div className="flex justify-end">
        <p className="max-w-[85%] whitespace-pre-wrap rounded-2xl rounded-br-sm bg-bosque/80 px-4 py-3 text-sm leading-relaxed text-crema sm:max-w-[70%]">
          {text}
        </p>
      </div>
    )
  }

  return (
    <div className="flex gap-3">
      <AvatarAgente />
      <div
        className={`min-w-0 flex-1 rounded-2xl rounded-tl-sm border-l-2 px-5 py-4 ${
          error ? 'border-sangre bg-sangre/10' : 'border-cuero bg-musgo/70'
        }`}
      >
        <Herramientas toolCalls={toolCalls} />
        <div className="respuesta-agente">
          <ReactMarkdown remarkPlugins={[remarkGfm]} components={COMPONENTES_MARKDOWN}>
            {text}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
