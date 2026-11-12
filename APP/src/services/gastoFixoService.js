import { api } from '@/boot/axios'

export async function getGastosFixos() {
  const response = await api.get('/gastos-fixos')
  return response.data
}

export async function addGastoFixo(dados) {
  const response = await api.post('/gastos-fixos', dados)
  return response.data
}

export async function updateGastoFixo(id, dados) {
  const response = await api.put(`/gastos-fixos/${id}`, dados)
  return response.data
}

export async function deleteGastoFixo(id) {
  const response = await api.delete(`/gastos-fixos/${id}`)
  return response.data
}

export async function processarGastosFixos() {
  const response = await api.post('/gastos-fixos/processar')
  return response.data
}
