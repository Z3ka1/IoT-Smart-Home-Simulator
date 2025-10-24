<script setup>
import { ref, onMounted, watch } from 'vue'
import { truncateText, truncateDescription } from '@/utils/stringUtils'

const props = defineProps({ device: Object })

const isExpanded = ref(false)
const isAvailable = ref(true)

// Indoor sensor data
const temperature = ref(0)
const humidity = ref(0)
const lastMeasurement = ref('')

// Outdoor API data
const apiTemperature = ref(0)
const apiFeelsLike = ref(0)
const apiPressure = ref(0)
const apiHumidity = ref(0)
const apiWeatherDescription = ref('')
const city = ref('')

const displayDeviceName = truncateText(props.device.name, 17, 'Weather Station')
const displayDeviceDescription = truncateDescription(props.device.description, 17, 'Climate Monitor')

onMounted(() => {
  isAvailable.value = props.device.available
  updateData()
})

const updateData = () => {
  const props_data = props.device.properties || {}
  
  // Indoor data
  temperature.value = props_data.temperature || 0
  humidity.value = props_data.humidity || 0
  lastMeasurement.value = props_data.last_measurement || 'N/A'
  
  // Outdoor data
  apiTemperature.value = props_data.api_temperature || 0
  apiFeelsLike.value = props_data.api_feels_like || 0
  apiPressure.value = props_data.api_pressure || 0
  apiHumidity.value = props_data.api_humidity || 0
  apiWeatherDescription.value = props_data.api_weather_description || 'Clear'
  city.value = props_data.city || 'Unknown'
}

// Watch for prop changes
watch(() => props.device.properties, () => {
  updateData()
}, { deep: true })

watch(() => props.device.available, (newVal) => {
  isAvailable.value = newVal
})

const getWeatherIcon = (description) => {
  const iconMap = {
    'Clear': 'clear.png',
    'Clouds': 'clouds.png',
    'Rain': 'rain.png',
    'Drizzle': 'drizzle.png',
    'Thunderstorm': 'thunderstorm.png',
    'Snow': 'snow.png',
    'Mist': 'fog.png',
    'Smoke': 'fog.png',
    'Haze': 'fog.png',
    'Dust': 'fog.png',
    'Fog': 'fog.png',
    'Sand': 'fog.png',
    'Ash': 'fog.png',
    'Squall': 'tornado.png',
    'Tornado': 'tornado.png'
  }
  return `/weather-icons/${iconMap[description] || 'clear.png'}`
}
</script>


