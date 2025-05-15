<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoomStore } from '@/stores/roomStore'
import axios from 'axios'

const name = ref('')
const description = ref('')
const roomId = ref('')
const isPairing = ref(false)
const statusMessage = ref('')
const progress = ref(0)

const roomStore = useRoomStore()
roomStore.fetchRooms()
const rooms = roomStore.rooms

const pairingDuration = 60 // seconds

let timerInterval = null

const startPairing = async () => {
  if (!name.value || !roomId.value) return

  isPairing.value = true
  statusMessage.value = ''
  progress.value = 0

  // Simulate progress
  let secondsElapsed = 0
  timerInterval = setInterval(() => {
    secondsElapsed++
    progress.value = Math.min((secondsElapsed / pairingDuration) * 100, 100)
    if (secondsElapsed >= pairingDuration) clearInterval(timerInterval)
  }, 1000)

  try {
    const gatewayId = localStorage.getItem('gatewayId')

    const res = await axios.post('http://localhost:8000/api/start-pairing', {
      name: name.value,
      room_id: roomId.value,
      description: description.value,
      type: 'generic'
    }, {
      headers: { 'X-Gateway-ID': gatewayId }
    })

    statusMessage.value = res.data.message || 'Device successfully paired!'
  } catch (error) {
    if (error.response?.status === 408) {
      statusMessage.value = 'Pairing timed out. Please try again.'
    } else {
      statusMessage.value = 'Error pairing device.'
    }
  } finally {
    clearInterval(timerInterval)
    isPairing.value = false
    progress.value = 100
  }
}
</script>

<template>
  <div class="p-6 max-w-xl mx-auto bg-white shadow rounded-lg text-center">
    <h2 class="text-xl font-semibold mb-6">Pair New Device</h2>

    <div v-if="!isPairing && !statusMessage">
      <form @submit.prevent="startPairing">
        <div class="mb-4 text-left">
          <label class="block mb-1">Device Name</label>
          <input v-model="name" type="text" class="w-full border rounded px-3 py-2" required />
        </div>

        <div class="mb-4 text-left">
          <label class="block mb-1">Description (optional)</label>
          <input v-model="description" type="text" class="w-full border rounded px-3 py-2" />
        </div>

        <div class="mb-4 text-left">
          <label class="block mb-1">Select Room</label>
          <select v-model="roomId" class="w-full border rounded px-3 py-2" required>
            <option disabled value="">-- Select a room --</option>
            <option v-for="room in rooms" :key="room.id" :value="room.id">
              {{ room.name }}
            </option>
          </select>
        </div>

        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded w-full">
          Start Pairing
        </button>
      </form>
    </div>

    <div v-else-if="isPairing">
      <svg class="mx-auto my-4" width="120" height="120" viewBox="0 0 120 120">
        <circle
          cx="60"
          cy="60"
          r="54"
          stroke="#e5e7eb"
          stroke-width="12"
          fill="none"
        />
        <circle
          cx="60"
          cy="60"
          r="54"
          :stroke-dasharray="339.292"
          :stroke-dashoffset="339.292 - (progress / 100) * 339.292"
          stroke="#3b82f6"
          stroke-width="12"
          fill="none"
          stroke-linecap="round"
          transform="rotate(-90 60 60)"
        />
        <text x="50%" y="50%" text-anchor="middle" dy=".3em" class="text-lg font-semibold fill-gray-700">
          {{ Math.round(progress) }}%
        </text>
      </svg>
      <p class="mt-4 text-gray-600">Waiting for device to connect...</p>
    </div>

    <div v-if="statusMessage" class="mt-6 text-lg text-gray-800">
      {{ statusMessage }}
    </div>
  </div>
</template>
