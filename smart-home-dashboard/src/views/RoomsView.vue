<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoomStore } from '@/stores/roomStore'
import { useAuthStore } from '@/stores/auth'
import PopupWindow from '@/components/PopupWindow.vue'
import axios from 'axios'

const roomStore = useRoomStore()
const authStore = useAuthStore()
let popupIsActive = ref(false)

console.log(roomStore.rooms)

const newRoomName = ref('')

const addNewRoom = async () => {
    if (!newRoomName.value.trim()) return

    try {
      const response = await axios.post('http://localhost:8000/api/rooms', {
      name: newRoomName.value,
      gatewayId: authStore.gatewayId
      })
      if (response.status === 201) {
        roomStore.addRoom( {id: response.data.id, gateway_id: response.data.gateway_id, name: newRoomName.value} )
        newRoomName.value = ''
        popupIsActive.value = false
      }
    } catch (error) {
        console.error('Error adding room:', error);
        alert('Error adding room')
    }
}

const removeRoom = async (roomId) => {
  console.log(roomId)
  try {
    const response = await axios.delete(`http://localhost:8000/api/rooms/remove/${roomId}`)
    if (response.status === 200) {
      roomStore.removeRoom(roomId)
    }
  }
  catch (error) {
    console.error('Error removing room: ', error);
    alert('Error removing room')
  }
}


</script>

<template>
  <div class="max-w-7xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-foreground">Rooms</h1>
        <p class="text-muted-foreground mt-2">Manage your smart home rooms</p>
      </div>
      <button
        class="bg-primary text-primary-foreground px-6 py-3 rounded-lg font-medium hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 focus:ring-offset-background transition-colors flex items-center gap-2"
        @click="popupIsActive=true"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
        </svg>
        Add Room
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="room in roomStore.rooms" :key="room.id" class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-all duration-200 group relative">
        <button
          class="absolute top-4 right-4 w-8 h-8 bg-destructive/10 hover:bg-destructive/20 text-destructive rounded-lg flex items-center justify-center transition-colors opacity-0 group-hover:opacity-100"
          @click="removeRoom(room.id)"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </button>
        
        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-secondary-foreground" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
            </svg>
          </div>
          <div>
            <h2 class="text-lg font-semibold text-foreground">{{ room.name }}</h2>
            <p class="text-sm text-muted-foreground">Smart room</p>
          </div>
        </div>
        
        <div class="flex items-center justify-between text-sm">
          <span class="text-muted-foreground">Status</span>
          <span class="text-success font-medium">Active</span>
        </div>
      </div>
    </div>

    <PopupWindow @closePopup="popupIsActive = false" v-if="popupIsActive">
      <div class="space-y-6">
        <div>
          <h3 class="text-lg font-semibold text-foreground mb-2">Add New Room</h3>
          <p class="text-muted-foreground text-sm">Create a new room for your smart home devices</p>
        </div>
        
        <div class="space-y-2">
          <label for="roomName" class="block text-sm font-medium text-foreground">Room Name</label>
          <input
            type="text"
            id="roomName"
            v-model="newRoomName"
            placeholder="Enter room name"
            class="w-full bg-background border border-border rounded-lg px-4 py-3 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-colors"
          />
        </div>

        <div class="flex justify-end space-x-3">
          <button
            @click="popupIsActive = false"
            class="px-4 py-2 text-muted-foreground hover:text-foreground transition-colors"
          >
            Cancel
          </button>
          <button
            @click="addNewRoom"
            class="bg-primary text-primary-foreground px-6 py-2 rounded-lg font-medium hover:bg-primary/90 transition-colors"
          >
            Add Room
          </button>
        </div>
      </div>
    </PopupWindow>
  </div>
</template>