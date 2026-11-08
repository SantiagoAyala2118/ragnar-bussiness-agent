import { useRef, useState } from 'react'
import { borrarSesion, enviarMensaje } from './api'
import Chat from './components/Chat'
import Fondo from './components/Fondo'
import Footer from './components/Footer'
import Funciones from './components/Funciones'
import Hero from './components/Hero'
import Navbar from './components/Navbar'

export default function App() {
  const [mensajes, setMensajes] = useState([])
  const [cargando, setCargando] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const chatRef = useRef(null)

  async function enviar(texto) {
    const message = texto.trim()
    if (!message || cargando) return
    setMensajes((m) => [...m, { role: 'user', text: message }])
    setCargando(true)
    try {
      const data = await enviarMensaje(message, sessionId)
      setSessionId(data.session_id)
      setMensajes((m) => [...m, { role: 'agent', text: data.reply, toolCalls: data.tool_calls }])
    } catch (err) {
      setMensajes((m) => [...m, { role: 'agent', text: `⚠️ ${err.message}`, error: true }])
    } finally {
      setCargando(false)
    }
  }

  // Atajos de las tarjetas: bajan hasta el chat y envian la consulta
  function usarAtajo(texto) {
    chatRef.current?.scrollIntoView({ behavior: 'smooth' })
    enviar(texto)
  }

  function nuevaConversacion() {
    if (sessionId) borrarSesion(sessionId)
    setSessionId(null)
    setMensajes([])
  }

  return (
    <>
      <Fondo />
      <Navbar />
      <main>
        <Hero />
        <Funciones onAtajo={usarAtajo} />
        <Chat
          ref={chatRef}
          mensajes={mensajes}
          cargando={cargando}
          onEnviar={enviar}
          onNuevaConversacion={nuevaConversacion}
        />
      </main>
      <Footer />
    </>
  )
}
