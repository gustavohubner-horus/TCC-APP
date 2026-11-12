<template>
  <q-page class="q-pa-md">
    <q-list v-if="store.categorias.length" bordered separator class="rounded-borders bg-white">
      <q-item v-for="cat in store.categorias" :key="cat.cat_id">
        <q-item-section>{{ cat.cat_nome }}</q-item-section>
        <q-item-section side>
          <div class="row items-center no-wrap">
            <q-btn flat round dense icon="edit" color="grey-7" @click="editar(cat)" />
            <q-btn flat round dense icon="delete" color="negative" @click="remover(cat)" />
          </div>
        </q-item-section>
      </q-item>
    </q-list>

    <div v-else-if="!store.loading" class="text-center text-grey q-mt-xl">
      <q-icon name="category" size="48px" />
      <div class="q-mt-sm">Nenhuma categoria cadastrada.</div>
    </div>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="primary" @click="adicionar" />
    </q-page-sticky>
  </q-page>
</template>

<script setup>
import { onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useCategoriaStore } from '@/stores/categoria-store'

const $q = useQuasar()
const store = useCategoriaStore()

onMounted(() => store.carregarCategorias())

function adicionar() {
  $q.dialog({
    title: 'Nova categoria',
    prompt: { model: '', type: 'text', label: 'Nome' },
    cancel: true,
  }).onOk(async (nome) => {
    if (!nome || !nome.trim()) return
    try {
      await store.adicionarCategoria(nome.trim())
      $q.notify({ type: 'positive', message: 'Categoria criada.' })
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao criar categoria.' })
    }
  })
}

function editar(cat) {
  $q.dialog({
    title: 'Editar categoria',
    prompt: { model: cat.cat_nome, type: 'text', label: 'Nome' },
    cancel: true,
  }).onOk(async (nome) => {
    if (!nome || !nome.trim()) return
    try {
      await store.atualizarCategoria(cat.cat_id, nome.trim())
      $q.notify({ type: 'positive', message: 'Categoria atualizada.' })
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao atualizar.' })
    }
  })
}

function remover(cat) {
  $q.dialog({
    title: 'Excluir',
    message: `Excluir a categoria "${cat.cat_nome}"?`,
    cancel: true,
    ok: { color: 'negative', label: 'Excluir' },
  }).onOk(async () => {
    try {
      await store.removerCategoria(cat.cat_id)
      $q.notify({ type: 'positive', message: 'Categoria excluída.' })
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao excluir.' })
    }
  })
}
</script>
