import { defineStore } from 'pinia'
import { ref, onMounted } from 'vue'
import axios from 'axios'

export const useRoomStore = defineStore('room', () => {
  const rooms = ref([])
  const isLoading = ref(false)

  const fetchRooms = async () => {
    try {
        isLoading.value = true
        const gatewayId = localStorage.getItem('gatewayId')

        const res = await axios.get('http://localhost:8000/api/rooms', {
          headers: {'X-Gateway-ID': gatewayId}
        })

        rooms.value = res.data
    } catch (error) {
        console.error('Failed to fetch rooms: ', error)
    } finally {
        isLoading.value = false
    }
  }
  
  onMounted(() => {
      fetchRooms();  
  });

  const resetRooms = () => {
    rooms.value = []
  }
  
  const addRoom = async (roomData) => {
    rooms.value.push(roomData)
  }

  const removeRoom = async (roomId) => {
    rooms.value = rooms.value.filter(room => room.id !== roomId)
  }

  return {
    rooms,
    isLoading,
    fetchRooms,
    addRoom,
    removeRoom,
    resetRooms
  }
})
