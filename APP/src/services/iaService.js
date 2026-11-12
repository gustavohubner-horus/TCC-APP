import { api } from '@/boot/axios'

export async function gastoPorVoz(audio) {
  const form = new FormData()
  form.append('audio', audio, 'gravacao.webm')
  const response = await api.post('/ia/gasto-voz', form)
  return response.data
}

export async function gastoPorFoto(imagem) {
  const form = new FormData()
  form.append('imagem', imagem, imagem.name || 'foto.jpg')
  const response = await api.post('/ia/gasto-foto', form)
  return response.data
}
