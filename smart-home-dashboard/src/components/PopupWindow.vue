<script setup>

</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4" aria-modal="true" role="dialog" tabindex="-1">
    <div class="absolute inset-0 bg-background/80 backdrop-blur-sm" @click="$emit('closePopup')"></div>
    
    <div class="relative bg-card border border-border rounded-xl p-6 shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
      <button 
        class="absolute top-4 right-4 w-8 h-8 bg-secondary hover:bg-accent rounded-lg flex items-center justify-center text-muted-foreground hover:text-foreground transition-colors"
        @click="$emit('closePopup')"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
        </svg>
      </button>

      <slot></slot>
    </div>
  </div>

</template>

<style scoped>
</style>