import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { useAuthStore } from './stores/auth'
import './assets/main.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())

const auth = useAuthStore()
auth.initialize()

import {useThemeStore} from '@/stores/themeStore'
const themeStore = useThemeStore()
themeStore.initTheme()

app.use(router)
app.mount('#app')
