import logo from '../assets/ragnar_logo_light.png'
import { NAVEGACION } from '../data/contenido'
import { useProgresoScroll } from '../hooks/useProgresoScroll'

/** Barra superior: anclas a cada seccion y el logo, que aparece al dejar la portada. */
export default function Navbar() {
  const progreso = useProgresoScroll(1)
  const opacidadLogo = Math.min(1, Math.max(0, (progreso - 0.35) / 0.45))
  const conFondo = progreso > 0.6

  return (
    <header
      className={`fixed inset-x-0 top-0 z-30 transition-colors duration-500 ${
        conFondo ? 'border-b border-petroleo/30 bg-base/80 backdrop-blur-md' : 'bg-transparent'
      }`}
    >
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between gap-6 px-6 lg:px-10">
        <a href="#inicio" className="font-titulo text-lg font-semibold tracking-[0.35em] text-crema">
          RAGNAR
        </a>

        <div className="flex items-center gap-8">
          <nav aria-label="Secciones" className="hidden items-center gap-8 md:flex">
            {NAVEGACION.map(({ id, texto }) => (
              <a
                key={id}
                href={`#${id}`}
                className="group relative text-xs font-medium uppercase tracking-[0.25em] text-crema/75 transition-colors hover:text-crema"
              >
                {texto}
                <span className="absolute -bottom-2 left-1/2 size-1 -translate-x-1/2 rounded-full bg-ambar opacity-0 transition-opacity group-hover:opacity-100" />
              </a>
            ))}
          </nav>
          <img
            src={logo}
            alt="Ragnar Provisiones"
            className="h-14 w-auto transition-transform duration-300"
            style={{ opacity: opacidadLogo, transform: `scale(${0.85 + opacidadLogo * 0.15})` }}
          />
        </div>
      </div>
    </header>
  )
}
