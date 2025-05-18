<script setup>
import { ref, watch, onMounted, watchEffect } from 'vue'
import axios from 'axios'
import debounce from 'lodash/debounce'

const props = defineProps({ device: Object })

const isOn = ref(false)
const ignoreNextUpdate = ref(false)

onMounted(() => {
    isOn.value = props.device.properties?.state === 'on'
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
        }, {
            headers: {'X-Gateway-ID': localStorage.getItem('gatewayId') || ''}
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
</script>

<template>
  <div class="relative rounded-2xl shadow-md p-4 bg-white w-64 h-32">
    <!-- On/Off Toggle -->
    <label class="absolute top-3 right-3 inline-flex items-center cursor-pointer">
      <input type="checkbox" v-model="isOn" class="sr-only peer">
      <div class="w-11 h-6 bg-gray-300 peer-focus:outline-none rounded-full peer peer-checked:bg-green-500 transition-colors duration-300"></div>
      <div class="absolute left-1 top-1 w-4 h-4 bg-white rounded-full shadow transform transition-transform duration-300"
           :class="{ 'translate-x-full': isOn }"></div>
    </label>

    <!-- Device Type -->
    <h3 class="text-lg font-semibold text-gray-800 mb-2">{{ device.name || 'LED Light' }}</h3>

    <!-- Status Text -->
    <p class="text-sm text-gray-500">Status: <span :class="isOn ? 'text-green-600' : 'text-red-500'">{{ isOn ? 'On' : 'Off' }}</span></p>
  </div>
</template>

<style scoped>
/* For smooth slider toggle animation */
input:checked + div + div {
  transform: translateX(1.25rem); /* Adjust to match toggle width */
}
</style>
