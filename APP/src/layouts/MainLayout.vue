<template>
  <q-layout view="hHh lpR fFf">
  <q-header class="bg-white text-dark">
    <q-toolbar class="q-px-xs">
      <q-btn flat round @click="sair">
        <q-icon name="logout" style="transform: scaleX(-1)" />
      </q-btn>
      <q-space />
      <q-btn flat no-caps icon-right="account_circle" :label="authStore.usuario?.usu_nome?.split(' ')[0]" class="text-subtitle1" />
    </q-toolbar>
  </q-header>

    <q-footer bordered class="bg-white text-grey-7">
      <div class="row q-py-sm">
        <q-btn flat stack no-caps size="sm" icon="space_dashboard" label="Início" class="col text-primary" />
        <q-btn flat stack no-caps size="sm" icon="receipt_long" label="Gastos" class="col" />
        <div class="col"/> 
        <q-btn flat stack no-caps size="sm" icon="category" label="Cadastros" class="col" />
        <q-btn flat stack no-caps size="sm" icon="group" label="Grupos" class="col" />
      </div>

      <div class="absolute-center">
        <q-fab icon="add" active-icon="close" direction="up" vertical-actions-align="center" color="primary">
          <q-fab-action color="primary" icon="mic"/>
          <q-fab-action color="primary" icon="photo_camera"/>
          <q-fab-action color="primary" icon="edit"/>
        </q-fab>
      </div>
    </q-footer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth-store'

const router = useRouter()
const authStore = useAuthStore()

function sair() {
  authStore.sair()
  router.push('/login')
}
</script>