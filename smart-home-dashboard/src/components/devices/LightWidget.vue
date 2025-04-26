<script setup>
defineProps({ device: Object })
</script>

<template>
    <div class="light-widget">
      <p>{{ device.type }}</p>
      <!-- <p>Color: {{ device.color }}</p> -->
    </div>
</template>

  