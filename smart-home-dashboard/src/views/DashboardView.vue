<script setup>
import { onMounted, computed, ref, watch, onUnmounted } from 'vue'
import { useDeviceStore } from '@/stores/deviceStore'
import GenericDeviceWidget from '@/components/devices/GenericDeviceWidget.vue'
import DashboardNavbar from '@/components/DashboardNavbar.vue'
import { deviceWidgetMap } from '@/utils/deviceWidgetMap'
import socket from '@/services/websocket'
import { useRoomStore } from '@/stores/roomStore'

import { useSceneStore } from '@/stores/sceneStore'
import PopupWindow from '@/components/PopupWindow.vue'
import SceneEditor from '@/components/SceneEditor.vue'

const sceneStore = useSceneStore()
const showSceneList = ref(false)
const showSceneEditor = ref(false)
const editingScene = ref(null)

const selectedRoomId = ref(null)
const deviceStore = useDeviceStore();
const { fetchDevices } = useDeviceStore();
const roomStore = useRoomStore()

const noRooms = computed (() => roomStore.rooms.length === 0)

const errorPopup = ref(false)
const errorMessage = ref('')
const confirmDeletePopup = ref(false)
const selectedScene = ref(null)

const socketHandlers = {
  device_status: null,
  motion_detected: null,
  weather_station_measurements: null,
  simpleled_state: null,
  lcddisplay_state: null,
  lcddisplay_text: null,
  lcddisplay_theme: null,
  rgbstrip_state: null,
  rgbstrip_color: null,
  rgbstrip_brightness: null,
  alarmsensor_enabled: null,
  test_pong: null
}

const handleSocketUpdate = (data) => {
  console.log('[INFO] Received device_status:', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) device.available = data.available
}

const handleMotionDetectedUpdate = (data) => {
  console.log('[INFO] Redceived motion_detected:', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if(device.type.toLowerCase() === 'alarmsensor' || Object.prototype.hasOwnProperty.call(device.properties, 'motion_detected')) {
      device.properties.motion_detected = data.motion_detected
    }
  }
}

const handleWeatherStationMeasurementsUpdate = (data) => {
  console.log('[INFO] Received weather station measurements:', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if (device.type.toLowerCase() === 'weatherstation' || (Object.prototype.hasOwnProperty.call(device.properties, 'temperature') 
      && Object.prototype.hasOwnProperty.call(device.properties, 'humidity'))) {
        device.properties.temperature = data.temperature
        device.properties.humidity = data.humidity
        device.properties.city = data.city
        device.properties.api_temperature = data.api_temperature
        device.properties.api_weather_description = data.api_weather_description
        device.properties.api_feels_like = data.api_feels_like
        device.properties.api_pressure = data.api_pressure
        device.properties.api_humidity = data.api_humidity
        device.properties.last_measurement = data.last_measurement
    }
  }
}

const handleSimpleLedStateUpdate = (data) => {
  console.log('[INFO] Received simpleled state: ', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if(device.type.toLowerCase() === 'simpleled' || (Object.prototype.hasOwnProperty.call(device.properties, 'state'))) {
      device.properties.state = data.state
    }
  }
}

const handleLcdDisplayStateUpdate = (data) => {
  console.log('[INFO] Received lcddisplay state: ', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if(device.type.toLowerCase() === 'lcddisplay' || (Object.prototype.hasOwnProperty.call(device.properties, 'state')
      && Object.prototype.hasOwnProperty.call(device.properties, 'second_line_text'))) {
      device.properties.state = data.state
    }
  }
}

const handleLcdDisplayTextUpdate = (data) => {
  console.log('[INFO] Received lcddisplay text: ', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if(device.type.toLowerCase() === 'lcddisplay' || (Object.prototype.hasOwnProperty.call(device.properties, 'first_line_text')
      && Object.prototype.hasOwnProperty.call(device.properties, 'second_line_text'))) {
      device.properties.first_line_text = data.first_line_text
      device.properties.second_line_text = data.second_line_text
    }
  }
}

const handleLcdDisplayThemeUpdate = (data) => {
  console.log('[INFO] Received lcddisplay theme: ', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if(device.type.toLowerCase() === 'lcddisplay' || (Object.prototype.hasOwnProperty.call(device.properties, 'display_theme'))) {
      device.properties.display_theme = data.display_theme
    }
  }
}

