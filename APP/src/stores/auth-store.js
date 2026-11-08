import { defineStore } from 'pinia'
import { api } from '@/boot/axios'

export const useAuthStore = defineStore('auth', {
   state: () => ({
    usuario: JSON.parse(localStorage.getItem('usuario')),
    token: localStorage.getItem('token'),
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
        localStorage.setItem('token', this.token)
        localStorage.setItem('usuario', JSON.stringify(this.usuario))
        return response.data
      } catch (err) {
        this.error = 'Login ou senha inválidos.'
        console.error(this.error, err)
        throw err
      } finally {
        this.loading = false
      }
    },

    sair() {
      this.usuario = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('usuario')
    },

    async cadastrar(dados) {
      this.loading = true
      this.error = null
      try {
        const response = await api.post('/auth/cadastro', dados)
        return response.data
      } catch (err) {
        const detail = err.response?.data?.detail
        if (Array.isArray(detail)) {
          this.error = detail.map((e) => e.msg).join(', ')
        } else {
          this.error = detail || 'Erro ao cadastrar.'
        }
        console.error(this.error, err)
        throw err
      } finally {
        this.loading = false
      }
    },

  },
})