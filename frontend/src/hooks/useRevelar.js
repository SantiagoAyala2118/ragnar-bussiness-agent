import { useEffect, useRef, useState } from 'react'

/**
 * Indica si un elemento ya entro en pantalla (una sola vez).
 * Se usa con la clase CSS `revelar` para animar su aparicion.
 */
export function useRevelar(umbral = 0.2) {
  const ref = useRef(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const elemento = ref.current
    if (!elemento) return undefined
    const observador = new IntersectionObserver(
      ([entrada]) => {
        if (entrada.isIntersecting) {
          setVisible(true)
          observador.disconnect()
        }
      },
      { threshold: umbral },
    )
    observador.observe(elemento)
    return () => observador.disconnect()
  }, [umbral])

  return [ref, visible]
}
