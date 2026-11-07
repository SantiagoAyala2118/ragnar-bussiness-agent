export async function enviarMensaje(message, sessionId) {
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  })
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    const detalle = typeof data.detail === 'string' ? data.detail : null
    throw new Error(detalle || `Error ${res.status} al contactar al agente`)
  }
  return res.json()
}

export async function borrarSesion(sessionId) {
  await fetch(`/api/sessions/${sessionId}`, { method: 'DELETE' }).catch(() => {})
}
