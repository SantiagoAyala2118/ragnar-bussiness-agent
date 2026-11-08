# Ragnar - Frontend

Chat en React (Vite) que consume el agente de precios a través del backend FastAPI.

## Requisitos

- Node 20+
- Ollama corriendo con sesión iniciada (`ollama signin`), porque el modelo `gemma4:31b-cloud` es remoto
- Entorno virtual de Python del proyecto (`env/`) con `requirements.txt` instalado

## Cómo levantarlo

Terminal 1, backend (desde la raíz del repo):

```powershell
env\Scripts\activate
uvicorn backend.main:app --reload --port 8080
```

Terminal 2, frontend:

```powershell
cd frontend
npm install
npm run dev
```

Abrir http://localhost:3000. Vite redirige `/api/*` a `http://localhost:8080`.

Puertos: frontend `3000`, backend `8080` y `adk web` `8000`, así pueden correr los tres a la vez.

## API del backend

| Método | Ruta                      | Descripción                                                                       |
| ------ | ------------------------- | --------------------------------------------------------------------------------- |
| GET    | `/api/health`             | Chequeo de estado                                                                 |
| POST   | `/api/chat`               | `{ message, session_id? }` → `{ session_id, reply, tool_calls }`                  |
| DELETE | `/api/sessions/{id}`      | Borra la sesión (historial) en memoria                                            |

Las sesiones se guardan en memoria (`InMemorySessionService`): se pierden al reiniciar el backend.
