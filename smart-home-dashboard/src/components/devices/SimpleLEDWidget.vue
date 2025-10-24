<script setup>
import { ref, watch, onMounted, watchEffect, onUnmounted } from 'vue'
import axios from '../../utils/axios'
import debounce from 'lodash/debounce'
import { truncateText, truncateDescription } from '@/utils/stringUtils'

const props = defineProps({ device: Object })

const isOn = ref(false)
const ignoreNextUpdate = ref(false)
const isAvailable = ref(true)

const displayDeviceName = truncateText(props.device.name, 17, 'LED Light')
const displayDeviceDescription = truncateDescription(props.device.description, 17, 'Smart LED')

onMounted(() => {
    isOn.value = props.device.properties?.state === 'on'
    isAvailable.value = props.device.available
})

// Watch for prop changes (e.g., polling)
watch(() => props.device.properties?.state, (newVal) => {
  if (!ignoreNextUpdate.value) {
    isOn.value = newVal === 'on'
  }
})

const updateDeviceState = debounce(async (newValue) => {
    ignoreNextUpdate.value = true
    try {
        await axios.put(`http://localhost:8000/api/devices/simpleled/${props.device.id}/state`, {
            state: newValue
        })
        console.log(`LED light ${newValue ? 'ON' : 'OFF'}`)
    } catch (error) {
        console.error('Failed to update device state:', error)
        isOn.value = !newValue
    } finally {
        setTimeout(() => {
            ignoreNextUpdate.value = false
        }, 200) //delay to allow backend update
    }
}, 200) //debounce delay

watch(isOn, async(newValue, oldValue) => {
    if (newValue !== oldValue && !ignoreNextUpdate.value) {
        updateDeviceState(newValue)
    }
})

watch(() => props.device.available, (newVal) => {
  isAvailable.value = newVal
})
</script>

<template>
  <div class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-all duration-200 group"
      :class = "{'opacity-50 grayscale pointer-events-none': !isAvailable}">
    
    <!-- Header with device info and toggle -->
    <div class="flex items-start justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-secondary-foreground" fill="currentColor" viewBox="0 0 20 20">
            <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.477.859h4z"/>
          </svg>
        </div>
        <div>
          <h3 class="font-semibold text-foreground" :title="device.name">{{ displayDeviceName }}</h3>
          <p class="text-sm text-muted-foreground">{{ displayDeviceDescription }}</p>
        </div>
      </div>
      
      <!-- Toggle switch -->
      <label class="relative inline-flex items-center cursor-pointer">
        <input type="checkbox" v-model="isOn" :disabled="!isAvailable" class="sr-only peer">
        <div class="w-11 h-6 bg-muted peer-focus:outline-none rounded-full peer peer-checked:bg-primary transition-colors duration-300 relative">
          <div class="absolute left-1 top-1 w-4 h-4 bg-background rounded-full shadow-sm transform transition-transform duration-300 peer-checked:translate-x-5"></div>
        </div>
      </label>
    </div>

    <!-- Status section -->
    <div class="space-y-3">
      <div class="flex items-center justify-between">
        <span class="text-sm text-muted-foreground">Status</span>
        <div class="flex items-center gap-2">
          <div :class="[
            'w-2 h-2 rounded-full',
            isOn ? 'bg-success' : 'bg-muted-foreground'
          ]"></div>
          <span :class="[
            'text-sm font-medium',
            isOn ? 'text-success' : 'text-muted-foreground'
          ]">{{ isOn ? 'On' : 'Off' }}</span>
        </div>
      </div>
      
      <div class="flex items-center justify-between">
        <span class="text-sm text-muted-foreground">Connection</span>
        <div class="flex items-center gap-2">
          <div :class="[
            'w-2 h-2 rounded-full',
            isAvailable ? 'bg-success' : 'bg-destructive'
          ]"></div>
          <span :class="[
            'text-sm font-medium',
            isAvailable ? 'text-success' : 'text-destructive'
          ]">{{ isAvailable ? 'Online' : 'Offline' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Enhanced toggle animation */
input:checked + div > div {
  transform: translateX(1.25rem);
}
</style>
