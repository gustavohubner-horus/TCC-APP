import { defineBoot } from '#q-app'
import axios from 'axios'

const api = axios.create({
  baseURL: 'https://hufe-api.onrender.com',
})

api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default defineBoot(({ app }) => {
  app.config.globalProperties.$api = api
})

export { api }
