import axios from "axios"
import router from "@/router"

// Axios instance with base config
const axiosInstance = axios.create({
  baseURL: "http://localhost:8000/api",
})

// Request interceptor to add JWT token to all requests
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken")

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor to handle token refresh
axiosInstance.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config

    // If error is 401 and we haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      const refreshToken = localStorage.getItem("refreshToken")

      if (refreshToken) {
        try {
          // Try to refresh the token
          const response = await axios.post("http://localhost:8000/api/refresh", {
            refresh_token: refreshToken,
          })

          const newAccessToken = response.data.access_token

          localStorage.setItem("accessToken", newAccessToken)

          // Retry the original request with new token
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`
          return axiosInstance(originalRequest)
        } catch (refreshError) {
          localStorage.removeItem("accessToken")
          localStorage.removeItem("refreshToken")
          localStorage.removeItem("loggedIn")
          localStorage.removeItem("gatewayId")
          localStorage.removeItem("gatewayName")
          router.push("/login")
          return Promise.reject(refreshError)
        }
      } else {
        localStorage.removeItem("accessToken")
        localStorage.removeItem("refreshToken")
        localStorage.removeItem("loggedIn")
        localStorage.removeItem("gatewayId")
        localStorage.removeItem("gatewayName")
        router.push("/login")
      }
    }

    return Promise.reject(error)
  },
)

export default axiosInstance
