<script setup>
import {ref} from 'vue';

const isOpen = ref(false);
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
  
      <ul
        class="md:flex space-x-6 hidden"
      >
        <li><router-link to="/" class="hover:text-blue-400">Dashboard</router-link></li>
        <li><router-link to="/deviceList" class="hover:text-blue-400">Device List</router-link></li>
        <li><router-link to="/pair" class="hover:text-blue-400">Pair Device</router-link></li>
        <li><router-link to="/rooms" class="hover:text-blue-400">Rooms</router-link></li>
      </ul>
  
      <!-- Mobile Menu -->
      <ul
        v-if="isOpen"
        class="absolute top-16 left-0 w-full bg-gray-800 flex flex-col items-center space-y-4 py-4 md:hidden"
      >
        <li><router-link to="/" @click="isOpen = false">Dashboard</router-link></li>
        <li><router-link to="/deviceList" @click="isOpen = false">Device List</router-link></li>
        <li><router-link to="/pair" @click="isOpen = false">Pair Device</router-link></li>
        <li><router-link to="/rooms" @click="isOpen = false">Rooms</router-link></li>
      </ul>
    </nav>
  </template>

<style scoped>

</style>

