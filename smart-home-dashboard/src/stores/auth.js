import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedIn: false,
    gatewayName: null,
    gatewayId: null
  }),
  actions: {
    login(name, id) {
      this.loggedIn = true
      this.gatewayName = name
      this.gatewayId = id
      localStorage.setItem('gatewayName', name)
      localStorage.setItem('loggedIn', 'true')
      localStorage.setItem('gatewayId', id)
    },
    logout() {
      this.loggedIn = false
      this.gatewayName = null
      this.gatewayId = null
      localStorage.removeItem('gatewayName')
      localStorage.removeItem('loggedIn')
      localStorage.removeItem('gatewayId')
    },
    initialize() {
      this.loggedIn = localStorage.getItem('loggedIn') === 'true'
      this.gatewayName = localStorage.getItem('gatewayName') || null
      this.gatewayId = localStorage.getItem('gatewayId') || null
    }
  }
})
