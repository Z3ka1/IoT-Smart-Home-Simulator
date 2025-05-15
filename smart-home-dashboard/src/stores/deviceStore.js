import { defineStore } from 'pinia'
import { ref, onMounted } from 'vue'
import axios from 'axios'

export const useDeviceStore = defineStore('device', () => {
  const devices = ref([])
  const isLoading = ref(false)

  const fetchDevices = async () => {
    try {
        isLoading.value = true
        const gatewayId = localStorage.getItem('gatewayId')

        const res = await axios.get('http://localhost:8000/api/devices', {
          headers: {'X-Gateway-ID': gatewayId}
        })
        devices.value = res.data
        console.log('Devices fetched:', devices.value)
    } catch (error) {
        console.error('Failed to fetch devices: ', error)
    } finally {
        isLoading.value = false
    }
  };

  onMounted(() => {
    fetchDevices();  
  }); 

  const getDevicesByRoomId = (roomId) => {
    return computed(() => devices.value.filter(device => device.roomId === roomId));
  }


  return {
    devices,
    isLoading,
    fetchDevices,
    getDevicesByRoomId
  }
})
