import { api } from '@/boot/axios'

export async function getCategorias() {
  const response = await api.get('/categorias')
  return response.data
}

export async function addCategoria(dados) {
  const response = await api.post('/categorias', dados)
  return response.data
}

export async function updateCategoria(id, dados) {
  const response = await api.put(`/categorias/${id}`, dados)
  return response.data
}

export async function deleteCategoria(id) {
  const response = await api.delete(`/categorias/${id}`)
  return response.data
}
