import { createSSRApp } from 'vue'
import App from './App.vue'
import { initializeDemoStore } from '@/store/app'

export function createApp() {
  initializeDemoStore()
  const app = createSSRApp(App)
  return { app }
}
