<template>
  <q-layout view="hHh lpR fFf">
    <q-header class="bg-white text-dark">
      <q-toolbar class="q-px-xs">
        <q-space />
        <q-btn
          flat
          no-caps
          icon-right="account_circle"
          :label="authStore.usuario?.usu_nome?.split(' ')[0]"
          class="text-subtitle1"
          to="/perfil"
        />
      </q-toolbar>
    </q-header>

    <q-footer bordered class="bg-white text-grey-7">
      <div class="row q-py-sm">
        <q-btn
          flat stack no-caps size="sm"
          icon="space_dashboard" label="Início"
          class="col"
          :class="{ 'text-primary': ativo('/') }"
          to="/"
        />
        <q-btn
          flat stack no-caps size="sm"
          icon="receipt_long" label="Gastos"
          class="col"
          :class="{ 'text-primary': ativo('/gastos') }"
          to="/gastos"
        />
        <div class="col" />
        <q-btn
          flat stack no-caps size="sm"
          icon="category" label="Cadastros"
          class="col"
          :class="{ 'text-primary': ativo('/cadastros') }"
          to="/cadastros"
        />
        <q-btn
          flat stack no-caps size="sm"
          icon="group" label="Grupos"
          class="col"
          :class="{ 'text-primary': ativo('/grupos') }"
          to="/grupos"
        />
      </div>

      <div class="absolute-center">
        <q-fab icon="add" active-icon="close" direction="up" vertical-actions-align="center" color="primary">
          <q-fab-action color="primary" icon="mic" @click="gravadorAberto = true" />
          <q-fab-action color="primary" icon="photo_camera" @click="abrirCamera" />
          <q-fab-action color="primary" icon="edit" @click="abrirManual" />
        </q-fab>
      </div>
    </q-footer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <input
      ref="inputFoto"
      type="file"
      accept="image/*"
      capture="environment"
      class="hidden"
      @change="onFoto"
    />

    <GastoDialog v-model="dialogGasto" :inicial="gastoInicial" />
    <GravadorAudio v-model="gravadorAberto" @gravado="onGravado" />
  </q-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '@/stores/auth-store'
import { processarGastosFixos } from '@/services/gastoFixoService'
import { gastoPorVoz, gastoPorFoto } from '@/services/iaService'
import GastoDialog from '@/components/GastoDialog.vue'
import GravadorAudio from '@/components/GravadorAudio.vue'

const route = useRoute()
const $q = useQuasar()
const authStore = useAuthStore()

const dialogGasto = ref(false)
const gravadorAberto = ref(false)
const gastoInicial = ref(null)
const inputFoto = ref(null)

onMounted(() => {
  processarGastosFixos().catch(() => {})
})

function ativo(path) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

function abrirManual() {
  gastoInicial.value = null
  dialogGasto.value = true
}

function abrirCamera() {
  inputFoto.value.click()
}

async function onFoto(e) {
  const arquivo = e.target.files[0]
  e.target.value = ''
  if (!arquivo) return
  $q.loading.show({ message: 'Lendo a imagem...' })
  try {
    gastoInicial.value = await gastoPorFoto(arquivo)
    dialogGasto.value = true
  } catch {
    $q.notify({ type: 'negative', message: 'Não foi possível ler a imagem.' })
  } finally {
    $q.loading.hide()
  }
}

async function onGravado(audio) {
  $q.loading.show({ message: 'Entendendo o áudio...' })
  try {
    gastoInicial.value = await gastoPorVoz(audio)
    dialogGasto.value = true
  } catch {
    $q.notify({ type: 'negative', message: 'Não foi possível entender o áudio.' })
  } finally {
    $q.loading.hide()
  }
}
</script>
