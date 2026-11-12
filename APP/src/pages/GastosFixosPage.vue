<template>
  <q-page class="q-pa-md">
    <q-list v-if="store.gastosFixos.length" bordered separator class="rounded-borders bg-white">
      <q-item v-for="f in store.gastosFixos" :key="f.gfx_id">
        <q-item-section>
          <q-item-label>
            {{ f.gfx_descricao }}
            <span v-if="!f.gfx_ativo" class="text-grey"> (inativo)</span>
          </q-item-label>
          <q-item-label caption>
            {{ formatar(f.gfx_valor) }} · dia {{ f.gfx_dia }} · {{ nomeCategoria(f.cat_id) }}
          </q-item-label>
        </q-item-section>
        <q-item-section side>
          <div class="row items-center no-wrap">
            <q-btn flat round dense icon="edit" color="grey-7" @click="abrirEditar(f)" />
            <q-btn flat round dense icon="delete" color="negative" @click="remover(f)" />
          </div>
        </q-item-section>
      </q-item>
    </q-list>

    <div v-else-if="!store.loading" class="text-center text-grey q-mt-xl">
      <q-icon name="event_repeat" size="48px" />
      <div class="q-mt-sm">Nenhum gasto fixo cadastrado.</div>
    </div>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn fab icon="add" color="primary" @click="abrirNovo" />
    </q-page-sticky>

    <q-dialog v-model="dialog">
      <q-card style="width: 100%; max-width: 400px;">
        <q-card-section class="text-h6">
          {{ editando ? 'Editar gasto fixo' : 'Novo gasto fixo' }}
        </q-card-section>
        <q-card-section class="q-gutter-md">
          <q-input v-model="descricao" label="Descrição" outlined bg-color="white" />
          <q-input v-model.number="valor" label="Valor" type="number" prefix="R$" outlined bg-color="white" />
          <q-input v-model.number="dia" label="Dia do vencimento" type="number" outlined bg-color="white" />
          <q-select
            v-model="catId"
            :options="opcoesCategorias"
            label="Categoria"
            outlined
            bg-color="white"
            emit-value
            map-options
            clearable
          />
          <q-toggle v-model="ativo" label="Ativo" color="primary" />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat no-caps label="Cancelar" color="grey" v-close-popup />
          <q-btn unelevated no-caps label="Salvar" color="primary" :loading="salvando" @click="salvar" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useGastoFixoStore } from '@/stores/gasto-fixo-store'
import { useCategoriaStore } from '@/stores/categoria-store'

const $q = useQuasar()
const store = useGastoFixoStore()
const catStore = useCategoriaStore()

const dialog = ref(false)
const salvando = ref(false)
const editando = ref(null)

const descricao = ref('')
const valor = ref(null)
const dia = ref(null)
const catId = ref(null)
const ativo = ref(true)

const opcoesCategorias = computed(() =>
  catStore.categorias.map((c) => ({ label: c.cat_nome, value: c.cat_id })),
)

onMounted(async () => {
  await catStore.carregarCategorias()
  await store.carregarGastosFixos()
})

function nomeCategoria(id) {
  if (!id) return 'Sem categoria'
  const c = catStore.categorias.find((x) => x.cat_id === id)
  return c ? c.cat_nome : 'Sem categoria'
}

function formatar(v) {
  return Number(v).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function abrirNovo() {
  editando.value = null
  descricao.value = ''
  valor.value = null
  dia.value = null
  catId.value = null
  ativo.value = true
  dialog.value = true
}

function abrirEditar(f) {
  editando.value = f.gfx_id
  descricao.value = f.gfx_descricao
  valor.value = Number(f.gfx_valor)
  dia.value = f.gfx_dia
  catId.value = f.cat_id
  ativo.value = f.gfx_ativo
  dialog.value = true
}

async function salvar() {
  if (!descricao.value || !descricao.value.trim()) {
    $q.notify({ type: 'negative', message: 'Informe a descrição.' })
    return
  }
  if (!valor.value || valor.value <= 0) {
    $q.notify({ type: 'negative', message: 'Informe um valor válido.' })
    return
  }
  if (!dia.value || dia.value < 1 || dia.value > 31) {
    $q.notify({ type: 'negative', message: 'Informe um dia entre 1 e 31.' })
    return
  }
  const dados = {
    descricao: descricao.value.trim(),
    valor: valor.value,
    dia: dia.value,
    cat_id: catId.value,
    ativo: ativo.value,
  }
  salvando.value = true
  try {
    if (editando.value) {
      await store.atualizarGastoFixo(editando.value, dados)
    } else {
      await store.adicionarGastoFixo(dados)
    }
    $q.notify({ type: 'positive', message: 'Gasto fixo salvo.' })
    dialog.value = false
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao salvar o gasto fixo.' })
  } finally {
    salvando.value = false
  }
}

function remover(f) {
  $q.dialog({
    title: 'Excluir',
    message: `Excluir o gasto fixo "${f.gfx_descricao}"?`,
    cancel: true,
    ok: { color: 'negative', label: 'Excluir' },
  }).onOk(async () => {
    try {
      await store.removerGastoFixo(f.gfx_id)
      $q.notify({ type: 'positive', message: 'Gasto fixo excluído.' })
    } catch {
      $q.notify({ type: 'negative', message: 'Erro ao excluir.' })
    }
  })
}
</script>
