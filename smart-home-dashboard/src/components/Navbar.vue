<script setup>
import {ref} from 'vue';
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router';
import { useRoomStore } from '@/stores/roomStore';
import { useThemeStore } from '@/stores/themeStore';

// isOpen used for better look on mobile devices.
const isOpen = ref(false);
const auth = useAuthStore();
const router = useRouter();
const roomStore = useRoomStore();
const themeStore = useThemeStore();

const handleLogout = () => {
  auth.logout();
  roomStore.resetRooms();
  router.push('/login');
}
</script>

<template>
  <nav class="bg-card border-b border-border px-6 py-4 flex justify-between items-center shadow-sm">
    <router-link
      to="/"
      class="text-2xl font-bold text-primary flex items-center gap-3 hover:opacity-80 transition-opacity"
    >
      <div class="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
        <svg class="w-5 h-5 text-primary-foreground" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
        </svg>
      </div>
      Smart Home
    </router-link>
  
    <button
      class="md:hidden block text-foreground hover:text-primary focus:outline-none transition-colors"
      @click="isOpen = !isOpen"
    >
      <svg class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="2"
           viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
    </button>
  
    <ul class="md:flex space-x-1 hidden items-center">
      <template v-if="auth.loggedIn">
        <li><router-link to="/" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Dashboard</router-link></li>
        <li><router-link to="/devices" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Devices</router-link></li>
        <li><router-link to="/pair" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Pair Device</router-link></li>
        <li><router-link to="/rooms" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Rooms</router-link></li>
        <li><button @click="handleLogout" class="px-4 py-2 rounded-lg hover:bg-destructive hover:text-destructive-foreground transition-colors">Logout</button></li>
        <li>
          <button
            @click="themeStore.toggleTheme"
            class="ml-4 px-3 py-2 text-sm rounded-lg text-muted-foreground hover:bg-muted/70 transition"
          >
            {{ themeStore.theme === 'dark' ? '☀️' : '🌑' }}
          </button>
        </li>
      </template>
      <template v-else>
        <li><router-link to="/login" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Login</router-link></li>
        <li><router-link to="/register" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Register</router-link></li>
      </template>
    </ul>
  
    <ul
      v-if="isOpen"
      class="absolute top-16 left-0 w-full bg-card border-b border-border flex flex-col items-center space-y-2 py-4 md:hidden shadow-lg z-50"
    >
      <template v-if="auth.loggedIn">
        <li><router-link to="/" @click="isOpen = false" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Dashboard</router-link></li>
        <li><router-link to="/devices" @click="isOpen = false" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Devices</router-link></li>
        <li><router-link to="/pair" @click="isOpen = false" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Pair Device</router-link></li>
        <li><router-link to="/rooms" @click="isOpen = false" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Rooms</router-link></li>
        <li><button @click="handleLogout(); isOpen = false" class="px-4 py-2 rounded-lg hover:bg-destructive hover:text-destructive-foreground transition-colors">Logout</button></li>
        <li>
          <button
            @click="themeStore.toggleTheme"
            class="ml-4 px-3 py-2 text-sm rounded-lg text-muted-foreground hover:bg-muted/70 transition"
          >
            {{ themeStore.theme === 'dark' ? '☀️' : '🌑' }}
          </button>
        </li>
      </template>
      <template v-else>
        <li><router-link to="/login" @click="isOpen = false" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Login</router-link></li>
        <li><router-link to="/register" @click="isOpen = false" class="px-4 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors">Register</router-link></li>
      </template>
    </ul>
  </nav>
</template>

<style scoped>

</style>

