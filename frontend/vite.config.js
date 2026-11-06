import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// El proxy reenvia /api al backend FastAPI (uvicorn en el puerto 8000)
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