const handleRgbStripStateUpdate = (data) => {
  console.log('[INFO] Received rgbstrip state: ', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if (device.type.toLowerCase() === 'rgbstrip' || (Object.prototype.hasOwnProperty.call(device.propertis, 'state'))) {
      device.properties.state = data.state
    }
  }
}

const handleRgbStripColorUpdate = (data) => {
  console.log('[INFO] Received rgbstrip color: ', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if (device.type.toLowerCase() === 'rgbstrip' || (Object.prototype.hasOwnProperty.call(device.propertis, 'red')
      && Object.prototype.hasOwnProperty.call(device.properties, 'green') && Object.prototype.hasOwnProperty.call(device.properties, 'blue'))) {
      device.properties.red = data.red
      device.properties.green = data.green
      device.properties.blue = data.blue
    }
  }
}

const handleRgbStripBrightnessUpdate = (data) => {
  console.log('[INFO] Received rgbstrip brightness: ', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if (device.type.toLowerCase() === 'rgbstrip' || (Object.prototype.hasOwnProperty.call(device.propertis, 'brightness'))) {
      device.properties.brightness = data.brightness
    }
  }
}

const handleAlarmSensorEnabledUpdate = (data) => {
  console.log('[INFO] Received alarmsensor is_enabled: ', data)
  const device = deviceStore.devices.find(d => d.id === data.id)
  if (device) {
    if (device.type.toLowerCase() === 'alarmsensor' || (Object.prototype.hasOwnProperty.call(device.properties, 'is_alarm_enabled'))) {
      device.properties.is_alarm_enabled = data.is_alarm_enabled
    }
  }
}

onMounted(() => {
  fetchDevices();
  sceneStore.fetchScenes();
  
  socketHandlers.device_status = handleSocketUpdate
  socketHandlers.motion_detected = handleMotionDetectedUpdate
  socketHandlers.weather_station_measurements = handleWeatherStationMeasurementsUpdate
  socketHandlers.simpleled_state = handleSimpleLedStateUpdate
  socketHandlers.lcddisplay_state = handleLcdDisplayStateUpdate
  socketHandlers.lcddisplay_text = handleLcdDisplayTextUpdate
  socketHandlers.lcddisplay_theme = handleLcdDisplayThemeUpdate
  socketHandlers.rgbstrip_state = handleRgbStripStateUpdate
  socketHandlers.rgbstrip_color = handleRgbStripColorUpdate
  socketHandlers.rgbstrip_brightness = handleRgbStripBrightnessUpdate
  socketHandlers.alarmsensor_enabled = handleAlarmSensorEnabledUpdate

  socket.on('device_status', socketHandlers.device_status)
  socket.on('motion_detected', socketHandlers.motion_detected)
  socket.on('weather_station_measurements', socketHandlers.weather_station_measurements)
  socket.on('simpleled_state', socketHandlers.simpleled_state)
  socket.on('lcddisplay_state', socketHandlers.lcddisplay_state)
  socket.on('lcddisplay_text', socketHandlers.lcddisplay_text)
  socket.on('lcddisplay_theme', socketHandlers.lcddisplay_theme)
  socket.on('rgbstrip_state', socketHandlers.rgbstrip_state)
  socket.on('rgbstrip_color', socketHandlers.rgbstrip_color)
  socket.on('rgbstrip_brightness', socketHandlers.rgbstrip_brightness)
  socket.on('alarmsensor_enabled', socketHandlers.alarmsensor_enabled)

  socket.on('connect_error', (err) => {
    console.error("[ERROR] Connection error:", err)
  })
});

