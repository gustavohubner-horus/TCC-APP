import { api } from '@/boot/axios'

export async function getGrupos() {
  const response = await api.get('/grupos')
  return response.data
}

export async function addGrupo(nome) {
  const response = await api.post('/grupos', { nome })
  return response.data
}

export async function getGrupo(id) {
  const response = await api.get(`/grupos/${id}`)
  return response.data
}

export async function getMembros(id) {
  const response = await api.get(`/grupos/${id}/membros`)
  return response.data
}

export async function addMembro(id, login) {
  const response = await api.post(`/grupos/${id}/membros`, { login })
  return response.data
}

export async function removeMembro(id, membroId) {
  const response = await api.delete(`/grupos/${id}/membros/${membroId}`)
  return response.data
}

export async function getGastosGrupo(id) {
  const response = await api.get(`/grupos/${id}/gastos`)
  return response.data
}

export async function getFechamento(id) {
  const response = await api.get(`/grupos/${id}/fechamento`)
  return response.data
}
