import { useProgresoScroll } from '../hooks/useProgresoScroll'

function Flecha({ className = '' }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true">
      <path d="M4 12h15m-5-5 5 5-5 5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

/** Portada: que es Ragnar y que hace, a la izquierda del vikingo. */
export default function Hero() {
  const progreso = useProgresoScroll(1)

  return (
    <section id="inicio" className="relative z-10 flex min-h-svh items-center">
      <div
        className="mx-auto w-full max-w-7xl px-6 pt-20 lg:px-10"
        style={{ opacity: Math.max(0, 1 - progreso * 1.4), transform: `translateY(${-progreso * 70}px)` }}
      >
        <div className="max-w-xl">
          <p className="mb-6 flex items-center gap-4 text-xs font-medium uppercase tracking-[0.4em] text-hielo">
            <span className="h-px w-10 bg-hielo/60" />
            Ragnar Provisiones
          </p>

          <h1 className="font-titulo text-5xl leading-[1.05] font-semibold text-crema sm:text-6xl lg:text-7xl">
            Precios que
            <br />
            <span className="text-ambar">conquistan.</span>
          </h1>

          <div className="my-8 h-px w-16 bg-cuero" />

          <p className="max-w-md text-base leading-relaxed text-crema/80">
            Ragnar es el agente de inteligencia de precios de nuestra cadena. Consulta el catálogo, investiga a la
            competencia en sus sitios oficiales y arma informes comparativos con fuentes y fechas verificables.
            Sin inventar un solo número.
          </p>

          <div className="mt-10 flex flex-wrap items-center gap-8">
            <a href="#agente" className="group flex items-center gap-4">
              <span className="flex size-14 items-center justify-center rounded-full border border-crema/40 transition-all duration-300 group-hover:border-ambar group-hover:bg-ambar/10">
                <Flecha className="size-5 text-crema transition-transform duration-300 group-hover:translate-x-1" />
              </span>
              <span className="text-xs font-medium uppercase tracking-[0.3em] text-crema">Consultar al agente</span>
            </a>
            <a
              href="#funciones"
              className="text-xs font-medium uppercase tracking-[0.3em] text-crema/60 underline-offset-8 transition-colors hover:text-crema hover:underline"
            >
              Ver qué hace
            </a>
          </div>
        </div>
      </div>

      {/* Indicador de avance y aviso de scroll (fuera del contenedor con transform) */}
      <div
        className="absolute inset-x-0 bottom-10 mx-auto max-w-7xl px-6 lg:px-10"
        style={{ opacity: Math.max(0, 1 - progreso * 2) }}
      >
        <div className="flex items-end justify-between">
          <div className="flex items-center gap-4 text-xs text-crema/60" aria-hidden="true">
            <span>01</span>
            <span className="relative h-px w-32 bg-crema/20">
              <span className="absolute inset-y-0 left-0 bg-ambar" style={{ width: `${Math.max(12, progreso * 100)}%` }} />
            </span>
            <span>03</span>
          </div>
          <div className="hidden flex-col items-center gap-3 text-[10px] uppercase tracking-[0.4em] text-crema/50 sm:flex">
            Scroll
            <span className="h-10 w-px animate-pulse bg-gradient-to-b from-ambar to-transparent" />
          </div>
        </div>
      </div>
    </section>
  )
}
