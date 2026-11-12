import { defineStore } from 'pinia'
import * as categoriaService from '@/services/categoriaService'

export const useCategoriaStore = defineStore('categoria', {
  state: () => ({
    categorias: [],
    loading: false,
    error: null,
  }),

  actions: {
    async carregarCategorias() {
      this.loading = true
      this.error = null
      try {
        this.categorias = await categoriaService.getCategorias()
      } catch (err) {
        this.error = 'Erro ao carregar categorias.'
        console.error(this.error, err)
      } finally {
        this.loading = false
      }
    },

    async adicionarCategoria(nome) {
      const nova = await categoriaService.addCategoria({ nome })
      await this.carregarCategorias()
      return nova
    },

    async atualizarCategoria(id, nome) {
      await categoriaService.updateCategoria(id, { nome })
      await this.carregarCategorias()
    },

    async removerCategoria(id) {
      await categoriaService.deleteCategoria(id)
      await this.carregarCategorias()
    },
  },
})
