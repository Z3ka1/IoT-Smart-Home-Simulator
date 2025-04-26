<script setup>
import { onMounted, computed, ref, watch } from 'vue'
import { useDeviceStore } from '@/stores/deviceStore'
import GenericDeviceWidget from '@/components/devices/GenericDeviceWidget.vue'
import DashboardNavbar from '@/components/DashboardNavbar.vue'
import { deviceWidgetMap } from '@/utils/deviceWidgetMap'

const selectedRoomId = ref(null)
const deviceStore = useDeviceStore();


const handleRoomSelected = (roomId) => {
  selectedRoomId.value = roomId;
};

const devicesInSelectedRoom = computed(() => {
  return deviceStore.devices.filter(d => d.roomId === selectedRoomId.value)
});

watch(selectedRoomId, (newValue, oldValue) => {
  console.log('selected room ID:', newValue);
})

watch(selectedRoomId, () => {
  if (deviceStore.devices.length > 0) {
    console.log('Devices In selected room: ',devicesInSelectedRoom.value);
  } else {
    console.log('Devices not yet fetched');
  }
});


</script>

<template>
    <div class="dashboard-view">
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