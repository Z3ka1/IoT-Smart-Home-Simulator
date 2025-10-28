import { defineStore } from "pinia"
import { ref } from "vue"
import axios from "../utils/axios"

export const useSceneStore = defineStore("scene", () => {
  const scenes = ref([])
  const isLoading = ref(false)

  const fetchScenes = async () => {
    try {
      isLoading.value = true
      const res = await axios.get("/scenes")
      scenes.value = res.data
      console.log("Scenes fetched:", scenes.value)
    } catch (error) {
      console.error("Failed to fetch scenes:", error)
    } finally {
      isLoading.value = false
    }
  }

  const createScene = async (sceneData) => {
    try {
      const res = await axios.post("/scenes", sceneData)
      scenes.value.push(res.data)
      return res.data
    } catch (error) {
      console.error("Failed to create scene:", error)
      throw error
    }
  }

  const updateScene = async (sceneId, sceneData) => {
    try {
      const res = await axios.put(`/scenes/${sceneId}`, sceneData)
      const index = scenes.value.findIndex((s) => s.id === sceneId)
      if (index !== -1) {
        scenes.value[index] = res.data
      }
      return res.data
    } catch (error) {
      console.error("Failed to update scene:", error)
      throw error
    }
  }

  const deleteScene = async (sceneId) => {
    try {
      await axios.delete(`/scenes/${sceneId}`)
      scenes.value = scenes.value.filter((s) => s.id !== sceneId)
    } catch (error) {
      console.error("Failed to delete scene:", error)
      throw error
    }
  }

  const activateScene = async (sceneId) => {
    try {
      const res = await axios.post(`/scenes/${sceneId}/activate`)
      console.log("Scene activated:", res.data)
      return res.data
    } catch (error) {
      console.error("Failed to activate scene:", error)
      throw error
    }
  }

  return {
    scenes,
    isLoading,
    fetchScenes,
    createScene,
    updateScene,
    deleteScene,
    activateScene,
  }
})
