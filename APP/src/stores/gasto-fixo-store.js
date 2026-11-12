import { defineStore } from 'pinia'
import * as gastoFixoService from '@/services/gastoFixoService'

export const useGastoFixoStore = defineStore('gastoFixo', {
  state: () => ({
    gastosFixos: [],
    loading: false,
    error: null,
  }),

  actions: {
    async carregarGastosFixos() {
      this.loading = true
      this.error = null
      try {
        this.gastosFixos = await gastoFixoService.getGastosFixos()
      } catch (err) {
        this.error = 'Erro ao carregar gastos fixos.'
        console.error(this.error, err)
      } finally {
        this.loading = false
      }
    },

    async adicionarGastoFixo(dados) {
      await gastoFixoService.addGastoFixo(dados)
      await this.carregarGastosFixos()
    },

    async atualizarGastoFixo(id, dados) {
      await gastoFixoService.updateGastoFixo(id, dados)
      await this.carregarGastosFixos()
    },

    async removerGastoFixo(id) {
      await gastoFixoService.deleteGastoFixo(id)
      await this.carregarGastosFixos()
    },
  },
})
