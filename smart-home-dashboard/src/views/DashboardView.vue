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
  test_pong: null
}

const handleSocketUpdate = (data) => {
  console.log('[INFO] Received device_status:', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) device.available = data.available
}

onMounted(() => {
  fetchDevices();
  
  socketHandlers.device_status = handleSocketUpdate

  socket.on('device_status', socketHandlers.device_status)

  socket.on('connect_error', (err) => {
    console.error("[ERROR] Connection error:", err)
  })
});

onUnmounted(() => {
  if (socketHandlers.device_status) socket.off('device_status', socketHandlers.device_status)

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
    <div class="max-w-7xl mx-auto p-4 sm:p-6 md:p-8">
      <!-- Dynamic Navbar -->
      <DashboardNavbar :selectedRoom="selectedRoomId" @room-selected="handleRoomSelected($event)"/>
  
      <!-- Device Widgets -->
      <div class="device-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
        <component
          v-for="device in devicesInSelectedRoom"
          :key="device.id"
          :is="(deviceWidgetMap[device.type.toLowerCase()] || GenericDeviceWidget)"
          :device="device"
        />
      </div>
    </div>
  </template>