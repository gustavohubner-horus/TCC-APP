import { defineStore } from 'pinia'
import { api } from '@/boot/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    usuario: null,
    token: null,
    loading: false,
    error: null,
  }),

  actions: {
    async entrar(login, senha) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/auth/login', { login, senha })
        this.token = response.data.access_token
        this.usuario = response.data.usuario
        return response.data
      } catch (err) {
        this.error = 'Login ou senha inválidos.'
        console.error(this.error, err)
        throw err
      } finally {
        this.loading = false
      }
    },
  },
})