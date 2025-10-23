<script setup>
import { ref, computed } from 'vue'
import { useDeviceStore } from '@/stores/deviceStore'
import { useRoomStore } from '@/stores/roomStore'
import axios from '../utils/axios'

const deviceStore = useDeviceStore()
const roomStore = useRoomStore()

const getRoomName = (roomId) => {
  const room = roomStore.rooms.find(r => r.id === roomId)
  return room ? room.name : 'Unknown Room'
}

const formatPropertyValue = (value) => {
  if (typeof value === 'boolean') return value ? 'Yes' : 'No'
  if (value === null || value === undefined) return 'N/A'
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

const deleteDevice = async (deviceId, deviceName) => {
  if (!confirm(`Are you sure you want to delete "${deviceName}"? This action cannot be undone.`)) {
    return
  }

  try {
    const response = await axios.delete(`http://localhost:8000/api/devices/remove/${deviceId}`)
    if (response.status === 200) {
      // Remove device from store
      deviceStore.devices = deviceStore.devices.filter(d => d.id !== deviceId)
      alert('Device deleted successfully')
    }
  } catch (error) {
    console.error('Error deleting device:', error)
    alert('Error deleting device')
  }
}

const getDeviceIcon = (type) => {
  const icons = {
    'simpleled': 'simpleled.png',
    'rgbstrip': 'rgbstrip.png',
    'lcddisplay': 'lcddisplay.png',
    'weatherstation': 'weatherstation.png',
    'alarmsensor': 'alarmsensor.png'
  }
  return `/device-icons/${icons[type] || 'genericdevice.png'}`
}
</script>

<template>
  <div class="max-w-7xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-foreground">All Devices</h1>
        <p class="text-muted-foreground mt-2">View and manage all your smart home devices</p>
      </div>
      <div class="text-sm text-muted-foreground">
        Total: <span class="font-semibold text-foreground">{{ deviceStore.devices.length }}</span> devices
      </div>
    </div>

    <div v-if="deviceStore.isLoading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      <p class="text-muted-foreground mt-4">Loading devices...</p>
    </div>

    <div v-else-if="deviceStore.devices.length === 0" class="text-center py-12 bg-card border border-border rounded-xl">
      <svg class="w-16 h-16 mx-auto text-muted-foreground mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
      </svg>
      <h3 class="text-lg font-semibold text-foreground mb-2">No devices found</h3>
      <p class="text-muted-foreground">Start by pairing a new device to your smart home</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="device in deviceStore.devices"
        :key="device.id"
        class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-all duration-200"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 bg-secondary rounded-xl flex items-center justify-center text-2xl">
              <!-- {{ getDeviceIcon(device.type) }} -->
              <img :src="getDeviceIcon(device.type)" 
                 :alt="deviceType"
                 class="w-12 h-12 object-contain drop-shadow-lg" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-foreground">{{ device.name }}</h3>
              <div class="flex items-center gap-3 mt-1">
                <span class="text-sm text-muted-foreground">{{ device.type }}</span>
                <span class="text-muted-foreground">•</span>
                <span class="text-sm text-muted-foreground">{{ getRoomName(device.roomId) }}</span>
              </div>
            </div>
          </div>
          
          <div class="flex items-center gap-3">
            <div class="flex items-center gap-2">
              <div :class="[
                'w-2 h-2 rounded-full',
                device.available ? 'bg-success' : 'bg-destructive'
              ]"></div>
              <span class="text-sm font-medium" :class="device.available ? 'text-success' : 'text-destructive'">
                {{ device.available ? 'Online' : 'Offline' }}
              </span>
            </div>
            
            <button
              @click="deleteDevice(device.id, device.name)"
              class="w-9 h-9 bg-destructive/10 hover:bg-destructive/20 text-destructive rounded-lg flex items-center justify-center transition-colors"
              title="Delete device"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </div>

        <div v-if="device.description" class="mb-4 text-sm text-muted-foreground">
          {{ device.description }}
        </div>

        <div class="border-t border-border pt-4">
          <h4 class="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
              <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
            </svg>
            Device Properties
          </h4>
          
          <div v-if="device.properties && Object.keys(device.properties).length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <div
              v-for="(value, key) in device.properties"
              :key="key"
              class="bg-secondary/50 rounded-lg p-3"
            >
              <div class="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">
                {{ key.replace(/_/g, ' ') }}
              </div>
              <div class="text-sm font-semibold text-foreground break-words">
                {{ formatPropertyValue(value) }}
              </div>
            </div>
          </div>
          
          <div v-else class="text-sm text-muted-foreground italic">
            No properties available
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
