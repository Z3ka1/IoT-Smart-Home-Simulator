<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoomStore } from '@/stores/roomStore'

const roomStore = useRoomStore()
const selectedRoom = ref(null)
const emit = defineEmits(['room-selected'])

const isRoomSelected = computed(() => {
  return (room) => room.id === selectedRoom.value
})

const handleRoomSelected = (roomId) => {
  selectedRoom.value = roomId
  emit('room-selected', roomId)  
}

onMounted(() => {
    if (roomStore.rooms.length === 0) {
        roomStore.fetchRooms()
    }
})

</script>

<template>
     <nav class="flex flex-wrap gap-3 bg-card border border-border rounded-xl p-4 mb-6">
      <div class="flex items-center gap-2 text-sm text-muted-foreground mb-2 w-full">
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
        </svg>
        Select Room
      </div>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="room in roomStore.rooms"
          :key="room.id"
          @click="handleRoomSelected(room.id)"
          :class="[
            'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border',
            isRoomSelected(room) 
              ? 'bg-primary text-primary-foreground border-primary shadow-sm' 
              : 'bg-secondary text-secondary-foreground border-border hover:bg-accent hover:text-accent-foreground hover:border-accent'
          ]"
        >
          {{ room.name }}
        </button>
      </div>
    </nav>
</template>