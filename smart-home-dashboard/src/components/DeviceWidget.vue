<script setup>
import { onMounted, computed, ref, watch } from 'vue'

const props = defineProps({
  device: {
    device: Object,
    required: true
  }
})

onMounted(() => {
    console.log('DeviceWidget rendered:', props.device.name)
})
console.log(props.device.name)
</script>

<template>
    <div class="device-widget p-4 rounded-lg shadow-md bg-white">
      <h2 class="text-lg font-semibold text-gray-800">{{ device.name }}</h2>
    </div>
  </template>