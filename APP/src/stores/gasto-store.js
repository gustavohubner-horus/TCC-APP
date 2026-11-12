import { defineStore } from 'pinia'
import * as gastoService from '@/services/gastoService'

export const useGastoStore = defineStore('gasto', {
  state: () => ({
    gastos: [],
    loading: false,
    error: null,
  }),

  actions: {
    async carregarGastos() {
      this.loading = true
      this.error = null
      try {
        this.gastos = await gastoService.getGastos()
      } catch (err) {
        this.error = 'Erro ao carregar gastos.'
        console.error(this.error, err)
      } finally {
        this.loading = false
      }
    },

    async adicionarGasto(dados) {
      const novo = await gastoService.addGasto(dados)
      await this.carregarGastos()
      return novo
    },

    async removerGasto(id) {
      await gastoService.deleteGasto(id)
      await this.carregarGastos()
    },
  },
})
