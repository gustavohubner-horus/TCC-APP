<template>
  <q-page class="q-pa-md">
    <q-list v-if="store.grupos.length" bordered separator class="rounded-borders bg-white">
      <q-item
        v-for="g in store.grupos"
        :key="g.gru_id"
        clickable
        v-ripple
        :to="`/grupos/${g.gru_id}`"
      >
        <q-item-section avatar>
          <q-icon name="group" color="primary" />
        </q-item-section>
        <q-item-section>{{ g.gru_nome }}</q-item-section>
        <q-item-section side>
          <q-icon name="chevron_right" />
        </q-item-section>
      </q-item>
    </q-list>

    <div v-else-if="!store.loading" class="text-center text-grey q-mt-xl">
      <q-icon name="group" size="48px" />
      <div class="q-mt-sm">Nenhum grupo ainda.</div>
    </div>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="primary" @click="criar" />
    </q-page-sticky>
  </q-page>
</template>

<script setup>
import { onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useGrupoStore } from '@/stores/grupo-store'

const $q = useQuasar()
const store = useGrupoStore()

onMounted(() => store.carregarGrupos())

function criar() {
  $q.dialog({
    title: 'Novo grupo',
    prompt: { model: '', type: 'text', label: 'Nome do grupo' },
    cancel: true,
  }).onOk(async (nome) => {
    if (!nome || !nome.trim()) return
    try {
      await store.adicionarGrupo(nome.trim())
      $q.notify({ type: 'positive', message: 'Grupo criado.' })
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao criar grupo.' })
    }
  })
}
</script>
