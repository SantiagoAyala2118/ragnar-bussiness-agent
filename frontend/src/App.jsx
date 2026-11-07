import { useEffect, useRef, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { borrarSesion, enviarMensaje } from './api'
import './App.css'

const SUGERENCIAS = [
  'Buscá el precio de Coca-Cola 2,25 L en Carrefour y Jumbo',
  '¿Hay promociones de yerba Playadito 1 kg en Día?',
  'Compará aceite Natura 1,5 L en Vea y Changomás',
]

const NOMBRES_HERRAMIENTAS = {
  buscar_productos_competencia: 'Búsqueda en competencia',
  verificar_coincidencia: 'Verificación de coincidencia',
  comparar_precios: 'Comparación de precios',
  detectar_promocion: 'Detección de promoción',
}

function Mensaje({ mensaje }) {
  const { role, text, toolCalls, error } = mensaje
  return (
    <div className={`mensaje ${role} ${error ? 'error' : ''}`}>
      <div className="burbuja">
        {role === 'agent' ? (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              a: (props) => <a {...props} target="_blank" rel="noreferrer" />,
            }}
          >
            {text}
          </ReactMarkdown>
        ) : (
          <p>{text}</p>
        )}
        {toolCalls?.length > 0 && (
          <details className="herramientas">
            <summary>{toolCalls.length} herramienta(s) usada(s)</summary>
            <ul>
              {toolCalls.map((t, i) => (
                <li key={i}>
                  <strong>{NOMBRES_HERRAMIENTAS[t.name] || t.name}</strong>
                  <code>{JSON.stringify(t.args)}</code>
                </li>
              ))}
            </ul>
          </details>
        )}
      </div>
    </div>
  )
}

export default function App() {
  const [mensajes, setMensajes] = useState([])
  const [input, setInput] = useState('')
  const [cargando, setCargando] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const finRef = useRef(null)

  useEffect(() => {
    finRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [mensajes, cargando])

  async function enviar(texto) {
    const message = texto.trim()
    if (!message || cargando) return
    setInput('')
    setMensajes((m) => [...m, { role: 'user', text: message }])
    setCargando(true)
    try {
      const data = await enviarMensaje(message, sessionId)
      setSessionId(data.session_id)
      setMensajes((m) => [
        ...m,
        { role: 'agent', text: data.reply, toolCalls: data.tool_calls },
      ])
    } catch (err) {
      setMensajes((m) => [
        ...m,
        { role: 'agent', text: `⚠️ ${err.message}`, error: true },
      ])
    } finally {
      setCargando(false)
    }
  }

  function nuevaConversacion() {
    if (sessionId) borrarSesion(sessionId)
    setSessionId(null)
    setMensajes([])
  }

  function onKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      enviar(input)
    }
  }

  return (
    <div className="app">
      <header>
        <div>
          <h1>Ragnar S.A.</h1>
          <span>Agente de inteligencia de precios</span>
        </div>
        <button className="secundario" onClick={nuevaConversacion} disabled={cargando}>
          Nueva conversación
        </button>
      </header>

      <main className="chat">
        {mensajes.length === 0 && (
          <div className="vacio">
            <h2>¿Qué producto querés comparar?</h2>
            <p>Busco precios en Carrefour, Jumbo, Disco, Vea, Día y Changomás.</p>
            <div className="sugerencias">
              {SUGERENCIAS.map((s) => (
                <button key={s} onClick={() => enviar(s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}
        {mensajes.map((m, i) => (
          <Mensaje key={i} mensaje={m} />
        ))}
        {cargando && (
          <div className="mensaje agent">
            <div className="burbuja escribiendo" aria-label="El agente está pensando">
              <span />
              <span />
              <span />
            </div>
          </div>
        )}
        <div ref={finRef} />
      </main>

      <form
        className="entrada"
        onSubmit={(e) => {
          e.preventDefault()
          enviar(input)
        }}
      >
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Escribí tu consulta… (Enter envía, Shift+Enter nueva línea)"
          rows={1}
          disabled={cargando}
        />
        <button type="submit" disabled={cargando || !input.trim()}>
          Enviar
        </button>
      </form>
    </div>
  )
}
