<script setup>
  import Navbar from './components/Navbar.vue';
  import socket from './services/websocket';

  socket.connect()

</script>

<template>
  <div class="min-h-screen bg-background text-foreground">
    <Navbar></Navbar>  
    <main class="p-6">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
</style>
