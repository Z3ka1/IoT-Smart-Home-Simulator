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
  <div class="p-6 max-w-xl mx-auto bg-card border border-border shadow-lg rounded-xl text-center">
    <h2 class="text-2xl font-bold mb-6 text-foreground">Pair New Device</h2>

    <div v-if="!isPairing && !statusMessage">
      <form @submit.prevent="startPairing">
        <div class="mb-4 text-left">
          <label class="block mb-2 text-sm font-medium text-muted-foreground">Device Name</label>
          <input 
            v-model="name" 
            type="text" 
            class="w-full bg-background border border-border rounded-lg px-4 py-3 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200" 
            placeholder="Enter device name"
            required 
          />
        </div>

        <div class="mb-4 text-left">
          <label class="block mb-2 text-sm font-medium text-muted-foreground">Description (optional)</label>
          <input 
            v-model="description" 
            type="text" 
            class="w-full bg-background border border-border rounded-lg px-4 py-3 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200" 
            placeholder="Enter device description"
          />
        </div>

        <div class="mb-6 text-left">
          <label class="block mb-2 text-sm font-medium text-muted-foreground">Select Room</label>
          <select 
            v-model="roomId" 
            class="w-full bg-background border border-border rounded-lg px-4 py-3 text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all duration-200" 
            required
          >
            <option disabled value="" class="text-muted-foreground">-- Select a room --</option>
            <option v-for="room in rooms" :key="room.id" :value="room.id" class="text-foreground">
              {{ room.name }}
            </option>
          </select>
        </div>

        <button 
          type="submit" 
          class="bg-primary hover:bg-primary/90 text-primary-foreground px-6 py-3 rounded-lg w-full font-medium transition-all duration-200 hover:shadow-lg"
        >
          Start Pairing
        </button>
      </form>
    </div>

    <div v-else-if="isPairing">
      <svg class="mx-auto my-6" width="120" height="120" viewBox="0 0 120 120">
        <circle
          cx="60"
          cy="60"
          r="54"
          stroke="hsl(var(--border))"
          stroke-width="12"
          fill="none"
        />
        <circle
          cx="60"
          cy="60"
          r="54"
          :stroke-dasharray="339.292"
          :stroke-dashoffset="339.292 - (progress / 100) * 339.292"
          stroke="hsl(var(--primary))"
          stroke-width="12"
          fill="none"
          stroke-linecap="round"
          transform="rotate(-90 60 60)"
        />
        <text x="50%" y="50%" text-anchor="middle" dy=".3em" class="text-lg font-semibold fill-foreground">
          {{ Math.round(progress) }}%
        </text>
      </svg>
      <p class="mt-4 text-muted-foreground">Waiting for device to connect...</p>
    </div>

    <div v-if="statusMessage" class="mt-6 p-4 bg-background border border-border rounded-lg">
      <p class="text-lg text-foreground">{{ statusMessage }}</p>
    </div>
  </div>
</template>
