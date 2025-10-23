<script setup>
import { onMounted, computed, ref, watch, onUnmounted } from 'vue'
import { useDeviceStore } from '@/stores/deviceStore'
import GenericDeviceWidget from '@/components/devices/GenericDeviceWidget.vue'
import DashboardNavbar from '@/components/DashboardNavbar.vue'
import { deviceWidgetMap } from '@/utils/deviceWidgetMap'
import socket from '@/services/websocket'
import { useRoomStore } from '@/stores/roomStore'

const selectedRoomId = ref(null)
const deviceStore = useDeviceStore();
const { fetchDevices } = useDeviceStore();
const roomStore = useRoomStore()

const noRooms = computed (() => roomStore.rooms.length === 0)

const socketHandlers = {
  device_status: null,
  motion_detected: null,
  weather_station_measurements: null,
  test_pong: null
}

const handleSocketUpdate = (data) => {
  console.log('[INFO] Received device_status:', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) device.available = data.available
}

const handleMotionDetectedUpdate = (data) => {
  console.log('[INFO] Redceived motion_detected:', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if(device.type.toLowerCase() === 'alarmsensor' || Object.prototype.hasOwnProperty.call(device.properties, 'motion_detected')) {
      device.properties.motion_detected = data.motion_detected
    }
  }
}

const handleWeatherStationMeasurementsUpdate = (data) => {
  console.log('[INFO] Received weather station measurements:', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if (device.type.toLowerCase() === 'weatherstation' || (Object.prototype.hasOwnProperty.call(device.properties, 'temperature') 
      && Object.prototype.hasOwnProperty.call(device.properties, 'humidity'))) {
        device.properties.temperature = data.temperature
        device.properties.humidity = data.humidity
        device.properties.city = data.city
        device.properties.api_temperature = data.api_temperature
        device.properties.api_weather_description = data.api_weather_description
        device.properties.api_feels_like = data.api_feels_like
        device.properties.api_pressure = data.api_pressure
        device.properties.api_humidity = data.api_humidity
        device.properties.last_measurement = data.last_measurement
    }
  }
}

onMounted(() => {
  fetchDevices();
  
  socketHandlers.device_status = handleSocketUpdate
  socketHandlers.motion_detected = handleMotionDetectedUpdate
  socketHandlers.weather_station_measurements = handleWeatherStationMeasurementsUpdate

  socket.on('device_status', socketHandlers.device_status)
  socket.on('motion_detected', socketHandlers.motion_detected)
  socket.on('weather_station_measurements', socketHandlers.weather_station_measurements)

  socket.on('connect_error', (err) => {
    console.error("[ERROR] Connection error:", err)
  })
});

onUnmounted(() => {
  if (socketHandlers.device_status) socket.off('device_status', socketHandlers.device_status)
  if (socketHandlers.motion_detected) socket.off('motion_detected', socketHandlers.motion_detected)
  if (socketHandlers.weather_station_measurements) socket.off('weather_station_measurements', socketHandlers.weather_station_measurements)

  console.log('[INFO] Cleaned up all socket listeners')
});

const handleRoomSelected = (roomId) => {
  selectedRoomId.value = roomId;
};
 
const devicesInSelectedRoom = computed(() => {
  return deviceStore.devices.filter(d => d.roomId === selectedRoomId.value)
});

watch(selectedRoomId, (newValue, oldValue) => {
  console.log('[INFO] selected room ID:', newValue);
})

watch(selectedRoomId, () => {
  if (deviceStore.devices.length > 0) {
    console.log('[INFO] Devices In selected room: ',devicesInSelectedRoom.value);
  } else {
    console.log('[INFO] Devices not yet fetched');
  }
});


</script>

<template>
  <div class="max-w-7xl mx-auto">
    <!-- Dynamic Navbar -->
    <DashboardNavbar :selectedRoom="selectedRoomId" @room-selected="handleRoomSelected($event)"/>
  
    <!-- Device Widgets -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 items-start">
      <component
        v-for="device in devicesInSelectedRoom"
        :key="device.id"
        :is="(deviceWidgetMap[device.type.toLowerCase()] || GenericDeviceWidget)"
        :device="device"
      />
    </div>
    
    <!-- Empty state when no devices -->
    <div v-if="devicesInSelectedRoom.length === 0 && selectedRoomId" class="text-center py-12">
      <div class="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-10 h-10 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-foreground mb-2">No devices found</h3>
      <p class="text-muted-foreground">This room doesn't have any devices yet.</p>
    </div>
 
    <!-- Empty state when no rooms exist -->
    <div v-if="noRooms" class="text-center py-20">
      <div class="w-20 h-20 bg-muted rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-10 h-10 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-foreground mb-2">No rooms found</h3>
      <p class="text-muted-foreground mb-6">
        You haven't created any rooms yet. Add a room to start managing your smart devices.
      </p>
      <RouterLink
        to="/rooms"
        class="bg-primary text-primary-foreground px-6 py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors inline-flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
        </svg>
        Add Room
      </RouterLink>
    </div>
 
  </div>
</template>