import { api } from '@/boot/axios'

export async function getGastos() {
  const response = await api.get('/gastos')
  return response.data
}

export async function addGasto(dados) {
  const response = await api.post('/gastos', dados)
  return response.data
}

export async function deleteGasto(id) {
  const response = await api.delete(`/gastos/${id}`)
  return response.data
}
