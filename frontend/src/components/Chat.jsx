import { forwardRef, useEffect, useRef, useState } from 'react'
import { SUGERENCIAS } from '../data/contenido'
import Mensaje, { AvatarAgente } from './Mensaje'

function Escribiendo() {
  return (
    <div className="flex items-center gap-3" role="status" aria-label="El agente está investigando">
      <AvatarAgente />
      <div className="flex items-center gap-3 rounded-2xl rounded-tl-sm border-l-2 border-cuero bg-musgo/70 px-5 py-4">
        {[0, 1, 2].map((i) => (
          <span key={i} className="punto-latido size-2 rounded-full bg-ambar" style={{ animationDelay: `${i * 0.18}s` }} />
        ))}
        <span className="text-xs text-crema/60">Ragnar está investigando…</span>
      </div>
    </div>
  )
}

function Vacio({ onEnviar }) {
  return (
    <div className="flex h-full flex-col items-center justify-center px-4 text-center">
      <span className="font-runa text-5xl text-cuero" aria-hidden="true">ᚱᚨᚷᚾᚨᚱ</span>
      <h3 className="mt-6 font-titulo text-2xl font-semibold text-crema">¿Qué producto querés investigar?</h3>
      <p className="mt-3 max-w-md text-sm text-crema/60">
        Busco precios en Jumbo, Disco, Vea, Día y Changomás, y los comparo con el catálogo de Ragnar.
      </p>
      <div className="mt-8 flex max-w-2xl flex-wrap justify-center gap-3">
        {SUGERENCIAS.map((sugerencia) => (
          <button
            key={sugerencia}
            type="button"
            onClick={() => onEnviar(sugerencia)}
            className="rounded-full border border-petroleo bg-noche px-4 py-2 text-left text-sm text-hielo transition-colors hover:border-ambar hover:text-crema"
          >
            {sugerencia}
          </button>
        ))}
      </div>
    </div>
  )
}

/** Seccion del agente: panel con scroll propio, asi la pagina no crece con la conversacion. */
const Chat = forwardRef(function Chat({ mensajes, cargando, onEnviar, onNuevaConversacion }, ref) {
  const [input, setInput] = useState('')
  const listaRef = useRef(null)

  useEffect(() => {
    const lista = listaRef.current
    if (lista) lista.scrollTo({ top: lista.scrollHeight, behavior: 'smooth' })
  }, [mensajes, cargando])

  function enviar() {
    if (!input.trim() || cargando) return
    onEnviar(input)
    setInput('')
  }

  function alPresionarTecla(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      enviar()
    }
  }

  return (
    <section id="agente" ref={ref} className="relative z-10 scroll-mt-24 px-4 pb-20 pt-8 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-5xl">
        <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.4em] text-hielo">Agente</p>
            <h2 className="mt-3 font-titulo text-4xl font-semibold text-crema">Consultá a Ragnar</h2>
          </div>
          <button
            type="button"
            onClick={onNuevaConversacion}
            disabled={cargando || mensajes.length === 0}
            className="rounded-full border border-cuero px-5 py-2 text-xs font-medium uppercase tracking-[0.2em] text-ambar transition-colors hover:bg-cuero/20 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Nueva conversación
          </button>
        </div>

        {/* Alto: pantalla menos navbar y titulo, para que el input quede siempre a la vista */}
        <div className="flex h-[calc(100svh-15rem)] min-h-[26rem] max-h-[820px] flex-col overflow-hidden rounded-3xl border border-petroleo/60 bg-noche/85 shadow-2xl shadow-black/40 backdrop-blur">
          <div ref={listaRef} className="scroll-fino flex-1 space-y-6 overflow-y-auto p-4 sm:p-6">
            {mensajes.length === 0 && !cargando ? (
              <Vacio onEnviar={onEnviar} />
            ) : (
              mensajes.map((mensaje, i) => <Mensaje key={i} mensaje={mensaje} />)
            )}
            {cargando && <Escribiendo />}
          </div>

          <form
            className="flex items-end gap-3 border-t border-petroleo/50 bg-base/60 p-3 sm:p-4"
            onSubmit={(e) => {
              e.preventDefault()
              enviar()
            }}
          >
            <label htmlFor="consulta" className="sr-only">
              Consulta para el agente
            </label>
            <textarea
              id="consulta"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={alPresionarTecla}
              placeholder="Escribí tu consulta… (Enter envía, Shift+Enter nueva línea)"
              rows={1}
              maxLength={1000}
              disabled={cargando}
              className="max-h-40 min-h-12 flex-1 resize-none rounded-2xl border border-petroleo bg-noche px-4 py-3 text-sm text-crema placeholder:text-crema/35 focus:border-niebla focus:outline-none disabled:opacity-60 field-sizing-content"
            />
            <button
              type="submit"
              disabled={cargando || !input.trim()}
              aria-label="Enviar consulta"
              className="flex size-12 shrink-0 items-center justify-center rounded-full bg-cuero text-crema transition-colors hover:bg-ambar hover:text-base disabled:cursor-not-allowed disabled:opacity-40"
            >
              <svg viewBox="0 0 24 24" className="size-5" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
                <path d="M4 12h15m-5-5 5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </section>
  )
})

export default Chat
