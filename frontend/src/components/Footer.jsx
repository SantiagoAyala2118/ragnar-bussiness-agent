import logo from '../assets/ragnar_logo_light.png'
import { EQUIPO, FRASE_RAGNAR } from '../data/contenido'
import { EscudoRed } from './IconosRedes'

/** Pie: logo, frase de Ragnar y redes de cada integrante. */
export default function Footer() {
  return (
    <footer id="equipo" className="relative z-10 border-t border-petroleo/40 bg-base px-6 pb-10 pt-20 lg:px-10">
      <div className="mx-auto grid max-w-7xl gap-16 lg:grid-cols-[1fr_1.4fr]">
        <div className="flex flex-col items-center gap-8 text-center sm:flex-row sm:text-left">
          <img src={logo} alt="Ragnar Provisiones" className="h-36 w-auto" />
          <blockquote>
            <p className="font-titulo text-xl leading-snug text-ambar italic">“{FRASE_RAGNAR}”</p>
            <footer className="mt-3 text-xs uppercase tracking-[0.3em] text-crema/50">Ragnar Lothbrok</footer>
          </blockquote>
        </div>

        <div className="grid gap-10 sm:grid-cols-3">
          {EQUIPO.map(({ nombre, redes }) => (
            <div key={nombre} className="flex flex-col items-center gap-4 sm:items-start">
              <h3 className="font-titulo text-base font-semibold tracking-wider text-crema">{nombre}</h3>
              <div className="flex gap-3">
                {Object.entries(redes).map(([red, url]) => (
                  <EscudoRed key={red} red={red} url={url} persona={nombre} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <p className="mx-auto mt-16 max-w-7xl border-t border-petroleo/30 pt-6 text-center text-xs text-crema/40">
        Ragnar Provisiones · Taller Complementario de IA · 2026
      </p>
    </footer>
  )
}