onUnmounted(() => {
  if (socketHandlers.device_status) socket.off('device_status', socketHandlers.device_status)
  if (socketHandlers.motion_detected) socket.off('motion_detected', socketHandlers.motion_detected)
  if (socketHandlers.weather_station_measurements) socket.off('weather_station_measurements', socketHandlers.weather_station_measurements)
  if (socketHandlers.simpleled_state) socket.off('simpleled_state', socketHandlers.simpleled_state)
  if (socketHandlers.lcddisplay_state) socket.off('lcddisplay_state', socketHandlers.lcddisplay_state)
  if (socketHandlers.lcddisplay_text) socket.off('lcddisplay_text', socketHandlers.lcddisplay_text)
  if (socketHandlers.lcddisplay_theme) socket.off('lcddisplay_theme', socketHandlers.lcddisplay_theme)
  if (socketHandlers.rgbstrip_state) socket.off('rgbstrip_state', socketHandlers.rgbstrip_state)
  if (socketHandlers.rgbstrip_color) socket.off('rgbstrip_color', socketHandlers.rgbstrip_color)
  if (socketHandlers.rgbstrip_brightness) socket.off('rgbstrip_brightness', socketHandlers.rgbstrip_brightness)
  if (socketHandlers.alarmsensor_enabled) socket.off('alarmsensor_enabled', socketHandlers.alarmsensor_enabled)

  console.log('[INFO] Cleaned up all socket listeners')
});

const handleRoomSelected = (roomId) => {
  selectedRoomId.value = roomId;
};
 
const devicesInSelectedRoom = computed(() => {
  return deviceStore.devices.filter(d => d.roomId === selectedRoomId.value)
});

watch(selectedRoomId, (newValue, oldValue) => {
  console.log('[INFO] selected room ID:', newValue);
})

watch(selectedRoomId, () => {
  if (deviceStore.devices.length > 0) {
    console.log('[INFO] Devices In selected room: ',devicesInSelectedRoom.value);
  } else {
    console.log('[INFO] Devices not yet fetched');
  }
});

//Scenes
const scenesInSelectedRoom = computed(() => {
  if (!selectedRoomId.value) return sceneStore.scenes
  return sceneStore.scenes.filter(s => !s.roomId || s.roomId === selectedRoomId.value)
})

const openSceneEditor = (scene = null) => {
  editingScene.value = scene
  showSceneEditor.value = true
  showSceneList.value = false
}

const handleSaveScene = async (sceneData) => {
  try {
    if (editingScene.value) {
      await sceneStore.updateScene(editingScene.value.id, sceneData)
    } else {
      await sceneStore.createScene(sceneData)
    }
    showSceneEditor.value = false
    editingScene.value = null
  } catch (error) {
    errorMessage.value = 'Failed to save scene: ' + error.message
    errorPopup.value = true
  }
}

const openDeleteConfirm = (scene) => {
  selectedScene.value = scene
  confirmDeletePopup.value = true
}

const closeDeleteConfirm = () => {
  confirmDeletePopup.value = false
  selectedScene.value = null
}

const handleDeleteScene = async () => {
  if (!selectedScene.value) return 
  try {
    await sceneStore.deleteScene(selectedScene.value.id)
    closeDeleteConfirm()
  } catch (error) {
    errorMessage.value = 'Failed to delete scene: ' + error.message
    errorPopup.value = true
    closeDeleteConfirm()
  }
  
}

const handleActivateScene = async (sceneId) => {
  try {
    await sceneStore.activateScene(sceneId)
    showSceneList.value = false
  } catch (error) {
    errorMessage.value = 'Failed to activate scene: ' + error.message
    errorPopup.value = true
  }
  finally {
    deviceStore.fetchDevices()
  }
}

</script>

