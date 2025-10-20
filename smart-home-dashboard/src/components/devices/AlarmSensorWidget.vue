<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from '../../utils/axios'
import debounce from 'lodash/debounce'

const props = defineProps({ device: Object })

const isEnabled = ref(false) // is_alarm_enabled
const motionDetected = ref(false) // motion_detected
const ignoreNextUpdate = ref(false)
const isAvailable = ref(true)

onMounted(() => {
  isEnabled.value = props.device.properties?.is_alarm_enabled
  motionDetected.value = props.device.properties?.motion_detected
  isAvailable.value = props.device.available
})

// Watch props for backend changes (polling/websocket updates)
watch(() => props.device.properties?.is_alarm_enabled, newVal => {
    if (!ignoreNextUpdate.value) isEnabled.value = newVal === true
})
watch(() => props.device.properties?.motion_detected,newVal => {
    motionDetected.value = newVal === true
})

watch(() => props.device.available, newVal => {
    isAvailable.value = newVal
})

// PUT to backend when toggled locally
const updateDeviceState = debounce(async newValue => {
  ignoreNextUpdate.value = true
  try {
    await axios.put(
      `http://localhost:8000/api/devices/alarmsensor/${props.device.id}/alarm_enabled`,
      { is_alarm_enabled: newValue }
    )
    console.log(`Alarm ${newValue ? 'ENABLED' : 'DISABLED'}`)
  } catch (error) {
    console.error('Failed to update alarm state:', error)
    isEnabled.value = !newValue // revert on error
  } finally {
    setTimeout(() => {
      ignoreNextUpdate.value = false
    }, 200)
  }
}, 200)

watch(isEnabled, (newValue, oldValue) => {
  if (newValue !== oldValue && !ignoreNextUpdate.value) {
    updateDeviceState(newValue)
  }
})
</script>

<template>
  <div
    class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-all duration-200 group"
    :class="{ 'opacity-50 grayscale pointer-events-none': !isAvailable }">
    <!-- Header -->
    <div class="flex items-start justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
          <!-- Alarm Icon -->
          <svg class="w-5 h-5 text-secondary-foreground" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2a9 9 0 00-9 9v5H2v2h20v-2h-1v-5a9 9 0 00-9-9zm0 2a7 7 0 017 7v5H5v-5a7 7 0 017-7zm-1 10h2v2h-2v-2zm0-6h2v4h-2V8z"/>
          </svg>
        </div>
        <div>
          <h3 class="font-semibold text-foreground">{{ device.name || 'Alarm' }}</h3>
          <p class="text-sm text-muted-foreground">Motion Alarm</p>
        </div>
      </div>

      <!-- Toggle switch -->
      <label class="relative inline-flex items-center cursor-pointer">
        <input type="checkbox" v-model="isEnabled" :disabled="!isAvailable" class="sr-only peer"/>
        <div class="w-11 h-6 bg-muted peer-focus:outline-none rounded-full peer peer-checked:bg-primary transition-colors duration-300 relative">
          <div class="absolute left-1 top-1 w-4 h-4 bg-background rounded-full shadow-sm transform transition-transform duration-300 peer-checked:translate-x-5"></div>
        </div>
      </label>
    </div>

    <!-- Status section -->
    <div class="space-y-3">
      <div class="flex items-center justify-between">
        <span class="text-sm text-muted-foreground">Alarm</span>
        <div class="flex items-center gap-2">
          <div :class="[ 'w-2 h-2 rounded-full', isEnabled ? 'bg-success' : 'bg-muted-foreground' ]" ></div>
          <span :class="[ 'text-sm font-medium', isEnabled ? 'text-success' : 'text-muted-foreground' ]" >{{ isEnabled ? 'Enabled' : 'Disabled' }}</span>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <span class="text-sm text-muted-foreground">Motion</span>
        <div class="flex items-center gap-2">
          <div :class="[ 'w-2 h-2 rounded-full animate-pulse', motionDetected ? 'bg-destructive' : 'bg-muted-foreground' ]"></div>
          <span :class="[ 'text-sm font-medium', motionDetected ? 'text-destructive' : 'text-muted-foreground' 
            ]">{{ motionDetected ? 'Detected!' : 'No motion' }}</span>
        </div>
      </div>

      <div class="flex items-center justify-between">
        <span class="text-sm text-muted-foreground">Connection</span>
        <div class="flex items-center gap-2">
          <div :class="[ 'w-2 h-2 rounded-full', isAvailable ? 'bg-success' : 'bg-destructive' ]" ></div>
          <span :class="[ 'text-sm font-medium', isAvailable ? 'text-success' : 'text-destructive' ]">{{ isAvailable ? 'Online' : 'Offline' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* same toggle animation */
input:checked + div > div {
  transform: translateX(1.25rem);
}
</style>
