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

  return {
    rooms,
    isLoading,
    fetchRooms
  }
})
