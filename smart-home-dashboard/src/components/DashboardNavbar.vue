<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoomStore } from '@/stores/roomStore'

const roomStore = useRoomStore()
const selectedRoom = ref(null)
const emit = defineEmits(['room-selected'])

onMounted(() => {
    if (roomStore.rooms.length === 0) {
        roomStore.fetchRooms()
    }
})

const isRoomSelected = computed(() => {
  return (room) => room.id === selectedRoom.value
})

const handleRoomSelected = (roomId) => {
  selectedRoom.value = roomId
  emit('room-selected', roomId)  
}

</script>

<template>
    <nav class="flex gap-4 bg-gray-600 text-white p-4">
      <button
        v-for="room in roomStore.rooms"
        :key="room.id"
        @click="handleRoomSelected(room.id)"
        :class="[
          'px-4 py-2 rounded',
          isRoomSelected(room) ? 'bg-purple-900' : 'bg-gray-900 hover:bg-red-900'
        ]"
      >
        {{ room.name }}
      </button>
    </nav>
</template>