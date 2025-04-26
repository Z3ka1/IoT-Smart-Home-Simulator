<script setup>
defineProps({ device: Object })
</script>

<template>
    <div class="thermometer-widget">
      <p>{{ device.type }}</p>
      <!-- <p>Color: {{ device.value }}</p> -->
    </div>
</template>

  