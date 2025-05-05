import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedIn: false,
    gatewayName: null
  }),
  actions: {
    login(name) {
      this.loggedIn = true
      this.gatewayName = name
      localStorage.setItem('gatewayName', name)
      localStorage.setItem('loggedIn', 'true')
    },
    logout() {
      this.loggedIn = false
      this.gatewayName = null
      localStorage.removeItem('gatewayName')
      localStorage.removeItem('loggedIn')
    },
    initialize() {
      this.loggedIn = localStorage.getItem('loggedIn') === 'true'
      this.gatewayName = localStorage.getItem('gatewayName') || null
    }
  }
})
