import { defineStore } from 'pinia'
import * as grupoService from '@/services/grupoService'

export const useGrupoStore = defineStore('grupo', {
  state: () => ({
    grupos: [],
    loading: false,
    error: null,
  }),

  actions: {
    async carregarGrupos() {
      this.loading = true
      this.error = null
      try {
        this.grupos = await grupoService.getGrupos()
      } catch (err) {
        this.error = 'Erro ao carregar grupos.'
        console.error(this.error, err)
      } finally {
        this.loading = false
      }
    },

    async adicionarGrupo(nome) {
      await grupoService.addGrupo(nome)
      await this.carregarGrupos()
    },
  },
})
