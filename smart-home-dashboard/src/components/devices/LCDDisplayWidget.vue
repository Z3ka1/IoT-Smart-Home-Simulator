<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import axios from 'axios'
import debounce from 'lodash/debounce'

const props = defineProps({ device: Object })

const isExpanded = ref(false)
const isOn = ref(false)
const firstLineText = ref('')
const secondLineText = ref('')
const firstLineInput = ref('')
const secondLineInput = ref('')
const displayTheme = ref('matrix-green')
const ignoreNextUpdate = ref(false)
const isAvailable = ref(true)
const firstLineError = ref('')
const secondLineError = ref('')

const themes = {
  'purple-haze': { name: 'Purple Haze', rgb: [148, 0, 110], bg: [26, 0, 18] },
  'lime-burst': { name: 'Lime Burst', rgb: [144, 249, 15], bg: [20, 35, 5] },
  'matrix-green': { name: 'Matrix Green', rgb: [0, 128, 60], bg: [0, 20, 10] },
  'amber-glow': { name: 'Amber Glow', rgb: [255, 209, 0], bg: [35, 28, 0] },
  'solar-flare': { name: 'Solar Flare', rgb: [248, 248, 60], bg: [35, 35, 8] },
  'midnight-blue': { name: 'Midnight Blue', rgb: [80, 80, 145], bg: [10, 10, 20] },
  'crimson': { name: 'Crimson', rgb: [255, 0, 0], bg: [35, 0, 0] },
  'electric-lime': { name: 'Electric Lime', rgb: [0, 255, 0], bg: [0, 35, 0] }
}

const lcdTextColor = computed(() => {
  const theme = themes[displayTheme.value]
  return `rgb(${theme.rgb.join(',')})`
})

const lcdBgColor = computed(() => {
  const theme = themes[displayTheme.value]
  return `rgb(${theme.bg.join(',')})`
})

const lcdBorderColor = computed(() => {
  const theme = themes[displayTheme.value]
  const darkRgb = theme.bg.map(v => Math.max(0, v - 10))
  return `rgb(${darkRgb.join(',')})`
})

onMounted(() => {
  isOn.value = props.device.properties?.state === 'on'
  firstLineText.value = props.device.properties?.first_line_text || ''
  secondLineText.value = props.device.properties?.second_line_text || ''
  displayTheme.value = props.device.properties?.display_theme || 'matrix-green'
  firstLineInput.value = firstLineText.value
  secondLineInput.value = secondLineText.value
  isAvailable.value = props.device.available
})

watch(() => props.device.properties?.state, (newVal) => {
  if (!ignoreNextUpdate.value) {
    isOn.value = newVal === 'on'
  }
})

watch(() => props.device.properties?.first_line_text, (newVal) => {
  if (!ignoreNextUpdate.value && newVal !== undefined) {
    firstLineText.value = newVal
    firstLineInput.value = newVal
  }
})

watch(() => props.device.properties?.second_line_text, (newVal) => {
  if (!ignoreNextUpdate.value && newVal !== undefined) {
    secondLineText.value = newVal
    secondLineInput.value = newVal
  }
})

watch(() => props.device.properties?.display_theme, (newVal) => {
  if (!ignoreNextUpdate.value && newVal !== undefined) {
    displayTheme.value = newVal
  }
})

watch(() => props.device.available, (newVal) => {
  isAvailable.value = newVal
})

const validateText = (text, lineNumber) => {
  if (text.length > 16) {
    return `Line ${lineNumber} must be 16 characters or less`
  }
  return ''
}

const updateDeviceState = debounce(async (newValue) => {
  ignoreNextUpdate.value = true
  try {
    await axios.put(`http://localhost:8000/api/devices/lcddisplay/${props.device.id}/state`, {
      state: newValue
    }, {
      headers: {'X-Gateway-ID': localStorage.getItem('gatewayId') || ''}
    })
    console.log(`LCD Display ${newValue ? 'ON' : 'OFF'}`)
  } catch (error) {
    console.error('Failed to update device state:', error)
    isOn.value = !newValue
  } finally {
    setTimeout(() => {
      ignoreNextUpdate.value = false
    }, 200)
  }
}, 200)

const updateText = async () => {
  // Validate both inputs
  firstLineError.value = validateText(firstLineInput.value, 1)
  secondLineError.value = validateText(secondLineInput.value, 2)
  
  if (firstLineError.value || secondLineError.value) {
    return
  }

  ignoreNextUpdate.value = true
  try {
    await axios.put(`http://localhost:8000/api/devices/lcddisplay/${props.device.id}/text`, {
      first_line_text: firstLineInput.value,
      second_line_text: secondLineInput.value
    }, {
      headers: {'X-Gateway-ID': localStorage.getItem('gatewayId') || ''}
    })
    firstLineText.value = firstLineInput.value
    secondLineText.value = secondLineInput.value
    console.log(`LCD Display text updated`)
  } catch (error) {
    console.error('Failed to update text:', error)
  } finally {
    setTimeout(() => {
      ignoreNextUpdate.value = false
    }, 200)
  }
}

const updateTheme = debounce(async (newTheme) => {
  ignoreNextUpdate.value = true
  try {
    await axios.put(`http://localhost:8000/api/devices/lcddisplay/${props.device.id}/theme`, {
      display_theme: newTheme
    }, {
      headers: {'X-Gateway-ID': localStorage.getItem('gatewayId') || ''}
    })
    console.log(`LCD Display theme updated to ${newTheme}`)
  } catch (error) {
    console.error('Failed to update theme:', error)
    displayTheme.value = props.device.properties?.display_theme || 'matrix-green'
  } finally {
    setTimeout(() => {
      ignoreNextUpdate.value = false
    }, 200)
  }
}, 200)

