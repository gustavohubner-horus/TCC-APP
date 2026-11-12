import { api } from '@/boot/axios'

export async function getLimites() {
  const response = await api.get('/limites')
  return response.data
}

export async function definirLimite(dados) {
  const response = await api.post('/limites', dados)
  return response.data
}

export async function deleteLimite(id) {
  const response = await api.delete(`/limites/${id}`)
  return response.data
}
