<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const name = ref('')
const password = ref('')
const error = ref('')
const success = ref(false)

const router = useRouter()

const register = async () => {
  error.value = ''
  success.value = false

  if (!name.value || !password.value) {
    error.value = 'Name and password are required.'
    return
  }

  try {
    const response = await axios.post('http://localhost:8000/api/register', {
      name: name.value,
      password: password.value
    })

    if (response.status === 201) {
      success.value = true
      setTimeout(() => {
        router.push('/login')
      }, 1500)
    }
  } catch (err) {
    if (err.response && err.response.status === 409) {
      error.value = 'Gateway name already exists.'
    } else {
      error.value = 'Registration failed. Please try again.'
    }
  }
}
</script>

<template>
  <div class="max-w-md mx-auto mt-10 bg-white p-6 rounded shadow-md">
    <h2 class="text-2xl font-bold mb-4 text-center">Register Gateway</h2>

    <div v-if="error" class="text-red-600 mb-2">{{ error }}</div>
    <div v-if="success" class="text-green-600 mb-2">Registration successful! Redirecting to login...</div>

    <form @submit.prevent="register" class="space-y-4">
      
        <label class="block text-sm font-medium text-gray-700">Gateway Name</label>
        <input
            v-model="name"
            type="text"
            class="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            required
        />

        
        <label class="block text-sm font-medium text-gray-700">Password</label>
        <input
            v-model="password"
            type="password"
            class="mt-1 block w-full border border-gray-300 rounded px-3 py-2"
            required
        />

        <button
            type="submit"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
            Register
        </button>
    </form>
  </div>
</template>

<style scoped>
</style>
