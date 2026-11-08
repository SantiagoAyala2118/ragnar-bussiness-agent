import imagenTienda from '../assets/ragnar_store_background_image.jpg'
import { useProgresoScroll } from '../hooks/useProgresoScroll'

/**
 * Fondo fijo de la pagina: la imagen de la tienda sube con parallax
 * y se funde con el color base a medida que se hace scroll.
 */
export default function Fondo() {
  const progreso = useProgresoScroll(1.3)
  const opacidad = Math.max(0, 1 - progreso * 1.25)

  return (
    <div className="pointer-events-none fixed inset-0 z-0 overflow-hidden bg-base" aria-hidden="true">
      {/* Brillos suaves que quedan cuando la imagen desaparece */}
      <div className="absolute -left-40 top-1/3 size-[36rem] rounded-full bg-petroleo/25 blur-[120px]" />
      <div className="absolute -right-32 bottom-0 size-[30rem] rounded-full bg-cuero/20 blur-[120px]" />

      <div
        className="absolute inset-y-0 right-0 w-full will-change-transform md:w-[70%]"
        style={{
          opacity: opacidad,
          transform: `translateY(${-progreso * 14}vh) scale(${1 + progreso * 0.06})`,
        }}
      >
        <img
          src={imagenTienda}
          alt=""
          className="size-full object-cover object-[72%_center]"
          fetchPriority="high"
        />
        {/* Degrade hacia el texto (izquierda) y hacia abajo */}
        <div className="absolute inset-0 bg-gradient-to-r from-base via-base/55 to-transparent md:via-base/30" />
        <div className="absolute inset-0 bg-gradient-to-t from-base via-transparent to-base/40" />
        <div className="absolute inset-0 bg-base/45 md:hidden" />
      </div>
    </div>
  )
}
