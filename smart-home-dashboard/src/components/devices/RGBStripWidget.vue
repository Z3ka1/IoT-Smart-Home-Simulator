<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from '../../utils/axios'
import debounce from 'lodash/debounce'
import { truncateText, truncateDescription } from '@/utils/stringUtils'

const props = defineProps({ device: Object })

const isExpanded = ref(false)
const isOn = ref(false)
const red = ref(0)
const green = ref(0)
const blue = ref(0)
const brightness = ref(100)
const ignoreNextUpdate = ref(false)
const isAvailable = ref(true)
const isInitializing = ref(true)

const displayDeviceName = truncateText(props.device.name, 17, 'RGB Strip')
const displayDeviceDescription = truncateDescription(props.device.description, 17, 'Smart RGB Led')

onMounted(() => {
  isInitializing.value = true

  isOn.value = props.device.properties?.state === 'on'
  red.value = props.device.properties?.red || 0
  green.value = props.device.properties?.green || 0
  blue.value = props.device.properties?.blue || 0
  brightness.value = props.device.properties?.brightness || 100
  isAvailable.value = props.device.available

  setTimeout(() => {
    isInitializing.value = false
  }, 500)
})

watch(() => props.device.properties?.state, (newVal) => {
  if (!ignoreNextUpdate.value) {
    isOn.value = newVal === 'on'
  }
})

watch(() => props.device.properties?.red, (newVal) => {
  if (!ignoreNextUpdate.value && newVal !== undefined) {
    red.value = newVal
  }
})

watch(() => props.device.properties?.green, (newVal) => {
  if (!ignoreNextUpdate.value && newVal !== undefined) {
    green.value = newVal
  }
})

watch(() => props.device.properties?.blue, (newVal) => {
  if (!ignoreNextUpdate.value && newVal !== undefined) {
    blue.value = newVal
  }
})

watch(() => props.device.properties?.brightness, (newVal) => {
  if (!ignoreNextUpdate.value && newVal !== undefined) {
    brightness.value = newVal
  }
})

watch(() => props.device.available, (newVal) => {
  isAvailable.value = newVal
})

const currentColor = () => {
  return `rgb(${red.value}, ${green.value}, ${blue.value})`
}

const updateDeviceState = debounce(async (newValue) => {
  ignoreNextUpdate.value = true
  try {
    await axios.put(`http://localhost:8000/api/devices/rgbstrip/${props.device.id}/state`, {
      state: newValue
    })
    console.log(`RGB Strip ${newValue ? 'ON' : 'OFF'}`)
  } catch (error) {
    console.error('Failed to update device state:', error)
    isOn.value = !newValue
  } finally {
    setTimeout(() => {
      ignoreNextUpdate.value = false
    }, 200)
  }
}, 200)

const updateColor = debounce(async () => {
  if (isInitializing.value) return

  ignoreNextUpdate.value = true
  try {
    await axios.put(`http://localhost:8000/api/devices/rgbstrip/${props.device.id}/color`, {
      red: red.value,
      green: green.value,
      blue: blue.value
    })
    console.log(`RGB Strip color updated: R${red.value} G${green.value} B${blue.value}`)
  } catch (error) {
    console.error('Failed to update color:', error)
  } finally {
    setTimeout(() => {
      ignoreNextUpdate.value = false
    }, 200)
  }
}, 300)

const updateBrightness = debounce(async (newValue) => {
  if (isInitializing.value) return

  ignoreNextUpdate.value = true
  try {
    await axios.put(`http://localhost:8000/api/devices/rgbstrip/${props.device.id}/brightness`, {
      brightness: newValue
    })
    console.log(`RGB Strip brightness: ${newValue}%`)
  } catch (error) {
    console.error('Failed to update brightness:', error)
  } finally {
    setTimeout(() => {
      ignoreNextUpdate.value = false
    }, 200)
  }
}, 300)

watch(isOn, async(newValue, oldValue) => {
  if (newValue !== oldValue && !ignoreNextUpdate.value) {
    updateDeviceState(newValue)
  }
})

watch([red, green, blue], () => {
  if (!ignoreNextUpdate.value) {
    updateColor()
  }
})

watch(brightness, (newValue, oldValue) => {
  if (newValue !== oldValue && !ignoreNextUpdate.value) {
    updateBrightness(newValue)
  }
})
</script>

