import { defineStore } from 'pinia'
import { ref, onMounted } from 'vue'
import axios from 'axios'

export const useRoomStore = defineStore('room', () => {
  const rooms = ref([])
  const isLoading = ref(false)

  const fetchRooms = async () => {
    try {
        isLoading.value = true
        const res = await axios.get('http://localhost:8000/api/rooms')
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
  
  const addRoom = async (roomData) => {
    const response = await axios.post('http://localhost:8000/api/rooms/add', roomData)
    rooms.value.push(response.data)
  }

  const removeRoom = async (roomId) => {
    const response = await axios.delete(`http://localhost:8000/api/rooms/remove/${roomId}`)
    rooms.value = rooms.value.filter(room => room.id !== roomId)
  }

  return {
    rooms,
    isLoading,
    fetchRooms,
    addRoom,
    removeRoom
  }
})
