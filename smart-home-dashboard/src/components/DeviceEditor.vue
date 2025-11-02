<script setup>
import { ref, computed } from 'vue'
import { useRoomStore } from '@/stores/roomStore'

const roomStore = useRoomStore()

const props = defineProps({
  device: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['save', 'close'])

const formData = ref({
  name: props.device.name,
  description: props.device.description || '',
  roomId: props.device.roomId
})

const isLoading = ref(false)
const errorMessage = ref('')

const isFormValid = computed(() => {
  return formData.value.name.trim() && formData.value.roomId
})

const handleSave = async () => {
  if (!isFormValid.value) return

  isLoading.value = true
  errorMessage.value = ''

  try {
    emit('save', {
      id: props.device.id,
      name: formData.value.name.trim(),
      description: formData.value.description.trim(),
      room_id: formData.value.roomId
    })
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isLoading.value = false
  }
}

const handleClose = () => {
  emit('close')
}
</script>

<template>
  <div>
    <h2 class="text-xl font-bold text-foreground mb-6">Edit Device</h2>

    <div v-if="errorMessage" class="mb-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive text-sm">
      {{ errorMessage }}
    </div>

    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-foreground mb-2">Device Name</label>
        <input
          v-model="formData.name"
          type="text"
          maxlength="100"
          class="w-full px-3 py-2 bg-secondary border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          placeholder="Enter device name"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-foreground mb-2">Description (Optional)</label>
        <textarea
          v-model="formData.description"
          rows="3"
          maxlength="255"
          class="w-full px-3 py-2 bg-secondary border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
          placeholder="Enter device description"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-foreground mb-2">Room</label>
        <select
          v-model="formData.roomId"
          class="w-full px-3 py-2 bg-secondary border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        >
          <option value="">Select a room</option>
          <option v-for="room in roomStore.rooms" :key="room.id" :value="room.id">
            {{ room.name }}
          </option>
        </select>
      </div>
    </div>

    <div class="flex gap-3 mt-6">
      <button
        @click="handleSave"
        :disabled="!isFormValid || isLoading"
        class="flex-1 px-4 py-2 bg-primary hover:bg-primary/90 disabled:bg-primary/50 text-white font-medium rounded-lg transition-colors"
      >
        {{ isLoading ? 'Saving...' : 'Save Changes' }}
      </button>
      <button
        @click="handleClose"
        :disabled="isLoading"
        class="flex-1 px-4 py-2 bg-secondary hover:bg-secondary/80 text-foreground font-medium rounded-lg transition-colors"
      >
        Cancel
      </button>
    </div>
  </div>
</template>
