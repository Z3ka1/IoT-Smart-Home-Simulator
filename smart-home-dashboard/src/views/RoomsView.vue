<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRoomStore } from '@/stores/roomStore'
import PopupWindow from '@/components/PopupWindow.vue'

const roomStore = useRoomStore()
let popupIsActive = ref(false)

console.log(roomStore.rooms)

const newRoomName = ref('')

const addNewRoom = async () => {
    if (!newRoomName.value.trim()) return

    try {
        await roomStore.addRoom( {name: newRoomName.value} )
        newRoomName.value = ''
        popupIsActive.value = false
    } catch (error) {
        console.error('Error adding room:', error);
        alert('Error adding room')
    }
}


</script>

<template>
    <div class="max-w-7xl mx-auto p-4 sm:p-6 md:p-8">
      <h1 class="text-3xl font-bold mb-4">Rooms</h1>
      <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <li v-for="room in roomStore.rooms" :key="room.id" class="bg-white rounded shadow-md p-4 relative">
          <button
            class="absolute top-2 right-2 text-red-500 hover:text-red-700 text-lg"
            @click="roomStore.removeRoom(room.id)"
          >
            &#215;
          </button>
          <h2 class="text-lg font-bold mb-2">{{ room.name }}</h2>
          <p class="text-gray-600">Description</p>
        </li>
      </ul>
      <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4"
        @click="popupIsActive=true"
      >
        Add New Room
      </button>

      <PopupWindow @closePopup="popupIsActive = false"
        v-if="popupIsActive">
        <div class="form space-y-4">
            <label for="roomName" class="block text-sm font-medium">Room Name</label>
            <input
            type="text"
            id="roomName"
            v-model="newRoomName"
            placeholder="Enter Room Name"
            class="input-field border rounded px-3 py-2 w-full"
            />

            <div class="flex justify-end space-x-2 mt-4">
                <button
                    @click="popupIsActive = false"
                    class="bg-gray-300 hover:bg-gray-400 text-black px-4 py-2 rounded"
                >
                    Cancel
                </button>
                <button
                    @click="addNewRoom"
                    class="bg-blue-500 hover:bg-blue-700 text-white px-4 py-2 rounded"
                >
                    Add Room
                </button>
            </div>
        </div>
      </PopupWindow>

    </div>
  </template>