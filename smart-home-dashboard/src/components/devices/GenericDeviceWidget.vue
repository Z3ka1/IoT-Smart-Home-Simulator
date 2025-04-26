<script setup>
import { onMounted, computed, ref, watch } from 'vue'
import { useRoomStore } from '@/stores/roomStore'

const roomStore = useRoomStore()

const props = defineProps({
  device: {
    device: Object,
    required: true
  }
})

onMounted(() => {
    console.log('DeviceWidget rendered:', props.device.type)
})

const roomName = computed(() => {
  const room = roomStore.rooms.find(r => r.id === props.device.roomId);
  return room ? room.name : 'Unknown Room';
});

console.log("Room Name:", roomName.value)

</script>

<template>
    <div class="device-widget p-4 rounded-lg shadow-md bg-white">
      <h2 class="text-lg font-semibold text-gray-800">{{ device.type }}</h2>
      <h2 class="text-lg font-semibold text-gray-800">{{ roomName }}</h2>
    </div>
  </template>