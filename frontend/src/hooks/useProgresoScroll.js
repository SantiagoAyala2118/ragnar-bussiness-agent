import { useEffect, useState } from 'react'

/**
 * Devuelve cuanto se avanzo con el scroll, de 0 a 1.
 * 1 se alcanza al recorrer `pantallas` alturas de ventana.
 */
export function useProgresoScroll(pantallas = 1) {
  const [progreso, setProgreso] = useState(0)

  useEffect(() => {
    let frame = null
    function medir() {
      frame = null
      const recorrido = window.innerHeight * pantallas
      setProgreso(Math.min(1, Math.max(0, window.scrollY / recorrido)))
    }
    function alHacerScroll() {
      if (frame === null) frame = requestAnimationFrame(medir)
    }
    medir()
    window.addEventListener('scroll', alHacerScroll, { passive: true })
    window.addEventListener('resize', alHacerScroll)
    return () => {
      window.removeEventListener('scroll', alHacerScroll)
      window.removeEventListener('resize', alHacerScroll)
      if (frame !== null) cancelAnimationFrame(frame)
    }
  }, [pantallas])

  return progreso
}
