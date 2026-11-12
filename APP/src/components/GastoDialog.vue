<template>
  <q-dialog v-model="aberto">
    <q-card style="width: 100%; max-width: 400px;">
      <q-card-section class="text-h6">Novo gasto</q-card-section>

      <q-card-section class="q-gutter-md">
        <q-input v-model="descricao" label="Descrição" outlined bg-color="white" />
        <q-input
          v-model.number="valor"
          label="Valor"
          type="number"
          prefix="R$"
          outlined
          bg-color="white"
        />
        <q-input v-model="data" label="Data" type="date" stack-label outlined bg-color="white" />
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
        <q-select
          v-model="gruId"
          :options="opcoesGrupos"
          label="Grupo"
          outlined
          bg-color="white"
          emit-value
          map-options
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat no-caps label="Cancelar" color="grey" v-close-popup />
        <q-btn unelevated no-caps label="Salvar" color="primary" :loading="salvando" @click="salvar" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useGastoStore } from '@/stores/gasto-store'
import { useCategoriaStore } from '@/stores/categoria-store'
import { useGrupoStore } from '@/stores/grupo-store'
import { useLimiteStore } from '@/stores/limite-store'

const props = defineProps({
  modelValue: Boolean,
  inicial: { type: Object, default: null },
})
const emit = defineEmits(['update:modelValue'])

const aberto = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

const $q = useQuasar()
const gastoStore = useGastoStore()
const catStore = useCategoriaStore()
const grupoStore = useGrupoStore()
const limiteStore = useLimiteStore()

const descricao = ref('')
const valor = ref(null)
const data = ref(new Date().toISOString().slice(0, 10))
const catId = ref(null)
const gruId = ref(null)
const salvando = ref(false)

const opcoesCategorias = computed(() =>
  catStore.categorias.map((c) => ({ label: c.cat_nome, value: c.cat_id })),
)

const opcoesGrupos = computed(() => [
  { label: 'Pessoal', value: null },
  ...grupoStore.grupos.map((g) => ({ label: g.gru_nome, value: g.gru_id })),
])

watch(aberto, (v) => {
  if (!v) return
  catStore.carregarCategorias()
  grupoStore.carregarGrupos()
  const i = props.inicial
  descricao.value = i?.descricao || ''
  valor.value = i?.valor ?? null
  data.value = i?.data || new Date().toISOString().slice(0, 10)
  catId.value = i?.cat_id ?? null
  gruId.value = i?.gru_id ?? null
})

async function salvar() {
  if (!valor.value || valor.value <= 0) {
    $q.notify({ type: 'negative', message: 'Informe um valor válido.' })
    return
  }
  if (!data.value) {
    $q.notify({ type: 'negative', message: 'Informe a data.' })
    return
  }
  salvando.value = true
  try {
    await gastoStore.adicionarGasto({
      descricao: descricao.value || null,
      valor: valor.value,
      data: data.value,
      cat_id: catId.value,
      gru_id: gruId.value,
    })
    $q.notify({ type: 'positive', message: 'Gasto registrado.' })
    await verificarLimite()
    aberto.value = false
  } catch {
    $q.notify({ type: 'negative', message: 'Erro ao registrar o gasto.' })
  } finally {
    salvando.value = false
  }
}

async function verificarLimite() {
  if (gruId.value || !catId.value) return
  await limiteStore.carregarLimites()
  const limite = limiteStore.limites.find((l) => l.cat_id === catId.value)
  if (!limite) return
  const prefixo = data.value.slice(0, 7)
  const totalCategoria = gastoStore.gastos
    .filter((g) => g.cat_id === catId.value && g.gas_data.startsWith(prefixo))
    .reduce((soma, g) => soma + Number(g.gas_valor), 0)
  const pct = (totalCategoria / Number(limite.lim_valor)) * 100
  if (pct > 100) {
    $q.notify({ type: 'negative', message: 'Você ultrapassou o limite desta categoria.' })
  } else if (pct >= 80) {
    $q.notify({ type: 'warning', message: 'Você está chegando no limite desta categoria.' })
  }
}
</script>
