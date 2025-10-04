<script setup>
import { onMounted, computed, ref, watch, onUnmounted } from 'vue'
import { useDeviceStore } from '@/stores/deviceStore'
import GenericDeviceWidget from '@/components/devices/GenericDeviceWidget.vue'
import DashboardNavbar from '@/components/DashboardNavbar.vue'
import { deviceWidgetMap } from '@/utils/deviceWidgetMap'
import socket from '@/services/websocket'

const selectedRoomId = ref(null)
const deviceStore = useDeviceStore();
const { fetchDevices } = useDeviceStore();

const socketHandlers = {
  device_status: null,
  motion_detected: null,
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

onMounted(() => {
  fetchDevices();
  
  socketHandlers.device_status = handleSocketUpdate
  socketHandlers.motion_detected = handleMotionDetectedUpdate

  socket.on('device_status', socketHandlers.device_status)
  socket.on('motion_detected', socketHandlers.motion_detected)

  socket.on('connect_error', (err) => {
    console.error("[ERROR] Connection error:", err)
  })
});

onUnmounted(() => {
  if (socketHandlers.device_status) socket.off('device_status', socketHandlers.device_status)
  if (socketHandlers.motion_detected) socket.off('motion_detected', socketHandlers.motion_detected)

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
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
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
        <svg class="w-8 h-8 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.467.881-6.127 2.325.895-.449 1.933-.725 3.127-.725 1.194 0 2.232.276 3.127.725z"/>
        </svg>
      </div>
      <h3 class="text-lg font-medium text-foreground mb-2">No devices found</h3>
      <p class="text-muted-foreground">This room doesn't have any devices yet.</p>
    </div>
  </div>
</template>