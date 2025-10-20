import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    loggedIn: false,
    gatewayName: null,
    gatewayId: null,
    accessToken: null,
    refreshToken: null
  }),
  actions: {
    login(name, id, accessToken, refreshToken) {
      this.loggedIn = true
      this.gatewayName = name
      this.gatewayId = id
      this.accessToken = accessToken
      this.refreshToken = refreshToken
      localStorage.setItem('gatewayName', name)
      localStorage.setItem('loggedIn', 'true')
      localStorage.setItem('gatewayId', id)
      localStorage.setItem('accessToken', accessToken)
      localStorage.setItem('refreshToken', refreshToken)
    },
    logout() {
      this.loggedIn = false
      this.gatewayName = null
      this.gatewayId = null
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('gatewayName')
      localStorage.removeItem('loggedIn')
      localStorage.removeItem('gatewayId')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    },
    initialize() {
      this.loggedIn = localStorage.getItem('loggedIn') === 'true'
      this.gatewayName = localStorage.getItem('gatewayName') || null
      this.gatewayId = localStorage.getItem('gatewayId') || null
      this.accessToken = localStorage.getItem('accessToken') || null
      this.refreshToken = localStorage.getItem('refreshToken') || null
    },
    updateAccessToken(newToken) {
      this.accessToken = newToken
      localStorage.setItem("accessToken", newToken)
    }
  }
})
