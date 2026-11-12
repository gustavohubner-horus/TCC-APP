<template>
  <q-page class="q-pa-md">
    <q-list v-if="catStore.categorias.length" bordered separator class="rounded-borders bg-white">
      <q-item v-for="cat in catStore.categorias" :key="cat.cat_id">
        <q-item-section>
          <q-item-label>{{ cat.cat_nome }}</q-item-label>
          <q-item-label caption>
            {{ limiteDe(cat.cat_id) ? formatar(limiteDe(cat.cat_id).lim_valor) : 'Sem limite' }}
          </q-item-label>
        </q-item-section>
        <q-item-section side>
          <div class="row items-center no-wrap">
            <q-btn flat round dense icon="edit" color="grey-7" @click="definir(cat)" />
            <q-btn
              v-if="limiteDe(cat.cat_id)"
              flat round dense icon="delete" color="negative"
              @click="remover(cat)"
            />
          </div>
        </q-item-section>
      </q-item>
    </q-list>

    <div v-else-if="!catStore.loading" class="text-center text-grey q-mt-xl">
      <q-icon name="savings" size="48px" />
      <div class="q-mt-sm">Cadastre categorias primeiro.</div>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useCategoriaStore } from '@/stores/categoria-store'
import { useLimiteStore } from '@/stores/limite-store'

const $q = useQuasar()
const catStore = useCategoriaStore()
const limiteStore = useLimiteStore()

onMounted(async () => {
  await catStore.carregarCategorias()
  await limiteStore.carregarLimites()
})

function limiteDe(catId) {
  return limiteStore.limites.find((l) => l.cat_id === catId)
}

function formatar(valor) {
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function definir(cat) {
  const atual = limiteDe(cat.cat_id)
  $q.dialog({
    title: `Limite de ${cat.cat_nome}`,
    prompt: {
      model: atual ? String(atual.lim_valor) : '',
      type: 'number',
      label: 'Valor (R$)',
    },
    cancel: true,
  }).onOk(async (valor) => {
    const v = Number(valor)
    if (!v || v <= 0) {
      $q.notify({ type: 'negative', message: 'Informe um valor válido.' })
      return
    }
    try {
      await limiteStore.definirLimite(cat.cat_id, v)
      $q.notify({ type: 'positive', message: 'Limite definido.' })
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao definir limite.' })
    }
  })
}

function remover(cat) {
  const atual = limiteDe(cat.cat_id)
  if (!atual) return
  $q.dialog({
    title: 'Remover limite',
    message: `Remover o limite de "${cat.cat_nome}"?`,
    cancel: true,
    ok: { color: 'negative', label: 'Remover' },
  }).onOk(async () => {
    try {
      await limiteStore.removerLimite(atual.lim_id)
      $q.notify({ type: 'positive', message: 'Limite removido.' })
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao remover.' })
    }
  })
}
</script>
