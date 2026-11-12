import { defineStore } from 'pinia'
import * as limiteService from '@/services/limiteService'

export const useLimiteStore = defineStore('limite', {
  state: () => ({
    limites: [],
    loading: false,
    error: null,
  }),

  actions: {
    async carregarLimites() {
      this.loading = true
      this.error = null
      try {
        this.limites = await limiteService.getLimites()
      } catch (err) {
        this.error = 'Erro ao carregar limites.'
        console.error(this.error, err)
      } finally {
        this.loading = false
      }
    },

    async definirLimite(cat_id, valor) {
      await limiteService.definirLimite({ cat_id, valor })
      await this.carregarLimites()
    },

    async removerLimite(id) {
      await limiteService.deleteLimite(id)
      await this.carregarLimites()
    },
  },
})
