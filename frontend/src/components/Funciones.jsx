import { FUNCIONES } from '../data/contenido'
import { useRevelar } from '../hooks/useRevelar'

// Alturas distintas para cada tarjeta, como en una composicion escalonada
const DESFASES = ['md:translate-y-0', 'md:-translate-y-10', 'md:translate-y-6', 'md:-translate-y-4']

function Tarjeta({ funcion, indice, visible, onAtajo }) {
  return (
    <div className={DESFASES[indice]}>
      <article
        className={`revelar group relative flex h-full flex-col overflow-hidden rounded-2xl border border-petroleo/50 bg-noche/75 p-6 backdrop-blur-sm transition-colors hover:border-cuero ${
          visible ? 'visible' : ''
        }`}
        style={{ transitionDelay: `${indice * 150}ms` }}
      >
        <span
          className="pointer-events-none absolute -right-2 -top-6 font-runa text-[9rem] leading-none text-cuero/25 transition-colors group-hover:text-cuero/40"
          aria-hidden="true"
        >
          {funcion.runa}
        </span>
        <span className="text-xs font-medium tracking-[0.3em] text-hielo/70">0{indice + 1}</span>
        <h3 className="mt-16 font-titulo text-xl font-semibold text-crema">{funcion.titulo}</h3>
        <p className="mt-3 flex-1 text-sm leading-relaxed text-crema/70">{funcion.texto}</p>
        <button
          type="button"
          onClick={() => onAtajo(funcion.atajo)}
          className="mt-6 flex items-center gap-2 self-start text-xs font-medium uppercase tracking-[0.25em] text-ambar transition-colors hover:text-crema"
        >
          Probar
          <span aria-hidden="true" className="transition-transform group-hover:translate-x-1">→</span>
        </button>
      </article>
    </div>
  )
}

/** Seccion intermedia: las cuatro tareas del agente, con atajos que le envian una consulta. */
export default function Funciones({ onAtajo }) {
  const [ref, visible] = useRevelar(0.15)

  return (
    <section id="funciones" className="relative z-10 px-6 py-32 lg:px-10">
      <div ref={ref} className="mx-auto max-w-7xl">
        <div className={`revelar mx-auto max-w-2xl text-center ${visible ? 'visible' : ''}`}>
          <p className="text-xs font-medium uppercase tracking-[0.4em] text-hielo">Qué hace Ragnar</p>
          <h2 className="mt-4 font-titulo text-4xl font-semibold text-crema md:text-5xl">Un agente, cuatro tareas</h2>
        </div>

        <div className="mt-24 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {FUNCIONES.map((funcion, indice) => (
            <Tarjeta key={funcion.titulo} funcion={funcion} indice={indice} visible={visible} onAtajo={onAtajo} />
          ))}
        </div>

        <p
          className={`revelar mx-auto mt-20 max-w-2xl text-center text-sm leading-relaxed text-crema/60 ${
            visible ? 'visible' : ''
          }`}
          style={{ transitionDelay: '650ms' }}
        >
          Cada precio que muestra Ragnar sale del catálogo o del sitio del competidor, con su enlace y la fecha de
          consulta. Si no encuentra una coincidencia confiable, lo dice: nunca compara productos distintos ni inventa
          datos.
        </p>
      </div>
    </section>
  )
}
