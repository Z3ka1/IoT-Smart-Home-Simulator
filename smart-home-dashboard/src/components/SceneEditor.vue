<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useDeviceStore } from '@/stores/deviceStore'
import { useRoomStore } from '@/stores/roomStore'
import PopupWindow from '@/components/PopupWindow.vue'

const deviceStore = useDeviceStore()
const roomStore = useRoomStore()

const props = defineProps({
  scene: Object,  // If editing existing scene
  roomId: Number  // Current room filter
})

const emit = defineEmits(['save', 'cancel'])

const sceneName = ref(props.scene?.name || '')
const sceneDescription = ref(props.scene?.description || '')
const selectedRoomId = ref(props.roomId || props.scene?.roomId || null)
const deviceConfigurations = ref(props.scene?.deviceConfigurations || {})

const errorPopup = ref(false)
const errorMessage = ref('')

// Get devices for selected room or all devices
const availableDevices = computed(() => {
  if (selectedRoomId.value) {
    return deviceStore.devices.filter(d => d.roomId === selectedRoomId.value)
  }
  return deviceStore.devices
})

const isDeviceIncluded = (deviceId) => {
  return deviceConfigurations.value.hasOwnProperty(deviceId.toString())
}

// Toggle device inclusion in scene
const toggleDevice = (device) => {
  const deviceIdStr = device.id.toString()
  if (isDeviceIncluded(device.id)) {
    delete deviceConfigurations.value[deviceIdStr]
  } else {
    // Add device with current properties
    deviceConfigurations.value[deviceIdStr] = { ...device.properties }
  }
}

const updateDeviceProperty = (deviceId, property, value) => {
  const deviceIdStr = deviceId.toString()
  if (!deviceConfigurations.value[deviceIdStr]) {
    deviceConfigurations.value[deviceIdStr] = {}
  }
  deviceConfigurations.value[deviceIdStr][property] = value
}

const getDeviceConfig = (deviceId) => {
  return deviceConfigurations.value[deviceId.toString()] || {}
}

const getRoomName = (roomId) => {
  const room = roomStore.rooms.find(r => r.id === roomId)
  return room?.name || 'Unknown Room'
}

const handleSave = () => {
  if (!sceneName.value.trim()) {
    errorMessage.value = 'Please enter a scene name!'
    errorPopup.value = true
    return
  }

  if (Object.keys(deviceConfigurations.value).length === 0) {
    errorMessage.value = 'Please select at least one device for the scene'
    errorPopup.value = true
    return
  }

  emit('save', {
    name: sceneName.value,
    description: sceneDescription.value,
    roomId: selectedRoomId.value,
    deviceConfigurations: deviceConfigurations.value
  })
}

onMounted(() => {
  deviceStore.fetchDevices()
  roomStore.fetchRooms()
})

onUnmounted(() => {
    deviceStore.fetchDevices()
})

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
</script>

