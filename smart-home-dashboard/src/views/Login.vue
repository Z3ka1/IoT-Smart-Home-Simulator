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
      auth.login(name.value)
      router.push('/')
    }
  } catch (err) {
    error.value = 'Invalid name or password'
  }
}
</script>

<template>
  <div class="max-w-md mx-auto mt-10 bg-white p-6 rounded shadow-md">
    <h2 class="text-2xl font-bold mb-4 text-center">Gateway Login</h2>
    
    <form @submit.prevent="handleLogin" class="space-y-4">
      <label class="block text-sm font-medium text-gray-700">Gateway Name</label>
      <input v-model="name" type="text" class="mt-1 block w-full border border-gray-300 rounded px-3 py-2" required />

      <label class="block text-sm font-medium text-gray-700">Password</label>
      <input v-model="password" type="password" class="mt-1 block w-full border border-gray-300 rounded px-3 py-2" required />

      <button type="submit" class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">Login</button>
    </form>

    <p v-if="error" class="text-red-500 mt-4">{{ error }}</p>
  </div>
</template>

<style scoped>
</style>
