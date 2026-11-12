<template>
  <q-page class="q-pa-md">
    <div class="text-h6 q-mb-md">{{ grupo?.gru_nome }}</div>

    <div class="text-subtitle2 q-mb-sm">Participantes</div>
    <q-list bordered separator class="rounded-borders bg-white q-mb-md">
      <q-item v-for="m in membros" :key="m.usu_id">
        <q-item-section>
          <q-item-label>{{ m.usu_nome }}</q-item-label>
          <q-item-label caption>{{ m.usu_login }}</q-item-label>
        </q-item-section>
        <q-item-section side v-if="ehDono && m.usu_id !== grupo.usu_id">
          <q-btn flat round dense icon="person_remove" color="negative" @click="removerMembro(m)" />
        </q-item-section>
      </q-item>
    </q-list>

    <q-btn
      v-if="ehDono"
      outline
      no-caps
      color="primary"
      icon="person_add"
      label="Adicionar membro"
      class="full-width q-mb-lg"
      @click="adicionarMembro"
    />

    <div class="row items-center q-mb-sm">
      <div class="text-subtitle2">Gastos do grupo</div>
      <q-space />
      <q-btn flat no-caps dense color="primary" label="Fechamento" @click="abrirFechamento" />
    </div>

    <q-list v-if="gastos.length" bordered separator class="rounded-borders bg-white">
      <q-item v-for="g in gastos" :key="g.gas_id">
        <q-item-section>
          <q-item-label>{{ g.gas_descricao || 'Sem descrição' }}</q-item-label>
          <q-item-label caption>{{ formatarData(g.gas_data) }} · {{ nomeMembro(g.usu_id) }}</q-item-label>
        </q-item-section>
        <q-item-section side class="text-dark">{{ formatar(g.gas_valor) }}</q-item-section>
        <q-item-section side v-if="g.usu_id === meuId">
          <q-btn flat round dense icon="delete" color="negative" @click="removerGasto(g)" />
        </q-item-section>
      </q-item>
    </q-list>
    <div v-else class="text-grey">Nenhum gasto no grupo.</div>

    <q-dialog v-model="dialogFechamento">
      <q-card style="width: 100%; max-width: 400px;">
        <q-card-section class="text-h6">Fechamento</q-card-section>
        <q-list separator>
          <q-item v-for="f in fechamento" :key="f.usu_id">
            <q-item-section>
              <q-item-label>{{ f.nome }}</q-item-label>
              <q-item-label caption>Pagou {{ formatar(f.pago) }} de {{ formatar(f.cota) }}</q-item-label>
            </q-item-section>
            <q-item-section side :class="Number(f.saldo) >= 0 ? 'text-positive' : 'text-negative'">
              {{ Number(f.saldo) >= 0 ? 'recebe ' : 'deve ' }}{{ formatar(Math.abs(Number(f.saldo))) }}
            </q-item-section>
          </q-item>
        </q-list>
        <q-card-actions align="right">
          <q-btn flat no-caps label="Fechar" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '@/stores/auth-store'
import * as grupoService from '@/services/grupoService'
import { deleteGasto } from '@/services/gastoService'

const route = useRoute()
const $q = useQuasar()
const authStore = useAuthStore()

const grupoId = route.params.id

const grupo = ref(null)
const membros = ref([])
const gastos = ref([])
const fechamento = ref([])
const dialogFechamento = ref(false)

const ehDono = computed(() => grupo.value && grupo.value.usu_id === authStore.usuario?.usu_id)
const meuId = computed(() => authStore.usuario?.usu_id)

onMounted(carregar)

async function carregar() {
  try {
    grupo.value = await grupoService.getGrupo(grupoId)
    membros.value = await grupoService.getMembros(grupoId)
    gastos.value = await grupoService.getGastosGrupo(grupoId)
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao carregar o grupo.' })
  }
}

function nomeMembro(id) {
  const m = membros.value.find((x) => x.usu_id === id)
  return m ? m.usu_nome : ''
}

function formatar(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatarData(data) {
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}

function adicionarMembro() {
  $q.dialog({
    title: 'Adicionar membro',
    prompt: { model: '', type: 'text', label: 'Login do usuário' },
    cancel: true,
  }).onOk(async (login) => {
    if (!login || !login.trim()) return
    try {
      await grupoService.addMembro(grupoId, login.trim())
      $q.notify({ type: 'positive', message: 'Membro adicionado.' })
      membros.value = await grupoService.getMembros(grupoId)
    } catch (err) {
      $q.notify({ type: 'negative', message: err.response?.data?.detail || 'Erro ao adicionar.' })
    }
  })
}

function removerMembro(m) {
  $q.dialog({
    title: 'Remover',
    message: `Remover ${m.usu_nome} do grupo?`,
    cancel: true,
    ok: { color: 'negative', label: 'Remover' },
  }).onOk(async () => {
    try {
      await grupoService.removeMembro(grupoId, m.usu_id)
      $q.notify({ type: 'positive', message: 'Membro removido.' })
      membros.value = await grupoService.getMembros(grupoId)
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao remover.' })
    }
  })
}

function removerGasto(g) {
  $q.dialog({
    title: 'Excluir gasto',
    message: 'Deseja excluir este gasto do grupo?',
    cancel: true,
    ok: { color: 'negative', label: 'Excluir' },
  }).onOk(async () => {
    try {
      await deleteGasto(g.gas_id)
      $q.notify({ type: 'positive', message: 'Gasto excluído.' })
      gastos.value = await grupoService.getGastosGrupo(grupoId)
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao excluir.' })
    }
  })
}

async function abrirFechamento() {
  try {
    fechamento.value = await grupoService.getFechamento(grupoId)
    dialogFechamento.value = true
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao calcular o fechamento.' })
  }
}
</script>