<template>
  <div class="max-w-7xl mx-auto">
    <!-- Dynamic Navbar -->
    <DashboardNavbar :selectedRoom="selectedRoomId" @room-selected="handleRoomSelected($event)"/>

    <div v-if="selectedRoomId" class="mb-6 flex items-center gap-3">
      <button
        @click="showSceneList = !showSceneList"
        class="flex items-center gap-2 bg-card border border-border hover:border-primary/50 text-foreground px-4 py-2 rounded-lg transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
        </svg>
        Scenes
        <span class="text-xs bg-primary/20 text-primary px-2 py-0.5 rounded-full">{{ scenesInSelectedRoom.length }}</span>
      </button>

      <button
        @click="openSceneEditor()"
        class="flex items-center gap-2 bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
        </svg>
        New Scene
      </button>
    </div>

    <div v-if="showSceneList && selectedRoomId" class="mb-6 bg-card border border-border rounded-xl p-4 shadow-lg">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-semibold text-foreground">Available Scenes</h3>
        <button @click="showSceneList = false" class="text-muted-foreground hover:text-foreground">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
          </svg>
        </button>
      </div>

      <div v-if="scenesInSelectedRoom.length === 0" class="text-center py-8 text-muted-foreground">
        <p>No scenes created yet</p>
        <button @click="openSceneEditor()" class="text-primary hover:underline mt-2">Create your first scene</button>
      </div>

      <div v-else class="space-y-2">
        <div
          v-for="scene in scenesInSelectedRoom"
          :key="scene.id"
          class="flex items-center justify-between p-3 bg-background rounded-lg hover:bg-muted/50 transition-colors group"
        >
          <div class="flex-1">
            <h4 class="font-medium text-foreground">{{ scene.name }}</h4>
            <p v-if="scene.description" class="text-sm text-muted-foreground">{{ scene.description }}</p>
            <p class="text-xs text-muted-foreground mt-1">
              {{ Object.keys(scene.deviceConfigurations || {}).length }} device(s)
            </p>
          </div>

          <div class="flex items-center gap-2">
            <button
              @click="handleActivateScene(scene.id)"
              class="bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors text-sm"
            >
              Activate
            </button>
            <button
              @click="openSceneEditor(scene)"
              class="p-2 text-muted-foreground hover:text-foreground transition-colors"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
              </svg>
            </button>
            <button
              @click="openDeleteConfirm(scene)"
              class="p-2 text-destructive hover:text-destructive/80 transition-colors"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Device Widgets -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 items-start">
      <component
        v-for="device in devicesInSelectedRoom"
        :key="device.id"
        :is="(deviceWidgetMap[device.type.toLowerCase()] || GenericDeviceWidget)"
        :device="device"
      />
    </div>
    
    <!-- Empty state when no devices -->
    <div v-if="devicesInSelectedRoom.length === 0 && selectedRoomId" class="text-center py-12">
      <div class="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-10 h-10 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-foreground mb-2">No devices found</h3>
      <p class="text-muted-foreground">This room doesn't have any devices yet.</p>
    </div>
 
    <!-- Empty state when no rooms exist -->
    <div v-if="noRooms" class="text-center py-20">
      <div class="w-20 h-20 bg-muted rounded-full flex items-center justify-center mx-auto mb-6">
        <svg class="w-10 h-10 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
      <h3 class="text-xl font-semibold text-foreground mb-2">No rooms found</h3>
      <p class="text-muted-foreground mb-6">
        You haven't created any rooms yet. Add a room to start managing your smart devices.
      </p>
      <RouterLink
        to="/rooms"
        class="bg-primary text-primary-foreground px-6 py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors inline-flex items-center gap-2"
      >
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
        </svg>
        Add Room
      </RouterLink>
    </div>

    <PopupWindow v-if="showSceneEditor" @closePopup="showSceneEditor = false; editingScene = null">
      <SceneEditor
        :scene="editingScene"
        :roomId="selectedRoomId"
        @save="handleSaveScene"
        @cancel="showSceneEditor = false; editingScene = null"
      />
    </PopupWindow>

    <!-- Confirm Delete Popup -->
    <PopupWindow @closePopup="closeDeleteConfirm" v-if="confirmDeletePopup">
      <div class="space-y-6">
        <h3 class="text-lg font-semibold text-foreground">
          Delete Scene "{{ selectedScene?.name }}"?
        </h3>
        <p class="text-muted-foreground text-sm">
          This action will permanently delete the scene and all related configurations.
        </p>
        <p class="text-sm text-muted-foreground italic">This action cannot be undone.</p>
 
        <div class="flex justify-end space-x-3">
          <button @click="closeDeleteConfirm" class="px-4 py-2 text-muted-foreground hover:text-foreground transition-colors">
            Cancel
          </button>
          <button
            @click="handleDeleteScene"
            class="bg-destructive text-destructive-foreground px-6 py-2 rounded-lg font-medium hover:bg-destructive/90 transition-colors"
          >
            Delete Scene
          </button>
        </div>
      </div>
    </PopupWindow>

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