watch(isOn, async(newValue, oldValue) => {
  if (newValue !== oldValue && !ignoreNextUpdate.value) {
    updateDeviceState(newValue)
  }
})

watch(displayTheme, async(newValue, oldValue) => {
  if (newValue !== oldValue && !ignoreNextUpdate.value) {
    updateTheme(newValue)
  }
})

// Clear errors when user types
watch(firstLineInput, () => {
  if (firstLineError.value) {
    firstLineError.value = validateText(firstLineInput.value, 1)
  }
})

watch(secondLineInput, () => {
  if (secondLineError.value) {
    secondLineError.value = validateText(secondLineInput.value, 2)
  }
})
</script>

<template>
  <div class="bg-card border border-border rounded-xl p-6 shadow-sm hover:shadow-md transition-all duration-200 group"
      :class="{'opacity-50 grayscale': !isAvailable}">
    
    <!-- Header with device info and toggle  -->
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-secondary-foreground" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm3.293 1.293a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 01-1.414-1.414L7.586 10 5.293 7.707a1 1 0 010-1.414zM11 12a1 1 0 100 2h3a1 1 0 100-2h-3z"/>
          </svg>
        </div>
        <div>
          <h3 class="font-semibold text-foreground">{{ device.name || 'LCD Display' }}</h3>
          <p class="text-sm text-muted-foreground">16x2 Display</p>
        </div>
      </div>
      
    <!-- Toggle switch  -->
      <label class="relative inline-flex items-center cursor-pointer">
        <input type="checkbox" v-model="isOn" :disabled="!isAvailable" class="sr-only peer">
        <div class="w-11 h-6 bg-muted peer-focus:outline-none rounded-full peer peer-checked:bg-primary transition-colors duration-300 relative">
          <div class="absolute left-1 top-1 w-4 h-4 bg-background rounded-full shadow-sm transform transition-transform duration-300 peer-checked:translate-x-5"></div>
        </div>
      </label>
    </div>

    <!-- LCD Display Preview (always visible)  -->
    <div class="mb-3">
      <div class="border-2 rounded-lg p-3 font-mono text-sm transition-colors duration-300"
           :style="{ 
             backgroundColor: lcdBgColor, 
             borderColor: lcdBorderColor,
             opacity: isOn ? 1 : 0.5
           }">
        <div class="leading-tight tracking-wide" :style="{ color: lcdTextColor }">
          {{ firstLineText || '                ' }}
        </div>
        <div class="leading-tight tracking-wide" :style="{ color: lcdTextColor }">
          {{ secondLineText || '                ' }}
        </div>
      </div>
    </div>

    <!-- Status section  -->
    <div class="space-y-3">
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
        
        <!-- Connection indicator  -->
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
      
    <!-- Expand/collapse button  -->
      <button 
        @click="isExpanded = !isExpanded"
        class="w-full flex items-center justify-center gap-1 text-muted-foreground hover:text-foreground transition-colors py-2"
      >
        <span class="text-xs">{{ isExpanded ? 'Hide Controls' : 'Edit Text' }}</span>
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

    <!-- Expandable text editor section  -->
    <div 
      class="overflow-hidden transition-all duration-300"
      :style="{ maxHeight: isExpanded ? '600px' : '0' }"
    >
      <div class="pt-4 mt-4 border-t border-border space-y-4">

        <!-- Theme Selector  -->
        <div>
          <label class="block text-sm font-medium text-foreground mb-2">
            Display Theme
          </label>
          <select 
            v-model="displayTheme"
            :disabled="!isAvailable"
            class="w-full px-3 py-2 bg-secondary border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <option v-for="(theme, key) in themes" :key="key" :value="key">
              {{ theme.name }}
            </option>
          </select>
        </div>

        <!-- First Line Input  -->
        <div>
          <label class="block text-sm font-medium text-foreground mb-2">
        <!-- Line 1 (max 16 chars) -->
          </label>
          <input 
            type="text" 
            v-model="firstLineInput"
            maxlength="16"
            :disabled="!isAvailable"
            class="w-full px-3 py-2 bg-secondary border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed font-mono text-sm"
            placeholder="Enter text..."
          />
          <div class="flex items-center justify-between mt-1">
            <span v-if="firstLineError" class="text-xs text-destructive">{{ firstLineError }}</span>
            <span class="text-xs text-muted-foreground ml-auto">{{ firstLineInput.length }}/16</span>
          </div>
        </div>

        <!-- Second Line Input  -->
        <div>
          <label class="block text-sm font-medium text-foreground mb-2">
        <!-- Line 2 (max 16 chars) -->
          </label>
          <input 
            type="text" 
            v-model="secondLineInput"
            maxlength="16"
            :disabled="!isAvailable"
            class="w-full px-3 py-2 bg-secondary border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all disabled:opacity-50 disabled:cursor-not-allowed font-mono text-sm"
            placeholder="Enter text..."
          />
          <div class="flex items-center justify-between mt-1">
            <span v-if="secondLineError" class="text-xs text-destructive">{{ secondLineError }}</span>
            <span class="text-xs text-muted-foreground ml-auto">{{ secondLineInput.length }}/16</span>
          </div>
        </div>

        <!-- Update Button  -->
        <button
          @click="updateText"
          :disabled="!isAvailable || (firstLineInput === firstLineText && secondLineInput === secondLineText)"
          class="w-full bg-primary text-primary-foreground py-2 px-4 rounded-lg font-medium hover:opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
        Update Display
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
input:checked + div > div {
  transform: translateX(1.25rem);
}
</style>
