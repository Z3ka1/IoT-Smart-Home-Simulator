<script setup>
import {ref} from 'vue';
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router';
import { useRoomStore } from '@/stores/roomStore';

const isOpen = ref(false);
const auth = useAuthStore();
const router = useRouter();
const roomStore = useRoomStore();

const handleLogout = () => {
  auth.logout();
  roomStore.resetRooms();
  router.push('/login');
}
</script>

<template>
    <nav class="bg-gray-900 text-white px-6 py-4 flex justify-between items-center">
      <div class="text-2xl font-bold">Smart Home</div>
  
      <button
        class="md:hidden block text-white focus:outline-none"
        @click="isOpen = !isOpen"
      >
        <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2"
             viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
      </button>
  
      <ul class="md:flex space-x-6 hidden">
        <template v-if="auth.loggedIn">
          <li><router-link to="/" class="hover:text-blue-400">Dashboard</router-link></li>
          <li><router-link to="/deviceList" class="hover:text-blue-400">Device List</router-link></li>
          <li><router-link to="/pair" class="hover:text-blue-400">Pair Device</router-link></li>
          <li><router-link to="/rooms" class="hover:text-blue-400">Rooms</router-link></li>
          <li><button @click="handleLogout" class="hover:text-red-400">Logout</button></li>
        </template>
        <template v-else>
          <li><router-link to="/login" class="hover:text-blue-400">Login</router-link></li>
          <li><router-link to="/register" class="hover:text-blue-400">Register</router-link></li>
      </template>
      </ul>
  
      <!-- Mobile Menu -->
      <ul
        v-if="isOpen"
        class="absolute top-16 left-0 w-full bg-gray-800 flex flex-col items-center space-y-4 py-4 md:hidden"
      >
        <template v-if="auth.loggedIn">
          <li><router-link to="/" @click="isOpen = false">Dashboard</router-link></li>
          <li><router-link to="/deviceList" @click="isOpen = false">Device List</router-link></li>
          <li><router-link to="/pair" @click="isOpen = false">Pair Device</router-link></li>
          <li><router-link to="/rooms" @click="isOpen = false">Rooms</router-link></li>
          <li><button @click="auth.logout(); isOpen = false" class="text-red-400">Logout</button></li>
        </template>
        <template v-else>
          <li><router-link to="/login" @click="isOpen = false">Login</router-link></li>
          <li><router-link to="/register" @click="isOpen = false">Register</router-link></li>
        </template>
      </ul>
    </nav>
  </template>

<style scoped>

</style>

