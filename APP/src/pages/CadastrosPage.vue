<template>
  <q-page class="q-pa-md">
    <q-card flat bordered class="q-mb-md">
      <q-item clickable v-ripple to="/cadastros/categorias">
        <q-item-section avatar>
          <q-icon name="category" color="primary" />
        </q-item-section>
        <q-item-section>Categorias</q-item-section>
        <q-item-section side>
          <q-icon name="chevron_right" />
        </q-item-section>
      </q-item>
    </q-card>

    <q-card flat bordered class="q-mb-md">
      <q-item clickable v-ripple to="/cadastros/limites">
        <q-item-section avatar>
          <q-icon name="savings" color="primary" />
        </q-item-section>
        <q-item-section>Limites por categoria</q-item-section>
        <q-item-section side>
          <q-icon name="chevron_right" />
        </q-item-section>
      </q-item>
    </q-card>

    <q-card flat bordered>
      <q-item clickable v-ripple to="/cadastros/gastos-fixos">
        <q-item-section avatar>
          <q-icon name="event_repeat" color="primary" />
        </q-item-section>
        <q-item-section>Gastos fixos</q-item-section>
        <q-item-section side>
          <q-icon name="chevron_right" />
        </q-item-section>
      </q-item>
    </q-card>
  </q-page>
</template>

<script setup></script>