<template>
  <div class="bg-card border border-border rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-all duration-200"
       :class="{'opacity-50 grayscale': !isAvailable}">
    
    <!-- Header -->
    <div class="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 p-4 border-b border-border/50">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-blue-500/20 rounded-lg flex items-center justify-center backdrop-blur-sm">
            <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>
            </svg>
          </div>
          <div>
            <h3 class="font-semibold text-foreground" :title = "device.name">{{ displayDeviceName }}</h3>
            <p class="text-xs text-muted-foreground">{{ displayDeviceDescription }}</p>
          </div>
        </div>
        
        <!-- Connection status -->
        <div class="flex items-center gap-2 bg-background/50 backdrop-blur-sm px-3 py-1.5 rounded-full">
          <div :class="[
            'w-1.5 h-1.5 rounded-full',
            isAvailable ? 'bg-green-400' : 'bg-red-400'
          ]"></div>
          <span :class="[
            'text-xs font-medium',
            isAvailable ? 'text-green-400' : 'text-red-400'
          ]">{{ isAvailable ? 'Online' : 'Offline' }}</span>
        </div>
      </div>
    </div>

    <div class="p-4">
      <!-- Collapsed View indoor temperature display -->
      <div v-if="!isExpanded" class="space-y-3">
        <div class="bg-gradient-to-br from-secondary/50 to-secondary/30 rounded-lg p-4 border border-border/30">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                </svg>
              </div>
              <span class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Indoor</span>
            </div>
            <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
              <span>{{ lastMeasurement }}</span>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <div class="flex items-baseline gap-1">
                <span class="text-4xl font-bold text-foreground">{{ temperature.toFixed(1) }}</span>
                <span class="text-2xl text-muted-foreground font-light">°C</span>
              </div>
              <div class="flex items-center gap-2 mt-2">
                <svg class="w-4 h-4 text-cyan-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M5.5 16a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 16h-8z"/>
                </svg>
                <span class="text-sm text-muted-foreground">{{ humidity }}% humidity</span>
              </div>
            </div>
            
            <div class="w-16 h-16 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-full flex items-center justify-center">
              <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
          </div>
        </div>

        <button 
          @click="isExpanded = true"
          class="w-full py-2.5 px-4 bg-secondary/80 hover:bg-secondary text-secondary-foreground rounded-lg text-sm font-medium transition-all duration-200 flex items-center justify-center gap-2 group">
          
          <span>Show Outdoor Weather</span>
          <svg class="w-4 h-4 group-hover:translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
      </div>

      <!-- Expanded View: full weather data display -->
      <div v-else class="space-y-3">
        <!-- Indoor Section -->
        <div class="bg-gradient-to-br from-secondary/50 to-secondary/30 rounded-lg p-4 border border-border/30">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-blue-500/20 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
                </svg>
              </div>
              <span class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Indoor</span>
            </div>
            <div class="flex items-center gap-1.5 text-xs text-muted-foreground">
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
              <span>{{ lastMeasurement }}</span>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <div class="flex items-baseline gap-1">
                <span class="text-4xl font-bold text-foreground">{{ temperature.toFixed(1) }}</span>
                <span class="text-2xl text-muted-foreground font-light">°C</span>
              </div>
              <div class="flex items-center gap-2 mt-2">
                <svg class="w-4 h-4 text-cyan-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M5.5 16a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 16h-8z"/>
                </svg>
                <span class="text-sm text-muted-foreground">{{ humidity }}% humidity</span>
              </div>
            </div>
            
            <div class="w-16 h-16 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 rounded-full flex items-center justify-center">
              <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Outdoor Section -->
        <div class="bg-gradient-to-br from-blue-500/10 to-cyan-500/10 rounded-lg p-4 border border-blue-500/20">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div class="w-7 h-7 bg-blue-500/30 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <span class="text-xs font-semibold text-foreground uppercase tracking-wider">Outdoor</span>
                <div class="text-xs text-muted-foreground">{{ city }}</div>
              </div>
            </div>
            
            <!-- weather icon -->
            <img :src="getWeatherIcon(apiWeatherDescription)" 
                 :alt="apiWeatherDescription"
                 class="w-12 h-12 object-contain drop-shadow-lg" />
          </div>
          
          <div class="mb-3">
            <div class="text-xs text-blue-400 font-medium mb-1">{{ apiWeatherDescription }}</div>
            <div class="flex items-baseline gap-2 mb-2">
              <span class="text-4xl font-bold text-foreground">{{ apiTemperature.toFixed(1) }}</span>
              <span class="text-xl text-muted-foreground font-light">°C</span>
            </div>
            <div class="text-sm text-muted-foreground flex items-center gap-1">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"/>
              </svg>
              Feels like {{ apiFeelsLike.toFixed(1) }}°C
            </div>
          </div>
          
          <div class="grid grid-cols-2 gap-2">
            <div class="bg-background/40 backdrop-blur-sm rounded-lg p-2.5">
              <div class="text-xs text-muted-foreground mb-1 flex items-center gap-1">
                <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M5.5 16a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.977A4.5 4.5 0 1113.5 16h-8z"/>
                </svg>
                Humidity
              </div>
              <div class="flex items-baseline gap-1">
                <span class="text-lg font-bold text-foreground">{{ apiHumidity }}</span>
                <span class="text-xs text-muted-foreground">%</span>
              </div>
            </div>
            <div class="bg-background/40 backdrop-blur-sm rounded-lg p-2.5">
              <div class="text-xs text-muted-foreground mb-1 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                </svg>
                Pressure
              </div>
              <div class="flex items-baseline gap-1">
                <span class="text-lg font-bold text-foreground">{{ apiPressure }}</span>
                <span class="text-xs text-muted-foreground">hPa</span>
              </div>
            </div>
          </div>
        </div>

        <button 
          @click="isExpanded = false"
          class="w-full py-2.5 px-4 bg-secondary/80 hover:bg-secondary text-secondary-foreground rounded-lg text-sm font-medium transition-all duration-200 flex items-center justify-center gap-2 group">
          <span>Show Less</span>
          <svg class="w-4 h-4 group-hover:-translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