<template>
  <div class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-all duration-200 group"
      :class="{'opacity-50 grayscale': !isAvailable}">
    
    <!-- Header with device info and toggle -->
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center transition-all duration-300"
             :style="{ backgroundColor: isOn ? currentColor() : '' }">
          <svg class="w-5 h-5" :class="isOn ? 'text-white' : 'text-secondary-foreground'" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clip-rule="evenodd"/>
          </svg>
        </div>
        <div>
          <h3 class="font-semibold text-foreground" :title = "device.name">{{ displayDeviceName }}</h3>
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

    <!-- Compact color preview and status (always visible) -->
    <div class="space-y-3">
      <div class="h-12 rounded-lg border border-border transition-all duration-300"
           :style="{ backgroundColor: currentColor(), opacity: isOn ? (brightness / 100) : 0.3 }">
      </div>
      
      <div class="flex items-center justify-between text-sm">
        <div class="flex items-center gap-2">
          <div :class="[
            'w-2 h-2 rounded-full',
            isOn ? 'bg-success' : 'bg-muted-foreground'
          ]"></div>
          <span :class="[
            'font-medium',
            isOn ? 'text-success' : 'text-muted-foreground'
          ]">{{ isOn ? 'On' : 'Off' }}</span>
        </div>
        
        <!-- Connection indicator in collapsed state -->
        <div class="flex items-center gap-2">
          <div :class="[
            'w-2 h-2 rounded-full',
            isAvailable ? 'bg-success' : 'bg-destructive'
          ]"></div>
          <span :class="[
            'text-xs',
            isAvailable ? 'text-success' : 'text-destructive'
          ]">{{ isAvailable ? 'Online' : 'Offline' }}</span>
        </div>
      </div>
      
      <!-- Expand/collapse button -->
      <button 
        @click="isExpanded = !isExpanded"
        class="w-full flex items-center justify-center gap-1 text-muted-foreground hover:text-foreground transition-colors py-2"
      >
        <span class="text-xs">{{ isExpanded ? 'Show Less' : 'Show More' }}</span>
        <svg 
          class="w-4 h-4 transition-transform duration-300" 
          :class="{ 'rotate-180': isExpanded }"
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </button>
    </div>

    <!-- Expandable controls section -->
    <div 
      class="overflow-hidden transition-all duration-300"
      :style="{ maxHeight: isExpanded ? '500px' : '0' }"
    >
      <div class="pt-4 mt-4 border-t border-border space-y-4">
        <!-- RGB Sliders -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="text-sm font-medium text-foreground">Red</label>
            <span class="text-sm text-muted-foreground">{{ red }}</span>
          </div>
          <input 
            type="range" 
            v-model.number="red" 
            min="0" 
            max="255" 
            :disabled="!isAvailable"
            class="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer slider-red"
          />
        </div>

        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="text-sm font-medium text-foreground">Green</label>
            <span class="text-sm text-muted-foreground">{{ green }}</span>
          </div>
          <input 
            type="range" 
            v-model.number="green" 
            min="0" 
            max="255" 
            :disabled="!isAvailable"
            class="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer slider-green"
          />
        </div>

        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="text-sm font-medium text-foreground">Blue</label>
            <span class="text-sm text-muted-foreground">{{ blue }}</span>
          </div>
          <input 
            type="range" 
            v-model.number="blue" 
            min="0" 
            max="255" 
            :disabled="!isAvailable"
            class="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer slider-blue"
          />
        </div>

        <!-- Brightness Slider -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="text-sm font-medium text-foreground">Brightness</label>
            <span class="text-sm text-muted-foreground">{{ brightness }}%</span>
          </div>
          <input 
            type="range" 
            v-model.number="brightness" 
            min="0" 
            max="100" 
            :disabled="!isAvailable"
            class="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer slider-brightness"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
input:checked + div > div {
  transform: translateX(1.25rem);
}

input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: hsl(var(--primary));
  cursor: pointer;
  border: 2px solid hsl(var(--background));
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input[type="range"]::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: hsl(var(--primary));
  cursor: pointer;
  border: 2px solid hsl(var(--background));
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider-red::-webkit-slider-runnable-track {
  background: linear-gradient(to right, hsl(var(--muted)), rgb(255, 0, 0));
}

.slider-red::-moz-range-track {
  background: linear-gradient(to right, hsl(var(--muted)), rgb(255, 0, 0));
}

.slider-green::-webkit-slider-runnable-track {
  background: linear-gradient(to right, hsl(var(--muted)), rgb(0, 255, 0));
}

.slider-green::-moz-range-track {
  background: linear-gradient(to right, hsl(var(--muted)), rgb(0, 255, 0));
}

.slider-blue::-webkit-slider-runnable-track {
  background: linear-gradient(to right, hsl(var(--muted)), rgb(0, 0, 255));
}

.slider-blue::-moz-range-track {
  background: linear-gradient(to right, hsl(var(--muted)), rgb(0, 0, 255));
}

.slider-brightness::-webkit-slider-runnable-track {
  background: linear-gradient(to right, hsl(var(--muted)), hsl(var(--foreground)));
}

.slider-brightness::-moz-range-track {
  background: linear-gradient(to right, hsl(var(--muted)), hsl(var(--foreground)));
}

input[type="range"]:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