<template>
  <div class="space-y-6">
    <div>
      <h3 class="text-xl font-semibold text-foreground mb-2">
        {{ scene ? 'Edit Scene' : 'Create New Scene' }}
      </h3>
      <p class="text-sm text-muted-foreground">Configure device states for this scene</p>
    </div>

    <!-- Scene Name & Description -->
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-foreground mb-2">Scene Name</label>
        <input
          v-model="sceneName"
          type="text"
          placeholder="e.g., Movie Night, Good Morning"
          class="w-full bg-background border border-border rounded-lg px-4 py-3 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-foreground mb-2">Description (Optional)</label>
        <input
          v-model="sceneDescription"
          type="text"
          placeholder="Describe what this scene does"
          class="w-full bg-background border border-border rounded-lg px-4 py-3 text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        />
      </div>

      <!-- Room Filter -->
      <div>
        <label class="block text-sm font-medium text-foreground mb-2">Room (Optional)</label>
        <select
          v-model="selectedRoomId"
          class="w-full bg-background border border-border rounded-lg px-4 py-3 text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        >
          <option :value="null">All Rooms</option>
          <option v-for="room in roomStore.rooms" :key="room.id" :value="room.id">
            {{ room.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Device Selection -->
    <div>
      <h4 class="text-sm font-medium text-foreground mb-3">Select Devices & Configure States</h4>
      <div class="space-y-3 max-h-96 overflow-y-auto">
        <div
          v-for="device in availableDevices"
          :key="device.id"
          class="bg-card border border-border rounded-lg p-4 hover:border-primary/50 transition-colors"
        >
          <div class="flex items-start gap-3">
            <!-- Checkbox to include device -->
            <input
              type="checkbox"
              :checked="isDeviceIncluded(device.id)"
              @change="toggleDevice(device)"
              class="mt-1 w-4 h-4 text-primary bg-background border-border rounded focus:ring-2 focus:ring-primary"
            />

            <div class="flex-1">
                <div class="flex items-center justify-between mb-2">
                    <div>
                        <h5 class="font-medium text-foreground">{{ device.name }}</h5>
                        <p class="text-xs text-muted-foreground">{{ device.type }} • {{ getRoomName(device.roomId) }}</p>
                    </div>
                </div>

              <!-- Device-specific controls (only shown if device is included) -->
              <div v-if="isDeviceIncluded(device.id)" class="mt-3 space-y-2 pl-2 border-l-2 border-primary/30">
                <!-- SimpleLED controls -->
                <div v-if="device.type.toLowerCase() === 'simpleled'" class="space-y-2">
                  <label class="block text-sm font-medium text-foreground">Power State</label>
                  <div class="flex flex-col gap-1 ml-2">
                    <label class="flex items-center gap-2">
                      <input
                        type="radio"
                        :name="'simpleled-' + device.id"
                        value="on"
                        :checked="getDeviceConfig(device.id).state === 'on'"
                        @change="updateDeviceProperty(device.id, 'state', 'on')"
                        class="text-primary bg-background border-border"
                      />
                      <span class="text-sm text-foreground">Turn On</span>
                    </label>
 
                    <label class="flex items-center gap-2">
                      <input
                        type="radio"
                        :name="'simpleled-' + device.id"
                        value="off"
                        :checked="getDeviceConfig(device.id).state === 'off'"
                        @change="updateDeviceProperty(device.id, 'state', 'off')"
                        class="text-primary bg-background border-border"
                      />
                      <span class="text-sm text-foreground">Turn Off</span>
                    </label>
                  </div>
                </div>
 
                <!-- RGB Strip controls -->
                <div v-if="device.type.toLowerCase() === 'rgbstrip'" class="space-y-2">
                    <label class="block text-sm font-medium text-foreground">Power State</label>
                    <div class="flex flex-col gap-1 ml-2">
                        <label class="flex items-center gap-2">
                        <input
                            type="radio"
                            :name="'rgbstrip-' + device.id"
                            value="on"
                            :checked="getDeviceConfig(device.id).state === 'on'"
                            @change="updateDeviceProperty(device.id, 'state', 'on')"
                            class="text-primary bg-background border-border"
                        />
                        <span class="text-sm text-foreground">Turn On</span>
                        </label>
    
                        <label class="flex items-center gap-2">
                        <input
                            type="radio"
                            :name="'rgbstrip-' + device.id"
                            value="off"
                            :checked="getDeviceConfig(device.id).state === 'off'"
                            @change="updateDeviceProperty(device.id, 'state', 'off')"
                            class="text-primary bg-background border-border"
                        />
                        <span class="text-sm text-foreground">Turn Off</span>
                        </label>
                    </div>
 
                    <!-- RGB Sliders -->
                    <div class="space-y-2">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <label class="text-sm font-medium text-foreground">Red</label>
                                <span class="text-sm text-muted-foreground">
                                {{ getDeviceConfig(device.id).red ?? 255 }}
                                </span>
                            </div>
                            <input
                                type="range"
                                :value="getDeviceConfig(device.id).red ?? 255"
                                min="0"
                                max="255"
                                @input="updateDeviceProperty(device.id, 'red', parseInt($event.target.value))"
                                class="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer slider-red"
                            />
                        </div>
    
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <label class="text-sm font-medium text-foreground">Green</label>
                                <span class="text-sm text-muted-foreground">
                                {{ getDeviceConfig(device.id).green ?? 255 }}
                                </span>
                            </div>
                            <input
                                type="range"
                                :value="getDeviceConfig(device.id).green ?? 255"
                                min="0"
                                max="255"
                                @input="updateDeviceProperty(device.id, 'green', parseInt($event.target.value))"
                                class="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer slider-green"
                            />
                        </div>

                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <label class="text-sm font-medium text-foreground">Blue</label>
                                <span class="text-sm text-muted-foreground">
                                {{ getDeviceConfig(device.id).blue ?? 255 }}
                                </span>
                            </div>
                            <input
                                type="range"
                                :value="getDeviceConfig(device.id).blue ?? 255"
                                min="0"
                                max="255"
                                @input="updateDeviceProperty(device.id, 'blue', parseInt($event.target.value))"
                                class="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer slider-blue"
                            />
                        </div>
                    </div>
                    
                    <!-- Brightness -->
                    <div class="space-y-2">
                        <div class="flex items-center justify-between">
                        <label class="text-sm font-medium text-foreground">Brightness</label>
                        <span class="text-sm text-muted-foreground">
                            {{ getDeviceConfig(device.id).brightness ?? 100 }}%
                        </span>
                        </div>

                        <input
                        type="range"
                        :value="getDeviceConfig(device.id).brightness ?? 100"
                        min="0"
                        max="100"
                        @input="updateDeviceProperty(device.id, 'brightness', parseInt($event.target.value))"
                        class="w-full h-2 bg-muted rounded-lg appearance-none cursor-pointer slider-brightness"
                        />
                    </div>
                  
                </div>

                <!-- LCD Display controls -->
                <div v-if="device.type.toLowerCase() === 'lcddisplay'" class="space-y-4">
                    <!-- Power State -->
                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-foreground">Power State</label>
                        <div class="flex flex-col gap-1 ml-2">
                        <label class="flex items-center gap-2">
                            <input
                            type="radio"
                            :name="'lcddisplay-' + device.id"
                            value="on"
                            :checked="getDeviceConfig(device.id).state === 'on'"
                            @change="updateDeviceProperty(device.id, 'state', 'on')"
                            class="text-primary bg-background border-border"
                            />
                            <span class="text-sm text-foreground">Turn On</span>
                        </label>
                        <label class="flex items-center gap-2">
                            <input
                            type="radio"
                            :name="'lcddisplay-' + device.id"
                            value="off"
                            :checked="getDeviceConfig(device.id).state === 'off'"
                            @change="updateDeviceProperty(device.id, 'state', 'off')"
                            class="text-primary bg-background border-border"
                            />
                            <span class="text-sm text-foreground">Turn Off</span>
                        </label>
                        </div>
                    </div>

                    <!-- Theme Selector -->
                    <div>
                        <label class="block text-sm font-medium text-foreground mb-2">Display Theme</label>
                        <select 
                        :value="getDeviceConfig(device.id).display_theme || 'purple-haze'"
                        @change="updateDeviceProperty(device.id, 'display_theme', $event.target.value)"
                        class="w-full px-3 py-2 bg-secondary border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                        >
                            <option v-for="(theme, key) in themes" :key="key" :value="key">
                                {{ theme.name }}
                            </option>
                        </select>
                    </div>

                    <!-- First Line Input -->
                    <div>
                        <label class="block text-sm font-medium text-foreground mb-2">First Line Text</label>
                        <input 
                        type="text" 
                        :value="getDeviceConfig(device.id).first_line_text || ''"
                        @input="updateDeviceProperty(device.id, 'first_line_text', $event.target.value)"
                        maxlength="16"
                        class="w-full px-3 py-2 bg-secondary border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all font-mono text-sm"
                        placeholder="Enter first line text..."
                        />
                        <div class="flex items-center justify-between mt-1">
                            <span class="text-xs text-muted-foreground ml-auto">
                                {{ (getDeviceConfig(device.id).first_line_text || '').length }}/16
                            </span>
                        </div>
                    </div>

                    <!-- Second Line Input -->
                    <div>
                        <label class="block text-sm font-medium text-foreground mb-2">Second Line Text</label>
                        <input 
                        type="text" 
                        :value="getDeviceConfig(device.id).second_line_text || ''"
                        @input="updateDeviceProperty(device.id, 'second_line_text', $event.target.value)"
                        maxlength="16"
                        class="w-full px-3 py-2 bg-secondary border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all font-mono text-sm"
                        placeholder="Enter second line text..."
                        />
                        <div class="flex items-center justify-between mt-1">
                            <span class="text-xs text-muted-foreground ml-auto">
                                {{ (getDeviceConfig(device.id).second_line_text || '').length }}/16
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Alarm Sensor controls -->
                <div v-if="device.type.toLowerCase() === 'alarmsensor'" class="space-y-4">
                    <!-- is_alarm_enabled -->
                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-foreground">Enable Alarm?</label>
                        <div class="flex flex-col gap-1 ml-2">
                            <label class="flex items-center gap-2">
                                <input
                                type="radio"
                                :name="'alarmsensor-' + device.id"
                                value="true"
                                :checked="getDeviceConfig(device.id).is_alarm_enabled === true"
                                @change="updateDeviceProperty(device.id, 'is_alarm_enabled', true)"
                                class="text-primary bg-background border-border"
                                />
                                <span class="text-sm text-foreground">Yes</span>
                            </label>
                            <label class="flex items-center gap-2">
                                <input
                                type="radio"
                                :name="'alarmsensor-' + device.id"
                                value="false"
                                :checked="getDeviceConfig(device.id).is_alarm_enabled === false"
                                @change="updateDeviceProperty(device.id, 'is_alarm_enabled', false)"
                                class="text-primary bg-background border-border"
                                />
                                <span class="text-sm text-foreground">No</span>
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Other devices -->
                <div v-if="!['simpleled', 'rgbstrip', 'lcddisplay', 'alarmsensor'].includes(device.type.toLowerCase())" class="space-y-2">
                  <label class="flex items-center gap-2">
                    <span class="text-sm text-foreground">Scenes not supported for this device.</span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="availableDevices.length === 0" class="text-center py-8 text-muted-foreground">
          No devices available. Add devices first.
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-end gap-3 pt-4 border-t border-border">
      <button
        @click="$emit('cancel')"
        class="px-4 py-2 text-muted-foreground hover:text-foreground transition-colors"
      >
        Cancel
      </button>
      <button
        @click="handleSave"
        class="bg-primary text-primary-foreground px-6 py-2 rounded-lg font-medium hover:bg-primary/90 transition-colors"
      >
        {{ scene ? 'Update Scene' : 'Create Scene' }}
      </button>
    </div>

    <!-- Error Popup -->
    <PopupWindow v-if="errorPopup" @closePopup="errorPopup = false">
      <div class="space-y-4">
        <h3 class="text-lg font-semibold text-destructive">Error</h3>
        <p class="text-muted-foreground">{{ errorMessage }}</p>
 
        <div class="flex justify-end">
          <button
            @click="errorPopup = false"
            class="bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors"
          >
            OK
          </button>
        </div>
      </div>
    </PopupWindow>

  </div>
</template>

<style scoped>
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
</style>