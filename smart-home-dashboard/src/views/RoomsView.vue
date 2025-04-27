<script setup>
import { onMounted, computed } from 'vue'
import { useRoomStore } from '@/stores/roomStore'

const roomStore = useRoomStore()

console.log(roomStore.rooms)

</script>

<template>
    <div class="max-w-7xl mx-auto p-4 sm:p-6 md:p-8">
      <h1 class="text-3xl font-bold mb-4">Rooms</h1>
      <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <li v-for="room in roomStore.rooms" :key="room.id" class="bg-white rounded shadow-md p-4 relative">
          <button
            class="absolute top-2 right-2 text-red-500 hover:text-red-700 text-lg"
            @click="removeRoom(room.id)"
          >
            &#215;
          </button>
          <h2 class="text-lg font-bold mb-2">{{ room.name }}</h2>
          <p class="text-gray-600">Description</p>
        </li>
      </ul>
      <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
        @click="addNewRoom"
      >
        Add New Room
      </button>
    </div>
  </template>