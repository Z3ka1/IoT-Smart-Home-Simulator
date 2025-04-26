<script setup>
import { onMounted, computed } from 'vue'
import { useRoomStore } from '@/stores/roomStore'

const roomStore = useRoomStore()

onMounted(() => {
    if (roomStore.rooms.length === 0) {
        roomStore.fetchRooms()
    }
})
console.log(roomStore.rooms)

</script>

<template>
    <div>
        <h1>Rooms</h1>

        <div v-if="roomStore.isLoading">Loading rooms...</div>
        <h3
            v-for="room in roomStore.rooms"
            :key="room.id"
        >
            {{ room.name }}
        </h3>

    </div>
</template>