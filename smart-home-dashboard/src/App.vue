<script setup>
  import Navbar from './components/Navbar.vue';
  import socket from './services/websocket';

  socket.connect()

</script>

<template>
  <div class="min-h-screen bg-gray-700">
    <Navbar></Navbar>  
    <main class="p-4">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
</style>
