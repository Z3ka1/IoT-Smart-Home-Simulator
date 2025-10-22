import { defineStore } from 'pinia'
 
export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: localStorage.getItem('theme') || 'dark'
  }),
  actions: {
    toggleTheme() {
      this.theme = this.theme === 'dark' ? 'light' : 'dark'
      localStorage.setItem('theme', this.theme)
      document.documentElement.classList.toggle('light', this.theme === 'light')
    },
    initTheme() {
      document.documentElement.classList.toggle('light', this.theme === 'light')
    }
  }
})