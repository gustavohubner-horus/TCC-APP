<template>
  <q-layout view="hHh lpR fFf">
  <q-header class="bg-white text-dark">
    <q-toolbar class="q-px-xs">
      <q-space />
      <q-btn flat no-caps icon-right="account_circle" label="Gustavo" class="text-subtitle1" />
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