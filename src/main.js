import { createSSRApp } from 'vue'
import App from './App.vue'
import { initializeStore } from '@/store/app'

export function createApp() {
  initializeStore()
  const app = createSSRApp(App)
  return { app }
}
