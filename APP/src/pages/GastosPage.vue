<template>
  <q-page class="q-pa-md">
    <q-list v-if="gastoStore.gastos.length" bordered separator class="rounded-borders bg-white">
      <q-item v-for="g in gastoStore.gastos" :key="g.gas_id">
        <q-item-section>
          <q-item-label>{{ g.gas_descricao || 'Sem descrição' }}</q-item-label>
          <q-item-label caption>
            {{ formatarData(g.gas_data) }} · {{ nomeCategoria(g.cat_id) }}
          </q-item-label>
        </q-item-section>
        <q-item-section side class="text-weight-medium text-dark">
          {{ formatarValor(g.gas_valor) }}
        </q-item-section>
        <q-item-section side>
          <q-btn flat round dense icon="delete" color="negative" @click="remover(g)" />
        </q-item-section>
      </q-item>
    </q-list>

    <div v-else-if="!gastoStore.loading" class="text-center text-grey q-mt-xl">
      <q-icon name="receipt_long" size="48px" />
      <div class="q-mt-sm">Nenhum gasto registrado.</div>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useGastoStore } from '@/stores/gasto-store'
import { useCategoriaStore } from '@/stores/categoria-store'

const $q = useQuasar()
const gastoStore = useGastoStore()
const catStore = useCategoriaStore()

onMounted(async () => {
  await catStore.carregarCategorias()
  await gastoStore.carregarGastos()
})

function nomeCategoria(catId) {
  if (!catId) return 'Sem categoria'
  const c = catStore.categorias.find((x) => x.cat_id === catId)
  return c ? c.cat_nome : 'Sem categoria'
}

function formatarValor(valor) {
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatarData(data) {
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}

function remover(g) {
  $q.dialog({
    title: 'Excluir gasto',
    message: 'Deseja excluir este gasto?',
    cancel: true,
    ok: { color: 'negative', label: 'Excluir' },
  }).onOk(async () => {
    try {
      await gastoStore.removerGasto(g.gas_id)
      $q.notify({ type: 'positive', message: 'Gasto excluído.' })
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao excluir.' })
    }
  })
}
</script>
