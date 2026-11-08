import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Ports: frontend 3000, backend 8080 (adk web keeps 8000 free)
// The proxy forwards /api to the FastAPI backend
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: true,
    proxy: {
      '/api': 'http://localhost:8080',
    },
  },
})
