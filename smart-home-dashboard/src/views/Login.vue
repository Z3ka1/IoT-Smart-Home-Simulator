<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const name = ref('')
const password = ref('')
const error = ref(null)

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/login', {
      name: name.value,
      password: password.value
    })

    if (response.status === 200) {
      auth.login(
        response.data.gateway_name,
        response.data.gateway_id,
        response.data.access_token,
        response.data.refresh_token
      )
      router.push('/')
    }
  } catch (err) {
    error.value = 'Invalid name or password'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-card border border-border rounded-xl p-8 shadow-lg">
      <div class="text-center mb-8">
        <div class="w-16 h-16 bg-primary rounded-xl flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-primary-foreground" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-foreground">Gateway Login</h2>
        <p class="text-muted-foreground mt-2">Access your smart home dashboard</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div class="space-y-2">
          <label class="block text-sm font-medium text-foreground">Gateway Name</label>
          <input 
            v-model="name" 
            type="text" 
            class="w-full bg-background border border-border rounded-lg px-4 py-3 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-colors" 
            placeholder="Enter gateway name"
            required 
          />
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-foreground">Password</label>
          <input 
            v-model="password" 
            type="password" 
            class="w-full bg-background border border-border rounded-lg px-4 py-3 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-colors" 
            placeholder="Enter password"
            required 
          />
        </div>

        <button 
          type="submit" 
          class="w-full bg-primary text-primary-foreground py-3 px-4 rounded-lg font-medium hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background transition-colors"
        >
          Sign In
        </button>
      </form>

      <div v-if="error" class="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
        <p class="text-destructive text-sm">{{ error }}</p>
      </div>

      <div class="mt-6 text-center">
        <p class="text-muted-foreground text-sm">
          Don't have a gateway? 
          <router-link to="/register" class="text-primary hover:text-primary/80 font-medium">Register here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
